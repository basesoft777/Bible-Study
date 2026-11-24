"""A „6. Kereszthivatkozások” szakasz és a Minősítés (S5): a modell számai a valós adaton, GK-A1, HN-10, a forrás-mező
szerkezete, az indoklás kapuja és a címke-ismétlés szabálya.

A HAMART-001 mai lapjának 6. szakasza: a motívum 49 helyéből 25 ad utalást (összesen 120); 6 hely több versre terjed;
5 hely 8 Károli-utalása nem megerősített. A Minősítés: 5 pár, 6 érintett hely, 99 vizsgált hely (mind elutasítva).
"""
import datetime
import unittest

import kozos
from kozos import alap_minirepo
from lapgen import bemenet, fo
from lapgen.bemenet import kereszthiv as KB
from lapgen.bemenet.nyelv import ok_cellaalakok
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import kereszthiv as KH
from lapgen.szoveg import MotivumId

_MODELL, _LAP = {}, {}
_DATUM = datetime.date(2026, 11, 13)


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


def modell(azonosito):
    if azonosito not in _MODELL:
        _MODELL[azonosito] = KH.szamit(_Korny(azonosito))
    return _MODELL[azonosito]


def szakasz_sorai(azonosito):
    """A kész lap 6. szakaszának sorai (a címsortól a 7. szakaszig) KeszSor alakban."""
    if azonosito not in _LAP:
        lap = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=_DATUM).nezetek['TUDOMANYOS']
        eleje = next(i for i, s in enumerate(lap) if s.szoveg.startswith('## ') and 'Kereszthivatkozások' in s.szoveg)
        vege = next((i for i in range(eleje + 1, len(lap)) if lap[i].szoveg.startswith('## ')), len(lap))
        _LAP[azonosito] = lap[eleje:vege]
    return _LAP[azonosito]


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


class Szamok(unittest.TestCase):
    def test_a_hamart_szamai_a_regi_lappal_egyeznek(self):
        m = modell('HAMART-001')
        self.assertEqual((m.n, len(m.helyek), m.osszes), (49, 25, 120))
        self.assertEqual([h.kod for h in m.nem_vizsgalhato],
                         ['1Móz 4:10-11', 'Ézs 24:5-6', 'Hós 4:1-3', 'Sof 1:2-3', 'Gal 3:13-14', 'Zsid 6:7-8'])
        self.assertEqual([h.kod for h, _db in m.kihagyott], ['Jer 6:7', 'Jer 51:46', 'Ez 12:19', 'Mik 6:12', 'Sof 1:9'])
        self.assertEqual((len(m.kihagyott), sum(db for _h, db in m.kihagyott)), (5, 8))
        mi = m.minosites
        self.assertEqual((len(mi.parok), mi.erintett, mi.n, len(mi.jeloltek)), (5, 6, 49, 99))
        self.assertEqual(mi.dontesek, ((KH.Dontes.ELUTASITVA, 99),))
        KH.kapu(m)

    def test_az_istentiszt_szamai(self):
        m = modell('ISTENTISZT-001')
        self.assertEqual((m.n, len(m.helyek), m.osszes), (20, 8, 19))
        mi = m.minosites
        self.assertEqual((len(mi.parok), mi.erintett, len(mi.jeloltek), mi.fok), (9, 7, 61, KH.MegerositesFok.KOZEPES))
        KH.kapu(m)

    def test_a_tsk_utalasok_csokkeno_szavazatszam_szerint_allnak(self):
        for h in modell('HAMART-001').helyek:
            tsk = [u.szavazat for u in h.utalasok if u.gyujtemeny is KH.Gyujtemeny.TSK]
            self.assertEqual(tsk, sorted(tsk, reverse=True), h.igehely.kod)
            self.assertTrue(all(sz >= KH.konfig.TSK_SZAVAZAT_KUSZOB for sz in tsk))

    def test_a_kapu_megfogja_a_nem_egyezo_osszeget(self):
        import dataclasses
        m = modell('HAMART-001')
        with self.assertRaises(KH.KapuHiba):
            KH.kapu(dataclasses.replace(m, osszes=m.osszes + 1))


