#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_bdb_zaras.py -- F38 zaromenet (DT-F38e): adat-regresszio az
adat/forditasok.tsv F38-as soraira.

  - minden `F38 BDB_FORDITAS` megjegyzesu soron allapot=sonnet es
    modell=claude-sonnet-5-5 (nincs `opus` allapot / `claude-opus` modell);
  - a #28 sorai (nem F38-as) nem kaptak sonnet cimket;
  - a szellem-lista (naplok/BDB_FORDITAS_szellem.py) minden cserejet
    tartalmazza a sor, a regi reszlet nincs benne;
  - a teljes kapusor (a sor terminologia-kiveteleivel) atmegy minden F38-as soron;
  - az uj normalizalo-szabalyok mar nem talalnak javitando helyet az F38-as sorokon;
  - DT-F38f: ugyanez a #28 sorokra is (a kapusor es a normalizalo), az `allapot` es a
    `modell` valtozatlan; a RV/AV kezi javitasok megvannak; nincs szocikkszintu `spirit`-kivetel.

    python eszkozok/teszt_bdb_zaras.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'naplok'))

import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
import normalizal as N  # noqa: E402
from BDB_FORDITAS_szellem import SZELLEM  # noqa: E402
from BDB_FORDITAS_ujranormalizal import kivetelek  # noqa: E402
from BDB_FORDITAS_zaras2 import RV_KEZI  # noqa: E402

JEL = 'F38 BDB_FORDITAS'


def f38_sorok():
    ki = []
    for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
        if r['szotar'] == 'BDB' and r['jelentes_szam'] == 'teljes':
            ki.append(r)
    return ki


class Cimkek(unittest.TestCase):
    def test_f38_sorok_sonnet(self):
        db = 0
        for r in f38_sorok():
            if JEL in r['megjegyzes']:
                db += 1
                self.assertEqual(r['allapot'], 'sonnet', r['strong'])
                self.assertEqual(r['modell'], 'claude-sonnet-5-5', r['strong'])
        self.assertGreaterEqual(db, 243)

    def test_nincs_opus_cimke_f38_soron(self):
        for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
            if JEL in r['megjegyzes']:
                self.assertNotIn('opus', r['allapot'] + r['modell'], r['strong'])

    def test_28_sorai_nem_sonnet(self):
        for r in E.tsv_dict_sorok(E.FORDITASOK_UT):
            if JEL not in r['megjegyzes']:
                self.assertNotEqual(r['allapot'], 'sonnet', r['strong'])


class Szellem(unittest.TestCase):
    def test_lista_alkalmazva(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        for strong, pont, regi, uj, _ in SZELLEM:
            hu = sorok[E.strong_padded(strong)]['forditas_hu']
            self.assertEqual(hu.count(uj), 1, (strong, pont))
            self.assertEqual(hu.count(regi), 0, (strong, pont))


class Kapuk(unittest.TestCase):
    def test_kapusor_atmegy_f38_soron(self):
        for r in f38_sorok():
            if JEL not in r['megjegyzes']:
                continue
            sp, forras = E.forras_szoveg(r['strong'])
            eredm = K.kapuk_futtat('BDB', forras, r['forditas_hu'], bizonytalan=kivetelek(r['megjegyzes']))
            self.assertTrue(K.atment(eredm), (r['strong'], [x for x in eredm if x[1] == 'SERTES']))

    def test_normalizalo_nem_talal_javitando_helyet(self):
        for r in f38_sorok():
            if JEL not in r['megjegyzes']:
                continue
            uj, valt = N.normalizal(r['forditas_hu'], 'BDB')
            self.assertEqual(valt, [], (r['strong'], valt))
            self.assertEqual(uj, r['forditas_hu'])


class DTF38f(unittest.TestCase):
    """DT-F38f (2026.10.02): a #28 sorain is ervenyesek a gepi szabalyok; a RV/AV-
    esetek angolul maradnak; a spirit-kivetel megszunt; a maradek `N t.` listan."""

    def test_28_sorai_kapusor_es_normalizalo(self):
        db = 0
        for r in f38_sorok():
            if JEL in r['megjegyzes']:
                continue
            db += 1
            sp, forras = E.forras_szoveg(r['strong'])
            eredm = K.kapuk_futtat('BDB', forras, r['forditas_hu'], bizonytalan=kivetelek(r['megjegyzes']))
            self.assertTrue(K.atment(eredm), (r['strong'], [x for x in eredm if x[1] == 'SERTES']))
            uj, valt = N.normalizal(r['forditas_hu'], 'BDB')
            self.assertEqual(valt, [], (r['strong'], valt))
            self.assertEqual(N.glossza_visszaallit(forras, r['forditas_hu'])[1], [], r['strong'])
        self.assertEqual(db, 26)

    def test_28_cimkek_valtozatlanok(self):
        for r in f38_sorok():
            if JEL not in r['megjegyzes']:
                self.assertIn(r['allapot'], ('kezi', 'opus'), r['strong'])
                self.assertNotIn('sonnet', r['modell'], r['strong'])

    def test_rv_av_kezi_javitasok(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        for strong, regi, uj in RV_KEZI:
            hu = sorok[strong]['forditas_hu']
            self.assertEqual(hu.count(uj), 1, strong)
            self.assertEqual(hu.count(regi), 0, strong)

    def test_nincs_szocikkszintu_spirit_kivetel(self):
        for r in f38_sorok():
            self.assertNotIn('spirit', kivetelek(r['megjegyzes']), r['strong'])

    def test_maradek_n_t_csak_a_listan_szereplo(self):
        import re
        minta = re.compile(r'\d\s?t\.(?![\w])')
        marad = {}
        for r in f38_sorok():
            if minta.search(r['forditas_hu']):
                marad[r['strong']] = len(minta.findall(r['forditas_hu']))
        # H7043: `Ges §67 t.` (nyelvtani §, nem gyakoriság); H4264: `33:816t.` (a vers és a
        # darabszám összeforrt); H4687: `Zsolt 119:20 t.` (szám nélküli t. vagy 119. zsoltár 20-szor)
        self.assertEqual(marad, {'H7043': 1, 'H4264': 1, 'H4687': 1})

    def test_szellem_nagybetus_a_h1320_ban(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        self.assertIn('nem Szellem Ézs 31:3', sorok['H1320']['forditas_hu'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
