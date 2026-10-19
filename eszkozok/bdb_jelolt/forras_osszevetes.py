#!/usr/bin/env python
"""A BDB két nyers forrásának összevetése (F107, 1. lépés; FELADATOK #107).

Bemenet:
  --json PATH   a DictBDB.json (eliranwong/unabridged-BDB-Hebrew-lexicon), a repón kívüli
                munkakönyvtárból; csak olvasás, semmi nem fut belőle (a hívó `python -I`-vel futtassa)
  konkordancia/lexikonok_nyers/BDB.lexicon (SQLite, csak olvasás, mode=ro)
  konkordancia/BDB_teljes_unabridged.tsv (split('\\t'), csv modul nélkül)

Mér:
  A. a JSON hash-e, és hogy a _convert_bdb.py (142ad625) eljárása belőle bájtra a K7-es
     eredeti TSV-t (sha256 1d28a840…dfa5) adja-e (= a 2026-09-02-i letöltéssel azonos tartalom);
  B. a BDB.lexicon hash-e és jelölő-számai;
  C. a BDB.lexicon lefedettsége a TSV Strong-soraira; Strong ↔ BDB-azonosító megfeleltetés;
  D. azonos átirat-e: latin szó-ujjlenyomat hasonlósága rögzített mintán (seed);
  E. a tagolás-jelölők (félkövér szerkezeti fejek) helye a két forrásban: blokk elején állnak-e.

Kimenet: összefoglaló a stdout-ra, proveniencia-sorral. Semmit nem ír a repóba.
"""
import argparse
import collections
import datetime
import hashlib
import html
import json
import os
import random
import re
import sqlite3
import sys
import difflib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEX = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'BDB.lexicon')
TSV = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
K7_HASH = '1d28a84004817b8ee09eff92d762038ae2eac7351f24abd0a8b1cc5df380dfa5'

