#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cremer_ocr_javit.py -- CREMER_OCR_BRIEF.md v2, O0-O2: a Cremer-lexikon hOCR-szovegenek
javitasa ket fuggetlen kepolvaso modellel OpenRouteren keresztul.

Alparancsok:
  gyanus   -- egy adott level gyanus szavainak listazasa (fejlesztes/ellenorzes;
              nem hivja a modelleket).
  futtat   -- a fo folyamat egy level-listara: lapkep kivagas a jp2-zipbol,
              hOCR-sorkontextus es gyanus szavak kigyujtese, OpenRouter-hivas
              (C1-C3, JSON-semaval), elonormalizalt egyezes (C4), alakellenorzes
              (C5), usage-alapu koltsegnaplo es -plafon (C6), gyorsitotar (D12).
              --szaraz: hivas nelkul -- csak a bemenet elokeszul, es a becsult
              token- es koltsegigeny keszul jelentesnek (O0.3).
              --csak-dontes: hivas nelkul, a gyorsitotarbol szamolja ujra a
              dontéseket.
              --onteszt: halozat es kulcs nelkuli onellenorzes (l. lent).

CLI:
    python eszkozok/cremer_ocr_javit.py gyanus --level 17
    python eszkozok/cremer_ocr_javit.py futtat --pilot --szaraz
    python eszkozok/cremer_ocr_javit.py futtat --pilot
    python eszkozok/cremer_ocr_javit.py futtat --levelek 17,82,124
    python eszkozok/cremer_ocr_javit.py futtat --onteszt

Az OPENROUTER_API_KEY kulcsot csak kornyezeti valtozobol olvassa; sehova nem
irja ki es nem naplozza -- a gyorsitotar-fajlba sem (csak a valasz torzse es a
hivas metaadatai kerulnek bele, HTTP-fejlec es kulcs nélkül). A
modellazonositokat es -arakat a cremer_ocr_config.json adja.

Kilepesi kod: 0 = rendben, 1 = szabalysertes (hianyzo modell/kulcs, vagy
--pilot nelkuli eles futas -- O2 meg nincs engedelyezve), 2 = hiba (ismeretlen
level), 3 = a koltsegplafon miatt korai leallas.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import io
import json
import os
import random
import re
import shutil
import tempfile
import time
import unicodedata
import zipfile
from datetime import datetime, timezone

REPO_GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NYERS_ALAP = os.path.join(REPO_GYOKER, "konkordancia", "_nyers", "cremer")
HOCR_UTVONAL = os.path.join(NYERS_ALAP, "cu31924098819406_hocr.html")
JP2ZIP_UTVONAL = os.path.join(NYERS_ALAP, "cu31924098819406_jp2.zip")
CONFIG_UTVONAL = os.path.join(REPO_GYOKER, "eszkozok", "cremer_ocr_config.json")
NAPLOK_DIR = os.path.join(REPO_GYOKER, "naplok")
CACHE_DIR = os.path.join(REPO_GYOKER, "konkordancia", "_nyers", "cremer_cache")

PROMPT_VERZIO = "v2"

# C7: pilot -- 7 ismert level (Abbott-Smith-szocikkek + gorog mutato) + a heber
# mutato levele + 12 veletlen level, rogzitett maggal.
PILOT_ISMERT_LEVELEK = [17, 82, 124, 350, 628, 760, 934, 950]
PILOT_VELETLEN_MAG = 20260923
PILOT_VELETLEN_DB = 12
LEVEL_MIN, LEVEL_MAX = 1, 967  # a page_numbers.json szerinti szamozott levelek (SS 0.2)


# ---------------------------------------------------------------------------
# hOCR feldolgozas -- lapindex, majd soronkenti tokenlista
# ---------------------------------------------------------------------------

_PAGE_START_RE = re.compile(rb'<div class=[\'"]ocr_page[\'"] id="page_(\d{6})"')
_LINE_START_RE = re.compile(rb'<span class="ocr_line" id="(?P<lineid>[^"]+)"')
_WORD_RE = re.compile(
    rb'<span class="ocrx_word" id="(?P<id>[^"]+)" '
    rb'title="bbox (?P<x0>\d+) (?P<y0>\d+) (?P<x1>\d+) (?P<y1>\d+); '
    rb'x_wconf (?P<wconf>\d+)[^"]*">(?P<text>.*?)</span>',
    re.DOTALL,
)


def hocr_lapindex_epit(hocr_utvonal=HOCR_UTVONAL):
    """Egyszeri vegigolvasas: level -> (kezdo_byteoffset, zaro_byteoffset) a hOCR-ben."""
    hatarok = []
    with open(hocr_utvonal, "rb") as fh:
        offset = 0
        for sor in fh:
            for m in _PAGE_START_RE.finditer(sor):
                hatarok.append((int(m.group(1)), offset))
            offset += len(sor)
        vegso_offset = offset
    index = {}
    for i, (level, start) in enumerate(hatarok):
        veg = hatarok[i + 1][1] if i + 1 < len(hatarok) else vegso_offset
        index[level] = (start, veg)
    return index


def level_hocr_szoveg(level, lapindex, hocr_utvonal=HOCR_UTVONAL):
    if level not in lapindex:
        raise KeyError("nincs level=%d a hOCR lapindexben" % level)
    start, veg = lapindex[level]
    with open(hocr_utvonal, "rb") as fh:
        fh.seek(start)
        return fh.read(veg - start)


def _html_dekodol(nyers_bytes):
    import html
    return html.unescape(nyers_bytes.decode("utf-8", errors="replace"))


_VEGYES_ESET_RE = re.compile(r"^[A-Za-z]+$")


def gyanus_e(szoveg_nyers, wconf):
    """CREMER_OCR_BRIEF SS1 'Gyanus szo': x_wconf < 60, VAGY latin betus torzkep
    (heurisztika: a betumag nem csupa nagybetu, nem egyszeru Title-eset, de
    van benne kis- ES nagybetu is -- pl. 'ABvocos'). Nem valtozott a v2-ben."""
    if wconf < 60:
        return True
    mag = re.sub(r"[^A-Za-z]", "", szoveg_nyers)
    if len(mag) < 2 or not _VEGYES_ESET_RE.match(mag):
        return False
    van_kicsi = any(c.islower() for c in mag)
    van_nagy = any(c.isupper() for c in mag)
    if not (van_kicsi and van_nagy):
        return False
    if mag.isupper():
        return False
    if mag[0].isupper() and mag[1:].islower():
        return False  # egyszeru Title-eset -- ez normalis angol szo eleje
    return True


def level_sorok(level, lapindex, hocr_utvonal=HOCR_UTVONAL):
    """A level osszes hOCR-sora, soronkent a tokenjeivel. Egy <p class="ocr_par">-on
    belul tobb <span class="ocr_line"> is allhat (nincs mindig </p> hataron), ezert
    a sorhatarokat a kovetkezo sor-kezdo tag (vagy a lap vege) jeloli ki -- nincs
    szukseg teljes HTML-parszolasra, mert a hOCR-export szerkezete flat (a
    sor-spanek soha nem agyazodnak egymasba)."""
    nyers = level_hocr_szoveg(level, lapindex, hocr_utvonal)
    inditasok = [(m.start(), m.group("lineid").decode("ascii")) for m in _LINE_START_RE.finditer(nyers)]
    sorok = []
    for i, (start, sor_id) in enumerate(inditasok):
        veg = inditasok[i + 1][0] if i + 1 < len(inditasok) else len(nyers)
        szegmens = nyers[start:veg]
        szavak = []
        for m in _WORD_RE.finditer(szegmens):
            szavak.append({
                "szo_id": m.group("id").decode("ascii"),
                "bbox": [int(m.group("x0")), int(m.group("y0")), int(m.group("x1")), int(m.group("y1"))],
                "wconf": int(m.group("wconf")),
                "ocr": _html_dekodol(m.group("text")),
            })
        if szavak:
            sorok.append({"sor_id": sor_id, "szavak": szavak})
    return sorok


def level_szavai(level, lapindex, hocr_utvonal=HOCR_UTVONAL):
    """Visszafele kompatibilis lapos lista (a 'gyanus' alparancshoz)."""
    szavak = []
    for sor in level_sorok(level, lapindex, hocr_utvonal):
        szavak.extend(sor["szavak"])
    return szavak


def level_gyanus_szavai(level, lapindex, hocr_utvonal=HOCR_UTVONAL):
    return [sz for sz in level_szavai(level, lapindex, hocr_utvonal) if gyanus_e(sz["ocr"], sz["wconf"])]


# ---------------------------------------------------------------------------
# Lapkep kivagas a jp2-zipbol (C2) -- kicsomagolas nelkul, laponkent
# ---------------------------------------------------------------------------

def level_kep_jpeg(level, max_el_px=2000, jp2zip_utvonal=JP2ZIP_UTVONAL):
    """Egy level kepenek JPEG-bajtjai, a hosszabb el <= max_el_px-re kicsinyitve.
    Visszaadja (jpeg_bytes, eredeti_meret, uj_meret)."""
    from PIL import Image

    nev = "cu31924098819406_jp2/cu31924098819406_%04d.jp2" % level
    with zipfile.ZipFile(jp2zip_utvonal) as z:
        nyers = z.read(nev)
    kep = Image.open(io.BytesIO(nyers))
    kep.load()
    eredeti_meret = kep.size
    hosszabb_el = max(kep.size)
    if hosszabb_el > max_el_px:
        arany = max_el_px / hosszabb_el
        uj_meret = (max(1, round(kep.size[0] * arany)), max(1, round(kep.size[1] * arany)))
        kep = kep.resize(uj_meret, Image.LANCZOS)
    else:
        uj_meret = kep.size
    if kep.mode not in ("L", "RGB"):
        kep = kep.convert("RGB")
    buf = io.BytesIO()
    kep.save(buf, format="JPEG", quality=90)
    return buf.getvalue(), eredeti_meret, uj_meret


