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

    def test_vedett_sor_mezokulcsos(self):
        kulcs = dict(szotar='BDB', strong='H8034', entry_id='H8034', jelentes_szam='teljes', mezo='forditas_hu')
        self.assertTrue(J.vedett(kulcs))
        # negativ: mas strong / mas mezo / mas jelentes_szam NEM vedett (a fajlsorszam nem szamit)
        for mezo, ertek in (('strong', 'H7585'), ('mezo', 'definicio_hu'), ('jelentes_szam', 'reszlet')):
            k2 = dict(kulcs)
            k2[mezo] = ertek
            self.assertFalse(J.vedett(k2), mezo)

    def test_negativ_nem_psi_dan_hely_kimarad_a_tablabol(self):
        # a Dt->Dan hiba nem psi: a csere-tabla nem tartalmazhat Dan-kulcsot
        for sor in open('naplok/F34_M2_csere.tsv', encoding='utf-8').read().split(chr(10))[1:]:
            if sor:
                self.assertFalse(sor.split(chr(9))[1].startswith(J.NEM_PSI_KONYV), sor)

    def test_negativ_hibas_token_nem_lesz_zsolt_masik_szocikkben(self):
        self.assertEqual(J.csere_forditason('Ez 73:23', 'H8034', CSERE)[0], 'Ez 73:23')


class VersTabla(unittest.TestCase):
    def test_zsoltar_versszamok(self):
        vt = J.vers_tabla()
        self.assertEqual(len(vt), 150)
        self.assertEqual(max(vt[119]), 176)
        self.assertIn(23, vt[73])
        self.assertNotIn(48, vt[81])


if __name__ == '__main__':
    unittest.main()
