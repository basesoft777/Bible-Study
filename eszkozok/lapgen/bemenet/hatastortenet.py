"""lapgen.bemenet.hatastortenet — a „9. Hatástörténet” szakasz bemenetei (S7).

Bemenetek: B38 (a visszhang-tábla ókori fordítás-sorai: Targum, Vulgata, LXX), B39 (a tanúk táblája), B41 (a görög
szöveg változatjegyzéke, STEPBible TAGNT), B74 (az SBL Greek New Testament apparátusa), B64 (a Targum szövege: mely
könyveket fedi), B73 (a szír fordítás, Peshitta: a forrás állapota), B08 (a héber szöveg angol tükörfordítása: a
láncbeli jelentés szűrője), B35 (a Septuaginta szavainak lemmája), B36 (a héber szavak versszintű görög társai).

A forrás állapota (GK-28, T7): a Targum- és a Peshitta-mondat a jegyzék `allapot` mezőjéből és az adat tényleges
állapotából jön; ha a kettő ellentmond (a jegyzék „nem vizsgált”-at mond, de a forrás megvan; „aktív”-at, de hiányzik;
„részleges”-t, de a forrás minden könyvet fed), BUKÁS. A régi generátor a Targum lefedettségét kódba írt könyvlistából
(a Mózes-könyvek) vette; a forrás ennél többet fed (a Próféták Jonatán-targumát is), a Zsoltárokat viszont nem.

A sorok mezőinek olvasói része szerkezetileg válik le, változatlanul: a tanú korának látható része a mező eleje
(a zárójeles adatbázis-évszám belső jelölés); a rabbinikus forrás hivatkozásának fejezet- és szakaszszáma szám. A
zárt értékkészletek (hagyomány, a tanú forrása) ismeretlen értéke kemény hiba.
"""
import datetime
import re
import unicodedata

from lapgen import konfig
from lapgen.bemenet import szavak as szavak_be
from lapgen.bemenet import szotari as szotari_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.ertekek import ForrasAllapot, TanuForras
from lapgen.szoveg import Strong

_OKORI_OSZLOPOK = ('motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes', 'betoldas',
                   'ellenorzes')
_TANU_OSZLOPOK = ('motivum', 'igehely', 'tanu_hely', 'hagyomany', 'tanu', 'mu', 'kor', 'kapcsolat', 'forras',
                  'lekerdezve', 'biblindex', 'ellenorzes', 'proveniencia')
_VALTOZAT_OSZLOPOK = ('igehely', 'strong', 'gorog', 'kiadasok', 'hianyzik_ebbol')
_APPARATUS_OSZLOPOK = ('igehely', 'jegyzet')
_TARGUM_OSZLOPOK = ('igehely',)
_ELVALASZTO = ' · '
_JELENTES_ZAROJEL = ' ('
_TANU_HELY_ELVALASZTO = '; '
_KOR_BELSO = ' (HCF: '                     # a kor mezőjének belső része: az adatbázis évszáma
_SEFARIA_HELY_RX = re.compile(r'^(?P<cim>.+) (?P<fejezet>\d+):(?P<resz>\d+)$')
_ZARO_IRASJEL = '·,.;'
_APPARATUS_MAS_RX = re.compile(r'\]\s*(\S+)')
_KIADAS_ELVALASZTO = '+'
_IGEN = 'igen'
_KONYV_RX = re.compile(r'^(\S+) \d')
_AUGMENTUM = 'ε'
_AUGMENTUM_MARADEK = 3


def _darabok(ertek):
    return tuple(x.strip() for x in ertek.split(_ELVALASZTO) if x.strip())


class OkoriSor:
    """A visszhang-tábla egy ókori fordítás-sora (Targum, Vulgata, LXX).

    `alakok`, `lemmak`, `kiejtesek`: a mező ` · `-vel tagolt részei idézetként; `csalad`: a szócsalád összevetési
    kulcsa a régi `_vh_csalad` szerint (LXX: a lemmák görög tövei; a többi forrásnál a lemma NFC alakja); `latin_csalad`:
    a lemmák első öt betűje kisbetűvel (a Vulgata szócsaládja az újszövetségi táblában; a `latin_jelek` ugyanez
    idézetként: a lemma eleje, a lapon „*maled-*” alakban); `tovek`: a görög lemmák
    tövei (az újszövetségi tábla LXX-oszlopához). `kiejtes_gepi`: a Targum-lemma gépi (arámi) kiejtése; a betoldás
    sorának `alak_kiejtes` és `jelentes` mezője a betoldás cellájához (a jelentés a mező eleje az első zárójelig)."""
    __slots__ = ('strong', 'igehely', 'forras', 'alakok', 'lemmak', 'kiejtesek', 'csalad', 'latin_csalad',
                 'latin_jelek', 'tovek', 'kiejtes_gepi', 'alak_kiejtes', 'jelentes', 'betoldas', 'ellenorzott',
                 'van_alak', 'van_lemma')

    def __init__(self, **mezok):
        for nev in self.__slots__:
            setattr(self, nev, mezok[nev])


