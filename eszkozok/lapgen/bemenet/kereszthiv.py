"""lapgen.bemenet.kereszthiv — a két hagyományos kereszthivatkozás-gyűjtemény a 6. szakaszhoz és a Minősítéshez (S5).

Bemenetek: B44 (a Treasury of Scripture Knowledge kereszthivatkozásai, KJV-számozással), B34 (a Károli-vers és a
KJV-vers megfeleltetése), B43 (a Károli-fordítás kereszthivatkozásai a HunKar-kiadásból, nyersen), B72 (a Károli-KH
javított, a MEK 00161 kiadással összevetett háromszintű táblája), B63 (a könyvek STEPBible-rövidítése), B04 (a jelöltek
döntésnaplója: a kereszthivatkozásból vizsgált helyek) és B56 (az elutasítási okok).

A TSK mindkét kulcsa KJV-számozású: a Károli-versre a megfeleltetés váltja (a régi `tsk_kulcs` szabálya: az ószövetségi
könyvekben a tábla párja, az MT-tartalék csak a számlálással kapott MT-osztályú soron; az Újszövetségben azonosság). A
Károli-KH sorai közül csak a javított tábla `megerositett` szintű sora jut tovább (a régi `karoli_kh_szuro` hozzáférési
pontja: a nyers sorok és a csak a MEK-ben álló megerősített sorok, azonos kulcs egyszer); a többi sor száma
forrásversenként kimondva áll.

A döntésnapló kereszthivatkozásos sorainak két szabad mezője közül az `indoklas` itt kézi próza: a lapon a vizsgált hely
indokaként áll, változatlanul (a régi lap is ezt közölte). Ezért a réteg kapuval ellenőrzi, hogy olvasói szöveg-e:
belső jelölés, egyenes idézőjel vagy kódjel esetén megáll, nem tisztít. A szövegben álló motívum-hivatkozás
(`[ID: <azonosító>]`) szerkezet: a réteg darabokra bontja (kézi szöveg és motívumazonosító). A `forras_kereses`
belső szöveg: a réteg csak a szerkezetét olvassa ki (melyik gyűjtemény, melyik helyről, hány szavazattal).
"""
import re

from lapgen.bemenet import dontes as dontes_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.ertekek import AjanlasFajta, Dontes, Gyujtemeny
from lapgen.szoveg import Igehely, MotivumId, Strong, SzovegHiba, prov

