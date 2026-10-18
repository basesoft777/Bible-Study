#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KJV_SZOVEG_M0_meres.py -- #118 (F118, KJV_SZOVEG) M0 mérőkódja. Csak olvas; a generátorba nem kerül.

Bemenet: --zip <a felhasznalo altal letoltott eng-kjv_usfm.zip>  (kibontas nelkul, zipfile-lal olvasva)
Kimenet (stdout): a mérés összesítője; fájlok:
  naplok/KJV_SZOVEG_M0_jelolok.tsv       az USFM-jelölőleltár (66 kanonikus könyv), kontextusonként
  naplok/KJV_SZOVEG_M0_versnelkuli.tsv   a vers nélküli, szöveget hordozó sorok (\\c után), és hova fűzné őket az F19-parszoló
  naplok/KJV_SZOVEG_M0_strong_elteres.tsv  csak ha az új csomag F19-parse-a eltér a KJV_Strongs_teljes.tsv-től

Három mérés:
  A. a zip azonossága és fájllistája (66 kanonikus / apokrif / egyéb), az F06-mérés megismétlése (fj2/kjv_asv.usfm_meres)
  B. az F19-parse (eszkozok/f19_ebible_import.olvas_zip + ir_teljes, változatlanul importálva) az új csomagon,
     összevetve a konkordancia/KJV_Strongs_teljes.tsv-vel: versek halmaza, Strong-címkék, szavak, bájtszintű tábla-egyezés
  C. az USFM-jelölőleltár és a vers nélküli sorok csapdája

