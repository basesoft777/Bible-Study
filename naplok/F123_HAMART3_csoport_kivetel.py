# -*- coding: utf-8 -*-
"""F123 HAMART-001: az egyenként beépített 5 vers kikerül a csoportos kizárás taglistájából (a felhasználó döntése,
2026-11-05: „ez most zárjuk le”; az ellenoriz.py 36. szabálya). A csoport versszáma csökken: H0127 178 → 174,
H7843 113 → 112. Ír: naplok/F123_teljesseg_HAMART-001_blokkok.tsv (5 sor ki), adat/jeloltek.tsv (2 sor)."""
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

KI = {('strong', 'H0127', '1Móz 7:4'), ('strong', 'H0127', '1Móz 7:23'), ('strong', 'H0127', 'Sof 1:2'),
      ('strong', 'H0127', 'Sof 1:3'), ('strong', 'H7843', 'Jer 51:25')}

ut = 'naplok/F123_teljesseg_HAMART-001_blokkok.tsv'
nyers = io.open(ut, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(nl)
uj = [s for s in sorok if tuple(s.split('\t')[:3]) not in KI]
assert len(sorok) - len(uj) == 5
uj.insert(1, '# F123.HAMART3.19 (2026-11-05): kivéve az egyenként beépített 5 vers (1Móz 7:4, 7:23, Sof 1:2, 1:3 a H0127, '
             'Jer 51:25 a H7843 blokkból); a vers nem lehet egyszerre előfordulás és csoport-tag (ellenoriz.py 36.)')
io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(uj))

CSERE = [
    ('blokk-sor (DT564 minta): 178 vers, a sor igehelye a blokk egy verse; a lista: naplok/F123_teljesseg_HAMART-001_blokkok.tsv (halo=strong, blokk=H0127)',
     'blokk-sor (DT564 minta): 174 vers, a sor igehelye a blokk egy verse; a lista: naplok/F123_teljesseg_HAMART-001_blokkok.tsv (halo=strong, blokk=H0127)'),
    ('Összesítő sor 178 versre', 'Összesítő sor 174 versre'),
    ('Az 1Móz 7:4, 7:23 és a Sof 1:2-3 saját sorban, beépítve áll.',
     'Az 1Móz 7:4, 7:23 és a Sof 1:2-3 nem tagja a csoportnak: saját sorban, beépítve áll.'),
    ('blokk-sor (DT564 minta): 113 vers, a sor igehelye a blokk egy verse; a lista: naplok/F123_teljesseg_HAMART-001_blokkok.tsv (halo=strong, blokk=H7843)',
     'blokk-sor (DT564 minta): 112 vers, a sor igehelye a blokk egy verse; a lista: naplok/F123_teljesseg_HAMART-001_blokkok.tsv (halo=strong, blokk=H7843)'),
    ('Összesítő sor 113 versre', 'Összesítő sor 112 versre'),
    ('A Jer 51:25 saját sorban, beépítve áll.', 'A Jer 51:25 nem tagja a csoportnak: saját sorban, beépítve áll.'),
]
ut = 'adat/jeloltek.tsv'
s = io.open(ut, encoding='utf-8', newline='').read()
for a, b in CSERE:
    assert s.count(a) == 1, (a[:50], s.count(a))
    s = s.replace(a, b)
io.open(ut, 'w', encoding='utf-8', newline='').write(s)
print('kész: 5 tag ki, 2 csoportsor')
