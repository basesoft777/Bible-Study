"""A teljes lap kapui (S9b): GK-11 (nincs globális állapot), GK-24 (alakosztály-kapu, típus szerint), GK-25 futásidejű
része (szerkezeti kapu), GK-26 (mutációs próba), GK-31 (futásidő), és a hibanapló S9-re hagyott példányai a teljes
lapon (HN-02, 04, 05, 06, 07, 08, 09).

A mutációs próba a kész lap sorait rontja el (a fajta-térképpel együtt), és megnézi, melyik kapu fogja meg; a
jelentés kapunként a teszt hibaüzenetében áll, ha egy változatot egyik sem fogja meg.
"""
import datetime
import re
import time
import unittest

import kozos
import teszt_vaz
from kozos import MINTALAPOK
from lapgen import alakosztaly, fo, ismetles, konfig, szerkezet
from lapgen.bemenet.jegyzek import BemenetHiba
from lapgen.megjelenites.md.iro import KeszSor, MEGJEGYZES, lap_szoveg
from lapgen.szoveg import Fajta, MotivumId

DATUM = datetime.date(2026, 11, 13)
FUTASIDO_HATAR = 60.0   # a brief 5. pontja: egy lap generálása legfeljebb 60 s (a régi 46,5 s; 1,5-szeres túllépés megállás)
_LAPOK = {}


def _lap(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM)
    return _LAPOK[azonosito]


def _szoveg(eredmeny):
    return {nezet: lap_szoveg(sorok) for nezet, sorok in eredmeny.nezetek.items()}


# --- a mutációk: a kész sor módosítása a fajta-térkép megtartásával ---------------------------------------------

def _beszur(sor, hol, szoveg, fajta):
    """A sorba a `hol` pozíción `szoveg` kerül, a megadott fajtával; a később kezdődő tartományok eltolódnak."""
    tartomanyok = []
    for k, v, f in sor.tartomanyok:
        if v <= hol:
            tartomanyok.append((k, v, f))
        elif k >= hol:
            tartomanyok.append((k + len(szoveg), v + len(szoveg), f))
        else:   # a beszúrás a tartomány belsejébe esik: két részre bomlik
            tartomanyok.extend([(k, hol, f), (hol + len(szoveg), v + len(szoveg), f)])
    tartomanyok.append((hol, hol + len(szoveg), fajta))
    return KeszSor(sor.szoveg[:hol] + szoveg + sor.szoveg[hol:], tuple(sorted(tartomanyok)))


def _csere(sor, kezdet, veg, szoveg, fajta):
    """A sor [kezdet, vég) része helyére `szoveg` kerül a megadott fajtával."""
    torolt = KeszSor(sor.szoveg[:kezdet] + sor.szoveg[veg:], tuple(
        (k if k <= kezdet else max(kezdet, k - (veg - kezdet)), v if v <= kezdet else max(kezdet, v - (veg - kezdet)), f)
        for k, v, f in sor.tartomanyok if not (kezdet <= k and v <= veg)))
    return _beszur(torolt, kezdet, szoveg, fajta)


def _elso(sorok, feltetel):
    return next(i for i, s in enumerate(sorok) if feltetel(s))


def _fajta_tartomany(sor, fajta):
    return next((k, v) for k, v, f in sor.tartomanyok if f is fajta and v - k > 3)


