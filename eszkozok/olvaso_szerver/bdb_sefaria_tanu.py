#!/usr/bin/env python
"""bdb_sefaria_tanu.py — F196: harmadik tanú a BDB vers → jelentéspont hozzárendeléshez (adat/bdb_vers_jelentes.tsv, 2.29).

A tanú a Sefaria BDB-feldolgozása (`/api/words`, „BDB Dictionary” / „BDB Aramaic Dictionary”): ugyanaz az 1906-os szöveg,
de a jelentésfát (törzs → szám → betű) és az igehely-linkeket (`data-ref`) a Sefaria saját feldolgozása adja, a mi
szeletelőnktől (`bdb_szelet`) és szakasztáblánktól (2.30) függetlenül. Ahol a két pont eltér, a sor `ketes:jp_tanu_sefaria`;
egyezésnél és ha a Sefaria a verset nem linkeli, a bizonyosság változatlan (az egyezés nem emel; DT-F196a).

Három lépés, mind külön alparancs:
  letolt   a Sefaria-válaszok gyorsítótárba, a REPÓN KÍVÜL (alapból D:\\pardes_tanu\\bdb\\api; `--cache`), kérésenként
           ≥ 1,1 s szünet, azonosító User-Agent, e-mail nélkül; a lekérések naplója: <cache>/../lekeresek.tsv.
  tabla    a gyorsítótárból a tanú-tábla: adat/bdb_jp_sefaria.tsv (SEMA 2.29.1). Soronként csak a Sefaria-pont normalizált
           útvonala áll (homonima | rész | törzs/szám/betű), Sefaria-szöveg nem.
  meres    a seed-103 vak minta (F185) 200 pontján: hány gépi hibát jelez a tanú, és hány helyes pontra ad téves riasztást;
           `--proba40`: a 40 soros téves-riasztási próba (a 19 `ketes` és 21 `biztos` sor, rögzített véletlennel).

Az összevetés szabálya (`osszevet`) egy helyen áll, ezt hívja a 2.29 generátora is (kapcsolóval, alapból kikapcsolva).
TSV: split('\\t') / '\\t'.join, csv modul nélkül.

Használat (a repó gyökeréből):
  python -I eszkozok/olvaso_szerver/bdb_sefaria_tanu.py letolt --minta seed103
  python -I eszkozok/olvaso_szerver/bdb_sefaria_tanu.py tabla --ts 2026-11-11
  python -I eszkozok/olvaso_szerver/bdb_sefaria_tanu.py meres [--proba40]
"""
import argparse
import collections
import hashlib
import json
import os
import random
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(D))
CACHE = os.environ.get('PARDES_SEFARIA_BDB', r'D:\pardes_tanu\bdb\api')
BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
VJ = os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')
KI = os.path.join(REPO, 'adat', 'bdb_jp_sefaria.tsv')
NAPLO = os.path.join(REPO, 'naplok')
API = 'https://www.sefaria.org/api/words/'
UA = 'PaRDeS-research/1.0'
MIN_KOZ = 1.1
MAX_ALAK = 4
LEXIKONOK = ('BDB Dictionary', 'BDB Aramaic Dictionary')
TANU = 'sefaria-api'
OSZLOPOK = ['strong', 'sorszam', 'mt_vers', 'sefaria_rid', 'illesztes', 'sefaria_ut', 'proveniencia']

