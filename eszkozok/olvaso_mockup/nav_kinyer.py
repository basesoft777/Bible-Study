"""A navigációs mockup adatai (csak olvasás): könyvek és fejezetszámok, a Jóel 2 szövege szavanként, kereszthivatkozások, Nave-témák, motívumok."""
import sys, sqlite3, json
from collections import defaultdict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = 'C:/Users/bases/Desktop/Bible-Study'
db = sqlite3.connect(f'file:{ROOT}/pardes.db?mode=ro', uri=True)
q = lambda s, *a: db.execute(s, a).fetchall()
KONYV, FEJ = 'Jóel', 2

konyvek = []
for kk, so, step, nev, _ in q("select * from konyv order by sorrend"):
    nf = q("select max(fejezet) from vers where konyv=?", kk)[0][0] or 0
    konyvek.append([kk, nev, nf, step])

versek = q("select igehely, vers, karoli_szoveg from vers where konyv=? and fejezet=? order by vers", KONYV, FEJ)
ihs = [v[0] for v in versek]

# héber tokenek és Károli-párok a szó-kártyához
heb = defaultdict(list)
for ih, sz, szo, strong, morf, gloss, lxx in q(
        f"select igehely,sorszam,szo,strong,morf,gloss,lxx_szo from token_macula where igehely in ({','.join('?'*len(ihs))}) order by igehely,sorszam", *ihs):
    heb[ih].append([szo, strong or '', morf or '', (gloss or '').replace('.', ' '), lxx or ''])
par = defaultdict(list)
for ih, hs, hu, strong, biz in q(
        f"select igehely,hu_sorszam,hu_szo,strong,bizonyossag from token_par where igehely in ({','.join('?'*len(ihs))}) order by igehely,hu_sorszam", *ihs):
    par[ih].append([hs, strong, biz])
strongok = sorted({p[1] for ps in par.values() for p in ps if p[1] and not p[1].startswith('H90')})
szotar = {}
for s in strongok:
    r = q("select szoto,kiejtes,jelentes from strong_szotar where strong=? or strong_szam=? limit 1", s, s)
    n = q("select count(*) from token_strong where strong=?", s)[0][0]
    if r:
        szotar[s] = [r[0][0], r[0][1], (r[0][2] or '')[:60], n]

# kereszthivatkozások (STEP-alak → magyar megjelenítés)
kh = defaultdict(list)
with open(f'{ROOT}/konkordancia/Karoli_kereszthivatkozasok.tsv', encoding='utf-8') as f:
    next(f)
    for s in f:
        m = s.rstrip('\n').split('\t')
        if m[0].startswith('Jol.2.'):
            kh[f"{KONYV} {FEJ}:{m[0].split('.')[2]}"].append(m[2])

nave = defaultdict(list)
for ih, tema in q(f"select igehely, tema from nave_vers where igehely in ({','.join('?'*len(ihs))})", *ihs):
    if tema not in nave[ih]:
        nave[ih].append(tema)

mot = {}
with open(f'{ROOT}/adat/motivumok.tsv', encoding='utf-8') as f:
    fej = None
    for s in f:
        if s.startswith('#') or not s.strip():
            continue
        m = s.rstrip('\n').split('\t')
        if fej is None:
            fej = m; continue
        d = dict(zip(fej, m)); mot[d['id']] = d['cim']
motv = defaultdict(list)
with open(f'{ROOT}/adat/elofordulasok.tsv', encoding='utf-8') as f:
    for s in f:
        if s.startswith('#'):
            continue
        m = s.rstrip('\n').split('\t')
        if len(m) > 1 and m[1] in ihs:
            motv[m[1]].append([m[0], mot.get(m[0], '')])

ki = {'konyvek': konyvek, 'konyv': KONYV, 'fej': FEJ, 'versek': versek, 'heb': heb, 'par': par, 'szotar': szotar,
      'kh': kh, 'nave': nave, 'motv': motv, 'motivumok': sorted(mot.items())}
json.dump(ki, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
print('versek', len(versek), 'heb', sum(map(len, heb.values())), 'par', sum(map(len, par.values())), 'szotar', len(szotar))
print('kh', sum(map(len, kh.values())), 'nave versek', len(nave), 'nave témák', len({t for v in nave.values() for t in v}), 'motv', dict(motv))
print('motívumok', len(mot), 'konyvek', len(konyvek), konyvek[28])
print(list(nave.items())[:3])
