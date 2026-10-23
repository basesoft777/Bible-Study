"""A tervező mód tesztjei (#98 M2): unittest.

Futtatás (Python 3.12 alatt, a `pardes` WSL-disztribúció venv-jével):
    PARDES_DB=/home/basesoft/pardes/pardes.db python eszkozok/olvaso_szerver/teszt_tervezo.py
A regiszter, a regiszter-őr, a szabálytérkép és az értékszűrés tesztjei adatbázis és Flask nélkül is futnak; a végpontot és a
lapokat kérő tesztek pardes.db és Flask nélkül kimaradnak (kifejezetten jelölve, nem zöldként).

A tesztek a repóba nem írnak: a mentési végpont tesztjei a konfiguráció ideiglenes másolatán dolgoznak.
"""
import copy
import difflib
import json
import os
import re
import shutil
import sys
import tempfile
import tomllib
import unittest
from html.parser import HTMLParser
from unittest import mock

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D)).replace('\\', '/') + '/'
sys.path.insert(0, D)

import arculat
import regiszter_or
import tervezo

try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

DB = os.environ.get('PARDES_DB') or (GY + 'pardes.db')
VAN_DB = os.path.exists(DB)
KONFIG = os.path.join(D, 'konfig')


def toml_adat():
    with open(tervezo.ELEMEK_UT, 'rb') as f:
        return tomllib.load(f)


def alap_arculat():
    return arculat.Arculat.betolt()


# =====================================================================================================================
# a regiszter
# =====================================================================================================================
class TestRegiszter(unittest.TestCase):
    """Az elem-regiszter (`konfig/elemek.toml`) a jóváhagyott M0 1.1 szerint (83 sor) és a #134 M3 komponensstílusai (19 elem:
    a navigáció és a műfajszínek; a javítókörben a tájoló pirula kikerült, DT-F134n: 18 maradt), minden token létező és állítható."""

    @classmethod
    def setUpClass(cls):
        cls.a = alap_arculat()
        cls.r = tervezo.Regiszter.betolt(cls.a.adat)

    def test_101_elem_egyedi_id(self):
        self.assertEqual(len(self.r.elemek), 83 + 18)
        self.assertEqual(len({e['id'] for e in self.r.elemek}), 83 + 18)
        self.assertNotIn('tajolo', {e['id'] for e in self.r.elemek})

    def test_a_mufajszinek_irhatok(self):
        """#134 M3 (DT296): a nyolc műfajszín (--g-*) és az árnyék színe regisztrált token, tehát a tervező módban írható."""
        tok = self.r.tokenek()
        for g in ('g-tor', 'g-tort', 'g-bolcs', 'g-prof', 'g-kis', 'g-ev', 'g-lev', 'g-apok', 'arnyek'):
            self.assertIn(g, tok)

    def test_a_jovahagyott_nevek_mintai(self):
        nev = {e['id']: (e['nev'], e['szelektor']) for e in self.r.elemek}
        self.assertEqual(nev['he-szo'], ('Héber szócsempe', '.he-szo'))
        self.assertEqual(nev['versszam'], ('Versszám', '.versszam'))
        self.assertEqual(nev['jelleg-modell'], ('Jelleg-címke: modell-kimenet', '.jelleg-modell'))
        self.assertEqual(nev['jelentes-jelolo'], ('Jelentés-jelölő a részletes listában (1, 2 … / a., b. …)', 'ol.jel > li, ol.al > li'))
        self.assertEqual(nev['jel-vazlat'][0], 'Jelentésszerkezet vázlata (a BDB-blokk elején)')
        self.assertEqual(nev['tema-aktiv'][1], '.tema button[aria-pressed="true"]')

    def test_minden_token_letezik_es_nem_betucsalad(self):
        for e in self.r.elemek:
            for t in e['tulajdonsag']:
                self.assertTrue(tervezo.token_letezik(t['token'], self.a.adat), t['token'])
                self.assertIn(tervezo.token_csoport(t['token'])[0], tervezo.IRHATO_CSOPORT, t['token'])

    def test_az_irhato_tokenek(self):
        tok = self.r.tokenek()
        self.assertIn('bg', tok)
        self.assertIn('space-he-csempe-min', tok)
        self.assertIn('fs-jelentes-jel', tok)
        # az M1.7 hét regiszteren kívüli tokenje (a tartalékon át csak előnézet)
        for t in ('fs-alcim', 'fs-kiscim', 'fs-csempe-megj', 'fs-il-eredeti-sor', 'lh-jelleg', 'lh-lxx-csempe', 'space-oszlopkoz'):
            self.assertNotIn(t, tok)
        self.assertFalse(any(t.startswith('font-') for t in tok))

    def test_rossz_regiszter_indulasi_hiba(self):
        def hibas(modosit, minta):
            adat = copy.deepcopy(toml_adat())
            modosit(adat)
            with self.assertRaises(tervezo.TervezoHiba) as e:
                tervezo.Regiszter('<teszt>', adat, self.a.adat)
            self.assertIn(minta, str(e.exception))
        hibas(lambda a: a['elem'][0]['tulajdonsag'].append({'nev': 'X', 'token': 'fs-nincs-ilyen'}), 'fs-nincs-ilyen')
        hibas(lambda a: a['elem'][0]['tulajdonsag'].append({'nev': 'X', 'token': 'font-ui'}), 'betűcsalád')
        hibas(lambda a: a['elem'][1].update(id=a['elem'][0]['id']), 'ismétlődő')
        hibas(lambda a: a['elem'][0].update(nev=''), 'nev')
        hibas(lambda a: a['kizart'].update(lista=''), 'indok')
        hibas(lambda a: a['elem'][0].update(extra=1), 'kulcsok')

    def test_szelektor_reszek_es_specifitas(self):
        self.assertEqual(tervezo.szelektor_reszek('.megj, .szam, .cimke:not(.cimkek .cimke)'), ['.megj', '.szam', '.cimke:not(.cimkek .cimke)'])
        self.assertEqual(tervezo.szelektor_reszek('.tema button[aria-pressed="true"]'), ['.tema button[aria-pressed="true"]'])
        self.assertGreater(tervezo.specifitas('.nezetvalto a.aktiv'), tervezo.specifitas('.nezetvalto a'))
        self.assertGreater(tervezo.specifitas('.versszam'), tervezo.specifitas('a'))
        self.assertEqual(tervezo.szelektor_osztalyok('.tema button[aria-pressed="true"]'), {'tema'})