def skaloz_bbox(bbox, arany_x, arany_y):
    """D9: az eredeti jp2-koordinatakat a kikuldott JPEG meretere skalazza, egesz
    pixelre kerekitve."""
    return [
        round(bbox[0] * arany_x), round(bbox[1] * arany_y),
        round(bbox[2] * arany_x), round(bbox[3] * arany_y),
    ]


# ---------------------------------------------------------------------------
# C2-C3: payload (sorkontextus + gyanus szavak) es ellenorzo kontextus
# ---------------------------------------------------------------------------

UTASITAS_SZOVEG = (
    "Ez egy 1880-as gorog-angol lexikon (Cremer) beszkennelt lapja. A hOCR "
    "csak angolul olvasta be jol; a gorog/heber szavak (vagy egy-ket romlott "
    "latin betus torzkep) HIANYOZNAK vagy HIBASAK a 'sorok' listaban. Minden "
    "sor a sajat sor_id-javal es a sorban levo OSSZES token (szo_id, hOCR-szoveg) "
    "listajaval szerepel; a 'gyanusak' listaban a valoszinuleg hibas tokenek "
    "vannak kiemelve (wconf es a lapkepen ervenyes bbox). Add vissza SZIGORU "
    "JSON objektumkent: {\"cserek\": [{\"szo_ids\": [...], \"alak\": ..., "
    "\"nyelv\": \"grc\"|\"heb\"|\"lat\", \"extra\": bool}]}. A 'szo_ids' egy "
    "vagy tobb, UGYANAZON sorban EGYMAST KOVETO azonosito (ha a torz szo tobb "
    "hOCR-tokenre esett szet). Az 'alak' irasjel NELKUL ertendo (a program a "
    "hOCR-tokenbol teszi vissza). Nem-extra elemnel a szo_ids kozott legalabb "
    "egy gyanus token legyen. Ha egy sorban olyan gorog/heber torzkepet latsz, "
    "ami NINCS a 'gyanusak' kozott jelolve, jelezd 'extra': true -vel. Ne irj "
    "szabad szoveget, csak ezt a JSON objektumot."
)


def level_payload_es_ctx(level, sorok, eredeti_meret, uj_meret):
    """Osszeallitja a modellnek kuldott payloadot (csak a gyanus szot tartalmazo
    sorok, teljes tokenlistaval) es egy ellenorzo kontextust a valasz
    validalasahoz: id_info[szo_id] = (sor_id, pozicio_a_sorban, gyanus_e)."""
    arany_x = uj_meret[0] / eredeti_meret[0]
    arany_y = uj_meret[1] / eredeti_meret[1]
    sorok_ki = []
    id_info = {}
    osszes_gyanus = 0
    for sor in sorok:
        gyanus_jelzok = [gyanus_e(w["ocr"], w["wconf"]) for w in sor["szavak"]]
        if not any(gyanus_jelzok):
            continue
        tokenek = [[w["szo_id"], w["ocr"]] for w in sor["szavak"]]
        gyanusak = []
        for poz, (w, is_gy) in enumerate(zip(sor["szavak"], gyanus_jelzok)):
            id_info[w["szo_id"]] = (sor["sor_id"], poz, is_gy)
            if is_gy:
                gyanusak.append({
                    "szo_id": w["szo_id"], "wconf": w["wconf"],
                    "bbox": skaloz_bbox(w["bbox"], arany_x, arany_y),
                })
                osszes_gyanus += 1
        sorok_ki.append({"sor_id": sor["sor_id"], "tokenek": tokenek, "gyanusak": gyanusak})
    payload = {
        "level": level,
        "kep_meret": [uj_meret[0], uj_meret[1]],
        "utasitas": UTASITAS_SZOVEG,
        "sorok": sorok_ki,
    }
    ctx = {"id_info": id_info}
    return payload, ctx, osszes_gyanus


# ---------------------------------------------------------------------------
# C3: JSON-sema es a valasz validalasa
# ---------------------------------------------------------------------------

def _json_sema():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "cremer_cserek",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "cserek": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "szo_ids": {"type": "array", "items": {"type": "string"}},
                                "alak": {"type": "string"},
                                "nyelv": {"type": "string", "enum": ["grc", "heb", "lat"]},
                                "extra": {"type": "boolean"},
                            },
                            "required": ["szo_ids", "alak", "nyelv", "extra"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["cserek"],
                "additionalProperties": False,
            },
        },
    }


def _cserek_validal(nyers, ctx):
    """A modell JSON-valaszat ellenorzi (O0.4 §2/3): letezo, egy sorbeli, egymast
    koveto azonositok; nem-extra elemnel legalabb egy gyanus id; atfedes tilos.
    Sikeres validalasnal a szo_ids-t a sorbeli pozicio szerint rendezve adja
    vissza (igy az egyezes-osszevetes ordering-fuggetlen)."""
    if not isinstance(nyers, dict) or not isinstance(nyers.get("cserek"), list):
        raise ValueError("hianyzik vagy ervenytelen a 'cserek' lista")
    eredmeny = []
    hasznalt = set()
    for elem in nyers["cserek"]:
        if not isinstance(elem, dict):
            raise ValueError("a 'cserek' egy eleme nem objektum: %r" % (elem,))
        szo_ids = elem.get("szo_ids")
        alak = elem.get("alak")
        nyelv = elem.get("nyelv")
        extra = bool(elem.get("extra", False))
        if not isinstance(szo_ids, list) or not szo_ids or not all(isinstance(x, str) for x in szo_ids):
            raise ValueError("ervenytelen szo_ids: %r" % (szo_ids,))
        if not isinstance(alak, str) or not alak:
            raise ValueError("ervenytelen alak: %r" % (alak,))
        if nyelv not in ("grc", "heb", "lat"):
            raise ValueError("ervenytelen nyelv: %r" % (nyelv,))
        sor_id = None
        pozicio_map = {}
        for sid in szo_ids:
            info = ctx["id_info"].get(sid)
            if info is None:
                raise ValueError("ismeretlen szo_id: %s" % sid)
            if sor_id is None:
                sor_id = info[0]
            elif info[0] != sor_id:
                raise ValueError("a szo_ids nem egy sorban vannak: %s" % szo_ids)
            pozicio_map[sid] = info[1]
        pozok_rendezett = sorted(pozicio_map.values())
        if pozok_rendezett != list(range(pozok_rendezett[0], pozok_rendezett[-1] + 1)):
            raise ValueError("a szo_ids nem egymast kovetoek: %s" % szo_ids)
        if not extra and not any(ctx["id_info"][sid][2] for sid in szo_ids):
            raise ValueError("nem-extra elemnek legalabb egy gyanus szo_id kell: %s" % szo_ids)
        if hasznalt & set(szo_ids):
            raise ValueError("atfedo szo_ids egy masik elemmel: %s" % szo_ids)
        hasznalt |= set(szo_ids)
        szo_ids_rendezett = sorted(szo_ids, key=lambda s: pozicio_map[s])
        eredmeny.append({"szo_ids": szo_ids_rendezett, "alak": alak, "nyelv": nyelv, "extra": extra})
    return eredmeny


# ---------------------------------------------------------------------------
# Token- es koltsegbecsles (--szaraz, O0.3)
# ---------------------------------------------------------------------------

def kep_token_becsles(uj_meret):
    """Durva, dokumentalt kozelites: pixelenkent kb. 1/750 token (a valodi
    erteket a szolgaltato tokenizalasa adja -- ez csak tervezesi becsles)."""
    szelesseg, magassag = uj_meret
    return max(1, round((szelesseg * magassag) / 750))


def szoveg_token_becsles(szoveg):
    """Durva kozelites: kb. 4 karakter/token (angol/JSON szovegre szokasos ökolszabaly)."""
    return max(1, round(len(szoveg) / 4))


def kimenet_token_becsles(gyanus_db):
    """Durva kozelites: kb. 12 token JSON-elemenkent a cserelistaban."""
    return gyanus_db * 12


def level_becsles(level, lapindex, max_el_px, hocr_utvonal=HOCR_UTVONAL, jp2zip_utvonal=JP2ZIP_UTVONAL):
    sorok = level_sorok(level, lapindex, hocr_utvonal)
    _, eredeti_meret, uj_meret = level_kep_jpeg(level, max_el_px, jp2zip_utvonal)
    payload, _, gyanus_db = level_payload_es_ctx(level, sorok, eredeti_meret, uj_meret)
    payload_szoveg = json.dumps(payload, ensure_ascii=False)
    kep_token = kep_token_becsles(uj_meret)
    szoveg_token = szoveg_token_becsles(payload_szoveg)
    kimenet_token = kimenet_token_becsles(gyanus_db)
    return {
        "level": level,
        "gyanus_db": gyanus_db,
        "eredeti_meret": eredeti_meret,
        "uj_meret": uj_meret,
        "kep_token_becsult": kep_token,
        "szoveg_token_becsult": szoveg_token,
        "bemenet_token_becsult": kep_token + szoveg_token,
        "kimenet_token_becsult": kimenet_token,
    }


# ---------------------------------------------------------------------------
# C5: alakellenorzes a meglevo alaklistakkal / lemmalistakkal
# ---------------------------------------------------------------------------

