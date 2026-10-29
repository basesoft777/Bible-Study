#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_forditas_kapuk.py -- F28_EMELES_BRIEF.md: a forditas_kapuk.py
DT25 utan felvett jelzo kapuinak (12. Szentlélek, 13. fejezetszam) es a
11. konyv-egyezes kapunak tesztjei.

    python eszkozok/teszt_forditas_kapuk.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import forditas_kapuk as K  # noqa: E402


class Szentlelek(unittest.TestCase):
    def test_jelzes(self):
        for szoveg in ('a Szentlélek által', 'Isten Lelke', 'Szent Lélek'):
            self.assertEqual(K.ellenoriz_szentlelek(szoveg)[0], 'JELZES', szoveg)

    def test_jovahagyott_alak(self):
        self.assertEqual(K.ellenoriz_szentlelek('a Szent Szellem, Isten Szelleme, a lélek')[0], 'RENDBEN')


class Fejezetszam(unittest.TestCase):
    def test_forrashiba_peldak_f38(self):
        # F38.266 (DT-F38e): a forrasbeli (BDB) igehely-hibak listazasa, nem javitasa
        e, d = K.ellenoriz_fejezetszam('Hab 41:47; Jóel 9:9; 1Móz 81:3')
        self.assertEqual(e, 'JELZES')
        for hely in ('Hab 41', 'Jóel 9', '1Móz 81'):
            self.assertIn(hely, d)

    def test_nem_javit_es_nem_gatol(self):
        e, _ = K.ellenoriz_fejezetszam('Hab 41:47')
        self.assertEqual(e, 'JELZES')
        self.assertTrue(K.atment([('13_fejezetszam', e, '')]))

    def test_tul_nagy_fejezet(self):
        e, d = K.ellenoriz_fejezetszam('Ez 73:23; Péld 57:1')
        self.assertEqual(e, 'JELZES')
        self.assertIn('Ez 73', d)

    def test_heber_szamozas_es_rovid_konyv(self):
        self.assertEqual(K.ellenoriz_fejezetszam('Jóel 4:19; 1Ján 5:7; Júd 1:20; Zsolt 150:6')[0], 'RENDBEN')


class KonyvTablaAlakok(unittest.TestCase):
    """F38, DT-F38 (c): a 11. kapu a tabla `Forrás-alakok` oszlopat is ismeri."""

    def test_forras_alak_karoli_megfelelovel_rendben(self):
        forras = 'Ex 7:29; Cant 1:12; 2 Chron 21:43; Malachi 3:19; Ezekiel 16:4'
        forditas = '2Móz 7:29; Én 1:12; 2Krón 21:43; Mal 3:19; Ez 16:4'
        self.assertEqual(K.ellenoriz_konyvek(forras, forditas)[0], 'RENDBEN')

    def test_forras_alak_angolul_hagyva_sertes(self):
        # a leképezés óta az angolul hagyott forrásalak hiánynak számít
        e, d = K.ellenoriz_konyvek('Ex 7:29; 1Chron 16:8', 'Ex 7:29; 1Chron 16:8')
        self.assertEqual(e, 'SERTES')
        self.assertIn('2Móz', d)
        self.assertIn('1Krón', d)

    def test_kings_szam_nelkul_nincs_lekepezve(self):
        # a „Kings” nem egyértelmű (1Kir/2Kir): forrásbeli szigla marad
        self.assertEqual(K.ellenoriz_konyvek('compare Kings 6:35', 'vö. Kings 6:35')[0], 'RENDBEN')


class PsiJavitas(unittest.TestCase):
    """F34 M4: a javitott BDB-ψ helyekre a 13. kapu jelzese 0; a hibas feloldasra marad."""

    def test_javitott_hely_nem_jelez(self):
        for sz in ('Zsolt 106:9; Zsolt 71:20', 'Zsolt 97:7', 'Zsolt 16:10; Zsolt 49:16'):
            self.assertEqual(K.ellenoriz_fejezetszam(sz)[0], 'RENDBEN', sz)

    def test_hibas_psi_feloldas_jelez(self):
        for sz in ('Ézs 106:9', 'Jób 97:7', 'Ez 73:25', 'Péld 75:1'):
            self.assertEqual(K.ellenoriz_fejezetszam(sz)[0], 'JELZES', sz)

    def test_javitott_sorok_a_forditasokban(self):
        sorok = open('adat/forditasok.tsv', encoding='utf-8').read().split(chr(10))
        for n in (78, 89):
            hu = sorok[n - 1].split(chr(9))[6]
            self.assertEqual(K.ellenoriz_fejezetszam(hu)[0], 'RENDBEN', n)


class LelekTovaltozat(unittest.TestCase):
    """ELLENOR_F28 3. tétel: a „lélek” tőváltozata (lelk-) csak a főnév
    toldalékolt alakjára illeszkedjen."""

    TERM = [{'angol': 'soul', 'magyar': 'lélek'}]

    def _e(self, forditas):
        return K.ellenoriz_terminologia('the soul of man', forditas, self.TERM, [])[0]

    def test_toldalekolt_alakok(self):
        for szo in ('lelke', 'lelkét', 'lelkem', 'lelkedből', 'lelkünk', 'lelkük',
                    'lelkek', 'lelketekben', 'keserű lelkű', 'Lelkét'):
            self.assertEqual(self._e('az ember %s' % szo), 'RENDBEN', szo)

    def test_nem_a_lelek_alakjai(self):
        for szo in ('lelkiismeret', 'lelkiismerete', 'lelkész', 'lelkésze',
                    'lelkes', 'lelkesedés', 'lelkület', 'lelki'):
            self.assertEqual(self._e('az ember %s' % szo), 'SERTES', szo)

    def test_alapalak(self):
        self.assertEqual(self._e('az ember lélek'), 'RENDBEN')


