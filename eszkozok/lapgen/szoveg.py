"""lapgen.szoveg — a lap szövegének típusai (alapszabály: DT823).

A látható szöveg külön típus (`Lathato`), pontosan három konstruktorral:

    proza(kezi)                  a kézi forrás egy rése vagy prózamezője, változatlanul
    sablon(sor, **parameterek)   a sablontábla egy sora; a paraméter típusa kötött, nyers `str` nem lehet
    idezet(forrasszoveg)         bibliavers vagy szótárszöveg a bemeneti rétegből; a forrást és a helyet
                                 maga az érték hordozza, így a kettő nem térhet el egymástól

A `Lathato` nem `str`: nincs rajta `replace`, szeletelés, formázás, és `str()`-rel sem alakítható
szöveggé. Szöveg csak a `kiiras()` függvénnyel lesz belőle, amelyet a megjelenítő író modulja hív.

A proveniencia külön típus (`Proveniencia`): a megjelenítő csak HTML-megjegyzésbe és a Kolofonba írja.

A bemeneti rétegből érkező nyers szöveg négyféle burkolóban jön, és a burkoló dönti el, mi lehet belőle:

    Kezi           kézzel írt próza            → proza()
    Forrasszoveg   idézhető forrásszöveg       → idezet()
    Belso          belső szabad szöveg         → csak Proveniencia
    Kulcs          belső azonosító, állapot    → névtábla (Nev) vagy Proveniencia
    Utvonal        fájlútvonal                 → csak Proveniencia

A festékpróba (`festek.py`) a burkolók szöveges alakját jelzőszóval látja el; a jelzőszó a kész lapon
megmutatja, ha egy belső mező a látható szövegbe szivárgott.
"""
import datetime
import enum
import re

# ---------------------------------------------------------------------------
# Hibák
# ---------------------------------------------------------------------------


class SzovegHiba(TypeError):
    """A látható szöveg szabályának megsértése (rossz típusú paraméter, tiltott átalakítás)."""


class SablonHiba(ValueError):
    """Hibás sablonsor vagy hibás sablonhívás (hiányzó, fölös vagy rossz típusú paraméter)."""


# ---------------------------------------------------------------------------
# Nyilvános azonosítók: megjeleníthetők, mert szigorú alakjuk miatt szabad szöveget nem hordozhatnak
# ---------------------------------------------------------------------------

_STRONG_RX = re.compile(r'^[HG]\d{4,5}[a-z]?$')
_MOTIVUM_RX = re.compile(r'^[A-Z]+-\d{3}$')
_HORGONY_RX = re.compile(r'^[0-9a-zà-ÿőű_-]+$')
_HORGONY_TISZTIT_RX = re.compile(r'[^0-9A-Za-zÀ-ÿ]+')
_IGEHELY_RX = re.compile(
    r'^(?P<konyv>[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ]*) '
    r'(?P<fejezet>\d+):(?P<vers>\d+)(?P<tobbi>(?:[-,]\d+(?::\d+)?)*)$')


class _Azonosito:
    """Közös ős: változtathatatlan, érték szerint egyenlő, szöveggé csak a konstruktorok alakítják."""
    __slots__ = ('_ertek',)
    _RX = None
    _NEV = 'azonosító'

    def __init__(self, ertek):
        if not isinstance(ertek, str) or not self._RX.match(ertek):
            raise SzovegHiba('érvénytelen %s: %r' % (self._NEV, ertek))
        object.__setattr__(self, '_ertek', ertek)

    def __setattr__(self, nev, ertek):
        raise AttributeError('változtathatatlan')

    def __eq__(self, masik):
        return type(masik) is type(self) and masik._ertek == self._ertek

    def __hash__(self):
        return hash((type(self).__name__, self._ertek))

    def __lt__(self, masik):
        return self._ertek < masik._ertek

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._ertek)

    def __str__(self):
        raise SzovegHiba('%s nem alakítható közvetlenül szöveggé; sablonparaméterként add át' % type(self).__name__)

    __format__ = None

    @property
    def kod(self):
        """Az azonosító nyers alakja, keresési kulcsnak és útvonalnak (nem látható szövegnek)."""
        return self._ertek


class Strong(_Azonosito):
    __slots__ = ()
    _RX = _STRONG_RX
    _NEV = 'Strong-szám'

    @property
    def heber(self):
        return self._ertek.startswith('H')


