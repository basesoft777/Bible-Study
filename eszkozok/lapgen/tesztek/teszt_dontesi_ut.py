"""Az S2 szelet második felének tesztjei: az „1. Döntési út” szakasz (1.1–1.5): a modell kapuja (GK-09, GK-21), a
teljesség minden keresésre (GK-04), a belső és a mellékletre mutató linkek, a kézi szöveg változatlansága, a
lemma-változat (GK-13) és az új bemenetek (B02, B10, B15, B47).

A valós adaton futó tesztek a két mintalapot generálják (a modul szintjén gyorsítótárazva)."""
import dataclasses
import datetime
import re
import unicodedata
import unittest

import kozos
from kozos import MINTALAPOK, alap_minirepo, tsv
from lapgen import bemenet, fo
from lapgen.bemenet import motivum as motivum_be
from lapgen.bemenet import szavak
from lapgen.ertekek import MaradtFajta
from lapgen.megjelenites.md.iro import MEGJEGYZES
from lapgen.szamitas import dontesi_ut, kizarasok, vizsgalat
from lapgen.szoveg import Igehely, Kezi, MotivumId, Strong

DATUM = datetime.date(2026, 11, 13)
_LAPOK, _MODELLEK = {}, {}
_J = ('igen', '-', '-', 'aktiv', '-', '-', 'manual')


def lapok(azonosito):
    if azonosito not in _LAPOK:
        _LAPOK[azonosito] = fo.lap_keszit(kozos.GYOKER, MotivumId(azonosito), datum=DATUM).nezetek
    return _LAPOK[azonosito]


def modell(azonosito):
    if azonosito not in _MODELLEK:
        korny = fo.Kornyezet(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA)
        _MODELLEK[azonosito] = dontesi_ut.szamit(korny)
    return _MODELLEK[azonosito]


def lathato(sor):
    return ''.join(sor.szoveg[k:v] for k, v, f in sor.tartomanyok if f != MEGJEGYZES)


def szakasz(azonosito):
    """A Döntési út sorai a tudományos nézetben (a címsortól a következő 2. szintű címsorig)."""
    sorok = lapok(azonosito)['TUDOMANYOS']
    kezd = next(i for i, s in enumerate(sorok) if s.szoveg.startswith('## 1. '))
    veg = next((i for i, s in enumerate(sorok) if i > kezd and s.szoveg.startswith('## ')), len(sorok))
    return sorok[kezd:veg]


def nfc(szoveg):
    return unicodedata.normalize('NFC', szoveg)


def _cim_horgony(cimsor):
    """A címsor horgonya, ahogy a megjelenítők képzik (kisbetű, írásjelek nélkül, a szóköz helyén kötőjel)."""
    return re.sub(r'[^\w\- ]', '', cimsor.lower()).strip().replace(' ', '-')


