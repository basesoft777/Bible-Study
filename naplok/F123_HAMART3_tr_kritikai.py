"""F123 HAMART-001 (`9_` v1, 3. szabály): az újszövetségi előfordulás-helyek motívumszavának szövegállása a Textus
Receptusban és a kritikai kiadásban (TAGNT `Kritikai kiadás` oszlop).

Kimenet: naplok/F123_HAMART3_tr_kritikai.tsv; összesítés a stdout-ra. Futtatás: python naplok/F123_HAMART3_tr_kritikai.py
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HELY = {'Róm 8:20-22': 'G5356', 'Gal 3:10': 'G1944', 'Gal 3:13': 'G1944', 'Zsid 6:7-8': 'G2671', 'Jel 11:18': 'G1311',
        'Jel 19:2': 'G5351', 'Jel 22:3': 'G2652', 'Mt 15:19': 'G1261', 'Mk 7:21-23': 'G1261', '2Pét 3:6-7': 'G2626'}


def versek(ige):
    k, h = ige.rsplit(' ', 1)
    f, v = h.split(':')
    a, b = (v.split('-') + [v])[:2]
    return ['%s %s:%d' % (k, f, i) for i in range(int(a), int(b) + 1)]


sorok = [l.rstrip('\n').split('\t') for l in open('konkordancia/TAGNT_kivonat.tsv', encoding='utf-8')]
fej = sorok[0]
kr = fej.index('Kritikai kiadás')
ki = ['# GENERÁLT: naplok/F123_HAMART3_tr_kritikai.py | scope=HAMART-001 ÚSZ E-helyek (10 sor) | forras=TAGNT_kivonat.tsv (Kritikai kiadás), split(\'\\t\') | ts=2026-11-05',
      'hely\tvers\tstrong\talak\tkritikai']
for hely, st in HELY.items():
    vs = set(versek(hely))
    talalt = [r for r in sorok[1:] if r[0] in vs and r[1].startswith(st)]
    for r in talalt:
        ki.append('\t'.join([hely, r[0], st, r[2], r[kr] if len(r) > kr else '']))
    print(hely, st, [(r[0], r[2], r[kr] if len(r) > kr else '') for r in talalt] or 'NINCS A TAGNT-BEN')
open('naplok/F123_HAMART3_tr_kritikai.tsv', 'w', encoding='utf-8').write('\n'.join(ki) + '\n')
