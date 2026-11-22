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
from lapgen.szoveg import Fajta, MotivumId

S2, S3, S4, S5, S6, S7, S8, S9 = ('S2 (F218.5)', 'S3 (F218.6)', 'S4 (F218.7)', 'S5 (F218.8)', 'S6 (F218.9)',
                                  'S7 (F218.10)', 'S8 (F218.11)', 'S9 (F218.12)')
# a T6 mondata (a párosítás mért pontossága egyszer, a Módszertanban) nyitott, döntéssel elhalasztva: a
# felhasználó 2026-11-21-én „Később, a validáció után”; a JOHD-validáció után, a validált számmal (N-F218v)
S8_GK19 = ('GK-19 (T6): nyitott, döntéssel elhalasztva (2026-11-21, „Később, a validáció után”; N-F218v); '
           'a mondat a JOHD-validáció után kerül a lapra')
S3_MARADEK = ('az S3 kész, de ezt a követelményt nem teljesítette (a 6. ellenőrzés E9 tétele); a 218a végi '
              'átnézésén szeletet kap')
HELY_EGYSEG = ('a névvel megadott szópár (1.4, `málé+chámász`) tagjait a modell nem köti Strong-számhoz; a kapu '
               'ehhez a bemeneti rétegben kér feloldást (N-tétel)')
ISM_3 = 'a „3. Kizárt és vizsgált helyek” szakasz szelete (a briefben nincs külön szelete; a szakasz megépítésekor)'


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
    """A mintalap kész szakaszainak látható szövege (a megjegyzések és a link-célpontok nélkül: a horgony a
    Markdown-link célja, az olvasó nem látja; a Tartalomjegyzék „#10-értelmezés” horgonya nem tételszám), nézetenként
    összefűzve."""
    eredmeny = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=_DATUM)
    return '\n'.join(''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f not in (MEGJEGYZES, Fajta.HORGONY))
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
    @unittest.skip(S3_MARADEK)
    def test_gk03_pillanatkep_csak_kapuval(self):
        """GK-03: elavított másolattal BUKÁS (B18, B19, B21, B36, B38); szeletenként bővül. A B05 kapuja kész
        (`teszt_dontes.py`); a B06-ot a csoportos sor versszáma igazolja (a számítás megáll, ha nem egyezik)."""

    @unittest.skip(HELY_EGYSEG)
    def test_gk04_hely_egyseg_kapu(self):
        """GK-04, a `hely_egyseg` része (a régi `hely_egyseg_kapu`, F212 Sz4): a szavanként az 1.4 csoportjainak
        helyszáma (szópárban is) és az Áttekintés „Helyek a motívumban” oszlopa egyezik, a modellen, mindkét mintalapon.
        Az `lxx_egyezes` része kész (`teszt_lxx.py` `Gk04`)."""



    @unittest.skip(ISM_3)
    def test_ism_a_3_szakasz_utal_nem_ismetel(self):
        """DT-F218n: a „3. Kizárt és vizsgált helyek” szakasz végi „Negatív kritérium” bekezdése helyett utalás áll
        a lap eleji meghatározásra, a szakasz elején."""

    @unittest.skip(S9)
    def test_gk11_nincs_globalis_allapot(self):
        """GK-11: a két mintalap fordított sorrendben generálva bájtra azonos."""

    @unittest.skip(S3_MARADEK)
    def test_gk13_lemma_kiejtes_es_valtozat(self):
        """GK-13: a szótári alak kiejtése ugyanabból a szolgáltatásból, a lemma-változattal: H2403a/b, H2398."""

    @unittest.skip(S3_MARADEK)
    def test_gk14_osszevont_versek_kulcsa(self):
        """GK-14: az összevont 9 versnél a szavak sorrendje a versösszevonás szerint áll."""

    @unittest.skip(S3_MARADEK)
    def test_gk18_bdb_betujavitas_mindenutt(self):
        """GK-18: a kártya és az olvasói réteg ugyanazt a teljesen javított BDB-szöveget adja."""

    @unittest.skip(S8_GK19)
    def test_gk19_karoli_parositas(self):
        """GK-19 (T6): a párosítás mért pontossága egyszer, a Módszertanban áll, a konfigból. (A másik két fele
        kész: minden pár számít, és a 4.13–4.14 látható szövegében nincs bizonyossági címke és páronkénti jelölés:
        `teszt_szotari_karoli.py`.)"""

    @unittest.skip(S9)
    def test_gk24_alakosztaly_kapu_tipus_szerint(self):
        """GK-24: a sablon-eredetű szövegen minden alakosztály tilos, az idézeten csak a proveniencia-alakok; 0
        találat mindkét új lapon, 0 hamis találat a mai mintalap prózáján és idézetein."""

    @unittest.skip(S9)
    def test_gk26_mutacios_proba(self):
        """GK-26: hat hibaváltozat (szivárgó mezőnév, ismételt címke, tört írásjel, jegyzet = cella, belső szám a
        mondatban, hiányzó „Funkció:”); mindet megfogja legalább egy kapu; jelentés kapunként."""



    @unittest.skip(S9)
    def test_gk31_futasido(self):
        """GK-31: egy lap generálása legfeljebb 60 s (a régi 46,5 s; 1,5-szeres túllépés megállás)."""


class AtvettTetelek(unittest.TestCase):
    """Az N-F212a tételei (a spec 6.1 táblája), az N178 és a szópár-követelmény."""

    @unittest.skip(S3_MARADEK)
    def test_gk_a10_csupasz_strong_szam(self):
        """GK-A10: a lapon 0 csupasz, zárójeles Strong-szám."""

    @unittest.skip(S3_MARADEK)
    def test_gk_a12_nem_letezo_karoli_vers(self):
        """GK-A12: BDB-hivatkozásból képzett igehely csak akkor link, ha a vers a Károliban létezik."""

    @unittest.skip(S9)
    def test_gk_b9(self):
        """GK-B9 (N-F212a, a spec 6.1 táblája): a hibaleltár leírása szerint újramérve, 0 eltérés. A leltár
        leírását az F218.1 halasztott része veszi át; a két futás bájtra azonos kimenetét és a `ts=` eredetét a
        `teszt_futas.py` `test_gk29_…` tesztjei már mérik."""

    @unittest.skip(S9)
    def test_gk_a11_a14_a15_b5_b8_c3_c9_d3(self):
        """GK-A11, A14, A15, B5, B8, C3, C9, D3: a hibaleltár leírása szerint újramérve, 0 eltérés (a leírásokat
        az F218.1 halasztott része veszi át)."""

    @unittest.skip(S3_MARADEK)
    def test_gk_n178_thayer_a_javitott_forrasbol(self):
        """GK-N178: a Thayer-kártya szakaszai a javított forrásból jönnek; a 15 érintett Strong tesztje."""



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

    @unittest.skip(S3_MARADEK)
    def test_hn12_angol_thayer_nyersen(self):
        """HN-12: nyers angol Thayer-szöveg nem kerül a lapra."""


if __name__ == '__main__':
    unittest.main(verbosity=1)
