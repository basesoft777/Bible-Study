"""Olvasói pilot, M2b: a `pardes.db` (#79) mérése a pilot két szakaszán.

Csak olvas (`mode=ro`), a meglévő adatbázist méri, nem építi újra. A pilot fő kimenete (adat.py → JSON →
HTML) továbbra is a TSV-kből készül; ez a szkript azt méri, mit tudna adni az adatbázis ugyanennek a lapnak.

  D1  blokk-lefedettség: melyik blokk állítható elő csak a pardes.db-ből, melyikhez kell TSV
  D2  egyezés: a TSV-ből (adat.py JSON-ja) és a pardes.db-ből előállított blokkok versenként / szavanként
  D3  lekérdezési idő: vers-lap és szó-lap adata, medián és p95, hideg és meleg gyorsítótár
  D4  szükséges részhalmaz mérete (naplok/SQLITE_EPIT_meres.md táblánkénti mérete alapján)
  D5  frissesség: meta sorszám/hash a tábla tartalmával, a forrás-TSV-k állapota (git) az építés időpontjához képest

Ha nincs pardes.db, a kimenet „nem mérhető”, nem hiba.
Futtatás: python eszkozok/olvaso_pilot/db_meres.py [--db pardes.db] [--szakasz "1Móz 1-25"] ... [--kimenet KÖNYVTÁR]
A --szakasz többször megadható (alapból "1Móz 1-25" és "Zsolt 22"); az adat.py JSON-ját ideiglenes könyvtárba állítja elő,
vagy a --json-könyvtár/<szakasz-azonosító>/olvaso_pilot.json fájlt használja."""
import argparse
import datetime
import gzip
import hashlib
import json
import os
import platform
import re
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
import unicodedata
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(os.path.dirname(D)).replace('\\', '/') + '/'
SZAKASZOK = ['1Móz 1-25', 'Zsolt 22']


def alap_db():
    """A pardes.db alapértelmezett helye: a munkafa gyökere; külön `git worktree`-ben a fő munkamásolat (a pardes.db .gitignore-ban van)."""
    ut = GY + 'pardes.db'
    if os.path.exists(ut):
        return ut
    kozos = subprocess.run(['git', '-C', GY, 'rev-parse', '--git-common-dir'], capture_output=True, text=True, encoding='utf-8').stdout.strip()
    if kozos:
        fo = os.path.dirname(os.path.abspath(os.path.join(GY, kozos))).replace(chr(0x5C), '/') + '/pardes.db'
        if os.path.exists(fo):
            return fo
    return ut


def azonosito(szakasz):
    ascii_ = ''.join(c for c in unicodedata.normalize('NFD', szakasz) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^A-Za-z0-9]+', '_', ascii_).strip('_').lower()


def hnorm(s):
    m = re.match(r'^([HG])0*(\d+)([A-Z]?)$', (s or '').strip().upper())
    return '%s%04d' % (m.group(1), int(m.group(2))) if m else None


def csupasz_alak(szo):
    return re.sub(r'[^\wáéíóöőúüűÁÉÍÓÖŐÚÜŰ-]', '', szo).lower()


def tisztit_tbesg(jel):
    jel = re.sub(r'<ref=[^>]*>', '', jel)
    jel = re.sub(r'<BR\s*/?>', '\n', jel)
    return re.sub(r'<[^>]+>', '', jel).replace('__', '').strip()


def kapcsolat(ut):
    return sqlite3.connect('file:%s?mode=ro' % ut.replace('\\', '/'), uri=True)


def meta(con):
    return {r[0]: r[1] for r in con.execute('SELECT kulcs, ertek FROM meta')}


# ----------------------------------------------------------------------------------------
# A lap adata a pardes.db-ből (ugyanazok a blokkok, mint az adat.py JSON-jában)
# ----------------------------------------------------------------------------------------
def db_vers(con, ig):
    r = con.execute('SELECT karoli_szoveg FROM vers WHERE igehely=?', (ig,)).fetchone()
    par = defaultdict(list)
    for hs, st, bz in con.execute('SELECT hu_sorszam, strong, bizonyossag FROM token_par WHERE igehely=? ORDER BY hu_sorszam, er_sorszam', (ig,)):
        par[hs].append((st, bz))
    heber = [(hnorm(sn) or sn, alak, kiej) for sn, alak, kiej in con.execute(
        "SELECT strong_nyers, alak, kiejtes FROM token_eredeti WHERE igehely=? AND nyelv='H' ORDER BY sorszam", (ig,))]
    tsk = con.execute('SELECT cel_igehely, votes FROM tsk WHERE igehely=? ORDER BY votes DESC', (ig,)).fetchall()
    kh_db = con.execute('SELECT COUNT(*) FROM kh WHERE igehely=?', (ig,)).fetchone()[0]
    sz = con.execute('SELECT osztaly, kjv_igehely, mt_igehely, megfeleltetes_forras FROM vers_szamozas WHERE igehely=?', (ig,)).fetchone()
    lxx = [x[0] for x in con.execute('SELECT DISTINCT lxx_igehely FROM lxx_versszintu_parok WHERE igehely=?', (ig,))]
    ubs = {}
    for st in {h[0] for h in heber}:
        ubs[st] = sorted(x[0] for x in con.execute(
            'SELECT DISTINCT r.lexid FROM ubs_dbh_referenciak r JOIN ubs_dbh_jelentesek j ON j.lexid=r.lexid '
            'WHERE r.igehely=? AND r.strong=?', (ig, st)))
    return {'karoli': r[0] if r else None, 'par': dict(par), 'heber': heber, 'tsk': tsk, 'kh_db': kh_db,
            'versszam': sz, 'lxx': lxx, 'ubs': ubs}


