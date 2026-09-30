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
import collections
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


def ir_teljes(fajl, adat, konyvek, fejsorok=()):
    sorok = list(fejsorok) + ['\t'.join(['Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó', 'Morfológiai kód'])]
    n = 0
    for step, _ in konyvek:
        for (f, v) in sorted(adat[step]):
            for i, (st, szo) in enumerate(adat[step][(f, v)]['szavak'], 1):
                sorok.append('\t'.join(['%s.%d.%d' % (step, f, v), str(i), st, szo, '']))
                n += 1
    with open(fajl, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(sorok) + '\n')
    return n


def olvas_mt(konyvek):
    """Macula Hebrew (WLC, MT-számozás): {(step, fejezet): set(versek)}. A 'ref' oszlop: 'GEN 1:1!1'."""
    import glob
    fel = {s.upper(): s for s, _ in konyvek}
    mt = {}
    for fp in glob.glob(os.path.join(REPO, 'konkordancia', 'Macula_heber_*.tsv')):
        for l in open(fp, encoding='utf-8').read().split('\n'):
            if not l or l.startswith('#') or l.startswith('xml_id'):
                continue
            m = re.match(r'^[^\t]+\t(\w+) ([0-9]+):([0-9]+)!', l)
            if m and m.group(1) in fel:
                mt.setdefault((fel[m.group(1)], int(m.group(2))), set()).add(int(m.group(3)))
    return mt


