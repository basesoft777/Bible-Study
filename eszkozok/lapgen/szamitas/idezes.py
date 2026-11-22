"""lapgen.szamitas.idezes — „12. Irodalom és idézés” (S8c): a szakasz modellje.

A szótárak és az adatforrások listája a lap számozott szakaszainak valódi olvasásaiból jön (GK-07; DT-F a forrás-
listáról): a szakaszrend a megelőző szakaszok olvasásait adja át (`fo.lap_keszit`), a jegyzék `irodalom` oszlopa szűr.
A szótárfájlok a szótár teljes neve szerint egy sorba vonódnak (a sorok a teljes név rendjében), az adatfájlok az
olvasói nevük szerint (a sorok az első fájljuk útvonalának rendjében); a licencek soronként egyszer, a címke rendjében.
Utánuk a generátor által nem olvasott külső források (a visszhang-tábla Vulgata-sorai, a tanúk forrásai). A vitatott
pontok szakirodalma (B40) a szerzős sorok teljes hivatkozása.
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from lapgen.bemenet import irodalom as irodalom_be
from lapgen.bemenet import szakirodalom as szakirodalom_be
from lapgen.ertekek import IrodLicenc
from lapgen.szoveg import Kulcs, Lathato, idezet, proza


@dataclass(frozen=True)
class Licenc:
    """A forrássor egy licence: az alakja és a licencleltár címkéje (idézet; a Chain Lineage-alaknál nincs)."""
    alak: IrodLicenc
    cimke: Optional[Lathato]


@dataclass(frozen=True)
class SzotarSor:
    """Egy szótár: a teljes neve (névtábla-kulcs: az első fájl útvonala), a fájljai (a névelős név kulcsai; az azonos
    nevű fájl egyszer) és a licencei."""
    nev: Kulcs
    forrasok: Tuple[Kulcs, ...]
    licencek: Tuple[Licenc, ...]


@dataclass(frozen=True)
class AdatSor:
    """Egy adatforrás (vagy külső forrás): a név kulcsa és a licencei."""
    nev: Kulcs
    licencek: Tuple[Licenc, ...]
    kulso: bool


@dataclass(frozen=True)
class Hivatkozas:
    """A vitatott pont szakirodalmának teljes hivatkozása: a szerző teljes neve (kézi), a cím, a megjelenés, a DOI vagy
    a webcím (idézetek)."""
    szerzo: Lathato
    ev: int
    cim: Lathato
    megjelenes: Lathato
    doi: Optional[Lathato]
    url: Optional[Lathato]


@dataclass(frozen=True)
class Idezes:
    szotarak: Tuple[SzotarSor, ...]
    szakirodalom: Tuple[Hivatkozas, ...]
    adatforrasok: Tuple[AdatSor, ...]


def licenc_lista(fajlok):
    lat, ki = set(), []
    for f in sorted(fajlok, key=lambda f: (f.cimke.ertek if f.cimke is not None else '', f.licenc.value)):
        kulcs = (f.licenc, f.cimke.ertek if f.cimke is not None else None)
        if kulcs in lat:
            continue
        lat.add(kulcs)
        ki.append(Licenc(f.licenc, idezet(f.cimke) if f.cimke is not None else None))
    return tuple(ki)


def _csoportok(fajlok):
    """A fájlok csoportjai a csoport (név) szerint, a csoport első fájljának rendjében."""
    csop = {}
    for f in fajlok:
        csop.setdefault(f.csoport, []).append(f)
    return csop


def szamit(korny, elozo):
    """A szakasz modellje. `elozo`: a megelőző számozott szakaszok olvasásai ({szakasz: B-azonosítók})."""
    azonositok = frozenset().union(*elozo.values()) if elozo else frozenset()
    fajlok = irodalom_be.irodalom_fajlok(korny.b, azonositok)
    szotarak = []
    for _nev, fs in sorted(_csoportok([f for f in fajlok if f.szotar]).items()):
        forrasok, latott = [], set()
        for f in fs:
            if f.forras_csoport not in latott:
                latott.add(f.forras_csoport)
                forrasok.append(f.kulcs)
        szotarak.append(SzotarSor(nev=fs[0].kulcs, forrasok=tuple(forrasok), licencek=licenc_lista(fs)))
    adat = [AdatSor(nev=fs[0].kulcs, licencek=licenc_lista(fs), kulso=False)
            for fs in _csoportok([f for f in fajlok if not f.szotar]).values()]
    for k in irodalom_be.kulso_forrasok(korny.b, korny.motivum, azonositok):
        adat.append(AdatSor(nev=k.kulcs, licencek=(Licenc(k.licenc, idezet(k.cimke) if k.cimke is not None else None),),
                            kulso=True))
    hivatkozasok = tuple(
        Hivatkozas(szerzo=proza(v.szerzo_teljes), ev=v.ev, cim=idezet(v.cim), megjelenes=idezet(v.megjelenes),
                   doi=idezet(v.doi) if v.doi is not None else None, url=idezet(v.url) if v.url is not None else None)
        for v in szakirodalom_be.b40_vitatott_forrasok(korny.b, korny.motivum) if v.szerzo is not None)
    return Idezes(szotarak=tuple(szotarak), szakirodalom=hivatkozasok, adatforrasok=tuple(adat))
