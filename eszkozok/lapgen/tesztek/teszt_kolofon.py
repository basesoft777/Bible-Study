"""A Kolofon (S8d; DT-F218y).

A HAMART-001 mai lapjával való egyezést (az engedélysorokkal) a regresszió méri; itt független számlálással: a
forrástábla sorai pontosan a számozott szakaszok olvasásai a jegyzék `irodalom` oszlopa szerint (GK-07, DT901), a
származtatott tábla CC BY-os bemenetei saját soron (F212); a licencszöveg és a kötelező megjelölés a licencleltárból;
a „Negatív kritérium” sor hivatkozás a lap elejére (DT874, 9. tétel); a jóváhagyás-mondat munka módban a korábbi
változatot mondja, kiadás módban a kapu megáll (GK-27, T9); a közel-keleti és a Chain Lineage-mondat az állapotból jön
(GK-28). A táblákat a teszt maga olvassa (`split('\t')`), nem a generátor kódjával.
"""
import dataclasses
import datetime
import os
import unittest

import kozos
from lapgen import bemenet, fo, konfig
from lapgen.bemenet import alap as alap_be
from lapgen.bemenet import irodalom as irodalom_be
from lapgen.bemenet import kolofon as kolofon_be
from lapgen.bemenet.jegyzek import BemenetHiba, JegyzekSor
from lapgen.ertekek import IrodLicenc
from lapgen.megjelenites.md import kolofon as MD
from lapgen.megjelenites.md.iro import Lapiro, lap_szoveg
from lapgen.szamitas import kolofon as SZ
from lapgen.szoveg import MotivumId, SablonHiba, SablonSor, kiiras, sablon

HAMART, ISTENTISZT = 'HAMART-001', 'ISTENTISZT-001'
DATUM = datetime.date(2026, 11, 13)


def kiir(lathato):
    return kiiras(lathato).szoveg


def _tabla(rel):
    with open(os.path.join(kozos.GYOKER, *rel.split('/')), encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def _nevek(tipus):
    return {s['kulcs']: s['olvasoi_nev'] for s in _tabla('adat/olvasoi_nevtabla.tsv') if s['tipus'] == tipus}


class _Korny:
    def __init__(self, azonosito, mod=fo.Mod.MUNKA):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), mod


def _elozo(korny):
    """A számozott szakaszok (és alrészeik) olvasásai, ahogy a `fo.lap_keszit` a gyűjtő szakasznak átadja."""
    elozo = {}
    for leiro in fo.szakaszrend().mind():
        if leiro.szamit is None or leiro.gyujto or leiro.nezet != konfig.NEZET_TUDOMANYOS:
            continue
        with korny.b.figyel() as f:
            leiro.szamit(korny)
        if leiro.szamozott or leiro.alresz:
            elozo[leiro.azonosito] = frozenset(f)
    return elozo


def _lap(korny, modell, datum=DATUM):
    b = korny.b
    keret = fo.Keret(bemenet.nyelv(b), korny.motivum, fo.szakaszrend(), 'ts=2026-11-13', korny.mod, b, datum)
    iro = Lapiro()
    MD.megjelenit(iro, modell, keret, fo._forrasok(b, bemenet.b01_licencek(b), frozenset()))
    return lap_szoveg(iro.kesz())


class _Alap(unittest.TestCase):
    AZONOSITO = HAMART
    _cache = {}

    @classmethod
    def setUpClass(cls):
        if cls.AZONOSITO not in _Alap._cache:
            korny = _Korny(cls.AZONOSITO)
            elozo = _elozo(korny)
            _Alap._cache[cls.AZONOSITO] = (korny, elozo, SZ.szamit(korny, elozo))
        cls.korny, cls.elozo, cls.modell = _Alap._cache[cls.AZONOSITO]
        cls.unio = frozenset().union(*cls.elozo.values())
        cls.lap = _lap(cls.korny, cls.modell)


