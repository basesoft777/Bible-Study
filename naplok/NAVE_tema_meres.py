"""A 12. szerep (Tematikus index, Nave) mérése egy motívumra (ISTENTISZT-001 arany lap, 2026-10-29) — a jelöltképzés és a
választás adatához. Csak olvas.

A Nave-sor Károli-versei a közös bontási szabállyal (`eszkozok/szerep_nave.nave_sorai` → `eszkozok/nave_bontas.py`, mint az
olvasó `nave_vers` táblája: a KJV-számozású hely a Károli-versek KJV-kulcsa szerint bomlik; a fejezet-szintű hely nem).
Témánként kiírja: hány motívumverset érint (és melyiket), a téma összes (bontott) versének számát, az arányt (motívumvers /
témavers), és a motívumverseket érintő altételeket (`cimke`); a végén a kihagyott forrássorok okonként. split('\\t').

  python naplok/NAVE_tema_meres.py ISTENTISZT-001 [--min 1]
"""
import argparse
import collections
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import szerep_nave as SN  # noqa: E402


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


ap = argparse.ArgumentParser()
ap.add_argument('id')
ap.add_argument('--min', type=int, default=1)
a = ap.parse_args()

motiv = {r['igehely'] for r in olvas(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')) if r['id'] == a.id}
tema_nev, tema_vers = {}, collections.defaultdict(set)
talalat = collections.defaultdict(lambda: collections.defaultdict(set))
for tid, tema, cimke, vs in SN.nave_sorai():
    tema_nev[tid] = tema
    for v in vs:
        tema_vers[tid].add(v)
        if v in motiv:
            talalat[tid][v].add(cimke)

print('motívum: %s, %d igehely; Nave-téma a motívumverseken: %d; lefedett motívumvers: %d'
      % (a.id, len(motiv), len(talalat), len(set().union(*[set(x) for x in talalat.values()]) if talalat else set())))
print('\n%-10s %-38s %4s %6s %7s  %s' % ('tema_id', 'téma', 'mot.', 'téma', 'arány', 'motívumversek · altételek'))
for tid, vs in sorted(talalat.items(), key=lambda x: (-len(x[1]), -len(x[1]) / max(1, len(tema_vers[x[0]])), x[0])):
    if len(vs) < a.min:
        continue
    cimkek = sorted({c for cs in vs.values() for c in cs if c})
    print('%-10s %-38.38s %4d %6d %6.1f%%  %s · %s' % (tid, tema_nev[tid], len(vs), len(tema_vers[tid]),
                                                    100.0 * len(vs) / max(1, len(tema_vers[tid])),
                                                    ', '.join(sorted(vs)), ' | '.join(cimkek)[:160]))
print('\nkihagyott forrássor (a közös szabály szerint):', dict(sorted(SN._CACHE[('kihagyott', SN.NAVE)].items())))
