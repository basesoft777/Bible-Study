# -*- coding: utf-8 -*-
"""F239 U1 1/4. pont: a H8415-versek tartalmi Strongjainak gyakorisága (kollokáció-jelöltek, gépi, döntés nélkül)."""
import sys, os
from collections import defaultdict, Counter
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L
gr = L.load_grammatikai_strongok()
byv = defaultdict(set); gl = {}
for parsed, strong, src in L.combined_rows():
    byv[parsed].add(strong)
for r in L.load_tahot():
    gl.setdefault(r['Strong-szám'], r.get('Rövid jelentés',''))
verses = [p for p, s in byv.items() if 'H8415' in s]
c = Counter()
for p in verses:
    for s in byv[p]:
        if s not in gr and s != 'H8415':
            c[s] += 1
print(len(verses))
for s, n in c.most_common(30):
    print(s, n, gl.get(s,''))
