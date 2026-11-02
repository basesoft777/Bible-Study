#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eszkozok/thayer_api_koteg.py önállóan (hálózat és kulcs nélkül, hamis hívóval).

    python eszkozok/teszt_thayer_api_koteg.py
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
import thayer_api_koteg as T  # noqa: E402

E, TB, F = T.E, T.TB, T.F
STRONG = 'G1941'     # kész sonnet szakaszos fordítás (7 szakasz, 37 helyőrző)


def hu_sorok(strong):
    return [r for r in E.tsv_dict_sorok(E.FORDITASOK_UT)
            if r['szotar'] == 'Thayer' and r['strong'] == strong and r['jelentes_szam'].startswith('sz')]


def hamis_valasz(strong, sorok):
    """Egy kész szakaszos fordításból a modell várt válasza: tokenes szöveg, a héber/görög szakaszok ⟦n⟧ helyőrzőkkel."""
    ker = T.kerelmek_strongra(strong)
    assert len(ker) == 1
    hely = ker[0]['hely']
    fin = ' '.join('%s %s' % (TB.token(int(r['jelentes_szam'][2:])), r['forditas_hu']) for r in sorok)
    hasznalt = set()

    def cs(m):
        for i, h in enumerate(hely):
            if i not in hasznalt and h == m.group(0):
                hasznalt.add(i)
                return '⟦%d⟧' % (i + 1)
        return m.group(0)
    return fin, E.HG_SZAKASZ.sub(cs, fin)


class Alap(unittest.TestCase):
    def setUp(self):
        self.regi = (T.MUNKA, T.PLAFON_USD, E.KISNAGYBETU_UT)
        T.MUNKA = tempfile.mkdtemp()
        E.KISNAGYBETU_UT = os.path.join(tempfile.mkdtemp(), 'kisnagybetu.tsv')      # a repó naplója nem módosul

    def tearDown(self):
        T.MUNKA, T.PLAFON_USD, E.KISNAGYBETU_UT = self.regi


class Kicsi(Alap):
    def test_custom_id_oda_vissza(self):
        self.assertEqual(T.custom_id('G1941', 2, 1), 'G1941-c2-p1')
        self.assertEqual(T.custom_id_bont('G1941-c2-p1'), ('G1941', 2, 1))
        self.assertEqual(T.custom_id_bont('G0003b-c1-p2'), ('G0003b', 1, 2))
        self.assertIsNone(T.custom_id_bont('H1941-c1-p1'))
        self.assertIsNone(T.custom_id_bont('G1941-1'))

    def test_prompt_azonos_a_forditas_prompt_epittel(self):
        k = T.kerelmek_strongra(STRONG)[0]
        _, szak = F.forras(STRONG)
        cs = TB.csoportok(szak)[0]
        eredeti = F.prompt_epit(F.forras(STRONG)[0], cs, E.darab_info_szoveg(0, 1))
        self.assertNotEqual(k['prompt'], eredeti)
        # a helyőrzős forrásrészt visszaállítva a prompt bájtra azonos
        i = k['prompt'].rfind(T.FORRAS_JEL)
        j = k['prompt'].find(T.KIMENET_JEL, i)
        bont = k['prompt'][i + len(T.FORRAS_JEL):j].strip('\n')
        vissza, hiany, tobb = E.helyorzo_visszaallit(bont, k['hely'])
        self.assertEqual((hiany, tobb), ([], []))
        self.assertEqual(k['prompt'][:i + len(T.FORRAS_JEL)] + '\n\n' + vissza + '\n\n' + k['prompt'][j:], eredeti)
        self.assertNotRegex(bont, '[Ͱ-Ͽἀ-῿֐-׿]')      # a forrásban nincs görög/héber, csak helyőrző
        self.assertIn('⟦1⟧', bont)
        self.assertIn('Thayer', k['prompt'])
        self.assertEqual(k['kot'], E.kotelezo_alakok_szoveg(TB.nezet(cs)))

    def test_helyorzo_korut_betuhu(self):
        for s in ('G1941', 'G4151'):
            for k in T.kerelmek_strongra(s):
                i = k['prompt'].rfind(T.FORRAS_JEL)
                j = k['prompt'].find(T.KIMENET_JEL, i)
                bont = k['prompt'][i + len(T.FORRAS_JEL):j].strip('\n')
                vissza, hiany, tobb = E.helyorzo_visszaallit(bont, k['hely'])
                self.assertEqual((hiany, tobb), ([], []))
                self.assertEqual(vissza, TB.tokenes(TB.csoportok(TB.szakaszok(s))[k['csoport'] - 1]).strip('\n'))

    def test_params(self):
        p = T.kerelem_params([{'role': 'user', 'content': 'x'}], 5000)
        self.assertEqual(p['model'], 'claude-sonnet-5-5')
        self.assertEqual(p['thinking'], {'type': 'adaptive'})
        self.assertEqual(p['output_config'], {'effort': 'high'})

    def test_strongok_olvas(self):
        f = os.path.join(T.MUNKA, 'l.txt')
        with open(f, 'w', encoding='utf-8') as h:
            h.write('# megj\nG1941\tx\n\nG12\nG1941\n')
        self.assertEqual(T.strongok_olvas(f), ['G1941', 'G0012'])


