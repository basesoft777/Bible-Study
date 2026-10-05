#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_szamkiosztas.py -- F30: a szamkiosztas.py es az E26 szabaly tesztjei.
Ideiglenes konyvtarban dolgoznak (az eles repot nem erintik).

Futtatas a repo gyokerebol:
    python eszkozok/ellenorzes/tesztek/test_szamkiosztas.py
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
sys.path.insert(0, os.path.dirname(_ITT))

import szamkiosztas as SK
import kozos as K
import szabalyok as SZ

DONTESEK = (
    '# DONTESEK\n\n'
    '| # | Feladat |\n|---|---|\n'
    '| DT1 | #1 egy |\n'
    '| DT5 | #5 ot |\n'
    '| DT-F40b | #40 masodik |\n'
    '| DT-F40a | #40 elso |\n'
)
NYITOTT = (
    '# Nyitott\n\n'
    '- **N7 -- regi tetel.**\n'
    '- **N-F40a -- uj tetel** (l. DT-F40a)\n'
)
FELADATOK = (
    '# Feladatok\n\n## Dontesnaplo\n\n'
    '| # | Dontes |\n|---|---|\n'
    '| D3 | regi |\n'
    '| D-F40 | uj |\n'
)
NAPLO = 'A DT-F40a es a DT-F40b dontes, N-F40a nyitott, D-F40 napló. DT-F99 arva. DT-F40ab nem helyorzo.\n'


class _Gyoker(object):
    def __enter__(self):
        self.ut = tempfile.mkdtemp(prefix='szamkiosztas_teszt_')
        for nev, tartalom in (('DONTESEK.md', DONTESEK), ('NYITOTT_FELADATOK.md', NYITOTT),
                              ('FELADATOK.md', FELADATOK), ('naplo.md', NAPLO)):
            with open(os.path.join(self.ut, nev), 'wb') as f:
                f.write(tartalom.encode('utf-8'))
        return self.ut

    def __exit__(self, *a):
        shutil.rmtree(self.ut, ignore_errors=True)


def _olvas(gy, nev):
    with open(os.path.join(gy, nev), 'rb') as f:
        return f.read().decode('utf-8')


class SzamkiosztasTeszt(unittest.TestCase):
    def test_terv_sorrend_es_szam(self):
        with _Gyoker() as gy:
            h, figy, arvak = SK.terv(gy)
            self.assertEqual(list(h.items()), [
                ('DT-F40b', 'DT6'), ('DT-F40a', 'DT7'),
                ('N-F40a', 'N8'), ('D-F40', 'D4')])
            self.assertEqual(arvak, ['DT-F99'])

    def test_ir_cserel_es_idempotens(self):
        with _Gyoker() as gy:
            h, _, _ = SK.terv(gy)
            SK.alkalmaz(gy, h, ir=True)
            self.assertIn('| DT6 | #40 masodik |', _olvas(gy, 'DONTESEK.md'))
            self.assertIn('A DT7 es a DT6 dont', _olvas(gy, 'naplo.md'))
            self.assertIn('DT-F99 arva', _olvas(gy, 'naplo.md'))
            self.assertIn('DT-F40ab nem helyorzo', _olvas(gy, 'naplo.md'))
            self.assertIn('napló', _olvas(gy, 'naplo.md'))
            h2, _, _ = SK.terv(gy)
            self.assertEqual(h2, {})
            self.assertEqual(SK.alkalmaz(gy, h2, ir=True), {})

    def test_proba_nem_ir(self):
        with _Gyoker() as gy:
            h, _, _ = SK.terv(gy)
            SK.alkalmaz(gy, h, ir=False)
            self.assertEqual(_olvas(gy, 'DONTESEK.md'), DONTESEK)

    def test_kihagy_jeloles_es_oroklott(self):
        with _Gyoker() as gy:
            with open(os.path.join(gy, 'pelda.md'), 'wb') as f:
                f.write('pelda DT-F40a <!-- szamkiosztas-kihagy -->\n'.encode('utf-8'))
            os.makedirs(os.path.join(gy, 'eszkozok'))
            with open(os.path.join(gy, SK.OROKLOTT_FAJL), 'wb') as f:
                f.write(b'# megj\nDT-F40b\n')
            h, _, arvak = SK.terv(gy)
            self.assertNotIn('DT-F40b', h)
            self.assertEqual(h['DT-F40a'], 'DT6')
            self.assertNotIn('DT-F40b', arvak)
            SK.alkalmaz(gy, h, ir=True)
            self.assertIn('pelda DT-F40a', _olvas(gy, 'pelda.md'))
            self.assertIn('DT-F40b', _olvas(gy, 'DONTESEK.md'))

    def test_crlf_megmarad(self):
        with _Gyoker() as gy:
            with open(os.path.join(gy, 'crlf.md'), 'wb') as f:
                f.write(b'DT-F40a\r\nmasodik DT-F40b\r\n')
            h, _, _ = SK.terv(gy)
            SK.alkalmaz(gy, h, ir=True)
            with open(os.path.join(gy, 'crlf.md'), 'rb') as f:
                self.assertEqual(f.read(), b'DT7\r\nmasodik DT6\r\n')


