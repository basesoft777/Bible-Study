#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_lapdiff_blokk.py -- F203 (N-F184a): a blokkszintű lapdiff (DT665 (b)) és a Feed 9. kapujának kivétele.

    python eszkozok/teszt_lapdiff_blokk.py
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lapdiff_blokk as LB  # noqa: E402


def blokk(nev, tartalom, ts='2026-11-10'):
    return ('<!-- GENERÁLT-KEZDET: general.py --cel lexikon#X-001#%s | forrás: a | licenc: b | ts=%s -->\n%s\n'
            '<!-- GENERÁLT-VÉGE: lexikon#X-001#%s -->' % (nev, ts, tartalom, nev))


def lap(proza='A próza.', szotar='BDB 1. jelentés', kh='Ter 3:17', kolofon='1. kiadás', elof='Ter 3:17 — átok', ts='2026-11-10'):
    return '\n'.join(['<!-- GENERÁLT: general.py --cel lexikon | rések: motivumok/X-001.md -->', '# X-001', '',
                      '## Kivonat', proza, '', '## 2. Előfordulások', blokk('elofordulasok', elof, ts), '',
                      '## 4. Szótári háttér', blokk('szocikkek', szotar, ts), '', '## 6. Kereszthivatkozások',
                      blokk('kereszthivatkozasok', kh, ts), '', '## 10. Értelmezés', 'Értelmező szöveg.', '',
                      '## Kolofon', blokk('kolofon', kolofon, ts), ''])


class Blokkok(unittest.TestCase):
    def test_blokknevek(self):
        b = LB.blokkok(lap())
        self.assertEqual([n for n in b], ['kivul:fej', 'kivul:Kivonat', 'kivul:2. Előfordulások', 'elofordulasok',
                                          'kivul:4. Szótári háttér', 'szocikkek', 'kivul:6. Kereszthivatkozások',
                                          'kereszthivatkozasok', 'kivul:10. Értelmezés', 'kivul:Kolofon', 'kolofon'])

    def test_csak_ts_valtozik_nincs_valtozas(self):
        self.assertEqual(LB.valtozott_blokkok(lap(), lap(ts='2026-11-11')), [])
        self.assertEqual(LB.dt665_b(lap(), lap(ts='2026-11-11'))[0], True)

    def test_szotari_es_kh_valtozas_teljesul(self):
        ok, v, tilos = LB.dt665_b(lap(), lap(szotar='BDB 1. jelentés, javítva', kh='Ter 3:17; 5:29', kolofon='1. kiadás; forrásjavítás'))
        self.assertTrue(ok)
        self.assertEqual(v, ['szocikkek', 'kereszthivatkozasok', 'kolofon'])
        self.assertEqual(tilos, [])

    def test_proza_valtozas_nem_teljesul(self):
        ok, v, tilos = LB.dt665_b(lap(), lap(proza='Más próza.', szotar='BDB új'))
        self.assertFalse(ok)
        self.assertEqual(tilos, ['kivul:Kivonat'])

    def test_elofordulas_valtozas_nem_teljesul(self):
        self.assertEqual(LB.dt665_b(lap(), lap(elof='Ter 3:17 — átok; Ter 5:29'))[2], ['elofordulasok'])

    def test_crlf_nem_szamit(self):
        self.assertEqual(LB.valtozott_blokkok(lap(), lap().replace('\n', '\r\n')), [])


class Kapu9(unittest.TestCase):
    """A Feed 9. kapuja (muhely_allapot.vizualis_atnezes) a DT665 kivételével."""

    def setUp(self):
        import muhely_allapot as M
        self.M = M
        self.eredeti = (M.lap_commit, M.tsv, LB.atnezes_dt665, M.os.path.exists)
        M.lap_commit = lambda m: 'b' * 40
        M.tsv = lambda ut: [{'id': 'X-001', 'lap_commit': 'aaaaaaa', 'datum': '2026.11.04', 'ki': 'felhasználó', 'idezet': 'jó'},
                            {'id': 'X-001', 'lap_commit': 'ccccccc', 'datum': '2026.11.05', 'ki': 'claude-opus-5-5', 'idezet': 'jó'}]
        M.os.path.exists = lambda p: True

    def tearDown(self):
        self.M.lap_commit, self.M.tsv, LB.atnezes_dt665, self.M.os.path.exists = self.eredeti

    def test_dt665_szerint_ervenyes(self):
        LB.atnezes_dt665 = lambda m, a, b, g=None: {'ervenyes': True, 'valtozott': ['szocikkek'], 'tilos': [], 'kolofon': False,
                                                     'ok': 'csak generált szótári/KH blokk változott: szocikkek'}
        s = self.M.vizualis_atnezes('X-001')
        self.assertEqual(s['lap_commit'], 'aaaaaaa')
        self.assertTrue(s['dt665']['ervenyes'])

    def test_mas_blokk_valtozasa_ervenytelenit(self):
        LB.atnezes_dt665 = lambda m, a, b, g=None: {'ervenyes': False, 'valtozott': ['kivul:Kivonat'], 'tilos': ['kivul:Kivonat'],
                                                     'kolofon': False, 'ok': 'nem szótári/KH blokk is változott: kivul:Kivonat'}
        self.assertIsNone(self.M.vizualis_atnezes('X-001'))

    def test_nem_felhasznaloi_sor_nem_szamit(self):
        hivott = []

        def dt(m, a, b, g=None):
            hivott.append(a)
            return {'ervenyes': True, 'valtozott': [], 'tilos': [], 'kolofon': False, 'ok': ''}
        LB.atnezes_dt665 = dt
        self.M.vizualis_atnezes('X-001')
        self.assertNotIn('ccccccc', hivott)


class Valos(unittest.TestCase):
    def test_hamart_kolofon_valtozasa(self):
        # a git-történetből: a HAMART-001 520ae8ec → 7aadf8e6 változásában csak a kolofon változott (DT665 (b) teljesül)
        regi, uj = LB.lap_valtozat('HAMART-001', '520ae8ec'), LB.lap_valtozat('HAMART-001', '7aadf8e6')
        if regi is None or uj is None:
            self.skipTest('a git-történet nem elérhető (sekély klón)')
        self.assertEqual(LB.dt665_b(regi, uj), (True, ['kolofon'], []))


if __name__ == '__main__':
    unittest.main(verbosity=1)
