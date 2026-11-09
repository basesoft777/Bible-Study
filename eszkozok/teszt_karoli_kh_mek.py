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

    def test_e1_nem_letezo_mek_par_nem_iteli_el_a_hunkar_sort(self):
        """DT-F181g (ELLENOR_F181 E1): a helyes HunKar-sort a nem létező célú MEK-pár nem ítéli el, akkor sem, ha a
        versen más MEK-sor beemelődik (Neh 1:5 -> 9:32, MEK 4,32; Ján 8:12 -> 12:46, MEK 9,46)."""
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Gen.3.1', 'Psa.99.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem;hibas_hivatkozas=Psa.99.6'),
               ('Gen.3.1', 'Mat.5.32', 'jelolt', 'MEK', 'csak_mek;mek_alak=y;tsk=nem')]
        b = self.bontas(jav)
        self.assertEqual(b[('Gen.3.1', 'Psa.33.6', 'HunKar')]['dontes'], K.D_HK_E1)
        self.assertEqual(b[('Gen.3.1', 'Psa.99.6', 'MEK')]['dontes'], K.D_NEMLETEZO)
        self.assertEqual(b[('Gen.3.1', 'Mat.5.32', 'MEK')]['dontes'], K.D_BEEMEL)
        uj = K.beemel([m + ('p',) for m in jav], K.jelolt_bontas(
            jav, self.LETEZO, lambda f, c: False, lambda f, c: False, set(), set()), '2026-11-09')
        self.assertEqual(uj[0][2], 'megerositett')
        self.assertEqual(uj[0][3], 'HunKar')
        self.assertIn('mek_par_nem_letezik=x', uj[0][4])
        self.assertEqual(uj[1][2], 'jelolt')

    def test_e1_a_kimenet_nem_fugg_a_fuggetlen_sorok_beemelesetol(self):
        """A Lev 23:17 -> Lev 2:12 eset: ugyanaz a döntés, akár van a versen beemelődő MEK-sor, akár nincs."""
        par = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Gen.3.1', 'Psa.99.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem;hibas_hivatkozas=Psa.99.6')]
        mas = par + [('Gen.3.1', 'Mat.5.32', 'jelolt', 'MEK', 'csak_mek;mek_alak=y;tsk=nem')]
        self.assertEqual(self.bontas(par)[('Gen.3.1', 'Psa.33.6', 'HunKar')]['dontes'], K.D_HK_E1)
        self.assertEqual(self.bontas(mas)[('Gen.3.1', 'Psa.33.6', 'HunKar')]['dontes'], K.D_HK_E1)

    def test_e1_nem_vonatkozik_a_letezo_elirasgyanus_parra_es_a_hibas_hunkar_celra(self):
        # a pár létező (elírás-gyanús): a HunKar-sor jelolt marad; a HunKar-cél nem létezik: nincs E1
        jav = [('Gen.3.1', 'Psa.33.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Gen.3.1', 'Psa.89.6', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem')]
        letezo = set(self.LETEZO) | {'Psa.89.6'}
        b = {(r['cel'], r['oldal']): r for r in K.jelolt_bontas(
            jav, letezo, lambda f, c: False, lambda f, c: False, set(), set())}
        self.assertEqual(b[('Psa.33.6', 'HunKar')]['dontes'], K.D_HK_MARAD)
        jav2 = [('Gen.3.1', 'Psa.99.6', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem;hibas_hivatkozas=Psa.99.6'),
                ('Gen.3.1', 'Psa.99.9', 'jelolt', 'MEK', 'csak_mek;mek_alak=x;tsk=nem;hibas_hivatkozas=Psa.99.9')]
        self.assertNotEqual(self.bontas(jav2)[('Gen.3.1', 'Psa.99.6', 'HunKar')]['dontes'], K.D_HK_E1)

    NEH = {'Neh.1.5', 'Psa.35.12', 'Neh.4.8', 'Neh.4.9', 'Neh.9.32', 'Psa.38.10', 'Psa.41.10', 'Psa.42.2', 'Psa.42.3',
           'Psa.23.2', 'Psa.23.3'}

    def test_e2_minta_felismerese(self):
        """DT-F181h (ELLENOR_F181 E2): a HunKar `X a:b` helyett a MEK `X c:a` és `X c:b` (az egyik nem létezik)."""
        lista = [('Neh.4.8', ''), ('Neh.4.9', ''), ('Neh.4.32', '')]
        m = K.e2_mintak(lista, self.NEH, ['Neh.9.32'])
        self.assertEqual(len(m), 1)
        self.assertEqual((m[0]['cel'], m[0]['hunkar'], m[0]['letezo_tagok']), ('Neh.9.32', 'Neh.9.32', ['Neh.4.9']))
        # HunKar-megfelelő nélkül is minta (a töredék jelolt lesz)
        self.assertIsNone(K.e2_mintak(lista, self.NEH, [])[0]['hunkar'])
        # a fordított alak (Zsolt 35:12: 38,41 nem létezik, 38,10 létezik)
        m = K.e2_mintak([('Psa.38.41', ''), ('Psa.38.10', '')], self.NEH, ['Psa.41.10'])
        self.assertEqual(m[0]['letezo_tagok'], ['Psa.38.10'])
        # nem minta: mindkét töredék létezik; a == c; a cél nem létező vers
        self.assertEqual(K.e2_mintak([('Neh.4.8', ''), ('Neh.4.9', '')], self.NEH, []), [])
        self.assertEqual(K.e2_mintak([('Neh.4.4', ''), ('Neh.4.32', '')], self.NEH, []), [])
        self.assertEqual(K.e2_mintak([('Neh.4.9', ''), ('Neh.4.99', '')], self.NEH, []), [])

    def test_e2_hunkar_tartomany_tovabbi_versei_a_mintahoz_tartoznak(self):
        """Zsolt 27:4: HunKar 42:2-3, MEK 23,42 + 23,2 + 23,3."""
        lista = [('Psa.23.42', ''), ('Psa.23.2', ''), ('Psa.23.3', '')]
        m = K.e2_mintak(lista, self.NEH, ['Psa.42.2-Psa.42.3'])
        self.assertEqual(m[0]['tagok'], ['Psa.23.42', 'Psa.23.2', 'Psa.23.3'])
        self.assertEqual(m[0]['letezo_tagok'], ['Psa.23.2', 'Psa.23.3'])

    def test_e2_a_letezo_toredek_nem_emelodik_be(self):
        letezo = set(self.LETEZO) | self.NEH
        jav = [('Neh.1.5', 'Neh.9.32', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Neh.1.5', 'Neh.4.9', 'jelolt', 'MEK', 'csak_mek;mek_alak=a;tsk=nem'),
               ('Neh.1.5', 'Neh.4.32', 'jelolt', 'MEK', 'csak_mek;mek_alak=b;tsk=nem;hibas_hivatkozas=Neh.4.32'),
               ('Neh.1.5', 'Mat.5.32', 'jelolt', 'MEK', 'csak_mek;mek_alak=c;tsk=nem')]
        b = {(r['cel'], r['oldal']): r for r in K.jelolt_bontas(
            jav, letezo, lambda f, c: False, lambda f, c: False, set(), set())}
        self.assertEqual(b[('Neh.4.9', 'MEK')]['dontes'], K.D_E2)
        self.assertEqual(b[('Neh.4.32', 'MEK')]['dontes'], K.D_NEMLETEZO)
        self.assertEqual(b[('Mat.5.32', 'MEK')]['dontes'], K.D_BEEMEL)
        self.assertEqual(b[('Neh.9.32', 'HunKar')]['dontes'], K.D_HK_E2)
        self.assertIn('mek_fejezet_minta=Neh.4.9+Neh.4.32', b[('Neh.9.32', 'HunKar')]['jegyzet'])
        # HunKar-megfelelő nélkül: a töredék jelolt, a HunKar-sor nincs
        b2 = {(r['cel'], r['oldal']): r for r in K.jelolt_bontas(
            [j for j in jav if j[3] != 'HunKar'], letezo, lambda f, c: False, lambda f, c: False, set(), set())}
        self.assertEqual(b2[('Neh.4.9', 'MEK')]['dontes'], K.D_E2)

    def test_e2_a_dt_f181e_esetei(self):
        """Zsolt 35:12 (HunKar 41:10, MEK 38,41 + 38,10): a MEK-töredék nem elírás-gyanús pár, hanem E2-minta."""
        letezo = set(self.LETEZO) | self.NEH
        jav = [('Psa.35.12', 'Psa.41.10', 'jelolt', 'HunKar', 'eltero_lista;tsk=nem'),
               ('Psa.35.12', 'Psa.38.41', 'jelolt', 'MEK', 'csak_mek;mek_alak=a;tsk=nem;hibas_hivatkozas=Psa.38.41'),
               ('Psa.35.12', 'Psa.38.10', 'jelolt', 'MEK', 'csak_mek;mek_alak=b;tsk=nem')]
        b = {(r['cel'], r['oldal']): r for r in K.jelolt_bontas(
            jav, letezo, lambda f, c: False, lambda f, c: False, set(), set())}
        self.assertEqual(b[('Psa.38.10', 'MEK')]['dontes'], K.D_E2)
        self.assertEqual(b[('Psa.41.10', 'HunKar')]['dontes'], K.D_HK_E2)

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
        beemelt MEK-sor (`szabaly=F181`), vagy a HunKar-sor, amelynek a MEK-párja nem ellentmond (`szabaly=F181`); a
        kiesik sor HunKar-sor; a MEK-sor csak a szabállyal lehet nem jelölt."""
        for m in self.jav:
            if m[2] == 'megerositett':
                self.assertIn(m[3], ('HunKar+MEK', 'MEK', 'HunKar'))
                self.assertNotIn('hibas_hivatkozas', m[4])
                if m[3] in ('MEK', 'HunKar'):
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

    def test_e1_esetek_a_tablan(self):
        """DT-F181g: a három helyes HunKar-KH (és a Lev 23:17 -> Lev 2:12) megerősített, nem kiesik."""
        d = {(m[0], m[1]): m for m in self.jav}
        for f, c in (('Neh.1.5', 'Neh.9.32'), ('Jhn.8.12', 'Jhn.12.46'), ('Act.14.22', 'Act.13.43'),
                     ('Lev.23.17', 'Lev.2.12')):
            self.assertEqual(d[(f, c)][2], 'megerositett', (f, c))
            self.assertEqual(d[(f, c)][3], 'HunKar')
            self.assertRegex(d[(f, c)][4], r'mek_par_nem_letezik=|mek_fejezet_minta=')
            self.assertTrue(SZ.elfogad(f, c))

    def test_e2_esetek_a_tablan(self):
        """DT-F181h: a létező töredék (Neh 4:9, Ján 9:12, ApCsel 11:13) nem megerősített, a HunKar-sor igen; a
        DT-F181e két esete (Zsolt 35:12, Ézs 53:7) szintén."""
        d = {(m[0], m[1]): m for m in self.jav}
        for f, c in (('Neh.1.5', 'Neh.4.9'), ('Jhn.8.12', 'Jhn.9.12'), ('Act.14.22', 'Act.11.13'),
                     ('Psa.35.12', 'Psa.38.10'), ('Isa.53.7', 'Psa.38.10')):
            self.assertEqual(d[(f, c)][2], 'jelolt', (f, c))
            self.assertFalse(SZ.elfogad(f, c))
        for f, c in (('Psa.35.12', 'Psa.41.10'), ('Isa.53.7', 'Psa.39.10'), ('Psa.34.18', 'Psa.32.10'),
                     ('Psa.27.4', 'Psa.42.2-Psa.42.3')):
            self.assertEqual(d[(f, c)][2], 'megerositett', (f, c))
            self.assertIn('mek_fejezet_minta=', d[(f, c)][4])

    def test_e2_teljes_meres(self):
        """DT-F181h: az E2-hibaminta gépi mérése a nyers táblán (a számok a jelentésben: 10. szakasz)."""
        szoveg, adat = K.e2_meres(self.hk, K.mek_sorok_betolt(), K.karoli_versek())
        self.assertEqual((adat['minta'], adat['versek'], adat['hk_minta']), (26, 24, 7))
        self.assertEqual((adat['toredek'], adat['csak_mek']), (21, 9))
        self.assertEqual([k[1] for k in adat['volt_beemel']], ['1Sa.22.20', 'Act.11.13', 'Jhn.9.12', 'Neh.4.9'])
        self.assertEqual(adat['hk_nelkul'], [('1Ki.2.26', '1Sa.22.20')])

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
        mek = K.mek_sorok_betolt()
        hk_celok = collections.defaultdict(list)
        for f, c, _, _ in self.hk:
            hk_celok[f].append(c)
        e2 = {}
        for f in {m[0] for m in self.jav if m[2] == 'jelolt' and m[3] == 'MEK'}:
            e2[f] = {t for x in K.e2_mintak(mek.get(f, []), letezo, hk_celok[f]) for t in x['letezo_tagok']}
        for m in self.jav:
            if m[2] == 'jelolt' and m[3] == 'MEK':
                nincs = not K.cel_letezik(m[1], letezo) or m[0] not in letezo
                elir = m[0] in {x[0] for x in self.jav if x[2] == 'jelolt' and x[3] == 'HunKar'}
                self.assertTrue(nincs or m[0] in gy_mek or elir or m[1] in e2[m[0]], m)
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
