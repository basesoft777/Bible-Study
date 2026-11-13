"""Az S2 szelet tesztjei: a vizsgálat számai és kapui (GK-03, GK-04, GK-06, GK-09, GK-21, HN-11), a döntésnapló
bemenetei és a kizárt versek melléklete.

A valós adaton futó tesztek a két mintalap modelljét számolják (a modul szintjén gyorsítótárazva)."""
import dataclasses
import datetime
import unittest

import kozos
from kozos import MINTALAPOK, alap_minirepo, tsv
from lapgen import bemenet, fo
from lapgen.bemenet import dontes as dontes_be
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import kizarasok, vizsgalat
from lapgen.szoveg import Belso, Horgony, Igehely, MotivumId, SablonHiba, SablonSor, cim_horgony, kiiras, sablon

DATUM = datetime.date(2026, 11, 13)
_MODELLEK, _LAPOK = {}, {}
_J = ('igen', '-', '-', 'aktiv', '-', '-', 'manual')
_NEM = ('nem', '-', '-', 'aktiv', '-', '-', 'manual')


def melleklet(azonosito):
    if azonosito not in _MODELLEK:
        korny = fo.Kornyezet(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA)
        _MODELLEK[azonosito] = kizarasok.szamit(korny)
    return _MODELLEK[azonosito]


def melleklet_lap(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM).nezetek['KIZARASOK']
    return _LAPOK[azonosito]


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


class Szamok(unittest.TestCase):
    def test_gk21_a_szamok_osszeadodnak(self):
        """GK-21: a vizsgálat számai összeadódnak mindkét mintalapon; a HAMART-001 számai a jóváhagyott lapéi, és
        nem marad döntés nélküli verse."""
        for azonosito in MINTALAPOK:
            v = vizsgalat.kapu(melleklet(azonosito).vizsgalat)
            self.assertEqual(v.bent + v.csoport + v.egyen + v.nyitva, v.osszes, azonosito)
        v = melleklet('HAMART-001').vizsgalat
        self.assertEqual((v.bent, v.helyek, v.csoport, v.egyen, v.nyitva, v.osszes), (56, 49, 1542, 242, 0, 1840))
        self.assertEqual((len(v.csoport_okok), len(v.egyen_okok)), (4, 26))

    def test_gk09_a_kapu_a_modellen_fut(self):
        """GK-09: a számegyezés-kapu a lapmodell számait veti össze: az elrontott modell BUKÁS, kiírt szöveg
        nélkül."""
        v = melleklet('HAMART-001').vizsgalat
        ok = v.csoport_okok[0]
        rossz = (
            dataclasses.replace(v, csoport=v.csoport + 1),
            dataclasses.replace(v, osszes=v.osszes + 1),
            dataclasses.replace(v, csoport_okok=(dataclasses.replace(ok, versek=ok.versek[1:]),) + v.csoport_okok[1:]),
            dataclasses.replace(v, csoport_okok=(dataclasses.replace(ok, versek=ok.versek[:-1] + ok.versek[:1]),)
                                + v.csoport_okok[1:]),
            dataclasses.replace(v, csoport_okok=(dataclasses.replace(ok, versek=ok.versek[:-1] + v.bent_versek[:1]),)
                                + v.csoport_okok[1:]),
        )
        for modell in rossz:
            with self.assertRaises(vizsgalat.KapuHiba):
                vizsgalat.kapu(modell)

    def test_gk04_melleklet_kapu_mindket_lapon(self):
        """GK-04: a melléklet-kapu a modellen fut mindkét mintalapon, és a szakaszrendbe be van kötve (a lap a
        megjelenítés előtt megáll, ha a kapu bukik)."""
        for azonosito in MINTALAPOK:
            kizarasok.kapu(melleklet(azonosito))
        m = melleklet('HAMART-001')
        csonka = dataclasses.replace(m.csoport[0], konyvek=m.csoport[0].konyvek[1:])
        with self.assertRaises(vizsgalat.KapuHiba):
            kizarasok.kapu(dataclasses.replace(m, csoport=(csonka,) + m.csoport[1:]))
        leirok = {leiro.azonosito: leiro for leiro in fo.szakaszrend().mind()}
        self.assertIs(leirok['kizarasok_melleklet'].kapu, kizarasok.kapu)

    def test_minden_vers_egyszer_all_a_mellekletben(self):
        for azonosito in MINTALAPOK:
            m = melleklet(azonosito)
            versek = [v for ok in m.csoport + m.egyen for k in ok.konyvek for v in k.versek]
            self.assertEqual(len(versek), len(set(versek)), azonosito)
            self.assertEqual(len(versek), m.vizsgalat.csoport + m.vizsgalat.egyen, azonosito)