def _csalad(forras, lemmak):
    if forras == konfig.FORRAS_LXX:
        ki = frozenset()
        for lemma in lemmak:
            ki |= szavak_be.gorog_alak_tovek(lemma)
        return ki
    return frozenset(unicodedata.normalize('NFC', x) for x in lemmak)


def okori_sorok(b, motivum):
    """B38 — a motívum ókori fordítás-sorai (Targum, Vulgata, LXX) a tábla rendjében."""
    return b.egyszer('B38:okori:%s' % motivum.kod, lambda: _okori_betolt(b, motivum))


def _okori_betolt(b, motivum):
    tabla = b._tabla('B38', oszlopok=_OKORI_OSZLOPOK)
    gepi = szavak_be.b13_heber_gepi(b)
    konyvek = b63_konyvek(b)
    ki = []
    for sor in tabla.szotarak():
        if sor['motivum'] != motivum.kod or sor['forras'] not in konfig.VISSZHANG_FORDITASOK:
            continue
        if not sor['igehely']:
            raise BemenetHiba('B38: ókori fordítás-sor igehely nélkül (%s, %s)' % (sor['strong'], sor['forras']))
        strong = Strong(sor['strong'])
        hely = konyvek.igehely(sor['igehely'])
        forras = sor['forras']
        lemmak = _darabok(sor['lemma'])
        kiejtes_gepi = None
        if forras == konfig.FORRAS_TARGUM and lemmak:
            k = gepi(lemmak[0], 0, False, aram=True)
            kiejtes_gepi = b.forrasszoveg('B13', 'kiejtes', k, hely) if k else None
        alak_kiejtes = None
        if sor['alak']:
            if forras == konfig.FORRAS_TARGUM:
                k = gepi(sor['alak'], 0, False, aram=True)
                alak_kiejtes = b.forrasszoveg('B13', 'kiejtes', k, hely) if k else None
            elif sor['kiejtes']:
                alak_kiejtes = b.forrasszoveg('B38', 'kiejtes', sor['kiejtes'], hely)
        jel = sor['jelentes'].split(_JELENTES_ZAROJEL)[0]
        ki.append(OkoriSor(
            strong=strong, igehely=hely, forras=forras,
            alakok=tuple(b.forrasszoveg('B38', 'alak', x, hely) for x in _darabok(sor['alak'])),
            lemmak=tuple(b.forrasszoveg('B38', 'lemma', x, hely) for x in lemmak),
            kiejtesek=tuple(b.forrasszoveg('B38', 'kiejtes', x, hely) for x in _darabok(sor['kiejtes'])),
            csalad=_csalad(forras, lemmak),
            latin_csalad=frozenset(x.lower()[:konfig.LATIN_CSALAD_HOSSZ] for x in lemmak),
            latin_jelek=tuple((x.lower()[:konfig.LATIN_CSALAD_HOSSZ],
                               b.forrasszoveg('B38', 'lemma_eleje', x.lower()[:konfig.LATIN_CSALAD_HOSSZ], hely))
                              for x in lemmak),
            tovek=_csalad(konfig.FORRAS_LXX, lemmak[:1]) if lemmak else frozenset(),
            kiejtes_gepi=kiejtes_gepi, alak_kiejtes=alak_kiejtes,
            jelentes=b.forrasszoveg('B38', 'jelentes', jel, hely) if jel else None,
            betoldas=sor['betoldas'] == _IGEN, ellenorzott=bool(sor['ellenorzes'].strip()),
            van_alak=bool(sor['alak']), van_lemma=bool(sor['lemma'])))
    return tuple(ki)


class GorogLemma:
    """Az újszövetségi hely görög szavának szótári alakja a görög szövegből (a TAGNT szótöve, idézet) és a tövei
    (összevetési kulcs)."""
    __slots__ = ('lemma', 'tovek')

    def __init__(self, lemma, tovek):
        self.lemma, self.tovek = lemma, tovek


