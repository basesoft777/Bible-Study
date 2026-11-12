"""teszt_f194_szopar.py -- F194 (az ISTENTISZT-001 2. kiadása, az új lapszerkezet): a két kapu a szópáros (formulaikus)
motívumon.

1. `lxx_egyezes_kapu(..., szopar=True)`: a pár minden tagja a motívum minden ószövetségi versében áll, ezért a héber 4.6
   szavankénti mondatai nem összeadódnak, hanem mindegyik a teljes versszámot mondja.
2. `lxx_egyforras_ellenoriz`: a 4.11-sor több lemmát is hordozhat ` · `-tal (1Kir 18:24: βοάω · ἐπικαλέω); a kapu
   mindegyiket a cellában keresi, nem az egész szöveget egy szóként.

Futtatás: python eszkozok/teszt_f194_szopar.py
"""
import os
import sys
import unittest

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)

import lexikon_general as LG  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

OSSZESITES = ('*Összesítés: egyező=13, ugyanaz a szócsalád=2, eltérő=0, nincs újszövetségi pár=0, LXX-minusz=0, '
              'a megfelelő nincs megállapítva=1, versszámozás miatt nem párosítva=0.*')


class Szoparkapu(unittest.TestCase):
    def lap(self, a='16', b='16'):
        return '\n\n'.join([
            'A motívum ószövetségi helyei 16 versre terjednek.',
            'Az x a motívum %s ószövetségi versében áll.' % a, 'Az y a motívum %s ószövetségi versében áll.' % b,
            OSSZESITES])

    def test_szopar_mindket_tag_teljes(self):
        m = LG.lxx_egyezes_kapu(self.lap(), 'X-001', szopar=True)
        self.assertEqual(m['n'], 16)

    def test_szopar_hianyos_tag_bukik(self):
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(b='15'), 'X-001', szopar=True)

    def test_szopar_nelkul_osszeg_marad(self):
        # a nem szópáros motívumon a régi szabály: a szavankénti mondatok összege a versszám
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(), 'X-001')
        self.assertEqual(LG.lxx_egyezes_kapu(self.lap(a='10', b='6'), 'X-001')['szavankent'], 16)


class TobbLemma(unittest.TestCase):
    def setUp(self):
        self.idx = {('1Kir 18:24', 'H7121'): ('βοάω · ἐπικαλέω', '')}
        self.regi = (LG.vh_lxx_index, LG._heber_kulcsszo_strong)
        LG.vh_lxx_index = lambda _mid: self.idx
        LG._heber_kulcsszo_strong = lambda _v, _st: 'KULCS'

    def tearDown(self):
        LG.vh_lxx_index, LG._heber_kulcsszo_strong = self.regi

    def sor(self, gorog):
        return '| 1Kir 18:24 | 3Kir 18:24 | KULCS | %s | egyező | gépi |' % gorog

    def test_mindket_lemma_a_cellaban(self):
        self.assertEqual(LG.lxx_egyforras_ellenoriz('X-001', [self.sor('βοάω · ἐπικαλέω (boaó · epikaleó)')]), [])

    def test_hianyzo_lemma_elter(self):
        self.assertTrue(LG.lxx_egyforras_ellenoriz('X-001', [self.sor('ἐπικαλέω (epikaleó)')]))


if __name__ == '__main__':
    unittest.main()