class KarolKhSzuro(unittest.TestCase):
    def test_a_b43_a_regi_hozzaferesi_ponttal_egyezik(self):
        """A B43/B72 szűrése (a megerősített Károli-KH utalások sorrendje és a nem megerősített sorok száma) a régi
        `karoli_kh_szuro.szures` eredményével egyezik a két mintalap minden versén (a 8. ellenőrzés E9 tétele)."""
        import karoli_kh_szuro as KHS
        b = bemenet.Bemenet(kozos.GYOKER)
        konyvek = bemenet.b63_konyvek(b)
        for azonosito in kozos.MINTALAPOK:
            for sor in bemenet.b03_elofordulasok(b, MotivumId(azonosito)):
                step = konyvek.step_vers(sor.igehely)
                if step is None:
                    continue
                uj, elvetett = KB.b43_karoli_kh(b, sor.igehely)
                jo, rossz = KHS.szures(step)
                regi = [r_.replace(',', ':', 1) if ':' not in r_ else r_ for r_ in
                        (KHS.hu_megjelenites(r) for r in jo)]
                self.assertEqual([u.cel.kod for u in uj], regi, (azonosito, step))
                self.assertEqual(elvetett, rossz, (azonosito, step))


class GkA1(unittest.TestCase):
    def test_gk_a1_a_versenkent_nem_vizsgalhato_hely_egyszer_all(self):
        """GK-A1: minden igehely legfeljebb egyszer szerepel a 6. szakaszban és a hatókör-jegyzetben együtt; a lista az
        adatból jön (a modell `nem_vizsgalhato` mezője), nem szövegmásolatból."""
        for azonosito in kozos.MINTALAPOK:
            m = modell(azonosito)
            nem = [h.kod for h in m.nem_vizsgalhato]
            self.assertEqual(len(nem), len(set(nem)))
            self.assertFalse(set(nem) & {h.igehely.kod for h in m.helyek})
            szoveg = '\n'.join(lathato(s) for s in szakasz_sorai(azonosito))
            for kod in nem:
                self.assertEqual(szoveg.count(kod), 1, (azonosito, kod))


class Hn10(unittest.TestCase):
    def test_hn10_a_forrasmegjeloles_a_valoban_olvasott_javitott_tablat_nevezi(self):
        """HN-10: a 6. szakasz blokkfejléce és a Minősítés rés-jelölője a javított Károli-KH táblát is nevezi (a valódi
        olvasásból); a látható szövegben fájlnév nem áll."""
        sorok = szakasz_sorai('HAMART-001')
        fej = next(s.szoveg for s in sorok if 'GENERÁLT-KEZDET' in s.szoveg)
        res = next(s.szoveg for s in sorok if 'GENERÁLT-RÉS: minosites' in s.szoveg)
        for jelolo in (fej, res):
            self.assertIn('konkordancia/Karoli_KH_javitott.tsv', jelolo)
            self.assertIn('konkordancia/TSK_kereszthivatkozasok.tsv', jelolo)
        for s in sorok:
            self.assertNotIn('.tsv', lathato(s))


class Ajanlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.konyvek = bemenet.b63_konyvek(bemenet.Bemenet(kozos.GYOKER))

    def a(self, fo_):
        return KB._ajanlas(fo_, self.konyvek)

    def test_tobb_forrasvers_es_szavazat_tartomany(self):
        a = self.a('TSK 1Móz 4:11, 4:12 (2-4)')
        self.assertEqual([h.kod for h in a.forrasok], ['1Móz 4:11', '1Móz 4:12'])
        self.assertEqual(a.szavazatok, ((2, 4),))

    def test_karoli_is_es_szavazatlista(self):
        a = self.a('TSK 1Móz 6:5 (25); Károli-KH is')
        self.assertTrue(a.karoli_is)
        self.assertEqual(self.a('TSK 1Móz 6:13 (6, 4, 2)').szavazatok, ((6, None), (4, None), (2, None)))

    def test_irany_talalat_es_karoli(self):
        a = self.a('TSK 1Krón 16:8 → Zsolt 105:15 (22)')
        self.assertEqual((a.forrasok[0].kod, a.cel.kod, a.szavazatok), ('1Krón 16:8', 'Zsolt 105:15', ((22, None),)))
        self.assertEqual(self.a('TSK Zak 13:9 (46 találat)').talalat, 46)
        self.assertIs(self.a('Károli-KH Ézs 12:4').fajta, KB.AjanlasFajta.KAROLI)
        self.assertIs(self.a('TSK/Károli-KH ApCsel 9:14').fajta, KB.AjanlasFajta.TSK_KAROLI)

    def test_a_forrasalak_a_tabla_rovidítesere_csereldik(self):
        # F241.5b (D13 (d), N195): a döntésnapló „Zef” alakja a lapon „Sof” (a normalizáló tábla Forrás-alakok oszlopa)
        self.assertEqual(self.a('Károli-KH Zef 3:9').forrasok[0].kod, 'Sof 3:9')
        with self.assertRaises(bemenet.BemenetHiba):
            self.a('Károli-KH Xyz 3:9')

    def test_a_szokatlan_szavazatalak_megall(self):
        with self.assertRaises(bemenet.BemenetHiba):
            self.a('TSK 1Móz 6:5 (2 - 4)')

    def test_az_ismeretlen_forrasforma_megall(self):
        with self.assertRaises(bemenet.BemenetHiba):
            self.a('kollokacio H0779+H0127')


