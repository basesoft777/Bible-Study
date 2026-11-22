"""lapgen.alakosztaly — az alakosztály-kapu, típus szerint (GK-24; a brief 2. pontja).

A kész lap minden sorához fajta-térkép tartozik (`iro.KeszSor.tartomanyok`: próza, sablon, idézet, horgony,
megjegyzés, jelölés). A kapu ezen fut, nem a nyers szövegen:
- a sablon-eredetű szövegen minden alakosztály tilos (aláhúzásos azonosító, `.tsv`/`.py` fájlnév, döntés- és
  tételszám, nyers szótárfej, héber szó számlálóval, a fordítási kör jele, nyers sortörés-elem, tört írásjel);
- a kézi prózán a belső jelölések osztályai (fájlnév, döntés- és tételszám, a lekérdezés proveniencia-mezői);
- az idézeten csak a proveniencia-alakok (a forrásszöveg maga bármit idézhet).
A megjegyzés, a horgony és a szerkezeti jelölés nem látható szöveg, a kapu nem nézi.

Kalibrálás: a két jóváhagyott mintalap prózáján és idézetein 0 hamis találat
(`teszt_kapuk.py`). Szólista nem kapu: a minták alakot keresnek, nem szavakat.
"""
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Fajta

# (név, minta): a sablon-eredetű szövegen tilos alakok
SABLON_ALAKOK = (
    ('aláhúzásos azonosító', re.compile(r'(?<![\w/.-])[A-Za-z]+_[A-Za-z0-9_]+\b')),
    ('fájlnév', re.compile(r'\b[\w-]+\.(?:tsv|py)\b')),
    ('döntésszám', re.compile(r'(?<![\w-])DT-?F?\d+')),
    ('tételszám', re.compile(r'(?<![\w&/])#\d{2,3}\b')),
    ('nyitott tétel', re.compile(r'(?<![\w/.#-])N-?F?\d+[a-z]?\b')),
    ('nyers szótárfej', re.compile(r'\b[HG]\d{4}\. [a-z]')),
    ('héber számlálóval', re.compile(r'[֐-׿]_\d{2,4}\b')),
    ('fordítási kör', re.compile(r'\bsz\d+\b')),
    ('nyers sortörés', re.compile(r'<br\s*/?>')),
    ('tört írásjel', re.compile(r',;|;\.')),
)
# a kézi prózán tilos alakok (a mai prózakapuk belső jelöléseinek osztályai)
PROZA_ALAKOK = (
    ('fájlnév', SABLON_ALAKOK[1][1]),
    ('döntésszám', SABLON_ALAKOK[2][1]),
    ('tételszám', SABLON_ALAKOK[3][1]),
    ('proveniencia-mező', re.compile(r'\b(?:scope|forras)=')),
    ('tört írásjel', SABLON_ALAKOK[9][1]),
)
# az idézeten tilos alakok: csak a proveniencia
IDEZET_ALAKOK = (
    ('proveniencia-mező', re.compile(r'\b(?:scope|forras)=|\bts=\d')),
)
_ALAKOK = {Fajta.SABLON: SABLON_ALAKOK, Fajta.PROZA: PROZA_ALAKOK, Fajta.IDEZET: IDEZET_ALAKOK}


class AlakHiba(BemenetHiba):
    """BUKÁS: alakosztály-találat a látható szövegen. A lap nem íródik ki."""


def _darabok(sor):
    """A sor összefüggő, azonos fajtájú látható darabjai: [(fajta, szöveg)]."""
    ki = []
    for kezdet, veg, fajta in sor.tartomanyok:
        if fajta not in _ALAKOK:
            continue
        if ki and ki[-1][0] is fajta and ki[-1][2] == kezdet:
            ki[-1] = (fajta, ki[-1][1] + sor.szoveg[kezdet:veg], veg)
        else:
            ki.append((fajta, sor.szoveg[kezdet:veg], veg))
    return [(f, s) for f, s, _v in ki]


def talalatok(sorok):
    """Az alakosztály-találatok a kész sorokon: [(sorszám, fajta, osztály, a talált alak)]."""
    ki = []
    for n, sor in enumerate(sorok, start=1):
        for fajta, szoveg in _darabok(sor):
            for nev, minta in _ALAKOK[fajta]:
                for m in minta.finditer(szoveg):
                    ki.append((n, fajta, nev, m.group(0)))
    return ki


def kapu(nezetek):
    """A kapu a lap minden nézetén. Találatnál AlakHiba a találatok felsorolásával."""
    hibak = []
    for nezet, sorok in nezetek.items():
        hibak.extend((nezet,) + t for t in talalatok(sorok))
    if hibak:
        raise AlakHiba('alakosztály-találat a látható szövegen (GK-24): %s' % '; '.join(
            '%s %d. sor, %s: %s „%s”' % (nezet, n, fajta.value, nev, alak) for nezet, n, fajta, nev, alak in hibak[:10]))
    return nezetek
