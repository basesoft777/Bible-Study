#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proza_1a.py -- az „1/a. Az igehelyek szövege” igehelyenkénti prózájának mérése a generált
lexikonlapon (`lexikon/[ID]_TUDOMANYOS.md`). Csak olvas; nem ír adatot és lapot.

A mérce az arany lap (ISTENTISZT-001, 1. kiadás): minden igehely Károli-szövege alatt
(a) egy teljes leíró mondat és (b) egy „Funkció:” sor áll. A lapot mérjük, nem az adatot,
mert az olvasó a lapot látja: így a hiányzó adat (üres `kapcsolodas`/`funkcio`) és a
generátor kihagyása (a „ — ” nélküli `funkcio` nem kerül a „Funkció:” sorba) egyaránt
megjelenik. A szöveg forrása az `adat/elofordulasok.tsv` `kapcsolodas` és `funkcio`
mezője (`eszkozok/lexikon_general.py`, 1/a-blokk).

Osztályok igehelyenként:
    próza:   kerek | töredék | hiányzik
    funkció: van   | töredék | hiányzik
A próza töredék, ha az idézőjeles és zárójeles részen, valamint a héber/görög betűs szón
kívül KEREK_MIN_SZO-nál kevesebb magyar (latin betűs) szó áll benne, vagy „ua.”-val kezdődik
és utána sincs elég szó. A funkció töredék, ha FUNKCIO_MIN_SZO-nál kevesebb szóból áll.
Az igehely kerek, ha a prózája kerek ÉS van „Funkció:” sora.

Használat:
    python eszkozok/proza_1a.py [ID ...] [--reszletes]
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEREK_MIN_SZO = 7      # az arany lap legrövidebb kerek prózája (ApCsel 22:16) 7 ilyen szó
FUNKCIO_MIN_SZO = 3    # az arany lap legrövidebb funkció-magyarázata („a próbatétel kudarca”) 3 szó

CIM_1A = '#### 1/a. Az igehelyek szövege'
CIM_1A_UJ = '#### 2.1. Az igehelyek szövege'   # F178.4: az új lapszerkezetben (2. Előfordulások, 2.1)
HORGONY = re.compile(r'^<a id="ige-[^"]*"></a>\s*$')
IDEZET = re.compile(r'"[^"]*"|„[^”"]*[”"]|»[^«]*«|“[^”]*”')
ZAROJEL = re.compile(r'\([^()]*\)')
MEGJEGYZES = re.compile(r'<!--.*?-->')
MAGYAR_SZO = re.compile(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüűÄäËëÏïÔôÛû]+')


def magyar_szavak(szoveg):
    """A latin betűs szavak száma az idézet, a zárójeles betét és a héber/görög szó nélkül."""
    t = IDEZET.sub(' ', szoveg)
    t = ZAROJEL.sub(' ', t)
    return len(MAGYAR_SZO.findall(t))


def proza_osztaly(proza):
    p = proza.strip()
    if not p:
        return 'hiányzik'
    if magyar_szavak(p) < KEREK_MIN_SZO:
        return 'töredék'
    return 'kerek'


def funkcio_osztaly(funkcio):
    f = (funkcio or '').strip()
    if not f:
        return 'hiányzik'
    if len(MAGYAR_SZO.findall(f)) < FUNKCIO_MIN_SZO:
        return 'töredék'
    return 'van'


def blokkok(szoveg):
    """[(igehely, próza, funkció)] az 1/a részből; üres lista, ha a lapon nincs 1/a."""
    sorok = szoveg.replace('\r', '').split('\n')
    kezdet = next((i for i, s in enumerate(sorok) if s in (CIM_1A, CIM_1A_UJ)), None)
    if kezdet is None:
        return []
    ki, akt = [], None
    for sor in sorok[kezdet + 1:]:
        if sor.startswith('## ') or sor.startswith('### ') or sor.startswith('#### '):
            break
        if HORGONY.match(sor):
            if akt:
                ki.append(akt)
            akt = {'igehely': '', 'proza': [], 'funkcio': ''}
            continue
        if akt is None:
            continue
        s = MEGJEGYZES.sub('', sor).strip()
        if not s:
            continue
        if not akt['igehely'] and s.startswith('**') and s.endswith('**'):
            akt['igehely'] = s.strip('*')
        elif s.startswith('*') and s.endswith('*') and not s.startswith('**'):
            continue  # Károli-szöveg
        elif s.startswith('Funkció:'):
            akt['funkcio'] = s[len('Funkció:'):].strip()
        else:
            akt['proza'].append(s)
    if akt:
        ki.append(akt)
    return [(b['igehely'], ' '.join(b['proza']), b['funkcio']) for b in ki]


def meres(szoveg):
    """[(igehely, próza-osztály, funkció-osztály, próza)] igehelyenként."""
    return [(ig, proza_osztaly(p), funkcio_osztaly(f), p) for ig, p, f in blokkok(szoveg)]


def osszesit(meres_lista):
    d = {'igehely': len(meres_lista), 'kerek': 0, 'töredék': 0, 'hiányzik': 0,
         'funkcio_van': 0, 'funkcio_töredék': 0, 'funkcio_hiányzik': 0, 'arany': 0}
    for _ig, po, fo, _p in meres_lista:
        d[po] += 1
        d['funkcio_' + fo] += 1
        d['arany'] += (po == 'kerek' and fo == 'van')
    return d


def lap_meres(motivum_id, gyoker=GYOKER):
    ut = os.path.join(gyoker, 'lexikon', motivum_id + '_TUDOMANYOS.md')
    if not os.path.exists(ut):
        return None
    with open(ut, encoding='utf-8') as f:
        return meres(f.read())


def lap_idk(gyoker=GYOKER):
    d = os.path.join(gyoker, 'lexikon')
    if not os.path.isdir(d):
        return []
    return sorted(n[:-len('_TUDOMANYOS.md')] for n in os.listdir(d) if n.endswith('_TUDOMANYOS.md'))


def main():
    ap = argparse.ArgumentParser(description='Az 1/a igehelyenkénti prózájának mérése a lexikonlapokon')
    ap.add_argument('id', nargs='*', help='motívum-ID-k (alapból minden lexikonlap)')
    ap.add_argument('--reszletes', action='store_true', help='a nem kerek igehelyek listája')
    a = ap.parse_args()
    print('| motívum | igehely | próza kerek | töredék | hiányzik | Funkció van | töredék | hiányzik | arany szint |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    reszlet = []
    for mid in a.id or lap_idk():
        m = lap_meres(mid)
        if m is None:
            print('| %s | — nincs lap — |||||||' % mid)
            continue
        d = osszesit(m)
        print('| %s | %d | %d | %d | %d | %d | %d | %d | %d |' % (
            mid, d['igehely'], d['kerek'], d['töredék'], d['hiányzik'], d['funkcio_van'],
            d['funkcio_töredék'], d['funkcio_hiányzik'], d['arany']))
        reszlet.extend((mid,) + x for x in m if not (x[1] == 'kerek' and x[2] == 'van'))
    if a.reszletes:
        print()
        for mid, ig, po, fo, p in reszlet:
            print('- %s %s — próza: %s, funkció: %s — %s' % (mid, ig, po, fo, p[:100]))


if __name__ == '__main__':
    main()