_gorog_alakok_cache = None
_gorog_szoveg_cache = None
_heber_szoveg_cache = None


def _gorog_alakok_epit():
    """Halmaz a TAGNT_kivonat es LXX_OS 'szoalak'/'lemma'/'Ragozott alak'/'Szoto'
    oszlopaibol -- pontos egyezeshez (C5)."""
    global _gorog_alakok_cache
    if _gorog_alakok_cache is not None:
        return _gorog_alakok_cache
    alakok = set()
    tagnt = os.path.join(REPO_GYOKER, "konkordancia", "TAGNT_kivonat.tsv")
    if os.path.exists(tagnt):
        with open(tagnt, encoding="utf-8") as fh:
            fejlec = fh.readline().rstrip("\n").split("\t")
            try:
                i_ragozott = fejlec.index("Ragozott alak")
                i_szoto = fejlec.index("Szótő")
            except ValueError:
                i_ragozott = i_szoto = None
            if i_ragozott is not None:
                for sor in fh:
                    mezok = sor.rstrip("\n").split("\t")
                    if len(mezok) > max(i_ragozott, i_szoto):
                        alakok.add(elonormalizal(mezok[i_ragozott]))
                        alakok.add(elonormalizal(mezok[i_szoto]))
    lxx_dir = os.path.join(REPO_GYOKER, "konkordancia", "LXX_OS")
    if os.path.isdir(lxx_dir):
        for nev in os.listdir(lxx_dir):
            if not nev.endswith(".tsv"):
                continue
            with open(os.path.join(lxx_dir, nev), encoding="utf-8") as fh:
                fejlec = None
                i_szoalak = i_lemma = None
                for sor in fh:
                    if sor.startswith("#"):
                        continue
                    if fejlec is None:
                        fejlec = sor.rstrip("\n").split("\t")
                        try:
                            i_szoalak = fejlec.index("szoalak")
                            i_lemma = fejlec.index("lemma")
                        except ValueError:
                            i_szoalak = i_lemma = None
                        continue
                    if i_szoalak is None:
                        continue
                    mezok = sor.rstrip("\n").split("\t")
                    if len(mezok) > max(i_szoalak, i_lemma):
                        alakok.add(elonormalizal(mezok[i_szoalak]))
                        alakok.add(elonormalizal(mezok[i_lemma]))
    _gorog_alakok_cache = alakok
    return alakok


def _gorog_szoveg_epit():
    """LSJ_teljes.tsv es TBESG.txt teljes szovege, tartalmazas-alapu kereseshez."""
    global _gorog_szoveg_cache
    if _gorog_szoveg_cache is not None:
        return _gorog_szoveg_cache
    reszek = []
    for nev in ("LSJ_teljes.tsv", "TBESG.txt"):
        p = os.path.join(REPO_GYOKER, "konkordancia", nev)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                reszek.append(fh.read())
    _gorog_szoveg_cache = elonormalizal("\n".join(reszek))
    return _gorog_szoveg_cache


def _heber_szoveg_epit():
    global _heber_szoveg_cache
    if _heber_szoveg_cache is not None:
        return _heber_szoveg_cache
    reszek = []
    for nev in ("TBESH.txt", "BDB_teljes_unabridged.tsv"):
        p = os.path.join(REPO_GYOKER, "konkordancia", nev)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                reszek.append(fh.read())
    _heber_szoveg_cache = elonormalizal("\n".join(reszek))
    return _heber_szoveg_cache


def alak_igazolt_e(alak, nyelv):
    """C5: 'alak_igazolt' -- talalat eseten True, kulonben False (nem hiba,
    l. C5 -- a Cremer klasszikus idezetei tobbnyire nincsenek a listakban)."""
    if not alak:
        return False
    alak_n = elonormalizal(alak)
    if nyelv == "grc":
        if alak_n in _gorog_alakok_epit():
            return True
        return alak_n in _gorog_szoveg_epit()
    if nyelv == "heb":
        return alak_n in _heber_szoveg_epit()
    return False


# ---------------------------------------------------------------------------
# C4: elonormalizalas + dontes (auto / vitas / hianyzo / hiba, extra_auto / extra_vitas)
# ---------------------------------------------------------------------------

_APOSZTROF_KEPEK = ("'", "ʼ", "᾽", "᾿")


def elonormalizal(alak):
    """D11 / C4: NFC, aposztrof-szeru jelek -> U+2019, lunaris szigma -> szigma,
    szovegi szigma -> vegso szigma (ς). Az NFC mellesleg a politonikus oxia- es a
    monotonikus tonos-ekezetet is egyesiti (pl. U+1F79 == NFC-utan U+03CC)."""
    s = unicodedata.normalize("NFC", alak)
    kimenet = []
    for ch in s:
        if ch in _APOSZTROF_KEPEK:
            kimenet.append("’")
        elif ch == "ϲ":  # lunaris szigma
            kimenet.append("σ")
        else:
            kimenet.append(ch)
    s = "".join(kimenet)
    if s.endswith("σ"):
        s = s[:-1] + "ς"
    return s


def dontes(csere1, csere2):
    """csere1, csere2: {'szo_ids':[...], 'alak':..., 'nyelv':...} vagy None.
    'auto' csak akkor, ha a szo_ids, a nyelv es az elonormalizalt alak is
    egyezik; None eseten 'hianyzo'."""
    if csere1 is None or csere2 is None:
        return "hianyzo"
    if (list(csere1["szo_ids"]) == list(csere2["szo_ids"])
            and csere1["nyelv"] == csere2["nyelv"]
            and elonormalizal(csere1["alak"]) == elonormalizal(csere2["alak"])):
        return "auto"
    return "vitas"


def _klaszter_dontes(elemek_m1, elemek_m2, ctx):
    """H4: egy union-find-klaszter (atfedo szo_ids-u m1/m2-elemek) donteset adja.
    Visszaad: (dontes_nev, szo_ids_unio_rendezve, m1_resz, m2_resz)."""
    def unio_rendezve(elemek):
        idk = set()
        for e in elemek:
            idk |= set(e["szo_ids"])
        return sorted(idk, key=lambda sid: ctx["id_info"][sid][1])

    van_m1, van_m2 = bool(elemek_m1), bool(elemek_m2)
    if van_m1 and not van_m2:
        d = "extra_vitas" if elemek_m1[0]["extra"] else "hianyzo"
        return d, unio_rendezve(elemek_m1), elemek_m1, []
    if van_m2 and not van_m1:
        d = "extra_vitas" if elemek_m2[0]["extra"] else "hianyzo"
        return d, unio_rendezve(elemek_m2), [], elemek_m2

    osszes = elemek_m1 + elemek_m2
    mind_extra = all(e["extra"] for e in osszes)
    van_extra = any(e["extra"] for e in osszes)
    if van_extra and not mind_extra:
        return "vitas", unio_rendezve(osszes), elemek_m1, elemek_m2

    if len(elemek_m1) == 1 and len(elemek_m2) == 1 and elemek_m1[0]["szo_ids"] == elemek_m2[0]["szo_ids"]:
        alap = dontes(elemek_m1[0], elemek_m2[0])
    else:
        alap = "vitas"
    vegso = ("extra_auto" if alap == "auto" else "extra_vitas") if mind_extra else alap
    return vegso, unio_rendezve(osszes), elemek_m1, elemek_m2


def level_dontesek(ctx, m1_eredmeny, m2_eredmeny):
    """Egy lap donteseit allitja ossze. m1_eredmeny/m2_eredmeny: 'hiba' (a teljes
    lap sikertelen volt a modellnel), vagy _cserek_validal() listaja. H4: a ket
    modell OSSZES eleme (extra es nem-extra egyutt) union-find-klaszterekbe
    kerul, atfedo szo_ids szerint -- igy az atfedo, de eltero csoportositas is
    'vitas' lesz, nem tunik el ket kulon 'hianyzo' sorkent. Visszaad:
    (sorok, []) -- minden gyanus szo_id pontosan egy sorban, {'szo_ids','dontes',
    'm1','m2','extra'} kulcsokkal (m1/m2: egyetlen csere-dict vagy dict-lista)."""
    gyanus_id_lista = [sid for sid, info in ctx["id_info"].items() if info[2]]
    if m1_eredmeny == "hiba" or m2_eredmeny == "hiba":
        return (
            [{"szo_ids": [sid], "dontes": "hiba", "m1": None, "m2": None, "extra": False}
             for sid in gyanus_id_lista],
            [],
        )

    cimkezett = [("m1", e) for e in m1_eredmeny] + [("m2", e) for e in m2_eredmeny]
    szulo = list(range(len(cimkezett)))

    def gyoker(x):
        while szulo[x] != x:
            szulo[x] = szulo[szulo[x]]
            x = szulo[x]
        return x

    def unio(a, b):
        ra, rb = gyoker(a), gyoker(b)
        if ra != rb:
            szulo[ra] = rb

    elso_elem_indexe = {}
    for i, (_, e) in enumerate(cimkezett):
        for sid in e["szo_ids"]:
            if sid in elso_elem_indexe:
                unio(i, elso_elem_indexe[sid])
            else:
                elso_elem_indexe[sid] = i

    klaszterek = {}
    for i, cimke_e in enumerate(cimkezett):
        klaszterek.setdefault(gyoker(i), []).append(cimke_e)

    sorok = []
    lefedett = set()
    for csoport in klaszterek.values():
        elemek_m1 = [e for f, e in csoport if f == "m1"]
        elemek_m2 = [e for f, e in csoport if f == "m2"]
        dontes_nev, uid_lista, c1_lista, c2_lista = _klaszter_dontes(elemek_m1, elemek_m2, ctx)
        sorok.append({
            "szo_ids": uid_lista,
            "dontes": dontes_nev,
            "m1": c1_lista[0] if len(c1_lista) == 1 else (c1_lista or None),
            "m2": c2_lista[0] if len(c2_lista) == 1 else (c2_lista or None),
            "extra": dontes_nev.startswith("extra_"),
        })
        lefedett |= set(uid_lista)

    for sid in gyanus_id_lista:
        if sid not in lefedett:
            sorok.append({"szo_ids": [sid], "dontes": "hianyzo", "m1": None, "m2": None, "extra": False})

    return sorok, []


