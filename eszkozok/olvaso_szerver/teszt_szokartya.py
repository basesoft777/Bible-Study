"""A BDB-szókártya tesztjei (F213, FELADATOK #213): a megjelenítési szabályok (`bdb_szokartya.py`) adatbázis nélkül, a szó-lap
szókártyája, a szófej alapjelentése (DT-F213a), a Strong-szótár és az „Ebben a versben” magyar sora a valódi lapokon.

Az elfogadási feltételek (a brief 4. pontja): a teljes szöveg megmarad („Szócikk egyben”); a forrás egyszer, a blokk alján; nincs
elavult „gépi szeletelés” címke; jelentésenként glossza, használati sorok, csukott apparátus és angol eredeti; a nem bontható sor a
teljes szövegrész; a kapcsoló három állapota; az F104 jelölése (DT178) változatlan; a héber–görög pár csak mért adatból.

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_szokartya` (a WSL-natív PARDES_DB-vel). A DB nélküli tesztek mindig futnak.
"""
import os
import re
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import bdb_szokartya as szk  # noqa: E402
from teszt_olvaso_szerver import VAN_DB, VAN_FLASK, app_keszit  # noqa: E402

_REF = re.compile(r'(?:\d?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\s)?(\d+):(\d+)')     # a könyvnévvel, mint a blokkok._ref_tokenek


def ref_tokenek(s):
    return [(m.start(), m.end(), (int(m.group(1)), int(m.group(2)))) for m in _REF.finditer(s or '')]


class Szabalyok(unittest.TestCase):
    """A megjelenítési szabályok adatbázis nélkül."""

    def test_hasznalati_sorok_a_pontosvesszo_szerint(self):
        s = 'reggeli fény, hajnal, הַבֹּקֶר אוֺר a reggel fénye Bír 16:2; 1Sám 14:36; 25:34; לָאוֺר Jób 24:14'
        sorok = szk.egysegek(s, ref_tokenek)
        self.assertEqual(len(sorok), 2)                    # a csak helyekből álló darab az előző sorhoz fűződik
        self.assertEqual(sorok[0]['szerk'], 'הַבֹּקֶר אוֺר')
        self.assertEqual(sorok[0]['magy'], 'reggeli fény, hajnal, a reggel fénye')
        self.assertIn('1Sám 14:36', sorok[0]['hely'])
        self.assertEqual(sorok[1]['szerk'], 'לָאוֺר')

    def test_zarojelen_beluli_pontosvesszo_nem_bont(self):
        sorok = szk.egysegek('föld (a; b) 1Móz 1:1; ég 1Móz 1:2', ref_tokenek)
        self.assertEqual([x['magy'] for x in sorok], ['föld (a; b)', 'ég'])

    def test_nem_bonthato_sor_a_teljes_szovegresz(self):
        sorok = szk.egysegek('a bűnbánatéként Neh 9:1 (vö. עָפָר אֵפֶר,; öszvérterhek 2Kir 5:17', ref_tokenek)
        self.assertTrue(sorok[0]['egesz'])
        self.assertEqual(sorok[0]['magy'], 'a bűnbánatéként Neh 9:1 (vö. עָפָר אֵפֶר,')
        self.assertFalse(sorok[1]['egesz'])

    def test_apparatusba_csak_a_hivatkozas_nelkuli_zarojel(self):
        forrasjel = re.compile(r'\((?:mind\s+)?[JEPD]\)')
        s, forras, app = szk.apparatusba('föld 1Móz 2:5 (mind J) vö. 4:2 (vagy ? Dl^Pr 105) (|| עפר 3:3)', ref_tokenek,
                                         lambda b: '?' in b, forrasjel)
        self.assertEqual(forras, ['(mind J)'])
        self.assertEqual(app, ['(vagy ? Dl^Pr 105)'])
        self.assertIn('(|| עפר 3:3)', s)                   # hivatkozást tartalmazó zárójel marad (a jelölés sorrendje miatt)
        self.assertNotIn('mind J', s)

    def test_nemi_tanu_es_csak_szofaj(self):
        self.assertEqual(szk.alap_nemi_tanu('főnév hímnemű^2Móz 10:13 reggel (késői héber)'), 'főnév hímnemű reggel (késői héber)')
        self.assertEqual(szk.alap_nemi_tanu('hímnemű főnév^1Móz 1:3 (nőnemű^Jób 36:32; Jer 13:16) fény'), 'hímnemű főnév fény')
        self.assertTrue(szk.csak_szofaj('hímnemű'))
        self.assertTrue(szk.csak_szofaj('főnév, nőnemű'))
        self.assertFalse(szk.csak_szofaj('reggel'))
        self.assertFalse(szk.csak_szofaj('kő'))

    def test_vers_kulcsok(self):
        self.assertEqual(szk.vers_kulcsok('Sof 1:2-3'), {'Sof 1:2', 'Sof 1:3'})
        self.assertEqual(szk.vers_kulcsok('1Móz 4:12'), {'1Móz 4:12'})
        self.assertEqual(szk.vers_kulcsok('nem igehely'), set())


