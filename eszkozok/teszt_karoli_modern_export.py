#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A karoli_modern_export.py és a karoli_modern_kapu.py tesztjei (F174).

Pozitív: a teljes adaton generált csomag 0 BUKÁS-t ad, és az export determinisztikus. Negatív: az elveszett és a
kitalált pár, a belső jel, a héber/görög írásjel, az export-kód a mappában, a megváltoztatott fájl, a hiányzó
attribúció és a kiadásba kerülő közlemény mind BUKÁS-t ad. Egységtesztek a kapcsolattípusra és a vetítésre.

Használat: python eszkozok/teszt_karoli_modern_export.py   (kb. egy perc: a teljes export kétszer fut)
"""
import copy
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_csomag as CS  # noqa: E402
import karoli_modern_export as E  # noqa: E402
import karoli_modern_kapu as G  # noqa: E402


def bukasok(fajlok, azon=None):
    t = G.mer(fajlok, ujra_is=False, git_is=False)
    return [x for x in t if x.suly == G.BUKAS and (azon is None or x.azon == azon)]


class Egyseg(unittest.TestCase):
    def test_kapcsolat(self):
        self.assertEqual(E.kapcsolat('H9003'), 'morfema')
        self.assertEqual(E.kapcsolat('H9049'), 'morfema')
        self.assertEqual(E.kapcsolat('H9050'), 'szo')
        self.assertEqual(E.kapcsolat('H7225'), 'szo')
        self.assertEqual(E.kapcsolat('G1161'), 'szo')
        self.assertEqual(E.kapcsolat('H9003+H9001'), 'morfema')
        self.assertEqual(E.kapcsolat('H1234+H9003'), 'szo')

    def _modern(self, sorszam, a1908, amod, kieso='', gazda=''):
        return {'igehely': '1Móz 1:1', 'sorszam': sorszam, 'alak_1908': a1908, 'alak_modern': amod, 'kieso': kieso,
                'kieso_gazda': gazda, 'szabaly': '', 'bizonytalan': ''}

    def test_vetites_kieso_megtartja_a_part(self):
        modern = [self._modern('1', 'a', '', 'osszevonva', '2'), self._modern('2', 'kik', 'akik'),
                  self._modern('3', 'és', 'és')]
        allapot = {('1Móz 1:1', '1'): {'szo': 'a', 'allapot': 'parositva'},
                   ('1Móz 1:1', '2'): {'szo': 'kik', 'allapot': 'parositva'},
                   ('1Móz 1:1', '3'): {'szo': 'és', 'allapot': 'betoldas'}}
        parok = {('1Móz 1:1', '1'): [{'hu_szo': 'a', 'er_sorszam': '4', 'strong': 'H0834', 'bizonyossag': 'magas'}],
                 ('1Móz 1:1', '2'): [{'hu_szo': 'kik', 'er_sorszam': '4', 'strong': 'H0834', 'bizonyossag': 'magas'},
                                     {'hu_szo': 'kik', 'er_sorszam': '2', 'strong': 'H9003', 'bizonyossag': 'magas'}]}
        konyvek = E.vetit(modern, parok, allapot)
        self.assertEqual([k for k, _ in konyvek], ['Gen'])
        sorok = konyvek[0][1]
        self.assertEqual(len(sorok), 4)                              # 1 + 2 pár + 1 betoldás
        self.assertEqual(sorok[0][:7], ['Gen.1.1', '1', 'a', '', 'igen', 'osszevonva', '2'])
        self.assertEqual(sorok[0][9], 'H0834')                       # a kieső szó párja megmarad
        self.assertEqual([s[10] for s in sorok[1:3]], ['2', '4'])    # eredeti sorszám szerint rendezve
        self.assertEqual(sorok[3][8:], ['betoldas', '', '', ''])            # a bizonyosság nem kerül be
        self.assertTrue(all(len(s) == len(E.FEJ) for s in sorok))

    def test_vetites_alakelteresnel_megall(self):
        modern = [self._modern('1', 'Kezdetben', 'Kezdetben')]
        allapot = {('1Móz 1:1', '1'): {'szo': 'Kezdetbe', 'allapot': 'parositva'}}
        with self.assertRaises(SystemExit):
            E.vetit(modern, {}, allapot)

    def test_vetites_arva_par_megall(self):
        modern = [self._modern('1', 'Kezdetben', 'Kezdetben')]
        allapot = {('1Móz 1:1', '1'): {'szo': 'Kezdetben', 'allapot': 'parositva'}}
        parok = {('1Móz 1:1', '1'): [{'hu_szo': 'Kezdetben', 'er_sorszam': '1', 'strong': 'H9003', 'bizonyossag': 'magas'}],
                 ('1Móz 1:1', '9'): [{'hu_szo': 'x', 'er_sorszam': '1', 'strong': 'H1', 'bizonyossag': 'magas'}]}
        with self.assertRaises(SystemExit):
            E.vetit(modern, parok, allapot)


class Csomag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fajlok, cls.N = E.export()

    def uj(self):
        return copy.deepcopy(self.fajlok)

    def test_pozitiv(self):
        self.assertEqual(bukasok(self.fajlok), [])

    def test_determinisztikus(self):
        masodik, _ = E.export()
        self.assertEqual(masodik, self.fajlok)

    def test_elveszett_par(self):
        f = self.uj()
        rel = 'data/konyvek/01_Gen.tsv'
        sorok = f[rel].split('\n')
        i = next(n for n, s in enumerate(sorok) if '\tjavaslat\t' in s)
        del sorok[i]
        f[rel] = '\n'.join(sorok)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_kitalalt_par(self):
        f = self.uj()
        rel = 'data/konyvek/01_Gen.tsv'
        sorok = f[rel].split('\n')
        i = next(n for n, s in enumerate(sorok) if '\tjavaslat\t' in s)
        m = sorok[i].split('\t')
        m[9] = 'H9999'
        sorok.insert(i, '\t'.join(m))
        f[rel] = '\n'.join(sorok)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_belso_jel(self):
        for szo in ('a DT305 szerint', 'l. naplok/X.md', 'scope=manual', 'az orkesztrátor', 'felhasználói döntés',
                    'a termék', 'PaRDeS', 'https://github.com/x'):
            f = self.uj()
            f['docs/hu/MODSZER.md'] += '\n' + szo + '\n'
            self.assertTrue(bukasok(f, 'NYILVANOS'), szo)

    def test_heber_gorog(self):
        f = self.uj()
        f['data/versek.tsv'] = f['data/versek.tsv'].replace('Kezdetben', 'Kezdetben בּ', 1)
        self.assertTrue(bukasok(f, 'HARMADIK'))
        f = self.uj()
        f['docs/hu/ISMERT_HIBAK.md'] += '\nδέ\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))

    def test_export_kod(self):
        f = self.uj()
        f['karoli_modern_export.py'] = 'print(1)\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))

    def test_attribucio(self):
        f = self.uj()
        f['docs/hu/ATTRIBUCIO.md'] = f['docs/hu/ATTRIBUCIO.md'].replace(E.STEP_ATTRIB, 'STEPBible')
        self.assertTrue(bukasok(f, 'LICENC'))
        f = self.uj()
        f['README.md'] += '\nCC BY-NC 4.0\n'
        self.assertTrue(bukasok(f, 'LICENC'))

    def test_valtozott_fajl(self):
        f = self.uj()
        f['docs/hu/OLVASSEL.md'] += ' '
        self.assertTrue(bukasok(f, 'OSSZEG'))

    def test_kozlemeny_kiadasban(self):
        f = self.uj()
        f['.gitattributes'] = '# semmi\n'
        self.assertTrue(bukasok(f, 'KOZLEMENY'))
        f = self.uj()
        del f['note/note_en.md']
        self.assertTrue(bukasok(f, 'KOZLEMENY'))

    def test_a_fa_alakja(self):
        gyokerek = {rel.split('/')[0] for rel in self.fajlok if '/' in rel}
        self.assertEqual(gyokerek, {'data', 'docs', 'note'})                     # paper/ csak kézzel kerül ide
        self.assertEqual(sorted(rel for rel in self.fajlok if '/' not in rel), sorted(CS.GYOKER_FAJLOK))
        self.assertEqual(sorted(rel for rel in self.fajlok if rel.startswith('docs/')),
                         ['docs/en/ATTRIBUTION.md', 'docs/en/CODEBOOK.md', 'docs/en/KNOWN_ISSUES.md',
                          'docs/en/METHODS.md', 'docs/hu/ATTRIBUCIO.md', 'docs/hu/ISMERT_HIBAK.md',
                          'docs/hu/KODKONYV.md', 'docs/hu/MODSZER.md', 'docs/hu/OLVASSEL.md'])
        self.assertEqual(sorted(rel for rel in self.fajlok if rel.startswith('note/')),
                         ['note/note_en.md', 'note/note_hu.md'])
        self.assertTrue(all(E.ENGEDETT.match(rel) for rel in self.fajlok))

    def test_nem_engedett_utak_bukast_adnak(self):
        for rel in ('KODKONYV.md', 'MODSZER.md', 'versek.tsv', 'konyvek/01_Gen.tsv', 'kozlemeny/kozlemeny_hu.md',
                    'docs/de/OLVASSEL.md', 'docs/hu/EXTRA.md', 'data/extra.tsv', 'data/konyvek/x.tsv',
                    'data/parok/01_Gen.tsv', 'paper/masik.md', 'note/note_de.md', 'eszkozok/x.py', 'extra/x.md'):
            f = self.uj()
            f[rel] = 'x\n'
            self.assertTrue(bukasok(f, 'HARMADIK'), rel)
        for rel in ('paper/kezirat_hu.md', 'paper/kezirat_en.md'):
            self.assertTrue(E.ENGEDETT.match(rel), rel)

    def test_concept_doi(self):
        for rel, sz in self.fajlok.items():
            for regi in ('24141884', '24141950', '24141612'):                                # a verzió-DOI nem áll a fájlokban
                self.assertNotIn(regi, sz, rel)
        self.assertEqual(E.DOI, '10.5281/zenodo.24141949')
        self.assertEqual(E.DOI_KAROLI_STRONG, '10.5281/zenodo.24141883')
        self.assertIn('doi: "10.5281/zenodo.24141949"', self.fajlok['CITATION.cff'])
        self.assertIn('kozzeteteli_hely: https://doi.org/10.5281/zenodo.24141949', self.fajlok['KIADAS.txt'])
        self.assertEqual(E.DOI_MAG, '10.5281/zenodo.24141611')                  # a motívum-adatmag concept DOI-ja
        self.assertIn('10.5281/zenodo.24141611', self.fajlok['README.md'])
        self.assertIn('10.5281/zenodo.24141883', self.fajlok['README.md'])      # a szóillesztési csomag concept DOI-ja

    def test_szamok(self):
        self.assertNotIn('bizonyossag', E.FEJ)                                 # a modell-egyezés nem minősítés
        self.assertEqual(self.N['token'] - self.N['strongos_token'], self.N['betoldas'] + self.N['fuggoben'])


if __name__ == '__main__':
    unittest.main(verbosity=1)
