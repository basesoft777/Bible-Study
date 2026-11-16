"""A 4.2 kártya (S3b): a szegmentált idézet műveletei, a lánc lépései kis bemeneten, és a kész lap fajta-térképe.

A HAMART-lapon a héber 4.2 bájtra egyezik a referenciával (a regresszió méri); itt a szabályok állnak: a jelölés
típusos darab, a forrásjavítás csak az idézet betűit cseréli, és jelölés vagy keret belsejébe egyik művelet sem nyúl.
"""
import unittest

import kozos  # noqa: F401  (a sys.path beállítása)
from kozos import MINTALAPOK
from lapgen import fo, konfig
from lapgen.bemenet import kartya as K
from lapgen.bemenet.jelolt import JelFajta, Jeloles, Jelolt, JeloltHiba, KaroliSzam
from lapgen.megjelenites.md.iro import JELOLES
from lapgen.szoveg import Fajta, Igehely, MotivumId


def _jelolt(szoveg):
    return Jelolt(szoveg, 'B18', 'szoveg_hu', 'H0000')


def _igehely(kod):
    return Igehely(kod)


class SzegmentaltIdezet(unittest.TestCase):
    def test_a_kiemeles_jeloles_darab_az_idezet_valtozatlan(self):
        j = _jelolt('föld 1Móz 2:5, 9; 3:17, 23; 4:2')
        talalt, hiany = K.kiemel(j, [('1Móz 3:17', 'a')], {'1Móz 3:23'}, _igehely)
        self.assertEqual((talalt, hiany), (['a'], []))
        self.assertEqual(j.idezet_szoveg(), 'föld 1Móz 2:5, 9; 3:17, 23; 4:2')
        fajtak = [x.fajta for x in j.jelolesek()]
        self.assertEqual(fajtak, [JelFajta.MARK_NYIT, JelFajta.MARK_ZAR, JelFajta.MARK_NYIT, JelFajta.MARK_ZAR])
        self.assertEqual([x.adat for x in j.jelolesek() if x.adat is not None],
                         [Igehely('1Móz 3:17'), Igehely('1Móz 3:23')])

    def test_a_jeloles_belsejebe_nem_lehet_beszurni(self):
        j = _jelolt('ab')
        j.beszur(1, Jeloles(JelFajta.KAROLI, None, 'XYZ'))
        with self.assertRaises(JeloltHiba):
            j.beszur(2, K.LRM)          # a „XYZ” jelölés belseje
        j.beszur(4, K.LRM)              # a jelölés után: megengedett
        self.assertEqual(j.idezet_szoveg(), 'ab')

    def test_a_forrasjavitas_jelolesen_at_nem_nyulhat(self):
        j = _jelolt('abcd')
        j.beszur(2, K.LRM)
        with self.assertRaises(JeloltHiba):
            j.javit(1, 4, 'x')

    def test_a_keret_nem_valtozhat(self):
        bek = K.Bekezdes([K.Keret('- **`2` — '), _jelolt('szöveg')])
        with self.assertRaises(JeloltHiba):
            bek.javit(3, 5, '')

    def test_a_rovidites_a_javitott_sorrendben_all_a_feloldassal(self):
        bek = K.Bekezdes([_jelolt('status absolutus ׳ח 1Móz 6:13')])
        K.izolal(bek)
        K.rovidites(bek, 'חָמָס (chámász)', 'ח')
        j = bek.jeloltek()[0]
        self.assertEqual(j.idezet_szoveg(), 'status absolutus ח׳ 1Móz 6:13')
        self.assertEqual([x.fajta for x in j.jelolesek()], [JelFajta.ABBR_NYIT, JelFajta.ABBR_ZAR, JelFajta.LRM])
        self.assertEqual(j.jelolesek()[0].adat.fajta.value, 'cimszo')

    def test_a_karoli_szamozas_jeloles_az_eredeti_szammal(self):
        class B:
            def forrasszoveg(self, b_id, mezo, ertek, hely):
                return (b_id, ertek)
        bek = K.Bekezdes([_jelolt('Péld 12:11; 28:19')])
        K.karoli_szamozas(bek, {('Péld', '12', '11'): ('12', '10')}, (set(), set()), B(), 'H0127')
        j = bek.jeloltek()[0]
        karoli = [x for x in j.jelolesek() if x.fajta is JelFajta.KAROLI]
        self.assertEqual(len(karoli), 1)
        self.assertEqual(karoli[0].adat, KaroliSzam(('B18', 'Péld'), 12, 10, 12, 11))
        self.assertEqual(j.idezet_szoveg(), '; 28:19')

    def test_az_elso_tagmondat_a_forras_reszlete_a_csonk_jel_kulon(self):
        resz, csonk = K.elso_tagmondat('2. a bűn állapota, a bűn vétke 1Móz 18:20; 50:17', csonkit_jel=True)
        self.assertEqual((resz, csonk), ('bűn állapota, a bűn vétke 1Móz 18:20', K.CSONK_SZOKOZZEL))
        self.assertIn(resz, '2. a bűn állapota, a bűn vétke 1Móz 18:20; 50:17')

    def test_a_belso_szamlalo_az_irajellel_torlodik(self):
        bek = K.Bekezdes([K.Keret(K.FEJ_KERET), _jelolt('H7451. ra \' I. רַע‎_226 melléknév')])
        bek.kesz = True
        K.belso_jelek_torlese(bek)
        self.assertEqual(bek.jeloltek()[0].idezet_szoveg(), 'I. רַע melléknév')


