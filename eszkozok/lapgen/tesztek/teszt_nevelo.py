"""A lista- és táblaelem névelő-kapuja a cella típusa szerint (F241.5b, D16 (c); `lapgen/nevelo.py`).

A kapu a kész lap fajta-térképén fut: a sablon-eredetű névelő BUKÁS, az idézet (Károli-szöveg) és a kézi, jóváhagyott
próza névelője nem mérődik. A Markdown-mérő (`olvasoi_kapu.ell_lista_nevelo`) ugyanazt a szabályt és elembontást
használja; a fajta-térkép átadásával ott is mentes az idézet és a kézi próza. Lapgen-futás nélkül.
"""
import os
import sys
import unittest

import kozos  # noqa: F401  (a sys.path beállítása)
from lapgen import nevelo
from lapgen.megjelenites.md.iro import JELOLES, KeszSor
from lapgen.szoveg import Fajta

S, P, I = Fajta.SABLON, Fajta.PROZA, Fajta.IDEZET


def sor(*darabok):
    """Kész sor (fajta, szöveg) darabokból, a fajta-térképpel."""
    szoveg, tart, hol = '', [], 0
    for fajta, resz in darabok:
        szoveg += resz
        tart.append((hol, hol + len(resz), fajta))
        hol += len(resz)
    return KeszSor(szoveg, tuple(tart))


def cella_sor(*cellak):
    darabok = [(JELOLES, '| ')]
    for i, c in enumerate(cellak):
        if i:
            darabok.append((JELOLES, ' | '))
        darabok.extend(c)
    darabok.append((JELOLES, ' |'))
    return sor(*darabok)


class Elembontas(unittest.TestCase):
    def test_tabla_cellai_helyukkel(self):
        t = '| Kulcsszó | a hívás |'
        self.assertEqual(nevelo.elemek(t), [('Kulcsszó', 2), ('a hívás', 13)])

    def test_elvalaszto_sor_nem_elem(self):
        self.assertEqual(nevelo.elemek('|---|:--:|'), [])

    def test_lista_elem(self):
        self.assertEqual(nevelo.elemek('- a BDB-szótár (közkincs)'), [('a BDB-szótár (közkincs)', 2)])
        self.assertEqual(nevelo.elemek('12. az ige'), [('az ige', 4)])

    def test_a_megjegyzes_nem_latszik_a_hely_marad(self):
        t = '| <!-- x --> a hívás |'
        (elem, kezdet), = nevelo.elemek(t)
        self.assertEqual(elem, 'a hívás')
        self.assertEqual(t[kezdet:kezdet + 7], 'a hívás')

    def test_folyo_szoveg_nem_elem(self):
        self.assertEqual(nevelo.elemek('a folyó szöveg névelővel kezdődhet'), [])


class Kapu(unittest.TestCase):
    def test_sablon_nevelo_bukas(self):
        lap = [cella_sor([(S, 'Forrás')], [(S, 'a BDB-szótár (közkincs)')])]
        self.assertEqual(nevelo.talalatok(lap), [(1, 'a BDB-szótár (közkincs)')])
        with self.assertRaises(nevelo.NeveloHiba):
            nevelo.kapu({'TUDOMANYOS': lap})

    def test_idezet_nem_merodik(self):
        """A Kulcsszó oszlop Károli-szava idézet: nem írható át a kapu kedvéért (D16 (c))."""
        lap = [cella_sor([(S, '1Móz 4:26')], [(I, 'az Úr nevét')])]
        self.assertEqual(nevelo.talalatok(lap), [])
        nevelo.kapu({'TUDOMANYOS': lap})

    def test_kezi_proza_nem_merodik(self):
        """A Funkció cella a szerkesztő jóváhagyott kézi kifejezése (`Kezi`): nem mérődik (D16 (c))."""
        lap = [cella_sor([(P, 'a segítségül hívás helye')])]
        self.assertEqual(nevelo.talalatok(lap), [])

    def test_sablon_tette_nevelo_kezi_ele_bukas(self):
        """A névelő karakterének fajtája dönt: a sablon által a kézi szöveg elé tett névelő sablonhiba."""
        lap = [cella_sor([(S, 'a '), (P, 'segítségül hívás')])]
        self.assertEqual(len(nevelo.talalatok(lap)), 1)

    def test_kiemeles_utan_is(self):
        lap = [sor((JELOLES, '- '), (JELOLES, '**'), (S, 'a tágabb kör'), (JELOLES, '**'))]
        self.assertEqual(len(nevelo.talalatok(lap)), 1)
        lap = [sor((JELOLES, '- '), (JELOLES, '**'), (I, 'az Úr'), (JELOLES, '**'))]
        self.assertEqual(nevelo.talalatok(lap), [])

    def test_nagybetus_mondatkezdet_megengedett(self):
        lap = [cella_sor([(S, 'A lap elején áll.')])]
        self.assertEqual(nevelo.talalatok(lap), [])


class MarkdownMero(unittest.TestCase):
    """Az `olvasoi_kapu` ugyanazt a szabályt használja; a fajta-térképpel az idézet és a kézi próza ott is mentes."""

    def setUp(self):
        import olvasoi_kapu
        self.ok = olvasoi_kapu
        self.regi = olvasoi_kapu.KIVETEL_NELKUL
        olvasoi_kapu.KIVETEL_NELKUL = True

    def tearDown(self):
        self.ok.KIVETEL_NELKUL = self.regi
        self.ok._NEVELO_MENTES = None

    def test_egy_szabaly(self):
        self.assertIs(self.ok.NEVELO_ELEM_RX, nevelo.NEVELO_ELEM_RX)

    def test_fajta_terkeppel_mentes(self):
        lap = [cella_sor([(I, 'az Úr nevét')], [(S, 'a BDB-szótár')])]
        szoveg = '\n'.join(s.szoveg for s in lap) + '\n'
        sorok = self.ok.tagol(szoveg)
        self.assertEqual(len(self.ok.ell_lista_nevelo(sorok)), 2)
        self.ok._NEVELO_MENTES = nevelo.mentes_fv(lap)
        talalt = self.ok.ell_lista_nevelo(sorok)
        self.assertEqual(len(talalt), 1)
        self.assertIn('a BDB-szótár', str(talalt[0]))


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    unittest.main()
