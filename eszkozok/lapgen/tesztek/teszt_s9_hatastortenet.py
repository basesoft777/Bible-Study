"""A „9. Hatástörténet: ókori fordítások és értelmezők” szakasz (S7): a modell számai a valós adaton, a szakasz
bájtra a HAMART-001 mai lapjával, a szópár (GK-SZOPAR), a rokon nyelvi tábla hiánymondata (GK-A6) és a forrás-állapot
mondatai (GK-28: Targum, Peshitta).

A HAMART-001 mai lapjának 9. szakasza: hat lánc-szó (a több versben álló ötből a Targum 3, a Vulgata 2, a LXX 4 szót
ad vissza minden versben egy szóval), egy betoldás (1Móz 8:21, a Targum); két görög szócsalád (egy egyezik); hat
helyen tíz tanú, köztük a Glossa Ordinaria.

A `teszt_f194_szopar.py` esetei az új generátoron (GK-SZOPAR): `SzoparLanc` — itt (`Szopar`); `Szoparkapu` — a
`teszt_lxx.py` `test_lxx_egyezes_kapu` tesztje (a szópáros motívumon minden tag a teljes versszámot mondja);
`TobbLemma` — itt (`test_tobb_lemmas_tarsitas`); `PontozatlanRokonAlak` (a táblarész) — a `teszt_szocikkek.py`
`test_istentiszt_szopar_ut` tesztje; `SzoparJegyzet` — a 2. tábla jegyzete a szópáros lapon, a `teszt_elofordulas.py`
jegyzet-tesztjei; a régi lapszöveg-kapuk esetei (`PontozatlanRokonAlak` kapurésze, `Szabaly42Cimke`, `NyersJelKapu`,
`MintaKapu`) a régi `olvasoi_kapu.py`-t és `ellenoriz.py`-t mérik: a brief O6 pontja szerint a 218c-ben kerülnek a
modellre.
"""
import datetime
import os
import unittest

import kozos
from lapgen import bemenet, fo, konfig
from lapgen.bemenet import elofordulas as elofordulas_be
from lapgen.bemenet import hatastortenet as HB
from lapgen.bemenet import lxx as lxx_be
from lapgen.bemenet import nyelvi_hatter as nyelvi_hatter_be
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import ForrasAllapot, TanuForras
from lapgen.megjelenites.md import hatastortenet as MD
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import hatastortenet as HS
from lapgen.szamitas import nyelvi_hatter as nyelvi_hatter_sz
from lapgen.szamitas import szocikkek as szocikkek_sz
from lapgen.szamitas.szotari_tipusok import Szo
from lapgen.szoveg import MotivumId, Strong, kiiras

_MODELL, _LAP = {}, {}
_DATUM = datetime.date(2026, 11, 13)
HAMART, ISTENTISZT = 'HAMART-001', 'ISTENTISZT-001'


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


def modell(azonosito):
    if azonosito not in _MODELL:
        _MODELL[azonosito] = HS.szamit(_Korny(azonosito))
    return _MODELL[azonosito]


def ny():
    return bemenet.nyelv(bemenet.Bemenet(kozos.GYOKER))


def szoveg(lathato):
    return kiiras(lathato).szoveg


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


def szakasz_sorai(azonosito):
    """A kész lap 9. szakaszának sorai (a 9. címsortól a következő szakaszig, illetve a nézet végéig)."""
    if azonosito not in _LAP:
        lap = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=_DATUM).nezetek[konfig.NEZET_TUDOMANYOS]
        eleje = next(i for i, s in enumerate(lap) if s.szoveg.startswith('## ') and 'Hatástörténet' in s.szoveg)
        vege = next((i for i in range(eleje + 1, len(lap)) if lap[i].szoveg.startswith('## ')), len(lap))
        _LAP[azonosito] = lap[eleje:vege]
    return _LAP[azonosito]


