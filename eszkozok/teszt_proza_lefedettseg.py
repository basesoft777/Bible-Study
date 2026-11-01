#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F125: az eszkozok/proza_lefedettseg.py es az ellenoriz.py 22-23. szabalyanak tesztjei.
Ideiglenes (a repon kivuli) gyokerben fut.

    python eszkozok/teszt_proza_lefedettseg.py
"""
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

import ellenoriz as E  # noqa: E402
import proza_lefedettseg as PL  # noqa: E402

EL_FEJ = 'id\tigehely\tpardes_szint\n'
KAP_FEJ = 'forras_igehely\tcel_igehely\tid\ttipus\n'
MK_FEJ = 'id_a\tigehely_a\talpont_a\tid_b\tigehely_b\talpont_b\ttipus\n'
JEL_FEJ = 'id\tigehely\tdontes\tjelolt_tipus\tindoklas\n'


class Alap(unittest.TestCase):
    def setUp(self):
        self.gy = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.gy, 'adat'))
        os.makedirs(os.path.join(self.gy, 'motivumok'))
        os.makedirs(os.path.join(self.gy, 'lexikon'))

    def tearDown(self):
        shutil.rmtree(self.gy, ignore_errors=True)

    def ir(self, rel, szoveg):
        with open(os.path.join(self.gy, rel), 'w', encoding='utf-8', newline='') as f:
            f.write(szoveg)

    def adat(self, el, kap='', mk='', jel=''):
        self.ir('adat/elofordulasok.tsv', EL_FEJ + el)
        self.ir('adat/kapcsolatok.tsv', '# k\n' + KAP_FEJ + kap)
        self.ir('adat/motivum_kapcsolatok.tsv', '# m\n' + MK_FEJ + mk)
        self.ir('adat/jeloltek.tsv', '# j\n' + JEL_FEJ + jel)


class TesztLefedettseg(Alap):
    def test_megnevezett_es_hianyzo(self):
        self.adat('T-001\t1Móz 12:8\tPeshat\nT-001\tZsolt 99:1\tPeshat\n')
        self.ir('motivumok/T-001.md', '# T\n\n## 1. Rész\n\nAz 1Móz 12:8 oltárt említ.\n')
        o = PL.osszesit('T-001', self.gy)
        self.assertEqual(o['el'], (2, 1, 0, 1))

    def test_versszam_tartomany_es_puszta_fejezet_vers(self):
        self.adat('T-001\t1Móz 14:18-20\tPeshat\nT-001\tZsolt 116:4,13,17\tPeshat\n')
        self.ir('motivumok/T-001.md', '## Rész\n\nAz 1Móz 14:19 áldás; a Zsolt 116 egy bekezdésében a 13. vers: 116:13.\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['el'][1], 2)

    def test_tabla_naplo_jelolo_nem_proza(self):
        self.adat('T-001\t1Móz 12:8\tPeshat\n')
        self.ir('motivumok/T-001.md', '## Rész\n\n| 1Móz 12:8 | x |\n\n【NAPLO: 1Móz 12:8】\n\n<!-- 1Móz 12:8 -->\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['el'], (1, 0, 0, 1))

    def test_csoportos_emlites_kulon_kategoria(self):
        self.adat('T-001\t1Móz 37:35\tRemez\nT-001\tJób 7:9\tRemez\n')
        self.ir('motivumok/T-001.md', '## Rész\n\nA szó még 63 egyedi igehelyen fordul elő.\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['el'], (2, 0, 2, 0))

    def test_csoportos_darabszam_felso_korlat(self):
        # TEREMT-002 tipus: „3 igehelyen” a prozaban, de 5 nev nelkuli elofordulas -> 3 fedett, 2 hiany
        sorok = ''.join(f'T-001\t1Móz 1:{i}\tRemez\n' for i in range(1, 6))
        self.adat(sorok)
        self.ir('motivumok/T-001.md', '## Rész\n\nEz 3 igehelyen fordul elő.\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['el'], (5, 0, 3, 2))

    def test_csoportos_ALVIL_eset_63_legalabb_57(self):
        # 63 >= 57 hiany -> mind a 57 fedett, hiany 0 (az ALVIL-001 valtozatlan merese)
        sorok = ''.join(f'T-001\tJób {i}:1\tRemez\n' for i in range(1, 58))
        self.adat(sorok)
        self.ir('motivumok/T-001.md', '## Rész\n\nA szó még 63 egyedi igehelyen fordul elő.\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['el'], (57, 0, 57, 0))

    def test_csoportos_csak_elofordulasra(self):
        self.adat('T-001\t1Móz 37:35\tRemez\n', kap='1Móz 1:1\t1Móz 2:2\tT-001\tPárhuzam\n')
        self.ir('motivumok/T-001.md', '## Rész\n\n63 egyedi igehelyen.\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['kap'], (1, 0, 0, 1))

    def test_kapcsolat_mindket_vegevel(self):
        self.adat('', kap='1Móz 4:26\tJóel 2:32\tT-001\tPárhuzam\n1Móz 4:26\tSof 3:9\tT-001\tPárhuzam\n')
        self.ir('motivumok/T-001.md', '## Rész\n\nAz 1Móz 4:26 és a Jóel 2:32 párhuzam.\n')
        self.assertEqual(PL.osszesit('T-001', self.gy)['kap'], (2, 1, 0, 1))

    def test_motivumkozi_es_nyitott(self):
        self.adat('', mk='A-001\tZsolt 1:1\t\tT-001\tÉzs 2:2\t\tszomszédos\n',
                  jel='T-001\tÉzs 41:25\tnyitva\telofordulas\tkérdéses\nT-001\tÉzs 9:9\tbeépítve\telofordulas\tx\n')
        self.ir('motivumok/T-001.md', '## Rész\n\nAz A-001 motívummal rokon.\n')
        o = PL.osszesit('T-001', self.gy)
        self.assertEqual(o['mk'], (1, 1, 0, 0))
        self.assertEqual(o['nyit'], (1, 0, 0, 1))


class TesztSzabaly(Alap):
    def test_23_jelentes_nem_sertes(self):
        self.adat('T-001\t1Móz 12:8\tPeshat\n')
        self.ir('motivumok/T-001.md', '## Rész\n\nSemmi.\n')
        s = E.szabaly23_proza_lefedettseg(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertEqual(s.n, 1)

    def test_23_rendben(self):
        self.adat('T-001\t1Móz 12:8\tPeshat\n')
        self.ir('motivumok/T-001.md', '## Rész\n\nAz 1Móz 12:8 oltár.\n')
        self.assertEqual(E.szabaly23_proza_lefedettseg(os.path.join(self.gy, 'adat')).verdict, 'RENDBEN')

    def test_22_kiejtes_nelkuli_szo(self):
        self.ir('lexikon/T-001_TUDOMANYOS.md', '## Rész\n\nA ἐπικατάρατος szó itt áll.\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'JELENTÉS')

    def test_22_kiejtessel_rendben(self):
        self.ir('lexikon/T-001_TUDOMANYOS.md', '## Rész\n\nA ἐπικατάρατος (epikatáratosz) szó itt áll.\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'RENDBEN')

    def test_22_szakaszban_bar_egy_kiejtes_elég(self):
        # DT-F125b: az elso elofordulas kiejtes nelkul, a masodik kiejtessel -> nincs jelzes (a regi kod jelzett)
        self.ir('lexikon/T-001_TUDOMANYOS.md',
                '## Rész\n\nA ἐπικατάρατος szó itt áll, majd ἐπικατάρατος (epikatáratosz) újra.\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'RENDBEN')

    def test_22_szakaszban_egyszer_sem_jelez(self):
        self.ir('lexikon/T-001_TUDOMANYOS.md',
                '## Rész\n\nA ἐπικατάρατος szó, majd ἐπικατάρατος újra, kiejtés nélkül.\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertEqual(s.n, 1)

    def test_22_masik_szakasz_kiejtese_nem_potol(self):
        self.ir('lexikon/T-001_TUDOMANYOS.md',
                '## A\n\nἐπικατάρατος (epikatáratosz).\n\n## B\n\nἐπικατάρατος.\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertEqual(s.n, 1)

    def test_22_tanulmanyon_is_jelez(self):
        os.makedirs(os.path.join(self.gy, 'tematikus_lezart'))
        self.ir('tematikus_lezart/Teszt_tematikus.md', '## Rész\n\nA ἐπικατάρατος szó itt áll.\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'JELENTÉS')
        self.assertIn('tematikus_lezart/Teszt_tematikus.md', ' '.join(s.peldak))

    def test_22_tanulmany_naplo_es_osszesito_kimarad(self):
        os.makedirs(os.path.join(self.gy, 'genezis', 'naplok'))
        self.ir('genezis/naplok/x.md', '## R\n\nἐπικατάρατος.\n')
        self.ir('genezis/Konnyu_ellenorzes_1-16_osszesito.md', '## R\n\nἐπικατάρατος.\n')
        self.ir('genezis/Teszt_bovitett.md', '## R\n\nἐπικατάρατος (epikatáratosz).\n')
        s = E.szabaly22_kiejtes_hiany(os.path.join(self.gy, 'adat'))
        self.assertEqual(s.verdict, 'RENDBEN')


if __name__ == '__main__':
    unittest.main(verbosity=1)