# =====================================================================================================================
# a regiszter-őr
# =====================================================================================================================
class TestRegiszterOr(unittest.TestCase):
    """A felület minden CSS-osztálya a regiszterben vagy a kizárt listán áll; az ismeretlen osztály hibát ad."""

    @classmethod
    def setUpClass(cls):
        cls.biz = regiszter_or.bizonyossag_ertekek(DB) if VAN_DB else None
        cls.elof = regiszter_or.felmeres(biz=cls.biz)
        cls.reg, cls.kizart = regiszter_or.regiszter_adat()

    def test_a_mai_feluleten_nincs_ismeretlen_osztaly(self):
        self.assertEqual(regiszter_or.ellenoriz(self.elof, self.reg, self.kizart), [])

    def test_a_kizart_lista_indokolt_es_nem_elavult(self):
        latott = {e.osztaly for e in self.elof}
        for o, indok in self.kizart.items():
            self.assertTrue(indok.strip(), o)
            self.assertIn(o, latott, 'elavult kizárt osztály: %s' % o)
            self.assertNotIn(o, self.reg, 'a kizárt osztály a regiszterben is áll: %s' % o)
        self.assertNotIn('jt', self.kizart)                    # az F98.11 óta nem létező osztály (a felhasználó kérése)

    def test_a_dinamikus_osztalyok_kibontva(self):
        latott = {e.osztaly for e in self.elof if e.dinamikus}
        for o in ('par-magas', 'par-alacsony', 'jelleg-forras', 'jelleg-gepi',
                  'jelleg-modell', 'st-link', 'strong', 'nyelvtani', 'folyamat', 'arany', 'aktiv', 'gor', 'heb'):
            self.assertIn(o, latott, o)
        self.assertIn('kijelolt', {e.osztaly for e in self.elof})               # a {% if %} … {% endif %} közti szöveg
        # #134: a nézetek helyett rétegek; a `nezet-` dinamikus előtag megszűnt (a body horga literál: reteg-il / reteg-nincs)
        self.assertFalse(hasattr(regiszter_or, 'NEZETEK'))
        self.assertTrue({'reteg-il', 'reteg-nincs', 'lap-nyitva'} <= {e.osztaly for e in self.elof})

    @unittest.skipUnless(VAN_DB, 'nincs pardes.db: a par- értékkészlet a tartalék listából')
    def test_a_bizonyossag_az_adatbazisbol(self):
        self.assertEqual(set(self.biz), set(regiszter_or.BIZONYOSSAG_TARTALEK))

    def test_proba_osztaly_a_sablonban_hibat_ad(self):
        with tempfile.TemporaryDirectory() as tmp:
            sd = os.path.join(tmp, 'sablonok')
            shutil.copytree(regiszter_or.SABLON_DIR, sd)
            with open(os.path.join(sd, 'alap.html'), encoding='utf-8') as f:
                t = f.read()
            t = t.replace('<main class="tartalom">', '<main class="tartalom proba-uj-osztaly">')
            with open(os.path.join(sd, 'alap.html'), 'w', encoding='utf-8') as f:
                f.write(t)
            hibak = regiszter_or.ellenoriz(regiszter_or.felmeres(sablon_dir=sd, biz=self.biz), self.reg, self.kizart)
        self.assertEqual(len(hibak), 1, hibak)
        self.assertRegex(hibak[0], r'^ismeretlen CSS-osztály: proba-uj-osztaly \(sablonok/alap\.html:\d+\)')

    def test_proba_osztaly_a_blokkokban_hibat_ad(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(D, 'blokkok.py'), encoding='utf-8') as f:
                src = f.read()
            src += "\n\ndef _proba(x):\n    return Markup('<span class=\"proba-blokk %s\">x</span>') % ('' if x else ' proba-allapot')\n"
            ut = os.path.join(tmp, 'blokkok.py')
            with open(ut, 'w', encoding='utf-8') as f:
                f.write(src)
            hibak = regiszter_or.ellenoriz(regiszter_or.felmeres(py_fajlok=(ut, os.path.join(D, 'oldalak.py')), biz=self.biz), self.reg, self.kizart)
        self.assertEqual(sorted(re.sub(r' \(.*', '', h) for h in hibak),
                         ['ismeretlen CSS-osztály: proba-allapot', 'ismeretlen CSS-osztály: proba-blokk'])

    def test_kibonthatatlan_kifejezes_hiba(self):
        with self.assertRaises(regiszter_or.Kibonthatatlan):
            regiszter_or.sablon_ertek('a {{ valami }}', {'nezet-': ['x']}, 'x.html', 1)
        with tempfile.TemporaryDirectory() as tmp:
            ut = os.path.join(tmp, 'm.py')
            with open(ut, 'w', encoding='utf-8') as f:
                f.write("def f(x):\n    return '<b class=\"%s\">' % x.nev\n")
            with self.assertRaises(regiszter_or.Kibonthatatlan):
                regiszter_or.py_osztalyok([ut])

    def test_a_js_altal_adott_osztalyok(self):
        js = {(e.osztaly, e.fajl) for e in self.elof if e.fajl.endswith('.js')}
        self.assertIn(('nincs-jeloles', 'statikus/olvaso.js'), js)
        self.assertIn(('aktiv', 'statikus/olvaso.js'), js)
        self.assertIn(('tz-nem', 'tervezo_statikus/tervezo.js'), js)
        self.assertIn('nincs-jeloles', self.kizart)
        with tempfile.TemporaryDirectory() as tmp:
            ut = os.path.join(tmp, 'p.js')
            with open(ut, 'w', encoding='utf-8') as f:
                f.write("x.classList.add('proba-js', \"proba-js2\");\ny.classList.toggle('aktiv', !z);\n")
            hibak = regiszter_or.ellenoriz(regiszter_or.felmeres(biz=self.biz, js_fajlok=((ut, 'p.js'),)), self.reg, self.kizart)
            self.assertEqual(sorted(re.sub(r' —.*', '', h) for h in hibak if 'proba' in h),
                             ['ismeretlen CSS-osztály: proba-js (p.js:1)', 'ismeretlen CSS-osztály: proba-js2 (p.js:1)'])
            for rossz in ("x.classList.add(nev);\n", "x.classList.remove('a', b);\n", "x.className = 'a';\n",
                          "x.setAttribute('class', 'a');\n"):
                with open(ut, 'w', encoding='utf-8') as f:
                    f.write(rossz)
                with self.assertRaises(regiszter_or.Kibonthatatlan, msg=rossz):
                    regiszter_or.js_osztalyok(((ut, 'p.js'),))

    def test_a_nema_kihagyasi_mintak_hibat_adnak(self):
        d = {'nezet-': ['x'], 'par-': ['magas']}
        for ertek in ("a {{ x or 'b' }}", "a {{ 'b' if f else x }}", "szo{{ ' b' ~ x }}", "a{{ 'b' }}"):
            with self.assertRaises(regiszter_or.Kibonthatatlan, msg=ertek):
                regiszter_or.sablon_ertek(ertek, d, 'x.html', 1)
        # a feltétel literálja nem osztály; a dinamikus előtag kibomlik
        self.assertEqual(regiszter_or.sablon_ertek("ful{{ ' aktiv' if ful == 'szo' else '' }}", d, 'x.html', 1),
                         [('aktiv', True), ('ful', False)])
        self.assertEqual(regiszter_or.sablon_ertek("szo{{ ' par-' ~ w.biz if w.biz else '' }}", d, 'x.html', 1),
                         [('par-magas', True), ('szo', False)])
        with tempfile.TemporaryDirectory() as tmp:
            sd = os.path.join(tmp, 'sablonok')
            os.mkdir(sd)
            for sablon in ("<b class='egyszeres'>x</b>", "<b class=csupasz>x</b>"):
                with open(os.path.join(sd, 'a.html'), 'w', encoding='utf-8') as f:
                    f.write(sablon)
                with self.assertRaises(regiszter_or.Kibonthatatlan, msg=sablon):
                    regiszter_or.sablon_osztalyok(sd, d)
            ut = os.path.join(tmp, 'm.py')
            for src in ("def f(x):\n    return '<b class=\"a ' + x + '\">'\n", "def f():\n    return \"<b class='a'>\"\n"):
                with open(ut, 'w', encoding='utf-8') as f:
                    f.write(src)
                with self.assertRaises(regiszter_or.Kibonthatatlan, msg=src):
                    regiszter_or.py_osztalyok([ut])
            with open(ut, 'w', encoding='utf-8') as f:
                f.write("def f(h):\n    return 'class=\"jelleg ' in h\n")      # vizsgálat, nem kimenet
            self.assertEqual(regiszter_or.py_osztalyok([ut]), [])

    def test_elavult_kizart_osztaly_hibat_ad(self):
        k = dict(self.kizart, jt='szövegrész-horog')
        self.assertIn('elavult kizárt osztály: jt', '\n'.join(regiszter_or.ellenoriz(self.elof, self.reg, k)))