class ALapon(unittest.TestCase):
    """A kész lap 4.2 sorai: a jelölés-darab nem idézet, az idézet-darab nem sablon (a fajta-térkép)."""
    _lapok = {}

    @classmethod
    def lap(cls, azonosito):
        if azonosito not in cls._lapok:
            cls._lapok[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito))
        return cls._lapok[azonosito]

    def _kartya_sorai(self, azonosito):
        sorok = self.lap(azonosito).nezetek[konfig.NEZET_TUDOMANYOS]
        ki, bent = [], False
        for s in sorok:
            if s.szoveg.startswith('<!-- APPARATUS-KEZDET'):
                bent = True
            if bent:
                ki.append(s)
            if s.szoveg.startswith('<!-- APPARATUS-VÉGE'):
                bent = False
        return ki

    def test_a_kiemeles_jelolese_sablon_a_vers_idezet(self):
        for azonosito in MINTALAPOK:
            with self.subTest(azonosito):
                sorok = self._kartya_sorai(azonosito)
                self.assertTrue(sorok)
                talalt = 0
                for s in sorok:
                    for kezd, veg, fajta in s.tartomanyok:
                        darab = s.szoveg[kezd:veg]
                        if '<mark class="motivumhely"' in darab:
                            self.assertIs(fajta, Fajta.SABLON, darab)
                            talalt += 1
                        if fajta is Fajta.IDEZET:
                            self.assertNotIn('<mark', darab)
                            self.assertNotIn('<abbr', darab)
                            self.assertNotIn('(héber számozás:', darab)
                        if darab == '‎':
                            self.assertEqual(fajta, JELOLES)
                self.assertGreater(talalt, 0)


    def test_a_csonkolt_glossza_jele_sablon_a_reszlet_idezet(self):
        """E2 (az 5. ellenőrzés): az ISTENTISZT-lap H8034 kártyáján a 70 karakteres csonkolás „…” jele sablon, előtte
        a forrás szó szerinti részlete idézet; a Károli-számozás számai nem idézetek."""
        sorok = self.lap('ISTENTISZT-001').nezetek[konfig.NEZET_TUDOMANYOS]
        talalt = 0
        for s in sorok:
            i = s.szoveg.find('egyfajta halál utáni életet ad, főként…')
            if i < 0:
                continue
            veg = i + len('egyfajta halál utáni életet ad, főként')
            fajtak = {f for kezd, v, f in s.tartomanyok if kezd <= veg < v}
            self.assertEqual(fajtak, {Fajta.SABLON}, s.szoveg)
            fajtak = {f for kezd, v, f in s.tartomanyok if kezd <= i < v}
            self.assertEqual(fajtak, {Fajta.IDEZET}, s.szoveg)
            talalt += 1
        self.assertEqual(talalt, 2)         # az olvasói sor és a summary (a vázlatsor csonkja eddig is sablon volt)
        for azonosito in MINTALAPOK:
            for s in self._kartya_sorai(azonosito):
                for kezd, veg, fajta in s.tartomanyok:
                    if fajta is Fajta.IDEZET:
                        self.assertFalse(s.szoveg[kezd:veg].endswith('…'), s.szoveg)