TORZS = r"(?:Qal|Niph`al|Pi`el|Pu`al|Hiph`il|Hoph`al|Hithpa`el|Hithp[a-z`]*|Pe`al|Pa`el|Haph`el|Aph`el|Ithpe`el|Ithpa`al|Hithpe`el|Po`lel|Po`el|Pilpel|Pol[a-z`]*|Pe`il|Shaph`el|Hophal|Piel|Hiphil|Niphal)"
TIPUSOK = [
    ('szam', re.compile(r'^\d{1,2}\.?$')),
    ('betu', re.compile(r'^[a-z]\.?$')),
    ('romai', re.compile(r'^(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.?$')),
    ('torzs', re.compile(r'^' + TORZS + r'\.?$')),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blokk in iter(lambda: f.read(1 << 20), b''):
            h.update(blokk)
    return h.hexdigest()


def strip_html_142ad625(txt):
    """A konkordancia/_convert_bdb.py strip_html()-je, változatlanul (a fájl importja futna)."""
    txt = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', txt)
    txt = re.sub(r'<ref0[^>]*>(.*?)</ref0>', r'\1', txt)
    txt = re.sub(r'<font[^>]*>(.*?)</font>', r'\1', txt)
    txt = re.sub(r'<heb>|</heb>', '', txt)
    txt = re.sub(r'<grk>|</grk>', '', txt)
    txt = re.sub(r'<sup>(.*?)</sup>', r'^\1', txt)
    txt = re.sub(r'<sub>(.*?)</sub>', r'_\1', txt)
    txt = re.sub(r'<i>|</i>', '', txt)
    txt = re.sub(r'<b>|</b>', '', txt)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub('‎', '', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt


def konvertal_142ad625(data):
    sorok = []
    for item in data:
        top = item.get('top', '')
        m = re.match(r'^H(\d+)', top)
        if not m:
            continue
        padded = 'H%04d' % int(m.group(1)) + top[len(m.group(0)):]
        plain = strip_html_142ad625(item.get('def', ''))
        if plain:
            sorok.append((padded, top, plain))
    szoveg = 'Strong_padded\tStrong_eredeti\tTeljes_szocikk\n' + ''.join(
        '%s\t%s\t%s\n' % (p, o, t.replace('\t', ' ')) for p, o, t in sorok)
    return sorok, szoveg


def unpad(s):
    m = re.match(r'^H0*(\d+)([a-z]?)$', s)
    return 'H%s%s' % (m.group(1), m.group(2)) if m else s


def ujjlenyomat(htmltxt, lexikon):
    t = htmltxt
    if lexikon:
        t = re.sub(r'<h1>.*?</h1>', ' ', t)
        t = re.sub(r'<div class="navigation">.*?</div>', ' ', t)
        t = re.sub(r'<ref [^>]*>.*?</ref>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.findall(r'\b[a-z]{3,}\b', t)


def elso_szocikk(hsor):
    """A lexikon H-kulcsú sorából a Strong saját (első) szócikke: a második <h1>-ig."""
    i = hsor.find('<h1>', 1)
    return hsor if i < 0 else hsor[:i]


def fej_tipus(b):
    s = re.sub(r'<[^>]+>', '', html.unescape(b)).strip()
    for nev, minta in TIPUSOK:
        if minta.match(s):
            return nev
    return None


BLOKK_JSON = re.compile(r'<p>\s*$')
BLOKK_LEX = re.compile(r'(?:<div class="(?:point|section|remarks)">|<p>|<br\s*/?>)(?:\s|&emsp;)*$')


def fejek(htmltxt, blokk_re):
    """(típus, blokk_elején) párok a szerkezeti félkövér fejekre."""
    ki = []
    for m in re.finditer(r'<b>(.*?)</b>', htmltxt, re.S):
        tip = fej_tipus(m.group(1))
        if tip:
            elotte = htmltxt[max(0, m.start() - 60):m.start()]
            ki.append((tip, bool(blokk_re.search(elotte))))
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', required=True)
    ap.add_argument('--minta', type=int, default=300)
    ap.add_argument('--seed', type=int, default=107)
    a = ap.parse_args()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # A. JSON
    json_hash = sha256(a.json)
    with open(a.json, encoding='utf-8') as f:
        data = json.load(f)
    jdict = {x['top']: x['def'] for x in data}
    print('## A. DictBDB.json')
    print('- sha256:', json_hash, '| bajt:', os.path.getsize(a.json), '| elem:', len(data),
          '| H-kulcs:', sum(1 for k in jdict if k.startswith('H')))
    sorok, szoveg = konvertal_142ad625(data)
    for nev, sz in (('LF', szoveg), ('CRLF', szoveg.replace('\n', '\r\n'))):
        hh = hashlib.sha256(sz.encode('utf-8')).hexdigest()
        print('- _convert_bdb (142ad625) újrafuttatva, %s: sha256 %s, sor %d, K7-egyezés: %s' % (
            nev, hh, len(sorok), 'IGEN' if hh == K7_HASH else 'nem'))
    with open(TSV, encoding='utf-8', newline='') as f:
        tsv = [s.split('\t') for s in f.read().split('\n')[1:] if s]
    tsv_eredeti = [s[1] for s in tsv]
    ujra = {o: t for _, o, t in sorok}
    azonos = sum(1 for s in tsv if ujra.get(s[1]) == s[2])
    print('- a mai TSV %d sorából a JSON-ból újrakonvertálttal bájtra azonos szövegű: %d; JSON-ban nincs kulcsa: %d'
          % (len(tsv), azonos, sum(1 for s in tsv if s[1] not in ujra)))
    jall = collections.Counter()
    for k, d in jdict.items():
        if k.startswith('H'):
            for tag in ('<p>', '<b>', '<sub>', '<sup>', '<i>', 'class="point"', 'class="section"', 'class="remarks"'):
                jall[tag] += d.count(tag)
    print('- jelölők a JSON-ban:', dict(jall))

    # B. BDB.lexicon
    con = sqlite3.connect('file:' + LEX.replace('\\', '/') + '?mode=ro', uri=True)
    rows = con.execute('select Topic, Definition from Lexicon').fetchall()
    con.close()
    print('\n## B. BDB.lexicon')
    print('- sha256:', sha256(LEX), '| sor:', len(rows))
    bdb_rows = {t: d for t, d in rows if t.startswith('BDB')}
    h_rows = {t: d for t, d in rows if re.match(r'^H\d', t)}
    for nev, halmaz in (('BDB*', bdb_rows), ('H*', h_rows)):
        c = collections.Counter()
        for d in halmaz.values():
            for tag in ('class="point"', 'class="section"', 'class="remarks"', '<b>', '<sub>', '<p>'):
                c[tag] += d.count(tag)
        print('- %s: %d sor; %s' % (nev, len(halmaz), dict(c)))

    # C. lefedettség és megfeleltetés
    print('\n## C. Lefedettség (TSV Strong-sorai) és Strong ↔ BDB')
    cimke = collections.defaultdict(list)
    for t, d in bdb_rows.items():
        h = re.match(r'<h1>(.*?)</h1>', d)
        for x in re.findall(r"lex\('(H\d+[a-z]?)'\)", h.group(1) if h else ''):
            cimke[x].append(t)
    h_bdb = {}
    for t, d in h_rows.items():
        h_bdb[t] = re.findall(r"<h1><entry onclick=\"bdbid\('(BDB\d+)'\)", d)
    van_h = sum(1 for o in tsv_eredeti if o in h_rows)
    van_cimke = sum(1 for o in tsv_eredeti if o in cimke)
    hiany = [o for o in tsv_eredeti if o not in h_rows and o not in cimke]
    print('- TSV-sor: %d; H-kulcsú lexikonsor van: %d; BDB-szócikk-címke van: %d; egyik sincs: %d %s'
          % (len(tsv_eredeti), van_h, van_cimke, len(hiany), hiany[:20]))
    eloszl = collections.Counter(min(len(h_bdb.get(o, [])), 4) for o in tsv_eredeti)
    print('- BDB-szócikk egy H-kulcsú sorban (a TSV Strongjaira; 4 = 4+):', sorted(eloszl.items()))
    egyezik = sum(1 for o in tsv_eredeti if o in h_rows and o in cimke and set(h_bdb[o]) >= set(cimke[o]))
    print('- a H-sor szócikkei tartalmazzák a címke szerinti összes szócikket: %d' % egyezik)
    pontos = sum(1 for o in tsv_eredeti if o in h_rows and o in cimke and set(h_bdb[o]) == set(cimke[o]))
    print('- a H-sor szócikkei pontosan a címke szerinti szócikkek: %d' % pontos)
    bdb_cimkei = collections.defaultdict(set)
    for k, l in cimke.items():
        for b in l:
            bdb_cimkei[b].add(k)
    tobb_strong = collections.Counter(min(len(bdb_cimkei.get(b, ())), 3) for b in bdb_rows)
    print('- BDB-szócikkek a rajtuk álló Strong-címkék száma szerint:', sorted(tobb_strong.items()))
    print('- extra H-kulcs a lexikonban (nincs TSV-sora): %d' % len(set(h_rows) - set(tsv_eredeti)))

    kozos = sorted(o for o in tsv_eredeti if o in h_rows and o in jdict)
    rnd = random.Random(a.seed)
    minta = rnd.sample(kozos, min(a.minta, len(kozos)))
    valtozatok = (('teljes H-sor', lambda o: h_rows[o]), ('csak az első szócikk', lambda o: elso_szocikk(h_rows[o])))

    # D. azonos átirat-e (minta)
    print('\n## D. Átirat-azonosság (latin szó-ujjlenyomat, minta: %d Strong, seed=%d, a %d közösből)'
          % (len(minta), a.seed, len(kozos)))
    for vnev, vf in valtozatok:
        savok = collections.Counter()
        legrosszabb = []
        for o in minta:
            jw = ujjlenyomat(jdict[o], False)
            lw = ujjlenyomat(vf(o), True)
            sm = difflib.SequenceMatcher(None, jw, lw, autojunk=False)
            lefed = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(jw))
            savok['>=0.95' if lefed >= 0.95 else ('0.80-0.95' if lefed >= 0.8 else '<0.80')] += 1
            legrosszabb.append((round(lefed, 3), o, len(jw), len(lw)))
        print('- lexikon = %s: a JSON-szavak lexikonbeli lefedése %s; 6 legalacsonyabb (lefedés, Strong, JSON-szó, lexikon-szó): %s'
              % (vnev, dict(savok), sorted(legrosszabb)[:6]))

    # E. tagolás-jelölők
    print('\n## E. Szerkezeti félkövér fejek (szám / betű / római / igetörzs) a teljes közös halmazon (%d Strong)' % len(kozos))
    for vnev, vf in valtozatok:
        stat = {'json': collections.Counter(), 'lex': collections.Counter()}
        szam_egyezik = 0
        for o in kozos:
            jf = fejek(jdict[o], BLOKK_JSON)
            lf = fejek(vf(o), BLOKK_LEX)
            for nev, ff in (('json', jf), ('lex', lf)):
                for tip, blokk in ff:
                    stat[nev][(tip, 'ossz')] += 1
                    if blokk:
                        stat[nev][(tip, 'blokk')] += 1
            if sum(1 for t, _ in jf if t == 'szam') == sum(1 for t, _ in lf if t == 'szam'):
                szam_egyezik += 1
        print('- lexikon = %s:' % vnev)
        for tip, _ in TIPUSOK:
            jo, jb = stat['json'][(tip, 'ossz')], stat['json'][(tip, 'blokk')]
            lo, lb = stat['lex'][(tip, 'ossz')], stat['lex'][(tip, 'blokk')]
            print('  - %-6s JSON: %6d fej, blokk elején %6d (%.1f%%) | lexicon: %6d fej, blokk elején %6d (%.1f%%)'
                  % (tip, jo, jb, 100.0 * jb / max(1, jo), lo, lb, 100.0 * lb / max(1, lo)))
        print('  - Strongok, ahol a számozott fejek darabszáma azonos: %d / %d' % (szam_egyezik, len(kozos)))

    print('\nproveniencia: scope=F107 1. lépés, DictBDB.json ↔ BDB.lexicon ↔ BDB_teljes_unabridged.tsv | '
          'forras=eszkozok/bdb_jelolt/forras_osszevetes.py --minta %d --seed %d; DictBDB.json sha256 %s | ts=%s'
          % (a.minta, a.seed, json_hash, ts))


if __name__ == '__main__':
    main()
