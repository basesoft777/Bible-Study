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
import subprocess
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

    # F11 M3 (DT-F11f (2)): az archivum/ kivétel csak az archívumra szól.
    ARCHIV_SOR = '<!-- ARCHÍV: x.md @ 0 · F11 M3 · 2026-10-18 · nem forrás -->\nBDB sense 3, nem sense 2.c.\n'

    def test_negativ_archivum_kizarva(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'archivum/PROBA-001/Proba_tematikus.md', self.ARCHIV_SOR)
            talalatok = SZ.e9_angol_sense([rel])
            self.assertEqual(talalatok, [])

    def test_pozitiv_ugyanaz_tematikus_alatt_hiba(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'tematikus_lezart/Proba_tematikus.md', self.ARCHIV_SOR)
            talalatok = SZ.e9_angol_sense([rel])
            self.assertEqual(len(talalatok), 1)
            self.assertEqual(talalatok[0].szint, 'HIBA')


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

    def test_helyorzo_veglegesre_csereje_nem_torles(self):
        self.assertEqual(SZ._tenylegesen_torolt_cimsorok(
            ['### 2026-10-29 DT-F131q — N-F131a és N-F131b lezárva',
             '## 3. Döntés (DT-F124a)'],
            ['### 2026-10-29 DT406 — N62 és N63 lezárva',
             '## 3. Döntés (DT403)']), [])

    def test_helyorzo_csere_mellett_szovegvaltozas_torles(self):
        self.assertEqual(SZ._tenylegesen_torolt_cimsorok(
            ['## 3. Döntés (DT-F124a)'], ['## 3. Határozat (DT403)']),
            ['## 3. Döntés (DT-F124a)'])


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


