"""lapgen.bemenet.alap — a lap keretéhez tartozó kis bemenetek: befagyasztás (B59), licenc (B01), döntések (B51)."""
import datetime
import re

from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.szoveg import MotivumId


def b59_befagyasztott(b):
    """B59 — a befagyasztott motívumok halmaza (futásidőben olvasva, nem importkor)."""
    tabla = b._tabla('B59', oszlopok=('id',))
    i = tabla.oszlop('id')
    return frozenset(MotivumId(sor[i]) for sor in tabla.sorok)


class Licencek:
    """A licencleltár: adatkészletenként a rövid licenccímke. Licencszöveg csak innen jön (GK-07)."""

    def __init__(self, b, cimkek):
        self._b, self._cimkek = b, cimkek

    def cimke(self, kulcs):
        try:
            return self._b.forrasszoveg('B01', 'cimke', self._cimkek[kulcs], None)
        except KeyError:
            raise BemenetHiba('B01: nincs `%s` sor a licencleltárban (a licencjelölés egyetlen forrása)' % kulcs) from None


def b01_licencek(b):
    """B01 — a licencleltár (`dataset` → `cimke`)."""
    tabla = b._tabla('B01', oszlopok=('dataset', 'allapot', 'cimke'))
    d, c = tabla.oszlop('dataset'), tabla.oszlop('cimke')
    cimkek = {}
    for sor in tabla.sorok:
        if not sor[c]:
            raise BemenetHiba('B01: üres `cimke` a(z) `%s` sorban' % sor[d])
        cimkek[sor[d]] = sor[c]
    return Licencek(b, cimkek)


_DONTES_SOR_RX = re.compile(r'^\|\s*(DT-?F?\d+[a-z]{0,2})\s*\|')
_UTOD_RX = re.compile(r'\*\*FELÜLÍRVA\s*→\s*(DT-?F?\d+[a-z]{0,2})\*\*')
_DATUM_RX = re.compile(r'(20\d\d)[-.](\d\d)[-.](\d\d)')
_ERVENYTELEN_JEL = '⛔'


class Dontesek:
    """A döntések érvényessége és dátuma. A lapra döntésszám nem kerül, csak a döntés dátuma."""

    def __init__(self, sorok):
        self._sorok = sorok

    def ervenyes(self, azonosito):
        """Az érvényes döntés azonosítója: maga, vagy felülírt döntésnél a felülíró lánc vége."""
        latott = set()
        while azonosito in self._sorok and not self._sorok[azonosito][0]:
            if azonosito in latott or self._sorok[azonosito][1] is None:
                raise BemenetHiba('B51: a(z) %s döntés érvénytelen, és nincs érvényes utódja' % azonosito)
            latott.add(azonosito)
            azonosito = self._sorok[azonosito][1]
        if azonosito not in self._sorok:
            raise BemenetHiba('B51: ismeretlen döntés: %s' % azonosito)
        return azonosito

    def datum(self, azonosito):
        """Az érvényes döntés dátuma (a sorában álló első dátum)."""
        datum = self._sorok[self.ervenyes(azonosito)][2]
        if datum is None:
            raise BemenetHiba('B51: a(z) %s döntés sorában nincs dátum' % azonosito)
        return datum


def b51_dontesek(b):
    """B51 — a döntések táblája: érvényesség (az „Állapot” cella ⛔ jele, a felülíró döntés) és dátum."""
    sorok = {}
    for utvonal in b._utvonalak('B51'):
        for sor in b._szoveg('B51', utvonal=utvonal).split('\n'):
            m = _DONTES_SOR_RX.match(sor)
            if not m:
                continue
            cellak = [c.strip() for c in sor.strip().strip('|').split(' | ')]
            allapot = cellak[5] if len(cellak) > 5 else ''
            dontes = cellak[6] if len(cellak) > 6 else ''
            ervenytelen = allapot.startswith(_ERVENYTELEN_JEL)
            utod = _UTOD_RX.search(dontes)
            d = _DATUM_RX.search(sor)
            sorok[m.group(1)] = (not ervenytelen, utod.group(1) if (ervenytelen and utod) else None,
                                 datetime.date(int(d.group(1)), int(d.group(2)), int(d.group(3))) if d else None)
    return Dontesek(sorok)
