#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_motivum_hatar.py -- F151: a `motivum_hatar.py` egysegtesztjei (kis, szintetikus adaton; a valodi adatot nem
olvassa, kiveve a tartomany-kibontas egy esetet a Karoli-fajlbol).

    python eszkozok/teszt_motivum_hatar.py
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
import motivum_hatar as H  # noqa: E402


def bonto(igehely):
    """Szintetikus bontó: 'K 1:2-4' -> 'K 1:2', 'K 1:3', 'K 1:4'; egyébként önmaga."""
    if '-' not in igehely:
        return [igehely]
    elol, tartomany = igehely.rsplit(':', 1)
    a, b = tartomany.split('-')
    return ['%s:%d' % (elol, v) for v in range(int(a), int(b) + 1)]


def sor(ln, i, ig, strong=''):
    return (ln, {'id': i, 'igehely': ig, 'kapcsolodas': 'kapcs ' + ig, 'strong': strong})


class ReszhalmazTeszt(unittest.TestCase):
    def test_viszony(self):
        self.assertEqual(H.reszhalmaz_viszony({'a'}, {'a', 'b'}), ('reszhalmaz', 1.0))
        self.assertEqual(H.reszhalmaz_viszony({'a', 'b'}, {'a', 'b'}), ('azonos', 1.0))
        t, r = H.reszhalmaz_viszony({'a', 'b', 'c', 'd', 'e'}, {'a', 'b', 'c', 'd', 'x'})
        self.assertEqual((t, r), ('atfedes', 0.8))
        self.assertIsNone(H.reszhalmaz_viszony({'a', 'b', 'c', 'd', 'e'}, {'a', 'b', 'c', 'x'}))  # 60%
        self.assertIsNone(H.reszhalmaz_viszony({'a'}, {'b'}))
        self.assertIsNone(H.reszhalmaz_viszony(set(), {'b'}))

    def test_tartomany_kibontas(self):
        sorok = [sor(3, 'A', 'K 1:2-4'), sor(4, 'B', 'K 1:3'), sor(5, 'B', 'K 1:4')]
        v = H.motivum_versek(sorok, 'A', bonto)
        self.assertEqual(list(v), ['K 1:2', 'K 1:3', 'K 1:4'])
        self.assertEqual(v['K 1:3'], [(3, 'K 1:2-4')])
        # B (2 vers) részhalmaza A-nak, A nem része B-nek: csak a B_A irány
        k = H.reszhalmaz_kerdesek('A', sorok, [], bonto)
        self.assertEqual([(x['irany'], x['tipus']) for x in k], [('B_A', 'reszhalmaz')])
        self.assertEqual([c[0] for c in k[0]['kozos']], ['K 1:3', 'K 1:4'])

    def test_ket_irany_es_kapcsolat(self):
        sorok = [sor(3, 'A', 'K 1:1'), sor(4, 'A', 'K 1:2'), sor(5, 'B', 'K 1:1'), sor(6, 'B', 'K 1:2'), sor(7, 'C', 'K 9:9')]
        kap = [(2, {'id_a': 'A', 'id_b': 'B', 'tipus': 'szomszédos'}), (3, {'id_a': 'B', 'id_b': 'C'})]
        k = H.reszhalmaz_kerdesek('A', sorok, kap, bonto)
        self.assertEqual(len(k), 1)  # azonos halmaz egyszer
        self.assertEqual((k[0]['irany'], k[0]['tipus'], k[0]['masik']), ('ket_irany', 'azonos', 'B'))
        self.assertEqual([ln for ln, _c in k[0]['kapcsolatok']], [2])  # csak az A-B pár kapcsolata
        self.assertNotIn('C', [x['masik'] for x in k])  # a C-vel nincs átfedés

    def test_atfedes_irany(self):
        # A 5 vers, B 10 vers; A-ból 4 benne van B-ben (80%): A_B átfedés; B-ből 4/10 = 40% -> nincs B_A
        a = [sor(3, 'A', 'K 1:%d' % i) for i in (1, 2, 3, 4, 5)]
        b = [sor(10 + i, 'B', 'K 1:%d' % i) for i in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11)]
        k = H.reszhalmaz_kerdesek('A', a + b, [], bonto)
        self.assertEqual([(x['irany'], x['tipus']) for x in k], [('A_B', 'atfedes')])
        self.assertAlmostEqual(k[0]['arany'], 0.8)

    def test_parok_tabla(self):
        sorok = [sor(3, 'A', 'K 1:1'), sor(4, 'B', 'K 1:1'), sor(5, 'B', 'K 1:2')]
        t = H.parok_tabla('A', sorok, [(9, {'id_a': 'A', 'id_b': 'B'})], bonto)
        self.assertEqual(t, [('B', 1, 2, 1, 1.0, 0.5, [9])])

    def test_kerdes_szoveg(self):
        sorok = [sor(3, 'A', 'K 1:1'), sor(4, 'B', 'K 1:1'), sor(5, 'B', 'K 1:2')]
        k = H.reszhalmaz_kerdesek('A', sorok, [], bonto)
        sz = '\n'.join(H.resz1_szoveg(k, 'A', 1, H.parok_tabla('A', sorok, [], bonto)))
        self.assertIn('K1 (reszhalmaz)', sz)
        self.assertIn('`adat/elofordulasok.tsv:3`', sz)
        self.assertIn('`adat/elofordulasok.tsv:4`', sz)
        üres = '\n'.join(H.resz1_szoveg([], 'A', 1))
        self.assertIn('0 kérdés', üres)


