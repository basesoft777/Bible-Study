#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nyilt_mag_kapu.py -- a nyílt mag (`nyilt_mag/`) saját kapuja (F162, FELADATOK #162).

Az olvasói kapu (`olvasoi_kapu.py`) BELSO/ANGOL szabályának megfelelője a nyílt exportra: a szabályokat onnan veszi
át (újrahasznosítja, nem másolja), és kiegészíti a nyílt csomag saját ellenőrzéseivel.

Ellenőrzések (azonosító — súlyosság):
    BELSO        belső jelölés a csomag szövegében (DT/N/F-szám, fájlnév, `gerinc`, `scope=`, `manual`,
                 `gerinc_elem`, snake_case belső azonosító, study/scan/gap; az olvasói kapu BELSO mintáival)  — BUKÁS
    ANGOL        angol maradék és munkazsargon a magyar szövegben (az `…_en` oszlopok és a kódkönyv angol
                 leírása kivétel)                                                                           — BUKÁS
    ANGOL_SOR    ≥3 angol funkciószó egy magyar cellában                                                    — FIGYELMEZTETÉS
    KODKONYV     oszlop vagy zárt értékkészlet-érték kódkönyv-leírás nélkül, vagy a leírás egyik nyelven
                 hiányzik / a két nyelv azonos                                                              — BUKÁS
    LICENC       kizárt (NC, GPL, tisztázatlan, zárt) forrás neve vagy értéke a csomagban; az SDBH/SDGNT-adat a
                 külön rétegen kívül                                                                        — BUKÁS
    RETEG        a CC BY-SA réteg attribúció/licenc-jelölés nélkül                                          — BUKÁS
    HIBAK        az „ismert hibák” szakasz hiányzik, vagy nem tartalmazza a Károli-KH mért számát           — BUKÁS
    HIVATKOZAS   döntés-azonosító (NYD) feloldás nélkül; ismeretlen motívum-azonosító                       — BUKÁS
    CSOPORT      összesítő kizárás-sor, amelynek a `kizaras_csoportok.tsv`-beli tagszáma nem egyezik a
                 `csoport_versszam`-mal (tag nélküli sor is), vagy csoport-tag nem létező összesítő sorhoz   — BUKÁS
    BAJTAZONOS   a lemezen lévő csomag nem egyezik az újragenerált kimenettel / az összeg-fájllal            — BUKÁS
    TERMEKRETEG  a lexikon szövegének mezője (kapcsolodas, kapcsolatok funkcio/indoklas, jelentes_hu) a csomagban; a funkció nem
                 rövid címke; a nem exportált mezőt a kódkönyv nem mondja ki                                 — BUKÁS
    KH_NEV       a „KJV” szó szövegben (versszámozási megjegyzés lehet, nem adat)                           — FIGYELMEZTETÉS
    OSIS         igehely-oszlop OSIS-pár nélkül; az OSIS-kulcs hiányzik, szabálytalan, ismeretlen könyvkódú, vagy
                 nem egyezik a magyar igehely leképezésével (F170, kapu (a))                                 — BUKÁS

Használat:
    python eszkozok/nyilt_mag_kapu.py [--csomag nyilt_mag] [--gyors]   (--gyors: újragenerálás nélkül)
