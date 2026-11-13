"""Az S1 szelet tesztjei: „2. Előfordulások” és „2.1 Az igehelyek szövege” (GK-13, GK-14, GK-17, GK-25, HN-01,
HN-16), a sablonmódosítók és a jegyzet-összevonás egységtesztjei.

A valós adaton futó tesztek a két mintalapot generálják (egyszer, a modul szintjén gyorsítótárazva)."""
import ast
import datetime
import re
import unicodedata
import unittest

import kozos
from kozos import MINTALAPOK, fa, kodfajlok, szovegliteralok
from lapgen import bemenet, fo
from lapgen.bemenet import gerinc as gerinc_be
from lapgen.bemenet import szavak
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szoveg import (Fajta, Forrasszoveg, Igehely, Kezi, MotivumId, SablonHiba, SablonSor, Strong, idezet,
                           kiiras, proza, sablon)

DATUM = datetime.date(2026, 11, 13)
_LAPOK = {}


def lap(azonosito):
    """A mintalap kész sorai (nézet: TUDOMANYOS), futásonként egyszer generálva."""
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM).nezetek['TUDOMANYOS']
    return _LAPOK[azonosito]


def lathato(sor):
    """A sor látható szövege: a megjegyzés-tartományok nélkül."""
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


def _sor(mondat, parameterek='-'):
    return SablonSor('teszt', mondat, parameterek)


def nfc(szoveg):
    return unicodedata.normalize('NFC', szoveg)


def _q(szoveg):
    return idezet(Forrasszoveg(szoveg, 'm', 'B', None))


class Modositok(unittest.TestCase):
    def test_a_cella_modosito_megszunt(self):
        """A cellakezdő alak nem a sablonmondat dolga (az is csere volna): `cella` módosító nincs."""
        with self.assertRaises(SablonHiba):
            sablon(_sor('{t|cella}', 't:lathato'), t=_q('a föld'))

    def test_a_sablon_a_prozat_es_az_idezetet_valtozatlanul_adja(self):
        """A sablonmondat a látható paraméterét nem írja át: a névelő-módosító csak sablonszöveget tesz elé."""
        for modosito in ('', '|a', '|A'):
            s = _sor('x {t%s} y' % modosito, 't:lathato')
            for ertek in (proza(Kezi('az átok', 'm')), _q('a föld színe'), _q('A megművelt föld')):
                kiirt = kiiras(sablon(s, t=ertek))
                self.assertEqual([kiirt.szoveg[k:v] for k, v, f in kiirt.tartomanyok if f is not Fajta.SABLON],
                                 [kiiras(ertek).szoveg])

    def test_a_cimke_cellakezdo_alakja_adat(self):
        """A címke cellakezdő alakja a névtábla `cimke_cella` sora (kézi adat); híján maga a címke áll."""
        g = gerinc_be.gerinc(bemenet.Bemenet(kozos.GYOKER))
        kulcs = ('BDB109', '-/1/-')
        self.assertEqual(g.cimke('BDB', 'H0127', kulcs).ertek, 'a megművelt föld, amely táplál')
        self.assertEqual(g.cimke_cella('BDB', 'H0127', kulcs).ertek, 'A megművelt föld, amely táplál')
        self.assertIsInstance(g.cimke_cella('BDB', 'H0127', kulcs), Kezi)
        mas = ('BDB7550', 'Qal/2/c')
        self.assertEqual(g.cimke_cella('BDB', 'H7121', mas), g.cimke('BDB', 'H7121', mas))

    def test_a_cellakezdo_alak_csak_a_cimke_alakja_lehet(self):
        """Kapu: a cellakezdő alak a címkétől csak a kezdő névelőben és a kezdőbetűben térhet el."""
        egyezik = gerinc_be._cella_alak_egyezik
        self.assertTrue(egyezik('a megművelt föld, amely táplál', 'A megművelt föld, amely táplál'))
        self.assertTrue(egyezik('az átok', 'Átok'))
        self.assertFalse(egyezik('az átok', 'Áldás'))
        self.assertFalse(egyezik('az átok', 'az átok'))
        self.assertFalse(egyezik('a megművelt föld', 'A megművelt föld, amely táplál'))

    def test_a_tabla_cellai_cellakezdo_alakban_allnak(self):
        """A HAMART-001 2. táblájában a jelentéscella a címke adatbeli cellakezdő alakjával, illetve a cellakezdő
        sablonmondattal kezdődik; a szöveg közepén a címke saját alakja áll."""
        cellak = [lathato(sor).split(' | ')[2] for sor in lap('HAMART-001') if sor.szoveg.startswith('| [')]
        self.assertTrue(any(c.startswith('A megművelt föld, amely táplál · 1') for c in cellak))
        self.assertTrue(any(c.startswith('Szócikk egésze — ') for c in cellak))
        self.assertFalse([c for c in cellak if re.match(r'(a|az) ', c)])

    def test_nevelo_a_masik_parameter_szerint(self):
        """A görög szó névelője a kiejtés szerint áll (`a:kiejtes`)."""
        s = _sor('{szo|a:kiejtes} ({kiejtes})', 'szo:lathato, kiejtes:lathato')
        self.assertEqual(kiiras(sablon(s, szo=_q('κατάθεμα'), kiejtes=_q('katathema'))).szoveg,
                         'a κατάθεμα (katathema)')
        self.assertEqual(kiiras(sablon(s, szo=_q('ἐπικατάρατος'), kiejtes=_q('epikataratosz'))).szoveg,
                         'az ἐπικατάρατος (epikataratosz)')


