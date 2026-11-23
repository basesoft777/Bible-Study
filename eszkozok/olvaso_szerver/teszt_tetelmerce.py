#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_tetelmerce.py -- F231: a tételenkénti gépi mérce (az olvasó-javítás „kész” mércéje, IRANY.md 1. szál).

Miért kell: a `naplok/F231_jelentes.md` 3. szakasza a 60 felmért hiba kimenetét emberi szöveggel rögzíti („előtte” / „utána”); a
„kész” állítás csak akkor gépi, ha mind az 58 tétel (a 60-ból a 23. és az 59. kimarad, l. a jelentés 0. pontját) egy-egy ellenőrzés.
Tételenként egy teszt (`test_t01` … `test_t60`):

  * **J** (javítva): az élő lap (a Flask belső kliense, a `pardes.db`-n) a javított alakot mutatja, és a hibás alak nincs rajta;
    a jelentés sora `J`;
  * **V** (elvetve), **R** (rád vár; az adathiba is, pl. #14, N-F231a): a jelentés sora áll, kimenettel és egysoros indokkal (az „Utána”
    cella legalább egy mondat); ahol a lapon ellenőrizhető állapot is van (V: a hiba már nem látszik; R: a szöveg igaz), azt is nézi;
  * **J/R**, **J (+N49)**: a javított rész élőben, a rád váró rész a jelentés sorában.

Az ellenőrzés fajtái (`E`): `van` / `nincs` a látható szövegben (a F232 pillanatképe, a csukott lenyílók `▸ ` sorai nélkül),
`van_kep` / `nincs_kep` a teljes pillanatképben (a csukott tartalommal), `html` / `nincs_html` a nyers HTML-ben, `blokksor` a
`data-blokk`-ok sorrendje. A szöveg és a minta NFC-re normalizálva hasonlít (a héber pontozás sorrendje miatt).

