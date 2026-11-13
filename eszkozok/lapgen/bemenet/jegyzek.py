"""lapgen.bemenet.jegyzek — a bemeneti réteg magja: jegyzék, fájlolvasás, olvasási napló, festés.

Ez az egyetlen modul, amely fájlt nyit olvasásra. Az útvonalak a jegyzéktáblából jönnek
(`JEGYZEK_UTVONAL`); a kódban más adat-útvonal nem áll (GK-01). Minden olvasás a naplóba kerül
(B-azonosító, útvonal, hash): ebből jön a blokkfejlécek, az Irodalom és a Kolofon forráslistája
(GK-07) és a regresszió bemenet-hash őre. Naplózás nélküli olvasás nincs: a jegyzéktábla saját olvasása is a
naplóba kerül (a jegyzék egy sora magára a jegyzékre mutat).

A hash a sorvég-normalizált tartalomból számolódik (`\\r\\n` → `\\n`), így Windowson és a CI-n egyezik.
"""
import contextlib
import glob as _glob
import hashlib
import os

from lapgen.szoveg import (FESTEK_ELOTAG, FESTEK_UTOTAG, Belso, Forrasszoveg, Kezi, Kulcs, Utvonal)

JEGYZEK_UTVONAL = 'adat/lapgen_bemenetek.tsv'
JEGYZEK_OSZLOPOK = ('id', 'utvonal', 'leiras', 'kotelezo', 'javitas', 'frissesseg', 'allapot',
                    'licenc_kulcs', 'olvasoi_nev_kulcs', 'forras')
ALLAPOTOK = ('aktiv', 'kivezetve', 'nem_vizsgalt', 'reszleges')
ID_HELYORZO = '<ID>'
NEM_FAJL = '-'


class BemenetHiba(Exception):
    """BUKÁS: hiányzó kötelező bemenet, hibás fejléc, elavult pillanatkép. A lap nem íródik ki."""


class Tabla:
    """Egy beolvasott TSV: fejléc és sorok, változtathatatlanul. A mezőt oszlopnév szerint adja."""
    __slots__ = ('fejlec', 'sorok', '_idx')

    def __init__(self, fejlec, sorok):
        self.fejlec = tuple(fejlec)
        self.sorok = tuple(sorok)
        self._idx = {nev: i for i, nev in enumerate(self.fejlec)}

    def oszlop(self, nev):
        return self._idx[nev]

    def van(self, nev):
        return nev in self._idx

    def szotarak(self):
        """A sorok szótárként (oszlopnév → érték); kis táblákhoz."""
        return tuple(dict(zip(self.fejlec, sor)) for sor in self.sorok)


class JegyzekSor:
    __slots__ = JEGYZEK_OSZLOPOK

    def __init__(self, **mezok):
        for nev in JEGYZEK_OSZLOPOK:
            setattr(self, nev, mezok[nev])


class Olvasas:
    """Az olvasási napló egy sora."""
    __slots__ = ('b_id', 'utvonal', 'sha256')

    def __init__(self, b_id, utvonal, sha256):
        self.b_id, self.utvonal, self.sha256 = b_id, utvonal, sha256


class Festo:
    """A festékpróba jelzőszavai. Mezőnként egy jelzőszó; a kategória visszakereshető."""

    def __init__(self):
        self.kategoriak = {}

    def jel(self, kategoria, mezo):
        jel = FESTEK_ELOTAG + mezo + FESTEK_UTOTAG
        elozo = self.kategoriak.setdefault(jel, kategoria)
        if elozo != kategoria:
            raise BemenetHiba('a(z) %s mező két kategóriában áll: %s és %s' % (mezo, elozo, kategoria))
        return jel


_FELDOLGOZOTT = {}   # tartalom-hash → Tabla; a gyorsítótár a fájl hash-ére kulcsolt, ezért állapotfüggetlen


def _tsv_ertelmez(szoveg, utvonal):
    sorok = szoveg.split('\n')
    if sorok and sorok[-1] == '':
        sorok.pop()
    i = 0
    while i < len(sorok) and sorok[i].startswith('#'):
        i += 1
    if i >= len(sorok):
        raise BemenetHiba('%s: nincs fejlécsor' % utvonal)
    fejlec = sorok[i].split('\t')
    szel = len(fejlec)
    ki = []
    for n, sor in enumerate(sorok[i + 1:], start=i + 2):
        if sor == '':
            continue
        mezok = sor.split('\t')
        if len(mezok) > szel:
            raise BemenetHiba('%s:%d: %d mező a %d oszlopos fejléc alatt' % (utvonal, n, len(mezok), szel))
        if len(mezok) < szel:
            mezok = mezok + [''] * (szel - len(mezok))
        ki.append(tuple(mezok))
    return Tabla(fejlec, ki)


def b68_jegyzek(b):
    """B68 — a bemenetek jegyzéke (maga a jegyzéktábla): a munkamenet megnyitásakor olvasódik, és az olvasása a
    naplóba kerül. Visszaadja a jegyzék azonosítóit."""
    b.jegyzek_sor('B68')
    return b.jegyzek_azonositok()


