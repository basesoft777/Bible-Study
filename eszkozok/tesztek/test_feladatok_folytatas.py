#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_feladatok_folytatas.py -- F49_FOLYTATAS_BRIEF.md: a `fut` allapot ket jelentese
(felbemaradt `Folytatás:` / dolgozik rajta valaki), a VAR_RAD sor es a FUTO-vizsgalat
szukitese a `feladatok.py jeloltek`-ben.

Futtatas: python eszkozok/tesztek/test_feladatok_folytatas.py
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402
from test_feladatok_fugges import Fixture  # noqa: E402

FOLYT = F.FOLYTATAS_ELOTAG + ' az 5. adagtól'


class FolytatasTest(Fixture):
    def jeloltek(self):
        return F.jeloltek(self.briefek(), {})

    def cli(self):
        ki = io.StringIO()
        with redirect_stdout(ki):
            F.main(['--gyoker', self.ut, 'jeloltek'])
        return ki.getvalue().split('\n')

    def test_a_elotag_konstans(self):
        self.assertEqual(F.FOLYTATAS_ELOTAG, 'Folytatás:')

    def test_a_fut_folytatas_jelolt(self):
        self.brief(1, allapot='fut', kovetkezo=FOLYT, ir=['a.md'])
        self.assertIsNone(self.jeloltek()[1])
        self.assertTrue(any(s.startswith('FOLYTATAS\t#1\t') and FOLYT in s for s in self.cli()))

    def test_a_folytatas_idezojellel_is(self):
        self.brief(1, allapot='fut', kovetkezo='"%s"' % FOLYT, ir=['a.md'])
        self.assertIsNone(self.jeloltek()[1])

    def test_b_fut_mas_kihagyva(self):
        self.brief(1, allapot='fut', kovetkezo='dolgozik rajta egy session', ir=['a.md'])
        self.assertEqual(self.jeloltek()[1], 'állapot: fut')
        self.assertTrue(any(s.startswith('KIHAGYVA\t#1\t') for s in self.cli()))

    def test_c_megallt_te_var_rad(self):
        self.brief(1, allapot='megallt', kovetkezo='Te: indítsd a Józst', ir=['a.md'])
        self.assertIsNotNone(self.jeloltek()[1])
        self.assertTrue(any(s.startswith('VAR_RAD\t#1\t') and 'Te: indítsd' in s
                            for s in self.cli()))

    def test_d_fut_te_var_rad(self):
        self.brief(1, allapot='fut', kovetkezo='Te: döntés kell', ir=['a.md'])
        self.assertTrue(any(s.startswith('VAR_RAD\t#1\t') for s in self.cli()))
        self.assertNotIn(1, F.csomag(self.briefek(), {}))

    def test_e_folytatas_nem_tart_vissza_kizar_part(self):
        self.brief(1, allapot='fut', kovetkezo=FOLYT, ir=['kozos.md'])
        self.brief(2, allapot='nem_indult', ir=['kozos.md'])
        j = self.jeloltek()
        self.assertIsNone(j[1])
        self.assertIsNone(j[2])           # nem `kizár (futó)`

    def test_e2_valodi_futo_visszatartja(self):
        self.brief(1, allapot='fut', kovetkezo='dolgozik', ir=['kozos.md'])
        self.brief(2, allapot='nem_indult', ir=['kozos.md'])
        self.assertEqual(self.jeloltek()[2], 'kizár (futó): #1')

    def test_f_fuggesre_varo_felbemaradt_nem_folytatas(self):
        self.brief(1, allapot='nem_indult', ir=['a.md'])
        self.brief(2, allapot='fut', kovetkezo=FOLYT, olvas=['a.md'], ir=['b.md'])
        self.assertEqual(self.jeloltek()[2], 'vár: #1')
        self.assertFalse(any(s.startswith('FOLYTATAS') for s in self.cli()))

    def test_csomag_folytatas_elore_es_kizar_par_kimarad(self):
        self.brief(1, allapot='nem_indult', ir=['a.md'])
        self.brief(2, allapot='fut', kovetkezo=FOLYT, ir=['b.md'])
        self.brief(3, allapot='nem_indult', ir=['b.md'])   # kizar-par: kimarad
        self.assertEqual(F.csomag(self.briefek(), {}), [2, 1])

    def test_regi_fejlecu_folytatas_egyedul(self):
        self.brief(1, allapot='fut', kovetkezo=FOLYT, ir=['a.md'])
        self.brief(2, allapot='nem_indult', ir=['b.md'])
        # `ir` nelkuli feladat (regi): csak egyedul fut
        nev = os.path.join(self.ut, 'F03_T3_BRIEF.md')
        with open(nev, 'w', encoding='utf-8', newline='') as f:
            f.write('---\nfeladat: 3\ncim: R\ntipus: feladat\nfazis: 1\nmodell: sonnet\n'
                    'allapot: fut\nad: x\nkovetkezo: %s\n---\n' % FOLYT)
        self.assertEqual(F.csomag(self.briefek(), {}), [1, 2])


if __name__ == '__main__':
    unittest.main()
