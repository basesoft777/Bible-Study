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
import ubs_hozzarendeles as UBS
import lxx_os_import as LXXOS

ROOT = G.ROOT
ADAT = G.ADAT
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')

LEXIKON_HIVATKOZASOK_TSV = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
OSHL_TSV = os.path.join(KONKORDANCIA, 'OSHL_lexikalis_index.tsv')
KAPCSOLATOK_TSV = os.path.join(ADAT, 'kapcsolatok.tsv')
JELOLTEK_TSV = os.path.join(ADAT, 'jeloltek.tsv')
FORDITAS_UBS_TSV = os.path.join(ADAT, 'forditas_ubs.tsv')
LXX_DONTESEK_TSV = os.path.join(ADAT, 'lxx_dontesek.tsv')
STRONG_SZOTAR_TSV = os.path.join(KONKORDANCIA, 'Strong_szotar.tsv')
TBESG_TXT = os.path.join(KONKORDANCIA, 'TBESG.txt')
TBESH_TXT = os.path.join(KONKORDANCIA, 'TBESH.txt')
LXX_OS_DIR = os.path.join(KONKORDANCIA, 'LXX_OS')

STRONG_TOKEN_RE = re.compile(r'^[HG]\d{4}[A-Za-z]?$')
EM_DASH = '—'

# --- Licencek, §1.3 -------------------------------------------------------

LICENC = {
    'BDB': 'közkincs',
    'Karoli_KH': 'közkincs',
    'TBESH': 'CC BY 4.0',
    'TBESG': 'CC BY 4.0',
    'TSK': 'CC BY 4.0',
    'OSHL': 'CC BY 4.0',
    'SDBH': 'CC BY-SA 4.0',
    'SDGNT': 'CC BY-SA 4.0',
    'LXX_OS': 'CC BY 4.0',
    'Thayer': 'közkincs',
    'LSJ': 'CC BY-SA 3.0',
    'SECE_G': 'közkincs',
    'SECE_H': 'közkincs',
    'MCGED': '© Mounce 1993',
    'UBS': 'CC BY-SA 4.0',
    'projekt-adat': 'projekt-adat',
}

# A lexikon_hivatkozasok.tsv szótárkulcsai közül ma egyik sem tisztázatlan
# (LEXV2_2_BRIEF.md: a Thayer közkincs). A halmaz üresen marad, nem törölve.
TISZTAZATLAN_SZOTARAK = set()

MOUNCE_MEGJELOLES = (
    'Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights '
    'Reserved, www.teknia.com/greek-dictionary'
)
LSJ_FORRASMEGJELOLES = (
    'LSJ forrás: Liddell-Scott-Jones, Perseus Digital Library (`lexica` '
    'repó), CC BY-SA 3.0.'
)


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
            return r['Ragozott alak'], r['Kiejtés'], ('TAHOT' if strong.startswith('H') else 'TAGNT')
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
        for path in (TBESG_TXT, TBESH_TXT):
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


def lemma_kiejtes(strong):
    """(lemma, kiejtes) vagy None, a TBESG/TBESH-ből, Strong-szám szerint
    -- pontos egyezés, majd betűutótag nélküli alapalakra visszaesve."""
    pontos, alap = tbesg_tbesh_index()
    if strong in pontos:
        return pontos[strong]
    return alap.get(strong)


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
    ('6. Értelmezés', False),
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
    hatokor = 'Ez a blokk a lexikon-oldal 12 szakaszának tartalomjegyzékét adja (LEXV2_2_BRIEF.md G1).'
    torzs = '\n'.join(sorok)
    return _lexikon_blokk(m['id'], 'tartalom', [], ['projekt-adat'], hatokor, torzs)


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
    return _lexikon_blokk(m['id'], 'jelmagyarazat', [], ['projekt-adat'], hatokor, JELMAGYARAZAT_TORZS)


# ---------------------------------------------------------------------------
# UBS-jelentés (G3) — az ubs_hozzarendeles.py logikájának újrafelhasználása
# ---------------------------------------------------------------------------

_ubs_ref_idx = None
_ubs_jelentes_idx = None
_ubs_definicio_idx = None
_forditas_ubs_idx = None


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


