"""Olvasói pilot: tesztek (F60.1, M1).

Futtatás: python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py
Az adat.py-t ideiglenes könyvtárba futtatja mindkét szakaszra (a kimenet nem kerül a repóba), és
ellenőrzi: a szakasz-feloldást, a fő szó választását, a görög szóalak párosítását, a BDB-bontást,
a proveniencia-sorokat, a „csak adat” ellenőrzőlistát (minden blokk-cím kap jelleg-címkét és
adatforrást; nincs feladatszám az oldalon).
Regresszió (K1): a TestRegresszioProto a prototípus (ce4ef98f) adat.py-ját a gitből ideiglenes fájlba írja, lefuttatja, és az
1Móz 1:1–2:3 kimenet minden kulcsának értékét összeveti (kivétel: ts= és az indokolt, darabszámmal megadott ENGEDELYEZETT lista).
A TestTeljes1Moz1_25 az 1Móz 1–25-öt (693 vers, ~30 s) futtatja. A TestKiadas az adat.py --kiadas kapcsolót ellenőrzi (DT-F60a).
A bővítés (F60.5) és a Szó / Vers részletei fülváltás (hidden szabály) tesztjei is itt vannak."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import warnings

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

warnings.simplefilter('ignore', ResourceWarning)
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import szakasz as sz  # noqa: E402

GY = sz.GY
TMP = tempfile.mkdtemp(prefix='olvaso_pilot_teszt_')
SZAKASZOK = {'gen': '1Móz 1:1-2:3', 'zsolt': 'Zsolt 22'}
ADAT = {}


def futtat(szakasz, ki):
    p = subprocess.run([sys.executable, os.path.join(D, 'adat.py'), '--szakasz', szakasz, '--kimenet', ki],
                       capture_output=True, text=True, encoding='utf-8')
    if p.returncode:
        raise RuntimeError('adat.py hiba (%s): %s' % (szakasz, p.stderr[-800:]))
    return json.load(open(os.path.join(ki, 'olvaso_pilot.json'), encoding='utf-8'))


def setUpModule():
    for k, v in SZAKASZOK.items():
        ADAT[k] = futtat(v, os.path.join(TMP, k))


def vers(d, ig):
    return next(v for v in d['versek'] if v['igehely'] == ig)


class SzakaszFeloldas(unittest.TestCase):
    def test_parse_es_cim(self):
        self.assertEqual(sz.szakasz_cim('1Móz 1:1-2:3'), '1Móz 1:1–2:3')
        self.assertEqual(sz.szakasz_cim('Zsolt 22'), 'Zsolt 22')
        self.assertEqual(sz.szakasz_cim('Zsolt 22:1-5'), 'Zsolt 22:1–5')
        self.assertEqual(sz.szakasz_azonosito('1Móz 1:1-2:3'), '1Moz_1_1-2_3')

    def test_versek(self):
        g = sz.szakasz_versei('1Móz 1:1-2:3')
        self.assertEqual((len(g), g[0], g[30], g[31], g[-1]), (34, '1Móz 1:1', '1Móz 1:31', '1Móz 2:1', '1Móz 2:3'))
        z = sz.szakasz_versei('Zsolt 22')
        self.assertEqual((len(z), z[0], z[-1]), (32, 'Zsolt 22:1', 'Zsolt 22:32'))

    def test_ismeretlen_konyv_megall(self):
        with self.assertRaises(SystemExit):
            sz.szakasz_versei('Ésa 1:1-3')

    def test_kimenet_a_repon_kivul(self):
        for s in SZAKASZOK.values():
            self.assertFalse(os.path.abspath(sz.alap_kimenet(s)).replace('\\', '/').startswith(GY.rstrip('/')))


class FoSzo(unittest.TestCase):
    def test_1moz_1_4(self):
        v = vers(ADAT['gen'], '1Móz 1:4')
        fo = {w['szo'].strip('.,;'): w['fo'] for w in v['hu_szavak']}
        self.assertEqual(fo['világosságot'], 'H0216')   # a בֵּין + אוֹר közül a tartalmas szó
        self.assertEqual(fo['setétségtől'], 'H2822')    # a מִן prefixum helyett


class GorogSzoalak(unittest.TestCase):
    def test_1moz_1_1_arche(self):
        w = next(x for x in vers(ADAT['gen'], '1Móz 1:1')['heber'] if x['strong'] == 'H7225')
        m = w['macula']
        self.assertEqual(m['lxx'], 'ἀρχῇ')
        self.assertEqual(m['lxx_forras'], 'LXX_OS')
        self.assertEqual(m['lxx_macula'], 'ἀρξῇ')       # a Macula szóalakja χ/ξ-hibás


class BdbBontas(unittest.TestCase):
    def jelek(self, d, h):
        a = d['lapok'][h]['appar']
        return [(j['jel'], [s['jel'] for s in j['al']]) for t in a['torzsek'] for j in t['jelentesek']]

    def test_h7225(self):
        self.assertEqual(self.jelek(ADAT['gen'], 'H7225'), [('1', ['a', 'b']), ('2', [])])

    def test_h0216(self):
        self.assertEqual(len(self.jelek(ADAT['gen'], 'H0216')), 11)


class Zsolt22(unittest.TestCase):
    def test_lefut_es_hossza(self):
        d = ADAT['zsolt']
        self.assertEqual(len(d['versek']), 32)
        self.assertTrue(d['lapok'])
        self.assertTrue(all(v['karoli'] for v in d['versek']))

    def test_felirat_van_lxx(self):
        # a 22:1 a felirat (Károli = MT-számozás); az F54 óta (zsolt_felirat_eltolas) az LXX_OS ehhez a versszámhoz
        # a LXX 21:1 feliratát köti (a korábbi „nincs LXX-szó” állapot megszűnt)
        self.assertGreater(len(vers(ADAT['zsolt'], 'Zsolt 22:1')['lxx']), 0)
        self.assertGreater(len(vers(ADAT['zsolt'], 'Zsolt 22:2')['lxx']), 0)

    def test_versszam_eltereskor_jelzes(self):
        self.assertEqual(vers(ADAT['zsolt'], 'Zsolt 22:32')['versszam']['kjv'], '')

    def test_versszam_tablak_ellentmondasa(self):
        # a versmegfeleltető tábla szerint Károli 22:2 = KJV 22:2; az LXX_OS saját KJV-oszlopa szerint 22:1
        vs = vers(ADAT['zsolt'], 'Zsolt 22:2')['versszam']
        self.assertEqual((vs['kjv'], vs['kjv_lxx']), ('22:2', '22:1'))

    def test_kh_kulcs_normalizalva(self):
        # a Karoli_kereszthivatkozasok STEPBible-alakú (Psa.22.2); a normalizálás nélkül üres lenne
        self.assertTrue(any(v['karoli_kh'] for v in ADAT['zsolt']['versek']))


class Proveniencia(unittest.TestCase):
    def test_minden_prov_sor(self):
        for k, d in ADAT.items():
            for kulcs, s in d['prov'].items():
                self.assertRegex(s, r'^scope=.+ \| forras=.+ \| ts=\d{4}-\d\d-\d\dT\d\d:\d\dZ$', (k, kulcs))

    def test_scope_a_szakasz(self):
        self.assertIn('scope=1Móz 1:1–2:3', ADAT['gen']['prov']['heber'])
        self.assertIn('scope=Zsolt 22', ADAT['zsolt']['prov']['heber'])
        self.assertIn('LXX_OS/psalms-lxx.tsv', ADAT['zsolt']['prov']['lxx'])
        self.assertIn('parok_Zsolt.tsv', ADAT['zsolt']['prov']['parok'])
        self.assertIn('parok_1Moz.tsv', ADAT['gen']['prov']['parok'])


def sablon():
    return open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()


class CsakAdat(unittest.TestCase):
    """Az ellenőrzőlista gépi része (M1): minden blokk-cím jelleg-címkét és adatforrást kap."""

    def sugo(self):
        s = sablon()
        blokk = s[s.index('const SUGO = ['):s.index('];', s.index('const SUGO = ['))]
        out = []
        for sor in blokk.split('\n')[1:]:
            m = re.match(r"^\s*\['([^']+)', \[(.*)\], \[([^\]]*)\]\],?\s*$", sor)
            if m:
                forrasok = re.findall(r"\['([^']+)',", m.group(2))
                jellegek = re.findall(r"'([^']+)'", m.group(3))
                out.append((m.group(1), forrasok, jellegek))
        return out

    def cimek(self):
        s = sablon()
        out = []
        for m in re.finditer(r"el\('h[34]',\s*\{[^}]*?text:\s*(`[^`]*`|'(?:[^'\\]|\\.)*')", s):
            t = m.group(1)[1:-1]
            out.append(re.sub(r'\$\{[^}]*\}', 'X', t))
        for t in re.findall(r"el\('h[34]',\s*\{[^}]*?text:\s*hu \? '([^']+)' : '([^']+)'", s):
            out.extend(t)
        return out

    def illeszt(self, cim, sugo):
        for k, f, j in sugo:
            if cim == k or (cim.startswith(k) and not re.match(r'[a-zA-ZáéíóöőúüűÁÉÍÓÖŐÚÜŰ]', cim[len(k)])):
                return k, f, j
        return None

    def test_minden_cim_kap_jelleget_es_forrast(self):
        sugo = self.sugo()
        self.assertGreater(len(sugo), 10)
        cimek = self.cimek()
        self.assertGreater(len(cimek), 15)
        for c in cimek:
            ill = self.illeszt(c, sugo)
            self.assertIsNotNone(ill, 'nincs jelleg/forrás a blokk-címhez: %r' % c)
            self.assertTrue(ill[1] and ill[2], c)
            for j in ill[2]:
                self.assertIn(j, ('forras', 'gepi', 'modell'))

    def test_jelleg_helyes_a_kenyes_blokkokon(self):
        sugo = self.sugo()
        # a Károli–Strong párosításon alapuló blokkok modell-kimenetek
        for c in ('Így fordítja Károli', 'Károli-szöveg', 'Ebben a versben (X)', 'Szó adatai (héber)'):
            self.assertIn('modell', self.illeszt(c, sugo)[2], c)
        # a héber BDB-lap címe a BDB-ként címkézett, nem a TBESG-ként
        self.assertEqual(self.illeszt('Jelentés (BDB, magyarul)', sugo)[0], 'Jelentés (BDB')
        self.assertEqual(self.illeszt('Jelentés (BDB)', sugo)[0], 'Jelentés (BDB')
        self.assertEqual(self.illeszt('Jelentés', sugo)[1], ['TBESG'])
        # a magyar fordítások modell-kimenetek
        self.assertIn('modell', self.illeszt('Jelentés magyarul', sugo)[2])
        self.assertIn('modell', self.illeszt('BDB-szócikk apparátusokra bontva (magyarul)', sugo)[2])

    def test_sugo_adatkeszletek_a_licenctablaban(self):
        kulcsok = set()
        for s in open(GY + 'adat/licencek.tsv', encoding='utf-8'):
            if s.startswith('#') or s.startswith('dataset'):
                continue
            kulcsok.add(s.split('\t')[0])
        for k, f, j in self.sugo():
            for x in f:
                self.assertIn(x, kulcsok, 'a(z) %s nincs az adat/licencek.tsv-ben (blokk: %s)' % (x, k))

    def test_forras_kulcsok_vannak_a_prov_ban(self):
        kulcsok = set()
        for m in re.finditer(r"forras\(([^)]*)\)", sablon()):
            kulcsok.update(re.findall(r"'([^']+)'", m.group(1)))
        for d in ADAT.values():
            for k in kulcsok:
                self.assertIn(k, d['prov'])

    def test_nincs_feladatszam_es_szakaszra_rogzitett_szoveg(self):
        s = sablon()
        szoveg = re.sub(r'<style>.*?</style>', '', s, flags=re.S)
        self.assertEqual(re.findall(r'(?<![\w&#])#\d{1,3}\b(?!\w)', re.sub(r'#[0-9a-fA-F]{3,6}\b', '', szoveg)), [])
        self.assertNotIn('1Mózes 1:1–2:3', s)
        self.assertNotIn('genesis.tsv', s)
        self.assertNotIn("'H0430'", s)

    def test_a_kenyes_sorok_jelleg_cimkei(self):
        s = sablon()
        for ez in ('forrásadat', 'gépi feldolgozás', 'modell-kimenet'):
            self.assertIn(ez, s)


class Bovites(unittest.TestCase):
    """F60.5 (v2): a bővítés blokkjai és a vers-kulcsok."""

    def test_szolap_uj_mezok(self):
        l = ADAT['gen']['lapok']['H0216']
        for k in ('domen', 'sece', 'oshl', 'tbesh'):
            self.assertTrue(l.get(k), k)
        g = ADAT['gen']['gor_lapok']
        self.assertTrue(any(x.get('lsj') for x in g.values()))
        self.assertTrue(any(x.get('mcged') for x in g.values()))
        self.assertTrue(any(x.get('ubs_en') for x in g.values()))
        self.assertTrue(any(x.get('domen') for x in g.values()))

    def test_tw_hivatkozasok_feloldhatok(self):
        for d in ADAT.values():
            for lap in list(d['lapok'].values()) + list(d['gor_lapok'].values()):
                for tid in lap.get('tw', []):
                    self.assertIn(tid, d['tw_cikkek'])

    def test_bsb_kjv_1moz_1_1(self):
        a = vers(ADAT['gen'], '1Móz 1:1')['angol']
        self.assertEqual(a['bsb']['kulcs'], 'Gen.1.1')
        self.assertEqual((a['bsb']['szavak'][0]['strong'], a['bsb']['szavak'][0]['szo']), ('H7225', 'In the beginning'))
        self.assertEqual(a['kjv']['szavak'][0]['szo'], 'beginning')

    def test_zsolt22_versszam_kulcsok(self):
        # Károli (MT) 22:3 = BSB Psa.22.3 (mt) = KJV 22:2; Károli 22:2 = KJV 22:1; a felirat (22:1) = KJV 22:0
        d = ADAT['zsolt']
        v3 = vers(d, 'Zsolt 22:3')
        self.assertEqual((v3['angol']['bsb']['kulcs'], v3['angol']['kjv']['kulcs']), ('Psa.22.3', 'Psa.22.2'))
        self.assertEqual(v3['angol']['bsb']['szavak'][0]['szo'], 'I cry out')
        self.assertEqual(vers(d, 'Zsolt 22:2')['angol']['kjv']['kulcs'], 'Psa.22.1')
        v1 = vers(d, 'Zsolt 22:1')['angol']
        self.assertEqual(v1['kjv']['kulcs'], 'Psa.22.0')
        self.assertEqual(len(v1['kjv']['szavak']), 5)
        self.assertEqual(vers(d, 'Zsolt 22:32')['versszam']['kjv_kulcs'], '22:31')

    def test_zsolt22_bsb_hiany_jelezve_nem_potolva(self):
        # a BSB-táblában nincs Psa.22.1 és Psa.22.2: üres marad (nem tölti ki szomszéd vers)
        for ig in ('Zsolt 22:1', 'Zsolt 22:2'):
            self.assertEqual(vers(ADAT['zsolt'], ig)['angol']['bsb']['szavak'], [])

    def test_versmegfeleltetes_tabla_ellentmondas_jelezve(self):
        self.assertTrue(vers(ADAT['zsolt'], 'Zsolt 22:5')['versszam']['tabla_ellentmond'])
        self.assertFalse(vers(ADAT['gen'], '1Móz 1:5')['versszam']['tabla_ellentmond'])

    def test_nave_tartomany_bontasa(self):
        x = [n for n in vers(ADAT['gen'], '1Móz 1:27')['nave'] if n['hely'] == '1Móz 1:26-28']
        self.assertTrue(x and all(n['tart'] for n in x))
        self.assertFalse([n for n in vers(ADAT['gen'], '1Móz 1:29')['nave'] if n['hely'] == '1Móz 1:26-28'])

    def test_nave_kjv_szamozas_zsolt22(self):
        # a Nave KJV-számozású: Zsolt 22:1 (KJV) = Károli 22:2
        d = ADAT['zsolt']
        self.assertTrue(any(n['cimke'] == 'DESPONDENCY IN' for n in vers(d, 'Zsolt 22:2')['nave']))
        self.assertFalse(any(n['cimke'] == 'DESPONDENCY IN' for n in vers(d, 'Zsolt 22:1')['nave']))

    def test_tipnr_illesztes(self):
        self.assertEqual([x['nev'] for x in vers(ADAT['gen'], '1Móz 1:1')['tipnr']], ['LORD'])
        z = vers(ADAT['zsolt'], 'Zsolt 22:1')['tipnr']
        self.assertEqual([(x['nev'], x['illesztes']) for x in z], [('David', 'MT-szám')])
        self.assertEqual(ADAT['zsolt']['stat']['tipnr_nem_illeszkedo'], [])

    def test_adatreteg_sorok(self):
        g = ADAT['gen']['stat']
        self.assertEqual((g['motivum_sor'], g['kapcsolat_sor']), (2, 3))
        self.assertEqual(vers(ADAT['gen'], '1Móz 1:2')['motivum'][0]['proveniencia'][:6], 'scope=')
        z = ADAT['zsolt']['stat']
        self.assertEqual((z['motivum_sor'], z['kapcsolat_sor'], z['lxx_dontes_sor']), (0, 0, 0))

    def test_morf_feloldas(self):
        w = next(x for x in vers(ADAT['gen'], '1Móz 1:1')['heber'] if x['strong'] == 'H1254')['macula']
        self.assertEqual(w['morf'], 'Vqp3ms')   # a nyers kód megmarad
        self.assertEqual(w['morf_hu'], 'ige, qal, perfectum (qatal), harmadik személy, hímnem, egyes szám')
        for d in ADAT.values():
            self.assertEqual(d['stat']['morf_ismeretlen'], 0)

    def test_morf_aramai(self):
        from bovites import MorfKulcs
        mk = MorfKulcs(GY)
        self.assertIn('peal', mk.dekodol('Vqp3ms', 'A'))
        self.assertIn('qal', mk.dekodol('Vqp3ms', 'H'))
        self.assertEqual(mk.dekodol('Vqc'), 'ige, qal, infinitivus constructus')
        self.assertEqual(mk.dekodol('C'), 'kötőszó')

    def test_bdb_alias_zsolt22(self):
        # a H0136 és a H7358 szócikke másik Strong-szám alatt áll (BDB_strong_alias.tsv): a lap jelzi, nem üres
        l = ADAT['zsolt']['lapok']
        for s, tabla in (('H0136', 'H0113'), ('H7358', 'H7356')):
            self.assertEqual(l[s]['bdb_alias']['tabla_strong'], tabla)
            self.assertTrue(l[s]['bdb_hu'] or l[s]['bdb_en'])
        # ahol van saját szócikk, nincs alias
        self.assertIsNone(l['H0001']['bdb_alias'] if 'H0001' in l else None)
        self.assertFalse(any(x['bdb_alias'] for x in ADAT['gen']['lapok'].values()))

    def test_domen_ut_es_usz_jelentes(self):
        d = ADAT['gen']['lapok']['H0216']['domen'][0]
        self.assertTrue(d['ut'])
        g = ADAT['gen']['gor_lapok']
        self.assertTrue(any(x['ubs'] for l in g.values() for x in l['usz_versek']))

    def test_licenc_jelzes(self):
        j = ADAT['gen']['licenc_jelzes']
        self.assertEqual(j['MCGED']['kereskedelmi'], 'nem')
        self.assertEqual(j['KJV_Strongs_teljes']['allapot'], 'tisztazatlan')

    def test_json_merete_a_hataron_belul(self):
        for k in SZAKASZOK:
            self.assertLess(os.path.getsize(os.path.join(TMP, k, 'olvaso_pilot.json')), 8 * 1024 * 1024)


class FulvaltasHidden(unittest.TestCase):
    """A Szó / Vers részletei fülváltás (F60.4 javítás): a hidden attribútum tényleges elrejtést ad.
    Böngésző nélküli statikus ellenőrzés: a sablon CSS-ében minden olyan elemre, amelyen a JS a hidden
    attribútumot kapcsolja, van [hidden] { display: none } szabály (különben a display: grid felülírja)."""

    def css(self):
        return re.search(r'<style>(.*?)</style>', sablon(), re.S).group(1)

    def test_section_lap_hidden_szabaly(self):
        self.assertRegex(self.css(), r'section\.lap\[hidden\]\s*\{\s*display:\s*none;?\s*\}')

    def test_kartya_hidden_szabaly(self):
        self.assertRegex(self.css(), r'\.kartya\[hidden\]\s*\{\s*display:\s*none;?\s*\}')

    def test_minden_display_szabaly_elemre_van_hidden_szabaly(self):
        # a JS-ben hidden-nel kapcsolt elemek: #szolap, #verslap (section.lap) és a .kartya
        css = self.css()
        for sel in ('section.lap', '.kartya'):
            self.assertRegex(css, re.escape(sel) + r'\s*\{[^}]*display:\s*grid')
            self.assertIn(sel + '[hidden]', css, sel)

    def test_a_js_a_hidden_tulajdonsagot_kapcsolja(self):
        s = sablon()
        self.assertIn("szolap.hidden = ful !== 'szo'", s)
        self.assertIn("verslap.hidden = ful !== 'vers'", s)
        self.assertRegex(s, r'<section class="lap" id="verslap"[^>]*\bhidden\b')


class LathatoForras(unittest.TestCase):
    """F60.11: minden blokk fejléce alatt látható forrássor áll (nem csak a „?” súgóban)."""

    def test_forrassor_a_fejlec_utan(self):
        s = sablon()
        self.assertIn("sor.after(forrasSor(s[1]))", s)
        self.assertIn("class: 'forrasnev'", s)

    def test_bdb_alszakaszok_forrassort_kapnak(self):
        s = sablon()
        self.assertRegex(s, re.compile(r"const resz = .{0,300}forrasnev.{0,200}BDB \(Brown", re.S))

    def test_minden_suggo_forras_kulcsnak_van_olvashato_neve(self):
        s = sablon()
        kulcsok = set(re.findall(r"\['([A-Za-z_]+)', '", s[s.index('const SUGO'):s.index('const FORRAS_NEV')]))
        kulcsok.discard('forras')
        nevek = s[s.index('const FORRAS_NEV'):s.index('const forrasSor')]
        hianyzo = sorted(k for k in kulcsok if k + ':' not in nevek)
        self.assertEqual(hianyzo, [])

    def test_legkisebb_betumeret_12px(self):
        css = re.search(r'<style>(.*?)</style>', sablon(), re.S).group(1)
        for m in re.finditer(r'font(?:-size)?:\s*(?:\d+\s+)?(\d+(?:\.\d+)?)px', css):
            self.assertGreaterEqual(float(m.group(1)), 12, m.group(0))


class SzinseMa(unittest.TestCase):
    """F60.12: világos/sötét/rendszer színséma-váltó; a tárolás csak try/catch-ben; a világos paletta az alap."""

    def test_valto_es_alap_paletta(self):
        s = sablon()
        self.assertIn('data-tema="light"', s)
        self.assertIn('data-tema="dark"', s)
        self.assertIn('data-tema="rendszer"', s)
        self.assertRegex(s, r':root\s*\{\s*--bg:\s*#f5f2ea')
        self.assertIn(':root[data-theme="dark"]', s)

    def test_localstorage_csak_trycatch_ben(self):
        s = sablon()
        for m in re.finditer(r'localStorage\.(get|set)Item', s):
            elotte = s[max(0, m.start() - 60):m.start()]
            self.assertIn('try', elotte, m.group(0))


class AlapNyitva(unittest.TestCase):
    """F60.13: a blokkok alapból nyitva; a „Forrás” (details.forras) és a „?” súgó (details.sugo) zárva marad."""

    def test_mindnyit_kizarasokkal(self):
        s = sablon()
        self.assertIn("details:not(.forras):not(.sugo)", s)
        self.assertIn("mindNyit(verslap)", s)
        self.assertIn("mindNyit(szolap)", s)


class LxxKiemeles(unittest.TestCase):
    """F60.14: a vers-lap LXX-sorában az aktuális héber szó görög párja ki van emelve; a szó-lap LXX-sorai átkattinthatók."""

    def test_par_kiemeles_es_tartalek(self):
        s = sablon()
        self.assertIn("(par ? ' par' : '')", s)
        self.assertIn("parAlakok", s)
        self.assertIn("aria-current", s)

    def test_szo_lap_lxx_sorok_atkattinthatok(self):
        s = sablon()
        i = s.index("Görög megfelelő a Septuagintában")
        blokk = s[i:i + 1200]
        self.assertIn("kivalaszt(x.strong)", blokk)
        self.assertIn("D.gor_lapok[x.strong]", blokk)
        self.assertIn("role: gk ? 'button'", blokk)


class ZarojelesElozoCikk(unittest.TestCase):
    """F60.17: a [gyök] előszócikkel induló BDB-sorban az „I. <lemma>” homonima a Strong-számé (H6030: „felelni”, nem „lakni”)."""

    def test_h6030_alapjelentes_felelni(self):
        import bdb_szelet
        hu = ("H6030. anah [עוּן] ige: lakni (valószínűleg; √, a következőé); — Qal perfectum Ézs 13:22 és sakálok laknak. "
              "I. עָנָה ige: felelni, válaszolni (késői héber); — Qal perfectum 1Móz 41:16.")
        r = bdb_szelet.szeletel(hu, 'עָנָה')
        self.assertEqual(r['fej']['heber'], 'עָנָה')
        self.assertTrue(r['alap'].startswith('ige: felelni'))
        self.assertIn('lakni', r['elotag'])

    def test_masik_lemma_nem_cserel(self):
        import bdb_szelet
        hu = ("H5222. nekeh [נֵכֶה] adjective id.; — plural נֵכִים Psa 35:15 smitten ones "
              "I. נָכוֺן noun [masculine] = blow Job 12:5")
        r = bdb_szelet.szeletel(hu, 'נֵכֶה')
        self.assertEqual(r['elotag'], '')

    def test_lemma_nelkul_is_marad_a_regi_viselkedes_ha_nincs_homonima(self):
        import bdb_szelet
        r = bdb_szelet.szeletel("H0001. av [אָב] noun father; — 1. father Gen 2:24.", 'אָב')
        self.assertEqual(r['elotag'], '')


class HomonimaSzakaszok(unittest.TestCase):
    """F60.18: egy BDB-sor több szócikke (zárójeles előszócikk, I./IV. homonimák, arámi Pe`al rész) külön szakasz; a Strong-lemma dönt."""

    HU = ("H6030. anah [עוּן] ige: lakni (valószínűleg); — Qal perfectum Ézs 13:22 és sakálok laknak. — Zsolt 87:7, l. מַעְיָן. "
          "I. עָנָה ige: felelni, válaszolni (késői héber); — Qal perfectum Mik 6:5; imperfectum יַעֲנֶה 1Móz 41:16; — 1 felelni, 1Sám 4:20. "
          "Hiph`il participium Préd 5:19, teljesen kétséges. "
          "IV. עָנָה ige: énekelni (arab); — Qal perfectum Jer 51:14; — énekelni, Kiv 15:21. "
          "I. [עֲנָה] ige: felelni (l. bibliai héber I. עָנָה); — Pe`al perfectum Dán 5:10; — 1 felelni, Dán 2:5, 7.")

    def setUp(self):
        import bdb_szelet
        self.r = bdb_szelet.szeletel(self.HU, 'עָנָה')

    def test_fo_szakasz_a_strong_lemma(self):
        self.assertEqual(self.r['fej']['heber'], 'עָנָה')
        self.assertTrue(self.r['alap'].startswith('ige: felelni'))

    def test_hiphil_nem_olvassa_be_az_arami_reszt(self):
        hiphil = [t for t in self.r['torzsek'] if t['nev'].startswith('Hiph')]
        self.assertEqual(len(hiphil), 1)
        szoveg = ' '.join(j['szoveg'] for j in hiphil[0]['jelentesek'])
        self.assertNotIn('Dán', szoveg)

    def test_szakaszok_szerepei(self):
        sz = {(x['szerep'], x['nyelv'], x['jel']) for x in self.r['szakaszok']}
        self.assertIn(('elo', 'héber', ''), sz)
        self.assertIn(('azonos_lemma', 'héber', 'IV'), sz)
        self.assertTrue(any(x['nyelv'] == 'arámi' for x in self.r['szakaszok']))
        arami = [x for x in self.r['szakaszok'] if x['nyelv'] == 'arámi'][0]
        self.assertTrue(any(t['nev'].startswith('Pe') for t in arami['torzsek']))

    def test_egyszeru_szocikk_valtozatlan(self):
        import bdb_szelet
        r = bdb_szelet.szeletel("H0001. av [אָב] noun father; — 1. father Gen 2:24.", 'אָב')
        self.assertEqual(r['szakaszok'], [])


