"""A „7. Kapcsolatok”, az Alátámasztás és a „8. Kapcsolódó motívumok” szakasz (S6): a modell számai a valós adaton,
a kapuk, a záró döntés-hivatkozás leválasztása, a következtetés ágai és a gráf szerkezete.

A HAMART-001 mai lapjának 7. szakasza: 56 kapcsolat 42 helyet köt össze (43 párhuzam, 7 kontraszt, 6 variáns; 26
magas, 30 közepes); az Alátámasztás 44 sora; a 8. szakasz 1 motívumközi kapcsolata és 1 döntésre váró jelölt.
"""
import dataclasses
import datetime
import unittest

import kozos
from lapgen import bemenet, fo
from lapgen.bemenet import kapcsolat as KB
from lapgen.ertekek import KapcsolatBiztossag, KapcsolatSzerkezet, KapcsolatTipus, Megbizhatosag
from lapgen.megjelenites.md import kapcsolatok as MD
from lapgen.megjelenites.md.iro import JELOLES, MEGJEGYZES, Lapiro
from lapgen.szamitas import kapcsolatok as KS
from lapgen.szoveg import MotivumId, kiiras

_MODELL, _LAP = {}, {}
_DATUM = datetime.date(2026, 11, 13)


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


def modell(azonosito, kapcsolodo=False):
    kulcs = (azonosito, kapcsolodo)
    if kulcs not in _MODELL:
        korny = _Korny(azonosito)
        _MODELL[kulcs] = KS.szamit_kapcsolodo(korny) if kapcsolodo else KS.szamit(korny)
    return _MODELL[kulcs]


def ny():
    return bemenet.nyelv(bemenet.Bemenet(kozos.GYOKER))


def szoveg(lathato):
    return kiiras(lathato).szoveg


def szakasz_sorai(azonosito):
    """A kész lap 7. és 8. szakaszának sorai (a 7. címsortól a 9. szakaszig)."""
    if azonosito not in _LAP:
        lap = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=_DATUM).nezetek['TUDOMANYOS']
        eleje = next(i for i, s in enumerate(lap) if s.szoveg.startswith('## ') and 'Kapcsolatok' in s.szoveg)
        kapcsolodo = next(i for i in range(eleje + 1, len(lap)) if lap[i].szoveg.startswith('## '))
        vege = next((i for i in range(kapcsolodo + 1, len(lap)) if lap[i].szoveg.startswith('## ')), len(lap))
        _LAP[azonosito] = lap[eleje:vege]
    return _LAP[azonosito]


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


class Szamok(unittest.TestCase):
    def test_a_hamart_szamai_a_regi_lappal_egyeznek(self):
        m = modell('HAMART-001')
        self.assertEqual((m.n, len(m.csomopontok), m.magas, m.kozepes, m.alacsony), (56, 42, 26, 30, 0))
        self.assertEqual(m.tipusok, ((KapcsolatTipus.PARHUZAM, 43), (KapcsolatTipus.KONTRASZT, 7),
                                     (KapcsolatTipus.VARIANS, 6)))
        self.assertEqual((m.szerkezet, m.biztossag),
                         (KapcsolatSzerkezet.TULNYOMO_PARHUZAM, KapcsolatBiztossag.KOZEPES_TOBBSEG))
        a = m.alatamasztas
        self.assertEqual((len(a.sorok), len(a.nelkul), len(a.megjegyzesek)), (44, 0, 1))
        self.assertEqual(sum(len(s.parok) for s in a.sorok), 56)
        KS.kapu(m)

    def test_az_istentiszt_szamai(self):
        m = modell('ISTENTISZT-001')
        self.assertEqual((m.n, len(m.csomopontok), m.magas, m.kozepes), (16, 20, 13, 3))
        self.assertEqual(m.tipusok, ((KapcsolatTipus.PARHUZAM, 13), (KapcsolatTipus.BETELJESEDES, 2),
                                     (KapcsolatTipus.VARIANS, 1)))
        self.assertEqual((m.szerkezet, m.biztossag), (KapcsolatSzerkezet.TULNYOMO_PARHUZAM, KapcsolatBiztossag.TOBBSEG))
        self.assertEqual([(a.kod, b.kod) for a, b in m.alatamasztas.nelkul], [('2Móz 33:19', '2Móz 34:5')])
        KS.kapu(m)

    def test_a_csomopontok_kanoni_sorrendben_allnak(self):
        m = modell('HAMART-001')
        self.assertEqual([h.kod for h in m.csomopontok[:3]], ['1Móz 3:14', '1Móz 3:16', '1Móz 3:17'])
        self.assertEqual([h.kod for h in m.csomopontok[-3:]], ['Jel 11:18', 'Jel 19:2', 'Jel 22:3'])

    def test_a_kapcsolodo_szamai(self):
        h = modell('HAMART-001', kapcsolodo=True)
        self.assertEqual([(r.masik.kod, r.itt.kod, r.ott.kod) for r in h.sorok],
                         [('ISTENTISZT-001', '1Móz 12:3', '1Móz 12:8')])
        self.assertEqual(([(m.kod, n) for m, n in h.nyitott], h.csak_szomszedos), ([('ISTENTISZT-001', 1)], True))
        self.assertEqual(h.dontes_datum, datetime.date(2026, 10, 19))
        i = modell('ISTENTISZT-001', kapcsolodo=True)
        self.assertEqual([(m.kod, n) for m, n in i.motivumok], [('ALVIL-001', 2), ('HAMART-001', 1)])
        self.assertEqual(i.nyitott_ossz, 3)
        KS.kapu_kapcsolodo(h)
        KS.kapu_kapcsolodo(i)


