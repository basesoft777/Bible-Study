#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_normalizal.py -- F28_EMELES_BRIEF.md E2: az
eszkozok/normalizal.py szabalyainak tesztjei (szabalyonként legalabb egy
pozitiv es egy negativ eset, meg a szotaranként kapcsolhatosag).

    python eszkozok/teszt_normalizal.py
    python -m unittest eszkozok/teszt_normalizal.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import normalizal as N  # noqa: E402


class KkK(unittest.TestCase):
    def test_ff_kk(self):
        self.assertEqual(N.szabaly_kk_k('Róm 5:12ff.; Jak 1:2 ff')[0], 'Róm 5:12kk.; Jak 1:2 kk.')

    def test_f_k(self):
        self.assertEqual(N.szabaly_kk_k('1Móz 2:4 f., 7')[0], '1Móz 2:4 k., 7')

    def test_bdb_nf_nem_valtozik(self):
        # a BDB `n.f.` (noun feminine) es a szo belseji f nem csere
        szoveg = 'נֶפֶשׁ n.f. lélek; ff-alak, ref. 3'
        self.assertEqual(N.szabaly_kk_k(szoveg), (szoveg, 0))

    def test_mar_kk_nem_valtozik(self):
        self.assertEqual(N.szabaly_kk_k('Mt 5:3kk.')[1], 0)


class Szerzonevek(unittest.TestCase):
    def test_philo(self):
        self.assertEqual(N.szabaly_szerzonevek('(Philo, Deus immut. 14. §)')[0], '(Philón, Deus immut. 14. §)')

    def test_filon_plutarch_tertullian(self):
        uj, n = N.szabaly_szerzonevek('Filón; Plutarch; Tertullian; Josephusz')
        self.assertEqual(uj, 'Philón; Plutarkhosz; Tertullianus; Josephus')
        self.assertEqual(n, 4)

    def test_toldalekos_alak_marad(self):
        szoveg = 'Philónnál, Plutarkhosznál, Philo-kiadás'
        self.assertEqual(N.szabaly_szerzonevek(szoveg), (szoveg, 0))

    def test_konyvcimben_birtokos_marad(self):
        # német/angol cím: Philo's Lehre ... (G0012) -- nem szerzőnév-alak
        szoveg = "J. G. Müller, Philo's Lehre von der Weltschöpfung"
        self.assertEqual(N.szabaly_szerzonevek(szoveg), (szoveg, 0))

    def test_mar_helyes_alak_marad(self):
        szoveg = 'Philón és Josephus; Plutarkhosz'
        self.assertEqual(N.szabaly_szerzonevek(szoveg), (szoveg, 0))