class TbeshSorrend(unittest.TestCase):
    """F60.18: a TBESH-sorok közül a Strong-lemmához és a rövid jelentéshez illő kerül előre (H6030b „answer”, nem H6030a „dwell”)."""

    def sorok(self):
        return [{'estrong': 'H6030a', 'lemma': 'עוּן', 'gloss': 'to dwell'},
                {'estrong': 'H6030b', 'lemma': 'עָנָה', 'gloss': 'to answer'},
                {'estrong': 'H6030c', 'lemma': 'עָנָה', 'gloss': 'to sing'}]

    def test_h6030(self):
        import bovites
        r = bovites._tbesh_sorrend(self.sorok(), 'עָנָה', 'to answer')
        self.assertEqual([x['estrong'] for x in r], ['H6030b', 'H6030a', 'H6030c'])
        self.assertEqual([x['elsodleges'] for x in r], [True, False, False])

    def test_egy_sor_es_nincs_egyezes_valtozatlan(self):
        import bovites
        egy = [{'estrong': 'H0001', 'lemma': 'אָב', 'gloss': 'father'}]
        self.assertEqual(bovites._tbesh_sorrend(egy, 'אָב', 'father'), egy)
        sok = self.sorok()
        self.assertEqual(bovites._tbesh_sorrend(sok, 'שׁלום', 'peace'), sok)


