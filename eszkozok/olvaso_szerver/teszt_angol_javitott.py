"""Az angol BDB- és Thayer-szöveg javított olvasása (F215): javított adat -> minden fogyasztó a javítottat olvassa.

* Thayer: a `szo.thayer` blokk (a `lekerdezesek.thayer`) szövege tartalmazza a `thayer_forras_javitas` mind a 15 beszúrását
  (a nyers `thayer.teljes_szocikk` egyiket sem), és egyezik a magyar ág bemenetével (`thayer_bemenet`).
* BDB: a `hivatkozas` / `javitva` javítások (412 sor, 247 Strong) az angol szövegben (`bdb.teljes_szocikk`, a
  `BDB_teljes_unabridged.tsv`-ből) már benne vannak, a nyers JSON-szakaszokban (`bdb_szakaszok.tsv`) nincsenek: az angol ágnak
  nincs teendője, ez a teszt őrzi.

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_angol_javitott` (a WSL-natív PARDES_DB-vel). Adatbázis nélkül kihagyódik.
"""
import collections
import os
import re
import sqlite3
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
sys.path.insert(0, os.path.join(os.path.dirname(D), 'thayer_jelolt'))
sys.path.insert(0, os.path.join(os.path.dirname(D), 'bdb_jelolt'))

import lekerdezesek as q
from teszt_olvaso_szerver import DB, VAN_DB

_NOWS = re.compile(r'\s+')
_KONYV = re.compile(r'(?<![A-Za-z])[1-3]?(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|[12]?Sam|[12]?Kgs|[12]?Chr|Ezra|Neh|Esth|Job|'
                    r'Psa|Prov|Eccl|Cant|Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jon|Mic|Nah|Hab|Zeph|Hag|Zech|Mal)(?![a-z])')


def _nows(s):
    return _NOWS.sub('', s)


class TestThayerJavitas(unittest.TestCase):
    def test_beszuras_egyszer_es_a_helyen(self):
        self.assertEqual(q.thayer_javitas('ab cd ef', [('cd', ' XY')]), 'ab cd XY ef')
        self.assertEqual(q.thayer_javitas('ab cd ef', []), 'ab cd ef')

    def test_nem_egyertelmu_elotte_hiba(self):
        with self.assertRaises(ValueError):
            q.thayer_javitas('ab ab', [('ab', 'X')])
        with self.assertRaises(ValueError):
            q.thayer_javitas('ab', [('zz', 'X')])


@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class TestAngolAdatbazis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect('file:%s?mode=ro' % DB.replace(os.sep, '/'), uri=True)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_thayer_mind_a_15_beszuras(self):
        sorok = self.con.execute("SELECT strong, javitott_alak FROM thayer_forras_javitas WHERE allapot='javitva'").fetchall()
        self.assertEqual(len(sorok), 15)
        for strong, alak in sorok:
            nyers = self.con.execute('SELECT teljes_szocikk FROM thayer WHERE strong=?', (strong,)).fetchone()[0]
            self.assertNotIn(alak, nyers, '%s: a nyers szöveg már tartalmazza a beszúrást' % strong)
            self.assertIn(alak, q.thayer(self.con, strong), '%s: a beszúrás nem látszik' % strong)

    def test_thayer_egyezik_a_magyar_ag_bemenetevel(self):
        """A javított sorok szövege (a `thayer_bemenet.szakaszok`, amelyből a magyar fordítás készül) a javított angol szócikkben áll."""
        import thayer_bemenet
        n = 0
        for (strong, sorszam) in thayer_bemenet.javitas_olvas():
            sor = next(x for x in thayer_bemenet.szakaszok(strong) if x['sorszam'] == int(sorszam))
            szoveg = sor['szoveg'][len(sor['jel']):] if sor['jel'] and sor['szoveg'].startswith(sor['jel']) else sor['szoveg']
            self.assertIn(_nows(szoveg), _nows(q.thayer(self.con, strong)), '%s#%s' % (strong, sorszam))
            n += 1
        self.assertEqual(n, 15)

    def test_nem_javitott_thayer_valtozatlan(self):
        javitott = {r[0] for r in self.con.execute("SELECT strong FROM thayer_forras_javitas WHERE allapot='javitva'")}
        for (strong, nyers) in self.con.execute('SELECT strong, teljes_szocikk FROM thayer LIMIT 400').fetchall():
            if strong not in javitott:
                self.assertEqual(q.thayer(self.con, strong), nyers)

    def test_bdb_h0026_hivatkozas(self):
        """H0026: a nyers JSON `Kt 2Sam 25:18`-at ír, a javítótábla `1Sam`-ot; az angol szöveg a javított alakot hordozza."""
        t = q.bdb_angol(self.con, 'H0026')
        self.assertIn('Kt 1Sam 25:18', t)
        self.assertNotIn('Kt 2Sam 25:18', t)

    def test_bdb_hivatkozas_javitasok_az_angol_szovegben(self):
        """Mind a 247 Strongon: az angol szöveg könyvrövidítés-sora a javított nézetével egyezik (a szakasz-összefűzés szóköz-
        zaját leszámítva), a nyers JSON-szakaszokétól viszont eltér."""
        import szakasz_bemenet
        tab, jav = szakasz_bemenet._betolt()
        eltero_javitott = eltero_nyers = 0
        for strong in jav:
            en = collections.Counter(_KONYV.findall(q.bdb_angol(self.con, strong)))
            javitott = collections.Counter(_KONYV.findall(' '.join(x['szoveg'] for x in szakasz_bemenet.szakaszok(strong))))
            nyers = collections.Counter(_KONYV.findall(' '.join(x['szoveg'] for x in tab[strong])))
            eltero_javitott += en != javitott
            eltero_nyers += en != nyers
        self.assertEqual(len(jav), 247)
        self.assertLessEqual(eltero_javitott, 2, 'a javított nézettől eltérő Strong (tokenhatár-zaj legfeljebb 1-2)')
        self.assertGreater(eltero_nyers, 200, 'a nyers nézettől a javítandó Strongok többségében el kell térnie')


if __name__ == '__main__':
    unittest.main()
