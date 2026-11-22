import json, os, sqlite3, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('file:%s?mode=ro' % os.environ['PARDES_DB'], uri=True)
tabl = json.load(open(os.environ['KI']))
sor = {r[0]: r for r in con.execute('select tabla, licenc_allapot, kereskedelmi, licenc_dataset, cimke from tabla_licenc')}
from collections import Counter
c = Counter()
for t in tabl:
    r = sor.get(t)
    print(t, '|', r[1:] if r else 'NINCS tabla_licenc-sor')
    if r:
        c[(r[1], r[2])] += 1
print(c)