# =====================================================================================================================
# a szabálytérkép és az értékszűrés
# =====================================================================================================================
class TestSzabalyterkep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sz = tervezo.css_szabalyok(tervezo.css_beolvas())
        cls.a = alap_arculat()

    def test_minden_token_letezik(self):
        tok = {t for r in self.sz for _, ts in r['deklaraciok'] for t in ts}
        self.assertEqual(sorted(t for t in tok if not tervezo.token_letezik(t, self.a.adat)), [])

    def test_ismert_szabalyok(self):
        alapok = {}
        for r in self.sz:
            for r2 in r['reszek']:
                alapok.setdefault(r2['alap'], []).extend(r['deklaraciok'])
        self.assertIn(['border-radius', ['radius-csempe']], alapok['.he-szo'])
        self.assertIn(['min-width', ['space-he-csempe-min']], alapok['.he-szo'])
        self.assertIn(['font-size', ['fs-csempe-megj']], alapok['.he-szo .mf'])
        # a dinamikus állapot levágva, de megjelölve
        r = [x for x in self.sz if x['szelektor'].startswith('.szo:hover')][0]
        self.assertEqual((r['reszek'][0]['alap'], r['reszek'][0]['allapot']), ('.szo', ':hover'))
        r = [x for x in self.sz if x['szelektor'].startswith('ol.jel > li::before')][0]
        self.assertEqual(r['reszek'][0]['alap'], 'ol.jel > li')
        # média-lekérdezés
        self.assertTrue(any(r['media'].startswith('@media (max-width: 640px)') for r in self.sz))
        # a csak ál-elemből álló szelektor kimarad (::selection)
        self.assertFalse(any(r2['alap'] == '' for r in self.sz for r2 in r['reszek']))


class TestErtekszures(unittest.TestCase):
    """A mentés értékszűrése (brief 3. pont, M0 2.2, DT-F98f (a))."""

    @classmethod
    def setUpClass(cls):
        cls.a = alap_arculat()
        cls.irhato = tervezo.Regiszter.betolt(cls.a.adat).tokenek()

    def ok(self, csop, v):
        self.assertEqual(tervezo.ertek_szuro(csop, v), v)

    def rossz(self, csop, v):
        with self.assertRaises(tervezo.TervezoHiba, msg='%s %r' % (csop, v)):
            tervezo.ertek_szuro(csop, v)

    def test_szin(self):
        for v in ('#abc', '#A1B2C3', 'rgb(1, 2, 3)', 'rgb(255,255,255)', 'hsl(160, 49%, 24%)', 'hsl(360, 100%, 0%)', 'hsl(10.5, 20.25%, 30%)'):
            self.ok('szin', v)
        for v in ('red', '#abcd', '#12345', 'rgb(256, 0, 0)', 'hsl(361, 0%, 0%)', 'hsl(0, 101%, 0%)', 'rgba(0,0,0,0)', 'url(x)',
                  '#abc;}body{', 'var(--bg)', '', ' #abc', 5, None):
            self.rossz('szin', v)

    def test_betumeret(self):
        for v in ('8px', '64px', '15.5px', '0.5rem', '4rem', '0.6em', '1.15em'):
            self.ok('betumeret', v)
        for v in ('7.5px', '64.5px', '0.4rem', '4.1em', '12pt', '12', '1e1px', '12px;', '-1px', '12 px', '12.1234px'):
            self.rossz('betumeret', v)

    def test_terkoz_dt_f98f(self):
        for v in ('0px', '72px', '128px', '0rem', '8rem', '8em'):
            self.ok('terkoz', v)
        for v in ('128.5px', '129px', '8.1rem', '9em', '-2px', 'calc(1px)'):
            self.rossz('terkoz', v)

    def test_lekerekites(self):
        for v in ('0px', '999px', '6px'):
            self.ok('lekerekites', v)
        for v in ('1000px', '1rem', '0.5em'):
            self.rossz('lekerekites', v)

    def test_sorkoz(self):
        for v in ('1', '1.0', '2.4', '1.85'):
            self.ok('sorkoz', v)
        for v in ('0.9', '2.5', '1.5px', 'normal', '1,5'):
            self.rossz('sorkoz', v)

    def test_a_valtozaslista(self):
        e = lambda t: tervezo.valtozasok_ellenoriz(t, self.irhato, self.a.adat)
        self.assertEqual(e({'tokenek': {'fs-versszam': '0.7em', 'bg': {'light': '#ffffff'}}}),
                         [('betumeret', 'versszam', None, '0.7em'), ('szin', 'bg', 'light', '#ffffff')])
        for rossz in ({}, [], {'tokenek': {}}, {'tokenek': {'fs-versszam': '0.7em'}, 'x': 1}, {'tokenek': []},
                      {'tokenek': {'fs-alcim': '16px'}},                  # létező, de regiszteren kívüli token
                      {'tokenek': {'font-ui': 'Arial'}},                  # betűcsalád: szabad szöveg
                      {'tokenek': {'nincs-ilyen': '#fff'}},
                      {'tokenek': {'bg': '#ffffff'}},                     # szín téma nélkül
                      {'tokenek': {'bg': {'kek': '#ffffff'}}},
                      {'tokenek': {'bg': {}}},
                      {'tokenek': {'fs-versszam': 0.7}},
                      {'tokenek': {'--bg': {'light': '#fff'}}},
                      {'tokenek': {'fs-versszam': '0.7em', 'bg': {'light': 'javascript:alert(1)'}}}):
            with self.assertRaises(tervezo.TervezoHiba, msg=repr(rossz)):
                e(rossz)


