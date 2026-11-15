"""lapgen.szamitas.kartya — a 4.2 Mélységi szócikk lapmodellje (S3b: BDB; S3c: Thayer).

A kártya tartalmát a bemeneti réteg állítja elő (`bemenet.kartya_lap`: a szótár szövegéből a szegmentált idézet, a
glosszák, a pontok); itt a lapmodell készül belőle, kötött típusokkal: a szövegdarab látható szöveg (idézet vagy kézi
próza), a jelölés a fajtája és a típusos adata. A görög kártya alatt az UBS-doménsor is itt számol (a fordítástábla
útján, mint a 4.9 cellái).
"""
import dataclasses
import enum
from typing import Optional, Tuple

from lapgen import konfig
from lapgen.bemenet import kartya_lap as KL
from lapgen.bemenet import ubs as ubs_be
from lapgen.bemenet.jelolt import Jeloles
from lapgen.ertekek import FeloldasFajta, JelFajta
from lapgen.szamitas.szotari_tipusok import Szoveg
from lapgen.szoveg import Forrasszoveg, Igehely, Kezi, Lathato, Proveniencia, Strong, idezet, prov, proza


class OlvasoiFajta(enum.Enum):
    SZOCIKK = 'szocikk'
    TAGOLATLAN = 'tagolatlan'
    FEJ_ELEJE = 'fej_eleje'
    SZAKASZ = 'szakasz'


class Tartalom(enum.Enum):
    GLOSSZA = 'glossza'
    CSAK_ALAK = 'csak_alak'
    CSAK_ALAK_THAYER = 'csak_alak_thayer'
    CSAK_PARHUZAM = 'csak_parhuzam'
    FORDITASRA_VAR = 'forditasra_var'
    KULON = 'kulon'


class PontFajta(enum.Enum):
    SZAKASZ = 'szakasz'
    TAGOLATLAN = 'tagolatlan'
    FEJ_ELEJE = 'fej_eleje'
    CSAK_ALAKKENT = 'csak_alakkent'


class Bizonytalansag(enum.Enum):
    SIGLA_KOZEL = 'sigla_kozel'
    TOBBERTELMU = 'tobbertelmu'
    ISMERETLEN_ALAK = 'ismeretlen_alak'
    NINCS_ELOZMENY = 'nincs_elozmeny'
    OROKLES_HIBAS = 'orokles_hibas'
    FORRAS_HIBA = 'forras_hiba'
    ATKULCSOLT_BIZONYTALAN = 'atkulcsolt_bizonytalan'
    KETES_PONT = 'ketes_pont'


class AppFajta(enum.Enum):
    FEJCIM = 'fejcim'
    FEJ = 'fej'
    SZAKASZ = 'szakasz'
    FUTAM = 'futam'


@dataclasses.dataclass(frozen=True)
class KartyaJel:
    """A szegmentált idézet egy darabja: idézet (`ertek`) vagy jelölés a típusos adatával."""
    fajta: JelFajta
    ertek: Optional[Lathato] = None          # az idézet-darab; a Károli-számozásnál a Károli-alak; a kiejtés
    eredeti: Optional[Lathato] = None        # a Károli-számozás eredeti (héber) száma
    vers: Optional[Igehely] = None           # a kiemelés címe
    feloldas: Optional[FeloldasFajta] = None
    tapadt: bool = False                     # a csonkítás jele szóköz nélkül


@dataclasses.dataclass(frozen=True)
class OlvasoiSor:
    fajta: OlvasoiFajta
    behuzas: int = 0
    sorszam: int = 0
    arami: bool = False
    felkover: bool = False
    jel: Optional[Lathato] = None
    jel_nyers: Optional[Lathato] = None
    jel_szam: bool = False
    gondolatjel: bool = False
    tartalom: Tartalom = Tartalom.GLOSSZA
    glossza: Optional[Lathato] = None
    hely_db: int = 0


@dataclasses.dataclass(frozen=True)
class PontNev:
    fajta: PontFajta
    szocikk_sorszam: int = 0                 # 0: a szónak egy szócikke van
    szocikk_arami: bool = False
    jel: Optional[Lathato] = None
    gondolatjel: bool = False
    glossza: Optional[Lathato] = None
    bizonytalan: Tuple[Bizonytalansag, ...] = ()


@dataclasses.dataclass(frozen=True)
class HelyCsoport:
    versek: Tuple[Igehely, ...]
    nevek: Tuple[PontNev, ...]


@dataclasses.dataclass(frozen=True)
class Vazlat:
    jel: Lathato
    darabok: Tuple[KartyaJel, ...]           # az első tagmondat; vagy a kézi címke egyetlen idézet-darab helyett:
    cimke: Optional[Lathato] = None


@dataclasses.dataclass(frozen=True)
class Futam:
    jelek: Tuple[Lathato, ...]
    glosszak: Tuple[Lathato, ...]
    hely_db: int
    vazlatok: Tuple[Vazlat, ...]


@dataclasses.dataclass(frozen=True)
class AppElem:
    fajta: AppFajta
    darabok: Tuple[KartyaJel, ...] = ()      # a fej, a kibontott szakasz idézete, a fejcím címszava
    szam: int = 0                            # a fejcím BDB-száma
    arami: bool = False
    sorszam: int = 0
    osszes: int = 0
    van_cimszo: bool = False
    jel: Optional[Lathato] = None
    cim: Optional[Lathato] = None
    futam: Optional[Futam] = None


@dataclasses.dataclass(frozen=True)
class Megjegyzes:
    vers: Igehely
    jel: Lathato
    kezdo: Igehely
    veg: int
    nyers: Lathato
    folytatas: Lathato


