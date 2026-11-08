# -*- coding: utf-8 -*-
"""F123 HAMART-001, határkör (2026-11-08), második lépés: azoknak az elutasított jelölt-soroknak az indoklása, amelyek
a határkörben kikerült vagy szűkített helyre mint „bent lévőre” hivatkoznak (naplok/F123_HAMART3_hatar.py után).
Csak a megnevezett szövegrész változik; a többi sor bájtra azonos marad.
Futtatás a repó gyökeréből: python naplok/F123_HAMART3_hatar_utalasok.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UT = 'adat/jeloltek.tsv'
# (igehely, régi szövegrész, új szövegrész)
CSERE = [
    ('2Pét 3:10', 'A hely a 2Pét 3:6-7 sorának folytatása. A tűz-ítélet, az elemek felbomlása és a föld megégése önmagában nem utal vissza az özönvízre; a visszautalás a 3:6-7-ben áll, és az a motívumban van.',
     'Noé alakja és az özönvíz ítélete felidézésként (2Pét 3:6-7), mint a 2Pét 2:5-ben; a tűz-ítélet, az elemek felbomlása és a föld megégése a lánc szavai nélkül áll.'),
    ('2Pét 3:12', 'A hely a 2Pét 3:6-7 sorának folytatása. Az Isten napjának várása és az egek felbomlása önmagában nem utal vissza az özönvízre; a visszautalás a 3:6-7-ben áll, és az a motívumban van.',
     'Noé alakja és az özönvíz ítélete felidézésként (2Pét 3:6-7), mint a 2Pét 2:5-ben; az Isten napjának várása és az egek felbomlása a lánc szavai nélkül áll.'),
    ('1Kor 9:25', 'csak a Róm 8:20-22 köti a lánchoz.', 'csak a Róm 8:21 köti a lánchoz.'),
    ('1Kor 15:53', 'csak a Róm 8:20-22 köti a lánchoz.', 'csak a Róm 8:21 köti a lánchoz.'),
    ('1Kor 15:54', 'csak a Róm 8:20-22 köti a lánchoz.', 'csak a Róm 8:21 köti a lánchoz.'),
    ('1Pét 1:18', 'csak a Róm 8:20-22 köti a lánchoz.', 'csak a Róm 8:21 köti a lánchoz.'),
    ('1Pét 1:23', 'csak a Róm 8:20-22 köti a lánchoz.', 'csak a Róm 8:21 köti a lánchoz.'),
    ('Róm 1:23', 'csak a Róm 8:20-22 köti a lánchoz.', 'csak a Róm 8:21 köti a lánchoz.'),
    ('1Krón 20:1', 'A Jer 51:25 nem tagja a csoportnak: saját sorban, beépítve áll.',
     'A Jer 51:25 nem tagja a csoportnak: saját sorban, ugyanezzel az okkal elutasítva áll.'),
]

sorok = open(UT, encoding='utf-8', newline='').read().split('\n')
eredeti = list(sorok)
kesz = []
for n, l in enumerate(sorok):
    r = l.split('\t')
    if len(r) < 5 or r[0] != 'HAMART-001' or r[3] != 'elutasítva':
        continue
    for ige, a, b in CSERE:
        if r[1] == ige and a in r[4]:
            r[4] = r[4].replace(a, b)
            kesz.append(ige)
    sorok[n] = '\t'.join(r)
assert sorted(kesz) == sorted(c[0] for c in CSERE), set(c[0] for c in CSERE) - set(kesz)
assert sum(1 for x, y in zip(sorok, eredeti) if x != y) == len(CSERE)
print('%s: %d indoklás javítva' % (UT, len(kesz)))
if '--ir' in sys.argv:
    open(UT, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
else:
    print('(próba; írás: --ir)')
