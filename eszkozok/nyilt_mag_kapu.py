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
    FORDITAS     szabad szöveges oszlop `_en` pár vagy `forditas_modja` nélkül; angol cella gépi-fordítás jelölés
                 nélkül; a tárolt fordítás forrás-hash-e nem a mai magyar cellaé (elavult); az angol cella nem a
                 tárolt fordítás (F170, kapu (c)–(e))                                                       — BUKÁS
                 kimondott hiány (`nincs fordítás` / `részben hiányzik`)                                    — FIGYELMEZTETÉS
    GLOSSZA      a `strong_glossza_en` nem a STEPBible TBESH/TBESG-glossza (más, pl. KJV-Strong eredetű érték;
                 F170, kapu (f))                                                                            — BUKÁS
    CIMKE        zárt oszlop `_en` pár nélkül; zárt érték angol címke (`cimke_en`) nélkül; az `_en` cella nem a
                 kódkönyv címkéje (F170, kapu (b))                                                          — BUKÁS
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
    SZERKESZTO   „felhasználó” / „orkesztrátor” / „the user's decision” a csomagban (F178.6)              — BUKÁS
    LYUK         üres hivatkozáshely a szövegmezőben: „: ;”, árva rag („a -ből”, „8:21 -je”), árva névelő („a ;”),
                 nyitva maradt zárójel (F182, F28)                                                           — BUKÁS
    OSIS         igehely-oszlop OSIS-pár nélkül; az OSIS-kulcs hiányzik, szabálytalan, ismeretlen könyvkódú, vagy
                 nem egyezik a magyar igehely leképezésével (F170, kapu (a))                                 — BUKÁS
    VISSZHANG    a hatástörténet-táblákban Chain Lineage-tanú / BDB-sor / nem jóváhagyott forrás, összefoglaló-szöveg,
                 forrás-megnevezés vagy licenc nélküli sor (F198)                                            — BUKÁS
    HELYORZO     nyers `[A LEXIKON CÍME]`, `[HELYŐRZŐ…]` vagy `<…_URL>` a csomagban; a cím, a szerző/ORCID vagy a
                 közzétételi hely hiányzik                                                                   — BUKÁS
    ARANY        forrásonként a nyílt mag tételeinek aránya a forrás tételszámához (F176.4): 1% felett
                 FIGYELMEZTETÉS (átnézés a következő kiadás előtt), 5% felett BUKÁS (a további átvétel a felhasználó
                 döntésével vagy ügyvédi vélemény után); a küszöbök óvatos mérnöki értékek, jogi alapjuk nincs
                 (a #86 terv 6. szakasz 13. pontja). A forrás tételszáma a `konkordancia/VISSZHANG_README.md`
                 táblájából / az `adat/datasetek.tsv` `fajl` oszlopából jön, nem kódba írva.
                 A soronkénti arány `ARANY  <forrás>: <tétel> / <tételszám> = <arány>%` alakban kerül kiírásra.

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
            'visszhang_megfelelok.tsv', 'visszhang_tanuk.tsv', 'vitatott_forrasok.tsv', 'sblgnt_apparatus.tsv',
            'OLVASSEL.md', 'ISMERT_HIBAK.md', 'ELLENORZO_OSSZEG.sha256', 'KIADAS.txt',
            'README.md', 'KNOWN_ISSUES.md', 'RELEASE.txt',
            'cc_by_sa_reteg/szemantikai_domenek.tsv', 'cc_by_sa_reteg/OLVASSEL.md']

# a zárt értékkészletű oszlopok (egy helyen: az exportban; F170.2), amelyeknek minden értékét a kódkönyv leírja,
# és amelyek mellett az export `<oszlop>_en` címke-oszlopot ad
ZART = E.ZART
# angol szöveget joggal hordozó oszlopok (az ANGOL-ellenőrzés kivétele)
ANGOL_OSZLOP = {'jelentes_en', 'glossza', 'lemma', 'leiras_en'}


def angol_oszlop(o):
    """Angol (vagy nyelvfüggetlen kódú) oszlop: a felsoroltak, az `…_en` és az `…_osis` oszlopok (F170)."""
    return o in ANGOL_OSZLOP or o.endswith('_en') or o.endswith('_osis')
