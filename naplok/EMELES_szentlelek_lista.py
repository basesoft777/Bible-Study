#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/EMELES_szentlelek_lista.py -- F28 DT25 (a): CSAK LISTAZ (nem javit),
hol all „Szentlélek” / „Isten Lelke” (es ragozott alakjaik) a kezzel irt
tanulmanyokban (tematikus_lezart/, genezis/, ujszovetseg/, melyelemzesek/,
motivumlog/) es a lexikonoldalak kezi szovegeben (lexikon/*.md, a
`GENERÁLT-KEZDET` ... `GENERÁLT-VÉGE` blokkokon kivul).

Kimenet: naplok/EMELES_szentlelek_lista.tsv (fajl, sor, alak, kornyezet).

    python naplok/EMELES_szentlelek_lista.py
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORRAS_DIROK = ['tematikus_lezart', 'genezis', 'ujszovetseg', 'melyelemzesek', 'motivumlog']
MINTA = re.compile(r'Szent ?[lL][ée]l\w*|Isten Lelk\w*')
KI = os.path.join(REPO, 'naplok', 'EMELES_szentlelek_lista.tsv')


def fajlok():
    for d in FORRAS_DIROK:
        for gy, _, nevek in os.walk(os.path.join(REPO, d)):
            for n in sorted(nevek):
                if n.endswith('.md'):
                    yield os.path.join(gy, n), False
    lex = os.path.join(REPO, 'lexikon')
    for n in sorted(os.listdir(lex)):
        if n.endswith('.md'):
            yield os.path.join(lex, n), True


def main():
    sorok = []
    for ut, csak_kezi in fajlok():
        generalt = False
        with open(ut, encoding='utf-8') as fh:
            for i, sor in enumerate(fh.read().split('\n'), 1):
                if 'GENERÁLT-KEZDET' in sor:
                    generalt = True
                if csak_kezi and generalt:
                    if 'GENERÁLT-VÉGE' in sor:
                        generalt = False
                    continue
                for m in MINTA.finditer(sor):
                    kornyezet = sor[max(0, m.start() - 40):m.end() + 40].replace('\t', ' ')
                    sorok.append((os.path.relpath(ut, REPO), str(i), m.group(0), kornyezet))
    with open(KI, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# F28 DT25 (a): Szentlélek / Isten Lelke elofordulasok -- csak lista, nem javitva\n')
        fh.write('fajl\tsor\talak\tkornyezet\n')
        for s in sorok:
            fh.write('\t'.join(s) + '\n')
    per_fajl = {}
    for f, _, a, _ in sorok:
        per_fajl[f] = per_fajl.get(f, 0) + 1
    print('osszesen %d elofordulas, %d fajlban' % (len(sorok), len(per_fajl)))
    for f in sorted(per_fajl):
        print('  %3d  %s' % (per_fajl[f], f))


if __name__ == '__main__':
    main()
