"""A „4. Szótári háttér” szakasz tesztjei (F218.6, S3): a váz, az áttekintő tábla és az egyszerű pontok.

GK-15 (fordítás-állapot), GK-16 (egy glossza-út), a szótári pontok rendje a táblából, a Septuaginta-megfelelő
egy mércéje, a nagy bemenetek naplózása, a regresszió részleges módja.
"""
import dataclasses
import unittest

import kozos
from lapgen import bemenet, fo, konfig, regresszio
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szotari as szotari_be
from lapgen.megjelenites.md import szocikkek as md_szocikkek
from lapgen.szamitas import szocikkek as sz
from lapgen.szamitas.vizsgalat import KapuHiba
from lapgen.szoveg import MotivumId, Strong, kiiras, prov

_MODELLEK = {}


def modell(azonosito, mod=fo.Mod.MUNKA):
    """A szakasz lapmodellje a valós adaton (motívumonként és módonként egyszer számolva)."""
    if (azonosito, mod) not in _MODELLEK:
        b = bemenet.Bemenet(kozos.GYOKER)
        _MODELLEK[(azonosito, mod)] = (sz.szamit(fo.Kornyezet(b, MotivumId(azonosito), mod)), b)
    return _MODELLEK[(azonosito, mod)]


def szoveg(lathato):
    return kiiras(lathato).szoveg


class Vaz(unittest.TestCase):
    def test_a_pontok_rendje_a_tablabol_jon(self):
        """A nyelvek saját pontjai és a nyelvfüggetlen pontok a szótári pontok táblájából jönnek; minden pontnak
        van olvasói neve a névtáblában, a megjelenítő pedig nem ismer a táblában nem álló pontot."""
        b = bemenet.Bemenet(kozos.GYOKER)
        szerepek = szotari_be.b52_szerepek(b)
        self.assertEqual(szerepek.nyelvi('gorog'), tuple(range(1, 11)))
        self.assertEqual(szerepek.nyelvi('heber'), tuple(range(1, 11)))
        self.assertEqual(szerepek.kozos(), (12, 13, 14))
        ny = bemenet.nyelv(b)
        for pont in szerepek.nyelvi('gorog') + szerepek.kozos():
            ny.nev(md_szocikkek.PONT_NEV_TIPUS, pont)
        self.assertLessEqual(set(md_szocikkek._PONTOK), set(szerepek.nyelvi('gorog')) | set(szerepek.kozos()))
        self.assertNotIn(konfig.PONT_VISSZHANG, szerepek.nyelvi('gorog') + szerepek.kozos())

    def test_a_szavak_a_ket_nyelv_kozott_oszlanak_meg(self):
        for azonosito in kozos.MINTALAPOK:
            m, _b = modell(azonosito)
            self.assertEqual(len(m.attekintes), len(m.szavak), azonosito)
            self.assertEqual(sum(len(resz.szavak) for resz in m.nyelvek), len(m.szavak), azonosito)
            self.assertEqual([resz.nyelv for resz in m.nyelvek], [sz.Nyelv.GOROG, sz.Nyelv.HEBER])
            sz.kapu(m)

    def test_a_helyek_szama_az_elofordulas_sorokbol(self):
        """Az áttekintő tábla „Helyek a motívumban” száma: ahány előfordulás-sorban a szó áll (saját számlálás)."""
        for azonosito in kozos.MINTALAPOK:
            m, b = modell(azonosito)
            sorok = bemenet.b03_elofordulasok(b, MotivumId(azonosito))
            for sor in m.attekintes:
                self.assertEqual(sor.helyek, sum(1 for s in sorok if sor.szo.strong in s.strongok))


