#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_strong_util.py -- F62: a strong_util.strong_normalizal alakonkénti tesztjei
(naplok/STRONG_NORMALIZAL_M0.md 2. pont, a 13 bemeneti alakcsalád).

    python eszkozok/teszt_strong_util.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strong_util import strong_normalizal as N, strong_ervenyes as V  # noqa: E402


class Alakok(unittest.TestCase):
    def test_01_sema_alak_valtozatlan(self):
        for s in ('H0779', 'H8415', 'G0086', 'G5228'):
            self.assertEqual(N(s), s)

    def test_02_nullazatlan(self):
        self.assertEqual(N('H779'), 'H0779')
        self.assertEqual(N('H1'), 'H0001')
        self.assertEqual(N('H70'), 'H0070')
        self.assertEqual(N('G976'), 'G0976')
        self.assertEqual(N('H922'), 'H0922')

    def test_03_elotag_nelkul(self):
        with self.assertRaises(ValueError):
            N('1078')
        self.assertEqual(N('1078', nyelv='G'), 'G1078')
        self.assertEqual(N('976', nyelv='H'), 'H0976')
        self.assertEqual(N('H976', nyelv='H'), 'H0976')
        with self.assertRaises(ValueError):
            N('G976', nyelv='H')

    def test_04_betuutotag(self):
        for s in ('H2967a', 'G3924a', 'H0032a'):
            with self.assertRaises(ValueError):
                N(s)
        self.assertEqual(N('H2967a', utotag='megtart'), 'H2967a')
        self.assertEqual(N('G924a', utotag='megtart'), 'G0924a')
        self.assertEqual(N('3924a', nyelv='G', utotag='megtart'), 'G3924a')

    def test_05_otjegyu(self):
        self.assertEqual(N('G00120'), 'G0120')
        self.assertEqual(N('H07121'), 'H7121')
        for s in ('G20447', 'H12345', 'G001200', 'G000000'):
            with self.assertRaises(ValueError):
                N(s)

    def test_06_aramai(self):
        with self.assertRaises(ValueError):
            N('A0002')

    def test_07_lanc(self):
        self.assertEqual(N('H8414+H0922'), 'H8414+H0922')
        self.assertEqual(N('H8414+H922'), 'H8414+H0922')
        self.assertEqual(N('G5228+G1537+G4053'), 'G5228+G1537+G4053')
        self.assertEqual(N('G4053+G5228+G1537'), 'G4053+G5228+G1537')  # sorrend megmarad
        self.assertEqual(N('H3+H2'), 'H0003+H0002')
        self.assertEqual(N('1537+4053', nyelv='G'), 'G1537+G4053')
        for s in ('H0779+', '+H0779', 'H0779++H0780', 'H0779+x'):
            with self.assertRaises(ValueError):
                N(s)

    def test_08_felsorolas_nem_lanc(self):
        for s in ('H0710,H0713', '1886j|2050b', 'H0710 H0713'):
            with self.assertRaises(ValueError):
                N(s)

    def test_09_tipnr_utotag(self):
        for s in ('H5653G', 'G0007G', 'H5660I', 'H0746A'):
            with self.assertRaises(ValueError):
                N(s)
            with self.assertRaises(ValueError):
                N(s, utotag='megtart')

    def test_10_ures_gondolatjel_nem_string(self):
        for s in ('', '   ', '—', '-', None, 779, ['H0779']):
            with self.assertRaises(ValueError):
                N(s)

    def test_11_kisbetu(self):
        self.assertEqual(N('h0779'), 'H0779')
        self.assertEqual(N('g2564'), 'G2564')
        self.assertEqual(N('h779+g94'), 'H0779+G0094')

    def test_12_szokoz(self):
        self.assertEqual(N(' H0779 '), 'H0779')
        self.assertEqual(N('\tH779\n'), 'H0779')
        self.assertEqual(N('H0779 + H0780'), 'H0779+H0780')

    def test_13_nulla_es_hibas(self):
        for s in ('H0000', 'H0', 'H', 'G', 'HG0779', 'X0779', 'H07.79'):
            with self.assertRaises(ValueError):
                N(s)

    def test_14_parameterek(self):
        with self.assertRaises(ValueError):
            N('H0779', nyelv='A')
        with self.assertRaises(ValueError):
            N('H0779', utotag='egyeb')


