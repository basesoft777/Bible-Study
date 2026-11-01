#!/usr/bin/env python
"""A BDB héber kifejezéseinek sorrend- és geres-javítása: a szabály és a Biblia-próba (N-F131y, DT-F131z).

A mérés: `naplok/BDB_HEBER_SORREND_meres.md` (a szabály és a próba onnan, változatlanul). A hiba a `DictBDB.json`-ban
van: a készítője minden `<heb>` futam szóköz szerinti tokenjeit megfordította, egy régebbi, a geresnél darabolt, vizuális
darabsorrendű digitalizálás (`BDB.lexicon`) fölött.

Szabály (R_hib): geres nélküli kifejezésnél a tokenek megfordítása (R0); geresnél R0, majd a `BDB.lexicon` `<bdbheb>`
darabhatárai szerint a darabok megfordítása (R_lex), ha a lexikon szerkezete átvihető, különben a csak szövegből daraboló
R_str. A lexikonból CSAK a darabhatár jön, szöveg nem (DT225); a javított alak betűi a JSON-éi.

Biblia-próba (TAHOT): a jelölt és a JSON-alak mássalhangzó-vázának mintája (a teljes szavak egymás után, a rövidítés a betűi
+ legfeljebb 8 betűnyi rés, az ellipszis legfeljebb 60 betűnyi rés) egy versben. Ítélet: `helyes` (a javított alak
előfordul, a JSON-alak nem), `rontott` (fordítva), `eldonthetetlen` (mindkettő / egyik sem / kevés anyag).

Döntés (DT-F131z, felhasználó, 2026-10-30/11-01: „Mehet”): gépi javítás (`javitva`) csak a Biblia által igazolt, tiszta
(írásjel és sziglum nélküli) tételeken; ahol a Biblia a JSON-alakot igazolja: `valodi_sorrend`; minden más változó tétel
`jelolt_marad`.
"""
import bisect
import collections
import html
import json
import re
import sqlite3
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

G = '׳'            # geres
MAKKEF = '־'
RAFE = 'ֿ'         # a forrás makkef-pótlója (két szó egybeírva)
ELLIPSZIS = '֗֗֗'
VEGSO = str.maketrans('ךםןףץ', 'כמנפצ')


def ws(s):
    return re.sub(r'\s+', ' ', s).strip()


def vaz(s):
    """Mássalhangzó-váz: NFD, csak betű, végső alak → alap, פ = מ (a JSON pe/mem hibája, SEMA 2.31)."""
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if 'א' <= c <= 'ת').translate(VEGSO)
    return s.replace('פ', 'מ')


def kulcs(s):
    return tuple(sorted(vaz(t) for t in s.replace(G, ' ').replace(MAKKEF, ' ').split() if vaz(t)))


# ---------------------------------------------------------------- szabályok

def r0(js):
    return ' '.join(reversed(ws(js).split(' ')))


EGYSEG_RE = re.compile(r'%s|\s+|[^%s\s]+' % (G, G))


def _egysegek(szoveg):
    return [('G' if m.group(0) == G else 'S' if m.group(0).isspace() else 'W', m.group(0))
            for m in EGYSEG_RE.finditer(szoveg)]


def _tomor(egys):
    out = []
    for e in egys:
        if e[0] == 'S' and (not out or out[-1][0] == 'S'):
            continue
        out.append(e)
    while out and out[-1][0] == 'S':
        out.pop()
    return out


def r_lex(js, darabok):
    """R0, majd a lexikon darabhatárai szerint a darabok megfordítása; None, ha a szerkezet nem vihető át."""
    lex = []
    for k, d in enumerate(darabok):
        lex += [(t, s, k) for t, s in _egysegek(d)]
    lex = _tomor(lex)
    sajat = _tomor(_egysegek(r0(js)))
    if [e[0] for e in lex] != [e[0] for e in sajat]:
        return None
    csop = collections.OrderedDict()
    for (_t, _s, k), (_t2, s2) in zip(lex, sajat):
        csop.setdefault(k, []).append(s2)
    return ws(''.join(''.join(v) for v in reversed(list(csop.values()))))


DARAB_RE = re.compile(r'%s|\s+|[^%s\s]+(?:\s+[^%s\s]+)*' % (G, G, G))


def r_str(js):
    return ws(''.join(reversed(DARAB_RE.findall(r0(js)))))


def r_hib(js, darabok):
    if G not in js:
        return r0(js)
    rl = r_lex(js, darabok) if darabok is not None else None
    return rl if rl is not None else r_str(js)


