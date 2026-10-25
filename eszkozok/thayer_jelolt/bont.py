#!/usr/bin/env python
"""A Thayer szakasztáblája (F132 M1; FELADATOK #132; DT-F132a (b), DT-F132b (1), (4)).

Forrás (DT-F132a (b), felhasználó, 2026-10-25):
  - szerkezet (bekezdéshatár, fej, `utvonal`): konkordancia/lexikonok_nyers/Thayer.lexicon (`Lexicon(Topic, Definition)`,
    HTML; a formázási réteg licence a forrásmondat szerint nem tisztázott, ezért innen csak szerkezet és azonosító jön);
  - szöveg: konkordancia/Thayer_teljes.tsv (`Teljes_szocikk`), illesztéssel: a szakasz szövege a TSV-szöveg szelete.

Kimenet: adat/thayer_szakaszok.tsv (séma: adat/SEMA.md, „thayer_szakaszok.tsv”). Egy sor = a szócikk egy bekezdése: a
`<p>`, `</p>`, `<div>`, `</div>` jelölők közötti, címkék nélkül nem üres HTML-darab, a forrás sorrendjében (a forrás
HTML-je helyenként egymásba ágyazott vagy lezáratlan `<p>`-t tartalmaz, pl. G21, G687; ezért a határ a jelölő, nem a
`<p>…</p>` pár).

Fejek (a bekezdés elején; a forrásban bekezdésen belüli fej nem fordul elő, mért: M1 felmérés):
  `<span class="lexheading">I.</span>` római (romai) · sima `A. ` nagybetű (nagy; csak a sorban következő betű: A, B, …)
  · `<b>1.</b>` szám (szam) · `<b>a.</b>` betű (betu). A felsőbb szint a mélyebbeket törli.
`utvonal`: `<felső>/<szám>/<betű>` (`-` a hiányzó szint; a felső a nagybetű és a római pontokkal: `A`, `I`, `A.I`);
különleges: `cim` (a `<b>G… — …</b>` / `<b>G…a: …</b>` címsor; újabb címsor a fejállapotot törli), `fej` (a cím után, az
első fej előtti bekezdés). Fej nélküli bekezdés az előző útvonalát örökli (`jel` üres).

Illesztés (`illesztes`, Strongonként): `egyezik` — a bekezdések szóközök nélküli szövege sorban, hézag és maradék
nélkül kiadja a TSV szövegét; `reszleges` — nem így: a határok a difflib egyező blokkjain át vetülnek a TSV-szövegre
(a szakasz szövege közelítő; explicit jelölés); `sikertelen` — a TSV-ben nincs ilyen Strong (a `szoveg` üres:
explicit hiány, nem kitöltés).

Módok:
  (alap)        a tábla írása
  --meres       csak statisztika, írás nélkül
  --ellenoriz   újragenerálás memóriában (a fájl fejlécének `--ts`-ével) és bájtos összevetés (kilépési kód 1, ha eltér)

TSV: split('\\t') olvasás, '\\t'.join írás, csv modul nélkül; a szövegben tab és sortörés szóközre cserélve.
"""
import argparse
import collections
import datetime
import difflib
import hashlib
import html
import os
import re
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import kulcs  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
LEX_UT = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'Thayer.lexicon')
TSV_UT = os.path.join(GYOKER, 'konkordancia', 'Thayer_teljes.tsv')
KI_UT = os.path.join(GYOKER, 'adat', 'thayer_szakaszok.tsv')

FEJLEC = ['strong', 'sorszam', 'utvonal', 'jel', 'szoveg', 'illesztes', 'forras', 'forras_hash', 'proveniencia']

HATAR = re.compile(r'</?p\b[^>]*>|</?div\b[^>]*>')
TAG = re.compile(r'<[^>]+>')
CIM = re.compile(r'^\s*<b>G\d+')
FEJ_ROMAI = re.compile(r'^\s*<span class="lexheading">((?:VIII|VII|VI|IV|IX|III|II|V|X|I)\.)</span>')
FEJ_B = re.compile(r'^\s*<b>(\d{1,2}\.|[a-z]\.)</b>')
FEJ_NAGY = re.compile(r'^([A-H])\.(?=\s)')
WS = re.compile(r'\s+')


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def kod_hash():
    h = hashlib.sha256()
    for ut in (os.path.abspath(__file__), os.path.join(ITT, 'kulcs.py')):
        with open(ut, 'rb') as f:
            h.update(f.read().replace(b'\r\n', b'\n'))
    return h.hexdigest()


