"""lapgen.bemenet.dontes — a vizsgálat döntésnaplója és a teljesség-mérés.

Bemenetek: B04 (a jelöltek döntésnaplója), B05 (a teljesség-mérés pillanatképe: keresésenként a versszám és a mérés
forrássora), B06 (a teljesség-mérés csoportlistája: a csoportosan kizárt versek), B56 (az elutasítási okok
mintaszótára).

A döntésnapló `forras_kereses` és `indoklas` mezője belső szabad szöveg: a lapra nem kerül. A réteg ezekből csak
szerkezetet olvas ki (a csoportos sor versszáma, a csoportlista kulcsa, az ajánlás ténye), az indoklást pedig a
mintaszótár okba sorolja; a lapon az ok kézi címkéje és kézi megjegyzése áll.

A jelöltek és a csoportlista igehelyei a Károli-fájl kulcsai: a könyv rövidítése úgy áll, ahogy az adatban
(a normalizáló táblán nem megy át; könyvnév-alias a kódban nincs).
"""
import enum
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Igehely, SzovegHiba

_JELOLT_OSZLOPOK = ('id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'jelolt_tipus')
_ELOFORDULAS_JELOLT = 'elofordulas'
_MEZO_ELVALASZTO = ' | '
_CSOPORT_VERSSZAM_RX = re.compile(r'blokk-(?:kizárás|sor)[^:|]*:\s*(\d+) vers')
_OSSZESITO_RX = re.compile(r'Összesítő sor (\d+) versre')
_LISTA_RX = re.compile(r'\b(blokk|osztaly)=([^),\s]+)')
_HALO_RX = re.compile(r'halo=(\w+)')
_NAPLO_RX = re.compile(r';\s*napló:')
_KULON_SOR = 'külön sor'
_AJANLAS_ELOTAGOK = ('TSK', 'Károli-KH')
_TARTOMANY_RX = re.compile(r'(.+ \d+):(\d+)[-–](\d+)')
_OSSZESITO_JELOLO_RX = re.compile(r'\s*\(összesítő sor\)\s*$')
_MINDEN_MOTIVUM = '*'
_STRONG_HALO = 'strong'
_MERT_STRONG_RX = re.compile(r'strong=([\w+]+)')


class Dontes(enum.Enum):
    BEEPITVE = 'beépítve'
    ELUTASITVA = 'elutasítva'
    NYITVA = 'nyitva'


def tartomany_versei(igehely_kod):
    """Az igehely versei a döntésnapló számolásához: az egy fejezeten belüli tartomány kibontva (a versszámok
    szerint), különben maga a hely."""
    m = _TARTOMANY_RX.fullmatch(igehely_kod)
    if m and int(m.group(2)) <= int(m.group(3)):
        return tuple('%s:%d' % (m.group(1), v) for v in range(int(m.group(2)), int(m.group(3)) + 1))
    return (igehely_kod,)


def _igehely(nyers, b_id):
    try:
        return Igehely(nyers.strip())
    except SzovegHiba as hiba:
        raise BemenetHiba('%s: érvénytelen igehely: %r (%s)' % (b_id, nyers, hiba)) from None


# --- B04: a jelöltek döntésnaplója ------------------------------------------------------------------------------

class Jelolt:
    """A döntésnapló egy sora. `csoport_versszam`: a csoportos (összesítő) sor versszáma a jelölés forrásából,
    egyenkénti sornál None; `osszesito_versszam`: ugyanez a szám az indoklás szerint; `lista_*`: a csoport
    tagjainak kulcsa a csoportlistában; `ajanlas`: a jelölt kereszthivatkozás-gyűjtemény ajánlása."""
    __slots__ = ('igehely', 'dontes', 'indoklas', 'csoport_versszam', 'osszesito_versszam', 'lista_oszlop',
                 'lista_blokk', 'lista_halo', 'kulon_sor', 'ajanlas')


def b04_jeloltek(b, motivum):
    """B04 — a motívum előfordulás-jelöltjeinek döntésnaplója, a fájl sorrendjében."""
    tabla = b._tabla('B04', oszlopok=_JELOLT_OSZLOPOK)
    idx = {o: tabla.oszlop(o) for o in _JELOLT_OSZLOPOK}
    ki = []
    for sor in tabla.sorok:
        if sor[idx['id']] != motivum.kod or sor[idx['jelolt_tipus']] != _ELOFORDULAS_JELOLT:
            continue
        forras, indoklas = sor[idx['forras_kereses']], sor[idx['indoklas']]
        j = Jelolt()
        j.igehely = _igehely(sor[idx['igehely']], 'B04')
        try:
            j.dontes = Dontes(sor[idx['dontes']])
        except ValueError:
            raise BemenetHiba('B04: ismeretlen döntés-érték: %r (%s)'
                              % (sor[idx['dontes']], sor[idx['igehely']])) from None
        j.indoklas = b.belso('B04', 'indoklas', indoklas.partition(_MEZO_ELVALASZTO)[0])
        elso = forras.split(_MEZO_ELVALASZTO)[0]
        m = _CSOPORT_VERSSZAM_RX.search(elso)
        j.csoport_versszam = int(m.group(1)) if m else None
        m = _OSSZESITO_RX.match(indoklas)
        j.osszesito_versszam = int(m.group(1)) if m else None
        m = _LISTA_RX.search(forras)
        j.lista_oszlop, j.lista_blokk = m.groups() if m else (None, None)
        m = _HALO_RX.search(forras)
        j.lista_halo = m.group(1) if m else None
        j.kulon_sor = _KULON_SOR in forras
        j.ajanlas = _NAPLO_RX.split(elso.strip())[0].strip().startswith(_AJANLAS_ELOTAGOK)
        ki.append(j)
    return tuple(ki)


# --- B56: az elutasítási okok mintaszótára -----------------------------------------------------------------------

class Ok:
    """Egy elutasítási ok: a kézi címke (a belső összesítő-jelölő nélkül) és a kézi megjegyzés (None, ha üres)."""
    __slots__ = ('cimke', 'megjegyzes')

    def __init__(self, cimke, megjegyzes):
        self.cimke, self.megjegyzes = cimke, megjegyzes


class Okok:
    """A mintaszótár: az indoklás szövegére illesztett minták a `sorrend` rendjében; az első egyező minta dönt."""

    def __init__(self, mintak, okok):
        self._mintak, self._okok = mintak, okok

    def besorol(self, indoklas):
        """Az indoklás (belső szöveg) oka. Be nem sorolható indoklás BemenetHiba: a lap nem találgat."""
        for minta, kulcs in self._mintak:
            if minta.search(indoklas.ertek):
                return self._okok[kulcs]
        raise BemenetHiba('B56: a mintaszótár nem sorolja be az indoklást: %s' % indoklas.ertek[:120])


def b56_okok(b, motivum):
    """B56 — az elutasítási okok mintaszótára: a motívum saját sorai és a minden motívumra érvényes sorok. A
    címke végén álló „(összesítő sor)” belső jelölő, nem a címke része; az azonos címkéjű sorok közül az első
    megjegyzése számít."""
    tabla = b._tabla('B56', oszlopok=('sorrend', 'id', 'minta', 'cimke', 'megjegyzes'))
    try:
        sorok = sorted((r for r in tabla.szotarak() if r['id'] in (_MINDEN_MOTIVUM, motivum.kod)),
                       key=lambda r: int(r['sorrend']))
    except ValueError:
        raise BemenetHiba('B56: a `sorrend` egész szám legyen') from None
    mintak, okok = [], {}
    for r in sorok:
        kulcs = _OSSZESITO_JELOLO_RX.sub('', r['cimke'])
        if not kulcs:
            raise BemenetHiba('B56: üres címke a(z) %s. sorrendű sorban' % r['sorrend'])
        try:
            mintak.append((re.compile(r['minta'], re.IGNORECASE), kulcs))
        except re.error as hiba:
            raise BemenetHiba('B56: hibás minta a(z) %s. sorrendű sorban: %s' % (r['sorrend'], hiba)) from None
        if kulcs not in okok:
            megjegyzes = r['megjegyzes'].strip()
            okok[kulcs] = Ok(b.kezi('B56', 'cimke', kulcs),
                             b.kezi('B56', 'megjegyzes', megjegyzes) if megjegyzes else None)
    return Okok(mintak, okok)


# --- B05: a teljesség-mérés pillanatképe ----------------------------------------------------------------------------

class Kereses:
    """A teljesség-mérés egy keresése (hálója): a kulcsa, a megvizsgált versek száma és a mérés forrássora."""
    __slots__ = ('kulcs', 'versszam', 'forrassor')

    def __init__(self, kulcs, versszam, forrassor):
        self.kulcs, self.versszam, self.forrassor = kulcs, versszam, forrassor


def b05_teljesseg(b, motivum, mai_strongok):
    """B05 — a teljesség-mérés pillanatképe keresésenként, az első előfordulás rendjében. Opcionális: ha a
    motívumnak nincs mérése, az eredmény None (kimondott hiány).

    Frissességi kapu: a pillanatkép a mérés idején érvényes Strong-halmazra készült. Ha a Strong-keresés
    forrássora nem nevezi meg a mért halmazt, vagy az nem a motívum mai Strong-halmaza (`mai_strongok`), a
    pillanatkép elavult: BemenetHiba, a lap nem készül el belőle."""
    if not b._van('B05', motivum):
        return None
    tabla = b._tabla('B05', motivum=motivum, oszlopok=('halo', 'igehely', 'proveniencia'))
    h, i, p = tabla.oszlop('halo'), tabla.oszlop('igehely'), tabla.oszlop('proveniencia')
    versek, forrassor = {}, {}
    for sor in tabla.sorok:
        versek.setdefault(sor[h], set()).add(sor[i])
        forrassor.setdefault(sor[h], sor[p])
    if _STRONG_HALO in versek:
        m = _MERT_STRONG_RX.search(forrassor[_STRONG_HALO])
        if not m:
            raise BemenetHiba('B05: a Strong-keresés forrássora nem nevezi meg a mért Strong-halmazt; a pillanatkép '
                              'frissessége nem igazolható: futtasd újra a teljesség-mérést')
        mert = frozenset(m.group(1).split('+'))
        if mert != frozenset(mai_strongok):
            raise BemenetHiba('B05: elavult pillanatkép: a mérés Strong-halmaza (%s) nem a motívum mai halmaza (%s); '
                              'futtasd újra a teljesség-mérést'
                              % ('+'.join(sorted(mert)), '+'.join(sorted(mai_strongok))))
    return tuple(Kereses(b.kulcs('B05', 'halo', halo), len(vv), b.belso('B05', 'proveniencia', forrassor[halo]))
                 for halo, vv in versek.items())


# --- B06: a teljesség-mérés csoportlistája --------------------------------------------------------------------------

class Csoportlista:
    """A csoportosan kizárt versek listája: a csoport tagjai a csoport kulcsa szerint."""

    def __init__(self, tabla):
        self._tabla = tabla

    def tagok(self, oszlop, blokk, halo):
        """A csoport verseinek kódja rendezve: az `oszlop` értéke a `blokk`; ha a jelölés keresést (`halo`) is
        megnevez, csak annak a sorai (a keresés oszlopa nélküli listában minden sor)."""
        if not self._tabla.van(oszlop) or not self._tabla.van('igehely'):
            raise BemenetHiba('B06: a csoportlistában nincs `%s` vagy `igehely` oszlop' % oszlop)
        o, i = self._tabla.oszlop(oszlop), self._tabla.oszlop('igehely')
        h = self._tabla.oszlop('halo') if self._tabla.van('halo') else None
        return sorted({sor[i] for sor in self._tabla.sorok
                       if sor[o] == blokk and (halo is None or h is None or sor[h] == halo)})


def b06_csoportlista(b, motivum):
    """B06 — a teljesség-mérés csoportlistája. Opcionális: hiánya None (a csoportos sor tagjai ilyenkor nem
    igazolhatók, és a számítás megáll, ha a motívumnak van csoportos sora)."""
    if not b._van('B06', motivum):
        return None
    return Csoportlista(b._tabla('B06', motivum=motivum, oszlopok=('igehely',)))


def vers_igehely(kod):
    """Egy verskód igehelyként (a döntésnapló és a csoportlista kulcsa); hibás alak BemenetHiba."""
    return _igehely(kod, 'B04/B06')
