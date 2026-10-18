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
        self.assertEqual(K.tisztit(t, jelolt=True), '‹Two [men] shall be in the field.›')

    def test_wj_a_vers_kozepen(self):
        t = u('And he said unto them, ~wj Follow me.~wj* And they')
        self.assertEqual(K.tisztit(t), 'And he said unto them, Follow me. And they')
        self.assertEqual(K.tisztit(t, jelolt=True), 'And he said unto them, ‹Follow me.› And they')

    def test_wj_versen_atnyulo_lezaras(self):
        sz = collections.Counter()
        # nyitas a versben, zaras a kovetkezo versben: a vers vegen lezarodik
        self.assertEqual(K.tisztit(u('said, ~wj Verily I say'), True, sz), 'said, ‹Verily I say›')
        # zaras a versben, nyitas az elozoben: a vers elejen megnyilik
        self.assertEqual(K.tisztit(u('unto you.~wj* And'), True, sz), '‹unto you.› And')
        self.assertEqual(sz['wj_atnyulo_lezaras'], 2)
        self.assertEqual(K.tisztit(u('said, ~wj Verily I say')), 'said, Verily I say')

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


# A jóváhagyott minta (naplok/KJV_SZOVEG_M1_minta.md, DT-F118e): a nyers USFM a forrásból (2026-10-17-i csomag),
# a lábjegyzet nélkül; az elvárt (Szöveg, Szöveg_jelolt) a jóváhagyott érték.
MINTA_NYERS = {
    'Gen.1.2': ('And the ~w earth|strong="H0776"~w* ~w was|strong="H1961"~w* without ~w form|strong="H8414"~w*, and ~w void|strong="H0922"~w*; '
                'and ~w darkness|strong="H2822"~w* ~add was~add* upon the ~w face|strong="H6440"~w* of the ~w deep|strong="H8415"~w*. '
                'And the ~w Spirit|strong="H7307"~w* of ~w God|strong="H0430"~w* ~w moved|strong="H7363"~w* ~w upon|strong="H5921"~w* '
                'the ~w face|strong="H6440"~w* of the ~w waters|strong="H4325"~w*.'),
    'Psa.3.1': ('~nd ~+w LORD|strong="H3068"~+w*~nd*, how are they ~w increased|strong="H7231"~w* that ~w trouble|strong="H6862"~w* me! '
                '~w many|strong="H7227"~w* ~add are~add* they that rise ~w up|strong="H6965"~w* against me.'),
    'Mrk.9.43': ('~wj And if thy hand offend thee, cut it off: it is better for thee to enter into life maimed, than having two hands '
                 'to go into hell, into the fire that never shall be quenched:~wj*'),
    'Luk.6.41': ('~wj And why beholdest thou the mote that is in thy brother\u2019s eye, but perceivest not the beam that is in thine own eye?~wj*'),
    'Luk.17.36': ('~wj Two ~+add men~+add* shall be in the field; the one shall be taken, and the other left.~wj*'),
    '1Jn.2.23': ('~w Whosoever|strong="G3956"~w* ~w denieth|strong="G0720"~w* the ~w Son|strong="G5207"~w*, the same ~w hath|strong="G2192"~w* '
                 '~w not|strong="G3761"~w* the ~w Father|strong="G3962"~w*: ~add [but] ~+w he that acknowledgeth|strong="G3670"~+w* '
                 '~+w the Son|strong="G5207"~+w* ~+w hath|strong="G2192"~+w* ~+w the Father|strong="G3962"~+w* ~+w also|strong="G2532"~+w*~add*.'),
}