class Lista(Alap):
    def test_minden_strongot_lefed_es_a_kesz_kesz(self):
        sorok = T.teljes_lista('2026-11-02')
        tabla = TB.tabla_olvas()
        self.assertEqual(len(sorok), len(tabla))
        self.assertEqual(len(sorok), 5426)
        self.assertEqual({r['strong'] for r in sorok}, set(tabla))
        d = {r['strong']: r for r in sorok}
        self.assertEqual((d[STRONG]['statusz'], d[STRONG]['ok']), ('kihagyva', 'kesz'))
        for r in sorok:
            self.assertIn('scope=%s | forras=' % r['strong'], r['proveniencia'])
            self.assertIn(r['ok'], ('kesz', 'nincs_szakaszos', 'hianyos', 'elavult_hash'))
        szoveg = T.lista_szoveg(sorok, '2026-11-02')
        self.assertEqual(len([s for s in szoveg.split('\n') if s and not s.startswith('#')]), 5427)


class Folyamat(Alap):
    def test_bekuld_nulla_plafonnal_nem_indul(self):
        hivott = []
        kod = T.bekuld([STRONG], 'teszt', 0.0, hivo=lambda *a, **k: hivott.append(a))
        self.assertEqual(kod, 3)
        self.assertEqual(hivott, [])
        self.assertEqual(T.bekuld([STRONG], 'teszt', hivo=lambda *a, **k: hivott.append(a)), 3)      # alapérték: 0
        self.assertEqual(hivott, [])

    def test_bekuld_plafon_felett_megall_alatta_kuld(self):
        hivott = []

        def hivo(m, ut, torzs=None, nyers=False):
            hivott.append((m, ut, torzs))
            return {'id': 'msgbatch_teszt'}
        self.assertEqual(T.bekuld([STRONG], 'teszt', 0.0001, hivo=hivo), 3)
        self.assertEqual(hivott, [])
        self.assertEqual(T.bekuld([STRONG], 'teszt', 50.0, hivo=hivo), 0)
        self.assertEqual(len(hivott), 1)
        kerelmek = hivott[0][2]['requests']
        self.assertEqual([k['custom_id'] for k in kerelmek], ['G1941-c1-p1'])
        self.assertEqual(kerelmek[0]['params']['model'], 'claude-sonnet-5-5')
        self.assertEqual(T.bekuld([STRONG], 'teszt', 50.0, hivo=hivo), 0)      # a második hívás már nem küld
        self.assertEqual(len(hivott), 1)

    def test_kapuz_rogzit_azonos_a_meglevo_sorokkal(self):
        sorok = hu_sorok(STRONG)
        self.assertEqual(len(sorok), 7)
        fin, valasz = hamis_valasz(STRONG, sorok)
        rek = {'custom_id': 'G1941-c1-p1', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn',
               'usage': {'input_tokens': 10, 'output_tokens': 10}, 'hiba': '', 'batch_id': 'b',
               'szoveg': json.dumps({'strong': STRONG, 'forditas_hu': valasz, 'bizonytalan_feloldasok': []}, ensure_ascii=False)}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [rek])
        self.assertEqual(T.kapuz([STRONG]), 0)
        eredm = T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))
        self.assertEqual(len(eredm), 1)
        self.assertEqual(eredm[0]['allapot'], 'kesz', eredm[0]['hibak'])
        self.assertEqual(eredm[0]['vegleges'], fin)
        munka = os.path.join(T.MUNKA, 'munka.tsv')
        bukott = os.path.join(T.MUNKA, 'bukott.tsv')
        self.assertEqual(T.rogzit([STRONG], datum='2026.11.02', munka_ut=munka, bukott_ut=bukott), 0)
        uj = list(E.tsv_dict_sorok(munka))
        self.assertEqual(len(uj), 7)
        self.assertFalse(os.path.exists(bukott))
        for u, r in zip(uj, sorok):
            self.assertEqual(u['forras_hash'], r['forras_hash'])
            self.assertEqual(u['jelentes_szam'], r['jelentes_szam'])
            self.assertEqual(u['forditas_hu'], r['forditas_hu'])
            self.assertEqual((u['szotar'], u['strong'], u['entry_id'], u['mezo']), (r['szotar'], r['strong'], r['entry_id'], r['mezo']))
            self.assertEqual((u['allapot'], u['modell']), ('sonnet', 'claude-sonnet-5-5'))      # a válasz tényleges modellneve

    def test_modellnev_a_valaszbol(self):
        sorok = hu_sorok(STRONG)
        _, valasz = hamis_valasz(STRONG, sorok)
        rek = {'custom_id': 'G1941-c1-p1', 'tipus': 'succeeded', 'modell': 'claude-opus-5-5', 'stop': 'end_turn', 'usage': {},
               'hiba': '', 'batch_id': 'b', 'szoveg': json.dumps({'forditas_hu': valasz}, ensure_ascii=False)}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [rek])
        T.kapuz([STRONG])
        munka = os.path.join(T.MUNKA, 'munka.tsv')
        T.rogzit([STRONG], datum='2026.11.02', munka_ut=munka, bukott_ut=os.path.join(T.MUNKA, 'b.tsv'))
        self.assertEqual({(r['allapot'], r['modell']) for r in E.tsv_dict_sorok(munka)}, {('opus', 'claude-opus-5-5')})

    def test_kapuhiba_javitando_majd_bukott(self):
        rek = {'custom_id': 'G1941-c1-p1', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn', 'usage': {},
               'hiba': '', 'batch_id': 'b', 'szoveg': json.dumps({'forditas_hu': 'nincs token és helyőrző'}, ensure_ascii=False)}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [rek])
        T.kapuz([STRONG])
        r = T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))[0]
        self.assertEqual((r['allapot'], r['proba']), ('javitando', 1))
        hivott = []
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [dict(rek, custom_id='G1941-c1-p2')])
        T.kapuz([STRONG])
        r = T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))[0]
        self.assertEqual((r['allapot'], r['proba']), ('javitando', 2))
        munka = os.path.join(T.MUNKA, 'munka.tsv')
        bukott = os.path.join(T.MUNKA, 'bukott.tsv')
        T.rogzit([STRONG], datum='2026.11.02', munka_ut=munka, bukott_ut=bukott)
        self.assertFalse(os.path.exists(munka))
        sorok = open(bukott, encoding='utf-8').read().split('\n')
        self.assertEqual(sorok[0].split('\t'), T.BUKOTT_FEJLEC)
        self.assertEqual(sorok[1].split('\t')[0], 'G1941')
        self.assertEqual(hivott, [])

    def test_javit_nulla_plafonnal_nem_kuld(self):
        rek = {'custom_id': 'G1941-c1-p1', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn', 'usage': {},
               'hiba': '', 'batch_id': 'b', 'szoveg': 'nem json'}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [rek])
        T.kapuz([STRONG])
        hivott = []
        self.assertEqual(T.javit([STRONG], 'teszt', 0.0, hivo=lambda *a, **k: hivott.append(a)), 3)
        self.assertEqual(hivott, [])
        self.assertEqual(T.javit([STRONG], 'teszt', 50.0, hivo=lambda m, u, t=None, nyers=False: (hivott.append(t), {'id': 'x'})[1]), 0)
        self.assertEqual(hivott[0]['requests'][0]['custom_id'], 'G1941-c1-p2')
        self.assertEqual(hivott[0]['requests'][0]['params']['messages'][1]['role'], 'assistant')

    def test_begyujt_hamis_batchbol(self):
        T.ujra_naplo('msgbatch_t', 'teszt', 1, 1, 1)
        eredmeny = {'custom_id': 'G1941-c1-p1', 'result': {'type': 'succeeded', 'message': {
            'model': 'claude-sonnet-5-5', 'stop_reason': 'end_turn', 'usage': {'input_tokens': 1000000, 'output_tokens': 0},
            'content': [{'type': 'text', 'text': '{"forditas_hu": "x"}'}]}}}

        def hivo(m, ut, torzs=None, nyers=False):
            if nyers:
                return json.dumps(eredmeny) + '\n'
            return {'processing_status': 'ended', 'results_url': 'http://x/r'}
        self.assertEqual(T.begyujt('teszt', hivo=hivo), 0)
        self.assertEqual(len(T.jsonl_olvas(T.ut('valaszok.jsonl'))), 1)
        self.assertAlmostEqual(T.futo_osszeg(), 1.0)
        self.assertEqual(T.begyujt('teszt', hivo=hivo), 0)      # újrafuttatás: nincs duplikátum
        self.assertEqual(len(T.jsonl_olvas(T.ut('valaszok.jsonl'))), 1)


def futtat():
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if res.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(futtat())