class Forrastabla(_Alap):
    def test_gk07_a_sorok_az_olvasasokbol(self):
        """GK-07 (DT901): a forrástábla nevei pontosan a számozott szakaszok olvasott bemeneteinek fájlnevei (a jegyzék
        `irodalom` oszlopa szerint), a származtatott tábla bemenetei (F212) és a külső források."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        szotar, kolofon, adat, kulso = (_nevek('irod_szotar'), _nevek('kolofon_szotar'), _nevek('irod_adat'),
                                        _nevek('irod_kulso'))

        def nevek(b_idk):
            ki = set()
            for b_id in b_idk:
                if jegyzek[b_id]['irodalom'] == '-':
                    continue
                for u in (x.strip() for x in jegyzek[b_id]['utvonal'].split(';')):
                    ki.add(kolofon[u] if u in szotar else adat[u])
            return ki
        vart = nevek(self.unio)
        for b_id, (jegyzekbeli, kulsok) in konfig.KOLOFON_SZARMAZTATOTT.items():
            if b_id in self.unio:
                vart |= nevek(jegyzekbeli) | {kulso[k] for k in kulsok}
        kapott = {s.nev.ertek: s for s in self.modell.forrasok}
        kapott_nevek = {(_nevek(s.nev_tipus)[k]) for k, s in kapott.items()}
        self.assertTrue(vart <= kapott_nevek, vart - kapott_nevek)
        self.assertTrue(kapott_nevek - vart <= set(kulso.values()), kapott_nevek - vart)
        # a MACULA (a BDB verstáblájának bemenete) saját soron áll (F212)
        self.assertIn(kulso['macula_heber'], kapott_nevek)

    def test_a_szakaszok_az_olvaso_szakaszok(self):
        """A „Szakasz” oszlop pontosan azok a szakaszok, amelyek a sor bemenetét olvasták (alrésznél a szülő)."""
        motivumtabla = [s for s in self.modell.forrasok if s.nev.ertek == 'adat/motivumok.tsv']
        self.assertEqual(len(motivumtabla), 1)
        vart = {a for a, olv in self.elozo.items() if 'B02' in olv}
        self.assertEqual(set(motivumtabla[0].szakaszok), vart)
        self.assertNotIn('3. Kizárt', self.lap)   # a 3. szakasznak nincs szelete: nem olvas

    def test_licenc_csak_a_licencleltarbol(self):
        """GK-07: a `licenc` alakú licenc a licencleltár címkéje szó szerint."""
        cimkek = {s['cimke'] for s in _tabla('adat/licencek.tsv')}
        for sor in self.modell.forrasok:
            for lic in sor.licencek:
                if lic.alak is IrodLicenc.LICENC:
                    self.assertIn(kiir(lic.cimke), cimkek)
        # a közlés DOI-ja a kiadási adatok egyetlen helyéről (a névtábla `kiadasi_adat` típusa, DT-F218y 1.)
        doi = _nevek('kiadasi_adat')['karoli_strong_doi']
        self.assertTrue(any(s.startswith('| Károli–Strong párosítás | CC BY 4.0, https://doi.org/%s |' % doi)
                            for s in self.lap.split('\n')))


class Megjeloles(_Alap):
    def test_a_megjelolesek_a_licencleltarbol(self):
        """A megjelölendő források a `konfig.KOLOFON_MEGJELOLES` kulcsai közül azok, amelyek bemenetét a lap
        olvasta; a nem saját mondatú megjelölés a licencleltár `kotelezo_megjeloles` mezőjének mondata, szó szerint."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        olvasott = {jegyzek[b]['licenc_kulcs'] for b in self.unio}
        mezo = {s['dataset']: s['kotelezo_megjeloles'] for s in _tabla('adat/licencek.tsv')}
        vart_sablon = [s for k, s in konfig.KOLOFON_MEGJELOLES if k in olvasott and s is not None]
        self.assertEqual([m.sablon for m in self.modell.megjelolesek if m.sablon], vart_sablon)
        for m in self.modell.megjelolesek:
            if m.sablon is None:
                self.assertTrue(any(m.szoveg is not None and kiir(m.szoveg) in mezo[k]
                                    for k, s in konfig.KOLOFON_MEGJELOLES if k in olvasott and s is None))
        self.assertNotIn('Mounce', self.lap)   # az új generátor a Mounce-szótárt nem olvassa
        self.assertIn('*LSJ forrás: Liddell-Scott-Jones', self.lap)


class Kriterium(_Alap):
    def test_ism_a_kolofon_nem_ismetli_a_kriteriumot(self):
        """DT-F218n, DT874 9. tétel: a „Negatív kritérium” sor a lap elejére hivatkozik, a kritériumot nem ismétli."""
        krit = [s['negativ_kriterium'] for s in _tabla('adat/motivumok.tsv') if s['id'] == HAMART][0]
        self.assertNotIn(krit[:60], self.lap)
        self.assertIn('| Negatív kritérium | a lap elején áll ([Mi tartozik ide, és mi nem](#mi-tartozik-ide)) |',
                      self.lap)


