"""Tesztváz (F218.3): a brief 7. pontjának még meg nem írt követelményei, név + docstring + `skip` alakban.

A teszt törzse azzal a szelettel íródik meg, amelyik a követelményt teljesíti; akkor a függvény innen a szelet
tesztfájljába költözik. A `skip` oka megnevezi a szeletet. A 218b/218c-re tartozó követelmények nincsenek itt.
"""
import datetime
import re
import unittest

import kozos
from kozos import MINTALAPOK
from lapgen import fo
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szoveg import MotivumId

S2, S3, S4, S5, S6, S7, S8, S9 = ('S2 (F218.5)', 'S3 (F218.6)', 'S4 (F218.7)', 'S5 (F218.8)', 'S6 (F218.9)',
                                  'S7 (F218.10)', 'S8 (F218.11)', 'S9 (F218.12)')


# A hibanapló példányainak szövegmintái (brief 7.3): HN → [(minta, lapszöveg-részlet a hibás lapról)]. A részlet a
# mintára BUKÁS-t ad (a minta megfogja); az új lap látható szövegén az elvárt találatszám 0. A minták forrása az
# alapmérés táblája (`naplok/F218_jelentes.md` „F218.1 — alapmérés”).
HN_MINTAK = {
    'HN-02': [(r'A formula nincs a versben: Nincs meg a formula',
               'A formula nincs a versben: Nincs meg a formula a versben, a szó önállóan áll')],
    'HN-03': [(r'\((?:a|az|A|Az) [^()\n]*(?:BDB|Thayer|TBESG|TBESH|STEPBible|MCGED|SDBH|LSJ|SECE)[^()\n]*szótár[^()\n]*\)',
               'a szó jelentése (a BDB-szótár szerint) a megművelt föld')],
    'HN-04': [(r'hivatkozas_kezi|negativ_kriterium|szerkesztő-chat|\bkollokacio\b',
               'a javítás forrása: hivatkozas_kezi,; kollokacio … szerkesztő-chat … negativ_kriterium')],
    'HN-05': [(r'felhasználó|orkesztrátor', 'a felhasználó döntése szerint'),
              (r'felhasználó|orkesztrátor', 'az orkesztrátor jóváhagyta')],
    'HN-06': [(r'\bgerinc', 'a motívum gerince a héber szó')],
    'HN-07': [(r'\bsz\d+ sorok', 'a Thayer-fordításból (a 4. kör, sz12 sorok,; kézi)')],
    'HN-08': [(r'\bDT-?F?\d+', 'a jelentés és a funkció szétválasztása (F131, DT272 (d))'),
              (r'(?<![\w&/])#\d{2,3}\b', 'a #142 tétel szerint'),
              (r'\bN\d+\b', 'nyitott kérdés: N59'),
              (r'\(G\d{1,3}\)', 'a generátor szabálya (G10)'),
              (r'\bF\d{2,3}\b', 'a címketábla (F131) szerint')],
    'HN-09': [(r'\bH\d{4}\. [a-z]', 'H7121. qara קָרָא hív, kiált'),
              (r'[\u0590-\u05FF]_\d{2,4}\b', 'אָדָם_560 hímnemű főnév')],
    'HN-10': [(r'Karoli_kereszthivatkozasok\.tsv', 'forrás: konkordancia/Karoli_kereszthivatkozasok.tsv')],
    'HN-15': [(r'magyar rövid glossza-tábla a görögre még nincs',
               'A magyar rövid glossza-tábla a görögre még nincs meg.')],
}
# Az új lap kész szakaszain már ma mért esetek (a többi a szakaszával együtt lép be; a HN-03 a hatókör-sor
# zárójeles forráslistája miatt a felhasználó döntésére vár).
HN_MERT = ('HN-02', 'HN-04', 'HN-05', 'HN-06', 'HN-07', 'HN-08', 'HN-09', 'HN-10', 'HN-15')
_DATUM = datetime.date(2026, 11, 13)


def _lathato_szoveg(azonosito):
    """A mintalap kész szakaszainak látható szövege (a megjegyzések nélkül), nézetenként összefűzve."""
    eredmeny = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=_DATUM)
    return '\n'.join(''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)
                     for sorok in eredmeny.nezetek.values() for sor in sorok)


class HibanaploMintak(unittest.TestCase):
    def test_a_mintak_megfogjak_a_hibas_lapszoveget(self):
        """Minden HN-minta BUKÁS-t ad a hibás lapról vett szövegrészleten (a minta él, nem üres)."""
        for hn, mintak in HN_MINTAK.items():
            for minta, reszlet in mintak:
                self.assertTrue(re.search(minta, reszlet), '%s: %s' % (hn, minta))

    def test_a_kesz_szakaszokon_nincs_hn_talalat(self):
        """Az új lap kész szakaszainak látható szövegén a már mért HN-esetek száma 0, mindkét mintalapon
        (szeletenként bővül: a lap a kész szakaszokkal nő)."""
        for azonosito in MINTALAPOK:
            szoveg = _lathato_szoveg(azonosito)
            talalatok = [(hn, m.group(0)) for hn in HN_MERT for minta, _reszlet in HN_MINTAK[hn]
                         for m in re.finditer(minta, szoveg)]
            self.assertEqual(talalatok, [], azonosito)


