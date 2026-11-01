#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerinc_terkep.py -- F124: prioritasi terkep a kovetkezo igeszakasz
kivalasztasahoz. A teljes Bibliara (TAHOT + TAGNT) lefuttatja a
gerinc-kartya logikajat (gerinc_kartya.kartya_sorok), kizarja a mar
adatba vett es a mar feldolgozott helyeket, es fejezetenkent rangsorolja,
hol surusodnek a meg feldolgozatlan gerinc-talalatok.

Determinisztikus, modell es koltseg nelkul; adatot nem ir, csak a
naplok/GERINC_TERKEP.tsv es .md fajlt (vagy a --kimenet konyvtarat).
Idempotens: a `ts` es a bemenet-azonosito a bemeneti fajlok git
blob-hash-e es a legutobbi bemeneti commit ideje, nem a futas ideje --
valtozatlan bemenetre a kimenet bajtra azonos.

Szamitas (F124_GERINC_KARTYA_BRIEF.md 2.2):
  * kizarva: (id, igehely), amely elofordulasok.tsv-sor (tartomany-igehelyek
    verseikre bontva), vagy jeloltek.tsv-sor elutasitva/beepitve dontessel;
  * `nyitva` jelolt kulon oszlopban (nyitva_db);
  * a #110 szuro (gerinc_szuro.py) altal kiszurt sor nem szamit;
  * a tag gerinc-Strong szuro nelkuli sora (`szuretlen_tag`) kulon
    oszlopban (szuretlen_tag_db), a surusegbe NEM szamit;
  * kizarva a mar feldolgozott vers: a lefedettseg a tanulmanyfajlok
    nevebol vers-pontosan szarmazik (genezis/, ujszovetseg/, melyelemzesek/);
  * egyseg: fejezet; rangsor lexikografikusan, sulyok nelkul:
    (kulonbozo motivumok, kollokacios talalatok, osszes szurt talalat),
    egyezesnel kanonikus sorrend.

CLI:
    python eszkozok/gerinc_terkep.py [--kimenet DIR] [--adat DIR]

Kilepesi kod: 0 = lefutott, 2 = hiba.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G
import lekerdez as L
import gerinc_kartya as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')
ALAPERTELMEZETT_KIMENET = os.path.join(ROOT, 'naplok')

TANULMANY_MAPPAK = ('genezis', 'ujszovetseg', 'melyelemzesek')
# Nem igeszakasz-tanulmany fajlok a tanulmanymappakban (osszesitok): nem hiba.
NEM_TANULMANY_ELOTAG = ('Konnyu_ellenorzes',)

BEMENETI_FAJLOK = [
    'adat/motivumok.tsv', 'adat/elofordulasok.tsv', 'adat/jeloltek.tsv',
    'adat/grammatikai_strongok.tsv', 'konkordancia/TAHOT_kivonat.tsv',
    'konkordancia/TAGNT_kivonat.tsv', 'konkordancia/Konyv_normalizalo_tabla.tsv',
    'eszkozok/gerinc_terkep.py', 'eszkozok/gerinc_kartya.py', 'eszkozok/gerinc_szuro.py',
    'eszkozok/general.py', 'eszkozok/lekerdez.py', 'eszkozok/strong_util.py',
]

TSV_FEJLEC = ['konyv', 'fejezet', 'motivum_db', 'motivumok', 'kollokacio_db', 'talalat_db',
              'nyitva_db', 'szuretlen_tag_db', 'proveniencia']

NEV_RE = re.compile(
    r'^(?P<k>[0-9]?[A-Za-z]+)_(?P<c1>\d+)(?:v(?P<v1>\d+))?(?:-(?:(?P<c2>\d+)v)?(?P<x2>\d+))?_bovitett\.md$')


# ---------------------------------------------------------------------------
# Lefedettseg: tanulmanyfajlok neveibol
# ---------------------------------------------------------------------------

