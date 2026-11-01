"""N60 mérése egy motívumon: a TSK erős ajánlásai (Votes >= küszöb), amelyek sem előfordulásként,
sem az adott motívum jelöltjeként nem szerepelnek, és hordozzák-e a gerinc szópárját.
Használat: python naplok/N60_TSK_meres.py [MOTIVUM-ID] [KÜSZÖB]  (alap: ISTENTISZT-001 15)
A gerinc-szűrés az ISTENTISZT-001-re szól (H7121+H8034 a TAHOT-ban, G1941 a TAGNT-ban).
Csak olvas; split('\t')."""
import os, sys
from collections import Counter
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MID = sys.argv[1] if len(sys.argv) > 1 else 'ISTENTISZT-001'
KUSZOB = int(sys.argv[2]) if len(sys.argv) > 2 else 15
def tsv(p):
    L = [l.rstrip('\n').split('\t') for l in open(os.path.join(REPO, p), encoding='utf-8') if not l.startswith('#')]
    return L[0], L[1:]
def kulcsok(p, strong):
    return {l.split('\t')[0] for l in open(os.path.join(REPO, 'konkordancia', p), encoding='utf-8') if strong in l}
_, e = tsv('adat/elofordulasok.tsv'); el = {r[1] for r in e if r[0] == MID}
_, j = tsv('adat/jeloltek.tsv'); jel = {r[1] for r in j if r[0] == MID}; barmely = {r[1] for r in j}
_, t = tsv('konkordancia/TSK_kereszthivatkozasok.tsv')
cel = {}
for r in t:
    if r[0] in el and r[3].isdigit():
        cel.setdefault(r[1], []).append((int(r[3]), r[0]))
k = sorted(((max(x)[0], c, max(x)[1]) for c, x in cel.items()
            if max(x)[0] >= KUSZOB and c not in el and c not in jel), reverse=True)
h = kulcsok('TAHOT_kivonat.tsv', 'H7121') & kulcsok('TAHOT_kivonat.tsv', 'H8034')
g = kulcsok('TAGNT_kivonat.tsv', 'G1941')
print('motívum:', MID, '| előfordulás:', len(el), '| jelölt:', len(jel))
print('TSK-cél Votes >= %d, se előfordulás, se jelölt: %d (>= 50: %d)' % (KUSZOB, len(k), sum(1 for x in k if x[0] >= 50)))
print('kiinduló igehely szerint:', Counter(f for _, _, f in k).most_common())
print('más motívum jelöltje:', sum(1 for x in k if x[1] in barmely))
print('gerinc szópárt hordoz:', [c for _, c, _ in k if c in h or c in g])
print('kontroll — az előfordulásokból gerinc szópárt hordoz: %d / %d' % (sum(1 for x in el if x in h or x in g), len(el)))
