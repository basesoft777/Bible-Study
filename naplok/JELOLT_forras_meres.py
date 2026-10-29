"""Az 1/b. blokk („Kizárt és vizsgált helyek”) új formájához: a `jeloltek.tsv` elutasított / nyitva maradt sorainak
`forras_kereses` és `indoklas` mintái, motívumonként (ISTENTISZT-001 arany lap, 2026-10-29). Csak olvas.

A `forras_kereses` értékeit normalizálva (számok → 9, igehelyek → <hely>, a `|`-utáni proveniencia levágva) csoportosítja,
gyakoriság szerint; az `indoklas` első 6 szavát is. split('\\t').

  python naplok/JELOLT_forras_meres.py [--id ISTENTISZT-001] [--indoklas]
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELY = re.compile(r'\b(?:[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6}) \d+:\d+(?:-\d+)?')

ap = argparse.ArgumentParser()
ap.add_argument('--id')
ap.add_argument('--indoklas', action='store_true')
a = ap.parse_args()

with open(os.path.join(GYOKER, 'adat', 'jeloltek.tsv'), encoding='utf-8', newline='') as f:
    s = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
fej = s[0].split('\t')
sorok = [dict(zip(fej, x.split('\t'))) for x in s[1:]]
sorok = [r for r in sorok if r.get('dontes') in ('elutasítva', 'nyitva') and (not a.id or r['id'] == a.id)]
print('sor:', len(sorok), '| motívum:', dict(collections.Counter(r['id'] for r in sorok)))
minta = collections.Counter()
pelda = {}
for r in sorok:
    fk = (r.get('forras_kereses') or '').split(' | ')[0]
    k = re.sub(r'\d+', '9', HELY.sub('<hely>', fk))
    minta[k] += 1
    pelda.setdefault(k, fk)
print('\n== forras_kereses minták ==')
for k, n in minta.most_common():
    print('%4d  %-70.70s  pl.: %.80s' % (n, k, pelda[k]))
if a.indoklas:
    print('\n== indoklás eleje ==')
    c = collections.Counter(' '.join((r.get('indoklas') or '').split()[:6]) for r in sorok)
    for k, n in c.most_common(60):
        print('%4d  %s' % (n, k))