class Szamok(unittest.TestCase):
    def test_hamart_oszovetsegi_tabla(self):
        o = modell(HAMART).osz
        self.assertFalse(o.szopar)
        self.assertEqual(o.teljes, (3, 2, 4))
        self.assertEqual([s.szo.strong.kod for s in o.sorok], ['H0779', 'H6093', 'H0127', 'H2403', 'H7843', 'H2555'])
        self.assertEqual([s.strong.kod for s in o.egyverses], ['H2403'])
        self.assertEqual((o.mag_hely.konyv, o.mag_elso, o.mag_utolso), ('1Móz', 3, 9))
        self.assertEqual([(b.hely.kod, b.betoldok) for b in o.betoldasok], [('1Móz 8:21', (HS.Forditas.TARGUM,))])
        # az iccávón Targum-cellája: minden versben más szó; a sáchat Vulgata-cellája: a versek egy részében
        self.assertIs(o.sorok[1].cellak[0].fajta, HS.CellaFajta.KULONBOZO)
        sachat = o.sorok[4].cellak[1]
        self.assertEqual((sachat.fajta, sachat.n, sachat.nn, sachat.mind_mas_szo), (HS.CellaFajta.RESZ, 2, 6, True))

    def test_hamart_lxx_alapvonal(self):
        """A LXX-mondatok a mai lap számai szerint: árar 39/47 (a szócsalád), adámá 87/89, chattát 252/266, chámász
        22/52 (gyakori); az iccávón a láncon kívül nem fordul elő; a sáchat egy versben más szót kap."""
        lxx = [s.mondatok[-1].lxx for s in modell(HAMART).osz.sorok]
        alap = [(m.alapvonal.talalat, m.alapvonal.nn, m.alapvonal.sav, m.szocsalad) if m.alapvonal else m.fajta
                for m in lxx]
        self.assertEqual(alap, [(39, 47, HS.Sav.SZOKASOS, True), HS.LxxFajta.NEM_MERHETO,
                                (87, 89, HS.Sav.SZOKASOS, False), (252, 266, HS.Sav.SZOKASOS, False),
                                HS.LxxFajta.ELTERES, (22, 52, HS.Sav.GYAKORI, False)])

    def test_hamart_ujszovetsegi_tabla_es_tanuk(self):
        u = modell(HAMART).usz
        self.assertEqual([r.mit for r in u.sorok], [HS.UszMit.RESZBEN, HS.UszMit.EGYEZO])
        self.assertEqual(u.egyezo, 1)
        self.assertEqual([t.kod for t in u.tematikus], ['Jel 22:3'])
        self.assertTrue(u.sorok[0].csaladon_belul)
        self.assertEqual([len(r.valtozatok) for r in u.sorok], [1, 0])
        self.assertIs(u.peshitta, ForrasAllapot.NEM_VIZSGALT)
        t = modell(HAMART).tanuk
        self.assertEqual((len(t.sorok), t.helyek, t.glossa), (10, 6, True))
        self.assertEqual(sum(1 for x in t.sorok if x.forras is TanuForras.CHAIN_LINEAGE), 4)


class Regresszio(unittest.TestCase):
    def test_a_hamart_kilencedik_szakasza_bajtra_a_mai_lap(self):
        """A 9. szakasz a jóváhagyott lap szövegével bájtra egyezik (a szakaszban engedélysor nincs)."""
        with open(os.path.join(kozos.GYOKER, 'lexikon', HAMART + '_TUDOMANYOS.md'), encoding='utf-8') as f:
            ref = f.read().replace('\r\n', '\n').split('\n')
        eleje = next(i for i, s in enumerate(ref) if s.startswith('## 9. Hatástörténet'))
        vege = next(i for i in range(eleje + 1, len(ref)) if ref[i].startswith('## '))
        uj = [s.szoveg for s in szakasz_sorai(HAMART)]
        self.assertEqual(uj, ref[eleje:vege])