class Szerkezeti(unittest.TestCase):
    @unittest.skip(S3)
    def test_gk03_pillanatkep_csak_kapuval(self):
        """GK-03: elavított másolattal BUKÁS (B18, B19, B21, B36, B38); szeletenként bővül. A B05 kapuja kész
        (`teszt_dontes.py`); a B06-ot a csoportos sor versszáma igazolja (a számítás megáll, ha nem egyezik)."""

    @unittest.skip(S4)
    def test_gk04_kapu_minden_lapon(self):
        """GK-04: az `lxx_egyezes` és a `hely_egyseg` kapuja a modellen fut, mindkét mintalapon. A melléklet-kapu és
        a teljesség-mérés frissességi kapuja kész (`teszt_dontes.py`)."""

    @unittest.skip(S8)
    def test_gk07_forrasmegjeloles_a_valodi_olvasasbol(self):
        """GK-07: a Kolofon, az Irodalom és a blokkfejlécek forrás-halmaza = az olvasási napló; licencszöveg csak
        a licencleltárból."""

    @unittest.skip(S8)
    def test_gk10_szakaszszam_es_horgony_a_modellbol(self):
        """GK-10: a szakaszrend cseréje után 0 hibás belső link."""

    @unittest.skip(S9)
    def test_gk11_nincs_globalis_allapot(self):
        """GK-11: a két mintalap fordított sorrendben generálva bájtra azonos."""

    @unittest.skip(S3)
    def test_gk13_lemma_kiejtes_es_valtozat(self):
        """GK-13: a szótári alak kiejtése ugyanabból a szolgáltatásból, a lemma-változattal: H2403a/b, H2398."""

    @unittest.skip(S3)
    def test_gk14_osszevont_versek_kulcsa(self):
        """GK-14: az összevont 9 versnél a szavak sorrendje a versösszevonás szerint áll."""

    @unittest.skip(S3)
    def test_gk15_forditas_allapot(self):
        """GK-15 (T5): `munka` módban az elavult fordítás a régi magyar szöveggel áll, jelölve; `kiadas` módban
        elavult vagy hiányzó fordítás BUKÁS; a modell listázza az érintett sorokat."""

    @unittest.skip(S3)
    def test_gk16_egy_glossza_ut(self):
        """GK-16: a héber rövid jelentés egy függvényből jön, egyféle hiánnyal."""

    @unittest.skip(S3)
    def test_gk18_bdb_betujavitas_mindenutt(self):
        """GK-18: a kártya és az olvasói réteg ugyanazt a teljesen javított BDB-szöveget adja."""

    @unittest.skip(S3)
    def test_gk19_karoli_parositas(self):
        """GK-19 (T6): minden pár számít; a látható szövegben 0 bizonyossági címke és 0 páronkénti jelölés; a mért
        pontosság egyszer, a Módszertanban áll, a konfigból."""

    @unittest.skip(S3)
    def test_gk21_a_dontesi_ut_szamai_osszeadodnak(self):
        """GK-21: a Nave-blokk nem üres. (A vizsgálat számainak összeadódása és a döntés nélküli versek száma a
        modellen kész: `teszt_dontes.py`; a Döntési út szakasz ugyanebből a modellből ír.)"""

    @unittest.skip(S9)
    def test_gk24_alakosztaly_kapu_tipus_szerint(self):
        """GK-24: a sablon-eredetű szövegen minden alakosztály tilos, az idézeten csak a proveniencia-alakok; 0
        találat mindkét új lapon, 0 hamis találat a mai mintalap prózáján és idézetein."""

    @unittest.skip(S9)
    def test_gk26_mutacios_proba(self):
        """GK-26: hat hibaváltozat (szivárgó mezőnév, ismételt címke, tört írásjel, jegyzet = cella, belső szám a
        mondatban, hiányzó „Funkció:”); mindet megfogja legalább egy kapu; jelentés kapunként."""

    @unittest.skip(S8)
    def test_gk27_jovahagyas_a_lapallapothoz(self):
        """GK-27 (T9): `munka` módban „a szerző a lap korábbi változatát hagyta jóvá (dátum)”; `kiadas` módban a
        `lap_commit` egyezése kötelező."""

    @unittest.skip(S3)
    def test_gk28_allapotmondat_adatbol(self):
        """GK-28 (T7): a SECE-, Peshitta-, Targum-, közel-keleti és Chain Lineage-mondat a jegyzék `allapot`
        mezőjéből és az adat tényleges állapotából jön; a hamis „még nincs” mondat nem áll."""

    @unittest.skip(S9)
    def test_gk31_futasido(self):
        """GK-31: egy lap generálása legfeljebb 60 s (a régi 46,5 s; 1,5-szeres túllépés megállás)."""


