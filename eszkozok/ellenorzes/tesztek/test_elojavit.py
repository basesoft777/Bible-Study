#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_elojavit.py -- F188 T3: az `elojavit.py` tesztjei (E32, E8, E5), ideiglenes
gyökérrel (a `kozos`/`szabalyok` ROOT-ja a teszt idejére átáll, mint a
`test_szabalyok.py` `_IdeiglenesGyoker`-ében), az E5-höz ideiglenes git-repóval.

Futtatás a repó gyökeréből:
    python eszkozok/ellenorzes/tesztek/test_elojavit.py
"""

import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_ITT))

import kozos as K  # noqa: E402
import szabalyok as SZ  # noqa: E402
import elojavit as EJ  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


class _Gyoker(object):
    def __enter__(self):
        self.tmp = tempfile.mkdtemp(prefix='elojavit_teszt_')
        os.makedirs(os.path.join(self.tmp, 'adat'))
        self._regi = (K.ROOT, K.ADAT, SZ.ROOT, SZ.ADAT)
        K.ROOT = SZ.ROOT = self.tmp
        K.ADAT = SZ.ADAT = os.path.join(self.tmp, 'adat')
        return self.tmp

    def __exit__(self, *exc):
        K.ROOT, K.ADAT, SZ.ROOT, SZ.ADAT = self._regi
        shutil.rmtree(self.tmp, ignore_errors=True)
        return False


def _ir(gyoker, relut, tartalom):
    ut = os.path.join(gyoker, *relut.split('/'))
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write(tartalom)


def _olvas(gyoker, relut):
    with open(os.path.join(gyoker, *relut.split('/')), encoding='utf-8', newline='') as f:
        return f.read()


def _csendben(fv, *a, **kw):
    with redirect_stdout(io.StringIO()):
        return fv(*a, **kw)


class E32SorTeszt(unittest.TestCase):
    def test_egyedul_zarojelben(self):
        self.assertEqual(EJ.e32_sor_javitas("    x = 'a kapcsolódó blokk (DT-F127b)'", 'DT-F127b'),
                         "    x = 'a kapcsolódó blokk'")

    def test_lista_eleje_es_vege(self):
        self.assertEqual(EJ.e32_sor_javitas("s = '(DT-F12a, N-F3b) szöveg'", 'DT-F12a'), "s = '(N-F3b) szöveg'")
        self.assertEqual(EJ.e32_sor_javitas("s = '(DT5; DT-F12a) szöveg'", 'DT-F12a'), "s = '(DT5) szöveg'")

    def test_mondat_resze_nem_javit(self):
        self.assertIsNone(EJ.e32_sor_javitas("s = 'a DT-F12a szerint'", 'DT-F12a'))

    def test_ketszer_nem_javit(self):
        self.assertIsNone(EJ.e32_sor_javitas("s = '(DT-F12a)'  # DT-F12a", 'DT-F12a'))

    def test_hosszabb_helyorzo_nem_egyezik(self):
        self.assertIsNone(EJ.e32_sor_javitas("s = '(DT-F12ab)'", 'DT-F12a'))


class E32FajlTeszt(unittest.TestCase):
    def test_javit_es_jelez(self):
        with _Gyoker() as g:
            _ir(g, 'eszkozok/gen.py', "A = 'blokk (DT-F9a)'\r\nB = 'a DT-F9b szerint'\r\n")
            regi = SZ.e32_kiosztott_helyorzo_literalban

            def al(fajlok):
                return [K.Talalat('E32', 'HIBA', 'eszkozok/gen.py', 1, '`DT-F9a` kiosztott helyőrző …'),
                        K.Talalat('E32', 'HIBA', 'eszkozok/gen.py', 2, '`DT-F9b` kiosztott helyőrző …')]
            SZ.e32_kiosztott_helyorzo_literalban = al
            try:
                szaraz = _csendben(EJ.e32_javitasok, ['eszkozok/gen.py'], False)
                self.assertIn("(DT-F9a)", _olvas(g, 'eszkozok/gen.py'))
                leletek = _csendben(EJ.e32_javitasok, ['eszkozok/gen.py'], True)
            finally:
                SZ.e32_kiosztott_helyorzo_literalban = regi
            self.assertEqual([le.javitott for le in szaraz], [True, False])
            self.assertEqual([le.javitott for le in leletek], [True, False])
            self.assertEqual(_olvas(g, 'eszkozok/gen.py'), "A = 'blokk'\r\nB = 'a DT-F9b szerint'\r\n")


class E8SorTeszt(unittest.TestCase):
    def test_stepbible_tanulmanyban(self):
        uj, jel = EJ.e8_sor_javitas('A Gen.12.7 versben áll.', True)
        self.assertEqual(uj, 'A `Gen.12.7` versben áll.')
        self.assertEqual(jel, [])

    def test_stepbible_mas_fajlban_nem_tiltott(self):
        self.assertEqual(EJ.e8_sor_javitas('A Gen.12.7 kulcs.', False), ('A Gen.12.7 kulcs.', []))

    def test_adatsor_idezet(self):
        uj, jel = EJ.e8_sor_javitas('A `adat/elofordulasok.tsv` sora: „1 Móz 3:16”.', False)
        self.assertEqual(uj, 'A `adat/elofordulasok.tsv` sora: `„1 Móz 3:16”`.')
        self.assertEqual(jel, [])

    def test_proza_csak_jelez(self):
        uj, jel = EJ.e8_sor_javitas('Lásd 1 Móz 3:16 és 1. Kor 13:4.', False)
        self.assertEqual(uj, 'Lásd 1 Móz 3:16 és 1. Kor 13:4.')
        self.assertEqual(len(jel), 2)
        self.assertIn('javasolt: "1Móz"', jel[0])
        self.assertIn('javasolt: "1Kor"', jel[1])

    def test_kodban_nem_talalat(self):
        self.assertEqual(EJ.e8_sor_javitas('Példa: `1 Móz`.', False), ('Példa: `1 Móz`.', []))


class E8FajlTeszt(unittest.TestCase):
    def test_tanulmany_javitas_utan_tiszta(self):
        with _Gyoker() as g:
            rel = 'genezis/1Moz_12_tanulmany.md'
            _ir(g, rel, '# T\n\nA Gen.12.7 és a Gen.13.15 egybecseng.\n\n```\nGen.1.1\n```\n')
            leletek = _csendben(EJ.e8_javitasok, [rel], True)
            self.assertTrue(all(le.javitott for le in leletek))
            self.assertIn('A `Gen.12.7` és a `Gen.13.15` egybecseng.', _olvas(g, rel))
            self.assertIn('```\nGen.1.1\n```', _olvas(g, rel))
            self.assertEqual(SZ.e8_igehely_format([rel]), [])

    def test_szaraz_futas_nem_ir(self):
        with _Gyoker() as g:
            rel = 'genezis/1Moz_12_tanulmany.md'
            _ir(g, rel, 'A Gen.12.7 áll.\n')
            _csendben(EJ.e8_javitasok, [rel], False)
            self.assertEqual(_olvas(g, rel), 'A Gen.12.7 áll.\n')


class E5Teszt(unittest.TestCase):
    DIFF = ('diff --git a/MUNKAMENET.md b/MUNKAMENET.md\n--- a/MUNKAMENET.md\n+++ b/MUNKAMENET.md\n'
            '@@ -3 +3 @@\n-## 2. Régi cím\n+## 3. Régi cím\n'
            '@@ -9 +8,0 @@\n-### Törölt alpont\n'
            'diff --git a/beerkezo/x.md b/beerkezo/x.md\n@@ -1 +0,0 @@\n-## Kimarad\n')

    def test_torlesek(self):
        self.assertEqual(EJ.e5_torlesek(self.DIFF, set()), [('MUNKAMENET.md', 'törölt címsor: ### Törölt alpont')])

    def test_study_30_sor(self):
        diff = 'diff --git a/sablonok/s.md b/sablonok/s.md\n@@ -1,31 +0,0 @@\n' + '-x\n' * 31
        self.assertEqual(EJ.e5_torlesek(diff, set()), [('sablonok/s.md', '31 törölt sor (study-/sablonfájl)')])
        self.assertEqual(EJ.e5_torlesek(diff.replace('sablonok/s.md', 'eszkozok/s.py'), set()), [])

    def test_jelolo_a_cli_mintaval_egyezik(self):
        sor = EJ.e5_jelolo_sor([('A.md', 'törölt címsor: ## X')])
        self.assertTrue(SZ.SZANDEKOS_JELOLES_MINTA.search(sor))

    def test_commit_uzenetbe(self):
        uzenet = 'F1.2: cím\n\nTörzs.\n\nCo-Authored-By: Claude <x@y>\n'
        self.assertEqual(EJ.commit_uzenetbe(uzenet, 'TÖRLÉS-SZÁNDÉKOS: A.md'),
                         'F1.2: cím\n\nTörzs.\n\nTÖRLÉS-SZÁNDÉKOS: A.md\n\nCo-Authored-By: Claude <x@y>\n')
        self.assertEqual(EJ.commit_uzenetbe('F1.2: cím\n', 'TÖRLÉS-SZÁNDÉKOS: A.md'),
                         'F1.2: cím\n\nTÖRLÉS-SZÁNDÉKOS: A.md\n')


class T2Teszt(unittest.TestCase):
    def test_csak_hozzaadott_sor(self):
        ts = [K.Talalat('SZAMISMETLES', 'JELENTES', 'NYITOTT_FELADATOK.md', n, 'x') for n in (3, 7)]
        self.assertEqual([t.sor for t in EJ.t2_szures(ts, {7, 8})], [7])
        self.assertEqual([t.sor for t in EJ.t2_szures(ts, None)], [3, 7])

    def test_jelzes_uj_fajlban(self):
        with _Gyoker() as g:
            _git(g, 'init', '-q')
            _ir(g, 'x.txt', 'a\n')
            _git(g, 'add', '.')
            _git(g, 'commit', '-q', '-m', 'alap')
            _ir(g, 'naplok/F9_jelentes.md', '# J\n\nAz `adat/x.tsv` most 312 sor.\n')
            leletek = EJ.t2_jelzesek(['naplok/F9_jelentes.md'], 'HEAD')
            self.assertEqual([(le.szabaly, le.sor, le.javitott) for le in leletek], [('T2', 3, False)])


def _git(gyoker, *args):
    subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=false'] + list(args),
                   cwd=gyoker, check=True, capture_output=True)


class E5RepoTeszt(unittest.TestCase):
    def test_jelzes_es_beiras(self):
        with _Gyoker() as g:
            _git(g, 'init', '-q')
            _ir(g, 'DOK.md', '# D\n\n## Marad\n\n## Megy\n\nszöveg\n')
            _git(g, 'add', '.')
            _git(g, 'commit', '-q', '-m', 'alap')
            _ir(g, 'DOK.md', '# D\n\n## Marad\n\nszöveg\n')
            leletek = EJ.e5_ellenoriz('HEAD', None, False, False)
            self.assertEqual(len(leletek), 1)
            self.assertFalse(leletek[0].javitott)
            self.assertIn('## Megy', leletek[0].szoveg)
            uzenet = os.path.join(g, 'uzenet.txt')
            _ir(g, 'uzenet.txt', 'F1.1: cím\n\nCo-Authored-By: Claude <x@y>\n')
            leletek = EJ.e5_ellenoriz('HEAD', uzenet, True, True)
            self.assertTrue(leletek[0].javitott)
            self.assertIn('TÖRLÉS-SZÁNDÉKOS: DOK.md — törölt címsor: ## Megy', _olvas(g, 'uzenet.txt'))
            self.assertEqual(EJ.e5_ellenoriz('HEAD', uzenet, False, False), [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
