"""Az „5. LXX-fordítói döntések” szakasz és a 4.6 (LXX-híd) modellje (S4): a versenkénti ítélet a valós adaton.

A HAMART-001 mai lapjának 5. szakasza 48 vers; az ítéletek és az összesítés a régi `lxx_osszevetes` +
`_lxx_ujraminosit` eredményével egyeznek (egyező 7, szócsalád 6, eltérő 1, nincs újszövetségi pár 20, a megfelelő
nincs megállapítva 13, versszámozás miatt nem párosítva 1).
"""
import unittest

import kozos
from lapgen import bemenet
from lapgen.bemenet import lxx as lxx_be
from lapgen.szamitas import lxx as LX
from lapgen.szamitas import szocikkek as SZ
from lapgen.szoveg import MotivumId, kiiras

_MODELL = {}


def modell(azonosito):
    if azonosito not in _MODELL:
        b = bemenet.Bemenet(kozos.GYOKER)
        _MODELL[azonosito] = LX.osszevetes(SZ._Forrasok(b, MotivumId(azonosito)))
    return _MODELL[azonosito]


def _sor(m, vers):
    return next(s for s in m.sorok if s.vers.kod == vers)


class Osszevetes(unittest.TestCase):
    def test_az_osszesites_a_regi_lappal_egyezik(self):
        m = modell('HAMART-001')
        self.assertEqual(len(m.sorok), 48)
        self.assertEqual(m.szamlalo, LX.Szamlalo(egyezo=7, szocsalad=6, eltero=1, nincs_par=20, minusz=0,
                                                 fuggoben=13, szamozas=1))
        self.assertEqual([s.kod for s in m.par_szavak], ['H0779', 'H7843'])

    def test_egy_merce_a_szavankenti_osszeg_az_osszesites(self):
        """A 4.6 szavankénti számai ugyanabból az ítéletsorból jönnek (egyszavas soroknál az összeg a teljes)."""
        m = modell('HAMART-001')
        for it in LX.Itelet:
            if it is LX.Itelet.FUGGOBEN:
                continue   # a tematikus (szó nélküli) sorok ítélete egy szóhoz sem tartozik
            self.assertEqual(sum(getattr(sz.szamlalo, it.value) for sz in m.szavankent),
                             getattr(m.szamlalo, it.value), it)

    def test_jellemzo_sorok(self):
        m = modell('HAMART-001')
        # a 4.11 társítása: szócsalád (καταράομαι ↔ ἐπικατάρατος), „(társítás)” jellel
        s = _sor(m, '1Móz 5:29')
        self.assertEqual((s.itelet, s.gorog.fajta), (LX.Itelet.SZOCSALAD, LX.GorogFajta.TARSITAS))
        # hídszó: a sáchat a versben (a chámász sora helyett), a fordítói döntés helyett a társítás
        s = _sor(m, '1Móz 6:13')
        self.assertTrue(lxx_be.ekezet_nelkul(kiiras(s.heber.alak).szoveg).startswith('משחית'))
        # a versszámozás eltérése: nincs LXX-igehely
        s = _sor(m, 'Jer 51:46')
        self.assertEqual((s.itelet, s.lxx), (LX.Itelet.SZAMOZAS, None))
        # az eltérő LXX-számozás jelölt
        self.assertEqual(_sor(m, 'Zsolt 14:1').lxx, LX.LxxHely(13, 1, True))
        # a kiejtés-pótlás a szakaszban először álló alakon
        self.assertIsNotNone(_sor(m, '1Móz 3:14').gorog.alak_kiejtes)
        self.assertIsNone(_sor(m, '1Móz 3:17').gorog.alak_kiejtes)

    def test_lxx_minusz_az_istentisztelet_lapon(self):
        m = modell('ISTENTISZT-001')
        s = _sor(m, 'Zsolt 116:17')
        self.assertEqual((s.itelet, s.gorog.fajta), (LX.Itelet.MINUSZ, LX.GorogFajta.MINUSZ))
        self.assertEqual(s.lxx, LX.LxxHely(115, 8, True))

    def test_ekezet_nelkuli_kulcs(self):
        self.assertEqual(lxx_be.ekezet_nelkul('Ἐπικατάρατος'), 'επικαταρατος')
        self.assertEqual(lxx_be.lxx_vers('Psalms (LXX) 13:1'), (13, 1))
        self.assertIsNone(lxx_be.lxx_vers('Psalms'))


