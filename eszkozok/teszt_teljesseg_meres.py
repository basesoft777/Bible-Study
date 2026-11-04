#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_teljesseg_meres.py -- DT548: az `eszkozok/teljesseg_meres.py` tiszta
függvényeinek tesztjei (tartomány-bontás, állapot, Károli-egyezés, szótári háló).
Ideiglenes (repón kívüli) fájlokkal fut.

    python eszkozok/teszt_teljesseg_meres.py
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

import teljesseg_meres as T  # noqa: E402


class Tartomany(unittest.TestCase):
    def test_tartomany_bontas(self):
        self.assertEqual(T.versekre('Jel 20:13-14'), ['Jel 20:13', 'Jel 20:14'])

    def test_egyes_vers(self):
        self.assertEqual(T.versekre('Hós 13:14'), ['Hós 13:14'])


class Allapot(unittest.TestCase):
    def test_harom_allapot(self):
        e, j = {'Zsolt 16:10'}, {'Mt 16:18': 'elutasítva'}
        self.assertEqual(T.allapot('Zsolt 16:10', e, j), 'E')
        self.assertEqual(T.allapot('Mt 16:18', e, j), 'J:elutasítva')
        self.assertEqual(T.allapot('Jób 3:17', e, j), 'ELTÉRÉS')


class KaroliEgyezes(unittest.TestCase):
    TABLA = {'sírba': 'sír', 'sírt': 'sír', 'koporsóba': 'koporsóba', 'sírás': 'sírás'}

    def egyezik(self, szo, lemmak=('sír', 'koporsó')):
        return T.karoli_egyezik(szo, set(lemmak), {x.lower() for x in lemmak}, self.TABLA)

    def test_szotari_alak(self):
        self.assertTrue(self.egyezik('sírba'))

    def test_tovezetlen_alak_elotaggal(self):
        # a szótövező a „koporsóba” alakot nem töveli: az előtag-egyezés fogja meg
        self.assertTrue(self.egyezik('koporsóba'))
        self.assertTrue(self.egyezik('Seolban', ('Seol',)))

    def test_tovezett_mas_szo_nem_egyezik(self):
        # a „sírás” szótári alakja önmaga, de nem a lemma: az előtag-szabály csak tövezetlen alakra áll
        self.assertTrue(self.egyezik('sírás'))  # tövezetlennek számít (szótári alak = szóalak)
        self.assertFalse(T.karoli_egyezik('sírt', {'koporsó'}, {'koporsó'}, self.TABLA))


class Halok(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_szotar_halo(self):
        bdb = [{'strong': 'H7585', 'karoli_vers': 'Jób 3:17', 'sorszam': '60', 'utvonal': '-/1'},
               {'strong': 'H0001', 'karoli_vers': 'Jób 3:18', 'sorszam': '1', 'utvonal': ''},
               {'strong': 'H7585', 'karoli_vers': '', 'sorszam': '2', 'utvonal': ''}]
        thayer = [{'strong': 'G0086', 'karoli_vers': 'ApCsel 2:24', 'sorszam': '14', 'utvonal': '-/2/-'}]
        t = T.halo_szotar({'H7585', 'G0086'}, bdb, thayer)
        self.assertEqual(sorted(t), ['ApCsel 2:24', 'Jób 3:17'])

    def test_motivum_adat_split_tab(self):
        elof = os.path.join(self.d, 'e.tsv')
        jel = os.path.join(self.d, 'j.tsv')
        with open(elof, 'w', encoding='utf-8') as f:
            f.write('# megjegyzés\nid\tigehely\tstrong\tkaroli_szo\n'
                    'X-001\tJel 20:13-14\tG0086\ta pokol\n'
                    'X-001\tHós 13:14\tH7585\t"a Seol" hatalmából\n'
                    'Y-001\tHós 13:14\tH1\t\n')
        with open(jel, 'w', encoding='utf-8') as f:
            f.write('id\tigehely\tdontes\tjelolt_tipus\n'
                    'X-001\tMt 16:18\telutasítva\telofordulas\n'
                    'X-001\tZsolt 116:3\tnyitva\tmotivumkozi\n')
        s, e, j, k = T.motivum_adat('X-001', elof, jel)
        self.assertEqual(s, {'G0086', 'H7585'})
        self.assertEqual(e, {'Jel 20:13', 'Jel 20:14', 'Hós 13:14'})
        self.assertEqual(j, {'Mt 16:18': 'elutasítva'})
        self.assertIn('"a Seol" hatalmából', k)  # az idézőjel nem vész el (nem csv-olvasás)


class Szoparmod(unittest.TestCase):
    """--kollokacio (F123.ANTROP2.2): a pár minden tagja (vagy rokon alakja) egy versben."""

    def test_rokon_terkep(self):
        self.assertEqual(T.rokon_terkep('G4151=G4152, G5590=G5591'),
                         {'G4151': {'G4151', 'G4152'}, 'G5590': {'G5590', 'G5591'}})

    def test_halo_par(self):
        vs = {'1Thessz 5:23': {'G4151', 'G5590'},   # főnévpár
              'Júd 1:19': {'G4151', 'G5591'},       # rokon alakkal
              'Luk 1:46': {'G5590'},                # csak az egyik tag
              '1Móz 2:7': {'H5315', 'H2416'}}       # a héber pár
        rokon = T.rokon_terkep('G4151=G4152,G5590=G5591')
        t = T.halo_par([('G4151', 'G5590'), ('H5315', 'H2416')], rokon, vs)
        self.assertEqual(sorted(t), ['1Móz 2:7', '1Thessz 5:23', 'Júd 1:19'])
        self.assertEqual(t['Júd 1:19'], ['G4151', 'G5591'])
        self.assertEqual(set(T.halo_par([('G4151', 'G5590')], {}, vs)), {'1Thessz 5:23'})

    def test_parok_gerinc_elembol(self):
        d = tempfile.mkdtemp()
        try:
            elof = os.path.join(d, 'e.tsv')
            with open(elof, 'w', encoding='utf-8') as f:
                f.write('id\tigehely\tgerinc_elem\tstrong\n'
                        'X-001\tLuk 1:46\tG4151+G5590\tG5590\n'
                        'X-001\t1Móz 2:7\tH5315+H2416\tH5315+H2416\n'
                        'X-001\tZsid 4:12\tG4151+G5590\tG4151+G5590\n'
                        'Y-001\tMt 1:1\tG1+G2\tG1\n')
            self.assertEqual(T.parok('X-001', elof), [('G4151', 'G5590'), ('H5315', 'H2416')])
        finally:
            shutil.rmtree(d)


if __name__ == '__main__':
    unittest.main()
