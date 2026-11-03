"""teszt_bdb_rovidites.py — a BDB egybetűs rövidítéseinek közös jelölője (N-F131x).

Futtatás: python eszkozok/teszt_bdb_rovidites.py
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_rovidites as BR  # noqa: E402

CIMSZO = 'קָרָא (kárá)'


class Jelol(unittest.TestCase):

    def test_jahve_helyes_sorrend(self):
        u = BR.jelol('hívni ׳י nevével', CIMSZO, 'ק')
        self.assertEqual(u, 'hívni <abbr class="rovidites" title="%s">י׳</abbr> nevével' % BR.JAHVE_CIM)

    def test_cimszo_kezdobetu(self):
        u = BR.jelol('perfectum ׳ק 1Móz 11:9', CIMSZO, 'ק')
        self.assertIn('<abbr class="rovidites" title="a címszó: קָרָא (kárá)">ק׳</abbr>', u)

    def test_jahve_es_cimszo_ha_a_cimszo_is_jod(self):
        u = BR.jelol('׳י', 'יָדַע (jádá)', 'י')
        self.assertIn('%s; vagy a címszó: יָדַע (jádá)' % BR.JAHVE_CIM, u)

    def test_mas_betu_altalanos(self):
        self.assertIn(BR.ALTALANOS, BR.jelol('׳א x', CIMSZO, 'ק'))

    def test_cimszo_nelkul_altalanos(self):
        self.assertIn(BR.ALTALANOS, BR.jelol('׳ק x'))

    def test_prezentacios_alak_betu(self):
        u = BR.jelol('a ׳שׁ eszerint', 'שְׁאוֹל (seól)', BR.alapbetu('שְׁאוֹל'))
        self.assertIn('title="a címszó: שְׁאוֹל (seól)">שׁ׳</abbr>', u)

    def test_tobbbetus_szo_valtozatlan(self):
        for sz in ('׳בשם x', 'י ׳בְּשֵׁם', 'אב׳'):
            self.assertEqual(BR.jelol(sz, CIMSZO, 'ק'), sz)

    def test_cim_escape_html_kimenethez(self):
        u = BR.jelol('&lt;b&gt; ׳ק', '<script>"x"</script>', 'ק', cim_esc=lambda s: s.replace('&', '&amp;').replace(
            '<', '&lt;').replace('>', '&gt;').replace('"', '&#34;'), attr=' tabindex="0"')
        self.assertNotIn('<script>', u)
        self.assertIn('&lt;b&gt; <abbr class="rovidites" title="a címszó: &lt;script&gt;&#34;x&#34;&lt;/script&gt;" '
                      'tabindex="0">ק׳</abbr>', u)

    def test_ures(self):
        self.assertEqual(BR.jelol(None), '')

    def test_javitott_alak_is(self):
        # DT-F131z: a sorrend-javítás után a geres a betű után áll
        u = BR.jelol('ק׳ בְּשֵׁם י׳ x', CIMSZO, 'ק')
        self.assertIn('<abbr class="rovidites" title="a címszó: קָרָא (kárá)">ק׳</abbr> בְּשֵׁם', u)
        self.assertIn('<abbr class="rovidites" title="%s">י׳</abbr> x' % BR.JAHVE_CIM, u)
        self.assertEqual(BR.jelol('לְשׁ׳ x', CIMSZO, 'ק'), 'לְשׁ׳ x')     # többbetűs: nem egybetűs rövidítés


class Atiras(unittest.TestCase):
    JAV = {'H0011': [('Sh®°ôl', 'Sheʾôl')]}

    def test_csere_toldalekkal(self):
        # DT-F164a: részszöveg szerint, a magyar toldalékkal is
        self.assertEqual(BR.atiras_javit('a Sh®°ôlban (Sh®°ôl).', 'H11', self.JAV), 'a Sheʾôlban (Sheʾôl).')
        self.assertEqual(BR.atiras_javit('a Sh®°ôlban', 'H0001', self.JAV), 'a Sh®°ôlban')

    def test_tabla(self):
        t = BR.atiras_javitasok()
        self.assertIn(('She®°ôl', 'Sheʾôl'), t.get('H7585', []))
        self.assertNotIn('H7848', t)          # jelolt_marad: nincs csere


class HeberSorrend(unittest.TestCase):
    JAV = {'H7121': [('׳ק י ׳בְּשֵׁם', 'ק׳ בְּשֵׁם י׳'), ('גְּדוֺל בְּקוֺל', 'בְּקוֺל גְּדוֺל')]}

    def test_csere_betu_szerint(self):
        u = BR.heber_sorrend_javit('c. ׳ק י ׳בְּשֵׁם hívni, és גְּדוֺל בְּקוֺל.', 'H7121', self.JAV)
        self.assertEqual(u, 'c. ק׳ בְּשֵׁם י׳ hívni, és בְּקוֺל גְּדוֺל.')

    def test_strong_kitoltes(self):
        self.assertEqual(BR.heber_sorrend_javit('גְּדוֺל בְּקוֺל', 'H7121', self.JAV), 'בְּקוֺל גְּדוֺל')
        self.assertEqual(BR.heber_sorrend_javit('גְּדוֺל בְּקוֺל', 'H0001', self.JAV), 'גְּדוֺל בְּקוֺל')

    def test_heber_betuvel_hataros_nem(self):
        sz = 'וּגְּדוֺל בְּקוֺל'
        self.assertEqual(BR.heber_sorrend_javit(sz, 'H7121', self.JAV), sz)

    def test_tabla(self):
        # a generált tábla javitva sorai betöltődnek; a valodi_sorrend és a jelolt_marad nem
        t = BR.sorrend_javitasok()
        self.assertIn(('גְּדוֺל בְּקוֺל', 'בְּקוֺל גְּדוֺל'), t.get('H7121', []))
        self.assertNotIn('׳ק י ׳בְּשֵׁם', dict(t.get('H7121', [])))


class Izolal(unittest.TestCase):

    def test_futam_utan_szam(self):
        self.assertEqual(BR.izolal('יִקְרָא 1Móz 2:19'), 'יִקְרָא‎ 1Móz 2:19')
        self.assertEqual(BR.izolal('׳י, 2Sám 7:1'), '׳י‎, 2Sám 7:1')
        self.assertEqual(BR.izolal('יִקְרָא <a href="/v">1Móz 2:19</a>'), 'יִקְרָא‎ <a href="/v">1Móz 2:19</a>')

    def test_nem_szam_utan_valtozatlan(self):
        for sz in ('יִקְרָא hívni', 'Gen 2:19 יִקְרָא', 'יִקְרָא Gen 2:19'):
            self.assertEqual(BR.izolal(sz), sz)

    def test_idempotens(self):
        egyszer = BR.izolal('יִקְרָא 1Móz 2:19')
        self.assertEqual(BR.izolal(egyszer), egyszer)


if __name__ == '__main__':
    unittest.main()
