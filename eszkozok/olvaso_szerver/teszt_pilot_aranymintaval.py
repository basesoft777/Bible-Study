"""A szerver és a #60 pilot aranymintájának összevetése (#76 M2b): a kirajzolt blokk-készlet, nem csak a számok.

Az `teszt_olvaso_szerver.py` D2-része a mért adatblokkok számát veti össze; ez a fájl azt, amit az olvasó lát: az írásjeles
Károli-szöveg, a fejléc-számlálók és az útmutató, a héber és az LXX szócsempék szavankénti tartalma, az „Ebben a versben”
blokk, az LXX versszintű együttelőfordulás, a fejezet-szintű Nave, a blokk-címek és a magyar tartalom. Az aranymintát a
TSV-ből készült pilot JSON adja (`eszkozok/olvaso_pilot/adat.py`), mindkét pilot-szakaszon (1Móz 1:1–2:3 és Zsolt 22).

A DT-F76e–i döntések (felhasználó, 2026-10-14) kódja kész, tesztjük (7. szakasz) valódi teszt: expectedFailure nincs. A tesztek a
blokk-jelenlétet, a pilot adatával való egyezést és a szerkezetet nézik; a pilot JSON ugyanabból a TSV-ből készül, amelyből a `pardes.db`.

Futtatás (Python 3.12, `pardes` WSL-disztribúció; a DB-s tesztek DB nélkül kimaradnak):
    PARDES_DB=/home/basesoft/pardes/pardes.db python eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py
Környezeti változók: PARDES_DB; PARDES_PILOT_JSON (<könyvtár>/<azonosító>/olvaso_pilot.json: 1moz_1_1_2_3, zsolt_22; hiányában az `adat.py`
ideiglenes könyvtárba fut). A tesztek csak olvasnak.
"""
import html
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

import adatbazis
import blokkok
import hozzaferes
import lekerdezesek as q
import oldalak
from teszt_olvaso_szerver import DB, GY, KONFIG, VAN_DB, _pilot_json

VAN_PILOT = os.path.exists(GY + 'konkordancia/Karoli_1908.tsv') or bool(os.environ.get('PARDES_PILOT_JSON'))
SZAKASZOK = (('1Móz 1:1-2:3', '1moz_1_1_2_3'), ('Zsolt 22', 'zsolt_22'))


