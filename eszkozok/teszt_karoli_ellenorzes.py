#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teszt a karoli_ellenorzes.py-hoz (F65): szintetikus mini-repón fut, a valódi adatot nem érinti.

    python eszkozok/teszt_karoli_ellenorzes.py
"""

import os
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_ellenorzes as ke  # noqa: E402

PAROK_FEJ = '# proveniencia: teszt\nvers\thu_sorszam\thu_szo\ter_sorszam\ter_szo\tstrong\tbizonyossag\tforras\n'
PAROK = [
    ('1Móz 1:2', 1, 'mélység', 'H8415', 'magas'),
    ('1Móz 1:2', 2, 'kietlen', 'H8414', 'magas'),
    ('1Móz 1:2', 3, 'és', 'H9002', 'magas'),
    ('1Móz 1:2', 4, 'puszta', 'H0922', 'magas'),
    ('1Móz 2:7', 1, 'élő', 'H2416', 'magas'),
    ('1Móz 2:7', 2, 'lélekké', 'H5315', 'magas'),
    ('1Móz 3:1', 1, 'kígyó', 'H5175', 'alacsony'),
    ('2Móz 19:6', 1, 'papok', 'H3548', 'magas'),
    ('2Móz 19:6', 2, 'birodalma', 'H4467', 'magas'),
]
FEJ = 'id\tigehely\tkapcsolodas\tstrong\tkaroli_szo\tazonositas_modja\tmegbizhatosag\tproveniencia'
E_SOROK = [
    # id, igehely, strong, szo, mod
    ('M-1', '1Móz 1:2', 'H8415', 'a mélység', 'tartalom-alapú'),            # egyezik, magas, részleges (a)
    ('M-1', '1Móz 2:7', 'H5315+H2416', 'élő lélekké', 'tartalom-alapú'),    # egyezik, magas
    ('M-1', '1Móz 3:1', 'H5175', 'kígyó', 'tartalom-alapú'),                # egyezik, de alacsony: nem frissül
    ('M-1', '2Móz 19:6', 'H3548+H4467', 'papok', 'tartalom-alapú'),         # elter
    ('M-1', 'Luk 1:46', 'G4151', 'lelkem', 'tartalom-alapú'),               # nincs_par
    ('M-1', '1Móz 1:2', 'H0922', 'puszta', 'szó-szintű-gépi'),              # már átállított: marad
]
J_FEJ = 'id\tigehely\tforras_kereses\tdontes\tindoklas\tkaroli_szo\tazonositas_modja\tmegbizhatosag\tdatum'


def kesz_repo(gyoker):
    os.makedirs(os.path.join(gyoker, 'adat', 'karoli_strong'))
    with open(os.path.join(gyoker, 'adat', 'karoli_strong', 'parok_1Moz.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write(PAROK_FEJ)
        for v, n, sz, st, bz in PAROK:
            if v.startswith('1Móz'):
                f.write('\t'.join([v, str(n), sz, str(n), 'x', st, bz, 'S+C']) + '\n')
    with open(os.path.join(gyoker, 'adat', 'karoli_strong', 'parok_2Moz.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write(PAROK_FEJ)
        for v, n, sz, st, bz in PAROK:
            if v.startswith('2Móz'):
                f.write('\t'.join([v, str(n), sz, str(n), 'x', st, bz, 'S+C']) + '\n')
    with open(os.path.join(gyoker, 'adat', 'elofordulasok.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('# teszt\n' + FEJ + '\n')
        for i, g, st, sz, m in E_SOROK:
            f.write('\t'.join([i, g, 'idézet "x"', st, sz, m, 'magas', 'scope=manual | forras=t | ts=1']) + '\n')
    with open(os.path.join(gyoker, 'adat', 'jeloltek.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('# teszt\n' + J_FEJ + '\n')
        for i, g, st, sz, m in E_SOROK:
            f.write('\t'.join([i, g, 'k', 'beépítve', 'ind', sz, m, 'magas', '2026.10.11']) + '\n')


class Teszt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        kesz_repo(self.tmp.name)
        self.regi_root = ke.ROOT
        ke.ROOT = self.tmp.name

    def tearDown(self):
        ke.ROOT = self.regi_root
        self.tmp.cleanup()

    def olvas(self, rel):
        with open(os.path.join(self.tmp.name, rel), encoding='utf-8', newline='') as f:
            return f.read()

    def itelet(self):
        return {(e['igehely'], e['karoli_szo']): e for e in ke.ellenorzes_futtat()}

    def test_iteletek(self):
        e = self.itelet()
        self.assertEqual(e[('1Móz 1:2', 'a mélység')]['r']['itelet'], 'egyezik')
        self.assertEqual(e[('2Móz 19:6', 'papok')]['r']['itelet'], 'elter')
        self.assertEqual(e[('Luk 1:46', 'lelkem')]['r']['itelet'], 'nincs_par')
        self.assertTrue(ke.frissitheto(e[('1Móz 2:7', 'élő lélekké')]['r']))
        self.assertFalse(ke.frissitheto(e[('1Móz 3:1', 'kígyó')]['r']))   # alacsony
        self.assertFalse(ke.frissitheto(e[('2Móz 19:6', 'papok')]['r']))

    def test_reszleges(self):
        e = self.itelet()
        r = e[('1Móz 1:2', 'a mélység')]['r']
        # "a mélység": a névelő kiszűrve -> teljes egyezés
        self.assertFalse(ke.reszleges(r))
        self.assertEqual(r['nem_illesztett'], [])
        # "kietlen és puszta" H8414 sor: az "és" kiszűrve, a "puszta" más Stronghoz (H0922) illeszkedik
        r2 = ke.ellenoriz_sor('1Móz 1:2', 'kietlen és puszta', ['H8414'], ke.betolt_parok()[0])
        self.assertTrue(ke.reszleges(r2))
        self.assertEqual(r2['mas_strong'], ['puszta:H0922'])
        self.assertEqual(r2['nincs_gepi_par'], [])
        # nincs gépi párja: "lélekké" mellett idegen szó
        r3 = ke.ellenoriz_sor('1Móz 2:7', 'élő lélekké nagyon', ['H2416'], ke.betolt_parok()[0])
        self.assertEqual(r3['nincs_gepi_par'], ['nagyon'])
        self.assertEqual(r3['mas_strong'], ['lélekké:H5315'])
        self.assertFalse(ke.reszleges(e[('1Móz 2:7', 'élő lélekké')]['r']))

    def test_szarazon_nem_ir(self):
        elo = self.olvas('adat/elofordulasok.tsv')
        self.assertEqual(ke.frissit(ir=False), (2, 2))
        self.assertEqual(self.olvas('adat/elofordulasok.tsv'), elo)

    def test_frissit_idempotens_es_csak_a_mod_valtozik(self):
        elo = self.olvas('adat/elofordulasok.tsv').split('\n')
        self.assertEqual(ke.frissit(ir=True), (2, 2))
        uj = self.olvas('adat/elofordulasok.tsv')
        ujsor = uj.split('\n')
        self.assertEqual(len(elo), len(ujsor))
        kulonbseg = [n for n, (a, b) in enumerate(zip(elo, ujsor)) if a != b]
        self.assertEqual(len(kulonbseg), 2)
        for n in kulonbseg:
            a, b = elo[n].split('\t'), ujsor[n].split('\t')
            self.assertEqual([k for k in range(len(a)) if a[k] != b[k]], [5])
            self.assertEqual(b[5], ke.UJ_MOD)
            self.assertIn('"x"', b[2])  # idézőjeles mező bájthű
        # másodszori futás: nem ír, nem bánt semmit
        j = self.olvas('adat/jeloltek.tsv')
        self.assertEqual(ke.frissit(ir=True), (0, 0))
        self.assertEqual(self.olvas('adat/elofordulasok.tsv'), uj)
        self.assertEqual(self.olvas('adat/jeloltek.tsv'), j)
        # az eltérő / alacsony / nincs_par sor nem változott
        for sz in ('papok', 'kígyó', 'lelkem'):
            self.assertIn('\t%s\ttartalom-alapú\t' % sz, uj)
        # az eleve átállított sor megmaradt
        self.assertIn('\tpuszta\tszó-szintű-gépi\t', uj)

    def test_motivum_szuro(self):
        self.assertEqual(ke.frissit(ir=False, motivum='NINCS'), (0, 0))

    def test_variancia_sajat_proveniencia(self):
        ut = os.path.join(self.tmp.name, 'var.tsv')
        ke.variancia(ut, '2026-10-11')
        sorok = self.olvas('var.tsv').split('\n')
        fej = sorok[1].split('\t')
        self.assertEqual(fej, ke.VAR_FEJ)
        m = [s.split('\t') for s in sorok[2:] if s.startswith('megerosites')]
        # a frissíthető 2 sor + az eleve átállított, még mindig egyező 'puszta' sor
        self.assertEqual(len(m), 3)
        for r in m:
            prov = r[fej.index('proveniencia')]
            self.assertTrue(prov.startswith('scope=manual | forras=adat/karoli_strong/parok_'))
            self.assertIn('ts=2026-10-11', prov)
        resz = {r[fej.index('karoli_szo')]: r[fej.index('reszleges')] for r in m}
        self.assertEqual(resz['a mélység'], 'nem')
        self.assertEqual(resz['élő lélekké'], 'nem')
        # az alacsony 1Móz 3:1 sor nem megerősítés; az aggregátumok bizonyossaga jelölt
        self.assertFalse(any(r[fej.index('karoli_szo')] == 'kígyó' for r in m))
        self.assertTrue(any(s.startswith('strong_szoalak\t1Moz\tH5175\tkígyó\t1\talacsony') for s in sorok))

    def test_variancia_ujrafuttatas_ugyanaz(self):
        ut = os.path.join(self.tmp.name, 'var.tsv')
        ke.variancia(ut, '2026-10-11')
        elso = self.olvas('var.tsv')
        ke.frissit(ir=True)
        ke.variancia(ut, '2026-10-11')
        self.assertEqual(self.olvas('var.tsv'), elso)  # az átállítás nem változtatja a megerősítéseket


if __name__ == '__main__':
    unittest.main(verbosity=2)
