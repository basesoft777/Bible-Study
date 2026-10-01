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


class PontosKulcsolas(unittest.TestCase):
    """DT26 #15/#26: a két „compare” sort a kulcs választja szét
    (`compare` → vö., `מִן compare` → comparativus)."""

    TERM = [{'angol': 'compare', 'magyar': 'vö.'},
            {'angol': 'מִן compare', 'magyar': 'comparativus'}]

    def _e(self, forras, forditas):
        return K.ellenoriz_terminologia(forras, forditas, self.TERM, [])

    def test_csak_min_compare_comparativust_kovetel(self):
        forras = 'be swift, with מִן compare, of warriors 2Sam 1:23'
        self.assertEqual(self._e(forras, 'gyorsnak lenni, a מִן comparativusszal, 2Sám 1:23')[0], 'RENDBEN')

    def test_min_compare_comparativus_nelkul_sertes(self):
        forras = 'be swift, with מִן compare, of warriors 2Sam 1:23'
        e, r = self._e(forras, 'gyorsnak lenni, vö. 2Sám 1:23')
        self.assertEqual(e, 'SERTES')
        self.assertIn('מִן compare -> comparativus', r)
        self.assertNotIn('compare -> vö.', r.replace('מִן compare -> comparativus', ''))

    def test_onallo_compare_vo_t_kovetel(self):
        forras = 'with מִן compare Ezek 8:17; compare Dr'
        e, r = self._e(forras, 'מִן comparativusszal Ez 8:17; Dr')
        self.assertEqual(e, 'SERTES')
        self.assertIn('compare -> vö. hianyzik', r)
        self.assertEqual(self._e(forras, 'מִן comparativusszal Ez 8:17; vö. Dr')[0], 'RENDBEN')


class KapuOszlop(unittest.TestCase):
    """DT27: a terminologia.tsv `kapu` oszlopa (igen/nem; hiányzó = igen)."""

    FORRAS = 'so read also 1:21; compare Dr'

    def _e(self, term):
        return K.ellenoriz_terminologia(self.FORRAS, 'így olvasandó az 1:21-ben is; Dr', term, [])

    def test_kapu_nem_nem_ad_sertest(self):
        term = [{'angol': 'read', 'magyar': 'olv.', 'kapu': 'nem'},
                {'angol': 'compare', 'magyar': 'vö.', 'kapu': 'nem'}]
        self.assertEqual(self._e(term)[0], 'RENDBEN')

    def test_kapu_igen_sertest_ad(self):
        e, r = self._e([{'angol': 'read', 'magyar': 'olv.', 'kapu': 'igen'}])
        self.assertEqual(e, 'SERTES')
        self.assertIn('read -> olv.', r)

    def test_hianyzo_es_ures_ertek_igen(self):
        self.assertEqual(self._e([{'angol': 'read', 'magyar': 'olv.'}])[0], 'SERTES')
        self.assertEqual(self._e([{'angol': 'read', 'magyar': 'olv.', 'kapu': ''}])[0], 'SERTES')
        self.assertTrue(K.kapus_sor({'kapu': ' '}))
        self.assertFalse(K.kapus_sor({'kapu': 'nem'}))

    def test_kapu_nem_hosszabb_kulcs_nem_von_el(self):
        # ELLENOR_DT27 1. (a) opció: a kapu=nem `which see` belsejében álló `see`
        # a kapu=igen „see → l.” soré marad
        term = [{'angol': 'see', 'magyar': 'l.', 'kapu': 'igen'},
                {'angol': 'which see', 'magyar': 'l. ott', 'kapu': 'nem'}]
        forras = 'Rom 8:21 (on which see δουλεία)'
        e, r = K.ellenoriz_terminologia(forras, 'Róm 8:21 (ehhez δουλεία)', term, [])
        self.assertEqual(e, 'SERTES')
        self.assertIn('see -> l. hianyzik', r)
        self.assertNotIn('which see', r)
        self.assertEqual(K.ellenoriz_terminologia(forras, 'Róm 8:21 (ehhez l. δουλεία)', term, [])[0],
                         'RENDBEN')

    def test_kapu_igen_hosszabb_kulcs_elvon(self):
        # a kapu=igen hosszabb kulcs (`which see`) továbbra is elvonja a rövidebbet
        term = [{'angol': 'see', 'magyar': 'l.', 'kapu': 'igen'},
                {'angol': 'which see', 'magyar': 'l. ott', 'kapu': 'igen'}]
        forras = '(λύτρον, which see)'
        e, r = K.ellenoriz_terminologia(forras, '(λύτρον, vö.)', term, [])
        self.assertEqual(e, 'SERTES')
        self.assertIn('which see -> l. ott', r)
        self.assertNotIn('; see -> l.', r)
        self.assertFalse(r.startswith('see -> l.'))

    def test_prompt_tartalmazza_a_kapu_nem_sorokat(self):
        import emeles
        # a prompt a tábla MINDEN sorát tartalmazza, a kapu értékétől függetlenül
        szoveg, _ = emeles.terminologia_szoveg()
        for t in emeles.tsv_dict_sorok(emeles.TERMINOLOGIA_UT):
            self.assertIn('`%s` = %s' % (t['angol'], t['magyar']), szoveg, t.get('kapu'))


class Konyvek(unittest.TestCase):
    def test_jsir_es_sir(self):
        self.assertEqual(K.ellenoriz_konyvek('Lam 3:57; Sir. 1:3', 'JSir 3:57; Sir 1:3')[0], 'RENDBEN')
        self.assertEqual(K.ellenoriz_konyvek('Lam 3:57', 'Sir 3:57')[0], 'SERTES')


if __name__ == '__main__':
    unittest.main(verbosity=2)