class IgehelyRov(unittest.TestCase):
    def test_bdb_alakok(self):
        uj, n = N.szabaly_igehely_rov('Exod 12:3; Judg 14:10; 1Kin 18:24; Ps. 79:6')
        # a `Ps.` nincs a listan -> marad (a kapu jelzi)
        self.assertEqual(uj, '2Móz 12:3; Bír 14:10; 1Kir 18:24; Ps. 79:6')
        self.assertEqual(n, 3)

    def test_thayer_es_stepbible_alakok(self):
        uj, _ = N.szabaly_igehely_rov('Joh 3:16; Mat 5:3; Song of Solomon 2:4; Rev 1:8')
        self.assertEqual(uj, 'Ján 3:16; Mt 5:3; Én 2:4; Jel 1:8')

    def test_lam_jsir(self):
        # DT24 (a): a Jeremiás siralmai Károli-rövidítése JSir, nem Sir
        # (a Sir a Sirák fia könyvével ütközne)
        uj, n = N.szabaly_igehely_rov('Lam 3:57; Lam. 4:2')
        self.assertEqual(uj, 'JSir 3:57; JSir 4:2')
        self.assertEqual(n, 2)
        self.assertEqual(N.KAROLI['Lam'][0], 'JSir')
        self.assertNotIn('Sir', N._KAROLI_ROV)

    def test_tabla_forras_alakjai(self):
        # F38, DT-F38 (c): a Konyv_normalizalo_tabla.tsv `Forrás-alakok` oszlopa
        uj, n = N.szabaly_igehely_rov(
            'Ex 7:29; Cant 7:2; Songs 7:14; 1Chron 16:8; I Chron 15:13; 2 Chron 12:20; '
            '2Che 22:11; Malachi 3:19; Ezekiel 16:4; Daniel 3:5; Proverbs 5:26; Nah 1:11; '
            'Esther 1:9; 1 Sam 28:3; 1 Ki 5:20; Haggai 1:15; Habakkuk 1:15; Paslm 119:93; '
            'Plalm 149:1; James 5:4; Titus 2:14')
        self.assertEqual(
            uj,
            '2Móz 7:29; Én 7:2; Én 7:14; 1Krón 16:8; 1Krón 15:13; 2Krón 12:20; '
            '2Krón 22:11; Mal 3:19; Ez 16:4; Dán 3:5; Péld 5:26; Náh 1:11; '
            'Eszt 1:9; 1Sám 28:3; 1Kir 5:20; Hag 1:15; Hab 1:15; Zsolt 119:93; '
            'Zsolt 149:1; Jak 5:4; Tit 2:14')
        self.assertEqual(n, 21)
        self.assertEqual(N.TABLA_ALAKOK['Cant'], 'Sng')

    def test_tabla_forras_alak_csak_igehely_elott(self):
        # Daniel/James/Titus szemelynevkent, Proverbs folyo szovegben nem csere
        szoveg = 'Daniel próféta; James Barr; Titus 2 fejezete; Ex. Proverbs'
        self.assertEqual(N.szabaly_igehely_rov(szoveg), (szoveg, 0))

    def test_tobbertelmu_alak_nincs_a_tablaban(self):
        # a szam nelkuli Kings / Chron / Samuel nem egyertelmu (1 vagy 2) -> nincs lekepezes
        for a in ('Kings', 'Chron', 'Chronicles', 'Samuel', 'Ki', 'Sam'):
            self.assertNotIn(a, N.IGE_LEK, a)

    def test_tabla_szerkezet_valtozatlan(self):
        # a tabla 66 sora, az elso harom oszlop sorrendje (mas fogyasztok erre epulnek)
        sorok = open(N.KAROLI_UT, encoding='utf-8').read().split('\n')
        self.assertEqual(sorok[0].split('\t'),
                         ['STEPBible-rövidítés', 'Magyar rövidítés', 'Teljes magyar könyvnév', 'Forrás-alakok'])
        adat = [s for s in sorok[1:] if s.strip()]
        self.assertEqual(len(adat), 66)
        self.assertTrue(all(len(s.split('\t')) == 4 for s in adat))

    def test_karoli_alak_marad(self):
        szoveg = '1Móz 4:26; Jer 10:25; Gal 3:13'
        self.assertEqual(N.szabaly_igehely_rov(szoveg), (szoveg, 0))

    def test_csak_igehely_elott(self):
        # fejezet:vers nelkul nem csere (Job mint szo, Mark mint nev)
        szoveg = 'Job könyvében; Mark 3 fejezet'
        self.assertEqual(N.szabaly_igehely_rov(szoveg), (szoveg, 0))


class Konyvnevek(unittest.TestCase):
    def test_folyo_szoveg(self):
        uj, n = N.szabaly_konyvnevek('a Hebrews és a Revelation kétszer')
        self.assertEqual(uj, 'a Zsidókhoz írt levél és a Jelenések könyve kétszer')
        self.assertEqual(n, 2)

    def test_igehely_elott_nem(self):
        szoveg = 'Song of Solomon 2:4'
        self.assertEqual(N.szabaly_konyvnevek(szoveg), (szoveg, 0))

    def test_angol_konyvcim_nem(self):
        # G0086: E. R. Craven in Lange on Revelation -- könyvcím
        szoveg = 'E. R. Craven in Lange on Revelation, 364–377. o.'
        self.assertEqual(N.szabaly_konyvnevek(szoveg), (szoveg, 0))

    def test_szemelynevek_nem(self):
        szoveg = 'Mark, John, James és Jude'
        self.assertEqual(N.szabaly_konyvnevek(szoveg), (szoveg, 0))


