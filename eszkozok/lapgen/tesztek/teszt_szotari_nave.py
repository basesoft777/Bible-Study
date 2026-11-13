"""A 4.12 pont (tematikus index, Nave): a bemenet, a kiválasztás szabálya és a lap.

A HAMART-lapon a pont bájtra egyezik a referenciával (a regresszió méri); itt a szabályok és a számok állnak.
"""
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import bemenet, fo, konfig
from lapgen.bemenet import nave as nave_be
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import szotari_nave
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import MotivumId

_LAPOK = {}


def lap(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito))
    return _LAPOK[azonosito]


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


def pont(azonosito):
    sorok = lap(azonosito).nezetek[konfig.NEZET_TUDOMANYOS]
    kezd = next(i for i, s in enumerate(sorok) if s.szoveg.startswith('#### ') and 'Tematikus index' in s.szoveg)
    veg = next(i for i, s in enumerate(sorok) if i > kezd and s.szoveg.startswith('#'))
    return [lathato(s) for s in sorok[kezd:veg]]


class Bemenet(unittest.TestCase):
    def test_a_nave_sorai_karoli_versekre_bomlanak(self):
        """A tárgymutató sorai Károli-versekre bontva jönnek; minden vers a Károli-fordítás verse."""
        b = bemenet.Bemenet(kozos.GYOKER)
        sorok = nave_be.b57_nave_sorok(b)
        karoli = bemenet.b07_karoli(b)
        self.assertGreater(len(sorok), 1000)
        for _tema_id, _tema, _cimke, versek in sorok[:500]:
            self.assertTrue(versek)
            for vers in versek:
                self.assertTrue(karoli.van(nave_be.vers(vers)), vers)

    def test_a_magyar_nev_csak_egyezo_forrasbol_all(self):
        """A magyar név csak akkor áll, ha a fordítás az angol név mai szövegéből készült; különben a név
        fordításra vár (a magyar mező None), és az angol név áll, a hibás karakterkód feloldva."""
        b = bemenet.Bemenet(kozos.GYOKER)
        index = nave_be.nave(b, MotivumId('HAMART-001'))
        tema_id = next(t for t, d in index.dontesek.items() if d == nave_be.DONTES_KIVALASZTOTT)
        angol = next(tema for t, tema, _c, _v in index.sorok if t == tema_id)
        self.assertIsNotNone(index.nev(tema_id, '', angol).magyar)
        ismeretlen = index.nev(tema_id, '', angol + ' &#8221 x')
        self.assertIsNone(ismeretlen.magyar)
        self.assertIn('” x', ismeretlen.angol.ertek)

    def test_ismeretlen_dontes_megall(self):
        repo = kozos.alap_minirepo(
            jegyzek_sorok=[('B70', 'adat/tematikus_temak.tsv', 'd', 'igen', '-', '-', 'aktiv', '-', '-', 'manual')],
            tovabbi={'adat/tematikus_temak.tsv': kozos.tsv(('id', 'forras', 'tema_id', 'dontes'),
                                                           ('PROBA-001', 'Nave', 't1', 'talan'))})
        try:
            with self.assertRaises(bemenet.BemenetHiba):
                nave_be.b70_tema_dontesek(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
        finally:
            repo.torol()


class ALapon(unittest.TestCase):
    def test_gk21_a_nave_blokk_nem_ures(self):
        """GK-21: a tematikus index pontja nem üres: a HAMART-lapon 7 téma áll (a jóváhagyott lap száma), minden
        témának van motívumverse, és a témasor motívumvers-száma a felsorolt versek száma."""
        sorok = pont('HAMART-001')
        temak = [s for s in sorok if s.startswith('- **')]
        self.assertEqual(len(temak), 7)
        self.assertIn(': 7 téma (például: átok)', sorok[2])
        for sor in temak:
            szam = int(sor.split(' — ')[1].split(' ')[0])
            self.assertGreaterEqual(szam, konfig.NAVE_MIN_VERS)
            self.assertEqual(szam, len(sor.rsplit('): ', 1)[1].split(', ')), sor[:60])

    def test_gk21_a_kapu_megfogja_az_ures_pontot(self):
        ures = szotari_nave.Tematikus(temak=(), szoba_johet=0, tiltott=0, tagabb_kor=None, eredeti=None)
        with self.assertRaises(KapuHiba):
            szotari_nave.kapu(ures)
        self.assertIsNone(szotari_nave.kapu(None))

    def test_az_altetelek_a_tema_verseibol_allnak(self):
        """Minden altétel verse a témája motívumversei közül való, és a téma minden verse áll legalább egy
        altételben vagy altétel nélküli sorban."""
        for azonosito in MINTALAPOK:
            modell = None
            for leiro_modell in (lap(azonosito),):
                modell = leiro_modell
            self.assertTrue(modell.nezetek)
            sorok = pont(azonosito)
            tema_versek = None
            for sor in sorok:
                if sor.startswith('- **'):
                    tema_versek = set(sor.rsplit('): ', 1)[1].split(', '))
                elif sor.startswith('  - '):
                    self.assertTrue(set(sor.rsplit(': ', 1)[1].split(', ')) <= tema_versek, sor[:60])

    def test_az_angol_nev_csak_ramutatasra_latszik(self):
        """A téma angol neve a `title` attribútumban áll; a látható szövegben a magyar név."""
        sorok = pont('HAMART-001')
        self.assertIn('- **<span title="CURSE">átok</span>** — 7 motívumvers / 51 témavers (13,7%): ', sorok[6])
        self.assertTrue(any('title="Of Cain, to be “a fugitive and vagabond,”"' in s for s in sorok))


if __name__ == '__main__':
    unittest.main()