class MotivumId(_Azonosito):
    __slots__ = ()
    _RX = _MOTIVUM_RX
    _NEV = 'motívumazonosító'


class Horgony(_Azonosito):
    """Lapon belüli horgony azonosítója (a `#` nélkül); a szakaszmodell és az igehely-horgony adja."""
    __slots__ = ()
    _RX = _HORGONY_RX
    _NEV = 'horgony'


class Igehely(_Azonosito):
    """Igehely a Károli-alakban (`1Móz 3:14`, `Gal 3:13-14`). A könyvnév érvényességét a bemeneti réteg
    ellenőrzi a normalizáló táblán; itt csak az alak kötött."""
    __slots__ = ('_konyv', '_fejezet', '_vers')
    _RX = _IGEHELY_RX
    _NEV = 'igehely'

    def __init__(self, ertek):
        _Azonosito.__init__(self, ertek)
        m = _IGEHELY_RX.match(ertek)
        object.__setattr__(self, '_konyv', m.group('konyv'))
        object.__setattr__(self, '_fejezet', int(m.group('fejezet')))
        object.__setattr__(self, '_vers', int(m.group('vers')))

    @property
    def konyv(self):
        return self._konyv

    @property
    def fejezet(self):
        return self._fejezet

    @property
    def vers(self):
        return self._vers

    def horgony(self):
        """Az igehely lapon belüli horgonya (`ige-1móz-3-14`): a 2.1 pont célpontja."""
        return Horgony('ige-' + _HORGONY_TISZTIT_RX.sub('-', self._ertek).strip('-').lower())


# ---------------------------------------------------------------------------
# A bemeneti réteg burkolói (csak a `bemenet/` hozza létre őket; a statikus teszt őrzi)
# ---------------------------------------------------------------------------

FESTEK_ELOTAG = 'ZZQ'
FESTEK_UTOTAG = 'ZZ'


class _Nyers:
    """Bemeneti szöveg burkolója. Az `ertek` a számításé (összevetés, keresés); a `szoveg` az, ami a
    lapra vagy megjegyzésbe kerülhet, és festett futásban a jelzőszót is hordozza."""
    __slots__ = ('_ertek', '_mezo', '_jel')
    _JEL_ELOL = True

    def __init__(self, ertek, mezo, jel=''):
        if not isinstance(ertek, str):
            raise SzovegHiba('a burkoló értéke szöveg legyen: %r' % (ertek,))
        object.__setattr__(self, '_ertek', ertek)
        object.__setattr__(self, '_mezo', mezo)
        object.__setattr__(self, '_jel', jel)

    def __setattr__(self, nev, ertek):
        raise AttributeError('változtathatatlan')

    @property
    def ertek(self):
        return self._ertek

    @property
    def mezo(self):
        return self._mezo

    @property
    def szoveg(self):
        if not self._jel:
            return self._ertek
        if self._JEL_ELOL:
            return self._jel + self._ertek
        return self._ertek + ' ' + self._jel if self._ertek else self._jel

    def __bool__(self):
        return bool(self._ertek)

    def __eq__(self, masik):
        return type(masik) is type(self) and masik._ertek == self._ertek

    def __hash__(self):
        return hash((type(self).__name__, self._ertek))

    def __repr__(self):
        return '%s(%r, mezo=%r)' % (type(self).__name__, self._ertek, self._mezo)

    def __str__(self):
        raise SzovegHiba('%s nem alakítható közvetlenül szöveggé' % type(self).__name__)

    __format__ = None


class Kezi(_Nyers):
    """Kézzel írt próza: a forrásfájl egy rése vagy egy adattábla prózamezője."""
    __slots__ = ()
    _JEL_ELOL = False


class Forrasszoveg(_Nyers):
    """Idézhető forrásszöveg (bibliavers, szótárszöveg, átírás). A `forras` a bemenet B-azonosítója,
    a `hely` az idézet helye (igehely, Strong-szám vagy sorkulcs)."""
    __slots__ = ('_forras', '_hely')
    _JEL_ELOL = False

    def __init__(self, ertek, mezo, forras, hely, jel=''):
        _Nyers.__init__(self, ertek, mezo, jel)
        object.__setattr__(self, '_forras', forras)
        object.__setattr__(self, '_hely', hely)

    @property
    def forras(self):
        return self._forras

    @property
    def hely(self):
        return self._hely


