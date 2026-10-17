#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F09_J_elavult_szuropr.py -- DT-F09g szúrópróba (3. javító menet): rétegzett minta rögzített seeddel az
`elavult_adat` soraiból: 10 TÖRÖLT + 5 HOZZÁADOTT + 5 az ATKULCSOLT_SOROK (F87.3-lábnyom) törölt sorai közül.
Horgony: PONTOS szövegegyezés (a normalizált sor teljes egyezése a másik oldalon) vagy a kizárólagos pár; igehely-egyezés
nem horgony. A kézi megítélés a naplok/SZOTAR_S2_elavult_szuropr.md-ben áll.

    python naplok/F09_J_elavult_szuropr.py [--seed 20261017]
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
    a = ap.parse_args()
    torolt, hozzaadott, atkulcsolt = [], [], []
    par_regi = {}   # (fájl, régi sor) -> (új sor, kulcs, mód)
    par_uj = {}     # (fájl, új sor) -> (régi sor, kulcs, mód)
    for f in sorted(os.listdir(PROBA)):
        parok = []
        e = R.proba_osztalyoz(f, olvas(os.path.join(ELES, f)), olvas(os.path.join(PROBA, f)), parok)
        for mod, regi, uj, kulcs, kat in parok:
            par_regi.setdefault((f, regi), (uj, kulcs, mod))
            par_uj.setdefault((f, uj), (regi, kulcs, mod))
        motiv = f.split('_')[0]
        for s in e.get('elavult_adat', {}).get('torolt', []):
            if (motiv, s.strip()) in R.ATKULCSOLT_SOROK:
                atkulcsolt.append((f, s))
            else:
                torolt.append((f, s))
        for s in e.get('elavult_adat', {}).get('hozzaadott', []):
            hozzaadott.append((f, s))
    print('elavult_adat: törölt (nem lábnyom) %d, hozzáadott %d, ATKULCSOLT-lábnyom törölt %d' % (len(torolt), len(hozzaadott), len(atkulcsolt)))
    rnd = random.Random(a.seed)
    minta = [('törölt',) + x for x in rnd.sample(torolt, min(10, len(torolt)))]
    minta += [('hozzáadott',) + x for x in rnd.sample(hozzaadott, min(5, len(hozzaadott)))]
    minta += [('ATKULCSOLT',) + x for x in rnd.sample(atkulcsolt, min(5, len(atkulcsolt)))]
    for i, (tip, f, s) in enumerate(minta, 1):
        oldal = olvas(os.path.join(PROBA if tip == 'törölt' or tip == 'ATKULCSOLT' else ELES, f)).split('\n')
        n = R._norm(s)
        pontos = [j + 1 for j, x in enumerate(oldal) if R._norm(x) == n]
        print('\n%d. [%s] %s' % (i, tip, f))
        print('   sor      : %s' % s.strip()[:230])
        if tip in ('törölt', 'ATKULCSOLT'):
            p = par_regi.get((f, s))
            print('   pár (új) : %s' % (('%s [%s, kulcs=%s]' % (p[0].strip()[:200], p[2], p[1])) if p else 'nincs kizárólagos pár'))
            print('   pontos egyezés a próbában: %s' % (pontos[:3] or 'nincs'))
        else:
            p = par_uj.get((f, s))
            print('   pár (régi): %s' % (('%s [%s, kulcs=%s]' % (p[0].strip()[:200], p[2], p[1])) if p else 'nincs kizárólagos pár'))
            print('   pontos egyezés az éles oldalon: %s' % (pontos[:3] or 'nincs'))


if __name__ == '__main__':
    main()
