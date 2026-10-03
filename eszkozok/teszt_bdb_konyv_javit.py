#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teszt_bdb_konyv_javit.py — F46 (BDB_KONYVFELOLDAS): a tokenizalas, a lanc/csoport,
a szamjegy-valtozatok es a forditasbeli illesztes egysegtesztjei.

Futtatas a repo gyokerebol: python eszkozok/teszt_bdb_konyv_javit.py
(a tesztek a konkordancia-tablakat nem toltik be; a Bizonyitek osztalyt nem peldanyositjak)
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_konyv_javit as J  # noqa: E402


class Tokenek(unittest.TestCase):
    def test_csoport_a_konvertalo_bontott_lancan(self):
        # H0413: a nyomtatott `Jb 3:22; 5:26; 15:22; 29:19` lanc tagjai kulon tokenek
        sz = 'only in Job ( 1 Samuel 3:22; 1 Samuel 5:26; 1Sam 15:22; 1 Samuel 29:19), with'
        ts = J.tokenek('H0413', sz)
        self.assertEqual([t.alak for t in ts], ['1 Samuel 3:22', '1 Samuel 5:26', '1Sam 15:22', '1 Samuel 29:19'])
        self.assertEqual(sorted(ts[0].csoport), [(5, 26), (15, 22), (29, 19)])

    def test_lanc_a_kovetkezo_tokenig(self):
        ts = J.tokenek('H1320', 'Judg 8:7; 1Kin 4:34; 5:10; 5:14; 6:30; Job 2:5')
        k = [t for t in ts if t.alak == '1Kin 4:34'][0]
        self.assertEqual(k.lanc, [(5, 10), (5, 14), (6, 30)])

    def test_bibliografiai_hivatkozas_nem_igehely(self):
        ts = J.tokenek('H2362', 'Wetzst in De^Job 2:598; ZKW 1884, Che^Comm. Isaiah 2:148, or')
        self.assertEqual(ts, [])

    def test_osszeolvadt_szamjegy(self):
        # `Gen 33:816t.` = 33:8, 16-szor: a vers 3 jegye a tokenben, a 4. jegytol farok
        ts = J.tokenek('H0000', 'Gen 33:816t. and more')
        self.assertEqual((ts[0].c, ts[0].v, ts[0].farok), (33, 816, ''))
        ts = J.tokenek('H0000', 'Gen 33:8160 x')
        self.assertEqual(ts[0].farok, '0')

    def test_jelentesszamhoz_tapadt_konyv(self):
        ts = J.tokenek('H3562', 'note). 22Chr 35:9. —')
        self.assertEqual(ts[0].tipus_jel, 'osszeolvadt_szam')

    def test_nem_lekepezett_alak(self):
        ts = J.tokenek('H4039', 'Ezek 3:1-2, 3; Ze 5:1-2,.')
        z = [t for t in ts if t.forma == 'Ze'][0]
        self.assertEqual(z.tipus_jel, 'nem_lekepezett')
        self.assertEqual(J.hu_regi(z), 'Ze 5:1')


class SzamjegyValtozatok(unittest.TestCase):
    def test_egyjegyu_es_felcserelt(self):
        v = J.egyjegyu_valtozatok(82)
        self.assertIn(28, v)    # felcserelt
        self.assertIn(32, v)    # egy jegy csere
        self.assertIn(8, v)     # jegy kiesese
        self.assertNotIn(82, v)


class ForditasIllesztes(unittest.TestCase):
    def test_azonos_alaku_tokenek_sorrendje(self):
        sz = 'a Hab 41:47; b Hab 41:47; c Gen 1:1'
        ts = J.tokenek('H9005', sz)
        hu = 'a Hab 41:47; b Hab 41:47; c 1Móz 1:1'
        allapot, j = J.ford_illesztes(ts, ts[1], hu)
        self.assertEqual(j, 1)
        self.assertTrue(allapot.startswith('illesztheto'))

    def test_eltero_darabszam_nem_illesztheto(self):
        ts = J.tokenek('H9005', 'a Hab 41:47; b Hab 41:47')
        allapot, j = J.ford_illesztes(ts, ts[0], 'a Hab 41:47')
        self.assertIsNone(j)
        self.assertTrue(allapot.startswith('nem_illesztheto'))

    def test_hosszabb_versszam_nem_talalat(self):
        self.assertEqual(J.hu_minta('Hab 41:4').findall('Hab 41:47'), [])


class Nevhiba(unittest.TestCase):
    def test_pharaoh_kontextus(self):
        sz = 'Gen 41:55 cried to Phoenician לַלָּחֶם for bread'
        self.assertEqual(len(J.nevhibak([('H9005', sz)])), 1)

    def test_nyelvi_hasznalat_nem_jelolt(self):
        for sz in ('(Moabite, Phoenician ל, Aramaic)', 'on the Phoenician coast Ezek 27:9',
                   'connection with Phoenician Zophesemim'):
            self.assertEqual(J.nevhibak([('H0000', sz)]), [], sz)


class Arameus(unittest.TestCase):
    def test_szakaszhatarok(self):
        self.assertTrue(J.arameus('Dán', 2, 4))
        self.assertFalse(J.arameus('Dán', 2, 3))
        self.assertTrue(J.arameus('Ezsd', 6, 18))
        self.assertFalse(J.arameus('Ezsd', 6, 19))


if __name__ == '__main__':
    unittest.main()
