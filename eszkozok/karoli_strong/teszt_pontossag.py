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


if __name__ == '__main__':
    unittest.main(verbosity=2)
