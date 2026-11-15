#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_heti_beosztas.py -- az `eszkozok/heti_beosztas.py` tesztjei (F222): a keret-hét határa, a három tábla
ellenőrzése, a valós állapot (brief, PR) és a kézi jelölés viszonya, a „lezárt tétel csak a visszanézésben áll”
szabály, a teendők, a keret és az oldal szerkezete. Ideiglenes könyvtárban felépített fixture-ekkel; git és gh nem
fut. A valós `adat/heti_terv.tsv`, `adat/heti_keret.tsv`, `adat/otlettar.tsv` érvényességét is méri.

Futtatás: python eszkozok/tesztek/test_heti_beosztas.py
"""

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
import heti_beosztas as B  # noqa: E402

HET = date(2026, 11, 14)            # szombat
ELOZO = date(2026, 11, 7)
DT = datetime(2026, 11, 15, 12, 0)  # vasárnap: a 2026-11-14-i keret-hét


def terv_sor(sav='CONTENT', sorrend=1, tetel='-', cel='Cél', modell='-', keret=0, kezi='', jov='javaslat',
             megj='', het=HET):
    return {'het': het.isoformat(), 'sav': sav, 'sorrend': str(sorrend), 'tetel': tetel, 'cel_a_het_vegere': cel,
            'modell': modell, 'becsult_keret_szazalek': str(keret), 'allapot_kezi': kezi, 'jovahagyva': jov,
            'megjegyzes': megj, '_sor': 2}


def tsv_szoveg(fejlec, sorok):
    return '\n'.join(['\t'.join(fejlec)] + ['\t'.join(s) for s in sorok]) + '\n'


def brief_szoveg(szam, allapot='nem_indult', kovetkezo='/kovetkezo', extra=None):
    sorok = ['---', 'feladat: %d' % szam, 'cim: Teszt %d' % szam, 'tipus: feladat', 'fazis: folyamat',
             'modell: sonnet', 'sav: SYSTEMS', 'allapot: %s' % allapot, 'ad: mit ad', 'kovetkezo: %s' % kovetkezo]
    for k, v in (extra or {}).items():
        sorok.append('%s: %s' % (k, v))
    sorok.append('---')
    return '\n'.join(sorok) + '\n\ntörzs\n'


def pr(szam, cim, ag='claude/x', merge=None, piszkozat=False):
    return {'number': szam, 'title': cim, 'state': 'MERGED' if merge else 'OPEN', 'isDraft': piszkozat,
            'mergedAt': merge, 'headRefName': ag, 'url': 'https://example.invalid/pull/%d' % szam}


class Alap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ut = self.tmp.name

    def brief(self, szam, **kw):
        with open(os.path.join(self.ut, 'F%02d_T%d_BRIEF.md' % (szam, szam)), 'w', encoding='utf-8', newline='') as f:
            f.write(brief_szoveg(szam, **kw))

    def modell(self, terv, keret=None, otlet=None, prok=None, dt=DT):
        briefek = F.briefek_beolvas(self.ut)
        return B.epit(terv, keret or [], otlet or [], briefek, {}, prok or [], dt)

    def oldal(self, m):
        return B.html_keszit(m, ('forrás', 'gépi'), datetime(2026, 11, 15, 12, 0))


class KeretHetTest(unittest.TestCase):
    def test_szombat_14_elott_az_elozo_het(self):
        self.assertEqual(B.het_kezdete(datetime(2026, 11, 14, 13, 59)), date(2026, 11, 7))

    def test_szombat_14_utan_az_uj_het(self):
        self.assertEqual(B.het_kezdete(datetime(2026, 11, 14, 14, 0)), HET)

    def test_het_kozben_es_a_hatar_elott(self):
        self.assertEqual(B.het_kezdete(datetime(2026, 11, 15, 9, 0)), HET)        # vasárnap
        self.assertEqual(B.het_kezdete(datetime(2026, 11, 20, 23, 59)), HET)      # péntek
        self.assertEqual(B.het_kezdete(datetime(2026, 11, 21, 13, 59)), HET)      # a következő szombat 14:00 előtt


class TablaTest(Alap):
    def irj(self, nev, fej, sorok):
        os.makedirs(os.path.join(self.ut, 'adat'), exist_ok=True)
        with open(os.path.join(self.ut, 'adat', nev), 'w', encoding='utf-8', newline='') as f:
            f.write(tsv_szoveg(fej, sorok))

    def terv_nyers(self, **kw):
        s = terv_sor(**kw)
        return [s[k] for k in B.TERV_FEJ]

    def hibak(self, sorok):
        self.irj('heti_terv.tsv', B.TERV_FEJ, sorok)
        self.irj('heti_keret.tsv', B.KERET_FEJ, [])
        self.irj('otlettar.tsv', B.OTLET_FEJ, [])
        return B.tablak_olvas(self.ut)[3]

    def test_ervenyes_terv(self):
        self.assertEqual(self.hibak([self.terv_nyers(keret=100)]), [])

    def test_nem_szombati_het(self):
        h = self.hibak([self.terv_nyers(keret=100, het=date(2026, 11, 15))])
        self.assertTrue(any('szombati' in x for x in h), h)

    def test_osszeg_nem_100(self):
        h = self.hibak([self.terv_nyers(keret=60)])
        self.assertTrue(any('nem 100' in x for x in h), h)

    def test_csuszik_indok_nelkul(self):
        h = self.hibak([self.terv_nyers(keret=100, kezi='csuszik')])
        self.assertTrue(any('indok' in x for x in h), h)
        self.assertEqual(self.hibak([self.terv_nyers(keret=100, kezi='csuszik: a #9 miatt')]), [])

    def test_ismeretlen_sav_es_jovahagyas(self):
        h = self.hibak([self.terv_nyers(sav='MASIK', keret=100, jov='talan')])
        self.assertTrue(any('ismeretlen `sav`' in x for x in h), h)
        self.assertTrue(any('jovahagyva' in x for x in h), h)

    def test_ismetlodo_kulcs(self):
        h = self.hibak([self.terv_nyers(keret=50), self.terv_nyers(keret=50)])
        self.assertTrue(any('ismétlődő' in x for x in h), h)

    def test_rossz_fejlec(self):
        self.irj('heti_terv.tsv', B.TERV_FEJ[:-1], [])
        self.irj('heti_keret.tsv', B.KERET_FEJ, [])
        self.irj('otlettar.tsv', B.OTLET_FEJ, [])
        self.assertTrue(any('fejlécsor' in x for x in B.tablak_olvas(self.ut)[3]))

    def test_elvetve_hivatkozas_nelkul(self):
        sor = ['OT001', 'SERVER', 'Cím', 'a felhasználó, 2026-11-15', 'elvetve', '']
        self.irj('heti_terv.tsv', B.TERV_FEJ, [])
        self.irj('heti_keret.tsv', B.KERET_FEJ, [])
        self.irj('otlettar.tsv', B.OTLET_FEJ, [sor])
        h = B.tablak_olvas(self.ut)[3]
        self.assertTrue(any('hivatkozás kell' in x for x in h), h)
        sor[4] = 'elvetve: DT846'
        self.irj('otlettar.tsv', B.OTLET_FEJ, [sor])
        self.assertEqual(B.tablak_olvas(self.ut)[3], [])

    def test_keret_ts_alak(self):
        self.irj('heti_terv.tsv', B.TERV_FEJ, [])
        self.irj('otlettar.tsv', B.OTLET_FEJ, [])
        self.irj('heti_keret.tsv', B.KERET_FEJ, [[HET.isoformat(), 'CONTENT', '30', 'tegnap', 'get_usage']])
        self.assertTrue(any('`ts`' in x for x in B.tablak_olvas(self.ut)[3]))

    def test_a_valos_tablak_ervenyesek(self):
        terv, keret, otlet, hibak = B.tablak_olvas(F.REPO)
        self.assertEqual(hibak, [])
        self.assertGreater(len(terv), 0)
        self.assertGreater(len(otlet), 0)
        # a mostani hét terve javaslat jelzéssel, az ötlettár állapotai a zárt készletből
        self.assertTrue(all(s['jovahagyva'] in B.JOVAHAGYVA for s in terv))
        self.assertTrue(all(B.otlet_allapot(o['allapot'])[0] in B.OTLET_ALLAPOTOK for o in otlet))


class AllapotTest(Alap):
    def allapot(self, sor, prok=None):
        briefek = F.briefek_beolvas(self.ut)
        return B.valos_allapot(sor, B.kontextus_keszit(briefek, prok or [], {}))

    def test_lezart_brief_lezart_sor(self):
        self.brief(5, allapot='lezarva')
        a = self.allapot(terv_sor(tetel='F5'))
        self.assertTrue(a['lezart'])
        self.assertEqual(a['forras'], 'brief')

    def test_futo_brief_nyitott_sor(self):
        self.brief(5, allapot='fut')
        a = self.allapot(terv_sor(tetel='#5'))
        self.assertFalse(a['lezart'])
        self.assertEqual(a['cimke'], 'folyamatban')

    def test_valos_allapot_felulirja_a_kezit(self):
        self.brief(5, allapot='fut')
        a = self.allapot(terv_sor(tetel='F5', kezi='kesz'))
        self.assertFalse(a['lezart'])
        self.assertIn('eltér', a['megjegyzes'])

    def test_kezi_kesz_brief_nelkul(self):
        self.assertTrue(self.allapot(terv_sor(tetel='N-F9', kezi='kesz'))['lezart'])
        self.assertTrue(self.allapot(terv_sor(tetel='-', kezi='elhagyva: nem kell'))['elhagyva'])
        a = self.allapot(terv_sor(tetel='N-F9', kezi='blokkolt: a felhasználó dönt'))
        self.assertFalse(a['lezart'])
        self.assertEqual(a['kulcs'], 'blokkolt')

    def test_nincs_jelezve(self):
        a = self.allapot(terv_sor(tetel='N-F9'))
        self.assertEqual(a['cimke'], 'nincs jelezve')
        self.assertFalse(a['lezart'])

    def test_ismeretlen_brief_a_kezi_jelolesre_esik_vissza(self):
        a = self.allapot(terv_sor(tetel='F99', kezi='kesz'))
        self.assertTrue(a['lezart'])
        self.assertIn('nem található', a['megjegyzes'])

    def test_nyitott_pr_a_nem_indult_briefnel(self):
        self.brief(5, allapot='nem_indult')
        a = self.allapot(terv_sor(tetel='F5'), prok=[pr(10, 'F5: valami', piszkozat=True)])
        self.assertFalse(a['lezart'])
        self.assertEqual(a['kulcs'], 'pr')
        self.assertEqual([p['szam'] for p in a['prok']], [10])

    def test_nyitott_sor_nem_mutat_egyesitett_prt(self):
        self.brief(5, allapot='fut')
        a = self.allapot(terv_sor(tetel='F5'), prok=[pr(10, 'F5: egy', piszkozat=True),
                                                       pr(9, 'F5: korábbi rész', merge='2026-11-13T10:00:00Z')])
        self.assertEqual([p['szam'] for p in a['prok']], [10])

    def test_pr_tetel(self):
        egyesitve = self.allapot(terv_sor(tetel='PR#9'), prok=[pr(9, 'x', merge='2026-11-13T10:00:00Z')])
        self.assertTrue(egyesitve['lezart'])
        nyitott = self.allapot(terv_sor(tetel='PR#10'), prok=[pr(10, 'x')])
        self.assertFalse(nyitott['lezart'])
        hianyzo = self.allapot(terv_sor(tetel='PR#11', kezi='csuszik: vár'), prok=[])
        self.assertIn('nem látszik', hianyzo['megjegyzes'])


class ModellTest(Alap):
    def test_lezart_tetel_csak_a_visszanezesben_all(self):
        self.brief(5, allapot='lezarva')
        self.brief(6, allapot='fut')
        terv = [terv_sor(sorrend=1, tetel='F5', cel='Lezárt cél'), terv_sor(sorrend=2, tetel='F6', cel='Nyitott cél'),
                terv_sor(sorrend=3, tetel='-', cel='Kézzel kész cél', kezi='kesz')]
        m = self.modell(terv)
        self.assertEqual([s['cel_a_het_vegere'] for s, _ in m['nyitott']], ['Nyitott cél'])
        self.assertEqual([s['cel_a_het_vegere'] for s, _ in m['kesz']], ['Lezárt cél', 'Kézzel kész cél'])
        oldal = self.oldal(m)
        sav = oldal[oldal.index('id="sav-content"'):oldal.index('id="keret"')]
        self.assertIn('Nyitott cél', sav)
        self.assertNotIn('Lezárt cél', sav)
        self.assertNotIn('Kézzel kész cél', sav)
        visszanezes = oldal[oldal.index('id="visszanezes"'):]
        self.assertIn('Lezárt cél', visszanezes)
        self.assertIn('Kézzel kész cél', visszanezes)
        teendok = oldal[oldal.index('id="teendok"'):oldal.index('id="sav-content"')]
        self.assertNotIn('Lezárt cél', teendok)

    def test_tervezett_keret_a_lezart_sort_is_szamolja(self):
        self.brief(5, allapot='lezarva')
        terv = [terv_sor(sorrend=1, tetel='F5', keret=40), terv_sor(sorrend=2, keret=15),
                terv_sor(sav='TARTALEK', keret=45)]
        k = self.modell(terv)['keret']
        self.assertEqual(k['CONTENT']['terv'], 55)
        self.assertEqual(k['TARTALEK']['terv'], 45)
        self.assertIsNone(k['CONTENT']['elhasznalt'])

    def test_elhasznalt_keret_a_tablabol(self):
        terv = [terv_sor(keret=60), terv_sor(sav='TARTALEK', keret=40)]
        keret = [{'het': HET.isoformat(), 'sav': 'CONTENT', 'elhasznalt_szazalek': '30', 'ts': '2026-11-15T10:00',
                  'forras': 'get_usage', '_sor': 2},
                 {'het': ELOZO.isoformat(), 'sav': 'CONTENT', 'elhasznalt_szazalek': '99', 'ts': '2026-11-14T10:00',
                  'forras': 'get_usage', '_sor': 3}]
        m = self.modell(terv, keret=keret)
        self.assertEqual(m['keret']['CONTENT'], {'terv': 60, 'elhasznalt': 30})
        self.assertIsNone(m['keret']['TARTALEK']['elhasznalt'])
        oldal = self.oldal(m)
        self.assertIn('nincs megadva', oldal)
        self.assertIn('30%', oldal)

    def test_teendok(self):
        self.brief(5, allapot='megallt', kovetkezo='"Te: a draft PR áttekintése"')
        terv = [terv_sor(sorrend=1, tetel='F5', cel='Az ötös', jov='javaslat'),
                terv_sor(sorrend=2, cel='Levél', megj='Te: a levél elküldése', jov='igen', sav='BUSINESS'),
                terv_sor(sorrend=3, cel='Nem teendő', megj='csak megjegyzés', jov='igen')]
        t = self.modell(terv)['teendok']
        szovegek = [x['szoveg'] for x in t]
        self.assertEqual(szovegek[0], 'A heti terv jóváhagyása')
        self.assertIn('Az ötös', szovegek)
        self.assertIn('Levél', szovegek)
        self.assertNotIn('Nem teendő', szovegek)

    def test_jovahagyott_terv_nem_ad_jovahagyasi_teendot(self):
        m = self.modell([terv_sor(keret=100, jov='igen')])
        self.assertEqual(m['teendok'], [])
        self.assertIn('jóváhagyott terv', self.oldal(m))

    def test_javaslat_jelzes_az_oldalon(self):
        oldal = self.oldal(self.modell([terv_sor(keret=100)]))
        self.assertIn('javaslat: még nincs jóváhagyva', oldal)
        self.assertIn('2026. november 14. 14:00 UTC', oldal)

    def test_visszanezes_az_elozo_hetrol(self):
        self.brief(5, allapot='lezarva')
        terv = [terv_sor(het=ELOZO, sorrend=1, tetel='F5', cel='Teljesült cél'),
                terv_sor(het=ELOZO, sorrend=2, cel='Átcsúszott cél', kezi='csuszik: a #7 miatt'),
                terv_sor(het=ELOZO, sorrend=3, cel='Elhagyott cél', kezi='elhagyva: nem kell'),
                terv_sor(het=HET, sorrend=1, cel='Mostani cél')]
        m = self.modell(terv)
        self.assertEqual([k for _, _, k in m['visszanezes']], ['teljesült', 'csúszott át', 'elhagyva'])
        oldal = self.oldal(m)
        visszanezes = oldal[oldal.index('id="visszanezes"'):]
        for cel in ('Teljesült cél', 'Átcsúszott cél', 'Elhagyott cél'):
            self.assertIn(cel, visszanezes)
        self.assertNotIn('Mostani cél', visszanezes)
        self.assertIn('a #7 miatt', visszanezes)

    def test_nincs_elozo_het(self):
        oldal = self.oldal(self.modell([terv_sor(keret=100)]))
        self.assertIn('ez az első hét', oldal)

    def test_felmerendo_otlet_a_felmeres_savban(self):
        otlet = [{'id': 'OT001', 'sav': 'SERVER', 'cim': 'Felmérendő ötlet', 'forras': 'a felhasználó, 2026-11-15',
                  'allapot': 'felmerendo', 'megjegyzes': '', '_sor': 2},
                 {'id': 'OT002', 'sav': 'SERVER', 'cim': 'Csak ötlet', 'forras': 'x', 'allapot': 'otlet',
                  'megjegyzes': '', '_sor': 3},
                 {'id': 'OT003', 'sav': 'SERVER', 'cim': 'Elvetett ötlet', 'forras': 'x', 'allapot': 'elvetve: DT1',
                  'megjegyzes': '', '_sor': 4}]
        m = self.modell([terv_sor(sav='FELMERES', keret=100, cel='Felmérés')], otlet=otlet)
        oldal = self.oldal(m)
        sav = oldal[oldal.index('id="sav-felmeres"'):oldal.index('id="keret"')]
        self.assertIn('Felmérendő ötlet', sav)
        self.assertNotIn('Csak ötlet', sav)
        self.assertNotIn('Elvetett ötlet', sav)
        self.assertIn('Ötlettár: 3 tétel', oldal)

    def test_backtick_nem_kerul_az_oldalra(self):
        oldal = self.oldal(self.modell([terv_sor(keret=100, cel='A `jovahagyva` mező', megj='lásd `PR#1`')]))
        self.assertNotIn('`', oldal.split('</style>')[1])

    def test_html_escape(self):
        oldal = self.oldal(self.modell([terv_sor(keret=100, cel='<b>x</b> & y')]))
        self.assertNotIn('<b>x</b>', oldal)
        self.assertIn('&lt;b&gt;x&lt;/b&gt; &amp; y', oldal)

    def test_ures_het(self):
        oldal = self.oldal(self.modell([terv_sor(het=ELOZO, keret=100)]))
        self.assertIn('Nincs terv erre a hétre', oldal)


class MeresIntegracioTest(Alap):
    """A mért keretfogyás (keret_meres) beillesztése: a kézi érték erősebb, a mért sávok terv nélkül is látszanak."""

    @staticmethod
    def meres(szazalek=None):
        def sav(egyseg, uzenet=1, sz=None, top=None):
            return {'egyseg': egyseg, 'fable_egyseg': 0.0, 'uzenet': uzenet, 'arany': egyseg / 100.0, 'szazalek': sz,
                    'fable_szazalek': None, 'top': top or [('SYSTEMS · A', egyseg, 'a session címe')], 'session': {}}
        return {'savok': {'SYSTEMS': sav(60, sz=szazalek and 6.0), 'CONTENT': sav(30, sz=szazalek and 3.0),
                          'ORKESZTRACIO': sav(10, sz=szazalek and 1.0), 'ISMERETLEN': sav(0, uzenet=0)},
                'osszes': 100.0, 'osszes_szazalek': szazalek, 'fable_osszes': 0.0, 'fable_osszes_szazalek': None,
                'kalibralas': {'heti': None if szazalek is None else 0.1, 'fable': None, 'pontok': 0 if szazalek is None else 1},
                'uzenet_db': 3, 'session_db': 2, 'ismeretlen_modell': {}}

    def test_merttel_kalibralas_nelkul_csak_arany(self):
        m = B.epit([terv_sor(sav='SYSTEMS', keret=60), terv_sor(sav='CONTENT', keret=40)], [], [], [], {}, [], DT, meres=self.meres())
        self.assertIsNone(m['keret']['SYSTEMS']['elhasznalt'])
        self.assertAlmostEqual(m['keret']['SYSTEMS']['arany'], 0.6)
        oldal = self.oldal(m)
        self.assertIn('nincs kalibrálva', oldal)
        self.assertIn('Mért arány', oldal)
        self.assertIn('Legnagyobb fogyasztók a sávon belül', oldal)

    def test_kalibralt_szazalek_kitolti_az_elhasznaltat(self):
        m = B.epit([terv_sor(sav='SYSTEMS', keret=60), terv_sor(sav='CONTENT', keret=40)], [], [], [], {}, [], DT,
                   meres=self.meres(szazalek=10.0))
        self.assertEqual(m['keret']['SYSTEMS']['elhasznalt'], 6.0)
        self.assertEqual(m['keret']['SYSTEMS']['forras'], 'mért')
        self.assertIn('(mért)', self.oldal(m))

    def test_kezi_ertek_erosebb_a_mertnel(self):
        keret = [{'het': HET.isoformat(), 'sav': 'SYSTEMS', 'elhasznalt_szazalek': '9', 'ts': '2026-11-15T10:00',
                  'forras': 'kézi', '_sor': 2}]
        m = B.epit([terv_sor(sav='SYSTEMS', keret=100)], keret, [], [], {}, [], DT, meres=self.meres(szazalek=10.0))
        self.assertEqual(m['keret']['SYSTEMS']['elhasznalt'], 9)
        self.assertEqual(m['keret']['SYSTEMS']['forras'], 'kézi')

    def test_mert_de_nem_tervezett_sav_terv_nelkul_latszik(self):
        m = B.epit([terv_sor(sav='SYSTEMS', keret=100)], [], [], [], {}, [], DT, meres=self.meres(szazalek=10.0))
        self.assertIn('ORKESZTRACIO', m['keret'])
        self.assertIsNone(m['keret']['ORKESZTRACIO']['terv'])
        self.assertNotIn('ISMERETLEN', m['keret'])      # üzenet nélküli, nem tervezett sáv nem kerül a táblába
        oldal = self.oldal(m)
        self.assertIn('Orkesztráció', oldal)
        self.assertIn('nincs tervezve', oldal)

    def test_meres_nelkul_a_regi_viselkedes(self):
        m = self.modell([terv_sor(sav='SYSTEMS', keret=100)])
        self.assertNotIn('arany', m['keret']['SYSTEMS'])
        self.assertIn('nincs bekapcsolva', self.oldal(m))


class CliTest(Alap):
    def test_repon_beluli_kimenet_elutasitva(self):
        self.assertTrue(B._repon_belul(os.path.join(F.REPO, 'x.html'), F.REPO))
        self.assertFalse(B._repon_belul(os.path.join(self.ut, 'x.html'), F.REPO))

    def test_ellenoriz_a_valos_tablakon(self):
        self.assertEqual(B.main(['--ellenoriz']), 0)


if __name__ == '__main__':
    unittest.main(verbosity=1)
