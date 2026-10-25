#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eszkozok/teszt_glossza_forditas.py -- F140 M0: a sor-valasztas es a kapuk tesztje."""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossza_forditas as g  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def sor(glossza='camel', szofaj='H:N', kapcsolat=''):
    return {'glossza': glossza, 'szofaj': szofaj, 'kapcsolat': kapcsolat, 'definicio': '', 'entry_id': 'H0000'}


class Kapuk(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(g.kapuk(sor(), 'teve'), [])
        self.assertEqual(g.kapuk(sor('Ammi', 'H:N-M'), 'Ammi'), [])

    def test_ures(self):
        self.assertEqual(g.kapuk(sor(), '  '), ['ures'])

    def test_heber(self):
        self.assertTrue(g.kapuk(sor(), 'teve אב'))

    def test_angol(self):
        self.assertTrue(g.kapuk(sor(), 'the teve'))
        self.assertTrue(g.kapuk(sor('father'), 'father'))

    def test_hossz(self):
        self.assertTrue(g.kapuk(sor(), 'egy kettő három négy öt hat hét nyolc'))

    def test_tiltott_jel(self):
        self.assertTrue(g.kapuk(sor(), 'teve?'))


class Valasztas(unittest.TestCase):
    def test_fo_es_homonima(self):
        v = [dict(sor(), entry_id='H1A'), dict(sor(), entry_id='H1B'),
             dict(sor(kapcsolat='a Meaning of'), entry_id='H1G')]
        f, k = g.valaszt(v)
        self.assertEqual([s['entry_id'] for s in f], ['H1A', 'H1B'])
        self.assertEqual([s['entry_id'] for s in k], ['H1G'])

    def test_fallback_gyenge_utan(self):
        v = [dict(sor(kapcsolat='a Part of'), entry_id='X1'), dict(sor(kapcsolat='a Name of'), entry_id='X2')]
        self.assertEqual(g.valaszt(v)[0][0]['entry_id'], 'X2')

    def test_valos_adat(self):
        al = {}
        for s in g.tbesh_sorok():
            al.setdefault(s['alap'], []).append(s)
        self.assertEqual(g.fo_jelolt(al['H0430'])['entry_id'], 'H0430G')
        self.assertEqual(g.fo_jelolt(al['H0410'])['entry_id'], 'H0410K')
        self.assertEqual([s['entry_id'] for s in g.valaszt(al['H2763'])[0]], ['H2763A', 'H2763B'])


if __name__ == '__main__':
    unittest.main()
