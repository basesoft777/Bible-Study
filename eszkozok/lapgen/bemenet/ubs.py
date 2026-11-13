"""lapgen.bemenet.ubs — az UBS-szótárak igehelyszintű jelentései és a fordítások.

Bemenetek: B32 (UBS görög szótár, DNTG: hivatkozások és jelentések), B33 (UBS héber szótár, DBH), B34 (a
Károli-vers masszoréta számozású megfelelője), B14 (a magyar fordítások táblája).
"""
import re

from lapgen.bemenet.konyvek import b63_konyvek
from lapgen.ertekek import DbhOk

_MT_VERS_RX = re.compile(r'^\d+:\d+$')
_USZ_IGEHELY_RX = re.compile(r'^(\S+)\s+(\d+):(\d+)(?:-(\d+))?$')
_OSZTALY_AZONOS = 'KJV'


class Forditas:
    """Egy mező magyar fordítása; az `elavult` jelzi, hogy a forrásszöveg azóta megváltozott (T5)."""
    __slots__ = ('szoveg', 'elavult')

    def __init__(self, szoveg, elavult):
        self.szoveg, self.elavult = szoveg, elavult


class Forditasok:
    def __init__(self, b, sorok):
        self._b, self._sorok = b, sorok

    def forditas(self, szotar, strong_kod, entry_id, jelentes_szam, mezo, hely):
        """A (szótár, Strong, szócikk, jelentés, mező) magyar fordítása, vagy None, ha nincs."""
        sor = self._sorok.get((szotar, strong_kod, entry_id, jelentes_szam, mezo))
        if sor is None or not sor[0]:
            return None
        return Forditas(self._b.forrasszoveg('B14', 'forditas_hu', sor[0], hely), sor[1] == 'elavult')


def b14_forditasok(b):
    """B14 — a magyar fordítások táblája; kulcs: szótár + Strong + szócikk + jelentés + mező."""
    def betolt():
        oszlopok = ('szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forditas_hu', 'allapot')
        tabla = b._tabla('B14', oszlopok=oszlopok)
        sz, st, e, j, m, f, a = (tabla.oszlop(o) for o in oszlopok)
        return Forditasok(b, {(s[sz], s[st], s[e], s[j], s[m]): (s[f], s[a]) for s in tabla.sorok})
    return b.egyszer('B14', betolt)


class UbsDntg:
    """Az UBS görög szótár: versenként és Strong-számonként a hivatkozott jelentések."""

    def __init__(self, b, hivatkozasok, jelentesek):
        self._b, self._hivatkozasok, self._jelentesek = b, hivatkozasok, jelentesek

    def lexidek(self, versek, strong_kod):
        """A versekben a Strong-számra hivatkozott jelentések azonosítói, rendezve, ismétlés nélkül."""
        return sorted({lexid for vers in versek for lexid in self._hivatkozasok.get((vers, strong_kod), ())})

    def jelentes(self, strong_kod, lexid, hely):
        """(szócikk-kód, angol glosszák) vagy None, ha a jelentés nincs a táblában."""
        sor = self._jelentesek.get((strong_kod, lexid))
        if sor is None:
            return None
        return sor[0], self._b.forrasszoveg('B32', 'glosszak', sor[1], hely)


def b32_ubs_dntg(b):
    """B32 — az UBS görög szótár (DNTG) hivatkozásai és jelentései. A jelentés doménenként ismétlődhet: az
    első sor számít."""
    def betolt():
        hiv_ut, jel_ut = b._utvonalak('B32')
        hiv = b._tabla('B32', utvonal=hiv_ut, oszlopok=('igehely', 'strong', 'lexid'))
        jel = b._tabla('B32', utvonal=jel_ut, oszlopok=('strong', 'lexid', 'entry_kod', 'glosszak'))
        i, s, x = hiv.oszlop('igehely'), hiv.oszlop('strong'), hiv.oszlop('lexid')
        hivatkozasok = {}
        for sor in hiv.sorok:
            hivatkozasok.setdefault((sor[i], sor[s]), []).append(sor[x])
        js, jx, je, jg = (jel.oszlop(o) for o in ('strong', 'lexid', 'entry_kod', 'glosszak'))
        jelentesek = {}
        for sor in jel.sorok:
            jelentesek.setdefault((sor[js], sor[jx]), (sor[je], sor[jg]))
        return UbsDntg(b, hivatkozasok, jelentesek)
    return b.egyszer('B32', betolt)