class Reszletkapu(unittest.TestCase):
    """E2 (az 5. ellenőrzés): a glossza csak a forrás szó szerinti részlete (vagy legfeljebb három részlete) lehet."""

    class _B:
        def forrasszoveg(self, b_id, mezo, ertek, hely):
            return (b_id, ertek)

    def _k(self):
        k = type('K', (), {})()
        k.b = self._B()
        return k

    def _strong(self):
        return type('S', (), {'kod': 'H0001'})()

    def test_a_szo_szerinti_reszlet_egy_resz(self):
        from lapgen.bemenet import kartya_lap as KL
        g = KL._forras_ertek(self._k(), KL.SZOTAR_BDB, self._strong(), 'a föld  színe', 'az a föld színe, 1Móz 2:6')
        self.assertEqual(g, KL.Glossza((('B18', 'a föld színe'),), False))

    def test_a_generator_csonkolasa_jelzo_nem_idezet(self):
        from lapgen.bemenet import kartya_lap as KL
        g = KL._forras_ertek(self._k(), KL.SZOTAR_BDB, self._strong(), 'hosszú meghatározás…',
                             'hosszú meghatározás, amely folytatódik')
        self.assertEqual(g, KL.Glossza((('B18', 'hosszú meghatározás'),), True))
        g = KL._forras_ertek(self._k(), KL.SZOTAR_BDB, self._strong(), 'a forrás …', 'így: a forrás …')
        self.assertEqual(g, KL.Glossza((('B18', 'a forrás …'),), False))

    def test_a_kihagyott_zarojel_ket_reszlet(self):
        from lapgen.bemenet import kartya_lap as KL
        g = KL._forras_ertek(self._k(), KL.SZOTAR_BDB, self._strong(), 'gonosz tervet kigondolni',
                             'חָשַׁב רָעָה gonosz (ártalmas) tervet kigondolni')
        self.assertEqual(g.reszek, (('B18', 'gonosz'), ('B18', 'tervet kigondolni')))

    def test_az_atalakitott_szoveg_megall(self):
        from lapgen.bemenet import kartya_lap as KL
        with self.assertRaises(JeloltHiba):
            KL._forras_ertek(self._k(), KL.SZOTAR_BDB, self._strong(), 'föld terület', 'a terület és a föld')
        self.assertIsNone(KL.reszletek('a b c d', 'a x b x c x d'))


class ElavultThayer(unittest.TestCase):
    """E3 (az 5. ellenőrzés; GK-15, T5): az elavult `sz<n>` Thayer-fordítás munka módban a régi magyar szöveggel, a
    felülvizsgálat jelével áll, és a fordítás-állapotba kerül (kiadási módban a szakasz kapuja megáll:
    `teszt_szocikkek.test_gk15_forditas_allapot`)."""

    @classmethod
    def setUpClass(cls):
        from lapgen import bemenet
        cls.b = bemenet.Bemenet(kozos.GYOKER)
        cls.ny = bemenet.nyelv(cls.b)

    def test_a_thayer_fa_az_elavult_sor_regi_szoveget_adja_jelolve(self):
        from lapgen.bemenet import gerinc as gerinc_be
        from lapgen.szamitas import szocikkek as SZ
        f = SZ._Forrasok(self.b, MotivumId('ISTENTISZT-001'))
        sz = gerinc_be.gerinc(self.b).thayer_fa('G2532', f.forditasok)[0][0]
        self.assertIn('sz9', sz['elavult'])
        sor = next(x for x in sz['szakaszok'] if x[4] == 'sz9')
        self.assertTrue(sor[2])                         # a régi magyar szöveg áll, nem „fordításra vár”

    def test_a_jel_a_lapmodellben_es_a_lapon(self):
        from lapgen.bemenet import kartya_lap as KL
        from lapgen.megjelenites.md import kartya as md_kartya
        from lapgen.megjelenites.md.iro import Lapiro
        from lapgen.szamitas import kartya as kartya_sz
        from lapgen.szoveg import Strong
        j = Jelolt('régi szöveg', 'B14', 'forditas_hu', Strong('G2532'), True)
        darabok = kartya_sz.darabok(self.b, j)
        self.assertIs(darabok[-1].fajta, JelFajta.FELULVIZSGALAT)
        iro = Lapiro()
        iro.sor(*md_kartya.darabok(self.ny, darabok, None))
        sor = iro.kesz()[0]
        self.assertEqual(sor.szoveg, 'régi szöveg *(a fordítás felülvizsgálat alatt)*')
        self.assertEqual([f for _k, _v, f in sor.tartomanyok], [Fajta.IDEZET, Fajta.SABLON])
        gl = KL.Glossza((self.b.forrasszoveg('B14', 'forditas_hu', 'régi', Strong('G2532')),), False, True)
        iro = Lapiro()
        iro.sor(md_kartya._gl(self.ny, kartya_sz._g(gl)))
        self.assertEqual(iro.kesz()[0].szoveg, 'régi *(a fordítás felülvizsgálat alatt)*')

    def test_az_elavult_szakasz_a_forditas_allapotba_kerul(self):
        from lapgen.szamitas import szocikkek as SZ
        from lapgen.szoveg import Strong
        allapot = SZ.ForditasAllapot()
        SZ.elavult_jelez(allapot, Strong('G2532'), type('K', (), {'elavult': ('sz4', 'sz9')})())
        self.assertEqual([t.fajta for t in allapot.tetelek()], [SZ.ForditasFajta.ELAVULT] * 2)


