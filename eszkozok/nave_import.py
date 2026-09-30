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
            if len(m) < 4 or not m[1]:
                continue
            konyv = m[0].rsplit(' ', 1)[0]
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


def sorok_generalas(entk, hu, vm):
    kimenet = []
    stat = collections.Counter()
    for ei, (cim, torzs) in enumerate(entk, 1):
        tema_id = "NAVE-%04d" % ei
        sorszam = 0
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
                refs = list(REF_RE.finditer(e))
                if not refs and tisztit(e):
                    # hivatkozás nélküli egység: a szöveg megmarad (cimke), sor nélkül nem volna nyoma
                    kimenet.append([tema_id, cim, str(sorszam), jel, str(tetel),
                                    tisztit(e), 'szoveg', '', '', '', '', '', '', 'nincs_hivatkozas'])
                    stat['szoveg_hivatkozas_nelkul'] += 1
                    continue
                for i, r in enumerate(refs):
                    gap = tisztit(e[pos:r.start()])
                    gap_szoveg = gap.strip(' ;,')
                    if gap_szoveg:
                        cimke = gap_szoveg
                    pos = r.end()
                    tipus, ertek, kij = r.group(1), r.group(2), tisztit(r.group(3))
                    utotag = ''
                    if i == len(refs) - 1:
                        utotag = tisztit(e[pos:]).strip(' ;,')
                    megj = []
                    if tipus == 'osisRef':
                        ig, ht, ka, ikar, m2 = igehely_alak(ertek, hu, vm)
                        if m2:
                            megj.append(m2)
                        if not DISP_RE.match(kij):
                            megj.append('gyanus_kijelzes:' + kij)
                            stat['gyanus_kijelzes'] += 1
                        if utotag:
                            megj.append('utotag:' + utotag)
                        kimenet.append([tema_id, cim, str(sorszam), jel, str(tetel), cimke,
                                        'vers', ig, ertek, ht, ka, ikar, '', ';'.join(megj)])
                        stat['vers'] += 1
                        stat['hely_tipus:' + ht] += 1
                        stat['karoli:' + ka] += 1
                    else:
                        cel = ertek[5:] if ertek.startswith('Nave:') else ertek
                        if not ertek.startswith('Nave:'):
                            megj.append('target_nem_Nave')
                        if kij != cel:
                            megj.append('kijelzett:' + kij)
                        if utotag:
                            megj.append('utotag:' + utotag)
                        kimenet.append([tema_id, cim, str(sorszam), jel, str(tetel), cimke,
                                        'lasd', '', '', '', '', '', cel, ';'.join(megj)])
                        stat['lasd'] += 1
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
    print('entry:', len(entk), 'egyedi cim:', uniq, 'sor:', len(kimenet))
    for k, v in sorted(stat.items()):
        print(' ', k, v)
    if a.json:
        print('json-osszevetes:', json_osszevetes(a.json, entk, kimenet))


if __name__ == '__main__':
    main()