# ---------------------------------------------------------------------------
# K3: a javitott sorszoveg osszeallitasa (irasjel a hOCR-tokenbol)
# ---------------------------------------------------------------------------

def szethuz_irasjelek(szoveg):
    """Vezeto/zaro nem-betus karakterek levalasztasa a betumag korul."""
    i = 0
    while i < len(szoveg) and not szoveg[i].isalpha():
        i += 1
    j = len(szoveg)
    while j > i and not szoveg[j - 1].isalpha():
        j -= 1
    return szoveg[:i], szoveg[i:j], szoveg[j:]


def token_csere_szoveg(hocr_tokenek_csoport, alak):
    """E7: osszevont auto cserenel az elso token vezeto es az utolso token zaro
    irasjelet teszi vissza az alak korul."""
    elso_elo, _, _ = szethuz_irasjelek(hocr_tokenek_csoport[0])
    _, _, utolso_uto = szethuz_irasjelek(hocr_tokenek_csoport[-1])
    return elso_elo + alak + utolso_uto


def szoveg_sort_epit(tokenek, auto_cserek):
    """tokenek: [[szo_id, hocr_szoveg], ...] sorrendben. auto_cserek: csak az
    elfogadott ('auto') cserek listaja, {'szo_ids','alak'} kulcsokkal.
    Visszaad: szo_id -> uj_szoveg lekepezes; a nem erintett token valtozatlan
    (K3), az osszevont csoport tobbi azonositoja ures string lesz."""
    ocr_by_id = dict(tokenek)
    uj = dict(ocr_by_id)
    for cs in auto_cserek:
        ids = cs["szo_ids"]
        csoport_szoveg = [ocr_by_id[i] for i in ids]
        uj[ids[0]] = token_csere_szoveg(csoport_szoveg, cs["alak"])
        for tobbi in ids[1:]:
            uj[tobbi] = ""
    return uj


# ---------------------------------------------------------------------------
# OpenRouter-hivas (C1-C3) -- HTTP-szint es JSON-validalasi szint kulon
# ---------------------------------------------------------------------------

class OpenRouterHiba(Exception):
    def __init__(self, uzenet, usage=None):
        super().__init__(uzenet)
        self.usage = usage or {}


def _valodi_http_kuldo(model_id, uzenetek, api_key, extra_parameterek):
    import requests
    return requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        json=dict(model=model_id, messages=uzenetek, temperature=0,
                   usage={"include": True}, **extra_parameterek),
        timeout=120,
    )


def _http_post_nyers(model_id, uzenetek, api_key, extra_parameterek,
                      ujraprobalkozas_http=4, kezdeti_varakozas=2, kuldo=None, alvas=None):
    """O0.4 §2/4: HTTP 429/5xx/idotullepes eseten visszalepeses ujraprobalkozas
    (2, 4, 8, 16 s), utana OpenRouterHiba ('hiba'). Visszaad: (nyers_valasz_json,
    tenylegesen elkuldott HTTP-kerelmek szama) -- H5: a 'kiserletek' oszlophoz."""
    kuldo = kuldo or _valodi_http_kuldo
    alvas = alvas or time.sleep
    import requests

    varakozas = kezdeti_varakozas
    utolso_hiba = None
    for kiserlet in range(ujraprobalkozas_http + 1):
        try:
            valasz = kuldo(model_id, uzenetek, api_key, extra_parameterek)
        except requests.exceptions.RequestException as e:
            utolso_hiba = e
            if kiserlet < ujraprobalkozas_http:
                alvas(varakozas)
                varakozas *= 2
                continue
            raise OpenRouterHiba("halozati hiba %d kiserlet utan: %s" % (kiserlet + 1, e), usage={})
        if valasz.status_code == 429 or valasz.status_code >= 500:
            utolso_hiba = "HTTP %d" % valasz.status_code
            if kiserlet < ujraprobalkozas_http:
                alvas(varakozas)
                varakozas *= 2
                continue
            raise OpenRouterHiba("HTTP hiba %d kiserlet utan: %s" % (kiserlet + 1, utolso_hiba), usage={})
        valasz.raise_for_status()
        return valasz.json(), kiserlet + 1
    raise OpenRouterHiba("nem sikerult a hivas: %s" % utolso_hiba, usage={})


def openrouter_hivas(model_id, kep_jpeg_bytes, payload, api_key, sema, ctx,
                      reasoning=None, ujraprobalkozas_json=1, ujraprobalkozas_http=4, posztolo=None,
                      ar_bemenet_1m=None, ar_kimenet_1m=None):
    """Egy hivas egy modellhez, egy laphoz (C2). posztolo(model_id, uzenetek,
    api_key, extra_parameterek, ujraprobalkozas_http) -> (nyers OpenRouter-valasz
    dict, HTTP-kiserletek szama); alapertelmezesben _http_post_nyers. H5: MINDEN
    JSON-ujraprobalkozasi kiserlet usage-e osszeadodik (token, gondolkodas,
    koltseg) -- a sema-sertes miatt eldobott elso valasz is szamlazott hivas
    volt. Visszaad: (cserek, osszesitett_usage, utolso_nyers_valasz), vagy dobja
    az OpenRouterHiba-t ('hiba') -- ilyenkor a kivetel .usage attributuma az
    addig osszegyult usage-et hordozza."""
    import base64

    posztolo = posztolo or _http_post_nyers
    kep_b64 = base64.b64encode(kep_jpeg_bytes).decode("ascii")
    uzenetek = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": json.dumps(payload, ensure_ascii=False)},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + kep_b64}},
            ],
        }
    ]
    extra_parameterek = {"response_format": sema}
    if reasoning:
        extra_parameterek["reasoning"] = reasoning

    osszes_be = osszes_ki = osszes_gondolkodas = osszes_http_kiserlet = 0
    osszes_koltseg = 0.0
    van_ismeretlen_koltseg = False
    utolso_hiba = None
    osszesitett_usage = {}

    for kiserlet in range(ujraprobalkozas_json + 1):
        nyers_valasz, http_kiserletek = posztolo(model_id, uzenetek, api_key, extra_parameterek, ujraprobalkozas_http)
        osszes_http_kiserlet += http_kiserletek
        usage = nyers_valasz.get("usage") or {}
        be = usage.get("prompt_tokens", 0) or 0
        ki = usage.get("completion_tokens", 0) or 0
        reszletek = usage.get("completion_tokens_details") or {}
        gondolkodas = reszletek.get("reasoning_tokens", 0) or 0
        koltseg = usage.get("cost")
        osszes_be += be
        osszes_ki += ki
        osszes_gondolkodas += gondolkodas
        if koltseg is not None:
            osszes_koltseg += koltseg
        else:
            van_ismeretlen_koltseg = True
            if ar_bemenet_1m is not None:
                osszes_koltseg += be / 1_000_000 * ar_bemenet_1m
            if ar_kimenet_1m is not None:
                osszes_koltseg += ki / 1_000_000 * ar_kimenet_1m
        osszesitett_usage = {
            "prompt_tokens": osszes_be,
            "completion_tokens": osszes_ki,
            "completion_tokens_details": {"reasoning_tokens": osszes_gondolkodas},
            "cost": osszes_koltseg,
            "koltseg_forras": "ar_config" if van_ismeretlen_koltseg else "openrouter",
            "kiserletek": osszes_http_kiserlet,
        }
        tartalom = nyers_valasz["choices"][0]["message"]["content"]
        try:
            cserek = _cserek_validal(json.loads(tartalom), ctx)
            return cserek, osszesitett_usage, nyers_valasz
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            utolso_hiba = e
            continue
    raise OpenRouterHiba(
        "ervenytelen JSON/sema %d kiserlet utan: %s" % (ujraprobalkozas_json + 1, utolso_hiba),
        usage=osszesitett_usage,
    )


# ---------------------------------------------------------------------------
# Gyorsitotar (D12) -- nyers valasz + metaadat, kulcs nelkul, fejlec nelkul
# ---------------------------------------------------------------------------

def _modell_slug(model_id):
    return re.sub(r"[^A-Za-z0-9_-]", "_", model_id)


def cache_utvonal(model_id, level, cache_dir=None):
    cache_dir = cache_dir or CACHE_DIR
    return os.path.join(cache_dir, _modell_slug(model_id), "%04d.json" % level)


def cache_olvas(model_id, level, cache_dir=None):
    p = cache_utvonal(model_id, level, cache_dir)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        adat = json.load(fh)
    if adat.get("prompt_verzio") != PROMPT_VERZIO or adat.get("model") != model_id:
        return None
    return adat


def cache_ir(model_id, level, nyers_valasz, usage, cache_dir=None):
    p = cache_utvonal(model_id, level, cache_dir)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    adat = {
        "model": model_id,
        "level": level,
        "prompt_verzio": PROMPT_VERZIO,
        "ts": datetime.now(timezone.utc).isoformat(),
        "usage": usage,
        "nyers_valasz": nyers_valasz,
    }
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(adat, fh, ensure_ascii=False, indent=1)


