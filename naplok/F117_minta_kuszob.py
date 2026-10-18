"""F117 4.2: a kis minta (naplok/F117_szoveg_osszevetes.tsv) küszöb-változatainak számlálása a DT-F117b-hez. Csak olvas."""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# A mintaszámok (naplok/F117_minta.md, DT-F117b) a 33abc45a állapotú F117_szoveg_osszevetes.tsv-ből jönnek; reprodukálás:
#   git show 33abc45a:naplok/F117_szoveg_osszevetes.tsv > minta.tsv && python naplok/F117_minta_kuszob.py minta.tsv
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'naplok', 'F117_szoveg_osszevetes.tsv')

with open(P, encoding='utf-8') as f:
    adat = [s.rstrip('\n').split('\t') for s in f if not s.startswith('#')]
fej, sorok = adat[0], adat[1:]
ix = {n: i for i, n in enumerate(fej)}


def margo(s):
    m = re.search(r'margo=([+-]\d+\.\d+)', s)
    return float(m.group(1)) if m else None


n = len(sorok)
egyezik = sum(1 for s in sorok if s[ix['elteres']] == 'egyezik')
sz_te = sum(1 for s in sorok if s[ix['kjv_szoveg']] == s[ix['kjv_teljes']])
m = [margo(s[ix['masodik_legjobb']]) for s in sorok]
s_sz = [float(s[ix['s_szoveg']]) for s in sorok]
ta = [float(s[ix['tahot']]) for s in sorok]
print('n=%d | ítélettel egyezik: %d | szöveg-igazítás = teljes igazítás: %d' % (n, egyezik, sz_te))
print('lépések:', sorted({s[ix['dontesi_ok']] for s in sorok}))
print('margó < 0: %d | margó < 0,05: %d | margó < 0,10: %d' % (
    sum(1 for x in m if x is not None and x < 0), sum(1 for x in m if x is not None and x < 0.05),
    sum(1 for x in m if x is not None and x < 0.10)))
print('s_szoveg < 0,50: %d | < 0,60: %d' % (sum(1 for x in s_sz if x < 0.5), sum(1 for x in s_sz if x < 0.6)))
for kus_s, kus_m in ((0.5, 0.05), (0.5, 0.0), (0.4, 0.0)):
    b = [s[0] for s, x, y in zip(sorok, s_sz, m) if x < kus_s or (y is not None and y < kus_m)]
    print('verszintű küszöb s_szoveg>=%.2f és margó>=%.2f: bizonytalan %d / %d' % (kus_s, kus_m, len(b), n))
print('TAHOT-Jaccard a választott páron: min %.2f, medián %.2f' % (min(ta), sorted(ta)[len(ta) // 2]))
horgony = {}
for s in sorok:
    fj = s[0].rsplit(':', 1)[0]
    h = horgony.setdefault(fj, [0, 0])
    h[1] += 1
    if s[ix['nev']] == '1.00' or s[ix['elso_utolso']] == '2':
        h[0] += 1
print('horgony-vers (nev=1 vagy elso_utolso=2) fejezetenként:', {k: '%d/%d' % tuple(v) for k, v in horgony.items()})
