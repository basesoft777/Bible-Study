#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_torzscikk_migralt.py -- N-F11e (FELADATOK #11): a `torzscikk_general.py`
(és így a `general.py --cel torzscikk`) a migrált motívumot -- F217 óta a forrás
(`motivumok/<ID>.md`) megléte és a törzscikk hiánya szerint --
kihagyja, hogy egy teljes `--ir` (pl. a #36) ne hozza vissza a megszűnt
kimenetet (D6, F11 M5). A nem migrált motívum törzscikke változatlanul készül.

A kitalált motívumfájlok és a próba-kimenet ideiglenes, repón kívüli könyvtárban áll
(tempfile); az éles listát a teszt csak olvassa.
Futtatás: python eszkozok/teszt_torzscikk_migralt.py
"""

import io
import os
import shutil
import sys
import tempfile
import types
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ESZKOZOK)
import torzscikk_general as T  # noqa: E402

def _ir(ut, szoveg):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with io.open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)


class MigraltLista(unittest.TestCase):
    def setUp(self):
        self.gy = tempfile.mkdtemp(prefix='nf11e_')

    def tearDown(self):
        shutil.rmtree(self.gy, ignore_errors=True)

    def test_forras_torzscikk_nelkul_migralt(self):
        _ir(os.path.join(self.gy, 'motivumok', 'PROBA-001.md'), '# forrás\n')
        _ir(os.path.join(self.gy, 'motivumok', 'REGI-001.md'), '# forrás\n')
        _ir(os.path.join(self.gy, 'lexikon', 'REGI-001_TORZSCIKK.md'), '# törzscikk\n')
        self.assertEqual(T.migralt_idk(self.gy), {'PROBA-001'})

    def test_hianyzo_motivumok_ures(self):
        self.assertEqual(T.migralt_idk(self.gy), set())

    def test_eles_repo(self):
        # Az éles repó: az ISTENTISZT-001 és a HAMART-001 migrált (törzscikkük archiválva), a KIRALY-001 nem.
        eles = T.migralt_idk()
        self.assertIn('ISTENTISZT-001', eles)
        self.assertIn('HAMART-001', eles)
        self.assertNotIn('KIRALY-001', eles)


class RunKihagyas(unittest.TestCase):
    def setUp(self):
        self.gy = tempfile.mkdtemp(prefix='nf11e_run_')
        self.args = types.SimpleNamespace(ir=False, ellenoriz=False, kimenet=self.gy)
        self.eredeti = (T.migralt_idk, T.LG.modell_epit, T.torzscikk_szoveg)
        self.hivasok = []

        def modell(m, *a, **k):
            self.hivasok.append(m['id'])
            return {}

        T.LG.modell_epit = modell
        T.torzscikk_szoveg = lambda m, lex, model: ('# próba %s\n' % m['id'], {
            'igehely': 1, 'igehely_osz': 1, 'kapcsolat': 0, 'lxx_sor': 0,
            'kereszthivatkozas_talalat': 0})
        for mid in ('PROBA-001', 'MAS-001'):
            _ir(os.path.join(self.gy, 'lexikon', '%s_TUDOMANYOS.md' % mid), '# lap\n')

    def tearDown(self):
        T.migralt_idk, T.LG.modell_epit, T.torzscikk_szoveg = self.eredeti
        shutil.rmtree(self.gy, ignore_errors=True)

    def _futtat(self, migralt):
        T.migralt_idk = lambda root=None: set(migralt)
        motivumok = [{'id': 'PROBA-001'}, {'id': 'MAS-001'}]
        elof = [{'id': 'PROBA-001'}, {'id': 'MAS-001'}]
        return T.run(self.args, motivumok, elof, {}, set())

    def test_migralt_kimarad(self):
        self.assertEqual(self._futtat({'PROBA-001'}), 0)
        self.assertFalse(os.path.exists(os.path.join(self.gy, 'lexikon', 'PROBA-001_TORZSCIKK.md')))
        self.assertTrue(os.path.exists(os.path.join(self.gy, 'lexikon', 'MAS-001_TORZSCIKK.md')))
        self.assertEqual(self.hivasok, ['MAS-001'])

    def test_nem_migralt_keszul(self):
        # Negatív eset: üres listával mindkét törzscikk elkészül (a szűrő nem szűr túl).
        self.assertEqual(self._futtat(set()), 0)
        for mid in ('PROBA-001', 'MAS-001'):
            self.assertTrue(os.path.exists(os.path.join(self.gy, 'lexikon', '%s_TORZSCIKK.md' % mid)))
        self.assertEqual(self.hivasok, ['PROBA-001', 'MAS-001'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
