"""lapgen.szamitas.kolofon — a Kolofon (S8d): a szakasz modellje.

A Kolofon négy részből áll: (1) a szerzőségi mondat és a közleményekre kötött bekezdések (hogyan idézd, módszertani
elvek, hatókör); (2) a motívum azonosító táblája, a kiadás és a lektorálás soraival; (3) a változásjegyzék; (4) a lap
forrástáblája (forrásonként a licenc és az olvasó szakaszok) és alatta a kötelező forrásmegjelölések.

A forrástábla a 12. szakasz forrás-halmazát használja (DT901: a számozott szakaszok és alrészeik valódi olvasásai, a
jegyzék `irodalom` oszlopa szerint szűrve; a tanúk és a Vulgata külső forrásai a tábláik ellenőrzött soraiból; a származtatott tábla
CC BY-os bemenetei saját soron, a saját licencükkel: F212, `konfig.KOLOFON_SZARMAZTATOTT`); a
forrás neve szótárfájlnál a `kolofon_szotar`, adatfájlnál az `irod_adat`, külső forrásnál az `irod_kulso` névtábla-sor,
az azonos nevű fájlok egy sorba vonódnak, a sorok a név szerinti rendben. A megjelölendő források halmaza és rendje a
`konfig.KOLOFON_MEGJELOLES`; a szöveg a licencleltárból jön (GK-07).

A jóváhagyás (T9, GK-27): munka módban a szerzőségi mondat a szerző korábbi jóváhagyását mondja, a legutóbbi átnézés
(híján a legutóbbi kiadás) dátumával; kiadás módban a jóváhagyás frissességét a lap `lap_commit`-ja igazolná, ezt az új
generátor a 218c-ig nem tudja: a kapu megáll (DT-F218y 2.).
"""
import datetime
import enum
from dataclasses import dataclass
from typing import Optional, Tuple

from lapgen import konfig
from lapgen.bemenet import b01_licencek
from lapgen.bemenet import irodalom as irodalom_be
from lapgen.bemenet import kolofon as kolofon_be
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szamitas.idezes import Licenc, licenc_lista
from lapgen.szoveg import Kulcs, Lathato, idezet, proza


class Szerzoseg(enum.Enum):
    """A szerzőségi mondat alakja."""
    GENERALT = 'generalt'       # nincs kézi rés: a lap minden szakasza generált
    KIADATLAN = 'kiadatlan'     # van kézi rés, de a lap nincs kiadva: a szerző nem hagyta jóvá
    KIADOTT = 'kiadott'         # kiadott lap kézi résekkel: a szerző jóváhagyta (munka módban: a korábbi változatot)


@dataclass(frozen=True)
class KiadasSor:
    szam: int
    datum: datetime.date
    valtozas: Lathato


@dataclass(frozen=True)
class LektorSor:
    modell: Lathato
    db: int
    datum: Optional[datetime.date]


@dataclass(frozen=True)
class ForrasSor:
    """A forrástábla egy sora: a név (névtábla-típus és kulcs), a licencek, az olvasó szakaszok azonosítói (a szakaszrend
    szerint; az alrész a szülő szakaszé)."""
    nev_tipus: str
    nev: Kulcs
    licencek: Tuple[Licenc, ...]
    szakaszok: Tuple[str, ...]


@dataclass(frozen=True)
class Megjeloles:
    """Egy kötelező forrásmegjelölés: szó szerinti idézet a licencleltárból (`szoveg`), vagy a lap saját mondata a
    forrásról (`sablon`: a `kolofon.megjeloles.<sablon>` sor; a `cimke` a licencleltár címkéje, ha a mondat kéri)."""
    szoveg: Optional[Lathato]
    sablon: Optional[str]
    cimke: Optional[Lathato]


@dataclass(frozen=True)
class Kolofon:
    szerzoseg: Szerzoseg
    resek: Tuple[str, ...]              # a kézi rések azonosítói (a címük a szakaszrend sablonsora)
    proza_modell: Optional[Lathato]     # a legutóbbi kiadás próza-modellje; None: a kiadás nem rögzíti
    jovahagyas: Optional[datetime.date]  # a szerző jóváhagyásának dátuma (kiadott lapnál)
    kiadas: bool                        # kiadás mód (a kapu ebben áll meg)
    cim: Lathato
    meghatarozas: Optional[Lathato]
    azonossag: Optional[Kulcs]
    folerendelt: Lathato                # mondatkezdő alakban (a táblacella elején áll)
    mezok: Tuple[Tuple[str, Lathato], ...]   # a motívumtábla kézi mezői (mező, érték)
    kiadasok: Tuple[KiadasSor, ...]
    javitasok: Tuple[datetime.date, ...]
    lektor: Optional[LektorSor]
    kozel_keleti: bool                  # a motívum a közel-keleti határ táblájában áll
    kozel_keleti_emlites: Optional[Lathato]
    forrasok: Tuple[ForrasSor, ...]
    megjelolesek: Tuple[Megjeloles, ...]


