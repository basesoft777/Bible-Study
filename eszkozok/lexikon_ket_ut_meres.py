#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lexikon_ket_ut_meres.py -- B4 (KEZI_FOLTOK felmérés): a lexikonlap kétféle
generálása bájtra egyezik-e.

A nulláról generált lap (`general.py --cel lexikon --id <ID> --kimenet <üres>`)
és a helyben frissített lap (ugyanez, a kimeneti könyvtárban már meglévő lappal:
a `--ir` útja) összevetése négy bemenetre: a friss kimenetre, a commitolt lapra,
és a commitolt lap CRLF-es munkapéldányára (a core.autocrlf=true checkout esete),
nyersen és LF-re normalizálva. A PARDES_DATUM a commitolt lap első GENERÁLT
jelölőjének ts= dátuma (mint az E28-ban). A repóba nem ír; minden kimenet
ideiglenes könyvtárba megy.

A CI-kapu az E28 (eszkozok/ellenorzes/szabalyok.py, `_e28_helyben_ag`): az csak
az e28_migralt_nezetek.tsv lapjain fut; ez a szkript mind a 9 lapot méri.

Futtatás: python eszkozok/lexikon_ket_ut_meres.py [ID ...]   (ID nélkül: mind)
Lapként négy generálás, kb. 6 perc.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = re.compile(r'GENERÁLT[^\n]*?\bts=(\d{4}-\d{2}-\d{2})')
CRLF, LF = b'\r\n', b'\n'


def lap_idk():
    return sorted(f[:-len('_TUDOMANYOS.md')] for f in os.listdir(os.path.join(ROOT, 'lexikon'))
                  if f.endswith('_TUDOMANYOS.md'))


def general(mid, datum, kimenet, bemenet=None):
    """A lap bájtjai; `bemenet` megadásakor az már a kimeneti könyvtárban áll (helyben frissítés)."""
    ut = os.path.join(kimenet, 'lexikon', mid + '_TUDOMANYOS.md')
    if bemenet is not None:
        os.makedirs(os.path.dirname(ut))
        with open(ut, 'wb') as f:
            f.write(bemenet)
    env = dict(os.environ, PARDES_DATUM=datum, PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, os.path.join(ROOT, 'eszkozok', 'general.py'), '--cel', 'lexikon',
                        '--id', mid, '--kimenet', kimenet], cwd=ROOT, env=env, capture_output=True)
    if p.returncode:
        raise RuntimeError('%s: a general.py %d kóddal állt le: %s'
                           % (mid, p.returncode, p.stderr.decode('utf-8', 'replace')[-400:]))
    with open(ut, 'rb') as f:
        return f.read()


def elso_elteres(a, b):
    a, b = a.decode('utf-8').split('\n'), b.decode('utf-8').split('\n')
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x != y:
            return '%d. sor: %r | %r (sorok: %d / %d)' % (i + 1, (x or '')[:90], (y or '')[:90], len(a), len(b))
    return None


def meres(mid):
    """[(címke, eltérés-szöveg vagy None)]."""
    commitolt = subprocess.run(['git', 'show', 'HEAD:lexikon/%s_TUDOMANYOS.md' % mid], cwd=ROOT,
                               capture_output=True, check=True).stdout
    datum = TS.search(commitolt.decode('utf-8')).group(1)
    tk = [tempfile.mkdtemp(prefix='ketut_') for _ in range(4)]
    try:
        friss = general(mid, datum, tk[0])
        helyben_friss = general(mid, datum, tk[1], friss)
        helyben_comm = general(mid, datum, tk[2], commitolt)
        helyben_crlf = general(mid, datum, tk[3], commitolt.replace(CRLF, LF).replace(LF, CRLF))
    finally:
        for t in tk:
            shutil.rmtree(t, ignore_errors=True)
    return datum, [
        ('nulláról == commitolt', elso_elteres(commitolt, friss)),
        ('helyben(nulláról) == nulláról', elso_elteres(friss, helyben_friss)),
        ('helyben(commitolt) == nulláról', elso_elteres(friss, helyben_comm)),
        ('helyben(CRLF) == nulláról', elso_elteres(friss, helyben_crlf)),
    ]


def main(argv):
    hibas = 0
    for mid in argv or lap_idk():
        datum, sorok = meres(mid)
        print('%s (PARDES_DATUM=%s)' % (mid, datum))
        for cimke, el in sorok:
            print('  %-32s %s' % (cimke, 'IGEN' if el is None else 'NEM — ' + el))
            # a nulláról == commitolt csak a migrált nézeten elvárás (E28); a két út egyezése mindenhol
            if el is not None and not cimke.startswith('nulláról'):
                hibas += 1
        sys.stdout.flush()
    print('a két út eltérése: %d' % hibas)
    return 1 if hibas else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
