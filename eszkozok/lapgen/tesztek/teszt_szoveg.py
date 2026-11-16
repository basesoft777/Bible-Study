"""A látható szöveg típusának tesztjei (F218a brief 2. pont, 1. réteg; GK-08a típus-része, GK-23)."""
import datetime
import unittest

import kozos  # noqa: F401  (a sys.path beállítása)
from lapgen.megjelenites.md import iro
from lapgen.szoveg import (Belso, Fajta, Forrasszoveg, Horgony, Igehely, Kezi, Kulcs, Lathato, MotivumId, Nev,
                           Proveniencia, SablonHiba, SablonSor, Strong, SzovegHiba, idezet, kiiras, prov,
                           prov_szoveg, proza, sablon)


def _sor(mondat, parameterek='-'):
    return SablonSor('teszt', mondat, parameterek)


class HaromKonstruktor(unittest.TestCase):
    def test_gk08a_lathato_kozvetlenul_nem_hozhato_letre(self):
        """GK-08a: a Lathato csak a három konstruktorral készülhet."""
        with self.assertRaises(SzovegHiba):
            Lathato(((Fajta.SABLON, 'x'),))

    def test_gk08a_proza_csak_kezi_ertekbol(self):
        self.assertEqual(kiiras(proza(Kezi('kézi szöveg', 'm'))).szoveg, 'kézi szöveg')
        for rossz in ('nyers', Belso('belső', 'm'), Kulcs('k', 'm'), Forrasszoveg('f', 'm', 'B07', None)):
            with self.assertRaises(SzovegHiba):
                proza(rossz)

    def test_gk08a_idezet_csak_forrasszovegbol(self):
        ertek = Forrasszoveg('És monda', 'szoveg', 'B07', Igehely('1Móz 3:14'))
        kiirt = kiiras(idezet(ertek))
        self.assertEqual(kiirt.szoveg, 'És monda')
        self.assertEqual(kiirt.tartomanyok, ((0, 8, Fajta.IDEZET),))
        for rossz in ('nyers', Kezi('k', 'm'), Belso('b', 'm')):
            with self.assertRaises(SzovegHiba):
                idezet(rossz)

    def test_gk08a_sablon_nyers_szoveget_nem_fogad(self):
        """GK-08a: nyers `str` sablonparaméter nem adható át, sem skalárként, sem listaelemként."""
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x}', 'x:lathato'), x='nyers szöveg')
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x|, }', 'x:lista(lathato)'), x=('nyers',))
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x}', 'x:szam'), x='3')

    def test_gk08a_lathato_nem_str(self):
        """A Lathato nem alakítható szöveggé a kiiras() megkerülésével, és nincs rajta szövegművelet."""
        l = sablon(_sor('mondat'))
        with self.assertRaises(SzovegHiba):
            str(l)
        with self.assertRaises(TypeError):
            '%s' % l
        with self.assertRaises(TypeError):
            '{}'.format(l)
        with self.assertRaises(TypeError):
            l + 'x'
        with self.assertRaises(TypeError):
            l[0:2]
        for muvelet in ('replace', 'split', 'translate', 'join', 'strip', 'format'):
            self.assertFalse(hasattr(l, muvelet), muvelet)
        with self.assertRaises(AttributeError):
            l.barmi = 1

    def test_burkolok_es_azonositok_nem_alakulnak_szovegge(self):
        for ertek in (Kezi('a', 'm'), Belso('a', 'm'), Kulcs('a', 'm'), Forrasszoveg('a', 'm', 'B', None),
                      Strong('H0779'), Igehely('1Móz 3:14'), MotivumId('PROBA-001'), Nev('t', 'k', 'név')):
            with self.assertRaises(TypeError):
                '%s' % ertek
            with self.assertRaises(TypeError):
                '{}'.format(ertek)