class PontosKulcsolas(unittest.TestCase):
    """DT26 #15/#26: a két „compare” sort a kulcs választja szét
    (`compare` → vö., `מִן compare` → comparativus)."""

    TERM = [{'angol': 'compare', 'magyar': 'vö.'},
            {'angol': 'מִן compare', 'magyar': 'comparativus'}]

    def _e(self, forras, forditas):
        return K.ellenoriz_terminologia(forras, forditas, self.TERM, [])

    def test_csak_min_compare_comparativust_kovetel(self):
        forras = 'be swift, with מִן compare, of warriors 2Sam 1:23'
        self.assertEqual(self._e(forras, 'gyorsnak lenni, a מִן comparativusszal, 2Sám 1:23')[0], 'RENDBEN')

    def test_min_compare_comparativus_nelkul_sertes(self):
        forras = 'be swift, with מִן compare, of warriors 2Sam 1:23'
        e, r = self._e(forras, 'gyorsnak lenni, vö. 2Sám 1:23')
        self.assertEqual(e, 'SERTES')
        self.assertIn('מִן compare -> comparativus', r)
        self.assertNotIn('compare -> vö.', r.replace('מִן compare -> comparativus', ''))

    def test_onallo_compare_vo_t_kovetel(self):
        forras = 'with מִן compare Ezek 8:17; compare Dr'
        e, r = self._e(forras, 'מִן comparativusszal Ez 8:17; Dr')
        self.assertEqual(e, 'SERTES')
        self.assertIn('compare -> vö. hianyzik', r)
        self.assertEqual(self._e(forras, 'מִן comparativusszal Ez 8:17; vö. Dr')[0], 'RENDBEN')


class KapuOszlop(unittest.TestCase):
    """DT27: a terminologia.tsv `kapu` oszlopa (igen/nem; hiányzó = igen)."""

    FORRAS = 'so read also 1:21; compare Dr'

    def _e(self, term):
        return K.ellenoriz_terminologia(self.FORRAS, 'így olvasandó az 1:21-ben is; Dr', term, [])

    def test_kapu_nem_nem_ad_sertest(self):
        term = [{'angol': 'read', 'magyar': 'olv.', 'kapu': 'nem'},
                {'angol': 'compare', 'magyar': 'vö.', 'kapu': 'nem'}]
        self.assertEqual(self._e(term)[0], 'RENDBEN')

    def test_kapu_igen_sertest_ad(self):
        e, r = self._e([{'angol': 'read', 'magyar': 'olv.', 'kapu': 'igen'}])
        self.assertEqual(e, 'SERTES')
        self.assertIn('read -> olv.', r)

    def test_hianyzo_es_ures_ertek_igen(self):
        self.assertEqual(self._e([{'angol': 'read', 'magyar': 'olv.'}])[0], 'SERTES')
        self.assertEqual(self._e([{'angol': 'read', 'magyar': 'olv.', 'kapu': ''}])[0], 'SERTES')
        self.assertTrue(K.kapus_sor({'kapu': ' '}))
        self.assertFalse(K.kapus_sor({'kapu': 'nem'}))

    def test_kapu_nem_hosszabb_kulcs_nem_von_el(self):
        # ELLENOR_DT27 1. (a) opció: a kapu=nem `which see` belsejében álló `see`
        # a kapu=igen „see → l.” soré marad
        term = [{'angol': 'see', 'magyar': 'l.', 'kapu': 'igen'},
                {'angol': 'which see', 'magyar': 'l. ott', 'kapu': 'nem'}]
        forras = 'Rom 8:21 (on which see δουλεία)'
        e, r = K.ellenoriz_terminologia(forras, 'Róm 8:21 (ehhez δουλεία)', term, [])
        self.assertEqual(e, 'SERTES')
        self.assertIn('see -> l. hianyzik', r)
        self.assertNotIn('which see', r)
        self.assertEqual(K.ellenoriz_terminologia(forras, 'Róm 8:21 (ehhez l. δουλεία)', term, [])[0],
                         'RENDBEN')

    def test_kapu_igen_hosszabb_kulcs_elvon(self):
        # a kapu=igen hosszabb kulcs (`which see`) továbbra is elvonja a rövidebbet
        term = [{'angol': 'see', 'magyar': 'l.', 'kapu': 'igen'},
                {'angol': 'which see', 'magyar': 'l. ott', 'kapu': 'igen'}]
        forras = '(λύτρον, which see)'
        e, r = K.ellenoriz_terminologia(forras, '(λύτρον, vö.)', term, [])
        self.assertEqual(e, 'SERTES')
        self.assertIn('which see -> l. ott', r)
        self.assertNotIn('; see -> l.', r)
        self.assertFalse(r.startswith('see -> l.'))

    def test_prompt_tartalmazza_a_kapu_nem_sorokat(self):
        import emeles
        # a prompt a tábla MINDEN sorát tartalmazza, a kapu értékétől függetlenül
        szoveg, _ = emeles.terminologia_szoveg()
        for t in emeles.tsv_dict_sorok(emeles.TERMINOLOGIA_UT):
            self.assertIn('`%s` = %s' % (t['angol'], t['magyar']), szoveg, t.get('kapu'))


class Konyvek(unittest.TestCase):
    def test_jsir_es_sir(self):
        self.assertEqual(K.ellenoriz_konyvek('Lam 3:57; Sir. 1:3', 'JSir 3:57; Sir 1:3')[0], 'RENDBEN')
        self.assertEqual(K.ellenoriz_konyvek('Lam 3:57', 'Sir 3:57')[0], 'SERTES')