class ALapon(unittest.TestCase):
    """Az 5. szakasz és a 4.6 a kész lapon (a HAMART-001 sorait a regresszió méri bájtra; itt az ISTENTISZT-001)."""

    def test_az_istentisztelet_lap_otodik_szakasza(self):
        from lapgen import fo, konfig
        sorok = [s.szoveg for s in fo.lap_keszit(kozos.GYOKER, MotivumId('ISTENTISZT-001')).nezetek[
            konfig.NEZET_TUDOMANYOS]]
        self.assertIn('| Zsolt 116:17 | Zsolt(LXX) 115:8 | אֶקְרָֽא (ekrá) | nincs megfelelő a görögben (LXX-minusz) '
                      '| LXX-minusz |', sorok)
        # N196 (b), szerkesztői döntés (2026-11-23): az 1Kir 18:24 a több lemmás társítás részenkénti szűrésével egyező
        self.assertIn('*Összesítés: egyező=13, ugyanaz a szócsalád=2, eltérő=0, nincs újszövetségi pár=0, LXX-minusz=1, '
                      'a megfelelő nincs megállapítva=0, versszámozás miatt nem párosítva=0.*', sorok)
        self.assertEqual(sum(1 for s in sorok if s == '#### 4.6. LXX-híd'), 2)


class Gk04(unittest.TestCase):
    """GK-04, az `lxx_egyezes` része (a teszt_vaz.py-ból): a kapu a modellen fut, mindkét mintalapon. A `hely_egyseg`
    része a teszt_vaz.py-ban maradt (N-tétel); a melléklet-kapu és a teljesség-mérés frissességi kapuja kész
    (`teszt_dontes.py`)."""

    def test_a_ket_mintalap_atmegy_a_kapukon(self):
        """A kapuk a lap készítésekor futnak; mindkét mintalap elkészül (a szópáros ISTENTISZT-001 is)."""
        from lapgen import fo, konfig
        for azonosito in kozos.MINTALAPOK:
            self.assertIn(konfig.NEZET_TUDOMANYOS, fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito)).nezetek)

    def test_lxx_egyezes_kapu(self):
        sz = LX.Szamlalo(egyezo=4, szocsalad=2, eltero=1, nincs_par=3, minusz=0, fuggoben=0, szamozas=0)   # 10 vers
        def m(n):
            return LX.SzoMondat(None, LX.Szamlalo(egyezo=0, szocsalad=0, eltero=0, nincs_par=n, minusz=0, fuggoben=0,
                                                  szamozas=0), False)
        motivum = MotivumId('X-001')
        LX.egyezes_kapu((m(6), m(4)), sz, False, motivum)            # egyes szavas: az összeg a versek száma
        with self.assertRaises(LX.KapuHiba):
            LX.egyezes_kapu((m(6), m(5)), sz, False, motivum)
        LX.egyezes_kapu((m(10), m(10)), sz, True, motivum)           # szópáros: minden tag minden versben
        with self.assertRaises(LX.KapuHiba):
            LX.egyezes_kapu((m(10), m(9)), sz, True, motivum)
        with self.assertRaises(LX.KapuHiba):
            LX.egyezes_kapu((m(5), m(5)), sz, True, motivum)        # szópárnál az összeg nem mérce


def _sz(egyezo=0, szocsalad=0, eltero=0, nincs_par=0, fuggoben=0):
    return LX.Szamlalo(egyezo=egyezo, szocsalad=szocsalad, eltero=eltero, nincs_par=nincs_par, minusz=0,
                       fuggoben=fuggoben, szamozas=0)