# a Sefaria angol könyvnevei → a 2.29 `mt_vers` magyar rövidítései (a Sefaria a Tanakhot MT-számozással linkeli)
SEF_KONYV = {
    'Genesis': '1Móz', 'Exodus': '2Móz', 'Leviticus': '3Móz', 'Numbers': '4Móz', 'Deuteronomy': '5Móz', 'Joshua': 'Józs',
    'Judges': 'Bír', 'Ruth': 'Ruth', 'I Samuel': '1Sám', 'II Samuel': '2Sám', 'I Kings': '1Kir', 'II Kings': '2Kir',
    'I Chronicles': '1Krón', 'II Chronicles': '2Krón', 'Ezra': 'Ezsd', 'Nehemiah': 'Neh', 'Esther': 'Eszt', 'Job': 'Jób',
    'Psalms': 'Zsolt', 'Proverbs': 'Péld', 'Ecclesiastes': 'Préd', 'Song of Songs': 'Én', 'Isaiah': 'Ézs', 'Jeremiah': 'Jer',
    'Lamentations': 'JSir', 'Ezekiel': 'Ez', 'Daniel': 'Dán', 'Hosea': 'Hós', 'Joel': 'Jóel', 'Amos': 'Ámós', 'Obadiah': 'Abd',
    'Jonah': 'Jón', 'Micah': 'Mik', 'Nahum': 'Náh', 'Habakkuk': 'Hab', 'Zephaniah': 'Sof', 'Haggai': 'Hag', 'Zechariah': 'Zak',
    'Malachi': 'Mal',
}
REF_RX = re.compile(r'data-ref="([^"]+)"')
# a törzsnév egyetlen szó (betű, átírásjel, aposztróf, pont); a többszavas vagy írásjeles `form` fejléc, nem törzs (ELLENOR_F196)
TORZS_FORM = re.compile(r"^[A-Za-z\u00C0-\u024F\u02BE\u02BF'`.]+$")
HEB = re.compile('[\u0590-\u05FF]+')
ROMAI = re.compile(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X)$')
ROMAI_ERT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
FELSO = {'²': 2, '³': 3, '⁴': 4, '⁵': 5, '⁶': 6, '⁷': 7}


# ------------------------------------------------------------------ közös

