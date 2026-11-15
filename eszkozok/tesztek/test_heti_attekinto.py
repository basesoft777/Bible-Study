#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_heti_attekinto.py -- az `eszkozok/heti_attekinto.py` tesztjei: a sáv szerinti csoportosítás
(csak nyitott tétel: folyamatban / vár), a hiányzó `sav` mező mint hiba, a „te teendőid”, a nyitott
PR-hozzárendelés. Ideiglenes könyvtárban felépített fixture-briefekkel; git és gh nem fut.

Futtatás: python eszkozok/tesztek/test_heti_attekinto.py
"""

import json
import os
import re
import sys
import tempfile
import unittest
from datetime import date, datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import feladatok as F  # noqa: E402
import heti_attekinto as H  # noqa: E402

MA = date(2026, 11, 15)


def brief_szoveg(szam, cim='Teszt', allapot='nem_indult', kovetkezo='/kovetkezo', sav='SYSTEMS', extra=None):
    sorok = ['---', 'feladat: %d' % szam, 'cim: %s' % cim, 'tipus: feladat', 'fazis: folyamat',
             'modell: sonnet', 'allapot: %s' % allapot, 'ad: mit ad', 'kovetkezo: %s' % kovetkezo]
    if sav is not None:
        sorok.append('sav: %s' % sav)
    for k, v in (extra or {}).items():
        sorok.append('%s: %s' % (k, v))
    sorok.append('---')
    return '\n'.join(sorok) + '\n\ntörzs\n'


class Alap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ut = self.tmp.name

    def brief(self, szam, **kw):
        with open(os.path.join(self.ut, 'F%02d_T%d_BRIEF.md' % (szam, szam)), 'w', encoding='utf-8', newline='') as f:
            f.write(brief_szoveg(szam, **kw))

    def csoport(self, prok=None):
        briefek = F.briefek_beolvas(self.ut)
        return H.csoportosit(briefek, prok or [], {}, H.sav_olvas)

    @staticmethod
    def szamok(blokk):
        return [e['szam'] for e in blokk]


class SavCsoportositasTest(Alap):
    def test_savok_egyeznek_a_feladatok_py_savjaival(self):
        self.assertEqual([s for s, _ in H.SAVOK], list(F.SAVOK))

    def test_negy_sav_ket_blokk(self):
        self.brief(1, allapot='fut', sav='SYSTEMS')
        self.brief(2, allapot='nem_indult', sav='CONTENT')
        self.brief(3, allapot='megallt', sav='SERVER')
        self.brief(4, allapot='dontesre_var', sav='USER')
        sorok, _, hibak, _ = self.csoport()
        self.assertEqual(hibak, [])
        self.assertEqual(self.szamok(sorok['SYSTEMS'][H.FUT]), [1])
        self.assertEqual(self.szamok(sorok['CONTENT'][H.VAR]), [2])
        self.assertEqual(self.szamok(sorok['SERVER'][H.FUT]), [3])       # a `megallt` a folyamatban blokkba kerül
        self.assertEqual(self.szamok(sorok['USER'][H.VAR]), [4])         # a `dontesre_var` a vár blokkba kerül

    def test_lezart_brief_nem_kerul_ki(self):
        self.brief(1, allapot='lezarva', sav='CONTENT')
        self.brief(2, allapot='fut', sav='CONTENT')
        sorok, teendok, _, _ = self.csoport()
        self.assertEqual(self.szamok(sorok['CONTENT'][H.FUT]), [2])
        self.assertEqual(self.szamok(sorok['CONTENT'][H.VAR]), [])
        self.assertEqual(teendok, [])

    def test_hianyzo_sav_hiba_nem_csoport(self):
        self.brief(1, allapot='fut', sav=None)
        self.brief(2, allapot='nem_indult', sav='CONTENT')
        sorok, _, hibak, _ = self.csoport()
        self.assertEqual(len(hibak), 1)
        self.assertIn('#1', hibak[0])
        self.assertNotIn(1, self.szamok(sorok['CONTENT'][H.FUT]) + self.szamok(sorok['CONTENT'][H.VAR]))
        self.assertEqual(set(sorok), {s for s, _ in H.SAVOK})            # besorolatlan csoport nincs

    def test_ismeretlen_sav_hiba(self):
        self.brief(1, allapot='fut', sav='VALAMI')
        _, _, hibak, _ = self.csoport()
        self.assertEqual(len(hibak), 1)

    def test_lezart_brief_hianyzo_sava_nem_hiba(self):
        self.brief(1, allapot='lezarva', sav=None)
        _, _, hibak, _ = self.csoport()
        self.assertEqual(hibak, [])

    def test_atmeneti_kivetel_savja(self):
        self.brief(217, allapot='nem_indult', sav=None)
        self.brief(218, allapot='nem_indult', sav=None)
        sorok, _, hibak, _ = self.csoport()
        self.assertEqual(hibak, [])
        self.assertEqual(self.szamok(sorok['SYSTEMS'][H.VAR]), [217])
        self.assertEqual(self.szamok(sorok['CONTENT'][H.VAR]), [218])

    def test_atmeneti_kivetel_csak_amig_a_tuple_tartalmazza(self):
        self.brief(217, allapot='nem_indult', sav=None)
        eredeti = F.SAV_ATMENET_KIVETEL
        F.SAV_ATMENET_KIVETEL = ()
        try:
            _, _, hibak, _ = self.csoport()
        finally:
            F.SAV_ATMENET_KIVETEL = eredeti
        self.assertEqual(len(hibak), 1)

    def test_sav_kisbetuvel_is_jo(self):
        self.brief(1, allapot='fut', sav='server')
        sorok, _, _, _ = self.csoport()
        self.assertEqual(self.szamok(sorok['SERVER'][H.FUT]), [1])

    def test_varakozas_fuggessel(self):
        self.brief(1, allapot='fut', sav='SYSTEMS')
        self.brief(2, allapot='nem_indult', sav='SYSTEMS', extra={'fugg': '[1]'})
        sorok, _, _, _ = self.csoport()
        var = sorok['SYSTEMS'][H.VAR]
        self.assertEqual([n for n, _ in var[0]['varakozas']], [1])

    def test_lezart_fuggoseg_nem_varakozas(self):
        self.brief(1, allapot='lezarva', sav='SYSTEMS')
        self.brief(2, allapot='nem_indult', sav='SYSTEMS', extra={'fugg': '[1]'})
        sorok, _, _, _ = self.csoport()
        self.assertEqual(sorok['SYSTEMS'][H.VAR][0]['varakozas'], [])


class TeendoTest(Alap):
    def teendok(self):
        return {t['szam']: t['teendo'] for t in self.csoport()[1]}

    def test_te_elotag_es_dontesre_var(self):
        self.brief(1, allapot='megallt', kovetkezo='"Te: a draft PR áttekintése"', sav='SYSTEMS')
        self.brief(2, allapot='dontesre_var', kovetkezo='a döntés kell')
        self.brief(3, allapot='fut', kovetkezo='/kovetkezo')
        t = self.teendok()
        self.assertEqual(t[1], 'a draft PR áttekintése')
        self.assertEqual(t[2], 'a döntés kell')
        self.assertNotIn(3, t)

    def test_megallasi_pont_megkezdett_munkanal(self):
        self.brief(1, allapot='fut', kovetkezo='⛔ a kezelés eldöntése')
        self.brief(2, allapot='nem_indult', kovetkezo='/kovetkezo; ⛔ M0 (terv)')
        t = self.teendok()
        self.assertIn(1, t)
        self.assertNotIn(2, t)

    def test_halasztott_es_lezart_nem_teendo(self):
        self.brief(1, allapot='nem_indult', kovetkezo='Halasztva: a #9 után, Te: kell')
        self.brief(2, allapot='lezarva', kovetkezo='Te: semmi')
        self.assertEqual(self.teendok(), {})

    def test_belso_azonosito_nem_kerul_ki(self):
        self.brief(1, allapot='megallt',
                   kovetkezo='"Te: [elteres_kor 2/2] ELLENOR_F1_3 1. mechanikus"')
        self.assertEqual(self.teendok()[1], 'az ellenőrzési jelentés 1. mechanikus')

    def test_ellenor_fajlnev_utvonallal_is(self):
        self.assertEqual(H.tisztit('ellenőr: naplok/ELLENOR_TERV_SZINKRON_3.md; az ELLENOR_F1_3 1.'),
                         'ellenőr: az ellenőrzési jelentés; az ellenőrzési jelentés 1.')


def pr(szam, cim, ag='claude/x', allapot='OPEN', merge=None, piszkozat=False):
    return {'number': szam, 'title': cim, 'state': allapot, 'isDraft': piszkozat, 'mergedAt': merge,
            'headRefName': ag, 'url': 'https://example.invalid/pull/%d' % szam}


class PrTest(Alap):
    def test_nyitott_pr_a_brief_soran(self):
        self.brief(5, allapot='fut', sav='SERVER')
        sorok, _, _, _ = self.csoport(prok=[pr(10, '[ELLENŐRZŐ] F5: valami', piszkozat=True)])
        fut = sorok['SERVER'][H.FUT]
        self.assertEqual(len(fut), 1)
        self.assertEqual([p['szam'] for p in fut[0]['prok']], [10])
        self.assertTrue(fut[0]['prok'][0]['piszkozat'])
        self.assertEqual(fut[0]['prok'][0]['cim'], 'F5: valami')   # az [ELLENŐRZŐ] előtag nélkül

    def test_pr_mezo_es_ag_szerinti_egyezes(self):
        self.brief(5, allapot='fut', sav='SERVER', extra={'pr': '"10"'})
        self.brief(6, allapot='fut', sav='USER', extra={'ag': 'claude/hat'})
        sorok, _, _, _ = self.csoport(prok=[pr(10, 'Valami cím'), pr(11, 'Más cím', ag='claude/hat')])
        self.assertEqual([p['szam'] for p in sorok['SERVER'][H.FUT][0]['prok']], [10])
        self.assertEqual([p['szam'] for p in sorok['USER'][H.FUT][0]['prok']], [11])

    def test_brief_nelkuli_pr_nem_kerul_az_oldalra(self):
        sorok, _, hibak, nelkuli = self.csoport(prok=[pr(20, 'Cím számjelzés nélkül')])
        self.assertEqual(hibak, [])
        self.assertEqual(nelkuli, 1)
        self.assertEqual(sum(len(v) for s in sorok.values() for v in s.values()), 0)

    def test_mergelt_pr_nem_jelenik_meg(self):
        self.brief(5, allapot='fut', sav='SYSTEMS')
        sorok, _, _, nelkuli = self.csoport(prok=[pr(30, 'F5: befogadás', allapot='MERGED', merge='2026-11-13T10:00:00Z')])
        self.assertEqual(sorok['SYSTEMS'][H.FUT][0]['prok'], [])
        self.assertEqual(nelkuli, 0)

    def test_pr_lista_fajl_kiszuri_a_mergeltet(self):
        ut = os.path.join(self.ut, 'prok.json')
        with open(ut, 'w', encoding='utf-8') as f:
            json.dump([pr(1, 'F1: nyitott'), pr(2, 'F2: mergelt', allapot='MERGED', merge='2026-11-13T10:00:00Z')], f)
        prok, hiba = H.pr_lista_fajl(ut)
        self.assertIsNone(hiba)
        self.assertEqual([p['number'] for p in prok], [1])


class OldalTest(Alap):
    def keszit(self, prok=None):
        pr_ut = os.path.join(self.ut, 'prok.json')
        with open(pr_ut, 'w', encoding='utf-8') as f:
            json.dump(prok or [], f)
        return H.osszeallit(self.ut, MA, pr_json=pr_ut, ts=datetime(2026, 11, 15, 12, 0))

    def test_oldal_felepitese_es_darabszam(self):
        self.brief(1, allapot='fut', sav='SYSTEMS', kovetkezo='Te: átnézés')
        self.brief(2, allapot='nem_indult', sav='CONTENT')
        self.brief(3, allapot='dontesre_var', sav='CONTENT')
        self.brief(4, allapot='lezarva', sav='CONTENT')
        oldal, szamok, hibak, pr_hiba = self.keszit()
        self.assertIsNone(pr_hiba)
        self.assertEqual(hibak, [])
        self.assertEqual(szamok['teendok'], 2)
        self.assertEqual(szamok['SYSTEMS'][H.FUT], 1)
        self.assertEqual(szamok['CONTENT'][H.VAR], 2)
        self.assertLess(oldal.index('A te teendőid'), oldal.index('Fejlesztői infrastruktúra</h2>'))
        self.assertIn('prefers-color-scheme:dark', oldal)
        self.assertIn('<html lang="hu">', oldal)
        self.assertIn('scope=4 brief-fejléc', oldal)       # proveniencia
        self.assertIn('ts=2026-11-15T12:00:00', oldal)

    def test_nincs_lezart_vagy_kesz_a_heten_elem_az_oldalon(self):
        self.brief(1, allapot='lezarva', sav='SYSTEMS', cim='LezartCim')
        self.brief(2, allapot='fut', sav='SYSTEMS', cim='NyitottCim')
        oldal, _, _, _ = self.keszit()
        szoveg = re.sub(r'<[^>]+>', ' ', oldal[oldal.index('<main>'):])
        self.assertNotIn('LezartCim', szoveg)
        self.assertIn('NyitottCim', szoveg)
        for tiltott in ('Kész a héten', 'lezárva', 'egyesítve', 'Besorolatlan'):
            self.assertNotIn(tiltott, szoveg)

    def test_nyers_belso_kulcs_nincs_az_oldalon(self):
        self.brief(1, allapot='nem_indult', sav='SYSTEMS')
        self.brief(2, allapot='dontesre_var', sav='SYSTEMS')
        self.brief(3, allapot='brief_kell', sav='SYSTEMS')
        self.brief(4, allapot='megallt', sav='SYSTEMS')
        oldal, _, _, _ = self.keszit()
        torzs = oldal[oldal.index('<main>'):]
        szoveg = re.sub(r'<[^>]+>', ' ', torzs)
        for kulcs in ('nem_indult', 'dontesre_var', 'brief_kell', 'SYSTEMS', 'CONTENT'):
            self.assertNotIn(kulcs, szoveg)
        self.assertIn('nem indult', szoveg)
        self.assertIn('döntésre vár', szoveg)

    def test_hianyzo_sav_hibaval_all_meg(self):
        self.brief(1, allapot='fut', sav=None)
        oldal, szamok, hibak, _ = self.keszit()
        self.assertIsNone(oldal)
        self.assertEqual(len(hibak), 1)

    def test_main_hibakod_es_nincs_kimenet(self):
        self.brief(1, allapot='fut', sav=None)
        pr_ut = os.path.join(self.ut, 'prok.json')
        with open(pr_ut, 'w', encoding='utf-8') as f:
            json.dump([], f)
        kimenet = os.path.join(tempfile.gettempdir(), 'heti_attekinto_teszt_%d.html' % os.getpid())
        self.addCleanup(lambda: os.path.exists(kimenet) and os.remove(kimenet))
        self.assertEqual(H.main(['--gyoker', self.ut, '--kimenet', kimenet, '--pr-json', pr_ut]), 2)
        self.assertFalse(os.path.exists(kimenet))

    def test_kulso_erdforras_csak_a_google_fonts(self):
        self.brief(1, allapot='fut')
        oldal, _, _, _ = self.keszit()
        hosztok = set(re.findall(r'(?:src|href)="https?://([^/"]+)', oldal))
        self.assertTrue(hosztok <= {'fonts.googleapis.com', 'fonts.gstatic.com'}, hosztok)

    def test_html_escape(self):
        self.brief(1, allapot='fut', cim='<script>alert(1)</script>')
        oldal, _, _, _ = self.keszit()
        self.assertNotIn('<script>alert', oldal)

    def test_kimenet_a_reponbelulre_elutasitva(self):
        self.assertEqual(H.main(['--gyoker', self.ut, '--kimenet', os.path.join(self.ut, 'x.html'),
                                 '--pr-json', os.path.join(self.ut, 'nincs.json')]), 2)
        self.assertFalse(os.path.exists(os.path.join(self.ut, 'x.html')))


if __name__ == '__main__':
    unittest.main(verbosity=1)