class Kuszobok(unittest.TestCase):
    """A 6. ellenőrzés E5 tétele: a híd fokozata és a szavankénti következtetés a modellben, a küszöbök a konfigban."""

    def test_hid_fok_a_konfig_kuszobeivel(self):
        from lapgen import konfig
        self.assertIsNone(LX.hid_fok(_sz(nincs_par=5)))
        n = 100
        eros = round(konfig.LXX_HID_EROS * n)
        reszleges = round(konfig.LXX_HID_RESZLEGES * n)
        self.assertIs(LX.hid_fok(_sz(egyezo=eros, eltero=n - eros)), LX.HidFok.EROS)
        self.assertIs(LX.hid_fok(_sz(egyezo=eros - 1, eltero=n - eros + 1)), LX.HidFok.RESZLEGES)
        self.assertIs(LX.hid_fok(_sz(szocsalad=reszleges, eltero=n - reszleges)), LX.HidFok.RESZLEGES)
        self.assertIs(LX.hid_fok(_sz(szocsalad=reszleges - 1, eltero=n - reszleges + 1)), LX.HidFok.GYENGE)

    def test_szavankenti_kovetkeztetes_a_konfig_kuszobeivel(self):
        from lapgen import konfig
        n = konfig.LXX_SZO_MIN
        a = -(-konfig.LXX_SZO_ARANY * n // 1)   # felfelé kerekítve: a küszöböt épp elérő szám
        self.assertTrue(LX.szo_kovetkeztetes(_sz(egyezo=int(a), eltero=n - int(a)), True))
        self.assertFalse(LX.szo_kovetkeztetes(_sz(egyezo=int(a), eltero=n - int(a)), False))      # pár nélkül nincs
        self.assertFalse(LX.szo_kovetkeztetes(_sz(egyezo=n - 1), True))                          # kevés vers
        self.assertFalse(LX.szo_kovetkeztetes(_sz(egyezo=int(a) - 1, eltero=n - int(a) + 1), True))

    def test_a_fokozatok_kulonboznek(self):
        """A célzott újraellenőrzés U1 tétele: az enum tagjai nem egyenlők egymással (nincs dataclass-dekorátor)."""
        self.assertNotEqual(LX.HidFok.EROS, LX.HidFok.GYENGE)
        self.assertEqual(len({LX.HidFok.EROS, LX.HidFok.RESZLEGES, LX.HidFok.GYENGE}), 3)

    def test_a_hamart_lap_foka(self):
        self.assertIs(modell('HAMART-001').fok, LX.HidFok.EROS)   # 13/14 a párral bíró versekben


class NemaAgak(unittest.TestCase):
    """A 6. ellenőrzés E7 tétele: a régi lánctól eltérő néma ágak kimondott hibával állnak meg."""

    def test_hibas_alaku_dontesmezo(self):
        from lapgen.bemenet.jegyzek import BemenetHiba
        r = {'igehely': '1Móz 1:1'}
        lxx_be._alak_kapu(r, '', lxx_be._GOROG_STRONG_RX, 'gorog_strong')         # üres: a forrás nem adja
        lxx_be._alak_kapu(r, 'G1941', lxx_be._GOROG_STRONG_RX, 'gorog_strong')
        with self.assertRaises(BemenetHiba):
            lxx_be._alak_kapu(r, '1941', lxx_be._GOROG_STRONG_RX, 'gorog_strong')

    def test_ismeretlen_fajl_igehely_lxx_nelkul(self):
        from lapgen.bemenet.jegyzek import BemenetHiba
        fejlec = ('igehely_karoli', 'szoalak')
        self.assertEqual(lxx_be._vers_index([('LXX_OS/karoli_fejezet_dontes.tsv', fejlec, [])]), {})
        with self.assertRaises(BemenetHiba):
            lxx_be._vers_index([('LXX_OS/uj_tabla.tsv', fejlec, [])])