class TapadtKonyvjelzes(unittest.TestCase):
    """F38.261, DT-F38d (c): a kisbetus szohoz tapadt angol konyvjelzes."""

    def test_tapadt_leval_es_karoli(self):
        self.assertEqual(N.szabaly_igehely_rov('abundantly2Chr 3:1')[0], 'abundantly 2Krón 3:1')
        self.assertEqual(N.szabaly_igehely_rov('completely2Chr 4:2; verbDeuteronomy 7:8')[0],
                         'completely 2Krón 4:2; verb 5Móz 7:8')

    def test_tapadt_szamlalo(self):
        self.assertEqual(N.szabaly_igehely_rov('abundantly2Chr 3:1')[1], 1)

    def test_normalis_igehely_nem_valtozik_masként(self):
        self.assertEqual(N.szabaly_igehely_rov('l. 2Chr 3:1')[0], 'l. 2Krón 3:1')

    def test_nagybetu_utan_nem_tapad(self):
        # nagybetu elott nem kisbetu: nem tapadt jelzes
        szoveg = 'ABC2Chr 3:1'
        self.assertEqual(N.szabaly_igehely_rov(szoveg), (szoveg, 0))

    def test_ige_szam_nelkul_nem(self):
        szoveg = 'verbDeuteronomy es egyeb'
        self.assertEqual(N.szabaly_igehely_rov(szoveg), (szoveg, 0))

    def test_teljes_lanc_bdb(self):
        self.assertEqual(N.normalizal('abundantly2Chr 3:1', 'BDB')[0], 'abundantly 2Krón 3:1')


class Kapcsolhatosag(unittest.TestCase):
    def test_teljes_lanc(self):
        uj, valt = N.normalizal('Philo; Exod 12:3ff.', 'BDB')
        self.assertEqual(uj, 'Philón; 2Móz 12:3kk.')
        self.assertEqual(dict(valt), {'igehely_rov': 1, 'kk_k': 1, 'szerzonevek': 1})

    def test_kikapcsolas(self):
        uj, valt = N.normalizal('Philo; Exod 12:3ff.', 'BDB', kikapcsolt=('szerzonevek',))
        self.assertEqual(uj, 'Philo; 2Móz 12:3kk.')
        self.assertNotIn('szerzonevek', dict(valt))

    def test_szotaronkent(self):
        eredeti = dict((k, set(v)) for k, v in N.SZABALYOK.items())
        try:
            N.SZABALYOK['kk_k'] = {'Thayer'}
            self.assertEqual(N.normalizal('1Móz 2:4 f.', 'BDB')[0], '1Móz 2:4 f.')
            self.assertEqual(N.normalizal('Mt 2:4 f.', 'Thayer')[0], 'Mt 2:4 k.')
        finally:
            N.SZABALYOK.clear()
            N.SZABALYOK.update(eredeti)

    def test_heber_gorog_erintetlen(self):
        szoveg = 'קָרָא Qal; ἀγάπη, -ης, ἡ'
        self.assertEqual(N.normalizal(szoveg, 'BDB'), (szoveg, []))


class TapadtKarolialak(unittest.TestCase):
    """F38.267: a mar Karoli-alakban tapadt konyvjelzes (`Dávidot2Krón 13:8`) is leválik."""

    def test_karoli_alak_tapadt(self):
        self.assertEqual(N.szabaly_igehely_rov('megöli Dávidot2Krón 13:8; 32:1')[0],
                         'megöli Dávidot 2Krón 13:8; 32:1')

    def test_heber_es_hosszu_ekezetes_utan(self):
        self.assertEqual(N.szabaly_igehely_rov('דָּן2Krón 2:13; hercegnő2Krón 22:11')[0],
                         'דָּן 2Krón 2:13; hercegnő 2Krón 22:11')

    def test_niqqud_vegu_heber_szo_utan(self):
        self.assertEqual(N.szabaly_igehely_rov('גְּדוֺלֶיהָNáh 3:10; רוּחַ2Kir 2:15')[0],
                         'גְּדוֺלֶיהָ Náh 3:10; רוּחַ 2Kir 2:15')

    def test_szokozzel_allo_valtozatlan(self):
        self.assertEqual(N.szabaly_igehely_rov('Dávidot 2Krón 13:8; Zsolt 5:1')[1], 0)

    def test_szamjegy_utan_nem_tapadt(self):
        # `1Kor 3:2` a `1`+`Kor`: a lookbehind kisbetut var, nem szamjegyet
        self.assertEqual(N.szabaly_igehely_rov('l. 2Kor 3:2')[1], 0)

    def test_igehely_nelkuli_szo_nem(self):
        self.assertEqual(N.szabaly_igehely_rov('a bűnösjer kifejezés')[1], 0)


