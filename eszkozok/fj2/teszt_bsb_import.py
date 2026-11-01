"""F120 (DT-F120a (a)): a bsb_import Károli -> MT fordításának tesztjei (fixtúrával, a BSB-klón nélkül).

A TAHOT az F85.6 óta Károli-kulcsú; a BSB_Strongs.tsv Igehely-e MT (DT-F41d). A bsb_import a TAHOT-halmazokat a
versmegfeleltető táblán át MT-kulcsra fordítja (karoli_mt, karoli_mt_terkep, tahot_mt_halmazok); az R4 (kk_max) helyett az
oda_vissza() próba igazolja, hogy a sqlite_epit visszaképzése a pontos inverz.
Futtatás: python eszkozok/fj2/teszt_bsb_import.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bsb_import as B  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# (igehely_karoli, igehely_kjv, igehely_mt, osztaly) -- a kk_betolt() alakja
KK = [
    ('Jób 16:22', '16:22', '', 'KJV'),
    ('Jób 17:1', '17:2', '17:2', 'KEZI'),       # KEZI + kitöltött mt (DT-F117e)
    ('Jób 17:2', '17:3', '17:3', 'KEZI'),
    ('Jób 40:1', '40:6', '', 'KEZI'),            # KEZI üres mt-vel: a KJV-pár
    ('Zsolt 13:1', '', '', 'KJV'),              # felirat: a Károli-szám az MT
    ('Zsolt 13:2', '13:1', '', 'KJV'),          # Zsoltár: KJV-osztály, igehely_kjv eltér -> a Károli-szám marad
    ('Jón 2:3', '2:2', '2:3', 'MT'),
    ('1Sám 20:43', '20:42', '21:1', 'KEZI'),    # explicit pár MT 21:1-re
    ('1Sám 21:1', '21:1', '', 'KJV'),           # azonossággal is MT 21:1 -> ütközés, az explicit nyer
]


class KaroliMt(unittest.TestCase):
    def test_szabaly(self):
        self.assertEqual(B.karoli_mt('Jób 17:1', '17:2', '17:2', 'KEZI'), '17:2')
        self.assertEqual(B.karoli_mt('Jób 40:1', '40:6', '', 'KEZI'), '40:6')
        self.assertEqual(B.karoli_mt('Zsolt 13:2', '13:1', '', 'KJV'), '13:2')
        self.assertEqual(B.karoli_mt('Jón 2:3', '2:2', '2:3', 'MT'), '2:3')
        self.assertEqual(B.karoli_mt('Zsolt 13:1', '', '', 'KJV'), '13:1')

    def test_utkozesnel_az_explicit_par_nyer(self):
        terkep, kimaradt = B.karoli_mt_terkep(KK)
        self.assertEqual(terkep[('1Sám', '20:43')], '21:1')
        self.assertNotIn(('1Sám', '21:1'), terkep)
        self.assertEqual(kimaradt, ['1Sám 21:1'])

    def test_explicit_par_nelkuli_utkozesnel_mind_kimarad(self):
        kk = [('A 1:1', '1:2', '', 'KEZI'), ('A 1:2', '1:2', '', 'KJV')]
        terkep, kimaradt = B.karoli_mt_terkep(kk)
        self.assertEqual(terkep, {})
        self.assertEqual(kimaradt, ['A 1:1', 'A 1:2'])


class TahotMt(unittest.TestCase):
    def test_a_tahot_mt_kulcsra_fordul_a_tablan_kivuli_vers_kimarad(self):
        forras = {'Jób 16:22': {1}, 'Jób 17:1': {2}, 'Jób 17:2': {3}, 'Jób 40:1': {4}, 'Zsolt 13:2': {5},
                  '1Sám 20:43': {6}, '1Sám 21:1': {7}, 'Jób 39:1': {8}}
        ki, at, kimaradt = B.tahot_mt_halmazok(forras, KK)
        self.assertEqual(ki, {'Jób 16:22': {1}, 'Jób 17:2': {2}, 'Jób 17:3': {3}, 'Jób 40:6': {4}, 'Zsolt 13:2': {5},
                              '1Sám 21:1': {6}})
        self.assertEqual(at, 4)
        self.assertEqual(kimaradt, ['1Sám 21:1', 'Jób 39:1'])

    def test_a_regi_viselkedes_kettos_kulcsot_adna(self):
        # negatív próba: a fordítás nélkül (az F85.6 utáni Károli-kulcs) a Jób 17:1 tartalma a 17:1 MT-kulcson állna,
        # holott az MT 17:2 -- a fordított halmazban a 17:1 MT-kulcs nem a Károli 17:1 tartalma
        ki, _, _ = B.tahot_mt_halmazok({'Jób 17:1': {2}}, KK)
        self.assertNotIn('Jób 17:1', ki)


class OdaVissza(unittest.TestCase):
    def test_a_fixtura_oda_vissza_hibatlan(self):
        self.assertEqual(B.oda_vissza(KK), [])

    def test_a_valos_tabla_oda_vissza_hibatlan(self):
        self.assertEqual(B.oda_vissza(B.kk_betolt()), [])


if __name__ == '__main__':
    unittest.main()
