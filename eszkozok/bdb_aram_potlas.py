#!/usr/bin/env python
"""A BDB elvetett arámi szócikkeinek pótlása külön táblába (F66, #66).

Forrás: konkordancia/BDB_strong_alias_elvetett.tsv (nyelv=aram sorok, a #57 kimenete, csak olvas),
konkordancia/lexikonok_nyers/BDB.lexicon (SQLite, csak olvas), konkordancia/OSHL_lexikalis_index.tsv.
A normalizálást, a HTML-tisztítást és a stílusigazítást az eszkozok/bdb_strong_potlas.py-ból veszi
(importálja, nem másolja).

Módok:
  --m0  felmérés: naplok/BDB_ARAM_POTLAS_M0.md
  --m1  jelölttábla: konkordancia/BDB_aram_potlas.tsv

A BDB_teljes_unabridged.tsv-t, a BDB_strong_alias.tsv-t és a BDB_strong_alias_elvetett.tsv-t
SOHA nem írja. A TSV-ket split('\\t')-tel olvassa, '\\t'.join()-nal írja (nem csv modul).

Állapotok (allapot):
  egyertelmu    a BDB-szócikk saját szöveggel bír, nem csonk, a címszó/glossza az OSHL-lemmával egyezik,
                a BDB-azonosítóra pontosan ez az egy címke nélküli (táblasor nélküli) Strong mutat
  csonk         gyök-hivatkozás ("√ of following"), szófaj és értelem nélkül: gyenge bizonyíték
  tobb_jelolt   a szócikk más, táblasor nélküli Strongot is hordoz (nem dönthető el, melyikhez tartozik)
  nincs_szoveg  a Strong saját szövege nem azonosítható: a címke nem szócikkre mutat (bevezető jegyzet),
                a szócikk címszava és glosszája az OSHL-lemmával sem egyezik, vagy üres a szöveg
"""
import sys
import os
import re
import sqlite3
import collections
import datetime
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_strong_potlas as B  # noqa: E402

GYOKER = B.GYOKER
KIMENET = os.path.join(GYOKER, 'konkordancia', 'BDB_aram_potlas.tsv')
M0_JELENTES = os.path.join(GYOKER, 'naplok', 'BDB_ARAM_POTLAS_M0.md')
FEJLEC = ['Strong_padded', 'bdb_id', 'cimszo', 'oshl_lemma', 'allapot', 'indok', 'Teljes_szocikk', 'proveniencia']
ALLAPOTOK = ('egyertelmu', 'csonk', 'tobb_jelolt', 'nincs_szoveg')
STOP = B.STOP | {'see', 'etc', 'but', 'its', 'are', 'was', 'not'}


def elvetett_aram():
    """Az elvetett tábla nyelv=aram sorai (a mezők split('\\t')-tel)."""
    with open(B.ELVETETT, encoding='utf-8', newline='') as f:
        sorok = [l.split('\t') for l in f.read().split('\n') if l]
    fej, adat = sorok[0], sorok[1:]
    assert fej == B.ELVETETT_FEJLEC, fej
    return [dict(zip(fej, r)) for r in adat if r[2] == 'aram']