class Belso(_Nyers):
    """Belső szabad szöveg (indoklás, megjegyzés, keresési napló): látható szöveg nem lehet belőle."""
    __slots__ = ()


class Kulcs(_Nyers):
    """Belső azonosító vagy állapotérték. Olvasói neve a névtáblából jön."""
    __slots__ = ()


class Utvonal(_Nyers):
    """Repó-relatív fájlútvonal: csak proveniencia lehet belőle."""
    __slots__ = ()


# ---------------------------------------------------------------------------
# Névtábla-elem
# ---------------------------------------------------------------------------


class Nev:
    """A névtábla egy sora: egy belső kulcs olvasói neve. Csak a névtábla betöltője hozza létre."""
    __slots__ = ('_tipus', '_kulcs', '_nev')

    def __init__(self, tipus, kulcs, olvasoi_nev):
        object.__setattr__(self, '_tipus', tipus)
        object.__setattr__(self, '_kulcs', kulcs)
        object.__setattr__(self, '_nev', olvasoi_nev)

    def __setattr__(self, nev, ertek):
        raise AttributeError('változtathatatlan')

    @property
    def tipus(self):
        return self._tipus

    @property
    def kulcs(self):
        return self._kulcs

    def __eq__(self, masik):
        return isinstance(masik, Nev) and (masik._tipus, masik._kulcs) == (self._tipus, self._kulcs)

    def __hash__(self):
        return hash((self._tipus, self._kulcs))

    def __repr__(self):
        return 'Nev(%r, %r)' % (self._tipus, self._kulcs)

    def __str__(self):
        raise SzovegHiba('a Nev nem alakítható közvetlenül szöveggé; sablonparaméterként add át')

    __format__ = None


# ---------------------------------------------------------------------------
# A látható szöveg
# ---------------------------------------------------------------------------


class Fajta(enum.Enum):
    PROZA = 'proza'
    SABLON = 'sablon'
    IDEZET = 'idezet'


_ENGEDELY = object()


class Lathato:
    """Látható szöveg: (fajta, szöveg) szegmensek változtathatatlan sora. Nem `str`."""
    __slots__ = ('_szegmensek',)

    def __init__(self, szegmensek, _engedely=None):
        if _engedely is not _ENGEDELY:
            raise SzovegHiba('Lathato csak a proza(), a sablon() vagy az idezet() konstruktorral készülhet')
        object.__setattr__(self, '_szegmensek', tuple(s for s in szegmensek if s[1]))

    def __setattr__(self, nev, ertek):
        raise AttributeError('változtathatatlan')

    def __eq__(self, masik):
        return isinstance(masik, Lathato) and masik._szegmensek == self._szegmensek

    def __hash__(self):
        return hash(self._szegmensek)

    def __bool__(self):
        return bool(self._szegmensek)

    def __repr__(self):
        return '<Lathato %d szegmens, %d karakter>' % (
            len(self._szegmensek), sum(len(s[1]) for s in self._szegmensek))

    def __str__(self):
        raise SzovegHiba('a Lathato nem alakítható közvetlenül szöveggé; a megjelenítő írja ki')

    __format__ = None


def proza(kezi):
    """A kézi forrás egy rése vagy prózamezője, változatlanul."""
    if not isinstance(kezi, Kezi):
        raise SzovegHiba('proza(): csak Kezi értékből készülhet, nem ebből: %s' % type(kezi).__name__)
    return Lathato(((Fajta.PROZA, kezi.szoveg),), _ENGEDELY)


def idezet(forrasszoveg):
    """Szó szerinti idézet a bemeneti rétegből; a forrást és a helyet az érték hordozza."""
    if not isinstance(forrasszoveg, Forrasszoveg):
        raise SzovegHiba('idezet(): csak Forrasszoveg értékből készülhet, nem ebből: %s'
                         % type(forrasszoveg).__name__)
    return Lathato(((Fajta.IDEZET, forrasszoveg.szoveg),), _ENGEDELY)


# --- sablon ----------------------------------------------------------------

