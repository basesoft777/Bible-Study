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


if __name__ == '__main__':
    unittest.main()
