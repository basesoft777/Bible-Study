#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teszt_szotari_gerinc.py — F131 (DT272, DT-F131a–e): a motívumlap szótári gerince.

Vizsgálja (a brief 2. lépése szerint):
  - a címkeforrást: BDB-példa és kutatói hozzárendelés (az ⓘ szövege);
  - a finomabb BDB-példa elsőbbségét a kutatói út alatt (2Móz 33:19 → Qal 3.b);
  - az ellentmondó esetet (a BDB-példa nem esik a kutatói út alá): GerincHiba, választás nélkül;
  - a minősítő alakot (`2.c (tagadva)` → `2.c`, a minősítő nem kerül a Jelentés-oszlopba);
  - a `horgonnyal` szakasz jelölését; az `elakad` szakasz explicit hiányát (angol + fordításra vár);
  - a magyar szövegben meg nem talált példahelyet (nincs kiemelés, napló);
  - a kapcsolót (csak az arany lap), az `ellenoriz.py` 17. szabályát, és a valódi adaton
    mind a 32 ISTENTISZT-001 sor címkéjét vagy kimondott hiányát.

    python eszkozok/teszt_szotari_gerinc.py
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

import lexikon_general as LG  # noqa: E402
import ellenoriz as E  # noqa: E402
import general as G  # noqa: E402


def cimke_sor(szotar, strong, szakasz, ljsz='', cimke=''):
    return {'szotar': szotar, 'strong': strong, 'szakasz': szakasz, 'lexikon_jelentes_szam': ljsz,
            'cimke_hu': cimke, 'hu_kezdet': '', 'hu_hossz': '', 'forditas_hash': '', 'proveniencia': 'scope=manual',
            'megjegyzes': ''}


def vj_sor(strong, sorszam, vers, utvonal):
    return {'strong': strong, 'sorszam': str(sorszam), 'karoli_vers': vers, 'utvonal': utvonal, 'szurt': '0'}


def adat(cimkek=(), vj=(), bdb_sz=None, bdb_hu=None):
    a = {'cimke': {}, 'bdb_sz': bdb_sz or {}, 'bdb_hu': bdb_hu or {}, 'bdb_vj': {}, 'th_sz': {}, 'th_vj': {},
         'glossza': {}}
    for c in cimkek:
        a['cimke'][(c['szotar'], c['strong'], c['szakasz'])] = c
    for r in vj:
        a['bdb_vj'].setdefault((r['strong'], r['karoli_vers']), []).append(r)
    return a


ALAP_CIMKEK = (
    cimke_sor('BDB', 'H7121', 'Qal/2/c', '2.c', 'segítségül hívni'),
    cimke_sor('BDB', 'H7121', 'Qal/3/-', '3', 'kihirdetni'),
    cimke_sor('BDB', 'H7121', 'Qal/3/b', '', 'a nevet kihirdetni'),
)
ALAP_SZ = {'H7121': [
    {'strong': 'H7121', 'sorszam': '8', 'utvonal': 'Qal/2/c', 'jel': 'c', 'szoveg': 'call with name'},
    {'strong': 'H7121', 'sorszam': '11', 'utvonal': 'Qal/3/-', 'jel': '3', 'szoveg': 'proclaim'},
    {'strong': 'H7121', 'sorszam': '13', 'utvonal': 'Qal/3/b', 'jel': 'b', 'szoveg': 'proclaim name'},
]}


def elo(igehely, jsz, strong='H7121+H8034', szotar='BDB', entry='H7121'):
    return {'id': 'ISTENTISZT-001', 'igehely': igehely, 'strong': strong, 'lexikon_szotar': szotar,
            'lexikon_entry_id': entry, 'jelentes_szam': jsz}


