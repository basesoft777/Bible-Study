#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_megfelelo_kinyer.py -- F178 javítókör (ELLENOR_F178 3., 4.): a visszhang kinyerő táblájának
`ellenorzes` mezője csak azt mondja, ami megtörtént. A kód nem állít kézi átnézést (az az átnézés-bemenet sorából jön),
az üres alak nem gépi egyezés, a kinyerő nem ellenőrizheti magát, és az ellenőri lemma-egységesítés második kéz (nem az ellenőr)
megerősítése nélkül ellenőrizetlen. Fájlt nem ír. A `teszt_futtat.py --gyors` része.

    python eszkozok/teszt_futtat.py --fajl teszt_megfelelo_kinyer
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ESZKOZOK, 'visszhang'))
import megfelelo_kinyer as MK  # noqa: E402

KINYERO, ELLENOR, HARMADIK = 'kinyero-modell', 'ellenor-modell', 'harmadik-modell'


def sor(**k):
    r = {o: '' for o in MK.OSZLOPOK}
    r.update(motivum='M-001', strong='H0001', igehely='1Móz 1:1', forras='vulgata', alak='terra', lemma='terra',
             kinyeres='modell', modell=KINYERO)
    r.update(k)
    return r


def atnezes(r, itelet='jo', atnezo=ELLENOR):
    return {MK.atnezes_kulcs(r): {'atnezo': atnezo, 'itelet': itelet, 'megjegyzes': ''}}


class GepiEgyezes(unittest.TestCase):
    def test_ures_alak_nem_egyezes(self):
        self.assertFalse(MK.gepi_egyezik('', 'In principio terra', lambda x: x))
        self.assertFalse(MK.gepi_egyezik('  ', 'In principio terra', lambda x: x))

    def test_alak_a_szovegben(self):
        self.assertTrue(MK.gepi_egyezik('terra', 'In principio terra', lambda x: x))
        self.assertTrue(MK.gepi_egyezik('principio · terra', 'In principio terra', lambda x: x))
        self.assertFalse(MK.gepi_egyezik('principio · cælum', 'In principio terra', lambda x: x))