# =====================================================================================================================
# a szinkron-kimenet a design systemhez
# =====================================================================================================================
class TestSzinkron(unittest.TestCase):
    """`arculat_szinkron.py`: a design system `tokens.json`-ja a token-fájlból (feltöltés nélkül)."""

    @classmethod
    def setUpClass(cls):
        import arculat_szinkron
        cls.sz = arculat_szinkron
        cls.a = alap_arculat()
        cls.r = tervezo.Regiszter.betolt(cls.a.adat)
        cls.css = tervezo.css_beolvas()

    def stilusok(self, ki):
        return {s['name']: s for g in ki['type']['groups'] for s in g['styles']}

    def test_alap_nelkul(self):
        ki = self.sz.tokens_json(self.a, self.r, self.css, None, '2026-10-15', 'teszt@0')
        self.assertEqual(list(ki), ['version', 'color', 'type', 'spacing', 'radius', 'name', 'meta'])
        self.assertEqual({t['name']: t['value'] for t in ki['color']['tokens']}, self.a.adat['szin'])
        st = self.stilusok(ki)
        self.assertEqual(set(st), set(self.a.adat['betumeret']))
        self.assertEqual((st['karoli-folyo']['fontSize'], st['karoli-folyo']['lineHeight']), ('1.25rem', '1.85'))
        self.assertEqual(st['oldalcim']['fontWeight'], '600')                          # a szerver értéke (M0 5. szakasz 2.)
        self.assertIn('Relatív érték: 0.6em', st['versszam']['usage'])
        self.assertIn('Versszám', st['versszam']['usage'])
        self.assertEqual({t['name']: t['value'] for t in ki['spacing']['tokens']}, {'space-' + k: v for k, v in self.a.adat['terkoz'].items()})
        self.assertEqual({t['name']: t['value'] for t in ki['radius']['tokens']}, {'radius-' + k: v for k, v in self.a.adat['lekerekites'].items()})
        self.assertEqual(ki['type']['families'], self.a.adat['betucsalad'])
        self.assertEqual(ki['meta']['paths']['tokens'], ['eszkozok/olvaso_szerver/konfig/arculat.json'])
        self.assertEqual((ki['meta']['ref'], ki['meta']['synced'], ki['meta']['arculat_hash']), ('teszt@0', '2026-10-15', self.a.hash))
        self.assertIn('Héber szócsempe', [t for t in ki['color']['tokens'] if t['name'] == 'bg'][0]['usage'])

    def test_alappal_a_leirasok_es_csoportok_maradnak(self):
        alap = {'version': 1,
                'color': {'themes': [{'id': 'light', 'name': 'Világos'}, {'id': 'dark', 'name': 'Sötét'}],
                          'tokens': [{'name': 'accent', 'value': {'light': '#000000', 'dark': '#000000'}, 'usage': 'Régi leírás'}]},
                'type': {'fonts': [{'family': 'X', 'file': 'fonts/x.woff2', 'weight': '400', 'style': 'normal'}], 'families': {},
                         'groups': [{'name': 'Olvasószöveg', 'family': 'text', 'note': '', 'styles': [
                             {'name': 'oldalcim', 'fontSize': '1px', 'lineHeight': '1', 'fontWeight': '300', 'letterSpacing': '0', 'fontStyle': 'normal',
                              'opticalSize': None, 'family': '', 'sample': 'Mózes első könyve 1', 'usage': 'A lap címe (h1).'},
                             {'name': 'interlinearis-heber', 'fontSize': '1px', 'lineHeight': '1', 'fontWeight': '400', 'family': 'he', 'usage': 'IL'}]}]},
                'spacing': {'note': '', 'tokens': [{'name': 'space-1', 'value': '4px', 'usage': ''}]},
                'radius': {'note': 'R', 'tokens': [{'name': 'radius-pill', 'value': '1px', 'usage': 'Pirula'}]},
                'name': 'PaRDeS olvasó', 'meta': {'repo': 'x', 'paths': {'fonts': ['f/']}}}
        ki = self.sz.tokens_json(self.a, self.r, self.css, alap, '2026-10-15', 'teszt@0')
        acc = ki['color']['tokens'][0]
        self.assertEqual((acc['name'], acc['value'], acc['usage']), ('accent', self.a.adat['szin']['accent'], 'Régi leírás'))
        self.assertEqual(len(ki['color']['tokens']), 19)                                # 10 + a #134 M3 műfajszínei (8) és árnyéka
        g0 = ki['type']['groups'][0]
        self.assertEqual(g0['name'], 'Olvasószöveg')
        oc = g0['styles'][0]
        self.assertEqual((oc['fontSize'], oc['lineHeight'], oc['fontWeight'], oc['usage'], oc['sample']),
                         ('1.625rem', '1.25', '600', 'A lap címe (h1).', 'Mózes első könyve 1'))
        self.assertEqual((g0['styles'][1]['fontSize'], g0['styles'][1]['family']), ('1.5rem', 'he'))
        self.assertEqual(ki['type']['groups'][-1]['name'], self.sz.UJ_CSOPORT)
        self.assertEqual(len(self.stilusok(ki)), len(self.a.adat['betumeret']))         # oldalcim + il-heber + a többi új csoportban
        self.assertEqual(ki['type']['fonts'], alap['type']['fonts'])
        self.assertNotIn('space-1', [t['name'] for t in ki['spacing']['tokens']])
        self.assertEqual((ki['radius']['tokens'][0]['name'], ki['radius']['tokens'][0]['value'], ki['radius']['tokens'][0]['usage']), ('radius-pill', '999px', 'Pirula'))
        self.assertEqual(ki['meta']['paths']['fonts'], ['f/'])
        self.assertEqual(ki['meta']['repo'], 'basesoft777/Bible-Study')


