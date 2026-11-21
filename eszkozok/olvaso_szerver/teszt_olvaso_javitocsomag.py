"""Az olvasó javítócsomagjának (F230) védelme: a 2026-11-21-i felmérés H-pontjai.

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_olvaso_javitocsomag`. A DB nélküli tesztek (a kiejtés-szolgáltatás és a tiszta
segédfüggvények) mindig futnak; a lapokat vizsgálók a `pardes.db`-vel és Flask-kal.
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

import blokkok
import hozzaferes
import kiejtes_szolg
import lekerdezesek as q
from teszt_olvaso_szerver import VAN_DB, VAN_FLASK, app_keszit

# az olvasói szövegben (blokkcím, jelző, megjegyzés, a lap látható szövege) tiltott belső jelölők
BELSO = re.compile(r'lxx_bridge|#\d{2,3}\b|\bDT-?F?\d+|\bN-?F\d+[a-z]?\b|\bF\d{2,3}\b|\.tsv|claude-\w+-\d|alias gépi|\{L:|\*\(')


def latszik(t, forras_nelkul=False):
    """A látható szöveg: script, style és minden címke nélkül (az attribútumok, köztük a `data-proveniencia`, nem látszanak).
    `forras_nelkul`: a blokkok „Forrás és licenc” sora (táblanevek) nélkül: az szándékos (a proveniencia-szabály), a felmérés V-je."""
    t = re.sub(r'<(script|style)\b.*?</\1>', '', t, flags=re.S)
    if forras_nelkul:
        t = re.sub(r'<p class="forras">.*?</p>', '', t, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', t))


class TestKiejtesSzolgaltatas(unittest.TestCase):
    """1. pont: a szó-lap és a versnézet kiejtése a közös szolgáltatásból; tartalék: üres."""

    def test_heber_szoto_nem_a_ragozott_alak_atirasa(self):
        k = kiejtes_szolg.heber_szoto('חָטָא', 'cha.ta')
        self.assertTrue(k)
        self.assertNotIn('tov', k)                         # a strong_szotar „cha.tov-” a ragozott alak STEP-átírása volt
        self.assertNotIn('.', k)                           # nem STEP-átírás (pontokkal tagolt)

    def test_jovahagyott_kivetel_elobb_mint_a_gepi(self):
        t = kiejtes_szolg._betolt()['heber']
        self.assertTrue(t, 'nincs héber kivétel-sor az adat/kiejtes_kivetelek.tsv-ben')
        # a kivételtábla kulcsa a lemma NFC alakja vagy a STEP-átírás; az átírás-kulcsra a (nem szereplő) lemma mellett is a kivétel adódik
        for kulcs, ki in list(t.items())[:5]:
            self.assertEqual(kiejtes_szolg.heber_szoto('חטא-nincs-ilyen-lemma', kulcs), ki, kulcs)

    def test_tartalek_pontozatlan_alakra_ures(self):
        self.assertEqual(kiejtes_szolg.heber_szoto('חטא', ''), '')     # pontozatlan: nem generálunk
        self.assertEqual(kiejtes_szolg.heber_szoto('', 'cha.ta'), '')  # lemma híján sem a STEP-átírás
        self.assertEqual(kiejtes_szolg.gorog(''), '')
        self.assertEqual(kiejtes_szolg.gorog(None), '')

    def test_gorog_magyaros(self):
        self.assertEqual(kiejtes_szolg.gorog('hamartanō'), 'hamartanó')

    def test_vers_szavak_elotag_es_toldalek_nem_kap_onallo_kiejtest(self):
        sorok = [('H', 'H9005', 'לְ', 'le.'), ('H', 'H0376', 'אִישָׁ֛', "'i.Sha"), ('H', 'H9024', 'הּ', 'h'), ('H', 'H0430', 'אֱלֹהִ֑ים', "'E.lo.Him")]
        k = kiejtes_szolg.vers_szavak(sorok)
        self.assertEqual(len(k), 4)
        self.assertEqual((k[0], k[2]), ('', ''))           # az előtag- és a toldalék-sor
        self.assertTrue(k[1].startswith('l'))             # a tő sora az írott szó (le + ísá + h) kiejtése
        self.assertEqual(k[3], 'elóhím')
        # az előtag a tő írott szavában: בְּ + רֵאשִׁ֖ית = berésít (a tő csempéjén), az előtag csempéjén nincs külön kiejtés
        self.assertEqual(kiejtes_szolg.vers_szavak([('H', 'H9003', 'בְּ', 'be.'), ('H', 'H7225', 'רֵאשִׁ֖ית', 're.Shit')]), ['', 'berésít'])

    def test_vers_szavak_pontozatlan_alak_ures(self):
        self.assertEqual(kiejtes_szolg.vers_szavak([('H', 'H0430', 'אלהים', "'e.lo.Him")]), [''])

    def test_vers_szavak_gorog(self):
        self.assertEqual(kiejtes_szolg.vers_szavak([('G', 'G0264', 'ἁμαρτάνω', 'hamartanō')]), ['hamartanó'])


class TestSegedfuggvenyek(unittest.TestCase):
    def test_br_nem_nyers(self):                           # 3. pont
        h = str(blokkok._br_szoveg('1) to sin<br>1a) (Qal)<BR/>1b) <b>x</b>'))
        self.assertNotIn('&lt;br', h.lower())
        self.assertEqual(h.count('<br>'), 2)
        self.assertIn('&lt;b&gt;', h)                      # a többi jelölő escape-elt

    def test_proveniencia_olvasoi_alakja(self):            # 12. pont
        pr = 'scope=manual | forras=F123 HAMART-001 új cikk, U3 (claude-opus-5-5; a jeloltek.tsv beépített sora, DT683) | ts=2026-11-05'
        h = str(blokkok._prov_olvaso(pr))
        self.assertEqual(blokkok._prov_olvaso(''), '')
        self.assertIsNone(BELSO.search(latszik(h)))
        self.assertIn('kézi bevitel · 2026-11-05', latszik(h))
        self.assertIn('data-proveniencia="%s"' % html.escape(pr), h)    # a teljes gépi sor megmarad (a repó 1. szabálya)

    def test_kh_tartomany_vege(self):                      # 13. pont
        self.assertEqual(blokkok._kh_veg('1Móz 2:4', '1Móz 2:5'), '–5')
        self.assertEqual(blokkok._kh_veg('1Móz 2:4', '1Móz 3:2'), '–3:2')
        self.assertEqual(blokkok._kh_veg('1Móz 2:4', '2Móz 1:1'), ' – 2Móz 1:1')
        self.assertEqual(blokkok._kh_veg('1Móz 2:4', '1Móz 2:4'), '')

    def test_ubs_lexema_jelolo_feloldva(self):             # 14. pont
        s = 'including {L:evening<SDBH:עֶרֶב>} and {L:morning<SDBH:בֹּקֶר>}; {L:x}'
        self.assertEqual(q.ubs_tisztit(s), 'including evening (עֶרֶב) and morning (בֹּקֶר); x')
        self.assertIsNone(q.ubs_tisztit(None))
        self.assertEqual(q.ubs_tisztit('nincs jelölő'), 'nincs jelölő')

    def test_tanulmany_cim_olvasoi(self):                  # 11. pont
        for nyers, olvaso in (('Sod (Titok) *(tömör, fegyelmezett)*', 'Sod (Titok)'), ('Peshat (Szó szerinti) — *részletesen kifejtve*', 'Peshat (Szó szerinti)'),
                              ('4. Kapcsolódó igehelyek', '4. Kapcsolódó igehelyek')):
            self.assertEqual(blokkok.szakasz_cim_olvaso(nyers), olvaso)
        h = str(blokkok._szakasz_linkek('x', [('a', '6. Kiegészítő szempontok', 'r'), ('b', '7. Lexikai audit — módszertani napló (2026.09.04)', 'r')]))
        self.assertIn('Kiegészítő', h)
        self.assertNotIn('napló', h)

    def test_regiszter_olvasoi_szoveg_nincs_belso_azonosito(self):      # 6., 7., 9. pont
        for b in blokkok.REGISZTER:
            for szoveg in (b.cim, b.jelleg_megj, b.forras_szoveg):
                self.assertIsNone(BELSO.search(szoveg or ''), '%s: %s' % (b.id, szoveg))

    def test_bdb_egy_kartya_regiszter(self):               # 2. pont
        self.assertNotIn('szo.bdb_magyar', blokkok.BLOKK_ID)
        self.assertIn('szo.bdb_apparatus', blokkok.BLOKK_ID)
        self.assertTrue(blokkok.BLOKK_ID['szo.bdb_angol'].ures_rejt)
        self.assertTrue(blokkok.BLOKK_ID['szo.nyelvtani'].ures_rejt)         # 4. pont


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestLapok(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = app_keszit('belso').test_client()
        cls.mem = {}

    def lap(self, u):
        if u not in self.mem:
            r = self.c.get(u)
            self.assertEqual(r.status_code, 200, u)
            self.mem[u] = r.get_data(as_text=True)
        return self.mem[u]

    def blokk(self, u, b):
        t = self.lap(u)
        i = t.index('data-blokk="%s"' % b)
        return t[i:t.index('</section>', i)]

    def test_1_kiejtes_szo_lap_es_versnezet(self):
        for u, rossz, jo in (('/szo/H2398', 'cha.tov-', 'chátá'), ('/szo/H7121', "i.yik.Ra'", 'kárá'), ('/szo/H1242', 'Vo.ker', 'bóker')):
            t = self.lap(u)
            self.assertNotIn(rossz, latszik(t), u)
            self.assertIn(jo, latszik(self.blokk(u, 'szo.szotar')), u)
        self.assertIn('hamartanó', latszik(self.lap('/szo/G0264')))
        # versnézet: a héber csempe átírása a szolgáltatásé, nem a TAHOT-é
        b = self.blokk('/1Moz/1/1', 'vers.heber_csempe')
        self.assertEqual(re.findall(r'<span class="at">(.*?)</span>', b)[:4], ['', 'berésít', 'bárá', 'elóhím'])       # az előtag csempéje üres
        self.assertNotIn("'E.lo.Him", latszik(b))

    def test_2_bdb_egy_kartya(self):
        for u in ('/szo/H1242', '/szo/H2398'):
            t = self.lap(u)
            self.assertEqual(re.findall(r'data-blokk="(szo\.bdb_[a-z]+)"', t), ['szo.bdb_apparatus'], u)
            self.assertIn('Angol eredeti', t)                        # a magyar elöl, az angol eredeti csukva a kártyában

    def test_2_bdb_szakasztabla_nelkul_a_magyar_szoveg_nem_vesz_el(self):
        """Kilenc Strongnak van magyar BDB-fordítása, de nincs szakasztáblája (pl. H0747): kártya nincs, a nyers blokk a magyar szöveget adja,
        az angol eredeti csukva (a külön magyar blokk megszűnése után sem vész el)."""
        t = self.lap('/r/szo/H0747')
        self.assertIn('data-blokk="szo.bdb_angol"', t)
        b = self.blokk('/r/szo/H0747', 'szo.bdb_angol')
        self.assertIn('<details class="angol-eredeti"><summary>Angol eredeti</summary>', b)
        self.assertIn('Hámán fia', latszik(b))                       # a magyar szöveg elöl áll
        self.assertLess(latszik(b).index('Hámán fia'), latszik(b).index('Angol eredeti'))

    def test_2_bdb_teljes_magyar_szoveg_csukva_a_kartyaban(self):
        """A tagolt kártya néhány szócikknél nem ad vissza minden magyar tagmondatot (H2416, H4723): a teljes magyar szöveg csukva a kártyában marad
        (a külön nyers blokk megszűnése után is: N-F76d)."""
        b = self.blokk('/szo/H2416', 'szo.bdb_apparatus')
        self.assertIn('<details class="szk-teljes"><summary>A magyar szócikk teljes szövege (tagolás nélkül)</summary>', b)
        self.assertIn('Jeromos', latszik(b))                              # a kártya tagolt részéből hiányzó tagmondat a teljes szövegben megvan

    def test_2_bdb_modellnev_nincs_az_allapotsorban(self):
        b = self.blokk('/szo/H1242', 'szo.bdb_apparatus')
        self.assertRegex(latszik(b), r'Lefordítva · gépi fordítás, \d{4}\.\d{2}\.\d{2}')
        self.assertNotRegex(latszik(b), r'claude-\w+-\d')
        self.assertRegex(b, r'data-modell="claude-')                     # a teljes meta a `data-modell` attribútumban

    def test_2_bdb_szint_nem_lazul(self):
        h = hozzaferes.Hozzaferes(['nyilvanos', 'kutato'], 'nyilvanos', {'szo.bdb_apparatus': 'kutato'}, 'nyilvanos')
        c = app_keszit('belso', hozz=h).test_client()
        t = c.get('/r/szo/H1242').get_data(as_text=True)
        self.assertEqual(re.findall(r'data-blokk="(szo\.bdb_[a-z]+)"', t), ['szo.bdb_angol'])     # kártya nélkül a nyers angol szócikk áll
        self.assertNotIn('Lefordítva', t)

    def test_2_bdb_fordites_nelkul_az_angol_nyitva(self):
        import unittest.mock as mock
        with mock.patch.object(q, 'bdb_magyar', return_value=None), mock.patch.object(q, 'bdb_magyar_meta', return_value=None), \
                mock.patch.object(q, 'bdb_szakasz_hu_sorok', return_value={}):
            t = app_keszit('belso').test_client().get('/r/szo/H1242').get_data(as_text=True)
        self.assertEqual(re.findall(r'data-blokk="(szo\.bdb_[a-z]+)"', t), ['szo.bdb_apparatus'])
        self.assertIn('Magyar fordítás nincs · az angol eredeti áll', t)
        self.assertNotIn('Lefordítva', t)

    def test_3b_thayer_fordites_nelkul_jelzes(self):
        b = latszik(self.blokk('/szo/G0264', 'szo.magyar_gorog'))
        self.assertIn('Magyar fordítás nincs · az angol eredeti áll', b)
        self.assertNotIn('Nincs adat (üres eredmény', b)
        self.assertIn('Thayer (angol)', latszik(self.lap('/szo/G0264')))

    def test_3_tbesh_nincs_nyers_br(self):
        for u in ('/szo/H1242', '/szo/H2398', '/szo/H7121'):
            self.assertNotIn('&lt;br', self.blokk(u, 'szo.tbesh').lower(), u)

    def test_4_nyelvtani_blokk_csak_nyelvtani_szonal(self):
        self.assertNotIn('szo.nyelvtani', self.lap('/szo/H1242'))
        self.assertNotIn('Nem szerepel a nyelvtani', self.lap('/szo/H1242'))
        self.assertIn('data-blokk="szo.nyelvtani"', self.lap('/r/szo/H0853'))     # a tárgyjelölő nyelvtani szó

    def test_6_7_12_olvasoi_szoveg_nincs_belso_azonosito(self):
        for u in ('/szo/H1242', '/szo/H2398', '/1Moz/4/7', '/1Moz/1/1', '/1Moz/1?biblia=modern'):
            t = latszik(self.lap(u), forras_nelkul=True)
            for blokk_cim in re.findall(r'<h3>(.*?)</h3>', self.lap(u), flags=re.S):
                self.assertIsNone(BELSO.search(latszik(blokk_cim)), (u, blokk_cim))
            self.assertIsNone(re.search(r'lxx_bridge|#\d{2,3}\b|alias gépi', t), u)
        m = latszik(self.blokk('/1Moz/4/7', 'vers.motivum'))
        self.assertNotRegex(m, r'DT\d+|F\d{3}|claude-')
        self.assertIn('kézi bevitel', m)
        self.assertRegex(self.blokk('/1Moz/4/7', 'vers.motivum'), r'data-proveniencia="scope=')
        d = latszik(self.blokk('/1Moz/4/7', 'vers.lxx_dontes'))
        self.assertNotRegex(d, r'F\d{2}|#\d+|DT\d+|naplok|\.tsv|lekerdez')
        self.assertIn('rögzítve', d)

    def test_9_lxx_tobblet_olvasoi_jelzes(self):
        b = self.blokk('/1Moz/1/1', 'vers.lxx_tobblet')
        self.assertNotRegex(latszik(b), r'\.tsv|N-F\d+|pardes\.db')
        self.assertIn('még nem érhető el', latszik(b))

    def test_10_ubs_csak_a_versben_allo_strongok(self):
        h = latszik(self.blokk('/1Moz/1/1', 'vers.ubs'))
        self.assertIn('H0853', h)
        self.assertNotIn('H0854', h)
        self.assertNotIn('H0855', h)

    def test_11_tanulmanyblokk_nincs_nyers_jel(self):
        b = self.blokk('/1Moz/4/7', 'vers.tanulmany')
        self.assertNotIn('*(', latszik(b))
        self.assertNotIn('módszertani napló', latszik(b))
        self.assertIn('Sod (Titok)', latszik(b))

    def test_13_kh_tartomany_vege(self):
        self.assertRegex(self.blokk('/1Moz/1/1', 'vers.kh'), r'>1Móz 2:4</a>–5<')

    def test_14_ubs_lexema_feloldva(self):
        b = self.blokk('/1Moz/1/5', 'vers.ubs')
        self.assertNotIn('{L:', b)
        self.assertNotIn('&lt;SDBH', b)
        self.assertIn('evening (עֶרֶב)', latszik(b))

    def test_14_ubs_lexema_a_szo_lap_ebben_a_versben_dobozaban_is(self):
        b = self.blokk('/1Kir/11/11?szo=H4467&ful=szo', 'szo.ebben')
        self.assertNotIn('{L:', b)
        self.assertNotIn('&lt;SDBH', b)
        self.assertRegex(latszik(b), r'king\s*\([^)]*[֐-׿][^)]*\)\s*vagy queen\s*\([^)]*[֐-׿][^)]*\)')       # a lexéma a héber szóval (a kódpontsorrend a forrásé: nem hasonlítunk héber szöveget)

    def test_24_nave_job_a_megfelelo_karoli_versre_mutat(self):
        """A Nave a KJV-számozást használja; a Károli-versmegfeleltetés Jób 39:1–3-at nem tartalmazza (az LXX_OS-ből jön a pár): a hivatkozás a lap
        versére mutat, nem nem létező Károli-versre (Jób 38:41)."""
        b = self.blokk('/Job/39/3', 'vers.nave')
        self.assertNotIn('href="/Job/38/41"', b)
        self.assertIn('href="/Job/39/3">Jób 38:41</a> <span class="megj">(KJV-számozás; Károli: Jób 39:3)</span>', b)

    def test_24_nave_hivatkozas_a_megfelelo_karoli_versre_mutat(self):
        b = self.blokk('/Zsolt/22/2', 'vers.nave')
        self.assertNotIn('href="/Zsolt/22/1"', b)
        self.assertIn('<a class="igehely" href="/Zsolt/22/2">Zsolt 22:1</a> <span class="megj">(KJV-számozás; Károli: Zsolt 22:2)</span>', b)

    def test_33_ugras_a_tartalomra(self):
        t = self.lap('/')
        self.assertIn('<a class="kihagy-link" href="#tartalom">Ugrás a tartalomra</a>', t)
        self.assertIn('id="tartalom"', t)


if __name__ == '__main__':
    unittest.main(verbosity=1)
