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


class K2FoSzabaly(unittest.TestCase):
    """DT-F140b K2/K5: a fo a TAHOT-tobbseggel egyezo glosszaju sor; istennevek a K5-lista szerint."""

    @classmethod
    def setUpClass(cls):
        cls.al = {}
        for s in g.tbesh_sorok():
            cls.al.setdefault(s['alap'], []).append(s)
        cls.tb = g.tahot_tobbseg()

    def fo(self, h):
        return g.fo_jelolt(self.al[h], self.tb)['entry_id']

    def test_a_2_2_szabaly_hibai_javitva(self):
        self.assertEqual(self.fo('H6213'), 'H6213H')   # "to make" (nem "to press")
        self.assertEqual(self.fo('H1004'), 'H1004B')   # "house" (nem "place")
        self.assertEqual(self.fo('H5892'), 'H5892B')   # "city" (nem "excitement")
        self.assertEqual(self.fo('H7451'), 'H7451C')
        self.assertEqual(self.fo('H4057'), 'H4057B')   # "wilderness" (nem "mouth")
        self.assertEqual(self.fo('H5483'), 'H5483M')   # "horse"

    def test_k5_istennevek(self):
        for h, e in [('H3068', 'H3068G'), ('H0430', 'H0430G'), ('H0410', 'H0410K'),
                     ('H5945', 'H5945B'), ('H6635', 'H6635B'), ('H0136', 'H0136'),
                     ('H3050', 'H3050'), ('H7706', 'H7706'), ('H1180', 'H1180')]:
            self.assertEqual(self.fo(h), e)

    def test_nem_illesztheto_heurisztika(self):
        # tobbseg nelkul a 2.2 heurisztika
        self.assertEqual(g.fo_jelolt(self.al['H1588']) ['entry_id'], g.fo_heurisztika(self.al['H1588'])['entry_id'])

    def test_strongonkent_egy_fo(self):
        fo = {}
        for h, v in self.al.items():
            if h in ('H9015', 'H9016', 'H9017', 'H9018', 'H9019'):
                continue
            fo[h] = g.fo_jelolt(v, self.tb)['entry_id']
        # TBESH-sajatossag: a H7178 alatt van egy H7156H entry_id (Kartan)
        self.assertEqual([h for h, e in fo.items() if not e.startswith(h)], ['H7178'])
        self.assertEqual(len(fo), 8718)

    def test_fix_istennevek_kapu(self):
        for eid, (hu, megj) in g.ISTENNEV_FIX.items():
            self.assertEqual(g.kapuk({'glossza': 'God'}, hu), [], eid)

    def test_kettospont_kapu(self):
        self.assertTrue(g.kapuk(sor('house: home'), 'ház otthon'))
        self.assertEqual(g.kapuk(sor('house: home'), 'ház: otthon'), [])



if __name__ == '__main__':
    unittest.main()
