#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/teszt_ellenoriz_30.py -- F123.LAPJAVIT (DT-F123f, SEMA 2.49): az
eszkozok/ellenoriz.py 30. szabályának (`lap_javitasok.tsv`: séma, zárt értékkészlet,
emberi jóváhagyó) tesztjei.

Ideiglenes (a repón kívüli) adat/ könyvtárban fut; a negatív esetekben a szabálynak
SÉRTÉS-t kell adnia.

    python eszkozok/teszt_ellenoriz_30.py
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

T, N = '\t', '\n'
MOTIVUMOK = {'HODIT-001', 'ALVIL-001'}
JO = {'id': 'HODIT-001', 'hely': '1/a, Zsolt 96:9', 'tipus': 'próza', 'gond': 'homályos',
      'regi': 'a hódolat gerince', 'uj': 'a hódolat közös szava', 'javasolta': 'claude-opus-5-5',
      'jovahagyta': 'felhasználó', 'datum': '2026.11.04',
      'proveniencia': 'scope=manual | forras=chat:/lap-javit HODIT-001 | ts=2026-11-04'}


class Szabaly28(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='teszt_ellenoriz_30_')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ir(self, sorok, fejlec=None):
        fejlec = fejlec or E.LAP_JAVITASOK_FEJLEC
        with open(os.path.join(self.tmp, 'lap_javitasok.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('# megjegyzés' + N + T.join(fejlec) + N)
            for r in sorok:
                f.write(T.join(r.get(k, '') for k in fejlec) + N)

    def futtat(self):
        return E.szabaly30_lap_javitasok(self.tmp, MOTIVUMOK)

    def valtozat(self, **kw):
        r = dict(JO)
        r.update(kw)
        return r

    def test_nincs_tabla(self):
        self.assertEqual(self.futtat().verdict, 'RENDBEN')

    def test_ures_tabla(self):
        self.ir([])
        self.assertEqual(self.futtat().verdict, 'RENDBEN')

    def test_jo_sor_minden_tipussal(self):
        self.ir([self.valtozat(tipus=t) for t in sorted(E.LAP_JAVITAS_TIPUS)]
                + [self.valtozat(gond=g) for g in sorted(E.LAP_JAVITAS_GOND)]
                + [self.valtozat(jovahagyta='Kiss Péter lektor')])
        s = self.futtat()
        self.assertEqual(s.verdict, 'RENDBEN', s.peldak)

    def test_fejlec_elteres(self):
        self.ir([JO], fejlec=E.LAP_JAVITASOK_FEJLEC[:-1])
        self.assertEqual(self.futtat().verdict, 'SÉRTÉS')

    def test_egyeb_gond_tiltott(self):
        self.ir([self.valtozat(gond='egyéb')])
        s = self.futtat()
        self.assertEqual(s.verdict, 'SÉRTÉS')
        self.assertIn('gond', s.peldak[0])

    def test_ismeretlen_tipus(self):
        self.ir([self.valtozat(tipus='stílus')])
        self.assertEqual(self.futtat().verdict, 'SÉRTÉS')

    def test_modell_nem_hagyhat_jova(self):
        for nev in ('claude-opus-5-5', 'Opus', 'sonnet'):
            self.ir([self.valtozat(jovahagyta=nev)])
            self.assertEqual(self.futtat().verdict, 'SÉRTÉS', nev)

    def test_ures_mezo(self):
        for k in ('regi', 'uj', 'jovahagyta', 'hely'):
            self.ir([self.valtozat(**{k: ''})])
            self.assertEqual(self.futtat().verdict, 'SÉRTÉS', k)

    def test_ismeretlen_motivum(self):
        self.ir([self.valtozat(id='NINCS-001')])
        self.assertEqual(self.futtat().verdict, 'SÉRTÉS')

    def test_datum_alak(self):
        self.ir([self.valtozat(datum='2026-11-04')])
        self.assertEqual(self.futtat().verdict, 'SÉRTÉS')

    def test_proveniencia(self):
        self.ir([self.valtozat(proveniencia='manual')])
        self.assertEqual(self.futtat().verdict, 'SÉRTÉS')

    def test_igazi_tabla(self):
        """A repó táblája a valódi motívumlistával átmegy."""
        import general as G
        _, motivumok = G.tsv_beolvas(os.path.join(E.ALAPERTELMEZETT_ADAT, 'motivumok.tsv'))
        s = E.szabaly30_lap_javitasok(E.ALAPERTELMEZETT_ADAT, {m['id'] for m in motivumok})
        self.assertEqual(s.verdict, 'RENDBEN', s.peldak)


if __name__ == '__main__':
    unittest.main()