def level_modell_hivas(level, model_cfg, payload, ctx, kep_jpeg_bytes, api_key, config,
                        csak_dontes=False, posztolo=None, cache_dir=None):
    """Egy modell egy lapra: gyorsitotarbol, vagy (ha --csak-dontes nincs)
    halozatrol -- ekkor SIKERES valaszt es a hasznalt metaadatokat el is menti
    (H3: 'hiba' valasz SOHA nem kerul a gyorsitotarba, hogy az ujrafutas
    ujraprobalja, ne ragadjon be). Visszaad: (cserek_vagy_'hiba', usage_dict,
    'cache'|'halozat'|None) -- hiba eseten a usage az addig osszegyult (H5)."""
    model_id = model_cfg["nev"]
    talalat = cache_olvas(model_id, level, cache_dir)
    if talalat is not None:
        tartalom = talalat["nyers_valasz"]["choices"][0]["message"]["content"]
        try:
            cserek = _cserek_validal(json.loads(tartalom), ctx)
        except (json.JSONDecodeError, ValueError, KeyError):
            cserek = "hiba"
        return cserek, talalat.get("usage", {}), "cache"

    if csak_dontes:
        return None, {}, None

    ujraprobalkozas_json = config.get("ujraprobalkozas_ervenytelen_json", 1)
    ujraprobalkozas_http = config.get("ujraprobalkozas_http", 4)
    sema = _json_sema()
    try:
        cserek, usage, nyers_valasz = openrouter_hivas(
            model_id, kep_jpeg_bytes, payload, api_key, sema, ctx,
            reasoning=model_cfg.get("reasoning"),
            ujraprobalkozas_json=ujraprobalkozas_json,
            ujraprobalkozas_http=ujraprobalkozas_http,
            posztolo=posztolo,
            ar_bemenet_1m=model_cfg.get("ar_bemenet_usd_per_1M"),
            ar_kimenet_1m=model_cfg.get("ar_kimenet_usd_per_1M"),
        )
    except OpenRouterHiba as e:
        return "hiba", e.usage, "halozat"
    cache_ir(model_id, level, nyers_valasz, usage, cache_dir)
    return cserek, usage, "halozat"


# ---------------------------------------------------------------------------
# Config es koltsegplafon (C6, usage-alapu)
# ---------------------------------------------------------------------------

def config_betolt(utvonal=CONFIG_UTVONAL):
    with open(utvonal, encoding="utf-8") as fh:
        return json.load(fh)


class KoltsegNaplo:
    def __init__(self, plafon_usd):
        self.plafon_usd = plafon_usd
        self.osszeg_usd = 0.0
        self.sorok = []

    def hozzaad_usage(self, level, model_id, usage, ar_bemenet_1m, ar_kimenet_1m):
        """usage: az openrouter_hivas/OpenRouterHiba.usage MAR OSSZESITETT alakja
        (a JSON-ujraprobalkozasok osszes kiserletenek usage-e osszeadva, H5),
        vagy egy nyers, egyszeru {'prompt_tokens':...,'completion_tokens':...}
        (visszafele kompatibilitas)."""
        bemenet = usage.get("prompt_tokens", 0) or 0
        kimenet = usage.get("completion_tokens", 0) or 0
        reszletek = usage.get("completion_tokens_details") or {}
        gondolkodas = reszletek.get("reasoning_tokens", 0) or 0
        kiserletek = usage.get("kiserletek", 1)
        if "koltseg_forras" in usage:
            forras = usage["koltseg_forras"]
            koltseg = usage.get("cost") or 0.0
        else:
            koltseg = usage.get("cost")
            forras = "openrouter"
            if koltseg is None:
                forras = "ar_config"
                koltseg = 0.0
                if ar_bemenet_1m is not None:
                    koltseg += bemenet / 1_000_000 * ar_bemenet_1m
                if ar_kimenet_1m is not None:
                    koltseg += kimenet / 1_000_000 * ar_kimenet_1m
        self.osszeg_usd += koltseg
        sor = {
            "level": level, "model": model_id,
            "bemenet_token": bemenet, "kimenet_token": kimenet, "gondolkodas_token": gondolkodas,
            "koltseg_usd": round(koltseg, 6), "koltseg_forras": forras,
            "futo_osszeg_usd": round(self.osszeg_usd, 6), "kiserletek": kiserletek,
        }
        self.sorok.append(sor)
        return sor

    def plafon_elerve_e(self):
        return self.plafon_usd is not None and self.osszeg_usd >= self.plafon_usd


# ---------------------------------------------------------------------------
# Pilot level-lista (C7)
# ---------------------------------------------------------------------------

def pilot_levelek():
    rng = random.Random(PILOT_VELETLEN_MAG)
    kulon = set(PILOT_ISMERT_LEVELEK)
    veletlen = []
    while len(veletlen) < PILOT_VELETLEN_DB:
        jelolt = rng.randint(LEVEL_MIN, LEVEL_MAX)
        if jelolt not in kulon and jelolt not in veletlen:
            veletlen.append(jelolt)
    return sorted(PILOT_ISMERT_LEVELEK) + sorted(veletlen)


# ---------------------------------------------------------------------------
# TSV-iras (CLAUDE.md szerint -- split/join, nem csv modul)
# ---------------------------------------------------------------------------

O1_CSERE_FEJLEC = ["szo_id", "szo_ids", "level", "bbox", "ocr", "m1", "m2", "dontes", "alak_igazolt", "extra"]
KOLTSEG_FEJLEC = ["level", "model", "bemenet_token", "kimenet_token", "gondolkodas_token",
                   "koltseg_usd", "koltseg_forras", "futo_osszeg_usd", "kiserletek"]


def tsv_ir(utvonal, fejlec, sorok):
    os.makedirs(os.path.dirname(utvonal), exist_ok=True)
    with open(utvonal, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(fejlec) + "\n")
        for sor in sorok:
            fh.write("\t".join(str(sor.get(mezo, "")) for mezo in fejlec) + "\n")


def _bbox_unio(bboxok):
    return [
        min(b[0] for b in bboxok), min(b[1] for b in bboxok),
        max(b[2] for b in bboxok), max(b[3] for b in bboxok),
    ]


def o1_csere_sor_epit(level, ocr_by_id, bbox_by_id, dontes_sor):
    """H2: a bbox az EREDETI (nem skalazott) jp2-bbox -- tobb azonositonal az
    azonositok bbox-ainak uniója. Az m1/m2 mezo 'auto'/'hianyzo'/'extra_*' eseten
    egyetlen csere-dict (vagy None), de H4 miatt 'vitas'-nal lehet tobb elemu
    lista is (ha a ket modell mas-mas alakzatban csoportositott)."""
    ids = dontes_sor["szo_ids"]
    m1, m2 = dontes_sor["m1"], dontes_sor["m2"]
    egyetlen_m1 = m1 if isinstance(m1, dict) else (m1[0] if isinstance(m1, list) and len(m1) == 1 else None)
    alak = egyetlen_m1["alak"] if dontes_sor["dontes"] in ("auto", "extra_auto") and egyetlen_m1 else ""
    nyelv = egyetlen_m1["nyelv"] if dontes_sor["dontes"] in ("auto", "extra_auto") and egyetlen_m1 else ""
    bboxok = [bbox_by_id[i] for i in ids if i in bbox_by_id]
    return {
        "szo_id": ids[0],
        "szo_ids": ",".join(ids),
        "level": level,
        "bbox": json.dumps(_bbox_unio(bboxok)) if bboxok else json.dumps([]),
        "ocr": " ".join(ocr_by_id.get(i, "") for i in ids),
        "m1": json.dumps(m1, ensure_ascii=False) if m1 else "",
        "m2": json.dumps(m2, ensure_ascii=False) if m2 else "",
        "dontes": dontes_sor["dontes"],
        "alak_igazolt": "igen" if alak and alak_igazolt_e(alak, nyelv) else "nem",
        "extra": "igen" if dontes_sor["extra"] else "nem",
    }


# ---------------------------------------------------------------------------
# --onteszt: halozat es kulcs nelkuli onellenorzes (O0.4 §2/8)
# ---------------------------------------------------------------------------

def _ror_valasz(cserek_dict, usage=None):
    """Szintetikus OpenRouter-valasz-boritek egy 'cserek' JSON-testhez."""
    return {
        "choices": [{"message": {"content": json.dumps(cserek_dict, ensure_ascii=False)}}],
        "usage": usage or {"prompt_tokens": 10, "completion_tokens": 5},
    }


def _onteszt_a_bbox_skalazas():
    lapindex = hocr_lapindex_epit()
    sorok = level_sorok(17, lapindex)
    _, eredeti_meret, uj_meret = level_kep_jpeg(17, 2000)
    payload, ctx, _ = level_payload_es_ctx(17, sorok, eredeti_meret, uj_meret)
    elso_gyanus = None
    for sor in payload["sorok"]:
        if sor["gyanusak"]:
            elso_gyanus = sor["gyanusak"][0]
            break
    assert elso_gyanus is not None, "nincs gyanus szo a 17. levelen"
    eredeti_bbox = None
    for sor in sorok:
        for w in sor["szavak"]:
            if w["szo_id"] == elso_gyanus["szo_id"]:
                eredeti_bbox = w["bbox"]
    assert eredeti_bbox is not None
    arany_x = uj_meret[0] / eredeti_meret[0]
    arany_y = uj_meret[1] / eredeti_meret[1]
    vart = [eredeti_bbox[0] * arany_x, eredeti_bbox[1] * arany_y,
            eredeti_bbox[2] * arany_x, eredeti_bbox[3] * arany_y]
    for kapott, v in zip(elso_gyanus["bbox"], vart):
        assert abs(kapott - v) <= 1, "bbox-skalazas eltero: %s vs %s" % (elso_gyanus["bbox"], vart)
    assert 0 <= elso_gyanus["bbox"][0] <= uj_meret[0]
    assert 0 <= elso_gyanus["bbox"][2] <= uj_meret[0]
    assert 0 <= elso_gyanus["bbox"][1] <= uj_meret[1]
    assert 0 <= elso_gyanus["bbox"][3] <= uj_meret[1]


