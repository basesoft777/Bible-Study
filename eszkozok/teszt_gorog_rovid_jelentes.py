#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_gorog_rovid_jelentes.py -- F121 (DT-F121o): a 7. szerep görög rövid jelentése a `forditasok.tsv`
`TBESG | <Strong> | <Strong> | rovid | glosszak_hu` sorából jön; ahol nincs, az angol + `fordításra vár`.

    python eszkozok/teszt_gorog_rovid_jelentes.py
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexikon_general as LG  # noqa: E402


class GorogRovid(unittest.TestCase):
    def setUp(self):
        self._eredeti = LG.forditas_ehhez
        self._tbesg = LG.tbesg_rovid_glossza

    def tearDown(self):
        LG.forditas_ehhez = self._eredeti
        LG.tbesg_rovid_glossza = self._tbesg

    def test_van_magyar_sor(self):
        hivasok = []

        def f(*a):
            hivasok.append(a)
            return 'hozni'
        LG.forditas_ehhez = f
        LG.tbesg_rovid_glossza = lambda s: 'to bring'
        self.assertEqual(LG.rovid_jelentes('G0071'), ('hozni', True))
        self.assertEqual(hivasok, [('TBESG', 'G0071', 'G0071', 'rovid', 'glosszak_hu')])

    def test_nincs_magyar_sor_az_angol_es_a_jelolo(self):
        LG.forditas_ehhez = lambda *a: ''
        LG.tbesg_rovid_glossza = lambda s: 'to bring'
        szoveg, van = LG.rovid_jelentes('G0071')
        self.assertFalse(van)
        self.assertEqual(szoveg, 'to bring %s' % LG.FORDITASRA_VAR)

    def test_nincs_se_magyar_se_angol(self):
        LG.forditas_ehhez = lambda *a: ''
        LG.tbesg_rovid_glossza = lambda s: None
        self.assertEqual(LG.rovid_jelentes('G9999'), (LG.EM_DASH, False))

    def test_heber_ag_valtozatlan(self):
        LG.forditas_ehhez = lambda *a: 'NE'
        self.assertNotEqual(LG.rovid_jelentes('H7121')[0], 'NE')


if __name__ == '__main__':
    unittest.main(verbosity=2)
