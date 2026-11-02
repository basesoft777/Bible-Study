#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F27 ⛔ M1 — 5 véletlen Strong (seed = 27, a beírt, nem funkciószó Strongok hossz szerinti harmadaiból) forrás és fordítás egymás alatt."""
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
ITT = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(ITT)
sys.path.insert(0, os.path.join(GY, 'eszkozok', 'thayer_jelolt'))
import thayer_bemenet as TB  # noqa: E402


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n')]
    s = [x for x in s if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


beirt = {}
for r in tsv(os.path.join(GY, 'adat', 'forditasok.tsv')):
    if r['szotar'] == 'Thayer' and r['allapot'] == 'sonnet' and r['datum'] == '2026.11.02' and r['jelentes_szam'].startswith('sz'):
        beirt.setdefault(r['strong'], {})[int(r['jelentes_szam'][2:])] = r['forditas_hu']
nem_fv = [r for r in tsv(os.path.join(ITT, 'FP3_m1_strongok.tsv')) if r['kategoria'] != 'funkciószó' and r['strong'] in beirt]
nem_fv.sort(key=lambda r: int(r['karakter']))
n = len(nem_fv)
harmad = [nem_fv[:n // 3], nem_fv[n // 3:2 * n // 3], nem_fv[2 * n // 3:]]
rnd = random.Random(27)
valasztott = [rnd.choice(harmad[0]), rnd.choice(harmad[0]), rnd.choice(harmad[1]), rnd.choice(harmad[2]), rnd.choice(harmad[2])]
ki = ['# FP3 — 5 véletlen Strong az M1 beírt soraiból (seed 27; a nem funkciószó beírt Strongok hossz szerinti harmadaiból: 2 rövid, 1 közepes, 2 hosszú)\n']
for r in valasztott:
    sp = r['strong']
    szak = TB.szakaszok(sp)
    ki.append('\n## %s (%s, %s kar., %s szakasz)\n' % (sp, r['kategoria'], r['karakter'], r['szakasz']))
    for x in szak[:4]:
        ki.append('**Forrás sz%d**\n\n%s\n\n**Fordítás sz%d**\n\n%s\n' % (x['sorszam'], x['szoveg'][:1500], x['sorszam'], beirt[sp][x['sorszam']][:1500]))
    if len(szak) > 4:
        ki.append('*(+%d további szakasz a táblában)*\n' % (len(szak) - 4))
open(os.path.join(ITT, 'FP3_veletlen.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(ki))
print([r['strong'] for r in valasztott])
