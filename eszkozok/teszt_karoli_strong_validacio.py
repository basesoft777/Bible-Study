#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — az emberi validáció mintájának és kiértékelőjének tesztjei.

A válaszfájlok kitaláltak (a tesztben generált műítéletek); valódi ellenőri ítélet
nincs bennük. A kimenet ideiglenes könyvtárba megy, a repón kívülre.

Futtatás: python eszkozok/teszt_karoli_strong_validacio.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_validacio_kiertekel as ki  # noqa: E402
import karoli_strong_validacio_minta as vm  # noqa: E402

SZKRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong_validacio_kiertekel.py')


def _export(nev, minta, hash_, itelet_of):
    v = {}
    for r in minta:
        it = itelet_of(r)
        if it:
            v[r['tetel_id']] = {'itelet': it[0], 'hibatipus': it[1], 'helyes_forras': [], 'megjegyzes': 'teszt'}
    return {'oldal': 'F175.V1', 'minta_hash': hash_, 'minta_meret': len(minta), 'ellenor': nev,
            'sorrend': [r['tetel_id'] for r in minta], 'valaszok': v}


class Statisztika(unittest.TestCase):
    def test_wilson(self):
        p, lo, hi = ki.wilson(0, 10)
        self.assertEqual(p, 0.0)
        self.assertAlmostEqual(lo, 0.0, places=6)
        self.assertAlmostEqual(hi, 0.2775, places=4)
        p, lo, hi = ki.wilson(95, 100)
        self.assertAlmostEqual(lo, 0.8882, places=3)
        self.assertAlmostEqual(hi, 0.9785, places=3)

    def test_kappa(self):
        self.assertAlmostEqual(ki.kappa([('a', 'a'), ('b', 'b')] * 5, ('a', 'b'))[0], 1.0)
        # klasszikus példa: 20 a/a, 5 a/b, 10 b/a, 15 b/b -> po=0.7, pe=0.5, kappa=0.4
        p = [('a', 'a')] * 20 + [('a', 'b')] * 5 + [('b', 'a')] * 10 + [('b', 'b')] * 15
        k, po, n = ki.kappa(p, ('a', 'b'))
        self.assertAlmostEqual(po, 0.7)
        self.assertAlmostEqual(k, 0.4)
        self.assertEqual(n, 50)

    def test_legnagyobb_maradek(self):
        d = vm.legnagyobb_maradek({'x': 1, 'y': 1, 'z': 1}, 10)
        self.assertEqual(sum(d.values()), 10)
        self.assertEqual(d, {'x': 4, 'y': 3, 'z': 3})


class Minta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.minta = ki.tabla(ki.MINTA)

    def test_meret_es_retegek(self):
        par = [r for r in self.minta if r['tipus'] == 'par']
        nelkul = [r for r in self.minta if r['tipus'] == 'parnelkuli']
        self.assertEqual(len(par), 300)
        self.assertEqual(len(nelkul), 80)
        self.assertEqual(len({r['tetel_id'] for r in self.minta}), 380)
        self.assertEqual(len({r['csoport'] for r in par}), 7)
        self.assertEqual(len({r['csoport'] for r in nelkul}), 7)
        self.assertTrue(all(r['f172_id'] for r in par))

    def test_kiemeles_a_szon_all(self):
        for r in self.minta:
            self.assertEqual(r['hu_vers'][int(r['hu_kezdet']):int(r['hu_veg'])], r['hu_szo'], r['tetel_id'])
            if r['tipus'] == 'par':
                tok = json.loads(r['er_tokenek_json'])
                self.assertEqual(tok[int(r['er_sorszam']) - 1]['a'], r['er_szo'], r['tetel_id'])

    def test_hash_egyezik_az_oldaleval(self):
        # az ellenorzo.html a böngészőben ezt számolta a mostani mintára (F175.V kipróbálás)
        self.assertEqual(ki.minta_hash(self.minta), '70a9f72b')


