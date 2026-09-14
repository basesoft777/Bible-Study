# -*- coding: utf-8 -*-
"""F3.4 zaro integritas-ellenorzes."""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEGBIZ = {'magas', 'közepes', 'alacsony'}
AZON = {'tartalom-alapú', 'szó-szintű-tagged', 'interlineáris-gloss', 'kikövetkeztetett'}


def olvas(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f]
    if sorok[0].startswith('#'):
        sorok = sorok[1:]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.strip()]


hibak = []

fe, elo = olvas(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))
ures = [s for s in elo if not s['karoli_szo'].strip()]
print('elofordulasok.tsv: %d sor, ures karoli_szo: %d' % (len(elo), len(ures)))
for s in elo:
    if s['karoli_szo'].strip():
        if s['azonositas_modja'] not in AZON:
            hibak.append('rossz azonositas_modja: %s %s = %r' % (s['id'], s['igehely'], s['azonositas_modja']))
        if s['megbizhatosag'] not in MEGBIZ:
            hibak.append('rossz megbizhatosag: %s %s = %r' % (s['id'], s['igehely'], s['megbizhatosag']))
    elif s['azonositas_modja'].strip() or s['megbizhatosag'].strip():
        hibak.append('ures karoli_szo mellett kitoltott triplet: %s %s' % (s['id'], s['igehely']))

fj, jel = olvas(os.path.join(ROOT, 'adat', 'jeloltek.tsv'))
eidx = {(s['id'], s['igehely']): s for s in elo}
elteres = 0
for j in jel:
    e = eidx.get((j['id'], j['igehely']))
    if e and e['karoli_szo'].strip() and j['karoli_szo'] != e['karoli_szo']:
        elteres += 1
    if j['karoli_szo'].strip():
        if j['azonositas_modja'] not in AZON or j['megbizhatosag'] not in MEGBIZ:
            hibak.append('jeloltek triplet hianyos: %s %s' % (j['id'], j['igehely']))
print('jeloltek.tsv: %d sor, elofordulasok-tol elteroe karoli_szo: %d' % (len(jel), elteres))

ut = os.path.join(ROOT, 'konkordancia', 'Karoli_Strong_kivonat.tsv')
_, join = olvas(ut)
kulcsok = [(s['Igehely'], s['Strong-szám']) for s in join]
dup = set(k for k in kulcsok if kulcsok.count(k) > 1)
print('Karoli_Strong_kivonat.tsv: %d sor, %d egyedi igehely, %d egyedi Strong'
      % (len(join), len(set(s['Igehely'] for s in join)),
         len(set(s['Strong-szám'] for s in join))))
if dup:
    hibak.append('duplikalt join-kulcs: %s' % sorted(dup))
for s in join:
    if not re.match(r'^[A-Za-z0-9]+\.\d+\.\d+$', s['Igehely']):
        hibak.append('rossz STEPBible-igehely: %r' % s['Igehely'])
    for tag in s['Strong-szám'].split('+'):
        if not re.match(r'^[HG]\d{4}$', tag):
            hibak.append('rossz Strong: %r (%s)' % (s['Strong-szám'], s['Igehely']))
            break
    if not s['Károli-szó'].strip():
        hibak.append('ures Karoli-szo: %s %s' % (s['Igehely'], s['Strong-szám']))
    if s['Megbízhatóság'] not in MEGBIZ:
        hibak.append('rossz megbizhatosag a joinban: %s %s = %r'
                     % (s['Igehely'], s['Strong-szám'], s['Megbízhatóság']))

meg = {}
for s in join:
    meg[s['Megbízhatóság']] = meg.get(s['Megbízhatóság'], 0) + 1
print('  megbizhatosag-megoszlas: %s' % meg)
forrasok = set(s['Forrás-tanulmány'] for s in join)
print('  forras-tanulmanyok szama: %d' % len(forrasok))

print('')
print('HIBAK (%d):' % len(hibak))
for h in hibak:
    print('   ' + h)
