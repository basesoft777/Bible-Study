#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/glossza_forditas.py -- F140 GLOSSZA_FORDITAS: a TBESH rovid glosszajanak
(7. oszlop) magyar forditasa a heber Strong-szamokra.

M0: a meres es a sor-valasztas (--m0). M1 (DT-F140b K7 (a)): a session forditja a kotegeket,
a szkript kotegeket keszit (--koteg), rogzit (--rogzit) es ellenoriz (--ellenoriz); nincs
modellhivas a szkriptben. M2 utan: --javit <atnezes.tsv> -- a felhasznalo altal jovahagyott javitasok
naplozott alkalmazasa (allapot=kezi; naplok/GLOSSZA_FORDITAS_javit_naplo.tsv). A tabla: adat/glosszak_heber_hu.tsv (SEMA 2.39).

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

TB = None
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

# K5 (DT-F140b): a TAHOT "Rovid jelentes"-e a 11 istenneves Strongnal "LORD"-ot hordoz (#138
# targya), ezert itt a K5-lista dont a fo sorrol; ahol a Strongnak tobb sora van, az entry_id-t
# a lista nevezi meg (H5945B 'Felseges', H6635B 'Seregek'); egysoros alapnal az egyetlen sor.
K5_FO = {'H3068': 'H3068G', 'H0430': 'H0430G', 'H0136': 'H0136', 'H0410': 'H0410K',
         'H5945': 'H5945B', 'H3050': 'H3050', 'H7706': 'H7706', 'H6635': 'H6635B',
         'H5943': 'H5943', 'H5946': 'H5946', 'H1180': 'H1180'}


def tahot_norm(glossza):
    """TAHOT 'Rovid jelentes' / TBESH-glossza osszevetesi alakja: a kettespont elotti resz,
    kisbetusen, az alahuzas szokozzel (a TAHOT 'House_of_the_Forest' alakja)."""
    return glossza.split(':')[0].replace('_', ' ').strip().lower()


def tahot_tobbseg():
    """Strongonkenti tobbsegi TAHOT 'Rovid jelentes' (normalizalt). A fo-jelolt kivalasztasaban
    szamit csak; szoveg nem kerul at (DT-F140b K2)."""
    szaml = defaultdict(Counter)
    with open(TAHOT, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) > 5 and re.match(r'^H\d{4}$', m[1]):
                szaml[m[1]][tahot_norm(m[5])] += 1
    return {h: c.most_common(1)[0][0] for h, c in szaml.items()}


def fo_heurisztika(sorok_alap):
    """A 2.2 heurisztika (M0): az elso kapcsolat nelkuli sor, amelynek glosszaja nem zarojeles
    es definicioja nem nevtoredek; ha nincs, az elso kapcsolat nelkuli; ha az sincs, a valaszt()
    fallbackja. Csak tartalek: a K2-szabaly (fo_jelolt) elobb a TAHOT-tobbseget nezi."""
    tiszta = [s for s in sorok_alap if s['kapcsolat'] == '' and '(' not in s['glossza']
              and not NEVTOREDEK.search(s['definicio'][:80])]
    if tiszta:
        return tiszta[0]
    fo = [s for s in sorok_alap if s['kapcsolat'] == '']
    if fo:
        return fo[0]
    return valaszt(sorok_alap)[0][0]


