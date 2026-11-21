"""lapgen.szamitas.eleje — a lap kerete, első rész (S8a): a lap eleje (cím, meghatározás, kritérium, tágabb kör), a
Kivonat, a Tartalomjegyzék és a Jelmagyarázat modellje.

A lap eleje a motívumtábla mai sorából jön (GK-A13: a cím mindig a motívumtábla címe; a meglévő lap nem bemenet). A
Kivonat a kézi forrás rése, változatlanul. A Tartalomjegyzék és a Jelmagyarázat nem olvas adatot: a szakaszrendből és
a sablontáblából áll (GK-10), a modelljük üres.
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Kulcs, Lathato, Proveniencia, prov_fuz, proza

RES_KIVONAT = 'kivonat'
RES_ELVALASZTO = ';'   # a több kézi forrás elválasztója a jelölőben (mint a motívumtáblában)


@dataclass(frozen=True)
class Fej:
    """A lap eleje. A kritérium és a tágabb kör kötelező (hiányuk BUKÁS, GK-06); a meghatározás és az azonosság
    típusa közül legalább az egyik áll, híján a cím (a régi `egyszerusitett_kolofon` szabálya)."""
    cim: Lathato
    kriterium: Lathato
    folerendelt: Lathato              # mondatkezdő alakban (a mondat a mezővel kezdődik)
    meghatarozas: Optional[Lathato]
    azonossag: Optional[Kulcs]
    forras_study: Proveniencia        # a kézi forrás útvonala(i), a lap fájlszintű jelölőjébe


def szamit_fej(korny):
    sor = motivum_be.b02_motivum(korny.b, korny.motivum)
    for nev, ertek in (('negativ_kriterium', sor.kriterium), ('folerendelt_fogalom', sor.folerendelt_mondatkezdo)):
        if ertek is None:
            raise BemenetHiba('B02: üres `%s` mező (%s): a lap elejének kötelező eleme' % (nev, korny.motivum.kod))
    return Fej(cim=proza(sor.cim), kriterium=proza(sor.kriterium), folerendelt=proza(sor.folerendelt_mondatkezdo),
               meghatarozas=proza(sor.meghatarozas) if sor.meghatarozas is not None else None,
               azonossag=sor.azonossag, forras_study=prov_fuz(RES_ELVALASZTO, sor.forras_study))


@dataclass(frozen=True)
class Kivonat:
    """A Kivonat rése soronként (kézi próza; üres sor: None)."""
    sorok: Tuple[Optional[Lathato], ...]


def szamit_kivonat(korny):
    res = motivum_be.kezi_res(korny.b, korny.motivum, RES_KIVONAT)
    if res is None or not res.sorok:
        raise BemenetHiba('B47: a(z) %s motívumnak nincs kézi Kivonata (a rés kötelező)' % korny.motivum.kod)
    for s in res.sorok:
        if s.eredeti is not None or s.belso:
            raise BemenetHiba('B47: a(z) %s Kivonatában kézi forrássor vagy belső jelölő áll (a Kivonat próza)'
                              % korny.motivum.kod)
    return Kivonat(tuple(proza(s.kezi) if s.kezi is not None else None for s in res.sorok))


@dataclass(frozen=True)
class Ures:
    """Adat nélküli szakasz modellje: a megjelenítő a keretből (szakaszrend, sablontábla) dolgozik."""


def szamit_ures(korny):
    return Ures()