class Szopar(unittest.TestCase):
    """GK-SZOPAR (DT833; a spec 6.3 feltételei): tisztán szópáros motívumon (van `H…+H…` hordozó elem, és nincs egyes
    szavas héber) (1) a 9. szakasz ószövetségi táblája nem üres; (2) a lánc-szó a formula igéje (a pár első tagja);
    (3) a versek a motívum saját ószövetségi versei, Peshat-mag nélkül; (4) a bevezető kimondja, hogy a táblázat a
    formula igéjét követi; (5) az ellenőrzött, alak nélküli LXX-sor „nincs megfelelő szó”; (6) az LXX-egyezés kapuja a
    szópár-feltételt használja; (7) a HAMART-001 szakasza változatlan (`Regresszio`); (8) a régi `SzoparLanc`
    esetei."""

    class _Sor:
        def __init__(self, elem):
            self.gerinc_elem = type('E', (), {'ertek': elem})()

    def test_szopar_felismeres(self):
        sorok = [self._Sor('H7121+H8034'), self._Sor('G1941')]
        self.assertTrue(elofordulas_be.szopar_motivum(sorok))
        # az egyes szavas lánc melletti szópár nem teszi szópárossá (HAMART-001: málé + chámász)
        self.assertFalse(elofordulas_be.szopar_motivum(sorok + [self._Sor('H2555')]))
        self.assertFalse(elofordulas_be.szopar_motivum([self._Sor('H0779')]))

    def test_istentiszt_lanc(self):
        f = szocikkek_sz.forrasok(bemenet.Bemenet(kozos.GYOKER), MotivumId(ISTENTISZT))
        self.assertTrue(elofordulas_be.szopar_motivum(f.sorok))
        lanc = nyelvi_hatter_sz.lanc_szavak(f, MotivumId(ISTENTISZT))
        self.assertEqual([g.kod for g, _v in lanc], ['H7121'])
        versek = lanc[0][1]
        self.assertEqual(len(versek), 16)
        self.assertEqual(versek[0].kod, '1Móz 4:26')
        self.assertFalse([v for v in versek if f.konyvek.ujszovetsegi(v.konyv)])
        o = modell(ISTENTISZT).osz
        self.assertTrue(o.szopar)
        self.assertEqual((o.sorok[0].szo.strong.kod, o.par.strong.kod), ('H7121', 'H8034'))

    def test_hamart_lanc_nem_szopar(self):
        f = szocikkek_sz.forrasok(bemenet.Bemenet(kozos.GYOKER), MotivumId(HAMART))
        self.assertFalse(elofordulas_be.szopar_motivum(f.sorok))
        self.assertFalse(modell(HAMART).osz.szopar)

    def test_a_szakasz_szovege(self):
        sorok = [lathato(s) for s in szakasz_sorai(ISTENTISZT)]
        bevezeto = next(s for s in sorok if s.startswith('A táblázat azt mutatja, hogyan adja vissza'))
        self.assertIn('a táblázat a formula igéjét követi', bevezeto)
        self.assertIn('(16 vers)', bevezeto)
        tabla = next(s for s in sorok if s.startswith('| קָרָא'))
        self.assertTrue(tabla.endswith('| LXX: egy versben nincs megfelelő szó. |'))
        self.assertFalse([s for s in sorok if 'Genezis' in s])

    def test_az_lxx_kapu_a_szopar_feltetelt_hasznalja(self):
        import inspect
        from lapgen.szamitas import lxx as lxx_sz
        self.assertIn('elofordulas_be.szopar_motivum(', inspect.getsource(lxx_sz.hid))

    def test_tobb_lemmas_tarsitas(self):
        """A régi `TobbLemma`: a több lemmás társítás (1Kir 18:24: βοάω · ἐπικαλέω) minden lemmája külön számít."""
        b = bemenet.Bemenet(kozos.GYOKER)
        t = lxx_be.Tarsitas(b.forrasszoveg('B38', 'lemma', 'βοάω · ἐπικαλέω', '1Kir 18:24'),
                            b.forrasszoveg('B38', 'kiejtes', 'boaó · epikaleó', '1Kir 18:24'))
        self.assertEqual(t.lemmak(), ['βοαω', 'επικαλεω'])


