#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/glossza_forditas.py -- F140 GLOSSZA_FORDITAS: a TBESH rovid glosszajanak
(7. oszlop) magyar forditasa a heber Strong-szamokra.

M0 allapot: csak a meres es a sor-valasztas (--m0). A forditas (M1) nincs benne.

A TBESH tab-tagolt; az adatsorok az 'eStrong#' fejlecsor utan kezdodnek:
  0 eStrong  1 dStrong ('H2763A =' vagy 'H0430G = a Name of')  2 uStrong
  3 Hebrew  4 Transliteration  5 Morph  6 Gloss  7 Meaning
Olvasas split('\t')-bel (CLAUDE.md: a csv modul tilos).
"""
import sys
import os
import re
import hashlib
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBESH = os.path.join(GYOKER, 'konkordancia', 'TBESH.txt')
SZOTAR = os.path.join(GYOKER, 'konkordancia', 'Strong_szotar.tsv')
TAHOT = os.path.join(GYOKER, 'konkordancia', 'TAHOT_kivonat.tsv')

HEBER_SOR = re.compile(r'^H\d{4}[a-z]?$')


def sha1(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


def tbesh_sorok():
    """A TBESH heber adatsorai szotarkent: alap, estrong, entry_id, kapcsolat, ..."""
    sorok = []
    ban = False
    with open(TBESH, encoding='utf-8-sig') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if sor.startswith('eStrong#\tdStrong'):
                ban = True
                continue
            if not ban:
                continue
            m = sor.split('\t')
            if len(m) < 8 or not HEBER_SOR.match(m[0]):
                continue
            els, _, kapcs = m[1].partition('=')
            sorok.append({
                'alap': m[0][:5],
                'estrong': m[0],
                'entry_id': els.strip(),
                'kapcsolat': kapcs.strip(),
                'ustrong': m[2],
                'lemma': m[3],
                'atiras': m[4],
                'szofaj': m[5],
                'glossza': m[6],
                'definicio': m[7],
            })
    return sorok


def szotar_strongok():
    ki = []
    with open(SZOTAR, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.rstrip('\n').split('\t')
            if m and re.match(r'^H\d{4}$', m[0]):
                ki.append(m[0])
    return ki


# Fallback-sorrend: ha nincs kapcsolat nelkuli sor, ezek a kapcsolatok NEM elsodlegesek
# (reszlet-, jelentes- es osszetett alsor), csak ha nincs jobb.
GYENGE_KAPCSOLAT = ('a Part of', 'combination of', 'a Meaning of')


def valaszt(sorok_alap):
    """Sor-valasztasi szabaly (M0-javaslat): visszaadja (forditando sorok, kimarado sorok).
    A: a kapcsolat nelkuli sorok mind fordulnak (homonimak a/b, kulon entry_id).
    B: ha nincs ilyen, az elso nem 'gyenge' kapcsolatu sor a fo glossza (pl. H0430G
       'a Name of'; H0576A 'in Aramaic of'); ha csak gyenge van, az elso sor.
    C: a tobbi kapcsolt alsor ('a Part of', 'a Meaning of', 'a Spelling of', ...) kimarad.
    """
    fo = [s for s in sorok_alap if s['kapcsolat'] == '']
    if fo:
        return fo, [s for s in sorok_alap if s['kapcsolat'] != '']
    jo = [s for s in sorok_alap if s['kapcsolat'] not in GYENGE_KAPCSOLAT]
    valasztott = (jo or sorok_alap)[0]
    return [valasztott], [s for s in sorok_alap if s is not valasztott]



NEVTOREDEK = re.compile(r'^\s*(This name|means)|Combined with')


def fo_jelolt(sorok_alap):
    """Strongonkenti kiemelt (fo) sor javaslata: az elso kapcsolat nelkuli sor, amelynek
    glosszaja nem zarojeles es definicioja nem nevtoredek ('Combined with', 'This name ...');
    ha nincs, az elso kapcsolat nelkuli sor; ha az sincs, a valaszt() B-fallbackja."""
    tiszta = [s for s in sorok_alap if s['kapcsolat'] == '' and '(' not in s['glossza']
              and not NEVTOREDEK.search(s['definicio'][:80])]
    if tiszta:
        return tiszta[0]
    fo = [s for s in sorok_alap if s['kapcsolat'] == '']
    if fo:
        return fo[0]
    return valaszt(sorok_alap)[0][0]


# ---------------------------------------------------------------- prompt (M0-javaslat v1)
PROMPT_V1 = """Feladat: a TBESH héber szótár rövid angol glosszájának (Gloss) magyar fordítása.
Kimenet: szavanként EGY sor, `<entry_id><TAB><magyar jelentés>`; semmi más.

