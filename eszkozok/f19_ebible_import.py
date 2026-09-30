#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f19_ebible_import.py -- F19 (FELADATOK #19, N29): a Strong-cimkes KJV es ASV teljes importja az eBible USFM-bol,
es a cimkezetlen versek besorolasa (luvlylavnder/bible-app-data keresztellenorzessel).

Bemenet (--munka mappa):
  kjv.zip, asv.zip      az https://ebible.org/Scriptures/eng-kjv_usfm.zip / eng-asv_usfm.zip (a szkript nem tolt le)
  luv/                  a luvlylavnder/bible-app-data klonja (Bible-Versions/KJV-Strongs, ASV-Strongs)
Kimenet:
  konkordancia/KJV_Strongs_teljes.tsv   Igehely | Szosorszam | Strong-szam | Angol szo | Morfologiai kod (ures)
  konkordancia/ASV_Strongs_teljes.tsv   ugyanaz (az ASV-forras nem ad morfologiai kodot; az oszlop ures)
  naplok/F19_hianyok.tsv                a cimke nelkuli versek besorolasa + a forras/licenc/meres fejlecsorai

Szabalyok: csak az 5 oszlopos, a KJV_Strongs_*.tsv-vel azonos formatum; a Strong-szam nullak nelkul (H0430 -> H430,
mint a BSB_Strongs.tsv-ben); a Strong-cimke nelkuli szavak nincsenek benne; a zsoltarfelirat (\\d) verse 0;
a versszamozas a forras (angol, KJV-) szamozasa, nem MT. TSV-olvasas/iras: split/join, csv modul nelkul.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BS = chr(92)
E = re.escape(BS)
RE_FN = re.compile(E + r'f ' + r'.*?' + E + r'f\*', re.S)
RE_W = re.compile(E + r'[+]?w ([^|' + E + r']*)\|([^' + E + r']*?)' + E + r'[+]?w\*')
RE_STRONG = re.compile(r'strong="([HG])0*([0-9]+)"')
RE_MARK = re.compile(E + r'[+]?[a-z]+[0-9]*[*]?')
RE_V = re.compile(E + r'v ([0-9]+)(?:-([0-9]+))?')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lista_konyvek():
    """[(STEP-rovidites, USFM-azonosito)] kanonikus sorrendben, a Konyv_normalizalo_tabla.tsv-bol."""
    sorok = open(os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8').read().split('\n')
    out = []
    for s in sorok[1:]:
        if not s.strip():
            continue
        step = s.split('\t')[0]
        out.append((step, step.upper()))
    assert len(out) == 66, len(out)
    return out


def parse_usfm(szoveg):
    """-> {(fejezet, vers): {'szavak': [(strong, szo)], 'szoveg': str}}; anomaliak: [(fejezet, szoveg-eleje)]"""
    szoveg = RE_FN.sub('', szoveg)
    versek = {}
    anomalia = []
    fej = None
    vers = None
    hidak = 0
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
        # egy soron belul tobb vers is lehet (sor elejen \v)
        darabok = []
        pos = 0
        for mv in RE_V.finditer(sor):
            if mv.start() > pos:
                darabok.append((vers, sor[pos:mv.start()]))
            vers = int(mv.group(1))
            if mv.group(2):
                hidak += 1
            pos = mv.end()
        darabok.append((vers, sor[pos:]))
        for v, d in darabok:
            szavak = []
            for mw in RE_W.finditer(d):
                ms = RE_STRONG.search(mw.group(2))
                if not ms:
                    anomalia.append((fej, 'strong_attr_ertelmezhetetlen: ' + mw.group(0)[:60]))
                    continue
                szavak.append((ms.group(1) + ms.group(2), mw.group(1).strip()))
            tiszta = RE_W.sub(lambda mw: mw.group(1), d)
            tiszta = RE_MARK.sub(' ', tiszta)
            tiszta = re.sub(r'\s+', ' ', tiszta).strip()
            if v is None:
                if szavak:
                    anomalia.append((fej, 'cimkezett_szo_verson_kivul: ' + d[:60]))
                continue
            rec = versek.setdefault((fej, v), {'szavak': [], 'szoveg': ''})
            rec['szavak'].extend(szavak)
            rec['szoveg'] = (rec['szoveg'] + ' ' + tiszta).strip()
    return versek, anomalia, hidak


def olvas_zip(zippath, ver, konyvek):
    """-> {step: {(fej, vers): rec}}, anomaliak, hidak"""
    z = zipfile.ZipFile(zippath)
    fajlok = {}
    for n in z.namelist():
        m = re.match(r'^[0-9]+-([0-9A-Z]{3})eng-' + ver + r'\.usfm$', n)
        if m:
            fajlok[m.group(1)] = n
    out, anom, hidak = {}, [], 0
    for step, usfm in konyvek:
        if usfm not in fajlok:
            raise SystemExit('hianyzo USFM-fajl: %s (%s)' % (usfm, ver))
        t = z.read(fajlok[usfm]).decode('utf-8-sig')
        v, a, h = parse_usfm(t)
        out[step] = v
        anom += [(step, f, s) for f, s in a]
        hidak += h
    return out, anom, hidak


def olvas_luv(mappa, almappa, fajl, konyvek):
    """-> {step: {(fej, vers): [strongok]}}"""
    d = json.load(open(os.path.join(mappa, 'Bible-Versions', almappa, fajl), encoding='utf-8'))
    out = {s: {} for s, _ in konyvek}
    for r in d['verses']:
        step = konyvek[r['book'] - 1][0]
        st = [a + b for a, b in re.findall(r'[{]([HG])0*([0-9]+)[}]', r['text'])]
        out[step][(r['chapter'], r['verse'])] = (st, len(r['text'].strip()))
    return out


def ir_teljes(fajl, adat, konyvek):
    sorok = ['\t'.join(['Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó', 'Morfológiai kód'])]
    n = 0
    for step, _ in konyvek:
        for (f, v) in sorted(adat[step]):
            for i, (st, szo) in enumerate(adat[step][(f, v)]['szavak'], 1):
                sorok.append('\t'.join(['%s.%d.%d' % (step, f, v), str(i), st, szo, '']))
                n += 1
    with open(fajl, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(sorok) + '\n')
    return n


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--munka', required=True)
    a = ap.parse_args()
    konyvek = lista_konyvek()
    M = a.munka
    fejsorok = []
    hianyok = []
    stat = {}
    ts = datetime.date.today().isoformat()
    luv_commit = os.popen('git -C "%s" rev-parse HEAD' % os.path.join(M, 'luv')).read().strip()
    for ver, VER, luvdir, luvfile in (('kjv', 'KJV', 'KJV-Strongs', 'kjv_strongs.json'), ('asv', 'ASV', 'ASV-Strongs', 'asvs.json')):
        zp = os.path.join(M, ver + '.zip')
        adat, anom, hidak = olvas_zip(zp, ver, konyvek)
        luv = olvas_luv(os.path.join(M, 'luv'), luvdir, luvfile, konyvek)
        ki = os.path.join(REPO, 'konkordancia', VER + '_Strongs_teljes.tsv')
        sor_db = ir_teljes(ki, adat, konyvek)
        vers_db = sum(len(adat[s]) for s, _ in konyvek)
        vers0 = sum(1 for s, _ in konyvek for (f, v) in adat[s] if v == 0)
        vers_kan = vers_db - vers0
        vers_cimkes = sum(1 for s, _ in konyvek for (f, v) in adat[s] if v > 0 and adat[s][(f, v)]['szavak'])
        # koordinata-halmaz egyezes a luv-vel
        kul_e = kul_l = 0
        koord_kul = []
        for s, _ in konyvek:
            e = set(k for k in adat[s] if k[1] > 0)
            l = set(luv[s])
            for k in sorted(e - l):
                koord_kul.append((s, k, 'csak_ebible'))
            for k in sorted(l - e):
                koord_kul.append((s, k, 'csak_luv'))
        # Strong-halmaz egyezes verseken (mindket forrasban cimkes)
        egyezik = osszes = 0
        for s, _ in konyvek:
            for k, rec in adat[s].items():
                if k[1] == 0 or k not in luv[s]:
                    continue
                es = set(x for x, _ in rec['szavak'])
                ls = set(luv[s][k][0])
                if es and ls:
                    osszes += 1
                    egyezik += 1 if es == ls else 0
        # meglevo studybible-tabla (Gen, Exo, Pro) egyezese
        regi_egy = regi_ossz = 0
        regi_fajl = {'KJV': ['Genesis', 'Exodus', 'Proverbs'], 'ASV': ['Genesis', 'Exodus', 'Proverbs']}[VER]
        for nev in regi_fajl:
            regi = {}
            fp = os.path.join(REPO, 'konkordancia', '%s_Strongs_%s.tsv' % (VER, nev))
            for i, s in enumerate(open(fp, encoding='utf-8').read().split('\n')):
                if i == 0 or not s.strip():
                    continue
                c = s.split('\t')
                m = re.match(r'^([0-9A-Za-z]+)[.]([0-9]+)[.]([0-9]+)$', c[0])
                regi.setdefault((m.group(1), int(m.group(2)), int(m.group(3))), set()).add(c[2])
            for (b, f, v), st in regi.items():
                rec = adat[b].get((f, v))
                if not rec:
                    continue
                es = set(x for x, _ in rec['szavak'])
                regi_ossz += 1
                regi_egy += 1 if es == st else 0
        # hianyok
        for s, _ in konyvek:
            for k in sorted(adat[s]):
                f, v = k
                rec = adat[s][k]
                if v == 0 or rec['szavak']:
                    continue
                hl = luv[s].get(k)
                tl = len(rec['szoveg'])
                if tl == 0:
                    osz = 'ures_vers_forras'
                    ind = 'a vers jelolo megvan, de nincs szovege az eBible-ben (kritikai szovegkiadas / versszamozasi eltérés); szabalyalapu'
                    allapot = 'szabaly'
                elif hl is None:
                    osz = 'szoveg_van_cimke_nincs_luv_vers_nincs'
                    ind = 'az eBible-ben van szoveg, cimke nincs; a luvlylavnder-ben a vers nincs (versszamozasi eltérés vagy a masik forras hiánya)'
                    allapot = 'javaslat'
                elif hl[0]:
                    osz = 'adathiany_ebible'
                    ind = 'az eBible-ben van szoveg, cimke nincs; a luvlylavnder ugyanazt a verset %d Strong-cimkevel tartalmazza: adathiány az eBible-ben (nem toltjuk ki, l. CLAUDE.md 3. szabaly)' % len(hl[0])
                    allapot = 'javaslat'
                else:
                    osz = 'szoveg_van_cimke_nincs_mindket_forrasban'
                    ind = 'szoveg van, Strong-cimke egyik forrasban sincs (pl. csak nem cimkezheto szavak): nem adathiány, nincs mit importalni'
                    allapot = 'javaslat'
                hianyok.append((VER, '%s.%d.%d' % (s, f, v), len(rec['szavak']), tl, 'igen' if hl is not None else 'nem', len(hl[0]) if hl else 0, osz, ind, allapot))
        for s, k, irany in koord_kul:
            ih = '%s.%d.%d' % (s, k[0], k[1])
            van = [i for i, h in enumerate(hianyok) if h[0] == VER and h[1] == ih]
            if van and irany == 'csak_ebible':
                h = list(hianyok[van[0]])
                h[6] = 'ures_vers_forras_versszamozasi_elteres'
                h[7] = 'a vers jelolo megvan az eBible-ben, de a szoveg csak labjegyzetben all (kritikai szovegkiadas: a vers nem resze a fo szovegnek), a luvlylavnder-ben a vers nincs: versszamozasi eltérés, nem adathiány; szabalyalapu'
                hianyok[van[0]] = tuple(h)
                continue
            hianyok.append((VER, ih, 0, 0, 'igen' if irany == 'csak_luv' else 'nem', 0,
                            'versszamozasi_elteres_' + irany, 'a vers csak az egyik forrasban letezik (koordinata-halmaz eltérés eBible vs luvlylavnder); szabalyalapu: versszamozasi eltérés', 'szabaly'))
        stat[VER] = dict(zip_sha=sha(zp), sor_db=sor_db, vers_db=vers_kan, vers0=vers0, vers_cimkes=vers_cimkes, hidak=hidak,
                         anom=len(anom), koord=len(koord_kul), egyezik=egyezik, osszes=osszes, regi_egy=regi_egy, regi_ossz=regi_ossz,
                         luv_vers=sum(len(luv[s]) for s, _ in konyvek))
        for x in anom[:20]:
            print('ANOMALIA', VER, x)
    # F19_hianyok.tsv
    with open(os.path.join(REPO, 'naplok', 'F19_hianyok.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# F19 hianyok: a Strong-cimke nelkuli (eBible) versek besorolasa. forras: https://ebible.org/Scriptures/eng-kjv_usfm.zip es eng-asv_usfm.zip (letoltve %s); keresztellenorzes: https://github.com/luvlylavnder/bible-app-data commit %s\n' % (ts, luv_commit))
        fh.write('# licenc: eBible KJV/ASV = Public Domain (copr.htm; a KJV-nel a brit korona-szabadalom csak az Egyesult Kiralysagbeli nyomtatasra vonatkozik); luvlylavnder = CC0 1.0 (gyoker LICENSE + README). Nincs licencutkozes; a scrollmapper kimarad (F19 4. lepes)\n')
        fh.write('# futtatasi parancs: python eszkozok/f19_ebible_import.py --munka <mappa>  (kjv.zip, asv.zip, luv/ klon)\n')
        for VER in ('KJV', 'ASV'):
            s = stat[VER]
            fh.write('# %s: zip sha256=%s; teljes tabla sorai=%d; kanonikus versek (v>0)=%d, ebbol cimkes=%d, cimke nelkuli=%d; zsoltarfelirat-versek (v=0)=%d; luvlylavnder versei=%d; koordinata-eltéres=%d; vershidak=%d; parse-anomalia=%d\n'
                     % (VER, s['zip_sha'], s['sor_db'], s['vers_db'], s['vers_cimkes'], s['vers_db'] - s['vers_cimkes'], s['vers0'], s['luv_vers'], s['koord'], s['hidak'], s['anom']))
            fh.write('# %s Strong-halmaz egyezes verseken: eBible=luvlylavnder %d/%d; eBible=meglevo studybible-tabla (Gen/Exo/Pro) %d/%d\n' % (VER, s['egyezik'], s['osszes'], s['regi_egy'], s['regi_ossz']))
        fh.write('\t'.join(['verzio', 'igehely', 'ebible_szo_db', 'ebible_szoveg_karakter', 'luv_van_vers', 'luv_strong_db', 'osztaly', 'indok', 'allapot']) + '\n')
        for h in hianyok:
            fh.write('\t'.join(str(x) for x in h) + '\n')
    for VER in stat:
        print(VER, stat[VER])
    print('hianyok sorai:', len(hianyok))


if __name__ == '__main__':
    main()
