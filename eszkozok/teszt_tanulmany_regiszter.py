#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_tanulmany_regiszter.py -- F149 M1: a tanulmány-regiszter és a vers -> szakasz index tesztjei.

    python eszkozok/teszt_tanulmany_regiszter.py

  címsor-tartomány:  egész fejezet, fejezethatáron átnyúló, több szegmens (DT-F149a (c))
  egyezés-ellenőrzés: eltérő fájlnév–címsor -> nem kerül a regiszterbe, a kimenet megnevezi
  hivatkozás-fokozat: egyedi vers = nev, tartomány = tartomany (DT-F149b); a tartományon kívüli
                      tartomány-említés, a sorozat-kontextus és a fejléc nem kerül az indexbe
  sorozat:           hézag és átfedés figyelmeztetés
  valós adat:        a repó tanulmányai kinyerhetők, nincs kihagyott, a Genezis-sorozat hézag nélküli
"""
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
import tanulmany_regiszter as T  # noqa: E402

ROOT = T.GYOKER
KULCSOK = T.karoli_kulcsok(ROOT)


def tmp_gyoker(fajlok):
    """Ideiglenes gyökér a könyvnév-táblával és a megadott tanulmány-fájlokkal."""
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, 'konkordancia'))
    shutil.copy(os.path.join(ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'),
                os.path.join(d, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'))
    for rel, szoveg in fajlok.items():
        p = os.path.join(d, *rel.split('/'))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
    return d


MINTA = """# 1Mózes 14:18–20 — Teszt
Fejléc: 1Móz 14:18-20 sorozat.

## 0. Sorozat-kontextus
Az előző: 1Móz 13:1-18.

## 1. Peshat
Melkisédek (14:18) kenyeret hoz. A 19–20. versben áld. Lásd Zsolt 110:4 és 1Móz 14:1-24.
Ézs 9:5 más.

