#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_szabalyok.py -- CI.1: minden E2-E16 szabalyhoz legalabb egy pozitiv es
egy negativ tesztfixture, a F02_CI_ELLENORZES_BRIEF.md-ben hivatkozott
incidensek rekonstrualt mintaival.

A tesztek egy ideiglenes konyvtarba irjak a fixture-fajlokat (nem az eles
repoba -- a lexikon/, tematikus_lezart/ stb. valodi tartalmat a teszt nem
piszkitja), es a `kozos`/`szabalyok` modulok ROOT/ADAT valtozojat erre az
ideiglenes gyokerre allitjak at a teszt idejere -- l. `_IdeiglenesGyoker`.

Futtatas a repo gyokerebol:
    python -m unittest eszkozok.ellenorzes.tesztek.test_szabalyok -v
vagy
    python eszkozok/ellenorzes/tesztek/test_szabalyok.py
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

_ITT = os.path.dirname(os.path.abspath(__file__))
_ELLENORZES = os.path.dirname(_ITT)
sys.path.insert(0, _ELLENORZES)

import kozos as K
import szabalyok as SZ


class _IdeiglenesGyoker(object):
    """Context manager: `kozos.ROOT`/`ADAT` es `szabalyok.ROOT`/`ADAT` egy
    ideiglenes konyvtarra mutat a `with` blokk idejere, utana visszaall."""

    def __init__(self):
        self.tmp = None
        self._eredeti = {}

    def __enter__(self):
        self.tmp = tempfile.mkdtemp(prefix='ci_teszt_')
        adat = os.path.join(self.tmp, 'adat')
        os.makedirs(adat)
        self._eredeti = {
            (K, 'ROOT'): K.ROOT, (K, 'ADAT'): K.ADAT,
            (SZ, 'ROOT'): SZ.ROOT, (SZ, 'ADAT'): SZ.ADAT,
        }
        K.ROOT = self.tmp
        K.ADAT = adat
        SZ.ROOT = self.tmp
        SZ.ADAT = adat
        return self.tmp

    def __exit__(self, *exc):
        for (mod, nev), ertek in self._eredeti.items():
            setattr(mod, nev, ertek)
        shutil.rmtree(self.tmp, ignore_errors=True)
        return False


def _ir(gyoker, relut, tartalom):
    teljes = os.path.join(gyoker, relut)
    konyvtar = os.path.dirname(teljes)
    if konyvtar and not os.path.isdir(konyvtar):
        os.makedirs(konyvtar)
    with open(teljes, 'w', encoding='utf-8') as f:
        f.write(tartalom)
    return relut.replace(os.sep, '/')


SABLON_7_OSZLOPOS = (
    "# 4. PaRDeS tematikus sablon\n\n"
    "## 1. Előfordulások összegyűjtése\n\n"
    "| Igehely | Kapcsolódás | PaRDeS-szint, ahol felmerült | Strong-szám(ok) "
    "| BDB-entry-id | Sense-szám | Jelentés-szöveg (BDB eredeti + magyar) |\n"
    "|---|---|---|---|---|---|---|\n"
    "| *(igehely)* | *(...)* | *(...)* | *(...)* | *(...)* | *(...)* | *(...)* |\n\n"
    "## 2. Eredeti nyelvi összevetés\n"
)


