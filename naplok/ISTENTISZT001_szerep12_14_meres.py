"""ISTENTISZT-001 arany lap, „teljes” menet (2026-10-29): a 12–14. szerep forrásainak lefedettsége.

Csak olvas. (12) Nave: hány Nave-téma hivatkozik a motívum igehelyeire; (13) Károli–Strong párosítás: mely
könyvekhez van `szavak_<könyv>.tsv`, mely motívumhelyek könyve hiányzik, és a H7121/H8034/G1941 Károli-alakjai a
meglévő könyvekben (bizonyosság szerint). split('\t').
"""
import collections
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


_, elo = olvas('adat/elofordulasok.tsv')
helyek = [r['igehely'] for r in elo if r['id'] == 'ISTENTISZT-001']
print('motívumhelyek:', len(helyek))

# (12) Nave
fej, nave = olvas('konkordancia/Nave_basokant.tsv')
print('\n(12) Nave fejléc:', fej, '| sorok:', len(nave))
vers_mezo = next((m for m in fej if 'igehely' in m.lower() or 'vers' in m.lower()), None)
tema_mezo = next((m for m in fej if 'tema' in m.lower() or 'topic' in m.lower() or 'cim' in m.lower()), fej[0])
print('vers-mező:', vers_mezo, '| téma-mező:', tema_mezo)
if vers_mezo:
    hely_set = set(helyek)
    talalt = collections.defaultdict(set)
    for r in nave:
        if r.get(vers_mezo) in hely_set:
            talalt[r[tema_mezo]].add(r[vers_mezo])
    lefedett = set().union(*talalt.values()) if talalt else set()
    print(f'Nave-témák a motívumhelyeken: {len(talalt)}; lefedett hely: {len(lefedett)}/{len(hely_set)}')
    for t, v in sorted(talalt.items(), key=lambda x: -len(x[1]))[:15]:
        print(f'  {len(v):3}  {t}')

# (13) Károli–Strong
konyvek = sorted(f[len('szavak_'):-4] for f in os.listdir('adat/karoli_strong') if f.startswith('szavak_'))
print('\n(13) szavak_<könyv>.tsv:', len(konyvek))
NORM = str.maketrans('áéíóöőúüűÁÉÍÓÖŐÚÜŰ', 'aeiooouuuAEIOOOUUU')
hianyzo = sorted({h.rsplit(' ', 1)[0] for h in helyek if h.rsplit(' ', 1)[0].translate(NORM) not in konyvek})
print('motívumhely könyve, párosítás nélkül:', hianyzo,
      [h for h in helyek if h.rsplit(' ', 1)[0] in hianyzo])
alak = collections.defaultdict(collections.Counter)
for k in konyvek:
    fej, sorok = olvas(f'adat/karoli_strong/szavak_{k}.tsv')
    for r in sorok:
        st = r.get('strong', '')
        for cel in ('H7121', 'H8034', 'G1941'):
            if r.get('oldal') == 'hu' and cel in st.split('+'):
                alak[cel][(r['szo'].lower(), r.get('bizonyossag', ''))] += 1
for cel, c in alak.items():
    ossz = sum(c.values())
    biz = collections.Counter()
    for (sz, b), n in c.items():
        biz[b] += n
    print(f'{cel}: {ossz} Károli-token; bizonyosság: {dict(biz)}; leggyakoribb: '
          + ', '.join(f'{sz} ({n})' for (sz, _b), n in c.most_common(8)))
