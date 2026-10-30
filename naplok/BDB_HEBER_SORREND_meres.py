#!/usr/bin/env python
"""A BDB héber kifejezéseinek sorrend- és geres-hibája: mérés és javítási-szabály javaslat (N-F131y).

Csak olvas és mér; adatot, forrást, lexikonlapot NEM ír. Kimenet: a mérés összesítése a konzolra, és a kézi
átnézésre szánt minta (`--minta-ki`, alapból a repón kívül nem; l. a jelentést: naplok/BDB_HEBER_SORREND_meres.md).

Bemenetek (csak olvasva):
  - konkordancia/lexikonok_nyers/DictBDB.json   — a <heb><ref0 entry="…"> héber kifejezései (a mért szöveg)
  - konkordancia/lexikonok_nyers/BDB.lexicon    — ugyanannak a digitalizálásnak a <bdbheb> darabjai (csak szerkezet:
                                                  a darabhatár; szöveget nem veszünk át belőle, DT225)
  - konkordancia/TAHOT_kivonat.tsv              — a héber Biblia szövege (független próba: a kifejezés szórendje)
  - adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/forditasok.tsv — a hatás mérése

Hipotézisek (a mérés előtt rögzítve):
  H1  a JSON kifejezése = a lexikon-darabok összefűzésének szóköz szerinti tokenjei FORDÍTOTT sorrendben;
  H2  a helyes logikai alak = a lexikon-darabok (a köztük álló szóközzel együtt) fordított sorrendje.
Szabályok:
  R0      csak a JSON tokenfordításának visszacsinálása (a tokenek megfordítása)
  R_lex   R0 + a lexikon darabhatárai szerint a darabok megfordítása (= H2; a lexikon kell hozzá)
  R_str   R0 + darabolás csak a szövegből: a geres, a geres melletti szóköz és a geres nélküli futam egy-egy darab
          (a futamon belüli szóköz marad), a darabok megfordítása — a lexikon nélkül is alkalmazható
  R_ang   a felhasználó hipotézise (2026-10-30): a futam szóvizuális (balról jobbra) alak; a szavak megfordítása, és
          tokenenként a betű elé került geres a token végére (a jelentés 8. szakasza)
  R_lap   a mai lap-javítás (lexikon_general.bdb_rovidites_jelol): csak az önálló, egybetűs ׳X → X׳

Próba a héber Biblián (TAHOT): a jelölt alak teljes szavai (és a rövidítés kezdőbetűje + rés, az ellipszis rés)
mássalhangzó-vázként egymás után előfordulnak-e egy versben. Egy tétel ítélete: `helyes` (a jelölt igen, a JSON-alak
nem), `rontott` (a JSON-alak igen, a jelölt nem), `eldonthetetlen` (mindkettő vagy egyik sem, vagy nincs két
szónyi anyag).

Futtatás: python naplok/BDB_HEBER_SORREND_meres.py [--minta-ki <utvonal.tsv>] [--seed 131]
"""
import argparse
import collections
import hashlib
import html
import json
import random
import re
import sqlite3
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

JSON_UT = 'konkordancia/lexikonok_nyers/DictBDB.json'
LEX_UT = 'konkordancia/lexikonok_nyers/BDB.lexicon'
TAHOT_UT = 'konkordancia/TAHOT_kivonat.tsv'
SZAK_UT = 'adat/bdb_szakaszok.tsv'
HU_UT = 'adat/bdb_szakasz_hu.tsv'
FORD_UT = 'adat/forditasok.tsv'

G = '׳'            # geres
MAKKEF = '־'
RAFE = 'ֿ'         # a forrás makkef-pótlója: a két szó egybeírva, a rafe a második szó első betűjén
ELLIPSZIS = '֗֗֗'   # a forrás „…”-jele (három revia)
BETU = 'א-ת'
VEGSO = str.maketrans('ךםןףץ', 'כמנפצ')