class AlapjelentesAFejlecben(unittest.TestCase):
    """F60.19: a szó-lap fejlécmezőjében (lemma, Strong, kiejtés, szófaj mellett) az alapjelentés is szerepel."""

    def test_heber_es_gorog_fejlec(self):
        s = sablon()
        self.assertIn("class: 'alapjel'", s)
        self.assertIn("function alapjelentes(l)", s)
        self.assertIn("alapjelentes(l) ? el('p', { class: 'alapjel'", s)
        self.assertIn("l.gloss ? el('p', { class: 'alapjel'", s)

    def test_heber_fejlec_forrasai_kozott_a_bdb(self):
        s = sablon()
        sor = [x for x in s.splitlines() if x.strip().startswith("['Szó adatai (héber)'")][0]
        self.assertIn("['BDB'", sor)
        self.assertIn('modell', sor)


class AlapjelentesTisztitas(unittest.TestCase):
    """F60.21: a szó-lap fejlécének alapjelentése a bdb_szelet.alap_jelentes függvényből jön (magyar BDB-sor gépi tisztítása):
    héber betű, forrás-hivatkozás, szófaji szó és átírás-maradék nélkül; ha nem marad használható szöveg, None (a Strong-rövid jelentés áll)."""

    ESETEK = [
        ("ige: felelni, válaszolni", "ige: felelni, válaszolni", False),
        ("אֶחָב, אַחְאָב, אָח stb. l. אחה. I. אָח_630 hímnemű főnév: testvér, fivér", "testvér, fivér", True),
        ("דָּוִד,_1066 tulajdonnév, hímnemű: Dávid, יִשַׂי fia, Izráel királya", "Dávid", True),
        ("lel vagy layelah לַ֫יִל לַ֫יְלָה,_242 hímnemű főnév^1Móz 40:5 éjszaka", "éjszaka", True),
        ("hímnemű שֵׁנִית nőnemű_157 melléknév: sorszámnév: második", "második", True),
        ("nőnemű főnév^5Móz 8:4 , láb", "láb", True),
        ("nőnemű főnév : év", "év", True),
        ("hímnemű főnév^Mal 3:1 úr", "úr", True),
        ("אָֽנֹכִ֫י (egyszer Jób 33:9) névmás, 1. személy egyes szám, közös nem: én; 1Móz 3:10", "én", True),
        ("isten, אֶלְדָּעָה אֶלְדָּד stb. l. I. אלה. II. אֵל hímnemű főnév isten, de különféle alárendelt alkalmazásokban a hatalom fogalmának kifejezésére", "isten", True),
    ]

    def test_esetek(self):
        import bdb_szelet
        for alap, vart, tisztitott in self.ESETEK:
            r = bdb_szelet.alap_jelentes(alap)
            self.assertIsNotNone(r, alap)
            self.assertEqual(r['szoveg'], vart, alap)
            self.assertEqual(r['tisztitott'], tisztitott, alap)

    def test_a_kimenet_tiszta(self):
        import bdb_szelet
        for alap, _, _ in self.ESETEK:
            sz = bdb_szelet.alap_jelentes(alap)['szoveg']
            self.assertIsNone(re.search(r'[\u0590-\u05ff\ufb1d-\ufb4f]', sz), sz)
            self.assertNotIn('^', sz)
            self.assertNotIn('_', sz)

    def test_nincs_hasznalhato_jelentes(self):
        import bdb_szelet
        self.assertIsNone(bdb_szelet.alap_jelentes('hímnemű többes számú főnév'))
        self.assertIsNone(bdb_szelet.alap_jelentes('ige'))
        self.assertIsNone(bdb_szelet.alap_jelentes('igenévi melléknév l. fent participium'))
        self.assertIsNone(bdb_szelet.alap_jelentes(''))
        self.assertIsNone(bdb_szelet.alap_jelentes(None))

    def test_a_sablon_a_kesz_mezot_hasznalja(self):
        s = sablon()
        self.assertIn("const a = l.alapjelentes;", s)
        self.assertNotIn("function tisztitAlap", s)   # a tisztítás a szeletelőben él, nem az oldalon

    def test_az_adat_py_kitolti_a_mezot(self):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adat.py'), encoding='utf-8').read()
        self.assertIn("_l['alapjelentes'] = alap_jelentes(", src)