_HELYORZO_RX = re.compile(r'\{([a-z][a-z0-9_]*)(?:\|([^{}]*))?\}')
_TIPUS_RX = re.compile(r'^(?P<nev>[a-z][a-z0-9_]*):(?P<tipus>[a-z]+)(?:\((?P<arg>[^()]*)\))?$')

_SKALAR_TIPUSOK = ('szam', 'tizedes', 'nev', 'igehely', 'strong', 'motivum', 'horgony', 'datum', 'lathato')
_MAGANHANGZO = 'aáeéiíoóöőuúüűAÁEÉIÍOÓÖŐUÚÜŰ'


def _nevelo(szoveg):
    """A határozott névelő alakja a következő szó előtt: „a” vagy „az”.

    A szó elején álló jelölést (idézőjel, zárójel, csillag) átlépi. Számnál a kiejtett alak dönt:
    „az” áll az 1 és az 5 előtt, valamint minden olyan szám előtt, amelynek kiejtése egy-, öt- vagy
    ezer-rel kezdődik (1, 5, 50–59, 500–599, 1000–1999, 5000–5999 és így tovább)."""
    mag = szoveg.lstrip('„"»«(*_[‹ ')
    if not mag:
        return 'a'
    if mag[0].isdigit():
        szam = re.match(r'\d+', mag).group(0)
        if szam[0] == '5':
            return 'az'
        if szam[0] == '1' and len(szam) % 3 == 1:
            return 'az'
        return 'a'
    return 'az' if mag[0] in _MAGANHANGZO else 'a'


def _tizedes(ertek, jegy):
    return ('%.*f' % (jegy, ertek)).replace('.', ',')


class SablonSor:
    """A sablontábla egy sora: kulcs, mondat helyőrzőkkel, a paraméterek kötött típusa."""
    __slots__ = ('kulcs', 'mondat', 'parameterek', 'szakasz', 'eredet', '_darabok')

    def __init__(self, kulcs, mondat, parameterek, szakasz='', eredet=''):
        self.kulcs = kulcs
        self.mondat = mondat
        self.szakasz = szakasz
        self.eredet = eredet
        self.parameterek = {}
        for resz in [p.strip() for p in parameterek.split(',')] if parameterek.strip() not in ('', '-') else []:
            m = _TIPUS_RX.match(resz)
            if not m:
                raise SablonHiba('%s: értelmezhetetlen paraméter-leírás: %r' % (kulcs, resz))
            tipus, arg = m.group('tipus'), m.group('arg') or ''
            if tipus == 'lista':
                if arg not in _SKALAR_TIPUSOK and not arg.startswith('nev:'):
                    raise SablonHiba('%s: ismeretlen listaelem-típus: %r' % (kulcs, arg))
            elif tipus not in _SKALAR_TIPUSOK:
                raise SablonHiba('%s: ismeretlen paramétertípus: %r' % (kulcs, tipus))
            if m.group('nev') in self.parameterek:
                raise SablonHiba('%s: kétszer leírt paraméter: %r' % (kulcs, m.group('nev')))
            self.parameterek[m.group('nev')] = (tipus, arg)
        darabok, veg = [], 0
        hasznalt = set()
        for m in _HELYORZO_RX.finditer(mondat):
            if m.start() > veg:
                darabok.append(('szoveg', mondat[veg:m.start()], None))
            if m.group(1) not in self.parameterek:
                raise SablonHiba('%s: a mondat le nem írt paramétert használ: %r' % (kulcs, m.group(1)))
            darabok.append(('helyorzo', m.group(1), m.group(2)))
            hasznalt.add(m.group(1))
            veg = m.end()
        if veg < len(mondat):
            darabok.append(('szoveg', mondat[veg:], None))
        if '{' in ''.join(d[1] for d in darabok if d[0] == 'szoveg'):
            raise SablonHiba('%s: értelmezhetetlen helyőrző a mondatban: %r' % (kulcs, mondat))
        fel_nem_hasznalt = set(self.parameterek) - hasznalt
        if fel_nem_hasznalt:
            raise SablonHiba('%s: leírt, de a mondatban nem használt paraméter: %s'
                             % (kulcs, ', '.join(sorted(fel_nem_hasznalt))))
        self._darabok = tuple(darabok)


