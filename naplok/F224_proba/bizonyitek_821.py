#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bizonyitek_821.py -- F224.13: a HAMART 1Móz 8:21-es bíráló-próba bizonyítéklapja az F224.5 eszközével, a mérés
(2026-11-15) bizonyítéklapjának hatókörén: a lánc genezisi helyei (1Móz 3:14–12:3), a lánc hat szava + az
érvvázlatban megnevezett qalal (H7043); a versek állapota a javítás előtti (f6da955e) adat szerint.

Használat: python naplok/F224_proba/bizonyitek_821.py <elof_f6.tsv> <jeloltek_f6.tsv> <kimenet.md>
"""
import os
import sys

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ITT, '..', '..', 'eszkozok'))
import bizonyiteklap as B  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VERSEK = ['1Móz 3:14', '1Móz 3:17', '1Móz 4:11', '1Móz 5:29', '1Móz 6:5', '1Móz 6:11', '1Móz 6:12', '1Móz 6:13',
          '1Móz 8:21', '1Móz 9:11', '1Móz 12:3']
LANC = ['H0779', 'H0127', 'H6093', 'H2403', 'H2555', 'H7843', 'H7043']

if __name__ == '__main__':
    elof, jelolt, ki = sys.argv[1:4]
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write(B.keszit('HAMART-001', VERSEK, LANC, elof_ut=elof, jelolt_ut=jelolt))
    print('kész:', ki)
