# -*- coding: utf-8 -*-
"""F123 HAMART-001 javítókör (2026-11-08): a független ellenőr (fuggetlen-ellenor) adatra vonatkozó ELTÉRÉS-ei.
- 1Móz 12:3: a határmondat az átok-formula ismétléseire szól (az 1Móz 3:14 a lánc első kimondása, nem ismétlés);
- 1Krón 20:1 összesítő sora: a Jer 51:25 saját okkal (fizikai pusztítás) áll kint, nem „ugyanezzel az okkal”;
- Jel 19:2: a görög Ószövetség 1Móz 6:11 mondatában a föld alany, nem tárgy.
Csak a megnevezett szövegrész változik. Futtatás a repó gyökeréből: python naplok/F123_HAMART3_javitokor2.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CSERE = [
    ('adat/jeloltek.tsv', '1Móz 12:3',
     'A határ az átok igéje (árar) és a föld (adámá) együttállása, ugyanaz a két szó, mint az 1Móz 3:17-ben, most az áldás keretében.',
     'Az átok-formula ismétléseinél a határ az átok igéje (árar) és a föld (adámá) együttállása, ugyanaz a két szó, mint az 1Móz 3:17-ben, itt az áldás keretében.'),
    ('adat/jeloltek.tsv', '1Krón 20:1',
     'A Jer 51:25 nem tagja a csoportnak: saját sorban, ugyanezzel az okkal elutasítva áll.',
     'A Jer 51:25 nem tagja a csoportnak: saját sorban, fizikai pusztításként elutasítva áll.'),
    ('adat/elofordulasok.tsv', 'Jel 19:2',
     'ugyanaz az ige és tárgy, mint a görög Ószövetségben az 1Móz 6:11 mondata, amely szerint a föld romlott vala.',
     'ugyanaz az ige, ugyanarra a földre, mint a görög Ószövetségben az 1Móz 6:11 mondata, amely szerint a föld romlott vala.'),
]

for ut in sorted({c[0] for c in CSERE}):
    sorok = open(ut, encoding='utf-8', newline='').read().split('\n')
    eredeti = list(sorok)
    kesz = []
    for n, l in enumerate(sorok):
        r = l.split('\t')
        if len(r) < 3 or r[0] != 'HAMART-001':
            continue
        for f, ige, a, b in CSERE:
            if f == ut and r[1] == ige and a in l:
                sorok[n] = l.replace(a, b)
                kesz.append(ige)
    vart = sorted(c[1] for c in CSERE if c[0] == ut)
    assert sorted(kesz) == vart, (ut, kesz, vart)
    assert sum(1 for x, y in zip(sorok, eredeti) if x != y) == len(vart)
    print('%s: %d sor' % (ut, len(kesz)))
    if '--ir' in sys.argv:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
if '--ir' not in sys.argv:
    print('(próba; írás: --ir)')
