"""A 4.2 kártya (S3b): a szegmentált idézet műveletei, a lánc lépései kis bemeneten, és a kész lap fajta-térképe.

A HAMART-lapon a héber 4.2 bájtra egyezik a referenciával (a regresszió méri); itt a szabályok állnak: a jelölés
típusos darab, a forrásjavítás csak az idézet betűit cseréli, és jelölés vagy keret belsejébe egyik művelet sem nyúl.
"""
import unittest

import kozos  # noqa: F401  (a sys.path beállítása)
from kozos import MINTALAPOK
from lapgen import fo, konfig
from lapgen.bemenet import kartya as K
from lapgen.bemenet.jelolt import JelFajta, Jeloles, Jelolt, JeloltHiba
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
        self.assertEqual(karoli[0].adat, (('B19', 'Péld 12:10'), ('B18', '12:11')))
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
