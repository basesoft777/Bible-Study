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
(híján a legutóbbi kiadás) dátumával. Kiadás módban a kézi résű lap jóváhagyásának frissessége a `lap_commit`-ból és a
kézi bemenetek lenyomatából jön (`bemenet/jovahagyas.py`, N221, DT933 (1)): friss jóváhagyásnál, vagy ha a jóváhagyott
változat óta csak generált blokk változott, a mondat „a szerző jóváhagyta”; különben a kapu megáll (új nézés kell).
"""
import datetime
import enum
from dataclasses import dataclass
from typing import Optional, Tuple

from lapgen import konfig
from lapgen.bemenet import b01_licencek
from lapgen.bemenet import irodalom as irodalom_be
from lapgen.bemenet import jovahagyas as jovahagyas_be
from lapgen.bemenet import kolofon as kolofon_be
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import Jovahagyas
from lapgen.szakaszok import Szakaszrend
from lapgen.szamitas.idezes import Licenc, licenc_lista
from lapgen.szoveg import Kulcs, Lathato, idezet, proza


class Szerzoseg(enum.Enum):
    """A szerzőségi mondat alakja."""
    GENERALT = 'generalt'       # nincs kézi rés: a lap minden szakasza generált
    KIADATLAN = 'kiadatlan'     # van kézi rés, de a lap nincs kiadva: a szerző nem hagyta jóvá
    KIADOTT = 'kiadott'         # kiadott lap kézi résekkel: a szerző jóváhagyta (munka módban: a korábbi változatot)


class ForrasNev(enum.Enum):
    """A forrástábla sorának névtábla-típusa."""
    KOLOFON_SZOTAR = 'kolofon_szotar'   # szótárfájl
    IROD_ADAT = 'irod_adat'             # adatfájl
    IROD_KULSO = 'irod_kulso'           # a generátor által nem olvasott külső forrás


class MegjelolesMondat(enum.Enum):
    """A lap saját mondata egy forrásról a kötelező megjelölések között (`kolofon.megjeloles.<érték>` sablonsor)."""
    LSJ = 'lsj'
    TW = 'tw'
    TWOT = 'twot'


class KeziRes(enum.Enum):
    """A szerzőségi mondatban felsorolható kézi rés (a címe a `cim.<érték>` sablonsor)."""
    KIVONAT = 'kivonat'
    MIERT_FONTOS = 'miert_fontos'
    MINOSITES = 'minosites'
    ALATAMASZTAS = 'alatamasztas'
    ERTELMEZES = 'ertelmezes'
    MODSZERTAN = 'modszertan'


class KolofonMezo(enum.Enum):
    """A motívumtábla kézi mezője a Kolofon táblájában (a címkéje a `kolofon.mezo.<érték>` sablonsor)."""
    UI_CIMKE = 'ui_cimke'
    TEMA = 'tema'
    PARDES_SZINT = 'pardes_szint'
    SABLON_VERZIO = 'sablon_verzio'


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
    """A forrástábla egy sora: a név (névtábla-típus és kulcs), a licencek, az olvasó szakaszok sorszáma (a szakaszrend
    szerint, növekvő; az alrész a szülő szakaszé)."""
    nev_tipus: ForrasNev
    nev: Kulcs
    licencek: Tuple[Licenc, ...]
    szakaszok: Tuple[int, ...]


@dataclass(frozen=True)
class Megjeloles:
    """Egy kötelező forrásmegjelölés: szó szerinti idézet a licencleltárból (`szoveg`), vagy a lap saját mondata a
    forrásról (`sablon`: a `kolofon.megjeloles.<sablon>` sor; a `cimke` a licencleltár címkéje, ha a mondat kéri)."""
    szoveg: Optional[Lathato]
    sablon: Optional[MegjelolesMondat]
    cimke: Optional[Lathato]


@dataclass(frozen=True)
class Kolofon:
    szerzoseg: Szerzoseg
    resek: Tuple[KeziRes, ...]          # a kézi rések, a lapon álló sorrendben
    proza_modell: Optional[Lathato]     # a legutóbbi kiadás próza-modellje; None: a kiadás nem rögzíti
    jovahagyas: Optional[datetime.date]  # a szerző jóváhagyásának dátuma (kiadott lapnál)
    kiadas: bool                        # kiadás mód (a kapu ebben áll meg)
    cim: Lathato
    meghatarozas: Optional[Lathato]
    azonossag: Optional[Kulcs]
    folerendelt: Lathato                # mondatkezdő alakban (a táblacella elején áll)
    mezok: Tuple[Tuple[KolofonMezo, Lathato], ...]   # a motívumtábla kézi mezői (mező, érték)
    kiadasok: Tuple[KiadasSor, ...]
    javitasok: Tuple[datetime.date, ...]
    lektor: Optional[LektorSor]
    kozel_keleti: bool                  # a motívum a közel-keleti határ táblájában áll
    kozel_keleti_emlites: Optional[Lathato]
    forrasok: Tuple[ForrasSor, ...]
    megjelolesek: Tuple[Megjeloles, ...]
    frissesseg: Optional[Jovahagyas] = None   # kiadás módban, kézi résű lapnál (GK-27); különben None


def _forrastabla(korny, elozo):
    rend = Szakaszrend()
    sorok = {}   # csoport (a név nyers szövege) -> [rendezési kulcs, típus, kulcs, licencforrások, szakaszok]

    def hozzaad(csoport, rendkulcs, tipus, kulcs, forras, azonosito):
        r = sorok.setdefault(csoport, [rendkulcs, tipus, kulcs, [], set()])
        r[3].append(forras)
        r[4].add(rend.sorszam(rend.szulo(azonosito)))

    for azonosito, olvasasok in elozo.items():
        szarm_fajlok, szarm_kulsok = irodalom_be.szarmaztatott_forrasok(korny.b, olvasasok)
        for f in irodalom_be.irodalom_fajlok(korny.b, olvasasok) + szarm_fajlok:
            hozzaad(f.kolofon_csoport, f.kolofon_rend, ForrasNev(f.kolofon_tipus), f.kulcs, f, azonosito)
        for k in irodalom_be.kulso_forrasok(korny.b, korny.motivum, olvasasok) + szarm_kulsok:
            hozzaad(k.csoport, k.rend, ForrasNev.IROD_KULSO, k.kulcs, k, azonosito)
    return tuple(ForrasSor(nev_tipus=t, nev=kulcs, licencek=licenc_lista(fs), szakaszok=tuple(sorted(sz)))
                 for _rend, t, kulcs, fs, sz in sorted(sorok.values(), key=lambda r: r[0]))


def _megjelolesek(korny, azonositok):
    kulcsok = {korny.b.jegyzek_sor(b_id).licenc_kulcs for b_id in azonositok}
    licencek = b01_licencek(korny.b)
    ki, latott = [], set()
    for kulcs, sablon in konfig.KOLOFON_MEGJELOLES:
        if kulcs not in kulcsok:
            continue
        if sablon is not None:
            ki.append(Megjeloles(szoveg=None, sablon=MegjelolesMondat(sablon), cimke=idezet(licencek.cimke(kulcs))))
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
    resek = tuple(KeziRes(r) for r in konfig.SZERZOSEG_RESEK if r in kezi)
    utolso = adatok.kiadasok[-1] if adatok.kiadasok else None
    if not resek:
        szerzoseg, jovahagyas = Szerzoseg.GENERALT, None
    elif utolso is None:
        szerzoseg, jovahagyas = Szerzoseg.KIADATLAN, None
    else:
        szerzoseg = Szerzoseg.KIADOTT
        jovahagyas = adatok.atnezesek[-1] if adatok.atnezesek else utolso.datum
    kiadas = korny.mod.value == konfig.MOD_KIADAS
    frissesseg = None
    if kiadas and resek:
        frissesseg = jovahagyas_be.frissesseg(korny.b, korny.motivum)
        if frissesseg.kiadhato:
            jovahagyas = kolofon_be.datum_ertek('B48', frissesseg.atnezes_datum, 'átnézés')
    lektor = kolofon_be.b49_lektor(korny.b, korny.motivum)
    kk = kolofon_be.b50_kozel_keleti(korny.b, korny.motivum)
    kolofon_be.b75_kozel_keleti_reteg(korny.b)
    azonositok = frozenset().union(*elozo.values()) if elozo else frozenset()
    return Kolofon(
        szerzoseg=szerzoseg, resek=resek,
        proza_modell=proza(utolso.modell) if utolso is not None and utolso.modell is not None else None,
        jovahagyas=jovahagyas, kiadas=kiadas,
        cim=proza(sor.cim), meghatarozas=proza(sor.meghatarozas) if sor.meghatarozas is not None else None,
        azonossag=sor.azonossag, folerendelt=proza(sor.folerendelt_mondatkezdo),
        mezok=tuple((KolofonMezo(m), proza(sor.kolofon[m])) for m in motivum_be.KOLOFON_MEZOK if m in sor.kolofon),
        kiadasok=tuple(KiadasSor(k.szam, k.datum, proza(k.valtozas)) for k in adatok.kiadasok),
        javitasok=adatok.javitasok,
        lektor=LektorSor(proza(lektor.modell), lektor.db, lektor.datum) if lektor is not None else None,
        kozel_keleti=kk is not None,
        kozel_keleti_emlites=proza(kk.emlites) if kk is not None and kk.emlites is not None else None,
        forrasok=_forrastabla(korny, elozo),
        megjelolesek=_megjelolesek(korny, azonositok),
        frissesseg=frissesseg)


_KAPU_OK = {
    jovahagyas_be.Frissesseg.NINCS_LAP: 'Kolofon (kiadás mód, GK-27): a lap (%s) nincs a repóban: a jóváhagyott változat nem azonosítható',
    jovahagyas_be.Frissesseg.NINCS_ATNEZES: 'Kolofon (kiadás mód, GK-27): a lapnak (%s) nincs érvényes szerzői átnézés-sora (lap_atnezesek.tsv, '
                                            'SEMA 2.48), amelynek lap_commit-ja őse a mai változatnak',
    jovahagyas_be.Frissesseg.ELAVULT: 'Kolofon (kiadás mód, GK-27): a jóváhagyott változat (%s) óta a kézi próza vagy a motívum adata változott: '
                                      'új nézés kell (DT933 (1))',
}


def kapu(modell):
    """GK-27 (T9): kiadás módban kézi résű lap csak friss jóváhagyással adható ki (N221): a szerző átnézés-sorának
    `lap_commit`-ja a lap mai utolsó commitja, vagy azóta csak generált blokk változott (a kézi bemenetek lenyomata
    azonos; ez változásjegyzék-sort kér, új nézést nem). Más esetben BUKÁS."""
    if not modell.kiadas or modell.szerzoseg is Szerzoseg.GENERALT:
        return modell
    f = modell.frissesseg
    if f is None:
        raise BemenetHiba('Kolofon (kiadás mód): a jóváhagyás frissessége nincs megmérve')
    if f.kiadhato:
        return modell
    hol = f.atnezes_commit[:12] if f.allapot is jovahagyas_be.Frissesseg.ELAVULT else (f.lap_commit or '')[:12]
    raise BemenetHiba(_KAPU_OK[f.allapot] % (hol or '—'))
