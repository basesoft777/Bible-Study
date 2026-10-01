#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_lekerdez_sir.py -- F28 DT25 (d): a lekerdez.py a régi „Sir”
(Jeremiás siralmai) alakot JSir-álnévként olvassa, így a rögzített
proveniencia (`scope=range:Sir 2:8`, adat/auditok.tsv 169-171. sor)
újrafuttatható, és a TAHOT_kivonat.tsv „Sir” igehelyei is illeszkednek.

    python eszkozok/teszt_lekerdez_sir.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lekerdez as L  # noqa: E402


class SirAlnev(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(L.parse_igehely('Sir 2:8'), ('JSir', 2, 8))
        self.assertEqual(L.parse_igehely('JSir 2:8'), ('JSir', 2, 8))

    def test_to_step(self):
        self.assertEqual(L.to_step('Sir 2:8'), 'Lam.2.8')
        self.assertEqual(L.to_step('JSir 2:8'), 'Lam.2.8')

    def test_step_iranybol_jsir(self):
        self.assertEqual(L.parse_igehely('Lam.2.8'), ('JSir', 2, 8))

    def test_tahot_illeszkedes(self):
        sorok = [r for r in L.load_tahot() if r['_parsed'][:2] == ('JSir', 2)]
        self.assertTrue(sorok, 'a TAHOT Siralmak 2. fejezete JSir-ként olvasandó')

    def test_mas_konyv_valtozatlan(self):
        self.assertEqual(L.parse_igehely('1Móz 3:16'), ('1Móz', 3, 16))


if __name__ == '__main__':
    unittest.main(verbosity=2)