class Modell(unittest.TestCase):
    def test_gk21_a_szamok_osszeadodnak_es_egyeznek_a_melleklettel(self):
        """GK-21, GK-09: a Döntési út számai összeadódnak, a csoportok helyei kiadják a motívum helyeit, és a
        számok ugyanazok, mint a kizárt versek mellékletében (a két nézet egy modellből számol)."""
        for azonosito in MINTALAPOK:
            m = dontesi_ut.kapu(modell(azonosito))
            v = m.vizsgalat
            self.assertEqual(v.bent + v.csoport + v.egyen + v.nyitva, v.osszes, azonosito)
            self.assertEqual(sum(len(c.helyek) for c in m.maradt), v.helyek, azonosito)
            korny = fo.Kornyezet(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), fo.Mod.MUNKA)
            mv = kizarasok.szamit(korny).vizsgalat
            self.assertEqual((v.bent, v.csoport, v.egyen, v.nyitva, v.osszes),
                             (mv.bent, mv.csoport, mv.egyen, mv.nyitva, mv.osszes), azonosito)
        v = modell('HAMART-001').vizsgalat
        self.assertEqual((v.osszes, v.bent, v.helyek, v.csoport, v.egyen, v.nyitva, v.ajanlas),
                         (1840, 56, 49, 1542, 242, 0, 99))

    def test_gk09_a_kapu_a_modellen_megfogja_az_elterest(self):
        """GK-09: a kapu a modellen fut: hiányzó hely vagy hibás megoszlás KapuHiba, a kiírt szöveg nélkül."""
        m = modell('HAMART-001')
        csonka = dataclasses.replace(m, maradt=m.maradt[1:])
        with self.assertRaises(vizsgalat.KapuHiba):
            dontesi_ut.kapu(csonka)
        hibas = dataclasses.replace(m.maradt[0], genezis=m.maradt[0].genezis + 1)
        with self.assertRaises(vizsgalat.KapuHiba):
            dontesi_ut.kapu(dataclasses.replace(m, maradt=(hibas,) + m.maradt[1:]))

    def test_html_jel_a_lenyilo_blokk_szovegeben_bukas(self):
        """A lenyíló (HTML-jelölésű) blokkba kerülő kézi szöveg és idézet nem tartalmazhat `<`, `>`, `&` jelet: a
        generátor nem ír át, így át sem kódol; az ilyen szöveg kapun akad meg."""
        self.assertIsNone(vizsgalat.html_ben(None))
        tiszta = Kezi('a föld átka — „idézet”', 'megjegyzes')
        self.assertIs(vizsgalat.html_ben(tiszta), tiszta)
        for rossz in ('a < b', 'x > y', 'ige & főnév'):
            with self.assertRaises(bemenet.BemenetHiba):
                vizsgalat.html_ben(Kezi(rossz, 'megjegyzes'))

    def test_a_csoportok_a_tabla_rendjeben_allnak(self):
        """A helyek a hordozó elemük szerint csoportosulnak, a csoportok az első helyük (a tábla) rendjében; a
        lánc szavai nélküli helyek egy csoportban állnak; a kézzel elnevezett szópár neve kézi szöveg."""
        m = modell('HAMART-001')
        self.assertEqual(len(m.maradt), 15)
        self.assertEqual(m.maradt[0].helyek[0].igehely, Igehely('1Móz 3:14'))
        fajtak = [c.fajta for c in m.maradt]
        self.assertEqual(fajtak.count(MaradtFajta.TEMATIKUS), 1)
        self.assertEqual(fajtak.count(MaradtFajta.NEVES_SZOPAR), 2)
        tematikus = m.maradt[fajtak.index(MaradtFajta.TEMATIKUS)]
        self.assertEqual((len(tematikus.helyek), tematikus.genezis, tematikus.oszovetseg, tematikus.ujszovetseg),
                         (6, 1, 4, 1))
        self.assertEqual(len(modell('ISTENTISZT-001').maradt), 2)