def tsv_sorok(ut):
    fej, ki = None, []
    with open(ut, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(dict(zip(fej, m)))
    return ki


def massalhangzo(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if 0x05D0 <= ord(c) <= 0x05EA)


def strong_szam(strong):
    return str(int(re.match(r'^H0*(\d+)', strong).group(1)))


def fejszavak(strongok):
    """{strong: a BDB-szócikk első héber tokenje, mássalhangzós alakban}."""
    ki = {}
    s_be = set(strongok)
    with open(BDB_EN, encoding='utf-8') as f:
        for s in f:
            k = s.split('\t', 1)[0]
            if k in s_be:
                m = HEB.search(unicodedata.normalize('NFD', s.split('\t', 2)[2][:160]))
                ki[k] = massalhangzo(m.group(0)) if m else ''
    return ki


def tahot_alakok(strongok):
    """{strong: [a leggyakoribb mássalhangzós felszíni alakok]} a TAHOT-ból (a fejszó után próbálandók)."""
    sz = collections.defaultdict(collections.Counter)
    s_be = set(strongok)
    with open(TAHOT, encoding='utf-8') as f:
        for s in f:
            m = s.split('\t')
            if len(m) > 2 and m[1] in s_be:
                a = massalhangzo(m[2])
                if a:
                    sz[m[1]][a] += 1
    return {k: [a for a, _ in sorted(v.items(), key=lambda x: (-x[1], x[0]))][:MAX_ALAK] for k, v in sz.items()}


def cache_ut(cache, szo):
    return os.path.join(cache, hashlib.md5(szo.encode('utf-8')).hexdigest() + '.json')


def cache_olvas(cache, szo):
    fn = cache_ut(cache, szo)
    if not os.path.exists(fn):
        return None
    with open(fn, encoding='utf-8') as f:
        return json.load(f)


# ------------------------------------------------------------------ letöltés

def lekeres(cache, szo, volt, naplo):
    var = MIN_KOZ - (time.time() - volt[0])
    if var > 0:
        time.sleep(var)
    req = urllib.request.Request(API + urllib.parse.quote(szo) + '?never_split=1', headers={'User-Agent': UA})
    allapot = 'ok'
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            nyers = r.read()
        adat = json.loads(nyers.decode('utf-8'))
    except Exception as e:  # a hibát naplózzuk, a szó nem kerül a gyorsítótárba
        volt[0] = time.time()
        naplo.write('%s\t%s\thiba: %s\t\n' % (szo, time.strftime('%Y-%m-%dT%H:%M:%S'), str(e).replace('\t', ' ')))
        return None
    volt[0] = time.time()
    with open(cache_ut(cache, szo), 'w', encoding='utf-8') as f:
        json.dump(adat, f, ensure_ascii=False)
    naplo.write('%s\t%s\t%s\t%s\n' % (szo, time.strftime('%Y-%m-%dT%H:%M:%S'), allapot, hashlib.sha256(nyers).hexdigest()))
    naplo.flush()
    return adat


def bdb_bejegyzesek(adat, szam):
    return [e for e in (adat or []) if e.get('parent_lexicon') in LEXIKONOK and szam in [str(x) for x in e.get('strong_numbers') or []]]


def letolt(strongok, cache):
    os.makedirs(cache, exist_ok=True)
    fej = fejszavak(strongok)
    alak = None
    volt = [0.0]
    n_ker = n_nincs = 0
    with open(os.path.join(os.path.dirname(cache), 'lekeresek.tsv'), 'a', encoding='utf-8', newline='\n') as naplo:
        for i, st in enumerate(sorted(strongok)):
            szam = strong_szam(st)
            probak = [fej.get(st, '')]
            talalt = False
            j = 0
            while j < len(probak):
                szo = probak[j]
                j += 1
                if not szo:
                    continue
                adat = cache_olvas(cache, szo)
                if adat is None:
                    adat = lekeres(cache, szo, volt, naplo)
                    n_ker += 1
                if bdb_bejegyzesek(adat, szam):
                    talalt = True
                    break
                if j == len(probak) and len(probak) == 1:
                    if alak is None:
                        alak = tahot_alakok(strongok)
                    probak += [a for a in alak.get(st, []) if a != szo]
            if not talalt:
                n_nincs += 1
            if i % 25 == 0:
                print('%d/%d %s kérés=%d nincs=%d' % (i, len(strongok), st, n_ker, n_nincs), flush=True)
    print('kész: %d Strong, %d kérés, %d Strong BDB-szócikk nélkül' % (len(strongok), n_ker, n_nincs))


# ------------------------------------------------------------------ a Sefaria-fa

def ref_versek(ref):
    """'I Samuel 25:37' → ['1Sám 25:37']; tartomány ('Exodus 20:9-10') → minden vers; nem bibliai ('BDB, …') → []."""
    m = re.match(r'^(.+?) (\d+):(\d+)(?:-(\d+)(?::(\d+))?)?$', ref.strip())
    if not m or m.group(1) not in SEF_KONYV:
        return []
    k = SEF_KONYV[m.group(1)]
    c, v = int(m.group(2)), int(m.group(3))
    if m.group(4) and not m.group(5):
        return ['%s %d:%d' % (k, c, x) for x in range(v, int(m.group(4)) + 1)][:40]
    return ['%s %d:%d' % (k, c, v)]


def _szint(num):
    """A Sefaria `num`-ja → (fajta, érték): római rész, arab szám, kisbetű, nagybetű (csoport), egyéb."""
    t = (num or '').strip().rstrip('.').strip('()')
    if ROMAI.match(t):
        return 'resz', t
    if re.match(r'^\d+$', t):
        return 'szam', t
    if re.match(r'^[a-z]$', t):
        return 'betu', t
    if re.match(r'^[A-Z]$', t):
        return 'nagy', t
    return 'egyeb', t


def fa_utak(bejegyzes):
    """A bejegyzés igehely-linkjei dokumentum-sorrendben: [(vers, (rész, törzs, szám, betű))]."""
    ki = []

    def bejar(s, resz, torzs, szam, betu):
        if s.get('form') and TORZS_FORM.match(s['form'].strip()):
            torzs = s['form'].strip()
            resz, szam, betu = '', '', ''
        if s.get('num'):
            f, e = _szint(s['num'])
            if f == 'resz':
                resz, szam, betu = e, '', ''
            elif f == 'szam':
                # zárójeles „(1)” vagy a betű alatti szám: harmadik szint, a fő mutató nem változik
                if not (szam and (s['num'].strip().startswith('(') or betu)):
                    szam, betu = e, ''
            elif f == 'betu':
                if not betu:
                    betu = e
        for r in REF_RX.findall(s.get('definition', '') or ''):
            for v in ref_versek(r):
                ki.append((v, (resz, torzs, szam, betu)))
        for t in s.get('senses', []) or []:
            bejar(t, resz, torzs, szam, betu)

    bejar(bejegyzes.get('content', {}) or {}, '', '', '', '')
    return ki


def homonima(headword):
    for ch, n in FELSO.items():
        if ch in headword:
            return n
    return 1


def ut_szoveg(hom, p):
    resz, torzs, szam, betu = p
    return '%d|%s|%s/%s/%s' % (hom, resz, torzs or '-', szam or '-', betu or '-')


def ut_bont(s):
    hom, resz, ut = s.split('|')
    t, sz, b = ut.split('/')
    return int(hom), resz, ('' if t == '-' else t), ('' if sz == '-' else sz), ('' if b == '-' else b)


# ------------------------------------------------------------------ összevetés (egy szabály, egy hely)

def _torzs_kulcs(t):
    # a Sefaria ékezetes átírása („Pōʿlēl”) NFD-bontással, a kombináló jelek nélkül
    t = ''.join(c for c in unicodedata.normalize('NFD', t or '') if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', t.lower())


def _torzs_egyezik(a, b):
    """`a`: a tábla törzse ('-': a táblában kifejezetten törzs nélküli számozott pont), `b`: a Sefaria-pont törzse."""
    if a == '-':
        return not b      # v3: a törzs hiánya eltérés, ha a Sefaria törzset ad (a szám-szabály párja; s103-N061)
    a, b = _torzs_kulcs(a), _torzs_kulcs(b)
    if not a or not b:
        return True
    return a.startswith(b) or b.startswith(a)


def tabla_pont(szakasz, resz, utvonal):
    """A 2.29 pontja → (homonima vagy None, rész, törzs, szám, betű); `fej` / `tagolatlan` → üres szintek."""
    hom = ROMAI_ERT.get(szakasz) if ROMAI.match(szakasz or '') else None
    if utvonal in ('fej', 'tagolatlan', 'cim', ''):
        return hom, resz or '', '', '', ''
    r = (utvonal.split('/') + ['-', '-', '-'])[:3]
    t = r[0].split('.')[0]
    sz = r[1] if re.match(r'^\d+$', r[1]) else ''
    b = r[2] if re.match(r'^[a-z]$', r[2]) else ''
    return hom, resz or '', ('-' if t == '-' and sz else ('' if t == '-' else t)), sz, b


def pont_egyezik(tp, sp, sef_tobb_homonima):
    """A tábla pontja (tabla_pont) és egy Sefaria-pont (ut_bont) összefér-e.
    homonima: NEM vetjük össze (v2, DT-F196a): a Sefaria felső indexe (²) a Sefaria saját sorszáma az azonos alakú címszavakra,
      nem a BDB római száma (pl. H2022 הַר: a BDB-ben számozatlan, a Sefariában „²”); a v1 ezen a seed-103 helyes sorain
      téves riasztást adott (naplok/F196_jelentes.md 3.);
    rész: csak ha mindkettő megadja; törzs: ha mindkettő megadja, egyik a másik előtagja (rövidítés: „Hiph.” ~ „Hiph'il”);
    szám: mindkét oldalon azonos (a hiány is: „fej” ↔ „1.” eltérés); betű: ha mindkettő megadja, azonos."""
    thom, tresz, tt, tsz, tb = tp
    shom, sresz, st, ssz, sb = sp
    if tresz and sresz and tresz != sresz:
        return False
    if not _torzs_egyezik(tt, st):
        return False
    if tsz != ssz:
        return False
    if tb and sb and tb != sb:
        return False
    return True


def osszevet(szakasz, resz, utvonal, sefaria_ut, tobb_hom):
    """→ 'egyezik' | 'elter' | 'nincs'. `sefaria_ut`: a tanú-tábla mezője (';'-vel több pont: bármelyik elég)."""
    if not sefaria_ut:
        return 'nincs'
    tp = tabla_pont(szakasz, resz, utvonal)
    for s in sefaria_ut.split(';'):
        if pont_egyezik(tp, ut_bont(s), tobb_hom):
            return 'egyezik'
    return 'elter'


# ------------------------------------------------------------------ a tanú-tábla

def strong_utak(cache, st, fej, alakok):
    """→ (rid-ek, {vers: [út-szöveg]}, több_homonima) a gyorsítótárból; None, ha a Strongra nincs gyorsítótárazott válasz."""
    szam = strong_szam(st)
    bej, volt_valasz = [], False
    for szo in [fej] + [a for a in alakok if a != fej]:
        if not szo:
            continue
        adat = cache_olvas(cache, szo)
        if adat is None:
            continue
        volt_valasz = True
        b = bdb_bejegyzesek(adat, szam)
        if b:
            bej = b
            break
    if not volt_valasz:
        return None
    # a fejszóval azonos mássalhangzós címszavú bejegyzések előnyben (a strong_numbers mező bő: más szócikkek is hordozzák)
    azonos = [e for e in bej if massalhangzo(e.get('headword', '')) == fej]
    if azonos:
        bej = azonos
    bej = [e for e in bej if fa_utak(e)]
    utak = collections.defaultdict(list)
    bejegyzes = collections.defaultdict(set)   # vers → a bejegyzések, amelyekben áll
    for e in sorted(bej, key=lambda e: e.get('rid') or ''):
        h = homonima(e.get('headword', ''))
        for v, p in fa_utak(e):
            utak[v].append(ut_szoveg(h, p))
            bejegyzes[v].add(e.get('rid') or '')
    tobb = len({homonima(e.get('headword', '')) for e in bej}) > 1
    return [e.get('rid') or '' for e in bej], utak, tobb, {v for v, r in bejegyzes.items() if len(r) > 1}


def tabla(cache, ts, strongok=None):
    vj = [r for r in tsv_sorok(VJ) if r['szurt'] == '0' and r['mt_vers'] and r['vers_feloldas'] != 'usz']
    if strongok is not None:
        vj = [r for r in vj if r['strong'] in strongok]
    st_be = sorted({r['strong'] for r in vj})
    fej = fejszavak(st_be)
    alak = tahot_alakok(st_be)
    per = collections.defaultdict(list)
    for r in vj:
        per[r['strong']].append(r)
    sorok = []
    for st in st_be:
        u = strong_utak(cache, st, fej.get(st, ''), alak.get(st, []))
        if u is None:
            continue  # nincs lekérdezve: nincs sor (a hiány nem ítélet)
        rid, utak, tobb, tobb_bej = u
        hanyadik = collections.Counter()
        osszes = collections.Counter(r['mt_vers'] for r in per[st])
        for r in sorted(per[st], key=lambda r: int(r['sorszam'])):
            v = r['mt_vers']
            k = hanyadik[v]
            hanyadik[v] += 1
            lst = utak.get(v, [])
            if not lst:
                ill, su = 'nincs', ''
            elif len(lst) == osszes[v] and v not in tobb_bej:  # bejegyzéseken át nincs k-adik illesztés
                ill, su = 'pontos', lst[k]
            else:
                ill, su = 'barmely', ';'.join(sorted(set(lst), key=lst.index))
            prov = 'scope=%s | forras=Sefaria /api/words (fejléc) | ts=%s' % (st, ts)
            sorok.append([st, r['sorszam'], v, ','.join(rid), ill + ('+hom' if tobb else ''), su, prov])
    return sorok


def tabla_ir(sorok, ts, ki=KI):
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/olvaso_szerver/bdb_sefaria_tanu.py tabla --ts %s — kézzel nem szerkesztendő (F196; séma: adat/SEMA.md 2.29.1).\n' % ts)
        f.write('# forras: Sefaria /api/words (BDB Dictionary, BDB Aramaic Dictionary; Brown–Driver–Briggs, Oxford 1906; közkincs, DT631), '
                'a nyers válaszok a repón kívül (D:\\pardes_tanu\\bdb\\api; lekérések: lekeresek.tsv) + adat/bdb_vers_jelentes.tsv '
                '(strong, sorszam, mt_vers). Csak a Sefaria-pont normalizált útvonala áll, Sefaria-szöveg nem.\n')
        f.write('\t'.join(OSZLOPOK) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')


def tanu_betolt(ut=KI):
    """{(strong, sorszam): (mt_vers, illesztes, sefaria_ut)} — a 2.29 generátora ezt olvassa (kapcsolóval)."""
    if not os.path.exists(ut):
        return {}
    return {(r['strong'], r['sorszam']): (r['mt_vers'], r['illesztes'], r['sefaria_ut']) for r in tsv_sorok(ut)}


def itelet(tanu, strong, sorszam, mt_vers, szakasz, resz, utvonal):
    t = tanu.get((strong, str(sorszam)))
    if not t or t[0] != mt_vers:
        return 'nincs'
    return osszevet(szakasz, resz, utvonal, t[2], t[1].endswith('+hom'))


# ------------------------------------------------------------------ mérés (seed-103)

def _m2():
    sys.path.insert(0, D)
    import m2_minta_osszevet as M2  # noqa: E402
    return M2


def seed103_helyes():
    """{azon: (kulcssor, helyes-e)} a F185_seed103_osszevet.py szabálya szerint (arany: A = B; az s103-N182 ítélete B)."""
    M2 = _m2()
    N = os.path.join(NAPLO, 'BDB_SZELETELO_M2_')
    kulcs = {r['azon']: r for r in M2.olvas(N + 'minta_seed103_kulcs.tsv')}
    A = {r['azon']: r for r in M2.olvas(N + 'seed103_kitoltott_A.tsv')}
    ITELET = {'N182': ('Qal/1/c', '')}
    ki = {}
    for az, k in kulcs.items():
        jp, resz = ITELET.get(az, (A[az]['jelentespont'], A[az].get('resz', '')))
        ksz, kseg = M2.bont(k['szakasz'], k['utvonal'])
        esz, eresz, eseg = M2.bont_kitoltott(jp, resz)
        ok = ksz == esz and (k['resz'] or '') == eresz and M2.fo(kseg) == M2.fo(eseg)
        ki[az] = (k, ok, jp, resz)
    return ki


def proba40(minta):
    """A 40 soros próba: mind a 19 `ketes` sor + 21 `biztos` (köztük az egyetlen hibás), rögzített véletlennel (seed 195)."""
    ketes = sorted(a for a, (k, ok, *_) in minta.items() if k['bizonyossag'] != 'biztos')
    biztos_hibas = sorted(a for a, (k, ok, *_) in minta.items() if k['bizonyossag'] == 'biztos' and not ok)
    biztos_jo = sorted(a for a, (k, ok, *_) in minta.items() if k['bizonyossag'] == 'biztos' and ok)
    rnd = random.Random(195)
    return ketes + biztos_hibas + sorted(rnd.sample(biztos_jo, 40 - len(ketes) - len(biztos_hibas)))


def meres(cache, csak40, ki_tsv=None):
    minta = seed103_helyes()
    azonok = proba40(minta) if csak40 else sorted(minta)
    strongok = {minta[a][0]['strong'] for a in azonok}
    tsor = tabla(cache, 'meres', strongok)
    tanu = {(s[0], s[1]): (s[2], s[4], s[5]) for s in tsor}
    szaml = collections.Counter()
    reszlet = []
    for a in azonok:
        k, ok, jp, resz = minta[a]
        it = itelet(tanu, k['strong'], k['sorszam'], k['mt_vers'], k['szakasz'], k['resz'], k['utvonal'])
        biz = k['bizonyossag'].split(':')[0]
        uj = 'ketes' if it == 'elter' else biz          # a bekötött szabály: csak az eltérés jelöl (DT-F196a)
        uj_a = biz if it == 'nincs' else ('biztos' if it == 'egyezik' else 'ketes')   # az elvetett változat: az egyezés emel
        szaml[('A', ok, uj_a)] += 1
        szaml[(ok, biz, it)] += 1
        t = tanu.get((k['strong'], k['sorszam']), ('', '', ''))
        reszlet.append([a, k['strong'], k['mt_vers'], '%s %s %s' % (k['szakasz'], k['resz'], k['utvonal']), '%s %s' % (jp, resz),
                        'helyes' if ok else 'HIBAS', k['bizonyossag'], it, uj, t[1], t[2]])
    return szaml, reszlet


def meres_kiir(szaml, reszlet, cim):
    A ={k: v for k, v in szaml.items() if k[0] == 'A'}
    szaml = {k: v for k, v in szaml.items() if k[0] != 'A'}
    n = sum(szaml.values())

    def c(**f):
        return sum(v for (ok, biz, it), v in szaml.items()
                   if all({'ok': ok, 'biz': biz, 'it': it}[x] == y for x, y in f.items()))
    print('== %s: %d pont' % (cim, n))
    print('tanú: egyezik %d, eltér %d, nincs adat %d' % (c(it='egyezik'), c(it='elter'), c(it='nincs')))
    print('helyes pont (%d): egyezik %d, eltér (TÉVES RIASZTÁS) %d, nincs %d' % (
        c(ok=True), c(ok=True, it='egyezik'), c(ok=True, it='elter'), c(ok=True, it='nincs')))
    print('  ebből biztos helyes (%d): téves riasztás %d' % (c(ok=True, biz='biztos'), c(ok=True, biz='biztos', it='elter')))
    print('  ebből ketes helyes (%d): egyezik (→ biztos, jó emelés) %d' % (c(ok=True, biz='ketes'), c(ok=True, biz='ketes', it='egyezik')))
    print('hibás pont (%d): eltér (MEGFOGVA) %d, egyezik (HIBÁS EMELÉS/MEGERŐSÍTÉS) %d, nincs %d' % (
        c(ok=False), c(ok=False, it='elter'), c(ok=False, it='egyezik'), c(ok=False, it='nincs')))
    # a bekötés utáni bizonyosság
    uj = collections.Counter()
    for r in reszlet:
        uj[(r[5], r[8])] += 1
    print('bekötés után: biztos sor %d (ebből hibás %d); ketes sor %d (ebből hibás %d)' % (
        uj[('helyes', 'biztos')] + uj[('HIBAS', 'biztos')], uj[('HIBAS', 'biztos')],
        uj[('helyes', 'ketes')] + uj[('HIBAS', 'ketes')], uj[('HIBAS', 'ketes')]))
    print('elvetett változat (az egyezés is emel): biztos sor %d (ebből hibás %d); ketes sor %d (ebből hibás %d)' % (
        A.get(('A', True, 'biztos'), 0) + A.get(('A', False, 'biztos'), 0), A.get(('A', False, 'biztos'), 0),
        A.get(('A', True, 'ketes'), 0) + A.get(('A', False, 'ketes'), 0), A.get(('A', False, 'ketes'), 0)))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('letolt')
    p.add_argument('--strong', nargs='*', default=[])
    p.add_argument('--minta', choices=['seed103'])
    p.add_argument('--mind', action='store_true', help='a 2.29 minden Strongja (≈ 8–9 ezer; órákig fut)')
    p.add_argument('--cache', default=CACHE)
    p = sub.add_parser('tabla')
    p.add_argument('--ts', required=True)
    p.add_argument('--cache', default=CACHE)
    p.add_argument('--ki', default=KI)
    p = sub.add_parser('meres')
    p.add_argument('--proba40', action='store_true')
    p.add_argument('--cache', default=CACHE)
    p.add_argument('--reszlet', metavar='TSV')
    a = ap.parse_args()
    if a.cmd == 'letolt':
        st = set(a.strong)
        if a.minta:
            st |= {r[0]['strong'] for r in seed103_helyes().values()}
        if a.mind:
            st |= {r['strong'] for r in tsv_sorok(VJ)}
        letolt(sorted(st), a.cache)
    elif a.cmd == 'tabla':
        sorok = tabla(a.cache, a.ts)
        tabla_ir(sorok, a.ts, a.ki)
        print('%d sor: %s' % (len(sorok), a.ki))
    else:
        szaml, reszlet = meres(a.cache, a.proba40)
        meres_kiir(szaml, reszlet, '40 soros próba' if a.proba40 else 'seed-103, 200 pont')
        if a.reszlet:
            with open(a.reszlet, 'w', encoding='utf-8', newline='\n') as f:
                f.write('\t'.join(['azon', 'strong', 'mt_vers', 'tabla_pont', 'arany', 'gepi', 'bizonyossag', 'tanu', 'uj_bizonyossag',
                                   'illesztes', 'sefaria_ut']) + '\n')
                for r in reszlet:
                    f.write('\t'.join(r) + '\n')


if __name__ == '__main__':
    main()
