#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_regresszio.py -- F38, DT-F38c (e): a teljes kapusor
(forditas_kapuk.kapuk_futtat) az adat/forditasok.tsv minden BDB `teljes`
soran (a #28 kezi/opus sorai es az F38 sorai egyarant), a sor
terminologia-kiveteleivel. Csak olvas. A kimenet JSON (strong -> {kapu:
eredmeny}), hogy a kapujavitas elotti es utani allapot osszevetheto legyen.

    python naplok/BDB_FORDITAS_regresszio.py --ki elotte.json
    python naplok/BDB_FORDITAS_regresszio.py --ki utana.json --vesd elotte.json
"""

import argparse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'naplok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
from BDB_FORDITAS_ujranormalizal import kivetelek  # noqa: E402


def futtat():
    ki = {}
    for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
        if r['szotar'] != 'BDB' or r['jelentes_szam'] != 'teljes':
            continue
        _, forras = E.forras_szoveg(r['strong'])
        eredm = K.kapuk_futtat('BDB', forras, r['forditas_hu'], bizonytalan=kivetelek(r['megjegyzes']))
        ki[r['strong']] = {n: e for n, e, _ in eredm}
        ki[r['strong']]['_atment'] = K.atment(eredm)
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki', required=True)
    ap.add_argument('--vesd')
    args = ap.parse_args()
    ki = futtat()
    with open(args.ki, 'w', encoding='utf-8') as fh:
        json.dump(ki, fh, ensure_ascii=False, indent=0, sort_keys=True)
    bukott = sorted(s for s, v in ki.items() if not v['_atment'])
    print('szocikk: %d, bukott: %d %s' % (len(ki), len(bukott), ' '.join(bukott)))
    if args.vesd:
        with open(args.vesd, encoding='utf-8') as fh:
            regi = json.load(fh)
        uj_bukas = []
        valtozas = []
        for s, v in sorted(ki.items()):
            for n, e in v.items():
                r = regi.get(s, {}).get(n)
                if r != e:
                    valtozas.append('%s %s: %s -> %s' % (s, n, r, e))
                    if e == 'SERTES' and r != 'SERTES':
                        uj_bukas.append('%s %s' % (s, n))
        print('valtozott kapueredmeny: %d' % len(valtozas))
        for v in valtozas:
            print('  ' + v)
        print('UJ BUKAS: %d %s' % (len(uj_bukas), '; '.join(uj_bukas)))
        sys.exit(1 if uj_bukas else 0)


if __name__ == '__main__':
    main()
