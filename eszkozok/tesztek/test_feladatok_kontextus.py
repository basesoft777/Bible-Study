#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_feladatok_kontextus.py -- F32_KONTEXTUS_BRIEF.md: a `munka` mező, a `csomag`
alparancs (K3.1), az OLVAS_HIANY (K3.2) és a `munka` nélküli, motívumfájlt író brief
E18 fejléchibája (az előzmény-briefek F09/F35 csak FIGYELEM). A `lexikon/` generált
kimenet, nem motívumfájl (DT28): az újragenerálása `adat` munka, csomagolható.

A fixture-ek repón kívüli ideiglenes könyvtárban vannak (`--gyoker`).

Futtatás: python eszkozok/tesztek/test_feladatok_kontextus.py
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import feladatok as F  # noqa: E402
from test_feladatok_fugges import Fixture, brief_szoveg  # noqa: E402

TANULMANY = 'tematikus_lezart/TEREMT-002_tematikus.md'
NAPLO = 'tematikus_lezart/naplok/TEREMT-002_kereszthivatkozas_naplo.md'
MOTIVUM = 'motivumok/TEREMT-002.md'

EXTRA_MUNKA_NELKUL = ('---\ncim: x\ntipus: feladat\nfazis: 1\nmodell: sonnet\n'
                      'allapot: nem_indult\nad: a\nkovetkezo: k\nolvas: [a]\n'
                      'ir: [motivumok/]\n---\n')


