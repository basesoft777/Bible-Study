#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_glossza_api_koteg.py -- F161: a glossza-lánc tesztje. A `szaraz` determinisztikus és a `bekuld` bájtra
ugyanazt küldi; a kapuk elkapják a tipikus hibákat (angol maradék, hiányzó helyőrző, elemszám, belső jel, egyenes
idézőjel, terminológia); a teljes út (bevesz → kapuz → javit → rogzit → beir) a meglévő sort nem rontja. Hálózat nélkül;
a munkakönyvtár és a forditasok.tsv-másolat ideiglenes könyvtárban.

    python eszkozok/teszt_glossza_api_koteg.py
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
import glossza_api_koteg as L  # noqa: E402
import glossza_lexikon_forditas as GLF  # noqa: E402

LISTA_FEJ = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forras_hossz', 'allapot', 'forrasszoveg']
# két valódi egység (a konkordancia mai adataiból oldódik fel) és egy, amely nem tartozik a lánchoz
KULCSOK = [('UBS_DNTG', 'G4151', '004054001003000', '12.37', 'glosszak_hu'),
           ('TBESG', 'G0444', 'G0444', 'rovid', 'glosszak_hu')]
IDEGEN = ('Thayer', 'G4151', 'G4151', '2', 'forditas_hu')


def lista_ir(ut, kulcsok=KULCSOK, hash_ront=False):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(LISTA_FEJ) + '\n')
        for k in kulcsok:
            forras = GLF.forras_szoveg(dict(zip(LISTA_FEJ, k)))
            h = GLF.sha1(forras) if not hash_ront else '0' * 40
            f.write('\t'.join(list(k) + [h, str(len(forras)), 'hianyzik', forras]) + '\n')
        f.write('\t'.join(list(IDEGEN) + ['', '', 'nincs_forras', '']) + '\n')


def egyseg(forras, mezo='glosszak_hu', szotar='UBS_DNTG', strong='G4151'):
    bont, hely = L.E.helyorzo_bont(forras)
    return {'szotar': szotar, 'strong': strong, 'entry_id': 'x', 'jelentes_szam': '12.37', 'mezo': mezo, 'forras': forras,
            'forras_hely': bont, 'helyorzok': hely}


def bukott_kapuk(e, hu):
    return [n for n, er, _ in L.egyseg_kapuk(e, hu, [])[2] if er == 'SERTES']


class Alap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='F161_teszt_')
        self.lista = os.path.join(self.tmp, 'lista.tsv')
        lista_ir(self.lista)
        L.munka_beallit(os.path.join(self.tmp, 'munka'))
        L._CTX.clear()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class Feloldo(unittest.TestCase):
    def test_tbesg_rovid_feloldva(self):
        # a #121 lista eddig a TBESG-et `nincs_forras`-ként hagyta; a közös feloldó a 13. szabályé (tovabbi_forras)
        self.assertEqual(GLF.forras_szoveg(dict(zip(LISTA_FEJ, KULCSOK[1]))), 'a human')

    def test_dntg_es_ismeretlen(self):
        self.assertEqual(GLF.forras_szoveg(dict(zip(LISTA_FEJ, KULCSOK[0]))), 'demon; evil spirit')
        self.assertIsNone(GLF.forras_szoveg(dict(zip(LISTA_FEJ, IDEGEN))))


