"""Egy elvetett (5) személy-szabály hatása a `hu_illeszt.py`-ban (ISTENTISZT-001 arany, BDB-frissítés, 2026-10-29).

A szabály: a „<szám>. egyes szám | többes szám | kettős szám | hímnemű | nőnemű” kezdetű szám nem jelölő. A mérés után
ELVETVE, a kódban nincs: ez a szkript a `magyar_jelolok` köré tett szűrővel próbálja ki. Eredmény (2026-10-29): jelölt 367 sor
(245 Strong), javul 359; rontás-jelölt 100 nem jelölt sor; a valódi szakaszszám + nyelvtani szó 86 sorából 36 változik
(H0173, H0703, H2549 …: „1. nőnemű Ézsau felesége”); a mohó illesztés eltolódik (H4843: a Pi'el 1–2. a Hiph'il 1–2. szövegét
kapja).

Csak olvas, nem ír táblát. A mai bemenettel kétszer generál: a szabály nélkül és vele.
Kiírja:
  1. a régi → új sorszámot és a változó Strongok / sorok számát, kategória-átmenetekkel;
  2. a jelölt sorokat (szabály nélkül: `illeszkedik` / `horgonnyal`, a magyar szakasz „<szám>. egyes szám | többes szám |
     kettős szám | hímnemű | nőnemű”-vel kezdődik, az angol nem „<szám> singular | plural | dual | masculine | feminine”-nel):
     hány javul (a szabállyal nem nyelvtani személlyel kezdődik), ebből hány vált `elakad`-ra (explicit hiány), hány marad;
  3. a rontást: nem jelölt sor, amely `illeszkedik`-ből `elakad`-ra / `horgonnyal`-ra vált, vagy a szövege üressé válik;
  4. a valódi szakaszszámot, amelyet nyelvtani szó követ: az angol sor `jel`-e szám, a szövege nyelvtani szóval kezdődik —
     ezek a szabállyal is maradjanak `illeszkedik`;
  5. a `--strong` Strongjainak sorait szabály nélkül / szabállyal.
split('\\t').
"""
import argparse
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

ap = argparse.ArgumentParser()
ap.add_argument('--strong', default='')
a = ap.parse_args()

HU_SZEMELY = re.compile(r'^\d{1,2}\.\s+(?:egyes szám|többes szám|kettős szám|hímnemű|nőnemű)')
EN_SZEMELY = re.compile(r'^\s*(?:\d+\s*)?(?:singular|plural|dual|masculine|feminine)', re.I)

SZEMELY = re.compile(r'\d{1,2}\.\s+(?:egyes szám|többes szám|kettős szám|hímnemű|nőnemű)')
_eredeti = hi.magyar_jelolok


def _szaballyal(hu):
    return [(p, j) for p, j in _eredeti(hu) if not (j.isdigit() and SZEMELY.match(hu, p))]


TS = '2026-10-29'
regi = hi.general(TS)[0]
hi.magyar_jelolok = _szaballyal
uj = hi.general(TS)[0]
hi.magyar_jelolok = _eredeti
assert [r[:2] for r in regi] == [r[:2] for r in uj]

angol = {}
with open(hi.TABLA, encoding='utf-8', newline='') as f:
    sorok = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
fej = sorok[0].split('\t')
for s in sorok[1:]:
    r = dict(zip(fej, s.split('\t')))
    angol[(r['strong'], r['sorszam'])] = r

valt = [(r, u) for r, u in zip(regi, uj) if r != u]
print('sor: %d → %d; változó Strong: %d, sor: %d' % (len(regi), len(uj), len({r[0] for r, _ in valt}), len(valt)))
print('kategória (szabály nélkül → szabállyal):', dict(collections.Counter((r[7], u[7]) for r, u in valt)))

jelolt = [i for i, r in enumerate(regi) if r[7] in ('illeszkedik', 'horgonnyal') and HU_SZEMELY.match(r[11])
          and not EN_SZEMELY.match(angol.get((r[0], r[1]), {}).get('szoveg', ''))]
javul = [i for i in jelolt if not HU_SZEMELY.match(uj[i][11])]
hianyra = [i for i in javul if uj[i][7] == 'elakad']
marad = [i for i in jelolt if HU_SZEMELY.match(uj[i][11])]
print('\njelölt sor: %d (%d Strong); javul: %d (ebből explicit hiányra, elakad: %d); marad: %d %s'
      % (len(jelolt), len({regi[i][0] for i in jelolt}), len(javul), len(hianyra), len(marad),
         [(regi[i][0], regi[i][1]) for i in marad][:20]))

jset = set(jelolt)
rontas = [(r, u) for i, (r, u) in enumerate(zip(regi, uj)) if i not in jset and r != u and (
    (r[7], u[7]) in (('illeszkedik', 'elakad'), ('illeszkedik', 'horgonnyal'), ('horgonnyal', 'elakad'))
    or (r[11] and not u[11] and u[7] != 'jelolo_nelkul'))]
print('\nrontás-jelölt (nem jelölt sor): %d' % len(rontas))
for r, u in rontas[:40]:
    e = angol.get((r[0], r[1]), {})
    print('  %s %s %s: %s → %s | EN: %.50s | régi: %.60s | új: %.60s' % (r[0], r[1], r[5], r[7], u[7],
                                                                       e.get('jel', '') + ' ' + e.get('szoveg', ''), r[11], u[11]))

valodi = [i for i, r in enumerate(uj) if re.fullmatch(r'\d+\.?', angol.get((r[0], r[1]), {}).get('jel', '') or '')
          and EN_SZEMELY.match(angol[(r[0], r[1])]['szoveg'])]
elveszett = [i for i in valodi if uj[i][7] != regi[i][7] or uj[i][11] != regi[i][11]]
print('\nvalódi szakaszszám + nyelvtani szó (angol `jel` szám, a szöveg nyelvtani szóval kezdődik): %d sor; a szabálytól '
      'változik: %d %s' % (len(valodi), len(elveszett), [(uj[i][0], uj[i][1], regi[i][7], uj[i][7]) for i in elveszett]))

if a.strong:
    for st in a.strong.split(','):
        print('\n==', st)
        for r, u in zip(regi, uj):
            if r[0] == st:
                print('  %s %-12s %s → %s | nélküle: %.60s | vele: %.60s' % (r[1], r[5], r[7], u[7], r[11], u[11]))
