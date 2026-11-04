#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_28.py -- DT-F123v: az eszkozok/ellenoriz.py 28.
szabalya (adat nelkuli szerkezeti blokk nem allhat olvasoi lapon) es a
generator opcionalis-res kezelese (lexikon_general.OPCIONALIS_RESEK).

A repo elo adataval fut (lexikon/ISTENTISZT-001_TUDOMANYOS.md, adat/), a
lapot csak memoriaban modositja.

    python eszkozok/teszt_ellenoriz_28.py
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
import lexikon_general as LG  # noqa: E402

MOTIVUM = 'ISTENTISZT-001'
M = {'id': MOTIVUM}
LAP = os.path.join(E.ROOT, 'lexikon', '%s_TUDOMANYOS.md' % MOTIVUM)


def _lap():
    with open(LAP, encoding='utf-8') as fh:
        return fh.read().replace('\r\n', '\n')


def _fejlec(res):
    return LG.res_forras_sorok()[(MOTIVUM, res)]['fejlec']


def _2b_beszur(lap, torzs):
    """A 2/b rés a Miért fontos fejléce elé, ahogy a 2026-11-04 előtti generátor írta."""
    kov = _fejlec('miert_fontos')
    span = '%s\n\n%s\n\n' % (_fejlec('2b'), torzs)
    i = lap.index(kov, lap.index('## 2. Szótári háttér'))
    return lap[:i] + span + lap[i:]


REGI_URES = ('A fenti szótári anyagon túli, kiegészítő szótári adatok. Ha nincs ilyen adat, ezt egy sor '
             'jelzi.<!-- olvasói -->\n\n<!-- GENERÁLT-RÉS: 2b | general.py --cel lexikon | forrás: '
             'adat/lexikon_hivatkozasok.tsv -->\n\n' + LG.SZERKEZETI_HELYORZOK['2b'][1] + '\n\n'
             '*Proveniencia: `scope=id:%s | forras=adat/lexikon_hivatkozasok.tsv | ts=2026-11-03`*' % MOTIVUM)


class Szabaly28(unittest.TestCase):
    def setUp(self):
        self.lap = _lap()

    def test_mai_lap_rendben(self):
        # a generátor a lapra nem tette ki az adat nélküli 2/b-t
        self.assertNotIn(_fejlec('2b'), self.lap)
        self.assertEqual(LG.lap_ures_szerkezeti_resek(self.lap, M), [])

    def test_regi_ures_2b_serteses(self):
        lap = _2b_beszur(self.lap, REGI_URES)
        self.assertEqual(LG.lap_ures_szerkezeti_resek(lap, M), ['2b'])

    def test_g15_helyorzo_serteses(self):
        lap = _2b_beszur(self.lap, LG.SZERKEZETI_HELYORZOK['2b'][0])
        self.assertEqual(LG.lap_ures_szerkezeti_resek(lap, M), ['2b'])

    def test_adattal_rendben(self):
        torzs = ('<!-- GENERÁLT-RÉS: 2b | general.py --cel lexikon | forrás: adat/lexikon_hivatkozasok.tsv -->\n\n'
                 '**MCGED G1941 — (részlet)**\n\n> call upon\n\n*Forrás: konkordancia/proba.tsv*\n\n'
                 '*Proveniencia: `scope=id:%s | forras=adat/lexikon_hivatkozasok.tsv | ts=2026-11-04`*' % MOTIVUM)
        self.assertEqual(LG.lap_ures_szerkezeti_resek(_2b_beszur(self.lap, torzs), M), [])

    def test_kutatasi_ures_eredmeny_nem_erintett(self):
        # a kimondott kutatási üres eredmény (CLAUDE.md 3. szabály) nem szerkezeti blokk: a szabály nem nézi
        self.assertNotIn('minosites', LG.OPCIONALIS_RESEK)
        self.assertNotIn('alatamasztas', LG.OPCIONALIS_RESEK)
        lap = self.lap.replace(_fejlec('alatamasztas') + '\n\n',
                               _fejlec('alatamasztas') + '\n\n' + LG.ALATAMASZTAS_NINCS_KAPCSOLAT + '\n\n', 1)
        self.assertEqual(LG.lap_ures_szerkezeti_resek(lap, M), [])


class SzabalyARepon(unittest.TestCase):
    def test_migralt_lap_gatol_regi_lap_jelentes(self):
        # migrált lapon (E28-lista) adat nélküli 2/b nincs; a régi sablonú lap találata JELENTÉS (DT507 (a))
        sor = E.szabaly28_ures_szerkezeti_blokk(E.ALAPERTELMEZETT_ADAT)
        self.assertIn(sor.verdict, ('RENDBEN', 'JELENTÉS'))
        self.assertTrue(all('nem migrált lap' in p for p in sor.peldak), sor.peldak)
        self.assertFalse(any(p.startswith(MOTIVUM) for p in sor.peldak))


class Generator(unittest.TestCase):
    def setUp(self):
        self.lap = _lap()

    def test_regi_ures_2b_lekerul(self):
        lap = _2b_beszur(self.lap, REGI_URES)
        self.assertEqual(LG.opcionalis_resek_torol(lap, M, ['2b']), self.lap)

    def test_visszaallit_es_torol_fixpont(self):
        # a kihagyott rés fejléce a határkereséshez visszakerül, utána a törlés a lapot változatlanul adja vissza
        vissza = LG.opcionalis_res_visszaallit(self.lap, M)
        self.assertIn(_fejlec('2b') + '\n\n' + _fejlec('miert_fontos'), vissza)
        self.assertEqual(LG.opcionalis_res_visszaallit(vissza, M), vissza)
        self.assertEqual(LG.opcionalis_resek_torol(vissza, M, ['2b']), self.lap)

    def test_res_torzs_lapbol_hianyzo_res(self):
        self.assertEqual(LG.res_torzs_lapbol(self.lap, M, '2b'), '')
        # a többi rés határa a kihagyott 2/b mellett is olvasható
        self.assertTrue(LG.res_torzs_lapbol(self.lap, M, 'miert_fontos'))


if __name__ == '__main__':
    unittest.main()
