"""A kiejtés-szabály szövegszintű tesztjei (eszkozok/kiejtes_szoveg.py; ISTENTISZT-001 arany lap, 2026-10-29).

  python -m unittest -q eszkozok.teszt_kiejtes_szoveg
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kiejtes_szoveg as KSZ  # noqa: E402


class Kiejtes(unittest.TestCase):
    def test_heber_jovahagyott_es_gepi(self):
        self.assertEqual(KSZ.heber_kiejtes('קָרָא'), 'kárá')
        self.assertEqual(KSZ.heber_kiejtes('שֵׁם'), 'sém')
        # DT-F131y (2026-10-30): jóváhagyott alak híján a pontozott szó gépi kiejtése, jelölve
        self.assertEqual(KSZ.heber_kiejtes('שֻׁם'), 'sum, gépi')       # a mássalhangzó-váz azonos, a szó más (H8036)
        self.assertEqual(KSZ.heber_kiejtes('זָכַר'), 'záchar, gépi')
        self.assertIsNone(KSZ.heber_kiejtes('זכר'))                    # pontozatlan, jóváhagyás nélkül: nincs
        self.assertEqual(KSZ.heber_kiejtes('בְּ שֵׁם'), 'besém')
        self.assertEqual(KSZ.heber_kiejtes('קָרָא בְשֵׁם'), 'kárá besém')

    def test_gorog_lemma_es_gepi(self):
        self.assertEqual(KSZ.gorog_kiejtes('καλέω'), 'kaleó')
        self.assertEqual(KSZ.gorog_kiejtes('Κυρίου'), 'küriú')


class Potlas(unittest.TestCase):
    LAP = '\n'.join([
        '## 1. Szakasz',
        '<!-- GENERÁLT-KEZDET: general.py --cel lexikon#X#a | forrás:  | licenc:  | ts=T -->',
        'A καλέω ige és a זָכַר ige.',
        'Megint καλέω.',
        '> idézet: καλέω',
        '<!-- GENERÁLT-VÉGE: lexikon#X#a -->',
        '### Kézi rész',
        'Itt a βοάω kézi.',
    ])

    def test_generalt_potol_kezi_marad(self):
        uj, hiany = KSZ.potol(self.LAP)
        self.assertIn('A καλέω (kaleó) ige', uj)
        self.assertIn('Megint καλέω.', uj)              # a szakaszban nem ismétlendő
        self.assertIn('> idézet: καλέω', uj)             # forrásidézet: nem kell
        self.assertIn('Itt a βοάω kézi.', uj)            # a kézi részt nem írja
        self.assertIn('a זָכַר (záchar, gépi) ige', uj)  # DT-F131y: a gépi héber kiejtés is pótol, jelölve
        self.assertEqual({(h[2], h[3]) for h in hiany}, {('kézi', 'βοάω')})
        self.assertEqual(KSZ.potol(uj)[0], uj)           # idempotens


if __name__ == '__main__':
    unittest.main()
