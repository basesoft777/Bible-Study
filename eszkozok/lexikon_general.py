#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lexikon_general.py — LEXV2_2_BRIEF.md V2.4: a `lexikon/[ID]_TUDOMANYOS.md`
lexikon-oldal v2 generátora.

A render-logika külön modulban (D13): a `general.py` a betöltést és a
CLI-t adja, ez a modul a tíz generált blokk tartalmát építi fel az
`adat/` táblákból és a `konkordancia/` kivonatokból, a `lekerdez.py` és
az `ubs_hozzarendeles.py` betöltőin/logikáján keresztül (import, nem
másolás).

Vegyes fájl (D1): a tíz blokk `general.py --cel lexikon` alatt frissül;
a blokkokon kívüli (kézi) szakaszokat a `blokk_beilleszt` érintetlenül
hagyja. Új célfájlnál a teljes váz íródik (fejléc+Kivonat + mind a 13
szakasz).

TSV-olvasás kizárólag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import io
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import general as G
import lekerdez as L
import tsk_kulcs as TK
import ubs_hozzarendeles as UBS
import lxx_os_import as LXXOS
import kiejtes as KJ
import utvonalak as _U

ROOT = G.ROOT
ADAT = G.ADAT
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')

RES_FORRAS_TSV = os.path.join(ADAT, 'res_forras.tsv')
LEXIKON_HIVATKOZASOK_TSV = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
OSHL_TSV = os.path.join(KONKORDANCIA, 'OSHL_lexikalis_index.tsv')
KAPCSOLATOK_TSV = os.path.join(ADAT, 'kapcsolatok.tsv')
JELOLTEK_TSV = os.path.join(ADAT, 'jeloltek.tsv')
FORDITASOK_TSV = os.path.join(ADAT, 'forditasok.tsv')
LXX_DONTESEK_TSV = os.path.join(ADAT, 'lxx_dontesek.tsv')
STRONG_SZOTAR_TSV = os.path.join(KONKORDANCIA, 'Strong_szotar.tsv')
TBESG_TXT = os.path.join(KONKORDANCIA, 'TBESG.txt')
TBESH_TXT = _U.TBESH_TXT
LXX_OS_DIR = os.path.join(KONKORDANCIA, 'LXX_OS')

STRONG_TOKEN_RE = re.compile(r'^[HG]\d{4}[A-Za-z]?$')
EM_DASH = '—'

# --- Licencek (F42 / DT-F42g, N9) ------------------------------------------
# A licenc-állapot és a megjelenő rövid címke EGYETLEN forrása az
# adat/licencek.tsv (SEMA 2.19). A kódban nincs licenc-konstans; ha egy kulcsnak
# nincs sora (vagy üres a `cimke` mezője), a generátor hibával áll meg --
# alapértelmezett érték nincs. Olvasás: split('\t'), nem csv (CLAUDE.md).

LICENCEK_TSV = os.path.join(ADAT, 'licencek.tsv')
_licencek_cache = None


def licencek():
    """adat/licencek.tsv -> {dataset: sor-dict}."""
    global _licencek_cache
    if _licencek_cache is None:
        sorok = []
        with io.open(LICENCEK_TSV, encoding='utf-8') as f:
            for sor in f:
                sor = sor.rstrip('\r\n')
                if sor and not sor.startswith('#'):
                    sorok.append(sor.split('\t'))
        fejlec = sorok[0]
        for kotelezo in ('dataset', 'allapot', 'cimke'):
            if kotelezo not in fejlec:
                raise SystemExit('HIBA: az adat/licencek.tsv fejlécéből hiányzik a `%s` oszlop' % kotelezo)
        d = {}
        for s in sorok[1:]:
            if len(s) != len(fejlec):
                raise SystemExit('HIBA: adat/licencek.tsv, a `%s` sor oszlopszáma %d, a fejlécé %d'
                                 % (s[0], len(s), len(fejlec)))
            r = dict(zip(fejlec, s))
            d[r['dataset']] = r
        _licencek_cache = d
    return _licencek_cache


def licenc_sor(dataset):
    r = licencek().get(dataset)
    if r is None:
        raise SystemExit('HIBA: nincs `%s` sor az adat/licencek.tsv-ben (a licencjelölés egyetlen '
                         'forrása; alapértelmezett érték nincs)' % dataset)
    if not r.get('cimke'):
        raise SystemExit('HIBA: üres `cimke` az adat/licencek.tsv `%s` során' % dataset)
    return r


def LC(dataset):
    """A dataset rövid licenc-címkéje az adat/licencek.tsv-ből."""
    return licenc_sor(dataset)['cimke']


def licenc_tisztazatlan(dataset):
    """`tisztazott` és `kozkincs`: nincs tisztázatlan-jelölés; `tisztazatlan`: van."""
    return licenc_sor(dataset)['allapot'] == 'tisztazatlan'


MOUNCE_MEGJELOLES = (
    'Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights '
    'Reserved, www.teknia.com/greek-dictionary'
)


def lsj_forrasmegjeloles():
    return ('LSJ forrás: Liddell-Scott-Jones, Perseus Digital Library (`lexica` '
            'repó), %s.' % LC('LSJ'))


def _sorted_unique(seq):
    return sorted(set(seq))


def igehely_rendez(igehelyek, konyv_sorrend, hianyzo_konyvek):
    return sorted(igehelyek, key=lambda ige: G.igehely_rendezo_kulcs(ige, konyv_sorrend, hianyzo_konyvek))


def karoli_colon(s):
    """'Péld 8,22' -> 'Péld 8:22'; '1Móz 2,4-5' -> '1Móz 2:4-5' (G8/K5:
    a TSK/Károli-KH magyar-megjelenítése vesszős, a generált oldal nem
    lehet az)."""
    return re.sub(r'(\d+),(\d+)', r'\1:\2', s, count=1)


def igehely_lista(igehely):
    """Egyetlen igehely -> [igehely] vagy egy tartomány minden verse,
    a `Karoli_1908.tsv` kulcsai + `L.parse_range`/`L.in_range` szerint."""
    if '-' not in igehely:
        return [igehely]
    try:
        rng = L.parse_range(igehely)
    except ValueError:
        return [igehely]
    if rng[0] == 'verse':
        return [igehely]
    karoli_terkep = L.load_karoli_1908()
    talalatok = []
    for kulcs in karoli_terkep:
        try:
            konyv, fej, vers = L.parse_igehely(kulcs)
        except ValueError:
            continue
        if L.in_range(rng, konyv, fej, vers):
            talalatok.append((fej, vers, kulcs))
    if not talalatok:
        return [igehely]
    talalatok.sort()
    return [t[2] for t in talalatok]


# ---------------------------------------------------------------------------
# Segéd: motívum Strong-tokenjei
# ---------------------------------------------------------------------------

def motivum_strong_tokenek(sorai):
    tokenek = set()
    for sor in sorai:
        for darab in (sor.get('strong') or '').split('+'):
            darab = darab.strip()
            if STRONG_TOKEN_RE.match(darab):
                tokenek.add(darab)
    return sorted(tokenek)


# ---------------------------------------------------------------------------
# Kiejtés-segédek (G6)
# ---------------------------------------------------------------------------

_tahot_idx_cache = None
_tagnt_idx_cache = None
_strong_szotar_cache = None

GOROG_ATIRAS = {
    'a': 'a', 'b': 'b', 'g': 'g', 'd': 'd', 'e': 'e', 'z': 'z', 'h': 'ē',
    'q': 'th', 'i': 'i', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'x': 'x',
    'o': 'o', 'p': 'p', 'r': 'r', 's': 's', 't': 't', 'u': 'y', 'f': 'ph',
    'c': 'ch', 'y': 'ps', 'w': 'ō',
}
_GOROG_BETU = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'ē',
    'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x',
    'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'y',
    'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'ō',
}


def gepi_atiras(gorog_szo):
    """Determinisztikus, SBL-közelítő gépi átírás — csak akkor, ha sem a
    TAHOT/TAGNT, sem a Strong_szotar.tsv nem ad kiejtést (G6)."""
    alap = LXXOS.strip_accents(gorog_szo)
    return ''.join(_GOROG_BETU.get(ch, ch) for ch in alap)


def tahot_index():
    global _tahot_idx_cache
    if _tahot_idx_cache is None:
        idx = {}
        for r in L.load_tahot():
            idx[(r['Igehely'], r['Strong-szám'])] = r
        _tahot_idx_cache = idx
    return _tahot_idx_cache


def tagnt_index():
    global _tagnt_idx_cache
    if _tagnt_idx_cache is None:
        idx = {}
        for r in L.load_tagnt():
            idx[(r['Igehely'], r['Strong-szám'])] = r
        _tagnt_idx_cache = idx
    return _tagnt_idx_cache


def kiejtes_ehhez(igehely, strong):
    """(ragozott_alak, kiejtes, forras) vagy None — a TAHOT/TAGNT Igehely+
    Strong kulcsával, az igehely-lista első verséig visszaesve tartománynál.
    Ragozott alak kiejtése -- kizárólag a tényleges ragozott alak mellett
    használandó (V2.6a pont 2), nem lemma-fejlécekben."""
    forras_idx = tahot_index() if strong.startswith('H') else tagnt_index()
    for ige in igehely_lista(igehely):
        r = forras_idx.get((ige, strong))
        if r:
            if strong.startswith('G'):
                # F09 S2.1: görög alak -> magyaros kiejtés; a héber alak STEP-átírása változatlan
                return r['Ragozott alak'], gorog_magyaros(r['Kiejtés']), 'TAGNT'
            return r['Ragozott alak'], r['Kiejtés'], 'TAHOT'
    return None


_tbesg_tbesh_cache = None


def tbesg_tbesh_index():
    """(pontos_kulcs, alap_kulcs) -- strong -> (lemma, kiejtes), a
    TBESG.txt/TBESH.txt 4./5. oszlopából (index 3/4) -- a lemma-szintű
    kiejtés egyetlen forrása (V2.6a pont 2). Az `alap_kulcs` a betűutótag
    nélküli Strong-számra esik vissza (első előfordulás), mert a TBESH egy
    részt sense-onként bont (`H2416a`, `H2416b`, …), a motívum saját
    `strong` mezője viszont a betűutótag nélküli alakot használja."""
    global _tbesg_tbesh_cache
    if _tbesg_tbesh_cache is None:
        pontos = {}
        alap = {}
        alap_re = re.compile(r'^([HG]\d{4})[a-zA-Z]?$')
        for path in (TBESG_TXT, _U.kotelezo(TBESH_TXT)):
            with io.open(path, encoding='utf-8') as f:
                for sor in f:
                    sor = sor.rstrip('\r\n')
                    cols = sor.split('\t')
                    if len(cols) < 5:
                        continue
                    strong = cols[0]
                    if not STRONG_TOKEN_RE.match(strong):
                        continue
                    pontos.setdefault(strong, (cols[3], cols[4]))
                    m = alap_re.match(strong)
                    if m:
                        alap.setdefault(m.group(1), (cols[3], cols[4]))
        _tbesg_tbesh_cache = (pontos, alap)
    return _tbesg_tbesh_cache


_kiejtes_tablak_cache = None


def _kiejtes_tablak():
    """(görög szabályok, görög kivételek, héber kivételek) -- egyszer betöltve
    a kiejtes.py betöltőivel (adat/kiejtes_szabalyok.tsv, adat/kiejtes_kivetelek.tsv)."""
    global _kiejtes_tablak_cache
    if _kiejtes_tablak_cache is None:
        _kiejtes_tablak_cache = (
            KJ.szabalyok_betolt(),
            KJ.kivetelek_betolt(nyelv='gorog'),
            KJ.kivetelek_betolt(nyelv='heber'),
        )
    return _kiejtes_tablak_cache


def gorog_magyaros(sbl_atiras):
    """F09 S2.1 (F05 S3): görög SBL-átírás -> magyaros kiejtés (kiejtes.py:
    szabálytábla + görög kivételek). A héber nem ezen megy át."""
    szabalyok, gorog_kivetelek, _ = _kiejtes_tablak()
    return KJ.atir(sbl_atiras, szabalyok, gorog_kivetelek)


HEBER_NINCS_KIEJTES_JELZO = '*(nincs jóváhagyott kiejtés; a héber lemma-kiejtést a render nem generálja)*'


def heber_lemma_kiejtes(lemma, step_atiras):
    """A jóváhagyott héber lemma-kiejtés az adat/kiejtes_kivetelek.tsv-ből (F05 S3,
    D15): előbb a TBESH-lemma NFC alakja, azután a STEP-átírás a kulcs. Gépi héber
    kiejtés nincs: ha nincs sor, None."""
    _, _, heber = _kiejtes_tablak()
    return heber.get(unicodedata.normalize('NFC', lemma)) or heber.get(step_atiras)


def lemma_kiejtes(strong):
    """(lemma, kiejtes) vagy None, a TBESG/TBESH-ből, Strong-szám szerint
    -- pontos egyezés, majd betűutótag nélküli alapalakra visszaesve.
    F09 S2.1: a kiejtés magyaros -- görögül a kiejtes.py átírása a TBESG-átírásból,
    héberül a jóváhagyott kivétel-sor; ha ilyen nincs, a STEP-átírás és a jelző
    (a render héber kiejtést nem generál)."""
    pontos, alap = tbesg_tbesh_index()
    nyers = pontos.get(strong) or alap.get(strong)
    if not nyers:
        return None
    lemma, step = nyers
    if strong.startswith('G'):
        return lemma, gorog_magyaros(step)
    hu = heber_lemma_kiejtes(lemma, step)
    if hu:
        return lemma, hu
    return lemma, '%s %s' % (step, HEBER_NINCS_KIEJTES_JELZO)


# ---------------------------------------------------------------------------
# Marker-blokk
# ---------------------------------------------------------------------------

def _cel_kulcs(motivum_id, blokk_nev):
    return 'lexikon#%s#%s' % (motivum_id, blokk_nev)


def _lexikon_blokk(motivum_id, blokk_nev, forras_lista, licenc_lista, hatokor_sor, torzs):
    cel_kulcs = _cel_kulcs(motivum_id, blokk_nev)
    fejl = '<!-- GENERÁLT-KEZDET: general.py --cel %s | forrás: %s | licenc: %s | ts=%s -->' % (
        cel_kulcs, ', '.join(forras_lista), ', '.join(licenc_lista), G.TS)
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % cel_kulcs
    return '\n\n'.join([fejl, '*%s*' % hatokor_sor, torzs, veg])


# ---------------------------------------------------------------------------
# Tartalomjegyzék + fejezetcímek (közösen tartva, hogy a TOC és a váz
# horgonyai sose fussanak szét)
# ---------------------------------------------------------------------------

SZAKASZOK = [
    # (cím, generált?)
    ('Kivonat', False),
    ('Jelmagyarázat és rövidítések', True),
    ('1. Előfordulások', True),
    ('1/b. Kizárt és vizsgált helyek', True),
    ('2. Szótári háttér', True),
    ('3. LXX-fordítói döntések', True),
    ('4. Kereszthivatkozások', True),
    ('5. Kapcsolatok', True),
    ('5/b. Kapcsolódó motívumok', True),  # DT-F127b (α) (#127)
    ('6. Értelmezés', False),
    ('6/b. Alkalmazás és tanítói egyezés', False),  # DT-F127a (#127)
    ('7. Módszertan és nyitott kérdések', False),
    ('8. Irodalom és idézés', True),
    ('Kolofon', True),
]

_SLUG_TILTOTT_RE = re.compile(r'[^\w\- ]', re.UNICODE)


def _heading_slug(cim):
    """GitHub-szerű heading-slug közelítés (kisbetű, szóköz -> kötőjel,
    írásjelek eltávolítva; a Tartalomjegyzék és a fejezetcímek ugyanezt a
    függvényt hívják, tehát a horgonyok garantáltan egyeznek)."""
    s = cim.lower()
    s = _SLUG_TILTOTT_RE.sub('', s)
    s = s.strip().replace(' ', '-')
    return s


def blokk_tartalom(m):
    sorok = ['- [%s](#%s)' % (cim, _heading_slug(cim)) for cim, _ in SZAKASZOK]
    hatokor = ('Ez a blokk a lexikon-oldal %d szakaszának tartalomjegyzékét adja (LEXV2_2_BRIEF.md G1).'
               % len(SZAKASZOK))
    torzs = '\n'.join(sorok)
    return _lexikon_blokk(m['id'], 'tartalom', [], [LC('projekt_adat')], hatokor, torzs)


# ---------------------------------------------------------------------------
# Jelmagyarázat és rövidítések (közös szöveg minden oldalon, G10)
# ---------------------------------------------------------------------------

JELMAGYARAZAT_TORZS = """**PaRDeS-szintek** (`sablonok/PaRDeS_gyorsreferencia.md`):
- **Peshat** — a szöveg szerinti, szó szerinti értelem.
- **Remez** — csak felismerés/azonosítás, következtetés nélkül.
- **Drash** — normatív, következtető, alkalmazó.
- **Sod** — fegyelmezett, csak szövegből levezethető, gematria/allegorizálás nélkül.

**Funkció:** a vers szerepe a motívum ívében — az `adat/SEMA.md` szerint
szabad szöveg (nincs zárt értékkészlet), az alábbi táblákban a motívum
saját study-jából átvett megnevezéssel szerepel.

**Rövidítések:** BDB (Brown–Driver–Briggs), TBESH/TBESG (Tyndale Bible
Encyclopedia — Strong's Hebrew/Greek), Thayer (Thayer's Greek Lexicon),
UBS (UBS Dictionary of New Testament Greek — Louw–Nida szemantikai
doménekkel), L–N (Louw–Nida doménkód), SDBH/SDGNT (Semantic Dictionary
of Biblical Hebrew/Greek), OSHL (Open Scriptures Hebrew Lexicon), TWOT
(Theological Wordbook of the Old Testament — csak számhivatkozás), TSK
(Treasury of Scripture Knowledge), KH (Károli-kereszthivatkozás), LXX
(Septuaginta), MT (Masoretic Text), KJV (King James Version).

A szótári fordításokban a πνεῦμα (pneuma) mindig *szellem*, a ψυχή
(pszükhé) *lélek*; a Károli-idézetek szövege változatlan (pl. »Lélek«)."""


def blokk_jelmagyarazat(m):
    hatokor = 'Ez a blokk közös, minden lexikon-oldalon szó szerint azonos szöveg (G10).'
    return _lexikon_blokk(m['id'], 'jelmagyarazat', [], [LC('projekt_adat')], hatokor, JELMAGYARAZAT_TORZS)


# ---------------------------------------------------------------------------
# UBS-jelentés (G3) — az ubs_hozzarendeles.py logikájának újrafelhasználása
# ---------------------------------------------------------------------------

_ubs_ref_idx = None
_ubs_jelentes_idx = None
_ubs_definicio_idx = None
_forditasok_idx = None


def ubs_indexek():
    global _ubs_ref_idx, _ubs_jelentes_idx, _ubs_definicio_idx
    if _ubs_ref_idx is None:
        ref_rows = UBS.read_tsv_rows(UBS.REFERENCIAK_PATH)
        jel_rows = UBS.read_tsv_rows(UBS.JELENTESEK_PATH)
        _ubs_ref_idx = UBS.build_ref_index(ref_rows)
        _ubs_jelentes_idx = UBS.build_jelentes_index(jel_rows)
        definicio_idx = {}
        for r in jel_rows:
            kulcs = (r['strong'], r['lexid'])
            if kulcs not in definicio_idx:
                definicio_idx[kulcs] = r['definicio_rovid']
        _ubs_definicio_idx = definicio_idx
    return _ubs_ref_idx, _ubs_jelentes_idx, _ubs_definicio_idx


def forditasok_index():
    """adat/forditasok.tsv (S1.1): kulcs szotar+strong+entry_id+jelentes_szam+mezo."""
    global _forditasok_idx
    if _forditasok_idx is None:
        rows = L.read_tsv_skip_comments(FORDITASOK_TSV)
        _forditasok_idx = {(r['szotar'], r['strong'], r['entry_id'], r['jelentes_szam'], r['mezo']): r
                            for r in rows}
    return _forditasok_idx


def forditas_ehhez(szotar, strong, entry_id, jelentes_szam, mezo):
    r = forditasok_index().get((szotar, strong, entry_id, jelentes_szam, mezo))
    return r['forditas_hu'] if r else ''


def ubs_glossza_cella(szotar, strong, entry_id, jelentes_szam, angol):
    """F121 (DT-F121g): az „UBS-jelentés” cella egy eleme: a rövid magyar glossza (`glosszak_hu`, a gyorsítótárból;
    ha nincs, az angol + `fordításra vár`) és ⓘ, amely a szónézetre mutat (a teljes UBS-szócikk ott áll)."""
    hu = forditas_ehhez(szotar, strong, entry_id, jelentes_szam, 'glosszak_hu')
    szoveg = _cella(hu) if hu else '%s %s' % (angol, FORDITASRA_VAR)
    return '%s [ⓘ](%s)' % (szoveg, SZONEZET_UT % strong)


def ubs_jelentes_cella(sor_id, igehely, strong_field):
    """G3: L–N kód — magyar definíció (vagy angol + 'fordítás függőben'),
    csak ÚSZ-soroknál. Az UBS.hozzarendel()-t hívja közvetlenül, egyetlen
    elemű bemenettel — nem másolja a logikáját. A cella sosem csupasz
    EM_DASH (P4, ISTENTISZT_V3_POTLAS.md): ÓSZ-sor, G-token nélküli sor és
    hozzárendelés nélküli Strong-token mind jelölve van, és összetett
    (Strong+Strong) token esetén mindkét token szerepel, tokenenként."""
    parsed = UBS.parse_igehely(igehely)
    if parsed is None:
        return '%s *(ÓSZ)*' % EM_DASH
    _konyv, versek = parsed

    strong_tokens = [s for s in (strong_field or '').split('+') if s]
    if not strong_tokens:
        return '%s *(nincs G-token)*' % EM_DASH

    ref_idx, jel_idx, definicio_idx = ubs_indexek()
    out_rows = UBS.hozzarendel([(sor_id, igehely, strong_field, versek)], ref_idx, jel_idx)

    tokenenkent = {}
    for r in out_rows:
        _id, _ige, strong, lexid, entry_kod, glosszak, egyertelmu, _megjegyzes = r
        if not entry_kod:
            continue
        # F121 (DT-F121g): a cellában a kód és a rövid glossza áll, mellette ⓘ a szónézetre (a teljes UBS-szócikk ott)
        szoveg = ubs_glossza_cella('UBS_DNTG', strong, lexid, entry_kod, glosszak)
        jelolt = '' if egyertelmu == 'igen' else ' *(jelölt, nem egyértelmű)*'
        tokenenkent.setdefault(strong, []).append('%s — %s%s' % (entry_kod, szoveg, jelolt))

    if len(strong_tokens) == 1:
        cellak = tokenenkent.get(strong_tokens[0])
        return '; '.join(cellak) if cellak else '%s *(nincs hozzárendelés)*' % EM_DASH

    reszek = []
    for strong in strong_tokens:
        cellak = tokenenkent.get(strong)
        if cellak:
            reszek.append('%s: %s' % (strong, '; '.join(cellak)))
        else:
            reszek.append('%s: *(nincs hozzárendelés)*' % strong)
    return ' · '.join(reszek)


# ---------------------------------------------------------------------------
# 1. Előfordulások + 1/a
# ---------------------------------------------------------------------------

_RAGOZOTT_ZARO_IRASJEL_RE = re.compile(r'[,.;·]+$')


def kulcsszo_cella(sor):
    karoli_szo = sor.get('karoli_szo') or ''
    strong_field = sor.get('strong') or ''
    reszek = []
    for strong in strong_field.split('+'):
        strong = strong.strip()
        if not strong or not STRONG_TOKEN_RE.match(strong):
            continue
        talalat = kiejtes_ehhez(sor['igehely'], strong)
        if talalat:
            ragozott, kiejtes, _forras = talalat
            ragozott = _RAGOZOTT_ZARO_IRASJEL_RE.sub('', ragozott)
            reszek.append('%s (%s)' % (ragozott, kiejtes))
    eredeti = '; '.join(reszek) if reszek else EM_DASH
    if karoli_szo:
        return '%s — %s' % (karoli_szo, eredeti)
    return eredeti


def _anchor_id(igehely):
    alap = re.sub(r'[^0-9A-Za-zÀ-ÿ]+', '-', igehely).strip('-').lower()
    return 'ige-%s' % alap