def _git(gy, *args):
    subprocess.check_call(('git', '-c', 'user.email=t@t', '-c', 'user.name=t') + args, cwd=gy,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class E26Teszt(unittest.TestCase):
    def _repo(self):
        gy = tempfile.mkdtemp(prefix='e26_teszt_')
        self.addCleanup(shutil.rmtree, gy, True)
        _git(gy, 'init', '-q')
        for nev, tartalom in (('DONTESEK.md', DONTESEK), ('NYITOTT_FELADATOK.md', NYITOTT),
                              ('FELADATOK.md', FELADATOK)):
            with open(os.path.join(gy, nev), 'wb') as f:
                f.write(tartalom.encode('utf-8'))
        _git(gy, 'add', '-A')
        _git(gy, 'commit', '-q', '-m', 'alap')
        return gy

    def _futtat(self, gy, modosit, uzenet='', esemeny='pull_request'):
        regi = K.ROOT, SZ.ROOT
        K.ROOT = SZ.ROOT = gy
        try:
            for nev, szoveg in modosit.items():
                with open(os.path.join(gy, nev), 'ab') as f:
                    f.write(szoveg.encode('utf-8'))
            _git(gy, 'add', '-A')
            _git(gy, 'commit', '-q', '-m', 'agon')
            return SZ.e26_vegleges_szam_agon('HEAD~1', 'HEAD', uzenet, esemeny)
        finally:
            K.ROOT, SZ.ROOT = regi

    def test_helyorzo_rendben(self):
        gy = self._repo()
        t = self._futtat(gy, {'DONTESEK.md': '| DT-F50a | #50 |\n', 'naplo.md': 'l. DT-F50a, DT5, N7\n'})
        self.assertEqual(t, [])

    def test_vegleges_sor_hiba(self):
        gy = self._repo()
        t = self._futtat(gy, {'DONTESEK.md': '| DT6 | #50 |\n'})
        self.assertTrue(t)
        self.assertTrue(all(x.szint == 'HIBA' for x in t))
        self.assertIn('helyőrző kell (DT-F<nn>)', t[0].reszlet)

    def test_uj_hivatkozott_szam_hiba(self):
        gy = self._repo()
        t = self._futtat(gy, {'naplo.md': 'l. DT9 es N20\n'})
        self.assertEqual(len(t), 2)

    def test_ketszer_definialt_helyorzo(self):
        gy = self._repo()
        t = self._futtat(gy, {'DONTESEK.md': '| DT-F50a | egy |\n| DT-F50a | ketto |\n'})
        self.assertTrue(any('kétszer' in x.reszlet for x in t))

    def test_szandekos_jeloles_es_push(self):
        gy = self._repo()
        t = self._futtat(gy, {'DONTESEK.md': '| DT6 | #50 |\n'}, uzenet='x\n\nSZÁMKIOSZTÁS-SZÁNDÉKOS: atszamozas\n')
        self.assertEqual(t, [])
        gy = self._repo()
        t = self._futtat(gy, {'DONTESEK.md': '| DT6 | #50 |\n'}, esemeny='push')
        self.assertEqual(t, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