def _skalar_szegmensek(kulcs, nev, tipus, arg, ertek, modosito):
    """Egy skalár paraméter szegmensei. A visszaadott lista (fajta, szöveg) párokból áll."""
    if tipus == 'lathato':
        if not isinstance(ertek, Lathato):
            raise SzovegHiba('%s: a(z) %s paraméter Lathato legyen, nem %s' % (kulcs, nev, type(ertek).__name__))
        return list(ertek._szegmensek)
    if tipus == 'szam':
        if isinstance(ertek, bool) or not isinstance(ertek, int):
            raise SzovegHiba('%s: a(z) %s paraméter egész szám legyen' % (kulcs, nev))
        szoveg = '%d' % ertek
    elif tipus == 'tizedes':
        if isinstance(ertek, bool) or not isinstance(ertek, (int, float)):
            raise SzovegHiba('%s: a(z) %s paraméter szám legyen' % (kulcs, nev))
        szoveg = _tizedes(ertek, int(arg or '2'))
    elif tipus == 'nev':
        if not isinstance(ertek, Nev) or (arg and ertek.tipus != arg):
            raise SzovegHiba('%s: a(z) %s paraméter %r típusú Nev legyen' % (kulcs, nev, arg))
        szoveg = ertek._nev
    elif tipus == 'igehely':
        if not isinstance(ertek, Igehely):
            raise SzovegHiba('%s: a(z) %s paraméter Igehely legyen' % (kulcs, nev))
        szoveg = ertek._ertek
    elif tipus == 'strong':
        if not isinstance(ertek, Strong):
            raise SzovegHiba('%s: a(z) %s paraméter Strong legyen' % (kulcs, nev))
        szoveg = ertek._ertek
    elif tipus == 'motivum':
        if not isinstance(ertek, MotivumId):
            raise SzovegHiba('%s: a(z) %s paraméter MotivumId legyen' % (kulcs, nev))
        szoveg = ertek._ertek
    elif tipus == 'horgony':
        if not isinstance(ertek, Horgony):
            raise SzovegHiba('%s: a(z) %s paraméter Horgony legyen' % (kulcs, nev))
        szoveg = ertek._ertek
    elif tipus == 'datum':
        if not isinstance(ertek, datetime.date) or isinstance(ertek, datetime.datetime):
            raise SzovegHiba('%s: a(z) %s paraméter dátum legyen' % (kulcs, nev))
        szoveg = ertek.isoformat()
    else:  # a SablonSor már ellenőrizte
        raise SablonHiba('%s: ismeretlen paramétertípus: %r' % (kulcs, tipus))
    return [(Fajta.SABLON, szoveg)]


_CELLA_NEVELO_RX = re.compile(r'^((?:\*\*|\*|\[)?)(a|az)\s+(?=\S)')
CELLA_MONDAT_SZO = 6   # ennyi szótól a cella mondat értékű: a névelő megmarad, nagy kezdőbetűvel


def _cellakezdet(szegmensek):
    """A `cella` módosító: tábla- és listaelem nem kezdődik kisbetűs névelővel. A rövid elem eleji „a”/„az”
    elmarad, és az elem nagy kezdőbetűt kap; a mondat értékű elem (legalább `CELLA_MONDAT_SZO` szó a névelő
    után) a névelőt megtartja, nagy kezdőbetűvel. Más elem változatlan."""
    teljes = ''.join(s[1] for s in szegmensek)
    m = _CELLA_NEVELO_RX.match(teljes)
    if not m:
        return szegmensek
    maradek = teljes[m.end():]
    if len(maradek.split()) >= CELLA_MONDAT_SZO:
        uj_eleje = m.group(1) + m.group(2).capitalize() + ' ' + maradek[:1]
    else:
        uj_eleje = m.group(1) + (maradek[:1].upper() if maradek[:1].isalpha() else maradek[:1])
    fogyo, ki = m.end() + 1, []
    for fajta, szoveg in szegmensek:
        if fogyo >= len(szoveg):
            fogyo -= len(szoveg)
            continue
        ki.append((fajta, szoveg[fogyo:]))
        fogyo = 0
    return [(szegmensek[0][0], uj_eleje)] + ki


