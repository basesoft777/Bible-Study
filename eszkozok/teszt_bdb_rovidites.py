"""teszt_bdb_rovidites.py — a BDB egybetűs rövidítéseinek közös jelölője (N-F131x).

Futtatás: python eszkozok/teszt_bdb_rovidites.py
"""
import os
import shutil
import tempfile
import unicodedata
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
        self.assertEqual(BR.atiras_javit('in Sh®°ôl (Sh®°ôl).', 'H11', self.JAV), 'in Sheʾôl (Sheʾôl).')
        # DT-F164a (felhasználó, 2026-11-03): a magyar szövegben „Seól”
        self.assertEqual(BR.atiras_javit('a Sh®°ôlban (Sh®°ôl-ról).', 'H11', self.JAV, magyar=True), 'a Seólban (Seól-ról).')
        self.assertEqual(BR.atiras_javit('a sh®°ôlba', 'H1004', {'H1004': [('sh®°ôl', 'sheʾôl')]}, magyar=True), 'a seólba')
        self.assertEqual(BR.atiras_javit('a Sh®°ôlban', 'H0001', self.JAV), 'a Sh®°ôlban')

    def test_kezi_sorok_h7121_h2416(self):
        """F123.GENKOR (DT-F181a): a betűkészlet többi torz jele kézi `atiras` sorral; magyarul a tár alakja."""
        t = BR.atiras_javitasok()
        self.assertIn(("'†or°¹n", 'Qorʾân'), t.get('H7121', []))
        self.assertIn(('†or°a¹n', 'Qorʾân'), t.get('H7121', []))
        self.assertEqual(BR.atiras_javit("recitálni (a '†or°¹n), a †or°a¹n;", 'H7121', magyar=True),
                         'recitálni (a Korán), a Korán;')
        self.assertEqual(BR.atiras_javit("recite (the '†or°¹n)", 'H7121'), 'recite (the Qorʾân)')
        self.assertEqual(BR.atiras_javit('Leµi felé', 'H2416', magyar=True), 'Lehi felé')

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


class Zarojel(unittest.TestCase):
    """F123.GENKOR (DT-F181a): a digitalizálásban elveszett zárójel kézi `zarojel` sora, angolul és magyarul."""

    def test_h7121(self):
        self.assertEqual(BR.zarojel_javit('b. felolvastatni vö. Qal 4): személytelenül', 'H7121'),
                         'b. felolvastatni (vö. Qal 4): személytelenül')
        self.assertEqual(BR.zarojel_javit('c. megidéztetni (vö. Qal 5: Ézs 31:4', 'H7121'),
                         'c. megidéztetni (vö. Qal 5): Ézs 31:4')
        self.assertEqual(BR.zarojel_javit('c. be summoned (compare Qal 5: Isa 31:4', 'H7121'),
                         'c. be summoned (compare Qal 5): Isa 31:4')
        kesz = 'c. megidéztetni (vö. Qal 5): Ézs 31:4'
        self.assertEqual(BR.zarojel_javit(kesz, 'H7121'), kesz)               # idempotens
        self.assertEqual(BR.zarojel_javit('felolvastatni vö. Qal 4)', 'H0001'), 'felolvastatni vö. Qal 4)')


def nfc(s):
    return unicodedata.normalize('NFC', s)


