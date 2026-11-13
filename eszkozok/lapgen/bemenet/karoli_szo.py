"""lapgen.bemenet.karoli_szo — a Károli-fordítás magyar szavainak bemenetei (a 4.13 és a 4.14 ponthoz).

Bemenetek: B55 (a Károli-szavak szótári alakja), B53 (a funkciókapcsolók: melyik motívumon épül a két pont),
B69 (a nyelvtani szavak Strong-számai). A motívumsor Károli-szava (B03) itt bomlik szavakra.

A szótári alak összevetési kulcs: a tábla értéke kisbetűsítve (a táblában nem álló szónál maga a szó,
kisbetűsítve). A lapon ez a kisbetűs alak áll idézhető forrásszövegként, ahogy a jóváhagyott lapon is („úr”,
„ábrám”): ez nem a tábla betűre vett értéke, és a festékpróba nem látja. Hogy a lapon a tábla eredeti alakja
álljon-e, a felhasználó döntése (a 3. független ellenőrzés E2 tétele, a 218a végi listában). A szóalak a
motívumsor mezőjének egy szava, változtatás nélkül.
"""
import re

_ALAK_OSZLOPOK = ('alak', 'szotari_alak', 'szotari_alak_mai')
_KAPCSOLO_OSZLOPOK = ('kapcsolo', 'id', 'allapot')
_KAPCSOLO_KAROLI = 'KAROLI_MEGFELELOK'
_AKTIV = 'aktiv'
_SZO_RX = re.compile(r'[^\W\d_]+')
_NYELVTANI_RX = re.compile(r'H9\d{3}')
NEM_KULCSSZO = frozenset({'a', 'az', 'és'})   # a névelő és a mellérendelő kötőszó nem a motívum magyar szava


class SzotariAlakok:
    """A Károli-szavak szótári alakja (B55): a szóalakhoz a mai helyesírású szótári alak, kisbetűvel. A táblában
    nem álló szó szótári alakja maga a szó (kisbetűvel)."""

    def __init__(self, b, tabla):
        self._b, self._tabla = b, tabla

    def lemma(self, szo):
        """A szóalak szótári alakja összevetési kulcsként."""
        return self._tabla.get(szo) or self._tabla.get(szo.lower()) or szo.lower()

    def egyezik(self, szo, kulcs, maradek):
        """A szóalak a kulcsszóval egyezik: azonos a szótári alakja, vagy a szóalak, illetve a szótári alak a
        kulcsszóval kezdődik, és utána legfeljebb `maradek` betű áll („hívám”, „hívnám” → „hív”)."""
        lemma = self.lemma(szo)
        if lemma == kulcs:
            return True
        return any(x.startswith(kulcs) and len(x) - len(kulcs) <= maradek for x in (lemma, szo.lower()))

    def idezheto(self, kulcs):
        """A szótári alak idézhető forrásszövegként."""
        return self._b.forrasszoveg('B55', 'szotari_alak', kulcs, kulcs)


def b55_szotari_alakok(b):
    """B55 — a Károli-szavak szótári alakjai."""
    def betolt():
        tabla = b._tabla('B55', oszlopok=_ALAK_OSZLOPOK)
        a, sz, m = (tabla.oszlop(o) for o in _ALAK_OSZLOPOK)
        return SzotariAlakok(b, {sor[a]: (sor[m] or sor[sz] or sor[a]).lower() for sor in tabla.sorok
                                 if len(sor) > m})
    return b.egyszer('B55', betolt)


def b53_karoli_pontok(b, motivum):
    """B53 — épül-e a motívumon a Károli-megfelelők két pontja. A funkció motívumonként jóváhagyott: csak a
    motívum saját sora kapcsolja be, a minden motívumra szóló (`*`) sor nem (a régi szabály szerint)."""
    tabla = b._tabla('B53', oszlopok=_KAPCSOLO_OSZLOPOK)
    return any(r['kapcsolo'] == _KAPCSOLO_KAROLI and r['allapot'] == _AKTIV and r['id'] == motivum.kod
               for r in tabla.szotarak())


class Nyelvtani:
    """A nyelvtani szavak (névelő, elöljáró, tárgyjel, toldalék-morféma) Strong-számai (B69)."""

    def __init__(self, strongok):
        self._strongok = strongok

    def __contains__(self, strong_kod):
        return strong_kod in self._strongok or bool(_NYELVTANI_RX.fullmatch(strong_kod))


def b69_nyelvtani(b):
    """B69 — a nyelvtani szavak Strong-számai."""
    def betolt():
        tabla = b._tabla('B69', oszlopok=('strong',))
        s = tabla.oszlop('strong')
        return Nyelvtani(frozenset(sor[s] for sor in tabla.sorok if sor))
    return b.egyszer('B69', betolt)


def szavak(szoveg):
    """Egy magyar szöveg szavai, ahogy állnak, sorrendben (az írásjel és a kihagyásjel nélkül)."""
    return _SZO_RX.findall(szoveg or '')


def szoalak(b, szo):
    """A motívumsor Károli-szavának egy szava idézhető forrásszövegként (a szó változtatás nélkül áll)."""
    return b.forrasszoveg('B03', 'karoli_szo', szo, szo)


def kotelezo_karoli_szo(sorok):
    """Van-e a motívum sorai között Károli-szóval álló sor (nélküle a két pont nem épül)."""
    return any(s.karoli_szo is not None and szavak(s.karoli_szo.ertek) for s in sorok)