class Arnyekmondat(unittest.TestCase):
    """E1 mechanikus része (az 5. ellenőrzés): a bemeneti réteg keret- és jelölésszövegei a sablontábla mondatának
    árnyékai (a régi lánc mintái a régi bekezdés teljes szövegén futnak). Itt minden árnyék a sablonsor kiírt
    szövegével egyezik; ha a sablon mondata változik, ez a teszt bukik."""

    @classmethod
    def setUpClass(cls):
        from lapgen import bemenet
        cls.b = bemenet.Bemenet(kozos.GYOKER)
        cls.ny = bemenet.nyelv(cls.b)

    def _l(self, szoveg):
        from lapgen.szoveg import Strong, idezet
        return idezet(self.b.forrasszoveg('B18', 'szoveg_hu', szoveg, Strong('H0001')))

    def _s(self, kulcs, **p):
        from lapgen.szoveg import kiiras
        return kiiras(self.ny.s(kulcs, **p)).szoveg

    def test_az_apparatus_keretei(self):
        from lapgen.bemenet import kartya_lap as KL
        from lapgen.szoveg import Strong
        s, l = self._s, self._l
        self.assertEqual(KL._hely(3), s('s4.p2.app.hiv', n=3))
        self.assertEqual(KL._hely(0), s('s4.p2.app.hiv.nincs'))
        self.assertEqual(KL._summary_cim(['2'], ['föld'], 3),
                         s('s4.p2.app.summary.egy', jel=l('2.'), glossza=l('föld'), hiv=self.ny.s('s4.p2.app.hiv', n=3)))
        self.assertEqual(KL._summary_cim(['2'], [], 0),
                         s('s4.p2.app.summary.egy.ures', jel=l('2.'), hiv=self.ny.s('s4.p2.app.hiv.nincs')))
        for gls, kulcs in ((['a', 'b'], 's4.p2.app.summary.tobb'), (['a', 'b', 'c', 'd', 'e'], 's4.p2.app.summary.tobb.tovabb')):
            self.assertEqual(KL._summary_cim(['1', '2', '3', '4', '5'], gls, 0),
                             s(kulcs, elso=l('1.'), utolso=l('5.'), n=5, glosszak=tuple(l(g) for g in gls[:4])))
        self.assertEqual(KL._summary_cim(['1', '2'], [], 0), s('s4.p2.app.summary.tobb.ures', elso=l('1.'),
                                                                utolso=l('2.'), n=2))
        self.assertEqual(KL._vazlat_keret('2.a').kesz, s('s4.p2.app.vazlat.eleje', jel=l('2.a')))
        eleje = s('s4.p2.app.idezet.eleje')
        uresek = 2 * chr(10)
        self.assertEqual(KL._kibontott_keret('2', 'föld').kesz,
                         s('s4.p2.app.szakasz.cimke', jel=l('2'), cimke=l('föld')) + uresek + eleje)
        self.assertEqual(KL._kibontott_keret('2', None).kesz, s('s4.p2.app.szakasz', jel=l('2')) + uresek + eleje)
        st = Strong('H0001')
        for arami in (False, True):
            ar = '.arami' if arami else ''
            k = KL._fejcim_keretek(7, arami, 'H0001', 1, 2, True)
            self.assertEqual(k[0].kesz, s('s4.p2.app.fejcim%s.eleje' % ar, szam=7))
            self.assertEqual(k[1].kesz, s('s4.p2.app.fejcim%s.vege' % ar, strong=st, i=1, n=2))
            k = KL._fejcim_keretek(7, arami, 'H0001', 1, 2, False)
            self.assertEqual(k[0].kesz, s('s4.p2.app.fejcim.ures' + ar, szam=7, strong=st, i=1, n=2))

    def test_a_jelolesek_belso_alakja(self):
        s, l = self._s, self._l
        self.assertEqual(K.FEJ_KERET, s('s4.p2.app.fej.eleje'))
        self.assertEqual(K.NINCS_KAROLI_BELSO, s('s4.p2.jel.nincs_karoli'))
        self.assertEqual('Péld 12:10' + K.KAROLI_BELSO % '12:11',
                         s('s4.p2.jel.karoli.konyv', konyv=l('Péld'), fej=12, vers=10, efej=12, evers=11))
        self.assertEqual('12:10' + K.KAROLI_BELSO % '12:11',
                         s('s4.p2.jel.karoli.fejezet', fej=12, vers=10, efej=12, evers=11))
        self.assertEqual('10' + K.KAROLI_BELSO % '12:11', s('s4.p2.jel.karoli.vers', vers=10, efej=12, evers=11))
        self.assertEqual(K.CSONK_SZOKOZZEL, s('s4.p2.jel.csonk'))
        self.assertEqual(K.CSONK_TAPADT, s('s4.p2.jel.csonk.tapadt'))
        self.assertEqual('föld' + K.CSONK_TAPADT, s('s4.p2.glossza.csonk', glossza=l('föld')))
        kiejtes = self.b.forrasszoveg('B18', 'szoveg_hu', 'adámá', 'H0127')
        self.assertEqual(K.kiejtes_jel(kiejtes).belso, s('s4.p2.jel.kiejtes', kiejtes=l('adámá')))


