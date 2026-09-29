#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula.py -- F06 3. lepes, Macula Hebrew (N31 + a #8 bemenete).

1. Lefedettseg: konyvenkenti versszam a TAHOT-hoz merve (kulon kiemelve 1Sam-2Kron), es
   annak leltara, hany fajl van a repo BARMELY konyvtaraban az adott konyv sorszamaval.
   Megjegyzes az FJ1 eredmenyehez: az FJ1 fajlnev-mintaja (^\\d+-([A-Za-z]+)-...) a szamjegyre
   kezdodo konyvkodokat (1Sam, 2Kron...) nem illeszti -- itt a fajlnev NN-elotagja
   (kanoni sorszam) a kulcs, a fajlkod csak ellenorzo oszlop.
2. A 87 fuggo LXX-hely: naplok/FORRAS_FJ1_lxx_jeloltek.tsv (motivum, igehely oszlop) minden
   sorara: mit ad a Macula (LXX-megfelelo Strong/lemma, azonositas modja, vagy nincs adat).
   A munkalap igehelyei Karoli-szamozasuak, a Macula heber (BHS) szamozasu: a verset
   szamozas-atalakitas nelkul keressuk; ha nincs meg, allapot=NINCS_VERS.

Kimenet: naplok/F06_macula_lefedettseg.tsv, naplok/F06_macula_87_hely.tsv
"""

import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

URL = 'https://github.com/Clear-Bible/macula-hebrew'
MUNKALAP = os.path.join(kozos.NAPLOK, 'FORRAS_FJ1_lxx_jeloltek.tsv')
KIEMELT = ['1Sám', '2Sám', '1Kir', '2Kir', '1Krón', '2Krón']


def alap_alak(s):
    s = unicodedata.normalize('NFD', s or '')
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^א-ת]', '', s)


def szo_strong(w):
    for attr in ('strongnumberx', 'strong', 'stronglemma'):
        v = w.get(attr)
        if v:
            n = kozos.strong_szam(v)
            if n is not None:
                return n
    return None


def betolt(mappa):
    """{sorszam(int): {'kod': fajlkod, 'fajlok': db, 'versek': {(fej, vers): [w...]}}}"""
    konyvek = {}
    for fn in sorted(os.listdir(mappa)):
        m = re.fullmatch(r'(\d+)-([A-Za-z0-9]+)-(\d+)-lowfat\.xml', fn)
        if not m:
            continue
        nn = int(m.group(1))
        k = konyvek.setdefault(nn, {'kod': m.group(2), 'fajlok': 0, 'versek': {}})
        k['fajlok'] += 1
        for w in ET.parse(os.path.join(mappa, fn)).iter('w'):
            r = re.match(r'^\S+\s+(\d+):(\d+)', w.get('ref', ''))
            if r:
                k['versek'].setdefault((int(r.group(1)), int(r.group(2))), []).append(w)
    return konyvek


def fut(munka, parancs):
    cel = os.path.join(munka, 'macula-hebrew')
    commit, hiba = kozos.klonoz(URL, cel, sparse=['WLC/lowfat'])
    if not commit:
        raise SystemExit('HIBA: a Macula Hebrew nem toltheto le: %s' % hiba)
    if kozos.SZARAZ:
        print('macula: szaraz futas, munkalap-utvonal: %s' % os.path.exists(MUNKALAP))
        return
    step_mag, mag_step = kozos.normalizalo()
    kanoni = list(step_mag.keys())            # STEP-kodok kanoni sorrendben
    kanoni_mag = [step_mag[k] for k in kanoni]
    konyvek = betolt(os.path.join(cel, 'WLC', 'lowfat'))
    # a teljes repo fajlleltara (barmely konyvtar), sorszam szerint
    r = kozos.futtat(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=cel)
    leltar = Counter()
    for ut in r.stdout.splitlines():
        m = re.match(r'^(\d+)-', os.path.basename(ut))
        if m:
            leltar[int(m.group(1))] += 1

    # --- 1. lefedettseg
    tahot = kozos.tahot_strongok()
    tahot_versek = {}
    for igehely in tahot:
        m = re.match(r'^(\S+)\s+(\d+):(\d+)$', igehely)
        if m:
            tahot_versek.setdefault(m.group(1), set()).add((int(m.group(2)), int(m.group(3))))
    lef = []
    for i in range(39):
        nn = i + 1
        mag = kanoni_mag[i]
        mk = konyvek.get(nn)
        mv = set(mk['versek']) if mk else set()
        tv = tahot_versek.get(mag, set())
        lef.append((mag, kanoni[i], str(nn), mk['kod'] if mk else '', str(mk['fajlok'] if mk else 0),
                    str(len(mv)), str(len(tv)), str(len(mv & tv)), str(len(mv - tv)), str(len(tv - mv)),
                    str(leltar.get(nn, 0)), 'igen' if mag in KIEMELT else 'nem'))
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_macula_lefedettseg.tsv'),
                 kozos.fejlec(URL, 'commit ' + commit, parancs) + [
                     'a fajlok_lowfat a WLC/lowfat konyvtarra vonatkozik; repo_fajl_osszesen a repo barmely konyvtaraban az NN- elotagu fajlok szama'],
                 ['konyv', 'step_kod', 'sorszam', 'macula_fajlkod', 'fajlok_lowfat', 'macula_versek', 'tahot_versek',
                  'kozos_versek', 'csak_macula', 'csak_tahot', 'repo_fajl_osszesen', 'kiemelt_1Sam_2Kron'], lef)

    # --- 2. a 87 fuggo hely
    fej, sorok = kozos.tsv_olvas(MUNKALAP)
    ix = {n: fej.index(n) for n in ('motivum', 'igehely', 'heber_kulcsszo', 'heber_strong')}
    ki = []
    allapotok = Counter()
    for s in sorok:
        motivum, igehely = s[ix['motivum']], s[ix['igehely']]
        kulcsszo, munka_strong = s[ix['heber_kulcsszo']], s[ix['heber_strong']]
        m = re.match(r'^(\S+)\s+(\d+):(\d+)', igehely)
        allapot, azon, hszo, glemma, gstrong, megj = '', '', '', '', '', ''
        mk = None
        if m and m.group(1) in kanoni_mag:
            mk = konyvek.get(kanoni_mag.index(m.group(1)) + 1)
        if not m:
            allapot = 'IGEHELY_NEM_ERTELMEZHETO'
        elif mk is None:
            allapot = 'NINCS_KONYV_FAJL'
        else:
            szavak = mk['versek'].get((int(m.group(2)), int(m.group(3))))
            if not szavak:
                allapot = 'NINCS_VERS'
                megj = 'a munkalap Karoli-szamozasu, a Macula heber; szamozas-atalakitas nem tortent'
            else:
                cel_strong = kozos.strong_szam(munka_strong) if munka_strong else None
                alak = alap_alak(kulcsszo.split('(')[0])
                talalt = []
                if cel_strong is not None:
                    talalt = [w for w in szavak if szo_strong(w) == cel_strong]
                    azon = 'strong'
                if not talalt and alak:
                    talalt = [w for w in szavak if alap_alak(w.text) == alak]
                    azon = 'szoalak' if talalt else ''
                if not talalt:
                    allapot = 'HEBER_SZO_NINCS_A_VERSBEN'
                else:
                    hszo = '|'.join(w.text or '' for w in talalt)
                    glemma = '|'.join(w.get('greek') or '-' for w in talalt)
                    gstrong = '|'.join(w.get('greekstrong') or '-' for w in talalt)
                    van = [w for w in talalt if w.get('greekstrong')]
                    allapot = 'LXX_MEGFELELO' if van else 'HEBER_SZO_GOROG_NELKUL'
                    if len({w.get('greekstrong') for w in van}) > 1:
                        megj = 'tobb heber talalat, eltero gorog Strong'
        allapotok[allapot] += 1
        ki.append((motivum, igehely, kulcsszo, munka_strong, allapot, azon, hszo, glemma, gstrong, megj))
    ossz = ', '.join('%s=%d' % kv for kv in sorted(allapotok.items()))
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_macula_87_hely.tsv'),
                 kozos.fejlec(URL + ' ; ' + os.path.relpath(MUNKALAP, kozos.REPO).replace(os.sep, '/'), 'commit ' + commit, parancs)
                 + ['sorok=%d ; %s' % (len(ki), ossz)],
                 ['motivum', 'igehely', 'heber_kulcsszo', 'heber_strong_munkalap', 'allapot', 'azonositas',
                  'macula_heber_szo', 'macula_gorog', 'macula_gorog_strong', 'megjegyzes'], ki)
    print('macula: %d sor; %s' % (len(ki), ossz))
