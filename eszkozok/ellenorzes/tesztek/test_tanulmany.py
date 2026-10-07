#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_tanulmany.py -- F37 T3: a tanulmany-szabalyok pozitiv es negativ tesztjei.
Az E20 uj szabaly; a tervezett E21-E24 az E13, E8, E9, E12 tanulmanyfajlra
szolo bovitese (naplok/T0_felmeres.md 3. pont, DT-F37-8). Minden szabalyhoz
legalabb egy pozitiv (talal) es egy negativ (nem talal) fixture.

A fixture-ok ideiglenes gyokerbe kerulnek (_IdeiglenesGyoker, l.
test_szabalyok.py), az eles repot a teszt nem irja.

Futtatas a repo gyokerebol:
    python eszkozok/ellenorzes/tesztek/test_tanulmany.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_ITT))
sys.path.insert(0, _ITT)

import kozos as K
import szabalyok as SZ
from test_szabalyok import _IdeiglenesGyoker, _ir

TANULMANY = 'genezis/1Moz_99v1_bovitett.md'
NEM_TANULMANY = 'genezis/proba.md'

SABLON = (
    "# 2. Tanulmány sablon (PaRDeS)\n\n"
    "## 0. Sorozat-kontextus *(feltételes pont)*\n\nfeltétel\n\n"
    "## 1. Alapkérdések\n\nkérdések\n\n"
    "## 2. Eredeti nyelvi szöveg *(a Peshat előtt)*\n\nszöveg\n\n"
    "## 3. PaRDeS keretrendszer\n\nrétegek\n\n"
    "## 7. Lexikai audit — módszertani napló *(feltételes pont)*\n\naudit\n\n"
    "## Terminológiai és formai szabályok (minden sablonra érvényes)\n\n- szabály\n"
)

JO_TANULMANY = (
    "# 1Móz 99:1 — tanulmány\n\n"
    "## 1. Alapkérdések\n\nKi írja?\n\n---\n\n"
    "## 2. Eredeti nyelvi szöveg\n\nA szöveg.\n\n"
    "## 3. PaRDeS keretrendszer\n\nPeshat.\n"
)


class TanulmanyFajlTeszt(unittest.TestCase):
    def test_tanulmany_fajl_e(self):
        self.assertTrue(K.tanulmany_fajl_e('genezis/1Moz_12v1-20_bovitett.md'))
        self.assertTrue(K.tanulmany_fajl_e('zsoltarok/Zsolt_23_tanulmany.md'))
        self.assertFalse(K.tanulmany_fajl_e('genezis/naplok/1Moz_1v1_bovitett.md'))
        self.assertFalse(K.tanulmany_fajl_e('sablonok/2_PaRDeS_bovitett_sablon.md'))
        self.assertFalse(K.tanulmany_fajl_e('genezis/Konnyu_ellenorzes_1-16_osszesito.md'))
        self.assertFalse(K.tanulmany_fajl_e('tematikus_lezart/Tehom_tematikus.md'))
        self.assertFalse(K.tanulmany_fajl_e('tematikus_lezart/Konnyu_ellenorzes_4_lezart_tanulmany.md'))


