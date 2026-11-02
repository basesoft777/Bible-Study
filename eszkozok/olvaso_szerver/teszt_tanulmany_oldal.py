"""A tanulmány-oldal és a tanulmány-panel tesztjei (F149 M2–M3): unittest.

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_tanulmany_oldal` (CLAUDE.md); a DB-s osztályok a `pardes.db`-ben lévő
`tanulmany*` táblák nélkül (régebbi építés) kimaradnak, a megjelenítő tesztjei adat nélkül is futnak.
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

import blokkok  # noqa: E402
import tanulmany_oldal as TO  # noqa: E402

T = blokkok.tanulmany_regiszter

try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

DB = os.environ.get('PARDES_DB') or (GY + 'pardes.db')


def _db_tanulmannyal():
    if not os.path.exists(DB):
        return False
    try:
        con = sqlite3.connect('file:%s?mode=ro' % DB, uri=True)
        try:
            return con.execute("SELECT 1 FROM sqlite_master WHERE name='tanulmany_szoveg'").fetchone() is not None
        finally:
            con.close()
    except sqlite3.Error:
        return False


VAN_TAN_DB = VAN_FLASK and _db_tanulmannyal()


def megjelenito(egy=('1Móz', 14), alap='1Móz'):
    kulcsok = T.karoli_kulcsok(GY)
    kar = T.Karoli(kulcsok, GY)

    def href(kulcs):
        m = re.match(r'^(\S+) (\d+):(\d+)$', kulcs)
        return '/%s/%s/%s#v%s' % (m.group(1).replace('ó', 'o'), m.group(2), m.group(3), m.group(3))
    return TO.Megjelenito(T, kar, href, alap, egy)


class Megjelenites(unittest.TestCase):
    def render(self, md, **kw):
        h, toc = megjelenito(**kw).megjelenit(md)
        return str(h), toc

    def test_html_escape_es_nincs_nyers_html(self):
        h, _ = self.render('Szöveg <script>alert(1)</script> és &amp; "idézet"')
        self.assertNotIn('<script>', h)
        self.assertIn('&lt;script&gt;', h)

    def test_horgonyok_egyeznek_az_index_horgonyaival(self):
        md = '# Cím — x\n\n## 1. Alapkérdések\nszöveg\n\n### Peshat (Szó szerinti)\nszöveg\n\n## 1. Alapkérdések\nmásik\n'
        h, toc = self.render(md)
        T_h = [x[0] for x in T.szakaszok(md) if x[0] != 'eleje']
        self.assertEqual([x[0] for x in toc], T_h)
        for hor in T_h:
            self.assertIn('id="%s"' % hor, h)
        self.assertEqual(len(set(T_h)), len(T_h))              # ismétlődő cím: -2

    def test_igehely_visszahorgony(self):
        h, _ = self.render('Melkisédek (14:18) áld; lásd Zsolt 110:4 és az 1Móz 14:19-20 helyet.\n')
        self.assertIn('<a class="igehely" href="/1Moz/14/18#v18">14:18</a>', h)
        self.assertIn('href="/Zsolt/110/4#v4"', h)
        self.assertIn('href="/1Moz/14/19#v19">1Móz 14:19-20</a>', h)

    def test_vers_jeloles_egyfejezetes_tanulmanyban(self):
        h, _ = self.render('A 18. v. szól Melkisédekről.\n')
        self.assertIn('href="/1Moz/14/18#v18"', h)
        h2, _ = self.render('A 18. v. szól.\n', egy=None)
        self.assertNotIn('class="igehely"', h2)                # több fejezetnél a „18. v.” nem oldható fel

    def test_nem_linkel_linken_belul_es_kodban(self):
        h, _ = self.render('`1Móz 14:18` nem link, **1Móz 14:19** link.\n')
        self.assertNotIn('<code><a', h)
        self.assertIn('<strong><a class="igehely" href="/1Moz/14/19#v19">1Móz 14:19</a></strong>', h)

    def test_tabla_es_lista_es_idezet(self):
        md = '| Vers | Szó |\n|---|---|\n| 18 | *kenyér* |\n| 19 | bor |\n\n- egy\n  - beágyazott\n- kettő\n\n> idézet\n'
        h, _ = self.render(md)
        self.assertIn('<th>Vers</th>', h)
        self.assertIn('<a class="igehely" href="/1Moz/14/18#v18">18</a>', h)
        self.assertIn('<em>kenyér</em>', h)
        self.assertIn('<ul><li>egy<ul><li>beágyazott</li></ul></li><li>kettő</li></ul>', h)
        self.assertIn('<blockquote>', h)

    def test_a_valos_tanulmanyok_megjelennek_es_horgonyaik_megvannak(self):
        for f in ('genezis/1Moz_14_bovitett.md', 'genezis/1Moz_4v25-5v32_bovitett.md'):
            with open(GY + f, encoding='utf-8') as fh:
                md = fh.read()
            h, toc = megjelenito(egy=None).megjelenit(md)
            h = str(h)
            self.assertGreater(len(toc), 5, f)
            for hor, _, _ in toc:
                self.assertEqual(h.count('id="%s"' % hor), 1, f + ' ' + hor)
            self.assertGreater(h.count('class="igehely"'), 5, f)


class PanelSzoveg(unittest.TestCase):
    def test_hivatkozas_nelkuli_vers_explicit_jelzes(self):
        h = str(blokkok._r_tanulmany(([('1Moz_14', 'bovitett', 'cim', '1Móz 14:1–24', 0, [])], []), None))
        self.assertIn('A tanulmány ezt a szakaszt tárgyalja, de erre a versre külön nem hivatkozik.', h)
        self.assertNotIn('név szerint szól', h)

    def test_ket_fokozat_kulon_szoveg(self):
        sorok = [('1-alap', 'Alapkérdések', 'nev', '14:18'), ('2-tab', 'Táblázat', 'tartomany', '14:18-20')]
        h = str(blokkok._r_tanulmany(([('1Moz_14', 'bovitett', 'cim', '1Móz 14:1–24', 0, sorok)], []), None))
        self.assertIn('A tanulmány erről a versről név szerint szól: <a href="/tanulmany/1Moz_14#1-alap">Alapkérdések</a>', h)
        self.assertIn('A tanulmány ezt a szakaszt egészében tárgyalja (14:18-20): <a href="/tanulmany/1Moz_14#2-tab">Táblázat</a>', h)

    def test_mas_tanulmany_hivatkozik(self):
        h = str(blokkok._r_tanulmany(([], [('1Moz_15', 'bovitett', 'x', '1Móz 15:1–21', [('4-kap', 'Kapcsolódó igehelyek', '14:18')])]), None))
        self.assertIn('Más tanulmányok is hivatkoznak erre a versre', h)
        self.assertIn('href="/tanulmany/1Moz_15#4-kap"', h)


class Tanulmany_nev(unittest.TestCase):
    def test_nev(self):
        self.assertEqual(blokkok.tanulmany_nev('1Móz 14:1–24', 'bővített PaRDeS-tanulmány (x)'), '1Móz 14:1–24')
        self.assertEqual(blokkok.tanulmany_nev('1Móz 4:25–5:32', 'Séth nemzetségtáblája'), '1Móz 4:25–5:32 — Séth nemzetségtáblája')
        self.assertEqual(blokkok.tanulmany_nev('1Móz 14:18–20 / Zsolt 110:4', 'Mélyelemzés'), '1Móz 14:18–20 / Zsolt 110:4')


@unittest.skipUnless(VAN_TAN_DB, 'nincs Flask vagy a pardes.db-ben még nincsenek a tanulmany* táblák (F149): építés után fut')
class Oldalak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import alkalmazas
        cls.app = alkalmazas.letrehoz(db_ut=DB, kiadas='belso')
        cls.c = cls.app.test_client()

    def get(self, u):
        r = self.c.get(u)
        return r.status_code, r.get_data(as_text=True)

    def test_panel_tartomanyon_beluli_vers(self):
        s, h = self.get('/r/vers/1Moz/14/18')
        self.assertEqual(s, 200)
        i = h.index('data-blokk="vers.tanulmany"')
        resz = h[i:i + 4000]
        self.assertIn('href="/tanulmany/1Moz_14"', resz)
        self.assertIn('href="/tanulmany/1Mozes_14_18-20_Zsolt110_4_Zsid5-7"', resz)
        self.assertIn('A tanulmány erről a versről név szerint szól', resz)
        self.assertNotIn('belső', resz)

    def test_fejezet_margojel_es_kapcsolo(self):
        s, h = self.get('/1Moz/4')
        self.assertEqual(s, 200)
        self.assertEqual(len(re.findall(r'class="tan-jel"', h)), 2)
        self.assertIn('id="tan-jeloles"', h)
        s, h = self.get('/1Moz/5')
        self.assertIn('Folytatás', h)

    def test_fejezet_tanulmany_nelkul_nincs_kapcsolo(self):
        s, h = self.get('/Zsolt/1')
        self.assertEqual(s, 200)
        self.assertNotIn('id="tan-jeloles"', h)
        self.assertNotIn('class="tan-jel"', h)

    def test_tanulmany_oldal_visszahorgony(self):
        s, h = self.get('/tanulmany/1Moz_14')
        self.assertEqual(s, 200)
        self.assertGreater(h.count('class="igehely"'), 10)
        self.assertIn('href="/1Moz/14/', h)
        self.assertIn('generált nézet', h)

    def test_ismeretlen_tanulmany_404(self):
        for u in ('/tanulmany/nincs_ilyen', '/tanulmany/..%2Fetc', '/tanulmany/' + 'a' * 200):
            self.assertEqual(self.get(u)[0], 404, u)

    def test_forrasfajlok_valtozatlanok(self):
        # a tanulmány oldala csak olvas: a forrás-könyvtárakban nincs módosított fájl (a tesztet a CI-ben a git diff is őrzi)
        self.assertTrue(os.path.exists(GY + 'genezis/1Moz_14_bovitett.md'))


if __name__ == '__main__':
    unittest.main(verbosity=1)
