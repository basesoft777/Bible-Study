"""lapgen.szamitas.szocikkek — a „Szótári háttér” szakasz lapmodellje.

A szakasz a motívum szavait tárgyalja: elöl az áttekintő tábla, azután nyelvenként a szótári pontok (a pontok rendje
a szótári pontok táblájából jön), végül a nyelvfüggetlen pontok. Ez a modul a vázat, az áttekintést és az egyszerű
pontokat számolja (alapjelentés, teológiai szócikk, szemantikai mező, kiejtés); a többi pont saját modulból jön.
Mondatot nem fogalmaz: azt a megjelenítő teszi a sablontáblából.

Fordítás-állapot (GK-15, T5): ahol a magyar szöveg hiányzik (az angol eredeti áll, „fordításra vár”) vagy elavult,
azt a modell tételesen felsorolja (`forditas_allapot`); kiadási módban a kapu ilyen tétellel megáll.
"""
import dataclasses
import enum
from typing import Optional, Tuple

from lapgen import bemenet, konfig
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.bemenet import szotari as szotari_be
from lapgen.bemenet import ubs as ubs_be
from lapgen.szamitas import elofordulas as elofordulas_sz
from lapgen.szamitas import szotari_karoli, szotari_nave, szotari_sece
from lapgen.szamitas.szotari_karoli import KaroliPontok
from lapgen.szamitas.szotari_nave import Tematikus
from lapgen.szamitas.szotari_sece import Sece
from lapgen.szamitas.szotari_tipusok import Jelentes, Szo, Szoveg
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Igehely, Lathato, Proveniencia, Strong, idezet, prov


class Nyelv(enum.Enum):
    GOROG = szotari_be.NYELV_GOROG
    HEBER = szotari_be.NYELV_HEBER


class Fok(enum.Enum):
    """Egy arány fokozata a következtetés mondatához (a küszöbök: `konfig.FOKOK`)."""
    SZINTE = 'szinte'
    TOBBSEG = 'tobbseg'
    FELE = 'fele'
    KEVES = 'keves'


def fok(arany):
    return Fok(next(nev for kuszob, nev in konfig.FOKOK if arany >= kuszob))


class ForditasFajta(enum.Enum):
    HIANYZIK = 'hianyzik'   # nincs magyar szöveg: az angol eredeti áll
    ELAVULT = 'elavult'     # a magyar szöveg forrása azóta megváltozott


@dataclasses.dataclass(frozen=True)
class ForditasJelzes:
    """A fordítás-állapot egy tétele: mi a baj, és melyik szöveggel (belső leírás, megjegyzésbe való)."""
    fajta: ForditasFajta
    hol: Proveniencia


class ForditasAllapot:
    """A szakasz fordítás-állapotának gyűjtője (a számítás alatt töltődik, a modellbe változtathatatlanul kerül)."""

    def __init__(self):
        self._tetelek = []

    def jelez(self, fajta, szotar, strong, mezo):
        self._tetelek.append(ForditasJelzes(fajta, prov('{} {} {}', szotar, strong, mezo)))

    def tetelek(self):
        return tuple(self._tetelek)


@dataclasses.dataclass(frozen=True)
class AttekintoSor:
    """Az áttekintő tábla egy sora. A `tars` a Septuaginta-megfelelő: héber szónál a legerősebben társuló görög
    szó, görög szónál a motívum héber szavai közül a legerősebben társuló; None, ha nincs a küszöb fölötti társ."""
    szo: Szo
    jelentes: Jelentes
    tars: Optional[Szo]
    tars_versek: int
    helyek: int


@dataclasses.dataclass(frozen=True)
class SzoJelentes:
    szo: Szo
    jelentes: Jelentes


@dataclasses.dataclass(frozen=True)
class Teologiai:
    """A teológiai szócikk pontjának egy sora: a translationWords szócikkcímei, héber szónál a TWOT-számok (`None`:
    a nyelvnek nincs ilyen száma; üres: a szónak nincs száma)."""
    szo: Szo
    cimek: Tuple[Szoveg, ...]
    twot: Optional[Tuple[Lathato, ...]]


