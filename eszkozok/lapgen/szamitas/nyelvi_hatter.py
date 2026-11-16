"""lapgen.szamitas.nyelvi_hatter — a 4.8 pont (Nyelvi háttér) héber része.

Két rész: (1) szavanként a BDB-szócikk fejének rövid alakja (alapjelentés, gyök); (2) a lánc héber szavainak rokon
nyelvi táblája a BDB szerint (a régi lapon a 4.11-ből áthelyezve). A régi generátor szabályai: `_gerinc_bdb_fej_rovid`
(a szólista), `lanc_szavak` és `lanc_mag` (a lánc szavai és versei), `_lanc_szo_cim` és `lanc_szo_jelentes` (a
sor címe), `blokk_visszhang_hatter` és `_hatter_sorok` (a sorok), `bdb_to_strong` (a főnév igei töve),
`bdb_rokon_szocikk` és `bdb_helyi_szocikk` (a hiány oka). Mondatot nem fogalmaz: a megjelenítő teszi a sablontáblából.

A tábla csak akkor áll, ha a motívumnak van ókori fordítás-sora a visszhang-táblában és van lánc-szava (a régi kód
ugyanezzel a feltétellel építette a 4.11-et, és abból a táblát).
"""
import dataclasses
import enum
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import gerinc as gerinc_be
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import nyelvi_hatter as nyelvi_hatter_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.szamitas.szotari_tipusok import Szo
from lapgen.szoveg import Lathato, Strong, idezet


@dataclasses.dataclass(frozen=True)
class HeberSzoHatter:
    """Egy héber szó rövid nyelvi háttere. `van_fej`: a szónak van magyar BDB-szócikkfeje; az `alap` és a `gyok` a
    fej részletei (idézet); ha a fej nem mondja ki az alapjelentést, a `rovid` a rövid szótár magyar jelentése."""
    szo: Szo
    van_fej: bool
    alap: Optional[Lathato]
    gyok: Optional[Lathato]
    rovid: Optional[Lathato]


class Megjegyzes(enum.Enum):
    """A rokon nyelvi sor megjegyzése (a régi szöveg betűrendjében)."""
    IRAS_NELKUL = 1
    BIZONYTALAN = 2
    ROMLOTT = 3


@dataclasses.dataclass(frozen=True)
class RokonAlak:
    alak: Lathato
    kiejtes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class RokonNyelvSor:
    """Egy rokon nyelv sora: a nyelv (a tábla szövege), az alakok kiejtéssel, a jelentések és a megjegyzések."""
    nyelv: Lathato
    alakok: Tuple[RokonAlak, ...]
    jelentesek: Tuple[Lathato, ...]
    megjegyzesek: Tuple[Megjegyzes, ...]


class Hiany(enum.Enum):
    """Miért nem áll rokon nyelvi sor a szónál (a régi kód mondatai szerint)."""
    NINCS_SOR = 'nincs_sor'               # a lekérdezés lefutott, a szócikkben nincs rokon alak
    NINCS_KINYERES = 'nincs_kinyeres'     # a szót nem kérdezték le
    NEM_AZONOSITOTT = 'nem_azonositott'   # a lekérdezés a szócikket nem azonosította (a helyi szövegben sincs)
    NEM_TALALHATO = 'nem_talalhato'       # a szócikk a helyi szövegben sem található
    NINCS_ADAT = 'nincs_adat'             # a szócikkben nincs rokon nyelvi adat


@dataclasses.dataclass(frozen=True)
class RokonSzo:
    """A tábla egy lánc-szava: a cím (a láncversek szerinti alak és a láncbeli jelentés), a saját sorai, vagy a hiány
    oka; a `to` a főnév igei töve, a `to_sorok` a tő sorai (ha a szó saját szócikkében nincs rokon adat)."""
    szo: Szo
    jelentes: Optional[Lathato]
    sorok: Tuple[RokonNyelvSor, ...]
    hiany: Optional[Hiany]
    to: Optional[Szo]
    to_sorok: Tuple[RokonNyelvSor, ...]