def tiszta(js):
    """Írásjel (`,;.:`) és szám / latin betű (sziglum) nélküli kifejezés."""
    return not re.search(r'[,;.:0-9A-Za-z]', js)


# ---------------------------------------------------------------- héber Biblia

class Biblia:
    """A TAHOT vázfolyama versenként; `van(alak)` → az első találat verse, None (nincs), vagy False (nem próbálható)."""

    def __init__(self, tahot_ut):
        versek = collections.OrderedDict()
        with open(tahot_ut, encoding='utf-8') as f:
            next(f)
            for ln in f:
                m = ln.rstrip('\n').split('\t')
                if len(m) > 2:
                    versek.setdefault(m[0], []).append(vaz(m[2]))
        self.kulcsok, self.kezdet, reszek, p = [], [], [], 1
        for k, v in versek.items():
            self.kulcsok.append(k)
            self.kezdet.append(p)
            s = ''.join(v)
            reszek.append(s)
            p += len(s) + 1
        self.f = '|' + '|'.join(reszek) + '|'
        self.cache = {}

    @staticmethod
    def minta(alak):
        reszek, teljes, rov = [], 0, 0
        for t in ws(alak).replace(MAKKEF, ' ').split(' '):
            if ELLIPSZIS in t and not vaz(t):
                reszek.append('[^|]{0,60}')
                continue
            v = vaz(t)
            if not v:
                continue
            if G in t:
                reszek.append(re.escape(v) + '[^|]{0,8}')
                rov += 1
            else:
                reszek.append(re.escape(v))
                teljes += 1
        if teljes < 1 or teljes + rov < 2:
            return None, None
        return re.compile(''.join(reszek)), max((vaz(t) for t in alak.split() if G not in t), key=len)

    def van(self, alak):
        if alak in self.cache:
            return self.cache[alak]
        rx, lit = self.minta(alak)
        if rx is None:
            self.cache[alak] = False
            return False
        talalt, i = None, self.f.find(lit)
        while i >= 0 and talalt is None:
            a = self.f.rfind('|', 0, i)
            b = self.f.find('|', i)
            if rx.search(self.f, a, b + 1):
                talalt = self.kulcsok[bisect.bisect_right(self.kezdet, a + 1) - 1]
            i = self.f.find(lit, b)
        self.cache[alak] = talalt
        return talalt


def itelet(bib, js, jelolt):
    """(ítélet, a JSON-alak verse, a jelölt verse)."""
    a, b = bib.van(js), bib.van(jelolt)
    if a is False or b is False:
        return 'eldonthetetlen', None, None
    if b and not a:
        return 'helyes', None, b
    if a and not b:
        return 'rontott', a, None
    return 'eldonthetetlen', a, b


# ---------------------------------------------------------------- bemenet

def json_tetelek(json_ut):
    """JSON-kulcs → a <heb><ref0> kifejezések látható szövege, a forrás sorrendjében."""
    with open(json_ut, encoding='utf-8') as f:
        d = json.load(f)
    out = collections.OrderedDict()
    for it in d:
        out[it['top']] = [html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
                          for m in re.finditer(r'<heb><ref0[^>]*>(.*?)</ref0>', it['def'], re.S)]
    return out


def lexikon_csoportok(lex_ut):
    con = sqlite3.connect('file:%s?mode=ro' % lex_ut.replace('\\', '/'), uri=True)
    lex = {}
    for t, df in con.execute("select Topic, Definition from Lexicon where Topic like 'BDB%'"):
        cs = []
        for m in re.finditer(r'(?:<bdbheb>.*?</bdbheb>\s*)+', df, re.S):
            cs.append([html.unescape(sm.group(1)) if sm.group(1) is not None else ' '
                       for sm in re.finditer(r'<bdbheb>(.*?)</bdbheb>|(\s+)', m.group(0).rstrip(), re.S)])
        lex[t] = cs
    con.close()
    return lex


def parosit(kifejezesek, csoportok):
    """A JSON-kifejezések párja a lexikon-csoportok közül (a váz-kulcs szerint, sorrendben); [darabok | None]."""
    hasz = [False] * len(csoportok)
    ck = [kulcs(''.join(c)) for c in csoportok]
    p, ki = 0, []
    for js in kifejezesek:
        k = kulcs(js)
        talalt = None
        for rng in (range(p, min(len(csoportok), p + 80)), range(len(csoportok))):
            for i in rng:
                if not hasz[i] and ck[i] == k:
                    talalt = i
                    break
            if talalt is not None:
                break
        if talalt is None:
            ki.append(None)
            continue
        hasz[talalt] = True
        p = talalt
        ki.append(csoportok[talalt])
    return ki
