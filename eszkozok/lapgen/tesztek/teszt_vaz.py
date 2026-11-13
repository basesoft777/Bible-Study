"""Tesztváz (F218.3): a brief 7. pontjának még meg nem írt követelményei, név + docstring + `skip` alakban.

A teszt törzse azzal a szelettel íródik meg, amelyik a követelményt teljesíti; akkor a függvény innen a szelet
tesztfájljába költözik. A `skip` oka megnevezi a szeletet. A 218b/218c-re tartozó követelmények nincsenek itt.
"""
import unittest

S2, S3, S4, S5, S6, S7, S8, S9 = ('S2 (F218.5)', 'S3 (F218.6)', 'S4 (F218.7)', 'S5 (F218.8)', 'S6 (F218.9)',
                                  'S7 (F218.10)', 'S8 (F218.11)', 'S9 (F218.12)')


class Szerkezeti(unittest.TestCase):
    @unittest.skip(S2)
    def test_gk03_pillanatkep_csak_kapuval(self):
        """GK-03: elavított másolattal BUKÁS (B05, B06, B18, B19, B21, B36, B38); szeletenként bővül."""

    @unittest.skip(S2)
    def test_gk04_kapu_minden_lapon(self):
        """GK-04: az `lxx_egyezes`, a `hely_egyseg`, a `teljesseg` (strong, karoli, szotar háló) és a melléklet-kapu
        a modellen fut, mindkét mintalapon."""

    @unittest.skip(S2)
    def test_gk06_opcionalis_bemenet_hianya_kimondott_hiany(self):
        """GK-06: opcionális bemenet hiánya a lapmodellben kimondott hiány (felsorolás-érték), nem üres lista."""

    @unittest.skip(S8)
    def test_gk07_forrasmegjeloles_a_valodi_olvasasbol(self):
        """GK-07: a Kolofon, az Irodalom és a blokkfejlécek forrás-halmaza = az olvasási napló; licencszöveg csak
        a licencleltárból."""

    @unittest.skip(S2)
    def test_gk09_szamegyezes_kapu_a_modellen(self):
        """GK-09: a számegyezés-kapuk a lapmodell számait vetik össze, nem a kiírt szöveget."""

    @unittest.skip(S8)
    def test_gk10_szakaszszam_es_horgony_a_modellbol(self):
        """GK-10: a szakaszrend cseréje után 0 hibás belső link."""

    @unittest.skip(S9)
    def test_gk11_nincs_globalis_allapot(self):
        """GK-11: a két mintalap fordított sorrendben generálva bájtra azonos."""

    @unittest.skip(S3)
    def test_gk13_lemma_kiejtes_es_valtozat(self):
        """GK-13: a szótári alak kiejtése ugyanabból a szolgáltatásból, a lemma-változattal: H2403a/b, H2398."""

    @unittest.skip(S2)
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

    @unittest.skip(S2)
    def test_gk21_a_dontesi_ut_szamai_osszeadodnak(self):
        """GK-21: a Döntési út számai összeadódnak; döntés nélküli vers 0; a Nave-blokk nem üres (S3)."""

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
    """A hibanapló példányai (HN): szövegminta a lapon; elvárt 0 találat az új lapon."""

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

    @unittest.skip(S2)
    def test_hn11_teljesseg_meres_pillanatkepe(self):
        """HN-11: a teljesség-mérés pillanatképe frissességi kapuval lép be."""

    @unittest.skip(S3)
    def test_hn12_angol_thayer_nyersen(self):
        """HN-12: nyers angol Thayer-szöveg nem kerül a lapra."""

    @unittest.skip(S3)
    def test_hn15_hamis_allapotmondat(self):
        """HN-15: „magyar rövid glossza-tábla a görögre még nincs”: 0 találat."""


if __name__ == '__main__':
    unittest.main(verbosity=1)
