"""lapgen.ismetles — az ismétlés két kapuja a kész lap látható szövegén (DT-F218n).

1. **A kritérium egyszer áll** (BUKÁS). A motívum kritériumának (a motívumtábla `negativ_kriterium` mezője)
   bármely `KRITERIUM_ABLAK` szavas részlete a látható lapon legfeljebb egyszer állhat; a teljes lapon (ha a lap
   eleje is elkészült) pontosan egyszer. A kritérium egyetlen teljes helye a lap eleje: a többi szakasz hivatkozik
   rá, nem ismétli. Ez a kapu fogja meg azt a hibát, amelyben egymásra rakódó javítások ugyanazt a szabályt több
   szakaszba is kiírták.
2. **Ismétlés-figyelő** (figyelmeztetés). Ha egy `ISMETLES_ABLAK` szavas szósor a látható lapon kétszer áll, a
   figyelő jelzi. A bibliai és a szótári idézet nem ismétlés: az ablakban legfeljebb
   `ISMETLES_IDEZET_LEGFELJEBB` idézett szó állhat. Az igehelyek felsorolása sem próza: az ablakban legfeljebb
   `ISMETLES_SZAM_LEGFELJEBB` tiszta szám állhat (a prózában álló néhány igehely ez alatt marad).

Mindkettő a kész sorok fajta-térképén fut: a megjegyzés, a szerkezeti jelölés és a horgony nem látható szöveg.
A szó: betűk és számjegyek sora, kisbetűsítve; az írásjel és a sablonmondatban álló jelölés (HTML-címke, a
Markdown kiemelése és linkje) nem számít. Az ablak egy soron belül áll (a lapon egy bekezdés egy sor).
"""
import re

from lapgen import konfig
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Fajta

_LATHATO = (Fajta.PROZA, Fajta.SABLON, Fajta.IDEZET)
_CIMKE_RX = re.compile(r'<[^>]*>')
_LINKCEL_RX = re.compile(r'\]\([^)\s]*\)')
_SZO_RX = re.compile(r'[^\W_]+')


class Szo:
    """A látható szöveg egy szava: a kisbetűs alak és az, hogy idézetben áll-e."""
    __slots__ = ('alak', 'idezett')

    def __init__(self, alak, idezett):
        self.alak, self.idezett = alak, idezett


def _jeloles_nelkul(szoveg):
    """A szöveg a jelölés nélkül, azonos hosszban: a HTML-címke és a Markdown-link célja helyén szóköz áll."""
    for rx in (_CIMKE_RX, _LINKCEL_RX):
        szoveg = rx.sub(lambda m: ' ' * len(m.group(0)), szoveg)
    return szoveg


def szavak(szoveg, idezett=False):
    """Egy szövegdarab szavai. A HTML-címke és a link célja nem szó."""
    return [Szo(m.group(0).lower(), idezett) for m in _SZO_RX.finditer(_jeloles_nelkul(szoveg))]


def sor_szavai(sor):
    """Egy kész sor látható szavai a fajta-térkép szerint, a lap rendjében. A jelölést a teljes soron keresi (a
    címke és a link célja több tartományon is átnyúlhat: a horgony külön tartomány)."""
    tiszta = _jeloles_nelkul(sor.szoveg)
    ki = []
    for kezdet, veg, fajta in sorted(sor.tartomanyok, key=lambda t: (t[0], t[1])):
        if fajta in _LATHATO:
            ki.extend(Szo(m.group(0).lower(), fajta is Fajta.IDEZET) for m in _SZO_RX.finditer(tiszta[kezdet:veg]))
    return ki


def _ablakok(szosor, meret):
    alakok = tuple(szo.alak for szo in szosor)
    return [(i, alakok[i:i + meret]) for i in range(len(alakok) - meret + 1)]


class KriteriumIsmetles:
    """A kritérium egy részlete többször áll, vagy a teljes lapról hiányzik: a részlet és a sorok sorszáma."""
    __slots__ = ('reszlet', 'sorszamok')

    def __init__(self, reszlet, sorszamok):
        self.reszlet, self.sorszamok = reszlet, sorszamok


def kriterium_egyszer(sorok, kriterium_szoveg, teljes, ablak=konfig.KRITERIUM_ABLAK):
    """A kritérium kapuja. A `kriterium_szoveg` a kritérium nyers szövege, a `teljes` azt mondja meg, hogy a lap
    eleje (a kritérium helye) elkészült-e. Visszaadja a hibákat (`KriteriumIsmetles`); üres lista: rendben.

    Az `ablak`-nál rövidebb kritérium egyetlen részletként, egészében számít."""
    kriterium = szavak(kriterium_szoveg)
    if not kriterium:
        return []
    meret = min(ablak, len(kriterium))
    keresett = {}
    for _hol, reszlet in _ablakok(kriterium, meret):
        keresett.setdefault(reszlet, [])
    for sorszam, sor in enumerate(sorok, start=1):
        for _hol, reszlet in _ablakok(sor_szavai(sor), meret):
            if reszlet in keresett:
                keresett[reszlet].append(sorszam)
    hibak = []
    for reszlet, sorszamok in keresett.items():
        if len(sorszamok) > 1 or (teljes and not sorszamok):
            hibak.append(KriteriumIsmetles(reszlet, tuple(sorszamok)))
    return hibak