def blokk_elofordulasok(m, sorai, konyv_sorrend, hianyzo_konyvek):
    sorai_rendezve = sorted(
        sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))

    gerinc = gerinc_aktiv(m['id'])
    if gerinc:
        # F131 (DT272 (d), DT374–e): a szó jelentése és a hely funkciója két szomszédos oszlop
        fejlec = ['| Igehely | Kulcsszó | Jelentés (a szó) | Funkció (a motívumban) | PaRDeS-szint | Strong | UBS-jelentés | Megbízhatóság · azonosítás módja |',
                  '|---|---|---|---|---|---|---|---|']
        g_adat = gerinc_adat()
    else:
        fejlec = ['| Igehely | Kulcsszó | Funkció | PaRDeS-szint | Strong | Szótári jelentés | UBS-jelentés | Megbízhatóság · azonosítás módja |',
                  '|---|---|---|---|---|---|---|---|']
    sorok = list(fejlec)
    labjegyzetek = []
    tetelek_1a = []

    for i, s in enumerate(sorai_rendezve, start=1):
        anchor = _anchor_id(s['igehely'])
        igehely_link = '[%s](#%s)' % (s['igehely'], anchor)

        proveniencia = (s.get('proveniencia') or '').strip()
        igazolas = (s.get('igazolas') or '').strip()
        labjegyzet_jel = ''
        jelentes_ik = ''
        if gerinc:
            jelentes_szo, jelentes_ik = jelentes_cella(g_adat, s)
        if proveniencia or igazolas or jelentes_ik:
            lj = 'proveniencia: %s | igazolas: %s' % (proveniencia or EM_DASH, igazolas or EM_DASH)
            if jelentes_ik:
                lj += ' | jelentés-címke: %s' % jelentes_ik
            labjegyzetek.append(lj)
            labjegyzet_jel = '[^%d]' % len(labjegyzetek)

        if gerinc:
            szotari_jelentes = '%s ⓘ%s' % (jelentes_szo, labjegyzet_jel)
        else:
            szotari_jelentes = lexikon_jelentes_cella(s)
        ubs_cella = ubs_jelentes_cella(s['id'], s['igehely'], s.get('strong') or '')
        if gerinc and ubs_cella.startswith('%s *(ÓSZ)*' % EM_DASH):
            # F131 (DT380): az ÓSZ-sorok UBS-jelentése a DBH-ból
            ubs_cella = dbh_jelentes_cella(s['igehely'], s.get('strong') or '')
        megb = '%s · %s%s' % (s.get('megbizhatosag') or EM_DASH, s.get('azonositas_modja') or EM_DASH,
                               labjegyzet_jel)

        funkcio_teljes = s.get('funkcio') or ''
        funkcio_cimke, _sep, funkcio_magyarazat = funkcio_teljes.partition(' — ')
        funkcio_cella = funkcio_cimke if funkcio_teljes else EM_DASH

        if gerinc:
            sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                igehely_link, kulcsszo_cella(s), _cella(szotari_jelentes), funkcio_cella,
                s.get('pardes_szint') or EM_DASH, s.get('strong') or EM_DASH,
                ubs_cella, megb))
        else:
            sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                igehely_link, kulcsszo_cella(s), funkcio_cella,
                s.get('pardes_szint') or EM_DASH, s.get('strong') or EM_DASH,
                szotari_jelentes, ubs_cella, megb))

        tetelek_1a.append((anchor, s, funkcio_magyarazat if _sep else ''))

    torzs = '\n'.join(sorok)
    if labjegyzetek:
        torzs += '\n\n' + '\n'.join('[^%d]: %s' % (i, lj) for i, lj in enumerate(labjegyzetek, start=1))

    if gerinc:
        torzs += ('\n\n*Az UBS-jelentés az újszövetségi soroknál az UBS Dictionary of New Testament Greek (DNTG), '
                  'az ószövetségi soroknál az UBS Dictionary of Biblical Hebrew (DBH) igehelyszintű jelentése '
                  '(`%s`, a Károli-vers az MT-számozásra képezve, `konkordancia/Karoli_versmegfeleltetes.tsv`); '
                  'tokenenként a hivatkozott jelentés(ek) kódja és rövid glosszája; az ⓘ a szónézetre mutat, ahol a teljes '
                  'UBS-szócikk (definíció és glosszák) áll (DT-F121g). A glossza magyarul a `forditasok.tsv`-ből jön, ahol van; '
                  'ahol nincs, az angol eredeti áll `(fordításra vár)` jelöléssel. Ahol a DBH a versre nem hivatkozik, a cella ezt kimondja.*'
                  % UBS_DBH_REFERENCIAK_FAJL)
    else:
        torzs += ('\n\n*Az UBS-jelentés csak újszövetségi soroknál áll: az UBS Greek New '
                  'Testament Dictionary az Újszövetséget fedi.*')

    torzs += '\n\n#### 1/a. Az igehelyek szövege\n'
    karoli_terkep = L.load_karoli_1908()
    for anchor, s, funkcio_magyarazat in tetelek_1a:
        reszek = ['<a id="%s"></a>' % anchor, '**%s**' % s['igehely']]
        for vers in igehely_lista(s['igehely']):
            szoveg = karoli_terkep.get(vers)
            if szoveg:
                reszek.append('*%s*' % szoveg)
            else:
                reszek.append('*(%s: nincs Károli-szöveg)*' % vers)
        if s.get('kapcsolodas'):
            reszek.append(s['kapcsolodas'])
        if funkcio_magyarazat:
            reszek.append('Funkció: %s' % funkcio_magyarazat)
        torzs += '\n\n' + '\n'.join(reszek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehely-sorát fedi az `elofordulasok.tsv`-ből, '
               'kanonikus sorrendben, a Károli-szöveggel (1/a) és az UBS-jelentés renderidejű '
               'hozzárendelésével (G3).' % (m['id'], len(sorai_rendezve)))
    forras_lista = ['adat/elofordulasok.tsv', 'konkordancia/Karoli_1908.tsv', 'konkordancia/UBS_DNTG_referenciak.tsv',
                    'konkordancia/UBS_DNTG_jelentesek.tsv', 'adat/forditasok.tsv']
    licenc_lista = [LC('projekt_adat'), LC('Karoli_1908'), LC('UBS_DNTG')]
    forras_licenc_parok = [
        ('adat/elofordulasok.tsv', LC('projekt_adat')),
        ('konkordancia/Karoli_1908.tsv', LC('Karoli_1908')),
        ('konkordancia/UBS_DNTG_referenciak.tsv', LC('UBS_DNTG')),
        ('konkordancia/UBS_DNTG_jelentesek.tsv', LC('UBS_DNTG')),
        ('adat/forditasok.tsv', LC('projekt_adat')),
    ]
    if gerinc:
        hatokor += (' A „Jelentés (a szó)” oszlop a szó jelentését a szótár tagolásában adja '
                    '(`%s`, `%s`, `%s`; a címke forrása a sor lábjegyzetében, ⓘ), a „Funkció (a motívumban)” '
                    'a hely motívumbeli funkcióját (F131, DT272 (d)).'
                    % (SZAKASZ_CIMKE_FAJL, BDB_VERS_JELENTES_FAJL, THAYER_VERS_JELENTES_FAJL))
        for fajl, kulcs in ((SZAKASZ_CIMKE_FAJL, 'projekt_adat'), (BDB_VERS_JELENTES_FAJL, 'BDB'),
                            (THAYER_VERS_JELENTES_FAJL, 'Thayer'), (UBS_DBH_REFERENCIAK_FAJL, 'UBS_DBH'),
                            (UBS_DBH_JELENTESEK_FAJL, 'UBS_DBH'),
                            ('konkordancia/Karoli_versmegfeleltetes.tsv', 'Karoli_versmegfeleltetes')):
            forras_lista.append(fajl)
            forras_licenc_parok.append((fajl, LC(kulcs)))
        licenc_lista = _sorted_unique(licenc_lista + [LC('BDB'), LC('Thayer'), LC('UBS_DBH'),
                                                      LC('Karoli_versmegfeleltetes')])
        # F131.27 (DT383 a TAHOT-ra, ELLENOR_SZOTARI_GERINC_3 2.): ha a tábla egy lábjegyzete (ⓘ) a TAHOT-ot
        # forrásként nevezi meg (pl. a Strong kétszeres előfordulása a versben), a TAHOT (CC BY 4.0, STEPBible) az
        # Irodalomban és a kolofon licenctáblájában áll, kötelező megjelöléssel; megnevezés nélkül nincs bejegyzés
        if any(TAHOT_KIVONAT_FAJL in lj for lj in labjegyzetek):
            forras_lista.append(TAHOT_KIVONAT_FAJL)
            forras_licenc_parok.append((TAHOT_KIVONAT_FAJL, LC('TAHOT')))
            licenc_lista = _sorted_unique(licenc_lista + [LC('TAHOT')])
    blokk_szoveg = _lexikon_blokk(m['id'], 'elofordulasok', forras_lista, licenc_lista, hatokor, torzs)
    return blokk_szoveg, forras_licenc_parok


def lexikon_jelentes_cella(sor):
    szotar = sor.get('lexikon_szotar') or ''
    entry_id = sor.get('lexikon_entry_id') or ''
    if not szotar:
        return EM_DASH
    jsz = sor.get('jelentes_szam') or ''
    cella = ('%s %s %s' % (szotar, entry_id, jsz)).strip()
    jelentes_hu = sor.get('jelentes_hu') or ''
    if jelentes_hu:
        cella += ' — %s' % jelentes_hu
    return cella


# ---------------------------------------------------------------------------
# 1/b. Kizárt és vizsgált helyek (G7)
# ---------------------------------------------------------------------------

_jeloltek_cache = None


def jeloltek_sorok():
    global _jeloltek_cache
    if _jeloltek_cache is None:
        _, sorok = G.tsv_beolvas(JELOLTEK_TSV)
        # DT-F127b: az 1/b. blokk és a `minosites` rés csak az előfordulás-
        # jelölteket látja; a motívumközi jelölt nem „kizárt hely”.
        _jeloltek_cache = G.elofordulas_jeloltek(sorok)
    return _jeloltek_cache


def blokk_kizart(m):
    sorok_ehhez = [r for r in jeloltek_sorok() if r['id'] == m['id'] and r.get('dontes') in ('elutasítva', 'nyitva')]

    reszek = []
    if sorok_ehhez:
        for r in sorok_ehhez:
            reszek.append('- **%s** (%s, `%s`): %s' % (
                r['igehely'], r['dontes'], r.get('forras_kereses') or EM_DASH, r.get('indoklas') or EM_DASH))
    else:
        reszek.append('Nincs kizárt vagy nyitva maradt jelölt a `jeloltek.tsv`-ben ehhez a motívumhoz.')

    negativ = (m.get('negativ_kriterium') or '').strip()
    if negativ:
        reszek.append('\n**Negatív kritérium** (`motivumok.tsv`): %s' % negativ)
    torzs = '\n'.join(reszek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d elutasított/nyitva maradt jelöltjét fedi a '
               '`jeloltek.tsv`-ből (G7).' % (m['id'], len(sorok_ehhez)))
    return _lexikon_blokk(m['id'], 'kizart', ['adat/jeloltek.tsv', 'adat/motivumok.tsv'],
                           [LC('projekt_adat')], hatokor, torzs), \
        [('adat/jeloltek.tsv', LC('projekt_adat')), ('adat/motivumok.tsv', LC('projekt_adat'))]


# ---------------------------------------------------------------------------
# 2. Szótári háttér
# ---------------------------------------------------------------------------

_oshl_cache = None
_lexikon_hivatkozasok_cache = None


def oshl_sorok():
    global _oshl_cache
    if _oshl_cache is None:
        _oshl_cache = L.read_tsv_skip_comments(OSHL_TSV)
    return _oshl_cache


def oshl_twot_ehhez(strong):
    return _sorted_unique(r['twot'] for r in oshl_sorok() if r['strong'] == strong and r['twot'] != EM_DASH)


def lexikon_hivatkozasok_sorok():
    global _lexikon_hivatkozasok_cache
    if _lexikon_hivatkozasok_cache is None:
        _lexikon_hivatkozasok_cache = L.read_tsv_skip_comments(LEXIKON_HIVATKOZASOK_TSV)
    return _lexikon_hivatkozasok_cache


def lexikon_hivatkozasok_ehhez(strong):
    sorok = [r for r in lexikon_hivatkozasok_sorok() if r['strong'] == strong]
    return sorted(sorok, key=lambda r: (r['szotar'], r['jelentes_szam']))


def domen_talalatok(strong):
    rows = L.load_sdbh_domenek() if strong.startswith('H') else L.load_sdgnt_domenek()
    hits = [r for r in rows if r['strong'] == strong]
    domenkodok = _sorted_unique(r['domen_kod'] for r in hits if r['domen_kod'] != EM_DASH)
    talalatok = []
    for kod in domenkodok:
        label = next(r['domen'] for r in hits if r['domen_kod'] == kod)
        talalatok.append((kod, label))
    return talalatok


def domen_anomalia_figyelmeztetes(strong):
    dataset_name = 'SDBH' if strong.startswith('H') else 'SDGNT'
    anom_rows = L.load_sdbh_sdgnt_anomaliak()
    return L._matching_jelentes_nelkul(anom_rows, dataset_name, strong)


def _jsz_cimke(jelentes_szam):
    if jelentes_szam == 'teljes':
        return '(teljes szócikk)'
    if jelentes_szam == 'részlet':
        return '(részlet)'
    return '%s. jelentés' % jelentes_szam


def _szotar_reszek(strong, szint_eltolas, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh):
    """Egy Strong-szám szótári adatai szerepenként szétbontva (F78, DT-F78b):
    a Strong-fejléc (lemma + kiejtés, 10. szerep), a TWOT-sor (héber 3.),
    a domén-sorok (4.), és a forrásonkénti jelentés-blokkok (1., 2., 8.).
    A licenc-gyűjtés mellékhatása azonos a régi, egybeépített változatéval.
    Visszaad egy dict-et: fejlec_cim, lemma_kiejtes, twot, domen (sorok listája),
    forras_blokkok [(szotar, [bekezdések])], van_hivatkozas, tisztazatlan_erintve."""
    cim_hash = '#' * (3 + szint_eltolas)
    sub_hash = '#' * (4 + szint_eltolas)

    lk = lemma_kiejtes(strong)
    if lk:
        lemma, kiejtes = lk
        fejlec = '%s %s — %s (%s)' % (cim_hash, strong, lemma, kiejtes)
        fajl_licenc_kulcsok_tbesg_tbesh.add('TBESG' if strong.startswith('G') else 'TBESH')
    else:
        fejlec = '%s %s' % (cim_hash, strong)

    if strong.startswith('H'):
        twotok = oshl_twot_ehhez(strong)
        twot = '**TWOT:** %s' % (', '.join(twotok) if twotok else EM_DASH)
        fajl_licenc_kulcsok.setdefault('konkordancia/OSHL_lexikalis_index.tsv', set()).add('OSHL')
    else:
        twot = '**TWOT:** %s' % EM_DASH

    domenek = domen_talalatok(strong)
    domen_szoveg = ', '.join('%s %s' % (kod, label) for kod, label in domenek) if domenek else EM_DASH
    domen_sorok = ['**Szemantikai domén:** %s' % domen_szoveg]
    domen_fajl = 'konkordancia/SDBH_domenek.tsv' if strong.startswith('H') else 'konkordancia/SDGNT_domenek.tsv'
    domen_licenc_kulcs = 'SDBH' if strong.startswith('H') else 'SDGNT'
    fajl_licenc_kulcsok.setdefault(domen_fajl, set()).add(domen_licenc_kulcs)

    for anom in domen_anomalia_figyelmeztetes(strong):
        domen_sorok.append('*Figyelem: elemzetlen bejegyzés illeszkedik — %s %s %s*'
                           % (anom['entry_id'], anom['lemma'], anom['nyers_ertek']))

    forras_blokkok = []
    van_hivatkozas = False
    tisztazatlan_erintve = False
    # F11 R: a szerephez nem rendelt (KIEGESZITO_SZOTARAK) sorokat a 2b rés
    # rendereli (adatres_2b), a szerepmátrix nem.
    hiv_sorok = [r for r in lexikon_hivatkozasok_ehhez(strong)
                 if r['szotar'] not in KIEGESZITO_SZOTARAK]
    if hiv_sorok:
        van_hivatkozas = True
        for r in hiv_sorok:
            fajl_licenc_kulcsok.setdefault('adat/lexikon_hivatkozasok.tsv', set()).add(r['szotar'])
            fajl_licenc_kulcsok.setdefault(r['forrasfajl'], set()).add(r['szotar'])
            if licenc_tisztazatlan(r['szotar']):
                tisztazatlan_erintve = True
            bek = ['%s %s %s — %s' % (sub_hash, r['szotar'], r['entry_id'], _jsz_cimke(r['jelentes_szam'])),
                   '> %s' % r['szoveg_en']]
            hu = forditas_ehhez(r['szotar'], r['strong'], r['entry_id'], r['jelentes_szam'], 'forditas_hu')
            if hu:
                bek.append('**🇭🇺** %s' % hu)
            else:
                bek.append(FORDITASRA_VAR)
            bek.append('*Forrás: %s*' % r['forrasfajl'])
            forras_blokkok.append((r['szotar'], bek))

    return {
        'fejlec': fejlec, 'lemma_kiejtes': lk, 'twot': twot, 'domen': domen_sorok,
        'forras_blokkok': forras_blokkok, 'van_hivatkozas': van_hivatkozas,
        'tisztazatlan_erintve': tisztazatlan_erintve,
    }


def _epit_szotar_alszakasz(strong, szint_eltolas, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh):
    """Egy Strong-szám szócikk-alszakasza -- azonos logika a motívum
    tokenjeire és a Rokon szavak (D2) bejegyzéseire, a `szint_eltolas`
    (0 vagy 1) csak a heading-mélységet tolja el. Visszaadja: (szöveg,
    van_hivatkozas, tisztazatlan_erintve). F78: a rokon szavak (S5) belső
    szerkezete változatlan; a szerep-sorrendű váz a `_szotar_reszek`-et használja."""
    r = _szotar_reszek(strong, szint_eltolas, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh)
    alszakasz = [r['fejlec'], r['twot']] + r['domen']
    if r['forras_blokkok']:
        for _, bek in r['forras_blokkok']:
            alszakasz.extend(bek)
    else:
        alszakasz.append('Nincs jelentés-hivatkozás a `lexikon_hivatkozasok.tsv`-ben.')
    return '\n\n'.join(alszakasz), r['van_hivatkozas'], r['tisztazatlan_erintve']


def rokon_szavak_strongok(sorai, tokenek):
    """D2 (a), (b), (c): a motívum sajat tokenjei kozul kimaradó, a motívum
    `lxx_dontesek.tsv` soraiban `gorog_strong`-ként megnevezett, és a
    `lexikon_hivatkozasok.tsv`-ben hivatkozással rendelkező Strong-számok."""
    dontesek_idx = lxx_dontesek_index()
    strongok = set()
    for s in sorai:
        for vers in igehely_lista(s['igehely']):
            for r in dontesek_idx.get(vers, []):
                gs = (r.get('gorog_strong') or '').strip()
                if gs and STRONG_TOKEN_RE.match(gs) and gs not in tokenek:
                    strongok.add(gs)
    return sorted(s for s in strongok
                  if any(r['szotar'] not in KIEGESZITO_SZOTARAK for r in lexikon_hivatkozasok_ehhez(s)))


# --- F78: szerep-sorrendű váz (DT-F78a B változat, DT-F78b szűkített hatókör) ---

# Melyik szótári forrás tölti a szerepet (a forrásonkénti belső render változatlan).
SZEREP_SZOTAR = {
    ('gorog', 1): 'TBESG', ('gorog', 2): 'Thayer', ('gorog', 8): 'LSJ',
    ('heber', 1): 'TBESH', ('heber', 2): 'BDB',
}
# A szerep saját sora a Strong-fejlécből (DT-F78b: a TWOT/domén/kiejtés a saját szerepe alá költözik).
SZEREP_SAJAT = {
    ('heber', 3): 'twot', ('gorog', 4): 'domen', ('heber', 4): 'domen',
    ('gorog', 10): 'kiejtes', ('heber', 10): 'kiejtes',
}
# Adatosított szerep, amelynek tartalma másutt jelenik meg: hivatkozás (S4).
SZEREP_HIVATKOZAS = {
    ('gorog', 6): 'l. a 3. szakaszt (LXX-fordítói döntések)',
    ('heber', 6): 'l. a 3. szakaszt (LXX-fordítói döntések)',
    ('gorog', 8): 'a motívum saját tokenjeihez nincs LSJ-sor a `lexikon_hivatkozasok.tsv`-ben; a rokon szavaknál (alább) és a kézi 2/b szakaszban l.',
    ('gorog', 9): 'l. az 1. szakasz táblázatát (UBS-jelentés oszlop; csak újszövetségi sorok)',
}
# A 7. szerep (SECE) adatosítva (F09 S2.4, DT189); a kézi 2/b szakaszban álló SECE-táblázatok a #70-ig
# (a 2/b átírása) érintetlenek, ezért a „l. 2/b” mutató kiegészítő sorként marad (DT189).
SZEREP_KEZI_2B = {
    ('gorog', 7): 'a kézi SECE-táblázatok a 2/b szakaszban a #70-ig változatlanul állnak (l. 2/b), ha van',
    ('heber', 7): 'a kézi SECE-táblázatok a 2/b szakaszban a #70-ig változatlanul állnak (l. 2/b), ha van',
}
ROKON_SZAVAK_CIM = '### Rokon szavak'


def ures_blokk(szerep, allapot, ok):
    """DT-F78a (B változat): gépi jelölő + látható zárójeles sor, amely kimondja,
    hogy a hiány nincs kitöltve."""
    return ('<!-- ÜRES-BLOKK: %s | %s -->\n'
            '*(üres blokk: %s; a hiány nincs kitöltve gyenge vagy asszociatív anyaggal)*'
            % (szerep, allapot, ok))


FORDITASRA_VAR = '*(fordításra vár)*'
NEM_TARGYALJA = '*a forrás nem tárgyalja*'

TBESH_KONSZ_FAJL = 'konkordancia/_nyers/tbesh/TBESH_konszolidalt.tsv'
TBESH_TXT_FAJL = 'konkordancia/TBESH.txt'
# DT-F09h: a verziózott kimenet (generalt_proba/, az éles lexikon/) CSAK a verziózott TBESH.txt-ből dolgozik; a
# gitignore-olt, licenc miatt nem verziózható `.lexicon`-eredetű konszolidált tábla csak helyi, nem verziózott
# kimenetben használható (general.py --helyi-lexicon). A hiányzó _nyers/ fájl sosem hiba.
TBESH_HELYI_LEXICON = False
_tbesh_konsz_cache = None
_tbesh_konsz_mod = None


def _tbesh_txt_sorok():
    """A TBESH.txt-ből (verziózott) épített sorok: ugyanaz a tisztítás és dedup, mint a konszolidáló
    importernél (`tbesh_konszolidalt_import.txt_betolt`), `forras` = txt."""
    import tbesh_konszolidalt_import as TI
    adat = TI.txt_betolt(_U.kotelezo(_U.TBESH_TXT))
    sorok = []
    for strong in sorted(adat, key=lambda s: (int(s[1:5]), s[5:])):
        a = adat[strong]
        sorok.append({'strong': strong, 'alap_strong': TI.alap_strong_szamol(strong), 'lemma': a['lemma'],
                      'atirat': a['atirat'], 'pos_kod': a['pos_kod'], 'rovid_glosszak': a['rovid_glosszak'],
                      'teljes_szoveg': a['teljes_szoveg'], 'forras': 'txt', '_fajl': TBESH_TXT_FAJL})
    return sorok


def tbesh_konszolidalt():
    """alap_strong -> [sor-dict, ...]: a TBESH.txt-ből épített sorok (F05 S4, D3, D38; F09 S2.2). Csak a
    `TBESH_HELYI_LEXICON` bekapcsolásakor és ha a gitignore-olt konszolidált tábla megvan, abból olvas
    (a .lexicon-bővítéssel); a fájl hiánya sosem hiba (DT-F09h)."""
    global _tbesh_konsz_cache, _tbesh_konsz_mod
    helyi = bool(TBESH_HELYI_LEXICON) and os.path.isfile(_U.TBESH_KONSZOLIDALT)
    if _tbesh_konsz_cache is None or _tbesh_konsz_mod != helyi:
        if helyi:
            sorok = L.read_tsv_skip_comments(_U.TBESH_KONSZOLIDALT)
            for r in sorok:
                r['_fajl'] = TBESH_KONSZ_FAJL
        else:
            sorok = _tbesh_txt_sorok()
        d = {}
        for r in sorok:
            d.setdefault(r['alap_strong'], []).append(r)
        for lista in d.values():
            lista.sort(key=lambda r: r['strong'])
        _tbesh_konsz_cache = d
        _tbesh_konsz_mod = helyi
    return _tbesh_konsz_cache


TBESH_FORRAS_JELZO = {
    'txt': 'a TBESH.txt szövege',
    'lexicon': 'a TBESH.lexicon szövege',
    'egyenlo': 'a TBESH.txt és a TBESH.lexicon szövege (±5% eltérésen belül egyenlő)',
}


def tbesh_szoveg_dedup(szoveg):
    """F09 J5 (ellenőri 2. mellékhiba): a TBESH.txt több jelentés-sora (pl. H0127: soil / country / planet)
    ugyanazt a számozott jelentéslistát ismétli (`: soil 1) ... | : country 1) ... | : planet 1) ...`).
    Ha minden ` | `-szel elválasztott rész azonos számozott farokkal végződik, a farok egyszer áll,
    a címkék (`: soil | : country | : planet`) előtte maradnak; egyébként a szöveg változatlan."""
    reszek = szoveg.split(' | ')
    if len(reszek) < 2:
        return szoveg
    fejek, farkak = [], set()
    for r_ in reszek:
        m_ = re.match(r'^(: [^0-9]*?) (1\) .*)$', r_)
        if not m_:
            return szoveg
        fejek.append(m_.group(1))
        farkak.add(m_.group(2))
    if len(farkak) != 1:
        return szoveg
    return ' | '.join(fejek) + ' ' + farkak.pop()


SZEMELYNEV_POS_RE = re.compile(r'^N:')   # minden N: kezdetű (tulajdonnév) morfológia (DT-F09h kiegészítés, 2. rész)


def tbesh_sorok_tokenhez(token):
    """A TBESH.txt sorai egy tokenhez (DT-F09h kiegészítés, F05 D38). Ha van pontos (betűutótag nélküli) sor,
    csak az; különben a betűutótagos alszócikkek (H2403a, H2403b …) a személynevek (`N:…-P` morfológia)
    kizárásával. (A TAHOT bővített Strong szerinti szűkítés nem érhető el: a TAHOT_kivonat.tsv Strong-oszlopa
    betűutótag nélküli.) Az alszócikk-sorok a blokkban jelöltek."""
    sorok = tbesh_konszolidalt().get(token, [])
    pontos = [r for r in sorok if r['strong'] == token]
    if pontos:
        return pontos
    return [r for r in sorok if not SZEMELYNEV_POS_RE.match(r.get('pos_kod', ''))]


def tbesh_csak_tulajdonnev(token):
    """A token alszócikkei (strong-kulcsok), ha a TBESH.txt-ben van sor, de mind tulajdonnév (`N:`): ilyenkor
    a blokk nem `a forrás nem tárgyalja`, hanem `csak tulajdonnév-alszócikk` jelzést kap."""
    sorok = tbesh_konszolidalt().get(token, [])
    if sorok and not tbesh_sorok_tokenhez(token):
        return [r['strong'] for r in sorok]
    return []


def _tbesh_konsz_blokk(r, ctx):
    """Egy konszolidált TBESH-sor forrásblokkja a #78 renderének mintájára (`_szotar_reszek`)."""
    alszo = r['strong'] != r['alap_strong']
    bek = ['##### TBESH %s — (konszolidált szócikk%s)' % (r['strong'], '; alszócikk: %s' % r['strong'] if alszo else '')]
    if r.get('rovid_glosszak') and r['rovid_glosszak'] != EM_DASH:
        bek.append('**Röviden:** %s' % r['rovid_glosszak'])
    bek.append('> %s' % tbesh_szoveg_dedup(r['teljes_szoveg']))
    hu = forditas_ehhez('TBESH', r['strong'], r['strong'], 'teljes', 'forditas_hu')
    bek.append('**🇭🇺** %s' % hu if hu else FORDITASRA_VAR)
    fajl = r.get('_fajl', TBESH_TXT_FAJL)
    bek.append('*Forrás: %s (%s)*' % (fajl, TBESH_FORRAS_JELZO.get(r['forras'], r['forras'])))
    ctx['fl'].setdefault(fajl, set()).add('TBESH')
    return bek


def _token_mutato_blokk(szerep, token, mutato):
    return ('<!-- ÜRES-BLOKK: %s | adatosítva, nincs bekötve -->\n'
            '**%s** · *(üres blokk: %s; a hiány nincs kitöltve gyenge vagy asszociatív anyaggal)*'
            % (szerep, token, mutato))


def _tartalom_heber_tbesh(nyelv, n, tokenek_ny, reszek, ctx):
    """Héber 1. szerep (Alapjelentés): TBESH. Sorrend tokenenként: (1) kijelölt mutató (H7121: BDB 2.c,
    DT-F42a; a TEREMT-002 tokenjei: #12b, DT187); (2) a `lexikon_hivatkozasok.tsv` TBESH-sora (bekötött
    szó szerinti kivonat, F6.3-minta, DT187); (3) a konszolidált tábla sorai; (4) `a forrás nem tárgyalja`."""
    out = []
    for t in tokenek_ny:
        mutato = SZEREP_TOKEN_MUTATO.get((nyelv, n, t))
        if mutato:
            out.append(_token_mutato_blokk(ctx['szerep'], t, mutato))
            continue
        bl = [b for b in reszek[t]['forras_blokkok'] if b[0] == 'TBESH']
        if bl:
            for _, bek in bl:
                out.extend(bek)
            continue
        # csak a pontos (betűutótag nélküli) Strong-sor: a H1121a/b stb. STEP-alszócikkek más szavak
        # (pl. a H1121b Beno, személynév), nem a motívum tokenjének szócikkei (D38)
        sorok = tbesh_sorok_tokenhez(t)
        if not sorok and tbesh_csak_tulajdonnev(t):
            out.append('**%s** · *csak tulajdonnév-alszócikk: %s* *(TBESH)*' % (t, ', '.join(tbesh_csak_tulajdonnev(t))))
            continue
        if not sorok:
            out.append('**%s** · %s *(TBESH)*' % (t, NEM_TARGYALJA))
            continue
        for r in sorok:
            out.extend(_tbesh_konsz_blokk(r, ctx))
    return out


