"""Olvasói pilot: tesztek (F60.1, M1).

Futtatás: python eszkozok/olvaso_pilot/teszt_olvaso_pilot.py
Az adat.py-t ideiglenes könyvtárba futtatja mindkét szakaszra (a kimenet nem kerül a repóba), és
ellenőrzi: a szakasz-feloldást, a fő szó választását, a görög szóalak párosítását, a BDB-bontást,
a proveniencia-sorokat, a „csak adat” ellenőrzőlistát (minden blokk-cím kap jelleg-címkét és
adatforrást; nincs feladatszám az oldalon).
Regressziós azonosság: ha az OLVASO_PROTOTIP_JSON környezeti változó egy korábbi olvaso_pilot.json
útvonala, az 1Móz 1:1–2:3 kimenete ahhoz képest bájtra azonos (a ts= mező kivételével)."""
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


class Regresszio(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('OLVASO_PROTOTIP_JSON'), 'OLVASO_PROTOTIP_JSON nincs megadva')
    def test_prototipussal_azonos(self):
        def tisztit(t):
            # a prototípus óta bővült mező (F60.2): kjv_lxx
            return re.sub(r', "kjv_lxx": "[^"]*"', '', re.sub(r'ts=[0-9T:\-Z]+', 'ts=X', t))
        a = tisztit(open(os.environ['OLVASO_PROTOTIP_JSON'], encoding='utf-8').read())
        b = tisztit(open(os.path.join(TMP, 'gen', 'olvaso_pilot.json'), encoding='utf-8').read())
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main(verbosity=2)
