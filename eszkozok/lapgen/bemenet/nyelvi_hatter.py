"""lapgen.bemenet.nyelvi_hatter — a 4.8 pont (Nyelvi háttér) görög részének bemenetei.

Bemenetek: B25 (a lexikon szótári hivatkozástáblája: melyik szóhoz melyik szótárnak van szócikke), B26 (az LSJ
teljes szövege: az utaló csonk felismerése), B37 (az LXX-fordítói döntések: a motívum verseiben megnevezett görög
szavak, a rokon szavak forrása).

A régi generátor szabályai (`lexikon_general._hivatkozas_szoveg`, `lsj_csonk`, `rokon_szavak_strongok`,
`lxx_dontesek_index`): az utaló csonk az a szócikk, amely csak a képzés leírása („… Middle voice from G1909 and
G2564”); az alapige a csonk utolsó Strong-száma. A rokon szó a motívum verseinek LXX-döntéseiben megnevezett, a
motívumon kívüli görög szó, amelynek a kiegészítő szótárakon kívül szócikke van.
"""
import re

from lapgen import konfig
from lapgen.bemenet import szavak as szavak_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import Strong

_HIV_OSZLOPOK = ('strong', 'szotar')
_LSJ_OSZLOPOK = ('Strong_padded', 'Teljes_szocikk')
_LXX_OSZLOPOK = ('igehely', 'gorog_strong', 'tipus', 'bizonyossag')
_LSJ_CSONK_RX = re.compile(r'^\S+ (?:Middle voice |Passive voice )?from G\d+(?: and G\d+)?\.?$')
_STRONG_RX = re.compile(r'\bG(\d+)\b')
_GOROG_STRONG_RX = re.compile(r'^G\d{4}$')


class Hivatkozasok:
    """A szótári hivatkozástábla: Strong-szám → a szócikket adó szótárak."""

    def __init__(self, szotarak):
        self._szotarak = szotarak

    def szotarai(self, strong):
        return self._szotarak.get(strong.kod, frozenset())


def b25_hivatkozasok(b):
    """B25 — a lexikon szótári hivatkozástáblája (melyik szóhoz melyik szótárnak van szócikke)."""
    tabla = b._tabla('B25', oszlopok=_HIV_OSZLOPOK)
    s, sz = tabla.oszlop('strong'), tabla.oszlop('szotar')
    szotarak = {}
    for sor in tabla.sorok:
        szotarak.setdefault(sor[s], set()).add(sor[sz])
    return Hivatkozasok({k: frozenset(v) for k, v in szotarak.items()})


class Csonk:
    """Az LSJ utaló csonkja: a szócikk szövege (idézet) és az alapige Strong-száma (a csonk utolsó száma)."""
    __slots__ = ('szoveg', 'alap')

    def __init__(self, szoveg, alap):
        self.szoveg, self.alap = szoveg, alap


class Lsj:
    def __init__(self, b, szocikkek):
        self._b, self._szocikkek = b, szocikkek

    def csonk(self, strong):
        """A szó LSJ-szócikke, ha az csak utaló csonk; különben None."""
        szoveg = (self._szocikkek.get(strong.kod) or '').strip()
        if not szoveg or not _LSJ_CSONK_RX.match(szoveg):
            return None
        szamok = _STRONG_RX.findall(szoveg)
        if not szamok:
            raise BemenetHiba('B26: a(z) %s utaló csonkjában nincs Strong-szám' % strong.kod)
        return Csonk(self._b.forrasszoveg('B26', 'Teljes_szocikk', szoveg, strong),
                     Strong('G%04d' % int(szamok[-1])))


def b26_lsj(b):
    """B26 — az LSJ teljes szövege Strong-szám szerint (csak az utaló csonk felismeréséhez)."""
    tabla = b._tabla('B26', oszlopok=_LSJ_OSZLOPOK)
    s, sz = tabla.oszlop('Strong_padded'), tabla.oszlop('Teljes_szocikk')
    return Lsj(b, {sor[s]: sor[sz] for sor in tabla.sorok})


class LxxDontesek:
    def __init__(self, index):
        self._index = index

    def gorog_szavak(self, vers_kod):
        """A vers megjelenő LXX-döntéseiben megnevezett görög Strong-számok, a tábla rendjében."""
        return self._index.get(vers_kod, ())