# --- F09 S2.3: UBS DBH (héber 5. és 9. szerep) -----------------------------

UBS_DBH_JELENTESEK_TSV = os.path.join(KONKORDANCIA, 'UBS_DBH_jelentesek.tsv')
UBS_DBH_REFERENCIAK_TSV = os.path.join(KONKORDANCIA, 'UBS_DBH_referenciak.tsv')
UBS_DBH_JELENTESEK_FAJL = 'konkordancia/UBS_DBH_jelentesek.tsv'
UBS_DBH_REFERENCIAK_FAJL = 'konkordancia/UBS_DBH_referenciak.tsv'
VERSMEGFELELTETES_TSV = os.path.join(KONKORDANCIA, 'Karoli_versmegfeleltetes.tsv')

_dbh_cache = None
_versmegf_cache = None


def _cella(szoveg):
    """Markdown-táblacellába szánt szöveg: a `|` jel escape-elve."""
    return (szoveg or '').replace('|', '\\|')


def ubs_dbh_adatok():
    """(jelentések, hivatkozások, darabszám) az UBS DBH-ból, csak az elofordulasok.tsv héber tokenjeire:
    jelentések = {strong: {lexid: első sor}} (a domén-duplikátumokból az első, mint az UBS DNTG-nél);
    hivatkozások = {(strong, igehely_MT): [lexid, ...]}; darabszám = {(strong, lexid): n}."""
    global _dbh_cache
    if _dbh_cache is None:
        _, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        kell = set()
        for r in elo:
            kell.update(t for t in motivum_strong_tokenek([r]) if t.startswith('H'))
        jelentesek = {}
        for r in L.read_tsv_skip_comments(UBS_DBH_JELENTESEK_TSV):
            if r['strong'] in kell:
                jelentesek.setdefault(r['strong'], {}).setdefault(r['lexid'], r)
        hivatkozasok = {}
        darab = {}
        for r in L.read_tsv_skip_comments(UBS_DBH_REFERENCIAK_TSV):
            if r['strong'] in kell:
                hivatkozasok.setdefault((r['strong'], r['igehely']), []).append(r['lexid'])
                kulcs = (r['strong'], r['lexid'])
                darab[kulcs] = darab.get(kulcs, 0) + 1
        _dbh_cache = (jelentesek, hivatkozasok, darab)
    return _dbh_cache


def karoli_mt_vers(karoli_vers):
    """(MT-vers, megjegyzés): a Károli-vers MT-számozású megfelelője a `Karoli_versmegfeleltetes.tsv`
    szerint (az UBS DBH hivatkozásai az MT-számozást követik). (None, ok), ha nincs biztos megfeleltetés
    -- ilyenkor a vers nem párosítható (nincs találgatás); `ÓSZ-vers`-e a tábla tagsága dönti el."""
    global _versmegf_cache
    if _versmegf_cache is None:
        _versmegf_cache = {r['igehely_karoli']: r for r in L.read_tsv_skip_comments(VERSMEGFELELTETES_TSV)}
    r = _versmegf_cache.get(karoli_vers)
    if r is None:
        return None, 'a Károli-vers nincs a versmegfeleltető táblában'
    konyv = karoli_vers.rsplit(' ', 1)[0]
    mt = (r.get('igehely_mt') or '').strip()
    if mt:
        if re.match(r'^\d+:\d+$', mt):
            return '%s %s' % (konyv, mt), ''
        return None, 'az MT-megfelelő nem egyetlen vers (%s)' % mt
    if r.get('osztaly') == 'KJV':
        return karoli_vers, ''
    return None, 'versszámozás-eltérés (%s), az MT-vers a táblában nincs megadva' % r.get('osztaly')


def _dbh_hu(mezo, strong, lexid, angol):
    """Magyar glossza/definíció a gyorsítótárból (szotar=UBS_DBH, entry_id=lexid, jelentes_szam=—);
    ha nincs sor: az angol szöveg és a `fordításra vár` jelölés (gépi fordítás nem fut, #7)."""
    hu = forditas_ehhez('UBS_DBH', strong, lexid, EM_DASH, mezo)
    return hu if hu else '%s %s' % (angol, FORDITASRA_VAR)


def _tartalom_heber_dbh_tomor(nyelv, n, tokenek_ny, reszek, ctx):
    """Héber 5. szerep (Tömör jelentés, előfordulás): UBS DBH jelentésenként glossza, rövid definíció
    és a hivatkozott helyek száma (az UBS DNTG-oldal mintájára)."""
    jelentesek, _hiv, darab = ubs_dbh_adatok()
    out = []
    for t in tokenek_ny:
        lex = jelentesek.get(t)
        if not lex:
            out.append('**%s** · %s *(UBS DBH)*' % (t, NEM_TARGYALJA))
            continue
        ossz = sum(darab.get((t, lexid), 0) for lexid in lex)
        sorok = ['**%s** · UBS DBH: %d jelentés, %d hivatkozott hely' % (t, len(lex), ossz), '',
                 '| Jelentés (lexid) | Glossza | Definíció (rövid) | Hivatkozott helyek |', '|---|---|---|---|']
        for lexid, r in lex.items():
            sorok.append('| `%s` | %s | %s | %d |' % (
                lexid, _cella(_dbh_hu('glosszak_hu', t, lexid, r['glosszak'])),
                _cella(_dbh_hu('definicio_hu', t, lexid, r['definicio_rovid'])), darab.get((t, lexid), 0)))
        out.append('\n'.join(sorok))
    ctx['fl'].setdefault(UBS_DBH_JELENTESEK_FAJL, set()).add('UBS_DBH')
    ctx['fl'].setdefault(UBS_DBH_REFERENCIAK_FAJL, set()).add('UBS_DBH')
    return out


def _tartalom_heber_dbh_vers(nyelv, n, tokenek_ny, reszek, ctx):
    """Héber 9. szerep (Versenkénti jelentés): a motívum ÓSZ-i igehelyeinél az UBS DBH jelentése
    (a Károli-verset az MT-számozásra képezve). Ahol nincs biztos megfeleltetés vagy hivatkozás, az
    ok áll, nem találgatás. Az ÚSZ-sorok nem tartoznak ide (a görög oldal az 1. szakasz oszlopa)."""
    jelentesek, hivatkozasok, _darab = ubs_dbh_adatok()
    sorai = ctx.get('sorai') or []
    konyv_sorrend = G.konyv_sorrend_betolt()
    hianyzo = set()
    rendezett = sorted(sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo))
    tokenhalmaz = set(tokenek_ny)
    sorok = []
    for s in rendezett:
        sor_tokenek = [t for t in motivum_strong_tokenek([s]) if t in tokenhalmaz]
        if not sor_tokenek:
            continue
        for vers in igehely_lista(s['igehely']):
            mt, ok = karoli_mt_vers(vers)
            if mt is None and ok == 'a Károli-vers nincs a versmegfeleltető táblában':
                continue  # nem ÓSZ-vers (a tábla az ÓSZ-t fedi): az ÚSZ-oldal az 1. szakaszban áll
            for t in sor_tokenek:
                if mt is None:
                    cella, megj = EM_DASH, ok
                else:
                    lexidek = sorted(set(hivatkozasok.get((t, mt), [])))
                    if lexidek:
                        cella = '; '.join('`%s` — %s' % (lx, _cella(jelentesek[t][lx]['glosszak']))
                                          for lx in lexidek if lx in jelentesek.get(t, {}))
                        megj = '' if mt == vers else 'MT: %s' % mt
                    else:
                        cella, megj = EM_DASH, 'nincs UBS DBH-hivatkozás erre a Strongra ebben a versben'
                sorok.append('| %s | %s | %s | %s |' % (vers, t, cella, megj or EM_DASH))
    ctx['fl'].setdefault(UBS_DBH_JELENTESEK_FAJL, set()).add('UBS_DBH')
    ctx['fl'].setdefault(UBS_DBH_REFERENCIAK_FAJL, set()).add('UBS_DBH')
    ctx['fl'].setdefault('konkordancia/Karoli_versmegfeleltetes.tsv', set()).add('Karoli_versmegfeleltetes')
    if not sorok:
        return []
    bevezeto = ('*A héber szó jelentése az ÓSZ-i igehelyeken (UBS DBH, MT-számozás szerint párosítva; a '
                'glosszák angolul állnak, magyar fordításuk a `forditasok.tsv`-be kerül, ahol van, onnan jön; '
                'a többi fordításra vár).*')
    tabla = '\n'.join(['| Igehely (Károli) | Strong | UBS DBH-jelentés (lexid — glossza) | Megjegyzés |',
                       '|---|---|---|---|'] + sorok)
    return [bevezeto, tabla]


# --- F09 S2.4: UBS DNTG + Mounce (görög 5. szerep), SECE (7. szerep) --------

UBS_DNTG_JELENTESEK_FAJL = 'konkordancia/UBS_DNTG_jelentesek.tsv'
UBS_DNTG_REFERENCIAK_FAJL = 'konkordancia/UBS_DNTG_referenciak.tsv'
MCGED_TSV = os.path.join(KONKORDANCIA, 'MCGED_teljes.tsv')
MCGED_FAJL = 'konkordancia/MCGED_teljes.tsv'
SECE_FAJL = {'G': 'konkordancia/SECE_G_teljes.tsv', 'H': 'konkordancia/SECE_H_teljes.tsv'}
SECE_LICENC_KULCS = {'G': 'SECE_G', 'H': 'SECE_H'}

_dntg_cache = None
_mcged_cache = None
_sece_cache = {}


def ubs_dntg_adatok():
    """(jelentések, darabszám) az UBS DNTG-ből a render Strongjaira: jelentések = {strong: {lexid: első sor}},
    darabszám = {(strong, lexid): hivatkozott helyek száma}. Az UBS DNTG-adatot a `ubs_hozzarendeles.py`
    olvasója tölti be (nem másolás)."""
    global _dntg_cache
    if _dntg_cache is None:
        jel_sorok = UBS.read_tsv_rows(UBS.JELENTESEK_PATH)
        ref_sorok = UBS.read_tsv_rows(UBS.REFERENCIAK_PATH)
        jelentesek = {}
        for r in jel_sorok:
            jelentesek.setdefault(r['strong'], {}).setdefault(r['lexid'], r)
        darab = {}
        for r in ref_sorok:
            kulcs = (r['strong'], r['lexid'])
            darab[kulcs] = darab.get(kulcs, 0) + 1
        _dntg_cache = (jelentesek, darab)
    return _dntg_cache


def mcged_sor(strong):
    """A Mounce-szócikk sora (dict) vagy None. A `gk_szam` oszlop a MCGED belső kulcsa (`G5` + a GK-szám)."""
    global _mcged_cache
    if _mcged_cache is None:
        _mcged_cache = {r['strong']: r for r in L.read_tsv_skip_comments(MCGED_TSV)}
    return _mcged_cache.get(strong)


def _dntg_hu(mezo, strong, lexid, entry_kod, angol):
    hu = forditas_ehhez('UBS_DNTG', strong, lexid, entry_kod, mezo)
    return hu if hu else '%s %s' % (angol, FORDITASRA_VAR)


def _tartalom_gorog_tomor(nyelv, n, tokenek_ny, reszek, ctx):
    """Görög 5. szerep (Tömör jelentés, előfordulás): az UBS DNTG glosszája és hivatkozás-száma
    jelentésenként, kiegészítve a Mounce tömör glosszájával (szó szerinti megjelöléssel, a kolofonban)."""
    jelentesek, darab = ubs_dntg_adatok()
    out = []
    for t in tokenek_ny:
        lex = jelentesek.get(t)
        sorok = []
        if lex:
            ossz = sum(darab.get((t, lexid), 0) for lexid in lex)
            sorok.append('**%s** · UBS DNTG: %d jelentés, %d hivatkozott hely' % (t, len(lex), ossz))
            sorok += ['', '| Jelentés (lexid) | Louw–Nida | Glossza | Definíció (rövid) | Hivatkozott helyek |',
                      '|---|---|---|---|---|']
            for lexid, r in lex.items():
                sorok.append('| `%s` | %s | %s | %s | %d |' % (
                    lexid, r['entry_kod'],
                    _cella(_dntg_hu('glosszak_hu', t, lexid, r['entry_kod'], r['glosszak'])),
                    _cella(_dntg_hu('definicio_hu', t, lexid, r['entry_kod'], r['definicio_rovid'])),
                    darab.get((t, lexid), 0)))
        else:
            sorok.append('**%s** · %s *(UBS DNTG)*' % (t, NEM_TARGYALJA))
        mc = mcged_sor(t)
        sorok.append('')
        if mc:
            hu = forditas_ehhez('MCGED', t, mc['gk_szam'], EM_DASH, 'glosszak_hu')
            sorok.append('*Mounce (GK %d):* %s' % (int(mc['gk_szam'][2:]), hu if hu else '%s %s' % (mc['glossza'], FORDITASRA_VAR)))
        else:
            sorok.append('*Mounce:* %s' % NEM_TARGYALJA)
        out.append('\n'.join(sorok))
    ctx['fl'].setdefault(UBS_DNTG_JELENTESEK_FAJL, set()).add('UBS_DNTG')
    ctx['fl'].setdefault(UBS_DNTG_REFERENCIAK_FAJL, set()).add('UBS_DNTG')
    ctx['fl'].setdefault(MCGED_FAJL, set()).add('MCGED')
    return out


def sece_megfelelok(strong):
    """A SECE-szócikk másik nyelvi megfelelő-listája (sorrendtartó, ismétlés nélkül), vagy None:
    görög szócikkben a `Hebrew:`, héberben a `Greek:` mező. (A `LN:` mező csak keresztellenőrzés az
    UBS DNTG ellen, a naplok/F09_S2_4_sece_ln_ellenorzes.py végzi, F05 D7.) None: nincs szócikk vagy
    a mező hiányzik -- a SECE nem tárgyalja."""
    nyelv = strong[0]
    if nyelv not in _sece_cache:
        ut = os.path.join(ROOT, SECE_FAJL[nyelv])
        _sece_cache[nyelv] = {r['Strong_padded']: r['Teljes_szocikk'] for r in L.read_tsv_skip_comments(ut)}
    szoveg = _sece_cache[nyelv].get(strong)
    if not szoveg:
        return None
    cimke = 'Hebrew' if nyelv == 'G' else 'Greek'
    m = re.search(r'\s%s:\s(.*?)\sDerivation:' % cimke, szoveg)
    if not m:
        return None
    lista = []
    for elem in m.group(1).split(','):
        elem = elem.strip()
        if elem and elem not in lista:
            lista.append(elem)
    return lista or None


def _tartalom_sece(nyelv, n, tokenek_ny, reszek, ctx):
    """7. szerep (Megfelelők a másik nyelven): a SECE megfelelő-listája. A szó szerinti lista a forrásé;
    ahol a SECE-szócikknek nincs ilyen mezője, `a forrás nem tárgyalja`."""
    out = []
    cimke = 'héber' if nyelv == 'gorog' else 'görög'
    betu = 'G' if nyelv == 'gorog' else 'H'
    for t in tokenek_ny:
        lista = sece_megfelelok(t)
        if lista:
            out.append('**%s** · SECE — %s megfelelők (%d): %s' % (t, cimke, len(lista), ', '.join(lista)))
        else:
            out.append('**%s** · %s *(SECE: nincs %s megfelelő-lista)*' % (t, NEM_TARGYALJA, cimke))
    if tokenek_ny:
        ctx['fl'].setdefault(SECE_FAJL[betu], set()).add(SECE_LICENC_KULCS[betu])
    return out


# --- F09 S2.5: tW + TWOT (3. szerep), BDB-etimológia (héber 8.), LXX versszintű párok (héber 6.) ---

TW_TSV = os.path.join(KONKORDANCIA, 'tW_szocikkek.tsv')
TW_FAJL = 'konkordancia/tW_szocikkek.tsv'
BDB_ETIM_TSV = os.path.join(KONKORDANCIA, 'BDB_etimologia_kezi_hatarok.tsv')
BDB_ETIM_FAJL = 'konkordancia/BDB_etimologia_kezi_hatarok.tsv'
BDB_TELJES_FAJL = 'konkordancia/BDB_teljes_unabridged.tsv'
LXX_PAROK_TSV = os.path.join(KONKORDANCIA, 'LXX_versszintu_parok.tsv')
LXX_PAROK_FAJL = 'konkordancia/LXX_versszintu_parok.tsv'
LXX_PAROK_TOP = 10

_tw_cache = None
_bdb_etim_cache = None
_lxx_parok_cache = None


def tw_szocikkek():
    """(sorok, strong -> [sor]) a tW_szocikkek.tsv-ből; a `strong` mező `+`-szal elválasztott lista."""
    global _tw_cache
    if _tw_cache is None:
        sorok = L.read_tsv_skip_comments(TW_TSV)
        idx = {}
        for r in sorok:
            r['strongok'] = [s for s in r['strong'].split('+') if s]
            for s in r['strongok']:
                idx.setdefault(s, []).append(r)
        _tw_cache = (sorok, idx)
    return _tw_cache


def _tw_szoveg_idezetblokk(szoveg):
    """A tW-szöveg `\\n` jelölései valódi sortörésre, soronként idézőblokkba (a szöveg változatlan; a
    formázás a módosítás, a kolofon jelzi)."""
    sorok = szoveg.replace('\\n', '\n').split('\n')
    return '\n'.join(('> %s' % s).rstrip() for s in sorok)


# A tW-szócikk szövegét közlő blokk jele: a kolofon „Módosítás” mondata ebből tudja, hogy a lap a szócikk szövegét
# közli-e, vagy csak az azonosítóit nevezi meg (F131.17, ELLENOR_SZOTARI_GERINC_2 1.).
TW_SZOVEG_JEL = '(tW; a motívum tokenje: '


def _tw_cikk_blokk(r, tokenek):
    kotes = [s for s in r['strongok'] if s in tokenek]
    hu = forditas_ehhez('tW_szocikkek', r['strongok'][0] if r['strongok'] else EM_DASH, r['tw_id'], EM_DASH, 'forditas_hu')
    return (('<details>\n<summary>%s — %s ' + TW_SZOVEG_JEL + '%s)</summary>\n\n%s\n\n%s\n\n</details>')
            % (r['tw_id'], r['cim'], ', '.join(kotes), _tw_szoveg_idezetblokk(r['szoveg']),
               '**🇭🇺** %s' % hu if hu else FORDITASRA_VAR))


def _tartalom_teologiai(nyelv, n, tokenek_ny, reszek, ctx):
    """3. szerep (Teológiai szócikk): unfoldingWord Translation Words (mindkét nyelven elfogadva, S0b.2),
    héberül a TWOT-szám hivatkozásként (D19). A szócikk szövege egyszer áll (szócikkenként), a tokenek
    sorai rá mutatnak; a Strong-kötés a tW saját `Word Data` listáját követi. Ahol nincs tW-szócikk: `a forrás
    nem tárgyalja` (D11)."""
    _sorok, idx = tw_szocikkek()
    tokenhalmaz = set(tokenek_ny)
    out = []
    latott = []
    for t in tokenek_ny:
        sorok_t = []
        if nyelv == 'heber':
            sorok_t.append('**%s** · %s' % (t, reszek[t]['twot']))
        cikkek = idx.get(t, [])
        if cikkek:
            sorok_t.append('**%s** · tW: %s' % (t, ', '.join('`%s`' % c['tw_id'] for c in cikkek)))
            for c in cikkek:
                if c['tw_id'] not in [x['tw_id'] for x in latott]:
                    latott.append(c)
        else:
            sorok_t.append('**%s** · %s *(tW)*' % (t, NEM_TARGYALJA))
        out.append('\n\n'.join(sorok_t))
    if latott:
        out.append('*A tW-szócikkek szövege (angolul; a magyar fordítás a gyorsítótárból, ahol van, különben '
                   'fordításra vár). A Strong-kötés a tW saját listáján alapul, nem a projekt azonosítása.*')
        out.extend(_tw_cikk_blokk(c, tokenhalmaz) for c in latott)
        ctx['fl'].setdefault(TW_FAJL, set()).add('tW_szocikkek')
    if nyelv == 'heber':
        ctx['fl'].setdefault('konkordancia/OSHL_lexikalis_index.tsv', set()).add('OSHL')
    return out


def bdb_etimologia():
    """strong -> sor a BDB_etimologia_kezi_hatarok.tsv-ből."""
    global _bdb_etim_cache
    if _bdb_etim_cache is None:
        _bdb_etim_cache = {r['strong']: r for r in L.read_tsv_skip_comments(BDB_ETIM_TSV)}
    return _bdb_etim_cache


def _tartalom_heber_etimologia(nyelv, n, tokenek_ny, reszek, ctx):
    """Héber 8. szerep (Nyelvi háttér): a BDB-szócikk feje (etimológia, rokon nyelvi adatok) az
    elsőként zárójelen kívüli em-dash előtti határig (D41). Csak `gepi` és `jovahagyott` határ
    (F05 D41); `nem_targyalja`: `a forrás nem tárgyalja`."""
    idx = bdb_etimologia()
    out = []
    for t in tokenek_ny:
        r = idx.get(t)
        if r is None or r['allapot'] == 'nem_targyalja':
            out.append('**%s** · %s *(BDB: a szócikk feje nem ad nyelvi hátteret)*' % (t, NEM_TARGYALJA))
            continue
        if r['allapot'] not in ('gepi', 'jovahagyott'):
            out.append('**%s** · *a BDB-határ állapota %s: nem renderelhető* (F05 D41)' % (t, r['allapot']))
            continue
        hu = forditas_ehhez('BDB', t, t, 'nyelvi_hatter', 'forditas_hu')
        out.append('\n\n'.join([
            '##### BDB %s — nyelvi háttér (a szócikk feje)' % t,
            '> %s' % r['nyelvi_hatter'],
            '**🇭🇺** %s' % hu if hu else FORDITASRA_VAR,
            '*Forrás: %s (a szócikk: %s); határ: %s*' % (BDB_ETIM_FAJL, BDB_TELJES_FAJL,
                                                         'gépi' if r['allapot'] == 'gepi' else 'jóváhagyott')]))
    if tokenek_ny:
        ctx['fl'].setdefault(BDB_ETIM_FAJL, set()).add('BDB')
        ctx['fl'].setdefault(BDB_TELJES_FAJL, set()).add('BDB')
    return out


def lxx_versszintu_parok():
    """heber_strong -> {'versek': {igehely: [gorog_strong,...]}, 'proveniencia': első sor proveniencia-ja}."""
    global _lxx_parok_cache
    if _lxx_parok_cache is None:
        d = {}
        for r in L.read_tsv_skip_comments(LXX_PAROK_TSV):
            e = d.setdefault(r['heber_strong'], {'versek': {}, 'proveniencia': r['proveniencia']})
            gs = e['versek'].setdefault(r['igehely'], [])
            if r['gorog_strong']:
                gs.append(r['gorog_strong'])
        _lxx_parok_cache = d
    return _lxx_parok_cache


def _tartalom_heber_lxx_parok(nyelv, n, tokenek_ny, reszek, ctx):
    """Héber 6. szerep (LXX-híd): a 3. szakaszra mutató hivatkozás MELLETT, külön sorban a
    LXX_versszintu_parok.tsv összesítése -- versszintű együtt-előfordulás, NEM szóillesztés és nem
    LXX-fordítói döntés (F05 S13, D14, D25)."""
    parok = lxx_versszintu_parok()
    out = ['*Hivatkozás: %s.*' % SZEREP_HIVATKOZAS[(nyelv, n)],
           '*Versszintű együtt-előfordulás, nem szóillesztés (a token összes ÓSZ-i helye, a grammatikai '
           'szavak szűrésével; nem LXX-fordítói döntés):*']
    for t in tokenek_ny:
        e = parok.get(t)
        if not e:
            out.append('**%s** · %s *(LXX versszintű párok)*' % (t, NEM_TARGYALJA))
            continue
        versek = e['versek']
        parral = {v: gs for v, gs in versek.items() if gs}
        szamlalo = {}
        for gs in parral.values():
            for g in set(gs):
                szamlalo[g] = szamlalo.get(g, 0) + 1
        legjobb = sorted(szamlalo.items(), key=lambda x: (-x[1], x[0]))[:LXX_PAROK_TOP]
        reszek_g = []
        for g, db in legjobb:
            lk = lemma_kiejtes(g)
            reszek_g.append('%s (%s, %s): %d vers' % (lk[0], lk[1], g, db) if lk else '%s: %d vers' % (g, db))
        out.append('**%s** · %d vers az LXX_OS-ben (ebből %d vers görög tartalmi szóval); leggyakoribb görög '
                   'társak: %s' % (t, len(versek), len(parral), '; '.join(reszek_g) if reszek_g else EM_DASH))
    if tokenek_ny:
        prov = next((parok[t]['proveniencia'] for t in tokenek_ny if t in parok), EM_DASH)
        prov = re.sub(r' \| heber_strong=H\d{4}', '', prov)
        out.append('*Proveniencia (a tábla soraiból): %s*' % prov)
        ctx['fl'].setdefault(LXX_PAROK_FAJL, set()).add('LXX_versszintu_parok')
    return out


def szerep_token_adat_van(nyelv, n, token):
    """True/False: az `adatosítva` szerep forrásában van-e adat ehhez a tokenhez (a törzscikk
    lefedettségi mátrixához, F05 D11: `a forrás nem tárgyalja`); None: a szerepre nincs token-szintű
    szabály (a cella a szerep forrása). Ugyanazokat az adatforrásokat kérdezi, mint a szerep-építők."""
    k = (nyelv, n)
    if k == ('heber', 1):
        return bool(tbesh_sorok_tokenhez(token)) \
            or any(r['szotar'] == 'TBESH' for r in lexikon_hivatkozasok_ehhez(token))
    if k in (('gorog', 3), ('heber', 3)):
        return bool(tw_szocikkek()[1].get(token)) or (nyelv == 'heber' and bool(oshl_twot_ehhez(token)))
    if k == ('gorog', 5):
        return bool(ubs_dntg_adatok()[0].get(token)) or mcged_sor(token) is not None
    if k in (('heber', 5), ('heber', 9)):
        return bool(ubs_dbh_adatok()[0].get(token))
    if k in (('gorog', 7), ('heber', 7)):
        return sece_megfelelok(token) is not None
    if k == ('heber', 8):
        r = bdb_etimologia().get(token)
        return bool(r) and r['allapot'] in ('gepi', 'jovahagyott')
    if k == ('heber', 6):
        return token in lxx_versszintu_parok()
    if k == ('heber', 10):
        return heber_lemma_kiejtes_van(token)
    return None


def heber_lemma_kiejtes_van(token):
    lk = tbesg_tbesh_index()
    nyers = lk[0].get(token) or lk[1].get(token)
    return bool(nyers) and heber_lemma_kiejtes(nyers[0], nyers[1]) is not None


