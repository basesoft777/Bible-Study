#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
foglalas_takarit.py -- F201: a feladatszam-foglalasok (origin `foglalas/F<nn>` agak, l.
`feladatok.py kovetkezo_szam --foglal`) torlese, ha a szamnak mar van briefje a main-en.
A main-en futo gepi Action hivja a gepi commit utan; a torles az App-token jogosultsagaval megy.

    python eszkozok/foglalas_takarit.py            # torol (push --delete)
    python eszkozok/foglalas_takarit.py --szaraz   # csak kiirja
"""

import argparse
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELOTAG = 'foglalas/F'
BRIEF = re.compile(r'^F(\d{2,})_')


def _git(gyoker, *args):
    p = subprocess.run(['git'] + list(args), cwd=gyoker, capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def teljesult(gyoker, remote='origin', foag='main'):
    """A foglalasok szamai, amelyeknek a foagon mar van `F<nn>_*` fajlja."""
    _git(gyoker, 'fetch', '--quiet', '--prune', remote)
    _, ki, _ = _git(gyoker, 'for-each-ref', '--format=%(refname)', 'refs/remotes/%s/%s*' % (remote, ELOTAG))
    talalatok = (re.search(r'/foglalas/F(\d+)$', r.strip()) for r in ki.split('\n') if r.strip())
    foglalt = sorted(int(m.group(1)) for m in talalatok if m)
    _, fajlok, _ = _git(gyoker, 'ls-tree', '--name-only', '%s/%s' % (remote, foag))
    van = {int(m.group(1)) for m in (BRIEF.match(f.strip()) for f in fajlok.split('\n')) if m}
    return [n for n in foglalt if n in van]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--szaraz', action='store_true')
    ap.add_argument('--gyoker', default=ROOT)
    a = ap.parse_args()
    lista = teljesult(a.gyoker)
    if not lista:
        print('Nincs torlendo foglalas.')
        return 0
    for n in lista:
        print('%s foglalas: F%d (van briefje a main-en)' % ('Torolne' if a.szaraz else 'Torli', n))
        if not a.szaraz:
            rc, _, hiba = _git(a.gyoker, 'push', '--quiet', 'origin', '--delete', 'refs/heads/%s%d' % (ELOTAG, n))
            if rc != 0:
                print('FIGYELMEZTETES: a torles nem sikerult: %s' % hiba.strip(), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
