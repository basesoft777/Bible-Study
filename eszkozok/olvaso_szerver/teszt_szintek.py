"""A szintváltó és a hozzáférési szintek tesztjei a valódi lapokon (#76 M2b, F76.34).

A szintváltó (fejléc, `/szint/<nev>`, süti) a felhasználó kérésére került be (2026-10-14), és az M5 próbaüzem egyik ellenőrzési pontja.
Csak a `belso` kiadásban jelenik meg és hat; `nyilvanos` és `kereskedelmi` kiadásban sem a vezérlő, sem a süti, sem a `?szint=` paraméter nem
emelheti a szintet.

A teszt a SAJÁT próba-konfigját használja (`konfig/hozzaferes_proba.toml`). A próba-konfig a MECHANIZMUST próbálja: a `kutato` szinthez kötött
blokkok a `forditasok`-ból olvasók (`szo.bdb_magyar`, `szo.bdb_apparatus`, `szo.magyar_gorog`) és további, a Thayer, TBESH, TBESG, LSJ, UBS_DNTG
szótárakhoz tartozó blokkok (`szo.thayer`, `szo.tbesh`, `szo.tbesg`, `szo.lsj`, `szo.ubs_dntg`), amelyek az eredeti angol forrástáblákat olvassák, nem a
`forditasok`-at. NEM követi pontosan a DT-F86c fordítás-listáját: a DT-F86c szerint a BY-SA-eredetű tartalom (pl. UBS_DNTG) nem zárható, a próba mégis zárja,
mert csak a szűrést próbálja. A #86 freemium/prémium határát nem dönti el; az éles `konfig/hozzaferes.toml`-ban mindenki `kutato`.

A valódi lapok: a két pilot-szakasz (1Móz 1:1–2:3, Zsolt 22) összes héber és görög szava, és versei.

Futtatás (Python 3.12, `pardes` WSL): PARDES_DB=/home/basesoft/pardes/pardes.db python eszkozok/olvaso_szerver/teszt_szintek.py
(PARDES_PILOT_JSON: lásd teszt_pilot_aranymintaval.py).
"""
import html
import os
import re
import sys
import unittest
import unittest.mock as mock

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
from teszt_olvaso_szerver import DB, KONFIG, VAN_DB, VAN_FLASK, _pilot_json
from teszt_pilot_aranymintaval import SZAKASZOK, VAN_PILOT, igehely_reszek, szoveg

PROBA = 'hozzaferes_proba.toml'
ALSO, KOZEP, FELSO = 'nyilvanos', 'regisztralt', 'kutato'

# a próba-konfigban a `kutato` szinthez kötött blokkok (a saját fordításból jövők)
HEBER_ZART = ('szo.bdb_magyar', 'szo.bdb_apparatus', 'szo.tbesh', 'szo.ubs_dbh')
GOROG_ZART = ('szo.magyar_gorog', 'szo.thayer', 'szo.tbesg', 'szo.lsj', 'szo.ubs_dntg')


def proba_hozz():
    return hozzaferes.Hozzaferes.betolt(KONFIG, PROBA)


def app_keszit(kiadas):
    import alkalmazas
    return alkalmazas.letrehoz(db_ut=DB, kiadas=kiadas, hozzaferes=proba_hozz())