class Glossza(unittest.TestCase):
    def test_gk16_egy_glossza_ut(self):
        """GK-16: a rövid jelentés egy függvényből jön (héber és görög szóra is), egyféle hiánnyal: az áttekintő
        tábla, a 4.1 pont és a Döntési út ugyanazt a szöveget kapja; magyar híján az angol eredeti áll, kimondott
        hiányként, és a magyar mezőbe angol szöveg nem kerül."""
        for azonosito in kozos.MINTALAPOK:
            m, b = modell(azonosito)
            rovid = motivum_be.rovid_jelentes(b)
            egy = {sor.szo.strong: sor.jelentes for resz in m.nyelvek for sor in resz.alapjelentes}
            for sor in m.attekintes:
                self.assertEqual(sor.jelentes, egy[sor.szo.strong])
                kozvetlen = rovid.jelentes(sor.szo.strong)
                self.assertEqual(sor.jelentes.magyar is None, kozvetlen.magyar is None)
                if kozvetlen.magyar is not None:
                    self.assertEqual(szoveg(sor.jelentes.magyar), kozvetlen.magyar.ertek)
                    self.assertEqual(rovid.magyar(sor.szo.strong).ertek, kozvetlen.magyar.ertek)
                    self.assertIsNone(sor.jelentes.angol)

    def test_gk16_magyar_hijan_az_angol_all_kimondott_hianykent(self):
        """Magyar rövid jelentés híján a forrás angol szava áll (`angol`), a `magyar` üres; ha az sincs, mindkettő
        hiányzik. Héber és görög szóra ugyanaz a szerkezet."""
        b = bemenet.Bemenet(kozos.GYOKER)
        rovid = motivum_be.rovid_jelentes(b)
        glosszak = motivum_be.b15_heber_glosszak(b)
        angol_csak = next((s for s, (hu, en) in sorted(glosszak.items()) if not hu and en), None)
        if angol_csak is not None:
            j = rovid.jelentes(Strong(angol_csak))
            self.assertIsNone(j.magyar)
            self.assertEqual(j.angol.ertek, glosszak[angol_csak][1])
        nincs = rovid.jelentes(Strong('H9999'))
        self.assertIsNone(nincs.magyar)
        self.assertIsNone(nincs.angol)
        gorog = rovid.jelentes(Strong('G9999'))
        self.assertIsNone(gorog.magyar)
        self.assertIsNone(gorog.angol)

    def test_gk15_forditas_allapot(self):
        """GK-15 (T5): a modell tételesen listázza a hiányzó és az elavult fordítást; `kiadas` módban ilyen tétellel
        a kapu megáll, `munka` módban a lap elkészül (az angol eredeti, illetve a régi magyar szöveg jelölve áll)."""
        m, _b = modell('HAMART-001')
        jelzes = sz.ForditasJelzes(sz.ForditasFajta.HIANYZIK, prov('{} {}', 'tW_szocikkek', Strong('H0056')))
        munka = dataclasses.replace(m, kiadas=False, forditas_allapot=(jelzes,))
        self.assertIs(sz.kapu(munka), munka)
        with self.assertRaises(KapuHiba):
            sz.kapu(dataclasses.replace(m, kiadas=True, forditas_allapot=(jelzes,)))
        with self.assertRaises(KapuHiba):
            sz.kapu(dataclasses.replace(m, kiadas=True, forditas_allapot=(
                sz.ForditasJelzes(sz.ForditasFajta.ELAVULT, prov('{}', 'Thayer')),)))
        self.assertIs(sz.kapu(dataclasses.replace(m, kiadas=True, forditas_allapot=())).kiadas, True)
        kiadas, _b = modell('HAMART-001', fo.Mod.KIADAS)
        self.assertTrue(kiadas.kiadas)
        self.assertEqual(kiadas.forditas_allapot, m.forditas_allapot)

    def test_gk15_a_jeloles_a_megjelenitoben(self):
        """A hiányzó fordítás „fordításra vár”, az elavult „a fordítás felülvizsgálat alatt” jelölést kap; a jelölés
        sablonszöveg, a forrásszöveg változatlan."""
        m, b = modell('HAMART-001')
        ny = bemenet.nyelv(b)
        alap = m.attekintes[0].jelentes.magyar
        var = md_szocikkek.szoveg_allapottal(ny, sz.Szoveg(alap, True))
        self.assertEqual(szoveg(var), szoveg(alap) + ' *(fordításra vár)*')
        elavult = md_szocikkek.szoveg_allapottal(ny, sz.Szoveg(alap, False, True))
        self.assertEqual(szoveg(elavult), szoveg(alap) + ' *(a fordítás felülvizsgálat alatt)*')
        self.assertIs(md_szocikkek.szoveg_allapottal(ny, sz.Szoveg(alap, False)), alap)
        self.assertEqual(szoveg(md_szocikkek.jelentes(ny, sz.Jelentes(None, None))),
                         'a szótár nem ad magyar rövid jelentést')
        self.assertEqual(szoveg(md_szocikkek.jelentes(ny, sz.Jelentes(None, alap))),
                         szoveg(alap) + ' *(fordításra vár)*')


