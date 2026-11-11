#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/tanu_index.py -- F191: metaadat-szintu tanuindex a visszhang-reteg tanureteghez (szoveg nelkul).

Ket generalt tablat allit elo a repon kivuli nyers forrasbol (a nyers adat helye: D:\\pardes_tanu\\, nem a repo):

  epit-atyak   HistoricalChristianFaith/Commentaries-Database `commentaries.sqlite`
               -> konkordancia/Tanu_atyak_index.tsv
               (Karoli-alaku igehely-tartomany, atya, kategoria, ev, mu, forras-URL, HCF-azonosito; a `txt` oszlop,
               vagyis az idezet SZOVEGE NEM kerul bele)
  epit-rabb    Sefaria-Export `links/links*.csv` (CC-BY)
               -> konkordancia/Tanu_rabbinikus_index.tsv
               (Karoli-alaku igehely-tartomany -> rabbinikus hely: kategoria, mu, ref; szoveg nincs)
  keres        egy igehelyre (pl. "1Móz 3:17") a ket tabla fedo sorai
  minta        a HAMART-versek (1Móz 3:17, 4:7, 4:11, 6:5, 6:11) tanu-darabszamai

Szabalyok (CLAUDE.md): a repo-TSV-t `split('\\t')` olvassa es `'\\t'.join()` irja (a csv modul ott tilos). A Sefaria-links
fajlok viszont NEM repo-TSV-k, hanem idezojeles, vesszovel tagolt CSV-k (a mezokben vesszo van); azokat a csv modul olvassa --
ez a TSV-szabaly hatokoren kivul all, es ide nem ir semmit.