def fo_jelolt(sorok_alap, tobbseg=None):
    """Strongonkenti kiemelt (fo) sor (DT-F140b K2, K5).
    1. K5-lista (istennevek): a lista entry_id-je;
    2. K2: az a sor, amelynek glosszaja (kettespont elotti resz, kisbetusen) egyezik a TAHOT
       Strongonkenti tobbsegi 'Rovid jelentes'-evel (tobbseg: tahot_tobbseg() eredmenye);
       tobb egyezo sornal a kapcsolat nelkuli, kettospont nelkuli sor az elso;
    3. egyebkent (nincs TAHOT-adat / nem illeszthetö) a 2.2 heurisztika."""
    alap = sorok_alap[0]['alap']
    if alap in K5_FO:
        for s in sorok_alap:
            if s['entry_id'] == K5_FO[alap]:
                return s
    if tobbseg and alap in tobbseg:
        egyezo = [s for s in sorok_alap if tahot_norm(s['glossza']) == tobbseg[alap]]
        if egyezo:
            # tobb egyezo sor: a kapcsolat nelkuli, kettospont nelkuli (a pontos glossza),
            # nem zarojeles, nem nevtoredek elonyben; egyenlo rangnal a fajlsorrend
            return min(enumerate(egyezo), key=lambda p: (
                p[1]['kapcsolat'] != '', ':' in p[1]['glossza'], '(' in p[1]['glossza'],
                bool(NEVTOREDEK.search(p[1]['definicio'][:80])), p[0]))[1]
    return fo_heurisztika(sorok_alap)


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
5. Istennevek (projekt-konvenció; az „az ÚR” nem Károli-alak): `LORD`/YHWH (H3068) → „az ÚR”;
   `God` (H0430, H0410G) → „Isten”; `Lord` (H0136) → „Úr”; `god` (H0410K) → „isten”;
   `Most High` (H5945B, H5943, H5946) → „Felséges”; `Almighty` (H7706) → „Mindenható”;
   `Hosts` (H6635B) → „Seregek”; Jah (H3050) → „Jah”; `Baal` (H1180) → „Baáli” `?`-lel.
   Összetételben ugyanígy: `(LORD)` → „(az ÚR)”, `(God)` → „(Isten)”. Ne írj „Jehova”-t, ha a glossza nem.
6. Jelölők: `[Obj.]`, `(f.s.)`, `+` és hasonló szögletes/zárójeles jelölők jelentése megmarad
   magyarul (pl. „[tárgyjel]”); kettősponttal bővített glossza („land: country”) → „föld: ország”.
7. Nincs benne héber vagy görög betű, angol szó, idézőjel, magyarázat, kérdőjel. Ha a glosszában
   kettőspont van („house: home”), a magyarban is megmarad („ház: otthon”).
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


KONTEXTUS_HOSSZ_ARNYALAT = 90


def kontextus_hossz(s):
    """Az arnyalat-soroknal (kapcsolat = 'a Meaning of', gloss tipikusan 'house: palace') a
    definicio eleje a szulo-szocikk szovegenek ismetlese; az arnyalat-cimke az elso karakterekben
    all, ezert 90 karakter elég (token-takarekossag). ELTERES a brief ~200 karakteres irányatol:
    az M2 zarojelentesben rogzitendo. A kapcsolat nelkuli es a homonima (a/b, pl. H2763A/B) sorokat
    a definicio valasztja szet, ezert azoknal 200 marad (DT-F140 tanacs, 2026-10-25).
    A 17. koteg ELOTT a szabaly a ':' jelre epult (':' in glossza), ami 20 homonima- es 72
    kapcsolat nelkuli sort is 90-re vitt; l. naplok/GLOSSZA_FORDITAS_homonima_szuroproba.tsv."""
    return KONTEXTUS_HOSSZ_ARNYALAT if s['kapcsolat'] == 'a Meaning of' else KONTEXTUS_HOSSZ


def prompt_epit(sorok):
    """Egy kotegre: a glosszakban/definicio-elejeken elofordulo terminologiai kulcsok
    + a kotegbemenet. Nincs modellhivas."""
    szoveg = ' '.join(s['glossza'] + ' ' + s['definicio'][:KONTEXTUS_HOSSZ] for s in sorok).lower()
    term = terminologia_sorok()
    talalt = ['%s -> %s' % (k, v) for k, v in term.items() if k.lower() in szoveg and len(k) > 3]
    bemenet = '\n'.join('%s | %s | %s | %s | %s | %s' % (
        s['entry_id'], s['lemma'], s['atiras'], s['szofaj'], s['glossza'],
        re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s['definicio']))[:kontextus_hossz(s)]) for s in sorok)
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
    if ':' in sor['glossza'] and ':' not in hu:
        hibak.append('kettospont elveszett (K3)')
    return hibak


