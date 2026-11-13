"""lapgen.megjelenites.md.iro — a Markdown-lap írója.

Ez az egyetlen modul, amely a `Lathato` értéket szöveggé alakítja (`kiiras`), és amely a
`Proveniencia` szövegét kiírja; az utóbbit csak HTML-megjegyzésbe. Az író háromféle darabot fogad el:

    Lathato        látható szöveg (próza, sablonmondat, idézet)
    Proveniencia   megjegyzésbe kerül
    Jel            szerkezeti jelölés a modul zárt készletéből (horgony, lábjegyzet-szám, cellahatár)

Nyers `str` darab nem adható át. Minden kiírt sorhoz fajta-térkép készül (melyik karakter próza,
sablon, idézet, megjegyzés vagy jelölés); ezt használja a festékpróba és az alakosztály-kapu.
"""
from lapgen.szoveg import Horgony, Lathato, Proveniencia, SzovegHiba, kiiras, prov_szoveg

MEGJEGYZES = 'megjegyzes'
JELOLES = 'jeloles'


class Jel:
    """Szerkezeti jelölés: nem látható szöveg. Csak ennek a modulnak a gyártófüggvényei hozzák létre."""
    __slots__ = ('_szoveg',)

    def __init__(self, szoveg, _engedely=None):
        if _engedely is not _JEL_ENGEDELY:
            raise SzovegHiba('Jel csak az iro modul gyártófüggvényeivel készülhet')
        self._szoveg = szoveg


_JEL_ENGEDELY = object()


def _jel(szoveg):
    return Jel(szoveg, _JEL_ENGEDELY)


def _szam(ertek):
    if isinstance(ertek, bool) or not isinstance(ertek, int):
        raise SzovegHiba('a jelölés sorszáma egész szám legyen')
    return str(ertek)


def lj_hivatkozas(szakasz, sorszam):
    """Lábjegyzet-hivatkozás a táblacellában: a szakasz és a jegyzet sorszámával."""
    s, n = _szam(szakasz), _szam(sorszam)
    return _jel('<sup class="lj"><a href="#j-' + s + '-' + n + '">' + s + '.' + n + '</a></sup>')


def lj_fej(szakasz, sorszam):
    """A tábla alatti jegyzet sorának eleje: listajel és a jegyzet horgonyos száma."""
    s, n = _szam(szakasz), _szam(sorszam)
    return _jel('- <span class="lj-szam" id="j-' + s + '-' + n + '">' + s + '.' + n + '</span>')


def horgony_jel(horgony):
    """Üres horgony-elem egy lapon belüli célponthoz."""
    if not isinstance(horgony, Horgony):
        raise SzovegHiba('horgony_jel(): Horgony kell')
    return _jel('<a id="' + horgony.kod + '"></a>')


OLVASOI_JEL = _jel('<!-- olvasói -->')
DETAILS_NYIT, DETAILS_ZAR = _jel('<details>'), _jel('</details>')
SUMMARY_NYIT, SUMMARY_ZAR = _jel('<summary>'), _jel('</summary>')
_CELLA_NYIT = _jel('| ')
_CELLA_KOZ = _jel(' | ')
_CELLA_ZAR = _jel(' |')


class KeszSor:
    """Egy kiírt sor és a fajta-térképe: (kezdet, vég, fajta) tartományok."""
    __slots__ = ('szoveg', 'tartomanyok')

    def __init__(self, szoveg, tartomanyok):
        self.szoveg = szoveg
        self.tartomanyok = tartomanyok


def _megjegyzes_szoveg(proveniencia):
    belso = prov_szoveg(proveniencia)
    if '-->' in belso or '\n' in belso:
        raise SzovegHiba('a megjegyzés szövege nem tartalmazhat megjegyzés-zárót vagy sortörést')
    return '<!-- ' + belso + ' -->'


class Lapiro:
    """A lap sorainak gyűjtője."""

    def __init__(self):
        self._sorok = []

    def sor(self, *darabok):
        """Egy sor a darabokból. Üres hívás üres sort ad."""
        reszek, tartomanyok, hol = [], [], 0
        for darab in darabok:
            if isinstance(darab, Lathato):
                kiirt = kiiras(darab)
                if '\n' in kiirt.szoveg:
                    raise SzovegHiba('a látható szöveg nem tartalmazhat sortörést')
                reszek.append(kiirt.szoveg)
                tartomanyok.extend((hol + k, hol + v, f) for k, v, f in kiirt.tartomanyok)
                hol += len(kiirt.szoveg)
            elif isinstance(darab, Proveniencia):
                szoveg = _megjegyzes_szoveg(darab)
                reszek.append(szoveg)
                tartomanyok.append((hol, hol + len(szoveg), MEGJEGYZES))
                hol += len(szoveg)
            elif isinstance(darab, Jel):
                reszek.append(darab._szoveg)
                tartomanyok.append((hol, hol + len(darab._szoveg), JELOLES))
                hol += len(darab._szoveg)
            else:
                raise SzovegHiba('az író csak Lathato, Proveniencia vagy Jel darabot fogad el, nem ezt: %s'
                                 % type(darab).__name__)
        self._sorok.append(KeszSor(''.join(reszek), tuple(tartomanyok)))

    def ures(self):
        self.sor()

    def cimsor(self, szint, cim):
        if szint not in (1, 2, 3, 4, 5):
            raise SzovegHiba('a címsor szintje 1 és 5 között legyen')
        self.sor(_jel('#' * szint + ' '), cim)

    def tabla_sor(self, cellak):
        """Táblasor; minden cella darabok sora (Lathato vagy Jel)."""
        darabok = [_CELLA_NYIT]
        for i, cella in enumerate(cellak):
            if i:
                darabok.append(_CELLA_KOZ)
            darabok.extend(cella if isinstance(cella, (tuple, list)) else (cella,))
        darabok.append(_CELLA_ZAR)
        self.sor(*darabok)

    def tabla_elvalaszto(self, oszlopok):
        self.sor(_jel('|' + '---|' * oszlopok))

    def kesz(self):
        return tuple(self._sorok)


def lap_szoveg(sorok):
    """A kész sorok egy fájl szövegeként (LF sorvéggel, záró sortöréssel)."""
    return '\n'.join(s.szoveg for s in sorok) + '\n'
