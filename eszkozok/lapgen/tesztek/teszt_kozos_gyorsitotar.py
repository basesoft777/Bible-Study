"""A közös lap-gyorsítótár (`kozos.lap_keszit`) őrtesztje: a gyorsítótárazott lap ugyanaz, mint a friss generálás, és a hívók egymás
eredményét nem módosíthatják."""
import datetime
import unittest

import kozos
from lapgen import fo
from lapgen.megjelenites.md.iro import lap_szoveg
from lapgen.szoveg import MotivumId

DATUM = datetime.date(2026, 11, 13)


class KozosGyorsitotar(unittest.TestCase):
    def test_a_gyorsitotarazott_lap_a_friss_generalassal_bajtra_azonos(self):
        for azonosito in kozos.MINTALAPOK:
            tarolt = kozos.lap_keszit(azonosito, DATUM)
            friss = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM)
            self.assertEqual(sorted(tarolt.nezetek), sorted(friss.nezetek), azonosito)
            for nezet in friss.nezetek:
                self.assertEqual(lap_szoveg(tarolt.nezetek[nezet]), lap_szoveg(friss.nezetek[nezet]), (azonosito, nezet))
            self.assertEqual(len(tarolt.figyelmeztetesek), len(friss.figyelmeztetesek), azonosito)

    def test_egyszer_generalodik_es_a_hivok_kulon_peldanyt_kapnak(self):
        a = kozos.lap_keszit('HAMART-001', DATUM)
        b = kozos.lap_keszit('HAMART-001', DATUM)
        self.assertIsNot(a, b)
        self.assertIsNot(a.nezetek, b.nezetek)
        self.assertIn(('HAMART-001', DATUM), kozos._LAP_GYORSITOTAR)
        a.nezetek.clear()   # egy hívó módosítása a többit nem érinti
        self.assertTrue(kozos.lap_keszit('HAMART-001', DATUM).nezetek)
        for sorok in b.nezetek.values():
            self.assertIsInstance(sorok, tuple)   # a kész sorok nem módosíthatók helyben


if __name__ == '__main__':
    unittest.main()
