#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_lekerdez_sir.py -- F28 DT25 (d): a lekerdez.py a Jeremiás
siralmai „Sir” és „JSir” alakját CSAK a scope-olvasásban kezeli; az
adatbeolvasás (parse_igehely, load_*) változatlan.

Követelmény (ELLENOR_F28 1. tétel):
  - a rögzített parancsok (adat/auditok.tsv 169-171: `lxx-hid`, `tsk`,
    `karoli` a `Sir 2:8`-ra; `gerinc "Sir 2"`, `scan --szakasz "Sir 2"`)
    a rögzített / az F28 előtti (e39f145) n-nel futnak újra;
  - a „JSir” alak ugyanezeken az utakon ugyanazt az n-t adja.

A várt n-ek: auditok.tsv 169 (lxx-hid n=24), 170 (tsk n=15), 171 (karoli
n=1); a gerinc és a scan értékét az F28 előtti kód (e39f145) adta ugyanerre a
parancsra (n=38, n=10) — l. naplok/EMELES_naplo.md, DT25 (d).

    python eszkozok/teszt_lekerdez_sir.py
"""

import os
import re
import subprocess
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)

import lekerdez as L  # noqa: E402

LEKERDEZ = os.path.join(ITT, 'lekerdez.py')


def futtat_n(*args):
    """A lekerdez.py futtatása; a proveniencia-sor scope-ja és n-je."""
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, LEKERDEZ, *args], capture_output=True,
                       text=True, encoding='utf-8', env=env)
    m = re.search(r'proveniencia: scope=([^|]*)\|.*\| n=(\d+) \|', p.stdout)
    if not m:
        raise AssertionError(f'nincs proveniencia-sor: {args}\n{p.stdout}\n{p.stderr}')
    return m.group(1).strip(), int(m.group(2))


class ScopeUtak(unittest.TestCase):
    """Minden érintett parancs, mindkét alakkal, a rögzített n-nel."""

    def _mindket_alak(self, sir_args, jsir_args, n_vart, scope_sir):
        scope, n = futtat_n(*sir_args)
        self.assertEqual(n, n_vart, sir_args)
        self.assertEqual(scope, scope_sir, 'a proveniencia a parancssori alakot rögzíti')
        _, n2 = futtat_n(*jsir_args)
        self.assertEqual(n2, n_vart, jsir_args)

    def test_lxx_hid(self):  # auditok.tsv:169
        self._mindket_alak(('lxx-hid', 'Sir 2:8'), ('lxx-hid', 'JSir 2:8'), 24, 'range:Sir 2:8')

    def test_tsk(self):  # auditok.tsv:170
        self._mindket_alak(('tsk', 'Sir 2:8'), ('tsk', 'JSir 2:8'), 15, 'range:Sir 2:8')

    def test_karoli(self):  # auditok.tsv:171
        self._mindket_alak(('karoli', 'Sir 2:8'), ('karoli', 'JSir 2:8'), 1, 'range:Sir 2:8')

    def test_gerinc(self):  # e39f145: n=38
        self._mindket_alak(('gerinc', 'Sir 2', 'Ézs 34'), ('gerinc', 'JSir 2', 'Ézs 34'), 38,
                           'range:Sir 2+Ézs 34')

    def test_scan_szakasz(self):  # e39f145: n=10
        self._mindket_alak(('scan', 'H1323', '--szakasz', 'Sir 2'),
                           ('scan', 'H1323', '--szakasz', 'JSir 2'), 10, 'range:Sir 2')


class ScopeSegedek(unittest.TestCase):
    def test_scope_adat_igehely(self):
        self.assertEqual(L.scope_adat_igehely('JSir 2:8'), 'Sir 2:8')
        self.assertEqual(L.scope_adat_igehely('Sir 2:8'), 'Sir 2:8')
        self.assertEqual(L.scope_adat_igehely('1Móz 3:16'), '1Móz 3:16')

    def test_scope_range(self):
        self.assertEqual(L.scope_range('JSir 2')[1], 'Sir')
        self.assertEqual(L.scope_range('Sir 2')[1], 'Sir')

    def test_scope_to_step(self):
        self.assertEqual(L.scope_to_step('Sir 2:8'), 'Lam.2.8')
        self.assertEqual(L.scope_to_step('JSir 2:8'), 'Lam.2.8')
        self.assertEqual(L.scope_to_step('1Móz 3:16'), 'Gen.3.16')


class AdatbeolvasasValtozatlan(unittest.TestCase):
    """A közös parse_igehely nem kap álnevet (DT25 d)."""

    def test_parse_igehely_nem_alnevesit(self):
        self.assertEqual(L.parse_igehely('Sir 2:8'), ('Sir', 2, 8))
        self.assertEqual(L.parse_igehely('JSir 2:8'), ('JSir', 2, 8))
        self.assertEqual(L.parse_igehely('1Móz 3:16'), ('1Móz', 3, 16))

    def test_nincs_regi_alnev(self):
        self.assertFalse(hasattr(L, 'REGI_ALNEV'))

    def test_tahot_sir_kulcs(self):
        sorok = [r for r in L.load_tahot() if r['_parsed'][:2] == ('Sir', 2)]
        self.assertTrue(sorok, 'a TAHOT Siralmak 2. fejezete a saját „Sir” kulcsán olvasandó')


if __name__ == '__main__':
    unittest.main(verbosity=2)