def forditas_ubs_index():
    global _forditas_ubs_idx
    if _forditas_ubs_idx is None:
        rows = L.read_tsv_skip_comments(FORDITAS_UBS_TSV)
        _forditas_ubs_idx = {(r['strong'], r['entry_kod']): r for r in rows}
    return _forditas_ubs_idx


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
    fud_idx = forditas_ubs_index()

    tokenenkent = {}
    for r in out_rows:
        _id, _ige, strong, lexid, entry_kod, glosszak, egyertelmu, _megjegyzes = r
        if not entry_kod:
            continue
        fud = fud_idx.get((strong, entry_kod))
        if fud and (fud.get('definicio_hu') or '').strip():
            szoveg = fud['definicio_hu']
        else:
            angol = definicio_idx.get((strong, lexid)) or glosszak
            szoveg = '%s *(fordítás függőben)*' % angol
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
        if proveniencia or igazolas:
            lj = 'proveniencia: %s | igazolas: %s' % (proveniencia or EM_DASH, igazolas or EM_DASH)
            labjegyzetek.append(lj)
            igehely_link += '[^%d]' % len(labjegyzetek)

        szotari_jelentes = lexikon_jelentes_cella(s)
        ubs_cella = ubs_jelentes_cella(s['id'], s['igehely'], s.get('strong') or '')
        megb = '%s · %s' % (s.get('megbizhatosag') or EM_DASH, s.get('azonositas_modja') or EM_DASH)

        sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
            igehely_link, kulcsszo_cella(s), s.get('funkcio') or EM_DASH,
            s.get('pardes_szint') or EM_DASH, s.get('strong') or EM_DASH,
            szotari_jelentes, ubs_cella, megb))

        tetelek_1a.append((anchor, s))

    torzs = '\n'.join(sorok)
    if labjegyzetek:
        torzs += '\n\n' + '\n'.join('[^%d]: %s' % (i, lj) for i, lj in enumerate(labjegyzetek, start=1))

    torzs += ('\n\n*Az UBS-jelentés csak újszövetségi soroknál áll: az UBS Greek New '
              'Testament Dictionary az Újszövetséget fedi.*')

    torzs += '\n\n#### 1/a. Az igehelyek szövege\n'
    karoli_terkep = L.load_karoli_1908()
    for anchor, s in tetelek_1a:
        reszek = ['<a id="%s"></a>' % anchor, '**%s**' % s['igehely']]
        for vers in igehely_lista(s['igehely']):
            szoveg = karoli_terkep.get(vers)
            if szoveg:
                reszek.append('*%s*' % szoveg)
            else:
                reszek.append('*(%s: nincs Károli-szöveg)*' % vers)
        if s.get('kapcsolodas'):
            reszek.append(s['kapcsolodas'])
        torzs += '\n\n' + '\n'.join(reszek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehely-sorát fedi az `elofordulasok.tsv`-ből, '
               'kanonikus sorrendben, a Károli-szöveggel (1/a) és az UBS-jelentés renderidejű '
               'hozzárendelésével (G3).' % (m['id'], len(sorai_rendezve)))
    blokk_szoveg = _lexikon_blokk(
        m['id'], 'elofordulasok',
        ['adat/elofordulasok.tsv', 'konkordancia/Karoli_1908.tsv', 'konkordancia/UBS_DNTG_referenciak.tsv',
         'konkordancia/UBS_DNTG_jelentesek.tsv', 'adat/forditas_ubs.tsv'],
        ['projekt-adat', 'közkincs', 'CC BY-SA 4.0'],
        hatokor, torzs)
    forras_licenc_parok = [
        ('adat/elofordulasok.tsv', 'projekt-adat'),
        ('konkordancia/Karoli_1908.tsv', 'közkincs'),
        ('konkordancia/UBS_DNTG_referenciak.tsv', 'CC BY-SA 4.0'),
        ('konkordancia/UBS_DNTG_jelentesek.tsv', 'CC BY-SA 4.0'),
        ('adat/forditas_ubs.tsv', 'projekt-adat'),
    ]
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
        _jeloltek_cache = sorok
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
                           ['projekt-adat'], hatokor, torzs), \
        [('adat/jeloltek.tsv', 'projekt-adat'), ('adat/motivumok.tsv', 'projekt-adat')]


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


