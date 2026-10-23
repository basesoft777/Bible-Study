"""A keresés tesztjei (#76 M3): unittest.

Futtatás: `python eszkozok/teszt_futtat.py` (a WSL venv-jével és a WSL-natív `~/pardes/pardes.db`-vel; `--fajl teszt_kereses`: csak ez).
A `PARDES_DB` nélkül a repó gyökerének `pardes.db`-je; ha nincs, a DB-s tesztek kimaradnak, a tiszta logikai tesztek futnak.

A tesztek csak olvasnak. Az elvárt értékeket, ahol lehet, független lekérdezés adja (nem a keresés saját kódja); a rögzített tények
(1Móz 1:1 „בְּרֵאשִׁית בָּרָא”, 1Móz 1:3 „Legyen világosság”) a Károli/TAHOT szövegéből valók.
"""
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
GY = os.path.dirname(os.path.dirname(D)).replace('\\', '/') + '/'
sys.path.insert(0, D)

import blokkok
import hozzaferes
import kereses
import lekerdezesek as q

try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

DB = os.environ.get('PARDES_DB') or (GY + 'pardes.db')
VAN_DB = os.path.exists(DB)


def app_keszit(kiadas='belso', hozz=None):
    import alkalmazas
    return alkalmazas.letrehoz(db_ut=DB, kiadas=kiadas, hozzaferes=hozz)


def talalat_igehelyek(html):
    return re.findall(r'<li class="talalat"><a href="[^"]+">([^<]+)</a>', html)


