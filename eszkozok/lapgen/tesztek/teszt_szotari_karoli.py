"""A 4.13 (Károli-megfelelők) és a 4.14 (rejtett és hamis párhuzam) pont: a számítás szabályai és a lap.

A szabályok a régi `szerep_karoli.py` logikáját követik (a HAMART-lapon a két pont bájtra egyezik a referenciával:
a regresszió méri); itt a szabályok külön, kis bemeneten állnak, és a két mintalap számai az adatból.
"""
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import bemenet, fo, ismetles, konfig
from lapgen.bemenet import karoli_szo as karoli_be
from lapgen.bemenet import szavak as szavak_be
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import szotari_karoli
from lapgen.szoveg import MotivumId

_LAPOK = {}


def lap(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito))
    return _LAPOK[azonosito]


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


def pont(azonosito, cim):
    """A pont látható sorai a címétől a következő címsorig vagy a blokk végéig."""
    sorok = lap(azonosito).nezetek[konfig.NEZET_TUDOMANYOS]
    kezd = next(i for i, s in enumerate(sorok) if s.szoveg.startswith('#### ') and cim in s.szoveg)
    veg = next(i for i, s in enumerate(sorok) if i > kezd and (s.szoveg.startswith('#') or 'GENERÁLT-VÉGE' in s.szoveg))
    return [lathato(s) for s in sorok[kezd:veg]]


class Bemenet(unittest.TestCase):
    def test_szotari_alak_es_egyezes(self):
        """A szótári alak a táblából jön, kisbetűvel; a táblában nem álló szó szótári alakja maga a szó. A ragozott
        alak a kulcsszóval egyezik, ha vele kezdődik, és utána legfeljebb három betű áll."""
        alakok = karoli_be.b55_szotari_alakok(bemenet.Bemenet(kozos.GYOKER))
        self.assertEqual(alakok.lemma('földet'), 'föld')
        self.assertEqual(alakok.lemma('Xyzabc'), 'xyzabc')
        self.assertTrue(alakok.egyezik('hívnám', 'hív', konfig.KAROLI_ELOTAG_MARADEK))
        self.assertFalse(alakok.egyezik('rendeléseit', 'rend', konfig.KAROLI_ELOTAG_MARADEK))

    def test_gk19_minden_par_szamit(self):
        """GK-19: a Károli–Strong párosítás minden párja számít, szűrő nélkül: a vers párjainak száma a tábla
        sorainak száma. A tartomány-kulcsra és a nem párosított könyvre az eredmény kimondottan üres."""
        b = bemenet.Bemenet(kozos.GYOKER)
        parositas = szavak_be.b54_karoli_parok(b)
        utvonal = next(u for u in b._utvonalak('B54') if u.endswith('parok_1Moz.tsv'))
        tabla = b._tabla('B54', utvonal=utvonal, oszlopok=('vers', 'hu_szo', 'strong'))
        v = tabla.oszlop('vers')
        self.assertEqual(len(parositas.parok('1Móz 3:17')), sum(1 for sor in tabla.sorok if sor[v] == '1Móz 3:17'))
        self.assertTrue(parositas.parok('1Móz 3:17'))
        self.assertEqual(tuple(parositas.parok('1Móz 4:10-11')), ())
        self.assertEqual(tuple(parositas.parok('Nincs 1:1')), ())

    def test_a_ket_pont_csak_jovahagyott_motivumon_epul(self):
        b = bemenet.Bemenet(kozos.GYOKER)
        self.assertTrue(karoli_be.b53_karoli_pontok(b, MotivumId('HAMART-001')))
        self.assertFalse(karoli_be.b53_karoli_pontok(b, MotivumId('NINCS-999')))

    def test_nyelvtani_szo(self):
        nyelvtani = karoli_be.b69_nyelvtani(bemenet.Bemenet(kozos.GYOKER))
        self.assertIn('H9001', nyelvtani)
        self.assertNotIn('H0127', nyelvtani)


