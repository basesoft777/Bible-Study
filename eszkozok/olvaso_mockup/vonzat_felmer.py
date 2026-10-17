import sys, sqlite3
from collections import Counter, defaultdict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro', uri=True)
print(db.execute("select * from token_macula limit 1").fetchall())
vers = defaultdict(list)
for row in db.execute("select igehely,sorszam,szo,lemma,strong,morf from token_macula where igehely in (select igehely from token_macula where strong='H7121') order by igehely,sorszam"):
    vers[row[0]].append(row)
c1, c2 = Counter(), Counter()
for ih, tl in vers.items():
    for i, t in enumerate(tl):
        if t[4] != 'H7121':
            continue
        nx = tl[i+1:i+4]
        c1[' '.join(f"{x[3]}|{x[4]}|{(x[5] or '')[:2]}" for x in nx[:1])] += 1
        c2[' '.join((x[3] or '?') for x in nx[:2])] += 1
print(c1.most_common(30))
print(c2.most_common(30))