def blokk_idk(h):
    return set(re.findall(r'data-blokk="([^"]+)"', h))


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestSzintvaltoSuti(unittest.TestCase):
    """A szintváltó: süti csak váltáskor, csak a belső kiadásban; más kiadásban semmi nem emeli a szintet."""

    def sutik(self, r):
        return r.headers.getlist('Set-Cookie')

    def test_a_proba_konfig_nem_az_eles(self):
        eles = hozzaferes.Hozzaferes.betolt(KONFIG)
        self.assertEqual(eles.alap_szint, 'kutato')                       # az éles konfigban mindenki kutato
        self.assertTrue(all(eles.lathato(b, eles.szint()) for b in blokkok.BLOKK_ID))
        p = proba_hozz()
        self.assertEqual(p.szintek, [ALSO, KOZEP, FELSO])
        self.assertEqual(p.alap_szint, ALSO)
        for b in HEBER_ZART + GOROG_ZART:
            self.assertIn(b, blokkok.BLOKK_ID)
        p.ellenoriz_blokkok(blokkok.BLOKK_ID)

    def test_belso_vezerlo_suti_es_ervenytelen_szint(self):
        c = app_keszit('belso').test_client()
        h = c.get('/1Moz/1').get_data(as_text=True)
        self.assertIn('class="szintvalto"', h)
        for n in (ALSO, KOZEP, FELSO):                                    # a vezérlő a konfig szintneveit mutatja
            self.assertIn('href="/szint/%s?vissza=' % n, h)
        self.assertEqual(self.sutik(c.get('/1Moz/1')), [])                # normál lekérés: nincs süti
        r = c.get('/szint/%s?vissza=/1Moz/1' % FELSO)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers['Location'], '/1Moz/1')
        suti = self.sutik(r)
        self.assertEqual(len(suti), 1)
        self.assertIn('pardes_szint=%s' % FELSO, suti[0])
        self.assertIn('HttpOnly', suti[0])
        self.assertIn('SameSite=Lax', suti[0])
        self.assertIn('Path=/', suti[0])
        self.assertEqual(self.sutik(c.get('/1Moz/1')), [])                # a lap sem hoz létre sütit
        self.assertIn('class="aktiv" aria-current="true">%s<' % FELSO, c.get('/1Moz/1').get_data(as_text=True).replace('\n', ''))
        self.assertEqual(c.get('/szint/nincs_ilyen').status_code, 404)    # ismeretlen szint: 404, nincs süti
        self.assertEqual(self.sutik(c.get('/szint/nincs_ilyen')), [])
        # érvénytelen süti-érték: az alapértelmezett szint, nem hiba
        c2 = app_keszit('belso').test_client()
        c2.set_cookie('pardes_szint', 'valami;rossz')
        self.assertEqual(c2.get('/r/szo/H6440').status_code, 200)

    def test_nyilvanos_es_kereskedelmi_kiadasban_a_szint_nem_emelheto(self):
        for kiadas in ('nyilvanos', 'kereskedelmi'):
            c = app_keszit(kiadas).test_client()
            h = c.get('/1Moz/1').get_data(as_text=True)
            self.assertNotIn('szintvalto', h, kiadas)                     # nincs vezérlő
            self.assertNotIn('/szint/', h, kiadas)
            r = c.get('/szint/%s' % FELSO)                                  # nincs útvonal, nincs süti
            self.assertEqual(r.status_code, 404, kiadas)
            self.assertEqual(self.sutik(r), [], kiadas)
            alap = c.get('/r/szo/H6440').get_data(as_text=True)
            self.assertNotIn('arc, arcok is', alap, kiadas)               # az alap szint (nyilvanos) érvényes
            # kézzel beállított süti és paraméter sem emel
            c.set_cookie('pardes_szint', FELSO)
            for ut in ('/r/szo/H6440', '/r/szo/H6440?szint=%s' % FELSO, '/szo/H6440?szint=%s' % FELSO, '/1Moz/1/2?szo=H6440&ful=szo&szint=%s' % FELSO):
                t = c.get(ut).get_data(as_text=True)
                self.assertNotIn('arc, arcok is', t, '%s %s' % (kiadas, ut))
                self.assertNotIn('data-blokk="szo.bdb_apparatus"', t, '%s %s' % (kiadas, ut))
            self.assertEqual(self.sutik(c.get('/1Moz/1?szint=%s' % FELSO)), [], kiadas)

    def test_belso_kiadasban_a_param_nem_emel_csak_a_suti(self):
        c = app_keszit('belso').test_client()
        self.assertNotIn('arc, arcok is', c.get('/r/szo/H6440?szint=%s' % FELSO).get_data(as_text=True))     # `?szint=` sehol nem választ szintet
        c.get('/szint/%s' % FELSO)
        self.assertIn('arc, arcok is', c.get('/r/szo/H6440').get_data(as_text=True))

    def test_a_szint_a_gyorsitotar_kulcsaban_es_az_etagben_van(self):
        c = app_keszit('belso').test_client()
        ut = '/r/szo/H6440'
        a = c.get(ut)                                                       # alap szint (nyilvanos)
        self.assertEqual(c.get(ut).headers['X-Cache'], 'HIT')
        c.get('/szint/%s' % FELSO)
        b = c.get(ut)
        self.assertEqual(b.headers['X-Cache'], 'MISS')                      # más szint: nem a gyorsítótárból
        self.assertNotEqual(a.headers['ETag'], b.headers['ETag'])
        self.assertNotEqual(a.get_data(as_text=True), b.get_data(as_text=True))
        self.assertEqual(c.get(ut, headers={'If-None-Match': a.headers['ETag']}).status_code, 200)      # az alsó szint ETag-jére a felső nem 304
        self.assertEqual(c.get(ut, headers={'If-None-Match': b.headers['ETag']}).status_code, 304)
        c.get('/szint/%s' % ALSO)                                           # vissza: az alsó lap jön, nem a felsőé
        self.assertNotIn('arc, arcok is', c.get(ut).get_data(as_text=True))
        self.assertEqual(c.get(ut).headers['ETag'], a.headers['ETag'])


