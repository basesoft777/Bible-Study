#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_general_forras.py -- F11 M2 (FELADATOK #11): a `general.py` forras-
olvasojanak (szintszures, SEMA 3.10.1-3.10.4; DT-F11d (a)) tesztjei.

A fixture a tesztben all; a teszt fajlt nem ir (a nezet memoriaban keszul).
Futtatas: python eszkozok/teszt_general_forras.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ESZKOZOK)
import general as G  # noqa: E402
from ellenorzes import szabalyok as SZ  # noqa: E402

FIXTURE = """# Próba-motívum — forrásréteg `[ID: ISTENTISZT-001]`

<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. NEM generált fájl. -->

【NAPLO: fejléc-proveniencia, 2026.10.18.】

## Kivonat

<!-- RÉS-KEZDET: kivonat -->
OLVASOI-KIVONAT mondat. Az előfordulások száma 4<!-- ADAT-ÉRTÉK: elofordulasok.tsv | x --> csoportban.
<!-- RÉS-VÉGE: kivonat -->

Közbülső mondat 【NAPLO: inline nyom, 2026.10.18.】 és folytatás.

<!-- INAKTÍV: 0. Forrás-összegyűjtés a meglévő anyagból — a feltétel nem áll fenn: próba -->

## 1. Előfordulások összegyűjtése

APPARATUS-KISERO próza az 1. szakaszban.

### Friss, teljes körű keresés (P1–P7)

BELSO-P1P7 levezetés.

<!-- JELÖLT: Zsolt 116:4 | gerinc: H7121 | a P3 scan új találata -->

### Logikai kötőszó szerinti bontás

APPARATUS-1L bontás.

<!-- ADAT-NÉZET: 1. pont, 7 oszlopos előfordulás-tábla | forrás: adat/elofordulasok.tsv | cél: general.py --cel study | SZINT: apparatus -->

<!-- SZINT-KEZDET: belso -->
BELSO-BLOKK az 1. szakaszban.

【NAPLO: több soros
napló-blokk, 2026.10.18.】
<!-- SZINT-VÉGE: belso -->

## 2. Eredeti nyelvi összevetés

APPARATUS-2 próza.
<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | BDB H7121 -->

## 3. A PaRDeS keretrendszer — a motívumra alkalmazva

OLVASOI-3 próza.

<!-- SZINT-KEZDET: apparatus -->
APPARATUS-3-BLOKK.
<!-- SZINT-VÉGE: apparatus -->

## 7. Nyitott kérdések

<!-- ADAT-NÉZET: Minőségi kapu (Q1–Q7) | eredménye adat, a próza nem írja be | SZINT: belso -->

APPARATUS-7N tétel.

## Proveniencia-sorok

[^p1]: proveniencia: scope=OT-full | forras=TAHOT_kivonat.tsv | ts=2026-10-18

## Tematikus áttekintés — a napló mai tétele *(archív)*

ISMERETLEN-ARCHIV szöveg.
"""

NEGATIV = {
    'párosítatlan KEZDET': '## 1. X\n<!-- SZINT-KEZDET: belso -->\nszöveg\n',
    'párosítatlan VÉGE': '## 1. X\n<!-- SZINT-VÉGE: belso -->\n',
    'ellentmondó pár': '## 1. X\n<!-- SZINT-KEZDET: belso -->\n<!-- SZINT-VÉGE: apparatus -->\n',
    '## átnyúlás': '## 1. X\n<!-- SZINT-KEZDET: belso -->\n## 2. Y\n<!-- SZINT-VÉGE: belso -->\n',
    'sekélyebb váltás': '## 0. X\n<!-- SZINT-KEZDET: olvasoi -->\nx\n<!-- SZINT-VÉGE: olvasoi -->\n',
    '#64 egyjelölős alak': '<!-- SZINT: belso -->\n## Kivonat\n',
    'ismeretlen szint': '## 1. X\n<!-- SZINT-KEZDET: titkos -->\n<!-- SZINT-VÉGE: titkos -->\n',
    'generált jelölő': '## Kivonat\n<!-- GENERÁLT-KEZDET: general.py --cel x | ts=1 -->\n',
    'ÜRES-BLOKK': '## Kivonat\n<!-- ÜRES-BLOKK: 3 | x -->\n',
    'lezáratlan NAPLO': '## Kivonat\n【NAPLO: nincs vége\n',
    'soron belüli JELÖLT': '## Kivonat\nszöveg <!-- JELÖLT: Zsolt 1:1 | gerinc: X | y --> tovább\n',
    'soron belüli ADAT-HIV': '## Kivonat\nszöveg <!-- ADAT-HIV: a.tsv | k -->\n',
    'soron belüli INAKTÍV': '## Kivonat\nszöveg <!-- INAKTÍV: 4. — ok -->\n',
    'soron belüli RÉS-KEZDET': '## Kivonat\nszöveg <!-- RÉS-KEZDET: kivonat --> x\n',
    'soron belüli FORRÁSRÉTEG': '## Kivonat\nx <!-- FORRÁSRÉTEG (F4 G2) -->\n',
}