def sima(raw):
    """A bekezdés sima szövege: címkék nélkül, entitások feloldva, a szóközök összevonva."""
    return WS.sub(' ', html.unescape(TAG.sub('', raw))).strip()


def szegmensek(definition):
    """A szócikk bekezdései nyers HTML-ként, a forrás sorrendjében (a M2 is ezt használja)."""
    return [s for s in HATAR.split(definition or '') if sima(s)]


def lexikon_beolvas(ut=LEX_UT):
    """-> OrderedDict: Strong_padded -> (Topic, Definition), a forrás sorrendjében."""
    con = sqlite3.connect('file:%s?mode=ro' % ut, uri=True)
    try:
        ki = collections.OrderedDict()
        for t, d in con.execute('select Topic, Definition from Lexicon'):
            p = kulcs.strong_pad(t or '')
            if p is None:
                continue
            if p in ki:
                raise ValueError('kettős Topic: %s' % t)
            ki[p] = (t, d)
        return ki
    finally:
        con.close()


def tsv_beolvas(ut=TSV_UT):
    ki = {}
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[0].rstrip('\r').split('\t')
    i_k, i_t = fej.index('Strong_padded'), fej.index('Teljes_szocikk')
    for s in sorok[1:]:
        s = s.rstrip('\r')
        if not s:
            continue
        r = s.split('\t')
        ki[kulcs.strong_pad(r[i_k])] = r[i_t]
    return ki


def fej_felismer(raw, tagolas):
    """-> (szint, jel) vagy (None, ''); a `tagolas` a szócikk eddigi állapota (a nagybetűs fej sorrendjéhez)."""
    m = FEJ_ROMAI.match(raw)
    if m:
        return 'romai', m.group(1)
    m = FEJ_B.match(raw)
    if m:
        return ('szam' if m.group(1)[0].isdigit() else 'betu'), m.group(1)
    m = FEJ_NAGY.match(sima(raw))
    if m and not raw.lstrip().startswith('<'):
        varhato = chr(ord(tagolas.get('nagy') or '@') + 1)
        if m.group(1) == varhato:
            return 'nagy', m.group(0)
    return None, ''


TOROL = {'nagy': ('romai', 'szam', 'betu'), 'romai': ('szam', 'betu'), 'szam': ('betu',), 'betu': ()}


def utvonal(t):
    felso = '.'.join(x for x in (t.get('nagy'), t.get('romai')) if x) or '-'
    return '%s/%s/%s' % (felso, t.get('szam') or '-', t.get('betu') or '-')


def szerkezet(definition):
    """-> [{'raw', 'plain', 'utvonal', 'jel'}] a szócikk bekezdéseire."""
    ki, t, allapot = [], {}, 'kezdet'
    for raw in szegmensek(definition):
        plain = sima(raw)
        if CIM.match(raw):
            t, allapot = {}, 'cim'
            ki.append({'raw': raw, 'plain': plain, 'utvonal': 'cim', 'jel': ''})
            continue
        szint, jel = fej_felismer(raw, t)
        if szint:
            t[szint] = jel.rstrip('.')
            for x in TOROL[szint]:
                t.pop(x, None)
            allapot = 'fejes'
            ki.append({'raw': raw, 'plain': plain, 'utvonal': utvonal(t), 'jel': jel})
        else:
            ut = utvonal(t) if allapot == 'fejes' else 'fej'
            ki.append({'raw': raw, 'plain': plain, 'utvonal': ut, 'jel': ''})
    return ki


def _nows(s):
    """(szóközök nélküli szöveg, indexlista az eredetibe)."""
    c, idx = [], []
    for i, ch in enumerate(s):
        if not ch.isspace():
            c.append(ch)
            idx.append(i)
    return ''.join(c), idx


