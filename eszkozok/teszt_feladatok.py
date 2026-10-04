#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_feladatok.py -- F20_BEFOGADAS_BRIEF.md (B1): az `eszkozok/feladatok.py`
tesztjei, ideiglenes konyvtarban felepitett fixture-briefekkel.

Futtatas: python eszkozok/teszt_feladatok.py
"""

import os
import sys
import tempfile
import unittest
from datetime import date

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402

MA = date(2026, 9, 30)

FELADATOK_VAZ = """# FELADATOK.md

## 1. fázis
%s

## 2. fázis
%s

## Folyamat
%s

## Naplózás
%s

## Kész
%s
""" % tuple('%s\n%s\n%s' % (F.MARKER_KEZDET % c, '(régi)', F.MARKER_VEGE % c)
            for c in F.CELOK)


def brief_szoveg(szam=None, cim='Teszt', tipus='feladat', fazis='1', modell='sonnet',
                 allapot='nem_indult', olvas=None, ir=None, fugg=None, nem_fugg=None,
                 kod=None, extra='', torzs='', **kozben):
    sorok = ['---']
    if szam is not None:
        sorok.append('feladat: %d' % szam)
    sorok.append('cim: %s' % cim)
    if kod:
        sorok.append('kod: %s' % kod)
    sorok.append('tipus: %s' % tipus)
    if fazis and tipus == 'feladat':
        sorok.append('fazis: %s' % fazis)
    sorok += ['modell: %s' % modell, 'allapot: %s' % allapot,
              'ad: mit ad', 'kovetkezo: következő lépés']
    if fugg is not None:
        sorok.append('fugg: [%s]' % ', '.join(str(x) for x in fugg))
    if nem_fugg is not None:
        sorok.append('nem_fugg: [%s]' % ', '.join(str(x) for x in nem_fugg))
    if olvas is not None:
        sorok.append('olvas: [%s]' % ', '.join(olvas))
    if ir is not None:
        sorok.append('ir: [%s]' % ', '.join(ir))
    for k, v in kozben.items():
        sorok.append('%s: %s' % (k, v))
    sorok.append('---')
    return '\n'.join(sorok) + '\n' + extra + '\n' + torzs + '\n'


class Gyoker(object):
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ut = self.tmp.name
        with open(os.path.join(self.ut, 'FELADATOK.md'), 'w', encoding='utf-8', newline='') as f:
            f.write(FELADATOK_VAZ)

    def brief(self, nev, szoveg):
        with open(os.path.join(self.ut, nev), 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)

    def olvas(self, nev='FELADATOK.md'):
        with open(os.path.join(self.ut, nev), encoding='utf-8', newline='') as f:
            return f.read()

    def briefek(self):
        return F.briefek_beolvas(self.ut)

    def bezar(self):
        self.tmp.cleanup()


class Alap(unittest.TestCase):
    def setUp(self):
        self.g = Gyoker()
        self.addCleanup(self.g.bezar)

    def fugg(self):
        return F.fuggesek(self.g.briefek(), {})


class FejlecTest(Alap):
    def test_lista_idezojellel(self):
        fej, _, hibak = F.fejlec_elemez('---\nolvas: [a, "*_BRIEF.md", b/]\n---\nszoveg')
        self.assertEqual(hibak, [])
        self.assertEqual(fej['olvas'], ['a', '*_BRIEF.md', 'b/'])

    def test_ures_lista(self):
        fej, _, _ = F.fejlec_elemez('---\nfugg: []\n---\n')
        self.assertEqual(fej['fugg'], [])

    def test_nincs_fejlec(self):
        fej, _, hibak = F.fejlec_elemez('# cim\nszoveg')
        self.assertEqual(fej, {})
        self.assertTrue(hibak)

    def test_crlf(self):
        fej, _, hibak = F.fejlec_elemez('---\r\nfeladat: 3\r\ncim: X\r\n---\r\n')
        self.assertEqual(hibak, [])
        self.assertEqual(fej['feladat'], 3)

    def test_kozvetlen_futtatas_blokk_atugrasa(self):
        """A nyitó prompt blokk a törzsben van; sem a fejlécet, sem a modellt nem érinti."""
        torzs = ('# cím\n<!-- KOZVETLEN_FUTTATAS -->\n> Modell: opus — hajtsd végre, és pusholj\n'
                 '<!-- /KOZVETLEN_FUTTATAS -->\n')
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, ir=['x'], olvas=['y'], torzs=torzs))
        b = self.g.briefek()[0]
        self.assertEqual(b.hibak, [])
        self.assertEqual(F.ellenoriz([b], self.g.ut), [])


class FuggesTest(Alap):
    def test_levezetett_fugges_fajlra(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv'], ir=['a.txt']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b.txt'], ir=['adat/x.tsv']))
        fugg, utk, _, _ = self.fugg()
        self.assertIn(2, fugg[1])
        self.assertEqual(fugg[1][2][0], 'levezetett')
        self.assertEqual(fugg[2], {})
        self.assertEqual(utk, [])

    def test_konyvtar_olvasas_kontextus(self):
        """F39 (DT-F39g): a `/`-re végződő olvas-bejegyzés nem ad sorrendet."""
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/'], ir=['a.txt']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b.txt'], ir=['adat/x.tsv']))
        self.assertEqual(self.fugg()[0][1], {})

    def test_konyvtar_iras_konkret_olvasassal(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv'], ir=['a.txt']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b.txt'], ir=['adat/']))
        self.assertIn(2, self.fugg()[0][1])

    def test_glob_illesztes(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['"eszkozok/*.py"'], ir=['a.txt']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b.txt'], ir=['eszkozok/x.py']))
        self.assertIn(2, self.fugg()[0][1])

    def test_nincs_egyezes(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv'], ir=['a.txt']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b.txt'], ir=['adat/y.tsv']))
        self.assertEqual(self.fugg()[0], {1: {}, 2: {}})

    def test_lezart_nem_fuggtet(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv'], ir=['a.txt']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b.txt'], ir=['adat/x.tsv'],
                                                    allapot='lezarva'))
        self.assertEqual(self.fugg()[0][1], {})

    def test_iras_iras_utkozes(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['q'], ir=['adat/x.tsv']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['r'], ir=['adat/']))
        _, utk, _, sorrend = self.fugg()
        self.assertEqual([(a, b) for a, b, _ in utk], [(1, 2)])
        self.assertEqual(sorrend[0][:2], (1, 2))
        self.assertIn('számból', sorrend[0][2])

    def test_utkozes_sorrendjet_a_fugges_adja(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['q'], ir=['adat/x.tsv'], fugg=[2]))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['r'], ir=['adat/x.tsv']))
        sorrend = self.fugg()[3]
        self.assertEqual(sorrend[0], (2, 1, 'függésből'))

    def test_kozos_fajl_kivetele(self):
        for n, k in ((1, 'A'), (2, 'B')):
            self.g.brief('F0%d_%s_BRIEF.md' % (n, k),
                         brief_szoveg(n, olvas=['FELADATOK.md', 'DONTESEK.md'],
                                      ir=['FELADATOK.md', 'DONTESEK.md',
                                          'NYITOTT_FELADATOK.md', 'adat/szotar_szerepek.tsv']))
        fugg, utk, _, _ = self.fugg()
        self.assertEqual(fugg, {1: {}, 2: {}})
        self.assertEqual(utk, [])

    def test_sajat_brief_es_naplo_kivetele(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, kod='SZOTAR S2', olvas=['*_BRIEF.md'],
                                                    ir=['F01_A_BRIEF.md', 'naplok/SZOTAR_x.md']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, kod='BETA', olvas=['naplok/SZOTAR_x.md'],
                                                    ir=['F02_B_BRIEF.md', 'naplok/F02_y.md']))
        fugg, utk, _, _ = self.fugg()
        self.assertEqual(fugg, {1: {}, 2: {}})
        self.assertEqual(utk, [])

    def test_regi_fejlec(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv']))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, ir=['a']))
        regiek = dict(self.fugg()[2])
        self.assertEqual(regiek[1], ['ir'])
        self.assertEqual(regiek[2], ['olvas'])

    def test_kezi_fugg_es_nem_fugg(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv'], ir=['a'],
                                                    fugg=[3], nem_fugg=[2]))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b'], ir=['adat/x.tsv']))
        self.g.brief('F03_C_BRIEF.md', brief_szoveg(3, olvas=['c'], ir=['c']))
        fugg = self.fugg()[0]
        self.assertEqual(fugg[1], {3: ('kezi', 'kezi')})

    def test_kimenet_jelolese(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['adat/x.tsv'], ir=['a'], fugg=[3]))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, olvas=['b'], ir=['adat/x.tsv']))
        self.g.brief('F03_C_BRIEF.md', brief_szoveg(3, olvas=['c'], ir=['c']))
        szoveg = F.fuggesek_szoveg(self.g.briefek(), {})
        self.assertIn('FUGGES\t1\t2\tadat/x.tsv*', szoveg)
        self.assertIn('FUGGES\t1\t3\tkezi', szoveg)


class EllenorizTest(Alap):
    def hibak(self):
        return F.ellenoriz(self.g.briefek(), self.g.ut)

    def test_ervenyes(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['a'], ir=['b']))
        self.assertEqual(self.hibak(), [])

    def test_hibas_allapot(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, allapot='kesz'))
        self.assertTrue(any('allapot érvénytelen' in u for _, u in self.hibak()))

    def test_kettozott_szam(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1))
        self.g.brief('F01_B_BRIEF.md', brief_szoveg(1))
        self.assertTrue(any('kettőzött' in u for _, u in self.hibak()))

    def test_fajlnev_szam_egyezes(self):
        self.g.brief('F02_A_BRIEF.md', brief_szoveg(1))
        self.assertTrue(any('nem egyezik a `feladat`' in u for _, u in self.hibak()))

    def test_modell_egyezes(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, modell='opus',
                                                    extra='*v1 · Modell: sonnet · x*'))
        self.assertTrue(any('régi `Modell:`' in u for _, u in self.hibak()))
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, modell='sonnet',
                                                    extra='**Modell:** Sonnet; Opus a fő szálon.'))
        self.assertEqual(self.hibak(), [])

    def test_hianyzo_mezo_es_tipus(self):
        self.g.brief('F01_A_BRIEF.md', '---\nfeladat: 1\ncim: X\ntipus: feladat\n---\n')
        ui = [u for _, u in self.hibak()]
        self.assertTrue(any('hiányzó kötelező mező: modell' in u for u in ui))
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, tipus='valami'))
        self.assertTrue(any('tipus érvénytelen' in u for _, u in self.hibak()))

    def test_archiv_fejlec_szam_nelkul(self):
        self.g.brief('RENDER_BRIEF.md', brief_szoveg(None, tipus='archiv', allapot='lezarva'))
        self.assertEqual(self.hibak(), [])
        self.g.brief('RENDER_BRIEF.md', brief_szoveg(5, tipus='archiv', allapot='lezarva'))
        self.assertTrue(self.hibak())

    def test_fejlec_nelkuli_brief_hiba_de_beerkezo_kimarad(self):
        self.g.brief('REGI_BRIEF.md', '# fejléc nélkül\n')
        self.assertTrue(self.hibak())
        os.remove(os.path.join(self.g.ut, 'REGI_BRIEF.md'))
        os.makedirs(os.path.join(self.g.ut, 'beerkezo'))
        with open(os.path.join(self.g.ut, 'beerkezo', 'X_BRIEF.md'), 'w', encoding='utf-8') as f:
            f.write('# fejléc nélkül\n')
        self.assertEqual(self.hibak(), [])

    def test_fugg_ismeretlen_szamra(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, fugg=[9]))
        self.assertTrue(any('nincs ilyen feladat' in u for _, u in self.hibak()))

    def test_ismeretlen_kulcs(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, valami='x'))
        self.assertTrue(any('ismeretlen kulcs' in u for _, u in self.hibak()))


class GeneralTest(Alap):
    def felallit(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(
            1, cim='Első', kod='ELSO', olvas=['adat/x.tsv'], ir=['a'], allapot='fut'))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(
            2, cim='Második', olvas=['b'], ir=['adat/x.tsv'], fugg=[3]))
        self.g.brief('F03_C_BRIEF.md', brief_szoveg(
            3, cim='Harmadik', olvas=['c'], ir=['c'], allapot='lezarva',
            lezarva_osszegzes='kész, merge `abc1234` (PR #1, 09.29)'))
        self.g.brief('F04_D_BRIEF.md', brief_szoveg(
            4, cim='Render', fazis='2', olvas=['d'], ir=['d']))
        self.g.brief('F05_E_BRIEF.md', brief_szoveg(
            5, cim='Folyamat', fazis='folyamat', olvas=['e'], ir=['e']))
        self.g.brief('F06_F_BRIEF.md', brief_szoveg(
            6, cim='Napló', tipus='naplozas', olvas=['f'], ir=['naplok/F06_x.md']))

    def test_blokkok(self):
        self.felallit()
        b = F.blokkok(self.g.briefek(), self.g.ut, MA, {})
        self.assertIn('| 1 | Első (ELSO) |', b['fazis1'])
        self.assertIn('▶ fut', b['fazis1'])
        self.assertIn('#3 (kész)', b['fazis1'])
        self.assertIn('| 4 | Render |', b['fazis2'])
        self.assertIn('Megjegyzés', b['fazis2'])
        self.assertIn('| 5 | Folyamat |', b['folyamat'])
        self.assertIn('- #6 Napló', b['naplozas'])
        self.assertIn('- Harmadik (#3): kész, merge `abc1234`', b['kesz'])
        self.assertNotIn('Harmadik', b['fazis1'])

    def test_levezetett_fugges_csillaggal(self):
        self.felallit()
        b = F.blokkok(self.g.briefek(), self.g.ut, MA, {})
        sor = [s for s in b['fazis1'].split('\n') if s.startswith('| 1 |')][0]
        self.assertIn('#2*', sor)

    def test_general_idempotens_nulla_diff(self):
        self.felallit()
        self.assertTrue(F.general(self.g.ut, MA, main_all={}))
        elso = self.g.olvas()
        self.assertFalse(F.general(self.g.ut, MA, main_all={}))
        self.assertEqual(self.g.olvas(), elso)
        self.assertIn('(régi)', FELADATOK_VAZ)
        self.assertNotIn('(régi)', elso)

    def test_kezi_szakasz_erintetlen(self):
        self.felallit()
        F.general(self.g.ut, MA, main_all={})
        ut = self.g.olvas()
        self.assertIn('# FELADATOK.md\n\n## 1. fázis', ut)
        self.assertIn('## Kész\n', ut)

    def test_pr_allapot_es_kesz_kor(self):
        self.felallit()
        # a main-en a #3 még `fut` volt: a PR-ben lezárt -> 🔀 PR-ben, nem „Kész”
        b = F.blokkok(self.g.briefek(), self.g.ut, MA, {3: 'fut'})
        self.assertIn('🔀 PR-ben', b['fazis1'])
        self.assertNotIn('Harmadik (#3)', b['kesz'])

    def test_hianyzo_jelolo(self):
        self.felallit()
        with open(os.path.join(self.g.ut, 'FELADATOK.md'), 'w', encoding='utf-8') as f:
            f.write('# nincs jelölő\n')
        with self.assertRaises(ValueError):
            F.general(self.g.ut, MA, main_all={})

    def test_pr_blokk_modositas(self):
        """E18: az alap blokkjától eltérő generált blokk hibát ad (git nélkül: alap nincs -> nincs hiba)."""
        self.assertEqual(F.pr_blokk_ellenorzes(self.g.ut, 'nincs/ilyen'), [])


class AtvetelTest(Alap):
    def test_tabla_sorok_es_atvetel(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, allapot='nem_indult'))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, allapot='nem_indult'))
        tabla = ('| # | Feladat | Mit ad | Állapot | Függ | Következő lépés | Hol |\n'
                 '|---|---|---|---|---|---|---|\n'
                 '| 1 | A | x | ▶ fut | — | **Te:** döntés | `F01` |\n'
                 '| 2 | B | x | ⬜ brief kell | — | brief | `F02` |\n')
        with open(os.path.join(self.g.ut, 'FELADATOK.md'), 'w', encoding='utf-8') as f:
            f.write(tabla)
        self.assertEqual(F.tabla_sorok(tabla)[1], ('fut', '**Te:** döntés'))
        valt = F.atvetel(self.g.ut)
        self.assertEqual(len(valt), 4)
        b = {x.szam: x for x in self.g.briefek()}
        self.assertEqual(b[1].fej['allapot'], 'fut')
        self.assertEqual(b[1].fej['kovetkezo'], '**Te:** döntés')
        self.assertEqual(b[2].fej['allapot'], 'brief_kell')
        self.assertEqual(F.atvetel(self.g.ut), [])


class KovetkezoSzamTest(Alap):
    def test_max_plusz_egy(self):
        self.g.brief('F03_A_BRIEF.md', brief_szoveg(3))
        self.g.brief('F07_B_BRIEF.md', brief_szoveg(7))
        self.assertEqual(F.kovetkezo_szam(self.g.briefek()), 8)

    def test_ures(self):
        self.assertEqual(F.kovetkezo_szam(self.g.briefek()), 1)


class KeszDatumTest(Alap):
    def test_datum_az_osszegzesbol(self):
        self.assertEqual(F._osszegzes_datum('merge `abc` (PR #62, 09.27)', MA), date(2026, 9, 27))
        self.assertEqual(F._osszegzes_datum('merge `abc` (09.29); PR #60 (`8bd`)', MA), date(2026, 9, 29))
        self.assertIsNone(F._osszegzes_datum('nincs datum', MA))
        self.assertEqual(F._osszegzes_datum('(12.30)', MA), date(2025, 12, 30))

    def test_regi_tetel_kiesik_a_keszbol(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(
            1, cim='Régi', olvas=['a'], ir=['b'], allapot='lezarva', lezarva_osszegzes='merge `abc` (09.01)'))
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(
            2, cim='Friss', olvas=['c'], ir=['d'], allapot='lezarva', lezarva_osszegzes='merge `def` (09.27)'))
        b = F.blokkok(self.g.briefek(), self.g.ut, MA, {})
        self.assertNotIn('Régi', b['kesz'])
        self.assertIn('Friss', b['kesz'])


class ExtraTest(Alap):
    def test_extra_szam_es_fugges(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['q'], ir=['adat/x.tsv']))
        ex = os.path.join(self.g.ut, 'kivul.md')
        with open(ex, 'w', encoding='utf-8') as f:
            f.write(brief_szoveg(None, tipus='feladat', olvas=['adat/x.tsv'], ir=['m']))
        b = F.extra_hozzaad(self.g.briefek(), [ex])
        self.assertEqual(b[-1].szam, 2)
        fugg, _, _, _ = F.fuggesek(b, {})
        self.assertIn(1, fugg[2])

    def test_extra_csonk_felvaltja_a_szamot(self):
        self.g.brief('F03_C_BRIEF.md', brief_szoveg(3, allapot='brief_kell'))
        ex = os.path.join(self.g.ut, 'kivul.md')
        with open(ex, 'w', encoding='utf-8') as f:
            f.write(brief_szoveg(3, olvas=['a'], ir=['b']))
        b = F.extra_hozzaad(self.g.briefek(), [ex])
        self.assertEqual([x.szam for x in b].count(3), 1)
        self.assertEqual(b[-1].allapot, 'nem_indult')


class CliTest(Alap):
    def test_kilepesi_kodok(self):
        self.g.brief('F01_A_BRIEF.md', brief_szoveg(1, olvas=['a'], ir=['b']))
        self.assertEqual(F.main(['--gyoker', self.g.ut, 'ellenoriz']), 0)
        self.g.brief('F02_B_BRIEF.md', brief_szoveg(2, allapot='rossz'))
        self.assertEqual(F.main(['--gyoker', self.g.ut, 'ellenoriz']), 1)


# F39: a függés-levezetés tesztjei (eszkozok/tesztek/), ugyanebben a futtatásban
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tesztek'))
from test_feladatok_fugges import MaiAllapotTest, SzabalyTest  # noqa: E402,F401
# F49: a FOLYTATAS/VAR_RAD jelölés tesztjei, ugyanígy
from test_feladatok_folytatas import FolytatasTest  # noqa: E402,F401
# F32: a csomag-ellenőrzés, az OLVAS_HIANY és a `munka` mező tesztjei, ugyanígy
from test_feladatok_kontextus import KontextusTest  # noqa: E402,F401


if __name__ == '__main__':
    unittest.main(verbosity=1)
