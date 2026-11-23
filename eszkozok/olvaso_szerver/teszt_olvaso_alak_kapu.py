#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_olvaso_alak_kapu.py -- az olvasó alak-kapuja (OLVASO-GYORS, 2026-11-23).

Miért kell: a `merce/` pillanatkép a mai állapotot rögzíti, hibáival együtt; az eltérése csak figyelmeztetés, ezért nem kapu. A
tételmérés példányokat mért, nem hibaosztályt: a belső alak (táblanév, aláhúzásos azonosító, nyers angol szótárcímke, ellentmondó
licencmondat, nyers dátumos gépi jelölés) a javítókörök után is a lapon maradt. Ez a teszt az olvasó minden oldaltípusát bejárja, és
minden olyan alakot megkeres, amely olvasóhoz nem kerülhet.

Mit néz (`latszo_szegmensek`): a HTML látható szövegét és a látható attribútumokat (`title`, `alt`, `aria-label`, `placeholder`), a
böngészőfül címét (`<head><title>`) is. Kimarad: `<script>`, `<style>`, `<template>`, `<noscript>`, `<svg>`, a `hidden` elemek és a
`<head>` többi része. A csukott `<details>` tartalma számít (kattintásra látszik), a lábléc is (az olvasó látja).

A minták egy helyen állnak (`MINTAK`); új minta: egy új `Minta(...)` sor. A találat kódhelye (`kodhely`): a legközelebbi `data-blokk`
ős (a blokk; a `p.forras` forrássorban a `forras_sor`, a blokkcím `jelleg`-címkéjében a `jelleg_cimkek`), blokkon kívül a legközelebbi
osztályos elem (lapváz), a sablon- vagy kódhellyel, ha a forrásban megtalálható.

A kapu (a CI nem pirosodik a mai hátraléktól): az `alak_kapu_hatralek.tsv` a ma ismert hibaosztályok listája (minta + kódhely). A
teszt akkor bukik, ha a bejárás a listán NEM szereplő (minta, kódhely) párt talál: új hibaosztály nem kerülhet be. A lista csak
szűkülhet: a DB nélküli teszt az `origin/main` változatával veti össze (egy új sor = bukás). A kijavított osztály kiírása
(`ALAK-KAPU JAVULT`) jelzi, hogy a sor törölhető (`--hatralek-frissit`, amely csak töröl, újat nem vesz fel).

Futtatás (a DB-s rész Flask-et és `pardes.db`-t kér; a repó gyökeréből):
    python eszkozok/teszt_futtat.py --fajl teszt_olvaso_alak_kapu       # a teszt
    python teszt_olvaso_alak_kapu.py --hatralek-frissit                 # a hátralék szűkítése (csak a már nem talált sorok törlése)
    python teszt_olvaso_alak_kapu.py --hatralek-alap [név=URL ...]      # az első rögzítés (csak ha még nincs a main-en); a megadott
        # élő szerverek (egy még be nem ment PR előnézete) osztályai is bekerülnek: 2026-11-23-án a #810 (8775) öt osztálya
    python teszt_olvaso_alak_kapu.py --leltar main=http://localhost:8765 pr810=http://localhost:8775
        # a leltár (`naplok/OLVASO_ALAK_KAPU_leltar.md`, generált): élő szervereken, HTTP-vel; a mintát és a kódhelyet ez a checkout adja
