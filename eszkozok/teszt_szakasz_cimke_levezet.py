#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_szakasz_cimke_levezet.py -- F148 (c): a `szakasz_cimke_levezet.py` tesztjei.

  - regresszió (kötelező): az ISTENTISZT-001 33 és az ALVIL-001 13 kitöltött sorára a levezetett szakasz
    azonos a `szotar_szakasz_cimke.tsv` kézi leképezésével (valódi adat);
  - a hat jelzéstípus (J1–J6) és a címke-jelzés (J7) egy-egy szintetikus esetre;
  - a binyan a vers morfológiájából (Qal/Niph'al azonos számozással);
  - az `--ir` írása repón kívüli ideiglenes táblán: új sor gépi címkével, üres kulcs pótlása, meglévő címke
    változatlan, ütközésnél megállás.

    python eszkozok/teszt_szakasz_cimke_levezet.py
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

import szakasz_cimke_levezet as SL  # noqa: E402


def sz(strong, sorszam, utvonal):
    return {'strong': strong, 'sorszam': str(sorszam), 'utvonal': utvonal}


def adat(macula=None):
    a = {
        'cimke': {('BDB', 'H7121', 'Qal/2/c'): {'szotar': 'BDB', 'strong': 'H7121', 'szakasz': 'Qal/2/c',
                                                'lexikon_jelentes_szam': '2.c', 'cimke_hu': 'segítségül hívni'},
                  ('BDB', 'H7585', '-/2/b'): {'szotar': 'BDB', 'strong': 'H7585', 'szakasz': '-/2/b',
                                              'lexikon_jelentes_szam': '', 'cimke_hu': 'az igaz kiváltása'}},
        'bdb_sz': {
            'H7121': [sz('H7121', 1, 'fej'), sz('H7121', 2, 'Qal/2/c'), sz('H7121', 3, "Niph'al/2/c"),
                      sz('H7121', 4, 'Qal/3/-')],
            'H7585': [sz('H7585', 1, 'fej'), sz('H7585', 2, '-/1/-'), sz('H7585', 3, '-/2/-'),
                      sz('H7585', 4, '-/2/a'), sz('H7585', 5, '-/2/b')],
            'H0922': [sz('H0922', 1, 'cim'), sz('H0922', 2, 'fej')],
        },
        'bdb_hu': {('H7121', '4'): {'szoveg_hu': '3 kihirdetni, kikiáltani Ézs 40:2'},
                   ('H7585', '2'): {'szoveg_hu': '1 az alvilág, ׳שׁ תַּחְתִּית 5Móz 32:22'},
                   ('H7585', '4'): {'szoveg_hu': 'a. a motívum gonoszai'}},
        'bdb_vj': {('H7585', 'Jób 17:12'): [{'utvonal': '-/2/b'}],
                   ('H7585', 'Zsolt 9:18'): [{'utvonal': '-/2/a'}, {'utvonal': '-/2/b'}],
                   ('H7585', 'Ézs 14:11'): [{'utvonal': '-/2/a'}]},
        'th_sz': {}, 'th_vj': {}, 'tiltott': [],
        'macula': macula or (lambda strong: {'1Móz 4:26': {'q'}, 'Ézs 43:7': {'N'}, 'Jer 1:1': {'q', 'N'}}),
    }
    return a


def sor(igehely, jsz, entry='H7121', szotar='BDB', strong=None):
    return {'id': 'X-001', 'igehely': igehely, 'lexikon_szotar': szotar, 'lexikon_entry_id': entry,
            'jelentes_szam': jsz, 'strong': strong or entry}


def jelek(js):
    return {j for j, _ in js if j != 'I'}


class Levezetes(unittest.TestCase):
    def test_binyan_a_morfologiabol(self):
        ut, js = SL.levezet_sor(adat(), sor('1Móz 4:26', '2.c'), set())
        self.assertEqual(ut, 'Qal/2/c')
        self.assertEqual(jelek(js), set())
        ut, _ = SL.levezet_sor(adat(), sor('Ézs 43:7', '2.c'), set())
        self.assertEqual(ut, "Niph'al/2/c")

    def test_szam_binyan_nelkul(self):
        self.assertEqual(SL.levezet_sor(adat(), sor('Ézs 14:11', '2.a', 'H7585'), set())[0], '-/2/a')
        self.assertEqual(SL.levezet_sor(adat(), sor('Péld 1:12', '1', 'H7585'), set())[0], '-/1/-')

    def test_j1_pelda_mas_pontra(self):
        ut, js = SL.levezet_sor(adat(), sor('Jób 17:12', '1', 'H7585'), set())
        self.assertEqual(ut, '-/1/-')  # nem választ: a levezetett marad, a jelzés kimondja
        self.assertIn('J1', jelek(js))

    def test_j2_alternativa_ket_binyan_ket_pelda(self):
        self.assertIn('J2', jelek(SL.levezet_sor(adat(), sor('1Móz 6:12', "Nif'ál / Hif'íl"), set())[1]))
        self.assertIn('J2', jelek(SL.levezet_sor(adat(), sor('1Móz 1:1', '1, 2', 'H7585'), set())[1]))
        ut, js = SL.levezet_sor(adat(), sor('Jer 1:1', '2.c'), set())  # a versben Qal és Niph'al is
        self.assertIsNone(ut)
        self.assertIn('J2', jelek(js))
        self.assertIn('J2', jelek(SL.levezet_sor(adat(), sor('Zsolt 9:18', '2', 'H7585'), set())[1]))

    def test_j3_ures(self):
        self.assertEqual(jelek(SL.levezet_sor(adat(), sor('Zsolt 16:10', '', ''), set())[1]), {'J3'})

    def test_j4_nincs_utvonal(self):
        self.assertIn('J4', jelek(SL.levezet_sor(adat(), sor('Ézs 14:11', '7', 'H7585'), set())[1]))
        self.assertIn('J4', jelek(SL.levezet_sor(adat(), sor('Zsolt 14:1', "Hif'íl"), set())[1]))
        self.assertIn('J4', jelek(SL.levezet_sor(adat(), sor('Róm 10:13', '9', 'G1941', 'TBESG'), set())[1]))

    def test_tbesg_kulcs(self):
        self.assertEqual(SL.levezet_sor(adat(), sor('Róm 10:13', '2', 'G1941', 'TBESG'),
                                        {('TBESG', 'G1941', '2')})[0], '2')

    def test_j5_tagolatlan(self):
        self.assertEqual(jelek(SL.levezet_sor(adat(), sor('1Móz 1:2', 'tagolatlan', 'H0922'), set())[1]), {'J5'})
        self.assertEqual(jelek(SL.levezet_sor(adat(), sor('1Móz 1:2', '1', 'H0922'), set())[1]), {'J5'})

    def test_j6_minosito(self):
        ut, js = SL.levezet_sor(adat(), sor('1Móz 4:26', '2.c (tagadva)'), set())
        self.assertEqual(ut, 'Qal/2/c')
        self.assertIn('J6', jelek(js))


class Cimke(unittest.TestCase):
    def test_elso_glossza(self):
        self.assertEqual(SL.elso_glossza('1 az alvilág, ׳שׁ תַּחְתִּית 5Móz 32:22'), 'az alvilág')
        self.assertEqual(SL.elso_glossza('3 kihirdetni, kikiáltani Ézs 40:2'), 'kihirdetni')
        self.assertEqual(SL.elso_glossza('2. köznévként: Orcus, az alvilág'), 'Orcus')

    def test_j7(self):
        a = adat()
        self.assertEqual(SL.cimke_javaslat(a, 'BDB', 'H7585', '-/1/-', [])[0], 'az alvilág')
        self.assertIn('J7', jelek(SL.cimke_javaslat(a, 'BDB', 'H7585', '-/2/-', [])[1]))  # nincs magyar szöveg
        self.assertIn('J7', jelek(SL.cimke_javaslat(a, 'BDB', 'H7585', '-/2/a', [])[1]))  # tiltott: motívum
        self.assertIn('J7', jelek(SL.cimke_javaslat(a, 'BDB', 'H7121', 'Qal/3/-',
                                                    [{'minta': 'kihirdet', 'magyar_alak': 'x'}])[1]))


class Teendo(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix='F148_lev_')
        self.ut = os.path.join(self.d, 'szotar_szakasz_cimke.tsv')
        self.eredeti = ('\t'.join(SL.CIMKE_FEJ) + '\n'
                        'BDB\tH7121\tQal/2/c\t2.c\tsegítségül hívni\tscope=manual | forras=x | ts=2026-10-26\t\n'
                        'BDB\tH7585\t-/2/b\t\taz igaz kiváltása\tscope=manual | forras=y | ts=2026-10-28\t\n')
        with open(self.ut, 'w', encoding='utf-8', newline='') as f:
            f.write(self.eredeti)

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_ellenoriz_teendok(self):
        elo = [dict(sor('1Móz 4:26', '2.c'), id='X-001'), dict(sor('Péld 1:12', '1', 'H7585'), id='X-001'),
               dict(sor('Ézs 38:18', '2.b', 'H7585'), id='X-001'), dict(sor('Jób 17:12', '1', 'H7585'), id='X-001')]
        ki = {r['igehely']: r for r in SL.ellenoriz('X-001', adat(), elo, set(), ts='2026-11-01')}
        self.assertEqual(ki['1Móz 4:26']['egyezik'], 'igen')
        self.assertEqual(ki['1Móz 4:26']['teendo'], '')
        self.assertEqual((ki['Péld 1:12']['teendo'], ki['Péld 1:12']['cimke_hu_javaslat']), ('uj_sor', 'az alvilág'))
        self.assertEqual(ki['Ézs 38:18']['teendo'], 'kulcs_potlas')
        self.assertEqual(ki['Jób 17:12']['teendo'], '')  # jelzéses sor nem írandó
        self.assertIn('forras=szakasz_cimke_levezet.py', ki['1Móz 4:26']['proveniencia'])
        self.assertIn('Macula', ki['1Móz 4:26']['proveniencia'])
        irando = SL.irasok(ki.values())
        self.assertEqual(set(irando), {('BDB', 'H7585', '-/1/-'), ('BDB', 'H7585', '-/2/b')})

    def test_ir_tabla(self):
        irando = {('BDB', 'H7585', '-/1/-'): ('uj_sor', '1', 'az alvilág'),
                  ('BDB', 'H7585', '-/2/b'): ('kulcs_potlas', '2.b', 'az igaz kiváltása')}
        p, u = SL.ir_tabla(self.ut, irando, '2026-11-01')
        self.assertEqual((p, u), (1, 1))
        with open(self.ut, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        self.assertEqual(sorok[1], self.eredeti.split('\n')[1])  # meglévő kézi sor bájtra változatlan
        potolt = sorok[2].split('\t')
        self.assertEqual((potolt[3], potolt[4]), ('2.b', 'az igaz kiváltása'))  # a címke nem íródik felül
        self.assertIn('szakasz_cimke_levezet.py', potolt[6])
        uj = sorok[3].split('\t')
        self.assertEqual(uj[:5], ['BDB', 'H7585', '-/1/-', '1', 'az alvilág'])
        self.assertIn('forras=szakasz_cimke_levezet.py (gépi, DT-F148c)', uj[5])

    def test_ir_tabla_megall(self):
        with self.assertRaises(SystemExit):
            SL.ir_tabla(self.ut, {('BDB', 'H7121', 'Qal/2/c'): ('uj_sor', '2.c', 'x')}, '2026-11-01')
        with self.assertRaises(SystemExit):
            SL.ir_tabla(self.ut, {('BDB', 'H7121', 'Qal/2/c'): ('kulcs_potlas', '3', 'x')}, '2026-11-01')
        with open(self.ut, encoding='utf-8', newline='') as f:
            self.assertEqual(f.read(), self.eredeti)

    def test_ket_kulcs_egy_szakaszra(self):
        ki = [{'teendo': 'uj_sor', 'szotar': 'BDB', 'strong': 'H1', 'levezetett_szakasz': '-/1/-',
               'jelentes_szam': '1', 'cimke_hu_javaslat': 'a'},
              {'teendo': 'uj_sor', 'szotar': 'BDB', 'strong': 'H1', 'levezetett_szakasz': '-/1/-',
               'jelentes_szam': '1', 'cimke_hu_javaslat': 'b'}]
        with self.assertRaises(ValueError):
            SL.irasok(ki)


class Regresszio(unittest.TestCase):
    """Kötelező: a valódi adaton a levezetett szakasz azonos a kézi leképezéssel (ISTENTISZT-001 33, ALVIL-001 13)."""

    def _ellenoriz(self, mid):
        return [r for r in SL.ellenoriz(mid) if r['jelentes_szam']]

    def test_istentiszt_33(self):
        ki = self._ellenoriz('ISTENTISZT-001')
        self.assertEqual(len(ki), 33)
        self.assertEqual([r['igehely'] for r in ki if r['egyezik'] != 'igen'], [])

    def test_alvil_13(self):
        ki = self._ellenoriz('ALVIL-001')
        self.assertEqual(len(ki), 13)
        self.assertEqual([r['igehely'] for r in ki if r['egyezik'] != 'igen'], [])
        # a két ismert kutatói kérdés jelzett, de a kézi döntés szakaszát adja vissza
        jelzett = {r['igehely'] for r in ki if 'J1' in r['jelzes']}
        self.assertEqual(jelzett, {'Jób 17:12', 'Zsolt 88:4'})
        self.assertEqual(SL.irasok(ki), {})


if __name__ == '__main__':
    unittest.main()