class Maqqef(unittest.TestCase):
    """F105, DT-F105a: a rafe-maqqéf (U+05BF) feloldása a megjelenítésben."""

    def test_masodik_szo_elso_betuje(self):
        self.assertEqual(nfc(BR.maqqef_javit('מִןהָֿאָרֶץ')), nfc('מִן־הָאָרֶץ'))
        self.assertEqual(nfc(BR.maqqef_javit('לֹאתִֿתֵּן')), nfc('לֹא־תִתֵּן'))

    def test_mater_betus_szokezdet(self):
        # a magánhangzót a következő mater-betű hordozza: a szóhatár akkor is a rafét hordozó betű előtt
        self.assertEqual(nfc(BR.maqqef_javit('קְצַררֿוּחַ')), nfc('קְצַר־רוּחַ'))

    def test_vegbetu_a_szohatar_utana(self):
        self.assertEqual(nfc(BR.maqqef_javit('עִםֿ הַחֲמוֺר')), nfc('עִם־הַחֲמוֺר'))

    def test_elozo_betu_vegbetu_alakra(self):
        self.assertEqual(nfc(BR.maqqef_javit('עִמהַֿחֲמוֺר')), nfc('עִם־הַחֲמוֺר'))

    def test_rovidites(self):
        self.assertEqual(nfc(BR.maqqef_javit('ב׳צֿ׳')), nfc('ב׳־צ׳'))

    def test_valtozatlan_es_idempotens(self):
        for sz in ('אֶזְרַח הָאָרֶץ', 'Gen 1:1', '', 'הָֿ'):
            self.assertEqual(BR.maqqef_javit(sz), sz)
        egyszer = BR.maqqef_javit('מִןהָֿאָרֶץ')
        self.assertEqual(BR.maqqef_javit(egyszer), egyszer)

    def test_a_sorrend_cserevel_egy_lepes(self):
        # a megjelenítés egyetlen héber lépése: javítás nélküli Strongnál is feloldja
        self.assertEqual(nfc(BR.heber_sorrend_javit('a מִןהָֿאָרֶץ b', 'H0001', {})), nfc('a מִן־הָאָרֶץ b'))


class HivatkozottVers(unittest.TestCase):
    """F105, DT-F105a: a hivatkozott-vers-próba (heber_sorrend.Biblia.van_versben, itelet_versen) egy kis TAHOT-on."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdb_jelolt'))
        import heber_sorrend as HS
        cls.HS = HS
        cls.tmp = tempfile.mkdtemp()
        ut = os.path.join(cls.tmp, 'tahot.tsv')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('Igehely\tStrong-szám\tRagozott alak\n')
            for vers, szo in (('Péld 17:18', 'אָדָם'), ('Péld 17:18', 'חֲסַר'), ('Péld 17:18', 'לֵב'),
                              ('Sir 4:7', 'חֲלָבִים'), ('Sir 4:7', 'אָדָם')):
                f.write('%s\tH0000\t%s\n' % (vers, szo))
        cls.bib = HS.Biblia(ut)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_hivatkozott_vers_dont(self):
        js, uj = 'ח לֵֿב׳אָדָם', 'אָדָם ח׳לֵֿב'
        self.assertEqual(self.HS.itelet_versen(self.bib, js, uj, 'Péld 17:18'), 'helyes')

    def test_masik_vers_nem_igazol(self):
        self.assertEqual(self.HS.itelet_versen(self.bib, 'ח לֵֿב׳אָדָם', 'אָדָם ח׳לֵֿב', 'Sir 4:7'), 'eldonthetetlen')

    def test_nincs_vers(self):
        self.assertIsNone(self.bib.van_versben('אָדָם לֵב', 'Jób 1:1'))


class HeberSorrendF105Tabla(unittest.TestCase):
    """A generált tábla F105-sorai: a hivatkozott-vers-próbával javított és a két kézi sor betöltődik és cserél."""

    def test_hivatkozott_vers_sorok(self):
        n = 0
        with open(BR.JAVITAS_UT, encoding='utf-8') as f:
            for s in f:
                m = s.rstrip('\n').split('\t')
                if len(m) > 10 and m[3] == 'heber_sorrend' and m[8] == 'javitva' and 'hivatkozott-vers-próba' in m[10]:
                    n += 1
        self.assertGreaterEqual(n, 1800)

    def test_h1245_amos_8_12(self):
        self.assertEqual(BR.heber_sorrend_javit('י ׳דבר Amos 8:12', 'H1245'), 'דבר י׳ Amos 8:12')

    def test_ket_kezi_sor(self):
        # a megjelenítés a forrás pontos alakját cseréli: a forrásalak a táblából (NFC szerint azonosítva)
        for st, forras, vart in (('H2638', 'ח לֵֿב׳אָדָם', 'אָדָם ח׳־לֵב'), ('H3801', 'קֹדֶשׁ׳כּ בַּֿד', 'כּ׳־בַּד קֹדֶשׁ')):
            alak = next(a for a, _u in BR.sorrend_javitasok().get(st, []) if nfc(a) == nfc(forras))
            self.assertEqual(nfc(BR.heber_sorrend_javit(alak, st)), nfc(vart))


if __name__ == '__main__':
    unittest.main()
