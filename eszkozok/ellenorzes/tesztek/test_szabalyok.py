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


if __name__ == '__main__':
    unittest.main()