def tagnt_lemma(b, igehely, strong):
    """A görög szó szótári alakja az újszövetségi versben (a régi `_tagnt_vers`: a vers első olyan szava, amelynek
    Strong-száma ez); None, ha a versben nem áll."""
    for s in szavak_be.b09_tagnt(b).sorok(igehely.kod):
        if s[0] == strong.kod:
            return GorogLemma(b.forrasszoveg('B09', 'szoto', s[3], igehely), szavak_be.gorog_alak_tovek(s[3]))
    return None


# --- B39: a tanúk -----------------------------------------------------------------------------------------------


class TanuSor:
    """A tanúk táblájának egy sora. `tanu`, `kor`, `kapcsolat`: kézi próza (a kor a mező látható eleje); `mu`: a mű
    címe idézetként (a rabbinikus forrásnál a hivatkozás címrésze, a `fejezet` és a `resz` számmal); `tanu_helyek`:
    a tanú tárgyalt helyei (üres: a sor helye)."""
    __slots__ = ('igehely', 'tanu_helyek', 'hagyomany', 'tanu', 'mu', 'fejezet', 'resz', 'kor', 'kapcsolat', 'forras',
                 'lekerdezve', 'biblindex', 'ellenorzott', 'proveniencia')

    def __init__(self, **mezok):
        for nev in self.__slots__:
            setattr(self, nev, mezok[nev])


def _datum(nyers, hely):
    if not nyers:
        return None
    try:
        return datetime.date.fromisoformat(nyers.strip())
    except ValueError:
        raise BemenetHiba('B39: érvénytelen lekérdezési dátum: %r (%s)' % (nyers, hely)) from None


def b39_tanuk(b, motivum):
    """B39 — a motívum ókori tanúi (az egyházatyák, a rabbinikus források, a Glossa Ordinaria, a Chain Lineage)."""
    tabla = b._tabla('B39', oszlopok=_TANU_OSZLOPOK)
    konyvek = b63_konyvek(b)
    ki = []
    for sor in tabla.szotarak():
        if sor['motivum'] != motivum.kod:
            continue
        hely = konyvek.igehely(sor['igehely'])
        if sor['hagyomany'] not in konfig.TANU_HAGYOMANYOK:
            raise BemenetHiba('B39: ismeretlen hagyomány: %r (%s)' % (sor['hagyomany'], hely.kod))
        try:
            forras = TanuForras(sor['forras'])
        except ValueError:
            raise BemenetHiba('B39: ismeretlen tanú-forrás: %r (%s)' % (sor['forras'], hely.kod)) from None
        helyek = tuple(konyvek.igehely(x) for x in sor['tanu_hely'].split(_TANU_HELY_ELVALASZTO) if x.strip())
        mu, fejezet, resz = sor['mu'], None, None
        if forras is TanuForras.SEFARIA:
            m = _SEFARIA_HELY_RX.match(sor['mu'])
            if not m:
                raise BemenetHiba('B39: a rabbinikus forrás hivatkozása nem „cím fejezet:szakasz” alakú: %r'
                                  % sor['mu'])
            mu, fejezet, resz = m.group('cim'), int(m.group('fejezet')), int(m.group('resz'))
        kor = sor['kor'].split(_KOR_BELSO)[0]
        ki.append(TanuSor(
            igehely=hely, tanu_helyek=helyek, hagyomany=b.kulcs('B39', 'hagyomany', sor['hagyomany']),
            tanu=b.kezi('B39', 'tanu', sor['tanu']), mu=b.forrasszoveg('B39', 'mu', mu, hely),
            fejezet=fejezet, resz=resz, kor=b.kezi('B39', 'kor', kor) if kor else None,
            kapcsolat=b.kezi('B39', 'kapcsolat', sor['kapcsolat']), forras=forras,
            lekerdezve=_datum(sor['lekerdezve'], hely.kod), biblindex=sor['biblindex'] == _IGEN,
            ellenorzott=bool(sor['ellenorzes'].strip()),
            proveniencia=b.belso('B39', 'proveniencia', sor['proveniencia'])))
    return tuple(ki)


# --- B41, B74: a görög szövegváltozatok ------------------------------------------------------------------------