class Indoklas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = bemenet.Bemenet(kozos.GYOKER)

    def test_a_motivum_es_a_strong_hivatkozas_szerkezet(self):
        d = KB._indok(self.b, 'A „x” motívum ([ID: TEREMT-002]) tagja; a rokon H6089 עֶצֶב (ecev) szót', 'Jer 4:23')
        self.assertEqual([x.motivum.kod for x in d if x.motivum is not None], ['TEREMT-002'])
        strong = [x for x in d if x.strong is not None]
        self.assertEqual([(x.strong.kod, x.kezi.ertek) for x in strong], [('H6089', 'עֶצֶב')])

    def test_a_nem_olvasoi_szoveg_megall_nem_tisztit(self):
        for szoveg in ('Antropológiai "általánosítás"', 'DT478: ok', 'a Strong-keresés szerint', 'cella | határ',
                       'forras=valami.md'):
            with self.assertRaises(bemenet.BemenetHiba, msg=szoveg):
                KB._indok(self.b, szoveg, 'Jer 4:23')


class CimkeIsmetles(unittest.TestCase):
    def test_hn02_a_cimke_nem_ismetlodik(self):
        """HN-02: „A formula nincs a versben: Nincs meg a formula a versben…” — a cellában csak az indoklás áll."""
        self.assertTrue(KB.cimke_ismetles('a formula nincs a versben',
                                          'Nincs meg a formula a versben: sem az ἐπικαλέω (epikaleó) nem áll benne.'))
        self.assertFalse(KB.cimke_ismetles('egy másik motívum tárgya',
                                           'A szív romlottsága a „jécer — a szív romlott hajlama” motívum tárgya, amely önálló tétel'))

    def test_a_lapon_nincs_cimke_ismetles(self):
        for azonosito in kozos.MINTALAPOK:
            for s in szakasz_sorai(azonosito):
                self.assertNotIn('A formula nincs a versben: Nincs meg a formula', lathato(s))


class OkCella(unittest.TestCase):
    @staticmethod
    def _repo(nevek):
        return alap_minirepo(nevek=nevek, jegyzek_sorok=[
            ('B56', 'adat/elutasitasi_okok.tsv', 'okok', 'igen', '-', '-', 'aktiv', '-', '-', 'manual')], tovabbi={
            'adat/elutasitasi_okok.tsv': kozos.tsv(('sorrend', 'id', 'minta', 'cimke', 'megjegyzes'),
                                                   ('1', '*', 'x', 'egy másik motívum tárgya (összesítő sor)', ''))})

    def test_a_cellakezdo_alak_csak_a_kezdobetuben_terhet_el(self):
        for nevek, jo in (([('ok_cella', 'egy másik motívum tárgya', 'Egy másik motívum tárgya', 'x')], True),
                          ([('ok_cella', 'egy másik motívum tárgya', 'Más motívum tárgya', 'x')], False),
                          ([('ok_cella', 'nem létező címke', 'Nem létező címke', 'x')], False)):   # árva sor
            repo = self._repo(nevek)
            try:
                if jo:
                    self.assertEqual(ok_cellaalakok(bemenet.Bemenet(repo.gyoker))['egy másik motívum tárgya'].ertek,
                                     'Egy másik motívum tárgya')
                else:
                    with self.assertRaises(bemenet.BemenetHiba, msg=nevek):
                        ok_cellaalakok(bemenet.Bemenet(repo.gyoker))
            finally:
                repo.torol()


if __name__ == '__main__':
    unittest.main()