def blokk_szocikkek(m, tokenek):
    reszek = []
    fajl_licenc_kulcsok = {'adat/lexikon_hivatkozasok.tsv': set()}
    van_hivatkozas_barmelyikhez = False
    tisztazatlan_erintve = False

    fajl_licenc_kulcsok_tbesg_tbesh = set()
    for strong in tokenek:
        lk = lemma_kiejtes(strong)
        if lk:
            lemma, kiejtes = lk
            alszakasz = ['### %s — %s (%s)' % (strong, lemma, kiejtes)]
            fajl_licenc_kulcsok_tbesg_tbesh.add('TBESG' if strong.startswith('G') else 'TBESH')
        else:
            alszakasz = ['### %s' % strong]

        if strong.startswith('H'):
            twotok = oshl_twot_ehhez(strong)
            alszakasz.append('**TWOT:** %s' % (', '.join(twotok) if twotok else EM_DASH))
            fajl_licenc_kulcsok.setdefault('konkordancia/OSHL_lexikalis_index.tsv', set()).add('OSHL')
        else:
            alszakasz.append('**TWOT:** %s' % EM_DASH)

        domenek = domen_talalatok(strong)
        domen_szoveg = ', '.join('%s %s' % (kod, label) for kod, label in domenek) if domenek else EM_DASH
        alszakasz.append('**Szemantikai domén:** %s' % domen_szoveg)
        domen_fajl = 'konkordancia/SDBH_domenek.tsv' if strong.startswith('H') else 'konkordancia/SDGNT_domenek.tsv'
        domen_licenc_kulcs = 'SDBH' if strong.startswith('H') else 'SDGNT'
        fajl_licenc_kulcsok.setdefault(domen_fajl, set()).add(domen_licenc_kulcs)

        for anom in domen_anomalia_figyelmeztetes(strong):
            alszakasz.append('*Figyelem: elemzetlen bejegyzés illeszkedik — %s %s %s*'
                              % (anom['entry_id'], anom['lemma'], anom['nyers_ertek']))

        hiv_sorok = lexikon_hivatkozasok_ehhez(strong)
        if hiv_sorok:
            van_hivatkozas_barmelyikhez = True
            for r in hiv_sorok:
                fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv'].add(r['szotar'])
                fajl_licenc_kulcsok.setdefault(r['forrasfajl'], set()).add(r['szotar'])
                if r['szotar'] in TISZTAZATLAN_SZOTARAK:
                    tisztazatlan_erintve = True
                jsz_cimke = '(teljes szócikk)' if r['jelentes_szam'] == 'teljes' else '%s. jelentés' % r['jelentes_szam']
                alszakasz.append('#### %s %s — %s' % (r['szotar'], r['entry_id'], jsz_cimke))
                alszakasz.append('> %s' % r['szoveg_en'])
                if r['forditas_hu']:
                    alszakasz.append('**🇭🇺** %s' % r['forditas_hu'])
                else:
                    alszakasz.append('*Fordítás függőben.*')
                alszakasz.append('*Forrás: %s*' % r['forrasfajl'])
        else:
            alszakasz.append('Nincs jelentés-hivatkozás a `lexikon_hivatkozasok.tsv`-ben.')

        reszek.append('\n\n'.join(alszakasz))

    if not fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv']:
        del fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv']
    if 'TBESG' in fajl_licenc_kulcsok_tbesg_tbesh:
        fajl_licenc_kulcsok.setdefault('konkordancia/TBESG.txt', set()).add('TBESG')
    if 'TBESH' in fajl_licenc_kulcsok_tbesg_tbesh:
        fajl_licenc_kulcsok.setdefault('konkordancia/TBESH.txt', set()).add('TBESH')

    torzs = '\n\n'.join(reszek)
    licenc_lista = _sorted_unique(LICENC[k] for kulcsok in fajl_licenc_kulcsok.values() for k in kulcsok)
    forras_licenc_parok = [
        (fajl, licenc)
        for fajl, kulcsok in fajl_licenc_kulcsok.items()
        for licenc in _sorted_unique(LICENC[k] for k in kulcsok)
    ]
    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d Strong-tokenjét fedi, %s jelentés-hivatkozással '
               'a `lexikon_hivatkozasok.tsv`-ből.'
               % (m['id'], len(tokenek), 'van' if van_hivatkozas_barmelyikhez else 'nincs'))
    blokk_szoveg = _lexikon_blokk(m['id'], 'szocikkek', sorted(fajl_licenc_kulcsok), licenc_lista, hatokor, torzs)
    return blokk_szoveg, tisztazatlan_erintve, forras_licenc_parok


