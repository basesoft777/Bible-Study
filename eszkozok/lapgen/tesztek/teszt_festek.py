"""A festékpróba tesztjei (GK-08b): a próba megfogja a szivárgást, és a két mintalapon 0 szivárgást ad."""
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import festek
from lapgen.bemenet.jegyzek import Festo
from lapgen.megjelenites.md.iro import Lapiro
from lapgen.szoveg import Forrasszoveg, Kezi, SablonSor, idezet, prov, proza, sablon


class _Eredmeny:
    def __init__(self, sorok, festo):
        self.nezetek = {'TUDOMANYOS': sorok}
        self.festo = festo


class ProbaEreje(unittest.TestCase):
    def setUp(self):
        self.festo = Festo()

    def _lap(self, *darabok):
        lap = Lapiro()
        lap.sor(*darabok)
        return _Eredmeny(lap.kesz(), self.festo)

    def test_gk08b_belso_mezo_a_lathato_szovegben_szivargas(self):
        """GK-08b: ha egy belső mező jelzőszava látható szövegben áll, a próba megfogja."""
        jel = self.festo.jel('belso', 'B04_forras_kereses')
        szivargo = proza(Kezi('a keresés szövege', 'forras_kereses', jel))
        szivargas, latott = festek.szivargasok(self._lap(szivargo))
        self.assertEqual(len(szivargas), 1)
        self.assertEqual(szivargas[0][2:4], (jel, 'belso'))
        self.assertEqual(latott, {'belso': 1})

    def test_gk08b_belso_mezo_megjegyzesben_rendben(self):
        jel = self.festo.jel('belso', 'B03_proveniencia')
        szivargas, latott = festek.szivargasok(self._lap(prov('proveniencia: {}', jel)))
        self.assertEqual(szivargas, [])
        self.assertEqual(latott, {'belso': 1})

    def test_gk08b_idezet_jelzoszava_csak_idezetben(self):
        """Az idézet-mező jelzőszava idézet-fajtájú helyen rendben van, prózában vagy sablonban szivárgás."""
        jel = self.festo.jel('idezet', 'B07_szoveg')
        jo = idezet(Forrasszoveg('vers', 'szoveg', 'B07', None, jel))
        self.assertEqual(festek.szivargasok(self._lap(jo))[0], [])
        sor = SablonSor('t', 'A vers: {v}', 'v:lathato')
        self.assertEqual(festek.szivargasok(self._lap(sablon(sor, v=jo)))[0], [])
        rossz = proza(Kezi('vers', 'szoveg', jel))
        self.assertEqual(len(festek.szivargasok(self._lap(rossz))[0]), 1)

    def test_gk08b_kezi_jelzoszava_csak_prozaban(self):
        jel = self.festo.jel('kezi', 'B03_kapcsolodas')
        self.assertEqual(festek.szivargasok(self._lap(proza(Kezi('próza', 'kapcsolodas', jel))))[0], [])
        rossz = idezet(Forrasszoveg('próza', 'kapcsolodas', 'B03', None, jel))
        self.assertEqual(len(festek.szivargasok(self._lap(rossz))[0]), 1)


class Mintalapok(unittest.TestCase):
    def test_gk08b_a_ket_mintalapon_nincs_szivargas(self):
        """GK-08b: festett futásban mindkét mintalap teljes bemenetén 0 szivárgás. (Szeletenként bővül: a
        látott jelzőszavak száma a kész szakaszokkal nő.)"""
        for azonosito in MINTALAPOK:
            szivargas, _latott, _eredmeny = festek.proba(azonosito, gyoker=kozos.GYOKER)
            self.assertEqual(szivargas, [], azonosito)


if __name__ == '__main__':
    unittest.main(verbosity=1)