def db_szo(con, strong):
    sz = con.execute('SELECT szoto, kiejtes, szofaj, jelentes FROM strong_szotar WHERE strong=?', (strong,)).fetchone()
    bdb_en = con.execute('SELECT teljes_szocikk FROM bdb WHERE strong=?', (strong,)).fetchone()
    bdb_hu = None
    for (szoveg,) in con.execute("SELECT forditas_hu FROM forditasok WHERE szotar='BDB' AND strong=? ORDER BY rowid", (strong,)):
        if szoveg and szoveg.strip():
            bdb_hu = szoveg.replace('\\n', '\n')
    elo = con.execute("SELECT COUNT(*), COUNT(DISTINCT substr(igehely, 1, instr(igehely, ' ') - 1)) FROM token_strong WHERE strong=?", (strong,)).fetchone()
    alak, magas = Counter(), 0
    gramm = con.execute('SELECT 1 FROM grammatikai_strongok WHERE strong=?', (strong,)).fetchone() if _van_oszlop(con, 'grammatikai_strongok', 'strong') else None
    for hu, bz in con.execute('SELECT hu_szo, bizonyossag FROM token_par WHERE strong=?', (strong,)):
        a = csupasz_alak(hu)
        if a:
            alak[a] += 1
            magas += (bz == 'magas')
    bridge = sorted(((int(c), g) for g, c in con.execute('SELECT greek_strong, count FROM lxx_bridge WHERE strong=?', (strong,))), reverse=True)[:3]
    return {'szotar': sz, 'bdb_en': bdb_en[0] if bdb_en else '', 'bdb_hu': bdb_hu, 'elofordulas': elo[0], 'konyvek': elo[1],
            'karoli_osszes': sum(alak.values()), 'karoli_magas': magas, 'karoli_top8': alak.most_common(8), 'bridge': bridge, 'gramm': bool(gramm)}


_OSZLOP = {}


def _van_oszlop(con, tabla, oszlop):
    k = (tabla, oszlop)
    if k not in _OSZLOP:
        _OSZLOP[k] = any(r[1] == oszlop for r in con.execute('PRAGMA table_info(%s)' % tabla))
    return _OSZLOP[k]


def db_gorog(con, g):
    tb = con.execute('SELECT szo, atiras, gloss, jelentes FROM tbesg WHERE strong=? ORDER BY rowid LIMIT 1', (g,)).fetchone()
    th = con.execute('SELECT teljes_szocikk FROM thayer WHERE strong=?', (g,)).fetchone()
    hu = con.execute("SELECT COUNT(*) FROM forditasok WHERE szotar IN ('Thayer','UBS_DNTG') AND strong=? AND forditas_hu <> ''", (g,)).fetchone()[0]
    usz = con.execute('SELECT COUNT(*), COUNT(DISTINCT igehely) FROM token_strong WHERE strong=?', (g,)).fetchone()
    heb = sorted(((int(c), h) for h, c in con.execute('SELECT hebrew_strong, count FROM lxx_bridge WHERE greek_strong=?', (g,))), reverse=True)[:5]
    return {'tbesg': tisztit_tbesg(tb[3]) if tb else '', 'tbesg_alak': (tb[0], tb[1], tb[2]) if tb else None,
            'thayer': th[0] if th else '', 'hu_db': hu, 'usz_db': usz[0], 'usz_versek_db': usz[1], 'heber': heb}


# ----------------------------------------------------------------------------------------
# D2: egyezés a TSV-ből készült JSON-nal
# ----------------------------------------------------------------------------------------
def hasonlit_vers(con, v, db=None):
    """A vers-lap blokkjainak összevetése: {blokk: (egyezik, tsv_ertek, db_ertek, ok)}."""
    ig = v['igehely']
    d = db or db_vers(con, ig)
    ki = {}
    ki['karoli_szoveg'] = (d['karoli'] == v['karoli'], v['karoli'], d['karoli'], '')
    tsv_par = [tuple(sorted(w['strongok'])) for w in v['hu_szavak']]
    db_par = [tuple(sorted(x[0] for x in d['par'].get(i, []))) for i in range(1, len(v['hu_szavak']) + 1)]
    ki['karoli_strong_parositas'] = (tsv_par == db_par, tsv_par, db_par, '')
    tsv_he = [(w['strong'], w['heber'], w['atiras']) for w in v['heber']]
    ki['heber_szavak'] = (tsv_he == d['heber'], tsv_he, d['heber'], '')
    egyezo_ubs = all(sorted(x['lexid'] for x in w['ubs']) == d['ubs'].get(w['strong'], []) for w in v['heber'])
    ki['ubs_jelentes'] = (egyezo_ubs, None, None, '')
    # TSK: a megjelenítési alak eltér ("Péld 8,22" a TSV-ben, "Péld 8:22" az adatbázisban)
    norm = lambda s: re.sub(r'(\d),(\d)', r'\1:\2', s)
    tsv_tsk = [norm(x) for x in v['tsk']]
    db_tsk = [x[0] for x in d['tsk']]
    elso6 = db_tsk[:6]
    # holtversenynél a sorrend nem határozza meg a TSV top-6-ot: a szavazatszám-sorozatot hasonlítjuk
    votes_db = [x[1] for x in d['tsk']][:6]
    ki['tsk_darab'] = (v['tsk_db'] == len(d['tsk']), v['tsk_db'], len(d['tsk']), '')
    ki['tsk_top6'] = (set(tsv_tsk) <= set(db_tsk) and len(tsv_tsk) == len(elso6), tsv_tsk, elso6,
                      'normalizálás: a TSV megjelenítési alakja (vessző) és az adatbázisé (kettőspont) eltér' if tsv_tsk != elso6 else '')
    ki['karoli_kereszthivatkozas_darab'] = (min(len(v['karoli_kh']), 8) == min(d['kh_db'], 8), len(v['karoli_kh']), d['kh_db'],
                                              'a tartalom nem vethető össze: a DB nem hordozza a TSV 3. oszlopát (magyar megjelenítési alak)')
    vs = v['versszam']
    sz = d['versszam'] or ('', '', '', '')
    # a régi ág JSON-ja a megfeleltetés-forrást nem hordozza (a kjv_kulcs a LXX_OS/eltolás származéka, nem a tábla): osztály, KJV, MT
    tsv_sz = (vs['osztaly'], vs['kjv'], vs['mt'])
    db_sz = (sz[0] or '', sz[1] or '', (sz[2] or '') or (sz[1] or ''))
    ki['versszamozas'] = (tsv_sz == db_sz, tsv_sz, db_sz, '')
    lxx_ok = ('a DB nem ad LXX-verset (az lxx_versszintu_parok csak a héber–görög Strong-párral rendelkező versekre tartalmaz sort)'
              if not d['lxx'] else 'a DB más LXX-verset ad, mint a TSV (LXX_OS első találat)')
    ki['lxx_vers_szam'] = ((not vs['lxx'] and not d['lxx']) or vs['lxx'] in d['lxx'], vs['lxx'], d['lxx'], lxx_ok)
    return ki