def m0():
    global TB
    TB = tahot_tobbseg()
    sorok = tbesh_sorok()
    alapok = defaultdict(list)
    for s in sorok:
        alapok[s['alap']].append(s)
    szot = szotar_strongok()
    kulso = sorted(set(alapok) - set(szot))
    print('TBESH-ban van, szotar-ban nincs (a hatokorbol kimarad):', kulso)
    alapok = defaultdict(list, {a: v for a, v in alapok.items() if a in set(szot)})
    sorok = [s for s in sorok if s['alap'] in alapok]
    print('hatokor (8718 Strong): sor', len(sorok), '; fo-jelolt (Strongonkent 1):', len({fo_jelolt(v, TB)['entry_id'] for v in alapok.values()}))
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
    tb = tahot_tobbseg()
    fo = {fo_jelolt(v, tb)['entry_id'] for v in al.values()}
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


# ---------------------------------------------------------------- M1: tabla, koteg, rogzites
TABLA = os.path.join(GYOKER, 'adat', 'glosszak_heber_hu.tsv')
ELAKAD = os.path.join(GYOKER, 'naplok', 'GLOSSZA_FORDITAS_elakad.tsv')
FEJLEC = ['strong', 'entry_id', 'kapcsolat', 'fo', 'glossza_en', 'forras_hash', 'glossza_hu',
          'allapot', 'modell', 'datum', 'megjegyzes']
KOTEG_MERET = 100

# K5 (DT-F140b): az istennevek fix forditasa entry_id szerint; a szkript irja be (nem a modell).
ISTENNEV_FIX = {
    'H3068G': ('az ÚR', ''), 'H0430G': ('Isten', ''), 'H0136': ('Úr', ''), 'H0410K': ('isten', ''),
    'H0410G': ('Isten', ''), 'H5945B': ('Felséges', ''), 'H3050': ('Jah', ''),
    'H7706': ('Mindenható', ''), 'H6635B': ('Seregek', ''), 'H5943': ('Felséges', ''),
    'H5946': ('Felséges', ''), 'H1180': ('Baáli', '?'),
}


def hatokor():
    """A 8718 heber Strong TBESH-sorai (a H9015-H9019 elemek kimaradnak): (alapok, sorok)."""
    szot = set(szotar_strongok())
    alapok = defaultdict(list)
    for s in tbesh_sorok():
        if s['alap'] in szot:
            alapok[s['alap']].append(s)
    return alapok, [s for v in alapok.values() for s in v]