class Kapu(unittest.TestCase):
    def test_a_kapu_megfogja_a_nem_egyezo_szamot(self):
        m = modell('HAMART-001')
        with self.assertRaises(KS.KapuHiba):
            KS.kapu(dataclasses.replace(m, magas=m.magas + 1))
        with self.assertRaises(KS.KapuHiba):
            KS.kapu(dataclasses.replace(m, elek=m.elek[1:]))

    def test_a_kapu_megfogja_a_hianyzo_alatamasztast(self):
        m = modell('HAMART-001')
        a = dataclasses.replace(m.alatamasztas, sorok=m.alatamasztas.sorok[1:])
        with self.assertRaises(KS.KapuHiba):
            KS.kapu(dataclasses.replace(m, alatamasztas=a))

    def test_a_kapcsolodo_kapuja(self):
        h = modell('HAMART-001', kapcsolodo=True)
        with self.assertRaises(KS.KapuHiba):
            KS.kapu_kapcsolodo(dataclasses.replace(h, nyitott_ossz=h.nyitott_ossz + 1))


class ZaroDontes(unittest.TestCase):
    def test_a_b46_atmeneti_levalasztasa_csak_a_rogzitett_alak(self):
        """N-F218r (átmenet): a B46-on csak a záró „Döntés: DT<n> (felhasználó, dátum).” válik le; más alak marad, és
        a benne álló döntésszámon a kapu megáll."""
        self.assertEqual(
            KB._mk_zaro_dontes_nelkul('A közös fejezet nem bizonyít. Döntés: DT280 (felhasználó, 2026-10-20).'),
            'A közös fejezet nem bizonyít.')
        for szoveg in ('A hely a lánc része (DT479, a felhasználó, 2026-11-01: „Igen, (b)”)',
                       'A hely a lánc része. Döntés: DT280 (a lánc szava miatt).'):
            self.assertEqual(KB._mk_zaro_dontes_nelkul(szoveg), szoveg)
            self.assertIsNotNone(KB.nem_olvasoi(szoveg))

    def test_a_b45_kezi_szovegeben_nincs_dontes_hivatkozas(self):
        """DT-F218t (a felhasználó döntése): a B45 indoklásának kézi részében döntés-hivatkozás nem áll (az adat a
        végleges alak; a döntés a sor proveniencia-részében). A kapu a hivatkozáson megállna: a két mintalap sorai
        ezért a bemeneten át sem jutnának, ha maradt volna."""
        b = bemenet.Bemenet(kozos.GYOKER)
        for azonosito in kozos.MINTALAPOK:
            for k in KB.b45_kapcsolatok(b, MotivumId(azonosito)):
                if k.indok is not None:
                    self.assertIsNone(KB.nem_olvasoi(k.indok.ertek), (azonosito, k.forras.kod))
        self.assertFalse(hasattr(KB, '_zaro_dontes_nelkul'))


