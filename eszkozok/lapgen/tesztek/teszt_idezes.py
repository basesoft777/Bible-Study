"""A 12. szakasz, „Irodalom és idézés” (S8c; DT-F218x).

A HAMART-001 mai lapjával való egyezést (az engedélysorokkal) a regresszió méri; itt a forrás-halmaz független
számlálással: a szótárak és az adatforrások fájljai pontosan a számozott szakaszok olvasásai a jegyzék `irodalom`
oszlopa szerint (GK-07), a licenc a licencleltár címkéje, a külső források a visszhang- és a tanútábla ellenőrzött
soraiból, a szakirodalom teljes hivatkozása; és a kimondott hibák (név nélküli fájl, ismeretlen `irodalom` érték).
A táblákat a teszt maga olvassa (`split('\t')`), nem a generátor kódjával.
"""
import os
import unittest

import kozos
from lapgen import bemenet, fo, konfig
from lapgen.bemenet import irodalom as irodalom_be
from lapgen.bemenet.nyelv import Nevtabla, b65_nevtabla
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.ertekek import IrodLicenc
from lapgen.megjelenites.md import idezes as MD
from lapgen.megjelenites.md.iro import Lapiro, lap_szoveg
from lapgen.szamitas import idezes as SZ
from lapgen.szoveg import MotivumId

HAMART, ISTENTISZT = 'HAMART-001', 'ISTENTISZT-001'
INFRASTRUKTURA = ('B01', 'B12', 'B13', 'B47', 'B51', 'B59', 'B63', 'B65', 'B66', 'B68', 'B76')
NEM_VIZSGALT = ('B73', 'B75')   # fájl nélküli, nem vizsgált forrás: a listán nem áll (SEMA 2.66)
KOLOFON_SAJAT = ('B48', 'B49', 'B50')   # a Kolofon saját metaadata (kiadás, lektor, közel-keleti határ; S8d)


