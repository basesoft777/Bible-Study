"""F239 U3 — a próza számai az adatból (csak olvas): Károli-alakok, csoportos kizárások, könyvek, TR/kritikai.
Futtatás: python naplok/F239_U3_proza_szamok.py"""
import sys, os, re, collections
sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def tsv(ut):
    fej = None
    for s in open(os.path.join(GY, ut), encoding='utf-8'):
        s = s.rstrip('\r\n')
        if not s or s.startswith('#'): continue
        m = s.split('\t')
        if fej is None: fej = m; continue
        yield dict(zip(fej, m + [''] * (len(fej) - len(m))))
elo = [r for r in tsv('adat/elofordulasok.tsv') if r['id'] == 'TEREMT-001']
konyv = collections.Counter()
for r in elo:
    k = r['igehely'].rsplit(' ', 1)[0]
    v = r['igehely'].rsplit(':', 1)[1]
    n = (int(v.split('-')[1]) - int(v.split('-')[0]) + 1) if '-' in v else 1
    konyv[k] += n
print('könyvenként (vers):', dict(konyv))
ksz = [r['karoli_szo'] for r in elo]
print('karoli_szo mélység-alak:', sum('mélység' in k.lower() for k in ksz), '/', len(ksz))
print('nem mélység-alak:', [(r['igehely'], r['karoli_szo']) for r in elo if 'mélység' not in r['karoli_szo'].lower()])
jel = [r for r in tsv('adat/jeloltek.tsv') if r['id'] == 'TEREMT-001' and r['jelolt_tipus'] == 'elofordulas' and r['dontes'] == 'elutasítva']
cs = 0; egyen = 0
for r in jel:
    m = re.match(r'Összesítő sor (\d+) versre', r['indoklas'])
    if m: cs += int(m.group(1))
    else: egyen += 1
print('elutasítva sor:', len(jel), '· csoportos versek:', cs, '· egyenkénti sor:', egyen)
# TR / kritikai a G0012-tokeneken
for r in tsv('konkordancia/TAGNT_kivonat.tsv'):
    if r['Strong-szám'] == 'G0012':
        print('G0012', r['Igehely'], r['Ragozott alak'], r['Kritikai kiadás'])
