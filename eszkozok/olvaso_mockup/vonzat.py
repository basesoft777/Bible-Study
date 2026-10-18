"""A H7121 vonzata gépi szabállyal (szóközelség, token_macula): a következő legfeljebb 4 tokenben az első vonzat-jelölő, tagmondathatárig (וְ)."""
import sys, os, json, sqlite3
from collections import Counter, defaultdict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect('file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro', uri=True)

vers = defaultdict(list)
for row in db.execute("select igehely,sorszam,szo,lemma,strong,morf from token_macula where igehely in (select igehely from token_macula where strong='H7121') order by igehely,sorszam"):
    vers[row[0]].append(row)

import re
def K(x):
    """Mássalhangzó-váz (a pontozás kódpont-sorrendje a forrásban eltérhet)."""
    return re.sub(r'[֑-ׇ‍]', '', x or '')

def osztaly(tl, i):
    t = tl[i]
    nx = tl[i+1:i+5]
    sem = lambda x: x[4] == 'H8034'
    elo = lambda x, v: K(x[3]) == v and (x[5] or '')[:1] == 'R'     # elöljáró
    nifal = (t[5] or '')[1:2] == 'N'
    if nifal and any(sem(x) for x in nx) and any(elo(x, 'על') for x in nx):
        return 'nev_rajta'
    for j, x in enumerate(nx):
        if K(x[3]) == 'ו' and j > 0:
            break
        kov = nx[j+1] if j + 1 < len(nx) else None
        kov2 = nx[j+2] if j + 2 < len(nx) else None
        if elo(x, 'ב') and kov and (sem(kov) or (K(kov[3]) == 'ה' and kov2 and sem(kov2))):
            return 'bsem'
        if sem(x):
            return 'sem'
        if elo(x, 'אל'):
            return 'el'
        if elo(x, 'ל'):
            return 'le'
        if K(x[3]) == 'את' and (x[5] or '')[:1] == 'T':
            return 'sem' if kov and sem(kov) else 'et'
        if elo(x, 'על'):
            return 'al'
        if elo(x, 'ב'):
            return 'bkol' if kov and K(kov[3]) in ('קול', 'אזן') else 'b'
    return 'nincs'

k = json.load(open(os.path.join(d, 'konk2.json'), encoding='utf-8'))
per = {}
cnt = Counter()
for ih, tl in vers.items():
    s = []
    for i, t in enumerate(tl):
        if t[4] == 'H7121':
            o = osztaly(tl, i)
            o = 'sem' if o == 'et_sem' else o
            s.append(o); cnt[o] += 1
    per[ih] = s
for r in k['sorok']:
    r['v'] = per.get(r['r'], [])
json.dump(k, open(os.path.join(d, 'konk3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(cnt.most_common())
for o in ('bsem', 'nev_rajta', 'el', 'bkol'):
    print(o, [ih for ih, s in per.items() if o in s][:12])