class Kiejtes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = bemenet.Bemenet(kozos.GYOKER)
        cls.kiejtes = szavak.kiejtes(cls.b)

    def _szo(self, vers, strong, karoli_szo=None):
        szo = Forrasszoveg(karoli_szo, 'karoli_szo', 'B03', Igehely(vers)) if karoli_szo else None
        return self.kiejtes.ragozott((Igehely(vers),), Strong(strong), szo)

    def test_gk13_egy_kiejtesi_ut(self):
        """GK-13: a kiejtés egy szolgáltatásból jön: a kiejtés-modulokat csak a `bemenet/szavak.py` importálja."""
        hibak = []
        for rel in kodfajlok():
            if rel == 'bemenet/szavak.py':
                continue
            for csomo in ast.walk(fa(rel)):
                nevek = []
                if isinstance(csomo, ast.Import):
                    nevek = [n.name for n in csomo.names]
                elif isinstance(csomo, ast.ImportFrom):
                    nevek = [csomo.module or '']
                hibak.extend('%s:%d %s' % (rel, csomo.lineno, n) for n in nevek
                             if n.split('.')[0] in ('kiejtes', 'heber_kiejtes', 'kiejtes_szoveg'))
        self.assertEqual(hibak, [])

    def test_gk13_heber_es_gorog_alak_kiejtese(self):
        """GK-13: a ragozott alak kiejtése a két mintalap ismert sorain (H7121, H2403, G1944)."""
        self.assertEqual(self._szo('1Móz 12:8', 'H7121').kiejtes.ertek, 'vajjikrá')
        self.assertEqual(self._szo('1Móz 4:7', 'H2403').kiejtes.ertek, 'chattát')
        gorog = self._szo('Gal 3:13', 'G1944')
        self.assertEqual((nfc(gorog.alak.ertek), gorog.kiejtes.ertek), (nfc('ἐπικατάρατος'), 'epikataratosz'))

    def test_gk14_ismetlodesnel_a_karoli_szohoz_kotott_alak(self):
        """GK-14 (T4, a módosított döntés): ha a Strong-szám többször áll a versben, az az alak számít, amelyhez
        a sor Károli-szava a párosításban kötődik."""
        self.assertEqual(self.kiejtes.token_szam(Igehely('1Móz 6:5'), Strong('H7451')), 2)
        self.assertEqual(nfc(self._szo('1Móz 6:5', 'H7451', 'gonosz').alak.ertek), nfc('רַ֖ע'))
        self.assertEqual(nfc(self._szo('1Móz 6:5', 'H7451', 'gonoszsága').alak.ertek), nfc('רָעַ֥ת'))
        self.assertEqual(nfc(self._szo('1Móz 6:12', 'H7843', 'megrontotta').alak.ertek), nfc('הִשְׁחִ֧ית'))
        self.assertEqual(nfc(self._szo('Jel 11:18', 'G1311', 'pusztítják').alak.ertek), nfc('διαφθείροντας'))

    def test_gk14_parositas_hijan_az_elso_elofordulas(self):
        """GK-14 (T4): ha a Károli-szóhoz nincs pár (vagy a sornak nincs Károli-szava), az első előfordulás áll,
        a vers szövegrendje szerint."""
        self.assertEqual(nfc(self._szo('1Móz 6:5', 'H7451').alak.ertek), nfc('רָעַ֥ת'))
        self.assertEqual(nfc(self._szo('1Móz 6:5', 'H7451', 'nincs ilyen szó a versben').alak.ertek), nfc('רָעַ֥ת'))
        self.assertEqual(nfc(self._szo('1Móz 6:12', 'H7843').alak.ertek), nfc('נִשְׁחָ֑תָה'))
        self.assertEqual(nfc(self._szo('Jel 11:18', 'G1311').alak.ertek), nfc('διαφθεῖραι'))

    def test_gk14_a_par_csak_egyezo_alakkal_ervenyes(self):
        """A pár sorszáma csak akkor dönt, ha azon a helyen ez a Strong-szám és a pár eredeti alakja áll; a nem
        párosított könyv (nincs fájlja) kimondott hiány: üres válasz, nem hiba. Ha a Károli-szó egy szava
        többször áll a versben, az összefüggő szókapcsolat párja számít."""
        parok = szavak.b54_karoli_parok(self.b)
        self.assertEqual([n for n, _alak in parok.kotott('1Móz 6:5', 'H7451', 'gonosz')], [18])
        self.assertEqual(parok.kotott('1Móz 6:5', 'H7451', 'föld'), [])
        self.assertEqual([n for n, _alak in parok.kotott('1Móz 4:26', 'H8034', 'nevét')], [11, 19])
        self.assertEqual([n for n, _alak in parok.kotott('1Móz 4:26', 'H8034', 'segítségül hívni az Úrnak nevét')],
                         [19])
        self.assertEqual(parok.kotott('Nincs 1:1', 'H7451', 'gonosz'), [])
        sorok = (('H7451', 'más alak', ''),) * 18
        self.assertIsNone(self.kiejtes._kotott_hely(
            sorok, Igehely('1Móz 6:5'), Strong('H7451'), Forrasszoveg('gonosz', 'karoli_szo', 'B03', None)))

    def test_gk14_tartomanynal_az_elso_vers_amelyben_a_szo_all(self):
        szo = self.kiejtes.ragozott((Igehely('Gal 3:13'), Igehely('Gal 3:14')), Strong('G1944'))
        self.assertEqual(szo.alak.hely, Igehely('Gal 3:13'))
        self.assertIsNone(self._szo('1Móz 1:1', 'H7451'))


