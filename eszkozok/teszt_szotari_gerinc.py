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
import re
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


def cimke_sor(szotar, strong, szakasz, ljsz='', cimke='', bdb_id=''):
    return {'szotar': szotar, 'strong': strong, 'bdb_id': bdb_id, 'szakasz': szakasz, 'lexikon_jelentes_szam': ljsz,
            'cimke_hu': cimke, 'hu_kezdet': '', 'hu_hossz': '', 'forditas_hash': '', 'proveniencia': 'scope=manual',
            'megjegyzes': ''}


def vj_sor(strong, sorszam, vers, utvonal, szurt='0', okkod='', mt_vers=None):
    return {'strong': strong, 'sorszam': str(sorszam), 'karoli_vers': vers, 'mt_vers': vers if mt_vers is None else mt_vers,
            'utvonal': utvonal, 'szurt': szurt, 'okkod': okkod}


def adat(cimkek=(), vj=(), bdb_sz=None, bdb_hu=None):
    a = {'cimke': {}, 'bdb_sz': bdb_sz or {}, 'bdb_hu': bdb_hu or {}, 'bdb_vj': {}, 'th_sz': {}, 'th_vj': {},
         'glossza': {}}
    for c in cimkek:
        a['cimke'][LG.cimke_kulcs(c)] = c
    a['bdb_vj_feloldott'] = {}
    for r in vj:
        # a `gerinc_adat` két indexe: a hivatkozásszámé (DT-F104d: szűretlen, feloldott) és a versé (szűretlen, Károli-verssel)
        if r['szurt'] != '1' and r['mt_vers']:
            a['bdb_vj_feloldott'].setdefault(r['strong'], []).append(r)
        if r['szurt'] != '1' and r['karoli_vers']:
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
        self.assertTrue(LG.gerinc_aktiv('HAMART-001'))  # a HAMART-001 migrált (F123.HAMART3.5, 51949f07): `aktiv`, nem kivétel
        for mid in ('KIRALY-001', 'TEREMT-001', None):
            self.assertFalse(LG.gerinc_aktiv(mid))

    def test_kivetellista_adatbol(self):
        # F148 (DT437): a kivétellista az `adat/funkcio_kapcsolok.tsv` `kivetel` sora, és az `ellenoriz.py`
        # ugyanazt a függvényt hívja, mint a generátor (egyetlen hely)
        import szerep_karoli as SZK
        self.assertEqual(LG.GERINC_KIVETEL_MOTIVUMOK, SZK.kapcsolo_kivetelek('SZOTARI_GERINC'))
        self.assertNotIn('ISTENTISZT-001', LG.GERINC_KIVETEL_MOTIVUMOK)
        self.assertNotIn('ALVIL-001', LG.GERINC_KIVETEL_MOTIVUMOK)

    def test_uj_motivum_kapcsolobejegyzes_nelkul(self):
        # F148 (a), elfogadás 2.: a kivétellistán kívüli új motívumon a gerinc kapcsolóbejegyzés nélkül megjelenik
        # (az előfordulás-tábla két oszlopa); kivétellistán nem
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        _, motivumok = G.tsv_beolvas(G.MOTIVUMOK_TSV)
        import szerep_karoli as SZK
        self.assertNotIn('UJTESZT-001', {r['id'] for r in SZK.funkcio_kapcsolok()})
        m = dict(next(r for r in motivumok if r['id'] == 'ISTENTISZT-001'), id='UJTESZT-001')
        sorai = [dict(r, id='UJTESZT-001') for r in elo_sorok if r['id'] == 'ISTENTISZT-001']
        sorrend = G.konyv_sorrend_betolt()
        self.assertTrue(LG.gerinc_aktiv('UJTESZT-001'))
        szov, _ = LG.blokk_elofordulasok(m, sorai, sorrend, set())
        self.assertIn('| Jelentés (a szó) | Funkció (a motívumban) |', szov)
        regi = LG.GERINC_KIVETEL_MOTIVUMOK
        try:
            LG.GERINC_KIVETEL_MOTIVUMOK = regi | {'UJTESZT-001'}
            szov2, _ = LG.blokk_elofordulasok(m, sorai, sorrend, set())
        finally:
            LG.GERINC_KIVETEL_MOTIVUMOK = regi
        self.assertNotIn('Jelentés (a szó)', szov2)


