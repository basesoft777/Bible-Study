"""lapgen.bemenet.kapcsolat — a motívum igehelyei közötti kapcsolatok és a motívumközi kapcsolatok (S6).

Bemenetek: B45 (a motívumon belüli igehely-párok kapcsolatai, SEMA 2.3), B46 (a motívumok közötti kapcsolatok,
SEMA 2.33) és B04 (a jelöltek döntésnaplója: a döntésre váró motívumközi jelöltek száma).

A két tábla `funkcio` mezője kézi próza: a lapon a táblacellában áll, változatlanul; a cellakezdő alak az adatban
a végleges alak (DT869). Az `indoklas` mező a B45-ben két részből áll: az első ` | ` előtti rész az Alátámasztás
kézi prózája (SEMA 2.3: „a lexikonoldal Alátámasztás-résének soronkénti adata”), a többi belső proveniencia (a
döntés hivatkozása és a lekérdezés sora), amely csak megjegyzésbe kerül. A B46 `indoklas` mezője a 8. szakasz
„Indoklás” cellájának kézi prózája. Mindkét táblában a kézi rész végén álló döntés-hivatkozás („Döntés: DT<n> (…).”,
illetve „(DT<n>, a felhasználó, …)”) szerkezet, amelyet a réteg leválaszt (DT-F218t; a döntést a B45 sor
proveniencia-része, illetve a B46 sor `dontes_ref` mezője hordozza); a próza többi része változatlan. A kézi
prózán a réteg kapuval ellenőrzi, hogy olvasói szöveg-e (ugyanaz a kapu, mint a kereszthivatkozásos indoklásé): ha
nem, megáll, nem tisztít.

A zárt értékkészletek (típus, bizonyosság) felsorolásra, a PaRDeS-szint névtábla-kulcsra alakul; ismeretlen érték
kemény hiba.
"""
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.kereszthiv import nem_olvasoi
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.ertekek import Dontes, KapcsolatTipus, Megbizhatosag, MotivumKapcsolatTipus
from lapgen.szoveg import MotivumId, SzovegHiba

_KAPCSOLAT_OSZLOPOK = ('forras_igehely', 'cel_igehely', 'id', 'tipus', 'funkcio', 'bizonyossag', 'pardes_szint',
                       'indoklas')
_MK_OSZLOPOK = ('id_a', 'igehely_a', 'id_b', 'igehely_b', 'tipus', 'funkcio', 'bizonyossag', 'pardes_szint',
                'indoklas')
_JELOLT_OSZLOPOK = ('id', 'dontes', 'jelolt_tipus', 'cel_id')
_MOTIVUMKOZI = 'motivumkozi'
_MEZO_ELVALASZTO = ' | '
_PARDES_ELVALASZTO = '/'
_DONTES_RX = re.compile(r'\bDT\d+\b')
# a mező végén álló döntés-hivatkozás két alakja: „Döntés: DT280 (…).” és „(DT479, a felhasználó, …: „…, (b)”)”
_ZARO_DONTES_RX = re.compile(r'\s*(?:Döntés:\s*DT-?F?\d+[a-z]?\s*(?:\([^()]*\))?\.?'
                             r'|\(DT-?F?\d+[a-z]?\b(?:[^()]|\([^()]*\))*\)\.?)\s*$')


def _zaro_dontes_nelkul(szoveg):
    """A kézi szöveg a végén álló döntés-hivatkozás nélkül (DT-F218t): a hivatkozás szerkezet, a döntést a sor
    proveniencia-része (B45) vagy `dontes_ref` mezője (B46) hordozza; a többi szöveg változatlan. Ha a hivatkozás
    máshol áll a szövegben, a kapu megáll."""
    return _ZARO_DONTES_RX.sub('', szoveg)


def _felsorolas(osztaly, nyers, b_id, mezo, hol):
    try:
        return osztaly(nyers.strip())
    except ValueError:
        raise BemenetHiba('%s: ismeretlen `%s` érték: %r (%s)' % (b_id, mezo, nyers, hol)) from None


def _kezi(b, b_id, mezo, nyers, hol):
    """Kézi próza a kapuval: üresnél None; ha nem olvasói szöveg, BemenetHiba."""
    szoveg = nyers.strip()
    if not szoveg:
        return None
    hiba = nem_olvasoi(szoveg)
    if hiba:
        raise BemenetHiba('%s: %s: a(z) `%s` mező nem olvasói szöveg (%r): a lap nem tisztít, a forrás javítandó'
                          % (b_id, hol, mezo, hiba))
    return b.kezi(b_id, mezo, szoveg)


def _pardes(b, b_id, nyers):
    return tuple(b.kulcs(b_id, 'pardes_szint', sz.strip()) for sz in nyers.split(_PARDES_ELVALASZTO) if sz.strip())


class Kapcsolat:
    """A motívum két igehelyének kapcsolata (B45 egy sora). `indok`: az Alátámasztás kézi prózája (None, ha nincs
    rögzített indoklás); `farok`: az indoklás belső proveniencia-része (None, ha nincs); `dontesek`: a farokban
    hivatkozott döntések azonosítói (a dátumuk megjegyzésbe kerül)."""
    __slots__ = ('forras', 'cel', 'tipus', 'funkcio', 'bizonyossag', 'pardes', 'indok', 'farok', 'dontesek')