# =====================================================================================================================
class TestErtelmezes(unittest.TestCase):
    """A bemenet értelmezése adatbázis nélkül."""

    def test_tipus_felismeres(self):
        self.assertEqual(kereses.ertelmez({'q': 'H0216'}).tipus, 'strong')
        self.assertEqual(kereses.ertelmez({'q': 'h216 g3056'}).szavak, ['H0216', 'G3056'])
        self.assertEqual(kereses.ertelmez({'q': 'világosság'}).tipus, 'szo')
        self.assertEqual(kereses.ertelmez({'q': 'a föld'}).tipus, 'frazis')
        self.assertEqual(kereses.ertelmez({'q': 'בראשית ברא'}).tipus, 'heber')
        self.assertIsNone(kereses.ertelmez({}))
        self.assertIsNone(kereses.ertelmez({'q': '   '}))

    def test_tipusos_parameter_elsobbsege(self):
        k = kereses.ertelmez({'szo': 'Föld', 'mod': 'pontos', 'q': 'H0216'})
        self.assertEqual((k.tipus, k.szavak, k.mod), ('szo', ['föld'], 'pontos'))
        self.assertEqual(kereses.ertelmez({'szo': 'föld', 'mod': 'ismeretlen'}).mod, kereses.ALAP_MOD)
        self.assertEqual(kereses.ALAP_MOD, 'szoto')                                    # DT146/2
        self.assertEqual(kereses.ertelmez({'szo': 'föld', 'tol': 'x'}).tol, -1)

    def test_hibas_bemenet(self):
        for args in ({'q': 'x' * 101}, {'q': 'λόγος'}, {'strong': 'H0216 H0430 H1254 H0776'}, {'strong': "H0216'; DROP TABLE vers;--"},
                     {'frazis': 'egyetlen'}, {'frazis': 'a b c d e'}, {'szo': 'két szó'}, {'q': '%'}, {'q': '\x00a'},
                     {'heber': 'abc'}, {'heber': 'א ב ג ד ה'}):
            with self.subTest(args=args):
                with self.assertRaises(kereses.KeresesHiba):
                    kereses.ertelmez(args)

    def test_normalizalas(self):
        self.assertEqual(kereses.szo_kis('Világosság,'), 'világosság')
        self.assertEqual(kereses.szo_kis('בְּרֵאשִׁ֖ית'), 'בראשית')
        self.assertEqual(kereses.kereso_alak(' Béth-Semes '), 'béth-semes')
        self.assertEqual(kereses.hu_darabok('Béth-Semes'), ['béth', 'semes'])
        self.assertEqual(kereses.heber_szavak('עַל־פְּנֵי תְהוֹם'), ['עלפני', 'תהום'])

    def test_heber_magok_es_illesztes(self):
        self.assertEqual(kereses.heber_magok('בראשית'), ['בראשית', 'ראשית'])
        self.assertEqual(kereses.heber_magok('יהוה'), ['יהוה'])
        tok = [(1, 'ב', 'בְּ'), (2, 'ראשית', 'רֵאשִׁית'), (3, 'ברא', 'בָּרָא'), (4, 'אלהים', 'אֱלֹהִים')]
        self.assertEqual(kereses.heber_illeszt(tok, ['בראשית', 'ברא']), [[[1, 2], [3]]])
        self.assertEqual(kereses.heber_illeszt(tok, ['ב', 'ראשית']), [[[1], [2]]])
        self.assertEqual(kereses.heber_illeszt(tok, ['ברא', 'בראשית']), [])
        self.assertEqual(kereses.heber_illeszt(tok, ['אלהים', 'ב']), [])            # a vers végén nem lép tovább

    def test_heber_magok_szuffixum_korlat(self):
        """F76.50, a dokumentált korlát: a mag az előtag-betűk utáni rész; a szuffixumot nem választja le."""
        self.assertEqual(kereses.heber_magok('ובארץ'), ['ובארץ', 'בארץ', 'ארץ'])     # előtag + szó: a mag egy token (ארץ)
        self.assertEqual(kereses.heber_magok('זרעו'), ['זרעו'])                       # szuffixumos: nincs leválasztás
        self.assertEqual(kereses.heber_magok('למינו'), ['למינו', 'מינו', 'ינו'])      # elöl a ל (és a מ is előtag-betű) leválik, a ו szuffixum nem
        self.assertNotIn('מינ', kereses.heber_magok('למינו'))

    def test_kiemeles_escape(self):
        h = kereses.kiemelt_vers('<script>x</script> és világosság.', [(1, 'script'), (2, 'x'), (3, 'script'), (4, 'és'), (5, 'világosság')], {5})
        self.assertNotIn('<script>', h)
        self.assertIn('<mark>világosság</mark>.', h)
        self.assertEqual(str(kereses.kiemelt_vers('<b>', [], set())), '&lt;b&gt;')

    def test_kereses_url(self):
        k = kereses.ertelmez({'szo': 'föld', 'mod': 'pontos'})
        self.assertEqual(kereses.kereses_url(k, 77), '/kereses?szo=f%C3%B6ld&mod=pontos&tol=77')
        self.assertEqual(kereses.kereses_url(kereses.ertelmez({'szo': 'föld'})), '/kereses?szo=f%C3%B6ld')

    def test_sql_csak_a_lekerdezesekben(self):
        """N-F76c: a keresés kódja nem tartalmaz SQL-t és nem hív `execute`-ot; a frázis-sablon szövege csak a szószámtól függ."""
        with open(os.path.join(D, 'kereses.py'), encoding='utf-8') as f:
            forras = f.read()
        self.assertNotIn('.execute(', forras)
        self.assertIsNone(re.search(r'\bSELECT\b|\bFROM\b\s+\w+\s+WHERE', forras))
        self.assertEqual(sorted(q.FRAZIS_SQL), [2, 3, 4])
        for sql in q.FRAZIS_SQL.values():
            self.assertNotIn('%', sql)

    def test_hozzaferesi_azonositok(self):
        h = hozzaferes.Hozzaferes(['a', 'b'], 'a', {'kereses.szo': 'b', 'vers.tsk': 'b'}, 'a')
        h.ellenoriz_blokkok(blokkok.ismert_azonositok())
        with self.assertRaises(ValueError):
            hozzaferes.Hozzaferes(['a', 'b'], 'a', {'kereses.nincs': 'b'}, 'a').ellenoriz_blokkok(blokkok.ismert_azonositok())


