#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teszt_bdb_psi_javit.py — F34: a BDB-psi csere-tabla ujrafuttathato a LEFORDITOTT szovegen.

Futtatas a repo gyokerebol: python eszkozok/teszt_bdb_psi_javit.py
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_psi_javit as J

CSERE = [('H7585', 'Ezek 73:23', 'Psa 73:23'), ('H7585', 'Ezek 73:25', 'Psa 73:25'),
         ('H7843', 'Prov 75:1', 'Psa 75:1'), ('H0430', 'Job 97:7', 'Psa 97:7')]


class ForditasonUjrafuttat(unittest.TestCase):
    def test_hibas_hely_javul_a_tobbi_bajtazonos(self):
        hu = 'sír; Ez 73:23 és Ez 73:25 (vö. Ez 16:10), Jób 97:7 itt nem érintett'
        uj, ki = J.csere_forditason(hu, 'H7585', CSERE)
        self.assertEqual(uj, 'sír; Zsolt 73:23 és Zsolt 73:25 (vö. Ez 16:10), Jób 97:7 itt nem érintett')
        self.assertEqual(len(ki), 2)

    def test_mas_szocikk_nem_valtozik(self):
        hu = 'Ez 73:23'
        self.assertEqual(J.csere_forditason(hu, 'H1234', CSERE)[0], hu)

    def test_idempotens(self):
        egyszer = J.csere_forditason('Péld 75:1', 'H7843', CSERE)[0]
        self.assertEqual(egyszer, 'Zsolt 75:1')
        self.assertEqual(J.csere_forditason(egyszer, 'H7843', CSERE)[0], egyszer)

    def test_hosszabb_versszam_nem_csonkul(self):
        # a Péld 75:1 tokent nem szabad a Péld 75:12-ben megtalalni
        hu = 'Péld 75:12'
        self.assertEqual(J.csere_forditason(hu, 'H7843', CSERE)[0], hu)

    def test_a_tabla_a_valodi_adaton_nem_rontja_a_kihagyott_sorokat(self):
        # a --forditas mod a VEDETT sorokat (81, 84, 85) nem irja at
        self.assertEqual(J.VEDETT_SOROK, {81, 84, 85})


class VersTabla(unittest.TestCase):
    def test_zsoltar_versszamok(self):
        vt = J.vers_tabla()
        self.assertEqual(len(vt), 150)
        self.assertEqual(max(vt[119]), 176)
        self.assertIn(23, vt[73])
        self.assertNotIn(48, vt[81])


if __name__ == '__main__':
    unittest.main()