Futtatás:  python -I naplok/KJV_SZOVEG_M0_meres.py --zip C:/Users/bases/Desktop/kjv_munka/kjv.zip
TSV-olvasás/írás: split('\\t') / '\\t'.join(), csv modul nélkül.
"""

import argparse
import collections
import datetime
import hashlib
import os
import re
import sys
import tempfile
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'fj2'))
import f19_ebible_import as f19  # noqa: E402
import kjv_asv as f06  # noqa: E402

BS = chr(92)
E = re.escape(BS)
RE_JEL = re.compile(E + r'(\+?)([a-z]+[0-9]*)(\*?)')
RE_WATTR = re.compile(E + r'\+?w ([^|' + E + r']*)\|([^' + E + r']*?)' + E + r'\+?w\*')
RE_KULCS = re.compile(r'([a-zA-Z-]+)="')
TABLA = os.path.join(REPO, 'konkordancia', 'KJV_Strongs_teljes.tsv')
NAPLO = os.path.join(REPO, 'naplok')

APOKRIF = set('TOB JDT ESG WIS SIR BAR S3Y SUS BEL 1MA 2MA 1ES MAN 2ES'.split())


def fajllista(z, konyvek):
    kan = {u for _, u in konyvek}
    out = collections.defaultdict(list)
    for n in z.namelist():
        m = re.match(r'^[0-9]+-([0-9A-Z]{3})eng-kjv\.usfm$', n)
        if not m:
            out['egyeb_nem_usfm'].append(n)
        elif m.group(1) in kan:
            out['kanonikus'].append(m.group(1))
        elif m.group(1) in APOKRIF:
            out['apokrif'].append(m.group(1))
        else:
            out['egyeb_usfm'].append(m.group(1))
    return out


def jelololeltar(szoveg):
    """-> Counter[(jelolo, nyito|zaro, kontextus)], Counter[w-attr-kulcs], egyeb szamlalok"""
    c = collections.Counter()
    attr = collections.Counter()
    egyeb = collections.Counter()
    fej = True
    for sor in szoveg.split('\n'):
        if re.match(E + r'c [0-9]+', sor):
            fej = False
        labj = None  # 'f' vagy 'x' -- egy soron beluli lab-/kereszthivatkozas-allapot
        for m in RE_JEL.finditer(sor):
            nev, zaro = m.group(2), m.group(3) == '*'
            if fej:
                ktx = 'fejlec'
            elif labj:
                ktx = 'labjegyzet' if labj == 'f' else 'kereszthiv'
            else:
                ktx = 'szoveg'
            if nev in ('f', 'x', 'fe') and not zaro:
                labj = 'x' if nev == 'x' else 'f'
                ktx = 'labjegyzet' if labj == 'f' else 'kereszthiv'
            elif nev in ('f', 'x', 'fe') and zaro:
                labj = None
            c[(nev, 'zaro' if zaro else 'nyito', ktx, 'beagyazott' if m.group(1) else '')] += 1
        for mw in RE_WATTR.finditer(sor):
            kulcsok = tuple(sorted(RE_KULCS.findall(mw.group(2))))
            attr[kulcsok] += 1
            if 'strong' not in kulcsok:
                egyeb['w_strong_nelkul'] += 1
            if ' ' in mw.group(1).strip():
                egyeb['w_tobbszavas'] += 1
        egyeb['pilcrow'] += sor.count('\u00b6')
        if not fej:
            tiszta = f19.RE_FN.sub('', sor)
            tiszta = RE_JEL.sub('', tiszta)
            for ch in tiszta:
                if ord(ch) > 127 and ch != '\u00b6':
                    egyeb['nem_ascii:U+%04X' % ord(ch)] += 1
        # tobbsoros labjegyzet (a sor vegen nyitva marad) -- az F19 RE_FN re.S-sel kezeli, itt csak szamoljuk
        egyeb['labjegyzet_tobbsoros'] += max(0, len(re.findall(E + r'f ', sor)) - sor.count(BS + 'f*'))
    return c, attr, egyeb


def versnelkuli(step, szoveg):
    """A \\c utani, \\v-t nem tartalmazo, (labjegyzet- es jelolotisztitas utan) szoveget hordozo sorok,
    es az F19 parse_usfm-logika szerinti 'aktualis vers', amelyhez a szoveg hozzafuzodne (None: eldobna)."""
    out = []
    szoveg = f19.RE_FN.sub('', szoveg)
    fej = None
    vers = None
    for sor in szoveg.split('\n'):
        m = re.match(E + r'c ([0-9]+)', sor)
        if m:
            fej = int(m.group(1))
            vers = None
            continue
        if fej is None:
            continue
        if sor.startswith(BS + 'd ') or sor == BS + 'd':
            vers = 0
        vs = list(f19.RE_V.finditer(sor))
        elotte = sor[:vs[0].start()] if vs else sor
        tiszta = f19.RE_W.sub(lambda mw: mw.group(1), elotte)
        tiszta = f19.RE_MARK.sub(' ', tiszta)
        tiszta = re.sub(r'\s+', ' ', tiszta).strip()
        if tiszta:
            mj = RE_JEL.match(sor.strip())
            elso = mj.group(2) if mj else '(nincs)'
            out.append((step, fej, vers, elso, tiszta, sor.strip()[:120]))
        if vs:
            vers = int(vs[-1].group(1))
    return out


def olvas_tabla():
    fejsorok, sorok = [], []
    for s in open(TABLA, encoding='utf-8').read().split('\n'):
        if not s:
            continue
        if s.startswith('#'):
            fejsorok.append(s)
            continue
        c = s.split('\t')
        if c[0] == 'Igehely':
            continue
        sorok.append((c[0], int(c[1]), c[2], c[3]))
    return fejsorok, sorok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', required=True)
    a = ap.parse_args()
    zp = a.zip
    nyers = open(zp, 'rb').read()
    sha = hashlib.sha256(nyers).hexdigest()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    prov = 'scope=KJV_SZOVEG M0 (66 kanonikus könyv; fájllista: a teljes zip) | forras=%s sha256=%s (%d bájt) + konkordancia/KJV_Strongs_teljes.tsv | ts=%s' % (
        os.path.basename(zp), sha, len(nyers), ts)
    print('# proveniencia:', prov)
    konyvek = f19.lista_konyvek()
    z = zipfile.ZipFile(zp)

    # ---- A. fajllista + F06-meres
    fl = fajllista(z, konyvek)
    print('A1 fajllista: bejegyzes=%d; kanonikus=%d; apokrif=%d (%s); egyeb_usfm=%s; nem_usfm=%s' % (
        len(z.namelist()), len(fl['kanonikus']), len(fl['apokrif']), ' '.join(sorted(fl['apokrif'])),
        ' '.join(fl['egyeb_usfm']) or '-', ' '.join(fl['egyeb_nem_usfm']) or '-'))
    hiany = sorted({u for _, u in konyvek} - set(fl['kanonikus']))
    print('A1 hianyzo kanonikus konyv:', ' '.join(hiany) or '0')
    datumok = collections.Counter(i.date_time for i in z.infolist())
    print('A1 bejegyzes-datumok:', dict(datumok))
    # copr.htm: a licencek.tsv KJV_Strongs_teljes soraban idezett mondatok megvannak-e szo szerint (adat, nem utasitas)
    if 'copr.htm' in z.namelist():
        cp = re.sub(r'<[^>]+>', ' ', z.read('copr.htm').decode('utf-8', 'replace'))
        cp = re.sub(r'\s+', ' ', cp)
        for idez in ('Public Domain', 'You may copy the King James Version of the Holy Bible freely.',
                     'This royal decree has no effect outside of the UK, where this work is firmly in the Public Domain.',
                     'courtesy of the Crosswire Bible Society and eBible.org'):
            print('A1b copr.htm tartalmazza: %s -> %s' % (idez[:60], idez in cp))
        print('A1b copr.htm datum-sor:', ' | '.join(sorted(set(re.findall(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}', cp)))))
    szovegek = [(n, z.read(n).decode('utf-8-sig')) for n in z.namelist() if n.endswith('.usfm')]
    r = f06.usfm_meres(szovegek)
    print('A2 F06-meres (fj2/kjv_asv.usfm_meres): konyv=%d vers=%d vers_strongos=%d strong_cimke=%d; kanoni66: konyv=%d vers=%d vers_strongos=%d' % r)
    print('A2 F06 2026-09-29 (naplok/F06_kjv_asv.tsv): konyv=81 vers=36822 vers_strongos=31099 strong_cimke=349308; kanoni66: konyv=66 vers=31102 vers_strongos=31099')

    # ---- B. F19-parse az uj csomagon vs KJV_Strongs_teljes.tsv
    adat, anom, hidak = f19.olvas_zip(zp, 'kjv', konyvek)
    T_all = {(s, f, v) for s, _ in konyvek for (f, v) in adat[s]}
    T_cimkes = {(s, f, v) for s, _ in konyvek for (f, v), rec in adat[s].items() if rec['szavak']}
    kan = [k for k in T_all if k[2] > 0]
    v0 = [k for k in T_all if k[2] == 0]
    print('B1 uj csomag F19-parse: kanonikus versek (v>0)=%d, ebbol cimkes=%d, cimke nelkuli=%d (%s); 0. versek=%d, ebbol cimkes=%d; vershidak=%d; parse-anomalia=%d' % (
        len(kan), sum(1 for k in kan if k in T_cimkes), sum(1 for k in kan if k not in T_cimkes),
        ' '.join('%s.%d.%d' % k for k in sorted(k for k in kan if k not in T_cimkes)),
        len(v0), sum(1 for k in v0 if k in T_cimkes), hidak, len(anom)))
    ures = sorted(k for k in T_all if not adat[k[0]][(k[1], k[2])]['szoveg'])
    print('B1 ures szoveg (F19-tisztitas utan): %d %s' % (len(ures), ' '.join('%s.%d.%d' % k for k in ures)))
    # az F19 'szoveg' mezoje olvasoszovegkent: szokoz az irasjel elott (a zaro jelolo helyen), pilcrow
    szk = sorted(k for k in T_all if re.search(r' [,.;:?!)]', adat[k[0]][(k[1], k[2])]['szoveg']))
    pk = sum(1 for k in T_all if '¶' in adat[k[0]][(k[1], k[2])]['szoveg'])
    print('B1b F19-szoveg: szokoz irasjel elott=%d vers (pl. %s); pilcrow-t tartalmaz=%d vers' % (
        len(szk), ' | '.join('%s.%d.%d: %s' % (k + (adat[k[0]][(k[1], k[2])]['szoveg'][:90],)) for k in szk[:2]), pk))
    for ih in (('Psa', 119, 8), ('Rom', 16, 27), ('Gen', 1, 2)):
        print('B1c F19-szoveg %s.%d.%d: %s' % (ih + (adat[ih[0]][(ih[1], ih[2])]['szoveg'],)))
    tfej, tsorok = olvas_tabla()
    S = set()
    for ih, _i, _s, _w in tsorok:
        b, f, v = ih.split('.')
        S.add((b, int(f), int(v)))
    print('B2 versek: |S| (tabla)=%d (v>0: %d, v=0: %d); |T_cimkes|=%d; |T_osszes|=%d' % (
        len(S), sum(1 for k in S if k[2] > 0), sum(1 for k in S if k[2] == 0), len(T_cimkes), len(T_all)))
    print('B2 S - T_osszes=%d; T_cimkes - S=%d; S - T_cimkes=%d; T_osszes - S=%d (v>0: %s; v=0: %d)' % (
        len(S - T_all), len(T_cimkes - S), len(S - T_cimkes), len(T_all - S),
        ' '.join('%s.%d.%d' % k for k in sorted(T_all - S) if k[2] > 0), sum(1 for k in T_all - S if k[2] == 0)))
    # sorszintu osszevetes
    uj = []
    for s, _ in konyvek:
        for (f, v) in sorted(adat[s]):
            for i, (st, szo) in enumerate(adat[s][(f, v)]['szavak'], 1):
                uj.append(('%s.%d.%d' % (s, f, v), i, st, szo))
    print('B3 Strong-cimkek: tabla=%d; uj=%d' % (len(tsorok), len(uj)))
    tv = collections.Counter(r_[0] for r_ in tsorok)
    uv = collections.Counter(r_[0] for r_ in uj)
    print('B3 versenkenti cimkeszam elter: %d vers' % sum(1 for k in set(tv) | set(uv) if tv[k] != uv[k]))
    tk3 = {(r_[0], r_[1], r_[2]) for r_ in tsorok}
    uk3 = {(r_[0], r_[1], r_[2]) for r_ in uj}
    print('B3 (vers, szosorszam, Strong) egyezes: kozos=%d; csak_tabla=%d; csak_uj=%d' % (len(tk3 & uk3), len(tk3 - uk3), len(uk3 - tk3)))
    tk4 = set(tsorok)
    uk4 = set(uj)
    print('B4 (vers, szosorszam, Strong, Angol szo) egyezes: kozos=%d; csak_tabla=%d; csak_uj=%d' % (len(tk4 & uk4), len(tk4 - uk4), len(uk4 - tk4)))
    print('B4 sorrend is azonos (lista-egyenloseg):', tsorok == uj)
    kulcs = collections.Counter(r_[2] for r_ in uj)
    print('B5 kulcs-Strongok (uj): ' + ' '.join('%s=%d' % (k, kulcs[k]) for k in ('H430', 'H776', 'H1', 'H3068', 'G746', 'G2316')))
    print('B5 kulcs-Strongok (tabla fejlece): ' + tfej[2].split('darabszáma: ')[-1])
    # bajtszintu: ir_teljes a tabla sajat fejlecsoraival, ideiglenes konyvtarba (repon kivul)
    tmp = tempfile.mkdtemp(prefix='kjv_m0_')
    ki = os.path.join(tmp, 'KJV_Strongs_teljes.tsv')
    f19.ir_teljes(ki, adat, konyvek, tfej)
    b_uj = open(ki, 'rb').read()
    b_regi = open(TABLA, 'rb').read()
    print('B6 ir_teljes(uj csomag, a tabla fejlecsoraival) == KJV_Strongs_teljes.tsv bajtra: %s (sha256 uj=%s, tabla=%s)' % (
        b_uj == b_regi, hashlib.sha256(b_uj).hexdigest()[:16], hashlib.sha256(b_regi).hexdigest()[:16]))
    os.remove(ki)
    os.rmdir(tmp)
    if tsorok != uj:
        el = os.path.join(NAPLO, 'KJV_SZOVEG_M0_strong_elteres.tsv')
        with open(el, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# proveniencia: ' + prov + '\n')
            fh.write('\t'.join(['irany', 'Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó']) + '\n')
            for r_ in sorted(tk4 - uk4):
                fh.write('\t'.join(['csak_tabla', r_[0], str(r_[1]), r_[2], r_[3]]) + '\n')
            for r_ in sorted(uk4 - tk4):
                fh.write('\t'.join(['csak_uj', r_[0], str(r_[1]), r_[2], r_[3]]) + '\n')
        print('B7 elteresek:', el)

    # ---- C. jelololeltar + vers nelkuli sorok (66 kanonikus konyv)
    fajlok = {}
    for n in z.namelist():
        m = re.match(r'^[0-9]+-([0-9A-Z]{3})eng-kjv\.usfm$', n)
        if m:
            fajlok[m.group(1)] = n
    C = collections.Counter()
    A = collections.Counter()
    X = collections.Counter()
    VN = []
    for s, u in konyvek:
        t = z.read(fajlok[u]).decode('utf-8-sig')
        c, at, eg = jelololeltar(t)
        C.update(c)
        A.update(at)
        X.update(eg)
        VN += versnelkuli(s, t)
    with open(os.path.join(NAPLO, 'KJV_SZOVEG_M0_jelolok.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# proveniencia: ' + prov + '\n')
        fh.write('# kontextus: fejlec = az elso \\c elott; labjegyzet = \\f…\\f* kozott; kereszthiv = \\x…\\x* kozott; szoveg = minden mas. beagyazott = \\+jelolo\n')
        fh.write('\t'.join(['jelolo', 'nyito_zaro', 'kontextus', 'beagyazott', 'db']) + '\n')
        for k, n in sorted(C.items(), key=lambda kv: (-kv[1], kv[0])):
            fh.write('\t'.join(list(k) + [str(n)]) + '\n')
    print('C1 jelolok (jelolo, nyito/zaro, kontextus, beagyazott) -> db:')
    for k, n in sorted(C.items(), key=lambda kv: (-kv[1], kv[0])):
        print('   ', '\t'.join(k), n)
    print('C2 \\w attributum-kulcsok:', dict(A))
    print('C3 egyeb:', dict(sorted(X.items())))
    with open(os.path.join(NAPLO, 'KJV_SZOVEG_M0_versnelkuli.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# proveniencia: ' + prov + '\n')
        fh.write('# a \\c utani, \\v elotti (vagy \\v nelkuli) szoveghordozo sorok; f19_vers = az F19 parse_usfm aktualis verse, amelyhez a szoveg hozzafuzodne (ures: eldobna)\n')
        fh.write('\t'.join(['konyv', 'fejezet', 'f19_vers', 'elso_jelolo', 'tiszta_szoveg', 'nyers_sor']) + '\n')
        for r_ in VN:
            fh.write('\t'.join(['' if x is None else str(x) for x in r_]) + '\n')
    vc = collections.Counter((r_[3], 'eldobna' if r_[2] is None else ('0. vers' if r_[2] == 0 else 'elozo vershez fuzne')) for r_ in VN)
    print('C4 vers nelkuli szoveghordozo sorok: %d; (elso jelolo, F19-sors) -> db: %s' % (len(VN), dict(vc)))
    zs = [r_ for r_ in VN if r_[0] == 'Psa' and r_[1] == 119]
    print('C5 Zsolt 119: %d fejlec-sor; eldobna=%d; elozo vershez fuzne=%d (pl. %s)' % (
        len(zs), sum(1 for r_ in zs if r_[2] is None), sum(1 for r_ in zs if r_[2]),
        '; '.join('119:%s <- %s' % (r_[2], r_[4]) for r_ in zs[1:3])))
    egyeb = [r_ for r_ in VN if r_[3] != 'd' and not (r_[0] == 'Psa' and r_[1] == 119)]
    print('C6 egyeb (nem \\d, nem Zsolt 119) vers nelkuli sorok: %d' % len(egyeb))
    for r_ in egyeb[:40]:
        print('   ', r_)


if __name__ == '__main__':
    main()