class KaroliNagybetusSzo(unittest.TestCase):
    """F38, DT-F38c (e): a c:v előtti nagybetűs, nem könyvnév szó nem 3. kapus hiba
    (a 2. és 3. adag önújrapróbáinak esetei)."""

    def setUp(self):
        self.karoli, _ = K._betolt()

    def _e(self, forras, forditas):
        return K.ellenoriz_karoli(forras, forditas, self.karoli)[0]

    def test_lancolt_igehely_magyar_szorenddel_rendben(self):
        for forras, forditas in (
                ("(God's hostility 23:16 the cause", '(Isten 23:16 ellenségeskedése'),
                ('of Judah 12:6; 19:8-9t.', 'Júdáról 12:6; 19:8-9t.'),
                ('the A 4:16 text', 'A 4:16 szöveg'),
                ('of Benjamin 18:16', 'Benjáminén 18:16'),
                ('Horeb 24:4', 'a Hóreben 24:4')):
            self.assertEqual(self._e(forras, forditas), 'RENDBEN', forditas)

    def test_konyvnevnek_latszo_alak_tovabbra_is_sertes(self):
        # angol/STEPBible könyvalak a fordításban
        self.assertEqual(self._e('Gen 1:1', 'Gen 1:1'), 'SERTES')
        # számmal kezdődő, ismeretlen könyvalak
        self.assertEqual(self._e('Ezek 3:4', '1Ezék 3:4'), 'SERTES')

    def test_karoli_rovidites_rendben(self):
        self.assertEqual(self._e('Gen 1:1; Ezek 3:4', '1Móz 1:1; Ez 3:4'), 'RENDBEN')

    def test_rossz_konyvet_a_11_kapu_fogja(self):
        # a 3. kapu átengedi (nem könyvnévnek látszik), a 11. hiányt jelez
        self.assertEqual(self._e('Isa 3:4', 'Ézsaiás 3:4'), 'RENDBEN')
        self.assertEqual(K.ellenoriz_konyvek('Isa 3:4', 'Ézsaiás 3:4')[0], 'SERTES')


class KisNagybetuCsere(unittest.TestCase):
    """F38, DT-F38c (d): az 5. kapu kötelező alakjának kis/nagybetű-eltérése gépi
    cserével javul, naplózva; más eltérés továbbra is SÉRTÉS."""

    def setUp(self):
        _, self.term = K._betolt()

    def test_h2719_zendzsirli(self):
        forras = 'Phoenician, Zinjirli חרב'
        uj, naplo = K.terminologia_kisnagybetu_csere(forras, 'föníciai, zendzsirli חרב', self.term)
        self.assertEqual(uj, 'föníciai, Zendzsirli חרב')
        self.assertEqual(naplo, [('Zinjirli', 'zendzsirli', 'Zendzsirli', 1)])
        self.assertEqual(K.ellenoriz_terminologia(forras, uj, self.term, [])[0], 'RENDBEN')

    def test_nem_csak_kisnagybetu_marad_sertes(self):
        forras = 'Phoenician, Zinjirli חרב'
        uj, naplo = K.terminologia_kisnagybetu_csere(forras, 'föníciai, zincirli חרב', self.term)
        self.assertEqual(naplo, [])
        self.assertEqual(K.ellenoriz_terminologia(forras, uj, self.term, [])[0], 'SERTES')

    def test_betuhu_alak_megvan_nincs_csere(self):
        forras = 'Zinjirli; Zinjirli'
        h = 'Zendzsirli; zendzsirli'
        self.assertEqual(K.terminologia_kisnagybetu_csere(forras, h, self.term), (h, []))

    def test_szo_belseje_nem_csere(self):
        # csak szókezdeten álló alakot cserél
        uj, naplo = K.terminologia_kisnagybetu_csere('Zinjirli', 'xzendzsirli', self.term)
        self.assertEqual(naplo, [])

    def test_kivetel_nem_csere(self):
        uj, naplo = K.terminologia_kisnagybetu_csere('Zinjirli', 'zendzsirli', self.term, ['Zinjirli'])
        self.assertEqual(naplo, [])

    def test_utofeldolgoz_naplozza(self):
        import emeles
        sp, forras = emeles.forras_szoveg('H2719')
        self.assertIn('Zinjirli', forras)
        # a forrás minimális „fordítása”: csak a csere hatását nézzük
        vegleges, valt, _, _ = emeles.utofeldolgoz(sp, 'zendzsirli')
        self.assertEqual(vegleges, 'Zendzsirli')
        self.assertTrue(any(v[0].startswith('5_kisnagybetu zendzsirli -> Zendzsirli') for v in valt), valt)


class FejezetszamBdbJeloles(unittest.TestCase):
    """F56 M5: a `Y [BDB: X]` jelolesben X-et a 13. kapu nem jelzi."""

    def test_bdb_jeloles_nem_jelzes(self):
        self.assertEqual(K.ellenoriz_fejezetszam('Préd 7:10 [BDB: Préd 17:10]')[0], 'RENDBEN')

    def test_valodi_hiba_tovabbra_jelzes(self):
        self.assertEqual(K.ellenoriz_fejezetszam('Préd 17:10')[0], 'JELZES')
        self.assertEqual(K.ellenoriz_fejezetszam('Préd 17:10 [BDB: Préd 17:10]')[0], 'JELZES')


class BdbJelolesVissza(unittest.TestCase):
    def test_visszaallitas(self):
        self.assertEqual(K.bdb_jeloles_vissza('lásd Préd 7:10 [BDB: Préd 17:10]; 1Kir 6:6 [BDB: 1Kir 66:6].'),
                         'lásd Préd 17:10; 1Kir 66:6.')

    def test_nincs_jeloles_valtozatlan(self):
        self.assertEqual(K.bdb_jeloles_vissza('Préd 7:10; 1Kir 6:6'), 'Préd 7:10; 1Kir 6:6')


class PromptKotelezoAlakok(unittest.TestCase):
    """F38, DT-F38c (d), prompt v4.1: a kötelező alakok előgyűjtése."""

    def test_prompt_helyorzo_kitoltve(self):
        import emeles
        sp, forras = emeles.forras_szoveg('H2719')
        p = emeles.prompt_epit(sp, forras)
        self.assertNotIn('{{KOTELEZO_ALAKOK}}', p)
        self.assertIn('- `Zinjirli` → `Zendzsirli`', p)

    def test_kapu_nem_sor_nincs_a_listaban(self):
        import emeles
        alakok = dict(emeles.kotelezo_alakok('compare this; which see'))
        self.assertNotIn('compare', alakok)
        self.assertNotIn('which see', alakok)
        self.assertEqual(alakok.get('see'), 'l.')


