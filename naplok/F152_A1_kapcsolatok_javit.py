"""F152 A.1: a két hibás indoklás javítása az adat/kapcsolatok.tsv-ben (1Móz 4:26 → Jóel 2:32; Zsolt 116:4 → 116:13,
Zsolt 116:13 → 116:17). TSV: split('\t') / '\t'.join(); írás előtt sorösszevetés: csak ez a három sor `indoklas` mezője
változhat, minden más bájtra azonos (CLAUDE.md, TSV-olvasás).

Futtatás: python naplok/F152_A1_kapcsolatok_javit.py [--ir]
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(GYOKER, 'adat', 'kapcsolatok.tsv')

JOEL = ('A formula szó szerint egyezik: a קָרָא בְּשֵׁם יְהוָה (kárá besém JHVH) az 1Móz 4:26-ban áll először az '
        'Ószövetségben („Akkor kezdték segítségül hívni az Úrnak nevét”), és a Jóel 2:32-ben éri el prófétai '
        'csúcspontját („mindaz, a ki az Úrnak nevét hívja segítségül, megmenekül”): az első ószövetségi hely és a '
        'prófétai csúcspont ugyanazt a kifejezést hordozza, innen a Magas bizonyosság.')
ZSOLT_REGI = 'ugyanabban a versben, háromszor.'
ZSOLT_UJ = 'ugyanabban a zsoltárban, három versben (116:4, 116:13, 116:17).'
CEL = {('1Móz 4:26', 'Jóel 2:32', 'ISTENTISZT-001'): lambda r: JOEL,
       ('Zsolt 116:4', 'Zsolt 116:13', 'ISTENTISZT-001'): lambda r: r.replace(ZSOLT_REGI, ZSOLT_UJ),
       ('Zsolt 116:13', 'Zsolt 116:17', 'ISTENTISZT-001'): lambda r: r.replace(ZSOLT_REGI, ZSOLT_UJ)}

with open(UT, encoding='utf-8', newline='') as f:
    nyers = f.read()
eol = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(eol)
fej = None
uj = []
valtozott = 0
for s in sorok:
    if s.startswith('#') or not s:
        uj.append(s)
        continue
    m = s.split('\t')
    if fej is None:
        fej = m
        uj.append(s)
        continue
    kulcs = tuple(m[:3])
    if kulcs in CEL:
        i = fej.index('indoklas')
        regi = m[i]
        m[i] = CEL[kulcs](regi)
        assert m[i] != regi, kulcs
        valtozott += 1
        print('%s → %s\n  régi: %s\n  új:   %s' % (kulcs[0], kulcs[1], regi, m[i]))
    uj.append('\t'.join(m))
assert valtozott == 3, valtozott
# sorösszevetés: csak a három sor változott, és azokban csak az indoklas mező
elter = [(a, b) for a, b in zip(sorok, uj) if a != b]
assert len(sorok) == len(uj) and len(elter) == 3
for a, b in elter:
    x, y = a.split('\t'), b.split('\t')
    assert len(x) == len(y) and [k for k in range(len(x)) if x[k] != y[k]] == [fej.index('indoklas')]
print('sorösszevetés: %d sor, eltérés 3 sor, csak az `indoklas` mezőben' % len(sorok))
if '--ir' in sys.argv:
    with open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write(eol.join(uj))
    print('írva: adat/kapcsolatok.tsv')