@unittest.skipUnless(VAN_DB and VAN_PILOT, 'nincs pardes.db vagy pilot-forrás')
class TestSzintekValodiLapokon(unittest.TestCase):
    """A két pilot-szakasz szavain és versein: alacsonyabb szinten a magyar BDB és minden belőle származó elem hiányzik (visszaesés az angol
    Strong-glosszára, nincs 500), a magasabb szinten megvan; ugyanígy a próba-konfig többi blokkja (Thayer, TBESH, TBESG, LSJ, UBS_DNTG)."""

    @classmethod
    def setUpClass(cls):
        cls.hozz = proba_hozz()
        cls.gyar = oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), cls.hozz)
        cls.rang = {n: cls.hozz.szint_nevbol(n) for n in (ALSO, KOZEP, FELSO)}
        cls.con = cls.gyar.con()
        cls.pilot = {azon: _pilot_json(sz, azon) for sz, azon in SZAKASZOK}

    def szo(self, strong, szint, ig=None):
        return self.gyar.szo_fragment(strong, self.rang[szint], ig)

    def test_heber_szavak_alacsony_es_magas_szinten(self):
        n = hu = kulon = 0
        for azon, adat in self.pilot.items():
            for strong, l in adat['lapok'].items():
                lent, fent = self.szo(strong, ALSO), self.szo(strong, FELSO)         # nincs kivétel (500) egyik szinten sem
                idk_lent, idk_fent = blokk_idk(lent), blokk_idk(fent)
                for b in HEBER_ZART:
                    self.assertNotIn(b, idk_lent, '%s %s' % (strong, b))
                self.assertIn('szo.bdb_angol', idk_lent)                              # az angol BDB nem a saját fordítás: marad
                self.assertIn('szo.bdb_angol', idk_fent)
                self.assertNotIn('Lefordítva', lent, strong)
                self.assertNotIn('data-blokk="szo.bdb_apparatus"', lent)
                if l['bdb_hu']:
                    hu += 1
                    # a magyar szócikk megkülönböztető darabjai a `forditasok` ADATBÓL (nem a renderelt lapból): fix hosszú, fix helyű szakaszok a szócikk
                    # elejétől, amelyek az angol BDB-szövegben nincsenek (a címsor sok szócikkben azonos). Magas szinten mind megvan a HTML-ben,
                    # alacsony szinten egyik sincs meg.
                    bdb = blokkok._bdb_adat(oldalak.Kontekst(self.con, self.gyar.kozos, strong=strong))      # a forditasok adatból (alias esetén az alias szócikke)
                    mag, ang = szoveg(bdb['hu']), szoveg(bdb['en'] or '')
                    darabok = [mag[i:i + 30] for i in range(0, min(len(mag) - 30, 400), 40) if mag[i:i + 30] not in ang]
                    lent_t, fent_t = szoveg(lent), szoveg(fent)
                    if len(mag) > 300:
                        self.assertGreaterEqual(len(darabok), 2, '%s: nincs elég megkülönböztető magyar darab' % strong)
                    for d in darabok:
                        self.assertNotIn(d, lent_t, '%s: a magyar szöveg szivárog alacsony szinten: %r' % (strong, d))
                        self.assertIn(d, fent_t, '%s: a magyar darab magas szinten sincs a lapon: %r' % (strong, d))
                    kulon += bool(darabok)
                    for b in HEBER_ZART[:2]:
                        self.assertIn(b, idk_fent, strong)
                    self.assertIn('Lefordítva · %s' % l['bdb_hu_meta'], szoveg(fent), strong)
                    # alapjelentés: lent az angol Strong-glossza, fent a magyar
                    a = l['alapjelentes']['szoveg'] if l['alapjelentes'] else None
                    if a:
                        self.assertNotIn('Alapjelentés %s' % a, szoveg(lent), strong)
                        self.assertIn('Alapjelentés %s' % a, szoveg(fent), strong)
                if l['rovid']:
                    self.assertRegex(lent, r'<p class="alapjel" lang="en"[^>]*><span class="fcim">Alapjelentés</span> ' + re.escape(html.escape(l['rovid'])), strong)
                self.assertIn('szo.tbesh', idk_fent) if l['tbesh'] else None
                n += 1
        self.assertGreater(n, 200)
        self.assertGreater(hu, 100)
        self.assertGreater(kulon, 100)

    def test_gorog_szavak_alacsony_es_magas_szinten(self):
        n = 0
        for azon, adat in self.pilot.items():
            for strong, l in list(adat['gor_lapok'].items())[:120]:
                lent, fent = self.szo(strong, ALSO), self.szo(strong, FELSO)
                idk_lent, idk_fent = blokk_idk(lent), blokk_idk(fent)
                for b in GOROG_ZART:
                    self.assertNotIn(b, idk_lent, '%s %s' % (strong, b))
                # a Thayer, TBESG, LSJ, UBS_DNTG blokkok fent megvannak, ahol a forrásban van adat (a blokk üres jelzéssel mindig megjelenik)
                for b in ('szo.thayer', 'szo.tbesg', 'szo.lsj', 'szo.ubs_dntg', 'szo.magyar_gorog'):
                    self.assertIn(b, idk_fent, '%s %s' % (strong, b))
                for b in ('szo.sece_g', 'szo.tw_g', 'szo.usz', 'szo.heber_hatter'):    # a nem saját fordítású blokkok lent is megvannak
                    self.assertIn(b, idk_lent, '%s %s' % (strong, b))
                self.assertIn('<h2 class="szocim">%s' % strong, lent)                      # a fejléc a Strong-szótárból áll (nincs 500)
                n += 1
        self.assertGreater(n, 100)
        # a TBESG-szöveg lent nem szivárog: a G2316 TBESG-cikkének egyedi jelölése
        self.assertNotIn('Of the one true God', szoveg(self.szo('G2316', ALSO)))
        self.assertIn('Of the one true God', szoveg(self.szo('G2316', FELSO)))

    def test_versek_es_fejezetek_minden_szinten_hiba_nelkul(self):
        for azon, adat in self.pilot.items():
            lapok = set()
            for v in adat['versek']:
                kk, fej, vn = igehely_reszek(v['igehely'])
                for sz in (ALSO, KOZEP, FELSO):
                    h = self.gyar.vers_fragment(self.gyar.kozos.slug[kk], fej, vn, self.rang[sz])
                    self.assertIn('data-blokk="vers.heber_csempe"', h)
                if (kk, fej) not in lapok:
                    lapok.add((kk, fej))
                    lent = self.gyar.fejezet_lap(self.gyar.kozos.slug[kk], fej, None, 'olvaso', self.rang[ALSO], None, 'szo', '/')
                    fent = self.gyar.fejezet_lap(self.gyar.kozos.slug[kk], fej, None, 'olvaso', self.rang[FELSO], None, 'szo', '/')
                    self.assertNotIn('BDB magyarul', lent)                                # a számláló is a szintet követi
                    self.assertRegex(fent, r'BDB magyarul: \d+/\d+')
                    # szó a vers mellett (az „Ebben a versben” blokk): alacsony szinten is hiba nélkül, az alapjelentés angol
                    ut = self.gyar.fejezet_lap(self.gyar.kozos.slug[kk], fej, vn, 'olvaso', self.rang[ALSO], 'H0430' if kk == '1Móz' else 'H0410', 'szo', '/')
                    self.assertIn('Ebben a versben', ut)
                    self.assertNotIn('Lefordítva', ut)

    def test_a_kozepso_szint_is_a_felso_kuszob_alatt_zar(self):
        t = szoveg(self.szo('H6440', KOZEP))
        self.assertNotIn('arc, arcok is', t)
        self.assertIn('face', t)

    def test_bdb_szocikk_minden_resze_alapbol_nyitva(self):
        """A bontott BDB minden lenyitható része (alakok, további szakaszok, jelentésszerkezet) alapállapotban nyitva (a pilot `mindNyit`-ja szerint is)."""
        n = 0
        for azon, adat in self.pilot.items():
            for strong, l in adat['lapok'].items():
                if not l['appar']:
                    continue
                h = self.szo(strong, FELSO)
                i = h.index('data-blokk="szo.bdb_apparatus"')
                blokk = h[i:h.index('</section>', i)]
                zart = re.findall(r'<details(?![^>]*\bopen\b)[^>]*>', blokk)
                self.assertEqual(zart, [], '%s: lenyitható rész zárva' % strong)
                n += len(re.findall(r'<details', blokk))
        self.assertGreater(n, 300)
        blokk = self.szo('H6440', FELSO)
        self.assertIn('<h4>Jelentésszerkezet', blokk)
        j = blokk.index('<h4>Jelentésszerkezet')
        # az F98.11 óta a részletes lista előtt a vázlat (nav.jel-vazlat) áll: a szakasz első lenyitható része legyen nyitva
        self.assertTrue(blokk.startswith('<details open>', blokk.index('<details', j)))

    # -- F76.36: a szűrés kikerülhetetlen (ellenőri 4. kör) ------------------------------------------------------------------------
    def _gyar(self, blokk_szint):
        h = hozzaferes.Hozzaferes([ALSO, FELSO], ALSO, blokk_szint, ALSO)
        return oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), h), h

    def test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat(self):
        gyar, h = self._gyar({'vers.ubs': FELSO, 'vers.eredeti': FELSO})
        lent, fent = h.rang[ALSO], h.rang[FELSO]
        # szo.ebben: az UBS DBH blokkot követi (zárt vers.ubs: a blokk nem jelenik meg, nincs 500)
        self.assertNotIn('data-blokk="szo.ebben"', gyar.szo_fragment('H6440', lent, '1Móz 1:2'))
        self.assertIn('data-blokk="szo.ebben"', gyar.szo_fragment('H6440', fent, '1Móz 1:2'))
        self.assertNotIn('Ebben a versben', gyar.fejezet_lap('1Moz', 1, 2, 'olvaso', lent, 'H6440', 'szo', '/'))
        # Interlineáris csempék: a vers.eredeti blokkot követik
        l = gyar.fejezet_lap('1Moz', 1, None, 'interlinearis', lent, None, 'szo', '/')
        self.assertNotIn('class="er', l)
        self.assertNotIn('il-parositatlan', l)
        self.assertNotIn('אֱלֹהִ', l)                                         # az eredeti szó nem jelenik meg
        self.assertIn('class="il-szo"', l)                                   # a magyar szavak igen
        f = gyar.fejezet_lap('1Moz', 1, None, 'interlinearis', fent, None, 'szo', '/')
        self.assertIn('class="er', f)
        self.assertIn('אֱלֹהִ', f)

    def test_tiltott_magyar_bdb_forditasok_tablat_nem_olvas(self):
        """1e: ha a szo.bdb_magyar zárt, a `forditasok` BDB-sorait sem a szó-lap blokkjai, sem az alapjelentés, sem a számláló nem olvassa."""
        gyar, h = self._gyar({'szo.bdb_magyar': FELSO})
        with mock.patch.object(q, 'bdb_magyar', side_effect=AssertionError('a tiltott magyar BDB olvasása lefutott')), \
                mock.patch.object(q, 'bdb_magyar_meta', side_effect=AssertionError('a tiltott magyar BDB olvasása lefutott')):
            t = gyar.szo_fragment('H6440', h.rang[ALSO], '1Móz 1:2')
            self.assertIn('data-blokk="szo.bdb_angol"', t)
            self.assertNotIn('data-blokk="szo.bdb_apparatus"', t)
            gyar.fejezet_lap('1Moz', 1, None, 'olvaso', h.rang[ALSO], None, 'szo', '/')
            self.assertNotIn('BDB magyarul', gyar.fejezet_lap('1Moz', 1, None, 'olvaso', h.rang[ALSO], None, 'szo', '/'))
        # az angol blokk forrássora nem listáz fordítás-datasetet
        i = t.index('data-blokk="szo.bdb_angol"')
        forras = t[i:t.index('</section>', i)]
        self.assertNotIn('forditasok', forras)
        gyar.szo_fragment('H6440', h.rang[FELSO])                            # magas szinten olvas (nincs mock): rendben

    def test_heber_fejlec_a_szo_szotar_lathatosagat_koveti(self):
        gyar, h = self._gyar({'szo.szotar': FELSO})
        lent = gyar.szo_fragment('H6440', h.rang[ALSO])
        self.assertNotIn('data-blokk="szo.szotar"', lent)
        self.assertNotIn('pe.Nei', lent)                                     # a kiejtés (Strong-szótár adat) nem szivárog a fejlécben
        self.assertNotIn('class="alapjel" lang="en"', lent)                  # az angol Strong-glossza sem
        self.assertIn('pe.Nei', gyar.szo_fragment('H6440', h.rang[FELSO]))
        self.assertIn('data-blokk="szo.elofordulas"', lent)                  # a többi blokk marad


if __name__ == '__main__':
    unittest.main(verbosity=2)