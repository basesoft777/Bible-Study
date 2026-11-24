"""lapgen.szamitas.kolofon — a Kolofon (S8d): a szakasz modellje.

A Kolofon négy részből áll: (1) a szerzőségi mondat és a közleményekre kötött bekezdések (hogyan idézd, módszertani
elvek, hatókör); (2) a motívum azonosító táblája, a kiadás és a lektorálás soraival; (3) a változásjegyzék; (4) a lap
forrástáblája (forrásonként a licenc és az olvasó szakaszok) és alatta a kötelező forrásmegjelölések.

A forrástábla a 12. szakasz forrás-halmazát használja (DT901: a számozott szakaszok és alrészeik valódi olvasásai, a
jegyzék `irodalom` oszlopa szerint szűrve; a tanúk és a Vulgata külső forrásai a tábláik ellenőrzött soraiból; a származtatott tábla
CC BY-os bemenetei saját soron, a saját licencükkel: F212, `konfig.KOLOFON_SZARMAZTATOTT`); a
forrás neve szótárfájlnál a `kolofon_szotar`, adatfájlnál az `irod_adat`, külső forrásnál az `irod_kulso` névtábla-sor,
az azonos nevű fájlok egy sorba vonódnak, a sorok a név szerinti rendben. A megjelölendő források halmaza és rendje a
`konfig.KOLOFON_MEGJELOLES`; a szöveg a licencleltárból jön (GK-07). A licenckapu (N223) minden módban azt méri, hogy
minden licencleltár-forrás, amelynek adatát a lap olvassa és `kotelezo_megjeloles`-e nem üres, megjelölve áll: a mező
minden mondata szó szerint, idézetként; a saját mondatú forrásnál (LSJ, OSHL, tW) a sablonmondat hordozza az idézetet
(D20 (1)), kivétel nélkül.

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
from lapgen.bemenet.jegyzek import IRODALOM_NINCS, BemenetHiba
from lapgen.ertekek import IrodLicenc, Jovahagyas
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
    """Egy kötelező forrásmegjelölés: szó szerinti idézet a licencleltárból (`szoveg`), önálló sorban; vagy a lap
    saját mondata a forrásról (`sablon`: a `kolofon.megjeloles.<sablon>` sor, a `cimke` a licencleltár címkéje, ha a
    mondat kéri), amely a `szoveg` idézetet a `{megjeloles}` helyén hordozza (D20 (1))."""
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
    # a licenckapu (N223, D14) lelete: a lap adatát adó források licenckulcsai, amelyeknek megjelölése vagy neve hiányzik
    licenc_hiany: Tuple[Kulcs, ...] = ()


def _forrastabla(korny, elozo):
    """A forrástábla sorai és a sorok által megnevezett licenckulcsok ({licenckulcs: a licenc alakjai}) a licenckapunak."""
    rend = Szakaszrend()
    sorok = {}   # csoport (a név nyers szövege) -> [rendezési kulcs, típus, kulcs, licencforrások, szakaszok]
    fedett = {}

    def hozzaad(csoport, rendkulcs, tipus, kulcs, forras, azonosito):
        r = sorok.setdefault(csoport, [rendkulcs, tipus, kulcs, [], set()])
        r[3].append(forras)
        r[4].add(rend.sorszam(rend.szulo(azonosito)))

    for azonosito, olvasasok in elozo.items():
        szarm_fajlok, szarm_kulsok = irodalom_be.szarmaztatott_forrasok(korny.b, olvasasok)
        for f in irodalom_be.irodalom_fajlok(korny.b, olvasasok) + szarm_fajlok:
            hozzaad(f.kolofon_csoport, f.kolofon_rend, ForrasNev(f.kolofon_tipus), f.kulcs, f, azonosito)
            for lk in _bemenet_licencei(korny.b, f.b_id):
                fedett.setdefault(lk, set()).add(f.licenc)
        for k in irodalom_be.kulso_forrasok(korny.b, korny.motivum, olvasasok) + szarm_kulsok:
            hozzaad(k.csoport, k.rend, ForrasNev.IROD_KULSO, k.kulcs, k, azonosito)
            fedett.setdefault(konfig.IROD_KULSO_LICENC[k.kulcs.ertek], set()).add(k.licenc)
    tabla = tuple(ForrasSor(nev_tipus=t, nev=kulcs, licencek=licenc_lista(fs), szakaszok=tuple(sorted(sz)))
                  for _rend, t, kulcs, fs, sz in sorted(sorok.values(), key=lambda r: r[0]))
    return tabla, fedett


def _bemenet_licencei(b, b_id):
    """Egy bemenet licenckulcsai: a jegyzék `licenc_kulcs`-a és a több forrású bemenet társai (`konfig.LICENC_TARS`)."""
    lk = b.jegyzek_sor(b_id).licenc_kulcs
    return ((lk,) if lk != '-' else ()) + konfig.LICENC_TARS.get(b_id, ())


def _megjelolesek(korny, kulcsok):
    """A kötelező megjelölések a `konfig.KOLOFON_MEGJELOLES` rendjében, a lap adatát adó források (`kulcsok`) közül;
    az ismétlődő mondat egyszer. Visszaad: (megjelölések, az idézett mondatok nyers szövegének halmaza)."""
    licencek = b01_licencek(korny.b)
    ki, latott = [], set()
    for kulcs, sablon in konfig.KOLOFON_MEGJELOLES:
        if kulcs not in kulcsok:
            continue
        if sablon is not None:
            # D20 (1): a saját mondat a leltár előírt megjelölését szó szerint hordozza (a `{megjeloles}` helyén)
            reszek = licencek.megjeloles(kulcs)
            if len(reszek) != 1:
                raise BemenetHiba('B01: a saját mondatú forrás (`%s`) `kotelezo_megjeloles` mezője %d mondat; a '
                                  'sablonmondat egyet hordoz' % (kulcs, len(reszek)))
            latott.add(reszek[0].ertek)
            ki.append(Megjeloles(szoveg=idezet(reszek[0]), sablon=MegjelolesMondat(sablon),
                                 cimke=idezet(licencek.cimke(kulcs))))
            continue
        for resz in licencek.megjeloles(kulcs):
            if resz.ertek not in latott:
                latott.add(resz.ertek)
                ki.append(Megjeloles(szoveg=idezet(resz), sablon=None, cimke=None))
    return tuple(ki), latott


def _lapon_allo_licencek(korny, azonositok):
    """A lap adatát adó források licenckulcsai: a számozott szakaszok olvasott, forráslistára kerülő bemenetei (a jegyzék
    `irodalom` oszlopa szerint, DT901; a több forrású bemenet társaival), a származtatott táblák bemenetei (F212) és a
    külső források (a tanúk, az ókori fordítások, a MACULA)."""
    b = korny.b
    kulcsok = set()
    for b_id in azonositok:
        if b.jegyzek_sor(b_id).irodalom != IRODALOM_NINCS:
            kulcsok.update(_bemenet_licencei(b, b_id))
    szarm_fajlok, szarm_kulsok = irodalom_be.szarmaztatott_forrasok(b, azonositok)
    for f in szarm_fajlok:
        kulcsok.update(_bemenet_licencei(b, f.b_id))
    for k in irodalom_be.kulso_forrasok(b, korny.motivum, azonositok) + szarm_kulsok:
        kulcsok.add(konfig.IROD_KULSO_LICENC[k.kulcs.ertek])
    return kulcsok


def licenc_meres(korny, elozo):
    """A licenckapu (N223, D14) bemenete egy szótárban: `lapon_allo` ({licenckulcs: tisztázatlan-e a licence}: a lap
    adatát adó források), `kotelezo` ({licenckulcs: a megjelölés mondatai}: közülük a nem üres megjelölésűek; a
    tisztázatlan licencű forrás mezője leírás, nem előírt szöveg, ezért nem tárgya, D14 (c)), `fedett` ({licenckulcs: a
    forrástábla licencalakjai}) és `idezett` (a Kolofon idézett megjelölés-mondatai; a saját mondatú forrásé is, mert a
    mondata a leltár szövegét szó szerint hordozza, D20 (1))."""
    azonositok = frozenset().union(*elozo.values()) if elozo else frozenset()
    kulcsok = _lapon_allo_licencek(korny, azonositok)
    licencek = b01_licencek(korny.b)
    lapon, kotelezo = {}, {}
    for lk in kulcsok:
        lapon[lk] = licencek.allapot(lk).ertek == konfig.LICENC_TISZTAZATLAN
        mondatok = licencek.megjeloles_mondatok(lk)
        if mondatok and not lapon[lk]:
            kotelezo[lk] = mondatok
    _tabla, fedett = _forrastabla(korny, elozo)
    _megj, idezett = _megjelolesek(korny, kulcsok)
    return {'lapon_allo': lapon, 'kotelezo': kotelezo, 'fedett': fedett, 'idezett': idezett}


def licenc_hianyok(meres):
    """A licenckapu (N223, D14) hiányai a `licenc_meres` szótárából, a licenckulcsok rendjében. (1) A lap adatát adó,
    kötelező megjelölésű forrás, amelynek mezőjéből egy mondat nem áll szó szerint a Kolofonban (idézetként, vagy a
    saját mondatú forrásnál a sablonmondat `{megjeloles}` helyén; D20 (1): kivétel nincs). (2) A lap adatát adó forrás, amelyet a
    forrástábla nem nevez meg, vagy tisztázatlan licencnél nem a licencállapot mondatával (GK-28) nevez meg."""
    ki = []
    for lk in sorted(meres['lapon_allo']):
        mondatok = meres['kotelezo'].get(lk, ())
        mondat_hiany = any(m not in meres['idezett'] for m in mondatok)
        alakok = meres['fedett'].get(lk)
        nev_hiany = alakok is None or (meres['lapon_allo'][lk] and IrodLicenc.CHAIN_LINEAGE not in alakok)
        if mondat_hiany or nev_hiany:
            ki.append(lk)
    return ki


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
    megjelolesek, _idezett = _megjelolesek(korny, _lapon_allo_licencek(korny, azonositok))
    forrasok, _fedett = _forrastabla(korny, elozo)
    hiany = tuple(korny.b.kulcs('B01', 'dataset', lk) for lk in licenc_hianyok(licenc_meres(korny, elozo)))
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
        forrasok=forrasok,
        megjelolesek=megjelolesek,
        frissesseg=frissesseg,
        licenc_hiany=hiany)


_KAPU_OK = {
    jovahagyas_be.Frissesseg.NINCS_LAP: 'Kolofon (kiadás mód, GK-27): a lap (%s) nincs a repóban: a jóváhagyott változat nem azonosítható',
    jovahagyas_be.Frissesseg.NINCS_ATNEZES: 'Kolofon (kiadás mód, GK-27): a lapnak (%s) nincs érvényes szerzői átnézés-sora (lap_atnezesek.tsv, '
                                            'SEMA 2.48), amelynek lap_commit-ja őse a mai változatnak',
    jovahagyas_be.Frissesseg.ELAVULT: 'Kolofon (kiadás mód, GK-27): a jóváhagyott változat (%s) óta a kézi próza vagy a motívum adata változott: '
                                      'új nézés kell (DT933 (1))',
}


def kapu(modell):
    """A Kolofon kapui: a licenckapu (N223) minden módban, a jóváhagyás frissessége (GK-27) kiadás módban."""
    if modell.licenc_hiany:
        raise BemenetHiba('Kolofon (licenckapu, N223, D14): a lap adatát adó forrás kötelező megjelölése vagy neve '
                          'hiányzik a Kolofonból: %r' % (tuple(k.ertek for k in modell.licenc_hiany),))
    return _jovahagyas_kapu(modell)


def _jovahagyas_kapu(modell):
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
