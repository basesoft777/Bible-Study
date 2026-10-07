"""Olvasói pilot: az oldal összeállítása.

A --kimenet könyvtár olvaso_pilot.json-ját beágyazza a sablon.html-be, és ugyanoda írja a
karoli_konkordancia_proba.html-t (alapból a repón kívüli ideiglenes könyvtárba, szakaszonként külön).
Futtatás: python eszkozok/olvaso_pilot/epit.py [--szakasz "Zsolt 22"] [--kimenet KÖNYVTÁR]
(ugyanazzal a --szakasz és --kimenet értékkel, mint az adat.py-nál)"""
import argparse
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
args = ap.parse_args()
kimenet = args.kimenet or alap_kimenet(args.szakasz)
adat = open(os.path.join(kimenet, 'olvaso_pilot.json'), encoding='utf-8').read().replace('</', '<\\/')
sablon = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
if sablon.count('__ADAT__') != 1:
    raise SystemExit('A sablonban pontosan egy __ADAT__ helyőrző kell.')
kesz = sablon.replace('__SZAKASZ__', html.escape(szakasz_cim(args.szakasz))).replace('__ADAT__', adat)
json.loads(kesz.split('id="adat">')[1].split('</script>')[0])
ki = os.path.join(kimenet, 'karoli_konkordancia_proba.html')
open(ki, 'w', encoding='utf-8').write(kesz)
print('kész:', ki, len(kesz.encode('utf-8')), 'bájt')
