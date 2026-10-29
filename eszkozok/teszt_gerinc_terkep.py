#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_gerinc_terkep.py -- F124: a gerinc_terkep.py tesztjei: fajlnev-alapu
lefedettseg, kizarasi szabalyok, rangsor-stabilitas, idempotencia (ket futas
bajtra azonos), es a valos adaton: adattabla nem valtozik.

    python eszkozok/teszt_gerinc_terkep.py
"""

import hashlib
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerinc_kartya as K  # noqa: E402
import gerinc_terkep as T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sor(mid, konyv, fej, vers, allapot='új', szures='', kolloc='', strong='H3548'):
    return {'id': mid, 'igehely': '%s %d:%d' % (konyv, fej, vers), 'kulcs': (konyv, fej, vers),
            'strong': strong, 'allapot': allapot, 'szures': szures, 'kollokacio': kolloc}


KIDX = K.konyv_index()


class Fajlnev(unittest.TestCase):
    TOK = T.konyv_tokenek()

    def t(self, nev):
        return T.fajlnev_tartomany(nev, self.TOK)

    def test_alakok(self):
        self.assertEqual(self.t('1Moz_14_bovitett.md'), ('1Móz', ('chapters', 14, None, 14, None)))
        self.assertEqual(self.t('1Moz_12v1-20_bovitett.md'), ('1Móz', ('verses', 12, 1, 12, 20)))
        self.assertEqual(self.t('1Moz_1v2-2v3_bovitett.md'), ('1Móz', ('verses', 1, 2, 2, 3)))
        self.assertEqual(self.t('1Moz_4v25-5v32_bovitett.md'), ('1Móz', ('verses', 4, 25, 5, 32)))
        self.assertEqual(self.t('Rom_8v10_bovitett.md'), ('Róm', ('verses', 8, 10, 8, 10)))
        self.assertEqual(self.t('1Thessz_5v23_bovitett.md'), ('1Thessz', ('verses', 5, 23, 5, 23)))
        self.assertEqual(self.t('Zsid_5-7_bovitett.md'), ('Zsid', ('chapters', 5, None, 7, None)))

    def test_nem_ertelmezheto(self):
        self.assertIsNone(self.t('1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md'))
        self.assertIsNone(self.t('Ismeretlen_3v1_bovitett.md'))
        self.assertIsNone(self.t('1Moz_3v1_masik.md'))


class Lefedettseg(unittest.TestCase):
    BB = {'1Móz': [('1Móz', c, v) for c in (1, 2, 3) for v in range(1, 6)]}

    def test_vers_pontos(self):
        f, ert, hib = T.lefedettseg([('genezis/1Moz_2v2-3v1_bovitett.md', '1Moz_2v2-3v1_bovitett.md')], self.BB)
        self.assertEqual(f, {('1Móz', 2, 2), ('1Móz', 2, 3), ('1Móz', 2, 4), ('1Móz', 2, 5), ('1Móz', 3, 1)})
        self.assertEqual((len(ert), hib), (1, []))

    def test_egy_vers_nem_fedi_a_fejezetet(self):
        f, _, _ = T.lefedettseg([('x', '1Moz_1v1_bovitett.md')], self.BB)
        self.assertEqual(f, {('1Móz', 1, 1)})

    def test_fejezet(self):
        f, _, _ = T.lefedettseg([('x', '1Moz_3_bovitett.md')], self.BB)
        self.assertEqual(len(f), 5)

    def test_hibak_listazva_osszesito_kihagyva(self):
        f, ert, hib = T.lefedettseg([('genezis/Konnyu_ellenorzes_1-16_osszesito.md', 'Konnyu_ellenorzes_1-16_osszesito.md'),
                                     ('melyelemzesek/1Mozes_x_melyelemzes.md', '1Mozes_x_melyelemzes.md'),
                                     ('genezis/1Moz_99_bovitett.md', '1Moz_99_bovitett.md')], self.BB)
        self.assertEqual(f, set())
        self.assertEqual([h[0] for h in hib], ['melyelemzesek/1Mozes_x_melyelemzes.md', 'genezis/1Moz_99_bovitett.md'])


class Szamitas(unittest.TestCase):
    def szamit(self, sorok, fedett=frozenset()):
        return T.terkep_szamit(sorok, set(fedett), KIDX)

    def test_kizarasok(self):
        sorok = [
            sor('A-001', '1Móz', 1, 1),                                   # szamit
            sor('A-001', '1Móz', 1, 2, allapot='már előfordulás'),        # kizarva
            sor('A-001', '1Móz', 1, 3, allapot='már jelölt: elutasítva'),
            sor('A-001', '1Móz', 1, 4, allapot='már jelölt: beépítve'),
            sor('A-001', '1Móz', 1, 5, szures='kiszurve'),                # kizarva
            sor('A-001', '1Móz', 1, 6),                                   # tanulmany fedi
            sor('A-001', '1Móz', 1, 7, allapot='már jelölt: nyitva'),     # kulon oszlop
            sor('A-001', '1Móz', 1, 8, szures='szuretlen_tag'),           # kulon oszlop
        ]
        ki, mot = self.szamit(sorok, {('1Móz', 1, 6)})
        self.assertEqual(len(ki), 1)
        r = ki[0]
        self.assertEqual((r['talalat_db'], r['nyitva_db'], r['szuretlen_tag_db'], r['motivum_db']), (1, 1, 1, 1))
        self.assertEqual(mot['A-001'], {'talalat_db': 1, 'szuretlen_tag_db': 1, 'nyitva_db': 1})

    def test_szuretlen_nem_sulyoz(self):
        ki, _ = self.szamit([sor('A-001', '1Móz', 1, v, szures='szuretlen_tag') for v in range(1, 6)])
        self.assertEqual((ki[0]['talalat_db'], ki[0]['motivum_db'], ki[0]['szuretlen_tag_db']), (0, 0, 5))

    def test_ketto_tag_egy_talalat(self):
        ki, _ = self.szamit([sor('A-001', '1Móz', 1, 1, strong='H7121', kolloc='kollokáció'),
                             sor('A-001', '1Móz', 1, 1, strong='H8034', kolloc='kollokáció')])
        self.assertEqual((ki[0]['talalat_db'], ki[0]['kollokacio_db']), (1, 1))

    def test_rangsor_lexikografikus_es_kanonikus(self):
        sorok = [
            sor('A-001', '2Móz', 5, 1), sor('B-001', '2Móz', 5, 2),                    # 2 motivum
            sor('A-001', '1Móz', 9, 1), sor('A-001', '1Móz', 9, 2, kolloc='kollokáció'),  # 1 motivum, kolloc 1
            sor('A-001', '1Móz', 7, 1), sor('A-001', '1Móz', 7, 2),                    # 1 motivum, 2 talalat
            sor('A-001', '1Móz', 3, 1), sor('A-001', '1Móz', 3, 2),                    # egyezes -> kanonikus
        ]
        ki, _ = self.szamit(sorok)
        self.assertEqual([(r['konyv'], r['fejezet']) for r in ki],
                         [('2Móz', 5), ('1Móz', 9), ('1Móz', 3), ('1Móz', 7)])

    def test_rangsor_stabil_a_bemeneti_sorrendtol(self):
        sorok = [sor('A-001', '1Móz', c, 1) for c in (5, 3, 4, 1)] + [sor('B-001', '2Móz', 1, 1)]
        a, _ = self.szamit(sorok)
        b, _ = self.szamit(list(reversed(sorok)))
        self.assertEqual(a, b)

    def test_ures(self):
        self.assertEqual(self.szamit([]), ([], {}))

    def test_kiszurt_nyitva_jelolt_a_nyitva_oszlopban_marad(self):
        ki, _ = self.szamit([sor('A-001', '1Móz', 1, 1, allapot='már jelölt: nyitva', szures='kiszurve')])
        self.assertEqual((ki[0]['nyitva_db'], ki[0]['talalat_db']), (1, 0))

    def test_siralmak_kanonikus_helye(self):
        self.assertLess(KIDX['Sir'], KIDX['Ez'] + 100)
        self.assertLess(KIDX['Sir'], 999)
        self.assertLess(KIDX['Sir'], KIDX['Jel'])


class Kimenet(unittest.TestCase):
    def test_tsv_fejlec_es_idempotens(self):
        ki, mot = T.terkep_szamit([sor('A-001', '1Móz', 1, 1, kolloc='kollokáció')], set(), KIDX)
        a = T.tsv_szoveg(ki, 'x@1', '2026-01-01T00:00Z')
        b = T.tsv_szoveg(ki, 'x@1', '2026-01-01T00:00Z')
        self.assertEqual(a, b)
        sorok = a.split('\n')
        self.assertTrue(sorok[0].startswith('# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes | forras='))
        self.assertIn('bemenet=x@1', sorok[0])
        self.assertEqual(sorok[1].split('\t'), T.TSV_FEJLEC)
        self.assertEqual(len(sorok[2].split('\t')), len(T.TSV_FEJLEC))
        self.assertIn('ts=2026-01-01T00:00Z', sorok[2])

    def test_md_ures_es_hibak(self):
        md = T.md_szoveg([], {}, [], [('f.md', 'ok')], 0, 'x@1', 'ts')
        self.assertTrue(md.startswith('# GENERÁLT: gerinc_terkep.py'))
        self.assertIn('üres', md)
        self.assertIn('`f.md` — ok', md)

    def test_bemenet_azonosito_nem_futasidobol(self):
        n = [('genezis/a_bovitett.md', 'a_bovitett.md')]
        a = T.bemenet_azonosito(ROOT, n, blob=lambda f, r: 'h', ts_fn=lambda p, r: 'T')
        b = T.bemenet_azonosito(ROOT, n, blob=lambda f, r: 'h', ts_fn=lambda p, r: 'T')
        self.assertEqual(a, b)
        c = T.bemenet_azonosito(ROOT, n + [('genezis/b_bovitett.md', 'b')], blob=lambda f, r: 'h', ts_fn=lambda p, r: 'T')
        self.assertNotEqual(a[0], c[0])      # uj tanulmanyfajl -> mas bemenet-azonosito


class GitAzonosito(unittest.TestCase):
    def test_valos_git_ket_hivasra_azonos(self):
        n = T.tanulmany_fajlnevek(ROOT)
        a = T.bemenet_azonosito(ROOT, n)
        self.assertEqual(a, T.bemenet_azonosito(ROOT, n))
        self.assertIn('eszkozok/general.py@', a[0])
        self.assertNotEqual(a[1], '')


def _hash(utak):
    h = {}
    for u in utak:
        with open(os.path.join(ROOT, u), 'rb') as f:
            h[u] = hashlib.sha1(f.read()).hexdigest()
    return h


class ValosAdat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')):
            raise unittest.SkipTest('nincs konkordancia')
        cls.versek = K.versek_betolt()

    def test_ket_futas_bajtra_azonos_es_nem_ir_adatot(self):
        tabla = ['adat/motivumok.tsv', 'adat/elofordulasok.tsv', 'adat/jeloltek.tsv', 'adat/kulcsszavak.tsv']
        elotte = _hash(tabla)
        d1 = tempfile.mkdtemp(prefix='terkep1_')
        d2 = tempfile.mkdtemp(prefix='terkep2_')
        self.addCleanup(shutil.rmtree, d1, True)
        self.addCleanup(shutil.rmtree, d2, True)
        stub = lambda root, nevek: ('stub@1', 'T')     # noqa: E731
        ki1, mot1, tsv1, md1 = T.futtat(os.path.join(ROOT, 'adat'), versek=self.versek, kimenet_dir=d1, bemenet_fn=stub)
        T.futtat(os.path.join(ROOT, 'adat'), versek=self.versek, kimenet_dir=d2, bemenet_fn=stub)
        for nev in ('GERINC_TERKEP.tsv', 'GERINC_TERKEP.md'):
            with open(os.path.join(d1, nev), 'rb') as a, open(os.path.join(d2, nev), 'rb') as b:
                self.assertEqual(a.read(), b.read(), nev)
        self.assertEqual(_hash(tabla), elotte)
        self.assertTrue(ki1)

    def test_feldolgozott_vers_nincs_a_terkepen(self):
        # a genezis/ tanulmanyok versei kizarva: az 1Moz 14 teljes fejezet fedett
        stub = lambda root, nevek: ('stub@1', 'T')     # noqa: E731
        ki, _, _, md = T.futtat(os.path.join(ROOT, 'adat'), versek=self.versek, bemenet_fn=stub)
        self.assertNotIn(('1Móz', 14), {(r['konyv'], r['fejezet']) for r in ki if r['talalat_db'] > 0})
        self.assertIn('Értelmezett tanulmányfájl:', md)


if __name__ == '__main__':
    unittest.main()