Szabályok:
1. A magyar jelentés rövid: legfeljebb ~5 szó; több értelem pontosvesszővel (`;`) elválasztva.
2. Szófaj nélkül írd (ne legyen benne „ige”, „főnév”); főnév alanyesetben, ige főnévi igenévvel
   („mondani”), melléknév alapfokon, a glosszában jelzett nemet/számot (pl. „(f.s.)”) megtartva.
3. A glossza a fő támpont. A héber lemma, az átírás, a szófaj és a definíció eleje csak
   kontextus a többértelmű glosszához (pl. `to devote/destroy`): a glosszát ne cseréld le a definícióra.
4. Tulajdonnév: a magyar (Károli-hagyományú) névalak (Rehoboam → Roboám, Abijah → Abija);
   ha nincs hagyományos magyar alak, magyaros átírás. Személy- és helynévnél semmi magyarázat.
5. Istennevek (Károli-szóhasználat): `YHWH`/`LORD` (H3068) → „az ÚR”; `God` (H0430) → „Isten”;
   `Lord` (H0136) → „Úr”; `El` → „Isten” vagy „El” (a glossza szerint). Ne írj „Jehova”-t, ha a glossza nem.
6. Jelölők: `[Obj.]`, `(f.s.)`, `+` és hasonló szögletes/zárójeles jelölők jelentése megmarad
   magyarul (pl. „[tárgyjel]”); kettősponttal bővített glossza („land: country”) → „föld: ország”.
7. Nincs benne héber vagy görög betű, angol szó, idézőjel, magyarázat, kérdőjel.
8. Terminológia (kötelező megfelelők): {terminologia}
9. Bizonytalanságot ne jelezz a szövegben; a nehéz esetre a sor végére `<TAB>?` kerül.

