"""F235: az olvasó sebességőre — időkorlát és lekérdezésszám a helyi pardes.db-n (a push előtti kapu `teszt_futtat.py --gyors` részeként fut).

Egy lap előállításának ideje MELEG szerveren, GYORSÍTÓTÁR NÉLKÜL (a lapgyorsítótár ürítve, a folyamat és az adatbázis-fájl gyorsítótára meleg):

    fejezet  ≤ 300 ms      vers  ≤ 400 ms      szó-lap  ≤ 250 ms      kereső  ≤ 50 ms
    laponként ≤ 100 SQL-utasítás      gyorsítótár-találat ≤ 20 ms

A mérés a Flask belső kliensével fut (nincs hálózat), a gyorsítótár ürítése a közvetlen `cache.urit()` (tesztkörnyezet: más kapu nincs, a szerver
nem kínál ürítő végpontot). Minden oldalt egyszer bemelegítünk (a sablonok, a modulok és a lusta betöltések), utána háromszor mérünk, és a legjobb idő
számít: a határ a kód lassulását őrzi, nem a gép pillanatnyi terhelését (a párhuzamos munkamenetek zaja ellen). Az SQL-utasítások számát a
kapcsolat `set_trace_callback`-je adja (a `PRAGMA`-kat is beleértve); a határhoz a három mérés legkisebb SQL-száma számít.

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

    def test_az_elotoltes_ugyanazt_adja_mint_az_egyedi_lekerdezes(self):
        """A lapszintű előtöltés (`elotoltes`) a vers- és strongszintű függvényeknek ugyanazt az értéket adja, mint az egyedi lekérdezés (a lap
        szövege ezért nem változhat): kilenc fejezeten át (köztük arámi részek, a 400-as csomaghatáron átnyúló vers- és strongszám)."""
        import lekerdezesek as q
        con = self.con
        igek = []
        for kk, fej in (('Zsolt', 119), ('Zsolt', 78), ('Zsolt', 89), ('Zsolt', 105), ('1Móz', 1), ('1Móz', 2), ('1Móz', 3), ('Dán', 2), ('Ezsd', 4)):
            igek += [ig for ig, _, _ in q.fejezet_versek(con, kk, fej)]
        self.assertGreater(len(igek), 400, 'a minta nem lépi át a 400-as csomaghatárt')
        strongok = q.heber_strongok_versekre(con, igek)
        self.assertGreater(len(strongok), 400, 'a strongok száma nem lépi át a 400-as csomaghatárt')

        def mind():
            ki = {}
            for ig in igek:
                ki[('eredeti', ig)] = q.eredeti_szavak(con, ig)
                ki[('macula', ig)] = q.macula(con, ig)
                ki[('lxx', ig)] = q.lxx_szavak_sorrendben(con, ig)
            xml = [m['xml_id'] for ig in igek for m in q.macula(con, ig) if m.get('xml_id')]
            ki['aramai'] = q.aramai_xml(con, xml)
            for st in strongok + ['H9999', 'G0001']:                # a nem létező strong: üres válasz
                ki[('bdb_en', st)] = q.bdb_angol(con, st)
                ki[('bdb_hu', st)] = q.bdb_magyar(con, st)
                ki[('bdb_meta', st)] = q.bdb_magyar_meta(con, st)
                ki[('lxx_h', st)] = q.lxx_bridge_h(con, st)
            return ki
        egyedi = mind()
        with q.elotoltes():
            q.elotolt_versek(con, igek)
            q.elotolt_strongok(con, strongok + ['H9999', 'G0001'])
            sorok = []
            con.set_trace_callback(sorok.append)
            try:
                elotoltott = mind()
            finally:
                con.set_trace_callback(None)
        self.assertLess(len(sorok), 20, 'az előtöltött hatókörben a lekérdezések gyorsítótárból válaszolnak: %d SQL' % len(sorok))
        self.assertEqual(sorted(egyedi, key=repr), sorted(elotoltott, key=repr))
        rossz = [k for k in egyedi if egyedi[k] != elotoltott[k]]
        self.assertEqual(rossz, [], 'az előtöltött érték eltér az egyedi lekérdezésétől: %r' % (rossz[:5],))
        # a hatókör vége után nincs szivárgás: az egyedi lekérdezés a régi úton fut
        sorok2 = []
        con.set_trace_callback(sorok2.append)
        try:
            q.bdb_magyar(con, strongok[0])
        finally:
            con.set_trace_callback(None)
        self.assertTrue(sorok2, 'a hatókör után a függvény nem válaszolhat gyorsítótárból')

    def test_a_tiltott_tabla_nem_olvasodik_az_elotoltesben(self):
        """`elotolt_strongok(bdb=False)` nem érinti a `forditasok` és a `bdb` táblát (a kiadás által kizárt tábla olvasása hibát ad)."""
        import lekerdezesek as q
        sorok = []
        self.con.set_trace_callback(sorok.append)
        try:
            with q.elotoltes():
                q.elotolt_strongok(self.con, ['H0430', 'H1254'], bdb=False)
        finally:
            self.con.set_trace_callback(None)
        szoveg = ' '.join(sorok).lower()
        self.assertIn('lxx_bridge', szoveg)
        self.assertNotIn('forditasok', szoveg)
        self.assertNotIn('from bdb ', szoveg)

    def test_az_elomelegites_lefut_es_a_lapgyorsitotarba_tolt(self):
        """Az `alkalmazas.elomelegit` a háttérszálon lefut, nem nyel el hibát némán, és a bemelegítő oldalak a lapgyorsítótárba kerülnek."""
        import alkalmazas
        app = alkalmazas.letrehoz(DB, 'belso', elomelegit_ki=False)
        ex = app.extensions['pardes']
        self.assertFalse(ex['elomelegitve'].is_set())
        alkalmazas.elomelegit(app)
        self.assertTrue(ex['elomelegitve'].wait(300), 'az előmelegítés nem fejeződött be')
        self.assertIsNone(ex.get('elomelegit_hiba'), 'az előmelegítés hibával állt le: %r' % (ex.get('elomelegit_hiba'),))
        r = app.test_client().get('/1Moz/1')
        self.assertEqual(r.headers.get('X-Cache'), 'HIT', 'a bemelegített oldal gyorsítótár-találat kell legyen')

    def test_a_kivetelek_szama_rogzitett(self):
        self.assertEqual(len(KIVETEL), KIVETEL_DB)
        self.assertTrue(all(len(v) == 3 and v[2].strip() for v in KIVETEL.values()), 'minden kivételnek ok és célfeladat kell')


if __name__ == '__main__':
    unittest.main()