class Bemenet:
    """Egy generálás bemeneti munkamenete: a jegyzék, a fájlok tartalma, az olvasási napló.

    A `_` kezdetű metódusok a nyers hozzáférés; csak a `bemenet/` moduljai hívják (GK-02)."""

    def __init__(self, gyoker, festek=False):
        self.gyoker = os.path.abspath(gyoker)
        self._festo = Festo() if festek else None
        self._naplo = []
        self._naplozott = set()
        self._figyelok = []
        self._naplo_sorrend = []
        self._epitett = {}
        self._tar = {}
        self._jegyzek = self._jegyzek_betolt()

    # --- jegyzék -------------------------------------------------------------

    def _jegyzek_betolt(self):
        tartalom, sha = self._fajl(JEGYZEK_UTVONAL)
        tabla = _tsv_ertelmez(tartalom, JEGYZEK_UTVONAL)
        if tabla.fejlec != JEGYZEK_OSZLOPOK:
            raise BemenetHiba('%s: a fejléc eltér a várt oszlopoktól: %r' % (JEGYZEK_UTVONAL, tabla.fejlec))
        jegyzek = {}
        for sor in tabla.szotarak():
            if sor['id'] in jegyzek:
                raise BemenetHiba('%s: ismétlődő azonosító: %s' % (JEGYZEK_UTVONAL, sor['id']))
            if sor['kotelezo'] not in ('igen', 'nem'):
                raise BemenetHiba('%s: %s: a kotelezo értéke igen/nem lehet' % (JEGYZEK_UTVONAL, sor['id']))
            if sor['allapot'] not in ALLAPOTOK:
                raise BemenetHiba('%s: %s: ismeretlen állapot: %r' % (JEGYZEK_UTVONAL, sor['id'], sor['allapot']))
            jegyzek[sor['id']] = JegyzekSor(**sor)
        sajat = [a for a, sor in jegyzek.items() if sor.utvonal.strip() == JEGYZEK_UTVONAL]
        if len(sajat) != 1:
            raise BemenetHiba('%s: a jegyzék pontosan egy sora mutasson magára a jegyzékre (az olvasása így kerül '
                              'a naplóba); most %d ilyen sor van' % (JEGYZEK_UTVONAL, len(sajat)))
        self._naploz(sajat[0], JEGYZEK_UTVONAL, sha)
        return jegyzek

    def jegyzek_sor(self, b_id):
        try:
            return self._jegyzek[b_id]
        except KeyError:
            raise BemenetHiba('ismeretlen bemenet-azonosító: %s (nincs sora a jegyzékben)' % b_id) from None

    def jegyzek_azonositok(self):
        return tuple(sorted(self._jegyzek))

    # --- nyers olvasás -------------------------------------------------------

    def _fajl(self, utvonal):
        """Egy repó-relatív fájl sorvég-normalizált szövege és hash-e. BemenetHiba, ha nincs."""
        if utvonal in self._tar:
            return self._tar[utvonal]
        teljes = os.path.join(self.gyoker, *utvonal.split('/'))
        try:
            with open(teljes, 'rb') as f:
                bajtok = f.read()
        except FileNotFoundError:
            raise BemenetHiba('hiányzó bemeneti fájl: %s' % utvonal) from None
        bajtok = bajtok.replace(b'\r\n', b'\n')
        sha = hashlib.sha256(bajtok).hexdigest()
        self._tar[utvonal] = (bajtok.decode('utf-8'), sha)
        return self._tar[utvonal]

    def _fejsorok(self, b_id, utvonal, darab):
        """Egy bemeneti fájl első sorai (annak megállapítására, mit tartalmaz a fájl: pl. melyik könyv
        párosítását). Ez is olvasás: a fájl hash-ével a naplóba kerül, így a regresszió bemenet-hash őre méri."""
        tartalom, sha = self._fajl(utvonal)
        self._naploz(b_id, utvonal, sha)
        return tartalom.split('\n', darab)[:darab]

    def _utvonalak(self, b_id, motivum=None):
        """A bemenet útvonalai a jegyzékből: `;`-vel több útvonal adható, a `*` glob, az `<ID>` a motívum."""
        sor = self.jegyzek_sor(b_id)
        ki = []
        for minta in [u.strip() for u in sor.utvonal.split(';')]:
            if ID_HELYORZO in minta:
                if motivum is None:
                    raise BemenetHiba('%s: az útvonal motívumot vár (%s)' % (b_id, minta))
                minta = minta.replace(ID_HELYORZO, motivum.kod)
            if '*' in minta:
                talalat = sorted(_glob.glob(os.path.join(self.gyoker, *minta.split('/'))))
                ki.extend(os.path.relpath(t, self.gyoker).replace(os.sep, '/') for t in talalat)
            else:
                ki.append(minta)
        return ki

    def _naploz(self, b_id, utvonal, sha):
        self._naplo_sorrend.append(b_id)
        if (b_id, utvonal) not in self._naplozott:
            self._naplozott.add((b_id, utvonal))
            self._naplo.append(Olvasas(b_id, utvonal, sha))
        for figyelo in self._figyelok:
            figyelo.add(b_id)

    def _teljes_utvonal(self, utvonal):
        """A repó-relatív útvonal abszolút alakja (a közös javító modulok útvonal-paraméteréhez)."""
        return os.path.join(self.gyoker, *utvonal.split('/'))

    def jegyzek_utvonal(self, b_id, sorszam=0):
        """A bemenet jegyzékbeli útvonala proveniencia-értékként (több útvonalnál a `sorszam`-adik)."""
        return self.utvonal_ertek(b_id, [u.strip() for u in self.jegyzek_sor(b_id).utvonal.split(';')][sorszam])

    def _naploz_modul(self, b_id):
        """Nem fájl-bemenet (szabálymodul) olvasásának naplózása; a jegyzékben az útvonala `-`."""
        if self.jegyzek_sor(b_id).utvonal.strip() != NEM_FAJL:
            raise BemenetHiba('%s: a jegyzék szerint fájl-bemenet, nem modul' % b_id)
        self._naploz(b_id, NEM_FAJL, '')

    def egyszer(self, kulcs, epito):
        """Munkameneten belüli gyorsítótár a beolvasott táblákból épített indexekhez: az `epito` egyszer fut.
        (A napló a figyelőknek minden híváskor jelez: l. `ujra_jelez`.)"""
        if kulcs not in self._epitett:
            elotte = len(self._naplo_sorrend)
            ertek = epito()
            self._epitett[kulcs] = (ertek, tuple(self._naplo_sorrend[elotte:]))
            return ertek
        ertek, olvasott = self._epitett[kulcs]
        for figyelo in self._figyelok:
            figyelo.update(olvasott)
        return ertek

    def _van(self, b_id, motivum=None):
        """Létezik-e a bemenet minden fájlja (opcionális bemenet hiányának megállapítására)."""
        utvonalak = self._utvonalak(b_id, motivum)
        return bool(utvonalak) and all(
            os.path.isfile(os.path.join(self.gyoker, *u.split('/'))) for u in utvonalak)

    def _szoveg(self, b_id, motivum=None, utvonal=None):
        """Egy bemeneti szövegfájl tartalma. Kötelező bemenet hiánya BemenetHiba."""
        utvonal = utvonal or self._egy_utvonal(b_id, motivum)
        tartalom, sha = self._fajl(utvonal)
        self._naploz(b_id, utvonal, sha)
        return tartalom

    def _egy_utvonal(self, b_id, motivum=None):
        utvonalak = self._utvonalak(b_id, motivum)
        if len(utvonalak) != 1:
            raise BemenetHiba('%s: egy útvonalat vártam, %d van' % (b_id, len(utvonalak)))
        return utvonalak[0]

    def _tabla(self, b_id, motivum=None, utvonal=None, oszlopok=()):
        """Egy bemeneti TSV. Az `oszlopok` a kötelező oszlopnevek: hiányuk BemenetHiba (fejléckapu)."""
        utvonal = utvonal or self._egy_utvonal(b_id, motivum)
        tartalom, sha = self._fajl(utvonal)
        self._naploz(b_id, utvonal, sha)
        tabla = _FELDOLGOZOTT.get(sha)
        if tabla is None:
            tabla = _FELDOLGOZOTT[sha] = _tsv_ertelmez(tartalom, utvonal)
        hianyzo = [o for o in oszlopok if not tabla.van(o)]
        if hianyzo:
            raise BemenetHiba('%s (%s): hiányzó oszlop: %s' % (b_id, utvonal, ', '.join(hianyzo)))
        return tabla

    # --- olvasási napló ------------------------------------------------------

    @contextlib.contextmanager
    def figyel(self):
        """A blokkon belül olvasott bemenetek B-azonosítóinak gyűjtése (a szakasz forráslistájához)."""
        gyujto = set()
        self._figyelok.append(gyujto)
        try:
            yield gyujto
        finally:
            self._figyelok.remove(gyujto)

    def olvasasi_naplo(self):
        return tuple(self._naplo)

    # --- burkolók (festéssel) ------------------------------------------------

    @property
    def festo(self):
        return self._festo

    def _jel(self, kategoria, b_id, mezo):
        if self._festo is None:
            return ''
        return self._festo.jel(kategoria, '%s_%s' % (b_id, mezo))

    def kezi(self, b_id, mezo, ertek):
        return Kezi(ertek, mezo, self._jel('kezi', b_id, mezo))

    def forrasszoveg(self, b_id, mezo, ertek, hely):
        return Forrasszoveg(ertek, mezo, b_id, hely, self._jel('idezet', b_id, mezo))

    def belso(self, b_id, mezo, ertek):
        return Belso(ertek, mezo, self._jel('belso', b_id, mezo))

    def kulcs(self, b_id, mezo, ertek):
        return Kulcs(ertek, mezo, self._jel('belso', b_id, mezo))

    def utvonal_ertek(self, b_id, utvonal):
        return Utvonal(utvonal, 'utvonal', self._jel('belso', b_id, 'utvonal'))