class KontextusTest(Fixture):
    def brief(self, szam, munka=None, **kw):
        """A Fixture.brief a `munka` mezőt nem ismeri: a fejlécbe utólag szúrjuk be."""
        nev = 'F%02d_T%d_BRIEF.md' % (szam, szam)
        szoveg = brief_szoveg(szam, **kw)
        if munka is not None:
            szoveg = szoveg.replace('\nmodell: sonnet\n', '\nmodell: sonnet\nmunka: %s\n' % munka, 1)
        with open(os.path.join(self.ut, nev), 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)

    def cli(self, *args):
        ki = io.StringIO()
        with redirect_stdout(ki):
            rc = F.main(['--gyoker', self.ut] + list(args))
        return rc, ki.getvalue()

    # --- csomag (K3.1) ---

    def test_adat_csomagolhato(self):
        self.brief(92, munka='adat', olvas=['a'], ir=['adat/y.tsv'])
        rc, ki = self.cli('csomag', '92')
        self.assertEqual(rc, 0)
        self.assertIn('CSOMAGOLHATO\t#92\tmunka: adat', ki)

    def test_folyamat_motivum_nelkul_csomagolhato(self):
        self.brief(93, munka='folyamat', olvas=['a'], ir=['BRIEF_SABLON.md'])
        self.assertEqual(self.cli('csomag', '93')[0], 0)

    def test_munka_nelkuli_nem_motivumot_iro_adatnak_szamit(self):
        self.brief(96, olvas=['a'], ir=['adat/y.tsv'])
        rc, ki = self.cli('csomag', '96')
        self.assertEqual(rc, 0)
        self.assertIn('adat (alapértelmezés)', ki)

    def test_ertelmezo_nem_csomagolhato(self):
        self.brief(90, munka='ertelmezo', olvas=[TANULMANY, NAPLO], ir=[MOTIVUM])
        rc, ki = self.cli('csomag', '90')
        self.assertEqual(rc, 1)
        self.assertIn('NEM_CSOMAGOLHATO\t#90', ki)

    def test_folyamat_motivumfajlt_irva_nem_csomagolhato(self):
        self.brief(94, munka='folyamat', olvas=[TANULMANY, NAPLO],
                   ir=['tematikus_lezart/TEREMT-002_javitas.md'])
        self.assertEqual(self.cli('csomag', '94')[0], 1)

    def test_munka_nelkuli_motivumot_iro_nem_csomagolhato(self):
        self.brief(95, olvas=['a'], ir=['tematikus_lezart/'])
        rc, ki = self.cli('csomag', '95')
        self.assertEqual(rc, 1)
        self.assertIn('hiányzó `munka` mező', ki)

    # --- DT28: a lexikon/ generált kimenet, nem motívumfájl ---

    def test_lexikon_ujrageneralas_folyamat_csomagolhato(self):
        """`munka: folyamat` + `lexikon/[ID]*` az `ir`-ben: nem motívumot ír, csomagolható;
        a K3.2 (olvas) viszont az adatfüggés miatt továbbra is kéri a tanulmányt és a naplót."""
        self.brief(94, munka='folyamat', olvas=['a'], ir=['lexikon/TEREMT-002_TUDOMANYOS.md'])
        self.assertEqual(self.cli('csomag', '94')[0], 0)
        self.assertEqual(len(F.kontextus_hibak(self.briefek()[0])), 2)
        self.assertFalse(F.motivumot_ir(self.briefek()[0]))

    def test_lexikon_ujrageneralas_munka_nelkul_adat(self):
        """A #36 alakja: `munka` nélkül, `ir: [lexikon/, generalt_proba/]` -- nincs E18, csomagolható `adat`-ként."""
        self.brief(36, olvas=['lexikon/', 'adat/res_forras.tsv'], ir=['lexikon/', 'generalt_proba/'])
        self.assertEqual(self.hibak(), [])
        self.assertEqual(F.figyelmeztetesek(self.briefek(), {}), [])
        rc, ki = self.cli('csomag', '36')
        self.assertEqual(rc, 0)
        self.assertIn('adat (alapértelmezés)', ki)
        self.assertNotIn(36, F.MUNKA_ELOZMENY)

    def test_vegyes_csomag_egy_rossz_miatt_1(self):
        self.brief(92, munka='adat', olvas=['a'], ir=['adat/y.tsv'])
        self.brief(90, munka='ertelmezo', olvas=[TANULMANY, NAPLO], ir=[MOTIVUM])
        rc, ki = self.cli('csomag', '92', '90')
        self.assertEqual(rc, 1)
        self.assertIn('CSOMAGOLHATO\t#92', ki)
        self.assertIn('NEM_CSOMAGOLHATO\t#90', ki)

    def test_nincs_ilyen_feladat(self):
        rc, ki = self.cli('csomag', '77')
        self.assertEqual(rc, 1)
        self.assertIn('nincs ilyen feladat', ki)

    # --- OLVAS_HIANY (K3.2) ---

    def test_olvas_teljes_nincs_hiany(self):
        self.brief(90, munka='ertelmezo', olvas=[TANULMANY, NAPLO], ir=[MOTIVUM])
        self.assertEqual(F.kontextus_hibak(self.briefek()[0]), [])
        self.assertEqual(self.hibak(), [])
        rc, ki = self.cli('fuggesek')
        self.assertEqual(rc, 0)
        self.assertNotIn('OLVAS_HIANY', ki)

    def test_teremt002_naplo_hianyzik(self):
        self.brief(91, munka='ertelmezo', olvas=[TANULMANY], ir=[MOTIVUM])
        hibak = F.kontextus_hibak(self.briefek()[0])
        self.assertEqual(len(hibak), 1)
        self.assertIn('kereszthivatkozás-napló', hibak[0])
        self.assertIn('tematikus_lezart/naplok/TEREMT-002', hibak[0])
        rc, ki = self.cli('fuggesek')
        self.assertEqual(rc, 1)
        self.assertIn('OLVAS_HIANY\t91', ki)
        self.assertEqual(self.cli('ellenoriz')[0], 1)

    def test_javito_kor_is_olvassa_az_egeszet(self):
        self.brief(97, munka='ertelmezo', olvas=['adat/x'],
                   ir=['tematikus_lezart/TEREMT-002_javitas.md'])
        self.assertEqual(len(F.kontextus_hibak(self.briefek()[0])), 2)

    def test_konyvtar_olvas_lefedi(self):
        self.brief(98, munka='ertelmezo', olvas=['tematikus_lezart/'], ir=[MOTIVUM])
        self.assertEqual(F.kontextus_hibak(self.briefek()[0]), [])

    def test_konyvtar_ir_id_nelkul_nem_olvas_hiany(self):
        self.brief(99, munka='adat', olvas=['a'], ir=['lexikon/'])
        self.assertEqual(F.kontextus_hibak(self.briefek()[0]), [])

    # --- munka mező értékkészlet, E18 hiány ---

    def test_ervenytelen_munka_ertek_hiba(self):
        self.brief(92, munka='valami', olvas=['a'], ir=['adat/y.tsv'])
        self.assertTrue(any('munka:' in u for _, u in self.hibak()))

    def test_munka_nelkuli_motivumot_iro_uj_brief_E18_hiba(self):
        self.brief(95, olvas=['a'], ir=['tematikus_lezart/'])
        self.assertTrue(any('E18' in u and 'munka' in u for _, u in self.hibak()))
        rc, ki = self.cli('ellenoriz')
        self.assertEqual(rc, 1)
        self.assertIn('HIBA\tF95_T95_BRIEF.md\tE18', ki)
        rc, ki = self.cli('fuggesek')
        self.assertEqual(rc, 1)
        self.assertIn('MUNKA_HIANY\t95', ki)

    def test_munka_kitoltve_nincs_hiba(self):
        self.brief(95, munka='adat', olvas=['a'], ir=['tematikus_lezart/'])
        self.assertEqual(self.hibak(), [])

    def test_elozmeny_brief_csak_figyelem(self):
        """A mechanizmus egy nem lezárt előzmény-brieffel (a 35 alakja, `nem_indult` állapotban)."""
        self.assertEqual(tuple(sorted(F.MUNKA_ELOZMENY)), (35,))
        self.brief(35, olvas=['a'], ir=['genezis/'])
        self.assertEqual(self.hibak(), [])
        fig = F.figyelmeztetesek(self.briefek(), {})
        self.assertTrue(any('E18' in u for _, u in fig))
        rc, ki = self.cli('ellenoriz')
        self.assertEqual(rc, 0)
        self.assertIn('FIGYELEM\tF35_T35_BRIEF.md\tE18', ki)
        rc, ki = self.cli('fuggesek')
        self.assertEqual(rc, 0)
        self.assertIn('FIGYELEM\t35\t-\tE18', ki)
        # az előzmény-brief sem csomagolható, amíg a mező nincs kitöltve
        self.assertEqual(self.cli('csomag', '35')[0], 1)
        # és nem is jelölt (DT-F32c, 1. opció)
        ok = F.jeloltek(self.briefek(), {}).get(35)
        self.assertIsNotNone(ok)
        self.assertIn('DT-F32c', ok)

    def test_9_mar_nem_elozmeny(self):
        """A 9 kikerült a kivételből (2026.10.06): `munka` nélkül, motívumfájllal már E18 hiba."""
        self.assertNotIn(9, F.MUNKA_ELOZMENY)
        self.brief(9, olvas=['a'], ir=['lexikon/', 'tematikus_lezart/Segitsegul_tematikus.md'])
        self.assertTrue(any('E18' in u for _, u in self.hibak()))

    def test_elozmeny_brief_kitoltve_jelolt(self):
        self.brief(9, munka='ertelmezo', olvas=['a'], ir=['lexikon/', 'tematikus_lezart/Segitsegul_tematikus.md'])
        self.assertIsNone(F.jeloltek(self.briefek(), {}).get(9))

    def test_lezart_elozmeny_nem_jelez(self):
        self.brief(35, allapot='lezarva', olvas=['a'], ir=['genezis/'])
        self.assertEqual(F.figyelmeztetesek(self.briefek(), {}), [])
        self.assertEqual(self.hibak(), [])

    def test_extra_javasolt_fejlec_E18(self):
        """A befogadás (`fuggesek --extra`) a munka nélküli, motívumot író javaslatot elutasítja."""
        ex = os.path.join(self.ut, 'kivul.md')
        with open(ex, 'w', encoding='utf-8') as f:
            f.write(EXTRA_MUNKA_NELKUL)
        rc, ki = self.cli('fuggesek', '--extra', ex)
        self.assertEqual(rc, 1)
        self.assertIn('MUNKA_HIANY', ki)


if __name__ == '__main__':
    unittest.main(verbosity=1)
