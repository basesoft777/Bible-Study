#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_jelolt_eloszures.py -- F150: a jelolt_eloszures.py tesztjei (DT432: a gepi szabaly csak
formulaikus hordozon dont). A 12 ismert hamis kizaras negativ teszt; a formulaikus motivumokon a mert
0 hamis kizaras es a felismert elutasitasok pozitiv teszt; a hordozo-szabaly es az idempotencia.

    python eszkozok/teszt_jelolt_eloszures.py
"""
import os
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jelolt_eloszures as J  # noqa: E402

# A 12 ismert hamis kizárás (F150 brief 2. szakasz; a jeloltek.tsv-ben versenként külön sorok).
ISMERT_12 = [
    ('MENNY-001', 'Júd 1:6'), ('MENNY-001', 'Júd 1:14-15'), ('MENNY-001', '2Pét 2:4-5'),
    ('ANTROP-001', 'Luk 1:46'), ('ANTROP-001', 'Luk 1:47'), ('ANTROP-001', '1Kor 2:14'), ('ANTROP-001', '1Kor 2:15'),
    ('HAMART-001', 'Ézs 24:5-6'), ('HAMART-001', 'Hós 4:1-3'), ('HAMART-001', 'Mt 15:19'),
    ('HAMART-001', 'Mk 7:21-23'), ('HAMART-001', '2Pét 3:6-7'),
]
MINDEN_DONTES = ('nyitva', 'beépítve', 'elutasítva')
_CACHE = {}


def valos(dontesek):
    if dontesek not in _CACHE:
        _CACHE[dontesek] = J.sorok_szamit(J.ALAPERTELMEZETT_ADAT, dontesek=dontesek)
    return _CACHE[dontesek]


class Szabaly(unittest.TestCase):
    """Szintetikus bemenet, a valós adat nélkül."""
    KOMB = {'T-1': [frozenset({'H8414', 'H0922'})]}

    def test_hianyzo_par_valoszinu_ki(self):
        j, ok = J.javaslat('T-1', 'formulaikus', '1Móz 1:1', self.KOMB, {'1Móz 1:1': {'H8414', 'H7225'}})
        self.assertEqual(j, 'valoszinu_ki')
        self.assertIn('H0922+H8414', ok)
        self.assertIn('a versben a gerincből: H8414', ok)

    def test_megvan_a_par_vizsgalando(self):
        j, _ = J.javaslat('T-1', 'formulaikus', '1Móz 1:1', self.KOMB, {'1Móz 1:1': {'H8414', 'H0922'}})
        self.assertEqual(j, 'vizsgalando')

    def test_nincs_szoveg_vizsgalando(self):
        j, ok = J.javaslat('T-1', 'formulaikus', '1Móz 1:1', self.KOMB, {})
        self.assertEqual(j, 'vizsgalando')
        self.assertIn('nincs szövegadat', ok)

    def test_nincs_kombinacio_vizsgalando(self):
        j, _ = J.javaslat('T-9', 'formulaikus', '1Móz 1:1', self.KOMB, {'1Móz 1:1': {'H1'}})
        self.assertEqual(j, 'vizsgalando')

    def test_nem_formulaikus_hordozon_sosem_valoszinu_ki(self):
        # a gerinc-szókapcsolat hiányzik, mégis vizsgalando, a megadott okkal
        for hordozo in ('lexikai', 'strukturális', 'referenciális', 'fogalmi', 'strukturalis', '?'):
            j, ok = J.javaslat('T-1', hordozo, '1Móz 1:1', self.KOMB, {'1Móz 1:1': {'H8414'}})
            self.assertEqual(j, 'vizsgalando', hordozo)
            self.assertEqual(ok, 'a hordozó nem formulaikus: a gépi szabály nem dönt')


class ValosAdat(unittest.TestCase):
    def test_a_12_ismert_eset_nem_kaphat_valoszinu_ki_t(self):
        sorok = {(m, s[0]): s for m, ss in valos(('beépítve',)).items() for s in ss}
        for kulcs in ISMERT_12:
            self.assertIn(kulcs, sorok, 'az ismert eset nincs a jeloltek.tsv-ben: %s %s' % kulcs)
            self.assertEqual(sorok[kulcs][1], 'vizsgalando', '%s %s' % kulcs)

    def test_formulaikus_motivumon_nulla_hamis_kizaras(self):
        v = valos(('beépítve',))
        mot = {r['id']: r['azonossag_tipusa'] for r in J.beolvas(os.path.join(J.ALAPERTELMEZETT_ADAT, 'motivumok.tsv'))}
        formulaikus = [m for m in v if mot[m] == 'formulaikus']
        self.assertGreaterEqual(len(formulaikus), 2)  # ISTENTISZT-001, TEREMT-002
        for m in formulaikus:
            self.assertTrue(v[m], m)
            self.assertEqual([s[0] for s in v[m] if s[1] == 'valoszinu_ki'], [], m)

    def test_formulaikus_motivumon_van_felismert_elutasitas(self):
        v = valos(('elutasítva',))
        felismert = [(m, s[0]) for m in ('ISTENTISZT-001', 'TEREMT-002') for s in v[m] if s[1] == 'valoszinu_ki']
        self.assertGreaterEqual(len(felismert), 1)
        # a mért érték (F150 M0): 58 + 62
        self.assertEqual(len(felismert), 120)

    def test_nem_formulaikus_motivumon_egy_sor_sem_valoszinu_ki(self):
        mot = {r['id']: r['azonossag_tipusa'] for r in J.beolvas(os.path.join(J.ALAPERTELMEZETT_ADAT, 'motivumok.tsv'))}
        for m, sorok in valos(MINDEN_DONTES).items():
            if mot[m] != 'formulaikus':
                self.assertEqual([s for s in sorok if s[1] == 'valoszinu_ki'], [], m)
                self.assertTrue(all(s[2] == J.OK_NEM_DONT and s[3] == mot[m] for s in sorok), m)

    def test_rendezes_vizsgalando_elol_valoszinu_ki_a_vegen(self):
        van = False
        for m, sorok in valos(MINDEN_DONTES).items():
            flag = [s[1] == 'valoszinu_ki' for s in sorok]
            self.assertEqual(flag, sorted(flag), m)
            van = van or any(flag)
        self.assertTrue(van)


class Kimenet(unittest.TestCase):
    def test_idempotens_es_generalt_fejlec(self):
        bemenet_fn = lambda root: ('proba@0', '2026-11-01T00:00Z')  # noqa: E731
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            a = J.futtat(kimenet_dir=d1, bemenet_fn=bemenet_fn, vers_st=None)
            b = J.futtat(kimenet_dir=d2, bemenet_fn=bemenet_fn, vers_st=None)
            self.assertEqual(a, b)
            nevek = sorted(os.listdir(d1))
            self.assertEqual(nevek, sorted(os.listdir(d2)))
            self.assertEqual(nevek, sorted('ELOSZURES_%s.tsv' % m for m in a))
            for nev in nevek:
                with open(os.path.join(d1, nev), 'rb') as f1, open(os.path.join(d2, nev), 'rb') as f2:
                    x = f1.read()
                    self.assertEqual(x, f2.read())
                    self.assertNotIn(b'\r', x)
                sorok = x.decode('utf-8').split('\n')
                self.assertTrue(sorok[0].startswith('# GENERÁLT: jelolt_eloszures.py'))
                self.assertEqual(sorok[1].split('\t'), J.FEJLEC)
                for s in sorok[2:]:
                    if s:
                        self.assertIn('scope=', s.split('\t')[4])
                        self.assertIn('ts=2026-11-01T00:00Z', s.split('\t')[4])

    def test_a_jeloltek_tsv_nem_valtozik(self):
        ut = os.path.join(J.ALAPERTELMEZETT_ADAT, 'jeloltek.tsv')
        with open(ut, 'rb') as f:
            elotte = f.read()
        with tempfile.TemporaryDirectory() as d:
            J.futtat(kimenet_dir=d)
        with open(ut, 'rb') as f:
            self.assertEqual(f.read(), elotte)


if __name__ == '__main__':
    unittest.main()
