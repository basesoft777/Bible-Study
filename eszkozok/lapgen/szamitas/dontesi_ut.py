"""lapgen.szamitas.dontesi_ut — az „1. Döntési út” szakasz lapmodellje (1.1–1.5).

A számok a vizsgálat közös modelljéből jönnek (`szamitas.vizsgalat`): ugyanabból, amelyből a kizárt versek melléklete
ír, ezért a két nézet számai egyeznek. A szakasz saját része: a keresés tárgya (a motívum sora), a lánc szavai a
szótári alakjukkal, a motívumhoz tartozó helyek a hordozó elemük szerint csoportosítva, a határesetek és a kézi
forrás nyitott kérdései. Mondatot nem fogalmaz: azt a megjelenítő teszi a sablontáblából.
"""
import dataclasses
from typing import Optional, Tuple

from lapgen import bemenet
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szavak
from lapgen.ertekek import MaradtFajta, Megbizhatosag
from lapgen.szamitas import vizsgalat
from lapgen.szamitas.vizsgalat import Vizsgalat, html_ben
from lapgen.szoveg import Horgony, Igehely, Kulcs, Lathato, Strong, idezet, proza


@dataclasses.dataclass(frozen=True)
class Targy:
    """A keresés tárgya megszámolva: a lánc héber és görög szavainak, valamint a szópároknak a száma. A kritérium
    szövege nem áll itt: annak egyetlen teljes helye a lap eleje, a szakasz oda hivatkozik (DT-F218n)."""
    heber: int
    gorog: int
    szoparok: int


@dataclasses.dataclass(frozen=True)
class LancSzo:
    """A lánc egy szava: a szótári alak, a kiejtés és a rövid magyar jelentés. Az `alak` hiánya: a szó nincs a
    szótárban (a lapon ilyenkor a Strong-száma áll); a `kiejtes` és a `jelentes` hiánya kimondott hiány."""
    strong: Strong
    alak: Optional[Lathato]
    kiejtes: Optional[Lathato]
    jelentes: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class MaradtHely:
    """A motívum egy helye a csoportjában: az igehely és a funkciójának magyarázata (kézi próza)."""
    igehely: Igehely
    horgony: Horgony
    magyarazat: Optional[Lathato]


@dataclasses.dataclass(frozen=True)
class MaradtCsoport:
    """A motívum helyei egy hordozó elemen: a lánc szava vagy szavai (`szavak`), kézzel elnevezett szópár (`nevek`),
    vagy a lánc szavai nélküli, tematikus helyek. A három szám a helyek megoszlása."""
    fajta: MaradtFajta
    szavak: Tuple[LancSzo, ...]
    nevek: Tuple[Lathato, ...]
    helyek: Tuple[MaradtHely, ...]
    genezis: int
    oszovetseg: int
    ujszovetseg: int


@dataclasses.dataclass(frozen=True)
class Hatareset:
    """Nem magas megbízhatóságú azonosítás: a hely és a megbízhatóság kulcsa (olvasói neve a névtáblában)."""
    igehely: Igehely
    horgony: Horgony
    megbizhatosag: Kulcs


@dataclasses.dataclass(frozen=True)
class DontesiUt:
    vizsgalat: Vizsgalat
    targy: Targy
    szavak: Tuple[LancSzo, ...]
    maradt: Tuple[MaradtCsoport, ...]
    hataresetek: Tuple[Hatareset, ...]
    kerdesek: Tuple[Lathato, ...]


def _opcionalis(kezi):
    return proza(kezi) if kezi is not None else None


