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


if __name__ == '__main__':
    unittest.main(verbosity=2)
