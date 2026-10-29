"""ISTENTISZT-001 arany lap, 2026-10-29 (DONTESEK: a „teljes” menet 3. pontja): a `hu_illeszt.py` siglum-szabályának (4) hatása, a tábla elavultságától elválasztva.

Csak olvas, nem ír táblát. Ugyanazzal a mai bemenettel kétszer generál: a (4) szabály nélkül (a `SIGLUM_ELOTT` soha nem
illeszkedik) és vele, majd Strongonként összeveti a két kimenetet. Kiírja az érintett Strongok számát, soronként a változott
kategóriákat, és Strongonként egy mintát (a változott sorok régi/új magyar szakaszának eleje). A tábla elavultságát
(a repóbeli `bdb_szakasz_hu.tsv` és a mai bemenet különbsége) külön számolja. split('\t').
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
uj = hi.general(TS)[0]
eredeti = hi.SIGLUM_ELOTT
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
for st, v in sorted(valtozott.items()):
    print('\n==', st, len(v), 'sor')
    for r, u in v:
        print('  %s %s %s → %s | régi: %r | új: %r' % (r[1], r[5], r[7], u[7], r[11][:70], u[11][:70]))

# a tábla elavultsága (a (4) szabálytól független)
with open(hi.KI_UT, encoding='utf-8', newline='') as f:
    tabla = [x.rstrip('\r').split('\t') for x in f.read().split('\n')[3:] if x.strip()]
t_st = {r[0] for r in tabla}
print('\nrepóbeli tábla: %d Strong, %d sor; a mai bemenet: %d Strong, %d sor'
      % (len(t_st), len(tabla), len({r[0] for r in regi}), len(regi)))
regi_k = {(r[0], r[1]): r[:13] for r in regi}
elteres = {r[0] for r in tabla if regi_k.get((r[0], r[1])) != r[:13]}
print('a repóbeli tábla Strongjai közül a mai bemenettel (szabály nélkül) eltér: %d' % len(elteres))
