"""lapgen.bemenet.vizsgalt — a vizsgált helyek döntésnaplójának soronkénti szerkezete a „3. Kizárt és vizsgált
helyek” táblájához (S9a).

Bemenet: B04 (a jelöltek döntésnaplója: a motívum elutasított és nyitva maradt előfordulás-jelöltjei) és B56 (az
elutasítási okok). A sor két szabad mezője közül a `forras_kereses` belső szöveg: a réteg csak a szerkezetét olvassa
ki (melyik gyűjtemény vagy keresés jelölte, melyik szóra, melyik hálóban, hány verset fed a csoportos sor), a lapra
a szerkezetből sablonmondat kerül (a régi `szerep_kizart.jeloles_oka` és a lap utólagos cseréi helyett). A
mezőben álló kézi megszorítás (pl. „Hif'íl-alakok”) kézi szöveg, kapuval.

Az `indoklas` kézi próza, a DT884 szerint a végleges alakjában: a réteg nem tisztít, a nem olvasói szövegen megáll
(`kereszthiv._indok`). Két szerkezet bomlik le róla: az összesítő sor eleje („Összesítő sor N versre (…):”, a régi
lap „A sor N verset foglal össze …” cseréje helyett sablonmondat) és a csoportos kizárás szerkesztői döntésének
záró mondata (a dátum és az idézet a döntés nyoma, a lapon sablonmondat áll).

A forrás-mező és az indoklás proveniencia-farka, valamint a döntés nyoma a jegyzet megjegyzésébe kerül
(proveniencia), változatlanul; a közös proveniencia-sor jele (‹K1› …) a számításé.
"""
import re

from lapgen.bemenet import dontes as dontes_be
from lapgen.bemenet import kereszthiv as kh
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.ertekek import AjanlasFajta, Dontes, JelolesFajta, VizsgaltCsoport, VizsgaltJegyzetFajta
from lapgen.szoveg import Strong, prov

_ELOFORDULAS_JELOLT = 'elofordulas'
_MEZO_ELVALASZTO = ' | '
_NAPLO_RX = re.compile(r';\s*napló:')
_STRONG_RX = re.compile(r'\b[HG]\d{4}[a-z]?\b')
_ATIRAS_RX = re.compile(r'\s*\([^()]*\)')
_SCOPE_RX = re.compile(r'\bscope=([^|]*)')
_KORPUSZOK = ('TAHOT', 'TAGNT')
_SZAM_U_RX = re.compile(r'^F\d+ U\d:')          # a mérés munkanaplóbeli tétele („F123 U2: …”): forrásleírás nélkül
_HELYORZO_RX = re.compile(r'(?<![\w-])(?:DT|N|D)-F\d+[a-z]*\b')
_NYOM_ELVALASZTO = ' · '
# a teljesség-mérés hálói a forrás-mezőben (a régi `szerep_kizart.TELJESSEG_HALOK` kulcsai, a rendjükkel); a háló
# olvasói neve a névtábla `halo_kereses` sora
_HALOK = (('szópár-háló', 'szopar'), ('Strong-háló', 'strong'), ('szótár (', 'szotar'), ('Károli-szó', 'karoli'),
          ('LXX-többlet', 'lxx_tobblet'), ('Septuaginta-híd', 'lxx_hid'))
_CSOPORT_RX = re.compile(r'(?:blokk-kizárás|blokk-sor)[^:|]*:\s*(\d+) vers')
_OSSZESITO_ELEJE_RX = re.compile(r'^Összesítő sor (\d+) versre \((?:a sor igehelye a blokk egy verse áll|az első itt '
                                 r'áll)\):\s*')
_SZERKESZTOI_ZARO_RX = re.compile(r'\s*A felhasználó döntése \(\d{4}-\d\d-\d\d: „[^”]*”\) szerint blokk-kizárás\.$')
_TEMATIKUS_RX = re.compile(r'^tematikus:')
# a forrás-mező proveniencia-hármasa (a régi `szerep_kizart.PROV_HARMAS`): scope, forrás, a lekérdezés további mezői,
# dátum, csatorna
_SEP = r'\s\\?\|\s*'
PROV_HARMAS = re.compile(r'scope=[^|`\n]*?' + _SEP + r'forras=[^|`\n]*?(?:' + _SEP + r'(?!ts=)[a-z_]+=[^|`\n]*?)*'
                         + _SEP + r'ts=[0-9T:Z-]+(?:' + _SEP + r'csatorna=[a-z_]+)?')


