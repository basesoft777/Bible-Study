#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_heti_attekinto.py -- az `eszkozok/heti_attekinto.py` tesztjei: a sáv szerinti csoportosítás,
a hiányzó `sav` mező (besorolatlan), a „te teendőid” és a „kész a héten” ablak, a PR-hozzárendelés.
Ideiglenes könyvtárban felépített fixture-briefekkel; git és gh nem fut.

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


def brief_szoveg(szam, cim='Teszt', allapot='nem_indult', kovetkezo='/kovetkezo', sav=None, extra=None):
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

    def csoport(self, prok=None, lezarasok=None, nap=7):
        briefek = F.briefek_beolvas(self.ut)
        return H.csoportosit(briefek, prok or [], {}, MA, nap, lezarasok or {},
                             lambda b: H.sav_olvas(self.ut, b))

    @staticmethod
    def szamok(blokk):
        return [e['szam'] for e in blokk]


class SavCsoportositasTest(Alap):
    def test_negy_sav_es_besorolatlan(self):
        self.brief(1, allapot='fut', sav='SYSTEMS')
        self.brief(2, allapot='nem_indult', sav='CONTENT')
        self.brief(3, allapot='lezarva', sav='SERVER')
        self.brief(4, allapot='megallt', sav='USER')
        self.brief(5, allapot='fut')
        sorok, _ = self.csoport(lezarasok={'F03_T3_BRIEF.md': date(2026, 11, 13)})
        self.assertEqual(self.szamok(sorok['SYSTEMS'][H.FUT]), [1])
        self.assertEqual(self.szamok(sorok['CONTENT'][H.VAR]), [2])
        self.assertEqual(self.szamok(sorok['SERVER'][H.KESZ]), [3])
        self.assertEqual(self.szamok(sorok['USER'][H.FUT]), [4])
        self.assertEqual(self.szamok(sorok[H.BESOROLATLAN][H.FUT]), [5])

    def test_hianyzo_sav_besorolatlan(self):
        self.brief(1, allapot='fut')
        self.brief(2, allapot='nem_indult')
        sorok, _ = self.csoport()
        self.assertEqual(self.szamok(sorok[H.BESOROLATLAN][H.FUT]), [1])
        self.assertEqual(self.szamok(sorok[H.BESOROLATLAN][H.VAR]), [2])
        for sav, _ in H.SAVOK:
            self.assertEqual(sum(len(v) for v in sorok[sav].values()), 0)

    def test_ismeretlen_sav_besorolatlan(self):
        self.brief(1, allapot='fut', sav='VALAMI')
        sorok, _ = self.csoport()
        self.assertEqual(self.szamok(sorok[H.BESOROLATLAN][H.FUT]), [1])

    def test_sav_kisbetuvel_is_jo(self):
        self.brief(1, allapot='fut', sav='server')
        sorok, _ = self.csoport()
        self.assertEqual(self.szamok(sorok['SERVER'][H.FUT]), [1])

    def test_varakozas_fuggessel(self):
        self.brief(1, allapot='fut', sav='SYSTEMS')
        self.brief(2, allapot='nem_indult', sav='SYSTEMS', extra={'fugg': '[1]'})
        sorok, _ = self.csoport()
        var = sorok['SYSTEMS'][H.VAR]
        self.assertEqual([n for n, _ in var[0]['varakozas']], [1])


class TeendoTest(Alap):
    def teendok(self):
        return {t['szam']: t['teendo'] for t in self.csoport()[1]}

    def test_te_elotag_es_dontesre_var(self):
        self.brief(1, allapot='megallt', kovetkezo='"Te: a draft PR áttekintése"')
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


class KeszAblakTest(Alap):
    def test_het_napon_belul(self):
        self.brief(1, allapot='lezarva', sav='CONTENT')
        self.brief(2, allapot='lezarva', sav='CONTENT')
        self.brief(3, allapot='lezarva', sav='CONTENT')
        sorok, _ = self.csoport(lezarasok={'F01_T1_BRIEF.md': date(2026, 11, 8),     # pontosan 7 napja
                                           'F02_T2_BRIEF.md': date(2026, 11, 7)})    # 8 napja
        self.assertEqual(self.szamok(sorok['CONTENT'][H.KESZ]), [1])
        self.assertEqual(self.szamok(sorok['CONTENT'][H.FUT]), [])

    def test_datum_hianyaban_nem_kerul_be(self):
        self.brief(1, allapot='lezarva', sav='CONTENT')
        sorok, _ = self.csoport()
        self.assertEqual(sorok['CONTENT'][H.KESZ], [])

    def test_lezarva_osszegzes_datuma_tartalek(self):
        self.brief(1, allapot='lezarva', sav='CONTENT', extra={'lezarva_osszegzes': '"kész (11.12)"'})
        sorok, _ = self.csoport()
        self.assertEqual(self.szamok(sorok['CONTENT'][H.KESZ]), [1])

    def test_rendezes_legujabb_elol(self):
        for n in (1, 2):
            self.brief(n, allapot='lezarva')
        sorok, _ = self.csoport(lezarasok={'F01_T1_BRIEF.md': date(2026, 11, 10),
                                           'F02_T2_BRIEF.md': date(2026, 11, 14)})
        self.assertEqual(self.szamok(sorok[H.BESOROLATLAN][H.KESZ]), [2, 1])


