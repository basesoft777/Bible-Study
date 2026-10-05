#!/usr/bin/env python
"""A BDB-tábla hiányzó szócikkei (F57, #57): M0 felmérés, M1 párosítás.

Forrás: konkordancia/lexikonok_nyers/BDB.lexicon (SQLite, csak olvasás),
konkordancia/BDB_teljes_unabridged.tsv (a meglévő tábla),
konkordancia/OSHL_lexikalis_index.tsv (lemma, Strong), konkordancia/TAHOT_kivonat.tsv.

Módok:
  --m0       felmérés: naplok/BDB_STRONG_POTLAS_M0.md
  --m1       párosítás: konkordancia/BDB_strong_potlas.tsv
  --alias    másodlagos H-címkék alias-táblája: konkordancia/BDB_strong_alias.tsv
  --m1-szakasz  az M1-jelentés 3. (alias) szakaszának újragenerálása
  --m2       az egyértelmű párok sorainak hozzáfűzése a BDB_teljes_unabridged.tsv-hez (csak új sorok)

Az --m0 és --m1 csak olvas a BDB-táblából; az --m2 ÍR a BDB_teljes_unabridged.tsv-be
(csak a jóváhagyott párok sorait cseréli/fűzi hozzá a végén, a meglévő sorok bájtra
változatlanok, idempotens), az --alias két új TSV-t ír (alias és elvetett lista).
A TSV-ket split('\t')-tel olvassa.
Alias-feltétel (DT-F57f/g): a másodlagos címke testvér-Strongjának táblasora ugyanabból a
BDB-szócikkből származik (a testvér H-kulcsának bdb_id-je egyezik a másodlagos címke
bdb_id-jével), a szócikk latin betűinek legalább 0,9 hányada a testvérsor elején megvan
(hivatkozások és héber szöveg nélkül), és pontosan egy testvér felel meg; ami elbukik, az
elvetett listára kerül (nyelvi szűrés nincs; kézi kivételek: KIZART).
"""
import sys
import os
import re
import sqlite3
import unicodedata
import collections
import datetime
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'BDB.lexicon')
TABLA = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
OSHL = os.path.join(GYOKER, 'konkordancia', 'OSHL_lexikalis_index.tsv')
TAHOT = os.path.join(GYOKER, 'konkordancia', 'TAHOT_kivonat.tsv')
POTLAS = os.path.join(GYOKER, 'konkordancia', 'BDB_strong_potlas.tsv')
M0_JELENTES = os.path.join(GYOKER, 'naplok', 'BDB_STRONG_POTLAS_M0.md')
M1_JELENTES = os.path.join(GYOKER, 'naplok', 'BDB_STRONG_POTLAS_M1.md')

FEJLEC = ['bdb_id', 'strong', 'cimszo', 'oshl_lemma', 'allapot', 'indok', 'proveniencia']
STOP = {'the', 'and', 'for', 'with', 'from', 'that', 'this', 'into', 'one', 'any', 'etc'}


def pad(t):
    m = re.match(r'H(\d+)(.*)$', t)
    return 'H%04d' % int(m.group(1)) + m.group(2)


def norm(s):
    """Héber címszó normalizálása (BRIEF §3 M1/1)."""
    s = unicodedata.normalize('NFD', s)
    s = s.replace('ֺ', 'ֹ')            # holem haser for vav -> holem
    out = []
    for ch in s:
        o = ord(ch)
        if 0x0591 <= o <= 0x05AF:                # kantillációs jelek
            continue
        if o in (0x05BD, 0x05BF, 0x05C0, 0x05C3, 0x05C4, 0x05C5, 0x200E, 0x200F, 0x05BE):
            continue                             # meteg, rafe, paszeq, sof paszuk, maqaf stb.
        if not (0x05B0 <= o <= 0x05EA):
            if ch in " ,.;׳'\"()[]":
                continue
        out.append(ch)
    s = ''.join(out)
    return unicodedata.normalize('NFC', s)


def kons(s):
    return ''.join(ch for ch in unicodedata.normalize('NFD', s) if 0x05D0 <= ord(ch) <= 0x05EA)


def tisztit(x):
    x = re.sub(r'<[^>]+>', ' ', x)
    x = x.replace('&amp;', '&')
    return re.sub(r'\s+', ' ', x).strip()


def bdb_beolvas():
    """BDB-azonosítós szócikkek: azonosító, címkék, címszavak, szófaj, glosszák."""
    con = sqlite3.connect('file:%s?mode=ro' % LEX.replace('\\', '/'), uri=True)
    cur = con.cursor()
    bdb = {}
    for t, d in cur.execute("select Topic,Definition from Lexicon where Topic like 'BDB%'"):
        h = re.match(r'<h1>(.*?)</h1>', d)
        fej = h.group(1) if h else ''
        cimkek = re.findall(r"lex\('(H\d+[a-z]?)'\)", fej)
        nav = re.search(r'</h1><div class="navigation">.*?\|(.*?)\|.*?</div>', d)
        nyelv = 'arameus' if nav and 'ARAMAIC' in nav.group(1) else 'heber'
        torzs = d[h.end():] if h else d
        torzs = re.sub(r'<div class="navigation">.*?</div>', '', torzs, count=1)
        p = re.search(r'<p>(.*?)(</p>|$)', torzs, re.S)
        elso = p.group(1) if p else ''
        # címszavak: a szófaj-jelölő (<b>) előtti <bdbheb> elemek
        b = re.search(r'<b>', elso)
        elotte = elso[:b.start()] if b else elso[:400]
        cimre = r'<bdb(?:heb|arc)>(.*?)</bdb(?:heb|arc)>'
        cimszavak = re.findall(cimre, elotte) or re.findall(cimre, elso)[:1]
        homonima = re.match(r'\s*([IVX]+)\.\s', tisztit(elso))
        szofaj = tisztit(re.search(r'<b>(.*?)</b>', elso).group(1)) if b else ''
        glosszak = [tisztit(g) for g in re.findall(r'<highlightword>(.*?)</highlightword>|<highlight>(.*?)</highlight>', elso)
                    for g in [g[0] or g[1]]]
        gyokstub = (not b) and ('of following' in elso or '√' in elso)
        bdb[t] = {'id': t, 'cimkek': cimkek, 'nyelv': nyelv, 'cimszavak': cimszavak,
                  'homonima': homonima.group(1) if homonima else '', 'szofaj': szofaj,
                  'glosszak': glosszak, 'gyokstub': gyokstub}
    htop = {}
    for t, d in cur.execute("select Topic,Definition from Lexicon where Topic like 'H%'"):
        h = re.match(r'<h1>(.*?)</h1>', d)
        fej = h.group(1) if h else ''
        m = re.search(r"bdbid\('(BDB\d+)'\)", fej)
        htop[pad(t)] = (m.group(1) if m else '', [pad(x) for x in re.findall(r"lex\('(H\d+[a-z]?)'\)", fej)])
    con.close()
    return bdb, htop