@dataclasses.dataclass(frozen=True)
class HeberHatter:
    szavak: Tuple[HeberSzoHatter, ...]
    rokon: Optional[Tuple[RokonSzo, ...]]   # None: a tábla nem áll


def _szo(f, strong, versek):
    """A szó szótári alakja és kiejtése a megadott versek szerinti változatban."""
    szotari = f.kiejtes.szotari(strong, versek)
    return Szo(strong=strong,
               alak=idezet(f.tablaban(szotari.alak)) if szotari is not None else None,
               kiejtes=idezet(f.tablaban(szotari.kiejtes))
               if szotari is not None and szotari.kiejtes is not None else None)


def _lanc_szavak(f, motivum):
    """[(Strong, láncversek)] a régi `lanc_szavak` szerint: a lánc-szó a sorok egyetlen héber Strong-számú hordozó
    eleme (a tábla rendjében); a láncvers a Pesat-gerinc azon verse, amely a motívum saját verse, és amelyben a szó
    a héber szövegben áll. Gerinc nélkül a szópáros motívum formulájának igéje, a motívum ószövetségi verseivel."""
    sorok = sorted(f.sorok, key=lambda s: s.fajl_sorszam)
    karoli = bemenet.b07_karoli(f.b)
    tahot = szavak_be.b08_tahot(f.b)
    szavak = []
    for s in sorok:
        reszek = s.gerinc_reszek
        if not s.tematikus and len(reszek) == 1 and isinstance(reszek[0], Strong) and reszek[0].heber \
                and reszek[0] not in szavak:
            szavak.append(reszek[0])
    mag = motivum_be.lanc_mag(f.b, motivum, sorok, karoli)
    versek = []
    if mag is None:
        if szavak:
            return ()
        ige = next((s.gerinc_reszek[0] for s in sorok if len(s.gerinc_reszek) == 2
                    and all(isinstance(r, Strong) and r.heber for r in s.gerinc_reszek)), None)
        if ige is None:
            return ()
        szavak = [ige]
        for s in sorok:
            for v in karoli.versek(s.igehely):
                if v not in versek and not f.konyvek.ujszovetsegi(v.konyv):
                    versek.append(v)
        versek.sort(key=f.konyvek.rendezo_kulcs)
    else:
        for s in sorok:
            for v in karoli.versek(s.igehely):
                if v not in versek and mag.tartalmazza(v):
                    versek.append(v)
    ki = []
    for g in szavak:
        vv = tuple(v for v in versek if tahot.token_szam(v.kod, g.kod))
        if vv:
            ki.append((g, vv))
    return tuple(ki)


def _lanc_jelentes(f, gerinc, strong, versek):
    """A lánc-szó jelentése a láncban (a régi `lanc_szo_jelentes`): a rövid magyar jelentés; ha a láncversekben a
    BDB egyetlen, nem Qal törzset ad, a régi kód a TAHOT glosszájából vett igét: ez az ág még nincs kész."""
    torzsek = {gerinc.vers_torzs(strong.kod, v.kod) for v in versek}
    if len(torzsek) == 1 and next(iter(torzsek)) in konfig.NEM_QAL_TORZSEK:
        raise bemenet.BemenetHiba('4.8: a(z) %s lánc-szó minden láncversében nem Qal törzs áll; a láncbeli jelentés '
                                  'ága (a TAHOT glosszájából) még nincs kész' % strong.kod)
    return f.jelentes(strong).magyar


