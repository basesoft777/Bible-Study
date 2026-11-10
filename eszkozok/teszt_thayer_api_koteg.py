#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eszkozok/thayer_api_koteg.py önállóan (hálózat és kulcs nélkül, hamis hívóval).

    python eszkozok/teszt_thayer_api_koteg.py
"""

import json
import os
import re
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
            # F187 (N-F186g): tagsor-biztos — csak az `sz<n>` alakú, nem `elavult` sor (a `sz<n>~<m>` tagsor nem)
            if r['szotar'] == 'Thayer' and r['strong'] == strong and re.fullmatch(r'sz\d+', r['jelentes_szam'])
            and r.get('allapot') != 'elavult']


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
        self.regi = (T.MUNKA, T.PLAFON_USD, E.KISNAGYBETU_UT, T.EFFORT, T.ELOZO_KIADAS_USD, T.SZUKIT)
        T.MUNKA = tempfile.mkdtemp()
        E.KISNAGYBETU_UT = os.path.join(tempfile.mkdtemp(), 'kisnagybetu.tsv')      # a repó naplója nem módosul

    def tearDown(self):
        T.MUNKA, T.PLAFON_USD, E.KISNAGYBETU_UT, T.EFFORT, T.ELOZO_KIADAS_USD, T.SZUKIT = self.regi


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

    def _kesz_valasz(self):
        _, valasz = hamis_valasz(STRONG, hu_sorok(STRONG))
        rek = {'custom_id': 'G1941-c1-p1', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn', 'usage': {},
               'hiba': '', 'batch_id': 'b', 'szoveg': json.dumps({'forditas_hu': valasz}, ensure_ascii=False)}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [rek])
        T.kapuz([STRONG])

    def test_rogzit_a_tobbi_sort_bajtra_megtartja(self):
        munka = os.path.join(T.MUNKA, 'munka.tsv')
        egyeb = 'Thayer\tG0099\tG99\tsz1\tforditas_hu\tabc\tx\tsonnet\tm\t2026.10.01\tv3\t'
        regi = 'Thayer\tG1941\tG1941\tsz1\tforditas_hu\tregiertek\tx\tsonnet\tm\td\tv\t'
        with open(munka, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(['# megjegyzés', '\t'.join(F.FEJLEC), egyeb, regi]) + '\n')
        self._kesz_valasz()
        T.rogzit([STRONG], datum='2026.11.02', munka_ut=munka, bukott_ut=os.path.join(T.MUNKA, 'b.tsv'))
        sorok = open(munka, encoding='utf-8').read().split('\n')
        self.assertEqual(sorok[:3], ['# megjegyzés', '\t'.join(F.FEJLEC), egyeb])
        self.assertEqual(len(sorok), 3 + 7 + 1)
        self.assertNotIn('regiertek', '\n'.join(sorok))

    def test_atmeneti_hiba_javitando_refusal_bukott(self):
        base = {'custom_id': 'G1941-c1-p1', 'modell': 'claude-sonnet-5-5', 'usage': {}, 'szoveg': '', 'batch_id': 'b'}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [dict(base, tipus='errored', stop=None, hiba='{"type":"overloaded"}')])
        T.kapuz([STRONG])
        self.assertEqual(T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))[0]['allapot'], 'javitando')
        T.MUNKA = tempfile.mkdtemp()
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [dict(base, tipus='succeeded', stop='refusal', hiba='')])
        T.kapuz([STRONG])
        self.assertEqual(T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))[0]['allapot'], 'kapuhiba')

    def test_bukott_sor_nem_duplazodik(self):
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [
            {'custom_id': 'G1941-c1-p%d' % p, 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn',
             'usage': {}, 'hiba': '', 'batch_id': 'b', 'szoveg': 'nem json'} for p in (1, 2)])
        T.kapuz([STRONG])
        bukott = os.path.join(T.MUNKA, 'bukott.tsv')
        for _ in range(2):
            T.rogzit([STRONG], datum='2026.11.02', munka_ut=os.path.join(T.MUNKA, 'm.tsv'), bukott_ut=bukott)
        self.assertEqual(len([x for x in open(bukott, encoding='utf-8') if x.strip()]), 2)      # fejléc + 1 sor

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


B_STRONGOK = ['G0540', 'G1944', 'G0086']      # kész sonnet szakaszos fordítások: kicsi, kicsi, közepes


def b_hamis_valasz(strongok, hianyzo=()):
    """A B-kérés várt nyers válasza: Strongonként egy objektum (a hianyzo Strongok kimaradnak) -> (JSON-tömb, {strong: végleges})."""
    tomb, fin_ok = [], {}
    for s in strongok:
        fin, valasz = hamis_valasz(s, hu_sorok(s))
        fin_ok[s] = fin
        if s not in hianyzo:
            tomb.append({'strong': s, 'forditas_hu': valasz, 'bizonytalan_feloldasok': []})
    return json.dumps(tomb, ensure_ascii=False), fin_ok


class BUt(Alap):
    def test_kategoria_es_csoportositas(self):
        ix = T.konnyu_index(B_STRONGOK + ['G2532', 'G4151'])
        self.assertEqual([T.kategoria(ix[s]) for s in B_STRONGOK], ['kicsi', 'kicsi', 'kozepes'])
        self.assertEqual(T.kategoria(ix['G2532']), 'nagy')
        self.assertEqual(T.kategoria(ix['G4151']), 'nagy')      # többcsoportos
        cs, egyedi = T.b_csoportok_epit(B_STRONGOK + ['G2532', 'G4151'], ix)
        self.assertEqual(cs, {'B001': B_STRONGOK})
        self.assertEqual(egyedi, ['G2532', 'G4151'])
        cs, _ = T.b_csoportok_epit(B_STRONGOK, ix, b_db=2)      # a Strong-szám korlát
        self.assertEqual(cs, {'B001': B_STRONGOK[:2], 'B002': B_STRONGOK[2:]})
        cs, _ = T.b_csoportok_epit(B_STRONGOK, ix, b_kar=1000)      # a forráskarakter-korlát (222 + 345 + 1786)
        self.assertEqual(cs, {'B001': B_STRONGOK[:2], 'B002': B_STRONGOK[2:]})

    def test_b_prompt_strongonkenti_resze_bajtra_azonos_az_egy_strongossal(self):
        ks = [T.kerelmek_strongra(s)[0] for s in B_STRONGOK]
        p = T.b_prompt(ks)
        for i, k in enumerate(ks):
            egy = k['prompt']
            c = egy.rfind(T.BEMENET_JEL)
            resz = egy[c + len(T.BEMENET_JEL):egy.index(T.KIMENET_JEL, c)].strip('\n')
            self.assertEqual(T.b_strong_blokk(k, i, len(ks)), '### %d/%d. szócikk\n%s' % (i + 1, len(ks), resz))
            self.assertIn(resz, p)
            self.assertEqual(p.count(resz), 1)
        # a szabály-rész egyszer áll, a példapár és a séma is
        self.assertEqual(p.count('## Kiegészítő szabály (v5.1) — Thayer-szócikk'), 1)
        self.assertEqual(p.count('## Példapár'), 1)
        self.assertEqual(p.count(T.BEMENET_JEL + '\n'), 1)
        # a kötelező-alak lista az egyes Strongok listáinak uniója
        for k in ks:
            for sor in k['kot'].split('\n'):
                if sor.startswith('- '):
                    self.assertIn(sor, p)
        # a szabálytartalom ugyanabból a prompt_epit-ből: a nem szűkített elejéig bájtra azonos
        j = ks[0]['prompt'].index(T.KOT_JEL) + len(T.KOT_JEL)      # a kötelező-alak listáig (az unió) bájtra azonos
        self.assertEqual(p[:j], ks[0]['prompt'][:j])

    def test_szukites_pontos_sorhalmaz(self):
        ks = [T.kerelmek_strongra(s)[0] for s in B_STRONGOK]
        forrasok = [k['nezet'] for k in ks]
        term, karoli = T.szukitett_tablak(forrasok)
        egy = '\n'.join(forrasok)
        bent = set(term.split('\n'))
        for angol, sor in T.term_sorok():
            talalt = bool(T.K._angol_minta(angol).search(egy))
            self.assertEqual(sor in bent, talalt, angol)
        for alakok, sor in T.karoli_sorok():
            talalt = any(T._alak_minta(a).search(egy) for a in alakok)
            self.assertEqual(sor in set(karoli.split('\n')), talalt, sor)
        # a kötelező alakok (az 5. kapu kulcsai) mind a szűkített táblában vannak
        for k in ks:
            for sor in k['kot'].split('\n'):
                if sor.startswith('- '):
                    angol = sor[3:sor.index('`', 3)]
                    self.assertTrue(any(t == angol and s in bent for t, s in T.term_sorok()), angol)
        # a teljes táblák sorai betűre azonosak az emeles-éval
        self.assertEqual('\n'.join(s for _, s in T.term_sorok()), E.terminologia_szoveg()[0])
        self.assertEqual('\n'.join(s for _, s in T.karoli_sorok()), E.karoli_szoveg())

    def test_szukitett_prompt_csak_a_ket_tablaban_ter_el(self):
        k = T.kerelmek_strongra('G0086')[0]
        nar = T.szukit(k['prompt'], [k['nezet']])
        self.assertLess(len(nar), len(k['prompt']))
        a, b = k['prompt'].index(T.TERM_FEJ), k['prompt'].index('\n\n' + T.BEMENET_JEL)
        self.assertEqual(nar[:a], k['prompt'][:a])
        self.assertEqual(nar[nar.index('\n\n' + T.BEMENET_JEL):], k['prompt'][b:])
        self.assertLess(T.allando_kar(nar), T.allando_kar(k['prompt']))
        T.SZUKIT = False
        try:
            self.assertEqual(T.kuldendo_prompt(k), k['prompt'])
        finally:
            T.SZUKIT = True

    def test_visszabontas_es_kapuk_strongonkent(self):
        valasz, fin_ok = b_hamis_valasz(B_STRONGOK)
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), [])
        os.makedirs(T.MUNKA, exist_ok=True)
        with open(T.ut('b_csoportok.json'), 'w', encoding='utf-8') as f:
            json.dump({'B001': B_STRONGOK, 'egyedi': []}, f)
        rek = {'custom_id': 'B001-p1', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn',
               'usage': {'input_tokens': 5, 'output_tokens': 5}, 'szoveg': valasz, 'hiba': '', 'batch_id': 'b'}
        bontott = T.b_szetbont(rek)
        self.assertEqual([r['custom_id'] for r in bontott], ['%s-c1-p1' % s for s in B_STRONGOK])
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), bontott)
        self.assertEqual(T.kapuz(B_STRONGOK), 0)
        eredm = {r['strong']: r for r in T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))}
        for s in B_STRONGOK:
            self.assertEqual(eredm[s]['allapot'], 'kesz', (s, eredm[s]['hibak']))
            self.assertEqual(eredm[s]['vegleges'], fin_ok[s])      # betűhű visszaállítás Strongonként

    def _b_kapu(self, valasz):
        os.makedirs(T.MUNKA, exist_ok=True)
        with open(T.ut('b_csoportok.json'), 'w', encoding='utf-8') as f:
            json.dump({'B001': B_STRONGOK, 'egyedi': []}, f)
        rek = {'custom_id': 'B001-p1', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn',
               'usage': {}, 'szoveg': valasz, 'hiba': '', 'batch_id': 'b'}
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), T.b_szetbont(rek))
        T.kapuz(B_STRONGOK)
        return {r['strong']: r for r in T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))}

    def test_hianyzo_strong_javitando_es_csoportosan_javul(self):
        """F07 M0 (b): a B-válaszból hiányzó kicsi/közepes Strong friss kérésként, B-javító (J001-p2) kérésben megy újra."""
        valasz, _ = b_hamis_valasz(B_STRONGOK, hianyzo=('G1944',))
        eredm = self._b_kapu(valasz)
        self.assertEqual([eredm[s]['allapot'] for s in B_STRONGOK], ['kesz', 'javitando', 'kesz'])
        hivott = []

        def hivo(m, ut, torzs=None, nyers=False):
            hivott.append(torzs)
            return {'id': 'msgbatch_j'}
        self.assertEqual(T.javit(B_STRONGOK, 'teszt', 50.0, hivo=hivo), 0)
        kerelmek = hivott[0]['requests']
        self.assertEqual([k['custom_id'] for k in kerelmek], ['J001-p2'])
        msgs = kerelmek[0]['params']['messages']
        self.assertEqual([m['role'] for m in msgs], ['user'])      # egyetlen felhasználói forduló: a kimenet nem megy kétszer
        szoveg = msgs[0]['content'][0]['text']
        self.assertIn('nem érkezett használható válasz', szoveg)
        self.assertNotIn('Az előző kísérlet kimenete', szoveg)      # nincs mit megjavítani
        self.assertEqual(json.load(open(T.ut('bj_csoportok.json'), encoding='utf-8')), {'J001': ['G1944']})
        # a már beküldött javító kérés nem megy újra
        self.assertEqual(T.javit(B_STRONGOK, 'teszt', 50.0, hivo=hivo), 0)
        self.assertEqual(len(hivott), 1)

    def test_b_javito_kerelem_strongonkenti_resze_bajtra_a_vart(self):
        valasz, _ = b_hamis_valasz(B_STRONGOK)
        tomb = json.loads(valasz)
        tomb[0]['forditas_hu'] = tomb[0]['forditas_hu'].replace('⟦1⟧', '')      # helyőrző-hiba: a kapu előtt bukik
        eredm = self._b_kapu(json.dumps(tomb, ensure_ascii=False))
        r = eredm[B_STRONGOK[0]]
        self.assertEqual(r['allapot'], 'javitando')
        ks = [T.kerelmek_strongra(s)[0] for s in (B_STRONGOK[0], B_STRONGOK[1])]
        p = T.b_prompt(ks, [(r['nyers'][0], r['hibak']), ('', [])])
        resz = ('\n\n#### Az előző kísérlet kimenete erre a szócikkre\n\n```json\n%s\n```\n\n#### Javítandó\n\n%s'
                % (r['nyers'][0].strip(), T.javito_resz(r['hibak'])))
        self.assertIn(T.b_strong_blokk(ks[0], 0, 2) + resz, p)      # a hibaüzenet bájtra ott áll, ahol várjuk
        self.assertIn('helyőrző', T.javito_resz(r['hibak']))
        self.assertEqual(p.count('## Példapár'), 1)      # a szabály-rész egyszer áll
        self.assertNotIn(' Add vissza', T.javito_resz(r['hibak']))

    def test_b_javito_visszabontas_es_kapuzas_strongonkent(self):
        valasz, fin_ok = b_hamis_valasz(B_STRONGOK, hianyzo=('G1944',))
        self._b_kapu(valasz)

        def hivo(m, ut, torzs=None, nyers=False):
            return {'id': 'msgbatch_j'}
        T.javit(B_STRONGOK, 'teszt', 50.0, hivo=hivo)
        javitott, _ = b_hamis_valasz(['G1944'])
        rek = {'custom_id': 'J001-p2', 'tipus': 'succeeded', 'modell': 'claude-sonnet-5-5', 'stop': 'end_turn', 'usage': {},
               'szoveg': javitott, 'hiba': '', 'batch_id': 'j'}
        bontott = T.b_szetbont(rek)
        self.assertEqual([r['custom_id'] for r in bontott], ['G1944-c1-p2'])
        T.jsonl_hozzaad(T.ut('valaszok.jsonl'), bontott)
        T.kapuz(B_STRONGOK)
        eredm = {r['strong']: r for r in T.jsonl_olvas(T.ut('kapu_eredmeny.jsonl'))}
        self.assertEqual((eredm['G1944']['allapot'], eredm['G1944']['proba']), ('kesz', 2))
        self.assertEqual(eredm['G1944']['vegleges'], fin_ok['G1944'])

    def test_b_javito_plafon_mert_futo_osszeggel(self):
        valasz, _ = b_hamis_valasz(B_STRONGOK, hianyzo=('G1944',))
        self._b_kapu(valasz)
        T.AK.tsv_hozzaad(T.ut('futasnaplo.tsv'), T.NAPLO_FEJLEC, {'ts': 'x', 'custom_id': 'B000-p1', 'modell': 'm', 'effort': 'high',
                                                                 'bemenet_token': 1, 'cache_olvasas': 0, 'cache_iras': 0,
                                                                 'kimenet_token': 1, 'stop_reason': 'end_turn',
                                                                 'koltseg_usd': '3.500000', 'futo_osszeg_usd': '3.500000'})
        hivott = []

        def hivo(m, ut, torzs=None, nyers=False):
            hivott.append(torzs)
            return {'id': 'msgbatch_j'}
        self.assertEqual(T.javit(B_STRONGOK, 'teszt', 3.5, hivo=hivo), 3)      # a mért futó összeg már kitölti a plafont
        self.assertEqual(hivott, [])
        self.assertEqual(T.javit(B_STRONGOK, 'teszt', 0.0, hivo=hivo), 3)
        self.assertEqual(T.javit(B_STRONGOK, 'teszt', 50.0, hivo=hivo), 0)

    def test_nagy_strong_javitasa_egyenkent_marad(self):
        """A nagy / többcsoportos Strong javító köre egyenként, az előző válasz assistant-fordulóként."""
        r = {'strong': 'G4151', 'proba': 1, 'allapot': 'javitando', 'nyers': ['{"strong": "G4151"}', 'x', 'y'], 'hibak': ['8_idezojel: x']}
        kerelmek, tetelek, bj = T.javito_kerelmek([r], ['G4151'])
        self.assertEqual([x['custom_id'] for x in kerelmek], ['G4151-c1-p2', 'G4151-c2-p2', 'G4151-c3-p2'])
        self.assertEqual([m['role'] for m in kerelmek[0]['params']['messages']], ['user', 'assistant', 'user'])
        self.assertEqual(bj, {})
        self.assertEqual({t[0] for t in tetelek}, {'A'})

    def test_max_tokens_kimenet_egy_b_batch_mar_nem_ad_semmit(self):
        rek = {'custom_id': 'B001-p1', 'tipus': 'succeeded', 'modell': 'm', 'stop': 'max_tokens', 'usage': {},
               'szoveg': '[{"strong": "G0540"}]', 'hiba': '', 'batch_id': 'b'}
        os.makedirs(T.MUNKA, exist_ok=True)
        with open(T.ut('b_csoportok.json'), 'w', encoding='utf-8') as f:
            json.dump({'B001': B_STRONGOK, 'egyedi': []}, f)
        self.assertEqual({r['szoveg'] for r in T.b_szetbont(rek)}, {''})

    def test_kalibralt_becslo(self):
        be, ki, usd = T.becsles_adat(0, 0, 0)
        self.assertEqual((be, ki, usd), (0, 0, 0))
        be, ki, usd = T.becsles_adat(T.ALLANDO_REF_KAR, 1000, 1)
        self.assertAlmostEqual(be, 17136 + 3.721 * 1000, delta=1)      # az F27 M1 illesztése, szűkítés nélkül
        self.assertAlmostEqual(ki, 1134 + 1.654 * 1000, delta=1)
        self.assertAlmostEqual(usd, (be * 1.0 + ki * 5.0) / 1e6)
        # a B-kérésben az állandó rész egyszer, a kimenet Strongonkénti állandója n-szer számít
        be20, ki20, _ = T.becsles_adat(T.ALLANDO_REF_KAR, 20000, 20)
        self.assertAlmostEqual(be20, 17136 + 3.721 * 20000, delta=1)
        self.assertAlmostEqual(ki20, 20 * 1134 + 1.654 * 20000, delta=1)

    def test_b_becslo_effortonkent_es_javito_kor(self):
        """F07 M0 (a): a B-kérés saját együtthatói, effortonként külön kimenettel; a javító kör a mért aránnyal."""
        be, ki_h, usd_h = T.becsles_adat(21084, 10000, 20, 'B', 'high')
        _, ki_m, usd_m = T.becsles_adat(21084, 10000, 20, 'B', 'medium')
        self.assertAlmostEqual(be, 0.684 * 21084 + 3.178 * 10000, delta=1)
        self.assertAlmostEqual(ki_h, 19590, delta=1)
        self.assertAlmostEqual(ki_m, 15207, delta=1)
        self.assertLess(usd_m, usd_h)
        # az effort-érzéketlen alap nem változott: az A-út 'high' értéke az F27 M1 illesztése
        self.assertEqual(T.becsles_adat(T.ALLANDO_REF_KAR, 1000, 1, 'A', 'high'), T.becsles_adat(T.ALLANDO_REF_KAR, 1000, 1))
        self.assertLess(T.becsles_adat(T.ALLANDO_REF_KAR, 1000, 1, 'A', 'medium')[1], T.becsles_adat(T.ALLANDO_REF_KAR, 1000, 1)[1])
        self.assertAlmostEqual(T.javito_kor_becsles(2.0, 'B'), 2.0 * T.JAVITO_ARANY['B'])
        self.assertGreater(T.JAVITO_ARANY['A'], T.JAVITO_ARANY['B'])

    def test_mero_adag_becslese_a_mert_koltseg_kozeleben(self):
        """A #159 mérő B-kéréseinek becslése az újraillesztett együtthatókkal: a mért 0,4983 (high) / 0,4072 (medium) USD ±5%."""
        for effort, mert in (('high', 0.4983), ('medium', 0.4072)):
            usd = 0.0
            for allando, kar, db in ((18591, 2353, 13), (21476, 9438, 20), (19713, 6094, 20), (24557, 14833, 7)):
                usd += T.becsles_adat(allando, kar, db, 'B', effort)[2]
            self.assertAlmostEqual(usd / mert, 1.0, delta=0.05, msg=effort)

    def test_plafon_mert_futo_osszeggel(self):
        hivott = []

        def hivo(m, ut, torzs=None, nyers=False):
            hivott.append(torzs)
            return {'id': 'msgbatch_b'}
        becs = T.becsles_adat(26000, 2553, 3)[2]      # nagyságrend: a B001 becslése
        self.assertEqual(T.b_bekuld(B_STRONGOK, 'teszt', 0, 0.0, hivo=hivo), 3)      # 0 plafon: nincs beküldés
        self.assertEqual(hivott, [])
        # a mért futó összeg beleszámít: a plafon a becslés fölött van, de a mért összeggel együtt alatta
        os.makedirs(T.MUNKA, exist_ok=True)
        AKt = T.AK
        AKt.tsv_hozzaad(T.ut('futasnaplo.tsv'), T.NAPLO_FEJLEC, {'ts': 'x', 'custom_id': 'B000-p1', 'modell': 'm', 'effort': 'high',
                                                                 'bemenet_token': 1, 'cache_olvasas': 0, 'cache_iras': 0,
                                                                 'kimenet_token': 1, 'stop_reason': 'end_turn',
                                                                 'koltseg_usd': '3.500000', 'futo_osszeg_usd': '3.500000'})
        self.assertAlmostEqual(T.futo_osszeg(), 3.5)
        self.assertEqual(T.b_bekuld(B_STRONGOK, 'teszt', 0, 3.5 + becs / 2, hivo=hivo), 3)
        self.assertEqual(hivott, [])
        T.ELOZO_KIADAS_USD = 1.0      # a másik adag mért költsége is a közös plafonba számít
        try:
            self.assertEqual(T.b_bekuld(B_STRONGOK, 'teszt', 0, 3.5 + becs * 1.5, hivo=hivo), 3)
            self.assertEqual(hivott, [])
            T.ELOZO_KIADAS_USD = 0.0
            self.assertEqual(T.b_bekuld(B_STRONGOK, 'teszt', 0, 3.5 + becs * 1.5, hivo=hivo), 0)
        finally:
            T.ELOZO_KIADAS_USD = 0.0
        kerelmek = hivott[0]['requests']
        self.assertEqual([k['custom_id'] for k in kerelmek], ['B001-p1'])
        self.assertEqual(kerelmek[0]['params']['output_config'], {'effort': 'high'})
        # a függő (be nem gyűjtött) batch becslése is számít: a második beküldés már nem szabad
        self.assertGreater(T.fuggo_becsles(), 0)
        self.assertEqual(T.b_bekuld(B_STRONGOK, 'teszt', 0, 100.0, hivo=hivo), 0)      # minden B-csoport be van küldve
        self.assertEqual(len(hivott), 1)

    def test_bekuld_a_b_utan_nem_kuldi_ujra_a_b_strongokat(self):
        hivott = []

        def hivo(m, ut, torzs=None, nyers=False):
            hivott.append(torzs)
            return {'id': 'msgbatch_%d' % len(hivott)}
        self.assertEqual(T.b_bekuld(B_STRONGOK, 'teszt', 0, 50.0, hivo=hivo), 0)
        lista = B_STRONGOK + ['G1941']      # a nagy Strong egyenként, a `bekuld`-del
        self.assertEqual(T.bekuld(lista, 'teszt', 50.0, hivo=hivo), 0)
        self.assertEqual([k['custom_id'] for k in hivott[1]['requests']], ['G1941-c1-p1'])
        self.assertEqual(T.bekuld(lista, 'teszt', 50.0, hivo=hivo), 0)      # minden be van küldve
        self.assertEqual(len(hivott), 2)
        self.assertTrue(os.path.exists(T.ut('csomag_01.txt')) and os.path.exists(T.ut('csomag_B001.txt')))

    def test_begyujtve_jelolo_nem_irodik_felul(self):
        os.makedirs(T.MUNKA, exist_ok=True)
        with open(T.ut('b_csoportok.json'), 'w', encoding='utf-8') as f:
            json.dump({'B001': B_STRONGOK[:2], 'egyedi': []}, f)
        T.ujra_naplo('msgbatch_b', 'teszt', 1, 'B:B001-B001', 1)
        valasz, _ = b_hamis_valasz(B_STRONGOK[:2])
        eredmeny = {'custom_id': 'B001-p1', 'result': {'type': 'succeeded', 'message': {
            'model': 'claude-sonnet-5-5', 'stop_reason': 'end_turn', 'usage': {'input_tokens': 10, 'output_tokens': 10},
            'content': [{'type': 'text', 'text': valasz}]}}}

        def hivo(m, ut, torzs=None, nyers=False):
            return json.dumps(eredmeny) + '\n' if nyers else {'processing_status': 'ended', 'results_url': 'http://x/r'}
        T.begyujt('teszt', hivo=hivo)
        T.begyujt('teszt', hivo=hivo)
        with open(T.ut('begyujtve_msgbatch_b.txt'), encoding='utf-8') as f:
            self.assertEqual(f.read().strip(), '3')

    def test_effort_a_kereseben(self):
        regi = T.EFFORT
        T.EFFORT = 'medium'
        try:
            p = T.kerelem_params([{'role': 'user', 'content': 'x'}], 100)
        finally:
            T.EFFORT = regi
        self.assertEqual(p['output_config'], {'effort': 'medium'})
        self.assertEqual(p['thinking'], {'type': 'adaptive'})

    def test_begyujt_b_batch(self):
        os.makedirs(T.MUNKA, exist_ok=True)
        with open(T.ut('b_csoportok.json'), 'w', encoding='utf-8') as f:
            json.dump({'B001': B_STRONGOK[:2], 'egyedi': []}, f)
        T.ujra_naplo('msgbatch_b', 'teszt', 1, 'B:B001-B001', 1)
        valasz, _ = b_hamis_valasz(B_STRONGOK[:2])
        eredmeny = {'custom_id': 'B001-p1', 'result': {'type': 'succeeded', 'message': {
            'model': 'claude-sonnet-5-5', 'stop_reason': 'end_turn', 'usage': {'input_tokens': 1000000, 'output_tokens': 0},
            'content': [{'type': 'text', 'text': valasz}]}}}

        def hivo(m, ut, torzs=None, nyers=False):
            if nyers:
                return json.dumps(eredmeny) + '\n'
            return {'processing_status': 'ended', 'results_url': 'http://x/r'}
        self.assertEqual(T.begyujt('teszt', hivo=hivo), 0)
        cidek = [r['custom_id'] for r in T.jsonl_olvas(T.ut('valaszok.jsonl'))]
        self.assertEqual(cidek, ['B001-p1', 'G0540-c1-p1', 'G1944-c1-p1'])
        self.assertAlmostEqual(T.futo_osszeg(), 1.0)      # a költség a B-kérésen, egyszer számít
        self.assertTrue(os.path.exists(T.ut('begyujtve_msgbatch_b.txt')))
        self.assertEqual(T.begyujt('teszt', hivo=hivo), 0)
        self.assertEqual(len(T.jsonl_olvas(T.ut('valaszok.jsonl'))), 3)


def futtat():
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if res.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(futtat())
