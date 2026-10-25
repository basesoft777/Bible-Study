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


class KapuFelulir(unittest.TestCase):
    """DT-F38k (1): a celzott kapu-felulbiralas (`--kapu-felulir` + `--dontes`) szabalyai."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.dont = os.path.join(self.tmp.name, 'DONTESEK.md')
        with open(self.dont, 'w', encoding='utf-8') as fh:
            fh.write('| DT-F38k | cim | ... |\n| DT99 | masik | ... |\n')

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def args(kapu=None, dontes=None):
        a = ['szakasz_rogzit', 'H0001', '--be', 'x.txt', '--allapot', 'sonnet', '--modell', 'm']
        if kapu:
            a += ['--kapu-felulir', kapu]
        if dontes:
            a += ['--dontes', dontes]
        return parse(a)

    @staticmethod
    def eredm(*bukott):
        nevek = ['1_gorog_heber', '5_terminologia', '11_konyvek', '14_szakasz']
        return [(n, 'SERTES' if n in bukott else 'RENDBEN', '') for n in nevek]

    def felulir(self, a, e):
        return E.kapu_felulir(a, e, self.dont)

    def test_felulbiralas_nelkul_nincs_megjegyzes(self):
        self.assertEqual(self.felulir(self.args(), self.eredm('11_konyvek')), '')

    def test_felulbiralas_nelkul_a_bukas_marad(self):
        # a rogzitok `not ok and not felulir` agon allnak meg: ures felulbiralas + bukas = megallas
        e = self.eredm('11_konyvek')
        self.assertFalse(all(x != 'SERTES' for _, x, _ in e))
        self.assertEqual(self.felulir(self.args(), e), '')

    def test_dontes_nelkul_hiba(self):
        with self.assertRaises(SystemExit) as k:
            self.felulir(self.args(kapu='11_konyvek'), self.eredm('11_konyvek'))
        self.assertIn('--dontes', str(k.exception))

    def test_dontes_kapu_nelkul_hiba(self):
        with self.assertRaises(SystemExit):
            self.felulir(self.args(dontes='DT-F38k'), self.eredm('11_konyvek'))

    def test_ismeretlen_dontes_hiba(self):
        with self.assertRaises(SystemExit) as k:
            self.felulir(self.args('11_konyvek', 'DT-F38z'), self.eredm('11_konyvek'))
        self.assertIn('DONTESEK.md', str(k.exception))

    def test_nem_bukott_kapu_felulbiralasa_hiba(self):
        with self.assertRaises(SystemExit) as k:
            self.felulir(self.args('5_terminologia', 'DT-F38k'), self.eredm('11_konyvek'))
        self.assertIn('felesleges', str(k.exception))

    def test_semmi_sem_bukott_felesleges(self):
        with self.assertRaises(SystemExit) as k:
            self.felulir(self.args('11_konyvek', 'DT-F38k'), self.eredm())
        self.assertIn('felesleges', str(k.exception))

    def test_ket_kapu_bukasa_egy_felulbiralassal_nem_eleg(self):
        with self.assertRaises(SystemExit) as k:
            self.felulir(self.args('11_konyvek', 'DT-F38k'), self.eredm('11_konyvek', '5_terminologia'))
        self.assertIn('nem eleg', str(k.exception))

    def test_ismeretlen_kapunev_hiba(self):
        with self.assertRaises(SystemExit):
            self.felulir(self.args('99_nincs', 'DT-F38k'), self.eredm('11_konyvek'))

    def test_siker_megjegyzessel(self):
        self.assertEqual(self.felulir(self.args('11_konyvek', 'DT-F38k'), self.eredm('11_konyvek')),
                         'kapu-felülbírálás: 11_konyvek (DT-F38k)')

    def test_a_rogzit_is_kapja_a_kapcsolot(self):
        a = parse(['rogzit', 'H0001', '--be', 'x.txt', '--allapot', 'sonnet', '--modell', 'm',
                   '--kapu-felulir', '11_konyvek', '--dontes', 'DT-F38k'])
        self.assertEqual((a.kapu_felulir, a.dontes), ('11_konyvek', 'DT-F38k'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