class TagolasRovidites(unittest.TestCase):
    """F38, DT-F38c (e): a c./d./f./i. betűjel nem kötelező (rövidítésként is áll),
    a fordítás oldalán a circa- és f-kivétel nem szűr."""

    def _e(self, forras, forditas):
        return K.ellenoriz_tagolas(forras, forditas)[0]

    def test_c_szamjeggyel_kezdodo_igehely_elott(self):
        # H3808: „c. Gen 15:13” -> „c. 1Móz 15:13” (eddig csak „c. —” alakkal ment át)
        self.assertEqual(self._e('Zeph 2:1). c. Gen 15:13 להם', 'Sof 2:1). c. 1Móz 15:13 להם'), 'RENDBEN')
        self.assertEqual(self._e('b. x c. 3rd person', 'b. x c. 3. személyben'), 'RENDBEN')

    def test_forditas_oldalan_az_i_e_kivetel_nem_szur(self):
        # H4325: „vizei. e.” — a fordításban az „e.” betűjelet eddig „i. e.”-nek vette
        self.assertEqual(self._e('d. x e. the waters', 'd. x vizei. e. a vizek'), 'RENDBEN')

    def test_rovidites_jellegu_betujel_elhagyhato(self):
        self.assertEqual(self._e('1. x f. below 2. y', '1. x lent 2. y'), 'RENDBEN')
        self.assertEqual(self._e('a. x i. below b. y', 'a. x lent b. y'), 'RENDBEN')
        self.assertEqual(self._e('a. x d. day b. y', 'a. x nap b. y'), 'RENDBEN')

    def test_opcionalis_betujel_megvan_es_illeszkedik(self):
        e, d = K.ellenoriz_tagolas('a. x b. y c. z d. w', 'a. x b. y c. z d. w')
        self.assertEqual(e, 'RENDBEN')
        self.assertNotIn('atlepett', d)

    def test_kotelezo_jelolo_tovabbra_is_sertes(self):
        self.assertEqual(self._e('a. x b. y c. z', 'a. x c. z'), 'SERTES')
        self.assertEqual(self._e('1. x 2. y', '1. x y'), 'SERTES')
        self.assertEqual(self._e('a. x e. y', 'a. x y'), 'SERTES')

    def test_opcionalis_nem_nyeli_el_a_kovetkezo_kotelezot(self):
        # a forrás „c.” rövidítés; a fordításban a „c.” csak a 2. után áll —
        # nem illeszkedhet a 2. elé, a 2. kötelező jelölő megmarad
        self.assertEqual(self._e('1. x c. y 2. z', '1. x y 2. z c. w'), 'RENDBEN')
        self.assertEqual(self._e('1. x c. y 2. z 3. q', '1. x y 2. z c. w'), 'SERTES')

    def test_igazitas_opcionalissal(self):
        ig = K.tagolas_igazitas('1. x f. below 2. y', '1. x lent 2. y')
        self.assertEqual([j for j, _, _ in ig], ['1', 'f', '2'])
        self.assertIsNone(ig[1][2])
        self.assertIsNotNone(ig[2][2])


class TapadtKonyvjelzes11(unittest.TestCase):
    """F38.261, DT-F38d (c): a 11. kapu a forrasbeli, szohoz tapadt angol
    konyvjelzest is szamolja."""

    def test_tapadt_forras_leválasztva_rendben(self):
        forras = 'abundantly2Chr 3:1; completely2Chr 4:2; verbDeuteronomy 7:8'
        forditas = 'bőségesen 2Krón 3:1; teljesen 2Krón 4:2; ige 5Móz 7:8'
        self.assertEqual(K.ellenoriz_konyvek(forras, forditas)[0], 'RENDBEN')

    def test_tapadt_forras_osszetapasztva_hagyva_sertes(self):
        # a forditasban tovabbra is tapadt, angol alak: hianyzo igehely
        e, d = K.ellenoriz_konyvek('abundantly2Chr 3:1', 'abundantly2Chr 3:1')
        self.assertEqual(e, 'SERTES')
        self.assertIn('2Krón', d)

    def test_tapadt_karoli_alak_a_forditasban_nem_szamit(self):
        e, _ = K.ellenoriz_konyvek('abundantly2Chr 3:1', 'bőségesen2Krón 3:1')
        self.assertEqual(e, 'SERTES')

    def test_nagybetu_elotti_nem_tapadt(self):
        self.assertEqual(K.ellenoriz_konyvek('ABC2Chr 3:1', 'ABC2Chr 3:1')[0], 'RENDBEN')

    def test_a_normalizalt_forditas_atmegy(self):
        import normalizal as N
        forras = 'abundantly2Chr 3:1'
        uj, _ = N.normalizal(forras, 'BDB')
        self.assertEqual(K.ellenoriz_konyvek(forras, uj)[0], 'RENDBEN')


class TorzsRagozott(unittest.TestCase):
    """F38.261, DT-F38d (c): a 10. kapu a magyar raggal allo torzsneveket is
    felismeri."""

    def test_ragozott_alakok(self):
        for szoveg, var in (('Qalban', ['Qal']), ('Nifalban', ['Niph']), ('Pielben', ['Piel']),
                            ('Pualban', ['Pual']), ('Hifilben', ['Hiph']), ('Hofalban', ['Hoph']),
                            ('Hitpaelben', ['Hith']), ('Qalról', ['Qal']), ('Qalnak', ['Qal'])):
            self.assertEqual(K.torzs_sorozat(szoveg), var, szoveg)

    def test_forras_es_forditas_egyezik(self):
        e, _ = K.ellenoriz_torzs('Qal Niph Pi Hiph', 'Qalban Nifalban Pi Hifilben')
        self.assertEqual(e, 'RENDBEN')

    def test_ragozott_torzs_elmaradasa_sertes(self):
        e, _ = K.ellenoriz_torzs('Qal Pual', 'Qalban')
        self.assertEqual(e, 'SERTES')

    def test_csupasz_alak_valtozatlan(self):
        self.assertEqual(K.torzs_sorozat('Qal, Niph, Hithpael.'), ['Qal', 'Niph', 'Hith'])

    def test_rovid_torzs_hamis_talalat_nincs(self):
        # Put (helynev), Pure: a Pi/Pu + rovid rag nem torzsnev
        self.assertEqual(K.torzs_sorozat('Put és Pure és Piacon'), [])

    def test_rovid_torzs_hosszu_raggal(self):
        self.assertEqual(K.torzs_sorozat('Pielben és Puban'), ['Piel', 'Pu'])

    def test_mas_szo_resze_nem(self):
        self.assertEqual(K.torzs_sorozat('Qalamar Hifilosz'), [])


