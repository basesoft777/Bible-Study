"""F158 mérés: az ISTENTISZT-001 beépített ÓSZ-előfordulásain mi áll a besém (H9003+H8034) után.

A K4 (DT-F151c) elhatárolása: a besém után álló JHVH (H3068). A mérés megmutatja,
melyik beépített sor teljesíti szó szerint, és melyiknél áll névmási rag
(pl. besimchá) vagy más név. Csak olvas; kimenet: stdout.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'


def sorok(ut):
    with open(ut, encoding='utf-8') as f:
        return [s.rstrip('\r\n').split('\t') for s in f if s.strip() and not s.startswith('#')]


elo = sorok('adat/elofordulasok.tsv')
fej = elo[0]
helyek = [s[1] for s in elo[1:] if s[0] == ID]

tahot = {}
for s in sorok('konkordancia/TAHOT_kivonat.tsv')[1:]:
    tahot.setdefault(s[0], []).append(s)

print('ISTENTISZT-001 előfordulás:', len(helyek))
for h in helyek:
    if h not in tahot:
        print('%-14s ÚSZ / nincs TAHOT-sor' % h)
        continue
    tok = tahot[h]
    talalat = []
    for i, t in enumerate(tok):
        if t[1] == 'H8034':
            elozo = tok[i - 1][1] if i else ''
            utana = [x[1] + ':' + x[3] for x in tok[i + 1:i + 3]]
            talalat.append('%s|%s(%s) → %s' % (elozo, t[2], t[3], ', '.join(utana)))
    print('%-14s %s' % (h, ' ;; '.join(talalat) or 'nincs H8034'))