class BdbFejlec(unittest.TestCase):
    """F60.23: a BDB-sor eleje (H4100 típus): átírás-változatok után az első héber szó a címszó; a „… — megjegyzés — <szófaj>: jelentés”
    szerkezetben a szófajos szakasz az alapjelentés; a zárójelben álló számok („(Da^§ 8, R. 2 K?:iii. 23 k.)”) nem jelentés-sorszámok."""

    H4100 = ("H4100. mah vagy ma- vagy meh מָה, ritkán מָהֿ (pl. 1Móz 31:43), מָ (csak a מָהֵם Ez 8:6 Kt. helyen) "
             "— ezen alakok használatának különbségéről l. Ges^§ 37 — kérdő és határozatlan névmás: mi? hogyan? valami; "
             "dolgokról használatos (arámi , מָא, arab ; valószínűleg egy n-es hosszabb alak, asszír minû): — "
             "1 kérdő: mi ? a. egyenes kérdésben, igék vagy főnevek előtt 1Móz 4:10 mit tettél ? "
             "b. gyakran függő kérdésben, Péld 25:8 (Da^§ 8, R. 2 K?:iii. 23 k.); felkiáltásként, Zsolt 89:48b. "
             "2 határozószóként használva: a. kérdőszóként: hogyan ? b. felkiáltásként: mily ... Jób 26:2-3,. "
             "3 határozatlan névmás: valami, bármi, 4Móz 23:3. "
             "4 Elöljárószókkal: a. בַּמָּה miben ? 2Móz 22:26; b. מֶה יַעַן Hag 1:9 mi miatt ?")

    def setUp(self):
        import bdb_szelet
        self.r = bdb_szelet.szeletel(self.H4100, 'מָה')

    def test_cimszo_a_heber_szo(self):
        self.assertEqual(self.r['fej']['heber'], 'מָה')
        self.assertEqual(self.r['fej']['atiras'], 'mah vagy ma- vagy meh')

    def test_alapjelentes_a_szofajos_szakasz(self):
        self.assertTrue(self.r['alap'].startswith('kérdő és határozatlan névmás'))
        self.assertTrue(any('arámi' in x for x in self.r['nyelvi']))
        self.assertIn('Ges^§ 37', self.r['alaktan'])

    def test_zarojelben_allo_szam_nem_jelolo(self):
        jelek = [j['jel'] for j in self.r['torzsek'][0]['jelentesek']]
        self.assertEqual(jelek, ['1', '2', '3', '4'])
        elso_al = [a['jel'] for a in self.r['torzsek'][0]['jelentesek'][0]['al']]
        self.assertEqual(elso_al, ['a', 'b'])

    def test_alapjelentes_a_fejlecbe(self):
        import bdb_szelet
        self.assertEqual(bdb_szelet.alap_jelentes(self.r['alap'])['szoveg'], 'kérdő és határozatlan névmás: mi? hogyan? valami')

    def test_zarojelben_segedfuggveny(self):
        import bdb_szelet
        s = "a (b 2 c) d 2 e"
        bent = bdb_szelet._zarojelben(s)
        self.assertTrue(bent[s.index('2')])
        self.assertFalse(bent[s.rindex('2')])
        # lezáratlan zárójel nem némít el mindent utána
        s2 = "a (b" + " x" * 300 + " 2 y"
        self.assertFalse(bdb_szelet._zarojelben(s2)[s2.rindex('2')])

    def test_egyszeru_fejlec_valtozatlan(self):
        import bdb_szelet
        r = bdb_szelet.szeletel("H0001. av [אָב] noun father; — 1. father Gen 2:24.", 'אָב')
        self.assertEqual(r['fej']['heber'], 'אָב')
        self.assertEqual(r['fej']['atiras'], 'av')
        r2 = bdb_szelet.szeletel("H1732. David דָּוִד,_1066 tulajdonnév, hímnemű: Dávid", 'דָּוִד')
        self.assertEqual((r2['fej']['heber'], r2['fej']['ossz']), ('דָּוִד', '1066'))