def szamit(korny):
    """A szakasz lapmodellje. A helyek a tábla rendjében állnak (a csoportok az első helyük rendjében)."""
    b, motivum = korny.b, korny.motivum
    v = vizsgalat.szamit(korny)
    sorok = sorted(bemenet.b03_elofordulasok(b, motivum), key=lambda s: s.fajl_sorszam)
    konyvek = bemenet.b63_konyvek(b)
    kiejtes = szavak.kiejtes(b)
    karoli = bemenet.b07_karoli(b)
    versek = tuple(vers for s in sorok for vers in karoli.versek(s.igehely))
    jelentes = motivum_be.rovid_jelentes(b)
    lancszavak = {}

    def lancszo(strong):
        if strong not in lancszavak:
            szo = kiejtes.szotari(strong, versek)
            magyar = jelentes.magyar(strong)
            lancszavak[strong] = LancSzo(
                strong=strong,
                alak=idezet(html_ben(szo.alak)) if szo is not None else None,
                kiejtes=idezet(html_ben(szo.kiejtes)) if szo is not None and szo.kiejtes is not None else None,
                jelentes=idezet(html_ben(magyar)) if magyar is not None else None)
        return lancszavak[strong]

    # a lánc szavai: a hordozó elemek Strong-részei; a héber szavak elöl, azon belül a Strong-szám rendjében
    lanc = []
    for s in sorok:
        lanc.extend(resz for resz in s.gerinc_reszek if isinstance(resz, Strong) and resz not in lanc)
    lanc.sort(key=lambda strong: (not strong.heber, strong.kod))

    csoportok = {}
    for s in sorok:
        if not s.tematikus and not s.gerinc_reszek:
            raise bemenet.BemenetHiba('B03: a(z) %s sor nem nevezi meg a hordozó elemét' % s.igehely.kod)
        csoportok.setdefault(s.gerinc_reszek, []).append(s)
    maradt = []
    for reszek, tagok in csoportok.items():
        strongok = tuple(r for r in reszek if isinstance(r, Strong))
        if tagok[0].tematikus:
            fajta = MaradtFajta.TEMATIKUS
        elif len(strongok) == len(reszek):
            fajta = MaradtFajta.SZO
        elif not strongok:
            fajta = MaradtFajta.NEVES_SZOPAR
        else:
            raise bemenet.BemenetHiba('B03: a(z) %s sor hordozó elemének részei vagy mind Strong-számok, vagy mind '
                                      'nevek legyenek' % tagok[0].igehely.kod)
        genezis = sum(1 for t in tagok if konyvek.elso(t.igehely.konyv))
        ujszov = sum(1 for t in tagok if konyvek.ujszovetsegi(t.igehely.konyv))
        maradt.append(MaradtCsoport(
            fajta=fajta,
            szavak=tuple(lancszo(strong) for strong in strongok) if fajta is MaradtFajta.SZO else (),
            nevek=tuple(proza(html_ben(r)) for r in reszek) if fajta is MaradtFajta.NEVES_SZOPAR else (),
            helyek=tuple(MaradtHely(t.igehely, t.igehely.horgony(),
                                    _opcionalis(html_ben(t.funkcio_magyarazat or t.funkcio_cimke or None)))
                         for t in tagok),
            genezis=genezis, oszovetseg=len(tagok) - genezis - ujszov, ujszovetseg=ujszov))

    return DontesiUt(
        vizsgalat=v,
        targy=Targy(heber=sum(1 for strong in lanc if strong.heber),
                    gorog=sum(1 for strong in lanc if not strong.heber),
                    szoparok=sum(1 for c in maradt if c.fajta is MaradtFajta.NEVES_SZOPAR or len(c.szavak) > 1)),
        szavak=tuple(lancszo(strong) for strong in lanc),
        maradt=tuple(maradt),
        hataresetek=tuple(Hatareset(s.igehely, s.igehely.horgony(), s.megbizhatosag_kulcs) for s in sorok
                          if s.megbizhatosag is not None and s.megbizhatosag is not Megbizhatosag.MAGAS),
        kerdesek=tuple(proza(k) for k in motivum_be.b47_nyitott_kerdesek(b, motivum)))


def kapu(modell):
    """A szakasz kapuja a modellen (GK-09, GK-21): a vizsgálat számegyezése; a keresés tárgyának két szószáma a
    lánc szavainak száma; a csoportok helyeinek összege a
    motívum helyeinek száma; csoportonként a megoszlás három száma a helyek száma."""
    vizsgalat.kapu(modell.vizsgalat)
    if modell.targy.heber + modell.targy.gorog != len(modell.szavak):
        raise vizsgalat.KapuHiba('a Döntési út %d héber és %d görög szót számol, a lánc szavainak száma %d'
                                 % (modell.targy.heber, modell.targy.gorog, len(modell.szavak)))
    if sum(len(c.helyek) for c in modell.maradt) != modell.vizsgalat.helyek:
        raise vizsgalat.KapuHiba('a Döntési út csoportjaiban %d hely áll, a motívumnak %d helye van'
                                 % (sum(len(c.helyek) for c in modell.maradt), modell.vizsgalat.helyek))
    for csoport in modell.maradt:
        if csoport.genezis + csoport.oszovetseg + csoport.ujszovetseg != len(csoport.helyek) or not csoport.helyek:
            raise vizsgalat.KapuHiba('a Döntési út egy csoportjának megoszlása nem adja ki a helyei számát (%d)'
                                     % len(csoport.helyek))
    return modell
