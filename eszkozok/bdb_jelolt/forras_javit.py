#!/usr/bin/env python
"""A BDB forráshibáinak javítótáblája (F107, 5. lépés; DT-F107f (a), felhasználó, 2026-10-18).

Egyetlen hibaosztály (ma): `pe_mem` — a DictBDB.json a dagesses pét dagesses memként írja (0 dagesses pe a JSON-ban,
`naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 2.2). A tábla az `adat/bdb_szakaszok.tsv` `szoveg` mezőjének MINDEN dagesses
memjére egy sort ad (a szó és azon belül a dagesses mem sorszámával), és eldönti:

  javitva       a mem → pe cserével kapott alak az illesztett lexikon-szócikk héber szavai között áll
                (és a változatlan alak nem): a javított alak a SZABÁLYBÓL jön, a lexikon csak igazol (DT-F107a (i))
  valodi_mem    a változatlan (dagesses mem-es) alak áll a lexikon-szócikkben: nem hiba
  jelolt_marad  egyik sem igazolt (a szóalak a lexikonban eltér, vagy a sornak nincs bdb_id-je): nincs javítás

Összevetés: NFD, a kantilláció (U+0591–U+05AF), a meteg (U+05BD), a paszek/szof pászuk (U+05C0, U+05C3) és a
U+200E nélkül, a holem haser for vav (U+05BA) holemként (U+05B9).

A nyers fájl (DictBDB.json) és a szakasztábla NEM változik; a javítás alkalmazása a szöveg-nézetben a DT-F107c (6. lépés)
döntése. Kimenet: adat/bdb_forras_javitas.tsv (séma: adat/SEMA.md, „bdb_forras_javitas.tsv”).

Módok: (alap) írás · --ellenoriz bájtos összevetés a fájllal · --meres csak számok.
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import sqlite3
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
LEX_UT = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'BDB.lexicon')
KI_UT = os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')

MEM, PE, DAG = 'מ', 'פ', 'ּ'
HEBER_SZO = re.compile(r'[֐-׿]+')
FEJLEC = ['strong', 'sorszam', 'bdb_id', 'hiba', 'szo_sorszam', 'elofordulas', 'forras_alak', 'javitott_alak',
          'allapot', 'indok', 'proveniencia']


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def kod_hash():
    with open(os.path.abspath(__file__), 'rb') as f:
        return hashlib.sha256(f.read().replace(b'\r\n', b'\n')).hexdigest()


def norm(szo):
    s = unicodedata.normalize('NFD', szo)
    s = ''.join(c for c in s if not ('֑' <= c <= '֯' or c in 'ֽ׀׃‎'))
    return s.replace('ֺ', 'ֹ')


def mem_dagesh_helyek(nfd):
    """A dagesses mem-ek indexei (a mem betű pozíciója) az NFD alakban."""
    helyek = []
    for i, c in enumerate(nfd):
        if c == MEM:
            j = i + 1
            while j < len(nfd) and '֑' <= nfd[j] <= 'ׇ':
                if nfd[j] == DAG:
                    helyek.append(i)
                    break
                j += 1
    return helyek


def cserel(nfd, helyek):
    s = list(nfd)
    for i in helyek:
        s[i] = PE
    return ''.join(s)


def lexikon_szavak():
    con = sqlite3.connect('file:' + LEX_UT.replace('\\', '/') + '?mode=ro', uri=True)
    ki = {}
    for t, d in con.execute("select Topic, Definition from Lexicon where Topic like 'BDB%'"):
        szoveg = re.sub(r'<[^>]+>', ' ', d)
        ki[t] = set(norm(w) for w in HEBER_SZO.findall(unicodedata.normalize('NFD', szoveg)))
    con.close()
    return ki


def tabla_sorok():
    with open(TABLA, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[3:] if s]


def general(ts):
    lex = lexikon_szavak()
    ki, stat = [], collections.Counter()
    prov = 'scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc) | ts=%s'
    for r in tabla_sorok():
        szavak = HEBER_SZO.findall(unicodedata.normalize('NFD', r['szoveg']))
        for si, szo in enumerate(szavak, 1):
            helyek = mem_dagesh_helyek(szo)
            if not helyek:
                continue
            lszavak = lex.get(r['bdb_id'])
            for ei, h in enumerate(helyek, 1):
                egy = cserel(szo, [h])
                mind = cserel(szo, helyek)
                if lszavak is None:
                    allapot, jav, indok = 'jelolt_marad', '', 'a sornak nincs bdb_id-je (illesztes=%s): nincs igazoló szócikk' % r['illesztes']
                elif norm(egy) in lszavak and norm(szo) not in lszavak:
                    allapot, jav, indok = 'javitva', egy, 'a pe-s alak a %s szócikkben áll, a mem-es nem' % r['bdb_id']
                elif len(helyek) > 1 and norm(mind) in lszavak and norm(szo) not in lszavak:
                    allapot, jav, indok = 'javitva', mind, 'a szó minden dagesses memjét pére cserélve a %s szócikk alakja' % r['bdb_id']
                elif norm(szo) in lszavak:
                    allapot, jav, indok = 'valodi_mem', '', 'a dagesses mem-es alak a %s szócikkben áll: nem hiba' % r['bdb_id']
                else:
                    allapot, jav, indok = 'jelolt_marad', '', 'egyik alak sincs a %s szócikk héber szavai között' % r['bdb_id']
                stat[allapot] += 1
                ki.append([r['strong'], r['sorszam'], r['bdb_id'], 'pe_mem', str(si), str(ei), szo, jav, allapot, indok,
                           prov % (r['strong'], ts)])
    ki.extend(kezi_sorok(stat))
    ki.extend(hivatkozas_sorok(stat, ts))
    ki.extend(kezi_hivatkozas_sorok(stat))
    return ki, stat


# ---------------------------------------------------------------- hivatkozas (DT-F107c (d), felhasználó, 2026-10-18)
# A BDB_teljes_unabridged.tsv 247 sorát a #34 (ψ, naplok/F34_M2_csere.tsv) és a #46 (könyvfeloldás,
# naplok/BDB_KONYVFELOLDAS_csere.tsv és _kezi.tsv) utólag javította. Ezek a javítások a nyers JSON-ban nincsenek; hogy a táblából
# generált nézet ne lépjen vissza, a javítótábla átveszi őket: a TSV és a JSON (a _convert_bdb.py szerint újrakonvertálva) szóköz
# szerinti tokenjeinek eltérő szakaszai (difflib), soronként egy. `elofordulas` = a `forras_alak` hányadik egész-token előfordulása
# a Strong nézet-szövegében (a jel + szoveg sorok egy szóközzel); `sorszam` = a táblasor, amelyben ez az előfordulás áll.
F34_CSERE = os.path.join(GYOKER, 'naplok', 'F34_M2_csere.tsv')
F46_CSERE = os.path.join(GYOKER, 'naplok', 'BDB_KONYVFELOLDAS_csere.tsv')
F46_KEZI = os.path.join(GYOKER, 'naplok', 'BDB_KONYVFELOLDAS_kezi.tsv')
TSV = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')


def _ws(t):
    return re.sub(r'\s+', ' ', t).strip()


def _tsv_olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


# A csere-naplókban nem szereplő, a git-történettel igazolt TSV-javítások (git log -G Pharaoh -- konkordancia/BDB_teljes_unabridged.tsv:
# a három sort a 6400b5a7 „F46.6: gépi csere a DT-F46 szerint” írta át; ellenőrizve 2026-10-18)
GIT_FORRAS = {
    (st, 'Phoenician', 'Pharaoh'): 'F46.6 (git 6400b5a7, gépi csere; a csere-naplóban nem szerepel)'
    for st in ('H5973', 'H7588', 'H9005')
}


def ref_kulcs(ref):
    """Hivatkozás-kulcs: (a könyvnév első 3 betűje kisbetűvel, a számelőtaggal; fejezet:vers) — „1Ki 50:1” = „1Kin 50:1”."""
    m = re.search(r'([1-3]?)\s*([A-Za-z]+)\.?\s+(\d+:\d+)', ref)
    if not m:
        return None
    return (m.group(1) + m.group(2)[:3].lower(), m.group(3))


def forrasjavitas_index():
    """(strong, az ÚJ hivatkozás kulcsa) → a javítás forrása (F34 / F46 csere / F46 kézi)."""
    idx = {}
    for d in _tsv_olvas(F34_CSERE):
        k = ref_kulcs(d.get('uj', ''))
        if d.get('dontes') == 'JAVIT' and k:
            idx.setdefault((d['szocikk_id'], k), 'F34 (naplok/F34_M2_csere.tsv, JAVIT)')
    for ut, nev in ((F46_CSERE, 'F46 (naplok/BDB_KONYVFELOLDAS_csere.tsv)'), (F46_KEZI, 'F46 (naplok/BDB_KONYVFELOLDAS_kezi.tsv)')):
        for d in _tsv_olvas(ut):
            k = ref_kulcs(d.get('javasolt_forras_alak', ''))
            if k:
                idx.setdefault((d['strong'], k), nev)
    return idx


def token_elofordulas(szoveg, token):
    """Az egész-token (szóközzel határolt) előfordulások kezdőpozíciói."""
    return [m.start() for m in re.finditer(r'(?<!\S)' + re.escape(token) + r'(?!\S)', szoveg)]


def strong_nezet(sorok):
    """A Strong nézet-szövege (jel + szoveg, egy szóközzel) és a sorhatárok."""
    darabok, hatar, p = [], [], 0
    for x in sorok:
        t = ' '.join(y for y in (x['jel'], x['szoveg']) if y)
        if not t:
            continue
        if darabok:
            p += 1
        hatar.append((p, p + len(t), x))
        darabok.append(t)
        p += len(t)
    return ' '.join(darabok), hatar


def hivatkozas_sorok(stat, ts):
    import json
    sys.path.insert(0, ITT)
    import bont
    import forras_osszevetes
    import difflib
    with open(TSV, encoding='utf-8', newline='') as f:
        tsv = {s.split('\t')[0]: s.split('\t')[2] for s in f.read().split('\n')[1:] if s}
    with open(bont.JSON_UT, encoding='utf-8') as f:
        ujra = {}
        for item in json.load(f):
            m = re.match(r'^H(\d+)', item.get('top', ''))
            if m:
                ujra['H%04d' % int(m.group(1)) + item['top'][len(m.group(0)):]] = forras_osszevetes.strip_html_142ad625(item['def'])
    tabla = collections.OrderedDict()
    for r in tabla_sorok():
        tabla.setdefault(r['strong'], []).append(r)
    idx = forrasjavitas_index()
    ki = []
    for st in tabla:
        if st not in tsv or st not in ujra or _ws(tsv[st]) == _ws(ujra[st]):
            continue
        a, b = _ws(ujra[st]).split(' '), _ws(tsv[st]).split(' ')
        nezet, hatar = strong_nezet(tabla[st])
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == 'equal':
                continue
            x, y = ' '.join(a[i1:i2]), ' '.join(b[j1:j2])
            # hányadik előfordulás a JSON-szövegben (a nézetben ugyanannyiadik)
            elotte = ' '.join(a[:i1])
            k = len(token_elofordulas(elotte + ' ' + x, x)) if x else 0
            poz = token_elofordulas(nezet, x) if x else []
            sor = next((h[2] for h in hatar if poz and len(poz) >= k and h[0] <= poz[k - 1] < h[1]), None)
            # az új hivatkozás: ha a szakasz csak könyvnév, a fejezet:vers a TSV következő tokenje
            if not re.search(r'\d+:\d+', y):
                uj_ref = y + ' ' + (b[j2] if j2 < len(b) else '')
            elif not re.search(r'[A-Za-z]{2,}\.?\s+\d+:\d+', y) and j1 > 0:
                uj_ref = b[j1 - 1] + ' ' + y          # csak fejezet:vers változott: a könyvnév az előző token
            else:
                uj_ref = y
            forras = idx.get((st, ref_kulcs(uj_ref))) or GIT_FORRAS.get((st, x, y))
            if sor is None:
                allapot, indok = 'jelolt_marad', 'a forrás-alak a tábla nézet-szövegében nem található (%d. előfordulás)' % k
                stat['hivatkozas_jelolt_marad'] += 1
            else:
                allapot = 'javitva'
                indok = 'a TSV utólagos hivatkozás-javítása (a nyers JSON-ban nincs): %s' % (forras or 'a forrásjavítás-naplóban nem azonosított')
                stat['hivatkozas_javitva'] += 1
                if not forras:
                    stat['hivatkozas_forras_nem_azonositott'] += 1
            ki.append([st, sor['sorszam'] if sor else '', sor['bdb_id'] if sor else '', 'hivatkozas', '', str(k), x, y,
                       allapot, indok,
                       'scope=%s | forras=bdb_jelolt/forras_javit.py (fejléc): BDB_teljes_unabridged.tsv ↔ DictBDB.json, %s | ts=%s'
                       % (st, (forras or 'F34/F46').split(' ')[0], ts)])
    return ki


# DT-F107g (b), felhasználó, 2026-10-18: a szerkezeti forráshibák (a jelölő a nyers forrásban hiányzik vagy hamis), mindegyik a
# DictBDB.json-ban ÉS a BDB.lexicon-ban igazolva (naplok/F107_BDB_JELOLT_SZOVEG_naplo.md 4.6). Kézi sorok: `allapot=kezi`,
# proveniencia `manual`. A `sorszam` a szakasztábla azon sora, amelynek `jel`+`szoveg`-e a horgonyt tartalmazza (az első);
# a `forras_alak` a nyers JSON rövid részlete, a `javitott_alak` a várt szerkezet (útvonal).
# (strong, horgony, hiba, forras_alak, javitott_alak, indok)
KEZI = [
    ('H0559', 'Qal Perfect', 'jelolo_hianyzik', '— Qal <i>Perfect</i> ׳א Gen 3:1', 'Qal',
     'a „Qal” törzsnév sima szöveg (nem félkövér) a DictBDB.json-ban és a BDB.lexicon-ban is; a törzsszint ezért a táblában '
     'nem nyílik meg (aranyminta: Qal, Qal/1–4; seed-101 M102)'),
    ('H0559', 'Say (subject God', 'jelolo_hianyzik', 'April, 1887, 263</sup>.1<i>Say</i>', 'Qal/1',
     'az „1” a DictBDB.json-ban sima szöveg a lapszám után; a BDB.lexicon ugyanitt jelöl: <div class="section"><p>1. Say '
     '(a JSON hibája, a lexikon igazolja; seed-101 M102)'),
    ('H0539', 'as abstract noun see', 'jelolo_hianyzik', 'see אֵמֻן. Niph`al נֶאֱמַן Prov 11:13', "Niph'al",
     'a „Niph`al” törzsnév sima szöveg mindkét forrásban (seed-101 M117)'),
    ('H0539', 'carried by a nurse', 'jelolo_hianyzik', 'Deut 28:59. 1.<i>carried</i>', "Niph'al/1",
     'az „1.” jelöletlen mindkét forrásban (a lexikonban „28:59. 1. carried”, a 2. pont már <div class="point">) (seed-101 M117)'),
    ('H3318', 'go or come out or forth', 'jelolo_hianyzik', '— </p><p><b>1</b> <i>go</i> or <i>come out</i>', 'Qal/1',
     'a „Qal” törzsnév az első törzs előtt mindkét forrásban hiányzik (lexikon: „— <div class="point"><b>1.</b> go or come '
     'out”) (seed-101 M162)'),
    ('H4900', 'trail seed', 'hamis_jelolo', 'compare </p><p><b>Niph`al 6.</b> <i>trail</i>', 'Qal/6',
     'a „compare Niph`al” hivatkozás törzsneve a 6. jelentés félkövér fejébe olvadt mindkét forrásban (lexikon: '
     '„compare </div><div class="point"><b>Niph`al 6.</b>”); a 6–7. jelentés a Qal-é (aranyminta: Qal/6, Qal/7)'),
    ('H1242', 'figurative of bright joy', 'hamis_jelolo', '<b>d.</b> above, &amp; below </p><p><b>2. g.</b>', '-/1/g',
     'a „2.” a g. alpont fejében téves mindkét forrásban (lexikon: <div class="point"><b>2. g.</b>); a g–h alpont az 1. '
     'jelentésé, a 2. jelentés később következik („morrow, next day”) (aranyminta: -/1/g, -/1/h)'),
    # F107 javítókör (ELLENOR_F107 szúrópróba, 2026-10-18): mindkettő a DictBDB.json-ban ÉS a BDB.lexicon-ban igazolva
    ('H6440', '= presence, person', 'hamis_jelolo', '— See further below </p><p><b>7. 2. a.</b> = <i>presence, person</i>', '-/2/a',
     'a „See further below 7” hivatkozás „7.”-e a 2. jelentés a. alpontjának félkövér fejébe olvadt mindkét forrásban (lexikon: '
     '„See further below </div><div class="point"><b>7. 2. a.</b>”); az útvonal (-/2/a, I. szakasz) helyes, a „7.” a fejben hamis'),
    ('H6440', '(a) in the face of, mostly', 'hamis_jelolo', 'see II. אֵת <b>4a. 3.</b> בִּפְנֵי: <i>(a) in the face of</i>', '-/3',
     'a „see II. אֵת 4a” hivatkozás „4a.”-ja a II. szakasz 3. jelentésének (בִּפְנֵי) fejébe olvadt mindkét forrásban (lexikon: '
     '„see II. אֵת </div><div class="point"><b>4 a. 3.</b> בִּפְנֵי”); a JSON-ban a fej a bekezdés közepén, héber szó után áll, ezért a '
     'tábla nem nyit szakaszt: a II/3 csomópont hiányzik (aranyminta: II -/3; a szakaszt figyelmen kívül hagyó összevető ezt az I/3-mal '
     'fedte, l. napló, Javítókör)'),
]


# DT-F131k (a) (felhasználó, 2026-10-28): kézi hivatkozás-javítás (`hivatkozas_kezi`). A BDB forrásszövege (a DictBDB.json és a
# BDB_teljes_unabridged.tsv is) létező, de hibás verset idéz; a 2.23 (`bdb_igehely_javitas.tsv`) csak nem létező fejezetet javít,
# ezért kézi sor. `allapot=kezi`, proveniencia `manual`; a `forras_alak` / `javitott_alak` a fejezet:vers token, az `elofordulas` a
# `forras_alak` hányadik egész-token előfordulása a Strong nézet-szövegében. A szöveg-nézet (nezet_general.py, szakasz_bemenet.py)
# NEM alkalmazza (a fordító bemenete változatlan); a 2.29 kinyerője (olvaso_szerver/bdb_vers_jelentes.py) olvassa, és a feloldott
# verset javítja. (strong, horgony, forras_alak, javitott_alak, indok)
KEZI_HIVATKOZAS = [
    ('H8034', 'in worship, so 12:8; 13:4; 21:33; 26:35', '26:35', '26:25',
     'a BDB „call with … the name ׳י in worship, so 12:8; 13:4; 21:33; 26:35” sora (1Móz) a 26:35-öt idézi; ott a שֵׁם nem áll '
     '(Ézsau feleségei), a TAHOT szerint az 1Móz 26:25-ben áll a קָרָא mellett (H7121 + H8034), és a szövegkörnyezet (oltárt épít, '
     'segítségül hívja az Úr nevét) a 12:8; 13:4; 21:33 formulája: sajtóhiba a forrásban, 26:35 → 26:25 (DT-F131k (a))'),
]


def kezi_hivatkozas_sorok(stat):
    tabla = collections.OrderedDict()
    for r in tabla_sorok():
        tabla.setdefault(r['strong'], []).append(r)
    ki = []
    for st, horgony, forras_alak, javitott, indok in KEZI_HIVATKOZAS:
        nezet, hatar = strong_nezet(tabla.get(st, []))
        h = next((h for h in hatar if horgony in nezet[h[0]:h[1]]), None)
        if h is None:
            raise SystemExit('HIBA: a kézi hivatkozás-sor horgonya nem található: %s %r' % (st, horgony))
        poz = token_elofordulas(nezet, forras_alak)
        k = next((i for i, p in enumerate(poz, 1) if h[0] <= p < h[1] and p >= h[0] + nezet[h[0]:h[1]].find(horgony)), None)
        if k is None:
            raise SystemExit('HIBA: a kézi hivatkozás-sor forrás-alakja nem található a horgonyban: %s %r' % (st, forras_alak))
        stat['hivatkozas_kezi'] += 1
        ki.append([st, h[2]['sorszam'], h[2]['bdb_id'], 'hivatkozas_kezi', '', str(k), forras_alak, javitott, 'kezi', indok,
                   'manual'])
    return ki


def kezi_sorok(stat):
    sorok = tabla_sorok()
    ki = []
    for st, horgony, hiba, forras_alak, javitott, indok in KEZI:
        r = next((x for x in sorok if x['strong'] == st and horgony in (x['jel'] + ' ' + x['szoveg'])), None)
        if r is None:
            raise SystemExit('HIBA: a kézi sor horgonya nem található: %s %r' % (st, horgony))
        stat['kezi'] += 1
        ki.append([st, r['sorszam'], r['bdb_id'], hiba, '', '', forras_alak, javitott, 'kezi', indok, 'manual'])
    return ki


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/bdb_jelolt/forras_javit.py --ts %s — kézzel nem szerkesztendő (F107, DT228 (a); séma: adat/SEMA.md, bdb_forras_javitas.tsv). A héber alakok NFD-ben.' % ts,
           '# forras: adat/bdb_szakaszok.tsv@%s + konkordancia/lexikonok_nyers/BDB.lexicon@%s (csak igazolás) + kód@%s'
           % (sha256_fajl(TABLA)[:12], sha256_fajl(LEX_UT)[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    sorok, stat = general(a.ts)
    print('sor: %d (pe_mem + kezi); %s; érintett Strong (javitva): %d' % (
        len(sorok), dict(stat), len(set(s[0] for s in sorok if s[8] == 'javitva'))))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, a.ts)
    if a.ellenoriz:
        with open(KI_UT, encoding='utf-8', newline='') as f:
            if f.read() != szoveg:
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