class E19SzakaszTeszt(unittest.TestCase):
    """F145 (DT-F142d, 2b): a `teljes` hivatkozast a Strong osszes szotari szakaszat lefedo `sz<n>` sorok is fedik."""

    LEX = (
        "# szotari hivatkozasok\n"
        "strong\tszotar\tentry_id\tjelentes_szam\tszoveg_en\tforrasfajl\n"
        "G0086\tThayer\tG86\tteljes\tx\tk\n"
        "G0540\tThayer\tG540\tteljes\tx\tk\n"
        "H0001\tBDB\tH1\tteljes\tx\tk\n"
    )
    FEJ = "szotar\tstrong\tentry_id\tjelentes_szam\tmezo\tforras_hash\tforditas_hu\tallapot\n"
    THAYER = (
        "# GENERALT: teszt\n"
        "strong\tsorszam\tutvonal\tjel\tszoveg\tillesztes\n"
        "G0086\t1\tcim\t\tG86 - a\tegyezik\n"
        "G0086\t2\t-/1/-\t1.\tb\tegyezik\n"
        "G0086\t3\t-/2/-\t2.\tc\tegyezik\n"
        "G0540\t1\tcim\t\tG540 - d\tegyezik\n"
        "G0540\t2\t-/1/-\t1.\te\tegyezik\n"
    )
    BDB = (
        "# GENERALT: teszt\n# forras: teszt\n"
        "strong\tbdb_id\tsorszam\tutvonal\tjelolo\tjel\tszoveg\tillesztes\n"
        "H0001\tBDB17\t1\tcim\tcim\t\tH1. ab\tegyezik\n"
        "H0001\tBDB17\t2\t-/1/-\tpoint\t1\tfather\tegyezik\n"
    )
    BDB_JAV = ("# GENERALT: teszt\n# forras: teszt\n"
               "strong\tsorszam\tbdb_id\thiba\tszo_sorszam\telofordulas\tforras_alak\tjavitott_alak\tallapot\n")

    @staticmethod
    def _sz(szotar, strong, entry, n, allapot='sonnet'):
        return "%s\t%s\t%s\tsz%d\tforditas_hu\th\tf\t%s\n" % (szotar, strong, entry, n, allapot)

    def _futtat(self, ford_sorok, thayer=True, bdb=True, fajlok=('adat/forditasok.tsv',)):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/lexikon_hivatkozasok.tsv', self.LEX)
            _ir(gy, 'adat/forditasok.tsv', "# gyorsitotar\n" + self.FEJ + ''.join(ford_sorok))
            if thayer:
                _ir(gy, 'adat/thayer_szakaszok.tsv', self.THAYER)
            if bdb:
                _ir(gy, 'adat/bdb_szakaszok.tsv', self.BDB)
                _ir(gy, 'adat/bdb_forras_javitas.tsv', self.BDB_JAV)
            return SZ.e19_szotari_forditas_hiany(list(fajlok))

    def _teljes_ot(self):
        return ([self._sz('Thayer', 'G0086', 'G86', n) for n in (1, 2, 3)]
                + [self._sz('Thayer', 'G0540', 'G540', n, 'kezi') for n in (1, 2)]
                + [self._sz('BDB', 'H0001', 'H1', n, 'opus') for n in (1, 2)])

    def test_negativ_teljes_lefedettseg_fed(self):
        # a #142 esete: a `teljes` hivatkozas sora, a fordito nem `teljes`, hanem szakaszsorokat rogzitett -> nincs talalat
        self.assertEqual(self._futtat(self._teljes_ot()), [])

    def test_pozitiv_hianyzo_szakasz_nem_fed(self):
        sorok = [r for r in self._teljes_ot() if not r.startswith('Thayer\tG0086\tG86\tsz3')]
        t = self._futtat(sorok)
        self.assertEqual([(x.szabaly, x.szint, x.sor) for x in t], [('E19', 'HIBA', 3)])  # G0086: a lexikon_hivatkozasok 3. sora

    def test_pozitiv_reszleges_bdb_lefedettseg_nem_fed(self):
        sorok = [r for r in self._teljes_ot() if not r.startswith('BDB\tH0001\tH1\tsz2')]
        self.assertEqual([x.sor for x in self._futtat(sorok)], [5])

    def test_pozitiv_elavult_es_pilot_szakasz_nem_szamit(self):
        sorok = self._teljes_ot()
        sorok[2] = self._sz('Thayer', 'G0086', 'G86', 3, 'elavult')
        sorok[4] = self._sz('Thayer', 'G0540', 'G540', 2, 'pilot')
        self.assertEqual([x.sor for x in self._futtat(sorok)], [3, 4])

    def test_pozitiv_masik_strong_szakaszai_nem_fednek(self):
        # a G0540 szakaszsorai a G0086 hivatkozasat nem fedik, es forditva
        sorok = [r for r in self._teljes_ot() if r.startswith('Thayer\tG0540')]
        self.assertEqual([x.sor for x in self._futtat(sorok)], [3, 5])

    def test_pozitiv_nincs_szakasztabla_nincs_alap(self):
        # tabla nelkul a szakaszkeszlet ismeretlen: a szakaszsorok nem fedhetik a `teljes` hivatkozast
        self.assertEqual([x.sor for x in self._futtat(self._teljes_ot(), thayer=False, bdb=False)], [3, 4, 5])
        self.assertEqual([x.sor for x in self._futtat(self._teljes_ot(), thayer=False)], [3, 4])

    def test_negativ_nem_teljes_hivatkozas_valtozatlan(self):
        # a nem `teljes` hivatkozast a szakaszok nem fedik (csak az azonos jelentes_szam vagy a `teljes` sor)
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/lexikon_hivatkozasok.tsv', "strong\tszotar\tentry_id\tjelentes_szam\tszoveg_en\tforrasfajl\n"
                "G0086\tThayer\tG86\t1\tx\tk\n")
            _ir(gy, 'adat/forditasok.tsv', "# gy\n" + self.FEJ + ''.join(self._sz('Thayer', 'G0086', 'G86', n) for n in (1, 2, 3)))
            _ir(gy, 'adat/thayer_szakaszok.tsv', self.THAYER)
            self.assertEqual([x.sor for x in SZ.e19_szotari_forditas_hiany(['adat/forditasok.tsv'])], [2])


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
    """F40: hivatkozas-ellenorzes (A-E), a DT-F40a/b dontes szerint. A
    `_kilepes*` segedek a futtat.py VALODI kilepesi kodjat merik (main()),
    nem a talalatok szintjebol szamolnak."""

    # kezzel irt (nem generalt) feladatkovetes
    JO = (
        "# FELADATOK.md\n\n## 1. fazis\n"
        "| 1 | Valami | `adat/SEMA.md` | `claude/nyitott-ag` | abc1234 |\n"
        "\n## Kész (utolsó 2 hét)\n"
        "| 2 | Régi | `claude/torolt-ag` |\n"
    )

    BRIEF1 = '---\nfeladat: 1\nir: [adat/SEMA.md]\nfugg: []\n---\n'

    @staticmethod
    def _gen(nyitott='', kesz=''):
        """Generalt blokkos FELADATOK.md: a nyitott sor az 1. feladaté."""
        return (
            "# FELADATOK.md\n\n## 1. fázis — adatréteg\n\n"
            "<!-- GENERÁLT-KEZDET: feladatok.py --cel fazis1 -->\n"
            "| # | Feladat | Hol |\n|---|---|---|\n"
            "| 1 | Valami | %s |\n"
            "<!-- GENERÁLT-VÉGE: feladatok.py --cel fazis1 -->\n\n"
            "## Kész (utolsó 2 hét)\n\n"
            "<!-- GENERÁLT-KEZDET: feladatok.py --cel kesz -->\n"
            "- Régi (#2): %s\n"
            "<!-- GENERÁLT-VÉGE: feladatok.py --cel kesz -->\n" % (nyitott, kesz)
        )

    def setUp(self):
        self._eredeti = (SZ._e27_tavoli_agak, SZ._e27_commit_van, SZ._e27_diff_statusz)
        SZ._e27_tavoli_agak = lambda: {'main', 'claude/nyitott-ag'}
        SZ._e27_commit_van = lambda az: az == 'abc1234'
        SZ._e27_diff_statusz = lambda b, h: {}

    def tearDown(self):
        SZ._e27_tavoli_agak, SZ._e27_commit_van, SZ._e27_diff_statusz = self._eredeti

    def _fixture(self, gy, feladatok, extra):
        _ir(gy, 'adat/SEMA.md', 'x\n')
        if feladatok.startswith('@CRLF@'):
            with open(os.path.join(gy, 'FELADATOK.md'), 'wb') as f:
                f.write(feladatok[6:].replace(chr(10), chr(13) + chr(10)).encode('utf-8'))
        else:
            _ir(gy, 'FELADATOK.md', feladatok)
        for ut, tart in (extra or {}).items():
            _ir(gy, ut, tart)

    def _fut(self, feladatok, extra=None, **kw):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy, feladatok, extra)
            kw.setdefault('base_ref', 'A')
            kw.setdefault('head_ref', 'B')
            return SZ.e27_hivatkozas(**kw)

    def _kilepes(self, feladatok, extra=None, hozzaadott=None, diff=True):
        """A futtat.py main() VALODI kilepesi kodja (--valtozott, push-esemeny).
        `hozzaadott`: a PR altal hozzaadott sorok halmaza (None = nem allapithato
        meg, a talalat a sajat szintjen marad)."""
        import contextlib
        import io
        import futtat as FU
        eredeti_hs = SZ._e27_hozzaadott_sorok
        eredeti_argv = sys.argv
        eredeti_root = FU.ROOT
        SZ._e27_hozzaadott_sorok = lambda b, h, ut: hozzaadott
        try:
            with _IdeiglenesGyoker() as gy:
                self._fixture(gy, feladatok, extra)
                FU.ROOT = gy
                sys.argv = ['futtat.py', '--valtozott', 'FELADATOK.md', '--esemeny', 'push']
                if diff:
                    sys.argv += ['--diff-alap', 'A', '--diff-fej', 'B']
                with contextlib.redirect_stdout(io.StringIO()):
                    return FU.main()
        finally:
            SZ._e27_hozzaadott_sorok = eredeti_hs
            sys.argv = eredeti_argv
            FU.ROOT = eredeti_root

    # --- DT-F09h: szűk kivétel a gitignore-olt _nyers/ hivatkozásra ------

    def test_nyers_hivatkozas_jelolo_nelkul_hiba(self):
        t = self._fut(self._gen(nyitott='`konkordancia/_nyers/x/y.tsv`'))
        self.assertTrue([x for x in t if x.szint == 'HIBA' and '_nyers/x/y.tsv' in x.reszlet], t)

    def test_nyers_hivatkozas_opcionalis_jelolovel_engedett(self):
        t = self._fut(self._gen(nyitott='`konkordancia/_nyers/x/y.tsv` (opcionális, DT-F09h)'))
        self.assertFalse([x for x in t if '_nyers/x/y.tsv' in x.reszlet], t)

    def test_jelolo_nem_nyers_hivatkozast_nem_ment(self):
        t = self._fut(self._gen(nyitott='`adat/nincs_ilyen.tsv` (opcionális, DT-F09h)'))
        self.assertTrue([x for x in t if x.szint == 'HIBA' and 'nincs_ilyen.tsv' in x.reszlet], t)

    # --- jo eset, "csak chatben" ---------------------------------------

    def test_jo_feladatkovetes_figyelmeztetes_a_keszben_es_a_kilepes_0(self):
        t = self._fut(self.JO)
        self.assertEqual([(x.szint, x.sor) for x in t], [('FIGYELMEZTETES', 7)])
        self.assertEqual(self._kilepes(self.JO), 0)

    def test_csak_chatben_sor_nem_ad_a_hibat_a_generalt_blokkban_sem(self):
        f = self._gen(nyitott='`F99_X_BRIEF.md` (csak chatben)')
        self.assertEqual([x for x in self._fut(f, {'F01_X_BRIEF.md': self.BRIEF1}) if x.szint == 'HIBA'], [])
        self.assertEqual(self._kilepes(f, {'F01_X_BRIEF.md': self.BRIEF1}, hozzaadott=set()), 0)

    # --- DT-F40a (a): a FELADATOK.md generalt blokkjanak nyitott sorai ----

    def test_a_generalt_nyitott_sor_hianyzo_fajl_mindig_hiba_es_nevezi_a_briefet(self):
        f = self._gen(nyitott='`adat/nincs.tsv`')
        for kw in ({'hozzaadott': set()}, {'hozzaadott': None}):
            self.assertEqual(self._kilepes(f, {'F01_X_BRIEF.md': self.BRIEF1}, **kw), 1)
        # diff nelkul (kezi futas) is HIBA, a PR altal nem erintett soron is
        t = self._fut(f, {'F01_X_BRIEF.md': self.BRIEF1}, base_ref=None, head_ref=None)
        h = [x for x in t if x.szint == 'HIBA']
        self.assertEqual(len(h), 1)
        self.assertIn('adat/nincs.tsv', h[0].reszlet)
        self.assertIn('F01_X_BRIEF.md', h[0].reszlet)      # DT-F40a (e)
        self.assertEqual(h[0].fajl, 'FELADATOK.md')

    def test_a_generalt_nyitott_sor_hianyzo_commit_mindig_hiba(self):
        f = self._gen(nyitott='deadbe1')
        t = self._fut(f, {'F01_X_BRIEF.md': self.BRIEF1})
        self.assertEqual([x.szint for x in t], ['HIBA'])
        self.assertIn('F01_X_BRIEF.md', t[0].reszlet)
        self.assertEqual(self._kilepes(f, {'F01_X_BRIEF.md': self.BRIEF1}, hozzaadott=set()), 1)

    def test_a_generalt_nyitott_sor_letezo_commit_nem_hiba(self):
        t = self._fut(self._gen(nyitott='abc1234'), {'F01_X_BRIEF.md': self.BRIEF1})
        self.assertEqual(t, [])

    def test_a_generalt_nyitott_sor_nem_letezo_ag_csak_figyelmeztetes(self):
        # a tervezett (meg nem letezo) ag ervenyes, pl. claude/f38-adag7
        f = self._gen(nyitott='`claude/f38-adag7`')
        t = self._fut(f, {'F01_X_BRIEF.md': self.BRIEF1})
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
        self.assertIn('F01_X_BRIEF.md', t[0].reszlet)
        self.assertEqual(self._kilepes(f, {'F01_X_BRIEF.md': self.BRIEF1}, hozzaadott=set()), 0)

    def test_a_generalt_sor_szama_nem_azonosit_briefet(self):
        t = self._fut(self._gen(nyitott='`adat/nincs.tsv`'))      # nincs brief
        self.assertEqual([x.szint for x in t], ['HIBA'])
        self.assertIn('nem azonosít briefet', t[0].reszlet)

    # --- DT-F40a (c): a Kesz szakasz --------------------------------------

    def test_kesz_szakasz_fajlhiany_figyelmeztetes_a_generalt_blokkban(self):
        f = self._gen(kesz='`adat/nincs.tsv`')
        t = self._fut(f, {'F01_X_BRIEF.md': self.BRIEF1})
        self.assertEqual([(x.szint, x.fajl) for x in t], [('FIGYELMEZTETES', 'FELADATOK.md')])
        self.assertEqual(self._kilepes(f, {'F01_X_BRIEF.md': self.BRIEF1}, hozzaadott=set()), 0)

    def test_kesz_szakasz_torolt_ag_figyelmeztetes(self):
        f = self._gen(kesz='`claude/torolt-ag`')
        t = self._fut(f, {'F01_X_BRIEF.md': self.BRIEF1})
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
        self.assertEqual(self._kilepes(f, {'F01_X_BRIEF.md': self.BRIEF1}), 0)

    def test_kesz_szakasz_kezi_sorban_a_fajlhiany_figyelmeztetes(self):
        t = self._fut("## Kész\n| 1 | `adat/nincs.tsv` |\n")
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])

    # --- DT-F40a (d): minden egyeb diff-hatokoru -------------------------

    def test_a_hianyzo_fajl_kezi_sorban_hiba(self):
        f = self.JO.replace("\n## Kész", "| 3 | `adat/nincs.tsv` |\n\n## Kész")
        t = self._fut(f)
        h = [x for x in t if x.szint == 'HIBA']
        self.assertEqual(len(h), 1)
        self.assertIn('adat/nincs.tsv', h[0].reszlet)
        self.assertEqual(self._kilepes(f), 1)

    def test_torolt_ag_kezi_nyitott_sorban_hiba(self):
        f = "| 1 | `claude/torolt-ag` |\n"
        self.assertEqual([x.szint for x in self._fut(f)], ['HIBA'])
        self.assertEqual(self._kilepes(f), 1)

    def test_torolt_ag_a_kesz_szakaszban_figyelmeztetes(self):
        f = "## Kész\n| 1 | `claude/torolt-ag` |\n"
        self.assertEqual([x.szint for x in self._fut(f)], ['FIGYELMEZTETES'])
        self.assertEqual(self._kilepes(f), 0)

    def test_nem_elerheto_tavoli_ag_nem_hiba(self):
        SZ._e27_tavoli_agak = lambda: None
        f = "| 1 | `claude/valami` |\n"
        self.assertEqual([x.szint for x in self._fut(f)], ['FIGYELMEZTETES'])
        self.assertEqual(self._kilepes(f), 0)

    def test_c_hianyzo_commit_kezi_sorban_figyelmeztetes(self):
        t = self._fut("| 1 | deadbe1 |\n")
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
        self.assertIn('deadbe1', t[0].reszlet)
        self.assertEqual(self._kilepes("| 1 | deadbe1 |\n"), 0)

    def test_d8_a_regi_hibas_kezi_sor_csak_jelentes(self):
        # a PR nem erinti a hibas sort: JELENTES (nem blokkol)
        eredeti = SZ._e27_hozzaadott_sorok
        SZ._e27_hozzaadott_sorok = lambda b, h, ut: set()
        try:
            t = self._fut("| 1 | `adat/nincs.tsv` |\n", base_ref='A', head_ref='B')
        finally:
            SZ._e27_hozzaadott_sorok = eredeti
        self.assertEqual([x.szint for x in t], ['JELENTES'])
        self.assertEqual(self._kilepes("| 1 | `adat/nincs.tsv` |\n", hozzaadott=set()), 0)

    def test_nyitott_feladatok_md_diff_hatokoru(self):
        # NYITOTT_FELADATOK.md: a PR altal hozzaadott soron HIBA, a regi soron JELENTES
        sor = "- hivatkozas: `adat/nincs.tsv`\n"
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'NYITOTT_FELADATOK.md', sor)
            eredeti = SZ._e27_hozzaadott_sorok
            try:
                SZ._e27_hozzaadott_sorok = lambda b, h, ut: {1}
                uj = SZ.e27_hivatkozas('A', 'B')
                SZ._e27_hozzaadott_sorok = lambda b, h, ut: set()
                regi = SZ.e27_hivatkozas('A', 'B')
            finally:
                SZ._e27_hozzaadott_sorok = eredeti
        self.assertEqual([x.szint for x in uj], ['HIBA'])
        self.assertEqual([x.szint for x in regi], ['JELENTES'])

    def test_diff_nelkul_a_kezi_sor_csak_jelentes(self):
        t = self._fut("| 1 | `adat/nincs.tsv` |\n", base_ref=None, head_ref=None)
        self.assertEqual([x.szint for x in t], ['JELENTES'])
        self.assertEqual(self._kilepes("| 1 | `adat/nincs.tsv` |\n", diff=False), 0)

    # --- DT-F40a (b), DT-F40b: a brief `olvas` mezoje --------------------

    def test_olvas_hianyzo_fajl_mindig_hiba(self):
        b = '---\nfeladat: 2\nolvas: [adat/SEMA.md, adat/nincs.md]\nir: [uj/fajl.md]\nfugg: []\n---\n'
        for diff in (True, False):
            t = self._fut('x\n', {'F02_X_BRIEF.md': b}, **({} if diff else {'base_ref': None, 'head_ref': None}))
            self.assertEqual([x.szint for x in t], ['HIBA'])    # az `ir` nem ellenorzott
            self.assertIn('adat/nincs.md', t[0].reszlet)
            self.assertEqual(t[0].sor, 3)
        self.assertEqual(self._kilepes('x\n', {'F02_X_BRIEF.md': b}, hozzaadott=set()), 1)

    def test_olvas_hianyzo_fajl_figyelmeztetes_ha_fugg_feladat_ir_mezoje_fedi(self):
        elo = '---\nfeladat: 5\nir: [naplok/audit.md]\nfugg: []\n---\n'
        b = '---\nfeladat: 6\nolvas: [naplok/audit.md]\nfugg: [5]\n---\n'
        extra = {'F05_ELO_BRIEF.md': elo, 'F06_UTO_BRIEF.md': b}
        t = self._fut('x\n', extra)
        self.assertEqual([(x.szint, x.fajl) for x in t], [('FIGYELMEZTETES', 'F06_UTO_BRIEF.md')])
        self.assertIn('F05_ELO_BRIEF.md', t[0].reszlet)
        self.assertEqual(self._kilepes('x\n', extra), 0)

    def test_olvas_konyvtar_elotag_is_fedi(self):
        elo = '---\nfeladat: 5\nir: [naplok/]\nfugg: []\n---\n'
        b = '---\nfeladat: 6\nolvas: [naplok/audit.md]\nfugg: [5]\n---\n'
        t = self._fut('x\n', {'F05_ELO_BRIEF.md': elo, 'F06_UTO_BRIEF.md': b})
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])

    def test_olvas_figyelmeztetes_ha_barmely_nem_lezart_feladat_ir_mezoje_fedi(self):
        # DT-F40c (b): a fedo feladat nem kell, hogy a `fugg`-ben legyen
        elo = '---\nfeladat: 5\nallapot: nem_indult\nir: [naplok/audit.md]\nfugg: []\n---\n'
        b = '---\nfeladat: 6\nallapot: nem_indult\nolvas: [naplok/audit.md]\nfugg: [7]\n---\n'
        extra = {'F05_ELO_BRIEF.md': elo, 'F06_UTO_BRIEF.md': b}
        t = self._fut('x\n', extra)
        self.assertEqual([(x.szint, x.fajl) for x in t], [('FIGYELMEZTETES', 'F06_UTO_BRIEF.md')])
        self.assertEqual(self._kilepes('x\n', extra), 0)

    def test_olvas_hiba_ha_csak_lezart_feladat_ir_mezoje_fedi(self):
        # DT-F40c (b): a lezart feladat mar nem allitja elo a fajlt
        elo = '---\nfeladat: 5\nallapot: lezarva\nir: [naplok/audit.md]\nfugg: []\n---\n'
        b = '---\nfeladat: 6\nallapot: nem_indult\nolvas: [naplok/audit.md]\nfugg: [5]\n---\n'
        extra = {'F05_ELO_BRIEF.md': elo, 'F06_UTO_BRIEF.md': b}
        self.assertEqual([x.szint for x in self._fut('x\n', extra)], ['HIBA'])
        self.assertEqual(self._kilepes('x\n', extra), 1)

    def test_olvas_jokeres_ir_is_fedi_nyitott_briefnel(self):
        elo = '---\nfeladat: 5\nallapot: fut\nir: [naplok/MF_*.tsv]\nfugg: []\n---\n'
        b = '---\nfeladat: 6\nolvas: [naplok/MF_x.tsv]\n---\n'
        t = self._fut('x\n', {'F05_ELO_BRIEF.md': elo, 'F06_UTO_BRIEF.md': b})
        self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])

    def test_olvas_lezart_brief_hianyzo_fajl_figyelmeztetes(self):
        # DT-F40c (a): az F46 esete, a fedes nem szamit
        b = '---\nfeladat: 6\nallapot: lezarva\nolvas: [adat/SEMA.md, beerkezo/eltunt.md]\nir: [uj/x.md]\nfugg: [4]\n---\n'
        for diff in (True, False):
            t = self._fut('x\n', {'F06_X_BRIEF.md': b}, **({} if diff else {'base_ref': None, 'head_ref': None}))
            self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])
            self.assertIn('beerkezo/eltunt.md', t[0].reszlet)
        self.assertEqual(self._kilepes('x\n', {'F06_X_BRIEF.md': b}), 0)
        self.assertEqual(self._kilepes('x\n', {'F06_X_BRIEF.md': b}, hozzaadott=set()), 0)

    def test_olvas_nyitott_brief_fedetlen_hianyzo_fajl_hiba_kilepes_1(self):
        b = '---\nfeladat: 6\nallapot: fut\nolvas: [beerkezo/eltunt.md]\n---\n'
        self.assertEqual([x.szint for x in self._fut('x\n', {'F06_X_BRIEF.md': b})], ['HIBA'])
        self.assertEqual(self._kilepes('x\n', {'F06_X_BRIEF.md': b}), 1)

    def test_olvas_hiba_ha_a_fugg_feladat_ir_mezeje_nem_fedi(self):
        elo = '---\nfeladat: 5\nir: [mas/fajl.md]\nfugg: []\n---\n'
        b = '---\nfeladat: 6\nolvas: [naplok/audit.md]\nfugg: [5]\n---\n'
        t = self._fut('x\n', {'F05_ELO_BRIEF.md': elo, 'F06_UTO_BRIEF.md': b})
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_hibas_yaml_fejlec_nem_e27_dolga_nincs_talalat_es_kilepes_0(self):
        # DT-F40b: lezaratlan fejlec / lezaratlan lista: az E18 jelez, az E27 hallgat
        for tartalom in ('---\nfeladat: 1\nolvas: [adat/SEMA.md\n---\n',
                         '---\nfeladat: 1\nolvas: [adat/SEMA.md]\n(nincs zaro)\n'):
            t = self._fut('x\n', {'F01_X_BRIEF.md': tartalom})
            self.assertEqual(t, [])
            self.assertEqual(self._kilepes('x\n', {'F01_X_BRIEF.md': tartalom}), 0)

    def test_skalar_olvas_mezo_is_ellenorzott(self):
        t = self._fut('x\n', {'F01_X_BRIEF.md': '---\nfeladat: 1\nolvas: adat/nincs.md\n---\n'})
        self.assertEqual([x.szint for x in t], ['HIBA'])

    # --- E: torles/atnevezes ----------------------------------------------

    def test_e_torolt_fajl_mutato_nelkul_hiba(self):
        SZ._e27_diff_statusz = lambda b, h: {'adat/SEMA.md': 'D'}
        f = "| 1 | `adat/SEMA.md` |\n"
        t = self._fut(f, base_ref='A', head_ref='B')
        self.assertEqual([x.szint for x in t], ['HIBA'])
        self.assertIn('ugyanabban a commitban', t[0].reszlet)
        self.assertEqual(self._kilepes(f), 1)

    def test_e_atnevezett_fajl_olvas_mezoben_hiba(self):
        SZ._e27_diff_statusz = lambda b, h: {'adat/SEMA.md': 'R'}
        b = {'F01_X_BRIEF.md': '---\nfeladat: 1\nolvas: [adat/SEMA.md]\n---\n'}
        t = self._fut('x\n', b, base_ref='A', head_ref='B')
        self.assertEqual([x.szint for x in t], ['HIBA'])
        self.assertEqual(self._kilepes('x\n', b), 1)

    # --- CRLF, kivetelek (a brief 2. pontja es naplok/F40_zaras.md) ---------

    def test_crlf_tures(self):
        t = self._fut('@CRLF@' + self.JO)
        self.assertEqual([(x.szint, x.sor) for x in t], [('FIGYELMEZTETES', 7)])

    def test_kivetel_rovid_alapnev_barmely_azonos_nevu_fajllal(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy, "| 1 | `SEMA.md` `nincs_ilyen.md` |\n", {'mappa/almappa/mas.py': 'x\n'})
            t = SZ.e27_hivatkozas('A', 'B')
        self.assertEqual(len(t), 1)
        self.assertIn('nincs_ilyen.md', t[0].reszlet)      # SEMA.md (adat/SEMA.md) elfogadott
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy, "| 1 | `mas.py` |\n", {'mappa/almappa/mas.py': 'x\n'})
            self.assertEqual(SZ.e27_hivatkozas('A', 'B'), [])   # mas helyen levo azonos nevu fajl

    def test_kivetel_kiterjesztes_nelkuli_a_b_csak_letezo_elso_taggal_utvonal(self):
        # `szervezet/repo` (nem letezo elso tag): nem fajlutvonal; `adat/nincs` (letezo `adat/`): az
        self.assertEqual(self._fut("| 1 | `szervezet/repo` |\n"), [])
        t = self._fut("| 1 | `adat/nincs` |\n")
        self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_kivetel_url_es_ag_nem_fajlutvonal(self):
        t = self._fut("| 1 | `https://x.y/z` `claude/nyitott-ag` `a/b` |\n")
        self.assertEqual(t, [])

    def test_kivetel_beerkezo_es_konkordancia_briefjei_nem_szamitanak_a_d_agban(self):
        rossz = '---\nfeladat: 9\nolvas: [adat/nincs.md]\n---\n'
        t = self._fut('x\n', {'beerkezo/F09_X_BRIEF.md': rossz, 'konkordancia/F09_Y_BRIEF.md': rossz})
        self.assertEqual(t, [])
        t = self._fut('x\n', {'tema/F09_X_BRIEF.md': rossz})
        self.assertEqual([x.szint for x in t], ['HIBA'])    # mas mappa: ellenorzott

    def test_valodi_repo_nincs_kivetel(self):
        # a repo tenyleges allapota: lefut, minden talalat E27
        t = SZ.e27_hivatkozas()
        self.assertTrue(all(x.szabaly == 'E27' for x in t))


