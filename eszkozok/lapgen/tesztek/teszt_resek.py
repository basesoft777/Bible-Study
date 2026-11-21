"""A kézi rések (S8b): a 4. szakasz „Miért fontos ez a lelet” rése, a 10. Értelmezés és a 11. Módszertan.

A HAMART-001 mai lapjával való bájt-egyezést a regresszió méri; itt a rés szerkezeti bontása (próza, üres sor, a kézi
forrássor helyén az olvasói forrássor a nevezett adatokkal, a belső sorok kimaradása), a vitatott pontok
szakirodalom-sora (hely, alak, a 12. szakasz száma a szakaszrendből: GK-10), és a kimondott hibák (ismeretlen jelölő,
meg nem nevezhető forrásfájl, pont nélküli szakirodalom-sor).
"""
import datetime
import unittest

import kozos
from lapgen import bemenet, fo, konfig, szakaszok
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szakirodalom as szakirodalom_be
from lapgen.ertekek import ResElemFajta
from lapgen.megjelenites.md import resek as MD
from lapgen.megjelenites.md.iro import Lapiro
from lapgen.szamitas import resek as SZ
from lapgen.szoveg import MotivumId, kiiras, prov_szoveg

HAMART, ISTENTISZT = 'HAMART-001', 'ISTENTISZT-001'
_DATUM = datetime.date(2026, 11, 13)


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


def _keret(rend=None):
    b = bemenet.Bemenet(kozos.GYOKER)
    return fo.Keret(bemenet.nyelv(b), MotivumId(HAMART), rend or fo.szakaszrend(), 'ts=2026-11-13', fo.Mod.MUNKA, b)


def _fajtak(modell):
    return [e.fajta for e in modell.elemek]


class Bontas(unittest.TestCase):

    def test_a_kezi_forrassor_helyen_olvasoi_forrassor(self):
        """A kézi forrássor helyén az olvasói forrássor: a nevezett adatbemenetek az első előfordulás rendjében, ismétlés
        nélkül; a nyers sor megjegyzésben, változatlanul. A HAMART-001 három résében 1 + 2 + 3 forrássor."""
        vart = {SZ.szamit_miert_fontos: (1, [('B07', 'B55', 'B08')]),
                SZ.szamit_ertelmezes: (2, [('B08', 'B07'), ('B08',)]),
                SZ.szamit_modszertan: (3, [('B08', 'B09', 'B07', 'B55', 'B19', 'B21'), ('B09',), ('B08', 'B07')])}
        for szamit, (db, bemenetek) in vart.items():
            m = szamit(_Korny(HAMART))
            forrasok = [e for e in m.elemek if e.fajta is ResElemFajta.FORRAS]
            self.assertEqual(len(forrasok), db)
            self.assertEqual([tuple(f.kulcs.ertek for f in e.bemenetek) for e in forrasok], bemenetek)
            for e in forrasok:
                self.assertTrue(all(f.jegyzekbeli for f in e.bemenetek))
                self.assertTrue(prov_szoveg(e.eredeti).startswith('eredeti: *Proveniencia: '))

    def test_a_belso_sorok_kimaradnak(self):
        """Az `ADAT-NÉZET` (belső szint), az `ADAT-HIV` és az egysoros `【NAPLO】` sor nem kerül a lapra; az üres
        sorok sorozata egy üres sor; a rés nem kezdődik és nem végződik üres sorral."""
        for azonosito in kozos.MINTALAPOK:
            for szamit in (SZ.szamit_miert_fontos, SZ.szamit_ertelmezes, SZ.szamit_modszertan):
                m = szamit(_Korny(azonosito))
                f = _fajtak(m)
                self.assertNotEqual(f[0], ResElemFajta.URES)
                self.assertNotEqual(f[-1], ResElemFajta.URES)
                self.assertFalse(any(a is b is ResElemFajta.URES for a, b in zip(f, f[1:])), (azonosito, szamit))
                for e in m.elemek:
                    if e.fajta is ResElemFajta.PROZA:
                        szoveg = kiiras(e.proza).szoveg
                        self.assertNotIn('<!--', szoveg)
                        self.assertNotIn('【', szoveg)

    def test_a_generator_altal_nem_olvasott_fajl_nevtablabol(self):
        """A kézi forrássorban nevezett, a generátor által nem olvasott fájl (ISTENTISZT-001: a Vulgata) a névtábla
        `kezi_forrasfajl` sorából kap nevet."""
        m = SZ.szamit_ertelmezes(_Korny(ISTENTISZT))
        nem_jegyzek = [f.kulcs.ertek for e in m.elemek if e.fajta is ResElemFajta.FORRAS for f in e.bemenetek
                       if not f.jegyzekbeli]
        self.assertIn('konkordancia/Vulgata_Clementina.tsv', nem_jegyzek)

    def test_ismeretlen_fajl_bukas(self):
        """A jegyzékben nem álló és névtábla-sor nélküli fájl a kézi forrássorban BemenetHiba; a kódfájl (a lekérdezés
        szkriptje), az archívumfájl és a nem fájlnév érték nem forrás."""
        b = bemenet.Bemenet(kozos.GYOKER)
        ut = motivum_be._jegyzek_utvonalak(b)
        with self.assertRaises(bemenet.BemenetHiba):
            motivum_be._forrassor_bemenetei(b, '*Proveniencia: scope=x | forras=adat/nincs_ilyen.tsv | ts=1*', ut)
        self.assertEqual(motivum_be._forrassor_bemenetei(
            b, "*Proveniencia: scope=x | forras=split('\\t') | ts=1 · forras=naplok/a.py+archivum/b.md+TAHOT_kivonat.tsv | ts=2*",
            ut), [(True, 'B08')])

    def test_naplo_sor(self):
        self.assertTrue(motivum_be._naplo_sor('【NAPLO: egy 【belső】 megjegyzés】'))
        self.assertFalse(motivum_be._naplo_sor('【NAPLO: nyitva'))
        self.assertFalse(motivum_be._naplo_sor('【NAPLO: egy】 és utána szöveg'))


