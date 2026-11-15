#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_keret_meres.py -- az `eszkozok/keret_meres.py` tesztjei (F222): a súlyozás, a deduplikálás (azonos üzenet-azonosító
csak egyszer, a hét kezdete előtti üzenet nem számít), a sávhoz rendelés (munkamappa-tábla, cím-előtag, ág-brief,
ismeretlen), a Fable külön összege és a kalibrálás. Mintaként kézzel írt jsonl-átiratok ideiglenes könyvtárban.

Futtatás: python eszkozok/tesztek/test_keret_meres.py
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import date

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import keret_meres as K  # noqa: E402

HET = date(2026, 11, 14)

SULY = [
    {'modell': 'claude-opus-5-5', 'csalad': 'opus', 'input': '4', 'cache_5m': '5', 'cache_1h': '8',
     'cache_olvasas': '0.2', 'output': '20', 'forras': 'teszt', '_sor': 2},
    {'modell': 'claude-sonnet-5-5', 'csalad': 'sonnet', 'input': '2', 'cache_5m': '2.5', 'cache_1h': '4',
     'cache_olvasas': '0.1', 'output': '10', 'forras': 'teszt', '_sor': 3},
    {'modell': 'claude-fable-5-2', 'csalad': 'fable', 'input': '8', 'cache_5m': '10', 'cache_1h': '16',
     'cache_olvasas': '0.2', 'output': '40', 'forras': 'teszt', '_sor': 4},
]


def usage(inp=0, c5=0, c1=0, olv=0, out=0, bontas=True):
    u = {'input_tokens': inp, 'cache_creation_input_tokens': c5 + c1, 'cache_read_input_tokens': olv,
         'output_tokens': out}
    if bontas:
        u['cache_creation'] = {'ephemeral_5m_input_tokens': c5, 'ephemeral_1h_input_tokens': c1}
    return u


def asszisztens(azon, ts, modell='claude-opus-5-5', u=None, cwd='E:\\x\\wt-a', ag='claude/x'):
    return {'type': 'assistant', 'timestamp': ts, 'cwd': cwd, 'gitBranch': ag, 'uuid': 'u-' + azon,
            'message': {'id': azon, 'model': modell, 'usage': u or usage(out=1000000)}}


class Alap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ut = self.tmp.name

    def atirat(self, rel, sorok):
        ut = os.path.join(self.ut, *rel.split('/'))
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            for s in sorok:
                f.write((json.dumps(s, ensure_ascii=False, separators=(',', ':')) if isinstance(s, dict) else s) + '\n')
        return ut

    def beolvas(self, fajlok):
        return K.beolvas(fajlok, HET)


class SulyozasTest(Alap):
    def test_tokenfajtankent_az_ar_szerint(self):
        # 1M input + 1M 5m írás + 1M 1h írás + 1M olvasás + 1M output opus 5.5-ön: 4 + 5 + 8 + 0.2 + 20
        u = usage(inp=1000000, c5=1000000, c1=1000000, olv=1000000, out=1000000)
        self.assertAlmostEqual(K.egyseg(u, SULY[0]), 37.2)

    def test_gyorsitotar_iras_bontas_nelkul_5_perces(self):
        u = usage(c5=1000000, bontas=False)
        self.assertEqual(K.tokenek(u)['cache_5m'], 1000000)
        self.assertEqual(K.tokenek(u)['cache_1h'], 0)

    def test_modell_leghosszabb_elotag(self):
        self.assertEqual(K.modell_ar('claude-fable-5-2', SULY)[0]['csalad'], 'fable')
        sor, pontos = K.modell_ar('claude-sonnet-5-5-20261101', SULY)
        self.assertEqual((sor['csalad'], pontos), ('sonnet', True))

    def test_ismeretlen_modell_csaladi_ar_es_jeloles(self):
        sor, pontos = K.modell_ar('claude-opus-9', SULY)
        self.assertEqual((sor['csalad'], pontos), ('opus', False))
        self.assertEqual(K.modell_ar('valami-mas', SULY), (None, False))

    def test_a_valos_tablak_ervenyesek(self):
        suly, mm, pontok, hibak = K.tablak_olvas(K.REPO)
        self.assertEqual(hibak, [])
        self.assertGreater(len(suly), 0)
        self.assertTrue(all(s['csalad'] in K.CSALADOK for s in suly))
        # a jelenlegi modellek mind szerepelnek a listaárban
        for m in ('claude-opus-5-5', 'claude-sonnet-5-5', 'claude-haiku-5-5', 'claude-fable-5-2'):
            self.assertTrue(K.modell_ar(m, suly)[1], m)


