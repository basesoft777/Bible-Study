#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F09_J_tiszta_klon_igazolas.py -- DT-F09h: a verziózott próba reprodukálhatósága tiszta klónon.

A gitignore-olt `konkordancia/_nyers/tbesh/TBESH_konszolidalt.tsv` fájlt ideiglenesen a repón kívülre (%TEMP%)
helyezi, a 8 motívum _TUDOMANYOS + _TORZSCIKK fájlját a repón kívüli ideiglenes könyvtárba generálja, bájtra
összeveti a verziózott `generalt_proba/F09_szotar_s2_proba/lexikon/` fájljaival, és a fájlt MINDENKÉPP visszateszi
(try/finally).

    python naplok/F09_J_tiszta_klon_igazolas.py
"""

import filecmp
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONSZ = os.path.join(ROOT, 'konkordancia', '_nyers', 'tbesh', 'TBESH_konszolidalt.tsv')
PROBA = os.path.join(ROOT, 'generalt_proba', 'F09_szotar_s2_proba', 'lexikon')
IDK = ['ALVIL-001', 'ANTROP-001', 'HAMART-001', 'HODIT-001', 'ISTENTISZT-001', 'KIRALY-001', 'MENNY-001', 'TEREMT-001']


def sha(ut):
    with open(ut, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    tmp = tempfile.mkdtemp(prefix='f09_tiszta_klon_')
    parkolo = os.path.join(tmp, 'TBESH_konszolidalt.tsv.parkolo')
    kimenet = os.path.join(tmp, 'kimenet')
    athelyezve = False
    try:
        if os.path.isfile(KONSZ):
            shutil.move(KONSZ, parkolo)
            athelyezve = True
        print('konszolidált tábla a helyén: %s (a fájl %s)' % (os.path.isfile(KONSZ), 'ideiglenesen elmozgatva' if athelyezve else 'eleve nem volt meg'))
        env = dict(os.environ, PARDES_DATUM='2026-10-17', PYTHONIOENCODING='utf-8')
        for mid in IDK:
            for cel in ('lexikon', 'torzscikk'):
                r = subprocess.run([sys.executable, os.path.join(ROOT, 'eszkozok', 'general.py'), '--cel', cel, '--id', mid,
                                    '--kimenet', kimenet], cwd=ROOT, env=env, capture_output=True)
                if r.returncode != 0:
                    print('HIBA: %s %s: %s' % (mid, cel, r.stderr.decode('utf-8', 'replace')[-400:]))
                    return 1
    finally:
        if athelyezve:
            shutil.move(parkolo, KONSZ)
        print('konszolidált tábla visszatéve: %s' % (os.path.isfile(KONSZ) or not athelyezve))
    gen = os.path.join(kimenet, 'lexikon')
    egyezik, elter = 0, []
    for f in sorted(os.listdir(PROBA)):
        a, b = os.path.join(PROBA, f), os.path.join(gen, f)
        if os.path.isfile(b) and filecmp.cmp(a, b, shallow=False):
            egyezik += 1
        else:
            elter.append(f)
    print('bájtra egyező fájl: %d / %d; eltérő: %s' % (egyezik, len(os.listdir(PROBA)), elter or 'nincs'))
    print('proveniencia: scope=generalt_proba/F09_szotar_s2_proba/lexikon (16 fájl) vs repón kívüli ideiglenes kimenet '
          '| forras=naplok/F09_J_tiszta_klon_igazolas.py (general.py --cel lexikon|torzscikk, PARDES_DATUM=2026-10-17, '
          'a konszolidált tábla nélkül) | ts=2026-10-17')
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if not elter else 2


if __name__ == '__main__':
    sys.exit(main())