def tabla_beolvas():
    sorok = {}
    with open(TABLA, encoding='utf-8', newline='') as f:
        szoveg = f.read()
    for sor in szoveg.split('\n')[1:]:
        if sor:
            sorok[sor.split('\t')[0]] = sor
    return sorok


def oshl_beolvas():
    sorok = []
    with open(OSHL, encoding='utf-8') as f:
        for sor in f.read().split('\n'):
            if not sor or sor.startswith('#'):
                continue
            sorok.append(sor.split('\t'))
    return sorok[1:]


def tahot_szamlalo():
    szam = collections.Counter()
    with open(TAHOT, encoding='utf-8') as f:
        for sor in f:
            m = sor.split('\t', 2)
            if len(m) > 2:
                szam[m[1]] += 1
    return szam


def tahot_db(szam, strong):
    return szam.get(strong, 0)


def szavak(s):
    return {w[:-1] if w.endswith('s') and len(w) > 4 else w
            for w in re.findall(r'[a-z]+', s.lower()) if len(w) > 2 and w not in STOP}


def adatok():
    bdb, htop = bdb_beolvas()
    tabla = tabla_beolvas()
    oshl = oshl_beolvas()
    cimkenelkuli = [e for e in bdb.values() if not e['cimkek']]
    cimkezett_strongok = set(htop)
    oshl_strongok = {}
    for r in oshl:
        s, nyelv, lemma, defen = r[0], r[4], r[6], r[9]
        if s == '—' or s in oshl_strongok:
            continue
        oshl_strongok[s] = {'strong': s, 'nyelv': nyelv, 'lemma': lemma, 'def_en': defen, 'bdb_id': r[3]}
    return bdb, htop, tabla, oshl, cimkenelkuli, cimkezett_strongok, oshl_strongok


def parosit(ts):
    bdb, htop, tabla, oshl, cimkenelkuli, cimkezett, oshl_s = adatok()
    jeloltek = {s: v for s, v in oshl_s.items() if s not in tabla and s not in cimkezett}
    prov = 'scope=konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/OSHL_lexikalis_index.tsv + konkordancia/BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py (cimszo-egyezes) | ts=%s' % ts
    return parosit_mag(bdb, cimkenelkuli, jeloltek), prov, (bdb, htop, tabla, oshl_s, jeloltek)


def parosit_mag(bdb, cimkenelkuli, jeloltek):
    """A párosítás magja (tesztelhető): címke nélküli szócikkek x jelölt Strongok."""
    index = collections.defaultdict(list)
    for s, v in jeloltek.items():
        index[(v['nyelv'], norm(v['lemma']))].append(s)
    jeloltek_kons = collections.defaultdict(list)
    for s, v in jeloltek.items():
        jeloltek_kons[(v['nyelv'], kons(v['lemma']))].append(s)
    elozetes = []
    for e in sorted(cimkenelkuli, key=lambda x: int(x['id'][3:])):
        cimsz = e['cimszavak'][0] if e['cimszavak'] else ''
        if e['gyokstub']:
            elozetes.append((e, cimsz, [], 'nincs_par', 'gyök-hivatkozás (szófaj nélküli "√ of following" szócikk)'))
            continue
        jel = []
        for cs in e['cimszavak'][:1]:
            jel = list(index.get((e['nyelv'], norm(cs)), []))
        elozetes.append((e, cimsz, jel, None, ''))
    # fordított szám: hány címke nélküli BDB-szócikk céloz ugyanarra a Strongra
    cel = collections.defaultdict(list)
    for e, cs, jel, st, ind in elozetes:
        for s in jel:
            cel[s].append(e['id'])
    kidx = collections.defaultdict(list)
    for e, cs, jel, st, ind in elozetes:
        if cs:
            kidx[(e['nyelv'], kons(cs))].append(e['id'])
    eredmeny = []
    for e, cs, jel, st, ind in elozetes:
        if st:
            eredmeny.append((e, cs, '', '', st, ind))
            continue
        if not jel:
            tipp = ''
            if cs:
                kj = [x for x in jeloltek_kons.get((e['nyelv'], kons(cs)), [])]
                if kj:
                    tipp = '; tipp (csak mássalhangzó-egyezés, a pontozás eltér, nem párosítás): %s' % ','.join(kj)
            eredmeny.append((e, cs, '', '', 'nincs_par', 'nincs egyező OSHL-lemma a hiányzó Strong-számok között (%s)%s' % (e['nyelv'], tipp)))
            continue
        if len(jel) == 1 and len(cel[jel[0]]) == 1:
            s = jel[0]
            eredmeny.append((e, cs, s, jeloltek[s]['lemma'], 'egyertelmu',
                             'egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: %s | OSHL def_en: %s'
                             % ('; '.join(e['glosszak'][:2]) or '—', jeloltek[s]['def_en'])))
            continue
        # homonímia: glossza-egyezés dönt
        bgl = set()
        for g in e['glosszak']:
            bgl |= szavak(g)
        talalt = [s for s in jel if bgl & szavak(jeloltek[s]['def_en'])]
        # a döntés csak akkor érvényes, ha a Strong oldaláról is egyetlen BDB-szócikk marad
        if len(talalt) == 1:
            s = talalt[0]
            versenytarsak = []
            for oid in cel[s]:
                if oid == e['id']:
                    continue
                e2 = bdb[oid]
                g2 = set()
                for g in e2['glosszak']:
                    g2 |= szavak(g)
                if g2 & szavak(jeloltek[s]['def_en']):
                    versenytarsak.append(oid)
            if not versenytarsak:
                eredmeny.append((e, cs, s, jeloltek[s]['lemma'], 'egyertelmu',
                                 'homonímia, a glossza dönt (közös szó: %s); BDB: %s | OSHL def_en: %s'
                                 % (', '.join(sorted(bgl & szavak(jeloltek[s]['def_en']))),
                                    '; '.join(e['glosszak'][:2]) or '—', jeloltek[s]['def_en'])))
                continue
        eredmeny.append((e, cs, ','.join(jel), jeloltek[jel[0]]['lemma'], 'tobb_jelolt',
                         'a glossza nem dönt (%d Strong-jelölt, %d BDB-jelölt a Strongra); BDB: %s | OSHL: %s'
                         % (len(jel), max(len(cel[s]) for s in jel), '; '.join(e['glosszak'][:2]) or '—',
                            ' / '.join('%s %s' % (s, jeloltek[s]['def_en']) for s in jel))))
    return eredmeny