def blokk(html, azon='szo.bdb_apparatus'):
    i = html.index('data-blokk="%s"' % azon)
    j = html.find('data-blokk="', i + 20)
    return html[i:j if j > 0 else len(html)]


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class Szokartya(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = app_keszit('belso').test_client()
        cls.lap = {}

    def get(self, u):
        if u not in self.lap:
            r = self.c.get(u)
            self.assertEqual(r.status_code, 200, u)
            self.lap[u] = r.get_data(as_text=True)
        return self.lap[u]

    def test_forras_egyszer_es_nincs_elavult_cimke(self):
        for u in ('/szo/H0216', '/szo/H0127', '/szo/H7843'):
            b = blokk(self.get(u))
            self.assertNotIn('gépi bontás', b, u)
            self.assertNotIn('hibás határ előfordulhat', b, u)
            self.assertNotIn('Gépi szeletelés', b, u)
            self.assertEqual(b.count('Forrás és licenc:'), 1, u)
            self.assertNotIn('class="forrasnev"', b, u)

    def test_teljes_szoveg_megmarad(self):
        """A „Szócikk egyben” bekezdései jelentésenként a teljes magyar szöveget hordozzák (semmi nem vész el, csak csukódik)."""
        b = blokk(self.get('/szo/H0127'))
        egyben = re.findall(r'<p class="szk-egyben jsz">(.*?)</p>', b, re.S)
        self.assertEqual(len(egyben), 7)
        szoveg = re.sub(r'<[^>]+>', '', ' '.join(egyben))
        for darab in ('földdarab, földbirtok', 'öszvérterhek belőle', 'város Naftáliban', 'mint harmattal nedves'):
            self.assertIn(darab, szoveg)

    def test_jelentes_felepitese(self):
        b = blokk(self.get('/szo/H0216'))
        self.assertEqual(len(re.findall(r'<li id="bdb-0-\d+" data-jel="\d+" class="szk-jel', b)), 11)
        self.assertIn('<span class="szk-glossza">reggeli fény, hajnal</span>', b)
        self.assertIn('<span class="szk-glossza">villám</span>', b)
        self.assertRegex(b, r'<span class="szk-szerk he" lang="he">[^<]*הַבֹּקֶר')
        self.assertIn('<span class="szk-magy">hajnaltól délig</span>', b)
        self.assertIn('<details class="szk-en"><summary>Angol eredeti</summary>', b)
        self.assertIn('<details class="szk-app"><summary>Apparátus és szövegkritika', b)
        self.assertNotRegex(b, r'<details class="szk-(app|en)" open')           # az apparátus és az angol alapból csukva
        self.assertRegex(b, r'<details class="szk-jel-d" open>')                 # szónézetben minden jelentés nyitva
        self.assertNotIn('<details class="szk-jel-d">', b)
        self.assertIn('<details class="szk-alakok"><summary>Alakok</summary>', b)
        self.assertIn('<details class="szk-rokon"><summary>Rokon nyelvek és eredet</summary>', b)

    def test_nem_bonthato_sor(self):
        b = blokk(self.get('/szo/H0127'))
        self.assertRegex(b, r'<li class="szk-sor szk-egesz"><span class="szk-magy">a bűnbánatéként')

    def test_tartalomjegyzek_es_motivum(self):
        b = blokk(self.get('/szo/H0127'))
        tj = re.search(r'<nav class="szk-tj".*?</nav>', b, re.S).group(0)
        self.assertEqual(len(re.findall(r'class="szk-tj-sor', tj)), 7)
        self.assertEqual(len(re.findall(r'class="szk-tj-sor szk-van-mot', tj)), 3)          # a HAMART-001 jelentései: 1., 3., 4.
        self.assertIn('a megművelt föld, amely táplál', tj)                                 # a szerkesztői címke (SEMA 2.40)
        self.assertIn('HAMART-001 · 4 hely', b)
        self.assertRegex(b, r'<a class="igehely szk-mot" href="/1Moz/3/17"')
        self.assertRegex(b, r'<a class="igehely szk-mot2" href="/5Moz/28/18"')            # a motívum helye, a sor más szón

    def test_lxx_par_jelentesenkent(self):
        b = blokk(self.get('/szo/H0216'))
        import unicodedata
        b = unicodedata.normalize('NFC', b)                                  # a görög ékezet (oxia/tonos) egységesen
        j6 = b[b.index('<li id="bdb-0-6"'):b.index('<li id="bdb-0-7"')]
        self.assertIn('φέγγος', j6)
        self.assertIn('φῶς', j6)
        j1 = blokk(self.get('/szo/H0127'))
        self.assertRegex(j1, r'class="szk-lxx"[^>]*>LXX <span class="gr" lang="grc">γῆ</span> 41')
        self.assertNotIn('>ὁ<', b)                                                          # a névelő (nyelvtani Strong) nem pár

    def test_nezetkapcsolo(self):
        b = blokk(self.get('/szo/H0127'))
        self.assertIn('<div class="szk" data-nezet="olvaso">', b)
        self.assertEqual(re.findall(r'data-szk-nezet="([a-z]+)"', b), ['olvaso', 'egyben', 'app'])
        js = open(os.path.join(D, 'statikus', 'olvaso.js'), encoding='utf-8').read()
        self.assertIn("get('nezet')", js)
        self.assertIn('pardes_szk_nezet', js)
        css = open(os.path.join(D, 'statikus', 'olvaso.css'), encoding='utf-8').read()
        self.assertIn('.szk[data-nezet="egyben"] .szk-egyben { display: block; }', css)

    def test_meg_n_hely(self):
        b = blokk(self.get('/szo/H0127'))
        self.assertRegex(b, r'<button type="button" class="szk-tobb" data-db="\d+">még \d+ hely</button>')
        sor = re.search(r'<li class="szk-sor">(?:(?!</li>).)*class="szk-tobb"(?:(?!</li>).)*</li>', b, re.S).group(0)
        rejtett = re.findall(r'<span class="szk-rejt">(.*?)</span>', sor)
        self.assertTrue(rejtett)
        self.assertFalse([r for r in rejtett if 'szk-mot' in r or 'bdb-itt' in r])          # a kiemelt hely sosem rejtett

    def test_f104_eros_jeloles_versbol(self):
        b = blokk(self.get('/szo/H0216?vers=1Moz/1/3'))
        self.assertIn('class="bdb-ebben"', b)
        self.assertRegex(b, r'<li id="bdb-0-1" data-jel="1" class="szk-jel bdb-itt">')
        self.assertRegex(b, r'<a class="igehely bdb-itt" href="/1Moz/1/3" title="feloldva: 1Móz 1:3"')
        self.assertIn('<span class="szk-tag szk-tag-ez">ez a vers</span>', b)

    def test_f104_nem_idezi(self):
        b = blokk(self.get('/szo/H0216?vers=1Moz/1/4'))
        self.assertIn('A BDB ezt a verset nem idézi.', b)
        self.assertNotRegex(b, r'class="szk-jel bdb-')

    def test_alapjelentes_glossza_elol(self):
        """DT-F213a: a magyar glossza elöl; a H1242 nemi tanús fejsora nem ad „hímnemű”-t."""
        for strong, vart in (('H1242', 'reggel'), ('H0127', 'föld: talaj'), ('H0216', 'fény'), ('G0032', 'angyal')):
            h = self.get('/szo/%s' % strong)
            self.assertRegex(h, r'<p class="alapjel" lang="hu" title="[^"]*" data-forras="glossza"><span class="fcim">Alapjelentés</span> '
                             + re.escape(vart) + '</p>', strong)

    def test_strong_szotar_magyarul_elol(self):
        b = blokk(self.get('/szo/H1242'), 'szo.szotar')
        self.assertIn('<td>reggel <span class="angol-kis" lang="en">morning</span></td>', b)

    def test_ebben_a_versben_glossza_es_ubs(self):
        b = blokk(self.get('/szo/H1242?vers=1Moz/1/5'), 'szo.ebben')
        self.assertIn('Glossza: reggel <span class="angol-kis" lang="en">morning</span>', b)
        self.assertIn('A UBS-jelentés magyar fordítása ehhez a szóhoz még nincs.', b)
        b2 = blokk(self.get('/szo/H0127?vers=1Moz/3/17'), 'szo.ebben')
        self.assertNotIn('még nincs', b2)                                                   # a H0127-nek van magyar UBS-fordítása
        self.assertRegex(b2, r'<span class="def">= [^<]*föld')


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class MagyarForditasBekotve(unittest.TestCase):
    """F213 bekötési audit (orkesztrátor, 2026-11-12): a `forditasok`-ban és a `nave_tema_hu`-ban álló magyar fordítás a blokkban
    elöl, az angol eredeti mellette vagy lenyílóban; fordítás nélkül az angol változatlan."""

    @classmethod
    def setUpClass(cls):
        cls.c = app_keszit('belso').test_client()

    def b(self, u, azon):
        r = self.c.get(u)
        self.assertEqual(r.status_code, 200, u)
        return blokk(r.get_data(as_text=True), azon)

    def test_tbesg_es_lsj(self):
        b = self.b('/szo/G0086', 'szo.tbesg')
        self.assertIn('pokol: Hádész <span class="angol-kis" lang="en">hell: Hades</span>', b)
        self.assertIn('<details class="angol-eredeti"><summary>Angol eredeti</summary>', b)
        self.assertIn('<details class="angol-eredeti"><summary>Angol eredeti</summary>', self.b('/szo/G0086', 'szo.lsj'))
        self.assertNotIn('angol-eredeti', self.b('/szo/G3056', 'szo.lsj'))                 # fordítás nélkül az angol változatlan

    def test_domenek(self):
        self.assertIn('Föld <span class="angol-kis" lang="en">Land</span>', self.b('/szo/H0127', 'szo.sdbh'))
        self.assertIn('Pusztítás <span class="angol-kis" lang="en">Destroy</span>', self.b('/szo/G1311', 'szo.sdgnt'))

    def test_tbesh_es_tw(self):
        b = self.b('/szo/H7585', 'szo.tbesh')
        self.assertIn('pokol: Seol <span class="angol-kis" lang="en">hell: Sheol</span>', b)
        self.assertIn('A szócikk magyarul:', b)
        tw = self.b('/szo/H7585', 'szo.tw_h')
        self.assertIn('Meghatározás', tw)
        self.assertIn('<details class="angol-eredeti"><summary>Angol eredeti</summary>', tw)
        self.assertIn('sirat, siralom <span class="angol-kis" lang="en">lament, lamentation</span>', self.b('/szo/H0056', 'szo.tw_h'))

    def test_nave_tema(self):
        b = self.b('/r/vers/Zak/8/21', 'vers.nave')
        self.assertIn('ébredések <span class="angol-kis" lang="en">REVIVALS</span>', b)
        self.assertIn('CHURCH', b)                                                          # fordítás nélküli téma angolul


@unittest.skipUnless(VAN_DB, 'nincs pardes.db')
class NemiTanu(unittest.TestCase):
    """A magyar BDB-fejsor alapjelentése a nemi tanús szavaknál (a glossza nélküli tartalék): nem csak szófaj, és a jelentés áll."""

    def test_nemi_tanus_szavak(self):
        import adatbazis
        import blokkok
        import oldalak
        from teszt_olvaso_szerver import DB
        con = adatbazis.Adatbazis(DB, 'belso').kapcsolat()
        kozos = oldalak.Kozos(con)
        for strong, vart in (('H1242', 'reggel'), ('H0018', 'jászol'), ('H0060', 'gyász'), ('H0212', 'kerék'), ('H0068', 'kő'),
                             ('H0216', 'fény')):
            K = oldalak.Kontekst(con, kozos, strong=strong)
            al = blokkok._bdb_alap(K)
            self.assertIsNotNone(al, strong)
            self.assertFalse(szk.csak_szofaj(al['szoveg']), strong)
            self.assertIn(vart, al['szoveg'], strong)


if __name__ == '__main__':
    unittest.main(verbosity=2)
