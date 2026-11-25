#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_proza_allitas.py -- a próza-állítás ellenőrző (`eszkozok/proza_allitas.py`, F200) tesztjei.

A gépi próbák a HAMART-001 lektorának pontossági tételein (naplok/KIADAS_HAMART-001_lektor.md, #696) mintázva, de a
motívum forrásától függetlenül: a tesztmondatok itt állnak, a vers-adat a konkordancia (TAHOT, Károli 1908, a
Károli-párosítás). Így a HAMART-001 javítóköre nem töri el a tesztet.

1. Igehely-felismerés: felsorolás egy könyvön belül és könyvváltással, tartomány, a fejezetszintű „1Mózes 3–9.” nem ige.
2. A tagadás hatóköre (`neg_ervenyes`): a „föld szava nélkül” a tagmondaton át nem nyúlik.
3. Szópár és alanya: „a föld megtelt erőszakkal (Ez 7:23)” ELTÉR (a városról szól), az Ez 8:17 egyezik; az Ez 12:19-ből
   a megtelés igéje hiányzik.
4. Szójelenlét: „a föld szava nélkül … (2Kir 17:23)” ELTÉR (ott az adámá áll).
5. Fordulat: „a „föld színéről” fordulat … is áll (1Kir 14:15, Ámós 9:8)”: az első ELTÉR, a második egyezik.
6. Idézet: a Károli szövege egyezik, a módosított idézet ELTÉR; a szótári jelentés idézőjelben nem idézet.
7. Szám: a lap egészére szóló szám az adattal; részhalmazra szóló szám kézi.
8. Kizárólagos állítás igehely nélkül: kézi ⚑.
9. A lektori lista pontossági tételei (1. vagy 4. kérdés).
10. F206: kapcsolat-állítás a kapcsolat-sor mellett (nincs sor / csak közepes: ⚑; magas: nincs jelzés; a motívumon
    kívüli hely és a kapcsolat-adat nélküli motívum nem jelez); hatókör: a helycsoport tematikus helye.
11. F200.7 (HIBA-szint, E41): a téves riasztás három oka (a „lexikai” minősítésű szám, a fordulat-idézet legközelebbi
    igehelye és névelője, a mondat által megnevezett héber szó) és a `--kapu` (új/régi formájú forrás, bukó és átmenő eset).
12. F224.4: a három új K-fajta (szám + kapcsolat/erősség, belső utalás, „nem dönti el”), mindegyik pozitív és negatív
    esettel; az új fajta soha nem gépi ELTÉR, a régi K-tételek számozása nem változik, a `--kapu` JELENTÉS-sort ad.
13. F224.14 (N-F224c): az idézettel lefedett mondat többletállítása K-tétel (a puszta idézet nem); az igehely nélküli
    szabály-mondat K-tétel a gerinc-szavak helyenkénti sorrendjével; a K-számozás három szintje.
14. F224.15: a mondaton kívüli adat (funkció-mező — csak a hely saját tételénél, N-F224f —, angol tükörfordítás, a lap más mondata ugyanarról a forrásról,
    Targum, szótári besorolás az elutasított jelöltekkel; a szótári kód és az útvonal illesztése).
15. F205 M3: a `--tanulmany` mód fixture-ön — a próza és a blokkok egységei (a changelog, a tábla, a kódblokk, a
    hibás fejlécű blokk és a hibás pont kimarad; a hiányos blokk meglévő szövege marad), a motívum-környezet a
    blokkok egyetlen motívumából (több motívumnál `--motivum` kell, a más motívum blokkja kimarad), az idézetpróba a
    prózán és a blokk saját versén, a jelentés forrás-leírása (a motívum-mód szövege változatlan), a CLI kizárásai.

Futtatás: python eszkozok/teszt_proza_allitas.py
"""
import io
import os
import shutil
import sys
import tempfile
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import proza_allitas as P  # noqa: E402

FORRAS = """# Teszt
#### H0127 — אֲדָמָה (adámá) · BDB
#### H2555 — חָמָס (chámász) · BDB
A lánc szavai: a föld (adámá) és az erőszak (chámász). A lánc szópárja (megtelt erőszakkal).
"""
ELOF = [
    {'id': 'X-001', 'igehely': '1Móz 4:14', 'gerinc_elem': 'H0127', 'strong': 'H0127'},
    {'id': 'X-001', 'igehely': '1Móz 6:11', 'gerinc_elem': 'H2555', 'strong': 'H2555'},
    {'id': 'X-001', 'igehely': 'Ez 8:17', 'gerinc_elem': 'málé+chámász', 'strong': 'H2555'},
]
VERSEK_KELL = ['Ézs 24:5-6', 'Hós 4:1-3', '1Móz 4:14', '1Móz 6:11', '1Móz 8:21', 'Ez 7:23', 'Ez 8:17', 'Ez 12:19', '2Kir 17:23', '1Kir 14:15',
               'Ámós 9:8', '5Móz 27:15', '1Kir 13:34', 'Jer 23:10']

_KORNYEZET = {}


def kornyezet():
    if not _KORNYEZET:
        adat = P.Adat()
        versek = set()
        for r in VERSEK_KELL:
            versek.update(adat.versek(r))
        adat.betolt_szavak(versek)
        adat.betolt_parok(versek)
        _KORNYEZET['adat'] = adat
        _KORNYEZET['igeh'] = P.Igehelyek()
        _KORNYEZET['szk'] = P.Szokeszlet(FORRAS, ELOF, adat)
    return _KORNYEZET


def futtat(mondat, forras='rés:kivonat', alap_ref=None):
    k = kornyezet()
    ell = P.Ellenor('X-001', k['adat'], k['szk'], ELOF, k['igeh'])
    ell.egyseg(P.Egyseg(forras, 'teszt:1', mondat, alap_ref=alap_ref))
    return ell.sorok


def iteletek(sorok, tipus=None):
    return {(s.vers, s.itelet) for s in sorok if tipus is None or s.tipus == tipus}


class Igehely(unittest.TestCase):
    def test_felsorolas(self):
        ig = P.Igehelyek()
        cs = ig.csoportok('az erőszakkal megtelt föld Ezékielnél (Ez 7:23, 8:17, 12:19), a föld színéről')
        self.assertEqual([r for _, _, rs in cs for r in rs], ['Ez 7:23', 'Ez 8:17', 'Ez 12:19'])

    def test_konyvvaltas_es_tartomany(self):
        ig = P.Igehelyek()
        cs = ig.csoportok('áll (1Kir 13:34, 14:15, 2Kir 17:23, Ámós 9:8), és (1Móz 6:12-13)')
        self.assertEqual([r for _, _, rs in cs for r in rs],
                         ['1Kir 13:34', '1Kir 14:15', '2Kir 17:23', 'Ámós 9:8', '1Móz 6:12-13'])

    def test_fejezetszint_nem_ige(self):
        self.assertEqual(P.Igehelyek().csoportok('Az 1Mózes 3–9. fejezetében hat héber szó'), [])


class Tagadas(unittest.TestCase):
    def test_tagmondaton_belul(self):
        s = 'csak a szövetség rendjében mondja ki, a föld szava nélkül: ilyenek az átkok (5Móz 27:15) és (2Kir 17:23).'
        neg = P.NEGALT.search(s)
        self.assertTrue(P.neg_ervenyes(s, neg, s.index('(2Kir'), ''))

    def test_tagmondaton_at_nem(self):
        s = ('kikerült (a törvény átok-formulái a föld szava nélkül, a többi), két tartomány pedig szűkült, '
             'amelyben a lánc szava áll (5Móz 28:18).')
        neg = P.NEGALT.search(s)
        self.assertFalse(P.neg_ervenyes(s, neg, s.index('(5Móz'), ''))


class Normalizalas(unittest.TestCase):
    def test_strong_norm_f62(self):
        """ELLENOR_F200 2.: az ötjegyű G-kiegészítő kód nem csonkolódik másik létező számmá."""
        self.assertEqual(P.strong_norm('G20447'), 'G20447')
        self.assertEqual(P.strong_norm('H127'), 'H0127')
        self.assertEqual(P.strong_norm('málé'), '')

    def test_vonatkozo_mellekmondat(self):
        """ELLENOR_F200 1.: az előző igehelyre szóló „…, ahol …” mellékmondat a következő csoport záradékából kimarad."""
        self.assertEqual(P.zaradek_sajat(', ahol az átok más héber szóval emészti meg a földet, a '), ' a ')
        self.assertEqual(P.zaradek_sajat(', a föld megtelt erőszakkal '), ', a föld megtelt erőszakkal ')


class GepiProbak(unittest.TestCase):
    def test_mas_szo_az_elozo_csoporte(self):
        sorok = futtat('Ilyen az Ézs 24:5-6, ahol a föld más héber szóval áll, és a Hós 4:1-3.')
        it = iteletek(sorok, 'szójelenlét')
        self.assertTrue([v for v, _ in it if v == 'Ézs 24:5-6'])
        self.assertFalse([v for v, _ in it if v == 'Hós 4:1-3'])

    def test_szopar_alanya_eltér(self):
        sorok = futtat('A próféták mondják, hogy a föld megtelt erőszakkal (Ez 7:23).')
        self.assertIn(('Ez 7:23', 'ELTÉR'), iteletek(sorok, 'szópár'))

    def test_szopar_alanya_egyezik(self):
        sorok = futtat('A próféták mondják, hogy a föld megtelt erőszakkal (Ez 8:17).')
        self.assertIn(('Ez 8:17', 'egyezik'), iteletek(sorok, 'szópár'))

    def test_szopar_hianyzo_szo(self):
        sorok = futtat('Az erőszakkal megtelt föld Ezékielnél (Ez 12:19).')
        self.assertIn(('Ez 12:19', 'ELTÉR'), iteletek(sorok, 'szópár'))

    def test_szo_nelkul_de_all(self):
        sorok = futtat('Nem tartozik ide, amely a föld szava nélkül mondja ki: Izrael fogsága (2Kir 17:23).')
        self.assertIn(('2Kir 17:23', 'ELTÉR'), iteletek(sorok, 'szójelenlét'))

    def test_fordulat(self):
        sorok = futtat('A „föld színéről” fordulat a földvesztés helyein is áll (1Kir 14:15, Ámós 9:8).')
        it = iteletek(sorok, 'fordulat')
        self.assertIn(('1Kir 14:15', 'ELTÉR'), it)
        self.assertIn(('Ámós 9:8', 'egyezik'), it)

    def test_idezet(self):
        jo = futtat('A fordulópont: „Nem átkozom meg többé a földet az emberért” (1Móz 8:21).')
        self.assertIn(('1Móz 8:21', 'egyezik'), iteletek(jo, 'idézet'))
        rossz = futtat('A fordulópont: „Nem átkozom meg soha a földet az ember miatt” (1Móz 8:21).')
        self.assertTrue(any(s.itelet == 'ELTÉR' for s in rossz if s.tipus == 'idézet'))

    def test_szotari_jelentes_nem_idezet(self):
        sorok = futtat('A szó elsősorban „néven nevezni, elnevezni” jelentésben áll (1Móz 8:21).')
        self.assertFalse([s for s in sorok if s.tipus == 'idézet'])

    def test_szam_a_lapra(self):
        jo = futtat('A lap 3 helyet sorol fel.')
        self.assertEqual([s.itelet for s in jo if s.tipus == 'szám'], ['egyezik'])
        rossz = futtat('A lap 5 helyet sorol fel.')
        self.assertEqual([s.itelet for s in rossz if s.tipus == 'szám'], ['ELTÉR'])

    def test_szam_reszhalmaz_kezi(self):
        sorok = futtat('A motívum helyei közül csak ebben a két versben áll más szó.')
        self.assertEqual([s.itelet for s in sorok if s.tipus == 'szám'], ['kézi'])

    def test_kizarolagos_allitas(self):
        sorok = futtat('A szöveg azt állítja, hogy a bűnnek mindig vannak az elkövetőn túli hatásai.',
                       forras='rés:ertelmezes')
        self.assertTrue(any(s.itelet == 'kézi' and s.jelzes for s in sorok))

    def test_erec_jelzes(self):
        sorok = futtat('Az özönvíz előtt a föld romlott meg (1Móz 6:11).')
        self.assertTrue(any(s.jelzes and 'H0776' in s.bizonyitek for s in sorok))


KAPCS_KOZEPES = [{'forras_igehely': '1Móz 6:11', 'cel_igehely': 'Ez 8:17', 'id': 'X-001', 'tipus': 'Párhuzam',
                  'bizonyossag': 'közepes'}]
KAPCS_MAGAS = [dict(KAPCS_KOZEPES[0], bizonyossag='magas')]
KAPCS_MASIK = [dict(KAPCS_KOZEPES[0], forras_igehely='1Móz 4:14', cel_igehely='1Móz 6:11')]


def futtat_k(mondat, kapcsolatok, forras='adat:kapcsolodas', alap_ref='Ez 8:17', elof=None):
    k = kornyezet()
    ell = P.Ellenor('X-001', k['adat'], k['szk'], elof or ELOF, k['igeh'], kapcsolatok)
    ell.egyseg(P.Egyseg(forras, 'teszt:1', mondat, alap_ref=alap_ref))
    return ell.sorok


def kapcs_jelzes(sorok):
    return [s for s in sorok if 'kapcsolat-állítás' in s.bizonyitek]


class F206(unittest.TestCase):
    """F206: a HAMART-001 lektori körének két ismétlődő hibaosztálya (lektor 10., 14., 26., 40.)."""
    MONDAT = 'A föld megtelt erőszakkal, és a szópár maga utal vissza a láncra.'

    def test_kapcsolat_sor_nelkul(self):
        self.assertTrue(kapcs_jelzes(futtat_k(self.MONDAT, KAPCS_MASIK)))

    def test_kapcsolat_kozepes(self):
        sorok = kapcs_jelzes(futtat_k(self.MONDAT, KAPCS_KOZEPES))
        self.assertTrue(sorok and 'közepes' in sorok[0].bizonyitek)

    def test_kapcsolat_magas_nem_jelez(self):
        self.assertFalse(kapcs_jelzes(futtat_k(self.MONDAT, KAPCS_MAGAS)))

    def test_kapcsolat_adat_nelkuli_motivum(self):
        """Kapcsolat-adat nélküli motívumon (pl. ALVIL-001) a próba nem fut: adathiány, nem a mondat hibája."""
        self.assertFalse(kapcs_jelzes(futtat_k(self.MONDAT, [])))

    def test_visszateres_fonev_nem_jelez(self):
        """A „visszatérés” főnév tartalmi szó lehet („nincs visszatérés”), nem kapcsolat-állítás."""
        self.assertFalse(kapcs_jelzes(futtat_k('Ebből a mélységből nincs visszatérés a földre.', KAPCS_MASIK)))

    def test_ige_nelkul_nem_jelez(self):
        self.assertFalse(kapcs_jelzes(futtat_k('A föld megtelt erőszakkal a próféta idejében.', KAPCS_MASIK)))

    def test_res_ige_masik_tagmondatban(self):
        """A rés mondatában a kapcsolat-ige a saját záradékra szól: a másik tagmondat helye nem kap jelzést."""
        sorok = futtat_k('Az átok szava visszatér (1Móz 6:11); a próféta a földről is beszél (Ez 8:17).', KAPCS_MASIK,
                         forras='rés:ertelmezes', alap_ref=None)
        self.assertFalse([s for s in kapcs_jelzes(sorok) if 'Ez 8:17' in s.bizonyitek])

    def test_hatokor_mas_nelkul_nem_nemit(self):
        """A „nélkül” csak a lánc szavával együtt mondja ki a kivételt (ELLENOR_F206)."""
        elof = ELOF + [{'id': 'X-001', 'igehely': 'Jel 22:3', 'gerinc_elem': 'tematikus:1Móz 3:17', 'strong': ''}]
        mondat = 'A motívum újszövetségi helyén a motívum szava kétség nélkül ugyanott áll.'
        sorok = futtat_k(mondat, [], forras='rés:modszertan', alap_ref=None, elof=elof)
        self.assertTrue([s for s in sorok if s.tipus == 'hatókör'])

    def test_res_motivumon_kivuli_hely(self):
        sorok = futtat_k('A formula Ezékielnél is visszatér (Ez 7:23).', KAPCS_MASIK, forras='rés:modszertan', alap_ref=None)
        self.assertFalse(kapcs_jelzes(sorok))

    def test_res_motivum_helye_sor_nelkul(self):
        sorok = futtat_k('A lánc szava Ezékielnél is visszatér (Ez 8:17).', KAPCS_MASIK, forras='rés:ertelmezes', alap_ref=None)
        self.assertTrue(kapcs_jelzes(sorok))

    def test_hatokor_tematikus(self):
        elof = ELOF + [{'id': 'X-001', 'igehely': 'Róm 8:21', 'gerinc_elem': 'G5356', 'strong': 'G5356'},
                       {'id': 'X-001', 'igehely': 'Jel 22:3', 'gerinc_elem': 'tematikus:1Móz 3:17', 'strong': ''}]
        mondat = 'A motívum két újszövetségi helyén a motívum szava a kritikai kiadásokban ugyanott áll.'
        sorok = futtat_k(mondat, [], forras='rés:modszertan', alap_ref=None, elof=elof)
        self.assertTrue([s for s in sorok if s.tipus == 'hatókör' and 'Jel 22:3' in s.bizonyitek])
        kimondva = mondat.replace('áll.', 'áll; a Jel 22:3 tematikus.')
        sorok = futtat_k(kimondva, [], forras='rés:modszertan', alap_ref=None, elof=elof)
        self.assertFalse([s for s in sorok if s.tipus == 'hatókör'])


FORRAS_ATOK = FORRAS + """#### H0779 — אָרַר (árar) · BDB
A lánc szava még az átok (árar).
"""
ELOF_NT = ELOF + [
    {'id': 'X-001', 'igehely': 'Róm 8:21', 'gerinc_elem': 'G5356', 'strong': 'G5356'},
    {'id': 'X-001', 'igehely': 'Gal 3:13', 'gerinc_elem': 'G1944', 'strong': 'G1944'},
    {'id': 'X-001', 'igehely': 'Zsid 6:7', 'gerinc_elem': 'G2671', 'strong': 'G2671'},
    {'id': 'X-001', 'igehely': 'Jel 11:18', 'gerinc_elem': 'G1311', 'strong': 'G1311'},
    {'id': 'X-001', 'igehely': 'Jel 19:2', 'gerinc_elem': 'G5351', 'strong': 'G5351'},
    {'id': 'X-001', 'igehely': 'Jel 22:3', 'gerinc_elem': 'tematikus:1Móz 3:17', 'strong': ''},
]


class F200_7(unittest.TestCase):
    """F200.7: a HIBA-szintre emelés előtti mérés (naplok/F200_HIBA_SZINT_MERES.md) téves riasztásainak gépi javítása."""

    def test_szam_lexikai_minosites(self):
        # öt lexikai + egy tematikus újszövetségi hely: az „öt lexikai” egyezik, a minősítés nélküli „öt” ELTÉR
        jo = futtat_k('A motívum öt lexikai újszövetségi helyén a lánc szava ugyanott áll.', [],
                      forras='rés:modszertan', alap_ref=None, elof=ELOF_NT)
        self.assertEqual([s.itelet for s in jo if s.tipus == 'szám'], ['egyezik'])
        rossz = futtat_k('A motívum öt újszövetségi helyén a lánc szava ugyanott áll.', [],
                         forras='rés:modszertan', alap_ref=None, elof=ELOF_NT)
        self.assertEqual([s.itelet for s in rossz if s.tipus == 'szám'], ['ELTÉR'])
        # a lexikai csoport számát is ellenőrzi: hat lexikai helyből csak öt van
        rossz = futtat_k('A motívum hat lexikai újszövetségi helyén a lánc szava ugyanott áll.', [],
                         forras='rés:modszertan', alap_ref=None, elof=ELOF_NT)
        self.assertEqual([s.itelet for s in rossz if s.tipus == 'szám'], ['ELTÉR'])

    def test_fordulat_a_fordulat_elotti_helyekre(self):
        mondat = ('Az 1Kir 13:34-ben és az Ámós 9:8-ban a „föld színéről” fordulattal, az 1Kir 14:15-ben és a 2Kir 17:23-ban '
                  '„a földről” áll a föld szava.')
        sorok = futtat(mondat, forras='rés:ertelmezes')
        it = iteletek(sorok, 'fordulat')
        self.assertIn(('Ámós 9:8', 'egyezik'), it)
        self.assertFalse([s for s in sorok if s.tipus == 'fordulat' and s.itelet == 'ELTÉR'])
        # a névelős idézet („a földről”) nem kétszavas fordulat
        self.assertFalse([s for s in sorok if s.tipus == 'fordulat' and 'a földről' in s.allitas])

    def test_fordulat_valodi_hiba_marad(self):
        # a fordulat a következő helyre szól és a versből hiányzik: továbbra is ELTÉR
        sorok = futtat('A „föld színéről” fordulat áll a földvesztés helyén (1Kir 14:15).', forras='rés:ertelmezes')
        self.assertIn(('1Kir 14:15', 'ELTÉR'), iteletek(sorok, 'fordulat'))

    def _szk_atok(self):
        k = kornyezet()
        return P.Szokeszlet(FORRAS_ATOK, ELOF, k['adat'])

    def _atok(self, mondat):
        k = kornyezet()
        ell = P.Ellenor('X-001', k['adat'], self._szk_atok(), ELOF, k['igeh'])
        ell.egyseg(P.Egyseg('adat:kapcsolodas', 'teszt:1', mondat, alap_ref='Jer 23:10'))
        return iteletek(ell.sorok, 'szójelenlét')

    def test_megnevezett_szo_a_versben(self):
        # a lánc „átok” szava az árar (H0779), a mondat az álá-t (H0423) nevezi meg: a Jer 23:10-ben az áll
        self.assertIn(('Jer 23:10', 'egyezik'),
                      self._atok('A héberben itt az átok szava áll (álá), ugyanaz, mint az Ézs 24:6-ban.'))

    def test_megnevezett_szo_nincs_a_versben(self):
        # az árar nincs a Jer 23:10-ben: a megnevezett szó sem, a lánc szava sem
        self.assertIn(('Jer 23:10', 'ELTÉR'), self._atok('A héberben itt az átok szava áll (árar), mint az Ézs 24:6-ban.'))
        # megnevezés nélkül a lánc szava dönt: ELTÉR
        self.assertIn(('Jer 23:10', 'ELTÉR'), self._atok('A héberben itt az átok szava áll, mint az Ézs 24:6-ban.'))

    def test_uj_formaju(self):
        k = kornyezet()
        self.assertTrue(P.uj_formaju('', k['szk']))   # a szókészlet nem üres
        szk_ures = P.Szokeszlet('Nincs megnevezés.', ELOF, k['adat'])
        self.assertFalse(P.uj_formaju('Nincs megnevezés.', szk_ures))
        self.assertTrue(P.uj_formaju('【NAPLO: (`sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`)', szk_ures))


class Kapu(unittest.TestCase):
    """F200.7: a `--kapu` (E41): ELTÉR = HIBA az új formájú forráson, a régi formájú kimarad, és kimondja."""

    RES = '<!-- RÉS-KEZDET: kivonat -->\n%s\n<!-- RÉS-VÉGE: kivonat -->\n'

    def _futtat(self, forrasok, mondat):
        tmp = tempfile.mkdtemp()
        try:
            for nev, elo in forrasok.items():
                with open(os.path.join(tmp, nev + '.md'), 'w', encoding='utf-8', newline='\n') as f:
                    f.write(elo + self.RES % mondat)
            elof = os.path.join(tmp, 'elof.tsv')
            with open(elof, 'w', encoding='utf-8', newline='\n') as f:
                f.write('id\tigehely\tgerinc_elem\tstrong\tkapcsolodas\n')
                for nev in forrasok:
                    for d in ELOF:
                        f.write('\t'.join([nev, d['igehely'], d['gerinc_elem'], d['strong'], '']) + '\n')
            ki = io.StringIO()
            return P.kapu(tmp, elof, ki), ki.getvalue()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_uj_forma_hiba_es_regi_forma_kimarad(self):
        hibak, ki = self._futtat({'X-001': FORRAS, 'X-002': 'Nincs megnevezés.\n'}, 'A lap 5 helyet sorol fel.')
        self.assertEqual(hibak, 1)
        self.assertIn('**HIBA** X-001', ki)
        self.assertIn('X-002: régi formájú forrás', ki)
        self.assertNotIn('**HIBA** X-002', ki)

    def test_atmeno_eset(self):
        hibak, ki = self._futtat({'X-001': FORRAS}, 'A lap 3 helyet sorol fel.')
        self.assertEqual(hibak, 0)
        self.assertIn('nincs ELTÉR-sor', ki)

    def test_kezi_sor_nem_hiba(self):
        # a „kézi” gépi ítélet (a szám viszonyítási alapja nem állapítható meg) jelentés marad
        hibak, _ = self._futtat({'X-001': FORRAS}, 'A motívum helyei közül csak ebben a két versben áll más szó.')
        self.assertEqual(hibak, 0)


def kapcs_sorok(n_magas, n_kozepes=0):
    ki = [{'forras_igehely': '1Móz 4:14', 'cel_igehely': '1Móz 6:11', 'id': 'X-001', 'bizonyossag': 'magas'}
          for _ in range(n_magas)]
    ki += [{'forras_igehely': '1Móz 6:11', 'cel_igehely': 'Ez 8:17', 'id': 'X-001', 'bizonyossag': 'közepes'}
           for _ in range(n_kozepes)]
    return ki


def futtat_uj(mondatok, kapcsolatok=(), cimek=(), hely=None):
    """F224.4: több egység egy Ellenoron (a „nem dönti el” mondat párjaihoz), címsorokkal."""
    k = kornyezet()
    ell = P.Ellenor('X-001', k['adat'], k['szk'], ELOF, k['igeh'], list(kapcsolatok))
    ell.cimek = list(cimek)
    ell.egysegek = [P.Egyseg('rés:ertelmezes', (hely or {}).get(i, 'teszt:%d' % (i + 1)), m)
                    for i, m in enumerate(mondatok)]
    for e in ell.egysegek:
        ell.egyseg(e)
    return ell


def uj_sorok(ell, tipus):
    return [s for s in ell.sorok if s.tipus == tipus]


class F224_4(unittest.TestCase):
    """F224.4: a kinyerés három új K-fajtája (az ISTENTISZT-001 mérésének 4. és 9. tétele után)."""

    def test_szam_kapcsolat_elter_jellegu(self):
        ell = futtat_uj(['A motívum helyei között három kapcsolat erős.'], kapcs_sorok(13, 3))
        s = uj_sorok(ell, 'szám-kapcsolat')
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0].itelet, 'kézi')        # soha nem gépi ELTÉR (E41 változatlan)
        self.assertIn(P.JELENTES_JEL, s[0].bizonyitek)
        self.assertIn('13 „magas”', s[0].bizonyitek)
        self.assertEqual(s[0].jelzes, '⚑')

    def test_szam_kapcsolat_egyezik(self):
        ell = futtat_uj(['A motívum helyei között három kapcsolat erős.'], kapcs_sorok(3, 2))
        s = uj_sorok(ell, 'szám-kapcsolat')
        self.assertEqual(len(s), 1)
        self.assertNotIn(P.JELENTES_JEL, s[0].bizonyitek)

    def test_szam_kapcsolat_nincs(self):
        ell = futtat_uj(['A motívum helyei között a kapcsolat erős, és három hely a Genezisben áll.'],
                        kapcs_sorok(13))
        self.assertEqual(uj_sorok(ell, 'szám-kapcsolat'), [])

    def test_helybol(self):
        ell = futtat_uj(['Mózes könyveinek hét helyéből ötben így, az 1Móz 4:14-ben viszont nem.'])
        s = uj_sorok(ell, 'szám-kapcsolat')
        self.assertEqual(len(s), 1)
        self.assertIn('7 helyből 5', s[0].bizonyitek)
        self.assertIn('1Móz 4:14', s[0].bizonyitek)

    def test_belso_utalas_nincs_cel(self):
        ell = futtat_uj(['A kérdést részletesen l. a 12. szakasz.'], cimek=['## 10. Értelmezés', '## 11. Módszertan'])
        s = uj_sorok(ell, 'belső utalás')
        self.assertEqual(len(s), 1)
        self.assertIn(P.JELENTES_JEL, s[0].bizonyitek)

    def test_belso_utalas_van_cel(self):
        ell = futtat_uj(['A kérdést részletesen l. a 11. szakasz, és a vitatott pontok tárgyalják.'],
                        cimek=['## 10. Értelmezés', '## 11. Módszertan', '### ⚠️ Vitatott pontok'])
        s = uj_sorok(ell, 'belső utalás')
        self.assertEqual(len(s), 2)
        self.assertTrue(all(P.JELENTES_JEL not in x.bizonyitek for x in s))
        self.assertIn('## 11. Módszertan', s[0].bizonyitek)

    def test_belso_utalas_nincs(self):
        ell = futtat_uj(['A föld a 11. versben áll, és a motívum hat helyen fordul elő.'],
                        cimek=['## 10. Értelmezés'])
        self.assertEqual(uj_sorok(ell, 'belső utalás'), [])

    def test_nem_donti_el(self):
        ell = futtat_uj(['**Az 1Móz 6:11: kezdet vagy ítélet.** Két olvasat áll szemben.',
                         'A lap a kérdést nem dönti el.',
                         'A fordulópont az 1Móz 6:11: a föld megtelt erőszakkal.',
                         'Az Ez 8:17 más helyről szól.'],
                        hely={0: 'teszt:5', 1: 'teszt:5', 2: 'teszt:9', 3: 'teszt:12'})
        s = uj_sorok(ell, 'nem dönti el')
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0].egyseg.szoveg, 'A lap a kérdést nem dönti el.')
        self.assertIn('1Móz 6:11', s[0].bizonyitek)             # a pont igehelye a bekezdés címéből
        self.assertIn('teszt:9', s[0].bizonyitek)               # a lap másik mondata ugyanerre a helyre
        self.assertNotIn('teszt:12', s[0].bizonyitek)

    def test_nem_donti_el_nincs(self):
        ell = futtat_uj(['A lap a kérdést a héber szöveg szerint eldönti (1Móz 6:11).'])
        self.assertEqual(uj_sorok(ell, 'nem dönti el'), [])

    def test_regi_k_szamozas_valtozatlan(self):
        # az első mondat csak új fajtát ad, a második régi kézi tételt (szám, viszonyítási alap nélkül):
        # a régi tétel kapja a K1-et, az új a K2-t
        k = kornyezet()
        ell = futtat_uj(['A lap a kérdést nem dönti el.', 'A motívum helyei közül csak ebben a két versben áll más szó.'])
        ki = P.jelentes('X-001', ell, k['adat'], None, 'teszt', ell.egysegek)
        self.assertIn('### K1 · teszt:2', ki)
        self.assertIn('### K2 ⚑ · teszt:1', ki)

    def test_kapu_jelentes_nem_hiba(self):
        d = tempfile.mkdtemp()
        try:
            mot = os.path.join(d, 'motivumok')
            os.makedirs(mot)
            with open(os.path.join(mot, 'X-001.md'), 'w', encoding='utf-8') as f:
                f.write(FORRAS + '<!-- RÉS-KEZDET: ertelmezes -->\nA kérdést l. a 12. szakasz.\n'
                        '<!-- RÉS-VÉGE: ertelmezes -->\n')
            elof = os.path.join(d, 'elof.tsv')
            with open(elof, 'w', encoding='utf-8') as f:
                f.write('id\tigehely\tgerinc_elem\tstrong\tkapcsolodas\n')
                for x in ELOF:
                    f.write('%s\t%s\t%s\t%s\t\n' % (x['id'], x['igehely'], x['gerinc_elem'], x['strong']))
            buf = io.StringIO()
            hibak = P.kapu(mot, elof, buf)
            self.assertEqual(hibak, 0)
            self.assertIn('JELENTÉS X-001', buf.getvalue())
            self.assertNotIn('**HIBA**', buf.getvalue())
        finally:
            shutil.rmtree(d)


def karoli_eleje(ref, n=7):
    """A vers Károli-szövegének első n szava (idézethez a tesztmondatban)."""
    k = kornyezet()
    return ' '.join(k['adat'].karoli_szoveg(k['adat'].versek(ref)).split()[:n])


ELOF_PAR = [
    {'id': 'X-001', 'igehely': '1Móz 6:11', 'gerinc_elem': 'H4390+H2555', 'strong': 'H2555',
     'funkcio': '🌊 diagnózis — a föld megtelik erőszakkal'},
    {'id': 'X-001', 'igehely': 'Ez 8:17', 'gerinc_elem': 'H4390+H2555', 'strong': 'H2555', 'funkcio': ''},
    {'id': 'X-001', 'igehely': '1Móz 4:14', 'gerinc_elem': 'H4390+H2555', 'strong': 'H0127', 'funkcio': ''},
]


def ell_par(mondatok, elof=None):
    k = kornyezet()
    ell = P.Ellenor('X-001', k['adat'], k['szk'], elof or ELOF_PAR, k['igeh'])
    ell.egysegek = [P.Egyseg('rés:ertelmezes', 'teszt:%d' % (i + 1), m) for i, m in enumerate(mondatok)]
    for e in ell.egysegek:
        ell.egyseg(e)
    return ell


class F224_14(unittest.TestCase):
    """F224.14 (N-F224c): az idézettel lefedett mondat többletállítása és az igehely nélküli szabály-mondat."""

    def test_idezeten_tul(self):
        m = ('Ez a hely a törvény átkát mondja ki az egész nép előtt: „%s” (5Móz 27:15).'
             % karoli_eleje('5Móz 27:15'))
        s = uj_sorok(futtat_uj([m]), 'idézeten túl')
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0].itelet, 'kézi')
        self.assertIn('törvény átkát', s[0].bizonyitek)

    def test_csak_idezet(self):
        m = 'A vers így szól: „%s” (5Móz 27:15).' % karoli_eleje('5Móz 27:15')
        ell = futtat_uj([m])
        self.assertEqual(uj_sorok(ell, 'idézeten túl'), [])
        self.assertFalse([x for x in ell.sorok if x.itelet == 'kézi'])   # a régi viselkedés: nincs kézi tétel

    def test_szabaly_mondat(self):
        ell = ell_par(['Ide az a hely tartozik, amelyben a megtelés igéje és az erőszak szava együtt áll.'])
        s = uj_sorok(ell, 'szabály-mondat')
        self.assertEqual(len(s), 1)
        self.assertIn('H4390 → H2555: 2 hely', s[0].bizonyitek)
        self.assertIn('nem áll mind a versben (H4390+H2555): 1Móz 4:14', s[0].bizonyitek)
        self.assertEqual(s[0].jelzes, '⚑')

    def test_szabaly_igehellyel_vagy_nelkule(self):
        self.assertEqual(uj_sorok(ell_par(['Ide az a hely tartozik, amely a föld megtelését mondja (1Móz 6:11).']),
                                  'szabály-mondat'), [])
        self.assertEqual(uj_sorok(ell_par(['A föld megtelése a lánc közepén áll.']), 'szabály-mondat'), [])

    def test_k_szamozas_szintek(self):
        """A régi fajta előbb kap számot, az F224.14 fajtája a végén, akkor is, ha előbb áll."""
        ell = ell_par(['Ide az a hely tartozik, amelyben a megtelés igéje és az erőszak szava együtt áll.',
                       'A föld szava mindig a lánc közepén áll (1Móz 6:11).'])
        k = kornyezet()
        szoveg = P.jelentes('X-001', ell, k['adat'], None, 'teszt', ell.egysegek)
        self.assertRegex(szoveg, r'### K1[ ·][^\n]*teszt:2')
        self.assertRegex(szoveg, r'### K2[ ·][^\n]*teszt:1')


class F224_15(unittest.TestCase):
    """F224.15: a mondaton kívüli adat a K-tétel alatt (funkció-mező, szótári besorolás, tükörfordítás, a lap más
    mondata ugyanarról a forrásról, Targum)."""

    def test_funkcio_csak_a_sajat_tetelnel(self):
        """N-F224f: a funkció-mező a hely saját adatsor-tételénél (kapcsolodas) a K része, a rés mondata alól kimarad."""
        ell = ell_par(['x'])
        sajat = P.Egyseg('adat:kapcsolodas', 'elofordulasok.tsv:2', 'A föld itt megtelik.', alap_ref='1Móz 6:11')
        kont = ell.kontextus(sajat, ['1Móz 6:11'])
        self.assertTrue(any(x.startswith('Funkció-mező') and 'diagnózis' in x for x in kont))
        res = P.Egyseg('rés:ertelmezes', 'teszt:1', 'A föld itt megtelik erőszakkal (1Móz 6:11).')
        self.assertFalse([x for x in ell.kontextus(res, ['1Móz 6:11']) if x.startswith('Funkció-mező')])
        masik = P.Egyseg('adat:kapcsolodas', 'elofordulasok.tsv:3', 'Ez a hely az 1Móz 6:11-re utal.', alap_ref='Ez 8:17')
        self.assertFalse([x for x in ell.kontextus(masik, ['Ez 8:17', '1Móz 6:11']) if 'diagnózis' in x])

    def test_funkcio_es_tukor(self):
        e = P.Egyseg('rés:ertelmezes', 'teszt:1', 'A föld itt megtelik erőszakkal (1Móz 6:11).')
        ell = ell_par([e.szoveg])
        kont = ell.kontextus(e, ['1Móz 6:11'])
        tukor = [x for x in kont if x.startswith('Angol tükörfordítás')]
        self.assertEqual(len(tukor), 1)
        self.assertIn('[', tukor[0])                       # a gerinc-szó jelölve

    def test_mas_mondat_es_targum(self):
        mondatok = ['A Targum az 1Móz 6:11-et másként adja.', 'A Targum itt is körülír (Ez 8:17).',
                    'A görög fordítás itt hű (1Móz 4:14).']
        ell = ell_par(mondatok)
        e = ell.egysegek[0]
        kont = ell.kontextus(e, ['1Móz 6:11'])
        mas = [x for x in kont if x.startswith('A lap más mondata')]
        self.assertEqual(len(mas), 1)
        self.assertIn('teszt:2', mas[0])
        self.assertTrue(any(x.startswith('Targum (') and '1Móz 6:11' in x for x in kont))

    def test_nincs_forrasnev(self):
        ell = ell_par(['A föld itt megtelik (1Móz 6:11).', 'A Targum itt is körülír (Ez 8:17).'])
        kont = ell.kontextus(ell.egysegek[0], ['1Móz 6:11'])
        self.assertFalse([x for x in kont if x.startswith(('A lap más mondata', 'Targum ('))])

    def test_szotari_besorolas(self):
        elof = [{'id': 'X-001', 'igehely': '1Móz 4:26', 'gerinc_elem': 'H7121+H8034', 'strong': 'H7121',
                 'lexikon_szotar': 'BDB', 'jelentes_szam': '2.c', 'funkcio': ''}]
        ell = ell_par(['x'], elof)
        ell.jeloltek = [{'id': 'X-001', 'igehely': 'Jer 10:25', 'dontes': 'elutasítva'}]
        e = P.Egyseg('rés:miert_fontos', 'teszt:9', 'A BDB a 2.c jelentés alá sorolja az 1Móz 4:26-ot.')
        kont = [x for x in ell.kontextus(e, ['1Móz 4:26']) if x.startswith('Szótári besorolás')]
        self.assertEqual(len(kont), 1)
        self.assertIn('BDB H7121, 2.c', kont[0])
        self.assertIn('elutasított jelölt 1 (Jer 10:25)', kont[0])

    def test_utvonal(self):
        self.assertTrue(P.utvonal_illik('Qal/2/c', '2.c'))
        self.assertFalse(P.utvonal_illik('Qal/2/c', '2'))
        self.assertTrue(P.utvonal_illik('-/1/-', '1'))
        self.assertFalse(P.utvonal_illik('tagolatlan', '2.c'))


JO_IDEZET = 'A fordulópont: „Nem átkozom meg többé a földet az emberért” (1Móz 8:21).'
ROSSZ_IDEZET = 'Az ígéret így szól: „Nem átkozom meg soha a földet az ember miatt” (1Móz 8:21).'
TANULMANY_FX = '\n'.join([
    '# 1Mózes 8:20–22 — próba-tanulmány',
    '',
    '*v1 — 2026.11.22 (próba; a changelog nem próza: „Nem átkozom meg soha a földet az ember miatt” 1Móz 8:21)*',
    '',
    '## 2. Kulcsszavak — H0127',
    '',
    JO_IDEZET,
    ROSSZ_IDEZET,
    '',
    '| Vers | Szó |',
    '|---|---|',
    '| 1Móz 8:21 | „Nem átkozom meg soha a földet az ember miatt” |',
    '',
    '```',
    'Kódblokk: „Nem átkozom meg soha a földet az ember miatt” (1Móz 8:21).',
    '```',
    '',
    '## 4/b. Igehelyenkénti jelölt blokkok',
    '',
    '<!-- IGEHELY-PÓTOLT: nem vak olvasás -->',
    '<!-- IGEHELY-BLOKK: 1Móz 8:21 | motivum: PROBA-001 | gerinc: H0127 -->',
    '- **funkció:** Az ígéret a föld újabb megátkozását zárja ki: „Nem átkozom meg soha a földet az ember miatt.”',
    '- **negatív próba:** nem — a versben a föld szava áll. Az átok kérdéséről szól.',
    '- **jelentéspont:** üres — a próbában nincs szótári pont',
    '- **vita:** üres — a versre nincs nevesíthető képviselőjű vita',
    '- **visszhang:** üres — a próbában nincs tanú',
    '- **versszámozás:** üres — a próbában nem mérve',
    '<!-- IGEHELY-BLOKK-VÉGE -->',
    '',
    '<!-- IGEHELY-BLOKK: 1Móz 8:22 | motivum: új | gerinc: — -->',
    '- **funkció:** Hiányos blokk: „Nem átkozom meg soha a földet az ember miatt.”',
    '- **negatív próba:** Hibás pont: „Nem átkozom meg soha a földet az ember miatt.”',
    '<!-- IGEHELY-BLOKK-VÉGE -->',
    '',
    '<!-- IGEHELY-BLOKK: 1Móz 8:20 | motivum: PROBA-001 -->',
    '- **funkció:** Hibás fejléc: „Nem átkozom meg soha a földet az ember miatt.”',
    '<!-- IGEHELY-BLOKK-VÉGE -->',
    '',
])
MAS_BLOKK = '\n'.join([
    '<!-- IGEHELY-BLOKK: 1Móz 8:21 | motivum: MAS-001 | gerinc: H0127 -->',
    '- **funkció:** Más motívum blokkja: „Nem átkozom meg soha a földet az ember miatt.”',
    '- **negatív próba:** üres — próba',
    '- **jelentéspont:** üres — próba',
    '- **vita:** üres — próba',
    '- **visszhang:** üres — próba',
    '- **versszámozás:** üres — próba',
    '<!-- IGEHELY-BLOKK-VÉGE -->',
    '',
])


class Tanulmany(unittest.TestCase):
    """F205 M3: a `--tanulmany` mód — a tanulmány prózája és a jelölt blokkok ugyanazokon a próbákon, fixture-ön
    (repón kívüli ideiglenes könyvtárban); a motívum-környezet a blokkok motívumaiból."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.fx = os.path.join(cls.tmp, 'Proba_8v20-22_bovitett.md')
        with open(cls.fx, 'w', encoding='utf-8', newline='\n') as f:
            f.write(TANULMANY_FX)
        cls.elof = os.path.join(cls.tmp, 'elof.tsv')
        with open(cls.elof, 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\tigehely\tgerinc_elem\tstrong\tkapcsolodas\n')
            for d in ELOF:
                f.write('\t'.join(['PROBA-001', d['igehely'], d['gerinc_elem'], d['strong'], '']) + '\n')
            f.write('\t'.join(['MAS-001', '1Móz 8:21', 'H0127', 'H0127', '']) + '\n')
        (cls.ell, cls.adat, cls.szk, cls.n, cls.idk, cls.hibak) = P.futtat_tanulmany(
            cls.fx, elof_ut=cls.elof, jelolt_ut=os.path.join(cls.tmp, 'nincs.tsv'))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _sorok(self, forras):
        return [s for s in self.ell.sorok if s.egyseg.forras == forras]

    def test_egysegek_kijelolese(self):
        egysegek, blokkok, hibak = P.tanulmany_egysegek(self.fx)
        prozai = [e for e in egysegek if e.forras == 'rés:tanulmány']
        self.assertEqual([e.szoveg for e in prozai], [JO_IDEZET, ROSSZ_IDEZET])   # changelog, tábla, kód kimarad
        self.assertTrue(all(e.fejezet_strong == 'H0127' and e.alap_ref is None for e in prozai))
        blokk = [e for e in egysegek if e.forras.startswith('rés:blokk-')]
        self.assertEqual(sorted({e.forras for e in blokk}), ['rés:blokk-funkció', 'rés:blokk-negatív_próba'])
        self.assertEqual({e.alap_ref for e in blokk}, {'1Móz 8:21', '1Móz 8:22'})   # a blokk saját verse
        self.assertEqual(len([e for e in blokk if e.forras == 'rés:blokk-negatív_próba']), 2)   # mondatonként
        # a hiányos blokk hibája jelentve (a kinyerő megáll rajta), a meglévő szövege a próbákon megy át; a hibás
        # pont és a hibás fejlécű blokk kimarad, a hibájuk jelentve
        self.assertEqual(len(blokkok), 2)
        osszes = ' '.join(hibak)
        self.assertIn('hiányzó pont', osszes)
        self.assertIn('a negatív próba alakja', osszes)
        self.assertIn('hibás IGEHELY-BLOKK fejléc', osszes)
        self.assertTrue(any('Hiányos blokk' in e.szoveg and e.alap_ref == '1Móz 8:22' for e in egysegek))
        self.assertFalse(any('Hibás pont' in e.szoveg or 'Hibás fejléc' in e.szoveg for e in egysegek))

    def test_motivum_kornyezet(self):
        self.assertEqual(self.idk, ['PROBA-001'])      # az „új” blokk nem ad motívumot
        self.assertEqual(self.ell.mid, 'PROBA-001')
        self.assertEqual({d['id'] for d in self.ell.elof}, {'PROBA-001'})

    def test_tobb_motivum(self):
        # több blokkmotívum: --motivum nélkül megáll (a számpróba alapja nem az összevont darabszám), vele a más
        # motívum blokkja kimarad
        fx2 = os.path.join(self.tmp, 'Ket_motivum_bovitett.md')
        with open(fx2, 'w', encoding='utf-8', newline='\n') as f:
            f.write(TANULMANY_FX + MAS_BLOKK)
        with self.assertRaises(P.TobbMotivum):
            P.futtat_tanulmany(fx2, elof_ut=self.elof)
        egysegek, _, _ = P.tanulmany_egysegek(fx2, 'PROBA-001')
        self.assertFalse(any('Más motívum' in e.szoveg for e in egysegek))
        self.assertTrue(any('Hiányos blokk' in e.szoveg for e in egysegek))   # az „új” blokk marad
        egysegek, _, _ = P.tanulmany_egysegek(fx2, 'MAS-001')
        self.assertTrue(any('Más motívum' in e.szoveg for e in egysegek))
        self.assertFalse(any('megátkozását zárja ki' in e.szoveg for e in egysegek))
        self.assertEqual(P.tanulmany_motivumok([{'motivum': 'ABC-001'}, {'motivum': '—'}, {'motivum': 'új'},
                                                {'motivum': 'ABC-001'}, {'motivum': 'ÁBC-002'}]), ['ABC-001', 'ÁBC-002'])

    def test_proza_ugyanazon_a_probakon(self):
        sorok = self._sorok('rés:tanulmány')
        idezet = {s.egyseg.szoveg: s.itelet for s in sorok if s.tipus == 'idézet'}
        self.assertEqual(idezet.get(JO_IDEZET), 'egyezik')
        self.assertEqual(idezet.get(ROSSZ_IDEZET), 'ELTÉR')

    def test_blokk_a_sajat_versere(self):
        sorok = [s for s in self._sorok('rés:blokk-funkció') if s.tipus == 'idézet']
        self.assertEqual(sorted(s.vers for s in sorok), ['1Móz 8:21', '1Móz 8:22'])
        self.assertTrue(all(s.itelet == 'ELTÉR' for s in sorok))

    def test_jelentes_es_cli(self):
        szoveg = P.jelentes('Proba_8v20-22_bovitett', self.ell, self.adat, None, 'teszt', self.ell.egysegek,
                            forras_leiras='a tanulmány prózája és blokkjai')
        self.assertIn('# ALLITAS Proba_8v20-22_bovitett', szoveg)
        self.assertIn('Forrás: a tanulmány prózája és blokkjai.', szoveg)
        self.assertNotIn('motivumok/', szoveg.split('## Gépi ítéletek')[0])
        regi = P.jelentes('X-001', self.ell, self.adat, None, 'teszt', self.ell.egysegek)
        self.assertIn('Forrás: `motivumok/X-001.md` értelmező rései és az `adat/elofordulasok.tsv` `kapcsolodas` '
                      'mezője (id=X-001).', regi)
        hiba = io.StringIO()
        for argv in (['X-001', '--tanulmany', self.fx], ['--tanulmany', self.fx, '--forras', 'x.md'],
                     ['X-001', '--motivum', 'X-001'], ['--kapu', '--tanulmany', self.fx]):
            regi_err, sys.stderr = sys.stderr, hiba
            try:
                with self.assertRaises(SystemExit):
                    P.main(argv)
            finally:
                sys.stderr = regi_err


ELOF_TEHOM = [{'id': 'X-002', 'igehely': r, 'gerinc_elem': 'H8415', 'strong': 'H8415'}
              for r in ('5Móz 8:7', 'Jób 38:30', 'Jób 41:32', 'Zsolt 33:7', 'Zsolt 71:20', 'Zsolt 135:6',
                        'Zsolt 148:7', 'Jón 2:6')]
VERSEK_TEHOM = [d['igehely'] for d in ELOF_TEHOM] + ['Jób 41:31', '2Móz 15:5']
_KORNYEZET_TEHOM = {}


def tehom_ell(mondatok, forras='rés:ertelmezes'):
    """F239 U4b: a TEREMT-001 E41-mérésének hét hozzárendelési hibája, a motívum verseivel (egy bekezdés)."""
    if not _KORNYEZET_TEHOM:
        adat = P.Adat()
        versek = set()
        for r in VERSEK_TEHOM:
            versek.update(adat.versek(r))
        adat.betolt_szavak(versek)
        adat.betolt_parok(versek)
        _KORNYEZET_TEHOM.update(adat=adat, szk=P.Szokeszlet(FORRAS, ELOF_TEHOM, adat))
    k = _KORNYEZET_TEHOM
    ell = P.Ellenor('X-002', k['adat'], k['szk'], ELOF_TEHOM, P.Igehelyek())
    ell.egysegek = [P.Egyseg(forras, 'teszt:1', m) for m in mondatok]
    for e in ell.egysegek:
        ell.egyseg(e)
    return ell


class F239_U4b(unittest.TestCase):
    """F239 U4b (E41): a TEREMT-001 nyolc ELTÉR-sorából hét az eszköz hozzárendelési hibája volt."""

    def test_konyv_nelkuli_versszam(self):
        ig = P.Igehelyek()
        refek = [r for _, _, rs in ig.csoportok('a Jób 41:31 helyén a mecólá áll, a 41:32-ben a tehóm') for r in rs]
        self.assertEqual(refek, ['Jób 41:31', 'Jób 41:32'])
        # könyves igehely nélkül (a mondat elején) nem igehely
        self.assertEqual(ig.csoportok('Jónás imájában a 2:4 mondata más szó'), [])

    def test_idezet_a_konyv_nelkuli_versbol(self):
        ell = tehom_ell(['A Jób 41:31 helyén a mecólá áll, a 41:32-ben a tehóm, amelyet a Károli „tenger”-nek '
                         'fordít: „azt hinné valaki, a tenger megőszült”.'])
        self.assertIn(('Jób 41:32', 'egyezik'), iteletek(ell.sorok, 'idézet'))
        self.assertFalse([s for s in ell.sorok if s.tipus == 'idézet' and s.itelet == 'ELTÉR'])

    def test_szo_glossza_zarojelben(self):
        for t, vart in (('a büthosz (βυθός, „a tenger mélye”) a mecólát', True),
                        ('a vers (Zsolt 33:7, „a tenger mélye”)', False)):
            self.assertEqual(P.szo_glossza(t, t.index('„')), vart)
        ell = tehom_ell(['A 2Móz 15:5 görög szövegében álló büthosz (βυθός, „a tenger mélye”) a mecólát fordítja.'])
        self.assertFalse([s for s in ell.sorok if s.tipus == 'idézet'])

    def test_fordulat_mas_szot_fordit(self):
        # a Jób 41:31-ben a „mély vizet” a mecólá: a mondat épp ezt mondja — kézi ⚑, nem ELTÉR
        ell = tehom_ell(['A Jób 41:31 „mély vizet” mondó helyén a mecólá áll.'])
        sorok = uj_sorok(ell, 'fordulat')
        self.assertTrue(sorok)
        self.assertEqual({s.itelet for s in sorok}, {'kézi'})
        self.assertIn('H4688', sorok[0].bizonyitek)

    def test_fordulat_ragos_felsorolas(self):
        ell = tehom_ell(['Az 5Móz 8:7-ben, a Jób 38:30-ban és a Zsolt 148:7-ben „mély vizek”, a Jób 41:32-ben pedig '
                         '„tenger” áll.'])
        it = iteletek(ell.sorok, 'fordulat')
        self.assertNotIn(('Jób 41:32', 'ELTÉR'), it)
        self.assertIn(('Zsolt 148:7', 'egyezik'), it)

    def test_fordulat_zarojeles_csoport(self):
        ell = tehom_ell(['Isten tárházakba rakja a mélység vizét (Zsolt 33:7), és „minden mélységben” megteszi, amit '
                         'akar (Zsolt 135:6).'])
        it = iteletek(ell.sorok, 'fordulat')
        self.assertEqual(it, {('Zsolt 135:6', 'egyezik')})

    def test_szam_heber_versei(self):
        ell = tehom_ell(['A Károli a tehómot a motívum 8 héber versének többségében a mélység szavával adja.'])
        self.assertEqual([(s.itelet, 'ószövetségi' in s.bizonyitek) for s in uj_sorok(ell, 'szám')],
                         [('egyezik', True)])

    def test_szam_reszhalmaz_felsorolassal(self):
        ell = tehom_ell(['A mélység a motívum két ószövetségi helyén a halál közelsége.',
                         'Jónást „mély ár kerített be” (Jón 2:6), a zsoltáros szerint Isten felhoz (Zsolt 71:20).'])
        sz = uj_sorok(ell, 'szám')
        self.assertEqual([s.itelet for s in sz], ['kézi'])
        # felsorolás nélkül a szám továbbra is a csoport egészére szól: ELTÉR
        sz = uj_sorok(tehom_ell(['A mélység a motívum két ószövetségi helyén a halál közelsége.']), 'szám')
        self.assertEqual([s.itelet for s in sz], ['ELTÉR'])


class Lektor(unittest.TestCase):
    def test_pontossagi(self):
        self.assertTrue(P.lektor_pontossagi({'gond': '1. kérdés (az igehely maga). A versben …'}))
        self.assertTrue(P.lektor_pontossagi({'gond': '4. és 2. kérdés. A bizonyosság indoka …'}))
        self.assertTrue(P.lektor_pontossagi({'gond': '2. és 4. kérdés. A …'}))
        self.assertFalse(P.lektor_pontossagi({'gond': '3. kérdés (műhelyszagú fordulat).'}))
        self.assertFalse(P.lektor_pontossagi({'gond': 'műhelyszagú fordulat az olvasói szövegben'}))


if __name__ == '__main__':
    unittest.main(verbosity=1)
