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


SZ1, SZ2 = 'H1. ab', '1 father Gn 1:1'   # a 2. szakasz a `hivatkozas` javítással (Gen -> Gn); pe/mem nélkül


class Szabaly13Szakasz(Szabaly13Teljes):
    """F128 (DT-F128a (a), DT-F128b (1), DT-F128g (a)): a BDB `sz<sorszam>` sorainak forrásszövege a szakasztábla
    szakasza a hivatkozás-javítással; a nem `elavult` szakaszsorok együtt a Strong összes szakaszát fedik."""

    def setUp(self):
        super().setUp()
        with open(os.path.join(self.adat, 'bdb_szakaszok.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# GENERÁLT: teszt\n# forras: teszt\n')
            fh.write('strong\tbdb_id\tsorszam\tutvonal\tjelolo\tjel\tszoveg\tillesztes\n')
            fh.write('H0001\tBDB17\t1\tcim\tcim\t\tH1. ab\tegyezik\n')
            fh.write('H0001\tBDB17\t2\t-/1/-\tpoint\t1\tfather Gen 1:1\tegyezik\n')
        with open(os.path.join(self.adat, 'bdb_forras_javitas.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# GENERÁLT: teszt\n# forras: teszt\n')
            fh.write('strong\tsorszam\tbdb_id\thiba\tszo_sorszam\telofordulas\tforras_alak\tjavitott_alak\tallapot\n')
            fh.write('H0001\t2\tBDB17\thivatkozas\t\t1\tGen\tGn\tjavitva\n')
            fh.write('H0001\t2\tBDB17\tpe_mem\t1\t1\tfather\tfathxr\tjavitva\n')   # pe/mem: nem alkalmazódik

    def _sz(self, n, szoveg, **kw):
        alap = {'szotar': 'BDB', 'strong': 'H0001', 'entry_id': 'H1', 'jelentes_szam': 'sz%d' % n,
                'mezo': 'forditas_hu', 'forras_hash': sha1(szoveg), 'forditas_hu': 'f%d' % n,
                'allapot': 'sonnet', 'modell': 'claude-sonnet-5-5', 'datum': '2026.10.21'}
        alap.update(kw)
        return alap

    def test_szakaszsorok_rendben(self):
        self.assertEqual(self._futtat([self._sz(1, SZ1), self._sz(2, SZ2)]).verdict, 'RENDBEN')

    def test_szakaszsorok_a_teljes_mellett(self):
        self.assertEqual(self._futtat([self._sor(), self._sz(1, SZ1), self._sz(2, SZ2)]).verdict, 'RENDBEN')

    def test_negativ_nyers_szoveg_hash_bukik(self):
        # a javítás nélküli szöveg hash-e (Gen) nem a bemenet hash-e
        self.assertEqual(self._futtat([self._sz(1, SZ1), self._sz(2, '1 father Gen 1:1')]).verdict, 'SÉRTÉS')

    def test_negativ_hianyos_szakaszsorok(self):
        e = self._futtat([self._sz(1, SZ1)])
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertTrue(any('nem fedik le' in h for h in e.peldak), e.peldak)

    def test_elavult_szakaszsor_nem_szamit_a_lefedesbe(self):
        # az `elavult` 2. szakaszsor mellett az élő sorok nem fedik le a Strongot
        self.assertEqual(self._futtat([self._sz(1, SZ1), self._sz(2, SZ2, allapot='elavult')]).verdict, 'SÉRTÉS')
        self.assertEqual(self._futtat([self._sz(1, SZ1, allapot='elavult'), self._sz(2, SZ2, allapot='elavult')]).verdict,
                         'RENDBEN')

    def test_negativ_tablan_kivuli_strong(self):
        self.assertEqual(self._futtat([self._sz(1, SZ1, strong='H4725', entry_id='H4725')]).verdict, 'SÉRTÉS')

    def test_negativ_entry_id_elter(self):
        self.assertEqual(self._futtat([self._sz(1, SZ1, entry_id='H0001'), self._sz(2, SZ2)]).verdict, 'SÉRTÉS')


TSZ1, TSZ2 = 'G1 — Α, ἄλφα', 'a first letter; cf. Homer'          # G0001: nyers (illesztés: egyezik)
TJ1, TJ2_NYERS, TJ2 = 'G2 — x', 'abc def', 'abc XYZ def'            # G0002: a 2. szakaszba a javítótábla szúr be


class Szabaly13Thayer(Szabaly13Teljes):
    """F145 (DT-F142d): a Thayer `sz<sorszam>` sorainak forrásszövege a `thayer_szakaszok.tsv` szakasza a `thayer_forras_javitas.tsv`
    beszúrásával (ugyanaz a szöveg és hash, amelyet a `forditas.py rogzit` használ); a nem `elavult` sorok a Strong összes szakaszát fedik."""

    def setUp(self):
        super().setUp()
        with open(os.path.join(self.adat, 'thayer_szakaszok.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# GENERÁLT: teszt\n# forras: teszt\n')
            fh.write('strong\tsorszam\tutvonal\tjel\tszoveg\tillesztes\n')
            fh.write('G0001\t1\tcim\t\t%s\tegyezik\n' % TSZ1)
            fh.write('G0001\t2\t-/1/-\t1.\t%s\tegyezik\n' % TSZ2)
            fh.write('G0002\t1\tcim\t\t%s\tjavitassal\n' % TJ1)
            fh.write('G0002\t2\t-/1/-\t\t%s\tjavitassal\n' % TJ2_NYERS)
        self._jav(['G0002\t2\ttsv_szovegvesztes\t10\t3\tabc\t XYZ\t\t4\tjavitva\tteszt'])

    def _jav(self, sorok):
        with open(os.path.join(self.adat, 'thayer_forras_javitas.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# GENERÁLT: teszt\n# forras: teszt\n')
            fh.write('strong\tsorszam\thiba\ttsv_poz\tsor_poz\telotte\tjavitott_alak\tutana\thossz\tallapot\tindok\n')
            for r in sorok:
                fh.write(r + '\n')

    def _t(self, n, szoveg, strong='G0001', entry_id='G1', **kw):
        alap = {'szotar': 'Thayer', 'strong': strong, 'entry_id': entry_id, 'jelentes_szam': 'sz%d' % n,
                'mezo': 'forditas_hu', 'forras_hash': sha1(szoveg), 'forditas_hu': 'f%d' % n,
                'allapot': 'sonnet', 'modell': 'claude-sonnet-5-5', 'datum': '2026.10.26'}
        alap.update(kw)
        return alap

    G1 = ('G0001', 'G1')
    G2 = ('G0002', 'G2')

    def test_thayer_szakaszsorok_rendben(self):
        # a 2. szakasz forrásszövege a jel + szöveg egy szóközzel
        self.assertEqual(self._futtat([self._t(1, TSZ1), self._t(2, '1. ' + TSZ2)]).verdict, 'RENDBEN')

    def test_thayer_javitott_nezet(self):
        # a `javitassal` illesztésű Strong szakaszába a javítótábla beszúr; a hash a javított szövegé
        sorok = [self._t(1, TJ1, *self.G2), self._t(2, TJ2, *self.G2)]
        self.assertEqual(self._futtat(sorok).verdict, 'RENDBEN')

    def test_negativ_thayer_nyers_szoveg_hash_bukik(self):
        sorok = [self._t(1, TJ1, *self.G2), self._t(2, TJ2_NYERS, *self.G2)]
        e = self._futtat(sorok)
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertTrue(any('forras_hash eltér' in h for h in e.peldak), e.peldak)

    def test_negativ_thayer_hibas_hash_bukik(self):
        self.assertEqual(self._futtat([self._t(1, TSZ1), self._t(2, 'más szöveg')]).verdict, 'SÉRTÉS')

    def test_negativ_thayer_hianyos_szakaszsorok(self):
        e = self._futtat([self._t(1, TSZ1)])
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertTrue(any(h.startswith('Thayer G0001: a szakaszsorok nem fedik le') for h in e.peldak), e.peldak)

    def test_thayer_elavult_nem_szamit_a_lefedesbe(self):
        self.assertEqual(self._futtat([self._t(1, TSZ1), self._t(2, '1. ' + TSZ2, allapot='elavult')]).verdict, 'SÉRTÉS')
        self.assertEqual(self._futtat([self._t(1, TSZ1, allapot='elavult'), self._t(2, '1. ' + TSZ2, allapot='elavult')]).verdict,
                         'RENDBEN')

    def test_negativ_thayer_tablan_kivuli_strong(self):
        e = self._futtat([self._t(1, TSZ1, strong='G9999', entry_id='G9999')])
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertTrue(any('nincs hozzá forrásszöveg' in h for h in e.peldak), e.peldak)

    def test_negativ_thayer_entry_id_elter(self):
        self.assertEqual(self._futtat([self._t(1, TSZ1, entry_id='G0001'), self._t(2, '1. ' + TSZ2, entry_id='G0001')]).verdict,
                         'SÉRTÉS')

    def test_negativ_szotar_nem_keveredik(self):
        # a BDB-sor nem kap Thayer-forrást (és fordítva): a G-Strong BDB-ként forrásszöveg nélkül marad
        e = self._futtat([self._t(1, TSZ1, szotar='BDB'), self._t(2, '1. ' + TSZ2, szotar='BDB')])
        self.assertEqual(e.verdict, 'SÉRTÉS')

    def test_negativ_thayer_javitas_nem_illeszkedik(self):
        # a javítótábla `elotte` mezője nem illeszkedik: SÉRTÉS az okkal (nem összeomlás)
        self._jav(['G0002\t2\ttsv_szovegvesztes\t10\t3\tXXX\t XYZ\t\t4\tjavitva\tteszt'])
        e = self._futtat([self._t(1, TJ1, *self.G2), self._t(2, TJ2, *self.G2)])
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertTrue(any('Thayer G0002' in h and 'nem illeszkedik' in h for h in e.peldak), e.peldak)

    def test_thayer_nincs_tabla_nincs_forras(self):
        os.remove(os.path.join(self.adat, 'thayer_szakaszok.tsv'))
        self.assertEqual(self._futtat([self._t(1, TSZ1), self._t(2, '1. ' + TSZ2)]).verdict, 'SÉRTÉS')



DBH_DEF = '= one or more words by which a person is known'
DBH_GL = 'name'


class Szabaly13DBH(Szabaly13Teljes):
    """F121 (DT-F121b): az UBS_DBH sor forrasszovege az UBS_DBH_jelentesek.tsv `definicio_rovid` / `glosszak`
    oszlopa (entry_id = lexid, jelentes_szam = em-dash); strongonkent az elso sor."""

    def setUp(self):
        super().setUp()
        fej = ['strong', 'strong_kod', 'lemma', 'main_id', 'lexid', 'entry_kod', 'domen_kod', 'domen',
               'definicio_rovid', 'definicio_hosszu', 'glosszak', 'megjegyzes']
        sor = ['H8034', 'H8034', 'x', '1', '007442001001000', '-', '1', 'D', DBH_DEF, '-', DBH_GL, '-']
        with open(os.path.join(self.gyoker, 'konkordancia', 'UBS_DBH_jelentesek.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# GENERALT: teszt\n')
            fh.write('\t'.join(fej) + '\n')
            fh.write('\t'.join(sor) + '\n')

    def _d(self, mezo, szoveg, **kw):
        alap = {'szotar': 'UBS_DBH', 'strong': 'H8034', 'entry_id': '007442001001000', 'jelentes_szam': '—',
                'mezo': mezo, 'forras_hash': sha1(szoveg), 'forditas_hu': 'forditás',
                'allapot': 'sonnet', 'modell': 'claude-sonnet-5-5', 'datum': '2026.10.28'}
        alap.update(kw)
        return alap

    def test_definicio_helyes_hash_rendben(self):
        self.assertEqual(self._futtat([self._d('definicio_hu', DBH_DEF)]).verdict, 'RENDBEN')

    def test_glossza_helyes_hash_rendben(self):
        self.assertEqual(self._futtat([self._d('glosszak_hu', DBH_GL)]).verdict, 'RENDBEN')

    def test_negativ_elrontott_hash_bukik(self):
        e = self._futtat([self._d('definicio_hu', DBH_DEF, forras_hash='0' * 40)])
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertIn('forras_hash eltér', e.peldak[0])

    def test_negativ_ismeretlen_lexid_bukik(self):
        e = self._futtat([self._d('definicio_hu', DBH_DEF, entry_id='999')])
        self.assertEqual(e.verdict, 'SÉRTÉS')
        self.assertIn('nincs hozzá forrásszöveg', e.peldak[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)
