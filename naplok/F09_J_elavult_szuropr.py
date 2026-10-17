#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F09_J_elavult_szuropr.py -- DT-F09g szúrópróba: 15 véletlen `elavult_adat`-sor (rögzített seed) a
`render_diff_osztalyoz.py --proba` osztályozásából. Minden mintához megadja, hol él tovább a régi tartalom az
új (próba) kimenetben (próba-sorszám + részlet), a mechanikus feltétel (`ProbaSzoveg.tovabb_el`) szerint.
A kézi megítélés a naplok/SZOTAR_S2_elavult_szuropr.md-ben áll.

    python naplok/F09_J_elavult_szuropr.py [--seed 20261017] [--n 15]
"""

import argparse
import io
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))

import render_diff_osztalyoz as R  # noqa: E402

PROBA = os.path.join(ROOT, 'generalt_proba', 'F09_szotar_s2_proba', 'lexikon')
ELES = os.path.join(ROOT, 'lexikon')


def olvas(ut):
    with io.open(ut, encoding='utf-8', newline='') as f:
        return f.read().replace('\r\n', '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=20261017)
    ap.add_argument('--n', type=int, default=15)
    a = ap.parse_args()
    minden = []   # (fajl, irany, sor)
    for f in sorted(os.listdir(PROBA)):
        if not f.endswith('_TUDOMANYOS.md'):
            continue
        eredmeny = R.proba_osztalyoz(f, olvas(os.path.join(ELES, f)), olvas(os.path.join(PROBA, f)))
        for irany in ('torolt', 'hozzaadott'):
            for s in eredmeny.get('elavult_adat', {}).get(irany, []):
                minden.append((f, irany, s))
    torolt = [x for x in minden if x[1] == 'torolt']
    print('elavult_adat sorok (a _TUDOMANYOS fájlokban): összesen %d, ebből törölt (régi tartalom) %d, hozzáadott %d'
          % (len(minden), len(torolt), len(minden) - len(torolt)))
    print('minta: a TÖRÖLT sorokból (a régi tartalom sorsa a kérdés), seed=%d, n=%d' % (a.seed, a.n))
    rnd = random.Random(a.seed)
    minta = rnd.sample(torolt, a.n)
    for i, (f, irany, s) in enumerate(minta, 1):
        eles = olvas(os.path.join(ELES, f)).split('\n')
        proba = olvas(os.path.join(PROBA, f)).split('\n')
        sz = R.ProbaSzoveg(proba)
        ok = sz.tovabb_el(s)
        eles_sor = [j + 1 for j, x in enumerate(eles) if x == s]
        n = R._norm(s)
        talalat = [j for j, x in enumerate(proba) if n and n in R._norm(x)][:2]
        if not talalat:
            ige = R._IGEHELY_RE.findall(n)
            talalat = [j for j, x in enumerate(proba) if ige and ige[0] in R._norm(x)][:2]
        print('\n%d. %s  éles sor %s' % (i, f, eles_sor[:2]))
        print('   régi sor : %s' % s[:220])
        print('   tovább él: %s' % ok)
        for j in talalat:
            print('   próba %d : %s' % (j + 1, proba[j][:220]))


if __name__ == '__main__':
    main()
