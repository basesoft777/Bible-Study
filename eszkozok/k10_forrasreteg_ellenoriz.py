#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
k10_forrasreteg_ellenoriz.py -- F4 K10: a G2 fuggetlen ellenorzese.

"A G2 utan a het motivumok/[ID].md egyuttes tartalma BAJTRA lefedi a naplobol
kivett blokkokat" (F4_GENERATOR_BRIEF.md 3. pont, K10).

Meres: a naplo git-beli kiindulo verzioja (alapertelmezesben a G2 commitjat
megelozo allapot) es a mai munkapeldany SORONKENTI kulonbsege. Minden sor,
amely a kiindulo verzioban benne volt, a maiban viszont nincs, meg kell
jelenjen valamelyik motivumok/*.md fajlban -- karakterre azonosan. Egyetlen
elveszett sor is 1-es kilepesi kodot ad.

Futtatas a repo gyokerebol:
    python eszkozok/k10_forrasreteg_ellenoriz.py [git-ref]
"""

import io
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLO_REL = 'motivumlog/PaRDeS_motivumok.md'
MOTIVUMOK_DIR = os.path.join(ROOT, 'motivumok')


def git_szoveg(ref, rel_ut):
    ki = subprocess.run(['git', 'show', '%s:%s' % (ref, rel_ut)],
                        cwd=ROOT, capture_output=True)
    if ki.returncode != 0:
        raise SystemExit('MEGALLAS: git show %s:%s sikertelen.' % (ref, rel_ut))
    return ki.stdout.decode('utf-8').replace('\r\n', '\n')


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
    regi = git_szoveg(ref, NAPLO_REL)
    with io.open(os.path.join(ROOT, NAPLO_REL), encoding='utf-8') as f:
        uj = f.read().replace('\r\n', '\n')

    forrasreteg = {}
    for fajl in sorted(os.listdir(MOTIVUMOK_DIR)):
        if not fajl.endswith('.md'):
            continue
        with io.open(os.path.join(MOTIVUMOK_DIR, fajl), encoding='utf-8') as f:
            forrasreteg[fajl] = f.read().replace('\r\n', '\n')
    print('Forrásréteg: %d fájl (%s)' % (len(forrasreteg), ', '.join(forrasreteg)))

    regi_sorok = [s for s in regi.split('\n') if s.strip()]
    uj_sorok = set(s for s in uj.split('\n') if s.strip())

    eltunt = [s for s in regi_sorok if s not in uj_sorok]
    print('A naplóból eltűnt, nem üres sorok (%s -> munkapéldány): %d' % (ref, len(eltunt)))

    fedetlen = []
    fedes = {}
    for sor in eltunt:
        hol = [f for f, t in forrasreteg.items() if sor in t]
        if not hol:
            fedetlen.append(sor)
        else:
            fedes[hol[0]] = fedes.get(hol[0], 0) + 1

    for fajl in sorted(fedes):
        print('  %-22s %d sor' % (fajl, fedes[fajl]))

    if fedetlen:
        print('\nFEDETLEN SOROK (%d) -- ezek sem a naplóban, sem a forrásrétegben '
              'nincsenek meg:' % len(fedetlen), file=sys.stderr)
        for s in fedetlen[:20]:
            print('  %s' % s[:150], file=sys.stderr)
        return 1

    print('\nK10 ✓ — mind a %d eltűnt sor karakterre megvan a forrásrétegben.'
          % len(eltunt))
    return 0


if __name__ == '__main__':
    sys.exit(main())