class Konyvnev(unittest.TestCase):
    def test_gk17_nincs_kodba_irt_konyvnev(self):
        """GK-17: könyvnév csak a normalizáló táblából jön: a lapgen kódjában (a tesztek kivételével) egyetlen
        szövegliterál sem azonos a tábla valamelyik könyvrövidítésével vagy teljes könyvnevével."""
        b = bemenet.Bemenet(kozos.GYOKER)
        tabla = b._tabla('B63')
        nevek = set()
        for sor in tabla.sorok:
            nevek.update(m for m in sor[1:3] if m)
        hibak = []
        for rel in kodfajlok():
            hibak.extend('%s:%d %r' % (rel, n, ertek) for n, ertek in szovegliteralok(rel) if ertek in nevek)
        self.assertEqual(hibak, [])

    def test_gk17_ismeretlen_konyv_bukas(self):
        konyvek = bemenet.b63_konyvek(bemenet.Bemenet(kozos.GYOKER))
        self.assertTrue(konyvek.ujszovetsegi('Jel'))
        self.assertFalse(konyvek.ujszovetsegi('1Móz'))
        with self.assertRaises(bemenet.BemenetHiba):
            konyvek.igehely('Eféz 2:1')


class Szerkezet(unittest.TestCase):
    """GK-25 és a HN-minták a két generált mintalap 2. szakaszán."""

    def _szakasz(self, azonosito):
        sorok = lap(azonosito)
        kezd = next(i for i, s in enumerate(sorok) if s.szoveg.startswith('## 2. '))
        return sorok[kezd:]

    def test_gk25_minden_igehely_alatt_proza_es_funkcio(self):
        """GK-25: a 2.1 pontban minden igehely alatt áll a vers szövege, teljes mondatú próza és „Funkció:” sor."""
        for azonosito in MINTALAPOK:
            sorok = [lathato(s) for s in self._szakasz(azonosito)]
            horgonyok = [i for i, s in enumerate(self._szakasz(azonosito)) if s.szoveg.startswith('<a id="ige-')]
            self.assertTrue(horgonyok, azonosito)
            for i in horgonyok:
                tetel = []
                for s in sorok[i + 1:]:
                    if s.startswith('<a id="ige-') or s.startswith('## '):
                        break
                    tetel.append(s)
                nem_ures = [s for s in tetel if s]
                self.assertRegex(nem_ures[0], r'^\*\*.+\*\*$')
                self.assertRegex(nem_ures[1], r'^\*.+\*$')
                self.assertTrue(nem_ures[-1].startswith('Funkció: '), '%s: %s' % (azonosito, nem_ures[0]))
                proza_sorok = [s for s in nem_ures[2:-1] if not re.match(r'^\*.+\*$', s)]
                self.assertEqual(len(proza_sorok), 1, '%s: %s' % (azonosito, nem_ures[0]))
                self.assertRegex(proza_sorok[0], r'[.!?”)]$')

    def test_gk25_a_jegyzet_a_tabla_alatt_all_rovid_es_egysoros(self):
        """GK-25: a táblajegyzetek közvetlenül a tábla alatt állnak, egy sorban, röviden; minden jegyzetre
        hivatkozik táblasor, és minden hivatkozásnak van jegyzete."""
        for azonosito in MINTALAPOK:
            szakasz = self._szakasz(azonosito)
            sorok = [s.szoveg for s in szakasz]
            utolso_tablasor = max(i for i, s in enumerate(sorok) if s.startswith('| ['))
            self.assertEqual(sorok[utolso_tablasor + 1], '')
            jegyzetek = []
            for s in szakasz[utolso_tablasor + 2:]:
                if not s.szoveg.startswith('- <span class="lj-szam"'):
                    break
                jegyzetek.append(s)
            self.assertTrue(jegyzetek, azonosito)
            hivatkozott = set(re.findall(r'href="#(j-2-\d+)"', '\n'.join(sorok[:utolso_tablasor + 1])))
            sajat = {re.search(r'id="(j-2-\d+)"', s.szoveg).group(1) for s in jegyzetek}
            self.assertEqual(hivatkozott, sajat, azonosito)
            for s in jegyzetek:
                szoveg = re.sub(r'<[^>]+>[\d.]*</span>', '', lathato(s), count=1)[2:]
                self.assertLessEqual(len(szoveg), 260, szoveg)
                self.assertRegex(szoveg, r'^[A-ZÁÉÍÓÖŐÚÜŰ].*\.$')

    def test_hn01_a_jegyzet_nem_ismetli_a_cellat(self):
        """HN-01: a tábla alatti jegyzet nem a rá hivatkozó cella szövegét ismétli (a jegyzet nem azonos a
        cellával, és nem tartalmazza a teljes jelentés-cellát)."""
        for azonosito in MINTALAPOK:
            szakasz = [lathato(s) for s in self._szakasz(azonosito)]
            jegyzet = {}
            for s in szakasz:
                m = re.match(r'^- <span class="lj-szam" id="(j-2-\d+)">[\d.]+</span>(.*)$', s)
                if m:
                    jegyzet[m.group(1)] = m.group(2)
            for s in szakasz:
                if not s.startswith('| ['):
                    continue
                cellak = [c.strip() for c in s.strip('|').split(' | ')]
                for m in re.finditer(r'href="#(j-2-\d+)"', cellak[2]):
                    cella = re.sub(r'<sup.*?</sup>', '', cellak[2]).strip()
                    self.assertNotIn(cella, jegyzet[m.group(1)], '%s: %s' % (azonosito, cellak[0]))

    def test_hn16_a_tematikus_hely_sajat_szava_adatbol_jon(self):
        """HN-16: a tematikus hely saját szava a kézi táblából (B67) jön, nem kódba írt kivételből: a sor a
        tábla Strong-számát mutatja, és a szó a lánc szavai között nem áll."""
        b = bemenet.Bemenet(kozos.GYOKER)
        for azonosito in MINTALAPOK:
            sajat = bemenet.elofordulas.b67_sajat_szavak(b, MotivumId(azonosito))
            sorok = bemenet.b03_elofordulasok(b, MotivumId(azonosito))
            lanc = {s for sor in sorok for s in sor.strongok}
            for hely, strong in sajat.items():
                self.assertNotIn(strong, lanc)
                tablasor = next(lathato(s) for s in lap(azonosito) if s.szoveg.startswith('| [%s](' % hely))
                cellak = [c.strip() for c in tablasor.strip('|').split(' | ')]
                self.assertEqual(cellak[5], strong.kod)
                self.assertEqual(cellak[2], 'tematikus hely: a lánc szava nélkül')

    def test_a_proveniencia_csak_megjegyzesben_all(self):
        """A 2. szakasz látható szövegében nincs proveniencia-hármas, közös forrásjel, fájlnév vagy döntésszám."""
        minta = re.compile(r'scope=|forras=|‹E\d+›|\.tsv\b|\.py\b|\bDT-?F?\d+|proveniencia|jelentés-címke')
        for azonosito in MINTALAPOK:
            for s in self._szakasz(azonosito):
                self.assertIsNone(minta.search(lathato(s)), '%s: %s' % (azonosito, lathato(s)[:120]))