def _folded(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()


def konyv_tokenek():
    """{ekezet nelkuli kisbetus token: magyar rovidites} a Konyv_normalizalo_tablabol."""
    step2hu, _ = L.book_tables()
    return {_folded(hu): hu for hu in step2hu.values()}


def fajlnev_tartomany(nev, tokenek):
    """(konyv, ('chapters'|'verses', c1, v1, c2, v2)) vagy None, ha a nev nem ertelmezheto."""
    m = NEV_RE.match(nev)
    if not m:
        return None
    konyv = tokenek.get(_folded(m.group('k')))
    if konyv is None:
        return None
    c1 = int(m.group('c1'))
    v1 = int(m.group('v1')) if m.group('v1') else None
    x2 = int(m.group('x2')) if m.group('x2') else None
    c2 = int(m.group('c2')) if m.group('c2') else None
    if v1 is None:
        return konyv, ('chapters', c1, None, x2 if x2 is not None else c1, None)
    if x2 is None:
        return konyv, ('verses', c1, v1, c1, v1)
    if c2 is None:
        return konyv, ('verses', c1, v1, c1, x2)
    return konyv, ('verses', c1, v1, c2, x2)


def tartomany_versei(konyv, tart, by_book):
    kind, c1, v1, c2, v2 = tart
    ki = set()
    for k in by_book.get(konyv, ()):
        _, ch, v = k
        if kind == 'chapters':
            if c1 <= ch <= c2:
                ki.add(k)
        else:
            if (ch, v) >= (c1, v1) and (ch, v) <= (c2, v2):
                ki.add(k)
    return ki


def lefedettseg(fajlnevek, by_book, tokenek=None):
    """(fedett_versek:set, ertelmezett:[(fajl, igehely-jel)], hibak:[(fajl, ok)]).
    `fajlnevek`: [(mappa-relativ utvonal, alapnev)]."""
    tokenek = tokenek if tokenek is not None else konyv_tokenek()
    fedett = set()
    ertelmezett = []
    hibak = []
    for ut, nev in fajlnevek:
        if nev.startswith(NEM_TANULMANY_ELOTAG):
            continue
        t = fajlnev_tartomany(nev, tokenek)
        if t is None:
            hibak.append((ut, 'a fájlnév nem értelmezhető igeszakasz-tanulmányként'))
            continue
        vs = tartomany_versei(t[0], t[1], by_book)
        if not vs:
            hibak.append((ut, 'az értelmezett tartomány nem ad verset a TAHOT/TAGNT-ben'))
            continue
        fedett |= vs
        ertelmezett.append((ut, t))
    return fedett, ertelmezett, hibak


def tanulmany_fajlnevek(root):
    ki = []
    for mappa in TANULMANY_MAPPAK:
        p = os.path.join(root, mappa)
        if not os.path.isdir(p):
            continue
        for nev in sorted(os.listdir(p)):
            if nev.endswith('.md') and os.path.isfile(os.path.join(p, nev)):
                ki.append(('%s/%s' % (mappa, nev), nev))
    return ki


# ---------------------------------------------------------------------------
# Szamitas
# ---------------------------------------------------------------------------

def terkep_szamit(sorok, fedett, kidx):
    """[fejezet-dict] rangsorban. A `sorok` a kartya_sorok kimenete (teljes Biblia)."""
    per = {}
    ki_motivum = {}

    def cella(k):
        return per.setdefault((k[0], k[1]), {'motivumok': set(), 'kolloc': set(), 'talalat': set(),
                                             'nyitva': set(), 'szuretlen': set()})

    for s in sorok:
        k = s['kulcs']
        if k in fedett:
            continue
        a = s['allapot']
        if a == 'már előfordulás' or a in ('már jelölt: elutasítva', 'már jelölt: beépítve'):
            continue
        if s['szures'] == 'kiszurve' and a != 'már jelölt: nyitva':
            continue      # a kiszurt nyitva jelolt mar latott hely: a nyitva_db-ben marad
        c = cella(k)
        par = (s['id'], k)
        m = ki_motivum.setdefault(s['id'], {'talalat': set(), 'szuretlen': set(), 'nyitva': set()})
        if a == 'már jelölt: nyitva':
            c['nyitva'].add(par)
            m['nyitva'].add(par)
        elif s['szures'] == 'szuretlen_tag':
            c['szuretlen'].add(par)
            m['szuretlen'].add(par)
        else:
            c['talalat'].add(par)
            c['motivumok'].add(s['id'])
            m['talalat'].add(par)
            if s['kollokacio'] == 'kollokáció':
                c['kolloc'].add(par)
    ki = []
    for (konyv, fej), c in per.items():
        ki.append({'konyv': konyv, 'fejezet': fej,
                   'motivum_db': len(c['motivumok']), 'motivumok': ','.join(sorted(c['motivumok'])),
                   'kollokacio_db': len(c['kolloc']), 'talalat_db': len(c['talalat']),
                   'nyitva_db': len(c['nyitva']), 'szuretlen_tag_db': len(c['szuretlen'])})
    ki.sort(key=lambda r: (-r['motivum_db'], -r['kollokacio_db'], -r['talalat_db'],
                           kidx.get(r['konyv'], 999), r['fejezet']))
    mot = {k: {'talalat_db': len(v['talalat']), 'szuretlen_tag_db': len(v['szuretlen']),
               'nyitva_db': len(v['nyitva'])} for k, v in sorted(ki_motivum.items())}
    return ki, mot


# ---------------------------------------------------------------------------
# Bemenet-azonosito (idempotencia)
# ---------------------------------------------------------------------------

def _git(args, root):
    try:
        r = subprocess.run(['git', '-C', root] + args, capture_output=True, text=True, encoding='utf-8')
    except OSError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def git_blob(rel, root):
    h = _git(['rev-parse', 'HEAD:%s' % rel], root)
    return h[:10] if h else 'nincs-git'


def git_ts(rels, root):
    # A tanulmanymappaknal csak a fajlnevek szamitanak (hozzaadas/torles/atnevezes),
    # a tartalmi szerkesztes nem: kulonben minden tanulmany-javitas uj `ts`-t adna.
    mappak = [r for r in rels if r in TANULMANY_MAPPAK]
    fajlok = [r for r in rels if r not in TANULMANY_MAPPAK]
    ep_f = _git(['log', '-1', '--format=%ct', '--'] + fajlok, root)
    ep_m = _git(['log', '-1', '--diff-filter=ADR', '--format=%ct', '--'] + mappak, root) if mappak else None
    ep = max((e for e in (ep_f, ep_m) if e and e.isdigit()), key=int, default=None)
    if not ep or not ep.isdigit():
        return 'ismeretlen'
    import datetime
    return datetime.datetime.fromtimestamp(int(ep), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def bemenet_azonosito(root, tanulmanyok, blob=git_blob, ts_fn=git_ts):
    """(bemenet-szoveg, ts). A tanulmany-fajlnevek lenyomata a fedettseg bemenete."""
    resz = ['%s@%s' % (f, blob(f, root)) for f in BEMENETI_FAJLOK]
    lenyomat = hashlib.sha1('\n'.join(sorted(u for u, _ in tanulmanyok)).encode('utf-8')).hexdigest()[:10]
    resz.append('tanulmanynevek@%s' % lenyomat)
    return ','.join(resz), ts_fn(BEMENETI_FAJLOK + list(TANULMANY_MAPPAK), root)


# ---------------------------------------------------------------------------
# Kimenet
# ---------------------------------------------------------------------------

def tsv_szoveg(ki, bemenet, ts):
    fej = ('# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes | '
           'forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | bemenet=%s | ts=%s' % (bemenet, ts))
    sorok = [fej, '\t'.join(TSV_FEJLEC)]
    for r in ki:
        prov = ('scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | '
                'strong=gerinc-halmaz | fejezet=%s %d | n=%d | ts=%s' % (r['konyv'], r['fejezet'], r['talalat_db'], ts))
        sorok.append('\t'.join([r['konyv'], str(r['fejezet']), str(r['motivum_db']), r['motivumok'],
                                str(r['kollokacio_db']), str(r['talalat_db']), str(r['nyitva_db']),
                                str(r['szuretlen_tag_db']), prov]))
    return '\n'.join(sorok) + '\n'


def md_szoveg(ki, mot, ertelmezett, hibak, fedett_db, bemenet, ts, top=20):
    h = ['# GENERÁLT: gerinc_terkep.py | scope=TAHOT-teljes+TAGNT-teljes | '
         'forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | bemenet=%s | ts=%s' % (bemenet, ts),
         '', '# Prioritási térkép — hol sűrűsödnek a feldolgozatlan gerinc-találatok', '',
         'Gépi, determinisztikus összesítő (`eszkozok/gerinc_terkep.py`, F124); a következő igeszakasz '
         'kiválasztását támogatja. Csak jelölt-sűrűséget mutat, minősítést nem: minden hely a '
         '`jeloltek.tsv`-n át, döntéssel kerülhet be. Részletes táblázat: `naplok/GERINC_TERKEP.tsv`.', '',
         '**Rangsor** (súlyok nélkül, lexikografikusan): különböző motívumok száma, kollokációs találatok, '
         'összes szűrt találat; egyezésnél kanonikus sorrend. **Kizárva:** az `elofordulasok.tsv`-ben szereplő, '
         'valamint az `elutasítva`/`beépítve` döntésű hely; a #110 szűrője által kiszűrt sor; a már feldolgozott '
         'igeszakasz versei. A `nyitva` jelölt külön oszlop (`nyitva_db`), a szűretlen tág gerinc-Strong '
         '(`szuretlen_tag_db`) a sűrűségbe nem számít.', '',
         '## A legjobb %d fejezet' % top, '',
         '| # | Fejezet | Különböző motívum | Motívumok | Kollokációs találat | Összes találat | Nyitva | Szűretlen tag |',
         '|---|---|---|---|---|---|---|---|']
    for i, r in enumerate([r for r in ki if r['talalat_db'] > 0][:top], 1):
        h.append('| %d | %s %d | %d | %s | %d | %d | %d | %d |' % (
            i, r['konyv'], r['fejezet'], r['motivum_db'], r['motivumok'], r['kollokacio_db'],
            r['talalat_db'], r['nyitva_db'], r['szuretlen_tag_db']))
    if not any(r['talalat_db'] > 0 for r in ki):
        h.append('| *(üres: nincs szűrt, feldolgozatlan találat)* | | | | | | | |')
    h += ['', '## Motívumonként', '',
          'A `szuretlen_tag` arány azt mutatja, a motívum új találatainak mekkora hányadára nincs még gépi '
          'szűrő (ahol magas, ott kell szűrő-szabály, DT184 (d)).', '',
          '| Motívum | Szűrt találat | Szűretlen tag | `szuretlen_tag` arány | Nyitva |', '|---|---|---|---|---|']
    for mid, v in mot.items():
        ossz = v['talalat_db'] + v['szuretlen_tag_db']
        arany = '%.0f%%' % (100.0 * v['szuretlen_tag_db'] / ossz) if ossz else '—'
        h.append('| %s | %d | %d | %s | %d |' % (mid, v['talalat_db'], v['szuretlen_tag_db'], arany, v['nyitva_db']))
    if not mot:
        h.append('| *(üres)* | | | | |')
    h += ['', '## Lefedettség-mérés', '',
          '- Fedett vers (tanulmányfájl-nevekből): %d' % fedett_db,
          '- Értelmezett tanulmányfájl: %d' % len(ertelmezett),
          '- Nem értelmezhető fájlnév: %d' % len(hibak)]
    if hibak:
        h += [''] + ['  - `%s` — %s' % (f, ok) for f, ok in hibak]
    else:
        h.append('  - *(üres: minden tanulmányfájl neve értelmezhető)*')
    return '\n'.join(h) + '\n'


def futtat(adat_dir, root=ROOT, versek=None, kimenet_dir=None, bemenet_fn=None):
    versek = versek if versek is not None else K.versek_betolt()
    gramm = L.load_grammatikai_strongok()
    _, motivumok = G.tsv_beolvas(os.path.join(adat_dir, 'motivumok.tsv'))
    _, elofordulasok = G.tsv_beolvas(os.path.join(adat_dir, 'elofordulasok.tsv'))
    _, jeloltek = G.tsv_beolvas(os.path.join(adat_dir, 'jeloltek.tsv'))
    sorok = K.kartya_sorok(versek, gramm, motivumok, elofordulasok, jeloltek)
    by_book = K.konyvenkent(versek)
    kidx = K.konyv_index()
    nevek = tanulmany_fajlnevek(root)
    fedett, ertelmezett, hibak = lefedettseg(nevek, by_book)
    ki, mot = terkep_szamit(sorok, fedett, kidx)
    bemenet, ts = (bemenet_fn or bemenet_azonosito)(root, nevek)
    tsv = tsv_szoveg(ki, bemenet, ts)
    md = md_szoveg(ki, mot, ertelmezett, hibak, len(fedett), bemenet, ts)
    if kimenet_dir:
        os.makedirs(kimenet_dir, exist_ok=True)
        for nev, szoveg in (('GERINC_TERKEP.tsv', tsv), ('GERINC_TERKEP.md', md)):
            with open(os.path.join(kimenet_dir, nev), 'w', encoding='utf-8', newline='\n') as f:
                f.write(szoveg)
    return ki, mot, tsv, md


def main():
    ap = argparse.ArgumentParser(description='F124 -- prioritási térkép')
    ap.add_argument('--kimenet', default=ALAPERTELMEZETT_KIMENET,
                    help='kimeneti könyvtár (helyi próbához ideiglenes könyvtár a repón kívül)')
    ap.add_argument('--adat', default=ALAPERTELMEZETT_ADAT, help='az adat/ könyvtár')
    args = ap.parse_args()
    try:
        ki, mot, tsv, md = futtat(args.adat, kimenet_dir=args.kimenet)
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
    print('  %d fejezet a térképen; kimenet: %s' % (len(ki), args.kimenet), file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
