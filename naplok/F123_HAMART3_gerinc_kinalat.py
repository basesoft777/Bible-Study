"""F123 HAMART-001 U2 (X.K): a szótári gerinc kínálata — minden E-sor (és az új jelöltek) verséhez a
BDB/Thayer vers-jelentés táblája szerinti szakasz, a gerinc-Strongnál.

Kimenet: naplok/F123_HAMART3_gerinc_kinalat.tsv; döntés nélkül (a D50 választás az U2-é).
"""
import sys
import collections

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UJ = [('1Móz 7:4', 'H0127'), ('1Móz 7:23', 'H0127'), ('Sof 1:3', 'H0127'), ('Sof 1:2', 'H0127'),
      ('Jer 51:25', 'H7843'), ('Hós 10:8', 'H6975'), ('Ez 12:19', 'H2555'), ('Mal 3:11', 'H7843'),
      ('Mal 3:11', 'H0127'), ('1Móz 8:21', 'H0127'), ('Jób 31:38', 'H0127')]


def tsv(fajl):
    sorok = [l.rstrip('\n').split('\t') for l in open(fajl, encoding='utf-8') if not l.startswith('#')]
    return [dict(zip(sorok[0], r)) for r in sorok[1:]]


def versek(igehely):
    konyv, hely = igehely.rsplit(' ', 1)
    fej, v = hely.split(':')
    if '-' in v:
        a, b = v.split('-')
        return ['%s %s:%d' % (konyv, fej, i) for i in range(int(a), int(b) + 1)]
    return [igehely]


bdb = collections.defaultdict(list)
for r in tsv('adat/bdb_vers_jelentes.tsv'):
    bdb[(r['strong'], r['karoli_vers'])].append('%s %s' % (r['bdb_id'], r['utvonal']))
thayer = collections.defaultdict(list)
for r in tsv('adat/thayer_vers_jelentes.tsv'):
    thayer[(r['strong'], r['karoli_vers'])].append('Thayer ' + r['utvonal'])

celok = []
for r in tsv('adat/elofordulasok.tsv'):
    if r['id'] == 'HAMART-001':
        celok.append(('E', r['igehely'], r['strong'] or r['gerinc_elem']))
for v, s in UJ:
    celok.append(('UJ', v, s))

with open('naplok/F123_HAMART3_gerinc_kinalat.tsv', 'w', encoding='utf-8') as ki:
    ki.write('# GENERÁLT: naplok/F123_HAMART3_gerinc_kinalat.py | scope=HAMART-001 E-sorok + új jelöltek × adat/bdb_vers_jelentes.tsv, adat/thayer_vers_jelentes.tsv | forras=split(\'\\t\') | ts=2026-11-05\n')
    ki.write('tipus\tigehely\tstrong\tszotar_szakasz\n')
    for t, ige, s in celok:
        talal = []
        for v in versek(ige):
            for st in s.replace('+', ' ').split():
                talal += [v.split(':')[1] + '→' + x for x in (bdb.get((st, v)) or thayer.get((st, v)) or [])]
        ki.write('%s\t%s\t%s\t%s\n' % (t, ige, s, '; '.join(talal) or '-'))
        print(t, ige, s, '|', '; '.join(talal) or '-')
