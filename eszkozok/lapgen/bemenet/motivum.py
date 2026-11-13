"""lapgen.bemenet.motivum — a motívum saját sora, a szavak rövid jelentése és a kézi forrás nyitott kérdései.

Bemenetek: B02 (a motívumok táblája: cím, negatív kritérium, fölérendelt fogalom), B15 (a héber szavak rövid magyar
jelentése), B14 (a görög szavak rövid magyar jelentése a fordítástáblából), B47 (a rések forrásjegyzéke és a motívum
kézi forrása).

A negatív kritérium kézi próza: a réteg csak szerkezetileg bontja két részre (ami ide tartozik; ami nem), a szöveget
nem írja át. A kézi forrásból a vitatott pontok és a nyitott kérdések címe és első mondata szó szerinti részletként
jön (a forrás nézete).
"""
import re

from lapgen.bemenet import szavak
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.bemenet.ubs import b14_forditasok

_MOTIVUM_OSZLOPOK = ('id', 'cim', 'negativ_kriterium', 'folerendelt_fogalom')
_NEM_TARTOZIK = 'Nem tartozik ide'
_MONDATVEG = '.'
_GLOSSZA_OSZLOPOK = ('strong', 'fo', 'glossza_hu', 'glossza_en')
_FO = 'igen'
_SZOTAR_TBESG, _ROVID, _GLOSSZA_MEZO = 'TBESG', 'rovid', 'glosszak_hu'
_RES_OSZLOPOK = ('id', 'res', 'forras', 'tanulmany')
_RES_KEZI = 'tanulmany'
_RES_ERTELMEZES, _RES_MODSZERTAN = 'ertelmezes', 'modszertan'
_RES_RX = r'(?ms)^<!-- RÉS-KEZDET: %s -->\s*\n(.*?)^<!-- RÉS-VÉGE: %s -->'
_VITATOTT_RX = re.compile(r'(?ms)^### ⚠️ Vitatott pontok\s*\n(.*?)(?=^### |\Z)')
_VITATOTT_TETEL_RX = re.compile(r'(?m)^(\*\*[^*]+?\.?\*\*\s+[^.!?]+[.!?])')
_NYITOTT_RX = re.compile(r'(?ms)^### Nyitott kérdések[^\n]*\n(.*?)(?=^### |\Z)')
_NYITOTT_TETEL_RX = re.compile(r'(?m)^\d+\.\s+(\*\*[^*]+?\.?\*\*\s+[^.!?]+[.!?])')


class MotivumSor:
    """A motívum sora: a cím, a negatív kritérium két része (ami ide tartozik; ami nem) és a fölérendelt fogalom,
    kézi prózaként. A hiányzó rész None."""
    __slots__ = ('cim', 'ide_tartozik', 'nem_tartozik', 'folerendelt')

    def __init__(self, cim, ide_tartozik, nem_tartozik, folerendelt):
        self.cim, self.ide_tartozik, self.nem_tartozik, self.folerendelt = cim, ide_tartozik, nem_tartozik, folerendelt


def b02_motivum(b, motivum):
    """B02 — a motívum sora. A cím és a fölérendelt fogalom a mondatzáró pont nélkül áll az adatban (a pontot a
    sablonmondat teszi ki): ha ponttal végződik, BemenetHiba (a réteg nem vág le a szövegből)."""
    tabla = b._tabla('B02', oszlopok=_MOTIVUM_OSZLOPOK)
    sorok = [r for r in tabla.szotarak() if r['id'] == motivum.kod]
    if len(sorok) != 1:
        raise BemenetHiba('B02: a motívumnak pontosan egy sora legyen (%s: %d)' % (motivum.kod, len(sorok)))
    sor = sorok[0]
    cim, kriterium, fol = sor['cim'].strip(), sor['negativ_kriterium'].strip(), sor['folerendelt_fogalom'].strip()
    if not cim:
        raise BemenetHiba('B02: üres cím (%s)' % motivum.kod)
    for nev, ertek in (('cim', cim), ('folerendelt_fogalom', fol)):
        if ertek.endswith(_MONDATVEG):
            raise BemenetHiba('B02: a `%s` mező ponttal végződik (%s): a pontot a lap mondata teszi ki, az adatban '
                              'ne álljon' % (nev, motivum.kod))
    eleje, elvalaszto, tobbi = kriterium.partition(_NEM_TARTOZIK)
    return MotivumSor(
        cim=b.kezi('B02', 'cim', cim),
        ide_tartozik=b.kezi('B02', 'negativ_kriterium', eleje.strip()) if eleje.strip() else None,
        nem_tartozik=b.kezi('B02', 'negativ_kriterium', elvalaszto + tobbi) if elvalaszto else None,
        folerendelt=b.kezi('B02', 'folerendelt_fogalom', fol) if fol else None)


def kriterium_szoveg(b, motivum):
    """A motívum kritériumának teljes szövege (B02, `negativ_kriterium`), a két rész egyben; üres mezőnél None.
    A kritérium kapuja kapja (lapgen.ismetles): látható szöveg ebből az értékből nem lesz."""
    sor = b02_motivum(b, motivum)
    reszek = [resz.ertek for resz in (sor.ide_tartozik, sor.nem_tartozik) if resz is not None]
    return ' '.join(reszek) if reszek else None