class Cimkeforras(unittest.TestCase):
    def test_bdb_pelda_es_kutatoi(self):
        a = adat(ALAP_CIMKEK, [vj_sor('H7121', 92, '1Móz 4:26', 'Qal/2/c')], ALAP_SZ)
        c, j, i = LG.jelentes_cimke_token(a, 'BDB', 'H7121', '2.c', '1Móz 4:26', True)
        self.assertEqual((c, j), ('segítségül hívni', 'Qal 2.c'))
        self.assertIn('BDB-példa', i)
        self.assertIn('sorszam 92', i)
        c, j, i = LG.jelentes_cimke_token(a, 'BDB', 'H7121', '2.c', '1Móz 13:4', True)
        self.assertEqual((c, j), ('segítségül hívni', 'Qal 2.c'))
        self.assertIn('kutatói hozzárendelés a BDB tagolása szerint', i)
        self.assertNotIn('BDB-példa', i)

    def test_finomabb_bdb_pelda_elsobbsege(self):
        a = adat(ALAP_CIMKEK, [vj_sor('H7121', 128, '2Móz 33:19', 'Qal/3/b')], ALAP_SZ)
        c, j, i = LG.jelentes_cimke_token(a, 'BDB', 'H7121', '3', '2Móz 33:19', True)
        self.assertEqual((c, j), ('a nevet kihirdetni', 'Qal 3.b'))
        self.assertIn('alá esik', i)

    def test_ellentmondo_eset_hiba(self):
        a = adat(ALAP_CIMKEK, [vj_sor('H7121', 999, '1Móz 4:26', 'Qal/3/b')], ALAP_SZ)
        with self.assertRaises(LG.GerincHiba):
            LG.jelentes_cimke_token(a, 'BDB', 'H7121', '2.c', '1Móz 4:26', True)

    def test_tobb_utvonalu_pelda_hiba(self):
        a = adat(ALAP_CIMKEK, [vj_sor('H7121', 1, '1Móz 4:26', 'Qal/2/c'),
                               vj_sor('H7121', 2, '1Móz 4:26', 'Qal/3/b')], ALAP_SZ)
        with self.assertRaises(LG.GerincHiba):
            LG.jelentes_cimke_token(a, 'BDB', 'H7121', '2.c', '1Móz 4:26', True)

    def test_minosito(self):
        self.assertEqual(LG.kutatoi_kulcs('2.c (tagadva)'), ('2.c', 'tagadva'))
        a = adat(ALAP_CIMKEK, [], ALAP_SZ)
        cella, ik = LG.jelentes_cella(a, elo('Jer 10:25', '2.c (tagadva)', strong='H7121'))
        self.assertEqual(cella, 'segítségül hívni · Qal 2.c')
        self.assertNotIn('tagadva', cella)
        self.assertIn('minősítője („tagadva”)', ik)

    def test_nincs_hozzarendeles_kimondva(self):
        a = adat(ALAP_CIMKEK, [], ALAP_SZ)
        cella, ik = LG.jelentes_cella(a, elo('1Móz 26:25', '2.c'))
        self.assertIn('H8034: *(nincs hozzárendelés)*', cella)
        self.assertIn('nincs kutatói hozzárendelés', ik)

    def test_lekepezetlen_kutatoi_kulcs(self):
        a = adat(ALAP_CIMKEK, [], ALAP_SZ)
        cella, ik = LG.jelentes_cella(a, elo('Zak 13:9', '7.z', strong='H7121'))
        self.assertEqual(cella, '*(nincs hozzárendelés)*')
        self.assertIn('nincs leképezve', ik)