class AtvettTetelek(unittest.TestCase):
    """Az N-F212a tételei (a spec 6.1 táblája), az N178 és a szópár-követelmény."""

    @unittest.skip(S5)
    def test_gk_a1_masolt_karoli_kh_lista(self):
        """GK-A1: minden igehely legfeljebb egyszer szerepel a 6. szakaszban és a hatókör-jegyzetben együtt."""

    @unittest.skip(S7)
    def test_gk_a6_rokon_nyelvi_tabla(self):
        """GK-A6: „a kinyerés még nem történt meg” pontosan azoknál a lánc-szavaknál áll, amelyeknek nincs
        BDB-soruk a visszhang-táblában."""

    @unittest.skip(S3)
    def test_gk_a10_csupasz_strong_szam(self):
        """GK-A10: a lapon 0 csupasz, zárójeles Strong-szám."""

    @unittest.skip(S3)
    def test_gk_a12_nem_letezo_karoli_vers(self):
        """GK-A12: BDB-hivatkozásból képzett igehely csak akkor link, ha a vers a Károliban létezik."""

    @unittest.skip(S8)
    def test_gk_a13_a_cim_a_motivumtablabol(self):
        """GK-A13: a lap címe mindig a motívumtábla mai címe; a meglévő lap nem bemenet."""

    @unittest.skip(S9)
    def test_gk_b9(self):
        """GK-B9 (N-F212a, a spec 6.1 táblája): a hibaleltár leírása szerint újramérve, 0 eltérés. A leltár
        leírását az F218.1 halasztott része veszi át; a két futás bájtra azonos kimenetét és a `ts=` eredetét a
        `teszt_futas.py` `test_gk29_…` tesztjei már mérik."""

    @unittest.skip(S9)
    def test_gk_a11_a14_a15_b5_b8_c3_c9_d3(self):
        """GK-A11, A14, A15, B5, B8, C3, C9, D3: a hibaleltár leírása szerint újramérve, 0 eltérés (a leírásokat
        az F218.1 halasztott része veszi át)."""

    @unittest.skip(S3)
    def test_gk_n178_thayer_a_javitott_forrasbol(self):
        """GK-N178: a Thayer-kártya szakaszai a javított forrásból jönnek; a 15 érintett Strong tesztje."""

    @unittest.skip(S7)
    def test_gk_szopar(self):
        """GK-SZOPAR (DT833): a szópáros motívum 9. szakaszának feltételei; a `teszt_f194_szopar.py` esetei."""


class Hibanaplo(unittest.TestCase):
    """A hibanapló példányai (HN): szövegminta a lapon; elvárt 0 találat az új lapon. A minták a `HN_MINTAK`
    táblában állnak; a kész szakaszokon a `HibanaploMintak` már ma méri őket, a teljes lapon az alábbi tesztek."""

    @unittest.skip('a hatókör-sor zárójeles forráslistája a felhasználó döntésére vár (az S1 utáni átnézés)')
    def test_hn03_forrasnev_a_mondat_kozepen(self):
        """HN-03: forrásnév a mondat közepén, zárójelben („(a BDB-szótár)”): 0 találat."""

    @unittest.skip(S9)
    def test_hn02_hn04_cimke_ismetles_es_belso_mezonev(self):
        """HN-02, HN-04: címke-ismétlés és belső mezőnév („hivatkozas_kezi,;”, „negativ_kriterium”): 0 találat."""

    @unittest.skip(S9)
    def test_hn05_hn06_munkaszereplo_es_gerinc(self):
        """HN-05, HN-06: „felhasználó”, „orkesztrátor”, „gerinc” a látható szövegben: 0 találat."""

    @unittest.skip(S9)
    def test_hn07_hn08_hn09_belso_szam_es_nyers_szotarfej(self):
        """HN-07, HN-08, HN-09: töredék („sz<n> sorok,;”), döntésszám és tételszám, nyers BDB-fej, héber
        számláló: 0 találat mindkét új lapon."""

    @unittest.skip(S5)
    def test_hn10_karoli_kh_forrasdeklaracio(self):
        """HN-10: a Károli-kereszthivatkozás forrásdeklarációja a ténylegesen olvasott javított forrást nevezi."""

    @unittest.skip(S3)
    def test_hn12_angol_thayer_nyersen(self):
        """HN-12: nyers angol Thayer-szöveg nem kerül a lapra."""

    @unittest.skip(S3)
    def test_hn15_hamis_allapotmondat(self):
        """HN-15: „magyar rövid glossza-tábla a görögre még nincs”: 0 találat."""


if __name__ == '__main__':
    unittest.main(verbosity=1)
