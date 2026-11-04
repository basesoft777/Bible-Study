#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDOKLAS_dt569_igazolas.py -- a kiadott lapokon csak generált rész változott-e (DT569; F123.INDOKLAS 4. lépés).

A lap egy korábbi változatát (`--rev`, alapból origin/main) és a mai fájlt soronként összeveti (difflib); minden
megváltozott sor a régi és az új oldalon is generált részben kell álljon (GENERÁLT-KEZDET…VÉGE, GENERÁLT-RÉS … a rés
proveniencia-soráig; a mérce a `kiejtes_szoveg._sor_reszek`, ugyanaz, amellyel a generátor a kézi részt kíméli).
A kézi részben álló változást kiírja; kilépési kód 1, ha van ilyen. Csak olvas.

    python naplok/INDOKLAS_dt569_igazolas.py [--rev REV] [ID ...]    # alapból: ISTENTISZT-001 ALVIL-001 ANTROP-001
"""
import difflib
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import kiejtes_szoveg as KSZ  # noqa: E402

KIADOTT = ['ISTENTISZT-001', 'ALVIL-001', 'ANTROP-001']


def szoveg(mid, rev=None):
    rel = 'lexikon/%s_TUDOMANYOS.md' % mid
    if rev:
        t = subprocess.run(['git', 'show', '%s:%s' % (rev, rel)], cwd=GYOKER, capture_output=True,
                           check=True).stdout.decode('utf-8')
    else:
        with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
            t = f.read()
    return t.replace('\r', '').split('\n')


def igazol(mid, rev):
    regi, uj = szoveg(mid, rev), szoveg(mid)
    rr, ur = KSZ._sor_reszek(regi), KSZ._sor_reszek(uj)
    valtozott, kezi = 0, []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, regi, uj, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        valtozott += max(i2 - i1, j2 - j1)
        for i in range(i1, i2):
            if not rr[i][0]:
                kezi.append(('régi', i + 1, rr[i][2], regi[i]))
        for j in range(j1, j2):
            if not ur[j][0]:
                kezi.append(('új', j + 1, ur[j][2], uj[j]))
    return valtozott, kezi


def main():
    arg = sys.argv[1:]
    rev = 'origin/main'
    if arg[:1] == ['--rev']:
        rev, arg = arg[1], arg[2:]
    hiba = 0
    print('lap\tmegváltozott sor\tebből kézi részben')
    for mid in arg or KIADOTT:
        n, kezi = igazol(mid, rev)
        print('%s\t%d\t%d' % (mid, n, len(kezi)))
        for oldal, sor, szakasz, t in kezi:
            print('   %s %d. sor [%s]: %s' % (oldal, sor, szakasz[:40], t[:160]))
        hiba |= bool(kezi)
    return 1 if hiba else 0


if __name__ == '__main__':
    sys.exit(main())
