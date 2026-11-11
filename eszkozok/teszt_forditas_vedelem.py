#!/usr/bin/env python3
"""teszt_forditas_vedelem.py — külön menetben készült fordítás: nem fordul újra, és nem marad ki a lapról (F182, F31).

Futtatás: python -m unittest eszkozok.teszt_forditas_vedelem  (a repó gyökeréből)
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import forditas_vedelem as FV  # noqa: E402

FEJ = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forditas_hu', 'allapot', 'modell', 'datum',
       'terminologia_verzio', 'megjegyzes']


def sor(allapot, h='abc', hu='átkozott'):
    return ['TBESG', 'G1944', 'G1944', '', 'glosszak_hu', h, hu, allapot, 'm', 'd', '', '']


class Vedelem(unittest.TestCase):
    def test_ervenyes_azonos_forras_nem_fordul_ujra(self):
        self.assertTrue(FV.ervenyes_ujraforditas(sor('sonnet'), sor('sonnet', hu='más'), FEJ))
        with self.assertRaises(SystemExit):
            FV.ellenoriz(sor('sonnet'), sor('sonnet', hu='más'), FEJ, ('TBESG', 'G1944'))

    def test_elavult_vagy_valtozott_forras_fordulhat(self):
        self.assertFalse(FV.ervenyes_ujraforditas(sor('elavult'), sor('sonnet'), FEJ))
        self.assertFalse(FV.ervenyes_ujraforditas(sor('sonnet', h='abc'), sor('sonnet', h='xyz'), FEJ))

    def test_jovahagyott_kezi_csere(self):
        self.assertFalse(FV.ervenyes_ujraforditas(sor('sonnet'), sor('kezi'), FEJ))

    def test_a_lancok_hivjak(self):
        for rel in ('glossza_api_koteg.py', os.path.join('thayer_jelolt', 'forditas.py'), 'emeles.py'):
            with open(os.path.join(GYOKER, 'eszkozok', rel), encoding='utf-8') as f:
                self.assertIn('FV.ellenoriz(', f.read(), rel)


class LaponAll(unittest.TestCase):
    """A 42. szabály: a lapon szereplő Strong érvényes fordítása a lapon is áll."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(GYOKER, 'lexikon', 'HAMART-001_TUDOMANYOS.md'), encoding='utf-8') as f:
            cls.lap = f.read()

    def test_proba(self):
        import ellenoriz as E
        self.assertEqual(E._ford_proba('1. rosszabbra változtatni, megrontani: az elméket'), 'rosszabbra változtatni megrontani')
        self.assertEqual(E._ford_proba('7. tulajdonnév, helynév: város Naftáliban'), 'tulajdonnév helynév')
        self.assertEqual(E._ford_proba('a. általában, רע ואם טוב'), 'általában')

    def test_hamart_minden_forditas_a_lapon(self):
        import ellenoriz as E
        self.assertEqual(E.lap_forditas_hianyok(os.path.join(GYOKER, 'adat'), 'HAMART-001', self.lap), [])

    def test_rontott_masolat_jelez(self):
        import ellenoriz as E
        self.assertIn('rosszabbra változtatni, megrontani', self.lap)
        rontott = self.lap.replace('rosszabbra változtatni, megrontani', 'xxxx')
        self.assertIn(('G1311', 'Thayer', 'sz3'), E.lap_forditas_hianyok(os.path.join(GYOKER, 'adat'), 'HAMART-001', rontott))


if __name__ == '__main__':
    unittest.main()
