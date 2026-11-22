"""A teljes lap kapui (S9b): GK-11 (nincs globális állapot), GK-24 (alakosztály-kapu, típus szerint), GK-25 futásidejű
része (szerkezeti kapu), GK-26 (mutációs próba), GK-31 (futásidő), és a hibanapló S9-re hagyott példányai a teljes
lapon (HN-02, 04, 05, 06, 07, 08, 09).

A mutációs próba a kész lap sorait rontja el (a fajta-térképpel együtt), és megnézi, melyik kapu fogja meg; a
jelentés kapunként a teszt hibaüzenetében áll, ha egy változatot egyik sem fogja meg.
"""
import datetime
import re
import time
import unittest

import kozos
import teszt_vaz
from kozos import MINTALAPOK
from lapgen import alakosztaly, fo, ismetles, konfig, szerkezet
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.megjelenites.md.iro import KeszSor, MEGJEGYZES, lap_szoveg
from lapgen.szoveg import Fajta, MotivumId

DATUM = datetime.date(2026, 11, 13)
FUTASIDO_HATAR = 60.0   # a brief 5. pontja: egy lap generálása legfeljebb 60 s (a régi 46,5 s; 1,5-szeres túllépés megállás)
_LAPOK = {}


def _lap(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM)
    return _LAPOK[azonosito]


def _szoveg(eredmeny):
    return {nezet: lap_szoveg(sorok) for nezet, sorok in eredmeny.nezetek.items()}


# --- a mutációk: a kész sor módosítása a fajta-térkép megtartásával ---------------------------------------------

def _beszur(sor, hol, szoveg, fajta):
    """A sorba a `hol` pozíción `szoveg` kerül, a megadott fajtával; a később kezdődő tartományok eltolódnak."""
    tartomanyok = []
    for k, v, f in sor.tartomanyok:
        if v <= hol:
            tartomanyok.append((k, v, f))
        elif k >= hol:
            tartomanyok.append((k + len(szoveg), v + len(szoveg), f))
        else:   # a beszúrás a tartomány belsejébe esik: két részre bomlik
            tartomanyok.extend([(k, hol, f), (hol + len(szoveg), v + len(szoveg), f)])
    tartomanyok.append((hol, hol + len(szoveg), fajta))
    return KeszSor(sor.szoveg[:hol] + szoveg + sor.szoveg[hol:], tuple(sorted(tartomanyok)))


def _csere(sor, kezdet, veg, szoveg, fajta):
    """A sor [kezdet, vég) része helyére `szoveg` kerül a megadott fajtával."""
    torolt = KeszSor(sor.szoveg[:kezdet] + sor.szoveg[veg:], tuple(
        (k if k <= kezdet else max(kezdet, k - (veg - kezdet)), v if v <= kezdet else max(kezdet, v - (veg - kezdet)), f)
        for k, v, f in sor.tartomanyok if not (kezdet <= k and v <= veg)))
    return _beszur(torolt, kezdet, szoveg, fajta)


def _elso(sorok, feltetel):
    return next(i for i, s in enumerate(sorok) if feltetel(s))


def _fajta_tartomany(sor, fajta):
    return next((k, v) for k, v, f in sor.tartomanyok if f is fajta and v - k > 3)


