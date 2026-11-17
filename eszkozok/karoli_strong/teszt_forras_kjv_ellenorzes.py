#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175K — a forrásoldali KJV-ellenőrzés (forras_kjv_ellenorzes.py) tesztjei, KITALÁLT mini-adaton
(hálózat nélkül; a kimenet ideiglenes könyvtárba megy).

A mini-adat: 1Móz 1:1–1:5 (TAHOT), Sir 1:1 (a Jeremiás siralmai a TAHOT-ban `Sir`), Mt 1:1–1:4 és
a Károli-pár nélküli Mt 1:3 (TAGNT), a KJV-ben Gen.1.7 és Mat.1.3 árva vers (a KJV-fájl STEPBible-kódokat használ).

Futtatás: python eszkozok/karoli_strong/teszt_forras_kjv_ellenorzes.py
"""

import argparse
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
import forras_kjv_ellenorzes as F  # noqa: E402


def _ir(ut, sorok):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for s in sorok:
            f.write(s + '\n')


def _olvas(ut, **kw):
    with open(ut, encoding='utf-8', **kw) as f:
        return f.read()


def _t(*mezok):
    return '\t'.join(mezok)


def mini(gyoker):
    kon = os.path.join(gyoker, 'konkordancia')
    csomag = os.path.join(gyoker, 'csomag')
    _ir(os.path.join(kon, 'Konyv_normalizalo_tabla.tsv'), [
        _t('STEPBible-rövidítés', 'Magyar rövidítés', 'Teljes magyar könyvnév', 'Forrás-alakok'),
        _t('Gen', '1Móz', 'Mózes első könyve', ''), _t('Lam', 'JSir', 'Jeremiás siralmai', ''),
        _t('Mat', 'Mt', 'Máté evangéliuma', '')])
    h7 = ['Igehely', 'Strong-szám', 'Ragozott alak', 'Kiejtés', 'Szótő', 'Rövid jelentés', 'Angol tükörfordítás']

    def ho(ig, st, szo='x', jel='j'):
        return _t(ig, st, 'a', 'k', szo, jel, 'e')
    _ir(os.path.join(kon, 'TAHOT_kivonat.tsv'), [_t(*h7)] + [
        ho('1Móz 1:1', 'H9003'), ho('1Móz 1:1', 'H7225'), ho('1Móz 1:1', 'H1254'), ho('1Móz 1:1', 'H0430'),
        ho('1Móz 1:1', 'H0853'),
        ho('1Móz 1:2', 'H1980'), ho('1Móz 1:2', 'H0776'),
        ho('1Móz 1:3', 'H0559'), ho('1Móz 1:3', 'H0216'),
        ho('1Móz 1:4', 'H0922'), ho('1Móz 1:5', 'H0123'),
        ho('Sir 1:1', 'H0349')])

    def go(ig, st, kiad):
        return _t(ig, st, 'a', 'k', 'x', 'j', 'e', kiad)
    _ir(os.path.join(kon, 'TAGNT_kivonat.tsv'), [_t(*(h7 + ['Kritikai kiadás']))] + [
        go('Mt 1:1', 'G0976', 'NA28+TR+Byz'), go('Mt 1:1', 'G1078', 'TR'), go('Mt 1:1', 'G2424', 'NA28+Byz'),
        go('Mt 1:2', 'G0011', 'NA28+TR'),
        go('Mt 1:3', 'G1080', 'NA28+TR'),
        go('Mt 1:4', 'G0001', 'NA28+TR')])
    kj = ['# komment', _t('Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó', 'Morfológiai kód')]
    for ig, st, szo in [('Gen.1.1', 'H7225', 'beginning'), ('Gen.1.1', 'H430', 'God'), ('Gen.1.1', 'H1254', 'created'),
                        ('Gen.1.1', 'H9999', 'igealak'),
                        ('Gen.1.2', 'H3212', 'went'), ('Gen.1.2', 'H776', 'earth'), ('Gen.1.2', 'H8414', 'void'),
                        ('Gen.1.3', 'H559', 'said'), ('Gen.1.7', 'H5921', 'upon'),
                        ('Lam.1.1', 'H349', 'how'),
                        ('Mat.1.1', 'G976', 'book'), ('Mat.1.1', 'G1078', 'generation'),
                        ('Mat.1.1', 'G2424', 'Jesus'), ('Mat.1.1', 'G5547', 'Christ'),
                        ('Mat.1.2', 'G11', 'Abraham'), ('Mat.1.3', 'G1080', 'begat')]:
        kj.append(_t(ig, '1', st, szo, ''))
    _ir(os.path.join(kon, 'KJV_Strongs_teljes.tsv'), kj)
    _ir(os.path.join(kon, 'Karoli_versmegfeleltetes.tsv'), [
        '# komment', _t('igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly', 'forras', 'megjegyzes'),
        _t('1Móz 1:1', '1:1', '', 'KJV', 's', ''), _t('1Móz 1:2', '1:2', '', 'KJV', 's', ''),
        _t('1Móz 1:3', '1:3', '', 'KJV', 's', ''), _t('1Móz 1:4', '', '1:4', 'MT', 's', ''),
        _t('Sir 1:1', '1:1', '', 'KJV', 's', '')])
    _ir(os.path.join(csomag, 'versek.tsv'), [
        '# GENERÁLT', _t('osis', 'szoveg_1908')] + [_t(o, 'x') for o in [
            'Gen.1.1', 'Gen.1.2', 'Gen.1.3', 'Gen.1.4', 'Gen.1.5', 'Lam.1.1', 'Matt.1.1', 'Matt.1.2', 'Matt.1.4']])
    pf = _t('osis', 'token', 'alak_1908', 'eredeti_token', 'strong', 'kapcsolat', 'allapot', 'nem_tr')
    _ir(os.path.join(csomag, 'parok', '01_Gen.tsv'), ['# GENERÁLT', pf] + [
        _t('Gen.1.1', '1', 'a', '1', 'H9003', 'morfema', 'javaslat', ''),
        _t('Gen.1.1', '1', 'a', '2', 'H7225', 'szo', 'javaslat', ''),
        _t('Gen.1.1', '2', 'b', '3', 'H1254', 'szo', 'javaslat', ''),
        _t('Gen.1.1', '3', 'c', '4', 'H0430', 'szo', 'javaslat', '')])
    sf = _t('osis', 'oldal', 'token', 'alak_1908', 'allapot', 'partner_token', 'strong')
    er = {'Gen.1.1': ['H9003', 'H7225', 'H1254', 'H0430', 'H0853'], 'Gen.1.2': ['H1980', 'H0776'],
          'Gen.1.3': ['H0559', 'H0216'], 'Gen.1.4': ['H0922'], 'Gen.1.5': ['H0123'], 'Lam.1.1': ['H0349'],
          'Matt.1.1': ['G0976', 'G1078', 'G2424'], 'Matt.1.2': ['G0011', 'G1080'], 'Matt.1.4': ['G0001']}
    rows = ['# GENERÁLT', sf]
    for osis, ss in er.items():
        for i, s in enumerate(ss, 1):
            rows.append(_t(osis, 'er', str(i), '', 'parositva', '1', s))
    _ir(os.path.join(csomag, 'szavak', '01_Gen.tsv'), rows)
    _ir(os.path.join(gyoker, 'gramm.tsv'), ['# k', _t('strong', 'rovid_jelentes', 'kategoria', 'kizaras_oka'),
                                             _t('H0853', 'obj', 'partikula', 'x')])
    return kon, csomag


class Teszt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix='f175k_teszt_')
        cls.kon, cls.csomag = mini(cls.tmp)
        cls.ki = os.path.join(cls.tmp, 'ki')
        cls.a = argparse.Namespace(
            konkordancia=cls.kon, csomag=cls.csomag, grammatikai=os.path.join(cls.tmp, 'gramm.tsv'), kimenet=cls.ki,
            verstabla=os.path.join(cls.tmp, 'verstabla.tsv'), min_vers=1, min_arany=0.5, top=50, min_kjv=2,
            atfedes_kuszob=0.5)
        cls.ms, cls.dg, cls.gy, cls.al = F.futtat(cls.a, head='teszt')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def dg_ertek(self, kulcs):
        return dict(self.dg)[kulcs]

    def mutato(self, valtozat, tip='osszes', cs='OSSZES'):
        for nev, t, c, m in self.ms:
            if nev == valtozat and t == tip and c == cs:
                return m
        self.fail('nincs sor: %s %s %s' % (valtozat, tip, cs))

    # --- kis függvények
    def test_strong_szuro(self):
        self.assertEqual(F.strong_norm('H430'), 'H0430')
        self.assertEqual(F.strong_norm('G976'), 'G0976')
        self.assertIsNone(F.strong_norm('1234'))
        self.assertTrue(F.morfema('H9001') and F.morfema('H9049'))
        self.assertFalse(F.morfema('H9050') or F.morfema('H0430') or F.morfema('G9001'))
        self.assertTrue(F.igealak_kod('H8675') and F.igealak_kod('G5625'))
        self.assertFalse(F.igealak_kod('H8674') or F.igealak_kod('G5624'))

    def test_kanon(self):
        k = F.kanon_terkep()
        self.assertEqual(k['H3212'], k['H1980'])
        self.assertEqual(k['H1980'], 'H1980')
        self.assertNotIn('H0430', k)

    def test_nincs_csv_modul(self):
        self.assertNotIn('import csv', _olvas(F.__file__))

    # --- egységek és nem illeszthető versek
    def test_egysegek_es_okok(self):
        self.assertEqual(self.dg_ertek('karoli_versek_a_csomagban'), 9)
        self.assertEqual(self.dg_ertek('osszehasonlitott_egysegek'), 6)
        self.assertEqual(self.dg_ertek('nem_illesztheto:nincs_kjv_megfeleles'), 1)     # 1Móz 1:4
        self.assertEqual(self.dg_ertek('nem_illesztheto:nincs_versmegf_sor'), 1)       # 1Móz 1:5
        self.assertEqual(self.dg_ertek('nem_illesztheto:kjv_vers_hianyzik'), 1)        # Mt 1:4
        sorok = [l.split('\t') for l in _olvas(os.path.join(self.ki, 'nem_illesztheto_versek.tsv')).split('\n')
                 if l and not l.startswith('#')][1:]
        self.assertIn(['1Móz 1:4', 'karoli', 'nincs_kjv_megfeleles'], sorok)
        self.assertIn(['Mt 1:4', 'karoli', 'kjv_vers_hianyzik'], sorok)

    def test_arva_kjv_vers_kapcsolas(self):
        # Gen.1.7 és Matt.1.3 árva: az előző hivatkozott KJV-vers egységéhez tartoznak
        self.assertEqual(self.dg_ertek('kjv_arva_versek_egyseghez_kapcsolva'), 2)
        self.assertEqual(self.dg_ertek('egyseg_arva_kjv_verssel_kiegeszitve'), 2)

    def test_forras_arva_kapcsolas_es_csomag_egyezes(self):
        # az árva TAGNT Mt 1:3 az Mt 1:2-hez kapcsolódik; a csomag `er` oldala ugyanezt tartalmazza
        self.assertEqual(self.dg_ertek('forras_vers_karoli_pár_nélkül_elozo_hez_kapcsolva'), 1)
        self.assertEqual(self.dg_ertek('csomag_er_oldal_elter_a_kivonattol_vers'), 0)
        self.assertEqual(self.dg_ertek('csomag_er_oldal_egyezik_a_kivonattal_vers'), 9)

    # --- mérőszámok (kézzel kiszámolt)
    def test_fo_valtozat(self):
        m = self.mutato('forras_vs_kjv')
        # Gen1:1 K⊆T · Gen1:2 (konvenció után H8414 csak KJV) · Gen1:3 (H5921 az árva versből) ·
        # Lam1:1 egyezik · Mt1:1 (G5547 csak KJV) · Mt1:2 egyezik (az árva Mt 1:3 mindkét oldalon kapcsolva)
        self.assertEqual(m['egyseg_db'], 6)
        self.assertEqual(m['egyezo_db'], 2)
        self.assertEqual(m['kjv_reszhalmaza_db'], 3)
        self.assertEqual(m['kjv_strong_db'], 3 + 3 + 2 + 1 + 4 + 2)
        self.assertEqual(m['kozos_strong_db'], 3 + 2 + 1 + 1 + 3 + 2)
        self.assertEqual(m['forras_strong_db'], 4 + 2 + 2 + 1 + 3 + 2)

    def test_nyers_valtozat_nem_normal(self):
        # konvenció nélkül a H1980 (forrás) és a H3212 (KJV) különbözik: a Gen1:2 közös Strongja csak H0776
        f, n = self.mutato('forras_vs_kjv'), self.mutato('forras_vs_kjv_nyers')
        self.assertEqual(f['kozos_strong_db'] - n['kozos_strong_db'], 1)

    def test_tartalmi_valtozat_grammatikai_nelkul(self):
        # a H0853 (grammatikai) csak a forrásban áll: a tartalmi változatból kimarad
        f, t = self.mutato('forras_vs_kjv'), self.mutato('forras_vs_kjv_tartalmi')
        self.assertEqual(f['forras_strong_db'] - t['forras_strong_db'], 1)
        self.assertEqual(f['kjv_strong_db'], t['kjv_strong_db'])

    def test_tr_valtozat(self):
        # a Mt 1:1 G2424 tokene nem TR-es: a TR-változatban kimarad a forrásból, a közös Strongok száma csökken
        f, t = self.mutato('forras_vs_kjv'), self.mutato('forras_TR_vs_kjv')
        self.assertEqual(f['kozos_strong_db'] - t['kozos_strong_db'], 1)

    def test_csomag_parok_valtozat(self):
        # a csomag pároknál álló Strongjai: csak a Gen 1:1 (H7225, H1254, H0430); a többi vers üres halmazú
        m = self.mutato('csomag_parok_vs_kjv', 'konyv', 'Gen')
        self.assertEqual(m['egyseg_db'], 3)
        self.assertEqual(m['forras_strong_db'], 3)
        self.assertEqual(m['kozos_strong_db'], 3)

    def test_testamentum_es_csoport_osszesites(self):
        self.assertEqual(self.mutato('forras_vs_kjv', 'testamentum', 'OSZ')['egyseg_db'], 4)
        self.assertEqual(self.mutato('forras_vs_kjv', 'testamentum', 'USZ')['egyseg_db'], 2)
        self.assertEqual(self.mutato('forras_vs_kjv', 'konyvcsoport', 'USZ_evangelium')['egyseg_db'], 2)
        self.assertEqual(self.mutato('forras_vs_kjv', 'konyv', 'Lam')['egyezo_db'], 1)   # a `Sir` alias működik

    # --- gyanúslista
    def test_gyanus_csak_kjv(self):
        sorok = [x for x in self.gy if x[0] == 'csak_kjv']
        strongok = {x[2]: x for x in sorok}
        self.assertIn('H8414', strongok)       # a Gen 1:2 KJV-ben van, a forrásban nincs
        self.assertIn('G5547', strongok)
        self.assertEqual(strongok['H8414'][14], 'igen')
        self.assertNotIn('H3212', strongok)    # a konvenció miatt H1980-ra képezve, mindkét oldalon megvan

    def test_csak_forras_grammatikai_jelolve(self):
        x = [r for r in self.gy if r[0] == 'csak_forras' and r[1] == 'H0853']
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0][8], 'igen')      # grammatikai
        self.assertEqual(x[0][14], 'nem')      # nem gyanús

    def test_csere_par(self):
        # a Gen 1:3: forrás H0216 ↔ KJV H5921 (tartalmi halmazok, egy-egy csak-oldali elem)
        csere = {(r[1], r[2]): r for r in self.gy if r[0] == 'csere'}
        self.assertIn(('H0216', 'H5921'), csere)
        self.assertEqual(csere[('H0216', 'H5921')][3], '1')

    # --- kimenet
    def test_kimenet_fajlok_es_fejlec(self):
        for fn in ('meres_osszesites.tsv', 'gyanus_forrascimkek.tsv', 'nem_illesztheto_versek.tsv',
                   'alacsony_atfedesu_egysegek.tsv', 'diagnosztika.tsv'):
            ut = os.path.join(self.ki, fn)
            self.assertTrue(os.path.exists(ut), fn)
            with open(ut, encoding='utf-8') as f:
                elso = f.readline()
            self.assertTrue(elso.startswith('# MANUAL: scope=F175K'), fn)
            self.assertIn('ts=git:teszt', elso)
            self.assertNotIn('\r', _olvas(ut, newline=''))

    def test_verstabla(self):
        sorok = [l.split('\t') for l in _olvas(self.a.verstabla).split('\n') if l and not l.startswith('#')]
        self.assertEqual(len(sorok) - 1, 6)
        gen12 = [r for r in sorok if r[0] == '1Móz 1:2'][0]
        self.assertEqual(gen12[6], 'H8414')     # csak_kjv

    def test_alacsony_atfedes_lista(self):
        # küszöb 50%, legalább 2 KJV-Strong: a Gen1:3 (K_ext = 2, közös 1: 50%) nem alacsonyabb a küszöbnél; Mt1:1: 3/4
        self.assertEqual(self.al, [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
