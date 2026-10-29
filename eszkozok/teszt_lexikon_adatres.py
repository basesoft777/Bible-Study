#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_lexikon_adatres.py -- F11 R (FELADATOK #11, DT-F11e): a
`lexikon_general.py` harom adatres-renderelojenek (alatamasztas, 2b,
minosites) es a `res_torzs` `forras=adat` aganak tesztjei.

A tiszta fuggvenyek (adatres_*) kitalalt sorokat kapnak; az eles adatot a
teszt nem irja. Futtatas: python eszkozok/teszt_lexikon_adatres.py
"""

import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ESZKOZOK)
import lexikon_general as LG  # noqa: E402


def kapcsolat(f, c, mid='PROBA-001', indoklas=''):
    return {'forras_igehely': f, 'cel_igehely': c, 'id': mid, 'indoklas': indoklas}


def hiv(strong, szotar, jsz='részlet', szoveg='LN: 1.1 Hebrew: x'):
    return {'strong': strong, 'szotar': szotar, 'entry_id': strong, 'jelentes_szam': jsz,
            'szoveg_en': szoveg, 'forrasfajl': 'konkordancia/proba.tsv'}


def jelolt(ige, forras, dontes, indoklas='ok', mid='PROBA-001'):
    return {'id': mid, 'igehely': ige, 'forras_kereses': forras, 'dontes': dontes, 'indoklas': indoklas}


class Alatamasztas(unittest.TestCase):
    def test_csoportositas_es_hiany(self):
        sorok = [kapcsolat('1Móz 4:26', 'Sof 3:9', indoklas='A indok'),
                 kapcsolat('1Kir 18:24', '1Kir 18:25', indoklas='Lánc | pipa'),
                 kapcsolat('1Kir 18:25', '1Kir 18:26', indoklas='Lánc | pipa'),
                 kapcsolat('Zsolt 1:1', 'Zsolt 1:2'),
                 kapcsolat('Mt 1:1', 'Mt 1:2', mid='MAS-001', indoklas='idegen')]
        ki = LG.adatres_alatamasztas('PROBA-001', sorok)
        self.assertIn('| 1Móz 4:26 → Sof 3:9 | A indok |', ki)
        self.assertIn('| 1Kir 18:24 → 1Kir 18:25; 1Kir 18:25 → 1Kir 18:26 | Lánc \\| pipa |', ki)
        self.assertIn('Rögzített indoklás nélküli kapcsolat-sor (1): Zsolt 1:1 → Zsolt 1:2.', ki)
        self.assertNotIn('idegen', ki)
        # a sorrend a fájlé: az A indok a lánc előtt
        self.assertLess(ki.index('A indok'), ki.index('Lánc'))

    def test_nincs_kapcsolat(self):
        self.assertEqual(LG.adatres_alatamasztas('PROBA-001', [kapcsolat('a', 'b', mid='MAS-001')]),
                         LG.ALATAMASZTAS_NINCS_KAPCSOLAT)

    def test_van_kapcsolat_de_nincs_indoklas(self):
        ki = LG.adatres_alatamasztas('PROBA-001', [kapcsolat('a', 'b'), kapcsolat('c', 'd')])
        self.assertIn('A motívum 2 kapcsolat-sorának egyikéhez sincs rögzített indoklás', ki)
        self.assertNotIn('| Kapcsolat |', ki)


class Kiegeszito2b(unittest.TestCase):
    def test_csak_kiegeszito_szotar_es_sajat_token(self):
        # a SECE-sor nem a 2/b-ben áll (a 7. szerep és a Rokon szavak olvasható táblázata; a nyers LN/GK mező
        # N-F33a szerint nem kerülhet a renderbe; ISTENTISZT-001 arany lap, 2026-10-29); a többi kiegészítő szótár igen
        sorok = [hiv('G1941', 'SECE_G'), hiv('G1941', 'BDB', jsz='1'), hiv('H7121', 'SECE_H'),
                 hiv('G9999', 'MCGED'), hiv('G1941', 'MCGED')]
        ki = LG.adatres_2b(['G1941', 'H7121'], sorok)
        self.assertIn('**MCGED G1941 — (részlet)**', ki)
        self.assertNotIn('SECE_G G1941', ki)
        self.assertNotIn('SECE_H H7121', ki)
        self.assertIn('*Forrás: konkordancia/proba.tsv*', ki)
        self.assertNotIn('BDB', ki)
        self.assertNotIn('G9999', ki)

    def test_rokon_szavak_tokenjei(self):
        tok = LG.adatres_2b_tokenek(['G1941', 'H7121'], ['G0994', 'G1941', 'G2564'])
        self.assertEqual(tok, ['G1941', 'H7121', 'G0994', 'G2564'])
        ki = LG.adatres_2b(tok, [hiv('G2564', 'MCGED'), hiv('G0994', 'MCGED'), hiv('G1941', 'MCGED')])
        self.assertLess(ki.index('G1941'), ki.index('G0994'))
        self.assertLess(ki.index('G0994'), ki.index('G2564'))
        self.assertTrue(LG.adatres_2b(tok, [hiv('G1941', 'SECE_G')]).startswith('*Nincs a szerepmátrixon'))

    def test_ures(self):
        ki = LG.adatres_2b(['G1941'], [hiv('G1941', 'BDB', jsz='1')])
        self.assertTrue(ki.startswith('*Nincs a szerepmátrixon'))


class Minosites(unittest.TestCase):
    ELOF = ['Jóel 2:32', 'Róm 10:13', 'ApCsel 2:21', 'Zsolt 1:1-3']
    TSK = {'Jóel 2:32': [{'Kapcsolódó igehely magyar megjelenítése': 'Róm 10,13', 'Votes': '103'},
                         {'Kapcsolódó igehely magyar megjelenítése': 'ApCsel 2,21', 'Votes': '14'},
                         {'Kapcsolódó igehely magyar megjelenítése': 'Róm 10,11', 'Votes': '19'}]}

    def test_megerosites_es_jeloltek(self):
        kh = {LG.L.to_step('ApCsel 2:21'): [{'Kapcsolódó igehely magyar megjelenítése': 'Jóel 2,32'}]}
        jel = [jelolt('Róm 10:11', 'TSK Jóel 2:32 → Róm 10:11 (19)', 'elutasítva', 'nincs | ige'),
               jelolt('Zsolt 9:9', 'scan G1941', 'nyitva'),
               jelolt('Róm 10:12', 'Károli-KH ApCsel 2:21', 'beépítve'),
               jelolt('Mt 1:1', 'TSK x', 'elutasítva', mid='MAS-001')]
        ki = LG.adatres_minosites('PROBA-001', self.ELOF, jel, self.TSK, kh)
        self.assertIn('**Független megerősítés** (2 pár):', ki)
        self.assertIn('- Jóel 2:32 → Róm 10:13 — TSK (Votes 103)', ki)
        self.assertIn('- ApCsel 2:21 → Jóel 2:32 — Károli-KH', ki)
        self.assertNotIn('Votes 14', ki)          # küszöb alatt
        self.assertNotIn('→ Róm 10:11 —', ki)      # cél nem előfordulás
        self.assertIn('(2 sor; beépítve 1, elutasítva 1)', ki)
        self.assertIn('| Róm 10:11 | elutasítva | TSK Jóel 2:32 → Róm 10:11 (19) | nincs \\| ige |', ki)
        self.assertNotIn('scan G1941', ki)
        self.assertNotIn('Mt 1:1', ki)

    def test_ures(self):
        ki = LG.adatres_minosites('PROBA-001', ['Mt 1:1'], [], {}, {})
        self.assertIn('**Független megerősítés:** nincs', ki)
        self.assertIn('**Kereszthivatkozásból minősített jelölt:** nincs', ki)


class ResTorzsAdatAg(unittest.TestCase):
    def test_rogzitett_mondat_valtozatlan(self):
        sor = {'forras': 'adat', 'tanulmany': 'A motívumhoz nincs rögzített kapcsolat.'}
        self.assertEqual(LG.res_torzs({'id': 'PROBA-001'}, 'alatamasztas', sor, []),
                         'A motívumhoz nincs rögzített kapcsolat.')

    def test_ures_mezo_renderel(self):
        eredeti = LG.ADAT_RES_RENDEREK['2b']
        try:
            LG.ADAT_RES_RENDEREK['2b'] = lambda mid, sorai: 'RENDER %s %d' % (mid, len(sorai))
            ki = LG.res_torzs({'id': 'PROBA-001'}, '2b', {'forras': 'adat', 'tanulmany': ''}, [{}, {}])
        finally:
            LG.ADAT_RES_RENDEREK['2b'] = eredeti
        self.assertIn('\n\nRENDER PROBA-001 2\n\n', ki)
        self.assertTrue(ki.startswith('<!-- GENERÁLT-RÉS: 2b | general.py --cel lexikon | forrás: '
                                      'adat/lexikon_hivatkozasok.tsv -->'))
        self.assertTrue(ki.endswith('*Proveniencia: `scope=id:PROBA-001 | forras=adat/lexikon_hivatkozasok.tsv '
                                    '| ts=%s`*' % LG.G.TS))

    def test_hatarkereses_kezi_tartalek(self):
        szoveg = 'x\n### Minősítés *(kézi)*\n\ny\n'
        i, talalt = LG._boundary_index(szoveg, '### Minősítés *(generált)*', 0, 'minosites')
        self.assertEqual((i, talalt), (2, '### Minősítés *(kézi)*'))
        with self.assertRaises(ValueError):
            LG._boundary_index(szoveg, '### Alátámasztás *(generált)*', 0, 'alatamasztas')

    def test_renderelo_nelkuli_res_hiba(self):
        with self.assertRaises(ValueError):
            LG.res_torzs({'id': 'PROBA-001'}, 'kivonat', {'forras': 'adat', 'tanulmany': ''}, [])


class KeziForrasApparatusNezet(unittest.TestCase):
    """A `motivumok/` alatti kézi forrás rés-törzse `apparatus` nézetből jön
    (a 【NAPLO】 és a `belso` blokk kimarad); a tematikus út változatlan."""
    FORRAS = ('# Próba — forrásréteg `[ID: PROBA-001]`\n\n'
              '## Kivonat\n\n'
              '<!-- RÉS-KEZDET: kivonat -->\n\n'
              'Olvasói mondat.\n\n'
              '【NAPLO: 2026-10-18, folyamat-nyom.】\n\n'
              '<!-- SZINT-KEZDET: belso -->\n\nBelső mondat.\n\n<!-- SZINT-VÉGE: belso -->\n\n'
              '<!-- RÉS-VÉGE: kivonat -->\n')

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix='teszt_adatres_')
        for rel in ('motivumok/PROBA-001.md', 'tematikus_lezart/Proba_tematikus.md'):
            ut = os.path.join(self.tmp, *rel.split('/'))
            os.makedirs(os.path.dirname(ut), exist_ok=True)
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write(self.FORRAS)
        self.regi_root = LG.ROOT
        LG.ROOT = self.tmp
        LG._tanulmany_szoveg_cache.clear()

    def tearDown(self):
        import shutil
        LG.ROOT = self.regi_root
        LG._tanulmany_szoveg_cache.clear()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_motivumok_apparatus(self):
        ki = LG.res_tanulmany_torzs('motivumok/PROBA-001.md', 'kivonat')
        self.assertEqual(ki, 'Olvasói mondat.')

    def test_tematikus_valtozatlan(self):
        ki = LG.res_tanulmany_torzs('tematikus_lezart/Proba_tematikus.md', 'kivonat')
        self.assertIn('【NAPLO: 2026-10-18', ki)
        self.assertIn('Belső mondat.', ki)


class KolofonNaploCella(unittest.TestCase):
    """F11 M3 javítókör (ELLENOR_F11_M 7. szakasz 3.): a migrált motívum
    Kolofonja nem a megszűnt `tematikus_lezart/naplok/` útra mutat."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix='teszt_kolofon_')
        for rel in ('tematikus_lezart/naplok/Elo_naplo.md', 'archivum/MIGR-001/Regi_naplo.md'):
            ut = os.path.join(self.tmp, *rel.split('/'))
            os.makedirs(os.path.dirname(ut), exist_ok=True)
            open(ut, 'w', encoding='utf-8').close()
        self.regi = (LG.ROOT, dict(LG.G.ID_NAPLO_TERKEP))
        LG.ROOT = self.tmp
        LG.G.ID_NAPLO_TERKEP.update({'ELO-001': 'Elo_naplo.md', 'MIGR-001': 'Regi_naplo.md',
                                     'HIANY-001': 'Nincs_naplo.md'})

    def tearDown(self):
        import shutil
        LG.ROOT = self.regi[0]
        LG.G.ID_NAPLO_TERKEP.clear()
        LG.G.ID_NAPLO_TERKEP.update(self.regi[1])
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_elo_naplo_valtozatlan(self):
        self.assertEqual(LG.kolofon_naplo_cella('ELO-001'), '`tematikus_lezart/naplok/Elo_naplo.md`')

    def test_migralt_archivum(self):
        ki = LG.kolofon_naplo_cella('MIGR-001')
        self.assertIn('`archivum/MIGR-001/Regi_naplo.md`', ki)
        self.assertNotIn('tematikus_lezart', ki)

    def test_nincs_sehol_es_nincs_terkep(self):
        self.assertEqual(LG.kolofon_naplo_cella('HIANY-001'), LG.EM_DASH)
        self.assertEqual(LG.kolofon_naplo_cella('NINCS-001'), LG.EM_DASH)