class Ellenoriz17(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

        def ir(nev, fej, sorok):
            with open(os.path.join(self.d, nev), 'w', encoding='utf-8') as f:
                f.write('\t'.join(fej) + '\n' + ''.join('\t'.join(s) + '\n' for s in sorok))
        self.ir = ir
        ir('bdb_szakaszok.tsv', ['strong', 'bdb_id', 'utvonal'], [['H7121', 'BDB7550', 'Qal/2/c'], ['H8034', 'BDB8776', '-/3/-'],
                                                               ['H8034', 'BDB9963', 'fej']])
        ir('thayer_szakaszok.tsv', ['strong', 'utvonal'], [['G9999', 'cim'], ['G9999', '-/1/-'], ['G9999', '-/2/-']])
        ir('lexikon_hivatkozasok.tsv', ['szotar', 'strong', 'jelentes_szam'], [['BDB', 'H7121', '2.c'],
                                                                               ['TBESG', 'G9999', '2']])
        ir('tiltott_fordulatok.tsv', ['magyar_alak', 'minta'],
           [['nevet tenni valakire', r'\bnevet\s+(?:tenni|tesz\w*|tett\w*)\s+(?:valaki\w*|rá\b)']])

    def tearDown(self):
        shutil.rmtree(self.d)

    def cimke(self, sorok):
        self.ir('szotar_szakasz_cimke.tsv', ['szotar', 'strong', 'bdb_id', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu',
                                             'proveniencia', 'megjegyzes'], sorok)
        return E.szakasz_cimke_hibak(self.d)

    def test_rendben(self):
        h = self.cimke([['BDB', 'H7121', 'BDB7550', 'Qal/2/c', '2.c', 'segítségül hívni', 'p', ''],
                        ['BDB', 'H8034', 'BDB8776', '-/3', '', 'név', 'p', ''],
                        ['TBESG', 'G9999', '', '2', '2', 'x', 'p', ''],
                        ['Thayer', 'G9999', '', '-/1/-', '', 'elnevezni', 'p', '']])
        self.assertEqual(h, [])

    def test_szocikk_kulcs(self):
        # F123.BDBGER: a BDB-sor kulcsa szócikk + szakasz; üres vagy más szócikk bdb_id-je hiba, nem BDB-sorban tilos
        h = self.cimke([['BDB', 'H7121', '', 'Qal/2/c', '', 'x', 'p', ''],
                        ['BDB', 'H8034', 'BDB9963', '-/3', '', 'név', 'p', ''],
                        ['Thayer', 'G9999', 'BDB1', '-/1/-', '', 'elnevezni', 'p', '']])
        szov = '\n'.join(h)
        self.assertIn('üres bdb_id', szov)
        self.assertIn('nincs a bdb_szakaszok.tsv-ben (ebben a szócikkben)', szov)
        self.assertIn('a bdb_id csak BDB-sorban állhat', szov)

    def test_hibak(self):
        h = self.cimke([['BDB', 'H7121', 'BDB7550', 'Qal/9/z', '', '', 'p', ''],
                        ['BDB', 'H7121', 'BDB7550', 'Qal/2/c', '3', 'nem invokáció', 'p', ''],
                        ['TBESG', 'G9999', '', '7', '', '', '', ''],
                        ['Thayer', 'G9999', '', '-/9/-', '', 'nevet tenni valakire', 'p', '']])
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
        self.assertEqual(h7121.count('`0065620'), 0)                       # 2026-11-03: a 15 jegyű kód nem látszik
        self.assertEqual(h7121.count('[ⓘ](/szo/H7121)'), 2)               # a két DBH-egység külön glosszával
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
        self.assertEqual(szak[('BDB8776', '-/5/-')][4], 'horgonnyal')
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
        mas = next(i for i in sorted(mot) if not LG.gerinc_aktiv(i)
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


class Kulcsszavak(unittest.TestCase):
    """A 2. szakasz eleji kulcsszó-blokk (a felhasználó: „2. Szótári háttér előtt kellene egy motivum kulcsszavai blokk”)."""

    def _sorai(self, mid):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        return [r for r in elo_sorok if r['id'] == mid]

    def test_istentiszt(self):
        szov = LG.kulcsszavak_blokk('ISTENTISZT-001', self._sorai('ISTENTISZT-001'), {})
        self.assertTrue(szov.startswith(LG.KULCSSZAVAK_CIM))
        self.assertIn('| Héber/görög szavak | Szavak (kiejtéssel) | Jelentés | Károli-kulcsszavak |', szov)
        self.assertNotIn('Gerinc', szov.split('\n\n', 3)[-1])   # F152 A.3: az olvasói táblában nincs „gerinc”
        self.assertIn('| H7121 + H8034 | ', szov)
        self.assertIn(' (kárá) + ', szov)
        self.assertIn(' (sém) | ', szov)
        self.assertIn('„segítségül”', szov)
        self.assertIn(LG.OLVASOI_CIMKE, szov)
        self.assertNotIn('Mit mutat ez a rész', szov)

    def test_kapcsolo_nelkul_ures(self):
        self.assertEqual(LG.kulcsszavak_blokk('HAMART-001', self._sorai('HAMART-001'), {}), '')


class RagozottKiejtes(unittest.TestCase):
    """A Kulcsszó cella: héberül (DT-F131y, 2026-10-30) a teljes ragozott szó saját gépi kiejtése, jelölve; pontozatlan
    alaknál a szótári alak kiejtése, „szótári alak:” jelöléssel."""

    def test_heber_jelolt(self):
        self.assertEqual(LG.ragozott_kiejtessel('X', 'kárá', 'TAHOT_LEMMA'), 'X (szótári alak: kárá)')
        self.assertEqual(LG.ragozott_kiejtessel('X', 'likró', 'TAHOT'), 'X (likró)')

    def test_gorog_ragozott(self):
        self.assertEqual(LG.ragozott_kiejtessel('Y', 'epikaleszétai', 'TAGNT'), 'Y (epikaleszétai)')

    def test_kiejtes_nelkul(self):
        self.assertEqual(LG.ragozott_kiejtessel('Z', '', 'TAHOT'), 'Z')

    def test_1moz_4_26_cella(self):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        s = next(r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] == '1Móz 4:26')
        cella = LG.kulcsszo_cella(s)
        self.assertIn('(likró)', cella)   # a teljes szó: לִ + קְרֹא
        self.assertNotIn('gépi', cella)   # DT430 kiegészítés: jelölés nélkül
        self.assertIn('(besém)', cella)   # בְּ + שֵׁם


class BdbRovidites(unittest.TestCase):
    """A BDB egybetűs rövidítései jelölve (a felhasználó: „nem lehetne jelölni a szövegben …, hogy a szó rövidités?”)."""

    def test_jahve(self):
        u = LG.bdb_rovidites_jelol('hívni ׳י nevével', 'H7121')
        self.assertIn('<abbr class="rovidites" title="%s">י׳</abbr>' % LG.BDB_JAHVE_CIM, u)

    def test_cimszo(self):
        u = LG.bdb_rovidites_jelol('perfectum ׳ק 1Móz 11:9', 'H7121')
        self.assertIn('title="a címszó: ', u)
        self.assertIn('ק׳</abbr>', u)

    def test_mas_betu_altalanos(self):
        u = LG.bdb_rovidites_jelol('׳א x', 'H7121')
        self.assertIn(LG.BDB_ROVIDITES_ALTALANOS, u)

    def test_tobbbetus_szo_valtozatlan(self):
        sz = '׳בשם x'
        self.assertEqual(LG.bdb_rovidites_jelol(sz, 'H7121'), sz)


class Olvasoi1314(unittest.TestCase):
    """A 13. és a 14. szerep olvasói szövege: lelet számokkal, utána következtetés (a felhasználó: „mindig vanjuk le a
    következtetést a találtakból . a magyarázó szöveg az adatokból induljon.”)."""

    def _sorai(self, mid):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        return [r for r in elo_sorok if r['id'] == mid]

    def test_13(self):
        m = LG.olvasoi_13(self._sorai('ISTENTISZT-001'))
        self.assertTrue(m.startswith('A motívum 33 igehelyén a Károli 17 különböző magyar szót használ.'))
        self.assertIn('**Következtetés:** a Károli a motívumot szinte mindenütt (a helyek 91%-án)', m)

    def test_13_kuszob(self):
        self.assertIn('változó szavakkal', LG.olvasoi_13(self._sorai('ALVIL-001')))

    def test_14(self):
        m = LG.olvasoi_14(self._sorai('ISTENTISZT-001'))
        self.assertIn('33 helye közül 4 helyen', m)
        self.assertIn('héberül a kárá és a sém, görögül az epikaleó', m)
        self.assertNotIn('gerinc', m)
        self.assertIn('1Kir 8:52 — „mikor téged segítségül hívnak”', m)
        self.assertIn('a 46 találat 37%-a nem a motívumhoz tartozik', m)

    def test_ures(self):
        self.assertIsNone(LG.olvasoi_13([]))
        self.assertIsNone(LG.olvasoi_14([]))

class KaroliHelyette(unittest.TestCase):
    """A 13. és a 14. szerep: mit ír a Károli a kulcsszó helyett (a felhasználó: „irjuk le azt is károli a motivom
    kulcsszavai helyet jellemzően mit forditott”)."""

    def _sorai(self, mid):
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        return [r for r in elo_sorok if r['id'] == mid]

    def test_rejtett_helyettesitok(self):
        sorai = self._sorai('ISTENTISZT-001')
        kulcs = {k: v for k, v in LG.SZK.kulcsszavak(sorai).items() if v}
        rejt = LG.SZK.rejtett_parhuzamok(sorai, kulcs=kulcs)
        hely = dict(LG.SZK.helyettesitok(sorai, [r[0] for r in rejt], [], kulcs))
        self.assertEqual(sorted(hely['kiált']), ['2Móz 33:19', '2Móz 34:5'])
        self.assertNotIn('név', hely)

    def test_13_es_14_mondat(self):
        sorai = self._sorai('ISTENTISZT-001')
        self.assertIn('Ahol nem a „hív” áll (3 helyen), ott a Károli jellemzően ezt írja helyette: „kiált” 2',
                      LG.olvasoi_13(sorai))
        m = LG.olvasoi_14(sorai)
        self.assertIn('helyett jellemzően ezt írja: „kiált” (2 hely)', m)
        self.assertIn('hacsak nem keres ezekre is: „kiált”', m)


def _szocikk_adat():
    """Szintetikus kétszócikkű Strong (F123.BDBGER): mindkét szócikknek `-/1/-` szakasza van; a második szócikk feje
    jelölő nélküli, magyar szöveg nélküli sor, a szövege a 2.32 szerint az első szócikk `1`-ében áll."""
    def sor(n, b, ut, szoveg):
        return {'strong': 'H9999', 'sorszam': str(n), 'bdb_id': b, 'utvonal': ut, 'jel': '', 'szoveg': szoveg}
    bdb_sz = {'H9999': [sor(1, 'BDB1', 'cim', 'H9999. ab'),
                        sor(2, 'BDB1', 'fej', 'I. אָב noun father, the first head'),
                        sor(3, 'BDB1', '-/1/-', 'first meaning of the word Gen 1:1'),
                        sor(4, 'BDB2', 'fej', 'II. אָב noun the second head word'),
                        sor(5, 'BDB2', '-/1/-', 'second meaning of the word Gen 2:2')]}
    bdb_hu = {('H9999', '2'): {'szoveg_hu': 'I. אָב főnév apa', 'kategoria': 'jelolo_nelkul'},
              ('H9999', '3'): {'szoveg_hu': '1 első jelentés 1Móz 1:1', 'kategoria': 'illeszkedik'},
              ('H9999', '4'): {'szoveg_hu': '', 'kategoria': 'jelolo_nelkul'},
              ('H9999', '5'): {'szoveg_hu': '1 második jelentés 1Móz 2:2', 'kategoria': 'illeszkedik'}}
    en = ('H9999. ab I. אָב noun father, the first head 1 first meaning of the word Gen 1:1 '
          'II. אָב noun the second head word 1 second meaning of the word Gen 2:2')
    a = adat(bdb_sz=bdb_sz, bdb_hu=bdb_hu)
    a['bdb_en'] = {'H9999': en}
    r = dict(vj_sor('H9999', 2, '1Móz 2:2', '-/1'), poz=str(LG._lapit(en).index('Gen 2:2')), okkod='', nyers='Gen 2:2')
    a['bdb_vj'][('H9999', '1Móz 2:2')] = [r]
    return a, r


class SzocikkKulcs(unittest.TestCase):
    """F123.BDBGER (DT-F123ga): a szakasz kulcsa (bdb_id, útvonal); különböző szócikkek szakaszai nem vonódnak össze."""

    def test_szocikkenkent(self):
        a, _r = _szocikk_adat()
        szocikkek, elnyelt = LG.bdb_gerinc_szocikkek(a, 'H9999')
        self.assertEqual([s['bdb_id'] for s in szocikkek], ['BDB1', 'BDB2'])
        self.assertEqual([s[0] for s in szocikkek[0]['szakaszok']], [('BDB1', '-/1/-')])
        self.assertEqual([s[0] for s in szocikkek[1]['szakaszok']], [('BDB2', '-/1/-')])
        self.assertEqual(szocikkek[1]['szakaszok'][0][2], '1 második jelentés 1Móz 2:2')
        self.assertEqual(elnyelt, {('BDB2', 'fej'): ('BDB1', '-/1/-')})

    def test_peldahely_szocikke_a_helybol(self):
        # az útvonal (`-/1`) mindkét szócikkben áll: a hely (`poz`) dönt
        a, r = _szocikk_adat()
        self.assertEqual(LG.bdb_vers_szocikk(a, 'H9999', r), ('BDB2', ''))
        self.assertEqual(LG.szakasz_kulcs_jel(a, 'BDB', 'H9999', ('BDB2', '-/1/-')), 'BDB2 1')
        # hely nélkül nem választ
        b, ok = LG.bdb_vers_szocikk(dict(a, bdb_en={}, _bdb_kezdet={}, _bdb_poz_ok={}), 'H9999', r)
        self.assertIsNone(b)
        self.assertIn('BDB1, BDB2', ok)

    def test_gerinc_blokk(self):
        a, _r = _szocikk_adat()
        bek, napl = LG.gerinc_blokk(a, 'BDB', 'H9999', [elo('1Móz 2:2', '', strong='H9999', entry='')])
        szov = '\n'.join(bek)
        self.assertIn('**BDB1 · I. אָב**', szov)
        self.assertIn('**BDB2 · II. אָב**', szov)
        self.assertLess(szov.index('**BDB1'), szov.index('**BDB2'))
        kibontva = [b for b in bek if b.startswith('- **`')]
        self.assertEqual(len(kibontva), 1)
        self.assertIn('második jelentés', kibontva[0])
        self.assertNotIn('első jelentés', kibontva[0])
        self.assertIn('**1Móz 2:2**', kibontva[0])
        self.assertEqual(napl['nem_talalt'], [])
        # az elnyelt fej: a lap kimondja, hol áll a szövege; az elnyelő szakasz jelölve
        self.assertIn('A magyar szöveg a BDB1 szócikk 1. szakaszának fordításában áll', szov)
        self.assertIn('BDB2 fej → BDB1 -/1/-', szov)
        self.assertIn('a BDB2 szócikk fejét is tartalmazza', szov)

    def test_h2416_valodi(self):
        a = LG.gerinc_adat()
        szocikkek, _e = LG.bdb_gerinc_szocikkek(a, 'H2416')
        self.assertEqual([s['bdb_id'] for s in szocikkek],
                         ['BDB2716', 'BDB2717', 'BDB2718', 'BDB2719', 'BDB2721', 'BDB9522', 'BDB9523'])
        egyes = sorted(k for s in szocikkek for k, *_x in s['szakaszok'] if k[1] == '-/1/-')
        self.assertEqual(egyes, [('BDB2718', '-/1/-'), ('BDB2721', '-/1/-'), ('BDB9522', '-/1/-')])
        # az 1Móz 2:7 a חַיִּים (BDB2721) `1`-ében: a 2.29 `-/1` útvonala három szócikkben áll, a hely dönt
        r = next(x for x in a['bdb_vj'][('H2416', '1Móz 2:7')] if x['utvonal'] == '-/1')
        self.assertEqual(LG.bdb_vers_szocikk(a, 'H2416', r)[0], 'BDB2721')


class Szabaly27(unittest.TestCase):
    """F123.BDBGER (DT-F123gb): a 27. szabály bukik, ha a lap BDB-gerince több szócikkű Strongnál nem szócikkenként áll."""

    def setUp(self):
        self.gy = tempfile.mkdtemp(prefix='F123_bdbger_')
        os.makedirs(os.path.join(self.gy, 'adat'))
        os.makedirs(os.path.join(self.gy, 'lexikon'))

        def ir(nev, fej, sorok):
            with open(os.path.join(self.gy, 'adat', nev), 'w', encoding='utf-8') as f:
                f.write('\t'.join(fej) + '\n' + ''.join('\t'.join(s) + '\n' for s in sorok))
        ir('bdb_szakaszok.tsv', ['strong', 'bdb_id', 'sorszam', 'utvonal'],
           [['H9999', 'BDB1', '1', 'cim'], ['H9999', 'BDB1', '2', 'fej'], ['H9999', 'BDB1', '3', '-/1/-'],
            ['H9999', 'BDB2', '4', 'fej'], ['H9999', 'BDB2', '5', '-/1/-'], ['H0001', 'BDB9', '1', 'fej']])
        ir('bdb_szakasz_hu.tsv', ['strong', 'sorszam', 'kategoria', 'szoveg_hu'],
           [['H9999', '2', 'jelolo_nelkul', 'fej'], ['H9999', '3', 'illeszkedik', '1 első'],
            ['H9999', '4', 'jelolo_nelkul', ''], ['H9999', '5', 'illeszkedik', '1 második']])

    def tearDown(self):
        shutil.rmtree(self.gy)

    def lap(self, torzs):
        with open(os.path.join(self.gy, 'lexikon', 'X-001_TUDOMANYOS.md'), 'w', encoding='utf-8') as f:
            f.write('# X\n\n##### H9999 — אָב (av) · BDB\n\n%s\n\n##### H0001 — x · BDB\n\n- `1` — y\n\n## 3. Vége\n' % torzs)
        return E.gerinc_szocikk_hibak(os.path.join(self.gy, 'adat'))

    def test_osszevont_lap_bukik(self):
        hibak, jelentes = self.lap('**A szócikk feje (nyelvi háttér).** fej\n\n- **`1`**\n\n  > első második')
        self.assertEqual(len(hibak), 1)
        self.assertIn('H9999', hibak[0])
        self.assertIn('nem szócikkenként', hibak[0])
        self.assertEqual(len(jelentes), 1)
        self.assertIn('BDB2 fej sor magyar szövege a BDB1 -/1/- sorában áll', jelentes[0])

    def test_szocikkenkenti_lap_rendben(self):
        hibak, _j = self.lap('**BDB1 · I. אָב** *(1/2)*\n\n- **`1`**\n\n  > első\n\n**BDB2 · II. אָב** *(2/2)*\n\n- `1` — második')
        self.assertEqual(hibak, [])
        hibak, _j = self.lap('**BDB2 · II. אָב**\n\n**BDB1 · I. אָב**')
        self.assertEqual(len(hibak), 1)  # a sorrend is számít


class KetreteguBdbKartya(unittest.TestCase):
    """F104 (DT-F104b): az új szerkezetű lap 4.2-es BDB-kártyája két rétegű — olvasói (a jelentések rendje glosszával, a
    motívum helyeinek jelentése, DT178 szerint tippelés nélkül) és a csukott kutatói apparátus (a teljes szöveg), egységes
    jelölővel; a régi út (ctx nélkül) változatlan."""

    def _adat(self):
        sz = {'H8034': [
            {'strong': 'H8034', 'sorszam': '1', 'utvonal': 'cim', 'jel': '', 'szoveg': ''},
            {'strong': 'H8034', 'sorszam': '2', 'utvonal': 'fej', 'jel': '', 'szoveg': 'name'},
            {'strong': 'H8034', 'sorszam': '3', 'utvonal': '-/4/-', 'jel': '4', 'szoveg': 'of false gods'},
            {'strong': 'H8034', 'sorszam': '4', 'utvonal': '-/5/-', 'jel': '5', 'szoveg': 'memorial Isa 55:13'},
        ]}
        hu = {('H8034', '2'): {'szoveg_hu': 'H8034. név', 'kategoria': 'jelolo_nelkul'},
              ('H8034', '3'): {'szoveg_hu': '4 hamis istenekről (J) 1Kir 18:24', 'kategoria': 'illeszkedik'},
              ('H8034', '4'): {'szoveg_hu': '5 = emlékjel Ézs 55:13', 'kategoria': 'illeszkedik'}}
        # a csukott cím hivatkozásszáma a táblából (DT-F104d): a -/4 egy feloldott sora; a szűrt sor nem számít
        return adat([], [vj_sor('H8034', 300, 'Ézs 55:13', '-/5'), vj_sor('H8034', 290, '1Kir 18:24', '-/4'),
                         vj_sor('H8034', 291, '', '-/4', szurt='1', okkod='nem_bibliai', mt_vers='')], sz, hu)

    def _blokk(self, ctx, sorok=None):
        sorok = sorok or [elo('Ézs 55:13', '', strong='H8034', entry=''), elo('Ézs 1:1', '', strong='H8034', entry='')]
        return '\n\n'.join(LG.gerinc_blokk(self._adat(), 'BDB', 'H8034', sorok, ctx)[0])

    def test_ket_reteg_egyseges_jelolovel(self):
        szov = self._blokk({'bdb_kartya': True, 'fl': {}})
        kezd = szov.index(LG.APPARATUS_KEZDET % 'H8034')
        vege = szov.index(LG.APPARATUS_VEGE % 'H8034')
        self.assertLess(kezd, vege)
        self.assertEqual(len(LG.APPARATUS_RX.findall(szov)), 2)
        olvasoi, app = szov[:kezd], szov[kezd:vege]
        self.assertIn('<details>\n<summary>%s</summary>' % LG.APPARATUS_CIM, app)
        # olvasói réteg: a jelentések rendje (a hordozó félkövér), a hely jelentése, a nem idézett hely kimondva
        self.assertIn(r'- 4\. hamis istenekről', olvasoi)   # F182.23: a sor eleji jel escape-elve
        self.assertIn('- **5.** emlékjel', olvasoi)
        self.assertIn('**A motívum helyein:** Ézs 55:13 → 5. emlékjel.', olvasoi)
        self.assertIn('A szótár ezt a helyet nem idézi: Ézs 1:1.', olvasoi)
        self.assertNotIn('(J)', olvasoi)
        # kutatói réteg: semmi nem vész el — a teljes magyar szöveg, a rövidítéssel, a nem idézett hely kutatói alakja
        self.assertIn('(J)', app)
        self.assertIn('= emlékjel **Ézs 55:13**', app)
        self.assertIn('a szótár nem idézi: Ézs 1:1', app)
        # a csukott cím glosszával (F10 (2)), nem „4 (1 szakasz)”
        self.assertIn('<summary>4. — hamis istenekről (1 hivatkozás)</summary>', app)
        self.assertNotIn('(1 szakasz)', szov)

    def test_bevezeto_egyszer(self):
        ctx = {'bdb_kartya': True, 'fl': {}}
        elso, masodik = self._blokk(ctx), self._blokk(ctx)
        self.assertEqual(elso.count('Szótári tagolás (DT272)'), 1)
        self.assertLess(elso.index('Szótári tagolás'), elso.index('##### H8034'))
        self.assertNotIn('Szótári tagolás', masodik)

    def test_regi_ut_valtozatlan(self):
        szov = self._blokk(None)
        self.assertNotIn('APPARATUS-', szov)
        self.assertIn('Szótári gerinc (DT272)', szov)
        self.assertIn('<summary>4 (1 szakasz)</summary>', szov)

    def test_kapcsolo_csak_a_hamart(self):
        # F182 (2. fázis, F25): az F33 után a HAMART-001 bekapcsolva; a régi lapok a saját teljes folyamatukban
        self.assertEqual(LG.KETRETEGU_BDB_KARTYA, frozenset({'HAMART-001'}))
        self.assertTrue(LG.bdb_kartya_aktiv('HAMART-001'))
        self.assertFalse(LG.bdb_kartya_aktiv('ANTROP-001'))

    def test_csak_alakot_kozlo_szakasz(self):
        sz = {'H0056': [
            {'strong': 'H0056', 'sorszam': '1', 'utvonal': 'fej', 'jel': '', 'szoveg': 'mourn'},
            {'strong': 'H0056', 'sorszam': '2', 'utvonal': "Hithpa'el/-/-", 'jel': "Hithpa'el", 'szoveg': 'Pf.'},
            {'strong': 'H0056', 'sorszam': '3', 'utvonal': "Niph'al/-/-", 'jel': "Niph'al", 'szoveg': 'Pt.'},
        ]}
        hu = {('H0056', '1'): {'szoveg_hu': 'gyászol', 'kategoria': 'illeszkedik'},
              ('H0056', '2'): {'szoveg_hu': "Hithpael — perfectum הִתְאַבֵּל 1Sám 15:35", 'kategoria': 'illeszkedik'},
              ('H0056', '3'): {'szoveg_hu': "Niphal participium נֵאָרִים átkozott Mal 3:9.", 'kategoria': 'illeszkedik'}}
        # a „(N hely)” a táblából (DT-F104d): egy feloldott Hithpa'el sor
        a = adat([], [vj_sor('H0056', 10, '1Sám 15:35', "Hithpa'el/-")], sz, hu)
        szov = '\n\n'.join(LG.gerinc_blokk(a, 'BDB', 'H0056', [elo('Hós 4:3', '', strong='H0056', entry='')],
                                             {'bdb_kartya': True, 'fl': {}})[0])
        self.assertIn("- Hithpa'el — a szótár csak alakot közöl (1 hely)", szov)
        self.assertIn("- Niph'al — átkozott", szov)
        self.assertNotIn('külön meghatározás nélkül', szov)

    def test_hivatkozasszam_a_tablabol_nem_a_szovegbol(self):
        # DT-F104d (ELLENOR_F104 1.): a magyar szöveg két helyet ír, a tábla szerint a szakasznak nincs feloldott sora —
        # a szám a tábláé, ezért nincs „(N hely)”
        sz = {'H0056': [
            {'strong': 'H0056', 'sorszam': '2', 'utvonal': "Hithpa'el/-/-", 'jel': "Hithpa'el", 'szoveg': 'Pf.'}]}
        hu = {('H0056', '2'): {'szoveg_hu': "Hithpael — perfectum הִתְאַבֵּל 1Sám 15:35, 16:1", 'kategoria': 'illeszkedik'}}
        a = adat([], [vj_sor('H0056', 10, '', "Hithpa'el/-", szurt='1', okkod='sigla_tapadt', mt_vers='')], sz, hu)
        szov = '\n\n'.join(LG.gerinc_blokk(a, 'BDB', 'H0056', [elo('Hós 4:3', '', strong='H0056', entry='')],
                                             {'bdb_kartya': True, 'fl': {}})[0])
        olvasoi = szov.split(LG.APPARATUS_KEZDET % 'H0056')[0]
        self.assertIn("- Hithpa'el — a szótár csak alakot közöl\n", olvasoi + '\n')
        self.assertNotIn('hely)', olvasoi)

    def test_bizonytalan_okkod_gyenge_szint(self):
        # DT-F104e (ELLENOR_F104 2.): a csak bizonytalan okkódú sorral idézett pont gyenge („vonatkozhat”, az okkal), nem az
        # erőssel azonos alakban; ahol a helynek és a pontnak erős sora is van, az erős marad
        a = self._adat()
        for r in (vj_sor('H8034', 310, 'Ézs 1:1', '-/4', okkod='forras_hiba'),
                  vj_sor('H8034', 311, 'Ézs 55:13', '-/5', okkod='forras_hiba')):
            a['bdb_vj'].setdefault(('H8034', r['karoli_vers']), []).append(r)
            a['bdb_vj_feloldott']['H8034'].append(r)
        szov = '\n\n'.join(LG.gerinc_blokk(a, 'BDB', 'H8034', [elo('Ézs 55:13', '', strong='H8034', entry=''),
                                                                elo('Ézs 1:1', '', strong='H8034', entry='')],
                                             {'bdb_kartya': True, 'fl': {}})[0])
        olvasoi = szov.split(LG.APPARATUS_KEZDET % 'H8034')[0]
        self.assertIn('**A motívum helyein:** Ézs 1:1 → 4. hamis istenekről *(vonatkozhat; a hivatkozás bizonytalan: a BDB '
                      'nyomtatott igehelye hibás)* · Ézs 55:13 → 5. emlékjel.', olvasoi)
        # a bizonytalansági szabály egy helyen (`eszkozok/bdb_vj_szabaly.py`): a szerver blokkja csak rámutat
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'olvaso_szerver', 'blokkok.py'), encoding='utf-8') as f:
            blokkok = f.read()
        self.assertIn('_vj_bizonytalan = bdb_vj_szabaly.vj_bizonytalan', blokkok)
        self.assertNotIn("'forras_hiba':", blokkok)
        self.assertEqual(LG.VJ.vj_bizonytalan({'okkod': 'forras_hiba,karoli_tahot'}),
                         ['a BDB nyomtatott igehelye hibás'])

    def test_bizonytalan_okkod_valodi_adat(self):
        # a táblában a H1802 2Móz 2:6 sora `forras_hiba` okkódú (Qal): a 4.2-ben gyenge szinten áll
        a = LG.gerinc_adat()
        szov = '\n\n'.join(LG.gerinc_blokk(a, 'BDB', 'H1802', [elo('2Móz 2:6', '', strong='H1802', entry='')],
                                             {'bdb_kartya': True, 'fl': {}})[0])
        sor = next(s for s in szov.split('\n\n') if s.startswith('**A motívum helyein:**'))
        self.assertRegex(sor, r'2Móz 2:6 → Qal[^·]*\*\(vonatkozhat; a hivatkozás bizonytalan: a BDB nyomtatott igehelye hibás\)\*')

    def test_h7843_valodi_adat(self):
        # ELLENOR_F104 1.: a H7843 Hiph'il magyar bontása az „1 singular”-t pontnak vette (a szövegben 1 hely maradt); a tábla
        # 13 feloldott `Hiph'il/-` sort tartalmaz, a Pi'el 5-öt
        a = LG.gerinc_adat()
        szam = {k[1]: n for k, n in LG.bdb_hivatkozas_szam(a, 'H7843').items()}
        self.assertEqual(szam.get("Hiph'il/-/-"), 13)
        self.assertEqual(szam.get("Pi'el/-/-"), 5)
        szov = '\n\n'.join(LG.gerinc_blokk(a, 'BDB', 'H7843', [elo('1Móz 6:12', '', strong='H7843', entry='')],
                                             {'bdb_kartya': True, 'fl': {}})[0])
        olvasoi = szov.split(LG.APPARATUS_KEZDET % 'H7843')[0]
        # a törzs félkövér lehet (a motívum helyén álló jelentés hordozója)
        self.assertRegex(olvasoi, r"\n- (\*\*)?Hiph'il(\*\*)? — a szótár csak alakot közöl \(13 hely\)")
        self.assertRegex(olvasoi, r"\n- (\*\*)?Pi'el(\*\*)? — a szótár csak alakot közöl \(5 hely\)")

    def test_olvasoi_glossza_es_egy_torzsalak(self):
        self.assertEqual(LG.vegyes_cim_nelkul("Hithpa'el", 'Hithpael — perfectum הִתְאַבֵּל 1Sám 15:35'), 'perfectum הִתְאַבֵּל 1Sám 15:35')
        self.assertEqual(LG.vegyes_cim_nelkul("Hiph'il", 'Hiphil_103 perfectum'), 'perfectum')
        self.assertIsNone(LG.olvasoi_glossza("Hithpa'el", '', 'Hithpael — perfectum הִתְאַבֵּל 1Sám 15:35'))
        self.assertEqual(LG.olvasoi_glossza('2', '', '2 — földdarab, földbirtok 1Móz 47:18-19'), 'földdarab, földbirtok')
        self.assertEqual(LG.olvasoi_glossza('4', '', '4 — átkozódás a היה לאלה kifejezésben'), 'átkozódás')
        self.assertEqual(LG.olvasoi_glossza('1', 'a megművelt föld', 'bármi'), 'a megművelt föld')
        self.assertEqual(LG.fej_glossza('H2555. chamas חָמָס hímnemű főnév Zsolt 7:17: erőszak, jogtalanság — status'),
                         'erőszak, jogtalanság')