def pr(szam, cim, ag='claude/x', allapot='OPEN', merge=None, piszkozat=False):
    return {'number': szam, 'title': cim, 'state': allapot, 'isDraft': piszkozat, 'mergedAt': merge,
            'headRefName': ag, 'url': 'https://example.invalid/pull/%d' % szam}


class PrTest(Alap):
    def test_nyitott_pr_a_brief_soran(self):
        self.brief(5, allapot='fut', sav='SERVER')
        sorok, _ = self.csoport(prok=[pr(10, '[ELLENŐRZŐ] F5: valami', piszkozat=True)])
        fut = sorok['SERVER'][H.FUT]
        self.assertEqual(len(fut), 1)
        self.assertEqual([p['szam'] for p in fut[0]['prok']], [10])
        self.assertTrue(fut[0]['prok'][0]['piszkozat'])
        self.assertEqual(fut[0]['prok'][0]['cim'], 'F5: valami')   # az [ELLENŐRZŐ] előtag nélkül

    def test_pr_mezo_es_ag_szerinti_egyezes(self):
        self.brief(5, allapot='fut', sav='SERVER', extra={'pr': '"10"'})
        self.brief(6, allapot='fut', sav='USER', extra={'ag': 'claude/hat'})
        sorok, _ = self.csoport(prok=[pr(10, 'Valami cím'), pr(11, 'Más cím', ag='claude/hat')])
        self.assertEqual([p['szam'] for p in sorok['SERVER'][H.FUT][0]['prok']], [10])
        self.assertEqual([p['szam'] for p in sorok['USER'][H.FUT][0]['prok']], [11])

    def test_brief_nelkuli_pr_besorolatlan(self):
        sorok, _ = self.csoport(prok=[pr(20, 'Cím számjelzés nélkül'),
                                      pr(21, 'Mergelt', allapot='MERGED', merge='2026-11-14T10:00:00Z'),
                                      pr(22, 'Régen mergelt', allapot='MERGED', merge='2026-10-01T10:00:00Z')])
        self.assertEqual([e['prok'][0]['szam'] for e in sorok[H.BESOROLATLAN][H.FUT]], [20])
        self.assertEqual([e['prok'][0]['szam'] for e in sorok[H.BESOROLATLAN][H.KESZ]], [21])

    def test_mergelt_pr_nyitott_brief_savjaban(self):
        self.brief(5, allapot='fut', sav='SYSTEMS')
        sorok, _ = self.csoport(prok=[pr(30, 'F5: befogadás', allapot='MERGED', merge='2026-11-13T10:00:00Z')])
        self.assertEqual([e['prok'][0]['szam'] for e in sorok['SYSTEMS'][H.KESZ]], [30])
        self.assertEqual(len(sorok['SYSTEMS'][H.FUT]), 1)

    def test_lezart_brief_mergelt_pr_a_brief_soran(self):
        self.brief(5, allapot='lezarva', sav='SYSTEMS')
        sorok, _ = self.csoport(prok=[pr(30, 'F5: lezárás', allapot='MERGED', merge='2026-11-13T10:00:00Z')],
                                lezarasok={'F05_T5_BRIEF.md': date(2026, 11, 13)})
        kesz = sorok['SYSTEMS'][H.KESZ]
        self.assertEqual(len(kesz), 1)
        self.assertEqual([p['szam'] for p in kesz[0]['prok']], [30])


class OldalTest(Alap):
    def keszit(self, prok=None, lezarasok=None):
        pr_ut = os.path.join(self.ut, 'prok.json')
        with open(pr_ut, 'w', encoding='utf-8') as f:
            json.dump(prok or [], f)
        return H.osszeallit(self.ut, MA, 7, pr_json=pr_ut, ts=datetime(2026, 11, 15, 12, 0))

    def test_oldal_felepitese_es_darabszam(self):
        self.brief(1, allapot='fut', sav='SYSTEMS', kovetkezo='Te: átnézés')
        self.brief(2, allapot='nem_indult', sav='CONTENT')
        self.brief(3, allapot='dontesre_var')
        oldal, szamok, teendok, hiba = self.keszit()
        self.assertIsNone(hiba)
        self.assertEqual(teendok, 2)
        self.assertEqual(szamok['SYSTEMS'][H.FUT], 1)
        self.assertEqual(szamok['CONTENT'][H.VAR], 1)
        self.assertEqual(szamok[H.BESOROLATLAN][H.FUT], 1)
        self.assertLess(oldal.index('A te teendőid'), oldal.index('Fejlesztői infrastruktúra</h2>'))
        self.assertIn('prefers-color-scheme:dark', oldal)
        self.assertIn('<html lang="hu">', oldal)
        self.assertIn('scope=3 brief-fejléc', oldal)       # proveniencia
        self.assertIn('ts=2026-11-15T12:00:00', oldal)

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

    def test_hianyzo_sav_nem_buktatja_az_oldalt(self):
        self.brief(1, allapot='fut')
        oldal, szamok, _, _ = self.keszit()
        self.assertIn('Besorolatlan', oldal)
        self.assertEqual(szamok[H.BESOROLATLAN][H.FUT], 1)

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
