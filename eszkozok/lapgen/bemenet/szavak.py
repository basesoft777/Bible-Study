"""lapgen.bemenet.szavak — a héber és a görög szöveg szavai a kiejtésükkel: egy kiejtés-szolgáltatás.

Bemenetek: B08 (a héber szöveg szavai, TAHOT), B09 (a görög szöveg szavai, TAGNT), B12 (a kiejtés szabály- és
kivételtáblája), B13 (a héber gépi kiejtés szabálya: kódmodul, nem fájl). A kiejtés minden lapon ezen az egy
úton jön (GK-13).

Ismétlődés (GK-14, T4): ha egy Strong-szám többször áll egy versben, az **első** előfordulás alakja és
kiejtése számít, a vers szövegrendje szerint.
"""
import re

import heber_kiejtes
import kiejtes as kiejtes_modul

from lapgen.bemenet.jegyzek import BemenetHiba

_ZARO_IRASJEL_RX = re.compile(r'[,.;·]+$')
_TAHOT_OSZLOPOK = ('Igehely', 'Strong-szám', 'Ragozott alak', 'Kiejtés')
_HEBER_ELOTAG = 'H'


class Szo:
    """Egy szó a versben: a ragozott alak és a kiejtése, idézhető forrásszövegként."""
    __slots__ = ('strong', 'alak', 'kiejtes')

    def __init__(self, strong, alak, kiejtes):
        self.strong, self.alak, self.kiejtes = strong, alak, kiejtes


class _Szoveg:
    """Egy szövegkiadás szavai versenként, a fájl sorrendjében: {igehely: [(Strong, alak, átírás)]}."""

    def __init__(self, versenkent):
        self._versenkent = versenkent

    def sorok(self, vers_kod):
        return self._versenkent.get(vers_kod, ())

    def token_szam(self, vers_kod, strong_kod):
        return sum(1 for s in self._versenkent.get(vers_kod, ()) if s[0] == strong_kod)


def _szoveg_betolt(b, b_id):
    tabla = b._tabla(b_id, oszlopok=_TAHOT_OSZLOPOK)
    i, s, a, k = (tabla.oszlop(o) for o in _TAHOT_OSZLOPOK)
    versenkent = {}
    for sor in tabla.sorok:
        versenkent.setdefault(sor[i], []).append((sor[s], sor[a], sor[k]))
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
        self._szabalyok, self._gorog_kivetelek, _heber = b12_kiejtes_tablak(b)
        self._heber_gepi = b13_heber_gepi(b)

    def token_szam(self, vers, strong):
        """Hányszor áll a héber Strong-szám a versben."""
        return self._tahot.token_szam(vers.kod, strong.kod)

    def ragozott(self, versek, strong):
        """A szó első előfordulása a megadott versek közül az elsőben, amelyben áll; None, ha egyikben sem."""
        heber = strong.kod.startswith(_HEBER_ELOTAG)
        szoveg = self._tahot if heber else self._tagnt
        for vers in versek:
            sorok = szoveg.sorok(vers.kod)
            helyek = [k for k, s in enumerate(sorok) if s[0] == strong.kod]
            if not helyek:
                continue
            i = helyek[0]
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


def kiejtes(b):
    """A kiejtés-szolgáltatás a munkamenethez."""
    return b.egyszer('kiejtes', lambda: Kiejtes(b))
