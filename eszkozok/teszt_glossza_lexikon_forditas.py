#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_glossza_lexikon_forditas.py -- F121: a mankók (szójegyzék-egyenérték, Károli-alakok, BDB-egyezés) és a
UBS_DBH forrásszöveg-feloldó tesztje. Hermetikus: ideiglenes könyvtár.

    python eszkozok/teszt_glossza_lexikon_forditas.py
"""
import os
import shutil
import sys
import tempfile
import unittest
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossza_lexikon_forditas as G  # noqa: E402


def sor(mezo='glosszak_hu', hu='nevezni; nevet adni', strong='H7121'):
    return {'szotar': 'UBS_DBH', 'strong': strong, 'entry_id': '006562001008000', 'jelentes_szam': G.EM_DASH, 'mezo': mezo,
            'forditas_hu': hu, 'megjegyzes': ''}


class Segedek(unittest.TestCase):
    def test_elemek_zarojel_nelkul(self):
        self.assertEqual(G.elemek('to acknowledge (a deity); to name'), ['to acknowledge', 'to name'])
        self.assertEqual(G.elemek(' ; '), [])

    def test_tovek_toldalekolas_ellen(self):
        self.assertIn('kiál', G.tovek('kiáltani'))
        self.assertIn('neve', G.tovek('nevezni; nevet adni'))
        self.assertNotIn('valaki', {t for t in G.tovek('valakinek lenni')})   # kötőszó/általános szó kimarad

    def test_ellenorzendo_szavak(self):
        self.assertEqual(G.ellenorzendo_szavak('glosszak_hu', 'találkozni'), 'találkozni')
        self.assertEqual(G.ellenorzendo_szavak('definicio_hu', 'szó szerint: kiáltani; innen: = olyan cselekvés'), 'kiáltani')
        self.assertEqual(G.ellenorzendo_szavak('definicio_hu', '= olyan cselekvés, amellyel emberek'), '')   # leíró definíció


class Szojegyzek(unittest.TestCase):
    TABLA = {'to name': Counter({'nevezni': 3}), 'authority': Counter({'hatalom': 1})}

    def test_egyezik(self):
        a, _ = G.szojegyzek_ellenorzes(sor(hu='nevezni; nevet adni'), 'to name; to call', self.TABLA)
        self.assertEqual(a, 'egyezik')

    def test_utkozik_versengo_alak(self):
        a, r = G.szojegyzek_ellenorzes(sor(hu='név; felhatalmazás'), 'name; authority', self.TABLA)
        self.assertEqual(a, 'utkozik')
        self.assertIn('hatalom', r)

    def test_nincs_adat_es_definicio(self):
        self.assertEqual(G.szojegyzek_ellenorzes(sor(hu='keresni'), 'to look for', self.TABLA)[0], 'nincs_adat')
        self.assertEqual(G.szojegyzek_ellenorzes(sor(mezo='definicio_hu'), 'x', self.TABLA)[0], 'nem_glossza')


class Karoli(unittest.TestCase):
    def setUp(self):
        self.mappa = tempfile.mkdtemp()
        with open(os.path.join(self.mappa, 'parok_1Moz.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('vers\thu_sorszam\thu_szo\ter_sorszam\ter_szo\tstrong\tbizonyossag\tforras\n')
            for st, szo in (('H7121', 'Nevezé'), ('H7121', 'nevezé'), ('H7121', 'kiálta'), ('H8034', 'neve'), ('G1941', 'segítségül')):
                f.write('\t'.join(['1Móz 1:1', '1', szo, '1', 'x', st, 'magas', 'teszt']) + '\n')
            f.write('\t'.join(['1Móz 1:2', '1', 'nullás', '1', 'x', 'H0430', 'magas', 'teszt']) + '\n')   # a nullával kitöltött alak is egyezik

    def tearDown(self):
        shutil.rmtree(self.mappa)

    def test_alakok_strongra_nullakkal_is(self):
        c = G.karoli_alakok_strongra('H7121', self.mappa)
        self.assertEqual(c['nevezé'], 2)
        self.assertEqual(G.karoli_alakok_strongra('H430', self.mappa)['nullás'], 1)       # H430 ~ H0430
        self.assertEqual(G.karoli_alakok_strongra('G1941', self.mappa)['segítségül'], 1)

    def test_egyezik_es_nem_talal(self):
        k = G.karoli_alakok_strongra('H7121', self.mappa)
        self.assertEqual(G.karoli_ellenorzes(sor(hu='nevezni; nevet adni'), k)[0], 'egyezik')
        self.assertEqual(G.karoli_ellenorzes(sor(hu='találkozni'), k)[0], 'nem_talal')
        self.assertEqual(G.karoli_ellenorzes(sor(mezo='definicio_hu', hu='= olyan cselekvés'), k)[0], 'nincs_ellenorzendo')


class Bdb(unittest.TestCase):
    def test_egyezes_es_nem_heber(self):
        self.assertEqual(G.bdb_ellenorzes(sor(hu='kiáltani'), 'hívni, kiáltani, olvasni')[0], 'egyezik')
        self.assertEqual(G.bdb_ellenorzes(sor(hu='keresni'), 'hívni, kiáltani')[0], 'nem_talal')
        self.assertEqual(G.bdb_ellenorzes(sor(strong='G1941'), 'x')[0], 'nem_heber')


class DbhForras(unittest.TestCase):
    def test_feloldo_az_elso_sort_adja(self):
        mappa = tempfile.mkdtemp()
        try:
            with open(os.path.join(mappa, 'UBS_DBH_jelentesek.tsv'), 'w', encoding='utf-8', newline='') as f:
                f.write('# GENERALT\nstrong\tlexid\tdefinicio_rovid\tglosszak\n')
                f.write('H8034\t1\tELSO\tname\nH8034\t1\tMASODIK\tname2\n')
            idx = G.dbh_forras_idx(mappa)
            self.assertEqual(idx[('H8034', '1', 'definicio_hu')], 'ELSO')
            self.assertEqual(idx[('H8034', '1', 'glosszak_hu')], 'name')
            self.assertEqual(G.forras_szoveg_dbh({'szotar': 'UBS_DBH', 'jelentes_szam': G.EM_DASH, 'strong': 'H8034',
                                                  'entry_id': '1', 'mezo': 'definicio_hu'}, idx), 'ELSO')
            self.assertIsNone(G.forras_szoveg_dbh({'szotar': 'BDB', 'jelentes_szam': G.EM_DASH, 'strong': 'H8034',
                                                   'entry_id': '1', 'mezo': 'definicio_hu'}, idx))
        finally:
            shutil.rmtree(mappa)


if __name__ == '__main__':
    unittest.main(verbosity=2)