class F185BetuJavitas(unittest.TestCase):
    """F185 P4: a 2.31 pe/mem és rés/dálet javításai megjelenítéskor mindkét nyelvre (`bdb_rovidites.betu_javit`, a
    `heber_sorrend_javit` része): a bekapcsolt ág a függvény szintjén és a generátorban (a kapcsolót a teszt kapcsolja be);
    kikapcsolva (DT-F185f, `lexikon_general.BDB_BETU_JAVIT`) a generátor kimenete a régi."""

    def test_betu_javit_pontos_token(self):
        import bdb_rovidites as BR
        t = {'H0127': {'מְּנֵי': 'פְּנֵי'}}
        self.assertEqual(BR.betu_javit('vö. még מְּנֵי הָא׳', 'H0127', t), 'vö. még פְּנֵי הָא׳')
        self.assertEqual(BR.betu_javit('הַמְּנֵיכֶם', 'H0127', t), 'הַמְּנֵיכֶם')      # nem egész token: marad

    def test_heber_sorrend_javit_bekapcsolva(self):
        import bdb_rovidites as BR
        self.assertEqual(BR.heber_sorrend_javit('vö. még מְּנֵי הָא׳', 'H0127'), 'vö. még פְּנֵי הָא׳')
        self.assertEqual(BR.heber_sorrend_javit('(מִן־הָא ׳עָפָד)', 'H0127'), '(מִן־הָא ׳עָפָר)')
        self.assertEqual(BR.heber_sorrend_javit('vö. még מְּנֵי הָא׳', 'H0127', betu=False), 'vö. még מְּנֵי הָא׳')

    def _blokk(self, mid=None):
        return '\n'.join(LG.gerinc_blokk(LG.gerinc_adat(), 'BDB', 'H0127', [elo('1Móz 2:7', '', strong='H0127', entry='H0127')],
                                          {'id': mid, 'fl': {}} if mid else None)[0])

    def test_h0127_blokk_magyar_bekapcsolva(self):
        # F182 (2. fázis, F25): a kapcsoló motívumhalmaz; a HAMART-001 lapján bekapcsolva
        szov = self._blokk('HAMART-001')
        self.assertIn('(מִן־הָא ׳עָפָר)', szov)            # a HAMART-001 1606. sorának esete (rés/dálet)
        self.assertNotIn('עָפָד', szov)
        self.assertIn('vö. még פְּנֵי הָא׳', szov)           # a 1616. sor esete (pe/mem)
        self.assertNotIn('מְּנֵי', szov)

    def test_kapcsolo_kikapcsolva_hatastalan(self):
        # DT731 (b): a régi lapokon kikapcsolva; a kimenet a régi (az E28 újragenerálás nélkül zöld)
        self.assertEqual(LG.BDB_BETU_JAVIT, frozenset({'HAMART-001'}))
        self.assertFalse(LG.bdb_betu_javit_aktiv('ANTROP-001'))
        szov = self._blokk('ANTROP-001')
        self.assertIn('עָפָד', szov)
        self.assertIn('מְּנֵי', szov)


