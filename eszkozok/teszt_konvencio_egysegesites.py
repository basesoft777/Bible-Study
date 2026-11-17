#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A konvenció-egységesítés (1.1) tesztjei: eszkozok/karoli_strong/konvencio_egysegesites.py (DT-F175vr).

A szabály egységtesztjei (névmáslista, a „ki” és az önálló „az” szűrője, ʾet) gyorsak; a teljes adaton futó teszt az
1.1-et ideiglenes könyvtárba (a repón kívülre) állítja elő, és ellenőrzi: 1.1 ⊂ 1.0, a megmaradó sorok bájtra
azonosak, minden megmaradó névelő-pár megfelel a szabálynak, 0 ʾet-pár, az 1.1-re futtatva a törlőlista üres
(idempotens), és két futás törlőlista-hash-e azonos.

Futtatás: python eszkozok/teszt_konvencio_egysegesites.py  (a teljes adaton ~1–2 perc; `--gyors`: csak egységteszt)
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong'))
import konvencio_egysegesites as K  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYORS = '--gyors' in sys.argv
if GYORS:
    sys.argv.remove('--gyors')


class Szabaly(unittest.TestCase):
    def d(self, strong, szo, elozo=None, kov='x', koztes=' '):
        return K.dontes(strong, szo, elozo, kov, koztes)

    def test_et_mindig_torlodik(self):
        for w in ('azt', 'őt', 'őket', 'urat'):
            self.assertEqual(self.d('H0853', w), (None, 'et'))

    def test_nevmas_marad(self):
        for w in ('kik', 'kinek', 'mely', 'melyek', 'mi', 'e', 'ez', 'ezt', 'azok', 'annak', 'ama', 'ő', 'őket',
                  'valaki', 'némelyek', 'ugyanazon', 'Kik'):
            self.assertEqual(self.d('H9009', w)[0], 'nevmas', w)
            self.assertEqual(self.d('G3588', w)[0], 'nevmas', w)

    def test_nem_nevmas_torlodik(self):
        for w in ('ma', 'mai', 'óh', 'oh', 'ó', 'hogy', 'közül', 'való', 'most', 'másnap', 'mikor', 'mint',
                  'istennek', 'föld', 'é', 'azért', 'ezért'):
            self.assertEqual(self.d('H9009', w), (None, 'nem_nevmas'), w)

    def test_ki_csak_a_utan(self):
        self.assertEqual(self.d('G3588', 'ki', elozo='a'), ('nevmas', None))
        self.assertEqual(self.d('G3588', 'ki', elozo='A'), ('nevmas', None))
        self.assertEqual(self.d('G3588', 'ki', elozo='mene'), (None, 'ki_a_nelkul'))
        self.assertEqual(self.d('G3588', 'ki', elozo=None), (None, 'ki_a_nelkul'))
        self.assertEqual(self.d('G3588', 'kik', elozo='mene')[0], 'nevmas')

    def test_a_vonatkozo(self):
        for k in ('ki', 'kik', 'mely', 'melyben', 'mi', 'mit'):
            self.assertEqual(self.d('H9009', 'a', kov=k), ('a_vonatkozo', None), k)
        self.assertEqual(self.d('H9009', 'a', kov='föld'), (None, 'nem_nevmas'))
        self.assertEqual(self.d('H9009', 'a', kov=None), (None, 'nem_nevmas'))

    def test_onallo_az(self):
        self.assertEqual(self.d('G3588', 'az', kov=None, koztes=''), ('az_versveg', None))
        self.assertEqual(self.d('G3588', 'az', kov='Isten', koztes=', '), ('az_irasjel_elott', None))
        self.assertEqual(self.d('G3588', 'az', kov='a'), ('az_nevelo_elott', None))
        self.assertEqual(self.d('G3588', 'az', kov='az'), ('az_nevelo_elott', None))
        self.assertEqual(self.d('G3588', 'az', kov='király'), ('az_massalhangzo_elott', None))
        for k in ('Isten', 'ember', 'Úr', 'ő', 'üdvösség', 'Ábrahám'):
            self.assertEqual(self.d('G3588', 'az', kov=k), (None, 'az_maganhangzo_elott'), k)

    def test_lista_nem_tartalmaz_hatarozoszot(self):
        for w in ('ma', 'mai', 'most', 'akkor', 'itt', 'ott', 'azért', 'ezért', 'mikor', 'hol', 'óh'):
            self.assertNotIn(w, K.NEVMAS, w)


@unittest.skipIf(GYORS, 'a teljes adaton futó teszt kihagyva (--gyors)')
class TeljesAdat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='konvencio11_')
        cls.hibak = K.general(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_ellenorzes_hibatlan(self):
        # részhalmaz, bájtra azonos sorok, a szabály az 1.1-en, 0 ʾet, a szótábla konzisztens
        self.assertEqual(self.hibak, 0)

    def test_idempotens(self):
        torol, _ = K.torlolista(self.tmp)
        self.assertEqual(torol, [])

    def test_nincs_et_par(self):
        _, megtart = K.torlolista(self.tmp)
        self.assertFalse([s for s in megtart if s[5] == K.ET])
        # minden megmaradó névelő-pár magyar szava a listán van, vagy a két minta („a” + vonatkozó, önálló „az”) egyike
        for s in megtart:
            w = s[2].lower()
            self.assertTrue(w in K.NEVMAS or (w == 'a' and s[8].lower() in K.VONATKOZO) or w == 'az', s)

    def test_hash_ismetelve_azonos(self):
        self.assertEqual(K.torlolista_hash(), K.torlolista_hash())


if __name__ == '__main__':
    unittest.main(verbosity=1)
