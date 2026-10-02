#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_bdb_zaras.py -- F38 zaromenet (DT-F38e): adat-regresszio az
adat/forditasok.tsv F38-as soraira.

  - minden `F38 BDB_FORDITAS` megjegyzesu soron allapot=sonnet es
    modell=claude-sonnet-5-5 (nincs `opus` allapot / `claude-opus` modell);
  - a #28 sorai (nem F38-as) nem kaptak sonnet cimket;
  - a szellem-lista (naplok/BDB_FORDITAS_szellem.py) minden cserejet
    tartalmazza a sor, a regi reszlet nincs benne;
  - a teljes kapusor (a sor terminologia-kiveteleivel) atmegy minden F38-as soron;
  - az uj normalizalo-szabalyok mar nem talalnak javitando helyet az F38-as sorokon.

    python eszkozok/teszt_bdb_zaras.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'naplok'))

import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
import normalizal as N  # noqa: E402
from BDB_FORDITAS_szellem import SZELLEM  # noqa: E402
from BDB_FORDITAS_ujranormalizal import kivetelek  # noqa: E402

JEL = 'F38 BDB_FORDITAS'


def f38_sorok():
    ki = []
    for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
        if r['szotar'] == 'BDB' and r['jelentes_szam'] == 'teljes':
            ki.append(r)
    return ki


class Cimkek(unittest.TestCase):
    def test_f38_sorok_sonnet(self):
        db = 0
        for r in f38_sorok():
            if JEL in r['megjegyzes']:
                db += 1
                self.assertEqual(r['allapot'], 'sonnet', r['strong'])
                self.assertEqual(r['modell'], 'claude-sonnet-5-5', r['strong'])
        self.assertGreaterEqual(db, 243)

    def test_nincs_opus_cimke_f38_soron(self):
        for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
            if JEL in r['megjegyzes']:
                self.assertNotIn('opus', r['allapot'] + r['modell'], r['strong'])

    def test_28_sorai_nem_sonnet(self):
        for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
            if JEL not in r['megjegyzes']:
                self.assertNotEqual(r['allapot'], 'sonnet', r['strong'])


class Szellem(unittest.TestCase):
    def test_lista_alkalmazva(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        for strong, pont, regi, uj, _ in SZELLEM:
            hu = sorok[E.strong_padded(strong)]['forditas_hu']
            self.assertEqual(hu.count(uj), 1, (strong, pont))
            self.assertEqual(hu.count(regi), 0, (strong, pont))


class Kapuk(unittest.TestCase):
    def test_kapusor_atmegy_f38_soron(self):
        for r in f38_sorok():
            if JEL not in r['megjegyzes']:
                continue
            sp, forras = E.forras_szoveg(r['strong'])
            eredm = K.kapuk_futtat('BDB', forras, r['forditas_hu'], bizonytalan=kivetelek(r['megjegyzes']))
            self.assertTrue(K.atment(eredm), (r['strong'], [x for x in eredm if x[1] == 'SERTES']))

    def test_normalizalo_nem_talal_javitando_helyet(self):
        for r in f38_sorok():
            if JEL not in r['megjegyzes']:
                continue
            uj, valt = N.normalizal(r['forditas_hu'], 'BDB')
            self.assertEqual(valt, [], (r['strong'], valt))
            self.assertEqual(uj, r['forditas_hu'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
