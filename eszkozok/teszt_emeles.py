#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_emeles.py -- F38.265 (DT-F38e): az emeles.py rogzit/beir
parancsainak argumentum-szabalyai. A modell-azonositonak nincs alaperteke
(a `claude-opus-5-5` alapertek miatt kaptak 243 Sonnet-forditas hibas
cimket), es a `sonnet` allapot elfogadott.

    python eszkozok/teszt_emeles.py
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stderr

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import emeles as E  # noqa: E402


def parse(argv):
    return E.parser_epit().parse_args(argv)


class RogzitModell(unittest.TestCase):
    def test_modell_nelkul_hiba(self):
        hiba = io.StringIO()
        with redirect_stderr(hiba), self.assertRaises(SystemExit) as k:
            parse(['rogzit', 'H0001', '--be', 'x.txt', '--allapot', 'sonnet'])
        self.assertNotEqual(k.exception.code, 0)
        self.assertIn('--modell', hiba.getvalue())

    def test_modell_megadva_rendben(self):
        a = parse(['rogzit', 'H0001', '--be', 'x.txt', '--allapot', 'sonnet', '--modell', 'claude-sonnet-5-5'])
        self.assertEqual(a.modell, 'claude-sonnet-5-5')

    def test_nincs_modell_alapertek(self):
        for sz in E.parser_epit()._subparsers._group_actions[0].choices['rogzit']._actions:
            if sz.dest == 'modell':
                self.assertIsNone(sz.default)
                self.assertTrue(sz.required)

    def test_rogzit_sonnet_allapot(self):
        a = parse(['rogzit', 'H0001', '--be', 'x.txt', '--allapot', 'sonnet', '--modell', 'm'])
        self.assertEqual(a.allapot, 'sonnet')


class RogzitAllapot(unittest.TestCase):
    def test_allapot_nelkul_hiba(self):
        hiba = io.StringIO()
        with redirect_stderr(hiba), self.assertRaises(SystemExit):
            parse(['rogzit', 'H0001', '--be', 'x.txt', '--modell', 'claude-sonnet-5-5'])
        self.assertIn('--allapot', hiba.getvalue())


class BeirAllapot(unittest.TestCase):
    def test_beir_sonnet_allapot(self):
        a = parse(['beir', 'H0001', '--allapot', 'sonnet'])
        self.assertEqual(a.allapot, 'sonnet')

    def test_beir_ismeretlen_allapot_hiba(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parse(['beir', 'H0001', '--allapot', 'haiku'])


class PromptAdatblokk(unittest.TestCase):
    """F56 M4, prompt v4.2: az {{ADATBLOKK}} helyorzo bekotese."""

    def test_bdb_prompt_adatblokkot_kap(self):
        sp, forras = E.forras_szoveg('H2617')
        p = E.prompt_epit(sp, forras)
        self.assertNotIn('{{ADATBLOKK}}', p)
        self.assertIn('### ADATBLOKK H2617', p)
        self.assertIn('scope=', p)
        # a blokk a forras elott all
        self.assertLess(p.index('### ADATBLOKK H2617'), p.index('Forrás (Thayer, angol):'))

    def test_thayer_prompt_nincs_adatblokk(self):
        sp, forras = E.forras_szoveg('G26')
        p = E.prompt_epit(sp, forras)
        self.assertNotIn('{{ADATBLOKK}}', p)
        self.assertNotIn('### ADATBLOKK', p)
        self.assertIn('nincs adatblokk', p)

    def test_prompt_szabalyok_kimondva(self):
        sp, forras = E.forras_szoveg('H2617')
        p = E.prompt_epit(sp, forras)
        self.assertIn('`alacsony` bizonyosságú Károli-alak **nem kevésbé valószínű olvasat**', p)
        self.assertIn('`[kihagyva …]` sor szavai', p)
        self.assertIn("ja'an", p)
        self.assertIn('`Y [BDB: X]`', p)


if __name__ == '__main__':
    unittest.main(verbosity=2)
