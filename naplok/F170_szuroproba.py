#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F170_szuroproba.py -- a gépi angol fordítás szúrópróbája (F170, 6. lépés): 30 véletlen cella (rögzített mag: 170)
az `adat/nyilt_angol.tsv`-ből, magyar–angol párban, egyedi szövegenként. Csak olvas; a kimenet a szabványos kimenet.
Használat: python naplok/F170_szuroproba.py [--n 30] [--mag 170]
"""
import argparse
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=30)
    ap.add_argument('--mag', type=int, default=170)
    a = ap.parse_args()
    with open(os.path.join(GY, 'adat', 'nyilt_angol.tsv'), encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ds = [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]
    egyedi = {}
    for d in sorted(ds, key=lambda d: (d['tabla'], d['oszlop'], d['sorkulcs'])):
        egyedi.setdefault(d['forras_hash'], d)
    lista = sorted(egyedi.values(), key=lambda d: d['forras_hash'])
    minta = random.Random(a.mag).sample(lista, min(a.n, len(lista)))
    for i, d in enumerate(minta, 1):
        print('### %d. %s / %s — %s (%s)' % (i, d['tabla'], d['oszlop'], d['sorkulcs'], d['modell']))
        print('HU: ' + d['forras_hu'])
        print('EN: ' + d['angol'])
        print()


if __name__ == '__main__':
    main()
