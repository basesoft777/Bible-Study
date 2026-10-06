#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_gyokcsoport_meres.py -- F38 M0 5. pont: BDB-gyokcsoportok merese
(csak meres, import nelkul).

Forras: konkordancia/OSHL_lexikalis_index.tsv (openscriptures/HebrewLexicon
LexicalIndex.xml @ 21c9add, CC BY 4.0; a repoban mar benne van, l. a README-t).
A BDB-gyok a bdb_id elso ket tagja (pl. a.ac.aa -> a.ac); a TWOT-csoport a
TWOT-szam (a betujeles utotag nelkul). Heber (nem arameus) Strong-ok.

Kimenet: naplok/BDB_FORDITAS_gyokcsoportok.tsv
(strong, bdb_gyok, twot, bdb_rokonok, twot_rokonok, csak_bdb).

TSV: split('\t') / '\t'.join() (CLAUDE.md).
"""
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(REPO, 'konkordancia', 'OSHL_lexikalis_index.tsv')
KI = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_gyokcsoportok.tsv')


def twot_alap(t):
    m = re.match(r'^(\d+)', t)
    return m.group(1) if m else ''


def main():
    sorok = []
    with open(IDX, encoding='utf-8') as f:
        fej = None
        for sor in f:
            sor = sor.rstrip('\n')
            if sor.startswith('#') or not sor:
                continue
            m = sor.split('\t')
            if fej is None:
                fej = m
                continue
            r = dict(zip(fej, m))
            sorok.append(r)
    heb = [r for r in sorok if r['nyelv'] == 'heber' and re.match(r'^H\d{4}$', r['strong'])]
    gy = defaultdict(set)
    tw = defaultdict(set)
    adat = {}
    for r in heb:
        bid = r['bdb_id']
        parts = bid.split('.')
        gyok = '.'.join(parts[:2]) if len(parts) >= 3 and bid != '—' else ''
        t = twot_alap(r['twot'])
        adat[r['strong']] = (gyok, t)
        if gyok:
            gy[gyok].add(r['strong'])
        if t:
            tw[t].add(r['strong'])
    ki = ['\t'.join(['strong', 'bdb_gyok', 'twot', 'bdb_rokonok', 'twot_rokonok', 'csak_bdb'])]
    lefedett = 0
    tobblet = 0
    van_bdb_rokon = 0
    twotos = 0
    twotos_tobblet = 0
    for s in sorted(adat):
        gyok, t = adat[s]
        if not gyok:
            continue
        lefedett += 1
        br = sorted(gy[gyok] - {s})
        tr = sorted(tw[t] - {s}) if t else []
        cs = sorted(set(br) - set(tr))
        if br:
            van_bdb_rokon += 1
        if cs:
            tobblet += 1
        if t:
            twotos += 1
            if cs:
                twotos_tobblet += 1
        ki.append('\t'.join([s, gyok, r_or(t), ','.join(br), ','.join(tr), ','.join(cs)]))
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    gyokok = len(gy)
    print('heber Strong az indexben: %d' % len(heb))
    print('lefedett Strong (van bdb_gyok): %d; BDB-gyokcsoport: %d' % (lefedett, gyokok))
    print('legalabb egy BDB-rokonnal: %d' % van_bdb_rokon)
    print('csak_bdb tobblet (van BDB-rokon, ami nem azonos TWOT alatt): %d (%.1f%% a lefedettekbol; %.1f%% a rokonosokbol)'
          % (tobblet, 100.0 * tobblet / lefedett, 100.0 * tobblet / max(van_bdb_rokon, 1)))
    print('TWOT-szammal rendelkezo lefedett Strong: %d, ebbol csak_bdb tobblettel: %d (%.1f%%)' % (twotos, twotos_tobblet, 100.0 * twotos_tobblet / max(twotos, 1)))
    print('twot nelkul: %d' % sum(1 for s in adat if not adat[s][1]))


def r_or(t):
    return t if t else '—'


main()