class SzellemKisNagybetu(unittest.TestCase):
    """F38, DT-F38f (2), DT25: a `spirit` kulcs magyar alakja kis- ES nagybetuvel
    is megfelel (szellem/Szellem es ragozott alakjaik); mas kulcsra nem lazul."""

    def setUp(self):
        _, self.term = K._betolt()

    def _e(self, forras, hu):
        return K.ellenoriz_terminologia(forras, hu, self.term, [])[0]

    def test_kisbetus_es_nagybetus_alak(self):
        for szo in ('szellem', 'szelleme', 'szellemet', 'Szellem', 'Szelleme', 'Szellemet',
                    'Szellemével', 'szellemmel'):
            self.assertEqual(self._e('the spirit of God', 'Isten %s' % szo), 'RENDBEN', szo)

    def test_hianyzo_alak_sertes(self):
        self.assertEqual(self._e('the spirit of God', 'Isten lehelete'), 'SERTES')

    def test_nagybetus_szellem_nem_csereli_kisbetusre(self):
        uj, naplo = K.terminologia_kisnagybetu_csere('the spirit of God', 'Isten Szelleme', self.term)
        self.assertEqual((uj, naplo), ('Isten Szelleme', []))

    def test_mas_kulcs_nem_lazul(self):
        # a `soul` -> `lélek` kulcsra a nagybetu nem megfelelo alak
        self.assertEqual(self._e('the soul of man', 'az ember Lélek'), 'SERTES')

    def test_nincs_szocikkszintu_spirit_kivetel_a_sorokon(self):
        for l in open('adat/forditasok.tsv', encoding='utf-8').read().split(chr(10)):
            m = l.split(chr(9))
            if len(m) == 12:
                self.assertNotIn('bizonytalan_feloldasok): spirit', m[11], m[1])


class ForrasVersOcr(unittest.TestCase):
    """F38, DT-F38g (5): a `FORRAS_VERS_OCR` csak a `Gen 33:816t.` helyre és csak a
    2_versszam kapu forrásparaméterére hat."""

    def test_lekepezes_pontosan_egy_tetel(self):
        self.assertEqual(K.FORRAS_VERS_OCR, {'Gen 33:816t.': 'Gen 33:8 16t.'})

    def test_javitja_az_osszeforrt_helyet(self):
        self.assertEqual(K._vers_ocr_javit('see Gen 33:816t. and'), 'see Gen 33:8 16t. and')

    def test_mas_hely_nem_valtozik(self):
        for szoveg in ('Gen 33:81 x', 'Gen 33:816', 'Gen 33:816t', 'Gen 3:816t.', 'Gen 33:8 16t.',
                       'Ex 33:816t.', 'Gen 34:816t.', 'Gen 33:8; Gen 33:16', 'nincs vers', ''):
            self.assertEqual(K._vers_ocr_javit(szoveg), szoveg, szoveg)

    def test_csak_a_2_versszam_kapu_kapja_a_javitott_forrast(self):
        from unittest import mock
        forras = 'Gen 33:816t. forrás'
        kapott = {}

        def rogzit(nev):
            def f(*args):
                kapott[nev] = args[0]
                return ('RENDBEN', '')
            return f

        with mock.patch.object(K._p4, 'ellenoriz_1_gorog_heber', rogzit('1')), \
                mock.patch.object(K._p4, 'ellenoriz_2_versszam', rogzit('2')), \
                mock.patch.object(K._p4, 'ellenoriz_6_hosszarany', rogzit('6')), \
                mock.patch.object(K, 'ellenoriz_karoli', rogzit('3')), \
                mock.patch.object(K, 'ellenoriz_formazas', rogzit('4')), \
                mock.patch.object(K, 'ellenoriz_terminologia', rogzit('5')), \
                mock.patch.object(K, 'ellenoriz_idezojel', rogzit('8')), \
                mock.patch.object(K, 'ellenoriz_tagolas', rogzit('9')), \
                mock.patch.object(K, 'ellenoriz_torzs', rogzit('10')), \
                mock.patch.object(K, 'ellenoriz_konyvek', rogzit('11')):
            K.kapuk_futtat('BDB', forras, 'fordítás')
        self.assertEqual(kapott['2'], 'Gen 33:8 16t. forrás')
        for nev, ertek in kapott.items():
            if nev != '2':
                self.assertEqual(ertek, forras, 'a %s. kapu nyers forrást kap' % nev)
        self.assertEqual(len(kapott), 10)


class IdezojelForrasMaradvany(unittest.TestCase):
    """A H4725 `«GKC:130c»` forras-maradvanya (DT-F38j): a « a forrasban is par."""

    def test_forras_francia_idezojel_par(self):
        forras = 'zz (Ges ^«GKC:130c»§ 130c) zz'
        forditas = 'zz (Ges ^«GKC:130c»§ 130c) zz'
        self.assertEqual(K.idezojel_parok_forras(forras), 1)
        self.assertEqual(K.ellenoriz_idezojel(forras, forditas)[0], 'RENDBEN')

    def test_valodi_hiany_tovabbra_is_serites(self):
        self.assertEqual(K.ellenoriz_idezojel('nincs', 'itt »van« egy')[0], 'SERTES')
        self.assertEqual(K.ellenoriz_idezojel('"x" y', 'x y')[0], 'SERTES')