class BdbSzeletelesAtnezes(unittest.TestCase):
    """F60.35: az F60.25 által megváltoztatott 19 szócikk (és három, az átnézés közben talált eset) várt törzs- és jelentés-szerkezete a magyar
    BDB-tábla (adat/forditasok.tsv, „teljes” sor) alapján. Jelölés: törzsenként a jelentés-jelek; „-” a sorszám nélküli fej (alakok), a
    zárójelben az alpontok. A H0834-nél az „1” kezdete pontatlan (l. naplok/OLVASOI_PILOT_szeletelo_atnezes.md, ismert hibák); a szám-sorrend helyes."""

    VART = {
        'H7121': [("Qal", "- 1(ab) 2(abcd) 3(abcd) 4(abc) 5(abcdef) 6(abcdefghi)"), ("Niph'al", "- 1 2(abcd)"), ("Pu'al", "-")],
        'H9003': [("", "-")],   # F99 seed-100 (DT-F99i): a fej nélküli betű-szócikk szakaszokra bomlik; a jelentések az I.–III. fő rész szakaszaiban
        'H0834': [("", "1 2 3 4(abcd) 5 6 7(abc) 8(abcdef)")],
        'H3588': [("", "1(abcdefg) 2(abc) 3(abcde)")],
        'H0935': [("Qal", "- 1(ab) 2(abcdefg) 3 4"), ("Hiph'il", "- 1(abcdefg) 2(abcde)"), ("Hoph'al", "-(abc)")],
        'H3027': [("", "1(ab) 2 3(abcde) 4(abcdefg) 5(abcdefghi)")],   # F99 M2: az aranyminta szerint (adat/bdb_aranyminta.tsv)
        'H5973': [("", "1(abcdefg) 2 3(abcde) 4(ab) 5")],   # F99 seed-100: a „מֵעִם_72” alcímszó a. – d. pontja külön szakasz
        'H2896': [("", "1(abcd) 2(abcde) 3(abcde) 4(ab) 5 6 7 8 9(ab) 10(ab)")],
        'H3205': [("Qal", "- 1(abc) 2(ab) 3"), ("Niph'al", "-"), ("Pi'el", "-"), ("Pu'al", "-"), ("Hiph'il", "- 1 2"), ("Hoph'al", "-"),
                  ("Hithpa'el", "-")],
        'H3772': [("Qal", "- 1(ab) 2 3 4"), ("Niph'al", "- 1(abc) 2 3 4"), ("Pu'al", "- 1 2"), ("Hiph'il", "- 1 2(abc) 3 4 5"), ("Hoph'al", "-")],
        'H3559': [("Niph'al", "- 1(abcd) 2 3 4"), ("Hiph'il", "- 1(abcd) 2(ab) 3 4"), ("Hoph'al", "- 1 2(ab) 3 4")],
        'H5800': [("Qal", "- 1(abcdefghijk) 2(abcdefg) 3"), ("Niph'al", "- 1 2"), ("Pu'al", "-")],
        'H0157': [("Qal", "- 1 2 3 4 5"), ("Niph'al", "-"), ("Pi'el", "- 1 2")],
        'H3201': [("Qal", "- 1(abcdefghi) 2(abc) 3")],
        'H7812': [("Qal", "-"), ("Hiph'il", "- 1(abc) 2(abcd) 3")],
        'H7931': [("Qal", "- 1(abc) 2(abcde)"), ("Pi'el", "- 1 2"), ("Hiph'il", "- 1(ab) 2")],
        'H3498': [("Qal", "-"), ("Niph'al", "-"), ("Hiph'il", "- 1(abc) 2 3")],
        'H3885': [("Qal", "- 1(abcd) 2"), ("Hiph'il", "-"), ("Hithpalpel", "-")],
        'H0560': [("", "1 2 3")],
        'H1869': [("Qal", "- 1 2 3 4"), ("Hiph'il", "- 1 2 3")],
        # az átnézés közben talált esetek
        'H4908': [("", "1 2(abc) 3(ab)")],      # főnév: az etimológiában álló „Pe`al imperfectum” nem törzsfejléc
        'H4191': [("Qal", "- 1(abcd) 2(abcd)"), ("Hiph'il", "- 1(ab) 2 3 4"), ("Hoph'al", "- 1 2 3 4")],   # „— megölni, halálra adni 1 abszolút”
        'H0622': [("Qal", "- 1 2 3 4"), ("Niph'al", "- 1 2 3"), ("Pi'el", "- 1 2 3"), ("Pu'al", "-"), ("Hithpa'el", "-")],   # „a Qal 2 passzívja”
    }
    SOROK = {}

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(GY, 'adat', 'forditasok.tsv'), encoding='utf-8') as fh:
            for s in fh:
                r = s.rstrip('\r\n').split('\t')
                if len(r) > 7 and r[0] == 'BDB' and r[3] == 'teljes' and r[6].strip():
                    cls.SOROK[r[1]] = r[6].replace('\\n', '\n')

    @staticmethod
    def alak(r):
        ki = []
        for t in r['torzsek']:
            ki.append((t['nev'], ' '.join((j['jel'] or '-') + ('(' + ''.join(a['jel'] for a in j['al']) + ')' if j['al'] else '')
                                          for j in t['jelentesek'])))
        return ki

    def test_varhato_szerkezet(self):
        import bdb_szelet
        for st, vart in self.VART.items():
            with self.subTest(strong=st):
                self.assertIn(st, self.SOROK)
                self.assertEqual(self.alak(bdb_szelet.szeletel(self.SOROK[st])), vart)

    def test_h7121_jelentesei_a_helyen(self):
        import bdb_szelet
        r = bdb_szelet.szeletel(self.SOROK['H7121'])
        qal = r['torzsek'][0]['jelentesek']
        self.assertTrue(qal[0]['szoveg'].startswith('perfectum'))       # az alaklista a fej, nem jelentés
        self.assertEqual([j['jel'] for j in r['torzsek'][1]['jelentesek']][1:], ['1', '2'])
        self.assertTrue(r['torzsek'][1]['jelentesek'][1]['szoveg'].startswith('visszaható'))

    def test_h0157_a_valodi_jelentesek(self):
        import bdb_szelet
        qal = bdb_szelet.szeletel(self.SOROK['H0157'])['torzsek'][0]['jelentesek']
        szovegek = {j['jel']: j['szoveg'] for j in qal}
        self.assertTrue(szovegek['1'].startswith('emberi szeretet'))
        self.assertTrue(szovegek['2'].startswith('ritkábban az étvágyról'))      # a jelölő előtt nincs írásjel („a participiumot 2 ritkábban”)
        self.assertTrue(szovegek['3'].startswith('szeretet Isten iránt'))

    def test_szemelyszam_nem_jelolo_de_a_pont_nelkuli_igen(self):
        import bdb_szelet
        m = bdb_szelet._szam_minta()
        self.assertIsNone(m.search("1. egyes szám אֵהָב 8:17"))
        self.assertIsNone(m.search("— 3. nőnemű egyes szám דָּֽרְכָה Józs 14:9"))
        self.assertIsNone(m.search("; 2. hímnemű többes szám suffixummal תְּאֵהֲבוּ"))
        self.assertIsNotNone(m.search("— 3 többes szám מִשְׁכָּנוֺת, lakóhelyek"))        # H4908: jelentés
        self.assertIsNotNone(m.search("— 1 egyes számú főnévvel, gyűjtőértelemben"))      # H3605: jelentés
        self.assertIsNone(m.search("; 1 Tsepreghi^Diss. Lugd. 171. o."))                  # H0834: bibliográfiai sorszám

    def test_laza_jelolo_csak_kisbetus_szo_utan(self):
        import bdb_szelet
        r = bdb_szelet._jelentesek("— 1 első jelentés Ézs 1:2. l. a participiumot 2 ritkábban az étvágyról, Qal 3 nem jelölő 3 harmadik", True)
        self.assertEqual([j['jel'] for j in r], ['1', '2', '3'])
        self.assertTrue(r[2]['szoveg'].startswith('harmadik'))
        r2 = bdb_szelet._jelentesek("— megölni, halálra adni 1 abszolút használatban 2 alanya Isten", True)
        self.assertEqual([j['jel'] for j in r2], ['', '1', '2'])
        r3 = bdb_szelet._jelentesek("alakok és még 1 szó után", False)      # nem igetörzs: az „1” laza jelölője kikapcsolva
        self.assertEqual([j['jel'] for j in r3], [''])

    def test_alakcsoport_fejlec_csak_igeben_es_nem_hivatkozasban(self):
        import bdb_szelet
        fo = bdb_szelet.szeletel("H1111. xx אב főnév: apa (arámi אב; — Pe`al imperfectum יִשְׁכְּנָן Dán 4:18 lakik) — 1 apa 2 ős")
        self.assertEqual([t['nev'] for t in fo['torzsek']], [''])
        ige = bdb_szelet.szeletel("H2222. yy אבד ige: elveszni — Qal perfectum אָבַד 1Móz 1:1; (olv. Qal imperfectum יֹאבַד Ézs 1:1); — 1 elvész 2 elpusztul")
        self.assertEqual([t['nev'] for t in ige['torzsek']], ['Qal'])


