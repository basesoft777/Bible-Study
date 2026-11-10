#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_teher_meres.py -- F188 T0: a `teher_meres.py` tiszta függvényeinek tesztjei
(hálózat és git nélkül; a `gh`-hívó rész nem tesztelt, az a mérés futtatásakor
„nem mért” jelöléssel jelzi a hibát).

Futtatás a repó gyökeréből:
    python eszkozok/ellenorzes/tesztek/test_teher_meres.py
"""

import os
import sys
import unittest

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_ITT))

import teher_meres as T  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class AdminTeszt(unittest.TestCase):
    def test_admin_fajlok(self):
        for ut in ('naplok/F188_jelentes.md', 'dontesek/uj/f188-x.md', 'nyitott/uj/f188-x.md',
                   'F188_TEHER_CSOKKENTES_BRIEF.md', 'NYITOTT_FELADATOK.md', 'FELADATOK.md', 'DONTESEK.md',
                   'naplok\\ELLENOR_F188.md'):
            self.assertTrue(T.admin_e(ut), ut)

    def test_tartalmi_fajlok(self):
        for ut in ('adat/elofordulasok.tsv', 'eszkozok/ellenorzes/szabalyok.py', 'MUNKAMENET.md',
                   'lexikon/HAMART-001_TUDOMANYOS.md', 'BRIEF_SABLON.md', 'sablonok/BRIEF_minta.md.txt'):
            self.assertFalse(T.admin_e(ut), ut)

    def test_szamlalas(self):
        self.assertEqual(T.fajlok_szama(['naplok/a.md', 'adat/b.tsv', 'X_BRIEF.md']), (2, 1))


class JavitokorTeszt(unittest.TestCase):
    def test_ellenor_fajl_sorszam(self):
        fajlok = ['naplok/ELLENOR_F184.md', 'naplok/ELLENOR_F184_2.md', 'naplok/ELLENOR_F184_3.md']
        self.assertEqual(T.javitokor(fajlok, []), (2, 'ELLENOR-fájl'))

    def test_valasz_nem_szamit(self):
        self.assertEqual(T.javitokor(['naplok/ELLENOR_F115_2_valasz.md'], [])[0], 0)

    def test_kor_jelolo(self):
        commitok = [{'cim': 'F181.9: fejléc — Te: [elteres_kor 2/2] /elteres 181', 'fajlok': []},
                    {'cim': 'F184.25: a javítókör 2/2 fejléce', 'fajlok': []}]
        self.assertEqual(T.javitokor([], commitok)[0], 2)

    def test_uj_jelentes_commit(self):
        commitok = [{'cim': 'F190.4: ellenőri jelentés (1. ellenőrzés: ELTÉRÉS, 2 tétel)', 'fajlok': None},
                    {'cim': 'F190.6: ellenőri jelentés (2. ellenőrzés: TISZTA)', 'fajlok': None}]
        self.assertEqual(T.javitokor([], commitok), (1, 'ellenőr-commit'))

    def test_cim_kozepen_nem_ellenor_commit(self):
        self.assertFalse(T.ellenor_commit_e('F102.14: az első ellenőri jelentés pótlása a CI-sorhoz', []))
        self.assertTrue(T.ellenor_commit_e('F190.4: ellenőri jelentés (1. ellenőrzés: TISZTA)', None))

    def test_nincs_jel(self):
        self.assertEqual(T.javitokor(['adat/x.tsv'], [{'cim': 'F1.1: x', 'fajlok': ['adat/x.tsv']}]),
                         (0, 'nincs jel'))


class IdoTeszt(unittest.TestCase):
    def test_ellenor_ido(self):
        commitok = [
            {'cim': 'F1.1: munka', 'ido': '2026-11-09T18:00:00Z', 'fajlok': ['adat/x.tsv']},
            {'cim': 'F1.2: az ELLENOR_F1 rögzítése', 'ido': '2026-11-09T18:40:00Z',
             'fajlok': ['naplok/ELLENOR_F1.md']},
            {'cim': 'F1.3: javítás', 'ido': '2026-11-09T19:00:00+01:00', 'fajlok': ['adat/x.tsv']},
            {'cim': 'F1.4: ellenőri jelentés (2.)', 'ido': '2026-11-09T18:12:00Z', 'fajlok': None},
        ]
        self.assertEqual([round(p) for p in T.ellenor_idok(commitok)], [40, 12])

    def test_elso_commit_nem_merheto(self):
        self.assertEqual(T.ellenor_idok([{'cim': 'ellenőri jelentés', 'ido': '2026-11-09T18:00:00Z',
                                          'fajlok': None}]), [])

    def test_ci(self):
        futasok = [
            {'status': 'completed', 'conclusion': 'success', 'createdAt': '2026-11-09T19:00:00Z',
             'updatedAt': '2026-11-09T19:02:00Z'},
            {'status': 'completed', 'conclusion': 'failure', 'createdAt': '2026-11-09T19:10:00Z',
             'updatedAt': '2026-11-09T19:11:00Z'},
            {'status': 'in_progress', 'conclusion': '', 'createdAt': '2026-11-09T19:20:00Z',
             'updatedAt': '2026-11-09T19:21:00Z'},
        ]
        n, b, atlag, osszes = T.ci_osszegzes(futasok)
        self.assertEqual((n, b), (3, 1))
        self.assertAlmostEqual(atlag, 1.5)
        self.assertAlmostEqual(osszes, 3.0)

    def test_ci_ures(self):
        self.assertEqual(T.ci_osszegzes([]), (0, 0, None, 0))


class KimenetTeszt(unittest.TestCase):
    def _sor(self, **kw):
        s = {k: T.NEM_MERT for k in T.OSZLOPOK}
        s['megjegyzes'] = ''
        s.update(kw)
        return s

    def test_tetel_elotag(self):
        self.assertEqual(T.tetel_elotagok(['F185.0.1: CI-javítás — E18', 'HATAR.GEPI: x',
                                           "Merge branch 'main'", 'szamkiosztas: DT-F1a → DT1']), 'F185,HATAR')
        self.assertEqual(T.tetel_elotagok(["Merge branch 'main'"]), '-')

    def test_osszesites_celokkal(self):
        sorok = [self._sor(pr='#1', admin='2', tartalmi='5', javitokor='0', ellenor_perc='12', ci_perc_atlag='1.0',
                           ci_futas='2', ellenor_futas='1'),
                 self._sor(pr='#2', admin='9', tartalmi='1', javitokor='2', ellenor_perc='40;20',
                           ci_perc_atlag='2.0', ci_futas='3', ellenor_futas='3'),
                 self._sor(pr='#3', admin='1', tartalmi='0', javitokor='0', ellenor_futas='0')]
        ki = T.osszesites(sorok)
        self.assertIn('admin ≤ tartalmi: 1 / 3 PR teljesíti (cél: mind)', ki)
        self.assertTrue(any(s.startswith('átlagos javítókör: 0.67') and s.endswith('teljesül') for s in ki), ki)
        self.assertIn('átlagos javítókör az ellenőrzött PR-okon: 1.00 (2 PR) — teljesül', ki)
        self.assertTrue(any('legnagyobb 40 perc, 2 a 15 perces cél fölött' in s for s in ki), ki)

    def test_nem_mert_nem_ures(self):
        sor = self._sor(pr='#3', ag='')
        mezok = T.tsv([sor])[1].split('\t')
        self.assertEqual(len(mezok), len(T.OSZLOPOK))
        self.assertTrue(all(m for m, k in zip(mezok, T.OSZLOPOK) if k != 'megjegyzes'))
        self.assertEqual(mezok[T.OSZLOPOK.index('ag')], T.NEM_MERT)

    def test_nem_mert_osszesites(self):
        ki = T.osszesites([self._sor(pr='#4')])
        self.assertIn('admin ≤ tartalmi: 0 / 0 PR teljesíti (cél: mind)', ki)
        self.assertIn('átlagos javítókör: %s' % T.NEM_MERT, ki)


if __name__ == '__main__':
    unittest.main(verbosity=1)
