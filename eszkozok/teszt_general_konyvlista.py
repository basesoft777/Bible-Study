#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_general_konyvlista.py -- F179 (N-F09f): a `general.py` ÚSZ-könyvlistája
(UJSZOVETSEGI_TOKENEK) a konkordancia/Konyv_normalizalo_tabla.tsv-ből olvasott,
teljes Mt-Jel; a `konyv_teszamentum()` ezen alapul.

Futtatás: python eszkozok/teszt_general_konyvlista.py
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

# A 27 újszövetségi könyv magyar rövidítése, a normalizáló tábla alakjában.
USZ = ['Mt', 'Mk', 'Luk', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef',
       'Fil', 'Kol', '1Thessz', '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem',
       'Zsid', 'Jak', '1Pét', '2Pét', '1Ján', '2Ján', '3Ján', 'Júd', 'Jel']


class KonyvlistaTeszt(unittest.TestCase):

    def test_minden_usz_rovidites_felismerve(self):
        for token in USZ:
            self.assertEqual(G.konyv_teszamentum(token), 'ÚSZ', token)

    def test_huszonhet_konyv(self):
        self.assertEqual(len(USZ), 27)
        self.assertEqual(set(USZ), set(G.UJSZOVETSEGI_TOKENEK))

    def test_a_tabla_minden_nem_usz_sora_osz(self):
        _, sorok = G.tsv_beolvas(G.KONYV_NORMALIZALO_TSV)
        osz = [s['Magyar rövidítés'] for s in sorok if s['Magyar rövidítés'] not in USZ]
        self.assertEqual(len(osz), 39)
        for token in osz:
            self.assertEqual(G.konyv_teszamentum(token), 'ÓSZ', token)

    def test_gal_3_13_usz(self):
        tok = G.konyv_token('Gal 3:13')
        self.assertEqual(tok, 'Gal')
        self.assertEqual(G.konyv_teszamentum(tok), 'ÚSZ')

    def test_szamozott_es_ekezetes_tokenek(self):
        for igehely, vart in (('1Ján 3:4', 'ÚSZ'), ('Ján 3:16', 'ÚSZ'), ('Mk 7:21-23', 'ÚSZ'),
                              ('1Móz 3:16', 'ÓSZ'), ('Jób 1:1', 'ÓSZ'), ('Zsolt 51:7', 'ÓSZ')):
            self.assertEqual(G.konyv_teszamentum(G.konyv_token(igehely)), vart, igehely)


if __name__ == '__main__':
    unittest.main()