class BeolvasasTest(Alap):
    def test_az_azonos_uzenet_egyszer_szamit(self):
        a = self.atirat('p1/sess-a.jsonl', [asszisztens('m1', '2026-11-15T10:00:00.000Z'),
                                            asszisztens('m1', '2026-11-15T10:00:00.000Z')])
        b = self.atirat('p2/sess-b.jsonl', [asszisztens('m1', '2026-11-15T10:00:00.000Z'),   # elágaztatott másolat
                                            asszisztens('m2', '2026-11-15T10:05:00.000Z')])
        uzenetek, _ = self.beolvas([a, b])
        self.assertEqual(sorted(uzenetek), ['m1', 'm2'])

    def test_blokkra_bontott_uzenetnel_a_legteljesebb_usage_marad(self):
        a = self.atirat('p1/sess-a.jsonl', [asszisztens('m1', '2026-11-15T10:00:00.000Z', u=usage(out=10)),
                                            asszisztens('m1', '2026-11-15T10:00:01.000Z', u=usage(out=500))])
        uzenetek, _ = self.beolvas([a])
        self.assertEqual(uzenetek['m1']['usage']['output_tokens'], 500)

    def test_a_het_kezdete_elotti_uzenet_nem_szamit(self):
        a = self.atirat('p1/sess-a.jsonl', [asszisztens('regi', '2026-11-14T13:59:59.000Z'),
                                            asszisztens('uj', '2026-11-14T14:00:00.000Z')])
        uzenetek, _ = self.beolvas([a])
        self.assertEqual(list(uzenetek), ['uj'])

    def test_synthetic_es_usage_nelkuli_kimarad(self):
        a = self.atirat('p1/sess-a.jsonl', [asszisztens('s', '2026-11-15T10:00:00.000Z', modell='<synthetic>'),
                                            {'type': 'assistant', 'timestamp': '2026-11-15T10:00:00.000Z',
                                             'message': {'id': 'nu', 'model': 'claude-opus-5-5'}},
                                            {'type': 'user', 'timestamp': '2026-11-15T10:00:00.000Z'},
                                            'nem json {'])
        self.assertEqual(self.beolvas([a])[0], {})

    def test_subagent_a_szulo_sessionhoz_tartozik(self):
        self.assertEqual(K.session_azonosito('C:\\p\\abc-123.jsonl'), 'abc-123')
        self.assertEqual(K.session_azonosito('/p/abc-123/subagents/agent-9.jsonl'), 'abc-123')
        a = self.atirat('p1/abc-123.jsonl', [asszisztens('m1', '2026-11-15T10:00:00.000Z'),
                                             {'type': 'custom-title', 'customTitle': 'SYSTEMS · Cím', 'sessionId': 'abc-123'}])
        s = self.atirat('p1/abc-123/subagents/agent-9.jsonl', [asszisztens('m2', '2026-11-15T10:01:00.000Z')])
        uzenetek, meta = self.beolvas([a, s])
        self.assertEqual({u['session'] for u in uzenetek.values()}, {'abc-123'})
        self.assertEqual(meta['abc-123']['cim'], 'SYSTEMS · Cím')