class Szakasz(unittest.TestCase):
    """F128 M3: a 14. szakasz-kapu (a `⟪n⟫` határtokenek), szintetikus esetek."""
    F = '⟪1⟫ H1. ab\n⟪2⟫ noun father\n⟪3⟫ 1 father of individual\n⟪4⟫ 2 of God'

    def _e(self, h):
        return K.ellenoriz_szakasz(self.F, h)

    def test_rendben(self):
        self.assertEqual(self._e('⟪1⟫ H1. ab ⟪2⟫ főnév apa ⟪3⟫ 1 egyén apja ⟪4⟫ 2 Istenről'), ('RENDBEN', '4 szakasz'))

    def test_hianyzo(self):
        e, d = self._e('⟪1⟫ H1. ab ⟪2⟫ főnév apa 1 egyén apja ⟪4⟫ 2 Istenről')
        self.assertEqual(e, 'SERTES')
        self.assertIn('hianyzo token: 3', d)

    def test_duplazott(self):
        e, d = self._e('⟪1⟫ H1. ab ⟪2⟫ főnév ⟪2⟫ apa ⟪3⟫ 1 egyén apja ⟪4⟫ 2 Istenről')
        self.assertEqual(e, 'SERTES')
        self.assertIn('duplazott token: 2', d)

    def test_felcserelt(self):
        e, d = self._e('⟪1⟫ H1. ab ⟪3⟫ 1 egyén apja ⟪2⟫ főnév apa ⟪4⟫ 2 Istenről')
        self.assertEqual(e, 'SERTES')
        self.assertIn('sorrendje', d)

    def test_ures_szakasz(self):
        e, d = self._e('⟪1⟫ H1. ab ⟪2⟫ ⟪3⟫ 1 egyén apja, főnév apa ⟪4⟫ 2 Istenről')
        self.assertEqual(e, 'SERTES')
        self.assertIn('ures szakasz: 2', d)

    def test_uj_token(self):
        e, d = self._e('⟪1⟫ H1. ab ⟪2⟫ főnév apa ⟪3⟫ 1 egyén apja ⟪4⟫ 2 Istenről ⟪5⟫ toldás')
        self.assertEqual(e, 'SERTES')
        self.assertIn('uj token: 5', d)

    def test_szoveg_az_elso_token_elott(self):
        e, d = self._e('Fordítás: ⟪1⟫ H1. ab ⟪2⟫ főnév apa ⟪3⟫ 1 egyén apja ⟪4⟫ 2 Istenről')
        self.assertEqual(e, 'SERTES')
        self.assertIn('elso token elott', d)

    def test_token_nelkuli_szoveg(self):
        self.assertEqual(K.szakasz_nelkul('⟪1⟫ a b\n⟪2⟫ c'), 'a b c')

    def test_atment_gatol(self):
        self.assertFalse(K.atment([('14_szakasz', 'SERTES', '')]))
        self.assertTrue(K.atment([('14_szakasz', 'RENDBEN', '')]))

    def test_tagolas_szakaszonkent(self):
        # a 2. jelentésszám a magyarban a szomszéd szakaszba vándorolt: egészben átmenne, szakaszonként nem
        f = '⟪1⟫ word. 1 father of individual ⟪2⟫ 2 of God as father'
        h = '⟪1⟫ szó. 1 egyén apja. 2 Isten ⟪2⟫ mint atya'
        self.assertEqual(K.ellenoriz_tagolas(K.szakasz_nelkul(f), K.szakasz_nelkul(h))[0], 'RENDBEN')
        self.assertEqual(K.ellenoriz_tagolas_szakaszonkent(f, h)[0], 'SERTES')
        jo = '⟪1⟫ szó. 1 egyén apja ⟪2⟫ 2 Isten mint atya'
        self.assertEqual(K.ellenoriz_tagolas_szakaszonkent(f, jo)[0], 'RENDBEN')

    def test_szakaszos_futtatas(self):
        f = '⟪1⟫ word. 1 father of individual ⟪2⟫ 2 of God as father'
        nevek = [n for n, _, _ in K.kapuk_futtat_szakaszos('BDB', f, '⟪1⟫ szó. 1 egyén apja ⟪2⟫ 2 Isten mint atya')]
        self.assertEqual(nevek[-1], '14_szakasz')
        self.assertIn('9_tagolas', nevek)
        e = dict((n, x) for n, x, _ in K.kapuk_futtat_szakaszos('BDB', f, '⟪1⟫ szó. 1 egyén apja 2 Isten mint atya'))
        self.assertEqual(e['14_szakasz'], 'SERTES')


class SzakaszKeszMagyar(unittest.TestCase):
    """F128 M3: a kész magyar BDB-fordítás (`adat/bdb_szakasz_hu.tsv`) `illeszkedik` sorainál kezdődő szakaszokból
    összerakott tokenes szövegeken a szakasz-kapu 0 hibát ad."""

    def test_kesz_forditasok(self):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdb_jelolt'))
        import szakasz_bemenet as SB
        strongok = sorted({r['strong'] for r in SB.nezet_general.olvas(SB.HU_TABLA)})
        self.assertEqual(len(strongok), 674)
        hibak, n = [], 0
        for st in strongok:
            p = SB.kesz_magyar_csoportositva(st)
            if p is None:
                continue
            n += 1
            e, d = K.ellenoriz_szakasz(p[0], p[1])
            if e != 'RENDBEN':
                hibak.append((st, d))
        self.assertEqual(hibak, [])
        self.assertEqual(n, 674)