class Rovid:
    """Egy szó rövid jelentése: a magyar szöveg, vagy magyar híján az angol eredeti (fordításra vár). Mindkettő
    hiánya: a szótárnak nincs rövid jelentése a szóra. Az `elavult` jelzi, hogy a magyar fordítás forrása azóta
    megváltozott (T5)."""
    __slots__ = ('magyar', 'angol', 'elavult')

    def __init__(self, magyar, angol, elavult=False):
        self.magyar, self.angol, self.elavult = magyar, angol, elavult


class RovidJelentes:
    """A szavak rövid jelentése egy úton (GK-16): héberül a héber glosszatábla fő sora, görögül a fordítástábla
    rövid glosszája; magyar híján a forrás angol szava áll, kimondott hiányként."""

    def __init__(self, b, heber, forditasok, angol):
        self._b, self._heber, self._forditasok, self._angol = b, heber, forditasok, angol

    def jelentes(self, strong):
        """A szó rövid jelentése (`Rovid`): a magyar szöveg, vagy az angol eredeti, vagy egyik sem."""
        if strong.heber:
            magyar, angol = self._heber.get(strong.kod, ('', ''))
            if magyar:
                return Rovid(self._b.forrasszoveg('B15', 'glossza_hu', magyar, strong), None)
            return Rovid(None, self._b.forrasszoveg('B15', 'glossza_en', angol, strong) if angol else None)
        forditas = self._forditasok.forditas(_SZOTAR_TBESG, strong.kod, strong.kod, _ROVID, _GLOSSZA_MEZO, strong)
        if forditas is not None:
            return Rovid(forditas.szoveg, None, forditas.elavult)
        angol = self._angol.get(strong.kod)
        return Rovid(None, self._b.forrasszoveg('B10', 'rovid_angol', angol, strong) if angol else None)

    def magyar(self, strong):
        """A szó rövid magyar jelentése, vagy None (angol szöveg innen nem jön)."""
        return self.jelentes(strong).magyar


def b15_heber_glosszak(b):
    """B15 — a héber szavak rövid jelentése (a tábla fő sora: `fo` = igen): {Strong: (magyar, angol)}."""
    def betolt():
        tabla = b._tabla('B15', oszlopok=_GLOSSZA_OSZLOPOK)
        s, f, g, e = (tabla.oszlop(o) for o in _GLOSSZA_OSZLOPOK)
        return {sor[s]: (sor[g], sor[e]) for sor in tabla.sorok if sor[f] == _FO}
    return b.egyszer('B15', betolt)


def rovid_jelentes(b):
    """A rövid jelentés szolgáltatása a munkamenethez (egy út a héber és a görög szóra)."""
    return b.egyszer('rovid_jelentes', lambda: RovidJelentes(b, b15_heber_glosszak(b), b14_forditasok(b),
                                                             szavak.b10_lemmak(b)[2]))


def b47_nyitott_kerdesek(b, motivum):
    """B47 — a motívum kézi forrásának vitatott pontjai és nyitott kérdései: mindegyikből a félkövér cím és az első
    mondat, szó szerinti részletként (kézi próza), a forrás rendjében: előbb az `ertelmezes` rés „Vitatott pontok”
    pontjai, azután a `modszertan` rés „Nyitott kérdések” listája.

    A rések forrását a forrásjegyzék mondja meg: csak a kézi forrásból jövő rés számít, és a jegyzékben álló útvonal
    a motívum kézi forrása kell legyen (más útvonal BemenetHiba). Hiányzó rés vagy pont nem hiba: üres eredmény."""
    jegyzek_ut, forras_ut = b._utvonalak('B47', motivum)
    tabla = b._tabla('B47', utvonal=jegyzek_ut, oszlopok=_RES_OSZLOPOK)
    resek = {r['res']: r for r in tabla.szotarak() if r['id'] == motivum.kod}
    ki = []
    for res, blokk_rx, tetel_rx in ((_RES_ERTELMEZES, _VITATOTT_RX, _VITATOTT_TETEL_RX),
                                    (_RES_MODSZERTAN, _NYITOTT_RX, _NYITOTT_TETEL_RX)):
        sor = resek.get(res)
        if sor is None or sor['forras'] != _RES_KEZI:
            continue
        if sor['tanulmany'] != forras_ut:
            raise BemenetHiba('B47: a(z) %s rés forrása (%s) nem a motívum kézi forrása (%s)'
                              % (res, sor['tanulmany'], forras_ut))
        szoveg = b._szoveg('B47', utvonal=forras_ut)
        torzs = re.search(_RES_RX % (re.escape(res), re.escape(res)), szoveg)
        blokk = blokk_rx.search(torzs.group(1)) if torzs else None
        for reszlet in (tetel_rx.findall(blokk.group(1)) if blokk else ()):
            ki.append(b.kezi('B47', 'nyitott_kerdes', reszlet.strip()))
    return tuple(ki)
