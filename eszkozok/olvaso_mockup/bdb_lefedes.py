"""Mely ÓSZ-fejezetekben van a legtöbb héber szónak magyar BDB-szócikke (csak olvasás)."""
import sys, sqlite3
from collections import defaultdict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro', uri=True)
hu = {s for (s,) in db.execute("select distinct strong from forditasok where szotar='BDB' and forditas_hu is not null and trim(forditas_hu)<>''")}
gram = {s for (s,) in db.execute("select strong from grammatikai_strongok")}
print('magyar BDB szócikk', len(hu))
fej = defaultdict(set)
for ih, s in db.execute("select t.igehely, t.strong from token_strong t where t.strong like 'H%'"):
    if s in gram or s.startswith('H90'):
        continue
    k, cv = ih.rsplit(' ', 1)
    fej[(k, cv.split(':')[0])].add(s)
sor = []
for (k, f), ss in fej.items():
    n = len(ss); m = len(ss & hu)
    sor.append((m / n, n, m, k, f))
sor.sort(reverse=True)
print('teljes lefedettségű fejezetek, legalább 40 szóval:')
for x in [x for x in sor if x[0] == 1 and x[1] >= 40][:20]:
    print(x)
print('legjobbak, legalább 80 szóval:')
for x in [x for x in sor if x[1] >= 80][:15]:
    print(x)
for k, f in [('1Móz', '1'), ('1Móz', '3'), ('Zsolt', '23'), ('Ézs', '53'), ('Jóel', '2')]:
    ss = fej[(k, f)]; print(k, f, len(ss), len(ss & hu))
