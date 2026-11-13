"""lapgen.bemenet.szavak — a héber és a görög szöveg szavai a kiejtésükkel: egy kiejtés-szolgáltatás.

Bemenetek: B08 (a héber szöveg szavai, TAHOT), B09 (a görög szöveg szavai, TAGNT), B12 (a kiejtés szabály- és
kivételtáblája), B13 (a héber gépi kiejtés szabálya: kódmodul, nem fájl), B54 (a Károli–Strong párosítás
könyvenként). A kiejtés minden lapon ezen az egy úton jön (GK-13).

Ismétlődés (GK-14, T4): ha egy Strong-szám többször áll egy versben, az az előfordulás számít, amelyhez a sor
Károli-szava a párosításban (B54) kötődik; párosítás híján az **első** előfordulás, a vers szövegrendje szerint.

A szótári alak (lemma) és kiejtése is innen jön (B10): görögül a szótár átírásának magyaros alakja, héberül a
jóváhagyott kivétel-sor, híján a pontozott lemma gépi kiejtése; ha az sincs, a kiejtés kimondva hiányzik.
"""
import re
import unicodedata

import heber_kiejtes
import kiejtes as kiejtes_modul

from lapgen.bemenet.jegyzek import BemenetHiba

_ZARO_IRASJEL_RX = re.compile(r'[,.;·]+$')
_TAHOT_OSZLOPOK = ('Igehely', 'Strong-szám', 'Ragozott alak', 'Kiejtés')
_HEBER_ELOTAG = 'H'
_PAR_OSZLOPOK = ('vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong')
_SZO_RX = re.compile(r'\w+')
_VERS_KONYV_RX = re.compile(r'^(\S+) \d+:\d+$')
_STRONG_TOKEN_RX = re.compile(r'^[HG]\d{4}[A-Za-z]?$')
_ALAP_STRONG_RX = re.compile(r'^([HG]\d{4})[a-zA-Z]?$')
_LEMMA_OSZLOP, _ATIRAS_OSZLOP = 3, 4
_LEMMA_VALASZTO = ','
_SZOTO_OSZLOP = 'Szótő'
_KANTILLACIO_ELSO, _KANTILLACIO_UTOLSO, _METEG = '\u0591', '\u05af', '\u05bd'


def _heber_kulcs(szo):
    """A héber szó összevetési kulcsa: a kantillációs jelek és a meteg nélkül (a pontozás marad)."""
    return unicodedata.normalize('NFC', ''.join(
        c for c in szo if not (_KANTILLACIO_ELSO <= c <= _KANTILLACIO_UTOLSO or c == _METEG)))


class Szo:
    """Egy szó a versben: a ragozott alak és a kiejtése, idézhető forrásszövegként."""
    __slots__ = ('strong', 'alak', 'kiejtes')

    def __init__(self, strong, alak, kiejtes):
        self.strong, self.alak, self.kiejtes = strong, alak, kiejtes


class _Szoveg:
    """Egy szövegkiadás szavai versenként, a fájl sorrendjében: {igehely: [(Strong, alak, átírás, szótő)]}."""

    def __init__(self, versenkent):
        self._versenkent = versenkent

    def sorok(self, vers_kod):
        return self._versenkent.get(vers_kod, ())

    def token_szam(self, vers_kod, strong_kod):
        return sum(1 for s in self._versenkent.get(vers_kod, ()) if s[0] == strong_kod)

    def tovek(self, versek, strong_kod):
        """A szó szótövei a megadott versekben (összevetési kulcsként)."""
        return {_heber_kulcs(s[3]) for vers in versek for s in self._versenkent.get(vers, ())
                if s[0] == strong_kod and s[3]}


def _szoveg_betolt(b, b_id):
    tabla = b._tabla(b_id, oszlopok=_TAHOT_OSZLOPOK)
    i, s, a, k = (tabla.oszlop(o) for o in _TAHOT_OSZLOPOK)
    t = tabla.oszlop(_SZOTO_OSZLOP) if tabla.van(_SZOTO_OSZLOP) else None
    versenkent = {}
    for sor in tabla.sorok:
        versenkent.setdefault(sor[i], []).append((sor[s], sor[a], sor[k], sor[t] if t is not None else ''))
    return _Szoveg(versenkent)