class Megjelenites(unittest.TestCase):
    def test_szakasz_jel(self):
        self.assertEqual(LG.szakasz_jel('Qal/2/c'), 'Qal 2.c')
        self.assertEqual(LG.szakasz_jel('Qal/3/-'), 'Qal 3')
        self.assertEqual(LG.szakasz_jel('-/3/-'), '3')
        self.assertEqual(LG.szakasz_jel('-/2/a'), '2.a')
        self.assertEqual(LG.szakasz_jel('Qal/-/-'), 'Qal')
        self.assertEqual(LG.szakasz_jel("Niph'al/2/c"), "Niph'al 2.c")
        self.assertEqual(LG.szakasz_jel('2'), '2')

    def test_utvonal_vag_es_ala_esik(self):
        self.assertEqual(LG.gerinc_utvonal_vag('-/3/-'), '-/3')
        self.assertTrue(LG.gerinc_ala_esik('-/3', '-/3/-'))
        self.assertTrue(LG.gerinc_ala_esik('Qal/3/b', 'Qal/3/-'))
        self.assertFalse(LG.gerinc_ala_esik('Qal/3/-', 'Qal/3/b'))
        self.assertFalse(LG.gerinc_ala_esik("Niph'al/2/c", 'Qal/2/-'))

    def test_kiemeles_oroklott_konyvvel(self):
        sz = '3 név … 1Móz 4:26 (J): valamivel hívni, így 12:8; 13:4; 2Móz 20:24'
        uj, t, h = LG.kiemel(sz, [('1Móz 4:26', 'a'), ('1Móz 12:8', 'b'), ('2Móz 12:8', 'c')])
        self.assertIn('**1Móz 4:26**', uj)
        self.assertIn('**12:8**', uj)
        self.assertNotIn('**13:4**', uj)
        self.assertEqual(sorted(t), ['a', 'b'])
        self.assertEqual(h, ['c'])

    def test_meg_nem_talalt_pelda(self):
        uj, t, h = LG.kiemel('c. hívni: 1Móz 4:26', [('Jer 10:25', 'x')])
        self.assertNotIn('**', uj)
        self.assertEqual((t, h), ([], ['x']))

    def test_ketszeres_elofordulas(self):
        uj, t, h = LG.kiemel('(1Kir 18:24 a) Baál 1Kir 18:24-25', [('1Kir 18:24', 'a'), ('1Kir 18:24', 'b')])
        self.assertEqual(uj.count('**1Kir 18:24**'), 2)
        self.assertEqual(t, ['a', 'b'])

    def _hu_adat(self, kategoria):
        sz = {'H8034': [
            {'strong': 'H8034', 'sorszam': '1', 'utvonal': 'cim', 'jel': '', 'szoveg': ''},
            {'strong': 'H8034', 'sorszam': '2', 'utvonal': 'fej', 'jel': '', 'szoveg': 'name'},
            {'strong': 'H8034', 'sorszam': '3', 'utvonal': '-/4/-', 'jel': '4', 'szoveg': 'of false gods'},
            {'strong': 'H8034', 'sorszam': '4', 'utvonal': '-/5/-', 'jel': '5', 'szoveg': 'memorial Isa 55:13'},
        ]}
        hu = {('H8034', '2'): {'szoveg_hu': 'H8034. név', 'kategoria': 'jelolo_nelkul'},
              ('H8034', '3'): {'szoveg_hu': '4 hamis istenekről 1Kir 18:24', 'kategoria': 'illeszkedik'},
              ('H8034', '4'): {'szoveg_hu': '' if kategoria == 'elakad' else '5 = emlékjel Ézs 55:13',
                               'kategoria': kategoria}}
        return adat([], [vj_sor('H8034', 300, 'Ézs 55:13', '-/5')], sz, hu)

    def test_horgonnyal_jelolve(self):
        a = self._hu_adat('horgonnyal')
        bek, napl = LG.gerinc_blokk(a, 'BDB', 'H8034', [elo('Ézs 55:13', '', strong='H8034', entry='')])
        szov = '\n'.join(bek)
        self.assertIn('horgonnyal illesztve, ellenőrzendő', szov)
        self.assertIn('**Ézs 55:13**', szov)
        self.assertEqual(len(napl['kiemelt']), 1)

    def test_elakad_explicit_hiany(self):
        a = self._hu_adat('elakad')
        bek, napl = LG.gerinc_blokk(a, 'BDB', 'H8034', [elo('Ézs 55:13', '', strong='H8034', entry='')])
        szov = '\n'.join(bek)
        self.assertIn('memorial Isa 55:13', szov)
        self.assertIn(LG.FORDITASRA_VAR, szov)
        self.assertEqual(napl['kiemelt'], [])
        self.assertEqual(len(napl['nem_talalt']), 1)

    def test_nem_hordozo_osszecsukva(self):
        a = self._hu_adat('illeszkedik')
        szov = '\n'.join(LG.gerinc_blokk(a, 'BDB', 'H8034', [elo('Ézs 55:13', '', strong='H8034', entry='')])[0])
        self.assertIn('<details>', szov)
        self.assertIn('- `4` — hamis istenekről 1Kir 18', szov)

    def test_kapcsolo(self):
        self.assertTrue(LG.gerinc_aktiv('ISTENTISZT-001'))
        for mid in ('ALVIL-001', 'HAMART-001', 'KIRALY-001', 'TEREMT-001', None):
            self.assertFalse(LG.gerinc_aktiv(mid))


