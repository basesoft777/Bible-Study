"""A 12. szerep (Tematikus index, Nave) mérése egy motívumra (ISTENTISZT-001 arany lap, 2026-10-29) — a küszöb és a
tiltólista javaslatához. Csak olvas.

A Nave-sor igehelye a Károli-számozásban: az `igehely_karoli`, ha ki van töltve, különben az `igehely`; a tartomány
(`1Móz 6:16-20`, egy fejezeten belül) a benne álló verseket fedi. Témánként kiírja: hány motívumverset érint (és melyiket), a
téma összes versének számát (Károli-kulcs, tartomány kibontva), az arányt (motívumvers / témavers), és a motívumverseket érintő
altételeket (`cimke`). split('\\t').

  python naplok/NAVE_tema_meres.py ISTENTISZT-001 [--min 1]
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TART = re.compile(r'^(.+ \d+):(\d+)-(\d+)$')


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def versek(hely):
    m = TART.match(hely)
    if not m:
        return [hely]
    return ['%s:%d' % (m.group(1), v) for v in range(int(m.group(2)), int(m.group(3)) + 1)]


ap = argparse.ArgumentParser()
ap.add_argument('id')
ap.add_argument('--min', type=int, default=1)
a = ap.parse_args()

motiv = {r['igehely'] for r in olvas(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')) if r['id'] == a.id}
tema_nev, tema_vers = {}, collections.defaultdict(set)
talalat = collections.defaultdict(lambda: collections.defaultdict(set))
for r in olvas(os.path.join(GYOKER, 'konkordancia', 'Nave_basokant.tsv')):
    hely = r.get('igehely_karoli') or r.get('igehely') or ''
    if not hely:
        continue
    tema_nev[r['tema_id']] = r['tema']
    for v in versek(hely):
        tema_vers[r['tema_id']].add(v)
        if v in motiv:
            talalat[r['tema_id']][v].add(r.get('cimke', ''))

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