class F187KartyaJavitasok(unittest.TestCase):
    """F187 / F29 (a)–(e): a kétrétegű BDB-kártya olvasói rétegének javításai, és a görög (Thayer) kártya két rétege."""

    @classmethod
    def setUpClass(cls):
        cls.a = LG.gerinc_adat()

    def kartya(self, szotar, strong, versek):
        szov = '\n\n'.join(LG.gerinc_blokk(self.a, szotar, strong, [elo(v, '', strong=strong, szotar=szotar, entry='')
                                                                     for v in versek], {'bdb_kartya': True, 'fl': {}})[0])
        kezd = szov.index(LG.APPARATUS_KEZDET % strong)
        return szov[:kezd], szov[kezd:]

    @staticmethod
    def helyek(olvasoi):
        return next(s for s in olvasoi.split('\n\n') if s.startswith('**A motívum helyein:**'))

    def test_a_piel_glossza_szemelyszammal_kezdodo_alakjegyzekbol(self):
        olvasoi, _app = self.kartya('BDB', 'H0779', ['1Móz 3:14'])
        self.assertIn("- Pi'el — átkozni, átok alá vetni", olvasoi)
        self.assertNotIn('külön meghatározás nélkül', olvasoi)

    def test_b_fej_nem_jelentespont_es_vers_egyszer(self):
        import olvasoi_kapu as OK
        for strong, vers, pont in (('H2403', '1Móz 4:7', '1.b Isten ellen'), ('H6975', '1Móz 3:18', '1. tövisbokor')):
            sor = self.helyek(self.kartya('BDB', strong, [vers])[0])
            self.assertNotIn('a szócikk feje', sor)
            self.assertEqual(sor.count(vers.split(' ')[1]), 1, sor)
            self.assertIn(pont, sor)
            self.assertEqual(OK.helyek_ismetlese(sor), [])

    def test_b_helyek_pontjai(self):
        szocikkek = [{'bdb_id': 'B1', 'fej': (('B1', 'fej'), '', 'x', '', ''),
                      'szakaszok': [(('B1', '-/1/-'), '1', 'egy', '', '')]}]
        # a csak a fejben idézett hely fej-pont marad (a kártyán: „a szótár csak alakként idézi”)
        self.assertEqual(LG.helyek_pontjai([('1Móz 1:1', ('B1', 'fej'))], szocikkek)['1Móz 1:1'], [('B1', 'fej')])
        # a fej más pont mellett, az ős-pont a leszármazott mellett elmarad
        vp = [('1Móz 4:7', ('B1', 'fej')), ('1Móz 4:7', ('B1', '-/1/b'))]
        self.assertEqual(LG.helyek_pontjai(vp, szocikkek)['1Móz 4:7'], [('B1', '-/1/b')])
        vp = [('1Móz 6:12', ('B1', "Hiph'il/-/-")), ('1Móz 6:12', ('B1', "Hiph'il/2/-"))]
        self.assertEqual(LG.helyek_pontjai(vp, szocikkek)['1Móz 6:12'], [('B1', "Hiph'il/2/-")])
        self.assertEqual(LG.CSAK_ALAKKENT, 'a szótár csak alakként idézi')

    def test_c_szocikk_neve_sorszam_es_azonosito_nelkul(self):
        olvasoi, _app = self.kartya('BDB', 'H7451', ['1Móz 6:5'])
        self.assertNotRegex(olvasoi, r'(?<![\w.])(?:\d+|[IVX]+)\.\s+szócikk')
        self.assertNotRegex(olvasoi, r'BDB\d+')
        self.assertIn('- *első szócikk*', olvasoi)
        self.assertIn('- *második szócikk*', olvasoi)
        olvasoi, _app = self.kartya('BDB', 'H2403', ['1Móz 4:7'])
        self.assertNotIn('szócikk*', olvasoi)        # egy látható szócikk: nincs szócikk-név
        self.assertNotRegex(olvasoi, r'BDB\d+')

    def test_c_apparatusban_olvashato_forras_hivatkozas(self):
        # N-F187b (orkesztrátori döntés): az apparátusban a BDB-azonosító olvasható forrás-hivatkozás, nyers útvonal nélkül
        self.assertEqual(LG.bdb_kulcs_olvashato(('BDB9520', 'fej')), 'BDB 9520. szócikk, feje')
        self.assertEqual(LG.bdb_kulcs_olvashato(('BDB2699', '-/5/-')), 'BDB 2699. szócikk, 5. szakasz')
        self.assertEqual(LG.bdb_azonosito_olvashato('a BDB9520 szócikk fejét; **BDB2699**'),
                         'a BDB 9520. szócikk fejét; **BDB 2699. szócikk**')
        _olv, app = self.kartya('BDB', 'H2403', ['1Móz 4:7'])
        self.assertNotRegex(app, r'BDB\d')
        self.assertNotIn('-/5/-', app)
        self.assertIn('**BDB 2699. szócikk**', app)
        self.assertIn('BDB 9520. szócikk, feje → BDB 2699. szócikk, 5. szakasz', app)
        self.assertIn('a BDB 9520. szócikk fejét is tartalmazza', app)

    def test_e_csak_gyenge_pont_nem_felkover(self):
        sz = {'H8034': [
            {'strong': 'H8034', 'sorszam': '2', 'utvonal': 'fej', 'jel': '', 'szoveg': 'name'},
            {'strong': 'H8034', 'sorszam': '3', 'utvonal': '-/4/-', 'jel': '4', 'szoveg': 'of false gods'}]}
        hu = {('H8034', '2'): {'szoveg_hu': 'H8034. név', 'kategoria': 'jelolo_nelkul'},
              ('H8034', '3'): {'szoveg_hu': '4 hamis istenekről 1Kir 18:24', 'kategoria': 'illeszkedik'}}
        a = adat([], [vj_sor('H8034', 310, 'Ézs 1:1', '-/4', okkod='forras_hiba')], sz, hu)
        szov = '\n\n'.join(LG.gerinc_blokk(a, 'BDB', 'H8034', [elo('Ézs 1:1', '', strong='H8034', entry='')],
                                             {'bdb_kartya': True, 'fl': {}})[0])
        olvasoi = szov.split(LG.APPARATUS_KEZDET % 'H8034')[0]
        self.assertIn(r'- 4\. hamis istenekről', olvasoi)   # F182.23: a sor eleji jel escape-elve
        self.assertNotIn('**4.**', olvasoi)
        self.assertIn('vonatkozhat', olvasoi)

    def test_thayer_ket_reteg(self):
        olvasoi, app = self.kartya('Thayer', 'G1944', ['Gal 3:13', 'Gal 3:14'])
        self.assertIn('**A jelentések rendje a Thayer szerint**', olvasoi)
        self.assertIn('a szócikk egésze** (nincs számozott jelentése) — átkozott, utálatos', olvasoi)
        self.assertIn('**A motívum helyein:** Gal 3:13 → a szócikk egésze — átkozott', olvasoi)
        self.assertIn('A szótár ezt a helyet nem idézi: Gal 3:14.', olvasoi)
        self.assertIsNone(re.search('[Ͱ-Ͽἀ-῿]', '\n'.join(s for s in olvasoi.split('\n') if not s.startswith('#####'))))   # a címsoron kívül
        self.assertIn('<summary>%s</summary>' % LG.APPARATUS_CIM, app)
        self.assertIn('ἐπικατάρατον', app)       # a görög alakjegyzék az apparátusban

    def test_thayer_glosszas_cimek(self):
        olvasoi, app = self.kartya('Thayer', 'G1311', ['Jel 11:18'])
        self.assertIn('- **2.b** elpusztítani', olvasoi)
        self.assertIn('- **`2.b` — elpusztítani**', app)
        self.assertRegex(app, r'<summary>2\. – 2\.a \(2 szakasz\): elpusztítani')
        olvasoi, _app = self.kartya('Thayer', 'G2671', ['Zsid 6:8'])
        self.assertIn('c — a szótár csak párhuzamot közöl', olvasoi)
        self.assertIn('Zsid 6:8 → a szócikk eleje — kiátkozás, elátkozás, átok', olvasoi)

    def test_thayer_fej_glossza(self):
        self.assertEqual(LG.thayer_fej_glossza('ἐπικατάρατον (ἐπικαταράομαι x), csak bibliai és egyházi használatban: átkozott, '
                                               'utálatos: Ján 7:49'), 'átkozott, utálatos')
        self.assertIsNone(LG.thayer_fej_glossza('φθορᾶς, ἡ (φθείρω), Aeschylus és Hérodotosz óta:'))



