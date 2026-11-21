"""lapgen.szamitas.resek — a kézi rések modellje (S8b): a 4. szakasz „Miért fontos ez a lelet” rése, a 10. Értelmezés és
a 11. Módszertan.

A rés törzse a kézi forrás szövege, változatlanul (`proza`). A kézi forrássor („*Proveniencia: …*”) nem kerül a lapra:
a helyén az olvasói forrássor áll a sorban nevezett adatbemenetek olvasói nevével, a nyers sor megjegyzésben (a régi
olvasói átírás eredménye, csere nélkül, szerkezetből). A belső adatnézet-jelölő nem áll a lapon. A vitatott pontok
bekezdése után a pont ellenőrzött szakirodalom-sora áll (a régi `szakirodalom_beszur`).
"""
import datetime
from dataclasses import dataclass
from typing import Optional, Tuple

from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szakirodalom as szakirodalom_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import ResElemFajta
from lapgen.szoveg import Kulcs, Lathato, Proveniencia, prov, proza

RES_MIERT_FONTOS, RES_ERTELMEZES, RES_MODSZERTAN = 'miert_fontos', 'ertelmezes', 'modszertan'


@dataclass(frozen=True)
class Szakirodalom:
    """Egy vitatott pont szakirodalom-sora; a szerző nélküli sor hiány-sor (a kérdésről lektorált forrás nincs)."""
    osszefoglalo: Lathato
    szerzo: Optional[Lathato]
    ev: Optional[int]
    lekerdezve: datetime.date


@dataclass(frozen=True)
class ForrasNev:
    """A kézi forrássorban nevezett adat: jegyzékbeli bemenet (a kulcs a B-azonosító, a név a névtábla `forras` sora),
    vagy a generátor által nem olvasott fájl (a kulcs az útvonal, a név a névtábla `kezi_forrasfajl` sora)."""
    jegyzekbeli: bool
    kulcs: Kulcs


@dataclass(frozen=True)
class ResElem:
    fajta: ResElemFajta
    proza: Optional[Lathato] = None
    bemenetek: Tuple[ForrasNev, ...] = ()       # FORRAS: a kézi forrássorban nevezett adatok, sorrendben
    eredeti: Optional[Proveniencia] = None      # FORRAS: a kézi forrássor nyers alakja (megjegyzésbe)
    szakirodalom: Optional[Szakirodalom] = None


@dataclass(frozen=True)
class Res:
    elemek: Tuple[ResElem, ...]


_URES = ResElem(ResElemFajta.URES)


def _elemek(b, motivum, res):
    r = motivum_be.kezi_res(b, motivum, res)
    if r is None:
        raise BemenetHiba('B47: a(z) %s motívumnak nincs kézi %s rése (a rés kötelező)' % (motivum.kod, res))
    elemek, pontok = [], {}
    for sor in r.sorok:
        if sor.belso:
            continue
        if sor.eredeti is not None:
            if not sor.bemenetek:
                raise BemenetHiba('B47: a(z) %s rés kézi forrássora adatbemenetet nem nevez (%s)' % (res, motivum.kod))
            elemek.append(ResElem(ResElemFajta.FORRAS, bemenetek=tuple(ForrasNev(j, k) for j, k in sor.bemenetek),
                                  eredeti=prov('eredeti: {}', sor.eredeti)))
        elif sor.kezi is None:
            # a belső sor kimaradása után az üres sorok sorozata egyetlen üres sor (a régi kiadható nézet szabálya)
            if not elemek or elemek[-1].fajta is not ResElemFajta.URES:
                elemek.append(_URES)
        else:
            if sor.pont is not None:
                pontok[sor.pont] = len(elemek)
            elemek.append(ResElem(ResElemFajta.PROZA, proza=proza(sor.kezi)))
    while elemek and elemek[0].fajta is ResElemFajta.URES:
        elemek.pop(0)
    while elemek and elemek[-1].fajta is ResElemFajta.URES:
        elemek.pop()
    if not elemek:
        raise BemenetHiba('B47: üres kézi rés: %s (%s)' % (res, motivum.kod))
    return elemek, pontok


def _szakirodalommal(elemek, pontok, sorok, motivum):
    """A vitatott pont bekezdése után (a bekezdést záró üres sor elé) üres sor és a szakirodalom-sor; a pont nélküli
    szakirodalom-sor BemenetHiba (a lap nem hagyhat ki ellenőrzött sort némán, GK-06)."""
    for vf in sorok:
        if vf.pont not in pontok:
            raise BemenetHiba('B40: a(z) %s egyik szakirodalom-sorának pontja nem áll a vitatott pontok között'
                              % motivum.kod)
        i = pontok[vf.pont]
        k = next((j for j in range(i + 1, len(elemek)) if elemek[j].fajta is ResElemFajta.URES), len(elemek))
        uj = ResElem(ResElemFajta.SZAKIRODALOM, szakirodalom=Szakirodalom(
            osszefoglalo=proza(vf.osszefoglalo), szerzo=proza(vf.szerzo) if vf.szerzo is not None else None,
            ev=vf.ev, lekerdezve=vf.lekerdezve))
        elemek[k:k] = [_URES, uj]
        pontok = {p: (h + 2 if h >= k else h) for p, h in pontok.items()}
    return elemek


def szamit_miert_fontos(korny):
    elemek, _pontok = _elemek(korny.b, korny.motivum, RES_MIERT_FONTOS)
    return Res(tuple(elemek))


def szamit_ertelmezes(korny):
    elemek, pontok = _elemek(korny.b, korny.motivum, RES_ERTELMEZES)
    sorok = szakirodalom_be.b40_vitatott_forrasok(korny.b, korny.motivum)
    return Res(tuple(_szakirodalommal(elemek, pontok, sorok, korny.motivum)))


def szamit_modszertan(korny):
    elemek, _pontok = _elemek(korny.b, korny.motivum, RES_MODSZERTAN)
    return Res(tuple(elemek))
