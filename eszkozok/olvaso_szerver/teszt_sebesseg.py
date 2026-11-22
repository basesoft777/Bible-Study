"""F235: az olvasó sebességőre — időkorlát és lekérdezésszám a helyi pardes.db-n (a push előtti kapu `teszt_futtat.py --gyors` részeként fut).

Egy lap előállításának ideje MELEG szerveren, GYORSÍTÓTÁR NÉLKÜL (a lapgyorsítótár ürítve, a folyamat és az adatbázis-fájl gyorsítótára meleg):

    fejezet  ≤ 300 ms      vers  ≤ 400 ms      szó-lap  ≤ 250 ms      kereső  ≤ 50 ms
    laponként ≤ 100 SQL-utasítás      gyorsítótár-találat ≤ 20 ms

A mérés a Flask belső kliensével fut (nincs hálózat), a gyorsítótár ürítése a közvetlen `cache.urit()` (tesztkörnyezet: más kapu nincs, a szerver
nem kínál ürítő végpontot). Minden oldalt egyszer bemelegítünk (a sablonok, a modulok és a lusta betöltések), utána háromszor mérünk, és a legjobb idő
számít: a határ a kód lassulását őrzi, nem a gép pillanatnyi terhelését (a párhuzamos munkamenetek zaja ellen). Az SQL-utasítások számát a
kapcsolat `set_trace_callback`-je adja (a `PRAGMA`-kat is beleértve).

Futtatás (WSL `pardes`, venv): PARDES_DB=<pardes.db> python eszkozok/olvaso_szerver/teszt_sebesseg.py [-v]
A teszt a `PARDES_DB` nélkül (vagy Flask nélkül) kimarad, kifejezetten jelölve (nem zöld). A határokat a `HATAROK` tartja; a megengedett
kivételek (`KIVETEL`) kimondottak és megszámoltak: minden tétel megnevezett célfeladattal.
"""
import os
import statistics
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D)).replace('\\', '/') + '/'
sys.path.insert(0, D)

DB = os.environ.get('PARDES_DB') or (GY + 'pardes.db')

# (oldaltípus, útvonal, időkorlát ms)
OLDALAK = [
    ('fejezet', '/1Moz/1', 300),
    ('fejezet', '/Mt/5', 300),
    ('fejezet', '/Zsolt/23', 300),
    ('fejezet', '/Zsolt/119', 300),
    ('vers', '/1Moz/1/1', 400),
    ('vers', '/1Moz/4/7', 400),
    ('szó', '/szo/H1242', 250),
    ('szó', '/szo/H7451', 250),
    ('szó', '/szo/G3056', 250),
    ('kereső', '/kereses?q=szeretet', 50),
    ('kereső', '/kereses?q=H7451', 50),
    ('kereső', '/kereses?frazis=Isten+szeretete', 50),
]
# Mért, de a határt ma nem tartó oldalak: útvonal -> (a megengedett idő ms, az SQL-utasítások megengedett száma, ok és célfeladat). Megszámolt lista.
KIVETEL = {}
KIVETEL_DB = len(KIVETEL)

SQL_HATAR = 100
TALALAT_HATAR_MS = 20
MERES_DB = 3


def _kornyezet():
    try:
        import flask  # noqa: F401
    except ImportError:
        raise unittest.SkipTest('nincs Flask: a sebességőr kimarad (nem zöld)')
    if not os.path.isfile(DB):
        raise unittest.SkipTest('nincs pardes.db (%s): a sebességőr kimarad (nem zöld)' % DB)


class TestSebesseg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _kornyezet()
        import alkalmazas
        cls.app = alkalmazas.letrehoz(DB, 'belso', elomelegit_ki=False)
        cls.ex = cls.app.extensions['pardes']
        cls.c = cls.app.test_client()
        cls.con = cls.ex['db'].kapcsolat()
        for _, ut, _ in OLDALAK:                                  # bemelegítés: sablonok, modulok, lusta betöltések
            cls.c.get(ut)
        cls.eredmeny = {}

    def _mer(self, ut):
        """(legjobb ms, SQL-utasítások száma a legjobb mérésben, találat ms) az útvonalra; a lapgyorsítótár minden mérés előtt üres."""
        if ut in self.eredmeny:
            return self.eredmeny[ut]
        ms, sql_db = [], []
        for _ in range(MERES_DB):
            self.ex['cache'].urit()
            sorok = []
            self.con.set_trace_callback(sorok.append)
            try:
                import time
                t = time.perf_counter()
                r = self.c.get(ut)
                ms.append((time.perf_counter() - t) * 1000)
            finally:
                self.con.set_trace_callback(None)
            self.assertEqual(r.status_code, 200, '%s: %d' % (ut, r.status_code))
            sql_db.append(len(sorok))
        import time
        t = time.perf_counter()
        r = self.c.get(ut)
        talalat = (time.perf_counter() - t) * 1000
        self.assertEqual(r.headers.get('X-Cache'), 'HIT', '%s: a második kérés nem gyorsítótár-találat' % ut)
        self.eredmeny[ut] = (min(ms), min(sql_db), talalat, sorted(ms))
        return self.eredmeny[ut]

    def test_idokorlat_es_lekerdezesszam(self):
        rossz = []
        for tipus, ut, hatar in OLDALAK:
            ms, sql_db, _, mind = self._mer(ut)
            ido_hatar, sql_hatar = KIVETEL.get(ut, (hatar, SQL_HATAR, ''))[:2]
            if os.environ.get('PARDES_SEBESSEG_KIIR') or '-v' in sys.argv:
                print('  %-7s %-34s %6.0f ms (határ %d)  %4d SQL (határ %d)   mérések: %s' % (tipus, ut, ms, ido_hatar, sql_db, sql_hatar,
                                                                                      ' '.join('%.0f' % x for x in mind)))
            if ms > ido_hatar:
                rossz.append('%s %s: %.0f ms > %d ms' % (tipus, ut, ms, ido_hatar))
            if sql_db > sql_hatar:
                rossz.append('%s %s: %d SQL-utasítás > %d' % (tipus, ut, sql_db, sql_hatar))
        self.assertEqual(rossz, [], 'a sebességőr határai nem teljesülnek (meleg szerver, gyorsítótár nélkül)')

    def test_gyorsitotar_talalat(self):
        rossz = []
        for tipus, ut, _ in OLDALAK:
            _, _, talalat, _ = self._mer(ut)
            if talalat > TALALAT_HATAR_MS:
                rossz.append('%s %s: %.1f ms > %d ms' % (tipus, ut, talalat, TALALAT_HATAR_MS))
        self.assertEqual(rossz, [], 'gyorsítótár-találat lassabb a határnál')

    def test_a_kivetelek_szama_rogzitett(self):
        self.assertEqual(len(KIVETEL), KIVETEL_DB)
        self.assertTrue(all(len(v) == 3 and v[2].strip() for v in KIVETEL.values()), 'minden kivételnek ok és célfeladat kell')


if __name__ == '__main__':
    unittest.main()