def eltolt_fejezet(step, fej, versek, mt):
    """Igaz, ha az OT-konyv fejezetenek MT-versszama (Macula/WLC) nem egyezik az angolet, vagy az MT-ben nincs ilyen fejezet.
    versek: az angol {(fej, vers): rec}. NT-konyvre (a Maculaban nincs) hamis."""
    if not any(k[0] == step for k in mt):
        return False
    en = set(v for (c, v) in versek if c == fej and v > 0)
    m = mt.get((step, fej))
    if m is None:
        return True
    return max(m) != max(en)


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
    mt = olvas_mt(konyvek)
    luv_commit = os.popen('git -C "%s" rev-parse HEAD' % os.path.join(M, 'luv')).read().strip()
    for ver, VER, luvdir, luvfile in (('kjv', 'KJV', 'KJV-Strongs', 'kjv_strongs.json'), ('asv', 'ASV', 'ASV-Strongs', 'asvs.json')):
        zp = os.path.join(M, ver + '.zip')
        adat, anom, hidak = olvas_zip(zp, ver, konyvek)
        luv = olvas_luv(os.path.join(M, 'luv'), luvdir, luvfile, konyvek)
        ki = os.path.join(REPO, 'konkordancia', VER + '_Strongs_teljes.tsv')
        sor_db = sum(len(rec['szavak']) for s_, _ in konyvek for rec in adat[s_].values())
        kulcs = collections.Counter(st for s_, _ in konyvek for rec in adat[s_].values() for st, _w in rec['szavak'])
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
                elif hl[0] and eltolt_fejezet(s, f, adat[s], mt):
                    osz = 'versszamozasi_eltolas'
                    ind = ('a vers a KJV/MT versszamozasi-eltéréssel érintett fejezetben van (a Macula/WLC-fejezet versszama != az angol; vagy az MT-ben nincs ilyen fejezet); '
                           'az eBible-forras cimkezese itt a nem-angol (MT) szamozashoz igazodhat, a luvlylavnder ugyanazt az angol verset %d cimkevel tartalmazza; '
                           'nem adathiany, szabalyalapu; a szomszed versek Strong-cimkei gyanusak' % len(hl[0]))
                    allapot = 'szabaly'
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
        # szomszed versek (+-1, azonos fejezet), amelyek cimkeseek, de eltolt vers mellett allnak: gyanus Strong-cimkek
        eltolt = set(h[1] for h in hianyok if h[0] == VER and h[6] == 'versszamozasi_eltolas')
        van_sor = set(h[1] for h in hianyok if h[0] == VER)
        for ih in sorted(eltolt):
            s, f, v = ih.split('.')
            for d in (-1, 1):
                kk = (int(f), int(v) + d)
                nb = '%s.%d.%d' % (s, kk[0], kk[1])
                rec = adat[s].get(kk)
                if rec is None or not rec['szavak'] or nb in van_sor or kk[1] < 1:
                    continue
                van_sor.add(nb)
                hl = luv[s].get(kk)
                hianyok.append((VER, nb, len(rec['szavak']), len(rec['szoveg']), 'igen' if hl is not None else 'nem', len(hl[0]) if hl else 0,
                                'szomszed_versszamozasi_eltolas_gyanu',
                                'cimkes vers, de eltolt vers (%s) szomszedja: az eBible-cimkek egy resze a szomszed vershez tartozhat (MT-szamozas); a Strong-halmaz megbizhatatlansaga: gyanus' % ih,
                                'jelolt'))
        # kulcs-Strongok es fejlec a teljes tablahoz (proveniencia: scope | forras | ts)
        kulcs_s = ' '.join('%s=%d' % (k, kulcs[k]) for k in ('H430', 'H776', 'H1', 'H3068', 'G746', 'G2316'))
        fej = ['# GENERÁLT: eszkozok/f19_ebible_import.py — kézzel nem szerkesztendő.',
               '# proveniencia: scope=%s teljes (66 kanonikus könyv, angol számozás) | forras=https://ebible.org/Scriptures/eng-%s_usfm.zip sha256=%s | ts=%s' % (VER, ver, sha(zp), ts),
               '# licenc: Public Domain (eBible copr.htm); l. naplok/F19_hianyok.tsv fejléce; kulcs-Strongok darabszáma: %s' % kulcs_s]
        if VER == 'ASV':
            fej += ['# ÁLLAPOT: javaslat — FORRÁSHIBÁS, tartalmi keresésre NEM használható. Az eBible ASV USFM \\w|strong= címkéi szisztematikusan hibásak',
                    '# (a nyers USFM-ben H430/H776/H1/G746 = 0 előfordulás, 1Móz 1:1 „God”→H8064, függvényszavak a szomszéd címkéjét viselik); a parszoló hűen adja vissza a forrást (l. eszkozok/f19_ellenorzes.py, DONTESEK DT19 (b)).',
                    '# Helyes ASV-Strong: a konkordancia/ASV_Strongs_{Genesis,Exodus,Proverbs}.tsv (studybible.info) vagy a luvlylavnder ASV-Strongs. Egyezés a meglévő táblákkal vershalmazonként: 1Móz 49/1532, 2Móz 52/1211, Péld 89/915.']
        else:
            fej += ['# ÁLLAPOT: importált, a meglévő KJV_Strongs_{Genesis,Exodus,Proverbs}.tsv-vel vershalmazonként 93,1% / 91,8% / 94,9% egyezik; a token-szintű egyezés a luvlylavnderrel 99,5%. A „Angol szó” néha frázis (pl. „man’s hand”); a Morfológiai kód üres.']
        ir_teljes(ki, adat, konyvek, fej)
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
        fh.write('# proveniencia: scope=66 kanonikus konyv, angol versszamozas (F19) | forras=eBible eng-kjv_usfm.zip, eng-asv_usfm.zip + luvlylavnder commit %s + Macula Hebrew (MT-szamozas, a versszamozasi-eltolas szabalyhoz) | ts=%s\n' % (luv_commit, ts))
        fh.write('# hatokor-kulonbseg az F06 merehez (naplok/F06_kjv_asv.tsv): az F06 a KJV-zipben 81 fajlt (apokrifokkal, 36822 vers), az ASV-zipben 68 fajlt merte (31102 vers); a Strong-cimkek szama (KJV 349308, ASV 705378) es a cimkes versek szama (31099, 30978) azonos, mert az apokrifok cimke nelkuliek; az F19 mindket forrasbol csak a 66 kanonikus konyvet importalja (31102 vers)\n')
        fh.write('# ASV: a hianyok besorolasa mellekes, mert az eBible-ASV cimkezese egeszeben hibas (l. konkordancia/ASV_Strongs_teljes.tsv fejlece, DT19 (b)); versszamozasi_eltolas = az MT-fejezetszam-eltéressel erintett fejezetek verse (Macula/WLC szerint), a szomszed_versszamozasi_eltolas_gyanu sorok az eltolt versek cimkes szomszedai (gyanus Strong-cimkek); a 6 megmarado adathiany_ebible sor NT-ben vagy egyezo versszamu fejezetben van (KJV 3, ASV 3: 2Sam 5:16, Rom 1:31, 2Kor 13:14)\n')
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
