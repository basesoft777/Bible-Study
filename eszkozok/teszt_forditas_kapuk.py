#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_forditas_kapuk.py -- F28_EMELES_BRIEF.md: a forditas_kapuk.py
DT25 utan felvett jelzo kapuinak (12. Szentlélek, 13. fejezetszam) es a
11. konyv-egyezes kapunak tesztjei.

    python eszkozok/teszt_forditas_kapuk.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import forditas_kapuk as K  # noqa: E402


class Szentlelek(unittest.TestCase):
    def test_jelzes(self):
        for szoveg in ('a Szentlélek által', 'Isten Lelke', 'Szent Lélek'):
            self.assertEqual(K.ellenoriz_szentlelek(szoveg)[0], 'JELZES', szoveg)

    def test_jovahagyott_alak(self):
        self.assertEqual(K.ellenoriz_szentlelek('a Szent Szellem, Isten Szelleme, a lélek')[0], 'RENDBEN')


class Fejezetszam(unittest.TestCase):
    def test_tul_nagy_fejezet(self):
        e, d = K.ellenoriz_fejezetszam('Ez 73:23; Péld 57:1')
        self.assertEqual(e, 'JELZES')
        self.assertIn('Ez 73', d)

    def test_heber_szamozas_es_rovid_konyv(self):
        self.assertEqual(K.ellenoriz_fejezetszam('Jóel 4:19; 1Ján 5:7; Júd 1:20; Zsolt 150:6')[0], 'RENDBEN')


class LelekTovaltozat(unittest.TestCase):
    """ELLENOR_F28 3. tétel: a „lélek” tőváltozata (lelk-) csak a főnév
    toldalékolt alakjára illeszkedjen."""

    TERM = [{'angol': 'soul', 'magyar': 'lélek'}]

    def _e(self, forditas):
        return K.ellenoriz_terminologia('the soul of man', forditas, self.TERM, [])[0]

    def test_toldalekolt_alakok(self):
        for szo in ('lelke', 'lelkét', 'lelkem', 'lelkedből', 'lelkünk', 'lelkük',
                    'lelkek', 'lelketekben', 'keserű lelkű', 'Lelkét'):
            self.assertEqual(self._e('az ember %s' % szo), 'RENDBEN', szo)

    def test_nem_a_lelek_alakjai(self):
        for szo in ('lelkiismeret', 'lelkiismerete', 'lelkész', 'lelkésze',
                    'lelkes', 'lelkesedés', 'lelkület', 'lelki'):
            self.assertEqual(self._e('az ember %s' % szo), 'SERTES', szo)

    def test_alapalak(self):
        self.assertEqual(self._e('az ember lélek'), 'RENDBEN')


class Konyvek(unittest.TestCase):
    def test_jsir_es_sir(self):
        self.assertEqual(K.ellenoriz_konyvek('Lam 3:57; Sir. 1:3', 'JSir 3:57; Sir 1:3')[0], 'RENDBEN')
        self.assertEqual(K.ellenoriz_konyvek('Lam 3:57', 'Sir 3:57')[0], 'SERTES')


if __name__ == '__main__':
    unittest.main(verbosity=2)