Kilépési kód: 1, ha van BUKÁS; 0 egyébként.
"""
import argparse
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import olvasoi_kapu as K  # noqa: E402
import nyilt_mag_export as E  # noqa: E402

BUKAS, FIGY = K.BUKAS, K.FIGY

KOTELEZO = ['motivumok.tsv', 'elofordulasok.tsv', 'kizarasok.tsv', 'beepitesi_dontesek.tsv', 'kizaras_csoportok.tsv', 'kapcsolatok.tsv',
            'motivum_kapcsolatok.tsv', 'dontesnaplo.tsv', 'forrasok_es_licencek.tsv', 'kodkonyv.tsv', 'KODKONYV.md',
            'OLVASSEL.md', 'ISMERT_HIBAK.md', 'ELLENORZO_OSSZEG.sha256', 'KIADAS.txt',
            'README.md', 'KNOWN_ISSUES.md', 'RELEASE.txt',
            'cc_by_sa_reteg/szemantikai_domenek.tsv', 'cc_by_sa_reteg/OLVASSEL.md']

# a zárt értékkészletű oszlopok, amelyeknek minden értékét a kódkönyv leírja
ZART = {
    'motivumok.tsv': ['pardes_szint', 'statusz', 'feldolgozasi_allapot', 'azonossag_tipusa'],
    'elofordulasok.tsv': ['pardes_szint', 'horgony_tipus', 'szotar', 'azonositas_modja', 'megbizhatosag',
                          'igazolas', 'lekerdezes_tipusa', 'forras_licenc'],
    'kizarasok.tsv': ['jelolt_tipus', 'azonositas_modja', 'megbizhatosag', 'keresesi_mod'],
    'beepitesi_dontesek.tsv': ['jelolt_tipus', 'keresesi_mod'],
    'kapcsolatok.tsv': ['tipus', 'bizonyossag', 'pardes_szint'],
    'motivum_kapcsolatok.tsv': ['tipus', 'bizonyossag', 'pardes_szint', 'lekerdezes_tipusa'],
    'forrasok_es_licencek.tsv': ['licenc', 'szerepe_a_csomagban'],
    'cc_by_sa_reteg/szemantikai_domenek.tsv': ['szotar'],
}
# angol szöveget joggal hordozó oszlopok (az ANGOL-ellenőrzés kivétele)
ANGOL_OSZLOP = {'jelentes_en', 'glossza', 'lemma', 'leiras_en'}


def angol_oszlop(o):
    """Angol (vagy nyelvfüggetlen kódú) oszlop: a felsoroltak, az `…_en` és az `…_osis` oszlopok (F170)."""
    return o in ANGOL_OSZLOP or o.endswith('_en') or o.endswith('_osis')
# a forrásleltár dataset-neve és szerepe: a datasetek nyilvános nevei (snake_case, angol nevek is)
SNAKE_KIVETEL = {'dataset', 'szerepe_a_csomagban'}
# nyilvános fájlnevek (a csomag saját fájljai: a „belső fájl” mintából kivéve)
CSOMAG_NEVEK = re.compile(r'\b(?:motivumok|elofordulasok|kizarasok|kizaras_csoportok|beepitesi_dontesek|kapcsolatok|'
                          r'motivum_kapcsolatok|dontesnaplo|forrasok_es_licencek|kodkonyv|szemantikai_domenek)\.tsv'
                          r'|\b(?:KODKONYV|OLVASSEL|ISMERT_HIBAK|README|KNOWN_ISSUES)\.md|ELLENORZO_OSSZEG\.sha256')

EXTRA_BELSO = [
    (re.compile(r'gerinc_elem'), 'belső oszlopnév (gerinc_elem)'),
    (re.compile(r'\bscope=|\bforras=|\bts=\d'), 'proveniencia-kulcs'),
    (re.compile(r'(?:naplok|eszkozok|adat|konkordancia|archivum|tematikus_lezart|genezis|motivumlog)/'),
     'belső könyvtárút'),
    (re.compile(r'\bjeloltek\b|\bdontes_ref\b|\belofordulasok\.tsv\b.*\bmanual\b'), 'belső tábla'),
    (re.compile(r'\b[a-z]+_[a-z0-9_]+(?:=\S+)?\b'), 'belső azonosító (snake_case)'),
]
# a belső azonosító-mintát csak az adatsorokon (nem az oszlopfejlécen, nem a leíró md-n) alkalmazzuk
SNAKE = EXTRA_BELSO[-1][0]

# a kizárt dataset-nevek, amelyek nem állhatnak a csomagban (a forrásleltár-tábla és a leíró md kivétel)
KIZART_NEV_KIVETEL = ('forrasok_es_licencek.tsv', 'OLVASSEL.md', 'ISMERT_HIBAK.md', 'ELLENORZO_OSSZEG.sha256',
                      'KODKONYV.md', 'README.md', 'KNOWN_ISSUES.md')
# kétnyelvű vagy angol attribúciós fájlok: az ANGOL-ellenőrzés kivétele (a kódkönyv angol leírása szándékos)
ANGOL_FAJL_KIVETEL = ('KODKONYV.md', 'kodkonyv.tsv', 'README.md', 'KNOWN_ISSUES.md', 'cc_by_sa_reteg/OLVASSEL.md',
                      'cc_by_sa_reteg/szemantikai_domenek.tsv')


class Talalat:
    def __init__(self, azon, suly, fajl, sor, idezet, uzenet):
        self.azon, self.suly, self.fajl, self.sor, self.idezet, self.uzenet = azon, suly, fajl, sor, idezet, uzenet


def olvas_csomag(ut):
    ki = {}
    for gyoker, _, nevek in os.walk(ut):
        for n in nevek:
            rel = os.path.relpath(os.path.join(gyoker, n), ut).replace('\\', '/')
            with open(os.path.join(gyoker, n), encoding='utf-8') as f:
                ki[rel] = f.read()
    return ki


def tsv_sorok(szoveg):
    """(fejléc, [(sorszám, dict)]) -- a `#` sorok kihagyva."""
    sorok = [(i + 1, s) for i, s in enumerate(szoveg.split('\n')) if s.strip() and not s.startswith('#')]
    if not sorok:
        return [], []
    fej = sorok[0][1].split('\t')
    ki = []
    for n, s in sorok[1:]:
        m = s.split('\t')
        ki.append((n, dict(zip(fej, m + [''] * (len(fej) - len(m))))))
    return fej, ki


def kor(s, m, szel=45):
    return s[max(0, m.start() - szel):m.end() + szel].replace('\t', ' ')


def szoveg_cellak(fajlok):
    """(fájl, sor, oszlop, érték) a TSV-k adatcelláiból, a kódkönyv-TSV nélkül; md-fájloknál sor-szintű (oszlop '')."""
    for rel, sz in sorted(fajlok.items()):
        if rel.endswith('.tsv') and rel != 'kodkonyv.tsv':
            fej, sorok = tsv_sorok(sz)
            for n, d in sorok:
                for o in fej:
                    if d[o]:
                        yield rel, n, o, d[o]
        elif rel.endswith('.md'):
            for i, s in enumerate(sz.split('\n'), 1):
                if s.strip() and not s.startswith('#') or (s.startswith('# ') and i > 1):
                    yield rel, i, '', s


def ell_belso(fajlok):
    ki = []
    for rel, n, o, ertek in szoveg_cellak(fajlok):
        t = CSOMAG_NEVEK.sub('', ertek)
        t = t.replace('`', '')
        for rx, nev in K.BELSO + EXTRA_BELSO[:-1]:
            if rel == 'ELLENORZO_OSSZEG.sha256':
                continue
            m = rx.search(t)
            if m:
                ki.append(Talalat('BELSO', BUKAS, rel, n, kor(t, m), '%s [%s]: %s' % (nev, o or 'szöveg', m.group(0))))
        if rel.endswith('.tsv') and o and not (rel == 'forrasok_es_licencek.tsv' and o in SNAKE_KIVETEL):
            m = SNAKE.search(t)
            if m:
                ki.append(Talalat('BELSO', BUKAS, rel, n, kor(t, m), 'belső azonosító (snake_case) [%s]: %s' % (
                    o, m.group(0))))
    return ki


def ell_angol(fajlok):
    ki = []
    for rel, n, o, ertek in szoveg_cellak(fajlok):
        if angol_oszlop(o) or rel in ANGOL_FAJL_KIVETEL or (rel == 'forrasok_es_licencek.tsv' and o == 'dataset'):
            continue
        t = CSOMAG_NEVEK.sub('', ertek)
        m = K.ANGOL_SZO.search(t)
        if m:
            ki.append(Talalat('ANGOL', BUKAS, rel, n, kor(t, m), 'angol maradék / zsargon: ' + m.group(0)))
        elif K.ANGOL_FUNKCIO.findall(t) and len(K.ANGOL_FUNKCIO.findall(t)) >= K.ANGOL_SOR_MIN and o != 'kerdes':
            ki.append(Talalat('ANGOL_SOR', FIGY, rel, n, t[:140], '%d angol funkciószó' % len(K.ANGOL_FUNKCIO.findall(t))))
    return ki


def ell_kodkonyv(fajlok):
    ki = []
    fej, kk = tsv_sorok(fajlok['kodkonyv.tsv'])
    kulcs = {}
    for n, d in kk:
        kulcs[(d['tabla'], d['oszlop'], d['ertek'])] = (n, d)
        hu, en = d['leiras_hu'].strip(), d['leiras_en'].strip()
        if not hu or not en:
            ki.append(Talalat('KODKONYV', BUKAS, 'kodkonyv.tsv', n, '%s / %s / %s' % (d['tabla'], d['oszlop'], d['ertek']),
                              'a leírás egyik nyelven hiányzik'))
        elif hu == en:
            ki.append(Talalat('KODKONYV', BUKAS, 'kodkonyv.tsv', n, hu[:80], 'a magyar és az angol leírás azonos'))
    for rel, sz in sorted(fajlok.items()):
        if not rel.endswith('.tsv') or rel == 'kodkonyv.tsv':
            continue
        fej, sorok = tsv_sorok(sz)
        for o in fej:
            if (rel, o, '') not in kulcs:
                ki.append(Talalat('KODKONYV', BUKAS, rel, 2, o, 'az oszlopnak nincs kódkönyv-leírása'))
        for o in ZART.get(rel, []):
            for ert in sorted({d[o] for _, d in sorok if d.get(o)}):
                for resz in [x.strip() for x in ert.split(';')]:
                    if resz and (rel, o, resz) not in kulcs:
                        ki.append(Talalat('KODKONYV', BUKAS, rel, 2, '%s = %s' % (o, resz),
                                          'a zárt értékkészlet értékének nincs kódkönyv-leírása'))
    return ki


def ell_licenc(fajlok):
    ki = []
    lic = E.Licenc()
    kizart = {ds for ds in lic.sor if lic.allapot(ds)[0] == 'kizart'}
    sa = {ds for ds in lic.sor if lic.allapot(ds)[0] == 'sa_reteg'}
    for rel, n, o, ertek in szoveg_cellak(fajlok):
        if rel in KIZART_NEV_KIVETEL or rel.startswith('cc_by_sa_reteg/'):
            continue
        for ds in sorted(kizart | {'KJV_Strongs', 'ETCBC', 'MCGED', 'Mounce'}):
            m = re.search(r'(?<![\w])' + re.escape(ds) + r'(?![\w])', ertek)
            if m:
                ki.append(Talalat('LICENC', BUKAS, rel, n, kor(ertek, m), 'kizárt licencű forrás a csomagban: ' + ds))
        for ds in sorted(sa):
            m = re.search(r'(?<![\w])' + re.escape(ds) + r'(?![\w])', ertek)
            if m:
                ki.append(Talalat('LICENC', BUKAS, rel, n, kor(ertek, m), 'SDBH/SDGNT-adat a külön rétegen kívül: ' + ds))
        if o == 'forras_dataset':
            for ds in [x.strip() for x in ertek.split(';') if x.strip()]:
                if lic.allapot(ds)[0] in ('kizart', 'sa_reteg'):
                    ki.append(Talalat('LICENC', BUKAS, rel, n, ertek, 'nem engedett licencű forrás-dataset: ' + ds))
        if o == 'forras_licenc' and re.search(r'tisztázatlan|minden jog|Mounce|GPL', ertek):
            ki.append(Talalat('LICENC', BUKAS, rel, n, ertek, 'nem engedett licenc-címke'))
    # a leltár-tábla: a kizárt datasetnek nincs „forrás” szerepe
    fej, sorok = tsv_sorok(fajlok['forrasok_es_licencek.tsv'])
    for n, d in sorok:
        st, _ = lic.allapot(d['dataset'])
        if st == 'kizart' and d['szerepe_a_csomagban'] != 'kizárva':
            ki.append(Talalat('LICENC', BUKAS, 'forrasok_es_licencek.tsv', n, d['dataset'], 'kizárt forrás nincs kizárva'))
    olv = fajlok['OLVASSEL.md']
    for ds in sorted(kizart):
        if ds not in olv:
            ki.append(Talalat('LICENC', BUKAS, 'OLVASSEL.md', 1, ds, 'a kizárt dataset listája nem mondja ki'))
    return ki


def ell_reteg(fajlok):
    ki = []
    o = fajlok.get('cc_by_sa_reteg/OLVASSEL.md', '')
    for kell in ('CC BY-SA 4.0', 'United Bible Societies', 'ShareAlike'):
        if kell not in o:
            ki.append(Talalat('RETEG', BUKAS, 'cc_by_sa_reteg/OLVASSEL.md', 1, kell, 'hiányzik az attribúció / licenc-jelölés'))
    t = fajlok.get('cc_by_sa_reteg/szemantikai_domenek.tsv', '')
    if 'CC BY-SA 4.0' not in t.split('\n')[0]:
        ki.append(Talalat('RETEG', BUKAS, 'cc_by_sa_reteg/szemantikai_domenek.tsv', 1, t.split('\n')[0][:80],
                          'a fejléc nem jelöli a CC BY-SA 4.0-t'))
    return ki


def ell_hibak(fajlok):
    ki = []
    h = fajlok.get('ISMERT_HIBAK.md', '')
    if 'Károli' not in h:
        ki.append(Talalat('HIBAK', BUKAS, 'ISMERT_HIBAK.md', 1, '', 'a Károli-KH hiba hiányzik'))
    kh = E.kh_meres()
    for k in ('gyanus', 'forrasvers', 'kh_sor'):
        if kh[k] is None:
            ki.append(Talalat('HIBAK', BUKAS, E.KH_JELENTES, 1, k, 'a mért szám nem olvasható a jelentésből'))
        elif str(kh[k]) not in h:
            ki.append(Talalat('HIBAK', BUKAS, 'ISMERT_HIBAK.md', 1, str(kh[k]), 'a mért szám nem szerepel (%s)' % k))
    if 'ISMERT_HIBAK.md' not in fajlok.get('OLVASSEL.md', ''):
        ki.append(Talalat('HIBAK', BUKAS, 'OLVASSEL.md', 1, '', 'a csomag leírása nem hivatkozik az „ismert hibák” szakaszra'))
    return ki


def ell_hivatkozas(fajlok):
    ki = []
    _, dn = tsv_sorok(fajlok['dontesnaplo.tsv'])
    nyd = {d['dontes_azonosito'] for _, d in dn}
    _, mot = tsv_sorok(fajlok['motivumok.tsv'])
    mids = {d['motivum_azonosito'] for _, d in mot}
    for rel in ('elofordulasok.tsv', 'kizarasok.tsv', 'beepitesi_dontesek.tsv', 'kizaras_csoportok.tsv', 'kapcsolatok.tsv',
                'motivum_kapcsolatok.tsv'):
        fej, sorok = tsv_sorok(fajlok[rel])
        for n, d in sorok:
            for o in ('motivum_azonosito', 'cel_motivum', 'motivum_a', 'motivum_b'):
                if d.get(o) and d[o] not in mids:
                    ki.append(Talalat('HIVATKOZAS', BUKAS, rel, n, '%s = %s' % (o, d[o]), 'ismeretlen motívum-azonosító'))
            for ert in re.findall(r'NYD-\d+', ' '.join(d.values())):
                if ert not in nyd:
                    ki.append(Talalat('HIVATKOZAS', BUKAS, rel, n, ert, 'a döntés-azonosító nincs a döntésnaplóban'))
    return ki


def ell_csoport(fajlok):
    """Minden összesítő kizárás-sor (`csoport_versszam` nem üres) tagjainak száma a `kizaras_csoportok.tsv`-ben
    egyezik a versszámmal; minden csoport-tag létező összesítő sorhoz tartozik, és egy csoporton belül nem ismétlődik."""
    ki = []
    _, kiz = tsv_sorok(fajlok['kizarasok.tsv'])
    _, tagok = tsv_sorok(fajlok['kizaras_csoportok.tsv'])
    osszesito = {(d['motivum_azonosito'], d['igehely']): (n, d['csoport_versszam']) for n, d in kiz
                 if d.get('csoport_versszam')}
    db, latott = {}, set()
    for n, d in tagok:
        k = (d['motivum_azonosito'], d['csoport_sor_igehely'])
        if k not in osszesito:
            ki.append(Talalat('CSOPORT', BUKAS, 'kizaras_csoportok.tsv', n, '%s %s' % k,
                              'a csoport-tag nem létező összesítő sorhoz tartozik'))
        if k + (d['igehely'],) in latott:
            ki.append(Talalat('CSOPORT', BUKAS, 'kizaras_csoportok.tsv', n, '%s %s / %s' % (k + (d['igehely'],)),
                              'ismétlődő csoport-tag'))
        latott.add(k + (d['igehely'],))
        db[k] = db.get(k, 0) + 1
    for k, (n, versszam) in sorted(osszesito.items()):
        if not versszam.isdigit() or int(versszam) != db.get(k, 0):
            ki.append(Talalat('CSOPORT', BUKAS, 'kizarasok.tsv', n, '%s %s' % k,
                              'a csoport versszáma %s, a felsorolt tagoké %d' % (versszam, db.get(k, 0))))
    return ki


def ell_osis(fajlok):
    """OSIS (F170, kapu (a)): minden igehely-oszlop mellett ott a `<oszlop>_osis` pár; minden kitöltött igehelynek
    van érvényes OSIS-kulcsa (szabályos alak, OSIS-könyvkód), és a kulcs a magyar igehely leképezése."""
    ki = []
    for rel, sz in sorted(fajlok.items()):
        if not rel.endswith('.tsv'):
            continue
        fej, sorok = tsv_sorok(sz)
        for o in fej:
            if o not in E.IGEHELY_OSZLOPOK:
                continue
            if o + '_osis' not in fej:
                ki.append(Talalat('OSIS', BUKAS, rel, 2, o, 'az igehely-oszlopnak nincs OSIS-párja'))
                continue
            for n, d in sorok:
                hu, k = d[o], d[o + '_osis']
                if not hu:
                    if k:
                        ki.append(Talalat('OSIS', BUKAS, rel, n, k, 'OSIS-kulcs üres igehely mellett'))
                    continue
                if not k:
                    ki.append(Talalat('OSIS', BUKAS, rel, n, hu, 'hiányzó OSIS-kulcs'))
                    continue
                for resz in k.split(' '):
                    if not E.OSIS_RX.match(resz):
                        ki.append(Talalat('OSIS', BUKAS, rel, n, resz, 'szabálytalan OSIS-kulcs'))
                    elif any(x.split('.')[0] not in E.OSIS_KONYVEK for x in resz.split('-')):
                        ki.append(Talalat('OSIS', BUKAS, rel, n, resz, 'ismeretlen OSIS-könyvkód'))
                try:
                    vart = E.osis(hu)
                except SystemExit as h:
                    ki.append(Talalat('OSIS', BUKAS, rel, n, hu, str(h)))
                    continue
                if vart != k:
                    ki.append(Talalat('OSIS', BUKAS, rel, n, '%s / %s' % (hu, k),
                                      'az OSIS-kulcs nem a magyar igehely leképezése (%s)' % vart))
    return ki


def ell_kh_nev(fajlok):
    ki = []
    for rel, n, o, ertek in szoveg_cellak(fajlok):
        if rel in KIZART_NEV_KIVETEL or rel.startswith('cc_by_sa_reteg/'):
            continue
        m = re.search(r'\bKJV\b', ertek)
        if m:
            ki.append(Talalat('KH_NEV', FIGY, rel, n, kor(ertek, m), 'a KJV szó szerepel (versszámozási megjegyzés lehet; nem adat)'))
    return ki


# a lexikon szövegének mezői (DT-F162c): értelmező próza és szótár-fordítás; nem lehetnek a csomagban
KI_MEZOK = {
    'elofordulasok.tsv': {'kapcsolodas', 'jelentes_hu', 'felmerult_tanulmany', 'forras_tanulmany', 'fo_elofordulas'},
    'kapcsolatok.tsv': {'funkcio', 'indoklas'},
    'motivum_kapcsolatok.tsv': {'funkcio', 'indoklas'},
}
FUNKCIO_MAX = 60


def ell_termekreteg(fajlok):
    """TERMEKRETEG: a KI-mezők nincsenek a csomagban; a `funkcio` csak rövid címke (nincs „ — ”, emoji, mondatvég);
    a kódkönyv mezőnként kimondja a nem exportált mezőket (réteg és ok)."""
    ki = []
    for rel, mezok in KI_MEZOK.items():
        fej, sorok = tsv_sorok(fajlok.get(rel, ''))
        for o in sorted(mezok & set(fej)):
            ki.append(Talalat('TERMEKRETEG', BUKAS, rel, 2, o, 'a lexikon szövegének mezője a csomagban'))
    fej, sorok = tsv_sorok(fajlok.get('elofordulasok.tsv', ''))
    for n, d in sorok:
        f = d.get('funkcio', '')
        if ' — ' in f or len(f) > FUNKCIO_MAX or re.search(r'[.!?]\s*$|\. ', f) or re.match(r'^[^\w(]', f):
            ki.append(Talalat('TERMEKRETEG', BUKAS, 'elofordulasok.tsv', n, f[:100],
                              'a funkció nem rövid címke (magyarázó rész vagy emoji maradt)'))
    _, kk = tsv_sorok(fajlok.get('kodkonyv.tsv', ''))
    nem = {d['oszlop'] for _, d in kk if d['tabla'] == '(nem exportált mezők)'}
    for rel, mezok in KI_MEZOK.items():
        for o in sorted(mezok - {'felmerult_tanulmany', 'forras_tanulmany', 'fo_elofordulas'}):
            if not any(x.startswith(rel + ' / ' + o) for x in nem):
                ki.append(Talalat('TERMEKRETEG', BUKAS, 'kodkonyv.tsv', 1, rel + ' / ' + o,
                                  'a nem exportált mezőt a kódkönyv nem mondja ki'))
    return ki


def ell_kanonikus(fajlok):
    """KANONIKUS: nincs GitHub-hivatkozás kanonikus forrásként; van helyőrző, kiadás-azonosító és a réteghatár."""
    ki = []
    for rel, sz in sorted(fajlok.items()):
        for i, sor in enumerate(sz.split('\n'), 1):
            m = re.search(r'github\.com|githubusercontent|\bgit@|/commit/[0-9a-f]{7,}|/pull/\d+', sor, re.I)
            if m:
                ki.append(Talalat('KANONIKUS', BUKAS, rel, i, kor(sor, m), 'GitHub-hivatkozás a csomagban'))
    o = fajlok.get('OLVASSEL.md', '')
    for kell in ('<KANONIKUS_FORRAS_URL>', '## Mi van benne, mi nincs', 'KIADAS.txt'):
        if kell not in o:
            ki.append(Talalat('KANONIKUS', BUKAS, 'OLVASSEL.md', 1, kell, 'hiányzik'))
    k = fajlok.get('KIADAS.txt', '')
    h = hashlib.sha256(fajlok.get('ELLENORZO_OSSZEG.sha256', '').encode('utf-8')).hexdigest()
    if 'kiadas_azonosito:' not in k or h not in k or '<KANONIKUS_FORRAS_URL>' not in k:
        ki.append(Talalat('KANONIKUS', BUKAS, 'KIADAS.txt', 1, k[:80], 'a kiadás-azonosító vagy a tartalmi hash hibás'))
    if E.ADATMAG_LEXIKON_HU not in fajlok.get('KODKONYV.md', '') or E.ADATMAG_LEXIKON_EN not in fajlok.get('KODKONYV.md', ''):
        ki.append(Talalat('KANONIKUS', BUKAS, 'KODKONYV.md', 1, '', 'a kódkönyv nem mondja ki a nyílt adatmag és a lexikon határát'))
    return ki


def ell_ketnyelv(fajlok):
    """KETNYELV: az olvasói fájlok mindkét nyelven megvannak (OLVASSEL/README, ISMERT_HIBAK/KNOWN_ISSUES,
    KIADAS/RELEASE), és az angol ugyanazt a tartalmat hordozza: ugyanazok a fájlsor-számok, mért számok, kizárt
    források, helyőrző és kiadás-azonosító; a GitHub-tilalom (ell_kanonikus) minden fájlra, így az angolra is áll."""
    ki = []
    hu, en = fajlok.get('OLVASSEL.md', ''), fajlok.get('README.md', '')
    for rel, sz in sorted(fajlok.items()):
        if rel.endswith('.tsv') and rel != 'kodkonyv.tsv' and not rel.startswith('cc_by_sa_reteg/'):
            sor = '| `%s` | %d |' % (rel, len([x for x in sz.split(chr(10)) if x.strip() and not x.startswith('#')]) - 1)
            for nev, t in (('OLVASSEL.md', hu), ('README.md', en)):
                if sor not in t:
                    ki.append(Talalat('KETNYELV', BUKAS, nev, 1, sor, 'a fájl sorszáma nem egyezik / hiányzik'))
    kizart = sorted(ds for ds in E.Licenc().sor if E.Licenc().allapot(ds)[0] == 'kizart')
    for ds in kizart:
        if ds not in en:
            ki.append(Talalat('KETNYELV', BUKAS, 'README.md', 1, ds, 'a kizárt dataset listája nem mondja ki'))
    for kell in ('<KANONIKUS_FORRAS_URL>', '## What is in it and what is not', 'RELEASE.txt', 'KNOWN_ISSUES.md',
                 'OLVASSEL.md'):
        if kell not in en:
            ki.append(Talalat('KETNYELV', BUKAS, 'README.md', 1, kell, 'hiányzik'))
    if 'README.md' not in hu or 'KNOWN_ISSUES.md' not in hu:
        ki.append(Talalat('KETNYELV', BUKAS, 'OLVASSEL.md', 1, '', 'a magyar leírás nem hivatkozik az angol változatra'))
    h = fajlok.get('KNOWN_ISSUES.md', '')
    kh = E.kh_meres()
    for k in ('gyanus', 'forrasvers', 'kh_sor', 'azonos', 'gyanus_sor'):
        if kh[k] is not None and str(kh[k]) not in h:
            ki.append(Talalat('KETNYELV', BUKAS, 'KNOWN_ISSUES.md', 1, str(kh[k]), 'a mért szám nem szerepel (%s)' % k))
    if 'Károli' not in h:
        ki.append(Talalat('KETNYELV', BUKAS, 'KNOWN_ISSUES.md', 1, '', 'a Károli-KH hiba hiányzik'))
    r, k_ = fajlok.get('RELEASE.txt', ''), fajlok.get('KIADAS.txt', '')
    hash_ = hashlib.sha256(fajlok.get('ELLENORZO_OSSZEG.sha256', '').encode('utf-8')).hexdigest()
    if 'release_id:' not in r or hash_ not in r or '<KANONIKUS_FORRAS_URL>' not in r:
        ki.append(Talalat('KETNYELV', BUKAS, 'RELEASE.txt', 1, r[:80], 'a kiadás-azonosító vagy a tartalmi hash hibás'))
    elif r.split(chr(10))[0].split(': ')[1] != k_.split(chr(10))[0].split(': ')[1]:
        ki.append(Talalat('KETNYELV', BUKAS, 'RELEASE.txt', 1, r[:80], 'a kiadás-azonosító nem egyezik a KIADAS.txt-vel'))
    return ki


def ell_olvasas(fajlok):
    """OLVASAS (F167.3): az OLVASSEL.md „Hogyan olvasd” és a README.md „How to read” szakasza megvan, a három
    példával, és a példák a csomag mai adatát mondják (az export ugyanazzal a függvénnyel számol, mint itt)."""
    ki = []
    try:
        p = E.olvasasi_peldak(fajlok)
    except SystemExit as h:
        return [Talalat('OLVASAS', BUKAS, 'OLVASSEL.md', 1, '', str(h))]
    hu = E.hogyan_olvasd_hu(p)
    en = E.hogyan_olvasd_en(p)
    for nev, cim, elvart in (('OLVASSEL.md', '## Hogyan olvasd', hu), ('README.md', '## How to read', en)):
        t = fajlok.get(nev, '')
        if cim not in t:
            ki.append(Talalat('OLVASAS', BUKAS, nev, 1, cim, 'a szakasz hiányzik'))
            continue
        if sum(1 for n in ('### 1.', '### 2.', '### 3.') if n in t) != 3:
            ki.append(Talalat('OLVASAS', BUKAS, nev, 1, cim, 'nincs meg mindhárom példa'))
        if '\n'.join(elvart) not in t:
            ki.append(Talalat('OLVASAS', BUKAS, nev, 1, cim, 'a példák nem a csomag mai adatát mondják'))
    return ki


def ell_osszeg(fajlok):
    ki = []
    sorok = [s for s in fajlok.get('ELLENORZO_OSSZEG.sha256', '').split('\n') if s.strip()]
    elvart = {}
    for s in sorok:
        h, _, rel = s.partition('  ')
        elvart[rel] = h
    for rel, sz in fajlok.items():
        if rel in ('ELLENORZO_OSSZEG.sha256', 'KIADAS.txt', 'RELEASE.txt'):
            continue
        h = hashlib.sha256(sz.encode('utf-8')).hexdigest()
        if elvart.get(rel) != h:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'az ellenőrző összeg nem egyezik'))
    for rel in elvart:
        if rel not in fajlok:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'az összeg-fájlban szereplő fájl hiányzik'))
    return ki


def ell_ujragenerals(fajlok, kimenet):
    ki = []
    uj, _ = E.export(kimenet)
    for rel in sorted(set(uj) | set(fajlok)):
        if rel not in fajlok:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'az újragenerált csomagban van, a lemezen nincs'))
        elif rel not in uj:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'a lemezen van, az újragenerált csomagban nincs'))
        elif uj[rel] != fajlok[rel]:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'a lemezen lévő fájl nem egyezik az újragenerálttal'))
    return ki


def mer(fajlok, kimenet=None, ujra=True):
    ki = []
    for rel in KOTELEZO:
        if rel not in fajlok:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'a csomag kötelező fájlja hiányzik'))
    if ki:
        return ki
    for f in (ell_belso, ell_angol, ell_kodkonyv, ell_licenc, ell_reteg, ell_hibak, ell_hivatkozas, ell_csoport, ell_kh_nev,
              ell_osis, ell_osszeg, ell_kanonikus, ell_termekreteg, ell_ketnyelv, ell_olvasas):
        ki += f(fajlok)
    if ujra:
        ki += ell_ujragenerals(fajlok, kimenet or 'nyilt_mag')
    return ki


def jelent(talalatok, max_sor=60):
    bukas = [t for t in talalatok if t.suly == BUKAS]
    figy = [t for t in talalatok if t.suly == FIGY]
    for t in (bukas + figy)[:max_sor]:
        print('%s  %s:%s  %s — „%s”' % (t.suly, t.fajl, t.sor, t.uzenet, t.idezet))
    if len(bukas) + len(figy) > max_sor:
        print('… további %d tétel' % (len(bukas) + len(figy) - max_sor))
    print('nyílt mag kapu: %d BUKÁS, %d FIGYELMEZTETÉS' % (len(bukas), len(figy)))
    return len(bukas)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--csomag', default='nyilt_mag')
    ap.add_argument('--gyors', action='store_true', help='az újragenerálás (bájtazonosság) nélkül')
    a = ap.parse_args()
    ut = a.csomag if os.path.isabs(a.csomag) else os.path.join(GYOKER, a.csomag)
    if not os.path.isdir(ut):
        print('BUKÁS: nincs csomag: %s' % ut)
        return 1
    fajlok = olvas_csomag(ut)
    return 1 if jelent(mer(fajlok, a.csomag, ujra=not a.gyors)) else 0


if __name__ == '__main__':
    sys.exit(main())
