#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F06 0. lepes: a 87 fuggo LXX-hely listajanak forrasa es lekerdezeses ellenorzese.
A lista forrasa: a lexikon/*_TUDOMANYOS.md 3. szakasz tablaja ('Igehely (Karoli)' fejlec),
ahol az 5. oszlop 'kutatoi azonositas fuggoben' (ugyanaz a szuro, mint a
naplok/FORRAS_FJ1_87_jelolt_general.py-ban), es a naplok/FORRAS_FJ1_lxx_jeloltek.tsv.
"""
import glob
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

FUGGO = 'kutatói azonosítás függőben'
tabla_sorok = []
for ut in sorted(glob.glob('lexikon/*_TUDOMANYOS.md')):
    motivum = os.path.basename(ut).replace('_TUDOMANYOS.md', '')
    be = False
    for sor in open(ut, encoding='utf-8'):
        if 'Igehely (Károli)' in sor and 'Egyezés' in sor:
            be = True
            continue
        if not be:
            continue
        if not sor.strip().startswith('|'):
            be = False
            continue
        if set(sor.strip()) <= set('|-: '):
            continue
        c = [x.strip() for x in sor.strip().strip('|').split('|')]
        if len(c) >= 6 and c[4] == FUGGO:
            tabla_sorok.append((motivum, c[0]))
print('lexikon-tablasorok (5. oszlop == függőben): %d ; egyedi (motivum, igehely): %d' % (len(tabla_sorok), len(set(tabla_sorok))))

sorok = [l.rstrip('\n').split('\t') for l in open('naplok/FORRAS_FJ1_lxx_jeloltek.tsv', encoding='utf-8')]
adat = sorok[1:]
print('munkalap: adatsor=%d ; egyedi (motivum, igehely)=%d ; egyedi igehely=%d' % (
    len(adat), len({(s[0], s[1]) for s in adat}), len({s[1] for s in adat})))
print('munkalap == lexikon-lista (halmazként): %s' % ({(s[0], s[1]) for s in adat} == set(tabla_sorok)))
