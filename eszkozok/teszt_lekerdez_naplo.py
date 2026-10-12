#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_lekerdez_naplo.py -- F61 (DT-F61a): a lekerdez.py --naplo /
--lepes onnaplozasa. Ideiglenes masolatokon dolgozik, az eles tablakat nem irja.

  - motivum-ID -> auditok.tsv-masolat; F<szam> -> naplok/<KOD>_lekerdezesek.tsv;
    minden mas -> exit 1, semmi nem irodik;
  - hozzafuzes, duplikacio-szures, a meglevo sorok valtozatlanok;
  - ervenytelen / hianyzo --lepes: hiba, nem ir;
  - a naplosor proveniencia-mezeje szo szerint a kiirt proveniencia-sor, csatorna=cli kulccsal;
  - kapcsolo nelkul a kimenet azonos a --naplo-s kimenet naplo-nelkuli reszevel
    (a proveniencia-sor csatorna-vegenek kivetelevel; a "# napló:" sor stderr-re megy);
  - az ellenoriz.py a csatorna kulcsot megengedi.

    python eszkozok/teszt_lekerdez_naplo.py
"""

import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ITT)
sys.path.insert(0, ITT)

import lekerdez as L  # noqa: E402
import ellenoriz as E  # noqa: E402

LEKERDEZ = os.path.join(ITT, 'lekerdez.py')
ARGS = ('tsk', 'Jób 3:3')


def kimenet(*args):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    return subprocess.run([sys.executable, LEKERDEZ, *args], capture_output=True, env=env)


UTOLSO_STDERR = ''


def futtat_beleirva(extra, auditok, naplok, parancs=ARGS):
    """In-process futtatas ideiglenes celfajlokkal; (stdout, kilepesi kod)."""
    args = L.build_parser().parse_args(list(extra) + list(parancs))
    global UTOLSO_STDERR
    puf = io.StringIO()
    hibapuf = io.StringIO()
    kod = 0
    with contextlib.redirect_stdout(puf), contextlib.redirect_stderr(hibapuf):
        try:
            L.futtat_naplozva(args, auditok=auditok, naplok_mappa=naplok)
        except SystemExit as e:
            kod = e.code or 0
    UTOLSO_STDERR = hibapuf.getvalue()
    return puf.getvalue(), kod


class Naplozas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.auditok = os.path.join(self.tmp, 'auditok.tsv')
        shutil.copy(os.path.join(ROOT, 'adat', 'auditok.tsv'), self.auditok)
        self.naplok = os.path.join(self.tmp, 'naplok')
        os.makedirs(self.naplok)
        with open(self.auditok, 'rb') as f:
            self.eredeti = f.read()
        with open(os.path.join(ROOT, 'adat', 'motivumok.tsv'), encoding='utf-8') as f:
            self.motivum = [s.split('\t')[0] for s in f.read().split('\n')
                            if s and not s.startswith('#')][1]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _sorok(self, ut):
        with open(ut, encoding='utf-8', newline='') as f:
            return f.read().split('\n')[:-1]

    def test_motivum_auditokba_hozzafuz_es_dedup(self):
        ki, kod = futtat_beleirva(['--naplo', self.motivum, '--lepes', 'A5'],
                                  self.auditok, self.naplok)
        self.assertEqual(kod, 0, ki)
        with open(self.auditok, 'rb') as f:
            uj = f.read()
        self.assertTrue(uj.startswith(self.eredeti), 'meglevo sor nem valtozhat')
        uj_sorok = uj[len(self.eredeti):].decode('utf-8').split('\n')[:-1]
        self.assertEqual(len(uj_sorok), 1)
        id_, lepes, prov, datum = uj_sorok[0].split('\t')
        self.assertEqual((id_, lepes), (self.motivum, 'A5'))
        self.assertTrue(prov.endswith(' | csatorna=cli'))
        self.assertIn('proveniencia: ' + prov, ki, 'szo szerint a kiirt sor')
        self.assertRegex(datum, r'^\d{4}\.\d{2}\.\d{2}$')
        self.assertTrue(E.proveniencia_ervenyes(prov), 'csatorna megengedett kulcs')
        ki2, _ = futtat_beleirva(['--naplo', self.motivum, '--lepes', 'A5'],
                                 self.auditok, self.naplok)
        with open(self.auditok, 'rb') as f:
            self.assertEqual(f.read(), uj)
        self.assertIn('már megvolt', UTOLSO_STDERR)
        self.assertTrue(ki2.splitlines()[-1].startswith('proveniencia:'), ki2)

    def test_feladatkod_sajat_fajlba(self):
        ki, kod = futtat_beleirva(['--naplo', 'F61', '--lepes', 'adhoc'],
                                  self.auditok, self.naplok)
        self.assertEqual(kod, 0, ki)
        sorok = self._sorok(os.path.join(self.naplok, 'F61_lekerdezesek.tsv'))
        self.assertEqual(sorok[1], 'id\tlepes\tproveniencia\tdatum')
        self.assertEqual(len(sorok), 3)
        self.assertEqual(sorok[2].split('\t')[:2], ['F61', 'adhoc'])
        with open(self.auditok, 'rb') as f:
            self.assertEqual(f.read(), self.eredeti, 'az auditok.tsv érintetlen')

    def test_ismeretlen_id_hiba(self):
        for rossz in ('NINCSILYEN-999', 'PILOT-X', 'f61', 'F61a'):
            ki, kod = futtat_beleirva(['--naplo', rossz, '--lepes', 'B2'],
                                      self.auditok, self.naplok)
            self.assertEqual(kod, 1, rossz)
        self.assertEqual(os.listdir(self.naplok), [])
        with open(self.auditok, 'rb') as f:
            self.assertEqual(f.read(), self.eredeti)

    def test_ervenytelen_lepes(self):
        ki, kod = futtat_beleirva(['--naplo', 'F61'], self.auditok, self.naplok)
        self.assertEqual(kod, 1)
        self.assertEqual(os.listdir(self.naplok), [])
        p = kimenet('--naplo', 'F61', '--lepes', 'B9', *ARGS)
        self.assertNotEqual(p.returncode, 0)
        p = kimenet('--lepes', 'B2', *ARGS)
        self.assertEqual(p.returncode, 1)

    def test_hibas_lekerdezes_nem_naploz(self):
        ki, kod = futtat_beleirva(['--naplo', 'F61', '--lepes', 'B2'], self.auditok,
                                  self.naplok, parancs=('karoli', 'Nincsilyen 99:99'))
        self.assertNotEqual(kod, 0)
        self.assertEqual(os.listdir(self.naplok), [])

    def test_hibas_utolso_sor_megallit(self):
        with open(self.auditok, 'ab') as f:
            f.write(b'csonka\tsor\n')
        ki, kod = futtat_beleirva(['--naplo', self.motivum, '--lepes', 'B2'],
                                  self.auditok, self.naplok)
        self.assertEqual(kod, 1)

    def test_kapcsolo_nelkul_azonos_kimenet(self):
        alap = kimenet(*ARGS).stdout.decode('utf-8').replace('\r\n', '\n')
        alap = re.sub(r'ts=[^ \n]*', 'ts=X', alap)
        ki, kod = futtat_beleirva(['--naplo', 'F61', '--lepes', 'adhoc'], self.auditok, self.naplok)
        ki = re.sub(r'ts=[^ \n]*', 'ts=X', ki).replace(' | csatorna=cli', '')
        self.assertNotIn('# napló:', ki)
        self.assertIn('# napló:', UTOLSO_STDERR)
        self.assertEqual(ki.replace('\r\n', '\n'), alap)
        self.assertNotIn('csatorna', alap)

    def test_domen_sys_exit0_is_naploz(self):
        ki, kod = futtat_beleirva(['--naplo', 'F61', '--lepes', 'B3'], self.auditok,
                                  self.naplok, parancs=('domen', 'H8414'))
        self.assertEqual(kod, 0, ki)
        self.assertEqual(len(self._sorok(os.path.join(self.naplok, 'F61_lekerdezesek.tsv'))), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
