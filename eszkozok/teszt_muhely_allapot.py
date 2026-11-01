#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F156: a muhely_allapot.py tesztjei -- a nyilvanos JSON csak feherlistas mezot hordoz; hianyzo/hibas mero nem zold."""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import muhely_allapot as M  # noqa: E402


def minta_belso():
    krit = [{'sorszam': i, 'nev': 'k%d' % i, 'allapot': 'zold', 'ertek': 'titkos hibaszöveg',
             'reszlet': ['döntésre váró kérdés szövege'], 'proveniencia': 'scope=x | forras=y | ts=z'}
            for i in range(1, 9)]
    st = {'cim': 'C', 'tema': 'T', 'pardes_szint': 'Drash', 'terjedelem_szo': 1, 'kotet': None,
          'elofordulas_osz': 1, 'elofordulas_usz': 1, 'kapcsolatok_db': 0, 'forditasi_lefedettseg': 1.0,
          'lektori_kerdes': None, 'utolso_generalas_commit': 'abc', 'verzio': 'v1',
          'kotet_megjegyzes': 'nincs kötet-adat'}
    return {
        '_generalt': 'eszkozok/muhely_allapot.py — feed_belso.json', 'generalva': 't', 'commit': 'abc',
        'rendszer': 'r', 'merok_osszesen': {}, 'heti_tortenes': [], 'elvetett_jeloltek_osszesen': 0,
        'pr_hiba': 'belső', 'ellenoriz_hiba': 'belső',
        'motivumok': [{'id': 'X-001', 'cim': 'c', 'tema': 't', 'pardes_szint': 'p', 'allasfokozat': 'lezárt',
                       'kriteriumok': krit, 'zold_db': 8, 'ossz_db': 8, 'nyitott_jelolt_db': 0,
                       'elvetett_jelolt_db': 0, 'beepitett_jelolt_db': 1, 'stash': st,
                       'prémium_mező': 'PRÉMIUM',
                       'elvetett_jeloltek': ['x'],
                       'nyitott_pr': [{'szam': 1}], 'tsv_statusz': 'publikálható',
                       'új_mező_alapból_belső': 'x'}],
    }


class Teszt(unittest.TestCase):
    def test_nyilvanos_csak_feherlista(self):
        ny = M.nyilvanos(minta_belso())
        self.assertTrue(set(ny) <= set(M.FEHERLISTA_TOP))
        m = ny['motivumok'][0]
        self.assertTrue(set(m) <= set(M.FEHERLISTA_MOTIVUM))
        for k in m['kriteriumok']:
            self.assertTrue(set(k) <= set(M.FEHERLISTA_KRITERIUM))
            self.assertNotIn('reszlet', k)
            self.assertNotIn('ertek', k)
        self.assertTrue(set(m['stash']) <= set(M.FEHERLISTA_STASH))
        szoveg = repr(ny)
        for tiltott in ('PRÉMIUM', 'döntésre váró', 'titkos hibaszöveg', 'új_mező_alapból_belső', 'pr_hiba',
                        'ellenoriz_hiba', "'nyitott_pr'", "'elvetett_jeloltek'"):
            self.assertNotIn(tiltott, szoveg)

    def test_hianyzo_mero_nem_zold(self):
        k = M.kriterium_7('NEMLETEZO-999')
        self.assertEqual(k['allapot'], M.NINCS)
        self.assertNotEqual(k['allapot'], M.ZOLD)

    def test_hianyzo_hatar_fajl_nem_zold(self):
        self.assertEqual(M.kriterium_5('NEMLETEZO-999')['allapot'], M.NINCS)

    def test_nem_futott_ellenoriz_hiba(self):
        self.assertEqual(M.kriterium_1('X-001', None, 1, 'hiba')['allapot'], M.HIBA)

    def test_globalis_serules_nem_zold(self):
        blokkok = [{'nev': '1. x', 'verdikt': 'SÉRTÉS', 'szoveg': ['**1. x**: SÉRTÉS -- valami']}]
        self.assertEqual(M.kriterium_1('X-001', blokkok, 0, '')['allapot'], M.PIROS)

    def test_proveniencia_forma(self):
        self.assertRegex(M.prov('mero', 'X-001'), r'^scope=motivum:X-001 \| forras=mero \| ts=\d{4}-')

    def test_datum(self):
        self.assertEqual(M.datum_iso('2026.09.13'), '2026-09-13')
        self.assertEqual(M.datum_iso('2026-10-21T09:18Z'), '2026-10-21')
        self.assertIsNone(M.datum_iso('x'))


if __name__ == '__main__':
    unittest.main()
