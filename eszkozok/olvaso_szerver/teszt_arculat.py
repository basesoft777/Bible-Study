"""Az arculati token-fájl és a token-blokk tesztjei (#98 M1): unittest.

Futtatás (Python 3.12 alatt, a `pardes` WSL-disztribúció venv-jével):
    PARDES_DB=/home/basesoft/pardes/pardes.db python eszkozok/olvaso_szerver/teszt_arculat.py
A token-fájl és a stíluslap tesztjei adatbázis és Flask nélkül is futnak; a lapokat és az `/arculat.css` útvonalat
kérő tesztek pardes.db és Flask nélkül kimaradnak (kifejezetten jelölve, nem zöldként).

A tesztek csak olvasnak; a repóba nem írnak (a módosított token-fájl ideiglenes könyvtárba kerül).
"""
import json
import os
import re
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

import arculat

try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

DB = os.environ.get('PARDES_DB') or (GY + 'pardes.db')
VAN_DB = os.path.exists(DB)
CSS = os.path.join(D, 'statikus', 'olvaso.css')
SZINEK = ('bg', 'panel', 'fg', 'muted', 'rule', 'accent', 'accent-soft', 'gold', 'gold-soft', 'low')


def css_szoveg():
    with open(CSS, encoding='utf-8') as f:
        return re.sub(r'/\*.*?\*/', '', f.read(), flags=re.S)


def alap_adat():
    with open(arculat.ALAP_UT, encoding='utf-8') as f:
        return json.load(f)


def arculat_adatbol(adat):
    return arculat.Arculat('<teszt>', json.dumps(adat, ensure_ascii=False, indent=2, sort_keys=True).encode('utf-8'))


# =====================================================================================================================
class TestTokenFajl(unittest.TestCase):
    """A token-fájl a mai értékekkel (naplok/TERVEZO_MOD_M0.md 3. szakasz, DT-F98a–c)."""

    def test_csoportok_es_tokenszamok(self):
        a = arculat.Arculat.betolt()
        self.assertEqual(sorted(a.adat['szin']), sorted(SZINEK))
        self.assertEqual(sorted(a.adat['betucsalad']), ['gr', 'he', 'mono', 'text', 'ui'])
        self.assertEqual(len(a.adat['betumeret']), 52)       # DT-F98a: szerep szerinti betűméret-tokenek
        self.assertEqual(len(a.adat['sorkoz']), 18)          # DT-F98c: a sorköz állítható
        self.assertEqual(len(a.adat['terkoz']), 35)          # DT-F98b: csak a regiszterben kitett térközök
        self.assertEqual(len(a.adat['lekerekites']), 6)

    def test_a_mai_ertekek(self):
        a = arculat.Arculat.betolt().adat
        self.assertEqual(a['szin']['bg'], {'light': '#f5f2ea', 'dark': '#151918'})
        self.assertEqual(a['szin']['accent'], {'light': '#1f5a49', 'dark': '#8cc4b1'})
        self.assertEqual((a['betumeret']['torzs'], a['sorkoz']['torzs']), ('15px', '1.6'))
        self.assertEqual((a['betumeret']['karoli-folyo'], a['sorkoz']['karoli-folyo']), ('1.25rem', '1.85'))
        self.assertEqual(a['betumeret']['versszam'], '0.6em')
        self.assertEqual(a['terkoz']['he-csempe-min'], '72px')
        self.assertEqual(a['lekerekites']['pill'], '999px')

    def test_a_fajl_rendezett_es_determinisztikus(self):
        """A mentés (M2) kis, olvasható git-diffet ad: rendezett kulcsok, 2 szóközös behúzás, záró újsor."""
        with open(arculat.ALAP_UT, 'rb') as f:
            nyers = f.read().replace(b'\r\n', b'\n')
        self.assertEqual(nyers.decode('utf-8'), json.dumps(alap_adat(), ensure_ascii=False, indent=2, sort_keys=True) + '\n')

    def test_hash_tartalomfuggo_es_sorveg_fuggetlen(self):
        self.assertEqual(arculat.tartalom_hash(b'a\nb\n'), arculat.tartalom_hash(b'a\r\nb\r\n'))
        self.assertNotEqual(arculat.tartalom_hash(b'a\nb\n'), arculat.tartalom_hash(b'a\nc\n'))
        self.assertEqual(len(arculat.Arculat.betolt().hash), 16)


