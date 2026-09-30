#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P2 — az Opus-arany szúrópróbája olvasható formában.

Az f21p/arany_opus.jsonl-ből 10 verset választ (rétegenként 2–3, rögzített
maggal), és naplok/F21P_arany_szuroproba.md-be írja: magyar szó -> eredeti
szó, Strong, angol glossza. A Strong-számot a szkript veszi a TAHOT/TAGNT-ből,
nem a modell (vagy az arany) írja.

Használat: python eszkozok/karoli_strong/szuroproba.py
"""

import json
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

MAG = 20260930
GYOKER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ARANY = os.path.join(GYOKER, 'f21p', 'arany_opus.jsonl')
MINTA = os.path.join(GYOKER, 'f21p', 'minta.tsv')
KIMENET = os.path.join(GYOKER, 'naplok', 'F21P_arany_szuroproba.md')
DARAB = {'R1': 3, 'R2': 2, 'R3': 2, 'R4': 3}


def main():
    reteg = {}
    with open(MINTA, encoding='utf-8') as f:
        fej = f.readline().rstrip('\n').split('\t')
        ih, rt = fej.index('igehely'), fej.index('reteg')
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if len(m) > rt:
                reteg[m[ih]] = m[rt]
    arany = []
    with open(ARANY, encoding='utf-8') as f:
        for sor in f:
            if sor.strip():
                arany.append(json.loads(sor))
    rng = random.Random(MAG)
    valasztott = []
    for r, n in DARAB.items():
        jel = [a for a in arany if reteg.get(a['vers']) == r]
        valasztott += rng.sample(jel, min(n, len(jel)))
    karoli = tokenek.betolt_karoli()
    ered = tokenek.betolt_eredeti()
    sorok = ['# F21P arany — szúrópróba (10 vers)', '',
             'Jelezd a hibás linkeket (vers + magyar szó sorszáma). A Strong-szám a TAHOT/TAGNT-ből jön.', '']
    osszes = 0
    for a in valasztott:
        ih = a['vers']
        kt = tokenek.tokenizal(karoli[ih])
        et = {w['sorsz']: w for w in ered[ih]}
        sorok += [f'## {ih} ({reteg.get(ih)})', '', f'Károli: {karoli[ih]}', '',
                  '| # | magyar | -> | eredeti | Strong | glossza |', '|---|---|---|---|---|---|']
        for ksz, esz in a['parok']:
            for e in esz:
                w = et[e]
                sorok.append(f"| {ksz} | {kt[ksz - 1]} | -> | {w['alak']} (#{e}) | {w['strong']} | {w['tukor']} |")
                osszes += 1
        sorok += ['', f"betoldas: {a['betoldas']} · forditatlan: {a['forditatlan']}", '']
    sorok.append(f'Összes link a szúrópróbában: {osszes}')
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok) + '\n')
    print(f'{len(valasztott)} vers, {osszes} link -> {KIMENET}')


if __name__ == '__main__':
    main()
