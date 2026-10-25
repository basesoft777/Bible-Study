#!/usr/bin/env python
"""A `szakasz_bemenet.py` tesztjei (F128 M1; DT-F128a–d).

    python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py
"""
import os
import sys
import unicodedata
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import nezet_general  # noqa: E402
import szakasz_bemenet as SB  # noqa: E402


def nfd(t):
    return unicodedata.normalize('NFD', t)


class Korpusz(unittest.TestCase):
    """Az egész szakasztáblán: a token nélküli kimenet = a nezet_general.py (--pe-mem nélküli) nézete; 0 pe/mem csere."""

    @classmethod
    def setUpClass(cls):
        cls.hibak, cls.stat, cls.nagy = SB.ellenoriz()

    def test_nincs_hiba(self):
        self.assertEqual(self.hibak, [])

    def test_lefedes(self):
        self.assertEqual(self.stat['strong'], 8090)
        self.assertEqual(self.stat['szakasz'], 36621)

    def test_tobbcsoportos_a_20000_folottiek(self):
        # F128 M0 3.: 11 szócikk 20 000 karakter fölött
        self.assertEqual(sorted(s for s, _, _ in self.nagy),
                         ['H0834', 'H1961', 'H1980', 'H3117', 'H3588', 'H4480', 'H5414', 'H5920', 'H6440', 'H7725', 'H9005'])


class Javitasok(unittest.TestCase):
    def setUp(self):
        self.jav = nezet_general.olvas(nezet_general.JAV)

    def test_hivatkozas_alkalmazva(self):
        d = next(d for d in self.jav if d['hiba'] == 'hivatkozas' and d['allapot'] == 'javitva')
        x = next(x for x in SB.szakaszok(d['strong']) if str(x['sorszam']) == d['sorszam'])
        self.assertIn(d['javitott_alak'], x['szoveg'])

    def test_pe_mem_nem_alkalmazva(self):
        # DT269 (1): a pe/mem csere a bemenetben nincs — a `javitva` sor mem-es alakja marad
        n = 0
        for d in self.jav:
            if d['hiba'] != 'pe_mem' or d['allapot'] != 'javitva':
                continue
            x = next(x for x in SB.szakaszok(d['strong']) if str(x['sorszam']) == d['sorszam'])
            szavak = [nfd(w) for w in x['szoveg'].split()]
            self.assertTrue(any(nfd(d['forras_alak']) in w for w in szavak), (d['strong'], d['sorszam']))
            n += 1
            if n >= 200:
                break
        self.assertEqual(n, 200)

    def test_tablan_kivuli(self):
        # DT-F128d (2): a 9 táblán kívüli Strong a régi `teljes` úton
        for st in ('H0747', 'H1753', 'H3367', 'H3848', 'H4123', 'H4725', 'H6433', 'H7560', 'H8065'):
            self.assertIsNone(SB.szakaszok(st), st)

    def test_hash(self):
        for x in SB.szakaszok('H0001'):
            self.assertEqual(x['hash'], SB.sha1(x['szoveg']))
            self.assertNotIn('⟪', x['szoveg'])


class Tokenek(unittest.TestCase):
    def test_tokenes_alak(self):
        szak = SB.szakaszok('H0001')
        t = SB.tokenes(szak)
        self.assertEqual([int(n) for n in SB.TOKEN.findall(t)], [x['sorszam'] for x in szak])
        self.assertTrue(t.startswith('⟪1⟫ H1. ab'))
        self.assertEqual(SB.TOKEN.sub('', t).replace('\n', ' ').split(), SB.nezet(szak).split())

    def test_jelentes_szam(self):
        self.assertEqual(SB.jelentes_szam(12), 'sz12')
        self.assertEqual(SB.sorszam_jelentesbol('sz12'), 12)
        for x in ('teljes', '2.c', 'sz', 'sz1a', ''):
            self.assertIsNone(SB.sorszam_jelentesbol(x))


def _sz(n, utvonal, hossz):
    return {'sorszam': n, 'jel': '', 'utvonal': utvonal, 'szoveg': 'x' * hossz, 'hash': ''}


