#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_bdb_adatblokk.py -- F56 (BDB_ADATBLOKK) tesztek: a Strong-
normalizalas (K2), az adatblokk szerkezete es proveniencia-sorai (K1), a
fejezetszam-javitotabla algoritmusa es a H7223 teszteset (K3), a visszamenoleges
atvezetes szovegcsereje (K5).

    python eszkozok/teszt_bdb_adatblokk.py
"""

import os
import re
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bdb_adatblokk as B  # noqa: E402

TS = '2026-10-06T00:00:00Z'


class StrongNormalizalas(unittest.TestCase):
    def test_alakok_egyeznek(self):
        for alak in ('H2617', 'H02617', '2617', 'h2617', ' H2617 '):
            self.assertEqual(B.strong_norm(alak), 'H2617')
            self.assertEqual(B.strong_szam(alak), 2617)
            self.assertEqual(B.strong_padded(alak), 'H2617')

    def test_kis_szam_es_homograf(self):
        self.assertEqual(B.strong_padded('H1'), 'H0001')
        self.assertEqual(B.strong_padded('1'), 'H0001')
        self.assertEqual(B.strong_padded('H90a'), 'H0090a')
        self.assertEqual(B.strong_szam('H0090a'), 90)

    def test_hibas(self):
        self.assertIsNone(B.strong_norm('G26'))
        self.assertIsNone(B.strong_norm('abc'))
        self.assertIsNone(B.strong_norm(''))

    def test_nincs_nema_nemtalalat(self):
        # K2: ismert Strong-szamok, amelyeknek van Karoli-parjuk, mindharom alakban
        for s in ('H2617', 'H5785', 'H8057'):
            for alak in (s, s.replace('H', 'H0'), s[1:]):
                self.assertTrue(B.karoli_alakok(B.strong_szam(alak)), '%s (%s)' % (s, alak))
                blokk = B.blokk_epit(alak, TS)
                self.assertNotIn('[NINCS KÁROLI-ALAK]', blokk, '%s (%s)' % (s, alak))
                self.assertIn('ADATBLOKK %s ' % s, blokk)


class Blokk(unittest.TestCase):
    def test_szakaszok_es_proveniencia(self):
        b = B.blokk_epit('H2617', TS)
        for jel in ('**1. ', '**2. ', '**3. ', '**4. ', '**5. ', '**6. '):
            self.assertIn(jel, b)
        # minden szakasz vegen proveniencia-sor
        self.assertEqual(len(re.findall(r'^\*proveniencia: scope=H2617 \| forras=.+ \| ts=%s\*$' % TS,
                                        b, re.M)), 6)

    def test_meretkorlat(self):
        for s in ('H2617', 'H3548', 'H7121', 'H0001', 'H9009', 'H1961'):
            self.assertLessEqual(len(B.blokk_epit(s, TS)), B.BLOKK_MAX, s)

    def test_nincs_karoli_alak(self):
        # H0426 (arami 'Isten'): a lefedett konyvekben nincs Karoli-par
        b = B.blokk_epit('H0426', TS)
        self.assertIn('[NINCS KÁROLI-ALAK]', b)
        self.assertEqual(len(re.findall(r'^\*proveniencia:', b, re.M)), 6)

    def test_ures_szakaszok_jelzese(self):
        b = B.blokk_epit('H0256', TS)       # nincs LXX-hid, nincs Karoli-par
        self.assertIn('**3. LXX-megfelelő**\n—', b)

    def test_pelda_idezet_szo_szerinti(self):
        # a kiemelt szo a hu_sorszam-adik token, az idezet a Karoli-versbol
        b = B.blokk_epit('H2617', TS)
        m = re.search(r'1Móz 24:14 „(.+?)”', b)
        self.assertIsNotNone(m)
        szoveg = m.group(1).replace('**', '').strip('.').replace('...', '')
        self.assertIn(szoveg.strip(), B.karoli_vers()['1Móz 24:14'])

    def test_hibas_strong(self):
        with self.assertRaises(ValueError):
            B.blokk_epit('G26', TS)


class Javitas(unittest.TestCase):
    def test_jeloltek_elgepeles(self):
        self.assertIn(7, B.fejezet_jeloltek('17', 12))
        self.assertIn(1, B.fejezet_jeloltek('17', 12))
        self.assertNotIn(17, B.fejezet_jeloltek('17', 12))
        self.assertNotIn(0, B.fejezet_jeloltek('10', 12))

    def test_h7223(self):
        # K3: Eccl 17:10 -> Eccl 7:10 (H7223, `javitva`)
        sorok = B.javitas_sorok('H7223', B.bdb_szocikkek()['H7223'], TS)
        s = [x for x in sorok if x['forras_hivatkozas'] == 'Eccl 17:10']
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0]['allapot'], 'javitva')
        self.assertEqual(s[0]['javitott_hivatkozas'], 'Préd 7:10')
        self.assertTrue(s[0]['indok'])
        self.assertIn('scope=H7223', s[0]['proveniencia'])

    def test_nem_letezo_fejezet_nem_talalgat(self):
        # ahol nincs jelolt, vagy tobb van, a sor jelolt_marad, javitott hivatkozas nelkul
        sorok = B.javitas_sorok('H0834', B.bdb_szocikkek()['H0834'], TS)
        for s in sorok:
            if s['allapot'] == 'jelolt_marad':
                self.assertEqual(s['javitott_hivatkozas'], '')

    def test_tabla_elemei(self):
        t = B.javitotabla_olvas()
        self.assertTrue(t)
        for sp, sorok in t.items():
            for s in sorok:
                self.assertIn(s['allapot'], ('javitva', 'jelolt_marad'))
                self.assertTrue(s['indok'] and s['proveniencia'])
                self.assertEqual(bool(s['javitott_hivatkozas']), s['allapot'] == 'javitva')

    def test_blokk_javitas_szakasz(self):
        b = B.blokk_epit('H7223', TS)
        self.assertIn('a forrásban `Eccl 17:10` → helyesen `Préd 7:10`', b)


class Atvezetes(unittest.TestCase):
    SOR = [{'forras_hivatkozas': 'Eccl 17:10', 'javitott_hivatkozas': 'Préd 7:10'}]

    def test_csere(self):
        uj, cs = B.atvezet_szoveg('mint Préd 17:10; Zsolt 79:8 és tovább', self.SOR)
        self.assertEqual(uj, 'mint Préd 7:10 [BDB: Préd 17:10]; Zsolt 79:8 és tovább')
        self.assertEqual(cs, [('Préd 17:10', 'Préd 7:10', 1)])

    def test_csak_a_hivatkozas(self):
        # nem erinti a hosszabb szamot es az mar atvezetett alakot
        uj, cs = B.atvezet_szoveg('Préd 17:100 es Préd 117:10', self.SOR)
        self.assertEqual(uj, 'Préd 17:100 es Préd 117:10')
        self.assertEqual(cs, [])

    def test_ketszeri_futtatas_idempotens(self):
        egyszer, _ = B.atvezet_szoveg('Préd 17:10', self.SOR)
        ketszer, cs = B.atvezet_szoveg(egyszer, self.SOR)
        self.assertEqual(egyszer, ketszer)
        self.assertEqual(cs, [])


if __name__ == '__main__':
    unittest.main()