class EllenorzesMezo(unittest.TestCase):
    def ell(self, r, jo, atn=None, meg=None, ellenor=ELLENOR):
        return MK.ellenorzes_mezo(r, jo, atn or {}, meg or {}, ellenor, '2026-11-08')

    def test_kezi_atnezes_nelkul_ellenorizetlen(self):
        mezo, ok = self.ell(sor(), True)
        self.assertEqual(mezo, '')
        self.assertIn('nincs kézi átnézés', ok)

    def test_kod_nem_allit_kezi_atnezest(self):
        # a régi kód minden gépi egyezésre beírta: „a megfelelés kézzel átnézve”
        mezo, _ = self.ell(sor(), True)
        self.assertNotIn('kézzel átnézve', mezo)

    def test_atnezessel_ellenorzott(self):
        r = sor()
        mezo, ok = self.ell(r, True, atnezes(r))
        self.assertIsNone(ok)
        self.assertTrue(mezo.startswith(ELLENOR + ', 2026-11-08: kézi átnézés'))
        self.assertIn('gépi összevetés', mezo)

    def test_elvetett_atnezes(self):
        r = sor()
        mezo, ok = self.ell(r, True, atnezes(r, itelet='elvet'))
        self.assertEqual(mezo, '')
        self.assertIn('elvetette', ok)

    def test_gepileg_nem_egyezo_alak_atnezessel_sem(self):
        r = sor()
        mezo, ok = self.ell(r, False, atnezes(r))
        self.assertEqual(mezo, '')
        self.assertIn('nem áll a forrásban', ok)

    def test_ures_alak_atnezessel_nem_gepi_egyezes(self):
        r = sor(alak='', megjegyzes='nincs megfelelő szó')
        mezo, ok = self.ell(r, False, atnezes(r))
        self.assertIsNone(ok)
        self.assertNotIn('szó szerint áll', mezo)
        self.assertIn('alak nélküli sor', mezo)

    def test_ures_alak_atnezes_nelkul_ellenorizetlen(self):
        mezo, _ = self.ell(sor(alak=''), False)
        self.assertEqual(mezo, '')

    def test_kinyero_nem_ellenorizheti_magat(self):
        r = sor(modell=ELLENOR)
        mezo, ok = self.ell(r, True, atnezes(r))
        self.assertEqual(mezo, '')
        self.assertIn('ugyanaz', ok)

    def test_atnezo_mas_mint_az_ellenor(self):
        r = sor()
        mezo, _ = self.ell(r, True, atnezes(r, atnezo=HARMADIK))
        self.assertEqual(mezo, '')

    def test_lemma_egysegesites_megerosites_nelkul(self):
        r = sor(megjegyzes='%s: egy gyök]' % MK.LEMMA_JEL)
        mezo, ok = self.ell(r, True, atnezes(r))
        self.assertEqual(mezo, '')
        self.assertIn('második kéz', ok)

    def test_lemma_egysegesites_az_ellenor_nem_erositheti_meg(self):
        r = sor(megjegyzes='%s: egy gyök]' % MK.LEMMA_JEL)
        meg = {('M-001', 'H0001', '1Móz 1:1', 'vulgata'): {'itelet': 'megerosit', 'lemma_a_tablaban': 'terra',
                                                           'modell': ELLENOR}}
        mezo, _ = self.ell(r, True, atnezes(r), meg)
        self.assertEqual(mezo, '')

    def test_lemma_egysegesites_harmadik_kez_megerositi(self):
        r = sor(megjegyzes='%s: egy gyök]' % MK.LEMMA_JEL)
        meg = {('M-001', 'H0001', '1Móz 1:1', 'vulgata'): {'itelet': 'megerosit', 'lemma_a_tablaban': 'terra',
                                                           'modell': KINYERO}}
        mezo, ok = self.ell(r, True, atnezes(r), meg)
        self.assertIsNone(ok)
        self.assertTrue(mezo)

    def test_megerosites_mas_lemmara_nem_er(self):
        r = sor(megjegyzes='%s: egy gyök]' % MK.LEMMA_JEL)
        meg = {('M-001', 'H0001', '1Móz 1:1', 'vulgata'): {'itelet': 'megerosit', 'lemma_a_tablaban': 'humus',
                                                           'modell': KINYERO}}
        mezo, _ = self.ell(r, True, atnezes(r), meg)
        self.assertEqual(mezo, '')


class AtnezesBemenet(unittest.TestCase):
    """ELLENOR_F178_2 2.: az átnézés-bemenet soronkénti, érdemi ítélet — sablonmondat, indok nélküli sor és kettőzött
    kulcs nem fogadható el; a `bdb` sornál a nyelv és a jelentés is kulcs."""
    def at(self, i, megj, **k):
        r = sor(igehely='1Móz 1:%d' % i, **k)
        r.update(atnezo=ELLENOR, itelet='jo', megjegyzes=megj)
        return r

    def test_erdemi_bemenet_rendben(self):
        self.assertEqual([], MK.atnezes_ellenoriz([self.at(i, 'a %d. vers terra szava a héber szó helyén' % i)
                                                   for i in range(1, 11)]))

    def test_csupa_azonos_megjegyzes_hiba(self):
        hibak = MK.atnezes_ellenoriz([self.at(i, 'a megfelelés helyes') for i in range(1, 11)])
        self.assertTrue(any(h.startswith('sablonmondat') for h in hibak))

    def test_kevés_ismetles_megengedett(self):
        sorok = [self.at(i, 'egyedi indok %d' % i) for i in range(1, 8)] +                 [self.at(i, 'közös indok') for i in range(8, 11)]
        self.assertEqual([], MK.atnezes_ellenoriz(sorok))

    def test_indok_nelkul_hiba(self):
        self.assertTrue(MK.atnezes_ellenoriz([self.at(1, '')]))

    def test_bdb_kulcs_a_nyelvvel_es_jelentessel(self):
        a = sor(forras='bdb', igehely='', alak='', lemma='újhéber', jelentes='fájdalmat érez')
        b = sor(forras='bdb', igehely='', alak='', lemma='újhéber', jelentes='formába nyújt')
        c = sor(forras='bdb', igehely='', alak='', lemma='etióp', jelentes='fájdalmat érez')
        self.assertEqual(3, len({MK.atnezes_kulcs(x) for x in (a, b, c)}))
        # a nem bdb sor kulcsa változatlan
        self.assertEqual(('M-001', 'H0001', '1Móz 1:1', 'vulgata', 'terra'), MK.atnezes_kulcs(sor()))

    def test_kettozott_kulcs_hiba(self):
        self.assertTrue(any('többször' in h for h in MK.atnezes_ellenoriz([self.at(1, 'x'), self.at(1, 'y')])))


