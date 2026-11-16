#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_bizonyiteklap.py -- a bizonyítéklap (`eszkozok/bizonyiteklap.py`, F224.5) tesztjei.

Kis, ideiglenes TAHOT-szerű korpuszon (a Károli-kulcsok valódiak: 1Móz 1:1–1:5), hogy a teszt gyors és a valódi
konkordancia változásától független legyen:

1. gyakorisági alapvonal: a versszám és az arány; az együttállás megfigyelt száma és a várt n_A · n_B / N;
2. a fordított sorrendű ismétlés: A … B … B … A jelölt; A B A B nem; két vers között nincs (csak versen belül);
   a véletlen-alapvonal (AABB minden sorrendje közül 2/6);
3. ítélet-mező nincs; láncon átívelő keret-jelölt nincs;
4. a vers állapota: eldöntött (elofordulasok), jelölt döntéssel, nem áll az adatban;
5. proveniencia-sor minden versnél.

Futtatás: python eszkozok/teszt_bizonyiteklap.py
"""
import os
import shutil
import sys
import tempfile
import unittest

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import bizonyiteklap as B  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FEJ = 'Igehely\tStrong-szám\tRagozott alak\tKiejtés\tSzótő\tRövid jelentés\tAngol tükörfordítás\n'
# 1:1: A B B A (fordított ismétlés); 1:2: A B A B (nincs); 1:3: A B; 1:4: B A (a 1:3-mal együtt sem jelölt); 1:5: C
KORPUSZ = [
    ('1Móz 1:1', ['H0001', 'H0002', 'H9999', 'H0002', 'H0001']),
    ('1Móz 1:2', ['H0001', 'H0002', 'H0001', 'H0002']),
    ('1Móz 1:3', ['H0001', 'H0002']),
    ('1Móz 1:4', ['H0002', 'H0001']),
    ('1Móz 1:5', ['H0003']),
]


class Alap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp()
        cls.tahot = os.path.join(cls.d, 'tahot.tsv')
        with open(cls.tahot, 'w', encoding='utf-8', newline='\n') as f:
            f.write(FEJ)
            for vers, strongok in KORPUSZ:
                for s in strongok:
                    f.write('%s\t%s\tal_%s\t-\tto_%s\tgl_%s\t-\n' % (vers, s, s, s, s))
        cls.elof = os.path.join(cls.d, 'elof.tsv')
        with open(cls.elof, 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tigehely\tstrong\n')
            f.write('T-001\t1Móz 1:1\tH0001\n')
            f.write('T-001\t1Móz 1:4-5\tH0002\n')   # tartomány-sor (a független ellenőrzés, 2026-11-16)
        cls.jelolt = os.path.join(cls.d, 'jelolt.tsv')
        with open(cls.jelolt, 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tigehely\tforras_kereses\tdontes\tindoklas\tjelolt_tipus\n')
            f.write('T-001\t1Móz 1:2\tx\tnyitva\ty\telofordulas\n')
        cls.ki = B.keszit('T-001', ['1Móz 1:1', '1Móz 1:2', '1Móz 1:3', '1Móz 1:4', '1Móz 1:5'],
                          ['H0001', 'H0002', 'H0003'], tanulmany='genezis/teszt.md', elof_ut=cls.elof,
                          jelolt_ut=cls.jelolt, tahot=cls.tahot, tagnt=os.path.join(cls.d, 'nincs.tsv'),
                          ts='2026-11-15T00:00Z')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d)

    def vers(self, k):
        r = self.ki.split('### %s ' % k, 1)[1]
        return r.split('\n### ', 1)[0]

    # 1. alapvonal
    def test_alapvonal(self):
        self.assertIn('| H0001 | to_H0001 | 4 | 5 | 0.8000 |', self.ki)
        self.assertIn('| H0003 | to_H0003 | 1 | 5 | 0.2000 |', self.ki)

    def test_egyuttallas_vart(self):
        # H0001 és H0002 4–4 versben, együtt 4-ben; N=5: várt 4·4/5 = 3.20
        self.assertIn('- H0001 + H0002: megfigyelt 4 vers; várt 3.20', self.vers('1Móz 1:1'))

    # 2. fordított ismétlés
    def test_forditott_jelolt(self):
        v = self.vers('1Móz 1:1')
        self.assertIn('Fordított sorrendű ismétlés (gépi jelölt, versen belül): H0001 … H0002 … H0002 … H0001', v)
        self.assertIn('véletlen-alapvonal: 0.333', v)

    def test_forditott_nincs(self):
        self.assertIn('Fordított sorrendű ismétlés: nincs', self.vers('1Móz 1:2'))

    def test_versen_belul(self):
        # az 1:3 (A B) és az 1:4 (B A) együtt ABBA lenne: versen átívelő jelölt nincs
        self.assertIn('Fordított sorrendű ismétlés: nincs', self.vers('1Móz 1:3'))
        self.assertIn('Fordított sorrendű ismétlés: nincs', self.vers('1Móz 1:4'))

    def test_minta_fuggveny(self):
        self.assertEqual(B.forditott_ismetles(['A', 'B', 'B', 'A']), ('A', 'B'))
        self.assertIsNone(B.forditott_ismetles(['A', 'B', 'A', 'B']))
        self.assertIsNone(B.forditott_ismetles(['A', 'A', 'A', 'A']))
        self.assertEqual(B.forditott_alapvonal(['A', 'B', 'B', 'A'])[0], 2 / 6)
        self.assertEqual(B.forditott_alapvonal(['A', 'B'])[0], 0.0)

    # 3. ítélet és keret nincs
    def test_itelet_mezo_nincs(self):
        for sor in self.ki.split('\n'):
            if sor.startswith('|'):
                self.assertNotIn('ítélet', sor.lower())
                self.assertNotIn('erős', sor.lower())
        self.assertNotIn('Keret', self.ki)
        self.assertNotIn('khiazmus', self.ki.lower())

    def test_tanulmany_csak_hivatkozas(self):
        self.assertIn('A tanulmány adata (nem ismétlődik itt): `genezis/teszt.md`.', self.ki)

    # 4. állapot
    def test_allapot(self):
        self.assertIn('### 1Móz 1:1 · eldöntött (adat/elofordulasok.tsv:2)', self.ki)
        self.assertIn('### 1Móz 1:2 · jelölt, döntés: nyitva (nem vehető át)', self.ki)
        self.assertIn('### 1Móz 1:3 · nem áll a motívum adatában (nem vehető át)', self.ki)
        self.assertIn('### 1Móz 1:4 · eldöntött (adat/elofordulasok.tsv:3)', self.ki)   # a tartomány verse
        self.assertIn('### 1Móz 1:5 · eldöntött (adat/elofordulasok.tsv:3)', self.ki)

    # 5. proveniencia
    def test_proveniencia_versenkent(self):
        for k, _ in KORPUSZ:
            self.assertIn('*(proveniencia: scope=%s, lánc:' % k, self.vers(k))

    def test_lanc_szava_nincs(self):
        ki = B.keszit(None, ['1Móz 1:5'], ['H0001'], elof_ut=self.elof, jelolt_ut=self.jelolt, tahot=self.tahot,
                      tagnt=os.path.join(self.d, 'nincs.tsv'), ts='x')
        self.assertIn('A lánc szava nem áll a versben.', ki)
        self.assertIn('*(proveniencia: scope=1Móz 1:5 |', ki)


if __name__ == '__main__':
    unittest.main(verbosity=1)