class TestRegresszioProto(unittest.TestCase):
    """K1 (M4: F60.46): az 1Móz 1:1–2:3 kimenet a prototípus (ce4ef98f, F60.0) kimenetével értékazonos: a prototípus
    minden kulcsának értéke megegyezik, a `ts=` időbélyeg kivételével és az alábbi, indokolt ENGEDELYEZETT listán kívül.
    A teszt maga állítja elő a prototípus-kimenetet: a ce4ef98f `adat.py`-ját ÉS `bdb_szelet.py`-ját (az egyetlen modul, amelyet
    a prototípus importál) együtt írja egy repón kívüli ideiglenes könyvtárba, és onnan futtatja (a prototípus saját szeletelőjével,
    nem a HEAD-ével); a repóba semmi nem kerül. Nem kihagyható.
    Az engedélyezett eltérés: (darabszám, indok). A darabszám pontos; adat- vagy szabályváltozásnál a lista
    szándékosan elromlik, és az új eltérést indokolni kell."""
    PROTO = 'ce4ef98f'
    ENGEDELYEZETT = {
        'morf_hu': (746, 'macula.morf_hu: a prototípusban üres volt, a v2 az adat/morf_kulcs_heber.tsv-ből feloldja (F60.5, gépi feldolgozás)'),
        'tbesg_teljes': (38, 'gor_lapok.*.tbesg: a prototípus 900 karakterre vágta „…”-tal; a v3.1 szabály szerint a teljes angol szöveg áll a lapon (F60.45)'),
        'thayer_teljes': (64, 'gor_lapok.*.thayer: a prototípus 700 karakterre vágta „…”-tal; a teljes angol szöveg áll a lapon (F60.45)'),
        'bdb_szeletelo': (52, 'lapok.*.appar (52 szó-lap, l. BDB_LAPOK): a BDB-szeletelő változásai a prototípus óta (F60.17, F60.18, F60.21, F60.23, F60.25, F60.35): jelentés-határok, a jelentés-sorszámok és a személyszám-jelölők kezelése, fejléc (héber szó, átírás), irodalom-/kritika-sorok; F99 M2 (a vak minta után, +11 lap): a vesszős/nagybetűs szó melletti „1” (H0226, H0402, H1419, H3220), a gyakoriság-zárójeles „1 (kb. 150-szer)” (H6086), a jelöletlen második címszó szakasza (H0259, H2896, H3220, H4325, H6754, H6996), a római számos fő tagolás (H2145); F99 seed-100 (+1 lap): az arámi שְׁמַיִן külön szakasz (H8064); a prototípus-kulcsok értéke ezeken a lapokon eltér'),
        'bdb_lemma_arg': (16, 'lapok.{H1254,H1288,H2416,H2896,H3220,H3651,H4325,H4723,H5414,H6213,H6754,H6960,H6996,H7235,H7287,H7363}.appar (a fenti 52-vel átfedve): a `szeletel(szoveg, lemma)` második argumentuma (F60.17, 8b642341) a homonima-szerepet jelöli (`azonos_lemma` / `masik_lemma` / `elo`); F99 M2: a jelöletlen második címszó (arámi rész: H1288, H5414; H2896, H3220, H6754, H6996) szerepe, és a H4325-ben a lemmával nem egyező, igehely nélküli utaló csonk helyett a fő szakasz; F99 seed-100: a H6213 II. עָשָׂה címszava (a fő tagolás külön szakasza mellett) homonima-szerepet kap; a teszt külön ellenőrzi, hogy a lemma-argumentum pontosan ennél a 16 lapnál módosítja a kimenetet'),
        'prov_elofordulas': (1, 'prov.elofordulas: a „(nem teljes)” megjegyzés kivéve (F60.29: a TAHOT fejezet-szinten teljes, F85)'),
    }
    BDB_LEMMA_LAPOK = {'H1254', 'H2416', 'H3651', 'H4723', 'H6960', 'H7235', 'H7287', 'H7363',
                       'H1288', 'H2896', 'H3220', 'H4325', 'H5414', 'H6754', 'H6996', 'H6213'}
    BDB_LAPOK = BDB_LEMMA_LAPOK | {'H0226', 'H0259', 'H0402', 'H1419', 'H2145', 'H6086', 'H8064'} | {
        'H0215', 'H0559', 'H0914', 'H1288', 'H1876', 'H1961', 'H2009', 'H2232', 'H2822', 'H2895', 'H3117', 'H3318', 'H3533',
        'H3605', 'H3615', 'H3915', 'H4390', 'H4725', 'H4910', 'H5414', 'H5774', 'H6213', 'H6440', 'H6509', 'H6635', 'H6942',
        'H7121', 'H7200', 'H7430', 'H7637', 'H8147', 'H8317'}

    @staticmethod
    def _ts(x):
        return re.sub(r'ts=[0-9T:\-Z]+', 'ts=X', x) if isinstance(x, str) else x

    def _proto_json(self):
        """A prototípus (ce4ef98f) adat.py + bdb_szelet.py a repón kívüli ideiglenes könyvtárból; a GY (a repó gyökere) a prototípus
        fájljában a valódi gyökérre van állítva, mert a prototípus a saját helyéből számolta."""
        with tempfile.TemporaryDirectory(prefix='olvaso_proto_') as t:
            for f in ('adat.py', 'bdb_szelet.py'):
                r = subprocess.run(['git', '-C', GY, 'show', '%s:eszkozok/olvaso_pilot/%s' % (self.PROTO, f)], capture_output=True)
                self.assertEqual(r.returncode, 0, 'a prototípus (%s) nem érhető el a git-történetben (a teszt nem hagyható ki)' % self.PROTO)
                with open(os.path.join(t, f), 'wb') as fh:
                    fh.write(r.stdout)
            ut = os.path.join(t, 'adat.py')
            with open(ut, encoding='utf-8') as fh:
                src = fh.read()
            gy_sor = "GY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\\\', '/') + '/'"
            self.assertEqual(src.count(gy_sor), 1)
            with open(ut, 'w', encoding='utf-8') as fh:
                fh.write(src.replace(gy_sor, 'GY = %r' % GY))
            ki = os.path.join(t, 'ki')
            p = subprocess.run([sys.executable, ut, '--kimenet', ki], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(p.returncode, 0, p.stderr[-800:])
            with open(os.path.join(ki, 'olvaso_pilot.json'), encoding='utf-8') as fh:
                return json.load(fh)

    @staticmethod
    def _resz(x, y):
        """x minden kulcsa y-ban azonos értékű (y-nak lehetnek új kulcsai)."""
        if isinstance(x, dict):
            return isinstance(y, dict) and all(k in y and TestRegresszioProto._resz(v, y[k]) for k, v in x.items())
        if isinstance(x, list):
            return isinstance(y, list) and len(x) == len(y) and all(TestRegresszioProto._resz(a, b) for a, b in zip(x, y))
        return x == y

    def test_ertekazonos_a_prototipussal(self):
        p = self._proto_json()
        g = ADAT['gen']
        szamlalo = {k: 0 for k in self.ENGEDELYEZETT}
        eltero_bdb = set()
        elteres = []

        def hasonlit(x, y, ut):
            m = re.match(r'^/lapok/(H\d{4})/appar$', ut)
            if m:
                if not self._resz(x, y):
                    szamlalo['bdb_szeletelo'] += 1
                    eltero_bdb.add(m.group(1))
                return
            if isinstance(x, dict):
                if not isinstance(y, dict):
                    elteres.append(ut + ' típus')
                    return
                for k, v in x.items():
                    if k not in y:
                        elteres.append('%s/%s hiányzik' % (ut, k))
                    else:
                        hasonlit(v, y[k], '%s/%s' % (ut, k))
            elif isinstance(x, list):
                if not isinstance(y, list) or len(x) != len(y):
                    elteres.append(ut + ' hossz')
                    return
                for i, (a, b) in enumerate(zip(x, y)):
                    hasonlit(a, b, '%s[%d]' % (ut, i))
            else:
                a, b = self._ts(x), self._ts(y)
                if a == b:
                    return
                if re.match(r'^/versek\[\d+\]/heber\[\d+\]/macula/morf_hu$', ut) and a == '':
                    szamlalo['morf_hu'] += 1
                elif re.match(r'^/gor_lapok/G\d{4}/tbesg$', ut) and a.endswith('…') and b.startswith(a[:-1]) and len(b) > len(a) - 1:
                    szamlalo['tbesg_teljes'] += 1
                elif re.match(r'^/gor_lapok/G\d{4}/thayer$', ut) and a.endswith('…') and b.startswith(a[:-1]) and len(b) > len(a) - 1:
                    szamlalo['thayer_teljes'] += 1
                elif ut == '/prov/elofordulas' and a.replace(' (nem teljes)', '') == b:
                    szamlalo['prov_elofordulas'] += 1
                else:
                    elteres.append('%s: %r != %r' % (ut, str(a)[:60], str(b)[:60]))

        hasonlit(p, g, '')
        self.assertEqual(elteres[:10], [])
        # a lemma-argumentum tétele külön teszt (átfedő számláló): itt a 40 szeletelő-lap a pontos lista
        szamlalo['bdb_lemma_arg'] = len(self.BDB_LEMMA_LAPOK)
        self.assertEqual(eltero_bdb, self.BDB_LAPOK)
        self.assertEqual(szamlalo, {k: v[0] for k, v in self.ENGEDELYEZETT.items()})

    def test_lemma_argumentum_pontosan_8_lapot_modosit(self):
        """A `szeletel(szoveg, lemma)` második argumentuma (F60.17) csak a BDB_LEMMA_LAPOK lapjainál módosítja a kimenetet."""
        import bdb_szelet
        eltero = set()
        for s, l in ADAT['gen']['lapok'].items():
            txt = l['bdb_hu'] or l['bdb_en']
            if bdb_szelet.szeletel(txt, None) != bdb_szelet.szeletel(txt, l['lemma']):
                eltero.add(s)
        self.assertEqual(eltero, self.BDB_LEMMA_LAPOK)

    def test_a_prototipus_kimenete_98_lap(self):
        self.assertEqual(len(self._proto_json()['lapok']), 98)


class TestTeljes1Moz1_25(unittest.TestCase):
    """K1: az 1Móz 1–25 szakasz 693 verset ad, az adat.py hibátlanul lefut (~30 s), a kimenet első versei és a közös
    szó-lapok azonosak az 1Móz 1:1–2:3 futáséval."""
    @classmethod
    def setUpClass(cls):
        cls.d = futtat('1Móz 1-25', os.path.join(TMP, 'gen25'))

    def test_693_vers(self):
        self.assertEqual(len(self.d['versek']), 693)
        self.assertEqual((self.d['versek'][0]['igehely'], self.d['versek'][-1]['igehely']), ('1Móz 1:1', '1Móz 25:34'))

    def test_elso_versek_egyeznek_az_1_1_2_3_futassal(self):
        a = ADAT['gen']
        self.assertEqual(self.d['versek'][:len(a['versek'])], a['versek'])
        for s, l in a['lapok'].items():
            self.assertEqual(self.d['lapok'][s], l, s)

    def test_nincs_ures_vers(self):
        self.assertTrue(all(v['karoli'] and v['heber'] for v in self.d['versek']))


class TestTeljesAngolSzoveg(unittest.TestCase):
    """F60.45 (v3.1): a TBESG- és a Thayer-szöveg vágás nélkül áll a lapon, gördíthető blokkban."""
    def test_nincs_vagas(self):
        g = ADAT['gen']['gor_lapok']
        self.assertGreater(max(len(x['tbesg']) for x in g.values()), 900)
        self.assertGreater(max(len(x['thayer']) for x in g.values()), 700)
        self.assertFalse([k for k, x in g.items() if x['tbesg'].endswith('…') or x['thayer'].endswith('…')])

    def test_gordulo_blokk_a_sablonban(self):
        h = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
        self.assertIn('.bdb.hosszu { max-height', h)
        self.assertIn("class: 'bdb en hosszu', lang: 'en', text: l.tbesg", h)
        self.assertIn("class: 'bdb en hosszu', lang: 'en', text: l.thayer", h)

    def test_tbesh_licenc_adatbol(self):
        """A TBESH licencsora nem rögzített szöveg: a licenc a `D.licenc` / `licenc_jelzes` adatból jön."""
        h = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
        self.assertNotIn('licenc-kérdés nyitott', h)
        self.assertIn('TBESH', ADAT['gen']['licenc'])
        self.assertEqual(ADAT['gen']['licenc_jelzes']['TBESH']['allapot'], 'tisztazott')


class TestKiadas(unittest.TestCase):
    """DT-F60a (a 2. előkészítése): az adat.py --kiadas {belso,nyilvanos,kereskedelmi}; alapérték: belso."""
    @classmethod
    def setUpClass(cls):
        cls.k = {}
        for kiadas in ('belso', 'nyilvanos', 'kereskedelmi'):
            ki = os.path.join(TMP, 'kiadas_' + kiadas)
            p = subprocess.run([sys.executable, os.path.join(D, 'adat.py'), '--szakasz', 'Zsolt 22', '--kimenet', ki, '--kiadas', kiadas],
                               capture_output=True, text=True, encoding='utf-8')
            if p.returncode:
                raise RuntimeError('adat.py --kiadas %s: %s' % (kiadas, p.stderr[-800:]))
            with open(os.path.join(ki, 'olvaso_pilot.json'), encoding='utf-8') as fh:
                cls.k[kiadas] = json.load(fh)

    @staticmethod
    def _kjv_van(d):
        return all(v['angol']['kjv'] and v['angol']['kjv']['szavak'] for v in d['versek'][2:])

    @staticmethod
    def _mcged_db(d):
        return sum(1 for g in d['gor_lapok'].values() if g.get('mcged'))

    def test_belso_minden_blokk(self):
        d = self.k['belso']
        self.assertEqual(d['kiadas'], 'belso')
        self.assertTrue(self._kjv_van(d))
        self.assertGreater(self._mcged_db(d), 0)
        self.assertIn('kjv', d['prov'])
        self.assertIn('mcged', d['prov'])

    def test_alap_a_belso(self):
        """Paraméter nélkül futtatva (ADAT['zsolt']) a kimenet azonos a --kiadas belso kimenettel (a ts kivételével)."""
        def maszk(d):
            return re.sub(r'ts=[0-9T:\-Z]+', 'ts=X', json.dumps(d, ensure_ascii=False, sort_keys=True))
        self.assertEqual(maszk(ADAT['zsolt']), maszk(self.k['belso']))

    def test_nyilvanos_nincs_kjv_strong(self):
        d = self.k['nyilvanos']
        self.assertEqual(d['kiadas'], 'nyilvanos')
        self.assertTrue(all(v['angol']['kjv'] is None for v in d['versek']))
        self.assertTrue(all(v['angol']['bsb'] for v in d['versek']))
        self.assertNotIn('kjv', d['prov'])
        self.assertEqual(d['stat']['kjv_vers'], 0)
        self.assertEqual(self._mcged_db(d), self._mcged_db(self.k['belso']))
        self.assertIn('mcged', d['prov'])

    def test_kereskedelmi_nincs_kjv_es_mcged(self):
        d = self.k['kereskedelmi']
        self.assertEqual(d['kiadas'], 'kereskedelmi')
        self.assertTrue(all(v['angol']['kjv'] is None for v in d['versek']))
        self.assertEqual(self._mcged_db(d), 0)
        self.assertNotIn('kjv', d['prov'])
        self.assertNotIn('mcged', d['prov'])
        self.assertEqual(d['stat']['mcged'], 0)

    def test_a_tobbi_adat_valtozatlan(self):
        """A kiadás-szűrő csak a két blokkot veszi ki: a héber, görög, vers-adat többi része azonos a belső kiadáséval."""
        b = self.k['belso']
        for kiadas in ('nyilvanos', 'kereskedelmi'):
            d = self.k[kiadas]
            for vb, vd in zip(b['versek'], d['versek']):
                self.assertEqual({k: v for k, v in vb.items() if k != 'angol'}, {k: v for k, v in vd.items() if k != 'angol'})
                self.assertEqual(vb['angol']['bsb'], vd['angol']['bsb'])
            self.assertEqual(b['lapok'], d['lapok'])
            for s, g in b['gor_lapok'].items():
                self.assertEqual({k: v for k, v in g.items() if k != 'mcged'}, {k: v for k, v in d['gor_lapok'][s].items() if k != 'mcged'})

    def test_ervenytelen_ertek_hiba(self):
        p = subprocess.run([sys.executable, os.path.join(D, 'adat.py'), '--szakasz', 'Zsolt 22', '--kiadas', 'xx',
                            '--kimenet', os.path.join(TMP, 'kiadas_xx')], capture_output=True, text=True, encoding='utf-8')
        self.assertNotEqual(p.returncode, 0)

    def test_sablon_kezeli_a_hianyzo_blokkot(self):
        h = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
        self.assertIn("a.kjv ? angolBlokk('Angol szó szavanként (KJV)'", h)
        self.assertIn("D.kiadas === 'kereskedelmi' ? null : mcgedBlokk(l)", h)


class TestDbMeres(unittest.TestCase):
    """M2b / K5: a db_meres.py egy vers-lap és szó-lapok D2-egyezése a pardes.db-vel (ha van); nincs adatbázis -> „nem mérhető”."""
    @classmethod
    def setUpClass(cls):
        import db_meres
        cls.dm = db_meres
        cls.db = db_meres.alap_db()

    def test_nincs_adatbazis_nem_merheto(self):
        ki = os.path.join(TMP, 'nincs_db')
        p = subprocess.run([sys.executable, os.path.join(D, 'db_meres.py'), '--db', os.path.join(TMP, 'nincs.db'), '--kimenet', ki],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(p.returncode, 0, p.stderr[-500:])
        self.assertIn('NEM MÉRHETŐ', p.stdout)
        with open(os.path.join(ki, 'olvaso_pilot_db_meres.json'), encoding='utf-8') as fh:
            self.assertEqual(json.load(fh)['allapot'], 'nem mérhető')

    def test_d2_vers_lap_egyezes(self):
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            v = ADAT['gen']['versek'][0]
            ki = self.dm.hasonlit_vers(con, v)
            for blokk in ('karoli_szoveg', 'karoli_strong_parositas', 'heber_szavak', 'versszamozas', 'tsk_darab'):
                self.assertTrue(ki[blokk][0], '%s: tsv=%r db=%r' % (blokk, ki[blokk][1], ki[blokk][2]))
        finally:
            con.close()

    def test_d2_szo_lap_egyezes(self):
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            for s in ('H7225', 'H0430'):
                ki = self.dm.hasonlit_szo(con, ADAT['gen']['lapok'][s])
                for blokk in ('strong_szotar', 'bdb_angol', 'bdb_magyar', 'lxx_bridge'):
                    self.assertTrue(ki[blokk][0], '%s %s: tsv=%r db=%r' % (s, blokk, ki[blokk][1], ki[blokk][2]))
        finally:
            con.close()

    def test_d2_elteres_kimutatasa(self):
        """A hasonlító valóban eltérést jelez, ha az adat eltér (nem mindig „egyezik”)."""
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            v = json.loads(json.dumps(ADAT['gen']['versek'][0]))
            v['karoli'] += ' x'
            self.assertFalse(self.dm.hasonlit_vers(con, v)['karoli_szoveg'][0])
        finally:
            con.close()

    # -- F92 (DT-F92a): az új táblák olvasási útja ------------------------------------------
    def _uj_tablak_vannak(self, con):
        return all(self.dm._van_tabla(con, t) for t in ('token_macula', 'lxx_token', 'lxx_versszam', 'bdb_alias', 'nave_vers'))

    def test_d2_uj_blokkok_zsolt22_es_1moz(self):
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            if not self._uj_tablak_vannak(con):
                self.skipTest('a pardes.db még nem hordozza az F92 tábláit (újraépítés kell)')
            for kulcs, ig in (('zsolt', 'Zsolt 22:3'), ('zsolt', 'Zsolt 22:1'), ('gen', '1Móz 1:1'), ('gen', '1Móz 1:4')):
                ki = self.dm.hasonlit_vers(con, vers(ADAT[kulcs], ig))
                for blokk in ('macula', 'lxx_szavak', 'nave', 'lxx_vers_szam'):
                    self.assertIn(blokk, ki)
                    self.assertTrue(ki[blokk][0], '%s %s: tsv=%r db=%r' % (ig, blokk, ki[blokk][1], ki[blokk][2]))
        finally:
            con.close()

    def test_d2_bdb_alias_szo_lap(self):
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            if not self._uj_tablak_vannak(con):
                self.skipTest('a pardes.db még nem hordozza az F92 tábláit (újraépítés kell)')
            for s in ('H0136', 'H7358'):
                ki = self.dm.hasonlit_szo(con, ADAT['zsolt']['lapok'][s])
                for blokk in ('bdb_angol', 'bdb_magyar', 'bdb_alias'):
                    self.assertTrue(ki[blokk][0], '%s %s: tsv=%r db=%r' % (s, blokk, ki[blokk][1], ki[blokk][2]))
                self.assertIsNotNone(ki['bdb_alias'][2])
        finally:
            con.close()

    def test_d2_uj_blokk_elteres_kimutatasa(self):
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            if not self._uj_tablak_vannak(con):
                self.skipTest('a pardes.db még nem hordozza az F92 tábláit (újraépítés kell)')
            v = json.loads(json.dumps(vers(ADAT['zsolt'], 'Zsolt 22:3')))
            v['lxx'][0]['szoalak'] += 'x'
            v['nave'] = v['nave'][1:]
            ki = self.dm.hasonlit_vers(con, v)
            self.assertFalse(ki['lxx_szavak'][0])
            self.assertFalse(ki['nave'][0])
        finally:
            con.close()

    def test_lxx_parhuzamos_szovegformak_nem_fesulnek_ossze(self):
        """Ellenőr ÚJ-1: ahol egy Károli-versre két LXX-szövegforma esik (Dán, Bír, Józs), az olvasási út formánként csoportosít."""
        if not os.path.exists(self.db):
            self.skipTest('nincs pardes.db')
        con = self.dm.kapcsolat(self.db)
        try:
            if not self._uj_tablak_vannak(con) or not self.dm._van_oszlop(con, 'lxx_token', 'szovegforma'):
                self.skipTest('a pardes.db még nem hordozza a szovegforma oszlopot (újraépítés kell)')
            for elo in ('Dán', 'Bír', 'Józs'):
                sor = con.execute("SELECT karoli_igehely FROM lxx_token WHERE karoli_igehely LIKE ? "
                                  "GROUP BY karoli_igehely HAVING COUNT(DISTINCT szovegforma)>1 LIMIT 1", (elo + ' %',)).fetchone()
                self.assertIsNotNone(sor, elo)
                d = self.dm.db_vers(con, sor[0])
                self.assertGreaterEqual(len(d['lxx_formak']), 2, sor[0])
                darab = {f: con.execute('SELECT COUNT(*) FROM lxx_token WHERE karoli_igehely=? AND szovegforma=?',
                                        (sor[0], f)).fetchone()[0] for f in d['lxx_formak']}
                self.assertEqual(len(d['lxx_szavak']), sum(darab.values()))
                sorrend = [r[0] for r in con.execute(
                    'SELECT szovegforma FROM lxx_token WHERE karoli_igehely=? ORDER BY szovegforma, pozicio, rowid', (sor[0],))]
                self.assertEqual(sorrend, sorted(sorrend))   # formánként összefüggő blokkok
                formak_lxx = [r[0] for r in con.execute(
                    "SELECT DISTINCT szovegforma FROM lxx_versszam WHERE karoli_igehely=? AND forras='LXX_OS'", (sor[0],))]
                self.assertGreaterEqual(len(formak_lxx), 2, sor[0])
        finally:
            con.close()

    def test_macula_kot_ketertelmu_pozicio_sorrend(self):
        mac = [{'strong': 'H0430'}, {'strong': 'H0430'}, {'strong': None}]
        # eltérő szegmentálás (3 Macula-sor, 2 TAHOT-token): a kétszer álló Strong kétértelmű, az első használatlan dönt
        kot, ketert = self.dm.macula_kot(['H0430', 'H0430'], mac, 2)
        self.assertEqual(kot, [mac[0], mac[1]])
        self.assertEqual(ketert, 1)           # csak az első kötésnél volt egynél több jelölt
        # azonos szegmentálás: sorrend szerinti kötés, nincs kétértelműség
        kot, ketert = self.dm.macula_kot(['H0430', 'H0430', 'H9020'], mac, 3)
        self.assertEqual((kot, ketert), (mac, 0))


class TestEpitHatokor(unittest.TestCase):
    def test_fejezet_tartomany(self):
        self.assertEqual(sz.szakasz_cim('1Móz 1-25'), '1Móz 1–25')
        self.assertEqual(sz.szakasz_azonosito('1Móz 1-25'), '1Moz_1-25')
        v = sz.szakasz_versei('1Móz 1-25')
        self.assertEqual((v[0], v[-1], len(v)), ('1Móz 1:1', '1Móz 25:34', 693))
        self.assertEqual(sz.szakasz_versei('1Móz 1:1-25:34'), v)

    def test_gzip_beagyazas_visszafejtheto(self):
        import base64
        import gzip
        ki = os.path.join(TMP, 'epit_gen')
        os.makedirs(ki, exist_ok=True)
        with open(os.path.join(ki, 'olvaso_pilot.json'), 'w', encoding='utf-8') as fh:
            json.dump(ADAT['gen'], fh, ensure_ascii=False)
        p = subprocess.run([sys.executable, os.path.join(D, 'epit.py'), '--szakasz', '1Móz 1:1-2:3', '--kimenet', ki],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(p.returncode, 0, p.stderr[-500:])
        with open(os.path.join(ki, 'karoli_konkordancia_proba.html'), encoding='utf-8') as fh:
            h = fh.read()
        m = re.search(r'<script type="application/json" id="adat" data-kodolas="gzip-base64">([^<]+)</script>', h)
        self.assertIsNotNone(m)
        self.assertEqual(json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode('utf-8')), ADAT['gen'])
        self.assertNotIn('__ADAT', h)
        self.assertNotIn(chr(0xFFFD), h)


if __name__ == '__main__':
    unittest.main(verbosity=2)