def _mutaciok(sorok):
    """A hat hibaváltozat (név → elrontott sorok)."""
    sorok = list(sorok)
    ki = {}

    def valtozat(i, uj):
        s = list(sorok)
        s[i] = uj
        return tuple(s)

    # 1. szivárgó mezőnév egy sablonmondatban
    i = _elso(sorok, lambda s: any(f is Fajta.SABLON and v - k > 3 for k, v, f in s.tartomanyok))
    k, _v = _fajta_tartomany(sorok[i], Fajta.SABLON)
    ki['szivárgó mezőnév'] = valtozat(i, _beszur(sorok[i], k, 'negativ_kriterium ', Fajta.SABLON))
    # 2. ismételt címke a 3. szakasz egy indok-cellájában (HN-02 alakja)
    i = _elso(sorok, lambda s: s.szoveg.startswith('| ') and 'Más szó áll a versben, nem a motívum lexémája: ' in s.szoveg)
    hol = sorok[i].szoveg.index('Más szó áll a versben, nem a motívum lexémája: ')
    cimke = 'A formula nincs a versben: Nincs meg a formula a versben, a szó önállóan áll'
    ki['ismételt címke'] = valtozat(i, _csere(sorok[i], hol, len(sorok[i].szoveg) - 2, cimke, Fajta.PROZA))
    # 3. tört írásjel egy kézi prózában
    i = _elso(sorok, lambda s: any(f is Fajta.PROZA and v - k > 3 for k, v, f in s.tartomanyok))
    k, v = _fajta_tartomany(sorok[i], Fajta.PROZA)
    ki['tört írásjel'] = valtozat(i, _beszur(sorok[i], v, ',;', Fajta.PROZA))
    # 4. jegyzet = cella: a 3. szakasz első jegyzete a sora „Miért került a vizsgálatba” cellájával azonos
    j = _elso(sorok, lambda s: s.szoveg.startswith('- <span class="lj-szam" id="j-3-'))
    azon = re.search(r'id="j-(3-\d+)"', sorok[j].szoveg).group(1)
    r = _elso(sorok, lambda s: s.szoveg.startswith('| ') and ('href="#j-%s"' % azon) in s.szoveg)
    cella = re.split(r' \| ', sorok[r].szoveg)[1]
    cella = re.sub(r'<sup.*?</sup>', '', cella)
    eleje = sorok[j].szoveg.index('</span>') + len('</span>')
    vege = sorok[j].szoveg.index('<!--') if '<!--' in sorok[j].szoveg else len(sorok[j].szoveg)
    ki['jegyzet = cella'] = valtozat(j, _csere(sorok[j], eleje, vege, cella, Fajta.SABLON))
    # 5. belső szám (döntésszám) a mondatban
    i = _elso(sorok, lambda s: any(f is Fajta.SABLON and v - k > 3 for k, v, f in s.tartomanyok))
    k, v = _fajta_tartomany(sorok[i], Fajta.SABLON)
    ki['belső szám a mondatban'] = valtozat(i, _beszur(sorok[i], v, ' (DT872)', Fajta.SABLON))
    # 6. hiányzó „Funkció:” sor a 2.1 pontban
    i = _elso(sorok, lambda s: s.szoveg.startswith('Funkció: '))
    ki['hiányzó „Funkció:”'] = tuple(sorok[:i] + sorok[i + 1:])
    return ki


def _kapuk(sorok, kriterium):
    """A kész lap kapui: (név, függvény) — mindegyik BemenetHiba-t dob hibánál."""
    return (('alakosztály (GK-24)', lambda: alakosztaly.kapu({'TUDOMANYOS': sorok})),
            ('szerkezet (GK-25)', lambda: szerkezet.kapu({'TUDOMANYOS': sorok})),
            ('kritérium (DT872)', lambda: ismetles.kriterium_kapu(sorok, kriterium, teljes=True)))


class Allapot(unittest.TestCase):
    def test_gk11_nincs_globalis_allapot(self):
        """GK-11: a két mintalap fordított sorrendben generálva bájtra azonos (egy folyamatban)."""
        elore = {a: _szoveg(_lap(a)) for a in MINTALAPOK}
        hatra = {a: _szoveg(fo.lap_keszit(kozos.GYOKER, MotivumId(a), datum=DATUM)) for a in reversed(MINTALAPOK)}
        self.assertEqual(elore, hatra)