class E20Teszt(unittest.TestCase):
    def test_negativ_minden_kotelezo_szakasz_megvan(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            rel = _ir(gy, TANULMANY, JO_TANULMANY)
            self.assertEqual(SZ.e20_kotelezo_szakaszok([rel]), [])

    def test_pozitiv_hianyzo_kotelezo_szakasz(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            rel = _ir(gy, TANULMANY, JO_TANULMANY.replace("## 3. PaRDeS keretrendszer\n\nPeshat.\n", ""))
            t = SZ.e20_kotelezo_szakaszok([rel])
            self.assertEqual(len(t), 1)
            self.assertIn('## 3.', t[0].reszlet)
            self.assertEqual(t[0].szint, 'HIBA')

    def test_pozitiv_eltero_cim_es_ures_torzs(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            szoveg = JO_TANULMANY.replace('## 1. Alapkérdések', '## 1. Bevezetés') \
                                 .replace('A szöveg.', '')
            rel = _ir(gy, TANULMANY, szoveg)
            t = SZ.e20_kotelezo_szakaszok([rel])
            self.assertEqual(len(t), 2)

    def test_negativ_felteteles_szakasz_hianyozhat(self):
        """A sablon `(feltételes pont)` szakasza (0., 7.) nem kotelezo."""
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            rel = _ir(gy, TANULMANY, JO_TANULMANY)
            self.assertFalse(any('## 0.' in x.reszlet or '## 7.' in x.reszlet
                                 for x in SZ.e20_kotelezo_szakaszok([rel])))

    def test_pozitiv_a_lista_a_sablonbol_jon_dt_f37_6(self):
        """A sablon uj kotelezo szakasza kodmodositas nelkul kotelezo lesz."""
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON + "\n## 4. Kapcsolódó igehelyek — hol\n\nx\n")
            rel = _ir(gy, TANULMANY, JO_TANULMANY)
            t = SZ.e20_kotelezo_szakaszok([rel])
            self.assertEqual(len(t), 1)
            self.assertIn('## 4.', t[0].reszlet)

    def test_negativ_nem_tanulmanyfajl(self):
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            rel = _ir(gy, NEM_TANULMANY, "# semmi\n")
            self.assertEqual(SZ.e20_kotelezo_szakaszok([rel]), [])


class E13TanulmanyTeszt(unittest.TestCase):
    """E21 -> E13: tanulmanyfajlon HIBA, minden futam, bovitett elfogadott alakok."""

    def test_pozitiv_tanulmanyban_hiba(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "A גדל gyök jelentése nagy.\n")
            t = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_pozitiv_masodik_futam_is(self):
        """A sor elso szava kiejtessel all, a masodik nem: talalat."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "A תֹהוּ – tohu és a בֹהוּ párja.\n")
            t = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual(len(t), 1)
            self.assertIn('בֹהוּ', t[0].reszlet)

    def test_pozitiv_hatokor_konyvtaron_kivul(self):
        """Uj konyvtarba irt tanulmany is HIBA (ELLENOR_TANULMANY_ELLENORZES 1.)."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'zsoltarok/Zsolt_23_tanulmany.md', "A גדל gyök jelentése nagy.\n")
            t = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual([x.szint for x in t], ['HIBA'])

    def test_negativ_hatokoron_kivul_nem_tanulmany(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'zsoltarok/jegyzet.md', "A גדל gyök jelentése nagy.\n")
            self.assertEqual(SZ.e13_kiejtes_hianya([rel]), [])

    def test_negativ_tablazat_kovetkezo_cellaja(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "| 12:2 | בְּרָכָה | *berachá* | H1293 | áldás |\n")
            self.assertEqual(SZ.e13_kiejtes_hianya([rel]), [])

    def test_negativ_zarojelben_vesszo_utan(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "a táblázatra (מִשְׁפְּחֹת, *mispachot*) utal\n")
            self.assertEqual(SZ.e13_kiejtes_hianya([rel]), [])

    def test_negativ_perjeles_atiras(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "| תּוֹלְדֹת / toledot (H8435) | ✅ |\nitt karat/כרת áll\n")
            self.assertEqual(SZ.e13_kiejtes_hianya([rel]), [])

    def test_negativ_eredeti_nyelvu_versor(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "> בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ׃\n")
            self.assertEqual(SZ.e13_kiejtes_hianya([rel]), [])

    def test_negativ_gorog_politonikus_atirassal(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "a lélek (ψυχῆς, *pszükhész*) és\n")
            self.assertEqual(SZ.e13_kiejtes_hianya([rel]), [])

    def test_nem_tanulmanyban_figyelmeztetes_marad(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, NEM_TANULMANY, "A גדל gyök jelentése nagy.\n")
            t = SZ.e13_kiejtes_hianya([rel])
            self.assertEqual([x.szint for x in t], ['FIGYELMEZTETES'])


class E8TanulmanyTeszt(unittest.TestCase):
    """E22 -> E8: tanulmanyban a hosszu konyvnev es a STEPBible-alak is tiltott."""

    def test_pozitiv_hosszu_konyvnev_es_step_alak(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "# 1Mózes 12:1-20 — tanulmány\n\nLásd Gen.12.7 és 1 Mózes 3:1.\n")
            t = SZ.e8_igehely_format([rel])
            self.assertEqual(len(t), 3)

    def test_negativ_helyes_format(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "# 1Móz 12:1-20 — tanulmány\n\nLásd 1Móz 12:7, Mózes első könyve.\n")
            self.assertEqual(SZ.e8_igehely_format([rel]), [])

    def test_negativ_step_alak_nem_tanulmanyban(self):
        """CLAUDE.md, briefek: a STEPBible-alak adatformatumkent legitim."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'F99_PROBA_BRIEF.md', "A Karoli_KH alakja Gen.1.1.\n")
            self.assertEqual(SZ.e8_igehely_format([rel]), [])


class E9TanulmanyTeszt(unittest.TestCase):
    """E23 -> E9: tanulmanyban a blockquote (🔗 blokk) sem kizart."""

    def test_pozitiv_blockquote_tanulmanyban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "> *(kulcsszó: áldás — a 2. sense szerint)*\n")
            self.assertEqual(len(SZ.e9_angol_sense([rel])), 1)

    def test_negativ_idezojeles_tanulmanyban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, '> a BDB szerint "in this sense"\n')
            self.assertEqual(SZ.e9_angol_sense([rel]), [])

    def test_negativ_blockquote_nem_tanulmanyban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, NEM_TANULMANY, "> be left over in this sense\n")
            self.assertEqual(SZ.e9_angol_sense([rel]), [])


class E12TanulmanyTeszt(unittest.TestCase):
    """E24 -> E12: naplojellegu cimsor/mondat tanulmanyban, NAPLO blokkon kivul."""

    def test_pozitiv_naplo_cimsor_es_mondat(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "## Formai önellenőrzés (elvégezve)\n\nA retroaktív pótlás kész.\n")
            t = SZ.e12_proveniencia_prozaban([rel])
            self.assertEqual(len(t), 2)
            self.assertTrue(all(x.szint == 'FIGYELMEZTETES' for x in t))

    def test_pozitiv_hatokor_konyvtaron_kivul(self):
        """Uj konyvtarba irt tanulmanyon is fut (ELLENOR_TANULMANY_ELLENORZES 1.)."""
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, 'zsoltarok/Zsolt_23_tanulmany.md', "## Formai önellenőrzés (elvégezve)\n\nA retroaktív pótlás kész.\n")
            self.assertEqual(len(SZ.e12_proveniencia_prozaban([rel])), 2)

    def test_negativ_naplo_blokkban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, TANULMANY, "【NAPLO: retroaktív pótlás, a Code-prompt szerint.】\n")
            self.assertEqual(SZ.e12_proveniencia_prozaban([rel]), [])

    def test_negativ_nem_tanulmanyban(self):
        with _IdeiglenesGyoker() as gy:
            rel = _ir(gy, NEM_TANULMANY, "## Formai önellenőrzés\n\nretroaktív\n")
            self.assertEqual(SZ.e12_proveniencia_prozaban([rel]), [])


class FuttatSzintTeszt(unittest.TestCase):
    """A futtat.py a talalat sajat szintjet veszi alapul (E13: tanulmany HIBA)."""

    def test_tanulmany_hiba_mas_figyelmeztetes(self):
        import futtat as FU
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            _ir(gy, TANULMANY, JO_TANULMANY + "\nA גדל gyök.\n")
            _ir(gy, NEM_TANULMANY, "A גדל gyök.\n")
            eredmeny = FU.fut([TANULMANY, NEM_TANULMANY], False)
        szintek = {(x.fajl, x.szint) for x in eredmeny['E13']}
        self.assertEqual(szintek, {(TANULMANY, 'HIBA'), (NEM_TANULMANY, 'FIGYELMEZTETES')})
        self.assertEqual(eredmeny['E20'], [])

    def test_teljes_modban_jelentes(self):
        import futtat as FU
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            _ir(gy, TANULMANY, "# üres\n")
            eredmeny = FU.fut([], True)
        self.assertTrue(eredmeny['E20'])
        self.assertTrue(all(x.szint == 'JELENTES' for x in eredmeny['E20']))


class TanulmanyAuditTeszt(unittest.TestCase):
    """Jelentes mod: minden tanulmanyfajl, nem bukik."""

    def test_audit_jelentes(self):
        import tanulmany_audit as TA
        with _IdeiglenesGyoker() as gy:
            _ir(gy, K.TANULMANY_SABLON, SABLON)
            _ir(gy, TANULMANY, "# üres\n\nA גדל gyök.\n")
            _ir(gy, 'genezis/1Moz_98v1_bovitett.md', JO_TANULMANY)
            fajlok, eredmeny = TA.audit()
            szoveg = TA.jelentes(fajlok, eredmeny)
        self.assertEqual(sorted(fajlok), ['genezis/1Moz_98v1_bovitett.md', TANULMANY])
        self.assertTrue(szoveg.startswith('# GENERÁLT'))
        self.assertIn('| E20 |', szoveg)
        self.assertEqual(len(eredmeny['E20']), 3)  # a TANULMANY-bol 1., 2., 3. hianyzik


class TanulmanyEllenorzesSegedTeszt(unittest.TestCase):
    """T4 segedszkript: igeszakasz a fajlnevbol, vers-cella ertelmezese (a
    valodi normalizalo tablaval)."""

    def test_szakasz_fajlnevbol(self):
        import tanulmany_ellenorzes as TE
        self.assertEqual(TE.tanulmany_szakasz('genezis/1Moz_12v1-20_bovitett.md'), ('1Móz', (12, 1), (12, 20)))
        self.assertEqual(TE.tanulmany_szakasz('genezis/1Moz_10v1-11v32_bovitett.md'), ('1Móz', (10, 1), (11, 32)))
        self.assertEqual(TE.tanulmany_szakasz('genezis/1Moz_14_bovitett.md'), ('1Móz', (14, 1), (14, None)))
        self.assertEqual(TE.tanulmany_szakasz('ujszovetseg/Rom_8v10_bovitett.md'), ('Róm', (8, 10), (8, 10)))

    def test_vers_cella(self):
        import tanulmany_ellenorzes as TE
        sz = ('1Móz', (6, 9), (6, 22))
        self.assertEqual(TE.versek(sz, '12:7/12:8 ⚠️'), ['1Móz 12:7', '1Móz 12:8'])
        self.assertEqual(TE.versek(sz, '17'), ['1Móz 6:17'])
        self.assertIsNone(TE.versek(sz, ''))


if __name__ == '__main__':
    unittest.main()