def m1(ts):
    eredmeny, prov, _ = parosit(ts)
    with open(POTLAS, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(FEJLEC) + '\n')
        for e, cs, s, lem, st, ind in eredmeny:
            mezok = [e['id'], s, cs, lem, st, ind.replace('\t', ' '), prov]
            f.write('\t'.join(mezok) + '\n')
    szam = collections.Counter(r[4] for r in eredmeny)
    m1_jelentes(eredmeny, prov, ts)
    print('M1 kész:', len(eredmeny), 'sor', dict(szam), '->', os.path.relpath(POTLAS, GYOKER))


HASONLOSAG_KUSZOB = 0.9  # DT-F57f: a szócikk eleje a testvérsor elején
ELEJE_MAX = 1500
FEJ_ENGEDMENY = 60


def _ujjlenyomat_teljes(x):
    """Összehasonlítási ujjlenyomat (DT-F57g): CSAK latin betűk.

    A héber szöveg kimarad, mert a DictBDB a többszavas héber kifejezések szórendjét megfordítja
    (pl. H3347: ugyanaz a szöveg fordított sorrendben); a bibliai hivatkozások (könyvrövidítés +
    szám) is kimaradnak, mert a két forrás eltérően rövidíti és tömöríti őket (1Kgs/1Kin,
    13:20 ; 13:21 / 13:20-21)."""
    x = re.sub(r'\b[0-9]?[A-Z][a-z]{1,9}[.]? *(?=[0-9])', '', x)
    return re.sub(r'[^A-Za-z]', '', x)


def _ujjlenyomat(x):
    return _ujjlenyomat_teljes(x)


def elejegyezes(forras, sorszoveg):
    """Mérőszám (DT-F57f/g): a szócikk ujjlenyomatának (latin betűk; legfeljebb ELEJE_MAX karakter)
    az a hányada, amely a testvérsor elején megvan.

    Pontosan: a = a szócikk ujjlenyomata[:ELEJE_MAX]; b = a testvérsor (a `H<n>.` előtag nélküli)
    ujjlenyomata[:len(a) + FEJ_ENGEDMENY] (a sorfej, azaz az átírás miatti +60 karakteres ablak);
    érték = a `difflib.SequenceMatcher(None, a, b, autojunk=False)` egyező blokkjai karakterszámának
    összege / len(a). A szócikknek tehát nem kell az egész sorral egyeznie (a DictBDB-sor a saját
    szócikke után további szócikkeket is tartalmazhat). Csonk szócikknél (rövid `a`) az egyezés
    triviálisan magas lehet (pl. BDB515, BDB3121); ez az alias oldalán nem okozott hamis aliast a
    mintában, de a mérőszám ott gyenge bizonyíték."""
    import difflib
    a = forras[:ELEJE_MAX]
    if not a:
        return 0.0
    sor = re.sub(r'^H[0-9]+[a-z]?[.]', '', sorszoveg)
    b = _ujjlenyomat_teljes(sor)[:len(a) + FEJ_ENGEDMENY]
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(blk.size for blk in m.get_matching_blocks()) / len(a)


# Kézzel kint tartott sorok (DT-F57g/i), függetlenül a mérőszámtól: Strong -> (indok-kód, magyarázat)
KIZART = {
    'H2088': ('kifejezes_tarscimke', 'a BDB6199 fejlécében [H6258 H2088 H2009 H5704 H3588] a „zeh” egy attá-kifejezés miatt kapott társcímkét; a saját szócikke máshol van, ezért valódi téves alias volna (a BDB6199 az עַתָּה szócikke)'),
}

# Az elvetett lista gépi indok-kódjai (az `indok_kod` oszlopban; a magyarázat az `indok` oszlopban)
INDOK_KODOK = ('nincs_testver', 'nem_ebbol_a_szocikkbol', 'kuszob_alatt', 'a_testversor_mas_szocikk',
               'tobb_testveres', 'kifejezes_tarscimke')


def _heber_kons_eleje(sorszoveg, n):
    """A testvérsor első n héber mássalhangzója (a sorfej és a latin szöveg átugorva)."""
    sorszoveg = unicodedata.normalize('NFD', sorszoveg)  # a prezentációs formák (pl. U+FB2A) bontása
    hu = ''.join(ch for ch in sorszoveg if 0x05D0 <= ord(ch) <= 0x05EA or ch == ' ')
    return kons(hu.strip())[:n]


