"""Az olvasói szerver tesztjei (#76 M2): unittest.

Futtatás (Python 3.12 alatt, a `pardes` WSL-disztribúció venv-jével; a Flask nélküli futtatás a Flask-os teszteket kihagyja):
    PARDES_DB=/home/basesoft/pardes/pardes.db python eszkozok/olvaso_szerver/teszt_olvaso_szerver.py
Környezeti változók:
    PARDES_DB          a pardes.db helye (alap: a repó gyökerének pardes.db-je); hiányában a DB-s tesztek kimaradnak
    PARDES_PILOT_JSON  az `adat.py` kimenete szakaszonként: <könyvtár>/<azonosító>/olvaso_pilot.json (1moz_1_25, zsolt_22);
                       hiányában a D2-teszt az `adat.py`-t ideiglenes könyvtárba futtatja (lassú: ~1-2 perc szakaszonként)

A tesztek csak olvasnak; a pardes.db-t nem módosítják, a repóba nem írnak.
"""
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D)).replace('\\', '/') + '/'
sys.path.insert(0, D)

import adatbazis
import blokkok
import hozzaferes
import lekerdezesek as q
import oldalak

try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

DB = os.environ.get('PARDES_DB') or (GY + 'pardes.db')
VAN_DB = os.path.exists(DB)
KONFIG = os.path.join(D, 'konfig')


def app_keszit(kiadas='belso', hozz=None):
    import alkalmazas
    return alkalmazas.letrehoz(db_ut=DB, kiadas=kiadas, hozzaferes=hozz)


# =====================================================================================================================
class TestHozzaferesKonfig(unittest.TestCase):
    """A hozzáférési szintek konfigurációból zárnak; a kódban csak a mechanizmus van."""

    def test_alap_konfig(self):
        h = hozzaferes.Hozzaferes.betolt(KONFIG)
        self.assertEqual(h.alap_szint, 'kutato')
        self.assertEqual(h.szint(), len(h.szintek) - 1)      # az első kiadásban mindenki mindent lát
        self.assertTrue(h.lathato('vers.tsk', h.szint()))

    def test_szint_zar(self):
        h = hozzaferes.Hozzaferes(['a', 'b', 'c'], 'a', {'x': 'c', 'y': 'b'}, 'a')
        self.assertFalse(h.lathato('x', 0))
        self.assertFalse(h.lathato('y', 0))
        self.assertTrue(h.lathato('y', 1))
        self.assertTrue(h.lathato('x', 2))
        self.assertTrue(h.lathato('ismeretlen_a_konfigban', 0))      # default szint

    def test_ismeretlen_blokk_a_legmagasabb_szintre_esik(self):
        h = hozzaferes.Hozzaferes(['a', 'b', 'c'], 'c', {}, 'a')
        self.assertFalse(h.lathato('nincs_a_regiszterben', 1, ismert=False))
        self.assertTrue(h.lathato('nincs_a_regiszterben', 2, ismert=False))

    def test_ismeretlen_blokk_azonosito_a_konfigban_indulasi_hiba(self):
        h = hozzaferes.Hozzaferes(['a', 'b'], 'a', {'vers.tsk': 'b', 'vers.tsl_elgepelve': 'b'}, 'a')
        with self.assertRaises(ValueError) as e:
            h.ellenoriz_blokkok(blokkok.BLOKK_ID)
        self.assertIn('vers.tsl_elgepelve', str(e.exception))
        hozzaferes.Hozzaferes(['a', 'b'], 'a', {'vers.tsk': 'b'}, 'a').ellenoriz_blokkok(blokkok.BLOKK_ID)   # érvényes: nem dob
        hozzaferes.Hozzaferes.betolt(KONFIG).ellenoriz_blokkok(blokkok.BLOKK_ID)                              # az alap konfig érvényes

    @unittest.skipUnless(VAN_DB, 'nincs pardes.db')
    def test_oldalgyar_nem_indul_elgepelt_konfiggal(self):
        h = hozzaferes.Hozzaferes(['a', 'b'], 'a', {'vers.nincs_ilyen': 'b'}, 'a')
        with self.assertRaises(ValueError):
            oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), h)

    def test_hibas_konfig_megallit(self):
        with self.assertRaises(ValueError):
            hozzaferes.Hozzaferes(['a', 'b'], 'z', {}, 'a')            # ismeretlen alapértelmezett szint
        with self.assertRaises(ValueError):
            hozzaferes.Hozzaferes(['a', 'b'], 'a', {'x': 'q'}, 'a')    # ismeretlen blokk-szint
        with self.assertRaises(ValueError):
            hozzaferes.Hozzaferes(['a', 'a'], 'a', {}, 'a')            # ismétlődő szint


class TestSzabalyok(unittest.TestCase):
    """Statikus szabályok (N-F76c elő): az SQL csak a lekerdezesek.py-ban áll, paraméterezve."""

    def _forras(self, nev):
        with open(os.path.join(D, nev), encoding='utf-8') as f:
            return f.read()

    def test_sql_csak_a_lekerdezesekben(self):
        for nev in sorted(os.listdir(D)):
            if not nev.endswith('.py') or nev in ('lekerdezesek.py', 'frissesseg.py') or nev.startswith('teszt_'):
                continue
            sorok = self._forras(nev).split('\n')
            for i, s in enumerate(sorok, 1):
                if '.execute(' in s and nev != 'adatbazis.py':
                    self.fail('%s:%d: .execute( a lekerdezesek.py-n kívül' % (nev, i))
                if nev == 'adatbazis.py' and '.execute(' in s and 'PRAGMA' not in s:
                    self.fail('%s:%d: nem PRAGMA .execute(' % (nev, i))

    def test_nincs_osszefuzott_sql(self):
        """A lekerdezesek.py-ban minden execute első argumentuma szöveg-literál vagy a helyőrző-lánccal összeállított;
        f-string és `%`-os formázás SQL-en nincs."""
        s = self._forras('lekerdezesek.py')
        self.assertNotRegex(s, r'execute\(\s*f["\']')
        self.assertNotRegex(s, r'execute\([^)]*["\']\s*%\s*[\(a-z]')
        self.assertNotIn(".format(", s.split('def _in(')[1].split('# ---')[0] if 'def _in(' in s else '')

    def test_jinja_autoescape(self):
        s = self._forras('oldalak.py')
        self.assertIn("select_autoescape(['html'])", s)

    def test_a_safe_csak_a_panel_toredekekre(self):
        for nev in os.listdir(os.path.join(D, 'sablonok')):
            with open(os.path.join(D, 'sablonok', nev), encoding='utf-8') as f:
                t = f.read()
            for m in re.finditer(r'\{\{\s*([^}]*?)\|safe', t):
                self.assertIn(m.group(1).strip(), ('szo_html', 'vers_html'), '%s: |safe: %s' % (nev, m.group(1)))

    def test_nincs_inline_script_vagy_stilus(self):
        for nev in os.listdir(os.path.join(D, 'sablonok')):
            with open(os.path.join(D, 'sablonok', nev), encoding='utf-8') as f:
                t = f.read()
            self.assertNotRegex(t, r'<script(?![^>]*\bsrc=)', nev)
            self.assertNotRegex(t, r'\sstyle=', nev)
            self.assertNotRegex(t, r'\son[a-z]+=', nev)

    def test_hnorm_konyv_slug(self):
        self.assertEqual(q.hnorm('h216'), 'H0216')
        self.assertEqual(q.hnorm('G1504a'), 'G1504A')
        self.assertIsNone(q.hnorm("H0216' OR 1=1--"))
        self.assertIsNone(q.hnorm('<script>'))
        self.assertIsNone(q.hnorm('H12345'))
        self.assertEqual(q.konyv_slug('1Móz'), '1Moz')

    def test_biztonsagos_vissza(self):
        f = oldalak.biztonsagos_vissza
        self.assertEqual(f('/1Moz/1?szo=H0216'), '/1Moz/1?szo=H0216')
        for rossz in ('//evil.com', 'http://evil.com', '/\\evil.com', 'javascript:alert(1)', '', None, '/x:y', 'evil', '/a\r\nb'):
            self.assertEqual(f(rossz), '/', repr(rossz))


class TestMaculaRegiAdatbazis(unittest.TestCase):
    """A `macula` az F115.4 előtt épült adatbázison (nincs `lxx_szo_forras` / `lxx_szo_rahlfs`) is fut: a két mező üres.
    Eset: a 2026-10-14-i pardes.db-n minden fejezetlap 500-at adott (`no such column: lxx_szo_forras`)."""
    ALAP = ('igehely TEXT, xml_id TEXT, szo TEXT, lemma TEXT, strong_nyers TEXT, morf TEXT, szofaj TEXT, gloss TEXT, '
            'lxx_szo TEXT, lxx_strong TEXT')
    SOR = ('1Móz 1:1', 'o010010010011', 'בְּ', 'בְּ', 'H9003', 'Rd', 'prep', 'in', 'ἐν', 'G1722')

    def _con(self, uj):
        con = sqlite3.connect(':memory:')
        con.execute('CREATE TABLE token_macula (%s%s)' % (self.ALAP, ', lxx_szo_forras TEXT, lxx_szo_rahlfs TEXT' if uj else ''))
        con.execute('INSERT INTO token_macula VALUES (%s)' % ', '.join('?' * (len(self.SOR) + (2 if uj else 0))),
                    self.SOR + (('ενς', 'ἐν') if uj else ()))
        return con

    def test_regi_sema_ures_lxx_forras(self):
        (m,) = q.macula(self._con(False), '1Móz 1:1')
        self.assertEqual((m['lxx'], m['lxx_strong'], m['lxx_forras'], m['lxx_rahlfs']), ('ἐν', q.hnorm('G1722'), '', ''))

    def test_uj_sema_valtozatlan(self):
        (m,) = q.macula(self._con(True), '1Móz 1:1')
        self.assertEqual((m['lxx_forras'], m['lxx_rahlfs']), ('ενς', 'ἐν'))


