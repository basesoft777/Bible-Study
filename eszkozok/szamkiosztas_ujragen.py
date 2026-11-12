#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
szamkiosztas_ujragen.py -- F201: a szamkiosztas utan a szamtol fuggo generalt nezetek
ujragenerálasa, UGYANABBAN a commitban (E28/E35 ne pirosodjon be).

Miert: a `szamkiosztas.py` a DT-F/N-F helyorzot veglegesre cserelte az adatban es a
dokumentumokban, de a generalt nezet (a lexikonlap „a dontes nyoma”, a datum-feloldas a
DONTESEK.md-bol; a nyilt mag dontesnaplója) a regi alakot hordozta -> az E28/E35 a
main-en pirosra valt (2026-11-11: #673/#674, majd #693 utan). Itt a lap NEM kerul ki
a valtozo szambol, mert a feloldott datum is a szamtol fugg: az igaz megoldas az
ujragenerálas (DT-F201a).

Lepesek (mind a szabalyos generatorral, kezi szerkesztes nelkul):
  1. a marker-blokkos celok (naplo, index, nyitott): general.py --cel X --ir
  2. minden migralt nezet (eszkozok/ellenorzes/e28_migralt_nezetek.tsv):
     PARDES_DATUM=<a lap GENERÁLT jelolojenek ts= datuma> general.py --cel C --id ID --ir
     (ugyanaz a datum, amit az E28 hasznal, igy a lap datuma nem csuszik)
  3. a nyilt mag: nyilt_mag_export.py

Idempotens: ha a szamkiosztas nem valtoztatott semmit, a generator bajtra ugyanazt adja,
nincs diff. A hiba nem csendes: nem nulla kilepesi kodot ad (a workflow megall, nem commitol).

CLI:
    python eszkozok/szamkiosztas_ujragen.py            # ir
    python eszkozok/szamkiosztas_ujragen.py --lista    # csak kiirja a lepeseket
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
LISTA = os.path.join(ROOT, 'eszkozok', 'ellenorzes', 'e28_migralt_nezetek.tsv')
MARKER_CELOK = ('naplo', 'index', 'nyitott')
_TS = re.compile(r'GENERÁLT[^\n]*?\bts=(\d{4}-\d{2}-\d{2})')


def migralt_nezetek(gyoker=ROOT):
    """[(id, fajl, cel)] a lista sorai. A TSV olvasasa split('\\t')."""
    ut = os.path.join(gyoker, 'eszkozok', 'ellenorzes', 'e28_migralt_nezetek.tsv')
    if not os.path.exists(ut):
        return []
    with open(ut, 'rb') as f:
        sorok = f.read().decode('utf-8').split('\n')
    fej = sorok[0].rstrip('\r').split('\t')
    ki = []
    for s in sorok[1:]:
        s = s.rstrip('\r')
        if not s.strip():
            continue
        d = dict(zip(fej, s.split('\t')))
        if d.get('fajl', '').strip():
            ki.append((d.get('id', '').strip(), d['fajl'].strip(), d.get('cel', '').strip()))
    return ki


def lap_datuma(gyoker, relut):
    """A lap GENERÁLT jelolojenek ts= datuma (az E28 ugyanezt hasznalja) vagy None."""
    ut = os.path.join(gyoker, *relut.split('/'))
    with open(ut, 'rb') as f:
        m = _TS.search(f.read().decode('utf-8'))
    return m.group(1) if m else None


def lepesek(gyoker=ROOT):
    """[(leiras, parancs, env_kiegeszites)] -- a futtatando lepesek sorban."""
    py = sys.executable
    gen = os.path.join(gyoker, 'eszkozok', 'general.py')
    ki = []
    for cel in MARKER_CELOK:
        ki.append(('marker-blokk: %s' % cel, [py, gen, '--cel', cel, '--ir'], {}))
    for azon, relut, cel in migralt_nezetek(gyoker):
        datum = lap_datuma(gyoker, relut)
        if not datum:
            raise SystemExit('HIBA: %s: nincs GENERÁLT jelölő ts= dátummal, a PARDES_DATUM nem '
                             'állapítható meg (kézi fájl nem lehet a migrált listán)' % relut)
        ki.append(('migrált nézet: %s' % relut,
                   [py, gen, '--cel', cel, '--id', azon, '--ir'],
                   {'PARDES_DATUM': datum}))
    ki.append(('nyílt mag', [py, os.path.join(gyoker, 'eszkozok', 'nyilt_mag_export.py')], {}))
    return ki


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--lista', action='store_true', help='csak kiirja a lepeseket')
    ap.add_argument('--gyoker', default=ROOT)
    a = ap.parse_args()
    for leiras, parancs, env in lepesek(a.gyoker):
        print('- %s%s' % (leiras, ' (PARDES_DATUM=%s)' % env['PARDES_DATUM'] if env else ''))
        if a.lista:
            continue
        p = subprocess.run(parancs, cwd=a.gyoker, env=dict(os.environ, PYTHONIOENCODING='utf-8', **env),
                           capture_output=True)
        if p.returncode != 0:
            sys.stderr.write(p.stdout.decode('utf-8', errors='replace')[-1500:])
            sys.stderr.write(p.stderr.decode('utf-8', errors='replace')[-1500:])
            print('HIBA: %s nem futott le (kilépési kód %d)' % (leiras, p.returncode), file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