class RokonNyelviTabla(unittest.TestCase):
    def test_gk_a6_rokon_nyelvi_tabla(self):
        """GK-A6: „a kinyerés még nem történt meg” pontosan azoknál a lánc-szavaknál áll, amelyeknek nincs
        BDB-soruk a visszhang-táblában, és a rokon írások lekérdezése sem futott rájuk; a lekérdezett, sor nélküli
        szónál a „nincs rokon nyelvi alak” mondat áll."""
        for azonosito in kozos.MINTALAPOK:
            b = bemenet.Bemenet(kozos.GYOKER)
            motivum = MotivumId(azonosito)
            f = szocikkek_sz.forrasok(b, motivum)
            from lapgen.bemenet import gerinc as gerinc_be
            rokon = nyelvi_hatter_sz._rokon(f, motivum, gerinc_be.gerinc(b))
            van_sora = {r.strong for r in nyelvi_hatter_be.b38_visszhang(b, motivum).rokon}
            lekerdezve = nyelvi_hatter_be.b24_rokon_irasok(b)
            for r in rokon:
                vart = r.szo.strong not in van_sora and r.szo.strong.kod not in lekerdezve
                self.assertEqual(r.hiany is nyelvi_hatter_sz.Hiany.NINCS_KINYERES, vart, (azonosito, r.szo.strong))
                if r.szo.strong not in van_sora and not vart:
                    self.assertIs(r.hiany, nyelvi_hatter_sz.Hiany.NINCS_SOR)


