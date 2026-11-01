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
    krit = [{'sorszam': i, 'nev': 'ellenoriz.py k%d' % i, 'allapot': 'nincs_mero', 'szin': 'szurke',
             'olvasoi_nev': M.OLV_NEV[i], 'olvasoi_allapot': M.OLV_ALLAPOT['nincs_mero'],
             'olvasoi_szoveg': M.OLV_NINCS[i], 'ertek': 'titkos hibaszöveg',
             'reszlet': ['döntésre váró kérdés szövege'], 'proveniencia': 'scope=x | forras=y | ts=z'}
            for i in range(1, 9)]
    st = {'cim': 'C', 'tema': 'T', 'pardes_szint': 'Drash', 'terjedelem_szo': 1, 'kotet': None,
          'elofordulas_osz': 1, 'elofordulas_usz': 1, 'kapcsolatok_db': 0, 'forditasi_lefedettseg': 1.0,
          'lektori_kerdes': None, 'utolso_generalas_commit': 'abc', 'verzio': 'v1',
          'kotet_megjegyzes': 'nincs kötet-adat'}
    return {
        '_generalt': 'eszkozok/muhely_allapot.py — feed_belso.json', 'generalva': 't', 'commit': 'abc',
        'rendszer': 'r', 'merok_osszesen': {}, 'elvetett_jeloltek_osszesen': 0,
        'heti_tortenes': [{'datum': '2026-11-01', 'motivum': 'X-001', 'esemeny': 'jelölt-döntés: beépítve', 'db': 2,
                           'olvasoi_esemeny': '2 igehely bekerült a motívumba'}],
        'pr_hiba': 'belső', 'ellenoriz_hiba': 'belső',
        'motivumok': [{'id': 'X-001', 'cim': 'c', 'tema': 't', 'pardes_szint': 'p', 'allasfokozat': 'lezárt (stash)', 'allasfokozat_olvasoi': 'Kész, megjelenésre vár',
                       'olvasoi_mondat': 'x', 'tsv_statusz_x': 1,
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
            for tiltott in ('reszlet', 'ertek', 'nev', 'allapot', 'proveniencia'):
                self.assertNotIn(tiltott, k)
        self.assertTrue(set(m['stash']) <= set(M.FEHERLISTA_STASH))
        szoveg = repr(ny)
        for tiltott in ('PRÉMIUM', 'döntésre váró', 'titkos hibaszöveg', 'új_mező_alapból_belső', 'pr_hiba',
                        'ellenoriz_hiba', "'nyitott_pr'", "'elvetett_jeloltek'", 'nincs_mero', 'ellenoriz.py',
                        'jelölt-döntés', "'esemeny'"):
            self.assertNotIn(tiltott, szoveg)

    def test_olvasoi_szoveg_nem_tartalmaz_belso_szot(self):
        belso_szavak = ('gerinc', 'ellenoriz', 'futtat', 'nulla-diff', 'DT', 'nincs_mero', '.py', 'CI', 'E2', 'jelölt',
                        'tsv')
        szovegek = list(M.OLV_NEV.values()) + list(M.OLV_ALLAPOT.values()) + list(M.OLV_ZOLD.values()) +             list(M.OLV_NINCS.values()) + list(M.OLV_ALLAS.values()) + [M.OLV_KOTET]
        for sz in range(1, 9):
            for al in ('zold', 'piros', 'nincs_mero', 'hiba'):
                szovegek.append(M.olvasoi_kapu({'sorszam': sz, 'allapot': al,
                                                'szam': {'n': 3, 'kiejtes': 1, 'fordit': 2, 'blokk': 1}}))
        for sz in szovegek:
            for szo in belso_szavak:
                self.assertNotIn(szo, sz, sz)

    def test_olvasoi_mondat(self):
        self.assertEqual(M.olvasoi_mondat(33, 6, 92, 3),
                         '33 igehely feldolgozva, 6 vizsgálat alatt, 92 kizárva; a nyolc ellenőrzési lépésből 3 teljesül.')
        self.assertEqual(M.olvasoi_mondat(8, 0, 0, 1),
                         '8 igehely feldolgozva, nincs vizsgálat alatt álló igehely; a nyolc ellenőrzési lépésből 1 teljesül.')

    def test_olvasoi_esemeny(self):
        self.assertEqual(M.olvasoi_esemeny({'esemeny': 'állapot: publikálható (v3)', 'db': 1}),
                         'A motívum lapja új változatot kapott (3. változat)')

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
