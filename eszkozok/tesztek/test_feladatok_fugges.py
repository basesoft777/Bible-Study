#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_feladatok_fugges.py -- F39_ORKESZTRATOR_FUGGES_BRIEF.md (M2): a `feladatok.py`
függés-levezetésének tesztjei, a 2026.10.01-i állapotot visszajátszó fixture-ekkel.

Futtatás: python eszkozok/tesztek/test_feladatok_fugges.py
(az `eszkozok/teszt_feladatok.py` is lefuttatja, ez a CI-útvonal)
"""

import os
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import feladatok as F  # noqa: E402


def _lista(x):
    return '[%s]' % ', '.join(str(i) for i in x)


def brief_szoveg(szam, olvas=(), ir=(), fugg=None, nem_fugg=None, fazis='1',
                 allapot='nem_indult', kovetkezo='következő lépés', kod=None):
    sorok = ['---', 'feladat: %d' % szam, 'cim: Teszt %d' % szam]
    if kod:
        sorok.append('kod: %s' % kod)
    sorok += ['tipus: feladat', 'fazis: %s' % fazis, 'modell: sonnet', 'allapot: %s' % allapot,
              'ad: mit ad', 'kovetkezo: %s' % kovetkezo,
              'olvas: %s' % _lista(olvas), 'ir: %s' % _lista(ir)]
    if fugg is not None:
        sorok.append('fugg: %s' % _lista(fugg))
    if nem_fugg is not None:
        sorok.append('nem_fugg: %s' % _lista(nem_fugg))
    sorok += ['---', '', '# Teszt %d' % szam, '']
    return '\n'.join(sorok)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ut = self.tmp.name

    def brief(self, szam, **kw):
        nev = 'F%02d_T%d_BRIEF.md' % (szam, szam)
        with open(os.path.join(self.ut, nev), 'w', encoding='utf-8', newline='') as f:
            f.write(brief_szoveg(szam, **kw))

    def briefek(self):
        return F.briefek_beolvas(self.ut)

    def fugg(self):
        return F.fuggesek(self.briefek(), {})

    def hibak(self):
        return F.ellenoriz(self.briefek(), self.ut)

    def mai_allapot(self):
        """A 2026.10.01-i állapot releváns részlete (#7, #9, #30, #35, #37, #38)."""
        self.brief(7, allapot='brief_kell', kovetkezo='halasztva (D46): a Thayer gépi fordítása',
                   olvas=['adat/forditasok.tsv'], ir=['adat/forditasok.tsv'])
        self.brief(9, fazis='2', olvas=['adat/forditasok.tsv', 'lexikon/'],
                   ir=['lexikon/', 'adat/forditasok.tsv', 'naplok/ELLENOR_SZOTAR.md'])
        self.brief(30, kod='SZAMOZAS', olvas=['.github/workflows/', 'CLAUDE.md'],
                   ir=['CLAUDE.md', 'eszkozok/ellenorzes/szabalyok.py',
                       '.github/workflows/ellenorzes.yml', 'naplok/ELLENOR_SZAMOZAS.md'])
        self.brief(35, kod='SIR_SZENTSZELLEM', olvas=['naplok/EMELES_szentlelek_lista.tsv'],
                   ir=['genezis/', 'tematikus_lezart/', 'naplok/ELLENOR_SIR.md'])
        self.brief(37, fazis='folyamat', kod='TANULMANY_ELLENORZES',
                   olvas=['sablonok/', 'genezis/', 'tematikus_lezart/', 'adat/',
                          'eszkozok/ellenorzes/', 'CLAUDE.md'],
                   ir=['eszkozok/ellenorzes/', 'naplok/'])
        self.brief(38, kod='BDB_FORDITAS', olvas=['adat/forditasok.tsv',
                                                 'naplok/EMELES_naplo.md'],
                   ir=['adat/forditasok.tsv', 'naplok/BDB_FORDITAS_naplo.md',
                       'naplok/ELLENOR_BDB.md'])


class MaiAllapotTest(Fixture):
    def test_nincs_35_37_es_30_37_kor(self):
        self.mai_allapot()
        fugg = self.fugg()[0]
        self.assertNotIn(37, fugg[35])
        self.assertNotIn(37, fugg[30])
        self.assertEqual(F.korok(fugg), [])
        self.assertEqual(self.hibak(), [])

    def test_38_nem_var_a_7_re_es_a_9_re(self):
        self.mai_allapot()
        fugg, kizar, _, _ = self.fugg()
        self.assertEqual(fugg[38], {})
        self.assertFalse([k for k in kizar if 38 in k[:2] and (7 in k[:2] or 9 in k[:2])])

    def test_ellenor_naplok_nem_utkoznek(self):
        self.mai_allapot()
        kizar = self.fugg()[1]
        self.assertFalse([k for k in kizar if 'ELLENOR' in k[2]])
        # a 35 és a 38 mindketten naplok/ELLENOR_*-t írnak
        self.assertFalse([k for k in kizar if set(k[:2]) == {35, 38}])

    def test_helyettesito_figyelmeztetes(self):
        self.mai_allapot()
        fig = F.figyelmeztetesek(self.briefek(), {})
        self.assertTrue(any('F37_' in f and 'konkrét fájlt' in u for f, u in fig))

    def test_jeloltek(self):
        self.mai_allapot()
        j = F.jeloltek(self.briefek(), {})
        self.assertIsNone(j[35])
        self.assertIsNone(j[38])
        self.assertIsNotNone(j[7])


class SzabalyTest(Fixture):
    def test_valodi_iras_olvasas_marad(self):
        self.brief(1, olvas=['adat/x.tsv'], ir=['a.txt'])
        self.brief(2, olvas=['b.txt'], ir=['adat/x.tsv'])
        fugg, kizar, _, _ = self.fugg()
        self.assertEqual(fugg[1][2], ('levezetett', 'adat/x.tsv'))
        self.assertEqual(kizar, [])
        self.assertIsNotNone(F.jeloltek(self.briefek(), {})[1])

    def test_kontextus_olvasas_nem_ad_sorrendet(self):
        self.brief(1, olvas=['adat/', 'CLAUDE.md', 'BRIEF_SABLON.md', 'MUNKAMENET.md'], ir=['a'])
        self.brief(2, olvas=['b'], ir=['adat/x.tsv', 'CLAUDE.md', 'BRIEF_SABLON.md',
                                       'MUNKAMENET.md'])
        self.assertEqual(self.fugg()[0][1], {})

    def test_iras_iras_kizaras_csak_futo_ellen_blokkol(self):
        self.brief(1, olvas=['q'], ir=['adat/x.tsv'])
        self.brief(2, olvas=['r'], ir=['adat/x.tsv'])
        _, kizar, _, sorrend = self.fugg()
        self.assertEqual([k[:2] for k in kizar], [(1, 2)])
        self.assertEqual(sorrend[0][:2], (1, 2))
        j = F.jeloltek(self.briefek(), {})
        self.assertIsNone(j[1])
        self.assertIsNone(j[2])           # nincs futó pár: mindkettő jelölt
        self.assertEqual(F.csomag(self.briefek(), {}), [1])   # de egy csomagba nem kerülnek
        self.brief(1, olvas=['q'], ir=['adat/x.tsv'], allapot='fut')
        j = F.jeloltek(self.briefek(), {})
        self.assertIn('kizár', j[2])

    def test_kolcsonos_iras_olvasas_kizaras_figyelmeztetessel(self):
        self.brief(1, olvas=['adat/b.tsv'], ir=['adat/a.tsv'])
        self.brief(2, olvas=['adat/a.tsv'], ir=['adat/b.tsv'])
        fugg, kizar, _, _ = self.fugg()
        self.assertEqual(fugg, {1: {}, 2: {}})
        self.assertEqual([k[:2] for k in kizar], [(1, 2)])
        szoveg = F.fuggesek_szoveg(self.briefek(), {})
        self.assertIn('kölcsönös függés: #1 ↔ #2', szoveg)
        self.assertEqual(self.hibak(), [])

    def test_explicit_fugg_nem_valik_kizarra(self):
        # a 1 explicit függ a 2-től, és a 2 levezetetten olvassa az 1 kimenetét is
        self.brief(1, fugg=[2], olvas=['adat/b.tsv'], ir=['adat/a.tsv'])
        self.brief(2, olvas=['adat/a.tsv'], ir=['adat/b.tsv'])
        fugg, kizar, _, _ = self.fugg()
        self.assertIn(2, fugg[1])           # az explicit él marad sorrendi
        self.assertEqual(kizar, [])
        self.assertTrue(any('függési kör' in u for _, u in self.hibak()))

    def test_kolcsonos_par_plusz_kozvetett_el_kor(self):
        # 1↔2 kölcsönös, de 1→3 és 3→2 is: a háromtagú kör hiba marad
        self.brief(1, olvas=['adat/b.tsv', 'adat/c.tsv'], ir=['adat/a.tsv'])
        self.brief(2, olvas=['adat/a.tsv'], ir=['adat/b.tsv'])
        self.brief(3, olvas=['adat/b.tsv'], ir=['adat/c.tsv'])
        self.assertTrue(any('függési kör' in u for _, u in self.hibak()))

    def test_harmas_kor_hiba(self):
        self.brief(1, olvas=['adat/b.tsv'], ir=['adat/a.tsv'])
        self.brief(2, olvas=['adat/c.tsv'], ir=['adat/b.tsv'])
        self.brief(3, olvas=['adat/a.tsv'], ir=['adat/c.tsv'])
        self.assertTrue(any('függési kör' in u for _, u in self.hibak()))

    def test_explicit_kor_hiba(self):
        self.brief(1, fugg=[2])
        self.brief(2, fugg=[1])
        self.assertTrue(any('függési kör' in u for _, u in self.hibak()))

    def test_explicit_fugg_2_fazisura_figyelmeztet(self):
        self.brief(1, fugg=[2])
        self.brief(2, fazis='2')
        fig = F.figyelmeztetesek(self.briefek(), {})
        self.assertTrue(any('D1' in u for _, u in fig))
        self.assertIn(2, self.fugg()[0][1])      # nem javítja automatikusan

    def test_2_fazisu_nem_ad_levezetett_kapcsolatot(self):
        self.brief(1, olvas=['adat/x.tsv'], ir=['a'])
        self.brief(2, fazis='2', olvas=['b'], ir=['adat/x.tsv'])
        fugg, kizar, _, _ = self.fugg()
        self.assertEqual(fugg[1], {})
        self.assertEqual(kizar, [])


if __name__ == '__main__':
    unittest.main(verbosity=1)
