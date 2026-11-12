"""teszt_f194_szopar.py -- F194 (az ISTENTISZT-001 2. kiadása, az új lapszerkezet): a két kapu a szópáros (formulaikus)
motívumon.

1. `lxx_egyezes_kapu(..., szopar=True)`: a pár minden tagja a motívum minden ószövetségi versében áll, ezért a héber 4.6
   szavankénti mondatai nem összeadódnak, hanem mindegyik a teljes versszámot mondja.
2. `lxx_egyforras_ellenoriz`: a 4.11-sor több lemmát is hordozhat ` · `-tal (1Kir 18:24: βοάω · ἐπικαλέω); a kapu
   mindegyiket a cellában keresi, nem az egész szöveget egy szóként.

Futtatás: python eszkozok/teszt_f194_szopar.py
"""
import os
import sys
import unittest

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)

import lexikon_general as LG  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

OSSZESITES = ('*Összesítés: egyező=13, ugyanaz a szócsalád=2, eltérő=0, nincs újszövetségi pár=0, LXX-minusz=0, '
              'a megfelelő nincs megállapítva=1, versszámozás miatt nem párosítva=0.*')


class Szoparkapu(unittest.TestCase):
    def lap(self, a='16', b='16'):
        return '\n\n'.join([
            'A motívum ószövetségi helyei 16 versre terjednek.',
            'Az x a motívum %s ószövetségi versében áll.' % a, 'Az y a motívum %s ószövetségi versében áll.' % b,
            OSSZESITES])

    def test_szopar_mindket_tag_teljes(self):
        m = LG.lxx_egyezes_kapu(self.lap(), 'X-001', szopar=True)
        self.assertEqual(m['n'], 16)

    def test_szopar_hianyos_tag_bukik(self):
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(b='15'), 'X-001', szopar=True)

    def test_szopar_nelkul_osszeg_marad(self):
        # a nem szópáros motívumon a régi szabály: a szavankénti mondatok összege a versszám
        with self.assertRaises(ValueError):
            LG.lxx_egyezes_kapu(self.lap(), 'X-001')
        self.assertEqual(LG.lxx_egyezes_kapu(self.lap(a='10', b='6'), 'X-001')['szavankent'], 16)


class TobbLemma(unittest.TestCase):
    def setUp(self):
        self.idx = {('1Kir 18:24', 'H7121'): ('βοάω · ἐπικαλέω', '')}
        self.regi = (LG.vh_lxx_index, LG._heber_kulcsszo_strong)
        LG.vh_lxx_index = lambda _mid: self.idx
        LG._heber_kulcsszo_strong = lambda _v, _st: 'KULCS'

    def tearDown(self):
        LG.vh_lxx_index, LG._heber_kulcsszo_strong = self.regi

    def sor(self, gorog):
        return '| 1Kir 18:24 | 3Kir 18:24 | KULCS | %s | egyező | gépi |' % gorog

    def test_mindket_lemma_a_cellaban(self):
        self.assertEqual(LG.lxx_egyforras_ellenoriz('X-001', [self.sor('βοάω · ἐπικαλέω (boaó · epikaleó)')]), [])

    def test_hianyzo_lemma_elter(self):
        self.assertTrue(LG.lxx_egyforras_ellenoriz('X-001', [self.sor('ἐπικαλέω (epikaleó)')]))


