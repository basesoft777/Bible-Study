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
import karoli_csomag as CS  # noqa: E402
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
    def test_szam_nevelo(self):
        az = ('1', '5', '1 600', '598 715', '50', '500', '5 078', '1 000 000', '1908', '1234567')
        a = ('2', '10', '12', '100', '160', '200', '34', '31 158', '466 785', '95', '15', '150', '12345', '12 345')
        for s in az:
            self.assertEqual(E.szam_nevelo(s), 'az', s)
        for s in a:
            self.assertEqual(E.szam_nevelo(s), 'a', s)
        self.assertEqual(E.nevelo_javit('A 598 715 párt; a 1 600 közül az 34, a 2. és a 1. kiadás'),
                         'Az 598 715 párt; az 1 600 közül a 34, a 2. és az 1. kiadás')
        self.assertEqual(E.nevelo_javit('a 3:18 és a 2Kir'), 'a 3:18 és a 2Kir')
        self.assertEqual(E.szo_nevelo('Logosz-lexikon'), 'a')
        self.assertEqual(E.szo_nevelo('Ószövetség'), 'az')

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
        self.assertEqual(len(ss[1]), len(E.SZO_FEJ))                            # a bizonyosság nem kerül be
        self.assertEqual(len(ps[0]), len(E.PAR_FEJ))
        self.assertNotIn('bizonyossag', E.PAR_FEJ + E.SZO_FEJ)
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
        self.assertEqual([p[7] for p in konyvek[0][1]], ['', 'igen'])


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
        self._sor_csere(f, 'data/parok/01_Gen.tsv', lambda s, i: s.pop(i))
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_kitalalt_par(self):
        f = self.uj()

        def fv(s, i):
            m = s[i].split('\t')
            m[4] = 'H9999'
            s.insert(i, '\t'.join(m))
        self._sor_csere(f, 'data/parok/01_Gen.tsv', fv)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_elveszett_szo(self):
        f = self.uj()
        self._sor_csere(f, 'data/szavak/66_Rev.tsv', lambda s, i: s.pop(i))
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_megvaltozott_allapot(self):
        f = self.uj()

        def fv(s, i):
            m = s[i].split('\t')
            m[4] = 'betoldas' if m[4] != 'betoldas' else 'parositva'
            s[i] = '\t'.join(m)
        self._sor_csere(f, 'data/szavak/01_Gen.tsv', fv)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_belso_jel(self):
        for szo in ('a DT623 szerint', 'l. naplok/X.md', 'scope=manual', 'az orkesztrátor', 'felhasználói döntés',
                    'a termék', 'PaRDeS', 'https://github.com/x', 'régi arany', '{p_osszes}'):
            f = self.uj()
            f['docs/hu/MODSZER.md'] += '\n' + szo + '\n'
            self.assertTrue(bukasok(f, 'NYILVANOS'), szo)

    def test_modell_egyezes(self):
        # a két modell egyezése nem minősítés, a költségkeret-történet nem a közölt állapot leírása
        for szo in ('`magas` bizonyosságú', 'alacsony bizonyosság', 'a költségkeret miatt', 'Gemini Flash',
                    'két független modell párosította', 'For reasons of cost', 'two independent models aligned',
                    'the confidence label', 'High confidence'):
            f = self.uj()
            f['docs/en/METHODS.md' if szo[0].isupper() or szo.startswith(('two', 'the')) else 'docs/hu/MODSZER.md'] += '\n' + szo + '\n'
            self.assertTrue(bukasok(f, 'NYILVANOS'), szo)
        # a „bizonyosság” a mért pontosságot jelenti (DT-F175e): így megengedett
        f = self.uj()
        f['docs/hu/MODSZER.md'] += '\nA bizonyosság a mért pontosság: 95% (Mózes öt könyve).\n'
        self.assertEqual(bukasok(f, 'NYILVANOS'), [])

    def test_bizonyossag_oszlop(self):
        f = self.uj()
        f['data/parok/01_Gen.tsv'] = f['data/parok/01_Gen.tsv'].replace('\tallapot\t', '\tbizonyossag\tallapot\t', 1)
        self.assertTrue(bukasok(f, 'TELJESSEG'))

    def test_kiadas_mondat(self):
        f = self.uj()
        f['README.md'] = f['README.md'].replace('Every file of the package is part of the release.', '')
        self.assertTrue(bukasok(f, 'NYILVANOS'))

    def test_nevelo_hiba(self):
        for rossz in ('A 598 715 pár', 'a 1 600 minta', 'az 34 eltérés', 'a(z) Logosz-lexikon', 'a 1. kiadás'):
            f = self.uj()
            f['docs/hu/MODSZER.md'] += '\n' + rossz + '\n'
            self.assertTrue(bukasok(f, 'NEVELO'), rossz)

    def test_heber_gorog_es_zart_forras(self):
        f = self.uj()
        f['data/versek.tsv'] = f['data/versek.tsv'].replace('Kezdetben', 'Kezdetben בּ', 1)
        self.assertTrue(bukasok(f, 'HARMADIK'))
        f = self.uj()
        f['docs/hu/ISMERT_HIBAK.md'] += '\nδέ\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))
        f = self.uj()
        f['docs/en/METHODS.md'] += '\nBible-Discovery\n'
        self.assertTrue(bukasok(f, 'HARMADIK'))

    def test_export_kod(self):
        f = self.uj()
        f['karoli_strong_export.py'] = 'print(1)\n'
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
        # a csomag pontosan a nyilvános repó: egyetlen export-ignore sem lehet
        f = self.uj()
        f['.gitattributes'] += 'note/ export-ignore\n'
        self.assertTrue(bukasok(f, 'KOZLEMENY'))
        f = self.uj()
        f['.gitattributes'] += 'docs/ export-ignore\n'
        self.assertTrue(bukasok(f, 'KOZLEMENY'))
        self.assertNotIn('export-ignore', self.fajlok['.gitattributes'])

    def test_note_a_csomagon_kivul(self):
        self.assertEqual(G.note(self.N, lemez=False)[0].suly, G.OK)
        self.assertFalse(any(rel.startswith('note/') for rel in self.fajlok))
        n = E.note(self.N)
        self.assertEqual(sorted(n), ['kozlemeny/note/karoli_strong/note_en.md', 'kozlemeny/note/karoli_strong/note_hu.md'])
        self.assertEqual(sorted(n), sorted(CS.note_utak('karoli_strong')))
        self.assertTrue(all(sz.startswith('<!-- GENERÁLT:') for _, sz in n.values()))
        self.assertTrue(all(not torzs.startswith('<!--') for torzs, _ in n.values()))

    def test_kezirat_a_csomagon_kivul(self):
        self.assertEqual(G.kezirat(self.N, lemez=False)[0].suly, G.OK)
        self.assertFalse(any('kezirat' in rel for rel in self.fajlok))
        k = E.kezirat(self.N)
        self.assertEqual(sorted(k), ['kozlemeny/data_paper/karoli_strong_kezirat_en.md',
                                     'kozlemeny/data_paper/karoli_strong_kezirat_hu.md'])
        self.assertTrue(all(sz.startswith('<!-- GENERÁLT:') for _, sz in k.values()))

    def test_masodik_modell_csak_a_kezirat_mi_nyilatkozataban(self):
        # DT-F175m: a második párosító modellről egy semleges mondat csak a JOHD-kézirat MI-nyilatkozatában áll;
        # a nyílt csomag, a közlemény és a kézirat többi része nem említi, és a MODELL_EGYEZES-tiltás érvényes marad
        jel = {'en': 'another language model was also run as a cross-check',
               'hu': 'egy másik nyelvi modell is futott keresztellenőrzésként'}
        for rel, (torzs, _) in E.kezirat(self.N).items():
            d = 'hu' if rel.endswith('_hu.md') else 'en'
            torzs = torzs.replace('\n', ' ')         # a sortörés helye a sablonban szabad
            nyil = torzs.split('## AI Declaration' if d == 'en' else '## Nyilatkozat a mesterséges intelligencia')
            self.assertEqual(len(nyil), 2, rel)
            self.assertNotIn(jel[d], nyil[0], rel)
            self.assertEqual(nyil[1].count(jel[d]), 1, rel)
        for rel, (torzs, _) in E.note(self.N).items():
            self.assertNotIn('cross-check', torzs)
            self.assertNotIn('keresztellenőrzés', torzs)
        self.assertFalse(any('cross-check' in sz or 'keresztellenőrzés' in sz for sz in self.fajlok.values()))
        for tilos in ('a Gemini model', 'two language models agreed', 'két nyelvi modell', 'high confidence'):
            self.assertTrue(any(rx.search(tilos) for rx, _ in G.TILTOTT), tilos)

    def test_szamok(self):
        N = self.N
        self.assertEqual(N['reteg_db'], 7)                                      # a két Mózes-réteg egy rétegben
        self.assertEqual(N['rn_OSZ_mozes'], 400)
        self.assertEqual(N['par'], N['heber_par'] + N['gorog_par'])
        self.assertEqual(N['hu_token'], N['hu_parositva'] + N['hu_betoldas'] + N['hu_fuggoben'])
        self.assertEqual(N['er_token'], N['er_parositva'] + N['er_forditatlan'] + N['er_fuggoben'])
        self.assertEqual(N['par'], N['keret'])