def _nevelovel(kulcs, nev, szegmensek, modosito, masik_szoveg=None):
    """A skalár helyőrző módosítója: „a” / „A” névelőt tesz a kiírt érték elé (az `a:<másik>` alak a névelőt a
    megnevezett másik paraméter szövege szerint választja, pl. a kiejtés szerint); a `cella` a cellakezdő alak."""
    if modosito in (None, ''):
        return szegmensek
    if modosito == 'cella':
        return _cellakezdet(szegmensek)
    alak = modosito.partition(':')[0]
    if alak not in ('a', 'A'):
        raise SablonHiba('%s: ismeretlen módosító a(z) %s helyőrzőn: %r' % (kulcs, nev, modosito))
    nevelo = _nevelo(masik_szoveg if masik_szoveg is not None else ''.join(s[1] for s in szegmensek))
    if alak == 'A':
        nevelo = nevelo.capitalize()
    return [(Fajta.SABLON, nevelo + ' ')] + szegmensek


def sablon(sor, **parameterek):
    """A sablontábla egy sora, kötött típusú paraméterekkel. Nyers `str` paraméter nem adható át.

    Helyőrzők a mondatban: `{nev}`; skalárnál `{nev|a}` / `{nev|A}` névelőt tesz elé; listánál a
    `|` utáni szöveg az elválasztó (`{elemek|; }`), két elválasztóval az utolsó elem előtti külön
    adható (`{elemek|, | és }`)."""
    if not isinstance(sor, SablonSor):
        raise SzovegHiba('sablon(): az első argumentum SablonSor legyen (a sablontábla egy sora)')
    hianyzo = set(sor.parameterek) - set(parameterek)
    folos = set(parameterek) - set(sor.parameterek)
    if hianyzo or folos:
        raise SablonHiba('%s: hiányzó paraméter: %s; fölös paraméter: %s' % (
            sor.kulcs, ', '.join(sorted(hianyzo)) or '–', ', '.join(sorted(folos)) or '–'))
    szegmensek = []
    for fajta, tartalom, modosito in sor._darabok:
        if fajta == 'szoveg':
            szegmensek.append((Fajta.SABLON, tartalom))
            continue
        tipus, arg = sor.parameterek[tartalom]
        ertek = parameterek[tartalom]
        if isinstance(ertek, str):
            raise SzovegHiba('%s: a(z) %s paraméter nyers szöveg; csak kötött típusú érték adható át'
                             % (sor.kulcs, tartalom))
        if tipus == 'lista':
            if not isinstance(ertek, (tuple, list)):
                raise SzovegHiba('%s: a(z) %s paraméter lista legyen' % (sor.kulcs, tartalom))
            elem_tipus, _, elem_arg = arg.partition(':')
            elvalasztok = (modosito or '').split('|')
            koztes, utolso = elvalasztok[0], elvalasztok[-1]
            for i, elem in enumerate(ertek):
                if isinstance(elem, str):
                    raise SzovegHiba('%s: a(z) %s lista eleme nyers szöveg' % (sor.kulcs, tartalom))
                if i:
                    szegmensek.append((Fajta.SABLON, utolso if i == len(ertek) - 1 else koztes))
                szegmensek.extend(_skalar_szegmensek(sor.kulcs, tartalom, elem_tipus, elem_arg, elem, None))
        else:
            reszek = _skalar_szegmensek(sor.kulcs, tartalom, tipus, arg, ertek, modosito)
            masik_szoveg = None
            if modosito and ':' in modosito:
                masik = modosito.partition(':')[2]
                if masik not in sor.parameterek or sor.parameterek[masik][0] == 'lista':
                    raise SablonHiba('%s: a névelő alapja ismeretlen vagy lista: %r' % (sor.kulcs, masik))
                m_tipus, m_arg = sor.parameterek[masik]
                masik_szoveg = ''.join(s[1] for s in _skalar_szegmensek(sor.kulcs, masik, m_tipus, m_arg,
                                                                         parameterek[masik], None))
            szegmensek.extend(_nevelovel(sor.kulcs, tartalom, reszek, modosito, masik_szoveg))
    return Lathato(_osszevon(szegmensek), _ENGEDELY)


def _osszevon(szegmensek):
    """Az egymást követő azonos fajtájú szegmensek összevonása (a kiírt szöveg nem változik)."""
    ki = []
    for fajta, szoveg in szegmensek:
        if not szoveg:
            continue
        if ki and ki[-1][0] is fajta:
            ki[-1] = (fajta, ki[-1][1] + szoveg)
        else:
            ki.append((fajta, szoveg))
    return ki


