"""A teljes futás tesztjei: determinizmus (GK-29), a befagyasztás-kivétel (GK-30), a célnév és a G01 módja (F241.2)."""
import contextlib
import datetime
import io
import os
import shutil
import sys
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
        from lapgen import bemenet
        fagyott = bemenet.b59_befagyasztott(bemenet.Bemenet(kozos.GYOKER))
        mintak = [a for a in MINTALAPOK if MotivumId(a) in fagyott]
        self.assertTrue(mintak, 'a mintalapok között nincs befagyasztott: a kivétel így nem mérhető')
        for azonosito in mintak:
            ki = io.StringIO()
            self.assertEqual(fo.futtat(kozos.GYOKER, azonosito, self.kint, datum='2026-11-13', ki=ki), 0,
                             ki.getvalue())
            self.assertNotIn('kihagyva', ki.getvalue())
            self.assertTrue(os.path.isfile(os.path.join(self.kint, 'lexikon', '%s_TUDOMANYOS.md' % azonosito)))

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


class Celnev(unittest.TestCase):
    """F241.2 (N243 (2), (4)): a `--cel lexikon` az új generátor; a még át nem állt motívum commitolt lapja a régi
    generátorral készül (visszaút, `ATALLT_MOTIVUMOK`); a régi generátor `--cel lexikon_regi` néven fut. A két generátor
    hívását a teszt rögzíti (nem futtatja)."""

    def setUp(self):
        import general
        import lexikon_general
        self.general, self.lg = general, lexikon_general
        self.hivasok = []
        self._eredeti = (fo.futtat, lexikon_general.run, sys.argv, general.ATALLT_MOTIVUMOK)
        fo.futtat = lambda gyoker, azon, kimenet, mod='munka', **_k: self.hivasok.append(('uj', azon, mod)) or 0
        lexikon_general.run = lambda args, motivumok, *_a: self.hivasok.append(
            ('regi', tuple(m['id'] for m in motivumok), args.cel)) or 0

    def tearDown(self):
        fo.futtat, self.lg.run, sys.argv, self.general.ATALLT_MOTIVUMOK = self._eredeti

    def _hiv(self, *argv):
        sys.argv = ['general.py'] + list(argv)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return self.general.main()

    def test_lap_nelkuli_motivum_az_uj_generatorral(self):
        self.assertEqual(self._hiv('--cel', 'lexikon', '--id', 'NINCSLAP-001', '--kimenet', 'x', '--mod', 'kiadas'), 0)
        self.assertEqual(self.hivasok, [('uj', 'NINCSLAP-001', 'kiadas')])

    def test_visszaut_a_regi_generatorra(self):
        """A commitolt régi lap (a HAMART-001 és a befagyasztott lapok) az átállásig a régi generátorral készül."""
        self.assertNotIn('HAMART-001', self.general.ATALLT_MOTIVUMOK)
        self.assertEqual(self._hiv('--cel', 'lexikon', '--id', 'HAMART-001', '--kimenet', 'x'), 0)
        self.assertEqual(self.hivasok, [('regi', ('HAMART-001',), 'lexikon')])

    def test_az_atallt_motivum_az_uj_generatorral(self):
        self.general.ATALLT_MOTIVUMOK = ('HAMART-001',)
        self.assertEqual(self._hiv('--cel', 'lexikon', '--id', 'HAMART-001', '--kimenet', 'x'), 0)
        self.assertEqual(self.hivasok, [('uj', 'HAMART-001', 'munka')])

    def test_a_regi_celnev(self):
        self.assertEqual(self._hiv('--cel', 'lexikon_regi', '--id', 'TEREMT-001', '--kimenet', 'x'), 0)
        self.assertEqual(self.hivasok, [('regi', ('TEREMT-001',), 'lexikon_regi')])


class G01Mod(unittest.TestCase):
    """F241.2: a jegyzék G01-sora (az egyetlen belépési pont) a kiadott lapot kiadás módban generálja (a Kolofon
    jóváhagyás-mondata és a GK-27 kapuja), a többit munka módban; a parancs a `--cel lexikon`."""

    def setUp(self):
        import generalt_nezetek
        self.gn = generalt_nezetek
        self.tagok = []
        self._eredeti = generalt_nezetek._futtat
        generalt_nezetek._futtat = lambda tagok, cwd, env_kieg=None: self.tagok.append(tagok) or (0, '')

    def tearDown(self):
        self.gn._futtat = self._eredeti

    def _kiadott(self):
        with open(os.path.join(kozos.GYOKER, 'adat', 'kiadasok.tsv'), encoding='utf-8') as f:
            return {s.split('\t')[0] for s in f if s.strip() and not s.startswith('#')}

    def test_a_parancs_az_uj_celnev(self):
        parancs = self.gn.sor(self.gn.LAP_SOR)['parancs'].split()
        self.assertEqual(parancs[parancs.index('--cel') + 1], 'lexikon')
        self.assertIn('{mod}', parancs)

    def test_kiadott_lap_kiadas_modban(self):
        kiadott = self._kiadott()
        self.assertIn('HAMART-001', kiadott)
        self.assertNotIn('TEREMT-001', kiadott)
        self.gn.lexikon_general('HAMART-001', 'x', '2026-11-13')
        self.gn.lexikon_general('TEREMT-001', 'x', '2026-11-13')
        modok = [t[t.index('--mod') + 1] for t in self.tagok]
        self.assertEqual(modok, ['kiadas', 'munka'])


if __name__ == '__main__':
    unittest.main(verbosity=1)