class Lap(unittest.TestCase):
    def test_az_ot_pont_cime_a_szakaszrendbol(self):
        for azonosito in MINTALAPOK:
            cimek = [s.szoveg for s in szakasz(azonosito) if s.szoveg.startswith('### ')]
            self.assertEqual(cimek, ['### 1.1. A keresés tárgya', '### 1.2. A keresés forrásai',
                                     '### 1.3. Mi esett ki és miért', '### 1.4. Mi maradt és miért',
                                     '### 1.5. Határesetek és nyitott kérdések'], azonosito)

    def test_gk04_a_teljesseg_minden_keresesre_all(self):
        """GK-04: az 1.2 pont táblájában mindhárom keresés (szavak, magyar szavak, szótárak) versszáma áll, az
        olvasói nevével, mindkét lapon; a belső kulcs nem."""
        for azonosito in MINTALAPOK:
            sorok = [lathato(s) for s in szakasz(azonosito)]
            for nev in ('| A szavak minden előfordulása | ', '| A magyar szavak | ', '| A szótárak idézőhelyei | ',
                        '| **Összesen, minden vers egyszer számolva** | '):
                self.assertEqual(sum(1 for s in sorok if s.startswith(nev)), 1, '%s: %s' % (azonosito, nev))
            self.assertFalse([s for s in sorok if re.match(r'^\| (strong|karoli|szotar) \|', s)], azonosito)
            self.assertIsNotNone(modell(azonosito).vizsgalat.keresesek, azonosito)

    def test_a_mellekletre_mutato_linkek_letezo_cimsorra_mutatnak(self):
        """A Döntési út minden mellékletre mutató linkje a melléklet egy létező címsorára mutat (a horgony a
        melléklet címéből képződik, nem külön szövegből)."""
        for azonosito in MINTALAPOK:
            cimek = {_cim_horgony(lathato(s).lstrip('#').strip())
                     for s in lapok(azonosito)['KIZARASOK'] if s.szoveg.startswith('#')}
            linkek = [m for s in szakasz(azonosito)
                      for m in re.findall(r'%s_KIZARASOK\.md#([^")]+)' % azonosito, s.szoveg)]
            self.assertGreater(len(linkek), 10, azonosito)
            self.assertEqual([link for link in linkek if link not in cimek], [], azonosito)

    def test_a_belso_linkek_letezo_igehelyre_mutatnak(self):
        """Az 1.4 és az 1.5 pont igehely-linkjei a lap létező horgonyára mutatnak (a 2.1 pont igehelyei)."""
        for azonosito in MINTALAPOK:
            horgonyok = set(re.findall(r'<a id="(ige-[^"]+)"></a>',
                                       '\n'.join(s.szoveg for s in lapok(azonosito)['TUDOMANYOS'])))
            linkek = [m for s in szakasz(azonosito) for m in re.findall(r'(?:href="|\]\()#(ige-[^")]+)', s.szoveg)]
            self.assertGreaterEqual(len(linkek), modell(azonosito).vizsgalat.helyek, azonosito)
            self.assertEqual([link for link in linkek if link not in horgonyok], [], azonosito)

    def test_a_lenyilo_blokkok_egy_sorban_zarulnak(self):
        for azonosito in MINTALAPOK:
            blokkok = [s.szoveg for s in szakasz(azonosito) if s.szoveg.startswith('<details')]
            m = modell(azonosito)
            self.assertEqual(len(blokkok), len(m.vizsgalat.csoport_okok) + len(m.vizsgalat.egyen_okok)
                             + len(m.maradt), azonosito)
            for blokk in blokkok:
                self.assertTrue(blokk.endswith('</details>'), blokk[:80])
                for jel in ('details', 'summary', 'strong', 'p', 'ul', 'li', 'em', 'a'):
                    self.assertEqual(len(re.findall(r'<%s[ >]' % jel, blokk)), blokk.count('</%s>' % jel),
                                     '%s: <%s> %s' % (azonosito, jel, blokk[:60]))

    def test_a_kezi_szoveg_valtozatlanul_all(self):
        """A funkció kézi magyarázata, a negatív kritérium és a nyitott kérdés a forrás szerint, átírás nélkül áll
        (nagybetűsítés sincs): a látható sor tartalmazza a kézi szöveget betűre."""
        b = bemenet.Bemenet(kozos.GYOKER)
        for azonosito in MINTALAPOK:
            motivum = MotivumId(azonosito)
            szoveg = '\n'.join(lathato(s) for s in szakasz(azonosito))
            for sor in bemenet.b03_elofordulasok(b, motivum):
                self.assertIn('>%s</a>: %s.</li>' % (sor.igehely.kod, sor.funkcio_magyarazat.ertek), szoveg)
            targy = motivum_be.b02_motivum(b, motivum)
            self.assertIn('**A motívum:** %s.' % targy.cim.ertek, szoveg)
            self.assertIn('**Ami ide tartozik:** %s' % targy.ide_tartozik.ertek, szoveg)
            self.assertIn('**Ami nem:** %s A motívumon kívül eső tágabb kör: %s.'
                          % (targy.nem_tartozik.ertek, targy.folerendelt.ertek), szoveg)
            kerdesek = motivum_be.b47_nyitott_kerdesek(b, motivum)
            self.assertTrue(kerdesek, azonosito)
            for kerdes in kerdesek:
                self.assertIn('- %s' % kerdes.ertek, szoveg)
        self.assertIn('>1Móz 3:14</a>: az átok első kimondása, a kígyóra;',
                      '\n'.join(lathato(s) for s in szakasz('HAMART-001')))

    def test_a_szakasz_lathato_szovegeben_nincs_belso_jeloles(self):
        """A szakasz látható szövegében nincs proveniencia, fájlnév, döntésszám, Strong-szám és belső kulcs (a
        mellékletre mutató link célja kivétel: az a jelölés része)."""
        minta = re.compile(r'scope=|forras=|\.tsv\b|\.py\b|\bDT-?F?\d+|\b[HG]\d{4}\b|gerinc|tematikus:|\bB\d\d\b')
        for azonosito in MINTALAPOK:
            for s in szakasz(azonosito):
                self.assertIsNone(minta.search(lathato(s)), '%s: %s' % (azonosito, lathato(s)[:120]))