def b08_tahot(b):
    """B08 — a héber szöveg szavai versenként (a kulcs a Károli-vers; az összevont verseknél a közös kulcson
    mindkét héber vers szavai állnak)."""
    return b.egyszer('B08', lambda: _szoveg_betolt(b, 'B08'))


def b09_tagnt(b):
    """B09 — a görög szöveg szavai versenként."""
    return b.egyszer('B09', lambda: _szoveg_betolt(b, 'B09'))


def b12_kiejtes_tablak(b):
    """B12 — a magyaros kiejtés szabálytáblája és kivételtáblája: (görög szabályok, görög kivételek, héber
    kivételek)."""
    def betolt():
        szabaly_ut, kivetel_ut = b._utvonalak('B12')
        szabalyok = b._tabla('B12', utvonal=szabaly_ut, oszlopok=('sorszam', 'minta', 'csere'))
        kivetelek = b._tabla('B12', utvonal=kivetel_ut, oszlopok=('nyelv', 'alak', 'kiejtes'))
        rendezett = sorted(szabalyok.szotarak(), key=lambda r: int(r['sorszam']))
        return ([(r['minta'], r['csere']) for r in rendezett],
                {r['alak']: r['kiejtes'] for r in kivetelek.szotarak() if r['nyelv'] == 'gorog'},
                {r['alak']: r['kiejtes'] for r in kivetelek.szotarak() if r['nyelv'] == 'heber'})
    return b.egyszer('B12', betolt)


class Parositas:
    """A Károli–Strong párosítás (B54): a Károli-szó tokenjeihez kötött eredeti szavak versenként. A könyv fájlja
    az első kérdéskor töltődik be; a nem párosított könyv (nincs fájlja) kimondott hiány: üres válasz."""

    def __init__(self, b, konyv_utvonal):
        self._b, self._konyv_utvonal, self._konyvek = b, konyv_utvonal, {}

    def _konyv(self, konyv):
        if konyv not in self._konyvek:
            index = {}
            utvonal = self._konyv_utvonal.get(konyv)
            if utvonal is not None:
                tabla = self._b._tabla('B54', utvonal=utvonal, oszlopok=_PAR_OSZLOPOK)
                v, hn, hu, er, szo, st = (tabla.oszlop(o) for o in _PAR_OSZLOPOK)
                for sor in tabla.sorok:
                    if sor[er].isdigit() and sor[hn].isdigit():
                        index.setdefault(sor[v], []).append(
                            (int(sor[hn]), ''.join(_SZO_RX.findall(sor[hu].casefold())), int(sor[er]), sor[szo],
                             sor[st]))
            self._konyvek[konyv] = index
        return self._konyvek[konyv]

    def kotott(self, vers_kod, strong_kod, karoli_szo):
        """A Károli-szó tokenjeihez kötött eredeti szavak a versben: [(sorszám a versben, 1-től; az eredeti
        alak)], a sorszám rendjében. Üres, ha a szóhoz nincs pár.

        Ha a Károli-szó egyik szava többször áll a versben („nevét … az Úrnak nevét”), az a pár számít, amelynek
        a szomszédos szavai a Károli-szó többi szavával egyeznek (a Károli-szó összefüggő szókapcsolatként áll a
        versben); ha ilyen nincs, a szó minden párja."""
        m = _VERS_KONYV_RX.match(vers_kod)
        if not m:
            return []
        tokenek = _SZO_RX.findall(karoli_szo.casefold())
        sorok = self._konyv(m.group(1)).get(vers_kod, ())
        vers_szavai = {hn: hu for hn, hu, _n, _alak, _st in sorok}
        jeloltek = [(hn, hu, n, alak) for hn, hu, n, alak, st in sorok if st == strong_kod and hu in tokenek]

        def osszefuggo(hn, hu):
            return any(all(vers_szavai.get(hn - j + i, t) == t for i, t in enumerate(tokenek))
                       for j, token in enumerate(tokenek) if token == hu)

        szukitett = [j for j in jeloltek if osszefuggo(j[0], j[1])]
        return sorted({(n, alak) for _hn, _hu, n, alak in (szukitett or jeloltek)})