class Jeloles:
    """A jelölés oka: a fajta és a paraméterei. `ajanlas`: a kereszthivatkozás-ajánlás szerkezete (`kh.Ajanlas`);
    `strongok`: a keresett szavak; `halok`: a teljesség-mérés hálóinak kulcsa (üres: a forrás nem nevezi meg);
    `csoport_versszam`: a csoportos sor versszáma (egyenkénti sornál None)."""
    __slots__ = ('fajta', 'ajanlas', 'strongok', 'halok', 'csoport_versszam')

    def __init__(self, fajta, ajanlas=None, strongok=(), halok=(), csoport_versszam=None):
        self.fajta, self.ajanlas, self.strongok = fajta, ajanlas, strongok
        self.halok, self.csoport_versszam = halok, csoport_versszam


class Jegyzet:
    """A sor jegyzete (a cellán túli jelölési forrás): a fajta, a szavak, a kézi megszorítás és a korpuszok kulcsa."""
    __slots__ = ('fajta', 'strongok', 'megszoritas', 'korpuszok')

    def __init__(self, fajta, strongok=(), megszoritas=None, korpuszok=()):
        self.fajta, self.strongok, self.megszoritas, self.korpuszok = fajta, strongok, megszoritas, korpuszok


class VizsgaltSor:
    """A döntésnapló egy elutasított vagy nyitva maradt előfordulás-jelöltje.

    `versek`: az igehely versei (a tartomány kibontva); `csoport`: a jelölés forráscsoportja; `indok`: az indoklás
    darabjai (`kh.IndokDarab`), az összesítő eleje és a szerkesztői záró mondat nélkül; `osszesito`: az összesítő sor
    versszáma az indoklás elejéről (None, ha nem összesítő sor); `szerkesztoi_zaro`: a csoportos kizárás szerkesztői
    döntésének záró mondata állt-e az indoklás végén; `ok`: az elutasítás oka (`dontes_be.Ok`; nyitott sornál None);
    `ok_ismetles`: az indoklás eleje maga kimondja-e az okot; `jegyzet_nyers`: a jegyzet megjegyzésének nyers
    szövege (a régi lábjegyzet alakja: a forrás-mező, az indoklás proveniencia-farka és a döntés nyoma), belső
    szövegként; `osszevonas_kulcs`: a sorok
    összevonásának kulcsa (azonos kulcsú, egymást követő versek egy sorba kerülnek)."""
    __slots__ = ('igehely', 'versek', 'dontes', 'csoport', 'jeloles', 'jegyzet', 'indok', 'osszesito',
                 'szerkesztoi_zaro', 'ok', 'ok_ismetles', 'jegyzet_nyers', 'osszevonas_kulcs')


def nyom_lapra(dontes_ref):
    """A `dontes_ref` megjegyzésbe kerülő alakja (a régi `szerep_kizart.nyom_lapra`): a helyőrző alakú azonosító
    nélkül; üres, ha nem marad semmi."""
    elemek = [e.strip() for e in (dontes_ref or '').split(_NYOM_ELVALASZTO)]
    return _NYOM_ELVALASZTO.join(e for e in elemek if e and not _HELYORZO_RX.search(e))


def _korpuszok(b, forras):
    m = _SCOPE_RX.search(forras)
    scope = m.group(1) if m else ''
    return tuple(b.kulcs('B04', 'korpusz', k) for k in _KORPUSZOK if k in scope)


