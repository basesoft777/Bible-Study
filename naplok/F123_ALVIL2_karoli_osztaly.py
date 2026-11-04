# -*- coding: utf-8 -*-
"""F123 ALVIL-001 új cikk, U1 — a teljesség-mérés 2. hálójának (Károli-szó) eltérései,
lexémánként osztályozva: a Károli-szó melyik héber/görög szót fordítja az adott versben.
Módszer: a vers TAHOT/TAGNT-tokenjei közül azok a Strongok, amelyek angol glosszája a
Károli-szó jelentéskörébe esik (sír/koporsó: grave, tomb, sepulchre, coffin, burial;
sír ige: weep, cry, wail, mourn; pokol/mélység/alvilág: pit, deep, abyss, hell, depth).
Gépi osztályozás, döntés nélkül; az osztálytalan sor kézi olvasásra marad.
Kimenet: naplok/F123_teljesseg_ALVIL-001_karoli_osztaly.tsv; összegzés a konzolra."""
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L  # noqa: E402

MINTA = {
    'sír/koporsó (főnév)': re.compile(r'\b(grave|tomb|sepulch|coffin|burial|bury)', re.I),
    'sír (ige: sírni)': re.compile(r'\b(weep|wept|cry|cried|wail|mourn|lament|tear)', re.I),
    'mélység/verem': re.compile(r'\b(pit|deep|abyss|depth|cistern|dungeon|well)', re.I),
    'halál': re.compile(r'\b(death|die|dead)', re.I),
}

tok = defaultdict(list)
for r in list(L.load_tahot()) + list(L.load_tagnt()):
    tok[r['Igehely']].append(r)

be = os.path.join(GY, 'naplok', 'F123_teljesseg_ALVIL-001.tsv')
sorok = [s.rstrip('\n').split('\t') for s in open(be, encoding='utf-8') if not s.startswith('#')]
fej, sorok = sorok[0], sorok[1:]
ki_sorok = []
osszeg = Counter()
lexema = Counter()
for s in sorok:
    d = dict(zip(fej, s))
    if d['halo'] != 'karoli' or d['allapot'] != 'ELTÉRÉS':
        continue
    talalt = []
    for t in tok.get(d['igehely'], []):
        glossz = (t.get('Rövid jelentés', '') + ' ' + t.get('Angol tükörfordítás', ''))
        for nev, m in MINTA.items():
            if m.search(glossz):
                talalt.append((nev, t['Strong-szám'], t.get('Szótő', '')))
    osztalyok = sorted({x[0] for x in talalt})
    osztaly = ' + '.join(osztalyok) if osztalyok else 'osztálytalan'
    osszeg[osztaly] += 1
    for x in {(a, b, c) for a, b, c in talalt}:
        lexema[x] += 1
    ki_sorok.append([d['igehely'], d['reszlet'], osztaly,
                     '; '.join(sorted({'%s %s' % (b, c) for a, b, c in talalt}))])

ki = os.path.join(GY, 'naplok', 'F123_teljesseg_ALVIL-001_karoli_osztaly.tsv')
with open(ki, 'w', encoding='utf-8', newline='\n') as f:
    f.write('# F123 ALVIL-001 U1: a Károli-háló eltéréseinek gépi lexéma-osztályozása (naplok/F123_ALVIL2_karoli_osztaly.py); '
            'scope=naplok/F123_teljesseg_ALVIL-001.tsv karoli ELTÉRÉS × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (glossza) | forras=split(\'\t\') | ts=2026-11-02\n')
    f.write('igehely\tkaroli_szoalak\tosztaly\tjelolt_strongok\n')
    for s in ki_sorok:
        f.write('\t'.join(s) + '\n')
for k, v in osszeg.most_common():
    print('%4d  %s' % (v, k))
print('--- leggyakoribb lexémák')
for (a, b, c), v in lexema.most_common(25):
    print('%4d  %-22s %s %s' % (v, a, b, c))