class SavTest(unittest.TestCase):
    TERKEP = ({'claude/ag-brief': 'SERVER'}, {218: 'CONTENT'})

    def sav(self, meta, mm=None):
        return K.hozzarendel(meta, mm or [], self.TERKEP)

    def test_cim_elotag(self):
        self.assertEqual(self.sav({'cim': 'SYSTEMS · Valami'})[0], 'SYSTEMS')
        self.assertEqual(self.sav({'cim': 'CONTENT · F218a: a következő menet'})[0], 'CONTENT')
        self.assertEqual(self.sav({'cim': 'Felmérés: BDB-tanú'})[0], 'FELMERES')
        self.assertEqual(self.sav({'cim': 'Orkesztrátor:'})[0], 'ORKESZTRACIO')
        self.assertEqual(self.sav({'cim': 'Valami más cím'})[0], K.ISMERETLEN)

    def test_munkamappa_tabla_eloszor(self):
        mm = [{'munkamappa': 'orkesztrator-uj-cikkek', 'sav': 'ORKESZTRACIO', 'megjegyzes': '', '_sor': 2}]
        meta = {'cwd': 'C:\\Users\\x\\.claude\\worktrees\\orkesztrator-uj-cikkek-ba7133', 'cim': 'SYSTEMS · Más'}
        self.assertEqual(self.sav(meta, mm), ('ORKESZTRACIO', 'munkamappa-tábla'))

    def test_cim_hianyaban_az_ag_briefje(self):
        self.assertEqual(self.sav({'ag': 'claude/ag-brief'}), ('SERVER', 'az ág briefje'))
        self.assertEqual(self.sav({'ag': 'claude/f218-generator-uj-a'}), ('CONTENT', 'az ág F-száma'))

    def test_ismeretlen_nem_vesz_el(self):
        self.assertEqual(self.sav({'ag': 'claude/valami', 'cwd': 'E:\\x'}), (K.ISMERETLEN, 'nem rendelhető'))