def _mutaciok(sorok):
    """A hat hibaváltozat (név → elrontott sorok)."""
    sorok = list(sorok)
    ki = {}

    def valtozat(i, uj):
        s = list(sorok)
        s[i] = uj
        return tuple(s)

    # 1. szivárgó mezőnév egy sablonmondatban
    i = _elso(sorok, lambda s: any(f is Fajta.SABLON and v - k > 3 for k, v, f in s.tartomanyok))
    k, _v = _fajta_tartomany(sorok[i], Fajta.SABLON)
    ki['szivárgó mezőnév'] = valtozat(i, _beszur(sorok[i], k, 'negativ_kriterium ', Fajta.SABLON))
    # 2. ismételt címke a 3. szakasz egy indok-cellájában (HN-02 alakja)
    i = _elso(sorok, lambda s: s.szoveg.startswith('| ') and 'Más szó áll a versben, nem a motívum lexémája: ' in s.szoveg)
    hol = sorok[i].szoveg.index('Más szó áll a versben, nem a motívum lexémája: ')
    cimke = 'A formula nincs a versben: Nincs meg a formula a versben, a szó önállóan áll'
    ki['ismételt címke'] = valtozat(i, _csere(sorok[i], hol, len(sorok[i].szoveg) - 2, cimke, Fajta.PROZA))
    # 3. tört írásjel egy kézi prózában
    i = _elso(sorok, lambda s: any(f is Fajta.PROZA and v - k > 3 for k, v, f in s.tartomanyok))
    k, v = _fajta_tartomany(sorok[i], Fajta.PROZA)
    ki['tört írásjel'] = valtozat(i, _beszur(sorok[i], v, ',;', Fajta.PROZA))
    # 4. jegyzet = cella: a 3. szakasz első jegyzete a sora „Miért került a vizsgálatba” cellájával azonos
    j = _elso(sorok, lambda s: s.szoveg.startswith('- <span class="lj-szam" id="j-3-'))
    azon = re.search(r'id="j-(3-\d+)"', sorok[j].szoveg).group(1)
    r = _elso(sorok, lambda s: s.szoveg.startswith('| ') and ('href="#j-%s"' % azon) in s.szoveg)
    cella = re.split(r' \| ', sorok[r].szoveg)[1]
    cella = re.sub(r'<sup.*?</sup>', '', cella)
    eleje = sorok[j].szoveg.index('</span>') + len('</span>')
    vege = sorok[j].szoveg.index('<!--') if '<!--' in sorok[j].szoveg else len(sorok[j].szoveg)
    ki['jegyzet = cella'] = valtozat(j, _csere(sorok[j], eleje, vege, cella, Fajta.SABLON))
    # 5. belső szám (döntésszám) a mondatban
    i = _elso(sorok, lambda s: any(f is Fajta.SABLON and v - k > 3 for k, v, f in s.tartomanyok))
    k, v = _fajta_tartomany(sorok[i], Fajta.SABLON)
    ki['belső szám a mondatban'] = valtozat(i, _beszur(sorok[i], v, ' (DT872)', Fajta.SABLON))
    # 6. hiányzó „Funkció:” sor a 2.1 pontban
    i = _elso(sorok, lambda s: s.szoveg.startswith('Funkció: '))
    ki['hiányzó „Funkció:”'] = tuple(sorok[:i] + sorok[i + 1:])
    return ki


def _kapuk(sorok, kriterium):
    """A kész lap kapui: (név, függvény) — mindegyik BemenetHiba-t dob hibánál."""
    return (('alakosztály (GK-24)', lambda: alakosztaly.kapu({'TUDOMANYOS': sorok})),
            ('szerkezet (GK-25)', lambda: szerkezet.kapu({'TUDOMANYOS': sorok})),
            ('kritérium (DT872)', lambda: ismetles.kriterium_kapu(sorok, kriterium, teljes=True)))


class Allapot(unittest.TestCase):
    def test_gk11_nincs_globalis_allapot(self):
        """GK-11: a két mintalap fordított sorrendben generálva bájtra azonos (egy folyamatban)."""
        elore = {a: _szoveg(_lap(a)) for a in MINTALAPOK}
        hatra = {a: _szoveg(fo.lap_keszit(kozos.GYOKER, MotivumId(a), datum=DATUM)) for a in reversed(MINTALAPOK)}
        self.assertEqual(elore, hatra)


class Alakosztaly(unittest.TestCase):
    def test_gk24_nulla_talalat_mindket_lapon(self):
        """GK-24: a sablon-eredetű szövegen minden alakosztály, a prózán a belső jelölések, az idézeten a proveniencia
        tilos; mindkét mintalap minden nézetén 0 találat (ez egyben a kalibrálás: 0 hamis találat a prózán és az
        idézeten)."""
        for azonosito in MINTALAPOK:
            for nezet, sorok in _lap(azonosito).nezetek.items():
                self.assertEqual(alakosztaly.talalatok(sorok), [], '%s %s' % (azonosito, nezet))

    def test_gk24_a_kapu_fajta_szerint_dont(self):
        """Ugyanaz az alak a megjegyzésben megengedett, a sablonban nem; az idézetben csak a proveniencia tilos."""
        sor = KeszSor('x DT872 y', ((0, 2, Fajta.SABLON), (2, 7, MEGJEGYZES), (7, 9, Fajta.SABLON)))
        self.assertEqual(alakosztaly.talalatok([sor]), [])
        sor = KeszSor('x DT872 y', ((0, 9, Fajta.SABLON),))
        self.assertEqual([t[2] for t in alakosztaly.talalatok([sor])], ['döntésszám'])
        sor = KeszSor('a .tsv fájl és DT872', ((0, 20, Fajta.IDEZET),))
        self.assertEqual(alakosztaly.talalatok([sor]), [])
        sor = KeszSor('scope=x', ((0, 7, Fajta.IDEZET),))
        self.assertEqual([t[2] for t in alakosztaly.talalatok([sor])], ['proveniencia-mező'])


