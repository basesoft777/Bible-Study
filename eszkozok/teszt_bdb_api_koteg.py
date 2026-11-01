#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eszkozok/bdb_api_koteg.py önállóan (hálózat és kulcs nélkül, hamis hívóval).

    python eszkozok/teszt_bdb_api_koteg.py
"""

import json
import os
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_api_koteg as B  # noqa: E402

STRONG = 'H8546'     # a 13. adag első sora


class Alap(unittest.TestCase):
    def setUp(self):
        self.regi = B.MUNKA
        B.MUNKA = tempfile.mkdtemp()

    def tearDown(self):
        B.MUNKA = self.regi


class Kicsi(Alap):
    def test_custom_id(self):
        self.assertEqual(B.custom_id('H8546', 1, 1), 'H8546-c1-p1')
        self.assertEqual(B.custom_id_bont('H0003b-c2-p2'), ('H0003b', 2, 2))
        self.assertIsNone(B.custom_id_bont('x-c1-p1'))

    def test_koltseg(self):
        self.assertAlmostEqual(B.koltseg({'input_tokens': 1000000, 'output_tokens': 1000000}), 6.0)
        u = {'cache_read_input_tokens': 1000000, 'cache_creation_input_tokens': 1000000,
             'cache_creation': {'ephemeral_1h_input_tokens': 1000000}}
        self.assertAlmostEqual(B.koltseg(u), 0.10 + 2.00)
        self.assertAlmostEqual(B.koltseg({'cache_creation_input_tokens': 1000000}), 1.25)

    def test_json_valasz(self):
        self.assertEqual(B.json_valasz('{"forditas_hu": "a", "bizonytalan_feloldasok": ["Heb."]}'), ('a', ['Heb.']))
        self.assertEqual(B.json_valasz('```json\n{"forditas_hu": "b"}\n```')[0], 'b')
        self.assertIsNone(B.json_valasz('nem json')[0])
        self.assertIsNone(B.json_valasz('{"forditas_hu": ""}')[0])

    def test_blokkok_osszefuzve_a_prompt(self):
        k = B.kerelmek_strongra(STRONG)[0]
        bl = B.blokkok(k['prompt'])
        self.assertEqual(''.join(bl), k['prompt'])
        self.assertEqual(len(bl), 3)
        tart = B.uzenet_tartalom(k['prompt'])
        self.assertIn('cache_control', tart[0])
        self.assertIn('cache_control', tart[1])
        self.assertNotIn('cache_control', tart[2])

    def test_kerelem_helyorzo_es_token(self):
        k = B.kerelmek_strongra(STRONG)[0]
        self.assertEqual(k['mod'], 'szakasz')
        self.assertIn('⟪1⟫', k['prompt'])
        forras = k['prompt'].split('Forrás (Thayer, angol):')[1].split('## Kimenet')[0]
        self.assertNotRegex(forras, '[֐-׿]')   # a forrásban nincs héber, csak helyőrző

    def test_params(self):
        p = B.kerelem_params([{'role': 'user', 'content': 'x'}], 5000)
        self.assertEqual(p['model'], 'claude-sonnet-5-5')
        self.assertEqual(p['thinking'], {'type': 'adaptive'})
        self.assertEqual(p['output_config'], {'effort': 'high'})
        self.assertGreaterEqual(p['max_tokens'], 16000)

    def test_modell_allapot(self):
        self.assertEqual(B.modell_allapot({'claude-sonnet-5-5'}), ('sonnet', 'claude-sonnet-5-5'))
        with self.assertRaises(SystemExit):
            B.modell_allapot({'a', 'b'})
        with self.assertRaises(SystemExit):
            B.modell_allapot({'gpt-x'})

    def test_terv_rendezes_es_csomag(self):
        t = B.terv(13, [STRONG, 'H8409', 'H8547'])
        self.assertEqual(sorted(k['strong'] for k in t), ['H8409', 'H8546', 'H8547'])
        self.assertEqual(B.terv(13, [STRONG, 'H8409', 'H8547']), t)      # determinisztikus
        self.assertEqual([len(c) for c in B.csomagok(t * 2, 4)], [4, 2])


class Folyamat(Alap):
    def hivo_keszit(self, szoveg_fn):
        kuldott = {}

        def hamis(met, path, torzs=None, nyers=False):
            if met == 'POST':
                kuldott['kerelmek'] = torzs['requests']
                return {'id': 'msgbatch_teszt'}
            if path.startswith('/v1/messages/batches/'):
                return {'processing_status': 'ended', 'results_url': 'https://x/r', 'request_counts': {}}
            sorok = []
            for k in reversed(kuldott['kerelmek']):    # fordított sorrend: custom_id szerint kell
                sorok.append({'custom_id': k['custom_id'], 'result': {'type': 'succeeded', 'message': {
                    'model': 'claude-sonnet-5-5', 'stop_reason': 'end_turn',
                    'content': [{'type': 'thinking', 'thinking': ''}, {'type': 'text', 'text': szoveg_fn(k)}],
                    'usage': {'input_tokens': 1000, 'output_tokens': 500, 'cache_read_input_tokens': 2000}}}})
            return '\n'.join(json.dumps(s, ensure_ascii=False) for s in sorok)
        return hamis, kuldott

    def test_bekuld_begyujt_kapuz(self):
        # a „fordítás” a forrás maga: a kapuk nem engedik át (angol szöveg), tehát javítandó lesz; a folyamat gépi része fut végig
        def ford(k):
            torzs = k['params']['messages'][0]['content'][-1]['text']
            forras = torzs.split('Forrás (Thayer, angol):')[1].split('## Kimenet')[0].strip()
            return json.dumps({'strong': STRONG, 'forditas_hu': forras, 'bizonytalan_feloldasok': []}, ensure_ascii=False)
        hamis, kuldott = self.hivo_keszit(ford)
        self.assertEqual(B.bekuld(13, 't', hivo=hamis, strongok=[STRONG]), 0)
        self.assertEqual([k['custom_id'] for k in kuldott['kerelmek']], ['H8546-c1-p1'])
        self.assertEqual(B.bekuld(13, 't', hivo=hamis, strongok=[STRONG]), 0)      # már beküldve: nem küld újra
        self.assertEqual(B.begyujt('t', hivo=hamis), 0)
        n = len(B.AK.tsv_olvas(B.ut('futasnaplo.tsv')))
        self.assertEqual(n, 1)
        B.begyujt('t', hivo=hamis)
        self.assertEqual(len(B.AK.tsv_olvas(B.ut('futasnaplo.tsv'))), 1)           # idempotens
        self.assertAlmostEqual(B.futo_osszeg(), B.koltseg({'input_tokens': 1000, 'output_tokens': 500,
                                                           'cache_read_input_tokens': 2000}), places=6)
        B.kapuz(13, [STRONG])
        r = B.jsonl_olvas(B.ut('kapu_eredmeny.jsonl'))
        self.assertEqual(len(r), 1)
        self.assertIn(r[0]['allapot'], ('kesz', 'javitando'))
        self.assertEqual(r[0]['modellek'], ['claude-sonnet-5-5'])

    def test_plafon_megallit(self):
        hamis, kuldott = self.hivo_keszit(lambda k: '')
        regi = B.PLAFON_USD
        B.PLAFON_USD = 0.0001
        try:
            self.assertEqual(B.bekuld(13, 't', hivo=hamis, strongok=[STRONG]), 3)
        finally:
            B.PLAFON_USD = regi
        self.assertNotIn('kerelmek', kuldott)

    def test_javito_uzenet(self):
        self.assertIn('- 14_szakasz: hianyzo token: 3', B.javito_uzenet(['14_szakasz: hianyzo token: 3']))


def futtat():
    s = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    return 0 if unittest.TextTestRunner(verbosity=1).run(s).wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(futtat())
