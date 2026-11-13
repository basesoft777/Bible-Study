"""lapgen.szamitas.kizarasok — a kizárt és vizsgált versek mellékletének lapmodellje.

A melléklet a vizsgálat modelljéből (`szamitas.vizsgalat`) készül: okonként a versek könyvenként, a
Károli-fordítás versrendjében. Új szám nincs benne: a kapuja a vizsgálat kapuja.
"""
import dataclasses
from typing import Tuple

from lapgen import bemenet
from lapgen.szamitas import vizsgalat
from lapgen.szamitas.vizsgalat import Vizsgalat
from lapgen.szoveg import Igehely, Lathato


@dataclasses.dataclass(frozen=True)
class KonyvSor:
    """Egy könyv versei egy okon belül; a könyvet az első vers nevezi meg."""
    elso: Igehely
    versek: Tuple[Igehely, ...]


@dataclasses.dataclass(frozen=True)
class MellekletOk:
    ok: Lathato
    leiras: Lathato
    versszam: int
    konyvek: Tuple[KonyvSor, ...]


@dataclasses.dataclass(frozen=True)
class Melleklet:
    vizsgalat: Vizsgalat
    csoport: Tuple[MellekletOk, ...]
    egyen: Tuple[MellekletOk, ...]


def _konyvenkent(versek, karoli):
    """A versek könyvenként, a Károli-fordítás versrendjében (az ott nem álló vers a végén, betűrendben)."""
    konyvek = {}
    for vers in sorted(frozenset(versek), key=lambda v: (karoli.sorrend(v), v.kod)):
        konyvek.setdefault(vers.konyv, []).append(vers)
    return tuple(KonyvSor(vv[0], tuple(vv)) for vv in konyvek.values())


def szamit(korny):
    v = vizsgalat.szamit(korny)
    karoli = bemenet.b07_karoli(korny.b)

    def okok(csoportok):
        return tuple(MellekletOk(o.ok, o.leiras, o.versszam, _konyvenkent(o.versek, karoli)) for o in csoportok)

    return Melleklet(vizsgalat=v, csoport=okok(v.csoport_okok), egyen=okok(v.egyen_okok))


def kapu(modell):
    """A melléklet kapuja: a vizsgálat számegyezése, és okonként a kiírt versek száma a versszám."""
    vizsgalat.kapu(modell.vizsgalat)
    for ok in modell.csoport + modell.egyen:
        if sum(len(k.versek) for k in ok.konyvek) != ok.versszam:
            raise vizsgalat.KapuHiba('a melléklet egy okának verslistája nem a versszáma (%d)' % ok.versszam)
    return modell
