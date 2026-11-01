"""ISTENTISZT-001 arany lap: a 2Móz 33:19 / 34:5 TSK-célpontjai (lekerdez.py tsk kimenete, fájlból)
metszik-e a motívum 31 emberi-invokációs helyét (elofordulasok.tsv, a B-eset nélkül).

Használat: python naplok/ISTENTISZT001_arany_tsk_meres.py <tsk_kimenet_1> [<tsk_kimenet_2> ...]
A célpont alakja `Könyv f,v` vagy `Könyv f,v-w`; a tartományt versenként bontja. split('\t'), csak olvas.
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'


def tabla(ut):
    with open(ut, encoding='utf-8') as f:
        fej = None
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            yield dict(zip(fej, m))


a_helyek = {d['igehely'] for d in tabla('adat/elofordulasok.tsv')
            if d['id'] == ID and 'B-eset' not in d['funkcio']}
print(f'A-helyek: {len(a_helyek)}')

for ut in sys.argv[1:]:
    celok = set()
    prov = ''
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n')
            if sor.startswith('proveniencia:'):
                prov = sor
            if sor.startswith('#') or '\t' not in sor:
                continue
            hely = sor.split('\t')[0]
            m = re.match(r'^(.+?) (\d+),(\d+)(?:-(\d+))?$', hely)
            if not m:
                print('  értelmezhetetlen célpont:', hely)
                continue
            konyv, fej, v1, v2 = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
            for v in range(v1, v2 + 1):
                celok.add(f'{konyv} {fej}:{v}')
    print(f'{ut}: {len(celok)} célvers; metszet az A-helyekkel: {sorted(celok & a_helyek) or "üres"}')
    print('  ', prov)