class Szaraz(Alap):
    def test_determinisztikus_es_bajtra_azonos(self):
        L.szaraz(self.lista)
        with open(L.ut('keresek.jsonl'), encoding='utf-8') as f:
            elso = f.read()
        L._CTX.clear()
        L.munka_beallit(os.path.join(self.tmp, 'munka2'))
        L.szaraz(self.lista)
        with open(L.ut('keresek.jsonl'), encoding='utf-8') as f:
            self.assertEqual(f.read(), elso)
        ker = [json.loads(s) for s in elso.splitlines()]
        self.assertEqual([k['custom_id'] for k in ker], ['G001-p1'])
        szoveg = ker[0]['params']['messages'][0]['content'][0]['text']
        self.assertIn('Fordítandó (angol): demon; evil spirit', szoveg)
        self.assertIn('Fordítandó (angol): a human', szoveg)
        self.assertNotIn('{{', szoveg)
        self.assertIn('`spirit` → `szellem`', szoveg)          # mankó: kötelező terminológia

        # a bekuld pontosan a fájl kéréseit küldi
        kuldott = {}

        def hivo(m, ut, torzs=None, nyers=False):
            kuldott['torzs'] = torzs
            return {'id': 'msgbatch_teszt'}
        self.assertEqual(L.bekuld(1, 1.0, hivo=hivo), 0)
        self.assertEqual(L.jsonl_szoveg(kuldott['torzs']['requests']), elso)
        self.assertEqual(L.bekuld(1, 1.0, hivo=hivo), 0)                    # másodszor nincs mit küldeni

    def test_prompt_ki_szo_szerint(self):
        L.szaraz(self.lista)
        ki = os.path.join(self.tmp, 'p.txt')
        L.prompt_ki('G001-p1', ki)
        with open(ki, encoding='utf-8') as f:
            self.assertEqual(f.read(), L.kerelmek_be(1)[0][0]['params']['messages'][0]['content'][0]['text'])

    def test_plafon_nelkul_tilos_es_eltero_keres(self):
        L.szaraz(self.lista)
        self.assertEqual(L.bekuld(1, 0.0, hivo=lambda *a, **k: self.fail('nem hívhat')), 3)
        with open(L.ut('keresek.jsonl'), 'a', encoding='utf-8') as f:
            f.write('\n')
        self.assertEqual(L.bekuld(1, 1.0, hivo=lambda *a, **k: self.fail('nem hívhat')), 2)

    def test_tbesg_csak_rovid(self):
        lista_ir(self.lista, kulcsok=KULCSOK + [('TBESG', 'G1941', 'G1941', 'teljes', 'forditas_hu')])
        self.assertEqual([(e['szotar'], e['jelentes_szam']) for e in L.egysegek_listabol(self.lista)],
                         [('UBS_DNTG', '12.37'), ('TBESG', 'rovid')])

    def test_elavult_lista_megall(self):
        lista_ir(self.lista, hash_ront=True)
        with self.assertRaises(SystemExit):
            L.szaraz(self.lista)

    def test_munka_a_repoban_tilos(self):
        with self.assertRaises(SystemExit):
            L.munka_beallit(os.path.join(L.ROOT, 'naplok', 'munka'))

    def test_csoportositas(self):
        egys = [{'szotar': 'UBS_DNTG', 'strong': 'G%04d' % (i // 7), 'id': i} for i in range(30)]
        cs = L.keresekre(egys, db=10)
        self.assertTrue(all(len(c) <= 10 for c in cs))
        self.assertEqual(sum(len(c) for c in cs), 30)
        self.assertEqual([e['id'] for c in cs for e in c], list(range(30)))


class Kapuk(unittest.TestCase):
    def test_jo_forditas_atmegy(self):
        e = egyseg('demon; evil spirit')
        v, _, er, ok = L.egyseg_kapuk(e, 'démon; gonosz szellem', [])
        self.assertTrue(ok, er)
        self.assertEqual(v, 'démon; gonosz szellem')

    def test_angol_maradek(self):
        e = egyseg('demon; evil spirit')
        self.assertIn('G2_angol', bukott_kapuk(e, 'démon; evil szellem'))       # a forrás szava
        self.assertIn('G2_angol', bukott_kapuk(e, 'the démon; gonosz szellem'))  # angol funkciószó

    def test_helyorzo(self):
        e = egyseg('ψυχή; living being', strong='G5590')
        self.assertIn('0_helyorzo', bukott_kapuk(e, 'lélek; élőlény'))
        v, _, er, ok = L.egyseg_kapuk(e, '⟦1⟧; élőlény', [])
        self.assertTrue(ok, er)
        self.assertEqual(v, 'ψυχή; élőlény')
        self.assertIn('0_helyorzo', bukott_kapuk(e, '⟦1⟧; ⟦1⟧ élőlény'))

    def test_elemszam(self):
        e = egyseg('wind; blowing; to blow')
        self.assertIn('G1_elemszam', bukott_kapuk(e, 'szél; fújni'))
        self.assertNotIn('G1_elemszam', bukott_kapuk(e, 'szél; fújás; fújni'))

    def test_belso_jel_es_idezojel(self):
        e = egyseg('ghost')
        self.assertIn('G3_belso', bukott_kapuk(e, 'kísértet (DT123)'))
        self.assertIn('G4_egyenes_idezojel', bukott_kapuk(e, '"kísértet"'))

    def test_terminologia(self):
        e = egyseg('demon; evil spirit')
        self.assertIn('5_terminologia', bukott_kapuk(e, 'démon; gonosz lélek'))

    def test_ubs_definicio_jelek_es_jeloles(self):
        e = egyseg('= fortified town; ◄ territory of {L:Naphtali<SDBH:נַפְתָּלִי>}', mezo='definicio_hu', szotar='UBS_DBH',
                   strong='H7152')
        v, _, er, ok = L.egyseg_kapuk(e, '= megerősített város; ◄ {L:Naphtali<SDBH:⟦1⟧>} területe', [])
        self.assertTrue(ok, er)                                                   # a jelölésben álló név nem angol maradék
        self.assertIn('{L:Naphtali<SDBH:נַפְתָּלִי>}', v)
        self.assertIn('G5_ubs_jelek', bukott_kapuk(e, '= megerősített város; {L:Naphtali<SDBH:⟦1⟧>} területe'))
        self.assertIn('G5_ubs_jelek', bukott_kapuk(e, '= megerősített város; ◄ {L:Naftáli<SDBH:⟦1⟧>} területe'))
        self.assertNotIn('G1_elemszam', [n for n, _, _ in er])                  # definíciónál nincs elemszám-kapu

    def test_tulajdonnev_es_gerinc_nem_hamis_pozitiv(self):
        e = egyseg('Simon; Anna')
        self.assertNotIn('G2_angol', bukott_kapuk(e, 'Simon; Anna'))
        e = egyseg('= the bone extending from the backbone', mezo='definicio_hu', szotar='UBS_DBH', strong='H2180')
        self.assertNotIn('G3_belso', bukott_kapuk(e, '= a gerinctől kiinduló csont'))

    def test_ures_es_sortores(self):
        e = egyseg('ghost')
        self.assertEqual(bukott_kapuk(e, ''), ['0_json'])
        self.assertEqual(bukott_kapuk(e, 'kísértet\nszellem'), ['0_json'])

    def test_valasz_bont(self):
        d, h = L.valasz_bont('```json\n{"egysegek": [{"id": "e001", "forditas_hu": "démon", "bizonytalan_feloldasok": []}]}\n```')
        self.assertEqual(d, {'e001': ('démon', [])})
        self.assertEqual(h, '')
        d, h = L.valasz_bont('{"egysegek": [{"id": "e001", "forditas_hu": "a"}, {"id": "e001", "forditas_hu": "b"}]}')
        self.assertIn('kétszer', h)
        self.assertEqual(L.valasz_bont('nem json')[1], 'a válasz nem JSON-objektum')


class TeljesUt(Alap):
    def valasz(self, d):
        ut = os.path.join(self.tmp, 'v.json')
        with open(ut, 'w', encoding='utf-8') as f:
            json.dump({'egysegek': d}, f, ensure_ascii=False)
        return ut

    def test_bevesz_kapuz_javit_rogzit_beir(self):
        L.szaraz(self.lista)
        with self.assertRaises(SystemExit):
            L.bevesz('G001-p1', self.valasz([]), 'sonnet')                 # nem teljes modellnév
        L.bevesz('G001-p1', self.valasz([{'id': 'e001', 'forditas_hu': 'démon; evil spirit'},
                                         {'id': 'e002', 'forditas_hu': 'ember'}]), 'claude-sonnet-5-5')
        with self.assertRaises(SystemExit):
            L.bevesz('G001-p1', self.valasz([]), 'claude-sonnet-5-5')      # kétszer nem
        L.kapuz()
        v = L.vegso_allapot()
        self.assertFalse(v['e001']['atment'])
        self.assertTrue(v['e002']['atment'])
        L.javit()
        p2 = L.kerelmek_be(2)[0]
        self.assertEqual([k['custom_id'] for k in p2], ['G001-p2'])
        uz = p2[0]['params']['messages']
        self.assertEqual([m['role'] for m in uz], ['user'])                     # egyetlen user-üzenet: API-n és subagenttel azonos
        sz = uz[0]['content'][0]['text']
        self.assertIn('### e001' + chr(10), sz)
        self.assertNotIn('### e002' + chr(10), sz)                                     # csak a bukott egység
        self.assertIn('- e001: korábbi fordításod: démon; evil spirit', sz)
        ki = os.path.join(self.tmp, 'p2.txt')
        L.prompt_ki('G001-p2', ki)
        with open(ki, encoding='utf-8') as f:
            self.assertEqual(f.read(), sz)
        kuldott = {}

        def hivo(m, ut, torzs=None, nyers=False):
            kuldott['torzs'] = torzs
            return {'id': 'msgbatch_p2'}
        self.assertEqual(L.bekuld(2, 1.0, hivo=hivo), 0)                         # a 2. kör is bájtra ellenőrizve
        with open(L.ut('keresek_p2.jsonl'), encoding='utf-8') as f:
            self.assertEqual(L.jsonl_szoveg(kuldott['torzs']['requests']), f.read())
        L.bevesz('G001-p2', self.valasz([{'id': 'e001', 'forditas_hu': 'démon; gonosz szellem'}]), 'claude-sonnet-5-5')
        L.kapuz()
        v = L.vegso_allapot()
        self.assertTrue(v['e001']['atment'] and v['e001']['proba'] == 2)
        with self.assertRaises(SystemExit):
            L.javit()                                                          # legfeljebb egy javító kör
        L.rogzit(datum='2026.11.03')
        rog = L.tsv_be(L.ut('rogzitett.tsv'))
        self.assertEqual(len(rog), 2)
        self.assertTrue(all(r['allapot'] == 'sonnet' and r['modell'] == 'claude-sonnet-5-5' for r in rog))
        self.assertTrue(all(r['megjegyzes'].startswith('F161 (glossza-lánc, prompt %s' % L.PROMPT_VERZIO) and 'scope=' in r['megjegyzes']
                            and '| forras=' in r['megjegyzes'] and '| ts=' in r['megjegyzes'] for r in rog))

        # beírás egy másolatba: a meglévő sorok bájtra változatlanok, az új sorok a végén
        masolat = os.path.join(self.tmp, 'forditasok.tsv')
        shutil.copy(GLF.FORDITASOK, masolat)
        with open(masolat, encoding='utf-8', newline='') as f:
            elotte = f.read()
        jelzes = any(r['_manko'] for r in rog)
        if jelzes:
            with self.assertRaises(SystemExit):
                L.beir(forditasok_ut=masolat)
        self.assertEqual(L.beir(jelzes_atnezve=True, forditasok_ut=masolat), 2)
        with open(masolat, encoding='utf-8', newline='') as f:
            utana = f.read()
        e_sorok, u_sorok = elotte.split('\n'), utana.split('\n')
        uj = [s for s in u_sorok if s.endswith('ts=%s' % L.datetime.date.today().isoformat()) and s.startswith(('UBS_DNTG', 'TBESG'))]
        self.assertEqual(len(uj), 2)
        self.assertEqual([s for s in u_sorok if s not in uj], e_sorok)          # a többi sor bájtra és sorrendben változatlan
        self.assertEqual(u_sorok[-2], e_sorok[-2])                              # nem a tábla végére (ott más PR-ok fűznek)
        for s in uj:                                                            # a saját szótár-blokkjában áll
            i = u_sorok.index(s)
            self.assertEqual(u_sorok[i - 1].split('\t')[0], s.split('\t')[0])
        self.assertTrue(all(len(s.split('\t')) == len(L.FEJLEC) for s in uj))
        # ugyanaz másodszor: a kulcs már megvan — csak --felulir-ral
        with self.assertRaises(SystemExit):
            L.beir(jelzes_atnezve=True, forditasok_ut=masolat)
        # kezi sor védett
        with open(masolat, encoding='utf-8', newline='') as f:
            t = f.read()
        kezi = t.replace('\tsonnet\tclaude-sonnet-5-5\t2026.11.03', '\tkezi\t\t2026.11.03')
        with open(masolat, 'w', encoding='utf-8', newline='') as f:
            f.write(kezi)
        with self.assertRaises(SystemExit):
            L.beir(jelzes_atnezve=True, felulir=True, forditasok_ut=masolat)

    def test_hash_elteres_beir_megall(self):
        L.szaraz(self.lista)
        L.bevesz('G001-p1', self.valasz([{'id': 'e001', 'forditas_hu': 'démon; gonosz szellem'},
                                         {'id': 'e002', 'forditas_hu': 'ember'}]), 'claude-sonnet-5-5')
        L.kapuz()
        L.rogzit()
        sorok = L.tsv_be(L.ut('rogzitett.tsv'))
        sorok[0]['forras_hash'] = '0' * 40
        L.tsv_ir(L.ut('rogzitett.tsv'), L.FEJLEC + ['_manko'], sorok)
        masolat = os.path.join(self.tmp, 'forditasok.tsv')
        shutil.copy(GLF.FORDITASOK, masolat)
        with self.assertRaises(SystemExit):
            L.beir(jelzes_atnezve=True, forditasok_ut=masolat)
        with open(GLF.FORDITASOK, encoding='utf-8', newline='') as a, open(masolat, encoding='utf-8', newline='') as b:
            self.assertEqual(a.read(), b.read())


if __name__ == '__main__':
    unittest.main(verbosity=1)