class Szerkezet(unittest.TestCase):
    """A csomagmappa szerkezete (`karoli_csomag.py`, F175.N): csak az engedett fájl és almappa állhat benne; az
    exportáló csak a generált almappákat írja, a kézi forrású `paper/`-hez nem nyúl; a concept DOI áll a fájlokban."""

    @classmethod
    def setUpClass(cls):
        cls.fajlok, cls.N = E.export()

    def uj(self):
        return copy.deepcopy(self.fajlok)

    def test_a_fa_alakja(self):
        gyokerek = {rel.split('/')[0] for rel in self.fajlok if '/' in rel}
        self.assertEqual(gyokerek, {'data', 'docs'})                             # paper/ csak kézzel kerül ide
        self.assertEqual(sorted(rel for rel in self.fajlok if '/' not in rel),
                         sorted(CS.GYOKER_FAJLOK))
        self.assertEqual(sorted(rel for rel in self.fajlok if rel.startswith('docs/')),
                         ['docs/en/ATTRIBUTION.md', 'docs/en/CODEBOOK.md', 'docs/en/KNOWN_ISSUES.md',
                          'docs/en/METHODS.md', 'docs/hu/ATTRIBUCIO.md', 'docs/hu/ISMERT_HIBAK.md',
                          'docs/hu/KODKONYV.md', 'docs/hu/MODSZER.md', 'docs/hu/OLVASSEL.md'])
        self.assertTrue(all(E.ENGEDETT.match(rel) for rel in self.fajlok))

    def test_nem_engedett_utak_bukast_adnak(self):
        for rel in ('KODKONYV.md', 'MODSZER.md', 'versek.tsv', 'parok/01_Gen.tsv', 'szavak/01_Gen.tsv',
                    'kozlemeny/kozlemeny_hu.md', 'docs/de/OLVASSEL.md', 'docs/hu/EXTRA.md', 'docs/hu/CODEBOOK.md',
                    'data/extra.tsv', 'data/parok/x.tsv', 'data/szavak/01_Gen.csv', 'paper/masik.md',
                    'paper/kezirat_de.md', 'note/note_de.md', 'note/note_hu.md', 'note/note_en.md', 'eszkozok/x.py', 'extra/x.md', 'README_hu.md'):
            f = self.uj()
            f[rel] = 'x\n'
            self.assertTrue(bukasok(f, 'HARMADIK'), rel)

    def test_engedett_paper(self):
        for rel in ('paper/kezirat_hu.md', 'paper/kezirat_en.md'):
            self.assertTrue(E.ENGEDETT.match(rel), rel)

    def test_egyutt_szakasz(self):
        # a két adatkészlet együtt: a másik adatkészlet concept DOI-ja, és a példasorok az adat sorai
        for rel, cim in (('README.md', '## Using the two datasets together'),
                         (CS.OLVASSEL, '## A két adatkészlet együtt')):
            sz = self.fajlok[rel]
            self.assertIn(cim, sz)
            self.assertIn('https://doi.org/10.5281/zenodo.24141949', sz.split(cim)[1].split('\n## ')[0])
            self.assertIn('data/szavak/NN_Konyv.tsv', sz.split(cim)[1])
        readme = self.fajlok['README.md']
        par = [s.split('\t') for s in self.fajlok['data/parok/01_Gen.tsv'].split('\n') if s.startswith('Gen.1.1\t')]
        er = [s.split('\t') for s in self.fajlok['data/szavak/01_Gen.tsv'].split('\n') if s.startswith('Gen.1.1\ter\t')]
        pelda_par = [s for s in par if int(s[1]) <= 3]
        pelda_er = [s for s in er if int(s[2]) <= 5]
        self.assertEqual(len(pelda_par), 4)
        for s in pelda_par:
            self.assertIn('| %s | %s | %s | %s | %s |' % (s[1], s[2], s[3], s[4], s[5]), readme)
        for s in pelda_er:
            self.assertIn('| %s | %s | %s | %s |' % (s[2], s[4], s[5], s[6]), readme)
        self.assertEqual(readme.count('| forditatlan |'), len([s for s in pelda_er if s[4] == 'forditatlan']))

    def test_concept_doi(self):
        for rel, sz in self.fajlok.items():
            for regi in ('24141884', '24141950', '24141612'):                                # a verzió-DOI nem áll a fájlokban
                self.assertNotIn(regi, sz, rel)
        self.assertEqual(E.DOI, '10.5281/zenodo.24141883')
        self.assertEqual(E.DOI_MODERN, '10.5281/zenodo.24141949')
        self.assertIn('doi: "10.5281/zenodo.24141883"', self.fajlok['CITATION.cff'])
        self.assertIn('kozzeteteli_hely: https://doi.org/10.5281/zenodo.24141883', self.fajlok['KIADAS.txt'])
        self.assertEqual(E.DOI_MAG, '10.5281/zenodo.24141611')                  # a motívum-adatmag concept DOI-ja
        self.assertIn('10.5281/zenodo.24141611', self.fajlok['README.md'])
        self.assertIn('10.5281/zenodo.24141949', self.fajlok['README.md'])      # a modernizált csomag concept DOI-ja

    def test_attribucio_ket_dokumentum(self):
        hu, en = self.fajlok[CS.ATTRIBUCIO], self.fajlok[CS.ATTRIBUTION]
        self.assertTrue(hu.startswith('# Forrásmegjelölés és licencek\n'))
        self.assertTrue(en.startswith('# Attribution and licences\n'))
        self.assertNotIn('In English', hu)
        self.assertNotIn('Magyarul', en)
        self.assertIn(E.STEP_ATTRIB, hu)
        self.assertIn(E.STEP_ATTRIB, en)

    def test_kodkonyv_ket_dokumentum(self):
        self.assertTrue(self.fajlok[CS.KODKONYV_HU].startswith('# Kódkönyv\n'))
        self.assertTrue(self.fajlok[CS.KODKONYV_EN].startswith('# Codebook\n'))
        self.assertIn('| oszlop | érték | leírás |', self.fajlok[CS.KODKONYV_HU])
        self.assertIn('| column | value | description |', self.fajlok[CS.KODKONYV_EN])
        self.assertIn('`data/parok/NN_Konyv.tsv`', self.fajlok[CS.KODKONYV_EN])

    def test_hivatkozasok_letezo_fajlra_mutatnak(self):
        # minden backtickes `data/…`, `docs/…` hivatkozás egy csomagbeli fájlra vagy mappára (NN_ mintával) mutat
        import re
        rx = re.compile(r'`((?:data|docs)/[^`\s]*)`')
        db = 0
        for rel in ('README.md', CS.OLVASSEL, CS.MODSZER, CS.METHODS, CS.ISMERT_HIBAK, CS.KNOWN_ISSUES):
            for m in rx.finditer(self.fajlok[rel]):
                ut = re.sub(r'NN_(?:Konyv|Book)\.tsv$', '', m.group(1))
                if ut.startswith('data/konyvek/'):   # a modernizált adatkészlet táblája (a „két adatkészlet együtt” szakasz)
                    continue
                db += 1
                self.assertTrue(any(f == ut or (ut.endswith('/') and f.startswith(ut)) for f in self.fajlok),
                                '%s: %s' % (rel, m.group(1)))
        self.assertGreater(db, 20)

    def test_kiir_a_kezi_forrashoz_nem_nyul(self):
        import shutil
        import tempfile
        tmp = tempfile.mkdtemp(prefix='karoli_csomag_teszt_')
        try:
            CS.kiir({'README.md': 'a\n', 'data/x.tsv': 'x\n'}, tmp)
            os.makedirs(os.path.join(tmp, 'paper'))
            with open(os.path.join(tmp, 'paper', 'kezirat_hu.md'), 'w', encoding='utf-8', newline='\n') as f:
                f.write('kézi\n')
            for regi in ('KODKONYV.md', 'kozlemeny/kozlemeny_hu.md', 'parok/01_Gen.tsv'):   # lapos maradvány
                os.makedirs(os.path.dirname(os.path.join(tmp, regi)), exist_ok=True)
                with open(os.path.join(tmp, regi), 'w', encoding='utf-8', newline='\n') as f:
                    f.write('régi\n')
            CS.kiir({'README.md': 'b\n', 'data/x.tsv': 'x\n'}, tmp)
            fa = sorted(os.path.relpath(os.path.join(gy, n), tmp).replace('\\', '/')
                        for gy, _, nevek in os.walk(tmp) for n in nevek)
            self.assertEqual(fa, ['README.md', 'data/x.tsv', 'paper/kezirat_hu.md'])
            self.assertEqual(sorted(os.listdir(tmp)), ['README.md', 'data', 'paper'])    # az üres mappák is mennek
            with open(os.path.join(tmp, 'paper', 'kezirat_hu.md'), encoding='utf-8') as f:
                self.assertEqual(f.read(), 'kézi\n')
        finally:
            shutil.rmtree(tmp)

    def test_kezi_forras_az_osszegben(self):
        import hashlib
        import shutil
        import tempfile
        tmp = tempfile.mkdtemp(prefix='karoli_csomag_teszt_')
        try:
            os.makedirs(os.path.join(tmp, 'paper'))
            with open(os.path.join(tmp, 'paper', 'kezirat_en.md'), 'w', encoding='utf-8', newline='\n') as f:
                f.write('manuscript\n')
            fajlok, _ = E.export(tmp)
            self.assertEqual(fajlok['paper/kezirat_en.md'], 'manuscript\n')
            self.assertIn('%s  paper/kezirat_en.md' % hashlib.sha256(b'manuscript\n').hexdigest(),
                          fajlok['ELLENORZO_OSSZEG.sha256'])
            self.assertEqual(bukasok(fajlok, 'OSSZEG'), [])
            self.assertEqual(bukasok(fajlok, 'HARMADIK'), [])
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main(verbosity=1)