def szerep_lefedettseg_cella(nyelv, sor, token):
    """A törzscikk lefedettségi mátrixának cellája: forrás-hivatkozás, ha az `adatosítva` szerepnek van
    adata a tokenhez; `a forrás nem tárgyalja`, ha a forrásban nincs szócikk (D11); H7121 héber 1.:
    a BDB 2.c mutató (DT-F42a); `javaslat` / `nincs forrás` / `nincs adatosítva`: az állapot maga."""
    allapot = sor['allapot']
    if allapot != 'adatosítva':
        return allapot
    n = int(sor['sorrend'])
    if (nyelv, n, token) in SZEREP_TOKEN_MUTATO:
        return 'BDB 2.c (DT-F42a)' if (nyelv, n, token) == ('heber', 1, 'H7121') else 'bekötés később'
    van = szerep_token_adat_van(nyelv, n, token)
    if van is False and (nyelv, n) == ('heber', 1) and tbesh_csak_tulajdonnev(token):
        return 'csak tulajdonnév-alszócikk: %s' % ', '.join(tbesh_csak_tulajdonnev(token))
    if van is False:
        return 'a forrás nem tárgyalja'
    return sor.get('forras', EM_DASH)


# Szerepenkénti egyedi építők: (nyelv, sorrend) -> függvény(nyelv, n, tokenek_ny, reszek, ctx) -> bekezdések.
# A többi szerep az alábbi általános ágakon (SZEREP_SZOTAR / SZEREP_SAJAT) épül.
SZEREP_EPITO = {
    ('heber', 1): _tartalom_heber_tbesh,
    ('gorog', 3): _tartalom_teologiai,
    ('heber', 3): _tartalom_teologiai,
    ('heber', 5): _tartalom_heber_dbh_tomor,
    ('heber', 6): _tartalom_heber_lxx_parok,
    ('heber', 8): _tartalom_heber_etimologia,
    ('heber', 9): _tartalom_heber_dbh_vers,
    ('gorog', 5): _tartalom_gorog_tomor,
    ('gorog', 7): _tartalom_sece,
    ('heber', 7): _tartalom_sece,
}


def _szerep_tartalom(nyelv, n, tokenek_ny, reszek, ctx):
    """A szerep kitöltött bekezdései: lista. Üres lista = a szerepnek nincs adata ezekhez a tokenekhez."""
    kulcs = (nyelv, n)
    if ctx.get('gerinc') and kulcs in GERINC_SZEREP_EPITO:
        return GERINC_SZEREP_EPITO[kulcs](nyelv, n, tokenek_ny, reszek, ctx)
    if kulcs in SZEREP_EPITO:
        return SZEREP_EPITO[kulcs](nyelv, n, tokenek_ny, reszek, ctx)
    out = []
    if kulcs in SZEREP_SZOTAR:
        szotar = SZEREP_SZOTAR[kulcs]
        tobb_van = any(b[0] == szotar for t in tokenek_ny for b in reszek[t]['forras_blokkok'])
        if tobb_van:
            for t in tokenek_ny:
                bl = [b for b in reszek[t]['forras_blokkok'] if b[0] == szotar]
                if not bl:
                    out.append('*%s: nincs %s-sor ehhez a szerephez.*' % (t, szotar))
                for _, bek in bl:
                    out.extend(bek)
    elif SZEREP_SAJAT.get(kulcs) == 'twot':
        for t in tokenek_ny:
            out.append('**%s** · %s' % (t, reszek[t]['twot']))
    elif SZEREP_SAJAT.get(kulcs) == 'domen':
        for t in tokenek_ny:
            d = reszek[t]['domen']
            out.append('**%s** · %s' % (t, d[0]))
            out.extend(d[1:])
    elif SZEREP_SAJAT.get(kulcs) == 'kiejtes':
        for t in tokenek_ny:
            lk = reszek[t]['lemma_kiejtes']
            if lk:
                out.append('**%s** · %s (%s)' % ((t,) + tuple(lk)))
    return out


# DT-F78d (lezárva): a TBESH (CC BY 4.0, DT-F33f) a héber 1. szerep forrása marad, `adatosítva`; a DT-F42a csak a
# H7121 „részlet” sorát váltotta ki BDB-vel. F09 (DT187): a TEREMT-002 két tokenének (H8414, H0922) szótári
# bekötése a #12b dolga; a render ezeken a helyeken a mutatót adja, adatsort a #9 nem ír.
# Tokenenkénti mutató az üres blokkon.
_TEREMT002_MUTATO = 'a TEREMT-002 szótári bekötése a #12b dolga (DT187)'
SZEREP_TOKEN_MUTATO = {
    ('heber', 1, 'H7121'): 'a H7121 alapjelentését a BDB 2.c adja (DT-F42a)',
    ('heber', 1, 'H8414'): _TEREMT002_MUTATO,
    ('heber', 1, 'H0922'): _TEREMT002_MUTATO,
    ('heber', 2, 'H8414'): _TEREMT002_MUTATO,
    ('heber', 2, 'H0922'): _TEREMT002_MUTATO,
}


def _token_ures_blokkok(nyelv, n, szerep, tokenek_ny):
    """Tokenenkénti jelölt üres blokkok, ha legalább egy tokennek van mutatója; különben üres lista
    (az általános, szerep-szintű üres blokk lép életbe)."""
    if not any((nyelv, n, t) in SZEREP_TOKEN_MUTATO for t in tokenek_ny):
        return []
    out = []
    for t in tokenek_ny:
        mutato = SZEREP_TOKEN_MUTATO.get(
            (nyelv, n, t), 'adatosítva, nincs bekötve; a bekötés még nem történt meg')
        out.append(_token_mutato_blokk(szerep, t, mutato))
    return out


def _szerep_blokk(nyelv, sor, tokenek_ny, reszek, ctx):
    n = int(sor['sorrend'])
    szerep, allapot = sor['szerep'], sor['allapot']
    szakasz = ['#### %d. %s' % (n, szerep)]
    ctx['szerep'] = szerep
    tart = _szerep_tartalom(nyelv, n, tokenek_ny, reszek, ctx)
    if allapot == 'adatosítva':
        if tart:
            szakasz.extend(tart)
            if (nyelv, n) in SZEREP_KEZI_2B:
                szakasz.append('*Hivatkozás: %s.*' % SZEREP_KEZI_2B[(nyelv, n)])
        elif (nyelv, n) in SZEREP_HIVATKOZAS and (nyelv, n) not in SZEREP_SAJAT:
            hiv = SZEREP_HIVATKOZAS[(nyelv, n)]
            szakasz.append('*Hivatkozás: %s%s*' % (hiv, '' if hiv.endswith('.') else '.'))
        elif _token_ures_blokkok(nyelv, n, szerep, tokenek_ny):
            szakasz.extend(_token_ures_blokkok(nyelv, n, szerep, tokenek_ny))
        else:
            # DT-F78c 1.: harmadik állapot, mutatóval a #9-re (a bekötés a #9 dolga)
            szakasz.append(ures_blokk(szerep, 'adatosítva, nincs bekötve',
                                      'a szerep adatosítva (a forrásfájl megvan), de a motívum tokenjeihez a '
                                      '`lexikon_hivatkozasok.tsv`-be nincs bekötve sor; a bekötés még nem történt meg'))
    elif not tart and (nyelv, n) in SZEREP_KEZI_2B:
        hiv = SZEREP_KEZI_2B[(nyelv, n)]
        szakasz.append('*Hivatkozás: %s.*' % hiv)
    else:
        if tart:
            szakasz.extend(tart)
            ok = '%s; a fenti sor csak hivatkozás/részadat, a szerep tartalma nincs adatosítva' % allapot
        else:
            ok = allapot
        szakasz.append(ures_blokk(szerep, allapot, ok))
    return '\n\n'.join(szakasz)


def szerep_vaz(tokenek, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh, sorai=None, motivum_id=None):
    """A 2. szakasz fő törzse: nyelv szerint (görög, héber), azon belül az
    `adat/szotar_szerepek.tsv` sorrendjében, a nem adatosított szerep explicit
    üres blokkal. Visszaad: (törzs szöveg, van_hivatkozas, tisztazatlan_erintve)."""
    szerepek = szerepek_sorok()
    van_hiv = False
    tiszt = False
    reszek = {}
    for t in tokenek:
        r = _szotar_reszek(t, 1, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh)
        nyelv = 'gorog' if t.startswith('G') else 'heber'
        megengedett = {s for (ny, _), s in SZEREP_SZOTAR.items() if ny == nyelv}
        for szotar, _ in r['forras_blokkok']:
            if szotar not in megengedett:
                raise ValueError('a(z) %s szótár nincs szerephez rendelve (%s, %s)' % (szotar, t, nyelv))
        van_hiv = van_hiv or r['van_hivatkozas']
        tiszt = tiszt or r['tisztazatlan_erintve']
        reszek[t] = r

    def sorrendben(ny):
        return sorted((s for s in szerepek if s['nyelv'] == ny), key=lambda s: int(s['sorrend']))

    g_sorok, h_sorok = sorrendben('gorog'), sorrendben('heber')
    h_idx = {int(s['sorrend']): s for s in h_sorok}
    kozos = set()
    for s in g_sorok:
        h = h_idx.get(int(s['sorrend']))
        if h and all(h[k] == s[k] for k in ('szerep', 'forras', 'allapot')):
            kozos.add(int(s['sorrend']))

    ctx = {'fl': fajl_licenc_kulcsok, 'tbesg_tbesh': fajl_licenc_kulcsok_tbesg_tbesh, 'sorai': sorai or [],
           'gerinc': gerinc_aktiv(motivum_id)}
    reszek_szoveg = []
    for nyelv, cim in (('gorog', 'Görög'), ('heber', 'Héber')):
        tok_ny = [t for t in tokenek if t.startswith('G' if nyelv == 'gorog' else 'H')]
        if not tok_ny:
            reszek_szoveg.append('### %s szavak\n\n<!-- ÜRES-NYELV: %s | nincs Strong-token -->\n'
                                 '*A motívumnak nincs %s Strong-tokenje; a %s szerepek nem alkalmazhatók.*'
                                 % (cim, nyelv, cim.lower(), cim.lower()))
            continue
        blokkok = ['### %s szavak: %s' % (cim, ', '.join(tok_ny))]
        if ctx['gerinc']:
            # F131 (DT371 1.): a szótári gerinc a nyelvi blokk elején
            blokkok.append(gerinc_nyelvi_blokk(nyelv, tok_ny, ctx))
        for s in (g_sorok if nyelv == 'gorog' else h_sorok):
            if int(s['sorrend']) in kozos:
                continue
            blokkok.append(_szerep_blokk(nyelv, s, tok_ny, reszek, ctx))
        reszek_szoveg.append('\n\n'.join(blokkok))
    if kozos:
        blokkok = ['### Nyelvfüggetlen szerepek']
        for s in g_sorok:
            if int(s['sorrend']) in kozos:
                blokkok.append(_szerep_blokk('gorog', s, [], reszek, ctx))
        reszek_szoveg.append('\n\n'.join(blokkok))
    return '\n\n'.join(reszek_szoveg), van_hiv, tiszt


def blokk_szocikkek(m, tokenek, sorai):
    reszek = []
    fajl_licenc_kulcsok = {'adat/lexikon_hivatkozasok.tsv': set()}
    van_hivatkozas_barmelyikhez = False
    tisztazatlan_erintve = False

    fajl_licenc_kulcsok_tbesg_tbesh = set()
    # F78 (DT-F78b): szerep-sorrendű váz a Strong-szám szerinti helyett.
    vaz_szov, van_hiv, tiszt = szerep_vaz(tokenek, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh, sorai,
                                          m['id'])
    van_hivatkozas_barmelyikhez = van_hivatkozas_barmelyikhez or van_hiv
    tisztazatlan_erintve = tisztazatlan_erintve or tiszt
    reszek.append(vaz_szov)

    rokon_strongok = rokon_szavak_strongok(sorai, tokenek)
    if rokon_strongok:
        rokon_reszek = ['### Rokon szavak']
        for strong in rokon_strongok:
            alszakasz_szov, van_hiv, tiszt = _epit_szotar_alszakasz(
                strong, 1, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh)
            van_hivatkozas_barmelyikhez = van_hivatkozas_barmelyikhez or van_hiv
            tisztazatlan_erintve = tisztazatlan_erintve or tiszt
            rokon_reszek.append(alszakasz_szov)
        reszek.append('\n\n'.join(rokon_reszek))

    if not fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv']:
        del fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv']
    if 'TBESG' in fajl_licenc_kulcsok_tbesg_tbesh:
        fajl_licenc_kulcsok.setdefault('konkordancia/TBESG.txt', set()).add('TBESG')
    if 'TBESH' in fajl_licenc_kulcsok_tbesg_tbesh:
        fajl_licenc_kulcsok.setdefault('konkordancia/TBESH.txt', set()).add('TBESH')

    torzs = '\n\n'.join(reszek)
    licenc_lista = _sorted_unique(LC(k) for kulcsok in fajl_licenc_kulcsok.values() for k in kulcsok)
    forras_licenc_parok = [
        (fajl, licenc)
        for fajl, kulcsok in fajl_licenc_kulcsok.items()
        for licenc in _sorted_unique(LC(k) for k in kulcsok)
    ]
    # A tisztázatlan-jelölés a blokk MINDEN felhasznált forráskulcsára a táblából jön (N9).
    tisztazatlan_erintve = tisztazatlan_erintve or any(
        licenc_tisztazatlan(k) for kulcsok in fajl_licenc_kulcsok.values() for k in kulcsok)
    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d Strong-tokenjét fedi, szerepenként a szerepmátrix '
               '(`szotar_szerepek.tsv`) sorrendjében, %s jelentés-hivatkozással '
               'a `lexikon_hivatkozasok.tsv`-ből.'
               % (m['id'], len(tokenek), 'van' if van_hivatkozas_barmelyikhez else 'nincs'))
    # F78: a szerepmátrix (projekt-adat) a blokk forrása is; a licenc-kulcsok között nem szerepel
    # (a kulcsok dataset-kulcsok), ezért külön kerül a forrás-, licenc- és pár-listába.
    forras_lista = sorted(list(fajl_licenc_kulcsok) + ['adat/szotar_szerepek.tsv'])
    licenc_lista = _sorted_unique(licenc_lista + [LC('projekt_adat')])
    forras_licenc_parok.append(('adat/szotar_szerepek.tsv', LC('projekt_adat')))
    blokk_szoveg = _lexikon_blokk(m['id'], 'szocikkek', forras_lista, licenc_lista, hatokor, torzs)
    return blokk_szoveg, tisztazatlan_erintve, forras_licenc_parok


# ---------------------------------------------------------------------------
# F131: a motívumlap szótári gerince (DT272 = DT338; DT371–e, SEMA 2.40)
# ---------------------------------------------------------------------------
# Kapcsoló: az új szótári blokk, a szerepmátrix szűkítése és az előfordulás-tábla
# két oszlopa ("Jelentés (a szó)", "Funkció (a motívumban)") csak ezeken a lapokon él;
# a többi lap bájtra változatlan (DT272 (f): előbb az arany lap).
SZOTARI_GERINC_MOTIVUMOK = frozenset({'ISTENTISZT-001'})

SZAKASZ_CIMKE_FAJL = 'adat/szotar_szakasz_cimke.tsv'
BDB_SZAKASZOK_FAJL = 'adat/bdb_szakaszok.tsv'
BDB_SZAKASZ_HU_FAJL = 'adat/bdb_szakasz_hu.tsv'
BDB_VERS_JELENTES_FAJL = 'adat/bdb_vers_jelentes.tsv'
BDB_FORRAS_JAVITAS_FAJL = 'adat/bdb_forras_javitas.tsv'
TAHOT_KIVONAT_FAJL = 'konkordancia/TAHOT_kivonat.tsv'
_HANYSZOR = {2: 'kétszer', 3: 'háromszor', 4: 'négyszer', 5: 'ötször'}
THAYER_SZAKASZOK_FAJL = 'adat/thayer_szakaszok.tsv'
THAYER_VERS_JELENTES_FAJL = 'adat/thayer_vers_jelentes.tsv'
GLOSSZAK_HEBER_HU_FAJL = 'adat/glosszak_heber_hu.tsv'
THAYER_TELJES_FAJL = 'konkordancia/Thayer_teljes.tsv'
SZONEZET_UT = '/szo/%s'

GERINC_BEVEZETO = {
    'BDB': ('*Szótári gerinc (DT272): a szó jelentéstartománya a BDB tagolásában (`%s`), magyarul (`%s`). A '
            'motívumot hordozó szakaszok kibontva állnak, a többi összecsukva; a jel a BDB útvonalából készül. '
            'Kiemelve, felirat nélkül: a BDB saját példahelyei a motívum igehelyei közül (`%s`). A szótári blokk a '
            'szóról szól; a hely motívumbeli funkcióját az 1. szakasz táblázata adja.*'
            % (BDB_SZAKASZOK_FAJL, BDB_SZAKASZ_HU_FAJL, BDB_VERS_JELENTES_FAJL)),
    'Thayer': ('*Szótári gerinc (DT272): a szó jelentéstartománya a Thayer tagolásában (`%s`), magyarul. A '
               'motívumot hordozó szakaszok kibontva állnak, a többi összecsukva. Kiemelve, felirat nélkül: a Thayer '
               'saját példahelyei a motívum igehelyei közül (`%s`). A szótári blokk a szóról szól; a hely '
               'motívumbeli funkcióját az 1. szakasz táblázata adja.*' % (THAYER_SZAKASZOK_FAJL, THAYER_VERS_JELENTES_FAJL)),
}


class GerincHiba(ValueError):
    """A szótári gerinc adata ellentmond önmagának (pl. a BDB-példa nem esik a kutatói út alá):
    a futás megáll, választás és kitöltés nélkül (DT374, CLAUDE.md 3. szabály)."""


def gerinc_aktiv(motivum_id):
    return motivum_id in SZOTARI_GERINC_MOTIVUMOK


def gerinc_utvonal_vag(utvonal):
    """A záró `/-` levágása: a 2.29 (`-/3`) és a 2.30 (`-/3/-`) alakja így összevethető."""
    while utvonal.endswith('/-'):
        utvonal = utvonal[:-2]
    return utvonal


def szakasz_jel(utvonal):
    """A tagolási jel az útvonalból: `Qal/2/c` → `Qal 2.c`, `Qal/3/-` → `Qal 3`, `-/3/-` → `3`,
    `Qal/-/-` → `Qal`, `fej` → `fej`; a TBESG kulcsa (`2`) változatlan."""
    if '/' not in utvonal:
        return utvonal
    reszek = utvonal.split('/')
    felso, tobbi = reszek[0], [r for r in reszek[1:] if r and r != '-']
    szam = '.'.join(tobbi)
    if felso in ('', '-'):
        return szam or utvonal
    return ('%s %s' % (felso, szam)) if szam else felso


_MAGANHANGZO = 'aáeéiíoóöőuúüű'


def _nevelo(szo):
    """A határozott névelő (`a`/`az`) a kiejtés szerint; számnál a kiolvasott alak
    (az 1., az 5., az 50.; a 3., a 4.)."""
    szam = re.match(r'\d+', szo)
    if szam:
        n = int(szam.group(0))
        return 'az' if n == 1 or str(n)[0] == '5' or 1000 <= n < 2000 else 'a'
    return 'az' if szo[:1].lower() in _MAGANHANGZO else 'a'


def szakasz_szoveg(jelek, nevelo=True):
    """Tagolási jel(ek) prózába, névelővel: `4` → `a 4.`, `Qal 2.c` → `a Qal 2.c`,
    `['3', '4']` → `a 3., 4.`; a puszta szám sorszámnév-pontot kap; `nevelo=False`: névelő nélkül."""
    if isinstance(jelek, str):
        jelek = [jelek]
    jelek = [j + '.' if j.isdigit() else j for j in jelek]
    return ('%s %s' % (_nevelo(jelek[0]), ', '.join(jelek))) if nevelo else ', '.join(jelek)


def gerinc_ala_esik(finom, durva):
    """Igaz, ha a `finom` útvonal a `durva` alá esik (vagy azonos vele), a záró `/-` levágása után."""
    f, d = gerinc_utvonal_vag(finom), gerinc_utvonal_vag(durva)
    return f == d or f.startswith(d + '/')


def kutatoi_kulcs(jelentes_szam):
    """(kulcs, minősítő): `2.c (tagadva)` → (`2.c`, `tagadva`); a minősítő nem a szó jelentése, és nem
    része a SEMA 2.2.2 értékkészletének, ezért a kulcshoz levágjuk."""
    m = re.match(r'^\s*([^\s(]+)\s*(?:\((.*)\))?\s*$', jelentes_szam or '')
    if not m:
        return (jelentes_szam or '').strip(), ''
    return m.group(1), (m.group(2) or '').strip()


_gerinc_adat_cache = None


def gerinc_adat():
    """A gerinc tábláinak indexei (egyszer betöltve). Tesztben ugyanilyen szerkezetű dict adható át."""
    global _gerinc_adat_cache
    if _gerinc_adat_cache is not None:
        return _gerinc_adat_cache

    def be(rel):
        return G.tsv_beolvas(os.path.join(ROOT, rel))[1]

    cimke = {}
    for r in be(SZAKASZ_CIMKE_FAJL):
        cimke[(r['szotar'], r['strong'], r['szakasz'])] = r
    bdb_sz = {}
    for r in be(BDB_SZAKASZOK_FAJL):
        bdb_sz.setdefault(r['strong'], []).append(r)
    bdb_hu = {}
    for r in be(BDB_SZAKASZ_HU_FAJL):
        bdb_hu[(r['strong'], r['sorszam'])] = r
    bdb_vj = {}
    for r in be(BDB_VERS_JELENTES_FAJL):
        if r.get('szurt') == '1' or not r.get('karoli_vers'):
            continue
        bdb_vj.setdefault((r['strong'], r['karoli_vers']), []).append(r)
    th_sz = {}
    for r in be(THAYER_SZAKASZOK_FAJL):
        th_sz.setdefault(r['strong'], []).append(r)
    th_vj = {}
    for r in be(THAYER_VERS_JELENTES_FAJL):
        if r.get('karoli_vers'):
            th_vj.setdefault((r['strong'], r['karoli_vers']), []).append(r)
    glossza = {}
    for r in be(GLOSSZAK_HEBER_HU_FAJL):
        if r.get('fo') == 'igen':
            glossza[r['strong']] = r
    tiltott = be(TILTOTT_FORDULATOK_FAJL)
    # ELLENOR_SZOTARI_GERINC 1. (7.4a): a héber Strong tokenjeinek száma a Károli-versben (a TAHOT kulcsa a
    # Károli-vers, F85.6); a versszintű BDB-példa csak egytokenes versben kerülhet a sor tokenjére
    token_szam = {}
    for r in L.load_tahot():
        k = (r['Igehely'], r['Strong-szám'])
        token_szam[k] = token_szam.get(k, 0) + 1
    _gerinc_adat_cache = {'cimke': cimke, 'bdb_sz': bdb_sz, 'bdb_hu': bdb_hu, 'bdb_vj': bdb_vj,
                          'th_sz': th_sz, 'th_vj': th_vj, 'glossza': glossza, 'tiltott': tiltott,
                          'token_szam': token_szam}
    return _gerinc_adat_cache


def _bdb_strong_kulcs(strong):
    """A 2.29/2.30 Strong-alakja (`H7121`; a táblák négyjegyű, betű nélküli kulcsot használnak)."""
    return strong


def kutatoi_szakasz(adat, szotar, strong, kulcs):
    """A kutatói jelentésszám leképezése a szótár szakaszára (DT372 2.): az a sor, amelynek
    `lexikon_jelentes_szam`-a a kulcs; None, ha nincs leképezve."""
    talalat = [k[2] for k, r in adat['cimke'].items()
               if k[0] == szotar and k[1] == strong and r['lexikon_jelentes_szam'] == kulcs]
    if len(talalat) > 1:
        raise GerincHiba('a(z) %s %s %s kutatói kulcs több szakaszra mutat: %s' % (szotar, strong, kulcs, talalat))
    return talalat[0] if talalat else None


def bdb_peldak(adat, strong, vers):
    """A BDB saját példahelyei a versre (2.29, `szurt≠1`), a `fej`/`cim` nélkül (az nem jelentéspont)."""
    return [r for r in adat['bdb_vj'].get((strong, vers), []) if r['utvonal'] not in ('fej', 'cim')]


_VERS_RE = re.compile(r'^(.+) (\d+):(\d+)$')


def bdb_tartomanyban(adat, strong, vers):
    """DT382 (A), a felhasználó döntése (2026-10-28): ha a BDB a verset csak egy verstartomány belsejében idézi
    („1Kin 18:24-25”: a 18:25), a hely nem BDB-példa (a tartomány nincs kibontva), de az ⓘ ezt kimondja.
    A tartomány a 2.29 sorának `nyers`-e és a 2.30 azonos útvonalú szakaszszövege szerint: az azonos `nyers`-ű
    sorok (sorszám szerint) és a `nyers` előfordulásai a szövegben sorrendben párosítva; eltérő darabszámnál nincs
    állítás. Csak `azonos` versfeloldású sorokon. Visszaad: az ⓘ-mondatok listája (üres, ha nincs ilyen tartomány)."""
    m = _VERS_RE.match(vers)
    if not m:
        return []
    konyv, c, v = m.group(1), int(m.group(2)), int(m.group(3))
    csoport = {}
    for (st, kv), sorok in adat['bdb_vj'].items():
        mk = _VERS_RE.match(kv) if st == strong else None
        if not mk or mk.group(1) != konyv or int(mk.group(2)) != c or int(mk.group(3)) >= v:
            continue
        for r in sorok:
            if r.get('vers_feloldas') == 'azonos' and r['utvonal'] not in ('fej', 'cim'):
                csoport.setdefault((gerinc_utvonal_vag(r['utvonal']), r['nyers']), []).append(r)
    ki = []
    for (vag, nyers), sorok in sorted(csoport.items()):
        szoveg = ' '.join(' '.join(x for x in (sz.get('jel'), sz.get('szoveg')) if x)
                          for sz in adat['bdb_sz'].get(strong, []) if gerinc_utvonal_vag(sz['utvonal']) == vag)
        elofordulas = list(re.finditer(r'(?<![\w:])' + re.escape(nyers) + r'(?![\d])', szoveg))
        sorok = sorted(sorok, key=lambda r: int(r['sorszam']))
        if len(elofordulas) != len(sorok):
            continue
        for r, e in zip(sorok, elofordulas):
            t = re.match(r'\s*[-–]\s*(\d+)(?![\d:])', szoveg[e.end():])
            if t and int(_VERS_RE.match(r['karoli_vers']).group(3)) < v <= int(t.group(1)):
                # a tartomány magyar alakja a kezdővers Károli-alakjából és az MT→Károli eltolásból;
                # a BDB angol rövidítése („1Kin”) zárójelben, forrásidézetként marad
                kezd, mt = _VERS_RE.match(r['karoli_vers']), _VERS_RE.match(r['mt_vers'] or r['karoli_vers'])
                veg = int(t.group(1)) + int(kezd.group(3)) - int(mt.group(3))
                ki.append('a BDB a helyet nem önállóan idézi, hanem %s szakaszban %s %s–%d verstartomány '
                          'belsejében (a BDB-ben: „%s%s”; `%s` sorszam %s); a tartomány nincs kibontva (DT382 (A)), '
                          'ezért a hely nem BDB-példa'
                          % (szakasz_szoveg(szakasz_jel(r['utvonal'])), _nevelo(r['karoli_vers']), r['karoli_vers'], veg, nyers,
                             t.group(0).strip(), BDB_VERS_JELENTES_FAJL, r['sorszam']))
    return ki


