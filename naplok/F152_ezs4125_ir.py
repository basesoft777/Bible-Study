"""F152.21: az Ézs 41:25 ISTENTISZT-001 jelölt elbírálása a DT478 szerint.

Írás előtt mérés a TAHOT-ból: a besém (H9003+H8034) után mi áll. Ha nem a JHVH (H3068),
hanem névmási rag, a jelölt `nyitva` → `elutasítva`, a felhasználó szavaival
(„Csak ahol JHVH áll”), manual provenienciával. Csak ez az egy sor változik;
split('\t') / '\t'.join(), összevetéssel.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID, HELY = 'ISTENTISZT-001', 'Ézs 41:25'

tok = []
with open('konkordancia/TAHOT_kivonat.tsv', encoding='utf-8') as f:
    for s in f:
        m = s.rstrip('\r\n').split('\t')
        if m[0] == HELY:
            tok.append(m)
utan = [(tok[i + 1][1], tok[i + 1][2], tok[i + 1][3]) for i in range(1, len(tok) - 1)
        if tok[i][1] == 'H8034' and tok[i - 1][1] == 'H9003']
print('TAHOT %s: besém után: %s' % (HELY, utan))
assert utan and all(u[0] != 'H3068' for u in utan)
assert all(u[0] in ('H9020', 'H9021', 'H9023') for u in utan)

UT = 'adat/jeloltek.tsv'
with open(UT, encoding='utf-8', newline='') as f:
    S = f.read().split('\n')
uj = list(S)
db = 0
for i, s in enumerate(S):
    m = s.split('\t')
    if len(m) > 9 and m[0] == ID and m[1] == HELY and m[9] == 'elofordulas':
        assert m[3] == 'nyitva', m[3]
        m[3] = 'elutasítva'
        m[4] = ('DT478 (a felhasználó, 2026-11-01: „Csak ahol JHVH áll”; alkalmazásra jóváhagyva 2026-11-02: '
                '„Igen, mind”): a besém után nem a JHVH (H3068) szó áll, hanem névmási rag (bismí, „nevemet”; '
                'TAHOT: %s) | scope=manual | forras=DONTESEK.md DT478 | ts=2026-11-02 | korábban (nyitva, %s): %s'
                % ('+'.join('%s %s' % (u[0], u[2]) for u in utan), m[8], m[4]))
        m[8] = '2026.11.02'
        uj[i] = '\t'.join(m)
        db += 1
assert db == 1
assert sum(a != b for a, b in zip(S, uj)) == 1 and len(S) == len(uj)
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(uj))
print('jeloltek.tsv: %s nyitva → elutasítva' % HELY)
