#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gepi_commit_uzenet.py -- F201 (DT-F201c): a main-re futo gepi Action egyetlen commitjanak uzenete.

Eddig a szamkiosztas, a FELADATOK.md-frissites, az ELOSZURES es a GERINC_TERKEP kulon-kulon commitolt
minden merge utan; most egy futas = egy commit. Az uzenet elso sora:
  - `szamkiosztas: DT-F.. → DT..` , ha tortent szamkiosztas (az E32 ezt a sort olvassa a git logbol, ezert
    az alakja valtozatlan; a szamkiosztas.py uzenetfajljabol jon);
  - egyebkent `FELADATOK.md frissítés (gép)`, ha a feladatkovetes valtozott; vagy `GERINC_TERKEP frissítés (gép)`,
    vagy `ELOSZURES frissítés (gép)` (a regi, az E30 altal gepinek ismert alakok).
A torzs felsorolja, mi valtozott a commitban (a staged fajlokbol).

    python eszkozok/gepi_commit_uzenet.py [--szam-uzenet FAJL]   # a `git diff --cached` alapjan, stdout
"""

import argparse
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# (felirat, elso sor, [utonevek / elotagok]) -- a sorrend az elso sor prioritasa
CSOPORTOK = (
    ('FELADATOK.md frissítés (gép)', ('FELADATOK.md', 'FELADATTERKEP.html', 'feladatterkep.json')),
    ('GERINC_TERKEP frissítés (gép)', ('naplok/GERINC_TERKEP.',)),
    ('ELOSZURES frissítés (gép)', ('naplok/ELOSZURES_',)),
)
UJRAGEN = (
    ('lexikon/', 'a számtól függő lexikonlapok újragenerálva'),
    ('nyilt_mag/', 'a nyílt mag újragenerálva'),
)


def valtozott(gyoker):
    p = subprocess.run(['git', 'diff', '--cached', '--name-only', '-z'], cwd=gyoker, capture_output=True)
    return [s for s in p.stdout.decode('utf-8', 'replace').split('\0') if s]


def uzenet(fajlok, szam_uzenet=None):
    cimek = []
    for cim, mintak in CSOPORTOK:
        if any(f == m or f.startswith(m) for f in fajlok for m in mintak):
            cimek.append(cim)
    if szam_uzenet:
        elso = szam_uzenet.strip().split('\n', 1)[0]
    elif cimek:
        elso = cimek[0]
    else:
        elso = 'FELADATOK.md frissítés (gép)'
    sorok = [elso, '']
    if szam_uzenet and len(szam_uzenet.strip().split('\n')) > 1:
        sorok += szam_uzenet.strip().split('\n')[1:] + ['']
    resz = []
    if szam_uzenet:
        resz.append('számkiosztás (és a dokumentumok cseréje)')
    for mintak, leiras in UJRAGEN:
        if any(f.startswith(mintak) for f in fajlok):
            resz.append(leiras)
    for cim in cimek:
        resz.append(cim.replace(' frissítés (gép)', ' frissítve'))
    sorok.append('Egy futás, egy commit (F201): ' + '; '.join(resz) + '.' if resz else 'Egy futás, egy commit (F201).')
    return '\n'.join(sorok) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--szam-uzenet', default=None, help='a szamkiosztas.py uzenetfajlja (ha volt kiosztas)')
    ap.add_argument('--gyoker', default='.')
    a = ap.parse_args()
    szam = None
    if a.szam_uzenet and os.path.exists(a.szam_uzenet):
        with open(a.szam_uzenet, 'rb') as f:
            szam = f.read().decode('utf-8')
    sys.stdout.write(uzenet(valtozott(a.gyoker), szam))
    return 0


if __name__ == '__main__':
    sys.exit(main())