class SeptuagintaMegfelelo(unittest.TestCase):
    def test_egy_merce_az_attekintesben(self):
        """A héber szó Septuaginta-megfelelője a társlista első eleme; a görög szóé a motívum héber szavai közül a
        legerősebben társuló. A társulás mértéke a közös versek kétszerese osztva a két szó verseinek összegével."""
        m, b = modell('HAMART-001')
        t = sz.tarsulas(b)
        parok = szotari_be.b36_lxx_parok(b)
        versszam = szotari_be.b35_lxx_szo_versszam(b)
        for sor in m.attekintes:
            if not sor.szo.strong.heber:
                continue
            tarsak = t.tarsak(sor.szo.strong)
            if not tarsak:
                self.assertIsNone(sor.tars)
                continue
            self.assertEqual(sor.tars.strong, tarsak[0][0])
            self.assertEqual(sor.tars_versek, tarsak[0][1])
            versek = parok.versek(sor.szo.strong)
            gorog = tarsak[0][0].kod
            kozos_db = sum(1 for g in versek.values() if gorog in g)
            self.assertEqual(kozos_db, tarsak[0][1])
            mertek = 2.0 * kozos_db / (len(versek) + versszam[gorog])
            self.assertGreaterEqual(mertek, konfig.LXX_TARS_KUSZOB)
            self.assertEqual(t.mertek(sor.szo.strong, gorog), (mertek, kozos_db))

    def test_a_nagy_bemenet_minden_fajlja_a_naploban_all(self):
        """A Septuaginta szövegkiadásának minden olvasott fájlja a naplóba kerül (a gyorsítótárból jövő indexnél
        is), a hash-ével."""
        _m, b = modell('HAMART-001')
        naplozott = {o.utvonal: o.sha256 for o in b.olvasasi_naplo() if o.b_id == 'B35'}
        self.assertEqual(sorted(naplozott), sorted(b._utvonalak('B35')))
        self.assertTrue(all(len(sha) == 64 for sha in naplozott.values()))
        masik = bemenet.Bemenet(kozos.GYOKER)
        szotari_be.b35_lxx_szo_versszam(masik)
        self.assertEqual({o.utvonal: o.sha256 for o in masik.olvasasi_naplo() if o.b_id == 'B35'}, naplozott)


