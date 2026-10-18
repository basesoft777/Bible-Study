"""A változatok többletadata (csak olvasás): a kereszthivatkozások célverseinek szövege és a TIPNR-nevek összesítése."""
import sys, os, json, re, sqlite3, unicodedata
from collections import Counter, defaultdict
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'C:/Users/bases/Desktop/Bible-Study'
d = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))
db = sqlite3.connect(f'file:{ROOT}/pardes.db?mode=ro', uri=True)

def ascii_(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
slug_kk = {ascii_(kk): kk for (kk,) in db.execute("select kk_kod from konyv")}

def blokk(h, b):
    m = re.search(r'<section class="blokk" id="b-%s"[^>]*>(.*?)</section>' % b.replace('.', '-'), h, re.S)
    return m.group(1) if m else ''

hrefek = set()
tipnr_strong = set()
for v, h in E['versek'].items():
    for b in ('vers.kh', 'vers.tsk', 'vers.nave'):
        hrefek.update(re.findall(r'href="(/[^"/?#]+/\d+/\d+)"', blokk(h, b)))
    tipnr_strong.update(re.findall(r'/szo/(H\d+[A-Za-z]?)', blokk(h, 'vers.tipnr')))

kh = {}
hiany = []
for hr in sorted(hrefek):
    _, slug, f, v = hr.split('/')
    kk = slug_kk.get(slug)
    r = db.execute("select igehely, karoli_szoveg from vers where konyv=? and fejezet=? and vers=?", (kk, int(f), int(v))).fetchone() if kk else None
    if r:
        kh[hr] = [r[0], r[1]]
    else:
        hiany.append(hr)

# TIPNR: a fejezet neveinek teljes-bibliai összesítése (STEP-alakból magyar igehelyre)
norm = {}
with open(f'{ROOT}/konkordancia/Konyv_normalizalo_tabla.tsv', encoding='utf-8') as f:
    next(f)
    for s in f:
        m = s.rstrip('\n').split('\t')
        norm[m[0]] = (m[1], m[2])
gyujt = defaultdict(list)
nevek = {}
with open(f'{ROOT}/konkordancia/TIPNR_kivonat.tsv', encoding='utf-8') as f:
    next(f)
    for s in f:
        m = s.rstrip('\n').split('\t')
        alap = re.match(r'H\d+', m[2])
        if not alap or alap.group(0) not in tipnr_strong:
            continue
        k = alap.group(0)
        nevek.setdefault(k, Counter())[m[1]] += 1   # a névváltozat (a normalizált név a Jákóbot is „Israel”-nek írja)
        st = m[4].split('.')
        if len(st) == 3 and st[0] in norm:
            gyujt[k].append((norm[st[0]][0], int(st[1]), int(st[2])))
sorrend = {kk: i for i, (kk,) in enumerate(db.execute("select kk_kod from konyv order by sorrend"))}
tipnr = {}
for k, hl in gyujt.items():
    egyedi = sorted(set(hl), key=lambda x: (sorrend.get(x[0], 99), x[1], x[2]))
    kc = Counter(x[0] for x in egyedi)
    tipnr[k] = {'nev': nevek[k].most_common(1)[0][0], 'db': len(egyedi), 'elso': '%s %d:%d' % egyedi[0] if egyedi else '',
                'konyvek': kc.most_common(6)}
json.dump({'kh': kh, 'tipnr': tipnr}, open(os.path.join(d, 'vadat.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('KH-célok', len(hrefek), 'szöveggel', len(kh), 'hiány', hiany[:10])
print('TIPNR', {k: (v['nev'], v['db'], v['elso'], v['konyvek'][:3]) for k, v in tipnr.items()})
