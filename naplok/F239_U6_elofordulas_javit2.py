# -*- coding: utf-8 -*-
"""F239 U6, az F2-újramérés után — az 1Móz 7:11 1/a-sorának pontosítása (F2 U6 63.: a Péld 8:28 „mélység forrásai”
kifejezésében más héber szó áll). Pontcsere, minden más sor bájtra azonos. Futtatás: [--ir]"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
UT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'adat', 'elofordulasok.tsv')
REGI = 'A mélység és a források szava a héberben a 8:2-n kívül csak a Péld 8:24-ben áll még együtt;'
UJ = ('A mélység és az itt álló „források” szó a héberben a 8:2-n kívül csak a Péld 8:24-ben áll még együtt '
      '(a Péld 8:28 „mélység forrásai” kifejezésében más héber szó áll);')
sorok = open(UT, encoding='utf-8', newline='').read().split('\n')
idx = [i for i, s in enumerate(sorok) if s.split('\t')[:2] == ['TEREMT-001', '1Móz 7:11']]
assert len(idx) == 1 and sorok[idx[0]].count(REGI) == 1
uj = list(sorok); uj[idx[0]] = sorok[idx[0]].replace(REGI, UJ)
assert sum(a != b for a, b in zip(sorok, uj)) == 1 and len(uj[idx[0]].split('\t')) == len(sorok[idx[0]].split('\t'))
print('változott sor: 1Móz 7:11')
if '--ir' in sys.argv:
    open(UT, 'w', encoding='utf-8', newline='').write('\n'.join(uj)); print('írva')