class GeneraltFejlec(unittest.TestCase):
    """F11 M4 (DT-F11h Á7): a helyben frissített lap fejléce után CRLF-es
    munkapéldányon is pontosan egy üres sor áll, mint az új fájlnál."""

    def test_crlf_es_lf_azonos(self):
        m = {'id': 'PROBA-001', 'forras_study': 'motivumok/PROBA-001.md'}
        fej = LG._generalt_fejlec_sor(m)
        lf = LG._generalt_fejlec_alkalmaz(fej + '\n\n# Cím\n', m)
        crlf = LG._generalt_fejlec_alkalmaz(fej + '\r\n\r\n\r\n# Cím\r\n', m)
        self.assertEqual(lf, fej + '\n\n# Cím\n')
        self.assertEqual(crlf.replace('\r\n', '\n'), lf)

    def test_fejlec_nelkuli_szoveg(self):
        m = {'id': 'PROBA-001', 'forras_study': ''}
        ki = LG._generalt_fejlec_alkalmaz('# Cím\n', m)
        self.assertTrue(ki.endswith('\n\n# Cím\n'))


class Szerepmatrix(unittest.TestCase):
    def test_kiegeszito_szotar_nem_szerepblokk(self):
        eredeti = LG.lexikon_hivatkozasok_ehhez
        try:
            LG.lexikon_hivatkozasok_ehhez = lambda s: [hiv(s, 'SECE_G'), hiv(s, 'Thayer', jsz='teljes')]
            r = LG._szotar_reszek('G1941', 1, {}, set())
        finally:
            LG.lexikon_hivatkozasok_ehhez = eredeti
        self.assertEqual([b[0] for b in r['forras_blokkok']], ['Thayer'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
