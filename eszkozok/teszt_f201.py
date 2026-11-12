#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F201: feladatszam-foglalas (atomi, tavoli agak), gepi commit-uzenet, foglalas-takaritas."""

import os
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402
import foglalas_takarit as T  # noqa: E402
import gepi_commit_uzenet as U  # noqa: E402


def git(cwd, *a):
    return subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'core.autocrlf=false'] + list(a),
                          cwd=cwd, capture_output=True, check=True).stdout.decode('utf-8')


class TavoliSzamTeszt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self.orig = os.path.join(t, 'orig.git')
        subprocess.run(['git', 'init', '-q', '--bare', self.orig], check=True)
        self.a, self.b = os.path.join(t, 'a'), os.path.join(t, 'b')
        subprocess.run(['git', 'init', '-q', '-b', 'main', self.a], check=True)
        git(self.a, 'remote', 'add', 'origin', self.orig)
        with open(os.path.join(self.a, 'F150_X_BRIEF.md'), 'w') as f:
            f.write('x')
        git(self.a, 'add', '-A')
        git(self.a, 'commit', '-qm', 'init')
        git(self.a, 'push', '-q', 'origin', 'main')
        subprocess.run(['git', 'clone', '-q', self.orig, self.b], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_tavoli_ag_briefje_szamit(self):
        git(self.a, 'checkout', '-q', '-b', 'claude/x')
        with open(os.path.join(self.a, 'F151_Y_BRIEF.md'), 'w') as f:
            f.write('y')
        git(self.a, 'add', '-A')
        git(self.a, 'commit', '-qm', 'y')
        git(self.a, 'push', '-q', 'origin', 'claude/x')
        self.assertEqual(F.kovetkezo_szam_tavoli([], self.b), 152)

    def test_foglalas_nem_ad_ket_agnak_ugyanazt(self):
        n1 = F.foglal([], self.a, 'ag-a')
        n2 = F.foglal([], self.b, 'ag-b')
        self.assertEqual((n1, n2), (151, 152))

    def test_foglalas_versenyhelyzet_ujraprobal(self):
        # b nem latja a2 foglalast a sajat szamolasakor (frissit=False), a push mégis atomian elbukik, es kovetkezot kap
        n1 = F.foglal([], self.a, 'ag-a')
        git(self.b, 'fetch', '-q')
        git(self.b, 'remote', 'prune', 'origin')
        # elavult nezet: a foglalas-agat helyben letoroljuk, mintha a b nem latna
        git(self.b, 'update-ref', '-d', 'refs/remotes/origin/foglalas/F%d' % n1)
        n2 = F.foglal([], self.b, 'ag-b', frissit=False)
        self.assertNotEqual(n1, n2)
        self.assertEqual(n2, n1 + 1)

    def test_takaritas_torli_a_teljesult_foglalast(self):
        n = F.foglal([], self.a, 'ag-a')
        self.assertEqual(T.teljesult(self.b), [])
        with open(os.path.join(self.a, 'F%d_Z_BRIEF.md' % n), 'w') as f:
            f.write('z')
        git(self.a, 'add', '-A')
        git(self.a, 'commit', '-qm', 'z')
        git(self.a, 'push', '-q', 'origin', 'main')
        self.assertEqual(T.teljesult(self.b), [n])


class UzenetTeszt(unittest.TestCase):
    def test_szamkiosztas_elso_sora_valtozatlan(self):
        u = U.uzenet(['DONTESEK.md', 'lexikon/HAMART-001_TUDOMANYOS.md', 'nyilt_mag/README.md', 'FELADATOK.md'],
                     'szamkiosztas: DT-F1a → DT7\n')
        self.assertTrue(u.startswith('szamkiosztas: DT-F1a → DT7\n'))
        self.assertIn('lexikonlapok újragenerálva', u)
        self.assertIn('nyílt mag újragenerálva', u)

    def test_csak_feladatok(self):
        self.assertTrue(U.uzenet(['FELADATOK.md', 'feladatterkep.json']).startswith('FELADATOK.md frissítés (gép)\n'))

    def test_csak_gerinc_es_eloszures(self):
        self.assertTrue(U.uzenet(['naplok/GERINC_TERKEP.tsv']).startswith('GERINC_TERKEP frissítés (gép)\n'))
        u = U.uzenet(['FELADATOK.md', 'naplok/GERINC_TERKEP.md', 'naplok/ELOSZURES_X.tsv'])
        self.assertTrue(u.startswith('FELADATOK.md frissítés (gép)\n'))
        self.assertIn('GERINC_TERKEP frissítve', u)
        self.assertIn('ELOSZURES frissítve', u)


if __name__ == '__main__':
    unittest.main()