def alias_szetvalogat():
    """A másodlagos H-címkék szétválogatása (DT-F57c, F57f, F57g, F57h): (alias_sorok, elvetett_sorok).

    Alias-feltétel: (1) a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér
    H-kulcsának bdb_id-je egyezik a másodlagos címke bdb_id-jével); (2) a szócikk latin betűinek
    legalább HASONLOSAG_KUSZOB (0,9) hányada a testvérsor elején megvan (elejegyezes); (3) ha több
    azonos szócikkbeli testvér van, pontosan EGY felel meg a (2)-nek (az az alias célja; 2+ megfelelő
    esetén `tobb_testveres`, elvetve); (4) a KIZART kézi kivételek kint maradnak. Nyelvi szűrés nincs.
    Elvetett indok-kódok: l. INDOK_KODOK.
    """
    bdb, htop, tabla, oshl, cimkenelkuli, cimkezett, oshl_s = adatok()
    alias_sorok, elvetett = [], []

    def kiesik(s, bid, nyelv, hw, tars, kod, indok, meres=''):
        elvetett.append({'s': s, 'bid': bid, 'nyelv': nyelv, 'hw': hw, 'tars': tars, 'kod': kod,
                         'indok': indok, 'meres': meres})

    for s in sorted(htop):
        if s in tabla or s == 'H0000':
            continue
        bid, ls = htop[s]
        e = bdb.get(bid)
        nyelv = 'aram' if e and e['nyelv'] == 'arameus' else 'heber'
        hw = e['cimszavak'][0] if e and e['cimszavak'] else ''
        tars = [x for x in ls if x != s and x in tabla]
        if not tars:
            kiesik(s, bid, nyelv, hw, '', 'nincs_testver', 'nincs testvér-Strong a táblában')
            continue
        azonos = [t for t in tars if htop.get(t, ('',))[0] == bid]
        if not azonos:
            kiesik(s, bid, nyelv, hw, ','.join(tars), 'nem_ebbol_a_szocikkbol',
                   'a testvér-sor nem ebből a BDB-szócikkből származik (a testvér H-kulcsa: %s)'
                   % ','.join(sorted({htop.get(t, ('?',))[0] for t in tars})))
            continue
        forras = _ujjlenyomat(strip_html(lexikon_torzs(bid)))
        mert = [(t, elejegyezes(forras, tabla[t].split('\t', 2)[2])) for t in azonos]
        jo = [(t, r) for t, r in mert if r >= HASONLOSAG_KUSZOB]
        legjobb_t, legjobb = max(mert, key=lambda x: x[1])
        if s in KIZART:
            kod, mag = KIZART[s]
            kiesik(s, bid, nyelv, hw, ','.join(azonos), kod, '%s; elejegyezés %.3f' % (mag, legjobb), '%.3f' % legjobb)
            continue
        if not jo:
            sor = tabla[legjobb_t].split('\t', 2)[2]
            kh = kons(hw)
            ugyanaz = bool(kh) and _heber_kons_eleje(sor, len(kh)) == kh
            if ugyanaz:
                kiesik(s, bid, nyelv, hw, ','.join(azonos), 'kuszob_alatt',
                       'küszöb alatt (%.3f < %.1f), a testvérsor ugyanazzal a címszóval kezdődik; jelöltként marad, egyedi beemelésre javasolt'
                       % (legjobb, HASONLOSAG_KUSZOB), '%.3f' % legjobb)
            else:
                kiesik(s, bid, nyelv, hw, ','.join(azonos), 'a_testversor_mas_szocikk',
                       'a testvérsor más szócikk (a bdb_id egyezik, de a szócikk szövege nem a testvérsor elején áll, '
                       'és a testvérsor nem ugyanazzal a címszóval kezdődik; elejegyezés %.3f, a feltétel: >= %.1f)'
                       % (legjobb, HASONLOSAG_KUSZOB), '%.3f' % legjobb)
            continue
        if len(jo) > 1:
            kiesik(s, bid, nyelv, hw, ','.join(t for t, _ in jo), 'tobb_testveres',
                   'több testvér-Strong sora is megfelel a szövegfeltételnek (%s): nem egyértelmű, melyik az alias célja'
                   % ','.join('%s %.3f' % (t, r) for t, r in jo), '%.3f' % max(r for _, r in jo))
            continue
        alias_sorok.append({'s': s, 'bid': bid, 'nyelv': nyelv, 'hw': hw, 'tars': jo[0][0],
                            'hasonlosag': '%.3f' % jo[0][1]})
    return alias_sorok, elvetett


def masodlagos_lista():
    return alias_szetvalogat()


