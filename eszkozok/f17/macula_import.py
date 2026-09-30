#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_import.py -- F17: a Macula-import fuggvenykonyvtara (a futtato: macula_futtat.py).

Bemenet (ket helyi klon, --heber / --gorog):
  Clear-Bible/macula-hebrew  WLC/lowfat/*-lowfat.xml   (CC BY 4.0, Biblica)
  Clear-Bible/macula-greek   Nestle1904/tsv, SBLGNT/tsv (CC BY 4.0, Biblica)
Kimenet:
  konkordancia/Macula_heber_<Konyv>.tsv   (39 fajl, F17.9) morfema-szintu sorok, Strong + Karoli-kulcs (KK)
  konkordancia/Macula_gorog.tsv   szo-szintu sorok (N1904 + SBLGNT), Strong + Karoli-kulcs
  naplok/F17_illesztetlen.tsv     az illesztetlen sorok / versek / Strong-szamok listaja
  naplok/F17_import_naplo.md      forras, licenc, verzio, sorszamok, a #8 ellenorzo szama

NEM importalt mezok (licenc / mereten kivul): a heber `sdbh`, `lexdomain`, `coredomain`,
`contextualdomain`, `sensenumber` es a gorog `domain`, `ln` (UBS MARBLE/SDBH: "Used with
permission", nem CC BY -- l. naplok/F17_import_naplo.md); tovabba mandarin, transliteration,
frame, participantref, subjref, referent (nem kellenek; javaslat-tetel a DONTESEK.md-ben).

Futtatas: python eszkozok/f17/macula_import.py --heber <klon> --gorog <klon>
"""

import argparse
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import macula_kozos as K  # noqa: E402
import macula_kk  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

XMLID = '{http://www.w3.org/XML/1998/namespace}id'
REF_RE = re.compile(r'^([A-Z0-9]{3}) (\d+):(\d+)!(\d+)$')
HEBER_URL = 'https://github.com/Clear-Bible/macula-hebrew'
GOROG_URL = 'https://github.com/Clear-Bible/macula-greek'

HEBER_OSZLOP = ['xml_id', 'ref', 'karoli', 'kk_mod', 'allapot', 'szo', 'lemma', 'strong', 'strong_x',
                'strong_illesztes', 'morf', 'szofaj', 'gloss', 'gorog_lxx', 'gorog_strong']
GOROG_OSZLOP = ['kiadas', 'xml_id', 'ref', 'karoli', 'kk_mod', 'allapot', 'szo', 'lemma', 'strong',
                'strong_x', 'strong_illesztes', 'morf', 'szofaj', 'gloss', 'english']


def ma():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def git_sha(mappa):
    r = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=mappa, capture_output=True, text=True, encoding='utf-8')
    return r.stdout.strip()


def strong_ertek(nyers, elotag):
    """'0871a' -> ('H0871', 'a'); '7225' -> ('H7225', ''); '' -> ('', '') (csak az LXX-oszlophoz)."""
    m = re.match(r'^(\d+)([a-z]*)$', (nyers or '').strip())
    if not m or int(m.group(1)) == 0:
        return '', ''
    return '%s%04d' % (elotag, int(m.group(1))), m.group(2)


TARTALMI_POS = ('noun', 'verb', 'adjective', 'adverb', 'pronoun')
FUNKCIO_POS = ('conjunction', 'suffix', 'preposition')


def funkcio_alapok_gyujt(lista):
    """Azok a szamok, amelyek betujeles kodja valahol elo-/utotag/kotoszo szerepu (Macula-azonosito-csalad)."""
    ki = set()
    for nn, fn, a in lista:
        m = re.match(r'^(\d+)[a-z]+$', a.get('strongnumberx', '') or '')
        if m and a.get('pos') in FUNKCIO_POS:
            ki.add(int(m.group(1)))
    return ki


def strong_feldolgoz(nyers, elotag, pos, szotar, heber, funkcio_alapok=frozenset()):
    """(strong, illesztes). A Macula heber `strongnumberx` erteke NEM mindig Strong-szam:
    a betujeles kod funkcio-morfemanal (elo-/utotag, kotoszo, nevelo) Macula-azonosito
    (pl. 0871a = a `be-` elo-tag, nem a H0871 Atharim). Szabaly:
      - tiszta szam -> H####; ha a Strong_szotar.tsv-ben van: `igen`
      - betujeles + tartalmi szofaj -> az alap-szam, `javaslat:betu_alap` (a betu nincs feloldva)
      - betujeles + funkcio-morfema -> nincs Strong, `javaslat:funkcio_kod` (strong_x megorzi)
      - nincs a szotarban -> `javaslat:nincs_szotarban`; nulla/ures -> `javaslat:nincs_strong`
      - '|' (heber) tobb kod egy elemen -> `tobbes` jelzes; ilyenkor a betujeles resz mindig funkcio_kod,
        es ha barmelyik resz nem illeszthetö, a `strong` ures (strong_x orzi)"""
    nyers = (nyers or '').strip()
    if not nyers:
        return '', 'javaslat:nincs_strong'
    reszek = re.split(r'\|', nyers) if heber else re.split(r'\+', nyers)
    acc, okok = [], set()
    if heber and len(reszek) > 1:
        okok.add('tobbes')
    for r in reszek:
        m = re.match(r'^(\d+)([a-z]*)$', r.strip())
        if not m:
            okok.add('ertelmezhetetlen')
            continue
        n = int(m.group(1))
        if n == 0:
            okok.add('nincs_strong')
            continue
        betu = m.group(2)
        if betu and (not heber or len(reszek) > 1 or pos not in TARTALMI_POS):
            okok.add('funkcio_kod')
            continue
        if betu and n in funkcio_alapok:
            okok.add('funkcio_kod')   # a szamcsalad mas elemei funkcio-morfemak (pl. 1886a/c/d)
            continue
        h = '%s%04d' % (elotag, n)
        if h not in szotar:
            okok.add('nincs_szotarban')
            continue
        if betu:
            okok.add('betu_alap')
        acc.append(h)
    if 'tobbes' in okok and len(okok) > 1:
        acc = []   # tobb kod egy elemen es valamelyik nem Strong: nem talalgatunk, strong ures (strong_x orzi)
    return '+'.join(acc), ('igen' if not okok else 'javaslat:' + '|'.join(sorted(okok)))


def allapot_strong_szerint(allapot, sill):
    """Ha a Strong nem illesztheto (sill != 'igen'), a sor allapota javaslat (brief 2. lepes)."""
    if sill == 'igen':
        return allapot
    ok = 'strong_' + sill.replace('javaslat:', '').replace('|', '+')
    if allapot == 'rendben':
        return 'javaslat:' + ok
    return allapot + '|' + ok


def szotar_strongok():
    fej, sorok = K.tsv_olvas(os.path.join(K.KONK, 'Strong_szotar.tsv'))
    return {s[0] for s in sorok}


def heber_sorok(mappa, konyvek_usfm):
    """A lowfat fajlok <w> elemei: (nn, fajlnev, attr-dict, szoveg), dokumentum-sorrendben."""
    lista = []
    fajlok = []
    for fn in sorted(os.listdir(mappa)):
        m = re.fullmatch(r'(\d+)-([A-Za-z0-9]+)-(\d+)-lowfat\.xml', fn)
        if m:
            fajlok.append((int(m.group(1)), int(m.group(3)), fn))
    fajlok.sort()
    for nn, fej, fn in fajlok:
        for ev, el in ET.iterparse(os.path.join(mappa, fn)):
            if el.tag == 'w':
                a = dict(el.attrib)
                a['_szoveg'] = (el.text or '')
                a['xml_id'] = a.pop(XMLID, '')
                lista.append((nn, fn, a))
                el.clear()
    return lista


def gorog_sorok(ut):
    fej, sorok = K.tsv_olvas(ut)
    ix = {n: i for i, n in enumerate(fej)}
    return ix, sorok


def alap_alak(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s or '')
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub('[^א-ת]', '', s)


def karoli_cimke(kulcs):
    return '%s %d:%d' % kulcs


def kk_ertek(lista):
    """Az MT-vers Karoli-megfeleloi -> (karoli, kk_mod, allapot)."""
    if not lista:
        return '', 'nincs', 'javaslat:nincs_karoli_vers'
    kulcsok = sorted({kk for kk, e in lista})
    karoli = ';'.join(karoli_cimke(k) for k in kulcsok)
    modok = sorted({e['forras'] for kk, e in lista})
    okok = sorted({e['ok'] for kk, e in lista if e['biz'] != 'rendben' and e['ok']})
    allapot = 'rendben' if not okok else 'javaslat:' + '|'.join(okok)
    return karoli, '+'.join(modok), allapot


def tsv_ir(ut, fejlec, oszlopok, sorok):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for h in fejlec:
            f.write('# %s\n' % K.tisztit(h))
        f.write('\t'.join(oszlopok) + '\n')
        for s in sorok:
            if len(s) != len(oszlopok):
                raise ValueError('oszlopszam-elteres: %r' % (s,))
            f.write('\t'.join(K.tisztit(x) for x in s) + '\n')


def fejlec_sorok(url, verzio, licenc, parancs, oszlop_megj):
    return ['GENERÁLT: eszkozok/f17/macula_futtat.py — kézzel nem szerkesztendő.',
            'forras=%s@%s | licenc=%s | ts=%s' % (url, verzio, licenc, ma()),
            'proveniencia: scope=teljes import (F17, FELADATOK #17) | forras=%s | ts=%s' % (url, ma()),
            'futtatasi parancs: %s' % parancs,
            oszlop_megj]


# A héber tábla könyvenkénti bontása (F17.9): a fájlnév a LXX_kivonat_*.tsv névadását követi
# (ASCII magyar könyvnév), a sorrend a Macula-kánon (= USFM_OSZ) sorrendje.
HEBER_KONYV_FAJL = {
    'GEN': 'Genezis', 'EXO': 'Exodus', 'LEV': 'Leviticus', 'NUM': 'Numeri', 'DEU': 'Deuteronomium',
    'JOS': 'Jozsue', 'JDG': 'Birak', 'RUT': 'Ruth', '1SA': 'Samuel_1', '2SA': 'Samuel_2',
    '1KI': 'Kiralyok_1', '2KI': 'Kiralyok_2', '1CH': 'Kronikak_1', '2CH': 'Kronikak_2',
    'EZR': 'Ezsdras', 'NEH': 'Nehemias', 'EST': 'Eszter', 'JOB': 'Job', 'PSA': 'Zsoltarok',
    'PRO': 'Peldabeszedek', 'ECC': 'Predikator', 'SNG': 'Enekek_Eneke', 'ISA': 'Ezsaias',
    'JER': 'Jeremias', 'LAM': 'Siralmak', 'EZK': 'Ezekiel', 'DAN': 'Daniel', 'HOS': 'Hoseas',
    'JOL': 'Joel', 'AMO': 'Amos', 'OBA': 'Abdias', 'JON': 'Jonas', 'MIC': 'Mikeas', 'NAM': 'Nahum',
    'HAB': 'Habakuk', 'ZEP': 'Sofonias', 'HAG': 'Aggeus', 'ZEC': 'Zakarias', 'MAL': 'Malakias',
}


def konyv_fejlec(fejlec, kod, db):
    """A közös fejléc + egy könyv-sor (kód, fájlnév-tag, sorszám); a bontó és a futtató is ezt használja."""
    return list(fejlec) + ['konyv=%s (%s) | sorok=%d | a Macula_heber tabla konyvenkenti bontasa (F17.9); '
                           'a konyvfajlok a Macula-kanon sorrendjeben (HEBER_KONYV_FAJL, eszkozok/f17/macula_import.py) osszefuzve, a fejlecek nelkul a teljes tabla torzset adjak' % (kod, HEBER_KONYV_FAJL[kod], db)]


def tsv_ir_konyvenkent(konyvtar, fejlec, oszlopok, sorok):
    """Könyvenkénti kiírás: konkordancia/Macula_heber_<Konyv>.tsv; a sor 2. oszlopa a ref ('GEN 1:1!1').
    Visszaad: [(fájlnév, sorszám)] a Macula-sorrendben."""
    csoportok = []
    for s in sorok:
        kod = s[1].split(' ')[0]
        if not csoportok or csoportok[-1][0] != kod:
            if any(c[0] == kod for c in csoportok):
                raise ValueError('a konyv sorai nem osszefuggoek: %s' % kod)
            csoportok.append((kod, []))
        csoportok[-1][1].append(s)
    ki = []
    for kod, ss in csoportok:
        nev = 'Macula_heber_%s.tsv' % HEBER_KONYV_FAJL[kod]
        tsv_ir(os.path.join(konyvtar, nev), konyv_fejlec(fejlec, kod, len(ss)), oszlopok, ss)
        ki.append((nev, len(ss)))
    return ki