def sha16(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for d in iter(lambda: f.read(1 << 20), b''):
            h.update(d)
    return h.hexdigest()[:12]


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
    """(típus, szöveg) egységek: G geres, S szóköz, W geres nélküli betűsor."""
    return [('G' if m.group(0) == G else 'S' if m.group(0).isspace() else 'W', m.group(0))
            for m in EGYSEG_RE.finditer(szoveg)]


def _tomor(egys):
    """Az egymást követő szóközök egybe, a szélső szóközök nélkül (a ws() megfelelője egységszinten)."""
    out = []
    for e in egys:
        if e[0] == 'S' and (not out or out[-1][0] == 'S'):
            continue
        out.append(e)
    while out and out[-1][0] == 'S':
        out.pop()
    return out


def r_lex(js, darabok):
    """R0 után a lexikon darabhatárai szerint a darabok megfordítása. A lexikonból CSAK a határ jön (DT225): a
    szöveg az R0(js)-é. None, ha a két egységsor szerkezete eltér (nem vihető át a határ)."""
    lex = []
    for k, d in enumerate(darabok):
        lex += [(t, s, k) for t, s in _egysegek(d)]
    lex = _tomor(lex)
    sajat = _tomor(_egysegek(r0(js)))
    if [e[0] for e in lex] != [e[0] for e in sajat]:
        return None
    csop = collections.OrderedDict()
    for (t, _s, k), (_t2, s2) in zip(lex, sajat):
        csop.setdefault(k, []).append(s2)
    return ws(''.join(''.join(v) for v in reversed(list(csop.values()))))


DARAB_RE = re.compile(r'%s|\s+|[^%s\s]+(?:\s+[^%s\s]+)*' % (G, G, G))


def r_str(js):
    return ws(''.join(reversed(DARAB_RE.findall(r0(js)))))


def r_ang(js):
    """A felhasználó hipotézise (2026-10-30, „angol szórend”): a futam szóvizuális, balról jobbra tárolt alak; a
    vizuális → logikai konverzió a szavak megfordítása, és tokenenként a betű elé került geres a token végére."""
    return ' '.join((t[1:] + G) if t.startswith(G) and len(t) > 1 else t for t in reversed(ws(js).split(' ')))


def r_hib(js, darabok):
    """Vegyes szabály (a mérés 2. menete alapján): geres nélkül R0; geresnél R_lex, ha a lexikon szerkezete
    átvihető, különben R_str."""
    if G not in js:
        return r0(js)
    rl = r_lex(js, darabok) if darabok is not None else None
    return rl if rl is not None else r_str(js)


# a lexikon_general.py BDB_ROVIDITES_RE-je (PR #521), változatlanul
_HEB_BETU = 'א-תיִ-ﭏ'
_HEB_JEL = 'ְ-ׇ'
LAP_RE = re.compile(r'(?<![%s%s])׳([%s][%s]*)(?![%s%s])' % (_HEB_BETU, _HEB_JEL, _HEB_BETU, _HEB_JEL,
                                                             _HEB_BETU, _HEB_JEL))


def r_lap(js):
    return LAP_RE.sub(lambda m: m.group(1) + G, js)


# ---------------------------------------------------------------- kategóriák

def kategoria(js):
    tok = ws(js).split(' ')
    van_g = G in js
    if len(tok) == 1:
        if not van_g:
            return 'egy_szo_geres_nelkul'
        betuk = vaz(js)
        return 'egybetus_rovidites' if len(betuk) == 1 else 'egy_token_geressel_tobb_betu'
    if van_g:
        return 'rovidites_es_szo' if len(tok) == 2 else 'harom_plusz_token_geressel'
    return 'ket_szo' if len(tok) == 2 else 'harom_plusz_szo'


def jelzok(js):
    j = []
    if MAKKEF in js:
        j.append('makkef')
    if ELLIPSZIS in js:
        j.append('ellipszis')
    if re.search(r'[0-9A-Za-z]', js):
        j.append('szam_latin')
    if RAFE in js:
        j.append('rafe_makkef')
    if re.search(r'[,;.:]', js):
        j.append('irasjel')
    if re.search(r'(^|\s)ה[ֶַָ]', unicodedata.normalize('NFD', js)):
        j.append('nevelo')
    return j


# ---------------------------------------------------------------- héber Biblia

def tahot_folyam():
    versek = collections.OrderedDict()
    with open(TAHOT_UT, encoding='utf-8') as f:
        next(f)
        for ln in f:
            m = ln.rstrip('\n').split('\t')
            if len(m) > 2:
                versek.setdefault(m[0], []).append(vaz(m[2]))
    return '|' + '|'.join(''.join(v) for v in versek.values()) + '|'


def minta_re(alak):
    """A jelölt alak mintája a vázfolyamon; None, ha nincs benne legalább egy teljes szó és még egy egység
    (teljes szó vagy rövidítés: a betűi + legfeljebb 8 betűnyi rés)."""
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
    leghosszabb = max((vaz(t) for t in alak.split() if G not in t), key=len)
    return re.compile(''.join(reszek)), leghosszabb


class Biblia:
    def __init__(self):
        self.f = tahot_folyam()
        self.cache = {}

    def van(self, alak):
        if alak in self.cache:
            return self.cache[alak]
        rx, lit = minta_re(alak)
        if rx is None:
            self.cache[alak] = None
            return None
        talalt, i = False, self.f.find(lit)
        while i >= 0 and not talalt:
            a = self.f.rfind('|', 0, i)
            b = self.f.find('|', i)
            if rx.search(self.f, a, b + 1):
                talalt = True
            i = self.f.find(lit, b)
        self.cache[alak] = talalt
        return talalt


def itelet(bib, js_alak, jelolt):
    if ws(js_alak) == ws(jelolt):
        return 'azonos'
    a, b = bib.van(js_alak), bib.van(jelolt)
    if a is None or b is None:
        return 'eldonthetetlen'
    if b and not a:
        return 'helyes'
    if a and not b:
        return 'rontott'
    return 'eldonthetetlen'


# ---------------------------------------------------------------- bemenet

def json_tetelek():
    d = json.load(open(JSON_UT, encoding='utf-8'))
    out = collections.OrderedDict()
    for it in d:
        lst = []
        for m in re.finditer(r'<heb><ref0[^>]*entry="([^"]*)"[^>]*>(.*?)</ref0>', it['def'], re.S):
            entry = html.unescape(m.group(1))
            szoveg = html.unescape(re.sub(r'<[^>]+>', '', m.group(2)))
            lst.append((entry, szoveg))
        out[it['top']] = lst
    return out


def lexikon_csoportok():
    con = sqlite3.connect('file:%s?mode=ro' % LEX_UT, uri=True)
    lex = {}
    for t, df in con.execute("select Topic, Definition from Lexicon where Topic like 'BDB%'"):
        cs = []
        for m in re.finditer(r'(?:<bdbheb>.*?</bdbheb>\s*)+', df, re.S):
            darabok = []
            for sm in re.finditer(r'<bdbheb>(.*?)</bdbheb>|(\s+)', m.group(0).rstrip(), re.S):
                darabok.append(html.unescape(sm.group(1)) if sm.group(1) is not None else ' ')
            cs.append(darabok)
        lex[t] = cs
    con.close()
    return lex


def tsv(ut):
    sorok, fej = [], None
    with open(ut, encoding='utf-8') as f:
        for ln in f:
            if ln.startswith('#'):
                continue
            m = ln.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m)))
    return sorok