def _jeloles(b, fo, forras, konyvek, igehely):
    """(csoport, jelölés, jegyzet) a forrás-mező első részéből (a régi `jeloles_oka` ágai, a lapon előforduló
    fajtákra). Ismeretlen fajta BemenetHiba: a lap nem találgat."""
    if fo.startswith(kh._ELOTAG_TSK_KAROLI) or fo.startswith(kh._ELOTAG_TSK) or fo.startswith(kh._ELOTAG_KAROLI):
        a = kh._ajanlas(fo, konyvek)
        csoport = VizsgaltCsoport.TSK if a.fajta in (AjanlasFajta.TSK, AjanlasFajta.TSK_ALACSONY) \
            else VizsgaltCsoport.KAROLI
        return csoport, Jeloles(JelolesFajta.AJANLAS, ajanlas=a), None
    if fo.startswith('scan'):
        if 'TSK' in fo:
            raise BemenetHiba('B04: %s: a TSK-ajánlással együtt álló szókeresés nincs leképezve: %s' % (igehely, fo[:80]))
        strongok = tuple(Strong(s) for s in _STRONG_RX.findall(fo))
        if not strongok:
            raise BemenetHiba('B04: %s: a szókeresés nem nevez meg Strong-számot: %s' % (igehely, fo[:80]))
        jeloles = Jeloles(JelolesFajta.SZO, strongok=strongok)
        if fo.startswith('scan:'):
            maradek = _ATIRAS_RX.sub('', _STRONG_RX.sub('', fo[len('scan:'):])).strip(' ,;')
            if not maradek:
                return VizsgaltCsoport.KERESES, jeloles, None
            hiba = kh.nem_olvasoi(maradek)
            if hiba:
                raise BemenetHiba('B04: %s: a szókeresés megszorítása nem olvasói szöveg (%r)' % (igehely, hiba))
            return VizsgaltCsoport.KERESES, jeloles, Jegyzet(VizsgaltJegyzetFajta.SZOKERESES, strongok=strongok,
                                                             megszoritas=b.kezi('B04', 'kereses_megszoritas', maradek))
        korpuszok = _korpuszok(b, forras)
        if not korpuszok:
            raise BemenetHiba('B04: %s: a szókeresés korpusza nem állapítható meg: %s' % (igehely, forras[:80]))
        return VizsgaltCsoport.KERESES, jeloles, Jegyzet(VizsgaltJegyzetFajta.KERESES_KORPUSZ, strongok=strongok,
                                                         korpuszok=korpuszok)
    if fo.startswith('kollokacio'):
        return VizsgaltCsoport.KERESES, Jeloles(JelolesFajta.SZOPAR, strongok=tuple(
            Strong(s) for s in _STRONG_RX.findall(fo))), None
    if _TEMATIKUS_RX.match(fo):
        return VizsgaltCsoport.SZERKESZTOI, Jeloles(JelolesFajta.TEMATIKUS), None
    if fo.startswith('napló:') or (not fo and 'napló:' in forras):
        return VizsgaltCsoport.SZERKESZTOI, Jeloles(JelolesFajta.NAPLO), None
    if fo.startswith('négyforrásos audit'):
        return VizsgaltCsoport.SZERKESZTOI, Jeloles(JelolesFajta.AUDIT), Jegyzet(VizsgaltJegyzetFajta.NAPLO)
    if 'teljesség-mérés' in fo:
        halok = tuple(b.kulcs('B04', 'halo', kulcs) for minta, kulcs in _HALOK if minta in fo)
        m = _CSOPORT_RX.search(fo)
        n = int(m.group(1)) if m else None
        if n is not None:
            jegyzet = None
        elif _SZAM_U_RX.match(fo):
            jegyzet = Jegyzet(VizsgaltJegyzetFajta.ADATTABLAK)
        else:
            jegyzet = Jegyzet(VizsgaltJegyzetFajta.TELJESSEG_EGYENKENT)
        return VizsgaltCsoport.KERESES, Jeloles(JelolesFajta.TELJESSEG, halok=halok, csoport_versszam=n), jegyzet
    if fo.startswith('pozíció-alapú frázis-keresés'):
        return VizsgaltCsoport.KERESES, Jeloles(JelolesFajta.FRAZIS), None
    if fo.startswith('csalad '):
        return VizsgaltCsoport.KERESES, Jeloles(JelolesFajta.SZOCSALAD, strongok=tuple(
            Strong(s) for s in _STRONG_RX.findall(fo))), None
    if fo.startswith('lanc'):
        korpuszok = _korpuszok(b, forras)
        return VizsgaltCsoport.KERESES, Jeloles(JelolesFajta.LANC), Jegyzet(VizsgaltJegyzetFajta.LANC,
                                                                             korpuszok=korpuszok)
    raise BemenetHiba('B04: %s: a jelölés forrása nincs leképezve a 3. szakasz táblájára: %s' % (igehely, fo[:120]))