class Elofordulas(unittest.TestCase):
    """F38.266 (DT-F38e): `N t.` -> `N-szor` (a toldalek a kiejtett szam szerint)."""

    def test_alapalakok(self):
        self.assertEqual(N.szabaly_elofordulas('33 t.')[0], '33-szor')
        self.assertEqual(N.szabaly_elofordulas('(26 t.)')[0], '(26-szor)')
        self.assertEqual(N.szabaly_elofordulas('Hag 1:14 (3 t. a versben); 4')[0],
                         'Hag 1:14 (a versben 3-szor); 4')

    def test_szokoz_nelkuli_es_zaro_jelek(self):
        self.assertEqual(N.szabaly_elofordulas('322t.; (117 t.): (116 t.).')[0],
                         '322-szer; (117-szer): (116-szor).')

    def test_magashangrendu_es_melyhangrendu(self):
        for n, v in ((3, 'szor'), (4, 'szer'), (5, 'ször'), (10, 'szer'), (20, 'szor'), (40, 'szer'),
                     (45, 'ször'), (100, 'szor'), (2, 'szer'), (7, 'szer'), (8, 'szor'), (9, 'szer')):
            self.assertEqual(N.szor_toldalek(n), v, n)

    def test_igehely_utani_szam_nem_gyakorisag(self):
        szoveg = '1Móz 22:3 t. és 5:12 t. stb.; 2-3 t.'
        self.assertEqual(N.szabaly_elofordulas(szoveg), (szoveg, 0))

    def test_tartomanyos_alak_darabszama(self):
        # DT-F38f (4): `5Móz 11:13-14t.` = `5Móz 11:13 + 14 t.` (a `-` után a darabszám áll)
        self.assertEqual(N.szabaly_elofordulas('5Móz 11:13-14t.; továbbá'),
                         ('5Móz 11:13, összesen 14-szer; továbbá', 1))
        self.assertEqual(N.szabaly_elofordulas('Ézs 65:1-2t.; imperfectum'),
                         ('Ézs 65:1, összesen 2-szer; imperfectum', 1))
        self.assertEqual(N.szabaly_elofordulas('Jer 25:3-4t. Jeremiás; Ez 1:3, 5'),
                         ('Jer 25:3, összesen 4-szer Jeremiás; Ez 1:3, 5', 1))
        self.assertEqual(N.szabaly_elofordulas('4Móz 7:14-15t. a 4Móz 7-ben')[0],
                         '4Móz 7:14, összesen 15-ször a 4Móz 7-ben')

    def test_pont_marad_tagolasi_szam_elott(self):
        # `4t. 2 twelve:` -> a 9. kapu (tagolás) csak `.;:—)` utáni számot ismer fel jelölőnek
        self.assertEqual(N.szabaly_elofordulas('Jer 1:3-4t. 2 tizenkettő: a.')[0],
                         'Jer 1:3, összesen 4-szer. 2 tizenkettő: a.')
        self.assertEqual(N.szabaly_elofordulas('(3 t.) 2 tizenkettő')[0], '(3-szor) 2 tizenkettő')
        self.assertEqual(N.szabaly_elofordulas('4 t. 2 tizenkettő')[0], '4-szer. 2 tizenkettő')

    def test_tartomanyos_alak_hataresetek(self):
        # valódi versszám-tartomány `t.` nélkül, szóközös alak, számtartomány: változatlan
        for szoveg in ('2Móz 4:8-9, 4Móz 15:24', 'Ézs 65:1-2 t.', '2-3t.', 'Gen 3:4-5; 6t'):
            self.assertEqual(N.szabaly_elofordulas(szoveg), (szoveg, 0), szoveg)

    def test_paragrafus_utan_nem_gyakorisag(self):
        # Ges §67 t. = a nyelvtan 67. §-ának t) pontja
        self.assertEqual(N.szabaly_elofordulas('Ges §67 t.) szerint'), ('Ges §67 t.) szerint', 0))

    def test_mas_t_rovidites_valtozatlan(self):
        szoveg = 'a t. termést; ahol t. = tárgyeset'
        self.assertEqual(N.szabaly_elofordulas(szoveg)[1], 0)

    def test_csak_bdb(self):
        self.assertEqual(N.normalizal('33 t.', 'Thayer')[0], '33 t.')
        self.assertEqual(N.normalizal('33 t.', 'BDB')[0], '33-szor')