class ForrasAllapotMondat(unittest.TestCase):
    """GK-28 (T7), a szelet része: a Targum- és a Peshitta-mondat a jegyzék `allapot` mezőjéből és az adat tényleges
    állapotából. (A Chain Lineage- és a közel-keleti mondat a Kolofoné: S8; a SECE-mondat az S3-é.)"""

    def test_a_targum_hiany_a_forras_lefedettsegebol(self):
        """A Targum-forrás a Zsoltárokat nem fedi: a három Zsoltár-vers „nincs Targum-forrás”, nem „nincs
        megfelelő szó”; a kódba írt Mózes-könyv lista mondata egyik lapon sem áll."""
        b = bemenet.Bemenet(kozos.GYOKER)
        targum = HB.b64_targum(b)
        self.assertIs(targum.allapot, ForrasAllapot.RESZLEGES)
        cella = modell(ISTENTISZT).osz.sorok[0].cellak[0]
        self.assertEqual([v.kod for v in cella.targum_kivul], ['Zsolt 116:4', 'Zsolt 116:13', 'Zsolt 116:17'])
        self.assertTrue(all(not targum.fedi(v) for v in cella.targum_kivul))
        self.assertFalse([e for e in cella.versek if e.hely in cella.targum_kivul])
        for azonosito in kozos.MINTALAPOK:
            self.assertFalse([s for s in szakasz_sorai(azonosito) if 'Mózes-könyveket' in s.szoveg])

    def test_a_targum_allapota_es_az_adat_ellentmondasa_bukas(self):
        b = bemenet.Bemenet(kozos.GYOKER)
        b.jegyzek_sor('B64').allapot = 'aktiv'
        with self.assertRaises(BemenetHiba):
            HB.b64_targum(b)
        b = bemenet.Bemenet(kozos.GYOKER)
        b.jegyzek_sor('B64').allapot = 'nem_vizsgalt'
        with self.assertRaises(BemenetHiba):
            HB.b64_targum(b)

    def test_a_targum_kulcs_kapuja(self):
        """A lefedettség csak ismert ószövetségi „könyv fejezet:vers” kulcsokból állapítható meg; idegen kulcs és üres
        forrás BUKÁS (különben minden Targum-cella hamisan „nincs Targum-forrás” lenne)."""
        from lapgen.bemenet.jegyzek import Tabla
        for sorok in ([('Psalms 1:1',)], [('Mt 1:1',)], []):
            b = bemenet.Bemenet(kozos.GYOKER)
            eredeti = b._tabla

            def tabla(b_id, _s=sorok, _e=eredeti, **kw):
                return Tabla(('igehely',), _s) if b_id == 'B64' else _e(b_id, **kw)
            b._tabla = tabla
            with self.assertRaises(BemenetHiba, msg=repr(sorok)):
                HB.b64_targum(b)

    def test_a_nem_fedett_versre_allo_targum_sor_bukas(self):
        """Ha a Targum-forrás nem fedi a verset, de ellenőrzött, alakos Targum-sor áll rá, az adat ellentmond: BUKÁS
        (a sor nem rejtőzhet el a „nincs Targum-forrás” mondat mögött). A lefedés itt a Mózes-könyveket nem
        tartalmazza; a HAMART-001 láncversei mind az 1Mózesben állnak."""
        eredeti = HS.ht_be.b64_targum
        HS.ht_be.b64_targum = lambda b: HB.TargumLefedes(ForrasAllapot.RESZLEGES, frozenset({'Ézs'}))
        try:
            with self.assertRaises(BemenetHiba):
                HS.szamit(_Korny(HAMART))
        finally:
            HS.ht_be.b64_targum = eredeti

    def test_szopar_tematikus_hellyel_kapuhiba(self):
        """A szópáros újszövetségi bevezető a tematikus helyek kimaradását nem tudja kimondani: kimondott hiba, nem
        néma hiány (GK-06)."""
        from lapgen.megjelenites.md.iro import Lapiro
        from lapgen.szamitas.vizsgalat import KapuHiba
        from lapgen.szoveg import Igehely
        u = HS.UszTabla(szopar=True, mag_hely=None, tematikus=(Igehely('Jel 22:3'),), sorok=(), egyezo=0,
                        peshitta=ForrasAllapot.NEM_VIZSGALT)
        with self.assertRaises(KapuHiba):
            MD._usz(Lapiro(), ny(), u)

    def test_a_tanu_koranak_belso_resze(self):
        """A tanú korának látható része a mező eleje; a belső rész csak „ (HCF: <év>)” alakú lehet."""
        self.assertEqual(HB._KOR_RX.match('4. sz. (HCF: 373)').group('kor'), '4. sz.')
        self.assertEqual(HB._KOR_RX.match('7. sz.').group('kor'), '7. sz.')
        self.assertEqual(HB._KOR_RX.match('').group('kor'), '')
        self.assertIsNone(HB._KOR_RX.match('4. sz. (HCF 373)'))

    def test_a_peshitta_mondat_az_allapotbol(self):
        b = bemenet.Bemenet(kozos.GYOKER)
        self.assertIs(HB.b73_peshitta(b), ForrasAllapot.NEM_VIZSGALT)
        for azonosito in kozos.MINTALAPOK:
            sorok = [s.szoveg for s in szakasz_sorai(azonosito)]
            self.assertEqual(sum(1 for s in sorok if 'A szír fordítás (Peshitta) nem vizsgált' in s), 1, azonosito)
        # a forrás megvan, a jegyzék „nem vizsgált”-at mond: elavult jegyzék, BUKÁS
        b = bemenet.Bemenet(kozos.GYOKER)
        b._utvonalak = lambda b_id, motivum=None: ['konkordancia/Peshitta.tsv']
        b._van = lambda b_id, motivum=None: True
        with self.assertRaises(BemenetHiba):
            HB.b73_peshitta(b)
        # aktív állapotnál a szakasz a szír fordítást még nem olvassa: kimondott hiba, nem néma mondat
        b = bemenet.Bemenet(kozos.GYOKER)
        b.jegyzek_sor('B73').allapot = 'aktiv'
        with self.assertRaises(BemenetHiba):
            HB.b73_peshitta(b)


