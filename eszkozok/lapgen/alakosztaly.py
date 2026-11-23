"""lapgen.alakosztaly — az alakosztály-kapu, típus szerint (GK-24; a brief 2. pontja).

A kész lap minden sorához fajta-térkép tartozik (`iro.KeszSor.tartomanyok`: próza, sablon, idézet, horgony,
megjegyzés, jelölés). A kapu ezen fut, nem a nyers szövegen:
- a sablon-eredetű szövegen minden alakosztály tilos (aláhúzásos azonosító, `.tsv`/`.py` fájlnév, döntés- és
  tételszám, nyers szótárfej, héber szó számlálóval, a fordítási kör jele, nyers sortörés-elem, tört írásjel);
- a kézi prózán a belső jelölések osztályai (fájlnév, döntés- és tételszám, a lekérdezés proveniencia-mezői, a
  zárójel nélküli Strong-szám);
- az idézeten csak a proveniencia-alakok (a forrásszöveg maga bármit idézhet).
A megjegyzés, a horgony és a szerkezeti jelölés nem látható szöveg, a kapu nem nézi.

A csupasz Strong-szám (N235, DT-F218e (2), DT-F218f) két kivétele:
- tartós: a szótári címke a címsorban („#### H0779 — אָרַר (árar) · BDB”): a Strong-szám után „ — ” és héber vagy
  görög betűvel a szó áll;
- ismert eltérés: az `ISMERT_CSUPASZ_STRONG` név szerinti listája (az S9c leltára, a két mintalap kézi adatában), a
  tételenként egy lapon megengedett legnagyobb darabszámmal; a darabszám fölötti előfordulás a kapun BUKÁS.
  A lista csak fogyhat: új tétel nem kerülhet rá (a befagyasztott leltár hash-sel rögzített), és minden tételének
  legalább az egyik mintalapon elő kell fordulnia (`teszt_kapuk.CsupaszStrong`); a javítás az N-F218i (a 218c
  adatköre, az F218.13 után).

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
CSUPASZ_STRONG = 'csupasz Strong-szám'
# a kézi prózán tilos alakok (a mai prózakapuk belső jelöléseinek osztályai)
PROZA_ALAKOK = (
    ('fájlnév', SABLON_ALAKOK[1][1]),
    ('döntésszám', SABLON_ALAKOK[2][1]),
    ('tételszám', SABLON_ALAKOK[3][1]),
    ('proveniencia-mező', re.compile(r'\b(?:scope|forras)=')),
    ('tört írásjel', SABLON_ALAKOK[9][1]),
    # N235 (DT-F218e (2), DT-F218f): a zárójel nélküli Strong-szám belső jelölés (a zárójeles: GK-A10); a nem négyjegyű
    # és a betű-utótagos alak (TBESH: H7451A) is
    (CSUPASZ_STRONG, re.compile(r'(?<![\w/])[HG]\d{1,5}[A-Za-z]?\b')),
)
# az idézeten tilos alakok: csak a proveniencia
IDEZET_ALAKOK = (
    ('proveniencia-mező', re.compile(r'\b(?:scope|forras)=|\bts=\d')),
)
_ALAKOK = {Fajta.SABLON: SABLON_ALAKOK, Fajta.PROZA: PROZA_ALAKOK, Fajta.IDEZET: IDEZET_ALAKOK}

# A szótári címke (tartós kivétel, DT-F218f (3)): címsorban a Strong-szám után „ — ” és héber vagy görög betűvel a szó.
_CIMKE_RX = re.compile(r' — [\u0590-\u05FF\u0370-\u03FF\u1F00-\u1FFF]')

# Az ismert eltérések (DT-F218f (4)): (csoport, Strong-szám, a szövegrész, amelyben áll, legfeljebb ennyi előfordulás egy
# lapon). A javításuk az N-F218i. A: a TSK-kizárás indoklása (16 cella, a mintalapon 29 látható sor); B: a Károli-
# csoport blokk-sorai (57 cella, soronként 1); D: egy kapcsolat-indoklás (1 sor, 2 szám); N235: a két csoportos
# indoklás („blokk-kizárás (a H7451 és a H7043 blokkjának mintájára)”, 2 cella, 2 sor): javul az F218.13-ban (N235;
# DT-F218e (2) (b): a kiadott lap és a bájt-referencia a szerkesztő nézése előtt nem mozdul).
_B_STRONGOK = (
    'G0173', 'G0174', 'G0331', 'G0332', 'G0685', 'G0862', 'G0942', 'G0971',
    'G2647', 'G2653', 'G2692', 'G3639', 'G4485', 'G4647', 'G4938', 'G5146',
    'H0006', 'H0329', 'H0423', 'H2254', 'H2255', 'H2312', 'H2336', 'H2554',
    'H2723', 'H2738', 'H3238', 'H3905', 'H4072', 'H4288', 'H4384', 'H4835',
    'H4893', 'H5285', 'H5518', 'H5544', 'H5636', 'H6217', 'H6231', 'H6234',
    'H6530', 'H6563', 'H6796', 'H6895', 'H7045', 'H7057', 'H7612', 'H7621',
    'H7667', 'H7701', 'H7703', 'H7722', 'H7898', 'H8045', 'H8047', 'H8068',
    'H8395',
)
ISMERT_CSUPASZ_STRONG = (
    (('A', 'H6093', 'de nem a H6093 iccávón-t', 29),)
    + tuple(('B', s, 'ezekben a versekben a %s szót fordítja' % s, 1) for s in _B_STRONGOK)
    + (('D', 'H7121', 'azonos H7121+H8034 pár', 1), ('D', 'H8034', 'azonos H7121+H8034 pár', 1))
    # javul az F218.13-ban (N235)
    + (('N235', 'H7451', 'a H7451 és a H7043 blokkjának mintájára', 2),
       ('N235', 'H7043', 'a H7451 és a H7043 blokkjának mintájára', 2))
)


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


def _csupasz_kivetel(sor, szoveg, m):
    """A csupasz Strong-szám kivétele: None, ha nincs; 'címke' a szótári címkénél; különben az ismert eltérés tétele."""
    if sor.szoveg.startswith('#') and _CIMKE_RX.match(szoveg, m.end()):
        return 'címke'
    for tetel in ISMERT_CSUPASZ_STRONG:
        if tetel[1] != m.group(0):
            continue
        kezdet = szoveg.find(tetel[2])
        while kezdet >= 0:
            if kezdet <= m.start() < kezdet + len(tetel[2]):
                return tetel
            kezdet = szoveg.find(tetel[2], kezdet + 1)
    return None


def talalatok(sorok, hasznalt=None):
    """Az alakosztály-találatok a kész sorokon: [(sorszám, fajta, osztály, a talált alak)]. A `hasznalt` szótárba
    (ha meg van adva) az ismert eltérések tételei kerülnek, előfordulásuk számával."""
    ki = []
    for n, sor in enumerate(sorok, start=1):
        for fajta, szoveg in _darabok(sor):
            for nev, minta in _ALAKOK[fajta]:
                for m in minta.finditer(szoveg):
                    if nev == CSUPASZ_STRONG:
                        kivetel = _csupasz_kivetel(sor, szoveg, m)
                        if kivetel is not None:
                            if hasznalt is not None and kivetel != 'címke':
                                hasznalt[kivetel] = hasznalt.get(kivetel, 0) + 1
                            continue
                    ki.append((n, fajta, nev, m.group(0)))
    return ki


def kapu(nezetek):
    """A kapu a lap minden nézetén. Találatnál AlakHiba a találatok felsorolásával."""
    hibak, hasznalt = [], {}
    for nezet, sorok in nezetek.items():
        hibak.extend((nezet,) + t for t in talalatok(sorok, hasznalt))
    tobb = sorted((t, db) for t, db in hasznalt.items() if db > t[3])
    if tobb:
        raise AlakHiba('alakosztály-kapu (GK-24): az ismert eltérés a megengedettnél többször áll a lapon: %s' % '; '.join(
            '%s „%s”: %d (legfeljebb %d)' % (t[1], t[2], db, t[3]) for t, db in tobb))
    if hibak:
        raise AlakHiba('alakosztály-találat a látható szövegen (GK-24): %s' % '; '.join(
            '%s %d. sor, %s: %s „%s”' % (nezet, n, fajta.value, nev, alak) for nezet, n, fajta, nev, alak in hibak[:10]))
    return nezetek