# ---------------------------------------------------------------------------
# E28, E29 (F116 -- naplok/MOTIVUM_FORRAS_ci_terv.md 1. es 2. szakasz)
# ---------------------------------------------------------------------------

_LISTA_FEJ = 'id\tfajl\tcel\tmelyseg\tfeladat\tdatum\n'
_LAP = 'lexikon/ZZTESZT-001_TUDOMANYOS.md'


def _lista(*sorok):
    return _LISTA_FEJ + ''.join(sorok)


def _lista_sor(fajl=_LAP, melyseg='apparatus', az='ZZTESZT-001', cel='lexikon'):
    return '%s\t%s\t%s\t%s\tF116-teszt\t2026-10-18\n' % (az, fajl, cel, melyseg)


def _ir_nyers(gyoker, relut, tartalom):
    """Mint a _ir, de a sorvegek valtozatlanok (Windowson sem lesz CRLF az LF-bol):
    az E28 a blob bajtjait veti ossze."""
    teljes = os.path.join(gyoker, relut)
    os.makedirs(os.path.dirname(teljes) or gyoker, exist_ok=True)
    with open(teljes, 'w', encoding='utf-8', newline='') as f:
        f.write(tartalom)
    return relut.replace(os.sep, '/')


def _lista_ir(gy, *sorok):
    _ir(gy, 'eszkozok/ellenorzes/e28_migralt_nezetek.tsv', _lista(*sorok))