class Nezetek(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.olv, _ = G.forras_nezet(FIXTURE, 'olvasoi')
        cls.app, cls.stat = G.forras_nezet(FIXTURE, 'apparatus')
        cls.bel, _ = G.forras_nezet(FIXTURE, 'belso')

    def test_kiadhato_nezetben_nincs_e29_minta(self):
        for nev, nezet, mintak in (('olvasoi', self.olv, SZ.E29_MINTAK + SZ.E29_OLVASOI_TOVABBI),
                                   ('apparatus', self.app, SZ.E29_MINTAK)):
            for m in mintak:
                with self.subTest(nezet=nev, minta=m):
                    self.assertNotIn(m, nezet)

    def test_belso_tartalom_nem_jut_ki(self):
        for nezet in (self.olv, self.app):
            for tilt in ('BELSO-', 'ISMERETLEN-ARCHIV', 'proveniencia:', 'Próba-motívum'):
                with self.subTest(tilt=tilt):
                    self.assertNotIn(tilt, nezet)

    def test_olvasoi_tartalom_mindket_nezetben(self):
        for nezet in (self.olv, self.app):
            self.assertIn('OLVASOI-KIVONAT', nezet)
            self.assertIn('OLVASOI-3', nezet)
            self.assertIn('4 csoportban', nezet)                 # ADAT-ÉRTÉK: az érték marad
            self.assertIn('Közbülső mondat  és folytatás.', nezet)  # inline NAPLO kivágva

    def test_olvasoi_nezetben_nincs_apparatus(self):
        self.assertNotIn('APPARATUS-', self.olv)
        self.assertNotIn('ADAT-NÉZET', self.olv)

    def test_apparatus_nezet_tartalma(self):
        for kell in ('APPARATUS-KISERO', 'APPARATUS-1L', 'APPARATUS-2', 'APPARATUS-3-BLOKK',
                     'APPARATUS-7N', 'RÉS-KEZDET: kivonat', 'SZINT: apparatus -->'):
            with self.subTest(kell=kell):
                self.assertIn(kell, self.app)
        self.assertNotIn('Minőségi kapu', self.app)   # a belso ADAT-NÉZET kimarad

    def test_ures_sor_sorozat_nincs(self):
        self.assertNotIn('\n\n\n', self.app)
        self.assertNotIn('\n\n\n', self.olv)

    def test_belso_nezet_a_forras_maga(self):
        self.assertEqual(self.bel, FIXTURE)

    def test_ismeretlen_szakasz_figyelmeztetes(self):
        self.assertTrue(any('ismeretlen szakasz' in f for f in self.stat['figyelmeztetesek']))


class NegativEsetek(unittest.TestCase):

    def test_mind_forrashiba(self):
        self.assertEqual(len(NEGATIV), 15)
        for nev, forras in NEGATIV.items():
            with self.subTest(eset=nev):
                with self.assertRaises(G.ForrasHiba):
                    G.forras_nezet(forras, 'apparatus')


class PLepesFigyelmeztetes(unittest.TestCase):
    """DT-F11d (a): az 1. szakasz P-lépést említő, nem belso alcíme."""

    @staticmethod
    def _figy(forras):
        _, st = G.forras_nezet(forras, 'apparatus')
        return [f for f in st['figyelmeztetesek'] if 'P-lépést említő' in f]

    def test_figyelmeztet(self):
        self.assertTrue(self._figy('## 1. X\n\n### A P2 indoklása\n\nszöveg\n'))

    def test_nem_figyelmeztet(self):
        for nev, forras in (
                ('1.P alcím', '## 1. X\n\n### Friss keresés (P1–P7)\n\nx\n'),
                ('belso pár', '## 1. X\n<!-- SZINT-KEZDET: belso -->\n### A P3 scan\nx\n'
                              '<!-- SZINT-VÉGE: belso -->\n'),
                ('nem 1. szakasz', '## 3. X\n\n### P2 a 3. szakaszban\n'),
                ('fixture', FIXTURE)):
            with self.subTest(eset=nev):
                self.assertFalse(self._figy(forras))


if __name__ == '__main__':
    unittest.main(verbosity=2)