class Versenkenti(unittest.TestCase):
    def test_a_szamok_a_2_tabla_ubs_cellajabol(self):
        """A versenkénti pont számai a 2. tábla UBS-cellájának modelljéből jönnek: szavanként a helyek száma a szó
        nyelvének szövetségében (saját számlálás), és a három részszám kiadja a helyek számát."""
        for azonosito in kozos.MINTALAPOK:
            m, b = modell(azonosito)
            sorok = bemenet.b03_elofordulasok(b, MotivumId(azonosito))
            konyvek = bemenet.b63_konyvek(b)
            for resz in m.nyelvek:
                heber = resz.nyelv is sz.Nyelv.HEBER
                for s in resz.versenkent.szavak:
                    sajat = sum(1 for sor in sorok if s.szo.strong in sor.strongok
                                and konyvek.ujszovetsegi(sor.igehely.konyv) != heber)
                    self.assertEqual(s.helyek, sajat, (azonosito, s.szo.strong))
                    self.assertGreaterEqual(s.helyek - s.egy - s.tobb, 0)
                    self.assertEqual(len(s.nem_egy), s.helyek - s.egy)

    def test_kovetkeztetes_csak_eleg_helynel(self):
        """Ha minden szó legfeljebb `VERSENKENTI_KIS` helyen áll, a pont nem von le következtetést; különben a
        fokozat az egy jelentésű helyek arányából jön."""
        m, _b = modell('HAMART-001')
        gorog, heber = m.nyelvek
        self.assertIsNone(gorog.versenkent.fok)
        self.assertLessEqual(max(s.helyek for s in gorog.versenkent.szavak), konfig.VERSENKENTI_KIS)
        vannak = [s for s in heber.versenkent.szavak if s.helyek]
        self.assertEqual(heber.versenkent.fok,
                         sz.fok(sum(s.egy for s in vannak) / sum(s.helyek for s in vannak)))
        self.assertIs(sz.fok(0.95), sz.Fok.SZINTE)
        self.assertIs(sz.fok(0.67), sz.Fok.TOBBSEG)
        self.assertIs(sz.fok(0.5), sz.Fok.FELE)
        self.assertIs(sz.fok(0.1), sz.Fok.KEVES)


class MasikNyelv(unittest.TestCase):
    def test_a_hid_a_motivum_szavai_kozott(self):
        """A kétnyelvű szótár hídja: a megfelelő a motívum saját szava (pontos), vagy héber szónál a görög megfelelő
        szócsaládjából áll a motívum szava az Újszövetségben; a helyek listája legfeljebb `HID_HELYEK` elemű."""
        m, _b = modell('HAMART-001')
        gorog, heber = m.nyelvek
        self.assertEqual([[x.strong.kod for x in p.szavak] for p in gorog.sece.pontosak], [['G1311', 'G5351']])
        self.assertEqual([[x.strong.kod for x in p.megfelelok] for p in gorog.sece.pontosak], [['H7843']])
        self.assertTrue(gorog.sece.pontosak[0].tovabbi)
        self.assertEqual(len(gorog.sece.pontosak[0].helyek), konfig.HID_HELYEK)
        self.assertEqual(gorog.sece.csaladok, ())
        self.assertEqual([cs.szo.strong.kod for cs in heber.sece.csaladok], ['H0779'])
        self.assertEqual([t.szo.strong.kod for t in heber.sece.csaladok[0].tagok], ['G1944', 'G2671'])
        self.assertEqual([[x.strong.kod for x in p.megfelelok] for p in heber.sece.pontosak], [['G1311', 'G5351']])
        self.assertIs(heber.sece.maradek, gorog.sece.maradek)
        self.assertEqual(heber.sece.maradek.value, 'tobbi')

    def test_a_tabla_minden_szora_all(self):
        """Szavanként egy tábla (vagy a lista kimondott hiánya); a motívum szava jelölve; a Strong-szám nélküli
        sornak nincs kiejtése és jelentése."""
        for azonosito in kozos.MINTALAPOK:
            m, _b = modell(azonosito)
            sajat = {szo.strong for szo in m.szavak}
            for resz in m.nyelvek:
                self.assertEqual([t.szo for t in resz.sece.tablak], list(resz.szavak))
                for tabla in resz.sece.tablak:
                    for sor in tabla.sorok or ():
                        self.assertEqual(sor.motivum_szava, any(st in sajat for st in sor.strongok))
                        self.assertEqual(len(sor.jelentesek), len(sor.strongok))
                        if not sor.strongok:
                            self.assertIsNone(sor.kiejtes)

    def test_a_kiirt_gorog_alak_gepi_atirasa(self):
        """A szótári alaktól eltérő, forrásban kiírt görög alak kiejtése a kiírt alak gépi átírásából jön."""
        from lapgen.bemenet import szavak
        self.assertEqual(szavak.gorog_gepi_atiras('ἀπόλλυμι'), 'apollymi')
        self.assertEqual(szavak.gorog_gepi_atiras('ᾅδης'), 'hadēs')
        self.assertEqual(szavak.gorog_gepi_atiras('εὐλογέω'), 'eulogeō')
        self.assertEqual(szavak.gorog_gepi_atiras('ῥῆμα'), 'rēma')

    def test_hn15_hamis_allapotmondat(self):
        """HN-15, GK-28 (a SECE-mondat): a megfelelők táblája alatti jegyzet a rövid jelentés forrását a valóban
        olvasott tábla nevével nevezi meg; a hamis „magyar rövid glossza-tábla a görögre még nincs” mondat egyik új
        lapon sem áll."""
        for azonosito in kozos.MINTALAPOK:
            eredmeny = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito))
            sorok = [sor.szoveg for sor in eredmeny.nezetek[konfig.NEZET_TUDOMANYOS]]
            self.assertFalse([s for s in sorok if 'még nincs' in s and 'glossza' in s], azonosito)
            jegyzet = [s for s in sorok if s.startswith('*A szólista és a sorrend a SECE-é')]
            self.assertEqual(len(jegyzet), 2, azonosito)
            self.assertTrue(all('görögül a lexikon fordítástáblája' in s for s in jegyzet))
            self.assertIn('B14', {o.b_id for o in eredmeny.naplo})
            self.assertIn('B15', {o.b_id for o in eredmeny.naplo})


