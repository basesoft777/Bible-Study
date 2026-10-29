"""ISTENTISZT-001 arany lap, 2026-10-29 (DONTESEK: a „teljes” menet 3. pontja): a `hu_illeszt.py` siglum-szabályának (4) hatása, a tábla elavultságától elválasztva.

Csak olvas, nem ír táblát. Ugyanazzal a mai bemenettel kétszer generál: a (4) szabály nélkül (a `SIGLUM_ELOTT` soha nem
illeszkedik) és vele, majd Strongonként összeveti a két kimenetet. Kiírja az érintett Strongok számát, soronként a változott
kategóriákat, és Strongonként egy mintát (a változott sorok régi/új magyar szakaszának eleje). A tábla elavultságát
(a repóbeli `bdb_szakasz_hu.tsv` és a mai bemenet különbsége, szabály nélkül) külön számolja: Strong, mezőszintű sorszám,
és hogy a H7121 / H8034 érintett-e. A `--tag` az első, elvetett változat (`^` + bármely siglum), a `--betus` a második,
elvetett változat (`^` + betűs vagy §-os siglum) hatását méri, a rontások (`illeszkedik` → `elakad`) felsorolásával.
split('\t').
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

TS = '2026-10-18'
VALTOZAT = {'--tag': r'\^[^\s^]+\s?$',                    # az első, elvetett változat
            '--betus': r'\^[A-Za-zÀ-ž§]+\.?\s?$'}          # a második, elvetett változat
TAG = next((a for a in sys.argv[1:] if a in VALTOZAT), None)
eredeti = hi.SIGLUM_ELOTT
if TAG:
    hi.SIGLUM_ELOTT = re.compile(VALTOZAT[TAG])
print('változat:', hi.SIGLUM_ELOTT.pattern)
uj = hi.general(TS)[0]
hi.SIGLUM_ELOTT = re.compile(r'(?!)')
regi = hi.general(TS)[0]
hi.SIGLUM_ELOTT = eredeti
assert [r[:2] for r in regi] == [r[:2] for r in uj]

valtozott = collections.defaultdict(list)
for r, u in zip(regi, uj):
    if r != u:
        valtozott[r[0]].append((r, u))
print('Strong a mai bemenettel: %d; a (4) szabálytól változó Strong: %d; sor: %d'
      % (len({r[0] for r in uj}), len(valtozott), sum(len(v) for v in valtozott.values())))
kat = collections.Counter((r[7], u[7]) for v in valtozott.values() for r, u in v)
print('kategória (régi → új):', dict(kat))
print('rontás (illeszkedik → elakad): %d sor, %s' % (
    kat[('illeszkedik', 'elakad')],
    sorted({st for st, v in valtozott.items() for r, u in v if (r[7], u[7]) == ('illeszkedik', 'elakad')})))
if TAG:
    raise SystemExit
for st, v in sorted(valtozott.items()):
    print('\n==', st, len(v), 'sor')
    for r, u in v:
        print('  %s %s %s → %s | régi: %r | új: %r' % (r[1], r[5], r[7], u[7], r[11][:70], u[11][:70]))

# a tábla elavultsága (a (4) szabálytól független)
with open(hi.KI_UT, encoding='utf-8', newline='') as f:
    tabla = [x.rstrip('\r').split('\t') for x in f.read().split('\n')[3:] if x.strip()]
t_st = {r[0] for r in tabla}
print('\nrepóbeli tábla: %d Strong, %d sor; a mai bemenet: %d Strong, %d sor; új Strong: %d'
      % (len(t_st), len(tabla), len({r[0] for r in regi}), len(regi), len({r[0] for r in regi} - t_st)))
regi_k = {(r[0], r[1]): r[:13] for r in regi}
elteres, mezo = set(), collections.Counter()
for r in tabla:
    u = regi_k.get((r[0], r[1]))
    if u != r[:13]:
        elteres.add(r[0])
        if u is None:
            mezo['nincs a mai kimenetben'] += 1
        else:
            for i, n in enumerate(hi.FEJLEC[:13]):
                if u[i] != r[i]:
                    mezo[n] += 1
print('a repóbeli tábla Strongjai közül a mai bemenettel (szabály nélkül) eltér: %d' % len(elteres))
print('eltérő mezők (sor):', dict(mezo))
print('H7121 érintett: %s; H8034 érintett: %s' % ('H7121' in elteres, 'H8034' in elteres))