def _bdb_sor_utvonal(adat, strong, vag_ut):
    """A 2.30 teljes útvonala a levágott alakhoz (`-/3` → `-/3/-`)."""
    for r in adat['bdb_sz'].get(strong, []):
        if gerinc_utvonal_vag(r['utvonal']) == vag_ut:
            return r['utvonal']
    return None


def jelentes_cimke_token(adat, szotar, strong, jelentes_szam, vers, kutatoi_token):
    """Egy token címkéje egy versen: (címke-szöveg vagy None, jel, ⓘ-szöveg).
    Elsőbbség (DT374): ha a szótár maga idézi a helyet, és útja a kutatói út alá esik, a finomabb
    útvonal címkéje; ha egyik sem esik a másik alá: GerincHiba. A címke a szóról szól."""
    kulcs, minosito = kutatoi_kulcs(jelentes_szam) if kutatoi_token else ('', '')
    kut_ut = kutatoi_szakasz(adat, szotar, strong, kulcs) if kulcs else None
    if kutatoi_token and kulcs and kut_ut is None:
        return None, '', ('a kutatói jelentésszám („%s”) nincs leképezve a %s tagolására (`%s`)'
                          % (kulcs, szotar, SZAKASZ_CIMKE_FAJL))
    peldak = bdb_peldak(adat, strong, vers) if szotar == 'BDB' else []
    tobb_token = []
    n_token = (adat.get('token_szam') or {}).get((vers, strong), 0)
    if peldak and n_token >= 2:
        # ELLENOR_SZOTARI_GERINC 1. (7.4a): a BDB-példa versszintű (a 2.29 nem jelöli a szót); ha a versben a
        # Strongnak több tokenje van, a példa nem rendelhető a sor tokenjéhez — a címke nem a BDB-példából jön
        tobb_token.append('a BDB a verset %s szakaszban idézi (`%s` sorszam %s), de a versben a szó %s áll '
                          '(`%s`), és a szótár nem jelöli, melyikre gondol; a BDB-példa ezért nem kerül erre a '
                          'tokenre' % (szakasz_szoveg(sorted({szakasz_jel(_bdb_sor_utvonal(adat, strong,
                                                                                       gerinc_utvonal_vag(r['utvonal']))
                                                                      or r['utvonal']) for r in peldak})),
                                       BDB_VERS_JELENTES_FAJL, ', '.join(r['sorszam'] for r in peldak),
                                       _HANYSZOR.get(n_token, '%d alkalommal' % n_token), TAHOT_KIVONAT_FAJL))
        peldak = []
    pelda_utak = sorted({gerinc_utvonal_vag(r['utvonal']) for r in peldak})
    if len(pelda_utak) > 1:
        raise GerincHiba('%s %s: a BDB-példák több útvonalra mutatnak (%s): kézi kérdés' % (strong, vers, pelda_utak))
    ip = []
    if peldak:
        p_ut = _bdb_sor_utvonal(adat, strong, pelda_utak[0]) or pelda_utak[0]
        sorszamok = ', '.join(r['sorszam'] for r in peldak)
        # DT381 (a): a forrás hibás versét a 2.31 kézi sora javította; az ⓘ a javítás forrását nevezi meg
        for r in peldak:
            if 'forras_javitas' in (r.get('okkod') or '').split(','):
                ip.append('a BDB forrásszövege itt a „%s” helyet idézi (sajtóhiba); javítva: %s — a javítás forrása: `%s`, '
                          'kézi sor (`hivatkozas_kezi`, `manual`; indok: a TAHOT és a szövegkörnyezet; DT381 (a))'
                          % (r['nyers'], r['karoli_vers'], BDB_FORRAS_JAVITAS_FAJL))
        if kut_ut is None:
            valasztott = p_ut
            ip.append('BDB-példa: a BDB %s szakaszban maga idézi a helyet (`%s` sorszam %s)'
                      % (szakasz_szoveg(szakasz_jel(p_ut)), BDB_VERS_JELENTES_FAJL, sorszamok))
        elif gerinc_ala_esik(p_ut, kut_ut):
            valasztott = p_ut
            ip.append('BDB-példa: a BDB %s szakaszban maga idézi a helyet (`%s` sorszam %s); ez a kutatói '
                      'hozzárendelés (%s → %s) alá esik, a címke a finomabb útvonalé'
                      % (szakasz_szoveg(szakasz_jel(p_ut)), BDB_VERS_JELENTES_FAJL, sorszamok, kulcs, szakasz_jel(kut_ut)))
        elif gerinc_ala_esik(kut_ut, p_ut):
            valasztott = kut_ut
            ip.append('kutatói hozzárendelés a BDB tagolása szerint (%s → %s, `%s`); a BDB a helyet a tágabb '
                      '%s szakaszban idézi (`%s` sorszam %s)'
                      % (kulcs, szakasz_jel(kut_ut), SZAKASZ_CIMKE_FAJL, szakasz_szoveg(szakasz_jel(p_ut), nevelo=False), BDB_VERS_JELENTES_FAJL,
                         sorszamok))
        else:
            raise GerincHiba('%s %s: a BDB-példa (%s) és a kutatói hozzárendelés (%s → %s) egyike sem esik a '
                             'másik alá: kézi kérdés, választás nélkül' % (strong, vers, p_ut, kulcs, kut_ut))
    elif kut_ut is not None:
        valasztott = kut_ut
        ip.append('kutatói hozzárendelés a %s tagolása szerint (`elofordulasok.tsv` jelentes_szam „%s” → %s, `%s`)'
                  % (szotar, kulcs, ('' if szotar == 'BDB' else szotar + ' ') + szakasz_jel(kut_ut),
                     SZAKASZ_CIMKE_FAJL))
        ip.extend(tobb_token)
        # a vers közvetlenül idézett (csak a token bizonytalan): a „nem önállóan idézi” tartomány-mondat nem igaz rá
        if szotar == 'BDB' and not tobb_token:
            ip.extend(bdb_tartomanyban(adat, strong, vers))
    else:
        tart = bdb_tartomanyban(adat, strong, vers) if szotar == 'BDB' and not tobb_token else []
        return None, '', '; '.join(tobb_token + tart)
    if minosito:
        ip.append('a kutatói jelentésszám minősítője („%s”) nem a szó jelentése, a címkébe nem kerül '
                  '(a minősítő nem része a SEMA 2.2.2 értékkészletének)'
                  % minosito)
    sor = adat['cimke'].get((szotar, strong, valasztott))
    cimke = (sor or {}).get('cimke_hu') or None
    jel = szakasz_jel(valasztott)
    if szotar != 'BDB':
        jel = '%s %s' % (szotar, jel)
    return cimke, jel, '; '.join(ip)




def jelentes_cella(adat, sor):
    """Az előfordulás-tábla „Jelentés (a szó)” cellája és az ⓘ szövege: (cella, ⓘ).
    Összetett Strong-mezőnél tokenenként; a kutatói hozzárendelés a `lexikon_entry_id` tokenjéé."""
    szotar = sor.get('lexikon_szotar') or ''
    entry = sor.get('lexikon_entry_id') or ''
    tokenek = [t for t in (sor.get('strong') or '').split('+') if t and STRONG_TOKEN_RE.match(t)]
    versek = igehely_lista(sor['igehely'])
    reszek, ik = [], []
    for t in tokenek:
        t_szotar = szotar if t == entry else ('BDB' if t.startswith('H') else '')
        cimke = jel = info = None
        for vers in versek:
            c, j, i = jelentes_cimke_token(adat, t_szotar, t, sor.get('jelentes_szam') or '', vers, t == entry)
            if c or j or i:
                cimke, jel, info = c, j, i
                break
        if t.startswith('G') and t_szotar != 'Thayer':
            th = [r for v in versek for r in adat['th_vj'].get((t, v), [])]
            if th:
                tinfo = 'a Thayer saját példahelye: %s (`%s` sorszam %s)' % (
                    ', '.join(sorted({'Thayer ' + szakasz_jel(r['utvonal']) for r in th})), THAYER_VERS_JELENTES_FAJL,
                    ', '.join(r['sorszam'] for r in th))
            else:
                tinfo = 'a Thayer a helyet nem idézi (`%s`)' % THAYER_VERS_JELENTES_FAJL
            info = '; '.join(x for x in (info, tinfo) if x)
        if cimke:
            szov = '%s · %s' % (cimke, jel)
        elif jel:
            szov = '*(nincs címke: %s)*' % jel
        else:
            szov = '*(nincs hozzárendelés)*'
            if not info:
                info = 'ehhez a tokenhez nincs kutatói hozzárendelés és szótári példahely'
        reszek.append((t, szov))
        ik.append('%s — %s' % (t, info) if len(tokenek) > 1 else info)
    if not reszek:
        return '*(nincs hozzárendelés)*', 'a sornak nincs Strong-tokenje'
    if len(reszek) == 1:
        cella = reszek[0][1]
    else:
        cella = '; '.join('%s: %s' % r for r in reszek)
    return cella, ' · '.join(x for x in ik if x)


def dbh_jelentes_cella(igehely, strong_field):
    """Az „UBS-jelentés” cella ÓSZ-soron (DT380): tokenenként (H-tokenek) a DBH igehelyszintű
    hivatkozásainak lexid-je és rövid definíciója, a DNTG-cella mintájára. A magyar definíció a
    `forditasok.tsv`-ből (`UBS_DBH`, entry_id = lexid, jelentes_szam = —, `definicio_hu`); ha nincs, az
    angol + `fordításra vár`. A Károli-vers az MT-számozásra képezve (`karoli_mt_vers`); ahol nincs biztos
    megfeleltetés vagy hivatkozás, a cella kimondja."""
    jelentesek, hivatkozasok, _darab = ubs_dbh_adatok()
    tokenek = [t for t in (strong_field or '').split('+') if t and t.startswith('H')]
    if not tokenek:
        return '%s *(ÓSZ; nincs H-token)*' % EM_DASH
    reszek = []
    van = False
    for t in tokenek:
        cellak = []
        okok = []
        for vers in igehely_lista(igehely):
            mt, ok = karoli_mt_vers(vers)
            if mt is None:
                okok.append(ok)
                continue
            if not hivatkozasok.get((t, mt)):
                okok.append('keresett MT-vers: %s' % mt)
            for lx in sorted(set(hivatkozasok.get((t, mt), []))):
                r = jelentesek.get(t, {}).get(lx)
                if r is None:
                    cellak.append('`%s` — *(a jelentés nincs a DBH-táblában)*' % lx)
                    continue
                szov = ubs_glossza_cella('UBS_DBH', t, lx, EM_DASH, r['glosszak'])
                cellak.append('`%s` — %s%s' % (lx, szov, '' if mt == vers else ' *(MT: %s)*' % mt))
        if cellak:
            van = True
            reszek.append((t, '; '.join(cellak)))
        else:
            reszek.append((t, '*(nincs DBH-hivatkozás%s)*' % (': ' + '; '.join(okok) if okok else '')))
    if not van:
        okok = sorted({r[1] for r in reszek})
        return '%s *(ÓSZ; %s)*' % (EM_DASH, ' · '.join(o.strip('*()') for o in okok))
    if len(reszek) == 1:
        return reszek[0][1]
    return ' · '.join('%s: %s' % r for r in reszek)


# --- hivatkozás-kiemelés a magyar szakaszban (DT272 (d)(e)) ----------------

_KONYV_RE = re.compile(r'((?:[1-3])?[A-ZÁÉÍÓÖŐÚÜŰ][A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ]*)\s+$')
_FV_RE = re.compile(r'(?<![\w:^])(\d+):(\d+)(?![\d])')
# a vers-folytatás („18:18, 25”), a verstartomány utáni is („18:24-25, 26”; DT382 (A), a 2.29 kinyerőjével
# egyezően): a tartomány nincs kibontva; a „, 1 Sámuel” / „, 1Kir” száma könyvnév, nem folytatás
_FOLYT_RE = re.compile(r'(?:\s*[-–]\s*\d+(?![\d:]))?\s*,\s*(\d+)(?![\d:\w])(?!\s+[A-ZÁÉÍÓÖŐÚÜŰ])')


def hivatkozasok_a_szovegben(szoveg):
    """[(kezdet, veg, konyv, fejezet, vers)]: a szöveg fejezet:vers hivatkozásai és vers-folytatásai, a könyv a
    közvetlenül előtte álló könyvnévből, ennek híján a legutóbbi kiírt könyvből (a BDB/Thayer folytatásos írásmódja)."""
    out = []
    aktualis = None
    for m in _FV_RE.finditer(szoveg):
        elotte = szoveg[max(0, m.start() - 12):m.start()]
        km = _KONYV_RE.search(elotte)
        kezdet = m.start()
        if km:
            aktualis = km.group(1)
            kezdet = m.start() - len(elotte) + km.start()
        out.append((kezdet, m.end(), aktualis, m.group(1), m.group(2)))
        q = m.end()
        while True:
            f = _FOLYT_RE.match(szoveg, q)
            if not f:
                break
            out.append((f.start(1), f.end(1), aktualis, m.group(1), f.group(1)))
            q = f.end()
    return out


def kiemel(szoveg, celok):
    """A célversek (`[(vers, azonosító)]`, vers Károli-alakban: `1Móz 4:26`) előfordulásait a szövegben
    felirat nélkül kiemeli (`**…**`). Versenként a k-adik előfordulás a k-adik azonosítóé.
    Visszaad: (új szöveg, [kiemelt azonosítók], [meg nem talált azonosítók])."""
    hiv = hivatkozasok_a_szovegben(szoveg)
    poz = {}
    for kezd, veg, konyv, fej, v in hiv:
        if konyv:
            poz.setdefault('%s %s:%s' % (konyv, fej, v), []).append((kezd, veg))
    csoport = {}
    for vers, azon in celok:
        csoport.setdefault(vers, []).append(azon)
    talalt, hianyzik, jelolok = [], [], []
    for vers, azonok in csoport.items():
        helyek = poz.get(vers, [])
        for i, azon in enumerate(azonok):
            if i < len(helyek):
                jelolok.append(helyek[i])
                talalt.append(azon)
            else:
                hianyzik.append(azon)
    for kezd, veg in sorted(set(jelolok), reverse=True):
        szoveg = szoveg[:kezd] + '**' + szoveg[kezd:veg] + '**' + szoveg[veg:]
    return szoveg, talalt, hianyzik


def _elso_tagmondat(szoveg, hatar=90):
    s = re.sub(r'^\s*(?:(?:\d+|[a-z]|T:\S+)\.?\s+){1,2}', '', szoveg or '').strip()
    m = re.search(r'(?<!\d):|:(?!\d)|;', s)
    if m and m.start() <= hatar:
        s = s[:m.start()]
    elif len(s) > hatar:
        s = s[:hatar].rstrip() + '…'
    return s.strip() or EM_DASH


def _vazlat_sor(jel, cimke, szoveg):
    return '- `%s` — %s' % (jel, cimke if cimke else _elso_tagmondat(szoveg))


HORGONNYAL_JELOLES = (' *(kutatói jelölés: a szakaszhatár horgonnyal illesztve, ellenőrzendő; `%s` kategoria '
                      '= horgonnyal)*' % BDB_SZAKASZ_HU_FAJL)


def _osszecsukva(sorok, elso, utolso):
    cim = elso if elso == utolso else '%s – %s' % (elso, utolso)
    return ('<details>\n<summary>%s (%d szakasz)</summary>\n\n%s\n\n</details>'
            % (cim, len(sorok), '\n'.join(sorok)))


def gerinc_szakasz_lista(szakaszok, hordozo, celok, adat_cimke, szotar, strong):
    """A tagolás vázlata: [(utvonal, jel, szöveg_hu vagy None, angol, kategória)] sorrendben.
    A hordozó szakaszok kibontva (címke + teljes magyar szöveg, kiemeléssel), a többi összecsukott
    futamokban. Visszaad: (bekezdések, kiemelt azonosítók, meg nem talált azonosítók)."""
    out, futam, talalt_ossz, hiany_ossz = [], [], [], []

    def lezar():
        if futam:
            out.append(_osszecsukva([f[2] for f in futam], futam[0][0], futam[-1][0]))
            del futam[:]

    for ut, jel, hu, angol, kat in szakaszok:
        cimke = (adat_cimke.get((szotar, strong, ut)) or {}).get('cimke_hu') or ''
        if ut not in hordozo:
            vazlat = _vazlat_sor(jel, cimke, hu or angol)
            if kat == 'horgonnyal':
                # ELLENOR_SZOTARI_GERINC 4. (7.2a): a határjelölés az összecsukott szakaszon is látszik
                vazlat += HORGONNYAL_JELOLES
            futam.append((jel, ut, vazlat))
            continue
        lezar()
        fej = '- **`%s` — %s**' % (jel, cimke) if cimke else '- **`%s`**' % jel
        if hu:
            szoveg, talalt, hiany = kiemel(hu, celok.get(ut, []))
            talalt_ossz += talalt
            hiany_ossz += hiany
            bek = [fej, '', '  > %s' % szoveg]
            if kat == 'horgonnyal':
                bek.append('  >' + HORGONNYAL_JELOLES)
        else:
            hiany_ossz += [a for _v, a in celok.get(ut, [])]
            bek = [fej, '', '  > %s' % angol, '', '  %s' % FORDITASRA_VAR]
        out.append('\n'.join(bek))
    lezar()
    return out, talalt_ossz, hiany_ossz


def _szonezet_mutato(strong, forras):
    return '[szónézet: %s](%s) · forrás: `%s`' % (SZONEZET_UT % strong, SZONEZET_UT % strong, forras)


def bdb_gerinc_szakaszok(adat, strong):
    """[(utvonal, jel, szöveg_hu, angol, kategória)] a 2.30 sorrendjében, útvonalanként összevonva
    (a `jelolo_nelkul` sor szövege az előző szakaszé), `cim` nélkül; a `fej` külön kerül vissza."""
    sorrend, adatok = [], {}
    for r in sorted(adat['bdb_sz'].get(strong, []), key=lambda x: int(x['sorszam'])):
        ut = r['utvonal']
        if ut == 'cim':
            continue
        hu = adat['bdb_hu'].get((strong, r['sorszam'])) or {}
        if ut not in adatok:
            sorrend.append(ut)
            adatok[ut] = {'hu': [], 'en': [], 'kat': ''}
        e = adatok[ut]
        if hu.get('szoveg_hu'):
            e['hu'].append(hu['szoveg_hu'])
        if (r.get('szoveg') or '').strip():
            e['en'].append(('%s %s' % (r.get('jel') or '', r['szoveg'])).strip())
        if hu.get('kategoria') in ('horgonnyal', 'elakad') or not e['kat']:
            e['kat'] = hu.get('kategoria') or e['kat']
    out = []
    for ut in sorrend:
        e = adatok[ut]
        hu = ' '.join(e['hu']) if e['hu'] else None
        if e['kat'] == 'elakad':
            hu = None
        out.append((ut, szakasz_jel(ut), hu, ' '.join(e['en']), e['kat']))
    return out


def thayer_gerinc_szakaszok(adat, strong):
    """[(utvonal, jel, szöveg_hu, angol, forrás)] a 2.34 sorrendjében, `cim` nélkül. A magyar szöveg a #142
    szakaszsoraiból (`forditasok.tsv` `Thayer`, `sz<sorszam>`, nem `elavult`; DT373 1.); ahol nincs, ott
    nincs magyar szöveg (angol + `fordításra vár`, explicit hiány)."""
    szak = sorted(adat['th_sz'].get(strong, []), key=lambda x: int(x['sorszam']))
    fidx = forditasok_index()
    out = []
    for r in szak:
        if r['utvonal'] == 'cim':
            continue
        f = fidx.get(('Thayer', strong, strong, 'sz%s' % r['sorszam'], 'forditas_hu'))
        hu = f['forditas_hu'] if f and f.get('allapot') != 'elavult' and f.get('forditas_hu') else None
        angol = ('%s %s' % (r.get('jel') or '', r.get('szoveg') or '')).strip()
        out.append((r['utvonal'], szakasz_jel(r['utvonal']), hu, angol, 'sz%s' % r['sorszam']))
    return out


TILTOTT_FORDULATOK_FAJL = 'adat/tiltott_fordulatok.tsv'


def tiltott_talalatok(tiltott, szoveg):
    """A `tiltott_fordulatok.tsv` (SEMA 2.36) mintáinak találatai a szövegben: [magyar_alak]."""
    return [r['magyar_alak'] for r in tiltott if r.get('minta') and re.search(r['minta'], szoveg or '', re.I)]


def gerinc_blokk(adat, szotar, strong, motivum_sorai, ctx=None):
    """Egy kulcsszó jelentéstartománya (szótári gerinc, DT272; DT371 (ii), DT373, DT374).
    Visszaad: (bekezdések, napló-dict a próbamérésekhez)."""
    versek = []
    kut_kulcsok = set()
    konyv_sorrend = G.konyv_sorrend_betolt()
    motivum_sorai = sorted(motivum_sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, set()))
    for s in motivum_sorai:
        tokenek = [t for t in (s.get('strong') or '').split('+') if t]
        if strong not in tokenek:
            continue
        versek.extend(igehely_lista(s['igehely']))
        if s.get('lexikon_entry_id') == strong and s.get('lexikon_szotar') == szotar:
            kut_kulcsok.add(kutatoi_kulcs(s.get('jelentes_szam') or '')[0])
    lk = lemma_kiejtes(strong)
    cim = '##### %s%s · %s' % (strong, ' — %s (%s)' % lk if lk else '', szotar)
    napl = {'strong': strong, 'szotar': szotar, 'kiemelt': [], 'nem_talalt': [], 'nem_idezett': []}
    if szotar == 'BDB':
        szakaszok = bdb_gerinc_szakaszok(adat, strong)
        vj = adat['bdb_vj']
        fej = next((s for s in szakaszok if s[0] == 'fej'), None)
        szakaszok = [s for s in szakaszok if s[0] != 'fej']
    else:
        szakaszok = thayer_gerinc_szakaszok(adat, strong)
        vj = adat['th_vj']
        fej = next((s for s in szakaszok if s[0] == 'fej'), None)
        szakaszok = [s for s in szakaszok if s[0] != 'fej']
    teljes_ut = {gerinc_utvonal_vag(s[0]): s[0] for s in szakaszok}
    celok, hordozo = {}, set()
    fej_celok = []
    napl['tartomanyban'] = []
    for vers in sorted(set(versek), key=versek.index):
        sorok = vj.get((strong, vers), [])
        if not sorok:
            # ELLENOR_SZOTARI_GERINC 3. (7.5b): a tartomány belsejében idézett hely nem „nem idézett”; a gerinc ⓘ-je a
            # sor ⓘ-jével azonos állítást mond (DT382 (A))
            tart = bdb_tartomanyban(adat, strong, vers) if szotar == 'BDB' else []
            if tart:
                napl['tartomanyban'].append('%s: %s' % (vers, '; '.join(tart)))
            else:
                napl['nem_idezett'].append(vers)
        for r in sorok:
            azon = '%s sorszam %s (%s, %s)' % (os.path.basename(BDB_VERS_JELENTES_FAJL if szotar == 'BDB'
                                                                else THAYER_VERS_JELENTES_FAJL),
                                               r['sorszam'], vers, r['utvonal'])
            if r['utvonal'] == 'fej':
                fej_celok.append((vers, azon))
                continue
            ut = teljes_ut.get(gerinc_utvonal_vag(r['utvonal']))
            if ut is None:
                napl['nem_talalt'].append(azon + ': az útvonal nincs a szakasztáblában')
                continue
            # DT381 (a): a forrásjavított sornál a magyar szöveg a forrás alakját hordozza („26:35”): azt emeli ki
            keres = vers
            if 'forras_javitas' in (r.get('okkod') or '').split(',') and re.fullmatch(r'\d+:\d+', r['nyers']):
                keres = '%s %s' % (vers.rsplit(' ', 1)[0], r['nyers'])
            celok.setdefault(ut, []).append((keres, azon))
            hordozo.add(ut)
    for k in kut_kulcsok:
        ut = kutatoi_szakasz(adat, szotar, strong, k)
        if ut:
            hordozo.add(ut)
    bek = [cim, GERINC_BEVEZETO['Thayer' if szotar == 'Thayer' else 'BDB']]
    if szotar == 'Thayer':
        bek.append('*A magyar szöveg a szakaszonkénti Thayer-fordításból (`adat/forditasok.tsv`, `sz<n>` sorok, #142; '
                   'DT373).*')
    napl['tiltott'] = []
    for ut, jel, hu, _a, forras in ([fej] if fej else []) + szakaszok:
        for alak in tiltott_talalatok(adat.get('tiltott', []), hu):
            napl['tiltott'].append('%s %s (%s): „%s”' % (szotar, jel, forras, alak))
    if fej:
        if fej[2]:
            szov, t, h = kiemel(fej[2], fej_celok)
            napl['kiemelt'] += t
            napl['nem_talalt'] += h
            bek.append('**A szócikk feje (nyelvi háttér).** %s' % szov)
        else:
            napl['nem_talalt'] += [a for _, a in fej_celok]
            bek.append('**A szócikk feje (nyelvi háttér).** > %s %s' % (fej[3], FORDITASRA_VAR))
    lista, talalt, hiany = gerinc_szakasz_lista(szakaszok, hordozo, celok, adat['cimke'], szotar, strong)
    napl['kiemelt'] += talalt
    napl['nem_talalt'] += hiany
    bek.extend(lista)
    if napl['nem_talalt'] or napl['nem_idezett'] or napl['tiltott'] or napl['tartomanyban']:
        reszek = []
        if napl['tiltott']:
            reszek.append('ismert hiány: a magyar szöveg tiltott fordulatot tartalmaz (`%s`): %s; a javítás a '
                          'fordítás újrafuttatása (#142, DT379), a lap a szöveget nem írja át'
                          % (TILTOTT_FORDULATOK_FAJL, '; '.join(napl['tiltott'])))
        if napl['nem_talalt']:
            reszek.append('a szótári példahely a magyar szövegben nem található, kiemelés nincs: %s'
                          % '; '.join(napl['nem_talalt']))
        if napl['nem_idezett']:
            reszek.append('a szótár nem idézi: %s' % ', '.join(napl['nem_idezett']))
        for t in napl['tartomanyban']:
            reszek.append(t)
        bek.append('*ⓘ Kutatói megjegyzés: %s.*' % ' · '.join(reszek))
    forras = BDB_TELJES_FAJL if szotar == 'BDB' else THAYER_TELJES_FAJL
    bek.append('*A teljes szócikk: %s*' % _szonezet_mutato(strong, forras))
    if ctx is not None:
        fl = ctx['fl']
        if szotar == 'BDB':
            for f in (BDB_SZAKASZOK_FAJL, BDB_SZAKASZ_HU_FAJL, BDB_VERS_JELENTES_FAJL, BDB_TELJES_FAJL):
                fl.setdefault(f, set()).add('BDB')
        else:
            for f in (THAYER_SZAKASZOK_FAJL, THAYER_VERS_JELENTES_FAJL, THAYER_TELJES_FAJL, 'adat/forditasok.tsv'):
                fl.setdefault(f, set()).add('Thayer')
        fl.setdefault(SZAKASZ_CIMKE_FAJL, set()).add('projekt_adat')
        if adat.get('tiltott'):
            fl.setdefault(TILTOTT_FORDULATOK_FAJL, set()).add('projekt_adat')
        ctx.setdefault('gerinc_naplo', []).append(napl)
    return bek, napl