class NegativKriteriumTeszt(unittest.TestCase):
    VERS_ST = {'K 1:1': {'H1', 'H2'}, 'K 1:2': {'H1'}, 'K 1:3': {'H9'}}

    def sorok(self):
        return [sor(3, 'F', 'K 1:1', 'H1+H2'), sor(4, 'F', 'K 1:2', 'H1+H2'), sor(5, 'F', 'K 1:3', 'H1+H2'),
                sor(6, 'F', 'K 8:8', 'H1+H2')]

    def test_formulaikus_ag(self):
        fut, e = H.negativ_kriterium_futtat('F', 'formulaikus', self.sorok(), self.VERS_ST)
        self.assertTrue(fut)
        # K 1:2 és K 1:3: a kombináció hiányzik; K 8:8: nincs szövegadat
        self.assertEqual([x[2] for x in e], [True, False, False, None])
        self.assertEqual([x[0] for x in e], [3, 4, 5, 6])  # fájlbeli sorszám

    def test_nem_formulaikus_ag(self):
        for hordozo in ('strukturális', 'lexikai', 'fogalmi', '?'):
            fut, e = H.negativ_kriterium_futtat('F', hordozo, self.sorok(), self.VERS_ST)
            self.assertFalse(fut)
            self.assertEqual(e, [])

    def test_szoveg_kimondja(self):
        mot = {'id': 'F', 'cim': 'c', 'negativ_kriterium': 'nk szöveg', 'folerendelt_fogalom': 'f'}
        ki = H.resz2_szoveg('F', 10, mot, False, [], 'strukturális')
        self.assertIn('a hordozó strukturális: a gépi negatív-kritérium próba nem fut', '\n'.join(ki))
        fut, e = H.negativ_kriterium_futtat('F', 'formulaikus', self.sorok(), self.VERS_ST)
        sz = '\n'.join(H.resz2_szoveg('F', 10, mot, fut, e, 'formulaikus'))
        self.assertIn('kérdés (hiányzik): 2', sz)
        self.assertIn('`adat/motivumok.tsv:10`', sz)
        self.assertIn('`adat/elofordulasok.tsv:4`', sz)
        self.assertIn('nem ellenőrizhető', sz)


class FajlTeszt(unittest.TestCase):
    def test_sorszam_kommenttel(self):
        with tempfile.TemporaryDirectory() as d:
            ut = os.path.join(d, 'x.tsv')
            with open(ut, 'w', encoding='utf-8', newline='') as f:
                f.write('# komment\nid\tigehely\nA\tK 1:1\n\nB\tK 1:2\n')
            self.assertEqual([(ln, r['id']) for ln, r in H.beolvas_sorszammal(ut)], [(3, 'A'), (5, 'B')])

    def test_modelles_resz_megorzese(self):
        regi = 'x\n%s\nvalami tartalom\n%s\n' % (H.MODELLES_KEZDET, H.MODELLES_VEGE)
        self.assertIn('valami tartalom', '\n'.join(H.modelles_resz(regi)))
        self.assertIn(H.MODELLES_HELYORZO, '\n'.join(H.modelles_resz(None)))
        self.assertIn(H.MODELLES_HELYORZO, '\n'.join(H.modelles_resz('%s\n\n%s' % (H.MODELLES_KEZDET, H.MODELLES_VEGE))))

    def test_valodi_tartomany(self):
        self.assertEqual(H.vers_lista('1Móz 4:10-11'), ['1Móz 4:10', '1Móz 4:11'])
        self.assertEqual(H.vers_lista('1Móz 4:10–11'), ['1Móz 4:10', '1Móz 4:11'])  # gondolatjel is


if __name__ == '__main__':
    unittest.main(verbosity=1)
