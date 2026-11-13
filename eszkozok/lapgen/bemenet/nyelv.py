"""lapgen.bemenet.nyelv — a látható szókészlet két táblája: a névtábla (B65) és a sablontábla (B66).

A névtábla minden belső kulcs olvasói nevét adja; ismeretlen kulcs kemény hiba (GK-23).
A sablontábla a lap minden gépi mondatát adja; a megjelenítő más forrásból látható szöveget nem ír.
"""
import enum

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Kulcs, Nev, SablonSor, sablon

NEVTABLA_OSZLOPOK = ('tipus', 'kulcs', 'olvasoi_nev', 'eredet')
SABLON_OSZLOPOK = ('kulcs', 'mondat', 'parameterek', 'szakasz', 'eredet', 'dontes')
CIMKE_CELLA_TIPUS = 'cimke_cella'   # a szótári szakaszcímke cellakezdő alakja; kulcs: szótár|Strong|szócikk|szakasz
_KULCS_ELVALASZTO = '|'


class NevHiba(KeyError):
    """Ismeretlen névtábla-kulcs: a belső kulcsnak nincs olvasói neve."""


class Nevtabla:
    def __init__(self, nevek, nyers=None):
        self._nevek = dict(nevek)
        self._nyers = dict(nyers or {})

    def nyers_nevek(self, tipus):
        """Egy típus sorai nyersen ({kulcs: név}); csak a bemeneti réteg hívja, burkoláshoz."""
        return {k: nev for (t, k), nev in self._nyers.items() if t == tipus}

    def nev(self, tipus, kulcs):
        """A (típus, kulcs) olvasói neve. A kulcs lehet `Kulcs`, felsorolás-érték vagy kódba írt kulcsszó."""
        if isinstance(kulcs, Kulcs):
            kulcs = kulcs.ertek
        elif isinstance(kulcs, enum.Enum):
            kulcs = kulcs.value
        elif isinstance(kulcs, int) and not isinstance(kulcs, bool):
            kulcs = str(kulcs)   # sorszám-kulcs (pl. a szótári pont sorszáma)
        try:
            return self._nevek[(tipus, kulcs)]
        except KeyError:
            raise NevHiba('nincs olvasói neve: típus=%s, kulcs=%s' % (tipus, kulcs)) from None

    def van(self, tipus, kulcs):
        return (tipus, kulcs.ertek if isinstance(kulcs, Kulcs) else kulcs) in self._nevek

    def kulcsok(self, tipus):
        return tuple(k for (t, k) in self._nevek if t == tipus)


class Sablonok:
    def __init__(self, sorok):
        self._sorok = dict(sorok)

    def __call__(self, kulcs, **parameterek):
        """A `kulcs` sablonmondata a paraméterekkel: `Lathato`."""
        try:
            sor = self._sorok[kulcs]
        except KeyError:
            raise NevHiba('nincs ilyen sablonmondat: %s' % kulcs) from None
        return sablon(sor, **parameterek)

    def van(self, kulcs):
        return kulcs in self._sorok

    def kulcsok(self):
        return tuple(self._sorok)

    def sor(self, kulcs):
        return self._sorok[kulcs]


class Nyelv:
    """A megjelenítő szókészlete: `s(kulcs, **p)` sablonmondat, `nev(tipus, kulcs)` olvasói név."""
    __slots__ = ('s', 'nevtabla')

    def __init__(self, sablonok, nevtabla):
        self.s = sablonok
        self.nevtabla = nevtabla

    def nev(self, tipus, kulcs):
        return self.nevtabla.nev(tipus, kulcs)

    def kulcs(self, *reszek):
        """Sablonkulcs a reszeibol (`e2.jegyzet`, `heber` -> `e2.jegyzet.heber`)."""
        return '.'.join(reszek)


def b65_nevtabla(b):
    """B65 — az olvasói névtábla."""
    tabla = b._tabla('B65', oszlopok=NEVTABLA_OSZLOPOK)
    nevek, nyers = {}, {}
    for sor in tabla.szotarak():
        kulcs = (sor['tipus'], sor['kulcs'])
        if kulcs in nevek:
            raise BemenetHiba('B65: ismétlődő névtábla-kulcs: %s / %s' % kulcs)
        if not sor['olvasoi_nev']:
            raise BemenetHiba('B65: üres olvasói név: %s / %s' % kulcs)
        nevek[kulcs] = Nev(sor['tipus'], sor['kulcs'], sor['olvasoi_nev'])
        nyers[kulcs] = sor['olvasoi_nev']
    return Nevtabla(nevek, nyers)


def cimke_cellaalakok(b):
    """A szótári szakaszcímkék cellakezdő alakja (B65, `cimke_cella` típus) kézi szövegként:
    {(szótár, Strong, szócikk, szakasz): Kezi}. A címke a táblacella elején ebben az alakban áll; az alak adat,
    a generátor a címkét nem írja át (a címke és az alakja egyezését a szótári gerinc betöltése ellenőrzi)."""
    ki = {}
    for kulcs, nev in b65_nevtabla(b).nyers_nevek(CIMKE_CELLA_TIPUS).items():
        reszek = tuple(kulcs.split(_KULCS_ELVALASZTO))
        if len(reszek) != 4:
            raise BemenetHiba('B65: a `%s` kulcsa szótár|Strong|szócikk|szakasz alakú legyen: %r'
                              % (CIMKE_CELLA_TIPUS, kulcs))
        ki[reszek] = b.kezi('B65', CIMKE_CELLA_TIPUS, nev)
    return ki


def b66_sablonok(b):
    """B66 — a sablontábla."""
    tabla = b._tabla('B66', oszlopok=SABLON_OSZLOPOK)
    sorok = {}
    for sor in tabla.szotarak():
        if sor['kulcs'] in sorok:
            raise BemenetHiba('B66: ismétlődő sablonkulcs: %s' % sor['kulcs'])
        sorok[sor['kulcs']] = SablonSor(sor['kulcs'], sor['mondat'], sor['parameterek'],
                                        szakasz=sor['szakasz'], eredet=sor['eredet'])
    return Sablonok(sorok)


def nyelv(b):
    """A két tábla együtt, ahogy a megjelenítő használja."""
    return Nyelv(b66_sablonok(b), b65_nevtabla(b))