class Alakosztaly(unittest.TestCase):
    def test_gk24_nulla_talalat_mindket_lapon(self):
        """GK-24: a sablon-eredetű szövegen minden alakosztály, a prózán a belső jelölések, az idézeten a proveniencia
        tilos; mindkét mintalap minden nézetén 0 találat (ez egyben a kalibrálás: 0 hamis találat a prózán és az
        idézeten)."""
        for azonosito in MINTALAPOK:
            for nezet, sorok in _lap(azonosito).nezetek.items():
                self.assertEqual(alakosztaly.talalatok(sorok), [], '%s %s' % (azonosito, nezet))

    def test_gk24_a_kapu_fajta_szerint_dont(self):
        """Ugyanaz az alak a megjegyzésben megengedett, a sablonban nem; az idézetben csak a proveniencia tilos."""
        sor = KeszSor('x DT872 y', ((0, 2, Fajta.SABLON), (2, 7, MEGJEGYZES), (7, 9, Fajta.SABLON)))
        self.assertEqual(alakosztaly.talalatok([sor]), [])
        sor = KeszSor('x DT872 y', ((0, 9, Fajta.SABLON),))
        self.assertEqual([t[2] for t in alakosztaly.talalatok([sor])], ['döntésszám'])
        sor = KeszSor('a .tsv fájl és DT872', ((0, 20, Fajta.IDEZET),))
        self.assertEqual(alakosztaly.talalatok([sor]), [])
        sor = KeszSor('scope=x', ((0, 7, Fajta.IDEZET),))
        self.assertEqual([t[2] for t in alakosztaly.talalatok([sor])], ['proveniencia-mező'])


# Az S9c leltára (DT-F218f (4); a két N235-hely: DT-F218e (2) (b)), befagyasztva: az ismert eltérések listája ennek részhalmaza lehet, bővülni nem.
# A másolat nem változik (a hash-e rögzített); a javított tétel csak az `alakosztaly.ISMERT_CSUPASZ_STRONG`-ból kerül ki.
_S9C_B = (
    'G0173', 'G0174', 'G0331', 'G0332', 'G0685', 'G0862', 'G0942', 'G0971',
    'G2647', 'G2653', 'G2692', 'G3639', 'G4485', 'G4647', 'G4938', 'G5146',
    'H0006', 'H0329', 'H0423', 'H2254', 'H2255', 'H2312', 'H2336', 'H2554',
    'H2723', 'H2738', 'H3238', 'H3905', 'H4072', 'H4288', 'H4384', 'H4835',
    'H4893', 'H5285', 'H5518', 'H5544', 'H5636', 'H6217', 'H6231', 'H6234',
    'H6530', 'H6563', 'H6796', 'H6895', 'H7045', 'H7057', 'H7612', 'H7621',
    'H7667', 'H7701', 'H7703', 'H7722', 'H7898', 'H8045', 'H8047', 'H8068',
    'H8395',
)
_S9C_LELTAR = frozenset(
    {('A', 'H6093', 'de nem a H6093 iccávón-t', 29),
     ('D', 'H7121', 'azonos H7121+H8034 pár', 1), ('D', 'H8034', 'azonos H7121+H8034 pár', 1),
     ('N235', 'H7451', 'a H7451 és a H7043 blokkjának mintájára', 2),
     ('N235', 'H7043', 'a H7451 és a H7043 blokkjának mintájára', 2)}
    | {('B', s, 'ezekben a versekben a %s szót fordítja' % s, 1) for s in _S9C_B})
_S9C_LELTAR_HASH = 'e756373b28afe70bffbe1b7571ceb2da38b687e6c46794adb8abf2f4c8f997c7'   # a leltár sha256-a