def b37_lxx_dontesek(b):
    """B37 — az LXX-fordítói döntések, a megjelenő bizonyosság és típus szűrőjével (a régi `lxx_dontesek_index`)."""
    tabla = b._tabla('B37', oszlopok=_LXX_OSZLOPOK)
    i, g, t, bz = (tabla.oszlop(o) for o in _LXX_OSZLOPOK)
    index = {}
    for sor in tabla.sorok:
        if sor[bz].strip() not in konfig.LXX_DONTES_BIZONYOSSAG or sor[t].strip() not in konfig.LXX_DONTES_TIPUS:
            continue
        gs = sor[g].strip()
        if _GOROG_STRONG_RX.match(gs):
            index.setdefault(sor[i], []).append(Strong(gs))
    return LxxDontesek({k: tuple(v) for k, v in index.items()})


# --- a 4.8 héber része: a rokon nyelvi tábla bemenetei ------------------------------------------------------------

_ROKON_LEKERDEZVE_RX = re.compile(r'^# lekérdezve: (H\d+) \|.*bdb_szócikk=(\d+)')
_VISSZHANG_OSZLOPOK = ('motivum', 'strong', 'igehely', 'forras', 'alak', 'lemma', 'kiejtes', 'jelentes',
                       'megjegyzes', 'ellenorzes')
# A jelentés-mező végén álló BDB-utalás (a régi `_magyar_jelentes` mintája): a zárójeles forrásmegjegyzés és a
# „; a BDB: …” toldalék nem a jelentés része. A réteg szerkezetileg bont: a látható jelentés a mező eleje, változatlanul.
_JELENTES_UTALAS_RX = re.compile(r'\s*\((?:[^()]*\b(?:BDB|so|see|Assyrian|Late|cf)\b[^()]*)\)')
_JELENTES_TOLDALEK_RX = re.compile(r';\s*a BDB:')
_KIEJTES_ZAROJEL_RX = re.compile(r'\s*\(.*?\)')
_KIEJTES_ELVALASZTO = '·'
_NYELV_PONTOSITAS = ' ('
_HEBER_BETU_RX = re.compile('[֐-׿]')
_BIZONYTALAN_RX = re.compile(r'\?|possibly|bizonytalan|valószínűleg|kétséges|dubious|ritka')


def b24_rokon_irasok(b):
    """B24 — a rokon írások lekérdezésének gyorsítótára: a `# lekérdezve:` sorok szerint Strong-számonként, hány
    BDB-szócikket azonosított a lekérdezés ({Strong kódja: szám}; a le nem kérdezett Strong hiányzik)."""
    def betolt():
        ki = {}
        for sor in b._szoveg('B24').split('\n'):
            m = _ROKON_LEKERDEZVE_RX.match(sor)
            if m:
                ki[m.group(1)] = int(m.group(2))
        return ki
    return b.egyszer('B24', betolt)


def _eleje(mezo, ertek, olvasoi, b_id='B38'):
    if not ertek.startswith(olvasoi):
        raise BemenetHiba('%s: a(z) `%s` mező olvasói része nem a mező eleje („%s”): a forrásban javítandó'
                          % (b_id, mezo, ertek[:80]))
    return olvasoi


class RokonAlak:
    """A rokon nyelvi szó egy írott alakja (idézet) és a kiejtése (idézet vagy gépi kiejtés; None: nincs)."""
    __slots__ = ('alak', 'kiejtes')

    def __init__(self, alak, kiejtes):
        self.alak, self.kiejtes = alak, kiejtes


class RokonSor:
    """A visszhang-megfelelők egy `bdb` (rokon nyelvi) sora, a régi `_hatter_sorok` szűrőinek jelzőivel.

    A `nyelv` a lemma-mező (a rokon nyelv neve, a tábla szövege), a `nyelv_kulcs` a csoportosítás kulcsa; az
    `alakok` az `alak` mező `·`-vel tagolt írott alakjai a kiejtéssel; a `jelentes` a mező olvasói része (a
    BDB-utalás nélkül: a mező eleje). A jelzők: `ellenorzott` (az ellenőrzés mezője nem üres), `rokon_nyelv` (a
    nyelv valódi rokon nyelv, nem targumi arámi), `ures` (a sornak nincs alakja és nyelve: a szócikkben nincs rokon
    adat), `azonos` (a jelentés „azonos a bibliai héberrel”), `romlott`, `bizonytalan` (a megjegyzés szerint)."""
    __slots__ = ('strong', 'nyelv', 'nyelv_kulcs', 'alakok', 'jelentes', 'ellenorzott', 'rokon_nyelv', 'ures',
                 'azonos', 'romlott', 'bizonytalan')

    def __init__(self, **mezok):
        for nev in self.__slots__:
            setattr(self, nev, mezok[nev])


