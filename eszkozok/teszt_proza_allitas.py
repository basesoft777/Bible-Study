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


class Lektor(unittest.TestCase):
    def test_pontossagi(self):
        self.assertTrue(P.lektor_pontossagi({'gond': '1. kérdés (az igehely maga). A versben …'}))
        self.assertTrue(P.lektor_pontossagi({'gond': '4. és 2. kérdés. A bizonyosság indoka …'}))
        self.assertTrue(P.lektor_pontossagi({'gond': '2. és 4. kérdés. A …'}))
        self.assertFalse(P.lektor_pontossagi({'gond': '3. kérdés (műhelyszagú fordulat).'}))
        self.assertFalse(P.lektor_pontossagi({'gond': 'műhelyszagú fordulat az olvasói szövegben'}))


if __name__ == '__main__':
    unittest.main(verbosity=1)