Futtatás: `python eszkozok/teszt_futtat.py --fajl teszt_tetelmerce`. Kimenet: tételenként `TÉTELMÉRCE #nn: ZÖLD|PIROS|KIMARAD`, a végén
`TÉTELMÉRCE: n/58 zöld` (ez a sor kerül a PR első sorába). Adatbázis vagy Flask nélkül az élő ellenőrzések kimaradnak (nem zöldek).
"""
import json
import os
import re
import sys
import time
import unicodedata
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)

from teszt_olvasoi_merce import pillanatkep, CSUKOTT_JEL  # noqa: E402

DB = os.environ.get('PARDES_DB') or os.path.join(GY, 'pardes.db')
VAN_DB = os.path.exists(DB)
try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False
ELO = VAN_DB and VAN_FLASK

JELENTES = os.path.join(GY, 'naplok', 'F231_jelentes.md')
NYITOTT_AG = os.path.join(GY, 'nyitott', 'uj', 'olvaso-egyben-3464e1.md')
CSS = os.path.join(D, 'statikus', 'olvaso.css')
ARCULAT = os.path.join(D, 'konfig', 'arculat.json')
KIMARAD = (23, 59)          # a megbízás szerint kívül esik (fizetős fordítás; motívumlap, F164)
OSSZES = 58

# a három kimenet (IRANY.md „Így dolgozunk”): javítva / elvetve / rád vár; vegyes sor (J/R) és megjegyzés (J (+N49)) megengedett
KIMENET_RE = r'^[JVR](?:/[JVR])?(?: \(\+N\d+\))?$'
KUTATO = 'kutato'          # a hozzáférési szint, amelyen a blokk látszik (a TSK és a motívumadat)


def E(url, fajta, minta, szint=None):
    return (url, fajta, minta, szint)


# --- a tételek: (a jelentés elvárt kimenete, élő ellenőrzések) --------------------------------------------------------------------------
H1242, H0430 = '/szo/H1242', '/szo/H0430'
TETELEK = {
    1: ('J', [E(H0430, 'van', r'a Krónikák \(31-szer\); Dán 11:37'),
              E(H0430, 'nincs', r'^Dán 11:37')]),                                   # a felsorolás nem vágódik fej nélküli sorra
    2: ('J', [E(H1242, 'van', r'^az éjszaka végéről \(ellentétben: לַיְלָה‎?\) 2Móz 10:13 \(J\)'),
              E(H1242, 'nincs', r'^\(szemben')]),
    3: ('J', [E(H1242, 'nincs', r'(^|\s)(l\.|vö\.)$'), E(H1242, 'nincs', r'^—$'), E(H1242, 'nincs', r' & '),
              E(H1242, 'nincs', r'\s\+[,;]'), E(H1242, 'van', r'és máshol')]),
    4: ('J', [E(H1242, 'nincs_html', r'class="[^"]*chip'),
              E(H1242, 'html', r'title="feloldva: 2Móz 34:25">34:25</a>')]),           # a folytatólagos hely feloldva, a súgóban
    5: ('J', [E(H1242, 'van', r'ellentétben: לֵילוֺת'), E(H1242, 'van', r'\(párhuzamban: מחר'), E(H1242, 'van', r'\(ellentétben: הַיּוֺם ma\)'),
              E(H1242, 'nincs', r'‖|\|\||szemben ')]),
    6: ('J', [E(H0430, 'html', r'Ézs<sup>2</sup> \(9-szer\)'), E('/szo/H3615', 'html', r'Dl<sup>HWB</sup>'),
              E('/szo/H3615', 'nincs', r'\^'),
              E(H0430, 'html', r'<abbr title="Targum, arámi fordítás">Targum</abbr>'),
              E(H0430, 'nincs', r'\^|ᵑ7|ᵐ5')]),
    7: ('J', [E(H0430, 'van', r'\(R, l\. Di 7:13\)'), E(H0430, 'html', r'<abbr title="A\. Dillmann">Di</abbr>'),
              E(H0430, 'nincs_html', r'<a [^>]*>Di 7:13</a>')]),
    8: ('J', [E(H1242, 'van', r'לַבּ׳ Ámós 4:4 7-szer'),
              E(H1242, 'nincs', r'(^|[\s(])׳[א-ת]'), E(H0430, 'nincs', r'(^|[\s(])׳[א-ת]')]),
    9: ('J', [E(H0430, 'html', r'<abbr class="rovidites" title="a címszó: אֱלֹהִים \(elóhím\)"[^>]*>א׳</abbr>'),
              E(H0430, 'van', r'א׳ אדני אברהם'), E(H0430, 'nincs_kep', r'א׳ אברהם אדני')]),
    10: ('J', [E(H1242, 'van', r'^1reggel131 hivatkozás$'), E(H1242, 'van', r'^2holnap, másnap71 hivatkozás$'),
               E(H1242, 'van', r'^Apparátus és szövegkritika \d+ tétel$'),       # F231.17: a blokk marad, a szám felirattal
               E(H1242, 'nincs', r'^Apparátus és szövegkritika \d+$')]),
    11: ('J', [E('/szo/H7837', 'van', r'^A szótár ezt a szócikket nem tagolja számozott jelentésekre; a teljes szöveg áll\.$'),
               E('/szo/H3615', 'van', r'^A szótár itt ragozott alakokat sorol; .*a törzs szövege egyben áll\.$'),
               E('/szo/H3615', 'nincs', r'^1—25$')]),
    12: ('J', [E('/szo/H2416', 'html', r'<details class="[^"]*"[^>]* open[^>]*>\s*<summary[^>]*>A magyar szócikk teljes szövege'),
               E('/szo/H2416', 'van', r'A tagolt kártya .*nem adja vissza|nem minden szövegrészét adja vissza|teljes szöveg nyitva')]),
    13: ('J', [E('/r/szo/H0747', 'van', r'^Lefordítva · gépi fordítás'), E('/r/szo/H0747', 'van', r'Hámán fia'),
               E('/r/szo/H0747', 'nincs_kep', r'nyers szöveg')]),
    14: ('R', []),          # az adathiba (N-F231a) rád vár: adat-PR a #231 után (integrátori döntés, 2026-11-23)
    15: ('J', [E(H1242, 'van', r'2Móz 10:13 \(J\) 3Móz 6:2 \(P\)'),
               E(H1242, 'van_kep', r'^▸ forrásjel 2Móz 10:13 \(J\) · 3Móz 6:2 \(P\) · 2Móz 23:18; 34:25 \(mindkettő J E\)'),
               E(H1242, 'nincs_kep', r'^▸ forrásjel \(')]),                                 # F231.17: az apparátusban a helyével
    16: ('J', [E('/szo/H1242?vers=1Moz/1/5', 'van', r'^A BDB besorolása: 1Móz 1:5$'),
               E('/szo/H1242?vers=1Moz/1/5', 'van', r'^A szótár ezt a helyet ebbe a jelentésbe sorolja: 1\. e\.'),
               E('/szo/H1242?vers=1Moz/1/5', 'blokk_db', ('szo.bdb_apparatus', r'Ebben a versben', 0))]),   # a kártyában (a szo.ebben blokk más)
    17: ('V', [E('/szo/H2403', 'nincs_kep', r'Külön meghatározás nélkül')]),
    18: ('R', [E('/szo/H7451', 'van', r'hivatkozás a szövegben kattintható, de a jelentéspontja ebben a tagolásban nem azonosítható')]),
    19: ('J', [E('/szo/H0026', 'html', r'href="/1Sam/25/18"'), E('/szo/H0026', 'nincs_html', r'/2Sam/25/18|2Sam 25:18')]),
    20: ('J', [E('/szo/H0127', 'van', r'פָּֽצְתָה הָא׳ אֶת־פִּיהָ‎? 4Móz 16:30 \(P\)'),
               E('/szo/H0127', 'nincs_kep', r'אֶת־מִּיהָ|אֶתמִּֿיהָ|מָּֽצְתָה')]),
    21: ('J', [E('/szo/G0264', 'blokksor', ('szo.szotar', 'szo.elofordulas', 'szo.karoli_alakok', 'szo.thayer')),
               E('/szo/G0264', 'nincs_kep', r'^## \[szo\.tbesg\]\n(?:.*\n)*?## \[szo\.szotar\]')]),
    22: ('J', [E('/szo/G0264', 'van', r'^Magyar fordítás nincs · az angol eredeti áll'),
               E('/szo/G0264', 'html', r'Magyar fordítás nincs · az angol eredeti áll(?:(?!data-blokk=).)*lang="en"')]),
    24: ('R', []),
    25: ('J', [E('/szo/G0264?vers=Rom/3/23', 'van', r'^A Thayer besorolása: Róm 3:23$'),
               E('/szo/G0264?vers=Rom/3/23', 'html', r'class="igehely bdb-itt" href="/Rom/3/23"')]),
    26: ('R', []),
    27: ('J', [E('/szo/G0264', 'van', r'^1\. to sin; to engage in wrongdoing; sin · Sin, Wrongdoing, Guilt$'),
               E('/szo/G0264', 'nincs_kep', r'\d{13,}'), E('/szo/H0251', 'nincs_kep', r'\d{13,}')]),
    28: ('J', [E('/szo/G0264', 'van', r'^43 előfordulás 37 versben\.$'), E('/szo/G0264', 'van', r'^Az első 5 vers áll a 37 közül\.$'),
               E('/szo/G0264', 'van', r'^Igehely \| Károli-szöveg \| Jelentés \(UBS\)$')]),
    29: ('J/R', [E('/szo/G0264?vers=Rom/3/23', 'van', r'^A szótár ezt a helyet ebbe a jelentésbe sorolja: ')]),
    30: ('J', [E('/1Moz/1/1', 'van', r'^בְּרֵאשִׁ֖ית ?berésít$'),
               E('/1Moz/1/1', 'van', r'^1 \| Kezdetben \| בְּ \+ רֵאשִׁ֖ית \| H9003 \+ H7225 \|')]),
    31: ('J', [E('/1Moz/3/6', 'van', r'^לְאִישָׁ֛הּ ?leísáh$')]),
    32: ('J', [E('/1Moz/1/1', 'blokk_db', ('vers.heber_csempe', r'berésít', 1))]),     # a kiejtés a kereten, a csempék nem ismétlik
    33: ('V', [E('/1Moz/3/6', 'van', r'^גַּם ?gam(?!-)')]),
    34: ('J', [E('/Jan/1/1', 'van_kep', r'\| ἀρχῇ \| arkhé \|'), E('/Jan/1/1', 'nincs_kep', r'arkhéa|ēa\b')]),
    35: ('J', [E('/Jan/1/1', 'van_kep', r'\| λόγος \| logosz \|'), E('/Jan/1/1', 'nincs_kep', r'λόγος, \| logosz')]),
    36: ('V', [E('/1Moz/1/1', 'html', r'<details class="forrasszoveg" open>\s*<summary[^>]*>Táblázatos nézet \(a csempék adatai soronként\)'),
               E('/1Moz/1/1', 'van', r'^Táblázatos nézet \(a csempék adatai soronként\)$')]),    # F231.17: nyitva, a main szerint
    37: ('J', [E('/Zsolt/22/2', 'van', r'^Versszámozás: héber \(MT\) 22:2 · angol \(KJV\) 22:1$'),
               E('/Zsolt/22/2', 'van', r'^Septuaginta-versszám: Zsolt 21:2$'), E('/Zsolt/22/2', 'nincs_kep', r'Osztály \| KJV-versszám')]),
    38: ('J', [E('/1Moz/1/5', 'van_kep', r'\| 99% \(Mózes öt könyve\)$'), E('/1Moz/1/5', 'nincs_kep', r'\| magas$')]),
    39: ('R', [E('/1Moz/1/1', 'van', r'^Ez az adat ebben a kiadásban még nem érhető el\.')]),
    40: ('J (+N49)', [E('/Zsolt/22/2', 'van', r'^A BSB-forrás ehhez a vershez nem ad szavakat \(a forrásból hiányzik\)\.$')]),
    41: ('V', []),
    42: ('J', [E('/Zsolt/22/2', 'html', r'<td>PROPHECY</td><td></td>'), E('/Zsolt/22/2', 'nincs_html', r'<td>PROPHECY</td><td>\.</td>')]),
    43: ('J', [E('/1Moz/1/1', 'html', r'<p class="megj">68 kereszthivatkozás; az első 15 áll, a szavazatszám szerint\.</p>\s*(?:<div[^>]*>\s*)?<table', KUTATO),
               E('/1Moz/1/1', 'nincs_kep', r'Összesen \d+ hivatkozás', KUTATO)]),
    44: ('J', [E('/r/vers/1Moz/4/7', 'html', r'<th>Értelmezési szint</th>'),    # a Motívum fül töredéke
               E('/r/vers/1Moz/4/7', 'nincs_kep', r'PaRDeS-szint'), E('/r/vers/Zsolt/116/4', 'nincs_kep', r'PaRDeS-szint')]),
    45: ('V', [E(H1242, 'van', r'^Strong-szótár forrásadat modell-kimenet$'),      # F231.17: a jelleg-címke a cím mellett, a main szerint
               E(H1242, 'html', r'<h3>Strong-szótár <span class="jelleg jelleg-forras" title="[^"]+">forrásadat</span>')]),
    46: ('J', [E(H1242, 'nincs_kep', r'Strong_szotar \(strong_szotar\)|projekt_adat'), E(H1242, 'nincs_html', r'forras-reszlet'),
               E(H1242, 'van', r'^Forrás és licenc: Strong szotar: CC BY 4\.0 · TBESH\+TAHOT\+a projekt saját adata: ')]),
    47: ('V', [E('/Jan/1/1', 'nincs', r'^Ezekben a forrásokban erre nincs adat'),         # F231.17: az üres blokk a helyén, a main szerint
               E('/Jan/1/1', 'blokk_db', ('vers.lxx_par', r'Nincs adat \(üres eredmény, nem negatív lelet\)\.', 1))]),
    48: ('J', [E('/Zsolt/22/2', 'nincs_kep', r'lxx_os_etalon')]),
    49: ('V', [E('/Zsolt/22/2', 'van', r'forrásadat gépi feldolgozás a Strong-címkék GPL-eredetűek: nyilvános kiadásból kimarad$')]),
    50: ('J', [E(H1242, 'van', r'^A szó saját lapja · Minden előfordulás versenként \(keresés\)$'),
               E(H1242, 'nincs_kep', r'szó-lap önálló címen')]),
    51: ('J', [E('/', 'van', r'^Biblialex olvasó$'), E('/', 'nincs_kep', r'PaRDeS olvasó')]),
    52: ('J', [E('/', 'van_kep', r'Szint nyilvános regisztrált kutató'), E('/', 'nincs_kep', r'nyilvanos regisztralt')]),
    53: ('J', [E('/', 'van_kep', r'Biblia és könyv kiválasztása')]),
    54: ('J', []),          # CSS-kontraszt: test_t54
    55: ('J', []),          # érintési cél és kontraszt: test_t55
    56: ('J', [E(H1242, 'van', r'^214 előfordulás$'), E(H1242, 'van', r'^29 könyvben$'), E(H1242, 'van', r'^221 Károli-előfordulás$')]),
    57: ('J', [E(H1242, 'van', r'^Mind a 66 könyv szó szintű párjai alapján\.$'), E(H1242, 'html', r'<meter class="sav"'),
               E(H1242, 'nincs_kep', r'A 66 feldolgozott könyv \(')]),
    58: ('V', [E(H1242, 'html', r'reggel <span class="angol-kis" lang="en">morning</span>')]),     # F231.17: a main szerint
    60: ('J', []),          # sebesség: test_t60
}
assert len(TETELEK) == OSSZES and not set(KIMARAD) & set(TETELEK)

_EREDMENY = {}


def nfc(s):
    return unicodedata.normalize('NFC', s)


def jelentes_sorok():
    """A jelentés 3. szakaszának táblázata: {sorszám: (kimenet, url, előtte, utána)}."""
    with open(JELENTES, encoding='utf-8') as f:
        s = f.read()
    m = re.search(r'^## 3\. .*?$(.*?)^## 4\. ', s, re.M | re.S)
    ki = {}
    for sor in (m.group(1) if m else '').splitlines():
        r = re.match(r'^\|\s*(\d+)\s*\|(.*)\|\s*$', sor)
        if r:
            cellak = [c.strip() for c in r.group(2).split(' | ')]
            if len(cellak) >= 4:
                ki[int(r.group(1))] = tuple(cellak[:4])
    return ki


# --- kontraszt (WCAG 2.x) ----------------------------------------------------------------------------------------------------------
def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lum(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (c(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontraszt(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def keveres(a, b, arany):
    """`color-mix(in srgb, a arany%, b)`."""
    return tuple(round(x * arany + y * (1 - arany)) for x, y in zip(a, b))


def _szinek_keres():
    with open(ARCULAT, encoding='utf-8') as f:
        a = json.load(f)
    for v in a.values():
        if isinstance(v, dict) and 'g-kis' in v:
            return v
    raise KeyError('az arculat.json-ban nincs színtábla (g-kis)')


def css_szabaly(szelektor_minta):
    with open(CSS, encoding='utf-8') as f:
        css = f.read()
    m = re.search(szelektor_minta + r'\s*\{([^}]*)\}', css)
    return m.group(1) if m else None


# =====================================================================================================================
class _Lapok:
    """Az élő lapok, URL-enként egyszer lekérve (alap- és kutatói szinten)."""

    def __init__(self):
        import teszt_olvasoi_merce as M
        self.kliens = {None: M.app_kliens(), KUTATO: M.app_kliens()}
        self.kliens[KUTATO].get('/szint/%s?vissza=/' % KUTATO)
        self.tar = {}

    def html(self, url, szint=None):
        k = (url, szint)
        if k not in self.tar:
            r = self.kliens[szint].get(url)
            if r.status_code != 200:
                raise AssertionError('%s: %s' % (url, r.status_code))
            h = nfc(r.get_data(as_text=True))
            self.tar[k] = (h, pillanatkep(h))
        return self.tar[k]


class TetelMerce(unittest.TestCase):
    lapok = None

    @classmethod
    def setUpClass(cls):
        cls.sorok = jelentes_sorok()
        if ELO:
            cls.lapok = _Lapok()

    @classmethod
    def tearDownClass(cls):
        zold = sum(1 for v in _EREDMENY.values() if v == 'ZÖLD')
        for n in sorted(_EREDMENY):
            print('TÉTELMÉRCE #%02d: %s' % (n, _EREDMENY[n]))
        print('TÉTELMÉRCE: %d/%d zöld' % (zold, OSSZES))

    # --- közös ellenőrzők -----------------------------------------------------------------------------------------------------------
    def jelentes_sor(self, n, kimenet):
        self.assertIn(n, self.sorok, '#%d: nincs sora a jelentés 3. szakaszában' % n)
        k, url, elotte, utana = self.sorok[n]
        self.assertEqual(k, kimenet, '#%d: a jelentés kimenete %r, a mérce %r' % (n, k, kimenet))
        self.assertTrue(url and elotte, '#%d: üres URL vagy „előtte” cella' % n)
        self.assertRegex(k, KIMENET_RE, '#%d: a kimenet csak javítva / elvetve / rád vár lehet (J, V, R): %r' % (n, k))
        if kimenet != 'J':
            # elvetve / rád vár: egysoros indok (legalább egy teljes mondat az „Utána” cellában)
            self.assertGreaterEqual(len(re.sub(r'[*`„”]', '', utana)), 40, '#%d: az indok hiányzik vagy túl rövid: %r' % (n, utana))
            self.assertRegex(utana, r'[a-záéíóöőúüű]{3,}.*[.;:)]', '#%d: az indok nem mondat: %r' % (n, utana))
            if 'R' in kimenet.split('/'):
                self.assertRegex(utana, r'[Rr]ád vár', '#%d: a „rád vár” tétel sora nem mondja ki, kire vár' % n)
        return utana

    def elo(self, n, ell):
        if not ell:
            return
        if not ELO:
            self.skipTest('nincs pardes.db vagy Flask: az élő ellenőrzés kimarad')
        for url, fajta, minta, szint in ell:
            h, kep = self.lapok.html(url, szint)
            lathato = '\n'.join(s for s in kep.split('\n') if not s.startswith(CSUKOTT_JEL))
            hol = '#%d %s %s' % (n, url, fajta)
            if fajta == 'blokksor':
                blokkok = re.findall(r'data-blokk="([^"]+)"', h)
                poz = [blokkok.index(b) if b in blokkok else -1 for b in minta]
                self.assertTrue(all(p >= 0 for p in poz) and poz == sorted(poz), '%s: %s (a lapon: %s)' % (hol, minta, blokkok[:12]))
                continue
            if fajta == 'blokk_db':
                blokk, m, db = minta
                r = re.search(r'^## \[%s\]\n(.*?)(?=^## \[|\Z)' % re.escape(blokk), kep if db == 0 else lathato, re.M | re.S)
                self.assertIsNotNone(r, '%s: nincs %s blokk' % (hol, blokk))     # a hiány (db == 0) a csukott tartalomra is áll
                self.assertEqual(len(re.findall(nfc(m), r.group(1))), db, '%s: %r a %s blokkban' % (hol, m, blokk))
                continue
            szoveg = {'van': lathato, 'nincs': lathato, 'van_kep': kep, 'nincs_kep': kep, 'html': h, 'nincs_html': h}[fajta]
            talal = re.search(nfc(minta), szoveg, re.M | (re.S if fajta in ('html', 'nincs_html') else 0))
            if fajta.startswith('nincs'):
                self.assertIsNone(talal, '%s: a hibás alak még látszik: %r' % (hol, talal and talal.group(0)[:200]))
            else:
                self.assertIsNotNone(talal, '%s: a javított alak nem látszik: %r' % (hol, minta))

    def tetel(self, n):
        kimenet, ell = TETELEK[n]
        _EREDMENY[n] = 'PIROS'
        try:
            self.jelentes_sor(n, kimenet)
            self.elo(n, ell)
            getattr(self, '_kulon_%02d' % n, lambda: None)()
        except unittest.SkipTest:
            _EREDMENY[n] = 'KIMARAD'
            raise
        _EREDMENY[n] = 'ZÖLD'

    # --- egyedi ellenőrzések ----------------------------------------------------------------------------------------------------------
    def _kulon_14(self):
        """N-F231a: az adathiba N-tétele az ág nyitott-fájljában áll, célfeladattal."""
        with open(NYITOTT_AG, encoding='utf-8') as f:
            s = f.read()
        self.assertIn('N-F231a', s)
        self.assertRegex(s, r'πρωὶ|G5459')

    def _kulon_54(self):
        """#54: az aktív „kis próféták” gomb (`color-mix(g-kis 85%, black)` háttér, `--panel` betű) mindkét témában ≥ 4,5:1."""
        sz = _szinek_keres()
        szabaly = css_szabaly(r'\.mufaj\[data-mufaj="kis"\] \.konyvgomb\.itt')
        self.assertIsNotNone(szabaly, 'nincs szabály az aktív kis-próféták gombra')
        m = re.search(r'background:\s*color-mix\(in srgb, var\(--g-kis\) (\d+)%, black\)', szabaly)
        self.assertIsNotNone(m, szabaly)
        self.assertIn('color: var(--panel)', szabaly)
        for tema in ('light', 'dark'):
            hatter = keveres(_rgb(sz['g-kis'][tema]), (0, 0, 0), int(m.group(1)) / 100)
            k = kontraszt(hatter, _rgb(sz['panel'][tema]))
            self.assertGreaterEqual(k, 4.5, '%s téma: %.2f:1' % (tema, k))

    def _kulon_55(self):
        """#55: érintőképernyőn (`pointer: coarse`) a kezelőelemek legalább 44 px magasak; a tanulmányjel átlátszóság nélkül ≥ 4,5:1."""
        with open(CSS, encoding='utf-8') as f:
            css = f.read()
        m = re.search(r'@media \(pointer: coarse\) \{(.*?)\n\}', css, re.S)
        self.assertIsNotNone(m, 'nincs pointer: coarse szabály')
        self.assertIn('min-height: 44px', m.group(1))
        for sz in ('.szintvalto a', '.ful', '.fejezetgomb', '.konyvgomb'):
            self.assertIn(sz, m.group(1))
        tj = css_szabaly(r'\n\.tan-jel')
        self.assertIsNotNone(tj, 'nincs .tan-jel szabály')
        self.assertNotIn('opacity', tj)
        self.assertIn('color: var(--muted)', tj)
        szin = _szinek_keres()
        for tema in ('light', 'dark'):
            for hatter in ('bg', 'panel'):
                k = kontraszt(_rgb(szin['muted'][tema]), _rgb(szin[hatter][tema]))
                self.assertGreaterEqual(k, 4.5, '%s téma, %s háttér: %.2f:1' % (tema, hatter, k))

    def _kulon_60(self):
        """#60: új (gyorsítótárban még nem álló) fejezet a meleg szerveren 0,8 s alatt (az „előtte” 0,8–3 s); a három lap legjobbja
        számít (a párhuzamos munkamenetek zaja ellen). A részletes határ a `teszt_sebesseg.py`-é (fejezet ≤ 300 ms, ürített tárral)."""
        if not ELO:
            self.skipTest('nincs pardes.db vagy Flask')
        c = self.lapok.kliens[None]
        c.get('/1Moz/2')                                       # bemelegítés
        idok = []
        for u in ('/Ezs/40', '/Jer/31', '/Ez/37'):
            t = time.perf_counter()
            r = c.get(u)
            idok.append(time.perf_counter() - t)
            self.assertEqual(r.status_code, 200, u)
        self.assertLess(min(idok), 0.8, 'új fejezet: %s s' % ', '.join('%.2f' % x for x in idok))
        self.assertTrue(os.path.exists(os.path.join(D, 'teszt_sebesseg.py')))