class Tulajdonsagok(unittest.TestCase):
    MINTAK = ['H0779', 'H779', 'h1', 'G00120', ' G976 ', 'H8414+H922', 'G5228+G1537+G4053',
              'H2967a', 'G3924a', '1078', 'H07121']
    KAPCSOLOK = ({}, {'nyelv': 'H'}, {'nyelv': 'G'}, {'utotag': 'megtart'},
                 {'nyelv': 'G', 'utotag': 'megtart'})

    def test_idempotencia(self):
        for s in self.MINTAK:
            for kw in self.KAPCSOLOK:
                try:
                    x = N(s, **kw)
                except ValueError:
                    continue
                self.assertEqual(N(x, **kw), x, (s, kw))
                self.assertEqual(N(x, utotag=kw.get('utotag', 'tilt')), x, (s, kw))

    def test_erveny_csak_szigoru_alak(self):
        self.assertTrue(V('H0779'))
        self.assertTrue(V('H8414+H0922'))
        self.assertFalse(V('H779'))
        self.assertFalse(V('h0779'))
        self.assertFalse(V(' H0779'))
        self.assertFalse(V('H2967a'))
        self.assertTrue(V('H2967a', utotag='megtart'))
        self.assertFalse(V('1078'))
        self.assertFalse(V(''))
        self.assertFalse(V(None))

    def test_ervenyes_osszhang_a_normalizaloval(self):
        for s in self.MINTAK:
            try:
                x = N(s)
            except ValueError:
                self.assertFalse(V(s))
                continue
            self.assertEqual(V(s), x == s)

    def test_adattabla_sema_alakjai_valtozatlanok(self):
        """A repó adat/ Strong-értékei (M0 mérés: 0 eltérés) a függvényen változatlanok."""
        gyoker = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for rel, oszlop in (('adat/elofordulasok.tsv', 'strong'),
                            ('adat/forditasok.tsv', 'strong'),
                            ('adat/lexikon_hivatkozasok.tsv', 'strong'),
                            ('konkordancia/Karoli_Strong_kivonat.tsv', 'Strong-szám')):
            with open(os.path.join(gyoker, rel), encoding='utf-8') as f:
                sorok = [l.rstrip('\r\n') for l in f if l.strip() and not l.startswith('#')]
            fejlec = sorok[0].split('\t')
            i = fejlec.index(oszlop)
            n = 0
            for l in sorok[1:]:
                p = l.split('\t')
                v = p[i] if i < len(p) else ''
                if v:
                    n += 1
                    self.assertEqual(N(v), v, (rel, v))
            self.assertGreater(n, 0, rel)


class LekerdezCli(unittest.TestCase):
    """DT-F62a: a lekerdez.py CLI-bemenete szigorú — hiba a helyes alakkal, nem néma nem-találat."""

    def setUp(self):
        import io
        import contextlib
        import lekerdez
        self.L = lekerdez
        self.io, self.cl = io, contextlib

    def _hiba(self, s):
        puf = self.io.StringIO()
        with self.cl.redirect_stderr(puf):
            with self.assertRaises(SystemExit) as cm:
                self.L.cli_strong(s)
        self.assertEqual(cm.exception.code, 1)
        return puf.getvalue()

    def test_ervenyes_alak(self):
        self.assertEqual(self.L.cli_strong('H0779'), 'H0779')
        self.assertEqual(self.L.cli_strong(' h0779 '), 'H0779')
        self.assertEqual(self.L.cli_strong('G0086'), 'G0086')

    def test_nullazatlan_hibat_ad_a_helyes_alakkal(self):
        self.assertIn('H0779 alakú legyen', self._hiba('H779'))

    def test_ervenytelen_alakok(self):
        for s in ('1078', 'A0002', 'H2967a', 'H0779+H0780', 'X1', '', 'H'):
            self._hiba(s)


if __name__ == '__main__':
    unittest.main(verbosity=2)
