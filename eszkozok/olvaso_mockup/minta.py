import sys, sqlite3
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
db = sqlite3.connect('file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro', uri=True)
q = lambda s, *a: db.execute(s, a).fetchall()
print(q("select * from token_strong where strong like '%7121%' limit 3"))
print(q("select * from konyv limit 3"))
print(q("select * from vers where igehely like 'Jóel 2:32'"))
print(q("select igehely,sorszam,szo,strong,morf,lxx_szo,lxx_strong,allapot from token_macula where strong like '%7121%' limit 3"))
print(q("select * from token_par where strong like '%7121%' limit 3"))
print(q("select * from token_karoli where igehely='Jóel 2:32' limit 12"))
print(q("select count(*), count(distinct igehely) from token_strong where strong='H7121'"))
print(q("select count(*), count(distinct igehely) from token_macula where strong='H7121'"))
