"""A `bdb_szakasz_hu.tsv` frissítésének összevetése (ISTENTISZT-001 arany, N-F131f; 2026-10-29).

Csak olvas. A régi tábla a git `--alap` revíziójából (alapértelmezés: HEAD), az új a munkapéldányból. A `proveniencia`
(a `ts`) nélkül vet össze. Kiírja:
  1. az összesítőt (régi / új Strong és sor, új Strongok, eltérő meglévő Strongok);
  2. a meglévő, eltérő Strongokat soronként: mely mező változott, a kategória régi → új, és az OK-ot:
     `forditas` (a `forditas_forras_hash` változott: a magyar fordítás maga új), `illesztes` (azonos fordítás, más
     szakaszhatár: az illesztő szabályai változtak a régi generálás óta), `szerkezet` (a sor a szakasztáblában más);
  3. a rontás-jelölteket: `illeszkedik` → `elakad` / `horgonnyal`, `horgonnyal` → `elakad`, vagy a nem üres `szoveg_hu`
     üressé válása (a `jelolo_nelkul` sorok kivételével);
  4. a `--minta N --mag M` kapcsolóval N véletlen új Strongot (rögzített maggal), soronként a kategóriával és a magyar
     szakasz elejével, az angol szakasz (bdb_szakaszok.tsv) elejével párban.
split('\\t'); a '\\r' levágva.
"""
import argparse
import collections
import random
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UT = 'adat/bdb_szakasz_hu.tsv'
MEZOK = ['strong', 'sorszam', 'bdb_id', 'szakasz', 'resz', 'utvonal', 'jel', 'kategoria', 'horgony', 'hu_kezdet', 'hu_hossz',
         'szoveg_hu', 'forditas_forras_hash']


def tabla(szoveg):
    sorok = [x.rstrip('\r') for x in szoveg.split('\n')]
    sorok = [x for x in sorok if x and not x.startswith('#')]
    fej = sorok[0].split('\t')
    d = collections.OrderedDict()
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        d[(r['strong'], r['sorszam'])] = r
    return d


ap = argparse.ArgumentParser()
ap.add_argument('--alap', default='HEAD')
ap.add_argument('--minta', type=int, default=0)
ap.add_argument('--mag', type=int, default=20261029)
ap.add_argument('--strong', default='', help='csak ezek a Strongok (vesszővel) a 2. pontban')
a = ap.parse_args()

regi = tabla(subprocess.run(['git', 'show', '%s:%s' % (a.alap, UT)], capture_output=True, encoding='utf-8').stdout)
with open(UT, encoding='utf-8', newline='') as f:
    uj = tabla(f.read())

r_st = collections.OrderedDict()
for k in regi:
    r_st.setdefault(k[0], []).append(k)
u_st = collections.OrderedDict()
for k in uj:
    u_st.setdefault(k[0], []).append(k)
uj_strong = [s for s in u_st if s not in r_st]
eltunt = [s for s in r_st if s not in u_st]
print('régi: %d Strong, %d sor; új: %d Strong, %d sor; új Strong: %d; eltűnt Strong: %d %s'
      % (len(r_st), len(regi), len(u_st), len(uj), len(uj_strong), len(eltunt), eltunt))

elteres = collections.OrderedDict()
for st, kulcsok in r_st.items():
    if st not in u_st:
        continue
    if [k for k in kulcsok] != u_st[st]:
        elteres[st] = [('sorlista', None, None)]
        continue
    v = []
    for k in kulcsok:
        ro, un = regi[k], uj[k]
        mez = [m for m in MEZOK if ro.get(m) != un.get(m)]
        if mez:
            v.append((k[1], mez, (ro, un)))
    if v:
        elteres[st] = v
print('eltérő meglévő Strong: %d' % len(elteres))

ok_szaml = collections.Counter()
mezo_szaml = collections.Counter()
rontas = []
szukit = set(a.strong.split(',')) if a.strong else None
print('\n== a meglévő, eltérő Strongok ==')
for st, v in elteres.items():
    if v[0][0] == 'sorlista':
        ok_szaml['szerkezet'] += 1
        print('%s  szerkezet: a sorlista más' % st)
        continue
    hash_valt = any('forditas_forras_hash' in m for _, m, _ in v)
    ok = 'forditas' if hash_valt else 'illesztes'
    ok_szaml[ok] += 1
    kat = collections.Counter()
    for sorszam, mez, (ro, un) in v:
        for m in mez:
            mezo_szaml[m] += 1
        if ro['kategoria'] != un['kategoria']:
            kat[(ro['kategoria'], un['kategoria'])] += 1
        romlik = ((ro['kategoria'], un['kategoria']) in (('illeszkedik', 'elakad'), ('illeszkedik', 'horgonnyal'),
                                                          ('horgonnyal', 'elakad'))
                  or (ro['szoveg_hu'] and not un['szoveg_hu'] and un['kategoria'] != 'jelolo_nelkul'))
        if romlik:
            rontas.append((st, sorszam, ro, un, ok))
    print('%s  %-9s  %2d sor  mezők: %s  kategória: %s' % (
        st, ok, len(v), ','.join(sorted({m for _, mz, _ in v for m in mz if m != 'forditas_forras_hash'})) or '-',
        dict(kat) or '-'))
    if szukit and st in szukit:
        for sorszam, mez, (ro, un) in v:
            print('    %s %s %s → %s | régi: %r\n%s| új:   %r' % (sorszam, ro['utvonal'], ro['kategoria'], un['kategoria'],
                                                            ro['szoveg_hu'][:100], ' ' * 26, un['szoveg_hu'][:100]))
print('\nok szerint:', dict(ok_szaml))
print('mezők (sor):', dict(mezo_szaml))
print('\n== rontás-jelöltek: %d sor ==' % len(rontas))
for st, sorszam, ro, un, ok in rontas:
    print('%s %s %s (%s): %s → %s | régi: %r | új: %r' % (st, sorszam, ro['utvonal'], ok, ro['kategoria'],
                                                          un['kategoria'], ro['szoveg_hu'][:70], un['szoveg_hu'][:70]))

if a.minta:
    angol = {}
    with open('adat/bdb_szakaszok.tsv', encoding='utf-8', newline='') as f:
        sorok = [x.rstrip('\r') for x in f.read().split('\n')]
    sorok = [x for x in sorok if x and not x.startswith('#')]
    fej = sorok[0].split('\t')
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        angol[(r['strong'], r['sorszam'])] = r
    minta = sorted(random.Random(a.mag).sample(uj_strong, a.minta))
    print('\n== %d véletlen új Strong (mag: %d) ==' % (a.minta, a.mag))
    kat_ossz = collections.Counter()
    for st in minta:
        sorok = [uj[k] for k in u_st[st]]
        k = collections.Counter(r['kategoria'] for r in sorok)
        kat_ossz.update(k)
        print('\n%s  %d sor  %s' % (st, len(sorok), dict(k)))
        for r in sorok:
            e = angol.get((r['strong'], r['sorszam']), {})
            print('  %s %-12s %-13s EN: %-60.60s | HU: %.60s' % (r['sorszam'], r['utvonal'], r['kategoria'],
                                                                e.get('jel', '') + ' ' + e.get('szoveg', ''),
                                                                r['szoveg_hu']))
    print('\na minta kategóriái:', dict(kat_ossz))