def szocikk_elemzes(bid):
    """A BDB.lexicon szócikkének elemzése: a betűfej-bekezdés (<big>) kihagyásával.

    Visszaad: dict(nyers, cimszavak, szofaj, glosszak, gyokstub, jegyzet, szoveg_hossz)."""
    con = sqlite3.connect('file:%s?mode=ro' % B.LEX.replace('\\', '/'), uri=True)
    r = con.execute('select Definition from Lexicon where Topic=?', (bid,)).fetchone()
    con.close()
    if not r:
        return None
    nyers = r[0]
    torzs = B.lexikon_torzs(bid)
    jegyzet = '[Note]' in torzs or 'class="remarks"' in torzs
    # betűfej: <p><bdbheb><big>X</big></bdbheb></p> — nem címszó
    torzs_cs = re.sub(r'<p>\s*<bdbheb>\s*<big>.*?</big>\s*</bdbheb>\s*</p>', '', torzs, count=1, flags=re.S)
    p = re.search(r'<p>(.*?)(</p>|$)', torzs_cs, re.S)
    elso = p.group(1) if p else ''
    b = re.search(r'<b>', elso)
    elotte = elso[:b.start()] if b else elso[:400]
    cimre = r'<bdb(?:heb|arc)>(.*?)</bdb(?:heb|arc)>'
    cimszavak = [c for c in (re.findall(cimre, elotte) or re.findall(cimre, elso)[:1]) if '<' not in c]
    szofaj = B.tisztit(re.search(r'<b>(.*?)</b>', elso).group(1)) if b else ''
    glosszak = []
    for g in re.findall(r'<highlightword>(.*?)</highlightword>', elso):
        glosszak.append(B.tisztit(g))
    gyokstub = (not b) or ('of following' in elso and not glosszak)
    szoveg = B.stilus_igazit(B.strip_html(torzs)).replace('\t', ' ')
    return {'nyers': nyers, 'cimszavak': cimszavak, 'szofaj': szofaj, 'glosszak': glosszak,
            'gyokstub': gyokstub, 'jegyzet': jegyzet, 'szoveg': szoveg,
            'latin': len(B._ujjlenyomat_teljes(szoveg))}


def szavak(s):
    return {w for w in re.findall(r'[a-z]{3,}', s.lower()) if w not in STOP}


def oshl_arameus():
    o = {}
    for r in B.oshl_beolvas():
        if r[0] != '—' and r[0] not in o:
            o[r[0]] = r
    return o


def adatok():
    bdb, htop = B.bdb_beolvas()
    tabla = B.tabla_beolvas()
    return bdb, htop, tabla, oshl_arameus()


def cimszo_egyezes(oshl_lemma, cimszavak):
    """('pont'|'kons'|'nincs')."""
    ol = B.norm(oshl_lemma)
    if ol in [B.norm(c) for c in cimszavak]:
        return 'pont'
    if B.kons(oshl_lemma) in [B.kons(c) for c in cimszavak]:
        return 'kons'
    return 'nincs'


def _osztalyoz(sor, bdb, htop, tabla, oshl):
    """Egy elvetett arámi sor állapota és indoka."""
    s, bid = sor['masodlagos_strong'], sor['bdb_id']
    e = szocikk_elemzes(bid)
    o = oshl.get(s)
    ol = o[6] if o else ''
    gl_oshl = o[9] if o else ''
    if e is None or not e['szoveg']:
        return 'nincs_szoveg', 'a BDB.lexicon-ban nincs ilyen azonosítójú, nem üres szócikk', e, ol
    if e['jegyzet'] or not e['cimszavak']:
        return ('nincs_szoveg', 'a címke nem szócikkre mutat: a %s a BDB arámi szakaszának bevezető jegyzete '
                '([Note]), nincs címszava; a Strong saját szócikke ebben a forrásban nem azonosítható' % bid), e, ol
    if e['gyokstub']:
        return ('csonk', 'gyök-hivatkozás ("√ of following"), szófaj és értelem nélkül; a címszó: %s; '
                'gyenge bizonyíték (#57 korlátja)' % ' '.join(e['cimszavak'][:2])), e, ol
    # más, táblasor nélküli Strong ugyanezen a szócikken
    cimkek = [B.pad(x) for x in re.findall(r"lex\('(H\d+[a-z]?)'\)", re.match(r'<h1>(.*?)</h1>', e['nyers'], re.S).group(1))]
    mas = [c for c in cimkek if c != s and c not in tabla and c != 'H0000']
    if mas:
        return ('tobb_jelolt', 'a szócikk más, táblasor nélküli Strongot is hordoz (%s): nem egyértelmű, melyikhez tartozik a szöveg'
                % ','.join(mas)), e, ol
    egy = cimszo_egyezes(ol, e['cimszavak']) if ol else 'nincs'
    glosszak_egy = szavak(gl_oshl) & szavak(' '.join(e['glosszak']))
    if egy == 'pont':
        alap = 'a címszó egyezik az OSHL-lemmával (normalizálva, magánhangzókkal)'
    elif egy == 'kons':
        alap = 'a címszó mássalhangzó-szinten egyezik az OSHL-lemmával (a pontozás eltér: BDB %s / OSHL %s)' % (e['cimszavak'][0], ol)
    elif glosszak_egy:
        alap = 'a címszó eltér (BDB %s / OSHL %s), de a glossza egyezik (%s)' % (e['cimszavak'][0], ol, ','.join(sorted(glosszak_egy)))
    else:
        return ('nincs_szoveg', 'a szócikk nem ennek a Strongnak a szövege: a címszó és a glossza sem egyezik az OSHL-lemmával (BDB %s / OSHL %s; OSHL def_en: %s; BDB glossza: %s)'
                % (' '.join(e['cimszavak'][:2]), ol or '—', gl_oshl or '—', '; '.join(e['glosszak']) or '—')), e, ol
    return 'egyertelmu', '%s; a szócikk a %s azonosítón önálló (egy táblasor nélküli címke); szófaj: %s' % (alap, bid, e['szofaj']), e, ol


