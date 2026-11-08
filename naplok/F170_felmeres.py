#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F170_felmeres.py -- a nyílt mag angol rétegének felmérése (F170, 1. lépés).

Oszloponként: zárt/szabad besorolás, egyedi értékek száma és karakterszáma; az igehely-oszlopok könyvnevei
és a leképezhetetlenek; a `jelentes_en` forrása (összevetés a TBESH/TBESG-glosszával). Csak olvas.
Használat: python naplok/F170_felmeres.py
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import nyilt_mag_kapu as K  # noqa: E402

fajlok = K.olvas_csomag(os.path.join(GY, 'nyilt_mag'))
IGEHELY_OSZLOP = {'igehely', 'cel_igehely', 'forras_igehely', 'igehely_a', 'igehely_b', 'csoport_sor_igehely'}

_, norm = K.E.tsv('konkordancia/Konyv_normalizalo_tabla.tsv')
hu_konyv = {s['Magyar rövidítés'] for s in norm}

print('== oszlopok')
for rel in sorted(fajlok):
    if not rel.endswith('.tsv') or rel == 'kodkonyv.tsv':
        continue
    fej, sorok = K.tsv_sorok(fajlok[rel])
    for o in fej:
        ert = [d[o] for _, d in sorok if d[o]]
        egyedi = sorted(set(ert))
        zart = o in K.ZART.get(rel, [])
        print('%s\t%s\t%s\tsor=%d\tegyedi=%d\tkar(egyedi)=%d\tpl=%s' % (
            rel, o, 'ZART' if zart else '-', len(ert), len(egyedi), sum(len(x) for x in egyedi),
            (egyedi[0][:70] if egyedi else '')))

print('== igehely-könyvnevek')
konyvek = {}
rossz = []
for rel in sorted(fajlok):
    if not rel.endswith('.tsv'):
        continue
    fej, sorok = K.tsv_sorok(fajlok[rel])
    for o in fej:
        if o not in IGEHELY_OSZLOP:
            continue
        for n, d in sorok:
            v = d[o]
            if not v:
                continue
            m = re.match(r'^(\S+) (\d+):(\d+)(?:[-–](\d+))?$', v)
            if not m:
                rossz.append((rel, o, n, v))
                continue
            konyvek[m.group(1)] = konyvek.get(m.group(1), 0) + 1
            if m.group(1) not in hu_konyv:
                rossz.append((rel, o, n, v))
print('különböző könyvnév: %d; igehely-cella: %d' % (len(konyvek), sum(konyvek.values())))
print('leképezhetetlen / nem szabályos alakú: %d' % len(rossz))
for r in rossz[:40]:
    print('  ', r)

print('== jelentes_en vs TBESH/TBESG')
glossza = {}
for fn in ('konkordancia/TBESH.txt', 'konkordancia/TBESG.txt'):
    with open(os.path.join(GY, fn), encoding='utf-8') as f:
        for s in f:
            m = s.rstrip('\n').split('\t')
            if len(m) >= 8 and re.match(r'^[HG]\d{4}[A-Za-z]?$', m[0]):
                glossza.setdefault(m[0][:5], set()).add(m[6].strip())
_, elo = K.tsv_sorok(fajlok['elofordulasok.tsv'])
egyez, nem, ures = 0, [], 0
for n, d in elo:
    je = d['jelentes_en']
    if not je:
        ures += 1
        continue
    st = (d['strong'] or '').split('+')[0].strip()[:5]
    g = glossza.get(st, set())
    if je in g:
        egyez += 1
    else:
        nem.append((d['igehely'], d['strong'], d['szotar'], je[:60], sorted(g)[:3]))
print('jelentes_en: kitöltött=%d, üres=%d, TBESH/TBESG-glosszával egyező=%d, eltérő=%d' % (
    len(elo) - ures, ures, egyez, len(nem)))
for x in nem[:15]:
    print('  ', x)
szotarak = {}
for _, d in elo:
    szotarak[d['szotar']] = szotarak.get(d['szotar'], 0) + 1
print('szotar-értékek: %s' % szotarak)