class Sablon(unittest.TestCase):
    def test_parameterek_kotott_tipusa(self):
        sor = _sor('{db} helyből {hely}: {szo} ({nev}), {datum}, {arany}',
                   'db:szam, hely:igehely, szo:strong, nev:nev(szint), datum:datum, arany:tizedes(2)')
        l = sablon(sor, db=49, hely=Igehely('Gal 3:13-14'), szo=Strong('G1944'), nev=Nev('szint', 'p', 'Peshat'),
                   datum=datetime.date(2026, 11, 13), arany=95.06)
        self.assertEqual(kiiras(l).szoveg, '49 helyből Gal 3:13-14: G1944 (Peshat), 2026-11-13, 95,06')

    def test_rossz_tipus_hiba(self):
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x}', 'x:szam'), x=True)
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x}', 'x:igehely'), x=Strong('H0001'))
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x}', 'x:nev(szint)'), x=Nev('masik', 'k', 'n'))

    def test_hianyzo_es_folos_parameter(self):
        with self.assertRaises(SablonHiba):
            sablon(_sor('{x}', 'x:szam'))
        with self.assertRaises(SablonHiba):
            sablon(_sor('mondat'), x=1)

    def test_hibas_sablonsor(self):
        for mondat, par in (('{x}', '-'), ('nincs benne', 'x:szam'), ('{x}', 'x:ismeretlen'), ('{x', 'x:szam'),
                            ('{x}', 'x:szam, x:szam')):
            with self.assertRaises(SablonHiba):
                _sor(mondat, par)

    def test_lista_elvalasztoval(self):
        elemek = (idezet(Forrasszoveg('a', 'm', 'B', None)), idezet(Forrasszoveg('b', 'm', 'B', None)),
                  idezet(Forrasszoveg('c', 'm', 'B', None)))
        self.assertEqual(kiiras(sablon(_sor('{x|; }', 'x:lista(lathato)'), x=elemek)).szoveg, 'a; b; c')
        self.assertEqual(kiiras(sablon(_sor('{x|, | és }', 'x:lista(lathato)'), x=elemek)).szoveg, 'a, b és c')
        self.assertEqual(kiiras(sablon(_sor('[{x|, }]', 'x:lista(szam)'), x=(1, 2))).szoveg, '[1, 2]')
        self.assertEqual(kiiras(sablon(_sor('[{x|, }]', 'x:lista(szam)'), x=())).szoveg, '[]')

    def test_nevelo(self):
        sor = _sor('a BDB {sz|a} szakaszban', 'sz:lathato')

        def ki(szoveg):
            return kiiras(sablon(sor, sz=idezet(Forrasszoveg(szoveg, 'm', 'B', None)))).szoveg

        self.assertEqual(ki('Qal'), 'a BDB a Qal szakaszban')
        self.assertEqual(ki('1.'), 'a BDB az 1. szakaszban')
        self.assertEqual(ki('1.b'), 'a BDB az 1.b szakaszban')
        self.assertEqual(ki('3.'), 'a BDB a 3. szakaszban')
        self.assertEqual(ki('5'), 'a BDB az 5 szakaszban')
        self.assertEqual(ki('10.c'), 'a BDB a 10.c szakaszban')
        self.assertEqual(ki('1000'), 'a BDB az 1000 szakaszban')
        self.assertEqual(ki("Hiph'il 2"), "a BDB a Hiph'il 2 szakaszban")
        self.assertEqual(ki('etimológia'), 'a BDB az etimológia szakaszban')
        self.assertEqual(kiiras(sablon(_sor('{sz|A} szakasz', 'sz:szam'), sz=1)).szoveg, 'Az 1 szakasz')

    def test_fajta_terkep_megorzi_a_beagyazott_fajtat(self):
        sor = _sor('Funkció: {f} — „{v}”', 'f:lathato, v:lathato')
        kiirt = kiiras(sablon(sor, f=proza(Kezi('láncszem', 'funkcio')),
                              v=idezet(Forrasszoveg('átkozott', 'vers', 'B07', None))))
        self.assertEqual(kiirt.szoveg, 'Funkció: láncszem — „átkozott”')
        fajtak = [(kiirt.szoveg[k:v], f) for k, v, f in kiirt.tartomanyok]
        self.assertEqual(fajtak, [('Funkció: ', Fajta.SABLON), ('láncszem', Fajta.PROZA), (' — „', Fajta.SABLON),
                                  ('átkozott', Fajta.IDEZET), ('”', Fajta.SABLON)])