class Valtozat:
    """A lánc szavát érintő szövegváltozat egy versben: az alak és a kiadásai, a kiadások, amelyekből hiányzik, és
    az apparátus szerinti másik alak (None: az apparátus nem nevez meg másik alakot), a tövével."""
    __slots__ = ('alak', 'kiadasok', 'hianyzik', 'mas', 'mas_tovek')

    def __init__(self, alak, kiadasok, hianyzik, mas, mas_tovek):
        self.alak, self.kiadasok, self.hianyzik, self.mas, self.mas_tovek = alak, kiadasok, hianyzik, mas, mas_tovek


def alak_tovek(alak):
    """A ragozott görög alak tövei az augmentum nélkül is (a régi `_alak_tovek`, ELLENOR_F183 1.): διέφθειρεν →
    δι + ε + φθειρεν."""
    t = ''.join(c for c in unicodedata.normalize('NFD', alak.lower()) if not unicodedata.combining(c))
    tovek = set(szavak_be.gorog_alak_tovek(t))
    for elotag in konfig.GOROG_AUGMENTUM_ELOTAGOK:
        if t.startswith(elotag + _AUGMENTUM) and len(t) > len(elotag) + _AUGMENTUM_MARADEK:
            tovek |= szavak_be.gorog_alak_tovek(t[len(elotag) + 1:])
    return frozenset(tovek)


class Valtozatok:
    def __init__(self, sorok, apparatus):
        self._sorok, self._apparatus = sorok, apparatus

    def versben(self, igehely, strongok):
        """A vers változatai a megadott görög szavakon (a változatjegyzék rendjében)."""
        kodok = {s.kod for s in strongok}
        return tuple(v for hely, strong, v in self._sorok if hely == igehely.kod and strong in kodok)


def _kiadasok(b, nyers, hely, elvalaszto):
    return tuple(b.forrasszoveg('B41', 'kiadas', x, hely) for x in nyers.split(elvalaszto) if x.strip())


def b41_valtozatok(b):
    """B41 — a görög szöveg változatjegyzéke (STEPBible TAGNT): a kiadásokból hiányzó szóalakok; mellé az SBL
    Greek New Testament apparátusának (B74) jegyzete adja a másik alakot."""
    def betolt():
        tabla = b._tabla('B41', oszlopok=_VALTOZAT_OSZLOPOK)
        apparatus = b74_apparatus(b)
        konyvek = b63_konyvek(b)
        sorok = []
        for sor in tabla.szotarak():
            if not sor['hianyzik_ebbol'].strip():
                continue
            alak = sor['gorog'].rstrip(_ZARO_IRASJEL)
            hely = konyvek.igehely(sor['igehely'])
            jegyzet = next((j for v, j in apparatus if v == sor['igehely'] and alak in j), '')
            m = _APPARATUS_MAS_RX.search(jegyzet.replace('\xa0', ' '))
            mas = m.group(1) if m else None
            sorok.append((sor['igehely'], sor['strong'], Valtozat(
                alak=b.forrasszoveg('B41', 'gorog', alak, hely),
                kiadasok=_kiadasok(b, sor['kiadasok'], hely, _KIADAS_ELVALASZTO),
                hianyzik=_kiadasok(b, sor['hianyzik_ebbol'], hely, None),
                mas=b.forrasszoveg('B74', 'jegyzet', mas, hely) if mas else None,
                mas_tovek=alak_tovek(mas) if mas else frozenset())))
        return Valtozatok(tuple(sorok), apparatus)
    return b.egyszer('B41', betolt)


def b74_apparatus(b):
    """B74 — az SBL Greek New Testament apparátusa: (igehely kódja, jegyzet) párok a tábla rendjében."""
    def betolt():
        tabla = b._tabla('B74', oszlopok=_APPARATUS_OSZLOPOK)
        return tuple((sor['igehely'], sor['jegyzet']) for sor in tabla.szotarak())
    return b.egyszer('B74', betolt)


# --- B64, B73: a fordítás-források állapota (GK-28) -------------------------------------------------------------


class TargumLefedes:
    """A Targum szövegének lefedettsége: a jegyzék állapota és a könyvek, amelyeket a forrás tartalmaz."""
    __slots__ = ('allapot', 'konyvek')

    def __init__(self, allapot, konyvek):
        self.allapot, self.konyvek = allapot, konyvek

    def fedi(self, igehely):
        return igehely.konyv in self.konyvek


def _allapot(b, b_id):
    try:
        return ForrasAllapot(b.jegyzek_sor(b_id).allapot)
    except ValueError:
        raise BemenetHiba('%s: a forrás-állapot mondatához ismeretlen jegyzék-állapot: %r'
                          % (b_id, b.jegyzek_sor(b_id).allapot)) from None


