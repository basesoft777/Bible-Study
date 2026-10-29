"""A szakaszonként fordított BDB-Strongok illesztésének mérése (ISTENTISZT-001 arany, BDB-frissítés, 2026-10-29; a NYITOTT
csoporthatár-alapú illesztés tételének számai).

Csak olvas, nem ír táblát. A mai bemenettel a memóriában generál (`hu_illeszt.general`, a mai kód), és kiírja:
  1. a szakaszonként fordított (a `forditasok.tsv` BDB-sorai között `sz<n>` jelentésszám) és az egyben fordított Strongok
     számát, az `elakad` sort tartalmazó Strongokat és a kategóriánkénti sorszámot;
  2. a nyelvtani személyt jelölőnek vevő sorokat (`illeszkedik` / `horgonnyal`, a magyar szakasz „<szám>. egyes szám |
     többes szám | kettős szám | hímnemű | nőnemű”-vel kezdődik, az angol nem „[<szám>] singular | plural | dual | masculine |
     feminine”-nel) a repóbeli táblában és a mai generálásban;
  3. a valódi szakaszfejet (az angol `jel` szám, a szöveg nyelvtani szóval kezdődik) a mai generálásban.
split('\\t'); a '\\r' levágva.
"""
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ITT, '..', 'eszkozok', 'bdb_jelolt'))
sys.path.insert(0, os.path.join(ITT, '..', 'eszkozok'))
import hu_illeszt as hi  # noqa: E402

HU_SZEMELY = re.compile(r'^\d{1,2}\.\s+(?:egyes szám|többes szám|kettős szám|hímnemű|nőnemű)')
EN_SZEMELY = re.compile(r'^\s*(?:\d+\s*)?(?:singular|plural|dual|masculine|feminine)', re.I)


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]


ford = olvas(hi.FORD)
fej = ford[0].split('\t')
szakaszos = set()
for s in ford[1:]:
    d = dict(zip(fej, s.split('\t')))
    if d['szotar'] == 'BDB' and d['jelentes_szam'].startswith('sz'):
        szakaszos.add('H%04d' % int(re.sub(r'\D', '', d['strong'])))

angol = {}
t = olvas(hi.TABLA)
fej = t[0].split('\t')
for s in t[1:]:
    r = dict(zip(fej, s.split('\t')))
    angol[(r['strong'], r['sorszam'])] = r

mai = hi.general('2026-10-29')[0]
kat = collections.defaultdict(collections.Counter)
for r in mai:
    kat[r[0]][r[7]] += 1
print('== 1. a mai generálás (%d Strong, %d sor) ==' % (len(kat), len(mai)))
for nev, h in (('szakaszonként fordított', [s for s in kat if s in szakaszos]),
               ('egyben fordított', [s for s in kat if s not in szakaszos])):
    sk = collections.Counter()
    for s in h:
        sk.update(kat[s])
    print('%s: %d Strong; elakad-sort tartalmaz: %d; sorok: %s'
          % (nev, len(h), sum(1 for s in h if kat[s]['elakad']), dict(sk)))


def szemely(sorok):
    return [(r[0], r[1]) for r in sorok if r[7] in ('illeszkedik', 'horgonnyal') and HU_SZEMELY.match(r[11])
            and not EN_SZEMELY.match(angol.get((r[0], r[1]), {}).get('szoveg', ''))]


repo = [x.split('\t') for x in olvas(hi.KI_UT)[1:]]
print('\n== 2. nyelvtani személy jelölőnek véve ==')
for nev, sorok in (('a repóbeli tábla', repo), ('a mai generálás', mai)):
    sz = szemely(sorok)
    print('%s: %d sor, %d Strong' % (nev, len(sz), len({x[0] for x in sz})))

valodi = [r for r in mai if re.fullmatch(r'\d+\.?', angol.get((r[0], r[1]), {}).get('jel', '') or '')
          and EN_SZEMELY.match(angol[(r[0], r[1])]['szoveg'])]
print('\n== 3. valódi szakaszfej (szám + nyelvtani szó), a mai generálás: %d sor ==' % len(valodi))
