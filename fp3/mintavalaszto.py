#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp3/mintavalaszto.py -- F27_FP3_BRIEF.md P1: 40 szocikkes minta.
Az fp2/minta.tsv 30 szocikke valtozatlanul + 10 uj hosszu (> 2000 kar.),
seed = 20260930, az fp2 minta (a kor2 szocikkeit is tartalmazza) kizarasaval.

Kimenet: fp3/minta.tsv (az fp2/minta.tsv oszlopai + forras: fp2 / uj)

    python fp3/mintavalaszto.py
"""

import hashlib
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
FP2_MINTA_UT = os.path.join(REPO, 'fp2', 'minta.tsv')
KIMENET_UT = os.path.join(REPO, 'fp3', 'minta.tsv')
SEED = 20260930
UJ_HOSSZU = 10


def tsv_dict_sorok(ut):
    fejlec = None
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if not sor:
                continue
            m = sor.split('\t')
            if fejlec is None:
                fejlec = m
                continue
            yield dict(zip(fejlec, m))


def main():
    thayer = {r['Strong_padded']: r['Teljes_szocikk'] for r in tsv_dict_sorok(THAYER_UT)}
    fp2 = list(tsv_dict_sorok(FP2_MINTA_UT))
    kizart = {r['strong'] for r in fp2}

    # ellenorzes: az fp2 minta hash-ei egyeznek a mostani forrassal
    for r in fp2:
        assert hashlib.sha1(thayer[r['strong']].encode('utf-8')).hexdigest() == r['forras_hash'], r['strong']

    jeloltek = sorted(s for s, t in thayer.items() if s not in kizart and len(t) > 2000)
    random.Random(SEED).shuffle(jeloltek)
    uj = sorted(jeloltek[:UJ_HOSSZU])

    fejlec = ['strong', 'csoport', 'hossz_kategoria', 'sulyos', 'hossz', 'forras_hash', 'forras']
    sorok = [dict(r, forras='fp2') for r in fp2]
    for s in uj:
        t = thayer[s]
        sorok.append({'strong': s, 'csoport': 'fp3', 'hossz_kategoria': 'hosszu', 'sulyos': 'nem',
                      'hossz': len(t), 'forras_hash': hashlib.sha1(t.encode('utf-8')).hexdigest(),
                      'forras': 'uj'})
    assert len({r['strong'] for r in sorok}) == 40
    with open(KIMENET_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(fejlec) + '\n')
        for r in sorok:
            fh.write('\t'.join(str(r[m]) for m in fejlec) + '\n')

    # a teljes Thayer ujramerese (hossz-kategoriankent: db / karakter)
    kat = {'rovid': [0, 0], 'kozepes': [0, 0], 'hosszu': [0, 0]}
    for t in thayer.values():
        h = len(t)
        k = 'rovid' if h <= 300 else ('kozepes' if h <= 2000 else 'hosszu')
        kat[k][0] += 1
        kat[k][1] += h
    print('teljes Thayer ujramerve:', kat, 'osszesen', sum(v[0] for v in kat.values()),
          sum(v[1] for v in kat.values()))
    from collections import Counter
    print('minta:', Counter(r['hossz_kategoria'] for r in sorok))
    print('uj hosszu:', [(s, len(thayer[s])) for s in uj])
    print('irva: %s' % KIMENET_UT)


if __name__ == '__main__':
    main()
