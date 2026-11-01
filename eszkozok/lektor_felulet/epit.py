#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epit.py -- F157: a lektor-felület artifact-oldala a `naplok/LEKTOR_*.tsv` kérdéseiből és a `sablon.html`-ből.

A kimenet az Artifact-eszköznek szánt oldal (a váz nélkül). A TSV-ből csak a kérdés-mezők és a repóban már rögzített döntés
(`valasz`, `allapot`) kerülnek be -- a felhasználó artifact-beli válaszai SOHA (az adatbázisban élnek, nem az oldalban).

    python eszkozok/lektor_felulet/epit.py <kimenet.html> [--motivum ID ...] [--lap-url URL]
"""
import argparse
import glob
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HELY))
sys.path.insert(0, os.path.dirname(HELY))
import lektor_kerdesek as L  # noqa: E402

BE_MEZOK = ['kerdes_id', 'forras', 'motivum', 'hely', 'kerdes', 'valaszlehetosegek', 'allapot', 'valasz']


def kerdesek(motivumok=None, root=ROOT):
    ki = []
    for ut in sorted(glob.glob(os.path.join(root, 'naplok', 'LEKTOR_*.tsv'))):
        m = os.path.basename(ut)[len('LEKTOR_'):-len('.tsv')]
        if motivumok and m not in motivumok:
            continue
        for r in L.beolvas(ut).values():
            ki.append({k: r[k] for k in BE_MEZOK})
    return ki


def epit(motivumok=None, lap_url='', root=ROOT):
    with open(os.path.join(HELY, 'sablon.html'), encoding='utf-8') as f:
        sablon = f.read()
    adat = json.dumps(kerdesek(motivumok, root), ensure_ascii=False).replace('</', '<\\/')
    url = json.dumps(lap_url, ensure_ascii=False).replace('</', '<\\/')
    if sablon.count('__ADAT__') != 1 or sablon.count('__LAP_URL__') != 1:
        raise ValueError('a sablon helyőrzői hiányoznak vagy ismétlődnek')
    return sablon.replace('__ADAT__', adat).replace('__LAP_URL__', url)


def main():
    ap = argparse.ArgumentParser(description='F157 -- lektor-felület építése')
    ap.add_argument('kimenet')
    ap.add_argument('--motivum', nargs='*', default=None)
    ap.add_argument('--lap-url', default='')
    a = ap.parse_args()
    szoveg = epit(a.motivum, a.lap_url)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('  %s: %d kérdés' % (a.kimenet, len(kerdesek(a.motivum))), file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
