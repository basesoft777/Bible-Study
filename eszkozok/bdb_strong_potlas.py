#!/usr/bin/env python
"""A BDB-tábla hiányzó szócikkei (F57, #57): M0 felmérés, M1 párosítás.

Forrás: konkordancia/lexikonok_nyers/BDB.lexicon (SQLite, csak olvasás),
konkordancia/BDB_teljes_unabridged.tsv (a meglévő tábla),
konkordancia/OSHL_lexikalis_index.tsv (lemma, Strong), konkordancia/TAHOT_kivonat.tsv.

Módok:
  --m0       felmérés: naplok/BDB_STRONG_POTLAS_M0.md
  --m1       párosítás: konkordancia/BDB_strong_potlas.tsv
  --sorszam  csak darabszámok a képernyőre

A szkript csak olvas (a BDB-táblát nem írja); a TSV-ket split('\\t')-tel olvassa.
Párosítási szabály (BRIEF §3 M1) szó szerint:
 1. Címszó-egyezés: OSHL-lemma és BDB-címszó normalizált alakja egyezik
    (kantilláció és meteg le, holem-waw U+05BA -> U+05B9; magánhangzók maradnak).
 2. Homonímia: ha több jelölt van, az OSHL def_en és a BDB glosszák szóegyezése
    dönt; ha nem dönt egyértelműen, tobb_jelolt.
 3. Kizárás: ha a BDB-szócikknek van Strong-címkéje, vagy a Strong-számnak van
    sora a táblában, vagy a BDB.lexicon H-kulcsa van, nem párosítható.
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


def masodlagos_lista():
    bdb, htop, tabla, oshl, cimkenelkuli, cimkezett, oshl_s = adatok()
    tahot = tahot_szamlalo()
    sorok = []
    for s in sorted(htop):
        if s in tabla or s == 'H0000':
            continue
        b, ls = htop[s]
        tars = [x for x in ls if x != s and x in tabla]
        e = bdb.get(b)
        hw = e['cimszavak'][0] if e and e['cimszavak'] else ''
        talal = False
        for x in tars:
            sz = tabla[x].split('	', 2)[2]
            if hw and kons(hw) and kons(hw) in kons(sz):
                talal = True
        o = oshl_s.get(s)
        sorok.append((s, b, tars, hw, talal, o, tahot_db(tahot, s)))
    return sorok


def m1_jelentes(eredmeny, prov, ts):
    szam = collections.Counter(r[4] for r in eredmeny)
    sor2 = masodlagos_lista()
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
    w('\n## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora\n')
    nt = sum(1 for r in sor2 if r[4])
    w('- %d Strong (a H0136 és a H0341 is ide tartozik), mindegyiknek a szócikke a BDB.lexicon `H<n>` kulcsa alatt **címkével** áll, tehát a 3. kizárási szabály miatt nem párosítható; a szöveg a táblában a testvér-Strong sora alatt megvan (a címszó mássalhangzós alakja a testvér-sor szövegében: %d/%d sorban megtalálható).' % (len(sor2), nt, len(sor2)))
    w('- Ez nem a tábla szövegének hiánya, hanem a Strong-kulcs hiánya (a DictBDB.json egy szócikkhez csak egy Strong-kulcsot ad). Lásd a ⛔ döntést (DONTESEK.md).\n')
    w('| Strong | BDB | testvér-Strong a táblában | címszó | címszó a testvér-sorban | OSHL def_en | TAHOT |')
    w('|---|---|---|---|---|---|---|')
    for s, b, tars, hw, talal, o, db in sor2:
        w('| %s | %s | %s | %s | %s | %s | %d |' % (s, b, ','.join(tars), hw, 'igen' if talal else 'NEM', (o['def_en'] if o else '—').replace('|', '/'), db))
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