# ---------------------------------------------------------------------------
# 3. LXX-fordítói döntések (G5)
# ---------------------------------------------------------------------------

_karoli_to_primary_slug = None
_lxx_os_rows_cache = {}
_lxx_os_karoli_idx_cache = {}
_lxx_dontesek_cache = None


def karoli_to_primary_slug():
    global _karoli_to_primary_slug
    if _karoli_to_primary_slug is None:
        terkep = {}
        for slug, (_title, book_key, _test) in LXXOS.BOOKS.items():
            karoli_book = LXXOS.BOOK_KEY_TO_KAROLI.get(book_key)
            if not karoli_book:
                continue
            if slug == book_key:
                terkep[karoli_book] = slug
            elif karoli_book not in terkep:
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


def lxx_dontesek_index():
    global _lxx_dontesek_cache
    if _lxx_dontesek_cache is None:
        _, sorok = G.tsv_beolvas(LXX_DONTESEK_TSV)
        idx = {}
        for r in sorok:
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
        kiejtes = gepi_atiras(r['lemma']) + ' *(gépi átírás)*'
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
                        kiejtes = gepi_atiras(r.get('gorog_lemma') or '') + ' *(gépi átírás)*'
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
                                   ['CC BY 4.0', 'projekt-adat'], hatokor, torzs)
    forras_licenc_parok = [(f, 'CC BY 4.0') for f in sorted(forras_fajlok)]
    if dontesek_hasznalt:
        forras_licenc_parok.append(('adat/lxx_dontesek.tsv', 'projekt-adat'))
    return blokk_szoveg, forras_licenc_parok


# ---------------------------------------------------------------------------
# 4. Kereszthivatkozások (TSK + Károli-KH)
# ---------------------------------------------------------------------------

_tsk_by_igehely = None
_kh_by_step = None


def tsk_index():
    global _tsk_by_igehely
    if _tsk_by_igehely is None:
        idx = {}
        for r in L.load_tsk():
            idx.setdefault(r['Igehely'], []).append(r)
        _tsk_by_igehely = idx
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
        ['CC BY 4.0', 'közkincs'], hatokor, torzs
    )
    forras_licenc_parok = [
        ('konkordancia/TSK_kereszthivatkozasok.tsv', 'CC BY 4.0'),
        ('konkordancia/Karoli_kereszthivatkozasok.tsv', 'közkincs'),
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
        return _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], ['projekt-adat'], hatokor, torzs), \
            [('adat/kapcsolatok.tsv', 'projekt-adat')]

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
    blokk_szoveg = _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], ['projekt-adat'], hatokor, torzs)
    return blokk_szoveg, [('adat/kapcsolatok.tsv', 'projekt-adat')]


# ---------------------------------------------------------------------------
# 8. Irodalom és idézés
# ---------------------------------------------------------------------------

FAJL_TELJES_NEV = {
    'konkordancia/BDB_teljes_unabridged.tsv':
        'BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906)',
    'konkordancia/TBESG.txt': 'TBESG (Tyndale Brief lexicon of Extended Strongs for Greek)',
    'konkordancia/TBESH.txt': 'TBESH (Tyndale Brief lexicon of Extended Strongs for Hebrew)',
    'konkordancia/Thayer_teljes.tsv': "Thayer (Thayer's Greek-English Lexicon of the New Testament)",
    'konkordancia/UBS_DNTG_jelentesek.tsv': 'UBS (UBS Dictionary of New Testament Greek — Louw–Nida szemantikai domének)',
    'konkordancia/UBS_DNTG_referenciak.tsv': 'UBS (UBS Dictionary of New Testament Greek — Louw–Nida szemantikai domének)',
    'konkordancia/SDBH_domenek.tsv': 'SDBH (Semantic Dictionary of Biblical Hebrew)',
    'konkordancia/SDGNT_domenek.tsv': 'SDGNT (Semantic Dictionary of Biblical Greek)',
    'konkordancia/OSHL_lexikalis_index.tsv': 'OSHL (Open Scriptures Hebrew Lexicon) — csak TWOT-szám',
    'konkordancia/TSK_kereszthivatkozasok.tsv': 'TSK (Treasury of Scripture Knowledge)',
}
ADATFORRAS_FAJLOK = {'konkordancia/Karoli_1908.tsv', 'konkordancia/Karoli_kereszthivatkozasok.tsv',
                      'adat/lexikon_hivatkozasok.tsv'}


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
    return _lexikon_blokk(m['id'], 'idezes', [], ['projekt-adat'], hatokor, torzs)