class Mondatok(unittest.TestCase):
    """A „Mit mutat” cella mondatai, a két mintalapon nem álló ágakkal együtt (a régi `_egyesites_mondat`,
    `_visszhang_mondat_lxx`)."""

    @staticmethod
    def _szo(kod, kiejtes):
        b = bemenet.Bemenet(kozos.GYOKER)
        from lapgen.szoveg import idezet
        return Szo(Strong(kod), None, idezet(b.forrasszoveg('B12', 'kiejtes', kiejtes, kod)))

    def test_egyesites_agai(self):
        n = ny()
        a, b = self._szo('H0779', 'árar'), self._szo('H7043', 'kálal')
        vart = {
            HS.EgyesitesFajta.NEM_MERHETO_FORRAS: 'A Targum a láncban mindkét héber szót (árar és kálal) ugyanazzal a '
                                                  'szóval adja vissza; hogy máshol is így fordítja-e, ebből a forrásból '
                                                  'nem mérhető.',
            HS.EgyesitesFajta.NEM_MERHETO: 'A Targum mindkét héber szót (árar és kálal) ugyanazzal a szócsaláddal adja '
                                           'vissza; a láncon kívül nem mérhető.',
            HS.EgyesitesFajta.SZOKASOS: 'A Targum mindkét héber szót (árar és kálal) ugyanazzal a szócsaláddal adja '
                                        'vissza; ez a láncon kívül is így van (árar 85%, kálal 90%).',
            HS.EgyesitesFajta.RITKA: '**A Targum mindkét héber szót (árar és kálal) ugyanazzal a szócsaláddal adja '
                                     'vissza, a láncon kívül viszont nem így (árar 85%, kálal 90%): a láncban választott '
                                     'egység.**',
            HS.EgyesitesFajta.GYAKORI: 'A Targum mindkét héber szót (árar és kálal) ugyanazzal a szócsaláddal adja '
                                       'vissza; a láncon kívül gyakran, de nem kizárólag (árar 85%, kálal 90%).'}
        for fajta, mondat in vart.items():
            m = HS.Egyesites((HS.Forditas.TARGUM,), fajta, (a, b), True, (85, 90))
            self.assertEqual(szoveg(MD._mondat(n, m)), mondat)
        tv = HS.Egyesites((HS.Forditas.TARGUM, HS.Forditas.VULGATA), HS.EgyesitesFajta.NEM_MERHETO_FORRAS, (a, b),
                          False, ())
        self.assertTrue(szoveg(MD._mondat(n, tv)).startswith('A Targum és a Vulgata a láncban'))
        self.assertEqual(szoveg(MD._mondat(n, HS.Utalas(a))), 'L. az árar sorát.')

    def test_lxx_mondat_agai(self):
        n = ny()
        m = HS.LxxMondat(HS.LxxFajta.ELTERES, None, 2, 1, 3, None, False)
        self.assertEqual(szoveg(MD._mondat(n, m)), 'LXX: 2 versben más szó; egy versben nincs megfelelő szó; 3 '
                                                   'versben nincs ellenőrzött adat.')
        m = HS.LxxMondat(HS.LxxFajta.NINCS_ADAT, HS.Hiany.NINCS_KINYERES, 0, 0, 0, None, False)
        self.assertEqual(szoveg(MD._mondat(n, m)), 'A LXX: a megfelelő kinyerése még nem történt meg.')
        m = HS.LxxMondat(HS.LxxFajta.ALAPVONAL, None, 0, 0, 0, HS.Alapvonal(HS.Sav.RITKA, 20, 10, 2), True)
        self.assertEqual(szoveg(MD._mondat(n, m)), '**LXX: a láncon kívüli 10 versből csak 2 versben (20%) áll ez: a '
                                                   'láncban más szót választ, mint máshol.**')


if __name__ == '__main__':
    unittest.main(verbosity=1)