@dataclasses.dataclass(frozen=True)
class DomenSor:
    """A szemantikai mező pontjának egy sora: a domének neve; az elemzetlen bejegyzések belső leírása megjegyzésbe."""
    szo: Szo
    domenek: Tuple[Szoveg, ...]
    elemzetlen: Tuple[Proveniencia, ...]


@dataclasses.dataclass(frozen=True)
class VersenkentiSzo:
    """A versenkénti jelentés pontjának egy sora: a szó helyei a nyelve szövetségében, és ebből hány helyen áll a
    szótár egy jelentésében, hány helyen több lehetségesben, hány helyen nincs hozzárendelés. A `nem_egy` a nem egy
    jelentésű helyek igehelye."""
    szo: Szo
    helyek: int
    egy: int
    tobb: int
    nem_egy: Tuple[Igehely, ...]


@dataclasses.dataclass(frozen=True)
class Versenkenti:
    """A versenkénti jelentés pontja: szavanként a számok, a nyelv különböző helyeinek száma, és a következtetés
    fokozata (None: kis elemszámnál nincs következtetés)."""
    szavak: Tuple[VersenkentiSzo, ...]
    hely_szam: int
    fok: Optional[Fok]


@dataclasses.dataclass(frozen=True)
class Nyelvresz:
    """Egy nyelv szavai és pontjai. A `pontok` a nyelv saját pontjainak sorszámai a tábla rendjében."""
    nyelv: Nyelv
    szavak: Tuple[Szo, ...]
    pontok: Tuple[int, ...]
    rovid_szotar_licenc: Lathato
    alapjelentes: Tuple[SzoJelentes, ...]
    teologiai: Tuple[Teologiai, ...]
    tw_licenc: Lathato
    domen: Tuple[DomenSor, ...]
    sece: Sece
    versenkent: Versenkenti


@dataclasses.dataclass(frozen=True)
class Szocikkek:
    kiadas: bool
    szavak: Tuple[Szo, ...]                 # a motívum minden szava: a héber szavak elöl, a Strong-szám rendjében
    attekintes: Tuple[AttekintoSor, ...]
    nyelvek: Tuple[Nyelvresz, ...]          # görög, héber: mindkettő áll, szavak nélkül is (kimondott hiány)
    kozos_pontok: Tuple[int, ...]
    tematikus: Optional[Tematikus]          # a 4.12 pont; None, ha a motívumnak nincs döntése a témákról
    karoli: KaroliPontok                    # a 4.13 és a 4.14 pont; ha a motívumon nem épülnek, a két mező None
    forditas_allapot: Tuple[ForditasJelzes, ...]