# =====================================================================================================================
# a végpont, a lapok és a kiadások
# =====================================================================================================================
@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestKiadasok(unittest.TestCase):
    """A tervező mód csak a belso kiadásban létezik; más kiadásban a végpontok 404-et adnak, és a HTML-ben nincs nyoma."""

    UTAK = ('/tervezo/kod', '/tervezo/terkep.json', '/tervezo/tervezo.js', '/tervezo/tervezo.css')

    @classmethod
    def setUpClass(cls):
        import alkalmazas
        cls.alkalmazas = alkalmazas
        cls.belso = alkalmazas.letrehoz(db_ut=DB, kiadas='belso').test_client()

    def test_belso(self):
        t = self.belso.get('/1Moz/1').get_data(as_text=True)
        self.assertIn('class="tervezo-kapcsolo"', t)
        self.assertRegex(t, r'<script src="/tervezo/tervezo\.js\?v=[0-9a-f]{16}" defer></script>')
        self.assertRegex(t, r'<link rel="stylesheet" href="/tervezo/tervezo\.css\?v=[0-9a-f]{16}">')
        # a kapcsoló a fejlécben, a szintváltó után és a témaváltó előtt
        self.assertLess(t.index('class="szintvalto"'), t.index('class="tervezo-kapcsolo"'))
        self.assertLess(t.index('class="tervezo-kapcsolo"'), t.index('class="tema"'))
        r = self.belso.get('/tervezo/tervezo.js')
        self.assertEqual(r.status_code, 200)
        self.assertIn('javascript', r.headers['Content-Type'])
        r.close()
        r = self.belso.get('/tervezo/tervezo.css')
        self.assertEqual((r.status_code, r.mimetype), (200, 'text/css'))
        r.close()
        self.assertEqual(self.belso.get('/tervezo/terkep.json').status_code, 200)

    def test_nyilvanos_es_kereskedelmi(self):
        for kiadas in ('nyilvanos', 'kereskedelmi'):
            c = self.alkalmazas.letrehoz(db_ut=DB, kiadas=kiadas).test_client()
            for ut in ('/', '/1Moz/1', '/1Moz/1/1?szo=H0430&ful=szo', '/szo/H0430', '/nincs-ilyen-konyv'):
                t = c.get(ut).get_data(as_text=True)
                self.assertNotIn('tervezo', t.lower(), (kiadas, ut))
                self.assertNotIn('tervező', t.lower(), (kiadas, ut))
            for ut in self.UTAK:
                self.assertEqual(c.get(ut).status_code, 404, (kiadas, ut))
            for ut in ('/tervezo/mentes', '/tervezo/visszaallit'):
                self.assertEqual(c.post(ut, data='{}', content_type='application/json').status_code, 404, (kiadas, ut))
                self.assertEqual(c.get(ut).status_code, 404, (kiadas, ut))
            self.assertEqual(c.get('/statikus/tervezo.js').status_code, 404, kiadas)

    def test_a_statikus_export_lapjan_nincs_tervezo(self):
        import adatbazis
        import hozzaferes
        import oldalak
        hozz = hozzaferes.Hozzaferes.betolt(KONFIG)
        gyar = oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), hozz)
        self.assertNotIn('tervezo', gyar.fejezet_lap('Ruth', 1, None, 'olvaso', hozz.szint(), '', '', '/Ruth/1').lower())

    def test_csp_nem_lazul_es_nincs_inline(self):
        for c in (self.belso, self.alkalmazas.letrehoz(db_ut=DB, kiadas='nyilvanos').test_client()):
            for ut in ('/', '/1Moz/1', '/1Moz/1/2?ful=vers', '/1Moz/1/2?ful=kh&reteg=il', '/1Moz/1?szo=H0430&ful=szo', '/szo/H0430'):
                r = c.get(ut)
                self.assertEqual(r.headers['Content-Security-Policy'], self.alkalmazas.CSP)
                t = r.get_data(as_text=True)
                self.assertIsNone(re.search(r'<script(?![^>]*\bsrc=)', t), ut)
                self.assertNotIn('<style', t, ut)
                self.assertIsNone(re.search(r'\sstyle\s*=', t), ut)
                self.assertIsNone(re.search(r'\son[a-z]+\s*=', t), ut)
        self.assertIn("script-src 'self'", self.alkalmazas.CSP)
        self.assertIn("style-src 'self'", self.alkalmazas.CSP)
        self.assertNotIn('unsafe', self.alkalmazas.CSP)
        for ut in ('/tervezo/terkep.json', '/tervezo/kod'):
            self.assertEqual(self.belso.get(ut).headers['Content-Security-Policy'], self.alkalmazas.CSP)

    def test_a_kliens_szkript_csp_kompatibilis(self):
        with open(os.path.join(tervezo.STATIKUS_DIR, 'tervezo.js'), encoding='utf-8') as f:
            js = f.read()
        for tilos in ('eval(', 'new Function', '.innerHTML', 'outerHTML', 'insertAdjacentHTML', "setAttribute('style'", 'setAttribute("style"',
                      'document.write', '.cssText', 'createElement(\'style\')', 'createElement("style")'):
            self.assertNotIn(tilos, js, tilos)
        self.assertIn("style.setProperty('--'", js)                                        # az előnézet CSS-változóval