def b45_kapcsolatok(b, motivum):
    """B45 — a motívum igehely-párjainak kapcsolatai, a tábla sorrendjében."""
    konyvek = b63_konyvek(b)
    tabla = b._tabla('B45', oszlopok=_KAPCSOLAT_OSZLOPOK)
    idx = {o: tabla.oszlop(o) for o in _KAPCSOLAT_OSZLOPOK}
    ki = []
    for sor in tabla.sorok:
        if sor[idx['id']] != motivum.kod:
            continue
        hol = '%s → %s' % (sor[idx['forras_igehely']], sor[idx['cel_igehely']])
        k = Kapcsolat()
        try:
            k.forras = konyvek.igehely(sor[idx['forras_igehely']])
            k.cel = konyvek.igehely(sor[idx['cel_igehely']])
        except BemenetHiba as hiba:
            raise BemenetHiba('B45: %s' % hiba) from None
        k.tipus = _felsorolas(KapcsolatTipus, sor[idx['tipus']], 'B45', 'tipus', hol)
        k.funkcio = _kezi(b, 'B45', 'funkcio', sor[idx['funkcio']], hol)
        k.bizonyossag = _felsorolas(Megbizhatosag, sor[idx['bizonyossag']], 'B45', 'bizonyossag', hol)
        k.pardes = _pardes(b, 'B45', sor[idx['pardes_szint']])
        fo, sep, farok = sor[idx['indoklas']].partition(_MEZO_ELVALASZTO)
        k.indok = _kezi(b, 'B45', 'indoklas', _zaro_dontes_nelkul(fo), hol)
        k.farok = b.belso('B45', 'indoklas_proveniencia', farok) if sep and farok.strip() else None
        k.dontesek = tuple(_DONTES_RX.findall(farok)) if sep else ()
        ki.append(k)
    return tuple(ki)


class MotivumKapcsolat:
    """Egy motívumközi kapcsolat a motívum szemszögéből: a másik motívum, az itteni és az ottani igehely."""
    __slots__ = ('masik', 'itt', 'ott', 'tipus', 'funkcio', 'bizonyossag', 'pardes', 'indok')


def _motivum(nyers, hol):
    try:
        return MotivumId(nyers.strip())
    except SzovegHiba as hiba:
        raise BemenetHiba('B46: %s: hibás motívumazonosító (%s)' % (hol, hiba)) from None


def b46_motivum_kapcsolatok(b, motivum):
    """B46 — a motívum motívumközi kapcsolatai (a sor mindkét érintett motívum lapján áll), a másik motívum, az
    itteni és az ottani igehely szerint rendezve."""
    konyvek = b63_konyvek(b)
    tabla = b._tabla('B46', oszlopok=_MK_OSZLOPOK)
    idx = {o: tabla.oszlop(o) for o in _MK_OSZLOPOK}
    ki = []
    for sor in tabla.sorok:
        if motivum.kod not in (sor[idx['id_a']], sor[idx['id_b']]):
            continue
        a_oldal = sor[idx['id_a']] == motivum.kod
        hol = '%s %s ↔ %s %s' % (sor[idx['id_a']], sor[idx['igehely_a']], sor[idx['id_b']], sor[idx['igehely_b']])
        mk = MotivumKapcsolat()
        mk.masik = _motivum(sor[idx['id_b'] if a_oldal else idx['id_a']], hol)
        try:
            itt = konyvek.igehely(sor[idx['igehely_a'] if a_oldal else idx['igehely_b']])
            ott = konyvek.igehely(sor[idx['igehely_b'] if a_oldal else idx['igehely_a']])
        except BemenetHiba as hiba:
            raise BemenetHiba('B46: %s' % hiba) from None
        mk.itt, mk.ott = itt, ott
        mk.tipus = _felsorolas(MotivumKapcsolatTipus, sor[idx['tipus']], 'B46', 'tipus', hol)
        mk.funkcio = _kezi(b, 'B46', 'funkcio', sor[idx['funkcio']], hol)
        mk.bizonyossag = _felsorolas(Megbizhatosag, sor[idx['bizonyossag']], 'B46', 'bizonyossag', hol)
        mk.pardes = _pardes(b, 'B46', sor[idx['pardes_szint']])
        # a záró döntés-hivatkozás („Döntés: DT280 (…).”) szerkezet: a döntést a `dontes_ref` és a jelölt sora
        # hordozza, a lapon nem áll (a régi lap is levágta); a kézi próza az előtte álló rész, változatlanul
        mk.indok = _kezi(b, 'B46', 'indoklas', _zaro_dontes_nelkul(sor[idx['indoklas']]), hol)
        ki.append(mk)
    ki.sort(key=lambda m: (m.masik.kod, m.itt.kod, m.ott.kod))
    return tuple(ki)


def motivumkozi_nyitott(b, motivum):
    """A B04 döntésre váró motívumközi jelöltjei, amelyek a motívumot érintik: ((másik motívum, darab), …) a másik
    motívum azonosítója szerint."""
    tabla = b._tabla('B04', oszlopok=_JELOLT_OSZLOPOK)
    idx = {o: tabla.oszlop(o) for o in _JELOLT_OSZLOPOK}
    szam = {}
    for sor in tabla.sorok:
        if sor[idx['jelolt_tipus']] != _MOTIVUMKOZI:
            continue
        try:
            dontes = Dontes(sor[idx['dontes']])
        except ValueError:
            raise BemenetHiba('B04: ismeretlen döntés-érték: %r (motívumközi jelölt)' % sor[idx['dontes']]) from None
        if dontes is not Dontes.NYITVA:
            continue
        if sor[idx['id']] == motivum.kod:
            masik = sor[idx['cel_id']]
        elif sor[idx['cel_id']] == motivum.kod:
            masik = sor[idx['id']]
        else:
            continue
        m = _motivum(masik, 'B04 motívumközi jelölt')
        szam[m] = szam.get(m, 0) + 1
    return tuple(sorted(szam.items(), key=lambda x: x[0].kod))