class Szakirodalom(unittest.TestCase):

    def test_a_vitatott_pont_bekezdese_utan(self):
        """A HAMART-001 három ellenőrzött szakirodalom-sora a pontja bekezdése után áll (üres sor, a sor, üres sor);
        a szerzős sor a 12. szakaszra a szakaszrend számával hivatkozik, a hiány-sor a lekérdezés dátumát mondja."""
        m = SZ.szamit_ertelmezes(_Korny(HAMART))
        f = _fajtak(m)
        helyek = [i for i, x in enumerate(f) if x is ResElemFajta.SZAKIRODALOM]
        self.assertEqual(len(helyek), 3)
        for i in helyek:
            self.assertIs(f[i - 1], ResElemFajta.URES)
            self.assertIs(f[i - 2], ResElemFajta.PROZA)
        iro = Lapiro()
        MD._torzs(iro, _keret(), m)
        sorok = [s.szoveg for s in iro.kesz() if s.szoveg.startswith('*Szakirodalom:*')]
        self.assertEqual(len(sorok), 3)
        self.assertTrue(any(s.endswith('(Carr, 2020; a teljes hivatkozás a 12. szakaszban.)') for s in sorok))
        self.assertTrue(any(s.endswith('(Keresve: OpenAlex, Crossref, 2026-11-11.)') for s in sorok))

    def test_a_12_szakasz_szama_a_szakaszrendbol(self):
        """GK-10: a szakaszrend változásával a szakirodalom-sor hivatkozása is változik (a 11. és a 12. szakasz
        cseréje után a hivatkozás a 11. szakaszra mutat)."""
        eredeti = szakaszok._rend

        def rovidebb():
            rend = list(eredeti())
            i = next(k for k, l in enumerate(rend) if l.azonosito == 'modszertan')
            j = next(k for k, l in enumerate(rend) if l.azonosito == 'idezes')
            rend[i], rend[j] = rend[j], rend[i]
            szam = 0
            for leiro in rend:
                leiro.sorszam = None
                if leiro.szamozott:
                    szam += 1
                    leiro.sorszam = szam
            return tuple(rend)
        szakaszok._rend = rovidebb
        try:
            rend = fo.szakaszrend()
        finally:
            szakaszok._rend = eredeti
        iro = Lapiro()
        MD._torzs(iro, _keret(rend), SZ.szamit_ertelmezes(_Korny(HAMART)))
        self.assertTrue(any('a teljes hivatkozás a 11. szakaszban.)' in s.szoveg for s in iro.kesz()))

    def test_pont_nelkuli_sor_bukas(self):
        """Ellenőrzött szakirodalom-sor, amelynek pontja nem áll a vitatott pontok között: BemenetHiba (GK-06)."""
        korny = _Korny(HAMART)
        eredeti = szakirodalom_be.b75_vitatott_forrasok

        def hamis(b, motivum):
            sor = eredeti(b, motivum)[0]
            return (szakirodalom_be.VitatottForras(b.kulcs('B75', 'pont', 'Nincs ilyen pont'), sor.szerzo, sor.ev,
                                                   sor.osszefoglalo, sor.lekerdezve),)
        szakirodalom_be.b75_vitatott_forrasok = hamis
        try:
            with self.assertRaises(bemenet.BemenetHiba):
                SZ.szamit_ertelmezes(korny)
        finally:
            szakirodalom_be.b75_vitatott_forrasok = eredeti

    def test_istentiszt_nincs_szakirodalom(self):
        self.assertEqual(szakirodalom_be.b75_vitatott_forrasok(bemenet.Bemenet(kozos.GYOKER), MotivumId(ISTENTISZT)), ())


class Szakaszrend(unittest.TestCase):

    def test_a_miert_fontos_alresz(self):
        """A „Miért fontos ez a lelet” rés a 4. szakasz alrésze: a szakaszrendben közvetlenül utána áll, számozatlan, és a
        Tartalomjegyzékben nem áll (a szakaszok száma 15 marad)."""
        rend = fo.szakaszrend()
        nevek = [l.azonosito for l in rend.mind()]
        self.assertEqual(nevek[nevek.index('szocikkek') + 1], MD.AZONOSITO_MIERT_FONTOS)
        leiro = rend.mind()[nevek.index(MD.AZONOSITO_MIERT_FONTOS)]
        self.assertTrue(leiro.alresz)
        self.assertIsNone(leiro.sorszam)
        from lapgen.megjelenites.md import eleje
        self.assertEqual(len(eleje.tartalom_elemek(_keret())), 15)

    def test_a_negyedik_szakasz_egeszben_merodik(self):
        from lapgen import regresszio
        self.assertEqual(regresszio.RESZLEGES_SZAKASZOK, ())
        self.assertTrue(konfig.KEZI_FORRAS_KOD_KITERJESZTES and konfig.KEZI_FORRAS_ARCHIVUM)


if __name__ == '__main__':
    unittest.main()
