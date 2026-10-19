#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_11.py -- DT-F11i: az eszkozok/ellenoriz.py 11.
szabalyanak (res-forras egyezes) datumfuggetlensege. Az elvart res-szoveg a
lapon allo proveniencia-sor `ts=` ertekevel generalodik, nem a mai nappal;
a ts-en kivuli eltérés tovabbra is SÉRTÉS.

A repo elo adataval fut (lexikon/ISTENTISZT-001_TUDOMANYOS.md, adat/), a
lapot csak memoriaban modositja; a "ma" a general.TS atallitasaval szimulalt.

    python eszkozok/teszt_ellenoriz_11.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ellenoriz as E  # noqa: E402
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402

MOTIVUM = 'ISTENTISZT-001'
ADATRESEK = ('2b', 'minosites', 'alatamasztas')
LAP = os.path.join(E.ROOT, 'lexikon', '%s_TUDOMANYOS.md' % MOTIVUM)


def _lap():
    with open(LAP, encoding='utf-8') as fh:
        return fh.read()


def _egyezik(lap, res):
    r = LG.res_forras_sorok()[(MOTIVUM, res)]
    elvart, tenyleges = E.res_elvart_es_tenyleges(LG, lap, MOTIVUM, res, r)
    return elvart == tenyleges


class Szabaly11Ts(unittest.TestCase):
    def setUp(self):
        self.eredeti_ts = G.TS
        self.lap = _lap()
        # a lapon allo ts (a generalas napja) -- a "ma" ennel kesobbi
        self.lap_ts = E.res_lap_ts(LG.res_torzs_lapbol(self.lap, {'id': MOTIVUM}, '2b'), MOTIVUM)
        self.assertIsNotNone(self.lap_ts, 'a 2b resben nincs proveniencia-ts')

    def tearDown(self):
        G.TS = self.eredeti_ts

    def test_pozitiv_korabbi_ts_ma_is_rendben(self):
        G.TS = '2099-12-31'  # a generalas utani barmelyik nap
        for res in ADATRESEK:
            with self.subTest(res=res):
                self.assertTrue(_egyezik(self.lap, res))

    def test_pozitiv_tegnapi_ts(self):
        # a lapon tegnapi ts all, ma van ma: RENDBEN
        lap = self.lap.replace('ts=%s`*' % self.lap_ts, 'ts=2026-10-18`*')
        G.TS = '2026-10-19'
        for res in ADATRESEK:
            with self.subTest(res=res):
                self.assertTrue(_egyezik(lap, res))

    def test_negativ_tartalmi_elteres_serteses(self):
        G.TS = '2099-12-31'
        torzs = LG.res_torzs_lapbol(self.lap, {'id': MOTIVUM}, 'alatamasztas')
        prov_kezdet = torzs.rindex('*Proveniencia:')
        modositott = torzs[:prov_kezdet] + 'Beszúrt, a táblából nem következő mondat.\n\n' + torzs[prov_kezdet:]
        lap = self.lap.replace(torzs, modositott, 1)
        self.assertNotEqual(lap, self.lap)
        self.assertFalse(_egyezik(lap, 'alatamasztas'))

    def test_negativ_forraslista_elteres_serteses(self):
        # a proveniencia-sor ts-en kivuli resze sem lazul
        lap = self.lap.replace('forras=adat/kapcsolatok.tsv |', 'forras=adat/mas.tsv |', 1)
        self.assertNotEqual(lap, self.lap)
        self.assertFalse(_egyezik(lap, 'alatamasztas'))

    def test_ts_nelkul_regi_viselkedes(self):
        self.assertIsNone(E.res_lap_ts('nincs proveniencia', MOTIVUM))
        self.assertIsNone(E.res_lap_ts(
            '*Proveniencia: `scope=id:MAS-001 | forras=adat/x.tsv | ts=2026-01-01`*', MOTIVUM))

    def test_szabaly_rendben_kesobbi_napon(self):
        G.TS = '2099-12-31'
        self.assertEqual(E.szabaly11_res_forras_egyezes(os.path.join(E.ROOT, 'adat')).verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main(verbosity=2)