MINTA_ELVART = {
    'Gen.1.1': ('In the beginning God created the heaven and the earth.', 'In the beginning God created the heaven and the earth.', '', ''),
    'Gen.1.2': ('And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.',
                'And the earth was without form, and void; and darkness [was] upon the face of the deep. And the Spirit of God moved upon the face of the waters.', '', ''),
    'Gen.1.3': ('And God said, Let there be light: and there was light.', 'And God said, Let there be light: and there was light.', '', ''),
    'Psa.3.0': ('A Psalm of David, when he fled from Absalom his son.', 'A Psalm of David, when he fled from Absalom his son.', '', ''),
    'Psa.3.1': ('LORD, how are they increased that trouble me! many are they that rise up against me.',
                'LORD, how are they increased that trouble me! many [are] they that rise up against me.', '', ''),
    'Psa.3.2': ('Many there be which say of my soul, There is no help for him in God. Selah.',
                'Many [there be] which say of my soul, [There is] no help for him in God. Selah.', '', ''),
    'Psa.119.1': ('Blessed are the undefiled in the way, who walk in the law of the LORD.',
                  'Blessed [are] the undefiled in the way, who walk in the law of the LORD.', '\u05d0 ALEPH.', ''),
    'Psa.119.8': ('I will keep thy statutes: O forsake me not utterly.', 'I will keep thy statutes: O forsake me not utterly.', '', ''),
    'Psa.119.9': ('Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word.',
                  'Wherewithal shall a young man cleanse his way? by taking heed [thereto] according to thy word.', '\u05d1 BETH.', ''),
    'Mat.1.1': ('The book of the generation of Jesus Christ, the son of David, the son of Abraham.',
                'The book of the generation of Jesus Christ, the son of David, the son of Abraham.', '', ''),
    'Rev.22.21': ('The grace of our Lord Jesus Christ be with you all. Amen.', 'The grace of our Lord Jesus Christ [be] with you all. Amen.', '', ''),
    'Mrk.9.43': ('And if thy hand offend thee, cut it off: it is better for thee to enter into life maimed, than having two hands to go into hell, into the fire that never shall be quenched:',
                 '\u2039And if thy hand offend thee, cut it off: it is better for thee to enter into life maimed, than having two hands to go into hell, into the fire that never shall be quenched:\u203a', '', ''),
    'Luk.6.41': ('And why beholdest thou the mote that is in thy brother\u2019s eye, but perceivest not the beam that is in thine own eye?',
                 '\u2039And why beholdest thou the mote that is in thy brother\u2019s eye, but perceivest not the beam that is in thine own eye?\u203a', '', ''),
    'Luk.17.36': ('Two men shall be in the field; the one shall be taken, and the other left.',
                  '\u2039Two [men] shall be in the field; the one shall be taken, and the other left.\u203a', '', ''),
    'Rom.16.27': ('To God only wise, be glory through Jesus Christ for ever. Amen.', 'To God only wise, [be] glory through Jesus Christ for ever. Amen.', '',
                  'Written to the Romans from Corinthus, and sent by Phebe servant of the church at Cenchrea.'),
    '1Jn.2.23': ('Whosoever denieth the Son, the same hath not the Father: [but] he that acknowledgeth the Son hath the Father also.',
                 'Whosoever denieth the Son, the same hath not the Father: [[but] he that acknowledgeth the Son hath the Father also].', '', ''),
}


class JovahagyottMinta(unittest.TestCase):
    """A minta-versek a nyers USFM-ből (zip nélkül, CI-ben is fut)."""

    def test_minta_nyersbol(self):
        for ih, nyers in MINTA_NYERS.items():
            with self.subTest(ih=ih):
                self.assertEqual((K.tisztit(u(nyers)), K.tisztit(u(nyers), jelolt=True)), MINTA_ELVART[ih][:2])

    def test_1jn_2_23_a_forras_szerint(self):
        szoveg, jelolt = MINTA_ELVART['1Jn.2.23'][:2]
        self.assertIn('[but]', szoveg)
        self.assertIn('[[but] ', jelolt)


ZIP = os.environ.get('KJV_ZIP', r'C:\Users\bases\Desktop\kjv_munka\kjv.zip')


@unittest.skipUnless(os.path.exists(ZIP), 'a kjv.zip nincs meg (KJV_ZIP); a teljes minta-ellenőrzés kimarad')
class JovahagyottMintaZipbol(unittest.TestCase):
    """Mind a 16 minta-vers, mind az öt mező, a valódi forrásból (a zip a repón kívül van, DT-F118d)."""

    def test_minta_16_vers(self):
        self.assertEqual(K.sha256(ZIP), K.VART_SHA256)
        kk = K.f19.lista_konyvek()
        adat, anom, _ = K.olvas(ZIP, kk)
        self.assertEqual(anom, [])
        rs = {r[0]: r for r in K.sorok(adat, kk)}
        for ih, elvart in MINTA_ELVART.items():
            with self.subTest(ih=ih):
                self.assertEqual(rs[ih][1:], elvart)


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
