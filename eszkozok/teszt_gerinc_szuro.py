#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_gerinc_szuro.py -- F124: a gerinc_szuro.py (a #110 szuro DT283 szabalya)
tesztjei; a valos adaton a naplok/F110_szuro_szimulacio.tsv-vel egyezes.

    python eszkozok/teszt_gerinc_szuro.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerinc_szuro as S  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def tok(*parok):
    return [{'strong': s, 'gloss': g} for s, g in parok]


class HeberSzuro(unittest.TestCase):
    def test_k0_nincs_par(self):
        r = S.heber(tok(('H8034', 'name'), ('H3068', 'LORD')))
        self.assertEqual(r[:2], ('K', 'K0_nincs_par'))

    def test_k1_passziv(self):
        r = S.heber(tok(('H7121', 'was called'), ('H9003', 'by'), ('H8034', 'name')))
        self.assertEqual(r[:2], ('K', 'K1_passziv'))

    def test_k2_nincs_be(self):
        r = S.heber(tok(('H7121', 'he called'), ('H0853', ''), ('H8034', 'name')))
        self.assertEqual(r[:2], ('K', 'K2_nincs_be'))
        self.assertIn('megnevezés', r[2])

    def test_k2_hatareset_jelzes(self):
        r = S.heber(tok(('H7121', 'I called'), ('H8034', 'name'), ('H3068', 'LORD')))
        self.assertEqual(r[1], 'K2_nincs_be')
        self.assertIn('HATÁRESET', r[2])

    def test_a_be_isten(self):
        r = S.heber(tok(('H7121', 'called'), ('H9003', 'on'), ('H8034', 'name'), ('H3068', 'LORD')))
        self.assertEqual(r[:2], ('A', 'A_be_isten'))

    def test_b_be_nem_nevszo(self):
        r = S.heber(tok(('H7121', 'called'), ('H9003', 'on'), ('H8034', 'name'), ('H1234', 'x')))
        self.assertEqual(r[:2], ('B', 'B_be_nem_nevszo'))

    def test_ablakon_kivul_k0(self):
        t = tok(('H7121', 'called')) + tok(*[('H1111', 'x')] * 7) + tok(('H9003', 'in'), ('H8034', 'name'))
        self.assertEqual(S.heber(t)[1], 'K0_nincs_par')

    def test_a_legjobb_par_nyer(self):
        t = tok(('H7121', 'was called'), ('H8034', 'name'), ('H7121', 'called'), ('H9003', 'on'), ('H8034', 'name'),
                ('H3068', 'LORD'))
        self.assertEqual(S.heber(t)[0], 'A')


class GorogSzuro(unittest.TestCase):
    def test_nincs_g1941(self):
        self.assertIsNone(S.gorog(tok(('G2316', 'God'))))

    def test_k1(self):
        self.assertEqual(S.gorog(tok(('G1941', 'is called'), ('G2316', 'God')))[:2], ('K', 'K1_passziv'))

    def test_k3_jogi(self):
        self.assertEqual(S.gorog(tok(('G1941', 'I appeal'), ('G2541', 'Caesar')))[:2], ('K', 'K3_jogi'))

    def test_a_es_b(self):
        self.assertEqual(S.gorog(tok(('G1941', 'calling'), ('G2962', 'Lord')))[:2], ('A', 'A_aktiv_isten'))
        self.assertEqual(S.gorog(tok(('G1941', 'calling'), ('G1111', 'x')))[:2], ('B', 'B_nincs_isten'))


class Szur(unittest.TestCase):
    def test_csak_istentiszt_kap_szurot(self):
        self.assertIsNone(S.szur('MENNY-001', 'H1121', [], []))
        self.assertIsNone(S.szur('ISTENTISZT-001', 'H3548', [], []))
        self.assertIsNotNone(S.szur('ISTENTISZT-001', 'H8034', tok(('H8034', 'n')), []))
        self.assertIsNone(S.szur('ISTENTISZT-001', 'G1941', [], tok(('G2316', 'God'))))


class F110Egyezes(unittest.TestCase):
    """A valos adaton a szimulacio-TSV minden sorat reprodukalja (osztaly + okkod)."""

    def test_szimulacio(self):
        sim = os.path.join(ROOT, 'naplok', 'F110_szuro_szimulacio.tsv')
        if not os.path.exists(sim):
            self.skipTest('nincs szimulacio-TSV')
        import lekerdez as L
        with open(sim, encoding='utf-8') as f:
            sorok = [l.rstrip('\n').split('\t') for l in f if not l.startswith('#')][1:]
        versek = {}
        for nev, rows in (('tahot', L.load_tahot()), ('tagnt', L.load_tagnt())):
            for r in rows:
                versek.setdefault(r['Igehely'], {'tahot': [], 'tagnt': []})[nev].append(
                    {'strong': r['Strong-szám'], 'gloss': r.get('Angol tükörfordítás', '')})
        hiba = []
        for csoport, vers, osztaly, okkod, _ in sorok:
            v = versek[vers]
            r = S.heber(v['tahot']) if csoport.startswith('H') else S.gorog(v['tagnt'])
            if (r[0], r[1]) != (osztaly, okkod):
                hiba.append((vers, r[:2], (osztaly, okkod)))
        self.assertEqual(hiba, [])
        self.assertGreater(len(sorok), 150)


if __name__ == '__main__':
    unittest.main()
