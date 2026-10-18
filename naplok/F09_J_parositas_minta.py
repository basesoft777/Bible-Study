#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F09_J_parositas_minta.py -- DT-F09g (3. javító menet): 15 párosított sor rögzített seeddel, a régi és az új
szöveg egymás mellett, a kulccsal és a kategóriával -> naplok/SZOTAR_S2_parositas_minta.md

    python naplok/F09_J_parositas_minta.py [--seed 20261017] [--n 15]
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


def cella(s):
    return '`' + s.strip().replace('|', '\\|').replace('`', "'")[:230] + '`'


def mezo_elteres(mod, regi, uj, kulcs):
    """A pár eltérő mezői (cellánkénti összevetés, 4. javító menet): `régi → új` rövidítve."""
    fajta = kulcs[0] if (mod == 'teljes kulcs' and isinstance(kulcs, tuple)) else None
    fa, fb = R._mezok(fajta, regi), R._mezok(fajta, uj)
    ki = []
    for i in range(max(len(fa), len(fb))):
        x = fa[i].strip() if i < len(fa) else '(nincs)'
        y = fb[i].strip() if i < len(fb) else '(nincs)'
        if x != y:
            ki.append('%d: %s → %s' % (i + 1, x[:60], y[:60]))
    return '; '.join(ki)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=20261017)
    ap.add_argument('--n', type=int, default=15)
    ap.add_argument('--ki', default=os.path.join(ROOT, 'naplok', 'SZOTAR_S2_parositas_minta.md'))
    a = ap.parse_args()
    minden = []
    for f in sorted(os.listdir(PROBA)):
        parok = []
        R.proba_osztalyoz(f, olvas(os.path.join(ELES, f)), olvas(os.path.join(PROBA, f)), parok)
        # csak az érdemi párok (a tartalom-azonos, csak fejléc-mélységűek nélkül)
        minden.extend((f,) + p for p in parok if p[1].strip() != p[2].strip())
    rnd = random.Random(a.seed)
    minta = rnd.sample(minden, a.n)
    sor = ['# SZOTAR S2 (#9) — párosítás szúrópróba (DT-F09g, 4. javító menet)', '',
           '*Mintavétel: `naplok/F09_J_parositas_minta.py` (seed %d, n=%d) a kizárólagos párosítás (`render_diff_osztalyoz.proba_osztalyoz`) '
           'összes párjából (%d pár, a csak fejléc-mélységűek nélkül). Proveniencia: scope=`generalt_proba/F09_szotar_s2_proba/lexikon` vs `lexikon/` '
           '| forras=`eszkozok/render_diff_osztalyoz.py` | ts=2026-10-17*' % (a.seed, a.n, len(minden)), '',
           '| # | Fájl | Párosítás | Kulcs | Régi (éles) | Új (próba) | Eltérő mezők | Kategória |', '|---|---|---|---|---|---|---|---|']
    for i, (f, mod, regi, uj, kulcs, kat) in enumerate(minta, 1):
        fn = f.replace('_TUDOMANYOS.md', ' (tud.)').replace('_TORZSCIKK.md', ' (törzs.)')
        sor.append('| %d | %s | %s | %s | %s | %s | %s | %s |' % (
            i, fn, mod, cella(kulcs if isinstance(kulcs, str) else repr(kulcs)), cella(regi), cella(uj),
            cella(mezo_elteres(mod, regi, uj, kulcs)), kat))
    with io.open(a.ki, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(sor) + '\n')
    print('%d pár, minta: %d' % (len(minden), len(minta)))


if __name__ == '__main__':
    main()
