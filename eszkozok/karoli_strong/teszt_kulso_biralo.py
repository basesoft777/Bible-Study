#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.B — a külső bírálók futtatójának tesztjei, kitalált batch-válaszokon
(hálózat és kulcs nélkül; a kimenet ideiglenes könyvtárba megy).

Futtatás: python eszkozok/karoli_strong/teszt_kulso_biralo.py
"""

import json
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
import kulso_biralo as kb  # noqa: E402
import pontossag_ellenor as pe  # noqa: E402

CELT = pe._celtabla()


def _jo_valasz(n, modell_onb='gpt-x'):
    versek = [{'vers': v, 'jeloles': [[h, [1]] for h in sorted(CELT[n][v])]} for v in CELT[n]]
    return {'modell': modell_onb, 'koteg': n, 'versek': versek}


def _eredmeny(n, tartalom, modell='openai/gpt-6.1-sol-20261101', usage=None, hiba=None):
    if hiba:
        return {'custom_id': 'koteg_%03d' % n, 'response': None, 'error': {'message': hiba}}
    body = {'model': modell, 'choices': [{'finish_reason': 'stop', 'message': {'content': tartalom}}],
            'usage': usage if usage is not None else {'prompt_tokens': 15000, 'completion_tokens': 3000,
                                                      'completion_tokens_details': {'reasoning_tokens': 2000},
                                                      'cost': 0.03}}
    return {'custom_id': 'koteg_%03d' % n, 'response': {'status_code': 200, 'body': body}, 'error': None}


class Alap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='kulso_biralo_teszt_')
        self.regi = (kb.KI, kb.BATCHEK, kb.NAPLO)
        kb.KI = self.tmp
        kb.BATCHEK = os.path.join(self.tmp, 'batchek.tsv')
        kb.NAPLO = os.path.join(self.tmp, 'futasnaplo.tsv')

    def tearDown(self):
        kb.KI, kb.BATCHEK, kb.NAPLO = self.regi
        shutil.rmtree(self.tmp, ignore_errors=True)


class Prompt(unittest.TestCase):
    def test_utasitas_es_bemenet_valtozatlan(self):
        p = kb.prompt(1)
        with open(os.path.join(pe.ELLENOR, 'utasitas.md'), encoding='utf-8') as f:
            self.assertTrue(p.startswith(f.read().rstrip('\n')))
        with open(os.path.join(pe.BEMENET_DIR, 'koteg_001.txt'), encoding='utf-8') as f:
            self.assertTrue(p.endswith(f.read()))
        self.assertIn(kb.KERET, p)

    def test_vak_nincs_opus_itelet(self):
        # Az utasítás példája („pl. claude-opus-5-5”, a modellmező alakja) az Opusé is volt, változatlan;
        # az Opus ítélete (a válaszfájl jelölései) és a gépi pár viszont nem lehet a promptban.
        p = kb.prompt(1)
        for tilos in ('itelet_par', 'er_sorszam'):
            self.assertNotIn(tilos, p)
        with open(os.path.join(pe.VALASZ_DIR, 'koteg_001.json'), encoding='utf-8') as f:
            opus = json.load(f)
        for x in opus['versek']:
            self.assertNotIn(json.dumps(x['jeloles']), p)

    def test_batch_torzs_sorrend(self):
        t = kb.batch_keres('gemini', [1, 2])
        self.assertEqual(list(t)[:2], ['endpoint', 'model'])
        self.assertEqual(list(t)[-1], 'requests')
        self.assertEqual(t['model'], 'google/gemini-4-argon')
        self.assertEqual([r['custom_id'] for r in t['requests']], ['koteg_001', 'koteg_002'])

    def test_72_koteg(self):
        self.assertEqual(kb.osszes_koteg(), list(range(1, 73)))


class Feldolgozas(Alap):
    def test_jo_valasz_kapun_at(self):
        b = {'id': 'batch_abc12345', 'provider': 'OpenAI',
             'results': [_eredmeny(1, json.dumps(_jo_valasz(1), ensure_ascii=False))]}
        n = kb.eredmeny_feldolgoz('gpt', b, CELT)
        self.assertEqual(n[0]['eredmeny'], 'rendben', n[0]['megjegyzes'])
        with open(os.path.join(self.tmp, 'gpt', 'valasz', 'koteg_001.json'), encoding='utf-8') as f:
            d = json.load(f)
        self.assertEqual(d['modell'], 'openai/gpt-6.1-sol-20261101')  # a tényleges, nem az önbevallott
        self.assertEqual(d['modell_onbevallas'], 'gpt-x')
        self.assertEqual(n[0]['cost_usd'], '0.030000')
        self.assertEqual(n[0]['reasoning_tokens'], 2000)
        self.assertEqual(kb.kesz_kotegek('gpt'), [1])

    def test_kodblokk_kerettel(self):
        t = '```json\n' + json.dumps(_jo_valasz(2), ensure_ascii=False) + '\n```'
        n = kb.eredmeny_feldolgoz('gemini', {'id': 'b1', 'results': [
            _eredmeny(2, t, modell='google/gemini-4-argon')]}, CELT)
        self.assertEqual(n[0]['eredmeny'], 'rendben', n[0]['megjegyzes'])

    def test_hianyzo_cel_elvetve(self):
        d = _jo_valasz(3)
        d['versek'][0]['jeloles'] = d['versek'][0]['jeloles'][1:] or []
        n = kb.eredmeny_feldolgoz('gpt', {'id': 'b2', 'results': [_eredmeny(3, json.dumps(d))]}, CELT)
        self.assertEqual(n[0]['eredmeny'], 'kapu_hiba')
        self.assertEqual(kb.kesz_kotegek('gpt'), [])
        self.assertTrue(os.listdir(os.path.join(self.tmp, 'gpt', 'elvetett')))

    def test_rossz_json_es_hiba(self):
        n = kb.eredmeny_feldolgoz('gpt', {'id': 'b3', 'results': [
            _eredmeny(4, 'nem json'), _eredmeny(5, None, hiba='timeout')]}, CELT)
        self.assertEqual([x['eredmeny'] for x in n], ['rossz_json', 'hiba'])

    def test_anthropic_modell_elutasitva(self):
        n = kb.eredmeny_feldolgoz('gpt', {'id': 'b4', 'results': [
            _eredmeny(6, json.dumps(_jo_valasz(6)), modell='anthropic/claude-opus-5.5')]}, CELT)
        self.assertEqual(n[0]['eredmeny'], 'kapu_hiba')

    def test_koltseg_arbol_ha_nincs_cost(self):
        n = kb.eredmeny_feldolgoz('gpt', {'id': 'b5', 'results': [_eredmeny(
            7, json.dumps(_jo_valasz(7)), usage={'prompt_tokens': 1000000, 'completion_tokens': 200000})]}, CELT)
        self.assertEqual((n[0]['cost_usd'], n[0]['koltseg_forras']), ('2.000000', 'ar_config'))


class Menet(Alap):
    def test_bekuld_begyujt_kitalalt_http(self):
        hivasok = []

        def http(m, ut, adat=None):
            hivasok.append((m, ut))
            if m == 'POST':
                return {'id': 'batch_teszt0001', 'status': 'validating'}
            return {'id': 'batch_teszt0001', 'status': 'completed', 'provider': 'Google',
                    'usage': {'prompt_tokens': 30000, 'completion_tokens': 6000, 'cost': 0.06},
                    'results': [_eredmeny(1, json.dumps(_jo_valasz(1)), modell='google/gemini-4-argon'),
                                _eredmeny(2, json.dumps(_jo_valasz(2)), modell='google/gemini-4-argon')]}
        kb.bekuld('gemini', '1,2', 5.0, http=http)
        self.assertEqual(kb.begyujt(0, http=http), 0)
        self.assertEqual(kb.kesz_kotegek('gemini'), [1, 2])
        self.assertAlmostEqual(kb.osszkoltseg(), 0.06)
        # a hiányzó kötegek: a kész kettő nélkül
        hivasok.clear()
        kb.bekuld('gemini', 'hianyzo', 500.0, http=lambda m, u, a=None: (
            hivasok.append(len(a['requests'])) or {'id': 'batch_teszt0002', 'status': 'validating'}))
        self.assertEqual(hivasok, [70])

    def test_plafon(self):
        with self.assertRaises(SystemExit):
            kb.bekuld('gpt', 'mind', 0.01, http=lambda *x: self.fail('nem hívhat'))


if __name__ == '__main__':
    unittest.main(verbosity=1)
