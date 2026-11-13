"""lapgen.szamitas.elofordulas — a „2. Előfordulások” szakasz és a „2.1 Az igehelyek szövege” pont lapmodellje.

Tiszta számítás: a bemeneti réteg típusos soraiból számokat, felsorolás-értékeket, idézeteket és prózát ad;
mondatot nem fogalmaz (azt a megjelenítő teszi a sablontáblából).
"""
import dataclasses
import datetime
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.ertekek import Megbizhatosag, SzovetsegKod
from lapgen.szoveg import Horgony, Igehely, Lathato, Nev, idezet, proza


@dataclasses.dataclass(frozen=True)
class Osszegzes:
    """Az összegző mondat számai és következtetés-kódjai."""
    helyek: int
    osz: int
    usz: int
    konyvek: int
    magas: int
    sulypont_konyv: Optional[Nev]
    sulypont_db: int
    szovetseg: SzovetsegKod
    bizonytalan: bool


@dataclasses.dataclass(frozen=True)
class VersSzoveg:
    """Egy vers Károli-szövege; a `szoveg` hiánya kimondott hiány (a vers nincs a Károliban)."""
    vers: Igehely
    szoveg: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class IgehelyTetel:
    """A 2.1 pont egy tétele: az igehely szövege, a hozzá írt próza és a funkció magyarázata."""
    igehely: Igehely
    horgony: Horgony
    versek: Tuple[VersSzoveg, ...]
    kapcsolodas: Optional[Lathato]
    funkcio: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class ElofordulasSzakasz:
    osszegzes: Osszegzes
    jelentes_dontes: datetime.date
    ubs_dontes: datetime.date
    tetelek: Tuple[IgehelyTetel, ...]


def _osszegzes(sorok, konyvek):
    n = len(sorok)
    usz = sum(1 for s in sorok if konyvek.ujszovetsegi(s.igehely.konyv))
    osz = n - usz
    konyv_db = {}
    for s in sorok:
        konyv_db[s.igehely.konyv] = konyv_db.get(s.igehely.konyv, 0) + 1
    rangsor = sorted(konyv_db.items(), key=lambda x: (-x[1], x[0]))
    magas = sum(1 for s in sorok if s.megbizhatosag is Megbizhatosag.MAGAS)
    sulypont = rangsor[0] if rangsor and rangsor[0][1] / n >= konfig.SULYPONT_KUSZOB else None
    if usz and osz and usz / n < konfig.SZOVETSEG_KUSZOB:
        szovetseg = SzovetsegKod.FOKENT_OSZ
    elif usz and osz and osz / n < konfig.SZOVETSEG_KUSZOB:
        szovetseg = SzovetsegKod.FOKENT_USZ
    elif usz and osz:
        szovetseg = SzovetsegKod.MINDKETTO
    else:
        szovetseg = SzovetsegKod.CSAK_OSZ if osz else SzovetsegKod.CSAK_USZ
    return Osszegzes(
        helyek=n, osz=osz, usz=usz, konyvek=len(konyv_db), magas=magas,
        sulypont_konyv=konyvek.nev(sulypont[0]) if sulypont else None,
        sulypont_db=sulypont[1] if sulypont else 0,
        szovetseg=szovetseg,
        bizonytalan=magas / n < konfig.BIZONYTALAN_KUSZOB)


def _tetel(sor, karoli):
    versek = tuple(VersSzoveg(vers, idezet(karoli.szoveg(vers)) if karoli.van(vers) else None)
                   for vers in karoli.versek(sor.igehely))
    return IgehelyTetel(
        igehely=sor.igehely, horgony=sor.igehely.horgony(), versek=versek,
        kapcsolodas=proza(sor.kapcsolodas) if sor.kapcsolodas else None,
        funkcio=proza(sor.funkcio_magyarazat) if sor.funkcio_magyarazat else None)


def szamit(korny):
    """A szakasz lapmodellje. Előfordulás nélküli motívumnál BemenetHiba: a szakasz nem állhat üresen."""
    b = korny.b
    sorok = bemenet.b03_elofordulasok(b, korny.motivum)
    if not sorok:
        raise bemenet.BemenetHiba('B03: a(z) %s motívumnak nincs előfordulás-sora' % korny.motivum.kod)
    konyvek = bemenet.b63_konyvek(b)
    karoli = bemenet.b07_karoli(b)
    dontesek = bemenet.b51_dontesek(b)
    return ElofordulasSzakasz(
        osszegzes=_osszegzes(sorok, konyvek),
        jelentes_dontes=dontesek.datum(konfig.DONTES_JELENTES_FUNKCIO),
        ubs_dontes=dontesek.datum(konfig.DONTES_UBS_SZONEZET),
        tetelek=tuple(_tetel(sor, karoli) for sor in sorok))