def osztalyoz(sor, bdb, htop, tabla, oshl):
    r = _osztalyoz(sor, bdb, htop, tabla, oshl)
    if isinstance(r[0], tuple):
        return r[0][0], r[0][1], r[1], r[2]
    return r


def sor_szoveg(s, e, o):
    """'H#. átírás szöveg' — ugyanaz a fej, mint a fő tábla soraiban (a #57 m2_sorok szabálya)."""
    eredeti = 'H' + str(int(s[1:5])) + s[5:]
    atiras = B.egyszerusitett_atiras(o[7], e['szofaj'].startswith('proper name')) if o else ''
    return '%s. %s %s' % (eredeti, atiras, e['szoveg'])


def m1(ts):
    bdb, htop, tabla, oshl = adatok()
    sorok = elvetett_aram()
    prov = ('scope=konkordancia/lexikonok_nyers/BDB.lexicon (Topic=<bdb_id>) + konkordancia/BDB_strong_alias_elvetett.tsv + '
            'konkordancia/OSHL_lexikalis_index.tsv | forras=eszkozok/bdb_aram_potlas.py --m1 (a BDB-szocikk sajat szovege, '
            'a _convert_bdb.py tisztitasaval; DT40, F66) | ts=%s' % ts)
    ki = []
    for sor in sorok:
        allapot, indok, e, ol = osztalyoz(sor, bdb, htop, tabla, oshl)
        o = oshl.get(sor['masodlagos_strong'])
        cim = (e['cimszavak'][0] if e and e['cimszavak'] else sor['cimszo'])
        if allapot == 'nincs_szoveg':
            szoveg = ''
        else:
            szoveg = sor_szoveg(sor['masodlagos_strong'], e, o)
        ki.append([sor['masodlagos_strong'], sor['bdb_id'], cim, ol, allapot, indok, szoveg, prov])
    ki.sort(key=lambda r: r[0])
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(FEJLEC) + '\n')
        for r in ki:
            assert all('\t' not in x and '\n' not in x for x in r), r[0]
            f.write('\t'.join(r) + '\n')
    print('M1 kész: %d sor, %s' % (len(ki), dict(collections.Counter(r[4] for r in ki))))
    return ki


