#!/usr/bin/env python3
"""teszt_dontes_allapot.py — érvénytelen döntés nem kerülhet a lapra (F182, 2. fázis, F27).

Futtatás: python -m unittest eszkozok.teszt_dontes_allapot  (a repó gyökeréből)

- a `DONTESEK.md` ⛔-jelölésének olvasása (`dontes_allapot`), a felülíró lánc;
- a generátor a felülíró döntés dátumát írja (`lexikon_general.ervenyes_dontes`);
- az `ellenoriz.py` 21. szabálya jelzi, ha a lap érvénytelen döntésre hivatkozik: a HAMART-001 mai lapján 0 lelet,
  egy érvénytelennek jelölt (rontott) döntés-állapottal jelez.
"""
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import dontes_allapot as DA  # noqa: E402

FEJ = '| # | Feladat | Kérdés | Opciók | Javaslat | Állapot | Döntés | Napló |\n|---|---|---|---|---|---|---|---|\n'
SOROK = [
    '| DT10 | #1 x | k | o | j | ⛔ | **FELÜLÍRVA → DT12** (a) régi, 2026-10-01 | n |',
    '| DT11 | #1 x | k | o | j | ⛔ | **VISSZAVONVA** (b), 2026-10-02 | n |',
    '| DT12 | #1 x | k | o | j | ⛔ | **FELÜLÍRVA → DT13** (c), 2026-10-03 | n |',
    '| DT13 | #1 x | k | o | j | ✅ | **(d)**, 2026-10-04 | n |',
    '| DT14 | #1 x | k | o | j | 🟢 | (a) — a felülírt DT9 helyett, 2026-10-05 | n |',
]


class Allapot(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        with open(os.path.join(self.d, 'DONTESEK.md'), 'w', encoding='utf-8') as f:
            f.write('# x\n\n' + FEJ + '\n'.join(SOROK) + '\n')

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_jeloles(self):
        a = DA.betolt(self.d)
        self.assertFalse(a['DT10']['ervenyes'])
        self.assertEqual(a['DT10']['utod'], 'DT12')
        self.assertEqual(a['DT11']['ok'], 'visszavonva')
        self.assertIsNone(a['DT11']['utod'])
        self.assertTrue(a['DT14']['ervenyes'])      # a szövegben álló „felülírt” szó nem jelölés

    def test_lanc(self):
        a = DA.betolt(self.d)
        self.assertEqual(DA.ervenyes_utod('DT10', a), 'DT13')
        self.assertIsNone(DA.ervenyes_utod('DT11', a))
        self.assertEqual(DA.ervenyes_utod('DT13', a), 'DT13')
        self.assertEqual(DA.ervenyes_utod('DT999', a), 'DT999')

    def test_generator_a_felulirot_irja(self):
        import lexikon_general as LG
        regi_a, regi_d = LG._dontes_allapot_cache, LG._dontes_datum_cache
        try:
            LG._dontes_allapot_cache = DA.betolt(self.d)
            LG._dontes_datum_cache = {'DT13': '2026-10-04', 'DT10': '2026-10-01'}
            self.assertEqual(LG.ervenyes_dontes('DT10'), 'DT13')
            self.assertEqual(LG._olvasoi_resz('a döntés nyoma: DT10'), 'a döntés nyoma: szerkesztői döntés, 2026-10-04')
            self.assertEqual(LG._olvasoi_resz('a döntés nyoma: DT11'), 'a döntés nyoma: szerkesztői döntés')
        finally:
            LG._dontes_allapot_cache, LG._dontes_datum_cache = regi_a, regi_d

    def test_valodi_dontesek_md(self):
        a = DA.betolt(GYOKER)
        self.assertIn('DT683', a)
        self.assertTrue(a['DT683']['ervenyes'])


class HamartLap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(GYOKER, 'lexikon', 'HAMART-001_TUDOMANYOS.md'), encoding='utf-8') as f:
            cls.lap = f.read()

    def test_mai_lap_ervenyes(self):
        import ellenoriz as E
        h = E.lap_hibak(self.lap, None, None, DA.betolt(GYOKER))
        self.assertEqual([x for x in h['iv'] if 'érvénytelen' in x], [])

    def test_rontott_allapot_jelez(self):
        import ellenoriz as E
        a = DA.betolt(GYOKER)
        self.assertIn('DT683', self.lap)
        a['DT683'] = {'ervenyes': False, 'utod': 'DT999', 'ok': 'felülírva'}
        h = E.lap_hibak(self.lap, None, None, a)
        self.assertTrue([x for x in h['iv'] if 'érvénytelen döntés a lapon: DT683' in x])


if __name__ == '__main__':
    unittest.main()