class UbsDbh:
    """Az UBS héber szótár: (Strong, masszoréta vers) szerint a hivatkozott jelentések."""

    def __init__(self, b, hivatkozasok, jelentesek):
        self._b, self._hivatkozasok, self._jelentesek = b, hivatkozasok, jelentesek

    def lexidek(self, strong_kod, mt_vers_kod):
        return sorted(set(self._hivatkozasok.get((strong_kod, mt_vers_kod), ())))

    def glosszak(self, strong_kod, lexid, hely):
        """A jelentés angol glosszái, vagy None, ha a jelentés nincs a táblában."""
        nyers = self._jelentesek.get((strong_kod, lexid))
        return None if nyers is None else self._b.forrasszoveg('B33', 'glosszak', nyers, hely)


def b33_ubs_dbh(b):
    """B33 — az UBS héber szótár (DBH) hivatkozásai és jelentései; a hivatkozás masszoréta versszámozású."""
    def betolt():
        hiv_ut, jel_ut = b._utvonalak('B33')
        hiv = b._tabla('B33', utvonal=hiv_ut, oszlopok=('strong', 'igehely', 'lexid'))
        jel = b._tabla('B33', utvonal=jel_ut, oszlopok=('strong', 'lexid', 'glosszak'))
        s, i, x = hiv.oszlop('strong'), hiv.oszlop('igehely'), hiv.oszlop('lexid')
        hivatkozasok = {}
        for sor in hiv.sorok:
            hivatkozasok.setdefault((sor[s], sor[i]), []).append(sor[x])
        js, jx, jg = (jel.oszlop(o) for o in ('strong', 'lexid', 'glosszak'))
        jelentesek = {}
        for sor in jel.sorok:
            jelentesek.setdefault((sor[js], sor[jx]), sor[jg])
        return UbsDbh(b, hivatkozasok, jelentesek)
    return b.egyszer('B33', betolt)


class Versmegfeleltetes:
    """A Károli-vers masszoréta számozású megfelelője."""

    def __init__(self, konyvek, sorok):
        self._konyvek, self._sorok = konyvek, sorok

    def mt_vers(self, vers):
        """(masszoréta vers vagy None, ok): None mellett az ok mondja meg, miért nincs biztos megfelelő."""
        sor = self._sorok.get(vers.kod)
        if sor is None:
            return None, DbhOk.NINCS_MEGFELELTETES
        mt, osztaly = sor
        if mt:
            if _MT_VERS_RX.match(mt):
                return self._konyvek.igehely(vers.konyv + ' ' + mt), None
            return None, DbhOk.NEM_EGY_VERS
        if osztaly == _OSZTALY_AZONOS:
            return vers, None
        return None, DbhOk.SZAMOZAS_ELTERES


def b34_versmegfeleltetes(b):
    """B34 — a Károli-vers és a masszoréta vers megfeleltetése."""
    def betolt():
        tabla = b._tabla('B34', oszlopok=('igehely_karoli', 'igehely_mt', 'osztaly'))
        k, m, o = (tabla.oszlop(x) for x in ('igehely_karoli', 'igehely_mt', 'osztaly'))
        return Versmegfeleltetes(b63_konyvek(b), {s[k]: (s[m].strip(), s[o]) for s in tabla.sorok})
    return b.egyszer('B34', betolt)


def usz_versek(igehely, konyvek):
    """Az újszövetségi igehely versei (egy vers vagy egy fejezeten belüli tartomány); None, ha az igehely
    nem újszövetségi, vagy az alakja más."""
    m = _USZ_IGEHELY_RX.match(igehely.kod)
    if not m or not konyvek.ujszovetsegi(igehely.konyv):
        return None
    elso = int(m.group(3))
    utolso = int(m.group(4)) if m.group(4) else elso
    return tuple('%s %s:%d' % (m.group(1), m.group(2), v) for v in range(elso, utolso + 1))
