#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bdb_rokon.py -- F176.3: a BDB rokon nyelvi irasainak (arab, etiop, szir) gyorsitotara a Sefaria "BDB Dictionary" /
"BDB Aramaic Dictionary" szocikkeibol -> konkordancia/BDB_rokon_irasok.tsv.

Miert: a repo BDB_teljes_unabridged.tsv-jeben a nem-latin, nem-heber irasu rokon szavak (pl. "Arabic ,") elvesztek;
a Sefaria szocikke megorizte oket. A BDB_teljes_unabridged.tsv NEM valtozik.

Bemenet: --strong H7843 H0779 ...   vagy   --motivum HAMART-001  (az adat/elofordulasok.tsv `strong` es `gerinc_elem`
         oszlopanak heber H-szamai). A szocikk fejszavat a BDB_teljes_unabridged.tsv adja (a Strong sorabol az elso
         heber irasu token), a Sefaria `/api/words/<mássalhangzós alak>` hivasa a BDB-szocikkeket a
         `strong_numbers` mezo alapjan illeszti a Strong-szamhoz.
Gyorsitotar: a szkript ELOSZOR a kimeneti tablaban keres. Egy Strong akkor "lekerdezett", ha a tabla fejlecsoraiban
         `# lekérdezve: H7843 | ...` bejegyzes van (ez rogziti a NEM-talalatot is, amely nem sor); csak a hianyzo Strong
         kerul lekerdezesre. Rata: >= 1 s a kerelmek kozott; azonosito User-Agent, felhasznaloi e-mail nelkul.
Kimenet oszlopai: strong, sefaria_ref, nyelv, szoalak, kontextus (<= 120 karakter a BDB-fejbol), proveniencia.

Futtatas:  python -I eszkozok/visszhang/bdb_rokon.py --motivum HAMART-001
           python -I eszkozok/visszhang/bdb_rokon.py --strong H7843