def b64_targum(b):
    """B64 — a Targum szövege (Onkelos, Jonatán): mely könyveket fedi. A jegyzék állapota és a fájl tartalma
    összevetve: „részleges” állapotnál a forrás nem fedheti az egész Ószövetséget, „aktív” állapotnál igen."""
    def betolt():
        allapot = _allapot(b, 'B64')
        tabla = b._tabla('B64', oszlopok=_TARGUM_OSZLOPOK)
        konyvek = set()
        for sor in tabla.szotarak():
            m = _KONYV_RX.match(sor['igehely'])
            if m:
                konyvek.add(m.group(1))
        osz = {k for k in b63_konyvek(b).osszes() if not b63_konyvek(b).ujszovetsegi(k)}
        teljes = osz <= konyvek
        if allapot is ForrasAllapot.RESZLEGES and teljes:
            raise BemenetHiba('B64: a jegyzék szerint a Targum-forrás részleges, de minden ószövetségi könyvet fed: '
                              'a jegyzék állapota elavult')
        if allapot is ForrasAllapot.AKTIV and not teljes:
            raise BemenetHiba('B64: a jegyzék szerint a Targum-forrás teljes, de %d ószövetségi könyv hiányzik belőle'
                              % len(osz - konyvek))
        if allapot not in (ForrasAllapot.AKTIV, ForrasAllapot.RESZLEGES):
            raise BemenetHiba('B64: a Targum-forrás állapota %s; a 9. szakasz ókori fordítás-táblája a Targumot olvassa'
                              % allapot.value)
        return TargumLefedes(allapot, frozenset(konyvek))
    return b.egyszer('B64', betolt)


def b73_peshitta(b):
    """B73 — a szír fordítás (Peshitta) forrásának állapota. „Nem vizsgált” állapotnál a forrásnak nem szabad
    megvolnia (ha megvan, a jegyzék állapota elavult); „aktív” állapotnál meg kell lennie. A 9. szakasz a szír
    fordítást nem olvassa: aktív forrásnál a hozzá tartozó oszlop még nincs kész, ez kimondott hiba."""
    allapot = _allapot(b, 'B73')
    megvan = bool(b._utvonalak('B73')) and b._van('B73')
    if allapot is ForrasAllapot.NEM_VIZSGALT and megvan:
        raise BemenetHiba('B73: a jegyzék szerint a Peshitta nem vizsgált, de a forrása megvan: a jegyzék állapota '
                          'elavult')
    if allapot is not ForrasAllapot.NEM_VIZSGALT:
        raise BemenetHiba('B73: a Peshitta állapota %s; a 9. szakasz a szír fordítást még nem olvassa'
                          % allapot.value)
    return allapot


# --- az LXX-alapvonal (B08, B35, B36) ---------------------------------------------------------------------------


_GLOSSZA_SZO_RX = re.compile(r'[a-z]+')


def _glossza_tovek(glosszak):
    return {w[:konfig.GLOSSZA_TO_HOSSZ] for g in glosszak for w in _GLOSSZA_SZO_RX.findall(g.lower())
            if len(w) >= konfig.GLOSSZA_TO_HOSSZ and w not in konfig.GLOSSZA_STOP}


def lxx_alapvonal(b, heber, csalad, lanc_versek):
    """(arány, versszám) a régi `lxx_alapvonal` szerint: a héber szó láncon kívüli ószövetségi verseinek hány részében
    áll a görög versben a szócsalád valamely lemmája (versszintű együtt-előfordulás, B36). Csak a láncbeli jelentés
    előfordulásai számítanak: a vers TAHOT-tükörfordítása a láncversekével közös szótövet hordoz. (None, 0): nincs
    láncon kívüli vers."""
    versek = szotari_be.b36_lxx_parok(b).versek(heber)
    if not versek:
        return None, 0
    lemma = szotari_be.lxx_lemmak(b)
    tg = szavak_be.b08_tahot(b).glosszak(heber.kod)
    lanc = {v.kod for v in lanc_versek}
    lanc_tovek = _glossza_tovek(g for v in lanc for g in tg.get(v, ()))
    kivul = [gs for v, gs in versek.items() if v not in lanc
             and (not lanc_tovek or _glossza_tovek(tg.get(v, ())) & lanc_tovek)]
    if not kivul:
        return None, 0
    van = sum(1 for gs in kivul if any(szavak_be.gorog_alak_tovek(lemma[g]) & csalad for g in gs if lemma.get(g)))
    return van / len(kivul), len(kivul)