class Csoportok(unittest.TestCase):
    def test_rovid_egy_csoport(self):
        szak = SB.szakaszok('H0001')
        self.assertEqual(SB.csoportok(szak), [szak])

    def test_nagy_csoportok(self):
        szak = SB.szakaszok('H1980')
        cs = SB.csoportok(szak)
        self.assertGreater(len(cs), 1)
        self.assertEqual([x for c in cs for x in c], szak)
        for c in cs:
            self.assertLessEqual(sum(SB._hossz(x) for x in c), SB.CSOPORT_CEL)

    def test_torzsvaltasnal_vag(self):
        # 3 × 4 000 karakter Qal alatt, majd Niph'al: a 3. Qal-szakasz után nem fér el a 4.; a vágás a törzsváltásnál
        szak = [_sz(1, 'cim', 10), _sz(2, 'Qal/1/-', 4000), _sz(3, 'Qal/2/-', 4000), _sz(4, "Niph'al/-/-", 1500),
                _sz(5, "Niph'al/1/-", 4000), _sz(6, "Niph'al/2/-", 4000), _sz(7, 'Hiph\'il/-/-', 4000)]
        cs = SB.csoportok(szak, hatar=1000, cel=10000)
        self.assertEqual([[x['sorszam'] for x in c] for c in cs], [[1, 2, 3], [4, 5, 6], [7]])

    def test_egyedul_tul_hosszu_szakasz(self):
        szak = [_sz(1, 'cim', 10), _sz(2, '-/1/-', 12000), _sz(3, '-/2/-', 100)]
        cs = SB.csoportok(szak, hatar=1000, cel=10000)
        self.assertEqual([[x['sorszam'] for x in c] for c in cs], [[1], [2], [3]])


def _f(jsz, szoveg, allapot='sonnet'):
    return {'szotar': 'BDB', 'strong': 'H0001', 'entry_id': 'H1', 'jelentes_szam': jsz, 'mezo': 'forditas_hu',
            'forditas_hu': szoveg, 'allapot': allapot}


class Osszefuzo(unittest.TestCase):
    def test_szakaszok_sorrendben(self):
        sorok = [_f('sz10', 'c'), _f('sz2', 'b'), _f('sz1', 'a')]
        self.assertEqual(SB.strong_magyar(sorok), ('a b c', 'szakasz'))

    def test_szakasz_elonyben_a_teljes_elott(self):
        # DT-F128e: a 98 Strong régi `teljes` sora `elavult`, mellette a szakaszsorok
        sorok = [_f('teljes', 'régi', 'elavult'), _f('sz1', 'a'), _f('sz2', 'b')]
        self.assertEqual(SB.strong_magyar(sorok), ('a b', 'szakasz'))
        sorok = [_f('teljes', 'régi'), _f('sz1', 'a')]
        self.assertEqual(SB.strong_magyar(sorok), ('a', 'szakasz'))

    def test_elavult_szakasz_kimarad(self):
        sorok = [_f('sz1', 'a'), _f('sz2', 'x', 'elavult'), _f('sz3', 'c')]
        self.assertEqual(SB.strong_magyar(sorok), ('a c', 'szakasz'))

    def test_kezi_teljes_elsobbsege_dt_f128f(self):
        # DT-F128f (3): a jóváhagyott `teljes` sor él, amíg a szakaszsorok nem mind `kezi`-k
        self.assertEqual(SB.strong_magyar([_f('teljes', 'jóváhagyott', 'kezi'), _f('sz1', 'a'), _f('sz2', 'b')]),
                         ('jóváhagyott', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'jóváhagyott', 'kezi'), _f('sz1', 'a', 'kezi'), _f('sz2', 'b')]),
                         ('jóváhagyott', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'jóváhagyott', 'kezi'), _f('sz1', 'a', 'kezi'),
                                           _f('sz2', 'b', 'kezi')]), ('a b', 'szakasz'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'régi', 'elavult'), _f('sz1', 'a', 'kezi'), _f('sz2', 'b', 'kezi')]),
                         ('a b', 'szakasz'))

    def test_felhasznalt_sorok(self):
        sorok = [_f('sz2', 'b', 'sonnet'), _f('sz1', 'a', 'sonnet')]
        sz, tipus, hasznalt = SB.strong_magyar_sorok(sorok)
        self.assertEqual([r['jelentes_szam'] for r in hasznalt], ['sz1', 'sz2'])
        self.assertEqual(SB.strong_magyar_sorok([_f('teljes', 'x')])[2][0]['forditas_hu'], 'x')

    def test_teljes_tartalek(self):
        self.assertEqual(SB.strong_magyar([_f('teljes', 'egész')]), ('egész', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'régi', 'elavult'), _f('teljes', 'új')]), ('új', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('teljes', 'régi', 'elavult')]), ('régi', 'teljes'))
        self.assertEqual(SB.strong_magyar([_f('2.c', 'rész', 'kezi')]), (None, None))
        self.assertEqual(SB.strong_magyar([]), (None, None))


