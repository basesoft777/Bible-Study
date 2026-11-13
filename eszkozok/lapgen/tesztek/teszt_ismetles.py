"""Az ismétlés két kapuja (DT-F218n): a kritérium egyszer áll (BUKÁS), és az ismétlés-figyelő (figyelmeztetés).

A kapuk a kész sorok fajta-térképén futnak; a tesztek az író moduljával készítenek sorokat, így ugyanazt a
térképet kapják, mint a lap.
"""
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import bemenet, fo, ismetles, konfig
from lapgen.bemenet import motivum as motivum_be
from lapgen.megjelenites.md.iro import Lapiro, horgony_jel
from lapgen.szakaszok import KRITERIUM_HORGONY
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import Igehely, MotivumId, Proveniencia, idezet, prov, proza

KRITERIUM = ('A versben a lánc egy szava áll, és a hely ezen a szón át a láncra utal vissza: az átkot a földön '
             'mondja ki, ismétli vagy fordítja meg. Nem tartozik ide a hely, amelyben a szó általános használatban áll.')


def _kezi(szoveg):
    b = bemenet.Bemenet(kozos.GYOKER)
    return proza(b.kezi('B02', 'negativ_kriterium', szoveg))


def _idezet(szoveg):
    b = bemenet.Bemenet(kozos.GYOKER)
    return idezet(b.forrasszoveg('B07', 'szoveg', szoveg, Igehely('1Móz 3:14')))


def _lap(*sorok):
    iro = Lapiro()
    for darabok in sorok:
        iro.sor(*(darabok if isinstance(darabok, tuple) else (darabok,)))
    return iro.kesz()


class KriteriumEgyszer(unittest.TestCase):
    def test_egyszer_all_rendben(self):
        lap = _lap(_kezi(KRITERIUM), _kezi('Más bekezdés, amely a szabályt nem ismétli.'))
        self.assertEqual(ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=True), [])
        ismetles.kriterium_kapu(lap, KRITERIUM, teljes=True)

    def test_ketszer_all_bukas(self):
        """A teljes kritérium második példánya BUKÁS; az üzenet megnevezi a sorokat."""
        lap = _lap(_kezi(KRITERIUM), _kezi('Közbeeső bekezdés.'), _kezi(KRITERIUM))
        hibak = ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=True)
        self.assertTrue(hibak)
        self.assertTrue(all(h.sorszamok == (1, 3) for h in hibak))
        with self.assertRaises(KapuHiba) as hiba:
            ismetles.kriterium_kapu(lap, KRITERIUM, teljes=True)
        self.assertIn('sorok: 1, 3', str(hiba.exception))

    def test_a_reszlet_is_szamit(self):
        """Nem csak a teljes szöveg: egy 12 szavas részlet második példánya is BUKÁS, más mondatba ágyazva is,
        más írásjelekkel és nagybetűvel is."""
        szavak = KRITERIUM.replace(',', '').replace(':', '').replace('.', '').split()
        reszlet = ' '.join(szavak[3:3 + konfig.KRITERIUM_ABLAK]).upper()
        lap = _lap(_kezi(KRITERIUM), _kezi('Ide az tartozik, ahol — ' + reszlet + ' — és így tovább.'))
        hibak = ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=True)
        self.assertEqual(len(hibak), 1)
        self.assertEqual(hibak[0].sorszamok, (1, 2))

    def test_tizenegy_szo_nem_szamit(self):
        """Az ablaknál rövidebb egyezés nem hiba (a kritérium szavai másutt is előfordulhatnak)."""
        szavak = KRITERIUM.replace(',', '').replace(':', '').replace('.', '').split()
        reszlet = ' '.join(szavak[3:3 + konfig.KRITERIUM_ABLAK - 1])
        lap = _lap(_kezi(KRITERIUM), _kezi('Ide az tartozik, ahol ' + reszlet + ' xyz.'))
        self.assertEqual(ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=True), [])

    def test_reszleges_lapon_a_hiany_nem_hiba_a_teljesen_igen(self):
        """Amíg a lap eleje nem készült el, a kritérium hiánya nem hiba; a teljes lapon pontosan egyszer áll."""
        lap = _lap(_kezi('A szakasz a lap elejére hivatkozik.'))
        self.assertEqual(ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=False), [])
        hibak = ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=True)
        self.assertTrue(hibak)
        self.assertTrue(all(h.sorszamok == () for h in hibak))
        with self.assertRaises(KapuHiba):
            ismetles.kriterium_kapu(lap, KRITERIUM, teljes=True)

    def test_megjegyzes_es_horgony_nem_lathato(self):
        """A megjegyzésben álló példány nem látható szöveg: nem számít."""
        megjegyzes = prov('eredeti: {}', bemenet.Bemenet(kozos.GYOKER).belso('B02', 'negativ_kriterium', KRITERIUM))
        self.assertIsInstance(megjegyzes, Proveniencia)
        lap = _lap(_kezi(KRITERIUM), megjegyzes, (horgony_jel(KRITERIUM_HORGONY), _kezi('Hivatkozás.')))
        self.assertEqual(ismetles.kriterium_egyszer(lap, KRITERIUM, teljes=True), [])

    def test_rovid_kriterium_egeszben_szamit(self):
        rovid = 'A hely a nevet hívja segítségül.'
        self.assertEqual(ismetles.kriterium_egyszer(_lap(_kezi(rovid)), rovid, teljes=True), [])
        self.assertTrue(ismetles.kriterium_egyszer(_lap(_kezi(rovid), _kezi(rovid)), rovid, teljes=True))

    def test_kriterium_nelkul_nincs_kapu(self):
        ismetles.kriterium_kapu(_lap(_kezi('Bármi.')), None, teljes=True)