_TSK_OSZLOPOK = ('Igehely', 'Kapcsolódó igehely', 'Votes')
_MEGF_OSZLOPOK = ('igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly', 'forras')
_KH_OSZLOPOK = ('Igehely', 'Kapcsolódó igehely', 'Kapcsolódó igehely magyar megjelenítése')
_JAV_OSZLOPOK = ('igehely', 'kapcsolodo', 'szint', 'forras')
_JELOLT_OSZLOPOK = ('id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'jelolt_tipus')
_VERS_RX = re.compile(r'^(.+?) (\d+):(\d+)$')
_MT_OSZTALY, _SZAMLALAS = 'MT', 'szamlalas'
_SZINT_RANG = {'megerositett': 0, 'jelolt': 1, 'kiesik': 2}
_MEGEROSITETT, _MEK = 'megerositett', 'MEK'
_KH_MEGJELENITES_RX = re.compile(r'^\S+ (\d+)[,:](\d+)(.*)$')
_ELOFORDULAS_JELOLT = 'elofordulas'
_MEZO_ELVALASZTO = ' | '
_NAPLO_RX = re.compile(r';\s*napló:')

# a forrás-mező szerkezete (a régi `szerep_kizart.jeloles_oka` kereszthivatkozásos ágai)
_HELY_RX = re.compile(r'\b[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6} \d+:\d+(?:-\d+)?')
_TOBB_RX = re.compile(r'TSK (%s(?:,\s*\d+:\d+(?:-\d+)?)+)' % _HELY_RX.pattern)
_ZAROJEL_RX = re.compile(r'\(([^)]*)\)')
_VOTES_RX = re.compile(r'Votes=(-?\d+)')
_TALALAT_RX = re.compile(r'(\d+) találat')
_SZAVAZATLISTA_RX = re.compile(r'[\d\s,\-–]+')
_SZAVAZAT_ELEM_RX = re.compile(r'(\d+)(?:-(\d+))?')
_ELOTAG_TSK_KAROLI, _ELOTAG_TSK, _ELOTAG_KAROLI = 'TSK/Károli-KH', 'TSK', 'Károli-KH'
_ALACSONY = 'alacsony szavazat'
_KAROLI_IS = 'Károli-KH is'

# az indoklás mint kézi próza: amit a lap nem közölhet (belső jelölés, munkaszó, kódjel, egyenes idézőjel)
_MOTIVUM_HIV_RX = re.compile(r'\[ID: ([A-Z]+-\d{3})\]')
# a Strong-szám, közvetlenül utána a héber vagy görög szó (a régi `olvasoi_utofeldolg.STRONG_ELOL`): Strong-hivatkozás
_SCRIPT = '[֐-׿Ͱ-Ͽἀ-῿]'
_JELEK = '[֑-ׇ̀-ͯ־]'
_SZKRIPT_SZO = '(?:' + _SCRIPT + '|' + _JELEK + r'|\w)*' + _SCRIPT + '(?:' + _SCRIPT + '|' + _JELEK + r'|\w)*'
_STRONG_HIV_RX = re.compile(r'(?<![\w+/])(?<![+/]\s)(?P<strong>[HG]\d{4}[a-z]?)\s+(?P<szo>' + _SZKRIPT_SZO + ')')
_NEM_OLVASOI_RX = re.compile(
    r'"|`|\[ID:|\bscope=|\bforras=|(?<![\w-])DT-?F?\d+|(?<![\w/.#-])(?:F\d{2,3}|N-?F?\d+[a-z]?)\b|(?<![\w&/])#\d{2,3}\b'
    r'|\.(?:tsv|py|md)\b|\(\s*[HG]\d{4}[a-z]?\s*\)|\borkesztrátor|\bstudy\b|\bscan|Strong-keresés|\||\n')
_SZO_RX = re.compile(r'\w+')
_CIMKE_TILTOTT_RX = re.compile(r'[\d\[\]→#(]')
_NAPLO_FORRAS_RX = re.compile(r'_kereszthivatkozas_naplo\.md$')
_MANUAL = 'manual'
_NAPLO_NEV, _KEZI_NEV, _MUNKAANYAG_NEV = 'a motívum korábbi kereszthivatkozás-naplója', 'kézi szerkesztés', 'a lap munkaanyaga'
_PROV_RX = re.compile(r'scope=(?P<scope>[^|]*?)\s*\|\s*forras=(?P<forras>[^|]*?)\s*\|\s*ts=(?P<ts>[0-9T:Z-]+)')


class Utalas:
    """Egy kereszthivatkozás egy forrásversről: a cél igehelye, a gyűjtemény és (a TSK-nál) a szavazatszám."""
    __slots__ = ('cel', 'gyujtemeny', 'szavazat')

    def __init__(self, cel, gyujtemeny, szavazat=None):
        self.cel, self.gyujtemeny, self.szavazat = cel, gyujtemeny, szavazat


# --- B34 + B44: a TSK Károli-kulcsra váltva -------------------------------------------------------------------------

class _Megfeleltetes:
    """A Károli- és a KJV-versszámozás megfeleltetése (a régi `tsk_kulcs` szabálya)."""

    def __init__(self, k2j, j2k, konyvek):
        self._k2j, self._j2k, self._konyvek = k2j, j2k, konyvek

    def karoli_kjv(self, vers):
        m = _VERS_RX.match(vers)
        if m is None:
            return None
        if m.group(1) not in self._konyvek:
            return vers      # az Újszövetség: azonosság (a tábla az Ószövetséget fedi)
        return self._k2j.get(vers) or None

    def kjv_karoli(self, vers):
        m = _VERS_RX.match(vers)
        if m is None:
            return []
        if m.group(1) not in self._konyvek:
            return [vers]
        return list(self._j2k.get(vers, ()))


def _megfeleltetes(b):
    def betolt():
        tabla = b._tabla('B34', oszlopok=_MEGF_OSZLOPOK)
        ik, ij, im, io, ifo = (tabla.oszlop(o) for o in _MEGF_OSZLOPOK)
        k2j, j2k, konyvek = {}, {}, set()
        for sor in tabla.sorok:
            m = _VERS_RX.match(sor[ik])
            if m is None:
                continue
            konyvek.add(m.group(1))
            kj = sor[ij].strip()
            if not kj and sor[io] == _MT_OSZTALY and sor[ifo] == _SZAMLALAS and sor[im].strip():
                kj = sor[im].strip()
            if kj:
                kj = '%s %s' % (m.group(1), kj)
                k2j[sor[ik]] = kj
                j2k.setdefault(kj, []).append(sor[ik])
            else:
                k2j[sor[ik]] = ''
        return _Megfeleltetes(k2j, j2k, frozenset(konyvek))
    return b.egyszer('B34-tsk', betolt)


def _tsk_epit(b):
    tabla = b._tabla('B44', oszlopok=_TSK_OSZLOPOK)
    i, c, v = (tabla.oszlop(o) for o in _TSK_OSZLOPOK)
    index = {}
    for sor in tabla.sorok:
        try:
            szavazat = int(sor[v])
        except ValueError:
            raise BemenetHiba('B44: a szavazatszám nem egész szám: %r (%s → %s)' % (sor[v], sor[i], sor[c])) from None
        index.setdefault(sor[i], []).append((sor[c], szavazat))
    return index


def b44_tsk(b, vers, kuszob):
    """B44 — a Károli-vers TSK-utalásai Károli-kulcsra váltva, a legalább `kuszob` szavazatúak, a forrás sorrendjében.
    A tartomány-igehelyre a gyűjtemény nem ad utalást (üres)."""
    megf = _megfeleltetes(b)
    konyvek = b63_konyvek(b)
    kjv = megf.karoli_kjv(vers.kod)
    if kjv is None:
        return ()
    ki = []
    for cel_kjv, szavazat in b.egyszer('B44', lambda: _tsk_epit(b)).get(kjv, ()):
        if szavazat < kuszob or vers.kod not in megf.kjv_karoli(kjv):
            continue
        for cel in megf.kjv_karoli(cel_kjv):
            ki.append(Utalas(konyvek.igehely(cel), Gyujtemeny.TSK, szavazat))
    return tuple(ki)


# --- B43 + B72: a Károli-KH megerősített sorai ---------------------------------------------------------------------

class _KarolKh:
    def __init__(self, sorok, elvetett):
        self.sorok, self.elvetett = sorok, elvetett


def _javitott_epit(b):
    konyvek = b63_konyvek(b)
    szint, mek = {}, []
    jav = b._tabla('B72', oszlopok=_JAV_OSZLOPOK)
    ji, jk, js, jf = (jav.oszlop(o) for o in _JAV_OSZLOPOK)
    for sor in jav.sorok:
        if not sor[ji]:
            continue
        kulcs = (sor[ji], sor[jk])
        if kulcs not in szint or _SZINT_RANG.get(sor[js], 9) < _SZINT_RANG.get(szint[kulcs], 9):
            szint[kulcs] = sor[js]
        if sor[js] == _MEGEROSITETT and sor[jf] == _MEK:
            reszek = sor[jk].split('.')
            if len(reszek) == 3 and konyvek.step_ismert(reszek[0]):
                mek.append((sor[ji], sor[jk], '%s %s,%s' % (konyvek.step_rov(reszek[0]), reszek[1], reszek[2])))
    return szint, tuple(mek)


def b72_karoli_kh_javitott(b):
    """B72 — a Károli-KH javított táblája: ({(forrás, cél): a legjobb szint}, a csak a MEK-ben álló megerősített sorok
    (forrás, cél, megjelenítés) alakban, a magyar megjelenítés a normalizáló tábla könyvnevével)."""
    return b.egyszer('B72', lambda: _javitott_epit(b))


def _karoli_kh_epit(b):
    szint, mek = b72_karoli_kh_javitott(b)
    nyers = b._tabla('B43', oszlopok=_KH_OSZLOPOK)
    ni, nk, nm = (nyers.oszlop(o) for o in _KH_OSZLOPOK)
    forrasonkent = {}
    for forras, cel, megj in [(s[ni], s[nk], s[nm]) for s in nyers.sorok] + list(mek):
        forrasonkent.setdefault(forras, []).append((cel, megj))
    sorok, elvetett = {}, {}
    for forras, elemek in forrasonkent.items():
        latott, egyedi = set(), []
        for cel, megj in elemek:
            if cel not in latott:
                latott.add(cel)
                egyedi.append((cel, megj))
        jo = [(cel, megj) for cel, megj in egyedi if szint.get((forras, cel)) == _MEGEROSITETT]
        if len(jo) < len(egyedi):
            elvetett[forras] = len(egyedi) - len(jo)
        sorok[forras] = tuple(jo)
    return _KarolKh(sorok, elvetett)


def _kh_cel(konyvek, cel, megjelenites):
    """A Károli-KH célhelye igehelyként: a könyv a cél STEPBible-alakjából (a normalizáló tábla rövidítése), a
    fejezet és a vers a forrás magyar megjelenítéséből (`2,4-5` és `2:4-5` egyaránt → `2:4-5`)."""
    m = _KH_MEGJELENITES_RX.match(megjelenites)
    step = cel.split('-')[0].split('.')[0]
    if m is None or not konyvek.step_ismert(step):
        raise BemenetHiba('B43: a Károli-KH célhelye nem értelmezhető: %s (%s)' % (megjelenites, cel))
    return konyvek.igehely('%s %s:%s%s' % (konyvek.step_rov(step), m.group(1), m.group(2), m.group(3)))


def b43_karoli_kh(b, vers):
    """B43 (B72-vel) — a Károli-vers megerősített Károli-KH utalásai és a nem megerősített sorok száma."""
    kh = b.egyszer('B43', lambda: _karoli_kh_epit(b))
    konyvek = b63_konyvek(b)
    step = konyvek.step_vers(vers)
    return (tuple(Utalas(_kh_cel(konyvek, cel, megj), Gyujtemeny.KAROLI) for cel, megj in kh.sorok.get(step, ())),
            kh.elvetett.get(step, 0))


# --- B04: a kereszthivatkozásból vizsgált helyek ------------------------------------------------------------------

class Ajanlas:
    """A jelölés oka a forrás-mezőből: a gyűjtemény, a forrásverse(i) (az első teljes igehely, a többi ugyanabból a
    könyvből), a célhely (ha az ajánlás iránya is meg van adva), a szavazatszámok ((tól, ig) párok; az `ig` None, ha
    egyetlen szám) vagy a forráshely TSK-találatainak száma, és hogy a Károli is ajánlja-e."""
    __slots__ = ('fajta', 'forrasok', 'cel', 'szavazatok', 'talalat', 'karoli_is')

    def __init__(self, fajta, forrasok=(), cel=None, szavazatok=None, talalat=None, karoli_is=False):
        self.fajta, self.forrasok, self.cel = fajta, forrasok, cel
        self.szavazatok, self.talalat, self.karoli_is = szavazatok, talalat, karoli_is


class IndokDarab:
    """Az indoklás egy darabja: kézi szöveg (`Kezi`), motívum-hivatkozás (`MotivumId`), vagy Strong-hivatkozás (a
    `strong` és a szó kézi szövegként, `kezi`)."""
    __slots__ = ('kezi', 'motivum', 'strong')

    def __init__(self, kezi=None, motivum=None, strong=None):
        self.kezi, self.motivum, self.strong = kezi, motivum, strong


class KhJelolt:
    """Egy kereszthivatkozásból vizsgált hely: igehely, döntés, a jelölés oka, az indoklás darabjai, az elutasítás
    oka (`dontes_be.Ok`; nem elutasított helynél None), hogy az indoklás eleje maga kimondja-e az okot
    (`ok_ismetles`: ilyenkor a cellában csak az indoklás áll), és a forrás-mező proveniencia-sora (None, ha nincs)."""
    __slots__ = ('igehely', 'dontes', 'ajanlas', 'indok', 'ok', 'ok_ismetles', 'prov')

    def __init__(self, igehely, dontes, ajanlas, indok, ok, ok_ismetles, prov):
        self.igehely, self.dontes, self.ajanlas, self.indok = igehely, dontes, ajanlas, indok
        self.ok, self.ok_ismetles, self.prov = ok, ok_ismetles, prov


class ProvSor:
    """A forrás-mező proveniencia-sora: a kulcs (scope, forrás, dátum), a teljes alak és az olvasói alak, mindkettő
    megjegyzésbe kerül (a régi `_prov_olvasoi` szerint)."""
    __slots__ = ('kulcs', 'harmas', 'olvasoi')

    def __init__(self, scope, forras, ts):
        self.kulcs = (scope, forras, ts)
        self.harmas = prov('scope={} | forras={} | ts={}', scope, forras, ts)
        nevek = []
        for f in re.split(r'[+,;]\s*', forras.strip()):
            f = re.sub(r'\s*\(.*$', '', f).strip()
            if f and _NAPLO_FORRAS_RX.search(f):
                nevek.append(_NAPLO_NEV)
        if scope.strip() == _MANUAL:
            nevek.append(_KEZI_NEV)
        datum = re.match(r'\d{4}-\d\d-\d\d', ts)
        self.olvasoi = prov('forrás: {}{}', '; '.join(nevek) or _MUNKAANYAG_NEV,
                            (', ' + datum.group(0)) if datum else '')


def cimke_ismetles(cimke, szoveg):
    """Igaz, ha az indoklás eleje (az első nyolc szó) a címke tartalmas szavait ismétli (a régi
    `szerep_kizart.cimke_ismetles`): ilyenkor a cellában csak az indoklás áll. A négy szónál rövidebb szöveg nem
    indoklás; a számot, zárójelet vagy nyilat tartalmazó címke nem hasonlítható."""
    cim = (cimke or '').strip().lower()
    if not cim or _CIMKE_TILTOTT_RX.search(cim):
        return False
    tobbi = _SZO_RX.findall((szoveg or '').lower())
    if len(tobbi) < 4:
        return False
    cim_szavai = _SZO_RX.findall(cim)
    if len(cim_szavai) >= 2 and tobbi[:2] == cim_szavai[:2]:
        return True
    szavak = [w for w in cim_szavai if len(w) > 3]
    eleje = ' '.join(tobbi[:8])
    return bool(szavak) and sum(w in eleje for w in szavak) >= max(1, len(szavak) - 1)


def _igehely(nyers, konyvek):
    """A forrás-mező igehelye. A mező belső szöveg, a könyvnevét a döntésnapló írója adta: a lapra a normalizáló
    tábla rövidítése kerül; a tábla `Forrás-alakok` oszlopában álló alak (pl. `Zef`, N195) a rövidítésre cserélődik
    (F241.5b, D13 (d)). Érvénytelen alak vagy ismeretlen könyvnév BemenetHiba."""
    try:
        return konyvek.forrasalak_igehely(nyers)
    except BemenetHiba as hiba:
        raise BemenetHiba('B04: a forrás-mező igehelye: %s' % hiba) from None


def _szavazatok(szoveg):
    elemek = []
    for resz in szoveg.split(','):
        m = _SZAVAZAT_ELEM_RX.fullmatch(resz.strip())
        if m is None:
            raise BemenetHiba('B04: a szavazatszámok alakja nem a megszokott („%s”)' % szoveg)
        elemek.append((int(m.group(1)), int(m.group(2)) if m.group(2) else None))
    # a lapon a szerkezetből készül az alak: csak akkor, ha ugyanazt adja, mint a forrás (néma változás nincs)
    if ', '.join('%d-%d' % (a, z) if z is not None else '%d' % a for a, z in elemek) != szoveg.strip():
        raise BemenetHiba('B04: a szavazatszámok alakja nem a megszokott („%s”)' % szoveg)
    return tuple(elemek)


def _ajanlas(fo, konyvek):
    """A forrás-mező első részének szerkezete (a régi `jeloles_oka` kereszthivatkozásos ágai)."""
    helyek = _HELY_RX.findall(fo)
    elso = _igehely(helyek[0], konyvek) if helyek else None
    if fo.startswith(_ELOTAG_TSK_KAROLI):
        return Ajanlas(AjanlasFajta.TSK_KAROLI, (elso,) if elso else ())
    if fo.startswith(_ELOTAG_TSK):
        if _ALACSONY in fo:
            return Ajanlas(AjanlasFajta.TSK_ALACSONY)
        cel = _igehely(helyek[1], konyvek) if ('→' in fo or '↔' in fo) and len(helyek) > 1 else None
        forrasok = (elso,) if elso else ()
        tobb = _TOBB_RX.match(fo)
        if tobb and cel is None:
            reszek = [x.strip() for x in tobb.group(1).split(',')]
            forrasok = (elso,) + tuple(_igehely('%s %s' % (elso.konyv, r), konyvek) for r in reszek[1:])
        szavazatok = talalat = None
        p = _ZAROJEL_RX.search(fo)
        if p and elso:
            t = p.group(1).strip()
            v = _VOTES_RX.fullmatch(t)
            tm = _TALALAT_RX.fullmatch(t)
            if v:
                szavazatok = ((int(v.group(1)), None),)
            elif tm:
                talalat = int(tm.group(1))
            elif _SZAVAZATLISTA_RX.fullmatch(t):
                szavazatok = _szavazatok(t)
        return Ajanlas(AjanlasFajta.TSK, forrasok, cel, szavazatok, talalat, _KAROLI_IS in fo)
    if fo.startswith(_ELOTAG_KAROLI):
        return Ajanlas(AjanlasFajta.KAROLI, (elso,) if elso else ())
    raise BemenetHiba('B04: a kereszthivatkozásos jelölés forrása nem értelmezhető: %s' % fo[:120])


def nem_olvasoi(szoveg):
    """Az első olyan részlet, amely miatt a kézi szöveg nem kerülhet a lapra (belső jelölés, munkaszó, kódjel,
    egyenes idézőjel, cellahatár), vagy None. A motívum-hivatkozás (`[ID: …]`) itt hibának számít: ahol szerkezet
    lehet, a hívó előbb darabolja."""
    m = _NEM_OLVASOI_RX.search(szoveg)
    return m.group(0) if m else None


def _indok(b, szoveg, igehely):
    """Az indoklás darabjai; ami nem olvasói szöveg, azon a réteg megáll (nem tisztít)."""
    darabok, veg = [], 0
    for m in _MOTIVUM_HIV_RX.finditer(szoveg):
        if m.start() > veg:
            darabok.append(szoveg[veg:m.start()])
        try:
            darabok.append(MotivumId(m.group(1)))
        except SzovegHiba as hiba:
            raise BemenetHiba('B04: %s: hibás motívum-hivatkozás (%s)' % (igehely, hiba)) from None
        veg = m.end()
    if veg < len(szoveg):
        darabok.append(szoveg[veg:])
    ki = []
    for d in darabok:
        if isinstance(d, MotivumId):
            ki.append(IndokDarab(motivum=d))
            continue
        hiba = _NEM_OLVASOI_RX.search(d)
        if hiba:
            raise BemenetHiba('B04: %s: az indoklás nem olvasói szöveg (%r): a lap nem tisztít, a forrás javítandó'
                              % (igehely, hiba.group(0)))
        veg = 0
        for m in _STRONG_HIV_RX.finditer(d):
            if m.start() > veg:
                ki.append(IndokDarab(kezi=b.kezi('B04', 'indoklas_kh', d[veg:m.start()])))
            ki.append(IndokDarab(kezi=b.kezi('B04', 'indoklas_kh', m.group('szo')), strong=Strong(m.group('strong'))))
            veg = m.end()
        if veg < len(d):
            ki.append(IndokDarab(kezi=b.kezi('B04', 'indoklas_kh', d[veg:])))
    return tuple(ki)


def kereszthiv_jeloltek(b, motivum):
    """A B04 kereszthivatkozásos sorai: a motívum kereszthivatkozásból vizsgált előfordulás-jelöltjei a döntésnapló sorrendjében."""
    konyvek = b63_konyvek(b)
    okok = dontes_be.b56_okok(b, motivum)
    tabla = dontes_be.jeloltnaplo_tabla(b)
    idx = {o: tabla.oszlop(o) for o in _JELOLT_OSZLOPOK}
    ki = []
    for sor in tabla.sorok:
        forras = sor[idx['forras_kereses']]
        if (sor[idx['id']] != motivum.kod or sor[idx['jelolt_tipus']] != _ELOFORDULAS_JELOLT
                or not forras.startswith((_ELOTAG_TSK, _ELOTAG_KAROLI))):
            continue
        igehely = dontes_be.vers_igehely(sor[idx['igehely']])
        try:
            dontes = Dontes(sor[idx['dontes']])
        except ValueError:
            raise BemenetHiba('B04: ismeretlen döntés-érték: %r (%s)' % (sor[idx['dontes']], igehely.kod)) from None
        reszek = forras.split(_MEZO_ELVALASZTO)
        fo = _NAPLO_RX.split(reszek[0].strip())[0].strip()
        p = _PROV_RX.search(forras)
        indok_fo = sor[idx['indoklas']].partition(_MEZO_ELVALASZTO)[0]
        indok = _indok(b, indok_fo, igehely.kod) if indok_fo.strip() else ()
        ok = okok.besorol(b.belso('B04', 'indoklas', indok_fo)) if dontes is Dontes.ELUTASITVA else None
        ki.append(KhJelolt(
            igehely=igehely, dontes=dontes, ajanlas=_ajanlas(fo, konyvek), indok=indok, ok=ok,
            ok_ismetles=bool(ok is not None and indok and cimke_ismetles(ok.cimke.ertek, indok_fo)),
            prov=ProvSor(p.group('scope'), p.group('forras'), p.group('ts')) if p else None))
    return tuple(ki)