class _Ideiglenes:
    """Az alkalmazás a konfiguráció ideiglenes másolatával (a token-fájl írása nem éri a repót)."""

    @classmethod
    def setUpClass(cls):
        import alkalmazas
        cls.tmp = tempfile.TemporaryDirectory()
        cls.kdir = os.path.join(cls.tmp.name, 'konfig')
        shutil.copytree(KONFIG, cls.kdir, ignore=shutil.ignore_patterns('*.elozo', '.*.tmp'))
        cls.app = alkalmazas.letrehoz(db_ut=DB, kiadas='belso', konfig_dir=cls.kdir)
        cls.c = cls.app.test_client()
        cls.gyar = cls.app.extensions['pardes']['gyar']
        cls.cache = cls.app.extensions['pardes']['cache']
        cls.mento = cls.app.extensions['pardes']['tervezo']
        cls.ut = os.path.join(cls.kdir, 'arculat.json')
        with open(cls.ut, 'rb') as f:
            cls.eredeti = f.read()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def tearDown(self):
        with open(self.ut, 'wb') as f:
            f.write(self.eredeti)
        if os.path.exists(self.ut + '.elozo'):
            os.remove(self.ut + '.elozo')
        self.gyar.arculat = arculat.Arculat(self.ut, self.eredeti)
        self.cache.urit()

    def fajl(self):
        with open(self.ut, 'rb') as f:
            return f.read()

    def kod(self, c=None):
        r = (c or self.c).get('/tervezo/kod')
        self.assertEqual(r.status_code, 200)
        return r.get_json()['kod']

    def ment(self, torzs, kod=None, c=None, **kw):
        h = kw.pop('headers', {})
        if kod is not None:
            h['X-Tervezo-Kod'] = kod
        return (c or self.c).post('/tervezo/mentes', data=json.dumps(torzs) if not isinstance(torzs, str) else torzs,
                                  content_type=kw.pop('content_type', 'application/json'), headers=h, **kw)


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestMentesBiztonsag(_Ideiglenes, unittest.TestCase):
    """Csak helyi kérés, csak POST, egyszeri kód; minden más 403/405, és a token-fájl változatlan."""

    TAVOLI = {'REMOTE_ADDR': '10.1.2.3'}
    TORZS = {'tokenek': {'fs-versszam': '0.7em'}}

    def test_kod_csak_helyi_kerésre(self):
        r = self.c.get('/tervezo/kod')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Cache-Control'], 'no-store')
        self.assertGreaterEqual(len(r.get_json()['kod']), 40)
        tiltott = [dict(environ_base=self.TAVOLI),
                   dict(headers={'X-Forwarded-For': '203.0.113.9'}),
                   dict(headers={'Forwarded': 'for=203.0.113.9'}),
                   dict(headers={'X-Real-IP': '203.0.113.9'}),
                   dict(base_url='http://evil.example'),                       # DNS-rebinding: idegen Host
                   dict(base_url='http://localhost.evil.example'),
                   dict(headers={'Origin': 'http://evil.example'}),
                   dict(headers={'Origin': 'http://127.0.0.1:9999'}),           # más port: más eredet
                   dict(headers={'Sec-Fetch-Site': 'cross-site'}),
                   dict(environ_base={'REMOTE_ADDR': '192.168.1.5'})]
        for kw in tiltott:
            self.assertEqual(self.c.get('/tervezo/kod', **kw).status_code, 403, kw)
        for kw in (dict(base_url='http://127.0.0.1:8765'), dict(environ_base={'REMOTE_ADDR': '::1'}, base_url='http://[::1]:8765'),
                   dict(headers={'Origin': 'http://localhost', 'Sec-Fetch-Site': 'same-origin'})):
            self.assertEqual(self.c.get('/tervezo/kod', **kw).status_code, 200, kw)

    def test_csak_post(self):
        for ut in ('/tervezo/mentes', '/tervezo/visszaallit'):
            self.assertEqual(self.c.get(ut).status_code, 405, ut)
            self.assertEqual(self.c.put(ut, data='{}').status_code, 405, ut)
        self.assertEqual(self.fajl(), self.eredeti)

    def test_kod_nelkul_rossz_koddal_403(self):
        self.assertEqual(self.ment(self.TORZS).status_code, 403)
        self.assertEqual(self.ment(self.TORZS, kod='rossz').status_code, 403)
        self.assertEqual(self.ment(self.TORZS, kod='').status_code, 403)
        self.assertEqual(self.c.post('/tervezo/visszaallit').status_code, 403)
        self.assertEqual(self.fajl(), self.eredeti)
        self.assertFalse(os.path.exists(self.ut + '.elozo'))

    def test_tavoli_keres_ervenyes_koddal_is_403(self):
        k = self.kod()
        for kw in (dict(environ_base=self.TAVOLI), dict(headers={'X-Forwarded-For': '203.0.113.9'}), dict(base_url='http://evil.example'),
                   dict(headers={'Origin': 'http://evil.example'})):
            h = dict(kw.pop('headers', {}))
            self.assertEqual(self.ment(self.TORZS, kod=k, headers=h, **kw).status_code, 403, (kw, h))
        self.assertEqual(self.fajl(), self.eredeti)

    def test_a_kod_egyszeri(self):
        k = self.kod()
        self.assertEqual(self.ment(self.TORZS, kod=k).status_code, 200)
        self.assertEqual(self.ment({'tokenek': {'fs-versszam': '0.65em'}}, kod=k).status_code, 403)
        self.assertIn(b'"0.7em"', self.fajl())

    def test_a_rossz_ertek_400_es_a_fajl_valtozatlan(self):
        for torzs in ({'tokenek': {'fs-versszam': '99px'}}, {'tokenek': {'terkoz-x': '1px'}}, {'tokenek': {'font-ui': 'x'}},
                      {'tokenek': {'fs-alcim': '16px'}}, {'tokenek': {'bg': {'light': 'red'}}}, {'tokenek': {'space-oldal': '129px'}},
                      {'tokenek': {'fs-versszam': '0.7em', 'bg': {'light': '#fff;}'}}}, {'x': 1}, '{"tokenek": ', 'nem json'):
            r = self.ment(torzs, kod=self.kod())
            self.assertEqual(r.status_code, 400, torzs)
            self.assertIn('hiba', r.get_json())
        self.assertEqual(self.ment(self.TORZS, kod=self.kod(), content_type='text/plain').status_code, 415)
        self.assertEqual(self.ment(self.TORZS, kod=self.kod(), content_type='application/x-www-form-urlencoded').status_code, 415)
        self.assertEqual(self.fajl(), self.eredeti)
        self.assertFalse(os.path.exists(self.ut + '.elozo'))

    def test_a_rossz_kerest_is_elhasznalja_a_kodot(self):
        k = self.kod()
        self.assertEqual(self.ment({'tokenek': {'fs-versszam': '99px'}}, kod=k).status_code, 400)
        self.assertEqual(self.ment(self.TORZS, kod=k).status_code, 403)


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestMentes(_Ideiglenes, unittest.TestCase):
    """A mentés: atomi írás, determinisztikus fájl, előző állapot, újratöltés újraindítás nélkül, új ETag."""

    def test_mentes_es_megjelenes_a_kovetkezo_lapkeresnel(self):
        a = self.c.get('/1Moz/1/3')
        self.assertEqual(self.c.get('/1Moz/1/3').headers['X-Cache'], 'HIT')
        regi_hash = self.gyar.arculat.hash
        r = self.ment({'tokenek': {'fs-versszam': '0.7em', 'accent': {'dark': '#99ccbb'}}}, kod=self.kod())
        self.assertEqual(r.status_code, 200, r.get_data(as_text=True))
        j = r.get_json()
        self.assertTrue(j['ok'])
        self.assertEqual(j['valtozas'], 2)
        self.assertNotEqual(j['arculat_hash'], regi_hash)
        self.assertEqual(j['arculat_hash'], self.gyar.arculat.hash)
        self.assertEqual(j['arculat_hash'], arculat.tartalom_hash(self.fajl()))
        # a következő lapkérés: új ETag, nem a gyorsítótárból, az új stíluslap-címmel
        b = self.c.get('/1Moz/1/3', headers={'If-None-Match': a.headers['ETag']})
        self.assertEqual(b.status_code, 200)
        self.assertEqual(b.headers['X-Cache'], 'MISS')
        self.assertNotEqual(b.headers['ETag'], a.headers['ETag'])
        self.assertIn('/arculat.css?v=%s"' % j['arculat_hash'], b.get_data(as_text=True))
        # más böngészőből, süti nélkül is
        friss = self.app.test_client()
        t = friss.get('/1Moz/1/3').get_data(as_text=True)
        self.assertIn('/arculat.css?v=%s"' % j['arculat_hash'], t)
        css = friss.get('/arculat.css?v=' + j['arculat_hash']).get_data(as_text=True)
        self.assertIn('--fs-versszam: 0.7em;', css)
        self.assertEqual(css.count('--accent: #99ccbb;'), 2)                                  # mindkét sötét blokkban
        self.assertIn('--accent: #1f5a49;', css)                                              # a világos változatlan

    def test_a_fajl_determinisztikus_es_a_diff_kicsi(self):
        self.assertEqual(self.ment({'tokenek': {'space-he-csempe-min': '80px'}}, kod=self.kod()).status_code, 200)
        uj = self.fajl()
        adat = json.loads(uj)
        # a sorvég a lemezes fájlé marad (core.autocrlf=true mellett a munkafa CRLF is lehet; l. test_a_crlf_sorveg_megmarad)
        sv = '\r\n' if b'\r\n' in self.eredeti else '\n'
        self.assertEqual(uj.decode('utf-8'), (json.dumps(adat, ensure_ascii=False, indent=2, sort_keys=True) + '\n').replace('\n', sv))
        diff = [s for s in difflib.unified_diff(self.eredeti.decode().splitlines(), uj.decode().splitlines(), lineterm='', n=0)
                if s[:1] in '+-' and not s.startswith(('+++', '---'))]
        self.assertEqual(diff, ['-    "he-csempe-min": "72px",', '+    "he-csempe-min": "80px",'])
        # a fájlba csak a token-fájl ismert csoportjai kerültek, szabad szöveg nincs
        self.assertEqual(set(adat), set(json.loads(self.eredeti)))

    def test_elozo_allapot_es_visszaallitas(self):
        self.assertEqual(self.c.post('/tervezo/visszaallit', headers={'X-Tervezo-Kod': self.kod()}).status_code, 409)   # nincs előző
        self.assertEqual(self.ment({'tokenek': {'lh-torzs': '1.7'}}, kod=self.kod()).status_code, 200)
        with open(self.ut + '.elozo', 'rb') as f:
            self.assertEqual(f.read(), self.eredeti)
        mentett = self.fajl()
        r = self.c.post('/tervezo/visszaallit', headers={'X-Tervezo-Kod': self.kod()})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.fajl(), self.eredeti)
        self.assertEqual(r.get_json()['arculat_hash'], arculat.tartalom_hash(self.eredeti))
        self.assertEqual(self.gyar.arculat.hash, arculat.tartalom_hash(self.eredeti))
        with open(self.ut + '.elozo', 'rb') as f:
            self.assertEqual(f.read(), mentett)                                                # a visszaállítás is visszavonható

    def test_atomi_iras_hiba_eseten_a_fajl_valtozatlan(self):
        regi = self.gyar.arculat
        valodi = os.replace

        def hibas_replace(src, dst):
            if dst == self.ut:
                raise OSError('próba: az átnevezés meghiúsul')
            return valodi(src, dst)

        with mock.patch.object(tervezo.os, 'replace', side_effect=hibas_replace):
            with self.assertRaises(OSError):
                self.mento.mentes({'tokenek': {'fs-versszam': '0.7em'}})
        self.assertEqual(self.fajl(), self.eredeti)
        self.assertIs(self.gyar.arculat, regi)
        self.assertEqual([n for n in os.listdir(self.kdir) if n.endswith('.tmp')], [])

    def test_a_lemezes_fajl_az_irany(self):
        """A token létezése a lemezes fájl szerint (arra ír): a lemezen hiányzó kulcs 400, nem 500; a nem érvényes lemezes
        fájl 500, külön üzenettel (nem „a törzs nem érvényes JSON”); a fájl mindkét esetben változatlan."""
        adat = json.loads(self.eredeti)
        del adat['betumeret']['versszam']
        hianyos = json.dumps(adat, ensure_ascii=False, indent=2, sort_keys=True).encode('utf-8') + b'\n'
        for lemez, kod, minta in ((hianyos, 400, 'nem regisztrált token'),
                                  (b'{"verzio": 1, ', 500, 'a lemezes token-fájl nem érvényes'),
                                  (self.eredeti.replace(b'"verzio": 1', b'"verzio": 2'), 500, 'a lemezes token-fájl nem érvényes')):
            with open(self.ut, 'wb') as f:
                f.write(lemez)
            r = self.ment({'tokenek': {'fs-versszam': '0.7em'}}, kod=self.kod())
            self.assertEqual(r.status_code, kod, r.get_data(as_text=True))
            self.assertIn(minta, r.get_json()['hiba'])
            self.assertNotIn('a törzs nem érvényes JSON', r.get_json()['hiba'])
            self.assertEqual(self.fajl(), lemez)
            self.assertFalse(os.path.exists(self.ut + '.elozo'))

    def test_nincs_ideiglenes_fajl_a_mentes_utan(self):
        self.assertEqual(self.ment({'tokenek': {'radius-csempe': '8px'}}, kod=self.kod()).status_code, 200)
        self.assertEqual([n for n in os.listdir(self.kdir) if n.endswith('.tmp')], [])

    def test_a_crlf_sorveg_megmarad(self):
        with open(self.ut, 'wb') as f:
            f.write(self.eredeti.replace(b'\n', b'\r\n'))
        self.assertEqual(self.ment({'tokenek': {'radius-csempe': '8px'}}, kod=self.kod()).status_code, 200)
        uj = self.fajl()
        self.assertEqual(uj.count(b'\r\n'), uj.count(b'\n'))

    def test_terkep(self):
        r = self.c.get('/tervezo/terkep.json')
        self.assertEqual(r.headers['Cache-Control'], 'no-cache')
        self.assertEqual(self.c.get('/tervezo/terkep.json', headers={'If-None-Match': r.headers['ETag']}).status_code, 304)
        t = r.get_json()
        self.assertEqual(len(t['regiszter']), 83 + 18)                    # a tájoló pirula kikerült (DT-F134n)
        self.assertEqual(t['arculat_hash'], self.gyar.arculat.hash)
        self.assertEqual(t['tokenek']['bg'], {'csoport': 'szin', 'tipus': 'szin', 'ertek': {'light': '#f5f2ea', 'dark': '#151918'}, 'irhato': True})
        self.assertFalse(t['tokenek']['fs-csempe-megj']['irhato'])                            # regiszteren kívüli: csak előnézet
        self.assertFalse(t['tokenek']['font-ui']['irhato'])
        self.assertEqual(t['tartomany']['terkoz']['px'], [0, 128])
        mf = [x for x in t['szabalyok'] if any(p['alap'] == '.he-szo .mf' for p in x['reszek'])][0]
        self.assertIn(['font-size', ['fs-csempe-megj']], mf['deklaraciok'])
        # a mentés után új ETag
        self.assertEqual(self.ment({'tokenek': {'radius-csempe': '8px'}}, kod=self.kod()).status_code, 200)
        self.assertNotEqual(self.c.get('/tervezo/terkep.json').headers['ETag'], r.headers['ETag'])


