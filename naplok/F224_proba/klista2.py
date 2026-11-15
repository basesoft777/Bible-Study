# -*- coding: utf-8 -*-
"""F224.17: K-tétel-lista egy forráson a jelöltekkel is (F224.14–.15, a mondaton kívüli adat).
Használat: klista2.py <ID> <forras.md> <elof.tsv> <kapcs.tsv> <jelolt.tsv> <lap.md> <ki.md>"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.getcwd(), 'eszkozok'))
import proza_allitas as P
mid, md, elof, kapcs, jelolt, lap, ki = sys.argv[1:8]
P.T_KAPCS = kapcs
ell, adat, szk, n = P.futtat(mid, md, elof, lap, jelolt)
szoveg = P.jelentes(mid, ell, adat, None, '%s (%s), %s, %s, %s; %d egység' % (
    os.path.basename(md), mid, os.path.basename(elof), os.path.basename(kapcs), os.path.basename(jelolt), n),
    ell.egysegek)
with open(ki, 'w', encoding='utf-8', newline='\n') as f:
    f.write(szoveg)
k = [l for l in szoveg.split('\n') if l.startswith('### K')]
print(mid, 'egység', n, 'K-tétel', len(k), 'ELTÉR', sum(1 for s in ell.sorok if s.itelet == 'ELTÉR'),
      'új fajta:', {t: sum(1 for s in ell.sorok if s.tipus == t) for t in P.UJ_FAJTAK})