class Pillanatkep(unittest.TestCase):
    def _repo(self, forrassor):
        sorok = [('halo', 'igehely', 'allapot', 'proveniencia'), ('strong', 'A 1:1', 'x', forrassor),
                 ('strong', 'A 1:2', 'x', forrassor), ('strong', 'A 1:2', 'y', forrassor), ('karoli', 'A 1:3', 'x', 'k')]
        repo = alap_minirepo(jegyzek_sorok=[('B05', 'naplok/t_<ID>.tsv', 'teljesseg') + _NEM],
                             tovabbi={'naplok/t_PROBA-001.tsv': tsv('# generált', *sorok)} if forrassor else None)
        self.addCleanup(repo.torol)
        return bemenet.Bemenet(repo.gyoker)

    def test_gk03_hn11_elavult_pillanatkep_bukas(self):
        """GK-03, HN-11: a teljesség-mérés pillanatképe frissességi kapuval lép be: ha a mért Strong-halmaz nem
        a motívum mai halmaza, vagy a forrássor nem nevezi meg, BUKÁS."""
        m = MotivumId('PROBA-001')
        friss = dontes_be.b05_teljesseg(self._repo('scope=x | strong=H0001+H0002 | n=2'), m, {'H0002', 'H0001'})
        self.assertEqual([(k.kulcs.ertek, k.versszam) for k in friss], [('strong', 2), ('karoli', 1)])
        with self.assertRaises(bemenet.BemenetHiba) as hiba:
            dontes_be.b05_teljesseg(self._repo('scope=x | strong=H0001+H0002 | n=2'), m, {'H0001'})
        self.assertIn('elavult pillanatkép', '%s' % hiba.exception)
        with self.assertRaises(bemenet.BemenetHiba) as hiba:
            dontes_be.b05_teljesseg(self._repo('scope=x | n=2'), m, {'H0001'})
        self.assertIn('nem igazolható', '%s' % hiba.exception)

    def test_gk06_hianyzo_teljesseg_meres_kimondott_hiany(self):
        """GK-06: az opcionális teljesség-mérés hiánya kimondott hiány (None), nem üres lista és nem hiba."""
        self.assertIsNone(dontes_be.b05_teljesseg(self._repo(None), MotivumId('PROBA-001'), set()))

    def test_gk03_a_mintalapok_pillanatkepe_friss(self):
        for azonosito in MINTALAPOK:
            self.assertEqual(len(melleklet(azonosito).vizsgalat.keresesek), 3, azonosito)