Bemenet (soronként: entry_id | lemma | átírás | szófaj | Gloss | definíció eleje):
{bemenet}
"""

TERMINOLOGIA = os.path.join(GYOKER, 'adat', 'terminologia.tsv')
KONTEXTUS_HOSSZ = 200


def terminologia_sorok():
    """A terminologia.tsv egyszavas/rovid kulcsai (kapu != nem), legujabb verzio."""
    ki = {}
    with open(TERMINOLOGIA, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) < 5 or m[0] == 'angol' or m[4] == 'nem':
                continue
            ki[m[0]] = m[1]
    return ki


def prompt_epit(sorok):
    """Egy kotegre: a glosszakban/definicio-elejeken elofordulo terminologiai kulcsok
    + a kotegbemenet. Nincs modellhivas."""
    szoveg = ' '.join(s['glossza'] + ' ' + s['definicio'][:KONTEXTUS_HOSSZ] for s in sorok).lower()
    term = terminologia_sorok()
    talalt = ['%s -> %s' % (k, v) for k, v in term.items() if k.lower() in szoveg and len(k) > 3]
    bemenet = '\n'.join('%s | %s | %s | %s | %s | %s' % (
        s['entry_id'], s['lemma'], s['atiras'], s['szofaj'], s['glossza'],
        re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s['definicio']))[:KONTEXTUS_HOSSZ]) for s in sorok)
    return PROMPT_V1.format(terminologia='; '.join(talalt) if talalt else '(ebben a kötegben nincs)',
                            bemenet=bemenet)


# ---------------------------------------------------------------- kapuk (M0-javaslat)
MAX_KARAKTER = 50
MAX_SZO = 6
ANGOL_FUNKCIOS = {'the', 'of', 'to', 'a', 'an', 'and', 'or', 'in', 'on', 'for', 'with', 'by', 'is',
                  'be', 'not', 'from', 'that', 'this', 'it', 'as', 'at', 'who', 'which'}
# kivetel-lista: ASCII-s magyar szavak, amelyek angol szonak is latszanak (bovitheto)
ANGOL_KIVETEL = {'an', 'is', 'as', 'at', 'or', 'on', 'it', 'be', 'to', 'in', 'a', 'by'}
HEBER_GOROG = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF\uFB1D-\uFB4F]')


def kapuk(sor, hu, forras_hash_elteres=False):
    """Gepi kapuk egy sorra; visszaadja a hibak listajat (ures = atment)."""
    hibak = []
    if not hu or not hu.strip():
        return ['ures']
    if HEBER_GOROG.search(hu):
        hibak.append('heber/gorog betu')
    szavak = re.findall(r"[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű'-]+", hu)
    if len(hu) > MAX_KARAKTER or len(szavak) > MAX_SZO:
        hibak.append('hossz (%d kar, %d szo)' % (len(hu), len(szavak)))
    # angol szo: (a) a forras-glossza ASCII-s szava szerepel a kimenetben (kiveve a tulajdonnevet,
    # amely kisbetus-nem-egyezo) vagy (b) angol funkciószo; a kivétel-lista felülírja
    forras = {w.lower() for w in re.findall(r"[A-Za-z']+", sor['glossza'])} - ANGOL_KIVETEL
    for w in szavak:
        wl = w.lower()
        if wl in ANGOL_KIVETEL or w[0].isupper():
            continue  # nagybetus szo: tulajdonnev-alak, a forras-egyezes nem hiba
        if wl in ANGOL_FUNKCIOS or (wl in forras and len(wl) > 3):
            hibak.append('angol szo: ' + w)
    if re.search(r'["“”?]', hu):
        hibak.append('tiltott jel')
    return hibak


def m0():
    sorok = tbesh_sorok()
    alapok = defaultdict(list)
    for s in sorok:
        alapok[s['alap']].append(s)
    szot = szotar_strongok()
    kulso = sorted(set(alapok) - set(szot))
    print('TBESH-ban van, szotar-ban nincs (a hatokorbol kimarad):', kulso)
    alapok = defaultdict(list, {a: v for a, v in alapok.items() if a in set(szot)})
    sorok = [s for s in sorok if s['alap'] in alapok]
    print('hatokor (8718 Strong): sor', len(sorok), '; fo-jelolt (Strongonkent 1):', len({fo_jelolt(v)['entry_id'] for v in alapok.values()}))
    print('TBESH heber sor:', len(sorok))
    print('TBESH alapszam:', len(alapok))
    print('Strong_szotar heber Strong:', len(szot), '(egyedi %d)' % len(set(szot)))
    print('szotar-ban van, TBESH-ban nincs:', sorted(set(szot) - set(alapok)))
    print('TBESH-ban van, szotar-ban nincs:', sorted(set(alapok) - set(szot)))
    print('entry_id egyedi:', len({s['entry_id'] for s in sorok}), 'sor:', len(sorok))
    print('kapcsolat-tipusok:', Counter(s['kapcsolat'] for s in sorok).most_common())
    egy = sum(1 for v in alapok.values() if len(v) == 1)
    print('1 soros alap:', egy, '; tobb soros:', len(alapok) - egy)
    nincs_fo = [a for a, v in alapok.items() if all(s['kapcsolat'] != '' for s in v)]
    print('alap kapcsolat nelkuli sor NELKUL:', len(nincs_fo), nincs_fo[:20])
    tobb_fo = {a: [s['entry_id'] for s in v if s['kapcsolat'] == ''] for a, v in alapok.items()
               if sum(1 for s in v if s['kapcsolat'] == '') > 1}
    print('alap >1 kapcsolat nelkuli sorral (homonima):', len(tobb_fo))
    fordit = []
    kimarad = []
    for a, v in alapok.items():
        f, k = valaszt(v)
        fordit += f
        kimarad += k
    print('M0 szabaly: fordítandó sor:', len(fordit), '; kimarado (kapcsolt alsor):', len(kimarad))
    print('  ebbol B-fallback (nincs fo sor) alap:', len(nincs_fo))
    print('fordítandó entry_id egyedi:', len({s['entry_id'] for s in fordit}))
    ures = [s['entry_id'] for s in fordit if not s['glossza'].strip()]
    print('fordítandó, de üres glossza:', len(ures), ures[:10])
    gl = [len(s['glossza']) for s in fordit]
    print('glossza karakter (fordítandó sorok):', sum(gl), 'max', max(gl))
    ctx = sum(len(s['definicio'][:200]) for s in fordit)
    print('definicio[:200] karakter (fordítandó):', ctx)
    print('szofaj-kodok:', Counter(s['szofaj'].split(':')[0] + ':' + s['szofaj'].split(':')[1][:1]
                                  if ':' in s['szofaj'] else s['szofaj'] for s in fordit).most_common(12))
    print('glossza zarojeles/szogletes:', sum(1 for s in fordit if '(' in s['glossza'] or '[' in s['glossza']))
    print('glossza tartalmaz /:', sum(1 for s in fordit if '/' in s['glossza']))
    print('glossza tartalmaz ,:', sum(1 for s in fordit if ',' in s['glossza']))
    print('glossza tobb szavas (>2 szo):', sum(1 for s in fordit if len(s['glossza'].split()) > 2))
    return alapok


def tahot_gyakorisag():
    cnt = Counter()
    with open(TAHOT, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.split('\t')
            if len(m) > 1:
                for h in re.findall(r'H\d{4}', m[1]):
                    cnt[h] += 1
    return cnt


def m0_proba(fajl):
    """A 30 szavas proba markdown-tablaja a kapuk eredmenyevel. fajl: entry_id TAB hu TAB [?]"""
    al = defaultdict(list)
    for s in tbesh_sorok():
        al[s['alap']].append(s)
    sor_id = {s['entry_id']: s for v in al.values() for s in v}
    fo = {fo_jelolt(v)['entry_id'] for v in al.values()}
    print('| entry_id | fo | kapcsolat | glossza_en | glossza_hu | ? | kapu |')
    print('|---|---|---|---|---|---|---|')
    db = hiba = 0
    with open(fajl, encoding='utf-8') as f:
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if len(m) < 2 or not m[0]:
                continue
            s = sor_id[m[0]]
            h = kapuk(s, m[1])
            db += 1
            hiba += bool(h)
            print('| %s | %s | %s | %s | %s | %s | %s |' % (
                m[0], 'fo' if m[0] in fo else '', s['kapcsolat'] or '-', s['glossza'], m[1],
                m[2] if len(m) > 2 else '', 'OK' if not h else '; '.join(h)))
    print('\nsorok: %d, kapuhiba: %d' % (db, hiba))


if __name__ == '__main__':
    if '--m0-proba' in sys.argv:
        m0_proba(sys.argv[sys.argv.index('--m0-proba') + 1])
    elif '--m0' in sys.argv:
        m0()
        g = tahot_gyakorisag()
        print('TAHOT Strong-kulcs, ossz. elofordulas (hogyan Strong-szam, 4 jegy):', len(g), sum(g.values()))
    else:
        print(__doc__)