class Kiirt:
    """A kiírt látható szöveg és a fajta-térképe: (kezdet, vég, fajta) tartományok a szövegben."""
    __slots__ = ('szoveg', 'tartomanyok')

    def __init__(self, szoveg, tartomanyok):
        self.szoveg = szoveg
        self.tartomanyok = tartomanyok


def kiiras(lathato):
    """A `Lathato` szöveggé alakítása. Csak a megjelenítő író modulja, a regresszió, a festékpróba és a
    kapuk hívhatják (statikus teszt őrzi)."""
    if not isinstance(lathato, Lathato):
        raise SzovegHiba('kiiras(): csak Lathato írható ki, nem ez: %s' % type(lathato).__name__)
    darabok, tartomanyok, hol = [], [], 0
    for fajta, szoveg in lathato._szegmensek:
        darabok.append(szoveg)
        tartomanyok.append((hol, hol + len(szoveg), fajta))
        hol += len(szoveg)
    return Kiirt(''.join(darabok), tuple(tartomanyok))


# ---------------------------------------------------------------------------
# Proveniencia
# ---------------------------------------------------------------------------

_PROV_HELYORZO = '{}'


class Proveniencia:
    """Proveniencia-szöveg: a megjelenítő csak HTML-megjegyzésbe és a Kolofonba írja."""
    __slots__ = ('_szoveg',)

    def __init__(self, szoveg, _engedely=None):
        if _engedely is not _ENGEDELY:
            raise SzovegHiba('Proveniencia csak a prov() konstruktorral készülhet')
        object.__setattr__(self, '_szoveg', szoveg)

    def __setattr__(self, nev, ertek):
        raise AttributeError('változtathatatlan')

    def __eq__(self, masik):
        return isinstance(masik, Proveniencia) and masik._szoveg == self._szoveg

    def __hash__(self):
        return hash(('prov', self._szoveg))

    def __bool__(self):
        return bool(self._szoveg)

    def __repr__(self):
        return '<Proveniencia %d karakter>' % len(self._szoveg)

    def __str__(self):
        raise SzovegHiba('a Proveniencia nem alakítható közvetlenül szöveggé; a megjelenítő írja megjegyzésbe')

    __format__ = None


def _prov_resz(ertek):
    if isinstance(ertek, Proveniencia):
        return ertek._szoveg
    if isinstance(ertek, _Nyers):
        return ertek.szoveg
    if isinstance(ertek, _Azonosito):
        return ertek._ertek
    if isinstance(ertek, Nev):
        return ertek._nev
    if isinstance(ertek, Lathato):
        return ''.join(s[1] for s in ertek._szegmensek)
    if isinstance(ertek, enum.Enum):
        return '%s' % (ertek.value,)
    if isinstance(ertek, bool):
        raise SzovegHiba('prov(): logikai érték nem írható ki')
    if isinstance(ertek, (int, float)):
        return '%s' % (ertek,)
    if isinstance(ertek, datetime.date):
        return ertek.isoformat()
    if isinstance(ertek, str):
        return ertek
    raise SzovegHiba('prov(): nem kiírható típus: %s' % type(ertek).__name__)


def prov(minta, *ertekek):
    """Proveniencia-szöveg a `minta` szerint; a `{}` helyőrzők sorban az értékeket kapják."""
    reszek = minta.split(_PROV_HELYORZO)
    if len(reszek) - 1 != len(ertekek):
        raise SzovegHiba('prov(): %d helyőrző, %d érték' % (len(reszek) - 1, len(ertekek)))
    ki = [reszek[0]]
    for ertek, utana in zip(ertekek, reszek[1:]):
        ki.append(_prov_resz(ertek))
        ki.append(utana)
    return Proveniencia(''.join(ki), _ENGEDELY)


def prov_fuz(elvalaszto, elemek):
    """Proveniencia-elemek összefűzése egy elválasztóval."""
    return Proveniencia(elvalaszto.join(_prov_resz(e) for e in elemek), _ENGEDELY)


def prov_szoveg(proveniencia):
    """A proveniencia szövege. Csak a megjelenítő író modulja hívhatja (megjegyzés, Kolofon)."""
    if not isinstance(proveniencia, Proveniencia):
        raise SzovegHiba('prov_szoveg(): csak Proveniencia írható ki')
    return proveniencia._szoveg
