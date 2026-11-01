#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_vedokorlat.py -- F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md 2. lepes: az
eszkozok/ellenoriz.py 18-21. szabalyanak pozitiv es negativ tesztjei.

Ideiglenes (a repon kivuli) gyoker/adat/ + gyoker/lexikon/ konyvtarban fut; a kivetellista a
`funkcio_kapcsolok.tsv` `kivetel` sora (DT-F148a), ugyanazzal a fuggvennyel olvasva, mint a generatorban.
A valodi adaton a kotelezo negativ teszt: az 1Kir 18:25-26 „Baál nevével” erteke nem jelzett (20.).

    python eszkozok/teszt_ellenoriz_vedokorlat.py
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

import ellenoriz as E  # noqa: E402
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402
import szerep_karoli as SZK  # noqa: E402


def ir(ut, fej, sorok):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(fej) + '\n')
        for s in sorok:
            f.write('\t'.join(s.get(k, '') for k in fej) + '\n')


KAPCS_FEJ = ['kapcsolo', 'id', 'allapot', 'szerep_cim_resz', 'indok', 'proveniencia']
CIMKE_FEJ = ['szotar', 'strong', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu', 'proveniencia', 'megjegyzes']
BDB_FEJ = ['strong', 'bdb_id', 'sorszam', 'alszocikk', 'szakasz', 'resz', 'utvonal', 'jelolo', 'jel']
TILT_FEJ = ['minta', 'magyar_alak']


def elo(mid, igehely, **k):
    sor = {'id': mid, 'igehely': igehely, 'strong': 'H7121', 'karoli_szo': 'segítségül hívá',
           'lexikon_szotar': 'BDB', 'lexikon_entry_id': 'H7121', 'jelentes_szam': '2.c', 'jelentes_hu': 'segítségül hívni'}
    sor.update(k)
    return sor


class Alap(unittest.TestCase):
    def setUp(self):
        self.gyoker = tempfile.mkdtemp(prefix='F148_teszt_')
        self.adat = os.path.join(self.gyoker, 'adat')
        self.lex = os.path.join(self.gyoker, 'lexikon')
        os.makedirs(self.adat)
        os.makedirs(self.lex)
        ir(os.path.join(self.adat, 'funkcio_kapcsolok.tsv'), KAPCS_FEJ, [
            {'kapcsolo': 'SZOTARI_GERINC', 'id': 'GERINC-001', 'allapot': 'aktiv'},
            {'kapcsolo': 'SZOTARI_GERINC', 'id': 'REGI-001', 'allapot': 'kivetel'},
        ])
        ir(os.path.join(self.adat, 'szotar_szakasz_cimke.tsv'), CIMKE_FEJ, [
            {'szotar': 'BDB', 'strong': 'H7121', 'szakasz': 'Qal/2/c', 'lexikon_jelentes_szam': '2.c',
             'cimke_hu': 'segítségül hívni', 'proveniencia': 'scope=manual'},
        ])
        ir(os.path.join(self.adat, 'bdb_szakaszok.tsv'), BDB_FEJ, [
            {'strong': 'H7121', 'sorszam': '1', 'utvonal': 'fej', 'jelolo': 'fej'},
            {'strong': 'H7121', 'sorszam': '2', 'utvonal': 'Qal/2/c', 'jelolo': 'point', 'jel': 'c'},
            {'strong': 'H0922', 'sorszam': '1', 'utvonal': 'cim', 'jelolo': 'cim'},
            {'strong': 'H0922', 'sorszam': '2', 'utvonal': 'fej', 'jelolo': 'fej'},
        ])
        ir(os.path.join(self.adat, 'tiltott_fordulatok.tsv'), TILT_FEJ, [{'minta': 'hívogat', 'magyar_alak': 'hívogat'}])
        with open(os.path.join(self.gyoker, 'DONTESEK.md'), 'w', encoding='utf-8') as f:
            f.write('| DT | x |\n|---|---|\n| DT272 | gerinc |\n')
        with open(os.path.join(self.gyoker, 'NYITOTT_FELADATOK.md'), 'w', encoding='utf-8') as f:
            f.write('- **N62 — valami** leírás\n## Lezárva\n* N63 — lezárt tétel, kiemelés nélkül\n')

    def tearDown(self):
        shutil.rmtree(self.gyoker)

    def lap(self, nev, szoveg):
        with open(os.path.join(self.lex, nev), 'w', encoding='utf-8') as f:
            f.write(szoveg)


class KivetellistaEgyHelyen(Alap):
    def test_ugyanaz_a_fuggveny(self):
        # elfogadás 6.: a lista egyetlen helyen (adat), a generátor és az ellenoriz.py ugyanazt hívja
        self.assertIs(E.SZK, SZK)
        self.assertEqual(E.gerinc_kivetelek(self.adat), frozenset({'REGI-001'}))
        valodi = E.gerinc_kivetelek(os.path.join(E.ROOT, 'adat'))
        self.assertEqual(valodi, LG.GERINC_KIVETEL_MOTIVUMOK)


class Szabaly18(Alap):
    def test_rendben(self):
        s = E.szabaly18_gerinc_cimke(self.adat, [elo('GERINC-001', '1Móz 4:26')])
        self.assertEqual(s.verdict, 'RENDBEN')

    def test_minosito_levagva(self):
        s = E.szabaly18_gerinc_cimke(self.adat, [elo('GERINC-001', '1Móz 4:26', jelentes_szam='2.c (tagadva)')])
        self.assertEqual(s.verdict, 'RENDBEN')

    def test_hianyzo_cimke_sertes(self):
        s = E.szabaly18_gerinc_cimke(self.adat, [elo('GERINC-001', '2Móz 33:19', jelentes_szam='3')])
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('nincs sora', s.peldak[0])

    def test_ures_mezo_sertes(self):
        s = E.szabaly18_gerinc_cimke(self.adat, [elo('UJ-001', 'Zsolt 16:10', jelentes_szam='')])
        self.assertEqual(s.verdict, 'SÉRTÉS')  # új, kapcsolóbejegyzés nélküli motívum: gerinces

    def test_kivetel_nem_fut(self):
        s = E.szabaly18_gerinc_cimke(self.adat, [elo('REGI-001', 'Zsolt 16:10', jelentes_szam='')])
        self.assertEqual(s.verdict, 'RENDBEN')


class Szabaly19(Alap):
    def test_rendben(self):
        self.assertEqual(E.szabaly19_kotelezo_mezok(self.adat, [elo('GERINC-001', '1Móz 4:26')]).verdict, 'RENDBEN')

    def test_ures_sertes(self):
        for mezo in E.KOTELEZO_MEZOK_19:
            s = E.szabaly19_kotelezo_mezok(self.adat, [elo('GERINC-001', '1Móz 4:26', **{mezo: ''})])
            self.assertEqual(s.verdict, 'SÉRTÉS', mezo)
            self.assertIn(mezo, s.peldak[0])

    def test_kivetel_jelentes(self):
        s = E.szabaly19_kotelezo_mezok(self.adat, [elo('REGI-001', 'Zsolt 16:10', karoli_szo=''),
                                                   elo('REGI-001', 'Zsolt 18:6', jelentes_szam='')])
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertEqual(s.n, 2)
        self.assertIn('REGI-001: 2', s.megjegyzes)

    def test_tagolatlan_egyetlen_strong(self):
        # DT-F148b (1): a sor egyetlen Strongja tagolatlan → explicit `tagolatlan`
        s = E.szabaly19_kotelezo_mezok(self.adat, [elo('GERINC-001', '1Móz 1:2', strong='H0922',
                                                       lexikon_entry_id='H0922', jelentes_szam='tagolatlan')])
        self.assertEqual(s.verdict, 'RENDBEN')
        self.assertEqual(E.szabaly18_gerinc_cimke(self.adat, [elo('GERINC-001', '1Móz 1:2', strong='H0922',
                         lexikon_entry_id='H0922', jelentes_szam='tagolatlan')]).verdict, 'RENDBEN')

    def test_tagolatlan_szam_helyett(self):
        s = E.szabaly19_kotelezo_mezok(self.adat, [elo('GERINC-001', '1Móz 1:2', strong='H0922',
                                                       lexikon_entry_id='H0922', jelentes_szam='1')])
        self.assertEqual(s.verdict, 'SÉRTÉS')

    def test_tagolatlan_entry_osszetett_soron(self):
        # DT-F148b (3): összetett soron (H8414+H0922) a tagolt token az entry
        s = E.szabaly19_kotelezo_mezok(self.adat, [elo('GERINC-001', '1Móz 1:2', strong='H8414+H0922',
                                                       lexikon_entry_id='H0922', jelentes_szam='tagolatlan')])
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('összetett', s.peldak[0])

    def test_tagolatlan_tagolt_szocikken(self):
        s = E.szabaly19_kotelezo_mezok(self.adat, [elo('GERINC-001', '1Móz 4:26', jelentes_szam='tagolatlan')])
        self.assertEqual(s.verdict, 'SÉRTÉS')


class Szabaly20(Alap):
    def test_szo_jelentese_rendben(self):
        for ertek in ('segítségül hívni', 'invokálni, segítségül hívni', 'Baál nevével'):
            s = E.szabaly20_jelentes_hu(self.adat, [elo('GERINC-001', '1Kir 18:25', jelentes_hu=ertek)])
            self.assertEqual(s.verdict, 'RENDBEN', ertek)

    def test_funkcio_ertelmezes_sertes(self):
        for ertek in ('hívni (NEM a valódi Istent)', 'tagadó szerkezet', 'a próféta vádjaként',
                      'a motívum magja', 'funkciója: invokáció', 'invokáció', 'hívogatni'):
            s = E.szabaly20_jelentes_hu(self.adat, [elo('GERINC-001', '1Kir 18:25', jelentes_hu=ertek)])
            self.assertEqual(s.verdict, 'SÉRTÉS', ertek)

    def test_kivetel_jelentes(self):
        s = E.szabaly20_jelentes_hu(self.adat, [elo('REGI-001', 'Zsolt 9:18', jelentes_hu='a motívum')])
        self.assertEqual(s.verdict, 'JELENTÉS')

    def test_valodi_1kir_18_25_26(self):
        # kötelező negatív teszt: az 1Kir 18:25–26 „Baál nevével” BDB-szöveg, nem értelmezés
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        sorok = [r for r in elo_sorok if r['id'] == 'ISTENTISZT-001' and r['igehely'] in ('1Kir 18:25', '1Kir 18:26')]
        self.assertEqual(len(sorok), 2)
        self.assertTrue(all(r['jelentes_hu'] == 'Baál nevével' for r in sorok))
        s = E.szabaly20_jelentes_hu(os.path.join(E.ROOT, 'adat'), sorok, kivetel=frozenset())
        self.assertEqual(s.verdict, 'RENDBEN')


class Szabaly21(Alap):
    TISZTA = '# Lap\n\nA döntés: DT272; a nyitott tétel: N62; a lezárt: N63.\n'

    def test_rendben(self):
        self.lap('GERINC-001_TUDOMANYOS.md', self.TISZTA)
        self.assertEqual(E.szabaly21_lap_tisztasag(self.adat, main=True).verdict, 'RENDBEN')

    def test_helyorzo_ag_jelentes_main_sertes(self):
        # DT-F148d (2)
        self.lap('GERINC-001_TUDOMANYOS.md', self.TISZTA + '(DT-F121g)\n')
        self.assertEqual(E.szabaly21_lap_tisztasag(self.adat, main=False).verdict, 'JELENTÉS')
        self.assertEqual(E.szabaly21_lap_tisztasag(self.adat, main=True).verdict, 'SÉRTÉS')

    def test_kezzel_irando(self):
        self.lap('GERINC-001_TORZSCIKK.md', self.TISZTA + '*Kézzel írandó.*\n')
        self.assertEqual(E.szabaly21_lap_tisztasag(self.adat, main=True).verdict, 'SÉRTÉS')

    def test_az_nevelo_mindig_sertes(self):
        self.lap('GERINC-001_TUDOMANYOS.md', self.TISZTA + 'a(z) 1Kir 18:24 verse\n')
        s = E.szabaly21_lap_tisztasag(self.adat, main=False)
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('(ii)', s.peldak[0])

    def test_nem_letezo_n_sertes_letezo_nem(self):
        # elfogadás 3.: a kitalált N9999 jelzett, a létező N62 nem
        self.lap('GERINC-001_TUDOMANYOS.md', self.TISZTA + 'l. N9999 és DT9999\n')
        s = E.szabaly21_lap_tisztasag(self.adat, main=False)
        self.assertEqual(s.verdict, 'SÉRTÉS')
        szov = '\n'.join(s.peldak)
        self.assertIn('N9999', szov)
        self.assertIn('DT9999', szov)
        self.assertNotIn('N62', szov)
        self.assertNotIn('N63', szov)  # a lezárt, kiemelés nélküli tétel is létező (ELLENOR_F148 4.)
        self.assertNotIn('DT272', szov)

    def test_kivetel_lap_jelentes(self):
        self.lap('REGI-001_TUDOMANYOS.md', self.TISZTA + 'a(z) N9999 (DT-F1a)\n')
        self.assertEqual(E.szabaly21_lap_tisztasag(self.adat, main=True).verdict, 'JELENTÉS')

    def test_mas_fajl_kimarad(self):
        self.lap('README.md', 'a(z) N9999\n')
        self.assertEqual(E.szabaly21_lap_tisztasag(self.adat, main=True).verdict, 'RENDBEN')

    def test_main_agon_kenyszer(self):
        self.assertTrue(E.main_agon('main'))
        self.assertFalse(E.main_agon('ag'))


class ValodiAdat(unittest.TestCase):
    def test_20_21_a_repon(self):
        # a repó mai adatán a 18–21. szabály tiszta (F148: az ALVIL-001 59 sora gépileg kitöltve, ⛔ A feloldva)
        adat = os.path.join(E.ROOT, 'adat')
        _, elo_sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        self.assertEqual(E.szabaly18_gerinc_cimke(adat, elo_sorok).verdict, 'RENDBEN')
        self.assertNotEqual(E.szabaly19_kotelezo_mezok(adat, elo_sorok).verdict, 'SÉRTÉS')
        self.assertEqual(E.szabaly20_jelentes_hu(adat, elo_sorok).verdict, 'RENDBEN')
        self.assertIn(E.szabaly21_lap_tisztasag(adat, main=True).verdict, ('RENDBEN',))


if __name__ == '__main__':
    unittest.main()