class Tiltott(unittest.TestCase):
    """F132 (DT-F132f; elv: DT241): a 15. kapu, adat/tiltott_fordulatok.tsv."""

    def test_tabla_betolt(self):
        t = K.tiltott_betolt()
        self.assertGreaterEqual(len(t), 2)
        self.assertIn('melléknéven nevezni', [a for a, _, _, _ in t])

    def test_igei_szerkezet_sertes(self):
        for s in ('nevet tenni valakire, melléknéven nevezni', 'akit melléknéven neveznek', 'hogy valakit Melléknéven nevezzenek',
                  'hívni, nevezni, melléknevet adni', 'melléknevet adott neki', 'nevezték melléknéven is'):
            self.assertEqual(K.ellenoriz_tiltott(s)[0], 'SERTES', s)

    def test_nevet_tenni_valakire(self):
        # DT379: a „to put a name upon” tükörfordítása; az „elnevezni” és a passzív alak rendben
        for s in ('nevet tenni valakire', 'nevet tettek rá', 'nevet tett valakire'):
            self.assertEqual(K.ellenoriz_tiltott(s)[0], 'SERTES', s)
        for s in ('elnevezni valakit', 'nevet adni valakinek', 'akit Péternek is neveznek'):
            self.assertEqual(K.ellenoriz_tiltott(s)[0], 'RENDBEN', s)

    def test_nyelvtani_melleknev_rendben(self):
        for s in ('melléknév, hímnemű', 'melléknévként használva', 'melléknévi igenév', 'a melléknév nőnemű alakja',
                  'más néven is nevezni', 'akit Péternek is neveznek'):
            self.assertEqual(K.ellenoriz_tiltott(s)[0], 'RENDBEN', s)

    def test_ures_tabla(self):
        self.assertEqual(K.ellenoriz_tiltott('melléknéven nevezni', tiltott=[])[0], 'RENDBEN')

    def test_gatol_a_kapusorban(self):
        self.assertIn('15_tiltott', K.GATOLO)
        e = K.kapuk_futtat('Thayer', 'to surname', 'melléknéven nevezni')
        self.assertEqual([x for x in e if x[0] == '15_tiltott'][0][1], 'SERTES')
        self.assertFalse(K.atment(e))

    def test_szakaszos_futtatasban_is(self):
        e = K.kapuk_futtat_szakaszos('Thayer', '⟪1⟫ to surname', '⟪1⟫ melléknéven nevezni')
        self.assertEqual([x for x in e if x[0] == '15_tiltott'][0][1], 'SERTES')

    def test_meglevo_forditasok(self):
        # mérés (F132, 2026-10-25): a forditasok.tsv-ben csak a két G1941 sor 4 helye talált (F121 2b/4); a TBESG-sor
        # javítva (F121.0, DT379), maradt a Thayer G1941; a nyelvtani „melléknév” sorok nem találatok
        ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'adat', 'forditasok.tsv')
        with open(ut, encoding='utf-8', newline='') as fh:
            sorok = [s for s in fh.read().split('\n') if s and not s.startswith('#')]
        fej = sorok[0].split('\t')
        talalt = set()
        for s in sorok[1:]:
            r = dict(zip(fej, s.split('\t')))
            if K.ellenoriz_tiltott(r['forditas_hu'])[0] == 'SERTES':
                talalt.add((r['szotar'], r['strong']))
        self.assertTrue(talalt <= {('Thayer', 'G1941')}, talalt)