def _indoklas(b, szoveg, igehely):
    """(összesítő versszám vagy None, szerkesztői záró mondat volt-e, az indoklás darabjai)."""
    osszesito = None
    m = _OSSZESITO_ELEJE_RX.match(szoveg)
    if m:
        osszesito = int(m.group(1))
        szoveg = szoveg[m.end():]
    zaro = _SZERKESZTOI_ZARO_RX.search(szoveg)
    if zaro:
        szoveg = szoveg[:zaro.start()]
    return osszesito, bool(zaro), (kh._indok(b, szoveg, igehely) if szoveg.strip() else ())


def vizsgalt_sorok(b, motivum):
    """A B04 elutasított és nyitva maradt előfordulás-jelöltjei a döntésnapló sorrendjében, a 3. szakasz
    táblájához."""
    konyvek = b63_konyvek(b)
    okok = dontes_be.b56_okok(b, motivum)
    tabla = dontes_be.jeloltnaplo_tabla(b, tovabbi=('dontes_ref',))
    idx = {o: tabla.oszlop(o) for o in dontes_be._JELOLT_OSZLOPOK + ('dontes_ref',)}
    ki = []
    for sor in tabla.sorok:
        if sor[idx['id']] != motivum.kod or sor[idx['jelolt_tipus']] != _ELOFORDULAS_JELOLT:
            continue
        try:
            dontes = Dontes(sor[idx['dontes']])
        except ValueError:
            raise BemenetHiba('B04: ismeretlen döntés-érték: %r (%s)' % (sor[idx['dontes']], sor[idx['igehely']])) \
                from None
        if dontes not in (Dontes.ELUTASITVA, Dontes.NYITVA):
            continue
        igehely_kod = sor[idx['igehely']].strip()
        forras = sor[idx['forras_kereses']]
        fo = _NAPLO_RX.split(forras.split(_MEZO_ELVALASZTO)[0].strip())[0].strip()
        csoport, jeloles, jegyzet = _jeloles(b, fo, forras, konyvek, igehely_kod)
        indok_fo, sep, farok = sor[idx['indoklas']].partition(_MEZO_ELVALASZTO)
        osszesito, zaro, indok = _indoklas(b, indok_fo, igehely_kod)
        ok = okok.besorol(b.belso('B04', 'indoklas', indok_fo)) if dontes is Dontes.ELUTASITVA else None
        v = VizsgaltSor()
        v.igehely = dontes_be._igehely(igehely_kod, 'B04')
        v.versek = dontes_be.tartomany_versei(igehely_kod)
        v.dontes, v.csoport, v.jeloles, v.jegyzet, v.indok = dontes, csoport, jeloles, jegyzet, indok
        v.osszesito, v.szerkesztoi_zaro, v.ok = osszesito, zaro, ok
        v.ok_ismetles = bool(ok is not None and indok and osszesito is None
                             and kh.cimke_ismetles(ok.cimke.ertek, indok_fo))
        nyom = nyom_lapra(sor[idx['dontes_ref']])
        lj = 'forrás: `%s`' % forras
        if sep:
            lj += ' · ' + farok
        if nyom:
            lj += ' · a döntés nyoma: `%s`' % nyom
        v.jegyzet_nyers = b.belso('B04', 'jegyzet_nyers', lj).szoveg
        v.osszevonas_kulcs = (forras, sor[idx['indoklas']], dontes, nyom)
        ki.append(v)
    return tuple(ki)


