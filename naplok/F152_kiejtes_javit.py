"""F152 kiejtés-tétel: a kézi próza héber szavainak kiejtése a forrásban (DT430: gépi magyaros kiejtés, „gépi” jelölés
nélkül; a kiejtés a `kiejtes_szoveg.kiejtes` javaslata, l. naplok/F152_kiejtes_meres.py).

- motivumok/ISTENTISZT-001.md: a PaRDeS négy szava (פְּשָׁט, רֶמֶז, דְּרַשׁ, סוֹד);
- motivumok/ALVIL-001.md: a שְׁאוֹל (2. szakasz, miert_fontos) és a תְּהוֹם (Kivonat).
Minden csere pontosan egyszer illeszkedik, különben nem ír.

Futtatás: python naplok/F152_kiejtes_javit.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSERE = {
    'motivumok/ISTENTISZT-001.md': [
        ('(פְּשָׁט, "egyszerű")', '(פְּשָׁט, pesát: "egyszerű")'),
        ('(רֶמֶז, "utalás")', '(רֶמֶז, remez: "utalás")'),
        ('(דְּרַשׁ, "keresés/magyarázat")', '(דְּרַשׁ, deras: "keresés/magyarázat")'),
        ('(סוֹד, "titok")', '(סוֹד, szód: "titok")'),
    ],
    'motivumok/ALVIL-001.md': [
        ('a תְּהוֹם/ἄβυσσος', 'a תְּהוֹם (*tehóm*)/ἄβυσσος'),
        ('**שְׁאוֹל — *seól*** (héber)', '**שְׁאוֹל** (*seól*, héber)'),
    ],
}
for f, cserek in CSERE.items():
    ut = os.path.join(GYOKER, f)
    with open(ut, encoding='utf-8', newline='') as fh:
        s = fh.read()
    for a, b in cserek:
        assert s.count(a) == 1, (f, a)
        s = s.replace(a, b)
    with open(ut, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)
    print('%s: %d csere' % (f, len(cserek)))