class _Forrasok:
    """A szakasz bemenetei egy helyen."""

    def __init__(self, b, motivum):
        self.b = b
        self.sorok = bemenet.b03_elofordulasok(b, motivum)
        karoli = bemenet.b07_karoli(b)
        self.versek = tuple(vers for s in self.sorok for vers in karoli.versek(s.igehely))
        self.kiejtes = szavak_be.kiejtes(b)
        self.rovid = motivum_be.rovid_jelentes(b)
        self.forditasok = ubs_be.b14_forditasok(b)
        self.licencek = bemenet.b01_licencek(b)
        self.allapot = ForditasAllapot()
        self.konyvek = bemenet.b63_konyvek(b)
        self._szavak = {}
        self._ubs_cellak = None

    def tablaban(self, burkolo):
        return tablaban(burkolo)

    def ubs_cellak(self):
        """A motívum sorainak UBS-cellái (a 2. tábla számításával), egyszer kiszámolva."""
        if self._ubs_cellak is None:
            self._ubs_cellak = elofordulas_sz.ubs_cellak(self.b, self.sorok)
        return self._ubs_cellak

    def szo(self, strong):
        """A szó szótári alakja és kiejtése (a változat a motívum versei szerint, GK-13)."""
        if strong not in self._szavak:
            szotari = self.kiejtes.szotari(strong, self.versek)
            self._szavak[strong] = Szo(
                strong=strong,
                alak=idezet(tablaban(szotari.alak)) if szotari is not None else None,
                kiejtes=idezet(tablaban(szotari.kiejtes)) if szotari is not None and szotari.kiejtes is not None
                else None)
        return self._szavak[strong]

    def jelentes(self, strong):
        """A szó rövid jelentése az egy glossza-úton (GK-16); a hiányt és az elavulást az állapot gyűjti."""
        rovid = self.rovid.jelentes(strong)
        if rovid.magyar is None and rovid.angol is not None:
            self.allapot.jelez(ForditasFajta.HIANYZIK, konfig.SZOTAR_ROVID, strong, konfig.MEZO_ROVID_JELENTES)
        if rovid.elavult:
            self.allapot.jelez(ForditasFajta.ELAVULT, konfig.SZOTAR_ROVID, strong, konfig.MEZO_ROVID_JELENTES)
        return Jelentes(
            magyar=idezet(tablaban(rovid.magyar)) if rovid.magyar is not None else None,
            angol=idezet(tablaban(rovid.angol)) if rovid.magyar is None and rovid.angol is not None else None,
            elavult=rovid.elavult)

    def forditott(self, szotar, strong_kod, szocikk, jelentes_szam, angol, hely):
        """Egy rövid forrásszöveg magyarul a fordítástáblából; ha nincs, az angol eredeti (fordításra vár)."""
        forditas = self.forditasok.forditas(szotar, strong_kod, szocikk, jelentes_szam, konfig.UBS_GLOSSZA_MEZO, hely)
        if forditas is None:
            self.allapot.jelez(ForditasFajta.HIANYZIK, szotar, hely, szocikk)
            return Szoveg(idezet(tablaban(angol)), True)
        if forditas.elavult:
            self.allapot.jelez(ForditasFajta.ELAVULT, szotar, hely, szocikk)
        return Szoveg(idezet(tablaban(forditas.szoveg)), False, forditas.elavult)


_TABLA_JELEK = ('|', '\n')


def tablaban(burkolo):
    """Kapu a táblacellába és a listasorba kerülő forrásszövegre: cellahatár (`|`) vagy sortörés nem állhat benne.
    A generátor a szöveget nem írja át (nem is kódolja át): az ilyen szöveg a forrásban javítandó."""
    if burkolo is not None and any(jel in burkolo.ertek for jel in _TABLA_JELEK):
        raise bemenet.BemenetHiba('a(z) `%s` mező szövege cellahatárt vagy sortörést tartalmaz, ezért a lap '
                                  'táblájába nem kerülhet: %s' % (burkolo.mezo, burkolo.ertek[:80]))
    return burkolo


def motivum_szavai(sorok):
    """A motívum szavai (az előfordulás-sorok Strong-számai): a héber szavak elöl, azon belül a szám rendjében."""
    return tuple(sorted({strong for s in sorok for strong in s.strongok}, key=lambda st: (not st.heber, st.kod)))


# --- az áttekintő tábla: a Septuaginta-megfelelő -----------------------------------------------------------------