def ubs_domensor(strong):
    """A görög szó UBS-doménsora (DT272 (a), DT371): a Louw–Nida-kódok a magyar glosszával, a teljes
    UBS-szócikk nélkül; ahol nincs magyar glossza, az angol és a `fordításra vár` jelölés."""
    jelentesek, _darab = ubs_dntg_adatok()
    lex = jelentesek.get(strong) or {}
    reszek = []
    for lexid, r in lex.items():
        reszek.append('%s %s' % (r['entry_kod'], _dntg_hu('glosszak_hu', strong, lexid, r['entry_kod'], r['glosszak'])))
    if not reszek:
        return '**UBS-domének (Louw–Nida):** %s' % NEM_TARGYALJA
    return '**UBS-domének (Louw–Nida):** %s' % ' · '.join(reszek)


def gerinc_nyelvi_blokk(nyelv, tokenek_ny, ctx):
    """A „Jelentéstartomány” blokk egy nyelvre (a „2. Szótári háttér” nyelvi blokkjának elején)."""
    adat = gerinc_adat()
    szotar = 'Thayer' if nyelv == 'gorog' else 'BDB'
    bek = ['#### Jelentéstartomány (szótári gerinc)']
    for t in tokenek_ny:
        b, _n = gerinc_blokk(adat, szotar, t, ctx.get('sorai') or [], ctx)
        bek.extend(b)
        if nyelv == 'gorog':
            bek.append(ubs_domensor(t))
            ctx['fl'].setdefault(UBS_DNTG_JELENTESEK_FAJL, set()).add('UBS_DNTG')
    return '\n\n'.join(bek)


# A szerepmátrix szűkítése az arany lapon (DT371 1.; (i) az SDBH-doménsor marad; (ii) a BDB-fej a
# gerincben; (iv) a TBESH helyén mutató + egysoros magyar jelentés). A többi szerep változatlan.

def _gerinc_hivatkozas_gerincre(nyelv, n, tokenek_ny, reszek, ctx):
    mit = {('gorog', 2): 'a Thayer-szócikk', ('heber', 2): 'a BDB-szócikk',
           ('heber', 8): 'a BDB-szócikk feje (nyelvi háttér)'}[(nyelv, n)]
    return ['*Hivatkozás: %s a fenti „Jelentéstartomány (szótári gerinc)” blokkban áll (DT371).*' % mit]


def _gerinc_tbesh(nyelv, n, tokenek_ny, reszek, ctx):
    adat = gerinc_adat()
    out = []
    for t in tokenek_ny:
        g = adat['glossza'].get(t)
        rovid = ('%s *(a TBESH rövid jelentése magyarul, `%s`)*' % (g['glossza_hu'], GLOSSZAK_HEBER_HU_FAJL)
                 if g else '*(nincs magyar rövid jelentés a `%s`-ben)*' % GLOSSZAK_HEBER_HU_FAJL)
        out.append('**%s** · %s · a teljes TBESH-szócikk: %s' % (t, rovid, _szonezet_mutato(t, TBESH_TXT_FAJL)))
    ctx['fl'].setdefault(GLOSSZAK_HEBER_HU_FAJL, set()).add('TBESH')
    return out


def _gerinc_tw(nyelv, n, tokenek_ny, reszek, ctx):
    _sorok, idx = tw_szocikkek()
    out = []
    for t in tokenek_ny:
        if nyelv == 'heber':
            out.append('**%s** · %s' % (t, reszek[t]['twot']))
        cikkek = idx.get(t, [])
        if cikkek:
            out.append('**%s** · tW: %s — a szócikkek szövege a szónézetben: %s'
                       % (t, ', '.join('`%s`' % c['tw_id'] for c in cikkek), _szonezet_mutato(t, TW_FAJL)))
            # DT383 (a) (ELLENOR_SZOTARI_GERINC 5.): a lap tW-azonosítókat és a tW-forrásfájlt nevez meg, ezért a tW
            # (CC BY-SA 4.0) az Irodalomban és a kolofon licenctáblájában áll; a szócikk szövege nem kerül a lapra
            ctx['fl'].setdefault(TW_FAJL, set()).add('tW_szocikkek')
        else:
            out.append('**%s** · %s *(tW)*' % (t, NEM_TARGYALJA))
    if nyelv == 'heber':
        ctx['fl'].setdefault('konkordancia/OSHL_lexikalis_index.tsv', set()).add('OSHL')
    return out


def _gerinc_ubs_mutato(nyelv, n, tokenek_ny, reszek, ctx):
    if nyelv == 'gorog':
        # F131.21 (DT383 (a) a Mounce-ra, ELLENOR_SZOTARI_GERINC_2 5.): a mutató a Mounce-ot név szerint megnevezi,
        # ezért a Mounce (MCGED, „redistribution with attribution”) az Irodalomban és a kolofonban áll (a tW útján,
        # F131.11); a glossza szövege nem kerül a lapra
        if any(mcged_sor(t) for t in tokenek_ny):
            ctx['fl'].setdefault(MCGED_FAJL, set()).add('MCGED')
        return ['**%s** · a teljes UBS DNTG-szócikk és a Mounce-glossza a szónézetben: %s; a Louw–Nida-doménsor a '
                'fenti jelentéstartományban áll.' % (t, _szonezet_mutato(t, UBS_DNTG_JELENTESEK_FAJL))
                for t in tokenek_ny]
    mit = 'jelentései' if n == 5 else 'versenkénti jelentése'
    return ['**%s** · az UBS DBH %s a szónézetben: %s' % (t, mit, _szonezet_mutato(t, UBS_DBH_JELENTESEK_FAJL))
            for t in tokenek_ny]


GERINC_SZEREP_EPITO = {
    ('gorog', 2): _gerinc_hivatkozas_gerincre,
    ('heber', 2): _gerinc_hivatkozas_gerincre,
    ('heber', 8): _gerinc_hivatkozas_gerincre,
    ('heber', 1): _gerinc_tbesh,
    ('gorog', 3): _gerinc_tw,
    ('heber', 3): _gerinc_tw,
    ('gorog', 5): _gerinc_ubs_mutato,
    ('heber', 5): _gerinc_ubs_mutato,
    ('heber', 9): _gerinc_ubs_mutato,
}


# ---------------------------------------------------------------------------
# 3. LXX-fordítói döntések (G5)
# ---------------------------------------------------------------------------

_karoli_to_primary_slug = None
_lxx_os_rows_cache = {}
_lxx_os_karoli_idx_cache = {}
_lxx_dontesek_cache = None


def karoli_to_primary_slug():
    """Károli-könyv -> LXX_OS slug; az elsődleges szövegváltozatot LXXOS.ELSODLEGES_SLUG adja
    (F42 / DT-F42f f2)."""
    global _karoli_to_primary_slug
    if _karoli_to_primary_slug is None:
        terkep = {}
        karoli_konyvek = set(LXXOS.BOOK_KEY_TO_KAROLI.values()) | set(LXXOS.ELSODLEGES_SLUG)
        for karoli_book in karoli_konyvek:
            slug = LXXOS.elsodleges_slug(karoli_book)
            if slug:
                terkep[karoli_book] = slug
        _karoli_to_primary_slug = terkep
    return _karoli_to_primary_slug


def lxx_os_sorok(slug):
    if slug not in _lxx_os_rows_cache:
        path = os.path.join(LXX_OS_DIR, '%s.tsv' % slug)
        _lxx_os_rows_cache[slug] = L.read_tsv_skip_comments(path) if os.path.exists(path) else []
    return _lxx_os_rows_cache[slug]


def lxx_os_karoli_index(slug):
    if slug not in _lxx_os_karoli_idx_cache:
        idx = {}
        for r in lxx_os_sorok(slug):
            if r.get('igehely_karoli'):
                idx.setdefault(r['igehely_karoli'], []).append(r)
        _lxx_os_karoli_idx_cache[slug] = idx
    return _lxx_os_karoli_idx_cache[slug]


# F08: csak a kiadott (biztos, ill. az F08 előtti, skála nélküli) és a
# megjelenítésre szánt tipusú sorok jelennek meg; a `valoszinu`/`nyitott`
# sorok "kutatói azonosítás függőben" jelöléssel jelennek meg (DT23), a
# `nincs_heber_kulcsszo` (`nem_alkalmazhato`) sorok saját címkéje külön
# tétel (N-F08b; adat/SEMA.md 2.11). A szűrő a 3. (LXX) blokkra
# és a rokon_szavak_strongok-on át a "Rokon szavak" blokkra is hat.
LXX_DONTES_MEGJELENO_BIZONYOSSAG = {'', 'biztos'}
LXX_DONTES_MEGJELENO_TIPUS = {'eltero_forditas', 'lxx_minusz'}


def lxx_dontesek_index():
    global _lxx_dontesek_cache
    if _lxx_dontesek_cache is None:
        _, sorok = G.tsv_beolvas(LXX_DONTESEK_TSV)
        idx = {}
        for r in sorok:
            if (r.get('bizonyossag') or '').strip() not in LXX_DONTES_MEGJELENO_BIZONYOSSAG:
                continue
            if (r.get('tipus') or '').strip() not in LXX_DONTES_MEGJELENO_TIPUS:
                continue
            idx.setdefault(r['igehely'], []).append(r)
        _lxx_dontesek_cache = idx
    return _lxx_dontesek_cache


def lxx_os_strong_normalizalt(nyers_strong):
    """Az LXX_OS 'strong' oszlopa csupasz szám ('1941'), nem a STRONG-típus
    ('G1941') -- ez a normalizáló a kettő közötti eltérést hidalja át
    (K3/G6/G5)."""
    nyers_strong = (nyers_strong or '').strip()
    if not nyers_strong.isdigit():
        return ''
    return 'G%04d' % int(nyers_strong)


_LXX_IGEHELY_VERS_RE = re.compile(r'(\d+):(\d+)$')


def lxx_igehely_magyar(lxx_ref, karoli_konyv, karoli_fej, karoli_vers):
    """A nyers LXX-igehely (angol könyvnév, pl. 'Genesis 4:26' vagy
    'Psalms (LXX) 115:8') saját (fejezet:vers) számozása, magyar könyv-
    rövidítéssel; '(LXX)' jelöléssel közvetlenül a könyvnév után, ha a
    számozás eltér a Károli-céltól (pl. 'Zsolt(LXX) 114:4'), egyezéskor
    jelölés nélkül (V2.6a pont 4). Ugyanez a függvény alakítja az
    `LXX_OS` sorok és az `lxx_dontesek.tsv` kutatói sorainak
    `lxx_igehely` mezőjét is — a tábla mezője angol marad, csak a
    megjelenítés magyar (V2.6b)."""
    m = _LXX_IGEHELY_VERS_RE.search(lxx_ref or '')
    if not m:
        return lxx_ref or EM_DASH
    lxx_fej, lxx_vers = int(m.group(1)), int(m.group(2))
    if lxx_fej == karoli_fej and lxx_vers == karoli_vers:
        return '%s %d:%d' % (karoli_konyv, karoli_fej, karoli_vers)
    return '%s(LXX) %d:%d' % (karoli_konyv, lxx_fej, lxx_vers)


def gorog_megfelelo_szoveg(r):
    strong = lxx_os_strong_normalizalt(r.get('strong'))
    lk = lemma_kiejtes(strong) if strong else None
    if lk:
        kiejtes = lk[1]
    else:
        kiejtes = gorog_magyaros(gepi_atiras(r['lemma'])) + ' *(gépi átírás)*'
    return '%s (%s, %s%s)' % (r['szoalak'], r['lemma'], kiejtes, ' %s' % strong if strong else '')


def blokk_lxx(m, sorai, tokenek):
    osz_sorai = [s for s in sorai if G.konyv_teszamentum(G.konyv_token(s['igehely'])) == 'ÓSZ']
    if not osz_sorai:
        hatokor = ('Ez a blokk a `[ID: %s]` motívum ÓSZ-i előfordulásait vetné össze az '
                    '`LXX_OS`-szel.' % m['id'])
        torzs = 'A motívumnak nincs ÓSZ-i előfordulása, ezért az LXX-fordítói döntések blokk üres.'
        return _lexikon_blokk(m['id'], 'lxx', [], [], hatokor, torzs), []

    gorog_tokenek = {t for t in tokenek if t.startswith('G')}
    terkep = karoli_to_primary_slug()
    dontesek_idx = lxx_dontesek_index()

    fejlec = ['| Igehely (Károli) | LXX-igehely | Héber kulcsszó | Görög megfelelő | Egyezés | Forrás |',
              '|---|---|---|---|---|---|']
    tabla_sorok = list(fejlec)
    szamlalo = {'egyező': 0, 'eltérő': 0, 'LXX-minusz': 0, 'kutatói azonosítás függőben': 0, 'szamozas_elteres': 0}
    forras_fajlok = set()

    for s in osz_sorai:
        strong_field = s.get('strong') or ''
        heber_tokenek = [t.strip() for t in strong_field.split('+') if t.strip().startswith('H')]

        for vers in igehely_lista(s['igehely']):
            konyv, karoli_fej, karoli_vers = L.parse_igehely(vers)
            slug = terkep.get(konyv)
            heber_kulcsszo = EM_DASH
            for ht in heber_tokenek:
                talalat = kiejtes_ehhez(vers, ht)
                if talalat:
                    ragozott, kiejtes, _f = talalat
                    heber_kulcsszo = '%s (%s)' % (ragozott, kiejtes)
                    break

            if slug is None:
                tabla_sorok.append('| %s | %s | %s | %s | %s | %s |' % (
                    vers, EM_DASH, heber_kulcsszo, EM_DASH, 'nincs LXX_OS-könyv', EM_DASH))
                continue
            forras_fajlok.add('konkordancia/LXX_OS/%s.tsv' % slug)

            sorai_ehhez_vershez = lxx_os_karoli_index(slug).get(vers, [])
            if not sorai_ehhez_vershez:
                szamlalo['szamozas_elteres'] += 1
                tabla_sorok.append('| %s | %s | %s | %s | %s | LXX_OS |' % (
                    vers, EM_DASH, heber_kulcsszo, EM_DASH, 'szamozas_elteres'))
                continue

            lxx_igehely = lxx_igehely_magyar(sorai_ehhez_vershez[0].get('igehely_lxx'), konyv, karoli_fej, karoli_vers)

            egyezo = [r for r in sorai_ehhez_vershez
                      if gorog_tokenek and lxx_os_strong_normalizalt(r.get('strong')) in gorog_tokenek]
            if egyezo:
                szamlalo['egyező'] += 1
                gm = gorog_megfelelo_szoveg(egyezo[0])
                tabla_sorok.append('| %s | %s | %s | %s | egyező | LXX_OS |' % (
                    vers, lxx_igehely, heber_kulcsszo, gm))
                continue

            kutatoi = dontesek_idx.get(vers, [])
            if kutatoi:
                r = kutatoi[0]
                if r.get('lxx_igehely'):
                    dontesek_lxx_igehely = lxx_igehely_magyar(r['lxx_igehely'], konyv, karoli_fej, karoli_vers)
                else:
                    dontesek_lxx_igehely = lxx_igehely
                if (r.get('tipus') or '').strip() == 'lxx_minusz':
                    szamlalo['LXX-minusz'] += 1
                    gm = 'nincs megfelelő a görögben (LXX-minusz)'
                    egyezes_cimke = 'LXX-minusz'
                else:
                    szamlalo['eltérő'] += 1
                    gorog_strong = (r.get('gorog_strong') or '').strip()
                    lk = lemma_kiejtes(gorog_strong) if gorog_strong else None
                    if lk:
                        kiejtes = lk[1]
                    else:
                        kiejtes = gorog_magyaros(gepi_atiras(r.get('gorog_lemma') or '')) + ' *(gépi átírás)*'
                    gm = '%s (%s%s)' % (r.get('gorog_lemma') or EM_DASH, kiejtes,
                                         ' %s' % gorog_strong if gorog_strong else '')
                    egyezes_cimke = 'eltérő'
                tabla_sorok.append('| %s | %s | %s | %s | %s | adat/lxx_dontesek.tsv |' % (
                    vers, dontesek_lxx_igehely, heber_kulcsszo, gm, egyezes_cimke))
                continue

            szamlalo['kutatói azonosítás függőben'] += 1
            tabla_sorok.append('| %s | %s | %s | %s | kutatói azonosítás függőben | LXX_OS |' % (
                vers, lxx_igehely, heber_kulcsszo, EM_DASH))

    torzs = '\n'.join(tabla_sorok)
    torzs += ('\n\n*Összesítés: egyező=%d, eltérő=%d, LXX-minusz=%d, kutatói azonosítás függőben=%d, '
              'szamozas_elteres=%d.*'
              % (szamlalo['egyező'], szamlalo['eltérő'], szamlalo['LXX-minusz'],
                 szamlalo['kutatói azonosítás függőben'], szamlalo['szamozas_elteres']))

    hatokor = ('Ez a blokk a `[ID: %s]` motívum ÓSZ-i előfordulásait veti össze az `LXX_OS`-szel '
               '(G5), soronként a Károli-vers minden versére.' % m['id'])
    dontesek_hasznalt = bool(szamlalo['eltérő'] or szamlalo['LXX-minusz'])
    forras_lista = sorted(forras_fajlok) + (['adat/lxx_dontesek.tsv'] if dontesek_hasznalt else [])
    blokk_szoveg = _lexikon_blokk(m['id'], 'lxx', sorted(set(forras_lista)),
                                   [LC('LXX_OS'), LC('projekt_adat')], hatokor, torzs)
    forras_licenc_parok = [(f, LC('LXX_OS')) for f in sorted(forras_fajlok)]
    if dontesek_hasznalt:
        forras_licenc_parok.append(('adat/lxx_dontesek.tsv', LC('projekt_adat')))
    return blokk_szoveg, forras_licenc_parok


# ---------------------------------------------------------------------------
# 4. Kereszthivatkozások (TSK + Károli-KH)
# ---------------------------------------------------------------------------

_tsk_by_igehely = None
_kh_by_step = None


def tsk_index():
    global _tsk_by_igehely
    if _tsk_by_igehely is None:
        # F114: a TSK KJV-kulcsú; a kulcsot (forrás és cél) a tsk_kulcs váltja Károli-versszámra.
        # A tartomány-igehelyre (N-F114b) ez az index sem keres.
        _tsk_by_igehely = TK.karoli_index(L.load_tsk())
    return _tsk_by_igehely


def kh_index():
    global _kh_by_step
    if _kh_by_step is None:
        idx = {}
        for r in L.load_karoli_kh():
            idx.setdefault(r['Igehely'], []).append(r)
        _kh_by_step = idx
    return _kh_by_step


def blokk_kereszthivatkozasok(m, sorai, konyv_sorrend, hianyzo_konyvek):
    sorai_rendezve = sorted(
        sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))

    bekezdesek = []
    nem_vizsgalhato = []
    talalat_szam = 0

    for s in sorai_rendezve:
        igehely = s['igehely']
        try:
            step = L.to_step(igehely)
        except ValueError:
            nem_vizsgalhato.append(igehely)
            continue

        tsk_talalatok = sorted(
            [r for r in tsk_index().get(igehely, []) if int(r['Votes']) >= 15],
            key=lambda r: -int(r['Votes'])
        )
        kh_talalatok = kh_index().get(step, [])
        if not tsk_talalatok and not kh_talalatok:
            continue

        sorok = ['#### %s' % igehely]
        for r in tsk_talalatok:
            sorok.append('- TSK: %s (Votes: %s)' % (karoli_colon(r['Kapcsolódó igehely magyar megjelenítése']), r['Votes']))
            talalat_szam += 1
        for r in kh_talalatok:
            sorok.append('- Károli-KH: %s' % karoli_colon(r['Kapcsolódó igehely magyar megjelenítése']))
            talalat_szam += 1
        bekezdesek.append('\n'.join(sorok))

    torzs_reszek = list(bekezdesek)
    if nem_vizsgalhato:
        torzs_reszek.append('*Versenkénti kereséssel nem vizsgálható: %s.*' % ', '.join(nem_vizsgalhato))
    torzs = '\n\n'.join(torzs_reszek) if torzs_reszek else 'Nincs TSK/Károli-KH találat ehhez a motívumhoz.'

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehelyét veti össze a TSK (Votes ≥ 15) és a '
               'Károli-KH táblával; %d igehely ad legalább egy találatot (%d találat összesen), '
               '%d igehely versenkénti kereséssel nem vizsgálható.'
               % (m['id'], len(sorai_rendezve), len(bekezdesek), talalat_szam, len(nem_vizsgalhato)))
    blokk_szoveg = _lexikon_blokk(
        m['id'], 'kereszthivatkozasok',
        ['konkordancia/TSK_kereszthivatkozasok.tsv', 'konkordancia/Karoli_kereszthivatkozasok.tsv'],
        [LC('TSK'), LC('Karoli_KH')], hatokor, torzs
    )
    forras_licenc_parok = [
        ('konkordancia/TSK_kereszthivatkozasok.tsv', LC('TSK')),
        ('konkordancia/Karoli_kereszthivatkozasok.tsv', LC('Karoli_KH')),
    ]
    return blokk_szoveg, forras_licenc_parok


# ---------------------------------------------------------------------------
# 5. Kapcsolatok
# ---------------------------------------------------------------------------

_kapcsolatok_cache = None


def kapcsolatok_sorok():
    global _kapcsolatok_cache
    if _kapcsolatok_cache is None:
        _, sorok = G.tsv_beolvas(KAPCSOLATOK_TSV)
        _kapcsolatok_cache = sorok
    return _kapcsolatok_cache


def blokk_kapcsolatok(m, konyv_sorrend, hianyzo_konyvek):
    sorok_ehhez = [r for r in kapcsolatok_sorok() if r['id'] == m['id']]

    if not sorok_ehhez:
        torzs = 'Nincs kapcsolat-sor a `kapcsolatok.tsv`-ben ehhez a motívumhoz.'
        hatokor = 'Ez a blokk a `[ID: %s]` motívum kapcsolat-sorait fedné a `kapcsolatok.tsv`-ből; 0 sor.' % m['id']
        return _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], [LC('projekt_adat')], hatokor, torzs), \
            [('adat/kapcsolatok.tsv', LC('projekt_adat'))]

    igehelyek = _sorted_unique(list(
        {r['forras_igehely'] for r in sorok_ehhez} | {r['cel_igehely'] for r in sorok_ehhez}
    ))
    igehelyek.sort(key=lambda ige: G.igehely_rendezo_kulcs(ige, konyv_sorrend, hianyzo_konyvek))
    node_id = {ige: 'n%d' % (i + 1) for i, ige in enumerate(igehelyek)}

    fejlec = ['| Forrás | Cél | Típus | Funkció | Bizonyosság | PaRDeS-szint |',
              '|---|---|---|---|---|---|']
    tabla_sorok = list(fejlec)
    for r in sorok_ehhez:
        tabla_sorok.append('| %s | %s | %s | %s | %s | %s |' % (
            r['forras_igehely'], r['cel_igehely'], r['tipus'], r['funkcio'],
            r['bizonyossag'], r['pardes_szint']))

    mermaid = ['```mermaid', 'graph LR']
    for ige in igehelyek:
        mermaid.append('    %s["%s"]' % (node_id[ige], ige))
    for r in sorok_ehhez:
        mermaid.append('    %s -->|%s| %s' % (
            node_id[r['forras_igehely']], r['tipus'], node_id[r['cel_igehely']]))
    mermaid.append('```')

    torzs = '\n'.join(tabla_sorok) + '\n\n<details>\n<summary>Mermaid-ábra</summary>\n\n' + \
        '\n'.join(mermaid) + '\n\n</details>'
    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d kapcsolat-sorát fedi a `kapcsolatok.tsv`-ből, '
               '%d igehely-csomóponttal.' % (m['id'], len(sorok_ehhez), len(igehelyek)))
    blokk_szoveg = _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], [LC('projekt_adat')], hatokor, torzs)
    return blokk_szoveg, [('adat/kapcsolatok.tsv', LC('projekt_adat'))]


# ---------------------------------------------------------------------------
# 5/b. Kapcsolódó motívumok (DT-F127b (α), #127) -- a motivum_kapcsolatok.tsv
# sorai mindkét érintett motívum lapján; a döntésre váró motívumközi jelöltek
# (jeloltek.tsv, jelolt_tipus=motivumkozi, nyitva) csak számként.
# ---------------------------------------------------------------------------

SZAKASZ_5B = '## 5/b. Kapcsolódó motívumok'
MOTIVUM_KAPCSOLATOK_TSV = os.path.join(ADAT, 'motivum_kapcsolatok.tsv')
KAPCSOLODO_FORRASOK = ('adat/motivum_kapcsolatok.tsv', 'adat/jeloltek.tsv')


def motivum_kapcsolatok_sorok():
    if not os.path.exists(MOTIVUM_KAPCSOLATOK_TSV):
        return []
    return G.tsv_beolvas(MOTIVUM_KAPCSOLATOK_TSV)[1]


def motivumkozi_jeloltek():
    _, sorok = G.tsv_beolvas(JELOLTEK_TSV)
    return [r for r in sorok if r.get('jelolt_tipus') == 'motivumkozi']


def kapcsolodo_torzs(motivum_id, mk_sorok, mk_jeloltek):
    """A blokk törzse (tiszta függvény): a motívum kapcsolat-sorai a másik
    motívum szemszögéből, és a döntésre váró motívumközi jelöltek száma."""
    sajat = []
    for r in mk_sorok:
        if r['id_a'] == motivum_id:
            sajat.append((r['id_b'], r['igehely_a'], r['igehely_b'], r))
        elif r['id_b'] == motivum_id:
            sajat.append((r['id_a'], r['igehely_b'], r['igehely_a'], r))
    out = []
    if sajat:
        out += ['| Kapcsolódó motívum | Itt | Ott | Típus | Funkció | Bizonyosság | PaRDeS-szint | Indoklás |',
                '|---|---|---|---|---|---|---|---|']
        for masik, itt, ott, r in sorted(sajat, key=lambda x: (x[0], x[1], x[2])):
            out.append('| [%s](%s_TUDOMANYOS.md) | %s | %s | %s | %s | %s | %s | %s |' % (
                masik, masik, itt, ott, r['tipus'], _cella(r['funkcio'] or EM_DASH), r['bizonyossag'],
                r['pardes_szint'] or EM_DASH, _cella(r['indoklas'] or EM_DASH)))
    else:
        out.append('A motívumhoz nincs rögzített motívumközi kapcsolat a `motivum_kapcsolatok.tsv`-ben.')
    nyitott = {}
    for j in mk_jeloltek:
        if j.get('dontes') != 'nyitva':
            continue
        if j['id'] == motivum_id:
            masik = j.get('cel_id', '')
        elif j.get('cel_id') == motivum_id:
            masik = j['id']
        else:
            continue
        nyitott[masik] = nyitott.get(masik, 0) + 1
    if nyitott:
        out += ['', '*Döntésre váró motívumközi jelölt (`jeloltek.tsv`, `nyitva`): %d — %s.*' % (
            sum(nyitott.values()), ', '.join('%s: %d' % (k, nyitott[k]) for k in sorted(nyitott)))]
    return '\n'.join(out)