def hasonlit_szo(con, l, db=None):
    s = l['strong']
    d = db or db_szo(con, s)
    ki = {}
    sz = d['szotar'] or ('', '', '', '')
    ki['strong_szotar'] = ((l['lemma'], l['kiejtes'], l['szofaj'], l['rovid']) == tuple(sz) or
                           (sz == ('', '', '', '')), (l['lemma'], l['kiejtes'], l['szofaj'], l['rovid']), sz, '')
    # a JSON (adat.py) az angol szöveget csak magyar fordítás hiányában tárolja: ott nincs mivel összevetni
    alias_ok = ('a szócikk a BDB_strong_alias.tsv (#57) szerint másik Strong-szám alatt áll; a pardes.db az alias-táblát nem hordozza'
                if l.get('bdb_alias') else '')
    ki['bdb_angol'] = (l['bdb_hu'] is not None or (l['bdb_en'] or '') == d['bdb_en'],
                       len(l['bdb_en'] or ''), len(d['bdb_en']), alias_ok)
    ki['bdb_magyar'] = (l['bdb_hu'] == d['bdb_hu'], len(l['bdb_hu'] or ''), len(d['bdb_hu'] or ''), alias_ok)
    ki['elofordulas'] = ((l['elofordulas'], l['konyvek_szama']) == (d['elofordulas'], d['konyvek']),
                         (l['elofordulas'], l['konyvek_szama']), (d['elofordulas'], d['konyvek']), '')
    ki['karoli_alakok'] = ((l['karoli_osszes'], l['karoli_magas']) == (d['karoli_osszes'], d['karoli_magas']) and
                           sorted(l['karoli']) == sorted(d['karoli_top8']) or
                           (l['karoli_osszes'], l['karoli_magas'], [x[1] for x in l['karoli']]) ==
                           (d['karoli_osszes'], d['karoli_magas'], [x[1] for x in d['karoli_top8']]),
                           (l['karoli_osszes'], l['karoli_magas']), (d['karoli_osszes'], d['karoli_magas']), '')
    tsv_b = [(x['strong'], x['db']) for x in l['lxx']]
    db_b = [(g, c) for c, g in d['bridge']]
    ki['lxx_bridge'] = (tsv_b == db_b, tsv_b, db_b, '')
    return ki


def egyezik_vagva(tsv, db):
    """Egyenlőség; ha a JSON-érték „…”-ra végződik (vágott), akkor az adatbázis-érték eleje egyezik vele."""
    tsv = tsv or ''
    return db.startswith(tsv[:-1]) if tsv.endswith('…') else tsv == db


def hasonlit_gorog(con, g, db=None):
    s = g['strong']
    d = db or db_gorog(con, s)
    ki = {}
    # a pilot JSON-ja a teljes TBESG/Thayer-szöveget tartalmazza (F60.46); a régi, 900/700 karakterre vágott JSON-t az előtag-egyezés még kezeli
    ki['tbesg'] = (egyezik_vagva(g['tbesg'], d['tbesg']), len(g['tbesg']), len(d['tbesg']), 'a JSON vágott szöveg (előtag-egyezés)' if (g['tbesg'] or '').endswith('…') else '')
    ki['thayer'] = (egyezik_vagva(g['thayer'], d['thayer']), len(g['thayer']), len(d['thayer']), 'a JSON vágott szöveg (előtag-egyezés)' if (g['thayer'] or '').endswith('…') else '')
    ki['magyar_szocikk'] = (len(g['hu']) == min(d['hu_db'], 6), len(g['hu']), d['hu_db'], '')
    ki['usz_elofordulas'] = ((g['usz_db'], g['usz_versek_db']) == (d['usz_db'], d['usz_versek_db']),
                             (g['usz_db'], g['usz_versek_db']), (d['usz_db'], d['usz_versek_db']), '')
    tsv_h = [(x['strong'], x['db']) for x in g['heber']]
    db_h = [(h, c) for c, h in d['heber']]
    ki['heber_hatter'] = (tsv_h == db_h, tsv_h, db_h, '')
    return ki


