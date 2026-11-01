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


class RogzitoAgKapuFelulir(unittest.TestCase):
    """DT-F38k (1): a `cmd_rogzit` es a `cmd_szakasz_rogzit` rogzito aga a kapu_felulir() eredmenyevel.
    Ideiglenes munkatabla es DONTESEK.md (a modul MUNKA_UT / DONTESEK_UT konstansainak atiras a teszt idejere);
    a szakasz-/forras-fuggo segedfuggvenyek (forras, utofeldolgozas, terminologia) kiszurve, hogy a valodi
    adat/ es naplok/ fajlokhoz a teszt ne nyuljon. Azt fedi, hogy a rogzito aga a kapu_felulir() eredmenyere
    megall (SystemExit, a munkatabla bajtra valtozatlan), illetve a megjegyzes a rogzitett sorba kerul."""

    SZOVEG = '⟪1⟫ elso ⟪2⟫ masodik'
    EREDM_BUKAS = [('1_gorog_heber', 'RENDBEN', ''), ('11_konyvek', 'SERTES', ''), ('14_szakasz', 'RENDBEN', '')]
    MEGJ = 'kapu-felülbírálás: 11_konyvek (DT-F38k)'

    def setUp(self):
        import tempfile
        from unittest import mock
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self.munka = os.path.join(t, 'EMELES_munka.tsv')
        self.dont = os.path.join(t, 'DONTESEK.md')
        self.be = os.path.join(t, 'be.txt')
        with open(self.dont, 'w', encoding='utf-8') as fh:
            fh.write('| DT-F38k | cim | ... |\n')
        with open(self.be, 'w', encoding='utf-8') as fh:
            fh.write(self.SZOVEG + '\n')
        # korabbi sor egy MASIK Strongra: a rogzites nem torolheti, a megallas nem valtoztathatja
        E.tsv_ir(self.munka, E.FORDITASOK_FEJLEC, [
            {'szotar': 'BDB', 'strong': 'H9999', 'entry_id': 'H9999', 'jelentes_szam': 'teljes',
             'mezo': 'forditas_hu', 'forditas_hu': 'regi sor', 'allapot': 'sonnet'}])
        with open(self.munka, 'rb') as fh:
            self.munka_elotte = fh.read()
        szak = [{'sorszam': 1, 'hash': 'h1'}, {'sorszam': 2, 'hash': 'h2'}]
        self.eredm = list(self.EREDM_BUKAS)
        self.ok = False
        foltok = [
            mock.patch.object(E, 'MUNKA_UT', self.munka),
            mock.patch.object(E, 'DONTESEK_UT', self.dont),
            mock.patch.object(E, 'forras_szoveg', lambda s: ('H0001', 'forras')),
            mock.patch.object(E, 'szakasz_forras', lambda s: ('H0001', szak)),
            mock.patch.object(E, 'terminologia_szoveg', lambda: ('', 'tv-teszt')),
            mock.patch.object(E, 'utofeldolgoz', lambda sp, sz, kiv: (sz, [], self.eredm, self.ok)),
            mock.patch.object(E, 'utofeldolgoz_szakasz', lambda sp, sz, kiv: (sz, [], self.eredm, self.ok)),
        ]
        for f in foltok:
            f.start()
            self.addCleanup(f.stop)
        self.addCleanup(self.tmp.cleanup)

    def args(self, parancs, kapu=None, dontes=None):
        a = [parancs, 'H0001', '--be', self.be, '--allapot', 'sonnet', '--modell', 'm', '--datum', '2026.01.01']
        if kapu:
            a += ['--kapu-felulir', kapu]
        if dontes:
            a += ['--dontes', dontes]
        return parse(a)

    def munka_valtozatlan(self):
        with open(self.munka, 'rb') as fh:
            return fh.read() == self.munka_elotte

    def sorok(self):
        return list(E.tsv_dict_sorok(self.munka))

    def test_szakasz_rogzit_felulbiralas_nelkul_megall(self):
        with self.assertRaises(SystemExit) as k:
            E.cmd_szakasz_rogzit(self.args('szakasz_rogzit'))
        self.assertIn('kapuhiba', str(k.exception))
        self.assertTrue(self.munka_valtozatlan())

    def test_rogzit_felulbiralas_nelkul_megall(self):
        with self.assertRaises(SystemExit) as k:
            E.cmd_rogzit(self.args('rogzit'))
        self.assertIn('kapuhiba', str(k.exception))
        self.assertTrue(self.munka_valtozatlan())

    def test_szakasz_rogzit_ervenytelen_felulbiralas_megall(self):
        # nem letezo DT-sor: a kapu_felulir() SystemExit-je a rogzites elott, a tabla valtozatlan
        with self.assertRaises(SystemExit):
            E.cmd_szakasz_rogzit(self.args('szakasz_rogzit', '11_konyvek', 'DT-F38z'))
        self.assertTrue(self.munka_valtozatlan())

    def test_szakasz_rogzit_felulbiralassal_megjegyzes_a_sorokban(self):
        E.cmd_szakasz_rogzit(self.args('szakasz_rogzit', '11_konyvek', 'DT-F38k'))
        uj = [r for r in self.sorok() if r['strong'] == 'H0001']
        self.assertEqual([r['jelentes_szam'] for r in uj], ['sz1', 'sz2'])
        for r in uj:
            self.assertEqual(r['megjegyzes'], self.MEGJ)
        # a masik Strong sora megmaradt
        self.assertEqual([r['strong'] for r in self.sorok() if r['strong'] != 'H0001'], ['H9999'])

    def test_rogzit_felulbiralassal_megjegyzes_a_sorban(self):
        E.cmd_rogzit(self.args('rogzit', '11_konyvek', 'DT-F38k'))
        uj = [r for r in self.sorok() if r['strong'] == 'H0001']
        self.assertEqual(len(uj), 1)
        self.assertEqual(uj[0]['jelentes_szam'], 'teljes')
        self.assertEqual(uj[0]['megjegyzes'], self.MEGJ)

    def test_felulbiralas_megjegyzes_a_tobbi_megjegyzes_utan(self):
        a = parse(['szakasz_rogzit', 'H0001', '--be', self.be, '--allapot', 'sonnet', '--modell', 'm',
                   '--megjegyzes', 'elozo', '--kapu-felulir', '11_konyvek', '--dontes', 'DT-F38k'])
        E.cmd_szakasz_rogzit(a)
        for r in self.sorok():
            if r['strong'] == 'H0001':
                self.assertEqual(r['megjegyzes'], 'elozo; ' + self.MEGJ)

    def test_atment_kapuknal_nincs_megjegyzes(self):
        self.eredm = [(n, 'RENDBEN', '') for n, _, _ in self.EREDM_BUKAS]
        self.ok = True
        E.cmd_szakasz_rogzit(self.args('szakasz_rogzit'))
        for r in self.sorok():
            if r['strong'] == 'H0001':
                self.assertEqual(r['megjegyzes'], '')