class OsszesitesTest(Alap):
    def futtat(self, sorok_a, sorok_b=None, pontok=None, mm=None):
        fajlok = [self.atirat('p1/sess-a.jsonl', sorok_a)]
        if sorok_b is not None:
            fajlok.append(self.atirat('p2/sess-b.jsonl', sorok_b))
        uzenetek, meta = self.beolvas(fajlok)
        return K.osszesit(uzenetek, meta, SULY, mm or [], pontok or [], HET)

    def cim(self, sid, cim):
        return {'type': 'custom-title', 'customTitle': cim, 'sessionId': sid}

    def test_savonkent_osszeg_arany_es_top(self):
        e = self.futtat(
            [self.cim('sess-a', 'SYSTEMS · A'), asszisztens('m1', '2026-11-15T10:00:00.000Z', u=usage(out=1000000))],   # 20
            [self.cim('sess-b', 'CONTENT · B'),
             asszisztens('m2', '2026-11-15T10:00:00.000Z', modell='claude-sonnet-5-5', u=usage(out=3000000)),          # 30
             asszisztens('m3', '2026-11-15T11:00:00.000Z', modell='claude-sonnet-5-5', u=usage(out=1000000))])        # 10
        self.assertAlmostEqual(e['savok']['SYSTEMS']['egyseg'], 20)
        self.assertAlmostEqual(e['savok']['CONTENT']['egyseg'], 40)
        self.assertAlmostEqual(e['savok']['CONTENT']['arany'], 40 / 60)
        self.assertEqual(e['savok']['CONTENT']['top'][0][0], 'CONTENT · B')
        self.assertAlmostEqual(e['osszes'], 60)

    def test_ismeretlen_sav_osszege_megvan(self):
        e = self.futtat([asszisztens('m1', '2026-11-15T10:00:00.000Z', ag='claude/valami', cwd='E:\\x')])
        self.assertAlmostEqual(e['savok'][K.ISMERETLEN]['egyseg'], 20)
        self.assertAlmostEqual(e['osszes'], 20)

    def test_mermesi_pont_nelkul_nincs_szazalek(self):
        e = self.futtat([self.cim('sess-a', 'SYSTEMS · A'), asszisztens('m1', '2026-11-15T10:00:00.000Z')])
        self.assertIsNone(e['kalibralas']['heti'])
        self.assertIsNone(e['savok']['SYSTEMS']['szazalek'])
        self.assertIsNone(e['osszes_szazalek'])

    def test_kalibralas_egy_ponttal(self):
        # 20 + 20 egység a pont ideje előtt: 40 egység = 8% -> 0,2 %/egység; a pont utáni 20 egység már +4%
        pont = {'ts': '2026-11-15T10:30', 'heti_szazalek': '8', 'fable_szazalek': '0', 'forras': 't', '_sor': 2}
        e = self.futtat([self.cim('sess-a', 'SYSTEMS · A'),
                         asszisztens('m1', '2026-11-15T10:00:00.000Z'), asszisztens('m2', '2026-11-15T10:10:00.000Z'),
                         asszisztens('m3', '2026-11-15T12:00:00.000Z')], pontok=[pont])
        self.assertAlmostEqual(e['kalibralas']['heti'], 0.2)
        self.assertAlmostEqual(e['savok']['SYSTEMS']['szazalek'], 12.0)
        self.assertIsNone(e['kalibralas']['fable'])      # 0% Fable pont nem ad szorzót
        self.assertEqual(e['kalibralas']['pontok'], 1)

    def test_masik_het_pontja_nem_szamit(self):
        pont = {'ts': '2026-11-10T10:30', 'heti_szazalek': '8', 'fable_szazalek': '0', 'forras': 't', '_sor': 2}
        e = self.futtat([asszisztens('m1', '2026-11-15T10:00:00.000Z')], pontok=[pont])
        self.assertIsNone(e['kalibralas']['heti'])
        self.assertEqual(e['kalibralas']['pontok'], 0)

    def test_fable_kulon_osszeg_es_szorzo(self):
        pont = {'ts': '2026-11-15T10:30', 'heti_szazalek': '10', 'fable_szazalek': '4', 'forras': 't', '_sor': 2}
        e = self.futtat([self.cim('sess-a', 'CONTENT · A'),
                         asszisztens('m1', '2026-11-15T10:00:00.000Z', modell='claude-fable-5-2', u=usage(out=1000000)),   # 40
                         asszisztens('m2', '2026-11-15T10:01:00.000Z', u=usage(out=3000000))],                            # 60
                        pontok=[pont])
        self.assertAlmostEqual(e['fable_osszes'], 40)
        self.assertAlmostEqual(e['osszes'], 100)
        self.assertAlmostEqual(e['savok']['CONTENT']['fable_egyseg'], 40)
        self.assertAlmostEqual(e['kalibralas']['heti'], 0.1)
        self.assertAlmostEqual(e['kalibralas']['fable'], 0.1)
        self.assertAlmostEqual(e['fable_osszes_szazalek'], 4.0)

    def test_ismeretlen_modell_jelolve(self):
        e = self.futtat([asszisztens('m1', '2026-11-15T10:00:00.000Z', modell='claude-opus-9')])
        self.assertEqual(e['ismeretlen_modell'], {'claude-opus-9': 1})
        self.assertAlmostEqual(e['osszes'], 20)      # a család szerinti (opus 5.5) ár

    def test_szoveg_kimenet_nem_tartalmaz_nyers_sort(self):
        e = self.futtat([self.cim('sess-a', 'SYSTEMS · A'), asszisztens('m1', '2026-11-15T10:00:00.000Z')])
        t = K.szoveg(e)
        self.assertIn('SYSTEMS', t)
        self.assertIn('arány', t)


if __name__ == '__main__':
    unittest.main(verbosity=1)
