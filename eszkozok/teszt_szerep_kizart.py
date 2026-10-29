"""Az 1/b. blokk olvasói formájának tesztjei (eszkozok/szerep_kizart.py; ISTENTISZT-001 arany lap, 2026-10-29).

  python -m unittest -q eszkozok.teszt_szerep_kizart
"""
import collections
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import szerep_kizart as SZKZ  # noqa: E402


class TestJelolesOka(unittest.TestCase):
    def test_tsk_szavazattal(self):
        c, t = SZKZ.jeloles_oka('TSK 1Móz 4:26 (Votes=42) | scope=x')
        self.assertEqual(c, 'TSK-ajánlás')
        self.assertEqual(t, 'TSK-ajánlás az 1Móz 4:26 helyről, 42 szavazat')

    def test_tsk_es_karoli(self):
        c, t = SZKZ.jeloles_oka('TSK/Károli-KH Zsolt 99:6')
        self.assertEqual((c, t), ('Károli-kereszthivatkozás', 'TSK- és Károli-kereszthivatkozás a Zsolt 99:6 helyről'))

    def test_gepi_strong_kereses(self):
        c, t = SZKZ.jeloles_oka('scan H7121')
        self.assertEqual((c, t), ('Gépi keresés', 'gépi Strong-keresés: H7121'))

    def test_be_nem_sorolhato_egyeb(self):
        c, t = SZKZ.jeloles_oka('valami más')
        self.assertEqual((c, t), ('Egyéb', 'valami más'))


class TestElutasitasOka(unittest.TestCase):
    def test_mintaszotar_sorrend_es_egyeb(self):
        minta = SZKZ.okok('ISTENTISZT-001')
        self.assertTrue(minta)
        self.assertEqual(SZKZ.elutasitas_oka('passzív szerkezet, K1_passziv', minta),
                         'passzív szerkezet vagy megnevezés (negatív kritérium)')
        self.assertEqual(SZKZ.elutasitas_oka('semmi ilyen', minta), SZKZ.EGYEB_OK)

    def test_nevelo(self):
        self.assertEqual(SZKZ.nevelo('1Krón 16:8'), 'az')
        self.assertEqual(SZKZ.nevelo('Zsolt 99:6'), 'a')
        self.assertEqual(SZKZ.nevelo('Ézs 12:4'), 'az')


class TestBlokkTorzs(unittest.TestCase):
    def test_csoport_labjegyzet_osszesito(self):
        sorok = [
            {'igehely': 'Zsolt 99:6', 'forras_kereses': 'TSK/Károli-KH Zsolt 99:6', 'dontes': 'elutasítva',
             'indoklas': 'semmi ilyen | scope=manual'},
            {'igehely': '1Móz 4:26', 'forras_kereses': 'scan H7121', 'dontes': 'nyitva', 'indoklas': 'kérdés'},
        ]
        tablak, labj, ossz = SZKZ.blokk_torzs(sorok, 'ISTENTISZT-001')
        self.assertEqual(len(labj), 2)
        self.assertIn('[^k1]', ''.join(tablak))
        self.assertEqual(ossz['egyeb'], ['Zsolt 99:6'])
        self.assertEqual(ossz['ok'], collections.Counter({SZKZ.EGYEB_OK: 1, 'nyitott döntés': 1}))
        sor = SZKZ.osszesito_sor(ossz)
        self.assertIn('egyéb 1 (Zsolt 99:6)', sor)
        self.assertIn('**Nyitott döntés:** 1', sor)
        self.assertIn('scope=manual', labj[0])


if __name__ == '__main__':
    unittest.main()
