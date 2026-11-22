import json, os, sqlite3, sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('file:%s?mode=ro' % os.environ['PARDES_DB'], uri=True)
tabl = json.load(open(os.environ['KI']))
try:
    meret = dict(con.execute("select name, sum(pgsize) from dbstat group by name").fetchall())
except Exception as e:
    print('nincs dbstat', e)
    meret = {}
ossz = 0
sor = []
for t in tabl:
    try:
        n = con.execute('select count(*) from "%s"' % t).fetchone()[0]
    except Exception as e:
        n = 'nincs: %s' % e
    m = meret.get(t, 0)
    # indexek
    idx = [r[0] for r in con.execute("select name from sqlite_master where type='index' and tbl_name=?", (t,))]
    mi = sum(meret.get(i, 0) for i in idx)
    sor.append((m + mi, t, n, m, mi))
for tot, t, n, m, mi in sorted(sor, reverse=True):
    print('%10.1f MB  %-28s sor=%s  tabla=%.1f idx=%.1f' % (tot / 1e6, t, n, m / 1e6, mi / 1e6))
    ossz += tot
print('OSSZ %.1f MB' % (ossz / 1e6))
print('db egyeb nagy tablak:')
allt = sorted(((v, k) for k, v in meret.items()), reverse=True)[:12]
for v, k in allt:
    print('  %.1f MB %s' % (v / 1e6, k))
print('vers sorok:', con.execute('select count(*) from vers').fetchone())
print('meta:', con.execute("select * from meta where kulcs like 'epites%' limit 3").fetchall() if True else '')
