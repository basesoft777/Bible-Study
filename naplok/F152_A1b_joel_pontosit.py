"""F152 A.1 utótétel (ELLENOR_F152, A.1 „először az ÓSZ-ben”): az 1Móz 4:26 → Jóel 2:32 indoklásában az „áll először az
Ószövetségben” helyett az adatból igazolható „a motívum első ószövetségi helye” (adat/elofordulasok.tsv, kanonikus
sorrend); a Strong-hármas (H7121+H8034+H3068) már az 1Móz 2:19-ben is együtt áll, névadásban. TSV: split('\t'); írás
előtt sorösszevetés: csak ez az egy mező változhat.

Futtatás: python naplok/F152_A1b_joel_pontosit.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(GYOKER, 'adat', 'kapcsolatok.tsv')
REGI = 'az 1Móz 4:26-ban áll először az Ószövetségben („Akkor kezdték segítségül hívni az Úrnak nevét”)'
UJ = 'az 1Móz 4:26-ban, a motívum első ószövetségi helyén áll („Akkor kezdték segítségül hívni az Úrnak nevét”)'
REGI2 = 'az első ószövetségi hely és a prófétai csúcspont ugyanazt a kifejezést hordozza'
UJ2 = 'a motívum első ószövetségi helye és prófétai csúcspontja ugyanazt a kifejezést hordozza'

with open(UT, encoding='utf-8', newline='') as f:
    nyers = f.read()
eol = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(eol)
uj = []
for s in sorok:
    m = s.split('\t')
    if m[:3] == ['1Móz 4:26', 'Jóel 2:32', 'ISTENTISZT-001']:
        assert m[-1].count(REGI) == 1 and m[-1].count(REGI2) == 1
        m[-1] = m[-1].replace(REGI, UJ).replace(REGI2, UJ2)
    uj.append('\t'.join(m))
elter = [(a, b) for a, b in zip(sorok, uj) if a != b]
assert len(sorok) == len(uj) and len(elter) == 1
x, y = elter[0][0].split('\t'), elter[0][1].split('\t')
assert [k for k in range(len(x)) if x[k] != y[k]] == [len(x) - 1]
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write(eol.join(uj))
print('sorösszevetés: %d sor, eltérés 1 sor, csak az indoklas mezőben; írva' % len(sorok))
