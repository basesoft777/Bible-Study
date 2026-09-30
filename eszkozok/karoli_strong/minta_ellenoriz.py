#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P-K1 — a rögzített minta (f21p/minta.tsv) önellenőrzése és összegzése.

Ellenőrzi: 200 egyedi vers; rétegenkénti darabszám (100/25/25/50); egy vers
sincs a 61 + 30 versmegfeleltetési maradékban és a sorrend-eltérők között;
R1-ben mind KJV-támponttal; 1Móz 40 versből legalább 20 régi-arany-verse;
a tokenizálás a régi arany minta-beli soraira (minden arany Károli-szó minden
tokenje megtalálható az adott vers tokenjei között).

Kilépési kód 1, ha bármelyik feltétel sérül. Futtatás a repó gyökeréből:
    python eszkozok/karoli_strong/minta_ellenoriz.py
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402
import minta_general  # noqa: E402

MINTA = os.path.join(tokenek.ROOT, 'f21p', 'minta.tsv')


def main():
    sorok = tokenek._sorok(MINTA)
    versek = [r[1] for r in sorok]
    hibak = []
    if len(sorok) != 200 or len(set(versek)) != 200:
        hibak.append('nem 200 egyedi vers: %d / %d' % (len(sorok), len(set(versek))))
    reteg = {}
    for r in sorok:
        reteg[r[2]] = reteg.get(r[2], 0) + 1
    if reteg != {'R1': 100, 'R2': 25, 'R3': 25, 'R4': 50}:
        hibak.append('rétegszámok: %s' % reteg)
    karoli = tokenek.betolt_karoli()
    ered = tokenek.betolt_eredeti()
    a, b = tokenek.maradek(karoli, ered)
    maradek = set(a) | set(b)
    bennt = [v for v in versek if v in maradek]
    if bennt:
        hibak.append('maradék vers a mintában: %s' % bennt)
    eltero = minta_general.eltero_versek()
    bennt2 = [v for v in versek if v in eltero]
    if bennt2:
        hibak.append('sorrend-eltérő vers a mintában: %s' % bennt2)
    for r in sorok:
        if r[2] == 'R1' and tokenek.kjv_tamapont(r[1]) is None:
            hibak.append('R1 KJV-támpont nélkül: %s' % r[1])
    arany = tokenek.regi_arany()
    arany_versek = {ig for ig, _, _ in arany}
    m1 = [v for v in versek if tokenek.konyv_rovid(v) == '1Móz']
    m1_arany = [v for v in m1 if v in arany_versek]
    if len(m1) != 40 or len(m1_arany) < 20:
        hibak.append('1Móz: %d vers, ebből régi-arany %d' % (len(m1), len(m1_arany)))

    # a régi arany a mintára szűrve, tokenizálási teszt
    halmaz = set(versek)
    minta_arany = tokenek.regi_arany(halmaz)
    nem_talalt = []
    for ig, szo, strong in minta_arany:
        toks = set(tokenek.tokenizal(karoli[ig]))
        if not all(t in toks for t in tokenek.tokenizal(szo)):
            nem_talalt.append((ig, szo))

    konyvenkent = {}
    for r in sorok:
        k = tokenek.konyv_rovid(r[1])
        konyvenkent[k] = konyvenkent.get(k, 0) + 1
    print('rétegek: %s' % ', '.join('%s=%d' % kv for kv in sorted(reteg.items())))
    print('könyvenként: %s' % ', '.join('%s=%d' % kv for kv in konyvenkent.items()))
    print('1Móz: %d vers, ebből régi-arany-vers: %d' % (len(m1), len(m1_arany)))
    print('régi arany a mintában: %d sor, %d vers; tokenizálás-nem-találat: %d'
          % (len(minta_arany), len({ig for ig, _, _ in minta_arany}), len(nem_talalt)))
    for x in nem_talalt:
        print('  nem találat: %s' % (x,))
    for l in sorted(reteg):
        rs = [r for r in sorok if r[2] == l]
        print('%s: eredeti szó átlag %.1f, Károli-szó átlag %.1f' % (
            l, sum(int(r[6]) for r in rs) / len(rs), sum(int(r[7]) for r in rs) / len(rs)))
    print('maradék (61 + 30): %d + %d, mintában: %d; sorrend-eltérő: %d, mintában: %d'
          % (len(a), len(b), len(bennt), len(eltero), len(bennt2)))
    if hibak:
        print('HIBA:')
        for h in hibak:
            print('  ' + h)
        sys.exit(1)
    print('rendben')


if __name__ == '__main__':
    main()
