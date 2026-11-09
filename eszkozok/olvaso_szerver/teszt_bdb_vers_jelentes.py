"""F99 M2: a BDB igehely-hivatkozásainak feloldása (bdb_szelet.hivatkozasok, csomopont_savok, jelentespont) és a vers → jelentés tábla
(adat/bdb_vers_jelentes.tsv, bdb_vers_jelentes.py). A szabályok: DT-F99a (felhasználó, 2026-10-15). Csak olvas.

Futtatás: python eszkozok/teszt_futtat.py --fajl teszt_bdb_vers_jelentes (vagy közvetlenül; DB nem kell).
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)

import bdb_szelet as B  # noqa: E402
import bdb_vers_jelentes as V  # noqa: E402


def sor(sorok, **kw):
    i = {k: n for n, k in enumerate(V.FEJ)}
    return [s for s in sorok if all(s[i[k]] == v for k, v in kw.items())]


class Hivatkozasok(unittest.TestCase):
    def test_kiirt_orokolt_folytatas(self):
        h = B.hivatkozasok('H9999. x אב noun father; — 1. father Gen 18:18, 25; 22:18 (P) Exod 4:2.')
        self.assertEqual([(x['konyv'], x['c'], x['v'], x['konyv_mod']) for x in h],
                         [('1Móz', 18, 18, 'kiirt'), ('1Móz', 18, 25, 'folytatas'), ('1Móz', 22, 18, 'orokolt'), ('2Móz', 4, 2, 'kiirt')])

    def test_tartomany_utani_folytatas(self):
        # DT382 (A): a tartomány („-25”) után álló folytatás („, 26”) sor lesz; a tartományt nem bontja ki
        h = B.hivatkozasok('H9999. x אב noun call 1Kin 18:24-25, 26; 2Kin 5:11; 4:25-26 x.')
        self.assertEqual([(x['konyv'], x['c'], x['v'], x['konyv_mod'], x['nyers']) for x in h],
                         [('1Kir', 18, 24, 'kiirt', '1Kin 18:24'), ('1Kir', 18, 26, 'folytatas', ', 26'),
                          ('2Kir', 5, 11, 'kiirt', '2Kin 5:11'), ('2Kir', 4, 25, 'orokolt', '4:25')])
        h = B.hivatkozasok('H9999. x אב noun Gen 18:18-19, 25-26; 22:18.')
        self.assertEqual([(x['c'], x['v'], x['konyv_mod']) for x in h], [(18, 18, 'kiirt'), (18, 25, 'folytatas'), (22, 18, 'orokolt')])
        # a tartomány utáni „, 1 Samuel” „1”-e könyvnév, nem folytatás
        h = B.hivatkozasok('H9999. x אב noun so 16:8-9, 1 Samuel 21:16 x.')
        self.assertEqual([(x['konyv'], x['c'], x['v']) for x in h], [(None, 16, 8), ('1Sám', 21, 16)])

    def test_folytatas_nem_indul_kiirt_hivatkozas_elejen(self):
        # F102 (g): tartomány nélkül sem folytatás a következő kiírt hivatkozás kezdő száma („2Chr 10:19, 2 Chronicles 10:20”, H1004:
        # a „2” könyvnév; a javítás előtt hamis 2Krón 10:2 sor)
        h = B.hivatkozasok('H9999. x אב noun 1Kin 12:19 = 2Chr 10:19, 2 Chronicles 10:20 x.')
        self.assertEqual([(x['konyv'], x['c'], x['v'], x['konyv_mod']) for x in h],
                         [('1Kir', 12, 19, 'kiirt'), ('2Krón', 10, 19, 'kiirt'), ('2Krón', 10, 20, 'kiirt')])
        # a valódi folytatás változatlan
        h = B.hivatkozasok('H9999. x אב noun 2Chr 10:19, 21; 11:2.')
        self.assertEqual([(x['c'], x['v'], x['konyv_mod']) for x in h], [(10, 19, 'kiirt'), (10, 21, 'folytatas'), (11, 2, 'orokolt')])

    def test_sigla_tapadt_kiszurendo_nemi_tanu_bibliai(self):
        h = B.hivatkozasok('H9999. x אב noun masculine^Gen 1:27 man (see Wetzst in De^Job 34:36), Gen 2:7.')
        ok = {(x['konyv'], x['c'], x['v']): x['okkod'] for x in h}
        self.assertEqual(ok[('1Móz', 1, 27)], '')
        self.assertEqual(ok[('Jób', 34, 36)], 'sigla_tapadt')
        self.assertEqual(ok[('1Móz', 2, 7)], '')
        h = B.hivatkozasok('H0226. oth אוֺת noun masculine_79 ^Exod 4:8 (feminine).')
        self.assertEqual(h[0]['okkod'], '')

    def test_nem_bibliai_es_utana_orokolt(self):
        h = B.hivatkozasok('H9999. x אב noun so Late Hebrew Yoma 5:1; 6:2.')
        self.assertTrue(all(x['okkod'] == 'nem_bibliai' for x in h), h)

    def test_egyfejezetes_konyv(self):
        h = B.hivatkozasok('H9999. x אב noun Obad 8; Obadiah 13.')
        self.assertEqual([(x['konyv'], x['c'], x['v']) for x in h], [('Abd', 1, 8), ('Abd', 1, 13)])

    def test_egyfejezetes_konyv_atugrasa_oroklesnel(self):
        # F102 (b), seed-101 M092: az Abdiás után a nem 1. fejezetű könyv nélküli hely az Abdiás előtti könyvet örökli, okkóddal
        h = B.hivatkozasok('H9999. x אב noun 2Chr 17:2; compare 34:6; Obadiah 19; hence alone 31:1; 32:5; Obad 1:4.')
        self.assertEqual([(x['konyv'], x['c'], x['v'], x['konyv_mod'], x['okkod']) for x in h],
                         [('2Krón', 17, 2, 'kiirt', ''), ('2Krón', 34, 6, 'orokolt', ''), ('Abd', 1, 19, 'kiirt', ''),
                          ('2Krón', 31, 1, 'orokolt', 'orokles_egyfejezetes'), ('2Krón', 32, 5, 'orokolt', 'orokles_egyfejezetes'),
                          ('Abd', 1, 4, 'kiirt', '')])
        # egyfejezetes könyv előtt nincs más könyv: nincs átugrás (a generátor `orokles_hibas`-ra teszi)
        h = B.hivatkozasok('H9999. x אב noun Obadiah 6, 49:18.')
        self.assertEqual([(x['konyv'], x['okkod']) for x in h], [('Abd', ''), ('Abd', '')])

    def test_nincs_elozmeny(self):
        h = B.hivatkozasok('H9999. x אב noun see 4:5.')
        self.assertEqual((h[0]['konyv'], h[0]['okkod'], h[0]['konyv_mod']), (None, 'nincs_elozmeny', 'feloldhatatlan'))

    def test_zarojelbeli_nem_bibliai_nem_oroklodik_kifele(self):
        # F99 M2 vak minta (M040, M210): a zárójelen belüli nem bibliai könyvjelölő után a zárójel előtti könyv folytatódik
        h = B.hivatkozasok('H9999. x אב noun masculine^Ezek 24:4 piece (Ecclus אב Ecclesiasticus 50:12a); — absolute 24:4; 24:6.')
        ok = [(x['nyers'], x['konyv'], x['okkod']) for x in h]
        self.assertEqual(ok[1][2], 'nem_bibliai')
        self.assertEqual(ok[2:], [('24:4', 'Ez', ''), ('24:6', 'Ez', '')])
        h = B.hivatkozasok('H9999. x אב noun masculine^Num 10:14 standard (compare also Di 2:2); construct 2:3 7t.')
        self.assertEqual([(x['nyers'], x['okkod']) for x in h][1:], [('Di 2:2', 'nem_bibliai'), ('2:3', '')])

    def test_kozvetlen_szerzo_sigla_tapadt(self):
        # F99 M2 vak minta (M006, M036, M115, M128, M201, M204): a közvetlenül előtte álló szerző^mű sigla tapadt; a lezárt megjegyzés,
        # a szövegtanú, a könyvrész („Isa^2”) és a forráskritikai „R^D” nem
        def ok(t):
            return [x['okkod'] for x in B.hivatkozasok('H9999. x אב noun ' + t)]
        self.assertEqual(ok('loan-word, Schr^COT Gen 2:8; Schr^COT on Neh 1:1; see Schr^ib. 24:1; compare Fl^De Job 6:2.'),
                         ['sigla_tapadt'] * 4)
        # DT-F99j (seed-100): a megnevezett kommentár-siglák listája (`sigla_lista`), egy tagmondatban a hellyel; a Targum (ᵑ7)
        # szövegtanú, nincs a listán (felhasználó, 2026-10-15) — a sigla melletti sorokról a generátorban a TAHOT dönt (DT-F99k)
        self.assertEqual(ok('cuneiform KG^121 COT on Josh 17:11; compare Bae^l.c. Dr on 2Sam 8:3; so ᵑ7^Jer כ ׳הֵי Gen 26:4.'),
                         ['sigla_lista', 'sigla_lista', 'sigla_kozel'])
        # F102 (c), M223: a lezárt zárójeles megjegyzésben álló sigla („(MI^10) Jer 48:1”) után a hely bibliai, nem sigla-sor
        self.assertEqual(ok('in Moab (MI^10) Jer 48:1; compare Dr^Amos 4:9: Exod 10:13; Schr^COT Glossary and Isa 46:1.'),
                         ['', 'sigla_tapadt', 'sigla_kozel', 'sigla_kozel'])
        # ezek a közeli-sigla szabály alá esnek (bizonytalan, a táblában maradnak), a tapadt alá nem; a lezárt zárójel után (F102 (c),
        # M223: „(Kö^ii.l,74) Jer 6:13”, „(both R^D), Jer 6:24”, „Josh 23:7 (R^D), compare Hosea 2:19”) bibliai
        self.assertEqual(ok('suffix (Kö^ii.l,74) Jer 6:13; (both R^D), Jer 6:24; ᵐ5^B Ezra 10:21; Isa^3 Isa 50:9; (compare R^D Josh 13:22).'),
                         ['', '', 'sigla_kozel', 'sigla_kozel', 'sigla_kozel'])
        self.assertEqual(ok('use forbidden Exod 23:13 (E), Josh 23:7 (R^D), compare Hosea 2:19; Psa 16:4.'), ['', '', '', ''])

    def test_nem_bibliai_jelolorol_oroklodo_konyv(self):
        # F102 (c), H2623: a nem bibliai jelölő (2 Macc) után a könyv nélküli hely jelöltje a jelölő előtti utolsó bibliai könyv
        # (`alt_konyv`); a generátor TAHOT-igazolással dönt
        h = B.hivatkozasok('H9999. x אב noun Psalm 52:11; see 1Macc 2:42; 7:13; 2 Macc 14:6; so perhaps 116:15.')
        self.assertEqual([(x['nyers'], x['okkod'], x.get('alt_konyv')) for x in h][1:],
                         [('1Macc 2:42', 'nem_bibliai', None), ('7:13', 'nem_bibliai', 'Zsolt'), ('2 Macc 14:6', 'nem_bibliai', None),
                          ('116:15', 'nem_bibliai', 'Zsolt')])


class Jelentespont(unittest.TestCase):
    def test_alpont_es_fej(self):
        t = 'H9999. x אב noun father; — Gen 1:1; — 1 morning: a. of end Exod 10:13. b. of dawn Gen 29:25. 2 morrow Exod 16:19.'
        r = B.szeletel(t, 'אב')
        sav = B.csomopont_savok(t, r)
        pont = {(x['c'], x['v']): B.jelentespont(x['poz'], sav)[1] for x in B.hivatkozasok(t)}
        self.assertEqual(pont[(1, 1)], 'fej')
        self.assertEqual(pont[(10, 13)], '-/1/a')
        self.assertEqual(pont[(29, 25)], '-/1/b')
        self.assertEqual(pont[(16, 19)], '-/2')

    def test_szogletes_zarojel_utani_sorszam(self):
        # F123 (H7585): a „[…] 4 …” — a szögletes zárójellel záruló szakasz utáni szám is jelentés-sorszám
        t = 'H9999. x אב noun pit; 1 the pit Gen 1:1. 2 depth: a. of x Exod 10:13. b. [y; so Psa 88:4.] 3 figurative Isa 57:9.'
        r = B.szeletel(t, 'אב')
        sav = B.csomopont_savok(t, r)
        pont = {(x['c'], x['v']): B.jelentespont(x['poz'], sav)[1] for x in B.hivatkozasok(t)}
        self.assertEqual(pont[(88, 4)], '-/2/b')
        self.assertEqual(pont[(57, 9)], '-/3')


class SzerkezetJavitas(unittest.TestCase):
    """F99 M2: a pont nélküli angol személyszám és a könyvnév része nem jelentés-sorszám; a „2 2nd son” jelölő (aranyminta 2.3/1–2)."""

    @classmethod
    def setUpClass(cls):
        cls.en, cls.lem = {}, {}
        for d in V.tsv_sorok(V.BDB_EN):
            if d['Strong_padded'] in ('H3615', 'H0776', 'H4908', 'H0029', 'H5022', 'H0157', 'H1157', 'H1961', 'H1285', 'H2764', 'H5030',
                                      'H3117', 'H6086', 'H3581', 'H2490', 'H2803', 'H1419', 'H3220'):
                cls.en[d['Strong_padded']] = d['Teljes_szocikk']

    def jelek(self, s, torzs=None):
        r = B.szeletel(self.en[s])
        for t in r['torzsek']:
            if torzs is None or t['nev'] == torzs:
                return [(j['jel'], [a['jel'] for a in j['al']]) for j in t['jelentesek'] if j['jel']]

    def test_szemelyszam_nem_jelolo(self):
        self.assertEqual(self.jelek('H3615', 'Qal'), [('1', ['a', 'b', 'c', 'd']), ('2', ['a', 'b', 'c'])])
        self.assertTrue(B.szeletel(self.en['H0157'])['torzsek'][0]['jelentesek'][1]['szoveg'].startswith('human love'))

    def test_valodi_tobbes_jelentes_marad(self):
        self.assertIn(('5', []), self.jelek('H0776'))                           # „5 plural אֲרָצוֺת is almost wholly late”
        self.assertIn('3', [j for j, _ in self.jelek('H4908')])                 # „3 plural מִשְׁכָּנוֺת, dwellings”

    def test_konyvnev_szama_nem_jelolo_es_sorszamnev(self):
        self.assertEqual(self.jelek('H5022'), [])                                # „1 Kings 21”
        self.assertTrue(B.szeletel(self.en['H1157'])['torzsek'][0]['jelentesek'][0]['szoveg'].startswith('literal'))   # „1 plural …, Amos 9:10”
        self.assertEqual([j for j, _ in self.jelek('H0029')], [str(i) for i in range(1, 9)])   # „2 Chronicles 13:23. 2 2nd son”

    # F99 M2, a vak minta eltérései (naplok/BDB_SZELETELO_M0.md 9.5)
    def test_fo_tagolas_romai_szakaszai(self):
        # H1961: „I. 1. a. Fall out … above II. Come into being … III. Be” — a Qal-ban, a törzs öröklődik; H1285: I./II./III. glosszával
        sz = [(x['jel'], [t['nev'] for t in x['torzsek']]) for x in B.szeletel(self.en['H1961'])['szakaszok']]
        self.assertEqual(sz[:3], [('I', ['Qal']), ('II', ['Qal']), ('III', ['Qal'])])
        self.assertEqual([x['jel'] for x in B.szeletel(self.en['H1285'])['szakaszok']], ['I', 'II', 'III'])
        # H2803: „Qal … I. of man: 1 … II. of God: 1 … Niph`al …” — a tagolás a Qal-on belüli; a Niph`al a fő címszó törzse
        r = B.szeletel(self.en['H2803'])
        self.assertEqual([t['nev'] for t in r['torzsek']], ['Qal', "Niph'al", "Pi'el", "Hithpa'el"])   # a Pe`al az arámi חֲשַׁב szakasza
        self.assertEqual([(x['jel'], [t['nev'] for t in x['torzsek']]) for x in r['szakaszok']][:2], [('I', ['Qal']), ('II', ['Qal'])])

    def test_fejleci_glossza_szamozasa_nem_szerkezet(self):
        # H2764: „1 devoted thing. 2 devotion, ban; — … — thing devoted to ׳י: 1 thing hostile …”
        self.assertTrue(B.szeletel(self.en['H2764'])['torzsek'][0]['jelentesek'][0]['szoveg'].startswith('thing hostile'))

    def test_kimaradt_jelolok(self):
        self.assertEqual([j for j, _ in self.jelek('H5030')], ['1', '2', '3'])        # „… see חתם 2 false prophets”
        self.assertEqual([j for j, _ in self.jelek('H3117')], [str(i) for i in range(1, 8)])   # „… 7g below 4 Plural days”
        # „— 1 (c. 150 t.) a. a standing tree … 2 (approximately 175 times …) a. wood” (seed-100 M161)
        self.assertEqual(self.jelek('H6086')[:2], [('1', ['a', 'b', 'c']), ('2', ['a', 'b', 'c', 'd', 'e', 'f'])])
        self.assertEqual([j for j, _ in self.jelek('H1419')], [str(i) for i in range(1, 11)])  # „— great, 1 in magnitude”
        self.assertEqual([j for j, _ in self.jelek('H3220')], [str(i) for i in range(1, 10)])  # „especially 1 Mediterranean”

    def test_cimszo_alakvaltozattal(self):
        # H3581: „II. כֹּחַ and (Dan 11:6) כּוֺחַ noun masculine” — egy II. szakasz, az alakváltozat nem nyit újat
        sz = B.szeletel(self.en['H3581'])['szakaszok']
        self.assertEqual([x['jel'] for x in sz], ['II'])
        self.assertEqual([j['jel'] for j in sz[0]['torzsek'][0]['jelentesek']][:3], ['1', '2', '3'])

    def test_homonima_utalas_nem_jelolo(self):
        # H2490 II: „Polel Participle from 1. חוּל dancers” — homonima-utalás, nem jelentés-sorszám
        ii = [x for x in B.szeletel(self.en['H2490'])['szakaszok'] if x['jel'] == 'II'][0]
        self.assertEqual([j['jel'] for t in ii['torzsek'] for j in t['jelentesek'] if j['jel']], [])


class Seed100Javitas(unittest.TestCase):
    """F99 M2 (felhasználó, 2026-10-15): a seed-100 jóváhagyott szeletelő-hibái (naplok/BDB_SZELETELO_M2_seed100_iteletek.md) — a hely
    jelentéspontja (címke, útvonal) a mai szeletelővel. A címke DT-F99i szerint „<homonima>§<rész>”."""
    ESETEK = [
        ('M037', 'H8438', 832, 'h:תולעת', '-/2'),        # jelöletlen második címszó két alakkal
        ('M052', 'H7832', 497, '', 'Qal/1/a'),           # „QalPerfect” (OCR)
        ('M065', 'H7704', 2649, '', '-/1/f'),            # prezentációs „שׂ” a címszóban
        ('M076', 'H2022', 10988, '', '-/1/m'),           # OCR: „l.” → „1”, „m.” → „masculine”
        ('M098', 'H9005', 29478, '', '-/5/g'),           # „29:5 a. 6 b” nem jelölő
        ('M100', 'H9003', 2098, 'I§I', '-/2'),           # fej nélküli betű-szócikk, fő tagolás
        ('M105', 'H0905', 961, 'II', '-/1/b'),           # „II. בָּ֑ד בַּד, noun” a címszó, nem az utaló „III.”
        ('M114', 'H5973', 10544, 'h:מעם', '-/-/a'),     # szófaj nélküli alcímszó „מֵעִם_72”
        ('M129', 'H0389', 667, '', '-/1'),               # fejléc-összefoglaló gondolatjel nélkül
        ('M149', 'H4911', 1061, 'II', 'Qal/-'),          # prezentációs „שׁ” a II. címszóban
        ('M161', 'H6086', 2423, '', '-/2/a'),            # „2 (approximately 175 times …)”
        ('M195', 'H6331', 921, '', "Hiph'il/1/b"),       # „verb Hiph`il” a fejlécben
        ('M210', 'H0758', 685, '', '-/4/a'),             # „3 1Chr 2:23” jelölő
        ('M240', 'H1138', 100, '', '-/1/a'),             # „proper name, masculine 1. Levites”
    ]

    @classmethod
    def setUpClass(cls):
        kell = {e[1] for e in cls.ESETEK}
        cls.en = {d['Strong_padded']: d['Teljes_szocikk'] for d in V.tsv_sorok(V.BDB_EN) if d['Strong_padded'] in kell}
        cls.lem = {}
        with open(V.STRONG_SZOTAR, encoding='utf-8') as f:
            for i, l in enumerate(f):
                m = l.rstrip('\n').split('\t')
                if i and len(m) > 1 and m[0] in kell:
                    cls.lem.setdefault(m[0], m[1])

    def test_jelentespontok(self):
        for az, st, poz, cimke, ut in self.ESETEK:
            with self.subTest(az=az):
                t = self.en[st]
                r = B.szeletel(t, self.lem.get(st, ''))
                self.assertEqual(B.jelentespont(poz, B.csomopont_savok(t, r), B.szakasz_savok(t, r)), (cimke, ut))


class Tabla(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sorok, _ = V.general('2026-10-15', ['H1242', 'H0006', 'H0015', 'H0196', 'H0226', 'H6666', 'H5591', 'H8079', 'H5704',
                                                      'H8641', 'H0068', 'H1802', 'H0113', 'H8034', 'H7585', 'H1004', 'H0669',
                                                      'H6215', 'H8478', 'H2623', 'H4912'])

    def test_minden_sorban_jelentespont_feloldasi_mod_es_proveniencia(self):
        i = {k: n for n, k in enumerate(V.FEJ)}
        for s in self.sorok:
            self.assertEqual(len(s), len(V.FEJ))
            self.assertTrue(s[i['utvonal']], s)
            self.assertIn(s[i['konyv_feloldas']], ('kiirt', 'orokolt', 'folytatas', 'feloldhatatlan'))
            self.assertTrue(s[i['proveniencia']].startswith('scope=%s | forras=bdb_vers_jelentes.py (fejléc) | ts=' % s[0]), s)
            self.assertNotIn('@', s[i['proveniencia']])          # DT-F99g: a kód-hash csak a fejlécben
            self.assertNotIn('manual', s[i['proveniencia']])
            if s[i['szurt']] == '1':
                self.assertEqual(s[i['karoli_vers']], '')

    def test_h1242_atkulcsolas_es_alpont(self):
        x = sor(self.sorok, strong='H1242', nyers='Lev 6:2')[0]
        i = {k: n for n, k in enumerate(V.FEJ)}
        self.assertEqual((x[i['mt_vers']], x[i['karoli_vers']], x[i['vers_feloldas']], x[i['utvonal']]),
                         ('3Móz 6:2', '3Móz 6:9', 'atkulcsolt', '-/1/a'))

    def test_tagolatlan_szocikk(self):
        x = sor(self.sorok, strong='H0196')[0]
        self.assertEqual(x[V.FEJ.index('utvonal')], 'tagolatlan')
        self.assertEqual(x[V.FEJ.index('karoli_vers')], 'Zak 11:15')

    def test_orokles_nem_letezo_fejezetre_bizonytalan(self):
        # seed-100 M013: „Malachi 3:20 … 5:9; … 143:1” — a Malakiásnak nincs 143. fejezete: a könyv nem öröklődik
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H6666', nyers='143:1')[0]
        self.assertEqual((x[i['konyv_feloldas']], x[i['mt_vers']], x[i['okkod']], x[i['szurt']]), ('feloldhatatlan', '', 'orokles_hibas', '0'))

    def test_forras_hiba_okkod(self):
        # seed-100 M006: a forrás „Joel 1:4, 12”-t ír (a szó a Jón 1:4-ben áll): a tábla a forrást rögzíti, okkóddal
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H5591', poz='422')[0]
        self.assertEqual((x[i['mt_vers']], x[i['okkod']], x[i['szurt']]), ('Jóel 1:4', 'forras_hiba', '0'))

    def test_forras_javitas_kezi_sorbol(self):
        # DT381 (a): a 2.31 hivatkozas_kezi sora (H8034 „26:35” → 26:25) a feloldott verset javítja; a nyers a forrás alakja
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H8034', nyers='26:35')[0]
        self.assertEqual((x[i['mt_vers']], x[i['karoli_vers']], x[i['okkod']], x[i['szurt']], x[i['utvonal']]),
                         ('1Móz 26:25', '1Móz 26:25', 'forras_javitas', '0', '-/3'))
        self.assertFalse(sor(self.sorok, strong='H8034', karoli_vers='1Móz 26:35'))

    def test_h7585_negyedik_pont_es_kezi_javitas(self):
        # F123: a 4. pont („NT.] 4 ׳שׁ figurative …”) példái a -/4 alatt, nem a -/3/b-ben; a „Prov 25:11” → Péld 15:11 (2.31 kézi sor)
        i = {k: n for n, k in enumerate(V.FEJ)}
        for vers in ('Ézs 57:9', 'Hós 13:14', 'Ézs 26:19'):
            self.assertEqual([x[i['utvonal']] for x in sor(self.sorok, strong='H7585', karoli_vers=vers) if x[i['utvonal']] != 'fej'],
                             ['-/4'], vers)
        x = sor(self.sorok, strong='H7585', nyers='Prov 25:11')[0]
        self.assertEqual((x[i['karoli_vers']], x[i['okkod']], x[i['utvonal']]), ('Péld 15:11', 'forras_javitas', '-/3/b'))

    def test_tartomany_utani_folytatas_a_tablaban(self):
        # DT382 (A): „1Kin 18:24-25, 26” → a 18:26 sor (folytatas); a 18:25 (tartomány) nem
        x = sor(self.sorok, strong='H8034', karoli_vers='1Kir 18:26')
        self.assertEqual([(s[V.FEJ.index('nyers')], s[V.FEJ.index('konyv_feloldas')]) for s in x], [(', 26', 'folytatas')])
        self.assertFalse(sor(self.sorok, strong='H8034', karoli_vers='1Kir 18:25'))

    def test_orokles_egyfejezetes_tahot_kapuval(self):
        # F102 (b): seed-101 M092 (H0669 „… Obadiah 19; hence … 31:1”) → 2Krón 31:1 (a TAHOT igazolja)
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H0669', nyers='31:1')[0]
        self.assertEqual((x[i['konyv_feloldas']], x[i['mt_vers']], x[i['karoli_vers']], x[i['okkod']], x[i['szurt']]),
                         ('orokolt', '2Krón 31:1', '2Krón 31:1', 'orokles_egyfejezetes', '0'))
        # H6215 „Obadiah 6, … 49:18”: a TAHOT a Jer 49:18-ban nem hordozza a szót → marad bizonytalan, könyv nélkül
        for x in sor(self.sorok, strong='H6215', nyers='49:18'):
            self.assertEqual((x[i['konyv_feloldas']], x[i['mt_vers']], x[i['okkod']]), ('feloldhatatlan', '', 'orokles_hibas'))

    def test_nem_bibliai_utan_tahot_kapuval(self):
        # F102 (c), ELLENOR_F99 12.: H2623 „2 Macc 14:6 …; so perhaps 116:15; 149:1; 149:5; 149:9” → Zsolt (TAHOT-igazolt), a „7:13”
        # (1Makk) szűrt marad; H4912 „1:1”, „1:6” → Péld
        i = {k: n for n, k in enumerate(V.FEJ)}
        for ny, vers in (('116:15', 'Zsolt 116:15'), ('149:1', 'Zsolt 149:1'), ('149:5', 'Zsolt 149:5'), ('149:9', 'Zsolt 149:9')):
            x = sor(self.sorok, strong='H2623', nyers=ny, okkod='orokles_nem_bibliai_utan')
            self.assertEqual([(y[i['mt_vers']], y[i['szurt']], y[i['konyv_feloldas']]) for y in x], [(vers, '0', 'orokolt')], ny)
        x = sor(self.sorok, strong='H2623', nyers='7:13')[0]
        self.assertEqual((x[i['okkod']], x[i['szurt']]), ('nem_bibliai', '1'))
        self.assertEqual(sorted(y[i['mt_vers']] for y in sor(self.sorok, strong='H4912', okkod='orokles_nem_bibliai_utan')),
                         ['Péld 1:1', 'Péld 1:1', 'Péld 1:6'])

    def test_maganyos_ii_fo_tagolas(self):
        # F102 (d), seed-101 M130: H8478 „— 1 as adverb … Ezek 47:1b II. as preposition; … 2 … a. … Hab 3:16” — rész II, -/2/a;
        # a II. előtti rész római szám nélküli (az „I.” nincs kiírva)
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H8478', poz='3485')[0]
        self.assertEqual((x[i['resz']], x[i['utvonal']]), ('II', '-/2/a'))
        x = sor(self.sorok, strong='H8478', nyers='Gen 49:25')[0]
        self.assertEqual((x[i['resz']], x[i['utvonal']]), ('', '-/1'))

    def test_h1004_nincs_hamis_folytatas(self):
        # F102 (g): „2Chr 10:19, 2 Chronicles 10:20” — a 2Krón 10:2 nem sor (a javítás előtt `folytatas`, sorszam 286)
        i = {k: n for n, k in enumerate(V.FEJ)}
        self.assertFalse([x for x in sor(self.sorok, strong='H1004', mt_vers='2Krón 10:2') if x[i['konyv_feloldas']] == 'folytatas'])
        self.assertEqual([x[i['mt_vers']] for x in sor(self.sorok, strong='H1004', poz='9208')], ['2Krón 10:20'])

    def test_sigla_tahot_szerint(self):
        # F102, DT-F102e (B): a tapadt sigla („De^Job 34:36”) mindig szűrt, akkor is, ha a TAHOT a versben hordozza a szót (אָבִי);
        # a DT-F99k TAHOT-kapuja csak a közeli siglára vonatkozik
        x = sor(self.sorok, strong='H0015', nyers='Job 34:36')[0]
        self.assertEqual((x[V.FEJ.index('okkod')], x[V.FEJ.index('szurt')], x[V.FEJ.index('karoli_vers')]), ('sigla_tapadt', '1', ''))
        # a közeli sigla a TAHOT igazolásával bibliai marad (H1242 „8:26”, Dán 8:26)
        x = sor(self.sorok, strong='H1242', poz='2899')[0]
        self.assertEqual((x[V.FEJ.index('okkod')], x[V.FEJ.index('szurt')], x[V.FEJ.index('karoli_vers')]), ('sigla_igazolt', '0', 'Dán 8:26'))
        # … és szűrt, ha nem („ᵐ5^Lev 11:30”: a שְׂמָמִית nincs a 3Móz 11:30-ban; seed-100 M075)
        x = sor(self.sorok, strong='H8079', nyers='Lev 11:30')[0]
        self.assertEqual((x[V.FEJ.index('okkod')], x[V.FEJ.index('szurt')], x[V.FEJ.index('karoli_vers')]), ('sigla_tapadt', '1', ''))

    def test_karoli_f85_es_tahot(self):
        # DT-F99h (b): az F85 fejezetszintű eltolás-táblája (seed-99 M112: 2Móz 36:6 MT → Károli 36:5) és a nincs_karoli sor azonos
        # számú Károli-versre, ha a TAHOT ott hordozza a szót (karoli_tahot)
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H8641', poz='1739')[0]
        self.assertEqual((x[i['mt_vers']], x[i['karoli_vers']], x[i['vers_feloldas']]), ('2Móz 36:6', '2Móz 36:5', 'atkulcsolt_f85'))
        x = sor(self.sorok, strong='H0068', poz='3699')[0]
        self.assertEqual((x[i['karoli_vers']], x[i['vers_feloldas']], x[i['okkod']]), ('2Móz 35:33', 'azonos_tahot', 'karoli_tahot'))
        # ELLENOR_F99 1. pont: az Ézs 3 (Károli 3:1 = MT 2:22; MT 3:n → Károli 3:(n+1)); próba: H0113 „Isa 3:1” → Ézs 3:2
        x = [y for y in sor(self.sorok, strong='H0113') if y[i['mt_vers']] == 'Ézs 3:1'][0]
        # DT-F99n: saját vers_feloldas-érték, nem keveredik az F85-ösökkel
        self.assertEqual((x[i['karoli_vers']], x[i['vers_feloldas']], x[i['okkod']]), ('Ézs 3:2', 'atkulcsolt_karoli_szoveg', ''))
        self.assertFalse(any(y[i['vers_feloldas']] == 'atkulcsolt_f85' and y[i['mt_vers']].startswith('Ézs 3:') for y in self.sorok))
        # seed-101 M049: forras_hiba
        x = sor(self.sorok, strong='H1802', poz='512')[0]
        self.assertIn('forras_hiba', x[i['okkod']].split(','))

    def test_ket_romai_szint(self):
        # DT-F99i: „H5704. ad III. עַד … I. preposition … 3 Of degree … Exod 9:7” — homonima III, rész I (seed-100 M019)
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H5704', nyers='Exod 9:7')[0]
        self.assertEqual((x[i['szakasz']], x[i['resz']], x[i['utvonal']]), ('III', 'I', '-/3'))


def _jelek(t, nyelv='en'):
    return [c['jel'] for c in B._csoportok(t, nyelv)]


class Csoportok(unittest.TestCase):
    """F103 (DT167 (1) (a), (5) (a)): a jelentésen belüli használati csoportok."""

    def test_mondatkezdo_bevezeto_vesszo_utan_nem(self):
        # H3176 Pi`el 2: a vessző utáni „followed by” a jelentés feje, a pontosvessző utáni csoport
        t = 'wait for = hope for, followed by לְ Isa 42:4; followed by ל infinitive Ezek 13:6; followed by אֶל Isa 51:5; absolute hope, Job 6:11.'
        self.assertEqual(_jelek(t), ['followed by', 'followed by', 'absolute'])

    def test_zarojelben_so_also_nem(self):
        t = 'love Gen 22:2 (absolute 3:8 & see below); so 1Sam 1:5; also Psa 1:1; with עַל Gen 2:3; & especially הבקר 5:5.'
        self.assertEqual(_jelek(t), ['with', 'especially'])

    def test_inf_abs_csak_hatarozoszoi(self):
        self.assertEqual(_jelek('finish Gen 1:1; so infinitive absolute adverb 2:2; Infinitive absolute הַבְדֵּל Isa 56:3.'),
                         ['Inf. abs. as adverb'])

    def test_zarojeles_sorozat_ocr_es_gorog(self):
        self.assertEqual(_jelek('in the hand of: -1בְּיַד נָתַן give Gen 27:17; -2into the possession 10:25; especially (3) ביד נתן Josh 6:2; '
                                '(4) בְּיַד נתן Gen 30:35.'), ['(1)', '(2)', '(3)', '(4)'])
        self.assertEqual(_jelek('of direction: (a) Gen 6:4; (β) 35:13; (γ) in אֲשֶׁר אֶל 2:2.'), ['(a)', '(β)', '(γ)'])
        # egyetlen tag nem sorozat
        self.assertEqual(_jelek('of place: (a) Gen 6:4 only.'), [])

    def test_prozai_felsorolas_nem_tagolas(self):
        t = 'according to Sperling, developed from the relative שׁ by (1) the prefixing of a merely prosthetic א, and (2) the addition of ל.'
        self.assertEqual(_jelek(t), [])

    def test_alaklista_nem_kap_csoportot(self):
        # a törzs számozott jelentései előtti alaklista („Perfect …; absolute …”) nem kap csoportot (status absolutus, nem használat)
        r = B.csoport_bont(B.szeletel('H9999. x [אבד] verb Qal Perfect אָבַד Gen 1:1; — 1 perish Gen 3:3; absolute Job 4:4. '
                                      '2 vanish Gen 5:5; with מִן Psa 6:6. Pi`el Perfect אִבֵּד Gen 7:7; absolute אִבֵּד 7:8; — 1 destroy '
                                      'Gen 8:8. 2 kill Gen 9:9.'), 'en')
        csop = {ut: [c['jel'] for c in n.get('csop') or []] for _, ut, n in B.csoport_bejar(r)}
        self.assertEqual(csop.get('Qal/1'), ['absolute'])
        self.assertEqual(csop.get('Qal/2'), ['with'])
        self.assertIn("Pi'el/-", csop)
        self.assertEqual(csop["Pi'el/-"], [])

    def test_magyar_csak_egyezo_sorozatnal(self):
        en = B.csoport_bont(B.szeletel('H9999. x אב noun — 1 day Gen 1:1; especially הבקר 2:2; figurative of end 3:3. '
                                       '2 night Gen 4:4; followed by לְ 5:5; with עַל 6:6.'), 'en')
        hu = B.csoport_bont(B.szeletel('H9999. x אב főnév — 1 nap 1Móz 1:1; különösen הבקר 2:2; képletesen a végről 3:3. '
                                       '2 éjszaka 1Móz 4:4; utána לְ 5:5; עַל-val 6:6.'), 'hu')
        B.csoport_magyar(hu, en)
        csop = {ut: [c['jel'] for c in n.get('csop') or []] for _, ut, n in B.csoport_bejar(hu)}
        self.assertEqual(csop.get('-/1'), ['especially', 'figurative'])
        self.assertEqual(csop.get('-/2'), [])  # a „with + héber” csoportnak nincs magyar bevezetője: a sorozat eltér, nincs bontás

    def test_csoport_savok_utvonal(self):
        t = 'H9999. x אב noun — 1 day Gen 1:1; especially of morning 2:2; opposed to night 3:3. 2 night Gen 4:4.'
        r = B.csoport_bont(B.szeletel(t), 'en')
        sv = B.csoport_savok(t, r)
        s = B.lapit(t)
        self.assertEqual([(x[3], x[4]) for x in sv], [('-/1/+1', 'csoport'), ('-/1/+2', 'csoport')])
        self.assertTrue(s[sv[0][0]:sv[0][1]].startswith('especially of morning'))
        self.assertTrue(s[sv[1][0]:sv[1][1]].startswith('opposed to night'))

    def test_szeletel_kimenete_valtozatlan(self):
        # a bontás kiegészítő: a szeletel() önmagában nem tesz `csop` kulcsot (a lexikon és a 2.29 bemenete változatlan)
        r = B.szeletel('H9999. x אב noun — 1 day Gen 1:1; especially of morning 2:2. 2 night Gen 4:4.')
        self.assertFalse(any('csop' in n for _, _, n in B.csoport_bejar(r)))


class CsoportAranyminta(unittest.TestCase):
    """F103: az aranyminta (adat/bdb_aranyminta.tsv) 184 csoport-sora tesztesetként. A szülő-csomópontonként illesztett jelölő-sorozatban
    csoportszintű hamis határ és hiány nincs; ami eltér, az a szeletelő szerkezeti hibája (a csoport szülője hiányzik vagy rossz),
    és ennek száma nem nőhet a F103 zárómérése fölé (naplok/F103_BDB_TAGOLAS_naplo.md)."""
    SZERKEZETI_HIANY_MAX = 20
    SZERKEZETI_HAMIS_MAX = 18

    @classmethod
    def setUpClass(cls):
        repo = os.path.dirname(os.path.dirname(D))
        cls.arany = []
        fej = None
        with open(os.path.join(repo, 'adat', 'bdb_aranyminta.tsv'), encoding='utf-8', newline='') as f:
            for s in f:
                if s.startswith('#'):
                    continue
                m = s.rstrip('\r\n').split('\t')
                if fej is None:
                    fej = m
                    continue
                cls.arany.append(dict(zip(fej, m)))
        kell = {g['strong'] for g in cls.arany}
        cls.en = {}
        with open(os.path.join(repo, 'konkordancia', 'BDB_teljes_unabridged.tsv'), encoding='utf-8', newline='') as f:
            for s in f:
                k = s[:5]
                if k in kell:
                    m = s.rstrip('\r\n').split('\t')
                    cls.en[m[0]] = m[2]
        cls.lemma = {}
        with open(os.path.join(repo, 'konkordancia', 'Strong_szotar.tsv'), encoding='utf-8', newline='') as f:
            for i, s in enumerate(f):
                m = s.rstrip('\r\n').split('\t')
                if i and not s.startswith('#') and len(m) > 1 and m[0] in kell:
                    cls.lemma.setdefault(m[0], m[1])

    @staticmethod
    def _kulcs(szak):
        import re
        import unicodedata
        if not szak or re.match(r'^(?:I{1,3}|IV|V|VI)$', szak) or szak.startswith('h:'):
            return szak
        return 'h:' + re.sub(r'[֑-ׇ]', '', unicodedata.normalize('NFC', szak))

    def test_aranyminta_csoportjai(self):
        import collections
        import difflib
        import re
        vart = collections.defaultdict(list)
        szulok = set()
        for g in self.arany:
            if g['szint'] in ('jelentes', 'alpont'):
                szulok.add((g['strong'], self._kulcs(g['szakasz']), g['utvonal']))
            if g['szint'] == 'csoport':
                p = g['utvonal'].rsplit('/', 1)[0]
                vart[(g['strong'], self._kulcs(g['szakasz']), p)].append(g['jel'])
        self.assertEqual(sum(len(v) for v in vart.values()), 184)
        egyezik = hiany_sz = hamis_sz = 0
        csoportszintu = []
        for strong in sorted({g['strong'] for g in self.arany}):
            r = B.csoport_bont(B.szeletel(self.en[strong], self.lemma.get(strong, '')), 'en')
            kapott = collections.defaultdict(list)
            sz_szulok = set()
            for szak, ut, n in B.csoport_bejar(r):
                a, b = B.szakasz_bont(szak)
                k = self._kulcs(a) + (' r:' + b if b else '')
                # az aranyminta a jelentés nélküli alpontot „X/a” alakban írja
                ut2 = re.sub(r'^([^/]+)/-/([a-l])$', r'\1/\2', ut)
                sz_szulok.add((k, ut2))
                kapott[(k, ut2)].extend(c['jel'] for c in n.get('csop') or [])
            for k in set(kapott) | {x[1:] for x in vart if x[0] == strong}:
                v, kp = vart.get((strong,) + k, []), kapott.get(k, [])
                m = sum(b.size for b in difflib.SequenceMatcher(a=v, b=kp, autojunk=False).get_matching_blocks())
                egyezik += m
                if len(v) > m:
                    if k in sz_szulok:
                        csoportszintu.append(('hiányzik', strong, k, v, kp))
                    else:
                        hiany_sz += len(v) - m
                if len(kp) > m:
                    if (strong,) + k in szulok and v:
                        csoportszintu.append(('hamis határ', strong, k, v, kp))
                    else:
                        hamis_sz += len(kp) - m
        self.assertEqual(csoportszintu, [])
        self.assertGreaterEqual(egyezik, 184 - self.SZERKEZETI_HIANY_MAX)
        self.assertLessEqual(hiany_sz, self.SZERKEZETI_HIANY_MAX)
        self.assertLessEqual(hamis_sz, self.SZERKEZETI_HAMIS_MAX)


class CsoportOszlop(unittest.TestCase):
    """F103 (DT-F103a (A), orkesztrátori döntés, 2026-11-09): a 2.29 két új oszlopa; a régi oszlopok és az `utvonal` változatlan."""
    # a régi 15 oszlop (oszlopnév szerint, soronként tab-join, SHA-256) a F103 előtti main-en (94c4c2ac) és utána
    # (naplok/F103_oszlop_hash.py); szándékos újragenerálásnál (bemenet- vagy szabályváltozás) a naplóval együtt frissítendő
    REGI_OSZLOPOK_SHA256 = '63373512b29fe3cb5b3a37494c9b411da240df7270c2999c7821b264e2347447'

    @classmethod
    def setUpClass(cls):
        cls.sorok, _ = V.general('2026-11-09', ['H3176', 'H3027', 'H0157'])
        cls.i = {k: n for n, k in enumerate(V.FEJ)}

    def test_fejlec(self):
        self.assertEqual(V.FEJ[V.FEJ.index('szurt') + 1:], ['csoport', 'csoport_jel', 'proveniencia'])

    def test_csoport_a_jelentesponton_belul(self):
        i = self.i
        x = sor(self.sorok, strong='H3176', nyers='Job 14:14')[0]
        self.assertEqual((x[i['utvonal']], x[i['csoport']], x[i['csoport_jel']]), ("Pi'el/1", '+1', 'absolute'))
        x = sor(self.sorok, strong='H3176', nyers='Micah 5:6', utvonal="Pi'el/1")[0]
        self.assertEqual((x[i['csoport']], x[i['csoport_jel']]), ('', ''))  # a jelentés feje: nincs csoport
        x = sor(self.sorok, strong='H3176', nyers='Ezek 13:6', utvonal="Pi'el/2")[0]
        self.assertEqual((x[i['csoport']], x[i['csoport_jel']]), ('+1', 'followed by'))

    def test_utvonal_nem_kap_csoportot_es_jel_csak_csoporttal(self):
        i = self.i
        for x in self.sorok:
            self.assertNotIn('+', x[i['utvonal']])
            self.assertEqual(bool(x[i['csoport']]), bool(x[i['csoport_jel']]))

    def test_regi_oszlopok_bajtra_azonosak(self):
        import hashlib
        with open(V.KI, encoding='utf-8', newline='') as f:
            sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
        fej = sorok[0].split('\t')
        regi = [k for k in V.FEJ if k not in ('csoport', 'csoport_jel')]
        idx = [fej.index(k) for k in regi]
        h = hashlib.sha256()
        for s in sorok[1:]:
            m = s.split('\t')
            h.update(('\t'.join(m[j] for j in idx) + '\n').encode('utf-8'))
        self.assertEqual(h.hexdigest(), self.REGI_OSZLOPOK_SHA256)


class Ujrageneralas(unittest.TestCase):
    """ELLENOR_F99 3.: platformtól függetlenül fut (a kód- és a forrás-hash LF-re normalizált tartalomból számolódik)."""
    def test_bajtra_azonos(self):
        with open(V.KI, encoding='utf-8', newline='') as f:
            regi = f.read()
        ts = regi.split('--ts ', 1)[1].split(' ', 1)[0]
        sorok, mh = V.general(ts)
        self.assertEqual(V.kiir(sorok, mh, ts), regi)


if __name__ == '__main__':
    unittest.main(verbosity=1)