class Tarsulas:
    """A héber szó és a görög szó versszintű társulása a Septuagintában (Dice-mérték): a közös versek kétszerese
    osztva a két szó verseinek összegével. A görög szó versszáma a teljes Septuagintából jön."""

    def __init__(self, b):
        self._parok = szotari_be.b36_lxx_parok(b)
        self._gorog_versszam = None
        self._b = b

    def _nevezo(self, gorog_kod, kozos):
        if self._gorog_versszam is None:
            self._gorog_versszam = szotari_be.b35_lxx_szo_versszam(self._b)
        return self._gorog_versszam.get(gorog_kod, kozos)

    def mertek(self, heber, gorog_kod):
        """(társulás, közös versek) a héber szó és a görög szó között."""
        versek = self._parok.versek(heber)
        if not versek:
            return 0.0, 0
        kozos = sum(1 for gorogok in versek.values() if gorog_kod in gorogok)
        if not kozos:
            return 0.0, 0
        return 2.0 * kozos / (len(versek) + self._nevezo(gorog_kod, kozos)), kozos

    def tarsak(self, heber):
        """A héber szó görög társai a társulás csökkenő rendjében, a küszöb fölött: [(görög Strong, közös versek)]."""
        versek = self._parok.versek(heber)
        if not versek:
            return ()
        jeloltek = sorted({g for gorogok in versek.values() for g in gorogok})
        pontok = sorted(((self.mertek(heber, g), g) for g in jeloltek), key=lambda x: (-x[0][0], x[1]))
        return tuple((Strong(g), kozos) for (mertek, kozos), g in pontok if mertek >= konfig.LXX_TARS_KUSZOB)

    def heber_tars(self, gorog, heberek):
        """A görög szóhoz a motívum héber szavai közül a legerősebben társuló: (héber Strong, közös versek), vagy
        None, ha egyik sem éri el a küszöböt. Egyenlő társulásnál a szavak rendjében az első."""
        legjobb = None
        for heber in heberek:
            mertek, kozos = self.mertek(heber, gorog.kod)
            if legjobb is None or mertek > legjobb[0]:
                legjobb = (mertek, kozos, heber)
        if legjobb is None or legjobb[0] < konfig.LXX_TARS_KUSZOB:
            return None
        return legjobb[2], legjobb[1]


def tarsulas(b):
    return b.egyszer('lxx_tarsulas', lambda: Tarsulas(b))


def _attekintes(f, szavak):
    t = tarsulas(f.b)
    heberek = tuple(s for s in szavak if s.heber)
    ki = []
    for strong in szavak:
        if strong.heber:
            tarsak = t.tarsak(strong)
            tars = tarsak[0] if tarsak else None
        else:
            tars = t.heber_tars(strong, heberek)
        ki.append(AttekintoSor(
            szo=f.szo(strong), jelentes=f.jelentes(strong),
            tars=f.szo(tars[0]) if tars is not None else None, tars_versek=tars[1] if tars is not None else 0,
            helyek=sum(1 for s in f.sorok if strong in s.strongok)))
    return tuple(ki)


# --- az egyszerű pontok ------------------------------------------------------------------------------------------


def _teologiai(f, strong):
    tw, twot = szotari_be.b29_tw(f.b), szotari_be.b30_twot(f.b)
    cimek = tuple(f.forditott(konfig.SZOTAR_TW, cikk.elso_strong, cikk.azonosito, konfig.TW_CIM_KULCS, cikk.cim, strong)
                  for cikk in tw.get(strong.kod, ()))
    return Teologiai(szo=f.szo(strong), cimek=cimek,
                     twot=tuple(idezet(tablaban(szam)) for szam in twot.get(strong.kod, ())) if strong.heber else None)


def _domen(f, strong):
    domenek = szotari_be.b31_domenek(f.b)
    szotar = konfig.SZOTAR_SDBH if strong.heber else konfig.SZOTAR_SDGNT
    return DomenSor(
        szo=f.szo(strong),
        domenek=tuple(f.forditott(szotar, strong.kod, kod, konfig.DOMEN_KULCS, nev, strong)
                      for kod, nev in domenek.domenek(strong)),
        elemzetlen=tuple(prov('{}', leiras) for leiras in domenek.anomaliak(strong)))


