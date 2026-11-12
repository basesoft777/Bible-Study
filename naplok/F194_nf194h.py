# -*- coding: utf-8 -*-
"""F194.34 — az N-F194h döntése (a felhasználó, 2026-11-12, az orkesztrátoron át, szó szerint: „Igen, mindhármat”):
a lektor 2., 15. és 21. tételének javaslata az `adat/motivumok.tsv` ISTENTISZT-001 sorában (DT-F194i, a DT-F194a és a
DT-F194e módosítása). Csak a `negativ_kriterium` és a `meghatarozas` mező változik, a megnevezett részeken.
Futtatás a repó gyökeréből: python naplok/F194_nf194h.py"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
P = 'adat/motivumok.tsv'
NK = [
    ('Az igehelyen a קָרָא (kárá, hív) igét a בְּשֵׁם (besém, „a nevén”) követi, és',
     'Az igehelyen a קָרָא (kárá, hív) ige és a בְּשֵׁם (besém, „a nevén”) együtt áll (a sorrend változhat), és'),
    ('áll: aktív, invokáló szerkezet', 'áll: segítségül hívó (invokáló) szerkezet'),
    ('a fölérendelt fogalomhoz tartozik', 'a tágabb körhöz tartozik'),
    ('(birtoklás, hovatartozás, nem invokáció)', '(birtoklás, hovatartozás, nem segítségül hívás)'),
]
MH = [
    ('és a gyülekezet Jézus Krisztus nevét hívja segítségül (1Kor 1:2).',
     'és Pál a gyülekezetet azokkal együtt köszönti, akik Jézus Krisztus nevét segítségül hívják (1Kor 1:2).'),
]
raw = open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
sorok = raw.split(nl)
fej = [s for s in sorok if s and not s.startswith('#')][0].split('\t')
ix = {k: i for i, k in enumerate(fej)}
n = 0
for i, s in enumerate(sorok):
    c = s.split('\t')
    if c[0] == 'ISTENTISZT-001':
        for mezo, cser in (('negativ_kriterium', NK), ('meghatarozas', MH)):
            for a, b in cser:
                assert c[ix[mezo]].count(a) == 1, (mezo, a)
                c[ix[mezo]] = c[ix[mezo]].replace(a, b)
        sorok[i] = '\t'.join(c); n += 1
assert n == 1
uj = nl.join(sorok)
assert sum(x != y for x, y in zip(raw.split(nl), uj.split(nl))) == 1
open(P, 'w', encoding='utf-8', newline='').write(uj)
print('ok')
