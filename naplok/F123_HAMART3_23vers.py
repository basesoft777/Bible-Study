"""F123 HAMART-001 U2: az X.A 1 256 új verse (UJ_HELY) és a teljesség-mérés 1 233 ELTÉRÉS-verse közti különbség.

Kimenet: naplok/F123_HAMART3_23vers.tsv és összesítés a stdout-ra.
"""
import sys
import collections

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def olvas(fajl):
    sorok = [l.rstrip('\n').split('\t') for l in open(fajl, encoding='utf-8') if not l.startswith('#')]
    return sorok[1:]


uj = collections.defaultdict(set)
for r in olvas('naplok/F123_adat_HAMART-001_f108_osszevetes.tsv'):
    if r[0] == 'ujrascan' and r[6].startswith('UJ_HELY'):
        uj[r[1]].add(r[2])

ma = collections.defaultdict(set)
for r in olvas('naplok/F123_teljesseg_HAMART-001.tsv'):
    if r[0] == 'strong':
        ma[r[1]].add(r[2])
elteres = {v for v, a in ma.items() if 'ELTÉRÉS' in a}

jel = collections.defaultdict(set)
for r in olvas('adat/jeloltek.tsv'):
    if r[0] == 'HAMART-001':
        jel[r[1]].add(r[3])

csak_xa = sorted(set(uj) - elteres)
csak_ma = sorted(elteres - set(uj))
print('X.A UJ_HELY vers:', len(uj), '| ma ELTÉRÉS:', len(elteres), '| csak X.A:', len(csak_xa), '| csak ma:', len(csak_ma))
oszt = collections.Counter()
with open('naplok/F123_HAMART3_23vers.tsv', 'w', encoding='utf-8') as ki:
    ki.write('# GENERÁLT: naplok/F123_HAMART3_23vers.py — az X.A UJ_HELY-versei, amelyek a teljesség-mérésben nem ELTÉRÉS\n')
    ki.write('irany\tigehely\txa_strong\tma_allapot\n')
    for v in csak_xa:
        a = ','.join(sorted(ma.get(v, {'nincs'})))
        oszt[a] += 1
        ki.write(f'csak_xa\t{v}\t{",".join(sorted(uj[v]))}\t{a}\n')
    for v in csak_ma:
        ki.write(f'csak_ma\t{v}\t-\t{",".join(sorted(ma[v]))}\n')
print(dict(oszt))