Verziozas: a HCF a KJV (angol) szamozast hasznalja, a Sefaria a masszoretikus (MT) szamozast; a Karoli szamozasa a
`konkordancia/Karoli_versmegfeleltetes.tsv` szerint (igehely_kjv / igehely_mt oszlop). Az atvezetes oszlop: egyezo | tabla |
tabla_hianyzik (OT, de a tablaban nincs: az azonos szam marad) | nt_feltetelezett (az UT-re nincs tabla: azonos szam).
"""
import argparse
import glob
import hashlib
import os
import re
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONYV_TABLA = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
VERSMEGF = os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
ATYAK_TSV = os.path.join(REPO, 'konkordancia', 'Tanu_atyak_index.tsv')
RABB_TSV = os.path.join(REPO, 'konkordancia', 'Tanu_rabbinikus_index.tsv')

MU_TSV = os.path.join(REPO, 'konkordancia', 'Tanu_atyak_mu.tsv')
# Üres igehely_veg = a tartomány egy verses (veg = kezdet); üres atvezetes = egyezo (a Károli-szám azonos a forrás számával).
ATYAK_OSZLOPOK = ['igehely_kezdet', 'igehely_veg', 'szelesseg', 'atya', 'ev', 'mu_id', 'hcf_id', 'atvezetes']
MU_OSZLOPOK = ['mu_id', 'atya', 'atya_kategoria', 'atya_kiegeszites', 'mu', 'forras_url']
RABB_OSZLOPOK = ['igehely_kezdet', 'igehely_veg', 'szelesseg', 'kategoria', 'mu', 'darab', 'hely', 'kapcsolat_tipus', 'atvezetes']

# HCF konyvnev (kisbetus, szokoz nelkul) -> STEPBible-rovidites. Az apokrif konyvek (wisdom, sirach, tobit, ...) nincsenek benne:
# a Karoli-kanonban nincsenek, ezert az index nem veszi fel oket (a darabszam a README-ben).
HCF_KONYV = {
    'genesis': 'Gen', 'exodus': 'Exo', 'leviticus': 'Lev', 'numbers': 'Num', 'deuteronomy': 'Deu', 'joshua': 'Jos',
    'judges': 'Jdg', 'ruth': 'Rut', '1samuel': '1Sa', '2samuel': '2Sa', '1kings': '1Ki', '2kings': '2Ki',
    '1chronicles': '1Ch', '2chronicles': '2Ch', 'ezra': 'Ezr', 'nehemiah': 'Neh', 'esther': 'Est', 'job': 'Job',
    'psalms': 'Psa', 'proverbs': 'Pro', 'ecclesiastes': 'Ecc', 'songofsolomon': 'Sng', 'isaiah': 'Isa', 'jeremiah': 'Jer',
    'lamentations': 'Lam', 'ezekiel': 'Ezk', 'daniel': 'Dan', 'hosea': 'Hos', 'joel': 'Jol', 'amos': 'Amo',
    'obadiah': 'Oba', 'jonah': 'Jon', 'micah': 'Mic', 'nahum': 'Nam', 'habakkuk': 'Hab', 'zephaniah': 'Zep',
    'haggai': 'Hag', 'zechariah': 'Zec', 'malachi': 'Mal',
    'matthew': 'Mat', 'mark': 'Mrk', 'luke': 'Luk', 'john': 'Jhn', 'acts': 'Act', 'romans': 'Rom',
    '1corinthians': '1Co', '2corinthians': '2Co', 'galatians': 'Gal', 'ephesians': 'Eph', 'philippians': 'Php',
    'colossians': 'Col', '1thessalonians': '1Th', '2thessalonians': '2Th', '1timothy': '1Ti', '2timothy': '2Ti',
    'titus': 'Tit', 'philemon': 'Phm', 'hebrews': 'Heb', 'james': 'Jas', '1peter': '1Pe', '2peter': '2Pe',
    '1john': '1Jn', '2john': '2Jn', '3john': '3Jn', 'jude': 'Jud', 'revelation': 'Rev',
}

# Sefaria angol konyvnev -> STEPBible-rovidites (csak a Tanakh).
SEFARIA_KONYV = {
    'Genesis': 'Gen', 'Exodus': 'Exo', 'Leviticus': 'Lev', 'Numbers': 'Num', 'Deuteronomy': 'Deu', 'Joshua': 'Jos',
    'Judges': 'Jdg', 'Ruth': 'Rut', 'I Samuel': '1Sa', 'II Samuel': '2Sa', 'I Kings': '1Ki', 'II Kings': '2Ki',
    'I Chronicles': '1Ch', 'II Chronicles': '2Ch', 'Ezra': 'Ezr', 'Nehemiah': 'Neh', 'Esther': 'Est', 'Job': 'Job',
    'Psalms': 'Psa', 'Proverbs': 'Pro', 'Ecclesiastes': 'Ecc', 'Song of Songs': 'Sng', 'Isaiah': 'Isa',
    'Jeremiah': 'Jer', 'Lamentations': 'Lam', 'Ezekiel': 'Ezk', 'Daniel': 'Dan', 'Hosea': 'Hos', 'Joel': 'Jol',
    'Amos': 'Amo', 'Obadiah': 'Oba', 'Jonah': 'Jon', 'Micah': 'Mic', 'Nahum': 'Nam', 'Habakkuk': 'Hab',
    'Zephaniah': 'Zep', 'Haggai': 'Hag', 'Zechariah': 'Zec', 'Malachi': 'Mal',
}

# Sefaria top-level kategoria -> kivett rabbinikus kategoria (a tobbi: Tanakh/Reference/Jewish Thought/Chasidut/Halakhah/
# Kabbalah/Musar/Liturgy/Responsa/Second Temple/_unlisted NEM rabbinikus tanu ebben az indexben). A Targum a
# `Conection Type == targum` sorokbol jon (mindket oldal Tanakh-kategoriaju).
RABB_KATEGORIAK = ('Midrash', 'Talmud', 'Mishnah', 'Tosefta')


class Kulcs:
    """Karoli-kulcs: a konyvsorrend, a fejezetek verszama es a KJV/MT -> Karoli atvezetes (versmegfeleltetes.tsv)."""

    def __init__(self):
        self.sorrend = []          # STEP-rovidites sorrendben
        self.step2k = {}           # STEP -> Karoli rovidites
        self.k2step = {}
        with open(KONYV_TABLA, encoding='utf-8') as f:
            next(f)
            for sor in f:
                m = sor.rstrip('\n').split('\t')
                if len(m) < 2 or not m[0]:
                    continue
                self.sorrend.append(m[0])
                self.step2k[m[0]] = m[1]
                self.k2step[m[1]] = m[0]
        self.rend = {k: i for i, k in enumerate(self.step2k.values())}
        self.mtmax = {}            # (Karoli-konyv, MT-fejezet) -> utolso MT-vers (az igehely_mt oszlop; ures = a Karoli-szam)
        self.chmax = {}            # (Karoli-konyv, fejezet) -> utolso vers (OT: a versmegfeleltetes tablabol)
        self.kjv2k = {}            # (Karoli-konyv, 'f:v') -> Karoli 'f:v'
        self.mt2k = {}
        self.ot = set()
        with open(VERSMEGF, encoding='utf-8') as f:
            for sor in f:
                if sor.startswith('#') or sor.startswith('igehely_karoli'):
                    continue
                m = sor.rstrip('\n').split('\t')
                if len(m) < 3 or not m[0]:
                    continue
                konyv, _, fv = m[0].rpartition(' ')
                fej, _, vers = fv.partition(':')
                self.ot.add(konyv)
                ch = (konyv, int(fej))
                self.chmax[ch] = max(self.chmax.get(ch, 0), int(vers))
                if m[1]:
                    self.kjv2k.setdefault((konyv, m[1]), fv)
                if m[2]:
                    self.mt2k.setdefault((konyv, m[2]), fv)
                mf, _, mv = (m[2] or fv).partition(':')
                if mf.isdigit() and mv.isdigit():
                    mc = (konyv, int(mf))
                    self.mtmax[mc] = max(self.mtmax.get(mc, 0), int(mv))

    def szelesseg(self, konyv, f1, v1, f2, v2):
        """A Karoli-szamozasu tartomany verszama (a fejezethatart a chmax-szal szamolva; ismeretlen fejezet: csak a vegpont)."""
        if (f1, v1) == (f2, v2):
            return 1
        if f1 == f2:
            return max(1, v2 - v1 + 1)
        n = self.chmax.get((konyv, f1))
        if n is None:
            return 2
        s = n - v1 + 1
        for f in range(f1 + 1, f2):
            s += self.chmax.get((konyv, f), 0)
        return s + v2

    def atvezet(self, konyv, f, v, tabla):
        """(f, v, jel): a (KJV vagy MT) szam Karoli-szama. tabla: 'kjv' | 'mt'."""
        if konyv not in self.ot:
            return f, v, 'nt_feltetelezett'
        t = self.kjv2k if tabla == 'kjv' else self.mt2k
        k = t.get((konyv, '%d:%d' % (f, v)))
        if k is None:
            # az azonos szamu Karoli-vers letezik-e: ha igen, egyezo; ha nem, a tabla hianyzik
            if (konyv, f) in self.chmax and v <= self.chmax[(konyv, f)]:
                return f, v, 'egyezo'
            return f, v, 'tabla_hianyzik'
        kf, kv = (int(x) for x in k.split(':'))
        return kf, kv, ('egyezo' if (kf, kv) == (f, v) else 'tabla')

    def rendkulcs(self, konyv, f, v):
        return (self.rend.get(konyv, 999), f, v)


def igehely_str(konyv, f, v):
    return '%s %d:%d' % (konyv, f, v)


def igehely_parse(s):
    """'1Móz 3:17' -> ('1Móz', 3, 17); hibas alakra ValueError."""
    m = re.match(r'^(\S+) (\d+):(\d+)$', s.strip())
    if not m:
        raise ValueError('hibas igehely: %r (varhato: "1Móz 3:17")' % s)
    return m.group(1), int(m.group(2)), int(m.group(3))


def tisztit(s):
    return s.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').strip()


def tisztit_url(u):
    """A Google Books-URL `dq=`/`q=` parametere idezetszoveget hordoz: kiveszi (a szoveg nem kerul az indexbe)."""
    u = tisztit(u)
    if '?' not in u:
        return u
    alap, _, qs = u.partition('?')
    resz = [x for x in qs.split('&') if not x.startswith(('dq=', 'q='))]
    return alap + ('?' + '&'.join(resz) if resz else '')


def sha256_fajl(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def ir_tsv(path, fejlec_sorok, oszlopok, sorok):
    """Ellenorzott irás: minden sor oszlopszama egyezik, nincs tab/sortores a mezoben (a tisztit() mar kivette)."""
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for h in fejlec_sorok:
            f.write(h + '\n')
        f.write('\t'.join(oszlopok) + '\n')
        for r in sorok:
            assert len(r) == len(oszlopok), r
            f.write('\t'.join(str(x) for x in r) + '\n')


# ---------------------------------------------------------------- HCF (egyhazatyak)

def hely_dekod(n):
    """HCF location_start/end: fejezet*1_000_000 + vers."""
    return n // 1000000, n % 1000000


def epit_atyak(sqlite_path, ki, ts):
    k = Kulcs()
    con = sqlite3.connect('file:%s?mode=ro' % sqlite_path.replace('\\', '/'), uri=True)
    meta = {n: (kat, ev) for n, ev, kat in con.execute('select name, default_year, father_category from father_meta')}
    sorok, kulcsok, mu_kulcsok = [], [], set()
    kimarad = {'nem_kanonikus_konyv': 0, 'fordított_tartomany': 0, 'nincs_karoli_vers': 0}
    kimaradt_konyvek = {}
    for (cid, atya, ts_ev, konyv, ls, le, url, cim, kieg) in con.execute(
            'select id, father_name, ts, book, location_start, location_end, source_url, source_title, '
            'append_to_author_name from commentary'):
        step = HCF_KONYV.get(konyv)
        if step is None:
            kimarad['nem_kanonikus_konyv'] += 1
            kimaradt_konyvek[konyv] = kimaradt_konyvek.get(konyv, 0) + 1
            continue
        kk = k.step2k[step]
        f1, v1 = hely_dekod(ls)
        f2, v2 = hely_dekod(le)
        if (f2, v2) < (f1, v1):
            kimarad['fordított_tartomany'] += 1
            continue
        if v1 == 0:
            v1 = 1
        if v2 >= 999 or v2 == 0:
            v2 = k.chmax.get((kk, f2), v2 if v2 else 1)
        kf1, kv1, j1 = k.atvezet(kk, f1, v1, 'kjv')
        kf2, kv2, j2 = k.atvezet(kk, f2, v2, 'kjv')
        if (kf2, kv2) < (kf1, kv1):       # az atvezetes megfordította: a tartomany egy verses lesz
            kf2, kv2 = kf1, kv1
        if kk in k.ot and kv1 > k.chmax.get((kk, kf1), 0):
            kimarad['nincs_karoli_vers'] += 1     # pl. Dán 13–14, Eszt 10:6 (görög kiegészítés), Jób 38:39–41: nincs ilyen Károli-vers
            continue
        jel = j1 if j1 == j2 else ('tabla' if 'tabla' in (j1, j2) else j1 if j1 != 'egyezo' else j2)
        kat = meta.get(atya, ('', ''))[0]
        mkulcs = (tisztit(atya), tisztit(kat), tisztit(kieg or ''), tisztit(cim or ''), tisztit_url(url or ''))
        mu_kulcsok.add(mkulcs)
        sorok.append([igehely_str(kk, kf1, kv1), '' if (kf1, kv1) == (kf2, kv2) else igehely_str(kk, kf2, kv2),
                      k.szelesseg(kk, kf1, kv1, kf2, kv2), mkulcs[0], '' if ts_ev is None else ts_ev, mkulcs,
                      cid[:10], '' if jel == 'egyezo' else jel])
        kulcsok.append(k.rendkulcs(kk, kf1, kv1) + (k.rendkulcs(kk, kf2, kv2), atya, cid))
    mu_lista = sorted(mu_kulcsok)
    mu_id = {m: i + 1 for i, m in enumerate(mu_lista)}
    for r in sorok:
        r[5] = mu_id[r[5]]
    assert len({r[6] for r in sorok}) == len(sorok), 'a 10 hexa hcf_id nem egyedi'
    con.close()
    ido = sorted(range(len(sorok)), key=lambda i: kulcsok[i])
    sorok = [sorok[i] for i in ido]
    fej = [
        '# GENERÁLT: eszkozok/tanu_index.py epit-atyak — kézzel nem szerkesztendő. Szöveg (a HCF `txt` oszlopa) NINCS benne.',
        '# Egyházatyai / történeti tanúk metaadat-indexe: Károli-alakú igehely-tartomány → atya, év, mu_id (→ Tanu_atyak_mu.tsv: '
        'kategória, mű, forrás-URL). Üres igehely_veg = egy verses; üres atvezetes = egyezo.',
        '# forras=HistoricalChristianFaith/Commentaries-Database release `latest` commentaries.sqlite (https://github.com/'
        'HistoricalChristianFaith/Commentaries-Database/releases/download/latest/commentaries.sqlite) | '
        'sha256=%s | letoltve=2026-11-11' % sha256_fajl(sqlite_path),
        '# licenc: a kompiláció (mappaszerkezet, fájlnevek, metaadatok, szkript) PUBLIC DOMAIN DEDICATION; az idézetszövegek '
        'egy része jogvédett (fair use) — ezért a szöveg nem kerül ide. Az index tény-adat; l. konkordancia/Tanu_index_README.md.',
        '# proveniencia: scope=commentary(%d sor)→index | forras=HCF commentaries.sqlite | ts=%s ; sorszintű visszakeresés: hcf_id'
        % (len(sorok), ts),
        '# igehely: Károli-szám (a HCF KJV-számát a Karoli_versmegfeleltetes.tsv igehely_kjv oszlopa szerint átvezetve); a '
        'szelesseg a tartomány verszáma (1 = pontos egyvers).',
    ]
    ir_tsv(ki, fej, ATYAK_OSZLOPOK, sorok)
    mu_ki = os.path.join(os.path.dirname(ki), 'Tanu_atyak_mu.tsv')
    mufej = ['# GENERÁLT: eszkozok/tanu_index.py epit-atyak — kézzel nem szerkesztendő. A Tanu_atyak_index.tsv mu_id-jének feloldása '
             '(atya, mű, forrás-URL). Szöveg nincs. Forrás, licenc, proveniencia: ugyanaz, mint a Tanu_atyak_index.tsv fejlécében.']
    ir_tsv(mu_ki, mufej, MU_OSZLOPOK, [[i + 1] + list(m) for i, m in enumerate(mu_lista)])
    return len(sorok), kimarad, kimaradt_konyvek


# ---------------------------------------------------------------- Sefaria (rabbinikus)

_REF = re.compile(r'^(?P<konyv>.+?) (?P<a>\d+)(?::(?P<b>\d+))?(?:-(?P<c>\d+)(?::(?P<d>\d+))?)?$')


def sefaria_tanakh_ref(s, k):
    """'Genesis 3:17-4:2' -> (step, f1, v1, f2, v2) MT-szamozassal; None, ha nem Tanakh-ref vagy nem ertelmezheto."""
    if s in SEFARIA_KONYV:      # egesz konyv
        step = SEFARIA_KONYV[s]
        kk = k.step2k[step]
        fs = [f for (b, f) in k.mtmax if b == kk]
        if not fs:
            return None
        return step, 1, 1, max(fs), k.mtmax[(kk, max(fs))]
    m = _REF.match(s)
    if not m or m.group('konyv') not in SEFARIA_KONYV:
        return None
    step = SEFARIA_KONYV[m.group('konyv')]
    kk = k.step2k[step]
    f1 = int(m.group('a'))
    v1 = int(m.group('b')) if m.group('b') else None
    c, d = m.group('c'), m.group('d')
    if c is None:
        f2, v2 = f1, v1
    elif d is not None:
        f2, v2 = int(c), int(d)
    elif v1 is None:
        f2, v2 = int(c), None       # fejezettol fejezetig
    else:
        f2, v2 = f1, int(c)         # f:v1-v2
    if v1 is None:
        v1 = 1
    if v2 is None:
        v2 = k.mtmax.get((kk, f2))      # MT-fejezethossz (a Karoli-fejezet hossza Joel/Mal/Zsolt stb. esetén más)
        if v2 is None:
            return None
    return step, f1, v1, f2, v2


ELOFORDULASOK = os.path.join(REPO, 'adat', 'elofordulasok.tsv')


def motivum_versek(k, path=ELOFORDULASOK):
    """A lexikonmotivumok igehelyei (adat/elofordulasok.tsv `igehely`, `Konyv f:v` vagy `Konyv f:v1-v2`) egyes versekke
    bontva, rendkulcs szerint rendezve. Vissza: (rendezett kulcslista, ertelmezhetetlen igehelyek listaja)."""
    kulcsok, rossz = set(), []
    oszl = None
    with open(path, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#') or not sor.strip():
                continue
            m = sor.rstrip('\n').split('\t')
            if oszl is None:
                oszl = m.index('igehely') if 'igehely' in m else 1
                continue
            g = re.match(r'^(\S+) (\d+):(\d+)(?:-(\d+))?$', m[oszl])
            if not g or g.group(1) not in k.rend:
                rossz.append(m[oszl])
                continue
            v1 = int(g.group(3))
            v2 = int(g.group(4)) if g.group(4) else v1
            for v in range(v1, v2 + 1):
                kulcsok.add(k.rendkulcs(g.group(1), int(g.group(2)), v))
    return sorted(kulcsok), rossz


def tartomany_erint(kulcsok, a, b):
    """Van-e a rendezett `kulcsok` kozott olyan, amely az [a, b] tartomanyba esik."""
    import bisect
    i = bisect.bisect_left(kulcsok, a)
    return i < len(kulcsok) and kulcsok[i] <= b


def epit_rabb(links_mappa, ki, ts, motivum_szukites=True):
    import csv     # csak a Sefaria-CSV-hez (l. a modul docstringje)
    k = Kulcs()
    fajlok = sorted(glob.glob(os.path.join(links_mappa, 'links*.csv')), key=lambda p: int(re.search(r'links(\d+)', p).group(1)))
    if not fajlok:
        raise SystemExit('nincs links*.csv a %s mappaban' % links_mappa)
    kulcsok, lathato = [], {}
    stat = {'olvasott': 0, 'rabbinikus_sor': 0, 'ertelmezhetetlen_ref': 0, 'ismetlodo': 0, 'hatokoron_kivul': 0}
    mkulcsok = None
    if motivum_szukites:
        mkulcsok, mrossz = motivum_versek(k)
        if mrossz:
            raise SystemExit('az elofordulasok.tsv nem ertelmezheto igehelyei: %s' % mrossz[:10])
    ertelmezhetetlen = {}
    for p in fajlok:
        with open(p, encoding='utf-8', newline='') as fh:
            r = csv.reader(fh)
            next(r)
            for row in r:
                stat['olvasott'] += 1
                if len(row) != 7:
                    continue
                c1, c2, tip, t1, t2, k1, k2 = row
                if tip == 'targum' and k1 == 'Tanakh' and k2 == 'Tanakh':
                    # a Tanakh-oldal az, amelyik egy csupasz konyvnev; a masik a targum-mu
                    if t1 in SEFARIA_KONYV and t2 not in SEFARIA_KONYV:
                        tan, mas, mt, kat = c1, c2, t2, 'Targum'
                    elif t2 in SEFARIA_KONYV and t1 not in SEFARIA_KONYV:
                        tan, mas, mt, kat = c2, c1, t1, 'Targum'
                    else:
                        continue
                elif k1 == 'Tanakh' and k2 in RABB_KATEGORIAK and t1 in SEFARIA_KONYV:
                    tan, mas, mt, kat = c1, c2, t2, k2
                elif k2 == 'Tanakh' and k1 in RABB_KATEGORIAK and t2 in SEFARIA_KONYV:
                    tan, mas, mt, kat = c2, c1, t1, k1
                else:
                    continue
                stat['rabbinikus_sor'] += 1
                pr = sefaria_tanakh_ref(tan, k)
                if pr is None:
                    stat['ertelmezhetetlen_ref'] += 1
                    if len(ertelmezhetetlen) < 15:
                        ertelmezhetetlen[tan] = ertelmezhetetlen.get(tan, 0) + 1
                    continue
                step, f1, v1, f2, v2 = pr
                kk = k.step2k[step]
                kf1, kv1, j1 = k.atvezet(kk, f1, v1, 'mt')
                kf2, kv2, j2 = k.atvezet(kk, f2, v2, 'mt')
                if (kf2, kv2) < (kf1, kv1):
                    kf2, kv2 = kf1, kv1
                if mkulcsok is not None and not tartomany_erint(mkulcsok, k.rendkulcs(kk, kf1, kv1), k.rendkulcs(kk, kf2, kv2)):
                    stat['hatokoron_kivul'] += 1
                    continue
                jel = j1 if j1 == j2 else ('tabla' if 'tabla' in (j1, j2) else j1 if j1 != 'egyezo' else j2)
                gk = (igehely_str(kk, kf1, kv1), '' if (kf1, kv1) == (kf2, kv2) else igehely_str(kk, kf2, kv2),
                      k.szelesseg(kk, kf1, kv1, kf2, kv2), kat, tisztit(mt), tisztit(tip), '' if jel == 'egyezo' else jel)
                ref = tisztit(mas)
                csop = lathato.setdefault(gk, [])
                if ref in csop:
                    stat['ismetlodo'] += 1
                    continue
                csop.append(ref)
                if len(csop) == 1:
                    kulcsok.append((k.rendkulcs(kk, kf1, kv1), k.rendkulcs(kk, kf2, kv2), kat, mt, gk))
    sorok = []
    kulcs_gk = []
    for (a, b, kat, mt, gk) in kulcsok:
        kulcs_gk.append((a, b, kat, mt, gk))
    kulcs_gk.sort()
    for (a, b, kat, mt, gk) in kulcs_gk:
        refek = lathato[gk]
        sorok.append([gk[0], gk[1], gk[2], gk[3], gk[4], len(refek), ' ; '.join(refek), gk[5], gk[6]])
    sha = ' '.join('%s=%s' % (os.path.basename(p), sha256_fajl(p)[:16]) for p in fajlok)
    fej = [
        '# GENERÁLT: eszkozok/tanu_index.py epit-rabb — kézzel nem szerkesztendő. Szöveg NINCS benne, csak a hely-mutató.',
        '# Rabbinikus tanúk helymutatója: Károli-alakú igehely-tartomány → rabbinikus hely (kategória, mű, ref). Kategóriák: '
        'Midrash, Talmud, Mishnah, Tosefta (a Sefaria top-level kategóriája) és Targum (kapcsolat-típus `targum`).',
        '# forras=Sefaria-Export links/links0.csv … links%d.csv (https://storage.googleapis.com/sefaria-export/links/) | '
        'sha256(elso16)=%s | letoltve=2026-11-11' % (len(fajlok) - 1, sha),
        '# licenc: CC BY — „Sefaria’s links dataset … is released under the CC-BY license” (https://developers.sefaria.org/docs/'
        'usage-of-our-name-and-logo, 2026-11-11); forrásmegjelölés: Sefaria.org; a változás (szűrés, Károli-átvezetés) jelezve.',
        '# hatokor: %s' % ('a lexikonmotívumok igehelyei (adat/elofordulasok.tsv, %d vers): csak az ezekkel átfedő tartományok '
                           '(a teljes Tanakh ~24 MB; N-F191a)' % len(mkulcsok) if mkulcsok is not None else 'a teljes Tanakh'),
        '# proveniencia: scope=links(%d olvasott sor, %d rabbinikus Tanakh-sor, %d hatókörön kívül, %d nem értelmezhető Tanakh-ref) | '
        'forras=Sefaria-Export links | ts=%s' % (stat['olvasott'], stat['rabbinikus_sor'], stat['hatokoron_kivul'],
                                                  stat['ertelmezhetetlen_ref'], ts),
        '# igehely: Károli-szám (a Sefaria MT-számát a Karoli_versmegfeleltetes.tsv igehely_mt oszlopa szerint átvezetve); a '
        'szelesseg a tartomány verszáma (1 = pontos egyvers; a nagy értékű sorok fejezet- vagy szakaszszintű kapcsolatok).',
    ]
    ir_tsv(ki, fej, RABB_OSZLOPOK, sorok)
    return len(sorok), stat, ertelmezhetetlen


# ---------------------------------------------------------------- lekerdezes

def betolt(path):
    """A repo-TSV beolvasasa: split('\\t'); a '#' sorok kimaradnak; vissza: (oszlopok, sorok mint dict)."""
    oszl, sorok = None, []
    with open(path, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n')
            if sor.startswith('#') or not sor:
                continue
            m = sor.split('\t')
            if oszl is None:
                oszl = m
                continue
            sorok.append(dict(zip(oszl, m)))
    return oszl, sorok


def fedo_sorok(sorok, igehely, k, max_szelesseg=None):
    """Az igehelyet tartalmazo (fedo) sorok; max_szelesseg: csak az annal nem szelesebb tartomanyok."""
    konyv, f, v = igehely_parse(igehely)
    kulcs = k.rendkulcs(konyv, f, v)
    ered = []
    for s in sorok:
        k1 = igehely_parse(s['igehely_kezdet'])
        k2 = igehely_parse(s['igehely_veg'] or s['igehely_kezdet'])
        if k1[0] != konyv:
            continue
        if k.rendkulcs(*k1) <= kulcs <= k.rendkulcs(*k2):
            if max_szelesseg is None or int(s['szelesseg']) <= max_szelesseg:
                ered.append(s)
    return ered


HAMART_VERSEK = ['1Móz 3:17', '1Móz 4:7', '1Móz 4:11', '1Móz 6:5', '1Móz 6:11']


def minta(atyak_path=ATYAK_TSV, rabb_path=RABB_TSV, versek=HAMART_VERSEK):
    k = Kulcs()
    _, a = betolt(atyak_path)
    _, r = betolt(rabb_path)
    sorok = []
    for v in versek:
        pont = [s for s in a if s['igehely_kezdet'] == v and not s['igehely_veg']]
        fedo = fedo_sorok(a, v, k)
        fedo_kicsi = fedo_sorok(a, v, k, max_szelesseg=10)
        rp = [s for s in r if s['igehely_kezdet'] == v and not s['igehely_veg']]
        rf = fedo_sorok(r, v, k, max_szelesseg=10)
        kat = {}
        for s in rp:
            kat[s['kategoria']] = kat.get(s['kategoria'], 0) + 1
        sorok.append({
            'vers': v,
            'atya_pontos_sor': len(pont), 'atya_pontos_kulonbozo': len({s['atya'] for s in pont}),
            'atya_fedo_max10_sor': len(fedo_kicsi), 'atya_fedo_max10_kulonbozo': len({s['atya'] for s in fedo_kicsi}),
            'atya_fedo_osszes_kulonbozo': len({s['atya'] for s in fedo}),
            'rabb_pontos_sor': len(rp), 'rabb_pontos_kulonbozo_mu': len({s['mu'] for s in rp}), 'rabb_kategoriak': kat,
            'rabb_fedo_max10_sor': len(rf), 'rabb_fedo_max10_kulonbozo_mu': len({s['mu'] for s in rf}),
        })
    return sorok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    sub = ap.add_subparsers(dest='parancs', required=True)
    a = sub.add_parser('epit-atyak')
    a.add_argument('--sqlite', required=True)
    a.add_argument('--ki', default=ATYAK_TSV)
    a.add_argument('--ts', default='2026-11-11')
    b = sub.add_parser('epit-rabb')
    b.add_argument('--links-mappa', required=True)
    b.add_argument('--ki', default=RABB_TSV)
    b.add_argument('--ts', default='2026-11-11')
    b.add_argument('--teljes', action='store_true', help='a motívum-szűkítés nélkül, a teljes Tanakh (~24 MB)')
    c = sub.add_parser('keres')
    c.add_argument('igehely')
    c.add_argument('--max-szelesseg', type=int, default=None)
    sub.add_parser('minta')
    arg = ap.parse_args(argv)
    if arg.parancs == 'epit-atyak':
        n, kim, konyvek = epit_atyak(arg.sqlite, arg.ki, arg.ts)
        print('Tanu_atyak_index: %d sor; kimaradt: %s; kimaradt konyvek: %s' % (n, kim, konyvek))
    elif arg.parancs == 'epit-rabb':
        n, st, er = epit_rabb(arg.links_mappa, arg.ki, arg.ts, motivum_szukites=not arg.teljes)
        print('Tanu_rabbinikus_index: %d sor; %s; ertelmezhetetlen ref minta: %s' % (n, st, er))
    elif arg.parancs == 'keres':
        k = Kulcs()
        for nev, p in (('atyak', ATYAK_TSV), ('rabbinikus', RABB_TSV)):
            _, sorok = betolt(p)
            for s in fedo_sorok(sorok, arg.igehely, k, arg.max_szelesseg):
                print(nev + '\t' + '\t'.join(s.values()))
    elif arg.parancs == 'minta':
        for s in minta():
            print(s)


if __name__ == '__main__':
    main()