### Alpont
Csak a 18. v. szól.
"""


class Cimsor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kar = T.Karoli(KULCSOK)

    def test_egesz_fejezet_es_hatar(self):
        t = T.tartomany_cimsorbol('# 1Mózes 14 — x', self.kar)
        self.assertEqual(t, [('1Móz', (14, 1), (14, 24))])
        t = T.tartomany_cimsorbol('# 1Mózes 4:25–5:32 — x', self.kar)
        self.assertEqual(t, [('1Móz', (4, 25), (5, 32))])
        t = T.tartomany_cimsorbol('# 1 Mózes 1:2 – 2:3 — Bővített', self.kar)
        self.assertEqual(t, [('1Móz', (1, 2), (2, 3))])

    def test_tobb_szegmens(self):
        t = T.tartomany_cimsorbol('# 1Mózes 14:18-20 / Zsoltárok 110:4 / Zsidók 5-7 — Mélyelemzés', self.kar)
        self.assertEqual([x[0] for x in t], ['1Móz', 'Zsolt', 'Zsid'])
        self.assertEqual(t[2][1], (5, 1))
        self.assertEqual(t[2][2][0], 7)

    def test_ertelmezhetetlen(self):
        self.assertIsNone(T.tartomany_cimsorbol('# Valami cím — x', self.kar))
        self.assertIsNone(T.tartomany_cimsorbol('# 1Mózes 14:20-18 — x', self.kar))   # fordított
        self.assertIsNone(T.tartomany_cimsorbol('# 1Mózes 14:99 — x', self.kar))      # nincs ilyen vers


class Kinyero(unittest.TestCase):
    def test_hivatkozas_fokozatok(self):
        d = tmp_gyoker({'genezis/1Moz_14v18-20_bovitett.md': MINTA})
        try:
            e = T.kinyer(d, KULCSOK)
        finally:
            shutil.rmtree(d)
        self.assertEqual(e.kihagyott, [])
        self.assertEqual([t.tanulmany_id for t in e.tanulmanyok], ['1Moz_14v18-20'])
        self.assertEqual(e.tanulmanyok[0].tartomany_szoveg, '1Móz 14:18–20')
        h = {(x.szakasz_horgony, x.igehely): x for x in e.hivatkozasok}
        # egyedi vers = nev, a tartományon belül
        self.assertEqual(h[('1-peshat', '1Móz 14:18')].fokozat, 'nev')
        self.assertEqual(h[('1-peshat', '1Móz 14:18')].tartomanyban, 1)
        # a „19–20. versben” tartomány-említés
        self.assertEqual(h[('1-peshat', '1Móz 14:19')].fokozat, 'tartomany')
        # külső vers név szerint bekerül, jelölve, hogy a tartományon kívül van
        self.assertEqual(h[('1-peshat', 'Zsolt 110:4')].fokozat, 'nev')
        self.assertEqual(h[('1-peshat', 'Zsolt 110:4')].tartomanyban, 0)
        # a tanulmány a 14:1-24 tartományt nevezi meg, ami nem a saját tartománya, de a tartományon kívüli
        # versekre (14:1) tartomány-említés nem kerül az indexbe (DT-F149b)
        self.assertNotIn(('1-peshat', '1Móz 14:1'), h)
        # a ### alszakasz saját horgony: a „18. v.” egyedi vers
        self.assertEqual(h[('alpont', '1Móz 14:18')].fokozat, 'nev')
        # a sorozat-kontextus és a fejléc nem kerül az indexbe
        self.assertFalse([x for x in e.hivatkozasok if x.szakasz_horgony in ('eleje', '0-sorozat-kontextus')])

    def test_eltero_cim_nem_kerul_be(self):
        d = tmp_gyoker({'genezis/1Moz_14v18-20_bovitett.md': MINTA.replace('14:18–20 —', '14:18–21 —', 1)})
        try:
            e = T.kinyer(d, KULCSOK)
        finally:
            shutil.rmtree(d)
        self.assertEqual(e.tanulmanyok, [])
        self.assertEqual(len(e.kihagyott), 1)
        self.assertIn('nem egyezik', e.kihagyott[0][1])
        self.assertIn('genezis/1Moz_14v18-20_bovitett.md', e.kihagyott[0][0])

    def test_sorozat_hezag_es_atfedes(self):
        def tan(fn, cim):
            return {fn: '# %s — x\n\n## 1. A\nszöveg 1Móz 1:1.\n' % cim}
        fajlok = {}
        fajlok.update(tan('genezis/1Moz_1v1_bovitett.md', '1Mózes 1:1'))
        fajlok.update(tan('genezis/1Moz_1v3-5_bovitett.md', '1Mózes 1:3–5'))      # hézag: 1:2
        fajlok.update(tan('genezis/1Moz_1v5-8_bovitett.md', '1Mózes 1:5–8'))      # átfedés: 1:5
        d = tmp_gyoker(fajlok)
        try:
            e = T.kinyer(d, KULCSOK)
        finally:
            shutil.rmtree(d)
        szoveg = '\n'.join(e.figyelmeztetesek)
        self.assertIn('hézag (1Móz): 1Móz 1:2 – 1Móz 1:2', szoveg)
        self.assertIn('átfedés (1Móz)', szoveg)

    def test_tablak_sema(self):
        d = tmp_gyoker({'genezis/1Moz_14v18-20_bovitett.md': MINTA})
        try:
            e = T.kinyer(d, KULCSOK)
        finally:
            shutil.rmtree(d)
        nevek = [t[0] for t in T.tablak(e)]
        self.assertEqual(nevek, ['tanulmany', 'tanulmany_tartomany', 'tanulmany_hivatkozas', 'tanulmany_szoveg'])
        for nev, oszl, sorok, _ in T.tablak(e):
            for s in sorok:
                self.assertEqual(len(s), len(oszl), nev)


class ValosAdat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = T.kinyer(ROOT, KULCSOK)

    def test_minden_tanulmany_kinyerheto(self):
        fajlok = {t.fajl for t in self.e.tanulmanyok}
        for k, minta in (('genezis', '_bovitett.md'), ('ujszovetseg', '_bovitett.md'), ('melyelemzesek', '_melyelemzes.md')):
            d = os.path.join(ROOT, k)
            for f in sorted(os.listdir(d)):
                if f.endswith(minta):
                    self.assertIn(k + '/' + f, fajlok)
        self.assertEqual(self.e.kihagyott, [])

    def test_genezis_sorozat_hezagtalan(self):
        self.assertEqual([x for x in self.e.figyelmeztetesek if '1Móz' in x], [])

    def test_melyelemzes_tobb_tartomany(self):
        m = [r for r in self.e.tartomanyok if r.tanulmany_id.startswith('1Mozes_14_18-20')]
        self.assertEqual([r.kezdo for r in m], ['1Móz 14:18', 'Zsolt 110:4', 'Zsid 5:1'])
        self.assertEqual(m[2].veg, 'Zsid 7:28')

    def test_a_forras_valtozatlan(self):
        # a kinyerő csak olvas: nincs írási út a forrásra (DT28) — a fájlok módosítási ideje nem változik
        p = os.path.join(ROOT, 'genezis', '1Moz_14_bovitett.md')
        elotte = os.path.getmtime(p)
        T.kinyer(ROOT, KULCSOK)
        self.assertEqual(os.path.getmtime(p), elotte)


if __name__ == '__main__':
    unittest.main(verbosity=1)