sys.path.insert(0, os.path.dirname(ITT))
import emeles as E  # noqa: E402


def _olvas(ut):
    with open(ut, encoding='utf-8') as f:
        return f.read()


class EmelesSzakaszag(unittest.TestCase):
    """F128 M2: az `emeles.py` szakaszonkénti ága. A rögzítés és a beírás ideiglenes munka- és fordítástáblán fut (a repó
    `adat/forditasok.tsv`-je nem íródik), a szakaszok helyén két szintetikus szakasszal."""

    def test_prompt_v5_egy_csoport(self):
        sp, szak = E.szakasz_forras('H1')
        p = E.szakasz_promptok(sp, szak)
        self.assertEqual(len(p), 1)
        self.assertNotIn('{{', p[0][2])
        self.assertIn('Kiegészítő szabály (v5) — szakaszhatár-tokenek', p[0][2])
        self.assertEqual([int(n) for n in SB.TOKEN.findall(p[0][1])], [x['sorszam'] for x in szak])
        self.assertIn(p[0][1], p[0][2])

    def test_prompt_v5_csoportok(self):
        sp, szak = E.szakasz_forras('H1980')
        p = E.szakasz_promptok(sp, szak)
        self.assertEqual(len(p), 6)
        self.assertEqual([int(n) for _, f, _ in p for n in SB.TOKEN.findall(f)], [x['sorszam'] for x in szak])
        self.assertIn('(2/6. rész', p[1][2])

    def test_regi_ut_marad(self):
        with self.assertRaises(SystemExit):
            E.szakasz_forras('H4725')    # táblán kívüli: a régi `teljes` út
        with self.assertRaises(SystemExit):
            E.szakasz_forras('G26')      # Thayer: nincs szakaszága
        sp, szoveg = E.forras_szoveg('H4725')
        self.assertIn('{{FORRAS_SZOVEG}}', _olvas(E.PROMPT_UT))
        self.assertNotIn('⟪', E.prompt_epit(sp, szoveg))

    def _kor(self, strong, tmp):
        import shutil
        from types import SimpleNamespace as NS
        from unittest import mock
        szak = [{'sorszam': 1, 'jel': '', 'utvonal': 'cim', 'szoveg': 'H1. ab', 'hash': SB.sha1('H1. ab')},
                {'sorszam': 2, 'jel': '', 'utvonal': 'fej', 'szoveg': 'father', 'hash': SB.sha1('father')}]
        ford = os.path.join(tmp, 'forditasok.tsv')
        shutil.copyfile(E.FORDITASOK_UT, ford)
        # a tesztkor a Strong valódi szakaszsorai nem számítanak (pl. a H8415 már szakaszonként le van fordítva, F38 N-F107b):
        # a másolatban csak a régi `teljes` sor marad, az az induló állapot
        with open(ford, encoding='utf-8', newline='') as f:
            sorok = f.read().split('\n')
        sorok = [s for s in sorok if not (s.startswith('BDB\t%s\t' % strong) and s.split('\t')[3].startswith('sz'))]
        with open(ford, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(sorok))
        be = os.path.join(tmp, 'hu.txt')
        with open(be, 'w', encoding='utf-8') as f:
            f.write('⟪1⟫ H1. ab ⟪2⟫ apa\n')
        p = [mock.patch.object(SB, 'szakaszok', lambda s: szak if s == strong else None),
             mock.patch.object(E, 'MUNKA_UT', os.path.join(tmp, 'munka.tsv')),
             mock.patch.object(E, 'FORDITASOK_UT', ford)]
        for x in p:
            x.start()
        self.addCleanup(lambda: [x.stop() for x in p])
        E.cmd_szakasz_rogzit(NS(strong=strong, be=be, allapot='sonnet', modell='teszt-modell', datum='2026.10.21',
                                megjegyzes='F128 teszt', kivetel=[]))
        return ford, NS

    def _sorok(self, ut):
        return [s.split('\t') for s in _olvas(ut).split('\n') if s and not s.startswith('#')][1:]

    def test_rogzit_beir_regi_elavult(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            ford, NS = self._kor('H0001', tmp)
            munka = self._sorok(E.MUNKA_UT)
            self.assertEqual([(m[3], m[5], m[6]) for m in munka],
                             [('sz1', SB.sha1('H1. ab'), 'H1. ab'), ('sz2', SB.sha1('father'), 'apa')])
            args = dict(strongok=['H0001'], allapot='sonnet', datum='2026.10.21', megjegyzes=None, kezi_felulir=False,
                        kezi_marad=False)
            with self.assertRaises(SystemExit):
                E.cmd_szakasz_beir(NS(regi_elavult=False, **args))
            regi = _olvas(E.FORDITASOK_UT)
            E.cmd_szakasz_beir(NS(regi_elavult=True, **args))
            uj = self._sorok(ford)
            h1 = [m for m in uj if m[1] == 'H0001']
            self.assertEqual([(m[3], m[7]) for m in h1], [('teljes', 'elavult'), ('sz1', 'sonnet'), ('sz2', 'sonnet')])
            self.assertIn('felváltva: szakaszonkénti fordítás', h1[0][11])
            regi_sorok = [s for s in regi.split('\n') if s]
            uj_sorok = [s for s in _olvas(ford).split('\n') if s]
            self.assertEqual(len(uj_sorok), len(regi_sorok) + 2)
            self.assertEqual(sum(1 for a, b in zip(regi_sorok, uj_sorok) if a != b), 1)
            # a közös összefűző a szakaszsorokat adja
            d = [dict(zip(E.FORDITASOK_FEJLEC, m)) for m in h1]
            self.assertEqual(SB.strong_magyar(d), ('H1. ab apa', 'szakasz'))

    def test_kezi_regi_sor_dt_f128f(self):
        # DT-F128f (3): a H8415 régi `kezi` sora érvényes marad, amíg az új szakaszsorok nem kapnak `kezi`-t
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            ford, NS = self._kor('H8415', tmp)
            alap = dict(strongok=['H8415'], datum='2026.10.21', megjegyzes=None, regi_elavult=True)
            with self.assertRaises(SystemExit):   # kifejezett --kezi-marad nélkül megáll
                E.cmd_szakasz_beir(NS(allapot='sonnet', kezi_felulir=False, kezi_marad=False, **alap))
            regi = [m for m in self._sorok(ford) if m[1] == 'H8415']
            E.cmd_szakasz_beir(NS(allapot='sonnet', kezi_felulir=False, kezi_marad=True, **alap))
            h = [m for m in self._sorok(ford) if m[1] == 'H8415']
            self.assertEqual(h[0], regi[0])                      # a régi `kezi` sor bájtra érintetlen
            self.assertEqual([(m[3], m[7]) for m in h[1:]], [('sz1', 'sonnet'), ('sz2', 'sonnet')])
            d = [dict(zip(E.FORDITASOK_FEJLEC, m)) for m in h]
            self.assertEqual(SB.strong_magyar(d), (regi[0][6], 'teljes'))   # a közös összefűző a jóváhagyott sort adja
            with self.assertRaises(SystemExit):   # a jóváhagyás (`kezi`) --kezi-felulir nélkül megáll
                E.cmd_szakasz_beir(NS(allapot='kezi', kezi_felulir=False, kezi_marad=False, **alap))
            E.cmd_szakasz_beir(NS(allapot='kezi', kezi_felulir=True, kezi_marad=False, **alap))
            h = [m for m in self._sorok(ford) if m[1] == 'H8415']
            self.assertEqual([(m[3], m[7]) for m in h], [('teljes', 'elavult'), ('sz1', 'kezi'), ('sz2', 'kezi')])
            d = [dict(zip(E.FORDITASOK_FEJLEC, m)) for m in h]
            self.assertEqual(SB.strong_magyar(d), ('H1. ab apa', 'szakasz'))

    def test_rogzit_hibas_token(self):
        import tempfile
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            ford, NS = self._kor('H0001', tmp)
            be = os.path.join(tmp, 'rossz.txt')
            with open(be, 'w', encoding='utf-8') as f:
                f.write('⟪1⟫ H1. ab apa\n')
            with self.assertRaises(SystemExit):
                E.cmd_szakasz_rogzit(NS(strong='H0001', be=be, allapot='sonnet', modell='m', datum=None,
                                        megjegyzes=None, kivetel=[]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