def illeszt(szak, tsv_szoveg):
    """A bekezdések szövege a TSV-szövegből. -> (kategória, [szöveg bekezdésenként, a `jel`-lel együtt])."""
    if tsv_szoveg is None:
        return 'sikertelen', [''] * len(szak)
    t, idx = _nows(tsv_szoveg)
    darabok = [_nows(x['plain'])[0] for x in szak]
    hatar, p, egyezik = [], 0, True
    for d in darabok:
        if t.startswith(d, p):
            hatar.append((p, p + len(d)))
            p += len(d)
        else:
            egyezik = False
            break
    if egyezik and p == len(t):
        kat = 'egyezik'
    else:
        kat = 'reszleges'
        lex = ''.join(darabok)
        sm = difflib.SequenceMatcher(None, lex, t, autojunk=False)
        blokkok = sm.get_matching_blocks()

        def vetit(q):
            # q: pozíció a lex-ben -> pozíció a t-ben (az utolsó q-nál nem nagyobb kezdetű blokk szerint)
            best = 0
            for a, b, n in blokkok:
                if a <= q:
                    best = b + min(q - a, n)
                else:
                    break
            return best
        hatar, q = [], 0
        for i, d in enumerate(darabok):
            a = vetit(q) if i else 0
            q += len(d)
            b = vetit(q) if i < len(darabok) - 1 else len(t)
            hatar.append((a, max(a, b)))
    ki = []
    for a, b in hatar:
        if b <= a:
            ki.append('')
        else:
            ki.append(tsv_szoveg[idx[a]:idx[b - 1] + 1].strip())
    return kat, ki


def jel_levag(jel, szoveg):
    if jel and szoveg.startswith(jel):
        return szoveg[len(jel):].strip()
    return szoveg


def tisztit(s):
    return WS.sub(' ', s.replace('\t', ' ')).strip()


def general(ts, lex_ut=LEX_UT, tsv_ut=TSV_UT):
    lex = lexikon_beolvas(lex_ut)
    tsv = tsv_beolvas(tsv_ut)
    sorok, stat = [], collections.Counter()
    reszlet = {}
    for sp, (topic, d) in lex.items():
        szak = szerkezet(d)
        kat, szovegek = illeszt(szak, tsv.get(sp))
        stat[kat] += 1
        if kat != 'egyezik':
            reszlet[sp] = kat
        if any(x['jel'] for x in szak):
            stat['fejes_szocikk'] += 1
        for i, (x, sz) in enumerate(zip(szak, szovegek), 1):
            sorok.append([sp, str(i), x['utvonal'], x['jel'], tisztit(jel_levag(x['jel'], sz)), kat,
                          'Thayer.lexicon:%s#%d' % (topic, i), hashlib.sha256(x['raw'].encode('utf-8')).hexdigest()[:16],
                          'scope=%s | forras=thayer_jelolt/bont.py (fejléc) | ts=%s' % (sp, ts)])
    stat['strong'] = len(lex)
    stat['tsv_lexikonban_nincs'] = len(set(tsv) - set(lex))
    return sorok, stat, reszlet


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/thayer_jelolt/bont.py --ts %s — kézzel nem szerkesztendő (F132; séma: adat/SEMA.md, thayer_szakaszok.tsv).' % ts,
           '# forras: konkordancia/lexikonok_nyers/Thayer.lexicon@%s (csak szerkezet: bekezdéshatár, fej; DT-F132a (b)) + '
           'konkordancia/Thayer_teljes.tsv@%s (szöveg, illesztéssel) + kód@%s'
           % (sha256_fajl(LEX_UT)[:12], sha256_fajl(TSV_UT)[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def fajl_ts(ut=KI_UT):
    with open(ut, encoding='utf-8') as f:
        m = re.search(r'--ts (\S+)', f.readline())
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts')
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    ts = a.ts or (fajl_ts() if a.ellenoriz and os.path.exists(KI_UT) else None) or datetime.date.today().isoformat()
    sorok, stat, reszlet = general(ts)
    print('Strong: %d; illesztés: egyezik %d, reszleges %d, sikertelen %d; fejes szócikk %d; a TSV-ben a lexikonon kívül: %d'
          % (stat['strong'], stat['egyezik'], stat['reszleges'], stat['sikertelen'], stat['fejes_szocikk'],
             stat['tsv_lexikonban_nincs']))
    ut_tip = collections.Counter(s[2] if s[2] in ('cim', 'fej') else ('fejes' if s[3] else 'orokolt') for s in sorok)
    print('sor: %d; %s' % (len(sorok), dict(ut_tip)))
    for k, v in sorted(reszlet.items()):
        print('  %s %s' % (k, v))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, ts)
    if a.ellenoriz:
        with open(KI_UT, encoding='utf-8', newline='') as f:
            regi = f.read()
        if regi != szoveg:
            print('ELTÉR: %s' % KI_UT)
            return 1
        print('azonos: %s' % KI_UT)
        return 0
    with open(KI_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('írva: %s' % KI_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