def egyezes(con, adat, forras_valtozott):
    """D2: minden vers, héber szó-lap és görög szó-lap összevetése; az eltérések blokkonként."""
    szamlalo = defaultdict(lambda: [0, 0])      # blokk -> [vizsgált, eltérő]
    peldak = defaultdict(list)
    okok = defaultdict(Counter)

    def felvesz(csoport, azon, ki):
        for blokk, (eg, tv, dv, ok) in ki.items():
            k = '%s:%s' % (csoport, blokk)
            szamlalo[k][0] += 1
            if not eg:
                szamlalo[k][1] += 1
                if len(peldak[k]) < 4:
                    peldak[k].append({'azon': azon, 'tsv': tv if not isinstance(tv, str) or len(tv) < 120 else tv[:120] + '…',
                                      'db': dv if not isinstance(dv, str) or len(dv) < 120 else dv[:120] + '…'})
                okok[k][ok or ('a forrás-TSV az építés óta módosult (D5); a tartalmi ok nem külön igazolt' if forras_valtozott.get(blokk) else 'ismeretlen')] += 1

    for v in adat['versek']:
        felvesz('vers', v['igehely'], hasonlit_vers(con, v))
    for l in adat['lapok'].values():
        felvesz('heber_szo', l['strong'], hasonlit_szo(con, l))
    for g in adat['gor_lapok'].values():
        felvesz('gorog_szo', g['strong'], hasonlit_gorog(con, g))
    return {k: {'vizsgalt': a, 'eltero': b, 'okok': dict(okok[k]), 'peldak': peldak[k]} for k, (a, b) in sorted(szamlalo.items())}


# ----------------------------------------------------------------------------------------
# D3: lekérdezési idő
# ----------------------------------------------------------------------------------------
def percentilis(x, p):
    x = sorted(x)
    return x[min(len(x) - 1, int(round(p * (len(x) - 1))))] if x else None


