#!/usr/bin/env python
"""A `szakasz_bemenet.py` tesztjei (F128 M1; DT-F128a–d).

    python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py
"""
import os
import sys
import unicodedata
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import nezet_general  # noqa: E402
import szakasz_bemenet as SB  # noqa: E402


def nfd(t):
    return unicodedata.normalize('NFD', t)


class Korpusz(unittest.TestCase):
    """Az egész szakasztáblán: a token nélküli kimenet = a nezet_general.py (--pe-mem nélküli) nézete; 0 pe/mem csere."""

    @classmethod
    def setUpClass(cls):
        cls.hibak, cls.stat, cls.nagy = SB.ellenoriz()

    def test_nincs_hiba(self):
        self.assertEqual(self.hibak, [])

    def test_lefedes(self):
        self.assertEqual(self.stat['strong'], 8090)
        self.assertEqual(self.stat['szakasz'], 36621)

    def test_tobbcsoportos_a_20000_folottiek(self):
        # F128 M0 3.: 11 szócikk 20 000 karakter fölött
        self.assertEqual(sorted(s for s, _, _ in self.nagy),
                         ['H0834', 'H1961', 'H1980', 'H3117', 'H3588', 'H4480', 'H5414', 'H5920', 'H6440', 'H7725', 'H9005'])


class Javitasok(unittest.TestCase):
    def setUp(self):
        self.jav = nezet_general.olvas(nezet_general.JAV)

    def test_hivatkozas_alkalmazva(self):
        d = next(d for d in self.jav if d['hiba'] == 'hivatkozas' and d['allapot'] == 'javitva')
        x = next(x for x in SB.szakaszok(d['strong']) if str(x['sorszam']) == d['sorszam'])
        self.assertIn(d['javitott_alak'], x['szoveg'])

    def test_pe_mem_nem_alkalmazva(self):
        # DT269 (1): a pe/mem csere a bemenetben nincs — a `javitva` sor mem-es alakja marad
        n = 0
        for d in self.jav:
            if d['hiba'] != 'pe_mem' or d['allapot'] != 'javitva':
                continue
            x = next(x for x in SB.szakaszok(d['strong']) if str(x['sorszam']) == d['sorszam'])
            szavak = [nfd(w) for w in x['szoveg'].split()]
            self.assertTrue(any(nfd(d['forras_alak']) in w for w in szavak), (d['strong'], d['sorszam']))
            n += 1
            if n >= 200:
                break
        self.assertEqual(n, 200)

    def test_tablan_kivuli(self):
        # DT-F128d (2): a 9 táblán kívüli Strong a régi `teljes` úton
        for st in ('H0747', 'H1753', 'H3367', 'H3848', 'H4123', 'H4725', 'H6433', 'H7560', 'H8065'):
            self.assertIsNone(SB.szakaszok(st), st)

    def test_hash(self):
        for x in SB.szakaszok('H0001'):
            self.assertEqual(x['hash'], SB.sha1(x['szoveg']))
            self.assertNotIn('⟪', x['szoveg'])


class Tokenek(unittest.TestCase):
    def test_tokenes_alak(self):
        szak = SB.szakaszok('H0001')
        t = SB.tokenes(szak)
        self.assertEqual([int(n) for n in SB.TOKEN.findall(t)], [x['sorszam'] for x in szak])
        self.assertTrue(t.startswith('⟪1⟫ H1. ab'))
        self.assertEqual(SB.TOKEN.sub('', t).replace('\n', ' ').split(), SB.nezet(szak).split())

    def test_jelentes_szam(self):
        self.assertEqual(SB.jelentes_szam(12), 'sz12')
        self.assertEqual(SB.sorszam_jelentesbol('sz12'), 12)
        for x in ('teljes', '2.c', 'sz', 'sz1a', ''):
            self.assertIsNone(SB.sorszam_jelentesbol(x))


def _sz(n, utvonal, hossz):
    return {'sorszam': n, 'jel': '', 'utvonal': utvonal, 'szoveg': 'x' * hossz, 'hash': ''}


class Csoportok(unittest.TestCase):
    def test_rovid_egy_csoport(self):
        szak = SB.szakaszok('H0001')
        self.assertEqual(SB.csoportok(szak), [szak])

    def test_nagy_csoportok(self):
        szak = SB.szakaszok('H1980')
        cs = SB.csoportok(szak)
        self.assertGreater(len(cs), 1)
        self.assertEqual([x for c in cs for x in c], szak)
        for c in cs:
            self.assertLessEqual(sum(SB._hossz(x) for x in c), SB.CSOPORT_CEL)

    def test_torzsvaltasnal_vag(self):
        # 3 × 4 000 karakter Qal alatt, majd Niph'al: a 3. Qal-szakasz után nem fér el a 4.; a vágás a törzsváltásnál
        szak = [_sz(1, 'cim', 10), _sz(2, 'Qal/1/-', 4000), _sz(3, 'Qal/2/-', 4000), _sz(4, "Niph'al/-/-", 1500),
                _sz(5, "Niph'al/1/-", 4000), _sz(6, "Niph'al/2/-", 4000), _sz(7, 'Hiph\'il/-/-', 4000)]
        cs = SB.csoportok(szak, hatar=1000, cel=10000)
        self.assertEqual([[x['sorszam'] for x in c] for c in cs], [[1, 2, 3], [4, 5, 6], [7]])

    def test_egyedul_tul_hosszu_szakasz(self):
        szak = [_sz(1, 'cim', 10), _sz(2, '-/1/-', 12000), _sz(3, '-/2/-', 100)]
        cs = SB.csoportok(szak, hatar=1000, cel=10000)
        self.assertEqual([[x['sorszam'] for x in c] for c in cs], [[1], [2], [3]])


def _f(jsz, szoveg, allapot='sonnet'):
    return {'szotar': 'BDB', 'strong': 'H0001', 'entry_id': 'H1', 'jelentes_szam': jsz, 'mezo': 'forditas_hu',
            'forditas_hu': szoveg, 'allapot': allapot}


class Osszefuzo(unittest.TestCase):
    def test_szakaszok_sorrendben(self):
        sorok = [_f('sz10', 'c'), _f('sz2', 'b'), _f('sz1', 'a')]
        self.assertEqual(SB.strong_magyar(sorok), ('a b c', 'szakasz'))

    def test_szakasz_elonyben_a_teljes_elott(self):
        # DT-F128e: a 98 Strong régi `teljes` sora `elavult`, mellette a szakaszsorok
        sorok = [_f('teljes', 'régi', 'elavult'), _f('sz1', 'a'), _f('sz2', 'b')]
        self.assertEqual(SB.strong_magyar(sorok), ('a b', 'szakasz'))
        sorok = [_f('teljes', 'régi'), _f('sz1', 'a')]
        self.assertEqual(SB.strong_magyar(sorok), ('a', 'szakasz'))

    def test_elavult_szakasz_kimarad(self):
        sorok = [_f('sz1', 'a'), _f('sz2', 'x', 'elavult'), _f('sz3', 'c')]
        self.assertEqual(SB.strong_magyar(sorok), ('a c', 'szakasz'))

    def test_teljes_tartalek(self):
        self.assertEqual(SB.strong_magyar([_f('teljes', 'egész')]), ('egész', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'régi', 'elavult'), _f('teljes', 'új')]), ('új', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'régi', 'elavult')]), ('régi', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('2.c', 'rész', 'kezi')]), (None, None))
        self.assertEqual(SB.strong_magyar([]), (None, None))


if __name__ == '__main__':
    unittest.main(verbosity=2)
