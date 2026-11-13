"""A teljes futás tesztjei: determinizmus (GK-29), a befagyasztás-kivétel (GK-30)."""
import datetime
import io
import os
import shutil
import tempfile
import unittest

import kozos
from kozos import MINTALAPOK, alap_minirepo
from lapgen import fo
from lapgen.megjelenites.md.iro import lap_szoveg
from lapgen.szoveg import MotivumId


def _szovegek(eredmeny):
    return {nezet: lap_szoveg(sorok) for nezet, sorok in eredmeny.nezetek.items()}


class Determinizmus(unittest.TestCase):
    def test_gk29_ket_futas_bajtra_azonos(self):
        """GK-29: két egymás utáni futás azonos bemenettel bájtra azonos kimenetet ad, rögzített dátummal és
        dátum nélkül is (ekkor a `ts=` a bemenetek hash-éből képződik)."""
        for azonosito in MINTALAPOK:
            for datum in (datetime.date(2026, 11, 13), None):
                elso = _szovegek(fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=datum))
                masodik = _szovegek(fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=datum))
                self.assertEqual(elso, masodik, '%s, dátum: %s' % (azonosito, datum))

    def test_gk29_a_ts_a_megadott_datumbol_jon(self):
        from lapgen.szoveg import Belso, prov
        ts = fo._ts(datetime.date(2026, 11, 13), ())
        self.assertEqual(ts, prov('ts={}', Belso('2026-11-13', 'ts')))
        hash_ts = fo._ts(None, ())
        self.assertEqual(hash_ts, fo._ts(None, ()))
        self.assertNotEqual(hash_ts, ts)


class Befagyasztas(unittest.TestCase):
    def setUp(self):
        self.repo = alap_minirepo()
        self.kint = tempfile.mkdtemp(prefix='lapgen_ki_')

    def tearDown(self):
        self.repo.torol()
        shutil.rmtree(self.kint, ignore_errors=True)

    def test_gk30_befagyasztott_kimenet_nelkul_kimondott_kihagyas(self):
        """GK-30: repón kívüli `--kimenet` nélkül a befagyasztott motívum kimondva kimarad (kilépési kód 0)."""
        ki = io.StringIO()
        belul = os.path.join(self.repo.gyoker, 'generalt_proba')
        self.assertEqual(fo.futtat(self.repo.gyoker, 'FAGYOTT-001', belul, ki=ki), 0)
        self.assertIn('kihagyva (befagyasztott', ki.getvalue())
        self.assertFalse(os.path.exists(belul))

    def test_gk30_nem_befagyasztott_kimenet_nelkul_hiba(self):
        """A 218a alatt a generátor a repó alá nem ír: repón belüli kimenetnél hívási hiba."""
        ki = io.StringIO()
        self.assertEqual(fo.futtat(self.repo.gyoker, 'SZABAD-001', os.path.join(self.repo.gyoker, 'x'), ki=ki), 2)
        self.assertEqual(fo.futtat(self.repo.gyoker, 'SZABAD-001', self.repo.gyoker, ki=ki), 2)

    def test_gk30_befagyasztott_repon_kivuli_kimenetbe_fut(self):
        """GK-30: repón kívüli próbakimenetbe a befagyasztott motívum is generálható."""
        ki = io.StringIO()
        self.assertEqual(fo.futtat(self.repo.gyoker, 'FAGYOTT-001', self.kint, datum='2026-11-13', ki=ki), 0)
        self.assertNotIn('kihagyva', ki.getvalue())

    def test_hivasi_hibak(self):
        ki = io.StringIO()
        self.assertEqual(fo.futtat(self.repo.gyoker, None, self.kint, ki=ki), 2)
        self.assertEqual(fo.futtat(self.repo.gyoker, 'rossz azonosító', self.kint, ki=ki), 2)
        self.assertEqual(fo.futtat(self.repo.gyoker, 'SZABAD-001', self.kint, mod='ismeretlen', ki=ki), 2)

    def test_gk30_az_eles_repoban_a_befagyasztott_minta_kimarad(self):
        """Az éles jegyzéken: a befagyasztott mintalap repón belüli kimenettel kimarad."""
        from lapgen import bemenet
        fagyott = bemenet.b59_befagyasztott(bemenet.Bemenet(kozos.GYOKER))
        for azonosito in MINTALAPOK:
            if MotivumId(azonosito) in fagyott:
                ki = io.StringIO()
                self.assertEqual(fo.futtat(kozos.GYOKER, azonosito, os.path.join(kozos.GYOKER, 'generalt_proba'),
                                           ki=ki), 0)
                self.assertIn('kihagyva', ki.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=1)
