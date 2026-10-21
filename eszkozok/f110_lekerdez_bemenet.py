#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F110 2. lépés: a 168 + 21 hely kigyűjtése az F108 eltérés-táblából és
újralekérdezése a mai adaton (lekerdez.py kollokacio / scan). Kimenet:
naplok/F110_lekerdezesek.tsv (proveniencia-sorok), naplok/F110_bemenet.tsv."""
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
rows = [l.rstrip('\n').split('\t') for l in open(ROOT/'naplok/F108_ujrascan_elteresek.tsv', encoding='utf-8')][1:]
ujH = [r[2] for r in rows if r[0] == 'ISTENTISZT-001' and r[1] == 'ujrascan' and r[4] == 'uj_talalat_nem_irva_tul_tag']
ujG = [r[2] for r in rows if r[0] == 'ISTENTISZT-001' and r[1] == 'ujrascan' and r[4] == 'uj_jelolt_irva']
print(len(ujH), len(set(ujH)), len(ujG), len(set(ujG)))


def run(args):
    p = subprocess.run([sys.executable, str(ROOT/'eszkozok/lekerdez.py')] + args,
                       capture_output=True, encoding='utf-8', cwd=str(ROOT))
    lines = p.stdout.splitlines()
    prov = [l for l in lines if l.startswith('proveniencia:')][-1][len('proveniencia: '):]
    places = [l for l in lines if l and not l.startswith('#') and not l.startswith('proveniencia:')]
    return places, prov


kol, provK = run(['kollokacio', 'H7121', 'H8034'])
scn, provS = run(['scan', 'G1941'])
setK, setS = set(kol), set(scn)
miss = [x for x in ujH if x not in setK] + [x for x in ujG if x not in setS]
print('kollokacio n=', len(kol), 'scan n=', len(scn), 'hiányzik az újralekérdezésből:', miss)
with open(ROOT/'naplok/F110_lekerdezesek.tsv', 'w', encoding='utf-8', newline='') as f:
    f.write('# GENERALT: F110.2 | az F108 uj-helyeinek ujralekerdezese a mai adaton (nem az elavult claude/f110-szuro-pilot agbol)\n')
    f.write('parancs\tn\tF108-bemenet_n\tbemenet_a_talalatban\tproveniencia\n')
    f.write(f'lekerdez.py kollokacio H7121 H8034\t{len(kol)}\t{len(ujH)}\t{sum(x in setK for x in ujH)}\t{provK}\n')
    f.write(f'lekerdez.py scan G1941\t{len(scn)}\t{len(ujG)}\t{sum(x in setS for x in ujG)}\t{provS}\n')
with open(ROOT/'naplok/F110_bemenet.tsv', 'w', encoding='utf-8', newline='') as f:
    f.write('csoport\tigehely\tforras\n')
    for x in ujH:
        f.write(f'H7121+H8034\t{x}\tF108_ujrascan_elteresek.tsv:uj_talalat_nem_irva_tul_tag\n')
    for x in ujG:
        f.write(f'G1941\t{x}\tF108_ujrascan_elteresek.tsv:uj_jelolt_irva\n')
