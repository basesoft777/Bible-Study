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
from lapgen.bemenet import szavak
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szoveg import (Fajta, Forrasszoveg, Igehely, Kezi, MotivumId, SablonSor, Strong, idezet, kiiras, proza,
                           sablon)

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
    def test_cellakezdet_rovid_elem_nevelo_nelkul(self):
        """A cellakezdő alak: a rövid elem eleji névelő elmarad, az elem nagy kezdőbetűt kap."""
        s = _sor('{t|cella}', 't:lathato')
        self.assertEqual(kiiras(sablon(s, t=sablon(_sor('a szócikk egésze — {g}', 'g:lathato'),
                                                    g=_q('fájdalom, fáradság')))).szoveg,
                         'Szócikk egésze — fájdalom, fáradság')
        self.assertEqual(kiiras(sablon(s, t=proza(Kezi('az átok', 'm')))).szoveg, 'Átok')

    def test_cellakezdet_mondat_erteku_elem_megtartja_a_nevelot(self):
        """Hat vagy több szónál a névelő marad, nagy kezdőbetűvel; a fajta-térkép megmarad."""
        s = _sor('{t|cella}', 't:lathato')
        belso = sablon(_sor('{c} · {j}', 'c:lathato, j:lathato'), c=proza(Kezi('a megművelt föld, amely táplál', 'm')),
                       j=_q('1'))
        kiirt = kiiras(sablon(s, t=belso))
        self.assertEqual(kiirt.szoveg, 'A megművelt föld, amely táplál · 1')
        self.assertEqual(kiirt.tartomanyok[0][2], Fajta.PROZA)
        self.assertEqual(kiirt.tartomanyok[-1][2], Fajta.IDEZET)

    def test_cellakezdet_mas_elem_valtozatlan(self):
        s = _sor('{t|cella}', 't:lathato')
        for szoveg in ('átkoz, átkozott · Qal', 'A föld', 'azonos szó', '—', 'a', '[1Móz 3:14](#ige-1móz-3-14)'):
            self.assertEqual(kiiras(sablon(s, t=_q(szoveg))).szoveg, szoveg)

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