class SzakaszJelek(unittest.TestCase):
    """A 2. független ellenőrzés 1. tétele: belső mezőből látható szöveg nem képződik; a több szócikk egyikét a
    szótár saját jelölése nevezi meg, belső azonosító nélkül."""

    @classmethod
    def setUpClass(cls):
        cls.b = bemenet.Bemenet(kozos.GYOKER)
        cls.g = gerinc_be.gerinc(cls.b)
        cls.ny = bemenet.nyelv(cls.b)

    def _latszik(self, szotar, strong, kulcs, prozai=False):
        from lapgen.megjelenites.md import elofordulas as md
        from lapgen.szamitas import szotari_gerinc
        return kiiras(md._szakaszjel(self.ny, szotari_gerinc._szakaszjel(self.g, szotar, strong, kulcs, prozai)))

    def test_a_tartomany_kezdo_verse_igehely(self):
        """A verstartomány kezdő verse a bemeneti rétegben képzett igehely (nem belső szöveg), a Thayer-példa
        jelentésszáma a bemeneti rétegben képzett szám (nem belső kulcs): a típus egyezik a használattal."""
        tartomanyok = self.g.tartomanyban('H8034', '1Kir 18:25')
        self.assertTrue(tartomanyok)
        self.assertEqual([(type(t.kezdo_vers), t.kezdo_vers.kod, t.veg) for t in tartomanyok],
                         [(Igehely, '1Kir 18:24', 25)])
        peldak = [p for kulcs in list(self.g._th_vj)[:400] for p in self.g.thayer_peldak(kulcs[0], [kulcs[1]])]
        self.assertTrue(any(p.jelentesszam is not None for p in peldak))
        for p in peldak:
            if p.jel.ertek.isdigit():
                self.assertEqual(p.jelentesszam, int(p.jel.ertek))
            else:
                self.assertIsNone(p.jelentesszam)

    def test_a_szamitas_nem_bont_ki_belso_erteket_lathato_szovegge(self):
        """Statikus őr: a `szamitas/` rétegben a burkoló `ertek` mezőjéből nem képződik szám és igehely (`int(…
        .ertek)`, `igehely(… .ertek)`): ilyen érték a bemeneti rétegből jön, a saját típusában."""
        hibak = []
        for rel in kodfajlok('szamitas'):
            for csomo in ast.walk(fa(rel)):
                if not isinstance(csomo, ast.Call):
                    continue
                nev = csomo.func.id if isinstance(csomo.func, ast.Name) else getattr(csomo.func, 'attr', '')
                if nev in ('int', 'float', 'igehely', 'Igehely', 'Strong', 'vers_igehely') and any(
                        isinstance(a, ast.Attribute) and a.attr == 'ertek' for arg in csomo.args
                        for a in ast.walk(arg)):
                    hibak.append('%s:%d %s(… .ertek)' % (rel, csomo.lineno, nev))
        self.assertEqual(hibak, [])

    def test_a_szocikk_megnevezese_a_szotar_sajat_jelolese(self):
        """Ha a szakasz jele a szó több szócikkében is áll, a jel mellett a szótár saját címszava áll a
        homográf-számával, szó szerinti idézetként; a jel maga csak a szócikken belüli tagolás."""
        kulcs = ('BDB8033', '-/1/-')
        szocikk = self.g.jel_szocikke('BDB', 'H7451', kulcs)
        self.assertEqual((nfc(szocikk.cimszo.ertek), szocikk.sorszam), (nfc('II. רַע'), 2))
        self.assertIsInstance(szocikk.cimszo, Forrasszoveg)
        self.assertEqual(self.g.jel('BDB', 'H7451', kulcs).ertek, '1')
        kiirt = self._latszik('BDB', 'H7451', kulcs)
        self.assertEqual(nfc(kiirt.szoveg), nfc('1 (II. רַע)'))
        self.assertEqual([f for _k, _v, f in kiirt.tartomanyok],
                         [Fajta.IDEZET, Fajta.SABLON, Fajta.IDEZET, Fajta.SABLON])
        # egy szócikkes szónál és a szócikken belül egyértelmű jelnél nincs megnevezés
        self.assertIsNone(self.g.jel_szocikke('BDB', 'H0127', ('BDB109', '-/1/-')))
        self.assertEqual(self._latszik('BDB', 'H0127', ('BDB109', '-/1/-'), prozai=True).szoveg, '1.')

    def test_homograf_szam_hijan_a_szocikk_sorszama_all(self):
        """Ha a szótár jelölése a szócikket nem különbözteti meg (a címszó másik szócikké is, és nincs
        homográf-szám), a megnevezés sablonmondat a szótár nevével és a szócikk sorszámával."""
        elso, masodik = ('BDB8035', 'Qal/1/-'), ('BDB8036', 'Qal/-/-')
        self.assertIsNone(self.g.jel_szocikke('BDB', 'H7489', elso).cimszo)
        self.assertEqual(self.g.jel_szocikke('BDB', 'H7489', elso).sorszam, 1)
        self.assertEqual(self._latszik('BDB', 'H7489', elso).szoveg, 'Qal 1 (a BDB 1. szócikke)')
        self.assertEqual(nfc(self._latszik('BDB', 'H7489', masodik).szoveg), nfc('Qal (II. [רָעַע])'))

    def test_belso_szocikk_azonosito_nem_all_a_lathato_jelben(self):
        """A több szócikkes szavak minden szakaszjelén: a látható alakban nincs belső szócikk-azonosító (a belső
        alak, amely megjegyzésbe kerül, tartalmazza)."""
        azonosito = re.compile(r'BDB\d+')
        vizsgalt = 0
        for strong in ('H7451', 'H7489', 'H0068', 'H8034', 'H0001'):
            for r in self.g._bdb_sz.get(strong, []):
                kulcs = (r['bdb_id'], r['utvonal'])
                if r['utvonal'] in ('fej', 'cim') or self.g.jel_szocikke('BDB', strong, kulcs) is None:
                    continue
                vizsgalt += 1
                self.assertIsNotNone(azonosito.search(self.g.kulcs_jel('BDB', strong, kulcs)))
                for prozai in (False, True):
                    self.assertIsNone(azonosito.search(self._latszik('BDB', strong, kulcs, prozai).szoveg))
        self.assertGreater(vizsgalt, 10)

    def test_a_mintalapokon_nincs_belso_szocikk_azonosito(self):
        for azonosito in MINTALAPOK:
            for sor in lap(azonosito):
                self.assertIsNone(re.search(r'BDB\d+', lathato(sor)), '%s: %s' % (azonosito, lathato(sor)[:100]))


