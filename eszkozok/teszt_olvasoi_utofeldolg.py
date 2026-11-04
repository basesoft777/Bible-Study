"""Az olvasói szöveg utófeldolgozásának tesztjei (eszkozok/olvasoi_utofeldolg.py; olvasói kapu, 2026-11-02).

  python eszkozok/teszt_olvasoi_utofeldolg.py
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olvasoi_utofeldolg as OU  # noqa: E402


class TestIdezojel(unittest.TestCase):
    def test_parok(self):
        self.assertEqual(OU.idezojel_sor('Illés: "hívjátok segítségül" — és "ő" hív.'),
                         'Illés: „hívjátok segítségül” — és „ő” hív.')

    def test_zarojel_es_kiemeles_utan(self):
        self.assertEqual(OU.idezojel_sor('(a "név") és *"kiemelt"* szó'), '(a „név”) és *„kiemelt”* szó')

    def test_kod_html_link_proveniencia_erintetlen(self):
        s = ('`x="y"` <a id="k1"></a> [lap](a "b.md") https://x.hu/?q="a" | scope=manual | forras="t" | ts=2026-11-02 '
             'és "ez"')
        ki = OU.idezojel_sor(s)
        self.assertIn('`x="y"`', ki)
        self.assertIn('<a id="k1">', ki)
        self.assertIn('https://x.hu/?q="a"', ki)
        self.assertIn('forras="t"', ki)
        self.assertTrue(ki.endswith('és „ez”'))

    def test_nincs_egyenes_marad_valtozatlan(self):
        s = 'már „helyes” szöveg'
        self.assertEqual(OU.idezojel_sor(s), s)


class TestKonyv(unittest.TestCase):
    def test_magyar_alakra(self):
        self.assertEqual(OU.konyv_sor('l. Zef 3:9, Csel 2:21, Ésa 53:10 és Ám 9:12'),
                         'l. Sof 3:9, ApCsel 2:21, Ézs 53:10 és Ámós 9:12')
        self.assertEqual(OU.konyv_sor('Mát 4:13; Ezék 16:36; Lk 1:59; 1Jn 3:1; Gen 6:12'),
                         'Mt 4:13; Ez 16:36; Luk 1:59; 1Ján 3:1; 1Móz 6:12')

    def test_magyar_alak_marad(self):
        s = '1Móz 3:16, Mt 24:38, Zsolt 14:2, ApCsel 2:21, Ézs 53:10'
        self.assertEqual(OU.konyv_sor(s), s)

    def test_angol_idezett_sor_marad(self):
        s = 'and the Lord said that Mat 11:23 was spoken of the city in which it was done'
        self.assertEqual(OU.konyv_sor(s), s)

    def test_szotar_alakot_szo_szerint_idezo_marad(self):
        s = 'a BDB-ben: „Gen 3:14” áll'
        self.assertEqual(OU.konyv_sor(s), s)

    def test_kod_marad_link_felirata_csere_cel_marad(self):
        s = '`Csel 2:21` és [Csel 2:21](Csel_2:21.md)'
        self.assertEqual(OU.konyv_sor(s), '`Csel 2:21` és [ApCsel 2:21](Csel_2:21.md)')


class TestBdb(unittest.TestCase):
    def test_felso_index_jele(self):
        self.assertEqual(OU.bdb_sor('(Ges^§ 48d Nes^Marg. 15) és Kö^ii. 1. 512'),
                         '(Ges § 48d Nes Marg. 15) és Kö ii. 1. 512')

    def test_labjegyzet_jel_marad(self):
        self.assertEqual(OU.bdb_sor('szöveg[^k12] és [^m3]'), 'szöveg[^k12] és [^m3]')

    def test_dupla_vessszo_es_rafe(self):
        self.assertEqual(OU.bdb_sor('ᾅδης,, ὁ'), 'ᾅδης, ὁ')
        self.assertEqual(OU.bdb_sor('שֶׁםֿ 1Sám'), 'שֶׁם 1Sám')

    def test_torz_atiras_nem_talalgat(self):
        self.assertEqual(OU.bdb_sor('She®°ôl'), 'She®°ôl')


class TestStrong(unittest.TestCase):
    """F123.INDOKLAS: a szó és a kiejtése mellett álló Strong-szám kikerül az olvasói szövegből."""

    def test_zarojel_a_szo_utan(self):
        self.assertEqual(OU.strong_ki('a versben ἐπικαλέομαι áll, de ὄνομα (G3686) nélkül'),
                         'a versben ἐπικαλέομαι áll, de ὄνομα nélkül')

    def test_zarojelben_a_kiejtes_mellett(self):
        self.assertEqual(OU.strong_ki('ἐπεκαλέσατο (epekaleszato) (ἐπικαλέω, epikaleó G1941)'),
                         'ἐπεκαλέσατο (epekaleszato) (ἐπικαλέω, epikaleó)')
        self.assertEqual(OU.strong_ki('A תְּהוֹם (tehóm, H8415) lexéma'), 'A תְּהוֹם (tehóm) lexéma')
        self.assertEqual(OU.strong_ki('a מָלֵא (*málé*, H4390, "megtelni") ige'), 'a מָלֵא (*málé*, "megtelni") ige')

    def test_a_szo_elott(self):
        self.assertEqual(OU.strong_ki('a rokon H6089 עֶצֶב szót'), 'a rokon עֶצֶב szót')

    def test_szo_nelkul_es_lancban_marad(self):
        for s in ('a H7496/H7497 Strong-szám szerinti megoszlás', 'a kárá (H7121) és a sém (H8034)',
                  'nem tartalmazza a H7121+H8034 / ἐπικαλέομαι formulát',
                  'TAHOT וְאֵין קוֹרֵא בְשִׁמְךָ (H0369 + H7121 + H9003 + H8034, 2. sz. birtokos rag)',
                  '(TAHOT: קֹרְאֵי שְׁמוֹ, H7121+H8034; a versben H6030 is)',
                  'nem JHVH (H3068) áll'):
            self.assertEqual(OU.strong_ki(s), s, s)

    def test_tabla_strong_oszlop_es_cim_marad(self):
        szoveg = ('## 1. Előfordulások\n\n<!-- GENERÁLT-KEZDET: x -->\n| Szó | Kiejtés | Strong | Indoklás |\n'
                  '|---|---|---|---|\n| שֵׁם | sém | H8034 | a שֵׁם (sém, H8034) szó |\n\n'
                  '### H5303 — נְפִלִים (ne.phil)\n<!-- GENERÁLT-VÉGE: x -->\n')
        ki = OU.alkalmaz(szoveg)
        self.assertIn('| שֵׁם | sém | H8034 | a שֵׁם (sém) szó |', ki)
        self.assertIn('### H5303 — נְפִלִים (ne.phil)', ki)
        self.assertEqual(OU.strong_valtozas(ki), [])

    def test_kezi_resz_erintetlen_de_jelzett(self):
        """DT569: a kézi részt a generátor nem írja; a kapu mérője jelzi (generált-e = False)."""
        szoveg = '## 6. Értelmezés *(kézi)*\n\nAz „oltár” (מִזְבֵּחַ, mizbéah, H4196) négy helyen áll.\n'
        self.assertEqual(OU.alkalmaz(szoveg), szoveg)
        v = OU.strong_valtozas(szoveg)
        self.assertEqual(len(v), 1)
        self.assertFalse(v[0][3])

    def test_kod_es_proveniencia_erintetlen(self):
        s = '`ὄνομα (G3686)` | scope=manual | forras=x (ὄνομα, G3686) | ts=2026-11-04'
        self.assertEqual(OU.strong_ki(s), s)


class TestAlkalmaz(unittest.TestCase):
    def test_hatarok(self):
        szoveg = '\n'.join([
            '# Cím', '', 'Szó "egy" és Zef 3:9.',
            '> "idézetblokk" Zef 3:9',
            '<!-- "komment" Zef 3:9 -->',
            '```', '"kód" Zef 3:9', '```',
            '[^k1]: forrás: `x` · "nyers" Zef 3:9',
            '## Kolofon', '"kolofon" Zef 3:9'])
        ki = OU.alkalmaz(szoveg).split('\n')
        self.assertEqual(ki[2], 'Szó „egy” és Sof 3:9.')
        self.assertEqual(ki[3], '> "idézetblokk" Zef 3:9')
        self.assertEqual(OU.alkalmaz('> Ges^§ 48d "x" Zef 3:9'), '> Ges § 48d "x" Zef 3:9')
        self.assertEqual(ki[4], '<!-- "komment" Zef 3:9 -->')
        self.assertEqual(ki[6], '"kód" Zef 3:9')
        self.assertEqual(ki[8], '[^k1]: forrás: `x` · "nyers" Zef 3:9')
        self.assertEqual(ki[10], '"kolofon" Zef 3:9')

    def test_idempotens(self):
        szoveg = 'Szó "egy" és Zef 3:9, Csel 2:21.\n'
        egyszer = OU.alkalmaz(szoveg)
        self.assertEqual(OU.alkalmaz(egyszer), egyszer)


if __name__ == '__main__':
    unittest.main()
