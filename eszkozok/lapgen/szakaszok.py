"""lapgen.szakaszok — a lap szakaszmodellje: a szakaszok rendje, száma, nézete és a hozzájuk tartozó
számító és megjelenítő függvény.

Minden szakaszszám és szakaszra mutató horgony ebből a rendből jön (GK-10); a kódban máshol
szakaszszám nem áll. A még el nem készült szakasz `szamit` és `megjelenit` mezője `None`: a lap
ilyenkor részleges, és a regresszió a hiányzó szakaszt „nincs kész”-ként jelzi.
"""
from lapgen import konfig
from lapgen.szoveg import Horgony

# A lap elején álló meghatározás („Mi tartozik ide, és mi nem”) horgonya: a kritérium egyetlen teljes helye a lap
# eleje, a többi szakasz erre hivatkozik (DT-F218n). A `fej` szakasz ezt a horgonyt írja ki, a hivatkozók ezt célozzák.
KRITERIUM_HORGONY = Horgony('mi-tartozik-ide')


class SzakaszLeiro:
    __slots__ = ('azonosito', 'szamozott', 'nezet', 'szamit', 'megjelenit', 'kapu', 'sorszam')

    def __init__(self, azonosito, szamozott, szamit=None, megjelenit=None, nezet=konfig.NEZET_TUDOMANYOS):
        self.azonosito = azonosito
        self.szamozott = szamozott
        self.nezet = nezet
        self.szamit = szamit
        self.megjelenit = megjelenit
        self.kapu = None       # a szakasz kapuja a lapmodellen (pl. számegyezés); None, ha nincs
        self.sorszam = None


def _rend():
    rend = (
        SzakaszLeiro('fej', False),
        SzakaszLeiro('kivonat', False),
        SzakaszLeiro('tartalom', False),
        SzakaszLeiro('jelmagyarazat', False),
        SzakaszLeiro('dontesi_ut', True),
        SzakaszLeiro('elofordulasok', True),
        SzakaszLeiro('kizart', True),
        SzakaszLeiro('szocikkek', True),
        SzakaszLeiro('lxx', True),
        SzakaszLeiro('kereszthivatkozasok', True),
        SzakaszLeiro('kapcsolatok', True),
        SzakaszLeiro('kapcsolodo', True),
        SzakaszLeiro('hatastortenet', True),
        SzakaszLeiro('ertelmezes', True),
        SzakaszLeiro('modszertan', True),
        SzakaszLeiro('idezes', True),
        SzakaszLeiro('kolofon', False),
        SzakaszLeiro('kizarasok_melleklet', False, nezet=konfig.NEZET_KIZARASOK),
    )
    szam = 0
    for leiro in rend:
        if leiro.szamozott:
            szam += 1
            leiro.sorszam = szam
    return rend


class Szakaszrend:
    """A szakaszok rendje egy generáláshoz. A `bekot` adja meg egy szakasz két függvényét."""

    def __init__(self):
        self._rend = _rend()
        self._nev_szerint = {leiro.azonosito: leiro for leiro in self._rend}

    def bekot(self, azonosito, szamit, megjelenit, kapu=None):
        leiro = self._nev_szerint[azonosito]
        leiro.szamit, leiro.megjelenit, leiro.kapu = szamit, megjelenit, kapu

    def sorszam(self, azonosito):
        """A számozott szakasz sorszáma; számozatlan szakaszra hiba."""
        szam = self._nev_szerint[azonosito].sorszam
        if szam is None:
            raise KeyError('a(z) %s szakasz nem számozott' % azonosito)
        return szam

    def cim_kulcs(self, azonosito):
        """A szakasz címének sablonkulcsa."""
        return 'cim.' + self._nev_szerint[azonosito].azonosito

    def kesz(self, azonosito):
        """Elkészült-e (be van-e kötve) a szakasz."""
        return self._nev_szerint[azonosito].szamit is not None

    def keszek(self, nezet):
        return tuple(leiro for leiro in self._rend if leiro.nezet == nezet and leiro.szamit is not None)

    def mind(self):
        return self._rend