def b54_karoli_parok(b):
    """B54 — a Károli–Strong párosítás könyvenként (modell-kimenet, javaslat; minden pár használható, szűrő
    nélkül). A könyvet a fájl első adatsora nevezi meg, így a kódban fájlnév-képzés és könyvnév-alias nem áll."""
    def betolt():
        konyv_utvonal = {}
        for utvonal in b._utvonalak('B54'):
            for sor in b._fejsorok('B54', utvonal, 8):
                m = _VERS_KONYV_RX.match(sor.split('\t')[0]) if not sor.startswith('#') else None
                if m:
                    konyv_utvonal.setdefault(m.group(1), utvonal)
                    break
        return Parositas(b, konyv_utvonal)
    return b.egyszer('B54', betolt)


_ROVID_OSZLOP = 6
_ALAP_HOSSZ = 5


def b10_lemmak(b):
    """B10 — a szavak szótári alakja és átírása a két rövid szótárból (görög, héber): (pontos, alap, rövid). A
    `pontos` a szótár saját Strong-kulcsa (az első sor számít); az `alap` a betűutótag nélküli Strong-számra esik
    vissza (a szótár egy részt jelentésenként bont: `H2416a`, `H2416b`); a `rövid` a szótár egyszavas angol jelentése
    a betűutótag nélküli Strong-számra (csak a magyar rövid jelentés hiányának kimondásához: „fordításra vár”)."""
    def betolt():
        pontos, alap, rovid = {}, {}, {}
        for utvonal in b._utvonalak('B10'):
            for sor in b._szoveg('B10', utvonal=utvonal).split('\n'):
                mezok = sor.split('\t')
                if len(mezok) <= _ATIRAS_OSZLOP or not _STRONG_TOKEN_RX.match(mezok[0]):
                    continue
                ertek = (mezok[_LEMMA_OSZLOP], mezok[_ATIRAS_OSZLOP])
                pontos.setdefault(mezok[0], ertek)
                m = _ALAP_STRONG_RX.match(mezok[0])
                if m:
                    alap.setdefault(m.group(1), ertek)
                if len(mezok) > _ROVID_OSZLOP and mezok[_ROVID_OSZLOP].strip():
                    rovid.setdefault(mezok[0][:_ALAP_HOSSZ], mezok[_ROVID_OSZLOP].strip())
        return pontos, alap, rovid
    return b.egyszer('B10', betolt)


def b13_heber_gepi(b):
    """B13 — a pontozott héber alak gépi kiejtése (szabálymodul, nem adatfájl). A visszaadott függvény:
    (teljes alak, előtag betűszáma, makkef) → kiejtés, pontozatlan alakra üres."""
    b._naploz_modul('B13')
    return heber_kiejtes.kiejt