class TestBdbMagyarOsszefuzo(unittest.TestCase):
    """F128 (DT-F128a (a), DT-F128f (3), DT-F128g (a)): a `bdb_magyar` / `bdb_magyar_meta` a közös összefűzőn át — a
    szakaszonként fordított Strong szövege a `sz<sorszam>` sorok összefűzése (nem az utolsó sor), a jóváhagyott `kezi`
    `teljes` sor addig él, amíg a szakaszsorok nem mind `kezi`-k; a régi (egy `teljes` soros) Strong változatlan."""

    def _con(self, sorok):
        con = sqlite3.connect(':memory:')
        con.execute('CREATE TABLE forditasok (szotar TEXT, strong TEXT, entry_id TEXT, jelentes_szam TEXT, mezo TEXT, '
                    'forras_hash TEXT, forditas_hu TEXT, allapot TEXT, modell TEXT, datum TEXT, terminologia_verzio TEXT, '
                    'megjegyzes TEXT)')
        for st, jsz, hu, allapot, modell, datum in sorok:
            con.execute('INSERT INTO forditasok VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                        ('BDB', st, st, jsz, 'forditas_hu', 'h', hu, allapot, modell, datum, 'v3', ''))
        return con

    def test_regi_teljes_sor_valtozatlan(self):
        con = self._con([('H7121', '2.c', 'részlet', 'kezi', '', '2026.09.01'),
                         ('H7121', 'teljes', 'egész\\nszöveg', 'kezi', 'claude-opus-5-5', '2026.10.01')])
        self.assertEqual(q.bdb_magyar(con, 'H7121'), 'egész\nszöveg')
        self.assertEqual(q.bdb_magyar_meta(con, 'H7121'), 'claude-opus-5-5, 2026.10.01')
        self.assertIsNone(q.bdb_magyar(con, 'H0002'))
        self.assertIsNone(q.bdb_magyar_meta(con, 'H0002'))

    def test_szakaszsorok_osszefuzve(self):
        con = self._con([('H0001', 'teljes', 'régi', 'elavult', 'claude-sonnet-5-5', '2026.10.01'),
                         ('H0001', 'sz2', 'apa', 'sonnet', 'claude-sonnet-5-5', '2026.10.22'),
                         ('H0001', 'sz1', 'H1. ab', 'sonnet', 'claude-opus-5-5', '2026.10.21')])
        self.assertEqual(q.bdb_magyar(con, 'H0001'), 'H1. ab apa')
        self.assertEqual(q.bdb_magyar_meta(con, 'H0001'), 'claude-opus-5-5 / claude-sonnet-5-5, 2026.10.22')

    def test_kezi_teljes_elsobbsege(self):
        con = self._con([('H8415', 'teljes', 'jóváhagyott', 'kezi', 'claude-opus-5-5', '2026.10.01'),
                         ('H8415', 'sz1', 'a', 'sonnet', 'claude-sonnet-5-5', '2026.10.22'),
                         ('H8415', 'sz2', 'b', 'sonnet', 'claude-sonnet-5-5', '2026.10.22')])
        self.assertEqual(q.bdb_magyar(con, 'H8415'), 'jóváhagyott')
        self.assertEqual(q.bdb_magyar_meta(con, 'H8415'), 'claude-opus-5-5, 2026.10.01')


@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class TestRegiszterEsAdatbazis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = adatbazis.Adatbazis(DB, 'belso')
        cls.con = cls.db.kapcsolat()
        cls.kozos = oldalak.Kozos(cls.con)

    def test_blokkszam_es_oldalak(self):
        # 46 = az M2 40 azonosítója (a pilot 39 mért adatblokkja; a 9. BSB/KJV két bejegyzés) + az M2b 6 új azonosítója: két szócsempe-blokk
        # (héber, LXX), az LXX versszintű együttelőfordulás, az „Ebben a versben” (szó-lap), az adatréteg-blokk háromra bontása (+2); a pilot kirajzolt blokk-készlete
        # a teszt_pilot_aranymintaval.py-ban van (a DT-F76e–i döntések kódja és tesztje kész, expectedFailure nincs)
        # +2 (F76.30–31): a bontott BDB-szócikk (szo.bdb_apparatus) és az „LXX többlet” blokk (vers.lxx_tobblet, „az adat még nincs a DB-ben”)
        # +1 (F99 M1): a „Rokon szavak (OSHL-gyökcsalád)” blokk (szo.oshl_csalad)
        # +1 (F121, DT393): az UBS DBH-jelentések szónézet-blokkja (szo.ubs_dbh)
        self.assertEqual(len(blokkok.REGISZTER), 50)
        self.assertEqual({b.oldal for b in blokkok.REGISZTER}, set(blokkok.OLDALAK))

    def test_minden_tablanak_van_licencsora(self):
        for b in blokkok.REGISZTER:
            for j in b.jelleg:
                self.assertIn(j, blokkok.JELLEG)
            sor = blokkok.forras_sor(b, self.kozos)            # hiány BlokkHiba
            self.assertTrue(sor.startswith('Forrás és licenc: '), b.id)
            for t in b.tablak:
                self.assertTrue(self.con.execute("SELECT 1 FROM sqlite_master WHERE name=?", (t,)).fetchone(), '%s: nincs %s tábla' % (b.id, t))

    # a blokk -> a pilot `sablon.html` SUGO-listájának címe; pontos=True: a blokknak saját pilot-címe van (a jellegek halmaza egyezik),
    # False: a pilot-cím több regiszter-blokkot fed (a blokk jellegei a pilot jellegeinek részhalmaza)
    PILOT_CIM = {
        'vers.karoli': ('Károli-szöveg', False), 'vers.par': ('Károli-szöveg', False), 'vers.eredeti': ('Héber szöveg', False),
        'vers.macula_morf': ('Ebben a versben', False), 'vers.macula_gorog': ('Ebben a versben', False), 'vers.lxx_szavak': ('Septuaginta', True),
        'vers.lxx_versszam': ('Versszámozás', False), 'vers.versszamozas': ('Versszámozás', True),
        'vers.bsb': ('Angol szó szavanként (BSB)', True), 'vers.kjv': ('Angol szó szavanként (KJV)', True), 'vers.nave': ('Témák (Nave)', True),
        'vers.tipnr': ('Tulajdonnevek (TIPNR)', True), 'vers.morf_hu': ('Héber szöveg', False), 'vers.motivum': ('Motívumadat (adatréteg)', True),
        'vers.kapcsolat': ('Igehely-kapcsolatok (adatréteg)', True), 'vers.lxx_dontes': ('LXX-fordítói döntések (adatréteg)', True),
        'vers.lxx_par': ('LXX versszintű együttelőfordulás', True), 'vers.heber_csempe': ('Héber szöveg', True), 'vers.lxx_csempe': ('Septuaginta', True),
        'szo.ebben': ('Ebben a versben', True), 'szo.bdb_apparatus': ('BDB-szócikk', True), 'vers.lxx_tobblet': ('LXX többlet és számozási eltérés', True),
        'vers.tsk': ('Kereszthivatkozások (TSK', True), 'vers.kh': ('Károli-kereszthivatkozások', True), 'vers.ubs': ('Ebben a versben', False),
        'szo.szotar': ('Szó adatai (héber)', False), 'szo.elofordulas': ('Szó adatai (héber)', False), 'szo.karoli_alakok': ('Szó adatai (héber)', False),
        'szo.bdb_angol': ('BDB-szócikk', False), 'szo.bdb_magyar': ('BDB-szócikk', False), 'szo.lxx_bridge': ('Görög megfelelő', True),
        'szo.sdbh': ('Szemantikai domén (SDBH)', True), 'szo.sece_h': ('SECE-szócikk (héber)', True), 'szo.oshl': ('TWOT- és BDB-azonosító', True),
        'szo.oshl_csalad': ('TWOT- és BDB-azonosító', False),   # F99 M1: a pilotnak nincs gyökcsalád-blokkja; az OSHL-cím jellegét örökli
        'szo.tbesh': ('Bővített Strong-szócikk', True), 'szo.tw_h': ('translationWords', True), 'szo.nyelvtani': ('Szó adatai (héber)', False),
        'szo.tbesg': ('Szó adatai (görög)', False), 'szo.thayer': ('Szótári szöveg (angol)', False), 'szo.usz': ('Az Újszövetségben', True),
        'szo.heber_hatter': ('Héber háttér', True), 'szo.sdgnt': ('Szemantikai domén (SDGNT)', True), 'szo.sece_g': ('SECE-szócikk (görög)', True),
        'szo.lsj': ('LSJ-szócikk', True), 'szo.mcged': ('Mounce-szótár', True), 'szo.ubs_dntg': ('UBS DNTG jelentések', True), 'szo.tw_g': ('translationWords', True),
        # a magyar Thayer/UBS DNTG jelentésnek nincs önálló SUGO-címe: a pilot README „Jelleg” táblája szerint modell-kimenet (#28)
    }

    @staticmethod
    def _pilot_jellegek():
        """A pilot sablon SUGO-listájából: {cím: set(jellegek)} (a sablon a mérvadó)."""
        with open(GY + 'eszkozok/olvaso_pilot/sablon.html', encoding='utf-8') as f:
            t = f.read()
        ki = {}
        for sor in t.split('\n'):
            m = re.match(r"^\s*\['([^']+)', \[.*\], \[((?:'[a-z]+'(?:, )?)+)\]\],?\s*$", sor)
            if m:
                ki[m.group(1)] = set(re.findall(r"'([a-z]+)'", m.group(2)))
        return ki

    def test_jelleg_egyezik_a_pilottal(self):
        """M0 3.4: a regiszter jellegei a pilot sablonjáéval egyeznek; eltérésnél a pilot a mérvadó."""
        pilot = self._pilot_jellegek()
        self.assertGreater(len(pilot), 30)
        for b in blokkok.REGISZTER:
            if b.id == 'szo.magyar_gorog':
                self.assertEqual(b.jelleg, ('modell',))
                continue
            if b.id == 'szo.ubs_dbh':          # F121 (DT393): nincs pilot-megfelelője; angol forrás + magyar modell-fordítás
                self.assertEqual(b.jelleg, ('forras', 'modell'))
                continue
            cim, pontos = self.PILOT_CIM[b.id]
            self.assertIn(cim, pilot, '%s: nincs ilyen pilot-cím: %s' % (b.id, cim))
            mine, theirs = set(b.jelleg), pilot[cim]
            if pontos:
                self.assertEqual(mine, theirs, '%s ↔ %s' % (b.id, cim))
            else:
                self.assertTrue(mine <= theirs, '%s ↔ %s: %s ⊄ %s' % (b.id, cim, mine, theirs))
        self.assertEqual(set(self.PILOT_CIM) | {'szo.magyar_gorog', 'szo.ubs_dbh'}, set(blokkok.BLOKK_ID))

    def test_licenc_jelzesek(self):
        b = blokkok.BLOKK_ID['szo.mcged']
        self.assertIn('nem kereskedelmi', blokkok.forras_sor(b, self.kozos))
        self.assertIn('tisztázatlan', blokkok.forras_sor(blokkok.BLOKK_ID['vers.kjv'], self.kozos))
        self.assertIn('share-alike', blokkok.forras_sor(blokkok.BLOKK_ID['szo.sdbh'], self.kozos))

    def test_konyv_slug_egyedi(self):
        self.assertEqual(len(self.kozos.konyvek), 66)
        self.assertEqual(len({sl for _, sl, _, _ in self.kozos.konyvek}), 66)

    def test_csak_olvaso(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.con.execute('CREATE TABLE x(a)')
        with self.assertRaises(sqlite3.OperationalError):
            self.con.execute("DELETE FROM vers WHERE igehely='1Móz 1:1'")

    def test_authorizer_tiltja_a_kizart_tablat(self):
        for kiadas, tabla, tiltott in (('belso', 'kjv', False), ('nyilvanos', 'kjv', True), ('nyilvanos', 'mcged', False),
                                      ('kereskedelmi', 'kjv', True), ('kereskedelmi', 'mcged', True)):
            db = adatbazis.Adatbazis(DB, kiadas)
            con = db.kapcsolat()
            if tiltott:
                with self.assertRaises(sqlite3.DatabaseError):
                    con.execute('SELECT COUNT(*) FROM %s' % tabla).fetchone()
                self.assertIn(tabla, db.kiserletek)
            else:
                self.assertGreater(con.execute('SELECT COUNT(*) FROM %s' % tabla).fetchone()[0], 0)
                self.assertEqual(db.kiserletek, [])
            db.bezar()

    def test_sql_injekcio_a_lekerdezesekben(self):
        rossz = ["1Móz 1:4' OR '1'='1", "'; DROP TABLE vers;--", 'x" OR 1=1 --', 'H0216 UNION SELECT 1']
        for r in rossz:
            self.assertIsNone(q.karoli_szoveg(self.con, r))
            self.assertEqual(q.tsk(self.con, r), [])
            self.assertEqual(q.fejezet_versek(self.con, r, 1), [])
            self.assertIsNone(q.strong_szotar(self.con, r))
            self.assertEqual(q.tw(self.con, r), [])
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM vers').fetchone()[0], 31158)


# =====================================================================================================================
@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestLapok(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_keszit('belso')
        cls.c = cls.app.test_client()

    def get(self, u, **kw):
        return self.c.get(u, **kw)

    def test_kezdolap_valaszto_es_konyvek(self):
        r = self.get('/')
        self.assertEqual(r.status_code, 200)
        h = r.get_data(as_text=True)
        self.assertIn('<select name="konyv">', h)
        self.assertEqual(len(re.findall(r'<option value=', h)), 66)
        self.assertIn('href="/1Moz/1"', h)
        self.assertIn('name="fej"', h)
        self.assertIn('name="vers"', h)

    def test_konyv_fejezet_vers_lap(self):
        self.assertEqual(self.get('/1Moz').status_code, 200)
        r = self.get('/1Moz/1')
        h = r.get_data(as_text=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(re.findall(r'class="vers[ "]', h)), 31)
        r = self.get('/1Moz/1/4')
        h = r.get_data(as_text=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn('data-igehely="1Móz 1:4"', h)

    def test_allando_cimek_es_nezetek_ugyanazt_adjak(self):
        for n in oldalak.NEZETEK:
            r = self.get('/1Moz/1/4?nezet=' + n)
            self.assertEqual(r.status_code, 200)
            self.assertIn('class="nezet-%s"' % n, r.get_data(as_text=True))

    def test_minden_vers_blokk_jelleggel_es_forrassal(self):
        h = self.get('/r/vers/1Moz/1/4').get_data(as_text=True)
        ids = re.findall(r'data-blokk="([^"]+)"', h)
        self.assertEqual(ids, [b.id for b in blokkok.blokkok_oldalra('vers')])
        self.assertEqual(len(re.findall(r'<h3>[^<]*<span class="jelleg jelleg-', h)), len(ids))      # blokkonként legalább egy címke
        self.assertEqual(len(re.findall(r'<p class="forras">Forrás és licenc: ', h)), len(ids))

    def test_szovegoszlop_jelleg_es_forras_mindharom_nezetben(self):
        for n in oldalak.NEZETEK:
            h = self.get('/1Moz/1/4?nezet=' + n).get_data(as_text=True)
            i = h.index('class="szoveg-jegy"')
            jegy = h[i:i + 2500]
            self.assertIn('jelleg-modell', jegy, n)
            self.assertIn('jelleg-forras', jegy, n)
            self.assertIn('Karoli_Strong_parok (token_par)', jegy, n)
            self.assertIn('Karoli_1908 (vers)', jegy, n)

    def test_minden_szo_blokk_jelleggel_es_forrassal(self):
        for strong, oldal in (('H0216', 'szo_h'), ('G0746', 'szo_g'), ('H9001', 'szo_h')):
            h = self.get('/r/szo/' + strong).get_data(as_text=True)
            ids = re.findall(r'data-blokk="([^"]+)"', h)
            # a vers-kontextust igénylő blokk (szo.ebben) önálló szó-lapon nem jelenik meg
            self.assertEqual(ids, [b.id for b in blokkok.blokkok_oldalra(oldal) if not b.vers_kell], strong)
            self.assertEqual(len(re.findall(r'<h3>[^<]*<span class="jelleg jelleg-', h)), len(ids))
            self.assertEqual(len(re.findall(r'<p class="forras">Forrás és licenc: ', h)), len(ids))

    def test_szo_lap_vers_kontextussal_az_ebben_a_versben_blokkal(self):
        h = self.get('/1Moz/1/2?szo=H6440&ful=szo').get_data(as_text=True)
        self.assertIn('data-blokk="szo.ebben"', h)
        self.assertNotIn('data-blokk="szo.ebben"', self.get('/szo/H6440').get_data(as_text=True))
        self.assertNotIn('data-blokk="szo.ebben"', self.get('/r/szo/H6440').get_data(as_text=True))

    def test_usz_elofordulas_bontasa_lanc_elemre(self):
        """DT-F76d / DT133: a görög szó-lapon az előfordulás mellett látszik a „+” Strong-lánc eredetű rész (G4218: 54, ebből 25)."""
        con = self.app.extensions['pardes']['db'].kapcsolat()
        self.assertEqual(q.usz(con, 'G4218')[0], 54)
        self.assertEqual(q.usz_lanc(con, 'G4218'), 25)
        h = self.get('/r/szo/G4218').get_data(as_text=True)
        self.assertIn('<b>54</b> előfordulás', h)
        self.assertIn('ebből <b>25</b> láncelemként', h)
        self.assertIn('az egész mezős előfordulás 29', h)
        # invariáns: összes = egész mezős + láncelem (több szóra, független számolás a nyers tábla egész mezős soraiból)
        for g in ('G2532', 'G0746', 'G3056', 'G1504', 'G4218', 'G1161'):
            egesz = con.execute("SELECT COUNT(*) FROM token_eredeti WHERE nyelv='G' AND strong_lanc=?", (g,)).fetchone()[0]
            self.assertEqual(q.usz(con, g)[0], egesz + q.usz_lanc(con, g), g)
        # lánc nélküli szónál nincs bontás-sor
        self.assertNotIn('láncelemként', self.get('/r/szo/G0746').get_data(as_text=True))

    def test_szo_lap_allando_cim(self):
        r = self.get('/szo/H0216')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.get('/szo/h216').status_code, 200)        # normalizált bemenet
        self.assertEqual(self.get('/szo/H9999').status_code, 404)
        self.assertEqual(self.get('/szo/xyz').status_code, 404)

    def test_ismeretlenek_404(self):
        for u in ('/NincsIlyen', '/1Moz/999', '/1Moz/1/999', '/r/vers/1Moz/1/999', '/r/szo/Q1', '/nezet/titkos', '/nincs/ilyen/ut/x'):
            self.assertEqual(self.get(u).status_code, 404, u)

    def test_pardes_db_nem_kerul_ki(self):
        for u in ('/pardes.db', '/pardes.db-wal', '/pardes.db-journal', '/adat/jeloltek.tsv', '/konkordancia/Karoli_1908.tsv',
                  '/statikus/../../../pardes.db', '/statikus/%2e%2e/%2e%2e/pardes.db', '/eszkozok/olvaso_szerver/adatbazis.py',
                  '/statikus/olvaso.py', '/static/pardes.db'):
            r = self.get(u)
            self.assertIn(r.status_code, (404, 400), u)
            self.assertNotIn(b'SQLite format 3', r.data[:100], u)
        r = self.get('/statikus/olvaso.css')
        self.assertEqual(r.status_code, 200)
        r.close()

    def test_statusz(self):
        r = self.get('/statusz')
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertEqual(j['kiadas'], 'belso')
        # a hash-sorok száma az építéstől függ (F99: +bdb_aranyminta, +bdb_vers_jelentes): a meta tábla saját számával vetjük össze
        con = adatbazis.Adatbazis(DB, 'belso').kapcsolat()
        vart = con.execute("SELECT COUNT(*) FROM meta WHERE kulcs LIKE 'hash:%'").fetchone()[0]
        con.close()
        self.assertGreaterEqual(vart, 73)
        self.assertEqual(j['meta_hash_sorok'], vart)
        self.assertRegex(j['epites_ts'], r'^\d{4}-\d\d-\d\dT')
        self.assertNotIn('igehely', r.get_data(as_text=True).lower().replace('adatbazis_kulcs', ''))   # nincs adat-tartalom

    def test_gyorsitotar_es_etag(self):
        a = self.get('/1Moz/1/3')
        b = self.get('/1Moz/1/3')
        self.assertEqual(b.headers['X-Cache'], 'HIT')
        self.assertEqual(a.headers['ETag'], b.headers['ETag'])
        r = self.get('/1Moz/1/3', headers={'If-None-Match': a.headers['ETag']})
        self.assertEqual(r.status_code, 304)
        self.assertEqual(b.headers['Cache-Control'], 'no-cache')      # belső kiadás
        # más nézet = más kulcs
        c = self.get('/1Moz/1/3?nezet=interlinearis')
        self.assertNotEqual(c.headers['ETag'], a.headers['ETag'])

    def test_etag_es_gyorsitotar_kulcsa_tartalmazza_a_kod_verziojat(self):
        """Kódváltozás után a szerver nem adhat 304-et és nem szolgálhat ki régi lapot a gyorsítótárból (F76.30)."""
        gyar = self.app.extensions['pardes']['gyar']
        a = self.get('/1Moz/1/3')
        self.assertEqual(self.get('/1Moz/1/3').headers['X-Cache'], 'HIT')
        regi = gyar.kod_verzio
        try:
            gyar.kod_verzio = 'masik-kod-verzio'
            b = self.get('/1Moz/1/3', headers={'If-None-Match': a.headers['ETag']})
            self.assertEqual(b.status_code, 200)                         # a régi ETag-re már nem 304
            self.assertEqual(b.headers['X-Cache'], 'MISS')                # és nem a régi lap jön a gyorsítótárból
            self.assertNotEqual(b.headers['ETag'], a.headers['ETag'])
        finally:
            gyar.kod_verzio = regi
        self.assertEqual(self.get('/1Moz/1/3').headers['ETag'], a.headers['ETag'])
        self.assertIn(regi, str(self.get('/statusz').get_data(as_text=True)))

    def test_bdb_apparatus_jellege_a_bontas_nyelvetol_fugg(self):
        """F76.32 (E7): a „modell-kimenet” csak a magyar fordításból készült bontásnál áll a címkék között."""
        c = self.get
        hu = c('/r/szo/H6440').get_data(as_text=True)
        i = hu.index('data-blokk="szo.bdb_apparatus"')
        self.assertIn('jelleg-modell', hu[i:hu.index('</h3>', i)])
        for s in ('H0002', 'H0003', 'H0005'):          # ahol nincs magyar BDB: angol bontás (vagy nincs szócikk)
            t = c('/r/szo/' + s).get_data(as_text=True)
            if 'data-blokk="szo.bdb_apparatus"' not in t:
                continue
            j = t.index('data-blokk="szo.bdb_apparatus"')
            blokk = t[j:t.index('</section>', j)]
            if 'Magyar fordítás nincs' in blokk:
                self.assertNotIn('jelleg-modell', blokk[:blokk.index('</h3>')], s)
                return
        self.skipTest('nincs angol-only BDB-szócikk a mintában')

    def test_bdb_jelentesszerkezet_jeloloi_a_szocikkbol(self):
        """A jelentésszerkezet jelölője a szócikké (H1242 בֹּקֶר: 1 → a.–h., 2), nem a böngésző 1, 2, 3 számozása: a lap a jelölőt a
        `data-jel` attribútumba írja, a stíluslap ezt mutatja (`list-style: none` + `content: attr(data-jel)`)."""
        t = self.get('/r/szo/H1242').get_data(as_text=True)
        i = t.index('data-blokk="szo.bdb_apparatus"')
        blokk = t[i:t.index('</section>', i)]
        self.assertEqual(re.findall(r'<li id="[^"]+" data-jel="([^"]*)"><details', blokk), ['1', '2'])
        self.assertEqual(re.findall(r'<li id="[^"]+" data-jel="([a-z]\.)"', blokk), ['%s.' % b for b in 'abcdefgh'])
        css = open(os.path.join(D, 'statikus', 'olvaso.css'), encoding='utf-8').read()
        self.assertRegex(css, r'ol\.jel, ol\.al \{[^}]*list-style: none')
        self.assertRegex(css, r'ol\.jel > li::before, ol\.al > li::before \{[^}]*content: attr\(data-jel\)')

    def test_bdb_jelmagyarazat(self):
        """A BDB rövidítései (konfig/bdb_jelek.tsv, kézi) a jelentések szövegében <abbr>-ral, a blokk végén a szócikkben előfordulók
        listája; a forrásjel csak zárójelben jelölő („(J)” igen, „J-ben” nem)."""
        t = self.get('/r/szo/H1242').get_data(as_text=True)
        i = t.index('data-blokk="szo.bdb_apparatus"')
        blokk = t[i:t.index('</section>', i)]
        self.assertIn('<abbr title="A. Klostermann">Klo</abbr>', blokk)
        self.assertIn('(<abbr title="jahvista forrás', blokk)
        self.assertIn('<h4>Jelmagyarázat</h4>', blokk)
        jm = blokk[blokk.index('<dl class="jelmagyarazat">'):blokk.index('</dl>')]
        jelek = re.findall(r'<dt>([^<]+)</dt>', jm)
        for j in ('J', 'P', 'Klo', 'We', 'Dr', 'Che'):
            self.assertIn(j, jelek)
        self.assertEqual(len(jelek), len(set(jelek)))
        self.assertNotIn('>J</abbr>-ben', blokk)
        jeles = blokkok._jeles
        self.assertEqual(str(jeles('Jelentés (J-ben) Dresden')), 'Jelentés (J-ben) Dresden')
        self.assertEqual(str(jeles('<b>')), '&lt;b&gt;')

    def test_bdb_egybetus_rovidites(self):
        """N-F131x: a BDB egybetűs rövidítései (a forrásban ׳י) a helyes alakban (י׳), <abbr class="rovidites">-ként, mint a lexikonlapon
        (közös jelölő: eszkozok/bdb_rovidites.py); a címszó feloldása a TBESH-lemma a jóváhagyott kiejtéssel. Minden BDB-blokkban."""
        t = self.get('/r/szo/H7121').get_data(as_text=True)
        latott = 0
        for b in ('szo.bdb_apparatus', 'szo.bdb_magyar', 'szo.bdb_angol'):
            if 'data-blokk="%s"' % b not in t:
                continue
            latott += 1
            i = t.index('data-blokk="%s"' % b)
            blokk = t[i:t.index('</section>', i)]
            self.assertIn('<abbr class="rovidites" title="יְהוָה (Jahve), az Úr" tabindex="0">י׳</abbr>', blokk, b)
            if b != 'szo.bdb_angol':
                self.assertIn('<abbr class="rovidites" title="a címszó: קָרָא (kárá)" tabindex="0">ק׳</abbr>', blokk, b)
            szoveg = re.sub(r'<[^>]*>', ' ', blokk)
            self.assertIsNone(blokkok.bdb_rovidites.ROVIDITES_RE.search(szoveg), b)
        self.assertGreaterEqual(latott, 2)
        css = open(os.path.join(D, 'statikus', 'olvaso.css'), encoding='utf-8').read()
        self.assertRegex(css, r'abbr\.rovidites \{[^}]*background: var\(--gold-soft\)')
        self.assertRegex(css, r'abbr\.rovidites:focus::after \{[^}]*content: attr\(title\)')

    def test_bdb_rovidites_escape(self):
        """A jelölő a kész, escape-elt HTML szövegrészein dolgozik: a címkéhez (attribútum) nem nyúl, a cím escape-elve kerül be."""
        class K:
            def memo(self, kulcs, f):
                return '<i>"x"</i>', 'ק'
        h = blokkok._rovidites(K(), blokkok.Markup('<p title="׳י">a ׳ק &lt;b&gt;</p>'))
        self.assertEqual(str(h), '<p title="׳י">a <abbr class="rovidites" title="a címszó: &lt;i&gt;&#34;x&#34;&lt;/i&gt;" '
                                 'tabindex="0">ק׳</abbr> &lt;b&gt;</p>')
        # hivatkozáson belül nincs tabindex (a koppintás a hivatkozásé), utána újra van
        h = str(blokkok._rovidites(K(), blokkok.Markup('<a href="#x"><span>׳ק</span></a> ׳ק')))
        self.assertEqual(h.count('tabindex'), 1)
        self.assertTrue(h.startswith('<a href="#x"><span><abbr class="rovidites" title="a címszó: &lt;i&gt;&#34;x&#34;&lt;/i&gt;">ק׳</abbr>'))

    def test_bdb_proba_es_mert_pontossag(self):
        """DT-F99l (c): a BDB-blokk „próba” jelölése mellett a nyers mért pontosság és a konfidencia-intervallum áll (F99, seed-101)."""
        t = self.get('/r/szo/H7451').get_data(as_text=True)
        self.assertIn('Gépi szeletelés (próba)', t)
        self.assertIn('92,0%', t)
        self.assertIn('87,3–95,4%', t)
        self.assertNotIn('93,5%', t)          # az ítélet utáni érték csak a naplóban

    def test_bdb_jelentes_cime_es_vazlata(self):
        """A főjelentés címe a szócikk saját szavaiból képződik (gépi): saját szöveg híján az első alpontéból (H0776 אֶרֶץ: 1 „föld”,
        3 „talaj”); a blokk elején vázlat áll, amelynek minden sora egy létező jelentés-azonosítóra ugrik."""
        t = self.get('/r/szo/H0776').get_data(as_text=True)
        i = t.index('data-blokk="szo.bdb_apparatus"')
        blokk = t[i:t.index('</section>', i)]
        # az 1. és a 3. főjelentésnek nincs saját meghatározása: a cím az a. alpontból kölcsönzött, és ezt a megjelenés jelzi
        self.assertEqual(re.findall(r'<span class="jcim">(?:<span class="kolcsonzott"[^>]*>)?([^<]*)', blokk)[:3], ['föld', 'ország', 'talaj'])
        self.assertEqual(re.findall(r'<span class="jcim">(<span class="kolcsonzott")?', blokk)[:3], ['<span class="kolcsonzott"', '', '<span class="kolcsonzott"'])
        self.assertIn('title="A BDB-ben ennek a jelentésnek nincs saját meghatározása; a cím az a. alpontból képződik (gépi)."', blokk)
        # a szám a kiírt igehely-hivatkozásoké, nem az előfordulásoké: a felirat és a súgó ezt mondja
        self.assertRegex(blokk, r'<span class="helyek" title="a BDB ennél a jelentésnél[^"]*">60 hivatkozás</span>')
        self.assertNotRegex(blokk, r'\d hely</span>')
        self.assertIn('class="jel-vazlat"', blokk)
        vz = blokk[blokk.index('class="jel-vazlat"'):blokk.index('</nav>')]
        celok = re.findall(r'href="#([^"]+)"', vz)
        self.assertEqual(len(celok), 5 + 3 + 7 + 2 + 5)          # 5 főjelentés, a 4 alpontos csoport a., b. … alpontjai
        idk = set(re.findall(r' id="([^"]+)"', blokk))
        self.assertEqual([c for c in celok if c not in idk], [])
        self.assertEqual(len(idk), len(re.findall(r' id="', blokk)), 'ismétlődő azonosító')
        jc = blokkok.jelentes_cim
        self.assertEqual(jc('föld, az egész föld (egy részével szemben) 1Móz 18:18, 25'), 'föld, az egész föld')
        self.assertEqual(jc('föld, az egész föld (egy részével szemben) 1Móz 18:18', vesszoig=True), 'föld')
        self.assertEqual(jc('', vesszoig=True), '')
        self.assertEqual(jc('ország =', vesszoig=True), 'ország')
        self.assertEqual(jc('gyakran (fent és máshol) elöljáróval (+ névelő); reggel'), 'gyakran elöljáróval')
        # saját szövegű főjelentés: a vessző nem határ (H7451 רַע: a megkülönböztető rész a vessző után áll)
        self.assertEqual(jc('rossz, kellemetlen, ártalmas: asszonyról, בְּעֵינֵי רָעָה 2Móz 21:8', max_hossz=70), 'rossz, kellemetlen, ártalmas')
        self.assertEqual(jc('rossz, nem tetsző פְלשְׁתִּים סַרְנֵי בְּעֵינֵי 1Sám 29:7.', max_hossz=70), 'rossz, nem tetsző')
        self.assertEqual(jc('הַמִּישׁוֺר אֶרֶץ a síkság földje 5Móz 4:33'), 'הַמִּישׁוֺר אֶרֶץ a síkság földje')
        self.assertEqual(jc('+ מִן comparativus: rosszabb, mint, 2Sám 19:8; felsőfokként', max_hossz=70), '+ מִן comparativus: rosszabb, mint')
        self.assertEqual(jc('מַחֲשֶׁבֶת(ה)רָעָה חָשַׁב gonosz (ártalmas) tervet kigondolni Ez 38:10', max_hossz=70),
                         'מַחֲשֶׁבֶת(ה)רָעָה חָשַׁב gonosz tervet kigondolni')
        # a vezető héber a magyar mögé kerül, minden héber futam lang="he"-vel
        self.assertEqual(str(blokkok._cim_html('מַחֲשֶׁבֶת(ה)רָעָה חָשַׁב gonosz tervet kigondolni')),
                         'gonosz tervet kigondolni <span class="he" lang="he">מַחֲשֶׁבֶת(ה)רָעָה חָשַׁב</span>')
        self.assertEqual(str(blokkok._cim_html('+ מִן comparativus: rosszabb, mint')),
                         '+ <span class="he" lang="he">מִן</span> comparativus: rosszabb, mint')
        self.assertEqual(str(blokkok._cim_html('a <b>')), 'a &lt;b&gt;')
        t = self.get('/r/szo/H7451').get_data(as_text=True)
        cimek = re.findall(r'<span class="jcim">([^<]*)</span>', t)
        # F99 M2: a szeletelő a II. רַע (főnév) és a רָעָה szakaszt külön választja; a lap ezeket a fő szerkezet előtt mutatja, ezért a fő
        # szerkezet első három címét a saját helyén keressük
        self.assertIn('rossz, kellemetlen, ártalmas', cimek)
        i = cimek.index('rossz, kellemetlen, ártalmas')
        self.assertEqual(cimek[i:i + 3], ['rossz, kellemetlen, ártalmas', 'rossz, kellemetlen, fájdalmat, boldogtalanságot, nyomorúságot okozó',
                                     'rossz, nem tetsző'])

    def test_kod_verzio_valtozik_a_fajl_valtozasaval(self):
        import shutil
        tmp = tempfile.mkdtemp(prefix='kodverzio_')
        try:
            for n, t in (('a.py', 'x = 1\n'), ('b.html', '<p>b</p>'), ('c.css', 'a{}'), ('teszt_x.py', 'nem szamit')):
                with open(os.path.join(tmp, n), 'w', encoding='utf-8', newline='') as f:
                    f.write(t)
            gy = [(tmp, ('.py', '.html', '.css', '.js', '.toml'))]
            v1 = oldalak.kod_verzio(gy)
            self.assertEqual(v1, oldalak.kod_verzio(gy))                 # determinisztikus
            with open(os.path.join(tmp, 'teszt_x.py'), 'w', encoding='utf-8') as f:
                f.write('mas')
            self.assertEqual(v1, oldalak.kod_verzio(gy))                 # a teszt_*.py nem számít
            for n in ('a.py', 'b.html', 'c.css'):
                with open(os.path.join(tmp, n), 'a', encoding='utf-8') as f:
                    f.write(' ')
                v2 = oldalak.kod_verzio(gy)
                self.assertNotEqual(v1, v2, n)
                v1 = v2
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(len(oldalak.kod_verzio()), 16)                  # az alap: a szerver és a pilot bdb_szelet.py

    def test_szo_toredek_vers_kontextussal(self):
        h = self.get('/r/szo/H6440?ig=1Moz/1/2').get_data(as_text=True)
        self.assertIn('data-blokk="szo.ebben"', h)
        self.assertNotIn('data-blokk="szo.ebben"', self.get('/r/szo/H6440?ig=nincs/1/2').get_data(as_text=True))
        self.assertNotIn('data-blokk="szo.ebben"', self.get('/r/szo/H6440?ig=1Moz/1/2;drop').get_data(as_text=True))     # csak szigorú alak

    def test_biztonsagi_fejlecek(self):
        r = self.get('/')
        self.assertIn("script-src 'self'", r.headers['Content-Security-Policy'])
        self.assertNotIn("'unsafe-inline'", r.headers['Content-Security-Policy'])
        self.assertEqual(r.headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(self.get('/robots.txt').get_data(as_text=True), 'User-agent: *\nDisallow: /\n')

    def test_ugras(self):
        r = self.get('/ugras?q=1Móz 1:4')
        self.assertEqual((r.status_code, r.headers['Location']), (302, '/1Moz/1/4'))
        self.assertEqual(self.get('/ugras?q=Zsolt 22').headers['Location'], '/Zsolt/22')
        self.assertEqual(self.get('/ugras?q=h216').headers['Location'], '/szo/H0216')
        self.assertEqual(self.get('/ugras?konyv=1Moz&fej=2&vers=3').headers['Location'], '/1Moz/2/3')
        self.assertEqual(self.get('/ugras?q=valami ismeretlen').status_code, 404)
        self.assertEqual(self.get('/ugras').status_code, 404)

    def test_interlinearis_pozicio_szerinti_illesztes(self):
        """1Móz 1:4: az „Isten” kétszer áll (3. és 10. szó), mindkettő H0430, de más eredeti szóalakkal (ékezet-jelek);
        a pozíció szerinti illesztés a saját párját adja, a „világosságot” (12.) két eredeti szót kap (H0996 + H0216)."""
        con = self.app.extensions['pardes']['db'].kapcsolat()
        szavak = q.fejezet_szavak(con, '1Móz', 1)['1Móz 1:4']
        d = {sz: (szo, parok) for sz, szo, parok in szavak}
        self.assertEqual(d[3][0], 'Isten')
        self.assertEqual(d[10][0], 'Isten')
        self.assertEqual([p[2] for p in d[3][1]], ['H0430'])
        self.assertEqual([p[2] for p in d[10][1]], ['H0430'])
        self.assertNotEqual(d[3][1][0][1], d[10][1][0][1])                 # eltérő eredeti szóalak
        self.assertEqual(d[3][1][0][0], 3)                                  # er_sorszam = 3
        self.assertEqual(d[10][1][0][0], 11)                                # er_sorszam = 11 (nem 3, ahogy Strong szerinti illesztés adná)
        self.assertEqual(sorted(p[2] for p in d[12][1]), ['H0216', 'H0996'])
        h = self.get('/1Moz/1/4?nezet=interlinearis').get_data(as_text=True)
        self.assertIn('il-szo', h)
        self.assertIn('אֱלֹהִ֛ים', h)
        self.assertIn('אֱלֹהִ֔ים', h)

    def test_interlinearis_parositatlan_sor_es_nt(self):
        h = self.get('/1Moz/1/4?nezet=interlinearis').get_data(as_text=True)
        self.assertIn('Párosítatlan eredeti szavak', h)       # pl. az אֶת (H0853)
        h = self.get('/Mt/1/1?nezet=interlinearis').get_data(as_text=True)
        self.assertIn('nincs Károli–Strong párosítás', h)        # ÚSZ: nincs token_par: explicit üres, nem néma

    def _rokon(self, strong):
        h = self.get('/r/szo/' + strong).get_data(as_text=True)
        i = h.index('data-blokk="szo.oshl_csalad"')
        return h[i:h.index('</section>', i)]

    def test_rokon_szavak_oshl_gyokcsalad(self):
        """F99 M1: a gyök és a származékok Strong-linkkel (H1242 בֹּקֶר: gyök H1239, család H0951, H1241, H1243, H1244); az OSHL szerint
        családon kívüli szónál (H3915 לַיְלָה, single) kifejezett „nincs” felirat; a Strong nélküli gyök-bejegyzés (H7307: רוח) jelölve."""
        con = adatbazis.Adatbazis(DB, 'belso').kapcsolat()
        van_oszlop = 'etym_tipus' in {r[1] for r in con.execute('PRAGMA table_info(oshl_lexikalis_index)')}
        con.close()
        if not van_oszlop:
            self.skipTest('a pardes.db még a gyökcsalád-oszlopok nélkül épült (újraépítés kell)')
        b = self._rokon('H1242')
        self.assertIn('href="/szo/H1239"', b)
        for s in ('H0951', 'H1241', 'H1243', 'H1244'):
            self.assertIn('href="/szo/%s"' % s, b)
        self.assertIn('Nincs OSHL-gyökcsalád', self._rokon('H3915'))
        self.assertIn('single', self._rokon('H3915'))
        b = self._rokon('H7307')
        self.assertIn('Strong-szám nélküli gyök-bejegyzés', b)
        self.assertIn('href="/szo/H7306"', b)


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestNezetSuti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_keszit('belso')

    def setUp(self):
        self.c = self.app.test_client()

    def test_nezetvaltas_sutit_hoz_letre(self):
        r = self.c.get('/nezet/interlinearis?vissza=/1Moz/1')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers['Location'], '/1Moz/1')
        sc = r.headers['Set-Cookie']
        self.assertTrue(sc.startswith('pardes_nezet=interlinearis'))
        self.assertIn('SameSite=Lax', sc)
        self.assertIn('HttpOnly', sc)
        self.assertIn('Max-Age=31536000', sc)
        self.assertIn('Path=/', sc)
        # a következő kérés a megjegyzett nézetet kapja
        h = self.c.get('/1Moz/1').get_data(as_text=True)
        self.assertIn('class="nezet-interlinearis"', h)

    def test_suti_csak_nezetvaltaskor_jon_letre(self):
        for u in ('/', '/1Moz', '/1Moz/1', '/1Moz/1/4', '/szo/H0216', '/statusz', '/ugras?q=H0216', '/1Moz/1?nezet=munkaasztal', '/nincs', '/r/szo/H0216'):
            r = self.c.get(u)
            self.assertNotIn('Set-Cookie', r.headers, u)

    def test_nezet_parameter_felulirja_a_sutit(self):
        self.c.get('/nezet/munkaasztal')
        h = self.c.get('/1Moz/1?nezet=interlinearis').get_data(as_text=True)
        self.assertIn('class="nezet-interlinearis"', h)
        r = self.c.get('/1Moz/1?nezet=interlinearis')
        self.assertNotIn('Set-Cookie', r.headers)

    def test_ismeretlen_ertek_az_alapra_esik(self):
        self.c.set_cookie('pardes_nezet', 'valami<script>')
        h = self.c.get('/1Moz/1').get_data(as_text=True)
        self.assertIn('class="nezet-olvaso"', h)
        self.assertNotIn('<script>', h.replace('<script src', ''))
        h = self.c.get('/1Moz/1?nezet=%3Cscript%3E').get_data(as_text=True)
        self.assertIn('class="nezet-olvaso"', h)

    def test_vissza_whitelist(self):
        for rossz in ('//evil.com/x', 'http://evil.com', 'https://evil.com', '/\\evil.com'):
            r = self.c.get('/nezet/olvaso', query_string={'vissza': rossz})
            self.assertEqual(r.headers['Location'], '/', rossz)

    def test_nezetvalto_hivatkozasok(self):
        h = self.c.get('/1Moz/1').get_data(as_text=True)
        for n in oldalak.NEZETEK:
            self.assertIn('href="/nezet/%s?vissza=' % n, h)


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestKiadasKapcsolo(unittest.TestCase):
    def _jar(self, kiadas):
        app = app_keszit(kiadas)
        c = app.test_client()
        html = {}
        for u in ('/r/vers/1Moz/1/4', '/r/vers/Zsolt/22/1', '/r/szo/G0746', '/r/szo/G3056', '/r/szo/H0216', '/1Moz/1/4', '/Mt/1/1', '/szo/G1504'):
            r = c.get(u)
            self.assertEqual(r.status_code, 200, (kiadas, u))
            html[u] = r.get_data(as_text=True)
        return app, html

    def test_belso_minden_blokk(self):
        app, h = self._jar('belso')
        self.assertIn('data-blokk="vers.kjv"', h['/r/vers/1Moz/1/4'])
        self.assertIn('data-blokk="szo.mcged"', h['/r/szo/G0746'])
        self.assertEqual(app.extensions['pardes']['db'].kiserletek, [])

    def test_nyilvanos_nincs_kjv(self):
        app, h = self._jar('nyilvanos')
        for u in ('/r/vers/1Moz/1/4', '/r/vers/Zsolt/22/1', '/1Moz/1/4'):
            self.assertNotIn('vers.kjv', h[u])
            self.assertIn('data-blokk="vers.bsb"', h['/r/vers/1Moz/1/4'])
        self.assertIn('data-blokk="szo.mcged"', h['/r/szo/G0746'])       # nyilvános kiadásban az MCGED marad
        self.assertEqual(app.extensions['pardes']['db'].kiserletek, [])   # nem volt olvasási kísérlet a tiltott táblára

    def test_kereskedelmi_nincs_kjv_es_mcged(self):
        app, h = self._jar('kereskedelmi')
        for u, t in h.items():
            self.assertNotIn('vers.kjv', t, u)
            self.assertNotIn('szo.mcged', t, u)
            self.assertNotIn('Mounce', t, u)
            self.assertNotIn('KJV_Strongs_teljes', t, u)
        self.assertEqual(app.extensions['pardes']['db'].kiserletek, [])
        self.assertIn('data-blokk="szo.tbesg"', h['/r/szo/G0746'])

    def test_kiadas_a_labjegyzetben_es_statuszban(self):
        app, h = self._jar('nyilvanos')
        self.assertIn('Kiadás: <b>nyilvanos</b>', h['/1Moz/1/4'])
        self.assertEqual(app.test_client().get('/statusz').get_json()['kiadas'], 'nyilvanos')

    def test_nyilvanos_cache_fejlec(self):
        app = app_keszit('nyilvanos')
        self.assertEqual(app.test_client().get('/1Moz/1').headers['Cache-Control'], 'public, max-age=300')

    def test_ismeretlen_kiadas_megallit(self):
        with self.assertRaises(ValueError):
            adatbazis.Adatbazis(DB, 'titkos')

    def test_authorizer_veszi_el_a_blokkot_nem_csak_a_megjelenites(self):
        """A kizárt blokk lekérdezése az authorizer miatt hibával áll meg: ha a regiszter-szűrés elromlana, nem szivárog."""
        db = adatbazis.Adatbazis(DB, 'nyilvanos')
        con = db.kapcsolat()
        K = oldalak.Kontekst(con, oldalak.Kozos(con), ig='1Móz 1:4')
        with self.assertRaises(sqlite3.DatabaseError):
            blokkok.BLOKK_ID['vers.kjv'].fetch(K)
        self.assertEqual(db.kiserletek, ['kjv'])


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestHozzaferesiSzintek(unittest.TestCase):
    def test_a_magasabb_szintu_blokk_nem_kerul_a_lapra_es_nem_fut(self):
        import unittest.mock as mock
        h = hozzaferes.Hozzaferes(['nyilvanos', 'kutato'], 'nyilvanos', {'vers.tsk': 'kutato', 'szo.bdb_magyar': 'kutato'}, 'nyilvanos')
        app = app_keszit('belso', hozz=h)
        c = app.test_client()
        with mock.patch.object(q, 'tsk', side_effect=AssertionError('a tiltott blokk lekérdezése lefutott')):
            t = c.get('/r/vers/1Moz/1/4').get_data(as_text=True)
        self.assertNotIn('vers.tsk', t)
        self.assertIn('data-blokk="vers.kh"', t)
        s = c.get('/r/szo/H0216').get_data(as_text=True)
        self.assertNotIn('szo.bdb_magyar', s)
        self.assertIn('data-blokk="szo.bdb_angol"', s)

    def test_alapjelentes_es_szamlalo_a_blokk_szuresen_at(self):
        """F76.32 (E1): a szó-lap fejlécének magyar alapjelentése és a „BDB magyarul” számláló is a blokk-szűrésen megy át: tiltott szintnél vagy
        kizárt `forditasok` táblánál az angol Strong-glosszára esik vissza (és a számláló elmarad), nem szivárog és nem ad 500-at."""
        import unittest.mock as mock
        # (1) hozzáférési szint: a szo.bdb_magyar nem látható
        h = hozzaferes.Hozzaferes(['nyilvanos', 'kutato'], 'nyilvanos', {'szo.bdb_magyar': 'kutato'}, 'nyilvanos')
        c = app_keszit('belso', hozz=h).test_client()
        r = c.get('/r/szo/H6440')
        self.assertEqual(r.status_code, 200)
        t = r.get_data(as_text=True)
        self.assertNotIn('arc, arcok is', t)                      # a magyar alapjelentés nem szivárog
        self.assertRegex(t, r'<p class="alapjel" lang="en"[^>]*><span class="fcim">Alapjelentés</span> face')
        self.assertNotIn('data-blokk="szo.bdb_apparatus"', t)
        ch = c.get('/1Moz/1')
        self.assertEqual(ch.status_code, 200)
        self.assertNotIn('BDB magyarul', ch.get_data(as_text=True))
        # (2) kiadás: a forditasok tábla kizárt (az authorizer olvasni sem engedi): nincs 500
        with mock.patch.dict(adatbazis.TABLA_KIZARAS, {'forditasok': ('nyilvanos',)}):
            c2 = app_keszit('nyilvanos').test_client()
            r2 = c2.get('/r/szo/H6440')
            self.assertEqual(r2.status_code, 200)
            t2 = r2.get_data(as_text=True)
            self.assertNotIn('arc, arcok is', t2)
            self.assertIn('face', t2)
            ch2 = c2.get('/1Moz/1')
            self.assertEqual(ch2.status_code, 200)
            self.assertNotIn('BDB magyarul', ch2.get_data(as_text=True))
            self.assertEqual(c2.get('/1Moz/1/2?szo=H6440&ful=szo').status_code, 200)
        # (3) alap konfig: a magyar alapjelentés és a számláló megvan
        t3 = app_keszit('belso').test_client().get('/r/szo/H6440').get_data(as_text=True)
        self.assertIn('arc, arcok is', t3)

    def test_kod_verzio_a_kulso_konfigot_is_tartalmazza(self):
        import shutil
        import unittest.mock as mock
        tmp = tempfile.mkdtemp(prefix='konfig_')
        try:
            with open(os.path.join(tmp, 'hozzaferes.toml'), 'w', encoding='utf-8') as f:
                f.write('a = 1\n')
            with mock.patch.dict(os.environ, {'PARDES_KONFIG_DIR': tmp}):
                v1 = oldalak.kod_verzio()
                with open(os.path.join(tmp, 'hozzaferes.toml'), 'a', encoding='utf-8') as f:
                    f.write('b = 2\n')
                self.assertNotEqual(v1, oldalak.kod_verzio())
            self.assertNotEqual(v1, oldalak.kod_verzio())              # a külső konfig nélkül más
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_a_szint_a_gyorsitotar_kulcsaban_van(self):
        h1 = hozzaferes.Hozzaferes(['nyilvanos', 'kutato'], 'nyilvanos', {'vers.tsk': 'kutato'}, 'nyilvanos')
        h2 = hozzaferes.Hozzaferes(['nyilvanos', 'kutato'], 'kutato', {'vers.tsk': 'kutato'}, 'nyilvanos')
        a1, a2 = app_keszit('belso', hozz=h1), app_keszit('belso', hozz=h2)
        self.assertNotIn('vers.tsk', a1.test_client().get('/r/vers/1Moz/1/4').get_data(as_text=True))
        self.assertIn('vers.tsk', a2.test_client().get('/r/vers/1Moz/1/4').get_data(as_text=True))

    def test_alap_konfig_mindent_lat(self):
        app = app_keszit('belso')
        t = app.test_client().get('/r/vers/1Moz/1/4').get_data(as_text=True)
        self.assertEqual(len(re.findall(r'data-blokk=', t)), len(blokkok.blokkok_oldalra('vers')))


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestInjekcioEsXSS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_keszit('belso')

    def setUp(self):
        self.c = self.app.test_client()

    def test_utvonal_injekcio(self):
        for u in ("/szo/H0216'%20OR%20'1'='1", "/szo/H0216;DROP%20TABLE%20vers", "/1Moz'%20OR%201=1--/1", "/1Moz/1/4'", "/r/szo/H0216'--",
                  "/szo/%3Cscript%3Ealert(1)%3C%2Fscript%3E", "/%3Cscript%3E"):
            r = self.c.get(u)
            self.assertIn(r.status_code, (404, 400), u)
            self.assertNotIn('<script>alert', r.get_data(as_text=True), u)

    def test_parameter_injekcio_es_xss(self):
        for u in ("/1Moz/1/4?szo=H0216'%20OR%201=1", '/1Moz/1/4?szo=<script>alert(1)</script>', '/1Moz/1/4?ful="><script>x</script>',
                  '/1Moz/1/4?nezet=<img src=x onerror=alert(1)>', '/ugras?q=<script>alert(1)</script>', "/ugras?q=' OR '1'='1", '/ugras?konyv=<b>&fej=1'):
            r = self.c.get(u)
            self.assertIn(r.status_code, (200, 302, 404), u)
            t = r.get_data(as_text=True)
            self.assertNotIn('<script>alert', t, u)
            self.assertNotIn('<script>x', t, u)
            self.assertNotIn('<img src=x', t, u)
        self.assertEqual(self.c.get('/1Moz/1/4?szo=H0216%27%20OR%201=1').status_code, 200)      # érvénytelen szo: figyelmen kívül marad
        self.assertEqual(self.app.extensions['pardes']['db'].kapcsolat().execute('SELECT COUNT(*) FROM vers').fetchone()[0], 31158)

    def test_adatbol_jovo_szoveg_escape_elve(self):
        """Szintetikus `<script>` érték a forrásadatban: minden blokk escape-eli."""
        import unittest.mock as mock
        rossz = '<script>alert("xss")</script> & <b>'
        with mock.patch.object(q, 'bdb_angol', return_value=rossz), mock.patch.object(q, 'bdb_magyar', return_value=rossz), \
                mock.patch.object(q, 'sece_h', return_value=rossz), mock.patch.object(q, 'tbesh', return_value=[(rossz, rossz, rossz, rossz, rossz)]), \
                mock.patch.object(q, 'tw', return_value=[('tw1', rossz, rossz, rossz)]):
            r = self.c.get('/szo/H0216')
        t = r.get_data(as_text=True)
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('<script>alert', t)
        self.assertIn('&lt;script&gt;alert(&#34;xss&#34;)&lt;/script&gt;', t)
        with mock.patch.object(q, 'karoli_szoveg', return_value=rossz), mock.patch.object(q, 'nave', return_value=[(rossz, rossz, rossz, True, 1)]), \
                mock.patch.object(q, 'tipnr', return_value=[(rossz, rossz, 'H0001', rossz)]), mock.patch.object(q, 'tsk', return_value=[(rossz, 3)]):
            t = self.c.get('/r/vers/1Moz/1/4').get_data(as_text=True)
        self.assertNotIn('<script>alert', t)
        self.assertIn('&lt;script&gt;', t)

    def test_ismert_hibas_tw_cikk_escape_elve(self):
        """A `tW_szocikkek.tsv` ismert U+FFFD tartalmú cikke hibátlanul, escape-elve jelenik meg."""
        con = self.app.extensions['pardes']['db'].kapcsolat()
        sor = con.execute("SELECT strong, tw_id FROM tw_szocikkek WHERE instr(szoveg, char(65533)) > 0 LIMIT 1").fetchone()
        if not sor:
            self.skipTest('nincs U+FFFD tartalmú tW-cikk')
        s = sor[0].split('+')[0]
        r = self.c.get('/szo/' + s)
        self.assertEqual(r.status_code, 200)
        self.assertIn(sor[1], r.get_data(as_text=True))


@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class TestExportVaz(unittest.TestCase):
    def test_oldalak_szerver_nelkul(self):
        """Az `oldalak.py` a Flask nélkül is előállítja a lapot; az export váza egy könyv fejezeteit kiírja."""
        import export
        hozz = hozzaferes.Hozzaferes.betolt(KONFIG)
        gyar = oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), hozz)
        with tempfile.TemporaryDirectory() as tmp:
            n = export.kiir(gyar, tmp, 'Ruth', hozz.szint())
            self.assertEqual(n, 4)
            with open(os.path.join(tmp, 'Ruth', '1.html'), encoding='utf-8') as f:
                self.assertIn('Ruth', f.read())

    def test_oldalak_nem_importal_flaskot(self):
        with open(os.path.join(D, 'oldalak.py'), encoding='utf-8') as f:
            self.assertNotRegex(f.read(), r'(?m)^\s*(?:import|from)\s+flask')


# =====================================================================================================================
# D2: egyezés a #60 pilot JSON-jával (TSV-ből készült `adat.py` kimenet) mindkét pilot-szakaszon
# =====================================================================================================================
def _pilot_json(szakasz, azon):
    import json
    kdir = os.environ.get('PARDES_PILOT_JSON')
    if kdir and os.path.exists(os.path.join(kdir, azon, 'olvaso_pilot.json')):
        with open(os.path.join(kdir, azon, 'olvaso_pilot.json'), encoding='utf-8') as f:
            return json.load(f)
    tmp = tempfile.mkdtemp(prefix='pilot_d2_')
    subprocess.run([sys.executable, GY + 'eszkozok/olvaso_pilot/adat.py', '--szakasz', szakasz, '--kimenet', tmp], check=True, capture_output=True)
    with open(os.path.join(tmp, 'olvaso_pilot.json'), encoding='utf-8') as f:
        return json.load(f)


@unittest.skipUnless(VAN_DB and VAN_FLASK and os.path.exists(GY + 'konkordancia/Karoli_1908.tsv'), 'nincs pardes.db, Flask vagy konkordancia/ (a pilot TSV-ből épül)')
class TestD2PilotEgyezes(unittest.TestCase):
    """A szerver saját lekérdezései (`lekerdezesek.py`, `blokkok.py`) a #60 D2 összehasonlítójával (db_meres.py):
    ugyanaz a vers- és szó-adat, mint a TSV-ből készült pilot JSON. Az eltérések darabszáma blokkonként egyezik a
    `db_meres.py` saját (db_vers/db_szo/db_gorog) mérésével; ahol az eltérés dokumentált ok, az ok is egyezik."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, GY + 'eszkozok/olvaso_pilot')
        import db_meres
        cls.dm = db_meres
        cls.db = adatbazis.Adatbazis(DB, 'belso')
        cls.con = cls.db.kapcsolat()
        cls.kozos = oldalak.Kozos(cls.con)

    # a szerver lekérdezéseiből a db_meres.db_vers / db_szo / db_gorog alakú szótárak
    def szerver_vers(self, ig):
        con = self.con
        K = oldalak.Kontekst(con, self.kozos, ig=ig)
        heber = q.heber_d2(con, ig)
        lxx, extra, _ = q.lxx_versszam(con, ig)
        return {'karoli': q.karoli_szoveg(con, ig), 'par': q.par(con, ig), 'heber': heber, 'tsk': q.tsk(con, ig), 'kh_db': q.kh_darab(con, ig),
                'versszam': q.versszamozas(con, ig), 'lxx': lxx, 'lxx_extra': extra, 'ubs': q.ubs_d2(con, ig, {h[0] for h in heber}),
                'macula': K.memo('macula', lambda: q.macula(con, ig)), 'lxx_szavak': q.lxx_szavak(con, ig),
                'lxx_formak': [], 'nave': q.nave(con, ig)}

    def szerver_szo(self, s):
        con = self.con
        K = oldalak.Kontekst(con, self.kozos, strong=s)
        b = blokkok._bdb_adat(K)
        sz = q.strong_szotar(con, s)
        ossz, magas, top = q.karoli_alakok(con, s)
        db, kony = q.elofordulas(con, s)
        return {'szotar': tuple(sz[:4]) if sz else None, 'bdb_en': b['en'] or '', 'bdb_hu': b['hu'], 'alias': b['alias'], 'elofordulas': db, 'konyvek': kony,
                'karoli_osszes': ossz, 'karoli_magas': magas, 'karoli_top8': top, 'bridge': q.lxx_bridge_h(con, s)[:3], 'gramm': bool(q.nyelvtani(con, s))}

    def szerver_gorog(self, g):
        con = self.con
        tb = q.tbesg(con, g)
        db, vdb, _ = q.usz(con, g)
        return {'tbesg': tb[3] if tb else '', 'tbesg_alak': tb[:3] if tb else None, 'thayer': q.thayer(con, g) or '', 'hu_db': len(q.magyar_gorog(con, g)),
                'usz_db': db, 'usz_versek_db': vdb, 'heber': q.lxx_bridge_g(con, g)[:5]}

    def _szakasz(self, szakasz, azon):
        dm = self.dm
        adat = _pilot_json(szakasz, azon)
        ossz = {}

        def felvesz(csoport, ki):
            for blokk, (eg, tv, dv, ok) in ki.items():
                k = '%s:%s' % (csoport, blokk)
                a = ossz.setdefault(k, [0, 0, 0])
                a[0] += 1
                if not eg:
                    a[1] += 1
                    # az egyetlen engedett eltérés: usz_elofordulas, dokumentált „+” Strong-lánc okkal (DT-F76d: elfogadva, a token_strong a helyes
                    # számlálás; DT133 külön, nyitott); minden más bukik
                    self.assertEqual(k, 'gorog_szo:usz_elofordulas', 'váratlan eltérés: %s (%s)' % (k, ok))
                    self.assertIn('a pilot TSV-útja a „+” Strong-láncok elemeit nem számolja', ok, 'az eltérésnek nincs/más az oka: %s %r' % (k, ok))
                    self.assertIn('DB-szám = TSV-szám + láncelem', ok)

        for v in adat['versek']:
            sz = self.szerver_vers(v['igehely'])
            ki_sz = dm.hasonlit_vers(self.con, v, db=sz)
            ki_dm = dm.hasonlit_vers(self.con, v)
            self.assertEqual({k: x[0] for k, x in ki_sz.items()}, {k: x[0] for k, x in ki_dm.items()}, v['igehely'])
            felvesz('vers', ki_sz)
        for l in adat['lapok'].values():
            ki_sz = dm.hasonlit_szo(self.con, l, db=self.szerver_szo(l['strong']))
            ki_dm = dm.hasonlit_szo(self.con, l)
            self.assertEqual({k: x[0] for k, x in ki_sz.items()}, {k: x[0] for k, x in ki_dm.items()}, l['strong'])
            felvesz('heber_szo', ki_sz)
        for g in adat['gor_lapok'].values():
            ki_sz = dm.hasonlit_gorog(self.con, g, db=self.szerver_gorog(g['strong']))
            ki_dm = dm.hasonlit_gorog(self.con, g)
            self.assertEqual({k: x[0] for k, x in ki_sz.items()}, {k: x[0] for k, x in ki_dm.items()}, g['strong'])
            felvesz('gorog_szo', ki_sz)
        return ossz

    def _ellenoriz(self, ossz):
        eltero = {k: v[1] for k, v in ossz.items() if v[1]}
        vizsgalt = sum(v[0] for v in ossz.values())
        print('\nD2: %d összevetés, eltérő blokk-csoport: %s' % (vizsgalt, eltero or 'nincs'))
        self.assertGreater(vizsgalt, 100)
        # a szerver lekérdezései a db_meres.py D2-jével azonos eredményt adnak (az assertEqual a ciklusokban); a pilot
        # TSV-úttal való eltérés tételes listája (dokumentált okokkal) a jelentésben: itt csak azt őrizzük, hogy nincs
        # eltérés a vers-szintű blokkok fő adatán
        self.assertTrue(set(eltero) <= {'gorog_szo:usz_elofordulas'}, 'váratlan eltérés: %s' % eltero)   # a dokumentált ok: a „+” Strong-láncok
        for k in ('vers:karoli_szoveg', 'vers:karoli_strong_parositas', 'vers:heber_szavak', 'vers:tsk_darab', 'vers:versszamozas', 'vers:nave'):
            self.assertEqual(ossz.get(k, [0, 0])[1], 0, k)

    def test_1moz_1_25(self):
        self._ellenoriz(self._szakasz('1Móz 1-25', '1moz_1_25'))

    def test_zsolt_22(self):
        self._ellenoriz(self._szakasz('Zsolt 22', 'zsolt_22'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
