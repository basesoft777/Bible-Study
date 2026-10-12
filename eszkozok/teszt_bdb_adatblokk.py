#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_bdb_adatblokk.py -- F56 (BDB_ADATBLOKK) tesztek: a Strong-
normalizalas (K2), az adatblokk szerkezete es proveniencia-sorai (K1), a
fejezetszam-javitotabla algoritmusa es a H7223 teszteset (K3), a visszamenoleges
atvezetes szovegcsereje (K5).

    python eszkozok/teszt_bdb_adatblokk.py
"""

import os
import re
import sys
import tempfile
import unittest
from unittest import mock

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bdb_adatblokk as B  # noqa: E402

TS = '2026-10-06T00:00:00Z'


class StrongNormalizalas(unittest.TestCase):
    def test_alakok_egyeznek(self):
        for alak in ('H2617', 'H02617', '2617', 'h2617', ' H2617 '):
            self.assertEqual(B.strong_norm(alak), 'H2617')
            self.assertEqual(B.strong_szam(alak), 2617)
            self.assertEqual(B.strong_padded(alak), 'H2617')

    def test_kis_szam_es_homograf(self):
        self.assertEqual(B.strong_padded('H1'), 'H0001')
        self.assertEqual(B.strong_padded('1'), 'H0001')
        self.assertEqual(B.strong_padded('H90a'), 'H0090a')
        self.assertEqual(B.strong_szam('H0090a'), 90)

    def test_hibas(self):
        self.assertIsNone(B.strong_norm('G26'))
        self.assertIsNone(B.strong_norm('abc'))
        self.assertIsNone(B.strong_norm(''))

    def test_nincs_nema_nemtalalat(self):
        # K2: ismert Strong-szamok, amelyeknek van Karoli-parjuk, mindharom alakban
        for s in ('H2617', 'H5785', 'H8057'):
            for alak in (s, s.replace('H', 'H0'), s[1:]):
                self.assertTrue(B.karoli_alakok(B.strong_szam(alak)), '%s (%s)' % (s, alak))
                blokk = B.blokk_epit(alak, TS)
                self.assertNotIn('[NINCS KÁROLI-ALAK]', blokk, '%s (%s)' % (s, alak))
                self.assertIn('ADATBLOKK %s ' % s, blokk)


class Blokk(unittest.TestCase):
    def test_szakaszok_es_proveniencia(self):
        b = B.blokk_epit('H2617', TS)
        for jel in ('**1. ', '**2. ', '**3. ', '**4. ', '**5. ', '**6. '):
            self.assertIn(jel, b)
        # minden szakasz vegen proveniencia-sor
        self.assertEqual(len(re.findall(r'^\*proveniencia: scope=H2617 \| forras=.+ \| ts=%s\*$' % TS,
                                        b, re.M)), 6)

    def test_meretkorlat(self):
        for s in ('H2617', 'H3548', 'H7121', 'H0001', 'H9009', 'H1961'):
            self.assertLessEqual(len(B.blokk_epit(s, TS)), B.BLOKK_MAX, s)

    def test_nincs_karoli_alak(self):
        # a teljes OSZ-parosítás után nincs ismert üres Strong: a parok üres voltát szimuláljuk
        # (F80: a korábbi H0426-fixture a 6 könyves állapotra épült)
        with mock.patch.object(B, 'parok', return_value={}):
            b = B.blokk_epit('H0426', TS)
        self.assertIn('[NINCS KÁROLI-ALAK]', b)
        self.assertEqual(len(re.findall(r'^\*proveniencia:', b, re.M)), 6)

    def test_ures_szakaszok_jelzese(self):
        b = B.blokk_epit('H0256', TS)       # nincs LXX-hid, nincs Karoli-par
        self.assertIn('**3. LXX-megfelelő**\n—', b)

    def test_pelda_idezet_szo_szerinti(self):
        # a kiemelt szo a hu_sorszam-adik token, az idezet a Karoli-versbol
        b = B.blokk_epit('H2617', TS)
        # F80: a példaversek a teljes ÓSZ-párosításból jönnek; az első idézett vers bármi lehet
        m = re.search(r'- \*\*[^*]+\*\*: (\S+ \d+:\d+) „(.+?)”', b)
        self.assertIsNotNone(m)
        szoveg = m.group(2).replace('**', '').strip('.').replace('...', '')
        self.assertIn(szoveg.strip(), B.karoli_vers()[m.group(1)])

    def test_hibas_strong(self):
        with self.assertRaises(ValueError):
            B.blokk_epit('G26', TS)


class LxxSzures(unittest.TestCase):
    """F56 M3b: a nyelvtani gorog talalatok kimaradnak, ha a heber szo nem nyelvtani."""

    def _lxx_sor(self, strong):
        b = B.blokk_epit(strong, TS)
        return re.search(r'\*\*3\. LXX-megfelelő\*\*\n([^\n]+)(?:\n(\[kihagyva[^\n]*))?', b)

    def test_grammatikai_halmaz(self):
        g = B.grammatikai()
        for s in ('G3588', 'G1519', 'H0413', 'H3588', 'H9009'):
            self.assertIn(s, g)
        self.assertNotIn('H0894', g)

    def test_nevelo_kimarad(self):
        # H3824 (szív): a nyers hídban G3588 ὁ x10 a 2. helyen állt; most nincs a listán
        m = self._lxx_sor('H3824')
        self.assertRegex(m.group(1), r'^G2588 \S+ ×200,')
        self.assertNotIn('G3588', m.group(1))
        self.assertRegex(m.group(2), r'G3588 \S+ ×10')      # a kihagyás jelölt, nem néma
        self.assertIn('G1271', m.group(1))             # a 3. hely a következő nem nyelvtani

    def test_eloljaro_kimarad(self):
        m = self._lxx_sor('H0894')
        self.assertNotIn('G1519', m.group(1))
        self.assertRegex(m.group(2), r'G1519 \S+ ×18')

    def test_nincs_nyelvtani_a_listan(self):
        # a héber szó nem nyelvtani -> egyetlen mintaszócikk listáján sincs nyelvtani görög
        # (a H3282 innen kikerült: DT-F68a, 2026.10.08 óta a nyelvtani listán van, ezért a görög nyelvtani találatok nála megmaradnak)
        gr = B.grammatikai()
        for s in ('H0894', 'H3824', 'H4294', 'H7272', 'H1366', 'H0410', 'H7097', 'H2617', 'H1481'):
            m = self._lxx_sor(s)
            for g in re.findall(r'G(\d+) ', m.group(1)):
                self.assertNotIn('G%04d' % int(g), gr, '%s: G%s' % (s, g))

    def test_nyelvtani_heber_marad(self):
        # a héber szó maga is nyelvtani (H3588 ki, H0413 el) -> a görög nyelvtani találatok maradnak
        gr = B.grammatikai()
        for s in ('H3588', 'H0413'):
            self.assertIn('H%04d' % B.strong_szam(s), gr)
            mind = sorted(B.lxx_hid().get(B.strong_szam(s), []), key=lambda x: (-x[1], x[0]))[:3]
            m = self._lxx_sor(s)
            self.assertIsNone(m.group(2), s)            # nincs kihagyás
            for g, db in mind:
                self.assertIn('G%d ' % int(g[1:]), m.group(1), s)

    def test_nem_nyelvtani_nem_csonkul(self):
        # H4390: nincs nyelvtani találat -> változatlan 3 elem
        m = self._lxx_sor('H4390')
        self.assertEqual(len(re.findall(r'G\d+ ', m.group(1))), 3)
        self.assertIsNone(m.group(2))

    def test_proveniencia_nevezi_a_listat(self):
        b = B.blokk_epit('H3824', TS)
        self.assertIn('adat/grammatikai_strongok.tsv', b)


class Javitas(unittest.TestCase):
    def test_jeloltek_elgepeles(self):
        self.assertIn(7, B.fejezet_jeloltek('17', 12))
        self.assertIn(1, B.fejezet_jeloltek('17', 12))
        self.assertNotIn(17, B.fejezet_jeloltek('17', 12))
        self.assertNotIn(0, B.fejezet_jeloltek('10', 12))

    def test_h7223(self):
        # K3: Eccl 17:10 -> Eccl 7:10 (H7223, `javitva`)
        sorok = B.javitas_sorok('H7223', B.bdb_szocikkek()['H7223'], TS)
        s = [x for x in sorok if x['forras_hivatkozas'] == 'Eccl 17:10']
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0]['allapot'], 'javitva')
        self.assertEqual(s[0]['javitott_hivatkozas'], 'Préd 7:10')
        self.assertTrue(s[0]['indok'])
        self.assertIn('scope=H7223', s[0]['proveniencia'])

    def test_nem_letezo_fejezet_nem_talalgat(self):
        # ahol nincs jelolt, vagy tobb van, a sor jelolt_marad, javitott hivatkozas nelkul
        sorok = B.javitas_sorok('H0834', B.bdb_szocikkek()['H0834'], TS)
        for s in sorok:
            if s['allapot'] == 'jelolt_marad':
                self.assertEqual(s['javitott_hivatkozas'], '')

    def test_tabla_elemei(self):
        t = B.javitotabla_olvas()
        self.assertTrue(t)
        for sp, sorok in t.items():
            for s in sorok:
                self.assertIn(s['allapot'], ('javitva', 'jelolt_marad'))
                self.assertTrue(s['indok'] and s['proveniencia'])
                self.assertEqual(bool(s['javitott_hivatkozas']), s['allapot'] == 'javitva')

    def test_konyvnev_gyanu_jelolt_marad(self):
        # DT-F56a: ha a hibas fejezet:vers masik konyvben is letezik es ott a Strong-szam szerepel,
        # a sor jelolt_marad (akkor is, ha egyetlen jelolt van), FIGYELEM-jelzessel
        sorok = B.javitas_sorok('H0834', B.bdb_szocikkek()['H0834'], TS)
        s = [x for x in sorok if x['forras_hivatkozas'] == 'Ruth 8:14']
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0]['allapot'], 'jelolt_marad')
        self.assertEqual(s[0]['javitott_hivatkozas'], '')
        self.assertIn('FIGYELEM', s[0]['indok'])
        self.assertIn('Ruth 4:14', s[0]['indok'])      # az egyetlen jelolt a indokban latszik

    def test_javitva_sorban_nincs_figyelem(self):
        t = B.javitotabla_olvas()
        db = 0
        for sorok in t.values():
            for s in sorok:
                if s['allapot'] == 'javitva':
                    db += 1
                    self.assertNotIn('FIGYELEM', s['indok'])
        self.assertEqual(db, 7)   # DT-F56c: a H4480 es a H9009 sora jelolt_marad

    def test_tabla_egyezik_az_algoritmussal(self):
        # a --javitas-epit ujrafuttatasa ugyanazt adja (allapot es javitott hivatkozas)
        t = B.javitotabla_olvas()
        for sp, szoveg in B.bdb_szocikkek().items():
            for s in B.javitas_sorok(sp, szoveg, TS):
                tabla = [x for x in t.get(sp, []) if x['forras_hivatkozas'] == s['forras_hivatkozas']]
                self.assertEqual(len(tabla), 1, '%s %s' % (sp, s['forras_hivatkozas']))
                self.assertEqual((tabla[0]['allapot'], tabla[0]['javitott_hivatkozas']),
                                 (s['allapot'], s['javitott_hivatkozas']))

    def test_elotag_par(self):
        # DT-F56c (a): az onallo es az elotag-alak Strongja egy szo (H4480 min = H9006 mi-)
        p = B.elotag_parok()
        self.assertEqual(p[4480], {4480, 9006})
        self.assertEqual(p[9006], {4480, 9006})

    def test_elotag_par_konyvnev_gyanu(self):
        # a grammatikai- es gyakorisag-szabaly kikapcsolva is jelolt_marad: az 5Moz 32:47 a H9006-tal
        # szerepel (a TAHOT-ban), a kozvetlen H4480-kereses ezt nem latja
        with mock.patch.object(B, 'grammatikai', lambda: set()), mock.patch.object(B, 'GYAKORI_VERS_KUSZOB', 10 ** 9):
            sorok = B.javitas_sorok('H4480', B.bdb_szocikkek()['H4480'], TS)
        s = [x for x in sorok if x['forras_hivatkozas'] == '1Ki 32:47']
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0]['allapot'], 'jelolt_marad')
        self.assertIn('5Móz 32:47', s[0]['indok'])

    def test_nyelvtani_strong_nem_javitva(self):
        # DT-F56c (b): nyelvtani listan szereplo Strongra egyetlen jelolt sem javitas
        for sp in ('H4480', 'H9009'):
            self.assertIn(sp, B.grammatikai())
            for s in B.javitas_sorok(sp, B.bdb_szocikkek()[sp], TS):
                self.assertEqual(s['allapot'], 'jelolt_marad', (sp, s['forras_hivatkozas']))
        s = [x for x in B.javitas_sorok('H9009', B.bdb_szocikkek()['H9009'], TS) if x['forras_hivatkozas'] == '1Ki 66:6']
        self.assertEqual(len(s), 1)
        self.assertIn('nyelvtani listan', s[0]['indok'])

    def test_gyakori_strong_nem_javitva(self):
        # DT-F56c (b): kuszob felett (nem nyelvtani) sem javitva; a kuszob alatt igen (H7223)
        with mock.patch.object(B, 'GYAKORI_VERS_KUSZOB', 100):
            sorok = B.javitas_sorok('H7223', B.bdb_szocikkek()['H7223'], TS)
        s = [x for x in sorok if x['forras_hivatkozas'] == 'Eccl 17:10']
        self.assertEqual(s[0]['allapot'], 'jelolt_marad')
        self.assertIn('nem bizonyit', s[0]['indok'])

    def test_blokk_javitas_szakasz(self):
        b = B.blokk_epit('H7223', TS)
        self.assertIn('a forrásban `Eccl 17:10` → helyesen `Préd 7:10`', b)


class Atvezetes(unittest.TestCase):
    SOR = [{'forras_hivatkozas': 'Eccl 17:10', 'javitott_hivatkozas': 'Préd 7:10'}]

    def test_csere(self):
        uj, cs = B.atvezet_szoveg('mint Préd 17:10; Zsolt 79:8 és tovább', self.SOR)
        self.assertEqual(uj, 'mint Préd 7:10 [BDB: Préd 17:10]; Zsolt 79:8 és tovább')
        self.assertEqual(cs, [('Préd 17:10', 'Préd 7:10', 1)])

    def test_csak_a_hivatkozas(self):
        # nem erinti a hosszabb szamot es az mar atvezetett alakot
        uj, cs = B.atvezet_szoveg('Préd 17:100 es Préd 117:10', self.SOR)
        self.assertEqual(uj, 'Préd 17:100 es Préd 117:10')
        self.assertEqual(cs, [])

    def test_visszaallitas(self):
        # DT-F56c: a mar atvezetett, de azota nem `javitva` alak visszaall; a megtartott javitva marad
        uj, cs = B.atvezet_vissza('1Kir 22:47 [BDB: 1Kir 32:47] es Préd 7:10 [BDB: Préd 17:10]', self.SOR)
        self.assertEqual(uj, '1Kir 32:47 es Préd 7:10 [BDB: Préd 17:10]')
        self.assertEqual(cs, [('1Kir 22:47', '1Kir 32:47', 1)])

    def test_visszaallitas_idempotens(self):
        egyszer, _ = B.atvezet_vissza('1Kir 22:47 [BDB: 1Kir 32:47]', [])
        ketszer, cs = B.atvezet_vissza(egyszer, [])
        self.assertEqual((egyszer, cs), ('1Kir 32:47', []))
        self.assertEqual(ketszer, egyszer)

    def test_forditasokban_nincs_nem_javitva_jeloles(self):
        # a forditasok.tsv-ben csak `javitva` sorra van [BDB: X] jeloles
        for sor in open(B.FORDITASOK_UT, encoding='utf-8').read().split(chr(10)):
            m = sor.split(chr(9))
            if len(m) == 12 and m[0] == 'BDB' and '[BDB: ' in m[6]:
                javitva = [x for x in B.javitotabla_olvas().get(B.strong_padded(m[1]), []) if x['allapot'] == 'javitva']
                uj, cs = B.atvezet_vissza(m[6], javitva)
                self.assertEqual(cs, [], m[1])

    def test_ketszeri_futtatas_idempotens(self):
        egyszer, _ = B.atvezet_szoveg('Préd 17:10', self.SOR)
        ketszer, cs = B.atvezet_szoveg(egyszer, self.SOR)
        self.assertEqual(egyszer, ketszer)
        self.assertEqual(cs, [])


TAB = chr(9)
NL = chr(10)


class KaroliTabla(unittest.TestCase):
    """F80 (BDB_KAROLI_POTLAS): adat/bdb_karoli.tsv -- minden kesz BDB-szocikk Karoli-adata,
    visszakereshetoen a parok_*.tsv forrassorra; az adat/forditasok.tsv nem valtozik."""

    @classmethod
    def setUpClass(cls):
        cls.sorok = B.karoli_tabla_olvas()
        cls.szocikkek = [s for s in cls.sorok if s['tipus'] == 'szocikk']

    def test_minden_kesz_szocikk_szerepel_proveniencival(self):
        kesz = B.kesz_bdb_strongok()
        self.assertGreaterEqual(len(kesz), 674)
        self.assertEqual([s['strong'] for s in self.szocikkek], kesz)
        for s in self.szocikkek:
            self.assertRegex(s['proveniencia'], r'^scope=H\d{4} \| forras=.+ \| ts=\S+$')
            if s['karoli_alak'] == B.NINCS_KAROLI_ALAK:      # kifejezett ures jelzes, nem kitoltes
                self.assertEqual((s['magas'], s['alacsony']), ('0', '0'))

    def test_minden_sor_proveniencia_nem_ures_es_alak_egyezik_a_szocikkevel(self):
        # SEMA 2.25: minden sorban kotelezo; az alak-sor proveniencia-ja a szocikk-soreval szo szerint azonos
        szoc = {s['strong']: s['proveniencia'] for s in self.szocikkek}
        for s in self.sorok:
            self.assertTrue(s['proveniencia'].strip(), (s['strong'], s['tipus'], s['karoli_alak']))
            self.assertEqual(s['proveniencia'], szoc[s['strong']], (s['strong'], s['tipus'], s['karoli_alak']))

    def test_pelda_versek_kanonikus_konyvsorrendben(self):
        # a pelda_versek a Konyv_normalizalo_tabla.tsv sorrendjeben (nem fajlnev/ASCII szerint)
        sorrend = B.kanonikus_konyvsorrend()
        ellenorzott = 0
        for s in self.sorok:
            if s['tipus'] != 'alak':
                continue
            kv = [v.rsplit(' ', 1)[0] for v in s['pelda_versek'].split(';') if v]
            idx = [sorrend[B.PAROK_KONYV_ALIAS.get(k, k)] for k in kv]
            self.assertEqual(idx, sorted(idx), (s['strong'], s['karoli_alak'], s['pelda_versek']))
            ellenorzott += len(kv)
        self.assertGreater(ellenorzott, 90000)
        # a H2617 'irgalmassága' elso peldaja nem lehet 1Kron (ASCII-sorrend hibaja volt)
        irg = [s for s in self.sorok if s['strong'] == 'H2617' and s['tipus'] == 'alak'
               and s['karoli_alak'] == 'irgalmassága']
        self.assertTrue(irg)
        self.assertFalse(irg[0]['pelda_versek'].startswith('1Krón'), irg[0]['pelda_versek'])

    def test_parok_konyvek_tabla_szerinti_sorrend_es_hiba(self):
        kv = [k for k, _ut in B.parok_konyvek()]
        db = len([f for f in os.listdir(B.PAROK_MAPPA) if re.match(r'^parok_.+[.]tsv$', f)])
        self.assertEqual(len(kv), db)
        self.assertEqual(kv[:3], ['1Moz', '2Moz', '3Moz'])
        self.assertLess(kv.index('Jozs'), kv.index('Bir'))
        self.assertLess(kv.index('Bir'), kv.index('1Sam'))
        self.assertLess(kv.index('Sir'), kv.index('Ez'))          # JSir a tablaban az Ez elott
        # ismeretlen konyv a parok-fajlban: nincs 99-es tartalek, hibaval all meg
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, 'parok_Xx.tsv'), 'w', encoding='utf-8', newline=NL) as fh:
                fh.write(TAB.join(['vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong', 'bizonyossag', 'forras']) + NL)
                fh.write(TAB.join(['Xx 1:1', '1', 'szo', '1', 'x', 'H0001', 'alacsony', 'S']) + NL)
            with mock.patch.object(B, 'PAROK_MAPPA', td):
                with self.assertRaises(ValueError):
                    B.parok_konyvek()

    def test_osszegek_egyeznek_a_forrassal(self):
        for strong in ('H2617', 'H5785', 'H8057'):
            sz = B.strong_szam(strong)
            alakok = [s for s in self.sorok if s['strong'] == strong and s['tipus'] == 'alak']
            par = B.parok()[sz]
            self.assertEqual(sum(int(a['magas']) + int(a['alacsony']) for a in alakok), len(par), strong)
            szoc = [s for s in self.szocikkek if s['strong'] == strong][0]
            self.assertEqual(int(szoc['par_db']), len(par), strong)

    def test_visszakereshetoseg_forrassorra(self):
        # legalabb 3 ismert Strong-szam (van Karoli-parja): minden pelda-hivatkozas (vers + Strong +
        # alak) a parok_*.tsv egy sorara visszakeresheto, fajlbeli sorszam nelkul
        for strong in ('H2617', 'H5785', 'H8057'):
            alakok = [s for s in self.sorok if s['strong'] == strong and s['tipus'] == 'alak']
            self.assertTrue(alakok, strong)
            ellenorzott = 0
            for a in alakok:
                for vers in [v for v in a['pelda_versek'].split(';') if v]:
                    forras = B.karoli_pelda_forras(strong, a['karoli_alak'], vers)
                    self.assertTrue(forras, '%s %s %s' % (strong, a['karoli_alak'], vers))
                    ellenorzott += 1
            self.assertGreater(ellenorzott, 3, strong)

    def test_nyers_parok_fajl_is_megerosit(self):
        # fuggetlen olvasas: a nyers parok_1Moz.tsv-ben a H2617 alak-sora tenyleg ott van
        ut = os.path.join(B.PAROK_MAPPA, 'parok_1Moz.tsv')
        talalt = set()
        for m in B.tsv_sorok(ut):
            if m[5] == 'H2617':
                talalt.add((m[0], m[2].lower()))
        peldak = [(v, a['karoli_alak']) for a in self.sorok
                  if a['strong'] == 'H2617' and a['tipus'] == 'alak'
                  for v in a['pelda_versek'].split(';') if v.startswith('1Móz ')]
        self.assertTrue(peldak)
        for v, alak in peldak:
            self.assertIn((v, alak), talalt)

    def test_forditasok_valtozatlan(self):
        # K3: a potlas nem ir az adat/forditasok.tsv-be -- a tabla-epites elott es utan
        # ugyanaz a fajl (bajtra), a 'teljes' BDB-sorok szama es a forditas_hu mezok is
        import hashlib
        import tempfile

        def hash_():
            return hashlib.sha256(open(B.FORDITASOK_UT, 'rb').read()).hexdigest()
        elotte = hash_()
        with tempfile.TemporaryDirectory() as td:
            ki = os.path.join(td, 'bdb_karoli.tsv')
            with mock.patch.object(B, 'KAROLI_TABLA_UT', ki):
                sorok = B.karoli_tabla_sorok(['H2617', 'H5785', 'H8057'], TS)
                B.karoli_tabla_ir(sorok, TS, ut=ki)
            self.assertTrue(os.path.exists(ki))
            # a tabla-epites CLI-je is csak a megadott celba ir
            ki2 = os.path.join(td, 'teljes.tsv')
            with mock.patch.object(B, 'KAROLI_TABLA_UT', ki2):
                self.assertEqual(B.main(['--karoli-epit', '--ts', TS]), 0)
            self.assertTrue(os.path.exists(ki2))
        self.assertEqual(hash_(), elotte)

    def test_ujraepites_idempotens(self):
        a = B.karoli_tabla_sorok(['H2617', 'H8057'], TS)
        b = B.karoli_tabla_sorok(['H2617', 'H8057'], TS)
        self.assertEqual(a, b)
        self.assertTrue(all('\t' not in x and '\n' not in x for s in a for x in s))

    def test_ures_forras_kifejezett_jelzes(self):
        with mock.patch.object(B, 'parok', return_value={}):
            sorok = B.karoli_tabla_sorok(['H0426'], TS)
        self.assertEqual(len(sorok), 1)
        self.assertEqual(sorok[0][1:5], ['szocikk', B.NINCS_KAROLI_ALAK, '0', '0'])
        self.assertIn('ts=' + TS, sorok[0][-1])


if __name__ == '__main__':
    unittest.main()