class E2Teszt(unittest.TestCase):
    """2026.09.10-es incidens: lefuttatatlan lekerdezes 'ellenőrizve'
    jelolessel, proveniencia-sor nelkul."""

    def test_pozitiv_jeloles_proveniencia_nelkul(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'motivumlog/teszt.md', (
                "## Szakasz\n\n"
                "1Krón 16:8 → Zsolt 105:15 — 🔍 STEPBible-ellenőrizve, releváns.\n"
            ))
            talalatok = SZ.e2_ellenorizve_proveniencia([rel])
            self.assertEqual(len(talalatok), 1)
            self.assertEqual(talalatok[0].sor, 3)

    def test_negativ_proveniencia_sorral(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'motivumlog/teszt.md', (
                "## Szakasz\n\n"
                "scope=range:1Móz 1:1 | forras=TAHOT_kivonat.tsv | ts=2026-09-10T10:00Z\n"
                "1Krón 16:8 → Zsolt 105:15 — 🔍 STEPBible-ellenőrizve, releváns.\n"
            ))
            talalatok = SZ.e2_ellenorizve_proveniencia([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_sima_ellenorizve_szo_d10(self):
        """D10: a sima 'ellenőrizve' szo (jelzoku nelkul) nem szamit."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'motivumlog/teszt.md', (
                "## Szakasz\n\nEz a mondat ellenőrizve lett, de nincs kulon jelzes.\n"
            ))
            talalatok = SZ.e2_ellenorizve_proveniencia([rel])
            self.assertEqual(talalatok, [])


class E3Teszt(unittest.TestCase):
    def test_pozitiv_ures_proveniencia(self):
        with _IdeiglenesGyoker() as gy:
            os.makedirs(os.path.join(gy, 'adat'), exist_ok=True)
            _ir(gy, 'adat/elofordulasok.tsv', (
                "# fejlec\n"
                "id\tigehely\tproveniencia\n"
                "TEREMT-001\t1Móz 1:2\t\n"
            ))
            talalatok = SZ.e3_proveniencia_mezo_ures_vagy_ellenorizve(['__TELJES__'])
            self.assertEqual(len(talalatok), 1)
            self.assertEqual(talalatok[0].sor, 3)

    def test_negativ_kitoltott_proveniencia(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/elofordulasok.tsv', (
                "# fejlec\n"
                "id\tigehely\tproveniencia\n"
                "TEREMT-001\t1Móz 1:2\tscope=x | forras=y | ts=2026-09-10T10:00Z\n"
            ))
            talalatok = SZ.e3_proveniencia_mezo_ures_vagy_ellenorizve(['__TELJES__'])
            self.assertEqual(talalatok, [])


class E4Teszt(unittest.TestCase):
    def test_pozitiv_nincs_naplo(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/auditok.tsv', "id\tlepes\tproveniencia\tdatum\nTEREMT-003\tB3\tscope=x\t2026.09.20\n")
            _ir(gy, 'adat/jeloltek.tsv', "id\tigehely\tdontes\n")
            talalatok = SZ.e4_teljes_scan_naplo_es_dontes(['__TELJES__'])
            self.assertEqual(len(talalatok), 1)
            self.assertIn('TEREMT-003', talalatok[0].reszlet)

    def test_negativ_naplo_es_dontes_megvan(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/auditok.tsv', "id\tlepes\tproveniencia\tdatum\nTEREMT-003\tB3\tscope=x\t2026.09.20\n")
            _ir(gy, 'adat/jeloltek.tsv', "id\tigehely\tdontes\nTEREMT-003\t1Móz 1:2\tbekerult\n")
            _ir(gy, 'genezis/naplok/x_kereszthivatkozas_naplo.md', "TEREMT-003 lezarva.\n")
            talalatok = SZ.e4_teljes_scan_naplo_es_dontes(['__TELJES__'])
            self.assertEqual(talalatok, [])


class E6Teszt(unittest.TestCase):
    def test_pozitiv_hianyzo_forras_szakasz(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'sablonok/4_PaRDeS_tematikus_sablon.md', SABLON_7_OSZLOPOS)
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', "# Proba\n\n## 1. Előfordulások összegyűjtése\n")
            talalatok = SZ.e6_tematikus_forras_es_tabla([rel])
            self.assertTrue(any('Forrás-összegyűjtés' in t.reszlet for t in talalatok))

    def test_negativ_megvan_a_szakasz_es_a_tabla_egyezik(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'sablonok/4_PaRDeS_tematikus_sablon.md', SABLON_7_OSZLOPOS)
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', (
                "# Proba\n\n## 0. Forrás-összegyűjtés a meglévő anyagból\n\nszoveg\n\n"
                + SABLON_7_OSZLOPOS.split('## 1.', 1)[1].join(['## 1.', ''])
            ))
            talalatok = SZ.e6_tematikus_forras_es_tabla([rel])
            self.assertEqual(talalatok, [])


class E7Teszt(unittest.TestCase):
    def test_pozitiv_bekerult_csak_prozaban(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/jeloltek.tsv', "id\tigehely\tdontes\nTEREMT-001\t1Móz 3:16\tbekerult\n")
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', (
                "## 1. Előfordulások\n\n"
                "| Igehely | X |\n|---|---|\n| 1Móz 3:17 | y |\n\n"
                "A szövegben említve: 1Móz 3:16 is idetartozik.\n"
            ))
            talalatok = SZ.e7_bekerult_de_nincs_tablaban([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_bekerult_a_tablaban_is(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/jeloltek.tsv', "id\tigehely\tdontes\nTEREMT-001\t1Móz 3:16\tbekerult\n")
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', (
                "## 1. Előfordulások\n\n| Igehely | X |\n|---|---|\n| 1Móz 3:16 | y |\n"
            ))
            talalatok = SZ.e7_bekerult_de_nincs_tablaban([rel])
            self.assertEqual(talalatok, [])


class E8Teszt(unittest.TestCase):
    def test_pozitiv_tiltott_format(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "Lásd 1 Móz 3:16 és ApCsel. 2:1.\n")
            talalatok = SZ.e8_igehely_format([rel])
            self.assertGreaterEqual(len(talalatok), 2)

    def test_negativ_helyes_format(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "Lásd 1Móz 3:16 és ApCsel 2:1.\n")
            talalatok = SZ.e8_igehely_format([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_backtickes_szabalyleiro_sor_d16(self):
        """D16: a F02_CI_ELLENORZES_BRIEF.md-fele szabalyleiro sor, ahol a
        tiltott minta csak peldakent, backtickben szerepel, nem talalat."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'F02_CI_ELLENORZES_BRIEF.md', (
                "| E8 | Igehely-formátum: `1 Móz`, `1. Móz`, `ApCsel. ` stb. "
                "tiltott; helyes: `1Móz 2:7` | study-rules | HIBA |\n"
            ))
            talalatok = SZ.e8_igehely_format([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_kodblokkban_d16(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "```\n1 Móz 3:16\n```\n")
            talalatok = SZ.e8_igehely_format([rel])
            self.assertEqual(talalatok, [])


class E9Teszt(unittest.TestCase):
    def test_pozitiv_angol_sense(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/proba.md', "A sense-szám mező kitöltendő.\n")
            talalatok = SZ.e9_angol_sense([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_blockquote_kizarva_d11(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/proba.md', '> "be left over" in this sense\n')
            talalatok = SZ.e9_angol_sense([rel])
            self.assertEqual(talalatok, [])


class E10Teszt(unittest.TestCase):
    """D17: E10 hatokore adat/ es lexikon/ -- a gyoker brief-/tervfajlok
    (ahol a szabaly sajat magat dokumentalja peldakent) kizarva."""

    def test_pozitiv_spirit_lelek_lexikonban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', 'A spirit szót itt lélek-nek fordítottuk.\n')
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(len(talalatok), 1)

    def test_pozitiv_spirit_lelek_adatban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'adat/terminologia.tsv', "angol\tmagyar\nspirit\tlélek\n")
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_szellem_forditas(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', 'A spirit szót itt szellem-nek fordítottuk.\n')
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_hatokoron_kivul_d17(self):
        """A gyoker F05_SZOTAR_BRIEF.md-fele sor, ahol a szabaly sajat magat
        dokumentalja, nincs a D17 hatokorben."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'F05_SZOTAR_BRIEF.md', (
                "induló sorok: spirit = szellem, spiritual = szellemi, soul = lélek.\n"
            ))
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(talalatok, [])

    def test_pozitiv_idezojeles_glossza_d17a(self):
        """D17a: az idezojel-kizarast a D17a visszavonta -- a lexikon a
        magyar glosszat idezojelben adja, ezt nem szabad elrejteni."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', 'pneuma: „lélek” (spirit)\n')
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(len(talalatok), 1)

    def test_pozitiv_blockquote_d17a(self):
        """D17a: a blockquote-kizarast a D17a visszavonta -- a Thayer-forditas
        (#7) blockquote-ban renderel, ezt nem szabad elrejteni."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', '> pneuma: spirit, azaz lélek\n')
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_inline_kod_kizarva_d17a(self):
        """D17a: kizarolag az inline kod marad kizarva."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', 'Lásd: `spirit -> lélek` (kódpélda).\n')
            talalatok = SZ.e10_spirit_lelek([rel])
            self.assertEqual(talalatok, [])


class E11Teszt(unittest.TestCase):
    def test_pozitiv_cremer_lexikonban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', "Forrás: Cremer (1895).\n")
            talalatok = SZ.e11_cremer_nidntte_nidotte([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_hatokoron_kivul_d12(self):
        """D12: a hatokoron kivuli (pl. brief-) fajlban a Cremer emlites nem szamit."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'CREMER_OCR_BRIEF.md', "A Cremer szotar OCR-javitasa.\n")
            talalatok = SZ.e11_cremer_nidntte_nidotte([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_blockquote_lexikonban_d12(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'lexikon/PROBA-001_TORZSCIKK.md', "> idézet: Cremer szerint...\n")
            talalatok = SZ.e11_cremer_nidntte_nidotte([rel])
            self.assertEqual(talalatok, [])


class E12Teszt(unittest.TestCase):
    def test_pozitiv_proveniencia_prozaban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'motivumlog/proba.md', "2026.09.10-én az audit során felismerve, l. 3. pont.\n")
            talalatok = SZ.e12_proveniencia_prozaban([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_naplo_blokkban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'motivumlog/proba.md', "【NAPLO: 2026.09.10-én lefutott lekérdezés.】\n")
            talalatok = SZ.e12_proveniencia_prozaban([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_hatokoron_kivul_d13(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'F8_BRIEF.md', "2026.09.10-én az audit során felismerve.\n")
            talalatok = SZ.e12_proveniencia_prozaban([rel])
            self.assertEqual(talalatok, [])


class E13Teszt(unittest.TestCase):
    def test_pozitiv_kiejtes_hianya(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "A תֹהוּ szó jelentése pusztaság.\n")
            talalatok = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_kotojeles_atirassal(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "A תֹהוּ – tohu szó jelentése pusztaság.\n")
            talalatok = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_veszos_atirassal_zarojelben_d13(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "A תֹהוּ (H8414, tohu) szó jelentése pusztaság.\n")
            talalatok = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual(talalatok, [])

    def test_negativ_step_pontozott_atirassal_d13(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'genezis/proba.md', "A תֹהוּ szó, te.hom, jelentése pusztaság.\n")
            talalatok = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual(talalatok, [])


class E14Teszt(unittest.TestCase):
    """D15: bizonyitando, hogy a szabaly egyaltalan talal."""

    def test_pozitiv_angol_jelentes_szoveg(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', (
                "## 1. Előfordulások összegyűjtése\n\n"
                "| Igehely | Kapcsolódás | PaRDeS-szint, ahol felmerült | Strong-szám(ok) "
                "| BDB-entry-id | Sense-szám | Jelentés-szöveg (BDB eredeti + magyar) |\n"
                "|---|---|---|---|---|---|---|\n"
                "| 1Móz 3:16 | x | Peshat | H1234 | H1234 | 1 | be left over and out of the it "
                "in on for and or is are be with as by at from that this not no into up down |\n"
            ))
            talalatok = SZ.e14_jelentes_szoveg_angol([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_magyar_jelentes_szoveg(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', (
                "## 1. Előfordulások összegyűjtése\n\n"
                "| Igehely | Kapcsolódás | PaRDeS-szint, ahol felmerült | Strong-szám(ok) "
                "| BDB-entry-id | Sense-szám | Jelentés-szöveg (BDB eredeti + magyar) |\n"
                "|---|---|---|---|---|---|---|\n"
                "| 1Móz 3:16 | x | Peshat | H1234 | H1234 | 1 | hátramarad, megmarad |\n"
            ))
            talalatok = SZ.e14_jelentes_szoveg_angol([rel])
            self.assertEqual(talalatok, [])


class E15Teszt(unittest.TestCase):
    """D15: bizonyitando, hogy a szabaly egyaltalan talal."""

    def test_pozitiv_25_szonal_hosszabb_idezet(self):
        hosszu = ' '.join(['szo%d' % i for i in range(30)])
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/proba.md', 'SzPA szerint: "%s"\n' % hosszu)
            talalatok = SZ.e15_szpa_idezet_hossz([rel])
            self.assertEqual(len(talalatok), 1)

    def test_negativ_rovid_idezet(self):
        rovid = ' '.join(['szo%d' % i for i in range(10)])
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/proba.md', 'SzPA szerint: "%s"\n' % rovid)
            talalatok = SZ.e15_szpa_idezet_hossz([rel])
            self.assertEqual(talalatok, [])


class E16Teszt(unittest.TestCase):
    def test_pozitiv_onmodositas_jeloles_nelkul(self):
        talalatok = SZ.e16_ellenorzo_onmodositas(
            ['eszkozok/ellenorzes/szabalyok.py'], pr_cim='Uj szabaly hozzaadasa'
        )
        self.assertEqual(len(talalatok), 1)

    def test_negativ_ellenorzo_jelolessel(self):
        talalatok = SZ.e16_ellenorzo_onmodositas(
            ['eszkozok/ellenorzes/szabalyok.py'], pr_cim='[ELLENŐRZŐ] Uj szabaly hozzaadasa'
        )
        self.assertEqual(talalatok, [])

    def test_negativ_nem_erinti_az_ellenorzot(self):
        talalatok = SZ.e16_ellenorzo_onmodositas(
            ['genezis/proba.md'], pr_cim='Study frissites'
        )
        self.assertEqual(talalatok, [])


class E5CimAtszamozasTeszt(unittest.TestCase):
    """E5: a pontcimek atszamozasa (16.x -> 22.x) nem torles; a szoveg
    valtozasa vagy a tenyleges torles az."""

    def test_atszamozas_nem_torles(self):
        self.assertEqual(SZ._tenylegesen_torolt_cimsorok(
            ['### 16.0 Felmérés és előkészítés', '## A FELADATOK.md #16 sorának mezője'],
            ['### 22.0 Felmérés és előkészítés', '## A FELADATOK.md #22 sorának mezője']), [])

    def test_szovegvaltozas_torles(self):
        self.assertEqual(SZ._tenylegesen_torolt_cimsorok(
            ['### 16.1 Prompt és kapu'], ['### 22.1 Prompt']), ['### 16.1 Prompt és kapu'])

    def test_szintvaltas_es_darabszam(self):
        self.assertEqual(len(SZ._tenylegesen_torolt_cimsorok(
            ['### 1 A', '### 2 A'], ['### 3 A'])), 1)
        self.assertEqual(len(SZ._tenylegesen_torolt_cimsorok(
            ['### 1 A'], ['## 1 A'])), 1)


class D8DiffHatokorTeszt(unittest.TestCase):
    """D8: a HIBA csak a diff altal hozzaadott sorra vonatkozik, a fajl
    regi sorai csak JELENTES-t kapnak."""

    def test_git_diff_hozzaadott_sorok_uj_es_regi_sor(self):
        gy = tempfile.mkdtemp(prefix='ci_teszt_git_')
        try:
            import subprocess
            subprocess.check_call(['git', 'init', '-q'], cwd=gy)
            subprocess.check_call(['git', 'config', 'user.email', 'x@x.hu'], cwd=gy)
            subprocess.check_call(['git', 'config', 'user.name', 'x'], cwd=gy)
            _ir(gy, 'proba.md', "a\nb\nc\n")
            subprocess.check_call(['git', 'add', '.'], cwd=gy)
            subprocess.check_call(['git', 'commit', '-q', '-m', 'elso'], cwd=gy)
            _ir(gy, 'proba.md', "a\nX\nb\nc\n")
            subprocess.check_call(['git', 'add', '.'], cwd=gy)
            subprocess.check_call(['git', 'commit', '-q', '-m', 'masodik'], cwd=gy)

            eredeti_root = K.ROOT
            K.ROOT = gy
            try:
                sorok = K.git_diff_hozzaadott_sorok('HEAD~1', 'HEAD', 'proba.md')
            finally:
                K.ROOT = eredeti_root
            self.assertEqual(sorok, {2})
        finally:
            shutil.rmtree(gy, ignore_errors=True)


class E16EsemenyTest(unittest.TestCase):
    """Az E16 push-esemenynel (ures PR-cim) nem ertelmezett; a PR-en fut."""

    FAJLOK = ['.github/workflows/ellenorzes.yml', 'eszkozok/ellenoriz.py']

    def _hiba(self, **kw):
        import futtat as FU
        eredmeny = FU.fut(self.FAJLOK, False, **kw)
        return eredmeny, FU

    def test_push_ures_cimmel_nem_piros(self):
        eredmeny, FU = self._hiba(pr_cim='', esemeny='push')
        self.assertEqual([t for t in eredmeny['E16'] if t.szint == 'HIBA'], [])
        szoveg, hiba_van = FU.jelentes_szoveg(eredmeny, False, 3, 'push')
        self.assertIn('E16: push-esemény, nem értelmezett (a PR-en fut)', szoveg)
        self.assertFalse(hiba_van)  # az összesített jelentés sem piros

    def test_pr_cim_nelkul_piros(self):
        eredmeny, _ = self._hiba(pr_cim='', esemeny='pull_request')
        self.assertTrue([t for t in eredmeny['E16'] if t.szint == 'HIBA'])

    def test_esemeny_megadasa_nelkul_piros(self):
        eredmeny, _ = self._hiba(pr_cim='')
        self.assertTrue([t for t in eredmeny['E16'] if t.szint == 'HIBA'])

    def test_pr_ellenorzo_cimmel_zold(self):
        eredmeny, _ = self._hiba(pr_cim='[ELLENŐRZŐ] valami', esemeny='pull_request')
        self.assertEqual([t for t in eredmeny['E16'] if t.szint == 'HIBA'], [])


class BeerkezoKizarasTest(unittest.TestCase):
    """F20 B6: a beerkezo/ minden szabalybol kimarad."""

    def test_kizart_e(self):
        self.assertTrue(K.kizart_e('beerkezo/valami_BRIEF.md'))
        self.assertTrue(K.kizart_e('beerkezo/README.md'))
        self.assertFalse(K.kizart_e('F20_BEFOGADAS_BRIEF.md'))


class E19Teszt(unittest.TestCase):
    """F28_EMELES_BRIEF.md E6: Thayer/BDB szotari hivatkozas forditas nelkul."""

    LEX = (
        "# szotari hivatkozasok\n"
        "strong\tszotar\tentry_id\tjelentes_szam\tszoveg_en\tforrasfajl\n"
        "G0012\tThayer\tG12\tteljes\tx\tk\n"
        "H7121\tBDB\tH7121\t2.c\tx\tk\n"
        "G1941\tTBESG\tG1941\t1\tx\tk\n"
    )
    FEJ = "szotar\tstrong\tentry_id\tjelentes_szam\tmezo\tforras_hash\tforditas_hu\tallapot\n"

    def _futtat(self, ford_sorok, fajlok=('adat/forditasok.tsv',)):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/lexikon_hivatkozasok.tsv', self.LEX)
            _ir(gy, 'adat/forditasok.tsv', "# gyorsitotar\n" + self.FEJ + ''.join(ford_sorok))
            return SZ.e19_szotari_forditas_hiany(list(fajlok))

    def test_negativ_minden_megvan(self):
        t = self._futtat([
            "Thayer\tG0012\tG12\tteljes\tforditas_hu\th\tf\topus\n",
            "BDB\tH7121\tH7121\tteljes\tforditas_hu\th\tf\tkezi\n",  # teljes fedi a 2.c-t
        ])
        self.assertEqual(t, [])

    def test_pozitiv_direkt_hianyzo_sor(self):
        # a G0012 forditasa hianyzik -> HIBA a lexikon_hivatkozasok 3. soran
        t = self._futtat(["BDB\tH7121\tH7121\t2.c\tforditas_hu\th\tf\tkezi\n"])
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0].szabaly, 'E19')
        self.assertEqual(t[0].szint, 'HIBA')
        self.assertEqual(t[0].sor, 3)

    def test_pozitiv_pilot_allapot_nem_eleg(self):
        t = self._futtat([
            "Thayer\tG0012\tG12\tteljes\tforditas_hu\th\tf\tpilot\n",
            "BDB\tH7121\tH7121\t2.c\tforditas_hu\th\tf\tkezi\n",
        ])
        self.assertEqual(len(t), 1)

    def test_nem_fut_ha_a_tablak_nem_valtoztak(self):
        t = self._futtat([], fajlok=('lexikon/X.md',))
        self.assertEqual(t, [])

    def test_teljes_modban_fut(self):
        # ELLENOR_F28 2. tetel: a futtat.py --teljes modja az E19-nek is a
        # '__TELJES__' jelzot adja; korabban az md-lista miatt el sem indult.
        import futtat as FU
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/lexikon_hivatkozasok.tsv', self.LEX)
            _ir(gy, 'adat/forditasok.tsv', "# gyorsitotar\n" + self.FEJ
                + "BDB\tH7121\tH7121\t2.c\tforditas_hu\th\tf\tkezi\n")
            eredmeny = FU.fut([], True)
        self.assertEqual(len(eredmeny['E19']), 1)
        self.assertEqual(eredmeny['E19'][0].sor, 3)
        self.assertEqual(eredmeny['E19'][0].szint, 'JELENTES')  # --teljes: minden JELENTES

    def test_teljes_jelzo_kozvetlenul(self):
        t = self._futtat(["BDB\tH7121\tH7121\t2.c\tforditas_hu\th\tf\tkezi\n"], fajlok=('__TELJES__',))
        self.assertEqual(len(t), 1)


class E25Teszt(unittest.TestCase):
    """F51 K3: a dontes_hatas.tsv alapu atvezetes-ellenorzes (E25)."""

    FEJ = ("dontes_forras\tdatum\terintett_fajl\ttilos_minta\tatmeneti_jeloles"
           "\ttovabbvivo_feladat\tmegjegyzes\n")
    FORRAS = "# dontesek\n| D34 | motivumonkent egy forras |\n"

    def _sor(self, erintett='ERINTETT.md', minta='regi allapot', atm='', tv='11',
             forras='FORRAS_BRIEF.md#D34', datum='2026-09-30'):
        return '\t'.join([forras, datum, erintett, minta, atm, tv, 'teszt']) + '\n'

    def _futtat(self, tabla_sorok, erintett_szoveg="regi allapot itt\n", brief_allapot='brief_kell',
                ma=None, extra=None, forras_szoveg=None):
        import datetime
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/dontes_hatas.tsv', "# komment\n" + self.FEJ + ''.join(tabla_sorok))
            _ir(gy, 'FORRAS_BRIEF.md', self.FORRAS if forras_szoveg is None else forras_szoveg)
            _ir(gy, 'ERINTETT.md', erintett_szoveg)
            _ir(gy, 'F11_X_BRIEF.md', "---\nfeladat: 11\nallapot: %s\n---\n" % brief_allapot)
            for rel, szoveg in (extra or {}).items():
                _ir(gy, rel, szoveg)
            regi = SZ.MA
            SZ.MA = ma or datetime.date(2026, 10, 5)
            try:
                return SZ.e25_dontes_atvezetes(['__TELJES__'])
            finally:
                SZ.MA = regi

    def test_negativ_nincs_regi_allapot(self):
        t = self._futtat([self._sor()], erintett_szoveg="uj allapot\n")
        self.assertEqual(t, [])

    def test_pozitiv_regi_allapot_figyelmeztetes(self):
        t = self._futtat([self._sor()])
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0].szabaly, 'E25')
        self.assertEqual(t[0].szint, 'FIGYELMEZTETES')
        self.assertEqual((t[0].fajl, t[0].sor), ('ERINTETT.md', 1))

    def test_atmeneti_jeloles_jelentes(self):
        t = self._futtat([self._sor(atm='Atmenet')], erintett_szoveg="regi allapot\nAtmenet (D34)\n")
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0].szint, 'JELENTES')

    def test_atmeneti_jeloles_hianyzik_a_fajlbol(self):
        t = self._futtat([self._sor(atm='Atmenet')])
        self.assertEqual(t[0].szint, 'FIGYELMEZTETES')

    def test_archiv_fajl_kimarad(self):
        archiv = "---\ntipus: archiv\n---\nregi allapot\n"
        t = self._futtat([self._sor()], erintett_szoveg=archiv)
        self.assertEqual(t, [])

    def test_nem_archiv_tipus_nem_marad_ki(self):
        t = self._futtat([self._sor()], erintett_szoveg="---\ntipus: feladat\n---\nregi allapot\n")
        self.assertEqual(len(t), 1)

    def test_b_regota_all_a_tovabbvivo(self):
        import datetime
        t = self._futtat([self._sor()], erintett_szoveg="uj\n", ma=datetime.date(2026, 10, 15))
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0].szint, 'FIGYELMEZTETES')
        self.assertEqual(t[0].fajl, 'adat/dontes_hatas.tsv')

    def test_b_pont_14_nap_meg_nem(self):
        import datetime
        t = self._futtat([self._sor()], erintett_szoveg="uj\n", ma=datetime.date(2026, 10, 14))
        self.assertEqual(t, [])

    def test_b_lezart_tovabbvivo_nem_szol(self):
        import datetime
        t = self._futtat([self._sor()], erintett_szoveg="uj\n", brief_allapot='lezarva',
                         ma=datetime.date(2026, 12, 1))
        self.assertEqual(t, [])

    def test_b_ures_tovabbvivo_nem_szol(self):
        import datetime
        t = self._futtat([self._sor(tv='')], erintett_szoveg="uj\n", ma=datetime.date(2026, 12, 1))
        self.assertEqual(t, [])

    def test_c_hianyzo_forrasfajl_hiba(self):
        t = self._futtat([self._sor(forras='NINCS_BRIEF.md#D34')], erintett_szoveg="uj\n")
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_c_hianyzo_azonosito_hiba(self):
        t = self._futtat([self._sor(forras='FORRAS_BRIEF.md#D99')], erintett_szoveg="uj\n")
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_c_hianyzo_erintett_fajl_hiba(self):
        t = self._futtat([self._sor(erintett='NINCS.md')])
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_c_hibas_regex_hiba(self):
        t = self._futtat([self._sor(minta='(nyitott')])
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_c_hibas_datum_hiba(self):
        t = self._futtat([self._sor(datum='tegnap')])
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_futtat_teljes_modban_jelentes_es_nincs_hiba(self):
        import futtat as FU
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/dontes_hatas.tsv', "# k\n" + self.FEJ + self._sor())
            _ir(gy, 'FORRAS_BRIEF.md', self.FORRAS)
            _ir(gy, 'ERINTETT.md', "regi allapot\n")
            eredmeny = FU.fut([], True)
        self.assertEqual(len(eredmeny['E25']), 1)
        self.assertEqual(eredmeny['E25'][0].szint, 'JELENTES')  # --teljes: minden JELENTES

    def test_futtat_valtozott_modban_megorzi_a_szintet(self):
        import futtat as FU
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/dontes_hatas.tsv', "# k\n" + self.FEJ + self._sor())
            _ir(gy, 'FORRAS_BRIEF.md', self.FORRAS)
            _ir(gy, 'ERINTETT.md', "regi allapot\n")
            eredmeny = FU.fut(['ERINTETT.md'], False)
        self.assertEqual([x.szint for x in eredmeny['E25']], ['FIGYELMEZTETES'])

    def test_valodi_tabla_nincs_hiba(self):
        # a repo tenyleges dontes_hatas.tsv-je: nulla HIBA (a jelenlegi main-en)
        t = SZ.e25_dontes_atvezetes(['__TELJES__'])
        self.assertEqual([x for x in t if x.szint == 'HIBA'], [])


class E27Teszt(unittest.TestCase):
    """F40: hivatkozas-ellenorzes (A-E)."""

    JO = (
        "# FELADATOK.md\n\n## 1. fazis\n"
        "| 1 | Valami | `adat/SEMA.md` | `claude/nyitott-ag` | abc1234 |\n"
        "\n## Kész (utolsó 2 hét)\n"
        "| 2 | Régi | `claude/torolt-ag` |\n"
    )

    def setUp(self):
        self._eredeti = (SZ._e27_tavoli_agak, SZ._e27_commit_van, SZ._e27_diff_statusz)
        SZ._e27_tavoli_agak = lambda: {'main', 'claude/nyitott-ag'}
        SZ._e27_commit_van = lambda az: az == 'abc1234'
        SZ._e27_diff_statusz = lambda b, h: {}

    def tearDown(self):
        SZ._e27_tavoli_agak, SZ._e27_commit_van, SZ._e27_diff_statusz = self._eredeti

    def _fut(self, feladatok, extra=None, **kw):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/SEMA.md', 'x\n')
            if feladatok.startswith('@CRLF@'):
                with open(os.path.join(gy, 'FELADATOK.md'), 'wb') as f:
                    f.write(feladatok[6:].replace(chr(10), chr(13) + chr(10)).encode('utf-8'))
            else:
                _ir(gy, 'FELADATOK.md', feladatok)
            for ut, tart in (extra or {}).items():
                _ir(gy, ut, tart)
            kw.setdefault('base_ref', 'A')
            kw.setdefault('head_ref', 'B')
            return SZ.e27_hivatkozas(**kw)

    def _kilepes(self, talalatok):
        import futtat as FU
        return 1 if any(t.szint == 'HIBA' for t in talalatok) else 0

    def test_jo_feladatkovetes_nincs_talalat_es_a_kilepes_0(self):
        # a Kész szakasz törölt ága csak figyelmeztetés
        t = self._fut(self.JO)
        self.assertEqual([(x.szint, x.sor) for x in t], [('FIGYELMEZTETES', 7)])
        self.assertEqual(self._kilepes(t), 0)

    def test_a_hianyzo_fajl_hiba(self):
        t = self._fut(self.JO + "\n| 3 | `adat/nincs.tsv` |\n")
        h = [x for x in t if x.szint == 'HIBA']
        self.assertEqual(len(h), 1)
        self.assertIn('adat/nincs.tsv', h[0].reszlet)
        self.assertEqual(self._kilepes(t), 1)

    def test_csak_chatben_sor_nem_ad_a_hibat(self):
        t = self._fut(self.JO + "\n| 3 | `F99_X_BRIEF.md` (csak chatben) |\n")
        self.assertEqual([x for x in t if x.szint == 'HIBA'], [])

    def test_torolt_ag_nyitott_sorban_hiba(self):
        t = self._fut("| 1 | `claude/torolt-ag` |\n")
        self.assertEqual([x.szint for x in t], ['HIBA'])
        self.assertEqual(self._kilepes(t), 1)

    def test_torolt_ag_a_kesz_szakaszban_figyelmeztetes(self):
        t = self._fut("## Kész\n| 1 | `claude/torolt-ag` |\n")
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
        self.assertEqual(self._kilepes(t), 0)

    def test_nem_elerheto_tavoli_ag_nem_hiba(self):
        SZ._e27_tavoli_agak = lambda: None
        t = self._fut("| 1 | `claude/valami` |\n")
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])

    def test_c_hianyzo_commit_figyelmeztetes(self):
        t = self._fut("| 1 | deadbe1 |\n")
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
        self.assertIn('deadbe1', t[0].reszlet)

    def test_d_hibas_yaml_fejlec_figyelmeztetes(self):
        t = self._fut('x\n', {'F01_X_BRIEF.md': '---\nfeladat: 1\nolvas: [adat/SEMA.md\n---\n'})
        self.assertEqual([(x.szint, x.fajl) for x in t], [('FIGYELMEZTETES', 'F01_X_BRIEF.md')])
        self.assertIn('hibás', t[0].reszlet)

    def test_d_olvas_hianyzo_fajl_figyelmeztetes_es_ir_nem_ellenorzott(self):
        t = self._fut('x\n', {'F01_X_BRIEF.md':
                              '---\nfeladat: 1\nolvas: [adat/SEMA.md, adat/nincs.md]\nir: [uj/fajl.md]\n---\n'})
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
        self.assertIn('adat/nincs.md', t[0].reszlet)

    def test_e_torolt_fajl_mutato_nelkul_hiba(self):
        SZ._e27_diff_statusz = lambda b, h: {'adat/SEMA.md': 'D'}
        t = self._fut("| 1 | `adat/SEMA.md` |\n", base_ref='A', head_ref='B')
        self.assertEqual([x.szint for x in t], ['HIBA'])
        self.assertIn('ugyanabban a commitban', t[0].reszlet)
        self.assertEqual(self._kilepes(t), 1)

    def test_e_atnevezett_fajl_olvas_mezoben_hiba(self):
        SZ._e27_diff_statusz = lambda b, h: {'adat/SEMA.md': 'R'}
        t = self._fut('x\n', {'F01_X_BRIEF.md': '---\nfeladat: 1\nolvas: [adat/SEMA.md]\n---\n'},
                      base_ref='A', head_ref='B')
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_d8_a_regi_hibas_sor_csak_jelentes(self):
        # a PR nem érinti a hibás sort: JELENTES (nem blokkol)
        eredeti = SZ._e27_hozzaadott_sorok
        SZ._e27_hozzaadott_sorok = lambda b, h, ut: set()
        try:
            t = self._fut("| 1 | `adat/nincs.tsv` |\n", base_ref='A', head_ref='B')
        finally:
            SZ._e27_hozzaadott_sorok = eredeti
        self.assertEqual([x.szint for x in t], ['JELENTES'])
        self.assertEqual(self._kilepes(t), 0)

    def test_crlf_tures(self):
        t = self._fut('@CRLF@' + self.JO)
        self.assertEqual([(x.szint, x.sor) for x in t], [('FIGYELMEZTETES', 7)])

    def test_rovid_alapnev_es_hivatkozas_kivetel(self):
        t = self._fut("| 1 | `SEMA.md` `https://x.y/z` `claude/nyitott-ag` `a/b` |\n")
        self.assertEqual(t, [])

    def test_diff_nelkul_csak_jelentes(self):
        t = self._fut("| 1 | `adat/nincs.tsv` |\n", base_ref=None, head_ref=None)
        self.assertEqual([x.szint for x in t], ['JELENTES'])

    def test_valodi_repo_nincs_kivetel(self):
        # a repo tényleges állapota: lefut, hiba nélkül (a találat lehet JELENTES)
        t = SZ.e27_hivatkozas()
        self.assertTrue(all(x.szabaly == 'E27' for x in t))


if __name__ == '__main__':
    unittest.main()