def blokk_kapcsolodo(m):
    torzs = kapcsolodo_torzs(m['id'], motivum_kapcsolatok_sorok(), motivumkozi_jeloltek())
    torzs += ('\n\n*Proveniencia: `scope=id:%s | forras=%s | ts=%s`*'
              % (m['id'], '+'.join(KAPCSOLODO_FORRASOK), G.TS))
    hatokor = ('Ez a blokk a `[ID: %s]` motívum motívumközi kapcsolatait adja a `motivum_kapcsolatok.tsv`-ből '
               '(minden sor mögött beépített motívumközi jelölt áll, DT277); a sor mindkét érintett '
               'motívum lapján megjelenik.' % m['id'])
    return _lexikon_blokk(m['id'], 'kapcsolodo', list(KAPCSOLODO_FORRASOK), [LC('projekt_adat')], hatokor, torzs)


def szakasz_5b_beszur(fajl_szoveg, m, blokk):
    """DT-F127b (α): ha a lapon még nincs „5/b.” szakasz, a 6. Értelmezés (az
    `ertelmezes` rés fejléce) elé szúrja a szakaszcímet és a generált blokkot."""
    if SZAKASZ_5B in fajl_szoveg:
        return fajl_szoveg
    sorok = res_forras_sorok()
    for res in ('alatamasztas', 'ertelmezes'):
        if (m['id'], res) not in sorok:
            raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], res))
    a_i, a_talalt = _boundary_index(fajl_szoveg, sorok[(m['id'], 'alatamasztas')]['fejlec'], 0, 'alatamasztas')
    e_i, _ = _boundary_index(fajl_szoveg, sorok[(m['id'], 'ertelmezes')]['fejlec'],
                             a_i + len(a_talalt), 'ertelmezes')
    return fajl_szoveg[:e_i] + SZAKASZ_5B + '\n\n' + blokk + '\n\n' + fajl_szoveg[e_i:]


# ---------------------------------------------------------------------------
# 8. Irodalom és idézés
# ---------------------------------------------------------------------------

FAJL_TELJES_NEV = {
    'konkordancia/BDB_teljes_unabridged.tsv':
        'BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906)',
    'konkordancia/TBESG.txt': 'TBESG (Tyndale Brief lexicon of Extended Strongs for Greek)',
    'konkordancia/TBESH.txt': 'TBESH (Tyndale Brief lexicon of Extended Strongs for Hebrew)',
    'konkordancia/_nyers/tbesh/TBESH_konszolidalt.tsv': 'TBESH (Tyndale Brief lexicon of Extended Strongs for Hebrew)',
    'konkordancia/Thayer_teljes.tsv': "Thayer (Thayer's Greek-English Lexicon of the New Testament)",
    'konkordancia/UBS_DNTG_jelentesek.tsv': 'UBS (UBS Dictionary of New Testament Greek — Louw–Nida szemantikai domének)',
    'konkordancia/MCGED_teljes.tsv': 'Mounce (Mounce Concise Greek-English Dictionary)',
    'konkordancia/tW_szocikkek.tsv': 'tW (Translation Words — unfoldingWord)',
    'konkordancia/BDB_etimologia_kezi_hatarok.tsv': 'BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906)',
    'konkordancia/SECE_G_teljes.tsv': "SECE (Strong's Exhaustive Concordance, Enhanced)",
    'konkordancia/SECE_H_teljes.tsv': "SECE (Strong's Exhaustive Concordance, Enhanced)",
    'konkordancia/UBS_DBH_jelentesek.tsv': 'UBS DBH (UBS Dictionary of Biblical Hebrew — Semantic Dictionary of Biblical Hebrew)',
    'konkordancia/UBS_DBH_referenciak.tsv': 'UBS DBH (UBS Dictionary of Biblical Hebrew — Semantic Dictionary of Biblical Hebrew)',
    'konkordancia/UBS_DNTG_referenciak.tsv': 'UBS (UBS Dictionary of New Testament Greek — Louw–Nida szemantikai domének)',
    'konkordancia/SDBH_domenek.tsv': 'SDBH (Semantic Dictionary of Biblical Hebrew)',
    'konkordancia/SDGNT_domenek.tsv': 'SDGNT (Semantic Dictionary of Biblical Greek)',
    'konkordancia/OSHL_lexikalis_index.tsv': 'OSHL (Open Scriptures Hebrew Lexicon) — csak TWOT-szám',
    'konkordancia/TSK_kereszthivatkozasok.tsv': 'TSK (Treasury of Scripture Knowledge)',
    'konkordancia/LSJ_teljes.tsv': 'LSJ (Liddell-Scott-Jones, A Greek-English Lexicon)',
}
ADATFORRAS_FAJLOK = {'konkordancia/Karoli_1908.tsv', 'konkordancia/Karoli_kereszthivatkozasok.tsv',
                      'adat/lexikon_hivatkozasok.tsv', 'konkordancia/Karoli_versmegfeleltetes.tsv',
                      'konkordancia/LXX_versszintu_parok.tsv', TAHOT_KIVONAT_FAJL}


def _teljes_nev(fajl):
    if fajl in FAJL_TELJES_NEV:
        return FAJL_TELJES_NEV[fajl]
    if fajl.startswith('konkordancia/LXX_OS/'):
        return 'LXX (Septuaginta — lxx-morph + GreekWordList szövegkorpusz)'
    return None


def _adatforras(fajl):
    return fajl.startswith('adat/') or fajl in ADATFORRAS_FAJLOK


def blokk_idezes(m, fajl_licenc_blokk_lista):
    """A szótárak a lexikon_hivatkozasok.tsv-ben ténylegesen idézett
    forrásfájljuk (nem maga a lexikon_hivatkozasok.tsv) szerint, teljes
    névvel jelennek meg a 'Felhasznált szótárak' alatt; egy szótár EGY
    sorban (a fájljai zárójelben felsorolva), az adat/*.tsv és a Károli-
    fájlok (a lexikon_hivatkozasok.tsv is) az 'Adatforrások' alatt
    maradnak (V2.7-előtti javítás)."""
    per_fajl = {}
    for fajl, licenc, _blokk_nev in fajl_licenc_blokk_lista:
        per_fajl.setdefault(fajl, set()).add(licenc)

    github_url = ('https://github.com/Basesoft777/Bible-Study/blob/main/lexikon/%s_TUDOMANYOS.md'
                  % m['id'])
    hogyan = [
        '**Hogyan hivatkozz:**',
        '- ID: `%s`' % m['id'],
        '- Cím: %s' % m.get('cim', EM_DASH),
        '- Státusz: %s (`%s`, %s)' % (m.get('statusz', EM_DASH), m.get('statusz_verzio', ''), m.get('statusz_datum', '')),
        '- Generálva: %s' % G.TS,
        '- Fájl: `%s`' % github_url,
    ]

    szotar_fajlok = {}
    szotar_licenc = {}
    adat_fajlok = []
    beazonositatlan = []
    for fajl in sorted(per_fajl):
        nev = _teljes_nev(fajl)
        if nev:
            szotar_fajlok.setdefault(nev, set()).add(fajl)
            szotar_licenc.setdefault(nev, set()).update(per_fajl[fajl])
        elif _adatforras(fajl):
            adat_fajlok.append(fajl)
        else:
            beazonositatlan.append(fajl)

    szotarak = ['**Felhasznált szótárak:**']
    for nev in sorted(szotar_fajlok):
        fajlok_felsorolas = ', '.join('`%s`' % f for f in sorted(szotar_fajlok[nev]))
        licencek = ', '.join(sorted(szotar_licenc[nev]))
        szotarak.append('- %s (%s, %s)' % (nev, fajlok_felsorolas, licencek))

    adatforrasok = ['**Adatforrások:**']
    for fajl in adat_fajlok + beazonositatlan:
        licencek = ', '.join(sorted(per_fajl[fajl]))
        adatforrasok.append('- `%s` (%s)' % (fajl, licencek))

    torzs = '\n'.join(hogyan) + '\n\n' + '\n'.join(szotarak) + '\n\n' + '\n'.join(adatforrasok)
    hatokor = ('Ez a blokk a `[ID: %s]` motívum hivatkozási adatait, a ténylegesen felhasznált '
               'szótárakat (teljes névvel, forrásfájlonként) és az adatforrásokat adja '
               '(G9, LEXV2_3-ig szűkítve).' % m['id'])
    return _lexikon_blokk(m['id'], 'idezes', [], [LC('projekt_adat')], hatokor, torzs)


# ---------------------------------------------------------------------------
# Kolofon (régi 0. Metaadatok + 9. Források és licencek összevonva)
# ---------------------------------------------------------------------------

# --- F09 S2.7: kötelező forrásmegjelölések (F05 S11) ---

# A TWOT csak szám-hivatkozás (D19): a mű megnevezése kötelező, a szövegét a render nem idézi.
TWOT_MEGJELOLES = ('TWOT: Theological Wordbook of the Old Testament — csak a szócikk száma áll hivatkozásként '
                   '(az OSHL-indexből, Open Scriptures Hebrew Bible Project), a mű szövegét a lexikonoldal nem idézi.')
# unfoldingWord Translation Words (CC BY-SA 4.0): a forrásmegjelölés szó szerint; a származékos szövegből a
# védjegy elmarad; a módosítást jelezni kell (tW_README.md, a LICENSE.md szó szerinti idézete).
TW_MEGJELOLES = ('Translation Words (tW), CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). '
                 'The original work by unfoldingWord is available from unfoldingword.org/utw. '
                 'Módosítás: a szócikkek szövegét a lexikonoldal idézőblokkba tördelve közli (a forrás `\\n` '
                 'sortörés-jelölései valódi sortörésre cserélve), egyébként változatlanul; a magyar fordítás '
                 '(ahol van) származékos munka, ugyanazon CC BY-SA 4.0 licenc alatt.')
# F131.17 (ELLENOR_SZOTARI_GERINC_2 1.): a szótári gerinces lap a tW-ből csak a szócikkek azonosítóit és a
# forrásfájlt nevezi meg (szónézet-mutató, `_gerinc_tw`); a „Módosítás” mondat ezt a tényleges felhasználást mondja.
TW_MEGJELOLES_MUTATO = ('Translation Words (tW), CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). '
                        'The original work by unfoldingWord is available from unfoldingword.org/utw. '
                        'Felhasználás: a lexikonoldal a szócikkek azonosítóit és a forrásfájlt nevezi meg a '
                        'szónézet mutatójaként; a szócikkek szövegét nem közli.')
FAJL_MEGJELOLES_KULCS = {
    'konkordancia/UBS_DBH_jelentesek.tsv': 'UBS_DBH', 'konkordancia/UBS_DBH_referenciak.tsv': 'UBS_DBH',
    'konkordancia/UBS_DNTG_jelentesek.tsv': 'UBS_DNTG', 'konkordancia/UBS_DNTG_referenciak.tsv': 'UBS_DNTG',
    'konkordancia/tW_szocikkek.tsv': 'tW_szocikkek',
    'konkordancia/OSHL_lexikalis_index.tsv': 'OSHL',
    'konkordancia/LXX_versszintu_parok.tsv': 'LXX_versszintu_parok',
    'konkordancia/Karoli_versmegfeleltetes.tsv': 'Karoli_versmegfeleltetes',
    TAHOT_KIVONAT_FAJL: 'TAHOT',  # F131.27 (ELLENOR_SZOTARI_GERINC_3 2.): a STEPBible-megjelölés (licencek.tsv)
}


def kotelezo_megjeloles(kulcs, tw_szoveg_kozolve=True):
    """A dataset kötelező forrásmegjelölése: az UBS-nél az adat/licencek.tsv `kotelezo_megjeloles` mezője
    (a ©-mondat szó szerint), a tW-nél és a TWOT-nál a fenti állandó. A tW-nél a `tw_szoveg_kozolve` dönt:
    ha a lap a szócikkek szövegét közli, a módosítást jelző mondat; ha csak azonosítót, a mutató-mondat."""
    if kulcs == 'tW_szocikkek':
        return TW_MEGJELOLES if tw_szoveg_kozolve else TW_MEGJELOLES_MUTATO
    if kulcs == 'OSHL':
        return TWOT_MEGJELOLES
    szoveg = licenc_sor(kulcs).get('kotelezo_megjeloles') or ''
    if not szoveg:
        raise SystemExit('HIBA: üres `kotelezo_megjeloles` az adat/licencek.tsv `%s` során' % kulcs)
    return szoveg


def megjeloles_reszek(szoveg):
    """Egy kötelező megjelölés önálló mondatai: a licencsor a több forrás megjelölését „.; ” határral
    fűzi össze (pl. `lxx-morph, … lxx-morph.; Data created by www.STEPBible.org …`). A határnál bont,
    a mondatok szövege szó szerint marad."""
    return [r.strip() for r in re.split(r'(?<=\.);\s+', szoveg) if r.strip()]


def kolofon_naplo_cella(motivum_id):
    """A Kolofon „Kereszthivatkozás-napló” cellája. A nem migrált motívumnál
    a `tematikus_lezart/naplok/` alatti napló; a migrált motívumnál (F11 M3,
    DT-F11a) a régi napló az `archivum/[ID]/` alatt áll, a minősítés pedig a
    `jeloltek.tsv`-ből generált -- a cella ezt mondja ki, nem a megszűnt utat."""
    naplo_fajlnev = G.ID_NAPLO_TERKEP.get(motivum_id)
    if not naplo_fajlnev:
        return EM_DASH
    if os.path.exists(os.path.join(ROOT, 'tematikus_lezart', 'naplok', naplo_fajlnev)):
        return '`tematikus_lezart/naplok/%s`' % naplo_fajlnev
    archiv = 'archivum/%s/%s' % (motivum_id, naplo_fajlnev)
    if os.path.exists(os.path.join(ROOT, *archiv.split('/'))):
        return ('generált (`adat/jeloltek.tsv`); a régi napló archívum: `%s`' % archiv)
    return EM_DASH


def blokk_kolofon(m, fajl_licenc_blokk_lista, tw_szoveg_kozolve=True):
    forras_study_sorok = [s.strip() for s in (m.get('forras_study') or '').split(';') if s.strip()]
    forras_study_cella = '<br>'.join('`%s`' % s for s in forras_study_sorok) if forras_study_sorok else EM_DASH

    naplo_cella = kolofon_naplo_cella(m['id'])
    statusz_cella = '%s (`%s`, %s)' % (m['statusz'], m.get('statusz_verzio', ''), m.get('statusz_datum', ''))

    metaadat_sorok = [
        '| Mező | Érték |',
        '|---|---|',
        '| ID | `%s` |' % m['id'],
        '| Rövid UI-címke | %s |' % m.get('ui_cimke', EM_DASH),
        '| Teljes cím | %s |' % m.get('cim', EM_DASH),
        '| Téma | %s |' % m.get('tema', EM_DASH),
        '| PaRDeS-szint | %s |' % m.get('pardes_szint', EM_DASH),
        '| Státusz | %s |' % statusz_cella,
        '| Azonosság típusa | %s |' % m.get('azonossag_tipusa', EM_DASH),
        '| Negatív kritérium | %s |' % m.get('negativ_kriterium', EM_DASH),
        '| Fölérendelt fogalom | %s |' % m.get('folerendelt_fogalom', EM_DASH),
        '| Forrás-study | %s |' % forras_study_cella,
        '| Kereszthivatkozás-napló | %s |' % naplo_cella,
        '| Sablon-megfelelőség | %s |' % m.get('sablon_verzio', EM_DASH),
    ]

    per_fajl = {}
    for fajl, licenc, blokk_nev in fajl_licenc_blokk_lista:
        rekord = per_fajl.setdefault(fajl, {'licenc': set(), 'blokkok': set()})
        rekord['licenc'].add(licenc)
        rekord['blokkok'].add(blokk_nev)

    forras_fejlec = ['| Forrás | Fájl | Licenc | Blokk |', '|---|---|---|---|']
    forras_sorok = list(forras_fejlec)
    tabla_licencek = set()
    for fajl in sorted(per_fajl):
        rekord = per_fajl[fajl]
        licenc = ', '.join(sorted(rekord['licenc']))
        blokkok = ', '.join(sorted(rekord['blokkok']))
        tabla_licencek.update(rekord['licenc'])
        forras_sorok.append('| `%s` | `%s` | %s | %s |' % (os.path.basename(fajl), fajl, licenc, blokkok))

    megjelolesek = []
    if LC('MCGED') in tabla_licencek:
        megjelolesek.append('*%s*' % MOUNCE_MEGJELOLES)
    if any(os.path.basename(f) == 'LSJ_teljes.tsv' for f in per_fajl):
        megjelolesek.append('*%s*' % lsj_forrasmegjeloles())
    # F09 S2.7 (F05 S11): a kötelező forrásmegjelölések szó szerint. Egy licencsor több megjelölést is
    # hordozhat („.; ” határral, pl. lxx-morph + STEPBible): mindegyik külön sorba kerül, és egyszer áll.
    for kulcs in sorted({FAJL_MEGJELOLES_KULCS[f] for f in per_fajl if f in FAJL_MEGJELOLES_KULCS}):
        for resz in megjeloles_reszek(kotelezo_megjeloles(kulcs, tw_szoveg_kozolve)):
            szoveg = '*%s*' % resz
            if szoveg not in megjelolesek:
                megjelolesek.append(szoveg)

    torzs = '\n'.join(metaadat_sorok) + '\n\n---\n\n' + '\n'.join(forras_sorok)
    if megjelolesek:
        torzs += '\n\n' + '\n\n'.join(megjelolesek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum törzsadatait (`motivumok.tsv`) és a lexikon-oldalon '
               'ténylegesen felhasznált forrásokat sorolja fel.' % m['id'])
    return _lexikon_blokk(m['id'], 'kolofon', sorted(set(per_fajl) | {'adat/motivumok.tsv'}),
                           sorted(tabla_licencek | {LC('projekt_adat')}), hatokor, torzs)


# ---------------------------------------------------------------------------
# R1.3 (RENDER_BRIEF.md) -- a het kezi res osszeallitasa adat/res_forras.tsv
# szerint. G2: fejlecsor a tablabol + torzs a tanulmanybol (vagy a lap mai
# rese valtozatlanul, vagy -- G16 -- adatbol generalva). Hianyzo jelolo vagy
# tabla-sor HIBAKOD, nem helyorzo (R1.3).
# ---------------------------------------------------------------------------

RES_SORREND = ('kivonat', '2b', 'miert_fontos', 'minosites', 'alatamasztas',
               'ertelmezes', 'alkalmazas', 'tanitoi', 'modszertan')

# DT-F127a (#127): a két új rés (`alkalmazas`, `tanitoi`) közös szakasza a
# 6. Értelmezés után. A régi lapokon a szakasz még nincs meg; a
# res_blokkok_alkalmaz() ilyenkor a 7. szakasz (a `modszertan` rés fejléce)
# elé szúrja, a törzset utána a res_forras.tsv szerint tölti.
SZAKASZ_6B = '## 6/b. Alkalmazás és tanítói egyezés *(kézi)*'
UJ_RESEK_6B = ('alkalmazas', 'tanitoi')

# A dokumentum-sorrend a VAZ_SABLON szerint (allandó): egy rés vagy egy
# generált szakasz literál címe követi az előzőt. A 'res' bejegyzések
# fejlécét a res_forras.tsv adja (motívumonként eltérhet -- pl. az
# ISTENTISZT-001 2/b fejléce); a 'lit' bejegyzések szó szerinti, közös
# szöveg minden oldalon.
_BOUNDARY_SLOTS = (
    ('res', 'kivonat'),
    ('lit', '## Tartalomjegyzék'),
    ('lit', '## Jelmagyarázat és rövidítések'),
    ('lit', '## 1. Előfordulások'),
    ('lit', '## 1/b. Kizárt és vizsgált helyek'),
    ('lit', '## 2. Szótári háttér'),
    ('res', '2b'),
    ('res', 'miert_fontos'),
    ('lit', '## 3. LXX-fordítói döntések'),
    ('lit', '## 4. Kereszthivatkozások'),
    ('res', 'minosites'),
    ('lit', '## 5. Kapcsolatok'),
    ('res', 'alatamasztas'),
    ('lit', SZAKASZ_5B),  # DT-F127b (α)
    ('res', 'ertelmezes'),
    ('lit', SZAKASZ_6B),
    ('res', 'alkalmazas'),
    ('res', 'tanitoi'),
    ('res', 'modszertan'),
    ('lit', '## 8. Irodalom és idézés'),
    ('lit', '## Kolofon'),
)

_res_forras_cache = None
_RES_MARKER_KEZDET = '<!-- RÉS-KEZDET: %s -->'
_RES_MARKER_VEGE = '<!-- RÉS-VÉGE: %s -->'


def res_forras_sorok():
    """{(id, res): sor} -- adat/res_forras.tsv."""
    global _res_forras_cache
    if _res_forras_cache is None:
        _, sorok = G.tsv_beolvas(RES_FORRAS_TSV)
        _res_forras_cache = {(r['id'], r['res']): r for r in sorok}
    return _res_forras_cache


def res_forras_teljesen_hianyzik_e(motivum_id):
    """Igaz, ha a motívumnak a res_forras.tsv-ben EGYETLEN (a 7 rés közül
    egy sem) sora sincs -- ilyenkor a motívum még nincs a lexikonoldal-
    rétegbe felvéve (l. FELADATOK #11/#12), a `run()` ezért kihagyja, nem
    dobja el a teljes generálást. Ha csak RÉSZBEN hiányzik, ez False marad,
    és a res_blokkok_alkalmaz saját HIBAKÓD-ja (ValueError) érvényesül --
    az részleges, tehát valódi adathiba, nem kihagyandó eset."""
    sorok = res_forras_sorok()
    return not any((motivum_id, res) in sorok for res in RES_SORREND)


_tanulmany_szoveg_cache = {}


def _tanulmany_szoveg(relativ_ut):
    if relativ_ut not in _tanulmany_szoveg_cache:
        path = os.path.join(ROOT, relativ_ut)
        with io.open(path, encoding='utf-8', newline='') as f:
            szoveg = f.read().replace('\r\n', '\n')
        # F11 R: a kézi forrás (`motivumok/[ID].md`, sablon 9) a lexikonoldalra
        # `apparatus` nézetként kerül (DT84 (10), SEMA 3.10.4): a `belso` szint
        # és a `【NAPLO】` kimarad, a RÉS-jelölők maradnak. A tematikus
        # tanulmány és a napló (a nem migrált motívumok) változatlanul.
        # DT-F127a: a 7. lépés saját fájlja (`motivumok/naplok/…_tanitoi_kereses.md`,
        # B9) nem sablon-9 forrás, a szintszűrő nem vonatkozik rá -- változatlanul.
        rel = relativ_ut.replace('\\', '/')
        if rel.startswith('motivumok/') and not rel.startswith('motivumok/naplok/'):
            szoveg = G.forras_nezet(szoveg, 'apparatus')[0]
        _tanulmany_szoveg_cache[relativ_ut] = szoveg
    return _tanulmany_szoveg_cache[relativ_ut]


def res_tanulmany_torzs(relativ_ut, res):
    """A tanulmány/napló <!-- RÉS-KEZDET: res -->…<!-- RÉS-VÉGE: res -->
    jelölőpárjainak törzse, dokumentum-sorrendben, egy üres sorral összefűzve
    (G2). HIBAKÓD (ValueError), ha egyetlen jelölőpár sincs -- nem helyőrző
    (R1.3)."""
    szoveg = _tanulmany_szoveg(relativ_ut)
    kezd = _RES_MARKER_KEZDET % res
    veg = _RES_MARKER_VEGE % res
    torzsek = []
    pos = 0
    while True:
        i = szoveg.find(kezd, pos)
        if i < 0:
            break
        torzs_kezd = i + len(kezd)
        j = szoveg.find(veg, torzs_kezd)
        if j < 0:
            raise ValueError('nyitó RÉS-marker záró pár nélkül: %s (%s)' % (res, relativ_ut))
        torzsek.append(szoveg[torzs_kezd:j].strip('\n'))
        pos = j + len(veg)
    if not torzsek:
        raise ValueError('nincs RÉS-marker-pár a tanulmányban: %s (%s)' % (res, relativ_ut))
    return '\n\n'.join(torzsek)


def res_torzs(m, res, sor, sorai=None):
    """A rés törzse a `forras` mező szerint -- 'tanulmany': a tanulmány/napló
    jelölői közötti szöveg (a `tanulmany` oszlop ilyenkor útvonal); 'adat':
    a `tanulmany` oszlop maga a generátor saját, adatból vezetett mondata
    (G16) -- a res_forras.tsv-be előre rögzítve, motívumonként eltérő
    indoklással (l. KIRALY-001, N19); ha a `tanulmany` mező üres, a rés
    törzsét az ADAT_RES_RENDEREK renderelője írja az adattáblákból (F11 R,
    DT-F11e); 'lap' erre a függvényre sosem hívódik (l. res_blokkok_alkalmaz).
    A `sorai` a motívum előfordulás-sorai; None esetén az elofordulasok.tsv-ből."""
    forras = sor['forras']
    if forras == 'tanulmany':
        return res_tanulmany_torzs(sor['tanulmany'], res)
    if forras == 'adat':
        mondat = sor.get('tanulmany')
        if mondat:
            return mondat
        if res not in ADAT_RES_RENDEREK:
            raise ValueError('nincs adat-alapú render szabály: %s / %s' % (m['id'], res))
        if sorai is None:
            sorai = _elofordulas_sorai(m['id'])
        return adatres_keret(m['id'], res, ADAT_RES_RENDEREK[res](m['id'], sorai))
    raise ValueError('ismeretlen forras: %r (%s / %s)' % (forras, m['id'], res))


# ---------------------------------------------------------------------------
# F11 R (DT-F11e): a három adatrés renderelője -- `forras=adat`, üres
# `tanulmany` mező. A tiszta függvények (adatres_*) a sorokat paraméterként
# kapják (tesztelhetők); az _adatres_* burkolók az élő táblákat töltik be.
# Üres adatnál a rés kimondott hiánymondatot kap (CLAUDE.md 3. szabály).
# ---------------------------------------------------------------------------

# A 2/b-be tartozó, szerephez nem rendelt szótárak (SEMA 2.5 `szotar`): a
# szerepmátrix (2.S) ezeket nem rendereli, a 2b rés igen (sablon 9 5. pont).
KIEGESZITO_SZOTARAK = ('SECE_G', 'SECE_H', 'MCGED')

ALATAMASZTAS_NINCS_KAPCSOLAT = 'A motívumhoz nincs rögzített kapcsolat.'
JELOLT_KERESZTHIV_ELOTAGOK = ('TSK', 'Károli-KH')


def _elofordulas_sorai(motivum_id):
    _, sorok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
    return [s for s in sorok if s['id'] == motivum_id]


def _kapcsolat_par(r):
    return '%s → %s' % (r['forras_igehely'], r['cel_igehely'])


