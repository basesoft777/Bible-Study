#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_dontes_nezet.py -- PR-onkenti dontes-/nyitott-fajlok (dontesek/uj, nyitott/uj):
a beolvasztas, az egyesitett nezet es a ket egymas utani merge szimulacioja.
Ideiglenes git-repoban dolgoznak (az eles repot nem erintik).

Futtatas a repo gyokerebol:
    python eszkozok/ellenorzes/tesztek/test_dontes_nezet.py
"""

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

_ITT = os.path.dirname(os.path.abspath(__file__))
_ESZKOZOK = os.path.dirname(os.path.dirname(_ITT))
sys.path.insert(0, _ESZKOZOK)

import dontes_nezet as DN
import szamkiosztas as SK

DONTESEK = ('# DONTESEK\r\n\r\n| # | Feladat |\r\n|---|---|\r\n'
            '| DT1 | #1 egy |\r\n| DT5 | #5 ot |\r\n')
NYITOTT = ('# Nyitott\r\n\r\n## Kisebb\r\n\r\n* **N7 -- regi tetel.**\r\n\r\n'
           + DN.NYITOTT_JELOLES + '\r\n\r\n## Lezárva\r\n* **N1 -- lezart.**\r\n')


def _ir(gyoker, rel, szoveg):
    ut = os.path.join(gyoker, *rel.split('/'))
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'wb') as f:
        f.write(szoveg.encode('utf-8'))


def _git(gyoker, *args, ok=True):
    r = subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'core.autocrlf=false']
                       + list(args), cwd=gyoker, capture_output=True)
    if ok and r.returncode != 0:
        raise AssertionError('git %s: %s' % (' '.join(args), r.stderr.decode('utf-8', 'replace')))
    return r


def _olvas(gyoker, rel):
    with open(os.path.join(gyoker, *rel.split('/')), 'rb') as f:
        return f.read().decode('utf-8')


class _Repo(object):
    def __enter__(self):
        self.ut = tempfile.mkdtemp(prefix='dontes_nezet_teszt_')
        _git(self.ut, 'init', '-q', '-b', 'main')
        _ir(self.ut, 'DONTESEK.md', DONTESEK)
        _ir(self.ut, 'NYITOTT_FELADATOK.md', NYITOTT)
        _git(self.ut, 'add', '-A')
        _git(self.ut, 'commit', '-q', '-m', 'alap')
        return self.ut

    def __exit__(self, *a):
        shutil.rmtree(self.ut, ignore_errors=True)


def _kiosztas(gyoker):
    """Az Action lepese: szamkiosztas --ir, majd commit (ha van valtozas)."""
    uz = os.path.join(gyoker, '_uzenet.txt')
    r = subprocess.run([sys.executable, os.path.join(_ESZKOZOK, 'szamkiosztas.py'), '--ir', '--gyoker', gyoker,
                        '--uzenet-fajl', uz], capture_output=True)
    assert r.returncode == 0, r.stderr.decode('utf-8', 'replace')
    if os.path.exists(uz):
        msg = _olvas(gyoker, '_uzenet.txt')
        os.remove(uz)
        _git(gyoker, 'add', '-u')
        _git(gyoker, 'commit', '-q', '-m', msg)
        return msg
    return None


class TestBeolvaszt(unittest.TestCase):
    def test_dontes_sorok_fejlec_nelkul(self):
        uj = '| # | F |\n|---|---|\n| DT-F9a | #9 uj | k |\n\n| DT-F9b | #9 masik |\n'
        self.assertEqual(DN.dontes_sorok(uj), ['| DT-F9a | #9 uj | k |', '| DT-F9b | #9 masik |'])

    def test_beolvaszt_dontesek_crlf_megmarad(self):
        ki = DN.beolvaszt_dontesek(DONTESEK, ['| DT-F9a | x |\n'])
        self.assertTrue(ki.endswith('| DT5 | #5 ot |\r\n| DT-F9a | x |\r\n'))
        self.assertNotIn('\n', ki.replace('\r\n', ''))

    def test_beolvaszt_nyitott_jelolesnel(self):
        ki = DN.beolvaszt_nyitott(NYITOTT, ['* **N-F9a -- uj.**\n  folytatas\n'])
        self.assertIn('N-F9a', ki)
        self.assertLess(ki.index('N7'), ki.index('N-F9a'))
        self.assertLess(ki.index('N-F9a'), ki.index(DN.NYITOTT_JELOLES))
        self.assertLess(ki.index(DN.NYITOTT_JELOLES), ki.index('## Lezárva'))

    def test_beolvaszt_nyitott_jeloles_nelkul_lezarva_elott(self):
        ki = DN.beolvaszt_nyitott(NYITOTT.replace(DN.NYITOTT_JELOLES, ''), ['* **N-F9a -- uj.**'])
        self.assertLess(ki.index('N-F9a'), ki.index('## Lezárva'))

    def test_nincs_uj_fajl_nincs_valtozas(self):
        self.assertEqual(DN.beolvaszt_dontesek(DONTESEK, []), DONTESEK)
        self.assertEqual(DN.beolvaszt_nyitott(NYITOTT, []), NYITOTT)

    def test_nyitott_frissites_es_lezart_blokk(self):
        fo = ('# N\r\nUtolsó frissítés: 2026.11.02 (regi)\r\n\r\n* **N7 x**\r\n\r\n' + DN.NYITOTT_JELOLES
              + '\r\n\r\n## Lezárva\r\n### 2026.11.01 (r):\r\n* N1\r\n')
        a = 'Utolsó frissítés: 2026.11.03 (A)\n* **N-F1a -- t**\n### 2026.11.03 (A):\n* N7 lezarva\n'
        b = 'Utolsó frissítés: 2026.11.04 (B)\n* **N-F2a -- u**\n'
        ki = DN.beolvaszt_nyitott(fo, [a, b])
        self.assertIn('Utolsó frissítés: 2026.11.04 (B); előtte 2026.11.03 (A); előtte 2026.11.02 (regi)\r\n', ki)
        self.assertLess(ki.index('N-F1a'), ki.index('N-F2a'))
        self.assertLess(ki.index('N-F2a'), ki.index(DN.NYITOTT_JELOLES))
        self.assertLess(ki.index('## Lezárva'), ki.index('### 2026.11.03 (A)'))
        self.assertLess(ki.index('### 2026.11.03 (A)'), ki.index('### 2026.11.01 (r)'))
        self.assertNotIn('Utolsó frissítés: 2026.11.03 (A)\r\n* **N-F1a', ki)   # a sor nem kerul a tetelek koze
        self.assertTrue(ki.count('\r\n') == ki.count('\n'))


class TestEgyesitettNezet(unittest.TestCase):
    def test_nezet_latja_az_uj_fajlt(self):
        with _Repo() as r:
            _ir(r, 'dontesek/uj/a.md', '| DT-F9a | #9 |\n')
            _ir(r, 'nyitott/uj/a.md', '* **N-F9a -- t.**\n')
            self.assertIn('DT-F9a', DN.dontesek_szoveg(r))
            self.assertIn('N-F9a', DN.nyitott_szoveg(r))
            self.assertNotIn('DT-F9a', _olvas(r, 'DONTESEK.md'))


class TestKetEgymasUtaniMerge(unittest.TestCase):
    """A fo cel: ket PR, mindketto uj dontes- es nyitott-fajllal, utkozes nelkul mergelheto; az Action mindkettot beirja."""

    def test_szimulacio(self):
        with _Repo() as r:
            for ag, dt, n in (('pr-a', 'DT-F10a', 'N-F10a'), ('pr-b', 'DT-F20a', 'N-F20a')):
                _git(r, 'checkout', '-q', '-b', ag, 'main')
                _ir(r, 'dontesek/uj/%s.md' % ag, '| %s | #1 %s | k |\n| %s | #1 masik |\n' % (dt, ag, dt[:-1] + 'b'))
                _ir(r, 'nyitott/uj/%s.md' % ag, '* **%s -- %s tetel.** *(ÚJ)* l. %s\n' % (n, ag, dt))
                _git(r, 'add', '-A')
                _git(r, 'commit', '-q', '-m', ag)
            _git(r, 'checkout', '-q', 'main')

            # 1. merge: A -> main, Action
            _git(r, 'merge', '-q', '--no-ff', '-m', 'merge A', 'pr-a')
            self.assertIn('DT6', _kiosztas(r))
            self.assertFalse(os.path.exists(os.path.join(r, 'dontesek', 'uj', 'pr-a.md')))

            # 2. merge: B -> main, UTKOZES NELKUL (a pr-b a regi alapra epul, a main kozben valtozott)
            res = _git(r, 'merge', '-q', '--no-ff', '-m', 'merge B', 'pr-b', ok=False)
            self.assertEqual(res.returncode, 0, res.stdout.decode() + res.stderr.decode())
            self.assertIn('DT8', _kiosztas(r))

            d, n = _olvas(r, 'DONTESEK.md'), _olvas(r, 'NYITOTT_FELADATOK.md')
            for sor in ('| DT6 | #1 pr-a', '| DT7 | #1 masik', '| DT8 | #1 pr-b', '| DT9 | #1 masik'):
                self.assertIn(sor, d)
            self.assertNotIn('-F', d)
            self.assertIn('N8 -- pr-a tetel', n)
            self.assertIn('N9 -- pr-b tetel', n)
            self.assertIn('l. DT6', n)          # a hivatkozas is lecserelodott
            self.assertIn('l. DT8', n)
            self.assertLess(n.index('N9 --'), n.index('## Lezárva'))
            self.assertTrue(d.endswith('\r\n') and '\n' not in d.replace('\r\n', ''))
            # idempotens: ujrafuttatva nincs valtozas
            self.assertIsNone(_kiosztas(r))

    def test_proba_nem_ir(self):
        with _Repo() as r:
            _ir(r, 'dontesek/uj/a.md', '| DT-F9a | #9 |\n')
            _git(r, 'add', '-A')
            _git(r, 'commit', '-q', '-m', 'x')
            p = subprocess.run([sys.executable, os.path.join(_ESZKOZOK, 'szamkiosztas.py'), '--proba', '--gyoker', r],
                               capture_output=True)
            ki = p.stdout.decode('utf-8', 'replace')
            self.assertIn('DT-F9a → DT6', ki)
            self.assertTrue(os.path.exists(os.path.join(r, 'dontesek', 'uj', 'a.md')))
            self.assertNotIn('DT-F9a', _olvas(r, 'DONTESEK.md'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