class Kiertekeles(unittest.TestCase):
    """Végponttól végpontig, kitalált ítéletekkel."""

    @classmethod
    def setUpClass(cls):
        _, cls.minta = ki.tabla(ki.MINTA)
        cls.h = ki.minta_hash(cls.minta)
        cls.tmp = tempfile.mkdtemp(prefix='ksval_teszt_')
        par = [r['tetel_id'] for r in cls.minta if r['tipus'] == 'par']
        nelkul = [r['tetel_id'] for r in cls.minta if r['tipus'] == 'parnelkuli']
        cls.b_hibas = set(par[:10])           # B: 10 pár hibás
        cls.b_bizonytalan = set(par[10:12])   # B: 2 pár bizonytalan
        cls.a_hibas = set(par[:4])            # A: 4 pár hibás (ezekben B-vel egyezik)
        cls.kimaradt = set(nelkul[:3])        # mindkettő: 3 pár nélküli szónak van eredetije

        def a_of(r):
            t = r['tetel_id']
            if t in cls.a_hibas:
                return ('hibas', 'rossz_forrasszo')
            if t in cls.kimaradt:
                return ('hibas', 'kimaradt_par')
            return ('helyes', '')

        def b_of(r):
            t = r['tetel_id']
            if t in cls.b_hibas:
                return ('hibas', 'folosleges_par')
            if t in cls.b_bizonytalan:
                return ('bizonytalan', '')
            if t in cls.kimaradt:
                return ('hibas', 'kimaradt_par')
            return ('helyes', '')

        cls.fa = os.path.join(cls.tmp, 'Teszt_A_valaszok.json')
        cls.fb = os.path.join(cls.tmp, 'Teszt_B_valaszok.json')
        for ut, nev, f in ((cls.fa, 'Teszt A', a_of), (cls.fb, 'Teszt B', b_of)):
            with open(ut, 'w', encoding='utf-8') as fh:
                json.dump(_export(nev, cls.minta, cls.h, f), fh, ensure_ascii=False)

    def _fut(self, *extra):
        ki_dir = os.path.join(self.tmp, 'ki_%d' % len(extra))
        r = subprocess.run([sys.executable, SZKRIPT, self.fa, self.fb, '--kimenet', ki_dir] + list(extra),
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(ki_dir, 'kiertekeles.md'), encoding='utf-8') as f:
            md = f.read()
        _, elt = ki.tabla(os.path.join(ki_dir, 'eltero_tetelek.tsv'))
        return md, elt, ki_dir

    def test_eltero_es_pontossag(self):
        md, elt, _ = self._fut()
        self.assertEqual(len(elt), 8)   # 6 hibás-vs-helyes + 2 bizonytalan
        self.assertIn('| A (Teszt A) | 300 | 296 | 4 | 0 | 98.67%', md)
        self.assertIn('| B (Teszt B) | 300 | 288 | 10 | 2 | 96.64%', md)
        # döntés nélkül a döntött minta csak az egyező tételeket tartalmazza
        self.assertIn('| **döntött minta** | 292 | 288 | 4 | 0 |', md)
        self.assertIn('| A (Teszt A) | 80 | 77 | 3 | 0 | 3.75%', md)
        self.assertIn('döntésre vár: 8', md)

    def test_harmadik_dontes_es_modell(self):
        _, elt, ki_dir = self._fut()
        # a harmadik döntés: minden eltérőnél "helyes"
        ut = os.path.join(self.tmp, 'dontes.tsv')
        with open(os.path.join(ki_dir, 'eltero_tetelek.tsv'), encoding='utf-8') as f:
            sorok = [s.rstrip('\n') for s in f]
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            for s in sorok:
                if s.startswith('#') or s.startswith('tetel_id'):
                    f.write(s + '\n')
                else:
                    m = s.split('\t')
                    m[ki.ELTERO_FEJ.index('dontes')] = 'helyes'
                    f.write('\t'.join(m) + '\n')
        md, _, _ = self._fut('--dontes', ut, '--modell-f172')
        self.assertIn('| **döntött minta** | 300 | 296 | 4 | 0 | 98.67%', md)
        self.assertIn('döntésre vár: 0', md)
        self.assertIn('| párok | 300 |', md)   # a modell (#172) mind a 300 párra ad ítéletet

    def test_rossz_hash_elutasitva(self):
        rossz = os.path.join(self.tmp, 'rossz.json')
        with open(self.fa, encoding='utf-8') as f:
            d = json.load(f)
        d['minta_hash'] = '0'
        with open(rossz, 'w', encoding='utf-8') as f:
            json.dump(d, f)
        r = subprocess.run([sys.executable, SZKRIPT, rossz, self.fb, '--kimenet', os.path.join(self.tmp, 'x')],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(r.returncode, 0)


class Oldal(unittest.TestCase):
    """Az ellenorzo.html szkriptje Node-on: kitöltés, emlékeztető, export, betöltés tiszta állapotba,
    tételenkénti időbélyeges összefésülés, idegen minta és más ellenőr fájlja."""

    @unittest.skipUnless(shutil.which('node'), 'nincs node')
    def test_betoltes_es_osszefesules(self):
        proba = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong_validacio_oldal_proba.js')
        oldal = os.path.join(ki.VALIDACIO, 'ellenorzo.html')
        r = subprocess.run(['node', proba, oldal], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('RENDBEN', r.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