class JegyzetOsszevonas(unittest.TestCase):
    def test_azonos_mondatu_jegyzet_egyszer_all(self):
        """Az azonos látható mondatú jegyzet egyszer áll; a számozás az első hivatkozás sorrendje; a sor végén
        minden eredeti lábjegyzet megjegyzésként áll."""
        sorok = [s for s in lap('HAMART-001') if s.szoveg.startswith('- <span class="lj-szam" id="j-2-')]
        szamok = [int(re.search(r'id="j-2-(\d+)"', s.szoveg).group(1)) for s in sorok]
        self.assertEqual(szamok, list(range(1, len(sorok) + 1)))
        mondatok = [lathato(s) for s in sorok]
        self.assertEqual(len(set(mondatok)), len(mondatok))
        eredetik = sum(s.szoveg.count('<!-- eredeti: [^') for s in sorok)
        tablasorok = [s for s in lap('HAMART-001') if s.szoveg.startswith('| [') and 'href="#j-2-' in s.szoveg]
        self.assertEqual(eredetik, len(tablasorok))

    def test_kozos_forrasmegjeloles_megjegyzesben(self):
        sorok = [s for s in lap('HAMART-001') if s.szoveg.startswith('<!-- közös forrásmegjelölés: ')]
        self.assertEqual(len(sorok), 1)
        self.assertEqual(lathato(sorok[0]), '')
        self.assertIn('‹E1› = forrás: kézi szerkesztés, ', sorok[0].szoveg)


if __name__ == '__main__':
    unittest.main(verbosity=1)
