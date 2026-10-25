#!/usr/bin/env python
"""A Thayer igehely → jelentéspont táblájának tesztjei (F132 M2, eszkozok/thayer_jelolt/vers_jelentes.py).

Futtatás: python eszkozok/thayer_jelolt/teszt_vers_jelentes.py   (a kiírt adat/thayer_vers_jelentes.tsv-t és a
adat/thayer_szakaszok.tsv-t olvassa; a determinizmus-teszt a --ellenoriz módot hívja).
"""
import collections
import os
import subprocess
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import bont  # noqa: E402
import vers_jelentes as V  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = V.KI_UT
SZAKASZ = bont.KI_UT


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = f.read().split('\n')
    fej = s[2].split('\t')
    return fej, [dict(zip(fej, x.split('\t'))) for x in s[3:] if x]


_C = {}


def adat():
    if not _C:
        _C['fej'], _C['sorok'] = olvas(TABLA)
        _, sz = olvas(SZAKASZ)
        _C['szak'] = {(r['strong'], r['sorszam']): r for r in sz}
        _C['lex'] = bont.lexikon_beolvas()
    return _C


class Tabla(unittest.TestCase):
    def test_fejlec(self):
        self.assertEqual(adat()['fej'], V.FEJLEC)
        with open(TABLA, encoding='utf-8') as f:
            self.assertTrue(f.readline().startswith('# GENERÁLT: eszkozok/thayer_jelolt/vers_jelentes.py --ts '))

    def test_minden_bcv_a_tablaban(self):
        a = adat()
        n = collections.Counter(r['strong'] for r in a['sorok'])
        ossz = 0
        for sp, (_, d) in a['lex'].items():
            db = len(V.BCV.findall(d))
            ossz += db
            self.assertEqual(n.get(sp, 0), db, sp)
        self.assertEqual(ossz, 63953)
        self.assertEqual(len(a['sorok']), 63953)

    def test_sorszam_folytonos(self):
        per = collections.defaultdict(list)
        for r in adat()['sorok']:
            per[r['strong']].append(int(r['sorszam']))
        for sp, l in per.items():
            self.assertEqual(l, list(range(1, len(l) + 1)), sp)

    def test_szakasz_es_utvonal_a_szakasztablaval(self):
        a = adat()
        for r in a['sorok']:
            sz = a['szak'].get((r['strong'], r['szakasz']))
            self.assertIsNotNone(sz, (r['strong'], r['szakasz']))
            self.assertEqual(sz['utvonal'], r['utvonal'])

    def test_karoli_vers(self):
        kv = set(V.konyvek().values())
        kk = V.karoli_kulcsok()
        ures = 0
        for r in adat()['sorok']:
            self.assertIn(r['konyv'], kv)
            if r['karoli_vers']:
                self.assertIn(r['karoli_vers'], kk)
                self.assertEqual(r['karoli_vers'],
                                 '%s %s:%s' % (V.KAROLI_KONYV.get(r['konyv'], r['konyv']), r['fejezet'], r['vers']))
            else:
                ures += 1
                self.assertNotIn('%s %s:%s' % (V.KAROLI_KONYV.get(r['konyv'], r['konyv']), r['fejezet'], r['vers']), kk)
        self.assertLess(ures, 100)

    def test_g1941_motivumhelyek(self):
        # napló M2: a 10 motívumhelyből 7-et idéz bcv-vel; 1Pét 1:17 az 1. pont alatt, a többi az 5. alatt
        g = [r for r in adat()['sorok'] if r['strong'] == 'G1941']
        self.assertEqual(len(g), 43)
        hely = {r['karoli_vers']: (r['szakasz'], r['utvonal']) for r in g}
        self.assertEqual(hely['1Pét 1:17'], ('3', '-/1/-'))
        for h in ('1Kor 1:2', '2Tim 2:22', 'ApCsel 2:21', 'ApCsel 9:14', 'Róm 10:12', 'Róm 10:13'):
            self.assertEqual(hely[h], ('7', '-/5/-'), h)
        for h in ('ApCsel 9:21', 'ApCsel 22:16', 'Róm 10:14'):
            self.assertNotIn(h, hely)

    def test_proveniencia(self):
        for r in adat()['sorok']:
            self.assertEqual(r['proveniencia'].split(' | ')[:2],
                             ['scope=%s' % r['strong'], 'forras=thayer_jelolt/vers_jelentes.py (fejléc)'])

    def test_konyvszam_lekepezes(self):
        kv = V.konyvek()
        self.assertEqual((kv[1], kv[40], kv[44], kv[66]), ('1Móz', 'Mt', 'ApCsel', 'Jel'))
        self.assertEqual(len(kv), 66)


class Determinizmus(unittest.TestCase):
    def test_ellenoriz(self):
        r = subprocess.run([sys.executable, os.path.join(ITT, 'vers_jelentes.py'), '--ellenoriz'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=1)