class LxxSzorend(unittest.TestCase):
    """ELLENOR_F178 7.: az 1Móz 3:16 „λύπας · λύπαις” sorából a második a בְּעֶצֶב (H6089) megfelelője."""
    TOK = [{'szoalak': 'λύπας', 'lemma': 'λύπη', 'strong': '3077'},
           {'szoalak': 'λύπαις', 'lemma': 'λύπη', 'strong': '3077'}]

    def test_rivalis_rovid_jelentes_szerint(self):
        # 1Móz 3:16 (TAHOT): עִצָּבוֹן „toil”, עֶצֶב „toil” — társulási adat nélkül a rövid jelentés dönt
        heber = [('H7235', 'multiply'), ('H6093', 'toil'), ('H2032', 'conception'), ('H6089', 'toil'), ('H3205', 'beget')]
        tok, riv = MK.szorend_szerint(self.TOK, 'H6093', heber, lambda h: None)
        self.assertEqual([t['szoalak'] for t in tok], ['λύπας'])
        self.assertEqual(riv, ['H6089'])

    def test_mas_jelentes_nem_rivalis(self):
        # 1Móz 7:23: אָדָם „man” nem rivális az אֲדָמָה „land” mellett, az אֶרֶץ „land” igen
        tok3 = self.TOK
        heber = [('H0127', 'land'), ('H0120', 'man'), ('H0776', 'land')]
        tok, riv = MK.szorend_szerint(tok3, 'H0127', heber, lambda h: None)
        self.assertEqual(riv, ['H0776'])
        self.assertEqual([t['szoalak'] for t in tok], ['λύπας'])

    def test_tarsulasi_adattal_a_jelentes_nem_dont(self):
        # ha a rivális héber szónak van társulási adata, és az más szócsalád, az azonos rövid jelentés nem elég
        heber = [('H6093', 'toil'), ('H6089', 'toil')]
        tok, riv = MK.szorend_szerint(self.TOK, 'H6093', heber, lambda h: {'xyz'})
        self.assertEqual(len(tok), 2)
        self.assertEqual(riv, [])

    def test_ket_heber_elofordulas_ket_gorog(self):
        heber = [('H7843', 'destroy'), ('H7843', 'destroy')]
        tok, riv = MK.szorend_szerint(self.TOK, 'H7843', heber, lambda h: None)
        self.assertEqual(len(tok), 2)
        self.assertEqual(riv, [])


class Szocsalad(unittest.TestCase):
    """A javítókör lelete: az előtagos alak eleje („κατ”) nem tő, különben minden κατα-szó egy család."""
    def test_kata_elotag_nem_kozos_to(self):
        self.assertFalse(MK.szocsalad('κατακλυσμός') & MK.szocsalad('καταφθείρω'))

    def test_valodi_csalad_megmarad(self):
        self.assertTrue(MK.szocsalad('φθείρω') & MK.szocsalad('καταφθείρω'))
        self.assertTrue(MK.szocsalad('ἐπικατάρατος') & MK.szocsalad('καταράομαι'))
        self.assertTrue(MK.szocsalad('λύπη') & MK.szocsalad('λύπη'))


if __name__ == '__main__':
    unittest.main()