# ---------------------------------------------------------------------------
# Kolofon (régi 0. Metaadatok + 9. Források és licencek összevonva)
# ---------------------------------------------------------------------------

def blokk_kolofon(m, fajl_licenc_blokk_lista):
    forras_study_sorok = [s.strip() for s in (m.get('forras_study') or '').split(';') if s.strip()]
    forras_study_cella = '<br>'.join('`%s`' % s for s in forras_study_sorok) if forras_study_sorok else EM_DASH

    naplo_fajlnev = G.ID_NAPLO_TERKEP.get(m['id'])
    naplo_cella = '`tematikus_lezart/naplok/%s`' % naplo_fajlnev if naplo_fajlnev else EM_DASH
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
    if '© Mounce 1993' in tabla_licencek:
        megjelolesek.append('*%s*' % MOUNCE_MEGJELOLES)
    if 'CC BY-SA 3.0' in tabla_licencek:
        megjelolesek.append('*%s*' % LSJ_FORRASMEGJELOLES)

    torzs = '\n'.join(metaadat_sorok) + '\n\n---\n\n' + '\n'.join(forras_sorok)
    if megjelolesek:
        torzs += '\n\n' + '\n\n'.join(megjelolesek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum törzsadatait (`motivumok.tsv`) és a lexikon-oldalon '
               'ténylegesen felhasznált forrásokat sorolja fel.' % m['id'])
    return _lexikon_blokk(m['id'], 'kolofon', sorted(set(per_fajl) | {'adat/motivumok.tsv'}),
                           sorted(tabla_licencek | {'projekt-adat'}), hatokor, torzs)


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

## 6. Értelmezés *(kézi)*

*Kézzel írandó — a forrás-study PaRDeS keretrendszere, bővítve a lexikai leletekkel.*

## 7. Módszertan és nyitott kérdések *(kézi)*

*Kézzel írandó.*

## 8. Irodalom és idézés

%(idezes)s

## Kolofon

%(kolofon)s
"""

BLOKK_NEVEK = ('tartalom', 'jelmagyarazat', 'elofordulasok', 'kizart', 'szocikkek', 'lxx',
               'kereszthivatkozasok', 'kapcsolatok', 'idezes', 'kolofon')


def render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek):
    tokenek = motivum_strong_tokenek(sorai)

    blokk_tartalom_szov = blokk_tartalom(m)
    blokk_jelmagyarazat_szov = blokk_jelmagyarazat(m)
    blokk_elofordulasok_szov, fl_elofordulasok = blokk_elofordulasok(m, sorai, konyv_sorrend, hianyzo_konyvek)
    blokk_kizart_szov, fl_kizart = blokk_kizart(m)
    blokk_szocikkek_szov, tisztazatlan_erintve, fl_szocikkek = blokk_szocikkek(m, tokenek)
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
    blokk_kolofon_szov = blokk_kolofon(m, fajl_licenc_blokk_lista)

    blokkok = {
        'tartalom': blokk_tartalom_szov,
        'jelmagyarazat': blokk_jelmagyarazat_szov,
        'elofordulasok': blokk_elofordulasok_szov,
        'kizart': blokk_kizart_szov,
        'szocikkek': blokk_szocikkek_szov,
        'lxx': blokk_lxx_szov,
        'kereszthivatkozasok': blokk_kereszthiv_szov,
        'kapcsolatok': blokk_kapcsolatok_szov,
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
        'idezes': blokkok['idezes'],
        'kolofon': blokkok['kolofon'],
    }


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
    szoveg = meglevo_szoveg
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

        blokkok, tisztazatlan_erintve_szocikkek = render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek)
        osszesitett_tisztazatlan[m['id']] = tisztazatlan_erintve_szocikkek

        cel_ut = os.path.join(kimenet_gyoker, '%s_TUDOMANYOS.md' % m['id'])

        if os.path.exists(cel_ut):
            with io.open(cel_ut, encoding='utf-8', newline='') as f:
                meglevo = f.read()
            uj_szoveg = frissit_meglevo_fajlt(meglevo, m, blokkok)
            allapot = 'változatlan' if uj_szoveg == meglevo else 'frissítve'
        else:
            uj_szoveg = epit_uj_fajl(m, blokkok)
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