class Nevalakok(unittest.TestCase):
    def test_izrael_izrael(self):
        self.assertEqual(N.szabaly_nevalakok('Izrael, Izraelről, az Izraellel')[0],
                         'Izráel, Izráelről, az Izráellel')

    def test_mar_helyes_es_izraelita_valtozatlan(self):
        szoveg = 'Izráel; izraelita; Izraelita; Jezréel'
        self.assertEqual(N.szabaly_nevalakok(szoveg)[1], 0)

    def test_csak_bdb(self):
        self.assertEqual(N.normalizal('Izrael', 'Thayer')[0], 'Izrael')
        self.assertEqual(N.normalizal('Izrael', 'BDB')[0], 'Izráel')


class KonyvRov(unittest.TestCase):
    def test_1pt_1pet(self):
        self.assertEqual(N.szabaly_konyv_rov('1Pt 2:3; 2Pt 1:1')[0], '1Pét 2:3; 2Pét 1:1')

    def test_sziglaja_utan(self):
        self.assertEqual(N.szabaly_konyv_rov('δόξα ᵐ51Pt 1:24 és')[0], 'δόξα ᵐ51Pét 1:24 és')

    def test_a_tablabeli_alak_a_merveado(self):
        self.assertEqual(N.KAROLI['1Pe'][0], '1Pét')

    def test_igehely_nelkuli_nem(self):
        self.assertEqual(N.szabaly_konyv_rov('az 1Pt kifejezés')[1], 0)

    def test_mar_helyes_valtozatlan(self):
        self.assertEqual(N.szabaly_konyv_rov('1Pét 2:3')[1], 0)


class GlosszaVisszaallit(unittest.TestCase):
    """F38.266: az RV/AV angol glosszaja angolul marad."""

    def test_lefordult_glossza_visszaall(self):
        uj, valt = N.glossza_visszaallit('(RV breath) 33:11', '(RV: lehelet) 33:11')
        self.assertEqual(uj, '(RV breath) 33:11')
        self.assertEqual(valt, [('RV: lehelet', 'RV breath')])

    def test_elvalaszto_nelkuli_es_vesszos_hatar(self):
        uj, _ = N.glossza_visszaallit('RV besides; de', 'RV mellett; de')
        self.assertEqual(uj, 'RV besides; de')
        uj, _ = N.glossza_visszaallit('RV against, see Ew', 'RV: valami ellen, l. Ew')
        self.assertEqual(uj, 'RV against, l. Ew')

    def test_tobb_szavas_glossza(self):
        uj, _ = N.glossza_visszaallit('(AV because of Gedaliah), read x', '(AV: Gedalja miatt), olv. x')
        self.assertEqual(uj, '(AV because of Gedaliah), olv. x')

    def test_mar_angol_valtozatlan(self):
        f = 'AV slacken me not, x'
        self.assertEqual(N.glossza_visszaallit(f, f), (f, []))

    def test_nem_glossza_mondatresz_valtozatlan(self):
        for f, h in (('RV renders sin-offering; de', 'RV fordítása sin-offering; de'),
                     ('RV and others in the heart of)', 'RV és mások: in the heart of)'),
                     ('RV Di and others; (', 'RV Di és mások; ('),
                     ('RVm, but order of words difficult;', 'RVm, de a szórend nehéz;')):
            self.assertEqual(N.glossza_visszaallit(f, h), (h, []), f)

    def test_jelek_szama_elter_valtozatlan(self):
        self.assertEqual(N.glossza_visszaallit('RV breath) x', 'RV: lehelet) RV'), ('RV: lehelet) RV', []))

    def test_zaro_jel_elter_valtozatlan(self):
        self.assertEqual(N.glossza_visszaallit('RV breath) x', 'RV: lehelet; x'), ('RV: lehelet; x', []))


if __name__ == '__main__':
    unittest.main(verbosity=2)