def _forrastabla(korny, elozo):
    sorok = {}   # csoport (a név nyers szövege) -> [típus, kulcs, licencforrások, szakaszok]
    for azonosito, olvasasok in elozo.items():
        for f in irodalom_be.irodalom_fajlok(korny.b, olvasasok):
            r = sorok.setdefault(f.kolofon_csoport, [f.kolofon_tipus, f.kulcs, [], set()])
            r[2].append(f)
            r[3].add(azonosito)
        szarm_fajlok, szarm_kulsok = irodalom_be.szarmaztatott_forrasok(korny.b, olvasasok)
        for f in szarm_fajlok:
            r = sorok.setdefault(f.kolofon_csoport, [f.kolofon_tipus, f.kulcs, [], set()])
            r[2].append(f)
            r[3].add(azonosito)
        for k in irodalom_be.kulso_forrasok(korny.b, korny.motivum, olvasasok) + szarm_kulsok:
            r = sorok.setdefault(k.csoport, [irodalom_be.NEV_KULSO, k.kulcs, [], set()])
            r[2].append(k)
            r[3].add(azonosito)
    return tuple(ForrasSor(nev_tipus=t, nev=kulcs, licencek=licenc_lista(fs), szakaszok=tuple(sorted(sz)))
                 for _csoport, (t, kulcs, fs, sz) in sorted(sorok.items(), key=lambda e: e[0].lower()))


def _megjelolesek(korny, azonositok):
    kulcsok = {korny.b.jegyzek_sor(b_id).licenc_kulcs for b_id in azonositok}
    licencek = b01_licencek(korny.b)
    ki, latott = [], set()
    for kulcs, sablon in konfig.KOLOFON_MEGJELOLES:
        if kulcs not in kulcsok:
            continue
        if sablon is not None:
            ki.append(Megjeloles(szoveg=None, sablon=sablon, cimke=idezet(licencek.cimke(kulcs))))
            continue
        for resz in licencek.megjeloles(kulcs):
            if resz.ertek not in latott:
                latott.add(resz.ertek)
                ki.append(Megjeloles(szoveg=idezet(resz), sablon=None, cimke=None))
    return tuple(ki)


def szamit(korny, elozo):
    """A szakasz modellje. `elozo`: a megelőző számozott szakaszok (és alrészeik) olvasásai ({szakasz: B-azonosítók})."""
    sor = motivum_be.b02_motivum(korny.b, korny.motivum)
    if sor.folerendelt_mondatkezdo is None:
        raise BemenetHiba('B02: üres `folerendelt_fogalom` mező (%s): a Kolofon táblájának kötelező eleme'
                          % korny.motivum.kod)
    adatok = kolofon_be.b48_kiadasi_adatok(korny.b, korny.motivum)
    kezi = motivum_be.b47_resek(korny.b, korny.motivum)
    resek = tuple(r for r in konfig.SZERZOSEG_RESEK if r in kezi)
    utolso = adatok.kiadasok[-1] if adatok.kiadasok else None
    if not resek:
        szerzoseg, jovahagyas = Szerzoseg.GENERALT, None
    elif utolso is None:
        szerzoseg, jovahagyas = Szerzoseg.KIADATLAN, None
    else:
        szerzoseg = Szerzoseg.KIADOTT
        jovahagyas = adatok.atnezesek[-1] if adatok.atnezesek else utolso.datum
    lektor = kolofon_be.b49_lektor(korny.b, korny.motivum)
    kk = kolofon_be.b50_kozel_keleti(korny.b, korny.motivum)
    kolofon_be.b75_kozel_keleti_reteg(korny.b)
    azonositok = frozenset().union(*elozo.values()) if elozo else frozenset()
    return Kolofon(
        szerzoseg=szerzoseg, resek=resek,
        proza_modell=proza(utolso.modell) if utolso is not None and utolso.modell is not None else None,
        jovahagyas=jovahagyas, kiadas=korny.mod.value == konfig.MOD_KIADAS,
        cim=proza(sor.cim), meghatarozas=proza(sor.meghatarozas) if sor.meghatarozas is not None else None,
        azonossag=sor.azonossag, folerendelt=proza(sor.folerendelt_mondatkezdo),
        mezok=tuple((m, proza(sor.kolofon[m])) for m in motivum_be.KOLOFON_MEZOK if m in sor.kolofon),
        kiadasok=tuple(KiadasSor(k.szam, k.datum, proza(k.valtozas)) for k in adatok.kiadasok),
        javitasok=adatok.javitasok,
        lektor=LektorSor(proza(lektor.modell), lektor.db, lektor.datum) if lektor is not None else None,
        kozel_keleti=kk is not None,
        kozel_keleti_emlites=proza(kk.emlites) if kk is not None and kk.emlites is not None else None,
        forrasok=_forrastabla(korny, elozo),
        megjelolesek=_megjelolesek(korny, azonositok))


def kapu(modell):
    """GK-27 (T9): kiadás módban kézi résű lap csak friss jóváhagyással adható ki; a frissességet a lap `lap_commit`-ja
    igazolná, ezt az új generátor a 218c-ig nem olvassa (N-F218w): a kapu megáll."""
    if modell.kiadas and modell.szerzoseg is not Szerzoseg.GENERALT:
        raise BemenetHiba('Kolofon (kiadás mód): a jóváhagyás frissessége nem igazolható, amíg az új generátor nem a lap '
                          'végleges helyére ír (a lap_commit egyezése a 218c-ben, N-F218w)')
    return modell