def masodlagos_szakasz():
    """Az M1-jelentés 3. szakasza (DT-F57c/F57f/F57g/F57h szerint: alias és elvetett lista)."""
    alias_sorok, elvetett = alias_szetvalogat()
    ossz = len(alias_sorok) + len(elvetett)
    nyelv_a = collections.Counter(r['nyelv'] for r in alias_sorok)
    nyelv_e = collections.Counter(r['nyelv'] for r in elvetett)
    ok_e = collections.Counter(r['kod'] for r in elvetett)
    nyelv_ok = collections.Counter((r['kod'], r['nyelv']) for r in elvetett)
    L = []
    w = L.append
    w('\n## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora (DT-F57a, DT-F57c, DT-F57f, DT-F57g, DT-F57h)\n')
    w('- %d Strong (a H0136 és a H0341 is ide tartozik): a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong másik Strong mellett áll, ezért a 3. kizárási szabály miatt nem párosítható.' % ossz)
    w('- **Alias-feltétel (DT-F57f/g/h, nyelvi szűrés nélkül):** (1) a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér `H<n>` kulcsának `bdb_id`-je egyezik a másodlagos címke `bdb_id`-jével); (2) **mérőszám** (`elejegyezes`): a szócikk ujjlenyomatának (CSAK latin betűk; a héber szöveg és a bibliai hivatkozások kimaradnak; legfeljebb %d karakter) az a hányada, amely a testvérsor elején megvan: a testvérsor (a `H<n>.` előtag nélküli) ujjlenyomatának első `hossz + %d` karaktere az ablak, az érték a `difflib.SequenceMatcher` egyező blokkjainak karakterszáma osztva a szócikk ujjlenyomatának hosszával; **küszöb ≥ %.1f**; (3) ha több azonos szócikkbeli testvér van, pontosan **egy** felel meg a (2)-nek, és az az alias célja (2+ megfelelő esetén `tobb_testveres`, elvetve; ilyen sor jelenleg nincs); (4) a kézi kivételek (`KIZART`) kint maradnak.' % (ELEJE_MAX, FEJ_ENGEDMENY, HASONLOSAG_KUSZOB))
    w('- A héber szöveg azért marad ki, mert a DictBDB a többszavas héber kifejezések szórendjét megfordítja (pl. H3347: ugyanaz a szöveg fordított sorrendben); a hivatkozások azért, mert a két forrás eltérően rövidíti őket (1Kgs/1Kin, 13:20 ; 13:21 / 13:20-21). Korlát: csonk szócikknél (rövid latin szöveg, pl. BDB515, BDB3121) az egyezés triviálisan magas lehet; az alias oldalán a mintában ebből hamis alias nem lett, de a mérőszám ott gyenge bizonyíték.')
    w('- **Az alias azt mondja meg, hol áll a BDB-szövege, nem azt, hogy a két szó azonos.** Pl. az Abel-összetett helynevek (H0059, H0063–H0067) a H0058 ʾābēl sorára oldódnak fel, mert a BDB alpontként tárgyalja őket.')
    w('- A H3071, H3073, H3074 (JHVH-nisszí, JHVH-sálóm, JHVH-sammá; a BDB a második tag szócikkében tárgyalja őket: נֵס, שָׁלוֹם, שָׁם) alias: ugyanaz a minta, mint az Abel-helyneveknél; az alias azt mondja meg, hol áll a BDB-szövege, nem azt, hogy a két szó azonos (DT-F57i).')
    w('- **Alias** (`konkordancia/BDB_strong_alias.tsv`): %d sor (héber %d, arámi %d). **Elvetett, jelölt marad** (`konkordancia/BDB_strong_alias_elvetett.tsv`): %d sor (héber %d, arámi %d).' % (
        len(alias_sorok), nyelv_a['heber'], nyelv_a['aram'], len(elvetett), nyelv_e['heber'], nyelv_e['aram']))
    w('- Elvetés oka (az `indok_kod` oszlop kódjai; darab, ebből arámi): %s.' % '; '.join('`%s`: %d (arámi %d)' % (k, v, nyelv_ok[(k, 'aram')]) for k, v in sorted(ok_e.items())))
    tobb = sum(1 for r in alias_sorok if ',' in r['tars'])
    w('- Több testvéres sor a megmaradt %d aliasban: **%d** (ellenőrizve). A `testver_strong` oszlop az elvetett listán csak az azonos szócikkbeli testvéreket sorolja fel (kivéve a `nem_ebbol_a_szocikkbol` sorokat, ahol nincs ilyen: ott a más szócikkből származó testvérek állnak).' % (len(alias_sorok), tobb))
    w('- **Az elvárástól való eltérés (DT-F57h/i).** A várakozás kb. 294 alias volt (a DT-F57h ~291 + a H3071, H3073, H3074); a tényleges szám **%d**: a H5853 és a H5855 → H5852 a szabály szerint alias (mérőszám 0,981: a H5852 sora szó szerint a BDB5999 szócikke), nem `kuszob_alatt` (az előzetes felhasználói mérés 0,86 volt). A két sor az aliasban van; ha mégis kint kellene tartani őket, a `KIZART` bővítendő.' % len(alias_sorok))
    w('- **Külön listázott sorok (a felhasználó ellenőrizheti; a mérőszám három tizedessel):**\n')
    w('| Strong | testvér | bdb_id | kimenet | mérőszám / indok |')
    w('|---|---|---|---|---|')
    ae = {r['s']: r for r in alias_sorok}
    ee = {r['s']: r for r in elvetett}
    for sid in ('H3347', 'H3606', 'H2088', 'H3071', 'H3073', 'H3074', 'H8550', 'H6990', 'H0206', 'H7929', 'H5853', 'H5855', 'H8625'):
        if sid in ae:
            r = ae[sid]
            w('| %s | %s | %s | alias | %s |' % (sid, r['tars'], r['bid'], r['hasonlosag']))
        elif sid in ee:
            r = ee[sid]
            w('| %s | %s | %s | elvetett | %s |' % (sid, r['tars'], r['bid'], r['indok'].replace('|', '/')))
    w('')
    ku = [r for r in elvetett if r['kod'] == 'kuszob_alatt']
    w('- **`kuszob_alatt` sorok (%d):** a testvérsor ugyanazzal a címszóval kezdődik, de a mérőszám a küszöb (%.1f) alatt van; jelöltként maradnak. A #57-ben nincs egyenkénti beemelés (DT-F57i); az `indok_kod` oszlop `kuszob_alatt` értéke szűrhető, egy későbbi feladat beemelheti őket.\n' % (len(ku), HASONLOSAG_KUSZOB))
    w('| Strong | testvér | bdb_id | címszó | mérőszám |')
    w('|---|---|---|---|---|')
    for r in ku:
        w('| %s | %s | %s | %s | %s |' % (r['s'], r['tars'], r['bid'], r['hw'], r['meres']))
    w('')
    w('- **Arámi szócikkek: két szám összevetése.** A BDB.lexicon nyelvjelölése szerint a 529 másodlagos címke között **%d** arámi szócikk van (BDB9264-től; ez a felhasználó 187-es száma). A független ellenőr 198-at talált; ez a szám a BDB.lexicon nyelvjelöléséből nem reprodukálható (a legközelebbi mérések: arámi szócikk 187; arámi másodlagos OSHL-Strong héber testvérsorral 174), a különbség (11) okát nem tudtuk azonosítani. Mérvadó a feltétel, nem a szám: az arámi szócikkek közül %d kerül elvetésre (ebből `nem_ebbol_a_szocikkbol`: %d, `a_testversor_mas_szocikk`: %d), %d marad aliasban.' % (
        nyelv_a['aram'] + nyelv_e['aram'], nyelv_e['aram'], nyelv_ok[('nem_ebbol_a_szocikkbol', 'aram')],
        nyelv_ok[('a_testversor_mas_szocikk', 'aram')], nyelv_a['aram']))
    w('- **Nyitott tétel:** (DT-F57d) az elvetett arámi szócikkek tényleges pótlása (a BDB.lexicon szövegéből új táblasorok) külön feladat a `/befogad` útján, nem az F57 része.\n')
    return L