class CsupaszStrong(unittest.TestCase):
    """N235 (DT-F218e (2), DT-F218f): a kézi prózán a zárójel nélküli Strong-szám tilos; a szótári címke tartós
    kivétel, az ismert eltérések listája csak fogyhat."""

    def test_a_lista_csak_fogyhat(self):
        """A lista a befagyasztott leltár részhalmaza (darabszámmal együtt: a megengedett darabszám sem nőhet); a leltár
        maga nem változik (hash)."""
        import hashlib
        lista = alakosztaly.ISMERT_CSUPASZ_STRONG
        self.assertEqual(len(lista), len(set(lista)), 'ismétlődő tétel')
        self.assertEqual(len(_S9C_LELTAR), 62)
        lenyomat = hashlib.sha256(repr(sorted(_S9C_LELTAR)).encode('utf-8')).hexdigest()
        self.assertEqual(lenyomat, _S9C_LELTAR_HASH, 'a befagyasztott leltár nem változhat')
        self.assertEqual(set(lista) - _S9C_LELTAR, set(), 'új tétel nem kerülhet az ismert eltérések közé')

    def test_minden_tetel_elofordul_a_mintalapokon(self):
        """A javított tétel kikerül a listából: minden tétel legalább az egyik mintalapon áll."""
        hasznalt = {}
        for azonosito in MINTALAPOK:
            for sorok in _lap(azonosito).nezetek.values():
                alakosztaly.talalatok(sorok, hasznalt)
        self.assertEqual(set(alakosztaly.ISMERT_CSUPASZ_STRONG) - set(hasznalt), set(),
                         'a mintalapokon már nem álló tétel törlendő a listából (és a leltár másolatából)')

    def test_a_kivetelek_hatara(self):
        def fajtak(szoveg):
            return [t[2] for t in alakosztaly.talalatok([KeszSor(szoveg, ((0, len(szoveg), Fajta.PROZA),))])]
        nev = alakosztaly.CSUPASZ_STRONG
        # új csupasz Strong-szám a prózában: tilos
        self.assertEqual(fajtak('a H1234 szó'), [nev])
        # szótári címke a címsorban: tartós kivétel; címsoron kívül, vagy „ — ” nélkül nem
        self.assertEqual(fajtak('#### H0779 — אָרַר (árar) · BDB'), [])
        self.assertEqual(fajtak('H0779 — אָרַר (árar)'), [nev])
        self.assertEqual(fajtak('#### a H0779 szó'), [nev])
        # ismert eltérés: csak a megnevezett szövegrészben, csak a megnevezett számra
        self.assertEqual(fajtak('szót, de nem a H6093 iccávón-t — a három'), [])
        self.assertEqual(fajtak('szót, de nem a H6093 iccávón-t, és a H6093 máshol'), [nev])
        self.assertEqual(fajtak('de nem a H6094 iccávón-t'), [nev])
        # a zárójeles alak (GK-A10) és a link nem csupasz; a nem négyjegyű és a betű-utótagos alak igen
        self.assertEqual(fajtak('[עֶצֶב](/szo/H6089)'), [])
        self.assertEqual(fajtak('a H7451A és a H779 szó'), [nev, nev])
        # a címke után héber vagy görög szónak kell állnia
        self.assertEqual(fajtak('#### H0779 — a szó'), [nev])
        self.assertEqual(fajtak('#### G1941 — ἐπικαλέω (epikaleó) · Thayer'), [])

    def test_a_darabszam_folott_bukas(self):
        """Az ismert eltérés a megengedett darabszám fölött a kapun BUKÁS (új cella ugyanazzal a fordulattal)."""
        def sor(szoveg):
            return KeszSor(szoveg, ((0, len(szoveg), Fajta.PROZA),))
        b = 'ezekben a versekben a G0331 szót fordítja'
        alakosztaly.kapu({'TUDOMANYOS': [sor(b)]})
        with self.assertRaises(BemenetHiba):
            alakosztaly.kapu({'TUDOMANYOS': [sor(b), sor(b)]})


class Szerkezet(unittest.TestCase):
    def test_gk25_nulla_hiba_mindket_lapon(self):
        for azonosito in MINTALAPOK:
            for nezet, sorok in _lap(azonosito).nezetek.items():
                self.assertEqual(szerkezet.hibak(sorok), [], '%s %s' % (azonosito, nezet))