class KodbeliForrasjavitas(unittest.TestCase):
    """DT-F218q, N-F218i: a kártya kódba írt forrásjavításai a `bemenet.kartya.KODBELI_FORRASJAVITASOK` jegyzékben
    állnak (az S9 után javítótáblába kerülnek). A teszt bukik, ha a bemeneti réteg (kartya.py, kartya_lap.py)
    jegyzéken kívüli függvénye írja az idézet betűit (`javit`, `torol_lrm_is`, `futamonkent`, a védett `sub`)."""

    _IRO = ('javit', 'torol_lrm_is', 'futamonkent')

    def _iro_fuggvenyek(self, rel):
        import ast
        fa = kozos.fa(rel)
        ki = set()
        for f in fa.body:                       # csak a modulszintű függvények (a Bekezdes saját metódusai nem)
            if not isinstance(f, ast.FunctionDef):
                continue
            for n in ast.walk(f):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and (
                        n.func.attr in self._IRO or (n.func.attr == 'sub' and any(kw.arg == 'vedett'
                                                                                  for kw in n.keywords))):
                    ki.add(f.name)
        return ki

    def test_minden_kodbeli_forrasjavitas_a_jegyzekben_all(self):
        self.assertEqual(self._iro_fuggvenyek('bemenet/kartya.py'), set(K.KODBELI_FORRASJAVITASOK))
        self.assertEqual(self._iro_fuggvenyek('bemenet/kartya_lap.py'), set())


class TiltottFordulat(unittest.TestCase):
    """GK-06 (az 5. ellenőrzés E4 tétele): a tiltott fordulatot tartalmazó kártyaszöveg kimondott hibával megáll."""

    class _B:
        def egyszer(self, _kulcs, epito):
            return epito()

        def _tabla(self, _b_id, oszlopok=()):
            class T:
                def szotarak(self):
                    return [{'magyar_alak': 'melléknéven nevezni', 'minta': r'\bmelléknéven\s+nevez\w*'}]
            return T()

    class _K:
        pass

    def _k(self):
        k = self._K()
        k.b = self._B()
        return k

    def test_a_tiltott_fordulat_megallitja_a_kartyat(self):
        from lapgen.bemenet import kartya_lap as KL
        sz = {'fej': ('fej', '', 'őt melléknéven nevezik', '', ''), 'szakaszok': []}
        with self.assertRaises(JeloltHiba):
            KL._tiltott_kapu(self._k(), type('S', (), {'kod': 'H0001'})(), [sz], KL.SZOTAR_BDB)

    def test_tiltott_fordulat_nelkul_nincs_hiba(self):
        from lapgen.bemenet import kartya_lap as KL
        sz = {'fej': None, 'szakaszok': [(('1', '1'), '1', 'nevet adni neki', '', '')]}
        KL._tiltott_kapu(self._k(), type('S', (), {'kod': 'H0001'})(), [sz], KL.SZOTAR_THAYER)


if __name__ == '__main__':
    unittest.main()