class F182Glossza(unittest.TestCase):
    """F182 (N137, N139): a csonkítási jel a kártya vázlatsorán; a glossza nélküli szakasz három általános esete."""

    def test_n139_forras_elotag(self):
        self.assertEqual(LG.olvasoi_glossza('1.f', '', 'f. a P (H) szerint a pap engesztelést szerez valakiért (על כמּר) bűnért'),
                         'a pap engesztelést szerez valakiért')

    def test_n139_plusz_heber_elotag(self):
        self.assertEqual(LG.olvasoi_glossza('6', '', '+ מִן comparativus: rosszabb, mint, 2Sám 19:8'), 'rosszabb')

    def test_n139_heber_kifejezes_elotag(self):
        self.assertEqual(LG.olvasoi_glossza('8', '', 'מַחֲשֶׁבֶת(ה)רָעָה חָשַׁב gonosz (ártalmas) tervet kigondolni Ez 38:10'),
                         'gonosz tervet kigondolni')

    def test_n139_zarojeles_kezdet_valtozatlan(self):
        self.assertIsNone(LG.olvasoi_glossza('1', '', '(vö. alább) bűn: x'))

    def test_n137_csonkitasi_jel(self):
        t = 'a. ember ellen 1Móz 31:36; 50:17 (E), 4Móz 12:11 (J)'
        self.assertEqual(LG._elso_tagmondat(t), 'ember ellen 1Móz 31:36')
        self.assertEqual(LG._elso_tagmondat(t, csonkit_jel=True), 'ember ellen 1Móz 31:36 …')
        self.assertEqual(LG._elso_tagmondat('a. ember ellen 1Móz 31:36', csonkit_jel=True), 'ember ellen 1Móz 31:36')