def _teszt(n):
    def t(self):
        self.tetel(n)
    t.__name__ = 'test_t%02d' % n
    t.__doc__ = 'F231 #%d (a jelentés 3. szakasza): %s' % (n, TETELEK[n][0])
    return t


for _n in TETELEK:
    setattr(TetelMerce, 'test_t%02d' % _n, _teszt(_n))


class Keszlet(unittest.TestCase):
    """A mérce maga: a jelentés 60 sorából pontosan az 58 megbízott tétel van benne, mindegyik a jelentés kimenetével."""

    def test_a_tetelek_a_jelentes_sorai(self):
        sorok = jelentes_sorok()
        self.assertEqual(sorted(sorok), list(range(1, 61)), 'a jelentés 3. szakasza nem 60 sor')
        for n in KIMARAD:
            self.assertEqual(sorok[n][0], 'K', '#%d: a kimaradó tétel kimenete' % n)
        self.assertEqual(sorted(TETELEK), sorted(set(range(1, 61)) - set(KIMARAD)))
        for n, (k, *_r) in sorted(sorok.items()):
            if n not in KIMARAD:
                self.assertRegex(k, KIMENET_RE, '#%d: negyedik kimenet a tételtáblában: %r' % (n, k))

    def test_a_kontraszt_keplet(self):
        self.assertAlmostEqual(kontraszt((0, 0, 0), (255, 255, 255)), 21.0, places=2)
        self.assertAlmostEqual(kontraszt(_rgb('#a0702a'), _rgb('#fffdf8')), 4.26, delta=0.03)   # a jelentés „előtte” értéke


if __name__ == '__main__':
    unittest.main()