class Azonositok(unittest.TestCase):
    def test_szigoru_alak(self):
        for rossz in ('H779', 'X0001', 'H0779 megjegyzés', ''):
            with self.assertRaises(SzovegHiba):
                Strong(rossz)
        for rossz in ('1Móz 3', 'adat/x.tsv', '1Móz 3:14 (megjegyzés)'):
            with self.assertRaises(SzovegHiba):
                Igehely(rossz)
        for rossz in ('proba-001', 'PROBA-1', 'PROBA-001 x'):
            with self.assertRaises(SzovegHiba):
                MotivumId(rossz)
        with self.assertRaises(SzovegHiba):
            Horgony('Nagy Betű')

    def test_igehely_reszei(self):
        hely = Igehely('Zsid 6:7-8')
        self.assertEqual((hely.konyv, hely.fejezet, hely.vers), ('Zsid', 6, 7))
        self.assertEqual(Igehely('1Móz 3:14'), Igehely('1Móz 3:14'))
        self.assertEqual(Igehely('2Móz 15:5,8').vers, 5)


class ProvenienciaEsIro(unittest.TestCase):
    def test_proveniencia_csak_megjegyzesbe_irhato(self):
        """A proveniencia a lapon csak HTML-megjegyzésként jelenik meg; sablonparaméter nem lehet."""
        p = prov('proveniencia: {} | igazolas: {}', Belso('scope=manual', 'proveniencia'), Kulcs('nincs', 'igazolas'))
        self.assertIsInstance(p, Proveniencia)
        self.assertEqual(prov_szoveg(p), 'proveniencia: scope=manual | igazolas: nincs')
        with self.assertRaises(SzovegHiba):
            sablon(_sor('{x}', 'x:lathato'), x=p)
        lap = iro.Lapiro()
        lap.sor(sablon(_sor('látható')), p)
        sor = lap.kesz()[0]
        self.assertEqual(sor.szoveg, 'látható<!-- proveniencia: scope=manual | igazolas: nincs -->')
        self.assertEqual(sor.tartomanyok[1][2], iro.MEGJEGYZES)

    def test_az_iro_nyers_szoveget_nem_fogad(self):
        lap = iro.Lapiro()
        with self.assertRaises(SzovegHiba):
            lap.sor('nyers szöveg')
        with self.assertRaises(SzovegHiba):
            lap.cimsor(2, 'nyers cím')
        with self.assertRaises(SzovegHiba):
            lap.sor(Belso('belső', 'm'))
        with self.assertRaises(SzovegHiba):
            iro.Jel('<b>')

    def test_megjegyzes_nem_zarhato_le_belulrol(self):
        lap = iro.Lapiro()
        with self.assertRaises(SzovegHiba):
            lap.sor(prov('{}', Belso('a --> b', 'm')))

    def test_festett_burkolo_jelzoszot_hordoz(self):
        """Festett futásban a burkoló szöveges alakja hordozza a jelzőszót; az érték változatlan."""
        k = Kulcs('magas', 'megbizhatosag', 'ZZQB03_megbizhatosagZZ')
        self.assertEqual(k.ertek, 'magas')
        self.assertEqual(k, Kulcs('magas', 'megbizhatosag'))
        self.assertIn('ZZQB03_megbizhatosagZZ', prov_szoveg(prov('{}', k)))
        kezi = Kezi('próza', 'kapcsolodas', 'ZZQB03_kapcsolodasZZ')
        self.assertEqual(kiiras(proza(kezi)).szoveg, 'próza ZZQB03_kapcsolodasZZ')


if __name__ == '__main__':
    unittest.main(verbosity=1)
