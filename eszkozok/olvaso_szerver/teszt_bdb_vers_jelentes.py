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
        # DT-F131l (A): a tartomány („-25”) után álló folytatás („, 26”) sor lesz; a tartományt nem bontja ki
        h = B.hivatkozasok('H9999. x אב noun call 1Kin 18:24-25, 26; 2Kin 5:11; 4:25-26 x.')
        self.assertEqual([(x['konyv'], x['c'], x['v'], x['konyv_mod'], x['nyers']) for x in h],
                         [('1Kir', 18, 24, 'kiirt', '1Kin 18:24'), ('1Kir', 18, 26, 'folytatas', ', 26'),
                          ('2Kir', 5, 11, 'kiirt', '2Kin 5:11'), ('2Kir', 4, 25, 'orokolt', '4:25')])
        h = B.hivatkozasok('H9999. x אב noun Gen 18:18-19, 25-26; 22:18.')
        self.assertEqual([(x['c'], x['v'], x['konyv_mod']) for x in h], [(18, 18, 'kiirt'), (18, 25, 'folytatas'), (22, 18, 'orokolt')])
        # a tartomány utáni „, 1 Samuel” „1”-e könyvnév, nem folytatás
        h = B.hivatkozasok('H9999. x אב noun so 16:8-9, 1 Samuel 21:16 x.')
        self.assertEqual([(x['konyv'], x['c'], x['v']) for x in h], [(None, 16, 8), ('1Sám', 21, 16)])

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
        self.assertEqual(ok('in Moab (MI^10) Jer 48:1; compare Dr^Amos 4:9: Exod 10:13; Schr^COT Glossary and Isa 46:1.'),
                         ['sigla_kozel', 'sigla_tapadt', 'sigla_kozel', 'sigla_kozel'])
        # ezek a közeli-sigla szabály alá esnek (bizonytalan, a táblában maradnak), a tapadt alá nem
        self.assertEqual(ok('suffix (Kö^ii.l,74) Jer 6:13; (both R^D), Jer 6:24; ᵐ5^B Ezra 10:21; Isa^3 Isa 50:9; (compare R^D Josh 13:22).'),
                         ['sigla_kozel'] * 5)


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
                                                      'H8641', 'H0068', 'H1802', 'H0113', 'H8034'])

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
        # DT-F131k (a): a 2.31 hivatkozas_kezi sora (H8034 „26:35” → 26:25) a feloldott verset javítja; a nyers a forrás alakja
        i = {k: n for n, k in enumerate(V.FEJ)}
        x = sor(self.sorok, strong='H8034', nyers='26:35')[0]
        self.assertEqual((x[i['mt_vers']], x[i['karoli_vers']], x[i['okkod']], x[i['szurt']], x[i['utvonal']]),
                         ('1Móz 26:25', '1Móz 26:25', 'forras_javitas', '0', '-/3'))
        self.assertFalse(sor(self.sorok, strong='H8034', karoli_vers='1Móz 26:35'))

    def test_tartomany_utani_folytatas_a_tablaban(self):
        # DT-F131l (A): „1Kin 18:24-25, 26” → a 18:26 sor (folytatas); a 18:25 (tartomány) nem
        x = sor(self.sorok, strong='H8034', karoli_vers='1Kir 18:26')
        self.assertEqual([(s[V.FEJ.index('nyers')], s[V.FEJ.index('konyv_feloldas')]) for s in x], [(', 26', 'folytatas')])
        self.assertFalse(sor(self.sorok, strong='H8034', karoli_vers='1Kir 18:25'))

    def test_sigla_tahot_szerint(self):
        # DT-F99k: a sigla melletti hivatkozás bibliai marad, ha a TAHOT a versben hordozza a Strong-számot („De^Job 34:36”: אָבִי)
        x = sor(self.sorok, strong='H0015', nyers='Job 34:36')[0]
        self.assertEqual((x[V.FEJ.index('okkod')], x[V.FEJ.index('szurt')], x[V.FEJ.index('karoli_vers')]), ('sigla_igazolt', '0', 'Jób 34:36'))
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
