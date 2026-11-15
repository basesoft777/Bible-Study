# -*- coding: utf-8 -*-
"""K-tétel-lista egy forráson (F224.4 alapvonal/összevetés).
Használat: klista.py <ID> <forras.md> <elof.tsv> <kapcs.tsv> <ki.txt> [lap.md]"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.getcwd(), 'eszkozok'))
import proza_allitas as P
mid, md, elof, kapcs, ki = sys.argv[1:6]
lap = sys.argv[6] if len(sys.argv) > 6 else None
P.T_KAPCS = kapcs
try:
    ell, adat, szk, n = P.futtat(mid, md, elof, lap)
except TypeError:
    ell, adat, szk, n = P.futtat(mid, md, elof)
szoveg = P.jelentes(mid, ell, adat, None, 'x', ell.egysegek)
with open(ki + '.teljes.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(szoveg)
sorok = [l for l in szoveg.split('\n') if l.startswith('### K')]
with open(ki, 'w', encoding='utf-8', newline='\n') as f:
    for l in sorok:
        f.write(l + '\n')
print(mid, os.path.basename(md), 'egység', n, 'K-tétel', len(sorok), 'ELTÉR', sum(1 for s in ell.sorok if s.itelet == 'ELTÉR'))
