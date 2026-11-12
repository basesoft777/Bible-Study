#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_32.py -- F123.KIADVEG: az eszkozok/ellenoriz.py 32.
szabályának (olvasói kapu a kiadott lapokon) tesztjei.

Ideiglenes (a repón kívüli) adat/ és lexikon/ könyvtárban fut; a lap a repó
élő ALVIL-001 lapjának másolata (0 BUKÁS), a negatív esetekben egy belső
jelöléssel (döntés-azonosító) rontva. Kiadott lapon a szabálynak SÉRTÉS-t, ki
nem adott lapon JELENTÉS-t kell adnia.

    python eszkozok/teszt_ellenoriz_32.py
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

import ellenoriz as E  # noqa: E402

T, N = '\t', '\n'
MOTIVUM = 'ALVIL-001'   # F194: az ISTENTISZT-001 új szerkezetű lett; a régi szerkezet mintája a befagyasztott ALVIL-001
LAP = os.path.join(E.ROOT, 'lexikon', '%s_TUDOMANYOS.md' % MOTIVUM)
FEJLEC = ['id', 'kiadas', 'datum', 'valtozas', 'proza_modell', 'forras']
# egy olvasói bekezdés a 1. blokk címe után: a döntés-azonosító a kapu BELSO-szabályán BUKÁS
RONTAS = 'A DT123 szerint a motívum így áll.'


def _lap():
    with open(LAP, encoding='utf-8') as fh:
        return fh.read().replace('\r\n', '\n')


def _ront(lap):
    cim = '## 1. Előfordulások\n'
    i = lap.index(cim) + len(cim)
    return lap[:i] + '\n' + RONTAS + '\n' + lap[i:]


class Szabaly32(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='teszt_ellenoriz_32_')
        self.adat = os.path.join(self.tmp, 'adat')
        self.lex = os.path.join(self.tmp, 'lexikon')
        os.makedirs(self.adat)
        os.makedirs(self.lex)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def kiadas(self, *idk):
        with open(os.path.join(self.adat, 'kiadasok.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('# megjegyzés' + N + T.join(FEJLEC) + N)
            for mid in idk:
                f.write(T.join([mid, '1', '2026.11.04', 'próba', 'manual',
                                'scope=manual | forras=teszt | ts=2026-11-04']) + N)

    def lap(self, mid, szoveg):
        with open(os.path.join(self.lex, mid + '_TUDOMANYOS.md'), 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)

    def futtat(self):
        return E.szabaly32_olvasoi_kapu_kiadott(self.adat)

    def test_kiadott_tiszta_lap_rendben(self):
        self.kiadas(MOTIVUM)
        self.lap(MOTIVUM, _lap())
        self.assertEqual(self.futtat().verdict, 'RENDBEN')

    def test_kiadott_bukasos_lap_sertes(self):
        self.kiadas(MOTIVUM)
        self.lap(MOTIVUM, _ront(_lap()))
        s = self.futtat()
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertTrue(any(p.startswith('%s (kiadott)' % MOTIVUM) and 'BELSO' in p for p in s.peldak), s.peldak)

    def test_ki_nem_adott_bukasos_lap_jelentes(self):
        self.kiadas()
        self.lap(MOTIVUM, _ront(_lap()))
        s = self.futtat()
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertTrue(any('nincs kiadva' in p for p in s.peldak), s.peldak)

    def test_vegyes_a_kiadott_dont(self):
        self.kiadas(MOTIVUM)
        self.lap(MOTIVUM, _lap())
        self.lap('MASIK-001', _ront(_lap()))
        self.assertEqual(self.futtat().verdict, 'JELENTÉS')
        self.kiadas(MOTIVUM, 'MASIK-001')
        self.assertEqual(self.futtat().verdict, 'SÉRTÉS')

    def test_kiadott_lap_nelkul_sertes(self):
        self.kiadas('NINCSLAP-001')
        s = self.futtat()
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('NINCSLAP-001', s.peldak[0])

    def test_nincs_kiadasok_tabla(self):
        self.lap(MOTIVUM, _lap())
        self.assertEqual(self.futtat().verdict, 'RENDBEN')

    def test_nincs_lexikon_konyvtar(self):
        shutil.rmtree(self.lex)
        self.assertEqual(self.futtat().verdict, 'KÉZI')

    def test_repo_mai_allapota(self):
        # a repó élő adatán: minden kiadott lap 0 BUKÁS
        self.assertNotEqual(E.szabaly32_olvasoi_kapu_kiadott(os.path.join(E.ROOT, 'adat')).verdict, 'SÉRTÉS')


if __name__ == '__main__':
    unittest.main(verbosity=2)