@dataclasses.dataclass(frozen=True)
class UbsElem:
    kod: Lathato
    szoveg: Szoveg


@dataclasses.dataclass(frozen=True)
class Kartya:
    strong: Strong
    olvasoi: Tuple[OlvasoiSor, ...]
    helyein: Tuple[HelyCsoport, ...]
    nem_idezett: Tuple[Igehely, ...]
    tartomanyban: Tuple[Igehely, ...]
    pont_nelkul: Tuple[Igehely, ...]
    apparatus: Tuple[AppElem, ...]
    megjegyzes: Tuple[Megjegyzes, ...]
    ubs: Optional[Tuple[UbsElem, ...]] = None
    forras: Optional[Proveniencia] = None    # a görög kártya forrássora (megjegyzésbe)


# --- a bemenet eredményéből a lapmodell ----------------------------------------------------------------------------
def _l(ertek):
    if ertek is None:
        return None
    if isinstance(ertek, Forrasszoveg):
        return idezet(ertek)
    if isinstance(ertek, Kezi):
        return proza(ertek)
    raise TypeError(type(ertek).__name__)


def darabok(b, jelolt):
    ki = []
    for d in jelolt.darabok(b):
        if not isinstance(d, Jeloles):
            ki.append(KartyaJel(JelFajta.IDEZET, ertek=idezet(d)))
        elif d.fajta is JelFajta.MARK_NYIT:
            ki.append(KartyaJel(d.fajta, vers=d.adat))
        elif d.fajta is JelFajta.ABBR_NYIT:
            ki.append(KartyaJel(d.fajta, feloldas=d.adat.fajta))
        elif d.fajta is JelFajta.KAROLI:
            ki.append(KartyaJel(d.fajta, ertek=idezet(d.adat[0]), eredeti=idezet(d.adat[1])))
        elif d.fajta is JelFajta.KIEJTES:
            ki.append(KartyaJel(d.fajta, ertek=idezet(d.adat)))
        elif d.fajta is JelFajta.CSONK:
            ki.append(KartyaJel(d.fajta, tapadt=d.adat))
        else:
            ki.append(KartyaJel(d.fajta))
    return tuple(ki)


def _olvasoi(s):
    return OlvasoiSor(OlvasoiFajta(s.fajta), s.behuzas, s.sorszam, s.arami, s.felkover, _l(s.jel), _l(s.jel_nyers),
                      s.jel_szam, s.gondolatjel, Tartalom(s.tartalom), _l(s.glossza), s.hely_db)


def _pont(n):
    sorszam, arami = n.szocikk if n.szocikk is not None else (0, False)
    return PontNev(PontFajta(n.fajta), sorszam, arami, _l(n.jel), n.gondolatjel, _l(n.glossza),
                   tuple(Bizonytalansag(o) for o in n.bizonytalan))


def _app(b, e):
    fajta = AppFajta(e.fajta)
    if fajta is AppFajta.FEJCIM:
        szam, cimszo, arami, i, n = e.adat
        return AppElem(fajta, darabok(b, cimszo) if cimszo is not None else (), szam, arami, i, n, cimszo is not None)
    if fajta is AppFajta.FEJ:
        return AppElem(fajta, darabok(b, e.adat))
    if fajta is AppFajta.SZAKASZ:
        jel, cim, j = e.adat
        return AppElem(fajta, darabok(b, j), jel=_l(jel), cim=_l(cim))
    oc = e.adat
    vazlatok = tuple(Vazlat(_l(jel), darabok(b, t), None) if isinstance(t, KL.Jelolt) else Vazlat(_l(jel), (), _l(t))
                     for jel, t in oc.vazlatok)
    return AppElem(fajta, futam=Futam(tuple(_l(j) for j in oc.jelek), tuple(_l(g) for g in oc.glosszak), oc.hely_db,
                                      vazlatok))


def thayer_forras(forditasok):
    """A Thayer-kártya magyar szövegének forrássora (megjegyzés)."""
    return prov('forrás: `{}`, `sz<n>` sorok, #142; DT373', forditasok.utvonal())


def modell(b, k, ubs=None, forras=None):
    """A bemenet kártyájából (`bemenet.kartya_lap.Kartya`) a lapmodell."""
    return Kartya(
        strong=k.strong,
        olvasoi=tuple(_olvasoi(s) for s in k.olvasoi),
        helyein=tuple(HelyCsoport(c.versek, tuple(_pont(n) for n in c.nevek)) for c in k.helyein),
        nem_idezett=k.nem_idezett, tartomanyban=k.tartomanyban, pont_nelkul=k.pont_nelkul,
        apparatus=tuple(_app(b, e) for e in k.apparatus),
        megjegyzes=tuple(Megjegyzes(vers, _l(jel), t.kezdo_vers, t.veg, _l(t.nyers), _l(t.folytatas_idezet))
                         for vers, t, jel in k.megjegyzes),
        ubs=ubs, forras=forras)


def ubs_sor(f, strong):
    """A görög kártya alatti UBS-doménsor: a szó jelentései a tábla rendjében, a magyar glosszával (a fordítástábla
    útján; híján az angol, „fordításra vár” jelöléssel)."""
    ki = []
    for kod, angol, lexid in ubs_be.b32_ubs_dntg(f.b).szo_jelentesei_burkolva(strong):
        ki.append(UbsElem(idezet(kod), f.forditott(konfig.SZOTAR_UBS_DNTG, strong.kod, lexid, kod.ertek, angol, strong)))
    return tuple(ki)
