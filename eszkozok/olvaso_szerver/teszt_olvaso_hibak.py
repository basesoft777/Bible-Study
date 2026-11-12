"""Az olvasó-szerver három nyitott hibájának védelme (F204): N-F99a (tW nyers Markdown), N117 (feloldatlan BDB-jelek), N118 (`/szo/<strong>?vers=`).

Futtatás: `python eszkozok/teszt_futtat.py --gyors` (a WSL-natív PARDES_DB-vel). A DB nélküli tesztek (a Markdown-renderelő) mindig futnak.
"""
import os
import re
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import blokkok
from teszt_olvaso_szerver import VAN_DB, VAN_FLASK, app_keszit


class TestTwMarkdown(unittest.TestCase):
    """N-F99a: a translationWords-szócikk Markdownja nem jelenhet meg nyersen."""

    MINTA = ('# abomination, abominable\\n\\n## Definition:\\n\\nA term “abomination” is __bold__ and *dim*.\\n\\n'
             '* Egy [link](rc://hu/tw/dict/bible/kt/falsegod) tétel.\\n* Más <b>tétel</b> ([x](../kt/sin.md)).\\n\\n## Translation Suggestions:\\n\\nVége.')

    def test_nincs_nyers_jel(self):
        h = str(blokkok._md_tw(self.MINTA, 'abomination, abominable'))
        self.assertNotIn('\\n', h)
        self.assertNotRegex(h, r'(^|>)\s*#')
        self.assertNotIn('](', h)
        self.assertNotIn('__', h)
        self.assertNotIn('rc://', h)

    def test_szerkezet(self):
        h = str(blokkok._md_tw(self.MINTA, 'abomination, abominable'))
        self.assertNotIn('<h5>abomination', h)              # a blokk h4-e már kiírja a címet
        self.assertEqual(re.findall(r'<h5>([^<]*)</h5>', h), ['Definition:', 'Translation Suggestions:'])
        self.assertEqual(h.count('<li>'), 2)
        self.assertIn('<strong>bold</strong>', h)
        self.assertIn('<em>dim</em>', h)
        self.assertIn('Egy link tétel.', h)
        self.assertIn('&lt;b&gt;tétel&lt;/b&gt; (x)', h)    # a nyers HTML escape-elve

    def test_valodi_ujsor_is_megy(self):
        h = str(blokkok._md_tw('# c\n\nszöveg\n\n* a\n* b'))
        self.assertEqual(h.count('<li>'), 2)
        self.assertIn('<p>szöveg</p>', h)

    def test_ures(self):
        self.assertEqual(str(blokkok._md_tw(None)), '<div class="szoveg gordul"></div>')


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestOlvasoHibakLap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = app_keszit('belso').test_client()

    def get(self, u):
        return self.c.get(u)

    def blokk(self, u, azon):
        t = self.get(u).get_data(as_text=True)
        i = t.index('data-blokk="%s"' % azon)
        return t[i:t.index('</section>', i)]

    def test_tw_blokk_a_lapon_renderelt(self):
        """N-F99a: a H8441 (abomination) szó-lapon a tW-blokkban nincs szó szerinti `\\n`, `#`, `](`, és van lista és fejléc."""
        t = self.get('/r/szo/H8441').get_data(as_text=True)
        if 'data-blokk="szo.tw_h"' not in t:
            self.skipTest('nincs tW-blokk a H8441 lapján')
        b = self.blokk('/r/szo/H8441', 'szo.tw_h')
        self.assertNotIn('\\n', b)
        self.assertNotRegex(b, r'(^|>)\s*#')
        self.assertNotIn('](', b)
        self.assertIn('<h5>', b)
        self.assertIn('<ul class="lista">', b)

    def test_bdb_nyelvtani_jelek_es_szerzok_feloldva(self):
        """N117: a status absolutus/constructus, az SS és a Wetzst a jelmagyarázatban és <abbr>-ban (H7451); a tábla ezeket tartalmazza."""
        for j, cs in (('status absolutus', 'nyelvtani'), ('status constructus', 'nyelvtani'), ('SS', 'szerző'), ('Wetzst', 'szerző')):
            self.assertIn(j, blokkok.BDB_JELEK, j)
            self.assertEqual(blokkok.BDB_JELEK[j][1], cs, j)
            self.assertTrue(blokkok.BDB_JELEK[j][0].strip(), j)
        b = self.blokk('/r/szo/H7451', 'szo.bdb_apparatus')
        feloldott = set(re.findall(r'<dt>([^<]+)</dt>', b[b.index('<dl class="jelmagyarazat">'):b.index('</dl>')]))
        self.assertIn('SS', feloldott)
        self.assertIn('Wetzst', feloldott)
        # a szövegben már nem áll feloldatlanul (<abbr> nélküli) az SS és a Wetzst
        szoveg = b[:b.index('<h4>Jelmagyarázat</h4>')]
        szoveg = re.sub(r'<abbr[^>]*>[^<]*</abbr>', '', szoveg)
        szoveg = re.sub(r'<[^>]+>', ' ', szoveg)
        self.assertIsNone(re.search(r'(?<![\w])(SS|Wetzst)(?![\w])', szoveg), 'feloldatlan jel maradt')

    def test_szo_lap_vers_parameter(self):
        """N118: a `/szo/<strong>?vers=1Moz/1/5` önálló lap a versszerinti BDB-jelölést adja, mint a /r/szo ...?ig=…; csak szigorú alak."""
        u = '/szo/H1242?vers=1Moz/1/5'
        r = self.get(u)
        self.assertEqual(r.status_code, 200)
        t = r.get_data(as_text=True)
        self.assertIn('class="bdb-ebben"', t)
        self.assertIn('a BDB itt idézi ezt a verset', t)
        self.assertRegex(t, r'<li id="bdb-0-1e" data-jel="e\." class="bdb-itt">')
        self.assertIn('data-blokk="szo.ebben"', t)
        # vers nélkül nincs jelölés; érvénytelen vagy nem szigorú alak is figyelmen kívül marad
        for rossz in ('/szo/H1242', '/szo/H1242?vers=nincs/1/5', '/szo/H1242?vers=1Moz/1/5;drop', '/szo/H1242?vers=1Moz/x/5'):
            t2 = self.get(rossz).get_data(as_text=True)
            self.assertNotIn('class="bdb-ebben"', t2, rossz)
        # a jelölés és a gyorsítótár: a két lap nem keveredik
        self.assertNotIn('bdb-itt', self.get('/szo/H1242').get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
