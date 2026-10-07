#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_karoli_lefedettseg.py -- F38 / DT-F38j: a BDB-forditas
es a Karoli-Strong parositas (#22) szinkronja.

Ket kerdesre felel, csak olvasva:
  1. A kovetkezo BDB-adag (kb. 500 000 forraskarakter a sorrendben) szocikkeinek
     hany szazalekahoz ad Karoli-alakot az adatblokk (eszkozok/bdb_adatblokk.py
     parok()) -- indulhat-e az adag a DT-F38j kuszobe (85%) szerint.
  2. A meg nem parositott konyvek kozul melyik hozna a legtobb uj Karoli-tamaszt
     a kovetkezo adagoknak (a #22 konyvsorrendjenek BDB-szempontu javaslata).

A 2. pont becsles: az elofordulast a TAHOT_kivonat.tsv adja (nem teljes, CLAUDE.md),
es nem minden elofordulasbol lesz sikeres par. A dontes a #22 sajat meneteben
a felhasznaloe.

    python naplok/BDB_FORDITAS_karoli_lefedettseg.py
    python naplok/BDB_FORDITAS_karoli_lefedettseg.py --tol 649 --adagok 3

TSV-olvasas split('\\t'), a csv modul tilos (CLAUDE.md).
"""

import argparse
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import bdb_adatblokk as B  # noqa: E402

SORREND_UT = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_sorrend.tsv')
FORDITASOK_UT = os.path.join(REPO, 'adat', 'forditasok.tsv')
TAHOT_UT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')

KUSZOB = 85.0          # DT-F38j: ennel kisebb lefedettsegu adag nem indul
ADAG_KARAKTER = 500000  # a brief szerinti adagmeret


def strong_szam(s):
    m = re.match(r'^H0*(\d+)', s)
    return int(m.group(1)) if m else None


def sorrend():
    ki = []
    with open(SORREND_UT, encoding='utf-8') as fh:
        for line in fh:
            m = line.rstrip('\n').split('\t')
            if m and m[0].isdigit():
                ki.append((int(m[0]), m[1], int(m[3])))
    return ki


def kesz_strongok():
    kesz = set()
    with open(FORDITASOK_UT, encoding='utf-8') as fh:
        for line in fh:
            m = line.rstrip('\n').split('\t')
            if len(m) > 3 and m[0] == 'BDB' and m[3] == 'teljes':
                kesz.add(m[1])
    return kesz


def tahot_konyvek():
    """{strong_szam: set(konyv)} a TAHOT-bol."""
    d = {}
    with open(TAHOT_UT, encoding='utf-8') as fh:
        next(fh)
        for line in fh:
            m = line.rstrip('\n').split('\t')
            if len(m) < 2:
                continue
            k = strong_szam(m[1])
            if k is None:
                continue
            d.setdefault(k, set()).add(m[0].rsplit(' ', 1)[0])
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tol', type=int, help='az adag elso sorrend-sora (alapertelmezes: az elso kesz nelkuli)')
    ap.add_argument('--adagok', type=int, default=3, help='hany adagot mer elore (alapertelmezes: 3)')
    a = ap.parse_args()

    sor = sorrend()
    kesz = kesz_strongok()
    parok = B.parok()
    lefedett = set(B.lefedett_konyvek())
    tahot = tahot_konyvek()

    tol = a.tol or next((sz for sz, st, _k in sor if st not in kesz), None)
    if tol is None:
        print('A sorrend minden sora kesz.')
        return

    # adagok: kb. ADAG_KARAKTER forraskarakterenkent a tol-tol
    adagok, akt, c = [], [], 0
    for sz, st, kar in sor:
        if sz < tol:
            continue
        akt.append((sz, st))
        c += kar
        if c >= ADAG_KARAKTER:
            adagok.append(akt)
            akt, c = [], 0
            if len(adagok) == a.adagok:
                break
    if akt and len(adagok) < a.adagok:
        adagok.append(akt)

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'Parositott konyvek: {", ".join(sorted(lefedett))}')
    print(f'Kuszob (DT-F38j): {KUSZOB:.0f}%\n')
    print('| adag (sorrend) | szocikk | Karoli-par | % | indulhat |')
    print('|---|---|---|---|---|')
    for i, ad in enumerate(adagok, 1):
        n = len(ad)
        van = sum(1 for _sz, st in ad if strong_szam(st) in parok)
        p = 100.0 * van / max(n, 1)
        print(f'| +{i} ({ad[0][0]}–{ad[-1][0]}) | {n} | {van} | {p:.0f}% | {"igen" if p >= KUSZOB else "nem"} |')

    # konyvenkenti nyereseg: a mert adagok par nelkuli szocikkei, amelyek a konyvben elofordulnak
    hianyzo = [strong_szam(st) for ad in adagok for _sz, st in ad if strong_szam(st) not in parok]
    nyer = {}
    for k in hianyzo:
        for kv in tahot.get(k, ()):
            if kv not in lefedett:
                nyer[kv] = nyer.get(kv, 0) + 1
    print(f'\nPar nelkuli szocikk a mert adagokban: {len(hianyzo)}')
    print('Konyvenkenti felso becsles (hany ilyen szocikk fordul elo a konyvben, TAHOT):')
    print('| konyv | uj tamasz (felso becsles) |')
    print('|---|---|')
    for kv, n in sorted(nyer.items(), key=lambda x: -x[1])[:12]:
        print(f'| {kv} | {n} |')
    print(f'\n*Proveniencia: scope=BDB-sorrend {tol}– , {len(adagok)} adag | '
          f'forras=naplok/BDB_FORDITAS_sorrend.tsv x adat/karoli_strong/parok_*.tsv x '
          f'konkordancia/TAHOT_kivonat.tsv x adat/forditasok.tsv | ts={ts}*')


if __name__ == '__main__':
    main()