class ReszlegesRegresszio(unittest.TestCase):
    REGI = '## 4. Szótári háttér\n\nbevezető\n\n### A\n\n#### 4.1. x\n\nrégi egy\n\n#### 4.2. y\n\nrégi kettő\n\n' \
           '<!-- GENERÁLT-VÉGE: z -->\n\n### Rés\n\nkézi\n'

    def _osszevet(self, uj, teljes=False):
        return regresszio.osszevet('TUDOMANYOS', self.REGI, uj, [], teljes)

    def test_a_hianyzo_alblokk_nincs_kesz(self):
        """Részleges szakaszban a még meg nem írt alblokk „nincs kész” (megszámolva), a megírt alblokk soronként
        vetődik össze; a generált blokk záró jelölője külön alblokk."""
        uj = '## 4. Szótári háttér\n\nbevezető\n\n### A\n\n#### 4.1. x\n\nrégi egy\n\n<!-- GENERÁLT-VÉGE: z -->\n\n'
        jelentes, kint, _h = self._osszevet(uj)
        self.assertEqual(kint, [])
        self.assertIn('részleges: 2 alblokk nincs kész', jelentes[-1][1])
        self.assertTrue(jelentes[-1][1].startswith('egyezik'))

    def test_a_megirt_alblokk_elterese_bukas(self):
        uj = '## 4. Szótári háttér\n\nbevezető\n\n### A\n\n#### 4.1. x\n\nmás\n\n<!-- GENERÁLT-VÉGE: z -->\n\n'
        jelentes, kint, _h = self._osszevet(uj)
        self.assertEqual(len(kint), 1)
        self.assertTrue(jelentes[-1][1].startswith('BUKÁS'))

    def test_teljes_modban_a_hianyzo_alblokk_is_elteres(self):
        uj = '## 4. Szótári háttér\n\nbevezető\n\n### A\n\n#### 4.1. x\n\nrégi egy\n\n<!-- GENERÁLT-VÉGE: z -->\n\n'
        _jelentes, kint, _h = self._osszevet(uj, teljes=True)
        self.assertGreater(len(kint), 0)

    def test_mas_szakasz_nem_reszleges(self):
        """A részleges mód csak a megnevezett szakaszra áll: más szakasz hiányzó alblokkja eltérés."""
        regi = '## 2. Előfordulások\n\n### A\n\negy\n\n### B\n\nkettő\n'
        uj = '## 2. Előfordulások\n\n### A\n\negy\n'
        _jelentes, kint, _h = regresszio.osszevet('TUDOMANYOS', regi, uj, [])
        self.assertGreater(len(kint), 0)
        self.assertIn('4. Szótári háttér', regresszio.RESZLEGES_SZAKASZOK)


if __name__ == '__main__':
    unittest.main()
