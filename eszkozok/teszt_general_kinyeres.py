#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_general_kinyeres.py -- F11 M2 (FELADATOK #11): a `general.py --cel
kinyeres` (SEMA 3.10.5; DT-F11d (d)) tesztjei, alfolyamatkent futtatva.

Minden irt fajl (forras-fixture, kitalalt jelolt-tabla, kinyeresi jelentes)
ideiglenes, repon kivuli konyvtarba kerul (tempfile); az eles adat/,
lexikon/ es generalt_proba/ konyvtarat a teszt nem irja (az eles
adat/jeloltek.tsv bajtjait elotte es utana osszeveti). Az adat/ tobbi
tablajat (motivumok.tsv, a normalizalo tabla) csak olvassa.
Futtatas: python eszkozok/teszt_general_kinyeres.py
"""

import hashlib
import io
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

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ESZKOZOK)
GENERAL = os.path.join(ESZKOZOK, 'general.py')
ELES_JELOLTEK = os.path.join(REPO, 'adat', 'jeloltek.tsv')

JELOLTEK_FEJ = ('# próba-jelölttábla (teszt_general_kinyeres.py)\n'
                'id\tigehely\tforras_kereses\tdontes\tindoklas\tkaroli_szo\tazonositas_modja'
                '\tmegbizhatosag\tdatum\n'
                'ISTENTISZT-001\t1Móz 4:26\tTSK 1Móz 4:26\tbeépítve\tpróba-sor\t\t\t\t2026.10.01\n')

TISZTA = """# Próba — forrásréteg `[ID: ISTENTISZT-001]`

## 1. Előfordulások összegyűjtése

### Friss, teljes körű keresés (P1–P7)

<!-- JELÖLT: Zsolt 999:4 | gerinc: H7121 | próba: új jelölt -->
<!-- JELÖLT: 1Móz 4:26 | gerinc: H7121 | próba: a kulcs már létezik -->
<!-- JELÖLT: Zsolt 999:4 | gerinc: H7121 | próba: ismétlés -->
<!-- JELÖLT: ApCsel 99:1-3 | gerinc: G1941 | próba: tartomány, | jellel az indoklásban -->

[^p1]: proveniencia: scope=OT-full | forras=TAHOT_kivonat.tsv | ts=2026-10-18
"""

HIBAS = TISZTA + """
## 2. Eredeti nyelvi összevetés

Szám: 3<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count -->.
<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | BDB H7121 -->
<!-- ADAT-HIV: nincs_ilyen.tsv | x -->
<!-- JELÖLT: Nincskönyv 1:1 | gerinc: X | rossz könyv -->
<!-- JELÖLT: Zsolt 1:1 | rossz alak -->
"""

JELENTES = os.path.join('kinyeres', 'ISTENTISZT-001_kinyeresi_jelentes.md')


def md5(ut):
    with open(ut, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


class Kinyeres(unittest.TestCase):

    def setUp(self):
        self.eles_md5 = md5(ELES_JELOLTEK)
        self.tmp = tempfile.mkdtemp(prefix='teszt_kinyeres_')
        self.jel = os.path.join(self.tmp, 'jeloltek.tsv')
        with io.open(self.jel, 'w', encoding='utf-8', newline='') as f:
            f.write(JELOLTEK_FEJ)
        self.f_tiszta = os.path.join(self.tmp, 'tiszta.md')
        self.f_hibas = os.path.join(self.tmp, 'hibas.md')
        for ut, szoveg in ((self.f_tiszta, TISZTA), (self.f_hibas, HIBAS)):
            with io.open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write(szoveg)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        self.assertEqual(md5(ELES_JELOLTEK), self.eles_md5, 'az éles adat/jeloltek.tsv megváltozott')

    def futtat(self, forras, kimenet, ir):
        parancs = [sys.executable, GENERAL, '--cel', 'kinyeres', '--id', 'ISTENTISZT-001',
                   '--forras-fajl', forras, '--jeloltek-fajl', self.jel,
                   '--kimenet', os.path.join(self.tmp, kimenet)] + (['--ir'] if ir else [])
        env = dict(os.environ, PARDES_DATUM='2026-10-18', PYTHONIOENCODING='utf-8')
        p = subprocess.run(parancs, cwd=REPO, env=env, capture_output=True)
        return p.returncode, p.stderr.decode('utf-8')

    def jelentes(self, kimenet):
        with io.open(os.path.join(self.tmp, kimenet, JELENTES), encoding='utf-8') as f:
            return f.read()

    def olvas(self):
        with open(self.jel, 'rb') as f:
            return f.read()

    def test_1_ir_nelkul_csak_jelentes(self):
        eredeti = self.olvas()
        kod, hb = self.futtat(self.f_tiszta, 'ki1', False)
        self.assertEqual(kod, 0, hb[-300:])
        self.assertEqual(self.olvas(), eredeti)
        j = self.jelentes('ki1')
        self.assertIn('| új jelölt-sor | 2 |', j)
        self.assertIn('| ütközés (a kulcs már létezik, nem írva) | 1 |', j)
        self.assertIn('| ismétlődő JELÖLT a forrásban | 1 |', j)
        self.assertIn('javaslat: a tábla nem íródott', j)

    def test_2_ir_hozzafuz_meglevo_bajtok_valtozatlanok(self):
        eredeti = self.olvas()
        kod, hb = self.futtat(self.f_tiszta, 'ki2', True)
        self.assertEqual(kod, 0, hb[-300:])
        utana = self.olvas()
        self.assertTrue(utana.startswith(eredeti))
        uj = [u for u in utana[len(eredeti):].decode('utf-8').split('\n') if u]
        self.assertEqual(len(uj), 2)
        self.assertEqual(uj[0], 'ISTENTISZT-001\tZsolt 999:4\tscope=manual | forras=motivumok/'
                                'ISTENTISZT-001.md#1. Előfordulások összegyűjtése | ts=2026.10.18'
                                '\tnyitva\tgerinc: H7121 — próba: új jelölt\t\t\t\t2026.10.18')
        self.assertEqual(uj[1].split('\t')[4],
                         'gerinc: G1941 — próba: tartomány, | jellel az indoklásban')
        self.assertTrue(all(len(u.split('\t')) == 9 for u in uj))

    def test_3_ujrafuttatas_idempotens(self):
        self.futtat(self.f_tiszta, 'ki3a', True)
        elotte = self.olvas()
        kod, hb = self.futtat(self.f_tiszta, 'ki3b', True)
        self.assertEqual(kod, 0, hb[-300:])
        self.assertEqual(self.olvas(), elotte)

    def test_4_hibas_forras_nem_ir(self):
        eredeti = self.olvas()
        kod, _ = self.futtat(self.f_hibas, 'ki4', True)
        self.assertEqual(kod, 1)
        self.assertEqual(self.olvas(), eredeti)
        j = self.jelentes('ki4')
        for kell in ('rossz kulcs-alak', 'ismeretlen kifejezés', 'nincs_ilyen.tsv',
                     'normalizáló táblában', 'hibás JELÖLT-jelölő', 'a futás megállt'):
            with self.subTest(kell=kell):
                self.assertIn(kell, j)
        self.assertNotIn('auditok', j.split('## Hibák')[1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