class Mutacio(unittest.TestCase):
    def test_gk26_mind_a_hat_hibavaltozatot_megfogja_egy_kapu(self):
        """GK-26: hat hibaváltozat (szivárgó mezőnév, ismételt címke, tört írásjel, jegyzet = cella, belső szám a
        mondatban, hiányzó „Funkció:”); mindet megfogja legalább egy kapu. Az ép lapon egyik kapu sem jelez."""
        from lapgen import bemenet
        from lapgen.bemenet import motivum as motivum_be
        azonosito = 'HAMART-001'
        sorok = _lap(azonosito).nezetek['TUDOMANYOS']
        kriterium = motivum_be.kriterium_szoveg(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito))
        for nev, kapu in _kapuk(sorok, kriterium):
            kapu()   # az ép lapon nem jelez
        jelentes, megfogatlan = {}, []
        for valtozat, elrontott in _mutaciok(sorok).items():
            fogo = []
            for nev, kapu in _kapuk(elrontott, kriterium):
                try:
                    kapu()
                except BemenetHiba:
                    fogo.append(nev)
            jelentes[valtozat] = fogo
            if not fogo:
                megfogatlan.append(valtozat)
        self.assertEqual(len(jelentes), 6)
        self.assertEqual(megfogatlan, [], 'jelentés kapunként: %r' % jelentes)


class Futasido(unittest.TestCase):
    def test_gk31_futasido(self):
        """GK-31: egy lap generálása legfeljebb 60 s (a régi generátor 46,5 s; 1,5-szeres túllépés megállás)."""
        for azonosito in MINTALAPOK:
            kezdet = time.monotonic()
            fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM)
            ido = time.monotonic() - kezdet
            self.assertLessEqual(ido, FUTASIDO_HATAR, '%s: %.1f s' % (azonosito, ido))


def _hn_talalatok(hnek):
    ki = []
    for azonosito in MINTALAPOK:
        szoveg = teszt_vaz._lathato_szoveg(azonosito)
        ki.extend((azonosito, hn, m.group(0)) for hn in hnek for minta, _r in teszt_vaz.HN_MINTAK[hn]
                  for m in re.finditer(minta, szoveg))
    return ki


class Hibanaplo(unittest.TestCase):
    """A hibanapló S9-re hagyott példányai a teljes lapon (a minták: `teszt_vaz.HN_MINTAK`)."""

    def test_hn02_hn04_cimke_ismetles_es_belso_mezonev(self):
        """HN-02, HN-04: címke-ismétlés és belső mezőnév („hivatkozas_kezi,;”, „negativ_kriterium”): 0 találat."""
        self.assertEqual(_hn_talalatok(('HN-02', 'HN-04')), [])

    def test_hn05_hn06_munkaszereplo_es_gerinc(self):
        """HN-05, HN-06: „felhasználó”, „orkesztrátor”, „gerinc” a látható szövegben: 0 találat."""
        self.assertEqual(_hn_talalatok(('HN-05', 'HN-06')), [])

    def test_hn07_hn08_hn09_belso_szam_es_nyers_szotarfej(self):
        """HN-07, HN-08, HN-09: töredék („sz<n> sorok,;”), döntésszám és tételszám, nyers BDB-fej, héber
        számláló: 0 találat mindkét új lapon."""
        self.assertEqual(_hn_talalatok(('HN-07', 'HN-08', 'HN-09')), [])

    def test_hn03_forrasnev_a_mondat_kozepen(self):
        """HN-03 (DT925 (2) (a)): forrásnév a mondat közepén, zárójelben („(a BDB-szótár szerint) a …”): 0 találat
        mindkét új lapon; a sor végén álló jegyzék-megjegyzés nem találat (a minta próbája)."""
        self.assertEqual(_hn_talalatok(('HN-03',)), [])
        minta = teszt_vaz.HN_MINTAK['HN-03'][0][0]
        self.assertIsNone(re.search(minta, '- BDB (Brown–Driver–Briggs, 1906) (a BDB-szótár, közkincs)\n'))
        self.assertIsNotNone(re.search(minta, 'alapjelentés: bűn *(a STEPBible rövid szótára szerint)*\n'))


_ANGOL_KONYV = re.compile(r'\b(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|[12] ?Sam|[12] ?Kgs|[12] ?Chr|Esth|Pss?|Prov|Eccl|Isa|Lam|'
                          r'Ezek|Hos|Obad|Mic|Nah|Zeph|Zech|Matt|Rom|Rev)\.? \d+:\d+')


