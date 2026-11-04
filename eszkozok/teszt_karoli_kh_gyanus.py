# -*- coding: utf-8 -*-
"""A Károli-KH gyanús-lista fájl és a szűrő tesztjei (N-F156a)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_kh_gyanus_general as GG  # noqa: E402
import karoli_kh_szuro as SZ  # noqa: E402


class GyanusFajl(unittest.TestCase):
    def test_ismert_masolat_blokk(self):
        lista, _ = GG.osztalyoz()
        d = {k: (o, e, g) for k, o, e, g in lista}
        self.assertEqual(d['Act.2.27'][0], 'blokk')
        self.assertIn('Act.7.14', d['Act.2.27'][2])
        self.assertNotIn('Act.7.14', d)

    def test_hamis_pozitivok_nincsenek_benne(self):
        for k in ('Pro.1.12', '1Ch.20.4', 'Psa.76.3'):
            self.assertNotIn(k, SZ.gyanus_forrasok())

    def test_generalt_fajl_egyezik(self):
        """A repóban lévő fájl a szkript mostani kimenetével azonos forrásvers-halmazt tartalmaz."""
        lista, _ = GG.osztalyoz()
        self.assertEqual({x[0] for x in lista}, SZ.gyanus_forrasok())


if __name__ == '__main__':
    unittest.main()
