#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_ubs_dbh.py -- F121 (DT393): a szónézet UBS DBH-blokkja (`szo.ubs_dbh`) és a magyar UBS DNTG
szétválasztása (`szo.magyar_gorog`: glossza / definíció). Hermetikus: memóriabeli SQLite, nem a pardes.db.

    python eszkozok/teszt_futtat.py --fajl teszt_ubs_dbh
"""
import os
import sqlite3
import sys
import unittest
from types import SimpleNamespace

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blokkok  # noqa: E402
import lekerdezesek as q  # noqa: E402

EM = '\u2014'


def adatbazis():
    con = sqlite3.connect(':memory:')
    con.execute('CREATE TABLE ubs_dbh_jelentesek (strong TEXT, lexid TEXT, domen TEXT, definicio_rovid TEXT, glosszak TEXT)')
    con.execute('CREATE TABLE forditasok (szotar TEXT, strong TEXT, entry_id TEXT, jelentes_szam TEXT, mezo TEXT, forditas_hu TEXT)')
    con.executemany('INSERT INTO ubs_dbh_jelentesek VALUES (?,?,?,?,?)', [
        ('H8034', '007442001001000', 'Name', '= one or more words', 'name'),
        ('H8034', '007442001001000', 'Reputation', '= one or more words', 'name'),   # domén-duplikátum: lexidenként egy sor
        ('H8034', '007442001002000', 'Authority', 'literally: name; hence: = state', 'name; authority'),
        ('H7121', '006562001001000', 'Shout', '= action', 'to cry out'),
    ])
    con.executemany('INSERT INTO forditasok VALUES (?,?,?,?,?,?)', [
        ('UBS_DBH', 'H8034', '007442001001000', EM, 'glosszak_hu', 'név'),
        ('UBS_DBH', 'H8034', '007442001001000', EM, 'definicio_hu', '= egy vagy több szó'),
        ('UBS_DBH', 'H8034', '007442001002000', EM, 'glosszak_hu', 'név; felhatalmazás'),
        ('UBS_DBH', 'H8034', '007442001002000', EM, 'definicio_hu', ''),              # üres magyar: nem számít fordításnak
        ('UBS_DNTG', 'G1941', '001957003000', '56.15', 'glosszak_hu', 'ügyében fellebbezni'),
        ('UBS_DNTG', 'G1941', '001957003000', '56.15', 'definicio_hu', 'a törvényes jog érvényesítése'),
    ])
    return con


class UbsDbhSzo(unittest.TestCase):
    def setUp(self):
        self.con = adatbazis()

    def test_lexidenkent_egy_sor_magyarral(self):
        d = q.ubs_dbh_szo(self.con, 'H8034')
        self.assertEqual([x[0] for x in d], ['007442001001000', '007442001002000'])
        self.assertEqual(d[0][4:], ('= egy vagy több szó', 'név'))

    def test_hianyzo_magyar_ures(self):
        d = q.ubs_dbh_szo(self.con, 'H8034')
        self.assertEqual(d[1][4], '')                                    # üres definicio_hu
        self.assertEqual(d[1][5], 'név; felhatalmazás')
        self.assertEqual(q.ubs_dbh_szo(self.con, 'H7121')[0][4:], ('', ''))   # nincs magyar sor

    def test_blokk_csak_heber(self):
        k = SimpleNamespace(con=self.con, strong='G1941')
        self.assertIsNone(blokkok._f_ubs_dbh(k))
        self.assertIsNone(blokkok._f_ubs_dbh(SimpleNamespace(con=self.con, strong='H9999')))

    def test_render_magyar_es_jeloles(self):
        k = SimpleNamespace(con=self.con, strong='H8034')
        html = str(blokkok._r_ubs_dbh(blokkok._f_ubs_dbh(k), k))
        self.assertIn('név; felhatalmazás', html)
        self.assertIn('= one or more words', html)                      # az angol mellette
        self.assertIn('(fordításra vár)', html)                         # a hiányzó magyar definíció kimondva

    def test_regiszterben(self):
        b = blokkok.BLOKK_ID['szo.ubs_dbh']
        self.assertEqual(b.oldal, 'szo_h')
        self.assertEqual(b.jelleg, ('forras', 'modell'))


class MagyarGorogSzetvalasztas(unittest.TestCase):
    def test_mezo_kulonbozteti_meg(self):
        con = adatbazis()
        d = q.magyar_gorog(con, 'G1941')
        self.assertEqual({x[3] for x in d}, {'glosszak_hu', 'definicio_hu'})
        html = str(blokkok._r_magyar_gorog(d, SimpleNamespace(con=con, strong='G1941')))
        self.assertIn('56.15. jelentés · glossza', html)
        self.assertIn('56.15. jelentés · definíció', html)


if __name__ == '__main__':
    unittest.main(verbosity=2)
