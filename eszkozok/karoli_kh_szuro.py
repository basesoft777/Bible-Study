#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_szuro.py -- a Károli-KH fogyasztók közös szűrője (N-F156a, DT-F156q).

A `konkordancia/Karoli_kereszthivatkozasok.tsv` a forráshoz hű (nyers) tábla, de a forrásverseinek egy része másik vers
listáját hordozza; ezeket a `Karoli_kereszthivatkozasok_gyanus.tsv` sorolja fel. A fogyasztók ezen a modulon át kihagyják őket.
`gyanus_forrasok()`: a STEP-alakú forrásversek halmaza (pl. `Act.2.27`).
"""
import os

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GYANUS = os.path.join(GYOKER, 'konkordancia', 'Karoli_kereszthivatkozasok_gyanus.tsv')
_CACHE = None


def gyanus_forrasok():
    global _CACHE
    if _CACHE is None:
        ki = set()
        if os.path.exists(GYANUS):
            with open(GYANUS, encoding='utf-8') as f:
                for s in f:
                    if s.startswith('#') or s.startswith('forras\t'):
                        continue
                    m = s.rstrip('\n').rstrip('\r').split('\t')
                    if m and m[0]:
                        ki.add(m[0])
        _CACHE = ki
    return _CACHE