# =====================================================================================================================
@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class TestKeresesAdat(unittest.TestCase):
    """A keresés függvényei a valódi adatbázison, független lekérdezéssel összevetve."""

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
        cls.sorrend = q.vers_sorrendek(cls.con)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def k(self, **args):
        return kereses.ertelmez(args)

    def test_szo_kis_azonos_az_epitovel(self):
        """A `szo_kis` szabálya egyezik a tárolt (az építő által számolt) értékkel, mindkét oldalon."""
        for oldal in ('hu', 'er'):
            sorok = self.con.execute("SELECT szo, szo_kis FROM token_karoli WHERE oldal=? AND rowid % 97 = 0 LIMIT 3000", (oldal,)).fetchall()
            self.assertGreater(len(sorok), 1000)
            elteres = [(a, b) for a, b in sorok if kereses.szo_kis(a) != (b or '')]
            self.assertEqual(elteres, [], oldal)

    def test_szo_pontos_fuggetlen_lekerdezessel(self):
        t = kereses.keres(self.con, self.k(szo='világosság', mod='pontos'), self.sorrend)
        vart = {r[0] for r in self.con.execute("SELECT DISTINCT igehely FROM token_karoli WHERE oldal='hu' AND lower(szo)='világosság'")}
        self.assertEqual({ig for _, ig in t.versek}, vart)
        self.assertIn('1Móz 1:3', vart)
        self.assertEqual(len({sz for ig, sz in t.hu if ig == '1Móz 1:3'}), 2)        # „Legyen világosság: és lőn világosság.”

    def test_szo_szotari_alak(self):
        t = kereses.keres(self.con, self.k(szo='világosság'), self.sorrend)
        # a #95 kereső-lekérdezése (db_meres.SZOTO_Q_K), egy lekérdezésben, a pontos alakkal együtt
        vart = {r[0] for r in self.con.execute("SELECT DISTINCT t.igehely FROM szotari_kereso k JOIN token_karoli t ON t.szo=k.alak AND t.oldal='hu' "
                                               "WHERE k.keresoalak='világosság'")}
        vart |= {r[0] for r in self.con.execute("SELECT DISTINCT igehely FROM token_karoli WHERE oldal='hu' AND szo_kis='világosság'")}
        self.assertEqual({ig for _, ig in t.versek}, vart)
        self.assertIn('világosságot', dict(t.info['alakok']))                       # 1Móz 1:4: „elválasztá … a világosságot”
        self.assertGreater(len(t.versek), len(kereses.keres(self.con, self.k(szo='világosság', mod='pontos'), self.sorrend).versek))

    def test_szo_mai_alakra_is_talal(self):
        """DT130 (1): a mai helyesírású alakra (amely) a régi (mely) is előjön."""
        t = kereses.keres(self.con, self.k(szo='amely'), self.sorrend)
        self.assertIn('mely', dict(t.info['alakok']))

    def test_szo_javaslat_a_szotari_alakra(self):
        t = kereses.keres(self.con, self.k(szo='földet'), self.sorrend)
        self.assertEqual(t.info.get('javaslat'), 'föld')

    def test_szo_strong_ag(self):
        a = kereses.keres(self.con, self.k(szo='világosság'), self.sorrend)
        c = kereses.keres(self.con, self.k(szo='világosság', mod='szoto_strong'), self.sorrend)
        self.assertTrue(set(a.versek) <= set(c.versek))
        self.assertIn('H0216', dict(c.info['strong_ag']))
        nyt = {r[0] for r in self.con.execute('SELECT strong FROM grammatikai_strongok')}
        self.assertFalse(set(dict(c.info['strong_ag'])) & nyt)
        zart = kereses.keres(self.con, self.k(szo='világosság', mod='szoto_strong'), self.sorrend, par_lathato=False)
        self.assertEqual(zart.versek, a.versek)
        self.assertTrue(zart.figyelmeztetes)

    def test_frazis_es_vershatar(self):
        t = kereses.keres(self.con, self.k(frazis='kietlen és'), self.sorrend)
        self.assertIn('1Móz 1:2', [ig for _, ig in t.versek])
        for _, ig in t.versek:
            szoveg = self.con.execute('SELECT karoli_szoveg FROM vers WHERE igehely=?', (ig,)).fetchone()[0]
            self.assertRegex(szoveg.lower(), r'kietlen\W+és')
        # 1Móz 1:1 vége „a földet.”, 1:2 eleje „A föld”: a frázis nem lép át a vershatáron
        t = kereses.keres(self.con, self.k(frazis='földet a föld'), self.sorrend)
        self.assertNotIn('1Móz 1:1', [ig for _, ig in t.versek])

    def test_strong(self):
        t = kereses.keres(self.con, self.k(strong='H0216'), self.sorrend)
        vart = {r[0] for r in self.con.execute("SELECT DISTINCT igehely FROM token_strong WHERE strong='H0216'")}
        self.assertEqual({ig for _, ig in t.versek}, vart)
        self.assertEqual(t.elofordulas, self.con.execute("SELECT COUNT(*) FROM token_strong WHERE strong='H0216'").fetchone()[0])
        ket = kereses.keres(self.con, self.k(strong='H1254 H0430'), self.sorrend)
        self.assertIn('1Móz 1:1', [ig for _, ig in ket.versek])
        self.assertTrue({ig for _, ig in ket.versek} <= {r[0] for r in self.con.execute("SELECT igehely FROM token_strong WHERE strong='H1254'")})
        rendezett = [s for s, _ in t.versek]
        self.assertEqual(rendezett, sorted(rendezett))

    def test_heber_frazis(self):
        for bemenet in ('בראשית ברא', 'בְּרֵאשִׁית בָּרָא', 'ב ראשית ברא'):
            with self.subTest(bemenet=bemenet):
                t = kereses.keres(self.con, self.k(heber=bemenet), self.sorrend)
                self.assertEqual([ig for _, ig in t.versek], ['1Móz 1:1'])
        # 1Móz 1:1 vége „וְאֵת הָאָרֶץ”, 1:2 eleje „וְהָאָרֶץ”: a frázis nem lép át a vershatáron
        t = kereses.keres(self.con, self.k(heber='הארץ והארץ'), self.sorrend)
        self.assertNotIn('1Móz 1:1', [ig for _, ig in t.versek])
        egy = kereses.keres(self.con, self.k(heber='יהוה'), self.sorrend)
        self.assertEqual(egy.elofordulas, self.con.execute("SELECT COUNT(*) FROM token_karoli WHERE oldal='er' AND szo_kis='יהוה'").fetchone()[0])

    def test_heber_elotag_es_szuffixum(self):
        """F76.50 (a súgó szerint): előtag + szó talál; a szuffixumos egybeírt alak nem (a TAHOT a szuffixumot külön tokenként tartja);
        tokenenként, szóközzel bontva talál, a tő szóvégi alak nélkül."""
        def igek(s):
            return [ig for _, ig in kereses.keres(self.con, self.k(heber=s), self.sorrend).versek]
        tok = [r[0] for r in self.con.execute("SELECT szo_kis FROM token_karoli WHERE oldal='er' AND igehely='1Móz 1:11' ORDER BY sorszam")]
        self.assertIn(['זרע', 'ו'], [tok[i:i + 2] for i in range(len(tok))])          # független: a szuffixum külön token
        self.assertIn(['ל', 'מינ', 'ו'], [tok[i:i + 3] for i in range(len(tok))])
        # előtag + szó (egybeírva és bontva) ugyanazt adja; a vers a független lekérdezésből
        vart = {r[0] for r in self.con.execute("SELECT DISTINCT a.igehely FROM token_karoli a JOIN token_karoli b ON b.igehely=a.igehely "
                                               "AND b.oldal='er' AND b.sorszam=a.sorszam+1 AND b.szo_kis='בארץ' WHERE a.oldal='er' AND a.szo_kis='ו'")}
        vart |= {r[0] for r in self.con.execute("SELECT DISTINCT a.igehely FROM token_karoli a JOIN token_karoli b ON b.igehely=a.igehely "
                                                "AND b.oldal='er' AND b.sorszam=a.sorszam+1 AND b.szo_kis='ארץ' JOIN token_karoli c "
                                                "ON c.igehely=a.igehely AND c.oldal='er' AND c.sorszam=a.sorszam-1 AND c.szo_kis='ו' "
                                                "WHERE a.oldal='er' AND a.szo_kis='ב'")}
        vart |= {r[0] for r in self.con.execute("SELECT DISTINCT igehely FROM token_karoli WHERE oldal='er' AND szo_kis='ובארץ'")}
        self.assertTrue(vart)
        self.assertEqual(set(igek('ובארץ')), vart)
        self.assertEqual(set(igek('ו ב ארץ')), vart)
        # a dokumentált korlát: a szuffixumos egybeírt alak az 1Móz 1:11-et nem adja
        self.assertNotIn('1Móz 1:11', igek('זרעו'))
        self.assertEqual(igek('למינו'), [])
        # a súgó szerinti bontás talál
        for s in ('זרע ו', 'ל מינ ו', 'למינ ו'):
            with self.subTest(bemenet=s):
                self.assertIn('1Móz 1:11', igek(s))
        self.assertEqual(igek('ל מין ו'), [])                                        # szóvégi alakkal (ן) nem: a súgó ezt is kiírja

    def test_ures_eredmeny(self):
        for args in ({'szo': 'xyzqw'}, {'frazis': 'xyzqw világosság'}, {'heber': 'שששששש'}, {'strong': 'H8999'}):
            with self.subTest(args=args):
                t = kereses.keres(self.con, kereses.ertelmez(args), self.sorrend)
                self.assertEqual(t.versek, [])
        self.assertTrue(kereses.keres(self.con, self.k(strong='H8999'), self.sorrend).figyelmeztetes)

    def test_lapozas(self):
        t = kereses.keres(self.con, self.k(szo='föld'), self.sorrend)
        elso, kov = kereses.lap(t, -1)
        masodik, _ = kereses.lap(t, kov)
        self.assertEqual(len(elso), kereses.OLDALMERET)
        self.assertEqual(elso + masodik, t.versek[:len(elso) + len(masodik)])
        self.assertFalse(set(elso) & set(masodik))


