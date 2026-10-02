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

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

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
import BDB_FORDITAS_zaras3 as Z3  # noqa: E402
from BDB_FORDITAS_zaras3 import KEZI3, MEGJ3, SZELLEM_KOVETELT, alkalmaz, szellem_ellenorzes  # noqa: E402

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
            if strong in ('H3772', 'H4397'):
                continue  # a DT-F38g (1), (4) felulirta: l. test_dtf38g_kezi_javitasok
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
        # H7043: `Ges §67 t.` (nyelvtani §, nem gyakoriság); H4687: `Zsolt 119:20 t.` (szám nélküli
        # t. vagy 119. zsoltár 20-szor). A H4264 `33:816t.` a DT-F38g (5) szerint `33:8, összesen 16-szor`.
        self.assertEqual(marad, {'H7043': 1, 'H4687': 1})

    def test_szellem_nagybetus_a_h1320_ban(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        self.assertIn('nem Szellem Ézs 31:3', sorok['H1320']['forditas_hu'])


class DTF38g(unittest.TestCase):
    """DT-F38g (2026.10.02): az ellenori hat elteres kezelese; a Szellem-tabla nagybetus helyei."""

    def test_dtf38g_kezi_javitasok(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        for strong, nev, regi, uj, iras in KEZI3:
            hu = sorok[strong]['forditas_hu']
            self.assertEqual(hu.count(uj), 1, strong)
            if regi not in uj:  # a H5674 uj szovege tartalmazza a regit (beszurt `a Szellemről`)
                self.assertEqual(hu.count(regi), 0, strong)

    def test_h3772_h4397_h4264_szoveg(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        self.assertIn('rendszerint így fordítják: RV made for thee a covenant with them,', sorok['H3772']['forditas_hu'])
        self.assertIn('(az RV angel szava túl szűk)', sorok['H4397']['forditas_hu'])
        self.assertIn('1Móz 33:8, összesen 16-szor', sorok['H4264']['forditas_hu'])

    def test_h2403_jeloles_kezi(self):
        sorok = {r['strong']: r for r in f38_sorok()}
        megj = sorok['H2403']['megjegyzes']
        self.assertIn('kézi javítás', megj)
        self.assertNotIn('gépi szabályok a #28 soron', megj)

    def test_szellem_tabla_nagybetus_helyei(self):
        hu = {r['strong']: r['forditas_hu'] for r in f38_sorok()}
        hibak, osszes = szellem_ellenorzes(hu)
        self.assertEqual(hibak, [])
        self.assertEqual(osszes, sum(len(v) for v in SZELLEM_KOVETELT.values()))

    def test_elihu_es_rossz_szellem_kisbetus(self):
        hu = {r['strong']: r['forditas_hu'] for r in f38_sorok()}
        self.assertIn('Jób 32:18 (Du: lehelet; Di Bu: isteni Szellem', hu['H7307'])
        self.assertIn('az isteni szellemről, amely az őrjöngés', hu['H7451'])
        self.assertIn('Saul Istentől való gonosz szelleméről', hu['H1961'])
        self.assertIn('a szellemről 4Móz 5:14', hu['H5674'])


class Zaras3Idempotencia(unittest.TestCase):
    """DT-F38g, ellenori 6. eltérés: a `BDB_FORDITAS_zaras3.py --ir` újrafuttatható."""

    def test_alkalmaz_ketszer_ugyanaz(self):
        for sp, nev, regi, uj, iras in KEZI3:
            alap = 'elő %s utó' % regi
            elso, valt1 = alkalmaz(alap, regi, uj)
            self.assertTrue(valt1, sp)
            self.assertEqual(elso.count(uj), 1, sp)
            masodik, valt2 = alkalmaz(elso, regi, uj)
            self.assertFalse(valt2, sp)
            self.assertEqual(masodik, elso, sp)

    def test_h5674_regi_resze_az_ujnak(self):
        sp, nev, regi, uj, iras = [k for k in KEZI3 if k[0] == 'H5674'][0]
        self.assertIn(regi, uj)  # ez volt a duplikálás oka
        elso, _ = alkalmaz('x ' + regi, regi, uj)
        self.assertEqual(alkalmaz(elso, regi, uj)[0].count('a Szellemről a Szellemről'), 0)

    def test_se_regi_se_uj_hiba(self):
        with self.assertRaises(SystemExit):
            alkalmaz('semmi', 'regi', 'uj')
        with self.assertRaises(SystemExit):
            alkalmaz('regi regi', 'regi', 'uj')

    def test_ir_ketszer_futtatva_nem_duplikal(self):
        ix = {n: i for i, n in enumerate(E.FORDITASOK_FEJLEC)}
        with open(E.FORDITASOK_UT, encoding='utf-8', newline='') as fh:
            jelen = fh.read()
        with open(Z3.KIMENET, encoding='utf-8', newline='') as fh:
            lista = fh.read()
        # a zaras3 elotti allapot: az uj reszletek visszacserelve, a 4 listasor es a H2403 jeloles nelkul
        sorok = jelen.split('\n')
        for i, sor in enumerate(sorok):
            m = sor.split('\t')
            if len(m) != 12 or m[0] != 'BDB' or m[3] != 'teljes':
                continue
            for sp, nev, regi, uj, iras in KEZI3:
                if m[1] == sp:
                    m[ix['forditas_hu']] = m[ix['forditas_hu']].replace(uj, regi)
            if m[1] in MEGJ3:
                regi_j, uj_j = MEGJ3[m[1]]
                m[ix['megjegyzes']] = m[ix['megjegyzes']].replace(uj_j, regi_j)
            sorok[i] = '\t'.join(m)
        elo = '\n'.join(sorok)
        self.assertNotEqual(elo, jelen)
        lsorok = lista.split('\n')
        self.assertEqual(lsorok[-1], '')
        elo_lista = '\n'.join(lsorok[:-5]) + '\n'
        self.assertEqual(['\t'.join(j) for j in
                          [(sp, nev, regi, uj, '1', iras) for sp, nev, regi, uj, iras in KEZI3]],
                         lsorok[-5:-1])
        tmp = tempfile.mkdtemp()
        try:
            tab = os.path.join(tmp, 'forditasok.tsv')
            lis = os.path.join(tmp, 'javitasok.tsv')
            with open(tab, 'w', encoding='utf-8', newline='') as fh:
                fh.write(elo)
            with open(lis, 'w', encoding='utf-8', newline='') as fh:
                fh.write(elo_lista)
            ered = []
            with mock.patch.object(E, 'FORDITASOK_UT', tab), mock.patch.object(Z3, 'KIMENET', lis),                     mock.patch.object(sys, 'argv', ['zaras3.py', '--ir']):
                for _ in range(3):
                    with contextlib.redirect_stdout(io.StringIO()):
                        Z3.main()
                    with open(tab, encoding='utf-8', newline='') as fh:
                        t = fh.read()
                    with open(lis, encoding='utf-8', newline='') as fh:
                        l = fh.read()
                    ered.append((t, l))
            self.assertEqual(ered[0][0], jelen)
            self.assertEqual(ered[0][1], lista)
            self.assertEqual(ered[1], ered[0])
            self.assertEqual(ered[2], ered[0])
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main(verbosity=2)
