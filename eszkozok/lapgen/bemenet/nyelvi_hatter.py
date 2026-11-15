"""lapgen.bemenet.nyelvi_hatter — a 4.8 pont (Nyelvi háttér) görög részének bemenetei.

Bemenetek: B25 (a lexikon szótári hivatkozástáblája: melyik szóhoz melyik szótárnak van szócikke), B26 (az LSJ
teljes szövege: az utaló csonk felismerése), B37 (az LXX-fordítói döntések: a motívum verseiben megnevezett görög
szavak, a rokon szavak forrása).

A régi generátor szabályai (`lexikon_general._hivatkozas_szoveg`, `lsj_csonk`, `rokon_szavak_strongok`,
`lxx_dontesek_index`): az utaló csonk az a szócikk, amely csak a képzés leírása („… Middle voice from G1909 and
G2564”); az alapige a csonk utolsó Strong-száma. A rokon szó a motívum verseinek LXX-döntéseiben megnevezett, a
motívumon kívüli görög szó, amelynek a kiegészítő szótárakon kívül szócikke van.
"""
import re

from lapgen import konfig
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Strong

_HIV_OSZLOPOK = ('strong', 'szotar')
_LSJ_OSZLOPOK = ('Strong_padded', 'Teljes_szocikk')
_LXX_OSZLOPOK = ('igehely', 'gorog_strong', 'tipus', 'bizonyossag')
_LSJ_CSONK_RX = re.compile(r'^\S+ (?:Middle voice |Passive voice )?from G\d+(?: and G\d+)?\.?$')
_STRONG_RX = re.compile(r'\bG(\d+)\b')
_GOROG_STRONG_RX = re.compile(r'^G\d{4}$')


class Hivatkozasok:
    """A szótári hivatkozástábla: Strong-szám → a szócikket adó szótárak."""

    def __init__(self, szotarak):
        self._szotarak = szotarak

    def szotarai(self, strong):
        return self._szotarak.get(strong.kod, frozenset())


def b25_hivatkozasok(b):
    """B25 — a lexikon szótári hivatkozástáblája (melyik szóhoz melyik szótárnak van szócikke)."""
    tabla = b._tabla('B25', oszlopok=_HIV_OSZLOPOK)
    s, sz = tabla.oszlop('strong'), tabla.oszlop('szotar')
    szotarak = {}
    for sor in tabla.sorok:
        szotarak.setdefault(sor[s], set()).add(sor[sz])
    return Hivatkozasok({k: frozenset(v) for k, v in szotarak.items()})


class Csonk:
    """Az LSJ utaló csonkja: a szócikk szövege (idézet) és az alapige Strong-száma (a csonk utolsó száma)."""
    __slots__ = ('szoveg', 'alap')

    def __init__(self, szoveg, alap):
        self.szoveg, self.alap = szoveg, alap


class Lsj:
    def __init__(self, b, szocikkek):
        self._b, self._szocikkek = b, szocikkek

    def csonk(self, strong):
        """A szó LSJ-szócikke, ha az csak utaló csonk; különben None."""
        szoveg = (self._szocikkek.get(strong.kod) or '').strip()
        if not szoveg or not _LSJ_CSONK_RX.match(szoveg):
            return None
        szamok = _STRONG_RX.findall(szoveg)
        if not szamok:
            raise BemenetHiba('B26: a(z) %s utaló csonkjában nincs Strong-szám' % strong.kod)
        return Csonk(self._b.forrasszoveg('B26', 'Teljes_szocikk', szoveg, strong),
                     Strong('G%04d' % int(szamok[-1])))


def b26_lsj(b):
    """B26 — az LSJ teljes szövege Strong-szám szerint (csak az utaló csonk felismeréséhez)."""
    tabla = b._tabla('B26', oszlopok=_LSJ_OSZLOPOK)
    s, sz = tabla.oszlop('Strong_padded'), tabla.oszlop('Teljes_szocikk')
    return Lsj(b, {sor[s]: sor[sz] for sor in tabla.sorok})


class LxxDontesek:
    def __init__(self, index):
        self._index = index

    def gorog_szavak(self, vers_kod):
        """A vers megjelenő LXX-döntéseiben megnevezett görög Strong-számok, a tábla rendjében."""
        return self._index.get(vers_kod, ())


def b37_lxx_dontesek(b):
    """B37 — az LXX-fordítói döntések, a megjelenő bizonyosság és típus szűrőjével (a régi `lxx_dontesek_index`)."""
    tabla = b._tabla('B37', oszlopok=_LXX_OSZLOPOK)
    i, g, t, bz = (tabla.oszlop(o) for o in _LXX_OSZLOPOK)
    index = {}
    for sor in tabla.sorok:
        if sor[bz].strip() not in konfig.LXX_DONTES_BIZONYOSSAG or sor[t].strip() not in konfig.LXX_DONTES_TIPUS:
            continue
        gs = sor[g].strip()
        if _GOROG_STRONG_RX.match(gs):
            index.setdefault(sor[i], []).append(Strong(gs))
    return LxxDontesek({k: tuple(v) for k, v in index.items()})
