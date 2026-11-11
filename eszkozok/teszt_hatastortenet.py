#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_hatastortenet.py -- a 9. Hatástörténet szakasz szabályai (F183, FELADATOK #183).

1. A HAMART-001 lapján: a 9. Hatástörténet a 10. Értelmezés előtt, számozatlan alcímekkel; a 4.11 helyén csak mutató
   (a visszhang-tábla egyszer áll a lapon); a „nincs szabad forrás” mondat nem áll; a régi szerkezetű nézetben
   (`regi_szerkezetre`) a szakasz nincs.
2. A tanúréteg szabályai (`tanuk_lapra`): ellenőrizetlen sor nem renderel; Peshat-szintű helyen nincs tanú;
   hagyományonként helyenként legfeljebb egy.
3. A kinyerő tábla ellenőrzője (`tanu_kinyer.ellenoriz`) jelez, ha egy helyen egy hagyománynak két ellenőrzött sora van.

Futtatás: python eszkozok/teszt_hatastortenet.py
"""
import os
import re
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
sys.path.insert(0, os.path.join(ITT, 'visszhang'))
import lexikon_general as LG  # noqa: E402
import tanu_kinyer as TK  # noqa: E402

LAP = os.path.join(os.path.dirname(ITT), 'lexikon', 'HAMART-001_TUDOMANYOS.md')


def tanu(igehely, hagyomany, tanu_nev, ellenorzes='claude-sonnet-5-5, 2026-11-11: kézi átnézés (ok)'):
    r = {o: '' for o in TK.OSZLOPOK}
    r.update({'motivum': 'X-001', 'igehely': igehely, 'hagyomany': hagyomany, 'tanu': tanu_nev, 'mu': 'mű',
              'kapcsolat': 'Egy mondat.', 'forras': 'hcf', 'lekerdezve': '2026-11-11', 'kinyeres': 'modell',
              'modell': 'claude-opus-5-5', 'ellenorzes': ellenorzes,
              'proveniencia': 'scope=teszt | forras=teszt | ts=2026-11-11'})
    return r


class HamartLap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(LAP, encoding='utf-8') as f:
            cls.lap = f.read()

    def test_szakaszrend(self):
        i = self.lap.find('\n## 9. Hatástörténet: ókori fordítások és értelmezők')
        j = self.lap.find('\n## 10. Értelmezés')
        self.assertTrue(0 < i < j)
        szakasz = self.lap[i:j]
        for alcim in (LG.HATAS_OSZ, LG.HATAS_USZ, LG.HATAS_TANU):
            self.assertIn('\n### %s\n' % alcim, szakasz)
        # számozatlan alcímek: a szakaszban nincs „### 9.N” vagy „#### 9.N”
        self.assertFalse(re.search(r'(?m)^#{3,4} 9\.\d', szakasz))

    def test_411_csak_mutato(self):
        i = self.lap.find('#### 4.11. Visszhang: ókori fordítások')
        j = self.lap.find('#### 4.12.', i)
        blokk = self.lap[i:j]
        self.assertIn('9. Hatástörténet', blokk)
        self.assertNotIn('| Lánc-szó', blokk)
        self.assertEqual(self.lap.count('| Lánc-szó · versek | Targum | Vulgata | LXX | Mit mutat |'), 1)

    def test_nincs_hamis_glossza_mondat(self):
        self.assertNotIn('nincs szabad forrás', self.lap)
        self.assertIn('Glossa Ordinaria', self.lap)

    def test_regi_szerkezetben_nincs(self):
        self.assertNotIn('## 9. Hatástörténet', LG.regi_szerkezetre(self.lap))


class TanuSzabaly(unittest.TestCase):
    def setUp(self):
        self.eredeti = LG.visszhang_tanuk
        self.sorai = [{'igehely': '1Móz 5:29', 'pardes_szint': 'Remez'},
                      {'igehely': '1Móz 3:17', 'pardes_szint': 'Peshat/Drash'}]

    def tearDown(self):
        LG.visszhang_tanuk = self.eredeti

    def lapra(self, sorok):
        LG.visszhang_tanuk = lambda _mid: sorok
        return LG.tanuk_lapra({'id': 'X-001'}, self.sorai)

    def test_ellenorizetlen_nem_renderel(self):
        self.assertEqual(self.lapra([tanu('1Móz 5:29', 'szir', 'Efrém', ellenorzes='')]), [])

    def test_peshat_helyen_nincs_tanu(self):
        self.assertEqual(self.lapra([tanu('1Móz 3:17', 'latin', 'Ágoston')]), [])

    def test_hagyomanyonkent_egy(self):
        ki = self.lapra([tanu('1Móz 5:29', 'latin', 'A'), tanu('1Móz 5:29', 'latin', 'B'),
                         tanu('1Móz 5:29', 'rabbinikus', 'C')])
        self.assertEqual([r['tanu'] for r in ki], ['A', 'C'])


class KinyeroEllenor(unittest.TestCase):
    def test_ket_ellenorzott_sor_egy_hagyomanyban_jelez(self):
        eredeti = TK.TABLA
        with tempfile.TemporaryDirectory() as d:
            TK.TABLA = os.path.join(d, 'visszhang_tanuk.tsv')
            try:
                with open(TK.TABLA, 'w', encoding='utf-8') as f:
                    f.write('\t'.join(TK.OSZLOPOK) + '\n')
                    for r in (tanu('1Móz 5:29', 'latin', 'A'), tanu('1Móz 5:29', 'latin', 'B')):
                        f.write('\t'.join(r[o] for o in TK.OSZLOPOK) + '\n')
                self.assertEqual(TK.ellenoriz(None), 1)
            finally:
                TK.TABLA = eredeti

    def test_a_valodi_tabla_rendben(self):
        self.assertEqual(TK.ellenoriz(None), 0)


if __name__ == '__main__':
    unittest.main(verbosity=1)