class F182KaroliSzamozas(unittest.TestCase):
    """F182 (F32): Károli-versszámozás a szótári hivatkozásokban (csak megjelenítés, az eredeti szám jelölésével)."""

    T = {('2Móz', '22', '27'): ('22', '28'), ('5Móz', '29', '11'): ('29', '12'), ('5Móz', '29', '13'): ('29', '14')}

    def test_konyv_es_fejezet_oroklodik(self):
        self.assertEqual(LG.karoli_szamozas('átok 2Móz 22:27; 5Móz 29:11, 13, 18; 30:1', self.T),
                         'átok 2Móz 22:28 (héber számozás: 22:27); 5Móz 29:12 (héber számozás: 29:11), '
                         '14 (héber számozás: 29:13), 18; 30:1')

    def test_terkep_a_2_29_atkulcsolt_sorabol(self):
        self.assertEqual(LG.bdb_karoli_terkep(LG.gerinc_adat(), 'H0779'), {('2Móz', '22', '27'): ('22', '28')})

    def test_nem_letezo_karoli_vers_jelentes(self):
        import ellenoriz as E
        lap = '## 4. Szótári háttér\n\nl. 2Móz 22:28; 99:1, és 1Móz 3:17\n\n## 5. LXX\n'
        kv = {'versek': {'2Móz 22:28', '1Móz 3:17'}, 'konyvek': {'2Móz', '1Móz'}}
        self.assertEqual(E.szotari_hivatkozas_hibak(lap, kv), ['2Móz 99:1'])