def kriterium_hiba_szoveg(hibak):
    """A kapu hibaüzenete: hány részlet ismétlődik, mely sorokban, és az első részlet."""
    tobbszor = [h for h in hibak if h.sorszamok]
    hianyzik = [h for h in hibak if not h.sorszamok]
    reszek = []
    if tobbszor:
        sorszamok = sorted({n for h in tobbszor for n in h.sorszamok})
        reszek.append('a kritérium %d részlete többször áll a lapon (sorok: %s); az első: „%s”'
                      % (len(tobbszor), ', '.join(str(n) for n in sorszamok), ' '.join(tobbszor[0].reszlet)))
    if hianyzik:
        reszek.append('a kritérium %d részlete nem áll a lapon; az első: „%s”'
                      % (len(hianyzik), ' '.join(hianyzik[0].reszlet)))
    return '; '.join(reszek)


def kriterium_kapu(sorok, kriterium_szoveg, teljes):
    """A kritérium kapuja a kész lapon: hibánál BUKÁS (`KapuHiba`), a lap nem íródik ki. Kritérium nélkül
    (`None`) nincs mit ellenőrizni."""
    if kriterium_szoveg is None:
        return
    hibak = kriterium_egyszer(sorok, kriterium_szoveg, teljes)
    if hibak:
        raise KapuHiba('az ismétlés kapuja: ' + kriterium_hiba_szoveg(hibak)
                       + '. A kritérium egyetlen teljes helye a lap eleje; máshol hivatkozás álljon')


class Ismetles:
    """Egy ismétlődő szósor: a szavai és az előfordulásai (sorszám, a sorban hányadik szótól)."""
    __slots__ = ('szavak', 'helyek')

    def __init__(self, szosor, helyek):
        self.szavak, self.helyek = szosor, helyek


def ismetlesek(sorok, ablak=konfig.ISMETLES_ABLAK, idezet_legfeljebb=konfig.ISMETLES_IDEZET_LEGFELJEBB):
    """Az ismétlés-figyelő: a legalább `ablak` szavas, a lapon legalább kétszer álló szósorok, a leghosszabb
    összefüggő alakjukban. A túlnyomóan idézett ablak nem számít."""
    hol_all = {}
    soronkent = {}
    for sorszam, sor in enumerate(sorok, start=1):
        szosor = sor_szavai(sor)
        if len(szosor) < ablak:
            continue
        soronkent[sorszam] = szosor
        idezett = [1 if szo.idezett else 0 for szo in szosor]
        # Az igehelyek felsorolása (könyv, fejezet, vers) nem próza: igehelyenként két szám áll egy könyvnév
        # mellett, ezért a felsorolás 16 szavas ablakában legalább 10 szó tiszta szám. A prózában álló néhány
        # igehely (ablakonként legfeljebb négy) ez alatt marad, az ilyen ismétlést a figyelő jelzi.
        szam = [1 if szo.alak.isdigit() else 0 for szo in szosor]
        for i, reszlet in _ablakok(szosor, ablak):
            if sum(idezett[i:i + ablak]) <= idezet_legfeljebb \
                    and sum(szam[i:i + ablak]) <= konfig.ISMETLES_SZAM_LEGFELJEBB:
                hol_all.setdefault(reszlet, []).append((sorszam, i))
    # Az ismétlődő ablak a helyein együtt nyúlik tovább, amíg minden helyén ugyanaz a szó következik: így egy
    # találat a leghosszabb közös szósor, és minden találatnak legalább két helye van. A már lefedett ablak
    # (egy korábbi találat belseje, ugyanazokon a helyeken) nem ad új találatot.
    lefedett, ki = set(), []
    for reszlet, helyek in sorted(hol_all.items(), key=lambda kv: kv[1][0]):
        if len(helyek) < 2 or all(hely in lefedett for hely in helyek):
            continue
        hossz = ablak
        while True:
            kovetkezok = {soronkent[n][i + hossz].alak if i + hossz < len(soronkent[n]) else None for n, i in helyek}
            if len(kovetkezok) != 1 or None in kovetkezok:
                break
            hossz += 1
        sorszam, i = helyek[0]
        ki.append(Ismetles(tuple(szo.alak for szo in soronkent[sorszam][i:i + hossz]), tuple(helyek)))
        lefedett.update((n, j + k) for n, j in helyek for k in range(hossz - ablak + 1))
    return ki
