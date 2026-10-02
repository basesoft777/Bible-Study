#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_cimkejavit.py -- F38.265 (DT-F38e): az 1-4. adag 243
sora (Sonnet-session) visszakerul az adat/forditasok.tsv-be a 20ef676
allapotabol (az F38.260 kivette oket), de helyes cimkevel:
allapot=sonnet, modell=claude-sonnet-5-5.

Minden `F38 BDB_FORDITAS` megjegyzesu sor cimkejet javitja; a #28 sorai
(es minden mas sor) bajtra valtozatlanok. Iras elott ellenorzi: a jelenlegi
tabla sorai a 20ef676-os tabla sorainak reszsorozata, a hianyzo sorok
pontosan az F38-as sorok. Elteresnel megall.

    python naplok/BDB_FORDITAS_cimkejavit.py          # csak jelentes
    python naplok/BDB_FORDITAS_cimkejavit.py --ir
"""

import argparse
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(REPO, 'adat', 'forditasok.tsv')
COMMIT = '20ef676'
JEL = 'F38 BDB_FORDITAS'
ALLAPOT_I, MODELL_I, MEGJ_I = 7, 8, 11
UJ_ALLAPOT, UJ_MODELL = 'sonnet', 'claude-sonnet-5-5'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    regi = subprocess.run(['git', 'show', '%s:adat/forditasok.tsv' % COMMIT], cwd=REPO,
                          capture_output=True, check=True).stdout.decode('utf-8')
    regi = regi.replace('\r\n', '\n').split('\n')
    if regi and regi[-1] == '':
        regi = regi[:-1]
    with open(UT, encoding='utf-8', newline='') as fh:
        most = fh.read().replace('\r\n', '\n').split('\n')
    if most and most[-1] == '':
        most = most[:-1]
    # a jelenlegi sorok a regi tabla reszsorozata
    j = 0
    for s in most:
        while j < len(regi) and regi[j] != s:
            j += 1
        if j == len(regi):
            raise SystemExit('a jelenlegi tabla egy sora nincs a %s-os tablaban: %s' % (COMMIT, s[:80]))
        j += 1
    ki = []
    f38 = 0
    for s in regi:
        m = s.split('\t')
        if not s.startswith('#') and len(m) == 12 and JEL in m[MEGJ_I]:
            if s in most:
                raise SystemExit('az F38-as sor mar benne van a jelenlegi tablaban: %s' % m[1])
            m[ALLAPOT_I] = UJ_ALLAPOT
            m[MODELL_I] = UJ_MODELL
            f38 += 1
            s = '\t'.join(m)
        elif s not in most:
            raise SystemExit('a nem F38-as sor hianyzik a jelenlegi tablabol: %s' % s[:80])
        ki.append(s)
    print('regi tabla: %d sor; jelenlegi: %d; visszakerul + cimkejavitva: %d F38-as sor; osszes: %d'
          % (len(regi), len(most), f38, len(ki)))
    if f38 != len(regi) - len(most):
        raise SystemExit('a hianyzo sorok szama (%d) nem egyezik az F38-as sorokeval (%d)'
                         % (len(regi) - len(most), f38))
    # a nem F38-as sorok bajtra azonosak
    nem = [s for s in ki if not any(JEL in x for x in [s.split('\t')[MEGJ_I] if len(s.split('\t')) == 12 else ''])]
    assert nem == [s for s in regi if s in set(most)], 'a nem F38-as sorok elterek'
    if args.ir:
        with open(UT, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(ki) + '\n')
        print('adat/forditasok.tsv irva')


if __name__ == '__main__':
    main()
