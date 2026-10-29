"""ISTENTISZT-001: a próza számszerű állításainak újramérése az Ézs 64:6 beépítése után.

Az elofordulasok.tsv ISTENTISZT-001 sorainak száma (ÓSZ/ÚSZ), és a kísérő szavak
(H3034, H4196, H3444, H3563, H5375, H3045, H5971, H1471) helyei az ószövetségi
sorok TAHOT-kulcsán (Károli-vers). split('\t'), csak olvas. Napló:
naplok/ISTENTISZT001_ezs64_zsolt99_naplo.md.
"""
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
UJSZ = {'Mt', 'Mk', 'Lk', 'Luk', 'Jn', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef',
        'Fil', 'Kol', '1Thessz', '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak',
        '1Pét', '2Pét', '1Ján', '2Ján', '3Ján', 'Júd', 'Jel'}
KISERO = ['H3034', 'H4196', 'H3444', 'H3563', 'H5375', 'H3045', 'H5971', 'H1471']


def tabla(ut):
    with open(ut, encoding='utf-8') as f:
        fej = None
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            yield dict(zip(fej, m))


helyek = [d['igehely'] for d in tabla('adat/elofordulasok.tsv') if d['id'] == ID]
osz = [h for h in helyek if h.split()[0] not in UJSZ]
usz = [h for h in helyek if h.split()[0] in UJSZ]
print(f'ISTENTISZT-001: {len(helyek)} hely, ÓSZ {len(osz)}, ÚSZ {len(usz)}')

strongok = {h: set() for h in osz}
with open('konkordancia/TAHOT_kivonat.tsv', encoding='utf-8') as f:
    next(f)
    for sor in f:
        m = sor.rstrip('\n').split('\t')
        if m[0] in strongok:
            strongok[m[0]].add(m[1])
hianyzo = [h for h, s in strongok.items() if not s]
print('TAHOT-sor nélküli ÓSZ-hely:', hianyzo or 'nincs')
for s in KISERO:
    print(s, sorted(h for h in osz if s in strongok[h]))
print('Ézs 64:6 kísérő szavai:', sorted(set(KISERO) & strongok.get('Ézs 64:6', set())) or 'egyik sem')
ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
print(f'proveniencia: scope=adat/elofordulasok.tsv (id={ID}, n={len(helyek)}) | '
      f'forras=TAHOT_kivonat.tsv (naplok/ISTENTISZT001_ezs64_zsolt99_meres.py, split(\'\\t\')) | ts={ts}')