_MARKER_BLOKK = (
    '<!-- GENERÁLT-KEZDET: general.py --cel naplo#teszt | forrás: x | ts=2026-10-18 -->\n'
    '\nEgy.\nKetto.\n\n<!-- GENERÁLT-VÉGE: naplo#teszt -->'
)


def _hamis_blokkok(cel):
    return [('naplo#teszt', _MARKER_BLOKK)]


class E28Teszt(unittest.TestCase):
    """E28: a generalt nezet bajtra egyezik az ujragenerálttal. A generator-hivas
    (`_e28_general_futtat`), a commitolt blob (`_e28_commitolt`) és a marker-blokkok
    forrása (`_e28_generalt_blokkok`) a teszt idejére helyettesítve: a fixture ideiglenes
    gyökérben áll, az éles repón nem fut generátor."""

    GEN_FEJ = '<!-- GENERÁLT: general.py --cel lexikon | ts=%s -->\n'

    def _render(self, gy, datum):
        """A "generator": a nezet az adat- es a forrasretegbol (fixture) all elo."""
        adat = open(os.path.join(gy, 'adat', 'elofordulasok.tsv'), encoding='utf-8').read()
        forras = open(os.path.join(gy, 'motivumok', 'ZZTESZT-001.md'), encoding='utf-8').read()
        return (self.GEN_FEJ % datum) + '## 2. Adat\n' + adat + '## 3. Olvasoi\n' + forras

    def _futtat(self, gy, fajlok=('__TELJES__',), marker_celok=()):
        def hamis_generator(cel, azonosito, datum, kimenet):
            ut = os.path.join(kimenet, *_LAP.split('/'))
            os.makedirs(os.path.dirname(ut), exist_ok=True)
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write(self._render(gy, datum))
            return 0, ''

        def blob(relut):
            try:
                with open(os.path.join(gy, *relut.split('/')), encoding='utf-8', newline='') as f:
                    return f.read()    # nyers: a blob sorvegei is szamitanak
            except OSError:
                return None

        from unittest import mock
        with mock.patch.object(SZ, '_e28_general_futtat', hamis_generator), \
                mock.patch.object(SZ, '_e28_commitolt', blob), \
                mock.patch.object(SZ, 'E28_MARKER_CELOK', tuple(marker_celok)), \
                mock.patch.object(SZ, '_e28_generalt_blokkok', _hamis_blokkok):
            return SZ.e28_generalt_nezet_egyezes(list(fajlok))

    def _fixture(self, gy, elof='ZZTESZT-001\t1Móz 1:1\tkapcsolodas: x\n', forras='Olvasoi bekezdes.\n'):
        _ir(gy, 'adat/elofordulasok.tsv', elof)
        _ir(gy, 'motivumok/ZZTESZT-001.md', forras)
        _lista_ir(gy, _lista_sor())
        # a commitolt nezet = a generator kimenete a nezet sajat datumara
        _ir_nyers(gy, _LAP, self._render(gy, '2026-10-01'))

    def test_pozitiv_valtozatlan_forrasbol_generalt_nezet_zold(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            self.assertEqual(self._futtat(gy), [])
            self.assertIn('E28: 1 migrált nézet', SZ.E28_JEGYZETEK)

    def test_pozitiv_marker_blokk_zold(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, 'naplo.md', 'kezi sor\n' + _MARKER_BLOKK.replace('ts=2026-10-18', 'ts=2026-09-15') + '\nkezi vege\n')
            self.assertEqual(self._futtat(gy, marker_celok=[('naplo', 'naplo.md')]), [])

    def test_negativ_a_kezzel_irt_szo_piros(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            szoveg = open(os.path.join(gy, _LAP), encoding='utf-8').read()
            _ir_nyers(gy, _LAP, szoveg.replace('Olvasoi bekezdes.', 'Olvasoi KEZZEL bekezdes.'))
            t = self._futtat(gy)
            self.assertEqual(len(t), 1)
            self.assertEqual((t[0].szabaly, t[0].szint, t[0].fajl), ('E28', 'HIBA', _LAP))
            self.assertIn('Javítás: python eszkozok/general.py --cel lexikon --id ZZTESZT-001 --ir', t[0].reszlet)
            self.assertGreater(t[0].sor, 0)

    def test_negativ_adat_valtozik_a_nezet_nem(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir(gy, 'adat/elofordulasok.tsv', 'ZZTESZT-001\t1Móz 1:1\tkapcsolodas: MODOSITOTT\n')
            t = self._futtat(gy)
            self.assertEqual([x.szabaly for x in t], ['E28'])
            self.assertIn('MODOSITOTT', t[0].reszlet)

    def test_negativ_forras_olvasoi_bekezdese_valtozik_a_nezet_nem(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir(gy, 'motivumok/ZZTESZT-001.md', 'Uj olvasoi bekezdes.\n')
            t = self._futtat(gy)
            self.assertEqual([x.szabaly for x in t], ['E28'])

    def test_negativ_marker_blokk_torzsenek_kezi_atirasa_piros(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            kezi = _MARKER_BLOKK.replace('Ketto.', 'Ketto KEZZEL ATIRVA.')
            _ir_nyers(gy, 'naplo.md', 'kezi sor\n' + kezi + '\n')
            t = self._futtat(gy, marker_celok=[('naplo', 'naplo.md')])
            self.assertEqual(len(t), 1)
            self.assertEqual((t[0].fajl, t[0].szint), ('naplo.md', 'HIBA'))
            self.assertIn('naplo#teszt', t[0].reszlet)
            self.assertIn('python eszkozok/general.py --cel naplo --ir', t[0].reszlet)
            self.assertEqual(t[0].sor, 5)      # a torzs 4. sora = a fajl 5. sora

    def test_negativ_marker_par_hianyzik(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, 'naplo.md', 'csak kezi sor\n')
            t = self._futtat(gy, marker_celok=[('naplo', 'naplo.md')])
            self.assertEqual(len(t), 1)
            self.assertIn('hiányzik', t[0].reszlet)

    def test_a_nem_listan_levo_befagyasztott_lap_nem_fut(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            # a befagyasztott lap tartalma eltér mindentől, de nincs a listán
            _ir(gy, 'lexikon/MASIK-001_TUDOMANYOS.md', 'kezzel irt, befagyasztott lap, 【NAPLO: x】\n')
            self.assertEqual(self._futtat(gy), [])

    def test_ures_lista_nulla_nezet(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'eszkozok/ellenorzes/e28_migralt_nezetek.tsv', _lista())
            self.assertEqual(self._futtat(gy), [])
            self.assertEqual(SZ.E28_JEGYZETEK, ['E28: 0 migrált nézet'])

    def test_nem_indul_erintetlen_fajlokkal(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, _LAP, 'tetszoleges, a generatortol eltero tartalom\n')
            self.assertEqual(self._futtat(gy, fajlok=['README.md']), [])
            self.assertIn('nem futott', SZ.E28_JEGYZETEK[0])

    def test_indul_adat_tsv_valtozassal(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, _LAP, 'tetszoleges, GENERÁLT ts=2026-10-01 jelolovel, de mas tartalom\n')
            self.assertEqual(len(self._futtat(gy, fajlok=['adat/jeloltek.tsv'])), 1)

    def test_negativ_generalt_jelolo_nelkuli_nezet(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, _LAP, 'kezi fajl jelolo nelkul\n')
            t = self._futtat(gy)
            self.assertEqual(len(t), 1)
            self.assertIn('nincs GENERÁLT jelölő', t[0].reszlet)

    def test_negativ_crlf_blob_lf_generalt_kimenettel_piros(self):
        # CI-terv 1. szakasz 3. pont: a sorvegnek is egyeznie kell (nincs normalizalas)
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, _LAP, self._render(gy, '2026-10-01').replace('\n', '\r\n'))
            t = self._futtat(gy)
            self.assertEqual([x.szabaly for x in t], ['E28'])
            self.assertEqual(t[0].sor, 1)
            self.assertIn('\\r', t[0].reszlet)     # a repr-ben latszik a CR

    def test_negativ_crlf_marker_blokk_piros(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, 'naplo.md', ('kezi\n' + _MARKER_BLOKK + '\n').replace('\n', '\r\n'))
            t = self._futtat(gy, marker_celok=[('naplo', 'naplo.md')])
            self.assertEqual(len(t), 1)
            self.assertEqual(t[0].szint, 'HIBA')

    def test_negativ_nyito_marker_zaro_nelkul_hibatalalat_nem_kivetel(self):
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            _ir_nyers(gy, 'naplo.md', 'kezi\n<!-- GENERÁLT-KEZDET: general.py --cel naplo#teszt | forrás: x | ts=2026-09-15 -->\ntorzs\n')
            t = self._futtat(gy, marker_celok=[('naplo', 'naplo.md')])
            self.assertEqual(len(t), 1)
            self.assertEqual((t[0].szabaly, t[0].szint, t[0].fajl), ('E28', 'HIBA', 'naplo.md'))
            self.assertIn('naplo#teszt', t[0].reszlet)
            self.assertIn('záró pár nélkül', t[0].reszlet)
            self.assertIn('python eszkozok/general.py --cel naplo --ir', t[0].reszlet)

    def test_valodi_blob_ag_nyers_bajtokat_ad_nem_mockolt_commitolt(self):
        # A `_e28_commitolt` NINCS mockolva: a `git show` kimenetet a subprocess.run
        # helyettesiti CRLF-es bajtokkal (commitolt CRLF-blob). A blob-agnak meg kell
        # orznie a CR-t, es az E28 piros (a generalt kimenet LF-es).
        from unittest import mock
        with _IdeiglenesGyoker() as gy:
            self._fixture(gy)
            crlf_blob = self._render(gy, '2026-10-01').replace('\n', '\r\n').encode('utf-8')
            hivasok = []

            def hamis_run(args, **kw):
                hivasok.append(args)
                self.assertEqual(args[:2], ['git', 'show'])
                return subprocess.CompletedProcess(args, 0, stdout=crlf_blob, stderr=b'')

            def hamis_generator(cel, azonosito, datum, kimenet):
                ut = os.path.join(kimenet, *_LAP.split('/'))
                os.makedirs(os.path.dirname(ut), exist_ok=True)
                with open(ut, 'w', encoding='utf-8', newline='') as f:
                    f.write(self._render(gy, datum))
                return 0, ''

            with mock.patch.object(SZ.subprocess, 'run', hamis_run):
                self.assertEqual(SZ._e28_commitolt(_LAP), crlf_blob.decode('utf-8'))
                self.assertIn('\r\n', SZ._e28_commitolt(_LAP))
                with mock.patch.object(SZ, '_e28_general_futtat', hamis_generator), \
                        mock.patch.object(SZ, 'E28_MARKER_CELOK', ()):
                    t = SZ.e28_generalt_nezet_egyezes(['__TELJES__'])
            self.assertTrue(hivasok)
            self.assertEqual([x.szabaly for x in t], ['E28'])
            self.assertIn('\\r', t[0].reszlet)

    def test_munkafa_tartalek_lf_es_jelzi_hogy_nem_blob(self):
        with _IdeiglenesGyoker() as gy:
            _ir_nyers(gy, 'x.md', 'a\r\nb\r\n')
            del SZ.E28_JEGYZETEK[:]
            self.assertEqual(SZ._e28_commitolt('x.md'), 'a\nb\n')
            self.assertTrue(any('nem blob-összevetés' in j for j in SZ.E28_JEGYZETEK))

    def test_szint_fajlszintu_hiba(self):
        self.assertEqual(SZ.SZINT['E28'], 'HIBA')
        self.assertIn('E28', SZ.FAJLSZINTU_SZABALYOK)
        self.assertIn('E28', SZ.SZABALYOK_FUGGVENYEI)


class E29Teszt(unittest.TestCase):
    """E29: a kiadhato kimenetben nulla `belso` jeloles es nulla 【NAPLO."""

    def _fut(self, tartalom, melyseg='apparatus', extra=None):
        with _IdeiglenesGyoker() as gy:
            _lista_ir(gy, _lista_sor(melyseg=melyseg))
            _ir(gy, _LAP, tartalom)
            for relut, szoveg in (extra or {}).items():
                _ir(gy, relut, szoveg)
            return SZ.e29_kiadhato_kimenet_tisztasaga(['__TELJES__'])

    def test_pozitiv_apparatus_nezet_naplo_nelkul_zold(self):
        self.assertEqual(self._fut('# Lap\n\nApparatus szoveg, proveniencia: scope=x.\n'), [])

    def test_negativ_naplo_a_lapon_piros(self):
        t = self._fut('# Lap\n\nSzoveg 【NAPLO: folyamat-nyom】\n')
        self.assertEqual([(x.szabaly, x.szint, x.fajl, x.sor) for x in t], [('E29', 'HIBA', _LAP, 3)])
        self.assertIn('【NAPLO', t[0].reszlet)

    def test_negativ_naplo_kodkeritesen_belul_is(self):
        t = self._fut('```\n【NAPLO: kodblokkban】\n```\n')
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0].sor, 2)

    def test_negativ_belso_szintjelolo_piros(self):
        t = self._fut('# Lap\n<!-- SZINT-KEZDET: belso -->\nbelso\n<!-- SZINT-VÉGE: belso -->\n')
        self.assertEqual([x.sor for x in t], [2, 4])

    def test_negativ_inaktiv_jelolo_piros(self):
        t = self._fut('# Lap\n<!-- INAKTÍV: nincs adat -->\n')
        self.assertEqual(len(t), 1)
        self.assertIn('INAKTÍV:', t[0].reszlet)

    def test_negativ_olvasoi_melysegben_proveniencia_piros_apparatusban_nem(self):
        sor = '# Lap\nAllitas. proveniencia: scope=x | forras=y | ts=z\n<!-- RÉS-KEZDET: kivonat -->\n'
        t = self._fut(sor, melyseg='olvasoi')
        self.assertEqual(sorted(x.reszlet for x in t),
                         ['minta: RÉS-KEZDET', 'minta: proveniencia:'])
        self.assertEqual(self._fut(sor, melyseg='apparatus'), [])

    def test_a_motivumok_forras_nem_hatokor(self):
        # a forrasban a 【NAPLO kotelezo hely; a lista csak a lexikon-lapot nevezi meg
        t = self._fut('# tiszta lap\n', extra={'motivumok/ZZTESZT-001.md': '【NAPLO: forrasban szabad】\n'})
        self.assertEqual(t, [])

    def test_ismeretlen_melyseg_hiba(self):
        t = self._fut('# tiszta lap\n', melyseg='belso')
        self.assertEqual(len(t), 1)
        self.assertIn('ismeretlen melyseg', t[0].reszlet)

    def test_ures_lista_nulla_talalat(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'eszkozok/ellenorzes/e28_migralt_nezetek.tsv', _lista())
            self.assertEqual(SZ.e29_kiadhato_kimenet_tisztasaga(['__TELJES__']), [])

    def test_szint_fajlszintu_hiba(self):
        self.assertEqual(SZ.SZINT['E29'], 'HIBA')
        self.assertIn('E29', SZ.FAJLSZINTU_SZABALYOK)
        self.assertIn('E29', SZ.SZABALYOK_FUGGVENYEI)


class TestE30(unittest.TestCase):
    """F112: ekezet nelkul irt magyar szo a commit-uzenetben (DT-F112a: FIGYELMEZTETES)."""

    SZOTAR = {'ket': 'két', 'javitas': 'javítás', 'konyv': 'könyv', 'meg': 'még',
              'allapot': 'állapot', 'forras': 'forrás', 'fuggetlen': 'független'}
    KIZ = {'meg': 'ketertelmu', 'allapot': 'mezonev'}

    def _j(self, uzenet):
        return [a for a, _ in SZ.e30_jeloltek(uzenet, self.SZOTAR, self.KIZ)]

    def test_ekezetlen_szo_jelol(self):
        self.assertEqual(self._j('F1.1: ket javitas'), ['ket', 'javitas'])
        self.assertEqual(SZ.e30_jeloltek('a konyv', self.SZOTAR, self.KIZ), [('konyv', 'könyv')])

    def test_mezonev_nem_jelol(self):
        self.assertEqual(self._j('brief fejlec: allapot: fut'), [])

    def test_ketertelmu_par_nem_jelol(self):
        self.assertEqual(self._j('meg nem kesz'), [])

    def test_kodreszben_allo_szo_nem_jelol(self):
        self.assertEqual(self._j('a `ket` mezo'), [])

    def test_fajlut_azonosito_coauthored_nem_jelol(self):
        self.assertEqual(self._j('naplok/ket_javitas.md frissitve'), [])
        self.assertEqual(self._j('lásd F112_ket_BRIEF.md és ISTENTISZT-001'), [])
        self.assertEqual(self._j('szöveg\n\nCo-Authored-By: Ket Konyv <a@b>'), [])
        self.assertEqual(self._j('forras=manual'), [])

    def test_ekezetes_alak_nem_jelol(self):
        self.assertEqual(self._j('két javítás'), [])

    def test_gepi_commit_kimarad(self):
        self.assertEqual(self._j('szamkiosztas: DT-F1a -> DT1 ket konyv'), [])

    def test_push_esemenynel_nem_fut(self):
        self.assertEqual(SZ.e30_ascii_commit('a', 'b', 'ket konyv javitas', 'push'), [])

    def test_szint_fajlszintu_figyelmeztetes(self):
        self.assertEqual(SZ.SZINT['E30'], 'FIGYELMEZTETES')
        self.assertIn('E30', SZ.FAJLSZINTU_SZABALYOK)

    def test_kizaras_tsv_minden_soranak_van_oka_es_forrasa(self):
        with open(SZ.E30_ALAKOK_TSV, encoding='utf-8') as f:
            sorok = [s for s in f.read().split('\n')[1:] if s.strip()]
        for s in sorok:
            m = s.split('\t')
            self.assertEqual(len(m), 3, s)
            self.assertIn(m[1], ('mezonev', 'ertekkeszlet', 'ketertelmu', 'rovidites'), s)
            self.assertTrue(m[2].strip(), s)


# ---------------------------------------------------------------------------
# E31 (#11 S2, DT250): a `forras_tanulmany` letezo, reponbeli fajlra mutat
# ---------------------------------------------------------------------------

_E31_FEJ = '# fejlec\nid\tigehely\tfelmerult_tanulmany\tforras_tanulmany\n'


class E31Teszt(unittest.TestCase):
    """E31: nem ures `forras_tanulmany` csak letezo, reponbeli fajlra mutathat;
    az ures ertek nem jelez."""

    def _fut(self, *ertekek, fajlok=('genezis/1Moz_3v7-24_bovitett.md',)):
        with _IdeiglenesGyoker() as gy:
            for relut in fajlok:
                _ir(gy, relut, '# tanulmany\n')
            sorok = ''.join('PROBA-001\t1Móz 3:%d\tx\t%s\n' % (i + 1, e) for i, e in enumerate(ertekek))
            _ir(gy, 'adat/elofordulasok.tsv', _E31_FEJ + sorok)
            return SZ.e31_forras_tanulmany_letezik(['__TELJES__'])

    def test_pozitiv_letezo_fajl_es_ures_ertek_zold(self):
        self.assertEqual(self._fut('genezis/1Moz_3v7-24_bovitett.md', ''), [])

    def test_pozitiv_csak_ures_ertekek_zold(self):
        self.assertEqual(self._fut('', '', fajlok=()), [])

    def test_negativ_nem_letezo_fajl_hiba(self):
        t = self._fut('genezis/1Moz_3v7-24_bovitett.md', 'genezis/nincs_ilyen.md')
        self.assertEqual([(x.szabaly, x.szint, x.fajl, x.sor) for x in t],
                         [('E31', 'HIBA', 'adat/elofordulasok.tsv', 4)])
        self.assertIn('nem létező fájl', t[0].reszlet)

    def test_negativ_csak_fajlnev_ut_nelkul_hiba(self):
        t = self._fut('1Moz_3v7-24_bovitett.md')
        self.assertEqual(len(t), 1)
        self.assertIn('nem létező fájl', t[0].reszlet)

    def test_negativ_kis_nagybetu_elteres_hiba(self):
        t = self._fut('Genezis/1Moz_3v7-24_bovitett.md')
        self.assertEqual(len(t), 1)
        self.assertIn('nem létező fájl', t[0].reszlet)

    def test_negativ_konyvtar_hiba(self):
        t = self._fut('genezis')
        self.assertEqual(len(t), 1)
        self.assertIn('könyvtár', t[0].reszlet)

    def test_negativ_reponbeliseg_es_alak(self):
        rossz = ['./genezis/1Moz_3v7-24_bovitett.md', 'genezis/../genezis/1Moz_3v7-24_bovitett.md',
                 '../kivul.md', '/genezis/1Moz_3v7-24_bovitett.md', 'C:/genezis/x.md',
                 'genezis\\1Moz_3v7-24_bovitett.md', ' genezis/1Moz_3v7-24_bovitett.md',
                 'genezis//1Moz_3v7-24_bovitett.md']
        t = self._fut(*rossz)
        self.assertEqual([x.sor for x in t], list(range(3, 3 + len(rossz))))
        self.assertTrue(all(x.szint == 'HIBA' for x in t))

    def test_tabla_nelkul_nulla_talalat(self):
        with _IdeiglenesGyoker():
            self.assertEqual(SZ.e31_forras_tanulmany_letezik(['__TELJES__']), [])

    def test_oszlop_nelkuli_tabla_nem_jelez(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'adat/elofordulasok.tsv', '# fejlec\nid\tigehely\nPROBA-001\t1Móz 3:1\n')
            self.assertEqual(SZ.e31_forras_tanulmany_letezik(['__TELJES__']), [])

    def test_szint_fajlszintu_hiba(self):
        self.assertEqual(SZ.SZINT['E31'], 'HIBA')
        self.assertIn('E31', SZ.FAJLSZINTU_SZABALYOK)
        self.assertIn('E31', SZ.SZABALYOK_FUGGVENYEI)

    def test_eles_tabla_zold(self):
        # a repo mai tablaja (az S2.4 19 athozott sora) az E31-en zold
        self.assertEqual(SZ.e31_forras_tanulmany_letezik(['__TELJES__']), [])


# ---------------------------------------------------------------------------
# E32 (#141, DT370): kiosztott helyorzo egy kimeneti string-literalban
# ---------------------------------------------------------------------------

class E32Teszt(unittest.TestCase):
    """E32: a szamkiosztas mar kiosztott helyorzoja a string-literalban jelez;
    megjegyzesben, docstringben, kihagy-jelolt soron es tesztfajlban nem."""

    KIOSZTOTT = {'DT-F127b': 'DT277'}

    def _fut(self, forras, relut='eszkozok/proba_kimenet.py', kiosztott=None):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, relut, forras)
            eredeti = SZ._e32_kiosztasok
            SZ._e32_kiosztasok = lambda: dict(self.KIOSZTOTT if kiosztott is None else kiosztott)
            try:
                return SZ.e32_kiosztott_helyorzo_literalban([relut])
            finally:
                SZ._e32_kiosztasok = eredeti

    def test_pozitiv_visszairt_kiosztott_helyorzo_a_literalban(self):
        t = self._fut('x = 1\nprint("lásd DT-F127b döntés")\n')
        self.assertEqual([(x.szabaly, x.szint, x.fajl, x.sor) for x in t],
                         [('E32', 'HIBA', 'eszkozok/proba_kimenet.py', 2)])
        self.assertIn('DT-F127b', t[0].reszlet)
        self.assertIn('DT277', t[0].reszlet)

    def test_pozitiv_tobbsoros_literal_pontos_sora(self):
        t = self._fut('S = """elso\nmasodik DT-F127b\nharmadik"""\n')
        self.assertEqual([x.sor for x in t], [2])

    def test_pozitiv_osszefuzott_tobbsoros_literal_tenyleges_sora(self):
        # implicit string-osszefuzes: egyetlen Constant, lineno = elso sor
        forras = ('x = 1\nS = ("elso sor "\n     "masodik DT-F127b "\n     "harmadik DT-F127b")\n')
        t = self._fut(forras)
        self.assertEqual([x.sor for x in t], [3, 4])

    def test_pozitiv_nem_ascii_osszefuzott_tobbsoros_literal(self):
        # az ast bajt-, a tokenize karakter-offszetet ad: nem-ASCII elotag nem ejtheti ki a tokent
        forras = ("print('Hiányzó', ('… DT-F127b '\n"
                  "                 'második sor … DT-F127b'))\n")
        self.assertEqual([x.sor for x in self._fut(forras)], [1, 2])

    def test_pozitiv_osszefuzott_literal_harmadik_soron(self):
        forras = 'print("a "\n      "b "\n      "c DT-F127b")\n'
        self.assertEqual([x.sor for x in self._fut(forras)], [3])

    def test_negativ_osszefuzott_literal_kihagy_a_tenyleges_soron(self):
        forras = ('S = ("elso "\n     "DT-F127b "  # e32-kihagy: torteneti\n     "vege")\n')
        self.assertEqual(self._fut(forras), [])

    def test_pozitiv_osszefuzott_literal_kihagy_mas_soron_nem_vedi(self):
        # a kihagy-jeloles az elso soron van, a helyorzo a masodikon
        forras = ('S = ("elso "  # e32-kihagy\n     "DT-F127b "\n     "vege")\n')
        self.assertEqual([x.sor for x in self._fut(forras)], [2])

    def test_pozitiv_fstring_literal_resze(self):
        t = self._fut('n = 3\nprint(f"{n} db, DT-F127b szerint")\n')
        self.assertEqual([x.sor for x in t], [2])

    def test_negativ_megjegyzes_nem_jelez(self):
        self.assertEqual(self._fut('# DT-F127b a megjegyzésben\nx = 1  # N-F127b\n', kiosztott={'DT-F127b': 'DT277', 'N-F127b': 'N5'}), [])

    def test_negativ_docstring_nem_jelez(self):
        forras = ('"""Modul DT-F127b.\n"""\n\n\ndef f():\n    """Függvény DT-F127b."""\n    return 1\n\n\n'
                  'class C:\n    "osztály DT-F127b"\n')
        self.assertEqual(self._fut(forras), [])

    def test_negativ_nem_kiosztott_helyorzo_nem_jelez(self):
        self.assertEqual(self._fut('print("DT-F999z")\n'), [])

    def test_negativ_kiosztott_szam_nem_jelez(self):
        self.assertEqual(self._fut('print("DT277")\n'), [])

    def test_negativ_kihagy_jeloles_a_soron(self):
        self.assertEqual(self._fut('print("DT-F127b")  # e32-kihagy: történeti\n'), [])
        self.assertEqual(self._fut('print("DT-F127b")  # szamkiosztas-kihagy\n'), [])

    def test_negativ_tesztfajl_es_szabalyfajl_kizart(self):
        for relut in ('eszkozok/teszt_proba.py', 'eszkozok/ellenorzes/tesztek/test_x.py',
                      'eszkozok/szamkiosztas.py', 'eszkozok/ellenorzes/szabalyok.py'):
            self.assertEqual(self._fut('print("DT-F127b")\n', relut=relut), [], relut)

    def test_negativ_nem_eszkozok_py_nem_jelez(self):
        self.assertEqual(self._fut('print("DT-F127b")\n', relut='masik/proba.py'), [])

    def test_negativ_szintaktikai_hibas_fajl_nem_omlik(self):
        self.assertEqual(self._fut('def (:\n'), [])

    def test_teljes_mod_bejarja_az_eszkozok_fat(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, 'eszkozok/al/mappa/k.py', 'print("DT-F127b")\n')
            eredeti = SZ._e32_kiosztasok
            SZ._e32_kiosztasok = lambda: dict(self.KIOSZTOTT)
            try:
                t = SZ.e32_kiosztott_helyorzo_literalban(['__TELJES__'])
            finally:
                SZ._e32_kiosztasok = eredeti
            self.assertEqual([(x.fajl, x.sor) for x in t], [('eszkozok/al/mappa/k.py', 1)])

    def test_kiosztasok_a_szamkiosztas_commitokbol(self):
        # valodi (ideiglenes) git-repo: a `szamkiosztas:` commit uzenetebol
        # kiolvasott hozzarendeles; a ma is definialt helyorzo nem kiosztott
        with _IdeiglenesGyoker() as gy:
            def git(*a):
                subprocess.check_call(('git', '-c', 'user.name=t', '-c', 'user.email=t@t') + a,
                                      cwd=gy, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            git('init', '-q')
            _ir(gy, 'DONTESEK.md', '| DT-F7q | #7 | kerdes |\n')
            git('add', '-A')
            git('commit', '-q', '-m', 'F1: alap')
            uz = _ir(gy, 'uzenet.txt', 'szamkiosztas: DT-F127b \u2192 DT277, DT-F7q \u2192 DT278\n')
            git('commit', '-q', '--allow-empty', '-F', 'uzenet.txt')
            self.assertEqual(SZ._e32_kiosztasok(), {'DT-F127b': 'DT277'})

    def test_szint_d8_jelentes_a_regi_soron(self):
        # nem fajlszintu: a futtat.py D8-cal csak a diff-ben hozzaadott soron HIBA
        self.assertEqual(SZ.SZINT['E32'], 'HIBA')
        self.assertNotIn('E32', SZ.FAJLSZINTU_SZABALYOK)
        self.assertIn('E32', SZ.HATOKOR_SZABALYOK)
        self.assertIn('E32', SZ.SZABALYOK_FUGGVENYEI)

    def test_eles_repo_csak_a_tesztek_kivul_jelez_es_fut(self):
        # a mai repon a szabaly lefut es a kizart fajlokat nem jelzi
        t = SZ.e32_kiosztott_helyorzo_literalban(['__TELJES__'])
        self.assertTrue(all(not SZ._e32_kizart(x.fajl) for x in t))


if __name__ == '__main__':
    unittest.main()
