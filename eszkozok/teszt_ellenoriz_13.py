#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_13.py -- F28_EMELES_BRIEF.md, DT24 (b): az
eszkozok/ellenoriz.py 13. szabalyanak (forditasi gyorsitotar, forras_hash)
tesztjei a `teljes` szintu Thayer/BDB sorok konkordancia-forrasaval.

Ideiglenes (a repon kivuli) adat/ + konkordancia/ konyvtarban fut; a
negativ esetekben a szabalynak SÉRTÉS-t kell adnia.

    python eszkozok/teszt_ellenoriz_13.py
"""

import hashlib
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ellenoriz as E  # noqa: E402

FEJ = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash',
       'forditas_hu', 'allapot', 'modell', 'datum', 'terminologia_verzio', 'megjegyzes']
FORRAS = 'H6093. itstsabon עִצָּבוֺן noun [masculine] pain, toil'
LEX_FORRAS = 'priest-king: e.g. Melchizedek'


def sha1(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


class Szabaly13Teljes(unittest.TestCase):
    def setUp(self):
        self.gyoker = tempfile.mkdtemp()
        self.adat = os.path.join(self.gyoker, 'adat')
        konk = os.path.join(self.gyoker, 'konkordancia')
        os.makedirs(self.adat)
        os.makedirs(konk)
        with open(os.path.join(konk, 'BDB_teljes_unabridged.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('Strong_padded\tStrong_eredeti\tTeljes_szocikk\n')
            fh.write('H6093\tH6093\t%s\n' % FORRAS)
        with open(os.path.join(self.adat, 'lexikon_hivatkozasok.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('strong\tszotar\tentry_id\tjelentes_szam\tszoveg_en\tforrasfajl\n')
            fh.write('H3548\tBDB\tH3548\t1\t%s\tkonkordancia/BDB_teljes_unabridged.tsv\n' % LEX_FORRAS)

    def tearDown(self):
        shutil.rmtree(self.gyoker)

    def _futtat(self, sorok):
        with open(os.path.join(self.adat, 'forditasok.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\t'.join(FEJ) + '\n')
            for s in sorok:
                fh.write('\t'.join(s.get(m, '') for m in FEJ) + '\n')
        return E.szabaly13_forditasi_gyorsitotar(self.adat)

    def _sor(self, **kw):
        alap = {'szotar': 'BDB', 'strong': 'H6093', 'entry_id': 'H6093', 'jelentes_szam': 'teljes',
                'mezo': 'forditas_hu', 'forras_hash': sha1(FORRAS), 'forditas_hu': 'fordítás',
                'allapot': 'kezi', 'datum': '2026.10.01'}
        alap.update(kw)
        return alap

    def test_teljes_helyes_hash_rendben(self):
        self.assertEqual(self._futtat([self._sor()]).verdict, 'RENDBEN')

    def test_opus_allapot_rendben(self):
        self.assertEqual(self._futtat([self._sor(allapot='opus', modell='claude-opus-5-5')]).verdict, 'RENDBEN')

    def test_sonnet_allapot_rendben(self):
        # F38.265 (DT-F38e): SEMA 2.14 uj `sonnet` ertek
        self.assertEqual(self._futtat([self._sor(allapot='sonnet', modell='claude-sonnet-5-5')]).verdict, 'RENDBEN')

    def test_negativ_ismeretlen_allapot_bukik(self):
        sor = self._futtat([self._sor(allapot='haiku')])
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertIn('ismeretlen allapot', sor.peldak[0])

    def test_negativ_hibas_hash_bukik(self):
        sor = self._futtat([self._sor(forras_hash='0' * 40)])
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertIn('forras_hash eltér', sor.peldak[0])

    def test_negativ_entry_id_elter_bukik(self):
        sor = self._futtat([self._sor(entry_id='H6094')])
        self.assertEqual(sor.verdict, 'SÉRTÉS')
        self.assertIn('nincs hozzá forrásszöveg', sor.peldak[0])

    def test_negativ_nem_teljes_sor_nem_kap_konkordancia_forrast(self):
        sor = self._futtat([self._sor(jelentes_szam='1')])
        self.assertEqual(sor.verdict, 'SÉRTÉS')

    def test_lexikon_hivatkozas_tovabbra_is_ervenyes(self):
        sor = self._futtat([self._sor(strong='H3548', entry_id='H3548', jelentes_szam='1',
                                      forras_hash=sha1(LEX_FORRAS))])
        self.assertEqual(sor.verdict, 'RENDBEN')

    def test_negativ_duplikalt_kulcs(self):
        self.assertEqual(self._futtat([self._sor(), self._sor()]).verdict, 'SÉRTÉS')


if __name__ == '__main__':
    unittest.main(verbosity=2)
