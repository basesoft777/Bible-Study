#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_31.py -- az ellenoriz.py 31. szabályának tesztjei (F123.INDOKLAS, DT-F123ib): a
`jeloltek.tsv` `indoklas` mezője belső jel nélküli olvasói szöveg; a nyom a `dontes_ref`-ben áll.

Ideiglenes (a repón kívüli) adat-könyvtárban fut; a valódi táblán a szabály RENDBEN.

    python eszkozok/teszt_ellenoriz_31.py
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

FEJ = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'karoli_szo', 'azonositas_modja', 'megbizhatosag',
       'datum', 'jelolt_tipus', 'cel_id', 'cel_igehely', 'cel_alpont', 'dontes_ref']
GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sor(indoklas, dontes_ref='', ige='Róm 10:12'):
    d = dict.fromkeys(FEJ, '')
    d.update(id='ISTENTISZT-001', igehely=ige, forras_kereses='TSK Zak 13:9', dontes='elutasítva',
             indoklas=indoklas, datum='2026-11-04', jelolt_tipus='elofordulas', dontes_ref=dontes_ref)
    return d


class Szabaly31(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix='teszt31_')

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def ir(self, sorok):
        with open(os.path.join(self.dir, 'jeloltek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# próba\n' + '\t'.join(FEJ) + '\n')
            for s in sorok:
                f.write('\t'.join(s[k] for k in FEJ) + '\n')

    def test_olvasoi_indoklas_rendben(self):
        self.ir([sor('A név nélküli görög sorok nem tartoznak a motívumba (a felhasználó döntése, 2026-11-01): a '
                     'versben ἐπικαλέομαι áll, de ὄνομα (G3686) nélkül',
                     'DT476 K2 · scope=manual | forras=DONTESEK.md DT476 | ts=2026-11-01')])
        self.assertEqual(E.szabaly31_indoklas_belso(self.dir).verdict, 'RENDBEN')

    def test_belso_jel_az_indoklasban_sertes(self):
        for ind in ('DT476 K2 (a felhasználó, 2026-11-01): ὄνομα nélkül',
                    'a név nélküli forma | scope=manual | forras=DONTESEK.md DT476 | ts=2026-11-01',
                    'a negatív kritérium (motivumok.tsv) kizárja',
                    'a jelen gerinchez nem tartozik',
                    'F123 X.A, elbírálatlan', 'elbírálás: N-F63a'):
            self.ir([sor(ind)])
            s = E.szabaly31_indoklas_belso(self.dir)
            self.assertEqual(s.verdict, 'SÉRTÉS', ind)
            self.assertEqual(s.n, 1, ind)

    def test_a_nyom_a_dontes_ref_ben_nem_hiba(self):
        self.ir([sor('a motívum negatív kritériuma kizárja', 'motivumok.tsv negativ_kriterium · gerinc · N59')])
        self.assertEqual(E.szabaly31_indoklas_belso(self.dir).verdict, 'RENDBEN')

    def test_valodi_tabla(self):
        s = E.szabaly31_indoklas_belso(os.path.join(GYOKER, 'adat'))
        self.assertEqual(s.verdict, 'RENDBEN', s.peldak)


if __name__ == '__main__':
    unittest.main(verbosity=1)
