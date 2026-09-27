#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
study_fajlok_szurese.py -- CI.2: a valtozott fajlok listajabol kivalasztja
azokat, amelyek tenylegesen study-fajlok (az `adat/motivumok.tsv`
`forras_study` oszlopaban szerepelnek). Ez kell az E1
(`eszkozok/ellenoriz.py --study FILE`) hivasahoz: ha egy nem-study fajlt
(pl. egy briefet vagy egy naplot) adnank at `--study`-nak, a Q7-ellenorzes
hamisan SÉRTÉS-t adna ("egyetlen motivumok.tsv sor forras_study-ja sem
tartalmazza ezt a fájlt"), es minden ilyen PR-t indokolatlanul buktatna.

CLI:
    python eszkozok/ellenorzes/study_fajlok_szurese.py < valtozott_fajlok.txt
    (soronkent egy relativ ut stdin-en; a study-fajlok kerulnek stdout-ra)
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import general as G


def study_fajlok_halmaza(adat_dir=None):
    adat_dir = adat_dir or os.path.join(ROOT, 'adat')
    _, motivumok = G.tsv_beolvas(os.path.join(adat_dir, 'motivumok.tsv'))
    halmaz = set()
    for m in motivumok:
        for f in (m.get('forras_study') or '').split(';'):
            f = f.strip()
            if f:
                halmaz.add(f)
    return halmaz


def main():
    valtozott = [sor.strip() for sor in sys.stdin if sor.strip()]
    study_halmaz = study_fajlok_halmaza()
    for f in valtozott:
        if f in study_halmaz:
            print(f)
    return 0


if __name__ == '__main__':
    sys.exit(main())
