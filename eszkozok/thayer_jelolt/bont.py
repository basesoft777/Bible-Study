#!/usr/bin/env python
"""A Thayer szakasztáblája (F132 M1; FELADATOK #132; DT-F132a (b), DT-F132b (1), (4)).

Forrás (DT-F132a (b), felhasználó, 2026-10-25):
  - szerkezet (bekezdéshatár, fej, `utvonal`): konkordancia/lexikonok_nyers/Thayer.lexicon (`Lexicon(Topic, Definition)`,
    HTML; a formázási réteg licence a forrásmondat szerint nem tisztázott, ezért innen csak szerkezet és azonosító jön);
  - szöveg: konkordancia/Thayer_teljes.tsv (`Teljes_szocikk`), illesztéssel: a szakasz szövege a TSV-szöveg szelete.

Kimenet: adat/thayer_szakaszok.tsv (séma: adat/SEMA.md, „thayer_szakaszok.tsv”). Egy sor = a szócikk egy szakasza: egy
bekezdés — a `<p>`, `</p>`, `<div>`, `</div>` jelölők közötti, címkék nélkül nem üres HTML-darab, a forrás sorrendjében (a
forrás HTML-je helyenként egymásba ágyazott vagy lezáratlan `<p>`-t tartalmaz, pl. G21, G687; ezért a határ a jelölő, nem a
`<p>…</p>` pár) —, vagy (F186 K1) a bekezdésnek egy bekezdésen belüli fejnél kezdődő része. A `forras` `#n`-je a szakasz
sorszáma.

Fejek a bekezdés elején: `<span class="lexheading">I.</span>` római (romai) · sima `A. ` nagybetű (nagy; csak a sorban
  következő betű: A, B, …) · `<b>1.</b>` szám (szam) · `<b>a.</b>` betű (betu). A felsőbb szint a mélyebbeket törli.
  F186 K2: a bekezdés eleji félkövér jelölő nem fej, ha „)”, „,”, „;”, „]” vagy kettőzött betű („bb.”) követi (a forrás
  kereszthivatkozás közepén tört bekezdést, pl. G4151 „<b>b.</b> bb.;”, G1909 „<b>c.</b>)):”).
Bekezdésen belüli fej (F186 K1; a seed-201 vak mérés 9 hibája, naplok/F186_jelentes.md): a forrás a bekezdés belsejében
  félkövér nélkül is nyit pontot („is used a. of time”, „; a: Luk 1:14”, „etc. h. of age”, „). 2. When …, it answers a.”).
  Ilyenkor a bekezdés a fejnél **kettéválik**: egy sor = egy szakasz (a bekezdés, vagy a bekezdésen belüli fejnél kezdődő
  része). A szabály: `belso_fejek` (a sorrendben várt következő betű/szám, a hivatkozás- és rövidítés-alakok kizárásával).
`utvonal`: `<felső>/<szám>/<betű>` (`-` a hiányzó szint; a felső a nagybetű és a római pontokkal: `A`, `I`, `A.I`);
különleges: `cim` (a `<b>G… — …</b>` / `<b>G…a: …</b>` címsor; újabb címsor a fejállapotot törli), `fej` (a cím után, az
első fej előtti bekezdés). Fej nélküli bekezdés az előző útvonalát örökli (`jel` üres).

Illesztés (`illesztes`, Strongonként): `egyezik` — a bekezdések szóközök nélküli szövege sorban, hézag és maradék
nélkül kiadja a TSV szövegét; `javitassal` — így van, de csak az `adat/thayer_forras_javitas.tsv` (SEMA 2.38, DT-F132i (2))
`javitva` sorainak beszúrásával: a határok a javított szövegen pontosak, a `szoveg` mező viszont a **nyers** TSV-szöveg (a
beszúrás nélkül; a javított szöveg nézet: `thayer_bemenet.szakaszok`); `reszleges` — nem így: a határok a difflib egyező blokkjain át vetülnek a TSV-szövegre
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
JAV_UT = os.path.join(GYOKER, 'adat', 'thayer_forras_javitas.tsv')
KI_UT = os.path.join(GYOKER, 'adat', 'thayer_szakaszok.tsv')

FEJLEC = ['strong', 'sorszam', 'utvonal', 'jel', 'szoveg', 'illesztes', 'forras', 'forras_hash', 'proveniencia']

HATAR = re.compile(r'</?p\b[^>]*>|</?div\b[^>]*>')
TAG = re.compile(r'<[^>]+>')
CIM = re.compile(r'^\s*<b>G\d+')
FEJ_ROMAI = re.compile(r'^\s*<span class="lexheading">((?:VIII|VII|VI|IV|IX|III|II|V|X|I)\.)</span>')
FEJ_B = re.compile(r'^\s*<b>(\d{1,2}\.|[a-z]\.)</b>')
FEJ_NAGY = re.compile(r'^([A-H])\.(?=\s)')
WS = re.compile(r'\s+')
# F186 K2: a bekezdés eleji félkövér jelölő, amelyet „)”, „,”, „;”, „]” vagy kettőzött betű („bb.”) követ, egy a forrásban
# kettétört kereszthivatkozás töredéke („<b>b.</b> bb.; γεννάω, …”, „<b>c.</b>)): as …”), nem fej (seed-201 T145).
HAMIS_FEJ_UTAN = re.compile(r'\s*[),;\]]|\s+([a-z])\1\.')
# F186 K1: bekezdésen belüli fej (félkövér nélkül is): kisbetű „a.”/„a:”/„i.:” vagy szám „2.” a szövegben (a címkék és a
# <ref>/<ref0> tartalma kitakarva), a sorrendben várt következő jelölő; l. `belso_fejek`.
TAKAR = re.compile(r'<(ref0?)\b[^>]*>.*?</\1>|<[^>]+>|&[#\w]+;', re.S)
BELSO_BETU = re.compile(r'(?<![\w&])([a-z])(\.:?|:)(?=[\s\x00]|$)')
BELSO_SZAM = re.compile(r'(?<=[.;:)][\s\x00])(\d{1,2})\.(?=\s+[\x00A-Za-z])')
# az előző szó, amely után a betű nem fej (rövidítés, utalás, hivatkozás): „i. e.”, „cf. a.”, „see b.”, „l. c.”, „p. 5 a.” …
NEM_FEJ_ELOTT = {'i', 'e', 'p', 'pp', 'l', 'cf', 'see', 'comp', 'vol', 'ed', 'no', 'ch', 'sq', 'ff', 'sub', 'under', 'art',
                 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                 'Rev', 'Rec', 'ad', 'et', 'ib', 'ibid', 'op', 'cit', 'loc', 'viz', 'q', 'v', 's', 'u', 'to'}
# a betű után álló folytatás, amely hivatkozásra vall: szám („h. a. 5, 19”), egybetűs rövidítés („a. d. Heb”, „b. g. 1”,
# „i. e.”, „e. g.”), utalás („c. below”, „c. above”, „b. at the end”)
BETU_UTAN_NEM = re.compile(r'[\s\x00]*(?:\d|[a-z]\.|([a-z])\1\.|below\b|above\b|at the end\b|init\b|fin\b)')
# a szám után álló római szám („1. ix. quaest.”): helyjelölés, nem fej
SZAM_UTAN_NEM = re.compile(r'\s+[ivxl]+\.')


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
    if m and not HAMIS_FEJ_UTAN.match(raw, m.end()):
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


def _takar(raw):
    """A raw azonos hosszú másolata, a címkék, a <ref>/<ref0> tartalma és az entitások helyén \\x00 (a pozíciók megmaradnak)."""
    return TAKAR.sub(lambda m: '\x00' * len(m.group(0)), raw)


def _elozo(tk, p):
    """(az előző nem szóköz, nem takart karakter, az előző szó) a `p` előtt a takart szövegben."""
    q = p - 1
    while q >= 0 and (tk[q].isspace() or tk[q] == '\x00'):
        q -= 1
    if q < 0:
        return '', ''
    kar = tk[q]
    if kar == '.':
        q -= 1
    elif not kar.isalpha():
        return kar, ''
    s = q
    while s >= 0 and tk[s].isalpha():
        s -= 1
    return kar, tk[s + 1:q + 1]


def belso_fejek(raw, t, kezdet=0):
    """F186 K1: a bekezdés belsejében (a `kezdet` után) nyitó fejek, sorrendben: [(poz a raw-ban, szint, jel, érték)].

    Fej a kisbetű („a.”, „a:”, „i.:”) vagy a szám („2.”), ha (1) a sorrendben várt következő jelölő (betű: az aktuális betű
    utáni, vagy `a`, ha nincs betű; szám: az aktuális szám utáni, vagy `1`); (2) betűnél utána szóköz, címke vagy a szöveg vége
    áll (nem „)”, „,”, „;”), az előtte álló karakter nem „,”, számjegy, „§”, „(”, „-”, „/”, „&”, az előző szó nem rövidítés
    vagy utalás (`NEM_FEJ_ELOTT`; „i. e.”, „e. g.” sem); (3) számnál előtte mondatzáró írásjel és szóköz, utána szóköz és szó
    áll. A `t` másolatán halad (a bekezdés eleji fej már benne van); a számfej a betűt törli (TOROL)."""
    tk = _takar(raw)
    t = dict(t)
    jelolt = []
    for m in BELSO_BETU.finditer(tk, kezdet):
        jelolt.append((m.start(), 'betu', m.group(0), m.group(1)))
    for m in BELSO_SZAM.finditer(tk, kezdet):
        jelolt.append((m.start(), 'szam', m.group(0), m.group(1)))
    ki = []
    for p, szint, jel, ertek in sorted(jelolt):
        if szint == 'betu':
            varhato = chr(ord(t['betu']) + 1) if t.get('betu') else 'a'
            if ertek != varhato:
                continue
            kar, szo = _elozo(tk, p)
            if kar and (kar in ',§(-/&=+' or kar.isdigit()):
                continue
            if szo in NEM_FEJ_ELOTT:
                continue
            if BETU_UTAN_NEM.match(tk, p + len(jel)):
                continue
        else:
            varhato = str(int(t['szam']) + 1) if (t.get('szam') or '').isdigit() else '1'
            if ertek != varhato or SZAM_UTAN_NEM.match(tk, p + len(jel)):
                continue
            # a szám előtt egybetűs vagy ismert rövidítés („orac. def. c. 1.”, „§ 27, 6 N. 1.”): fejezet-/jegyzetszám
            _, szo = _elozo(tk, p)
            if len(szo) == 1 or szo in NEM_FEJ_ELOTT:
                continue
        t[szint] = ertek
        for x in TOROL[szint]:
            t.pop(x, None)
        # a félkövér jelölő („<b>a.</b>”) a címkével együtt nyit
        q = p
        while q >= 3 and raw[q - 3:q] == '<b>':
            q -= 3
        ki.append((q, szint, jel.rstrip(':') if jel.endswith('.:') else jel, ertek))
    return ki


def szerkezet(definition):
    """-> [{'raw', 'plain', 'utvonal', 'jel'}] a szócikk szakaszaira: a bekezdések, a bekezdésen belüli fejeknél (F186 K1)
    kettévágva."""
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
            darabok = [(raw, utvonal(t), jel)]
        else:
            darabok = [(raw, utvonal(t) if allapot == 'fejes' else 'fej', '')]
        # a bekezdés eleji félkövér jelölő (fej vagy K2 szerinti hamis fej) a belső keresésből kimarad
        mb = FEJ_B.match(raw)
        kezdet = mb.end() if mb else 0
        belso = belso_fejek(raw, t, kezdet)
        if belso:
            elso_raw, elso_ut, elso_jel = darabok[0]
            darabok, elozo = [], 0
            vagas = [p for p, _, _, _ in belso]
            for i, (p, sz, j, ertek) in enumerate(belso):
                if i == 0:
                    darabok.append((raw[:p], elso_ut, elso_jel))
                t[sz] = ertek
                for x in TOROL[sz]:
                    t.pop(x, None)
                allapot = 'fejes'
                vege = vagas[i + 1] if i + 1 < len(vagas) else len(raw)
                darabok.append((raw[p:vege], utvonal(t), j))
            darabok = [d for d in darabok if sima(d[0])] or darabok[:1]
        for r, ut, j in darabok:
            ki.append({'raw': r, 'plain': sima(r) if len(darabok) > 1 else plain, 'utvonal': ut, 'jel': j})
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
    kat, tart = illeszt_tart(szak, tsv_szoveg)
    return kat, [tsv_szoveg[a:b].strip() if a is not None else '' for a, b in tart]


def illeszt_tart(szak, tsv_szoveg):
    """-> (kategória, [(a, b)] bekezdésenként: a szelet a TSV-szöveg nyers indexeiben; (None, None), ha üres)."""
    if tsv_szoveg is None:
        return 'sikertelen', [(None, None)] * len(szak)
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
            ki.append((None, None))
        else:
            ki.append((idx[a], idx[b - 1] + 1))
    return kat, ki


def sor_szoveg(jel, s):
    """A tábla `szoveg` mezője a nyers szeletből: a `jel` levágva, a szóközök összevonva."""
    return tisztit(jel_levag(jel, s.strip()))


def javitas_beolvas(ut=JAV_UT):
    """-> {Strong: [(tsv_poz, alak, sorszam, sor_poz)]} a javítótábla `javitva` soraiból (SEMA 2.38); {} ha a fájl nincs."""
    ki = {}
    if not ut or not os.path.exists(ut):
        return ki
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [x for x in f.read().split('\n') if x and not x.startswith('#')]
    fej = sorok[0].split('\t')
    for x in sorok[1:]:
        r = dict(zip(fej, x.split('\t')))
        if r['allapot'] == 'javitva':
            ki.setdefault(r['strong'], []).append((int(r['tsv_poz']), r['javitott_alak'], int(r['sorszam']), int(r['sor_poz'])))
    return ki


def beszur_pont(nyers, javitott, alak):
    """A `p`, amelyre nyers[:p] + alak + nyers[p:] == javitott (a közös előtagtól visszafelé keresve); None, ha nincs."""
    if len(javitott) != len(nyers) + len(alak):
        return None
    p = 0
    while p < len(nyers) and nyers[p] == javitott[p]:
        p += 1
    while p >= 0:
        if nyers[:p] + alak + nyers[p:] == javitott:
            return p
        p -= 1
    return None


def illeszt_javitassal(szak, tsv_szoveg, jav):
    """A TSV-szöveg a javítótábla beszúrásaival (jav: [(tsv_poz, alak, …)]).

    -> ('javitassal', [nyers sorszöveg], [(sor index, sor_poz, alak)]) ha a javított szöveg `egyezik`, és minden beszúrás
    egyetlen sor belsejébe esik, soronként legfeljebb egy; különben None (a javítás nem alkalmazható)."""
    if tsv_szoveg is None or not jav:
        return None
    reszek, tart, elozo, eltol = [], [], 0, 0
    for poz, alak in sorted((j[0], j[1]) for j in jav):
        if poz < elozo or poz > len(tsv_szoveg):
            return None
        reszek += [tsv_szoveg[elozo:poz], alak]
        tart.append((poz + eltol, poz + eltol + len(alak), alak))
        eltol += len(alak)
        elozo = poz
    reszek.append(tsv_szoveg[elozo:])
    kor = ''.join(reszek)
    kat, hat = illeszt_tart(szak, kor)
    if kat != 'egyezik':
        return None
    szovegek, beszurt = [], []
    hasznalt = 0
    for i, (x, (a, b)) in enumerate(zip(szak, hat)):
        if a is None:
            szovegek.append('')
            continue
        benne = [(c, d, al) for c, d, al in tart if a <= c and d <= b]
        if any((c < b and d > a) and not (a <= c and d <= b) for c, d, _ in tart) or len(benne) > 1:
            return None
        if not benne:
            szovegek.append(sor_szoveg(x['jel'], kor[a:b]))
            continue
        c, d, al = benne[0]
        nyers = sor_szoveg(x['jel'], kor[a:c] + kor[d:b])
        jav_sz = sor_szoveg(x['jel'], kor[a:b])
        p = beszur_pont(nyers, jav_sz, al)
        if p is None:
            return None
        szovegek.append(nyers)
        beszurt.append((i, p, al))
        hasznalt += 1
    if hasznalt != len(tart):
        return None
    return 'javitassal', szovegek, beszurt


def jel_levag(jel, szoveg):
    if jel and szoveg.startswith(jel):
        return szoveg[len(jel):].strip()
    return szoveg


def tisztit(s):
    return WS.sub(' ', s.replace('\t', ' ')).strip()


def general(ts, lex_ut=LEX_UT, tsv_ut=TSV_UT, jav_ut=JAV_UT):
    lex = lexikon_beolvas(lex_ut)
    tsv = tsv_beolvas(tsv_ut)
    javitas = javitas_beolvas(jav_ut)
    sorok, stat = [], collections.Counter()
    reszlet = {}
    for sp, (topic, d) in lex.items():
        szak = szerkezet(d)
        jr = illeszt_javitassal(szak, tsv.get(sp), javitas.get(sp))
        if jr is not None:
            kat, szovegek = jr[0], jr[1]
        else:
            kat, nyers = illeszt(szak, tsv.get(sp))
            szovegek = [sor_szoveg(x['jel'], sz) for x, sz in zip(szak, nyers)]
            if sp in javitas:
                stat['javitas_nem_alkalmazhato'] += 1
        stat[kat] += 1
        if kat != 'egyezik':
            reszlet[sp] = kat
        if any(x['jel'] for x in szak):
            stat['fejes_szocikk'] += 1
        for i, (x, sz) in enumerate(zip(szak, szovegek), 1):
            sorok.append([sp, str(i), x['utvonal'], x['jel'], sz, kat,
                          'Thayer.lexicon:%s#%d' % (topic, i), hashlib.sha256(x['raw'].encode('utf-8')).hexdigest()[:16],
                          'scope=%s | forras=thayer_jelolt/bont.py (fejléc) | ts=%s' % (sp, ts)])
    stat['strong'] = len(lex)
    stat['tsv_lexikonban_nincs'] = len(set(tsv) - set(lex))
    return sorok, stat, reszlet


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/thayer_jelolt/bont.py --ts %s — kézzel nem szerkesztendő (F132; séma: adat/SEMA.md, thayer_szakaszok.tsv).' % ts,
           '# forras: konkordancia/lexikonok_nyers/Thayer.lexicon@%s (csak szerkezet: bekezdéshatár, fej; DT327 (b)) + '
           'konkordancia/Thayer_teljes.tsv@%s (szöveg, illesztéssel) + adat/thayer_forras_javitas.tsv@%s (csak a határokhoz; '
           'DT333 (2)) + kód@%s'
           % (sha256_fajl(LEX_UT)[:12], sha256_fajl(TSV_UT)[:12],
              sha256_fajl(JAV_UT)[:12] if os.path.exists(JAV_UT) else 'nincs', kod_hash()[:12]),
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
    print('Strong: %d; illesztés: egyezik %d, javitassal %d, reszleges %d, sikertelen %d; fejes szócikk %d; '
          'a TSV-ben a lexikonon kívül: %d; a javítás nem alkalmazható: %d'
          % (stat['strong'], stat['egyezik'], stat['javitassal'], stat['reszleges'], stat['sikertelen'], stat['fejes_szocikk'],
             stat['tsv_lexikonban_nincs'], stat['javitas_nem_alkalmazhato']))
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