class F182LathatoHibak(unittest.TestCase):
    """F182 (befagyasztás, 1. pont): a HAMART-001 lapján nem áll belső hiányjel a Jelentés cellában, és a tagolatlan szócikk
    pontja nem „nem található”."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lexikon',
                               'HAMART-001_TUDOMANYOS.md'), encoding='utf-8') as f:
            cls.lap = f.read()

    def test_nincs_belso_hianyjel(self):
        for t in ('*(nincs címke:', '*(nincs hozzárendelés)*', 'az útvonal nincs a szakasztáblában'):
            self.assertNotIn(t, self.lap, t)

    def test_nincs_ures_felsorolasjel(self):
        # a sor eleji „- 2. …” a Markdownban üres felsorolásjel + beágyazott számozott lista
        import re
        self.assertEqual(re.findall(r'(?m)^ *- \d+\. .*$', self.lap), [])

    def test_cella_glosszaval(self):
        self.assertIn('| Isten ellen · 1.b[^', self.lap)
        self.assertIn('| a szócikk egésze — fájdalom, fáradság[^', self.lap)

    def test_regi_lapon_valtozatlan(self):
        a = LG.gerinc_adat()
        import general as G
        _, elo = G.tsv_beolvas(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'adat',
                                            'elofordulasok.tsv'))
        sor = next(r for r in elo if r['id'] == 'HAMART-001' and r['igehely'] == '1Móz 3:16')
        self.assertEqual(LG.jelentes_cella(a, sor)[0], '*(nincs hozzárendelés)*')
        self.assertTrue(LG.jelentes_cella(a, sor, uj=True)[0].startswith('a szócikk egésze'))

if __name__ == '__main__':
    unittest.main()
