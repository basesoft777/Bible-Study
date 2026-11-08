# -*- coding: utf-8 -*-
"""F123 HAMART-001 javítókör (2026-11-08): a 38. gépi őr (strukturális hordozón a beépítés nem „csak e szó miatt”)
két beépített sort jelzett, amelynek indoklása csak a szóegyezést nevezte meg. Mindkét hely szerkezeti okból van bent;
az indoklás most a szerkezeti jegyet is kimondja. Csak a megnevezett két mező változik.
Futtatás a repó gyökeréből: python naplok/F123_HAMART3_or38.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

UT = 'adat/jeloltek.tsv'
TOLD = {
    '1Móz 6:17': (' — az özönvíz célja szó szerint ugyanaz az ige, mint a 6:12 emberi cselekvése',
                  ' — az özönvíz célja szó szerint ugyanaz az ige, mint a 6:12 emberi cselekvése: a tükörítélet '
                  'szerkezete, amelyben a büntetés annak a tettnek a folytatása, amelyet az ember elvégzett'),
    'Róm 8:21': ('amellyel a görög Ószövetség az 1Móz 6:11-13 romlás-igéjét (sáchat) fordítja;',
                 'amellyel a görög Ószövetség az 1Móz 6:11-13 romlás-igéjét (sáchat) fordítja, és a teremtett világ a '
                 'romlás rabságában vár szabadulásra: a lánc állapota az Újszövetségben;'),
}
sorok = open(UT, encoding='utf-8', newline='').read().split('\n')
eredeti = list(sorok)
kesz = []
for n, l in enumerate(sorok):
    r = l.split('\t')
    if len(r) > 4 and r[0] == 'HAMART-001' and r[3] == 'beépítve' and r[1] in TOLD:
        a, b = TOLD[r[1]]
        assert r[4].count(a) == 1, r[1]
        r[4] = r[4].replace(a, b)
        sorok[n] = '\t'.join(r)
        kesz.append(r[1])
assert sorted(kesz) == sorted(TOLD), kesz
assert sum(1 for x, y in zip(sorok, eredeti) if x != y) == len(TOLD)
print('%s: %d indoklás kiegészítve' % (UT, len(kesz)))
if '--ir' in sys.argv:
    open(UT, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
else:
    print('(próba; írás: --ir)')