def strong_bdb(szak):
    s2b = collections.OrderedDict()
    for r in szak:
        kulcs_ = r['forras'].split(':', 1)[1].split('#')[0]
        lst = s2b.setdefault(kulcs_, [])
        if r['bdb_id'] and r['bdb_id'] not in lst:
            lst.append(r['bdb_id'])
    return s2b


# ---------------------------------------------------------------- mérés

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=131)
    ap.add_argument('--minta-ki')
    a = ap.parse_args()

    tet = json_tetelek()
    lex = lexikon_csoportok()
    szak = tsv(SZAK_UT)
    s2b = strong_bdb(szak)
    bib = Biblia()

    # 0. census a JSON-on
    osszes = sum(len(v) for v in tet.values())
    entry_elter = sum(1 for v in tet.values() for e, s in v if ws(e) != ws(s))
    geres_elott = geres_utan = geres_egyeb = 0
    for v in tet.values():
        for e, _ in v:
            for i, c in enumerate(e):
                if c != G:
                    continue
                elotte = e[i - 1] if i else ' '
                utana = e[i + 1] if i + 1 < len(e) else ' '
                if re.match('[%s]' % BETU, utana) and not re.match('[%s֑-ׇ]' % BETU, elotte):
                    geres_elott += 1
                elif re.match('[%s֑-ׇ]' % BETU, elotte):
                    geres_utan += 1
                else:
                    geres_egyeb += 1
    print('== 0. A JSON héber kifejezései')
    print('tétel (<heb><ref0>):', osszes, '| entry ≠ szöveg:', entry_elter)
    print('geres a kifejezésekben (csak a szöveg, az entry-attribútum nélkül): betű előtt %d, betű után %d, egyéb %d'
          % (geres_elott, geres_utan, geres_egyeb))

    # 1. párosítás a lexikonnal, H1
    stat = collections.Counter()
    tetelek = []   # (strong, js, darabok|None)
    for top, lst in tet.items():
        cs = []
        for b in s2b.get(top, []):
            cs += lex.get(b, [])
        hasz = [False] * len(cs)
        p = 0
        for js, _ in lst:
            k = kulcs(js)
            talalt = None
            for i in range(p, min(len(cs), p + 80)):
                if not hasz[i] and kulcs(''.join(cs[i])) == k:
                    talalt = i
                    break
            if talalt is None:
                for i in range(len(cs)):
                    if not hasz[i] and kulcs(''.join(cs[i])) == k:
                        talalt = i
                        break
            if talalt is None:
                stat['parositatlan'] += 1
                tetelek.append((top, js, None))
                continue
            hasz[talalt] = True
            p = talalt
            dar = cs[talalt]
            stat['parositott'] += 1
            osszef = ws(''.join(dar))
            if vaz_tok(r0(js)) == vaz_tok(osszef):
                stat['H1 igaz'] += 1
            else:
                stat['H1 hamis'] += 1
            if len([x for x in dar if x.strip()]) > 1:
                stat['tobb darab'] += 1
            tetelek.append((top, js, dar))
    print('\n== 1. Párosítás a BDB.lexicon darabjaival')
    print(dict(stat))

    # 2. szabályok a héber Biblián, kategóriánként
    print('\n== 2. Szabályok a héber Biblián (TAHOT), kategóriánként')
    kat_stat = collections.defaultdict(collections.Counter)
    jel_stat = collections.defaultdict(collections.Counter)
    egyezes = collections.Counter()
    geres_jo = collections.Counter()
    elter_pelda, rontott_pelda = [], collections.defaultdict(list)
    geres_pelda, elter_stat = [], collections.defaultdict(collections.Counter)
    rafe = sum(1 for _t, js, _d in tetelek if RAFE in js)
    for top, js, dar in tetelek:
        kat = kategoria(js)
        jel = jelzok(js)
        jeloltek = {'R0': r0(js), 'R_str': r_str(js), 'R_lap': r_lap(js), 'R_hib': r_hib(js, dar), 'R_ang': r_ang(js)}
        if dar is not None:
            rl = r_lex(js, dar)
            if rl is None:
                kat_stat[kat]['R_lex:szerkezet_elter'] += 1
            else:
                jeloltek['R_lex'] = rl
                if vaz_tok(rl) != vaz_tok(jeloltek['R_str']) or geres_hely(rl) != geres_hely(jeloltek['R_str']):
                    if len(elter_pelda) < 40:
                        elter_pelda.append((top, js, rl, jeloltek['R_str']))
            if rl is not None:
                egyezes['R_str = R_lex' if vaz_tok(jeloltek['R_str']) == vaz_tok(jeloltek['R_lex'])
                    and geres_hely(jeloltek['R_str']) == geres_hely(jeloltek['R_lex']) else 'R_str ≠ R_lex'] += 1
        kat_stat[kat]['tétel'] += 1
        for j in jel:
            jel_stat[j]['tétel'] += 1
        for nev, alak in jeloltek.items():
            it = itelet(bib, js, alak)
            if it == 'rontott' and nev in ('R_lex', 'R_str') and len(rontott_pelda[nev]) < 25:
                rontott_pelda[nev].append((top, js, alak))
            kat_stat[kat]['%s:%s' % (nev, it)] += 1
            for j in jel:
                jel_stat[j]['%s:%s' % (nev, it)] += 1
            if G in alak:
                jo = geres_mind_utan(alak)
                geres_jo['%s:%s' % (nev, 'jo' if jo else 'rossz')] += 1
                if not jo and nev == 'R_hib' and len(geres_pelda) < 30:
                    geres_pelda.append((top, js, alak))
        if dar is not None and 'R_lex' in jeloltek and ws(jeloltek['R_lex']) != ws(jeloltek['R_str']):
            for nev in ('R0', 'R_str', 'R_lex', 'R_hib'):
                elter_stat['%s geres' % ('van' if G in js else 'nincs')]['%s:%s' % (nev, itelet(bib, js, jeloltek[nev]))] += 1
    for kat in sorted(kat_stat):
        print(kat, dict(sorted(kat_stat[kat].items())))
    print('-- jelzők')
    for j in sorted(jel_stat):
        print(j, dict(sorted(jel_stat[j].items())))
    print('-- R_str és R_lex egyezése a párosított tételeken:', dict(egyezes))
    print('-- geres a betű után (ortográfiai próba), a geres tételeken:', dict(sorted(geres_jo.items())))
    print('-- a rafe (U+05BF) mint makkef-pótló (összevont szavak) tételei:', rafe)
    print('-- ahol R_str ≠ R_lex, a héber Biblia ítélete szabályonként:')
    for k in sorted(elter_stat):
        print('   ', k, dict(sorted(elter_stat[k].items())))
    print('-- R_hib után is rossz helyen álló geres (strong | JSON | R_hib):')
    for p in geres_pelda:
        print('   ', ' | '.join(p))
    print('-- példák, ahol R_str ≠ R_lex (strong | JSON | R_lex | R_str):')
    for p in elter_pelda:
        print('   ', ' | '.join(p))
    for nev in ('R_lex', 'R_str'):
        print('-- %s rontott példák (strong | JSON | jelölt):' % nev)
        for p in rontott_pelda[nev]:
            print('   ', ' | '.join(p))

    # 2/b. a felhasználó példái (H7121 Qal 2.c a nyomtatott BDB szerint; a lap példái): a váz-kulcs szerint keresve
    peldak = {('H7121', ('בשמ', 'י', 'ק')): 'ק׳ בְּשֵׁם י׳'}
    lap_peldak = {('למענ', 'ש'), ('י', 'שמ'), ('לש',)}
    print('\n-- példák (strong | JSON | R_hib | várt):')
    latott = set()
    for top, js, dar in tetelek:
        k = kulcs(js)
        if (top, k) in peldak and (top, k) not in latott:
            latott.add((top, k))
            print('   ', top, '|', ws(js), '|', r_hib(js, dar), '|', peldak[(top, k)])
        elif top in ('H7812', 'H8034', 'H4616') and k in lap_peldak and (top, k) not in latott:
            latott.add((top, k))
            print('   ', top, '|', ws(js), '|', r_hib(js, dar), '| (a lap példája)')
    # 2/c. összesítés R_hib-re: írásjel és sziglum nélkül / velük
    ossz = collections.defaultdict(collections.Counter)
    for top, js, dar in tetelek:
        kat = kategoria(js)
        if kat == 'egy_szo_geres_nelkul':
            continue
        jel = jelzok(js)
        osztaly = 'irasjel_vagy_sziglum' if ('irasjel' in jel or 'szam_latin' in jel) else 'tiszta'
        ossz[osztaly][itelet(bib, js, r_hib(js, dar))] += 1
        ossz[osztaly]['tétel'] += 1
        ossz[osztaly]['geres_jo' if (G not in r_hib(js, dar) or geres_mind_utan(r_hib(js, dar))) else 'geres_rossz'] += 1
    print('-- R_hib összesítve (a geres nélküli egyszavas tételek nélkül):')
    for k in sorted(ossz):
        print('   ', k, dict(sorted(ossz[k].items())))

    # 2/d. a felhasználó hipotézise (R_ang: szóvizuális tárolás → logikai): ugyanígy, futam-típusonként, és az
    # egyezés az R_hib-bel
    ang = collections.defaultdict(collections.Counter)
    ang_pelda = []
    for top, js, dar in tetelek:
        kat = kategoria(js)
        if kat == 'egy_szo_geres_nelkul':
            continue
        jel = jelzok(js)
        tipus = ('irasjel_vagy_sziglum' if ('irasjel' in jel or 'szam_latin' in jel)
                 else 'tiszta_geressel' if G in js else 'tiszta_geres_nelkul')
        ra, rh = r_ang(js), r_hib(js, dar)
        ang[tipus]['tétel'] += 1
        ang[tipus]['Biblia:' + itelet(bib, js, ra)] += 1
        ang[tipus]['= R_hib' if ra == rh else '≠ R_hib'] += 1
        ang[tipus]['geres_jo' if (G not in ra or geres_mind_utan(ra)) else 'geres_rossz'] += 1
        if ra != rh:
            it_a, it_h = itelet(bib, js, ra), itelet(bib, js, rh)
            ang[tipus]['eltérésben R_ang:%s / R_hib:%s' % (it_a, it_h)] += 1
            if len(ang_pelda) < 12 and tipus == 'tiszta_geressel':
                ang_pelda.append((top, ws(js), ra, rh, it_a, it_h))
    print('-- R_ang (a felhasználó hipotézise) futam-típusonként:')
    for k in sorted(ang):
        print('   ', k, dict(sorted(ang[k].items())))
    print('-- R_ang ≠ R_hib példák (strong | JSON | R_ang | R_hib | Biblia R_ang | Biblia R_hib):')
    for p in ang_pelda:
        print('   ', ' | '.join(p))

    # 3. hatás
    print('\n== 3. Hatás')
    valtozo = collections.defaultdict(set)
    for top, js, dar in tetelek:
        uj = r_hib(js, dar)
        if ws(uj) != ws(js):
            valtozo[top].add(ws(js))
    sor_db, strong_db = 0, set()
    for r in szak:
        top = r['forras'].split(':', 1)[1].split('#')[0]
        if any(x in r['szoveg'] for x in valtozo.get(top, ())):
            sor_db += 1
            strong_db.add(r['strong'])
    print('változó kifejezés: %d (%d Strong) | bdb_szakaszok.tsv érintett sor: %d / %d (%d Strong)'
          % (sum(len(v) for v in valtozo.values()), len(valtozo), sor_db, len(szak), len(strong_db)))
    pad = {('H%04d' % int(re.match(r'H(\d+)', k).group(1))) + k[len(re.match(r'H(\d+)', k).group(0)):]: k
           for k in valtozo}
    hu = tsv(HU_UT)
    hu_db = 0
    for r in hu:
        v = valtozo.get(pad.get(r['strong'], ''), ())
        if any(x in r['szoveg_hu'] for x in v):
            hu_db += 1
    ford = [r for r in tsv(FORD_UT) if r['szotar'] == 'BDB']
    f_sor, f_szo_ben = 0, 0
    strong_hu = collections.defaultdict(str)
    for r in ford:
        strong_hu[r['strong']] += '\n' + r['forditas_hu']
        v = valtozo.get(pad.get(r['strong'], ''), ())
        if not v:
            continue
        ben = [x for x in v if x in r['forditas_hu']]
        if ben:
            f_sor += 1
        f_szo_ben += len(ben)
    ford_strong = {r['strong'] for r in ford}
    erintett_ford_strong = {s for s in ford_strong if pad.get(s) in valtozo}
    kif_ossz = kif_ben = 0
    for s in erintett_ford_strong:
        for x in valtozo[pad[s]]:
            kif_ossz += 1
            kif_ben += x in strong_hu[s]
    print('forditasok.tsv: a lefordított, érintett Strongok változó kifejezései: %d; ebből a magyarban szó szerint '
          'megtalálható (cserével javítható): %d (%.1f%%)' % (kif_ossz, kif_ben, 100.0 * kif_ben / max(kif_ossz, 1)))
    print('bdb_szakasz_hu.tsv érintett sor (a hibás héber alak szó szerint a magyarban): %d / %d' % (hu_db, len(hu)))
    print('forditasok.tsv BDB: %d sor, %d Strong; érintett Strong (van változó kifejezése): %d; '
          'sor, amelyben a hibás alak szó szerint áll: %d; szó szerinti előfordulás: %d'
          % (len(ford), len(ford_strong), len(erintett_ford_strong), f_sor, f_szo_ben))

    # 3/b. határ: a héber futam és az utána álló szám (igehely). Bidi-megjelenítésben a futam utáni gyenge szám
    # (EN) és a köztük álló semleges jel (szóköz, írásjel) a jobbról balra futamhoz tapad, ha nincs elválasztó (LRM,
    # izoláló jel vagy elem). A JSON a futam után LRM-et tesz; a bont.py / _convert_bdb.py sima() kiveszi.
    print('\n== 3/b. Határ: héber futam + utána szám')
    d = json.load(open(JSON_UT, encoding='utf-8'))
    hatar = collections.Counter()
    for it in d:
        for m in re.finditer(r'</heb>((?:&#x200E;|‎)?)', it['def']):
            hatar['futam'] += 1
            hatar['utana LRM' if m.group(1) else 'utana nincs LRM'] += 1
            kov = re.sub(r'<[^>]+>', '', it['def'][m.end():m.end() + 200])
            kov = html.unescape(kov).replace('‎', '')
            mm = re.match(r'[\s,;:()\[\].\-–—=]*(.)', kov)
            if mm and mm.group(1).isdigit():
                hatar['utana (semlegesek után) szám'] += 1
    print('DictBDB.json:', dict(hatar))
    minta_hatar = re.compile(r'[֑-״יִ-ﭏ][\s,;:()\[\].\-–—=]*\d')
    for nev, sorok_, mezo in ((SZAK_UT, szak, 'szoveg'), (HU_UT, hu, 'szoveg_hu'),
                              (FORD_UT, ford, 'forditas_hu')):
        elof = sum(len(minta_hatar.findall(r[mezo])) for r in sorok_)
        sor = sum(1 for r in sorok_ if minta_hatar.search(r[mezo]))
        lrm = sum(r[mezo].count('‎') for r in sorok_)
        print('%s (%s): héber + szám határ %d előfordulás, %d sor; LRM a mezőben: %d' % (nev, mezo, elof, sor, lrm))

    # 4. kézi minta
    rnd = random.Random(a.seed)
    jelolt_tet = [t for t in tetelek if kategoria(t[1]) != 'egy_szo_geres_nelkul']
    minta = rnd.sample(jelolt_tet, 50)
    print('\n== 4. Kézi minta (seed %d, 50 tétel a %d geres- vagy több tokenes tételből)' % (a.seed, len(jelolt_tet)))
    sorok = ['sorszam\tstrong\tkategoria\tjelzok\tjson_alak\tjavasolt_R_hib\tbiblia_R_hib\tlexikon_parositva\tR_ang']
    for n, (top, js, dar) in enumerate(minta, 1):
        rh = r_hib(js, dar)
        ra = r_ang(js)
        sorok.append('\t'.join([str(n), top, kategoria(js), ','.join(jelzok(js)), ws(js), rh, itelet(bib, js, rh),
                                'igen' if dar is not None else 'nem', '= R_hib' if ra == rh else ra]))
    if a.minta_ki:
        with open(a.minta_ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok) + '\n')
        print('minta kiírva:', a.minta_ki)
    else:
        print('\n'.join(sorok))

    print('\nproveniencia: scope=DictBDB.json összes <heb> kifejezése | forras=naplok/BDB_HEBER_SORREND_meres.py; '
          'DictBDB.json@%s, BDB.lexicon@%s, TAHOT_kivonat.tsv@%s, bdb_szakaszok.tsv@%s, bdb_szakasz_hu.tsv@%s, '
          'forditasok.tsv@%s | ts=2026-10-30'
          % tuple(sha16(u) for u in (JSON_UT, LEX_UT, TAHOT_UT, SZAK_UT, HU_UT, FORD_UT)))


def vaz_tok(s):
    return [vaz(t) for t in s.replace(G, ' ').split() if vaz(t)]


def geres_hely(s):
    """A geresek helye: melyik váz-tokenhez tapadnak, és előtte vagy utána."""
    return re.sub(r'[^\s%s%s]' % (G, BETU), '', unicodedata.normalize('NFD', s))


def geres_mind_utan(s):
    """A geres minden előfordulása betű (prezentációs alak is, l. a lap regexét) vagy pontozás után áll."""
    return all(i > 0 and re.match('[%s%s֑-֯]' % (_HEB_BETU, _HEB_JEL), s[i - 1])
               for i, c in enumerate(s) if c == G)


if __name__ == '__main__':
    main()