def proveniencia_harmasok(szoveg):
    """A belső szöveg proveniencia-hármasai (a közös jel számításához), a `\\|` escape nélkül."""
    return [m.group(0).replace('\\|', '|') for m in PROV_HARMAS.finditer(szoveg)]


def proveniencia_csere(szoveg, sorszamok):
    """A belső szöveg proveniencia-hármasai helyén a közös jel (‹K<n>›, a `sorszamok` szerint, ahol van); az
    eredmény proveniencia."""
    def jel(m):
        n = sorszamok.get(m.group(0).replace('\\|', '|'))
        return '‹K%d›' % n if n is not None else m.group(0)
    return prov('{}', PROV_HARMAS.sub(jel, szoveg))


# A proveniencia-hármas olvasói alakja a közös forrásmegjelölés megjegyzésébe (a régi `_prov_olvasoi` és
# `olvasoi_forrasnev` szabálya, a 3. szakasz forrásfájljaira; megjegyzés, nem látható szöveg).
_FAJL_RX = re.compile(r'(?:[\w.-]+/)*[\w-]+\.(?:tsv|py|md|txt|json)')
_FAJL_NEVEK = (
    (re.compile(r'(?:[\w.-]+/)*[\w-]*_kereszthivatkozas_naplo\.md'), 'a motívum korábbi kereszthivatkozás-naplója'),
    (re.compile(r'(?:[\w.-]+/)*F123_teljesseg_[\w-]+?(?:_blokkok)?\.(?:md|tsv)'), 'a lap teljesség-mérése'),
    (re.compile(r'(?:[\w.-]+/)*F123_[\w-]+\.(?:md|tsv|py)'), 'a lap munkanaplója'),
    (re.compile(r'(?:[\w.-]+/)*teljesseg_meres\.py'), 'a teljesség-mérő'),
    (re.compile(r'(?:[\w.-]+/)*TAHOT_kivonat\.tsv'), 'a STEPBible héber szövege (TAHOT)'),
    (re.compile(r'(?:[\w.-]+/)*TAGNT_(?:kivonat|valtozatok)\.tsv'), 'a STEPBible görög szövege (TAGNT)'),
    (re.compile(r'(?:[\w.-]+/)*lekerdez\.py'), 'a szókereső eszköz'),
    (re.compile(r'(?:[\w.-]+/)*jeloltek\.tsv'), 'a vizsgált helyek döntésnaplója'),
    (re.compile(r'(?:[\w.-]+/)*[\w-]+\.py'), 'a lap generátora'),
    (re.compile(r'(?:[\w.-]+/)*[\w-]+\.tsv'), 'a lap adattáblája'),
    (re.compile(r'(?:[\w.-]+/)*[\w-]+\.(?:txt|json)'), 'a lap adatforrása'),
    (re.compile(r'(?:[\w.-]+/)*[\w-]+\.md'), 'a lap munkaanyaga'),
)
_FORRAS_MEZO_RX = re.compile(r'forras=([^|]+)')
_TS_DATUM_RX = re.compile(r'ts=(\d{4}-\d{2}-\d{2})')


def prov_olvasoi(harmas):
    """A proveniencia-hármas olvasói alakja (proveniencia): a forrásfájlok olvasói neve, a kézi szerkesztés és a
    dátum."""
    forras = _FORRAS_MEZO_RX.search(harmas)
    datum = _TS_DATUM_RX.search(harmas)
    nevek = []
    for f in re.split(r'[+,;]\s*', (forras.group(1) if forras else '').strip()):
        f = re.sub(r'\s*\(.*$', '', f).strip()
        if not f or not _FAJL_RX.fullmatch(f):
            continue
        nev = next((n for rx, n in _FAJL_NEVEK if rx.fullmatch(f)), None)
        if nev and nev not in nevek:
            nevek.append(nev)
    if 'scope=manual' in harmas and 'kézi szerkesztés' not in nevek:
        nevek.append('kézi szerkesztés')
    return prov('forrás: {}{}', '; '.join(nevek) or 'a lap munkaanyaga', (', ' + datum.group(1)) if datum else '')