# =====================================================================================================================
# a regiszter szelektorai a valódi lapokon
# =====================================================================================================================
URES_ELEM = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}


class Csp:
    __slots__ = ('tag', 'attr', 'osztaly', 'szulo', 'gyerek')

    def __init__(self, tag, attr, szulo):
        self.tag, self.attr, self.szulo, self.gyerek = tag, attr, szulo, []
        self.osztaly = set((attr.get('class') or '').split())


class Fa(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.gyoker = Csp('#doc', {}, None)
        self.verem = [self.gyoker]
        self.mind = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        n = Csp(tag, {k: (v or '') for k, v in attrs}, self.verem[-1])
        self.verem[-1].gyerek.append(n)
        self.mind.append(n)
        if tag not in URES_ELEM:
            self.verem.append(n)

    def handle_startendtag(self, tag, attrs):
        n = Csp(tag, {k: (v or '') for k, v in attrs}, self.verem[-1])
        self.verem[-1].gyerek.append(n)
        self.mind.append(n)

    def handle_endtag(self, tag):
        for i in range(len(self.verem) - 1, 0, -1):
            if self.verem[i].tag == tag:
                del self.verem[i:]
                return


def _lepesek(resz):
    """Egy összetett szelektor lépései balról jobbra: [(kombinátor, egyszerű szelektor)]; kombinátor: ' ' vagy '>'."""
    ki, akt, mely, komb = [], '', 0, None
    i = 0
    while i < len(resz):
        ch = resz[i]
        if ch in '([':
            mely += 1
        elif ch in ')]':
            mely -= 1
        if mely == 0 and (ch.isspace() or ch == '>'):
            if akt:
                ki.append((komb, akt))
                akt = ''
                komb = ' '
            if ch == '>':
                komb = '>'
            i += 1
            continue
        akt += ch
        i += 1
    if akt:
        ki.append((komb, akt))
    return ki


def _egyszeru_illik(n, sel):
    m = re.match(r'^([a-z][a-z0-9]*|\*)?', sel)
    if m.group(1) and m.group(1) != '*' and n.tag != m.group(1):
        return False
    s = sel[m.end():]
    while s:
        m = re.match(r'^\.([A-Za-z_][\w-]*)', s)
        if m:
            if m.group(1) not in n.osztaly:
                return False
            s = s[m.end():]
            continue
        m = re.match(r'^\[([\w-]+)(?:="([^"]*)")?\]', s)
        if m:
            if m.group(1) not in n.attr or (m.group(2) is not None and n.attr[m.group(1)] != m.group(2)):
                return False
            s = s[m.end():]
            continue
        if s.startswith(':not('):
            mely, j = 1, 5
            while mely:
                mely += {'(': 1, ')': -1}.get(s[j], 0)
                j += 1
            if illik(n, s[5:j - 1]):
                return False
            s = s[j:]
            continue
        raise ValueError('a teszt illesztője nem ismeri: %r' % s)
    return True


def _lanc_illik(n, lep):
    komb, sel = lep[-1]
    if n is None or n.tag == '#doc' or not _egyszeru_illik(n, sel):
        return False
    if len(lep) == 1:
        return True
    if komb == '>':
        return _lanc_illik(n.szulo, lep[:-1])
    p = n.szulo
    while p is not None and p.tag != '#doc':
        if _lanc_illik(p, lep[:-1]):
            return True
        p = p.szulo
    return False


def illik(n, szelektor):
    return any(_lanc_illik(n, _lepesek(r)) for r in tervezo.szelektor_reszek(szelektor))


class TestIlleszto(unittest.TestCase):
    def test_a_teszt_illesztoje(self):
        fa = Fa('<div class="cimkek"><span class="cimke arany">a</span></div><p><span class="cimke">b</span></p>'
                '<ol class="jel"><li data-jel="1"><ol class="al"><li>x</li></ol></li></ol><div class="tema"><button aria-pressed="true">t</button></div>')
        cimkek = [n for n in fa.mind if 'cimke' in n.osztaly]
        self.assertEqual([illik(n, '.megj, .szam, .cimke:not(.cimkek .cimke)') for n in cimkek], [False, True])
        self.assertEqual([illik(n, '.cimkek .cimke.arany') for n in cimkek], [True, False])
        li = [n for n in fa.mind if n.tag == 'li']
        self.assertEqual([illik(n, 'ol.jel > li') for n in li], [True, False])
        self.assertEqual([illik(n, 'ol.jel > li, ol.al > li') for n in li], [True, True])
        b = [n for n in fa.mind if n.tag == 'button'][0]
        self.assertTrue(illik(b, '.tema button[aria-pressed="true"]'))
        self.assertFalse(illik(b, '.tema button[aria-pressed="false"]'))


# a lapok, amelyeken a regiszter minden szelektorának találnia kell (a belső kiadás alapértelmezett szintjén)
LAPOK = (
    '/', '/1Moz', '/nincs-ilyen-konyv',
    '/1Moz/1', '/1Moz/1?reteg=il', '/1Moz/1?ful=info',
    '/1Moz/1/1?szo=H0430&ful=szo', '/1Moz/1/2?ful=vers', '/1Moz/1/2?ful=kh', '/1Moz/1/2?ful=temak', '/1Moz/1/2?ful=motivum',
    '/Jan/1/1?szo=G3056&ful=szo', '/Jan/1/1?reteg=il', '/Zsolt/22/2?szo=H0410&ful=szo&reteg=il',
    '/szo/H0430', '/szo/G3056', '/szo/H7307', '/szo/H6440',
    '/szo/H1254',                       # ige: törzscímek (.torzs h5, .vz-torzs), magyar fordítás nélkül (.allapot.folyamat)
)
TOREDEKEK = ('/r/szo/G3056?ig=Jan/1/1', '/r/szo/H0430?ig=1Moz/1/1', '/r/vers/1Moz/1/1', '/r/vers/Jan/1/1')


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestSzelektorokAValodiLapokon(unittest.TestCase):
    """A regiszter minden szelektora legalább egy valódi lapon talál elemet (brief 4. pont, M2)."""

    def test_minden_szelektor_talal(self):
        import alkalmazas
        app = alkalmazas.letrehoz(db_ut=DB, kiadas='belso')
        c = app.test_client()
        reg = app.extensions['pardes']['regiszter']
        csomopontok = []
        for ut in LAPOK + TOREDEKEK + tuple(os.environ.get('PARDES_TERVEZO_LAPOK', '').split()):
            r = c.get(ut)
            self.assertIn(r.status_code, (200, 404), ut)
            csomopontok += Fa(r.get_data(as_text=True)).mind
        hiany = [e['id'] + ' ' + e['szelektor'] for e in reg.elemek if not any(illik(n, e['szelektor']) for n in csomopontok)]
        self.assertEqual(hiany, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
