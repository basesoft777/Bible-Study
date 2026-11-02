#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_proza_1a.py -- DT-F1Aa: az `eszkozok/proza_1a.py` mérő és az
`eszkozok/ellenoriz.py` 25. szabályának tesztjei. A mérce az arany lap
(ISTENTISZT-001, 1Móz 4:26); az ellenpéldák a felhasználó 2026-11-02-i ALVIL-001-
töredékei. A szabály-tesztek ideiglenes (repón kívüli) könyvtárban futnak.

    python eszkozok/teszt_proza_1a.py
"""

import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ellenoriz as E  # noqa: E402
import proza_1a as P  # noqa: E402

ARANY = ('<a id="ige-1móz-4-26"></a>\n'
         '**1Móz 4:26**\n'
         '*Séthnek is született fia, és nevezé annak nevét Énósnak. Akkor kezdték segítségül hívni az Úrnak nevét.*\n'
         'A formula első előfordulása — Séth fia, Énós nemzedéke; a Kain-vonal önerős civilizációépítése utáni '
         'korszakváltás jele.\n'
         'Funkció: a motívum legelső megjelenése a kánonban, minden későbbi eset erre vezethető vissza\n')


def blokk(igehely, proza, funkcio=None):
    sorok = ['<a id="ige-x"></a>', '**%s**' % igehely, '*Károli-szöveg.*']
    if proza:
        sorok.append(proza)
    if funkcio is not None:
        sorok.append('Funkció: %s' % funkcio)
    return '\n'.join(sorok) + '\n'


def lap(*blokkok):
    return ('# cím\n\n#### 1/a. Az igehelyek szövege\n\n**Mit mutat ez a rész?** bevezető.\n\n'
            + '\n'.join(blokkok) + '\n## 1/b. Kizárt és vizsgált helyek\n\n'
            + blokk('Kívül 1:1', 'ez már nem az 1/a része'))


class Osztalyozas(unittest.TestCase):

    def test_arany_lap_kerek(self):
        m = P.meres(lap(ARANY))
        self.assertEqual(m, [('1Móz 4:26', 'kerek', 'van', m[0][3])])

    def test_felhasznalo_toredekei(self):
        for proza in ['Jákób gyásza: "leszállok fiamhoz a Seolba, gyászolva"',
                      'Benjámin miatti félelem',
                      'Júda közbenjárása',
                      '"és befedte őket a föld"',
                      'Isten haragjának tüze "a Seol fenekéig" ég',
                      '"az Úr... Seolba visz és onnan felhoz" — Anna éneke',
                      '"a Seol kötelei körülvettek" (= Zsolt 18:6 párhuzam)',
                      'Dávid Salamonnak — Joáb "őszen szálljon a Seolba"',
                      'ua. — Simei']:
            self.assertEqual(P.proza_osztaly(proza), 'töredék', proza)

    def test_heber_es_zarojel_nem_szamit(self):
        self.assertEqual(P.proza_osztaly('אָרוּר (árúr, átok, első, kimondás, kígyó, föld) — az átok'), 'töredék')

    def test_hianyzo_proza_es_funkcio(self):
        m = P.meres(lap(blokk('Jób 1:1', '')))
        self.assertEqual(m[0][1:3], ('hiányzik', 'hiányzik'))

    def test_funkcio_toredek(self):
        self.assertEqual(P.funkcio_osztaly('krisztológiai betöltés'), 'töredék')
        self.assertEqual(P.funkcio_osztaly('a próbatétel kudarca'), 'van')

    def test_html_megjegyzes_nem_proza(self):
        m = P.meres(lap(blokk('Jób 1:1', 'rövid <!-- GENERÁLT: hosszú hosszú hosszú hosszú hosszú hosszú hosszú -->')))
        self.assertEqual(m[0][1], 'töredék')

    def test_1a_hatara(self):
        m = P.meres(lap(ARANY, blokk('Jób 1:1', 'Benjámin miatti félelem')))
        self.assertEqual([x[0] for x in m], ['1Móz 4:26', 'Jób 1:1'])
        self.assertEqual(P.osszesit(m)['arany'], 1)


class AranyLap(unittest.TestCase):

    def test_az_elo_arany_lap_minden_igehelye_arany_szintu(self):
        # DT-F1Ab óta a „ — ” nélküli `funkcio` is a „Funkció:” sorba kerül
        m = P.lap_meres('ISTENTISZT-001')
        if m is None:
            self.skipTest('nincs lexikon/ISTENTISZT-001_TUDOMANYOS.md')
        d = P.osszesit(m)
        self.assertEqual(d['arany'], d['igehely'], [x[:3] for x in m if x[1:3] != ('kerek', 'van')])


class Szabaly25(unittest.TestCase):

    def setUp(self):
        self.gyoker = tempfile.mkdtemp(prefix='teszt_proza_1a_')
        os.makedirs(os.path.join(self.gyoker, 'adat'))
        os.makedirs(os.path.join(self.gyoker, 'lexikon'))

    def tearDown(self):
        shutil.rmtree(self.gyoker, ignore_errors=True)

    def ir(self, mid, szoveg):
        with open(os.path.join(self.gyoker, 'lexikon', mid + '_TUDOMANYOS.md'), 'w', encoding='utf-8') as f:
            f.write(szoveg)

    def test_rendben_ha_minden_arany(self):
        self.ir('ARANY-001', lap(ARANY))
        s = E.szabaly25_proza_1a(os.path.join(self.gyoker, 'adat'))
        self.assertEqual(s.verdict, 'RENDBEN')

    def test_jelentes_toredeknel(self):
        self.ir('ARANY-001', lap(ARANY))
        self.ir('TORED-001', lap(blokk('1Móz 42:38', 'Benjámin miatti félelem'), ARANY))
        s = E.szabaly25_proza_1a(os.path.join(self.gyoker, 'adat'))
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertEqual(s.n, 1)
        self.assertTrue(s.peldak[0].startswith('TORED-001: 1/2'))

    def test_kezi_lap_nelkul(self):
        shutil.rmtree(os.path.join(self.gyoker, 'lexikon'))
        s = E.szabaly25_proza_1a(os.path.join(self.gyoker, 'adat'))
        self.assertEqual(s.verdict, 'KÉZI')


if __name__ == '__main__':
    unittest.main(verbosity=2)
