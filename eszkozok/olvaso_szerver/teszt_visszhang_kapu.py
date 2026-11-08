#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_visszhang_kapu.py -- F178.5 (DT-F178d, DT-F178e): a 4.11 visszhang-blokk regressziós
kapuja (`olvasoi_kapu.ell_visszhang`, V1–V6). Arany minta: a HAMART-001 lapjának 4.11 blokkja — a kapu ott 0 BUKÁS-t ad;
egy-egy szándékosan rontott másolaton szabályonként jelez. A `teszt_futtat.py --gyors` része.

    python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ESZKOZOK)
import olvasoi_kapu as K  # noqa: E402

LAP = os.path.join(os.path.dirname(ESZKOZOK), 'lexikon', 'HAMART-001_TUDOMANYOS.md')


def arany_blokk():
    """A HAMART-001 4.11 blokkja (a „#### 4.11.” címtől a „#### 4.12.” címig), a fölötte álló szakaszcímmel."""
    with open(LAP, encoding='utf-8') as f:
        t = f.read().replace('\r\n', '\n')
    a = t.index('#### 4.11. ')
    b = t.index('#### 4.12. ', a)
    return '## 4. Szótári háttér\n\n' + t[a:b]


def visszhang(szoveg):
    return [x for x in K.ell_visszhang(K.tagol(szoveg)) if x['sulyossag'] == K.BUKAS]


def szabalyok(szoveg):
    return {x['uzenet'].split(' ', 1)[0] for x in visszhang(szoveg)}


class Arany(unittest.TestCase):
    def test_hamart_4_11_tiszta(self):
        self.assertEqual([], visszhang(arany_blokk()))

    def test_hamart_teljes_lap_nincs_visszhang_bukas(self):
        with open(LAP, encoding='utf-8') as f:
            tal, _ = K.lap_meres(f.read(), kh=False, atvett=False, arany=False)
        self.assertFalse([t for t in tal if t['azonosito'] == 'VISSZHANG' and t['sulyossag'] == K.BUKAS])


class Rontott(unittest.TestCase):
    def setUp(self):
        self.b = arany_blokk()

    def test_v1_angol_maradek(self):
        r = self.b.replace('| megvet, meggyaláz |', '| megvet, meggyaláz; see be shaken |', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V1', szabalyok(r))

    def test_v2_ujheber_sor(self):
        sor = '| קָלַל (kálal) — könnyűnek lenni | újhéber קָלַל (kálal) | azonos a bibliai héberrel | — |'
        r = self.b.rstrip('\n') + '\n' + sor + '\n'
        self.assertIn('V2', szabalyok(r))

    def test_v3_nincs_a_nem_azonositott_helyen(self):
        r = self.b.replace('a rokon írások lekérdezése a BDB-szócikket nem azonosította; a helyi BDB-szövegben rokon '
                           'nyelvi alak nem áll', 'a BDB-szócikkben nincs rokon nyelvi adat', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V3', szabalyok(r))

    def test_v3_azonositott_szocikknel_nincs_rendben(self):
        self.assertNotIn('V3', szabalyok(self.b))   # chámász: azonosított szócikk, rokon alak nélkül

    def test_v4_ugyanaz_a_szo_ket_lemmanal(self):
        r = self.b.replace('A LXX: ugyanaz a szócsalád mind a 3 láncversben; a láncon kívül',
                           'A LXX: ugyanaz a szó mind a 3 láncversben; a láncon kívül', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V4', szabalyok(r))

    def test_v5_kiemelt_alapvonal_nelkul(self):
        r = self.b.replace('A Targum: ugyanaz a szó mind a 4 láncversben; hogy ez a szó szokásos fordítása-e, ebből a '
                           'forrásból nem mérhető.', '**A Targum: ugyanaz a szó mind a 4 láncversben.**', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V5', szabalyok(r))

    def test_v6_sablonmondat_ismetles(self):
        sor = ('| X<br>1:1 | a · 1/1 | b · 1/1 | c · 1/1 | Ugyanaz a fordítás minden láncversben, a lánc egységként '
               'hallatszik. |')
        r = self.b.replace('| nincs héber szó', '\n'.join([sor] * 3) + '\n| nincs héber szó', 1)
        self.assertNotEqual(r, self.b)
        self.assertIn('V6', szabalyok(r))


if __name__ == '__main__':
    unittest.main()