def _onteszt_b_elonormalizalas():
    c_ao1 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "ἀλλ'"}  # ἀλλ'
    c_ao2 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "ἀλλ’"}  # ἀλλ’
    assert dontes(c_ao1, c_ao2) == "auto"

    c_lo1 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "λόγοσ"}  # λόγοσ (nem-vegso szigma vegen)
    c_lo2 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "λόγος"}  # λόγος
    assert dontes(c_lo1, c_lo2) == "auto"

    c_ox1 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "λόγος"}  # λόγος (oxia)
    c_ox2 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "λόγος"}  # λόγος (tonos)
    assert dontes(c_ox1, c_ox2) == "auto"

    c_e1 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "λόγος"}  # λόγος
    c_e2 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "λογος"}  # λογος (ekezet nelkul)
    assert dontes(c_e1, c_e2) == "vitas"

    c_i1 = {"szo_ids": ["a"], "nyelv": "grc", "alak": "x"}
    c_i2 = {"szo_ids": ["a", "b"], "nyelv": "grc", "alak": "x"}
    assert dontes(c_i1, c_i2) == "vitas"


def _onteszt_c_json_feldolgozas():
    ctx = {"id_info": {"a": ("sor1", 0, True), "b": ("sor1", 1, True)}}
    sema = _json_sema()

    # a) ervenyes valasz
    valaszok = iter([(_ror_valasz({"cserek": [{"szo_ids": ["a"], "alak": "λόγος", "nyelv": "grc", "extra": False}]}), 1)])
    cserek, _, _ = openrouter_hivas(
        "m", b"x", {"level": 1}, "kulcs", sema, ctx,
        ujraprobalkozas_json=1, posztolo=lambda *a, **k: next(valaszok),
    )
    assert cserek[0]["szo_ids"] == ["a"]

    # b) ketelemu szo_ids
    valaszok = iter([(_ror_valasz({"cserek": [{"szo_ids": ["b", "a"], "alak": "λόγος", "nyelv": "grc", "extra": False}]}), 1)])
    cserek, _, _ = openrouter_hivas(
        "m", b"x", {"level": 1}, "kulcs", sema, ctx,
        ujraprobalkozas_json=1, posztolo=lambda *a, **k: next(valaszok),
    )
    assert cserek[0]["szo_ids"] == ["a", "b"]  # pozicio szerint rendezve

    # c) semasertes -> egy ujraprobalkozas -> hiba
    hibas = _ror_valasz({"cserek": [{"szo_ids": ["ismeretlen"], "alak": "x", "nyelv": "grc", "extra": False}]})
    valaszok = iter([(hibas, 1), (hibas, 1)])
    hivas_szamlalo = {"n": 0}

    def posztolo_hibas(*a, **k):
        hivas_szamlalo["n"] += 1
        return next(valaszok)

    try:
        openrouter_hivas("m", b"x", {"level": 1}, "kulcs", sema, ctx,
                          ujraprobalkozas_json=1, posztolo=posztolo_hibas)
        raise AssertionError("vart OpenRouterHiba")
    except OpenRouterHiba:
        pass
    assert hivas_szamlalo["n"] == 2, "az egy ujraprobalkozas nem tortent meg"

    # d) HTTP 429 -> ujraprobalkozas -> siker (a _http_post_nyers szinten)
    class _FakeValasz:
        def __init__(self, status_code, body):
            self.status_code = status_code
            self._body = body

        def json(self):
            return self._body

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception("HTTP %d" % self.status_code)

    allapotok = [429, 200]
    testek = [{}, _ror_valasz({"cserek": []})]
    hivas_n = {"n": 0}

    def kuldo(model_id, uzenetek, api_key, extra):
        i = hivas_n["n"]
        hivas_n["n"] += 1
        return _FakeValasz(allapotok[i], testek[i])

    eredmeny, kiserletek = _http_post_nyers("m", [], "kulcs", {}, ujraprobalkozas_http=2,
                                             kezdeti_varakozas=0, kuldo=kuldo, alvas=lambda s: None)
    assert eredmeny == testek[1]
    assert hivas_n["n"] == 2
    assert kiserletek == 2


def _onteszt_d_szovegosszeallitas():
    tokenek = [["w1", "foo"], ["w2", '"ABvocos'], ["w3", "2"], ["w4", "bar,"]]
    cserek = [{"szo_ids": ["w2"], "alak": "ἄβυσσος"}]  # ἄβυσσος
    uj = szoveg_sort_epit(tokenek, cserek)
    assert uj["w1"] == "foo"
    assert uj["w3"] == "2"
    assert uj["w4"] == "bar,"
    assert uj["w2"] == '"ἄβυσσος'

    # osszevont csoport: az elso token vezeto es az utolso token zaro irasjele
    # kerul vissza az alak korul, a masodik azonosito uresen marad
    tokenek2 = [["w1", "(foo"], ["w2", "bar)."]]
    cserek2 = [{"szo_ids": ["w1", "w2"], "alak": "ἄβυσσος"}]
    uj2 = szoveg_sort_epit(tokenek2, cserek2)
    assert uj2["w1"] == "(" + "ἄβυσσος" + ")."
    assert uj2["w2"] == ""


def _onteszt_e_gyorsitotar():
    tmp = tempfile.mkdtemp(prefix="cremer_onteszt_cache_")
    try:
        hivas_szamlalo = {"n": 0}

        def posztolo(model_id, uzenetek, api_key, extra, ujraprobalkozas_http):
            hivas_szamlalo["n"] += 1
            return _ror_valasz({"cserek": []}), 1

        ctx = {"id_info": {}}
        payload = {"level": 1, "sorok": []}
        model_cfg = {"nev": "teszt/onteszt-modell"}
        config = {"ujraprobalkozas_ervenytelen_json": 1, "ujraprobalkozas_http": 0}

        level_modell_hivas(1, model_cfg, payload, ctx, b"x", "kulcs", config,
                            posztolo=posztolo, cache_dir=tmp)
        assert hivas_szamlalo["n"] == 1
        level_modell_hivas(1, model_cfg, payload, ctx, b"x", "kulcs", config,
                            posztolo=posztolo, cache_dir=tmp)
        assert hivas_szamlalo["n"] == 1, "a masodik futasnal a gyorsitotarnak hivas nelkul kellett volna mukodnie"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _onteszt_f_level_dontesek_h4():
    # m1 [a,b], m2 [a] -- atfedo, de eltero csoportositas -> EGY 'vitas' sor, szo_ids=[a,b]
    ctx = {"id_info": {"a": ("sor1", 0, True), "b": ("sor1", 1, True)}}
    m1 = [{"szo_ids": ["a", "b"], "alak": "x", "nyelv": "grc", "extra": False}]
    m2 = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}]
    sorok, extra = level_dontesek(ctx, m1, m2)
    assert extra == []
    assert len(sorok) == 1, "atfedo, de eltero szo_ids-nek egyetlen vitas sort kell adnia: %r" % sorok
    assert sorok[0]["dontes"] == "vitas"
    assert sorok[0]["szo_ids"] == ["a", "b"]

    # ugyanarra az id-re az egyik modell extra, a masik nem -> vitas
    ctx2 = {"id_info": {"a": ("sor1", 0, True)}}
    m1b = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": True}]
    m2b = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}]
    sorok2, _ = level_dontesek(ctx2, m1b, m2b)
    assert len(sorok2) == 1
    assert sorok2[0]["dontes"] == "vitas"

    # csak az egyik modell ad elemet -> hianyzo
    ctx3 = {"id_info": {"a": ("sor1", 0, True)}}
    sorok3, _ = level_dontesek(ctx3, [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}], [])
    assert len(sorok3) == 1
    assert sorok3[0]["dontes"] == "hianyzo"

    # minden gyanus id pontosan egy sorban szerepel (vegyes eset)
    ctx4 = {"id_info": {
        "a": ("sor1", 0, True), "b": ("sor1", 1, True), "c": ("sor1", 2, True), "d": ("sor1", 3, False),
    }}
    m1c = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False},
           {"szo_ids": ["c", "d"], "alak": "y", "nyelv": "grc", "extra": False}]
    m2c = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}]
    sorok4, _ = level_dontesek(ctx4, m1c, m2c)
    osszes_id = sorted(sid for s in sorok4 for sid in s["szo_ids"])
    assert osszes_id == ["a", "b", "c", "d"]
    egyszeri = [sid for s in sorok4 for sid in s["szo_ids"]]
    assert len(egyszeri) == len(set(egyszeri)), "egy azonosito tobb sorban is szerepel"


