"""Olvasói pilot: tesztek (F60.1, M1).

Futtatás: python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py
Az adat.py-t ideiglenes könyvtárba futtatja mindkét szakaszra (a kimenet nem kerül a repóba), és
ellenőrzi: a szakasz-feloldást, a fő szó választását, a görög szóalak párosítását, a BDB-bontást,
a proveniencia-sorokat, a „csak adat” ellenőrzőlistát (minden blokk-cím kap jelleg-címkét és
adatforrást; nincs feladatszám az oldalon).
Regressziós alap: ha az OLVASO_PROTOTIP_JSON környezeti változó egy korábbi (F60.4, a bővítés előtti)
olvaso_pilot.json útvonala, az 1Móz 1:1–2:3 kimenete ahhoz képest csak új mezőkkel térhet el (a macula.morf_hu
maszkolva: a feloldás üres volt). Előállítás: git worktree add <könyvtár> 98b5098, ott adat.py --szakasz ... --kimenet ...
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

    def test_felirat_nincs_lxx(self):
        # a 22:1 a felirat (Károli = MT-számozás); az LXX_OS ehhez a versszámhoz nem ad szót
        self.assertEqual(len(vers(ADAT['zsolt'], 'Zsolt 22:1')['lxx']), 0)
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


class Regresszio(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('OLVASO_PROTOTIP_JSON'), 'OLVASO_PROTOTIP_JSON nincs megadva')
    def test_prototipussal_azonos(self):
        """Az 1Móz 1:1–2:3 JSON a korábbi (F60.4) kimenethez képest csak az új mezőkkel térhet el.
        Maszkolt (szándékosan megváltozott) érték: macula.morf_hu (a feloldás üres volt)."""
        MASZK = {'morf_hu'}
        a = json.load(open(os.environ['OLVASO_PROTOTIP_JSON'], encoding='utf-8'))
        b = json.load(open(os.path.join(TMP, 'gen', 'olvaso_pilot.json'), encoding='utf-8'))

        def reszhalmaz(x, y, ut):
            if isinstance(x, dict):
                self.assertIsInstance(y, dict, ut)
                for k, v in x.items():
                    self.assertIn(k, y, ut + '/' + k)
                    if k not in MASZK:
                        reszhalmaz(v, y[k], ut + '/' + k)
            elif isinstance(x, list):
                self.assertEqual(len(x), len(y), ut)
                for i, (p, q) in enumerate(zip(x, y)):
                    reszhalmaz(p, q, '%s[%d]' % (ut, i))
            else:
                if isinstance(x, str):     # a ts= mező a futás ideje: maszkolva
                    x, y = re.sub(r'ts=[0-9T:\-Z]+', 'ts=X', x), re.sub(r'ts=[0-9T:\-Z]+', 'ts=X', y)
                self.assertEqual(x, y, ut)
        reszhalmaz(a, b, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
