#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_kjv_szoveg_import.py -- #118 (KJV_SZOVEG) tesztek: a jelölőtisztítás egységei (a naplok/KJV_SZOVEG_M0.md
2. pontjának bánásmódja szerint), a vers-szétvágás (\\d -> 0. vers, \\s1 -> Elotte/Utoirat, nem a versszövegbe),
és a fejlécsorok. Szintetikus USFM-mel fut, a zip nem kell hozzá. A minta-versek rögzített elvárt értékei
az M1 jóváhagyása után kerülnek be (M2).

    python eszkozok/teszt_kjv_szoveg_import.py
"""

import collections
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kjv_szoveg_import as K  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

B = chr(92)
P = '¶'


def u(s):
    """A tesztszövegben a '~' jelöli a backslash-t (olvashatóság, és nincs escape-csapda)."""
    return s.replace('~', B)


class Tisztitas(unittest.TestCase):
    def test_w_a_szo_marad_a_strong_kimarad(self):
        t = u('In the ~w beginning|strong="H7225"~w* ~w God|strong="H0430"~w* created.')
        self.assertEqual(K.tisztit(t), 'In the beginning God created.')

    def test_add_sima_es_jelolt(self):
        t = u('and darkness ~add was~add* upon the deep.')
        self.assertEqual(K.tisztit(t), 'and darkness was upon the deep.')
        self.assertEqual(K.tisztit(t, jelolt=True), 'and darkness [was] upon the deep.')

    def test_zaro_jelolo_utan_nincs_szokoz_az_irasjel_elott(self):
        t = u('of Jerahmeel ~add were~add*, Mesha')
        self.assertEqual(K.tisztit(t), 'of Jerahmeel were, Mesha')
        self.assertEqual(K.tisztit(t, jelolt=True), 'of Jerahmeel [were], Mesha')

    def test_nd_beagyazott_w(self):
        t = u('unto the ~nd ~+w LORD|strong="H3068"~+w*~nd*; for')
        self.assertEqual(K.tisztit(t), 'unto the LORD; for')

    def test_wj_beagyazott_add(self):
        t = u('~wj Two ~+add men~+add* shall be in the field.~wj*')
        self.assertEqual(K.tisztit(t), 'Two men shall be in the field.')
        self.assertEqual(K.tisztit(t, jelolt=True), 'Two [men] shall be in the field.')

    def test_pilcrow_csak_a_jeloltben(self):
        t = P + u(' And ~w God|strong="H0430"~w* said')
        self.assertEqual(K.tisztit(t), 'And God said')
        self.assertEqual(K.tisztit(t, jelolt=True), P + ' And God said')

    def test_labjegyzet_kimarad(self):
        t = u('the darkness.~f + ~fr 1.4 ~ft the light from: Heb. between ~+nd LORD~+nd*~f*')
        self.assertEqual(K.tisztit(t), 'the darkness.')

    def test_tl_a_szoveg_marad(self):
        self.assertEqual(K.tisztit(u('~tl  א ALEPH.~tl*')), 'א ALEPH.')

    def test_bekezdesjelolo_szamolva(self):
        sz = collections.Counter()
        self.assertEqual(K.tisztit(u('~q1'), szamlalo=sz), '')
        self.assertEqual(sz['q1'], 1)

    def test_leltaron_kivuli_jelolo_hibat_dob(self):
        with self.assertRaises(K.IsmeretlenJelolo):
            K.tisztit(u('text ~qs Selah~qs*'))

    def test_szamlalok(self):
        sz = collections.Counter()
        K.tisztit(u('~w a|strong="H1"~w* ~add b~add* ~nd c~nd* ') + P, szamlalo=sz)
        self.assertEqual((sz['w'], sz['add'], sz['nd'], sz['pilcrow']), (1, 1, 1, 1))


KONYV = u('\n'.join([
    '~id PSA Psalms',
    '~h Psalms',
    '~toc1 The Book of Psalms',
    '~mt1 The Book of Psalms',
    '~c 3',
    '~d A ~w Psalm|strong="H4210"~w* of David.',
    '~q1',
    '~v 1 ~nd ~+w LORD|strong="H3068"~+w*~nd*, how are they increased!',
    '~q1',
    '~v 2 Many ~add there be~add* which say.',
    '~c 119',
    '~s1 ~tl  א ALEPH.~tl*',
    '~q1',
    '~v 1 Blessed ~add are~add* the undefiled.',
    '~v 8 I will keep thy statutes.',
    '~s1 ~tl  ב BETH.~tl*',
    '~q1',
    '~v 9 Wherewithal shall a young man',
    'cleanse his way?',
    '~s1 Written to the Romans from Corinthus, ~add and sent~add* by Phebe.',
]))


class Versek(unittest.TestCase):
    def setUp(self):
        self.sz = collections.Counter()
        self.v, self.anom = K.parse_konyv(KONYV, self.sz)

    def test_nincs_anomalia_es_a_versek(self):
        self.assertEqual(self.anom, [])
        self.assertEqual(list(self.v), [(3, 0), (3, 1), (3, 2), (119, 1), (119, 8), (119, 9)])
        self.assertEqual(self.sz['fejlec_sor'], 4)

    def test_zsoltarfelirat_a_0_vers(self):
        self.assertEqual(K.tisztit(self.v[(3, 0)]['nyers']), 'A Psalm of David.')

    def test_s1_a_kovetkezo_vers_elotte_mezojebe(self):
        self.assertEqual(K.tisztit(self.v[(119, 1)]['elotte']), 'א ALEPH.')
        self.assertEqual(K.tisztit(self.v[(119, 9)]['elotte']), 'ב BETH.')

    def test_s1_nem_fuzodik_az_elozo_vershez(self):
        self.assertEqual(K.tisztit(self.v[(119, 8)]['nyers']), 'I will keep thy statutes.')
        self.assertIsNone(self.v[(119, 8)]['elotte'])

    def test_utoirat_a_konyv_utolso_versen(self):
        self.assertEqual(K.tisztit(self.v[(119, 9)]['utoirat']), 'Written to the Romans from Corinthus, and sent by Phebe.')
        self.assertIsNone(self.v[(119, 8)]['utoirat'])

    def test_vers_folytatas_sor(self):
        self.assertEqual(K.tisztit(self.v[(119, 9)]['nyers']), 'Wherewithal shall a young man cleanse his way?')
        self.assertEqual(self.sz['vers_folytatas_sor'], 1)

    def test_sorok_otmezos(self):
        rs = K.sorok({'Psa': self.v}, [('Psa', 'PSA')])
        self.assertEqual(rs[0], ('Psa.3.0', 'A Psalm of David.', 'A Psalm of David.', '', ''))
        self.assertEqual(rs[2], ('Psa.3.2', 'Many there be which say.', 'Many [there be] which say.', '', ''))
        self.assertEqual(rs[3][3], 'א ALEPH.')
        self.assertTrue(all(len(r) == 5 for r in rs))


class Fejlec(unittest.TestCase):
    def test_fejlecsorok(self):
        f = K.fejlecsorok('ab' * 32, '2026-10-18', collections.Counter(w=3))
        self.assertTrue(f[0].startswith('# GENERÁLT: eszkozok/kjv_szoveg_import.py'))
        self.assertIn('sha256=' + 'ab' * 32, f[1])
        self.assertTrue(f[1].startswith('# proveniencia: scope='))
        self.assertTrue(f[2].startswith('# licenc: közkincs'))
        self.assertTrue(f[3].startswith('# ÁLLAPOT:'))
        self.assertIn('Strong-címke (\\w strong=) 3', f[4])


if __name__ == '__main__':
    unittest.main()
