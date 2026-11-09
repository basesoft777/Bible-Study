#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_karoli_kh_mek.py -- F177 (KAROLI_KH_MEK) tesztek:
  * az RTF-dekodolas (cp1250 `\\'xx`, `\\uN`, a cel-csoportok kihagyasa, a bekezdes-stilus);
  * a MEK-kivonat mesterseges RTF-en (fejezetsor nelkuli uj fejezet, az "1. 2." szamozasi elirás, a ketvegpontos
    tartomany, a nem ertelmezheto KH-sor megorzese);
  * az osszevetes harom szintje mesterseges adaton (megerositett / kiesik / jelolt, tartomany-vegpontok,
    hibas_hivatkozas);
  * a repoban levo tablak invariansai (ha megvannak): minden HunKar-sor pontosan egyszer szerepel a javitott
    tablaban, a szintek ertekkeszlete, az alias-tabla 66 konyve, a szuro (`elfogad`) a `megerositett` szintet engedi.

    python eszkozok/teszt_karoli_kh_mek.py
"""
import collections
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(HELY)
sys.path.insert(0, HELY)

import karoli_kh_mek as K  # noqa: E402
import karoli_kh_szuro as SZ  # noqa: E402

ALIAS = {'1 Móz.': 'Gen', 'Zsolt.': 'Psa', 'Neh.': 'Neh', 'Mát.': 'Mat'}
KONYVEK = ['Gen', 'Psa']


def rtf(*bekezdesek):
    """(stílus, szöveg) bekezdésekből minimális RTF; a szöveg a `\\'xx`-escape-et maga tartalmazhatja."""
    ki = ['{\\rtf1\\ansi\\ansicpg1250{\\fonttbl{\\f0 Times;}}{\\*\\generator Teszt;}']
    for st, t in bekezdesek:
        ki.append('\\pard\\plain %s %s\\par ' % ('\\s%d' % st if st else '', rtf_szoveg(t)))
    ki.append('}')
    return ''.join(ki).encode('latin-1')


def rtf_szoveg(t):
    """A nem-ASCII karakter cp1250 `\\'xx` escape-be (ha van), egyébként `\\uN?`-be; a már escape-elt rész marad."""
    ki = []
    for ch in t:
        if ord(ch) < 128:
            ki.append(ch)
            continue
        try:
            ki.append("\\'%02x" % ch.encode('cp1250')[0])
        except UnicodeEncodeError:
            ki.append('\\u%d?' % ord(ch))
    return ''.join(ki)


class RtfDekodolas(unittest.TestCase):
    def test_cp1250_es_unicode(self):
        par = K.rtf_bekezdesek(rtf((None, '1. És monda: ős ősá')))
        self.assertEqual(par[0][1].strip(), '1. És monda: ős ősá')
        par = K.rtf_bekezdesek(b"{\\rtf1\\ansi \\pard 1. \\'c9s \\u337?s\\par }")
        self.assertEqual(par[0][1].strip(), '1. És ős')

    def test_cel_csoport_kimarad(self):
        par = K.rtf_bekezdesek(rtf((None, '1. {\\*\\bkmkstart _Toc1}Szó{\\*\\bkmkend _Toc1} vége')))
        self.assertEqual(par[0][1].strip(), '1. Szó vége')

    def test_bekezdes_stilus(self):
        par = K.rtf_bekezdesek(rtf((1, 'Cím'), (2, '1.'), (3, 'Zsolt. 1,1.'), (None, '1. Vers')))
        self.assertEqual([s for s, _ in par[:4]], [1, 2, 3, None])


class Kivonat(unittest.TestCase):
    def kiv(self, *par):
        return K.mek_kivonat(rtf(*par), ALIAS, KONYVEK)

    def test_alapeset_es_ketvegpont(self):
        sorok, nap = self.kiv(
            (1, 'Első'), (2, '1.'), (None, '1. Kezdet'), (3, '1 Móz. 2,4. , 1 Móz. 2,5. , Zsolt. 33,6.'),
            (None, '2. Második'), (1, 'Második könyv'), (2, '1.'), (None, '1. Zsoltár'), (3, 'Mát. 1,1.'))
        self.assertEqual(sorok[0], ('Gen.1.1', 'Gen.2.4', '1 Móz. 2,4.'))
        self.assertEqual(sorok[1], ('Gen.1.1', 'Gen.2.5', '1 Móz. 2,5.'))
        self.assertEqual(sorok[2], ('Gen.1.1', 'Psa.33.6', 'Zsolt. 33,6.'))
        self.assertEqual(sorok[3], ('Psa.1.1', 'Mat.1.1', 'Mát. 1,1.'))
        self.assertEqual(nap['versek'], 3)

    def test_szokoz_nelkuli_elvalaszto(self):
        sorok, _ = self.kiv((1, 'A'), (2, '1.'), (None, '1. x'), (3, 'Neh. 9,7., Zsolt. 1,1.'), (1, 'B'))
        self.assertEqual([s[1] for s in sorok], ['Neh.9.7', 'Psa.1.1'])

    def test_fejezetsor_nelkuli_uj_fejezet(self):
        sorok, nap = self.kiv((1, 'A'), (2, '1.'), (None, '1. a'), (None, '2. b'), (None, '1. c'), (3, 'Zsolt. 1,1.'),
                              (1, 'B'))
        self.assertEqual(sorok[0][0], 'Gen.2.1')
        self.assertEqual(nap['fejezet_nelkul_uj'], [('Gen', 2)])

    def test_szamozasi_elirás_sorrendbol(self):
        """A MEK '1. 2. szöveg' elírása után a versszám a sorrendből jön (Jób 24 / Zsolt 102 / Zak 11 mintájára)."""
        sorok, nap = self.kiv((1, 'A'), (2, '1.'), (None, '1. 2. egyben'), (None, '3. harmadik'),
                              (3, 'Zsolt. 1,1.'), (1, 'B'))
        self.assertEqual(sorok[0][0], 'Gen.1.2')
        self.assertTrue(nap['vers_ugras'])

    def test_ertelmezhetetlen_sor_megmarad_ures_kapcsolodoval(self):
        sorok, nap = self.kiv((1, 'A'), (2, '1.'), (None, '1. a'), (3, '1 Móz. 12,.'), (1, 'B'))
        self.assertEqual(sorok, [('Gen.1.1', '', '1 Móz. 12,.')])
        self.assertEqual(len(nap['ertelmezhetetlen_kh']), 1)

    def test_ismeretlen_konyv_megmarad(self):
        sorok, nap = self.kiv((1, 'A'), (2, '1.'), (None, '1. a'), (3, 'Tudom. 1,1.'), (1, 'B'))
        self.assertEqual(sorok[0][1], '')
        self.assertEqual(len(nap['ismeretlen_konyv']), 1)

    def test_konyvszam_eltérés_hiba(self):
        _, nap = K.mek_kivonat(rtf((1, 'A'), (2, '1.'), (None, '1. a')), ALIAS, KONYVEK)
        self.assertIn('hiba', nap)


class Osszevetes(unittest.TestCase):
    LETEZO = {'Gen.1.1', 'Gen.2.4', 'Gen.2.5', 'Psa.33.6', 'Psa.89.12', 'Gen.3.1', 'Gen.4.1', 'Gen.5.1', 'Gen.6.1'}

    def ov(self, hk, mek):
        hk = [(f, c, c.split('-')[0], c.split('-')[-1]) for f, c in hk]
        return {(s[0], s[1]): s for s in K.osszevet(hk, mek, self.LETEZO, lambda f, c: False)}

    def test_megerositett_es_tartomany(self):
        r = self.ov([('Gen.1.1', 'Gen.2.4-Gen.2.5'), ('Gen.1.1', 'Psa.33.6')],
                    {'Gen.1.1': [('Gen.2.4', 'a'), ('Gen.2.5', 'b'), ('Psa.33.6', 'c')]})
        self.assertEqual(r[('Gen.1.1', 'Gen.2.4-Gen.2.5')][2:4], ('megerositett', 'HunKar+MEK'))
        self.assertEqual(r[('Gen.1.1', 'Psa.33.6')][2], 'megerositett')
        self.assertEqual(len(r), 2)

    def test_tartomany_egy_vegpont_nem_egyezes(self):
        r = self.ov([('Gen.1.1', 'Gen.2.4-Gen.2.5')], {'Gen.1.1': [('Gen.2.4', 'a')]})
        self.assertEqual(r[('Gen.1.1', 'Gen.2.4-Gen.2.5')][2], 'jelolt')
        self.assertIn('eltero_lista', r[('Gen.1.1', 'Gen.2.4-Gen.2.5')][4])
        self.assertEqual(r[('Gen.1.1', 'Gen.2.4')][2:4], ('jelolt', 'MEK'))

    def test_kiesik_ha_a_mek_ures(self):
        r = self.ov([('Gen.1.1', 'Psa.33.6')], {})
        self.assertEqual(r[('Gen.1.1', 'Psa.33.6')][2:4], ('kiesik', 'HunKar'))

    def test_jelolt_elter_es_csak_mek(self):
        r = self.ov([('Gen.3.1', 'Psa.33.6')], {'Gen.3.1': [('Psa.89.12', 'x')], 'Gen.4.1': [('Gen.5.1', 'y')]})
        self.assertEqual(r[('Gen.3.1', 'Psa.33.6')][2], 'jelolt')
        self.assertEqual(r[('Gen.3.1', 'Psa.89.12')][2:4], ('jelolt', 'MEK'))
        self.assertEqual(r[('Gen.4.1', 'Gen.5.1')][2:4], ('jelolt', 'MEK'))

    def test_hibas_hivatkozas_nem_javitott(self):
        r = self.ov([('Gen.3.1', 'Gen.99.9')], {'Gen.3.1': [('Gen.99.9', 'z')], 'Gen.4.1': [('Gen.26.59', 'w')]})
        self.assertEqual(r[('Gen.3.1', 'Gen.99.9')][2], 'jelolt')  # az egyező, de nem létező vers sem megerősített
        self.assertIn('hibas_hivatkozas=Gen.99.9', r[('Gen.3.1', 'Gen.99.9')][4])
        self.assertIn('hibas_hivatkozas=Gen.26.59', r[('Gen.4.1', 'Gen.26.59')][4])

    def test_ertelmezhetetlen_mek_sor(self):
        r = self.ov([], {'Gen.3.1': [('', '1 Sám. 12,.')]})
        self.assertIn('ertelmezhetetlen', r[('Gen.3.1', '')][4])
        self.assertEqual(r[('Gen.3.1', '')][2], 'jelolt')


class JeloltSzabaly(unittest.TestCase):
    """F181: a jelolt szint bontása és a beemelési szabály mesterséges adaton."""
    LETEZO = {'Gen.1.1', 'Gen.2.4', 'Gen.2.5', 'Gen.3.1', 'Gen.4.1', 'Gen.5.1', 'Gen.6.1', 'Psa.33.6', 'Psa.89.12',
              'Mat.5.32', 'Exo.6.20', 'Num.26.59'}

    def bontas(self, sorok, gy_hk=(), gy_mek=()):
        return {(r['forras_vers'], r['cel'], r['oldal']): r for r in K.jelolt_bontas(
            sorok, self.LETEZO, lambda f, c: False, lambda f, c: False, set(gy_hk), set(gy_mek))}

    def test_kapcsolat_tipusok(self):
        self.assertEqual(K.kapcsolat('Gen.2.4', 'Gen.2.4-Gen.2.5'), 'tartomány/vershatár')
        self.assertEqual(K.kapcsolat('Gen.2.6', 'Gen.2.4-Gen.2.5'), 'tartomány/vershatár')
        self.assertEqual(K.kapcsolat('Gal.2.13', 'Gal.3.13'), 'fejezet-elírás')
        self.assertEqual(K.kapcsolat('Exo.26.59', 'Num.26.59'), 'könyv-elírás')
        self.assertEqual(K.kapcsolat('Gen.2.9', 'Gen.2.4'), 'versszám-elírás')
        self.assertIsNone(K.kapcsolat('Psa.89.12', 'Gen.2.4'))

    def test_cel_letezik_tartomany(self):
        self.assertTrue(K.cel_letezik('Gen.2.4-Gen.2.5', self.LETEZO))
        self.assertFalse(K.cel_letezik('Gen.2.4-Gen.2.9', self.LETEZO))

    def test_mek_ismetlodo(self):
        mek = {'A.1.1': [('Gen.1.1', 'a'), ('Gen.2.4', 'b')], 'A.1.2': [('Gen.2.4', 'c'), ('Gen.1.1', 'd')],
               'A.1.3': [('Gen.1.1', 'e')], 'A.1.4': [('Gen.1.1', 'f')]}
        self.assertEqual(K.mek_ismetlodo(mek), {'A.1.1', 'A.1.2'})  # az egyelemű egyezés nem ismétlődés

    def test_beemel_nem_letezo_gyanus(self):
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem'),
               ('Gen.4.1', 'Psa.89.12', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem'),
               ('Gen.5.1', 'Gen.99.9', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem;hibas_hivatkozas=Gen.99.9'),
               ('Gen.6.1', 'Gen.2.4', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem')]
        b = self.bontas(jav, gy_hk={'Gen.3.1'}, gy_mek={'Gen.4.1', 'Gen.6.1'})
        self.assertEqual(b[('Gen.3.1', 'Psa.33.6', 'MEK')]['dontes'], K.D_BEEMEL)  # a HunKar-oldali gyanús-jelölés nem zár ki
        self.assertEqual(b[('Gen.4.1', 'Psa.89.12', 'MEK')]['dontes'], K.D_GYANUS)
        self.assertEqual(b[('Gen.5.1', 'Gen.99.9', 'MEK')]['dontes'], K.D_NEMLETEZO)
        self.assertEqual(b[('Gen.6.1', 'Gen.2.4', 'MEK')]['dontes'], K.D_GYANUS)

    def test_hunkar_oldali_gyanus_jeloles_nem_zar_ki(self):
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem')]
        b = K.jelolt_bontas(jav, self.LETEZO, lambda f, c: False, lambda f, c: False, {'Gen.3.1'}, set())
        self.assertEqual(b[0]['dontes'], K.D_BEEMEL)

    def test_elirasgyanus_osztaly_marad(self):
        # a MEK-cél egyetlen összetevőben (fejezet) tér el a forrásvers HunKar-sorától és létezik -> jelolt marad
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Gen.3.1', 'Psa.89.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem')]
        letezo = set(self.LETEZO) | {'Psa.89.6'}
        b = {(r['cel'], r['oldal']): r for r in K.jelolt_bontas(
            jav, letezo, lambda f, c: False, lambda f, c: False, set(), set())}
        self.assertEqual(b[('Psa.89.6', 'MEK')]['altipus'], 'fejezet-elírás')
        self.assertEqual(b[('Psa.89.6', 'MEK')]['dontes'], K.D_ELIRAS)
        self.assertEqual(b[('Psa.33.6', 'HunKar')]['dontes'], K.D_HK_MARAD)

    def test_a_tsk_nem_szabaly_feltetel(self):
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem')]
        igen = K.jelolt_bontas(jav, self.LETEZO, lambda f, c: True, lambda f, c: True, set(), set())
        nem = K.jelolt_bontas(jav, self.LETEZO, lambda f, c: False, lambda f, c: False, set(), set())
        self.assertEqual(igen[0]['dontes'], nem[0]['dontes'])
        self.assertEqual(nem[0]['dontes'], K.D_BEEMEL)

    def test_egyezo_nem_letezo_marad(self):
        jav = [('Gen.3.1', 'Gen.99.9', 'jelolt', 'HunKar+MEK', 'egyezik;hibas_hivatkozas=Gen.99.9')]
        self.assertEqual(self.bontas(jav)[('Gen.3.1', 'Gen.99.9', 'egyező')]['dontes'], K.D_NEMLETEZO)

    def test_hunkar_oldali_sor_sorsa(self):
        # a MEK-sor beemelődik -> a HunKar-sor kiesik; a MEK-sor nem létező -> a HunKar-sor jelölt marad
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Gen.3.1', 'Psa.89.12', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem'),
               ('Gen.4.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Gen.4.1', 'Gen.99.9', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem;hibas_hivatkozas=Gen.99.9')]
        b = self.bontas(jav)
        self.assertEqual(b[('Gen.3.1', 'Psa.33.6', 'HunKar')]['dontes'], K.D_HK_KIESIK)
        self.assertEqual(b[('Gen.4.1', 'Psa.33.6', 'HunKar')]['dontes'], K.D_HK_MARAD)

    def test_beemel_alkalmazasa(self):
        jav = [('Gen.1.1', 'Psa.33.6', 'megerositett', 'HunKar+MEK', 'egyezik', 'p'),
               ('Gen.3.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem', 'p'),
               ('Gen.3.1', 'Psa.89.12', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem', 'p'),
               ('Gen.4.1', 'Gen.99.9', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem;hibas_hivatkozas=Gen.99.9', 'p'),
               ('Gen.5.1', 'Psa.33.6', 'kiesik', 'HunKar', 'mek_ures_vers;tsk=nem', 'p')]
        b = K.jelolt_bontas([m[:5] for m in jav], self.LETEZO, lambda f, c: False, lambda f, c: False, set(), set())
        uj = K.beemel(jav, b, '2026-11-09')
        self.assertEqual(len(uj), len(jav))
        self.assertEqual([m[2] for m in uj], ['megerositett', 'kiesik', 'megerositett', 'jelolt', 'kiesik'])
        self.assertIn('szabaly=F181', uj[2][4])
        self.assertEqual(uj[0], list(jav[0]))
        self.assertEqual(uj[3], list(jav[3]))
        # idempotens
        b2 = K.jelolt_bontas([m[:5] for m in uj], self.LETEZO, lambda f, c: False, lambda f, c: False, set(), set())
        self.assertEqual(K.beemel(uj, b2, '2026-11-09'), uj)


@unittest.skipUnless(os.path.exists(os.path.join(GYOKER, K.JAVITOTT)) and os.path.exists(os.path.join(GYOKER, K.MEK_TSV)),
                     'a javított tábla nincs a repóban')
class RepoTablak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jav = K.tsv_sorok(K.JAVITOTT)
        cls.hk = K.hunkar_sorok()
        cls.mek = K.tsv_sorok(K.MEK_TSV)

    def test_oszlopszam_es_szintek(self):
        for m in self.jav:
            self.assertEqual(len(m), 6, m)
            self.assertIn(m[2], K.SZINTEK)
            self.assertIn(m[3], ('HunKar', 'HunKar+MEK', 'MEK'))

    def test_minden_hunkar_sor_pontosan_egyszer(self):
        hk = collections.Counter((f, c) for f, c, _, _ in self.hk)
        jav = collections.Counter((m[0], m[1]) for m in self.jav if m[3] in ('HunKar', 'HunKar+MEK'))
        self.assertEqual(hk, jav)

    def test_megerositett_ketforrasu_kiesik_hunkar(self):
        """A #177 szintjei, az F181 beemelésével: a megerősített sor vagy két forrású, vagy a szabály által
        beemelt MEK-sor (`szabaly=F181`); a kiesik sor HunKar-sor; a MEK-sor csak a szabállyal lehet nem jelölt."""
        for m in self.jav:
            if m[2] == 'megerositett':
                self.assertIn(m[3], ('HunKar+MEK', 'MEK'))
                self.assertNotIn('hibas_hivatkozas', m[4])
                if m[3] == 'MEK':
                    self.assertIn('szabaly=F181', m[4])
            if m[2] == 'kiesik':
                self.assertEqual(m[3], 'HunKar')
            if m[3] == 'MEK' and m[2] != 'jelolt':
                self.assertEqual(m[2], 'megerositett')
                self.assertIn('szabaly=F181', m[4])

    def test_kiesik_sor_tsk_jelolest_kap(self):
        """ELLENOR_F177 1.: minden kiesik sor indokában ott a tsk=igen / tsk=nem, mint az eltero_lista és csak_mek soron."""
        for m in self.jav:
            if m[2] == 'kiesik':
                self.assertRegex(m[4], r'^(mek_ures_vers|eltero_lista);tsk=(igen|nem)(;|$)', m)

    def test_kiesik_tsk_jeloles_a_szabalyt_koveti(self):
        r = Osszevetes().ov([('Gen.1.1', 'Psa.33.6')], {})
        self.assertIn('tsk=nem', r[('Gen.1.1', 'Psa.33.6')][4])
        hk = [('Gen.1.1', 'Psa.33.6', 'Psa.33.6', 'Psa.33.6')]
        s = K.osszevet(hk, {}, Osszevetes.LETEZO, lambda f, c: True)
        self.assertIn('tsk=igen', s[0][4])

    def test_kiesik_verse_a_mekben_ures(self):
        mek_versek = {m[0] for m in self.mek}
        for m in self.jav:
            if m[2] == 'kiesik' and 'szabaly=F181' not in m[4]:
                self.assertNotIn(m[0], mek_versek)

    def test_mek_sor_megvan_a_javitottban(self):
        """Minden MEK-sor vagy egyezésként (HunKar+MEK), vagy csak_mek-ként szerepel."""
        jav = {(m[0], m[1]) for m in self.jav}
        vegpont = set()
        for m in self.jav:
            if m[3] == 'HunKar+MEK':
                for v in m[1].split('-'):
                    vegpont.add((m[0], v))
        for m in self.mek:
            self.assertTrue((m[0], m[1]) in jav or (m[0], m[1]) in vegpont, m[:3])

    def test_brief_peldai(self):
        d = {(m[0], m[1]): m for m in self.jav}
        self.assertEqual(d[('Gen.1.1', 'Psa.33.6')][2], 'megerositett')
        e = d[('Exo.6.20', 'Exo.26.59')]
        self.assertEqual(e[2], 'jelolt')
        self.assertIn('hibas_hivatkozas=Exo.26.59', e[4])
        self.assertIn('hibas_hivatkozas=Gen.15.26', d[('Deu.7.15', 'Gen.15.26')][4])

    def test_szuro(self):
        self.assertTrue(SZ.elfogad('Gen.1.1', 'Psa.33.6'))
        self.assertFalse(SZ.elfogad('Exo.6.20', 'Exo.26.59'))
        kiesik = next(m for m in self.jav if m[2] == 'kiesik')
        self.assertFalse(SZ.elfogad(kiesik[0], kiesik[1]))
        self.assertEqual(SZ.szint(kiesik[0], kiesik[1]), 'kiesik')

    def test_f181_szabaly_a_tablan(self):
        """F181: a beemelt MEK-sor célja és forrásverse létezik, a forrásvers nem gyanús ismétlődő; a MEK-oldali
        jelölt maradék indoka nem létező célvers vagy gyanús ismétlődés; a beemelés idempotens; a sorszám állandó."""
        gy_hk = K.gyanus_versek()
        gy_mek = K.mek_ismetlodo(K.mek_sorok_betolt())
        letezo = K.karoli_versek()
        self.assertEqual(len(self.jav), 35204)
        be = [m for m in self.jav if m[2] == 'megerositett' and m[3] == 'MEK']
        self.assertTrue(be)
        for m in be:
            self.assertTrue(K.cel_letezik(m[1], letezo) and m[0] in letezo, m)
            self.assertNotIn(m[0], gy_mek)  # csak a MEK-oldali ismétlődés zár ki; a HunKar-oldali jelölés nem (DT-F181f)
        for m in self.jav:
            if m[2] == 'jelolt' and m[3] == 'MEK':
                nincs = not K.cel_letezik(m[1], letezo) or m[0] not in letezo
                elir = m[0] in {x[0] for x in self.jav if x[2] == 'jelolt' and x[3] == 'HunKar'}
                self.assertTrue(nincs or m[0] in gy_mek or elir, m)
        van_be = {m[0] for m in be}
        for m in self.jav:
            if m[2] == 'jelolt' and m[3] == 'HunKar' and m[0] in van_be:
                # a MEK-lista beemelődött -> a HunKar-sor kiesik; kivétel az elírás-gyanús MEK-sor párja (jelolt marad)
                self.assertIn(m[0], {x[0] for x in self.jav if x[2] == 'jelolt' and x[3] == 'MEK'}, m)
        sorok6 = [m[:6] for m in self.jav]
        bontas, _, _ = K._bontas_sorokra(sorok6)
        self.assertEqual(K.beemel(sorok6, bontas, '2026-11-09'), [list(m) for m in sorok6])

    def test_szuro_csak_mek_megerositett_sor(self):
        """F181: a szűrő a csak a MEK-ben álló, megerősített sort elfogadja és kiadja (mek_sorok); a kiesik és a
        jelolt sor nem jut át."""
        mek = SZ.mek_sorok()
        be = [m for m in self.jav if m[2] == 'megerositett' and m[3] == 'MEK']
        self.assertEqual(len(mek), len(be))
        self.assertTrue(mek)
        for r in mek:
            self.assertTrue(SZ.elfogad(r['Igehely'], r['Kapcsolódó igehely']))
            self.assertRegex(r['Kapcsolódó igehely magyar megjelenítése'], r'^\S+ \d+,\d+$')
        self.assertEqual(len(SZ.mek_sorok(mek[0]['Igehely'])), sum(1 for r in mek if r['Igehely'] == mek[0]['Igehely']))
        for m in self.jav:
            if m[2] in ('kiesik', 'jelolt'):
                self.assertFalse(SZ.elfogad(m[0], m[1]), m)
        kulcsok = {(r['Igehely'], r['Kapcsolódó igehely']) for r in mek}
        self.assertFalse(kulcsok & {(f, c) for f, c, _, _ in self.hk if SZ.szint(f, c) != 'megerositett'})

    def test_alias_tabla(self):
        al = K.mek_aliasok()
        self.assertEqual(len(set(al.values())), 66)
        self.assertEqual(set(al.values()), set(K.step_konyvek()))
        self.assertEqual(K.aliasok('karoli_1908')['Sir'], 'Lam')

    def test_versszerkezet(self):
        sz = K.tsv_sorok(K.SZERKEZET)
        self.assertEqual(len(sz), 1189)
        self.assertEqual(sum(int(m[2]) for m in sz), 31170)


if __name__ == '__main__':
    unittest.main()