"""
import argparse
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402

KIMENET = os.path.join(K.GYOKER, 'konkordancia', 'BDB_rokon_irasok.tsv')
BDB_TELJES = os.path.join(K.GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
ELOFORDULAS = os.path.join(K.GYOKER, 'adat', 'elofordulasok.tsv')
TAHOT = os.path.join(K.GYOKER, 'konkordancia', 'TAHOT_kivonat.tsv')
MAX_ALAK = 4        # a fejszon kivul legfeljebb ennyi gyakori felszini alak kerul lekerdezesre
API = 'https://www.sefaria.org/api/words/'
UA = 'PaRDeS-research/1.0'
MIN_KOZ = 1.1       # masodperc a kerelmek kozott (>= 1 s)
LEXIKONOK = ('BDB Dictionary', 'BDB Aramaic Dictionary')
HEBER_RX = re.compile('[\u0590-\u05FF]+')       # a szocikk NFD-re bontva (az FB1D-FB4F bemutatasi alakok felbomlanak)
TAG_RX = re.compile(r'<[^>]+>')
OSZLOPOK = ['strong', 'sefaria_ref', 'nyelv', 'szoalak', 'kontextus', 'proveniencia']

# (blokk-tartomanyok, nyelvtipp) -- Unicode-blokk szerint
IRASOK = [
    ('arab', [(0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF)]),
    ('etióp', [(0x1200, 0x139F), (0x2D80, 0x2DDF), (0xAB00, 0xAB2F)]),
    ('szír', [(0x0700, 0x074F), (0x0860, 0x086F)]),
]


def irasa(ch):
    o = ord(ch)
    for nev, tart in IRASOK:
        for a, b in tart:
            if a <= o <= b:
                return nev
    return None


def tokenek(szoveg):
    """-> [(nyelv, token, kezdo_index)] -- szokozzel/irasjellel tagolt, azonos irasu szavak."""
    ki = []
    i, n = 0, len(szoveg)
    while i < n:
        ny = irasa(szoveg[i])
        if ny is None:
            i += 1
            continue
        j = i
        while j < n and (irasa(szoveg[j]) == ny or unicodedata.category(szoveg[j]) in ('Mn', 'Me')):
            j += 1
        ki.append((ny, szoveg[i:j], i))
        i = j
    return ki


def tiszta_szoveg(x):
    """A Sefaria-szocikk `content` fa osszes szovege, egyetlen sorban, tag nelkul."""
    reszek = []

    def bejar(o):
        if isinstance(o, str):
            reszek.append(o)
        elif isinstance(o, list):
            for e in o:
                bejar(e)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ('definition', 'senses', 'text', 'content'):
                    bejar(v)
    bejar(x)
    t = ' '.join(reszek)
    t = html.unescape(TAG_RX.sub(' ', t))
    return re.sub(r'\s+', ' ', t).strip()


def fejszo(strong):
    """A Strong heber fejszava a BDB_teljes_unabridged.tsv-bol, magánhangzójelek nelkul (mássalhangzós alak)."""
    with open(BDB_TELJES, encoding='utf-8') as f:
        for s in f:
            if s.startswith(strong + '\t'):
                szoveg = unicodedata.normalize('NFD', s.split('\t', 2)[2][:120])
                m = HEBER_RX.search(szoveg)
                if m:
                    return mássalhangzós(m.group(0))
    return ''


def mássalhangzós(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if 0x05D0 <= ord(c) <= 0x05EA)


def alakok(strong):
    """A Strong leggyakoribb felszini alakjai a TAHOT_kivonat.tsv-bol (mássalhangzós alak), gyakorisag szerint.
    A Sefaria /api/words a SZOALAK-indexben keres (nem fejszoban): a tovabbi alakok csak akkor kellenek, ha a fejszo
    nem ad BDB-szocikket."""
    szaml = {}
    with open(TAHOT, encoding='utf-8') as f:
        for s in f:
            if '	' + strong + '	' not in s:
                continue
            m = s.split('	')
            if len(m) > 2 and m[1] == strong:
                a = mássalhangzós(m[2])
                if a:
                    szaml[a] = szaml.get(a, 0) + 1
    return [a for a, _ in sorted(szaml.items(), key=lambda x: (-x[1], x[0]))][:MAX_ALAK]


def probalkozasok(strong, szo):
    """Lusta generator: eloszor a fejszo, csak ha az nem ad BDB-szocikket, a TAHOT-alakok (a TAHOT beolvasasa draga)."""
    yield szo
    for a in alakok(strong):
        if a != szo:
            yield a


def lekeres(szo, volt):
    """Sefaria /api/words/<szo> -> JSON-lista. A `volt` egy egyelemu lista az utolso kerelem idejevel (rata)."""
    var = MIN_KOZ - (time.time() - volt[0])
    if var > 0:
        time.sleep(var)
    req = urllib.request.Request(API + urllib.parse.quote(szo), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        adat = json.loads(r.read().decode('utf-8'))
    volt[0] = time.time()
    return adat


def olvas_gyorsitotar(ut):
    sorok, lekerdezve = [], {}
    if not os.path.exists(ut):
        return sorok, lekerdezve
    with open(ut, encoding='utf-8') as f:
        for s in f.read().split('\n'):
            if s.startswith('# lekérdezve: '):
                resz = [x.strip() for x in s[len('# lekérdezve: '):].split('|')]
                lekerdezve[resz[0]] = resz[1:]
            elif s.strip() and not s.startswith('#') and not s.startswith('strong\t'):
                sorok.append(s.split('\t'))
    return sorok, lekerdezve


def strongok_motivumbol(azon):
    ki = []
    with open(ELOFORDULAS, encoding='utf-8') as f:
        sorok = [s for s in f.read().split('\n') if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    for s in sorok[1:]:
        m = s.split('\t')
        if m[fej.index('id')] != azon:
            continue
        for cella in (m[fej.index('strong')], m[fej.index('gerinc_elem')]):
            for h in re.findall(r'H\d{4}', cella):
                if h not in ki:
                    ki.append(h)
    return ki


def kontextus(szoveg, kezdo, token):
    """<= 120 karakter a szocikk szovegebol a token korul (a token elott ~50 karakter)."""
    a = max(0, kezdo - 50)
    if a > 0:
        sp = szoveg.find(' ', a)
        a = sp + 1 if 0 <= sp < kezdo else a
    b = a + 120
    if b < len(szoveg):
        sp = szoveg.rfind(' ', kezdo, b)
        b = sp if sp > kezdo + len(token) else b
    return szoveg[a:b].strip()[:120]


def feldolgoz(strong, adat, ts):
    """-> sorok, ahol a token nem-heber, nem-latin irasu (arab/etiop/szir), a szocikk `strong_numbers` mezoje alapjan."""
    szam = str(int(strong[1:]))
    sorok = []
    for e in adat:
        if e.get('parent_lexicon') not in LEXIKONOK:
            continue
        if szam not in [str(x) for x in e.get('strong_numbers', [])]:
            continue
        szoveg = tiszta_szoveg(e.get('content'))
        ref = '%s, %s' % (e['parent_lexicon'], e.get('headword', ''))
        if e.get('rid'):
            ref += ' [%s]' % e['rid']
        lattuk = set()
        for ny, tok, k in tokenek(szoveg):
            if (ny, tok) in lattuk:
                continue
            lattuk.add((ny, tok))
            prov = 'scope=Sefaria /api/words (%s; strong_numbers∋%s) | forras=sefaria.org BDB (Brown–Driver–Briggs, Oxford 1906) | ts=%s' % (
                e['parent_lexicon'], szam, ts)
            sorok.append([strong, ref, ny, tok, kontextus(szoveg, k, tok), prov])
    return sorok


def fut(strongok, ki=KIMENET, lekero=lekeres):
    sorok, lekerdezve = olvas_gyorsitotar(ki)
    ts = K.ts()
    volt, keres, jelentes = [0.0], 0, []
    for st in strongok:
        if st in lekerdezve:
            jelentes.append((st, 'gyorsítótárban', sum(1 for s in sorok if s[0] == st)))
            continue
        szo = fejszo(st)
        if not szo:
            raise SystemExit('nincs heber fejszo a BDB_teljes_unabridged.tsv-ben: %s' % st)
        probak = probalkozasok(st, szo)
        szam = str(int(st[1:]))
        adat, hasznalt, illeszkedo = [], [], 0
        for pr in probak:
            adat = lekero(pr, volt)
            keres += 1
            hasznalt.append(pr)
            illeszkedo = sum(1 for e in adat if e.get('parent_lexicon') in LEXIKONOK and szam in [str(x) for x in e.get('strong_numbers', [])])
            if illeszkedo:
                break
        uj = feldolgoz(st, adat, ts)
        sorok.extend(uj)
        lekerdezve[st] = ['próbált_alakok=%s' % ','.join(hasznalt), 'bdb_szócikk=%d' % illeszkedo, 'rokon_írás_sor=%d' % len(uj), 'ts=%s' % ts]
        jelentes.append((st, 'lekérve', len(uj)))
    sorok.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
    fejlec = [
        'GENERÁLT/GYORSÍTÓTÁR: eszkozok/visszhang/bdb_rokon.py (F176.3); a BDB_teljes_unabridged.tsv nem változik.',
        'forras=Sefaria API /api/words (BDB Dictionary, BDB Aramaic Dictionary; Brown–Driver–Briggs, Oxford 1906; a szócikk-illesztés a strong_numbers mező szerint); csak arab/etióp/szír írású tokenek (Unicode-blokk szerint).',
    ]
    fejlec += ['lekérdezve: %s | %s' % (k, ' | '.join(v)) for k, v in sorted(lekerdezve.items())]
    K.ir_tsv(ki, fejlec, OSZLOPOK, sorok)
    return jelentes, keres, sorok


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--strong', nargs='*', default=[])
    ap.add_argument('--motivum')
    ap.add_argument('--ki', default=KIMENET)
    a = ap.parse_args()
    lista = [s if s.startswith('H') and len(s) == 5 else 'H%04d' % int(s.lstrip('H')) for s in a.strong]
    if a.motivum:
        lista += [s for s in strongok_motivumbol(a.motivum) if s not in lista]
    if not lista:
        raise SystemExit('adj --strong vagy --motivum')
    jel, keres, sorok = fut(lista, a.ki)
    for st, mod, n in jel:
        print('%s: %s, rokon-iras sor: %d' % (st, mod, n))
    print('HTTP-kerelem: %d; sorok osszesen: %d' % (keres, len(sorok)))