def _onteszt_g_hiba_nem_cachelt():
    tmp = tempfile.mkdtemp(prefix="cremer_onteszt_hibacache_")
    try:
        ctx = {"id_info": {"a": ("sor1", 0, True)}}
        payload = {"level": 1, "sorok": []}
        model_cfg = {"nev": "teszt/hiba-modell"}
        config = {"ujraprobalkozas_ervenytelen_json": 0, "ujraprobalkozas_http": 0}
        hivas_szamlalo = {"n": 0}
        hibas_valasz = _ror_valasz({"cserek": [{"szo_ids": ["ismeretlen"], "alak": "x", "nyelv": "grc", "extra": False}]})

        def posztolo(model_id, uzenetek, api_key, extra, ujraprobalkozas_http):
            hivas_szamlalo["n"] += 1
            return hibas_valasz, 1

        cserek1, _, honnan1 = level_modell_hivas(1, model_cfg, payload, ctx, b"x", "kulcs", config,
                                                  posztolo=posztolo, cache_dir=tmp)
        assert cserek1 == "hiba"
        assert honnan1 == "halozat"
        assert cache_olvas(model_cfg["nev"], 1, cache_dir=tmp) is None, "hibas valasz nem kerulhet a gyorsitotarba"

        elozo = hivas_szamlalo["n"]
        level_modell_hivas(1, model_cfg, payload, ctx, b"x", "kulcs", config,
                            posztolo=posztolo, cache_dir=tmp)
        assert hivas_szamlalo["n"] == elozo + 1, "a masodik futasnak ujra kellett volna hivnia (nincs gyorsitotar)"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _onteszt_h_usage_osszegzes():
    ctx = {"id_info": {"a": ("sor1", 0, True)}}
    sema = _json_sema()

    hibas = _ror_valasz(
        {"cserek": [{"szo_ids": ["ismeretlen"], "alak": "x", "nyelv": "grc", "extra": False}]},
        usage={"prompt_tokens": 100, "completion_tokens": 20},
    )
    ervenyes = _ror_valasz(
        {"cserek": [{"szo_ids": ["a"], "alak": "λόγος", "nyelv": "grc", "extra": False}]},
        usage={"prompt_tokens": 100, "completion_tokens": 20},
    )
    valaszok = iter([(hibas, 1), (ervenyes, 1)])
    cserek, usage, _ = openrouter_hivas("m", b"x", {"level": 1}, "kulcs", sema, ctx,
                                         ujraprobalkozas_json=1, posztolo=lambda *a, **k: next(valaszok))
    assert cserek[0]["szo_ids"] == ["a"]
    assert usage["prompt_tokens"] == 200, "a ket kiserlet usage-enek ossze kellett volna adodnia"
    assert usage["completion_tokens"] == 40
    assert usage["kiserletek"] == 2

    # hiba esetén is van naplozhato usage, nem nulla tokennel
    hibas2 = _ror_valasz(
        {"cserek": [{"szo_ids": ["ismeretlen"], "alak": "x", "nyelv": "grc", "extra": False}]},
        usage={"prompt_tokens": 50, "completion_tokens": 10},
    )
    valaszok2 = iter([(hibas2, 1), (hibas2, 1)])
    try:
        openrouter_hivas("m", b"x", {"level": 1}, "kulcs", sema, ctx,
                          ujraprobalkozas_json=1, posztolo=lambda *a, **k: next(valaszok2))
        raise AssertionError("vart OpenRouterHiba")
    except OpenRouterHiba as e:
        assert e.usage["prompt_tokens"] == 100, "hiba eseten is az osszegyult usage-nek kell megjelennie"
        assert e.usage["kiserletek"] == 2


def _onteszt_i_vegponttol_vegpontig():
    tmp_kimenet = tempfile.mkdtemp(prefix="cremer_onteszt_e2e_kimenet_")
    tmp_cache = tempfile.mkdtemp(prefix="cremer_onteszt_e2e_cache_")
    try:
        lapindex = hocr_lapindex_epit()
        config = {
            "modellek": {
                "m1": {"nev": "teszt/e2e-m1", "ar_bemenet_usd_per_1M": 0.1, "ar_kimenet_usd_per_1M": 0.1},
                "m2": {"nev": "teszt/e2e-m2", "ar_bemenet_usd_per_1M": 0.1, "ar_kimenet_usd_per_1M": 0.1},
            },
            "koltsegplafon_pilot_usd": 100.0,
            "ujraprobalkozas_ervenytelen_json": 0,
            "ujraprobalkozas_http": 0,
        }
        modellek = config["modellek"]

        def posztolo(model_id, uzenetek, api_key, extra, ujraprobalkozas_http):
            return _ror_valasz({"cserek": []}), 1

        class _Args:
            pilot = True
            csak_dontes = False

        naplok_elotte = os.listdir(NAPLOK_DIR) if os.path.isdir(NAPLOK_DIR) else None
        cache_elotte = os.listdir(CACHE_DIR) if os.path.isdir(CACHE_DIR) else None

        eredmeny = _futtat_eles([17], lapindex, 2000, config, modellek, "fake-kulcs", _Args(),
                                 posztolo=posztolo, cache_dir=tmp_cache)
        assert eredmeny["leallt_plafon_miatt"] is False  # cmd_futtat ekkor 0-val lepne ki

        csere_utvonal = os.path.join(tmp_kimenet, "CREMER_O1_csere.tsv")
        koltseg_utvonal = os.path.join(tmp_kimenet, "CREMER_O1_koltseg.tsv")
        tsv_ir(csere_utvonal, O1_CSERE_FEJLEC, eredmeny["o1_sorok"])
        tsv_ir(koltseg_utvonal, KOLTSEG_FEJLEC, eredmeny["koltseg_sorok"])

        assert os.path.exists(csere_utvonal)
        assert os.path.exists(koltseg_utvonal)

        with open(csere_utvonal, encoding="utf-8") as fh:
            csere_sorok = fh.read().splitlines()
        assert csere_sorok[0].split("\t") == O1_CSERE_FEJLEC
        assert len(csere_sorok) > 1, "nincs csere-sor a 17. levelen"
        bbox_idx = O1_CSERE_FEJLEC.index("bbox")
        for sor in csere_sorok[1:]:
            mezok = sor.split("\t")
            assert mezok[bbox_idx] not in ("", "[]"), "ures bbox mezo: %s" % sor

        with open(koltseg_utvonal, encoding="utf-8") as fh:
            koltseg_sorok = fh.read().splitlines()
        assert koltseg_sorok[0].split("\t") == KOLTSEG_FEJLEC

        naplok_utana = os.listdir(NAPLOK_DIR) if os.path.isdir(NAPLOK_DIR) else None
        cache_utana = os.listdir(CACHE_DIR) if os.path.isdir(CACHE_DIR) else None
        assert naplok_elotte == naplok_utana, "a valodi naplok/ konyvtarat nem szabad erinteni"
        assert cache_elotte == cache_utana, "a valodi gyorsitotar-konyvtarat nem szabad erinteni"
    finally:
        shutil.rmtree(tmp_kimenet, ignore_errors=True)
        shutil.rmtree(tmp_cache, ignore_errors=True)


ONTESZT_AGAK = [
    ("a_bbox_skalazas", _onteszt_a_bbox_skalazas),
    ("b_elonormalizalas", _onteszt_b_elonormalizalas),
    ("c_json_feldolgozas", _onteszt_c_json_feldolgozas),
    ("d_szovegosszeallitas", _onteszt_d_szovegosszeallitas),
    ("e_gyorsitotar", _onteszt_e_gyorsitotar),
    ("f_level_dontesek_h4", _onteszt_f_level_dontesek_h4),
    ("g_hiba_nem_cachelt", _onteszt_g_hiba_nem_cachelt),
    ("h_usage_osszegzes", _onteszt_h_usage_osszegzes),
    ("i_vegponttol_vegpontig", _onteszt_i_vegponttol_vegpontig),
]


def onteszt_futtat():
    ok = True
    for nev, fv in ONTESZT_AGAK:
        try:
            fv()
        except Exception as e:
            ok = False
            print("HIBA  [%s]: %s" % (nev, e), file=sys.stderr)
        else:
            print("OK    [%s]" % nev)
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_gyanus(args):
    lapindex = hocr_lapindex_epit()
    if args.level not in lapindex:
        print("nincs ilyen level a hOCR-ben:", args.level, file=sys.stderr)
        return 2
    gyanus = level_gyanus_szavai(args.level, lapindex)
    print("level %d: %d gyanus szo" % (args.level, len(gyanus)))
    for sz in gyanus:
        print("  %s wconf=%d bbox=%s ocr=%r" % (sz["szo_id"], sz["wconf"], sz["bbox"], sz["ocr"]))
    return 0


def _levelek_argumentumbol(args):
    if args.pilot:
        return pilot_levelek()
    if args.levelek:
        return sorted(int(x) for x in args.levelek.split(","))
    print("adj meg --pilot vagy --levelek LISTAT", file=sys.stderr)
    return None