# =====================================================================================================================
@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestKeresesLap(unittest.TestCase):
    """A /kereses útvonal: ismert kérdés, üres eredmény, injekció, XSS, forrássor, linkek, nézetek, kiadás, hozzáférési szint."""

    @classmethod
    def setUpClass(cls):
        cls.app = app_keszit()
        cls.c = cls.app.test_client()

    def get(self, u):
        return self.c.get(u)

    def test_ismert_kerdes_es_forrassor(self):
        for u, vart in (('/kereses?szo=világosság&mod=pontos', '1Móz 1:3'), ('/kereses?q=H0216', '1Móz 1:3'), ('/kereses?frazis=kietlen és', '1Móz 1:2'),
                        ('/kereses?heber=בראשית ברא', '1Móz 1:1'), ('/kereses?q=világosság', '1Móz 1:4')):
            with self.subTest(u=u):
                r = self.get(u)
                self.assertEqual(r.status_code, 200)
                h = r.get_data(as_text=True)
                self.assertIn(vart, talalat_igehelyek(h))
                self.assertIn('class="forras">Forrás és licenc:', h)
                self.assertIn('class="jelleg ', h)
                self.assertIn('<mark>', h)

    def test_talalati_linkek_vers_lapra(self):
        h = self.get('/kereses?szo=világosság&mod=pontos').get_data(as_text=True)
        linkek = re.findall(r'<li class="talalat"><a href="([^"]+)">', h)
        self.assertTrue(linkek)
        for u in linkek[:8]:
            self.assertRegex(u, r'^/[A-Za-z0-9]+/\d+/\d+$')
            self.assertEqual(self.get(u).status_code, 200, u)

    def test_ures_eredmeny_explicit(self):
        r = self.get('/kereses?szo=xyzqw')
        self.assertEqual(r.status_code, 200)
        h = r.get_data(as_text=True)
        self.assertIn('Nincs találat', h)
        self.assertIn('0 vers', h)

    def test_hibas_bemenet_400(self):
        for u in ('/kereses?q=%25', '/kereses?q=λόγος', '/kereses?frazis=egy', '/kereses?strong=X1'):
            with self.subTest(u=u):
                r = self.get(u)
                self.assertEqual(r.status_code, 400)
                self.assertIn('role="alert"', r.get_data(as_text=True))

    def test_injekcio(self):
        con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
        elotte = con.execute('SELECT COUNT(*) FROM vers').fetchone()[0]
        for u in ("/kereses?szo=' OR '1'='1", "/kereses?q=' OR 1=1 --", "/kereses?strong=H0216'; DROP TABLE vers;--", '/kereses?frazis=a"; DROP TABLE vers; --',
                  '/kereses?heber=א\'; DELETE FROM vers;--', '/kereses?szo=%25', '/kereses?szo=_', '/kereses?tol=1 OR 1=1&szo=föld', '/kereses?mod=pontos)--&szo=föld'):
            with self.subTest(u=u):
                r = self.get(u)
                self.assertIn(r.status_code, (200, 400))
        self.assertEqual(con.execute('SELECT COUNT(*) FROM vers').fetchone()[0], elotte)
        # a `%` és `_` nem helyettesítő karakter (nincs LIKE): a „szo=_” nem talál mindent
        self.assertNotIn('<li class="talalat">', self.get('/kereses?szo=_').get_data(as_text=True))
        con.close()

    def test_xss(self):
        for u in ('/kereses?q=<script>alert(1)</script>', '/kereses?szo=<img src=x onerror=alert(1)>', '/kereses?frazis=<b>a</b> föld',
                  '/kereses?heber=<script>א</script>', '/kereses?q="><svg onload=alert(1)>'):
            with self.subTest(u=u):
                h = self.get(u).get_data(as_text=True)
                self.assertNotIn('<script>alert', h)
                self.assertNotIn('<img src=x', h)
                self.assertNotIn('<svg onload', h)
                self.assertNotIn('<b>a</b>', h)

    def test_ugras_igehelyre(self):
        r = self.get('/kereses?q=1Móz 1:4')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers['Location'], '/1Moz/1/4')

    def test_minden_retegbol_elerheto(self):
        """A fejléc kereső mezője (Ctrl+K: `.ugras input[name=q]`) réteggel és nélküle is a /kereses-re küld (#134: nézetek helyett rétegek)."""
        for reteg in ('', 'il'):
            for u in ('/1Moz/1/3?reteg=' + reteg, '/szo/H0216?reteg=' + reteg, '/?reteg=' + reteg, '/kereses?szo=föld&reteg=' + reteg):
                with self.subTest(u=u):
                    h = self.get(u).get_data(as_text=True)
                    self.assertRegex(h, r'<form class="ugras" action="/kereses" method="get" role="search">\s*<input type="text" name="q"')
        with open(os.path.join(D, 'statikus', 'olvaso.js'), encoding='utf-8') as f:
            self.assertIn(".ugras input[name=q]", f.read())

    def test_lapozo_link(self):
        h = self.get('/kereses?szo=föld').get_data(as_text=True)
        self.assertEqual(len(talalat_igehelyek(h)), kereses.OLDALMERET)
        m = re.search(r'<a href="(/kereses\?szo=[^"]+tol=(\d+))">a következő', h)
        self.assertTrue(m)
        h2 = self.get(m.group(1).replace('&amp;', '&')).get_data(as_text=True)
        self.assertIn('start="%d"' % (kereses.OLDALMERET + 1), h2)
        self.assertFalse(set(talalat_igehelyek(h)) & set(talalat_igehelyek(h2)))

    def test_szotoken_nelkuli_konyvek_jelzese(self):
        h = self.get('/kereses?szo=ige').get_data(as_text=True)
        self.assertIn('Nem keresett könyvek', h)
        for kk in ('Mt', 'Ján', 'Jel'):
            self.assertIn(kk, h)
        g = self.get('/kereses?strong=G3056').get_data(as_text=True)
        self.assertIn('Mt 5:37', talalat_igehelyek(g))                                # a Strong-keresés a párosítatlan könyvekben is talál,
        self.assertIn('szótoken nélkül: kiemelés nincs', g)                            # de kiemelés nélkül, és ezt kiírja

    def test_sugo_heber_korlat(self):
        """F76.50: a súgó kimondja, mit tud a héber keresés (előtag + szó) és mit nem (szuffixumos egybeírt alak), és hogyan kell bontani."""
        h = self.get('/kereses').get_data(as_text=True)
        for resz in ('előtag + szót', 'Nem talál', 'névmási szuffixumos', 'זרעו', 'למינו', 'szóközzel', 'זרע ו', 'ל מינ ו', 'szóvégi alak nélkül'):
            with self.subTest(resz=resz):
                self.assertIn(resz, h)
        with open(os.path.join(D, 'README.md'), encoding='utf-8') as f:
            readme = f.read()
        for resz in ('**Nem talál**', 'זרעו', 'זרע ו', 'ל מינ ו'):
            self.assertIn(resz, readme)

    def test_szo_panel_linkje(self):
        self.assertIn('/kereses?strong=H0216', self.get('/r/szo/H0216').get_data(as_text=True))


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestKeresesKiadasEsSzint(unittest.TestCase):

    def test_kiadasok(self):
        """A keresés egyik kiadásban sem olvas kizárt táblát (az authorizer-napló üres)."""
        for kiadas in ('belso', 'nyilvanos', 'kereskedelmi'):
            with self.subTest(kiadas=kiadas):
                app = app_keszit(kiadas)
                c = app.test_client()
                for u in ('/kereses?szo=föld&mod=szoto_strong', '/kereses?q=H0216', '/kereses?strong=G3056', '/kereses?frazis=a föld', '/kereses?heber=בראשית ברא'):
                    self.assertEqual(c.get(u).status_code, 200, u)
                self.assertEqual(app.extensions['pardes']['db'].kiserletek, [])

    def test_hozzaferesi_szint_zar(self):
        h = hozzaferes.Hozzaferes(['nyilvanos', 'kutato'], 'nyilvanos', {'kereses.szo': 'kutato', 'vers.par': 'kutato'}, 'nyilvanos')
        app = app_keszit('nyilvanos', hozz=h)
        hivas = []
        eredeti = q.kereses_hu_szo_kis
        try:
            q.kereses_hu_szo_kis = lambda *a, **kw: hivas.append(a) or eredeti(*a, **kw)
            r = app.test_client().get('/kereses?szo=föld')
        finally:
            q.kereses_hu_szo_kis = eredeti
        self.assertEqual(r.status_code, 200)
        self.assertIn('nem érhető el', r.get_data(as_text=True))
        self.assertEqual(hivas, [])                                                    # zárt módban a lekérdezés nem fut
        # a Strong-keresés nyitott, de a párosításos kiemelés (vers.par) zárt: nincs <mark>
        g = app.test_client().get('/kereses?strong=H0216').get_data(as_text=True)
        self.assertIn('1Móz 1:3', talalat_igehelyek(g))
        self.assertNotIn('<mark>', g.split('<ol class="talalatok"')[1].split('</ol>')[0])
        self.assertNotIn('Károli-alakok a párosításban', g)                              # a párosítás adata zárt blokknál nem szivárog


if __name__ == '__main__':
    unittest.main(verbosity=2)
