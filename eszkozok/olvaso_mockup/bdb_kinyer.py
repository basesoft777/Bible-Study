"""A H7121 BDB-jelentésszerkezete az éles szeletelővel, jelentésenként az idézett igehelyekkel (csak olvasás)."""
import sys, os, json, re, sqlite3

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SZ = r'C:\Users\bases\Desktop\Bible-Study\eszkozok\olvaso_szerver'
sys.path.insert(0, SZ)
import bdb_szelet  # noqa: E402

S = 'H7121'
db = sqlite3.connect('file:C:/Users/bases/Desktop/Bible-Study/pardes.db?mode=ro', uri=True)
hu = None
for (t,) in db.execute("SELECT forditas_hu FROM forditasok WHERE szotar='BDB' AND strong=? ORDER BY rowid", (S,)):
    if t and t.strip():
        hu = t.replace('\\n', '\n')
lemma = db.execute("select szoto from strong_szotar where strong=? or strong_szam=? limit 1", (S, S)).fetchone()[0]
r = bdb_szelet.szeletel(hu, lemma)
print('kulcsok', list(r.keys()))

def refek(szoveg):
    ki = []
    for h in bdb_szelet.hivatkozasok(szoveg):
        if h['okkod'] in ('', 'sigla_kozel') and h['konyv']:
            ki.append(f"{h['konyv']} {h['c']}:{h['v']}")
    return ki

def cimke(s):
    s = re.sub(r'\s+', ' ', s).strip(' —;:,.')
    s = re.split(r'[:;(]|\s—\s', s)[0].strip(' ,.')
    return s[:70]

# a hivatkozásokat a teljes szövegen oldjuk fel (öröklött könyvnév), és a csomópont-sávokhoz rendeljük
# a hivatkozás-feloldó az angol (eredeti) szócikk rövidítéseit ismeri: a sávok és a hivatkozások az angolból, a címkék a magyarból
en = db.execute('SELECT teljes_szocikk FROM bdb WHERE strong=?', (S,)).fetchone()[0]
r_en = bdb_szelet.szeletel(en, lemma)
savok = bdb_szelet.csomopont_savok(en, r_en)
osszes_h = [h for h in bdb_szelet.hivatkozasok(en) if h['okkod'] in ('', 'sigla_kozel') and h['konyv']]
print('angol utak', sorted({sv[3] for sv in savok})[:40])
ut_refek = {}
for h in osszes_h:
    tal = [sv for sv in savok if sv[0] <= h['poz'] < sv[1]]
    if tal:
        ut = max(tal, key=lambda sv: sv[0])[3]
        ut_refek.setdefault(ut, []).append(f"{h['konyv']} {h['c']}:{h['v']}")

jel = []
def bejar(torzsek, szakasz):
    for t in torzsek:
        for j in t['jelentesek']:
            if not j['jel'] and not j['al']:
                continue
            jp = '%s/%s' % (t['nev'] or '-', j['jel'] or '-')
            al = []
            for a in j['al']:
                al.append({'jel': a['jel'], 'cimke': cimke(a['szoveg']), 'refek': ut_refek.get('%s/%s' % (jp, a['jel']), [])})
            jel.append({'szakasz': szakasz, 'torzs': t['nev'], 'jel': j['jel'], 'cimke': cimke(j['szoveg']),
                        'refek': ut_refek.get(jp, []), 'al': al})

bejar(r['torzsek'], '')
print('hivatkozás összesen', len(osszes_h), 'sávhoz rendelt', sum(len(v) for v in ut_refek.values()))

for j in jel:
    print(j['torzs'], j['jel'], j['cimke'][:50], len(j['refek']), [(a['jel'], a['cimke'][:40], len(a['refek'])) for a in j['al']])

# melyik idézett igehelyen áll ténylegesen H7121 (Károli-kulccsal)
van = {ih for (ih,) in db.execute("select distinct igehely from token_strong where strong=?", (S,))}
osszes = [x for j in jel for x in j['refek'] + [y for a in j['al'] for y in a['refek']]]
talal = [x for x in osszes if x in van]
print('hivatkozás', len(osszes), 'H7121-es versen', len(talal), 'egyedi vers', len(set(talal)))
print('nem talált minta', [x for x in osszes if x not in van][:25])
json.dump({'jel': jel, 'hiv_n': len(osszes), 'talal_n': len(talal)}, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