def cmd_futtat(args):
    if args.onteszt:
        return 0 if onteszt_futtat() else 1

    levelek = _levelek_argumentumbol(args)
    if levelek is None:
        return 2

    config = config_betolt(args.config)
    max_el_px = config.get("kepmeret_max_el_px", 2000)
    lapindex = hocr_lapindex_epit()

    hianyzo_levelek = [lv for lv in levelek if lv not in lapindex]
    if hianyzo_levelek:
        print("HIBA -- nincs a hOCR-ben:", hianyzo_levelek, file=sys.stderr)
        return 2

    if args.szaraz:
        return _futtat_szaraz(levelek, lapindex, max_el_px, config)

    if not args.pilot:
        print("O2 meg nincs engedelyezve -- csak --pilot vagy --szaraz futtathato.", file=sys.stderr)
        return 1

    modellek = config.get("modellek", {})
    hianyzo_modell = [k for k, v in modellek.items() if not v.get("nev")]
    if hianyzo_modell and not args.csak_dontes:
        print(
            "HIBA -- a config.modellek alatt nincs kitoltve a nev: %s "
            "(l. CREMER_OCR_BRIEF.md C1)" % hianyzo_modell,
            file=sys.stderr,
        )
        return 1

    api_key = None
    if not args.csak_dontes:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            print("HIBA -- az OPENROUTER_API_KEY kornyezeti valtozo nincs beallitva", file=sys.stderr)
            return 1

    eredmeny = _futtat_eles(levelek, lapindex, max_el_px, config, modellek, api_key, args)

    csere_utvonal = os.path.join(args.kimenet_dir, "CREMER_O1_csere.tsv")
    koltseg_utvonal = os.path.join(args.kimenet_dir, "CREMER_O1_koltseg.tsv")
    tsv_ir(csere_utvonal, O1_CSERE_FEJLEC, eredmeny["o1_sorok"])
    tsv_ir(koltseg_utvonal, KOLTSEG_FEJLEC, eredmeny["koltseg_sorok"])

    _futtat_osszesito_kiir(eredmeny, csere_utvonal, koltseg_utvonal)

    if eredmeny["leallt_plafon_miatt"]:
        print("\nA futas a koltsegplafon miatt korabban leallt.", file=sys.stderr)
        return 3
    return 0


def _futtat_osszesito_kiir(eredmeny, csere_utvonal, koltseg_utvonal):
    print("\n=== osszesito ===")
    print("kiirva:", csere_utvonal)
    print("kiirva:", koltseg_utvonal)
    szamlalo = {}
    for sor in eredmeny["o1_sorok"]:
        szamlalo[sor["dontes"]] = szamlalo.get(sor["dontes"], 0) + 1
    for d, n in sorted(szamlalo.items()):
        print("  %-12s %d" % (d, n))
    osszkoltseg = sum(s["koltseg_usd"] for s in eredmeny["koltseg_sorok"])
    osszgondolkodas = sum(s["gondolkodas_token"] for s in eredmeny["koltseg_sorok"])
    print("osszkoltseg: %.6f USD" % osszkoltseg)
    print("gondolkodasi token osszesen:", osszgondolkodas)


def _futtat_szaraz(levelek, lapindex, max_el_px, config):
    print("=== --szaraz: bemenet elokeszitese, %d level ===" % len(levelek))
    osszes_bemenet = 0
    osszes_kimenet = 0
    osszes_gyanus = 0
    modellek = config.get("modellek", {})
    aktiv_modellek = list(modellek.keys()) or ["m1", "m2"]
    for level in levelek:
        b = level_becsles(level, lapindex, max_el_px)
        osszes_bemenet += b["bemenet_token_becsult"]
        osszes_kimenet += b["kimenet_token_becsult"]
        osszes_gyanus += b["gyanus_db"]
        print(
            "level %4d: gyanus=%3d kep=%s->%s bemenet~%5d token kimenet~%4d token"
            % (level, b["gyanus_db"], b["eredeti_meret"], b["uj_meret"],
               b["bemenet_token_becsult"], b["kimenet_token_becsult"])
        )

    hivasok_db = len(levelek) * max(1, len(aktiv_modellek))
    print("\n--- osszesites (%d level x %d modell = %d hivas) ---" % (
        len(levelek), len(aktiv_modellek), hivasok_db))
    print("osszes gyanus szo:", osszes_gyanus)
    print("becsult bemenet token (egy modellel, a pilotra):", osszes_bemenet)
    print("becsult kimenet token (egy modellel, a pilotra):", osszes_kimenet)

    print("\n--- modellenkenti becsles (config-arak) ---")
    koltseg_pilot_osszesen = 0.0
    koltseg_kotet_osszesen = 0.0
    kotet_szorzo = LEVEL_MAX / len(levelek)
    for kulcs, m in modellek.items():
        nev = m.get("nev") or "(nincs megadva)"
        ar_be = m.get("ar_bemenet_usd_per_1M")
        ar_ki = m.get("ar_kimenet_usd_per_1M")
        if ar_be is not None and ar_ki is not None:
            koltseg_pilot = osszes_bemenet / 1_000_000 * ar_be + osszes_kimenet / 1_000_000 * ar_ki
            koltseg_kotet = koltseg_pilot * kotet_szorzo
            koltseg_pilot_osszesen += koltseg_pilot
            koltseg_kotet_osszesen += koltseg_kotet
            print("  %s (%s): pilot ~%.4f USD, teljes kotet (~%d lap) ~%.2f USD [gondolkodasi token nelkul]"
                  % (kulcs, nev, koltseg_pilot, LEVEL_MAX, koltseg_kotet))
        else:
            print("  %s (%s): ar nincs megadva a configban -- koltseg ismeretlen" % (kulcs, nev))

    if koltseg_pilot_osszesen:
        print("\nbecsult koltseg osszesen (mindket modellel, gondolkodas nelkul): pilot ~%.4f USD, "
              "teljes kotet ~%.2f USD" % (koltseg_pilot_osszesen, koltseg_kotet_osszesen))

    print("\nmegjegyzes: a fenti tokenszamok tervezesi kozelitesek "
          "(kep ~pixel/750, szoveg ~karakter/4), es NEM tartalmazzak a gondolkodasi "
          "tokeneket (m2 'low' reasoning) -- a valodi, usage-alapu koltseget csak a "
          "pilot-futas (O1) koltsegnaploja adja meg pontosan (C6).")
    return 0


def _futtat_eles(levelek, lapindex, max_el_px, config, modellek, api_key, args,
                  posztolo=None, cache_dir=None):
    koltsegplafon = config.get("koltsegplafon_pilot_usd" if args.pilot else "koltsegplafon_usd")
    naplo = KoltsegNaplo(koltsegplafon)
    o1_sorok = []
    leallt_plafon_miatt = False
    modell_kulcsok = list(modellek.keys())
    k1 = modell_kulcsok[0] if len(modell_kulcsok) >= 1 else None
    k2 = modell_kulcsok[1] if len(modell_kulcsok) >= 2 else k1

    for level in levelek:
        if not args.csak_dontes and naplo.plafon_elerve_e():
            print("koltsegplafon elerve, leallas level=%d elott" % level, file=sys.stderr)
            leallt_plafon_miatt = True
            break

        sorok = level_sorok(level, lapindex)
        kep_bytes, eredeti_meret, uj_meret = level_kep_jpeg(level, max_el_px)
        payload, ctx, gyanus_db = level_payload_es_ctx(level, sorok, eredeti_meret, uj_meret)
        if gyanus_db == 0:
            continue

        ocr_by_id = {w["szo_id"]: w["ocr"] for sor in sorok for w in sor["szavak"]}
        bbox_by_id = {w["szo_id"]: w["bbox"] for sor in sorok for w in sor["szavak"]}

        eredmenyek = {}
        for kulcs in dict.fromkeys([k1, k2]):
            if kulcs is None:
                continue
            m_cfg = modellek[kulcs]
            cserek, usage, honnan = level_modell_hivas(
                level, m_cfg, payload, ctx, kep_bytes, api_key, config,
                csak_dontes=args.csak_dontes, posztolo=posztolo, cache_dir=cache_dir,
            )
            eredmenyek[kulcs] = cserek
            if honnan == "halozat":
                naplo.hozzaad_usage(level, m_cfg["nev"], usage,
                                     m_cfg.get("ar_bemenet_usd_per_1M"), m_cfg.get("ar_kimenet_usd_per_1M"))

        if eredmenyek.get(k1) is None or eredmenyek.get(k2) is None:
            continue  # --csak-dontes es nincs meg gyorsitotar-talalat ehhez a laphoz

        nem_extra, extra = level_dontesek(ctx, eredmenyek[k1], eredmenyek[k2])
        for d_sor in nem_extra + extra:
            o1_sorok.append(o1_csere_sor_epit(level, ocr_by_id, bbox_by_id, d_sor))

    return {
        "o1_sorok": o1_sorok, "koltseg_sorok": naplo.sorok, "naplo": naplo,
        "leallt_plafon_miatt": leallt_plafon_miatt,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="parancs", required=True)

    ap_gyanus = sub.add_parser("gyanus", help="egy level gyanus szavai")
    ap_gyanus.add_argument("--level", type=int, required=True)
    ap_gyanus.set_defaults(func=cmd_gyanus)

    ap_futtat = sub.add_parser("futtat", help="a fo folyamat")
    ap_futtat.add_argument("--pilot", action="store_true")
    ap_futtat.add_argument("--levelek", type=str, default=None, help="veszovel elvalasztott level-lista")
    ap_futtat.add_argument("--szaraz", action="store_true", help="hivas nelkul: csak bemenet + becsles")
    ap_futtat.add_argument("--csak-dontes", dest="csak_dontes", action="store_true",
                            help="hivas nelkul, a gyorsitotarbol szamolja ujra a donteseket")
    ap_futtat.add_argument("--onteszt", action="store_true",
                            help="halozat es kulcs nelkuli onellenorzes; a tobbi kapcsolot figyelmen kivul hagyja")
    ap_futtat.add_argument("--config", type=str, default=CONFIG_UTVONAL)
    ap_futtat.add_argument("--kimenet-dir", dest="kimenet_dir", type=str, default=NAPLOK_DIR,
                            help="hova irja a CREMER_O1_csere.tsv / CREMER_O1_koltseg.tsv fajlokat")
    ap_futtat.set_defaults(func=cmd_futtat)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