class TestEllenorzes(unittest.TestCase):
    """Rossz token-fájl indulási hiba, a hibás kulcs megnevezésével (a stíluslapba szabad szöveg nem kerülhet)."""

    def hibas(self, modosit, minta):
        adat = alap_adat()
        modosit(adat)
        with self.assertRaises(arculat.ArculatHiba) as e:
            arculat_adatbol(adat)
        self.assertIn(minta, str(e.exception))

    def test_ervenyes_alap(self):
        arculat_adatbol(alap_adat())

    def test_ismeretlen_csoport(self):
        self.hibas(lambda a: a.update(arnyek={'x': '1px'}), 'arnyek')

    def test_verzio(self):
        self.hibas(lambda a: a.update(verzio=2), 'verzio')

    def test_rossz_szin(self):
        self.hibas(lambda a: a['szin']['bg'].update(light='red'), 'szin.bg.light')
        self.hibas(lambda a: a['szin']['bg'].update(dark='#12345'), 'szin.bg.dark')
        self.hibas(lambda a: a['szin']['bg'].pop('dark'), 'szin.bg')

    def test_elfogadott_szinalakok(self):
        for v in ('#abc', '#A1B2C3', 'rgb(10, 20, 30)', 'hsl(160, 49%, 24%)'):
            adat = alap_adat()
            adat['szin']['bg']['light'] = v
            arculat_adatbol(adat)

    def test_rossz_hossz_es_injekcio(self):
        self.hibas(lambda a: a['betumeret'].update(torzs='12pt'), 'betumeret.torzs')
        self.hibas(lambda a: a['terkoz'].update(oldal='1px;}body{display:none'), 'terkoz.oldal')
        self.hibas(lambda a: a['lekerekites'].update(pill='1rem'), 'lekerekites.pill')     # lekerekítés csak px
        self.hibas(lambda a: a['sorkoz'].update(torzs='1.6px'), 'sorkoz.torzs')            # sorköz mértékegység nélkül
        self.hibas(lambda a: a['betucsalad'].update(ui='x;} body { color: red'), 'betucsalad.ui')
        self.hibas(lambda a: a['betumeret'].update(Torzs='15px'), 'betumeret.Torzs')       # token-név: kisbetű, kötőjel

    def test_nem_json(self):
        with self.assertRaises(arculat.ArculatHiba):
            arculat.Arculat('<teszt>', b'{"verzio": 1,')

    def test_konfigbol(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(arculat.Arculat.konfigbol(tmp).ut, arculat.ALAP_UT)           # nincs a könyvtárban: az alap
            adat = alap_adat()
            adat['szin']['bg']['light'] = '#ffffff'
            with open(os.path.join(tmp, 'arculat.json'), 'w', encoding='utf-8') as f:
                json.dump(adat, f)
            a = arculat.Arculat.konfigbol(tmp)
            self.assertEqual(a.adat['szin']['bg']['light'], '#ffffff')
            self.assertIn('--bg: #ffffff;', a.css)


class TestStiluslapEsTokenBlokk(unittest.TestCase):
    """Egyetlen forrás: a stíluslap a token-értékeket nem ismétli, a token-blokk a token-fájlból generálódik (DT-F98e)."""

    def test_a_stiluslapban_nincs_token_definicio(self):
        css = css_szoveg()
        self.assertNotIn(':root', css)
        self.assertNotIn('data-tema', css)
        self.assertNotIn('prefers-color-scheme', css)
        self.assertIsNone(re.search(r'(?<![\w-])--[a-z0-9-]+\s*:', css), 'CSS-változó definíció az olvaso.css-ben')
        for hex_ in re.findall(r'#[0-9a-fA-F]{3,6}\b', css):
            self.fail('színérték az olvaso.css-ben: %s' % hex_)

    def test_minden_hivatkozott_valtozo_letezik_es_minden_token_hasznalt(self):
        hiv = set(re.findall(r'var\((--[a-z0-9-]+)\)', css_szoveg()))
        tok = arculat.Arculat.betolt().tokenek()
        self.assertEqual(sorted(hiv - tok), [], 'ismeretlen változó az olvaso.css-ben')
        self.assertEqual(sorted(tok - hiv), [], 'a token-fájl tokenje nincs használva az olvaso.css-ben')

    def test_meretek_csak_tokenbol_a_kiemelt_tulajdonsagokban(self):
        """A betűméret, a sorköz és a lekerekítés literál értéke nem maradhat a stíluslapban (a térközök közül csak a
        regiszterben kitettek tokenek, DT-F98b; azok a token-fájl `terkoz` csoportjában)."""
        css = css_szoveg()
        for prop, v in re.findall(r'(font-size|line-height|border-radius)\s*:\s*([^;}]+)', css):
            self.assertRegex(v.strip(), r'^(?:var\(--[a-z0-9-]+\)|0)(?:\s+(?:var\(--[a-z0-9-]+\)|0))*$', '%s: %s' % (prop, v))
        for v in re.findall(r'(?<![\w-])font\s*:\s*([^;}]+)', css):
            self.assertNotRegex(v, r'\d(?:px|rem|em)\b', 'font: %s' % v)

    def test_token_blokk_szerkezete(self):
        a = arculat.Arculat.betolt()
        b = a.css
        self.assertTrue(b.startswith('/* GENERÁLT: '))
        self.assertIn(':root {\n', b)
        self.assertIn('@media (prefers-color-scheme: dark) {\n  :root:not([data-tema="light"]) {', b)
        self.assertIn('\n:root[data-tema="dark"] {', b)
        self.assertEqual(b.count('color-scheme: dark;'), 2)
        gyoker = b[b.index(':root {'):b.index('}')]
        for n in SZINEK:
            self.assertIn('--%s: %s;' % (n, a.adat['szin'][n]['light']), gyoker)
            self.assertEqual(b.count('--%s: %s;' % (n, a.adat['szin'][n]['dark'])), 2, n)    # mindkét sötét blokkban
        self.assertIn('--fs-karoli-folyo: 1.25rem;', gyoker)
        self.assertIn('--lh-csempe: 1.3;', gyoker)
        self.assertIn('--space-he-csempe-min: 72px;', gyoker)
        self.assertIn('--radius-pill: 999px;', gyoker)
        self.assertIn('--font-he: "Frank Ruhl Libre"', gyoker)
        self.assertEqual(len(re.findall(r'^  --', b, re.M)), 10 + 5 + 52 + 18 + 35 + 6)

    def test_a_token_blokk_determinisztikus(self):
        self.assertEqual(arculat.Arculat.betolt().css, arculat.Arculat.betolt().css)


# =====================================================================================================================
@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestArculatUtvonal(unittest.TestCase):
    """A szerver a token-blokkot a `/arculat.css?v=<hash>` címen adja; a hash a lap gyorsítótár-kulcsában és ETag-jében."""

    @classmethod
    def setUpClass(cls):
        import alkalmazas
        cls.app = alkalmazas.letrehoz(db_ut=DB, kiadas='belso')
        cls.c = cls.app.test_client()
        cls.gyar = cls.app.extensions['pardes']['gyar']

    def test_utvonal(self):
        h = self.gyar.arculat.hash
        r = self.c.get('/arculat.css?v=' + h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'text/css; charset=utf-8')
        self.assertEqual(r.get_data(as_text=True), self.gyar.arculat.css)
        self.assertEqual(r.headers['Cache-Control'], 'public, max-age=31536000, immutable')
        self.assertEqual(r.headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(self.c.get('/arculat.css').headers['Cache-Control'], 'no-cache')           # hash nélkül: újraellenőrzendő
        self.assertEqual(self.c.get('/arculat.css?v=regi').headers['Cache-Control'], 'no-cache')
        self.assertEqual(self.c.get('/arculat.css', headers={'If-None-Match': r.headers['ETag']}).status_code, 304)

    def test_a_lap_linkeli_a_hash_sel_az_olvaso_css_elott(self):
        for ut in ('/', '/1Moz/1', '/szo/H0430', '/nincs-ilyen-konyv'):
            t = self.c.get(ut).get_data(as_text=True)
            i = t.index('<link rel="stylesheet" href="/arculat.css?v=%s">' % self.gyar.arculat.hash)
            self.assertLess(i, t.index('href="/statikus/olvaso.css"'), ut)
            self.assertNotIn('<style', t, ut)                                                    # CSP: nincs inline stílus

    def test_a_hash_a_lap_kulcsaban_es_etagjeben(self):
        """A token-fájl változása után (M2: mentés) nincs 304 a régi ETag-re, és nincs régi lap a gyorsítótárból."""
        a = self.c.get('/1Moz/1/3')
        self.assertEqual(self.c.get('/1Moz/1/3').headers['X-Cache'], 'HIT')
        regi = self.gyar.arculat
        adat = alap_adat()
        adat['szin']['accent']['light'] = '#123456'
        try:
            self.gyar.arculat = arculat_adatbol(adat)
            b = self.c.get('/1Moz/1/3', headers={'If-None-Match': a.headers['ETag']})
            self.assertEqual(b.status_code, 200)
            self.assertEqual(b.headers['X-Cache'], 'MISS')
            self.assertNotEqual(b.headers['ETag'], a.headers['ETag'])
            self.assertIn('/arculat.css?v=%s"' % self.gyar.arculat.hash, b.get_data(as_text=True))
            self.assertIn('--accent: #123456;', self.c.get('/arculat.css').get_data(as_text=True))
        finally:
            self.gyar.arculat = regi
        self.assertEqual(self.c.get('/1Moz/1/3').headers['ETag'], a.headers['ETag'])

    def test_minden_kiadasban_linkelve(self):
        """A token-blokk az arculat része, nem a tervező módé: nyilvános és kereskedelmi kiadásban is kell."""
        import alkalmazas
        for kiadas in ('nyilvanos', 'kereskedelmi'):
            c = alkalmazas.letrehoz(db_ut=DB, kiadas=kiadas).test_client()
            self.assertIn('href="/arculat.css?v=', c.get('/1Moz/1').get_data(as_text=True), kiadas)
            self.assertEqual(c.get('/arculat.css').status_code, 200, kiadas)


@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class TestExportArculat(unittest.TestCase):
    def test_az_export_ugyanabbol_a_fuggvenybol_irja(self):
        import adatbazis
        import export
        import hozzaferes
        import oldalak
        hozz = hozzaferes.Hozzaferes.betolt(os.path.join(D, 'konfig'))
        gyar = oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), hozz)
        with tempfile.TemporaryDirectory() as tmp:
            export.kiir(gyar, tmp, 'Ruth', hozz.szint())
            with open(os.path.join(tmp, 'arculat.css'), encoding='utf-8') as f:
                self.assertEqual(f.read(), arculat.css_blokk(gyar.arculat.adat))
            with open(os.path.join(tmp, 'Ruth', '1.html'), encoding='utf-8') as f:
                self.assertIn('/arculat.css?v=%s' % gyar.arculat.hash, f.read())


if __name__ == '__main__':
    unittest.main(verbosity=2)
