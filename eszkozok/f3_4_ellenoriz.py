# -*- coding: utf-8 -*-
"""F3.4 dontes-tabla ellenorzese — betoltes elott es utan egyarant futtathato.

Ket dolgot nez:
  (1) a dontes-tabla pontosan azokat a sorokat fedi-e, amelyeknek fednie kell —
      betoltes elott az ures karoli_szo-jueket, betoltes utan azokat, amelyek
      a dontes-tabla ertekét viselik;
  (2) a megadott karoli_szo tenylegesen szerepel-e a hivatkozott Karoli-versben,
      a ket ismert vers-eltolodast (Job 17, Pred 9) figyelembe veve.
"""
import csv
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSSZU = {'Jelenések': 'Jel', 'Lukács': 'Luk', 'Máté': 'Mt', 'Róma': 'Róm'}
# a Karoli_1908.tsv ismert vers-eltolodasai, l. konkordancia/Karoli_adatminosegi_anomaliak.tsv
ELTOLAS = {'Jób 17:16': 'Jób 17:15', 'Préd 9:10': 'Préd 9:12'}

karoli = {}
with open(os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
    r = csv.reader(f, delimiter='\t')
    next(r)
    for s in r:
        if len(s) >= 2:
            karoli[s[0]] = s[1]

with open(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'), encoding='utf-8') as f:
    sorok = [s.rstrip('\n') for s in f][1:]
fejlec = sorok[0].split('\t')
elo = [dict(zip(fejlec, s.split('\t'))) for s in sorok[1:] if s.strip()]

with open(os.path.join(ROOT, 'eszkozok', 'f3_4_dontesek.tsv'), encoding='utf-8') as f:
    dont = list(csv.DictReader(f, delimiter='\t'))
dkulcs = [(d['id'], d['igehely']) for d in dont]
dmap = {k: d for k, d in zip(dkulcs, dont)}

hibak = []
if len(dkulcs) != len(set(dkulcs)):
    hibak.append('duplikált döntés-kulcs a f3_4_dontesek.tsv-ben')

ures = set((s['id'], s['igehely']) for s in elo if not s['karoli_szo'].strip())
betoltott = set((s['id'], s['igehely']) for s in elo
                if (s['id'], s['igehely']) in dmap
                and s['karoli_szo'] == dmap[(s['id'], s['igehely'])]['karoli_szo'])

if ures:
    # betoltes elotti allapot: a dontes-tablanak pontosan az ures sorokat kell fednie
    allapot = 'BETÖLTÉS ELŐTT'
    tobb, keves = set(dkulcs) - ures, ures - set(dkulcs)
else:
    # betoltes utani allapot: minden dontes-sornak meg kell jelennie a tablaban
    allapot = 'BETÖLTÉS UTÁN'
    tobb, keves = set(), set(dkulcs) - betoltott

if tobb:
    hibak.append('fölös döntés-sor: %s' % sorted(tobb))
if keves:
    hibak.append('a döntés nem érvényesült / lefedetlen sor: %s' % sorted(keves))

# szovegszintu visszaellenorzes
nem_talal = []
for d in dont:
    if not d['join_igehely']:
        continue
    ig = ELTOLAS.get(d['igehely'], d['join_igehely'])
    ig = re.sub(r'^(\S+)', lambda m: HOSSZU.get(m.group(1), m.group(1)), ig)
    vers = karoli.get(ig)
    if vers is None:
        nem_talal.append((d['id'], d['igehely'], ig, 'nincs versszöveg'))
        continue
    mag = re.sub(r'\s*\([^)]*\)', '', d['karoli_szo']).split(';')[0].strip()
    mag = mag.split()[-1] if mag else ''
    if mag and mag.lower() not in vers.lower():
        nem_talal.append((d['id'], d['igehely'], ig, 'nem szerepel: ' + mag))

print('Állapot: %s' % allapot)
print('Döntés-sorok: %d | üres karoli_szo: %d | betöltött döntés: %d'
      % (len(dont), len(ures), len(betoltott)))
print('Szerkezeti hibák: %s' % (hibak or 'nincs'))
print('Szövegszintű eltérés (%d):' % len(nem_talal))
for t in nem_talal:
    print('   %-14s %-18s %-16s %s' % t)