class Visszhang:
    """A motívum visszhang-megfelelői: van-e ókori fordítás-sora (Targum, Vulgata, LXX), és a rokon nyelvi sorok
    a tábla rendjében."""
    __slots__ = ('van_forditas', 'rokon')

    def __init__(self, van_forditas, rokon):
        self.van_forditas, self.rokon = van_forditas, rokon


def _alakok(b, sor, kiejtes, hely):
    """Az írott alakok a kiejtéssel (a régi `_hatter_sorok` szabálya): a pontozatlan héber alak kiejtés nélkül áll
    (a vokalizációját az adat nem adja, F194); a pontozott héber alak gépi kiejtést kap (B13); a nem héber írású
    alak a sor kiejtés-mezőjének első kiejtését."""
    gepi = szavak_be.b13_heber_gepi(b)
    ki = []
    for alak in [x.strip() for x in sor['alak'].split(_KIEJTES_ELVALASZTO) if x.strip()]:
        idezett = b.forrasszoveg('B38', 'alak', alak, hely)
        if _HEBER_BETU_RX.search(alak):
            if not szavak_be.heber_pontozott(alak):
                ki.append(RokonAlak(idezett, None))
                continue
            gepi_kiejtes = gepi(alak, 0, False)
            if not gepi_kiejtes:
                raise BemenetHiba('B38: a(z) %s pontozott rokon alakjára nincs gépi kiejtés' % alak)
            ki.append(RokonAlak(idezett, b.forrasszoveg('B13', 'kiejtes', gepi_kiejtes, hely)))
        else:
            ki.append(RokonAlak(idezett, b.forrasszoveg('B38', 'kiejtes', kiejtes, hely) if kiejtes else None))
    return tuple(ki)


def b38_visszhang(b, motivum):
    """B38 — a motívum visszhang-megfelelői (az ókori fordítások és a BDB rokon nyelvi adatai)."""
    tabla = b._tabla('B38', oszlopok=_VISSZHANG_OSZLOPOK)
    van_forditas, rokon = False, []
    for sor in tabla.szotarak():
        if sor['motivum'] != motivum.kod:
            continue
        if sor['forras'] in konfig.VISSZHANG_FORDITASOK:
            van_forditas = True
        if sor['forras'] != konfig.VISSZHANG_ROKON:
            continue
        hely = Strong(sor['strong'])
        jel = _JELENTES_TOLDALEK_RX.split(_JELENTES_UTALAS_RX.sub('', sor['jelentes']))[0].strip(' ;')
        kiejtes = _KIEJTES_ZAROJEL_RX.sub('', sor['kiejtes']).split(_KIEJTES_ELVALASZTO)[0].strip()
        megj = sor['megjegyzes']
        nyelv = sor['lemma'].split(_NYELV_PONTOSITAS)[0].strip()
        rokon.append(RokonSor(
            strong=hely,
            nyelv=b.forrasszoveg('B38', 'lemma', sor['lemma'], hely) if sor['lemma'] else None,
            nyelv_kulcs=sor['lemma'],
            alakok=_alakok(b, sor, _eleje('kiejtes', sor['kiejtes'], kiejtes), hely),
            jelentes=b.forrasszoveg('B38', 'jelentes', _eleje('jelentes', sor['jelentes'], jel), hely) if jel else None,
            ellenorzott=bool(sor['ellenorzes'].strip()),
            rokon_nyelv=(nyelv in konfig.ROKON_NYELVEK and not any(j in megj for j in konfig.ROKON_TARGUM_JELEK)),
            ures=not sor['alak'] and not sor['lemma'],
            azonos=konfig.ROKON_AZONOS in jel,
            romlott=konfig.ROKON_ROMLOTT in megj,
            bizonytalan=bool(_BIZONYTALAN_RX.search(megj + jel))))
    return Visszhang(van_forditas, tuple(rokon))