class Ellenoriz17(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.hu = 'G9999 — x, y: fej. 1. első rész. 2. második rész.'

        def ir(nev, fej, sorok):
            with open(os.path.join(self.d, nev), 'w', encoding='utf-8') as f:
                f.write('\t'.join(fej) + '\n' + ''.join('\t'.join(s) + '\n' for s in sorok))
        self.ir = ir
        ir('bdb_szakaszok.tsv', ['strong', 'utvonal'], [['H7121', 'Qal/2/c'], ['H8034', '-/3/-']])
        ir('thayer_szakaszok.tsv', ['strong', 'utvonal'], [['G9999', 'cim'], ['G9999', '-/1/-'], ['G9999', '-/2/-']])
        ir('lexikon_hivatkozasok.tsv', ['szotar', 'strong', 'jelentes_szam'], [['BDB', 'H7121', '2.c'],
                                                                               ['TBESG', 'G9999', '2']])
        ir('forditasok.tsv', ['szotar', 'strong', 'jelentes_szam', 'mezo', 'forditas_hu'],
           [['Thayer', 'G9999', 'teljes', 'forditas_hu', self.hu]])

    def tearDown(self):
        shutil.rmtree(self.d)

    def cimke(self, sorok):
        self.ir('szotar_szakasz_cimke.tsv', ['szotar', 'strong', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu',
                                             'hu_kezdet', 'hu_hossz', 'forditas_hash', 'proveniencia', 'megjegyzes'],
                sorok)
        return E.szakasz_cimke_hibak(self.d)

    def thayer(self, hash_=None):
        h = hash_ or hashlib.sha1(self.hu.encode('utf-8')).hexdigest()
        k1 = self.hu.index('1.')
        k2 = self.hu.index('2.')
        return [['Thayer', 'G9999', 'cim', '', '', '0', str(len(self.hu[:k1].rstrip())), h, 'p', ''],
                ['Thayer', 'G9999', '-/1/-', '', '', str(k1), str(len(self.hu[k1:k2].rstrip())), h, 'p', ''],
                ['Thayer', 'G9999', '-/2/-', '', '', str(k2), str(len(self.hu) - k2), h, 'p', '']]

    def test_rendben(self):
        h = self.cimke([['BDB', 'H7121', 'Qal/2/c', '2.c', 'segítségül hívni', '', '', '', 'p', ''],
                        ['BDB', 'H8034', '-/3', '', 'név', '', '', '', 'p', ''],
                        ['TBESG', 'G9999', '2', '2', 'x', '', '', '', 'p', '']] + self.thayer())
        self.assertEqual(h, [])

    def test_hibak(self):
        h = self.cimke([['BDB', 'H7121', 'Qal/9/z', '', '', '', '', '', 'p', ''],
                        ['BDB', 'H7121', 'Qal/2/c', '3', 'nem invokáció', '', '', '', 'p', ''],
                        ['TBESG', 'G9999', '7', '', '', '', '', '', '', '']])
        szov = '\n'.join(h)
        self.assertIn('nincs a bdb_szakaszok.tsv-ben', szov)
        self.assertIn('nem lexikon_hivatkozasok.tsv-kulcs', szov)
        self.assertIn('tiltott minősítést', szov)
        self.assertIn('üres proveniencia', szov)

    def test_thayer_elavult_es_hezag(self):
        h = self.cimke(self.thayer(hash_='0' * 40))
        self.assertTrue(any('elavultak' in x for x in h))
        rossz = self.thayer()
        rossz[1][6] = '3'
        h = self.cimke(rossz)
        self.assertTrue(any('hézag nélkül' in x for x in h))


class ValodiAdat(unittest.TestCase):
    """A repó mai adatán: mind a 32 sor kap címkét vagy kimondott hiányt, ellentmondás nélkül;
    a 17. szabály RENDBEN."""

    def test_32_sor(self):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        sorai = [s for s in elo_sorok if s['id'] == 'ISTENTISZT-001']
        self.assertEqual(len(sorai), 32)
        a = LG.gerinc_adat()
        for s in sorai:
            cella, ik = LG.jelentes_cella(a, s)
            self.assertTrue(cella, s['igehely'])
            self.assertTrue(ik, s['igehely'])
            entry_resz = cella.split(';')[0]
            self.assertNotIn('nincs hozzárendelés', entry_resz, s['igehely'])
            for tiltott in ('eltér', 'máshová sorol', 'NEM invokáció', 'szemben a BDB', 'a BDB szerint nem'):
                self.assertNotIn(tiltott.lower(), cella.lower())

    def test_2moz_33_19(self):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == '2Móz 33:19')
        cella, _ik = LG.jelentes_cella(LG.gerinc_adat(), s)
        self.assertIn('Qal 3.b', cella)

    def test_szabaly17(self):
        self.assertEqual(E.szabaly17_szakasz_cimke(E.ALAPERTELMEZETT_ADAT).verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main()