class Leltar(unittest.TestCase):
    """A hibaleltár (`GENERATOR_HIBALELTAR_2026-11-11.md`, N-F212a) tételei a leírásuk szerint újramérve az új lapon
    (S9c). A régi generátorra nyitott N-tételek a régi lapra szólnak; itt az új generátor mintalapjain 0 eltérés."""

    @classmethod
    def setUpClass(cls):
        cls.lap = {a: teszt_vaz._lathato_szoveg(a) for a in MINTALAPOK}

    def test_gk_b9_a_ts_a_megadott_datumbol(self):
        """GK-B9 (N-F11d): a generált `ts=` determinisztikus: két különböző megadott dátummal a lap minden sora
        egyezik, csak a megadott dátum cserélődik (a mai nap sehol nem áll); azonos dátummal bájtra azonos
        (`teszt_futas.py` GK-29)."""
        a, b = datetime.date(2026, 11, 13), datetime.date(2026, 11, 14)
        sa, sb = ('\n'.join(_szoveg(fo.lap_keszit(kozos.GYOKER, MotivumId('HAMART-001'), datum=d)).values())
                  for d in (a, b))
        self.assertNotEqual(sa, sb)
        self.assertEqual(sa.replace('2026-11-13', 'D').replace('2026.11.13', 'D'),
                         sb.replace('2026-11-14', 'D').replace('2026.11.14', 'D'))

    def test_gk_a11_a14_a15_b5_b8(self):
        """A11 (N92): angol könyvnévvel álló igehely az idézeten kívül nincs (a BDB saját alakja csak „…” idézetben
        áll, a szakirodalom dőlt angol címében is). A14 (N-F12h): a rokon nyelvi alak hiánya kimondott mondat
        (HAMART-001). A15 (N-F12i): a Kolofon „Sablon-megfelelőség” cellája nem üres. B5 (N-F148a): a fordítatlan egység jelölt („(fordításra vár)”; a T5
        kapuja: GK-15, `teszt_kartya.py`), a nyers angol Thayer nincs a lapon (HN-12). B8: 【NAPLO】 blokk nincs a
        látható szövegben."""
        for azonosito, szoveg in self.lap.items():
            idezet_nelkul = re.sub(r'\*[^*\n]+\*', '', re.sub(r'„[^”]*”', '', szoveg))   # az idézet és a dőlt cím
            self.assertEqual(_ANGOL_KONYV.findall(idezet_nelkul), [], 'A11 %s' % azonosito)
            self.assertRegex(szoveg, r'Sablon-megfelelőség \| v\d+ \|', 'A15 %s' % azonosito)
            self.assertNotIn('【', szoveg, 'B8 %s' % azonosito)
        self.assertIn('Nincs rokon nyelvi alak a BDB szócikkében', self.lap['HAMART-001'])
        self.assertGreater(self.lap['ISTENTISZT-001'].count('*(fordításra vár)*'), 0)

    @unittest.skip('218c (#238): N98 és N113 — a BDB-gerinc al-szócikk szerinti átkulcsolása és a sorbelső fej a '
                   'bemeneti rétegben; a két mintalapon nem fordul elő (a H2416 esete)')
    def test_gk_c3_bdb_gerinc_atkulcsolas(self):
        """GK-C3 (N98, N144, N145): a BDB-gerinc al-szócikk és útvonal szerint kulcsol; a sorbelső fej ismert."""

    @unittest.skip('218c (#238): N-F114b — a TSK-index tartomány-igehelyre nem keres (a HAMART-001 6 tartomány-helye '
                   'ma is utalás nélkül, a régi lappal egyezően); a bemeneti réteg bővítése')
    def test_gk_c9_tsk_tartomany_igehely(self):
        """GK-C9 (N-F114a, N-F114b): a tartomány-igehely TSK-utalásai versenként keresve."""

    @unittest.skip('218b: N-F131i — a szótári gerinc vizuális elkülönítése az olvasói CSS-ben (nem a lapgen kimenete)')
    def test_gk_d3_gerinc_vizualis_elkulonites(self):
        """GK-D3 (N-F131i): a szótári gerinc vizuálisan elkülönül."""


if __name__ == '__main__':
    unittest.main(verbosity=1)