def szoveg(h):
    """HTML -> sima szöveg (címkék nélkül, entitások feloldva, szóközök egységesítve)."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def igehely_reszek(ig):
    m = re.match(r'^(.+?) (\d+):(\d+)$', ig)
    return m.group(1), int(m.group(2)), int(m.group(3))


@unittest.skipUnless(VAN_DB and VAN_PILOT, 'nincs pardes.db vagy pilot-forrás (konkordancia/ vagy PARDES_PILOT_JSON)')
class TestPilotAranymintaval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hozz = hozzaferes.Hozzaferes.betolt(KONFIG)
        cls.gyar = oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), cls.hozz)
        cls.con = cls.gyar.con()
        cls.kozos = cls.gyar.kozos
        cls.pilot = {azon: _pilot_json(sz, azon) for sz, azon in SZAKASZOK}

    # -- segédek -----------------------------------------------------------------------------------------------
    def K(self, ig=None, strong=None):
        return oldalak.Kontekst(self.con, self.kozos, ig=ig, strong=strong)

    def fejezet(self, ig, reteg='', **kw):
        kk, fej, v = igehely_reszek(ig)
        return self.gyar.fejezet_lap(self.kozos.slug[kk], fej, kw.get('vers'), reteg, self.hozz.szint(), kw.get('szo'), kw.get('ful', 'szo'), '/')

    def vers_panel(self, ig):
        kk, fej, v = igehely_reszek(ig)
        return self.gyar.vers_fragment(self.kozos.slug[kk], fej, v, self.hozz.szint())

    def szo_panel(self, strong, ig=None):
        return self.gyar.szo_fragment(strong, self.hozz.szint(), ig)

    def versek(self):
        for azon, adat in self.pilot.items():
            for v in adat['versek']:
                yield azon, adat, v

    # -- 1. Károli-szöveg írásjelekkel -----------------------------------------------------------------------------
    def test_karoli_szoveg_irasjelekkel_retegekkel(self):
        """A fejezet-lap szövege (a `token_karoli` szavai + a `vers.karoli_szoveg` írásjelei) szó szerint a pilot Károli-szövege:
        réteg nélkül (folyó szöveg) és az interlineáris réteggel (#134: a munkaasztal nem nézet többé, DT-F134g)."""
        n = 0
        for nezet in ('', 'il'):
            lapok = {}
            for azon, adat, v in self.versek():
                kk, fej, vn = igehely_reszek(v['igehely'])
                if (kk, fej) not in lapok:
                    lapok[(kk, fej)] = self.fejezet(v['igehely'], nezet)
                h = lapok[(kk, fej)]
                if nezet == 'il':
                    m = re.search(r'<div class="il-vers[^"]*" id="v%d">(.*?)<div class="il-szavak">(.*?)</div>\s*(?:</div>|<div class="il-parositatlan">)' % vn, h, re.S)
                    self.assertIsNotNone(m, v['igehely'])
                    szavak = re.findall(r'<span class="hu">(.*?)</span>', m.group(2), re.S)
                    kapott = szoveg(' '.join(szavak))
                    # kötőjel után nincs szóköz a forrásban: az összefűzést a sima szóköz-egységesítés nem tudja visszaadni → szóköz nélkül hasonlítunk
                    self.assertEqual(kapott.replace(' ', ''), szoveg(v['karoli']).replace(' ', ''), '%s (%s)' % (v['igehely'], nezet))
                else:
                    # folyó szöveg (DT-F76e): egy bekezdés, a versek <span class="vers"> elemek; a vers szövege a következő versig tart
                    folyo = re.search(r'<p class="folyo" id="szoveg">(.*?)</p>', h, re.S).group(1)
                    darabok = re.split(r'<span class="vers[^"]*" id="v(\d+)">', folyo)
                    vers_html = {int(darabok[i]): darabok[i + 1] for i in range(1, len(darabok), 2)}
                    self.assertIn(vn, vers_html, v['igehely'])
                    kapott = html.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<a class="versszam".*?</a>', '', vers_html[vn], flags=re.S)))
                    kapott = re.sub(r'\s+', ' ', kapott).strip()
                    self.assertEqual(kapott, szoveg(v['karoli']), '%s (%s)' % (v['igehely'], nezet))
                n += 1
        self.assertGreater(n, 100)

    def test_irasjel_visszaadasa_az_egesz_1moz_zsolt_matthaeus_konyvon(self):
        """A szavak + írásjelük a vers szövegét adják vissza: a kötőjeles és idézőjeles szövegekre is (mintavétel a DB-ből)."""
        hibak, db = [], 0
        for kk in ('1Móz', 'Zsolt', 'Mt', 'Jel'):
            for ig, szov in self.con.execute('SELECT igehely, karoli_szoveg FROM vers WHERE konyv=?', (kk,)).fetchall():
                tok = [r[0] for r in self.con.execute("SELECT szo FROM token_karoli WHERE igehely=? AND oldal='hu' ORDER BY sorszam", (ig,))]
                if not tok:
                    continue
                ki = q.szovegbe_igazit(szov, tok)
                kapott = ''.join(k + ('' if not sz else ' ') for k, sz in ki).strip()
                db += 1
                if re.sub(r'\s+', '', kapott) != re.sub(r'\s+', '', szov):
                    hibak.append(ig)
        self.assertGreater(db, 3000)
        self.assertLessEqual(len(hibak), db // 1000, 'az írásjel-visszaadás eltér: %d / %d vers, pl. %s' % (len(hibak), db, hibak[:5]))

    # -- 2. fejléc-számlálók és útmutató ------------------------------------------------------------------------------
    def test_szamlalok_egyeznek_a_pilottal(self):
        for azon, adat in self.pilot.items():
            igek = [v['igehely'] for v in adat['versek']]
            sz = self.gyar.szamlalok(igek)
            self.assertEqual(sz['vers'], len(adat['versek']), azon)
            self.assertEqual(sz['heber'], len(adat['lapok']), azon)
            self.assertEqual(sz['gorog'], len(adat['gor_lapok']), azon)
            self.assertEqual(sz['bdb_hu'], sum(1 for l in adat['lapok'].values() if l['bdb_hu']), azon)
            self.assertEqual(sz['konyv'], len(adat['karoli_konyvek']), azon)

    def test_cimkek_es_utmutato_a_fejezet_lapon(self):
        h = self.fejezet('1Móz 1:1')
        self.assertIn('Hogyan olvasd ezt az oldalt?', h)
        self.assertRegex(h, r'<span class="cimke">31 vers</span>')
        self.assertRegex(h, r'<span class="cimke">\d+ héber \+ \d+ görög szó-lap</span>')
        self.assertRegex(h, r'<span class="cimke arany">BDB magyarul: \d+/\d+</span>')       # nem teljes → arany
        self.assertRegex(h, r'<span class="cimke">Károli–Strong: 57 könyv</span>')
        for jelleg in ('forrásadat', 'gépi feldolgozás', 'modell-kimenet'):
            self.assertIn(jelleg, szoveg(h[h.index('id="utmutato"'):h.index('class="lap-tartalom')]))

    # -- 3. a héber és az LXX szócsempék ------------------------------------------------------------------------------
    def test_heber_csempe_szavankent_a_pilot_szerint(self):
        n = 0
        for azon, adat, v in self.versek():
            th = blokkok._heber_csempek(self.K(ig=v['igehely']))
            self.assertEqual(len(th), len(v['heber']), v['igehely'])
            for w, p in zip(th, v['heber']):
                pm = p.get('macula') or {}
                m = w.get('macula') or {}
                self.assertEqual((w['heber'], w['atiras'], w['tukor'], w['strong'], w['nyelvtani']), (p['heber'], p['atiras'], p['tukor'], p['strong'], p['nyelvtani']), v['igehely'])
                self.assertEqual((m.get('lxx'), m.get('lxx_strong'), m.get('morf'), m.get('morf_hu')), (pm.get('lxx'), pm.get('lxx_strong'), pm.get('morf'), pm.get('morf_hu')),
                                 '%s %s' % (v['igehely'], p['heber']))
                n += 1
        self.assertGreater(n, 300)

    def test_heber_csempe_html_szerkezete(self):
        h = self.vers_panel('1Móz 1:1')
        i = h.index('data-blokk="vers.heber_csempe"')
        blokk = h[i:h.index('</section>', i)]
        self.assertEqual(len(re.findall(r'class="he-szo', blokk)), 11)
        self.assertEqual(len(re.findall(r'class="he-szo nyelvtani', blokk)), 6)            # בְּ הַ וְ הָ + tárgyjel ×2: a nyelvtani elemek (nincs szó-lapjuk)
        self.assertIn('אֱלֹהִ֑ים', blokk)
        self.assertIn('class="lx kat"', blokk)                                              # kattintható görög megfelelő
        self.assertIn('θεὸς', blokk)
        self.assertIn('LXX: —', blokk)                                                      # a tárgyjelnek nincs LXX-megfelelője
        self.assertIn('jelleg-gepi', blokk[:blokk.index('class="he-szo')])
        self.assertIn('href="/1Moz/1/1?szo=H0430&amp;ful=szo#v1"', blokk)                   # a szó a vers mellett nyílik meg

    def test_lxx_csempe_a_pilot_szerint(self):
        for azon, adat, v in self.versek():
            ki = q.lxx_szavak_sorrendben(self.con, v['igehely'])
            self.assertEqual([(x['szoalak'], x['strong'], x['lemma'], x['morf']) for x in ki],
                             [(x['szoalak'], x['strong'], x['lemma'], x['morf']) for x in v['lxx']], v['igehely'])
        h = self.vers_panel('1Móz 1:1')
        i = h.index('data-blokk="vers.lxx_csempe"')
        blokk = h[i:h.index('</section>', i)]
        self.assertEqual(len(re.findall(r'class="gk"', blokk)), 10)
        self.assertIn('href="/1Moz/1/1?szo=G2316&amp;ful=szo#v1"', blokk)                   # a görög szó-lap kattintásra

    def test_angol_blokkok_csempek(self):
        h = self.vers_panel('1Móz 1:1')
        self.assertEqual(h.count('class="ang-csempe"'), 7 + 6)                                # BSB 7 + KJV 6 szó
        self.assertIn('<span class="ang">In the beginning</span>', h)

    # -- 4. LXX versszintű együttelőfordulás, fejezet-szintű Nave ----------------------------------------------------------
    def test_lxx_versszintu_parok_a_pilot_szerint(self):
        n = 0
        for azon, adat, v in self.versek():
            self.assertEqual(q.lxx_versszintu(self.con, v['igehely']), v['lxx_par'], v['igehely'])
            n += bool(v['lxx_par'])
        self.assertGreater(n, 10)
        h = self.vers_panel('1Móz 1:2')
        self.assertIn('4 héber szó, 40 pár', szoveg(h))

    def test_nave_fejezet_a_pilot_szerint(self):
        for azon, adat, v in self.versek():
            kk, fej, vn = igehely_reszek(v['igehely'])
            vart = [(x['tema'], x['cimke'], x['hely'], x['id']) for x in (adat['nave_fejezet'].get(str(fej)) or [])]
            self.assertEqual(q.nave_fejezet(self.con, v['igehely']), vart, v['igehely'])
        h = szoveg(self.vers_panel('1Móz 1:1'))
        self.assertIn('Fejezet-szintű hivatkozások (2)', h)
        self.assertIn('<details class="fejezet-nave" open>', self.vers_panel('1Móz 1:1'))        # a pilot kinyitja (mindNyit)
        self.assertIn('MIRACLES', h)

    # -- 5. „Ebben a versben” a szó-lapon -------------------------------------------------------------------------------
    def test_ebben_a_versben_a_szo_lapon(self):
        esetek = (('1moz_1_1_2_3', '1Móz 1:2', 'H6440'), ('zsolt_22', 'Zsolt 22:2', 'H0410'))
        for azon, ig, strong in esetek:
            adat = self.pilot[azon]
            v = next(x for x in adat['versek'] if x['igehely'] == ig)
            w = next(x for x in v['heber'] if x['strong'] == strong)
            m = w['macula']
            hu = next(x for x in v['hu_szavak'] if x['fo'] == strong)['szo'].rstrip('.,;:!?')
            t = szoveg(self.szo_panel(strong, ig))
            self.assertIn('Ebben a versben', t)
            self.assertIn('Károli itt: „%s”' % hu, t, ig)
            self.assertIn('Alak: %s (%s) · %s (%s)' % (w['heber'], w['atiras'], m['morf_hu'], m['morf']), t, ig)
            if m.get('lxx'):
                self.assertIn('Görögül ebben a versben (LXX): %s' % m['lxx'], t, ig)
            if w['ubs']:
                self.assertIn(w['ubs'][0]['definicio'][:30], t, ig)
            else:
                self.assertIn('A UBS-szótár ehhez az előforduláshoz nem ad jelentés-besorolást.', t, ig)
        # vers-kontextus nélkül (önálló szó-lap) az „Ebben a versben” blokk nem jelenik meg
        self.assertNotIn('Ebben a versben', szoveg(self.szo_panel('H6440')))
        # a fejezet-lap vers- és szó-paramétere megnyitja
        self.assertIn('Ebben a versben', szoveg(self.fejezet('1Móz 1:2', vers=2, szo='H6440')))

    # -- 6. a pilot blokk-címei a szerveren ---------------------------------------------------------------------------------
    VERS_CIMEK = (('Versszámozás', 'Versszámozás'), ('Károli-szöveg', 'Károli-szöveg'), ('Héber szöveg', 'Héber szöveg'),
                  ('Septuaginta (LXX, Rahlfs)', 'Septuaginta (LXX, Rahlfs)'), ('Kereszthivatkozások (TSK', 'Kereszthivatkozások (TSK)'),
                  ('Károli-kereszthivatkozások', 'Károli-kereszthivatkozások'), ('Angol szó szavanként (BSB)', 'Angol szavak szavanként (BSB)'),
                  ('Angol szó szavanként (KJV)', 'Angol szavak szavanként (KJV'), ('Témák (Nave)', 'Témák (Nave'),
                  ('Tulajdonnevek (TIPNR)', 'Tulajdonnevek (TIPNR)'), ('Motívumadat (adatréteg)', 'Motívumadat (adatréteg)'),
                  ('Igehely-kapcsolatok (adatréteg)', 'Igehely-kapcsolatok (adatréteg)'), ('LXX-fordítói döntések (adatréteg)', 'LXX-fordítói döntések (adatréteg)'),
                  ('LXX versszintű együttelőfordulás', 'LXX versszintű együttelőfordulás'))
    HEBER_SZO_CIMEK = (('Ebben a versben', 'Ebben a versben'), ('Így fordítja Károli', 'Károli-alakok és bizonyosság'), ('Görög megfelelő a Septuagintában', 'Görög megfelelő'),
                       ('Szemantikai domén (SDBH)', 'Szemantikai domén (SDBH)'), ('SECE-szócikk (héber)', 'SECE-szócikk (héber)'),
                       ('TWOT- és BDB-azonosító (OSHL)', 'OSHL: TWOT- és BDB-azonosító'), ('Bővített Strong-szócikk (TBESH)', 'Bővített Strong-szócikk (TBESH)'),
                       ('translationWords (tW)', 'translationWords'))
    GOROG_SZO_CIMEK = (('Héber háttér', 'Héber háttér'), ('Az Újszövetségben', 'ÚSZ-előfordulás és versek'), ('Szótári szöveg (angol)', 'TBESG'),
                       ('Szemantikai domén (SDGNT)', 'Szemantikai domén (SDGNT)'), ('UBS DNTG jelentések (angol)', 'UBS DNTG jelentés'),
                       ('LSJ-szócikk (angol)', 'LSJ'), ('Mounce-szótár (MCGED)', 'MCGED (Mounce)'), ('SECE-szócikk (görög)', 'SECE-szócikk (görög)'),
                       ('translationWords (tW)', 'translationWords'))

    def _cimek(self, h):
        return re.findall(r'<h3>(.*?)<span class="jelleg', h, re.S)

    def test_a_pilot_cimei_a_pilot_sablonban_es_a_szerveren(self):
        with open(GY + 'eszkozok/olvaso_pilot/sablon.html', encoding='utf-8') as f:
            sablon = f.read()
        for lista in (self.VERS_CIMEK, self.HEBER_SZO_CIMEK, self.GOROG_SZO_CIMEK):
            for pilot_cim, _ in lista:
                self.assertIn(pilot_cim, sablon, 'a pilot sablonjában nincs ilyen cím: %s' % pilot_cim)
        vers = [c.strip() for c in self._cimek(self.vers_panel('1Móz 1:2'))]
        for pilot_cim, szerver_cim in self.VERS_CIMEK:
            self.assertTrue(any(c.startswith(szerver_cim) for c in vers), 'vers-panel: hiányzik a pilot „%s” blokkja (%s); van: %s' % (pilot_cim, szerver_cim, vers))
        szo = [c.strip() for c in self._cimek(self.szo_panel('H6440', '1Móz 1:2'))]
        for pilot_cim, szerver_cim in self.HEBER_SZO_CIMEK:
            self.assertTrue(any(c.startswith(szerver_cim) for c in szo), 'héber szó-lap: hiányzik a pilot „%s” blokkja (%s); van: %s' % (pilot_cim, szerver_cim, szo))
        gor = [c.strip() for c in self._cimek(self.szo_panel('G2316'))]
        for pilot_cim, szerver_cim in self.GOROG_SZO_CIMEK:
            self.assertTrue(any(c.startswith(szerver_cim) for c in gor), 'görög szó-lap: hiányzik a pilot „%s” blokkja (%s); van: %s' % (pilot_cim, szerver_cim, gor))

    def test_magyar_tartalom_a_szo_lapokon(self):
        """A pilot magyar tartalma a szerveren is megvan, ahol a forrás a `pardes.db`-ben van: a magyar BDB-szócikk szövege és a
        Károli-alakok; a pilot lapja szerinti számok (előfordulás, könyv, Károli-pár)."""
        for azon, adat in self.pilot.items():
            for strong, l in list(adat['lapok'].items())[:40]:
                if not l['bdb_hu']:
                    continue
                t = szoveg(self.szo_panel(strong))
                self.assertIn(szoveg(l['bdb_hu'])[:40], t, strong)
                self.assertIn('%d előfordulás, %d könyvben' % (l['elofordulas'], l['konyvek_szama']), t, strong)
                self.assertIn('%d Károli-előfordulás, ebből %d magas' % (l['karoli_osszes'], l['karoli_magas']), t, strong)

    def test_karoli_strong_konyvek_jelzese_a_szo_lapon(self):
        t = szoveg(self.szo_panel('H6440'))
        self.assertIn('57 feldolgozott könyv', t)

    # -- 7. a döntések (DT-F76e–i, felhasználó, 2026-10-14) kódja: valódi tesztek ---------------------------------------------
    def test_DT_F76f_magyar_alapjelentes_a_szo_lapon(self):
        """DT-F76f (a): a fejlécben a magyar alapjelentés (a pilot `alap_jelentes()` szabálya), híján az angol Strong-glossza; minden pilot-lapra."""
        n = hu = 0
        for azon, adat in self.pilot.items():
            for strong, l in adat['lapok'].items():
                a = blokkok.alapjelentes(self.K(strong=strong))
                if l['alapjelentes'] and l['alapjelentes']['szoveg']:
                    self.assertEqual((a['szoveg'], a['nyelv'], a['tisztitott']), (l['alapjelentes']['szoveg'], 'hu', l['alapjelentes']['tisztitott']), strong)
                    hu += 1
                else:
                    self.assertEqual((a['szoveg'], a['nyelv']) if a else None, (l['rovid'], 'en') if l['rovid'] else None, strong)
                n += 1
        self.assertGreater(hu, 100)
        t = szoveg(self.szo_panel('H6440', '1Móz 1:2'))
        self.assertIn('Alapjelentés arc, arcok is', t)
        self.assertIn('face', t)                                          # az angol Strong-glossza a Strong-szótár blokkban megmarad

    def test_DT_F76g_bdb_bontas_egyezik_a_pilottal_szocikkenkent(self):
        """DT-F76g (b): a szerver a pilot `bdb_szelet.py`-ját hívja; a bontás, a jelölés és az alias szócikkenként egyezik a pilotéval."""
        import json
        n = 0
        for azon, adat in self.pilot.items():
            for strong, l in adat['lapok'].items():
                d = blokkok._bdb_bontas(self.K(strong=strong))
                if l['appar'] is None:
                    self.assertIsNone(d, strong)
                    continue
                self.assertIsNotNone(d, strong)
                self.assertEqual(json.dumps(d['appar'], sort_keys=True, ensure_ascii=False), json.dumps(l['appar'], sort_keys=True, ensure_ascii=False), strong)
                self.assertEqual(d['hu'], bool(l['bdb_hu']), strong)
                self.assertEqual(d['meta'], l['bdb_hu_meta'], strong)
                self.assertEqual(bool(d['alias']), bool(l['bdb_alias']), strong)
                n += 1
        self.assertGreater(n, 200)

    def test_DT_F76g_bdb_apparatus_a_lapon(self):
        l = self.pilot['1moz_1_1_2_3']['lapok']['H6440']
        h = self.szo_panel('H6440')
        i = h.index('data-blokk="szo.bdb_apparatus"')
        blokk = h[i:h.index('</section>', i)]
        t = szoveg(blokk)
        self.assertIn('Lefordítva · %s' % l['bdb_hu_meta'], t)
        self.assertIn('hibás határ előfordulhat', t)
        for cim in ('Címszó', 'Alapjelentés és szófaj', 'Alakok (alaktani apparátus)', 'Jelentésszerkezet'):
            self.assertRegex(blokk, r'<h4>\s*%s' % re.escape(cim))
        for jelleg in ('jelleg-forras', 'jelleg-modell', 'jelleg-gepi'):
            self.assertIn(jelleg, blokk[:blokk.index('</h3>')])
        self.assertIn('arc, arcok is', t)

    def test_DT_F76g_bdb_apparatus_escape_elt(self):
        """A bontott szócikk minden szövege escape-elt (M0 3.7): szintetikus `<script>` a szeletelt mezőkben nem kerül a HTML-be."""
        x = '<script>alert(1)</script>'
        d = {'hu': True, 'meta': x, 'alias': {'tabla_strong': x, 'bdb_id': x, 'hasonlosag': x}, 'alap': None, 'appar': {
            'fej': {'heber': x, 'atiras': x, 'homonima': x, 'ossz': x}, 'alap': x, 'nyelvi': [x], 'alaktan': x, 'ref_ossz': x, 'irodalom': [x], 'krit': [x],
            'torzsek': [{'nev': x, 'db': x, 'jelentesek': [{'jel': x, 'szoveg': x, 'ref': x, 'al': [{'jel': x, 'szoveg': x, 'ref': x}]}]}],
            'szakaszok': [{'szerep': 'azonos_lemma', 'nyelv': 'héber', 'jel': x, 'heber': x, 'alap': x, 'nyelvi': [x], 'ref': x, 'torzsek': [
                {'nev': x, 'db': x, 'jelentesek': [{'jel': x, 'szoveg': x, 'ref': x, 'al': []}]}]}]}}
        h = str(blokkok._r_bdb_apparatus(d, self.K(strong='H6440')))
        self.assertNotIn('<script>', h)
        self.assertIn('&lt;script&gt;', h)

    def test_DT_F76h_lxx_tobblet_blokk_az_adat_meg_nincs_a_db_ben(self):
        """DT-F76h (c): a blokk megjelenik, és kimondja, hogy az adat még nincs a DB-ben (üres eredmény nem negatív lelet); a forrássor a TSV-ket nevezi."""
        h = self.vers_panel('1Móz 1:2')
        i = h.index('data-blokk="vers.lxx_tobblet"')
        blokk = h[i:h.index('</section>', i)]
        self.assertIn('LXX többlet és számozási eltérés', blokk)
        t = szoveg(blokk)
        self.assertIn('Az adat még nincs a DB-ben', t)
        self.assertIn('N-F76j', t)
        self.assertIn('Verzifikacios_elteres_tabla.tsv', t)
        self.assertIn('jelleg-forras', blokk)
        self.assertIn('<p class="forras">Forrás és licenc: LXX_tobblet_szakaszok.tsv', blokk)

    def test_DT_F76e_folyo_szoveg_az_interlinearis_reteg_versenkent(self):
        """DT-F76e (c): réteg nélkül folyó szöveg kis versszámokkal (a pilot elrendezése), az interlineáris réteggel versenként (#134)."""
        h = self.fejezet('1Móz 1:1', '')
        self.assertEqual(len(re.findall(r'<p class="folyo"', h)), 1)
        self.assertNotIn('<p class="vers', h)
        self.assertEqual(len(re.findall(r'<span class="vers[ "]', h)), 31)
        self.assertEqual(len(re.findall(r'<a class="versszam"', h)), 31)
        i = self.fejezet('1Móz 1:1', 'il')
        self.assertEqual(len(re.findall(r'<div class="il-vers[ "]', i)), 31)
        self.assertNotIn('class="folyo"', i)

    def test_DT_F76i_alahuzas_kapcsolo_es_tema_valto(self):
        """DT-F76i (a): „Kapcsolt szavak jelölése” kapcsoló a folyó szövegnél, Rendszer/Világos/Sötét témaváltó; a JS és a CSS kezeli (CSP: nincs inline)."""
        # az interlineáris rétegben nincs aláhúzott szó, ott a kapcsoló nem jelenik meg (F76.32, E4)
        self.assertNotIn('id="jeloles"', self.fejezet('1Móz 1:1', 'il'))
        for nezet in ('', 'il'):
            h = self.fejezet('1Móz 1:1', nezet)
            if nezet != 'il':
                self.assertIn('<input type="checkbox" id="jeloles" checked> Strong számok', h, nezet)   # DT-F134o: a felirat
            for t in ('rendszer', 'light', 'dark'):
                self.assertIn('data-tema="%s"' % t, h, nezet)
            self.assertNotIn('<script>', h)
        with open(os.path.join(D, 'statikus', 'olvaso.js'), encoding='utf-8') as f:
            js = f.read()
        with open(os.path.join(D, 'statikus', 'olvaso.css'), encoding='utf-8') as f:
            css = f.read()
        self.assertIn("getElementById('jeloles')", js)
        self.assertIn("setAttribute('data-tema'", js)
        self.assertIn('.nincs-jeloles .szo', css)
        # a téma-blokkok a token-fájlból generált token-blokkban (#98 M1, DT-F98e; /arculat.css), nem az olvaso.css-ben
        import arculat
        blokk = arculat.Arculat.betolt().css
        self.assertIn(':root[data-tema="dark"]', blokk)
        self.assertIn(':root:not([data-tema="light"])', blokk)

    def test_interlinearis_csempek_a_pilot_heber_csempei_szerint(self):
        """F76.30: az interlineáris réteg szavai csempék: magyar szó, alatta az eredeti, átírás, angol tükörfordítás, Strong (a pilot héber-csempe adata)."""
        n = 0
        for azon, adat in self.pilot.items():
            lapok = {}
            for v in adat['versek']:
                kk, fej, vn = igehely_reszek(v['igehely'])
                if (kk, fej) not in lapok:
                    lapok[(kk, fej)] = self.fejezet(v['igehely'], 'il')
                h = lapok[(kk, fej)]
                m = re.search(r'<div class="il-vers[^"]*" id="v%d">(.*?)(?=<div class="il-vers|</section>)' % vn, h, re.S)
                self.assertIsNotNone(m, v['igehely'])
                csempek = re.findall(r'<span class="heb" lang="he" dir="rtl">(.*?)</span><span class="at">(.*?)</span><span class="gl">(.*?)</span><span class="st">(.*?)</span>', m.group(1))
                csempek = [tuple(html.unescape(x) for x in c) for c in csempek]
                self.assertGreater(len(csempek), 0, v['igehely'])
                # teljes egyezés: a csempék sorrendben a token_par párjai, mindegyik a pilot héber szavából (er_sorszam = a TAHOT-lista helye)
                vart = [(v['heber'][ers - 1]['heber'], v['heber'][ers - 1]['atiras'], v['heber'][ers - 1]['tukor'], v['heber'][ers - 1]['strong'])
                        for hs, hu, ers, erszo, st, bz in q.par_szavak(self.con, v['igehely']) if st]
                self.assertEqual(csempek, vart, '%s: az Interlineáris csempék nem egyeznek a pilot héber szavaival' % v['igehely'])
                n += len(csempek)
        self.assertGreater(n, 300)
        h = self.fejezet('1Móz 1:1', 'il')
        self.assertIn('href="/1Moz/1/1?szo=H0430&amp;ful=szo#v1"', h)                # kattintásra a szó-lap
        self.assertIn('class="er nyelvtani"', h)                                        # a nyelvtani elemnek nincs szó-lapja


if __name__ == '__main__':
    unittest.main(verbosity=2)