Környezeti változó: PARDES_DB.
"""
import collections
import os
import random
import re
import sqlite3
import subprocess
import sys
import unittest
import urllib.error
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)
DB = os.environ.get('PARDES_DB') or (REPO.replace('\\', '/') + '/pardes.db')
VAN_DB = os.path.exists(DB)
try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

HATRALEK = os.path.join(D, 'alak_kapu_hatralek.tsv')
HATRALEK_REPO_UT = 'eszkozok/olvaso_szerver/alak_kapu_hatralek.tsv'
LELTAR = os.path.join(REPO, 'naplok', 'OLVASO_ALAK_KAPU_leltar.md')


# =====================================================================================================================
# A minták: EGY hely. Új belső alak = új sor. A `szuro` a találat szövegét kapja (és a táblanév-, dataset-halmazt), True: számít.
# =====================================================================================================================
@dataclass(frozen=True)
class Minta:
    kulcs: str
    leiras: str
    regex: str
    flags: int = 0
    szuro: object = None      # (talalat, nevek) -> bool; nevek: {'tabla': set, 'dataset': set}


_AZON = r'(?<![\w/.-])[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+(?![\w-])'
_ANGOL_TW = ('Definition', 'Facts', 'Bible References', 'Translation Suggestions', 'Word Data', 'Examples from the Bible stories', 'See also')
_ANGOL_LEX = ('Derivation', 'See', 'KJV', 'LN', 'GK', 'Hebrew', 'Greek', "Strong's")

MINTAK = (
    Minta('tablanev', 'adatbázis-táblanév (pl. `token_par`, `lxx_bridge`; zárójelben aláhúzás nélkül is, pl. `(bdb)`)',
          _AZON + r'|(?<=\()[a-z][a-z0-9]*(?=\))', szuro=lambda t, n: t in n['tabla']),
    Minta('dataset_kod', 'dataset- vagy provenienciakód aláhúzással (pl. `projekt_adat`, `Karoli_Strong_parok`)',
          _AZON, szuro=lambda t, n: t in n['dataset'] and t not in n['tabla']),
    Minta('alahuzas_azonosito', 'egyéb aláhúzásos belső azonosító (pl. `tW_szocikkek`)',
          _AZON, szuro=lambda t, n: t not in n['dataset'] and t not in n['tabla']),
    Minta('proveniencia_sor', 'nyers proveniencia-mező (`scope=`, `forras=`, `ts=`)', r'\b(?:scope|forras|ts)=\S'),
    Minta('rc_link', 'nyers `rc://` hivatkozás (translationWords)', r'rc://[^\s)\]]*'),
    Minta('tw_kategoria', 'translationWords kategóriakód (pl. `(kt, kt/angel)`, `other/wrong`)',
          r'\((?:kt|names|other),[^)]*\)|(?<![\w/])(?:kt|names|other)/[a-z][\w-]*'),
    Minta('md_felkover', 'nyers Markdown félkövér (`**…**`)', r'\*\*[^*\n]+\*\*'),
    Minta('md_link', 'nyers Markdown hivatkozás (`[…](…)`)', r'\[[^\]\n]+\]\([^)\n]+\)'),
    Minta('md_cimsor', 'nyers Markdown címsor (sor eleji `#`)', r'(?m)^[ \t]*#{1,6}[ \t]+\S'),
    Minta('angol_cimke_tw', 'angol szótárcímke, translationWords (pl. `Definition:`)', r'\b(?:%s):' % '|'.join(map(re.escape, _ANGOL_TW))),
    Minta('angol_cimke_lexikon', 'angol szótárcímke, lexikon (pl. `Derivation:`, `See:`, `KJV:`)',
          r'(?<![\w-])(?:%s):' % '|'.join(map(re.escape, _ANGOL_LEX))),
    Minta('hosszu_szamazonosito', 'hosszú számazonosító (12+ jegy, pl. a 15 jegyű UBS-azonosító)', r'(?<!\d)\d{12,}(?!\d)'),
    Minta('kalap_index', 'nyers `^` index', r'\^'),
    Minta('licenc_ellentmondas', 'ellentmondó licencmondat (`CC BY` és „minden jog fenntartva” egy mondatban)',
          r'CC[ -]BY(?:(?!\.\s|[!?·\n]).)*?minden jog fenntartva|minden jog fenntartva(?:(?!\.\s|[!?·\n]).)*?CC[ -]BY', re.I),
    Minta('gepi_datum', 'nyers dátumos gépi jelölés (pl. „Lefordítva · gépi fordítás, 2026.10.01”)',
          r'(?:Lefordítva|gépi fordítás)[^\n]{0,40}?\d{4}[.-]\d{2}[.-]\d{2}'),
    Minta('fajlnev', 'belső fájlnév (`.db`, `.tsv`, `.py`, `.md`, `.json`, `.toml`)', r'(?<![\w/])[\w-]+\.(?:db|tsv|py|md|json|toml)\b'),
)
MINTA_KULCS = {m.kulcs: m for m in MINTAK}
_REGEX = {m.kulcs: re.compile(m.regex, m.flags) for m in MINTAK}
LATHATO_ATTR = ('title', 'alt', 'aria-label', 'placeholder')


# =====================================================================================================================
# A bejárt lapok: a merce/ 18 lapja, minden oldaltípus, rögzített magú véletlen minta (vers- és szólapok)
# =====================================================================================================================
from teszt_olvasoi_merce import MINTA as MERCE_MINTA  # noqa: E402  (a 18 mintalap; a merce/ fájljaihoz e menet nem nyúl)

MAG = 20261123
VELETLEN_VERS = 12
VELETLEN_SZO = 12
FUL_VERSEK = ('/1Moz/1/1', '/Jan/1/1')
FULEK = ('szo', 'info', 'vers', 'kh', 'temak', 'motivum')
EGYEB = ('/', '/1Moz', '/Mt', '/Zsolt', '/szo/H9999',                                   # kezdőlap, könyvlap, 404
         '/szo/H0216?vers=1Moz/1/3', '/szo/G3056?vers=Jan/1/1',                         # a szó-lap vers-kontextussal (szo.ebben)
         '/r/szo/H0216?ig=1Moz/1/3', '/r/szo/G3056?ig=Jan/1/1', '/r/szo/H1242',         # a szókártya (töredék)
         '/r/vers/1Moz/1/1', '/r/vers/Jan/1/1')
KERESO = ('/kereses', '/kereses?q=vil%C3%A1goss%C3%A1g', '/kereses?strong=H0216', '/kereses?q=%D7%90%D7%95%D7%A8',
          '/kereses?frazis=az+Isten+ig%C3%A9je', '/kereses?q=xyzqq')


def veletlen_minta(db=DB):
    """(versek, szavak): rögzített magú véletlen minta a `vers` és a `strong_szotar` táblából (a kanonikus sorrendből)."""
    con = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
    try:
        import lekerdezesek
        versek = [(k, f, v) for k, f, v in con.execute('SELECT konyv, fejezet, vers FROM vers ORDER BY sorrend')]
        szavak = [s for (s,) in con.execute('SELECT DISTINCT strong FROM strong_szotar WHERE strong IS NOT NULL ORDER BY strong')]
        tanulmany = [t for (t,) in con.execute('SELECT tanulmany_id FROM tanulmany ORDER BY tanulmany_id LIMIT 2')] if _van_tabla(con, 'tanulmany') else []
    finally:
        con.close()
    r = random.Random(MAG)
    vk = ['/%s/%d/%d' % (lekerdezesek.konyv_slug(k), f, v) for k, f, v in r.sample(versek, VELETLEN_VERS)]
    sk = ['/szo/' + s for s in r.sample(szavak, VELETLEN_SZO)]
    return vk, sk, ['/tanulmany/' + t for t in tanulmany]


def _van_tabla(con, nev):
    return con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (nev,)).fetchone() is not None


def bejart_lapok(db=DB):
    """A bejárt URL-ek, sorrendben, ismétlés nélkül."""
    vk, sk, tan = veletlen_minta(db)
    fulek = ['%s?ful=%s' % (v, f) for v in FUL_VERSEK for f in FULEK] + ['%s?reteg=il' % v for v in FUL_VERSEK] + ['/1Moz/1?reteg=il']
    ki = []
    for u in list(MERCE_MINTA) + fulek + list(EGYEB) + tan + list(KERESO) + vk + sk:
        if u not in ki:
            ki.append(u)
    return ki


def oldaltipus(url):
    ut = url.split('?')[0]
    r = [x for x in ut.split('/') if x]
    if not r:
        return 'egyéb'
    if r[0] == 'r':
        return 'szókártya' if r[1:2] == ['szo'] else 'vers-töredék'
    if r[0] == 'szo':
        return 'szó'
    if r[0] == 'kereses':
        return 'kereső'
    if r[0] == 'tanulmany':
        return 'egyéb'
    if len(r) == 3:
        return 'vers'
    if len(r) == 2:
        return 'fejezet'
    return 'egyéb'


def nevek(db=DB):
    """{'tabla': az adatbázis táblái, 'dataset': a `tabla_licenc` dataset-kódjai (a `+` mentén bontva)}."""
    if not os.path.exists(db):
        return {'tabla': set(), 'dataset': set()}
    con = sqlite3.connect('file:%s?mode=ro' % db, uri=True)
    try:
        tabla = {n for (n,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        ds = set()
        if 'tabla_licenc' in tabla:
            for (d,) in con.execute('SELECT DISTINCT licenc_dataset FROM tabla_licenc'):
                ds.update(x.strip() for x in (d or '').split('+') if x.strip())
    finally:
        con.close()
    return {'tabla': tabla, 'dataset': ds}


# =====================================================================================================================
# A látható szöveg szegmensei, a kódhely-jelöléssel
# =====================================================================================================================
_VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())
_BLOKK = frozenset('address article aside blockquote body dd details div dl dt fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 '
                   'header hr li main nav ol p pre section summary table tbody thead tfoot tr td th ul br'.split())
_KIHAGY = frozenset('script style template noscript svg'.split())
_KEZELO = frozenset('a button label option'.split())


@dataclass
class Szegmens:
    szoveg: str
    hely: str          # 'szöveg' | 'attr:title' | ... | 'fül-cím'
    kodhely: str       # stabil kulcs: 'blokk:<id>' | 'forrássor:<id>' | 'jelleg-címke:<id>' | 'lapváz:<tag.osztály>'


class _Kinyer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.verem = []      # (tag, kihagy, blokk_id, osztalyok)
        self.szeg = []
        self.sor = ''
        self.fej = False
        self.cim = None      # a <head><title> gyűjtője

    def _kihagy(self):
        return any(e[1] for e in self.verem)

    def _kodhely(self):
        blokk = None
        for i in range(len(self.verem) - 1, -1, -1):
            if self.verem[i][2]:
                blokk = (i, self.verem[i][2])
                break
        if blokk:
            i, bid = blokk
            belso = self.verem[i + 1:]
            if any('forras' in e[3] for e in belso):
                return 'forrássor:' + bid
            if any('jelleg' in e[3] for e in belso):
                return 'jelleg-címke:' + bid
            return 'blokk:' + bid
        for e in reversed(self.verem):
            if e[3]:
                return 'lapváz:%s.%s' % (e[0], e[3][0])
        return 'lapváz:' + (self.verem[-1][0] if self.verem else '?')

    def _flush(self):
        if self.sor.strip() and not self._kihagy():
            self.szeg.append(Szegmens(_normal(self.sor), 'szöveg', self._kodhely()))
        self.sor = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'head':
            self.fej = True
        if tag == 'title' and self.fej:
            self.cim = ''
            return
        if tag in _BLOKK and not self._kihagy():
            self._flush()
        if tag in _VOID:
            if not self._kihagy() and not self.fej:
                self._attr(a, tag)
            return
        kihagy = tag in _KIHAGY or 'hidden' in a or self.fej
        if kihagy and not self._kihagy():
            self._flush()        # a rejtett elem előtti látható szöveg nem veszhet el
        osztaly = tuple((a.get('class') or '').split())
        if tag in _KEZELO:
            self.sor += ' '      # a szomszédos kezelőelemek (pl. a fejezetrács számai) ne tapadjanak össze
        self.verem.append((tag, kihagy, a.get('data-blokk'), osztaly))
        if not self._kihagy():
            self._attr(a, tag)

    def _attr(self, a, tag):
        for n in LATHATO_ATTR:
            if a.get(n) and a[n].strip():
                self.szeg.append(Szegmens(_normal(a[n]), 'attr:' + n, self._kodhely()))

    def handle_endtag(self, tag):
        if tag == 'title' and self.cim is not None:
            self.szeg.append(Szegmens(_normal(self.cim), 'fül-cím', 'lapváz:title'))
            self.cim = None
            return
        if tag == 'head':
            self.fej = False
        if tag in _VOID:
            return
        for i in range(len(self.verem) - 1, -1, -1):
            if self.verem[i][0] == tag:
                if tag in _BLOKK:
                    self._flush()
                elif tag in _KEZELO and not self._kihagy():
                    self.sor += ' '
                del self.verem[i:]
                return

    def handle_data(self, data):
        if self.cim is not None:
            self.cim += data
            return
        if not self._kihagy():
            self.sor += data

    def vege(self):
        self._flush()
        return self.szeg


def _normal(s):
    """A sorhatár (`\\n`) megmarad (a sor eleji `#` mintához), a többi üres tér egy szóköz."""
    sorok = [re.sub(r'[ \t\r\f\v ]+', ' ', x).strip() for x in s.split('\n')]
    return '\n'.join(x for x in sorok if x)


def latszo_szegmensek(html):
    k = _Kinyer()
    k.feed(html)
    k.close()
    return k.vege()


@dataclass(frozen=True)
class Talalat:
    minta: str
    kodhely: str
    url: str
    hely: str
    szoveg: str        # a találat szövege
    kornyezet: str     # rövid környezet a leltárhoz


def talalatok(url, html, nv):
    ki = []
    for sz in latszo_szegmensek(html):
        for m in MINTAK:
            for t in _REGEX[m.kulcs].finditer(sz.szoveg):
                if m.szuro and not m.szuro(t.group(0), nv):
                    continue
                a, b = t.start(), t.end()
                korny = sz.szoveg[max(0, a - 40):b + 40].replace('\n', ' ⏎ ')
                ki.append(Talalat(m.kulcs, sz.kodhely, url, sz.hely, t.group(0), korny))
    return ki


# =====================================================================================================================
# Kódhely: a blokk render-függvénye (`blokkok.REGISZTER`), a lapváz osztályának első előfordulása a sablonokban/kódban
# =====================================================================================================================
def kodhely_leiras(kodhely):
    """A stabil kódhely-kulcs olvasható forráshelye, ha megállapítható (ennek a checkoutnak a kódjából)."""
    fajta, _, ertek = kodhely.partition(':')
    try:
        import blokkok
    except Exception:                                                   # Flask/markupsafe nélkül csak a kulcs
        blokkok = None
    if blokkok and fajta in ('blokk', 'forrássor', 'jelleg-címke'):
        if fajta == 'forrássor':
            return _fv(blokkok.forras_sor)
        if fajta == 'jelleg-címke':
            return _fv(blokkok.jelleg_cimkek)
        b = blokkok.BLOKK_ID.get(ertek)
        return _fv(b.render) if b else 'blokkok.py (a blokk ebben a checkoutban nincs a regiszterben)'
    if fajta == 'lapváz':
        osztaly = ertek.partition('.')[2]
        if ertek == 'title':
            return 'sablonok/*.html `{% block cim %}`'
        if osztaly:
            return _keres_osztaly(osztaly) or '(nem található)'
    return ''


def _fv(f):
    import inspect
    try:
        return '%s:%d `%s`' % (os.path.basename(inspect.getsourcefile(f)), f.__code__.co_firstlineno, f.__name__)
    except Exception:
        return getattr(f, '__name__', str(f))


def _keres_osztaly(osztaly):
    minta = re.compile(r'class="[^"]*(?<![\w-])%s(?![\w-])' % re.escape(osztaly))
    fajlok = [os.path.join('sablonok', f) for f in sorted(os.listdir(os.path.join(D, 'sablonok')))] + \
             [f for f in ('oldalak.py', 'blokkok.py', 'tanulmany_oldal.py', 'kereses.py', 'alkalmazas.py')]
    for f in fajlok:
        with open(os.path.join(D, f), encoding='utf-8') as h:
            for i, sor in enumerate(h, 1):
                if minta.search(sor):
                    return '%s:%d' % (f.replace('\\', '/'), i)
    return None


# =====================================================================================================================
# A bejárás és a hátralék
# =====================================================================================================================
def bejaras(lekero, urlek, nv):
    """(találatok, {url: státusz}). `lekero(url) -> (státusz, content-type, html)`."""
    ossz, statusz = [], {}
    for u in urlek:
        st, ct, html = lekero(u)
        statusz[u] = st
        if 'html' in (ct or ''):
            ossz.extend(talalatok(u, html, nv))
    return ossz, statusz


def osztalyok(talalat_lista):
    return sorted({(t.minta, t.kodhely) for t in talalat_lista})


def hatralek_olvas(szoveg=None):
    if szoveg is None:
        if not os.path.exists(HATRALEK):
            return set()
        with open(HATRALEK, encoding='utf-8', newline='') as f:
            szoveg = f.read()
    ki = set()
    for sor in szoveg.replace('\r\n', '\n').split('\n'):
        if not sor.strip() or sor.startswith('#') or sor.startswith('minta\t'):
            continue
        r = sor.split('\t')
        ki.add((r[0], r[1]))
    return ki


def hatralek_ir(parok):
    sorok = ['# GENERÁLT: teszt_olvaso_alak_kapu.py --hatralek-frissit (csak szűkülhet; új sor = új hibaosztály = bukás)',
             '# A ma ismert hibaosztályok: (minta, kódhely). A leltár: naplok/OLVASO_ALAK_KAPU_leltar.md.',
             'minta\tkodhely']
    sorok += ['\t'.join(p) for p in sorted(parok)]
    with open(HATRALEK, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok) + '\n')


def hatralek_main():
    """Az `origin/main` hátraléka, vagy None (nincs git, nincs origin/main, vagy a fájl még nincs a main-en)."""
    try:
        p = subprocess.run(['git', 'show', 'origin/main:' + HATRALEK_REPO_UT], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode != 0:
        return None
    return hatralek_olvas(p.stdout.decode('utf-8'))


def app_lekero():
    import alkalmazas
    c = alkalmazas.letrehoz(db_ut=DB, kiadas='belso').test_client()

    def lek(u):
        r = c.get(u)
        return r.status_code, r.headers.get('Content-Type', ''), r.get_data(as_text=True)
    return lek


def http_lekero(alap):
    def lek(u):
        try:
            with urllib.request.urlopen(alap.rstrip('/') + u, timeout=120) as r:
                return r.status, r.headers.get('Content-Type', ''), r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as ex:
            return ex.code, ex.headers.get('Content-Type', ''), ex.read().decode('utf-8', 'replace')
    return lek


# =====================================================================================================================
class TestMintak(unittest.TestCase):
    """A minták és a kinyerő (DB nélkül)."""
    NV = {'tabla': {'token_par', 'lxx_bridge', 'bdb'}, 'dataset': {'projekt_adat', 'Karoli_Strong_parok', 'lxx_bridge'}}

    def _k(self, html):
        return sorted((t.minta, t.szoveg) for t in talalatok('/x', html, self.NV))

    def test_a_kert_peldak_mind_buknak(self):
        h = ('<section data-blokk="szo.x"><p>Karoli_Strong_parok (token_par) · projekt_adat · lxx_bridge</p>'
             '<p>Definition: a word (kt, kt/angel) rc://*/tw/dict/bible/kt/angel</p><p>**félkövér** és [link](rc://x)</p>'
             '<p>003076001001000 és H1^2</p><p class="forras">TBESH (x): CC BY 4.0; minden jog fenntartva</p>'
             '<p>Lefordítva · gépi fordítás, 2026.10.01</p><pre>## Cím</pre><p>(bdb)</p></section>')
        k = {m for m, _ in self._k(h)}
        for kell in ('dataset_kod', 'tablanev', 'angol_cimke_tw', 'tw_kategoria', 'rc_link', 'md_felkover', 'md_link',
                     'hosszu_szamazonosito', 'kalap_index', 'licenc_ellentmondas', 'gepi_datum', 'md_cimsor'):
            self.assertIn(kell, k)
        self.assertIn(('tablanev', 'token_par'), self._k(h))
        self.assertIn(('tablanev', 'lxx_bridge'), self._k(h))           # a tábla elsőbb a dataset-kódnál
        self.assertNotIn(('dataset_kod', 'lxx_bridge'), self._k(h))

    def test_olvasoi_szoveg_nem_bukik(self):
        h = ('<p>CC BY 4.0. Minden jog fenntartva a fordításon.</p><table><tr><th>#</th><th>Szó</th></tr></table>'
             '<p>1Móz 1:1 · H0216 · Isten: az Úr · 2026. november 23.</p><p>Licenc: CC BY 4.0 (TSK)</p>'
             '<div>' + ''.join('<a href="#">%d</a>' % i for i in range(1, 51)) + '</div>'     # a fejezetrács: nem 12+ jegyű szám
             '<p>A: CC BY 4.0 · B: minden jog fenntartva</p>'                                  # két külön forrás, két külön licenc
             '<p>humans and (other) objects</p>')
        self.assertEqual(self._k(h), [])

    def test_rejtett_es_script_nem_szamit_attr_igen(self):
        h = ('<head><title>token_par — Biblialex</title><script>var a_b = 1;</script></head><body><p hidden>token_par</p>'
             '<span title="projekt_adat">x</span><img alt="lxx_bridge"><template>token_par</template><p>ok</p></body>')
        k = sorted((t.minta, t.szoveg, t.hely) for t in talalatok('/x', h, self.NV))
        self.assertEqual(k, [('dataset_kod', 'projekt_adat', 'attr:title'), ('tablanev', 'lxx_bridge', 'attr:alt'),
                             ('tablanev', 'token_par', 'fül-cím')])

    def test_kodhely(self):
        h = ('<header class="fejlec"><a title="a_b">x</a></header><section data-blokk="szo.tw_h"><h3>C <span class="jelleg x" '
             'title="token_par">j</span></h3><div>projekt_adat</div><p class="forras">Forrás: Karoli_Strong_parok</p></section>')
        k = sorted((t.kodhely, t.szoveg) for t in talalatok('/x', h, self.NV))
        self.assertEqual(k, [('blokk:szo.tw_h', 'projekt_adat'), ('forrássor:szo.tw_h', 'Karoli_Strong_parok'),
                             ('jelleg-címke:szo.tw_h', 'token_par'), ('lapváz:header.fejlec', 'a_b')])

    def test_a_rejtett_elem_elotti_szoveg_megmarad(self):
        k = sorted((t.minta, t.szoveg) for t in talalatok('/x', '<p>projekt_adat <span hidden>token_par</span> utana</p>', self.NV))
        self.assertEqual(k, [('dataset_kod', 'projekt_adat')])

    def test_oldaltipus(self):
        self.assertEqual([oldaltipus(u) for u in ('/', '/1Moz', '/1Moz/1', '/1Moz/1/1?ful=kh', '/szo/H1', '/r/szo/H1', '/r/vers/a/1/1',
                                                  '/kereses?q=x', '/tanulmany/x')],
                         ['egyéb', 'egyéb', 'fejezet', 'vers', 'szó', 'szókártya', 'vers-töredék', 'kereső', 'egyéb'])

    def test_a_mintak_kulcsa_egyedi(self):
        self.assertEqual(len(MINTA_KULCS), len(MINTAK))

    def test_a_hatralek_csak_szukulhet(self):
        """Az `origin/main` hátralékához képest új sor nem lehet (új hibaosztály); a main-en még nem létező fájlnál nincs mit vetni."""
        main = hatralek_main()
        if main is None:
            self.skipTest('a hátralék még nincs az origin/main-en (vagy nincs git)')
        uj = hatralek_olvas() - main
        self.assertFalse(uj, 'a hátralék új sort kapott az origin/main-hez képest (új hibaosztály nem vehető fel): %s' % sorted(uj))

    def test_a_hatralek_mintai_ismertek(self):
        for m, _ in hatralek_olvas():
            self.assertIn(m, MINTA_KULCS)


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestAlakKapu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.urlek = bejart_lapok()
        cls.tal, cls.statusz = bejaras(app_lekero(), cls.urlek, nevek())

    def test_minden_oldaltipus_bejarva(self):
        tipusok = {oldaltipus(u) for u in self.urlek}
        self.assertTrue({'fejezet', 'vers', 'szó', 'kereső', 'egyéb', 'szókártya'} <= tipusok, tipusok)
        rossz = {u: s for u, s in self.statusz.items() if s >= 500}
        self.assertFalse(rossz, 'szerverhiba a bejárt lapokon: %s' % rossz)

    def test_nincs_uj_hibaosztaly(self):
        talalt = set(osztalyok(self.tal))
        ismert = hatralek_olvas()
        db = collections.Counter((t.minta, t.kodhely) for t in self.tal)
        for p in sorted(ismert - talalt):
            print('ALAK-KAPU JAVULT: %s · %s nem fordul elő (a hátralékból törölhető: --hatralek-frissit)' % p)
        print('ALAK-KAPU: %d lap, %d találat, %d hibaosztály (ebből a hátralékban: %d)'
              % (len(self.urlek), len(self.tal), len(talalt), len(talalt & ismert)))
        uj = sorted(talalt - ismert)
        if uj:
            peldak = []
            for p in uj:
                t = next(x for x in self.tal if (x.minta, x.kodhely) == p)
                peldak.append('%s · %s (%d db), pl. %s: „%s”' % (p[0], p[1], db[p], t.url, t.kornyezet))
            self.fail('új belső alak az olvasóban (nincs a hátralékban, alak_kapu_hatralek.tsv):\n  ' + '\n  '.join(peldak))


# =====================================================================================================================
# A leltár (generált): naplok/OLVASO_ALAK_KAPU_leltar.md
# =====================================================================================================================
def _cella(s, n=110):
    s = s if len(s) <= n else s[:n - 1] + '…'
    return s.replace('|', '\\|').replace('`', "'")


def leltar(szerverek):
    """szerverek: [(név, alap-URL)]. Minden szerveren ugyanaz a lapkészlet; a táblában szerverenként a darabszám."""
    urlek = bejart_lapok()
    nv = nevek()
    eredm = {}
    allas = {}
    for nev, alap in szerverek:
        _, _, h = http_lekero(alap)('/')
        m = re.search(r'ág: <b>([^<]*)</b> · commit: <code>([0-9a-f]+)', h)
        allas[nev] = '%s @ `%s`' % (m.group(1), m.group(2)) if m else 'ismeretlen ág és commit'
        print('bejárás: %s (%s), %d lap' % (nev, alap, len(urlek)), flush=True)
        eredm[nev] = bejaras(http_lekero(alap), urlek, nv)
    nevsor = [n for n, _ in szerverek]
    tipus_db = collections.Counter(oldaltipus(u) for u in urlek)
    ki = ['<!-- GENERÁLT: eszkozok/olvaso_szerver/teszt_olvaso_alak_kapu.py --leltar; kézzel ne szerkeszd -->',
          '# Az olvasó alak-kapujának leltára',
          '',
          'A hátralék és a bekötési leltár: minden belső alak, amely ma az olvasó lapjain látszik, mintánként és kódhelyenként. '
          'A darabszám a találatok (előfordulások) száma a bejárt lapokon; a kapu (`alak_kapu_hatralek.tsv`) a (minta, kódhely) '
          'osztályokat tartja, és új osztályra bukik.',
          '',
          '- Szerverek: ' + ', '.join('**%s** = `%s` (%s)' % (n, a, allas[n]) for n, a in szerverek),
          '- Bejárt lapok: %d (%s); a `merce/` 18 lapja, a vers fülei és rétege, szókártya, kereső, egyéb lapok, és rögzített magú '
          '(%d) véletlen minta: %d vers, %d szó.' % (len(urlek), ', '.join('%s %d' % kv for kv in sorted(tipus_db.items())), MAG,
                                                     VELETLEN_VERS, VELETLEN_SZO),
          '- A kódhely ennek a checkoutnak a kódjából áll (a sorszám a `main`-é); a blokk-azonosító (`data-blokk`) mindkét ágon azonos.',
          '- Nem 200-as lapok: ' + ('; '.join('%s: %s' % (n, ', '.join('%s=%s' % (u, s) for u, s in eredm[n][1].items() if s != 200) or 'nincs')
                                         for n in nevsor)),
          '']
    ki += ['## Összesítés', '', '| minta | ' + ' | '.join('%s (db)' % n for n in nevsor) + ' | ' +
           ' | '.join('%s (osztály)' % n for n in nevsor) + ' |', '|---|' + '---:|' * (2 * len(nevsor))]
    for m in MINTAK:
        dbk = [sum(1 for t in eredm[n][0] if t.minta == m.kulcs) for n in nevsor]
        osz = [len({t.kodhely for t in eredm[n][0] if t.minta == m.kulcs}) for n in nevsor]
        ki.append('| `%s` — %s | %s | %s |' % (m.kulcs, m.leiras, ' | '.join(map(str, dbk)), ' | '.join(map(str, osz))))
    ossz = [len(eredm[n][0]) for n in nevsor]
    ki.append('| **összesen** | %s | %s |' % (' | '.join('**%d**' % x for x in ossz),
                                             ' | '.join('**%d**' % len(osztalyok(eredm[n][0])) for n in nevsor)))
    ki.append('')
    if len(nevsor) > 1:
        ki += ['## Eltérés a szerverek között (hibaosztály: minta · kódhely)', '']
        for n in nevsor:
            tobbi = set().union(*(set(osztalyok(eredm[x][0])) for x in nevsor if x != n))
            csak = sorted(set(osztalyok(eredm[n][0])) - tobbi)
            ki.append('- csak **%s**: %s' % (n, ', '.join('`%s` · `%s`' % p for p in csak) if csak else 'nincs'))
        ki.append('')
    for m in MINTAK:
        parok = sorted({t.kodhely for n in nevsor for t in eredm[n][0] if t.minta == m.kulcs})
        if not parok:
            continue
        ki += ['## `%s` — %s' % (m.kulcs, m.leiras), '',
               '| kódhely | forráshely | ' + ' | '.join(nevsor) + ' | oldaltípus | példa URL | példa |',
               '|---|---|' + '---:|' * len(nevsor) + '---|---|---|']
        for kh in parok:
            mind = [t for n in nevsor for t in eredm[n][0] if t.minta == m.kulcs and t.kodhely == kh]
            dbk = [sum(1 for t in eredm[n][0] if t.minta == m.kulcs and t.kodhely == kh) for n in nevsor]
            tip = sorted({oldaltipus(t.url) for t in mind})
            urlek_p = []
            for t in mind:
                if t.url not in urlek_p:
                    urlek_p.append(t.url)
            hely = sorted({t.hely for t in mind})
            ki.append('| `%s`%s | %s | %s | %s | %s | %s |' % (
                kh, (' (%s)' % ', '.join(hely)) if hely != ['szöveg'] else '',_cella(kodhely_leiras(kh)), ' | '.join(map(str, dbk)), ', '.join(tip),
                ' '.join('`%s`' % u for u in urlek_p[:2]), _cella(mind[0].kornyezet)))
        ki.append('')
    with open(LELTAR, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki))
    print('leltár: %s; %s' % (os.path.relpath(LELTAR, REPO), ', '.join('%s: %d találat, %d osztály' % (n, len(eredm[n][0]),
                                                                                                    len(osztalyok(eredm[n][0]))) for n in nevsor)))
    return eredm


def hatralek_parancs(alap, szerverek=()):
    """`alap`: az első rögzítés (ez a checkout, és a megadott élő szerverek osztályainak uniója: egy nyitott PR, amely a main-re még
    bemegy, ne bukjon a saját meglévő osztályain); különben szűkítés (csak törlés)."""
    if not (VAN_DB and VAN_FLASK):
        print('HIBA: pardes.db (PARDES_DB) és Flask kell.', file=sys.stderr)
        return 2
    urlek, nv = bejart_lapok(), nevek()
    tal, _ = bejaras(app_lekero(), urlek, nv)
    talalt = set(osztalyok(tal))
    if alap:
        if hatralek_main() is not None:
            print('HIBA: a hátralék már a main-en van; csak szűkíthető (--hatralek-frissit).', file=sys.stderr)
            return 1
        for nev, url in szerverek:
            tobb = set(osztalyok(bejaras(http_lekero(url), urlek, nv)[0])) - talalt
            print('hátralék: %s (%s): +%d osztály: %s' % (nev, url, len(tobb), sorted(tobb)))
            talalt |= tobb
        hatralek_ir(talalt)
        print('hátralék: %d osztály rögzítve' % len(talalt))
        return 0
    regi = hatralek_olvas()
    uj = regi & talalt
    hatralek_ir(uj)
    print('hátralék: %d -> %d osztály (törölve: %s); új osztály nem került be (%d)' % (len(regi), len(uj), sorted(regi - uj), len(talalt - regi)))
    return 0


if __name__ == '__main__':
    if '--leltar' in sys.argv:
        sz = [a.split('=', 1) for a in sys.argv[sys.argv.index('--leltar') + 1:] if '=' in a]
        leltar(sz)
        sys.exit(0)
    if '--hatralek-frissit' in sys.argv or '--hatralek-alap' in sys.argv:
        sys.exit(hatralek_parancs('--hatralek-alap' in sys.argv, [a.split('=', 1) for a in sys.argv[1:] if '=' in a]))
    unittest.main()