def adatres_alatamasztas(motivum_id, kapcsolat_sorok):
    """Az Alátámasztás rés a `kapcsolatok.tsv` `indoklas` mezőjéből (SEMA 2.3,
    3.10.7 1.): az azonos indoklású sorok egy táblasorba kerülnek (a fájl
    sorrendjében, az első előfordulás helyén); az indoklás nélküli sorok
    felsorolva, hiányként."""
    sajat = [r for r in kapcsolat_sorok if r['id'] == motivum_id]
    if not sajat:
        return ALATAMASZTAS_NINCS_KAPCSOLAT
    csoportok = []
    index = {}
    nelkul = []
    for r in sajat:
        indoklas = (r.get('indoklas') or '').strip()
        if not indoklas:
            nelkul.append(_kapcsolat_par(r))
            continue
        if indoklas not in index:
            index[indoklas] = len(csoportok)
            csoportok.append((indoklas, []))
        csoportok[index[indoklas]][1].append(_kapcsolat_par(r))
    sorok = ['*Generált a `kapcsolatok.tsv` `indoklas` mezőjéből: soronként miért ez a funkció-címke, '
             'miért ez a bizonyossági szint.*', '']
    if csoportok:
        sorok += ['| Kapcsolat | Alátámasztás |', '|---|---|']
        for indoklas, parok in csoportok:
            sorok.append('| %s | %s |' % (_cella('; '.join(parok)), _cella(indoklas)))
    else:
        sorok.append('A motívum %d kapcsolat-sorának egyikéhez sincs rögzített indoklás a '
                     '`kapcsolatok.tsv`-ben.' % len(sajat))
    if nelkul and csoportok:
        sorok += ['', '*Rögzített indoklás nélküli kapcsolat-sor (%d): %s.*' % (len(nelkul), '; '.join(nelkul))]
    return '\n'.join(sorok)


def adatres_2b(tokenek, hiv_sorok):
    """A 2/b rés a `lexikon_hivatkozasok.tsv` szerephez nem rendelt
    (KIEGESZITO_SZOTARAK) soraiból, a kapott Strong-tokenekre (a motívum saját
    tokenjei + a rokon szavak, adatres_2b_tokenek): a sor
    szó szerinti kivonata (`szoveg_en`) és forrásfájlja; a fordítás, ha az
    `adat/forditasok.tsv`-ben áll."""
    sorok_ehhez = []
    for t in tokenek:
        sajat = [r for r in hiv_sorok if r['strong'] == t and r['szotar'] in KIEGESZITO_SZOTARAK]
        sorok_ehhez += sorted(sajat, key=lambda r: (r['szotar'], r['jelentes_szam']))
    if not sorok_ehhez:
        return ('*Nincs a szerepmátrixon (2. szakasz) túli kiegészítő szótári sor a '
                '`lexikon_hivatkozasok.tsv`-ben ehhez a motívumhoz.*')
    out = ['*Generált a `lexikon_hivatkozasok.tsv`-ből: a szerepmátrixon (2. szakasz) túli szótári sorok '
           '(%s).*' % ', '.join(KIEGESZITO_SZOTARAK)]
    for r in sorok_ehhez:
        bek = ['**%s %s — %s**' % (r['szotar'], r['strong'], _jsz_cimke(r['jelentes_szam'])),
               '> %s' % r['szoveg_en']]
        hu = forditas_ehhez(r['szotar'], r['strong'], r['entry_id'], r['jelentes_szam'], 'forditas_hu')
        if hu:
            bek.append('**🇭🇺** %s' % hu)
        bek.append('*Forrás: %s*' % r['forrasfajl'])
        out.append('\n\n'.join(bek))
    return '\n\n'.join(out)


def adatres_minosites(motivum_id, elof_igehelyek, jelolt_sorok, tsk_idx, kh_idx):
    """A Minősítés rés (SEMA 3.10.7 2.): (1) a független megerősítés -- a
    motívum előfordulás-igehelyeiről induló TSK (Votes ≥ 15) és Károli-KH
    találat, amelynek célja is a motívum előfordulás-igehelye; (2) a
    kereszthivatkozásból minősített jelöltek a `jeloltek.tsv`-ből
    (`forras_kereses` TSK / Károli-KH előtaggal), döntéssel és indoklással.
    `tsk_idx`: {igehely: [TSK-sor]}, `kh_idx`: {STEP-igehely: [KH-sor]}."""
    halmaz = set(elof_igehelyek)
    parok = []
    lattuk = set()
    for a in elof_igehelyek:
        if '-' in a:
            continue
        talalatok = [('TSK (Votes %s)' % r['Votes'], r) for r in tsk_idx.get(a, []) if int(r['Votes']) >= 15]
        try:
            step = L.to_step(a)
        except ValueError:
            step = None
        if step is not None:
            talalatok += [('Károli-KH', r) for r in kh_idx.get(step, [])]
        for cimke, r in talalatok:
            b = karoli_colon(r['Kapcsolódó igehely magyar megjelenítése'])
            kulcs = (a, b, cimke)
            if b in halmaz and b != a and kulcs not in lattuk:
                lattuk.add(kulcs)
                parok.append('- %s → %s — %s' % (a, b, cimke))
    out = ['*Generált: a független megerősítés a TSK (Votes ≥ 15) és a Károli-KH találatainak metszete a '
           'motívum előfordulás-igehelyeivel; a minősített jelöltek a `jeloltek.tsv`-ből (`forras_kereses`: '
           'TSK / Károli-KH).*']
    if parok:
        out.append('**Független megerősítés** (%d pár):\n\n%s' % (len(parok), '\n'.join(parok)))
    else:
        out.append('**Független megerősítés:** nincs olyan TSK- (Votes ≥ 15) vagy Károli-KH-találat, amely a '
                   'motívum két előfordulás-igehelyét kötné össze.')
    jeloltek = [j for j in jelolt_sorok if j['id'] == motivum_id
                and (j.get('forras_kereses') or '').startswith(JELOLT_KERESZTHIV_ELOTAGOK)]
    if jeloltek:
        szam = {}
        for j in jeloltek:
            szam[j['dontes']] = szam.get(j['dontes'], 0) + 1
        osszeg = ', '.join('%s %d' % (d, szam[d]) for d in ('beépítve', 'elutasítva', 'nyitva') if d in szam)
        tabla = ['**Kereszthivatkozásból minősített jelöltek** (%d sor; %s):' % (len(jeloltek), osszeg), '',
                 '| Igehely | Döntés | Forrás-keresés | Indoklás |', '|---|---|---|---|']
        for j in jeloltek:
            tabla.append('| %s | %s | %s | %s |' % (j['igehely'], j['dontes'], _cella(j['forras_kereses']),
                                                     _cella(j.get('indoklas') or EM_DASH)))
        out.append('\n'.join(tabla))
    else:
        out.append('**Kereszthivatkozásból minősített jelölt:** nincs a `jeloltek.tsv`-ben ehhez a motívumhoz.')
    return '\n\n'.join(out)


def _adatres_alatamasztas(motivum_id, sorai):
    return adatres_alatamasztas(motivum_id, kapcsolatok_sorok())


def adatres_2b_tokenek(tokenek, rokon):
    """A 2b rés Strong-tokenjei (DT-F11g (1)): a motívum saját tokenjei, utána
    a szerepmátrix „Rokon szavak” tokenjei (rokon_szavak_strongok), ismétlés
    nélkül -- így a lapon tárgyalt rokon igék kiegészítő sorai is megjelennek."""
    return list(tokenek) + [t for t in rokon if t not in tokenek]


def _adatres_2b(motivum_id, sorai):
    tokenek = motivum_strong_tokenek(sorai)
    return adatres_2b(adatres_2b_tokenek(tokenek, rokon_szavak_strongok(sorai, tokenek)),
                      lexikon_hivatkozasok_sorok())


def _adatres_minosites(motivum_id, sorai):
    return adatres_minosites(motivum_id, [s['igehely'] for s in sorai], jeloltek_sorok(),
                             tsk_index(), kh_index())


# A generált rés forrásai (a GENERÁLT-RÉS jelölő és a proveniencia-sor
# `forras=` mezője; CLAUDE.md 1. szabály).
ADAT_RES_FORRASAI = {
    'alatamasztas': ('adat/kapcsolatok.tsv',),
    '2b': ('adat/lexikon_hivatkozasok.tsv',),
    'minosites': ('adat/jeloltek.tsv', 'adat/elofordulasok.tsv',
                  'konkordancia/TSK_kereszthivatkozasok.tsv', 'konkordancia/Karoli_kereszthivatkozasok.tsv'),
}


def adatres_keret(motivum_id, res, torzs):
    """A generált rés kerete (ELLENOR_F11_M 7. szakasz 4.): elöl gépi
    GENERÁLT-RÉS jelölő, a végén a proveniencia-sor (`scope=… | forras=… |
    ts=…`, a ts a general.TS: PARDES_DATUM vagy a mai nap)."""
    forrasok = ', '.join(ADAT_RES_FORRASAI[res])
    return ('<!-- GENERÁLT-RÉS: %s | general.py --cel lexikon | forrás: %s -->\n\n%s\n\n'
            '*Proveniencia: `scope=id:%s | forras=%s | ts=%s`*'
            % (res, forrasok, torzs, motivum_id, '+'.join(ADAT_RES_FORRASAI[res]), G.TS))


ADAT_RES_RENDEREK = {
    'alatamasztas': _adatres_alatamasztas,
    '2b': _adatres_2b,
    'minosites': _adatres_minosites,
}


# G11: a 2/b fejléc egységesítése a 2. menetben -- a meglévő lexikonoldalak
# még a régi fejlécet hordozzák a boundary-keresés pillanatában, ezért a
# határ-keresés (nem az írás) egyszeri fallback-ként elfogadja a régi
# szöveget is. Csak a '2b' résnél volt eltérő induló fejléc (R0.2).
_LEGACY_FEJLEC = {'2b': '### 2/b *(kézi, ha van)*'}


def _boundary_index(fajl_szoveg, needle, search_from, res):
    """(index, ténylegesen megtalált szöveg) -- a hívó a második elem
    hosszával lépteti tovább a keresés kezdőpontját."""
    try:
        return fajl_szoveg.index(needle, search_from), needle
    except ValueError:
        pass
    # F11 M3 javítókör: a generált rés fejléce `*(generált)*`; a meglévő lap
    # és a VAZ_SABLON még a `*(kézi)*` alakot hordozza.
    kezi = needle.replace('*(generált)*', '*(kézi)*')
    if kezi != needle:
        try:
            return fajl_szoveg.index(kezi, search_from), kezi
        except ValueError:
            pass
    legacy = _LEGACY_FEJLEC.get(res)
    if legacy is not None and legacy != needle:
        return fajl_szoveg.index(legacy, search_from), legacy
    raise ValueError('a rés-fejléc nem található: %r' % needle)


def szakasz_6b_beszur(fajl_szoveg, m):
    """DT-F127a: ha a lapon még nincs „6/b.” szakasz, a 7. szakasz (a
    `modszertan` rés fejléce) elé szúrja: a szakaszcím, és a két új rés
    fejléce helyőrző törzzsel (a törzset a res_blokkok_alkalmaz cseréli).
    Ha a szakasz már megvan, a szöveg változatlan."""
    if SZAKASZ_6B in fajl_szoveg:
        return fajl_szoveg
    sorok = res_forras_sorok()
    fejlecek = []
    for res in ('ertelmezes',) + UJ_RESEK_6B + ('modszertan',):
        sor = sorok.get((m['id'], res))
        if sor is None:
            raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], res))
        fejlecek.append(sor['fejlec'])
    ert_i, ert_talalt = _boundary_index(fajl_szoveg, fejlecek[0], 0, 'ertelmezes')
    mod_i, _ = _boundary_index(fajl_szoveg, fejlecek[-1], ert_i + len(ert_talalt), 'modszertan')
    betet = '\n\n'.join([SZAKASZ_6B] + ['%s\n\n*Kézzel írandó.*' % f for f in fejlecek[1:-1]]) + '\n\n'
    return fajl_szoveg[:mod_i] + betet + fajl_szoveg[mod_i:]


def res_blokkok_alkalmaz(fajl_szoveg, m):
    """A het rés fejléc+törzs span-jét cseréli az adat/res_forras.tsv szerint
    -- 'lap' forrású résekhez NEM NYÚL (G12: a lap mai rése, változatlanul).
    HIBAKÓD, ha egy sor hiányzik a táblából (R1.3)."""
    sorok = res_forras_sorok()
    fajl_szoveg = szakasz_6b_beszur(fajl_szoveg, m)
    for res in RES_SORREND:
        sor = sorok.get((m['id'], res))
        if sor is None:
            raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], res))
        if sor['forras'] == 'lap':
            continue

        offsets = []
        search_from = 0
        for kind, ertek in _BOUNDARY_SLOTS:
            if kind == 'lit':
                i, talalt = _boundary_index(fajl_szoveg, ertek, search_from, None)
            else:
                masik_sor = sorok.get((m['id'], ertek))
                if masik_sor is None:
                    raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], ertek))
                i, talalt = _boundary_index(fajl_szoveg, masik_sor['fejlec'], search_from, ertek)
            offsets.append(i)
            search_from = i + len(talalt)

        slot_idx = _BOUNDARY_SLOTS.index(('res', res))
        fejlec = sor['fejlec']
        span_start = offsets[slot_idx]
        span_end = offsets[slot_idx + 1]
        torzs = res_torzs(m, res, sor)
        uj_span = fejlec + '\n\n' + torzs + '\n\n'
        fajl_szoveg = fajl_szoveg[:span_start] + uj_span + fajl_szoveg[span_end:]
    return fajl_szoveg


def res_torzs_lapbol(fajl_szoveg, m, res):
    """A rés törzse egy MÁR MEGÍRT lexikonoldal szövegéből -- 'lap' forrású
    résekhez (amelyeknek nincs adat-alapú vagy tanulmány-alapú előállítása,
    l. res_torzs()); a törzscikk-generátor (R1.7) ezzel olvassa vissza,
    amit a res_blokkok_alkalmaz() a lexikonoldalon változatlanul hagyott."""
    sorok = res_forras_sorok()
    offsets = []
    search_from = 0
    for kind, ertek in _BOUNDARY_SLOTS:
        if kind == 'lit':
            needle = ertek
        else:
            sor = sorok.get((m['id'], ertek))
            if sor is None:
                raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], ertek))
            needle = sor['fejlec']
        i = fajl_szoveg.index(needle, search_from)
        offsets.append(i)
        search_from = i + len(needle)
    slot_idx = _BOUNDARY_SLOTS.index(('res', res))
    fejlec = sorok[(m['id'], res)]['fejlec']
    body_start = offsets[slot_idx] + len(fejlec)
    body_end = offsets[slot_idx + 1]
    return fajl_szoveg[body_start:body_end].strip('\n')


_szerepek_cache = None


def szerepek_sorok():
    """[{nyelv, sorrend, szerep, forras, allapot}, ...] -- adat/szotar_szerepek.tsv
    (R1.5, G6), a tábla saját sorrendjében (nyelv szerint csoportosítva,
    azon belül `sorrend` szerint -- a beolvasás maga a fájl sorrendje)."""
    global _szerepek_cache
    if _szerepek_cache is None:
        path = os.path.join(ADAT, 'szotar_szerepek.tsv')
        _, _szerepek_cache = G.tsv_beolvas(path)
    return _szerepek_cache


def modell_epit(m, sorai, konyv_sorrend, hianyzo_konyvek, lexikon_szoveg=None):
    """G5: a `_TUDOMANYOS` és a `_TORZSCIKK` render közös belső adatmodellje
    -- egy szótár: a motívum sorai/tokenjei, a hét rés (fejléc+törzs, vagy
    `lap`-nál a már megírt lexikonoldalból visszaolvasva, ha az elérhető), és
    a szerepmátrix. A 10 generált blokk saját építő-logikája nem változik
    (render_lexikon_egy_id) -- ez a modell a rés- és szerep-réteget adja
    egységesen mindkét renderernek."""
    tokenek = motivum_strong_tokenek(sorai)
    sorok = res_forras_sorok()

    resek = {}
    for res in RES_SORREND:
        sor = sorok.get((m['id'], res))
        if sor is None:
            raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], res))
        if sor['forras'] == 'lap':
            torzs = (res_torzs_lapbol(lexikon_szoveg, m, res)
                     if lexikon_szoveg is not None else None)
        else:
            torzs = res_torzs(m, res, sor, sorai)
        resek[res] = {'fejlec': sor['fejlec'], 'forras': sor['forras'], 'torzs': torzs}

    return {
        'motivum': m,
        'tokenek': tokenek,
        'sorai': sorted(sorai, key=lambda s: G.igehely_rendezo_kulcs(
            s['igehely'], konyv_sorrend, hianyzo_konyvek)),
        'resek': resek,
        'szerepek': szerepek_sorok(),
        'kapcsolatok': [r for r in kapcsolatok_sorok() if r['id'] == m['id']],
    }


# ---------------------------------------------------------------------------
# Teljes fájlváz
# ---------------------------------------------------------------------------

VAZ_SABLON = """# 📖 %(id)s — %(cim)s

## Kivonat *(kézi)*

*Kézzel írandó — 3-5 mondatos prózai kivonat: mi a motívum, milyen azonosság-típusú, hány igehelyen, mi a legfontosabb lexikai lelet.*

## Tartalomjegyzék

%(tartalom)s

## Jelmagyarázat és rövidítések

%(jelmagyarazat)s

## 1. Előfordulások

%(elofordulasok)s

## 1/b. Kizárt és vizsgált helyek

%(kizart)s

## 2. Szótári háttér

%(szocikkek)s

### 2/b *(kézi, ha van)*

*Kézzel írandó, ha van.*

### Miért fontos ez a lelet *(kézi)*

*Kézzel írandó.*

## 3. LXX-fordítói döntések

%(lxx)s

## 4. Kereszthivatkozások

%(kereszthivatkozasok)s

### Minősítés *(kézi)*

*Kézzel írandó: független megerősítés / új találat / nem releváns.*

## 5. Kapcsolatok

%(kapcsolatok)s

### Alátámasztás *(kézi)*

*Kézzel írandó.*

## 5/b. Kapcsolódó motívumok

%(kapcsolodo)s

## 6. Értelmezés *(kézi)*

*Kézzel írandó — a forrás-study PaRDeS keretrendszere, bővítve a lexikai leletekkel.*

## 6/b. Alkalmazás és tanítói egyezés *(kézi)*

### Alkalmazás és tanítványság *(kézi)*

*Kézzel írandó.*

### Tanítói egyezés *(kézi)*

*Kézzel írandó.*

## 7. Módszertan és nyitott kérdések *(kézi)*

*Kézzel írandó.*

## 8. Irodalom és idézés

%(idezes)s

## Kolofon

%(kolofon)s
"""

BLOKK_NEVEK = ('tartalom', 'jelmagyarazat', 'elofordulasok', 'kizart', 'szocikkek', 'lxx',
               'kereszthivatkozasok', 'kapcsolatok', 'kapcsolodo', 'idezes', 'kolofon')


def render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek):
    tokenek = motivum_strong_tokenek(sorai)

    blokk_tartalom_szov = blokk_tartalom(m)
    blokk_jelmagyarazat_szov = blokk_jelmagyarazat(m)
    blokk_elofordulasok_szov, fl_elofordulasok = blokk_elofordulasok(m, sorai, konyv_sorrend, hianyzo_konyvek)
    blokk_kizart_szov, fl_kizart = blokk_kizart(m)
    blokk_szocikkek_szov, tisztazatlan_erintve, fl_szocikkek = blokk_szocikkek(m, tokenek, sorai)
    blokk_lxx_szov, fl_lxx = blokk_lxx(m, sorai, tokenek)
    blokk_kereszthiv_szov, fl_kereszthiv = blokk_kereszthivatkozasok(m, sorai, konyv_sorrend, hianyzo_konyvek)
    blokk_kapcsolatok_szov, fl_kapcsolatok = blokk_kapcsolatok(m, konyv_sorrend, hianyzo_konyvek)

    fajl_licenc_blokk_lista = (
        [(fajl, licenc, 'elofordulasok') for fajl, licenc in fl_elofordulasok]
        + [(fajl, licenc, 'kizart') for fajl, licenc in fl_kizart]
        + [(fajl, licenc, 'szocikkek') for fajl, licenc in fl_szocikkek]
        + [(fajl, licenc, 'lxx') for fajl, licenc in fl_lxx]
        + [(fajl, licenc, 'kereszthivatkozasok') for fajl, licenc in fl_kereszthiv]
        + [(fajl, licenc, 'kapcsolatok') for fajl, licenc in fl_kapcsolatok]
    )
    blokk_idezes_szov = blokk_idezes(m, fajl_licenc_blokk_lista)
    # F131.17: a tW „Módosítás” mondata a tényleges felhasználást követi (szövegközlés vagy csak azonosító)
    blokk_kolofon_szov = blokk_kolofon(m, fajl_licenc_blokk_lista,
                                       tw_szoveg_kozolve=TW_SZOVEG_JEL in blokk_szocikkek_szov)

    blokkok = {
        'tartalom': blokk_tartalom_szov,
        'jelmagyarazat': blokk_jelmagyarazat_szov,
        'elofordulasok': blokk_elofordulasok_szov,
        'kizart': blokk_kizart_szov,
        'szocikkek': blokk_szocikkek_szov,
        'lxx': blokk_lxx_szov,
        'kereszthivatkozasok': blokk_kereszthiv_szov,
        'kapcsolatok': blokk_kapcsolatok_szov,
        'kapcsolodo': blokk_kapcsolodo(m),  # DT-F127b (α)
        'idezes': blokk_idezes_szov,
        'kolofon': blokk_kolofon_szov,
    }

    return blokkok, tisztazatlan_erintve


def epit_uj_fajl(m, blokkok):
    return VAZ_SABLON % {
        'id': m['id'],
        'cim': m.get('cim', ''),
        'tartalom': blokkok['tartalom'],
        'jelmagyarazat': blokkok['jelmagyarazat'],
        'elofordulasok': blokkok['elofordulasok'],
        'kizart': blokkok['kizart'],
        'szocikkek': blokkok['szocikkek'],
        'lxx': blokkok['lxx'],
        'kereszthivatkozasok': blokkok['kereszthivatkozasok'],
        'kapcsolatok': blokkok['kapcsolatok'],
        'kapcsolodo': blokkok['kapcsolodo'],
        'idezes': blokkok['idezes'],
        'kolofon': blokkok['kolofon'],
    }


def _generalt_fejlec_sor(m):
    """R2.5: a lexikonoldal első sora elé kerülő, fájl-szintű gépi jelölés --
    nem tévesztendő össze a 10 blokk saját GENERÁLT-KEZDET/VÉGE jelölésével."""
    return '<!-- GENERÁLT: general.py --cel lexikon | rések: %s -->' % (m.get('forras_study') or '')


def _generalt_fejlec_alkalmaz(szoveg, m):
    fejlec = _generalt_fejlec_sor(m)
    if szoveg.startswith('<!-- GENERÁLT: general.py --cel lexikon'):
        sor_vege = szoveg.index('\n')
        # F11 M4 (DT-F11h Á7): CRLF-es munkapéldányon a fejléc utáni üres
        # sorok '\r'-t is hordoznak; csak a '\n' levágása egy plusz üres sort
        # hagyott (a helyben frissített lap ≠ az új fájlként generált).
        marad = szoveg[sor_vege + 1:].lstrip('\r\n')
        return fejlec + '\n\n' + marad
    return fejlec + '\n\n' + szoveg


_TS_LEVAGVA_RE = re.compile(r'\| ts=\S+ -->$')


def _fejlec_ts_nelkul(fejlec):
    return _TS_LEVAGVA_RE.sub('-->', fejlec)


def _blokk_beilleszt_fejleccel(fajl_szoveg, cel_kulcs, uj_blokk):
    talalat = G.marker_par_keres(fajl_szoveg, cel_kulcs)
    if not talalat:
        raise ValueError('nincs marker-pár: %s' % cel_kulcs)
    kezd_idx, torzs_kezd, torzs_veg, _veg_idx = talalat
    regi_fejlec = fajl_szoveg[kezd_idx:torzs_kezd]
    regi_torzs = fajl_szoveg[torzs_kezd:torzs_veg]

    uj_fejlec_vege = uj_blokk.index('-->') + len('-->')
    uj_fejlec = uj_blokk[:uj_fejlec_vege]
    uj_torzs = G.blokk_torzs(uj_blokk, cel_kulcs)

    if _fejlec_ts_nelkul(regi_fejlec) == _fejlec_ts_nelkul(uj_fejlec) and regi_torzs == uj_torzs:
        return fajl_szoveg, 'változatlan'
    return fajl_szoveg[:kezd_idx] + uj_fejlec + uj_torzs + fajl_szoveg[torzs_veg:], 'frissítve'


def frissit_meglevo_fajlt(meglevo_szoveg, m, blokkok):
    # DT-F127b (α): a régi lapon az 5/b. szakasz még nincs meg -- beszúrás a
    # 6. Értelmezés elé, utána a blokk a többihez hasonlóan frissül.
    szoveg = szakasz_5b_beszur(meglevo_szoveg, m, blokkok['kapcsolodo'])
    for blokk_nev in BLOKK_NEVEK:
        cel_kulcs = _cel_kulcs(m['id'], blokk_nev)
        szoveg, _ = _blokk_beilleszt_fejleccel(szoveg, cel_kulcs, blokkok[blokk_nev])
    return szoveg


def run(args, motivumok, elofordulasok, konyv_sorrend, hianyzo_konyvek):
    elof_id_szerint = G.elofordulasok_id_szerint(elofordulasok)
    kimenet_gyoker = (
        os.path.join(G.ROOT, 'lexikon') if (args.ir or args.ellenoriz)
        else os.path.join(args.kimenet, 'lexikon')
    )

    osszesitett_tisztazatlan = {}

    for m in motivumok:
        sorai = elof_id_szerint.get(m['id'], [])
        if not sorai:
            continue

        if res_forras_teljesen_hianyzik_e(m['id']):
            print('  %s: KIHAGYVA -- nincs egyetlen res_forras.tsv sora sem (a lexikonoldal-réteg '
                  'még nem indult el ehhez a motívumhoz, l. FELADATOK #11/#12)' % m['id'])
            continue

        blokkok, tisztazatlan_erintve_szocikkek = render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek)
        osszesitett_tisztazatlan[m['id']] = tisztazatlan_erintve_szocikkek

        cel_ut = os.path.join(kimenet_gyoker, '%s_TUDOMANYOS.md' % m['id'])

        if os.path.exists(cel_ut):
            with io.open(cel_ut, encoding='utf-8', newline='') as f:
                meglevo = f.read()
            uj_szoveg = frissit_meglevo_fajlt(meglevo, m, blokkok)
            uj_szoveg = res_blokkok_alkalmaz(uj_szoveg, m)
            uj_szoveg = _generalt_fejlec_alkalmaz(uj_szoveg, m)
            allapot = 'változatlan' if uj_szoveg == meglevo else 'frissítve'
        else:
            uj_szoveg = epit_uj_fajl(m, blokkok)
            uj_szoveg = res_blokkok_alkalmaz(uj_szoveg, m)
            uj_szoveg = _generalt_fejlec_alkalmaz(uj_szoveg, m)
            allapot = 'új fájl'

        if args.ellenoriz:
            print('  %s: --ellenoriz, nincs írás (%s lenne)' % (m['id'], allapot))
            continue

        os.makedirs(kimenet_gyoker, exist_ok=True)
        with io.open(cel_ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(uj_szoveg)
        print('  %s: %s (%s, %d bájt)'
              % (m['id'], os.path.relpath(cel_ut, ROOT), allapot, os.path.getsize(cel_ut)))

    print('  tisztázatlan licencű forrás érintett-e (motívumonként): %s'
          % ', '.join('%s=%s' % (k, 'igen' if v else 'nem') for k, v in osszesitett_tisztazatlan.items()))
    return 0