class ALapon(unittest.TestCase):
    def test_a_szamok_osszeadodnak(self):
        """4.13: a szócsaládok listájának sorai és a bevezető száma egyezik; minden sor helyszáma a felsorolt
        igehelyek száma. 4.14: a hamis párhuzam könyvenkénti listájának összege a kimondott versszám."""
        for azonosito in MINTALAPOK:
            modell = lap(azonosito)
            sorok13 = pont(azonosito, 'Károli-megfelelők')
            csaladok = [s for s in sorok13 if s.startswith('- **')]
            self.assertIn('a Károli %d különböző magyar szót használ' % len(csaladok), sorok13[2], azonosito)
            for sor in csaladok:
                szam = int(sor.split('** (')[1].split(')')[0])
                self.assertEqual(szam, len(sor.rsplit(': ', 1)[1].split(', ')), sor[:40])
            sorok14 = pont(azonosito, 'Rejtett / hamis párhuzam')
            konyvsorok = [s for s in sorok14 if s.startswith('- ') and s.endswith(' vers')]
            osszeg = sum(int(s.rsplit(' — ', 1)[1].split(' ')[0]) for s in konyvsorok)
            self.assertIn('— %d vers, könyvenként' % osszeg, '\n'.join(sorok14), azonosito)
            self.assertIn('<summary>A %d vers</summary>' % osszeg, '\n'.join(sorok14), azonosito)
            self.assertTrue(modell.nezetek)

    def test_gk19_nincs_bizonyossagi_cimke_es_paronkenti_jeloles(self):
        """GK-19: a két pont látható szövegében nincs bizonyossági címke, százalékos párosítási pontosság és
        páronkénti jelölés (a párosítás pontossága egyszer, a Módszertanban áll)."""
        for azonosito in MINTALAPOK:
            szoveg = '\n'.join(pont(azonosito, 'Károli-megfelelők') + pont(azonosito, 'Rejtett / hamis párhuzam'))
            for tiltott in ('95,06', 'bizonyosság', 'megbízhatóság:', 'javaslat-állapot', '*jelölt:'):
                self.assertNotIn(tiltott, szoveg, '%s: %s' % (azonosito, tiltott))

    def test_a_forrassor_a_nevtablabol_jon(self):
        """A három nyelvfüggetlen pont (4.12, 4.13, 4.14) záró forrássora olvasói forrásneveket sorol fel (fájlnév
        nélkül); a belső proveniencia megjegyzésben áll mögötte."""
        for azonosito in MINTALAPOK:
            sorok = lap(azonosito).nezetek[konfig.NEZET_TUDOMANYOS]
            forrassorok = [s for s in sorok if s.szoveg.startswith('*(forrás: ')]
            self.assertEqual(len(forrassorok), 3, azonosito)
            for sor in forrassorok:
                lathato_resz = lathato(sor)
                self.assertNotIn('.tsv', lathato_resz)
                self.assertNotIn('proveniencia', lathato_resz)
                self.assertIn('<!-- eredeti: *(proveniencia: scope=', sor.szoveg)

    def test_a_hamart_szamai(self):
        """A HAMART-lap ismert számai (a jóváhagyott lap szerint): 25 szócsalád, 2 kulcsszavas szó, 1 rejtett
        párhuzam, 2310 hamis párhuzam."""
        szoveg13 = '\n'.join(pont('HAMART-001', 'Károli-megfelelők'))
        szoveg14 = '\n'.join(pont('HAMART-001', 'Rejtett / hamis párhuzam'))
        self.assertIn('A motívum 49 igehelyén a Károli 25 különböző magyar szót használ', szoveg13)
        self.assertIn('a motívum 15 szava közül 2-nak van', szoveg14)
        self.assertIn('— 1 hely.', szoveg14)
        self.assertIn('<summary>A 2310 vers</summary>', szoveg14)


class SzamitasSzabalyai(unittest.TestCase):
    def test_szocsalad_olvadas(self):
        """A ragozott maradék a rövidebb, legalább öt betűs szótári alakba olvad; a rövidebb alapba nem."""
        f = type('F', (), {'b': bemenet.Bemenet(kozos.GYOKER)})()
        sz = szotari_karoli._Szamolo(f)
        ig = lambda kod: bemenet.b63_konyvek(f.b).igehely(kod)   # noqa: E731
        tetelek = [('erőszak', ['erőszak'], [ig('1Móz 6:13')]),
                   ('erőszakossággal', ['erőszakossággal'], [ig('Ez 8:17')]),
                   ('úr', ['Úr'], [ig('1Móz 4:26')]), ('úrnak', ['Úrnak'], [ig('1Móz 12:8')])]
        csaladok = {lemma: (alakok, [h.kod for h in helyek]) for lemma, alakok, helyek in sz.szocsalad(tetelek)}
        self.assertEqual(csaladok['erőszak'], (['erőszak', 'erőszakossággal'], ['1Móz 6:13', 'Ez 8:17']))
        self.assertIn('úrnak', csaladok)   # az „úr” két betűs: abba nem olvad semmi

    def test_az_igehely_felsorolas_nem_ismetles(self):
        """Az ismétlés-figyelő az igehelyek hosszú, azonos felsorolását nem jelzi (a két pont listái ilyenek)."""
        for azonosito in MINTALAPOK:
            for talalat in lap(azonosito).figyelmeztetesek:
                szamos = sum(1 for szo in talalat.szavak[:konfig.ISMETLES_ABLAK] if any(b.isdigit() for b in szo))
                self.assertLessEqual(szamos, konfig.ISMETLES_SZAMOS_LEGFELJEBB, ' '.join(talalat.szavak[:12]))
        self.assertTrue(ismetles.ismetlesek)


if __name__ == '__main__':
    unittest.main()