class Bemenetek(unittest.TestCase):
    def test_gk13_a_lemma_valtozata_a_motivum_szovege_szerint(self):
        """GK-13: ha a szótár a szót több változatban adja (H2403a / H2403b), az áll, amelyik a motívum verseiben
        szerepel; versek nélkül az alapalak. A görög szó kiejtése a szótár átírásának magyaros alakja."""
        k = szavak.kiejtes(bemenet.Bemenet(kozos.GYOKER))
        versben = k.szotari(Strong('H2403'), (Igehely('1Móz 4:7'),))
        self.assertEqual((nfc(versben.alak.ertek), versben.kiejtes.ertek), (nfc('חַטָּאת'), 'chattát'))
        self.assertEqual(nfc(k.szotari(Strong('H2403')).alak.ertek), nfc('חַטָּאָה'))
        gorog = k.szotari(Strong('G2671'))
        self.assertEqual((nfc(gorog.alak.ertek), gorog.kiejtes.ertek), (nfc('κατάρα'), 'katara'))
        self.assertIsNone(k.szotari(Strong('H9999')))
        szavak_lapon = [nfc(lathato(s)) for s in szakasz('HAMART-001') if '**A motívum szavai:**' in s.szoveg]
        self.assertEqual(len(szavak_lapon), 1)
        self.assertIn(nfc('חַטָּאת (chattát), bűn;'), szavak_lapon[0])
        self.assertTrue(szavak_lapon[0].startswith(nfc('**A motívum szavai:** אֲדָמָה (adámá), föld: talaj; ')))

    def test_ismeretlen_hordozo_elotagnal_a_generalas_megall(self):
        """A hordozó elem fajtája zárt készlet (Strong-számok, kézzel elnevezett szópár, `tematikus:`): ismeretlen
        típusjelölő előtagnál (`referencia:`, `idézet:`, `formula:`) a bemenet kimondott hibával megáll, a lap nem
        találgat nevet. (Valós adat: a MENNY-001 három sora.)"""
        with self.assertRaises(bemenet.BemenetHiba) as hiba:
            bemenet.b03_elofordulasok(bemenet.Bemenet(kozos.GYOKER), MotivumId('MENNY-001'))
        self.assertIn('ismeretlen hordozó-előtag', str(hiba.exception))
        from lapgen.bemenet import elofordulas
        for elem, elotag in (('referencia:1Énokh 10:4-6', 'referencia'), ('idézet:1Énokh 1:9', 'idézet'),
                             ('formula:οὐκ ἐφείσατο (nem kegyelmezett)', 'formula'), ('tematikus:1Móz 6:5', 'tematikus')):
            self.assertEqual(elofordulas._ELOTAG_RX.match(elem).group(1), elotag)
        for elem in ('H0127', 'H6975+H1863', 'málé+chámász'):
            self.assertIsNone(elofordulas._ELOTAG_RX.match(elem))
        for azonosito in MINTALAPOK:
            self.assertTrue(bemenet.b03_elofordulasok(bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito)))

    def test_a_rovid_jelentes_egy_uton_jon(self):
        jelentes = motivum_be.rovid_jelentes(bemenet.Bemenet(kozos.GYOKER))
        self.assertEqual(jelentes.magyar(Strong('H0779')).ertek, 'megátkozni')
        self.assertEqual(jelentes.magyar(Strong('G2671')).ertek, 'átok')
        self.assertIsNone(jelentes.magyar(Strong('H9999')))

    def _repo(self, motivum_sor, forras='', res_sorok=()):
        fejlec = ('id', 'cim', 'negativ_kriterium', 'folerendelt_fogalom')
        return alap_minirepo(
            jegyzek_sorok=[('B02', 'adat/motivumok.tsv', 'motivum') + _J,
                           ('B47', 'adat/res_forras.tsv ; motivumok/<ID>.md', 'resek') + _J],
            tovabbi={'adat/motivumok.tsv': tsv(fejlec, motivum_sor),
                     'adat/res_forras.tsv': tsv(('id', 'res', 'fejlec', 'forras', 'tanulmany'), *res_sorok),
                     'motivumok/PROBA-001.md': forras})

    def test_b02_a_negativ_kriterium_szerkezeti_bontasa(self):
        """B02: a negatív kritérium a „Nem tartozik ide” szavaknál válik ketté, a szöveg változatlan; a cím és a
        fölérendelt fogalom záró pontja BemenetHiba (a réteg nem vág le a szövegből)."""
        repo = self._repo(('PROBA-001', 'A cím', 'Ide ez tartozik.  Nem tartozik ide az, ami más.', 'a tágabb kör'))
        try:
            sor = motivum_be.b02_motivum(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
            self.assertEqual((sor.ide_tartozik.ertek, sor.nem_tartozik.ertek, sor.folerendelt.ertek),
                             ('Ide ez tartozik.', 'Nem tartozik ide az, ami más.', 'a tágabb kör'))
            self.assertIsInstance(sor.cim, Kezi)
        finally:
            repo.torol()
        for rossz in (('PROBA-001', 'A cím.', 'x', 'y'), ('PROBA-001', 'A cím', 'x', 'a tágabb kör.'),
                      ('MAS-001', 'A cím', 'x', 'y')):
            repo = self._repo(rossz)
            try:
                with self.assertRaises(bemenet.BemenetHiba):
                    motivum_be.b02_motivum(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
            finally:
                repo.torol()
        repo = self._repo(('PROBA-001', 'A cím', 'Csak az tartozik ide, ami ilyen.', ''))
        try:
            sor = motivum_be.b02_motivum(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
            self.assertEqual((sor.nem_tartozik, sor.folerendelt), (None, None))
        finally:
            repo.torol()

    def test_b47_a_nyitott_kerdesek_szo_szerinti_reszletek(self):
        """B47: a vitatott pontok és a nyitott kérdések címe és első mondata a kézi forrás szó szerinti részlete,
        a forrás rendjében; a nem kézi forrású rés kimarad; idegen útvonal BemenetHiba."""
        forras = '\n'.join([
            '<!-- RÉS-KEZDET: ertelmezes -->', '### ⚠️ Vitatott pontok', '',
            '**Első pont.** Az első mondat áll itt. A második már nem.', '', '### Más cím', '',
            '**Nem ide tartozik.** Ez nem vitatott pont.', '<!-- RÉS-VÉGE: ertelmezes -->', '',
            '<!-- RÉS-KEZDET: modszertan -->', '### Nyitott kérdések', '',
            '1. **Második pont.** Kérdés-e ez? Igen.', '<!-- RÉS-VÉGE: modszertan -->', ''])
        resek = [('PROBA-001', 'ertelmezes', '## 6.', 'tanulmany', 'motivumok/PROBA-001.md'),
                 ('PROBA-001', 'modszertan', '## 7.', 'tanulmany', 'motivumok/PROBA-001.md')]
        sor = ('PROBA-001', 'A cím', 'x', 'y')
        repo = self._repo(sor, forras, resek)
        try:
            kerdesek = motivum_be.b47_nyitott_kerdesek(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
            self.assertEqual([k.ertek for k in kerdesek],
                             ['**Első pont.** Az első mondat áll itt.', '**Második pont.** Kérdés-e ez?'])
        finally:
            repo.torol()
        repo = self._repo(sor, forras, [resek[0][:3] + ('adat', ''), resek[1]])
        try:
            kerdesek = motivum_be.b47_nyitott_kerdesek(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
            self.assertEqual([k.ertek for k in kerdesek], ['**Második pont.** Kérdés-e ez?'])
        finally:
            repo.torol()
        repo = self._repo(sor, forras, [resek[0][:4] + ('tematikus_lezart/MAS.md',)])
        try:
            with self.assertRaises(bemenet.BemenetHiba):
                motivum_be.b47_nyitott_kerdesek(bemenet.Bemenet(repo.gyoker), MotivumId('PROBA-001'))
        finally:
            repo.torol()


if __name__ == '__main__':
    unittest.main(verbosity=1)
