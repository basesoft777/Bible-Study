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

import collections
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
import tablajegyzet as TJ
import lxx_os_import as LXXOS
import kiejtes as KJ
import utvonalak as _U
import szerep_karoli as SZK
import szerep_nave as SZN
import szerep_kizart as SZKZ
import olvasoi_kovetkeztetes as OK  # az olvasói szöveg: lelet + következtetés (2026-10-30)
import bdb_rovidites as BR  # a BDB egybetűs rövidítései, közös az olvasóval (N-F131x)
import bdb_tagolas as BT  # a BDB-szócikk tagolása a szakasztáblából, közös az olvasóval (F182, F33)
import olvasoi_utofeldolg as OU  # az olvasói szöveg egységesítése a kész lapon (olvasói kapu, 2026-11-02)
import heber_kiejtes as HK  # gépi magyaros héber kiejtés a pontozott szövegből (DT-F131y)
import bdb_vj_szabaly as VJ  # a 2.29 sorainak minősítése, közös az olvasó-szerverrel (DT-F104d/e)
# F187: a szótári glossza-szabály (a 4.2 kártyája és a szó-lap közös szabálya, egy hely)
from szotari_glossza import (  # noqa: E402,F401
    jelolo_levag, _GOROG_BETU_RX, _KLASSZIKUS, _zarojel_nelkul, _THAYER_META, thayer_fej_glossza, thayer_glossza,
    thayer_csak_alak, _torzs_norm, vegyes_cim_nelkul, _GLOSSZA_VAG, olvasoi_glossza, _ALAKTANI_KEZDET)

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


# A Károli-KH/TSK magyar megjelenítésének régi könyvrövidítései, amelyek nem a
# `Konyv_normalizalo_tabla.tsv` alakjai (olvasói kapu KONYV).
KH_KONYV_JAVIT = {'Eféz': 'Ef', 'Siral': 'JSir'}


def karoli_colon(s):
    """'Péld 8,22' -> 'Péld 8:22'; '1Móz 2,4-5' -> '1Móz 2:4-5' (G8/K5:
    a TSK/Károli-KH magyar-megjelenítése vesszős, a generált oldal nem
    lehet az); a régi könyvrövidítés a normalizáló tábla alakjára."""
    for regi, uj in KH_KONYV_JAVIT.items():
        if s.startswith(regi + ' '):
            s = uj + s[len(regi):]
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
    # a szókezdő spiritus asper „h” (ᾅδης → hadés; ELLENOR_ISTENTISZT_OLVASOI_2 4.); a kezdő ρ-nél „rh”
    nfd = unicodedata.normalize('NFD', gorog_szo)
    elso = re.match(r'[^\W\d_]([\u0300-\u036f]*)', nfd)
    if elso and '\u0314' in elso.group(1) and alap[:1].lower() != 'ρ':
        return 'h' + gepi_atiras_nyers(alap)
    return gepi_atiras_nyers(alap)


def gepi_atiras_nyers(alap):
    # a kettőshangzóban (αυ, ευ, ηυ, ου) az υ SBL szerint „u” (Κυρίου → kyriou, nem kyrioy; a kiejtés-szabály, ISTENTISZT-001 arany lap 2026-10-29)
    return ''.join('u' if ch in 'υΥ' and i and alap[i - 1].lower() in 'αεηο' else _GOROG_BETU.get(ch.lower(), ch)
                   if ch.isupper() and ch.lower() in _GOROG_BETU else _GOROG_BETU.get(ch, ch)
                   for i, ch in enumerate(alap))


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
    használandó (V2.6a pont 2), nem lemma-fejlécekben.
    Héberül (DT-F131y, 2026-10-30) a ragozott alak a TELJES szó (előtag + tő + toldalék, a TAHOT vers-soraiból),
    és a saját gépi kiejtését kapja „…, gépi” jelöléssel (forras='TAHOT'); pontozatlan alaknál a lemma kiejtése
    áll, „szótári alak:” jelöléssel (forras='TAHOT_LEMMA')."""
    forras_idx = tahot_index() if strong.startswith('H') else tagnt_index()
    for ige in igehely_lista(igehely):
        r = forras_idx.get((ige, strong))
        if r:
            if strong.startswith('G'):
                # F09 S2.1: görög alak -> magyaros kiejtés; a héber alak STEP-átírása változatlan
                return r['Ragozott alak'], gorog_magyaros(r['Kiejtés']), 'TAGNT'
            sorok = tahot_vers_index().get(ige, [])
            i = max(k for k, x in enumerate(sorok) if x['Strong-szám'] == strong)  # a tahot_index választása (utolsó)
            alak, elotag, makkef = HK.teljes_szo(sorok, i)
            gepi = heber_gepi(alak, elotag, makkef)
            if gepi:
                return alak, gepi, 'TAHOT'
            lk = lemma_kiejtes(strong)
            return r['Ragozott alak'], lk[1] if lk else '', 'TAHOT_LEMMA'
    return None


_tahot_vers_cache = None


def tahot_vers_index():
    """{igehely: [TAHOT-sorok a fájl sorrendjében]} -- a teljes szó összerakásához (DT-F131y)."""
    global _tahot_vers_cache
    if _tahot_vers_cache is None:
        idx = {}
        for r in L.load_tahot():
            idx.setdefault(r['Igehely'], []).append(r)
        _tahot_vers_cache = idx
    return _tahot_vers_cache


def heber_gepi(alak, elotag_hossz=0, makkef=False):
    """A pontozott héber alak gépi kiejtése („vajjikrá”; DT-F131y, jelölés nélkül — DT430 kiegészítés: a felhasználó
    „nem kell odarakni hogy gépi”), vagy '' pontozatlan alakra."""
    k = HK.kiejt(alak, elotag_hossz, makkef)
    return k or ''


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
    """(lemma, kiejtés) vagy None, a TBESG/TBESH-ből, Strong-szám szerint -- pontos egyezés, majd betűutótag nélküli
    alapalakra visszaesve. A kiejtés-szabály (kiejtés-szabály, ISTENTISZT-001 arany lap, 2026-10-29): görögül a kiejtes.py magyaros átírása a TBESG-átírásból,
    héberül a jóváhagyott kivétel-sor (`adat/kiejtes_kivetelek.tsv`), ennek híján (DT-F131y) a pontozott lemma gépi
    kiejtése „…, gépi” jelöléssel; ha az sincs (pontozatlan lemma), a kiejtés '', és a Strong a KIEJTES_HIANY-ba kerül."""
    return lemma_kiejtes_szabaly(strong)


def lemma_cim(lk):
    """„lemma (kiejtés)”, vagy „lemma”, ha a kiejtés üres (kiejtés-szabály, ISTENTISZT-001 arany lap, 2026-10-29)."""
    return '%s (%s)' % lk if lk[1] else lk[0]


# A kiejtés-szabály (kiejtés-szabály, ISTENTISZT-001 arany lap, 2026-10-29): a lemma mellett mindig magyaros kiejtés — görögül gépi, héberül a jóváhagyott
# (`adat/kiejtes_kivetelek.tsv`), ennek híján gépi „…, gépi” jelöléssel (DT-F131y, 2026-10-30); ha az sincs, a jelölt hiányok közé kerül.
KIEJTES_HIANY = {}


# F182 (A04, N-F178b): a betű nélküli Strong TBESH-változata (H2403a חַטָּאָה ↔ H2403b חַטָּאת) a motívum szövegéhez
# illesztve: a 4.11 `strong_valtozat_versben` szabálya dönt. Csak az új szerkezetű lap generálása alatt áll be
# (`lemma_valtozat_beallit`); a régi lapok a betű nélküli alapalakot kapják (E28).
LEMMA_VALTOZAT = {}


def lemma_valtozat_beallit(sorai):
    """{Strong: változat-kulcs} a motívum soraiból, a 4.11 szabályával (`strong_valtozat_versben`: a versek TAHOT-szótöve a
    változatok TBESH-lemmájával összevetve; egy szabály, egy hely)."""
    LEMMA_VALTOZAT.clear()
    strongok = {t for s in sorai or [] for t in (s.get('strong') or '').split('+') if t.startswith('H')}
    versek = [v for s in sorai or [] for v in igehely_lista(s['igehely'])]
    for st in strongok:
        v = strong_valtozat_versben(st, versek)
        if v != st:
            LEMMA_VALTOZAT[st] = v
    return LEMMA_VALTOZAT


def lemma_kiejtes_szabaly(strong):
    """(lemma, magyaros kiejtés vagy '') vagy None. Héberül jóváhagyott kiejtés híján gépi, jelölve (DT-F131y); ha az
    sincs, '' (a KIEJTES_HIANY-ba kerül)."""
    pontos, alap = tbesg_tbesh_index()
    nyers = pontos.get(LEMMA_VALTOZAT.get(strong, strong)) or pontos.get(strong) or alap.get(strong)
    if not nyers:
        return None
    lemma, step = nyers
    if strong.startswith('G'):
        return lemma, gorog_magyaros(step)
    hu = heber_lemma_kiejtes(lemma, step)
    if not hu:
        # DT-F131y: jóváhagyott kiejtés híján gépi, jelölve (a TBESH-lemma első alakjából: „X, Y” → X)
        hu = heber_gepi(lemma.split(',')[0].strip())
    if not hu:
        KIEJTES_HIANY.setdefault(strong, (lemma, step))
        return lemma, ''
    return lemma, hu


# ---------------------------------------------------------------------------
# Marker-blokk
# ---------------------------------------------------------------------------

def _cel_kulcs(motivum_id, blokk_nev):
    return 'lexikon#%s#%s' % (motivum_id, blokk_nev)


def _lexikon_blokk(motivum_id, blokk_nev, forras_lista, licenc_lista, hatokor_sor, torzs, olvasoi=None):
    """A generált blokk. `olvasoi`: a „Mit mutat ez a rész?” olvasói bekezdés (OLVASOI_SABLON), közvetlenül a
    szakaszcím alatt, az üzemeltetői hatókör-mondat előtt; az utóbbi változatlan."""
    cel_kulcs = _cel_kulcs(motivum_id, blokk_nev)
    fejl = '<!-- GENERÁLT-KEZDET: general.py --cel %s | forrás: %s | licenc: %s | ts=%s -->' % (
        cel_kulcs, ', '.join(forras_lista), ', '.join(licenc_lista), G.TS)
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % cel_kulcs
    return '\n\n'.join([fejl] + ([olvasoi_bekezdes(olvasoi)] if olvasoi else []) + ['*%s*' % hatokor_sor, torzs, veg])


# --- Olvasói bevezető („Mit mutat ez a rész?”) — ISTENTISZT-001 arany lap, 2026-10-29 ---
# Minden generált szakasz és minden szerep-blokk a cím alatt 1–3 mondatos olvasói bevezetőt kap. A mondatok sablonok,
# az adatból töltve (szám, szó, kiejtés); motívumra szabott kézi értelmezés nincs bennük, fájlnév és szerepkód sem.

# a címke 2026-11-03-tól nem látszik (a felhasználó észrevétele); a bekezdést a végén álló láthatatlan jel azonosítja
OLVASOI_CIMKE = '<!-- olvasói -->'
OLVASOI_SABLON = {
    'tartalom': 'A lap szakaszai. Hogy melyik szakaszt ki írta, a Kolofon szerzőségi mondata mondja meg.',
    'jelmagyarazat': 'A lapon használt rövidítések, jelek és forrásnevek feloldása. Ha a lap egy jelét nem érted, '
                     'itt keresd.',
    'elofordulasok': 'A motívum %(n)d igehelye a bibliai könyvek sorrendjében (%(reszek)s), mindegyik a Károli-fordítás '
                     'szövegével. Soronként látszik, melyik szó hordozza a motívumot, és mit jelent az adott versben.',
    'kizart': 'Ezeket a helyeket megvizsgáltuk, de nem tartoznak a motívumhoz, vagy a döntés még nyitott '
              '(%(reszek)s). Mindegyiknél látszik, miért került a vizsgálatba, és miért maradt ki.',
    'kizart_ures': 'Itt állnának a megvizsgált, de a motívumból kizárt helyek; ennél a motívumnál nincs ilyen.',
    'szocikkek': 'A motívumot hordozó szavak szótári háttere: %(szavak)s. Minden szónál számozott pontok követik '
                 'egymást; a 2. pont a fő szótár (%(fo)s) szócikke.%(gerinc)s',
    'szocikkek_gerinc': ' Ott elöl, kibontva állnak azok a jelentések, amelyek a motívumot hordozzák; a többi '
                        'szótár utána következik.',
    'lxx': 'Ez a táblázat azt mutatja meg, hogyan fordította a Septuaginta (LXX) a motívum %(n)d ószövetségi helyét: '
           'ugyanazzal a görög szóval, amelyet az Újszövetség is használ, vagy mással. Összesítve: %(osszegzes)s.',
    'lxx_ures': 'Itt állna, hogyan fordította a Septuaginta (LXX) a motívum ószövetségi helyeit; ennek a motívumnak '
                'nincs ószövetségi előfordulása.',
    'kereszthivatkozasok': 'Mely más bibliai helyekre utalnak a motívum helyeiről a hagyományos kereszthivatkozás-'
                           'gyűjtemények (a TSK és a Károli-Biblia utalásai). A motívum %(n)d igehelyéből %(talalt)d-nál '
                           'van ilyen utalás, összesen %(osszes)d.',
    'kapcsolatok': 'A motívum igehelyei közötti kapcsolatok (%(n)d): melyik hely melyikkel áll kapcsolatban, milyen '
                   'jellegű ez a kapcsolat, és mennyire biztos.',
    'kapcsolatok_ures': 'Itt állnának a motívum igehelyei közötti kapcsolatok; ennél a motívumnál még nincs ilyen.',
    'kapcsolodo': 'Azok a más motívumok, amelyekkel ez a motívum kapcsolatban áll. Ugyanez a sor a másik motívum '
                  'lapján is megjelenik.',
    'idezes': 'Hogyan hivatkozz erre a lapra, és mely szótárakból, adatforrásokból készült.',
    'kolofon': 'A lap technikai adatai: a motívum azonosítója és állapota, és minden forrás, amelyből a lap készült.',
    '1a': 'A fenti táblázat igehelyeinek teljes szövege a Károli-fordításban, a motívumot hordozó szavakkal.',
    'nyelv': 'A motívumot hordozó %(nyelv)s szavak (%(szavak)s) szótári anyaga, számozott pontokban: minden pont egy '
             'kérdésre felel (alapjelentés, fő szótár, teológiai szócikk, jelentésmező, …).',
    # F182 (A09; F8): az új szerkezetű lapon írással és kiejtéssel, a pontrendszer magyarázata a Jelmagyarázatban
    'nyelv_uj': 'A motívumot hordozó %(nyelv)s szavak: %(szavak)s. Szavanként a szótári adatok a 4.1–4.%(utolso)d pontban.',
    # F12 (TEREMT-002, az első motívum görög szó nélkül): az ÜRES-NYELV blokk olvasói bevezetője (Feed 6. kapu)
    'nyelv_ures': 'A motívum %(nyelv)s szavainak szótári anyaga. A motívumnak ezen a nyelven nincs saját szava, ezért '
                  'ez a rész üres; a szótári anyag a másik nyelv szavainál áll.',
    'nyelvfuggetlen': 'A szavakon túli, a motívum egészére vonatkozó pontok: tematikus mutató, a Károli-fordítás magyar '
                      'szavai, és a rejtett vagy hamis párhuzamok.',
    'rokon': 'A motívum szavaival rokon, a lapon hivatkozott szavak (%(szavak)s) szótári anyaga.',
}
# A rések (kézi vagy adatból generált) olvasói bevezetője: a generátor írja a rés címe alá (ISTENTISZT-001 arany lap, 2026-10-29); a rés törzse
# (a kézi próza) változatlan.
OLVASOI_RES = {
    'kivonat': 'A motívum rövid összefoglalása: miről szól, és hol fordul elő a Bibliában.',
    '2b': 'A fenti szótári anyagon túli, kiegészítő szótári adatok.',  # DT-F174a: adat nélkül a rés nem áll a lapon
    'miert_fontos': 'Miért jelentős a fenti szótári anyag a motívum szempontjából.',
    'minosites': 'Ez a rész megmutatja, hogy a motívum helyeit két, tőlünk független kereszthivatkozás-gyűjtemény (a '
                 'Treasury of Scripture Knowledge és a Károli-biblia kereszthivatkozásai) mennyire köti össze '
                 'egymással. Minél több hely kap ilyen kapcsolatot, annál erősebb a motívum külső megerősítése.',
    'alatamasztas': 'Soronként, miért kapta a fenti kapcsolat a funkcióját és a bizonyossági szintjét.',
    'ertelmezes': 'A motívum értelmezése a PaRDeS négy szintjén: szó szerinti értelem, utalás, tanítás, mélyebb réteg. '
                  'Az állítások alatt a mért adat forrása áll.',
    'alkalmazas': 'Mit jelent a motívum a hívő életében ma.',
    'tanitoi': 'Nevesített bibliatanítók, akik a motívumról ugyanerre jutottak, forrásmegjelöléssel.',
    'modszertan': 'Hogyan készült a kutatás: a döntések, a korlátok és a nyitva maradt kérdések.',
}
# A szerep-blokkok (2. Szótári háttér, „#### n.” pontok) olvasói mondata; (nyelv, sorrend), a nyelv nélküli kulcs
# mindkét nyelvre áll.
OLVASOI_SZEREP = {
    1: 'A szó alapjelentése röviden, a STEPBible rövid szótára szerint.',
    2: 'A szó fő szótári szócikke (%(fo)s).',
    ('gorog', 2, 'gerinc'): 'A szó jelentéseinek teljes rendje a fő szótárban (Thayer). Kibontva azok a jelentések '
                            'állnak, amelyek a motívumot hordozzák; a többi összecsukva.',
    ('heber', 2, 'gerinc'): 'A szó jelentéseinek teljes rendje a fő szótárban (BDB). Kibontva azok a jelentések '
                            'állnak, amelyek a motívumot hordozzák; a többi összecsukva.',
    3: 'Teológiai szócikk a szóról (mit jelent a bibliai gondolkodásban), vagy a hivatkozás arra, ahol olvasható.',
    4: 'A szó helye a jelentéstani mezők rendszerében: milyen rokon jelentésű szavakkal tartozik egy csoportba.',
    5: 'A szó jelentései tömören, vagy a hivatkozás arra, ahol a jelentések teljes listája olvasható.',
    ('gorog', 6): 'Hogyan kapcsolódik a görög szó a héber Ószövetséghez: a Septuaginta (LXX) a motívum ószövetségi '
                  'helyein ugyanezt a szót használja-e.',
    ('heber', 6): 'A görög fordítás (Septuaginta, LXX) a motívum helyein, ahol ez a szó áll, a motívum görög szavát '
                  'használja-e; és a teljes Ószövetségben mely görög szavak állnak a szó versei mellett.',
    7: 'Mely szavak felelnek meg ennek a szónak a másik bibliai nyelven, egy kétnyelvű szótár (SECE) szerint; a '
       'motívum saját szava kiemelve.',
    ('gorog', 8): 'A szó tágabb nyelvi háttere a klasszikus görög nagyszótárban (LSJ).',
    ('heber', 8): 'A szó eredete és nyelvi háttere.',
    9: 'Hogy az egyes versekben a szó melyik jelentésében áll.',
    10: 'A szó magyaros kiejtése.',
    12: 'Mely témákhoz sorolja a szót és helyeit egy régi bibliai témagyűjtemény (Nave).',
    13: 'A motívum igehelyein a Károli-fordítás ezekkel a magyar szavakkal adja vissza a motívumot hordozó kifejezést '
        '(a héber és a görög szavakat együtt, nem szavanként). A zárójeles szám azt mutatja, hány igehelyen áll a szó; '
        'utána a ragozott alakok és az igehelyek.',
    # F123.ANTROP2 (olvasói kapu, BELSO): a „gerinc” belső szó helyett olvasói megnevezés
    14: 'Két ellenőrzés a motívum héber és görög szavaira (l. „A motívum kulcsszavai”) és a Károli magyar '
        'kulcsszavaira. **Rejtett párhuzam:** a motívum olyan helye, ahol az eredeti szövegben a motívum szavai állnak, '
        'de a Károli nem a szokásos magyar kulcsszavakkal fordítja, így a magyar olvasó nem ismeri fel. **Hamis '
        'párhuzam:** olyan vers, ahol a Károliban ugyanazok a magyar kulcsszavak állnak, de az eredetiben nem a motívum '
        'szavai, így a magyar olvasó tévesen kapcsolná ide.',
}


_motivumok_cache = None


def motivum_mezo(ctx, mezo):
    """A motívum `motivumok.tsv`-sorának mezője (a ctx `sorai` első sorának `id`-je szerint), vagy ''."""
    global _motivumok_cache
    if _motivumok_cache is None:
        _motivumok_cache = {r['id']: r for r in L.read_tsv_skip_comments(os.path.join(ADAT, 'motivumok.tsv'))}
    sorai = ctx.get('sorai') or []
    return ((_motivumok_cache.get(sorai[0].get('id')) or {}).get(mezo) or '').strip() if sorai else ''


def ikon_nelkul(szoveg):
    """A szöveg elejéről leszedi az ikont/emojit (nem betű, nem számjegy, nem idézőjel/zárójel)."""
    return re.sub(r'^[^\w"„(]+', '', szoveg or '')


def olvasoi_bekezdes(szoveg):
    return '%s%s' % (szoveg, OLVASOI_CIMKE)   # a jel a sor végén áll: a sor elején álló <!-- … --> HTML-blokk lenne, és a szöveg nyersen jelenne meg


def olvasoi(kulcs, **adat):
    return OLVASOI_SABLON[kulcs] % adat if adat else OLVASOI_SABLON[kulcs]


# A felhasználó átnézése (4., 7.): az új szerkezetű lap szótári pontjainak bevezetője; a forrás és a soronként ismétlődő
# címke itt áll egyszer.
UJ_OLVASOI_SZEREP = {
    ('heber', 1): 'A szó alapjelentése röviden, a STEPBible héber rövid szótára (TBESH, CC BY 4.0) szerint, magyarul; a '
                  'teljes szócikk a szónézetben.',
    ('gorog', 1): 'A szó alapjelentése röviden, a STEPBible görög rövid szótára (TBESG, CC BY 4.0) szerint, magyarul; a '
                  'teljes szócikk a szónézetben.',
    ('heber', 3): 'Szavanként a translationWords (unfoldingWord, CC BY-SA 4.0) magyar szócikkcímei és a szó TWOT-száma: '
                  'a szócikk száma a Theological Wordbook of the Old Testamentben. A szócikkek a szónézetben '
                  'olvashatók.',
    ('gorog', 3): 'Szavanként a translationWords (unfoldingWord, CC BY-SA 4.0) magyar szócikkcímei; a szócikkek a '
                  'szónézetben olvashatók.',
}


def olvasoi_szerep(nyelv, n, gerinc=False):
    """A szerep-blokk olvasói mondata, vagy None, ha a szerepre nincs sablon."""
    if gerinc and (nyelv, n, 'gerinc') in OLVASOI_SZEREP:
        return OLVASOI_SZEREP[(nyelv, n, 'gerinc')]
    szoveg = OLVASOI_SZEREP.get((nyelv, n), OLVASOI_SZEREP.get(n))
    if szoveg and '%(fo)s' in szoveg:
        szoveg = szoveg % {'fo': SZEREP_SZOTAR.get((nyelv, n), EM_DASH)}
    return szoveg


def szam_osszegzes(parok):
    """[(címke, szám)] -> „23 ószövetségi, 10 újszövetségi” — a nulla tagok nélkül."""
    return ', '.join('%d %s' % (n, c) for c, n in parok if n) or EM_DASH


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
    cimek = UJ_SZAKASZOK if uj_szerkezet(m['id']) else [cim for cim, _ in SZAKASZOK]   # F178.4
    sorok = ['- [%s](#%s)' % (cim, _heading_slug(cim)) for cim in cimek]
    hatokor = ('Ez a blokk a lexikon-oldal %d szakaszának tartalomjegyzékét adja (LEXV2_2_BRIEF.md G1).'
               % len(cimek))
    torzs = '\n'.join(sorok)
    return _lexikon_blokk(m['id'], 'tartalom', [], [LC('projekt_adat')], hatokor, torzs, olvasoi('tartalom'))


# ---------------------------------------------------------------------------
# Jelmagyarázat és rövidítések (közös szöveg minden oldalon, G10)
# ---------------------------------------------------------------------------

# A módszertani közlemények (`kozlemeny/`, F163) a lapról relatív hivatkozással érhetők el: a lap a `lexikon/` alatt áll,
# ezért a `../kozlemeny/…` út a repóban és bármely, a könyvtárszerkezetet megtartó közzétételben is a fájlra mutat. GitHub-URL
# nem kerül a lapra (a GitHub nem kanonikus forrás, 2026-11-04); a kanonikus közzétételi hely és a DOI helyőrző, amíg nincs meg.
KOZLEMENY = {
    'mi': '../kozlemeny/MI_NYILATKOZAT.md',
    'hays': '../kozlemeny/HAYS_LEKEPEZES.md',
    'recepcios': '../kozlemeny/PARDES_RECEPCIOS_KERET.md',
    'kozel_keleti': '../kozlemeny/KOZEL_KELETI_HATAR.md',
    'citation': '../CITATION.cff',
}
KANONIKUS_FORRAS_HELYORZO = '<KANONIKUS_FORRAS_URL>'
DOI_HELYORZO = '<DOI>'
LEXIKON_CIM_HELYORZO = '[HELYŐRZŐ: A LEXIKON CÍME]'
# a „Hogyan idézd” egyetlen mutató mondata a nyílt adatkészletre (F167.4); az ellenoriz.py 35. szabálya ezt keresi
NYILT_ADAT_MUTATO = 'A lap adatai (előfordulások, kizárt helyek) nyílt adatkészletként is elérhetők'
SZERZO_HELYORZO = '[HELYŐRZŐ: SZERZŐ NEVE]'

# A felhasználó döntései (2026-11-11, az orkesztrátor továbbításában): a szerző „Demeter Tamás”, a lexikon címe „Logosz-
# lexikon”, a kanonikus cím egyetlen beállításból („logoszlexikon.hu - a domain”): a szócikk állandó címe `<alap>/<ID>`, a
# kiadás változatcíme `<alap>/<ID>/<kiadás>`. Üres beállításnál olvasói mondat áll, nyers helyőrző nem (olvasói kapu:
# HELYORZO). Csak az új szerkezetű lapon; a nyílt mag, a CITATION.cff és a közlemények külön tétel.
SZERZO_NEV = 'Demeter Tamás'
# a lexikon neve (a felhasználó, 2026-11-11: „mehet” a javaslatra): magyar szövegben „Logosz-lexikon” (AkH. 12.:
# tulajdonnév + köznév, kötőjellel, kisbetűs köznév); angol metaadatban „Logosz Lexikon” — a lapon angol cím nem áll
LEXIKON_CIM_HU = 'Logosz-lexikon'
KANONIKUS_ALAP_URL = 'https://logoszlexikon.hu'
# a nyílt adatmag concept DOI-ja (Zenodo); a felhasználó (2026-11-11): Zenodo-feltöltés „még nem volt” — a HAMART kiadása
# után a felhasználó lépése, a kapott DOI ide kerül
# a felhasználó (2026-11-11): „nyílt adatmag doi: 10.5281/zenodo.24141612” — egy Zenodo-piszkozat lefoglalt DOI-ja; a
# rekord a HAMART kiadása után, ugyanezzel a DOI-val lesz közzétéve (addig a link nem oldódik fel: ez nem hiba)
NYILT_MAG_DOI = '10.5281/zenodo.24141612'
# a Károli–Strong párosítás lefoglalt DOI-ja (a felhasználó, 2026-11-11: „károli strong: 10.5281/zenodo.24141884”;
# Zenodo-piszkozat, a közzététel később); a Kolofon forrástáblájának sorában hivatkozásként áll
KAROLI_STRONG_DOI = '10.5281/zenodo.24141884'
KANONIKUS_URL_HIANY = 'a lap állandó webcíme az első nyilvános megjelenéskor kerül ide'
NYILT_ADAT_MUTATO_UJ = 'A lap adatai (előfordulások, kizárt helyek) nyílt adatkészletként is megjelennek'
DOI_HIANY = 'az adatkészlet DOI-ja az első Zenodo-közléskor kerül ide'


def kanonikus_cim(motivum_id, kiadas=None):
    """A szócikk állandó címe (`<alap>/<ID>`), kiadásszámmal a változatcím (`<alap>/<ID>/<kiadás>`); üres alapnál
    az olvasói mondat."""
    if not KANONIKUS_ALAP_URL:
        return KANONIKUS_URL_HIANY
    return '%s/%s%s' % (KANONIKUS_ALAP_URL.rstrip('/'), motivum_id, ('/%s' % kiadas) if kiadas else '')

JELMAGYARAZAT_TORZS = """**PaRDeS-szintek** (`sablonok/PaRDeS_gyorsreferencia.md`):
- **Peshat** — a szöveg szerinti, szó szerinti értelem.
- **Remez** — csak felismerés/azonosítás, következtetés nélkül.
- **Drash** — normatív, következtető, alkalmazó.
- **Sod** — fegyelmezett, csak szövegből levezethető, gematria/allegorizálás nélkül.

A szint olvasási módot jelöl, nem a szöveg jelentését: a zsidó írásmagyarázat négyes sémájának kategóriáival mondja
meg, hogyan kapcsolódik a hely a motívumhoz (szó szerint, utalásként, következtetésként vagy spirituális olvasatban). Nem
kritikai állítás arról, mit szándékolt a bibliai szerző, és nem a szöveg eredeti, történeti jelentésének szintje. A
besorolást e munka adja, saját szabályai szerint; hogy egy nevesített magyarázó egy helyet ténylegesen hogyan olvasott,
azt a Tanítói egyezés dokumentálja, ahol van. Egy hely motívumhoz tartozásának bizonyítéka a héber és a görög szöveg, nem
a szint (részletesen: [A PaRDeS-szint mint recepciós címke](%(recepcios)s)).

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

**Kiejtés:** a héber és a görög szó mellett zárójelben a magyaros kiejtés, mindkét nyelven szabályos átírás. A
héber kiejtés a pontozott héber szövegből rögzített szabályokkal készül (pl. „וַיִּקְרָא (vajjikrá)”); ahol van kézzel
jóváhagyott alak, az áll. A ragozott szó mellett a saját kiejtése áll, nem a szótári alaké.

**Olvasói bevezető** — minden blokk elején egy-két mondatos összefoglaló; az alatta álló dőlt, technikai
mondat a lap készítőinek szól.

**Proveniencia-sor** (dőlt, `scope=… | forras=… | ts=…` alakú): honnan és mikor származik a fölötte álló adat — milyen
körre (`scope`), melyik adattáblából vagy lekérdezésből (`forras`), mikor (`ts`); a `manual` kézi rögzítést jelöl. Az
ellenőrzéshez való, olvasáskor átugorható.

**Közös forrásmegjelölés** (‹E1›, ‹K1›, ‹M1› …): ha egy blokk több sora ugyanabból a forrásból jön, a soron csak a jel
áll, a teljes proveniencia-sor egyszer, a blokk alatt. Az előtag a blokkot jelöli: E az előfordulások, K a kizárt és
vizsgált helyek, M a minősítés.

**Héber rövidítések a BDB-szövegben** (kiemelve; az egérmutató alatt a feloldás): a BDB a gyakori szavakat egy
betűvel és a rövidítő jellel (׳, geres) írja. **י׳** = יְהוָה (JHVH), a Károliban „az Úr”; a szócikk címszavának
kezdőbetűje (pl. **ק׳** a קָרָא szócikkében, **שׁ׳** a שֵׁם szócikkében) maga a címszó. Más betűnél a feloldás a
szócikk szövegéből derül ki.

A szótári fordításokban a πνεῦμα (pneuma) mindig *szellem*, a ψυχή
(pszükhé) *lélek*; a Károli-idézetek szövege változatlan (pl. »Lélek«).""" % KOZLEMENY


def blokk_jelmagyarazat(m):
    hatokor = 'Ez a blokk közös, minden lexikon-oldalon szó szerint azonos szöveg (G10).'
    return _lexikon_blokk(m['id'], 'jelmagyarazat', [], [LC('projekt_adat')], hatokor, JELMAGYARAZAT_TORZS,
                          olvasoi('jelmagyarazat'))


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
    """F121 (DT393): az „UBS-jelentés” cella egy eleme: a rövid magyar glossza (`glosszak_hu`, a gyorsítótárból;
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
        # F121 (DT393): a cellában a kód és a rövid glossza áll, mellette ⓘ a szónézetre (a teljes UBS-szócikk ott)
        szoveg = ubs_glossza_cella('UBS_DNTG', strong, lexid, entry_kod, glosszak)
        jelolt = '' if egyertelmu == 'igen' else ' *(jelölt, nem egyértelmű)*'
        tokenenkent.setdefault(strong, []).append('%s%s' % (szoveg, jelolt))   # a 15 jegyű kód nem látszik (2026-11-03)

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


def ragozott_kiejtessel(ragozott, kiejtes, forras):
    """„ragozott (kiejtés)”. Héberül (DT-F131y, 2026-10-30) a teljes ragozott szó saját gépi kiejtése, jelölve:
    „וַיִּקְרָא (vajjikrá, gépi)”; pontozatlan alaknál a szótári alak kiejtése, jelölve: „(szótári alak: kárá)”
    (forras='TAHOT_LEMMA'); görögül a ragozott alak gépi magyaros kiejtése, jelölés nélkül."""
    if not kiejtes:
        return ragozott
    return '%s (%s%s)' % (ragozott, SZOTARI_ALAK_ELOTAG if forras == 'TAHOT_LEMMA' else '', kiejtes)


SZOTARI_ALAK_ELOTAG = 'szótári alak: '


# A felhasználó döntése (2026-11-12, „Mindhármat”; a lektor és a Fable közös véleménye): a lánc szava nélküli tematikus
# sor a vers saját szavát mutatja (TAGNT: Jel 22:3 κατάθεμα G2652 minden kiadásban); csak a 2. tábla sorában, adat nélkül.
TEMATIKUS_SAJAT_SZO = {('HAMART-001', 'Jel 22:3'): 'G2652'}


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
            ragozott, kiejtes, forras = talalat
            ragozott = _RAGOZOTT_ZARO_IRASJEL_RE.sub('', ragozott)
            reszek.append(ragozott_kiejtessel(ragozott, kiejtes, forras))
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
            jelentes_szo, jelentes_ik = jelentes_cella(g_adat, s, uj=uj_szerkezet(m['id']))
        if proveniencia or igazolas or jelentes_ik:
            lj = 'proveniencia: %s | igazolas: %s' % (proveniencia or EM_DASH, igazolas or EM_DASH)
            if jelentes_ik:
                lj += ' | jelentés-címke: %s' % jelentes_ik
            labjegyzetek.append(lj)
            labjegyzet_jel = '[^%d]' % len(labjegyzetek)

        if gerinc:
            szotari_jelentes = '%s%s' % (jelentes_szo, labjegyzet_jel)
        else:
            szotari_jelentes = lexikon_jelentes_cella(s)
        ubs_cella = ubs_jelentes_cella(s['id'], s['igehely'], s.get('strong') or '')
        if gerinc and ubs_cella.startswith('%s *(ÓSZ)*' % EM_DASH):
            # F131 (DT380): az ÓSZ-sorok UBS-jelentése a DBH-ból
            ubs_cella = dbh_jelentes_cella(s['igehely'], s.get('strong') or '')
        if uj_szerkezet(s['id']) and (s.get('gerinc_elem') or '').startswith('tematikus:')                 and ubs_cella == '%s *(nincs G-token)*' % EM_DASH:
            # lap-javit HAMART-001 (orkesztrátor, lektor 46.): a tematikus hely cellája olvasói magyarázattal
            ubs_cella = '%s *(tematikus hely: a lánc szava nélkül áll a lapon, l. a Kivonatot)*' % EM_DASH
        megb = '%s · %s%s' % (s.get('megbizhatosag') or EM_DASH, s.get('azonositas_modja') or EM_DASH,
                               labjegyzet_jel)

        funkcio_teljes = s.get('funkcio') or ''
        funkcio_cimke, _sep, funkcio_magyarazat = funkcio_teljes.partition(' — ')
        if funkcio_teljes and not _sep:
            # DT-F1Ab: „ — ” nélkül a „: ” utáni rész, annak híján a teljes érték (a vezető emoji nélkül)
            # az 1/a „Funkció:” sorába; a táblázat cellája változatlanul a teljes érték
            _c, sep2, utana = funkcio_teljes.partition(': ')
            funkcio_magyarazat = utana if sep2 else re.sub(r'^[^\w"„(]+', '', funkcio_teljes)
        # 2026-11-03: a cellában és az 1/a „Funkció:” sorában nincs vezető ikon/emoji, a szöveg marad
        funkcio_cella = ikon_nelkul(funkcio_cimke) if funkcio_teljes else EM_DASH
        funkcio_magyarazat = ikon_nelkul(funkcio_magyarazat)

        sajat = TEMATIKUS_SAJAT_SZO.get((m['id'], s['igehely']))
        if gerinc and uj_szerkezet(m['id']) and sajat and labjegyzet_jel:
            # a felhasználó döntése (2026-11-12, „Mindhármat”): a tematikus sor a másik három mintájára a vers saját,
            # nem lánc-szavát mutatja (TAGNT); az adat (`elofordulasok.tsv` strong) változatlan, ezért a szó a 4.
            # szakaszban nem kap szócikket
            labjegyzetek[-1] = labjegyzetek[-1].replace(
                'jelentés-címke: a sornak nincs Strong-tokenje',
                'jelentés-címke: Tematikus hely: a vers görög szava, a %s nem a lánc szava; forrás: a STEPBible görög '
                'szövege (TAGNT), %s' % (kulcsszo_cella({'igehely': s['igehely'], 'strong': sajat}), sajat))
            sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                igehely_link, kulcsszo_cella(dict(s, strong=sajat)), 'tematikus hely: a lánc szava nélkül', funkcio_cella,
                s.get('pardes_szint') or EM_DASH, sajat, ubs_jelentes_cella(s['id'], s['igehely'], sajat), megb))
        elif gerinc and uj_szerkezet(m['id']) and (s.get('gerinc_elem') or '').startswith('tematikus:') \
                and not (s.get('strong') or '').strip():
            # a felhasználó átnézése (3.): a lánc szava nélküli tematikus sor: a Károli-szó, rövid megjegyzés, a jegyzet
            # egyszer (a sor végén), „— —” és üres gondolatjel-cella nélkül; a vers saját görög szava nem áll (nincs
            # róla döntés)
            sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                igehely_link, s.get('karoli_szo') or EM_DASH, 'tematikus hely: a lánc szava nélkül', funkcio_cella,
                s.get('pardes_szint') or EM_DASH, 'nincs lánc-szó', 'nem alkalmazható (tematikus hely)', megb))
        elif gerinc:
            sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                igehely_link, kulcsszo_cella(s), _cella(szotari_jelentes), funkcio_cella,
                s.get('pardes_szint') or EM_DASH, s.get('strong') or EM_DASH,
                ubs_cella, megb))
        else:
            sorok.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
                igehely_link, kulcsszo_cella(s), funkcio_cella,
                s.get('pardes_szint') or EM_DASH, s.get('strong') or EM_DASH,
                szotari_jelentes, ubs_cella, megb))

        tetelek_1a.append((anchor, s, funkcio_magyarazat))

    torzs = '\n'.join(sorok)
    if labjegyzetek:
        labjegyzetek, kozos = SZKZ.kozos_proveniencia(labjegyzetek, 'E')   # F152 B.2
        torzs += '\n\n' + '\n'.join('[^%d]: %s' % (i, lj) for i, lj in enumerate(labjegyzetek, start=1))
        if kozos:
            torzs += '\n\n' + kozos

    if gerinc:
        torzs += ('\n\n*Az UBS-jelentés az újszövetségi soroknál az UBS Dictionary of New Testament Greek (DNTG), '
                  'az ószövetségi soroknál az UBS Dictionary of Biblical Hebrew (DBH) igehelyszintű jelentése '
                  '(`%s`, a Károli-vers az MT-számozásra képezve, `konkordancia/Karoli_versmegfeleltetes.tsv`); '
                  'tokenenként a hivatkozott jelentés(ek) kódja és rövid glosszája; az ⓘ a szónézetre mutat, ahol a teljes '
                  'UBS-szócikk (definíció és glosszák) áll (DT393). A glossza magyarul a `forditasok.tsv`-ből jön, ahol van; '
                  'ahol nincs, az angol eredeti áll `(fordításra vár)` jelöléssel. Ahol a DBH a versre nem hivatkozik, a cella ezt kimondja.*'
                  % UBS_DBH_REFERENCIAK_FAJL)
    else:
        torzs += ('\n\n*Az UBS-jelentés csak újszövetségi soroknál áll: az UBS Greek New '
                  'Testament Dictionary az Újszövetséget fedi.*')

    torzs += '\n\n#### 1/a. Az igehelyek szövege\n\n%s\n' % olvasoi_bekezdes(OLVASOI_SABLON['1a'])
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
            reszek.append(SZKZ.olvasoi_indok(s['kapcsolodas']) or s['kapcsolodas'])
        if funkcio_magyarazat:
            reszek.append('\nFunkció: %s' % funkcio_magyarazat)   # új bekezdés: a renderelt nézetben is új sor
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
                    '(`%s`, `%s`, `%s`; a címke forrása a sor lábjegyzetében), a „Funkció (a motívumban)” '
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
    tesz = [G.konyv_teszamentum(G.konyv_token(s['igehely'])) for s in sorai]
    konyv_db = {}
    for s in sorai:
        k = G.konyv_token(s['igehely'])
        konyv_db[k] = konyv_db.get(k, 0) + 1
    olv = (OK.elofordulasok_uj if uj_szerkezet(m['id']) else OK.elofordulasok)(
        len(sorai), tesz.count('ÓSZ'), tesz.count('ÚSZ'), len(konyv_db),
        sorted(konyv_db.items(), key=lambda x: (-x[1], x[0])),
        sum(1 for s in sorai if (s.get('megbizhatosag') or '').strip() == 'magas'),
        **({'konyvnev': konyv_teljes_nev} if uj_szerkezet(m['id']) else {})) or \
        olvasoi('elofordulasok', n=len(sorai),
                reszek=szam_osszegzes([('ószövetségi', tesz.count('ÓSZ')), ('újszövetségi', tesz.count('ÚSZ'))]))
    blokk_szoveg = _lexikon_blokk(m['id'], 'elofordulasok', forras_lista, licenc_lista, hatokor, torzs, olv)
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


def blokk_kizart(m, n_motivum=0):
    sorok_ehhez = [r for r in jeloltek_sorok() if r['id'] == m['id'] and r.get('dontes') in ('elutasítva', 'nyitva')]

    reszek = []
    labj = []
    kizart_olv = None
    if sorok_ehhez:
        # ISTENTISZT-001 arany lap, 2026-10-29: csoportosítva aszerint, miért lett jelölt; a döntés és az indok, fent az
        # elutasítási okok összesítője (eszkozok/szerep_kizart.py, adat/elutasitasi_okok.tsv); a nyers forrás lábjegyzetben
        cs_n = csoport_n(m['id']) if uj_szerkezet(m['id']) else None   # F182 (K34)
        tablak, labj, ossz = SZKZ.blokk_torzs(sorok_ehhez, m['id'], strong_cim=strong_cim, csoport_n=cs_n)
        okok = sorted(((k, v) for k, v in ossz['ok'].items() if k != 'nyitott döntés'),
                      key=lambda x: (-x[1], x[0]))
        # F123.TUD1B: verseket számol; az összesítő sor versszáma a `forras_kereses`-ből (szerep_kizart.csoport_versszam)
        v = SZKZ.vizsgalt_versek(sorok_ehhez, csoport_n=cs_n)
        kizart_olv = (OK.kizart_uj if uj_szerkezet(m['id']) else OK.kizart)(v['egyenkent'], v['csoport_vers'], v['csoport_sor'], v['elutasitva'], v['nyitva'], okok,
                               [(c, ossz['forras'][c]) for c in SZKZ.CSOPORTOK if ossz['forras'].get(c)], n_motivum)
        reszek.append(SZKZ.osszesito_sor(ossz))
        reszek.extend(tablak)
    else:
        reszek.append('Ehhez a motívumhoz nincs kizárt vagy nyitva maradt jelölt.')

    negativ = (m.get('negativ_kriterium') or '').strip()
    if negativ:
        reszek.append('**Negatív kritérium:** %s' % (SZKZ.olvasoi_indok(negativ) or negativ))
    if labj:
        labj, kozos = SZKZ.kozos_proveniencia(labj, 'K')   # F152 B.2
        reszek.append('\n'.join('[^k%d]: %s' % (i, t) for i, t in enumerate(labj, 1)))
        if kozos:
            reszek.append(kozos)
    torzs = '\n\n'.join(reszek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d elutasított/nyitva maradt jelöltjét fedi a '
               '`jeloltek.tsv`-ből (G7).' % (m['id'], len(sorok_ehhez)))
    nyitott = sum(1 for r in sorok_ehhez if r.get('dontes') == 'nyitva')
    olv = ((kizart_olv or olvasoi('kizart', reszek=szam_osszegzes([('elutasítva', len(sorok_ehhez) - nyitott),
                                                                    ('nyitott', nyitott)])))
           if sorok_ehhez else olvasoi('kizart_ures'))
    return _lexikon_blokk(m['id'], 'kizart', ['adat/jeloltek.tsv', 'adat/motivumok.tsv'],
                           [LC('projekt_adat')], hatokor, torzs, olv), \
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


UJ_DOMEN_MAGYAR = [False]   # F182: a render idejére az új szerkezetű motívumnál igaz (`run`)


def domen_magyar(szotar, kod, label, strong):
    hu = forditas_ehhez(szotar, strong, kod, 'domen', 'glosszak_hu')
    return hu if hu else '%s %s' % (label, FORDITASRA_VAR)


def tw_cim_magyar(c):
    """F182 (A11): a tW-szócikk magyar címe (fordítási gyorsítótár), fordítás nélkül az angol cím „fordításra vár”-ral."""
    hu = forditas_ehhez('tW_szocikkek', c['strong'].split('+')[0], c['tw_id'], 'cim', 'glosszak_hu')
    return hu if hu else '%s %s' % (c['cim'], FORDITASRA_VAR)


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
    if jelentes_szam == 'tagolatlan':  # DT438: a szócikk nem tagol (pl. H0922), a sor a teljes szócikkfej
        return '(tagolatlan szócikk)'
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
        fejlec = '%s %s — %s' % (cim_hash, strong, lemma_cim(lk))
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
    if UJ_DOMEN_MAGYAR[0]:
        # F182 (A12, K11): az új szerkezetű lapon a doménnév magyarul (fordítási gyorsítótár), a kód nélkül; fordítás
        # nélkül az angol név „fordításra vár” jelöléssel
        domen_szoveg = '; '.join(domen_magyar('SDBH' if strong.startswith('H') else 'SDGNT', kod, label, strong)
                                 for kod, label in domenek) if domenek else EM_DASH
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
        alszakasz.append('Ehhez a szóhoz nincs rögzített szótári jelentés-hivatkozás.')
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
    ('gorog', 8): 'a motívum saját tokenjeihez nincs LSJ-sor a `lexikon_hivatkozasok.tsv`-ben',
    ('gorog', 9): 'l. az 1. szakasz táblázatát (UBS-jelentés oszlop; csak újszövetségi sorok)',
}
# A 7. szerep (SECE) adatosított (F09 S2.4, DT189): a megfelelő-lista a szerep tartalma. A korábbi „kézi
# SECE-táblázatok a 2/b-ben a #70-ig” mutató megszűnt (ISTENTISZT-001 arany lap, 2026-10-29): a 2/b rés generált
# (`adat/lexikon_hivatkozasok.tsv`), kézi SECE-táblázat nincs benne.


def _hivatkozas_szoveg(nyelv, n, ctx):
    """A szerep hivatkozás-szövege. A görög 8. (LSJ) a motívum adatából: ha a saját tokenekhez nincs LSJ-sor, a rokon
    szavak közül azokat nevezi meg, amelyeknek van (a „Rokon szavak” blokkban állnak); ha egyiknek sincs, jelölt hiány."""
    hiv = SZEREP_HIVATKOZAS[(nyelv, n)]
    if (nyelv, n) != ('gorog', 8):
        return hiv
    sorai = ctx.get('sorai') or []
    tokenek = motivum_strong_tokenek(sorai)
    lsj = {r.get('strong') for r in lexikon_hivatkozasok_sorok() if r.get('szotar') == 'LSJ'}
    gorog = [t for t in tokenek if t.startswith('G')]
    csonk = [t for t in gorog if lsj_csonk(t)]
    rokon = [t for t in rokon_szavak_strongok(sorai, tokenek) if t.startswith('G') and t in lsj]
    if csonk and len(csonk) == len(gorog):
        # ISTENTISZT-001 arany lap, 2026-10-29: az összetett ige LSJ-szócikke csak az alapigéhez irányít; a tartalom az alapige szócikkében
        reszek = []
        for t in csonk:
            alap = re.findall(r'\bG\d+\b', lsj_csonk(t))[-1:]
            alap = ['G%04d' % int(alap[0][1:])] if alap else []
            lk = lemma_kiejtes_szabaly(alap[0]) if alap else None
            reszek.append('%s: az összetett ige LSJ-szócikke az alapigéhez irányít%s (a `%s` sora: „%s”)'
                          % (t, ' (%s, %s, %s)' % (lk[0], lk[1], alap[0]) if lk else '', LSJ_TELJES_FAJL,
                             lsj_csonk(t)))
        hiv = '; '.join(reszek)
        if rokon:
            return '%s; az alapige LSJ-szócikke a rokon szavaknál áll (alább): %s.' % (hiv, ', '.join(rokon))
        return '%s; az alapige LSJ-szócikke nincs bekötve: jelölt hiány.' % hiv
    if rokon:
        return '%s; LSJ-szócikk a rokon szavaknál (alább): %s.' % (hiv, ', '.join(rokon))
    return '%s, és a rokon szavaknál sincs: jelölt hiány.' % hiv


LSJ_TELJES_FAJL = 'konkordancia/LSJ_teljes.tsv'
# Utaló csonk: a szócikk csak a képzés leírása (pl. „ἐπικαλεìομαι Middle voice from G1909 and G2564”).
LSJ_CSONK_RE = re.compile(r'^\S+ (?:Middle voice |Passive voice )?from G\d+(?: and G\d+)?\.?$')
_lsj_cache = None


def lsj_csonk(strong):
    """A `LSJ_teljes.tsv` szócikke, ha az csak utaló csonk (lásd LSJ_CSONK_RE); különben None."""
    global _lsj_cache
    if _lsj_cache is None:
        _lsj_cache = {r['Strong_padded']: r['Teljes_szocikk']
                      for r in L.read_tsv_skip_comments(os.path.join(ROOT, LSJ_TELJES_FAJL))}
    sz = (_lsj_cache.get(strong) or '').strip()
    return sz if sz and LSJ_CSONK_RE.match(sz) else None
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
    DT-F42a); (2) a `lexikon_hivatkozasok.tsv` TBESH-sora (bekötött
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


_lemma_strong_cache = None
_glosszak_heber_cache = None


def lemma_strong_index():
    """NFC-lemma -> a betűutótag nélküli Strong-számok rendezett listája, a TBESG/TBESH lemmáiból és a SECE
    címszavaiból (a SECE megfelelő-listája csak a szóalakot adja; a Strong-szám ebből párosul, több találatnál
    mind)."""
    global _lemma_strong_cache
    if _lemma_strong_cache is None:
        idx = {}

        def hozzaad(lemma, strong):
            kulcs = unicodedata.normalize('NFC', lemma.strip())
            if kulcs and strong[:5] not in idx.setdefault(kulcs, []):
                idx[kulcs].append(strong[:5])
        for strong, (lemma, _k) in tbesg_tbesh_index()[0].items():
            hozzaad(lemma, strong)
        for betu in ('G', 'H'):
            for r in L.read_tsv_skip_comments(os.path.join(ROOT, SECE_FAJL[betu])):
                hozzaad(r['Teljes_szocikk'].split(' (')[0], r['Strong_padded'])
        _lemma_strong_cache = {k: sorted(v) for k, v in idx.items()}
    return _lemma_strong_cache


_tbesg_glossza_cache = None


def tbesg_rovid_glossza(strong):
    """A TBESG rövid angol glosszája (7. oszlop), az első sor a betűutótag nélküli Strong-számra."""
    global _tbesg_glossza_cache
    if _tbesg_glossza_cache is None:
        _tbesg_glossza_cache = {}
        with io.open(TBESG_TXT, encoding='utf-8') as f:
            for sor in f:
                cols = sor.rstrip('\r\n').split('\t')
                if len(cols) > 6 and STRONG_TOKEN_RE.match(cols[0]):
                    _tbesg_glossza_cache.setdefault(cols[0][:5], cols[6].strip())
    return _tbesg_glossza_cache.get(strong)


def glosszak_heber_hu():
    """strong -> az `adat/glosszak_heber_hu.tsv` fő sora (`fo` = igen)."""
    global _glosszak_heber_cache
    if _glosszak_heber_cache is None:
        _glosszak_heber_cache = {r['strong']: r for r in L.read_tsv_skip_comments(os.path.join(ROOT, GLOSSZAK_HEBER_HU_FAJL))
                                 if r.get('fo') == 'igen'}
    return _glosszak_heber_cache


def strong_cim(strong):
    """A prózában jelölt Strong-szám `title`-je (DT-F181b): a szám és — ha van — a rövid magyar jelentés („H4196 · oltár”);
    magyar jelentés híján csak a szám (a „fordításra vár” jelzés nem kerül az egérfeliratba)."""
    szoveg, van_magyar = rovid_jelentes(strong)
    return '%s · %s' % (strong, szoveg) if van_magyar and szoveg != EM_DASH else strong


def rovid_jelentes(strong):
    """(szöveg, van_magyar): a rövid magyar jelentés — héberül a `glosszak_heber_hu.tsv`; görögül magyar rövid
    a `forditasok.tsv` `TBESG | <Strong> | <Strong> | rovid | glosszak_hu` sora (F121, DT-F121o); ahol nincs, a TBESG
    rövid angol glosszája + `fordításra vár`; ha az sincs, EM_DASH."""
    if strong.startswith('H'):
        g = glosszak_heber_hu().get(strong)
        if not g:
            return EM_DASH, False
        if g.get('glossza_hu'):
            return _cella(g['glossza_hu']), True
        return '%s %s' % (_cella(g.get('glossza_en') or EM_DASH), FORDITASRA_VAR), False
    hu = forditas_ehhez('TBESG', strong, strong, 'rovid', 'glosszak_hu')   # F121 (DT-F121o)
    if hu:
        return _cella(hu), True
    en = tbesg_rovid_glossza(strong)
    if not en:
        return EM_DASH, False
    return '%s %s' % (_cella(en), FORDITASRA_VAR), False


def _sece_kiejtes(szo, strong):
    """A SECE-listában kiírt alak kiejtése: ha a görög alak nem a TBESG-lemma (pl. διαῤῥήσσω ↔ διαρρήγνυμι), a kiírt
    alak gépi magyaros átírása; különben a kiejtés-szabály szerinti lemma-kiejtés (ELLENOR_ISTENTISZT_OLVASOI 6.)."""
    lk = lemma_kiejtes_szabaly(strong)
    if strong.startswith('G') and lk and unicodedata.normalize('NFC', lk[0]) != unicodedata.normalize('NFC', szo):
        return gorog_magyaros(gepi_atiras(szo))
    if (strong.startswith('H') and lk and _heber_alap(lk[0].split(',')[0]) != _heber_alap(szo)
            and HK.kiejt(szo) != HK.kiejt(lk[0].split(',')[0])):  # más pontírás, ugyanaz a szó (שְׁאֹול ↔ שְׁאוֹל): a lemmáé
        # DT-F131y: a kiírt héber alak nem a TBESH-lemma (זַעַק ↔ זְעָקָה): a kiírt alak jóváhagyott vagy gépi kiejtése
        return heber_lemma_kiejtes(szo, '') or heber_gepi(szo) or (lk[1] or EM_DASH)
    return lk[1] if lk and lk[1] else EM_DASH


def _heber_alap(alak):
    """A héber alak összevetési kulcsa: NFC, kantilláció és meteg nélkül, a magánhangzójelekkel."""
    return unicodedata.normalize('NFC', HK.tisztit(alak).replace(HK.METEG, '').strip())


def _rovid_kiejtes(strong):
    """A kiejtés-szabály szerinti kiejtés (kiejtés-szabály, ISTENTISZT-001 arany lap, 2026-10-29); héberül jóváhagyott alak
    híján a gépi, jelölve (DT-F131y); EM_DASH, ha az sincs (jelölt hiány)."""
    lk = lemma_kiejtes_szabaly(strong)
    return lk[1] if lk and lk[1] else EM_DASH


def _tartalom_sece(nyelv, n, tokenek_ny, reszek, ctx):
    """7. szerep (Megfelelők a másik nyelven): a SECE megfelelő-listája, olvasható táblázatban — a szó, a
    kiejtés, a Strong-szám (a TBESG/TBESH lemmájából párosítva) és a rövid magyar jelentés; a motívum saját
    szava jelölve. A sorrend és a szólista a SECE-é; ahol a szócikknek nincs ilyen mezője, `a forrás nem
    tárgyalja`. Gyakoriságot a SECE nem ad (ISTENTISZT-001 arany lap, 2026-10-29)."""
    out = []
    cimke = 'héber' if nyelv == 'gorog' else 'görög'
    sajat = set(motivum_strong_tokenek(ctx.get('sorai') or []))
    for t in tokenek_ny:
        tabla = sece_tabla(t, sajat)
        if not tabla:
            out.append('**%s** · %s *(SECE: nincs %s megfelelő-lista)*' % (t, NEM_TARGYALJA, cimke))
            continue
        out.append('**%s** · SECE — %s megfelelők (%d):' % (szo_cim(t), cimke, tabla[0]))
        out.append(tabla[1])
    if tokenek_ny:
        out.append(SECE_LABJEGYZET)
        for b in ('G', 'H'):
            ctx['fl'].setdefault(SECE_FAJL[b], set()).add(SECE_LICENC_KULCS[b])
    return out


SECE_LABJEGYZET = ('*A szólista és a sorrend a SECE-é (gyakoriságot nem ad; az ismétlődő szóalak egyszer áll); a '
                   'Strong-szám a TBESG/TBESH lemmájából vagy a SECE címszavából párosul; a rövid jelentés: héberül '
                   '`adat/glosszak_heber_hu.tsv`, görögül a TBESG angol glosszája (magyar rövid glossza-tábla a görögre '
                   'még nincs).*')


def sece_tabla(t, sajat):
    """(elemszám, táblázat-szöveg) a token SECE-megfelelőiből, vagy None: szó (a motívum szava kiemelve), kiejtés
    (a kiejtés-szabály szerint), Strong, rövid jelentés. A 7. szerep és a Rokon szavak közös formája (ISTENTISZT-001 arany lap, 2026-10-29);
    a SECE nyers szövege (LN, GK, TWOT) nem kerül a lapra (N-F33a)."""
    lista = sece_megfelelok(t)
    if not lista:
        return None
    masik = 'H' if t.startswith('G') else 'G'
    idx = lemma_strong_index()
    sorok = ['| Szó | Kiejtés | Strong | Rövid jelentés |', '|---|---|---|---|']
    for szo in lista:
        strongok = [x for x in idx.get(unicodedata.normalize('NFC', szo), []) if x.startswith(masik)]
        if not strongok:
            sorok.append('| %s | %s | %s | %s |' % (szo, EM_DASH, EM_DASH, EM_DASH))
            continue
        jel = []
        for x in strongok:
            szoveg, _van = rovid_jelentes(x)
            jel.append(szoveg if len(strongok) == 1 else '%s: %s' % (x, szoveg))
        motivum = any(x in sajat for x in strongok)
        szo_cella = '**%s** *(a motívum szava)*' % szo if motivum else szo
        strong_cella = (strongok[0] if len(strongok) == 1
                        else '%s *(a SECE csak a szóalakot adja)*' % ' vagy '.join(strongok))
        sorok.append('| %s | %s | %s | %s |' % (szo_cella, _sece_kiejtes(szo, strongok[0]), strong_cella, ' / '.join(jel)))
    return len(lista), '\n'.join(sorok)


LXX_SZAKASZ_LINK = '[3. LXX-fordítói döntések](#3-lxx-fordítói-döntések)'


def _lxx_ctx(ctx):
    if 'lxx' not in ctx:
        sorai = ctx.get('sorai') or []
        ctx['lxx'] = lxx_osszevetes(sorai, motivum_strong_tokenek(sorai))
    return ctx['lxx']


def _tartalom_gorog_lxx(nyelv, n, tokenek_ny, reszek, ctx):
    """Görög 6. szerep (LXX-híd): a 3. szakasz összegzése egy sorban, a szakaszra mutató hivatkozással
    (ISTENTISZT-001 arany lap, 2026-10-29)."""
    if not tokenek_ny:
        return []
    _sorok, szamlalo, _f, _h = _lxx_ctx(ctx)
    osszes = sum(szamlalo.values())
    if not osszes:
        return ['**%s** · a motívumnak nincs ószövetségi előfordulása, LXX-összevetés nincs.' % ', '.join(tokenek_ny)]
    if uj_szerkezet(ctx.get('id')):
        # F182 (A13): a görög szavak mondata (a fenti összegzés versszámai), a hivatkozás link
        csal = szamlalo.get('szocsalad', 0)
        return ['A motívum görög szavai (%s) az ószövetségi helyek %d verséből %d versben állnak a Septuaginta '
                'szövegében is%s. Versenként: [5. LXX-fordítói döntések](#5-lxx-fordítói-döntések).'
                % (szo_lista_irassal(tokenek_ny), osszes, szamlalo.get('egyező', 0),
                   ('; további %d versben ugyanannak a szócsaládnak egy másik tagja áll' % csal) if csal else '')]
    return ['**%s** · az LXX a motívum %d ószövetségi versében: %s *(egyező: a görög szövegben is %s áll)* — '
            'versenként: %s' % (', '.join(tokenek_ny), osszes, lxx_olvasoi_osszegzes(szamlalo),
                                ', '.join(tokenek_ny), LXX_SZAKASZ_LINK)]




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
    out = ['*Hivatkozás: %s.*' % SZEREP_HIVATKOZAS[(nyelv, n)]]
    _sorok, _sz, _f, heber_sz = _lxx_ctx(ctx)
    gorog = [x for x in motivum_strong_tokenek(ctx.get('sorai') or []) if x.startswith('G')]
    for t in tokenek_ny:
        hsz = heber_sz.get(t)
        if hsz and sum(hsz.values()) and uj_szerkezet(ctx.get('id')):
            # F182 (A13; F11, K61): szavanként egy teljes mondat, a hivatkozás link
            # a lektor és a Fable közös véleménye (1.): az újszövetségi pár nélküli szónál nincs következtetés
            out.append('%s Versenként: [5. LXX-fordítói döntések](#5-lxx-fordítói-döntések).' % OK.lxx_szo_uj(
                _szo_irassal_nevelovel(t), sum(hsz.values()), hsz.get('egyező', 0), hsz.get('szocsalad', 0),
                hsz.get('eltérő', 0), hsz.get('nincs_par', 0), hsz.get('LXX-minusz', 0),
                hsz.get('kutatói azonosítás függőben', 0), hsz.get('szamozas_elteres', 0),
                t in lxx_par_tokenek(motivum_strong_tokenek(ctx.get('sorai') or []))))
        elif hsz and sum(hsz.values()):
            # ELLENOR_ISTENTISZT_OLVASOI 2.: a számláló a motívum görög szavának egyezését méri a sor versében, nem a
            # héber szó saját görög megfelelőjét — a mondat ezt mondja ki
            out.append('**%s** · a motívum %d ószövetségi versében, ahol ez a szó áll, a görög szöveg a motívum görög '
                       'szavát (%s) %s — versenként: %s'
                       % (szo_cim(t), sum(hsz.values()), ', '.join(gorog) or EM_DASH,
                          'használja-e: ' + lxx_olvasoi_osszegzes(hsz), LXX_SZAKASZ_LINK))
        else:
            out.append('**%s** · a 3. szakaszban nincs sora — %s' % (szo_cim(t), LXX_SZAKASZ_LINK))
    out += ['*Versszintű együtt-előfordulás, nem szóillesztés (a token összes ÓSZ-i helye, a grammatikai '
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
            reszek_g.append('%s (%s%s): %d vers' % (lk[0], lk[1] + ', ' if lk[1] else '', g, db) if lk
                            else '%s: %d vers' % (g, db))
        out.append('**%s** · %d vers a Septuagintában (ebből %d vers görög tartalmi szóval); leggyakoribb görög '
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
    ('gorog', 6): _tartalom_gorog_lxx,
}


def _szerep_tartalom(nyelv, n, tokenek_ny, reszek, ctx):
    """A szerep kitöltött bekezdései: lista. Üres lista = a szerepnek nincs adata ezekhez a tokenekhez."""
    kulcs = (nyelv, n)
    if kulcs == ('gorog', 1) and uj_szerkezet(ctx.get('id')):
        # F182 (A10; F5, K52): a görög szavak alapjelentése a STEPBible rövid szótárából (TBESG), ugyanúgy, mint a
        # héber 4.1 (a magyar rövid jelentés a fordítási gyorsítótárból, `rovid_jelentes`); csak az új szerkezetű lapon
        # a felhasználó átnézése (4.): „**szó** — jelentés · Strong · [szónézet]”; a forrás egyszer, a bevezetőben
        out = []
        for t in tokenek_ny:
            rj, van = rovid_jelentes(t)
            out.append('**%s** — %s · %s · [szónézet](%s)' % (_szo_irassal(t), rj, t, SZONEZET_UT % t))
        ctx['tbesg_tbesh'].add('TBESG')
        return out
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
            if uj_szerkezet(ctx.get('id')):   # F182 (A12): a szó írással és kiejtéssel
                out.append('**%s** · %s' % (_szo_irassal(t), d[0]))
            else:
                out.append('**%s** · %s' % (t, d[0]))
            out.extend(d[1:])
    elif SZEREP_SAJAT.get(kulcs) == 'kiejtes':
        for t in tokenek_ny:
            lk = reszek[t]['lemma_kiejtes']
            if lk:
                out.append('**%s** · %s (%s)' % ((t,) + tuple(lk)))
    return out


# DT-F78d (lezárva): a TBESH (CC BY 4.0, DT-F33f) a héber 1. szerep forrása marad, `adatosítva`; a DT-F42a csak a
# H7121 „részlet” sorát váltotta ki BDB-vel. A TEREMT-002 két tokenének (H8414, H0922) DT187-mutatója az F12.2-ben
# kivezetve: a szótári bekötést a #12 elvégezte (F12.1).
# Tokenenkénti mutató az üres blokkon.
SZEREP_TOKEN_MUTATO = {
    ('heber', 1, 'H7121'): 'a H7121 alapjelentését a BDB 2.c adja (DT-F42a)',
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


def szerep_megjelenitett(szerep):
    """A szerep neve a renderben: a nem `aktiv` funkció-kapcsolók címrésze (pl. „ (+ SZPA)”) nélkül (ISTENTISZT-001 arany lap, 2026-10-29;
    `adat/funkcio_kapcsolok.tsv`)."""
    for r in SZK.funkcio_kapcsolok():
        if r['id'] == '*' and r.get('allapot') != 'aktiv' and r.get('szerep_cim_resz'):
            szerep = szerep.replace(r['szerep_cim_resz'], '')
    return szerep


def _motivum_tokenek(sorai):
    out = []
    for s in sorai:
        out += [t for t in (s.get('strong') or '').split('+') if t and t not in out]
    return out


def _sece_strongok(t):
    idx = lemma_strong_index()
    masik = 'H' if t.startswith('G') else 'G'
    ki = []
    for szo in sece_megfelelok(t) or []:
        for x in idx.get(unicodedata.normalize('NFC', szo), []):
            if x.startswith(masik) and x not in ki:
                ki.append(x)
    return ki


def _gorog_csalad(a, b):
    la, lb = lemma_kiejtes(a), lemma_kiejtes(b)
    if not la or not lb:
        return False
    return bool(_gorog_tovek(la[0]) & _gorog_tovek(lb[0])) or _strong_szarmazas(a) == b or _strong_szarmazas(b) == a


def _helyek_strongra(sorai, strong, usz):
    return [s['igehely'] for s in sorai if strong in (s.get('strong') or '').split('+')
            and (G.konyv_teszamentum(G.konyv_token(s['igehely'])) != 'ÓSZ') == usz]


def _jelentes_rovid(t):
    rj, van = rovid_jelentes(t)
    return ' ’%s’' % rj if van and rj else ''


def sece_hid_olvasoi(nyelv, tokenek_ny, sorai, tok):
    """A 4.7 olvasói mondatai (a felhasználó átnézése, 9.): a görög Biblia és a kétnyelvű szótár hídja a motívum héber és
    görög szavai között. Rövid mondatok: miért érdekes, aztán a lelet példával; a megfeleltetés a szócsaládra is néz
    (árar → kataraomai ~ epikataratosz, katara); ahol a szótár nem ad kapcsolatot, ezt mondja ki."""
    heber = nyelv == 'heber'
    sajat_masik = [x for x in tok if x.startswith('G' if heber else 'H')]
    if heber:
        ki = ['A görög Biblia a héber szavakat görög szavakkal adja vissza. Ha ez a görög szó ugyanaz, amely az '
              'Újszövetségben áll, a két rész szó szerint is összekapcsolódik.']
    else:
        ki = ['Az Újszövetség görög szavai a görög Bibliában héber szavakat fordítanak. Ha a héber szó a motívum saját '
              'szava, a két rész szó szerint is összekapcsolódik.']
    van = []
    csoport = {}                    # azonos lelet (ugyanazok a pontos megfelelők) -> a szavak
    for t in tokenek_ny:
        eq = _sece_strongok(t)
        pontos = tuple(x for x in eq if x in sajat_masik)
        if pontos:
            csoport.setdefault(pontos, []).append(t)
            van.append(t)
            continue
        if heber:
            csalad_e = [e for e in eq if any(_gorog_csalad(e, g) for g in sajat_masik)]
            if csalad_e:
                e = csalad_e[0]
                gs = [g for g in sajat_masik if _gorog_csalad(e, g)]
                helyek = list(dict.fromkeys(h for g in gs for h in _helyek_strongra(sorai, g, True)))
                ki.append('%s a szótár szerint görögül %s%s; ennek szócsaládjából %s áll az Újszövetségben (%s).' % (
                    _nagy_kezdo(_szo_irassal_nevelovel(t)), _szo_irassal(e), _jelentes_rovid(e),
                    OK._lista([_szo_irassal_nevelovel(g) + _jelentes_rovid(g) for g in gs]), ', '.join(helyek[:4])))
                van.append(t)
    for pontos, szavak in csoport.items():
        helyek = list(dict.fromkeys(h for x in pontos for h in _helyek_strongra(sorai, x, heber)))
        alany = _nagy_kezdo(OK._lista([_szo_irassal_nevelovel(t) for t in szavak]))
        if heber:
            ki.append('%s ilyen: a kétnyelvű szótár szerint görögül %s, és az Újszövetség is %s beszél (%s).' % (
                alany, OK._lista([_szo_irassal(x) for x in pontos]),
                'ezekkel a szavakkal' if len(pontos) > 1 else 'ezzel a szóval', ', '.join(helyek[:4])))
        else:
            ki.append('%s ilyen: a kétnyelvű szótár szerint héberül %s felel meg %s, és a motívum ószövetségi helyein ez '
                      'a szó áll (%s).' % (alany, OK._lista([_szo_irassal_nevelovel(x) for x in pontos]),
                                           'nekik' if len(szavak) > 1 else 'neki',
                                           ', '.join(helyek[:4]) + (', …' if len(helyek) > 4 else '')))
    if len(van) < len(tokenek_ny):
        ki.append('A többi szónál a szótár nem ad ilyen kapcsolatot.' if van else
                  'A motívum szavainál a szótár nem ad ilyen kapcsolatot.')
    return ' '.join(ki)


def sece_sajat(t, sajat):
    """(a SECE-megfelelők száma, [a motívum saját Strongjai köztük]) — a sece_tabla egyezés-szabályával."""
    lista = sece_megfelelok(t) or []
    masik = 'H' if t.startswith('G') else 'G'
    idx = lemma_strong_index()
    talalt = []
    for szo in lista:
        for x in idx.get(unicodedata.normalize('NFC', szo), []):
            if x.startswith(masik) and x in sajat and x not in talalt:
                talalt.append(x)
    return len(lista), talalt


def szerep_olvasoi(nyelv, n, tokenek_ny, ctx):
    """A 6., 7. és 9. szerep olvasói szövege (lelet + következtetés), vagy None."""
    sorai = ctx['sorai']
    tok = _motivum_tokenek(sorai)
    uj = uj_szerkezet(ctx.get('id'))
    if n == 6:
        return lxx_olvasoi(lxx_osszevetes(sorai, tok)[1], tok, uj=uj)
    if n == 7 and uj:
        # a felhasználó átnézése (9.): olvasói mondatok a 9. tétel mintájára (miért érdekes → lelet példával); a
        # megfeleltetés a szócsaládra is néz (árar → kataraomai ~ katara); ahol a szótár nem ad kapcsolatot, ezt mondja
        return sece_hid_olvasoi(nyelv, tokenek_ny, sorai, tok)
    if n == 7 and uj:
        return OK.sece_csoport('héber' if nyelv == 'heber' else 'görög',
                               [(_szo_irassal_nevelovel(t), db, [_szo_irassal(x) for x in sj])
                                for t, (db, sj) in ((t, sece_sajat(t, set(tok))) for t in tokenek_ny)])
    if n == 9 and uj:
        # F182 (A16; F7): egy csoportosított mondat, a kivételek igehellyel
        tesz = 'ószövetségi' if nyelv == 'heber' else 'újszövetségi'
        szavak = []
        for t in tokenek_ny:
            nn, h, j, helyek = _ubs_oszlop_szamlalo(t, ctx, helyekkel=True)
            szavak.append((_szo_irassal_nevelovel(t), nn, h, helyek))
        hely_szam = len({s['igehely'] for s in sorai if any(x in tokenek_ny for x in (s.get('strong') or '').split('+'))
                         and (G.konyv_teszamentum(G.konyv_token(s['igehely'])) == 'ÓSZ') == (nyelv == 'heber')})
        return OK.versenkenti_csoport('héber' if nyelv == 'heber' else 'görög', tesz, szavak, hely_szam)
    if n == 7:
        adat = {t: sece_sajat(t, set(tok)) for t in tokenek_ny}
        # F12 (TEREMT-002): a motívumnak nincs szava a másik nyelven -> a SECE-megfelelők közül az LXX-döntések szavai
        masik = 'G' if nyelv == 'heber' else 'H'
        nincs_masik = not any(x.startswith(masik) for x in tok)
        lxx_strongok = set()
        if nincs_masik:
            igehelyek = {v for s in sorai for v in igehely_lista(s['igehely'])}
            lxx_strongok = {(r.get('gorog_strong') or '').strip()
                            for v in igehelyek for r in lxx_dontesek_index().get(v, [])}
        reszek = [OK.sece(_szo_nev(t), db, [_szo_nev(x) for x in sj],
                          tars=next((_szo_nev(u) for u in tokenek_ny if u != t and adat[u][1]), ''),
                          nincs_masik=nincs_masik,
                          lxx_nevek=[_szo_nev(x) for x in sece_sajat(t, lxx_strongok)[1]] if nincs_masik else ())
                  for t, (db, sj) in adat.items()]
        return ' '.join(r for r in reszek if r) or None
    if n == 9:
        tesz = 'ószövetségi' if nyelv == 'heber' else 'újszövetségi'
        return OK.versenkenti([(_szo_nev(t),) + tuple(_ubs_oszlop_szamlalo(t, ctx)[:2]) + (tesz,)
                               for t in tokenek_ny])
    return None


def _szerep_blokk(nyelv, sor, tokenek_ny, reszek, ctx):
    n = int(sor['sorrend'])
    szerep, allapot = szerep_megjelenitett(sor['szerep']), sor['allapot']
    szakasz = ['#### %d. %s' % (n, szerep)]
    olv = olvasoi_szerep(nyelv, n, bool(ctx.get('gerinc')) and (nyelv, n) in GERINC_SZEREP_EPITO)
    if n == 12 and ctx.get('gerinc'):
        olv = SZN.olvasoi_12(ctx.get('sorai') or [], motivum_mezo(ctx, 'folerendelt_fogalom').split(' (')[0]) or olv
    if n in (6, 7, 9) and ctx.get('sorai'):
        olv = szerep_olvasoi(nyelv, n, tokenek_ny, ctx) or olv
    if n in (13, 14) and ctx.get('sorai') and ctx['sorai'][0].get('id') in SZEREP_KAROLI_MOTIVUMOK:
        if uj_szerkezet(ctx['sorai'][0].get('id')):   # F182 (A24): a több szóval hordozott motívum mérése szavanként
            olv = (olvasoi_13_szavankent if n == 13 else olvasoi_14_szavankent)(ctx['sorai']) or olv
        else:
            olv = (olvasoi_13 if n == 13 else olvasoi_14)(ctx['sorai']) or olv
    if uj_szerkezet(ctx.get('id')) and (nyelv, n) in UJ_OLVASOI_SZEREP:
        olv = UJ_OLVASOI_SZEREP[(nyelv, n)]
    if olv:
        szakasz.append(olvasoi_bekezdes(olv))
    ctx['szerep'] = szerep
    tart = _szerep_tartalom(nyelv, n, tokenek_ny, reszek, ctx)
    if allapot == 'adatosítva':
        if tart:
            szakasz.extend(tart)
        elif (nyelv, n) in SZEREP_HIVATKOZAS and (nyelv, n) not in SZEREP_SAJAT:
            hiv = _hivatkozas_szoveg(nyelv, n, ctx)
            szakasz.append('*Hivatkozás: %s%s*' % (hiv, '' if hiv.endswith('.') else '.'))
        elif _token_ures_blokkok(nyelv, n, szerep, tokenek_ny):
            szakasz.extend(_token_ures_blokkok(nyelv, n, szerep, tokenek_ny))
        else:
            # DT-F78c 1.: harmadik állapot, mutatóval a #9-re (a bekötés a #9 dolga)
            szakasz.append(ures_blokk(szerep, 'adatosítva, nincs bekötve',
                                      'a szerep adatosítva (a forrásfájl megvan), de a motívum tokenjeihez a '
                                      '`lexikon_hivatkozasok.tsv`-be nincs bekötve sor; a bekötés még nem történt meg'))
    elif tart and ctx.get('gerinc') and (nyelv, n) in GERINC_TELJES:
        szakasz.extend(tart)
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
           'gerinc': gerinc_aktiv(motivum_id), 'bdb_kartya': bdb_kartya_aktiv(motivum_id), 'id': motivum_id}
    reszek_szoveg = []
    for nyelv, cim in (('gorog', 'Görög'), ('heber', 'Héber')):
        tok_ny = [t for t in tokenek if t.startswith('G' if nyelv == 'gorog' else 'H')]
        if not tok_ny:
            reszek_szoveg.append('### %s szavak\n\n<!-- ÜRES-NYELV: %s | nincs Strong-token -->\n%s\n\n'
                                 '*A motívumnak nincs %s Strong-tokenje; a %s szerepek nem alkalmazhatók.*'
                                 % (cim, nyelv, olvasoi_bekezdes(OLVASOI_SABLON['nyelv_ures'] % {'nyelv': cim.lower()}),
                                    cim.lower(), cim.lower()))
            continue
        nyelv_olv = (OLVASOI_SABLON['nyelv_uj'] % {'nyelv': cim.lower(), 'szavak': szo_lista_irassal(tok_ny),
                                                   'utolso': max(int(x['sorrend']) for x in (g_sorok if nyelv == 'gorog'
                                                                                             else h_sorok)
                                                                 if int(x['sorrend']) <= 10)}
                     if uj_szerkezet(motivum_id) else
                     OLVASOI_SABLON['nyelv'] % {'nyelv': cim.lower(), 'szavak': szo_felsorolas(tok_ny)})
        blokkok = ['### %s szavak: %s' % (cim, ', '.join(tok_ny)), olvasoi_bekezdes(nyelv_olv)]
        # a szótári gerinc a 2. szerep („Mélységi szócikk”) tartalma (ISTENTISZT-001 arany lap, 2026-10-29: a DT371 1.
        # helye módosítva; l. GERINC_SZEREP_EPITO ('gorog'/'heber', 2))
        for s in (g_sorok if nyelv == 'gorog' else h_sorok):
            if int(s['sorrend']) in kozos:
                continue
            blokkok.append(_szerep_blokk(nyelv, s, tok_ny, reszek, ctx))
        reszek_szoveg.append('\n\n'.join(blokkok))
    if kozos:
        blokkok = ['### Nyelvfüggetlen szerepek', olvasoi_bekezdes(OLVASOI_SABLON['nyelvfuggetlen'])]
        for s in g_sorok:
            if int(s['sorrend']) in kozos:
                blokkok.append(_szerep_blokk('gorog', s, [], reszek, ctx))
        reszek_szoveg.append('\n\n'.join(blokkok))
    return '\n\n'.join(reszek_szoveg), van_hiv, tiszt


KULCSSZAVAK_CIM = '### A motívum kulcsszavai'


def kulcsszavak_blokk(motivum_id, sorai, fajl_licenc_kulcsok):
    """A 2. szakasz eleje (ISTENTISZT-001 arany lap, 2026-10-29; a felhasználó: „2. Szótári háttér előtt kellene egy
    motivum kulcsszavai blokk”): gerinc-kombinációnként a szavak kiejtéssel, a rövid jelentésük (1. szerep) és a
    Károli-kulcsszavak (a 14. szerep szabálya, `szerep_karoli.kulcsszavak`). Csak a `KAROLI_MEGFELELOK` kapcsolóval
    (a Károli-kulcsszó a `karoli_szo` mezőn áll); egyébként ''. Csak megjelenítés, új adat nincs."""
    if motivum_id not in SZEREP_KAROLI_MOTIVUMOK or uj_szerkezet(motivum_id):
        # F182 (A24): az új szerkezetű lapon a kulcsszó szavanként a 4.13–4.14-ben áll; a formula-motívumra szabott
        # „A motívum kulcsszavai” blokk (egy szókapcsolat) a több szóval hordozott motívumra nem mond igazat
        return ''
    kombok = SZK.gerinc_kombinaciok(sorai)
    if not kombok:
        return ''
    kulcs = SZK.kulcsszavak(sorai)
    # F152 A.3: a „gerinc” üzemeltetői szó, az olvasói oszlopfejben nem áll
    sorok = ['| Héber/görög szavak | Szavak (kiejtéssel) | Jelentés | Károli-kulcsszavak |', '|---|---|---|---|']
    for k in kombok:
        st = sorted(k, key=lambda s: (s[0] != 'G', s))
        szavak = ' + '.join(lemma_cim(lemma_kiejtes(s)) if lemma_kiejtes(s) else s for s in st)
        jelentes = ' + '.join(rovid_jelentes(s)[0] for s in st)
        karoli = ', '.join('„%s”' % w for w in kulcs.get(k, [])) or EM_DASH
        sorok.append('| %s | %s | %s | %s |' % (' + '.join(st), szavak, jelentes, karoli))
    fajl_licenc_kulcsok.setdefault('adat/elofordulasok.tsv', set()).add('projekt_adat')
    fajl_licenc_kulcsok.setdefault('adat/szoto/karoli_szotari_alak.tsv', set()).add('projekt_adat')
    olv = OK.kulcsszavak([('héber' if sorted(k)[0].startswith('H') else 'görög', [_szo_nev(s) for s in sorted(k)],
                           sum(1 for r in sorai if SZK._komb(r) == k)) for k in kombok]) or \
        ('A motívumot hordozó héber és görög szavak, a jelentésük, és azok a magyar szavak, amelyekkel a '
         'Károli-fordítás a motívum helyein a legtöbbször visszaadja őket.')
    hatokor = ('*Gerinc-kombinációnként (az `elofordulasok.tsv` `strong` mezője, %d sor); a jelentés az 1. szerep '
               'rövid jelentése; a Károli-kulcsszó a 14. szerep szabálya szerint (`eszkozok/szerep_karoli.py`: a '
               'motívumsorok Károli-szóalakjainak legalább felében álló szótári alak). Csak megjelenítés.*'
               % sum(1 for s in sorai if s.get('strong')))
    return '\n\n'.join([KULCSSZAVAK_CIM, olvasoi_bekezdes(olv), hatokor, '\n'.join(sorok)])


def blokk_szocikkek(m, tokenek, sorai):
    reszek = []
    fajl_licenc_kulcsok = {'adat/lexikon_hivatkozasok.tsv': set()}
    kulcs_szov = kulcsszavak_blokk(m['id'], sorai or [], fajl_licenc_kulcsok)
    if kulcs_szov:
        reszek.append(kulcs_szov)
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
        rokon_reszek = ['### Rokon szavak',
                        olvasoi_bekezdes(OLVASOI_SABLON['rokon'] % {'szavak': szo_felsorolas(rokon_strongok)})]
        for strong in rokon_strongok:
            alszakasz_szov, van_hiv, tiszt = _epit_szotar_alszakasz(
                strong, 1, fajl_licenc_kulcsok, fajl_licenc_kulcsok_tbesg_tbesh)
            van_hivatkozas_barmelyikhez = van_hivatkozas_barmelyikhez or van_hiv
            tisztazatlan_erintve = tisztazatlan_erintve or tiszt
            rokon_reszek.append(alszakasz_szov)
            # ISTENTISZT-001 arany lap, 2026-10-29: a rokon szó SECE-megfelelői a 7. szerep formájában (a 2/b. SECE-blokkjai helyett)
            tabla = sece_tabla(strong, set(tokenek))
            if tabla:
                rokon_reszek.append('##### %s · SECE — %s megfelelők (%d)\n\n%s\n\n%s\n\n%s' % (
                    szo_cim(strong), 'héber' if strong.startswith('G') else 'görög', tabla[0],
                    olvasoi_bekezdes(OLVASOI_SZEREP[7]), tabla[1], SECE_LABJEGYZET))
                for b in ('G', 'H'):
                    fajl_licenc_kulcsok.setdefault(SECE_FAJL[b], set()).add(SECE_LICENC_KULCS[b])
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
    fo = ', '.join('%s a %s' % (ny, SZEREP_SZOTAR[(k, 2)]) for ny, k in (('héberül', 'heber'), ('görögül', 'gorog'))
                     if any(t.startswith('H' if k == 'heber' else 'G') for t in tokenek))
    olv = olvasoi('szocikkek', szavak=szo_felsorolas(tokenek), fo=fo or EM_DASH,
                  gerinc=OLVASOI_SABLON['szocikkek_gerinc'] if gerinc_aktiv(m['id']) else '')
    if uj_szerkezet(m['id']):
        # F182 (A09; F8): a szavak írással és zárójeles kiejtéssel, Strong-szám nélkül; a pontrendszer a Jelmagyarázatban
        h = [t for t in tokenek if t.startswith('H')]
        g = [t for t in tokenek if t.startswith('G')]
        reszek = ['%s: %s' % (ny, szo_lista_irassal(ts)) for ny, ts in (('héberül', h), ('görögül', g)) if ts]
        olv = ('A motívumot %s hordozza; %s. Szavanként számozott pontok követik egymást (a pontok rendje a '
               'Jelmagyarázatban áll); a 4.2 pont a fő szótár (%s) szócikke.%s'
               % (' és '.join('%d %s szó' % (len(ts), ny) for ny, ts in (('héber', h), ('görög', g)) if ts),
                  '; '.join(reszek), fo or EM_DASH,
                  OLVASOI_SABLON['szocikkek_gerinc'] if gerinc_aktiv(m['id']) else ''))
    blokk_szoveg = _lexikon_blokk(m['id'], 'szocikkek', forras_lista, licenc_lista, hatokor, torzs, olv)
    return blokk_szoveg, tisztazatlan_erintve, forras_licenc_parok


# A 13. és a 14. szerep olvasói mondata az adatból, példával (a felhasználó, 2026-10-29: „ez érthetőbbé kell tenni”;
# „a gerinc szavai is elvont”): a motívum saját szavai kiejtéssel, a Károli szavai, egy-egy példa a lap adatából.

def _szo_nev(strong):
    """A szó neve a prózában: a kiejtés (héberül a jóváhagyott), ennek híján a lemma, névelővel: „a kárá”."""
    lk = lemma_kiejtes(strong)
    nev = (lk[1] or lk[0]) if lk else strong
    return '%s %s' % (_nevelo(nev), nev)


def _szo_kiejtessel(strong):
    """„kárá (H7121)” — a kiejtés (héberül a jóváhagyott), ennek híján a lemma, a Strong-számmal (F152 A.3)."""
    lk = lemma_kiejtes(strong)
    nev = (lk[1] or lk[0]) if lk else ''
    return '%s (%s)' % (nev, strong) if nev else strong


def _es_lista(xs):
    return xs[0] if len(xs) == 1 else '%s és %s' % (', '.join(xs[:-1]), xs[-1])


def motivum_szavai_proza(sorai, nyelvvel=True):
    """`nyelvvel`: „a héber szövegben a kárá és a sém, a görögben az epikaleó”; különben „a kárá és a sém, illetve az
    epikaleó” — a motívumsorok Strong-tokenjei nyelvenként."""
    st = []
    for k in SZK.gerinc_kombinaciok(sorai):
        st += [s for s in sorted(k) if s not in st]
    reszek = []
    for ny, betu in (('a héber szövegben', 'H'), ('a görögben', 'G')):
        xs = [_szo_nev(s) for s in st if s.startswith(betu)]
        if xs:
            reszek.append('%s %s' % (ny, _es_lista(xs)) if nyelvvel else _es_lista(xs))
    return ', '.join(reszek) if nyelvvel else ', illetve '.join(reszek)


def _idezet(xs):
    return _es_lista(['„%s”' % x for x in xs])


# A 13. szerep következtetése a leggyakoribb Károli-szó arányából (a felhasználó, 2026-10-30: „mindig vanjuk le a
# következtetést a találtakból . a magyarázó szöveg az adatokból induljon.”): (alsó küszöb, következtetés).
OLVASOI_13_KUSZOB = (
    (0.90, 'a Károli a motívumot szinte mindenütt (a helyek %d%%-án) ugyanazzal a szóval adja vissza, ezért magyarul '
           'olvasva is jól követhető'),
    (0.67, 'a Károli a motívumot a legtöbb helyen (%d%%) ugyanazzal a szóval adja vissza'),
    (0.50, 'a Károli a motívumot a helyek felén-kétharmadán (%d%%) adja vissza ugyanazzal a szóval'),
    (0.0, 'a Károli a motívumot változó szavakkal adja vissza (a leggyakoribb szó is csak a helyek %d%%-án áll), ezért '
          'magyarul olvasva nehezen követhető'),
)


def olvasoi_13(sorai):
    """A 13. szerep olvasói szövege: a lelet számokkal, utána a szabály szerinti következtetés; None, ha nincs Károli-szó."""
    tetel = SZK.karoli_megfelelok(sorai)
    n = sum(1 for s in sorai if s.get('karoli_szo'))
    if not tetel or not n:
        return None
    gyak = ', '.join('„%s” %d' % (l, len(h)) for l, _a, h in tetel[:3])
    arany = len(tetel[0][2]) / n
    kov = next(t for k, t in OLVASOI_13_KUSZOB if arany >= k) % round(100 * arany)
    hianyzo = [s['igehely'] for s in sorai if s.get('karoli_szo') and s['igehely'] not in tetel[0][2]]
    helyette = ''
    if hianyzo:
        hely = SZK.helyettesitok(sorai, hianyzo, [tetel[0][0]], strongok=SZK.strongjai(sorai, tetel[0][0]))
        if hely:
            helyette = (' Ahol nem a „%s” áll (%d helyen), ott a Károli jellemzően ezt írja helyette: %s.'
                        % (tetel[0][0], len(hianyzo), ', '.join('„%s” %d' % (l, len(h)) for l, h in hely[:3])))
    return ('A motívum %d igehelyén a Károli %d különböző magyar szót használ. A leggyakoribbak (igehelyek száma): %s.%s '
            '**Következtetés:** %s. A sorokban a ragozott alakok és az igehelyek állnak.'
            % (n, len(tetel), gyak, helyette, kov))


# --- F182 (A24; F14, K69): a 4.13 és a 4.14 a több szóval hordozott (strukturális) motívumon -------------------------
# A HAMART-001 lánca tíz héber és öt görög szón áll; a motívum egészére számolt „leggyakoribb magyar szó” (olvasoi_13) és a
# „minden helyen ugyanaz a kulcsszó” feltevés (olvasoi_14) itt nem mond igazat. A szöveg ezért szavanként mér: a szó
# helyein a Károli leggyakoribb szava és aránya; kulcsszó csak ott, ahol a 14. szerep szabálya (`szerep_karoli.
# kulcsszavak`) ad ilyet, és a rejtett / hamis párhuzam csak ezekre a szavakra állítható. Kis elemszámnál (KAROLI_MIN_HELY
# alatt) a szóról nincs következtetés (K10).
KAROLI_MIN_HELY = 3
KAROLI_ALLANDO = 0.67


def _szo_irassal(strong):
    lk = lemma_kiejtes_szabaly(strong)
    if not lk:
        return strong
    return '%s (%s)' % (lk[0], lk[1]) if lk[1] else lk[0]


def _kombo_nev(k):
    return ' + '.join(_szo_irassal(t) for t in sorted(k))


def _kombo_nevelovel(k):
    """„az אֲדָמָה (adámá)” — a névelő a kiejtés szerint."""
    lk = lemma_kiejtes_szabaly(sorted(k)[0])
    return '%s %s' % (_nevelo((lk[1] or lk[0]) if lk else 'a'), _kombo_nev(k))


def _idezett_nevelovel(w):
    return '%s „%s”' % (_nevelo(w), w)


def _szocsalad(tetel):
    """[(szótári alak, [igehely])] a karoli_megfelelok tételeiből, a ragozott maradék a rövidebb alakba olvasztva (a
    szabály egy helyen: `szerep_karoli.szocsalad`; a 4.13 listája is ezt használja)."""
    return [(l, h) for l, _a, h in SZK.szocsalad(tetel)]


def karoli_szavankent(sorai):
    """[(kombináció, helyek száma, [(szótári alak, [igehely])])] — a motívum szavanként (a sorok Strong-kombinációja), a
    Károli-szavak szócsaládonként, gyakoriság szerint."""
    ki = []
    for k in SZK.gerinc_kombinaciok(sorai):
        csop = [s for s in sorai if SZK._komb(s) == k and SZK.szavak(s.get('karoli_szo'))]
        if csop:
            ki.append((k, len(csop), _szocsalad(SZK.karoli_megfelelok(csop))))
    return sorted(ki, key=lambda x: (-x[1], sorted(x[0])))


def olvasoi_13_szavankent(sorai):
    tetel = SZK.karoli_megfelelok(sorai)
    n = sum(1 for s in sorai if s.get('karoli_szo'))
    if not tetel or not n:
        return None
    szavak = karoli_szavankent(sorai)
    merheto = [(k, db, cs) for k, db, cs in szavak if db >= KAROLI_MIN_HELY]
    reszek = ['%s %d helyéből %d helyen „%s”' % (_kombo_nevelovel(k), db, len(cs[0][1]), cs[0][0])
              for k, db, cs in merheto]
    # F182 javítókör (ELLENOR_F182 #9): a szám a 4.13 listájáéval egy alapon, szócsaládonként
    lelet = ('A motívum %d igehelyén a Károli %d különböző magyar szót használ (szócsaládonként). A motívumot több héber '
             'és görög szó hordozza, ezért a magyar szavakat szavanként érdemes nézni' % (n, len(SZK.szocsalad(tetel))))
    lelet += (': a legalább %d helyen álló szavaknál a leggyakoribb magyar szó %s.' % (KAROLI_MIN_HELY, '; '.join(reszek))
              if reszek else '; egyik szó sem áll %d helynél többen.' % (KAROLI_MIN_HELY - 1))
    kevés = len(szavak) - len(merheto)
    if kevés:
        lelet += ' A többi %d szó %d helynél kevesebben áll, ezekről nincs következtetés.' % (kevés, KAROLI_MIN_HELY)
    if not merheto:
        return lelet + ' A sorokban a ragozott alakok és az igehelyek állnak.'
    allando = [_kombo_nevelovel(k) for k, db, cs in merheto if len(cs[0][1]) / db >= KAROLI_ALLANDO]
    valtozo = [_kombo_nevelovel(k) for k, db, cs in merheto if len(cs[0][1]) / db < KAROLI_ALLANDO]
    kov = []
    if allando:
        kov.append('%s helyein a Károli többnyire ugyanazzal a magyar szóval fordít, ezért %s magyarul is %s'
                   % (_es_lista(allando), 'ezek a szavak' if len(allando) > 1 else 'ez a szó',
                      'követhetők' if len(allando) > 1 else 'követhető'))
    if valtozo:
        kov.append('%s helyein váltakozó szavakkal, ezért %s magyarul nehezen %s'
                   % (_es_lista(valtozo), 'ezek' if len(valtozo) > 1 else 'ez',
                      'követhetők' if len(valtozo) > 1 else 'követhető'))
    kov = '; '.join(kov)
    return '%s **Következtetés:** %s. A sorokban a ragozott alakok és az igehelyek állnak.' % (lelet, kov)


def olvasoi_14_szavankent(sorai):
    kulcs = collections.OrderedDict((k, v) for k, v in SZK.kulcsszavak(sorai).items() if v)
    if not kulcs:
        return ('A rejtett és a hamis párhuzam a Károli állandó magyar kulcsszavával mérhető (a szó helyeinek legalább '
                'felében ugyanaz a magyar szó). A motívum egyik szavának sincs ilyen kulcsszava, ezért egyik sem '
                'állapítható meg; a vizsgálat eredménye üres.')
    nevek = ['%s: „%s”' % (_kombo_nevelovel(k), '”, „'.join(v)) for k, v in kulcs.items()]
    osszes = len(SZK.gerinc_kombinaciok(sorai))
    szoveg = ('A rejtett és a hamis párhuzam a Károli állandó magyar kulcsszavával mérhető: azzal a magyar szóval, '
              'amely a szó motívumhelyeinek legalább felében ugyanabban a szótári alakban áll (legalább %d helyen álló '
              'szónál). Ilyen kulcsszava a motívum %d szava közül %d-nak van: %s. A többi szónál nincs ilyen szótári alak '
              '(vagy a szó %d helynél kevesebben áll), ezért azoknál a rejtett és a hamis párhuzam ezzel a módszerrel nem '
              'mérhető; a magyar szavaik a 4.13-ban állnak.'
              % (SZK.KULCS_MIN_SOR, osszes, len(kulcs), _es_lista(nevek), SZK.KULCS_MIN_SOR))
    rejt = SZK.rejtett_parhuzamok(sorai, kulcs=kulcs)
    hamis = SZK.hamis_parhuzamok(sorai, kulcs=kulcs)
    if rejt:
        szoveg += (' **Rejtett párhuzam** (a motívum szava áll, de a Károli nem a kulcsszóval fordítja): %d hely, %s.'
                   % (len(rejt), ', '.join('%s — „%s”' % (h, k) for h, k, _s, _hi in rejt[:3])))
    else:
        szoveg += ' **Rejtett párhuzam** nincs: ezeknek a szavaknak minden helyén a kulcsszó áll.'
    if hamis:
        mogott = SZK.hamis_strongjai(hamis, kulcs)
        mog = []
        for kw, lista in mogott.items():
            fo = [(st, db) for st, db in lista if not any(st in k for k in kulcs)][:1]
            if fo:
                mog.append('%s mögött leggyakrabban %s (%d versben)'
                           % (_idezett_nevelovel(kw), _kombo_nevelovel({fo[0][0]}), fo[0][1]))
        szoveg += (' **Hamis párhuzam** (a magyar kulcsszó áll, de az eredetiben nem a motívum szava): %d vers, %s.'
                   % (len(hamis), '; '.join(mog) if mog else 'a párosítás a versek mögötti szót nem adja meg'))
    else:
        szoveg += ' **Hamis párhuzam** nincs.'
    if not rejt and not hamis:
        return szoveg + ' **Következtetés:** ezeknél a szavaknál a magyar kulcsszó megbízhatóan jelzi a motívumot.'
    talalat = sum(1 for s in sorai if SZK._komb(s) in kulcs) - len(rejt) + len(hamis)
    kw = [w for v in kulcs.values() for w in v]
    kw_lista = ' vagy '.join([_idezett_nevelovel(w) for w in kw])
    return szoveg + (' **Következtetés:** aki a Károliban %s szóra keres, a %d találat %d%%-a nem a motívumhoz '
                     'tartozik%s; a motívum ezért ezeknél a szavaknál is az eredeti szavak alapján kereshető, nem a magyar '
                     'fordítás alapján.' % (kw_lista, talalat, round(100 * len(hamis) / talalat) if talalat else 0,
                                            ', és a motívum %d helyét nem találja meg' % len(rejt) if rejt else ''))


def _tagmondat(vers, szavak):
    """A vers kulcsszavakat leginkább tartalmazó tagmondata (vessző, pontosvessző, kettőspont, pont mentén)."""
    reszek = [r.strip() for r in re.split(r'[,;:.]', vers) if r.strip()]
    return max(reszek, key=lambda r: sum(1 for w in szavak if w in r.lower())) if reszek else vers


def olvasoi_14(sorai):
    """A 14. szerep olvasói szövege: a rejtett és a hamis párhuzam száma példával, utána a következtetés (a magyar
    szókeresés hiánya és téves aránya: hamis / (a kulcsszavas motívumhelyek + hamis)); None, ha nincs kulcsszó."""
    kulcs = {k: v for k, v in SZK.kulcsszavak(sorai).items() if v}
    if not kulcs:
        return None
    n = len(sorai)
    rejt = SZK.rejtett_parhuzamok(sorai, kulcs=kulcs)
    hely_szavak = []
    hamis = SZK.hamis_parhuzamok(sorai, kulcs=kulcs)
    minden = []
    for v in kulcs.values():
        minden += [w for w in v if w not in minden]
    szavak = motivum_szavai_proza(sorai).replace('a héber szövegben', 'héberül').replace('a görögben', 'görögül')
    if rejt:
        h, k, _s, _hi = rejt[0]
        szoveg = ('A motívum %d helye közül %d helyen a héber vagy görög szövegben megvan a motívum szava (%s), de a '
                  'Károli más magyar szóval fordítja, például: %s — „%s”. Ez a **rejtett párhuzam**.'
                  % (n, len(rejt), szavak, h, k))
        hely = SZK.helyettesitok(sorai, [r[0] for r in rejt], [], kulcs)
        if hely:
            szoveg += (' Ezeken a helyeken a Károli a motívum magyar kulcsszavai helyett jellemzően ezt írja: %s.'
                       % ', '.join('„%s” (%d hely)' % (l, len(hh)) for l, hh in hely[:3]))
        hely_szavak = [l for l, _hh in hely[:3]]
    else:
        szoveg = ('A motívum mind a %d helyén, ahol a héber vagy görög szövegben a motívum szava áll (%s), a Károli is a '
                  'szokásos magyar szavakat használja: **rejtett párhuzam** nincs.' % (n, szavak))
    if hamis:
        h, vers, _g = hamis[0]
        szoveg += (' Ugyanakkor %d olyan vers van, amelyben magyarul ugyanazok a szavak állnak (%s), de az eredetiben nem '
                   'a motívum szavai, például: %s — „%s”. Ez a **hamis párhuzam**.'
                   % (len(hamis), _idezet(minden), h, _tagmondat(vers, minden)))
    else:
        szoveg += ' Olyan vers, amelyben magyarul ugyanezek a szavak állnak, de az eredetiben nem, nincs: **hamis párhuzam** nincs.'
    if not rejt and not hamis:
        return szoveg + ' **Következtetés:** a magyar szavak megbízhatóan jelzik a motívumot.'
    reszek = []
    if rejt:
        reszek.append('a motívum %d helyét nem találja meg%s' % (
            len(rejt), ', hacsak nem keres ezekre is: %s' % ', '.join('„%s”' % w for w in hely_szavak)
            if hely_szavak else ''))
    if hamis:
        # a magyar szókeresés találatai: a kulcsszavas kombinációjú motívumhelyek, ahol a kulcsszó áll, és a hamis versek
        talalat = sum(1 for s in sorai if SZK._komb(s) in kulcs) - len(rejt) + len(hamis)
        reszek.append('a %d találat %d%%-a nem a motívumhoz tartozik' % (talalat, round(100 * len(hamis) / talalat)))
    return szoveg + (' **Következtetés:** aki a Károliban ezekre a magyar szavakra keres, %s. A motívumot ezért az '
                     'eredeti szavak alapján kell keresni, nem a magyar fordítás alapján.' % ', és '.join(reszek))


def _szo_irassal_nevelovel(strong):
    """„az אָבַל (ával)” — írás, zárójeles kiejtés, a névelő a kiejtés szerint (F182)."""
    lk = lemma_kiejtes_szabaly(strong)
    if not lk:
        return strong
    return '%s %s' % (_nevelo(lk[1] or lk[0]), '%s (%s)' % (lk[0], lk[1]) if lk[1] else lk[0])


def konyv_teljes_nev(rov):
    """A könyv teljes magyar neve a normalizáló táblából („1Móz” → „Mózes első könyve”); ismeretlennél a rövidítés."""
    global _konyv_nev_cache
    if _konyv_nev_cache is None:
        _konyv_nev_cache = {}
        with io.open(os.path.join(KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8') as f:
            for i, sor in enumerate(f):
                r = sor.rstrip('\r\n').split('\t')
                if i and len(r) > 2:
                    _konyv_nev_cache[r[1]] = r[2]
    return _konyv_nev_cache.get(rov, rov)


_konyv_nev_cache = None


def szo_lista_irassal(tokenek):
    """F182 (A09; F8): „אָבַל (ával), אֲדָמָה (adámá) és שָׁחַת (sáchat)” — írás és zárójeles kiejtés, Strong-szám nélkül
    (a kiejtés a kiejtés-szabály szerint; jóváhagyott héber alak nélkül csak az írás)."""
    xs = []
    for t in tokenek:
        lk = lemma_kiejtes_szabaly(t)
        xs.append(('%s (%s)' % (lk[0], lk[1]) if lk[1] else lk[0]) if lk else t)
    return _es_lista(xs) if xs else EM_DASH


def szo_felsorolas(tokenek):
    """„héberül a kárá (H7121) és a sém (H8034), görögül az epikaleó (G1941)” — a kiejtés a TBESG/TBESH-ből (héberül
    a jóváhagyott kiejtés, ha van, különben a STEP-átírás)."""
    def szo(t):
        lk = tbesg_tbesh_index()[0].get(t) or tbesg_tbesh_index()[1].get(t)
        if not lk:
            return t
        k = lemma_kiejtes(t)[1]
        if not k:
            return '%s %s (%s)' % (SZKZ.nevelo(lk[0]), lk[0], t)
        return '%s %s (%s)' % (SZKZ.nevelo(k), k, t)

    def lista(xs):
        return xs[0] if len(xs) == 1 else '%s és %s' % (', '.join(xs[:-1]), xs[-1])
    reszek = []
    for ny, betu in (('héberül', 'H'), ('görögül', 'G')):
        xs = [szo(t) for t in tokenek if t.startswith(betu)]
        if xs:
            reszek.append('%s %s' % (ny, lista(xs)))
    return ', '.join(reszek) or EM_DASH


# ---------------------------------------------------------------------------
# F131: a motívumlap szótári gerince (DT272 = DT338; DT371–e, SEMA 2.40)
# ---------------------------------------------------------------------------
# Kapcsoló: az új szótári blokk, a szerepmátrix szűkítése és az előfordulás-tábla
# két oszlopa ("Jelentés (a szó)", "Funkció (a motívumban)") csak ezeken a lapokon él;
# a többi lap bájtra változatlan (DT272 (f): előbb az arany lap). A #123 migrációja motívumonként,
# a sorrendjében kapcsolja be (DT-F123g (a)): ALVIL-001.
# A motívumonkénti bekapcsolás adat (`adat/funkcio_kapcsolok.tsv`, `SZOTARI_GERINC`), nem kódbeli lista (ISTENTISZT-001
# arany lap, 2026-10-29: a blokk-szintű változások motívum-id szerinti kivétel nélkül; a tesztek felülírhatják).
# F148 (DT437): a gerinc alapból be van kapcsolva; a még nem migrált motívum sora `kivetel` (a #123 a migrációkor
# `aktiv`-ra állítja). Az `ellenoriz.py` 18–21. szabálya ugyanezt a függvényt hívja.
GERINC_KIVETEL_MOTIVUMOK = SZK.kapcsolo_kivetelek('SZOTARI_GERINC')

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
    return bool(motivum_id) and motivum_id not in GERINC_KIVETEL_MOTIVUMOK


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
        cimke[cimke_kulcs(r)] = r
    bdb_sz = {}
    for r in be(BDB_SZAKASZOK_FAJL):
        bdb_sz.setdefault(r['strong'], []).append(r)
    bdb_hu = {}
    for r in be(BDB_SZAKASZ_HU_FAJL):
        bdb_hu[(r['strong'], r['sorszam'])] = r
    bdb_vj, bdb_vj_feloldott = {}, {}
    for r in be(BDB_VERS_JELENTES_FAJL):
        # DT-F104d: a 4.2 kártyájának hivatkozásszáma a feloldott, szűrt hivatkozásoké (a szerver szabálya, Károli-vers nélkül is)
        if VJ.vj_feloldott(r):
            bdb_vj_feloldott.setdefault(r['strong'], []).append(r)
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
    # F123.BDBGER: a teljes angol szócikk (a 2.29 `poz`-ának szövege), a példahely szócikkének azonosításához
    bdb_en = {r['Strong_padded']: r['Teljes_szocikk'] for r in be(BDB_TELJES_FAJL)}
    _gerinc_adat_cache = {'cimke': cimke, 'bdb_sz': bdb_sz, 'bdb_hu': bdb_hu, 'bdb_vj': bdb_vj,
                          'bdb_vj_feloldott': bdb_vj_feloldott,
                          'th_sz': th_sz, 'th_vj': th_vj, 'glossza': glossza, 'tiltott': tiltott,
                          'token_szam': token_szam, 'bdb_en': bdb_en}
    return _gerinc_adat_cache


def _bdb_strong_kulcs(strong):
    """A 2.29/2.30 Strong-alakja (`H7121`; a táblák négyjegyű, betű nélküli kulcsot használnak)."""
    return strong


# --- a szakasz kulcsa: szócikk + útvonal (F123.BDBGER) ----------------------------------------------------------
# Egy Strongnak több BDB-szócikke lehet (`bdb_id`: I., II., arámi); az útvonal (`-/1/-`) csak a szócikken belül egyedi.
# A szakasz kulcsa ezért (bdb_id, utvonal); a Thayer és a TBESG kulcsa ('', utvonal), mert ott a Strong egy szócikk.

# A BDB arámi szócikkei a BDB9264-től (konkordancia/BDB_aram_potlas_README.md: „a BDB9264-től induló arámi szócikkek”)
BDB_ARAMI_ELSO = 9264
_ROMAI_LEMMA_RE = re.compile(r'\s*(?:(IV|V|VI{0,3}|I{1,3})\.\s+)?\[?([^\s\[\]]*[֐-׿][^\s\[\],;]*)')
_bdb_szelet = None


def _szelet_modul():
    """Az olvasó-szerver szeletelője (`olvaso_szerver/bdb_szelet.py`), egyszer betöltve."""
    global _bdb_szelet
    if _bdb_szelet is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'bdb_szelet_lg', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'olvaso_szerver', 'bdb_szelet.py'))
        _bdb_szelet = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_bdb_szelet)
    return _bdb_szelet


def _lapit(szoveg):
    """A szeletelő `lapit`-ja (`olvaso_szerver/bdb_szelet.py`): a 2.29 `poz`-a erre a szövegalakra vonatkozik."""
    return _szelet_modul().lapit(szoveg)


def cimke_kulcs(r):
    """A `szotar_szakasz_cimke.tsv` (SEMA 2.40) sorának kulcsa: (szotar, strong, bdb_id, szakasz); a `bdb_id` csak a
    BDB-sorban nem üres."""
    return (r['szotar'], r['strong'], r.get('bdb_id') or '', r['szakasz'])


def kulcs_ala_esik(finom, durva):
    """Igaz, ha a `finom` szakasz a `durva` alá esik: azonos szócikkben, és az útvonala alá (vagy azonos vele)."""
    return finom[0] == durva[0] and gerinc_ala_esik(finom[1], durva[1])


def bdb_szocikkek(adat, strong):
    """A Strong BDB-szócikkei (`bdb_id`) a 2.30 sorrendjében, ami a BDB saját rendje (I., II., …, arámi)."""
    out = []
    for r in sorted(adat['bdb_sz'].get(strong, []), key=lambda x: int(x['sorszam'])):
        if r.get('bdb_id', '') not in out:
            out.append(r.get('bdb_id', ''))
    return out


def _utvonal_szocikkei(adat, strong, utvonal):
    vag = gerinc_utvonal_vag(utvonal)
    return {r.get('bdb_id', '') for r in adat['bdb_sz'].get(strong, []) if gerinc_utvonal_vag(r['utvonal']) == vag}


def szakasz_kulcs_jel(adat, szotar, strong, k):
    """A szakasz jele (`1.a`); ha az útvonal a Strong több BDB-szócikkében is áll, a szócikk azonosítójával (`BDB2718 1.a`)."""
    jel = szakasz_jel(k[1])
    if szotar == 'BDB' and k[0] and len(_utvonal_szocikkei(adat, strong, k[1])) > 1:
        return '%s %s' % (k[0], jel)
    return jel


def bdb_szocikk_fejcim(adat, strong, bdb_id):
    """A szócikk fejcíme a lapon: `BDB2718 · I. חַיָּה`, az arámi szócikknél `· arámi` (a fej angol szövegének római száma
    és első héber szava; ha nincs, csak az azonosító)."""
    fej = next((r for r in sorted(adat['bdb_sz'].get(strong, []), key=lambda x: int(x['sorszam']))
                if r.get('bdb_id', '') == bdb_id and r['utvonal'] == 'fej'), None)
    reszek = [bdb_id]
    m = _ROMAI_LEMMA_RE.match((fej or {}).get('szoveg') or '')
    if m:
        reszek.append(('%s. %s' % (m.group(1), m.group(2))) if m.group(1) else m.group(2))
    szam = re.match(r'BDB(\d+)$', bdb_id or '')
    if szam and int(szam.group(1)) >= BDB_ARAMI_ELSO:
        reszek.append('arámi')
    return ' · '.join(reszek)


def _bdb_sor_kezdetek(adat, strong):
    """[(bdb_id, kezdet vagy None)] a 2.30 sorrendjében: a sor szövegének kezdete a teljes angol szócikk `lapit`-alakjában
    (a 2.29 `poz`-ának koordinátái), sorban előre keresve; None, ha a szöveg nem található vagy rövid (15 karakter alatt)."""
    cache = adat.setdefault('_bdb_kezdet', {})
    if strong not in cache:
        s = _lapit((adat.get('bdb_en') or {}).get(strong, ''))
        ki, kurzor = [], 0
        for r in sorted(adat['bdb_sz'].get(strong, []), key=lambda x: int(x['sorszam'])):
            t = _lapit(r.get('szoveg') or '')[:40]
            i = s.find(t, kurzor) if s and len(t) >= 15 else -1
            ki.append((r.get('bdb_id', ''), i if i >= 0 else None))
            if i >= 0:
                kurzor = i + 1
        cache[strong] = ki
    return cache[strong]


def _bdb_poz_szocikkei(adat, strong, poz):
    """A szócikkek, amelyekben a `poz` állhat: az előtte kezdődő utolsó megtalált sor szócikke és a következő megtalált
    sorig a nem megtalált sorok szócikkei (szöveg nélkül: mind)."""
    sorok = _bdb_sor_kezdetek(adat, strong)
    elotte = [k for k, (_b, i) in enumerate(sorok) if i is not None and i <= poz]
    utana = [k for k, (_b, i) in enumerate(sorok) if i is not None and i > poz]
    tol = elotte[-1] if elotte else 0
    ig = utana[0] if utana else len(sorok)
    return {sorok[k][0] for k in range(tol, ig)}


def _vers_ut_szocikkei(adat, strong, ut):
    """Az útvonal szerint szóba jövő szócikkek: `fej` — amelynek van feje; `tagolatlan` — amelynek csak feje van."""
    sorok = adat['bdb_sz'].get(strong, [])
    if ut == 'fej':
        return {x.get('bdb_id', '') for x in sorok if x['utvonal'] == 'fej'}
    if ut == 'tagolatlan':
        return {b for b in bdb_szocikkek(adat, strong)
                if all(x['utvonal'] in ('cim', 'fej') for x in sorok if x.get('bdb_id', '') == b)}
    return _utvonal_szocikkei(adat, strong, ut)


def _bdb_poz_megbizhato(adat, strong):
    """A hely (`poz`) szerinti szócikk-sávok megbízhatók-e a Strongban: az útvonalból egyértelmű minden 2.29-sorban a
    hely szerinti jelöltek között ott van az útvonal szócikke (a két forrás szócikkhatára egyezik). Ha valahol nem,
    a hely a Strongban nem dönt (mérés: naplok/F123_BDBGER_meres.md)."""
    cache = adat.setdefault('_bdb_poz_ok', {})
    if '_bdb_vj_strong' not in adat:
        idx = {}
        for (st, _v), sorok in adat['bdb_vj'].items():
            idx.setdefault(st, []).append(sorok)
        adat['_bdb_vj_strong'] = idx
    if strong not in cache:
        ok = True
        for sorok in adat['_bdb_vj_strong'].get(strong, []):
            for r in sorok:
                if r['utvonal'] in ('fej', 'tagolatlan'):
                    continue
                ut_j = _utvonal_szocikkei(adat, strong, r['utvonal'])
                try:
                    if len(ut_j) == 1 and not ut_j <= _bdb_poz_szocikkei(adat, strong, int(r.get('poz'))):
                        ok = False
                except (TypeError, ValueError):
                    pass
        cache[strong] = ok
    return cache[strong]


def bdb_vers_szocikk(adat, strong, r):
    """A 2.29 sorának szócikke: (bdb_id vagy None, ok). A 2.29 nem a 2.30 szócikk-azonosítóját hordozza; a szócikk az
    útvonalból jön, ha az a Strongnak csak egy szócikkében áll, különben a hivatkozás helyéből (`poz`) is, ha az a
    Strongban megbízható: az a szócikk, amely mindkettőnek megfelel (ha az útvonal a 2.30-ban nincs meg, csak a helyé).
    Ha nem egyértelmű, None: a példa nem rendelhető szakaszhoz (választás nélkül)."""
    ids = bdb_szocikkek(adat, strong)
    if len(ids) <= 1:
        return (ids[0] if ids else None), ''
    ut = r['utvonal']
    ut_j = _vers_ut_szocikkei(adat, strong, ut)
    if len(ut_j) == 1:
        return next(iter(ut_j)), ''
    if not _bdb_poz_megbizhato(adat, strong):
        return None, ('a %s útvonal a %s szócikkei közül %s; a hivatkozás helye (`poz`) itt nem dönt, mert a 2.29 és a '
                      '2.30 szócikkhatára a Strongban máshol eltér'
                      % (ut, strong, ('ezekben áll: ' + ', '.join(b for b in ids if b in ut_j)) if ut_j else 'egyikben sem áll'))
    try:
        p_j = _bdb_poz_szocikkei(adat, strong, int(r.get('poz')))
    except (TypeError, ValueError):
        p_j = set(ids)
    j = (ut_j & p_j) if ut_j else p_j
    if len(j) == 1:
        return next(iter(j)), ''
    return None, ('a %s útvonal a %s szócikkében áll (%s), a hivatkozás helye (`poz` %s) szerint: %s'
                  % (ut, strong, ', '.join(b for b in ids if b in ut_j) or EM_DASH, r.get('poz'),
                     ', '.join(b for b in ids if b in p_j) or EM_DASH))


def kutatoi_szakasz(adat, szotar, strong, kulcs):
    """A kutatói jelentésszám leképezése a szótár szakaszára (DT372 2.): az a sor, amelynek
    `lexikon_jelentes_szam`-a a kulcs, (bdb_id, szakasz) alakban; None, ha nincs leképezve."""
    talalat = [(k[2], k[3]) for k, r in adat['cimke'].items()
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
                # F123.BDBGER: a tartomány szövege a példahely saját szócikkéé; nem azonosítható szócikknél nincs állítás
                b, _ok = bdb_vers_szocikk(adat, strong, r)
                if b is not None:
                    csoport.setdefault((b, gerinc_utvonal_vag(r['utvonal']), r['nyers']), []).append(r)
    ki = []
    for (b, vag, nyers), sorok in sorted(csoport.items()):
        szoveg = ' '.join(' '.join(x for x in (sz.get('jel'), sz.get('szoveg')) if x)
                          for sz in adat['bdb_sz'].get(strong, [])
                          if sz.get('bdb_id', '') == b and gerinc_utvonal_vag(sz['utvonal']) == vag)
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
                          % (szakasz_szoveg(szakasz_kulcs_jel(adat, 'BDB', strong, (b, r['utvonal']))),
                             _nevelo(r['karoli_vers']), r['karoli_vers'], veg, nyers,
                             t.group(0).strip(), BDB_VERS_JELENTES_FAJL, r['sorszam']))
    return ki


def _bdb_sor_utvonal(adat, strong, bdb_id, vag_ut):
    """A 2.30 teljes útvonala a levágott alakhoz (`-/3` → `-/3/-`), a szócikken belül."""
    for r in adat['bdb_sz'].get(strong, []):
        if r.get('bdb_id', '') == bdb_id and gerinc_utvonal_vag(r['utvonal']) == vag_ut:
            return r['utvonal']
    return None


def _pelda_kulcs(adat, strong, b, r):
    """A példahely szakaszkulcsa: (bdb_id, a 2.30 teljes útvonala)."""
    vag = gerinc_utvonal_vag(r['utvonal'])
    return (b, _bdb_sor_utvonal(adat, strong, b, vag) or r['utvonal'])


def jelentes_cimke_token(adat, szotar, strong, jelentes_szam, vers, kutatoi_token):
    """Egy token címkéje egy versen: (címke-szöveg vagy None, jel, ⓘ-szöveg).
    Elsőbbség (DT374): ha a szótár maga idézi a helyet, és útja a kutatói út alá esik, a finomabb
    útvonal címkéje; ha egyik sem esik a másik alá: GerincHiba. A címke a szóról szól."""
    kulcs, minosito = kutatoi_kulcs(jelentes_szam) if kutatoi_token else ('', '')
    kut_k = kutatoi_szakasz(adat, szotar, strong, kulcs) if kulcs else None
    if kutatoi_token and kulcs and kut_k is None:
        return None, '', ('a kutatói jelentésszám („%s”) nincs leképezve a %s tagolására (`%s`)'
                          % (kulcs, szotar, SZAKASZ_CIMKE_FAJL))

    def kjel(k):
        return szakasz_kulcs_jel(adat, szotar, strong, k)

    # F123.BDBGER: a példahely szakaszkulcsa (bdb_id, útvonal); ha a szócikk nem azonosítható, a példa nem kerül a tokenre
    peldak, nem_azon = [], []
    for r in (bdb_peldak(adat, strong, vers) if szotar == 'BDB' else []):
        b, ok = bdb_vers_szocikk(adat, strong, r)
        if b is None:
            nem_azon.append('a BDB a helyet idézi (`%s` sorszam %s), de nem azonosítható, melyik szócikkében (%s); a '
                            'BDB-példa ezért nem kerül erre a tokenre' % (BDB_VERS_JELENTES_FAJL, r['sorszam'], ok))
        else:
            peldak.append((_pelda_kulcs(adat, strong, b, r), r))
    tobb_token = []
    n_token = (adat.get('token_szam') or {}).get((vers, strong), 0)
    if peldak and n_token >= 2:
        # ELLENOR_SZOTARI_GERINC 1. (7.4a): a BDB-példa versszintű (a 2.29 nem jelöli a szót); ha a versben a
        # Strongnak több tokenje van, a példa nem rendelhető a sor tokenjéhez — a címke nem a BDB-példából jön
        tobb_token.append('a BDB a verset %s szakaszban idézi (`%s` sorszam %s), de a versben a szó %s áll '
                          '(`%s`), és a szótár nem jelöli, melyikre gondol; a BDB-példa ezért nem kerül erre a '
                          'tokenre' % (szakasz_szoveg(sorted({kjel(k) for k, _r in peldak})),
                                       BDB_VERS_JELENTES_FAJL, ', '.join(r['sorszam'] for _k, r in peldak),
                                       _HANYSZOR.get(n_token, '%d alkalommal' % n_token), TAHOT_KIVONAT_FAJL))
        peldak = []
    pelda_k = sorted({k for k, _r in peldak})
    ip = []
    if len(pelda_k) > 1:
        # F123 (DT-F123h): a több útvonalú BDB-példát a kutatói hozzárendelés dönti el, ha pontosan egy útvonal esik alá;
        # a többi útvonal ⓘ-ben marad (a szótár ott is idézi). Kutatói kulcs nélkül, vagy ha ez nem egyértelmű: kézi kérdés.
        ala = [k for k in pelda_k if kut_k and kulcs_ala_esik(k, kut_k)]
        if len(ala) != 1:
            raise GerincHiba('%s %s: a BDB-példák több útvonalra mutatnak (%s): kézi kérdés' % (strong, vers, pelda_k))
        mas = [(k, r) for k, r in peldak if k != ala[0]]
        ip.append('a BDB a helyet %s is idézi (`%s` sorszam %s); a kutatói hozzárendelés (%s → %s, `%s`) dönt'
                  % (szakasz_szoveg(sorted({kjel(k) for k, _r in mas})),
                     BDB_VERS_JELENTES_FAJL, ', '.join(r['sorszam'] for _k, r in mas), kulcs, kjel(kut_k), SZAKASZ_CIMKE_FAJL))
        peldak = [(k, r) for k, r in peldak if k == ala[0]]
        pelda_k = ala
    if peldak:
        p_k = pelda_k[0]
        sorszamok = ', '.join(r['sorszam'] for _k, r in peldak)
        # DT381 (a): a forrás hibás versét a 2.31 kézi sora javította; az ⓘ a javítás forrását nevezi meg
        for _k, r in peldak:
            if 'forras_javitas' in (r.get('okkod') or '').split(','):
                ip.append('a BDB forrásszövege itt a „%s” helyet idézi (sajtóhiba); javítva: %s — a javítás forrása: `%s`, '
                          'kézi sor (`hivatkozas_kezi`, `manual`; indok: a TAHOT és a szövegkörnyezet; DT381 (a))'
                          % (r['nyers'], r['karoli_vers'], BDB_FORRAS_JAVITAS_FAJL))
        if kut_k is None:
            valasztott = p_k
            ip.append('BDB-példa: a BDB %s szakaszban maga idézi a helyet (`%s` sorszam %s)'
                      % (szakasz_szoveg(kjel(p_k)), BDB_VERS_JELENTES_FAJL, sorszamok))
        elif kulcs_ala_esik(p_k, kut_k):
            valasztott = p_k
            ip.append('BDB-példa: a BDB %s szakaszban maga idézi a helyet (`%s` sorszam %s); ez a kutatói '
                      'hozzárendelés (%s → %s) alá esik, a címke a finomabb útvonalé'
                      % (szakasz_szoveg(kjel(p_k)), BDB_VERS_JELENTES_FAJL, sorszamok, kulcs, kjel(kut_k)))
        elif kulcs_ala_esik(kut_k, p_k):
            valasztott = kut_k
            ip.append('kutatói hozzárendelés a BDB tagolása szerint (%s → %s, `%s`); a BDB a helyet a tágabb '
                      '%s szakaszban idézi (`%s` sorszam %s)'
                      % (kulcs, kjel(kut_k), SZAKASZ_CIMKE_FAJL, szakasz_szoveg(kjel(p_k), nevelo=False), BDB_VERS_JELENTES_FAJL,
                         sorszamok))
        else:
            raise GerincHiba('%s %s: a BDB-példa (%s) és a kutatói hozzárendelés (%s → %s) egyike sem esik a '
                             'másik alá: kézi kérdés, választás nélkül' % (strong, vers, p_k, kulcs, kut_k))
    elif kut_k is not None:
        valasztott = kut_k
        ip.append('kutatói hozzárendelés a %s tagolása szerint (`elofordulasok.tsv` jelentes_szam „%s” → %s, `%s`)'
                  % (szotar, kulcs, ('' if szotar == 'BDB' else szotar + ' ') + kjel(kut_k),
                     SZAKASZ_CIMKE_FAJL))
        ip.extend(tobb_token)
        # a vers közvetlenül idézett (csak a token bizonytalan): a „nem önállóan idézi” tartomány-mondat nem igaz rá
        if szotar == 'BDB' and not tobb_token:
            ip.extend(bdb_tartomanyban(adat, strong, vers))
    else:
        tart = bdb_tartomanyban(adat, strong, vers) if szotar == 'BDB' and not tobb_token else []
        return None, '', '; '.join(tobb_token + nem_azon + tart)
    ip.extend(nem_azon)
    if minosito:
        ip.append('a kutatói jelentésszám minősítője („%s”) nem a szó jelentése, a címkébe nem kerül '
                  '(a minősítő nem része a SEMA 2.2.2 értékkészletének)'
                  % minosito)
    sor = adat['cimke'].get((szotar, strong) + valasztott)
    cimke = (sor or {}).get('cimke_hu') or None
    jel = kjel(valasztott)
    if szotar != 'BDB':
        jel = '%s %s' % (szotar, jel)
    return cimke, jel, '; '.join(ip)




def _szakasz_olvasoi_glossza(adat, strong, jel):
    """F182: a BDB-szakasz olvasói glosszája a jele szerint (a kártya szabályával: `olvasoi_glossza`); None, ha nincs."""
    for sz in bdb_gerinc_szocikkek(adat, strong)[0]:
        for k, j, hu, _a, _f in sz['szakaszok']:
            if szakasz_kulcs_jel(adat, 'BDB', strong, k) == jel:
                cimke = (adat['cimke'].get(('BDB', strong) + k) or {}).get('cimke_hu') or ''
                return olvasoi_glossza(j, cimke, hu)
    return None


def _tagolatlan_olvasoi(adat, strong):
    """F182: a tagolatlan (számozott jelentés nélküli) BDB-szócikk olvasói neve a fej glosszájával; None, ha a szócikk tagolt."""
    szocikkek = bdb_gerinc_szocikkek(adat, strong)[0]
    if len(szocikkek) != 1 or szocikkek[0]['szakaszok']:
        return None
    fej = szocikkek[0]['fej']
    gl = fej_glossza(fej[2] if fej and fej[2] else '')
    return 'a szócikk egésze' + (' — %s' % gl if gl else '')


def jelentes_cella(adat, sor, uj=False):
    """Az előfordulás-tábla „Jelentés (a szó)” cellája és az ⓘ szövege: (cella, ⓘ).
    Összetett Strong-mezőnél tokenenként; a kutatói hozzárendelés a `lexikon_entry_id` tokenjéé. `uj` (F182, az új
    szerkezetű lap): címke nélküli pontnál a szakasz olvasói glosszája áll a „(nincs címke: …)” helyett, a tagolatlan
    szócikknél „a szócikk egésze” a „(nincs hozzárendelés)” helyett (a régi lapok szövege változatlan, E28)."""
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
        gl = _szakasz_olvasoi_glossza(adat, t, jel) if (uj and not cimke and jel and t_szotar == 'BDB') else None
        tg = _tagolatlan_olvasoi(adat, t) if (uj and not cimke and not jel and t.startswith('H')) else None
        if cimke:
            szov = '%s · %s' % (cimke, jel)
        elif gl:
            szov = '%s · %s' % (gl, jel)
        elif tg:
            szov = tg
        elif jel:
            szov = '*(nincs címke: %s)*' % jel
        else:
            szov = '*(nincs hozzárendelés)*'
            if not info:
                info = 'ehhez a tokenhez nincs kutatói hozzárendelés és szótári példahely'
        reszek.append((t, szov))
        ik.append('%s — %s' % (t, info) if len(tokenek) > 1 else info)
    if not reszek:
        return (EM_DASH if uj else '*(nincs hozzárendelés)*'), 'a sornak nincs Strong-tokenje'
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
                    cellak.append('*(a jelentés nincs a DBH-táblában)*')
                    continue
                szov = ubs_glossza_cella('UBS_DBH', t, lx, EM_DASH, r['glosszak'])
                cellak.append('%s%s' % (szov, '' if mt == vers else ' *(MT: %s)*' % mt))
        # tartomány-sornál (pl. 5Móz 27:15-26) a versek ugyanazt a jelentést adják: sorrendtartó ismétlésszűrés
        cellak = list(dict.fromkeys(cellak))
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


def kiemel(szoveg, celok, mark=False, extra=None):
    """A célversek (`[(vers, azonosító)]`, vers Károli-alakban: `1Móz 4:26`) előfordulásait a szövegben
    felirat nélkül kiemeli (`**…**`). Versenként a k-adik előfordulás a k-adik azonosítóé.
    `mark` (az új szerkezetű lap; a felhasználó a v6-on: „a félkövér nem erőteljes, nem jól látható … látványosabb
    jelölés kell”): a kiemelés `<mark class="motivumhely" title="a motívum helye: 1Móz 3:23">`; a title a teljes
    igehely, mert a BDB folytatásos írásmódjában a hivatkozás gyakran csak versszám („3:17, 23”). A BDB szövege
    nem változik.
    `extra` (az új szerkezetű lap; a lektor ajánlása, a felhasználó jóváhagyásával): a motívum minden verse, amelyet a
    szócikk idéz, kiemelve áll, bármelyik szón áll a motívum sora; a jelentéspont-hozzárendelést (`talalt`) nem érinti.
    Visszaad: (új szöveg, [kiemelt azonosítók], [meg nem talált azonosítók])."""
    hiv = hivatkozasok_a_szovegben(szoveg)
    poz = {}
    for kezd, veg, konyv, fej, v in hiv:
        if konyv:
            poz.setdefault('%s %s:%s' % (konyv, fej, v), []).append((kezd, veg))
    csoport = {}
    for vers, azon in celok:
        csoport.setdefault(vers, []).append(azon)
    talalt, hianyzik, jelolok = [], [], {}
    for vers, azonok in csoport.items():
        helyek = poz.get(vers, [])
        for i, azon in enumerate(azonok):
            if i < len(helyek):
                jelolok.setdefault(helyek[i], vers)
                talalt.append(azon)
            else:
                hianyzik.append(azon)
    if mark and extra:
        for vers in extra:
            for hely in poz.get(vers, []):
                jelolok.setdefault(hely, vers)
    for (kezd, veg), vers in sorted(jelolok.items(), reverse=True):
        if mark:
            nyit = '<mark class="motivumhely" title="a motívum helye: %s">' % _vers_teljes(vers)
            szoveg = szoveg[:kezd] + nyit + szoveg[kezd:veg] + '</mark>' + szoveg[veg:]
        else:
            szoveg = szoveg[:kezd] + '**' + szoveg[kezd:veg] + '**' + szoveg[veg:]
    return szoveg, talalt, hianyzik


def _vers_teljes(vers):
    """A kiemelés title-je: a Károli-alakú igehely (a forrásjavított „26:35” alak is könyvnévvel áll)."""
    return vers.replace('"', '&quot;')


def _elso_tagmondat(szoveg, hatar=90, csonkit_jel=False):
    """A vázlatsor: a szöveg első tagmondata. `csonkit_jel` (F182, N137: a kétrétegű kártya): ha a tagmondat-határ után
    a szöveg folytatódik, a sor „…”-re végződik — a cím hivatkozásszáma a teljes szakaszé, a sor csak az elejét mutatja."""
    s = re.sub(r'^\s*(?:(?:\d+|[a-z]|T:\S+)\.?\s+){1,2}', '', szoveg or '').strip()
    # a tagmondat-határ csak zárójelen kívül (F123.GENKOR: „(|| אוֺת; így …)” belsejében nem vág; olvasói kapu ZAROJEL)
    m = next((m for m in re.finditer(r'(?<!\d):|:(?!\d)|;', s)
              if s[:m.start()].count('(') <= s[:m.start()].count(')')), None)
    if m and m.start() <= hatar:
        folytatodik = bool(s[m.end():].strip(' .;:'))
        s = s[:m.start()]
        if csonkit_jel and folytatodik:
            s = s.rstrip(' ,;:') + ' …'
    elif len(s) > hatar:
        s = s[:hatar].rstrip()
        # nyitva maradó zárójel elé vágunk (olvasói kapu ZAROJEL, N-F123f)
        if s.count('(') > s.count(')'):
            s = s[:s.rfind('(')].rstrip(' ,;')
        s = s + '…'
    # a forrásban nyitva maradt zárójel a vázlatsorban sem marad nyitva (F123.GENKOR)
    while s.count('(') > s.count(')') and s.rfind('(') > 0:
        s = s[:s.rfind('(')].rstrip(' ,;') + '…'
    return s.strip() or EM_DASH


def _vazlat_sor(jel, cimke, szoveg):
    return '- `%s` — %s' % (jel, cimke if cimke else _elso_tagmondat(szoveg))


HORGONNYAL_JELOLES = ' *(kutatói jelölés: a szakaszhatár horgonnyal illesztve, ellenőrzendő)*'


def _osszecsukva(sorok, elso, utolso):
    cim = elso if elso == utolso else '%s – %s' % (elso, utolso)
    return ('<details>\n<summary>%s (%d szakasz)</summary>\n\n%s\n\n</details>'
            % (cim, len(sorok), '\n'.join(sorok)))


def _kulcs_hely(k, rag):
    """A szakaszkulcs prózában, raggal: `('BDB8371', 'fej'), 'nak'` → „a BDB8371 szócikk fejének”."""
    if k[1] == 'fej':
        return 'a %s szócikk fej%s' % (k[0], 'ének' if rag == 'nak' else 'ét')
    return 'a %s szócikk %s szakasz%s' % (k[0], szakasz_szoveg(szakasz_jel(k[1]), nevelo=False), 'ának' if rag == 'nak' else 'át')


def elnyelt_mondat(hova):
    """F123.BDBGER: a szakasz magyar szövege (a 2.32 jelölő nélküli sora szerint) egy másik szócikk szakaszában áll;
    a forrás (a 2.32) a gerinc ⓘ-jében áll, az olvasói szövegben nem."""
    return '*A magyar szöveg %s fordításában áll (a fordítás nem választja külön).*' % _kulcs_hely(hova, 'nak')


def elnyelo_mondat(kulcsok):
    """F123.BDBGER: a szakasz magyar szövege egy másik szócikk szövegét is tartalmazza (a 2.32 szerint)."""
    return '*(a magyar szöveg %s is tartalmazza)*' % _es_lista([_kulcs_hely(k, 't') for k in kulcsok])


# --- F104 (DT-F104b): a 4.2 kétrétegű BDB-kártyája az új szerkezetű lapon ------------------------------------------
# Olvasói réteg: a jelentések rendje tömören (glosszával) és a motívum helyeinek jelentése (DT178: a szótár nem idézte
# helynél nincs tippelt pont). Kutatói réteg: a teljes BDB-szöveg (fej, kibontott és összecsukott szakaszok, kutatói
# megjegyzés, a szónézet-mutató), alapból csukott <details>-ben. A kutatói réteg gépi jelölője EGY helyen áll (itt); a
# SEMA, a sablon és az olvasói kapu csak hivatkozik rá. A <details> sor szándékosan attribútum nélküli: a meglévő
# <details>-számlálók (`kiejtes_szoveg.py`, `torzscikk_general.py`) így változatlanul működnek.
# A KAPCSOLÓ (DT-F104c): a kétrétegű kártya csak az itt felsorolt (új szerkezetű) lapokon áll; ma üres, így minden lap
# bájtra a korábbi alakjában generálódik (E28). A #182 a HAMART-001 újragenerálásakor veszi fel; a régi lapok a saját
# teljes folyamatukban. A kapcsoló egyetlen helye ez; a kapu (`olvasoi_kapu.BDB_OLVASOI`) a lap jelölőjéhez igazodik.
# F187: ugyanez a kapcsoló a görög 4.2 Thayer-kártyáját is kétrétegűvé teszi (egy kapcsoló, egy jelölő, egy kapu).
# F182 (2. fázis, F25): a HAMART-001 az F33 (a tagolás a szakasztáblából, egy forrásból) után kapcsolva be.
KETRETEGU_BDB_KARTYA = frozenset({'HAMART-001'})


def bdb_kartya_aktiv(motivum_id):
    return motivum_id in KETRETEGU_BDB_KARTYA and uj_szerkezet(motivum_id)


APPARATUS_KEZDET = '<!-- APPARATUS-KEZDET: %s -->'
APPARATUS_VEGE = '<!-- APPARATUS-VÉGE: %s -->'
APPARATUS_CIM = 'Szótári apparátus'
APPARATUS_RX = re.compile(r'<!-- APPARATUS-(KEZDET|VÉGE): (\S+) -->')
UJ_GERINC_BEVEZETO = {
    # a felhasználó átnézése (5.): olvasói mondat, a döntés-hivatkozás és a dátum nélkül
    'BDB': ('*Szavanként előbb a jelentések rendje áll a BDB szerint, rövid magyar meghatározással, és az, hogy a motívum '
            'helyein melyik jelentésben áll a szó; ahol a szótár a helyet nem idézi, ott jelentéspont sincs. Alatta, '
            'összecsukva, a szótári apparátus: a teljes BDB-szócikk magyarul, a rövidítésekkel, az alakok jegyzékével és '
            'az igehelyekkel. A szócikkben kiemelve áll minden vers, amely a motívum helye, bármelyik szón áll a motívum '
            'sora; az egérmutató alatt a teljes igehellyel. A szótári rész a szóról szól; a hely funkcióját a motívumban a 2. szakasz táblázata adja.*'),
    'Thayer': ('*Szavanként előbb a jelentések rendje áll a Thayer szerint, rövid magyar meghatározással, és az, hogy a '
               'motívum helyein melyik jelentésben áll a szó; ahol a szótár a helyet nem idézi, ott jelentéspont sincs. '
               'Alatta, összecsukva, a szótári apparátus: a teljes Thayer-szócikk magyarul, a görög alakok jegyzékével, a '
               'klasszikus párhuzamokkal és az igehelyekkel. A szócikkben kiemelve áll minden vers, amely a motívum '
               'helye, bármelyik szón áll a motívum sora; az egérmutató alatt a teljes igehellyel. A szótári rész a szóról szól; a hely funkcióját a motívumban a 2. '
               'szakasz táblázata adja.*'),
}

# F187 (DT-F104b Thayer-ága): a vers -> jelentéspont hozzárendelés mért pontossága a lap bevezetőjében nem áll (a szó-lapon
# áll, `olvaso_szerver/konfig/thayer_pontossag.toml`); a lapon csak a jelentésfa és a helyek.
def thayer_hivatkozas_szam(adat, strong):
    """A Thayer-kártya hivatkozásszámai a vers -> jelentés táblából (2.35): {('', a szakasztábla útvonala): sorok száma}
    (a `gerinc_blokk` illesztése szerint: a levágott útvonal a szakasztáblában)."""
    cache = adat.setdefault('_th_hiv_db', {})
    if strong not in cache:
        teljes = {}
        for r in adat['th_sz'].get(strong, []):
            teljes.setdefault(gerinc_utvonal_vag(r['utvonal']), r['utvonal'])
        db = collections.Counter()
        for (s, _v), sorok in adat.get('th_vj', {}).items():
            if s == strong:
                for r in sorok:
                    u = teljes.get(gerinc_utvonal_vag(r['utvonal']))
                    if u is not None:
                        db[('', u)] += 1
        cache[strong] = db
    return cache[strong]


def fej_glossza(hu):
    """A tagolatlan szócikk meghatározása a fej magyar szövegéből: az első gondolatjel előtti utolsó (nem versszámbeli)
    kettőspont után álló rész („… főnév Zsolt 7:17: erőszak, jogtalanság — …” → „erőszak, jogtalanság”)."""
    s = hu or ''
    vege = re.search(r'\s[—–]\s', s)
    s = s[:vege.start()] if vege else s[:200]
    kp = [m for m in re.finditer(':', s) if not (m.start() and s[m.start() - 1].isdigit() and s[m.end():m.end() + 1].isdigit())]
    return olvasoi_glossza('', '', s[kp[-1].end():]) if kp else None


_ALAK_UTAN = re.compile(r'[֐-׿יִ-ﭏ][^\s]*\s*(?:\([^)]*\)\s*)?\u200e?\s*'
                        r'([a-záéíóöőúüű][a-záéíóöőúüű ,]*?)(?=\s*(?:[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\s+)?\d+:\d+|\s*[;(.:]|[\s,]*[֐-׿יִ-ﭏ]|$)')


def alak_utani_glossza(szoveg):
    """Az alakjegyzékkel nyíló szakasz magyar meghatározása az alak után („participium נֵאָרִים átkozott Mal 3:9” →
    „átkozott”), ha van; None, ha a szakasz csak alakot közöl."""
    for m in _ALAK_UTAN.finditer(szoveg or ''):
        g = m.group(1).strip(' ,')
        if len(g) >= 3 and not _ALAKTANI_KEZDET.match(g) and not re.fullmatch(r'(?:és|vagy|mind|stb)', g):
            return g
    return None


def gondolatjel_utani_glossza(hu):
    """F182 (A17; F10 (2), K55): a törzs-szakasz (Hithpa'el, Niph'al …) glosszája, ha a címketábla nem ad: a BDB-szakasz
    alakjegyzéke utáni első gondolatjel és a következő pontosvessző / zárójel / pont közti rész („… 1Sám 16:1 összesen
    2-szer stb.; — gyászolni (többnyire próza)” → „gyászolni”); None, ha nincs ilyen vagy nem magyar szó."""
    def jo(g):
        return g and 3 <= len(g) <= 80 and not re.search(r'[֐-׿יִ-ﭏ\d]', g) and not _ALAKTANI_KEZDET.match(g)
    for m in re.finditer(r'\s—\s+([a-záéíóöőúüű][^;(.:]*?)\s*(?=[;(.:]|$)', hu or ''):
        if jo(m.group(1).strip(' ,')):
            return m.group(1).strip(' ,')
    m = re.search(r'^\S+:\s+([a-záéíóöőúüű][^;(.:]*?)(?=,\s*(?:perfectum|imperfectum|participium|infinitivus)|[;(.:]|$)',
                  hu or '')
    g = m.group(1).strip(' ,') if m else (alak_utani_glossza(hu) or '')
    return g if jo(g) else None


def _jel_olvasoi(jel):
    return szakasz_szoveg(jel, nevelo=False)


def _versek_rovid(versek):
    """„1Móz 3:17, 1Móz 3:23, Sof 1:2” → „1Móz 3:17, 3:23, Sof 1:2” (az ismételt könyvnév elmarad)."""
    ki, elozo = [], None
    for v in versek:
        konyv, hely = v.rsplit(' ', 1)
        ki.append(hely if konyv == elozo else v)
        elozo = konyv
    return ', '.join(ki)


def bdb_hivatkozas_szam(adat, strong):
    """DT-F104d: a kártya hivatkozásszámai a vers -> jelentés táblából (2.29), nem a magyar szakaszszöveg regexéből:
    {szakaszkulcs (bdb_id, a 2.30 útvonala; a fejé (bdb_id, 'fej')): a feloldott, szűrt hivatkozások száma}. A sorhalmaz a
    szerver pontos hivatkozásszámáé (`bdb_vj_szabaly.vj_feloldott`: `szurt≠1`, van MT-vers); a sor szakasza a `gerinc_blokk`
    illesztése (`bdb_vers_szocikk` + a levágott útvonal a szakasztáblában). A szám a szakasz saját soraié (az alpontoké nem),
    mint a szerver `VersJelolo.db`-jében; a szócikkhez nem köthető sor egyik szakaszhoz sem számít."""
    cache = adat.setdefault('_bdb_hiv_db', {})
    if strong not in cache:
        szocikkek, _elnyelt = bdb_gerinc_szocikkek(adat, strong)
        teljes_ut = {(k[0], gerinc_utvonal_vag(k[1])): k for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
        db = collections.Counter()
        for r in adat.get('bdb_vj_feloldott', {}).get(strong, []):
            b, _ok = bdb_vers_szocikk(adat, strong, r)
            if b is None:
                continue
            k = (b, 'fej') if r['utvonal'] == 'fej' else teljes_ut.get((b, gerinc_utvonal_vag(r['utvonal'])))
            if k is not None:
                db[k] += 1
        cache[strong] = db
    return cache[strong]


def bdb_kulcs_olvashato(k):
    """N-F187b: a szakaszkulcs olvasható forrás-hivatkozásként: `('BDB9520', 'fej')` → „BDB 9520. szócikk, feje”,
    `('BDB2699', '-/5/-')` → „BDB 2699. szócikk, 5. szakasz” (nyers útvonal nélkül; a lap szóhasználata „szakasz”, nem „pont”)."""
    m = re.match(r'BDB(\d+)$', k[0] or '')
    nev = ('BDB %s. szócikk' % m.group(1)) if m else (k[0] or 'a szócikk')
    if k[1] == 'fej':
        return '%s, feje' % nev
    return '%s, %s szakasz' % (nev, szakasz_szoveg(szakasz_jel(k[1]), nevelo=False))


_BDB_AZON_RX = re.compile(r'(?<![\w.])BDB(\d+)\b(?:\s+szócikk)?')


def bdb_azonosito_olvashato(szoveg):
    """N-F187b (orkesztrátori döntés, 2026-11-10): a kutatói rétegben (apparátus) a BDB-szócikk azonosítója forrás-hivatkozásként
    maradhat, olvasható formában: „BDB9520” / „BDB9520 szócikk” → „BDB 9520. szócikk”. Az olvasói rétegben nem áll (kapu)."""
    return _BDB_AZON_RX.sub(lambda m: 'BDB %s. szócikk' % m.group(1), szoveg)


SORSZAMNEV = ('első', 'második', 'harmadik', 'negyedik', 'ötödik', 'hatodik')
CSAK_ALAKKENT = 'a szótár csak alakként idézi'


def _szocikk_olvasoi_nev(adat, strong, bdb_id, i):
    """F187 / F29 (c): a több szócikkes Strong szócikkének olvasói neve belső azonosító és számjegyes sorszám nélkül
    („első szócikk”), arámi szócikknél „(arámi)”. A héber címszó nem áll itt (a kiejtés-szabály miatt csak a jóváhagyott
    kiejtéssel állhatna; a szócikkek címszava az apparátusban áll)."""
    nev = '%s szócikk' % (SORSZAMNEV[i - 1] if i <= len(SORSZAMNEV) else 'további')
    szam = re.match(r'BDB(\d+)$', bdb_id or '')
    if szam and int(szam.group(1)) >= BDB_ARAMI_ELSO:
        nev += ' (arámi)'
    return nev


def _os_pont(a, b):
    """Igaz, ha az `a` szakaszkulcs a `b` őse ugyanabban a szócikkben (`Hiph'il` → `Hiph'il/2`, `-/1` → `-/1/b`)."""
    if a[0] != b[0] or a[1] in ('fej', 'tagolatlan') or b[1] in ('fej', 'tagolatlan'):
        return False
    pa, pb = gerinc_utvonal_vag(a[1]).split('/'), gerinc_utvonal_vag(b[1]).split('/')
    return len(pa) < len(pb) and pb[:len(pa)] == pa


def helyek_pontjai(vers_pont, szocikkek):
    """F29 (b): {vers: [kulcs]} a vers → pont párokból, a vers első előfordulásának sorrendjében. A tagolatlan szócikk fej-pontja a
    szócikk egésze; a fej-pont elmarad, ha a versnek más pontja is van; az ős-pont elmarad, ha ugyanannál a versnél a
    leszármazottja is áll."""
    tagolatlan = {sz['bdb_id'] for sz in szocikkek if not sz['szakaszok']}
    pontok = collections.OrderedDict()
    for vers, k in vers_pont:
        if k[1] == 'fej' and k[0] in tagolatlan:
            k = (k[0], 'tagolatlan')
        lista = pontok.setdefault(vers, [])
        if k not in lista:
            lista.append(k)
    for vers, lista in pontok.items():
        if len(lista) > 1:
            lista[:] = [k for k in lista if k[1] != 'fej'] or lista
            lista[:] = [k for k in lista if not any(_os_pont(k, m) for m in lista)]
    return pontok


def fan_kivuli_pontok(vers_pont, szocikkek):
    """F33 (F182): [(vers, kulcs)] — a vers → pont párok, amelyek pontja (nem fej, nem a tagolatlan szócikk egésze) nem
    csomópontja a megjelenített fának (`bdb_tagolas.szocikkek`). A kártya ezeket nem nevezi meg pontként."""
    fa = {sz_k for sz in szocikkek for sz_k, _j, _h, _a, _f in sz['szakaszok']}
    return [(v, k) for v, k in vers_pont if k[1] not in ('fej', 'tagolatlan') and k not in fa]


def bdb_olvasoi_reteg(adat, strong, szocikkek, hordozo, vers_pont, nem_idezett, tartomanyban, pont_nelkul, gyenge=None,
                      szotar='BDB', fej_hu=None):
    """Az olvasói réteg bekezdései: a jelentések rendje (hordozó szakasz félkövér) és „A motívum helyein” sor.
    `gyenge`: {(vers, kulcs): [ok]} — a csak bizonytalan okkódú sorral idézett pont (DT-F104e, DT178): a sorban gyenge
    szinten („vonatkozhat”, az okkal) áll, nem az erőssel azonos alakban, és a jelentések rendjében nem félkövér (F29 (e)).
    F29 (b): egy vers egyszer áll; a csak a szócikk fejében idézett hely „a szótár csak alakként idézi”. F29 (c): a szócikk
    neve sorszám és belső azonosító nélkül. F187: `szotar='Thayer'` a görög kártya (glossza a görög szó előtt elvágva; a
    meghatározás nélküli szakasz „csak alakot/párhuzamot közöl”; a fej meghatározása `fej_hu`-ból)."""
    gyenge = gyenge or {}
    thayer = szotar == 'Thayer'
    # F33 (F182): a „A motívum helyein” sor pontja a megjelenített fa csomópontja; a fán kívüli pont (pl. a szakasztábla
    # sorbelső feje, amelyet a fa nem bont külön) nem kap kitalált nevet, a vers a „nem azonosítható” helyek közé kerül
    kint = fan_kivuli_pontok(vers_pont, szocikkek)
    if kint:
        vers_pont = [x for x in vers_pont if x not in kint]
        pont_nelkul = list(pont_nelkul) + [v for v, _k in kint]
    hiv_db = thayer_hivatkozas_szam(adat, strong) if thayer else bdb_hivatkozas_szam(adat, strong)
    glossza = thayer_glossza if thayer else olvasoi_glossza
    lathato = [sz for sz in szocikkek if sz['szakaszok'] or (sz['fej'] and sz['fej'][2])]
    tobb = len(lathato) > 1
    # F29 (e): a csak bizonytalan sorral idézett pont nem félkövér; F29 (b): a helyek sorából kimaradó ős-pont sem
    pontok = helyek_pontjai(vers_pont, szocikkek)
    eros_k = {k for v, lista in pontok.items() for k in lista if not gyenge.get((v, k))}
    felkover = {k for k in hordozo if k in eros_k or not any(kk == k for _v, kk in vers_pont)}
    nevek, sorok, lat = {}, [], set()
    fej_gl = thayer_fej_glossza(fej_hu) if thayer and fej_hu else None
    for i, sz in enumerate(lathato, 1):
        behuz = ''
        szn = _szocikk_olvasoi_nev(adat, strong, sz['bdb_id'], i) if tobb else ''
        if tobb:
            sorok.append('- *%s*' % szn)
            behuz = '  '
        if not sz['szakaszok']:
            # a tagolatlan szócikk (nincs törzs, számozott jelentés, alpont): egy meghatározás a fejből
            gl = thayer_fej_glossza(sz['fej'][2] if sz['fej'] else '') if thayer else fej_glossza(sz['fej'][2] if sz['fej'] else '')
            k = (sz['bdb_id'], 'tagolatlan')
            nevek[k] = 'a szócikk egésze' + (' — %s' % gl if gl else '')
            if tobb:
                nevek[k] = '%s, %s' % (szn, nevek[k])
            if sz['fej'] and sz['fej'][2]:
                hordoz = any(kk[0] == sz['bdb_id'] for _v, kk in vers_pont)
                sorok.append('%s- %s%s' % (behuz, '**a szócikk egésze**' if hordoz else 'a szócikk egésze',
                                           (' (nincs számozott jelentése) — %s' % gl) if gl else ' (nincs számozott jelentése)'))
            continue
        if thayer and fej_gl:
            # a Thayer feje gyakran maga is meghatározás: a számozott jelentések előtt áll
            k = (sz['bdb_id'], 'fej')
            nevek[k] = 'a szócikk eleje — %s' % fej_gl
            hordoz = any(k in lista for lista in pontok.values())
            sorok.append('%s- %s — %s' % (behuz, '**a szócikk eleje**' if hordoz else 'a szócikk eleje', fej_gl))
        for k, jel, hu, _angol, _kat in sz['szakaszok']:
            if k in lat:
                continue        # az azonos útvonalú folytatás-szakasz (Thayer) egyszer áll
            lat.add(k)
            cimke = (adat['cimke'].get((szotar, strong) + k) or {}).get('cimke_hu') or ''
            gl = glossza(jel, cimke, hu)
            csak_alak = None
            if not gl and hu and thayer:
                csak_alak = thayer_csak_alak(hu)
            elif not gl and hu and _ALAKTANI_KEZDET.match(re.sub(r'^\s*(?:\d+\.\s*)+', '', vegyes_cim_nelkul(
                    jel, jelolo_levag(hu, jel)).strip(' —–-'))):
                # az alakjegyzékkel nyíló szakasz (F29 (a): a személyszámmal kezdődő is, „3. hímnemű …”): az alak utáni
                # magyar meghatározás, ennek híján a kimondott tény (DT-F104c 4.)
                gl = alak_utani_glossza(hu)
                if not gl:
                    n = hiv_db.get(k, 0)     # DT-F104d: a táblából, nem a szövegből
                    csak_alak = 'a szótár csak alakot közöl' + (' (%d hely)' % n if n else '')
            elif not gl and not hu and thayer:
                csak_alak = FORDITASRA_VAR
            elv = ' — ' if jel[:1].isalpha() else ' '
            nevek[k] = ('%s%s%s' % (_jel_olvasoi(jel), elv, gl)) if gl else _jel_olvasoi(jel)
            if tobb:
                nevek[k] = '%s, %s' % (szn, nevek[k])
            melyseg = len([x for x in re.split(r'[ .]', jel) if x]) - 1
            # F182 (látható hiba): a sor eleji „2.” jelet a Markdown számozott listának veszi (üres felsorolásjel, beágyazott
            # lista); a nem félkövér jel pontja ezért escape-elve áll („2\.”)
            jel_m = ('**%s**' % _jel_olvasoi(jel)) if k in felkover else re.sub(r'^(\d+)\.(?=\s|$)', r'\1\\.',
                                                                              _jel_olvasoi(jel))
            sorok.append('%s%s- %s%s%s' % (behuz, '  ' * max(0, melyseg), jel_m, ' — ' if (gl and elv == ' — ') or csak_alak else ' ',
                                           gl or csak_alak or '*(külön meghatározás nélkül)*'))
    bek = ['**A jelentések rendje a %s szerint** (félkövér: a motívum helyein álló jelentés)' % szotar, '\n'.join(sorok)]
    # F29 (b): versenként a pontok (fej és ős nélkül), majd az azonos pontú versek egy csoportban; egy vers egyszer áll
    csop, rend = {}, []
    for vers, lista in pontok.items():
        g = tuple((k, tuple(gyenge.get((vers, k), ()))) for k in lista)
        if g not in csop:
            csop[g] = []
            rend.append(g)
        csop[g].append(vers)
    reszek = []
    for g in rend:
        nevsor = []
        for k, okok in g:
            if k[1] == 'fej':
                nev = nevek.get(k) if thayer else None
                nev = nev or CSAK_ALAKKENT
            else:
                nev = nevek.get(k, _jel_olvasoi(szakasz_jel(k[1])))
            nevsor.append(nev + ((' *(vonatkozhat; a hivatkozás bizonytalan: %s)*' % '; '.join(okok)) if okok else ''))
        reszek.append('%s → %s' % (_versek_rovid(csop[g]), '; '.join(nevsor)))
    mondat = '**A motívum helyein:** %s.' % (' · '.join(reszek) if reszek else 'a szótár egyiket sem idézi')
    if nem_idezett:
        mondat += ' A szótár ezt a helyet nem idézi: %s.' % _versek_rovid(nem_idezett)
    if tartomanyban:
        mondat += ' Csak egy verstartomány részeként idézi, jelentésponthoz nem köthető: %s.' % _versek_rovid(tartomanyban)
    pont_nelkul = [v for v in dict.fromkeys(pont_nelkul) if v not in pontok]
    if pont_nelkul:
        mondat += ' A szótár idézi, de a jelentéspont nem azonosítható: %s.' % _versek_rovid(pont_nelkul)
    bek.append(mondat)
    return bek



def _osszecsukva_uj(futam):
    """Az összecsukott szakaszfutam címe glosszával (F10 (2)): „2 — földdarab, földbirtok (1 hely)”, futamnál
    „5 – 7 (3 jelentés): ország · az egész föld · tulajdonnév”; a törzs a cím mellett egy alakban."""
    def hely(n):
        return '%d hivatkozás' % n if n else 'hivatkozás nélkül'
    if len(futam) == 1:
        jel, _k, _vz, gl, n = futam[0]
        cim = '%s — %s (%s)' % (_jel_olvasoi(jel), gl, hely(n)) if gl else '%s (%s)' % (_jel_olvasoi(jel), hely(n))
    else:
        gls = [f[3] for f in futam if f[3]]
        cim = '%s – %s (%d szakasz)%s' % (_jel_olvasoi(futam[0][0]), _jel_olvasoi(futam[-1][0]), len(futam),
                                           (': ' + ' · '.join(gls[:4]) + (' …' if len(gls) > 4 else '')) if gls else '')
    return '<details>\n<summary>%s</summary>\n\n%s\n\n</details>' % (cim, '\n'.join(f[2] for f in futam))


def gerinc_szakasz_lista(szakaszok, hordozo, celok, adat_cimke, szotar, strong, elnyelt=None, uj=False, hiv_db=None,
                        extra=None):
    """A tagolás vázlata: [(kulcs, jel, szöveg_hu vagy None, angol, kategória)] sorrendben, a kulcs (bdb_id, utvonal).
    A hordozó szakaszok kibontva (címke + teljes magyar szöveg, kiemeléssel), a többi összecsukott
    futamokban. `elnyelt`: {kulcs: a szövegét hordozó kulcs} (F123.BDBGER). Visszaad: (bekezdések, kiemelt
    azonosítók, meg nem talált azonosítók). `uj` (F104, az új szerkezetű lap): az összecsukott futam címe glosszával, a
    vázlatsorban a törzsnév egy alakban; a cím hivatkozásszáma `hiv_db`-ből (`bdb_hivatkozas_szam`, DT-F104d)."""
    elnyelt = elnyelt or {}
    hiv_db = hiv_db or {}
    elnyelo = {}
    for k, hova in elnyelt.items():
        elnyelo.setdefault(hova, []).append(k)
    out, futam, talalt_ossz, hiany_ossz = [], [], [], []

    def lezar():
        if futam:
            out.append(_osszecsukva_uj(futam) if uj else _osszecsukva([f[2] for f in futam], futam[0][0], futam[-1][0]))
            del futam[:]

    for k, jel, hu, angol, kat in szakaszok:
        cimke = (adat_cimke.get((szotar, strong) + k) or {}).get('cimke_hu') or ''
        if k not in hordozo:
            vazlat = _vazlat_sor(jel, cimke, hu or angol)
            if uj:
                # F29 (d) nem javítva (F187, N-F187a): a vázlatsor az első tagmondat; a teljes szöveg a kiejtés-szabály
                # hiányát 21-ről 126-ra emelné a HAMART-001-en
                vazlat = '- `%s` — %s' % (jel, vegyes_cim_nelkul(jel, cimke) if cimke else
                                         vegyes_cim_nelkul(jel, _elso_tagmondat(hu or angol, csonkit_jel=True)))
            if kat == 'horgonnyal':
                # ELLENOR_SZOTARI_GERINC 4. (7.2a): a határjelölés az összecsukott szakaszon is látszik
                vazlat += HORGONNYAL_JELOLES
            if k in elnyelo:
                vazlat += ' ' + elnyelo_mondat(elnyelo[k])
            gl = (thayer_glossza if szotar == 'Thayer' else olvasoi_glossza)(jel, cimke, hu) if uj else ''
            if uj and not gl and szotar != 'Thayer':
                gl = gondolatjel_utani_glossza(hu)   # F182 (A17; F10 (2)): a törzs-szakasz glosszája a gondolatjel után
            futam.append((jel, k, vazlat, gl, hiv_db.get(k, 0)) if uj else (jel, k, vazlat))
            continue
        lezar()
        fej = '- **`%s` — %s**' % (jel, cimke) if cimke else '- **`%s`**' % jel
        if uj and not cimke and szotar == 'Thayer':
            # F187: a kibontott Thayer-szakasz címe is glosszás („2.b — elpusztítani”)
            gl = thayer_glossza(jel, '', hu)
            fej = '- **`%s` — %s**' % (jel, gl) if gl else fej
        if hu:
            szoveg, talalt, hiany = kiemel(jelolo_levag(hu, jel), celok.get(k, []), mark=bool(uj), extra=extra)
            talalt_ossz += talalt
            hiany_ossz += hiany
            bek = [fej, '', '  > %s' % szoveg]
            if kat == 'horgonnyal':
                bek.append('  >' + HORGONNYAL_JELOLES)
            if k in elnyelo:
                bek.append('  >')
                bek.append('  > ' + elnyelo_mondat(elnyelo[k]))
        elif k in elnyelt:
            hiany_ossz += [a for _v, a in celok.get(k, [])]
            bek = [fej, '', '  %s' % elnyelt_mondat(elnyelt[k])]
        else:
            hiany_ossz += [a for _v, a in celok.get(k, [])]
            bek = [fej, '', '  > %s' % angol, '', '  %s' % FORDITASRA_VAR]
        out.append('\n'.join(bek))
    lezar()
    return out, talalt_ossz, hiany_ossz


def _szonezet_mutato(strong, forras):
    return '[szónézet: %s](%s) · forrás: `%s`' % (SZONEZET_UT % strong, SZONEZET_UT % strong, forras)


def bdb_gerinc_szocikkek(adat, strong):
    """A Strong BDB-szócikkei a 2.30 (a BDB) sorrendjében: ([{'bdb_id', 'fej', 'szakaszok'}], elnyelt). A fa egyetlen
    helye a `bdb_tagolas.szocikkek` (F33, egy szabály, egy hely: a kártya és az olvasó tagolása a szakasztáblából);
    itt csak a megjelenítés előtti zárójel-javítás (F123.GENKOR, `bdb_forras_javitas.tsv` `zarojel`) és a szakaszjel
    szabálya csatlakozik."""
    return BT.szocikkek(adat['bdb_sz'].get(strong, []), _bdb_hu_strong(adat, strong), szakasz_jel,
                        lambda t: BR.zarojel_javit(t, strong))


def _bdb_hu_strong(adat, strong):
    """{sorszám: a 2.32 sora} egy Strongra (a `gerinc_adat` `bdb_hu` indexéből)."""
    return {r['sorszam']: adat['bdb_hu'][(strong, r['sorszam'])] for r in adat['bdb_sz'].get(strong, [])
            if (strong, r['sorszam']) in adat['bdb_hu']}


def bdb_gerinc_szakaszok(adat, strong):
    """[(kulcs, jel, szöveg_hu, angol, kategória)] a 2.30 sorrendjében, szócikkenként (a fej a szócikk elején)."""
    out = []
    for sz in bdb_gerinc_szocikkek(adat, strong)[0]:
        out.extend(([sz['fej']] if sz['fej'] else []) + sz['szakaszok'])
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
        # F123: a Thayer saját kulcsa az 1000 alatti Strongnál nulla nélküli („G86”), a `forditasok.tsv` `entry_id`-je is
        f = (fidx.get(('Thayer', strong, strong, 'sz%s' % r['sorszam'], 'forditas_hu'))
             or fidx.get(('Thayer', strong, strong[0] + str(int(strong[1:])), 'sz%s' % r['sorszam'], 'forditas_hu')))
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
    # a lektor ajánlása (a felhasználó jóváhagyásával): a szócikkben a motívum minden verse kiemelt (csak az új szerkezet)
    motivum_versek = {v for s in motivum_sorai for v in igehely_lista(s['igehely'])}
    for s in motivum_sorai:
        tokenek = [t for t in (s.get('strong') or '').split('+') if t]
        if strong not in tokenek:
            continue
        versek.extend(igehely_lista(s['igehely']))
        if s.get('lexikon_entry_id') == strong and s.get('lexikon_szotar') == szotar:
            kut_kulcsok.add(kutatoi_kulcs(s.get('jelentes_szam') or '')[0])
    lk = lemma_kiejtes(strong)
    cim = '##### %s%s · %s' % (strong, ' — %s' % lemma_cim(lk) if lk else '', szotar)
    napl = {'strong': strong, 'szotar': szotar, 'kiemelt': [], 'nem_talalt': [], 'nem_idezett': []}
    uj = bool(ctx and ctx.get('bdb_kartya'))
    vers_pont, pont_nelkul = [], []
    # DT-F104e (DT178): a bizonytalan okkódú sor pontja gyenge („vonatkozhat”); ha ugyanannak a helynek és pontnak erős sora is
    # van, az erős marad (a szerver `VersJelolo`-jával egyezően). A szabály: `bdb_vj_szabaly.vj_bizonytalan`.
    eros_pont, gyenge_ok = set(), {}

    def pont(vers, k, r):
        vers_pont.append((vers, k))
        okok = VJ.vj_bizonytalan(r) if szotar == 'BDB' else []
        if okok:
            gyenge_ok.setdefault((vers, k), set()).update(okok)
        else:
            eros_pont.add((vers, k))
    if szotar == 'BDB':
        # F123.BDBGER: szócikkenként (bdb_id), a BDB saját rendjében; a szakasz kulcsa (bdb_id, utvonal)
        szocikkek, elnyelt = bdb_gerinc_szocikkek(adat, strong)
        vj = adat['bdb_vj']
    else:
        szakaszok = [(('', s[0]),) + tuple(s[1:]) for s in thayer_gerinc_szakaszok(adat, strong)]
        szocikkek = [{'bdb_id': '', 'fej': next((s for s in szakaszok if s[0][1] == 'fej'), None),
                      'szakaszok': [s for s in szakaszok if s[0][1] != 'fej']}]
        elnyelt = {}
        vj = adat['th_vj']
    tobb_szocikk = len(szocikkek) > 1
    teljes_ut = {(k[0], gerinc_utvonal_vag(k[1])): k for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
    celok, hordozo = {}, set()
    fej_celok = {}
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
            b, ok = bdb_vers_szocikk(adat, strong, r) if szotar == 'BDB' else ('', '')
            if b is None:
                napl['nem_talalt'].append(azon + ': nem azonosítható, melyik szócikkében (%s)' % ok)
                pont_nelkul.append(vers)
                continue
            if r['utvonal'] == 'fej':
                pont(vers, (b, 'fej'), r)
                hova = elnyelt.get((b, 'fej'), (b, 'fej'))
                if hova[1] == 'fej':
                    fej_celok.setdefault(hova[0], []).append((vers, azon))
                else:
                    celok.setdefault(hova, []).append((vers, azon))
                    hordozo.add(hova)
                continue
            k = teljes_ut.get((b, gerinc_utvonal_vag(r['utvonal'])))
            if k is None:
                if not (uj and r['utvonal'] == 'tagolatlan'):
                    napl['nem_talalt'].append(azon + ': az útvonal nincs a szakasztáblában')
                if r['utvonal'] == 'tagolatlan':
                    pont(vers, (b, 'tagolatlan'), r)       # F104: a tagolatlan szócikk egésze
                else:
                    pont_nelkul.append(vers)
                continue
            pont(vers, k, r)
            # DT381 (a): a forrásjavított sornál a magyar szöveg a forrás alakját hordozza („26:35”): azt emeli ki
            keres = vers
            if 'forras_javitas' in (r.get('okkod') or '').split(',') and re.fullmatch(r'\d+:\d+', r['nyers']):
                keres = '%s %s' % (vers.rsplit(' ', 1)[0], r['nyers'])
            # F123.BDBGER: az elnyelt szakasz szövege a hordozó szakaszban áll: ott emeli ki
            hova = elnyelt.get(k, k)
            if hova[1] == 'fej':
                fej_celok.setdefault(hova[0], []).append((keres, azon))
            else:
                celok.setdefault(hova, []).append((keres, azon))
                hordozo.add(hova)
            hordozo.add(k)
    for kk in kut_kulcsok:
        k = kutatoi_szakasz(adat, szotar, strong, kk)
        if k:
            hordozo.add(k)
    bek = [cim, GERINC_BEVEZETO['Thayer' if szotar == 'Thayer' else 'BDB']]
    if szotar == 'Thayer':
        bek.append('*A magyar szöveg a szakaszonkénti Thayer-fordításból (`adat/forditasok.tsv`, `sz<n>` sorok, #142; '
                   'DT373).*')
    napl['tiltott'] = []
    for sz in szocikkek:
        for k, _jel, hu, _a, forras in ([sz['fej']] if sz['fej'] else []) + sz['szakaszok']:
            for alak in tiltott_talalatok(adat.get('tiltott', []), hu):
                napl['tiltott'].append('%s %s (%s): „%s”' % (szotar, szakasz_kulcs_jel(adat, szotar, strong, k), forras, alak))
    elnyelo = {}
    for k, hova in elnyelt.items():
        elnyelo.setdefault(hova, []).append(k)
    for i, sz in enumerate(szocikkek, 1):
        if tobb_szocikk:
            bek.append('**%s** *(a %s %d. BDB-szócikke a %d-ből)*'
                       % (bdb_szocikk_fejcim(adat, strong, sz['bdb_id']), strong, i, len(szocikkek)))
        fej = sz['fej']
        fc = fej_celok.get(sz['bdb_id'], [])
        if fej and fej[2]:
            szov, t, h = kiemel(fej[2], fc, mark=bool(uj), extra=motivum_versek)
            napl['kiemelt'] += t
            napl['nem_talalt'] += h
            if fej[0] in elnyelo:
                szov += ' ' + elnyelo_mondat(elnyelo[fej[0]])
            bek.append('**A szócikk feje (nyelvi háttér).** %s' % szov)
        elif fej and fej[0] in elnyelt:
            napl['nem_talalt'] += [a for _, a in fc]
            bek.append('**A szócikk feje (nyelvi háttér).** %s' % elnyelt_mondat(elnyelt[fej[0]]))
        elif fej:
            napl['nem_talalt'] += [a for _, a in fc]
            bek.append('**A szócikk feje (nyelvi háttér).** > %s %s' % (fej[3], FORDITASRA_VAR))
        lista, talalt, hiany = gerinc_szakasz_lista(sz['szakaszok'], hordozo, celok, adat['cimke'], szotar, strong,
                                                    elnyelt, uj=uj, extra=motivum_versek,
                                                    hiv_db=(bdb_hivatkozas_szam(adat, strong) if szotar == 'BDB' else
                                                            thayer_hivatkozas_szam(adat, strong)) if uj else None)
        napl['kiemelt'] += talalt
        napl['nem_talalt'] += hiany
        bek.extend(lista)
    if szotar == 'BDB':
        betu = bdb_betu_javit_aktiv((ctx or {}).get('id'))
        bek[2:] = [bdb_rovidites_jelol(b, strong, betu) for b in bek[2:]]
        if uj:
            # F182 (F32): a kutatói rétegben (az apparátusban) a BDB magyar szövegének hivatkozásai Károli-számozással, az
            # eredeti (héber) szám jelölésével; az olvasói réteg „A motívum helyein” sora eleve Károli-vers
            # (itt a `bek[2:]` még csak a kutatói tartalom; az olvasói réteg lent, külön épül)
            terkep = bdb_karoli_terkep(adat, strong)
            kv = karoli_versek()
            bek[2:] = [karoli_szamozas(b, terkep, kv) for b in bek[2:]]
    napl['elnyelt'] = ['%s → %s' % (' '.join(k), ' '.join(v)) for k, v in sorted(elnyelt.items())]
    if napl['nem_talalt'] or napl['nem_idezett'] or napl['tiltott'] or napl['tartomanyban'] or napl['elnyelt']:
        reszek = []
        if napl['elnyelt']:
            # F123.BDBGER (N-F123ga): a 2.32 jelölő nélküli sora szócikkhatáron át az előző sor szövegében áll
            reszek.append('a magyar szöveg szócikkhatáron át az előző sorban áll (`%s`, jelölő nélküli sor): %s'
                          % (BDB_SZAKASZ_HU_FAJL, '; '.join(napl['elnyelt']) if not uj else '; '.join(
                              '%s → %s' % (bdb_kulcs_olvashato(k), bdb_kulcs_olvashato(v)) for k, v in sorted(elnyelt.items()))))
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
    if uj:
        # F104 (DT-F104b): a szótári tagolás bevezetője szótáranként egyszer, a 4.2 elején (az első szó előtt); a BDB-nél
        # két réteg: az olvasói (a jelentések rendje, a motívum helyei) és a csukott kutatói apparátus
        elso = szotar not in ctx.setdefault('gerinc_bevezeto', set())
        ctx['gerinc_bevezeto'].add(szotar)
        bev = [UJ_GERINC_BEVEZETO.get(szotar, bek[1])] if elso else []
        # F187: a Thayer-kártya ugyanígy két rétegű (ugyanaz a kapcsoló, jelölő és kapu)
        tart = [t.split(': ', 1)[0] for t in napl['tartomanyban']]
        gyenge = {p: sorted(o) for p, o in gyenge_ok.items() if p not in eros_pont}
        fej0 = szocikkek[0]['fej'] if szocikkek else None
        olv = bdb_olvasoi_reteg(adat, strong, szocikkek, hordozo, vers_pont, napl['nem_idezett'], tart, pont_nelkul,
                                gyenge, szotar=szotar, fej_hu=(fej0[2] if fej0 and szotar == 'Thayer' else None))
        # N-F187b (orkesztrátori döntés): az apparátusban a BDB-azonosító olvasható forrás-hivatkozásként áll
        bek = bev + [bek[0]] + olv + [APPARATUS_KEZDET % strong, '<details>\n<summary>%s</summary>' % APPARATUS_CIM] + \
            [bdb_azonosito_olvashato(b) for b in bek[2:]] + ['</details>', APPARATUS_VEGE % strong]
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


# A BDB egybetűs rövidítései (a felhasználó, 2026-10-29): a jelölő a közös `bdb_rovidites.py`-ban (N-F131x), amelyet az
# olvasó-szerver szó-lapja is hív; itt a címszó (lemma + kiejtés a kiejtés-szabály szerint) kerül mellé.
BDB_ROVIDITES_RE = BR.ROVIDITES_RE
BDB_JAHVE_CIM = BR.JAHVE_CIM
BDB_ROVIDITES_ALTALANOS = BR.ALTALANOS


# A BETŰJAVÍTÁS KAPCSOLÓJA (F185, DT-F185f, orkesztrátori döntés, 2026-11-10): a 2.31 pe/mem és rés/dálet javításait
# (`bdb_rovidites.betu_javit`) a lexikon-generátor csak bekapcsolt állapotban alkalmazza; ma ki van kapcsolva, így minden lap
# bájtra a korábbi alakjában generálódik (E28). Tömeges újragenerálás nincs: a #182 kapcsolja be, a lapok motívumonként, a
# teljes folyamatban kapják meg (az F35 mellé). Az olvasó (`olvaso_szerver/blokkok.py`) a javítást mindig alkalmazza.
# A kapcsoló egyetlen helye ez.
# F182 (2. fázis, F25): motívumhalmaz, a `KETRETEGU_BDB_KARTYA` mintájára; a HAMART-001 az F33 után kapcsolva be.
BDB_BETU_JAVIT = frozenset({'HAMART-001'})


def bdb_betu_javit_aktiv(motivum_id):
    return bool(motivum_id) and motivum_id in BDB_BETU_JAVIT


# F182 (F32): a szótári szöveg versszámozása (a BDB a héber MT-t követi) a megjelenítésben Károli-számozásra vált, az eredeti
# szám jelölésével („2Móz 22:28 (héber számozás: 22:27)”). A térkép a 2.29 átkulcsolt soraiból (`vers_feloldas` =
# `atkulcsolt*`, `mt_vers` ≠ `karoli_vers`); a forrás szövege nem változik. A könyv és a fejezet a folytatólagos hivatkozásra
# öröklődik („5Móz 29:11, 13” — a 13 is 5Móz 29).
KAROLI_SZAM_JEL = ' (héber számozás: %s)'
_HIV_TOK = re.compile(r'(?P<k>(?<![\w])(?:[1-5])?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6})\s(?P<c>\d{1,3}):(?P<v>\d{1,3})(?![\d:])'
                      r'|(?<![\w:.])(?P<c2>\d{1,3}):(?P<v2>\d{1,3})(?![\d:])'
                      r'|(?<=, )(?P<v3>\d{1,3})(?![\d:])')


def bdb_karoli_terkep(adat, strong):
    """{(könyv, fejezet, vers) az MT szerint: (fejezet, vers) a Károliban} a Strong 2.29-soraiból (csak az átkulcsolt sorok)."""
    ki = {}
    for sorok in adat['bdb_vj'].values():
        for r in sorok:
            if r['strong'] != strong or not (r.get('vers_feloldas') or '').startswith('atkulcsolt'):
                continue
            m1 = re.match(r'^(.+) (\d+):(\d+)$', r.get('mt_vers') or '')
            m2 = re.match(r'^(.+) (\d+):(\d+)$', r.get('karoli_vers') or '')
            if m1 and m2 and m1.group(1) == m2.group(1) and m1.groups() != m2.groups():
                ki[(m1.group(1), m1.group(2), m1.group(3))] = (m2.group(2), m2.group(3))
    return ki


NINCS_KAROLI_JEL = ' *(a Károliban nincs ilyen vers: a szótár hivatkozása)*'


def szotari_hivatkozasok(szoveg):
    """[(match, könyv, fejezet, vers)] a szöveg hivatkozásai a könyv és a fejezet öröklésével (a BDB szokása: „5Móz 29:11, 13;
    30:1”). Egy hely: a Károli-számozás (`karoli_szamozas`) és az `ellenoriz.py` 43. szabálya is ezt használja."""
    ki, konyv, fej, elozo_veg = [], None, None, -10
    for m in _HIV_TOK.finditer(szoveg):
        if m.group('k'):
            konyv, fej, vers = m.group('k'), m.group('c'), m.group('v')
        elif m.group('c2'):
            if konyv is None:
                elozo_veg = m.end()
                fej = m.group('c2')
                continue
            fej, vers = m.group('c2'), m.group('v2')
        else:
            if konyv is None or fej is None or m.start() - elozo_veg != 2:
                continue
            vers = m.group('v3')
        elozo_veg = m.end()
        ki.append((m, konyv, fej, vers))
    return ki


_karoli_versek_cache = None


def karoli_versek():
    """{'versek': {„1Móz 3:17”, …}, 'konyvek': {…}} a Károli-szövegből (`konkordancia/Karoli_1908.tsv`)."""
    global _karoli_versek_cache
    if _karoli_versek_cache is None:
        v = set()
        with io.open(os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
            for sor in f:
                c = sor.split('\t', 1)[0]
                if re.match(r'^\S+ \d+:\d+$', c):
                    v.add(c)
        _karoli_versek_cache = {'versek': v, 'konyvek': {x.rsplit(' ', 1)[0] for x in v}}
    return _karoli_versek_cache


def karoli_szamozas(szoveg, terkep, versek=None):
    """A szöveg hivatkozásai a `terkep` szerint Károli-számozással, az eredeti szám jelölésével (csak megjelenítés). A
    Károliban nem létező versre mutató hivatkozás (ha `versek` adott) átirányítás nélkül, gyenge jelöléssel áll
    (orkesztrátori keret, 2026-11-11: hamis átirányítás nem kerülhet a lapra)."""
    if not terkep and not versek:
        return szoveg
    ki, poz = [], 0
    for m, konyv, fej, vers in szotari_hivatkozasok(szoveg):
        cel = (terkep or {}).get((konyv, fej, vers))
        if not cel:
            if (versek and konyv in versek['konyvek'] and '%s %s:%s' % (konyv, fej, vers) not in versek['versek']):
                ki.append(szoveg[poz:m.end()] + NINCS_KAROLI_JEL)
                poz = m.end()
            continue
        eredeti = '%s:%s' % (fej, vers)
        if m.group('k'):
            uj = '%s %s:%s' % (konyv, cel[0], cel[1])
        elif m.group('c2') or cel[0] != fej:
            uj = '%s:%s' % cel
        else:
            uj = cel[1]
        ki.append(szoveg[poz:m.start()] + uj + KAROLI_SZAM_JEL % eredeti)
        poz = m.end()
    return ''.join(ki) + szoveg[poz:]


def bdb_rovidites_jelol(szoveg, strong, betu=False):
    """A BDB-szöveg megjelenítése (`bdb_rovidites`, DT-F131z): a torz átírás javítása (B3; a magyar bekezdésben a magyar
    alak, a „fordításra vár” jelű angol bekezdésben a helyreállított átírás), a Biblia által igazolt héber sorrend-javítás,
    a futam utáni szám izolálása (LRM), majd az egybetűs rövidítések: „׳י” / „י׳” → `<abbr class="rovidites" title="…">י׳</abbr>`."""
    lk = lemma_kiejtes(strong)
    szoveg = BR.atiras_javit(szoveg, strong, magyar=FORDITASRA_VAR not in szoveg)
    szoveg = BR.izolal(BR.heber_sorrend_javit(szoveg, strong, betu=betu))
    return BR.jelol(szoveg, lemma_cim(lk) if lk else '', BR.alapbetu(lk[0]) if lk else '')


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


def _gerinc_szocikk(nyelv, n, tokenek_ny, reszek, ctx):
    """A 2. szerep („Mélységi szócikk”) a gerinc-lapon: a szótári gerinc (a jelentéstartomány a Thayer, ill. a BDB
    tagolásában) maga, saját címsor és mutató nélkül (ISTENTISZT-001 arany lap, 2026-10-29: a DT371 1. helye módosítva —
    a gerinc és a 2. szerep egy hely)."""
    adat = gerinc_adat()
    szotar = 'Thayer' if nyelv == 'gorog' else 'BDB'
    bek = []
    for t in tokenek_ny:
        b, _n = gerinc_blokk(adat, szotar, t, ctx.get('sorai') or [], ctx)
        bek.extend(b)
        if nyelv == 'gorog':
            bek.append(ubs_domensor(t))
            ctx['fl'].setdefault(UBS_DNTG_JELENTESEK_FAJL, set()).add('UBS_DNTG')
    return bek


# A szerepmátrix szűkítése az arany lapon (DT371 1.; (i) az SDBH-doménsor marad; (ii) a BDB-fej a
# gerincben — a 2. szerepben; (iv) a TBESH helyén mutató + egysoros magyar jelentés). A többi szerep változatlan.

def _gerinc_bdb_fej_mutato(nyelv, n, tokenek_ny, reszek, ctx):
    return ['*Hivatkozás: a BDB-szócikk feje (nyelvi háttér) a 2. szerepben („Mélységi szócikk”) áll, szavanként „A szócikk '
            'feje (nyelvi háttér)” címmel (DT371).*']


# A BDB-fejben a rokon nyelvi adat megnevezései (a magyar fordítás szóalakjai), a rövid nyelvi háttérhez.
BDB_ROKON_NYELVEK = ('késői héber', 'föníciai', 'moábita', 'ugariti', 'asszír', 'akkád', 'arab', 'szabeus', 'etióp',
                     'óarámi', 'arámi', 'nabateus', 'palmürai', 'szír', 'mandeus', 'egyiptomi')


def bdb_fej_rovid(hu):
    """(alapjelentés, gyök, [rokon nyelvek]) a BDB-szócikk magyar fejéből: az alapjelentés az első zárójel előtti
    utolsó „: ” utáni rész, a gyök a „√” utáni megjegyzés, a rokon nyelvek a megnevezések sorrendjében."""
    eleje = hu.split('(')[0]
    alap = eleje.split(': ')[-1].strip(' ;,—') if ': ' in eleje else ''
    # a „; —” utáni alakjegyzék (pl. „— ׳ח 1Móz 25:6 és máshol”) nem az alapjelentés része (N-F123l)
    alap = alap.split('; —')[0].strip(' ;,—')
    gy = re.search(r'√\s*([^;,()]+)', hu)  # a nyitó zárójelnél is megáll (nyitva maradt zárójel: HAMART-001, H0127)
    nyelvek = []
    for m in re.finditer(r'(?<![\wáéíóöőúüű])(%s)(?![\wáéíóöőúüű])' % '|'.join(BDB_ROKON_NYELVEK), hu):
        cimke = m.group(1)
        utana = hu[m.end():m.end() + 40].split(';')[0]
        if 'kétséges' in utana or '?' in utana:
            cimke += ' (kétséges)'
        if cimke not in nyelvek and m.group(1) not in nyelvek:
            nyelvek.append(cimke)
    return alap, (gy.group(1).strip() if gy else ''), nyelvek


def _gerinc_bdb_fej_rovid(nyelv, n, tokenek_ny, reszek, ctx):
    """Héber 8. szerep a gerinc-lapon: a BDB-szócikk fejének rövid formája szavanként (alapjelentés, gyök, rokon
    nyelvek); a teljes fej a 2. szerepben (ISTENTISZT-001 arany lap, 2026-10-29). Ahol nincs magyar fej, a mutató."""
    adat = gerinc_adat()
    out = []
    for t in tokenek_ny:
        # F123.BDBGER: a Strong első BDB-szócikkének feje (több szócikknél a többi a 2. szerepben, szócikkenként)
        szocikkek = bdb_gerinc_szocikkek(adat, t)[0]
        fej = szocikkek[0]['fej'] if szocikkek else None
        if not fej or not fej[2]:
            out.append('**%s** · a BDB-szócikk feje magyarul nem áll rendelkezésre; a forrásszöveg a 2. szerepben.' % t)
            continue
        alap, gyok, nyelvek = bdb_fej_rovid(fej[2])
        if uj_szerkezet(ctx.get('id')):
            # F182 (A15; F13): alapjelentés (a nyelvtani alakok nélkül) és gyök; a rokon nyelvi sorok a pont végén, a
            # táblában (a 4.11-ből áthelyezve), a teljes szócikkfej a 4.2-ben — egyszer kimondva, nem szavanként
            alap = re.split(r'\s+—\s+', alap)[0].strip(' ;,')
            r_t = []
            if alap:
                r_t.append('alapjelentés: %s' % bdb_rovidites_jelol(alap, t, bdb_betu_javit_aktiv(ctx.get('id'))))
            else:
                rj, van = rovid_jelentes(t)
                if van:
                    r_t.append('alapjelentés: %s *(a STEPBible rövid szótára szerint)*' % rj)
            if gyok:
                r_t.append('gyök (√): %s' % gyok)
            out.append('**%s** · %s' % (_szo_irassal(t), ' · '.join(r_t) or EM_DASH))
            continue
        reszek_t = []
        if alap:
            reszek_t.append('alapjelentés: %s' % bdb_rovidites_jelol(alap, t, bdb_betu_javit_aktiv(ctx.get('id'))))
        else:
            # a BDB-fej nem mondja ki az alapjelentést (pl. H7585): a TBESH rövid magyar jelentése, jelölve
            rj, van = rovid_jelentes(t)
            if van:
                reszek_t.append('alapjelentés: %s *(a TBESH rövid jelentése; a BDB-fej nem mondja ki)*' % rj)
        if gyok:
            reszek_t.append('gyök (√): %s' % gyok)
        if nyelvek:
            reszek_t.append('rokon nyelvi adat: %s' % ', '.join(nyelvek))
        out.append('**%s** · %s — a teljes szócikkfej a 2. szerepben („A szócikk feje (nyelvi háttér)”).'
                   % (szo_cim(t), ' · '.join(reszek_t) or EM_DASH))
    return out


def szo_cim(t):
    """„H7121 — קָרָא (kárá)”: a Strong, a lemma és a magyaros kiejtés (héberül csak a jóváhagyott; ha nincs, kiejtés
    nélkül, l. kiejtes_hiany)."""
    lk = lemma_kiejtes_szabaly(t)
    if not lk:
        return t
    return '%s — %s%s' % (t, lk[0], ' (%s)' % lk[1] if lk[1] else '')


def _ubs_oszlop_szamlalo(t, ctx, helyekkel=False):
    """(sorok száma, hozzárendelt sorok száma) a token testamentumának soraiban: az 1. szakasz UBS-oszlopa a tokenre
    (görögül az UBS DNTG, héberül a gerinc-lapon az UBS DBH; F131, DT380). `helyekkel` (F182, A16): a nem egyértelmű
    (nem egy jelentésű) helyek igehelyei is."""
    sorai = ctx.get('sorai') or []
    n = h = j = 0
    nem_egy = []
    for s in sorai:
        tok = [x for x in (s.get('strong') or '').split('+') if x]
        if t not in tok:
            continue
        osz = G.konyv_teszamentum(G.konyv_token(s['igehely'])) == 'ÓSZ'
        if osz != t.startswith('H'):
            continue
        n += 1
        cella = (dbh_jelentes_cella(s['igehely'], s.get('strong') or '') if osz
                 else ubs_jelentes_cella(s['id'], s['igehely'], s.get('strong') or ''))
        resz = next((r for r in cella.split(' · ') if r.startswith(t + ':')), cella if len(tok) == 1 else '')
        if '[ⓘ]' in resz:
            if 'nem egyértelmű' in resz or resz.count('[ⓘ]') > 1:
                j += 1  # jelölt, vagy több jelentéskód a cellában (ELLENOR_ISTENTISZT_OLVASOI_2 6.)
                nem_egy.append(s['igehely'])
            else:
                h += 1
        else:
            nem_egy.append(s['igehely'])
    return (n, h, j, nem_egy) if helyekkel else (n, h, j)


def _tartalom_ubs_oszlop(nyelv, n, tokenek_ny, reszek, ctx):
    """9. szerep (Versenkénti jelentés), ahol az 1. szakasz táblázatának UBS-oszlopa a tokent hordozza: szavanként egy
    mondat a sorszámmal és a szónézet linkje (ISTENTISZT-001 arany lap, 2026-10-29)."""
    tesz = 'ószövetségi' if nyelv == 'heber' else 'újszövetségi'
    forras = UBS_DBH_JELENTESEK_FAJL if nyelv == 'heber' else UBS_DNTG_JELENTESEK_FAJL
    out = []
    for t in tokenek_ny:
        sz, h, j = _ubs_oszlop_szamlalo(t, ctx)
        if not sz:
            out.append('**%s** · a motívumnak nincs %s helye ezzel a szóval.' % (t, tesz))
            continue
        out.append('**%s** · a motívum %d %s helyén a vers-szintű jelentést az [1. Előfordulások](#1-előfordulások) '
                   'táblázatának „UBS-jelentés” oszlopa mutatja (%s); a szó teljes versenkénti listája a szónézetben: %s.'
                   % (szo_cim(t), sz, tesz,
                      szam_osszegzes([('helyen egy jelentés', h), ('helyen több vagy jelölt, nem egyértelmű jelentés', j),
                                      ('helyen nincs hozzárendelés', sz - h - j)]),
                      _szonezet_mutato(t, forras)))
    return out


SZEREP_EPITO[('gorog', 9)] = _tartalom_ubs_oszlop


def _gerinc_tbesh(nyelv, n, tokenek_ny, reszek, ctx):
    adat = gerinc_adat()
    out = []
    if uj_szerkezet(ctx.get('id')):
        # a felhasználó átnézése (4.): „**אָבַל (ával)** — gyászolni · H0056 · [szónézet]”; a forrás és a „TBESH rövid
        # jelentése” egyszer, a bevezetőben (`UJ_OLVASOI_SZEREP`)
        for t in tokenek_ny:
            g = adat['glossza'].get(t)
            out.append('**%s** — %s · %s · [szónézet](%s)' % (
                _szo_irassal(t), g['glossza_hu'] if g else 'a szótár nem ad magyar rövid jelentést', t, SZONEZET_UT % t))
        ctx['fl'].setdefault(GLOSSZAK_HEBER_HU_FAJL, set()).add('TBESH')
        return out
    for t in tokenek_ny:
        g = adat['glossza'].get(t)
        rovid = ('%s *(a TBESH rövid jelentése magyarul)*' % g['glossza_hu']
                 if g else '*(nincs magyar rövid jelentés)*')
        out.append('**%s** · %s · a teljes TBESH-szócikk: %s' % (t, rovid, _szonezet_mutato(t, TBESH_TXT_FAJL)))
    ctx['fl'].setdefault(GLOSSZAK_HEBER_HU_FAJL, set()).add('TBESH')
    return out


def _gerinc_tw(nyelv, n, tokenek_ny, reszek, ctx):
    _sorok, idx = tw_szocikkek()
    out = []
    uj = uj_szerkezet(ctx.get('id'))
    for t in tokenek_ny:
        if nyelv == 'heber' and not uj:
            out.append('**%s** · %s' % (t, reszek[t]['twot']))
        cikkek = idx.get(t, [])
        if uj:
            # F182 (A11; F6 és pontosítása): szavanként egy sor, írással és kiejtéssel; a tW-cím magyarul, az azonosító
            # nélkül, a szónézet link; a TWOT száma ugyanabban a sorban; a forrás egyszer, a pont végén
            # a felhasználó átnézése (7.): a sorban a szó, a címek, a TWOT-szám és a szónézet; a felirat és a
            # TWOT-magyarázat egyszer, a bevezetőben (`UJ_OLVASOI_SZEREP`)
            reszek_t = []
            if cikkek:
                reszek_t.append(' · '.join('*%s*' % tw_cim_magyar(c) for c in cikkek))
                ctx['fl'].setdefault(TW_FAJL, set()).add('tW_szocikkek')
            else:
                reszek_t.append('a translationWords nem tárgyalja')
            if nyelv == 'heber':
                reszek_t.append(reszek[t]['twot'].replace('**TWOT:**', 'TWOT').replace('TWOT:', 'TWOT'))
            out.append('**%s** — %s · [szónézet](%s)' % (_szo_irassal(t), ' · '.join(reszek_t), SZONEZET_UT % t))
            continue
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


# A 13–14. szerep (Károli-megfelelők, Rejtett / hamis párhuzam) a motívumonként jóváhagyott lapokon épül (a gerinc-lista
# mintájára): a többi gerinc-lapon a `javaslat` üres blokk marad, amíg a motívumra nincs döntés (DONTESEK, B5).
SZEREP_KAROLI_MOTIVUMOK = SZK.kapcsolo_motivumok('KAROLI_MEGFELELOK')  # adat: `adat/funkcio_kapcsolok.tsv`


def _gerinc_karoli(nyelv, n, tokenek_ny, reszek, ctx):
    """A 13. (Károli-megfelelők) és a 14. (Rejtett / hamis párhuzam) nyelvfüggetlen szerep az arany lapon
    (ISTENTISZT-001 arany lap, 2026-10-29): az általános építő az `eszkozok/szerep_karoli.py`-ban; itt csak a motívum
    engedélyezése (`SZEREP_KAROLI_MOTIVUMOK`) és a forrás- és licencnyilvántartás."""
    sorai = ctx.get('sorai') or []
    if not sorai or sorai[0].get('id') not in SZEREP_KAROLI_MOTIVUMOK:
        return []
    uj = uj_szerkezet(sorai[0].get('id'))
    out = (SZK.blokk_13(sorai, G.TS, csalad=uj) if n == 13 else
           SZK.blokk_14(sorai, G.TS, szo_nev=_szo_irassal if uj else _szo_kiejtessel, tomor=uj, kulcs_nev=_kombo_nev))
    if out:
        ctx['fl'].setdefault('adat/elofordulasok.tsv', set()).add('projekt_adat')
        ctx['fl'].setdefault('adat/szoto/karoli_szotari_alak.tsv', set()).add('projekt_adat')
        if n == 14:
            ctx['fl'].setdefault('konkordancia/Karoli_1908.tsv', set()).add('Karoli_1908')
            ctx['fl'].setdefault(TAHOT_KIVONAT_FAJL, set()).add('TAHOT')
            ctx['fl'].setdefault('konkordancia/TAGNT_kivonat.tsv', set()).add('TAGNT')
            ctx['fl'].setdefault('adat/karoli_strong', set()).add('projekt_adat')
            ctx['fl'].setdefault('adat/jeloltek.tsv', set()).add('projekt_adat')
    return out


def _gerinc_nave(nyelv, n, tokenek_ny, reszek, ctx):
    """A 12. nyelvfüggetlen szerep (Tematikus index, Nave) az arany lapon (ISTENTISZT-001 arany lap, 2026-10-29): az
    általános jelöltképzés és választás az `eszkozok/szerep_nave.py`-ban; itt csak a forrás- és licencnyilvántartás. A
    blokk csak akkor épül, ha a motívumnak van döntése az `adat/tematikus_temak.tsv`-ben (a halmaz a felhasználóé, B5);
    különben a `javaslat` üres blokk marad."""
    sorai = ctx.get('sorai') or []
    if not sorai or not SZN.tema_dontesek(sorai[0].get('id')):
        return []
    out = SZN.blokk_12(sorai, G.TS)
    if out:
        ctx['fl'].setdefault('konkordancia/Nave_basokant.tsv', set()).add('Nave_basokant')
        ctx['fl'].setdefault('adat/elofordulasok.tsv', set()).add('projekt_adat')
        ctx['fl'].setdefault('adat/tematikus_temak.tsv', set()).add('projekt_adat')
        ctx['fl'].setdefault('adat/nave_tema_hu.tsv', set()).add('projekt_adat')
    return out


# a gerinc-építő tartalma a szerep teljes tartalma: a `javaslat` állapotú szerep alá nem kerül általános üres blokk
GERINC_TELJES = frozenset({('gorog', 12), ('gorog', 13), ('gorog', 14)})

GERINC_SZEREP_EPITO = {
    ('gorog', 12): _gerinc_nave,
    ('gorog', 13): _gerinc_karoli,
    ('gorog', 14): _gerinc_karoli,
    ('gorog', 2): _gerinc_szocikk,
    ('heber', 2): _gerinc_szocikk,
    ('heber', 8): _gerinc_bdb_fej_rovid,
    ('heber', 1): _gerinc_tbesh,
    ('gorog', 3): _gerinc_tw,
    ('heber', 3): _gerinc_tw,
    ('gorog', 5): _gerinc_ubs_mutato,
    ('heber', 5): _gerinc_ubs_mutato,
    ('heber', 9): _tartalom_ubs_oszlop,
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
        kiejtes = gorog_magyaros(gepi_atiras(r['lemma']))  # DT430 kiegészítés: a kiejtés jelölés nélkül
    return '%s (%s, %s%s)' % (r['szoalak'], r['lemma'], kiejtes, ' %s' % strong if strong else '')


LXX_SZAMLALO_KULCSOK = ('egyező', 'eltérő', 'LXX-minusz', 'kutatói azonosítás függőben', 'szamozas_elteres', 'szocsalad',
                        'nincs_par')
# Az olvasói összegzés címkéi (ISTENTISZT-001 arany lap, 2026-10-29): a nulla értékű tag elmarad.
LXX_OLVASOI_CIMKE = {'egyező': 'egyező', 'eltérő': 'eltérő', 'LXX-minusz': 'görögből hiányzik',
                     'kutatói azonosítás függőben': 'azonosításra vár',
                     'szamozas_elteres': 'versszámozás miatt nem párosítva', 'szocsalad': 'ugyanaz a szócsalád',
                     'nincs_par': 'nincs újszövetségi pár'}


def lxx_olvasoi(szamlalo, tokenek, uj=False):
    """A 3. szakasz és a 6. szerep olvasói szövege (lelet + következtetés, OK.lxx). `uj` (F182, A20): versben mérve."""
    g = [t for t in tokenek if t.startswith('G')]
    if uj and g:
        # a lektor és a Fable közös véleménye (1.): a szóhíd azokon a szavakon át, amelyeknek van újszövetségi párja; a
        # „nincs megállapítva” és a „nem párosítva” külön áll (2.)
        par = lxx_par_tokenek(tokenek)
        return OK.lxx_hid(sum(szamlalo.values()), szamlalo.get('egyező', 0), szamlalo.get('szocsalad', 0),
                          szamlalo.get('eltérő', 0), szamlalo.get('nincs_par', 0),
                          szamlalo.get('kutatói azonosítás függőben', 0), szamlalo.get('szamozas_elteres', 0),
                          szamlalo.get('LXX-minusz', 0),
                          [_szo_irassal_nevelovel(t) for t in tokenek if t in par])
    return OK.lxx(sum(szamlalo.values()), szamlalo.get('egyező', 0), szamlalo.get('eltérő', 0),
                  szamlalo.get('LXX-minusz', 0),
                  szamlalo.get('kutatói azonosítás függőben', 0) + szamlalo.get('szamozas_elteres', 0),
                  _szo_nev(g[0]) if len(g) == 1 else '', nincs_gorog=not g)


def lxx_olvasoi_osszegzes(szamlalo):
    """„egyező 19 · eltérő 3 · görögből hiányzik 1” — a nulla tagok nélkül; üres számlálónál EM_DASH."""
    reszek = ['%s %d' % (LXX_OLVASOI_CIMKE[k], szamlalo.get(k, 0)) for k in LXX_SZAMLALO_KULCSOK if szamlalo.get(k)]
    return ' · '.join(reszek) if reszek else EM_DASH


def lxx_osszevetes(sorai, tokenek):
    """A 3. szakasz versenkénti összevetése: (táblázat-sorok fejléc nélkül, számláló, forrásfájlok, héber
    tokenenkénti számláló). Ugyanezt olvassa a 6. szerep összegzése (ISTENTISZT-001 arany lap, 2026-10-29)."""
    osz_sorai = [s for s in sorai if G.konyv_teszamentum(G.konyv_token(s['igehely'])) == 'ÓSZ']
    gorog_tokenek = {t for t in tokenek if t.startswith('G')}
    terkep = karoli_to_primary_slug()
    dontesek_idx = lxx_dontesek_index()

    tabla_sorok = []
    szamlalo = dict.fromkeys(LXX_SZAMLALO_KULCSOK, 0)
    heber_szamlalo = {}
    forras_fajlok = set()

    # F12 (TEREMT-002, összetett sor): ha egy héber tokennek saját döntéssora van, a tokenenkénti számláló azt
    # használja (a nem megjelenő bizonyosságú sor „függőben”); saját sor nélkül a vers verdiktje (a korábbi viselkedés).
    sajat_dontes = {(r['igehely'], (r.get('heber_strong') or '').strip()) for r in G.tsv_beolvas(LXX_DONTESEK_TSV)[1]}
    szamolt = []   # (vers, a sor héber szavai, a sor ítélete), a tábla soraival egy sorrendben
    vh_idx = vh_lxx_index(sorai[0]['id']) if sorai and uj_szerkezet(sorai[0]['id']) else None   # F182 (A19)

    def token_verdikt(vers, ht, kulcs):
        if kulcs not in ('eltérő', 'LXX-minusz', 'kutatói azonosítás függőben') or (vers, ht) not in sajat_dontes:
            return kulcs
        r = next((x for x in dontesek_idx.get(vers, []) if (x.get('heber_strong') or '').strip() == ht), None)
        if r is None:
            return 'kutatói azonosítás függőben'
        return 'LXX-minusz' if (r.get('tipus') or '').strip() == 'lxx_minusz' else 'eltérő'

    for s in osz_sorai:
        strong_field = s.get('strong') or ''
        heber_tokenek = [t.strip() for t in strong_field.split('+') if t.strip().startswith('H')]

        def szamol(kulcs):
            szamolt.append((vers, tuple(heber_tokenek), kulcs))
            szamlalo[kulcs] += 1
            for ht in heber_tokenek:
                hsz = heber_szamlalo.setdefault(ht, dict.fromkeys(LXX_SZAMLALO_KULCSOK, 0))
                hsz[token_verdikt(vers, ht, kulcs)] += 1

        for vers in igehely_lista(s['igehely']):
            konyv, karoli_fej, karoli_vers = L.parse_igehely(vers)
            slug = terkep.get(konyv)
            heber_kulcsszo = EM_DASH
            for ht in heber_tokenek:
                talalat = kiejtes_ehhez(vers, ht)
                if talalat:
                    heber_kulcsszo = ragozott_kiejtessel(*talalat)
                    break

            if slug is None:
                tabla_sorok.append('| %s | %s | %s | %s | %s | %s |' % (
                    vers, EM_DASH, heber_kulcsszo, EM_DASH, 'nincs Septuaginta-könyv', EM_DASH))
                continue
            forras_fajlok.add('konkordancia/LXX_OS/%s.tsv' % slug)

            sorai_ehhez_vershez = lxx_os_karoli_index(slug).get(vers, [])
            if not sorai_ehhez_vershez:
                szamol('szamozas_elteres')
                tabla_sorok.append('| %s | %s | %s | %s | %s | Septuaginta |' % (
                    vers, EM_DASH, heber_kulcsszo, EM_DASH, 'szamozas_elteres'))
                continue

            lxx_igehely = lxx_igehely_magyar(sorai_ehhez_vershez[0].get('igehely_lxx'), konyv, karoli_fej, karoli_vers)

            egyezo = [r for r in sorai_ehhez_vershez
                      if gorog_tokenek and lxx_os_strong_normalizalt(r.get('strong')) in gorog_tokenek]
            if egyezo and vh_idx is not None:
                # F182 javítókör (ELLENOR_F182 #4): az egyező görög szó csak a sor héber kulcsszavának saját LXX-megfelelője
                # lehet (a 4.11 párja), nem a vers bármely motívumszava (1Móz 3:17: adámá ↔ γῆ, nem ἐπικατάρατος)
                sajat_par = {_nfc_ekezet_nelkul(vh_idx[(vers, ht)][0]) for ht in heber_tokenek if (vers, ht) in vh_idx}
                if sajat_par:
                    egyezo = [r for r in egyezo if _nfc_ekezet_nelkul(r.get('lemma') or '') in sajat_par]
            if egyezo:
                szamol('egyező')
                gm = gorog_megfelelo_szoveg(egyezo[0])
                if vh_idx is not None:
                    # F182 (A19): a héber kulcsszó az a lánc-szó, amelynek a 4.11 szerinti megfelelője ez a görög szó
                    gl = _nfc_ekezet_nelkul(egyezo[0].get('lemma') or '')
                    ht_par = next((ht for ht in heber_tokenek
                                   if _nfc_ekezet_nelkul((vh_idx.get((vers, ht)) or ('',))[0]) == gl), None)
                    if ht_par and kiejtes_ehhez(vers, ht_par):
                        heber_kulcsszo = ragozott_kiejtessel(*kiejtes_ehhez(vers, ht_par))
                tabla_sorok.append('| %s | %s | %s | %s | egyező | Septuaginta |' % (
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
                    szamol('LXX-minusz')
                    gm = 'nincs megfelelő a görögben (LXX-minusz)'
                    egyezes_cimke = 'LXX-minusz'
                else:
                    szamol('eltérő')
                    gorog_strong = (r.get('gorog_strong') or '').strip()
                    lk = lemma_kiejtes(gorog_strong) if gorog_strong else None
                    if lk:
                        kiejtes = lk[1]
                    else:
                        kiejtes = gorog_magyaros(gepi_atiras(r.get('gorog_lemma') or ''))
                    gm = '%s (%s%s)' % (r.get('gorog_lemma') or EM_DASH, kiejtes,
                                         ' %s' % gorog_strong if gorog_strong else '')
                    egyezes_cimke = 'eltérő'
                tabla_sorok.append('| %s | %s | %s | %s | %s | adat/lxx_dontesek.tsv |' % (
                    vers, dontesek_lxx_igehely, heber_kulcsszo, gm, egyezes_cimke))
                continue

            if vh_idx is not None:
                # F182 (A19, K72): a megfelelő egy forrásból — a 4.11 visszhang-blokkjának ellenőrzött LXX-társítása
                # (`adat/visszhang_megfelelok.tsv`), ha a versre és a lánc-szóra van ilyen sor
                par = next(((ht, vh_idx[(vers, ht)]) for ht in heber_tokenek if (vers, ht) in vh_idx), None)
                if par:
                    ht, (lemma_g, kiejtes_g) = par
                    if kiejtes_ehhez(vers, ht):
                        heber_kulcsszo = ragozott_kiejtessel(*kiejtes_ehhez(vers, ht))
                    szamol('eltérő')
                    forras_fajlok.add(VISSZHANG_TSV_REL)
                    tabla_sorok.append('| %s | %s | %s | %s (%s) | eltérő | gépi társítás (versszintű) |' % (
                        vers, lxx_igehely, heber_kulcsszo, lemma_g, kiejtes_g))
                    continue
            szamol('kutatói azonosítás függőben')
            tabla_sorok.append('| %s | %s | %s | %s | kutatói azonosítás függőben | Septuaginta |' % (
                vers, lxx_igehely, heber_kulcsszo, EM_DASH))
    if vh_idx is not None:
        # a lektor és a Fable közös véleménye (1–2.): négy egyezés-érték, és a 4.6 szavankénti mondata ugyanabból a
        # versenkénti ítéletből számol, mint az 5. szakasz táblája (1Móz 5:29: a kettő eddig eltért)
        tabla_sorok, szamlalo, heber_szamlalo = _lxx_ujraminosit(tabla_sorok, szamolt, tokenek, sorai[0]['id'])
    return tabla_sorok, szamlalo, forras_fajlok, heber_szamlalo


LXX_UJ_CIMKE = {'szocsalad': 'ugyanaz a szócsalád', 'nincs_par': 'nincs újszövetségi pár'}


def lxx_par_tokenek(tokenek):
    """A motívum héber szavai közül azok, amelyeknek a motívumban van újszövetségi párja: a kétnyelvű szótár (SECE)
    szerint a megfelelőjük a motívum egy görög szava, vagy annak szócsaládja (a 4.7 szabálya)."""
    g = [t for t in tokenek if t.startswith('G')]
    ki = set()
    for h in (t for t in tokenek if t.startswith('H')):
        eq = _sece_strongok(h)
        if any(x in g for x in eq) or any(_gorog_csalad(e, x) for e in eq for x in g):
            ki.add(h)
    return ki


def _lxx_csalad_cella(cella, gorog_tokenek):
    """A tábla görög cellájának valamely szava a motívum egy görög szavának szócsaládjába tartozik-e."""
    szavak = set(re.findall(r'[\u0370-\u03ff\u1f00-\u1fff]+', cella))
    for t in gorog_tokenek:
        lk = lemma_kiejtes(t)
        if lk and any(_gorog_tovek(w) & _gorog_tovek(lk[0]) for w in szavak):
            return True
    return False


def _lxx_ujraminosit(tabla_sorok, szamolt, tokenek, motivum_id):
    """Az új szerkezetű lap egyezés-értékei: egyező / ugyanaz a szócsalád / eltérő / nincs újszövetségi pár (a többi
    változatlan). A tábla és a szavankénti számláló egy ítéletből; kapu: a szavankénti összeg = a tábla összesítése."""
    gorog = [t for t in tokenek if t.startswith('G')]
    par = lxx_par_tokenek(tokenek)
    szamlalo = dict.fromkeys(LXX_SZAMLALO_KULCSOK, 0)
    heber = {}
    ki, k = [], 0
    for sor in tabla_sorok:
        cellak = [c.strip() for c in sor.strip().strip('|').split('|')]
        if len(cellak) < 6 or cellak[4] == 'nincs Septuaginta-könyv':
            ki.append(sor)
            continue
        _vers, hts, kulcs = szamolt[k]
        k += 1
        if kulcs == 'eltérő':
            if not any(h in par for h in hts):
                kulcs = 'nincs_par'
            elif _lxx_csalad_cella(cellak[3], gorog):
                kulcs = 'szocsalad'
            if kulcs in LXX_UJ_CIMKE:
                sor = sor.replace(' | eltérő | ', ' | %s | ' % LXX_UJ_CIMKE[kulcs], 1)
        szamlalo[kulcs] += 1
        for h in hts:
            heber.setdefault(h, dict.fromkeys(LXX_SZAMLALO_KULCSOK, 0))[kulcs] += 1
        ki.append(sor)
    if k != len(szamolt):
        raise ValueError('%s: az 5. szakasz sorai és az ítéletek száma eltér (%d / %d)' % (motivum_id, k, len(szamolt)))
    if all(len(h) == 1 for _v, h, _k in szamolt):
        for kk in LXX_SZAMLALO_KULCSOK:
            osszeg = sum(hs[kk] for hs in heber.values())
            if osszeg != szamlalo[kk]:
                raise ValueError('%s: a 4.6 szavankénti összege (%s=%d) eltér az 5. szakasz összesítésétől (%d)'
                                 % (motivum_id, kk, osszeg, szamlalo[kk]))
    return ki, szamlalo, heber


VISSZHANG_TSV_REL = 'adat/visszhang_megfelelok.tsv'


def _nfc_ekezet_nelkul(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s or '') if not unicodedata.combining(c)).lower()


def vh_lxx_index(motivum_id):
    """F182 (A19): {(Károli-vers, héber Strong): (görög lemma, kiejtés)} a 4.11 visszhang-blokk LXX-soraiból — csak az
    ellenőrzött (`ellenorzes` kitöltött), lemmás sor; a 4.11 ugyanezeket rendereli."""
    return {(r['igehely'], r['strong']): (r['lemma'], r['kiejtes']) for r in visszhang_sorok(motivum_id)
            if r['forras'] == 'lxx' and (r.get('lemma') or '').strip() and (r.get('ellenorzes') or '').strip()}


def lxx_egyforras_ellenoriz(motivum_id, tabla_sorok):
    """F182 (A19, K72) — kapu: ugyanarra a (vers, héber szó) párra az 5. szakasz és a 4.11 nem adhat eltérő LXX-megfelelőt.
    A tábla sorának héber kulcsszava kiejtéssel áll; a párt a sor görög lemmája és a 4.11 sora adja. Visszaad: az eltérések
    listája [(vers, Strong, 5. szakasz, 4.11)]."""
    idx = vh_lxx_index(motivum_id)
    elter = []
    for sor in tabla_sorok:
        cellak = [c.strip() for c in sor.strip('|').split('|')]
        if len(cellak) < 6 or cellak[4] not in ('egyező', 'eltérő', 'ugyanaz a szócsalád', 'nincs újszövetségi pár'):
            continue
        vers, gorog = cellak[0], cellak[3]
        # a cella görög szavai (az alak és a zárójeles lemma is)
        g_szavak = {_nfc_ekezet_nelkul(w) for w in re.findall(r'[Ͱ-Ͽἀ-῿]+', gorog)}
        vh = [(st, l) for (v, st), (l, _k) in idx.items() if v == vers]
        if not vh:
            continue
        # csak akkor ellentmondás, ha a sor héber kulcsszavának Strongjára van 4.11-sor; a cellában ennek a Strongnak a
        # saját párja kell álljon, nem a vers egy másik szaváé (F182 javítókör, ELLENOR_F182 #4: 1Móz 3:17 adámá ↔ γῆ)
        kulcs_st = [st for st, _l in vh if _heber_kulcsszo_strong(vers, st) == cellak[2]]
        for st in kulcs_st:
            if _nfc_ekezet_nelkul(idx[(vers, st)][0]) not in g_szavak:
                elter.append((vers, st, gorog, idx[(vers, st)][0]))
    return elter


def _heber_kulcsszo_strong(vers, strong):
    t = kiejtes_ehhez(vers, strong)
    return ragozott_kiejtessel(*t) if t else None


def blokk_lxx(m, sorai, tokenek):
    osz_sorai = [s for s in sorai if G.konyv_teszamentum(G.konyv_token(s['igehely'])) == 'ÓSZ']
    if not osz_sorai:
        hatokor = ('Ez a blokk a `[ID: %s]` motívum ÓSZ-i előfordulásait vetné össze az '
                    '`LXX_OS`-szel.' % m['id'])
        torzs = 'A motívumnak nincs ÓSZ-i előfordulása, ezért az LXX-fordítói döntések blokk üres.'
        return _lexikon_blokk(m['id'], 'lxx', [], [], hatokor, torzs, olvasoi('lxx_ures')), []

    fejlec = ['| Igehely (Károli) | LXX-igehely | Héber kulcsszó | Görög megfelelő | Egyezés | Forrás |',
              '|---|---|---|---|---|---|']
    sorok, szamlalo, forras_fajlok, _h = lxx_osszevetes(sorai, tokenek)
    if uj_szerkezet(m['id']):
        elter = lxx_egyforras_ellenoriz(m['id'], sorok)
        if elter:   # F182 (A19, K72): eltérésnél nem renderel
            raise ValueError('%s: az 5. szakasz és a 4.11 LXX-megfelelője eltér: %s' % (m['id'], elter))
    torzs = '\n'.join(fejlec + sorok)
    if uj_szerkezet(m['id']):
        torzs += ('\n\n*Összesítés: egyező=%d, ugyanaz a szócsalád=%d, eltérő=%d, nincs újszövetségi pár=%d, '
                  'LXX-minusz=%d, kutatói azonosítás függőben=%d, szamozas_elteres=%d.*'
                  % (szamlalo['egyező'], szamlalo['szocsalad'], szamlalo['eltérő'], szamlalo['nincs_par'],
                     szamlalo['LXX-minusz'], szamlalo['kutatói azonosítás függőben'], szamlalo['szamozas_elteres']))
    else:
        torzs += ('\n\n*Összesítés: egyező=%d, eltérő=%d, LXX-minusz=%d, kutatói azonosítás függőben=%d, '
                  'szamozas_elteres=%d.*'
                  % (szamlalo['egyező'], szamlalo['eltérő'], szamlalo['LXX-minusz'],
                     szamlalo['kutatói azonosítás függőben'], szamlalo['szamozas_elteres']))

    hatokor = ('Ez a blokk a `[ID: %s]` motívum ÓSZ-i előfordulásait veti össze az `LXX_OS`-szel '
               '(G5), soronként a Károli-vers minden versére.' % m['id'])
    dontesek_hasznalt = bool(szamlalo['eltérő'] or szamlalo['LXX-minusz'])
    forras_lista = sorted(forras_fajlok) + (['adat/lxx_dontesek.tsv'] if dontesek_hasznalt else [])
    olv = lxx_olvasoi(szamlalo, tokenek, uj=uj_szerkezet(m['id'])) or olvasoi('lxx', n=sum(szamlalo.values()),
                                                      osszegzes=lxx_olvasoi_osszegzes(szamlalo))
    blokk_szoveg = _lexikon_blokk(m['id'], 'lxx', sorted(set(forras_lista)),
                                   [LC('LXX_OS'), LC('projekt_adat')], hatokor, torzs, olv)
    forras_licenc_parok = [(f, LC('projekt_adat') if f == VISSZHANG_TSV_REL else LC('LXX_OS'))
                           for f in sorted(forras_fajlok)]
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


_kh_kihagyott = set()
_kh_gazda = {}   # a kihagyott forrásvers -> a lista gazdája (STEP-alak), az olvasói jegyzethez


def kh_index():
    """A Károli-KH listák forrásversenként. A másolat-gyanús forrásversek listája nem kerül a lapra (DT-F156n, N-F156a:
    a lista egy másik vers listájának másolata, `karoli_kh_epseg.gyanus_forrasok`); ezek a `_kh_kihagyott` halmazba
    kerülnek, és a blokk hatókör-sora megnevezi a számukat."""
    global _kh_by_step
    if _kh_by_step is None:
        import karoli_kh_epseg as KHE
        gyanus = KHE.gyanus_forrasok()
        idx = {}
        for r in L.load_karoli_kh():
            if r['Igehely'] in gyanus:
                _kh_kihagyott.add(r['Igehely'])
                _kh_gazda[r['Igehely']] = gyanus[r['Igehely']]
                continue
            idx.setdefault(r['Igehely'], []).append(r)
        _kh_by_step = idx
    return _kh_by_step


# A Minősítés olvasói szövegéhez: a 4. szakasz találatszáma és a rés párjai motívumonként (a rés később épül).
KERESZT_OSSZES = {}
MINOSITES_STAT = {}


def blokk_kereszthivatkozasok(m, sorai, konyv_sorrend, hianyzo_konyvek):
    sorai_rendezve = sorted(
        sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))

    bekezdesek = []
    nem_vizsgalhato = []
    kh_kihagyva = []
    talalat_szam = 0

    for s in sorai_rendezve:
        igehely = s['igehely']
        try:
            step = L.to_step(igehely)
        except ValueError:
            nem_vizsgalhato.append(igehely)
            continue

        kh_index()
        if step in _kh_kihagyott:
            kh_kihagyva.append(igehely)
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
    if nem_vizsgalhato and not uj_szerkezet(m['id']):   # az új szerkezetben a jegyzet mondja (lektor 16.)
        torzs_reszek.append('*Versenkénti kereséssel nem vizsgálható: %s.*' % ', '.join(nem_vizsgalhato))
    torzs = '\n\n'.join(torzs_reszek) if torzs_reszek else 'Nincs TSK/Károli-KH találat ehhez a motívumhoz.'

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehelyét veti össze a TSK (Votes ≥ 15) és a '
               'Károli-KH táblával; %d igehely ad legalább egy találatot (%d találat összesen), '
               '%d igehely versenkénti kereséssel nem vizsgálható.'
               % (m['id'], len(sorai_rendezve), len(bekezdesek), talalat_szam, len(nem_vizsgalhato)))
    if kh_kihagyva:
        hatokor += (' %d igehely Károli-KH listája kimaradt, mert egy másik vers listájának másolata '
                    '(`eszkozok/karoli_kh_epseg.py`, DT557): %s.' % (len(kh_kihagyva), ', '.join(kh_kihagyva)))
    if uj_szerkezet(m['id']):
        # lap-javit HAMART-001 (lektor 16.): olvasói jegyzet műhelyszavak nélkül, a nem vizsgált helyek okával és a
        # kimaradt listák gazdájával
        def _hu(step):
            try:
                k, f, v = L.parse_igehely(step.split('-')[0])
                return '%s %d:%d' % (k, f, v)
            except ValueError:
                return step
        hatokor = ('Ez a blokk a motívum %d helyét veti össze két hagyományos kereszthivatkozás-gyűjteménnyel: a '
                   'Treasury of Scripture Knowledge (TSK) erős, legalább 15 olvasói szavazatot kapott utalásaival és a '
                   'Károli-fordítás utalásaival; %d hely ad legalább egy utalást (összesen %d).'
                   % (len(sorai_rendezve), len(bekezdesek), talalat_szam))
        if nem_vizsgalhato:
            hatokor += (' %d hely több versre terjed (%s): a gyűjtemények versenként adnak utalást, ezért ezekre a '
                        'keresés nem terjed ki.' % (len(nem_vizsgalhato), ', '.join(nem_vizsgalhato)))
        if kh_kihagyva:
            hatokor += (' %d hely Károli-utalásai nem állnak itt, mert egy másik vers utalás-listájának (teljes vagy '
                        'részleges) másolatai: %s.' % (len(kh_kihagyva), '; '.join(
                            '%s (a %s listája)' % (ige, _hu(_kh_gazda.get(L.to_step(ige), ['?'])[0]))
                            for ige in kh_kihagyva)))
    blokk_szoveg = _lexikon_blokk(
        m['id'], 'kereszthivatkozasok',
        ['konkordancia/TSK_kereszthivatkozasok.tsv', 'konkordancia/Karoli_kereszthivatkozasok.tsv'],
        [LC('TSK'), LC('Karoli_KH')], hatokor, torzs,
        OK.kereszthivatkozasok(len(sorai_rendezve), len(bekezdesek), talalat_szam)
        or olvasoi('kereszthivatkozasok', n=len(sorai_rendezve), talalt=len(bekezdesek), osszes=talalat_szam)
    )
    KERESZT_OSSZES[m['id']] = talalat_szam
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


def _tipus_szam(sorok):
    d = {}
    for r in sorok:
        d[r['tipus']] = d.get(r['tipus'], 0) + 1
    return sorted(d.items(), key=lambda x: (-x[1], x[0]))


def blokk_kapcsolatok(m, konyv_sorrend, hianyzo_konyvek):
    sorok_ehhez = [r for r in kapcsolatok_sorok() if r['id'] == m['id']]

    if not sorok_ehhez:
        torzs = 'Ehhez a motívumhoz nincs rögzített kapcsolat.'
        hatokor = 'Ez a blokk a `[ID: %s]` motívum kapcsolat-sorait fedné a `kapcsolatok.tsv`-ből; 0 sor.' % m['id']
        return _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], [LC('projekt_adat')], hatokor, torzs,
                              olvasoi('kapcsolatok_ures')), \
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
    if uj_szerkezet(m['id']):
        # lap-javit HAMART-001 (lektor 18., orkesztrátori döntés): az oszlop jelentése egy helyen
        hatokor += (' A PaRDeS-szint oszlop a kapcsolat jellegét írja le (Remez: a két hely egymásra mutat), nem a '
                    'célhely saját szintjét; a helyek szintje a 2. szakaszban áll.')
    blokk_szoveg = _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], [LC('projekt_adat')], hatokor, torzs,
                                  OK.kapcsolatok(len(sorok_ehhez), len(igehelyek), _tipus_szam(sorok_ehhez),
                                                 sum(1 for r in sorok_ehhez if r['bizonyossag'] == 'magas'),
                                                 sum(1 for r in sorok_ehhez if r['bizonyossag'] == 'közepes')
                                                 if uj_szerkezet(m['id']) else None)
                                  or olvasoi('kapcsolatok', n=len(sorok_ehhez)))
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
                r['pardes_szint'] or EM_DASH, SZKZ.indok_cella(r['indoklas'] or EM_DASH)))
    else:
        out.append('A motívumhoz nincs rögzített motívumközi kapcsolat.')
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
    return _lexikon_blokk(m['id'], 'kapcsolodo', list(KAPCSOLODO_FORRASOK), [LC('projekt_adat')], hatokor, torzs,
                          kapcsolodo_olvasoi(m['id'], motivum_kapcsolatok_sorok(), motivumkozi_jeloltek())
                          or olvasoi('kapcsolodo'))


def kapcsolodo_olvasoi(motivum_id, mk_sorok, mk_jeloltek):
    """Az 5/b. olvasói szövege (OK.kapcsolodo) ugyanabból, amiből a kapcsolodo_torzs épül."""
    sajat = [(r['id_b'] if r['id_a'] == motivum_id else r['id_a'], r['tipus'], r['bizonyossag'])
             for r in mk_sorok if motivum_id in (r['id_a'], r['id_b'])]
    nyitott = sum(1 for j in mk_jeloltek if j.get('dontes') == 'nyitva'
                  and motivum_id in (j['id'], j.get('cel_id')))
    return OK.kapcsolodo(sajat, nyitott)


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

    # a lap helye a kanonikus közzétételi hely (helyőrző, amíg nincs meg); GitHub-URL nem kerül a lapra, mert a GitHub
    # nem kanonikus forrás (F168, 2026-11-04). A teljes idézési forma a Kolofon „Hogyan idézd” bekezdése.
    hogyan = [
        '**Hogyan hivatkozz:**',
        '- ID: `%s`' % m['id'],
        '- Cím: %s' % m.get('cim', EM_DASH),
        ('- Státusz: %s' % kiadasi_statusz(m['id']) if uj_szerkezet(m['id']) else   # F182 (A02; F18 (c))
         '- Státusz: %s (`%s`, %s)' % (m.get('statusz', EM_DASH), m.get('statusz_verzio', ''), m.get('statusz_datum', ''))),
        '- Generálva: %s' % G.TS,
        '- Hely: `%s`' % KANONIKUS_FORRAS_HELYORZO,
        '- Idézési forma: a Kolofon „Hogyan idézd” bekezdése',
    ]
    if uj_szerkezet(m['id']):
        # a felhasználó (2026-11-11): egy idézési forma, a Kolofonban; itt csak a mutató (a státusz és a generálás
        # dátuma a Kolofon táblájában)
        hogyan = ['**Hogyan hivatkozz:** az idézési forma a [Kolofon](#kolofon) „Hogyan idézd” bekezdésében áll.']

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
    if uj_szerkezet(m['id']):
        # F182 (B10): az olvasói forrásnév egyszer áll (több fájlja egy forrás), a licencek egyesítve
        csop = collections.OrderedDict()
        for fajl in adat_fajlok + beazonositatlan:
            csop.setdefault(olvasoi_forrasnev(fajl, nevelovel=False), set()).update(
                olvasoi_licencek(fajl, per_fajl[fajl]))
        adatforrasok = ['**Adatforrások:**'] + ['- %s (%s)' % (nev, ', '.join(sorted(lic))) for nev, lic in csop.items()]

    torzs = '\n'.join(hogyan) + '\n\n' + '\n'.join(szotarak) + '\n\n' + '\n'.join(adatforrasok)
    hatokor = ('Ez a blokk a `[ID: %s]` motívum hivatkozási adatait, a ténylegesen felhasznált '
               'szótárakat (teljes névvel, forrásfájlonként) és az adatforrásokat adja '
               '(G9, LEXV2_3-ig szűkítve).' % m['id'])
    return _lexikon_blokk(m['id'], 'idezes', [], [LC('projekt_adat')], hatokor, torzs, olvasoi('idezes'))


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


NINCS_ROGZITVE = 'nincs rögzítve'


def kolofon_naplo_cella(motivum_id):
    """A Kolofon „Kereszthivatkozás-napló” cellája. A nem migrált motívumnál
    a `tematikus_lezart/naplok/` alatti napló; a migrált motívumnál (F11 M3,
    DT-F11a) a régi napló az `archivum/[ID]/` alatt áll, a minősítés pedig a
    `jeloltek.tsv`-ből generált -- a cella ezt mondja ki, nem a megszűnt utat."""
    naplo_fajlnev = G.ID_NAPLO_TERKEP.get(motivum_id)
    if not naplo_fajlnev:
        return NINCS_ROGZITVE
    if os.path.exists(os.path.join(ROOT, 'tematikus_lezart', 'naplok', naplo_fajlnev)):
        return '`tematikus_lezart/naplok/%s`' % naplo_fajlnev
    archiv = 'archivum/%s/%s' % (motivum_id, naplo_fajlnev)
    if os.path.exists(os.path.join(ROOT, *archiv.split('/'))):
        return ('generált (`adat/jeloltek.tsv`); a régi napló archívum: `%s`' % archiv)
    return NINCS_ROGZITVE


KIADASOK_TSV = os.path.join(ADAT, 'kiadasok.tsv')
NINCS_KIADVA = 'nincs kiadva — feldolgozás alatt'


def kolofon_kiadasok(motivum_id, ut=None):
    """A motívum kiadás-sorai kiadásszám szerint (`adat/kiadasok.tsv`, SEMA 2.46; N-F125a/b, DT-F125d);
    sor nélkül, vagy ha a fájl hiányzik: üres lista. A kiadásszám egész, a rendezés számszerű."""
    ut = ut or KIADASOK_TSV
    if not os.path.isfile(ut):
        return []
    sorok = [r for r in L.read_tsv_skip_comments(ut) if (r.get('id') or '').strip() == motivum_id]
    return sorted(sorok, key=lambda r: int(r['kiadas']))


def kolofon_kiadas_sorok(kiadasok):
    """A Kolofon metaadat-táblájának „Kiadás” és „Próza modellje” sora (a legutóbbi kiadásé), és a
    „Változásjegyzék” tábla. Kiadás-sor nélkül (a lap még nincs kiadva) a három hely kitöltött, de nem állít kiadást:
    „nincs kiadva — feldolgozás alatt” (olvasói kapu, KOLOFON, 2026-11-02)."""
    if not kiadasok:
        return (['| Kiadás | %s |' % NINCS_KIADVA, '| Próza modellje | %s |' % NINCS_KIADVA],
                ['**Változásjegyzék**', '', 'Még nincs kiadás, ezért nincs változás sem rögzítve; a jegyzék az első '
                 'kiadással indul.'])
    utolso = kiadasok[-1]
    meta = ['| Kiadás | %s |' % utolso['kiadas'].strip(),
            '| Próza modellje | `%s` |' % ((utolso.get('proza_modell') or '').strip() or 'manual')]
    jegyzek = ['**Változásjegyzék**', '', '| Kiadás | Dátum | Mi változott |', '|---|---|---|']
    for r in kiadasok:
        jegyzek.append('| %s | %s | %s |' % (r['kiadas'].strip(), r.get('datum', '').strip(), r.get('valtozas', '').strip()))
    return meta, jegyzek


LAP_ATNEZESEK_TSV = os.path.join(ADAT, 'lap_atnezesek.tsv')
# a szerzőségi mondatban felsorolt értelmező rések (a `res_forras.tsv` `tanulmany` forrású rései), a lapon álló sorrendben
SZERZOSEG_RESEK = ('kivonat', 'miert_fontos', 'minosites', 'alatamasztas', 'ertelmezes', 'alkalmazas', 'tanitoi',
                   'modszertan')


def _cim_szoveg(fejlec):
    """A rés fejléce címként: a `#` jelek, a sorszám és a régi „(kézi)” jelölés nélkül („## 6. Értelmezés” → „Értelmezés”)."""
    s = CIMJELOLES_RE.sub('', fejlec or '').lstrip('#').strip()
    return re.sub(r'^\d+(?:/[a-z])?\.\s*', '', s)


def kolofon_szerzoseg(motivum_id, kiadasok, atnezes_ut=None, res_sorok=None):
    """A Kolofon szerzőségi mondata (F123.GENKOR, DT-F181c) adatból: az értelmező rések (`res_forras.tsv`
    `tanulmany` forrás) neve, a legutóbbi kiadás `proza_modell`-je (`adat/kiadasok.tsv`), és hogy a felhasználó
    átnézte-e (`adat/lap_atnezesek.tsv`) — a „(kézi)” címsorjelölés helyett, amely a prózát hamisan a kutatónak
    tulajdonította. `manual` modellnél a mondat azt mondja, amit az adat: a készítő modellje nincs rögzítve."""
    res_sorok = res_forras_sorok() if res_sorok is None else res_sorok
    nevek = [_cim_szoveg(res_sorok[(motivum_id, r)]['fejlec']) for r in SZERZOSEG_RESEK
             if (res_sorok.get((motivum_id, r)) or {}).get('forras') == 'tanulmany']
    if not nevek:
        return 'A lap minden szakasza az adattáblákból generált.'
    reszek = '(%s)' % ', '.join(nevek)
    ut = atnezes_ut or LAP_ATNEZESEK_TSV
    # az átnézésből csak a tény és a dátum kerül a lapra; az `idezet` (a felhasználó szavai) belső nyilvántartás, soha
    # nem olvasói szöveg
    datumok = sorted((r.get('datum') or '').strip() for r in (L.read_tsv_skip_comments(ut) if os.path.isfile(ut) else [])
                     if (r.get('id') or '').strip() == motivum_id and (r.get('ki') or '').strip() == 'felhasználó')
    atnezve = datumok[-1] if datumok else ''
    if not kiadasok:
        return ('Az értelmező szakaszok %s még nincsenek kiadva: a szerző nem hagyta jóvá őket. A többi szakasz az '
                'adattáblákból generált.' % reszek)
    modell = (kiadasok[-1].get('proza_modell') or '').strip()
    if atnezve:
        jovahagyas = 'a szerző átnézte (%s) és jóváhagyta' % atnezve if atnezve.strip() else \
            'a szerző átnézte és jóváhagyta'
    else:
        jovahagyas = 'a szerző jóváhagyta'
    if modell and modell != 'manual':
        kezdet = ('Az értelmező szakaszokat %s mesterséges intelligencia (`%s`) írta az adatok alapján'
                  % (reszek, modell))
    else:
        kezdet = ('Az értelmező szakaszok %s készítőjét a kiadás nem rögzíti modellnévvel (kézi rögzítés, `manual`)'
                  % reszek)
    return '%s; %s. A többi szakasz az adattáblákból generált.' % (kezdet, jovahagyas)


KOZEL_KELETI_TSV = os.path.join(ADAT, 'kozel_keleti_hatar.tsv')


def kozel_keleti_sor(motivum_id, ut=None):
    """A motívum sora az `adat/kozel_keleti_hatar.tsv`-ből (SEMA 2.51), vagy None (a motívum nem érintett, vagy a
    tábla hiányzik)."""
    ut = ut or KOZEL_KELETI_TSV
    if not os.path.isfile(ut):
        return None
    for r in L.read_tsv_skip_comments(ut):
        if (r.get('id') or '').strip() == motivum_id:
            return r
    return None


def kolofon_kozlemenyek(m, kiadasok, kk_sor=None):
    """A Kolofon közleményekre kötött szövege (F168): az MI-nyilatkozatra mutató mondat (a szerzőségi mondat után áll),
    és három bekezdés: a „Hogyan idézd” (csak a lap idézése, utána egyetlen mutató mondat a nyílt adatkészletre),
    a módszertani elvek (Hays-leképezés) és a hatókör (az ókori közel-keleti határ). A hatókör-mondat minden
    lapon áll; az érintett motívumnál (`kozel_keleti_hatar.tsv`) egy további mondat, és ha a próza közel-keleti
    hátteret említ, egy harmadik. A szöveg sablon és adat, kézi próza nem kerül bele. A DOI, a kanonikus hely, a
    lexikon címe és a szerző neve helyőrző, amíg nincs meg. A lap a lexikon (fizetős ág) része: a nyílt adatmag
    magyarázata, idézési képlete és a `CITATION.cff` a nyílt mag dokumentációjába tartozik, a lapon csak egy mutató
    mondat áll (F167.4, a felhasználó döntése: „Lap + egy mutató”, 2026-11-05)."""
    mi = ('A mesterséges intelligencia szerepét, az ellenőrzés menetét és azt, amit az ellenőrzés nem állít, a '
          '[Nyilatkozat a mesterséges intelligencia használatáról](%s) írja le.' % KOZLEMENY['mi'])
    if kiadasok:
        kiadas = '%s. kiadás (%s)' % (kiadasok[-1]['kiadas'].strip(), (kiadasok[-1].get('datum') or '').strip())
    else:
        kiadas = 'kiadás előtti változat, még nem idézhető'
    idezes = ('**Hogyan idézd.** %(szerzo)s: *%(lexikon)s*, „%(cim)s” (`%(id)s`), %(kiadas)s, `%(url)s`. '
              + NYILT_ADAT_MUTATO + ': DOI: `%(doi)s`.') % {
                  'szerzo': SZERZO_HELYORZO, 'lexikon': LEXIKON_CIM_HELYORZO, 'cim': m.get('cim') or m['id'],
                  'id': m['id'], 'kiadas': kiadas, 'url': KANONIKUS_FORRAS_HELYORZO, 'doi': DOI_HELYORZO}
    if uj_szerkezet(m['id']):
        kiadasszam = kiadasok[-1]['kiadas'].strip() if kiadasok else None
        datum = (kiadasok[-1].get('datum') or '').strip() if kiadasok else G.TS
        kiadas_szoveg = ('%s. kiadás' % kiadasszam) if kiadasszam else 'kiadás előtti változat, még nem idézhető'
        nyilt = ('%s: https://doi.org/%s.' % (NYILT_ADAT_MUTATO, NYILT_MAG_DOI) if NYILT_MAG_DOI
                 else '%s; %s.' % (NYILT_ADAT_MUTATO_UJ, DOI_HIANY))
        idezes = ('**Hogyan idézd.** %s: *%s*, „%s” (%s), %s, %s, %s. %s' % (
            SZERZO_NEV, LEXIKON_CIM_HU, m.get('cim') or m['id'], m['id'], kiadas_szoveg, datum,
            kanonikus_cim(m['id'], kiadasszam), nyilt))
    modszer = ('**Módszertani elvek.** Hogy a módszer elemei a bibliai intertextualitás-kutatásban bevett mérce, '
               'Richard B. Hays hét kritériuma közül melyiknek felelnek meg, és melyiket nem fedik (a történeti '
               'hihetőséget nem), [A módszer Hays hét kritériumának tükrében](%s) mutatja be.' % KOZLEMENY['hays'])
    if uj_szerkezet(m['id']):
        # a felhasználó jelzése (2026-11-11): a link-cím olvasóként kitöltetlen helyőrzőnek látszott; a bekezdés a
        # közlemény (`kozlemeny/HAYS_LEKEPEZES.md`) táblája szerint mondja ki, mit fed a módszer
        modszer = ('**Módszertani elvek.** A bibliai intertextualitás-kutatás bevett mércéje Richard B. Hays hét kérdése '
                   'arról, valóban visszhangoz-e egy szöveg egy korábbit. A módszer a tematikus koherenciát fedi (a '
                   'kizáró feltétel és a fölérendelt fogalom); részben fedi a hozzáférhetőséget (a Septuaginta-'
                   'megfelelés), a hangerőt (a közös szavak és szópárok) és az értelmezéstörténetet; a visszatérést a '
                   'teljes korpuszon méri, nem szerzőnként; a kielégítő értelem csak értelmezésként, mérés nélkül áll; '
                   'a történeti hihetőséget nem fedi, mert ókori közel-keleti és keltezési réteg nincs. A részletes '
                   'leképezés a lexikon módszertani közleményében áll („A módszer Hays hét kritériumának tükrében”).')
    hatokor = ('**Hatókör.** A lap állításai a bibliai korpuszra (héber Ószövetség, görög Újszövetség, Septuaginta) '
               'vonatkoznak. Ókori közel-keleti (ugariti, mezopotámiai, egyiptomi) összehasonlító réteg a munkában nincs, '
               'ezért ha a lap nem hoz közel-keleti párhuzamot, az a módszer határa, nem negatív lelet '
               '([Az ókori közel-keleti háttér határa](%s)).' % KOZLEMENY['kozel_keleti'])
    if kk_sor is not None:
        hatokor += (' Ennél a motívumnál a nemzetközi szakirodalom a közel-keleti, főként ugariti anyag bevonását is '
                    'várja; ez a lap ilyen összevetést nem végez.')
        emlites = (kk_sor.get('proza_emlites') or '').strip()
        if emlites:
            hatokor += (' Ahol az értelmező szöveg közel-keleti hátteret említ (%s), az értelmezés, másodlagos '
                        'irodalom nyomán: nem a lekérdezések eredménye, és az eredeti közel-keleti szövegen nem '
                        'ellenőriztük.' % emlites)
    return mi, [idezes, modszer, hatokor]


LAP_JAVITASOK_TSV = os.path.join(ADAT, 'lap_javitasok.tsv')


def kolofon_lektoralas(motivum_id, ut=None):
    """A Kolofon „Emberi lektorálás” sora az `adat/lap_javitasok.tsv`-ből (SEMA 2.49, DT-F123f): a lapon
    ténylegesen javított helyek (a nem `generátor` típusú sorok) száma, a dátumok és a jóváhagyók, ismétlés nélkül,
    rendezve. Sor nélkül, vagy ha a fájl hiányzik: None (a Kolofon nem ír semmit)."""
    ut = ut or LAP_JAVITASOK_TSV
    if not os.path.isfile(ut):
        return None
    sorok = [r for r in L.read_tsv_skip_comments(ut)
             if (r.get('id') or '').strip() == motivum_id and (r.get('tipus') or '').strip() != 'generátor']
    if not sorok:
        return None
    datumok = sorted({(r.get('datum') or '').strip() for r in sorok if (r.get('datum') or '').strip()})
    lektorok = sorted({(r.get('jovahagyta') or '').strip() for r in sorok if (r.get('jovahagyta') or '').strip()})
    return '| Emberi lektorálás | %d hely (%s); lektorálók: %s |' % (len(sorok), ', '.join(datumok), ', '.join(lektorok))


KIADAS_LEKTOR_MD = os.path.join(os.path.dirname(ADAT), 'naplok', 'KIADAS_%s_lektor.md')


def kolofon_lektor_uj(motivum_id, lektor_ut=None, javitas_ut=None):
    """Az új szerkezetű lap Kolofonjának lektori sorai. (1) „Modell-lektor (<modell>) | N jelzett hely (dátum)”: a
    `/kiadas` lektorának kérdéslistájából (`naplok/KIADAS_<ID>_lektor.md`): a modell a „Lektor:” sor `claude-…` neve, az
    N a „Lektor kérdései” szakasz számozott tételei (az orkesztrátori észrevételek nélkül), a dátum a szakasz első
    dátuma. (2) „Szerkesztői átnézés és jóváhagyás”: a `lap_javitasok.tsv` felhasználó által jóváhagyott sorainak
    dátumaival. Forrás nélkül a sor nem áll."""
    ki = []
    lektor_ut = lektor_ut or KIADAS_LEKTOR_MD % motivum_id
    if os.path.isfile(lektor_ut):
        with io.open(lektor_ut, encoding='utf-8') as f:
            sz = f.read().replace('\r\n', '\n')
        mm = re.search(r'(?m)^Lektor:.*?`(claude-[\w.-]+)`', sz)
        if mm and '## Lektor kérdései' in sz:
            resz = sz.split('## Lektor kérdései', 1)[1].split('\n## ', 1)[0]
            n = len(re.findall(r'(?m)^\*\*\d+\. ', resz))
            d = re.search(r'(20\d\d)-(\d\d)-(\d\d)', resz)
            if n:
                ki.append('| Modell-lektor (%s) | %d jelzett hely%s |' % (
                    mm.group(1), n, (' (%s.%s.%s)' % d.groups()) if d else ''))
    javitas_ut = javitas_ut or LAP_JAVITASOK_TSV
    if os.path.isfile(javitas_ut):
        sorok = [r for r in L.read_tsv_skip_comments(javitas_ut)
                 if (r.get('id') or '').strip() == motivum_id and (r.get('jovahagyta') or '').strip() == 'felhasználó']
        datumok = sorted({(r.get('datum') or '').strip() for r in sorok if (r.get('datum') or '').strip()})
        if sorok:
            ki.append('| Szerkesztői átnézés és jóváhagyás | a teljes lap; a jelzett helyek javításait a szerkesztő '
                      'hagyta jóvá (%s) |' % ', '.join(datumok))
    return ki


# F182 (B10, K91): az új szerkezetű lap Kolofonjának forrástáblája forrásonként egy sor, „Fájl” oszlop nélkül (a fájlnév nem
# állhat a lapon, az olvasói név pedig a „Forrás” oszlop ismétlése volt); a blokk-kód helyett a lap szakaszának neve.
KOLOFON_SZAKASZNEV = {'elofordulasok': '2. Előfordulások', 'kizart': '3. Kizárt és vizsgált helyek',
                      'szocikkek': '4. Szótári háttér', 'lxx': '5. LXX-fordítói döntések',
                      'kereszthivatkozasok': '6. Kereszthivatkozások', 'kapcsolatok': '7. Kapcsolatok',
                      'hatastortenet': '9. Hatástörténet', 'ertelmezes': '10. Értelmezés'}   # F183


# a nyílt mag (`nyilt_mag/`, CC BY 4.0) a saját adatból ezeket adja ki (`nyilt_mag_export.py`): a lapon ezek licence a
# nyílt mag szerint áll, nem „minden jog fenntartva” (a felhasználó jelzése, 2026-11-11)
NYILT_MAG_ADAT = frozenset({'adat/motivumok.tsv', 'adat/elofordulasok.tsv', 'adat/jeloltek.tsv', 'adat/kapcsolatok.tsv',
                            'adat/motivum_kapcsolatok.tsv', 'adat/elutasitasi_okok.tsv'})
NYILT_MAG_LICENC = 'CC BY 4.0, a nyílt adatmagban'
# az előfordulás-tábla igehelyenkénti magyarázata (`kapcsolodas`, a funkció magyarázata) a nyílt magból kimarad
# (`nyilt_mag_export.py` `funkcio_cimke`, README „Not included”): a lapon ez a rész a projekté (ELLENOR_HAMART_lapkeret 1.)
ELOFORDULAS_LICENC = 'adatoszlopok: CC BY 4.0, a nyílt adatmagban; igehelyenkénti magyarázat: %s'   # névelő nélkül (lista- és táblaelem)
FORDITAS_LICENC = 'magyar fordítás: %s; a lefordított szótárszöveg licence a szótár saját soránál áll'


def olvasoi_licencek(fajl, licencek):
    """Az új szerkezetű lap forráslistájának licence: a nyílt magban kiadott saját adat CC BY 4.0 (az előfordulás-
    táblánál csak az adatoszlopok; a magyarázat a projekté); a Károli–Strong párosítás CC BY 4.0 (DT623); a
    fordítástáblában a fordítás a projekté, a lefordított szótárszöveg licence a szótár saját soránál."""
    lic = set(licencek)
    projekt = LC('projekt_adat')
    if fajl.endswith('adat/elofordulasok.tsv') and projekt in lic:
        lic = (lic - {projekt}) | {ELOFORDULAS_LICENC % projekt}
    elif fajl in NYILT_MAG_ADAT and projekt in lic:
        lic = (lic - {projekt}) | {NYILT_MAG_LICENC}
    elif fajl.rstrip('/').endswith('karoli_strong') and projekt in lic:
        lic = (lic - {projekt}) | {LC('Karoli_Strong_parok') + (', https://doi.org/%s' % KAROLI_STRONG_DOI
                                                                 if KAROLI_STRONG_DOI else '')}
    elif fajl.endswith('forditasok.tsv') and projekt in lic:
        # a fordítások forrása vegyes licencű (BDB, Thayer közkincs; UBS CC BY-SA 4.0): a forrás licence a szótár
        # sorában áll, itt csak a fordításé (ELLENOR_HAMART_lapkeret 1.)
        lic = {FORDITAS_LICENC % projekt}
    return lic


def kolofon_forrastabla_olvasoi(per_fajl):
    csop = collections.OrderedDict()
    for fajl in sorted(per_fajl, key=lambda f: olvasoi_forrasnev(f, nevelovel=False).lower()):
        r = csop.setdefault(olvasoi_forrasnev(fajl, nevelovel=False), {'licenc': set(), 'blokkok': set()})
        r['licenc'].update(olvasoi_licencek(fajl, per_fajl[fajl]['licenc']))
        r['blokkok'].update(per_fajl[fajl]['blokkok'])
    sorrend = list(KOLOFON_SZAKASZNEV)
    sorok = ['| Forrás | Licenc | Szakasz |', '|---|---|---|']
    for nev, r in csop.items():
        szak = ', '.join(KOLOFON_SZAKASZNEV.get(b, b) for b in sorted(r['blokkok'], key=lambda b: (
            sorrend.index(b) if b in sorrend else len(sorrend), b)))
        sorok.append('| %s | %s | %s |' % (nev, ', '.join(sorted(r['licenc'])), szak))
    return sorok


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
        '| Sablon-megfelelőség | %s |' % (m.get('sablon_verzio') or NINCS_ROGZITVE),
    ]
    kiadasok = kolofon_kiadasok(m['id'])
    kiadas_meta, kiadas_jegyzek = kolofon_kiadas_sorok(kiadasok)
    uj = uj_szerkezet(m['id'])
    if uj:
        # F182 (A02; F18 (e)), a felhasználó (2026-11-11): a lap elején az egyszerűsített kolofon
        # (`egyszerusitett_kolofon`), a Kolofonban a teljes azonosító tábla, a sablon és a kiadás adatai, olvasói
        # mezőnévvel
        # a felhasználó (2026-11-11): az elején egyszerűsített kolofon, „a legvégén a teljes”; a „Kézi forrás” és a
        # „Kereszthivatkozás-napló” belső sora nem olvasói, kimarad
        metaadat_sorok = (metaadat_sorok[:2]
                          + ['| %s | %s |' % (nev, kiadasi_statusz(m['id']) if kulcs is None else (m.get(kulcs) or EM_DASH))
                             for nev, kulcs in AZONOSITO_MEZOK]
                          + metaadat_sorok[-1:] + ['| Generálva | %s |' % G.TS])
    metaadat_sorok += kiadas_meta
    if uj_szerkezet(m['id']):
        # a felhasználó döntése (2026-11-12): a modell-lektor és a szerkesztői jóváhagyás külön sorban; az „Emberi
        # lektorálás” sor egy későbbi, nevesített emberi lektornak marad
        lektoralas = kolofon_lektor_uj(m['id'])
        metaadat_sorok += lektoralas
    else:
        lektoralas = kolofon_lektoralas(m['id'])
        if lektoralas:
            metaadat_sorok.append(lektoralas)

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
    if uj:
        forras_sorok = kolofon_forrastabla_olvasoi(per_fajl)

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

    kk_sor = kozel_keleti_sor(m['id'])
    mi_mondat, kozlemeny_bekezdesek = kolofon_kozlemenyek(m, kiadasok, kk_sor)
    torzs = ('**Szerzőség.** %s %s\n\n' % (kolofon_szerzoseg(m['id'], kiadasok), mi_mondat)
             + ''.join(b + '\n\n' for b in kozlemeny_bekezdesek) + '\n'.join(metaadat_sorok))
    if kiadas_jegyzek:
        torzs += '\n\n' + '\n'.join(kiadas_jegyzek)
    torzs += '\n\n---\n\n' + '\n'.join(forras_sorok)
    if megjelolesek:
        torzs += '\n\n' + '\n\n'.join(megjelolesek)

    hatokor = ('Ez a blokk a `[ID: %s]` motívum törzsadatait (`motivumok.tsv`) és a lexikon-oldalon '
               'ténylegesen felhasznált forrásokat sorolja fel.' % m['id'])
    if uj:
        # a felhasználó jelzése (2026-11-11): a belső szó („motívumtábla”) helyett olvasói mondat
        hatokor = ('Ez a blokk a motívum azonosító adatait, a lap kiadási állapotát és a lap minden forrását, '
                   'licencével együtt, sorolja fel.')
    return _lexikon_blokk(m['id'], 'kolofon', sorted(set(per_fajl) | {'adat/motivumok.tsv', 'adat/res_forras.tsv'} | ({'adat/kiadasok.tsv', 'adat/lap_atnezesek.tsv'} if kiadasok else set()) | ({'adat/lap_javitasok.tsv'} if lektoralas else set()) | ({'adat/kozel_keleti_hatar.tsv'} if kk_sor else set())),
                           sorted(tabla_licencek | {LC('projekt_adat')}), hatokor, torzs, olvasoi('kolofon'))


# ---------------------------------------------------------------------------
# R1.3 (RENDER_BRIEF.md) -- a het kezi res osszeallitasa adat/res_forras.tsv
# szerint. G2: fejlecsor a tablabol + torzs a tanulmanybol (vagy a lap mai
# rese valtozatlanul, vagy -- G16 -- adatbol generalva). Hianyzo jelolo vagy
# tabla-sor HIBAKOD, nem helyorzo (R1.3).
# ---------------------------------------------------------------------------

# DT-F178b (a felhasználó: „Kivezetjük”; lépcsős kivezetés, orkesztrátori döntés, 2026-11-08): a `tanitoi` rés
# sora motívumonként, a motívum teljes folyamatának lapgenerálásával kerül ki a `res_forras.tsv`-ből (MUNKAMENET C5).
# Sor nélkül a rés kivezetett: a régi címhatár a váz literál fejlécével olvasható, a rés nem renderel.
TANITOI_KIVEZETVE_FEJLEC = '### Tanítói egyezés'
# F182 (A21; F17, B04: „nincs is alkalmazás”, a felhasználó, 2026-11-10): az `alkalmazas` rés ugyanígy, lépcsősen kerül ki
# (a HAMART-001 sora törölve; a többi motívum a teljes folyamatával); a régi címhatár a váz literál fejlécével olvasható
KIVEZETETT_RES_FEJLEC = {'tanitoi': TANITOI_KIVEZETVE_FEJLEC, 'alkalmazas': '### Alkalmazás és tanítványság'}


def res_kivezetett(motivum_id, res):
    return res in KIVEZETETT_RES_FEJLEC and (motivum_id, res) not in res_forras_sorok()


RES_SORREND = ('kivonat', '2b', 'miert_fontos', 'minosites', 'alatamasztas',
               'ertelmezes', 'alkalmazas', 'tanitoi', 'modszertan')

# DT-F127a (#127): a két új rés (`alkalmazas`, `tanitoi`) közös szakasza a
# 6. Értelmezés után. A régi lapokon a szakasz még nincs meg; a
# res_blokkok_alkalmaz() ilyenkor a 7. szakasz (a `modszertan` rés fejléce)
# elé szúrja, a törzset utána a res_forras.tsv szerint tölti.
SZAKASZ_6B = '## 6/b. Alkalmazás és tanítói egyezés'
# F123.GENKOR (DT-F181c): a címsor régi „*(kézi)*” / „*(generált)*” jelölése (a prózát hamisan a kutatónak tulajdonította);
# a generátor a kész lap minden címsorából leveszi (`cimjeloles_ki`), a határkeresés a régi alakot is elfogadja
CIMJELOLES_RE = re.compile(r' ?\*\((?:kézi|generált)(?:, ha van)?\)\*')


def cimjeloles_ki(szoveg):
    """A kész lap címsoraiból a „*(kézi)*” / „*(generált)*” jelölés nélkül (a kódblokk érintetlen)."""
    ki, kod = [], False
    for sor in szoveg.split('\n'):
        if sor.strip().startswith('```'):
            kod = not kod
        elif not kod and re.match(r'^#{1,6}\s', sor):
            sor = CIMJELOLES_RE.sub('', sor).rstrip()
        ki.append(sor)
    return '\n'.join(ki)
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
        torzs = res_tanulmany_torzs(sor['tanulmany'], res)
        return '' if res_ures_e(res, torzs) else torzs
    if forras == 'adat':
        mondat = sor.get('tanulmany')
        # F182: a rögzített hiány-mondat („nincs rögzített kapcsolat”) csak adat híján áll; ha a kapcsolat-táblában van
        # sora a motívumnak, a rés az adatból renderel (különben a lap hamisat állít; HAMART-001, F182.2 után 56 sor)
        if mondat and not (mondat == ALATAMASZTAS_NINCS_KAPCSOLAT and res == 'alatamasztas'
                           and any(r['id'] == m['id'] for r in kapcsolatok_sorok())):
            return mondat
        if res not in ADAT_RES_RENDEREK:
            raise ValueError('nincs adat-alapú render szabály: %s / %s' % (m['id'], res))
        if sorai is None:
            sorai = _elofordulas_sorai(m['id'])
        torzs = ADAT_RES_RENDEREK[res](m['id'], sorai)
        if res_ures_e(res, torzs):
            return ''
        # a kiejtés-szabály már itt (a rés saját `###` szakasz): így a lap rése és a táblából elvárt rés azonos
        # (ellenoriz.py 11. szabály); a lap utófeldolgozása (kiejtes_potol) itt már nem talál pótolnivalót
        import kiejtes_szoveg as KSZ
        return KSZ.potol(adatres_keret(m['id'], res, torzs))[0]
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
SECE_SZOTARAK = ('SECE_G', 'SECE_H')

# DT-F174a (2026-11-04): az adat nélküli szerkezeti blokk nem áll az olvasói lapon. Az opcionális rés csak akkor
# jelenik meg (fejléc, olvasói bevezető, törzs, proveniencia-sor), ha van tartalma: adatból generált résnél a
# renderelő sort talált, tanulmányból vett résnél a törzs nem a RENDER G15 mechanikus helyőrzője. A rés a sémában és a
# `res_forras.tsv`-ben megmarad: ha egyszer lesz MCGED-sor vagy kézi 2/b, magától megjelenik. A kutatási üres
# eredmény (pl. „üres blokk: javaslat” a szerepmátrixban, a Minősítés „nincs” mondatai) nem ilyen, az a lapon marad.
OPCIONALIS_RESEK = ('2b',)
# a rés hiánymondatai: a RENDER G15 helyőrzője a tanulmányokban (nem kutatási lelet, hanem a jelölőpár kitöltése), és
# a 2026-11-04 előtti generátor hiánymondata (az ellenoriz.py 31. szabálya a régi lapon is felismeri)
SZERKEZETI_HELYORZOK = {'2b': ('Nincs kiegészítő szótári adat.',
                               '*Nincs a szerepmátrixon (2. szakasz) túli kiegészítő szótári sor a '
                               '`lexikon_hivatkozasok.tsv`-ben ehhez a motívumhoz.*')}
_GENERALT_RES_JELOLO_RE = re.compile(r'^<!-- GENERÁLT-RÉS: [^\n]*-->$', re.M)
_RES_PROV_SOR_RE = re.compile(r'^\*Proveniencia: `scope=[^`]*`\*$', re.M)


def res_ures_e(res, torzs):
    """Igaz, ha az opcionális rés törzse adat nélküli szerkezeti blokk: üres, vagy -- a GENERÁLT-RÉS jelölő és a
    proveniencia-sor nélkül -- csak a hiánymondata (SZERKEZETI_HELYORZOK)."""
    if res not in OPCIONALIS_RESEK:
        return False
    t = _RES_PROV_SOR_RE.sub('', _GENERALT_RES_JELOLO_RE.sub('', torzs or '')).strip()
    return not t or t in SZERKEZETI_HELYORZOK.get(res, ())


def lap_ures_szerkezeti_resek(fajl_szoveg, m):
    """A lapon álló, adat nélküli opcionális rések (ellenoriz.py 31. szabály)."""
    fajl_szoveg = regi_szerkezetre(fajl_szoveg)   # F178: az új szerkezetű lap a régi rés-határokkal olvasva
    talalt = []
    for res in OPCIONALIS_RESEK:
        if (m['id'], res) not in res_forras_sorok():
            continue
        if _opcionalis_res_helye(fajl_szoveg, m, res)[0] is None:
            continue
        if res_ures_e(res, res_torzs_lapbol(fajl_szoveg, m, res)):
            talalt.append(res)
    return talalt

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
    if csoportok and uj_szerkezet(motivum_id):
        # lap-javit HAMART-001 (lektor 20.): a soronként ismétlődő döntés- és forrásfarok (` | DT… | scope=…`) a
        # cellában nem áll; a blokk alatt egyszer, olvasói alakban, a nyers farok HTML-megjegyzésben
        sorok += ['| Kapcsolat | Alátámasztás |', '|---|---|']
        farkak = []
        for indoklas, parok in csoportok:
            fo, _, farok = indoklas.partition(' | ')
            if farok and farok not in farkak:
                farkak.append(farok)
            sorok.append('| %s | %s |' % (_cella('; '.join(parok)), SZKZ.indok_cella(fo)))
        dt = sorted({d for f in farkak for d in re.findall(r'\bDT\d+\b', f)})
        datumok = sorted({dontes_datum(d) for d in dt if dontes_datum(d)})
        if uj_szerkezet(motivum_id):
            # a felhasználó átnézése (14.): olvasói mondat; a döntés dátuma és a nyers farok a rejtett megjegyzésben
            sorok += ['', '*Az egyezéseket a héber és a görög szöveg, a Septuaginta és a két kereszthivatkozás-gyűjtemény '
                      '(TSK, Károli) méri; az indoklás a szerkesztőé.*%s'
                      % ''.join('<!-- %s%s -->' % (f.replace('--', '—'),
                                                   (' (%s)' % ', '.join(datumok)) if datumok else '') for f in farkak)]
        else:
            sorok += ['', '*Az indoklások egy szerkesztői döntésből valók%s; a mért egyezéseket a héber és a görög szöveg, a '
                      'Septuaginta és a két hagyományos kereszthivatkozás-gyűjtemény (TSK, Károli) adja.*%s'
                      % ((' (%s)' % ', '.join(datumok)) if datumok else '',
                         ''.join('<!-- %s -->' % f.replace('--', '—') for f in farkak))]
    elif csoportok:
        sorok += ['| Kapcsolat | Alátámasztás |', '|---|---|']
        for indoklas, parok in csoportok:
            sorok.append('| %s | %s |' % (_cella('; '.join(parok)), SZKZ.indok_cella(indoklas)))
    else:
        sorok.append('A motívum %d kapcsolat-sorának egyikéhez sincs rögzített indoklás.' % len(sajat))
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
        # ISTENTISZT-001 arany lap, 2026-10-29: a SECE-sorok nem itt állnak (a 7. szerep és a Rokon szavak olvasható táblázata; a nyers LN/GK
        # mező N-F33a szerint nem kerülhet a renderbe)
        sajat = [r for r in hiv_sorok if r['strong'] == t and r['szotar'] in KIEGESZITO_SZOTARAK
                 and r['szotar'] not in SECE_SZOTARAK]
        sorok_ehhez += sorted(sajat, key=lambda r: (r['szotar'], r['jelentes_szam']))
    if not sorok_ehhez:
        return ''  # DT-F174a: adat nélkül a rés nem áll a lapon (res_ures_e, OPCIONALIS_RESEK)
    out =['*Generált a `lexikon_hivatkozasok.tsv`-ből: a szerepmátrixon (2. szakasz) túli szótári sorok '
           '(%s).*' % ', '.join(x for x in KIEGESZITO_SZOTARAK if x not in SECE_SZOTARAK)]
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
    erintett = {x for a, b, _c in lattuk for x in (a, b)}
    MINOSITES_STAT[motivum_id] = (len(parok), len(erintett), len(elof_igehelyek))
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
        # DT-F152a (b): a tábla az 1/b. adatát ismétli, ezért csukva áll. F123.INDOKLAS: az 1/b. olvasói formája —
        # miért lett jelölt (szöveggel), döntés és ok; a nyers forrás, a proveniencia és a döntés nyoma (`dontes_ref`)
        # lábjegyzetben.
        tabla = ['<details>',
                 '<summary>Kereszthivatkozásból minősített jelöltek (%d sor; %s)</summary>' % (len(jeloltek), osszeg),
                 '', '| Igehely | Miért lett jelölt | Döntés és indok |', '|---|---|---|']
        sorok_md, labj = minosites_jelolt_sorok(motivum_id, jeloltek)
        tabla += sorok_md
        tabla += ['', '</details>']
        out.append('\n'.join(tabla))
        labj, kozos = SZKZ.kozos_proveniencia(labj, 'M')   # F152 B.2
        out.append('\n'.join('[^mj%d]: %s' % (i, t) for i, t in enumerate(labj, 1)))
        if kozos:
            out.append(kozos)
    else:
        out.append('**Kereszthivatkozásból minősített jelölt:** ehhez a motívumhoz nincs.')
    return '\n\n'.join(out)


def minosites_jelolt_sorok(motivum_id, jeloltek):
    """(táblasorok, lábjegyzetek) a Minősítés rés jelölt-táblájához, az 1/b. mintájára (`szerep_kizart`): a miért lett
    jelölt a `forras_kereses`-ből, a döntés és az elutasítás oka a mintaszótárból, az indoklás olvasói alakja; a
    lábjegyzetben a nyers forrás, az indoklás ` | ` utáni része és a `dontes_ref` (F123.INDOKLAS)."""
    minta = SZKZ.okok(motivum_id)
    sorok, labj = [], []
    for j in jeloltek:
        _csop, miert = SZKZ.jeloles_oka(j.get('forras_kereses'))
        fo, _sep, farok = (j.get('indoklas') or '').partition(' | ')
        if j['dontes'] == 'elutasítva':
            dontes = '**elutasítva** — %s' % SZKZ.elutasitas_oka(fo, minta)
        elif j['dontes'] == 'nyitva':
            dontes = '**nyitott döntés**'
        else:
            dontes = '**%s**' % j['dontes']
        olv = SZKZ.olvasoi_indok(fo)
        lj = 'forrás: `%s`%s' % (j.get('forras_kereses') or EM_DASH, (' · ' + _cella(farok)) if farok else '')
        if SZKZ.nyom_lapra(j.get('dontes_ref')):
            lj += ' · a döntés nyoma: `%s`' % SZKZ.nyom_lapra(j.get('dontes_ref'))
        if olv != fo:
            lj += ' · indoklás (nyers): %s' % _cella(fo)
        labj.append(lj)
        cella = dontes if not olv else '%s: %s' % (dontes, SZKZ.indok_strong(_cella(olv), strong_cim))   # F123.TUD1B
        sorok.append('| %s | %s[^mj%d] | %s |' % (j['igehely'], _cella(miert), len(labj), cella))
    return sorok, labj


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
    # F123.GENKOR (DT-F181c): a fejléc sor eleji, teljes sor; a meglévő lap a régi „*(kézi)*” / „*(generált)*”
    # jelölést is hordozhatja (a jelölés nélküli fejléc mindkét alakot megtalálja; F11 M3: a kettő egymásnak is megfelel)
    alap = CIMJELOLES_RE.sub('', needle)
    m = re.compile(r'(?m)^' + re.escape(alap) + r'(?:' + CIMJELOLES_RE.pattern + r')?[ \t]*$').search(fajl_szoveg,
                                                                                                    search_from)
    if m:
        return m.start(), m.group(0)
    try:
        return fajl_szoveg.index(needle, search_from), needle
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
    fajl_szoveg = opcionalis_res_visszaallit(fajl_szoveg, m)
    uresek = []
    for res in RES_SORREND:
        sor = sorok.get((m['id'], res))
        if sor is None and res_kivezetett(m['id'], res):
            continue   # DT-F178b: a kivezetett tanítói rés nem renderel
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
                if masik_sor is None and res_kivezetett(m['id'], ertek):
                    masik_sor = {'fejlec': KIVEZETETT_RES_FEJLEC[ertek]}
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
        if res in OPCIONALIS_RESEK and not torzs:
            # DT-F174a: a fejléc a többi rés határkereséséig marad, utána kikerül (opcionalis_resek_torol)
            uresek.append(res)
            fajl_szoveg = fajl_szoveg[:span_start] + fejlec + '\n\n' + fajl_szoveg[span_end:]
            continue
        # ISTENTISZT-001 arany lap, 2026-10-29: a rés olvasói bevezetője a generátorból (a kézi próza változatlan; res_torzs_lapbol leválasztja)
        olv = OLVASOI_RES.get(res)
        if res == 'minosites' and m['id'] in MINOSITES_STAT:
            olv = OK.minosites(*MINOSITES_STAT[m['id']], osszes=KERESZT_OSSZES.get(m['id']),
                               rag=uj_szerkezet(m['id'])) or olv
        uj_span = fejlec + '\n\n' + (olvasoi_bekezdes(olv) + '\n\n' if olv else '') + torzs + '\n\n'
        fajl_szoveg = fajl_szoveg[:span_start] + uj_span + fajl_szoveg[span_end:]
    return opcionalis_resek_torol(fajl_szoveg, m, uresek)


def _opcionalis_res_helye(fajl_szoveg, m, res):
    """(a rés fejlécének indexe vagy None, a következő határ indexe) -- az előző határ után keresve."""
    sorok = res_forras_sorok()
    slot_idx = _BOUNDARY_SLOTS.index(('res', res))

    def keres(slot, honnan):
        kind, ertek = slot
        if kind == 'lit':
            return _boundary_index(fajl_szoveg, ertek, honnan, None)
        return _boundary_index(fajl_szoveg, sorok[(m['id'], ertek)]['fejlec'], honnan, ertek)

    e_i, e_talalt = keres(_BOUNDARY_SLOTS[slot_idx - 1], 0)
    k_i, _ = keres(_BOUNDARY_SLOTS[slot_idx + 1], e_i + len(e_talalt))
    try:
        r_i, _ = keres(('res', res), e_i + len(e_talalt))
    except ValueError:
        return None, k_i
    return (r_i if r_i < k_i else None), k_i


def opcionalis_res_visszaallit(fajl_szoveg, m):
    """DT-F174a: az adat nélkül kihagyott opcionális rés (OPCIONALIS_RESEK) fejlécét a határkereséshez
    visszateszi a helyére (a következő határ elé); ha a rés a lapon áll, a szöveg változatlan."""
    for res in OPCIONALIS_RESEK:
        sor = res_forras_sorok().get((m['id'], res))
        if sor is None:
            continue
        r_i, k_i = _opcionalis_res_helye(fajl_szoveg, m, res)
        if r_i is None:
            fajl_szoveg = fajl_szoveg[:k_i] + sor['fejlec'] + '\n\n' + fajl_szoveg[k_i:]
    return fajl_szoveg


def opcionalis_resek_torol(fajl_szoveg, m, uresek):
    """DT-F174a: az üres opcionális rések fejléc+törzs span-je kikerül a lapról."""
    for res in uresek:
        r_i, k_i = _opcionalis_res_helye(fajl_szoveg, m, res)
        if r_i is not None:
            fajl_szoveg = fajl_szoveg[:r_i] + fajl_szoveg[k_i:]
    return fajl_szoveg


# A kézi rések nevesített lábjegyzetei (TEREMT-002, 2026-11-02, a felhasználó hibajelzése: „hülye jelek”). A rés törzse
# a RÉS-KEZDET/RÉS-VÉGE közötti szöveg; a benne álló `[^kulcs]` hivatkozások definíciója a forrás „Proveniencia-sorok”
# szakaszában, a réseken kívül áll, ezért a lapra nem került át, és a hivatkozás nyers jelként látszott. Az első natív
# forrás, amely nevesített lábjegyzetet használ, a TEREMT-002 (az ISTENTISZT-001 és az ALVIL-001 forrásában nincs ilyen).
# A lap definíció nélküli nevesített hivatkozásainak definíciója a motívum kézi forrásaiból (a `res_forras.tsv`
# `tanulmany` fájljai) egy generált blokkba kerül a kolofon elé; ha nincs hiány, nincs blokk (a többi lap bájtra azonos).
RES_LJ_BLOKK = 'res_labjegyzet'
_LJ_HIV_RE = re.compile(r'\[\^([^\]\s]+)\](?!:)')
_LJ_DEF_RE = re.compile(r'^\[\^([^\]\s]+)\]:[ \t]*(.*)$', re.M)


def lap_labjegyzet_hiany(szoveg):
    """A lap definíció nélküli lábjegyzet-hivatkozásai, első előfordulásuk sorrendjében (az ellenoriz.py 24.
    szabálya is ezt hívja)."""
    defs = {k for k, _v in _LJ_DEF_RE.findall(szoveg)}
    return list(dict.fromkeys(k for k in _LJ_HIV_RE.findall(szoveg) if k not in defs))


def res_labjegyzetek_alkalmaz(fajl_szoveg, m):
    cel_kulcs = _cel_kulcs(m['id'], RES_LJ_BLOKK)
    kezd_eleje = '<!-- GENERÁLT-KEZDET: general.py --cel %s ' % cel_kulcs
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % cel_kulcs
    regi = None
    i = fajl_szoveg.find(kezd_eleje)
    if i >= 0:
        j = fajl_szoveg.find(veg, i)
        if j < 0:
            raise ValueError('nyitó GENERÁLT-jelölő záró pár nélkül: %s' % cel_kulcs)
        j += len(veg)
        if fajl_szoveg[j:j + 2] == '\n\n':
            j += 2
        regi = fajl_szoveg[i:j]
        fajl_szoveg = fajl_szoveg[:i] + fajl_szoveg[j:]
    hiany = lap_labjegyzet_hiany(fajl_szoveg)
    if not hiany:
        return fajl_szoveg
    forrasok = list(dict.fromkeys(s['tanulmany'] for (mid, _res), s in sorted(res_forras_sorok().items())
                                  if mid == m['id'] and s['forras'] == 'tanulmany' and s.get('tanulmany')))
    definicio = {}
    for ut in forrasok:
        # a nyers forrásfájl: a `_tanulmany_szoveg` mélység szerint szűr, és a `belso` „Proveniencia-sorok” kimarad
        with io.open(os.path.join(G.ROOT, *ut.split('/')), encoding='utf-8') as f:
            for k, v in _LJ_DEF_RE.findall(f.read().replace('\r\n', '\n')):
                definicio.setdefault(k, (v, ut))
    sorok = ['[^%s]: %s' % (k, definicio[k][0]) for k in hiany if k in definicio]
    if not sorok:
        return fajl_szoveg
    forrasok = list(dict.fromkeys(definicio[k][1] for k in hiany if k in definicio))
    torzs = ('*A kézi rések (Kivonat, Miért fontos, Értelmezés, Módszertan) forrásjegyzetei, a kézi forrás '
             '„Proveniencia-sorok” szakaszából.*\n\n' + '\n'.join(sorok) + '\n\n' + veg + '\n\n')
    blokk = '%s| forrás: %s | licenc: %s | ts=%s -->\n\n%s' % (
        kezd_eleje, ', '.join(forrasok), LC('projekt_adat'), G.TS, torzs)
    ts_nelkul = re.compile(r' \| ts=[^ ]+ -->')
    if regi is not None and ts_nelkul.sub(' -->', regi, 1) == ts_nelkul.sub(' -->', blokk, 1):
        blokk = regi  # változatlan tartalom: a régi időbélyeg marad (fixpont)
    k = fajl_szoveg.find('\n## Kolofon')
    if k < 0:
        return fajl_szoveg.rstrip('\n') + '\n\n' + blokk
    return fajl_szoveg[:k + 1] + blokk + fajl_szoveg[k + 1:]


def res_torzs_lapbol(fajl_szoveg, m, res):
    """A rés törzse egy MÁR MEGÍRT lexikonoldal szövegéből -- 'lap' forrású
    résekhez (amelyeknek nincs adat-alapú vagy tanulmány-alapú előállítása,
    l. res_torzs()); a törzscikk-generátor (R1.7) ezzel olvassa vissza,
    amit a res_blokkok_alkalmaz() a lexikonoldalon változatlanul hagyott."""
    sorok = res_forras_sorok()
    fajl_szoveg = regi_szerkezetre(fajl_szoveg)   # F178: az új szerkezetű lap a régi rés-határokkal olvasva
    if res in OPCIONALIS_RESEK and _opcionalis_res_helye(fajl_szoveg, m, res)[0] is None:
        return ''  # DT-F174a: adat nélkül a rés nem áll a lapon
    fajl_szoveg = opcionalis_res_visszaallit(fajl_szoveg, m)
    offsets, talaltak = [], []
    search_from = 0
    for kind, ertek in _BOUNDARY_SLOTS:
        if kind == 'lit':
            needle = ertek
        else:
            sor = sorok.get((m['id'], ertek))
            if sor is None and res_kivezetett(m['id'], ertek):
                sor = {'fejlec': KIVEZETETT_RES_FEJLEC[ertek]}
            if sor is None:
                raise ValueError('hiányzó res_forras.tsv sor: %s / %s' % (m['id'], ertek))
            needle = sor['fejlec']
        # F123.GENKOR (DT-F181c): a régi lap a fejlécet még „*(kézi)*” jelöléssel hordozhatja
        i, talalt = _boundary_index(fajl_szoveg, needle, search_from, ertek if kind == 'res' else None)
        offsets.append(i)
        talaltak.append(talalt)
        search_from = i + len(talalt)
    slot_idx = _BOUNDARY_SLOTS.index(('res', res))
    body_start = offsets[slot_idx] + len(talaltak[slot_idx])
    body_end = offsets[slot_idx + 1]
    torzs = fajl_szoveg[body_start:body_end].strip('\r\n')
    if torzs.split('\n', 1)[0].endswith(OLVASOI_CIMKE):  # a generált olvasói bevezető nem a rés törzse (ISTENTISZT-001 arany lap, 2026-10-29)
        torzs = torzs.split('\n', 1)[1].strip('\r\n') if '\n' in torzs else ''
    return torzs


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
        if sor is None and res_kivezetett(m['id'], res):
            continue   # DT-F178b
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

# ===========================================================================
# F178 — az új lapszerkezet: Döntési út, folyamatos számozás (1–12, a szótári pontok 4.1–4.14), „/b” alszakasz és
# nevesített tanítói rész nélkül, áttekintő szótári tábla a 4. szakasz elején, visszhang-blokk (4.11)
# ===========================================================================
# Egyeztetett eltérés (a felhasználó, 2026-11-08: „Előbb csak a hamart”): az új szerkezet első lépésben csak a
# HAMART-001 lapján áll; a többi lap a felhasználó átnézése után egy körben követi, akkor a halmaz megszűnik
# (minden lap az új szerkezetre). Addig a többi lap generálása bájtra változatlan (E28).
UJ_LAPSZERKEZET = frozenset({'HAMART-001'})


def uj_szerkezet(motivum_id):
    return motivum_id in UJ_LAPSZERKEZET


UJ_SZAKASZOK = [
    'Kivonat', 'Jelmagyarázat és rövidítések', '1. Döntési út', '2. Előfordulások', '3. Kizárt és vizsgált helyek',
    '4. Szótári háttér', '5. LXX-fordítói döntések', '6. Kereszthivatkozások', '7. Kapcsolatok',
    '8. Kapcsolódó motívumok', '9. Hatástörténet: ókori fordítások és értelmezők', '10. Értelmezés',
    '11. Módszertan és nyitott kérdések', '12. Irodalom és idézés',
    'Kolofon',
]

# régi címsor -> új címsor (a teljes sor); a horgony és a link szövege ugyanígy cserélődik
UJ_CIMCSERE = [
    ('## 1. Előfordulások', '## 2. Előfordulások'),
    ('#### 1/a. Az igehelyek szövege', '#### 2.1. Az igehelyek szövege'),
    ('## 1/b. Kizárt és vizsgált helyek', '## 3. Kizárt és vizsgált helyek'),
    ('## 2. Szótári háttér', '## 4. Szótári háttér'),
    ('### 2/b. Kiegészítő szótári adatok', '### Kiegészítő szótári adatok'),
    ('## 3. LXX-fordítói döntések', '## 5. LXX-fordítói döntések'),
    ('## 4. Kereszthivatkozások', '## 6. Kereszthivatkozások'),
    ('## 5. Kapcsolatok', '## 7. Kapcsolatok'),
    ('## 5/b. Kapcsolódó motívumok', '## 8. Kapcsolódó motívumok'),
    ('## 6. Értelmezés', '## 10. Értelmezés'),   # F183: a 9. a Hatástörténet
    ('## 6/b. Alkalmazás és tanítói egyezés', '## 10. Alkalmazás'),
    ('## 7. Módszertan és nyitott kérdések', '## 11. Módszertan és nyitott kérdések'),
    ('## 8. Irodalom és idézés', '## 12. Irodalom és idézés'),
]

# a generált szövegek szakaszhivatkozásai (a régi szám -> az új); csak ezek a fordulatok, a szótárak saját
# „N. szakasz”-a (BDB, Thayer) érintetlen
UJ_SZOVEGCSERE = [
    ('a hely motívumbeli funkcióját az 1. szakasz táblázata adja', 'a hely motívumbeli funkcióját a 2. szakasz '
     'táblázata adja'),
    ('l. a 3. szakaszt (LXX-fordítói döntések)', 'l. az 5. szakaszt (LXX-fordítói döntések)'),
    ('a 3. szakaszban nincs sora', 'az 5. szakaszban nincs sora'),
    ('a Károli-szöveggel (1/a)', 'a Károli-szöveggel (2.1)'),
    ('a 2. pont a fő szótár', 'a 4.2 pont a fő szótár'),
]


def _cim_szoveg_csak(cim_sor):
    return cim_sor.lstrip('#').strip()


def uj_cimek_alkalmaz(szoveg):
    """A régi szakaszcímek az új számozással; a 4. szakaszon belül a szótári pontok („#### N. …”) 4.N-ként; a
    horgonyok és a link-szövegek a címmel együtt; a generált szöveg szakaszhivatkozásai (UJ_SZOVEGCSERE)."""
    csere = dict(UJ_CIMCSERE)
    ki, kod, szotari = [], False, False
    for sor in szoveg.split('\n'):
        if sor.strip().startswith('```'):
            kod = not kod
        if not kod:
            alap = sor.rstrip()
            if alap in csere:
                sor = csere[alap]
            if re.match(r'^## ', sor):
                szotari = sor.startswith('## 4. Szótári háttér')
            elif szotari:
                m = re.match(r'^#### (\d{1,2})\. (.*)$', sor)
                if m:
                    sor = '#### 4.%s. %s' % (m.group(1), m.group(2))
        ki.append(sor)
    szoveg = '\n'.join(ki)
    for regi, uj in UJ_CIMCSERE:
        r, u = _cim_szoveg_csak(regi), _cim_szoveg_csak(uj)
        szoveg = szoveg.replace('](#%s)' % _heading_slug(r), '](#%s)' % _heading_slug(u))
        szoveg = szoveg.replace('[%s](' % r, '[%s](' % u)
    for regi, uj in UJ_SZOVEGCSERE:
        szoveg = szoveg.replace(regi, uj)
    return szoveg


UJ_SZERKEZET_RX = re.compile(r'(?m)^## 1\. Döntési út[ \t]*$')


def regi_szerkezetre(szoveg):
    """Az új szerkezetű lap (F178) a régi szakaszcímekkel, a rés-határok olvasásához (a 11. és 31. szabály, a
    törzscikk): a címek visszaszámozva, a 4.N szótári pontok N-ként, az alkalmazás és a (kivezetett, üres) tanítói
    rés fejléce a helyén. A régi szerkezetű lap változatlan."""
    if not UJ_SZERKEZET_RX.search(szoveg):
        return szoveg
    # F183 (K67f): a vitatott pontok szakirodalom-sora generált, nem a rés része (a rés a kézi forrásé)
    szoveg = re.sub(r'\n\n\*Szakirodalom:\* [^\n]*', '', szoveg)
    # F183: a 9. Hatástörténet szakasz a régi szerkezetben nincs (a régi 4.11 helyén a mutató áll); a rés-határok
    # olvasásához a szakasz kimarad
    h = re.compile(r'(?m)^## 9\. Hatástörténet[^\n]*\n').search(szoveg)
    if h:
        k = re.compile(r'(?m)^## ').search(szoveg, h.end())
        szoveg = szoveg[:h.start()] + (szoveg[k.start():] if k else '')
    vissza = {uj: regi for regi, uj in UJ_CIMCSERE}
    ki = []
    for sor in szoveg.split('\n'):
        alap = sor.rstrip()
        if alap in vissza:
            sor = vissza[alap]
        else:
            sor = re.sub(r'^#### 4\.(\d{1,2})\. ', r'#### \1. ', sor)
        ki.append(sor)
    szoveg = '\n'.join(ki)
    if SZAKASZ_6B not in szoveg:
        # F182 (A21, B04): az Alkalmazás szakasz nélküli lapon a 6/b és a két kivezetett rés fejléce a Módszertan elé
        return szoveg.replace('\n## 7. Módszertan és nyitott kérdések', '\n%s\n\n### Alkalmazás és tanítványság\n\n'
                              '### Tanítói egyezés\n\n\n## 7. Módszertan és nyitott kérdések' % SZAKASZ_6B, 1)
    szoveg = szoveg.replace('## 6/b. Alkalmazás és tanítói egyezés\n',
                            '## 6/b. Alkalmazás és tanítói egyezés\n\n### Alkalmazás és tanítványság\n', 1)
    return szoveg.replace('\n## 7. Módszertan és nyitott kérdések', '\n### Tanítói egyezés\n\n'
                          '\n## 7. Módszertan és nyitott kérdések', 1)


def tanitoi_resz_ki(szoveg):
    """F178.4: a nevesített tanítói rész a lapról kikerül (a `tanitoi` rés adata nem változik; a rés sorsa a
    felhasználó döntése, DT-F178b). Az alkalmazás alcíme is kikerül: a 10. szakasz maga az alkalmazás."""
    m = re.search(r'(?m)^### Tanítói egyezés[ \t]*\n', szoveg)
    if m:
        k = re.compile(r'(?m)^## ').search(szoveg, m.end())
        szoveg = szoveg[:m.start()] + (szoveg[k.start():] if k else '')
    return re.sub(r'(?m)^(## 10\. Alkalmazás)\n\n### Alkalmazás és tanítványság[ \t]*\n', r'\1\n', szoveg)


def alkalmazas_resz_ki(szoveg):
    """F182 (A21; F17, B04): az Alkalmazás szakasz az új szerkezetű lapról kikerül, a számozás folyamatos (a Módszertan
    10., az Irodalom 11.: `UJ_CIMCSERE`). Az `alkalmazas` rés kivezetett (`KIVEZETETT_RES_FEJLEC`): a szakaszban csak a
    váz literál fejléce állhat, kézi szöveg nem."""
    m = re.search(r'(?m)^## 10\. Alkalmazás[ \t]*\n', szoveg)
    if not m:
        return szoveg
    k = re.compile(r'(?m)^## ').search(szoveg, m.end())
    torzs = szoveg[m.end():k.start() if k else len(szoveg)]
    if re.sub(r'\*Kézzel írandó\.\*|### Alkalmazás és tanítványság', '', torzs).strip():
        raise ValueError('az Alkalmazás szakasz nem üres: az `alkalmazas` rés sora még áll a res_forras.tsv-ben')
    return szoveg[:m.start()] + (szoveg[k.start():] if k else '')


# --- F182 (A02; F18, B15): a motívum azonosító táblája nyitja a lapot -------------------------------------------------
# A felhasználó (2026-11-09): „ezzel a kolofon résszel induljon az oldal minden esetben”. A tábla a cím után, a Kivonat
# előtt áll, olvasói mezőnevekkel (F18 (d)); a státusz a kiadási állapotból (`adat/kiadasok.tsv`, F18 (c)), nem a
# motívumtábla régi `statusz` mezőjéből. A Kolofonban a kiadási és a forrásadatok maradnak (F18 (e)).
AZONOSITO_MEZOK = (('ID', 'id'), ('Rövid cím', 'ui_cimke'), ('Teljes cím', 'cim'), ('Téma', 'tema'),
                   ('PaRDeS-szint', 'pardes_szint'), ('Státusz', None), ('Meghatározás', 'meghatarozas'),
                   ('Azonosság típusa', 'azonossag_tipusa'),
                   ('Negatív kritérium', 'negativ_kriterium'), ('Fölérendelt fogalom', 'folerendelt_fogalom'))


def kiadasi_statusz(motivum_id, kiadasok=None):
    """A lap olvasói státusza a kiadási állapotból: kiadás-sor nélkül „nincs kiadva — feldolgozás alatt”, különben a
    legutóbbi kiadás száma és dátuma."""
    kiadasok = kolofon_kiadasok(motivum_id) if kiadasok is None else kiadasok
    if not kiadasok:
        return NINCS_KIADVA
    u = kiadasok[-1]
    return '%s. kiadás (%s)' % (u['kiadas'].strip(), (u.get('datum') or '').strip() or EM_DASH)


def _nagy_kezdo(t):
    return t[:1].upper() + t[1:]


# A lap elején „A motívum.” bekezdése azt mondja meg, mi a motívum azonosságának hordozója (CLAUDE.md, az új ID
# négy kérdése, 1.), mert a cím a lap címsorában már áll (lap-javit HAMART-001, lektor 1.: a címismétlés helyett).
AZONOSSAG_OLVASOI = {
    'lexikai': 'Szavas motívum: azonosságát egy szó vagy szócsalád adja, amely minden helyén áll.',
    'formulaikus': 'Fordulat-motívum: azonosságát egy állandó szókapcsolat vagy fordulat adja.',
    'referenciális': 'Utalás-motívum: azonosságát az adja, hogy a helyek ugyanarra a személyre, helyre vagy eseményre '
                     'utalnak.',
    'fogalmi': 'Fogalmi motívum: azonosságát egy fogalom adja, amelyet a helyek különböző szavakkal mondanak ki.',
    'strukturális': 'Szerkezeti motívum: azonosságát nem egyetlen szó adja, hanem egy szerkezet, amelyet több szó '
                    'együtt hordoz.',
}


def egyszerusitett_kolofon(m):
    """A lap elején a motívum három meghatározó adata olvasói alakban (a felhasználó, 2026-11-11: „a motívum
    megfogalmazása / negatív elhatárolás / fölérendelt fogalom ahogy a régiben volt — a legvégén a teljes”; a forma:
    „maradjon a bekezdés”); a technikai mezők (azonosító, téma, PaRDeS-szint, státusz, azonosság típusa) a Kolofonban.
    Lap-javit HAMART-001 (lektor 1., 2., 4.): „A motívum.” az azonosság hordozóját mondja (a cím a címsorban áll); a
    második címke a tartalmát fedi (a negatív kritérium a hely minimális jegye: mi tartozik ide, és mi nem); a
    harmadik zárójele a belső „hígulna” szó nélkül."""
    tipus = (m.get('azonossag_tipusa') or '').strip()
    # a felhasználó (2026-11-11): „hiányolom a motívum definíciót … a kolofonban is és az elején”: a meghatározás
    # (`motivumok.tsv` `meghatarozas`) áll elöl, utána az azonosság típusa egy mondatban
    megh = (m.get('meghatarozas') or '').strip()
    tip = AZONOSSAG_OLVASOI.get(tipus, '' if megh else '%s.' % (m.get('cim') or m['id']).rstrip('.'))
    return '\n\n'.join([
        '**A motívum.** %s' % ' '.join(x for x in (megh, tip) if x),
        '**Mi tartozik ide, és mi nem.** %s' % (m.get('negativ_kriterium') or EM_DASH),
        '**Fölérendelt fogalom** (a tágabb kategória: ha egy hely csak ezen át tartozna ide, kimarad). %s.'
        % _nagy_kezdo((m.get('folerendelt_fogalom') or EM_DASH).rstrip('.')),
        '*Az azonosító és technikai adatok (azonosító, téma, PaRDeS-szint, státusz, azonosság típusa) a '
        '[Kolofonban](#kolofon) állnak.*'])


def azonosito_tabla_beszur(szoveg, m):
    i = szoveg.find('\n## Kivonat\n')
    if i < 0:
        raise ValueError('%s: nincs „## Kivonat” címsor az azonosító tábla helyéhez' % m['id'])
    return szoveg[:i + 1] + egyszerusitett_kolofon(m) + '\n\n' + szoveg[i + 1:]


def _ige_link(hely):
    return '[%s](#%s)' % (hely, _anchor_id(hely))


def _funkcio_magyarazat(funkcio):
    """A `funkcio` mező („🔗 címke — magyarázat”) magyarázata, nagy kezdőbetűvel és ponttal; magyarázat híján a
    címke."""
    f = re.sub(r'^[^\wÁÉÍÓÖŐÚÜŰáéíóöőúüű]+', '', (funkcio or '').strip())
    cimke, _, magy = f.partition(' — ')
    t = (magy or cimke).strip().rstrip('.')
    return (t[:1].upper() + t[1:] + '.') if t else ''


def _lanc_szo_nev(elem):
    """A beépített sor `gerinc_elem`-je olvasói névvel: a Strong-szó („adámá (föld)”), a szópár („kóc + dardar”), a
    tematikus sor („a lánc szavai nélkül”)."""
    if elem.startswith('tematikus'):
        return 'a lánc szavai nélkül (tematikus, nem lexikai kapcsolat)'
    reszek = elem.split('+')
    if all(STRONG_TOKEN_RE.match(r) for r in reszek):
        nevek = []
        for r in reszek:
            lk = lemma_kiejtes(r)
            nevek.append(lemma_cim(lk) if lk else r)
        jel = rovid_jelentes(reszek[0])
        return ' + '.join(nevek) + (' — %s' % jel[0] if jel[1] and len(reszek) == 1 else '')
    return 'szópár: ' + ' + '.join(reszek)


def _konyvresz(hely):
    k = hely.split(' ')[0]
    if k == '1Móz':
        return 'gen'
    return 'usz' if k in OU_USZ_KONYVEK() else 'osz'


_usz_konyvek_cache = None


def OU_USZ_KONYVEK():
    global _usz_konyvek_cache
    if _usz_konyvek_cache is None:
        sorok = [r for r in L.read_tsv(os.path.join(KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'))]
        hu = [r['Magyar rövidítés'] for r in sorok]
        i = next(k for k, r in enumerate(sorok) if r['STEPBible-rövidítés'] == 'Mat')
        _usz_konyvek_cache = set(hu[i:])
    return _usz_konyvek_cache


def _hely_bontas(helyek):
    c = collections.Counter(_konyvresz(h) for h in helyek)
    reszek = [('%d a Genezisben' % c['gen']) if c['gen'] else '',
              ('%d az Ószövetség többi könyvében' % c['osz']) if c['osz'] else '',
              ('%d az Újszövetségben' % c['usz']) if c['usz'] else '']
    reszek = [r for r in reszek if r]
    return ', '.join(reszek[:-1]) + (' és ' if len(reszek) > 1 else '') + reszek[-1] if reszek else ''


TELJESSEG_HALO_NEV = (
    ('strong', 'A szavak minden előfordulása', 'a lánc héber és görög szavai a teljes Ó- és Újszövetségben'),
    ('karoli', 'A magyar szavak', 'a lánc szavainak magyar megfelelői a teljes Károli-fordításban'),
    ('szotar', 'A szótárak idézőhelyei', 'ahol a héber és a görög szótár ezeknél a szavaknál egy verset idéz'),
)


def teljesseg_halok(motivum_id):
    """[(háló, versszám, proveniencia)] a motívum teljesség-méréséből (`naplok/F123_teljesseg_<ID>.tsv`, a
    `teljesseg_meres.py` generált kimenete); a fájl híján üres lista."""
    ut = os.path.join(ROOT, 'naplok', 'F123_teljesseg_%s.tsv' % motivum_id)
    if not os.path.exists(ut):
        return []
    with io.open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    halo = collections.OrderedDict()
    prov = {}
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        halo.setdefault(r['halo'], set()).add(r['igehely'])
        prov.setdefault(r['halo'], r.get('proveniencia', ''))
    return [(h, len(v), prov[h]) for h, v in halo.items()]


def _versek_halmaz(helyek):
    ki = set()
    for h in helyek:
        ki.update(SZKZ.versek(h))
    return ki


_csoport_egyedi_cache = {}


def csoport_egyedi(mid):
    """F182 (A23 kapujának lelete, K34): {a csoportos sor igehelye: (egyedi versszám, [egyedi tagok])}. Egy vers két
    háló csoportjában is állhat (pl. a Károli-szó és a Strong szerinti keresés ugyanazt a tövis-verset); a vers a
    jelöltek döntésnaplójában előbb álló csoportnál számít, a későbbiben nem. Taglista nélkül a sor versszáma marad."""
    if mid not in _csoport_egyedi_cache:
        import nyilt_mag_export as NYM
        jel = [r for r in jeloltek_sorok() if r['id'] == mid]
        kulon = {(r['id'], r['igehely']) for r in jel if 'külön sor' in (r.get('forras_kereses') or '')
                 and not NYM.CSOPORT_RX.match(r.get('indoklas') or '')}
        latott, ki = set(), {}
        for r in jel:
            n = SZKZ.csoport_versszam(r.get('forras_kereses'))
            if n is None or r.get('dontes') not in ('elutasítva', 'nyitva'):
                continue
            _db, tagok = NYM.csoport_tagjai(r, kulon)
            if len(tagok) != n:
                ki[r['igehely']] = (n, None)
                continue
            uj = [t for t in tagok if t not in latott]
            latott.update(uj)
            ki[r['igehely']] = (len(uj), uj)
        _csoport_egyedi_cache[mid] = ki
    return _csoport_egyedi_cache[mid]


def csoport_n(mid):
    return {h: n for h, (n, _t) in csoport_egyedi(mid).items()}


def dontesi_ut_adat(m, sorai):
    """A Döntési út számai (minden vers egyszer): {'bent', 'egyen', 'csoport', 'nyitva', 'osszes', 'csoport_ok',
    'egyen_ok', 'tsk'}. Az egyenként elutasított vers, amely egy beépített sorban is áll, a beépítetteknél számít."""
    mid = m['id']
    minta = SZKZ.okok(mid)
    bent = _versek_halmaz(s['igehely'] for s in sorai)
    egyen = collections.OrderedDict()
    csoport_ok, egyen_ok = collections.Counter(), collections.OrderedDict()
    csoport = nyitva_cs = tsk = 0
    egyedi = csoport_n(mid) if uj_szerkezet(mid) else {}
    for r in jeloltek_sorok():
        if r['id'] != mid or r.get('dontes') not in ('elutasítva', 'nyitva'):
            continue
        n = SZKZ.csoport_versszam(r.get('forras_kereses'))
        if n is not None and r['igehely'] in egyedi:
            n = egyedi[r['igehely']]   # F182 (K34): a más csoportban is álló vers egyszer számít
        fo_ind = (r.get('indoklas') or '').partition(' | ')[0]
        ok = SZKZ.olvasoi_ok(SZKZ.elutasitas_oka(fo_ind, minta)) if r.get('dontes') == 'elutasítva' else None
        if SZKZ.jeloles_oka(r.get('forras_kereses'))[0] in SZKZ.CSOPORTOK[:2]:
            tsk += n or len(SZKZ.versek(r['igehely']))
        if n is not None:
            if ok is None:
                nyitva_cs += n
            else:
                csoport += n
                csoport_ok[ok] += n
            continue
        for v in SZKZ.versek(r['igehely']):
            if v in bent:
                continue
            d = egyen.setdefault(v, [set(), None])
            d[0].add(r.get('dontes'))
            if ok and not d[1]:
                d[1] = ok
    nyitva = nyitva_cs + sum(1 for d in egyen.values() if 'nyitva' in d[0])
    for v, (d, ok) in egyen.items():
        if 'nyitva' not in d and ok:
            egyen_ok.setdefault(ok, []).append(v)
    n_egyen = sum(len(v) for v in egyen_ok.values())
    return {'bent': len(bent), 'egyen': n_egyen, 'csoport': csoport, 'nyitva': nyitva,
            'osszes': len(bent) + n_egyen + csoport + nyitva, 'csoport_ok': csoport_ok, 'egyen_ok': egyen_ok,
            'tsk': tsk, 'pelda': {}}


# --- F182 (A23; F3 módosítva, B14, K39): a kizárt helyek mellékletlapja ------------------------------------------------
# A felhasználó (2026-11-09, a módosított változatra: „mehet”): minden vizsgált, nem beépült vers a saját indokával egy
# generált mellékletlapon áll (`lexikon/[ID]_KIZARASOK.md`), a lapról okonként linkkel. Kapu (HIBA): a melléklet
# igehelyeinek uniója egyenlő a Döntési út csoportos + egyenkénti számával, a csoportonkénti taglista hossza a csoport
# versszámával, és minden igehely a jelöltek döntésnaplójából vagy a teljesség-mérés csoportlistájából jön; eltérésnél
# a melléklet nem renderel, a generálás megáll (nincs kitöltés).
KIZARASOK_UTOTAG = '_KIZARASOK.md'
KIZARASOK_NYITVA_HATAR = 10   # ennyi versig a lista nyitva áll, fölötte csukva (F3 megjelenés)


class MellekletHiba(ValueError):
    pass


def kizarasok_adat(m, sorai):
    """{'csoport': {ok: [igehely, …]}, 'egyen': {ok: [igehely, …]}, 'nyitva': [igehely, …]} a Döntési út szabályával
    (`dontesi_ut_adat`): a csoportos sor tagjai a teljesség-mérés csoportlistájából (`nyilt_mag_export.csoport_tagjai`),
    az egyenkénti versek a jelöltek döntésnaplójából. Kapu: `MellekletHiba` eltérésnél."""
    import nyilt_mag_export as NYM
    mid = m['id']
    a = dontesi_ut_adat(m, sorai)
    minta = SZKZ.okok(mid)
    jel = [r for r in jeloltek_sorok() if r['id'] == mid]
    kulon = {(r['id'], r['igehely']) for r in jel
             if 'külön sor' in (r.get('forras_kereses') or '') and not NYM.CSOPORT_RX.match(r.get('indoklas') or '')}
    csoport = collections.OrderedDict()
    hibak = []
    for r in jel:
        if r.get('dontes') != 'elutasítva':
            continue
        n = SZKZ.csoport_versszam(r.get('forras_kereses'))
        if n is None:
            continue
        ok = SZKZ.olvasoi_ok(SZKZ.elutasitas_oka((r.get('indoklas') or '').partition(' | ')[0], minta))
        n_egyedi, tagok = csoport_egyedi(mid).get(r['igehely'], (n, None))
        if tagok is None:
            hibak.append('%s: a csoport %d versének taglistája nem igazolja a számot' % (r['igehely'], n))
            continue
        csoport.setdefault(ok, []).extend(tagok)
    egyen = collections.OrderedDict((ok, list(vv)) for ok, vv in a['egyen_ok'].items())
    for ok, n in a['csoport_ok'].items():
        if len(csoport.get(ok, [])) != n:
            hibak.append('„%s”: %d vers helyett %d a mellékletben' % (ok, n, len(csoport.get(ok, []))))
    unio = [v for vv in csoport.values() for v in vv] + [v for vv in egyen.values() for v in vv]
    if len(unio) != len(set(unio)):
        hibak.append('%d vers többször áll' % (len(unio) - len(set(unio))))
    if len(set(unio)) != a['csoport'] + a['egyen']:
        hibak.append('a melléklet %d verse ≠ a Döntési út %d csoportos + %d egyenkénti verse'
                     % (len(set(unio)), a['csoport'], a['egyen']))
    bent = _versek_halmaz(s['igehely'] for s in sorai)
    if set(unio) & bent:
        hibak.append('%d beépített vers a mellékletben' % len(set(unio) & bent))
    if hibak:
        raise MellekletHiba('%s: a kizárt helyek melléklete nem renderel — %s' % (mid, '; '.join(hibak)))
    return {'csoport': csoport, 'egyen': egyen, 'a': a}


def _konyvenkent(versek):
    konyvek = collections.OrderedDict()
    for v in sorted(set(versek), key=SZK.vers_kulcs):
        k, h = v.rsplit(' ', 1)
        konyvek.setdefault(k, []).append(h)
    return '\n'.join('- **%s** (%d): %s' % (k, len(hh), ', '.join(hh)) for k, hh in konyvek.items())


def kizarasok_cim(ok, n):
    return '%s — %s vers' % (ok, OK._ezres(n))


def kizarasok_link(mid, ok, n):
    return '%s%s#%s' % (mid, KIZARASOK_UTOTAG, _heading_slug(kizarasok_cim(ok, n)))


def kizarasok_melleklet(m, sorai):
    d = kizarasok_adat(m, sorai)
    mid, a = m['id'], d['a']
    megj = SZKZ.ok_megjegyzesek(mid)
    ki = ['<!-- GENERÁLT: general.py --cel lexikon | melléklet: %s -->' % mid, '',
          '# 📎 %s — Kizárt és vizsgált versek (melléklet)' % mid, '',
          'A [%s lap](%s_TUDOMANYOS.md#1-döntési-út) Döntési útjának melléklete: a motívum %s versén túl megvizsgált, '
          'a motívumhoz nem tartozó mind %s %s vers, okonként, a saját indokával. A csoportosan kizárt verseket gépi '
          'mérés sorolja egy közös okba, az egyenként elutasítottakat egyedi döntés. Egy vers egyszer áll: ha két '
          'keresés csoportjában is szerepel, az elsőnél.'
          % (mid, mid, OK._ezres(a['bent']), _nevelo(str(a['csoport'] + a['egyen'])),
             OK._ezres(a['csoport'] + a['egyen'])), '',
          '**Összeadás:** %s (csoportosan kizárva) + %s (egyenként elutasítva) = %s vers.'
          % (OK._ezres(a['csoport']), OK._ezres(a['egyen']), OK._ezres(a['csoport'] + a['egyen']))]
    for cim, csop in (('Csoportosan kizárt versek, okonként', d['csoport']),
                      ('Egyenként elutasított versek, okonként', d['egyen'])):
        if not csop:
            continue
        ki += ['', '## %s' % cim]
        for ok, vv in sorted(csop.items(), key=lambda x: (-len(x[1]), x[0])):
            ki += ['', '### %s' % kizarasok_cim(ok, len(vv)), '', megj.get(ok) or ok, '']
            lista = _konyvenkent(vv)
            if len(vv) > KIZARASOK_NYITVA_HATAR:
                ki += ['<details>', '<summary>A %s vers</summary>' % OK._ezres(len(vv)), '', lista, '', '</details>']
            else:
                ki.append(lista)
    ki += ['', '*Forrás: a jelöltek döntésnaplója és a teljesség-mérés csoportlistája (a nyílt adatkészletben is: '
           'a kizárások és a csoportos kizárások táblája); generálva: %s.*' % G.TS, '']
    # a felhasználó v8-átnézése (4.): az adatcellák önreferáló „lap” fordulata itt is az olvasói alakban
    return TJ.onref_csere('\n'.join(ki))


def _reszletek(cim, n, szoveg_reszek, nyitva=False):
    return ('<details%s><summary><strong>%s</strong> — %s vers</summary>%s</details>'
            % (' open' if nyitva else '', html_escape(cim), OK._ezres(n), ''.join(szoveg_reszek)))


def html_escape(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _modszertan_nyitott(motivum_id):
    """[(cím, első mondat)] a motívum kézi forrásának „Nyitott kérdések” listájából és a „Vitatott pontok”
    címeiből (a forrás nézete, új adat nincs)."""
    ki = []
    for res in ('ertelmezes', 'modszertan'):
        sor = res_forras_sorok().get((motivum_id, res))
        if not sor or sor.get('forras') != 'tanulmany':
            continue
        try:
            torzs = res_torzs(dict(id=motivum_id), res, sor) or ''
        except Exception:  # noqa: BLE001 — a nézet nem akadályozza a generálást; a hiány a lapon kimondva
            continue
        if res == 'ertelmezes':
            m = re.search(r'(?ms)^### ⚠️ Vitatott pontok\s*\n(.*?)(?=^### |\Z)', torzs)
            for cim, mondat in re.findall(r'(?m)^\*\*([^*]+?)\.?\*\*\s+([^.!?]+[.!?])', m.group(1) if m else ''):
                ki.append((cim.strip(), mondat.strip()))
        else:
            m = re.search(r'(?ms)^### Nyitott kérdések[^\n]*\n(.*?)(?=^### |\Z)', torzs)
            for cim, mondat in re.findall(r'(?m)^\d+\.\s+\*\*([^*]+?)\.?\*\*\s+([^.!?]+[.!?])', m.group(1) if m else ''):
                ki.append((cim.strip(), mondat.strip()))
    return ki


def blokk_dontesi_ut(m, sorai):
    """F178.4: a Döntési út — mit keresünk, hol kerestünk, mi esett ki és miért, mi maradt és miért, határesetek. A
    számok a `jeloltek.tsv` és az `elofordulasok.tsv` soraiból, minden vers egyszer; a keresések versszáma a
    teljesség-mérésből. Csak megjelenítés, új adat nincs (minta: a lapmakett, 2026-11-08)."""
    mid = m['id']
    a = dontesi_ut_adat(m, sorai)
    megj = SZKZ.ok_megjegyzesek(mid)
    karoli = L.load_karoli_1908()
    reszek = []

    # 1.1 A keresés tárgya (DT760: névszói alcím, a K12 harmadik személyű szabálya szerint)
    neg = (m.get('negativ_kriterium') or '').strip()
    neg = SZKZ.olvasoi_indok(neg) or neg
    ide, sep, nem = neg.partition('Nem tartozik ide')
    fol = (m.get('folerendelt_fogalom') or '').strip()
    r1 = ['### 1.1. A keresés tárgya', '**A motívum:** %s.' % (m.get('cim') or mid).rstrip('.')]
    if ide.strip():
        r1.append('**Ami ide tartozik:** %s' % ide.strip())
    if sep:
        r1.append('**Ami nem:** %s%s' % (sep + nem, (' A motívum nem a fölérendelt fogalom: %s.' % fol.rstrip('.'))
                                         if fol else ''))
    elif fol:
        r1.append('**Ami nem:** %s.' % (fol[:1].upper() + fol[1:].rstrip('.')))
    reszek.append('\n\n'.join(r1))

    # 1.2 A keresés forrásai (DT760)
    lanc = []
    for s in sorai:
        for e in (s.get('gerinc_elem') or '').split('+'):
            if STRONG_TOKEN_RE.match(e) and e not in lanc:
                lanc.append(e)
    lanc.sort(key=lambda s: (s[0] != 'H', s))
    szavak = []
    for s in lanc:
        lk = lemma_kiejtes(s)
        jel = rovid_jelentes(s)
        szavak.append('%s%s' % (lemma_cim(lk) if lk else s, (', %s' % jel[0]) if jel[1] else ''))
    r2 = ['### 1.2. A keresés forrásai']
    if szavak:
        r2.append('**A motívum szavai:** %s.' % '; '.join(szavak))
    tabla = ['| Keresés | Vers | Mit nézett |', '|---|---|---|']
    halok = teljesseg_halok(mid)
    nev = {k: (c, d) for k, c, d in TELJESSEG_HALO_NEV}
    for h, n, _p in halok:
        c, d = nev.get(h, (h, ''))
        tabla.append('| %s | %s | %s |' % (c, OK._ezres(n), d))
    if a['tsk']:
        tabla.append('| Kereszthivatkozások ajánlásai | %s | a kereszthivatkozás-gyűjtemények (TSK, Károli) ajánlásai a '
                     'motívum helyeihez |' % OK._ezres(a['tsk']))
    tabla.append('| **Összesen, minden vers egyszer számolva** | **%s** | a keresések és az ajánlások együtt, a motívum '
                 'helyeivel |' % OK._ezres(a['osszes']))
    r2.append('\n'.join(tabla))
    if halok:
        r2.append('*A keresések versszáma a teljesség-mérésből.*%s'
                  % ''.join('<!-- %s -->' % p.replace('--', '—') for _h, _n, p in halok))
    reszek.append('\n\n'.join(r2))

    # 1.3 Mi esett ki és miért
    r3 = ['### 1.3. Mi esett ki és miért',
          '\n'.join(['| Lépés | Vers | Miért |', '|---|---|---|',
                     '| **Megvizsgált versek összesen** | **%s** | az 1.2. lépés minden találata |' % OK._ezres(a['osszes']),
                     '| **Csoportosan kizárva** | **%s** | a keresés találata, de egy közös ok miatt egyik sem tartozik ide '
                     '(%d ok, lent lenyitható) |' % (OK._ezres(a['csoport']), len(a['csoport_ok'])),
                     '| **Egyenként elbírálva és elutasítva** | **%s** | egyenként olvasott versek, mindegyik saját '
                     'indokkal (%d ok, lent lenyitható) |' % (OK._ezres(a['egyen']), len(a['egyen_ok'])),
                     '| **A motívumhoz tartozik** | **%s** | %d hely (a tartomány-soroknál több vers egy helyen) |'
                     % (OK._ezres(a['bent']), len(sorai))]
                    + (['| **Döntésre vár** | **%s** | |' % OK._ezres(a['nyitva'])] if a['nyitva'] else [])),
          '**Összeadás:** %s (a motívumhoz tartozik) + %s (csoportosan kizárva) + %s (egyenként elutasítva)%s = %s '
          'megvizsgált vers. Döntés nélkül maradt vers: %s.'
          % (OK._ezres(a['bent']), OK._ezres(a['csoport']), OK._ezres(a['egyen']),
             (' + %s (döntésre vár)' % OK._ezres(a['nyitva'])) if a['nyitva'] else '', OK._ezres(a['osszes']),
             OK._ezres(a['nyitva']))]
    if a['csoport_ok']:
        r3.append('#### Csoportosan kizárt versek, okonként')
        dd = []
        for ok, n in sorted(a['csoport_ok'].items(), key=lambda x: (-x[1], x[0])):
            pelda = [r['igehely'] for r in jeloltek_sorok()
                     if r['id'] == mid and r.get('dontes') == 'elutasítva'
                     and SZKZ.csoport_versszam(r.get('forras_kereses')) is not None
                     and SZKZ.olvasoi_ok(SZKZ.elutasitas_oka((r.get('indoklas') or '').partition(' | ')[0],
                                                             SZKZ.okok(mid))) == ok][:5]
            p = ['<p>%s</p>' % html_escape(megj.get(ok) or ok)]
            if pelda:
                p.append('<p>Példák (a Károli-szöveggel):</p><ul>%s</ul>'
                         % ''.join('<li>%s: <em>%s</em></li>' % (h, html_escape(karoli.get(h, '')))
                                   for h in pelda if karoli.get(h)))
            if uj_szerkezet(mid):   # F182 (A23): a teljes lista a mellékletlapon, okonként linkkel
                p.append('<p>A csoport %s a <a href="%s">kizárt helyek mellékletében</a> áll.</p>'
                         % ('egyetlen verse' if n == 1 else 'mind a %s verse' % OK._ezres(n),
                            html_escape(kizarasok_link(mid, ok, n))))
            else:
                p.append('<p>A csoport %s a lap nyílt adatkészletében áll.</p>'
                         % ('egyetlen verse' if n == 1 else 'mind a %s verse' % OK._ezres(n)))
            dd.append(_reszletek(ok, n, p))
        r3.append('\n'.join(dd))
    if a['egyen_ok']:
        r3.append('#### Egyenként elutasított versek, okonként')
        dd = []
        for ok, vv in sorted(a['egyen_ok'].items(), key=lambda x: (-len(x[1]), x[0])):
            dd.append(_reszletek(ok, len(vv), ['<p>%s</p>' % html_escape(megj.get(ok) or ok),
                                               '<p>Versek: %s.</p>' % ', '.join(vv)]
                                 + (['<p>A <a href="%s">kizárt helyek mellékletében</a> is.</p>'
                                     % html_escape(kizarasok_link(mid, ok, len(vv)))] if uj_szerkezet(mid) else [])))
        r3.append('\n'.join(dd))
    reszek.append('\n\n'.join(r3))

    # 1.4 Mi maradt és miért
    csop = collections.OrderedDict()
    for s in sorai:
        elem = (s.get('gerinc_elem') or '').strip() or EM_DASH
        csop.setdefault('tematikus' if elem.startswith('tematikus') else elem, []).append(s)
    r4 = ['### 1.4. Mi maradt és miért']
    dd = []
    for elem, ss in csop.items():
        helyek = [s['igehely'] for s in ss]
        tetel = ''.join('<li>%s: %s</li>' % ('<a href="#%s">%s</a>' % (_anchor_id(s['igehely']), s['igehely']),
                                              html_escape(_funkcio_magyarazat(s.get('funkcio'))))
                        for s in ss)
        dd.append('<details open><summary><strong>%s</strong> — %d hely</summary><p>%s.</p><ul>%s</ul></details>'
                  % (html_escape(_lanc_szo_nev(elem)), len(ss),
                     ('%d hely: %s' % (len(ss), _hely_bontas(helyek))) if len(ss) > 1 else
                     ('Egy hely, %s' % _hely_bontas(helyek).split(' ', 1)[1]), tetel))
    r4.append('\n'.join(dd))
    reszek.append('\n\n'.join(r4))

    # 1.5 Határesetek és nyitott kérdések
    r5 = ['### 1.5. Határesetek és nyitott kérdések']
    hatar = [s for s in sorai if (s.get('megbizhatosag') or '').strip() not in ('', 'magas')]
    if hatar:
        r5.append('**Határesetek** (nem magas megbízhatóságú azonosítás): %s.'
                  % ', '.join('%s (%s)' % (_ige_link(s['igehely']), s['megbizhatosag']) for s in hatar))
    nyitott = _modszertan_nyitott(mid)
    if nyitott:
        r5.append('\n'.join('- **%s.** %s' % (c, t) for c, t in nyitott))
        r5.append('A kérdések kifejtése a 10. (Értelmezés) és a 11. szakaszban (Módszertan és nyitott kérdések) áll.')
    if len(r5) == 1:
        r5.append('A motívumnak nincs határesete és nyitott kérdése.')
    reszek.append('\n\n'.join(r5))

    # a felhasználó v8-átnézése (1., 4.): a szakasz alanya a vizsgálat, nem „a lap”
    olv = ('Ez a szakasz azt mutatja meg, hogyan jutott el a vizsgálat az igehelyekig: mit keresett, hol, mi esett ki és '
           'miért, és mi maradt. %s %s megvizsgált versből %s tartozik a motívumhoz; minden vers egyszer számít, így a '
           'számok összeadódnak.' % (OK.nevelo_szam(a['osszes']).capitalize(), OK._ezres(a['osszes']),
                                     OK._ezres(a['bent'])))
    torzs = '\n\n'.join(reszek)
    hatokor = ('A Döntési út: a motívum keresésének és döntéseinek összegzése; a részletek a 2. és a 3. szakaszban.')
    return _lexikon_blokk(mid, 'dontesi_ut', ['adat/jeloltek.tsv', 'adat/elofordulasok.tsv', 'adat/motivumok.tsv',
                                               'adat/elutasitasi_okok.tsv', 'konkordancia/Karoli_1908.tsv'],
                          [LC('projekt_adat'), LC('Karoli_1908')], hatokor, torzs, olv), a


def dontesi_ut_beszur(szoveg, m, blokk):
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % _cel_kulcs(m['id'], 'jelmagyarazat')
    i = szoveg.find(veg)
    if i < 0:
        raise ValueError('%s: nincs Jelmagyarázat-blokk a Döntési út elé' % m['id'])
    i += len(veg)
    return szoveg[:i] + '\n\n## 1. Döntési út\n\n' + blokk + szoveg[i:]


def OU_PROV(p):
    """A proveniencia-sor olvasói rövid alakja (a forrás és a dátum); a teljes sor HTML-megjegyzésben marad."""
    forras = re.search(r'forras=([^|]+)', p or '')
    ts = re.search(r'ts=(\d{4}-\d{2}-\d{2})', p or '')
    nev = olvasoi_forrasnev((forras.group(1) if forras else '').strip())
    return '%s, %s<!-- %s -->' % (nev, ts.group(1) if ts else EM_DASH, (p or '').replace('--', '—'))


# --- F178.4: belső jel olvasói formára (átírás, nem törlés) ------------------------------------------------------
# Az új szerkezetű lapon a belső jelölés (fájlnév, döntés- és feladatazonosító, a blokk technikai kódja, a nyers
# proveniencia-sor) olvasói alakban áll; a nyers proveniencia-sor a sor végén HTML-megjegyzésben megmarad (CLAUDE.md
# 1. szabály: a sor a lap forrásában az állítás mellett áll, az olvasó a forrás nevét és dátumát látja). Az olvasói
# kapu az új szerkezetű lapon kivétel nélkül mér (a technikai dőlt sor, a lábjegyzet, a Kolofon és az Irodalom is).
OLVASOI_FORRASNEV = (
    (r'karoli_strong', 'a', 'Károli–Strong párosítás'),   # F182 (A24): a 4.14 forrása (könyvtár, a párosítás táblái)
    (r'[\w-]*_kereszthivatkozas_naplo\.md', 'a', 'motívum korábbi kereszthivatkozás-naplója'),
    (r'F123_teljesseg_[\w-]+?(?:_blokkok)?\.(?:md|tsv)', 'a', 'lap teljesség-mérése'),
    (r'F123_[\w-]+\.(?:md|tsv|py)', 'a', 'lap munkanaplója'),
    (r'TSK_VERSSZAM_felmeres\.md', 'a', 'kereszthivatkozások versszám-felmérése'),
    (r'teljesseg_meres\.py', 'a', 'teljesség-mérő'),
    (r'bdb_vers_jelentes\.tsv', 'a', 'BDB-szótár versenkénti jelentései'),
    (r'bdb_szakasz_hu\.tsv|bdb_szakaszok\.tsv|BDB_teljes_unabridged\.tsv|BDB_etimologia_kezi_hatarok\.tsv',
     'a', 'BDB-szótár'),
    (r'BDB_rokon_irasok\.tsv', 'a', 'BDB-szótár rokon nyelvi írásai'),
    (r'thayer_vers_jelentes\.tsv|thayer_szakaszok\.tsv|Thayer_teljes\.tsv', 'a', 'Thayer-szótár'),
    (r'elofordulasok\.tsv', 'a', 'motívum előfordulás-táblája'),
    (r'szotar_szakasz_cimke\.tsv', 'a', 'szótári szakaszok címketáblája'),
    (r'lxx_dontesek\.tsv', 'az', 'LXX-fordítói döntések táblája'),
    (r'jeloltek\.tsv', 'a', 'jelöltek döntésnaplója'),
    (r'UBS_DBH_\w+\.tsv', 'az', 'UBS Dictionary of Biblical Hebrew'),
    (r'UBS_DNTG_\w+\.tsv', 'az', 'UBS Dictionary of New Testament Greek'),
    (r'TAHOT_kivonat\.tsv', 'a', 'STEPBible héber szövege (TAHOT)'),
    (r'TAGNT_kivonat\.tsv|TAGNT_valtozatok\.tsv', 'a', 'STEPBible görög szövege (TAGNT)'),
    (r'tW_szocikkek\.tsv', 'a', 'translationWords szócikkei'),
    (r'TBESH\.txt', 'a', 'STEPBible héber rövid szótára (TBESH)'),
    (r'TBESG\.txt', 'a', 'STEPBible görög rövid szótára (TBESG)'),
    (r'forditasok\.tsv', 'a', 'lexikon fordítástáblája'),
    (r'lexikon_hivatkozasok\.tsv', 'a', 'lexikon szótári hivatkozástáblája'),
    (r'tematikus_temak\.tsv', 'a', 'tematikus index döntései'),
    (r'nave_tema_hu\.tsv', 'a', 'Nave-témák magyar nevei'),
    (r'Nave_\w+\.tsv', '', 'Nave tárgymutatója (1897)'),
    (r'glosszak_heber_hu\.tsv', 'a', 'héber glosszák magyar táblája'),
    (r'TSK_kereszthivatkozasok\.tsv', 'a', 'Treasury of Scripture Knowledge'),
    (r'Karoli_kereszthivatkozasok\.tsv', 'a', 'Károli-kereszthivatkozások'),
    (r'Karoli_versmegfeleltetes\.tsv', 'a', 'Károli-versmegfeleltetés'),
    (r'Karoli_1908\.tsv', 'a', 'Károli-fordítás (1908)'),
    (r'karoli_szotari_alak\.tsv', 'a', 'Károli-szavak szótári alakjai'),
    (r'szotar_szerepek\.tsv', 'a', 'szótári pontok rendje'),
    (r'motivum_kapcsolatok\.tsv', 'a', 'motívumközi kapcsolatok táblája'),
    (r'kapcsolatok\.tsv', 'a', 'kapcsolat-tábla'),
    (r'motivumok\.tsv', 'a', 'motívumtábla'),
    (r'LXX_versszintu_parok\.tsv', 'a', 'Septuaginta versszintű szópárjai'),
    (r'(?:LXX_OS/)?[a-z0-9]+(?:-lxx)?\.tsv', 'a', 'Septuaginta szövege'),
    (r'SECE_[HG]_teljes\.tsv', 'a', 'SECE szólista'),
    (r'SDBH_domenek\.tsv', 'az', 'SDBH szemantikai szótár'),
    (r'SDGNT_domenek\.tsv', 'az', 'SDGNT szemantikai szótár'),
    (r'OSHL_lexikalis_index\.tsv', 'az', 'Open Scriptures héber lexikona'),
    (r'MCGED_teljes\.tsv', 'az', 'MCGED görög szótár'),
    (r'tiltott_fordulatok\.tsv', 'a', 'tiltott fordulatok listája'),
    (r'grammatikai_strongok\.tsv', 'a', 'grammatikai szavak listája'),
    (r'res_forras\.tsv', 'a', 'lap réseinek forrástáblája'),
    (r'visszhang_megfelelok\.tsv', 'a', 'visszhang-megfelelők táblája'),
    (r'Targum_PD\.tsv', 'a', 'Targum (közkincs)'),
    (r'Vulgata_Clementina\.tsv', 'a', 'Vulgata (Clementina)'),
    (r'visszhang_tanuk\.tsv', 'a', 'tanúréteg kinyerő táblája'),                                   # F183
    (r'vitatott_forrasok\.tsv', 'a', 'vitatott pontok szakirodalom-táblája'),                       # F183 (K67f)
    (r'SBLGNT_apparatus\.tsv', 'az', 'SBL Greek New Testament apparátusa'),
    (r'TAGNT_valtozatok\.tsv', 'a', 'STEPBible TAGNT változatjegyzéke'),
    (r'Glossa_Ordinaria\.tsv', 'a', 'Glossa Ordinaria (Migne, 1880)'),
    (r'Tanu_atyak_(?:index|mu)\.tsv', 'a', 'HistoricalChristianFaith kommentár-adatbázis (metaadat)'),
    (r'Tanu_rabbinikus_index\.tsv', 'a', 'Sefaria kapcsolat-adata'),
    (r'chain-lineages', 'a', 'Chain Lineage Browser (Blidstein, Inowlocki, Verheyden; a bibliai hivatkozások: BiblIndex, '
                        'Institut des Sources Chrétiennes, CNRS – HiSoMA, Lyon)'),
    (r'motivumok/[\w-]+\.md', 'a', 'motívum kézi forrása'),
    (r'SEMA\.md', 'az', 'adatséma'),
    (r'PaRDeS_gyorsreferencia\.md', 'a', 'PaRDeS-gyorsreferencia'),
    (r'LEXV2_\w+\.md', 'a', 'lapszerkezet leírása'),
    (r'[\w-]+\.py', 'a', 'lap generátora'),
    (r'[\w-]+\.tsv', 'a', 'lap adattáblája'),
    (r'[\w-]+\.txt', 'a', 'lap adatforrása'),
    (r'[\w-]+\.json', 'a', 'lap adatforrása'),
    (r'[\w-]+\.md', 'a', 'lap munkaanyaga'),
)
_FORRASNEV_RX = [(re.compile(r'(?:[\w.-]+/)*(?:' + rx + ')'), nevelo, nev) for rx, nevelo, nev in OLVASOI_FORRASNEV]


def _nevelo_illeszt(elso, nev):
    """A szövegben álló névelő („a”/„A”) és a forrásnév saját névelője egyesítve: a név névelője dönt, a kis- vagy
    nagybetűt a szöveg adja; névelő nélküli névnél a szöveg névelője marad."""
    m = re.match(r'(az?) (.*)$', nev, re.S)
    if not m:
        return '%s %s' % (elso, nev)
    nevelo = m.group(1)
    return '%s %s' % (nevelo.capitalize() if elso.isupper() else nevelo, m.group(2))


def olvasoi_forrasnev(fajl, nevelovel=True):
    """A forrásfájl olvasói neve. A tábla a nevet névelő nélkül tárolja, a névelőt külön (lap-javit HAMART-001,
    orkesztrátori tétel: lista- és táblaelem nem kezdődhet névelővel); a folyó szöveg névelővel kéri
    (`nevelovel=True`), a lista és a tábla névelő nélkül, nagy kezdőbetűvel (`nevelovel=False`)."""
    for rx, nevelo, nev in _FORRASNEV_RX:
        if rx.fullmatch(fajl.strip()):
            if nevelovel:
                return ('%s %s' % (nevelo, nev)) if nevelo else nev
            return _nagy_kezdo(nev)
    return fajl


_dontes_datum_cache = None


_dontes_allapot_cache = None


def ervenyes_dontes(azon):
    """F182 (F27): a lapra csak érvényes döntés kerül — felülírt döntés helyett a felülíró (a `DONTESEK.md` jelölése,
    `dontes_allapot`); érvénytelen, utód nélküli döntésnél maga az azonosító marad (dátum nélkül), és az `ellenoriz.py`
    21. szabálya SÉRTÉS-t ad."""
    global _dontes_allapot_cache
    if _dontes_allapot_cache is None:
        import dontes_allapot as DA
        _dontes_allapot_cache = DA.betolt(ROOT)
    import dontes_allapot as DA
    if azon not in _dontes_allapot_cache:
        return azon
    utod = DA.ervenyes_utod(azon, _dontes_allapot_cache)
    return utod if utod else ''


def dontes_datum(azon):
    """A végleges döntés (DTnnn) dátuma a `DONTESEK.md` sorából (az első dátum a sorban); ismeretlen: ''."""
    global _dontes_datum_cache
    if _dontes_datum_cache is None:
        _dontes_datum_cache = {}
        ut = os.path.join(ROOT, 'DONTESEK.md')
        if os.path.exists(ut):
            with io.open(ut, encoding='utf-8') as f:
                for sor in f:
                    m = re.match(r'^\| (DT\d+) \|', sor)
                    if m:
                        d = re.search(r'(20\d\d)[-.](\d\d)[-.](\d\d)', sor)
                        _dontes_datum_cache[m.group(1)] = ('%s-%s-%s' % d.groups()) if d else ''
    return _dontes_datum_cache.get(azon, '')


_FAJL_RX = re.compile(r'(?<![\w/.-])(?:[\w.-]+/)*[\w-]+\.(?:tsv|py|md|txt|json)\b(?:\s*§\s*([\w/]+))?')
_PROV_RX = re.compile(r'scope=[^`<]*?(?:ts=[\dT:Z.-]+|(?=`)|$)')
# F182 (2. fázis; F22, H4, F24 (c)): a generátor közös szövegeinek munkaszavai az új szerkezetű lapon olvasói alakban (a régi
# lapok szövege változatlan, E28). A tiltott szavak listája egy helyen: `olvasoi_kapu.MUNKASZAVAK` (a MUNKASZO kapu).
UJ_OLVASOI_MUNKASZO = (
    (re.compile(r'\*\(üres blokk: .*?; a hiány nincs kitöltve gyenge vagy asszociatív anyaggal\)\*'),
     '*(Ennél a pontnál a lap nem közöl adatot; a hiányt nem tölti ki gyenge vagy asszociatív anyaggal.)*'),
    (re.compile(r'\*\(kutatói jelölés: a szakaszhatár horgonnyal illesztve, ellenőrzendő\)\*'),
     '*(a magyar szakaszhatár gépi illesztésű)*'),
    (re.compile(r'(?:kutatói|az) azonosítás függőben'), 'a megfelelő nincs megállapítva'),
    (re.compile(r'azonosításra vár'), 'megállapítatlan'),
    (re.compile(r'\*\(nincs G-token\)\*'), '*(nincs görög szó)*'),
    # a fájlnév olvasói névre cseréje után maradó kettőzött névelő („Generált a a kapcsolat-tábla”) és a mezőnév
    (re.compile(r'\b(Generált) a (?=a )'), r'\1 '),
    (re.compile(r'\bindoklas mezőjéből\b'), 'indoklás mezőjéből'),
    (re.compile(r'\b(Strong-)?token(\w*)'), lambda m: _token_olvasoi(m.group(1), m.group(2))),
    (re.compile(r'négyforrásos audit a napló §7 szerint, retroaktív\s+betöltés'),
     'négy forrás összevetése a motívum korábbi kereszthivatkozás-naplójában, utólagos betöltés'),
    # F182 javítókör (ELLENOR_F182 #5, #6): a napló-szakasz utalása („(7. rész)”, „(4/b. rész)”) és a nyers mezőnevek,
    # -értékek (`csatorna=cli`, `szamozas_elteres`, `forras_kereses`) olvasói alakja; a kapu: `olvasoi_kapu.NYERS_JELEK`
    (re.compile(r'\s*\(\d+(?:/[a-z])?\. rész\)'), ''),
    (re.compile(r'\s*[|·]\s*csatorna=\w+'), ''),
    (re.compile(r'\bszamozas_elteres\b'), 'versszámozás miatt nem párosítva'),
    (re.compile(r'\s*\(forras_kereses: ([^)]*)\)'), r' (a keresés forrása: \1)'),
    (re.compile(r'\bforras_kereses\b'), 'a keresés forrása'),
)
_TOKEN_RAG = {'': 'szó', 'je': 'szava', 'jét': 'szavát', 'jei': 'szavai', 'jeihez': 'szavaihoz', 'enként': 'szavanként',
              're': 'szóra', 'hez': 'szóhoz', 'ek': 'szavak', 'sorrend': 'szósorrend'}
_STRONG_TOKEN_RAG = {'': 'Strong-szám', 'je': 'Strong-száma', 'jét': 'Strong-számát', 'jei': 'Strong-számai',
                     'jeihez': 'Strong-számaihoz', 'ek': 'Strong-számok'}


def _token_olvasoi(strong, rag):
    """F182 (F22): a „token” munkaszó olvasói alakja (a „Strong-token” a Strong-szám, a puszta „token” a szó)."""
    tabla = _STRONG_TOKEN_RAG if strong else _TOKEN_RAG
    return tabla.get(rag, ('Strong-szám' if strong else 'szó') + rag)


_ZSARGON = (
    (re.compile(r'Forrás-study'), 'Kézi forrás'),
    (re.compile(r'\bstudy-j?\w*'), 'tanulmány'),
    (re.compile(r'\bstudy\b'), 'tanulmány'),
    (re.compile(r'-scan\b'), '-keresés'),
    (re.compile(r'\bscan\w*'), 'keresés'),
    (re.compile(r'\bLXX_OS\b'), 'a Septuaginta szövege'),
    (re.compile(r'\bforrásfájlonként\b'), 'forrásonként'),
    (re.compile(r'\bforrásfájl(\w*)'), r'forrás\1'),
    (re.compile(r'"([^"\n]{1,200})"'), r'„\1”'),
)
_DT_RX = re.compile(r'(?<![\w-])DT-?F?\d+[a-z]{0,2}\b')
_TETEL_RX = re.compile(r'(?<![\w/.#-])(?:F\d{1,3}(?:\.[\w-]+)*|N-F\d+[a-z]{0,2}|N\d{1,3})\b|(?<![\w&/])#\d{2,3}\b')
_KOD_RX = re.compile(r'\s?\((?:G\d+|R\d(?:\.\d+)?)(?:[,;][^)]*)?\)')


def _prov_olvasoi(p):
    forras = re.search(r'forras=([^|]+)', p)
    ts = re.search(r'ts=(\d{4}-\d{2}-\d{2})', p)
    nevek = []
    for f in re.split(r'[+,;]\s*', (forras.group(1) if forras else '').strip()):
        f = re.sub(r'\s*\(.*$', '', f).strip()
        if not f:
            continue
        nev = olvasoi_forrasnev(f) if _FAJL_RX.fullmatch(f) else None
        if nev and nev not in nevek:
            nevek.append(nev)
    if 'scope=manual' in p and 'kézi szerkesztés' not in nevek:
        nevek.append('kézi szerkesztés')
    return 'forrás: %s%s' % ('; '.join(nevek) or 'a lap munkaanyaga', (', %s' % ts.group(1)) if ts else '')


IGAZOLAS_OLVASOI = {
    'TAHOT-igazolt': 'a héber szöveg (TAHOT) igazolja', 'TAGNT-igazolt': 'a görög szöveg (TAGNT) igazolja',
    'TAHOT-hatokoron-kivul': 'a héber szöveg (TAHOT) hatókörén kívül', 'nincs': 'szövegigazolás nélkül',
}


def _olvasoi_resz(t):
    """Egy védett elemek nélküli szövegrész olvasói átírása."""
    t = _PROV_RX.sub(lambda m: _prov_olvasoi(m.group(0)), t)
    # F182 (A08, K05): a kézi forrású sor („proveniencia: forrás: kézi szerkesztés, …”) is olvasói alakra
    t = re.sub(r'^(:\s*)proveniencia: (‹\w+›|forrás: [^|]+?) \| igazolas: ([\w-]+) \| jelentés-címke: ',
               lambda m: '%sForrás: %s · %s · a jelentés címkéje: ' % (m.group(1), _forras_elotag_nelkul(m.group(2)),
                                                                        IGAZOLAS_OLVASOI.get(m.group(3), m.group(3))), t)
    t = re.sub(r'^(:\s*)proveniencia: (‹\w+›|forrás: [^|]+?) \| igazolas: ([\w-]+)',
               lambda m: '%sForrás: %s · %s' % (m.group(1), _forras_elotag_nelkul(m.group(2)),
                                                IGAZOLAS_OLVASOI.get(m.group(3), m.group(3))), t)
    t = re.sub(r'\bsorszam\b', 'sorszám', t)
    # F182 (A08, K42): a lábjegyzet nem „… sorszám 12, 23”, és nem hoz nyers mezőnevet
    t = re.sub(r'(?<=\S) sorszám \d+(?:, \d+)*(?=\))', '', t)
    t = t.replace('előfordulás-táblája jelentes_szam', 'előfordulás-táblájában a jelentésszám')
    t = re.sub(r'\bjelentes_szam\b', 'jelentésszám', t)
    # F182 (K05): a dőlt forrássor címkéje olvasói („Forrás:”), a nyers mezőnév („Proveniencia:”) nélkül
    t = re.sub(r'\bProveniencia: (`?)forrás: ', r'\1Forrás: ', t)
    t = re.sub(r'\(proveniencia: (`?)forrás: ', r'(\1forrás: ', t)
    t = t.replace('az `adat/jeloltek.tsv`-n át', 'a jelöltek döntésnaplóján át')
    t = re.sub(r'\bkaroli_szo\b', 'a Károli-szó mezője', t)
    import nyilt_mag_export as NYM   # F178.6: „szerkesztői döntés” — a lapon és a nyílt magban ugyanaz a csere
    t = NYM.szerkesztoi(t)
    t = re.sub(r'kutatói hozzárendelés', 'szerkesztői hozzárendelés', t)
    t = re.sub(r'kutatói jelentésszám', 'szerkesztői jelentésszám', t)
    t = re.sub(r'a `?\[ID: [\w-]+\]`? motívum', 'a motívum', t)
    t = re.sub(r'`?\[ID: ([\w-]+)\]`?', r'\1', t)
    t = re.sub(r'\b[Aa]z?\s+`?LXX_OS`?-\w+', 'a Septuaginta szövegével', t)
    # a ragozott fájlnév („az `elofordulasok.tsv`-ből”): a név zárójeles forrásmegjelölésként, rag és névelő nélkül
    t = re.sub(r'(?:\b[Aa]z?\s+)?`?((?:[\w.-]+/)*[\w-]+\.(?:tsv|py|md|txt|json))`?-[a-záéíóöőúüű]+',
               lambda m: '(forrás: %s)' % olvasoi_forrasnev(m.group(1)), t)
    # lap-javit HAMART-001 (névelő-tétel): a névelővel álló fájlnév („az `adat/SEMA.md` szerint”) helyén a forrásnév a
    # saját névelőjével áll, nem kettőzve („az az adatséma” helyett „az adatséma”); a mondatkezdő nagybetű marad
    t = re.sub(r'\b([Aa])z?\s+`?((?:[\w.-]+/)*[\w-]+\.(?:tsv|py|md|txt|json))\b`?(?!-)',
               lambda m: _nevelo_illeszt(m.group(1), olvasoi_forrasnev(m.group(2))), t)
    # F182 javítókör (ELLENOR_F182 #5): a fájl szakaszjele („§7”) napló-utalás, az olvasói szövegben nem áll
    t = _FAJL_RX.sub(lambda m: olvasoi_forrasnev(m.group(0).split('§')[0].strip()), t)
    t = _DT_RX.sub(lambda m: 'szerkesztői döntés' + ((', ' + dontes_datum(ervenyes_dontes(m.group(0))))
                                                      if dontes_datum(ervenyes_dontes(m.group(0))) else ''), t)
    t = _TETEL_RX.sub('', t)
    t = _KOD_RX.sub('', t)
    t = t.replace('`', '')
    for rx, uj in _ZSARGON:
        t = rx.sub(uj, t)
    t = re.sub(r'\bmanual\b', 'kézi szerkesztés', t)
    for rx, uj in UJ_OLVASOI_MUNKASZO:
        t = rx.sub(uj, t)
    t = re.sub(r'Szótári gerinc\b', 'Szótári tagolás', t)
    t = re.sub(r'\bgerinc-?elem\w*', 'a motívum szava', t)
    t = re.sub(r'\bgerinc\w*', 'szótári tagolás', t)
    # takarítás: a fájlnevekből lett azonos forrásnév egyszer („a Septuaginta szövege, a Septuaginta szövege”)
    t = re.sub(r'((?:az?|a) [^,()]{3,60}?)(?:, \1)+(?=[,)])', r'\1', t)
    # takarítás: üres zárójel, kettőzött elválasztó
    for _ in range(3):
        t = re.sub(r'\(\s*[;,·]?\s*\)', '', t)
        t = re.sub(r'\(\s*[;,·]\s*', '(', t)
        t = re.sub(r'\s*[;,·]\s*\)', ')', t)
        t = re.sub(r'(?:\s·){2,}\s', ' · ', t)
        t = re.sub(r';\s*;', ';', t)
        t = re.sub(r',\s*,', ',', t)
        t = re.sub(r'(?<=\S)[ \t]{2,}', ' ', t)
        t = re.sub(r'(?<=\S)\s+([,.;:)])', r'\1', t)
    return t


def _forras_elotag_nelkul(x):
    return x[len('forrás: '):] if x.startswith('forrás: ') else x


_VEDETT_RX = re.compile(r'<!--.*?-->|\]\([^)]*\)|<[^>]+>|\[\^[^\]]+\]')


def olvasoi_sor(sor):
    reszek, utolso = [], 0
    for m in _VEDETT_RX.finditer(sor):
        reszek.append(_olvasoi_resz(sor[utolso:m.start()]))
        reszek.append(m.group(0))
        utolso = m.end()
    reszek.append(_olvasoi_resz(sor[utolso:]))
    return ''.join(reszek)


def olvasoi_atiras(szoveg):
    """F178.4: a lap minden látható sora olvasói alakban (a kódblokk, a HTML-megjegyzés, a címsor és a
    GENERÁLT-jelölő érintetlen); a proveniencia-sor nyers alakja a sor végén megjegyzésben megmarad."""
    ki, kod = [], False
    for sor in szoveg.split('\n'):
        if sor.strip().startswith('```'):
            kod = not kod
            ki.append(sor)
            continue
        if kod or not sor.strip() or sor.lstrip().startswith('<!--') or sor.startswith('#'):
            ki.append(sor)
            continue
        uj = olvasoi_sor(sor)
        if uj != sor and ('scope=' in sor or re.match(r'^\[\^[^\]]+\]:\s*(?:forrás|proveniencia)', sor)):
            uj += '<!-- eredeti: %s -->' % sor.replace('--', '—')
        ki.append(uj)
    return '\n'.join(ki)


# --- F182 (a kész lap követelménylistája, `sablonok/KESZ_LAP_KOVETELMENY.md` (a)): az új szerkezetű lap közös szövegeinek
# olvasói alakja. A régi lapok szövege változatlan (E28); a csere csak itt, az új szerkezetű lapon fut.
UJ_JELMAGYARAZAT_CSERE = (
    # A26 (L66): belső „tanulmány”-utalás és nem magyar mondat
    ('az alábbi táblákban a motívum\nsaját study-jából átvett megnevezéssel szerepel.',
     'az alábbi táblákban a motívum\nkézi forrásában rögzített megnevezés áll.'),
    # A26 (L84), K05: a látható szövegben olvasói forrásnév és dátum áll, a nyers sor csak a lap forrásában
    ('**Proveniencia-sor** (dőlt, `scope=… | forras=… | ts=…` alakú): honnan és mikor származik a fölötte álló adat — milyen\n'
     'körre (`scope`), melyik adattáblából vagy lekérdezésből (`forras`), mikor (`ts`); a `manual` kézi rögzítést jelöl. Az\n'
     'ellenőrzéshez való, olvasáskor átugorható.',
     '**Forrásmegjelölés** (dőlt sor vagy a tábla alatti számozott jegyzet, „forrás: …” alakú): melyik adattáblából vagy\n'
     'lekérdezésből és mikor származik a fölötte álló adat; a „kézi szerkesztés” kézi rögzítést jelöl. A tábla sorában a\n'
     'jegyzet száma áll (pl. 2.5); az azonos jegyzet a tábla alatt egyszer szerepel, és több sor is mutathat rá. A teljes,\n'
     'gépi alakú forrássor a forrásfájlban, megjegyzésként áll. Az ellenőrzéshez való, olvasáskor átugorható.'),
    # a felhasználó átnézése (2.): a közös forrásmegjelölés jele (‹E1› …) a jegyzetekben nem áll, a feloldása a rejtett
    # megjegyzésben; a jelmagyarázata ezért nem áll a lapon
    ('\n\n**Közös forrásmegjelölés** (‹E1›, ‹K1›, ‹M1› …): ha egy blokk több sora ugyanabból a forrásból jön, a soron csak a jel\n'
     'áll, a teljes proveniencia-sor egyszer, a blokk alatt. Az előtag a blokkot jelöli: E az előfordulások, K a kizárt és\n'
     'vizsgált helyek, M a minősítés.', ''),
    # a lektor és a Fable közös véleménye (4.): a 9. szakasz tanúinak rövidítése
    ('(Septuaginta), MT (Masoretic Text), KJV (King James Version).',
     '(Septuaginta), MT (Masoretic Text), KJV (King James Version), HCF (HistoricalChristianFaith\nCommentaries Database, '
     'az egyházatyai tanúk adatbázisa; a „HCF: 373” alakban a szám az adatbázisban\na szerzőhöz rendelt évszám).'),
)


# F182 javítókör (ELLENOR_F182 #7): a mondatközi kisbetűsítés nem bántja a mozaikszót („LXX-híd”) és a tulajdonnevet
# („Károli-megfelelők”); a tulajdonnevek listája a szerepnevekben álló nevek.
KISBETU_TULAJDONNEV = ('Károli', 'Septuaginta', 'Strong', 'Thayer', 'Vulgata', 'Targum', 'Nave', 'Pesitta', 'BDB', 'TSK')


def kisbetus_kezdes(s):
    """A szöveg első betűje kisbetűvel, kivéve, ha az első szó (kötőjelig) mozaikszó (legalább két nagybetű) vagy
    tulajdonnév (`KISBETU_TULAJDONNEV`)."""
    if not s:
        return s
    elso = re.match(r'[^\s\-–/(]+', s)
    szo = elso.group(0) if elso else ''
    if sum(1 for c in szo if c.isupper()) >= 2 or szo in KISBETU_TULAJDONNEV:
        return s
    return s[0].lower() + s[1:]


def szotari_pontok_jelmagyarazat():
    """F182 (A09; F8 (4)): a 4. szakasz pontrendszerének magyarázata a Jelmagyarázatban (a szóbevezető helyett), a
    szerepmátrix (`adat/szotar_szerepek.tsv`) sorrendjében és neveivel; a 4.11 a visszhang-blokk."""
    nevek = {int(r['sorrend']): szerep_megjelenitett(r['szerep']).strip() for r in szerepek_sorok() if r['nyelv'] == 'gorog'}
    nevek[11] = 'Visszhang: ókori fordítások (a 9. szakaszban)'
    pontok = '; '.join('4.%d %s' % (n, kisbetus_kezdes(nevek[n])) for n in sorted(nevek))
    return ('**A szótári pontok** (4. Szótári háttér): szavanként számozott pontok követik egymást, mindegyik egy kérdésre '
            'felel: %s. A 4.1–4.10 nyelvenként, szavanként áll, a 4.11–4.14 a motívum egészére vonatkozik.' % pontok)


def kesz_lap_elotte(szoveg, m, sorai):
    for regi, uj in UJ_JELMAGYARAZAT_CSERE:
        if regi not in szoveg:
            raise ValueError('a Jelmagyarázat cserélendő szövege nincs a lapon: %r' % regi[:60])
        szoveg = szoveg.replace(regi, uj, 1)
    jel = '\n\n**Olvasói bevezető** — '
    if jel not in szoveg:
        raise ValueError('a Jelmagyarázat „Olvasói bevezető” bekezdése nincs a lapon')
    return szoveg.replace(jel, '\n\n' + szotari_pontok_jelmagyarazat() + jel, 1)


# F182 (A08, K42; az orkesztrátor lelete, 2026-11-11): a kizárt (k) és a minősített (mj) jelöltek lábjegyzete a jelölés
# nyers forrását (`forras_kereses`), a régi napló-hivatkozást („napló: … (4/b. rész)”), a nyers indoklást és a belső
# keresési jelet (halo=, blokk=, lanc, csalad) hozta. Az olvasói alak a forrás olvasói nevét és a döntést adja; a nyers
# sor a lábjegyzet végén, megjegyzésben megmarad (CLAUDE.md 1. szabály).
_LJ_JELOLT_RX = re.compile(r'^(\[\^(?:k|mj)\d+\]: )(forrás: .*?)(<!--.*)?$')


def _strong_olvasoi(m):
    st = m.group(1)
    return _szo_irassal(st) if lemma_kiejtes_szabaly(st) else st


def jelolt_labjegyzet_olvasoi(t):
    t = re.sub(r' · indoklás \(nyers\): .*?(?= · |$)', '', t)
    t = re.sub(r';\s*napló: [^|·]*?(?=\s*[|·]|$)', '', t)
    t = re.sub(r' · a döntés nyoma: szótári tagolás(?= · |$)', '', t)
    t = t.replace('a döntés nyoma: · ', 'a döntés nyoma: ').replace('a döntés nyoma:', 'döntés:')
    t = re.sub(r'TSK (\d?[A-ZÁÉÍÓÖŐÚÜŰ]\w* [\d:,\- ]+?) \(([\d, \-]+)\)', r'TSK-ajánlás (\1; szavazat: \2)', t)
    t = re.sub(r'\bKároli-KH is\b', 'a Károli-kereszthivatkozás is', t)
    t = re.sub(r'U1 teljesség-mérés, ([^,]+?)[- ]háló(?: \([^)]*\))?, blokk-sor \([^)]*\): (\d+) vers, a sor igehelye a '
               r'blokk egy verse; a lista: .*?(?=\s\|\s|\s·\s|$)',
               r'teljesség-mérés (\1 szerinti keresés), csoportos sor: \2 vers; a sor igehelye a csoport egy verse, a csoport minden '
               r'verse a kizárt helyek mellékletében áll', t)
    t = re.sub(r'\blanc ±1\b', 'lánc-keresés (két lánc-szó egy versben vagy a szomszédos versben)', t)
    t = re.sub(r'\bcsalad ([HG]\d{4}[a-z]?)', lambda m: 'szócsalád-keresés: ' + _strong_olvasoi(m), t)
    t = re.sub(r'\bkeresés: ([HG]\d{4}[a-z]?)(?: \([^)]*\))?', lambda m: 'Strong-keresés: ' + _strong_olvasoi(m), t)
    t = re.sub(r'\s+\|\s+', ' · ', t)
    return t


def kesz_lap_utana(szoveg, m, sorai):
    ki = []
    for sor in szoveg.split('\n'):
        mm = _LJ_JELOLT_RX.match(sor)
        if mm:
            sor = mm.group(1) + jelolt_labjegyzet_olvasoi(mm.group(2)) + (mm.group(3) or '')
        ki.append(sor)
    # F182 (F6 (2), F10 (6)): a szónézet linkje olvasói szöveggel, a nyers útvonal („szónézet: /szo/G1311”) nélkül
    szoveg = SZONEZET_NYERS_RX.sub(r'[szónézet](\1)', '\n'.join(ki))
    # F182 (A17; F10 (5), K54): a BDB-fej nyers előtagja („H7451. ra ' ”) és a címszó belső számlálója („רַע‎_226”) nélkül
    szoveg = BDB_FEJ_NYERS_RX.sub(r'\1', szoveg)
    return BDB_SZAMLALO_RX.sub('', szoveg)


BDB_FEJ_NYERS_RX = re.compile(r'(\*\*A szócikk feje \(nyelvi háttér\)\.\*\* )[HG]\d{1,4}[a-z]?\. [^֐-׿יִ-ﭏ\[\n]*?'
                              r'(?=(?:[IV]+\. )?\[?[֐-׿יִ-ﭏ])')
BDB_SZAMLALO_RX = re.compile(r'(?:(?<=[֐-׿יִ-ﭏ\]‎])‎?|(?<=Qal)|(?<=[`\']al)|(?<=[`\']el)|(?<=[`\']il)|'
                             r'(?<=Hiphil)|(?<=Hophal)|(?<=Niphal))_\d+(?=[\s,;.)\]])')


SZONEZET_NYERS_RX = re.compile(r'\[szónézet: (/szo/[HG]\d{4}[a-z]?)\]\(\1\)')


# --- lap-javit HAMART-001 (orkesztrátori tétel, a felhasználó: „pedig ezt külön megjelöltük”): lista- és
# táblaelem nem kezdődik névelővel. A forrásnév a táblában névelő nélkül tárolódik (`olvasoi_forrasnev`); az adatból
# jövő leíró cella vagy listaelem eleji kisbetűs „a”/„az” névelője itt marad le, és az elem nagy kezdőbetűt kap. A
# mondatkezdő, nagybetűs „A”/„Az” (pl. számozott kérdéslista) marad. Kapu: `olvasoi_kapu.py` LISTA_NEVELO.
# ELLENOR_HAMART_lapjavit 4.: a mondat értékű elem (legalább NEVELO_MONDAT_SZO szó) a névelőt megtartja, nagy
# kezdőbetűvel („A szótár a héber … szerint idézi”); a kódblokk belseje és az inline kód védett.
_NEVELO_ELEM_RX = re.compile(r'^((?:\*\*|\*|\[)?)(a|az)\s+(?=\S)')
_LISTAELEM_RX = re.compile(r'^(\s*(?:[-*]|\d+\.)\s+)(.*)$')
_KOMMENT_RX = re.compile(r'<!--.*?-->')
NEVELO_MONDAT_SZO = 6


def _nevelo_nelkul(e):
    m = _NEVELO_ELEM_RX.match(e)
    if not m:
        return e
    rest = e[m.end():]
    if len(_KOMMENT_RX.sub('', rest).split()) >= NEVELO_MONDAT_SZO:
        return m.group(1) + m.group(2).capitalize() + ' ' + rest
    return m.group(1) + (rest[:1].upper() + rest[1:] if rest[:1].isalpha() else rest)


def nevelo_le(szoveg):
    ki, komment, kod = [], False, False
    for sor in szoveg.split('\n'):
        t = sor.strip()
        if t.startswith('```'):
            kod = not kod
            ki.append(sor)
            continue
        if kod:
            ki.append(sor)
            continue
        if komment:
            komment = '-->' not in sor
            ki.append(sor)
            continue
        if t.startswith('<!--'):
            komment = '-->' not in sor
            ki.append(sor)
            continue
        megj = []

        def _ment(mm):
            megj.append(mm.group(0))
            return '\x00%d\x00' % (len(megj) - 1)
        vedett = _KOMMENT_RX.sub(_ment, sor)
        if vedett.strip().startswith('|') and not re.match(r'^\s*\|[\s:|-]+\|\s*$', vedett):
            cellak = re.split(r'(?<!\\)\|', vedett)
            for i in range(1, len(cellak) - 1):
                c = cellak[i]
                bal = c[:len(c) - len(c.lstrip())]
                jobb = c[len(c.rstrip()):]
                cellak[i] = bal + _nevelo_nelkul(c.strip()) + jobb
            vedett = '|'.join(cellak)
        else:
            m = _LISTAELEM_RX.match(vedett)
            if m:
                vedett = m.group(1) + _nevelo_nelkul(m.group(2))
        ki.append(re.sub('\x00(\\d+)\x00', lambda mm: megj[int(mm.group(1))], vedett))
    return '\n'.join(ki)


def uj_szerkezet_alkalmaz(szoveg, m, sorai):
    """F178: a kész (régi szerkezetű) lapból az új szerkezet — Döntési út, új számozás, tanítói rész nélkül,
    olvasói átírás. Csak az UJ_LAPSZERKEZET motívumain fut."""
    blokk, _adat = blokk_dontesi_ut(m, sorai)
    szoveg = dontesi_ut_beszur(szoveg, m, blokk)
    szoveg = alkalmazas_resz_ki(tanitoi_resz_ki(uj_cimek_alkalmaz(szoveg).replace(
        '## 10. Alkalmazás\n\n### Alkalmazás és tanítványság', '## 10. Alkalmazás')))
    szoveg = szoveg.replace(
        'hogy egy nevesített magyarázó egy helyet ténylegesen hogyan olvasott,\nazt a Tanítói egyezés dokumentálja, '
        'ahol van.', 'nevesített magyarázók olvasata itt nem\nszerepel; az ókori fordítások és értelmezők olvasatát a '
        '9. szakasz mutatja.')
    szoveg = attekinto_beszur(szoveg, m, sorai)
    szoveg = visszhang_beszur(szoveg, m, sorai)
    szoveg = rokon_tabla_48(szoveg, m)
    szoveg = hatastortenet_athelyez(szoveg, m, sorai)   # F183
    szoveg = szakirodalom_beszur(szoveg, m)             # F183 (K67f)
    szoveg = azonosito_tabla_beszur(szoveg, m)
    szoveg = kesz_lap_elotte(szoveg, m, sorai)
    return nevelo_le(kesz_lap_utana(olvasoi_atiras(szoveg), m, sorai))


# --- F178.4: áttekintő tábla a Szótári háttér (4. szakasz) elején ------------------------------------------------
# A felhasználó jóváhagyásával (2026-11-08, „mehet”): szavanként egy sor — kiejtés, alapjelentés, LXX-megfelelő, a
# helyek száma. Csak megjelenítés, új adat nincs: az alapjelentés a 4.1 pont rövid jelentése (`rovid_jelentes`), a
# LXX-megfelelő a 4.6 pont versszintű párjaiból (héber szónál a leggyakoribb görög társ, görög szónál a motívum
# leggyakoribb héber társa; versszintű együtt-előfordulás, nem szóillesztés), a helyek száma a motívum soraiból.
ATTEKINTO_CIM = '### Áttekintés: a motívum szavai'


_lxx_g_versek_cache = None


def _lxx_g_versek():
    """{G-Strong: versszám} a teljes LXX_OS-ben (a Dice-társítás nevezője)."""
    global _lxx_g_versek_cache
    if _lxx_g_versek_cache is None:
        versek = {}
        for fn in sorted(os.listdir(LXX_OS_DIR)):
            if not fn.endswith('.tsv'):
                continue
            with io.open(os.path.join(LXX_OS_DIR, fn), encoding='utf-8') as f:
                fej = None
                for sor in f:
                    if sor.startswith('#') or not sor.strip():
                        continue
                    c = sor.rstrip('\r\n').split('\t')
                    if fej is None:
                        fej = c
                        continue
                    d = dict(zip(fej, c))
                    s = d.get('strong') or ''
                    if s.isdigit():
                        versek.setdefault('G%04d' % int(s), set()).add(d.get('igehely_lxx') or d.get('igehely_karoli'))
        _lxx_g_versek_cache = {g: len(v) for g, v in versek.items()}
    return _lxx_g_versek_cache


def _dice(h, g):
    e = lxx_versszintu_parok().get(h)
    if not e:
        return 0.0, 0
    k = sum(1 for gs in e['versek'].values() if g in (gs or []))
    return (2.0 * k / (len(e['versek']) + _lxx_g_versek().get(g, k))) if k else 0.0, k


def _lxx_tars(strong, motivum_hebr):
    """A LXX-megfelelő a versszintű párokból, Dice-társulással (a leggyakoribb szavak — γῆ, λέγω, κύριος — így nem
    nyernek a puszta együtt-előfordulással; ugyanaz a mérce, mint a visszhang kinyerő tábla LXX-oszlopa)."""
    parok = lxx_versszintu_parok()
    if strong.startswith('H'):
        e = parok.get(strong)
        if not e:
            return EM_DASH
        jeloltek = {g for gs in e['versek'].values() for g in set(gs or [])}
        pont = sorted(((_dice(strong, g), g) for g in jeloltek), key=lambda x: -x[0][0])
        if not pont or pont[0][0][0] < 0.05:
            return EM_DASH
        (d, k), g = pont[0]
        lk = lemma_kiejtes(g)
        return '%s · %d vers' % (lemma_cim(lk) if lk else g, k)
    pont = sorted(((_dice(h, strong), h) for h in motivum_hebr), key=lambda x: -x[0][0])
    if not pont or pont[0][0][0] < 0.05:
        return EM_DASH
    (d, k), h = pont[0]
    lk = lemma_kiejtes(h)
    return 'héberül: %s · %d vers' % (lemma_cim(lk) if lk else h, k)


def attekinto_tabla(sorai):
    tokenek = motivum_strong_tokenek(sorai)
    hebr = [t for t in tokenek if t.startswith('H')]
    sorok = ['| Szó (kiejtés) | Alapjelentés | LXX-megfelelő | Helyek a motívumban |', '|---|---|---|---|']
    for t in sorted(tokenek, key=lambda s: (s[0] != 'H', s)):
        lk = lemma_kiejtes(t)
        n = sum(1 for s in sorai if t in (s.get('strong') or '').split('+'))
        jel = rovid_jelentes(t)
        sorok.append('| %s | %s | %s | %d |' % (lemma_cim(lk) if lk else t, jel[0] if jel[1] else EM_DASH,
                                               _lxx_tars(t, hebr), n))
    return '\n'.join(sorok), len(tokenek)


def attekinto_beszur(szoveg, m, sorai):
    tabla, n = attekinto_tabla(sorai)
    if not n:
        return szoveg
    i = szoveg.find('## 4. Szótári háttér')
    if i < 0:
        return szoveg
    j = re.compile(r'(?m)^### (?:Görög|Héber) szavak').search(szoveg, i)
    if not j:
        return szoveg
    betet = '\n\n'.join([
        ATTEKINTO_CIM,
        # a lektor és a Fable közös véleménye (3.): a cella társulási mércével választ, nem gyakorisággal
        olvasoi_bekezdes('A motívum %d szava egy táblában: a kiejtés, a rövid alapjelentés, a görög fordítás '
                         '(Septuaginta) az a szava, amely a héber szó verseiben a legjellemzőbben áll vele együtt (a '
                         'társulás mértéke szerint, nem a puszta gyakoriság szerint), és hogy hány helyen áll a szó a '
                         'motívumban. A részletek szavanként a 4.1–4.10 pontban.' % n),
        tabla,
        # F182 (A25, K51): a lábjegyzet megmondja, mit mér az oszlop a 4.11 láncbeli megfelelőjéhez képest
        '*Az LXX-megfelelő versszintű együtt-előfordulás (a 4.6 pont párjai, Dice-társulással), nem szóillesztés, és a '
        'szó minden ószövetségi versén mér, nem csak a motívum helyein; a motívum láncverseiben álló görög megfelelőt '
        'a 9. szakasz (Hatástörténet) ószövetségi táblázata adja, ezért a kettő eltérhet.%s*'
        % (' A „—” alapjelentés: a rövid magyar jelentés még nincs lefordítva.' if re.search(r'(?m)^\| [^|]+ \| — \|', tabla)
           else ''), ''])
    return szoveg[:j.start()] + betet + '\n' + szoveg[j.start():]


def visszhang_beszur(szoveg, m, sorai):
    """F178.5: a 4.11 visszhang-blokk (a kinyerő tábla soraiból); adat nélkül a blokk nem áll a lapon."""
    blokk = blokk_visszhang(m, sorai)
    if not blokk:
        return szoveg
    k = re.compile(r'(?m)^#### 4\.12\. ').search(szoveg)
    if not k:
        return szoveg
    return szoveg[:k.start()] + blokk + '\n\n' + szoveg[k.start():]


# ---------------------------------------------------------------------------

# --- F178.5: a visszhang-blokk (4.11) -----------------------------------------------------------------------------
# DT639 (a felhasználó jóváhagyásával, 2026-11-08): lánc-szavanként egy sor, az azonosság (`n/N`) a fő tartalom, a cella a
# fordítás szava kiejtéssel; betoldás-sor; a „Mit mutat” lelettel kezd. A következtetés szabálya (DT-F178d, szerkesztői
# döntés, „Mehet”, 2026-11-08): az n/N mellé alapvonal — hogyan adja vissza ugyanaz a fordító ugyanazt a héber szót a
# láncon kívül. A LXX-nél gépi (a héber szó összes ószövetségi versében a görög vers lemmái, `LXX_versszintu_parok`, a
# szócsalád szerint); a Targumnál és a Vulgatánál szóillesztés nincs, az alapvonal nem mérhető, a következtetés óvatos.
# Kiemelt visszhang csak (a) ha a fordító két különböző héber lánc-szót egy szóval / szócsaláddal ad vissza, vagy (b) ha
# a láncban más szót választ, mint máshol (alacsony alapvonal). Ha a láncbeli szó a szokásos fordítás (magas alapvonal):
# „a lánc egysége megmarad, de ez önmagában nem lelet”. Csak az `adat/visszhang_megfelelok.tsv` ellenőrzött soraiból.
VISSZHANG_TSV = os.path.join(ADAT, 'visszhang_megfelelok.tsv')
VISSZHANG_FORRASOK = (('targum', 'Targum'), ('vulgata', 'Vulgata'), ('lxx', 'LXX'))
VISSZHANG_NEV = {'targum': 'a Targum', 'vulgata': 'a Vulgata', 'lxx': 'a LXX'}
ALAPVONAL_SZOKASOS = 0.80   # a láncon kívüli versek legalább ennyi részében ugyanaz a szócsalád: szokásos fordítás
ALAPVONAL_RITKA = 0.40      # ennél ritkábban a láncon kívül: a láncban választott szó (kiemelt visszhang, (b))
ROKON_NYELVEK = ('asszír', 'akkád', 'arab', 'etióp', 'szír', 'arámi', 'óarámi', 'ugariti', 'Tell el-Amarna',
                 'sabeus')   # az arámi: a BDB „Aramaic” alakja; a targumi (ᵑ7) sor nem rokon nyelvi háttér
SZAMSZO_VH = {2: 'két', 3: 'három', 4: 'négy', 5: 'öt'}

_bdb_rokon_szocikk_cache = None


def bdb_rokon_szocikk(strong):
    """A rokon írások gyorsítótárának (`BDB_rokon_irasok.tsv`) `# lekérdezve:` sora szerint hány BDB-szócikket
    azonosított a lekérdezés a Strongra; None, ha a Strongot nem kérdezték le."""
    global _bdb_rokon_szocikk_cache
    if _bdb_rokon_szocikk_cache is None:
        _bdb_rokon_szocikk_cache = {}
        ut = os.path.join(KONKORDANCIA, 'BDB_rokon_irasok.tsv')
        if os.path.exists(ut):
            with io.open(ut, encoding='utf-8') as f:
                for sor in f:
                    m = re.match(r'# lekérdezve: (H\d+) \|.*bdb_szócikk=(\d+)', sor)
                    if m:
                        _bdb_rokon_szocikk_cache[m.group(1)] = int(m.group(2))
    return _bdb_rokon_szocikk_cache.get(strong)


def bdb_helyi_szocikk(strong):
    """A helyi BDB-szöveg (`BDB_teljes_unabridged.tsv`) tartalmaz-e szócikket a Strongra."""
    with io.open(os.path.join(KONKORDANCIA, 'BDB_teljes_unabridged.tsv'), encoding='utf-8') as f:
        return any(sor.startswith(strong + '\t') for sor in f)


def visszhang_sorok(motivum_id):
    if not os.path.exists(VISSZHANG_TSV):
        return []
    _, sorok = G.tsv_beolvas(VISSZHANG_TSV)
    return [r for r in sorok if r['motivum'] == motivum_id]


def _gorog_tovek(lemma):
    t = ''.join(c for c in unicodedata.normalize('NFD', lemma.lower()) if not unicodedata.combining(c))
    tovek, sor = set(), [t]
    while sor:
        x = sor.pop()
        gyerek = [x[len(e):] for e in ('επι', 'κατα', 'κατ', 'δια', 'δι', 'συν', 'εκ', 'απο', 'προ')
                  if x.startswith(e) and len(x) > len(e) + 2]
        if gyerek:
            sor.extend(gyerek)   # az előtagos alak eleje („κατ”) nem tő: csak az előtag nélküli alaké (F178 javítókör)
        else:
            tovek.add(x[:3])
    return frozenset(tovek)


def _vh_csalad(forras, lemma):
    if forras == 'lxx':
        return _gorog_tovek(lemma)
    return frozenset([unicodedata.normalize('NFC', lemma.strip())])


def _vh_szo(forras, r):
    lemma = r['lemma'].split(' · ')[0]
    if forras == 'targum':
        ki = HK.kiejt(lemma, aram=True)
        return '%s (%s)' % (lemma, ki) if ki else lemma
    if forras == 'lxx':
        return '%s (%s)' % (lemma, r['kiejtes'].split(' · ')[0]) if r['kiejtes'] else lemma
    return '*%s*' % lemma


def _rovid_hely(h):
    return h.split(' ', 1)[1] if h.startswith('1Móz ') else h


_lxx_lemma_cache = None


def _lxx_lemma():
    """{G-Strong: lemma} a LXX_OS-ből (az alapvonal szócsaládjához)."""
    global _lxx_lemma_cache
    if _lxx_lemma_cache is None:
        _lxx_lemma_cache = {}
        for fn in sorted(os.listdir(LXX_OS_DIR)):
            if not fn.endswith('.tsv'):
                continue
            with io.open(os.path.join(LXX_OS_DIR, fn), encoding='utf-8') as f:
                fej = None
                for sor in f:
                    if sor.startswith('#') or not sor.strip():
                        continue
                    c = sor.rstrip('\r\n').split('\t')
                    if fej is None:
                        fej = c
                        continue
                    d = dict(zip(fej, c))
                    s = d.get('strong') or ''
                    if s.isdigit():
                        _lxx_lemma_cache.setdefault('G%04d' % int(s), d.get('lemma', ''))
    return _lxx_lemma_cache


_tahot_glossza_cache = {}
_GLOSSZA_STOP = {'they', 'were', 'will', 'shall', 'have', 'that', 'with', 'from', 'your', 'them', 'their', 'this',
                 'there', 'which', 'been', 'what', 'when', 'also', 'into', 'upon', 'unto'}


def tahot_glosszak(strong):
    """{Károli-vers: [angol tükörfordítás]} a TAHOT-ból egy Strongra (a láncbeli jelentés és az alapvonal szűrője)."""
    if strong not in _tahot_glossza_cache:
        d = {}
        with io.open(os.path.join(KONKORDANCIA, 'TAHOT_kivonat.tsv'), encoding='utf-8') as f:
            fej = None
            for sor in f:
                if sor.startswith('#') or not sor.strip():
                    continue
                c = sor.rstrip('\r\n').split('\t')
                if fej is None:
                    fej = c
                    i_h, i_s, i_g = fej.index('Igehely'), fej.index('Strong-szám'), fej.index('Angol tükörfordítás')
                    continue
                if len(c) > i_g and c[i_s] == strong:
                    d.setdefault(c[i_h], []).append(c[i_g])
        _tahot_glossza_cache[strong] = d
    return _tahot_glossza_cache[strong]


def _glossza_tovek(glosszak):
    return {w[:4] for g in glosszak for w in re.findall(r'[a-z]+', g.lower()) if len(w) >= 4 and w not in _GLOSSZA_STOP}


def lxx_alapvonal(heber, csalad, lanc_versek):
    """(arány, versszám): a héber szó láncon kívüli ószövetségi verseinek hány részében áll a görög versben a
    szócsalád valamely lemmája (versszintű együtt-előfordulás, `LXX_versszintu_parok.tsv`). Csak a láncbeli jelentés
    előfordulásai számítanak: a vers TAHOT-tükörfordítása a láncversekével közös szótövet hordoz (a kálal 8:21-es
    ’átkoz’ Piélje így nem keveredik a ’könnyűnek lenni’ Qaljával)."""
    e = lxx_versszintu_parok().get(heber)
    if not e:
        return None, 0
    lemma = _lxx_lemma()
    tg = tahot_glosszak(heber)
    lanc_tovek = _glossza_tovek(g for v in lanc_versek for g in tg.get(v, []))
    kivul = [gs for v, gs in e['versek'].items() if v not in lanc_versek
             and (not lanc_tovek or _glossza_tovek(tg.get(v, [])) & lanc_tovek)]
    if not kivul:
        return None, 0
    van = sum(1 for gs in kivul if any(_gorog_tovek(lemma.get(g, '')) & csalad for g in (gs or []) if lemma.get(g)))
    return van / len(kivul), len(kivul)


def visszhang_cella(forras, sorok_f, versek):
    """(cella, n, N, a fő szócsalád, a fő lemmák, eltérő helyek, különböző szavak száma)."""
    N = len(versek)
    jo = {r['igehely']: r for r in sorok_f if r['ellenorzes'] and r['alak']}
    # ellenőrzött, alak nélküli sor: a fordításban nincs megfelelő szó (kimondva, nem kitöltve)
    ures = {r['igehely'] for r in sorok_f if r['ellenorzes'] and not r['alak']}

    def hiany(h):
        if h in ures:
            return 'nincs megfelelő szó'
        if any(r['igehely'] == h for r in sorok_f):
            return 'nincs ellenőrzött adat'
        return 'a megfelelő kinyerése még nem történt meg'
    csal = collections.OrderedDict()
    for h in versek:
        r = jo.get(h)
        if not r:
            continue
        c = _vh_csalad(forras, r['lemma'].split(' · ')[0])
        kulcs = next((k for k in csal if k & c), c)
        csal.setdefault(kulcs, []).append(h)
    if not csal:
        # a hiány kimondva, nem kitöltve: kinyerés nélkül „még nem történt meg”, ellenőrizetlen sorral „nincs
        # ellenőrzött adat” (a Targum és a Vulgata kinyerése a motívum lezárásának lépése, MUNKAMENET C-vh)
        return ('nincs ellenőrzött adat' if sorok_f else 'a megfelelő kinyerése még nem történt meg'), \
            0, N, None, [], versek, 0
    fo, helyek = max(csal.items(), key=lambda x: len(x[1]))
    n = len(helyek)
    lemmak = list(dict.fromkeys(jo[h]['lemma'].split(' · ')[0] for h in helyek))
    szo = ' · '.join(dict.fromkeys(_vh_szo(forras, jo[h]) for h in helyek))
    tobbi = [h for h in versek if h not in helyek]
    if n == 1 and len(csal) == len(jo) and N > 1:
        return ('%s különböző szó: %s' % (SZAMSZO_VH.get(len(jo), str(len(jo))),
                                          '; '.join('%s %s' % (_rovid_hely(h), _vh_szo(forras, jo[h]))
                                                    for h in versek if h in jo)), 1, N, None, [], tobbi, len(jo))
    if n == N:
        return '%s · %d/%d' % (szo, n, N), n, N, fo, lemmak, [], len(csal)
    elteres = '; '.join('%s %s' % (_rovid_hely(h), _vh_szo(forras, jo[h]) if h in jo else hiany(h)) for h in tobbi)
    if all(h in jo for h in tobbi):
        cimke = 'egy versben más szó' if len(tobbi) == 1 else 'más szó'
    else:
        cimke = 'egy versben' if len(tobbi) == 1 else '%s versben' % SZAMSZO_VH.get(len(tobbi), str(len(tobbi)))
    return '%s · %d/%d; %s: %s' % (szo, n, N, cimke, elteres), n, N, fo, lemmak, tobbi, len(csal)


TORZS_MAGYAR = {"Pi'el": 'Piél', "Niph'al": 'Nifál', "Hiph'il": 'Hifíl', "Hithpa'el": 'Hitpaél', "Pu'al": 'Puál',
                "Hoph'al": 'Hofál', 'Qal': 'Qal'}
_bdb_vers_torzs_cache = None


def bdb_vers_torzs(strong, vers):
    """A BDB törzse (Qal, Pi'el …) a versben a `bdb_vers_jelentes.tsv` szerint; None, ha nincs vagy több."""
    global _bdb_vers_torzs_cache
    if _bdb_vers_torzs_cache is None:
        _bdb_vers_torzs_cache = {}
        _, sorok = G.tsv_beolvas(os.path.join(ADAT, 'bdb_vers_jelentes.tsv'))
        for r in sorok:
            t = (r.get('utvonal') or '').split('/')[0]
            if t:
                _bdb_vers_torzs_cache.setdefault((r['strong'], r['karoli_vers']), set()).add(t)
    t = _bdb_vers_torzs_cache.get((strong, vers)) or set()
    return next(iter(t)) if len(t) == 1 else None


def lanc_szo_jelentes(strong, versek):
    """A lánc-szó jelentése a láncban: a rövid jelentés, kivéve, ha a láncversekben a BDB más törzset ad (nem Qal) —
    akkor a TAHOT-tükörfordítás igéjének magyar glosszája a projekt glosszáriumából (`glosszak_heber_hu.tsv`, „to X”),
    a törzs nevével („megátkozni (Piél)”: a kálal 8:21). Adat híján a rövid jelentés."""
    alap = rovid_jelentes(strong)
    torzsek = {bdb_vers_torzs(strong, v) for v in versek}
    if len(torzsek) != 1 or not (torzsek <= set(TORZS_MAGYAR) - {'Qal'}):
        return alap[0] if alap[1] else ''
    torzs = torzsek.pop()
    angol = [g for v in versek for g in tahot_glosszak(strong).get(v, [])]
    szavak = [w for g in angol for w in re.findall(r'[a-z]+', g.lower()) if w not in _GLOSSZA_STOP and len(w) >= 4]
    _, gl = G.tsv_beolvas(os.path.join(ADAT, 'glosszak_heber_hu.tsv'))
    for w in szavak:
        hu = collections.Counter(r['glossza_hu'] for r in gl if r.get('glossza_hu')
                                 and (r.get('glossza_en') or '').strip() == 'to ' + w)
        if hu:
            return '%s (%s)' % (hu.most_common(1)[0][0], TORZS_MAGYAR.get(torzs, torzs))
    return alap[0] if alap[1] else ''


def _heber_kulcs(szo):
    """A héber szó összevetési alakja: NFC, a kantillációs jelek (U+0591–U+05AF) és a meteg nélkül."""
    szo = unicodedata.normalize('NFD', szo or '')
    return unicodedata.normalize('NFC', ''.join(c for c in szo if not ('\u0591' <= c <= '\u05af' or c == '\u05bd')))


def strong_valtozat_versben(strong, versek):
    """A Strong-szám betűs változata (TBESH `H2403a` / `H2403b`), amely a versekben ténylegesen áll (ELLENOR_F178_2 3.):
    a TAHOT szótöve (`Szótő`) a versben, összevetve a változatok TBESH-lemmájával. Egy változat vagy azonosítás híján
    maga a Strong-szám (a `lemma_kiejtes` alapváltozatra esik vissza)."""
    pontos, _ = tbesg_tbesh_index()
    valtozatok = [k for k in pontos if len(k) == len(strong) + 1 and k.startswith(strong) and k[-1].isalpha()]
    if len(valtozatok) < 2 or not versek:
        return strong
    idx = tahot_vers_index()
    tovek = {_heber_kulcs(r.get('Szótő')) for v in versek for r in idx.get(v, []) if r['Strong-szám'] == strong}
    talalt = [k for k in sorted(valtozatok)
              if any(_heber_kulcs(x.strip()) in tovek for x in pontos[k][0].split(','))]
    return talalt[0] if len(talalt) == 1 else strong


def _lanc_szo_cim(strong, versek=None):
    """A lánc-szó címe a 4.11-ben és a BDB-háttérben: a lemma a láncversek saját Strong-változatából (ELLENOR_F178_2
    3.: 1Móz 4:7 → H2403b חַטָּאת, nem az alapváltozat חַטָּאָה-ja), kiejtéssel és a láncbeli jelentéssel."""
    reszek = []
    for s in strong.split('+'):
        lk = lemma_kiejtes(strong_valtozat_versben(s, versek or []))
        reszek.append(lemma_cim(lk) if lk else s)
    jel = lanc_szo_jelentes(strong.split('+')[0], versek or [])
    return ' · '.join(reszek) + ((' — %s' % jel) if jel else '')


def _alapvonal_mondat(alap):
    """Az alapvonal sávja szerinti mondatrész (DT-F178d): ≥ 80% szokásos, 40–80% gyakori, < 40% választott. A mondat a
    nevezőt és a találatot külön mondja (ELLENOR_F178 5.): „a láncon kívüli N versből x versben (y%)” — a régi
    „a versek y%-ában (N vers)” alak a nevezőt találatszámnak mutatta."""
    pct = int(round(alap[0] * 100))
    N = alap[1]
    x = int(round(alap[0] * N))
    if alap[0] >= ALAPVONAL_SZOKASOS:
        return 'szokas', 'a láncon kívüli %d versből %d versben (%d%%) is ez áll: a szó szokásos fordítása, a lánc ' \
                         'egysége megmarad, de ez önmagában nem lelet' % (N, x, pct)
    if alap[0] >= ALAPVONAL_RITKA:
        return 'gyakori', 'a láncon kívüli %d versből %d versben (%d%%) áll ez: a szó gyakori, de nem kizárólagos ' \
                          'fordítása' % (N, x, pct)
    return 'ritka', 'a láncon kívüli %d versből csak %d versben (%d%%) áll ez: a láncban más szót választ, mint ' \
                    'máshol' % (N, x, pct)


def _visszhang_mondat_lxx(eredm):
    n, N, lemmak, alap = eredm['n'], eredm['N'], eredm['lemmak'], eredm['alap']
    if not n:
        return 'A LXX: %s.' % eredm['cella']
    # a lelet (n/N, a szó vagy a szócsalád) a cellában áll; a mondat csak az alapvonalat mondja (ismétlés nélkül)
    if n < N:
        mas, hianyzo = eredm.get('mas', N - n), eredm.get('hianyzo', 0)
        reszek = []
        if mas:
            reszek.append('egy versben más szó' if mas == 1 else '%d versben más szó' % mas)
        if hianyzo:
            reszek.append('%s nincs ellenőrzött adat' % ('egy versben' if hianyzo == 1 else '%d versben' % hianyzo))
        return 'LXX: %s.' % '; '.join(reszek)
    if alap[0] is None:
        return 'LXX: a héber szó a láncon kívül nem fordul elő, az alapvonal nem mérhető.'
    sav, resz = _alapvonal_mondat(alap)
    if len(lemmak) > 1:
        resz = resz.replace(': a szó ', ': a szócsalád ')
    return ('**LXX: %s.**' if sav == 'ritka' else 'LXX: %s.') % resz


def _egyesites_mondat(f, s1, s2, e1, e2):
    """A két héber lánc-szó egy szóval / szócsaláddal (DT-F178d, pontosítva): kiemelt csak alapvonallal."""
    nevek = '%s és %s' % (_szo_nev(s1.split('+')[0]).split(' ', 1)[1], _szo_nev(s2.split('+')[0]).split(' ', 1)[1])
    Nev = VISSZHANG_NEV[f][:1].upper() + VISSZHANG_NEV[f][1:]
    csal = len(set(e1['lemmak'] + e2['lemmak'])) > 1
    if f != 'lxx':
        return '%s a láncban mindkét héber szót (%s) ugyanazzal a szóval adja vissza; hogy máshol is így fordítja-e, ' \
               'ebből a forrásból nem mérhető.' % (Nev, nevek)
    alap = [x['alap'] for x in (e1, e2)]
    if any(a[0] is None for a in alap):
        return '%s mindkét héber szót (%s) ugyanazzal a %s adja vissza; a láncon kívül nem mérhető.' % (
            Nev, nevek, 'szócsaláddal' if csal else 'szóval')
    pct = ', '.join('%s %d%%' % (n, int(round(a[0] * 100))) for n, a in zip(nevek.split(' és '), alap))
    if all(a[0] >= ALAPVONAL_SZOKASOS for a in alap):
        return '%s mindkét héber szót (%s) ugyanazzal a %s adja vissza; ez a láncon kívül is így van (%s).' % (
            Nev, nevek, 'szócsaláddal' if csal else 'szóval', pct)
    if any(a[0] < ALAPVONAL_RITKA for a in alap):
        return '**%s mindkét héber szót (%s) ugyanazzal a %s adja vissza, a láncon kívül viszont nem így (%s): a ' \
               'láncban választott egység.**' % (Nev, nevek, 'szócsaláddal' if csal else 'szóval', pct)
    return '%s mindkét héber szót (%s) ugyanazzal a %s adja vissza; a láncon kívül gyakran, de nem kizárólag (%s).' % (
        Nev, nevek, 'szócsaláddal' if csal else 'szóval', pct)


TORA_KONYVEK = ('1Móz', '2Móz', '3Móz', '4Móz', '5Móz')
NINCS_TARGUM = 'nincs Targum-forrás (az Onkelos csak a Mózes-könyveket fedi)'
_LANC_MAG_RE = re.compile(r'\baz? (\S+) (\d+)[–-](\d+)\.? láncára\b')


def _pesat_sor(s):
    """A motívum Pesat-sora: a `pardes_szint` mezőben a Peshat szint áll (önmagában vagy összetételben)."""
    return 'peshat' in (s.get('pardes_szint') or '').lower()


def lanc_mag(m, sorai=()):
    """(könyv, első fejezet, utolsó fejezet): a motívum Pesat-gerince, az adatból (DT-F178g; ELLENOR_F178_2 1.):
    1. ha a motívum negatív kritériuma megnevezi a láncot („az 1Móz 3–9 láncára utal vissza”), az;
    2. különben a motívum Pesat-sorainak (`pardes_szint` ∋ Peshat) fejezet-tartománya az első Pesat-sor könyvében;
    3. Pesat-sor nélkül None (nincs lánc, a 4.11 nem renderel — üres eredmény, nem kitöltés).
    Rögzített szakasz (a régi „genezisi mag”, a teljes 1Mózes) nincs. A láncversek a gerinc versei közül csak a
    motívum saját versei (`lanc_szavak`) — nem a szó teljes előfordulása a gerincben."""
    k = _LANC_MAG_RE.search(m.get('negativ_kriterium') or '')
    if k:
        return (k.group(1), int(k.group(2)), int(k.group(3)))
    pesat = [v for s in sorai if _pesat_sor(s) for v in igehely_lista(s.get('igehely') or '')]
    if not pesat:
        return None
    konyv = pesat[0].split(' ')[0]
    fej = [int(v.split(' ', 1)[1].split(':')[0]) for v in pesat if v.split(' ')[0] == konyv]
    return (konyv, min(fej), max(fej))


def _magban(vers, mag):
    konyv, _, hely = vers.partition(' ')
    return konyv == mag[0] and mag[1] <= int(hely.split(':')[0]) <= mag[2]


def lanc_szavak(m, sorai):
    """DT-F178g (ELLENOR_F178 2., ELLENOR_F178_2 1.): a 4.11 lánca a motívumadatból, nem a kinyerő tábla soraiból.
    Lánc-szó (a lánc kulcsszava): a motívum beépített sorainak `gerinc_elem`-értéke, ha egyetlen héber Strong (a
    szópár, a `tematikus:` és a görög elem nem lánc-szó) — ez nem az 1.2 teljes szólistája. Láncvers: a motívum
    Pesat-gerincének (`lanc_mag`) azon verse, amely a motívum saját verse (a beépített sorok versei, a tartomány
    versenként), és amelyben a kulcsszó a héber szövegben (TAHOT) áll; a gerincen kívüli helyek a lánc bibliai
    visszhangjai, nem láncversek.
    Visszaad: ([(strong, [láncversek])], mag); gerinc nélkül ([], None)."""
    szavak = []
    for s in sorai:
        g = (s.get('gerinc_elem') or '').strip()
        if re.fullmatch(r'H\d{4}', g) and g not in szavak:
            szavak.append(g)
    mag = lanc_mag(m, sorai)
    if mag is None:
        return [], None
    versek = []
    for s in sorai:
        for v in igehely_lista(s['igehely']):
            if v not in versek and _magban(v, mag):
                versek.append(v)
    idx = tahot_vers_index()
    ki = []
    for g in szavak:
        vv = [v for v in versek if any(r['Strong-szám'] == g for r in idx.get(v, []))]
        if vv:
            ki.append((g, vv))
    return ki, mag


def blokk_visszhang(m, sorai):
    sorok = visszhang_sorok(m['id'])
    lanc = [r for r in sorok if r['forras'] in ('targum', 'vulgata', 'lxx')]
    szolista, mag = lanc_szavak(m, sorai)
    if not lanc or not szolista:
        return ''
    szavak = [s for s, _ in szolista]
    lanc_versek = collections.OrderedDict(szolista)
    minden_lancvers = {v for vv in lanc_versek.values() for v in vv}
    betoldas_kulcs = {(r['strong'], r['igehely']) for r in lanc if r['betoldas'] == 'igen'
                      and r['strong'] in szavak and r['igehely'] in minden_lancvers}
    eredmeny = {}
    for s in szavak:
        versek = lanc_versek[s]
        ss = [r for r in lanc if r['strong'] == s and r['igehely'] in versek and (s, r['igehely']) not in betoldas_kulcs]
        for f, _nev in VISSZHANG_FORRASOK:
            fv = [v for v in versek if f != 'targum' or v.split(' ')[0] in TORA_KONYVEK]
            kivul = [v for v in versek if v not in fv]
            tobbi, sf = [], [r for r in ss if r['forras'] == f]
            if not fv:
                c, n, N, fo, lemmak, kul = NINCS_TARGUM, 0, 0, None, [], 0
            else:
                c, n, N, fo, lemmak, tobbi, kul = visszhang_cella(f, sf, fv)
                if kivul:
                    c += '; %s: %s' % (', '.join(_rovid_hely(h) for h in kivul), NINCS_TARGUM)
            alap = (None, 0)
            if f == 'lxx' and fo is not None and n == N:
                alap = lxx_alapvonal(s.split('+')[0], fo, set(versek))
            # az eltérő versek: más szó (ellenőrzött sor alakkal) vagy adat nélkül — a mondat a kettőt nem keveri
            mas = sum(1 for h in tobbi if any(r['igehely'] == h and r['ellenorzes'] and r['alak'] for r in sf))
            eredmeny[(s, f)] = {'cella': c, 'n': n, 'N': N, 'fo': fo, 'lemmak': lemmak, 'kulonbozo': kul, 'alap': alap,
                                'mas': mas, 'hianyzo': len(tobbi) - mas}
    # két különböző héber lánc-szó egy szóval / szócsaláddal: a mondat az első szó sorában, a másodikban utalás
    egyesites, utal = {}, {}
    for f, _nev in VISSZHANG_FORRASOK:
        for i, s1 in enumerate(szavak):
            for s2 in szavak[i + 1:]:
                e1, e2 = eredmeny[(s1, f)], eredmeny[(s2, f)]
                if e1['fo'] is not None and e2['fo'] is not None and e1['n'] == e1['N'] and e2['n'] == e2['N'] \
                        and e1['fo'] & e2['fo'] and (s1, f) not in egyesites and (s2, f) not in utal:
                    egyesites[(s1, f)] = _egyesites_mondat(f, s1, s2, e1, e2)
                    utal[(s2, f)] = s1
    tabla = ['| Lánc-szó · versek | Targum | Vulgata | LXX | Mit mutat |', '|---|---|---|---|---|']
    teljes = collections.Counter()
    # lektor 25.: egyetlen versen a következetesség nem mérhető, az egyverses szó a számlálásból kimarad
    egyverses = [s for s in szavak if len(lanc_versek[s]) < 2]
    for s in szavak:
        cellak, mondatok = [], []
        for f, _nev in VISSZHANG_FORRASOK:
            e = eredmeny[(s, f)]
            cellak.append(e['cella'])
            if e['N'] and e['n'] == e['N'] and s not in egyverses:
                teljes[f] += 1
            if (s, f) in egyesites:
                mondatok.append(egyesites[(s, f)])
            elif (s, f) in utal:
                cel = 'l. %s sorát' % _szo_nev(utal[(s, f)].split('+')[0])
                if cel not in mondatok:
                    mondatok.append(cel[:1].upper() + cel[1:] + '.')
            elif f == 'lxx':
                mondatok.append(_visszhang_mondat_lxx(e))
        mondatok = list(dict.fromkeys(mondatok))
        # a Targum és a Vulgata egyező egyesítés-mondata egy mondatban (ismétlés nélkül)
        tv = [x for x in mondatok if x.startswith(('A Targum a láncban', 'A Vulgata a láncban'))]
        if len(tv) == 2 and tv[0].split(' ', 2)[2] == tv[1].split(' ', 2)[2]:
            mondatok = ['A Targum és a Vulgata ' + tv[0].split(' ', 2)[2]] + [x for x in mondatok if x not in tv]
        tabla.append('| %s<br>%s | %s | %s |' % (_lanc_szo_cim(s, lanc_versek[s]),
                                               ', '.join(_rovid_hely(h) for h in lanc_versek[s]),
                                               ' | '.join(cellak), ' '.join(mondatok)))
    for s, h in sorted(betoldas_kulcs):
        cellak, betoldo = [], []
        for f, _nev in VISSZHANG_FORRASOK:
            r = next((x for x in lanc if x['strong'] == s and x['igehely'] == h and x['forras'] == f), None)
            if r and r['ellenorzes'] and r['alak'] and r['betoldas'] == 'igen':
                ki = HK.kiejt(r['alak'], aram=True) if f == 'targum' else r['kiejtes']
                cellak.append('%s%s — %s · betoldás' % (r['alak'], (' (%s)' % ki) if ki else '',
                                                        _cella(r['jelentes'].split(' (')[0])))
                betoldo.append(VISSZHANG_NEV[f])
            elif r and r['ellenorzes']:
                cellak.append('nincs betoldás')
            else:
                cellak.append('nincs ellenőrzött adat')
        jel = rovid_jelentes(s)
        szo = jel[0] if jel[1] else s
        tabla.append('| nincs héber szó<br>%s: %s betoldás | %s | %s |' % (
            _rovid_hely(h), szo, ' | '.join(cellak),
            ('Betoldás: %s a lánc szavát (%s) olyan láncversbe teszi, ahol a héberben nincs.'
             % (' és '.join(betoldo), szo)) if betoldo else '—'))
    honnan = ('A lánc %d kulcsszava a motívum helyeit összekötő egyes héber szavak, soronként egy (az 1.2 teljes '
              'szólistája ennél bővebb: szópárokat és görög szavakat is felsorol); láncvers a motívum Peshat-magjának '
              '(%s %d–%d) azon verse, amelyben a kulcsszó a héber szövegben áll; a magon kívüli helyek a lánc bibliai '
              'visszhangjai, a 2. szakaszban állnak.' % ((len(szavak),) + tuple(mag)))
    bevezeto = ('A táblázat lánc-szavanként azt mutatja, hogy az ókori fordító ugyanazzal a szóval adja-e vissza a héber '
                'szót minden láncversben. %s A motívum %d lánc-szavából a Targum %d, a Vulgata %d, a LXX %d szót ad '
                'vissza minden láncversben ugyanazzal a szóval vagy szócsaláddal. Hogy ez lelet-e, az alapvonal dönti el: a '
                'LXX-nél mérhető, hogyan fordítja ugyanazt a szót a láncon kívül; a Targumnál és a Vulgatánál a cella '
                'csak a láncot mutatja, mert hogy a szó a fordító szokásos szava-e, ebből a forrásból nem mérhető.'
                % (honnan, len(szavak), teljes['targum'], teljes['vulgata'], teljes['lxx']))
    if uj_szerkezet(m['id']):
        # lap-javit HAMART-001 (lektor 23–25.): műhelyszavak nélkül; a „láncvers” a Genezis-lánc verse (a szintje az
        # adat szerint Peshat vagy Remez); az egyverses szó a következetesség számlálásából kimarad
        szam_szavak = len(szavak) - len(egyverses)
        bevezeto = ('A táblázat lánc-szavanként azt mutatja, hogy az ókori fordító a Genezis láncának minden versében '
                    'ugyanazzal a szóval adja-e vissza a héber szót. A lánc %d kulcsszava a motívum helyeit összekötő '
                    'egyes héber szavak, soronként egy (az 1.2 teljes szólistája ennél bővebb: szópárokat és görög '
                    'szavakat is felsorol). A versek a Genezis láncának (%s %d–%d) azok a versei, amelyekben a kulcsszó '
                    'a héber szövegben áll; a lánc későbbi bibliai visszhangjai a 2. szakaszban állnak. A több versben '
                    'álló %d lánc-szóból a Targum %d, a Vulgata %d, a LXX %d szót ad vissza minden versben ugyanazzal a '
                    'szóval vagy szócsaláddal%s. Hogy az egyezés lelet-e, azon múlik, szokásos fordítás-e: a LXX-nél ez '
                    'mérhető (hogyan fordítja ugyanazt a héber szót a láncon kívül), a Targumnál és a Vulgatánál ebből a '
                    'forrásból nem, ott a táblázat csak a láncot mutatja.'
                    % ((len(szavak),) + tuple(mag) + (szam_szavak, teljes['targum'], teljes['vulgata'], teljes['lxx'],
                       ('; a csak egy versben álló szónál (%s) a következetesség nem mérhető'
                        % ', '.join(_szo_nev(s.split('+')[0]) for s in egyverses)) if egyverses else '')))
    reszek = ['#### 4.11. Visszhang: ókori fordítások' if uj_szerkezet(m['id']) else
              '#### 4.11. Visszhang: ókori fordítások és rokon nyelvek', olvasoi_bekezdes(bevezeto), '\n'.join(tabla),
              '*A cella a fordítás szava (kiejtéssel) és hogy hány láncversben ugyanaz (n/N). A „Mit mutat” a LXX '
              'alapvonalát és a különleges leletet mondja: a héber szó láncon kívüli ószövetségi verseiben (a láncbeli '
              'jelentéssel) a görög versben ugyanaz a szócsalád-e (versszintű együtt-előfordulás, nem szóillesztés); '
              '%d%% felett szokásos fordítás, %d–%d%% gyakori, de nem kizárólagos, %d%% alatt a láncban választott szó '
              '(félkövér). A láncversek a motívum Peshat-magjának azon versei, ahol a kulcsszó áll: a motívum saját helyei, '
              'nem a szó teljes előfordulása (a magon belül sem). Targum: Onkelos (közkincs); Vulgata: Clementina (közkincs); LXX: a Septuaginta szövege '
              '(CC BY 4.0). A fordítás szavát a kinyerő tábla adja: a LXX-ét gépi társítás, a Targumét és a Vulgatáét '
              'modell emeli ki, egy másik kéz ellenőrzi; ellenőrizetlen sor nem áll a táblában.*'
              % (int(ALAPVONAL_SZOKASOS * 100), int(ALAPVONAL_RITKA * 100), int(ALAPVONAL_SZOKASOS * 100),
                 int(ALAPVONAL_RITKA * 100))]
    if uj_szerkezet(m['id']):
        # ELLENOR_HAMART_lapjavit (24.): az „alapvonal” szó a cellában sem áll
        reszek[2] = reszek[2].replace('az alapvonal nem mérhető', 'így nem mérhető, szokásos fordítás-e')
        # lektor 24., 44.: a jegyzet a forrást és a módszert nevezi meg, a munkamenet leírása nélkül
        reszek[3] = ('*A cella a fordítás szava (kiejtéssel) és az, hány láncversben áll ugyanaz (n/N). A „Mit mutat” '
                     'azt mondja meg, szokásos-e ez a fordítás: a héber szó láncon kívüli ószövetségi verseiben (a '
                     'láncbeli jelentéssel) a görög versben ugyanaz a szócsalád áll-e. A mérés versenként veti össze a két '
                     'szöveget, nem szavanként; %d%% felett szokásos fordítás, %d–%d%% gyakori, de nem kizárólagos, %d%% '
                     'alatt a láncban választott szó (félkövér). Targum: Onkelos (közkincs); Vulgata: Clementina '
                     '(közkincs); LXX: a Septuaginta szövege (CC BY 4.0). A görög megfelelő a Septuaginta szövegéből '
                     'versenként társítva, az arámi és a latin megfelelő a fordítás szövegéből, a forrásszövegen '
                     'ellenőrizve; ellenőrizetlen sor nem áll a táblázatban.*'
                     % (int(ALAPVONAL_SZOKASOS * 100), int(ALAPVONAL_RITKA * 100), int(ALAPVONAL_SZOKASOS * 100),
                        int(ALAPVONAL_RITKA * 100)))
        # a lektor és a Fable közös véleménye (1.): a két mérés kimondva
        reszek.insert(4, 'Ez a tábla a láncon belüli fordítói következetességet méri: ugyanazzal a szóval adja-e vissza a '
                         'fordító a héber szót a lánc minden versében. Hogy a görög szó azonos-e az újszövetségi helyek '
                         'szavával, azt az [5. szakasz](#5-lxx-fordítói-döntések) mutatja.')
    hatter = blokk_visszhang_hatter([r for r in sorok if r['forras'] == 'bdb'], lanc_versek, szavak)
    if hatter and uj_szerkezet(m['id']):
        # F182 (A15; F13 döntése: „igen”, 2026-11-09): a rokon nyelvi tábla a 4.8-ban áll (`rokon_tabla_48`)
        reszek.append('A lánc szavainak rokon nyelvi hátterét (a BDB-szótár szerint) a héber szavak 4.8 pontja adja.')
        ROKON_TABLA_48[m['id']] = hatter
    elif hatter:
        reszek += hatter
    return '\n\n'.join(reszek)


ROKON_TABLA_48 = {}


def rokon_tabla_48(szoveg, m):
    """F182 (A15): a 4.11-ből áthelyezett rokon nyelvi tábla a héber 4.8 pont végére (a V2/V3 kapu a „Háttér: rokon
    nyelvek” alcím alatt mér, a helyétől függetlenül); a pont zárómondata a teljes szócikkfejre mutat."""
    hatter = ROKON_TABLA_48.pop(m['id'], None)
    i = szoveg.find('### Héber szavak')
    j = szoveg.find('#### 4.8. Nyelvi háttér', i) if i >= 0 else -1
    k = szoveg.find('#### 4.9.', j) if j >= 0 else -1
    if k < 0:
        return szoveg
    betet = ['A szavak teljes BDB-szócikkfeje (a nyelvtani alakokkal) a 4.2 pontban áll.']
    if hatter:
        betet += [h.replace('| Lánc-szó |', '| Szó |') for h in hatter]
    return szoveg[:k].rstrip('\n') + '\n\n' + '\n\n'.join(betet) + '\n\n' + szoveg[k:]


# --- F183: 9. Hatástörténet — ókori fordítások és értelmezők -------------------------------------------------------
# A felhasználó döntése (2026-11-11): a visszhang a szótári pont szerepén túlnő, saját főszakaszt kap a 10. Értelmezés
# előtt, számozatlan alcímekkel; benne a visszhang 1 (az ószövetségi lánc ókori fordításai, a korábbi 4.11), a visszhang 2
# újszövetségi ága (Vulgata, szövegváltozat, LXX-előkép) és a tanúréteg (`adat/visszhang_tanuk.tsv`, SEMA 2.57). A 4.11
# helyén mutató marad (egy szabály, egy hely: a blokk egyszer áll a lapon). Csak az új szerkezetű lapon.
HATAS_CIM = '9. Hatástörténet: ókori fordítások és értelmezők'
HATAS_OSZ = 'Ókori fordítások: Ószövetség'
HATAS_USZ = 'Ókori fordítások: Újszövetség'
HATAS_TANU = 'Ókori értelmezők'
VISSZHANG_TANU_TSV_REL = 'adat/visszhang_tanuk.tsv'
TANU_HAGYOMANY = (('gorog', 'görög'), ('latin', 'latin'), ('szir', 'szír'), ('rabbinikus', 'rabbinikus'))
# A Glossa Ordinaria (a felhasználó döntése, 2026-11-11: „1”): a Vulgata-csomag lábjegyzeteiből
# (`konkordancia/Glossa_Ordinaria.tsv`, `eszkozok/visszhang/glossza_import.py`) a tanúréteg egy tanúja, a szabály ugyanaz.
# ELLENOR_F183 3.: a mondat csak akkor áll, ha a motívumnak van Glossa-tanúja (adat), és csak ezt mondja ki; az
# átnézés helyenkénti nyoma a motívum jelentésében (HAMART-001: `naplok/F183_glossza_atnezes.tsv`).
GLOSSZA_MONDAT = ('A Glossa Ordinaria (a Vulgata középkori kommentárja; Migne, 1880, közkincs) a táblázatban ott áll '
                  'tanúként, ahol jegyzete ugyanezt a kapcsolatot mondja ki.')
PESHITTA_MONDAT = 'A szír fordítás (Peshitta) nem vizsgált: szabad, digitális forrása nem áll rendelkezésre.'


def hatas_horgony():
    return _heading_slug(HATAS_CIM)


def _latin_csalad(lemma):
    """A latin szócsalád: a szótári alakok első öt betűje (maledictus ~ maledictum ~ maledico; corruptio ~ corrumpo)."""
    return frozenset(x.strip().lower()[:5] for x in (lemma or '').split(' · ') if x.strip())


def _gorog_kiejtes(lemma):
    try:
        return gorog_magyaros(gepi_atiras(lemma))
    except Exception:
        return ''


_tagnt_cache = None


def _tagnt_vers(igehely):
    """[(Strong, ragozott alak, szótő)] a TAGNT-kivonatból (a vers saját görög szavai)."""
    global _tagnt_cache
    if _tagnt_cache is None:
        _tagnt_cache = collections.defaultdict(list)
        with io.open(os.path.join(KONKORDANCIA, 'TAGNT_kivonat.tsv'), encoding='utf-8') as f:
            for sor in f:
                if sor.startswith('#'):
                    continue
                c = sor.rstrip('\r\n').split('\t')
                if len(c) > 4 and c[0] != 'Igehely':
                    _tagnt_cache[c[0]].append((c[1], c[2], c[4]))
    return _tagnt_cache.get(igehely, [])


_szarmazas_cache = None


def _strong_szarmazas(strong):
    """A Strong-szótár származtatás-mezőjében hivatkozott Strong (φθορά G5356 → φθείρω G5351), vagy None."""
    global _szarmazas_cache
    if _szarmazas_cache is None:
        _szarmazas_cache = {}
        with io.open(os.path.join(KONKORDANCIA, 'Strong_szotar.tsv'), encoding='utf-8') as f:
            next(f)
            for sor in f:
                c = sor.rstrip('\r\n').split('\t')
                if len(c) > 4:
                    mm = re.search(r'\((G\d{4})\)', c[4])
                    if mm:
                        _szarmazas_cache[c[0]] = mm.group(1)
    return _szarmazas_cache.get(strong)


def _konk_sorok(fajl):
    with io.open(os.path.join(KONKORDANCIA, fajl), encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n').split('\t') for s in f if not s.startswith('#') and s.strip()]
    return [dict(zip(sorok[0], s)) for s in sorok[1:]] if sorok else []


_valtozat_cache = {}


def _usz_valtozatok(igehely, strongok):
    """A lánc szavát érintő szövegváltozat a versben: a TAGNT-változatok azon sora, amelynek Strongja a lánc szava és
    valamelyik kiadásból hiányzik; mellé az SBLGNT-apparátus jegyzete, ha az az alakot említi. [(alak, jegyzet)]"""
    if 'tagnt' not in _valtozat_cache:
        _valtozat_cache['tagnt'] = _konk_sorok('TAGNT_valtozatok.tsv')
        _valtozat_cache['sblgnt'] = _konk_sorok('SBLGNT_apparatus.tsv')
    ki = []
    for r in _valtozat_cache['tagnt']:
        if r.get('igehely') == igehely and r.get('strong') in strongok and (r.get('hianyzik_ebbol') or '').strip():
            alak = r['gorog'].rstrip('·,.;')
            jegyzet = next((a['jegyzet'] for a in _valtozat_cache['sblgnt']
                            if a.get('igehely') == igehely and alak in a.get('jegyzet', '')), '')
            mm = re.search(r'\]\s*(\S+)', jegyzet.replace('\xa0', ' '))
            ki.append((alak, ', '.join(r['kiadasok'].split('+')), ', '.join(r['hianyzik_ebbol'].split()),
                       mm.group(1) if mm else ''))
    return ki


def _alak_tovek(alak):
    """A ragozott görög alak tövei az augmentum nélkül is (ELLENOR_F183 1.): διέφθειρεν → δι + ε + φθειρεν; a
    `_gorog_tovek` a szótári alakra készült, a múlt idejű ε-augmentumot nem ismeri."""
    t = ''.join(c for c in unicodedata.normalize('NFD', alak.lower()) if not unicodedata.combining(c))
    tovek = set(_gorog_tovek(t))
    for elotag in ('', 'δι', 'κατ', 'επ', 'απ', 'εξ', 'συν', 'προ'):
        if t.startswith(elotag + 'ε') and len(t) > len(elotag) + 3:
            tovek |= _gorog_tovek(t[len(elotag) + 1:])
    return frozenset(tovek)


def blokk_hatas_usz(m, sorai):
    """Az újszövetségi ág: a motívum görög lánc-szavai szócsaládonként; Vulgata (a kinyerő tábla ellenőrzött sora), a
    lánc szavát érintő szövegváltozat, és a LXX-előkép (ugyanaz a görög szócsalád a Genezis-lánc ellenőrzött
    LXX-soraiban). Adat nélkül None."""
    vh = [r for r in visszhang_sorok(m['id']) if r['ellenorzes']]
    usz = [r for r in vh if r['forras'] == 'vulgata' and r['strong'].startswith('G')]
    if not usz:
        return None
    sorrend = {}
    for i, s in enumerate(sorai):
        for v in SZKZ.versek(s['igehely']):
            sorrend.setdefault(v, i)
    lemma = {}
    for r in usz:
        for st, _alak, to in _tagnt_vers(r['igehely']):
            if st == r['strong']:
                lemma.setdefault(r['strong'], to)
    # szócsaládok: összefüggő komponensek — két Strong egy családban, ha közös a tövük, vagy a Strong-szótár
    # származtatása köti össze (φθορά ← φθείρω; διαφθείρω ~ φθείρω a tő szerint)
    # determinisztikus sorrend (E28): az első előfordulás, egyezésnél a Strong-szám (két szó ugyanabban a versben)
    strongok = sorted({r['strong'] for r in usz},
                      key=lambda s_: (min(sorrend.get(x['igehely'], 999) for x in usz if x['strong'] == s_), s_))
    tovek = {st: _gorog_tovek(lemma.get(st, '')) for st in strongok}
    csoportok = []
    for st in strongok:
        tagok = [c for c in csoportok if any(tovek[st] & tovek[x] or _strong_szarmazas(st) == x
                                             or _strong_szarmazas(x) == st for x in c['strongok'])]
        cs = {'tovek': set(tovek[st]), 'strongok': [st]}
        for c in tagok:
            cs['strongok'] = c['strongok'] + cs['strongok']
            cs['tovek'] |= c['tovek']
            csoportok.remove(c)
        cs['strongok'].sort(key=strongok.index)
        csoportok.append(cs)
    csoportok.sort(key=lambda c: min(strongok.index(x) for x in c['strongok']))
    szolista, _mag = lanc_szavak(m, sorai)
    lanc_par = {(s_, v) for s_, vv in (szolista or []) for v in vv}
    # az előkép csak a lánc-szó láncverseiben (a 8:21 kálal-sora nem lánc-szó: nem előkép)
    lxx = [r for r in vh if r['forras'] == 'lxx' and r['alak'] and r['lemma'] and (r['strong'], r['igehely']) in lanc_par]
    osz_vulg = {(r['strong'], r['igehely']): r for r in vh if r['forras'] == 'vulgata' and r['strong'].startswith('H')}
    tabla = ['| Görög szó · helyek | Vulgata | Szövegváltozat | Előkép a Septuagintában | Mit mutat |',
             '|---|---|---|---|---|']
    egyezo = 0
    for cs in csoportok:
        sorok_cs = sorted([r for r in usz if r['strong'] in cs['strongok']], key=lambda r: sorrend.get(r['igehely'], 999))
        versek = list(dict.fromkeys(r['igehely'] for r in sorok_cs))
        szavak = ' · '.join('%s (%s)' % (lemma.get(s, s), _gorog_kiejtes(lemma.get(s, ''))) for s in cs['strongok'])
        csal = collections.Counter(k for r in sorok_cs for k in _latin_csalad(r['lemma']))
        fo = csal.most_common(1)[0][0] if csal else None
        vv = collections.OrderedDict()
        for r in sorok_cs:
            vv.setdefault(r['igehely'], []).append(r)
        n = sum(1 for rr in vv.values() if any(fo in _latin_csalad(r['lemma']) for r in rr))
        vulg = '; '.join('%s *%s*' % (v, ' · '.join(r['alak'] for r in rr)) for v, rr in vv.items())
        vulg += ' · %d/%d' % (n, len(vv))
        valt, valt_csaladon_belul = [], False
        for v in versek:
            for alak, kiad, hiany, mas in _usz_valtozatok(v, cs['strongok']):
                if mas:
                    valt.append('%s: %s (%s) — %s; %s (%s) — %s' % (v, alak, _gorog_kiejtes(alak), kiad, mas,
                                                                   _gorog_kiejtes(mas), hiany))
                    if _alak_tovek(mas) & cs['tovek']:
                        valt_csaladon_belul = True
                else:
                    valt.append('%s: %s (%s) — %s; eltér: %s' % (v, alak, _gorog_kiejtes(alak), kiad, hiany))
        valt_cella = '; '.join(valt) if valt else 'nincs a lánc szavát érintő változat'
        elo = [r for r in lxx if _gorog_tovek(r['lemma'].split(' · ')[0]) & cs['tovek']]
        elo_versek = list(dict.fromkeys(r['igehely'] for r in elo))
        elo_lemma = list(dict.fromkeys(x for r in elo for x in r['lemma'].split(' · ')))
        elo_cella = ('%s (%s)' % (', '.join(_rovid_hely(h) for h in elo_versek), ', '.join(elo_lemma))
                     if elo_versek else 'nincs a láncversekben')
        osz = [osz_vulg.get((r['strong'], r['igehely'])) for r in elo]
        osz = [r for r in osz if r and r['alak']]
        osz_n = sum(1 for r in osz if fo and fo in _latin_csalad(r['lemma']))
        if fo and n == len(vv) and osz and osz_n == len(osz):
            mit = ('A Vulgata az újszövetségi helyeken és a Genezis-lánc %d előképversében is ugyanazt a latin '
                   'szócsaládot használja (*%s-*): a latin olvasó a két szövetség helyeit egy szóval olvassa.'
                   % (len(osz), fo))
            egyezo += 1
        elif fo and osz:
            mit = ('A Vulgata az újszövetségi helyeken %d/%d versben a *%s-* szócsaládot használja; a Genezis-lánc '
                   'előképverseiben ugyanezt %d/%d versben: a latin szóválasztás a két szövetség között csak '
                   'részben egyezik.' % (n, len(vv), fo, osz_n, len(osz)))
        elif fo:
            mit = 'A Vulgata az újszövetségi helyeken %d/%d versben a *%s-* szócsaládot használja.' % (n, len(vv), fo)
        else:
            mit = '—'
        if valt_csaladon_belul:
            mit += ' A szövegváltozat ugyanabban a görög szócsaládban marad: a lánc szava minden kiadásban áll.'
        tabla.append('| %s<br>%s | %s | %s | %s | %s |' % (szavak, ', '.join(versek), vulg, valt_cella, elo_cella, mit))
    bevezeto = ('Az újszövetségi helyeken a lánc görög szavai állnak. A táblázat szócsaládonként azt mutatja, hogy a '
                'latin Vulgata ugyanazzal a latin szóval adja-e vissza őket, van-e a lánc szavát érintő szövegváltozat, '
                'és hol áll ugyanez a görög szó a Genezis-lánc Septuaginta-szövegében. A %d görög szócsaládból %d '
                'esetében a Vulgata a két szövetségben ugyanazt a latin szócsaládot használja.' % (len(csoportok), egyezo))
    if uj_szerkezet(m['id']):
        # lektor 26.: a tematikus újszövetségi hely kimaradása kimondva; az „előkép” helyett szóegyezés
        tem = [s['igehely'] for s in sorai if (s.get('gerinc_elem') or '').startswith('tematikus:')
               and _konyvresz(s['igehely']) == 'usz']
        bevezeto = ('A motívum lexikai újszövetségi helyein a lánc görög szavai állnak%s. A táblázat szócsaládonként azt '
                    'mutatja, hogy a latin Vulgata ugyanazzal a latin szóval adja-e vissza őket, van-e a lánc szavát '
                    'érintő szövegváltozat, és a Genezis-lánc mely Septuaginta-verseiben áll ugyanez a görög szócsalád. A '
                    '%d görög szócsaládból %d esetében a Vulgata a két szövetségben ugyanazt a latin szócsaládot '
                    'használja.' % ((' (a tematikus %s a lánc szava nélkül áll, ezért nem szerepel)' % ', '.join(tem))
                                    if tem else '', len(csoportok), egyezo))
        tabla[0] = tabla[0].replace('Előkép a Septuagintában', 'Ugyanez a szó a Genezis-lánc Septuagintájában')
        # ELLENOR_HAMART_lapjavit (26.): az „előkép” szó a cellákban sem áll
        tabla = [x.replace('előképversében', 'versében').replace('előképverseiben', 'verseiben') for x in tabla]
    lab = ('*A Vulgata-cella a versben álló latin szó és az, hány versben áll a fő latin szócsalád (n/N); a latin '
           'megfelelőt modell emeli ki, egy másik kéz ellenőrzi. Szövegváltozat: az SBL Greek New Testament apparátusa '
           '(CC BY 4.0) és a STEPBible TAGNT változatjegyzéke (CC BY 4.0), csak ahol a lánc szavát érinti. Előkép: '
           'ugyanaz a görög szócsalád a Genezis-lánc ellenőrzött Septuaginta-soraiban (az ószövetségi táblázat '
           'LXX-oszlopa). Vulgata: Clementina (közkincs). %s*' % PESHITTA_MONDAT)
    if uj_szerkezet(m['id']):
        lab = ('*A Vulgata-cella a versben álló latin szó és az, hány versben áll a fő latin szócsalád (n/N); a latin '
               'megfelelő a Vulgata szövegéből, a forrásszövegen ellenőrizve. Szövegváltozat: az SBL Greek New Testament '
               'apparátusa (CC BY 4.0) és a STEPBible TAGNT változatjegyzéke (CC BY 4.0), csak ahol a lánc szavát '
               'érinti. A Genezis-lánc Septuagintája: ugyanaz a görög szócsalád a Genezis-lánc ellenőrzött '
               'Septuaginta-soraiban (az ószövetségi táblázat LXX-oszlopa); ez szóegyezés, nem tipológiai állítás. '
               'Vulgata: Clementina (közkincs). %s*' % PESHITTA_MONDAT)
    return '\n\n'.join([olvasoi_bekezdes(bevezeto), '\n'.join(tabla), lab])


def visszhang_tanuk(motivum_id):
    ut = os.path.join(ADAT, 'visszhang_tanuk.tsv')
    if not os.path.exists(ut):
        return []
    _, sorok = G.tsv_beolvas(ut)
    return [r for r in sorok if r.get('motivum') == motivum_id]


def tanuk_lapra(m, sorai):
    """A lapra kerülő tanúk: ellenőrzött sor, Remez- vagy Sod-szintű hely (a beépített sor `pardes_szint`-je),
    hagyományonként helyenként legfeljebb egy, a helyek sorrendjében."""
    szint = {s['igehely']: s.get('pardes_szint', '') for s in sorai}
    sorrend = {s['igehely']: i for i, s in enumerate(sorai)}
    hagy = [h for h, _ in TANU_HAGYOMANY]
    jo = [r for r in visszhang_tanuk(m['id']) if r['ellenorzes'] and re.search(r'Remez|Sod', szint.get(r['igehely'], ''))
          and r['hagyomany'] in hagy]
    latott, tanuk = set(), []
    for r in sorted(jo, key=lambda r: (sorrend.get(r['igehely'], 999), hagy.index(r['hagyomany']))):
        if (r['igehely'], r['hagyomany']) not in latott:
            latott.add((r['igehely'], r['hagyomany']))
            tanuk.append(r)
    return tanuk


def blokk_hatas_tanuk(m, sorai):
    """A tanúréteg. Adat nélkül is áll: a lap kimondja, mit vizsgált (üres eredmény, nem kitöltés)."""
    tanuk = tanuk_lapra(m, sorai)
    hagy_nev = dict(TANU_HAGYOMANY)
    # ELLENOR_F183 2–3.: a bevezető motívumfüggetlen, és a két tanúfajtát külön mondja ki: az olvasat (a forrásszöveg
    # alapján, két kézzel: ugyanazt a kapcsolatot látja) és az együtt-idézés (Chain Lineage, tényadat: a kapcsolat
    # értelmezését a lap ezekről nem állítja)
    bevezeto = ('Az ókori értelmezők, akik a motívum egy helyét a lánc egy másik helyével együtt olvassák. Két fajta '
                'tanú áll itt: akinek olvasatát a forrás szövege alapján egy saját szavas mondat foglalja össze — ő '
                'ugyanazt a kapcsolatot látja, amelyet a lap leír —, és akit egy versláncban a hely a lánc más '
                'verseivel együtt idéz (a Chain Lineage Browser tényadata; a kapcsolat értelmezését a lap ezekről nem '
                'állítja). Hagyományonként (görög, latin, szír, rabbinikus) helyenként legfeljebb egy tanú áll, csak '
                'a Remez- és Sod-szintű helyeken; idézet nincs.')
    if uj_szerkezet(m['id']):
        # lap-javit HAMART-001 (lektor 27., 44.): teljes mondat; az „ugyanazt a kapcsolatot látja” csak ott, ahol a
        # mondat a lánc másik helyét megnevezi; műhelyszavak nélkül
        bevezeto = ('Ez a rész azt mutatja, hogyan olvasták a motívum helyeit az ókori értelmezők. Két fajta tanú áll '
                    'itt. Az egyiknél egy mondatos összefoglaló mondja meg a forrás szövege alapján, mit lát a tanú a '
                    'helyben; ahol a tanú a lánc egy másik helyére is utal, a mondat megnevezi. A másik fajta tanú egy '
                    'versláncban idézi a helyet a lánc más verseivel együtt (a Chain Lineage Browser adata); ez az '
                    'együtt-idézés ténye, a kapcsolat értelmezéséről nem állít semmit. Hagyományonként (görög, latin, '
                    'szír, rabbinikus) helyenként '
                    'legfeljebb egy tanú áll, csak a Remez- és Sod-szintű helyeken; idézet nincs.')
    if tanuk:
        bevezeto += ' A motívum %d helyén %d tanú áll.' % (len({r['igehely'] for r in tanuk}), len(tanuk))
    else:
        bevezeto += ' A vizsgált helyeken nincs ilyen tanú.'
    tabla = ['| Hely | Tanú · hagyomány · kor | Mit lát | Forrás |', '|---|---|---|---|']
    for r in tanuk:
        kor = (' · %s' % r['kor']) if r['kor'] else ''
        if r['forras'] == 'chain_lineage':
            forras = 'Chain Lineage Browser (Blidstein és mtsai), lekérdezve: %s%s' % (
                r['lekerdezve'], ' · BiblIndex' if r['biblindex'] == 'igen' else '')
        elif r['forras'] == 'hcf':
            forras = 'HistoricalChristianFaith, lekérdezve: %s' % r['lekerdezve']
        elif r['forras'] == 'glossa':
            forras = 'Glossa Ordinaria (Migne, 1880) a Vulgata Clementina csomagjában (eBible, közkincs)'

        else:
            forras = 'Sefaria, lekérdezve: %s' % r['lekerdezve']
        tanu_hely = '' if r['tanu_hely'] in ('', r['igehely']) or r['forras'] == 'chain_lineage' \
            else ' (Tárgyalt hely: %s.)' % r['tanu_hely']
        mu = re.sub(r'(\d+):(\d+)$', r'\1.\2', r['mu']) if r['forras'] == 'sefaria' else r['mu']
        fajta = ' *(együtt-idézés)*' if r['forras'] == 'chain_lineage' else ''
        tabla.append('| %s | %s, *%s* · %s%s | %s%s%s | %s |' % (
            _ige_link(r['igehely']), r['tanu'], mu, hagy_nev[r['hagyomany']], kor, r['kapcsolat'], tanu_hely, fajta,
            forras))
    lab = ('*A tanú-jelölteket a tanúindex (HistoricalChristianFaith, Sefaria), a Glossa Ordinaria jegyzetei és a Chain '
           'Lineage Browser adta; a lapra '
           'csak ellenőrzött sor kerül: a modell által írt mondatot egy másik kéz a forrásszövegen ellenőrzi, a Chain '
           'Lineage-sor tényadat (szerző, mű, század, nyelv, az együtt idézett versek), a lekérdezés újrafuttatásával '
           'ellenőrizve. Az egyházatyák és a rabbinikus források szövegét a lap nem idézi. A Chain Lineage Browser '
           'bibliai hivatkozásai a BiblIndexből valók (Institut des Sources Chrétiennes, CNRS – HiSoMA, Lyon).*')
    if uj_szerkezet(m['id']):
        lab = ('*A tanúk forrásai: a HistoricalChristianFaith kommentár-adatbázis és a Sefaria (egyházatyák, '
               'rabbinikus források), a Glossa Ordinaria jegyzetei és a Chain Lineage Browser. Az összefoglaló mondat a '
               'forrásszövegen ellenőrizve áll a táblázatban; a versláncok adata (szerző, mű, század, nyelv, az együtt '
               'idézett versek) a lekérdezés megismétlésével ellenőrizve. Az egyházatyák és a rabbinikus források '
               'szövegéből itt nincs idézet. A Chain Lineage Browser bibliai hivatkozásai a BiblIndexből valók (Institut '
               'des Sources Chrétiennes, CNRS – HiSoMA, Lyon).*')
    reszek = [olvasoi_bekezdes(bevezeto)]
    if tanuk:
        reszek.append('\n'.join(tabla))
    reszek.append(lab)
    if any(r['forras'] == 'glossa' for r in tanuk):
        reszek.append(GLOSSZA_MONDAT)
    return '\n\n'.join(reszek)


CHAIN_LINEAGE_LICENC_OLVASOI = 'licenc nincs megadva; csak tényadatként, forrásmegjelöléssel használva'


def hatastortenet_forrasok(m):
    """F183: a 9. Hatástörténet szakasz forrásai a Kolofon forrástáblájához és az Irodalomhoz [(fájl, licenc)]; csak az
    új szerkezetű lapon, csak a ténylegesen használt forrás (a tanúréteg forrásai a tábla ellenőrzött soraiból)."""
    if not uj_szerkezet(m['id']):
        return []
    ki = [('adat/visszhang_megfelelok.tsv', LC('projekt_adat')), ('konkordancia/Targum_PD.tsv', LC('Targum_PD')),
          ('konkordancia/Vulgata_Clementina.tsv', LC('Vulgata_Clementina')),
          ('konkordancia/SBLGNT_apparatus.tsv', LC('SBLGNT_apparatus')),
          ('konkordancia/TAGNT_valtozatok.tsv', LC('TAGNT_valtozatok'))]
    tanuk = [r for r in visszhang_tanuk(m['id']) if r['ellenorzes']]
    if tanuk:
        ki.append(('adat/visszhang_tanuk.tsv', LC('projekt_adat')))
    forrasok = {r['forras'] for r in tanuk}
    if 'hcf' in forrasok:
        ki.append(('konkordancia/Tanu_atyak_index.tsv', LC('Tanu_atyak_index')))
    if 'sefaria' in forrasok:
        ki.append(('konkordancia/Tanu_rabbinikus_index.tsv', LC('Tanu_rabbinikus_index')))
    if 'glossa' in forrasok:
        ki.append(('konkordancia/Glossa_Ordinaria.tsv', LC('Glossa_Ordinaria')))
    if 'chain_lineage' in forrasok:
        # az orkesztrátor döntése (2026-11-11): az olvasónak a „tisztázatlan” félrevezető; a `licencek.tsv` belső
        # jelölése `tisztazatlan` marad, a lapon ez a mondat áll (a forrás a nyílt magba nem kerül)
        ki.append(('chain-lineages', CHAIN_LINEAGE_LICENC_OLVASOI))
    return ki


# --- F183 (K67f): a vitatott pontok lektorált szakirodalma -------------------------------------------------------
# A felhasználó döntése (2026-11-11, „mehet”): a 10. Értelmezés „⚠️ Vitatott pontok” részében pontonként legfeljebb egy
# lektorált forrás (OpenAlex, Crossref, DOAB), egymondatos, saját szavas összefoglalóval; ahol nincs a kérdésről szóló
# forrás, a lap kimondja. Forrás: `adat/vitatott_forrasok.tsv` (SEMA 2.58), csak ellenőrzött sor; a pont bekezdését a
# kézi forrás adja, a generátor csak utána illeszti a szakirodalom-sort (DT28: a forrásba nem ír vissza).
VITATOTT_FORRASOK_TSV_REL = 'adat/vitatott_forrasok.tsv'


def vitatott_forrasok(motivum_id):
    ut = os.path.join(ADAT, 'vitatott_forrasok.tsv')
    if not os.path.exists(ut):
        return []
    _, sorok = G.tsv_beolvas(ut)
    return [r for r in sorok if r.get('motivum') == motivum_id and r.get('ellenorzes')]


def _szakirodalom_hivatkozas(r):
    return '%s, %s: *%s*. %s.%s' % (r['szerzo'], r['ev'], r['cim'], r['megjelenes'],
                                    (' DOI: %s' % r['doi']) if r['doi'] else (' %s' % r['url']))


def szakirodalom_beszur(szoveg, m):
    """F183 (K67f): a vitatott pontok bekezdése után a szakirodalom-sor; a 12. Irodalomba a teljes hivatkozás."""
    if not uj_szerkezet(m['id']):
        return szoveg
    sorok = vitatott_forrasok(m['id'])
    if not sorok:
        return szoveg
    i = szoveg.find('### ⚠️ Vitatott pontok')
    if i < 0:
        return szoveg
    for r in sorok:
        j = szoveg.find('**%s.**' % r['pont'], i)
        if j < 0:
            continue
        k = szoveg.find('\n\n', j)
        k = k if k >= 0 else len(szoveg)
        if r['szerzo']:
            sor = '*Szakirodalom:* %s (%s, %s; a teljes hivatkozás a 12. szakaszban.)' % (
                r['osszefoglalo'], r['szerzo'].split(',')[0].split()[-1], r['ev'])
        else:
            sor = '*Szakirodalom:* %s (Keresve: OpenAlex, Crossref, %s.)' % (r['osszefoglalo'], r['lekerdezve'])
        szoveg = szoveg[:k] + '\n\n' + sor + szoveg[k:]
    forrasok = [r for r in sorok if r['szerzo']]
    if forrasok:
        h = szoveg.find('**Adatforrások:**')
        if h >= 0:
            blokk = '**Szakirodalom (a vitatott pontokhoz):**\n\n' + '\n'.join(
                '- %s' % _szakirodalom_hivatkozas(r) for r in forrasok) + '\n\n'
            szoveg = szoveg[:h] + blokk + szoveg[h:]
    return szoveg


def hatastortenet_athelyez(szoveg, m, sorai):
    """F183: a 4.11 visszhang-blokk tartalma a 9. Hatástörténet szakaszba (az „Ókori fordítások: Ószövetség” alcím
    alá), mellé az újszövetségi ág és a tanúréteg; a 4.11 helyén mutató. A szakasz a 10. Értelmezés elé kerül."""
    if not uj_szerkezet(m['id']):
        return szoveg
    if szoveg.find('\n## 10. Értelmezés') < 0:
        return szoveg
    i = szoveg.find('#### 4.11. Visszhang: ókori fordítások')
    osz = ''
    if i >= 0:
        j = re.compile(r'(?m)^#### 4\.12\. ').search(szoveg, i)
        j = j.start() if j else i
        blokk = szoveg[i:j]
        osz = blokk.split('\n', 1)[1].strip() if '\n' in blokk else ''
        mutato = '#### 4.11. Visszhang: ókori fordítások\n\n%s\n\n' % olvasoi_bekezdes(
            'Az ókori fordítások és értelmezők olvasata a [%s](#%s) szakaszban áll.' % (HATAS_CIM, hatas_horgony()))
        szoveg = szoveg[:i] + mutato + szoveg[j:]
    cel = szoveg.find('\n## 10. Értelmezés')
    usz = blokk_hatas_usz(m, sorai)
    tanu = blokk_hatas_tanuk(m, sorai)
    bevezeto = ('A szakasz azt mutatja, hogyan olvasták a motívum láncát a legkorábbi fordítók és értelmezők: az '
                'ószövetségi lánc ókori fordításai (Targum, Vulgata, Septuaginta), az újszövetségi helyek latin '
                'fordítása és szövegváltozatai, végül az egyházatyák és a rabbinikus hagyomány tanúi.')
    reszek = ['## %s' % HATAS_CIM, olvasoi_bekezdes(bevezeto)]
    if osz:
        reszek += ['### %s' % HATAS_OSZ, osz]
    if usz:
        reszek += ['### %s' % HATAS_USZ, usz]
    reszek += ['### %s' % HATAS_TANU, tanu]
    return szoveg[:cel].rstrip('\n') + '\n\n' + '\n\n'.join(reszek) + '\n\n' + szoveg[cel:].lstrip('\n')


def _magyar_jelentes(t):
    """A jelentés olvasói alakja: az angol maradék és a BDB-utalás zárójele nélkül."""
    t = re.sub(r'\s*\((?:[^()]*\b(?:BDB|so|see|Assyrian|Late|cf)\b[^()]*)\)', '', t or '')
    t = re.split(r';\s*a BDB:', t)[0]
    return t.strip(' ;')


def massalhangzos_atiras(szo):
    """Pontozatlan héber betűs alak mássalhangzós átírása a kiejtési szabály betűi szerint (קללם → k-l-l-m)."""
    ki = []
    for c in szo:
        if 'א' <= c <= 'ת':
            ki.append(HK.ALAP_MSH.get(c, '') or "'")
    return '-'.join(ki)


_bdb_fejek_cache = None


def _bdb_fejek():
    """[(strong, mássalhangzók, szófaj-ige-e)] a helyi BDB-szöveg szócikk-fejéből."""
    global _bdb_fejek_cache
    if _bdb_fejek_cache is None:
        _bdb_fejek_cache = []
        with io.open(os.path.join(KONKORDANCIA, 'BDB_teljes_unabridged.tsv'), encoding='utf-8') as f:
            for sor in f:
                c = sor.split('\t')
                if len(c) < 3 or not re.match(r'^H\d{4}', c[0]):
                    continue
                fej = c[2][:160]
                heb = re.search(r'[א-ת][א-ת֑-ׇ]*', fej)
                if not heb:
                    continue
                mh = ''.join(ch for ch in heb.group(0) if 'א' <= ch <= 'ת')
                _bdb_fejek_cache.append((c[1].strip() or c[0].strip(), mh, bool(re.search(r'\]?\s*verb\b', fej))))
    return _bdb_fejek_cache


def bdb_to_strong(strong):
    """A főnévi lánc-szó igei töve a helyi BDB-ben: az az ige, amelynek mássalhangzói a főnév mássalhangzói, vagy a
    főnévéi a szokásos képzők (-ón, -t, -á, m-, t-) nélkül (חָמָס → חָמַס; עִצָּבוֹן → עָצַב); None, ha nincs."""
    fejek = _bdb_fejek()
    sajat = next((f for f in fejek if f[0] == strong), None)
    if not sajat or sajat[2]:
        return None
    mh = sajat[1].replace('ך', 'כ').replace('ם', 'מ').replace('ן', 'נ') \
        .replace('ף', 'פ').replace('ץ', 'צ')
    jeloltek = [mh]
    for veg in ('ונ', 'ת', 'ה', 'ות'):
        if mh.endswith(veg) and len(mh) - len(veg) >= 2:
            jeloltek.append(mh[:-len(veg)])
    for kezd in ('מ', 'ת'):
        jeloltek += [j[1:] for j in list(jeloltek) if j.startswith(kezd) and len(j) > 3]
    vegso = str.maketrans('ךםןףץ', 'כמנפצ')
    for j in jeloltek:
        for s, m2, ige in fejek:
            if ige and s != strong and m2.translate(vegso) == j:
                return s
    return None


def _hatter_sorok(hs, nyelv_nev_elotag=''):
    """[(nyelv, szavak, jelentések, megjegyzés)] nyelvenként, csak valódi rokon nyelvvel (DT-F178d)."""
    nyelvek = collections.OrderedDict()
    for r in hs:
        if not r['ellenorzes']:
            continue
        nyelv = r['lemma'].split(' (')[0].strip()
        if nyelv not in ROKON_NYELVEK or 'Targum' in (r['megjegyzes'] or '') or 'ᵑ7' in (r['megjegyzes'] or ''):
            continue
        jel = _magyar_jelentes(r['jelentes'])
        if not r['alak'] and (not jel or 'azonos a bibliai héberrel' in jel):
            continue
        nyelvek.setdefault(r['lemma'], []).append((r, jel))
    ki = []
    for nyelv, lista in nyelvek.items():
        szavak, jelek, megj = [], [], set()
        for r, jel in lista:
            for a in [x.strip() for x in r['alak'].split('·') if x.strip()]:
                if re.search('[֐-׿]', a):
                    k = HK.kiejt(a) or massalhangzos_atiras(a)
                else:
                    k = re.sub(r'\s*\(.*?\)', '', r['kiejtes'] or '').split('·')[0].strip()
                szavak.append('%s (%s)' % (a, k) if k else a)
            if not r['alak']:
                megj.add('a BDB az alakot írás nélkül adja')
            if re.search(r'\?|possibly|bizonytalan|valószínűleg|kétséges|dubious|ritka', (r['megjegyzes'] or '') + jel):
                megj.add('a BDB szerint bizonytalan vagy ritka')
            if jel and jel not in jelek:
                jelek.append(jel)
        ki.append((nyelv, szavak, jelek, '; '.join(sorted(megj)) or '—'))
    return ki


def _to_iras_kiejtes(strong):
    """„חָטָא (chátá)” — a szó írása és zárójeles kiejtése (sablon 6: táblában írás + kiejtés)."""
    lk = lemma_kiejtes(strong)
    if not lk:
        return strong
    return '%s (%s)' % (lk[0], lk[1]) if lk[1] else lk[0]


def blokk_visszhang_hatter(hatter, lanc_versek=None, szavak=None):
    """A rokon nyelvi háttér (DT-F178d): csak valódi rokon nyelv (ROKON_NYELVEK), nyelvenként egy sor; az újhéber, a
    targumi arámi és a Sirák sora nem rokon nyelvi háttér; a tartalom nélküli sor nem áll. Főnévnél, amelynek
    szócikkében nincs rokon alak, az igei tő szócikke (`bdb_to_strong`) — „a főnév szócikkében nincs; a tő szerint”.
    Csak a lánc szavai (`szavak`, DT-F178g) és a tövük; lánc-szó, amelynek nincs `bdb` sora: a hiány kimondva."""
    lanc_versek = lanc_versek or {}
    if szavak is None:
        szavak = list(dict.fromkeys(r['strong'] for r in hatter))
    if not hatter and not szavak:
        return []
    van_sora = {r['strong'] for r in hatter}
    tovek = {bdb_to_strong(s) for s in szavak
             if any(not r['alak'] and not r['lemma'] for r in hatter if r['strong'] == s)} - {None}
    hatter = [r for r in hatter if r['strong'] in szavak or r['strong'] in tovek]
    tohoz = {r['strong'] for r in hatter}
    ht = ['| Lánc-szó | Rokon nyelv · szó (kiejtés) | Jelentés | Megjegyzés |', '|---|---|---|---|']
    for s in szavak:
        cim = _lanc_szo_cim(s, lanc_versek.get(s))
        if s not in van_sora:
            # lap-javit HAMART-001 (orkesztrátor, lektor 45.): a cella a szóról szól, nem a munka állapotáról; ha a
            # rokon írások lekérdezése lefutott, és a szócikkben nincs rokon alak, ezt mondja ki, a tőre utalva
            if bdb_rokon_szocikk(s) is not None:
                to = bdb_to_strong(s)
                ht.append('| %s | Nincs rokon nyelvi alak a BDB szócikkében%s | — | — |' % (cim, (
                    '; az igei tő, a %s szócikke ad rokon alakokat, ezek a táblában nem szerepelnek'
                    % _to_iras_kiejtes(to)) if to else ''))
            else:
                ht.append('| %s | a rokon nyelvi adat kinyerése még nem történt meg | — | — |' % cim)
            continue
        hs = [r for r in hatter if r['strong'] == s]
        if any(not r['alak'] and not r['lemma'] for r in hs):
            to = bdb_to_strong(s)
            if bdb_rokon_szocikk(s) == 0:
                elo = ('a rokon írások lekérdezése a BDB-szócikket nem azonosította; a helyi BDB-szövegben rokon '
                       'nyelvi alak nem áll' if bdb_helyi_szocikk(s) else 'nem azonosítható: a BDB-szócikk nem található')
            else:
                elo = 'a BDB-szócikkben nincs rokon nyelvi adat'
            to_sorok = _hatter_sorok([r for r in hatter if r['strong'] == to]) if to and to in tohoz else []
            if to_sorok:
                lk = lemma_kiejtes(to)
                tonev = lemma_cim(lk) if lk else to
                ht.append('| %s | %s; a tő, a %s ige szócikke szerint: | — | — |' % (
                    cim, elo.replace('a BDB-szócikkben nincs', 'a főnév szócikkében nincs'), tonev))
                for nyelv, szavak, jelek, megj in to_sorok:
                    ht.append('| ↳ tő: %s | %s%s | %s | %s |' % (tonev, nyelv, (' ' + ' · '.join(szavak)) if szavak else '',
                                                               _cella('; '.join(jelek) or '—'), megj))
            else:
                ht.append('| %s | %s | — | — |' % (cim, elo))
            continue
        for nyelv, szavak, jelek, megj in _hatter_sorok(hs):
            ht.append('| %s | %s%s | %s | %s |' % (cim, nyelv, (' ' + ' · '.join(szavak)) if szavak else '',
                                                  _cella('; '.join(jelek) or '—'), megj))
    return ['##### Háttér: rokon nyelvek (BDB)',
            olvasoi_bekezdes('A lánc héber szavainak rokon nyelvi alakjai a BDB-szótár szerint (akkád/asszír, arab, '
                             'etióp, szír, arámi, óarámi, Tell el-Amarna, sabeus), kiejtéssel és magyar jelentéssel. A '
                             'rokon nyelv a szó eredetéről szól, nem a motívum funkciójáról.'),
            '\n'.join(ht)]


VAZ_SABLON = """# 📖 %(id)s — %(cim)s

## Kivonat

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

### Miért fontos ez a lelet

*Kézzel írandó.*

## 3. LXX-fordítói döntések

%(lxx)s

## 4. Kereszthivatkozások

%(kereszthivatkozasok)s

### Minősítés

*Kézzel írandó: független megerősítés / új találat / nem releváns.*

## 5. Kapcsolatok

%(kapcsolatok)s

### Alátámasztás

*Kézzel írandó.*

## 5/b. Kapcsolódó motívumok

%(kapcsolodo)s

## 6. Értelmezés

*Kézzel írandó — a forrás-study PaRDeS keretrendszere, bővítve a lexikai leletekkel.*

## 6/b. Alkalmazás és tanítói egyezés

### Alkalmazás és tanítványság

*Kézzel írandó.*

### Tanítói egyezés

*Kézzel írandó.*

## 7. Módszertan és nyitott kérdések

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
    blokk_kizart_szov, fl_kizart = blokk_kizart(m, len(sorai))
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
        + [(fajl, licenc, 'hatastortenet') for fajl, licenc in hatastortenet_forrasok(m)]   # F183
        + ([(VITATOTT_FORRASOK_TSV_REL, LC('projekt_adat'), 'ertelmezes')] if uj_szerkezet(m['id'])
           and vitatott_forrasok(m['id']) else [])                                              # F183 (K67f)
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


KIEJTES_JELOLT_HIANY = {}


def kiejtes_potol(szoveg, motivum_id):
    """A kiejtés-szabály (kiejtés-szabály, ISTENTISZT-001 arany lap, 2026-10-29) a kész lapon: a generált részeken az első előfordulás kiejtése pótolva
    (`kiejtes_szoveg.potol`); a megmaradt hiányok (jóváhagyott héber alak nélkül, vagy a kézi részen) a
    KIEJTES_JELOLT_HIANY-ba kerülnek, a futás végén listázva."""
    import kiejtes_szoveg as KSZ
    uj, hiany = KSZ.potol(szoveg)
    KIEJTES_JELOLT_HIANY[motivum_id] = hiany
    return uj


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

        if uj_szerkezet(m['id']):
            lemma_valtozat_beallit(sorai)        # F182 (A04): a lemma-változat a motívum szövegéhez
        else:
            LEMMA_VALTOZAT.clear()
        UJ_DOMEN_MAGYAR[0] = uj_szerkezet(m['id'])   # F182 (A12)
        blokkok, tisztazatlan_erintve_szocikkek = render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek)
        osszesitett_tisztazatlan[m['id']] = tisztazatlan_erintve_szocikkek

        cel_ut = os.path.join(kimenet_gyoker, '%s_TUDOMANYOS.md' % m['id'])
        meglevo_uj = None
        if uj_szerkezet(m['id']):
            # F178: az új szerkezetű lap mindig nulláról épül (minden rése a kézi forrásból vagy az adatból jön; a
            # helyben frissítés a régi címekhez igazodik), majd az új szerkezetre alakul
            if any(s['forras'] == 'lap' for (mid, _r), s in res_forras_sorok().items() if mid == m['id']):
                raise ValueError('%s: az új lapszerkezet lap-forrású rést nem kezel' % m['id'])
            if os.path.exists(cel_ut):
                meglevo_uj, _sorveg, _crlf, _lf = G.eles_fajl_beolvas(cel_ut)
            uj_szoveg = epit_uj_fajl(m, blokkok)
            uj_szoveg = res_blokkok_alkalmaz(uj_szoveg, m)
            uj_szoveg = res_labjegyzetek_alkalmaz(uj_szoveg, m)
            uj_szoveg = _generalt_fejlec_alkalmaz(uj_szoveg, m)
            uj_szoveg = uj_szerkezet_alkalmaz(uj_szoveg, m, sorai)
            uj_szoveg = kiejtes_potol(uj_szoveg, m['id'])
            uj_szoveg = OU.alkalmaz(cimjeloles_ki(uj_szoveg), strong_cim=strong_cim)
            # lap-javit HAMART-001 (a felhasználó átnézése, 2., 12.; „mehet így”): a jegyzetek és a forrássorok olvasói
            # alakja, a 2. és 3. tábla jegyzetei a tábla alatt
            uj_szoveg = TJ.alkalmaz(uj_szoveg)
            allapot = ('új fájl' if meglevo_uj is None else
                       'változatlan' if uj_szoveg == meglevo_uj else 'frissítve')
        elif os.path.exists(cel_ut):
            # B4: LF-re normalizálva (mint a general.eles_fajl_beolvas). A
            # core.autocrlf=true munkapéldánya CRLF-es; nyersen a '\n\n'-re
            # illesztő lépések (pl. res_labjegyzetek_alkalmaz) nem találtak,
            # és a helyben frissített lap két üres sorral tért el az új
            # fájlként generálttól (TEREMT-002, 1A.11, SABLON.6).
            meglevo, _sorveg, _crlf, _lf = G.eles_fajl_beolvas(cel_ut)
            uj_szoveg = frissit_meglevo_fajlt(meglevo, m, blokkok)
            uj_szoveg = res_blokkok_alkalmaz(uj_szoveg, m)
            uj_szoveg = res_labjegyzetek_alkalmaz(uj_szoveg, m)
            uj_szoveg = _generalt_fejlec_alkalmaz(uj_szoveg, m)
            uj_szoveg = kiejtes_potol(uj_szoveg, m['id'])
            uj_szoveg = OU.alkalmaz(cimjeloles_ki(uj_szoveg), strong_cim=strong_cim)
            allapot = 'változatlan' if uj_szoveg == meglevo else 'frissítve'
        else:
            uj_szoveg = epit_uj_fajl(m, blokkok)
            uj_szoveg = res_blokkok_alkalmaz(uj_szoveg, m)
            uj_szoveg = res_labjegyzetek_alkalmaz(uj_szoveg, m)
            uj_szoveg = _generalt_fejlec_alkalmaz(uj_szoveg, m)
            uj_szoveg = kiejtes_potol(uj_szoveg, m['id'])
            uj_szoveg = OU.alkalmaz(cimjeloles_ki(uj_szoveg), strong_cim=strong_cim)
            allapot = 'új fájl'

        if args.ellenoriz:
            print('  %s: --ellenoriz, nincs írás (%s lenne)' % (m['id'], allapot))
            continue

        os.makedirs(kimenet_gyoker, exist_ok=True)
        with io.open(cel_ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(uj_szoveg)
        if uj_szerkezet(m['id']):
            # F182 (A23): a kizárt helyek melléklete a lap mellett (a kapu a kizarasok_adat-ban)
            mell_ut = os.path.join(kimenet_gyoker, '%s%s' % (m['id'], KIZARASOK_UTOTAG))
            with io.open(mell_ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write(kizarasok_melleklet(m, sorai))
            print('  %s: %s (melléklet, %d bájt)' % (m['id'], G.kiirt_ut(mell_ut), os.path.getsize(mell_ut)))
        print('  %s: %s (%s, %d bájt)'
              % (m['id'], G.kiirt_ut(cel_ut), allapot, os.path.getsize(cel_ut)))
        h = KIEJTES_JELOLT_HIANY.get(m['id']) or []
        if h:
            print('    kiejtés-szabály: %d hiány maradt — generált %d (jóváhagyott héber alak nélkül), kézi %d '
                  '(a forrásban javítandó); részletek: python naplok/KIEJTES_elso_elofordulas_meres.py %s'
                  % (len(h), sum(1 for x in h if x[2] == 'generált'), sum(1 for x in h if x[2] == 'kézi'),
                     G.kiirt_ut(cel_ut)))

    print('  tisztázatlan licencű forrás érintett-e (motívumonként): %s'
          % ', '.join('%s=%s' % (k, 'igen' if v else 'nem') for k, v in osszesitett_tisztazatlan.items()))
    return 0
