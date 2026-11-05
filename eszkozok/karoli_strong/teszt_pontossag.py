#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F172 — a pontosságmérés tesztjei.

F172.1: a mintavétel determinizmusa (ugyanaz a mag -> ugyanaz a minta;
más mag -> más minta; a rétegek mérete egymástól független).

Futtatás: python eszkozok/karoli_strong/teszt_pontossag.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pontossag_minta as pm  # noqa: E402


def _mu_keret():
    """Kis műkeret: rétegenként 50 sor."""
    ki = []
    for rt in pm.RETEGEK:
        for i in range(50):
            ki.append({'reteg': rt, 'konyv': 'X', 'vers': 'X %d:1' % i, 'hu_sorszam': '1',
                       'hu_szo': 'a', 'er_sorszam': str(i), 'er_szo': 'b', 'strong': 'H0001',
                       'bizonyossag': 'alacsony', 'forras': 'S', 'morfema': '0', 'nem_tr': '0'})
    return ki


class Mintavetel(unittest.TestCase):
    def test_azonos_mag_azonos_minta(self):
        k = _mu_keret()
        self.assertEqual(pm.mintavetel(k, 10, 1), pm.mintavetel(k, 10, 1))

    def test_mas_mag_mas_minta(self):
        k = _mu_keret()
        self.assertNotEqual([r['vers'] for r in pm.mintavetel(k, 10, 1)],
                            [r['vers'] for r in pm.mintavetel(k, 10, 2)])

    def test_reteg_meret(self):
        m = pm.mintavetel(_mu_keret(), 10, 1)
        for rt in pm.RETEGEK:
            self.assertEqual(sum(1 for r in m if r['reteg'] == rt), 10)

    def test_retegek_fuggetlenek(self):
        # egy réteg kivétele a keretből nem változtatja a többi réteg mintáját
        k = _mu_keret()
        k2 = [r for r in k if r['reteg'] != 'OSZ_mozes']
        a = [r for r in pm.mintavetel(k, 10, 1) if r['reteg'] == 'USZ_level']
        b = [r for r in pm.mintavetel(k2, 10, 1) if r['reteg'] == 'USZ_level']
        self.assertEqual(a, b)

    def test_minta_fajl_reprodukalhato(self):
        ut = os.path.join(pm.KIMENET, 'minta.tsv')
        if not os.path.exists(ut):
            self.skipTest('nincs f172/minta.tsv')
        _, sorok = pm._tabla(ut)
        uj = pm.mintavetel(pm.keret_parok(), pm.DARAB, pm.MAG)
        self.assertEqual([r['minta_id'] + r['vers'] + r['hu_sorszam'] + r['er_sorszam'] for r in sorok],
                         [r['minta_id'] + r['vers'] + r['hu_sorszam'] + r['er_sorszam'] for r in uj])


import pontossag_meres as pme  # noqa: E402


class Meres(unittest.TestCase):
    def test_wilson_ismert_ertek(self):
        lo, hi = pme.wilson(95, 100)
        self.assertAlmostEqual(lo, 0.8883, places=3)
        self.assertAlmostEqual(hi, 0.9785, places=3)

    def test_wilson_szelsok(self):
        lo, hi = pme.wilson(100, 100)
        self.assertEqual(hi, 1.0)
        self.assertLess(lo, 1.0)
        lo, hi = pme.wilson(0, 50)
        self.assertAlmostEqual(lo, 0.0, places=12)

    def test_retegzett_egy_reteg(self):
        p, lo, hi, n = pme.retegzett({'A': (90, 100)}, {'A': 1000})
        self.assertAlmostEqual(p, 0.9)
        self.assertEqual(n, 100)
        self.assertLess(lo, 0.9)
        self.assertGreater(hi, 0.9)

    def test_retegzett_sulyok(self):
        # A: 100% (súly 3), B: 50% (súly 1) -> 0,875, a mintaméret nem számít bele
        p, _, _, _ = pme.retegzett({'A': (10, 10), 'B': (50, 100)}, {'A': 300, 'B': 100})
        self.assertAlmostEqual(p, 0.875)

    def test_retegzett_ures_reteg_kimarad(self):
        p, _, _, n = pme.retegzett({'A': (9, 10), 'B': (0, 0)}, {'A': 1, 'B': 1000})
        self.assertAlmostEqual(p, 0.9)
        self.assertEqual(n, 10)

    def test_hibatipus(self):
        strong = {1: 'H9001', 2: 'H1254', 3: 'H0430', 5: 'H0430'}.get
        self.assertEqual(pme.hibatipus(2, 'H1254', set(), strong), 'fölös pár')
        self.assertEqual(pme.hibatipus(5, 'H0430', {3}, strong), 'azonos lexéma, más előfordulás')
        self.assertEqual(pme.hibatipus(1, 'H9001', {2}, strong), 'egység határa')
        self.assertEqual(pme.hibatipus(5, 'H0430', {2}, strong), 'rossz szó a versben')

    def test_strong_norm(self):
        self.assertEqual(pme._strong_norm('H0430'), pme._strong_norm('H430'))
        self.assertEqual(pme._strong_norm('G0086'), 'G86')


import tempfile  # noqa: E402

import pontossag_kulso as pk  # noqa: E402


class Kulso(unittest.TestCase):
    """Szintetikus, saját bemenet (a zárt forrás szövege nem kerül a tesztbe)."""

    def _fajl(self, szoveg):
        fd, ut = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(szoveg)
        self.addCleanup(os.remove, ut)
        return ut

    def test_elemzes_szo_utani_szam(self):
        ut = self._fajl('9Kv 1:1\nAlfa 1234 béta, 2077, 8002 gamma.6440 delta 5493, 0, 8686, 0 el.5493, 8686  *(7126, 8686)\n')
        v, megj = pk.bd_elemez(ut, usz=False)
        self.assertEqual(megj, 1)
        self.assertEqual(v['9Kv 1:1'], [('Alfa', {1234}), ('béta', {2077, 8002}), ('gamma', {6440}),
                                        ('delta', {5493}), ('el', {5493})])

    def test_elemzes_gorog_igealak_kod(self):
        ut = self._fajl('9Kv 2:3\nszó 3056, 5656 más 5624\n')
        v, _ = pk.bd_elemez(ut, usz=True)
        self.assertEqual(v['9Kv 2:3'], [('szó', {3056}), ('más', {5624})])

    def test_igazitas_osszevonas_es_helyesiras(self):
        sajat = ['a', 'mely', 'nősténynyel', 'jő']
        bd = [('amely', {834}), ('nősténnyel', {5347}), ('jő', set())]
        m = pk.igazit(sajat, bd)
        self.assertEqual(m, {1: {834}, 2: {834}, 3: {5347}, 4: set()})

    def test_igazitas_nem_igazithato(self):
        m = pk.igazit(['egy', 'kettő', 'három'], [('egy', {1}), ('négy', {4}), ('öt', {5}), ('három', {3})])
        self.assertNotIn(2, m)
        self.assertEqual(m[1], {1})
        self.assertEqual(m[3], {3})


if __name__ == '__main__':
    unittest.main(verbosity=2)
