"""Olvasói pilot: az oldal összeállítása.

A --kimenet könyvtár olvaso_pilot.json-ját beágyazza a sablon.html-be, és ugyanoda írja a
karoli_konkordancia_proba.html-t (alapból a repón kívüli ideiglenes könyvtárba, szakaszonként külön).
Alapból gzip + base64 alakban ágyaz be (a böngésző DecompressionStream-mel bontja ki): az 1Móz 1–25 JSON-ja
tízmegás nagyságrendű, tömörítve töredéke. A --nyers a JSON-t változatlanul ágyazza be (hibakereséshez).
Futtatás: python eszkozok/olvaso_pilot/epit.py [--szakasz "Zsolt 22"] [--kimenet KÖNYVTÁR] [--nyers]
(ugyanazzal a --szakasz és --kimenet értékkel, mint az adat.py-nál)"""
import argparse
import base64
import gzip
import html
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from szakasz import alap_kimenet, szakasz_cim  # noqa: E402

ap = argparse.ArgumentParser(description='Olvasói pilot: oldalépítés')
ap.add_argument('--szakasz', default='1Móz 1:1-2:3')
ap.add_argument('--kimenet', default=None)
ap.add_argument('--nyers', action='store_true', help='a JSON beágyazása tömörítés nélkül')
args = ap.parse_args()
kimenet = args.kimenet or alap_kimenet(args.szakasz)
nyers = open(os.path.join(kimenet, 'olvaso_pilot.json'), encoding='utf-8').read()
json.loads(nyers)
sablon = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
if sablon.count('__ADAT__') != 1 or sablon.count('__ADATATTR__') != 1:
    raise SystemExit('A sablonban pontosan egy __ADAT__ és egy __ADATATTR__ helyőrző kell.')
if args.nyers:
    adat, attr = nyers.replace('</', '<\\/'), ''
else:
    adat = base64.b64encode(gzip.compress(nyers.encode('utf-8'), 9, mtime=0)).decode('ascii')
    attr = ' data-kodolas="gzip-base64"'
kesz = sablon.replace('__SZAKASZ__', html.escape(szakasz_cim(args.szakasz))).replace('__ADATATTR__', attr).replace('__ADAT__', adat)
ki = os.path.join(kimenet, 'karoli_konkordancia_proba.html')
with open(ki, 'w', encoding='utf-8') as fh:
    fh.write(kesz)
print('kész:', ki, len(kesz.encode('utf-8')), 'bájt (JSON:', len(nyers.encode('utf-8')), 'bájt,', 'nyers' if args.nyers else 'gzip+base64', ')')
