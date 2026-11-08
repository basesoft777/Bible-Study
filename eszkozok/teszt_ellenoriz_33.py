#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_33.py -- az ellenoriz.py 33. szabályának tesztjei (F123.TUD1B): az összesítő jelöltsor
versszáma géppel olvasható a `forras_kereses`-ből, és egyezik az indoklás számával. Az 1/b. összesítő mondatának
versszám-tesztjei is itt futnak (szerep_kizart, olvasoi_kovetkeztetes), mert a CI ezt a fájlt hívja.

Ideiglenes (a repón kívüli) adat-könyvtárban fut; a valódi táblán a szabály RENDBEN.

    python eszkozok/teszt_ellenoriz_33.py
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
from teszt_szerep_kizart import TestVersszam  # noqa: E402,F401  (a CI-ben is fusson)
from teszt_olvasoi_kovetkeztetes import Szovegek  # noqa: E402,F401
from teszt_ellenoriz_36 import Szabaly36  # noqa: E402,F401  (F123.HAMART3: a 36. szabály is fusson a CI-ben)
from teszt_ellenoriz_37_38 import Szabaly37, Szabaly38  # noqa: E402,F401  (F123.HAMART3 javítókör: 37., 38.)

FEJ = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'karoli_szo', 'azonositas_modja', 'megbizhatosag',
       'datum', 'jelolt_tipus', 'cel_id', 'cel_igehely', 'cel_alpont', 'dontes_ref']
GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSOP = ('F123 U1 teljesség-mérés, Károli-szó háló, blokk-kizárás (DT564): 33 vers, az első itt; a lista: '
        'naplok/x.tsv | scope=manual | forras=y | ts=2026-11-02')


def sor(forras, indoklas, ige='1Móz 1:2'):
    d = dict.fromkeys(FEJ, '')
    d.update(id='ALVIL-001', igehely=ige, forras_kereses=forras, dontes='elutasítva', indoklas=indoklas,
             datum='2026.11.04', jelolt_tipus='elofordulas')
    return d


class Szabaly33(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix='teszt33_')

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def ir(self, sorok):
        with open(os.path.join(self.dir, 'jeloltek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# próba\n' + '\t'.join(FEJ) + '\n')
            for s in sorok:
                f.write('\t'.join(s[k] for k in FEJ) + '\n')

    def test_rendben(self):
        self.ir([sor(CSOP, 'Összesítő sor 33 versre (az első itt áll): a szó nem áll'),
                 sor('scan H7585 | scope=x', 'a szó más jelentésben', 'Zsolt 1:1')])
        self.assertEqual(E.szabaly33_osszesito_versszam(self.dir).verdict, 'RENDBEN')

    def test_versszam_nelkul_sertes(self):
        self.ir([sor('F123 U1 teljesség-mérés, blokk-kizárás | scope=manual', 'Összesítő sor 33 versre: …')])
        s = E.szabaly33_osszesito_versszam(self.dir)
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('nem hordoz versszámot', s.peldak[0])

    def test_indoklas_osszesito_forras_nelkul_sertes(self):
        self.ir([sor('scan H7585 | scope=x', 'Összesítő sor 12 versre: …')])
        self.assertEqual(E.szabaly33_osszesito_versszam(self.dir).verdict, 'SÉRTÉS')

    def test_eltero_szam_sertes(self):
        self.ir([sor(CSOP, 'Összesítő sor 34 versre (az első itt áll): …')])
        self.assertEqual(E.szabaly33_osszesito_versszam(self.dir).verdict, 'SÉRTÉS')

    def test_valodi_tabla_rendben(self):
        self.assertEqual(E.szabaly33_osszesito_versszam(os.path.join(GYOKER, 'adat')).verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main()