class Szerkezet(unittest.TestCase):
    def test_gk25_nulla_hiba_mindket_lapon(self):
        for azonosito in MINTALAPOK:
            for nezet, sorok in _lap(azonosito).nezetek.items():
                self.assertEqual(szerkezet.hibak(sorok), [], '%s %s' % (azonosito, nezet))


class Mutacio(unittest.TestCase):
    def test_gk26_mind_a_hat_hibavaltozatot_megfogja_egy_kapu(self):
        """GK-26: hat hibaváltozat (szivárgó mezőnév, ismételt címke, tört írásjel, jegyzet = cella, belső szám a
        mondatban, hiányzó „Funkció:”); mindet megfogja legalább egy kapu. Az ép lapon egyik kapu sem jelez."""
        from lapgen import bemenet
        from lapgen.bemenet import motivum as motivum_be
        azonosito = 'HAMART-001'
        sorok = _lap(azonosito).nezetek['TUDOMANYOS']
        kriterium = motivum_be.kriterium_szoveg(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito))
        for nev, kapu in _kapuk(sorok, kriterium):
            kapu()   # az ép lapon nem jelez
        jelentes, megfogatlan = {}, []
        for valtozat, elrontott in _mutaciok(sorok).items():
            fogo = []
            for nev, kapu in _kapuk(elrontott, kriterium):
                try:
                    kapu()
                except BemenetHiba:
                    fogo.append(nev)
            jelentes[valtozat] = fogo
            if not fogo:
                megfogatlan.append(valtozat)
        self.assertEqual(len(jelentes), 6)
        self.assertEqual(megfogatlan, [], 'jelentés kapunként: %r' % jelentes)


class Futasido(unittest.TestCase):
    def test_gk31_futasido(self):
        """GK-31: egy lap generálása legfeljebb 60 s (a régi generátor 46,5 s; 1,5-szeres túllépés megállás)."""
        for azonosito in MINTALAPOK:
            kezdet = time.monotonic()
            fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM)
            ido = time.monotonic() - kezdet
            self.assertLessEqual(ido, FUTASIDO_HATAR, '%s: %.1f s' % (azonosito, ido))


def _hn_talalatok(hnek):
    ki = []
    for azonosito in MINTALAPOK:
        szoveg = teszt_vaz._lathato_szoveg(azonosito)
        ki.extend((azonosito, hn, m.group(0)) for hn in hnek for minta, _r in teszt_vaz.HN_MINTAK[hn]
                  for m in re.finditer(minta, szoveg))
    return ki


class Hibanaplo(unittest.TestCase):
    """A hibanapló S9-re hagyott példányai a teljes lapon (a minták: `teszt_vaz.HN_MINTAK`)."""

    def test_hn02_hn04_cimke_ismetles_es_belso_mezonev(self):
        """HN-02, HN-04: címke-ismétlés és belső mezőnév („hivatkozas_kezi,;”, „negativ_kriterium”): 0 találat."""
        self.assertEqual(_hn_talalatok(('HN-02', 'HN-04')), [])

    def test_hn05_hn06_munkaszereplo_es_gerinc(self):
        """HN-05, HN-06: „felhasználó”, „orkesztrátor”, „gerinc” a látható szövegben: 0 találat."""
        self.assertEqual(_hn_talalatok(('HN-05', 'HN-06')), [])

    def test_hn07_hn08_hn09_belso_szam_es_nyers_szotarfej(self):
        """HN-07, HN-08, HN-09: töredék („sz<n> sorok,;”), döntésszám és tételszám, nyers BDB-fej, héber
        számláló: 0 találat mindkét új lapon."""
        self.assertEqual(_hn_talalatok(('HN-07', 'HN-08', 'HN-09')), [])

    def test_hn03_forrasnev_a_mondat_kozepen(self):
        """HN-03 (DT925 (2) (a)): forrásnév a mondat közepén, zárójelben („(a BDB-szótár szerint) a …”): 0 találat
        mindkét új lapon; a sor végén álló jegyzék-megjegyzés nem találat (a minta próbája)."""
        self.assertEqual(_hn_talalatok(('HN-03',)), [])
        minta = teszt_vaz.HN_MINTAK['HN-03'][0][0]
        self.assertIsNone(re.search(minta, '- BDB (Brown–Driver–Briggs, 1906) (a BDB-szótár, közkincs)\n'))
        self.assertIsNotNone(re.search(minta, 'alapjelentés: bűn *(a STEPBible rövid szótára szerint)*\n'))


if __name__ == '__main__':
    unittest.main(verbosity=1)
