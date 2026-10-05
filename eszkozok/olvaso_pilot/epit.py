"""Olvasói pilot (prototípus): az oldal összeállítása.

A --kimenet könyvtár olvaso_pilot.json-ját beágyazza a sablon.html-be, és ugyanoda írja a
karoli_konkordancia_proba.html-t (alapból a repón kívüli ideiglenes könyvtárba).
Futtatás: python eszkozok/olvaso_pilot/epit.py [--kimenet KÖNYVTÁR]"""
import argparse
import json
import os
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ap = argparse.ArgumentParser(description='Olvasói pilot: oldalépítés')
ap.add_argument('--kimenet', default=os.path.join(tempfile.gettempdir(), 'olvaso_pilot'))
args = ap.parse_args()
D = os.path.dirname(os.path.abspath(__file__))
adat = open(os.path.join(args.kimenet, 'olvaso_pilot.json'), encoding='utf-8').read().replace('</', '<\\/')
sablon = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
if sablon.count('__ADAT__') != 1:
    raise SystemExit('A sablonban pontosan egy __ADAT__ helyőrző kell.')
kesz = sablon.replace('__ADAT__', adat)
json.loads(kesz.split('id="adat">')[1].split('</script>')[0])
ki = os.path.join(args.kimenet, 'karoli_konkordancia_proba.html')
open(ki, 'w', encoding='utf-8').write(kesz)
print('kész:', ki, len(kesz.encode('utf-8')), 'bájt')