class BdbJavitas(unittest.TestCase):
    """F67: a 17_bdb_javitas kapu (DT55); tabla: adat/bdb_igehely_javitas.tsv, SEMA 2.23."""

    F = 'A fold. Eccl 17:10 mondja.'

    def kapu(self, forras, forditas, strong='H7223', szotar='BDB'):
        return K.ellenoriz_bdb_javitas(szotar, forras, forditas, strong)

    def test_rendben(self):
        self.assertEqual(self.kapu(self.F, 'A fold. Préd 7:10 [BDB: Préd 17:10] mondja.')[0], 'RENDBEN')

    def test_hianyzo_jeloles(self):
        e, d = self.kapu(self.F, 'A fold. Préd 7:10 mondja.')
        self.assertEqual(e, 'SERTES')
        self.assertIn('hiányzik', d)

    def test_rossz_y(self):
        e, d = self.kapu(self.F, 'A fold. Préd 8:10 [BDB: Préd 17:10] mondja.')
        self.assertEqual(e, 'SERTES')
        self.assertIn('hiányzik', d)
        self.assertIn('jogosulatlan: Préd 8:10 [BDB: Préd 17:10]', d)

    def test_csupasz_x(self):
        e, d = self.kapu(self.F, 'A fold. Préd 17:10 mondja.')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jelölés nélküli', d)

    def test_jelolt_marad_jelolese(self):
        # H0001 `Esth 11:32`: jelolt_marad, a forras alakja marad; a jelolese jogosulatlan
        e, d = self.kapu('Esth 11:32 itt', 'Eszt 10:32 [BDB: Eszt 11:32] itt', strong='H0001')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jogosulatlan', d)
        self.assertEqual(self.kapu('Esth 11:32 itt', 'Eszt 11:32 itt', strong='H0001')[0], 'RENDBEN')

    def test_ismeretlen_x(self):
        e, d = self.kapu(self.F, 'A fold. Préd 7:10 [BDB: Préd 17:10] Ézs 2:3 [BDB: Ézs 22:3] mondja.')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jogosulatlan: Ézs 2:3 [BDB: Ézs 22:3]', d)

    def test_hatarolt_forrashivatkozas(self):
        # `Ezra 16:8` nem talalat az `Ezra 16:80`-ban; a forras nem tartalmazza, jeloles sem kell
        self.assertEqual(self.kapu('Ezra 16:80 itt', 'Ezsd 16:80 itt', strong='H0479')[0], 'RENDBEN')
        self.assertEqual(self.kapu('Ezra 16:8 itt', 'Ezsd 6:8 [BDB: Ezsd 16:8] itt', strong='H0479')[0], 'RENDBEN')

    def test_versfel_betu(self):
        # DT-F38v (c): a `16:8b` forras-hivatkozas jelolese Y<betu> [BDB: X<betu>], azonos betuvel
        f = 'Ezra 16:8b itt'
        self.assertEqual(self.kapu(f, 'Ezsd 6:8b [BDB: Ezsd 16:8b] itt', strong='H0479')[0], 'RENDBEN')
        # eltero betu / hianyzo betu / betu a jeloles utan: SERTES
        for rossz in ('Ezsd 6:8c [BDB: Ezsd 16:8c] itt', 'Ezsd 6:8 [BDB: Ezsd 16:8] itt',
                      'Ezsd 6:8 [BDB: Ezsd 16:8]b itt', 'Ezsd 6:8b [BDB: Ezsd 16:8] itt'):
            self.assertEqual(self.kapu(f, rossz, strong='H0479')[0], 'SERTES', rossz)
        # betu nelkuli forras: valtozatlan; a betu a szo elejen nem versfel-betu
        self.assertEqual(self.kapu('Ezra 16:8 itt', 'Ezsd 6:8 [BDB: Ezsd 16:8] itt', strong='H0479')[0], 'RENDBEN')
        self.assertEqual(self.kapu('Ezra 16:8 and', 'Ezsd 6:8 [BDB: Ezsd 16:8] and', strong='H0479')[0], 'RENDBEN')

    def test_versfel_betu_visszaallitas_es_tobbi_kapu(self):
        self.assertEqual(K.bdb_jeloles_vissza('Ezsd 6:8b [BDB: Ezsd 16:8b] itt'), 'Ezsd 16:8b itt')
        e = dict((n, x) for n, x, _ in K.kapuk_futtat('BDB', 'Ezra 16:8b itt', 'Ezsd 6:8b [BDB: Ezsd 16:8b] itt', strong='H0479'))
        self.assertEqual((e['2_versszam'], e['11_konyvek'], e['17_bdb_javitas']), ('RENDBEN', 'RENDBEN', 'RENDBEN'))

    def test_tobbszori_elofordulas(self):
        f = 'Eccl 17:10 es Eccl 17:10'
        self.assertEqual(self.kapu(f, 'Préd 7:10 [BDB: Préd 17:10] es Préd 7:10 [BDB: Préd 17:10]')[0], 'RENDBEN')
        e, d = self.kapu(f, 'Préd 7:10 [BDB: Préd 17:10] es Préd 17:10')
        self.assertEqual(e, 'SERTES')
        self.assertIn('forrás ×2, jelölt ×1', d)

    def test_nincs_tablasor(self):
        self.assertEqual(self.kapu('semmi', 'semmi', strong='H9999')[0], 'RENDBEN')
        self.assertEqual(self.kapu('semmi', 'Préd 7:10 [BDB: Préd 17:10]', strong='H9999')[0], 'SERTES')

    def test_strong_nelkul_es_thayer_nem_gatol(self):
        self.assertEqual(K.ellenoriz_bdb_javitas('BDB', self.F, 'A fold. Préd 7:10 mondja.')[0], 'RENDBEN')
        self.assertEqual(self.kapu(self.F, 'bármi', strong='G0012', szotar='Thayer')[0], 'RENDBEN')

    def test_kapusor_strong_nelkul_bajtra_azonos(self):
        f, h = 'to surname Eccl 17:10', 'melléknéven nevezni Préd 7:10 [BDB: Préd 17:10]'
        mostani = K.kapuk_futtat('BDB', f, h)
        self.assertNotIn('17_bdb_javitas', [n for n, _, _ in mostani])
        strongos = K.kapuk_futtat('BDB', f, h, strong='H7223')
        self.assertEqual([x for x in strongos if x[0] != '17_bdb_javitas'], mostani)
        self.assertEqual(strongos[-1][:2], ('17_bdb_javitas', 'RENDBEN'))
        self.assertEqual(K.kapuk_futtat('Thayer', f, h, strong='G0012'), K.kapuk_futtat('Thayer', f, h))

    def test_gatol(self):
        self.assertIn('17_bdb_javitas', K.GATOLO)
        e = K.kapuk_futtat('BDB', self.F, 'A fold. Préd 7:10 mondja.', strong='H7223')
        self.assertFalse(K.atment(e))

    def test_szakaszos(self):
        f = '⟪1⟫ szó. A fold. Eccl 17:10 mondja. ⟪2⟫ 2 más'
        jo = '⟪1⟫ szó. A fold. Préd 7:10 [BDB: Préd 17:10] mondja. ⟪2⟫ 2 más'
        rossz = '⟪1⟫ szó. A fold. Préd 7:10 mondja. ⟪2⟫ 2 más'
        e = dict((n, x) for n, x, _ in K.kapuk_futtat_szakaszos('BDB', f, jo, strong='H7223'))
        self.assertEqual(e['17_bdb_javitas'], 'RENDBEN')
        e = dict((n, x) for n, x, _ in K.kapuk_futtat_szakaszos('BDB', f, rossz, strong='H7223'))
        self.assertEqual(e['17_bdb_javitas'], 'SERTES')
        nevek = [n for n, _, _ in K.kapuk_futtat_szakaszos('BDB', f, jo)]
        self.assertNotIn('17_bdb_javitas', nevek)

    def test_onallo_jeloles_tabla_nelkuli_strongnal(self):
        e, d = self.kapu('semmi', 'szo [BDB: Préd 17:10] szo', strong='H9999')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jogosulatlan: [BDB: Préd 17:10]', d)

    def test_onallo_jeloles_csak_jelolt_marad_sorral(self):
        e, d = self.kapu('Esth 11:32 itt', 'Eszt 11:32 [BDB: Eszt 11:32] itt', strong='H0001')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jogosulatlan', d)
        e, d = self.kapu('Esth 11:32 itt', 'itt [BDB: Eszt 11:32] itt', strong='H0001')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jogosulatlan: [BDB: Eszt 11:32]', d)

    def test_onallo_jeloles_javitva_sorral_y_nelkul(self):
        e, d = self.kapu(self.F, 'A fold. Préd 7:10 mondja [BDB: Préd 17:10].')
        self.assertEqual(e, 'SERTES')
        self.assertIn('jogosulatlan: [BDB: Préd 17:10]', d)
        e, d = self.kapu(self.F, 'A fold. a [BDB: Préd 17:10] mondja.')
        self.assertEqual(e, 'SERTES')

    def test_homograf_kulcs(self):
        self.assertEqual(K._strong_kulcs('H90a'), 'H0090a')
        self.assertEqual(K._strong_kulcs('H7223'), 'H7223')


if __name__ == '__main__':
    unittest.main(verbosity=2)
