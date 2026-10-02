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


if __name__ == '__main__':
    unittest.main(verbosity=2)