def m1_szakasz_frissit():
    """Az M1-jelentés 3. szakaszának újragenerálása a meglévő jelentésben (az --m1 nélkül)."""
    with open(M1_JELENTES, encoding='utf-8') as f:
        szoveg = f.read()
    i = szoveg.index('\n## 3. ')
    uj = szoveg[:i] + '\n'.join(masodlagos_szakasz()).rstrip('\n') + '\n'
    with open(M1_JELENTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write(uj)
    print('M1-jelentés 3. szakasza frissítve')


def m1_jelentes(eredmeny, prov, ts):
    szam = collections.Counter(r[4] for r in eredmeny)
    L = []
    w = L.append
    w('# BDB_STRONG_POTLAS M1 — párosítás (F57)\n')
    w('*Generálta: `python eszkozok/bdb_strong_potlas.py --m1` · %s*\n' % prov)
    w('## 1. Párosítási szabály (szó szerint, BRIEF §3 M1)\n')
    w('1. Címszó-egyezés: az OSHL-lemma és a BDB-címszó normalizált alakja egyezik; a normalizálás egységesíti a holem-waw írásváltozatokat (U+05BA -> U+05B9), eltávolítja a kantillációs jeleket (U+0591-05AF) és a meteget/rafét; a magánhangzópontok megmaradnak. Címszó: a szófaj-jelölő előtti első `<bdbheb>`; nyelv (héber/arámi) egyezik.')
    w('2. Homonímia: ha több jelölt van, az OSHL `def_en` és a BDB glosszái közti szóegyezés dönt; ha nem dönt egyértelműen, `tobb_jelolt`.')
    w('3. Kizárás: ha a BDB-szócikknek már van Strong-címkéje, vagy a Strong-számnak már van sora a táblában (vagy `H<n>` kulcsa a BDB.lexicon-ban), nem párosítható.')
    w('Gyök-hivatkozás ("√ of following", szófaj nélkül) mindig `nincs_par`.\n')
    w('## 2. Eredmény a címke nélküli szócikkekre\n')
    w('- Sorok: %d; állapotok: %s.' % (len(eredmeny), dict(szam)))
    w('- A `BDB_strong_potlas.tsv` a **címke nélküli** BDB-szócikkeket (BDB-azonosító szerint) sorolja; a Strong-oszlop a pár.\n')
    w('### Egyértelmű párok (mind)\n')
    w('| BDB | Strong | címszó | OSHL-lemma | indok |')
    w('|---|---|---|---|---|')
    for e, cs, s, lem, st, ind in eredmeny:
        if st == 'egyertelmu':
            w('| %s | %s | %s | %s | %s |' % (e['id'], s, cs, lem, ind.replace('|', '/')))
    w('\n### Tobb_jelolt sorok (mind)\n')
    tj = [r for r in eredmeny if r[4] == 'tobb_jelolt']
    if not tj:
        w('Nincs.\n')
    else:
        w('| BDB | Strong-jelöltek | címszó | indok |')
        w('|---|---|---|---|')
        for e, cs, s, lem, st, ind in tj:
            w('| %s | %s | %s | %s |' % (e['id'], s, cs, ind.replace('|', '/')))
    tipp = [r for r in eredmeny if 'tipp (' in r[5]]
    w('\n### Nincs_par, mássalhangzó-egyezési tipppel (nem párosítás; kézi döntéshez)\n')
    w('| BDB | címszó | tipp |')
    w('|---|---|---|')
    for e, cs, s, lem, st, ind in tipp:
        w('| %s | %s | %s |' % (e['id'], cs, ind.split('): ')[-1]))
    L.extend(masodlagos_szakasz())
    os.makedirs(os.path.dirname(M1_JELENTES), exist_ok=True)
    with open(M1_JELENTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')


def m0(ts):
    bdb, htop, tabla, oshl, cimkenelkuli, cimkezett, oshl_s = adatok()
    tahot = tahot_szamlalo()
    kozos = set(htop)
    hianyzo_h = sorted(s for s in kozos if s not in tabla)
    masod = []
    for s in hianyzo_h:
        b, ls = htop[s]
        tars = [x for x in ls if x != s and x in tabla]
        masod.append((s, b, tars))
    oshl_hiany = sorted(s for s in oshl_s if s not in tabla)
    ossz = collections.Counter()
    sorok = []
    for s in oshl_hiany:
        v = oshl_s[s]
        if s in htop:
            osz = 'masodlagos_cimke'
        else:
            osz = 'nincs_H_kulcs'
        ossz[osz] += 1
        sorok.append((s, v, osz, tahot_db(tahot, s)))
    ora = datetime.date.today().isoformat()
    L = []
    w = L.append
    w('# BDB_STRONG_POTLAS M0 — felmérés (F57)\n')
    w('*Generálta: `python eszkozok/bdb_strong_potlas.py --m0` · proveniencia: scope=konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/BDB_teljes_unabridged.tsv + konkordancia/OSHL_lexikalis_index.tsv + konkordancia/TAHOT_kivonat.tsv | forras=eszkozok/bdb_strong_potlas.py | ts=%s*\n' % ts)
    w('## 1. A BDB.lexicon szerkezete\n')
    w('- SQLite, egyetlen `Lexicon` tábla (`Topic`, `Definition`); `Topic` háromféle: `BDB####` (%d szócikk), `H<n>` (%d Strong-kulcs), `info` (1).' % (len(bdb), len(htop)))
    w('- A szócikk fejlécében (`<h1>`) a Strong-címke `<entry onclick="lex(\'H…\')">` alakban áll; egy szócikknek 0, 1 vagy több címkéje lehet. A `H<n>` kulcs a szócikket a *saját* címkéi alatt adja vissza.')
    w('- Nyelv: a navigációs sorban `BIBLICAL HEBREW` / `BIBLICAL ARAMAIC` (%d / %d).\n' % (
        sum(1 for e in bdb.values() if e['nyelv'] == 'heber'), sum(1 for e in bdb.values() if e['nyelv'] == 'arameus')))
    w('## 2. Címke nélküli BDB-szócikkek\n')
    w('- BDB-azonosítós szócikk: %d; ebből címkével: %d; **címke nélkül: %d** (heber %d, arámi %d).' % (
        len(bdb), len(bdb) - len(cimkenelkuli), len(cimkenelkuli),
        sum(1 for e in cimkenelkuli if e['nyelv'] == 'heber'), sum(1 for e in cimkenelkuli if e['nyelv'] == 'arameus')))
    w('- Ebből szófaj nélküli gyök-hivatkozás ("√ of following"): %d.\n' % sum(1 for e in cimkenelkuli if e['gyokstub']))
    w('| BDB-azonosító | nyelv | homonímaszám | címszó | szófaj | első glossza | gyök-hivatkozás |')
    w('|---|---|---|---|---|---|---|')
    for e in sorted(cimkenelkuli, key=lambda x: int(x['id'][3:])):
        w('| %s | %s | %s | %s | %s | %s | %s |' % (e['id'], e['nyelv'], e['homonima'] or '—',
                                                   e['cimszavak'][0] if e['cimszavak'] else '—',
                                                   (e['szofaj'] or '—')[:40],
                                                   (e['glosszak'][0] if e['glosszak'] else '—')[:50].replace('|', '/'),
                                                   'igen' if e['gyokstub'] else ''))
    w('\n## 3. A táblából hiányzó Strong-számok (OSHL-index szerint)\n')
    w('- A tábla sorai: %d; OSHL-index Strong-számai (különböző, `—` nélkül): %d; **a táblából hiányzik: %d** (heber %d, arámi %d).' % (
        len(tabla), len(oshl_s), len(oshl_hiany),
        sum(1 for s in oshl_hiany if oshl_s[s]['nyelv'] == 'heber'), sum(1 for s in oshl_hiany if oshl_s[s]['nyelv'] == 'arameus')))
    w('- OSHL-sor Strong nélkül (`—`): nem listázható (nincs Strong-kulcs).')
    w('- Osztályok: %s.' % dict(ossz))
    w('  - `masodlagos_cimke`: a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong **más Strong mellett** áll (pl. H0136 a BDB125-ben, [H113 H136]); a szöveg a táblában a testvér-Strong alatt már megvan.')
    w('  - `nincs_H_kulcs`: a BDB.lexicon-ban a Strongnak nincs `H<n>` kulcsa: ide a címke nélküli szócikkekből lehet párosítani (M1).')
    w('- Az ismert "396" az előfelmérés számítási módjától függ; ez a lista a teljes OSHL-indexen (heber + arámi, minden Strong, ha a táblában nincs sora) készült.\n')
    w('| Strong | lemma | OSHL bdb_id | def_en | nyelv | osztály | TAHOT-előfordulás |')
    w('|---|---|---|---|---|---|---|')
    for s, v, osz, db in sorok:
        w('| %s | %s | %s | %s | %s | %s | %d |' % (s, v['lemma'], v['bdb_id'], v['def_en'].replace('|', '/'), v['nyelv'], osz, db))
    w('\n## 4. BDB.lexicon H-kulcsok, amelyek a táblából hiányoznak\n')
    nmt = sum(1 for _, _, t in masod if t)
    w('- A `H<n>` kulcsok száma: %d; a táblában nincs sora: **%d**; ebből testvér-Strong a táblában van: %d, nincs: %d.' % (
        len(htop), len(hianyzo_h), nmt, len(masod) - nmt))
    w('- Ez a másodlagos-címke osztály; a szócikk szövege a testvér-sor alatt a táblában benne van, ezért nem szövegpótlás, hanem Strong→sor megfeleltetés kérdése (⛔ döntés).\n')
    w('## 5. Ellenőrzés a DictBDB.json-ban\n')
    w('- A `DictBDB.json` nincs a repóban (a `_convert_bdb.py` a `Temp` könyvtárból olvasta); újraletöltése nem történt (lemezkeret, letöltési engedély). A konverter **minden** nem üres bejegyzést kiír, a tábla tehát a JSON kulcskészletének képe (kulcsok: %d, ebből betűutótagos: %d, a fejlécsor nélkül).' % (
        len(tabla), sum(1 for k in tabla if re.search(r'[a-z]$', k))))
    w('- Következtetés: a hiányzó Strong-szám a JSON-ban sem szerepel más kulcs alatt (a betűutótagos kulcsok száma fent; a tábla kulcsai és a hiányzók listája diszjunkt). A közvetlen JSON-ellenőrzés a konverter forrásának újraletöltését igényelné; ezt a ⛔ nem blokkolja.')
    os.makedirs(os.path.dirname(M0_JELENTES), exist_ok=True)
    with open(M0_JELENTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('M0 kész ->', os.path.relpath(M0_JELENTES, GYOKER))
    print('címke nélküli:', len(cimkenelkuli), '| OSHL hiányzó Strong:', len(oshl_hiany), dict(ossz),
          '| H-kulcs hiányzik:', len(hianyzo_h), '| ebből testvér a táblában:', nmt)


# ---- M2 és alias ----
ALIAS = os.path.join(GYOKER, 'konkordancia', 'BDB_strong_alias.tsv')
ALIAS_FEJLEC = ['masodlagos_strong', 'tabla_strong', 'bdb_id', 'nyelv', 'cimszo', 'szoveg_hasonlosag', 'proveniencia']


def strip_html(txt):
    """Ugyanaz a tisztítás, mint a konkordancia/_convert_bdb.py-ban, kiegészítve a BDB.lexicon saját címkéivel."""
    txt = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', txt)
    txt = re.sub(r'<ref0[^>]*>(.*?)</ref0>', r'\1', txt)
    txt = re.sub(r'<font[^>]*>(.*?)</font>', r'\1', txt)
    txt = re.sub(r'<heb>|</heb>|<bdbheb>|</bdbheb>|<bdbarc>|</bdbarc>', '', txt)
    txt = re.sub(r'<grk>|</grk>', '', txt)
    txt = re.sub(r'<sup>(.*?)</sup>', r'^\1', txt)
    txt = re.sub(r'<sub>(.*?)</sub>', r'_\1', txt)
    txt = re.sub(r'<i>|</i>|<b>|</b>', '', txt)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    import html
    txt = html.unescape(txt)
    txt = txt.replace('\u200e', '')
    return re.sub(r'\s+', ' ', txt).strip()


def lexikon_torzs(bdb_id):
    con = sqlite3.connect('file:%s?mode=ro' % LEX.replace('\\', '/'), uri=True)
    d = con.execute('select Definition from Lexicon where Topic=?', (bdb_id,)).fetchone()[0]
    con.close()
    d = re.sub(r'^<h1>.*?</h1>', '', d, count=1, flags=re.S)
    return re.sub(r'<div class="navigation">.*?</div>', '', d, count=1, flags=re.S)


KONYVNEV = {'1Kgs': '1Kin', '2Kgs': '2Kin', 'Ps': 'Psa', 'Hos': 'Hosea', 'Mic': 'Micah',
            'Nah': 'Nahum', 'Esth': 'Est'}


def stilus_igazit(txt):
    """A meglévő sorok stílusa: 1Kin/Psa/Hosea/Micah/Nahum/Est könyvnevek, nincs szóköz
    írásjel előtt, nyitó zárójel és '^' után. (A kisebb eltérések a forrás tagolásából jönnek.)"""
    for regi, uj_ in KONYVNEV.items():
        txt = re.sub(r'\b' + regi + r'(?= \d)', uj_, txt)
    txt = re.sub(r' +([,;.)])', r'\1', txt)
    txt = re.sub(r'\( +', '(', txt)
    txt = re.sub(r'\^ +', '^', txt)
    return txt


def egyszerusitett_atiras(atiras, tulajdonnev=False):
    """A meglévő sorok fejének egyszerűsített átírása (akal, adon, mah…; nem diakritikus).

    Szabály (a meglévő sorok konvenciója szerint): š -> sh; az aleph és ajin jele (ʾ, ʿ) és minden
    kombináló diakritika (hosszúságjel, circumflex, breve, pont alatt/felett) elhagyva; köznévnél
    kisbetű (maqom), tulajdonnévnél nagy kezdőbetű (a meglévő tulajdonnév-fejek: Aryowk, Moab).
    Pl. ʾărîsay (tulajdonnév) -> Arisay, māqôm -> maqom, mahătallôt -> mahatallot.
    """
    t = atiras.replace('š', 'sh').replace('Š', 'Sh')
    t = unicodedata.normalize('NFD', t)
    t = ''.join(ch for ch in t if not unicodedata.combining(ch))
    t = t.replace('ʾ', '').replace('ʿ', '').replace("'", '')
    t = unicodedata.normalize('NFC', t)
    return t[:1].upper() + t[1:] if tulajdonnev else t


def m2_sorok():
    """A potlas-tabla egyertelmu soraiból az új táblasorok (Strong, sor)."""
    oshl = {r[0]: r for r in oshl_beolvas() if r[0] != '—'}
    ki = []
    with open(POTLAS, encoding='utf-8') as f:
        sorok = [l.split('\t') for l in f.read().split('\n') if l][1:]
    for r in sorok:
        if r[4] != 'egyertelmu':
            continue
        bid, strong, cim = r[0], r[1], r[2]
        eredeti = 'H' + str(int(strong[1:]))
        e = bdb_beolvas()[0].get(bid)
        atiras = egyszerusitett_atiras(oshl[strong][7], bool(e and e['szofaj'].startswith('proper name')))
        szoveg = stilus_igazit(strip_html(lexikon_torzs(bid)))
        szoveg = szoveg.replace('\t', ' ')
        ki.append((strong, '\t'.join([strong, eredeti, '%s. %s %s' % (eredeti, atiras, szoveg)])))
    return ki


def m2():
    with open(TABLA, 'rb') as f:
        elotte = f.read()
    if b'\r' in elotte:
        raise SystemExit('CRLF a táblában, megállok')
    if not elotte.endswith(b'\n'):
        raise SystemExit('a tábla nem újsorral végződik, megállok')
    sorok = elotte.decode('utf-8').split('\n')[:-1]
    uj = m2_sorok()
    ujkulcsok = {s for s, _ in uj}
    regi = [l for l in sorok if l.split('\t')[0] not in ujkulcsok]
    # a pótolt Strongok sorai a tábla végén állnak (a kulcsok egyediek)
    eredmeny = regi + [sor for _, sor in uj]
    utana = ('\n'.join(eredmeny) + '\n').encode('utf-8')
    if utana == elotte:
        print('M2: nincs változás (már pótolva)')
        return
    # ellenőrzés: a nem pótolt sorok sorrendben, bájtra azonosak
    assert [l for l in utana.decode('utf-8').split('\n')[:-1] if l.split('\t')[0] not in ujkulcsok] == regi
    assert len(eredmeny) == len(regi) + len(uj)
    with open(TABLA, 'wb') as f:
        f.write(utana)
    print('M2 kész: %d pótolt sor (%s), a többi %d sor változatlan' % (len(uj), ', '.join(sorted(ujkulcsok)), len(regi)))


ELVETETT = os.path.join(GYOKER, 'konkordancia', 'BDB_strong_alias_elvetett.tsv')
ELVETETT_FEJLEC = ['masodlagos_strong', 'bdb_id', 'nyelv', 'cimszo', 'testver_strong', 'indok_kod', 'indok', 'proveniencia']


def alias(ts):
    prov = 'scope=konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py --alias (masodlagos H-cimke; feltetel: bdb_id-egyezes + a szocikk latin betui >= 0,9 aranyban a testversor elejen, egy megfelelo testver; DT-F57f/g/h) | ts=%s' % ts
    alias_sorok, elvetett = alias_szetvalogat()
    with open(ALIAS, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(ALIAS_FEJLEC) + '\n')
        for r in alias_sorok:
            f.write('\t'.join([r['s'], r['tars'], r['bid'], r['nyelv'], r['hw'], r['hasonlosag'], prov]) + '\n')
    with open(ELVETETT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(ELVETETT_FEJLEC) + '\n')
        for r in elvetett:
            f.write('\t'.join([r['s'], r['bid'], r['nyelv'], r['hw'], r['tars'], r['kod'], r['indok'], prov]) + '\n')
    print('alias kész: %d sor, elvetett: %d sor (%s)' % (len(alias_sorok), len(elvetett),
          dict(collections.Counter(r['nyelv'] for r in elvetett))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m0', action='store_true')
    ap.add_argument('--m1', action='store_true')
    ap.add_argument('--m2', action='store_true')
    ap.add_argument('--alias', action='store_true')
    ap.add_argument('--m1-szakasz', action='store_true')
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    if a.m0:
        m0(a.ts)
    if a.m1:
        m1(a.ts)
    if a.alias:
        alias(a.ts)
    if a.m1_szakasz:
        m1_szakasz_frissit()
    if a.m2:
        m2()


if __name__ == '__main__':
    main()
