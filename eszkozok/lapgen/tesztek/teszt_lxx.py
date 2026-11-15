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