class BdbJavitasKapu(unittest.TestCase):
    """F67: az utofeldolgoz / utofeldolgoz_szakasz atadja a Strongot a 17_bdb_javitas kapunak."""

    def test_utofeldolgoz_bdb_kapusora(self):
        nevek = [n for n, _, _ in E.utofeldolgoz('H7223', 'szo')[2]]
        self.assertIn('17_bdb_javitas', nevek)

    def test_utofeldolgoz_thayer_nem_kap(self):
        nevek = [n for n, _, _ in E.utofeldolgoz('G0012', 'szo')[2]]
        self.assertNotIn('17_bdb_javitas', nevek)

    def test_kapu_felulir_a_17_kapura(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            dont = os.path.join(d, 'DONTESEK.md')
            with open(dont, 'w', encoding='utf-8') as fh:
                fh.write('| DT-F38s | cim | ... |\n')
            a = parse(['rogzit', 'H7223', '--be', 'x.txt', '--allapot', 'sonnet', '--modell', 'm',
                       '--kapu-felulir', '17_bdb_javitas', '--dontes', 'DT-F38s'])
            e = [('11_konyvek', 'RENDBEN', ''), ('17_bdb_javitas', 'SERTES', '')]
            self.assertIn('17_bdb_javitas', E.kapu_felulir(a, e, dont))


if __name__ == '__main__':
    unittest.main(verbosity=2)