class Dontesnaplo(unittest.TestCase):
    def test_b56_besorolas_es_osszesito_jelolo(self):
        """Az ok címkéje kézi adat; a címke végén álló összesítő-jelölő belső, nem része a címkének. A be nem
        sorolható indoklás BUKÁS."""
        okok = tsv(('sorrend', 'id', 'minta', 'cimke', 'megjegyzes', 'proveniencia'),
                   ('2', '*', 'általános', 'általános ok', 'közös megjegyzés', 'p'),
                   ('1', 'PROBA-001', '^összesítő sor', 'más szó áll (összesítő sor)', 'a magyar szó mást fordít', 'p'),
                   ('3', 'MASIK-001', 'általános', 'nem ide tartozó sor', '', 'p'))
        repo = alap_minirepo(jegyzek_sorok=[('B56', 'adat/okok.tsv', 'okok') + _J], tovabbi={'adat/okok.tsv': okok})
        self.addCleanup(repo.torol)
        szotar = dontes_be.b56_okok(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
        ok = szotar.besorol(Belso('Összesítő sor 3 versre', 'indoklas'))
        self.assertEqual((ok.cimke.ertek, ok.megjegyzes.ertek), ('más szó áll', 'a magyar szó mást fordít'))
        self.assertEqual(szotar.besorol(Belso('ez általános használat', 'indoklas')).cimke.ertek, 'általános ok')
        with self.assertRaises(bemenet.BemenetHiba):
            szotar.besorol(Belso('semmire nem illik', 'indoklas'))

    def test_b04_szerkezet_a_belso_szovegbol(self):
        """A döntésnapló belső szövegéből a réteg csak szerkezetet olvas ki: a csoportos sor versszámát, a
        csoportlista kulcsát és az ajánlás tényét."""
        fej = ('id', 'igehely', 'forras_kereses', 'dontes', 'indoklas', 'jelolt_tipus')
        csoportos = ('PROBA-001', 'A 1:1', 'mérés, blokk-sor (minta): 3 vers; a lista: x.tsv (halo=nf, blokk=H0001) | scope=m',
                     'elutasítva', 'Összesítő sor 3 versre (más szó) | megjegyzés', 'elofordulas')
        jeloltek = tsv(fej, csoportos, ('PROBA-001', 'B 2:3-4', 'TSK A 1:1 (2); napló: x', 'nyitva', 'egyedi', 'elofordulas'),
                       ('PROBA-001', 'C 1:1', 'kézi', 'elutasítva', 'kapcsolat', 'kapcsolat'),
                       ('MASIK-001', 'D 1:1', 'kézi', 'elutasítva', 'más', 'elofordulas'))
        repo = alap_minirepo(jegyzek_sorok=[('B04', 'adat/j.tsv', 'jeloltek') + _J], tovabbi={'adat/j.tsv': jeloltek})
        self.addCleanup(repo.torol)
        cs, egyedi = dontes_be.b04_jeloltek(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
        self.assertEqual((cs.csoport_versszam, cs.osszesito_versszam, cs.lista_oszlop, cs.lista_blokk, cs.lista_halo),
                         (3, 3, 'blokk', 'H0001', 'nf'))
        self.assertEqual((cs.dontes, cs.ajanlas, cs.indoklas.ertek),
                         (dontes_be.Dontes.ELUTASITVA, False, 'Összesítő sor 3 versre (más szó)'))
        self.assertEqual((egyedi.csoport_versszam, egyedi.dontes, egyedi.ajanlas, egyedi.igehely),
                         (None, dontes_be.Dontes.NYITVA, True, Igehely('B 2:3-4')))
        rossz = alap_minirepo(jegyzek_sorok=[('B04', 'adat/j.tsv', 'jeloltek') + _J],
                              tovabbi={'adat/j.tsv': tsv(fej, ('PROBA-001', 'A 1:1', 'kézi', 'talán', 'x', 'elofordulas'))})
        self.addCleanup(rossz.torol)
        with self.assertRaises(bemenet.BemenetHiba):
            dontes_be.b04_jeloltek(bemenet.Bemenet(rossz.gyoker), MotivumId('PROBA-001'))

    def test_tartomany_versei(self):
        self.assertEqual(dontes_be.tartomany_versei('B 2:3-5'), ('B 2:3', 'B 2:4', 'B 2:5'))
        self.assertEqual(dontes_be.tartomany_versei('B 2:3'), ('B 2:3',))
        self.assertEqual(dontes_be.tartomany_versei('B 2:30-3:2'), ('B 2:30-3:2',))


class Megjelenites(unittest.TestCase):
    def test_ezres_tagolas_es_az_igehely_reszei(self):
        """A `szam(ezres)` nem törő szóközzel tagol, a névelő a kiejtés szerint áll; az igehely könyve és
        versrésze külön paramétertípus."""
        s = SablonSor('t', '{n|a} vers, {m}', 'n:szam(ezres), m:szam(ezres)')
        self.assertEqual(kiiras(sablon(s, n=1784, m=925)).szoveg, 'az 1 784 vers, 925')
        self.assertEqual(kiiras(sablon(s, n=12500, m=1000000)).szoveg, 'a 12 500 vers, 1 000 000')
        with self.assertRaises(SablonHiba):
            SablonSor('t', '{n}', 'n:szam(tort)')
        k = SablonSor('t', '{konyv} ({db}): {versek|, }', 'konyv:konyvrov, db:szam, versek:lista(versresz)')
        versek = (Igehely('1Kir 1:52'), Igehely('1Kir 2:8'))
        self.assertEqual(kiiras(sablon(k, konyv=versek[0], db=2, versek=versek)).szoveg, '1Kir (2): 1:52, 2:8')

    def test_cim_horgony(self):
        cim = sablon(SablonSor('t', '{n}. Döntési út', 'n:szam'), n=1)
        self.assertEqual(cim_horgony(cim), Horgony('1-döntési-út'))

    def test_a_melleklet_szerkezete(self):
        """A melléklet első sora megjegyzés, a számai a modellből jönnek, és a teljesség-mérés forrássora csak
        megjegyzésben áll: a látható szövegben nincs proveniencia-sor és fájlnév."""
        for azonosito in MINTALAPOK:
            sorok = melleklet_lap(azonosito)
            self.assertEqual(lathato(sorok[0]), '', azonosito)
            szoveg = '\n'.join(lathato(sor) for sor in sorok)
            for tiltott in ('scope=', 'forras=', '.tsv', 'naplok/'):
                self.assertNotIn(tiltott, szoveg, azonosito)
            self.assertIn('scope=', '\n'.join(sor.szoveg for sor in sorok), azonosito)
        szoveg = '\n'.join(lathato(sor) for sor in melleklet_lap('HAMART-001'))
        self.assertIn('**Összeadás:** 1 542 (csoportosan kizárva) + 242 (egyenként elutasítva) = 1 784 vers.',
                      szoveg)
        self.assertIn('## Csoportosan kizárt versek, okonként', szoveg)

    def test_a_karoli_versrendje(self):
        karoli = bemenet.b07_karoli(bemenet.Bemenet(kozos.GYOKER))
        self.assertEqual(karoli.sorrend(Igehely('1Móz 1:1')), 0)
        self.assertLess(karoli.sorrend(Igehely('1Móz 3:14-15')), karoli.sorrend(Igehely('2Móz 1:1')))
        self.assertGreater(karoli.sorrend(Igehely('Nincs 1:1')), karoli.sorrend(Igehely('Jel 22:21')))


if __name__ == '__main__':
    unittest.main(verbosity=1)