def tabla_olvas():
    sorok = {}
    if not os.path.exists(TABLA):
        return sorok
    with open(TABLA, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            if i == 0:
                assert sor.rstrip('\n').split('\t') == FEJLEC, 'fejlec elter'
                continue
            m = sor.rstrip('\n').split('\t')
            assert len(m) == len(FEJLEC), 'oszlopszam: ' + sor[:40]
            sorok[m[1]] = dict(zip(FEJLEC, m))
    return sorok


def tabla_ir(sorok, engedett=()):
    """Teljes ujrairas entry_id szerint rendezve; az irás elott a meglevo sorok valtozatlansaganak
    ellenorzese (CLAUDE.md: tablat iro szkript az eredetivel veti ossze; eltereskor megall).
    engedett: a naplozott javito mod (--javit) altal modosithato entry_id-k."""
    regi = tabla_olvas()
    for k, v in regi.items():
        if k not in engedett and sorok.get(k) != v:
            raise SystemExit('MEGALL: a meglevo sor valtozna: ' + k)
    with open(TABLA, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(FEJLEC) + '\n')
        for k in sorted(sorok):
            f.write('\t'.join(sorok[k][c] for c in FEJLEC) + '\n')


def uj_sor(s, fo_ids, hu, allapot, modell, datum, megj):
    return {'strong': s['alap'], 'entry_id': s['entry_id'], 'kapcsolat': s['kapcsolat'],
            'fo': 'igen' if s['entry_id'] in fo_ids else '', 'glossza_en': s['glossza'],
            'forras_hash': sha1(s['glossza']), 'glossza_hu': hu, 'allapot': allapot,
            'modell': modell, 'datum': datum, 'megjegyzes': megj}


def fo_idk(alapok):
    tb = tahot_tobbseg()
    return {fo_jelolt(v, tb)['entry_id'] for v in alapok.values()}


def fuggo_parok(sorok, kesz):
    """A (glossza, szofaj) parok, amelyeknek van meg forditatlan sora; gyakorisag szerint
    csokkeno sorrendben (a TAHOT-elofordulas), igy a reszleges futas is a legfontosabbat adja.
    Visszaad: lista [(rep_sor, [forditatlan sorok])]."""
    gy = tahot_gyakorisag()
    csoport = defaultdict(list)
    for s in sorok:
        if s['entry_id'] in ISTENNEV_FIX:
            continue
        csoport[(s['glossza'], s['szofaj'])].append(s)
    ki = []
    for kulcs, v in csoport.items():
        hianyzo = [s for s in v if s['entry_id'] not in kesz]
        if not hianyzo:
            continue
        rep = max(v, key=lambda s: (gy.get(s['alap'], 0), s['kapcsolat'] == '', s['entry_id']))
        ki.append((rep, hianyzo))
    ki.sort(key=lambda p: (-gy.get(p[0]['alap'], 0), p[0]['entry_id']))
    return ki


def parancs_fix(modell):
    alapok, sorok = hatokor()
    tabla = tabla_olvas()
    fo = fo_idk(alapok)
    datum = ido()
    uj = dict(tabla)
    for s in sorok:
        if s['entry_id'] in ISTENNEV_FIX and s['entry_id'] not in tabla:
            hu, megj = ISTENNEV_FIX[s['entry_id']]
            uj[s['entry_id']] = uj_sor(s, fo, hu, 'sonnet', modell, datum, megj)
    tabla_ir(uj)
    print('fix istennev-sorok:', len(uj) - len(tabla), '; tabla:', len(uj))


def ido():
    import datetime
    return datetime.date.today().isoformat()


def parancs_koteg(meret, kimenet):
    alapok, sorok = hatokor()
    kesz = tabla_olvas()
    par = fuggo_parok(sorok, kesz)
    if not par:
        print('NINCS fuggo par: minden sor forditva')
        return
    mai = par[:meret]
    bemenet_sorok = [rep for rep, _ in mai]
    szoveg = prompt_epit(bemenet_sorok)
    if '--csak-bemenet' in sys.argv:
        # folytato kotegeknel a szabalyok mar a kontextusban vannak: csak a terminologia + bemenet
        term = szoveg.split('8. Terminológia', 1)[1].split('\n', 1)[0]
        szoveg = '8. Terminológia' + term + '\n\n' + szoveg.split('definíció eleje):\n', 1)[1]
    with open(kimenet, 'w', encoding='utf-8') as f:
        f.write(szoveg)
    print('fuggo par: %d (sor: %d); a koteg: %d par, %d sor; prompt: %s' % (
        len(par), sum(len(h) for _, h in par), len(mai), sum(len(h) for _, h in mai), kimenet))


def parancs_rogzit(valasz, modell, masodik):
    alapok, sorok = hatokor()
    kesz = tabla_olvas()
    par = {rep['entry_id']: (rep, h) for rep, h in fuggo_parok(sorok, kesz)}
    fo = fo_idk(alapok)
    datum = ido()
    uj = dict(kesz)
    hibas = []
    n_par = n_sor = 0
    with open(valasz, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor.strip():
                continue
            # a valasz sora: TAB-bal vagy ' | '-pel tagolt (a session ' | '-pel irja)
            m = sor.split('\t') if '\t' in sor else sor.split(' | ')
            m[0] = m[0].strip()
            if m[0] not in par:
                raise SystemExit('ISMERETLEN/MAR KESZ azonosito a valaszban: ' + m[0])
            hu = m[1].strip() if len(m) > 1 else ''
            bizonytalan = len(m) > 2 and m[2].strip() == '?'
            rep, hianyzo = par.pop(m[0])
            h = kapuk(rep, hu)
            if h:
                hibas.append((rep, hu, h))
                continue
            n_par += 1
            for s in hianyzo:
                uj[s['entry_id']] = uj_sor(s, fo, hu, 'sonnet', modell, datum,
                                           '?' if bizonytalan else '')
                n_sor += 1
    tabla_ir(uj)
    print('rogzitve: %d par, %d sor; tabla: %d sor' % (n_par, n_sor, len(uj)))
    print('a valaszbol hianyzo (nem kapott forditast): %d par' % len(par))
    for rep, hu, h in hibas:
        print('KAPUHIBA\t%s\t%s\t%s\t%s' % (rep['entry_id'], rep['glossza'], hu, '; '.join(h)))
    if masodik and hibas:
        uj_fejlec = not os.path.exists(ELAKAD)
        with open(ELAKAD, 'a', encoding='utf-8', newline='\n') as f:
            if uj_fejlec:
                f.write('entry_id\tglossza_en\tutolso_hu\thiba\tdatum\n')
            for rep, hu, h in hibas:
                f.write('%s\t%s\t%s\t%s\t%s\n' % (rep['entry_id'], rep['glossza'], hu, '; '.join(h), datum))
        print('masodik bukas: %d par az elakado-listaba kerult' % len(hibas))


def parancs_ellenoriz():
    alapok, sorok = hatokor()
    tabla = tabla_olvas()
    tbesh = {s['entry_id']: s for s in sorok}
    hibak = []
    for k, r in tabla.items():
        s = tbesh.get(k)
        if s is None:
            hibak.append((k, 'nincs TBESH-sor'))
            continue
        if r['glossza_en'] != s['glossza'] or r['forras_hash'] != sha1(s['glossza']):
            hibak.append((k, 'forras_hash/glossza_en eltér'))
        if r['strong'] != s['alap'] or r['kapcsolat'] != s['kapcsolat']:
            hibak.append((k, 'strong/kapcsolat eltér'))
        h = kapuk(s, r['glossza_hu'])
        if h:
            hibak.append((k, '; '.join(h)))
        if r['megjegyzes'] not in ('', '?') :
            hibak.append((k, 'megjegyzes ismeretlen'))
        if not r['modell'] or r['allapot'] not in ('sonnet', 'kezi'):
            hibak.append((k, 'modell/allapot'))
    fo = fo_idk(alapok)
    for k, r in tabla.items():
        if (r['fo'] == 'igen') != (k in fo):
            hibak.append((k, 'fo eltér a szabálytól'))
    for h in hibak[:50]:
        print('HIBA\t%s\t%s' % h)
    ures_fo = [a for a in alapok if any(x['entry_id'] in tabla for x in alapok[a])
               and not any(tabla[x['entry_id']]['fo'] == 'igen' for x in alapok[a] if x['entry_id'] in tabla)]
    print('sor: %d / %d ; strong (legalabb egy sorral): %d / %d ; hiba: %d ; bizonytalan (?): %d ; fo nélküli, részben kész strong: %d' % (
        len(tabla), len(sorok), len({r['strong'] for r in tabla.values()}), len(alapok), len(hibak),
        sum(1 for r in tabla.values() if r['megjegyzes'] == '?'), len(ures_fo)))
    return len(hibak)


def javit_alkalmaz(atnezes_sorok, tabla, tbesh, datum):
    """A felhasznalo altal jovahagyott javitasok (naplok/GLOSSZA_FORDITAS_atnezes.tsv, 'javitas_hu'
    oszlop). Szabaly: ures vagy '=' -> a fordítás marad; ha a megjegyzes '?', a '?' torlodik es a
    sor 'kezi' lesz; mas ertek -> kapuk, majd allapot='kezi', megjegyzes ures, datum frissul,
    a modell mezo valtozatlan (a forditot rogziti; a javitast a felhasznalo hagyta jova). '=?' -> a
    szoveg marad, a '?' beallitva (naplo: '? beallitva'; allapot 'kezi'; DT-F140c).
    Visszaad: (uj_tabla, naplo_sorok, hibak, engedett_idk)."""
    uj = {k: dict(v) for k, v in tabla.items()}
    naplo, hibak, engedett = [], [], set()
    for k, jav in atnezes_sorok:
        if k not in uj:
            hibak.append((k, 'nincs ilyen sor a tablaban'))
            continue
        jav = jav.strip()
        r = uj[k]
        if jav == '=?':
            if r['megjegyzes'] != '?':
                naplo.append((k, r['glossza_hu'], r['glossza_hu'], datum, '? beallitva'))
                r.update({'megjegyzes': '?', 'allapot': 'kezi', 'datum': datum})
                engedett.add(k)
            continue
        if jav in ('', '='):
            if jav == '=' and r['megjegyzes'] == '?':
                naplo.append((k, r['glossza_hu'], r['glossza_hu'], datum, '? torolve'))
                r.update({'megjegyzes': '', 'allapot': 'kezi', 'datum': datum})
                engedett.add(k)
            continue
        h = kapuk(tbesh[k], jav)
        if h:
            hibak.append((k, '; '.join(h)))
            continue
        naplo.append((k, r['glossza_hu'], jav, datum, 'javitas'))
        r.update({'glossza_hu': jav, 'allapot': 'kezi', 'megjegyzes': '', 'datum': datum})
        engedett.add(k)
    return uj, naplo, hibak, engedett


def parancs_javit(fajl):
    alapok, sorok = hatokor()
    tabla = tabla_olvas()
    tbesh = {s['entry_id']: s for s in sorok}
    atn = []
    with open(fajl, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) >= 10:
                atn.append((m[2], m[9]))
    datum = ido()
    uj, naplo, hibak, engedett = javit_alkalmaz(atn, tabla, tbesh, datum)
    for h in hibak:
        print('JAVITAS-HIBA\t%s\t%s' % h)
    if hibak:
        raise SystemExit('MEGALL: a javitasok nem mentek at a kapukon; a tabla nem valtozott')
    tabla_ir(uj, engedett)
    naplo_fajl = os.path.join(GYOKER, 'naplok', 'GLOSSZA_FORDITAS_javit_naplo.tsv')
    uj_fejlec = not os.path.exists(naplo_fajl)
    with open(naplo_fajl, 'a', encoding='utf-8', newline='\n') as f:
        if uj_fejlec:
            f.write('entry_id\tregi_hu\tuj_hu\tdatum\tmuvelet\n')
        for n in naplo:
            f.write('\t'.join(n) + '\n')
    print('javitva: %d sor (naplo: %s)' % (len(naplo), naplo_fajl))


def argv_ertek(nev, alap=None):
    if nev in sys.argv:
        return sys.argv[sys.argv.index(nev) + 1]
    return alap


if __name__ == '__main__':
    if '--fix' in sys.argv:
        parancs_fix(argv_ertek('--modell'))
    elif '--koteg' in sys.argv:
        parancs_koteg(int(argv_ertek('--meret', KOTEG_MERET)), argv_ertek('--koteg'))
    elif '--rogzit' in sys.argv:
        if not argv_ertek('--modell'):
            raise SystemExit('--modell kotelezo (a ténylegesen futó modell neve)')
        parancs_rogzit(argv_ertek('--rogzit'), argv_ertek('--modell'), '--masodik' in sys.argv)
    elif '--javit' in sys.argv:
        parancs_javit(argv_ertek('--javit'))
    elif '--ellenoriz' in sys.argv:
        raise SystemExit(1 if parancs_ellenoriz() else 0)
    elif '--m0-proba' in sys.argv:
        m0_proba(sys.argv[sys.argv.index('--m0-proba') + 1])
    elif '--m0' in sys.argv:
        m0()
        g = tahot_gyakorisag()
        print('TAHOT Strong-kulcs, ossz. elofordulas (hogyan Strong-szam, 4 jegy):', len(g), sum(g.values()))
    else:
        print(__doc__)
