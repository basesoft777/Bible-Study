"""A festékpróba tesztjei (GK-08b): a próba megfogja a szivárgást, és a két mintalapon 0 szivárgást ad."""
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import festek
from lapgen.bemenet.jegyzek import Festo
from lapgen.megjelenites.md.iro import Lapiro
from lapgen.szoveg import Forrasszoveg, Kezi, SablonSor, cim_horgony, idezet, prov, proza, sablon


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


class Horgony(unittest.TestCase):
    """A 3. független ellenőrzés 2. tétele: a horgonyba kerülő, átalakított jelzőszót is látja a próba."""

    def setUp(self):
        self.festo = Festo()
        self.link = SablonSor('t', '[{cim}](#{horgony})', 'cim:lathato, horgony:horgony')

    def _lap(self, *darabok):
        lap = Lapiro()
        lap.sor(*darabok)
        return _Eredmeny(lap.kesz(), self.festo)

    def test_a_kezi_cim_jelzoszava_a_horgonyban_megengedett(self):
        """A címsorból képzett horgony a kézi cím kisbetűs alakját hordozza: a próba látja (kis- és nagybetűtől
        függetlenül keres), és a kézi szöveg jelzőszavát a horgonyban megengedi."""
        jel = self.festo.jel('kezi', 'B56_cimke')
        cim = proza(Kezi('Az ok címe', 'cimke', jel))
        horgony = cim_horgony(cim)
        self.assertIn(jel.lower(), horgony.kod)
        szivargas, latott = festek.szivargasok(self._lap(sablon(self.link, cim=cim, horgony=horgony)))
        self.assertEqual(szivargas, [])
        self.assertEqual(latott, {'kezi': 2, 'horgony': 1})

    def test_belso_mezo_jelzoszava_a_horgonyban_is_szivargas(self):
        jel = self.festo.jel('belso', 'B04_indoklas')
        cim = proza(Kezi('belső szöveg', 'indoklas', jel))
        szivargas, _latott = festek.szivargasok(self._lap(sablon(self.link, cim=cim, horgony=cim_horgony(cim))))
        self.assertEqual(sorted(s[3] for s in szivargas), ['belso', 'belso'])

    def test_atalakitott_jelzoszo_a_horgonyon_kivul_szivargas(self):
        """Ha a jelzőszó átalakítva (kisbetűvel) áll a horgonyon kívül, a szöveget valami átírta: szivárgás,
        akkor is, ha a kategóriája ott megengedett volna."""
        jel = self.festo.jel('kezi', 'B03_kapcsolodas')
        atirt = proza(Kezi('próza', 'kapcsolodas', jel.lower()))
        szivargas, _latott = festek.szivargasok(self._lap(atirt))
        self.assertEqual([(s[3], s[4]) for s in szivargas], [('kezi', festek.ATALAKITOTT)])


class Mintalapok(unittest.TestCase):
    def test_a_mintalapok_horgonyaiban_latszik_a_jelzoszo(self):
        """A próba ereje: a két mintalapon a mellékletre mutató horgonyokban álló (kisbetűs) jelzőszavakat a
        próba megszámolja, és mind kézi szövegé."""
        for azonosito in MINTALAPOK:
            szivargas, latott, _eredmeny = festek.proba(azonosito, gyoker=kozos.GYOKER)
            self.assertEqual(szivargas, [], azonosito)
            self.assertGreater(latott.get('horgony', 0), 10, azonosito)

    def test_gk08b_a_ket_mintalapon_nincs_szivargas(self):
        """GK-08b: festett futásban mindkét mintalap teljes bemenetén 0 szivárgás. (Szeletenként bővül: a
        látott jelzőszavak száma a kész szakaszokkal nő.)"""
        for azonosito in MINTALAPOK:
            szivargas, _latott, _eredmeny = festek.proba(azonosito, gyoker=kozos.GYOKER)
            self.assertEqual(szivargas, [], azonosito)

    def test_gk08b_a_szotari_ag_mezoi_is_festettek(self):
        """GK-08b: a szótári példahelyek mezői (B19) is jelzőszót kapnak: a belső mezők belső, a forrás
        idézhető alakja idézet kategóriában; így a próba a szótári ágat is fedi."""
        _szivargas, _latott, eredmeny = festek.proba('HAMART-001')
        kategoriak = eredmeny.festo.kategoriak
        self.assertEqual(kategoriak.get('ZZQB19_sorszamZZ'), 'belso')
        self.assertEqual(kategoriak.get('ZZQB19_karoli_versZZ'), 'belso')
        self.assertEqual(kategoriak.get('ZZQB19_nyersZZ'), 'idezet')
        szoveg = '\n'.join(sor.szoveg for sor in eredmeny.nezetek['TUDOMANYOS'])
        self.assertIn('ZZQB19_sorszamZZ', szoveg)


if __name__ == '__main__':
    unittest.main(verbosity=1)