class Kiejtes:
    """A kiejtés-szolgáltatás: egy vers egy szavának ragozott alakja és kiejtése."""

    def __init__(self, b):
        self._b = b
        self._tahot = b08_tahot(b)
        self._tagnt = b09_tagnt(b)
        self._szabalyok, self._gorog_kivetelek, self._heber_kivetelek = b12_kiejtes_tablak(b)
        self._heber_gepi = b13_heber_gepi(b)
        self._parok = b54_karoli_parok(b)

    def token_szam(self, vers, strong):
        """Hányszor áll a héber Strong-szám a versben."""
        return self._tahot.token_szam(vers.kod, strong.kod)

    def _kotott_hely(self, sorok, vers, strong, karoli_szo):
        """A Károli-szóhoz a párosításban kötött előfordulás helye a vers sorai között; None, ha nincs ilyen.
        A pár sorszáma akkor érvényes, ha azon a helyen ez a Strong-szám és a pár eredeti alakja áll."""
        if karoli_szo is None:
            return None
        for n, alak in self._parok.kotott(vers.kod, strong.kod, karoli_szo.ertek):
            if 0 < n <= len(sorok) and sorok[n - 1][0] == strong.kod and sorok[n - 1][1] == alak:
                return n - 1
        return None

    def ragozott(self, versek, strong, karoli_szo=None):
        """A szó alakja és kiejtése a megadott verseken (T4): az az előfordulás, amelyhez a `karoli_szo` a
        párosításban kötődik (a versek rendjében az első ilyen); párosítás híján az első előfordulás az első
        olyan versben, amelyben a szó áll. None, ha a szó egyik versben sem áll."""
        heber = strong.kod.startswith(_HEBER_ELOTAG)
        szoveg = self._tahot if heber else self._tagnt
        valasztott = None
        for vers in versek:
            sorok = szoveg.sorok(vers.kod)
            kotott = self._kotott_hely(sorok, vers, strong, karoli_szo)
            if kotott is not None:
                valasztott = (vers, kotott)
                break
            helyek = [k for k, s in enumerate(sorok) if s[0] == strong.kod]
            if helyek and valasztott is None:
                valasztott = (vers, helyek[0])
        for vers, i in ((valasztott,) if valasztott is not None else ()):
            sorok = szoveg.sorok(vers.kod)
            if not heber:
                alak = _ZARO_IRASJEL_RX.sub('', sorok[i][1])
                kiejtes = kiejtes_modul.atir(sorok[i][2], self._szabalyok, self._gorog_kivetelek)
                return Szo(strong, self._b.forrasszoveg('B09', 'ragozott_alak', alak, vers),
                           self._b.forrasszoveg('B12', 'kiejtes', kiejtes, vers) if kiejtes else None)
            szotarak = [{'Strong-szám': s[0], 'Ragozott alak': s[1], 'Kiejtés': s[2]} for s in sorok]
            teljes, elotag, makkef = heber_kiejtes.teljes_szo(szotarak, i)
            gepi = self._heber_gepi(teljes, elotag, makkef)
            if not gepi:
                raise BemenetHiba('B13: a(z) %s %s pontozatlan alak; a szótári alak kiejtése (B10) a 4. szakasz '
                                  'szeletével készül el' % (vers.kod, strong.kod))
            return Szo(strong, self._b.forrasszoveg('B08', 'ragozott_alak', _ZARO_IRASJEL_RX.sub('', teljes), vers),
                       self._b.forrasszoveg('B13', 'kiejtes', gepi, vers))
        return None


    def _valtozat(self, strong, versek, pontos):
        """A betű nélküli héber Strong-szám szótári változata (`H2403a` / `H2403b`), amely a megadott versekben
        ténylegesen áll: a versek szótöve a változatok lemmájával összevetve. Pontosan egy egyező változatnál annak
        a sora; különben None (az alapalak áll)."""
        valtozatok = sorted(k for k in pontos if len(k) == len(strong.kod) + 1 and k.startswith(strong.kod)
                            and k[-1].isalpha())
        if len(valtozatok) < 2 or not versek:
            return None
        tovek = self._tahot.tovek([v.kod for v in versek], strong.kod)
        talalt = [k for k in valtozatok
                  if any(_heber_kulcs(x.strip()) in tovek for x in pontos[k][0].split(_LEMMA_VALASZTO))]
        return pontos[talalt[0]] if len(talalt) == 1 else None

    def szotari(self, strong, versek=()):
        """A szó szótári alakja (lemma) és kiejtése; None, ha a szótárban nincs ilyen szó. A kiejtés None, ha
        sem jóváhagyott, sem gépi kiejtés nincs (pontozatlan héber lemma): kimondott hiány. A `versek` a motívum
        versei: ha a szótár a szót több változatban adja, az áll, amelyik ezekben a versekben szerepel (GK-13)."""
        pontos, alap, _rovid = b10_lemmak(self._b)
        nyers = (self._valtozat(strong, versek, pontos) if strong.kod.startswith(_HEBER_ELOTAG) else None) \
            or pontos.get(strong.kod) or alap.get(strong.kod)
        if not nyers:
            return None
        lemma, atiras = nyers
        if not strong.kod.startswith(_HEBER_ELOTAG):
            forras, szoveg = 'B12', kiejtes_modul.atir(atiras, self._szabalyok, self._gorog_kivetelek)
        else:
            forras = 'B12'
            szoveg = (self._heber_kivetelek.get(unicodedata.normalize('NFC', lemma))
                      or self._heber_kivetelek.get(atiras))
            if not szoveg:
                forras, szoveg = 'B13', self._heber_gepi(lemma.split(_LEMMA_VALASZTO)[0].strip(), 0, False)
        return Szo(strong, self._b.forrasszoveg('B10', 'lemma', lemma, strong),
                   self._b.forrasszoveg(forras, 'kiejtes', szoveg, strong) if szoveg else None)


def kiejtes(b):
    """A kiejtés-szolgáltatás a munkamenethez."""
    return b.egyszer('kiejtes', lambda: Kiejtes(b))