# a forrásleltár dataset-neve és szerepe: a datasetek nyilvános nevei (snake_case, angol nevek is)
SNAKE_KIVETEL = {'dataset', 'szerepe_a_csomagban', 'szerepe_a_csomagban_en'}
# a hivatkozás-oszlopok (URL, DOI) a forrás saját alakjában állnak: a snake_case-minta nem vonatkozik rájuk (F198)
URL_OSZLOP = {'forras_url', 'url', 'doi'}
# nyilvános fájlnevek (a csomag saját fájljai: a „belső fájl” mintából kivéve)
CSOMAG_NEVEK = re.compile(r'\b(?:motivumok|elofordulasok|kizarasok|kizaras_csoportok|beepitesi_dontesek|kapcsolatok|'
                          r'motivum_kapcsolatok|dontesnaplo|forrasok_es_licencek|kodkonyv|szemantikai_domenek|'
                          r'visszhang_megfelelok|visszhang_tanuk|vitatott_forrasok|sblgnt_apparatus)\.tsv'
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
            if angol_oszlop(o) and nev.startswith('proveniencia-érték (manual)'):
                continue    # az angol szövegben a „manual” közszó (pl. „manual reading”), nem a belső jel (F170)
            m = rx.search(t)
            if m:
                ki.append(Talalat('BELSO', BUKAS, rel, n, kor(t, m), '%s [%s]: %s' % (nev, o or 'szöveg', m.group(0))))
        if rel.endswith('.tsv') and o and o not in URL_OSZLOP and not (rel == 'forrasok_es_licencek.tsv' and o in SNAKE_KIVETEL):
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


def ell_cimke(fajlok):
    """CIMKE (F170.2, kapu (b)): minden zárt oszlop mellett ott a `<oszlop>_en` pár; minden zárt érték(rész)nek van
    `cimke_en`-je a kódkönyvben; az `_en` cella pontosan a részek címkéje, `; `-vel fűzve."""
    ki = []
    _, kk = tsv_sorok(fajlok['kodkonyv.tsv'])
    cimke = {(d['tabla'], d['oszlop'], d['ertek']): d.get('cimke_en', '').strip() for _, d in kk if d['ertek']}
    for (t, o, e), c in sorted(cimke.items()):
        if not c:
            ki.append(Talalat('CIMKE', BUKAS, 'kodkonyv.tsv', 1, '%s / %s / %s' % (t, o, e), 'a zárt értéknek nincs angol címkéje'))
    for rel, oszlopok in sorted(ZART.items()):
        fej, sorok = tsv_sorok(fajlok.get(rel, ''))
        for o in oszlopok:
            if o not in fej:
                continue
            if o + '_en' not in fej:
                ki.append(Talalat('CIMKE', BUKAS, rel, 2, o, 'a zárt oszlopnak nincs angol címke-párja'))
                continue
            for n, d in sorok:
                reszek = E.ertek_reszek(d[o])
                vart = '; '.join(cimke.get((rel, o, r), '') for r in reszek)
                if any(not cimke.get((rel, o, r)) for r in reszek):
                    ki.append(Talalat('CIMKE', BUKAS, rel, n, '%s = %s' % (o, d[o]), 'a zárt értéknek nincs angol címkéje'))
                elif d[o + '_en'] != vart:
                    ki.append(Talalat('CIMKE', BUKAS, rel, n, '%s / %s' % (d[o], d[o + '_en']),
                                      'az angol címke nem a kódkönyvé (%s)' % vart))
    return ki


def ell_forditas(fajlok):
    """FORDITAS (F170, kapu (c)–(e))."""
    ki = []
    E._ANGOL = None
    tar = E.angol_tar()
    for tabla, mezok in sorted(E.SZABAD.items()):
        fej, sorok = tsv_sorok(fajlok.get(tabla, ''))
        hianyzo_par = [o for o in mezok if o in fej and o + '_en' not in fej]
        for o in hianyzo_par:
            ki.append(Talalat('FORDITAS', BUKAS, tabla, 2, o, 'a szabad szöveges oszlopnak nincs angol párja'))
        if 'forditas_modja' not in fej:
            ki.append(Talalat('FORDITAS', BUKAS, tabla, 2, tabla, 'nincs forditas_modja oszlop'))
            continue
        for n, d in sorok:
            k = E.sorkulcs(tabla, d)
            fm = d['forditas_modja']
            for o in mezok:
                if o not in fej or o in hianyzo_par:
                    continue
                hu, en = d[o], d[o + '_en']
                t = tar.get((tabla, o, k))
                if not hu:
                    if en:
                        ki.append(Talalat('FORDITAS', BUKAS, tabla, n, en[:60], 'angol cella üres magyar mező mellett'))
                    continue
                # F178.6: a tárolt fordítás a szerkesztői csere előtti magyar szövegre készült; friss, ha a forrása a
                # csere után a mai cella
                if t and t['forras_hash'] != E.szoveg_hash(hu) and not (
                        t['forras_hash'] == E.szoveg_hash(t.get('forras_hu', ''))
                        and E.szerkesztoi_egyezik(t.get('forras_hu', ''), hu)):
                    ki.append(Talalat('FORDITAS', BUKAS, tabla, n, '%s / %s' % (o, k),
                                      'a fordítás elavult: a magyar forrás változott (újrafordítandó)'))
                    continue
                if not en:
                    if E.FORDITAS_NINCS not in fm and 'részben hiányzik' not in fm:
                        ki.append(Talalat('FORDITAS', BUKAS, tabla, n, '%s / %s' % (o, k),
                                          'hiányzó fordítás kimondott hiány-jelölés nélkül'))
                    else:
                        ki.append(Talalat('FORDITAS', FIGY, tabla, n, '%s / %s' % (o, k), 'a fordítás hiányzik (jelölve)'))
                    continue
                if not fm.startswith('gépi fordítás ('):
                    ki.append(Talalat('FORDITAS', BUKAS, tabla, n, fm, 'angol cella gépi-fordítás jelölés nélkül'))
                if not t or (t['angol'] != en and E.szerkesztoi(t['angol']) != en):   # F178.6: a csere után
                    ki.append(Talalat('FORDITAS', BUKAS, tabla, n, en[:60], 'az angol cella nem a tárolt fordítás'))
                elif t['modell'] not in fm:
                    ki.append(Talalat('FORDITAS', BUKAS, tabla, n, fm, 'a jelölés nem a fordító modellt nevezi meg'))
    return ki


def ell_glossza(fajlok):
    """GLOSSZA (F170, kapu (f)): a `strong_glossza_en` pontosan a TBESH/TBESG-glossza (újraszámolva), tehát nem
    KJV-Strong (GPL) vagy más forrás értéke."""
    ki = []
    fej, sorok = tsv_sorok(fajlok.get('elofordulasok.tsv', ''))
    if 'strong_glossza_en' not in fej:
        return [Talalat('GLOSSZA', BUKAS, 'elofordulasok.tsv', 2, '', 'nincs strong_glossza_en oszlop')]
    for n, d in sorok:
        vart = E.glossza_en(d['strong'])
        if d['strong_glossza_en'] != vart:
            ki.append(Talalat('GLOSSZA', BUKAS, 'elofordulasok.tsv', n, d['strong_glossza_en'][:60],
                              'nem a STEPBible-glossza (%s)' % vart))
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


# F178.6: a munkafolyamat szereplője (felhasználó, orkesztrátor) nem áll a csomagban; a döntés olvasói neve
# „szerkesztői döntés” / „editorial decision” (a felhasználó jóváhagyásával, 2026-11-08: „vegyük fel / mehet”).
SZERKESZTO_RX = re.compile(r"\b(?:[Ff]elhasználó\w*|[Oo]rkesztrátor\w*|[Oo]rchestrator\w*|user's decision|"
                           r"[Tt]he user\b|\(the user,|\bUser, \d{4})")


def ell_szerkeszto(fajlok):
    ki = []
    for rel, sz in sorted(fajlok.items()):
        for n, sor in enumerate(sz.split('\n'), 1):
            m = SZERKESZTO_RX.search(sor)
            if m:
                ki.append(Talalat('SZERKESZTO', BUKAS, rel, n, kor(sor, m),
                                  'munkafolyamat-szereplő a csomagban (olvasói név: szerkesztői döntés)'))
    return ki


# F182 (F28): a kivágott belső hivatkozás helyén maradt lyuk (az export olvasói mondatra írja át, nem vágja ki)
LYUK_RX = [
    (re.compile(r':\s*[;,)]'), 'üres hivatkozáshely („: ;”)'),
    (re.compile(r'(?:^|\s)-(?:je|ja|ből|ból|ben|ban|re|ra|val|vel|nak|nek|hez|hoz|t|et|ot|at|e|a)\b'), 'árva rag'),
    (re.compile(r'(?<![\w-])(?:[Aa]z?|[Ee]gy)\s+[;,.)]'), 'árva névelő'),
]


def ell_lyuk(fajlok):
    ki = []
    for rel, n, o, ertek in szoveg_cellak(fajlok):
        if not rel.endswith('.tsv') or angol_oszlop(o) or o.endswith('_en'):
            continue
        for rx, nev in LYUK_RX:
            m = rx.search(ertek)
            if m:
                ki.append(Talalat('LYUK', BUKAS, rel, n, kor(ertek, m), '%s [%s]' % (nev, o)))
        if ertek.count('(') > ertek.count(')') and not ertek.rstrip().endswith('…'):   # a „…”-es vágás szándékos
            ki.append(Talalat('LYUK', BUKAS, rel, n, ertek[-60:], 'nyitva maradt zárójel [%s]' % o))
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
    for kell in (E.KANONIKUS_HELY, E.SZERZO, E.ORCID, '## Mi van benne, mi nincs', 'KIADAS.txt'):
        if kell not in o:
            ki.append(Talalat('KANONIKUS', BUKAS, 'OLVASSEL.md', 1, kell, 'hiányzik'))
    k = fajlok.get('KIADAS.txt', '')
    h = hashlib.sha256(fajlok.get('ELLENORZO_OSSZEG.sha256', '').encode('utf-8')).hexdigest()
    if 'kiadas_azonosito:' not in k or h not in k or E.KANONIKUS_HELY not in k:
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
    for kell in (E.KANONIKUS_HELY, E.SZERZO, E.ORCID, '## What is in it and what is not', 'RELEASE.txt', 'KNOWN_ISSUES.md',
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
    if 'release_id:' not in r or hash_ not in r or E.KANONIKUS_HELY not in r:
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


# --- ARANY: forrásonkénti arány-kapu (F176.4) ---------------------------------------------------------------
# Óvatos mérnöki küszöbök, jogi alapjuk nincs (a #86 terv 6. szakasz 13. pontja): egy külső adatkészletből a nyílt
# magba átvett tételek aránya 1% felett FIGYELMEZTETÉS (átnézés a következő kiadás előtt), 5% felett HIBA (a kapu
# megáll; további átvétel a felhasználó döntésével vagy ügyvédi vélemény után).
ARANY_FIGY = 1.0
ARANY_HIBA = 5.0
VISSZHANG_README = os.path.join(GYOKER, 'konkordancia', 'VISSZHANG_README.md')
ARANY_INFO = []     # a legutóbbi futás soronkénti kimenete (a jelent() kiírja)


def arany_szint(darab, tetelszam):
    """-> (arány %-ban, 'rendben' | 'figy' | 'hiba'). A határérték maga (pl. 1,0%) még nem lépi át a küszöböt."""
    if tetelszam <= 0:
        return None, 'ismeretlen'
    a = 100.0 * darab / tetelszam
    if a > ARANY_HIBA:
        return a, 'hiba'
    if a > ARANY_FIGY:
        return a, 'figy'
    return a, 'rendben'


def visszhang_tetelszamok(readme_szoveg):
    """A VISSZHANG_README.md gépi olvasású tábláját olvassa: `| dataset | fajl | tetel | ...` sorok.
    -> {dataset: (fajl, tetel_int vagy 'sor')}"""
    ki = {}
    for s in readme_szoveg.split('\n'):
        if not s.startswith('| '):
            continue
        c = [x.strip().strip('`') for x in s.strip().strip('|').split('|')]
        if len(c) >= 3 and c[0] and c[0] != 'dataset' and not c[0].startswith('-'):
            if re.fullmatch(r'[0-9]+', c[2]):
                ki[c[0]] = (c[1], int(c[2]))
            elif c[2] == 'sor':
                ki[c[0]] = (c[1], 'sor')
    return ki


def sorszam_fajl(ut):
    """A fájl adatsorainak száma (a `#` sorok és az oszlopfejléc nélkül); glob is lehet."""
    import glob
    n = 0
    for f in sorted(glob.glob(ut)):
        with open(f, encoding='utf-8') as fh:
            sorok = [s for s in fh.read().split('\n') if s.strip() and not s.startswith('#')]
        n += max(0, len(sorok) - 1)
    return n


def forras_tetelszam(dataset, vissz):
    """A forrás tételszáma NEM kódba írva: a VISSZHANG_README.md táblájából, különben az adat/datasetek.tsv `fajl` oszlopából."""
    if dataset in vissz:
        fajl, t = vissz[dataset]
        return sorszam_fajl(os.path.join(GYOKER, fajl)) if t == 'sor' else t
    with open(os.path.join(GYOKER, 'adat', 'datasetek.tsv'), encoding='utf-8') as f:
        for s in f.read().split('\n'):
            m = s.split('\t')
            if len(m) > 2 and m[1] == dataset and m[2].strip():
                return sorszam_fajl(os.path.join(GYOKER, m[2].strip()))
    return 0


def ell_arany(fajlok):
    """Forrásonként: <forrás>: <nyílt mag tételei> / <forrás tételszáma> = <arány>% (1% felett FIGY, 5% felett BUKÁS).
    A nyílt mag tétele: az `elofordulasok.tsv` sora, amelynek `forras_dataset` (`;`-vel tagolt) vagy `szotar` oszlopa a forrást
    nevezi. A visszhang-források mindig szerepelnek a kiíratásban (akkor is, ha még 0 tétel hivatkozik rájuk)."""
    ki = []
    del ARANY_INFO[:]
    try:
        vissz = visszhang_tetelszamok(open(VISSZHANG_README, encoding='utf-8').read())
    except OSError:
        vissz = {}
    fej, sorok = tsv_sorok(fajlok['elofordulasok.tsv'])
    szaml = {}
    for _, d in sorok:
        nevek = {x.strip() for x in d.get('forras_dataset', '').split(';') if x.strip()}
        if d.get('szotar', '').strip():
            nevek.add(d['szotar'].strip())
        for n in nevek:
            szaml[n] = szaml.get(n, 0) + 1
    for n in vissz:
        szaml.setdefault(n, 0)
    for n in sorted(szaml):
        t = forras_tetelszam(n, vissz)
        a, szint = arany_szint(szaml[n], t)
        if szint == 'ismeretlen':
            ARANY_INFO.append('%s: %d / ? (a forrás tételszáma nem állapítható meg)' % (n, szaml[n]))
            if szaml[n] > 0:
                ki.append(Talalat('ARANY', FIGY, 'elofordulasok.tsv', 1, n, 'a forrás tételszáma nem állapítható meg, az arány nem ellenőrizhető (%s: %d / ?): vegyük fel a VISSZHANG_README.md tételszám-táblájába vagy a datasetek.tsv sorába' % (n, szaml[n])))
            continue
        ARANY_INFO.append('%s: %d / %d = %.2f%%' % (n, szaml[n], t, a))
        if szint == 'hiba':
            ki.append(Talalat('ARANY', BUKAS, 'elofordulasok.tsv', 1, n, 'a nyílt mag tételeinek aránya %.2f%% > %.0f%% (%s: %d / %d)' % (
                a, ARANY_HIBA, n, szaml[n], t)))
        elif szint == 'figy':
            ki.append(Talalat('ARANY', FIGY, 'elofordulasok.tsv', 1, n, 'a nyílt mag tételeinek aránya %.2f%% > %.0f%%: átnézés a következő kiadás előtt (%s: %d / %d)' % (
                a, ARANY_FIGY, n, szaml[n], t)))
    return ki


# --- VISSZHANG (F198): a hatástörténet-táblák csak a jóváhagyott forrásokból állhatnak ----------------------------
VISSZHANG_ENGEDETT = {
    'visszhang_megfelelok.tsv': ('forras', {'targum', 'vulgata', 'lxx'}),
    'visszhang_tanuk.tsv': ('forras', {'hcf', 'sefaria', 'glossa'}),
}
VISSZHANG_TILTOTT = re.compile(r'chain[ _-]?lineage|mblida|biblindex|blidstein', re.I)


def ell_visszhang(fajlok):
    """VISSZHANG: a Chain Lineage-tanú (nincs licence) és a BDB-sor nem szerepelhet a hatástörténet-táblákban; csak a
    jóváhagyott `forras`-értékek állhatnak; a vitatott források táblájában nincs összefoglaló-szöveg; minden sor
    forrás-megnevezést és licencet hordoz, a licenc nem lehet tisztázatlan."""
    ki = []
    for rel in ('visszhang_megfelelok.tsv', 'visszhang_tanuk.tsv', 'vitatott_forrasok.tsv', 'sblgnt_apparatus.tsv'):
        fej, sorok = tsv_sorok(fajlok.get(rel, ''))
        if 'osszefoglalo' in fej or 'osszefoglalo_en' in fej:
            ki.append(Talalat('VISSZHANG', BUKAS, rel, 2, 'osszefoglalo', 'a vitatott források összefoglaló-szövege nincs a csomagban'))
        for n, d in sorok:
            for o in fej:
                m = VISSZHANG_TILTOTT.search(d[o])
                if m:
                    ki.append(Talalat('VISSZHANG', BUKAS, rel, n, kor(d[o], m), 'licenc nélküli forrás (Chain Lineage) a csomagban'))
            if rel in VISSZHANG_ENGEDETT:
                o, ok = VISSZHANG_ENGEDETT[rel]
                if d[o] not in ok:
                    ki.append(Talalat('VISSZHANG', BUKAS, rel, n, d[o], 'nem jóváhagyott forrás-érték'))
            if rel != 'vitatott_forrasok.tsv':
                if not d.get('forras_megnevezes') or d.get('forras_licenc') in ('', 'tisztázatlan'):
                    ki.append(Talalat('VISSZHANG', BUKAS, rel, n, '', 'a sorból hiányzik a forrás megnevezése vagy a licenc'))
    return ki


def ell_helyorzo(fajlok):
    """HELYORZO: nyers helyőrző (`[A LEXIKON CÍME]`, `[HELYŐRZŐ…]`, `<…_URL>`) nem állhat a csomagban; a cím a
    megállapított cím, a közzétételi hely a DOI-hivatkozás, a szerző és az ORCID a README-ben és az OLVASSEL-ben áll."""
    ki = []
    for rel, sz in sorted(fajlok.items()):
        for i, sor in enumerate(sz.split('\n'), 1):
            m = E.NYERS_HELYORZO.search(sor)
            if m:
                ki.append(Talalat('HELYORZO', BUKAS, rel, i, kor(sor, m), 'nyers helyőrző a csomagban: ' + m.group(0)))
    if E.LEXIKON_CIME not in fajlok.get('OLVASSEL.md', '') or E.LEXIKON_CIME_EN not in fajlok.get('README.md', ''):
        ki.append(Talalat('HELYORZO', BUKAS, 'OLVASSEL.md', 1, E.LEXIKON_CIME, 'a lexikon címe nem áll a README-ben / OLVASSEL-ben'))
    return ki


def mer(fajlok, kimenet=None, ujra=True):
    ki = []
    for rel in KOTELEZO:
        if rel not in fajlok:
            ki.append(Talalat('BAJTAZONOS', BUKAS, rel, 1, '', 'a csomag kötelező fájlja hiányzik'))
    if ki:
        return ki
    for f in (ell_belso, ell_angol, ell_kodkonyv, ell_licenc, ell_reteg, ell_hibak, ell_hivatkozas, ell_csoport, ell_kh_nev,
              ell_osis, ell_cimke, ell_forditas, ell_glossza, ell_osszeg, ell_kanonikus, ell_termekreteg, ell_ketnyelv, ell_olvasas, ell_arany,
              ell_szerkeszto, ell_lyuk, ell_visszhang, ell_helyorzo):
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
    for s in ARANY_INFO:
        print('ARANY  %s' % s)
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
