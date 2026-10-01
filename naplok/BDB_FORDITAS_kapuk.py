#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_kapuk.py -- F38: a teljes kapusor (forditas_kapuk.kapuk_futtat)
az adat/forditasok.tsv F38-as `opus` soraira (megjegyzes: "F38 BDB_FORDITAS"),
a sor terminologia-kiveteleivel. Csak olvas.

    python naplok/BDB_FORDITAS_kapuk.py [--adag 2]
"""

import argparse
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--adag', type=int)
    args = ap.parse_args()
    bukott = jelzes = n = 0
    for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
        if r['allapot'] != 'opus' or 'F38 BDB_FORDITAS' not in r['megjegyzes']:
            continue
        if args.adag and '(adag %d)' % args.adag not in r['megjegyzes']:
            continue
        n += 1
        _, forras = E.forras_szoveg(r['strong'])
        eredm = K.kapuk_futtat(r['szotar'], forras, r['forditas_hu'], bizonytalan=kivetelek(r['megjegyzes']))
        ok = K.atment(eredm)
        bukott += not ok
        nem_rendben = [(nn, e, d) for nn, e, d in eredm if e != 'RENDBEN' and not nn.startswith('6')]
        jelzes += any(e == 'JELZES' for _, e, _ in nem_rendben)
        print('%s %s%s' % (r['strong'], 'ATMENT' if ok else 'BUKOTT',
                           ''.join('\n    %-22s %-8s %s' % (nn, e, d[:200]) for nn, e, d in nem_rendben)))
    print('szocikk: %d, bukott: %d, jelzes: %d' % (n, bukott, jelzes))


if __name__ == '__main__':
    main()
