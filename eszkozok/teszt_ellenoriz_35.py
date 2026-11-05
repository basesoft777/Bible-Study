#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_35.py -- F168: az eszkozok/ellenoriz.py 35.
szabályának (közlemény-hivatkozások a lapon) és a generátor közlemény-
szövegének (lexikon_general.kolofon_kozlemenyek) tesztjei.

Ideiglenes (a repón kívüli) lexikon/ és kozlemeny/ könyvtárban fut; a lap a
repó élő ISTENTISZT-001 lapjának másolata (minden hivatkozással), a negatív
esetekben egy-egy hivatkozás kivéve vagy GitHub-URL betéve.

    python eszkozok/teszt_ellenoriz_35.py
"""

import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ellenoriz as E  # noqa: E402
import lexikon_general as LG  # noqa: E402

MOTIVUM = 'ISTENTISZT-001'
LAP = os.path.join(E.ROOT, 'lexikon', '%s_TUDOMANYOS.md' % MOTIVUM)
KOZLEMENYEK = ('MI_NYILATKOZAT.md', 'HAYS_LEKEPEZES.md', 'PARDES_RECEPCIOS_KERET.md', 'KOZEL_KELETI_HATAR.md')


def _lap():
    with open(LAP, encoding='utf-8') as fh:
        return fh.read().replace('\r\n', '\n')


class Szabaly35(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='teszt_ellenoriz_35_')
        self.adat = os.path.join(self.tmp, 'adat')
        self.lex = os.path.join(self.tmp, 'lexikon')
        os.makedirs(self.adat)
        os.makedirs(self.lex)
        os.makedirs(os.path.join(self.tmp, 'kozlemeny'))
        for nev in KOZLEMENYEK:
            open(os.path.join(self.tmp, 'kozlemeny', nev), 'w', encoding='utf-8').close()
        open(os.path.join(self.tmp, 'CITATION.cff'), 'w', encoding='utf-8').close()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _fut(self, lap):
        with open(os.path.join(self.lex, MOTIVUM + '_TUDOMANYOS.md'), 'w', encoding='utf-8') as fh:
            fh.write(lap)
        return E.szabaly35_kozlemeny_hivatkozas(self.adat, self.lex)

    def test_elo_lap_rendben(self):
        sor = self._fut(_lap())
        self.assertEqual(sor.verdict, 'RENDBEN', sor.peldak)

    def test_hianyzo_mi_hivatkozas(self):
        sor = self._fut(_lap().replace('](../kozlemeny/MI_NYILATKOZAT.md)', ']'))
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertTrue(any('MI-nyilatkozat' in p for p in sor.peldak), sor.peldak)

    def test_hianyzo_idezes(self):
        sor = self._fut(_lap().replace('**Hogyan idézd.**', '**Idézés.**'))
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertTrue(any('Hogyan idézd' in p for p in sor.peldak), sor.peldak)

    def test_hianyzo_nyilt_adat_mutato(self):
        sor = self._fut(_lap().replace(LG.NYILT_ADAT_MUTATO, 'A lap adatai'))
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertTrue(any('nyílt adatkészletre' in p for p in sor.peldak), sor.peldak)

    def test_hianyzo_recepcios_keret(self):
        sor = self._fut(_lap().replace('](../kozlemeny/PARDES_RECEPCIOS_KERET.md)', ']'))
        self.assertEqual(sor.verdict, 'SÉRTÉS')

    def test_nem_letezo_kozlemeny(self):
        os.remove(os.path.join(self.tmp, 'kozlemeny', 'HAYS_LEKEPEZES.md'))
        sor = self._fut(_lap())
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertTrue(any('HAYS_LEKEPEZES.md' in p for p in sor.peldak), sor.peldak)

    def test_github_url(self):
        sor = self._fut(_lap() + '\n- Fájl: `https://github.com/Basesoft777/Bible-Study/blob/main/x.md`\n')
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertTrue(any('GitHub' in p for p in sor.peldak), sor.peldak)


class KolofonKozlemenyek(unittest.TestCase):
    M = {'id': 'X-001', 'cim': 'Próba'}

    def test_kiadas_nelkul(self):
        mi, bek = LG.kolofon_kozlemenyek(self.M, [], None)
        self.assertIn(LG.KOZLEMENY['mi'], mi)
        self.assertIn('még nem idézhető', bek[0])
        self.assertIn(LG.KANONIKUS_FORRAS_HELYORZO, bek[0])
        self.assertIn(LG.DOI_HELYORZO, bek[0])
        self.assertIn(LG.NYILT_ADAT_MUTATO, bek[0])
        self.assertNotIn('CITATION.cff', bek[0])
        self.assertNotIn('minden jog fenntartva', bek[0])
        self.assertNotIn('github', ''.join(bek).lower())
        self.assertNotIn('Ennél a motívumnál', bek[2])

    def test_kiadassal_es_kozel_keleti_sorral(self):
        mi, bek = LG.kolofon_kozlemenyek(self.M, [{'kiadas': '2', 'datum': '2026.11.04'}],
                                         {'id': 'X-001', 'proza_emlites': 'az ugariti szövegek'})
        self.assertIn('2. kiadás (2026.11.04)', bek[0])
        self.assertIn('Ennél a motívumnál', bek[2])
        self.assertIn('(az ugariti szövegek)', bek[2])

    def test_kozel_keleti_sor_emlites_nelkul(self):
        _, bek = LG.kolofon_kozlemenyek(self.M, [], {'id': 'X-001', 'proza_emlites': ''})
        self.assertIn('Ennél a motívumnál', bek[2])
        self.assertNotIn('értelmező szöveg közel-keleti hátteret említ', bek[2])


if __name__ == '__main__':
    unittest.main(verbosity=2)
