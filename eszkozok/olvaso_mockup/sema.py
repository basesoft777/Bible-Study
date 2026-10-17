import sys, sqlite3
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro', uri=True)
for (n, s) in db.execute("select name, sql from sqlite_master where type='table' order by name"):
    if any(k in n for k in ('token', 'vers', 'karoli', 'morf', 'konyv', 'strong', 'lxx')):
        print(s[:400]); print()