def _nyelv_sorok(sorok):
    """A rokon nyelvi sorok nyelvenként (a régi `_hatter_sorok`): csak ellenőrzött sor, valódi rokon nyelvvel; az
    alak nélküli sor csak akkor, ha van jelentése, és az nem „azonos a bibliai héberrel”."""
    csoportok = {}
    for r in sorok:
        if not r.ellenorzott or not r.rokon_nyelv:
            continue
        if not r.alakok and (r.jelentes is None or r.azonos):
            continue
        csoportok.setdefault(r.nyelv_kulcs, []).append(r)
    ki = []
    for lista in csoportok.values():
        alakok, jelek, latott, megj = [], [], [], set()
        for r in lista:
            alakok.extend(RokonAlak(idezet(a.alak), idezet(a.kiejtes) if a.kiejtes is not None else None)
                          for a in r.alakok)
            if not r.alakok:
                megj.add(Megjegyzes.ROMLOTT if r.romlott else Megjegyzes.IRAS_NELKUL)
            if r.bizonytalan:
                megj.add(Megjegyzes.BIZONYTALAN)
            if r.jelentes is not None and r.jelentes.ertek not in latott:
                latott.append(r.jelentes.ertek)
                jelek.append(idezet(r.jelentes))
        ki.append(RokonNyelvSor(nyelv=idezet(lista[0].nyelv), alakok=tuple(alakok), jelentesek=tuple(jelek),
                                megjegyzesek=tuple(sorted(megj, key=lambda m: m.value))))
    return tuple(ki)


def _rokon(f, motivum, gerinc):
    vh = nyelvi_hatter_be.b38_visszhang(f.b, motivum)
    lanc = _lanc_szavak(f, motivum)
    if not vh.van_forditas or not lanc:
        return None
    lekerdezve = nyelvi_hatter_be.b24_rokon_irasok(f.b)
    szavak = [g for g, _v in lanc]
    sorok = vh.rokon
    van_sora = {r.strong for r in sorok}
    tovek = {gerinc.igei_to(s.kod) for s in szavak if any(r.ures for r in sorok if r.strong == s)} - {None}
    sorok = tuple(r for r in sorok if r.strong in szavak or r.strong.kod in tovek)
    tohoz = {r.strong.kod for r in sorok}
    ki = []
    for g, versek in lanc:
        cim = _szo(f, g, versek)
        jel = _lanc_jelentes(f, gerinc, g, versek)
        if g not in van_sora:
            to = gerinc.igei_to(g.kod) if g.kod in lekerdezve else None
            ki.append(RokonSzo(cim, jel, (), Hiany.NINCS_SOR if g.kod in lekerdezve else Hiany.NINCS_KINYERES,
                               _szo(f, Strong(to), ()) if to else None, ()))
            continue
        sajat = tuple(r for r in sorok if r.strong == g)
        if any(r.ures for r in sajat):
            to = gerinc.igei_to(g.kod)
            if lekerdezve.get(g.kod) == 0:
                hiany = Hiany.NEM_AZONOSITOTT if gerinc.helyi_szocikk(g.kod) else Hiany.NEM_TALALHATO
            else:
                hiany = Hiany.NINCS_ADAT
            to_sorok = _nyelv_sorok(tuple(r for r in sorok if r.strong.kod == to)) if to and to in tohoz else ()
            ki.append(RokonSzo(cim, jel, (), hiany, _szo(f, Strong(to), ()) if to_sorok else None, to_sorok))
            continue
        ki.append(RokonSzo(cim, jel, _nyelv_sorok(sajat), None, None, ()))
    return tuple(ki)


def szamit(f, motivum, sajat):
    """A 4.8 pont héber része a nyelvrész szavaira (`sajat`)."""
    gerinc = gerinc_be.gerinc(f.b)
    szavak = []
    for strong in sajat:
        fej = gerinc.fej_rovid(strong)
        alap = idezet(fej.alap) if fej is not None and fej.alap is not None else None
        rovid = f.jelentes(strong).magyar if fej is not None and alap is None else None
        szavak.append(HeberSzoHatter(szo=f.szo(strong), van_fej=fej is not None, alap=alap,
                                     gyok=idezet(fej.gyok) if fej is not None and fej.gyok is not None else None,
                                     rovid=rovid))
    return HeberHatter(szavak=tuple(szavak), rokon=_rokon(f, motivum, gerinc))
