#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDOKLAS_belso_meres.py -- az olvasói kapu BELSO-találatai laponként (F123.INDOKLAS, a 4. lépés előtte/utána mérése).

Kimenet soronként: lap, BELSO összesen (az `ell_belso` találatai, csoportosítás előtt), ebből a Strong-szám, és ebből
a `jeloltek.tsv`-ből jövő blokkok (1/b. és Minősítés) találatai. A mérce mindkét változaton a mai kapu (`olvasoi_kapu.py`).
Csak olvas.

    python naplok/INDOKLAS_belso_meres.py [--rev REV] [ID ...]     # --rev: a lap egy korábbi változata (git show)
"""
import glob
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import olvasoi_kapu as K  # noqa: E402


def lap_szoveg(mid, rev=None):
    rel = 'lexikon/%s_TUDOMANYOS.md' % mid
    if rev:
        return subprocess.run(['git', 'show', '%s:%s' % (rev, rel)], cwd=GYOKER, capture_output=True,
                              check=True).stdout.decode('utf-8')
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        return f.read()


def jelolt_blokk(s):
    return s.szakasz.startswith('1/b.') or s.alszakasz.startswith('Minősítés')


def meres(mid, rev=None):
    sorok = K.tagol(lap_szoveg(mid, rev).replace('\r', ''))
    sor = {s.n: s for s in sorok}
    talalat = [t for t in K.ell_belso(sorok) if t['azonosito'] == 'BELSO']
    strong = sum(1 for t in talalat if t['uzenet'].startswith('Strong-szám'))
    jelolt = sum(1 for t in talalat if t['sor'] in sor and jelolt_blokk(sor[t['sor']]))
    return len(talalat), strong, jelolt


def main():
    arg = sys.argv[1:]
    rev = None
    if arg[:1] == ['--rev']:
        rev, arg = arg[1], arg[2:]
    ids = arg or sorted(os.path.basename(p)[:-len('_TUDOMANYOS.md')]
                        for p in glob.glob(os.path.join(GYOKER, 'lexikon', '*_TUDOMANYOS.md')))
    print('lap\tBELSO\tebből Strong\tebből 1/b.+Minősítés')
    for mid in ids:
        print('%s\t%d\t%d\t%d' % ((mid,) + meres(mid, rev)))


if __name__ == '__main__':
    main()
