#!/usr/bin/env python3
"""teszt_szakasz_forditas.py — a szakasz hiányzó szótári fordításainak listája (F205 M4).

A tesztek a repó valós szótár- és szakasztábláin futnak (a láncok saját állapot-szabályát kell visszaadniuk), a
fordítási sorok fixture-ök; a kimenet a repón kívüli ideiglenes mappába íródik, a repóban fájl nem keletkezik.

Futtatás: python -m unittest eszkozok.teszt_szakasz_forditas  (a repó gyökeréből)
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import szakasz_forditas as SF  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def bdb(jsz, allapot='opus', h='x', hu='föld'):
    return {'szotar': 'BDB', 'strong': 'H0127', 'entry_id': 'H127', 'jelentes_szam': jsz, 'mezo': 'forditas_hu',
            'forras_hash': h, 'forditas_hu': hu, 'allapot': allapot}


class Szakasz(unittest.TestCase):
    def test_elemzes(self):
        self.assertEqual(SF.szakasz_elemez('1Móz 8:20-22'), ('1Móz', (8, 20), (8, 22)))
        self.assertEqual(SF.szakasz_elemez('1Móz 4:25-5:32'), ('1Móz', (4, 25), (5, 32)))
        self.assertEqual(SF.szakasz_elemez('1Móz 14'), ('1Móz', (14, 1), (14, None)))
        self.assertEqual(SF.szakasz_elemez('Mt 5:3'), ('Mt', (5, 3), (5, 3)))
        for rossz in ('1Móz', '1Móz 8:22-20', 'Gen.8.21', '1Móz 8-9'):
            with self.assertRaises(SystemExit):
                SF.szakasz_elemez(rossz)

    def test_benne_karoli_kulcs(self):
        self.assertTrue(SF.benne('1Móz 5:1', '1Móz', (4, 25), (5, 32)))
        self.assertFalse(SF.benne('1Móz 4:24', '1Móz', (4, 25), (5, 32)))
        self.assertTrue(SF.benne('1Móz 14:24', '1Móz', (14, 1), (14, None)))
        self.assertFalse(SF.benne('2Móz 14:1', '1Móz', (14, 1), (14, None)))

    def test_osszevont_strong_elemenkent(self):
        st, fajl, versek = SF.szakasz_strongok('Mt', (1, 1), (1, 25))
        self.assertEqual(fajl, 'TAGNT_kivonat.tsv')
        self.assertTrue(versek > 0)
        self.assertTrue(all('+' not in s for s in st))


class Allapot(unittest.TestCase):
    def test_bdb_nincs_sor_hianyzik(self):
        a, _, k, e = SF.bdb_allapot('H0127', [])
        self.assertEqual(a, 'hianyzik')
        self.assertTrue(k > 0 and e > 0)

    def test_bdb_ervenyes_teljes_sor_kesz(self):
        self.assertEqual(SF.bdb_allapot('H0127', [bdb('teljes')])[0], 'kesz')
        self.assertEqual(SF.bdb_allapot('H0127', [bdb('teljes', allapot='kezi')])[0], 'kesz')

    def test_bdb_elavult_teljes_sor_hianyzik(self):
        self.assertEqual(SF.bdb_allapot('H0127', [bdb('teljes', allapot='elavult')])[0], 'hianyzik')

    def test_bdb_reszleges_szakaszsor_hianyos(self):
        szak = SF.SB.szakaszok('H0127')
        self.assertTrue(len(szak) > 1)
        sorok = [bdb('sz%d' % szak[0]['sorszam'], h=szak[0]['hash'])]
        a, _, k, e = SF.bdb_allapot('H0127', sorok)
        self.assertEqual(a, 'hianyos')
        self.assertEqual(e, len(szak) - 1)
        self.assertEqual(k, sum(len(x['szoveg']) for x in szak[1:]))

    def test_bdb_teljes_szakaszfedes_kesz(self):
        szak = SF.SB.szakaszok('H0127')
        sorok = [bdb('sz%d' % x['sorszam'], h=x['hash']) for x in szak]
        self.assertEqual(SF.bdb_allapot('H0127', sorok)[0], 'kesz')
        sorok[0]['forras_hash'] = 'regi'
        self.assertEqual(SF.bdb_allapot('H0127', sorok)[0], 'elavult_hash')

    def test_bdb_szotaron_kivul(self):
        self.assertEqual(SF.bdb_allapot('H5668', [])[0], 'nincs_szakasz')

    def test_tbesg(self):
        c = {}
        forras = SF.GLF.tovabbi_forras({'szotar': 'TBESG', 'strong': 'G1944', 'entry_id': 'G1944',
                                        'jelentes_szam': 'rovid', 'mezo': 'glosszak_hu'}, cache=c)
        h = hashlib.sha1(forras.encode('utf-8')).hexdigest()
        sor = {'jelentes_szam': 'rovid', 'mezo': 'glosszak_hu', 'forras_hash': h, 'forditas_hu': 'átkozott',
               'allapot': 'sonnet'}
        self.assertEqual(SF.tbesg_allapot('G1944', [sor], c)[0], 'kesz')
        self.assertEqual(SF.tbesg_allapot('G1944', [dict(sor, forras_hash='regi')], c)[0], 'elavult_hash')
        self.assertEqual(SF.tbesg_allapot('G1944', [dict(sor, allapot='elavult')], c)[0], 'hianyzik')
        self.assertEqual(SF.tbesg_allapot('G1944', [], c)[0], 'hianyzik')


class Futas(unittest.TestCase):
    """A HAMART-001 Strongjaira az F182.17 mérte: minden érvényes fordítással áll (fordítandó 0)."""

    def test_hamart_szakasz_nincs_forditando(self):
        e = SF.futtat('1Móz 8:20-22', '2026-11-12')
        self.assertFalse([r for r in e['sorok'] if r['allapot'] in SF.FORDITANDO])
        self.assertTrue(e['kihagyott'])                       # a nyelvtani Strongok kimaradnak
        for r in e['sorok']:
            self.assertIn('scope=H', r['proveniencia'])
            self.assertIn('ts=2026-11-12', r['proveniencia'])

    def test_alias_a_szocikk_strongjara(self):
        e = SF.futtat('1Móz 8:22', '2026-11-12')
        r = [r for r in e['sorok'] if r['strong'] == 'H7019']
        self.assertTrue(r and r[0]['cel'] == 'H6972' and r[0]['allapot'] == 'kesz')

    def test_ismeretlen_szakasz(self):
        with self.assertRaises(SystemExit):
            SF.futtat('Xyz 1:1', '2026-11-12')

    def test_kimenet_repon_kivul_es_lancbemenet(self):
        with self.assertRaises(SystemExit):
            SF.kiir(SF.futtat('1Móz 8:20-22', '2026-11-12'), os.path.join(GYOKER, 'naplok', '_szakasz_proba'))
        self.assertFalse(os.path.exists(os.path.join(GYOKER, 'naplok', '_szakasz_proba')))
        e = SF.futtat('Gal 3:10-14', '2026-11-12')
        with tempfile.TemporaryDirectory() as d:
            SF.kiir(e, d)
            with open(os.path.join(d, 'glossza_lista.tsv'), encoding='utf-8') as f:
                sorok = [s.split('\t') for s in f.read().splitlines()]
            self.assertEqual(sorok[0], SF.GLOSSZA_FEJLEC)
            self.assertTrue(all(s[-1] == 'hianyzik' and s[0] == 'TBESG' for s in sorok[1:]))
            with open(os.path.join(d, 'thayer_strongok.txt'), encoding='utf-8') as f:
                th = [s for s in f.read().splitlines() if s and not s.startswith('#')]
            vart = [r['strong'] for r in e['sorok'] if r['lanc'] == 'Thayer' and r['allapot'] in SF.FORDITANDO]
            self.assertEqual(th, vart)

    def test_repo_erintetlen(self):
        elotte = subprocess.run(['git', 'status', '--porcelain'], cwd=GYOKER, capture_output=True, text=True).stdout
        with tempfile.TemporaryDirectory() as d:
            SF.main(['--szakasz', 'Gal 3:13-14', '--ts', '2026-11-12', '--ki', d])
        utana = subprocess.run(['git', 'status', '--porcelain'], cwd=GYOKER, capture_output=True, text=True).stdout
        self.assertEqual(elotte, utana)


if __name__ == '__main__':
    unittest.main()