def _versenkenti(f, nyelv, sajat):
    """A versenkénti jelentés számai a 2. tábla UBS-cellájának modelljéből: a szó a nyelve szövetségének soraiban
    számít (héber szó az ószövetségi, görög az újszövetségi sorokban)."""
    heber = nyelv is Nyelv.HEBER
    cellak = [(sor, cella) for sor, cella in f.ubs_cellak()
              if f.konyvek.ujszovetsegi(sor.igehely.konyv) != heber]
    szavak = []
    for strong in sajat:
        helyek = egy = tobb = 0
        nem_egy = []
        for sor, cella in cellak:
            if strong not in sor.strongok:
                continue
            helyek += 1
            jelentesek = [g for t in cella.tokenek if t.strong == strong for g in t.glosszak if g.glossza is not None]
            if not jelentesek:
                nem_egy.append(sor.igehely)
            elif len(jelentesek) > 1 or any(g.nem_egyertelmu for g in jelentesek):
                tobb += 1
                nem_egy.append(sor.igehely)
            else:
                egy += 1
        szavak.append(VersenkentiSzo(f.szo(strong), helyek, egy, tobb, tuple(nem_egy)))
    hely_szam = len({sor.igehely for sor, _c in cellak if any(s in sajat for s in sor.strongok)})
    vannak = [s for s in szavak if s.helyek]
    kovetkeztetes = None
    if vannak and max(s.helyek for s in vannak) > konfig.VERSENKENTI_KIS:
        kovetkeztetes = fok(sum(s.egy for s in vannak) / sum(s.helyek for s in vannak))
    return Versenkenti(tuple(szavak), hely_szam, kovetkeztetes)


def _nyelvresz(f, nyelv, szavak, szerepek):
    sajat = tuple(s for s in szavak if szotari_be.nyelv_kulcs(s) == nyelv.value)
    return Nyelvresz(
        nyelv=nyelv,
        szavak=tuple(f.szo(s) for s in sajat),
        pontok=szerepek.nyelvi(nyelv.value),
        rovid_szotar_licenc=idezet(f.licencek.cimke(konfig.LICENC_ROVID_SZOTAR[nyelv.value])),
        alapjelentes=tuple(SzoJelentes(f.szo(s), f.jelentes(s)) for s in sajat),
        teologiai=tuple(_teologiai(f, s) for s in sajat),
        tw_licenc=idezet(f.licencek.cimke(konfig.LICENC_TW)),
        domen=tuple(_domen(f, s) for s in sajat),
        sece=szotari_sece.szamit(f, nyelv is Nyelv.HEBER, sajat, szavak),
        versenkent=_versenkenti(f, nyelv, sajat))


def szamit(korny):
    """A szakasz lapmodellje."""
    f = _Forrasok(korny.b, korny.motivum)
    szavak = motivum_szavai(f.sorok)
    szerepek = szotari_be.b52_szerepek(korny.b)
    attekintes = _attekintes(f, szavak)
    nyelvek = tuple(_nyelvresz(f, nyelv, szavak, szerepek) for nyelv in (Nyelv.GOROG, Nyelv.HEBER))
    return Szocikkek(
        kiadas=korny.mod.value == konfig.MOD_KIADAS,
        szavak=tuple(f.szo(s) for s in szavak),
        attekintes=attekintes,
        nyelvek=nyelvek,
        kozos_pontok=szerepek.kozos(),
        tematikus=szotari_nave.szamit(f, korny.motivum),
        karoli=szotari_karoli.szamit(f, korny.motivum),
        forditas_allapot=f.allapot.tetelek())


def kapu(modell):
    """A szakasz kapuja a modellen: kiadási módban hiányzó vagy elavult fordítással a lap nem készül el (GK-15);
    az áttekintő tábla minden szóról szól, és a szavak a két nyelvrész között maradék nélkül oszlanak meg."""
    if modell.kiadas and modell.forditas_allapot:
        raise KapuHiba('kiadási módban a szótári háttér %d szövege hiányzó vagy elavult fordítással áll'
                       % len(modell.forditas_allapot))
    if len(modell.attekintes) != len(modell.szavak):
        raise KapuHiba('az áttekintő tábla %d sora nem a motívum %d szava'
                       % (len(modell.attekintes), len(modell.szavak)))
    if sum(len(resz.szavak) for resz in modell.nyelvek) != len(modell.szavak):
        raise KapuHiba('a nyelvenkénti szavak száma nem adja ki a motívum szavainak számát (%d)' % len(modell.szavak))
    szotari_nave.kapu(modell.tematikus)
    return modell