class Jovahagyas(_Alap):
    def test_gk27_munka_modban_a_korabbi_valtozat(self):
        """GK-27 (T9): munka módban a szerző a lap korábbi változatát hagyta jóvá, a legutóbbi átnézés (híján a
        legutóbbi kiadás) dátumával."""
        kiadasok = sorted((s for s in _tabla('adat/kiadasok.tsv') if s['id'] == HAMART), key=lambda s: int(s['kiadas']))
        atnezes = sorted(s['datum'] for s in _tabla('adat/lap_atnezesek.tsv')
                         if s['id'] == HAMART and s['ki'] == 'felhasználó')
        datum = (atnezes or [kiadasok[-1]['datum']])[-1]
        self.assertIn('; a szerző a lap korábbi változatát hagyta jóvá (%s). A többi szakasz' % datum, self.lap)
        self.assertNotIn('a szerző jóváhagyta', self.lap)
        self.assertIs(SZ.kapu(self.modell), self.modell)

    def test_gk27_kiadas_modban_a_kapu_megall(self):
        """GK-27 (T9, DT-F218y 2.): kiadás módban a kézi résű lap kapuja megáll (a `lap_commit` a 218c-ben)."""
        with self.assertRaises(BemenetHiba):
            SZ.kapu(dataclasses.replace(self.modell, kiadas=True))
        generalt = dataclasses.replace(self.modell, kiadas=True, szerzoseg=SZ.Szerzoseg.GENERALT, resek=())
        self.assertIs(SZ.kapu(generalt), generalt)

    def test_kiadasi_adatok(self):
        adatok = kolofon_be.b48_kiadasi_adatok(self.korny.b, self.korny.motivum)
        kiadasok = [s for s in _tabla('adat/kiadasok.tsv') if s['id'] == HAMART]
        self.assertEqual([k.szam for k in adatok.kiadasok], sorted(int(s['kiadas']) for s in kiadasok))
        javitasok = {s['datum'] for s in _tabla('adat/lap_javitasok.tsv')
                     if s['id'] == HAMART and s['jovahagyta'] == 'felhasználó' and s['datum']}
        self.assertEqual([d.strftime('%Y.%m.%d') for d in adatok.javitasok], sorted(javitasok))
        self.assertIn('vetette el (2026.11.11–13) |', self.lap)   # a dátumok tartománya (azonos hónap)
        self.assertIn('| Kiadás | %d |' % adatok.kiadasok[-1].szam, self.lap)


class Allapotmondat(_Alap):
    def test_gk28_kozel_keleti_csak_nem_vizsgalt_allapotban(self):
        """GK-28: a közel-keleti mondat csak „nem vizsgált” rétegállapotnál áll; más állapotnál a Kolofon megáll."""
        self.assertIn('összehasonlító réteg a munkában nincs', self.lap)
        b = bemenet.Bemenet(kozos.GYOKER)
        sor = b.jegyzek_sor('B75')
        b._jegyzek['B75'] = JegyzekSor(**dict({k: getattr(sor, k) for k in sor.__slots__}, allapot='aktiv'))
        with self.assertRaises(BemenetHiba):
            kolofon_be.b75_kozel_keleti_reteg(b)

    def test_gk28_chain_lineage_a_licencleltar_allapotabol(self):
        """GK-28: a Chain Lineage licencmondata a licencleltár állapotából (`tisztazatlan`) jön; tisztázott
        állapotnál a címke áll."""
        b = bemenet.Bemenet(kozos.GYOKER)
        k = {x.kulcs.ertek: x for x in irodalom_be.kulso_forrasok(b, MotivumId(HAMART), {'B39'})}
        self.assertIs(k['chain_lineage'].licenc, IrodLicenc.CHAIN_LINEAGE)
        eredeti = irodalom_be.b01_licencek

        def hamis(bb):
            lic = eredeti(bb)
            allapotok = dict(lic._allapotok, Chain_Lineage_Browser='tisztazott')
            return alap_be.Licencek(bb, lic._cimkek, allapotok, lic._megjelolesek)
        irodalom_be.b01_licencek = hamis
        try:
            k = {x.kulcs.ertek: x for x in irodalom_be.kulso_forrasok(b, MotivumId(HAMART), {'B39'})}
        finally:
            irodalom_be.b01_licencek = eredeti
        self.assertIs(k['chain_lineage'].licenc, IrodLicenc.LICENC)
        self.assertIsNotNone(k['chain_lineage'].cimke)


class Istentiszt(_Alap):
    AZONOSITO = ISTENTISZT

    def test_a_lap_elkeszul(self):
        self.assertIn('| Negatív kritérium | a lap elején áll', self.lap)
        self.assertIn('| ID | ISTENTISZT-001 |', self.lap)


class Datumforma(unittest.TestCase):
    def test_datum_pont_es_nap(self):
        sor = SablonSor('x', '{a}–{b}', 'a:datum(pont), b:datum(nap)')
        self.assertEqual(kiir(sablon(sor, a=datetime.date(2026, 11, 1), b=datetime.date(2026, 11, 3))),
                         '2026.11.01–03')

    def test_ismeretlen_datumforma(self):
        with self.assertRaises(SablonHiba):
            SablonSor('x', '{a}', 'a:datum(ev)')


if __name__ == '__main__':
    unittest.main()