class SzoparLanc(unittest.TestCase):
    """DT-F194h (a DT-F178g kiterjesztése szópárra): a szópáros motívum 9. Hatástörténet-lánca a formula igéjéből és a
    motívum saját ószövetségi verseiből áll, Peshat-mag nélkül; az egyes szavas lánc (HAMART-001) nem változik."""

    def test_szopar_felismeres(self):
        par = [{'gerinc_elem': 'H7121+H8034'}, {'gerinc_elem': 'G1941'}]
        self.assertTrue(LG.szopar_motivum(par))
        self.assertEqual(LG.szopar_ige(par), 'H7121')
        self.assertEqual(LG.par_nev(par, 'H7121'), 'H8034')
        # az egyes szavas lánc melletti szópár nem teszi szópárossá (HAMART-001: málé + chámász)
        self.assertFalse(LG.szopar_motivum(par + [{'gerinc_elem': 'H2555'}]))
        self.assertFalse(LG.szopar_motivum([{'gerinc_elem': 'H0779'}]))

    def test_istentiszt_lanc(self):
        sorai = [r for r in self.elofordulasok() if r['id'] == 'ISTENTISZT-001']
        szavak, mag = LG.lanc_szavak({'id': 'ISTENTISZT-001', 'negativ_kriterium': ''}, sorai)
        self.assertEqual(mag, LG.SZOPAR_MAG)
        self.assertEqual([s for s, _ in szavak], ['H7121'])
        versek = szavak[0][1]
        self.assertEqual(len(versek), 16)
        self.assertEqual(versek[0], '1Móz 4:26')
        self.assertTrue(all(not v.startswith(('ApCsel', 'Róm', '1Kor')) for v in versek))

    def test_hamart_lanc_valtozatlan(self):
        sorai = [r for r in self.elofordulasok() if r['id'] == 'HAMART-001']
        m = next(r for r in self.motivumok() if r['id'] == 'HAMART-001')
        _szavak, mag = LG.lanc_szavak(m, sorai)
        self.assertNotEqual(mag, LG.SZOPAR_MAG)
        self.assertFalse(LG.szopar_motivum(sorai))

    @staticmethod
    def elofordulasok():
        import general as G
        return G.tsv_beolvas(os.path.join(os.path.dirname(ESZKOZOK), 'adat', 'elofordulasok.tsv'))[1]

    @staticmethod
    def motivumok():
        import general as G
        return G.tsv_beolvas(os.path.join(os.path.dirname(ESZKOZOK), 'adat', 'motivumok.tsv'))[1]


class PontozatlanRokonAlak(unittest.TestCase):
    """Az orkesztrátor döntése (2026-11-12): a pontozatlan rokon nyelvi alak átírás nélkül áll, és az ATIRAS-kapu nem
    veti össze a szó kiejtésével (a vokalizációt az adat nem adja)."""

    def test_tabla_atiras_nelkul(self):
        r = {'strong': 'H7121', 'lemma': 'óarámi', 'alak': 'קרא', 'kiejtes': '', 'jelentes': 'hív', 'megjegyzes': '',
             'ellenorzes': 'x'}
        ki = LG._hatter_sorok([r])
        self.assertEqual(ki[0][1], ['קרא'])

    def test_kapu_nem_veti_ossze(self):
        import olvasoi_kapu as K
        self.assertTrue(K.PONTOZATLAN_HEBER('קרא'))
        self.assertFalse(K.PONTOZATLAN_HEBER('קָרָא'))
        jo = K.tagol('A szó קָרָא (kárá).\n\n##### Háttér: rokon nyelvek (BDB)\n\nAz óarámi alak קרא (kr), átírás nélkül.\n')
        # a rokon táblán kívül a pontozatlan alak is összevetendő (a független ellenőr 10. tétele)
        kivul = K.tagol('A szó קָרָא (kárá).\n\nA szótár szövegében קרא (kara).\n')
        self.assertTrue([x for x in K.ell_atiras(kivul) if 'ATIRAS' in str(x)])
        self.assertEqual([x for x in K.ell_atiras(jo) if 'ATIRAS' in str(x)], [])
        # a pontozott alak két kiejtése továbbra is BUKÁS
        rossz = K.tagol('A szó קָרָא (kárá).\n\nMásutt קָרָא (kara).\n')
        self.assertTrue([x for x in K.ell_atiras(rossz) if 'ATIRAS' in str(x)])




class Szabaly42Cimke(unittest.TestCase):
    """F194: a 42. szabály a Thayer-szakasz jóváhagyott címkéjét (szotar_szakasz_cimke.tsv) is elfogadja a csukott
    vázlatsorban; a címke nélküli szakasz fordításának eleje továbbra is kell."""

    def test_cimke_kepviseli_a_szakaszt(self):
        import ellenoriz as E
        adat = os.path.join(os.path.dirname(ESZKOZOK), 'adat')
        self.assertTrue(E._thayer_cimke_a_lapon(adat, 'G1941', '1. nevet adni valakinek, elnevezni: τινα',
                                                ' a szó 1 elnevezni a vázlatban '))
        self.assertFalse(E._thayer_cimke_a_lapon(adat, 'G1941', '1. nevet adni valakinek', ' más szöveg '))
        self.assertFalse(E._thayer_cimke_a_lapon(adat, 'G1941', 'nincs szakaszszám', ' elnevezni '))


if __name__ == '__main__':
    unittest.main()
