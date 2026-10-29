#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teszt_szotari_gerinc.py — F131 (DT272, DT371–e): a motívumlap szótári gerince.

Vizsgálja (a brief 2. lépése szerint):
  - a címkeforrást: BDB-példa és kutatói hozzárendelés (az ⓘ szövege);
  - a finomabb BDB-példa elsőbbségét a kutatói út alatt (2Móz 33:19 → Qal 3.b);
  - az ellentmondó esetet (a BDB-példa nem esik a kutatói út alá): GerincHiba, választás nélkül;
  - a minősítő alakot (`2.c (tagadva)` → `2.c`, a minősítő nem kerül a Jelentés-oszlopba);
  - a `horgonnyal` szakasz jelölését; az `elakad` szakasz explicit hiányát (angol + fordításra vár);
  - a magyar szövegben meg nem talált példahelyet (nincs kiemelés, napló);
  - a kapcsolót (csak az arany lap), az `ellenoriz.py` 17. szabályát, és a valódi adaton
    mind a 33 ISTENTISZT-001 sor címkéjét vagy kimondott hiányát.

    python eszkozok/teszt_szotari_gerinc.py
"""
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
        # kutatói hozzárendelés nélkül a több útvonalú BDB-példa kézi kérdés
        a = adat(ALAP_CIMKEK, [vj_sor('H7121', 1, '1Móz 4:26', 'Qal/2/c'),
                               vj_sor('H7121', 2, '1Móz 4:26', 'Qal/3/b')], ALAP_SZ)
        with self.assertRaises(LG.GerincHiba):
            LG.jelentes_cimke_token(a, 'BDB', 'H7121', '', '1Móz 4:26', True)

    def test_tobb_utvonalu_pelda_kutatoi_dontes(self):
        # F123 (DT-F123h): ha a kutatói út pontosan egy példa-útvonalat fed, az dönt; a másik ⓘ-ben marad
        a = adat(ALAP_CIMKEK, [vj_sor('H7121', 1, '1Móz 4:26', 'Qal/2/c'),
                               vj_sor('H7121', 2, '1Móz 4:26', 'Qal/3/b')], ALAP_SZ)
        c, j, i = LG.jelentes_cimke_token(a, 'BDB', 'H7121', '2.c', '1Móz 4:26', True)
        self.assertEqual((c, j), ('segítségül hívni', 'Qal 2.c'))
        self.assertIn('a Qal 3.b is idézi', i)
        self.assertIn('a kutatói hozzárendelés (2.c → Qal 2.c', i)

    def test_minosito(self):
        self.assertEqual(LG.kutatoi_kulcs('2.c (tagadva)'), ('2.c', 'tagadva'))
        a = adat(ALAP_CIMKEK, [], ALAP_SZ)
        cella, ik = LG.jelentes_cella(a, elo('Jer 10:25', '2.c (tagadva)', strong='H7121'))
        self.assertEqual(cella, 'segítségül hívni · Qal 2.c')
        self.assertNotIn('tagadva', cella)
        self.assertIn('minősítője („tagadva”)', ik)

    def test_nincs_hozzarendeles_kimondva(self):
        a = adat(ALAP_CIMKEK, [], ALAP_SZ)
        cella, ik = LG.jelentes_cella(a, elo('Zsolt 116:4', '2.c'))
        self.assertIn('H8034: *(nincs hozzárendelés)*', cella)
        self.assertIn('nincs kutatói hozzárendelés', ik)

    def test_tobb_token_a_versben(self):
        # ELLENOR_SZOTARI_GERINC 1. (7.4a): a versszintű BDB-példa nem kerül a tokenre, ha a Strongnak a versben
        # >=2 tokenje van; kutatói hozzárendelés nélkül a cella kimondott hiány, az ⓘ az okot mondja
        sz = {'H8034': [{'strong': 'H8034', 'sorszam': '10', 'utvonal': '-/4/-', 'jel': '4', 'szoveg': 'false gods'}]}
        a = adat((cimke_sor('BDB', 'H8034', '-/4/-', '', 'név: hamis istenekről'),),
                 [vj_sor('H8034', 208, '1Kir 18:24', '-/4')], sz)
        c, j, i = LG.jelentes_cimke_token(a, 'BDB', 'H8034', '', '1Kir 18:24', False)
        self.assertEqual((c, j), ('név: hamis istenekről', '4'))
        a['token_szam'] = {('1Kir 18:24', 'H8034'): 2}
        c, j, i = LG.jelentes_cimke_token(a, 'BDB', 'H8034', '', '1Kir 18:24', False)
        self.assertEqual((c, j), (None, ''))
        self.assertIn('a versben a szó kétszer áll', i)
        self.assertIn('sorszam 208', i)
        self.assertNotIn('BDB-példa: a BDB', i)
        # kutatói hozzárendeléssel a címke a kutatóié, a BDB-példa nem
        a2 = adat(ALAP_CIMKEK, [vj_sor('H7121', 92, '1Móz 4:26', 'Qal/2/c')], ALAP_SZ)
        a2['token_szam'] = {('1Móz 4:26', 'H7121'): 2}
        c, j, i = LG.jelentes_cimke_token(a2, 'BDB', 'H7121', '2.c', '1Móz 4:26', True)
        self.assertEqual((c, j), ('segítségül hívni', 'Qal 2.c'))
        self.assertIn('kutatói hozzárendelés', i)
        self.assertIn('kétszer áll', i)
        self.assertNotIn('verstartomány belsejében', i)

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

    def test_szakasz_szoveg(self):
        # a prózai ⓘ névelője és sorszámnév-pontja (a „a(z) 4 szakaszban” helyett)
        self.assertEqual(LG.szakasz_szoveg('4'), 'a 4.')
        self.assertEqual(LG.szakasz_szoveg('1'), 'az 1.')
        self.assertEqual(LG.szakasz_szoveg('5'), 'az 5.')
        self.assertEqual(LG.szakasz_szoveg('Qal 2.c'), 'a Qal 2.c')
        self.assertEqual(LG.szakasz_szoveg("Hiph'il 1"), "a Hiph'il 1")
        self.assertEqual(LG.szakasz_szoveg('Ithpa'), 'az Ithpa')
        self.assertEqual(LG.szakasz_szoveg(['3', '4']), 'a 3., 4.')
        self.assertEqual(LG.szakasz_szoveg('3', nevelo=False), '3.')

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

    def test_jelolo_levag(self):
        # a kibontott szakasz idézete nem ismétli a címke jelét („`3` — név…” után „> 3 név…”)
        self.assertEqual(LG.jelolo_levag('3 név, mint Isten megjelölése', '3'), 'név, mint Isten megjelölése')
        self.assertEqual(LG.jelolo_levag('2. a. rendszerint személyé', '2.a'), 'rendszerint személyé')
        self.assertEqual(LG.jelolo_levag('c. hívni ׳י nevével', 'Qal 2.c'), 'hívni ׳י nevével')
        self.assertEqual(LG.jelolo_levag('1. nevet adni', '1'), 'nevet adni')
        self.assertEqual(LG.jelolo_levag('b. = hírnév', '2.b'), '= hírnév')
        # nem a saját jele, névelő, igehely, üres maradék: változatlan
        self.assertEqual(LG.jelolo_levag('4 hamis istenekről', '3'), '4 hamis istenekről')
        self.assertEqual(LG.jelolo_levag('a név ereje', '2.a'), 'a név ereje')
        self.assertEqual(LG.jelolo_levag('1Móz 4:26 szerint', '1'), '1Móz 4:26 szerint')
        self.assertEqual(LG.jelolo_levag('3 ', '3'), '3 ')

    def test_kibontott_idezet_jel_nelkul(self):
        a = self._hu_adat('illeszkedik')
        szov = '\n'.join(LG.gerinc_blokk(a, 'BDB', 'H8034', [elo('Ézs 55:13', '', strong='H8034', entry='')])[0])
        self.assertIn('> = emlékjel **Ézs 55:13**', szov)
        self.assertNotIn('> 5 ', szov)

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
        self.assertTrue(LG.gerinc_aktiv('ALVIL-001'))  # F123 (DT-F123g (a)): a migrációval bekapcsolva
        for mid in ('HAMART-001', 'KIRALY-001', 'TEREMT-001', None):
            self.assertFalse(LG.gerinc_aktiv(mid))


class Ellenoriz17(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

        def ir(nev, fej, sorok):
            with open(os.path.join(self.d, nev), 'w', encoding='utf-8') as f:
                f.write('\t'.join(fej) + '\n' + ''.join('\t'.join(s) + '\n' for s in sorok))
        self.ir = ir
        ir('bdb_szakaszok.tsv', ['strong', 'utvonal'], [['H7121', 'Qal/2/c'], ['H8034', '-/3/-']])
        ir('thayer_szakaszok.tsv', ['strong', 'utvonal'], [['G9999', 'cim'], ['G9999', '-/1/-'], ['G9999', '-/2/-']])
        ir('lexikon_hivatkozasok.tsv', ['szotar', 'strong', 'jelentes_szam'], [['BDB', 'H7121', '2.c'],
                                                                               ['TBESG', 'G9999', '2']])
        ir('tiltott_fordulatok.tsv', ['magyar_alak', 'minta'],
           [['nevet tenni valakire', r'\bnevet\s+(?:tenni|tesz\w*|tett\w*)\s+(?:valaki\w*|rá\b)']])

    def tearDown(self):
        shutil.rmtree(self.d)

    def cimke(self, sorok):
        self.ir('szotar_szakasz_cimke.tsv', ['szotar', 'strong', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu',
                                             'proveniencia', 'megjegyzes'], sorok)
        return E.szakasz_cimke_hibak(self.d)

    def test_rendben(self):
        h = self.cimke([['BDB', 'H7121', 'Qal/2/c', '2.c', 'segítségül hívni', 'p', ''],
                        ['BDB', 'H8034', '-/3', '', 'név', 'p', ''],
                        ['TBESG', 'G9999', '2', '2', 'x', 'p', ''],
                        ['Thayer', 'G9999', '-/1/-', '', 'elnevezni', 'p', '']])
        self.assertEqual(h, [])

    def test_hibak(self):
        h = self.cimke([['BDB', 'H7121', 'Qal/9/z', '', '', 'p', ''],
                        ['BDB', 'H7121', 'Qal/2/c', '3', 'nem invokáció', 'p', ''],
                        ['TBESG', 'G9999', '7', '', '', '', ''],
                        ['Thayer', 'G9999', '-/9/-', '', 'nevet tenni valakire', 'p', '']])
        szov = '\n'.join(h)
        self.assertIn('nincs a bdb_szakaszok.tsv-ben', szov)
        self.assertIn('nincs a thayer_szakaszok.tsv-ben', szov)
        self.assertIn('nem lexikon_hivatkozasok.tsv-kulcs', szov)
        self.assertIn('tiltott minősítést', szov)
        self.assertIn('tiltott fordulatot', szov)
        self.assertIn('üres proveniencia', szov)


class ThayerSzakaszsorok(unittest.TestCase):
    """DT373 1.: a magyar Thayer a #142 sz<n> soraiból; hiányzó sor: angol + fordításra vár;
    a tiltott fordulat a lapon ismert hiányként jelölve, a szöveg nem íródik át."""

    def test_sz_sorok_es_tiltott(self):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        sorai = [s for s in elo_sorok if s['id'] == 'ISTENTISZT-001']
        a = LG.gerinc_adat()
        szak = LG.thayer_gerinc_szakaszok(a, 'G1941')
        self.assertEqual([s[4] for s in szak], ['sz2', 'sz3', 'sz4', 'sz5', 'sz6', 'sz7'])
        self.assertTrue(all(s[2] for s in szak))
        bek, napl = LG.gerinc_blokk(a, 'Thayer', 'G1941', sorai)
        szov = '\n'.join(bek)
        # ELLENOR_SZOTARI_GERINC 2.: a jelöletlen folytatás (ApCsel 9:21, 22:16) is a Thayer példahelye: 7 → 9
        self.assertEqual(len(napl['kiemelt']), 9)
        self.assertEqual(napl['nem_talalt'], [])
        self.assertNotIn('ApCsel 9:21', napl['nem_idezett'])
        self.assertNotIn('ApCsel 22:16', napl['nem_idezett'])
        if any('nevet tenni valakire' in (s[2] or '') for s in szak):
            self.assertTrue(any('sz3' in x for x in napl['tiltott']))
            self.assertIn('ismert hiány', szov)

    def test_hianyzo_sz_sor(self):
        a = dict(LG.gerinc_adat())
        a['th_sz'] = {'G0000': [{'strong': 'G0000', 'sorszam': '1', 'utvonal': 'cim', 'jel': '', 'szoveg': 'x'},
                                {'strong': 'G0000', 'sorszam': '2', 'utvonal': '-/1/-', 'jel': '1.', 'szoveg': 'to call'}]}
        szak = LG.thayer_gerinc_szakaszok(a, 'G0000')
        self.assertEqual(szak, [('-/1/-', '1', None, '1. to call', 'sz2')])


class DbhOszlop(unittest.TestCase):
    """DT380: az ÓSZ-sorok „UBS-jelentés” cellája a DBH-ból, tokenenként; hiány soha nem néma."""

    def test_1moz_4_26_tokenenkent(self):
        c = LG.dbh_jelentes_cella('1Móz 4:26', 'H7121+H8034')
        self.assertTrue(c.startswith('H7121: '))
        self.assertIn('[ⓘ](/szo/H7121)', c)                               # F121 (DT393): kód + glossza + ⓘ a szónézetre
        self.assertNotIn('= action by which', c)
        self.assertIn(' · H8034: ', c)
        h7121 = c.split(' · H8034: ')[0]
        self.assertEqual(h7121.count('`0065620'), 2)
        if 'fordításra vár' not in c:
            self.assertNotIn('= action by which', c)

    def test_nincs_hivatkozas_kimondva(self):
        # F121: a Jóel 2:32 a #146 óta (Károli↔MT versszámozás) hivatkozik; helyette az Ézs 7:11 (H7585), amelyre a DBH nem
        c = LG.dbh_jelentes_cella('Ézs 7:11', 'H7585')
        self.assertIn('nincs DBH-hivatkozás', c)
        self.assertIn('keresett MT-vers', c)

    def test_g_token_nelkul(self):
        self.assertIn('nincs H-token', LG.dbh_jelentes_cella('1Móz 4:26', 'G1941'))


class ValodiAdat(unittest.TestCase):
    """A repó mai adatán: mind a 33 sor kap címkét vagy kimondott hiányt, ellentmondás nélkül;
    a 17. szabály RENDBEN. (A 33. sor az Ézs 64:6, DT399.)"""

    def test_33_sor(self):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        sorai = [s for s in elo_sorok if s['id'] == 'ISTENTISZT-001']
        self.assertEqual(len(sorai), 33)
        a = LG.gerinc_adat()
        for s in sorai:
            cella, ik = LG.jelentes_cella(a, s)
            self.assertTrue(cella, s['igehely'])
            self.assertTrue(ik, s['igehely'])
            entry_resz = cella.split(';')[0]
            self.assertNotIn('nincs hozzárendelés', entry_resz, s['igehely'])
            for tiltott in ('eltér', 'máshová sorol', 'NEM invokáció', 'szemben a BDB', 'a BDB szerint nem'):
                self.assertNotIn(tiltott.lower(), cella.lower())

    def test_1moz_26_25_forras_javitas(self):
        # DT381 (a): a 2.31 kézi sora javítja a BDB „26:35”-ét; a H8034 cellája valódi BDB-példa, az ⓘ a javítás forrása
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == '1Móz 26:25')
        cella, ik = LG.jelentes_cella(LG.gerinc_adat(), s)
        self.assertNotIn('nincs hozzárendelés', cella)
        self.assertNotIn('gyanú', cella + ik)
        self.assertIn('BDB-példa', ik)
        self.assertIn('„26:35”', ik)
        self.assertIn('adat/bdb_forras_javitas.tsv', ik)
        self.assertIn('DT381 (a)', ik)

    def test_1kir_18_25_26_bdb_pelda(self):
        # DT382 (A): az „1Kin 18:24-25, 26” folytatása (18:26) BDB-példa; a 18:25 a tartomány belseje, nem az
        a = LG.gerinc_adat()
        self.assertTrue(LG.bdb_peldak(a, 'H8034', '1Kir 18:26'))
        self.assertTrue(LG.bdb_peldak(a, 'H7121', '1Kir 18:26'))
        self.assertFalse(LG.bdb_peldak(a, 'H8034', '1Kir 18:25'))

    def test_1kir_18_25_tartomanyban(self):
        # DT382 (A): a 18:25 a „1Kin 18:24-25” tartomány belseje; a cella hiányt mond, az ⓘ a tartományt nevezi meg
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == '1Kir 18:25')
        cella, ik = LG.jelentes_cella(LG.gerinc_adat(), s)
        self.assertIn('H8034: *(nincs hozzárendelés)*', cella)
        self.assertNotIn('nincs kutatói hozzárendelés és szótári példahely', ik)
        self.assertEqual(ik.count('az 1Kir 18:24–25 verstartomány belsejében (a BDB-ben: „1Kin 18:24-25”'), 2)
        self.assertIn('sorszam 99)', ik)
        self.assertIn('sorszam 208)', ik)
        self.assertNotIn('sorszam 97)', ik)

    def test_1kir_18_24_h8034_nem_a_tokenen(self):
        # ELLENOR_SZOTARI_GERINC 1. (7.4a): a versben két H8034 áll (a ti isteneitek neve, az Úr neve); a BDB 4
        # (hamis istenekről) versszintű példája nem kerülhet a sor tokenjére
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == '1Kir 18:24')
        cella, ik = LG.jelentes_cella(LG.gerinc_adat(), s)
        self.assertIn('H8034: *(nincs hozzárendelés)*', cella)
        self.assertNotIn('hamis istenekről', cella)
        self.assertIn('H8034 — a BDB a verset a 4. szakaszban idézi', ik)
        self.assertIn('kétszer áll', ik)

    def test_tobb_token_szabaly_merete(self):
        # a 33 sorból a szabály két sort érint (1Móz 4:26, 1Kir 18:24), mindkettőn mindkét H-tokent
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        a = LG.gerinc_adat()
        erint = set()
        for s in elo_sorok:
            if s['id'] != 'ISTENTISZT-001':
                continue
            for t in s['strong'].split('+'):
                for v in LG.igehely_lista(s['igehely']):
                    if t.startswith('H') and LG.bdb_peldak(a, t, v) and a['token_szam'].get((v, t), 0) >= 2:
                        erint.add((s['igehely'], t))
        self.assertEqual(erint, {('1Móz 4:26', 'H7121'), ('1Móz 4:26', 'H8034'),
                                 ('1Kir 18:24', 'H7121'), ('1Kir 18:24', 'H8034')})

    def test_apcsel_9_21_22_16_thayer_idezi(self):
        # ELLENOR_SZOTARI_GERINC 2. (7.5a): a Thayer „Act 9:14,21; 22:16” folytatása; az ⓘ nem mondhatja, hogy nem idézi
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        for h in ('ApCsel 9:21', 'ApCsel 22:16'):
            s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == h)
            _cella, ik = LG.jelentes_cella(LG.gerinc_adat(), s)
            self.assertNotIn('a Thayer a helyet nem idézi', ik, h)
            self.assertIn('a Thayer saját példahelye: Thayer 5', ik, h)

    def test_1kir_18_25_gerinc_i_egyezik_a_sorral(self):
        # ELLENOR_SZOTARI_GERINC 3. (7.5b): a gerinc ⓘ-je nem mondhatja „nem idézi”-nek a tartomány belsejében idézett
        # 1Kir 18:25-öt; ugyanazt az állítást mondja, mint a sor ⓘ-je
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        sorai = [r for r in elo_sorok if r['id'] == 'ISTENTISZT-001']
        a = LG.gerinc_adat()
        s = next(r for r in sorai if r['igehely'] == '1Kir 18:25')
        _cella, sor_i = LG.jelentes_cella(a, s)
        for strong in ('H7121', 'H8034'):
            bek, napl = LG.gerinc_blokk(a, 'BDB', strong, sorai)
            self.assertNotIn('1Kir 18:25', napl['nem_idezett'], strong)
            self.assertEqual(len(napl['tartomanyban']), 1, strong)
            t = napl['tartomanyban'][0]
            self.assertTrue(t.startswith('1Kir 18:25: '), t)
            self.assertIn(t[len('1Kir 18:25: '):], sor_i, strong)
            self.assertIn('az 1Kir 18:24–25 verstartomány belsejében (a BDB-ben: „1Kin 18:24-25”', '\n'.join(bek))

    def test_horgonnyal_osszecsukva_az_eles_lapon(self):
        # ELLENOR_SZOTARI_GERINC 4. (7.2a): a H8034 `-/5/-` szakasza `horgonnyal` határú és összecsukva áll; a jelölés
        # ott is kint van (nem csak a kibontott szakaszon)
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        sorai = [r for r in elo_sorok if r['id'] == 'ISTENTISZT-001']
        a = LG.gerinc_adat()
        szak = {s[0]: s for s in LG.bdb_gerinc_szakaszok(a, 'H8034')}
        self.assertEqual(szak['-/5/-'][4], 'horgonnyal')
        bek, _napl = LG.gerinc_blokk(a, 'BDB', 'H8034', sorai)
        osszecsukott = [b for b in bek if b.startswith('<details>') and '- `5` —' in b]
        self.assertEqual(len(osszecsukott), 1)
        sor5 = next(x for x in osszecsukott[0].split('\n') if x.startswith('- `5` —'))
        self.assertIn('horgonnyal illesztve, ellenőrzendő', sor5)
        self.assertIn('horgonnyal','\n'.join(bek))

    def test_tw_forrasmegjeloles(self):
        # DT383 (a) (ELLENOR_SZOTARI_GERINC 5.): ha a lap tW-azonosítót nevez meg, a tW-fájl a forráslistába kerül
        # (Irodalom, kolofon licenctábla); tW-szócikk nélkül nem
        ctx = {'fl': {}}
        sorok = LG._gerinc_tw('gorog', 3, ['G1941'], {}, ctx)
        self.assertTrue(any('tW: `kt/call-speakloudly`' in x for x in sorok))
        self.assertEqual(ctx['fl'].get(LG.TW_FAJL), {'tW_szocikkek'})
        ctx2 = {'fl': {}}
        LG._gerinc_tw('gorog', 3, ['G0000'], {}, ctx2)
        self.assertNotIn(LG.TW_FAJL, ctx2['fl'])

    def test_mounce_forrasmegjeloles(self):
        # F131.21 (ELLENOR_SZOTARI_GERINC_2 5.): a görög mutató a Mounce-ot megnevezi, ezért az MCGED a forráslistába
        # kerül (Irodalom, kolofon licenctábla és MOUNCE_MEGJELOLES); Mounce-szócikk nélkül nem
        ctx = {'fl': {}}
        sorok = LG._gerinc_ubs_mutato('gorog', 5, ['G1941'], {}, ctx)
        self.assertTrue(any('Mounce' in x for x in sorok))
        self.assertEqual(ctx['fl'].get(LG.MCGED_FAJL), {'MCGED'})
        ctx2 = {'fl': {}}
        LG._gerinc_ubs_mutato('gorog', 5, ['G0000'], {}, ctx2)
        self.assertNotIn(LG.MCGED_FAJL, ctx2['fl'])
        ctx3 = {'fl': {}}
        LG._gerinc_ubs_mutato('heber', 5, ['H7121'], {}, ctx3)
        self.assertNotIn(LG.MCGED_FAJL, ctx3['fl'])
        kol = LG.blokk_kolofon({'id': 'ISTENTISZT-001', 'statusz': 'x'}, [(LG.MCGED_FAJL, LG.LC('MCGED'), 'szocikkek')])
        self.assertIn(LG.MOUNCE_MEGJELOLES, kol)

    def test_tahot_forrasmegjeloles(self):
        # F131.27 (ELLENOR_SZOTARI_GERINC_3 2.): az 1Móz 4:26 és az 1Kir 18:24 ⓘ-je a TAHOT-ot forrásként nevezi meg,
        # ezért a TAHOT (CC BY 4.0, STEPBible) az előfordulás-blokk forráslistájában, az Irodalom „Adatforrások”
        # listájában és a kolofon licenctáblájában áll, a licencek.tsv kötelező megjelölésével; a nem gerinces lap
        # előfordulás-blokkja nem veszi fel (más lap nem változik)
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        _, motivumok = G.tsv_beolvas(G.MOTIVUMOK_TSV)
        mot = {r['id']: r for r in motivumok}
        sorrend = G.konyv_sorrend_betolt()
        sorai = [r for r in elo_sorok if r['id'] == 'ISTENTISZT-001']
        szov, parok = LG.blokk_elofordulasok(mot['ISTENTISZT-001'], sorai, sorrend, set())
        self.assertIn(LG.TAHOT_KIVONAT_FAJL, szov)
        self.assertIn((LG.TAHOT_KIVONAT_FAJL, LG.LC('TAHOT')), parok)
        self.assertEqual(LG.LC('TAHOT'), 'CC BY 4.0')
        mas = next(i for i in sorted(mot) if i not in LG.SZOTARI_GERINC_MOTIVUMOK
                   and any(r['id'] == i for r in elo_sorok))
        _szov2, parok2 = LG.blokk_elofordulasok(mot[mas], [r for r in elo_sorok if r['id'] == mas], sorrend, set())
        self.assertNotIn(LG.TAHOT_KIVONAT_FAJL, [f for f, _l in parok2])
        lista = [(LG.TAHOT_KIVONAT_FAJL, LG.LC('TAHOT'), 'elofordulasok')]
        kol = LG.blokk_kolofon({'id': 'ISTENTISZT-001', 'statusz': 'x'}, lista)
        self.assertIn('| `TAHOT_kivonat.tsv` | `konkordancia/TAHOT_kivonat.tsv` | CC BY 4.0 | elofordulasok |', kol)
        megj = LG.licenc_sor('TAHOT')['kotelezo_megjeloles']
        self.assertIn('www.STEPBible.org', megj)
        self.assertIn('*%s*' % megj, kol)
        idez = LG.blokk_idezes({'id': 'ISTENTISZT-001', 'statusz': 'x'}, lista)
        adatforras = idez.split('**Adatforrások:**', 1)[1]
        self.assertIn('- `konkordancia/TAHOT_kivonat.tsv` (CC BY 4.0)', adatforras)

    def test_tw_modositas_mondat_a_felhasznalast_koveti(self):
        # F131.17 (ELLENOR_SZOTARI_GERINC_2 1.): a gerinces lap a tW-ből csak azonosítót nevez meg, ezért a
        # kolofon nem mondhatja, hogy a szócikkek szövegét idézőblokkban közli; szövegközlésnél a régi mondat marad
        self.assertIn('szövegét nem közli', LG.kotelezo_megjeloles('tW_szocikkek', tw_szoveg_kozolve=False))
        self.assertNotIn('idézőblokkba', LG.kotelezo_megjeloles('tW_szocikkek', tw_szoveg_kozolve=False))
        self.assertIn('idézőblokkba', LG.kotelezo_megjeloles('tW_szocikkek'))
        # a jel a szövegközlő blokkból jön, a gerinc-mutatóban nem áll
        r = {'strongok': ['G1941'], 'tw_id': 'kt/x', 'cim': 'x', 'szoveg': 'a\\nb'}
        self.assertIn(LG.TW_SZOVEG_JEL, LG._tw_cikk_blokk(r, {'G1941'}))
        ctx = {'fl': {}}
        self.assertFalse(any(LG.TW_SZOVEG_JEL in x for x in LG._gerinc_tw('gorog', 3, ['G1941'], {}, ctx)))
        kol = LG.blokk_kolofon({'id': 'ISTENTISZT-001', 'statusz': 'x'},[(LG.TW_FAJL, 'tW_szocikkek', 'szocikkek')], tw_szoveg_kozolve=False)
        self.assertIn('szövegét nem közli', kol)
        self.assertNotIn('idézőblokkba', kol)

    def test_2moz_33_19(self):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == '2Móz 33:19')
        cella, _ik = LG.jelentes_cella(LG.gerinc_adat(), s)
        self.assertIn('Qal 3.b', cella)

    def test_szabaly17(self):
        self.assertEqual(E.szabaly17_szakasz_cimke(E.ALAPERTELMEZETT_ADAT).verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main()