class Megjelenites(unittest.TestCase):
    def test_a_kovetkeztetes_agai(self):
        m, n = modell('HAMART-001'), ny()
        esetek = [
            (dict(szerkezet=KapcsolatSzerkezet.LANC), 'beteljesedésbe tartó láncot'),
            (dict(szerkezet=KapcsolatSzerkezet.TULNYOMO, fo_tipus=KapcsolatTipus.KONTRASZT),
             'túlnyomórészt kontraszt jellegűek'),
            (dict(szerkezet=KapcsolatSzerkezet.TOBBFELE), 'egyik sem uralkodó'),
            (dict(biztossag=KapcsolatBiztossag.SZINTE_MIND), 'szinte mind biztosak'),
            (dict(biztossag=KapcsolatBiztossag.KEVES), 'kevesebb mint fele magas'),
            (dict(magas=56, kozepes=0, alacsony=0), '56 magas bizonyosságú.'),
            (dict(magas=20, kozepes=30, alacsony=6), '20 magas, 30 közepes, 6 alacsony bizonyosságú.'),
        ]
        for valtozas, vart in esetek:
            self.assertIn(vart, szoveg(MD.olvasoi(n, dataclasses.replace(m, **valtozas))), valtozas)
        self.assertIn('43 párhuzam, 7 kontraszt, 6 variáns', szoveg(MD.olvasoi(n, m)))

    def test_ures_ag_sablonjai(self):
        """A kapcsolat nélküli motívum ágai (a két mintalapon nem futnak) kimondott mondatot adnak."""
        n = ny()
        self.assertIn('még nincs ilyen', szoveg(MD.olvasoi(n, dataclasses.replace(modell('HAMART-001'), n=0))))
        h = modell('HAMART-001', kapcsolodo=True)
        self.assertIn('1 döntésre vár', szoveg(MD.olvasoi_kapcsolodo(n, dataclasses.replace(h, sorok=()))))
        self.assertTrue(szoveg(MD.olvasoi_kapcsolodo(n, dataclasses.replace(h, sorok=(), nyitott_ossz=0)))
                        .endswith('más motívummal.'))

    def test_a_graf_csomopontjai_es_elei(self):
        sorok = [s.szoveg for s in szakasz_sorai('HAMART-001')]
        eleje, vege = sorok.index('```mermaid'), sorok.index('```')
        graf = sorok[eleje + 2:vege]
        self.assertEqual(sum(1 for s in graf if s.endswith('"]')), 42)
        self.assertEqual(sum(1 for s in graf if ' -->|' in s), 56)
        self.assertIn('    n3 -->|Kontraszt| n42', graf)

    def test_a_link_a_masik_motivum_lapjara_mutat_a_cel_jeloles(self):
        sor = next(s for s in szakasz_sorai('HAMART-001') if s.szoveg.startswith('| [ISTENTISZT-001]'))
        self.assertTrue(sor.szoveg.startswith('| [ISTENTISZT-001](ISTENTISZT-001_TUDOMANYOS.md) | 1Móz 12:3 |'))
        szoveg_resz = ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f not in (MEGJEGYZES, JELOLES))
        self.assertNotIn('TUDOMANYOS', szoveg_resz)

    def test_a_lathato_szovegben_nincs_dontesszam(self):
        for azonosito in kozos.MINTALAPOK:
            for s in szakasz_sorai(azonosito):
                self.assertNotRegex(lathato(s), r'\bDT\d+', (azonosito, s.szoveg[:80]))


class Hozzaferes(unittest.TestCase):
    def test_gk01_a_b04_egyetlen_hozzaferesi_pontja(self):
        """GK-01: a döntésnaplót (B04) csak a `bemenet/dontes.py` nyitja (`jeloltnaplo_tabla`); a többi olvasó ezt
        hívja (a 9. ellenőrzés E4 tétele)."""
        nyitok = [rel for rel in kozos.kodfajlok('bemenet') if "_tabla('B04'" in kozos.forras(rel)]
        self.assertEqual([r.replace('\\', '/') for r in nyitok], ['bemenet/dontes.py'])

    def test_a_kapcsolodo_kapu_megfogja_az_ismetlodo_part(self):
        h = modell('HAMART-001', kapcsolodo=True)
        with self.assertRaises(KS.KapuHiba):
            KS.kapu_kapcsolodo(dataclasses.replace(h, sorok=h.sorok + h.sorok,
                                                   motivumok=((h.sorok[0].masik, 2),)))


class Iro(unittest.TestCase):
    def test_a_link_jelolo_csak_motivumot_es_ismert_nezetet_fogad(self):
        from lapgen.megjelenites.md.iro import lap_link_zar
        from lapgen.szoveg import SzovegHiba
        with self.assertRaises(SzovegHiba):
            lap_link_zar('ISTENTISZT-001', 'TUDOMANYOS')
        with self.assertRaises(SzovegHiba):
            lap_link_zar(MotivumId('ISTENTISZT-001'), 'masik')
        iro = Lapiro()
        iro.sor(lap_link_zar(MotivumId('ISTENTISZT-001'), 'TUDOMANYOS'))
        self.assertEqual(iro.kesz()[0].szoveg, '](ISTENTISZT-001_TUDOMANYOS.md)')


if __name__ == '__main__':
    unittest.main()