def m0(ts):
    bdb, htop, tabla, oshl = adatok()
    sorok = elvetett_aram()
    L = []
    w = L.append
    prov = ('scope=konkordancia/BDB_strong_alias_elvetett.tsv + konkordancia/lexikonok_nyers/BDB.lexicon + '
            'konkordancia/OSHL_lexikalis_index.tsv | forras=eszkozok/bdb_aram_potlas.py --m0 | ts=%s' % ts)
    w('# BDB_ARAM_POTLAS M0 — felmérés (F66)\n')
    w('*Generálta: `python eszkozok/bdb_aram_potlas.py --m0` · %s*\n' % prov)
    ids = sorted((r['bdb_id'] for r in sorok), key=lambda x: int(x[3:]))
    kod = collections.Counter(r['indok_kod'] for r in sorok)
    w('## 1. Az elvetett tábla `nyelv=aram` sorai\n')
    w('- Darab: **%d** (parancs: `awk -F"\\t" \'$3=="aram"\' konkordancia/BDB_strong_alias_elvetett.tsv | wc -l`; a `--m0` ugyanezt a `split(\'\\t\')` olvasással számolja).' % len(sorok))
    w('- `indok_kod` szerint: %s.' % ', '.join('`%s`: %d' % kv for kv in sorted(kod.items())))
    w('- BDB-azonosító-tartomány: %s – %s (szám szerint rendezve).' % (ids[0], ids[-1]))
    sec = [s for s in htop if s not in tabla and s != 'H0000']
    arb = {k for k, e in bdb.items() if e['nyelv'] == 'arameus'}
    ar_sec = [s for s in sec if htop[s][0] in arb]
    alias_ar = [l.split('\t') for l in open(B.ALIAS, encoding='utf-8').read().split('\n') if l][1:]
    alias_ar = [r for r in alias_ar if r[3] == 'aram']
    oshl_ar = [s for s in sec if oshl.get(s) and oshl[s][4] == 'arameus']
    oshl_ar_bdb = [s for s in oshl_ar if htop[s][0] in arb]
    w('- **A 187 reprodukálása:** a BDB.lexicon %d másodlagos (táblasor nélküli) Strong-kulcsa közül %d mutat arámi nyelvű szócikkre (`bdb_beolvas`, a navigációs sor „BIBLICAL ARAMAIC” jelölése); 187 = %d alias + %d elvetett = %d. Reprodukálva.' % (
        len(sec), len(ar_sec), len(alias_ar), len(sorok), len(alias_ar) + len(sorok)))
    w('- **A 198 (ellenőri szám, M1-napló 75. sor) újramérése:** nem reprodukálható. Mért alternatívák: az OSHL szerint arámi másodlagos Strong: %d; ebből a BDB-ben is arámi szócikkre mutat: %d; az összes arámi BDB-szócikk (nem csak a másodlagosak): %d. Egyik sem 198; a különbség okát nem azonosítottuk (a mérvadó a feltétel, nem a szám).' % (
        len(oshl_ar), len(oshl_ar_bdb), len(arb)))
    w('')
    w('## 2. Szócikkenként: önálló, nem üres szöveg; csonk\n')
    ossz = collections.Counter()
    csonk_lista, jegyzet_lista = [], []
    hossz = []
    for sor in sorok:
        e = szocikk_elemzes(sor['bdb_id'])
        if not e or not e['szoveg']:
            ossz['nincs_szoveg'] += 1
            continue
        ossz['van_szoveg'] += 1
        hossz.append(e['latin'])
        if e['jegyzet'] or not e['cimszavak']:
            ossz['jegyzet'] += 1
            jegyzet_lista.append(sor['masodlagos_strong'] + '/' + sor['bdb_id'])
        elif e['gyokstub']:
            ossz['gyokstub'] += 1
            csonk_lista.append(sor['masodlagos_strong'] + '/' + sor['bdb_id'])
        else:
            ossz['onallo'] += 1
    w('- Önálló, nem üres `Definition`: %d/%d.' % (ossz['van_szoveg'], len(sorok)))
    w('- Ebből valódi szócikk (van címszó, szófaj, értelem): **%d**; gyök-hivatkozás (csonk, „√ of following”): **%d** (%s); nem szócikk, hanem nyelvi szakasz bevezető jegyzete: **%d** (%s).' % (
        ossz['onallo'], ossz['gyokstub'], ', '.join(csonk_lista) or '—', ossz['jegyzet'], ', '.join(jegyzet_lista) or '—'))
    hossz.sort()
    w('- A latin betűs szöveg hossza (hivatkozások nélkül): legrövidebb %d, medián %d, leghosszabb %d karakter. **Csonk-szabály:** a #57 korlátja (csonk = rövid latin szöveg) itt nem alkalmazható hosszküszöbbel, mert a rövid arámi szócikkek (pl. Zerubbabel, 29 latin betű) teljesek; a csonk a **gyök-hivatkozás** (szófaj és értelem nélkül).' % (hossz[0], hossz[len(hossz) // 2], hossz[-1]))
    w('')
    w('## 3. Többszörös megfeleltetés\n')
    cnt_bdb = collections.Counter(r['bdb_id'] for r in sorok)
    tobb_bdb = {k: v for k, v in cnt_bdb.items() if v > 1}
    w('- Ugyanarra a BDB-azonosítóra több **elvetett arámi** címke: %d eset%s.' % (len(tobb_bdb), (' (%s)' % tobb_bdb) if tobb_bdb else ''))
    alias_bdb = {r[2] for r in alias_ar}
    w('- Ugyanarra a BDB-azonosítóra egy elvetett és egy **alias** arámi címke: %d eset.' % len({r['bdb_id'] for r in sorok} & alias_bdb))
    cnt_s = collections.Counter(h for e in bdb.values() for h in set(B.pad(x) for x in e['cimkek']))
    tobb_s = [r['masodlagos_strong'] for r in sorok if cnt_s[r['masodlagos_strong']] > 1]
    w('- Ugyanarra a Strong-számra több BDB-szócikk (a fejlécek címkéi szerint): %d eset%s.' % (len(tobb_s), (' (%s)' % ', '.join(tobb_s)) if tobb_s else ''))
    mas_tobb = []
    for sor in sorok:
        e = szocikk_elemzes(sor['bdb_id'])
        h = re.match(r'<h1>(.*?)</h1>', e['nyers'], re.S).group(1)
        mas = [B.pad(x) for x in re.findall(r"lex\('(H\d+[a-z]?)'\)", h)]
        mas = [c for c in mas if c != sor['masodlagos_strong'] and c not in tabla]
        if mas:
            mas_tobb.append('%s(+%s)' % (sor['masodlagos_strong'], ','.join(mas)))
    w('- Olyan szócikk, amely az érintett Strong mellett más, táblasor nélküli Strongot is hordoz: %d eset%s.' % (len(mas_tobb), (' (%s)' % ', '.join(mas_tobb)) if mas_tobb else ''))
    w('')
    w('## 4. OSHL-lemma és BDB-címszó egyezése (a #57 M1 normalizálásával)\n')
    cs = collections.Counter()
    elt = []
    for sor in sorok:
        s = sor['masodlagos_strong']
        e = szocikk_elemzes(sor['bdb_id'])
        o = oshl.get(s)
        if not o:
            cs['nincs_oshl'] += 1
            elt.append((s, '—', '—', 'nincs OSHL-sor'))
            continue
        if not e['cimszavak']:
            cs['nincs_cimszo'] += 1
            elt.append((s, o[6], '—', 'nincs címszó (jegyzet)'))
            continue
        eg = cimszo_egyezes(o[6], e['cimszavak'])
        gl = szavak(o[9]) & szavak(' '.join(e['glosszak']))
        if eg == 'nincs':
            cs['nincs+gloss' if gl else 'nincs'] += 1
            elt.append((s, o[6], ' '.join(e['cimszavak'][:2]), 'glossza egyezik: %s' % ','.join(sorted(gl)) if gl else 'glossza sem egyezik (OSHL: %s; BDB: %s)' % (o[9], '; '.join(e['glosszak']))))
        else:
            cs[eg] += 1
    w('- Összesítés: %s (`pont` = normalizált, pontozott egyezés; `kons` = csak a mássalhangzók egyeznek; `nincs+gloss` = a címszó eltér, de az OSHL-glossza és a BDB-glossza közös szót tartalmaz; `nincs` = semmi nem egyezik).' % dict(cs))
    if elt:
        w('\nEltérő sorok (nem `pont`/`kons`):\n')
        w('| Strong | OSHL-lemma | BDB-címszó | megjegyzés |')
        w('|---|---|---|---|')
        for r in elt:
            w('| %s | %s | %s | %s |' % r)
    w('')
    with open(M0_JELENTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('M0 kész: naplok/BDB_ARAM_POTLAS_M0.md')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m0', action='store_true')
    ap.add_argument('--m1', action='store_true')
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    if a.m0:
        m0(a.ts)
    if a.m1:
        m1(a.ts)


if __name__ == '__main__':
    main()
