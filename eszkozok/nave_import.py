"""Nave's Topical Bible (1897) import — saját parszoló a basokant/nave NYERS szövegfájlján.

Forrás: basokant/nave, `data/nave.txt` (a nyers, lekaparott szövegfájl), commit
4f35c7d4ffd4933f4db1b9d5182db90dc04bd235. A basokant szkriptjeit (bin/parse.ts,
bin/scrape.ts) és a belőlük készült `data/parsed-nave.json`-t NEM vesszük át:
a JSON csak ellenőrző összevetésre használható (`--json`), az import nem ezen alapul.
Licenc: a mű közkincs (Nave, 1897) a basokant README-je szerint; licencfájl nincs
(l. naplok/F18_licenc.md). A theonize/bible_database-t a DT5 döntés szerint nem használjuk.

Kimenet: konkordancia/Nave_basokant.tsv (egy sor = egy igehely- vagy „lásd”-hivatkozás).
Séma és szerkezet: konkordancia/Nave_basokant_README.md.

Használat:
    python eszkozok/nave_import.py --forras <nave.txt> [--json <parsed-nave.json>] [--kimenet <tsv>]
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import collections
import hashlib
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONK = os.path.join(REPO_ROOT, "konkordancia")
NORM_TABLA = os.path.join(KONK, "Konyv_normalizalo_tabla.tsv")
VERSMEGF = os.path.join(KONK, "Karoli_versmegfeleltetes.tsv")
ALAP_KIMENET = os.path.join(KONK, "Nave_basokant.tsv")

BASOKANT_COMMIT = "4f35c7d4ffd4933f4db1b9d5182db90dc04bd235"

# OSIS-könyvkód (ahogy a nave.txt használja) -> STEPBible-rövidítés
OSIS_STEP = {
    "Gen": "Gen", "Exod": "Exo", "Lev": "Lev", "Num": "Num", "Deut": "Deu",
    "Josh": "Jos", "Judg": "Jdg", "Ruth": "Rut", "1Sam": "1Sa", "2Sam": "2Sa",
    "1Kgs": "1Ki", "2Kgs": "2Ki", "1Chr": "1Ch", "2Chr": "2Ch", "Ezra": "Ezr",
    "Neh": "Neh", "Esth": "Est", "Job": "Job", "Ps": "Psa", "Prov": "Pro",
    "Eccl": "Ecc", "Song": "Sng", "Isa": "Isa", "Jer": "Jer", "Lam": "Lam",
    "Ezek": "Ezk", "Dan": "Dan", "Hos": "Hos", "Joel": "Jol", "Amos": "Amo",
    "Obad": "Oba", "Jonah": "Jon", "Mic": "Mic", "Nah": "Nam", "Hab": "Hab",
    "Zeph": "Zep", "Hag": "Hag", "Zech": "Zec", "Mal": "Mal",
    "Matt": "Mat", "Mark": "Mrk", "Luke": "Luk", "John": "Jhn", "Acts": "Act",
    "Rom": "Rom", "1Cor": "1Co", "2Cor": "2Co", "Gal": "Gal", "Eph": "Eph",
    "Phil": "Php", "Col": "Col", "1Thess": "1Th", "2Thess": "2Th",
    "1Tim": "1Ti", "2Tim": "2Ti", "Titus": "Tit", "Phlm": "Phm", "Heb": "Heb",
    "Jas": "Jas", "1Pet": "1Pe", "2Pet": "2Pe", "1John": "1Jn", "2John": "2Jn",
    "3John": "3Jn", "Jude": "Jud", "Rev": "Rev",
}

UJSZ = {"Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph",
        "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb",
        "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"}

OSIS_RE = re.compile(
    r'^([0-9A-Za-z]+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z]+)\.(\d+)(?:\.(\d+))?)?$')
# a kijelzett szöveg szabályos alakja: [könyvrövidítés] szám[:szám] ... ; ettől eltérő = gyanús
DISP_RE = re.compile(r'^(?:\d?\s?[A-Za-z]{1,6}\.?\s+)?[\d:,\-–; ]+$')
REF_RE = re.compile(r'<ref (osisRef|target)="([^"]*)">(.*?)</ref>', re.S)
TAG_RE = re.compile(r'<[^>]+>')
EGYFEJEZETES = {"Obad", "Phlm", "2John", "3John", "Jude"}
EGYFEJ_RE = re.compile(r'^[0-9A-Za-z]+\.1\.1$')
# a <ref> UTÁN közvetlenül (szóköz nélkül) álló hivatkozás-töredék: a lekaparás a névvel összeolvadt
# kijelzésben ("Micah 2" + "Ch 34:20" = valójában 2Ch 34:20) a könyvnév számjegyét a kijelzett névhez
# ragasztotta, a betűs rész a </ref> után maradt
TOREDEK_RE = re.compile(r'(?:Ch|Ki|Sa|Ti|Co|Th|Pe|Jn)\s*\d+[\d:,\-–; ]*')
TOREDEK_KONYV = {"Ch", "Ki", "Sa", "Ti", "Co", "Th", "Pe", "Jn"}
# a <ref> után közvetlenül álló versszám-lista: ":7", ":8-13", ":9,10", ":4-6, 8"
VERSSZAM_RE = re.compile(r'\s*:\s*(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)')

FEJLEC = ["tema_id", "tema", "sor", "sor_jel", "tetel", "cimke", "kapcsolat",
          "igehely", "igehely_osis", "hely_tipus", "karoli_allapot",
          "igehely_karoli", "cel_tema", "megjegyzes"]


def tisztit(s):
    return re.sub(r'\s+', ' ', TAG_RE.sub('', s)).strip()


def beolvas_normtabla():
    """STEP-rövidítés -> magyar rövidítés (split('\\t'), nincs csv)."""
    hu = {}
    with open(NORM_TABLA, encoding='utf-8') as f:
        next(f)
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if len(m) >= 2 and m[0]:
                hu[m[0]] = m[1]
    return hu


def beolvas_versmegf():
    """(magyar könyv, KJV fejezet:vers) -> [igehely_karoli, ...]"""
    idx = collections.defaultdict(list)
    with open(VERSMEGF, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#') or sor.startswith('igehely_karoli'):
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) < 4:
                continue
            konyv = m[0].rsplit(' ', 1)[0]
            if not m[1]:
                # nincs KJV-megfelelő (pl. MT-only vers): külön kulcs, hogy a Nave-sor státusza megkülönböztethető legyen
                if m[2]:
                    idx[(konyv, 'MT:' + m[2])].append(m[0])
                continue
            idx[(konyv, m[1])].append(m[0])
    return idx


def igehely_alak(osis, hu, vm):
    """osisRef -> (igehely, hely_tipus, karoli_allapot, igehely_karoli, megjegyzes)"""
    m = OSIS_RE.match(osis)
    if not m:
        return osis, 'hibas', 'n.a.', '', 'osisRef_nem_ertelmezheto'
    k1, c1, v1, k2, c2, v2 = m.groups()
    if k1 not in OSIS_STEP:
        return osis, 'ismeretlen_konyv', 'n.a.', '', 'konyv_nincs_a_normalizalo_tablaban:' + k1
    hu1 = hu[OSIS_STEP[k1]]
    megj = ''
    if k2 is None:
        if v1 is None:
            return "%s %s" % (hu1, c1), 'fejezet', 'fejezet', '', megj
        ig = "%s %s:%s" % (hu1, c1, v1)
        kulcs = (hu1, "%s:%s" % (c1, v1))
        if k1 in UJSZ:
            return ig, 'vers', 'ujszovetseg_nincs_tabla', '', megj
        t = vm.get(kulcs, [])
        if not t:
            if vm.get((hu1, 'MT:%s:%s' % (c1, v1))):
                # a Károli-tábla ismeri ezt a c:v számot, de csak MT-számozásként, KJV-megfelelő nélkül
                return ig, 'vers', 'a_tablaban_nincs_kjv_megfelelo', '', megj
            return ig, 'vers', 'nincs_a_tablaban', '', megj
        if len(t) == 1 and t[0] == ig:
            return ig, 'vers', 'azonos', '', megj
        if len(t) == 1:
            return ig, 'vers', 'eltero', t[0], megj
        return ig, 'vers', 'tobbes', ';'.join(t), megj
    if k2 not in OSIS_STEP:
        return osis, 'ismeretlen_konyv', 'n.a.', '', 'konyv_nincs_a_normalizalo_tablaban:' + k2
    if k2 != k1:
        hu2 = hu[OSIS_STEP[k2]]
        a = "%s %s%s" % (hu1, c1, (':' + v1) if v1 else '')
        b = "%s %s%s" % (hu2, c2, (':' + v2) if v2 else '')
        return a + ' - ' + b, 'konyvhatar_tartomany', 'tartomany', '', megj
    if v1 is None and v2 is None:
        if c1 == c2:
            return "%s %s" % (hu1, c1), 'fejezet', 'fejezet', '', megj
        return "%s %s-%s" % (hu1, c1, c2), 'fejezettartomany', 'tartomany', '', megj
    if v1 is not None and v2 is not None:
        if c1 == c2:
            if v1 == v2:
                return igehely_alak("%s.%s.%s" % (k1, c1, v1), hu, vm)
            return "%s %s:%s-%s" % (hu1, c1, v1, v2), 'tartomany', 'tartomany', '', megj
        return "%s %s:%s-%s:%s" % (hu1, c1, v1, c2, v2), 'tartomany', 'tartomany', '', megj
    # vegyes: az egyik vég fejezet, a másik vers
    a = "%s%s" % (c1, (':' + v1) if v1 else '')
    b = "%s%s" % (c2, (':' + v2) if v2 else '')
    return "%s %s-%s" % (hu1, a, b), 'tartomany', 'tartomany', '', 'vegyes_veg(fejezet/vers)'


def javaslat_hely(kij, ertek, toredek, hu):
    """Az összeolvadt kijelzés + töredék alapján rekonstruált hely (csak javaslat), vagy ''.
    Feltétel: a kijelzés számjegyre végződik, ez egyezik az osisRef fejezetszámával, és
    szám+töredék-betűk = létező könyvrövidítés (pl. 2+Ch = 2Ch). A töredék teljes hely-listája
    megmarad (kezdő és záró vers, vesszős/pontosvesszős lista), nem csonkolódik az első versre
    (F18.12)."""
    mk = re.search(r'(\d+)$', kij)
    mo = OSIS_RE.match(ertek)
    tm = re.match(r'([A-Za-z]+)\s*(\d[\d:,\-–; ]*)', toredek)
    if not (mk and mo and tm):
        return ''
    # ismert könyvnél az osisRef fejezetszáma egyezzen a kijelzés számjegyével; az ismeretlen
    # (lekaparás-hibás) osisRef-nél (PrAzar.1.2, Wis.2) ez nem követelhető meg
    if mo.group(1) in OSIS_STEP and mo.group(2) != mk.group(1):
        return ''
    step = mk.group(1) + tm.group(1)
    if step not in hu:
        return ''
    hely = re.sub(r'\s+', ' ', tm.group(2).replace('–', '-')).strip(' ;,')
    return "%s %s" % (hu[step], hely)


def bontas_egysegek(sor):
    """Egy sor -> [(tetel_nsz, szoveg)]: tetel 0 = a sor feje, 1..n = <item>-ek.
    Visszaad egy hibalistát is, ha <list> mellett bármi más szöveg áll."""
    egysegek = []
    hibak = []
    pos = 0
    n = 0
    fej_reszek = []
    for m in re.finditer(r'<list>(.*?)</list>', sor, re.S):
        fej_reszek.append(sor[pos:m.start()])
        bel = m.group(1)
        maradek = re.sub(r'<item>.*?</item>', '', bel, flags=re.S)
        if maradek.strip():
            hibak.append('list_kozti_szoveg:' + maradek.strip()[:40])
        for it in re.findall(r'<item>(.*?)</item>', bel, re.S):
            n += 1
            egysegek.append((n, it))
        pos = m.end()
    fej_reszek.append(sor[pos:])
    fej = ' '.join(r for r in fej_reszek if r.strip())
    return [(0, fej)] + egysegek, hibak


def parszol(szoveg):
    """nave.txt -> entry-k listája: (cím, törzs)"""
    darabok = szoveg.split('$$$')[1:]
    ent = []
    for d in darabok:
        cim, _, rest = d.partition('\n')
        m = re.search(r'<def>(.*)</def>', rest, re.S)
        if not m:
            raise ValueError('hiányzó <def>: ' + cim)
        ent.append((cim.strip(), m.group(1)))
    return ent


def gyanus_jeloles(megj, kij, ertek, toredek, hu):
    """Hibás kijelzés jelölése (a megj listába); True, ha a hivatkozás megbízhatatlan."""
    if DISP_RE.match(kij) and not toredek:
        return False
    megj.append('gyanus_kijelzes:' + kij)
    if toredek:
        megj.append('toredek:' + toredek)
        j = javaslat_hely(kij, ertek, toredek, hu)
        if j:
            megj.append('javaslat:' + j)
    return True


# --- F18.12: önálló <ref>-es töredék, ref nélküli hivatkozások, „with N:N” folytatás -------------

# a Nave-rövidítések (a forrás kijelzett alakjai) -> OSIS-könyv; a `Co` szándékosan hiányzik
# (1Co/2Co előtag nélkül nem egyértelmű, a lekaparás `Col`-ra képezte), és a hosszú névalakok
# (Micah, Titus …) sem tartoznak ide: az összeolvadt nevek külön osztály
NAVE_ROV = {
    "Ge": "Gen", "Ex": "Exod", "Le": "Lev", "Nu": "Num", "De": "Deut", "Jos": "Josh",
    "Jud": "Judg", "Ru": "Ruth", "1Sa": "1Sam", "2Sa": "2Sam", "1Ki": "1Kgs", "2Ki": "2Kgs",
    "1Ch": "1Chr", "2Ch": "2Chr", "Ezr": "Ezra", "Ne": "Neh", "Es": "Esth", "Job": "Job",
    "Ps": "Ps", "Pr": "Prov", "Ec": "Eccl", "So": "Song", "Isa": "Isa", "Jer": "Jer",
    "La": "Lam", "Eze": "Ezek", "Da": "Dan", "Ho": "Hos", "Joe": "Joel", "Am": "Amos",
    "Ob": "Obad", "Jon": "Jonah", "Mic": "Mic", "Na": "Nah", "Hab": "Hab", "Zep": "Zeph",
    "Hag": "Hag", "Zec": "Zech", "Mal": "Mal", "Mt": "Matt", "Mr": "Mark", "Lu": "Luke",
    "Joh": "John", "Ac": "Acts", "Ro": "Rom", "1Co": "1Cor", "2Co": "2Cor", "Ga": "Gal",
    "Eph": "Eph", "Php": "Phil", "Col": "Col", "1Th": "1Thess", "2Th": "2Thess",
    "1Ti": "1Tim", "2Ti": "2Tim", "Tit": "Titus", "Phm": "Phlm", "Heb": "Heb", "Jas": "Jas",
    "1Pe": "1Pet", "2Pe": "2Pet", "1Jo": "1John", "2Jo": "2John", "3Jo": "3John",
    "Jude": "Jude", "Re": "Rev",
}
STEP_OSIS = {v: k for k, v in OSIS_STEP.items()}
# római számos név után, <ref> nélkül álló hivatkozás: "Ben-hadad I 1Ki 20", "Herod Agrippa II Ac 26:2,3"
ROMAN_RE = re.compile(
    r'\b(?:I{1,3}|IV|VI{0,3}|IX|X)\s+((?:[123]\s?)?[A-Z][a-z]{1,3})\s+(\d+[\d:,\-–; ]*)')
# „with N:N” folytató-hivatkozás: az előző hivatkozás könyvét örökli
WITH_RE = re.compile(r'\bwith\s+(\d+:\d+[\d:,\-–; ]*)')
SPEC_ELSO_RE = re.compile(r'(\d+)(?::(\d+))?(?:-(?:(\d+):)?(\d+))?$')
SPEC_TOVABBI_RE = re.compile(r'(\d+)(?:-(\d+))?$')


def spec_osisok(konyv, spec):
    """Nave-hivatkozás-lista ("25:13-27; 26", "13:3-5,13,14") -> [osis, ...] (egy elem = egy sor),
    vagy None, ha nem értelmezhető. A Nave-szokás: pontosvessző után fejezet[:vers], vessző után
    vers (ha a csoport c:v-vel kezdődött) vagy fejezet."""
    out = []
    for csoport in spec.replace('–', '-').split(';'):
        elso = True
        versmod = False
        cur = None
        for p in csoport.split(','):
            p = re.sub(r'\s+', '', p)
            if not p:
                continue
            if elso or ':' in p:
                m = SPEC_ELSO_RE.match(p)
                if not m:
                    return None
                c, v, c2, e = m.groups()
                if v is None:
                    versmod = False
                    if e is None:
                        out.append("%s.%s" % (konyv, c))
                    elif c2 is None:
                        out.append("%s.%s-%s.%s" % (konyv, c, konyv, e))
                    else:
                        return None
                else:
                    versmod = True
                    cur = c
                    if e is None:
                        out.append("%s.%s.%s" % (konyv, c, v))
                    elif c2 is None:
                        out.append("%s.%s.%s-%s.%s.%s" % (konyv, c, v, konyv, c, e))
                    else:
                        out.append("%s.%s.%s-%s.%s.%s" % (konyv, c, v, konyv, c2, e))
                elso = False
            else:
                m = SPEC_TOVABBI_RE.match(p)
                if not m:
                    return None
                a, b = m.groups()
                if versmod:
                    if b is None:
                        out.append("%s.%s.%s" % (konyv, cur, a))
                    else:
                        out.append("%s.%s.%s-%s.%s.%s" % (konyv, cur, a, konyv, cur, b))
                else:
                    if b is None:
                        out.append("%s.%s" % (konyv, a))
                    else:
                        out.append("%s.%s-%s.%s" % (konyv, a, konyv, b))
    return out or None


def extra_talalatok(szoveg):
    """A <ref> nélküli hivatkozások a szövegben: [(kezdet, veg, fajta, konyv_osis|None, spec)]."""
    t = []
    for m in WITH_RE.finditer(szoveg):
        t.append((m.start(), m.end(), 'with', None, m.group(1)))
    for m in ROMAN_RE.finditer(szoveg):
        abbr = m.group(1).replace(' ', '')
        if abbr in NAVE_ROV:
            t.append((m.start(1), m.end(), 'roman', NAVE_ROV[abbr], m.group(2)))
    t.sort()
    ki = []
    veg = -1
    for x in t:
        if x[0] >= veg:
            ki.append(x)
            veg = x[1]
    return ki


def javaslat_konyv(megj, hu):
    """A megjegyzés-lista `javaslat:<könyv> <hely>` eleméből a javasolt könyv OSIS-kódja, vagy None."""
    for x in megj:
        if x.startswith('javaslat:'):
            nev = x[len('javaslat:'):].rsplit(' ', 1)[0]
            for step, h in hu.items():
                if h == nev:
                    return STEP_OSIS.get(step)
    return None


def konyv_osis(osis):
    """A hivatkozás (utolsó) könyve OSIS-ben, vagy None."""
    m = OSIS_RE.match(osis)
    if not m:
        return None
    return m.group(4) or m.group(1)


def extrak(szoveg, cimke, last_book, alap, hu, vm, stat):
    """A szöveg (hézag / utótag / hivatkozás nélküli egység) feldolgozása: a <ref> nélküli
    hivatkozásokból sor lesz. Visszaad: (maradék szövegrészek, sorok, cimke, last_book).
    Extra nélkül a maradék az egész szöveg (kerettel levágva), a cimke ezzel frissül — az F18.11
    viselkedés."""
    sorok = []
    maradek = []
    pos = 0
    for (a, b, fajta, konyv, spec) in extra_talalatok(szoveg):
        pre = szoveg[pos:a].strip(' ;,')
        if pre:
            cimke = pre
            maradek.append(pre)
        pos = b
        raw = szoveg[a:b].strip(' ;,')
        biztos = True
        if fajta == 'with':
            if last_book is None:
                sorok.append(alap + [raw, 'szoveg', '', '', '', '', '', '',
                                     'gyanus_kijelzes:with_folytato_nincs_elozo_konyv'])
                stat['with_arva'] += 1
                continue
            konyv, biztos, jb = last_book
            megj0 = ['with_folytato:' + raw, 'konyv_oroklve:' + konyv]
        else:
            megj0 = ['ref_nelkuli_hivatkozas:' + raw]
        osisok = spec_osisok(konyv, spec) if konyv in OSIS_STEP else None
        if osisok is None:
            sorok.append(alap + [raw, 'szoveg', '', '', '', '', '', '',
                                 'gyanus_kijelzes:%s_nem_ertelmezheto' % fajta])
            stat[fajta + '_nem_ertelmezheto'] += 1
            continue
        for o in osisok:
            ig, ht, ka, ikar, m2 = igehely_alak(o, hu, vm)
            megj = list(megj0)
            if not biztos:
                megj.append('gyanus_kijelzes:with_folytato_bizonytalan_konyv')
                if jb:
                    # az előző hivatkozás összeolvadt töredékéből rekonstruált könyv: csak javaslat
                    oj = spec_osisok(jb, spec)
                    if oj and len(oj) == len(osisok):
                        megj.append('javaslat:' + igehely_alak(oj[osisok.index(o)], hu, vm)[0])
                ka = 'nem_ertekelt'
                stat['with_bizonytalan'] += 1
            if m2:
                megj.append(m2)
            sorok.append(alap + [cimke, 'vers', ig, o, ht, ka, ikar, '', ';'.join(megj)])
            stat[fajta + '_sor'] += 1
            stat['hely_tipus:' + ht] += 1
            stat['karoli:' + ka] += 1
        if fajta == 'roman':
            last_book = (konyv, True, None)
    tail = szoveg[pos:].strip(' ;,')
    if tail:
        cimke = tail
        maradek.append(tail)
    return maradek, sorok, cimke, last_book


def onallo_toredek(refs, e, hu):
    """Önálló <ref>-es töredék: `<ref osisRef="Titus.2">Titus 2</ref><ref osisRef="Col.8.16">Co 8:16</ref>`
    (valójában „By Titus 2Co 8:16”). Az A ref kijelzése számjegyre végződik, közvetlenül utána B ref
    kijelzése `Ch|Ki|Sa|Ti|Co|Th|Pe|Jn` + szám, és szám+betűk létező könyv (2+Co = 2Co).
    Egyértelmű (javítható), ha: A osisRef-fejezete = a kijelzés számjegye; B osisRef c[:v] = a
    kijelzett c[:v]. Ekkor B és a rá következő, betű nélküli kijelzésű, azonos (téves) könyvű
    láncelemek könyve a helyes könyvre íródik át. Különben A, B és a lánc csak jelölt.
    Visszaad: (javitas {ref_index: (uj_osis, eredeti_osis)}, toredek_a {ref_index: B_kijelzes},
    bizonytalan {ref_index, ...})."""
    javitas = {}
    toredek_a = {}
    bizonytalan = set()
    for i in range(len(refs) - 1):
        A, B = refs[i], refs[i + 1]
        if A.group(1) != 'osisRef' or B.group(1) != 'osisRef':
            continue
        if e[A.end():B.start()].strip():
            continue
        kij_a, kij_b = tisztit(A.group(3)), tisztit(B.group(3))
        ma = re.search(r'(\d+)$', kij_a)
        mb = re.match(r'([A-Za-z]+)\s*(\d+)(?::(\d+))?', kij_b)
        if not (ma and mb and mb.group(1) in TOREDEK_KONYV):
            continue
        oa, ob = OSIS_RE.match(A.group(2)), OSIS_RE.match(B.group(2))
        step = ma.group(1) + mb.group(1)
        egyertelmu = (step in hu and step in STEP_OSIS and oa is not None and ob is not None
                      and (oa.group(1) not in OSIS_STEP or oa.group(2) == ma.group(1))
                      and ob.group(2) == mb.group(2)
                      and (mb.group(3) is None or ob.group(3) == mb.group(3)))
        regi = ob.group(1) if ob else None
        lanc = [i + 1]
        j = i + 2
        while j < len(refs):
            if not re.fullmatch(r'[\s,;]*', e[refs[j - 1].end():refs[j].start()]):
                break
            r = refs[j]
            oj = OSIS_RE.match(r.group(2))
            if (r.group(1) == 'osisRef' and oj and oj.group(1) == regi
                    and re.fullmatch(r'[\d:,\-–; ]+', tisztit(r.group(3)))):
                lanc.append(j)
                j += 1
            else:
                break
        if egyertelmu:
            uj = STEP_OSIS[step]
            for k in lanc:
                o = refs[k].group(2)
                javitas[k] = ('-'.join(uj + p[len(regi):] if p.startswith(regi + '.') else p
                                       for p in o.split('-')), o)
            toredek_a[i] = kij_b
        else:
            bizonytalan.update([i] + lanc)
    return javitas, toredek_a, bizonytalan


def sorok_generalas(entk, hu, vm):
    kimenet = []
    stat = collections.Counter()
    for ei, (cim, torzs) in enumerate(entk, 1):
        tema_id = "NAVE-%04d" % ei
        sorszam = 0
        last_book = None  # (OSIS-könyv, megbízható) — a „with N:N” folytatás az entry előző hivatkozásának könyvét örökli
        for nyers in torzs.split('\n'):
            if not nyers.strip():
                continue
            sorszam += 1
            s = nyers.strip()
            if s.startswith('→'):
                jel, s = '→', s[1:]
            else:
                mm = re.match(r'(\d+)\.\s', s)
                if mm:
                    jel, s = 'szam:' + mm.group(1), s[mm.end():]
                else:
                    jel = 'folyt'
            egysegek, hibak = bontas_egysegek(s)
            for h in hibak:
                stat['bontasi_figyelmeztetes'] += 1
            for tetel, e in egysegek:
                cimke = ''
                pos = 0
                alap = [tema_id, cim, str(sorszam), jel, str(tetel)]
                refs = list(REF_RE.finditer(e))
                if not refs and tisztit(e):
                    # hivatkozás nélküli egység: római számos név után álló hivatkozás sorrá lesz,
                    # a többi szöveg megmarad (cimke), sor nélkül nem volna nyoma
                    szoveg_e = tisztit(e)
                    maradek, xs, _, last_book = extrak(szoveg_e, '', last_book, alap, hu, vm, stat)
                    if xs:
                        kimenet.extend(xs)
                        stat['szoveg_hivatkozas_nelkul_felbontva'] += 1
                        tail = szoveg_e[extra_talalatok(szoveg_e)[-1][1]:].strip(' ;,')
                        if tail:
                            kimenet.append(alap + [tail, 'szoveg', '', '', '', '', '', '', 'nincs_hivatkozas'])
                            stat['szoveg_hivatkozas_nelkul'] += 1
                    else:
                        kimenet.append(alap + [szoveg_e, 'szoveg', '', '', '', '', '', '', 'nincs_hivatkozas'])
                        stat['szoveg_hivatkozas_nelkul'] += 1
                    continue
                javitas, toredek_a, bizonytalan = onallo_toredek(refs, e, hu)
                for i, r in enumerate(refs):
                    gap = tisztit(e[pos:r.start()])
                    _, xs, cimke, last_book = extrak(gap, cimke, last_book, alap, hu, vm, stat)
                    kimenet.extend(xs)
                    pos = r.end()
                    tipus, ertek, kij = r.group(1), r.group(2), tisztit(r.group(3))
                    megj = []
                    if i in javitas:
                        # önálló <ref>-es töredék (egyértelmű): a könyv javítva, a karoli_allapot újraszámítva
                        ertek_eredeti = ertek
                        ertek = javitas[i][0]
                        megj.append('javitva:eredeti_osis=' + ertek_eredeti)
                        stat['onallo_toredek_javitva'] += 1
                    # egyfejezetes könyvek: a valódi versszám a <ref> UTÁN áll (":7", ":8-13", ":9,10"),
                    # az osisRef csak "X.1.1" (alapérték) — a versszámot innen vesszük
                    egyfej = (tipus == 'osisRef' and EGYFEJ_RE.match(ertek) is not None
                              and ertek.split('.')[0] in EGYFEJEZETES)
                    vers_spec = ''
                    if egyfej:
                        vm_ = VERSSZAM_RE.match(e[pos:])
                        if vm_:
                            vers_spec = re.sub(r'\s+', '', vm_.group(1)).replace('–', '-')
                            pos += vm_.end()
                    toredek = ''
                    if tipus == 'osisRef':
                        tm_ = TOREDEK_RE.match(e[pos:])
                        if tm_:
                            toredek = tm_.group(0).strip(' ;,')
                            pos += tm_.end()
                        elif i in toredek_a:
                            toredek = toredek_a[i]
                    utotag = ''
                    xs_ut = []
                    utolso = (i == len(refs) - 1)

                    def utotag_feldolg(last_book_uj, cimke_):
                        if not utolso:
                            return '', [], last_book_uj, cimke_
                        mar, xs_, cimke_uj, lb = extrak(tisztit(e[pos:]), cimke_, last_book_uj,
                                                        alap, hu, vm, stat)
                        return ' '.join(mar), xs_, lb, cimke_  # a sor saját cimkéje nem változik

                    if tipus == 'osisRef':
                        if vers_spec:
                            konyv = ertek.split('.')[0]
                            osisok = []
                            for seg in vers_spec.split(','):
                                if not seg:
                                    continue
                                if '-' in seg:
                                    a_, b_ = seg.split('-', 1)
                                    osisok.append("%s.1.%s-%s.1.%s" % (konyv, a_, konyv, b_))
                                else:
                                    osisok.append("%s.1.%s" % (konyv, seg))
                            stat['egyfejezetes_ref_javitva'] += 1
                            megj.append('eredeti_osis:' + ertek)
                            gyanus = gyanus_jeloles(megj, kij, ertek, toredek, hu)
                            if i in bizonytalan:
                                megj.append('gyanus_kijelzes:onallo_toredek_nem_egyertelmu')
                                gyanus = True
                            last_book = (konyv, not gyanus, None)
                            utotag, xs_ut, last_book, cimke = utotag_feldolg(last_book, cimke)
                            if utotag:
                                megj.append('utotag:' + utotag)
                            megj.append('egyfejezetes_versszam_a_ref_utan:' + vers_spec)
                            for osis_ in osisok:
                                ig, ht, ka, ikar, m2 = igehely_alak(osis_, hu, vm)
                                if gyanus:
                                    ka = 'nem_ertekelt'
                                mj = list(megj) + ([m2] if m2 else [])
                                kimenet.append(alap + [cimke, 'vers', ig, osis_, ht, ka, ikar, '', ';'.join(mj)])
                                stat['vers'] += 1
                                stat['hely_tipus:' + ht] += 1
                                stat['karoli:' + ka] += 1
                            kimenet.extend(xs_ut)
                            continue
                        ig, ht, ka, ikar, m2 = igehely_alak(ertek, hu, vm)
                        if m2:
                            megj.append(m2)
                        gyanus = gyanus_jeloles(megj, kij, ertek, toredek, hu)
                        if egyfej:
                            # egyfejezetes könyv, de a ref után nincs versszám: az X 1:1 alapérték nem megbízható
                            megj.append('gyanus_kijelzes:egyfejezetes_nincs_versszam')
                            gyanus = True
                            stat['egyfejezetes_versszam_nelkul'] += 1
                        if i in bizonytalan:
                            megj.append('gyanus_kijelzes:onallo_toredek_nem_egyertelmu')
                            gyanus = True
                            stat['onallo_toredek_bizonytalan'] += 1
                        if gyanus:
                            ka = 'nem_ertekelt'
                        kb = konyv_osis(ertek)
                        last_book = (kb, (not gyanus) and kb in OSIS_STEP, javaslat_konyv(megj, hu)) if kb else last_book
                        utotag, xs_ut, last_book, cimke = utotag_feldolg(last_book, cimke)
                        if utotag:
                            megj.append('utotag:' + utotag)
                        kimenet.append(alap + [cimke, 'vers', ig, ertek, ht, ka, ikar, '', ';'.join(megj)])
                        stat['vers'] += 1
                        stat['hely_tipus:' + ht] += 1
                        stat['karoli:' + ka] += 1
                        kimenet.extend(xs_ut)
                    else:
                        cel = ertek[5:] if ertek.startswith('Nave:') else ertek
                        if not ertek.startswith('Nave:'):
                            megj.append('target_nem_Nave')
                        if kij != cel:
                            megj.append('kijelzett:' + kij)
                        utotag, xs_ut, last_book, cimke = utotag_feldolg(last_book, cimke)
                        if utotag:
                            megj.append('utotag:' + utotag)
                        kimenet.append(alap + [cimke, 'lasd', '', '', '', '', '', cel, ';'.join(megj)])
                        stat['lasd'] += 1
                        kimenet.extend(xs_ut)
    return kimenet, stat


def ir(ut, fejlec_sorok, kimenet):
    sorok = ['\t'.join(FEJLEC)] + ['\t'.join(r) for r in kimenet]
    for r in kimenet:
        assert len(r) == len(FEJLEC), r
        for mezo in r:
            assert '\t' not in mezo and '\n' not in mezo, r
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for h in fejlec_sorok:
            f.write(h + '\n')
        f.write('\n'.join(sorok) + '\n')


def json_osszevetes(ut, entk, kimenet):
    """Csak ellenőrzés: a basokant JSON-ja (nem importforrás) és a saját parszolás mennyiségei."""
    with open(ut, encoding='utf-8') as f:
        adat = json.load(f)

    def bej(n):
        v = len(n.get('verses', []))
        r = len(n.get('relatedTopics', []))
        for s in n.get('subtopics', []):
            a, b = bej(s)
            v += a
            r += b
        return v, r
    jv = jr = 0
    for t in adat:
        a, b = bej(t)
        jv += a
        jr += b
    sv = sum(1 for r in kimenet if r[6] == 'vers')
    sl = sum(1 for r in kimenet if r[6] == 'lasd')
    return {'json_tema': len(adat), 'json_vers': jv, 'json_rel': jr,
            'sajat_tema': len(entk), 'sajat_vers': sv, 'sajat_lasd': sl}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--forras', required=True, help='a basokant/nave data/nave.txt fájlja')
    ap.add_argument('--json', help='opcionális: data/parsed-nave.json, csak összevetéshez')
    ap.add_argument('--kimenet', default=ALAP_KIMENET)
    a = ap.parse_args()
    with open(a.forras, 'rb') as f:
        nyers = f.read()
    sha = hashlib.sha256(nyers).hexdigest()
    szoveg = nyers.decode('utf-8')
    entk = parszol(szoveg)
    hu = beolvas_normtabla()
    vm = beolvas_versmegf()
    kimenet, stat = sorok_generalas(entk, hu, vm)
    fejlec = [
        "# GENERÁLT: eszkozok/nave_import.py — kézzel nem szerkesztendő.",
        "# forras: basokant/nave @ %s | data/nave.txt sha256=%s | saját parszoló (a basokant szkriptjei nincsenek átvéve)" % (BASOKANT_COMMIT, sha),
        "# licenc: Nave's Topical Bible (1897), közkincs a basokant README szerint; licencfájl nincs (naplok/F18_licenc.md)",
        "# proveniencia: scope=teljes-Nave | forras=basokant/nave@%s data/nave.txt | ts=2026-09-30" % BASOKANT_COMMIT[:7],
        "# versszámozás: a Nave-hivatkozás KJV-számozású, magyar könyvrövidítéssel (Konyv_normalizalo_tabla.tsv); igehely_karoli: Karoli_versmegfeleltetes.tsv szerint, csak egyes versekre",
    ]
    ir(a.kimenet, fejlec, kimenet)
    uniq = len(set(c for c, _ in entk))
    gy_sor = sum(1 for r in kimenet if 'gyanus_kijelzes:' in r[13])
    gy_tag = sum(r[13].count('gyanus_kijelzes:') for r in kimenet)
    print('gyanus_sor:', gy_sor, 'gyanus_tag (elofordulas):', gy_tag,
          'javaslat_sor:', sum(1 for r in kimenet if 'javaslat:' in r[13]),
          'toredek_sor:', sum(1 for r in kimenet if 'toredek:' in r[13]))
    print('entry:', len(entk), 'egyedi cim:', uniq, 'sor:', len(kimenet))
    for k, v in sorted(stat.items()):
        print(' ', k, v)
    if a.json:
        print('json-osszevetes:', json_osszevetes(a.json, entk, kimenet))


if __name__ == '__main__':
    main()