def _tabla(rel):
    """Egy repó-tábla sorai szótárként (a megjegyzéssorok nélkül), `split('\t')`-tel."""
    with open(os.path.join(kozos.GYOKER, *rel.split('/')), encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


class _Korny:
    def __init__(self, azonosito):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA


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


class _Alap(unittest.TestCase):
    AZONOSITO = HAMART

    @classmethod
    def setUpClass(cls):
        cls.korny = _Korny(cls.AZONOSITO)
        cls.elozo = _elozo(cls.korny)
        cls.unio = frozenset().union(*cls.elozo.values())
        cls.modell = SZ.szamit(cls.korny, cls.elozo)


class Forrashalmaz(_Alap):
    def test_gk07_a_fajlok_az_olvasasokbol(self):
        """GK-07 (DT-F218x): a 12. szakasz fájljai pontosan a számozott szakaszok olvasott bemeneteinek fájljai,
        a jegyzék `irodalom` oszlopa szerint; a generátor infrastruktúrája nem áll köztük."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        vart = {u.strip() for b in self.unio if jegyzek[b]['irodalom'] != '-'
                for u in jegyzek[b]['utvonal'].split(';') if u.strip() != '-'}
        kapott = [f.rend for f in irodalom_be.irodalom_fajlok(self.korny.b, self.unio)]
        self.assertEqual(sorted(kapott), sorted(vart))
        self.assertEqual(len(kapott), len(set(kapott)))
        self.assertTrue(vart)
        self.assertFalse({jegyzek[b]['utvonal'] for b in INFRASTRUKTURA} & set(kapott))
        for b in INFRASTRUKTURA + NEM_VIZSGALT:
            self.assertEqual(jegyzek[b]['irodalom'], '-', b)
        for b, sor in jegyzek.items():
            if sor['irodalom'] == '-':
                self.assertIn(b, INFRASTRUKTURA + NEM_VIZSGALT + KOLOFON_SAJAT,
                              'a `-` csak az infrastruktúráé, a nem vizsgált forrásé és a Kolofon metaadatáé')
        for b in ('B14', 'B15', 'B18'):
            self.assertEqual(jegyzek[b]['irodalom'], 'forditas', b)

    def test_gk07_a_licenc_a_leltarbol(self):
        """GK-07: a licencleltár alakú licenc a jegyzék licenckulcsának leltárbeli címkéje."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        cimke = {s['dataset']: s['cimke'] for s in _tabla('adat/licencek.tsv')}
        for f in irodalom_be.irodalom_fajlok(self.korny.b, self.unio):
            self.assertEqual(f.cimke.ertek, cimke[jegyzek[f.b_id]['licenc_kulcs']], f.rend)
            self.assertEqual(f.licenc.value, jegyzek[f.b_id]['irodalom'], f.rend)

    def test_sorok_egyszer_es_rendben(self):
        """A szótárak a teljes nevük rendjében, mindegyik egyszer; az adatforrások neve egyszer áll."""
        t = b65_nevtabla(self.korny.b)
        szotar = [t.nyers_nevek('irod_szotar')[s.nev.ertek] for s in self.modell.szotarak]
        self.assertEqual(szotar, sorted(set(szotar)))
        adat = [t.nyers_nevek('irod_kulso' if a.kulso else 'irod_adat')[a.nev.ertek] for a in self.modell.adatforrasok]
        self.assertEqual(len(adat), len(set(adat)))
        for s in self.modell.szotarak:
            nevek = [t.nyers_nevek('irod_szotar_forras')[f.ertek] for f in s.forrasok]
            self.assertEqual(len(nevek), len(set(nevek)))


class KulsoForrasok(unittest.TestCase):
    def _vart(self, azonosito):
        okori = {s['forras'] for s in _tabla('adat/visszhang_megfelelok.tsv')
                 if s['motivum'] == azonosito and s['ellenorzes'].strip() and s['forras'] == 'vulgata'}
        tanuk = {s['forras'] for s in _tabla('adat/visszhang_tanuk.tsv')
                 if s['motivum'] == azonosito and s['ellenorzes'].strip()}
        return okori | tanuk

    def test_a_tablak_ellenorzott_soraibol(self):
        """A külső források (Vulgata, a tanúk forrásai) a két tábla ellenőrzött soraiból, mindkét mintalapon."""
        for azonosito in (HAMART, ISTENTISZT):
            b = bemenet.Bemenet(kozos.GYOKER)
            kapott = {k.kulcs.ertek for k in irodalom_be.kulso_forrasok(b, MotivumId(azonosito), {'B38', 'B39'})}
            self.assertEqual(kapott, self._vart(azonosito), azonosito)
            self.assertTrue(kapott)

    def test_csak_az_olvasott_tablabol(self):
        """Ha a tábla nem áll a szakaszok olvasásai között, a forrásai sem állnak a listán."""
        b = bemenet.Bemenet(kozos.GYOKER)
        self.assertEqual(irodalom_be.kulso_forrasok(b, MotivumId(HAMART), set()), [])

    def test_chain_lineage_licence_a_dontott_mondat(self):
        b = bemenet.Bemenet(kozos.GYOKER)
        k = {k.kulcs.ertek: k for k in irodalom_be.kulso_forrasok(b, MotivumId(HAMART), {'B39'})}
        self.assertIs(k['chain_lineage'].licenc, IrodLicenc.CHAIN_LINEAGE)
        self.assertIsNone(k['chain_lineage'].cimke)


class Szakirodalom(_Alap):
    def test_a_szerzos_sor_teljes_hivatkozasa(self):
        vart = [s for s in _tabla('adat/vitatott_forrasok.tsv')
                if s['motivum'] == HAMART and s['ellenorzes'].strip() and s['szerzo'].strip()]
        self.assertEqual(len(self.modell.szakirodalom), len(vart))
        iro = Lapiro()
        b = self.korny.b
        keret = fo.Keret(bemenet.nyelv(b), MotivumId(HAMART), fo.szakaszrend(), 'ts=2026-11-13', fo.Mod.MUNKA, b)
        MD.megjelenit(iro, self.modell, keret, fo._forrasok(b, bemenet.b01_licencek(b), frozenset()))
        lap = lap_szoveg(iro.kesz())
        for s in vart:
            self.assertIn('- %s, %s: *%s*. %s. DOI: %s' % (s['szerzo'], s['ev'], s['cim'], s['megjelenes'], s['doi']), lap)
        self.assertIn('[Kolofon](#kolofon)', lap)


class SzakirodalomNelkul(_Alap):
    AZONOSITO = ISTENTISZT

    def test_nincs_szakirodalom_blokk(self):
        self.assertEqual(self.modell.szakirodalom, ())


class KimondottHibak(unittest.TestCase):
    def test_nev_nelkuli_fajl_megall(self):
        """GK-23: a listázandó fájlnak a névtáblában pontosan egy neve legyen; híján a generálás megáll."""
        eredeti = irodalom_be.b65_nevtabla

        def hamis(b):
            t = eredeti(b)
            return Nevtabla({k: v for k, v in t._nevek.items()
                                      if k != ('irod_adat', 'adat/motivumok.tsv')},
                                     {k: v for k, v in t._nyers.items() if k != ('irod_adat', 'adat/motivumok.tsv')})
        irodalom_be.b65_nevtabla = hamis
        try:
            with self.assertRaises(BemenetHiba):
                irodalom_be.irodalom_fajlok(bemenet.Bemenet(kozos.GYOKER), {'B02'})
        finally:
            irodalom_be.b65_nevtabla = eredeti

    def test_ismeretlen_irodalom_ertek(self):
        repo = kozos.alap_minirepo(jegyzek_sorok=[
            ('B99', 'adat/x.tsv', 'x', 'nem', '-', '-', 'aktiv', 'projekt_adat', '-', 'rossz', 'm')])
        try:
            with self.assertRaises(BemenetHiba):
                bemenet.Bemenet(repo.gyoker)
        finally:
            repo.torol()


if __name__ == '__main__':
    unittest.main()
