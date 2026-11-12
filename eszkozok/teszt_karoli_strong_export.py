#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A karoli_strong_export.py és a karoli_strong_kapu.py tesztjei (F175).

Pozitív: a teljes adaton generált csomag 0 BUKÁS-t ad, és az export determinisztikus. Negatív: az elveszett, a kitalált
és a megváltoztatott pár, az elveszett szó, a belső jel, a héber/görög írásjel, a zárt forrás neve, az export-kód a
mappában, a megváltoztatott fájl, a hiányzó attribúció, a repó-gyökér kimondásának hiánya és a kiadásba kerülő
közlemény mind BUKÁS-t ad. Egységtesztek a kapcsolattípusra és az átalakításra.

Használat: python eszkozok/teszt_karoli_strong_export.py   (kb. egy perc: a teljes export kétszer fut)
"""
import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_export as E  # noqa: E402
import karoli_strong_kapu as G  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def bukasok(fajlok, azon=None):
    t = G.mer(fajlok, ujra_is=False, git_is=False)
    return [x for x in t if x.suly == G.BUKAS and (azon is None or x.azon == azon)]


class Egyseg(unittest.TestCase):
    def test_kapcsolat(self):
        self.assertEqual(E.kapcsolat('H9003'), 'morfema')
        self.assertEqual(E.kapcsolat('H9049'), 'morfema')
        self.assertEqual(E.kapcsolat('H9050'), 'szo')
        self.assertEqual(E.kapcsolat('G1161'), 'szo')
        self.assertEqual(E.kapcsolat('H9003+H9001'), 'morfema')
        self.assertEqual(E.kapcsolat('H1234+H9003'), 'szo')

    def _alap(self):
        versek = [{'Igehely': '1Móz 1:1', 'Károli-szöveg (teljes vers)': 'Kezdetben teremté Isten.'}]
        szavak = [
            {'vers': '1Móz 1:1', 'oldal': 'er', 'sorszam': '2', 'szo': 'X', 'allapot': 'parositva',
             'partner_sorszam': '1', 'strong': 'H7225', 'bizonyossag': 'magas'},
            {'vers': '1Móz 1:1', 'oldal': 'hu', 'sorszam': '1', 'szo': 'Kezdetben', 'allapot': 'parositva',
             'partner_sorszam': '1,2', 'strong': 'H9003+H7225', 'bizonyossag': 'magas'},
            {'vers': '1Móz 1:1', 'oldal': 'er', 'sorszam': '1', 'szo': 'Y', 'allapot': 'parositva',
             'partner_sorszam': '1', 'strong': 'H9003', 'bizonyossag': 'magas'},
            {'vers': '1Móz 1:1', 'oldal': 'hu', 'sorszam': '2', 'szo': 'teremté', 'allapot': 'fuggoben',
             'partner_sorszam': '', 'strong': '', 'bizonyossag': 'kezi'},
        ]
        parok = [
            {'vers': '1Móz 1:1', 'hu_sorszam': '1', 'hu_szo': 'Kezdetben', 'er_sorszam': '2', 'strong': 'H7225',
             'bizonyossag': 'magas'},
            {'vers': '1Móz 1:1', 'hu_sorszam': '1', 'hu_szo': 'Kezdetben', 'er_sorszam': '1', 'strong': 'H9003',
             'bizonyossag': 'magas'},
        ]
        return versek, parok, szavak

    def test_atalakitas_sorrend_es_alak(self):
        versek, parok, szavak = self._alap()
        konyvek, vsorok = E.atalakit(versek, parok, szavak, [])
        self.assertEqual([k for k, _, _ in konyvek], ['Gen'])
        _, ps, ss = konyvek[0]
        self.assertEqual([p[3] for p in ps], ['1', '2'])                       # eredeti sorszám szerint
        self.assertEqual(ps[0][5], 'morfema')
        self.assertEqual([(s[1], s[2]) for s in ss], [('hu', '1'), ('hu', '2'), ('er', '1'), ('er', '2')])
        self.assertEqual(ss[2][3], '')                                          # az eredeti alak nem kerül be
        self.assertEqual(ss[1][7], '')                                          # kezi -> üres bizonyosság
        self.assertEqual(vsorok, [['Gen.1.1', 'Kezdetben teremté Isten.']])

    def test_alakelteresnel_megall(self):
        versek, parok, szavak = self._alap()
        parok[0]['hu_szo'] = 'Kezdetbe'
        with self.assertRaises(SystemExit):
            E.atalakit(versek, parok, szavak, [])

    def test_ismeretlen_versnel_megall(self):
        versek, parok, szavak = self._alap()
        szavak[0]['vers'] = '1Móz 9:99'
        with self.assertRaises(SystemExit):
            E.atalakit(versek, parok, szavak, [])

    def test_nem_tr_jeloles(self):
        versek, parok, szavak = self._alap()
        konyvek, _ = E.atalakit(versek, parok, szavak, [{'vers': '1Móz 1:1', 'er_sorszam': '2'}])
        self.assertEqual([p[8] for p in konyvek[0][1]], ['', 'igen'])


class Csomag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fajlok, cls.N = E.export()

    def uj(self):
        return copy.deepcopy(self.fajlok)

    def _sor_csere(self, f, rel, fv):
        sorok = f[rel].split('\n')
        i = next(n for n, s in enumerate(sorok) if s and not s.startswith('#') and not s.startswith('osis\t'))
        fv(sorok, i)
        f[rel] = '\n'.join(sorok)

    def test_pozitiv(self):
        self.assertEqual(bukasok(self.fajlok), [])

    def test_determinisztikus(self):
        masodik, _ = E.export()
        self.assertEqual(masodik, self.fajlok)

    def test_elveszett_par(self):
        f = self.uj()
        self._sor_csere(f, 'parok/01_Gen.tsv', lambda s, i: s.pop(i))
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_kitalalt_par(self):
        f = self.uj()

        def fv(s, i):
            m = s[i].split('\t')
            m[4] = 'H9999'
            s.insert(i, '\t'.join(m))
        self._sor_csere(f, 'parok/01_Gen.tsv', fv)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_elveszett_szo(self):
        f = self.uj()
        self._sor_csere(f, 'szavak/66_Rev.tsv', lambda s, i: s.pop(i))
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_megvaltozott_allapot(self):
        f = self.uj()

        def fv(s, i):
            m = s[i].split('\t')
            m[4] = 'betoldas' if m[4] != 'betoldas' else 'parositva'
            s[i] = '\t'.join(m)
        self._sor_csere(f, 'szavak/01_Gen.tsv', fv)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_belso_jel(self):
        for szo in ('a DT623 szerint', 'l. naplok/X.md', 'scope=manual', 'az orkesztrátor', 'felhasználói döntés',
                    'a termék', 'PaRDeS', 'https://github.com/x', 'régi arany', '{p_osszes}'):
            f = self.uj()
            f['MODSZER.md'] += '\n' + szo + '\n'
            self.assertTrue(bukasok(f, 'NYILVANOS'), szo)

    def test_repo_gyoker(self):
        f = self.uj()
        f['README.md'] = f['README.md'].replace('root of a self-contained public repository', 'folder')
        self.assertTrue(bukasok(f, 'NYILVANOS'))

    def test_heber_gorog_es_zart_forras(self):
        f = self.uj()
        f['versek.tsv'] = f['versek.tsv'].replace('Kezdetben', 'Kezdetben בּ', 1)
        self.assertTrue(bukasok(f, 'HARMADIK'))
        f = self.uj()
        f['ISMERT_HIBAK.md'] += '\nδέ\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))
        f = self.uj()
        f['METHODS.md'] += '\nBible-Discovery\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))

    def test_export_kod(self):
        f = self.uj()
        f['karoli_strong_export.py'] = 'print(1)\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))

    def test_attribucio(self):
        f = self.uj()
        f['ATTRIBUCIO.md'] = f['ATTRIBUCIO.md'].replace(E.STEP_ATTRIB, 'STEPBible')
        self.assertTrue(bukasok(f, 'LICENC'))
        f = self.uj()
        f['README.md'] += '\nCC BY-NC 4.0\n'
        self.assertTrue(bukasok(f, 'LICENC'))

    def test_valtozott_fajl(self):
        f = self.uj()
        f['OLVASSEL.md'] += ' '
        self.assertTrue(bukasok(f, 'OSSZEG'))

    def test_kozlemeny_kiadasban(self):
        f = self.uj()
        f['.gitattributes'] = '# semmi\n'
        self.assertTrue(bukasok(f, 'KOZLEMENY'))
        f = self.uj()
        del f['kozlemeny/kozlemeny_en.md']
        self.assertTrue(bukasok(f, 'KOZLEMENY'))

    def test_szamok(self):
        N = self.N
        self.assertEqual(N['par'], N['magas'] + N['alacsony'])
        self.assertEqual(N['par'], N['heber_par'] + N['gorog_par'])
        self.assertEqual(N['hu_token'], N['hu_parositva'] + N['hu_betoldas'] + N['hu_fuggoben'])
        self.assertEqual(N['er_token'], N['er_parositva'] + N['er_forditatlan'] + N['er_fuggoben'])
        self.assertEqual(N['par'], N['keret'])


if __name__ == '__main__':
    unittest.main(verbosity=1)
