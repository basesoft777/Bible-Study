"""Az olvasói konkordancia-mockup adatai a pardes.db-ből (csak olvasás), a H7121-re."""
import sys, sqlite3, json
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB = 'file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro'
S = 'H7121'
db = sqlite3.connect(DB, uri=True)
q = lambda s, *a: db.execute(s, a).fetchall()

try:
    sor = db.execute("select * from meta").fetchall()
    epites = next((r[1] for r in sor if r[0] == 'epites_ts'), '')
except sqlite3.OperationalError:
    epites = ''

konyvek = [(k, so, nev) for k, so, _, nev, _ in q("select * from konyv order by sorrend")]

# versek, amelyekben a H7121 előfordul (macula: alak + morf + LXX)
tok = defaultdict(list)
for ih, sz, szo, morf, lxx, lxxs in q("select igehely,sorszam,szo,morf,lxx_szo,lxx_strong from token_macula where strong=? order by igehely,sorszam", S):
    tok[ih].append({'h': szo, 'm': morf or '', 'g': lxx or '', 'gs': lxxs or ''})

versek = {ih: (k, f, v, so, t) for ih, k, f, v, so, t in q(
    "select igehely,konyv,fejezet,vers,sorrend,karoli_szoveg from vers where igehely in (select igehely from token_macula where strong=?)", S)}

par = defaultdict(list)
for ih, hs, hu, biz in q("select igehely,hu_sorszam,hu_szo,bizonyossag from token_par where strong=? order by igehely,hu_sorszam", S):
    par[ih].append([hs, hu, biz])

nev = {ih for (ih,) in q("select distinct igehely from token_strong where strong='H8034' and igehely in (select igehely from token_strong where strong=?)", S)}
par_konyvek = {r[0] for r in q("select distinct substr(igehely,1,instr(igehely,' ')-1) from token_par")}

sorok = []
for ih, tl in tok.items():
    if ih not in versek:
        print('vers nélkül:', ih); continue
    k, f, v, so, t = versek[ih]
    sorok.append({'r': ih, 'k': k, 'o': so, 't': t, 'tok': tl, 'p': par.get(ih, []),
                  'n': ih in nev, 'pk': k in par_konyvek})
sorok.sort(key=lambda r: r['o'])

# Károli-alakok (token_par), bizonyosság szerint
alak = Counter(); alak_m = Counter()
for hu, biz in q("select hu_szo_kis,bizonyossag from token_par where strong=?", S):
    alak[hu] += 1
    if biz == 'magas':
        alak_m[hu] += 1

# kollokáció (strong_parok), a nyelvtani Strong-számok nélkül
gram = {r[0] for r in q("select strong from grammatikai_strongok")}
koll = []
for a, b, n in q("select a,b,n from strong_parok where a=? or b=? order by n desc", S, S):
    m = b if a == S else a
    if m in gram:
        continue
    sz = q("select szoto, jelentes from strong_szotar where strong=? or strong_szam=? limit 1", m, m)
    koll.append([m, n, sz[0][0] if sz else '', (sz[0][1] or '')[:40] if sz else ''])
    if len(koll) >= 12:
        break

# párhuzam: Jóel 2:32 – LXX – Róm 10:13, ApCsel 2:21
def vers_szoveg(ih):
    r = q("select karoli_szoveg from vers where igehely=?", ih)
    return r[0][0] if r else ''
lxx = q("select szoalak, strong from lxx_token where karoli_igehely='Jóel 2:32' order by pozicio")
usz = {ih: q("select alak, strong_lanc from token_eredeti where igehely=? order by sorszam", ih) for ih in ('ApCsel 2:21', 'Róm 10:13')}
heb = q("select szo, strong, morf from token_macula where igehely='Jóel 2:32' order by sorszam")
parh = {'heb': heb, 'lxx': lxx, 'usz': usz,
        'karoli': {ih: vers_szoveg(ih) for ih in ('Jóel 2:32', 'ApCsel 2:21', 'Róm 10:13')}}

ki = {'strong': S, 'epites': epites, 'konyvek': konyvek, 'sorok': sorok,
      'alak': alak.most_common(), 'alak_m': dict(alak_m), 'koll': koll, 'parh': parh,
      'par_konyvek': sorted(par_konyvek), 'ures': len(tok.get('', []))}
print('usz minta', usz['Róm 10:13'][:5], 'lxx minta', lxx[:4])
json.dump(ki, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
print('versek', len(sorok), 'tokenek', sum(len(r['tok']) for r in sorok), 'névvel', sum(r['n'] for r in sorok))
print('párosított vers', sum(1 for r in sorok if r['p']), 'alakok', len(alak), sum(alak.values()))
print('koll', koll)
print('stem', Counter(t['m'][1:2] for r in sorok for t in r['tok']))
print('ragozas', Counter(t['m'][2:3] for r in sorok for t in r['tok']))
print('lxx', Counter(t['gs'] for r in sorok for t in r['tok']).most_common(8))
print('epites', epites, 'usz', {k: len(v) for k, v in usz.items()}, 'lxx', len(lxx))