def ido(db_ut, versek, szavak, gorogok, hideg_minta=40):
    def t(f, *a):
        t0 = time.perf_counter()
        f(*a)
        return (time.perf_counter() - t0) * 1000.0

    ki = {}
    con = kapcsolat(db_ut)
    meleg = {'vers': [], 'szo': [], 'gorog': []}
    for menet in (1, 2):                     # az 1. menet bemelegít, a 2. a „meleg” mérés
        for k, lista, f in (('vers', versek, db_vers), ('szo', szavak, db_szo), ('gorog', gorogok, db_gorog)):
            xs = [t(f, con, e) for e in lista]
            if menet == 2:
                meleg[k] = xs
    con.close()
    for k, lista, f in (('vers', versek, db_vers), ('szo', szavak, db_szo), ('gorog', gorogok, db_gorog)):
        lepes = max(1, len(lista) // hideg_minta)
        hideg = []
        for e in lista[::lepes][:hideg_minta]:
            c = kapcsolat(db_ut)             # új kapcsolat: üres SQLite-gyorsítótár
            hideg.append(t(f, c, e))
            c.close()
        ki[k] = {'n_meleg': len(meleg[k]), 'meleg_median_ms': round(statistics.median(meleg[k]), 2) if meleg[k] else None,
                 'meleg_p95_ms': round(percentilis(meleg[k], 0.95), 2) if meleg[k] else None,
                 'n_hideg': len(hideg), 'hideg_median_ms': round(statistics.median(hideg), 2) if hideg else None,
                 'hideg_p95_ms': round(percentilis(hideg, 0.95), 2) if hideg else None}
    return ki


# ----------------------------------------------------------------------------------------
# D4: szükséges részhalmaz mérete
# ----------------------------------------------------------------------------------------
LAPHOZ_TABLAK = ['vers', 'token_par', 'token_eredeti', 'token_strong', 'tsk', 'kh', 'vers_szamozas', 'strong_szotar', 'bdb',
                 'forditasok', 'thayer', 'tbesg', 'lxx_bridge', 'lxx_versszintu_parok', 'ubs_dbh_referenciak', 'ubs_dbh_jelentesek',
                 'grammatikai_strongok', 'licencek', 'meta',
                 # a régi ág (claude/olvasoi-pilot) bővebb blokkjai (F60.5–F60.9)
                 'bsb', 'kjv', 'tipnr', 'nave_basokant', 'igehely_tartomany', 'lxx_dontesek', 'kapcsolatok', 'motivumok',
                 'morf_kulcs_heber', 'sdbh_domenek', 'sdgnt_domenek', 'sece_h', 'sece_g', 'tbesh', 'lsj', 'mcged',
                 'ubs_dntg_jelentesek', 'ubs_dntg_referenciak', 'tw_szocikkek', 'oshl_lexikalis_index', 'oshl_bdb_igehelyek']


def tabla_meretek():
    """{tábla: (MB indexszel, MB licenc_* nélkül)} a naplok/SQLITE_EPIT_meres.md táblázatából.
    A táblázat „MB”-ja valójában MiB (lapszám × lapméret / 2^20: a fájl 886 415 360 bájt = 845,4 MiB = 886,4 MB); az itt visszaadott
    érték MB = 10^6 bájt (F60.52: egy egységet használunk)."""
    MIB_MB = 1048576 / 1e6
    ki = {}
    ut = GY + 'naplok/SQLITE_EPIT_meres.md'
    if not os.path.exists(ut):
        return ki
    for s in open(ut, encoding='utf-8'):
        m = re.match(r'^\| `(\w+)` \| (\d+) \| ([\d.]+) \| ([\d.]+) \|', s)
        if m:
            ki[m.group(1)] = (float(m.group(3)) * MIB_MB, float(m.group(4)) * MIB_MB)
    return ki


def reszhalmaz_meret(db_ut, tomorites):
    tm = tabla_meretek()
    van = [t for t in LAPHOZ_TABLAK if t in tm]
    hianyzik = [t for t in LAPHOZ_TABLAK if t not in tm]
    szukseges = sum(tm[t][0] for t in van)
    licenc_nelkul = sum(tm[t][1] for t in van)
    osszes = sum(v[0] for v in tm.values())
    fajl_mb = os.path.getsize(db_ut) / 1e6
    ki = {'forras': 'naplok/SQLITE_EPIT_meres.md (táblánkénti méret indexszel; MiB-ből átszámolva MB = 10^6 bájtra)', 'fajl_mb': round(fajl_mb, 1),
          'tablak_osszege_mb': round(osszes, 1), 'szukseges_tablak': van, 'nincs_a_meres_tablazataban': hianyzik,
          'szukseges_mb': round(szukseges, 1), 'szukseges_licenc_oszlop_nelkul_mb': round(licenc_nelkul, 1),
          'resz_a_teljesbol_szazalek': round(100 * szukseges / osszes, 1) if osszes else None,
          'nem_kell': sorted(((t, tm[t][0]) for t in tm if t not in LAPHOZ_TABLAK), key=lambda x: -x[1])[:6]}
    # a TSV-ként maradó blokkok (Macula, LXX_OS) mérete, ha az adatbázisba kerülnének
    tsv = 0
    for pat in ('konkordancia/Macula_heber_', 'konkordancia/LXX_OS/'):
        if pat.endswith('/'):
            tsv += sum(os.path.getsize(os.path.join(GY + pat, f)) for f in os.listdir(GY + pat) if f.endswith('.tsv'))
        else:
            d = GY + 'konkordancia/'
            tsv += sum(os.path.getsize(d + f) for f in os.listdir(d) if f.startswith('Macula_heber_'))
    ki['macula_es_lxx_os_tsv_mb'] = round(tsv / 1e6, 1)
    if tomorites:
        h0 = time.time()
        orig = comp = 0
        z = __import__('zlib').compressobj(6, wbits=31)
        with open(db_ut, 'rb') as fh:
            while True:
                b = fh.read(1 << 22)
                if not b:
                    break
                orig += len(b)
                comp += len(z.compress(b))
        comp += len(z.flush())
        arany = comp / orig
        ki['gzip_arany_a_teljes_fajlra'] = round(arany, 3)
        ki['gzip_becsles_szukseges_mb'] = round(szukseges * arany, 1)
        ki['gzip_meres_mp'] = round(time.time() - h0, 1)
    ki['viszonyitas_ADATVAGYON_TERV'] = {
        '3. szakasz': 'a Netlify-function zip-je ~50 MB tömörítve (kicsomagolva ~250 MB); a teljes adatvagyon 30–60 MB zip körül, „a határon”',
        '7. szakasz': 'a teljes Biblia indexekkel 50–150 MB (becslés); „több száz MB fölött még megy, csak a Netlify-csomagméret korlátoz”'}
    return ki


# ----------------------------------------------------------------------------------------
# D5: frissesség
# ----------------------------------------------------------------------------------------
TSV_FORRAS = {'vers': ['konkordancia/Karoli_1908.tsv'], 'token_par': ['adat/karoli_strong/'],
              'token_eredeti': ['konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv'],
              'token_strong': ['konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv'],
              'tsk': ['konkordancia/TSK_kereszthivatkozasok.tsv'], 'kh': ['konkordancia/Karoli_kereszthivatkozasok.tsv'],
              'vers_szamozas': ['konkordancia/Karoli_versmegfeleltetes.tsv'], 'strong_szotar': ['konkordancia/Strong_szotar.tsv'],
              'bdb': ['konkordancia/BDB_teljes_unabridged.tsv'], 'forditasok': ['adat/forditasok.tsv'],
              'thayer': ['konkordancia/Thayer_teljes.tsv'], 'tbesg': ['konkordancia/TBESG.txt'],
              'lxx_bridge': ['adat/kulso/lxx_bridge.tsv'],
              'lxx_versszintu_parok': ['konkordancia/LXX_OS/'],
              'ubs_dbh_referenciak': ['konkordancia/UBS_DBH_referenciak.tsv'], 'ubs_dbh_jelentesek': ['konkordancia/UBS_DBH_jelentesek.tsv'],
              'grammatikai_strongok': ['adat/grammatikai_strongok.tsv'], 'licencek': ['adat/licencek.tsv']}
EGYEZO_SORSZAM = {'strong_szotar': 'konkordancia/Strong_szotar.tsv', 'bdb': 'konkordancia/BDB_teljes_unabridged.tsv',
                  'thayer': 'konkordancia/Thayer_teljes.tsv', 'lxx_bridge': 'adat/kulso/lxx_bridge.tsv',
                  'forditasok': 'adat/forditasok.tsv', 'tsk': 'konkordancia/TSK_kereszthivatkozasok.tsv',
                  'ubs_dbh_jelentesek': 'konkordancia/UBS_DBH_jelentesek.tsv', 'ubs_dbh_referenciak': 'konkordancia/UBS_DBH_referenciak.tsv',
                  'kh': 'konkordancia/Karoli_kereszthivatkozasok.tsv', 'vers': 'konkordancia/Karoli_1908.tsv'}


def git(*a):
    return subprocess.run(['git', '-C', GY] + list(a), capture_output=True, text=True, encoding='utf-8').stdout.strip()


def tsv_sorok(rel):
    n = 0
    with open(GY + rel, encoding='utf-8') as fh:
        for s in fh:
            if s.strip() and not s.startswith('#'):
                n += 1
    return n - 1                              # a fejlécsor nem adat


def tabla_hash(con, n):
    oszlopszam = len(con.execute('PRAGMA table_info("%s")' % n).fetchall())
    order = ','.join(str(i + 1) for i in range(oszlopszam))
    h, db = hashlib.sha256(), 0
    for row in con.execute('SELECT * FROM "%s" ORDER BY %s' % (n, order)):
        h.update(('\t'.join('' if v is None else str(v) for v in row) + '\n').encode('utf-8'))
        db += 1
    return db, h.hexdigest()


def frissesseg(con, hash_ellenorzes):
    m = meta(con)
    ts = m.get('epites_ts', '')
    try:
        epites = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        epites = None
    sorok, elter = [], []
    for t in LAPHOZ_TABLAK:
        if t == 'meta':
            continue
        h = m.get('hash:' + t)
        sor = {'tabla': t, 'meta_sor': int(h.split('|')[0]) if h else None, 'meta_hash16': h.split('|')[1][:16] if h else None}
        if hash_ellenorzes and h:
            db, hh = tabla_hash(con, t)
            sor['tartalom_egyezik_a_meta_hash-sel'] = (db == sor['meta_sor'] and hh == h.split('|')[1])
        valt = []
        for rel in TSV_FORRAS.get(t, []):
            ut = rel
            if git('status', '--porcelain', '--', ut):
                valt.append('%s: nem commitolt módosítás' % rel)
            ci = git('log', '-1', '--format=%cI', '--', ut)
            if ci and epites:
                cdt = datetime.datetime.fromisoformat(ci)
                if cdt > epites:
                    valt.append('%s: utolsó commit %s, az építés %s' % (rel, ci, ts))
        if t == 'token_eredeti':
            osszeg = sum(tsv_sorok(x) for x in TSV_FORRAS[t])
            sor['tsv_sor_most'] = osszeg
            if sor['meta_sor'] is not None and osszeg != sor['meta_sor']:
                valt.append('sorszám: tsv (TAHOT+TAGNT) %d, adatbázis %d (különbség %+d)' % (osszeg, sor['meta_sor'], osszeg - sor['meta_sor']))
        if t in EGYEZO_SORSZAM and os.path.exists(GY + EGYEZO_SORSZAM[t]):
            ts_sor = tsv_sorok(EGYEZO_SORSZAM[t])
            sor['tsv_sor_most'] = ts_sor
            if sor['meta_sor'] is not None and ts_sor != sor['meta_sor']:
                valt.append('sorszám: tsv %d, adatbázis %d' % (ts_sor, sor['meta_sor']))
        sor['eltérés'] = valt
        if valt or sor.get('tartalom_egyezik_a_meta_hash-sel') is False:
            elter.append(t)
        sorok.append(sor)
    return {'epites_ts': ts, 'mod': m.get('mod'), 'tablak': sorok, 'eltero_tablak': elter,
            'hash_ellenorzes_futott': bool(hash_ellenorzes)}


# ----------------------------------------------------------------------------------------
# D1: blokk-lefedettség
# ----------------------------------------------------------------------------------------
# (blokk, melyik oldalon, a DB-táblák, ha a DB elég; különben a TSV-forrás)
BLOKKOK = [
    ('vers-lap: Károli-szöveg', 'vers', ['vers'], None),
    ('vers-lap: Károli–Strong párosítás (aláhúzás)', 'vers', ['token_par'], None),
    ('vers-lap: héber szavak (TAHOT: alak, átírás, tükörfordítás, Strong)', 'vers', ['token_eredeti'], None),
    ('vers-lap: igealak-kód, szófaj (Macula)', 'vers', [], 'konkordancia/Macula_heber_*.tsv'),
    ('vers-lap: héber–görög párosítás szavanként (Macula)', 'vers', [], 'konkordancia/Macula_heber_*.tsv'),
    ('vers-lap: görög szóalak és a Septuaginta-vers szavai (LXX_OS)', 'vers', [], 'konkordancia/LXX_OS/*.tsv'),
    ('vers-lap: LXX-versszám', 'vers', ['lxx_versszintu_parok'], None),
    ('vers-lap: versszámozás (MT / KJV)', 'vers', ['vers_szamozas'], None),
    ('vers-lap: angol szavak szavanként (BSB, KJV+Strong)', 'vers', ['bsb', 'kjv'], None),
    ('vers-lap: Nave-témák (a tartományok versekre bontva)', 'vers', ['nave_basokant', 'igehely_tartomany'], None),
    ('vers-lap: TIPNR (személy- és helynevek)', 'vers', ['tipnr'], None),
    ('vers-lap: igealak magyar feloldása (morf_kulcs_heber)', 'vers', ['morf_kulcs_heber'], None),
    ('vers-lap: LXX-döntés, kapcsolat, motívum (adatréteg-sorok)', 'vers', ['lxx_dontesek', 'kapcsolatok', 'motivumok'], None),
    ('vers-lap: TSK-kereszthivatkozás', 'vers', ['tsk'], None),
    ('vers-lap: Károli-kereszthivatkozás', 'vers', ['kh'], None),
    ('vers-lap: UBS-jelentés az előfordulásra', 'vers', ['ubs_dbh_referenciak', 'ubs_dbh_jelentesek'], None),
    ('szó-lap (héber): Strong-szótár (szótő, kiejtés, szófaj, rövid jelentés)', 'szo', ['strong_szotar'], None),
    ('szó-lap (héber): előfordulás, könyvek száma', 'szo', ['token_strong'], None),
    ('szó-lap (héber): Károli-alakok és bizonyosság', 'szo', ['token_par'], None),
    ('szó-lap (héber): BDB angol szócikk', 'szo', ['bdb'], None),
    ('szó-lap (héber): BDB magyar fordítás', 'szo', ['forditasok'], None),
    ('szó-lap (héber): görög megfelelő (lxx_bridge)', 'szo', ['lxx_bridge'], None),
    ('szó-lap (héber): szemantikai domén (SDBH)', 'szo', ['sdbh_domenek'], None),
    ('szó-lap (héber): SECE-szócikk (héber)', 'szo', ['sece_h'], None),
    ('szó-lap (héber): OSHL (lexikális index, BDB-helyek)', 'szo', ['oshl_lexikalis_index', 'oshl_bdb_igehelyek'], None),
    ('szó-lap (héber): TBESH', 'szo', ['tbesh'], None),
    ('szó-lap (héber): tW-szócikk', 'szo', ['tw_szocikkek'], None),
    ('szó-lap (héber): nyelvtani Strong-számok szűrése (nincs lap)', 'szo', ['grammatikai_strongok'], None),
    ('szó-lap (görög): TBESG', 'gorog', ['tbesg'], None),
    ('szó-lap (görög): Thayer angol', 'gorog', ['thayer'], None),
    ('szó-lap (görög): magyar jelentés (Thayer, UBS DNTG)', 'gorog', ['forditasok'], None),
    ('szó-lap (görög): ÚSZ-előfordulás és versek', 'gorog', ['token_strong', 'vers'], None),
    ('szó-lap (görög): héber háttér', 'gorog', ['lxx_bridge'], None),
    ('szó-lap (görög): szemantikai domén (SDGNT)', 'gorog', ['sdgnt_domenek'], None),
    ('szó-lap (görög): SECE-szócikk (görög)', 'gorog', ['sece_g'], None),
    ('szó-lap (görög): LSJ', 'gorog', ['lsj'], None),
    ('szó-lap (görög): MCGED', 'gorog', ['mcged'], None),
    ('szó-lap (görög): UBS DNTG jelentés', 'gorog', ['ubs_dntg_jelentesek', 'ubs_dntg_referenciak'], None),
    ('szó-lap (görög): tW-szócikk', 'gorog', ['tw_szocikkek'], None),
]


def lefedettseg(con, adat):
    """D1: táblánként: létezik-e, hány sora van a szakaszra / a lapok Strong-számaira."""
    igek = [v['igehely'] for v in adat['versek']]
    tablak = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    tseg = {}
    for t, oszlop in (('vers', 'igehely'), ('token_par', 'igehely'), ('token_eredeti', 'igehely'), ('tsk', 'igehely'), ('kh', 'igehely'),
                      ('vers_szamozas', 'igehely'), ('lxx_versszintu_parok', 'igehely'), ('ubs_dbh_referenciak', 'igehely'),
                      ('bsb', 'igehely'), ('kjv', 'igehely'), ('tipnr', 'igehely'), ('igehely_tartomany', 'igehely'),
                      ('lxx_dontesek', 'igehely'), ('kapcsolatok', 'forras_igehely')):
        if t in tablak:
            n = 0
            for i in range(0, len(igek), 400):
                resz = igek[i:i + 400]
                n += con.execute('SELECT COUNT(*) FROM %s WHERE %s IN (%s)' % (t, oszlop, ','.join('?' * len(resz))), resz).fetchone()[0]
            tseg[t] = n
    he = list(adat['lapok'])
    go = list(adat['gor_lapok'])
    for t, kulcsok in (('strong_szotar', he + go), ('bdb', he), ('forditasok', he + go), ('lxx_bridge', he), ('thayer', go), ('tbesg', go),
                       ('token_strong', he + go), ('ubs_dbh_jelentesek', he), ('sdbh_domenek', he), ('sece_h', he), ('tbesh', he),
                       ('oshl_lexikalis_index', he), ('oshl_bdb_igehelyek', he), ('sdgnt_domenek', go), ('sece_g', go), ('lsj', go),
                       ('mcged', go), ('ubs_dntg_jelentesek', go), ('ubs_dntg_referenciak', go), ('tw_szocikkek', he + go)):
        if t in tablak:
            col = 'hebrew_strong' if t == 'lxx_bridge' else 'strong'
            seg = 0
            for i in range(0, len(kulcsok), 400):
                resz = kulcsok[i:i + 400]
                seg += con.execute('SELECT COUNT(*) FROM %s WHERE %s IN (%s)' % (t, col, ','.join('?' * len(resz))), resz).fetchone()[0]
            tseg[t] = seg
    for t in ('grammatikai_strongok', 'morf_kulcs_heber', 'motivumok'):   # nem szakasz-függő táblák: az összes sor
        if t in tablak:
            tseg[t] = con.execute('SELECT COUNT(*) FROM %s' % t).fetchone()[0]
    ki, db_ben, tsv_kell = [], 0, 0
    for nev, oldal, tbl, tsv in BLOKKOK:
        if tsv:
            ki.append({'blokk': nev, 'forras': 'TSV', 'tsv': tsv, 'ok': 'a pardes.db-ben nincs ilyen tábla (az építő szándékosan nem tölti be)'})
            tsv_kell += 1
            continue
        hianyzo = [t for t in tbl if t not in tablak]
        ures = [t for t in tbl if t in tablak and tseg.get(t, 0) == 0]
        if hianyzo:
            ki.append({'blokk': nev, 'forras': 'TSV', 'ok': 'hiányzó tábla: ' + ', '.join(hianyzo)})
            tsv_kell += 1
        elif ures:
            ki.append({'blokk': nev, 'forras': 'részben', 'ok': 'a tábla nem ad sort erre a szakaszra: ' + ', '.join(ures), 'tablak': tbl,
                       'sorok_a_szakaszra': {t: tseg.get(t, 0) for t in tbl}})
        else:
            ki.append({'blokk': nev, 'forras': 'pardes.db', 'tablak': tbl, 'sorok_a_szakaszra': {t: tseg.get(t, 0) for t in tbl}})
            db_ben += 1
    return {'blokkok': ki, 'db_bol_elo_allithato': db_ben, 'tsv_kell': tsv_kell, 'osszes_blokk': len(ki)}


# ----------------------------------------------------------------------------------------
def adat_json(szakasz, json_konyvtar):
    if json_konyvtar:
        ut = os.path.join(json_konyvtar, azonosito(szakasz), 'olvaso_pilot.json')
        if os.path.exists(ut):
            return json.load(open(ut, encoding='utf-8'))
    tmp = tempfile.mkdtemp(prefix='olvaso_pilot_dbm_')
    subprocess.run([sys.executable, os.path.join(D, 'adat.py'), '--szakasz', szakasz, '--kimenet', tmp], check=True,
                   capture_output=True)
    return json.load(open(os.path.join(tmp, 'olvaso_pilot.json'), encoding='utf-8'))


def main():
    ap = argparse.ArgumentParser(description='Olvasói pilot: a pardes.db mérése (M2b)')
    ap.add_argument('--db', default=alap_db())
    ap.add_argument('--szakasz', action='append', help='alapból: %s' % ', '.join(SZAKASZOK))
    ap.add_argument('--json-konyvtar', default=None, help='az adat.py kimenete szakaszonként <könyvtár>/<azonosító>/olvaso_pilot.json')
    ap.add_argument('--kimenet', default=os.path.join(tempfile.gettempdir(), 'olvaso_pilot'))
    ap.add_argument('--nincs-hash', action='store_true', help='a meta hash újraszámítása nélkül (gyorsabb)')
    ap.add_argument('--nincs-tomorites', action='store_true', help='a gzip-arány mérése nélkül')
    a = ap.parse_args()
    os.makedirs(a.kimenet, exist_ok=True)
    ki_ut = os.path.join(a.kimenet, 'olvaso_pilot_db_meres.json')
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    if not os.path.exists(a.db):
        eredmeny = {'allapot': 'nem mérhető', 'ok': 'nincs pardes.db (%s); az adatbázist ez a szkript nem építi újra' % a.db,
                    'proveniencia': 'scope=%s | forras=pardes.db (nincs) | ts=%s' % (', '.join(a.szakasz or SZAKASZOK), ts)}
        json.dump(eredmeny, open(ki_ut, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('M2b: NEM MÉRHETŐ -', eredmeny['ok'])
        return 0
    con = kapcsolat(a.db)
    m = meta(con)
    hashek = '; '.join('%s=%s' % (t, m['hash:' + t].split('|')[1][:12]) for t in LAPHOZ_TABLAK if 'hash:' + t in m)
    forras = 'pardes.db meta.epites_ts=%s meta.mod=%s hash(tábla=sha12)=%s' % (m.get('epites_ts'), m.get('mod'), hashek)
    fr = frissesseg(con, not a.nincs_hash)
    forras_valtozott = {}
    eredmeny = {'allapot': 'mérve', 'db': a.db, 'gep': {'platform': platform.platform(), 'cpu_db': os.cpu_count(), 'python': platform.python_version(),
                                                      'fajl_mb': round(os.path.getsize(a.db) / 1e6, 1)},
                'meta': {'epites_ts': m.get('epites_ts'), 'mod': m.get('mod')}, 'szakaszok': {}}
    eredmeny['D4'] = reszhalmaz_meret(a.db, not a.nincs_tomorites)
    eredmeny['D5'] = fr
    valt = set(fr['eltero_tablak'])
    forras_valtozott = {'karoli_szoveg': 'vers' in valt, 'karoli_strong_parositas': 'token_par' in valt, 'heber_szavak': 'token_eredeti' in valt,
                        'tsk_darab': 'tsk' in valt, 'tsk_top6': 'tsk' in valt, 'ubs_jelentes': bool({'ubs_dbh_referenciak', 'ubs_dbh_jelentesek'} & valt),
                        'versszamozas': 'vers_szamozas' in valt, 'strong_szotar': 'strong_szotar' in valt, 'bdb_angol': 'bdb' in valt,
                        'bdb_magyar': 'forditasok' in valt, 'elofordulas': 'token_strong' in valt, 'karoli_alakok': 'token_par' in valt,
                        'lxx_bridge': 'lxx_bridge' in valt, 'tbesg': 'tbesg' in valt, 'thayer': 'thayer' in valt, 'magyar_szocikk': 'forditasok' in valt,
                        'usz_elofordulas': 'token_strong' in valt, 'heber_hatter': 'lxx_bridge' in valt}
    for sz in (a.szakasz or SZAKASZOK):
        adat = adat_json(sz, a.json_konyvtar)
        prov = 'scope=%s | forras=%s | ts=%s' % (sz, forras, ts)
        versek = [v['igehely'] for v in adat['versek']]
        r = {'proveniencia': prov, 'versek': len(versek), 'heber_lapok': len(adat['lapok']), 'gorog_lapok': len(adat['gor_lapok'])}
        r['D1'] = lefedettseg(con, adat)
        r['D2'] = egyezes(con, adat, forras_valtozott)
        r['D3'] = ido(a.db, versek, list(adat['lapok']), list(adat['gor_lapok']))
        eredmeny['szakaszok'][sz] = r
        print('==', prov)
        print('D1: db-ből előállítható blokk %d / %d; TSV kell %d' % (r['D1']['db_bol_elo_allithato'], r['D1']['osszes_blokk'], r['D1']['tsv_kell']))
        for k, v in r['D2'].items():
            print('D2 %-40s vizsgált %5d, eltérő %5d %s' % (k, v['vizsgalt'], v['eltero'], v['okok'] if v['eltero'] else ''))
        for k, v in r['D3'].items():
            print('D3 %-6s meleg median %s ms, p95 %s ms | hideg median %s ms, p95 %s ms' % (k, v['meleg_median_ms'], v['meleg_p95_ms'], v['hideg_median_ms'], v['hideg_p95_ms']))
    print('D4:', json.dumps({k: v for k, v in eredmeny['D4'].items() if k not in ('szukseges_tablak', 'nem_kell')}, ensure_ascii=False))
    print('D5: eltérő táblák:', fr['eltero_tablak'], '| építés:', fr['epites_ts'])
    json.dump(eredmeny, open(ki_ut, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('kimenet:', ki_ut)
    return 0


if __name__ == '__main__':
    sys.exit(main())