class IsmetlesFigyelo(unittest.TestCase):
    HOSSZU = ('ez a mondat tizenhat szónál hosszabb mert a figyelő csak az ennél hosszabb azonos szósort jelzi '
              'és ez éppen ilyen')

    def test_hosszu_ismetles_jelez(self):
        lap = _lap(_kezi('Bevezetés: ' + self.HOSSZU + '.'), _kezi('Közbeeső.'), _kezi(self.HOSSZU + ', és tovább.'))
        talalatok = ismetles.ismetlesek(lap)
        self.assertEqual(len(talalatok), 1)
        self.assertEqual(' '.join(talalatok[0].szavak), self.HOSSZU)
        self.assertEqual([n for n, _hol in talalatok[0].helyek], [1, 3])

    def test_tizenot_szo_nem_jelez(self):
        """15 azonos szó még nem találat: a küszöb a 15-nél hosszabb szósor."""
        rovid = ' '.join(self.HOSSZU.split()[:konfig.ISMETLES_ABLAK - 1])
        lap = _lap(_kezi(rovid + ' egyik vége.'), _kezi(rovid + ' másik vége.'))
        self.assertEqual(ismetles.ismetlesek(lap), [])

    def test_idezet_nem_ismetles(self):
        """A kétszer idézett bibliai szöveg nem találat; a prózában álló ismétlés néhány idézett szóval az."""
        lap = _lap(_idezet(self.HOSSZU), _idezet(self.HOSSZU))
        self.assertEqual(ismetles.ismetlesek(lap), [])
        vegyes = lambda: (_kezi(self.HOSSZU + ' '), _idezet('idézett szó'))   # noqa: E731
        self.assertEqual(len(ismetles.ismetlesek(_lap(vegyes(), vegyes()))), 1)

    def test_jeloles_nem_szo(self):
        """A HTML-címke és a link célja nem szó: a szósor a jelöléstől függetlenül azonos."""
        jelolt = self.HOSSZU.replace('figyelő', '<strong>figyelő</strong>').replace('szósort', '[szósort](#cel-pont)')
        lap = _lap(_kezi(self.HOSSZU), _kezi(jelolt))
        self.assertEqual(len(ismetles.ismetlesek(lap)), 1)


class AMintalapokon(unittest.TestCase):
    def test_a_kriterium_kapuja_zold_es_el(self):
        """A két mintalap generálódik (a kapu zöld), és a kapu él: ha a lap egy sora után a kritérium áll még
        egyszer, a kapu megfogja. A részleges lapon a kritérium még nem áll (a lap eleje később készül el)."""
        for azonosito in MINTALAPOK:
            motivum = MotivumId(azonosito)
            eredmeny = fo.lap_keszit(kozos.GYOKER, motivum)
            lap = eredmeny.nezetek[konfig.NEZET_TUDOMANYOS]
            kriterium = motivum_be.kriterium_szoveg(bemenet.Bemenet(kozos.GYOKER), motivum)
            self.assertTrue(kriterium, azonosito)
            self.assertEqual(ismetles.kriterium_egyszer(lap, kriterium, teljes=False), [], azonosito)
            ketszer = lap + _lap(_kezi(kriterium), _kezi(kriterium))
            self.assertTrue(ismetles.kriterium_egyszer(ketszer, kriterium, teljes=False), azonosito)

    def test_a_figyelo_talalatai_valodi_ismetlesek(self):
        """A figyelő minden találata legalább két helyen áll, és legalább az ablak hosszú (a HAMART-on kalibrálva:
        a kész szakaszokon hamis találat nincs)."""
        for azonosito in MINTALAPOK:
            eredmeny = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito))
            for talalat in eredmeny.figyelmeztetesek:
                self.assertGreaterEqual(len(talalat.helyek), 2, azonosito)
                self.assertGreaterEqual(len(talalat.szavak), konfig.ISMETLES_ABLAK, azonosito)


if __name__ == '__main__':
    unittest.main()
