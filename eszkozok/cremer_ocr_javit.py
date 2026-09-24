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
level), 3 = a koltsegplafon miatt korai leallas, 4 = a 'hiba' sorok aranya a
futas vegen > 10% (D15).
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
HIBA_DIR = os.path.join(REPO_GYOKER, "konkordancia", "_nyers", "cremer_hibak")

PROMPT_VERZIO = "v5"
# O0.5e/7: a v4 -> v5 valtas csak a modellnek kuldott UTASITAS_SZOVEG-et es a
# validalas szemantikajat (Qwen-zaj kulon kezelese) erintette, a tenyleges
# JSON-huzal-formatumot ("i"/"a"/"l"/"x") NEM -- egy v4-es sikeres valasz
# tartalma szerkezetileg ervenyes es ujraertelmezheto a v5 szabalyokkal is.
# Ezert a gyorsitotar-olvasas a v4-et is elfogadja: egy folytatott/megismetelt
# futas nem hivja ujra azokat a lapokat, amik mar sikerrel lekerultek v4 alatt.
PROMPT_VERZIO_KOMPATIBILIS = {"v4", "v5"}

# C7: pilot -- 7 ismert level (Abbott-Smith-szocikkek + gorog mutato) + a heber
# mutato levele + 12 veletlen level, rogzitett maggal.
PILOT_ISMERT_LEVELEK = [17, 82, 124, 350, 628, 760, 934, 950]
PILOT_VELETLEN_MAG = 20260923
PILOT_VELETLEN_DB = 12
LEVEL_MIN, LEVEL_MAX = 1, 967  # a page_numbers.json szerinti szamozott levelek (SS 0.2)

HIBA_ARANY_KUSZOB = 0.10  # D15: ha a futas vegen a 'hiba' sorok aranya ennel nagyobb, kilepesi kod 4


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
    "sor a sajat sor_id-javal es a sorban levo OSSZES token (egesz azonosito, "
    "hOCR-szoveg) listajaval szerepel; a 'gyanusak' listaban a valoszinuleg "
    "hibas tokenek vannak kiemelve ('i'=azonosito, wconf, es a lapkepen "
    "ervenyes bbox). Add vissza SZIGORU JSON objektumkent: {\"cserek\": "
    "[{\"i\": [...], \"a\": ..., \"l\": \"grc\"|\"heb\"|\"lat\", \"x\": true}]}. "
    "Mezok: 'i' = az azonositok listaja, 'a' = a javasolt alak, 'l' = nyelv, "
    "'x' = csak akkor szerepeljen, ha true (kulonben hagyd ki). Az 'i' egy "
    "vagy tobb, UGYANAZON sorban EGYMAST KOVETO azonosito -- KIZAROLAG akkor, "
    "ha EGYETLEN torz szo esett szet tobb egymas melletti hOCR-tokenre (pl. "
    "egy szohoz tartozo idezojel es betuk kulon tokenkent). HA UGYANAZ A SZO "
    "KETSZER (vagy tobbszor) jelenik meg a sorban NEM-SZOMSZEDOS helyeken -- "
    "peldaul egy elofejben 'CIMSZO [oldalszam] CIMSZO' mintazatban --, az KET "
    "(vagy tobb) KULON cserek-elem, KULON-KULON 'i'-vel, MEG AKKOR IS, ha az "
    "alakjuk azonos. Az 'i' SOHA nem fog at tavoli, kulonallo elofordulasokat, "
    "csak egyetlen szo egybefuggo toredekeit. Az 'a' irasjel NELKUL ertendo "
    "(a program a hOCR-tokenbol teszi vissza). SZIGORUAN TILOS elemet adni "
    "olyan tokenre, ami NINCS a 'gyanusak' listaban, KIVEVE ha ott gorog vagy "
    "heber torzkepet latsz -- ekkor \"x\": true KOTELEZO. Ha egy 'gyanusak'-ban "
    "jelolt token szerinted VALOJABAN HELYES (nem kell javitani), egyszeruen "
    "NE adj ra elemet -- ne is emlitsd. Osszefoglalva: nem-'x' elem CSAK "
    "'gyanusak'-beli azonositot tartalmazhat; minden mas tokenre vonatkozo "
    "elemnel \"x\": true KOTELEZO, kulonben az elemet eldobjuk. Ne irj szabad "
    "szoveget, csak ezt a JSON objektumot."
)


def level_payload_es_ctx(level, sorok, eredeti_meret, uj_meret):
    """Osszeallitja a modellnek kuldott payloadot (csak a gyanus szot tartalmazo
    sorok, teljes tokenlistaval) es egy ellenorzo kontextust a valasz
    validalasahoz. O0.5c/1: a hOCR szo_id (pl. 'word_000017_000123') helyett a
    payloadban laponkenti, 0-tol indulo EGESZ sorszam megy ki a modellnek --
    rovidebb, olcsobb kimenet -- es az eszkoz kepezi vissza a valodi szo_id-ra
    (ctx['id_terkep']). id_info[int_id] = (sor_id, pozicio_a_sorban, gyanus_e)."""
    arany_x = uj_meret[0] / eredeti_meret[0]
    arany_y = uj_meret[1] / eredeti_meret[1]
    sorok_ki = []
    id_info = {}
    id_terkep = {}
    kovetkezo_int_id = 0
    osszes_gyanus = 0
    for sor in sorok:
        gyanus_jelzok = [gyanus_e(w["ocr"], w["wconf"]) for w in sor["szavak"]]
        if not any(gyanus_jelzok):
            continue
        tokenek = []
        gyanusak = []
        for poz, (w, is_gy) in enumerate(zip(sor["szavak"], gyanus_jelzok)):
            int_id = kovetkezo_int_id
            kovetkezo_int_id += 1
            id_terkep[int_id] = w["szo_id"]
            id_info[int_id] = (sor["sor_id"], poz, is_gy)
            tokenek.append([int_id, w["ocr"]])
            if is_gy:
                gyanusak.append({
                    "i": int_id, "wconf": w["wconf"],
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
    ctx = {"id_info": id_info, "id_terkep": id_terkep}
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
                                "i": {"type": "array", "items": {"type": "integer"}},
                                "a": {"type": "string"},
                                "l": {"type": "string", "enum": ["grc", "heb", "lat"]},
                                "x": {"type": "boolean"},
                            },
                            "required": ["i", "a", "l"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["cserek"],
                "additionalProperties": False,
            },
        },
    }


class _NemGyanusZaj(ValueError):
    """O0.5e/2: a Qwen-zaj kulon kategoria -- egy egyebkent szerkezetileg
    ervenyes elem, ami nem-'x'-kent olyan azonositokra vonatkozik, amik kozul
    egy sem gyanus. Ez NEM szamit sema-sertesnek (nem lassitja/buktatja az
    50%-os kuszobot), csak elvetett zaj."""
    pass


def _cserek_validal(nyers, ctx):
    """A modell JSON-valaszat ellenorzi (D15: elemszintu validalas; O0.5c/1-2:
    tomor 'i'/'a'/'l'/'x' mezok es rovid egesz azonositok; O0.5e/1-2: harmas
    bontas). Letezo, egy sorbeli, egymast koveto azonositok; atfedes tilos.
    A 'cserek' lista MEGLETE es tipusa a teljes valaszra vonatkozo, tovabbra
    is kivetelt dob (ez a hivo oldalon meg mindig 'egesz valasz ervenytelen'
    -- ujraprobalkozas, utana hiba). Egy-egy ELEM problemaja NEM dob kivetelt
    a teljes valaszra: valodi SZERKEZETI hiba (ismeretlen/nem-szomszedos/
    tobb-soros/atfedo azonosito, hianyzo mezo) az 'ervenytelen' listaba kerul
    (D15: ez SZAMIT az 50%-os kuszobbe). A 'Qwen-zaj' -- szerkezetileg rendben
    levo, de nem-'x'-kent csupa nem-gyanus azonositora vonatkozo elem -- kulon
    'elvetett_nem_gyanus' listaba kerul, es NEM SZAMIT bele a kuszobbe (O0.5e/2
    -- a D17 dontes oka). Sikeres elemnel a rovid 'i' egesz azonositok a
    ctx['id_terkep'] szerint VISSZAKEPEZODNEK a valodi hOCR szo_id-ra (str),
    sorbeli pozicio szerint rendezve -- a visszaadott elem a tovabbi
    feldolgozashoz (level_dontesek, tsv-iras) a regi belso alakot hasznalja:
    {"szo_ids": [str, ...], "alak": str, "nyelv": str, "extra": bool}.
    Visszaad: (ervenyes_elemek, ervenytelen_elemek, elvetett_nem_gyanus_elemek)
    -- az utobbi ketto: [{"elem": <nyers elem>, "hiba": <szoveg>}, ...]."""
    if not isinstance(nyers, dict) or not isinstance(nyers.get("cserek"), list):
        raise ValueError("hianyzik vagy ervenytelen a 'cserek' lista")
    id_info = ctx["id_info"]
    id_terkep = ctx["id_terkep"]
    ervenyes = []
    ervenytelen = []
    elvetett_nem_gyanus = []
    hasznalt = set()
    for elem in nyers["cserek"]:
        try:
            if not isinstance(elem, dict):
                raise ValueError("a 'cserek' egy eleme nem objektum: %r" % (elem,))
            i_lista = elem.get("i")
            alak = elem.get("a")
            nyelv = elem.get("l")
            extra = bool(elem.get("x", False))
            if (not isinstance(i_lista, list) or not i_lista
                    or not all(isinstance(x, int) and not isinstance(x, bool) for x in i_lista)):
                raise ValueError("ervenytelen 'i': %r" % (i_lista,))
            if not isinstance(alak, str) or not alak:
                raise ValueError("ervenytelen 'a': %r" % (alak,))
            if nyelv not in ("grc", "heb", "lat"):
                raise ValueError("ervenytelen 'l': %r" % (nyelv,))
            sor_id = None
            pozicio_map = {}
            for iid in i_lista:
                info = id_info.get(iid)
                if info is None:
                    raise ValueError("ismeretlen azonosito: %s" % iid)
                if sor_id is None:
                    sor_id = info[0]
                elif info[0] != sor_id:
                    raise ValueError("az 'i' nem egy sorban van: %s" % i_lista)
                pozicio_map[iid] = info[1]
            pozok_rendezett = sorted(pozicio_map.values())
            if pozok_rendezett != list(range(pozok_rendezett[0], pozok_rendezett[-1] + 1)):
                raise ValueError("az 'i' nem egymast kovetoek: %s" % i_lista)
            if not extra and not any(id_info[iid][2] for iid in i_lista):
                raise _NemGyanusZaj("nem-'x' elem, egyetlen gyanus azonosito nelkul: %s" % i_lista)
            i_rendezett = sorted(i_lista, key=lambda x: pozicio_map[x])
            szo_ids_rendezett = [id_terkep[iid] for iid in i_rendezett]
            if hasznalt & set(szo_ids_rendezett):
                raise ValueError("atfedo azonositok egy korabbi ervenyes elemmel: %s" % szo_ids_rendezett)
            hasznalt |= set(szo_ids_rendezett)
            ervenyes.append({"szo_ids": szo_ids_rendezett, "alak": alak, "nyelv": nyelv, "extra": extra})
        except _NemGyanusZaj as e:
            elvetett_nem_gyanus.append({"elem": elem, "hiba": str(e)})
        except ValueError as e:
            ervenytelen.append({"elem": elem, "hiba": str(e)})
    return ervenyes, ervenytelen, elvetett_nem_gyanus


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
    O0.5e/1: ha csak az egyik modellnek van eleme a klaszterben (nem-extra),
    a dontes 'hianyzo_m1' vagy 'hianyzo_m2' -- megjelolve, melyik modell ADOTT
    elemet (a masik hallgatasa "megtartanam a hOCR-alakot" -- ez mar nem
    'valtozatlan', mert az EGYIK modell javasolt valamit). Visszaad:
    (dontes_nev, szo_ids_unio_rendezve, m1_resz, m2_resz)."""
    def unio_rendezve(elemek):
        idk = set()
        for e in elemek:
            idk |= set(e["szo_ids"])
        return sorted(idk, key=lambda sid: ctx["id_info"][sid][1])

    van_m1, van_m2 = bool(elemek_m1), bool(elemek_m2)
    if van_m1 and not van_m2:
        d = "extra_vitas" if elemek_m1[0]["extra"] else "hianyzo_m1"
        return d, unio_rendezve(elemek_m1), elemek_m1, []
    if van_m2 and not van_m1:
        d = "extra_vitas" if elemek_m2[0]["extra"] else "hianyzo_m2"
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
    # ctx['id_info'] a rovid EGESZ azonositokkal van kulcsolva (O0.5c), de az
    # m1_eredmeny/m2_eredmeny elemei mar a VISSZAKEPEZETT hOCR szo_id (str)
    # stringeket hasznaljak (_cserek_validal). A _klaszter_dontes ezert egy
    # string-kulcsu id_info-t var -- kulonben KeyError-ral all le (dokumentalt
    # eset: az elso O1.1-ujraindulas ezzel a hibaval bukott el a 17. levelen).
    id_terkep = ctx["id_terkep"]
    string_id_info = {id_terkep[iid]: info for iid, info in ctx["id_info"].items()}
    string_ctx = {"id_info": string_id_info}
    gyanus_id_lista = [sid for sid, info in string_id_info.items() if info[2]]
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
        dontes_nev, uid_lista, c1_lista, c2_lista = _klaszter_dontes(elemek_m1, elemek_m2, string_ctx)
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
            # O0.5e/1: egyik modell sem adott elemet -- mindketto megtartana a
            # hOCR-alakot, ez 'valtozatlan' (nem 'hianyzo', ami mostantol csak
            # a "pontosan az egyik modell adott elemet" esetet jeloli)
            sorok.append({"szo_ids": [sid], "dontes": "valtozatlan", "m1": None, "m2": None, "extra": False})

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
        if valasz.status_code >= 400:
            # 4xx: kliens-hiba (pl. a modell nem fogadja el a reasoning parametert)
            # -- ujraprobalkozas nem segitene, azonnal 'hiba'
            szoveg = ""
            try:
                szoveg = valasz.text[:300]
            except Exception:
                pass
            raise OpenRouterHiba("HTTP kliens-hiba %d: %s" % (valasz.status_code, szoveg), usage={})
        return valasz.json(), kiserlet + 1
    raise OpenRouterHiba("nem sikerult a hivas: %s" % utolso_hiba, usage={})


ELEM_HIBAARANY_KUSZOB = 0.5  # D15: ha egy modell elemeinek tobb mint fele semasertes -> ujraprobalkozas, utana hiba


def openrouter_hivas(model_id, kep_jpeg_bytes, payload, api_key, sema, ctx,
                      reasoning=None, ujraprobalkozas_json=1, ujraprobalkozas_http=4, posztolo=None,
                      ar_bemenet_1m=None, ar_kimenet_1m=None, hiba_naplo_dir=None):
    """Egy hivas egy modellhez, egy laphoz (C2). posztolo(model_id, uzenetek,
    api_key, extra_parameterek, ujraprobalkozas_http) -> (nyers OpenRouter-valasz
    dict, HTTP-kiserletek szama); alapertelmezesben _http_post_nyers. H5: MINDEN
    JSON-ujraprobalkozasi kiserlet usage-e osszeadodik (token, gondolkodas,
    koltseg) -- a sema-sertes miatt eldobott elso valasz is szamlazott hivas
    volt. D15: a 'cserek' letezese/tipusa vagy maga a JSON ervenytelensege
    tovabbra is a teljes valaszt bukdtatja (ujraprobalkozas, utana 'hiba'), DE
    egy-egy ELEM semasertese onmagaban NEM -- csak az az elem esik ki (a
    hibanaploba kerul), a tobbi ervenyes elem hasznalhato marad. Ha egy
    valaszban az ELEM_HIBAARANY_KUSZOB-nal (0.5) tobb elem semasertes, az
    egesz valasz ugy szamit, mintha a JSON lenne ervenytelen (ujraprobalkozas,
    utana 'hiba'). Visszaad: (ervenyes_cserek, osszesitett_usage,
    utolso_nyers_valasz), vagy dobja az OpenRouterHiba-t ('hiba') -- ilyenkor
    a kivetel .usage attributuma az addig osszegyult usage-et hordozza."""
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
            nyers_json = json.loads(tartalom)
            ervenyes, ervenytelen, elvetett_nem_gyanus = _cserek_validal(nyers_json, ctx)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            utolso_hiba = e
            continue

        if ervenytelen or elvetett_nem_gyanus:
            hiba_naplo_ir(model_id, payload.get("level"), kiserlet + 1, ervenytelen,
                          elvetett_nem_gyanus, hiba_naplo_dir)

        # O0.5e/2: az elvetett_nem_gyanus (Qwen-zaj) NEM szamit bele a kuszobbe
        elem_szam = len(ervenyes) + len(ervenytelen)
        if elem_szam > 0 and len(ervenytelen) / elem_szam > ELEM_HIBAARANY_KUSZOB:
            utolso_hiba = "elemek tobb mint fele semasertes (%d/%d)" % (len(ervenytelen), elem_szam)
            continue

        return ervenyes, osszesitett_usage, nyers_valasz
    raise OpenRouterHiba(
        "ervenytelen JSON/sema %d kiserlet utan: %s" % (ujraprobalkozas_json + 1, utolso_hiba),
        usage=osszesitett_usage,
    )


# ---------------------------------------------------------------------------
# Gyorsitotar (D12) -- nyers valasz + metaadat, kulcs nelkul, fejlec nelkul
# ---------------------------------------------------------------------------

def _modell_slug(model_id):
    return re.sub(r"[^A-Za-z0-9_-]", "_", model_id)


def hiba_naplo_ir(model_id, level, kiserlet, ervenytelen_elemek, elvetett_nem_gyanus_elemek=None, hiba_dir=None):
    """D15/O0.5e: a semasertes miatt elvetett ('ervenytelen_elemek', SZAMIT az
    50%-os kuszobbe) es a Qwen-zaj miatt elvetett ('elvetett_nem_gyanus_elemek',
    NEM szamit bele) elemek NYERSEN, kulcs es HTTP-fejlec nelkul --
    konkordancia/_nyers/cremer_hibak/<modell_slug>/<level:04d>_<kiserlet>.json.
    Ez NEM gyorsitotar: ujrafutaskor sosem olvassa vissza senki."""
    hiba_dir = hiba_dir or HIBA_DIR
    p = os.path.join(hiba_dir, _modell_slug(model_id), "%04d_%d.json" % (int(level), int(kiserlet)))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    adat = {
        "model": model_id,
        "level": level,
        "kiserlet": kiserlet,
        "ts": datetime.now(timezone.utc).isoformat(),
        "ervenytelen_elemek": ervenytelen_elemek,
        "elvetett_nem_gyanus_elemek": elvetett_nem_gyanus_elemek or [],
    }
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(adat, fh, ensure_ascii=False, indent=1)
    return p


def cache_utvonal(model_id, level, cache_dir=None):
    cache_dir = cache_dir or CACHE_DIR
    return os.path.join(cache_dir, _modell_slug(model_id), "%04d.json" % level)


def cache_olvas(model_id, level, cache_dir=None):
    p = cache_utvonal(model_id, level, cache_dir)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        adat = json.load(fh)
    if adat.get("prompt_verzio") not in PROMPT_VERZIO_KOMPATIBILIS or adat.get("model") != model_id:
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
                        csak_dontes=False, posztolo=None, cache_dir=None, hiba_naplo_dir=None):
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
            cserek, _ervenytelen, _elvetett = _cserek_validal(json.loads(tartalom), ctx)
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
            hiba_naplo_dir=hiba_naplo_dir,
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


def tsv_fejlec_ir_mindig(utvonal, fejlec):
    """O0.5d: a futas ELEJEN mindig ujrairja a fajlt, csak fejleccel (torli az
    elozo futas eredmenyet) -- ezutan tsv_sorokat_fuzz() hozzafuzessel bovitheti,
    lapok kozott megszakithatoan. A FOLYTATAST a gyorsitotar adja (level_modell_hivas
    cache-olvasasa), NEM a mar meglevo tsv-sorok: egy megismetelt futas ugyanazokat
    a donteseket ujra kiirja, gyorsitotar-talalat eseten halozati hivas nelkul --
    ezert nincs duplikacio, es a tsv mindig a legutobbi futas teljes, konzisztens
    eredmenyet tukrozi."""
    tsv_ir(utvonal, fejlec, [])


def tsv_sorokat_fuzz(utvonal, fejlec, sorok):
    """O0.5c/3: egy lap sorainak hozzafuzese -- a futas megszakitasakor a
    mar kesz lapok eredmenye nem veszik el."""
    if not sorok:
        return
    os.makedirs(os.path.dirname(utvonal), exist_ok=True)
    with open(utvonal, "a", encoding="utf-8", newline="\n") as fh:
        for sor in sorok:
            fh.write("\t".join(str(sor.get(mezo, "")) for mezo in fejlec) + "\n")


def tsv_olvas(utvonal):
    with open(utvonal, encoding="utf-8") as fh:
        tartalom = fh.read()
    sorok = tartalom.split("\n")
    if sorok and sorok[-1] == "":
        sorok = sorok[:-1]
    if not sorok:
        return []
    fejlec = sorok[0].split("\t")
    return [dict(zip(fejlec, sor.split("\t"))) for sor in sorok[1:]]


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
    elso_gyanus_szo_id = ctx["id_terkep"][elso_gyanus["i"]]
    eredeti_bbox = None
    for sor in sorok:
        for w in sor["szavak"]:
            if w["szo_id"] == elso_gyanus_szo_id:
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
    # ctx: rovid egesz azonositok (0, 1), 'id_terkep' kepezi ezeket vissza a
    # (szintetikus) hOCR szo_id-ra 'a'/'b' (O0.5c/1)
    ctx = {"id_info": {0: ("sor1", 0, True), 1: ("sor1", 1, True)}, "id_terkep": {0: "a", 1: "b"}}
    sema = _json_sema()

    # a) ervenyes valasz (tomor 'i'/'a'/'l' kulcsok, O0.5c/2)
    valaszok = iter([(_ror_valasz({"cserek": [{"i": [0], "a": "λόγος", "l": "grc"}]}), 1)])
    cserek, _, _ = openrouter_hivas(
        "m", b"x", {"level": 1}, "kulcs", sema, ctx,
        ujraprobalkozas_json=1, posztolo=lambda *a, **k: next(valaszok),
    )
    assert cserek[0]["szo_ids"] == ["a"]

    # b) ketelemu 'i'
    valaszok = iter([(_ror_valasz({"cserek": [{"i": [1, 0], "a": "λόγος", "l": "grc"}]}), 1)])
    cserek, _, _ = openrouter_hivas(
        "m", b"x", {"level": 1}, "kulcs", sema, ctx,
        ujraprobalkozas_json=1, posztolo=lambda *a, **k: next(valaszok),
    )
    assert cserek[0]["szo_ids"] == ["a", "b"]  # pozicio szerint rendezve

    # c) semasertes -> egy ujraprobalkozas -> hiba
    hibas = _ror_valasz({"cserek": [{"i": [999], "a": "x", "l": "grc"}]})
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

        ctx = {"id_info": {}, "id_terkep": {}}
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
    # (level_dontesek mar validalt, belso-formaju elemekkel dolgozik -- itt az
    # 'id_terkep' identitas-lekepezes, csak a fuggveny szerzodese miatt kell)
    ctx = {"id_info": {"a": ("sor1", 0, True), "b": ("sor1", 1, True)}, "id_terkep": {"a": "a", "b": "b"}}
    m1 = [{"szo_ids": ["a", "b"], "alak": "x", "nyelv": "grc", "extra": False}]
    m2 = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}]
    sorok, extra = level_dontesek(ctx, m1, m2)
    assert extra == []
    assert len(sorok) == 1, "atfedo, de eltero szo_ids-nek egyetlen vitas sort kell adnia: %r" % sorok
    assert sorok[0]["dontes"] == "vitas"
    assert sorok[0]["szo_ids"] == ["a", "b"]

    # ugyanarra az id-re az egyik modell extra, a masik nem -> vitas
    ctx2 = {"id_info": {"a": ("sor1", 0, True)}, "id_terkep": {"a": "a"}}
    m1b = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": True}]
    m2b = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}]
    sorok2, _ = level_dontesek(ctx2, m1b, m2b)
    assert len(sorok2) == 1
    assert sorok2[0]["dontes"] == "vitas"

    # O0.5e/1: csak m1 ad elemet -> hianyzo_m1
    ctx3 = {"id_info": {"a": ("sor1", 0, True)}, "id_terkep": {"a": "a"}}
    sorok3, _ = level_dontesek(ctx3, [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}], [])
    assert len(sorok3) == 1
    assert sorok3[0]["dontes"] == "hianyzo_m1"

    # O0.5e/1: csak m2 ad elemet -> hianyzo_m2
    sorok3b, _ = level_dontesek(ctx3, [], [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}])
    assert len(sorok3b) == 1
    assert sorok3b[0]["dontes"] == "hianyzo_m2"

    # O0.5e/1: egyik modell sem ad elemet a gyanus azonositora -> valtozatlan
    # (nem hianyzo -- mindketto megtartana a hOCR-alakot)
    sorok3c, _ = level_dontesek(ctx3, [], [])
    assert len(sorok3c) == 1
    assert sorok3c[0]["dontes"] == "valtozatlan"
    assert sorok3c[0]["m1"] is None and sorok3c[0]["m2"] is None

    # minden gyanus id pontosan egy sorban szerepel (vegyes eset)
    ctx4 = {
        "id_info": {
            "a": ("sor1", 0, True), "b": ("sor1", 1, True), "c": ("sor1", 2, True), "d": ("sor1", 3, False),
        },
        "id_terkep": {"a": "a", "b": "b", "c": "c", "d": "d"},
    }
    m1c = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False},
           {"szo_ids": ["c", "d"], "alak": "y", "nyelv": "grc", "extra": False}]
    m2c = [{"szo_ids": ["a"], "alak": "x", "nyelv": "grc", "extra": False}]
    sorok4, _ = level_dontesek(ctx4, m1c, m2c)
    osszes_id = sorted(sid for s in sorok4 for sid in s["szo_ids"])
    assert osszes_id == ["a", "b", "c", "d"]
    egyszeri = [sid for s in sorok4 for sid in s["szo_ids"]]
    assert len(egyszeri) == len(set(egyszeri)), "egy azonosito tobb sorban is szerepel"

    # regresszio: eles alaku (EGESZ-kulcsu id_info + id_terkep, O0.5c) ctx, ami
    # tobbelemu 'vitas' klasztert termel -- az elso O1.1-ujraindulas pontosan
    # itt bukott el (KeyError, mert a _klaszter_dontes belso lekepezese
    # string-kulcsokat var, de egesz-kulcsu id_info-t kapott)
    ctx5 = {
        "id_info": {10: ("sor1", 0, True), 11: ("sor1", 1, True), 12: ("sor1", 2, True)},
        "id_terkep": {10: "word_a", 11: "word_b", 12: "word_c"},
    }
    m1d = [{"szo_ids": ["word_a", "word_b"], "alak": "x", "nyelv": "grc", "extra": False}]
    m2d = [{"szo_ids": ["word_a"], "alak": "x", "nyelv": "grc", "extra": False},
           {"szo_ids": ["word_c"], "alak": "z", "nyelv": "grc", "extra": False}]
    sorok5, _ = level_dontesek(ctx5, m1d, m2d)  # nem szabad KeyError-t dobnia
    osszes_id5 = sorted(sid for s in sorok5 for sid in s["szo_ids"])
    assert osszes_id5 == ["word_a", "word_b", "word_c"]


def _onteszt_g_hiba_nem_cachelt():
    tmp = tempfile.mkdtemp(prefix="cremer_onteszt_hibacache_")
    try:
        ctx = {"id_info": {0: ("sor1", 0, True)}, "id_terkep": {0: "a"}}
        payload = {"level": 1, "sorok": []}
        model_cfg = {"nev": "teszt/hiba-modell"}
        config = {"ujraprobalkozas_ervenytelen_json": 0, "ujraprobalkozas_http": 0}
        hivas_szamlalo = {"n": 0}
        hibas_valasz = _ror_valasz({"cserek": [{"i": [999], "a": "x", "l": "grc"}]})

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
    ctx = {"id_info": {0: ("sor1", 0, True)}, "id_terkep": {0: "a"}}
    sema = _json_sema()

    hibas = _ror_valasz(
        {"cserek": [{"i": [999], "a": "x", "l": "grc"}]},
        usage={"prompt_tokens": 100, "completion_tokens": 20},
    )
    ervenyes = _ror_valasz(
        {"cserek": [{"i": [0], "a": "λόγος", "l": "grc"}]},
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
        {"cserek": [{"i": [999], "a": "x", "l": "grc"}]},
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

        csere_utvonal = os.path.join(tmp_kimenet, "CREMER_O1_csere.tsv")
        koltseg_utvonal = os.path.join(tmp_kimenet, "CREMER_O1_koltseg.tsv")
        eredmeny = _futtat_eles([17], lapindex, 2000, config, modellek, "fake-kulcs", _Args(),
                                 posztolo=posztolo, cache_dir=tmp_cache,
                                 csere_utvonal=csere_utvonal, koltseg_utvonal=koltseg_utvonal)
        assert eredmeny["leallt_plafon_miatt"] is False  # cmd_futtat ekkor 0-val lepne ki

        # O0.5c/3: laponkenti hozzafuzessel mar a _futtat_eles maga irta ki a ket tsv-t
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

        # O0.5d: masodik futas UGYANAZZAL a gyorsitotarral -- a tsv a futas
        # elejen ujrairodik (csak fejlec), a folytatast a gyorsitotar adja
        # (nincs uj halozati hivas), a vegeredmeny sorszama nem duplikalodik
        elso_csere_sorszam = len(csere_sorok)
        elso_koltseg_sorszam = len(koltseg_sorok)

        def posztolo_masodik_nem_hivhato(*a, **k):
            raise AssertionError("a masodik futasnak a gyorsitotarbol kellett volna dolgoznia, nem uj halozati hivasbol")

        eredmeny2 = _futtat_eles([17], lapindex, 2000, config, modellek, "fake-kulcs", _Args(),
                                  posztolo=posztolo_masodik_nem_hivhato, cache_dir=tmp_cache,
                                  csere_utvonal=csere_utvonal, koltseg_utvonal=koltseg_utvonal)
        assert eredmeny2["leallt_plafon_miatt"] is False

        with open(csere_utvonal, encoding="utf-8") as fh:
            csere_sorok2 = fh.read().splitlines()
        with open(koltseg_utvonal, encoding="utf-8") as fh:
            koltseg_sorok2 = fh.read().splitlines()
        assert len(csere_sorok2) == elso_csere_sorszam, (
            "a masodik futas utan a csere-tsv sorszamanak ugyanannyinak kell lennie (nincs duplikacio): %d != %d"
            % (len(csere_sorok2), elso_csere_sorszam)
        )
        assert len(koltseg_sorok2) == elso_koltseg_sorszam, (
            "a masodik futas utan a koltseg-tsv sorszamanak ugyanannyinak kell lennie (nincs duplikacio): %d != %d"
            % (len(koltseg_sorok2), elso_koltseg_sorszam)
        )

        naplok_utana = os.listdir(NAPLOK_DIR) if os.path.isdir(NAPLOK_DIR) else None
        cache_utana = os.listdir(CACHE_DIR) if os.path.isdir(CACHE_DIR) else None
        assert naplok_elotte == naplok_utana, "a valodi naplok/ konyvtarat nem szabad erinteni"
        assert cache_elotte == cache_utana, "a valodi gyorsitotar-konyvtarat nem szabad erinteni"
    finally:
        shutil.rmtree(tmp_kimenet, ignore_errors=True)
        shutil.rmtree(tmp_cache, ignore_errors=True)


def _onteszt_j_elemszintu_validalas():
    tmp = tempfile.mkdtemp(prefix="cremer_onteszt_hibanaplo_")
    try:
        # a) 1 ervenyes + 1 nem-szomszedos 'i' (semasertes) elem -> az
        #    ervenyes megmarad, a lap NEM hiba, a hibas elem a hibanaploba kerul
        ctx = {
            "id_info": {0: ("sor1", 0, True), 1: ("sor1", 1, False), 2: ("sor1", 2, True), 3: ("sor1", 3, True)},
            "id_terkep": {0: "a", 1: "b", 2: "c", 3: "x"},
        }
        valasz = _ror_valasz({"cserek": [
            {"i": [3], "a": "λόγος", "l": "grc"},
            {"i": [0, 2], "a": "y", "l": "grc"},  # id 1 ('b') kimarad kozbol -> nem szomszedosak
        ]})
        cserek, usage, _ = openrouter_hivas(
            "teszt/j-modell", b"x", {"level": 12345}, "kulcs", _json_sema(), ctx,
            ujraprobalkozas_json=1, posztolo=lambda *a, **k: (valasz, 1),
            hiba_naplo_dir=tmp,
        )
        assert len(cserek) == 1 and cserek[0]["szo_ids"] == ["x"], (
            "a lapnak NEM szabad hiba-nak lennie, az ervenyes elemnek meg kell maradnia: %r" % cserek
        )
        hiba_fajl = os.path.join(tmp, _modell_slug("teszt/j-modell"), "12345_1.json")
        assert os.path.exists(hiba_fajl), "a semasertes elemnek a hibanaplóba kellett volna kerulnie"
        with open(hiba_fajl, encoding="utf-8") as fh:
            naplo = json.load(fh)
        assert len(naplo["ervenytelen_elemek"]) == 1

        # b) elemek tobb mint fele semasertes -> ujraprobalkozas, utana hiba
        ctx2 = {"id_info": {0: ("sor1", 0, True), 1: ("sor1", 1, True)}, "id_terkep": {0: "a", 1: "b"}}
        tobbsegi_hibas = _ror_valasz({"cserek": [
            {"i": [997], "a": "x", "l": "grc"},
            {"i": [998], "a": "x", "l": "grc"},
            {"i": [0], "a": "y", "l": "grc"},
        ]})  # 2/3 semasertes > 50%
        hivas_n = {"n": 0}

        def posztolo2(*a, **k):
            hivas_n["n"] += 1
            return tobbsegi_hibas, 1

        try:
            openrouter_hivas("teszt/j-modell2", b"x", {"level": 999}, "kulcs", _json_sema(), ctx2,
                              ujraprobalkozas_json=1, posztolo=posztolo2, hiba_naplo_dir=tmp)
            raise AssertionError("vart OpenRouterHiba (tobbsegi semasertes)")
        except OpenRouterHiba:
            pass
        assert hivas_n["n"] == 2, "a tobbsegi semasertesnek ujra kellett volna probalkoznia"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _onteszt_k_rovid_id_visszakepezes():
    """O0.5c/5: a payloadban kikuldott rovid egesz 'i' azonositonak a valodi
    hOCR szo_id-ra kell visszakepezodnie a validalas utan -- valodi 17. leveli
    adaton."""
    lapindex = hocr_lapindex_epit()
    sorok = level_sorok(17, lapindex)
    _, eredeti_meret, uj_meret = level_kep_jpeg(17, 2000)
    payload, ctx, _ = level_payload_es_ctx(17, sorok, eredeti_meret, uj_meret)
    elso_sor = next(s for s in payload["sorok"] if s["gyanusak"])
    elso_gyanus_i = elso_sor["gyanusak"][0]["i"]
    vart_szo_id = ctx["id_terkep"][elso_gyanus_i]
    assert isinstance(elso_gyanus_i, int)

    valasz = _ror_valasz({"cserek": [{"i": [elso_gyanus_i], "a": "λόγος", "l": "grc"}]})
    cserek, _, _ = openrouter_hivas(
        "teszt/k-modell", b"x", payload, "kulcs", _json_sema(), ctx,
        ujraprobalkozas_json=0, posztolo=lambda *a, **k: (valasz, 1),
    )
    assert cserek[0]["szo_ids"] == [vart_szo_id], (
        "a rovid azonosito nem kepezodott vissza helyesen a hOCR szo_id-ra: %r != %r"
        % (cserek[0]["szo_ids"], [vart_szo_id])
    )


def _onteszt_l_elvetett_nem_gyanus():
    """O0.5e/4: nem-gyanus, nem-'x' elemek (Qwen-zaj) elvetett_nem_gyanus-ba
    kerulnek, a hibanaploba is beirodnak, de NEM szamitanak bele az 50%-os
    kuszobbe -- a lap az egyetlen valodi (gyanus) elemmel is sikeres marad."""
    tmp = tempfile.mkdtemp(prefix="cremer_onteszt_zaj_")
    try:
        ctx = {
            "id_info": {0: ("sor1", 0, True), 1: ("sor1", 1, False), 2: ("sor1", 2, False)},
            "id_terkep": {0: "gyanus_a", 1: "tiszta_b", 2: "tiszta_c"},
        }
        valasz = _ror_valasz({"cserek": [
            {"i": [0], "a": "λόγος", "l": "grc"},
            {"i": [1], "a": "zaj1", "l": "lat"},
            {"i": [2], "a": "zaj2", "l": "lat"},
            {"i": [1], "a": "zaj3", "l": "lat"},
            {"i": [2], "a": "zaj4", "l": "lat"},
        ]})
        cserek, usage, _ = openrouter_hivas(
            "teszt/l-modell", b"x", {"level": 4242}, "kulcs", _json_sema(), ctx,
            ujraprobalkozas_json=0, posztolo=lambda *a, **k: (valasz, 1),
            hiba_naplo_dir=tmp,
        )
        assert len(cserek) == 1 and cserek[0]["szo_ids"] == ["gyanus_a"], (
            "a nem-gyanus zaj-elemek nem szabad, hogy a lapot hiba-va tegyek: %r" % cserek
        )
        hiba_fajl = os.path.join(tmp, _modell_slug("teszt/l-modell"), "4242_1.json")
        assert os.path.exists(hiba_fajl)
        with open(hiba_fajl, encoding="utf-8") as fh:
            naplo = json.load(fh)
        assert naplo["ervenytelen_elemek"] == [], "ezek nem valodi semasertesek, nem oda valok"
        assert len(naplo["elvetett_nem_gyanus_elemek"]) == 4
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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
    ("j_elemszintu_validalas", _onteszt_j_elemszintu_validalas),
    ("k_rovid_id_visszakepezes", _onteszt_k_rovid_id_visszakepezes),
    ("l_elvetett_nem_gyanus", _onteszt_l_elvetett_nem_gyanus),
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

    modellek = dict(config.get("modellek", {}))
    if getattr(args, "m2", None) == "tartalek":
        tartalek = config.get("tartalek_m2")
        if not tartalek or not tartalek.get("nev"):
            print("HIBA -- a config.tartalek_m2 nincs kitoltve", file=sys.stderr)
            return 1
        uj_m2 = dict(tartalek)
        uj_m2.setdefault("reasoning", {"effort": "low"})
        modellek["m2"] = uj_m2
        print("--m2 tartalek: m2 = %s (reasoning=%s)" % (uj_m2["nev"], uj_m2.get("reasoning")))

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

    csere_utvonal = os.path.join(args.kimenet_dir, "CREMER_O1_csere.tsv")
    koltseg_utvonal = os.path.join(args.kimenet_dir, "CREMER_O1_koltseg.tsv")
    eredmeny = _futtat_eles(levelek, lapindex, max_el_px, config, modellek, api_key, args,
                             csere_utvonal=csere_utvonal, koltseg_utvonal=koltseg_utvonal)

    _futtat_osszesito_kiir(eredmeny, csere_utvonal, koltseg_utvonal)

    if eredmeny["leallt_plafon_miatt"]:
        print("\nA futas a koltsegplafon miatt korabban leallt.", file=sys.stderr)
        return 3

    osszes_db = len(eredmeny["o1_sorok"])
    hiba_db = sum(1 for s in eredmeny["o1_sorok"] if s["dontes"] == "hiba")
    if osszes_db and hiba_db / osszes_db > HIBA_ARANY_KUSZOB:
        print(
            "\nHIBA -- a hiba-sorok aranya tul magas: %d/%d = %.1f%% (kuszob: %.0f%%)."
            % (hiba_db, osszes_db, 100 * hiba_db / osszes_db, 100 * HIBA_ARANY_KUSZOB),
            file=sys.stderr,
        )
        return 4
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


# ---------------------------------------------------------------------------
# O1.2: 'ellenorzes' alparancs -- kivagasok es atnezooldalak, halozat nelkul
# ---------------------------------------------------------------------------

ELLENORZES_MINTA_MAG = 20260924
ELLENORZES_MINTA_DB = 300
ELLENORZES_SOR_PER_OLDAL = 50
ELLENORZES_KEP_MAX_SZELESSEG = 600
ELLENORZES_KEP_MINOSEG = 75
ELLENORZES_VIZSZINTES_PARNAZAS = 150


def level_kep_eredeti(level, jp2zip_utvonal=JP2ZIP_UTVONAL):
    """A level teljes felbontasu kepe (PIL Image), a --szaraz/API-hivasokban
    hasznalt kicsinyites nelkul -- az O1-csere-tsv bbox-a (H2) is eredeti
    (nem skalazott) jp2-koordinata, tehat a kivagasnak is ebbol kell jonnie."""
    from PIL import Image

    nev = "cu31924098819406_jp2/cu31924098819406_%04d.jp2" % level
    with zipfile.ZipFile(jp2zip_utvonal) as z:
        nyers = z.read(nev)
    kep = Image.open(io.BytesIO(nyers))
    kep.load()
    return kep


def kivagas_hatarok(bbox, kep_meret):
    """Vizszintesen +-150 px, fuggolegesen egy sormagassaggal a bbox alatt/felett
    (a csoport sajat magassagat hasznalva sormagassag-kozelitesnek)."""
    x0, y0, x1, y1 = bbox
    magassag = max(1, y1 - y0)
    return [
        max(0, x0 - ELLENORZES_VIZSZINTES_PARNAZAS), max(0, y0 - magassag),
        min(kep_meret[0], x1 + ELLENORZES_VIZSZINTES_PARNAZAS), min(kep_meret[1], y1 + magassag),
    ]


def kivagas_ments(kep, hatarok, cel_utvonal, max_szelesseg=ELLENORZES_KEP_MAX_SZELESSEG,
                   minoseg=ELLENORZES_KEP_MINOSEG):
    from PIL import Image

    x0, y0, x1, y1 = [int(round(v)) for v in hatarok]
    x1, y1 = max(x1, x0 + 1), max(y1, y0 + 1)
    resz = kep.crop((x0, y0, x1, y1)).convert("L")
    if resz.width > max_szelesseg:
        arany = max_szelesseg / resz.width
        resz = resz.resize((max_szelesseg, max(1, round(resz.height * arany))), Image.LANCZOS)
    os.makedirs(os.path.dirname(cel_utvonal), exist_ok=True)
    resz.save(cel_utvonal, format="JPEG", quality=minoseg)


def _o1_sor_alak(sor, mezo):
    """A csere-tsv 'm1'/'m2' mezoje JSON-string (csere-dict) vagy ures -- ebbol
    az 'alak'-ot adja vissza, vagy ''-t."""
    nyers = sor.get(mezo, "")
    if not nyers:
        return ""
    try:
        adat = json.loads(nyers)
    except (json.JSONDecodeError, TypeError):
        return ""
    if isinstance(adat, dict):
        return adat.get("alak", "") or ""
    return ""


def _ellenorzes_minta_epit(fo_sorok, lite_sorok):
    """O1.2: 300 veletlen 'auto' sor (rogzitett maggal), minden 'vitas'/'extra_*'
    sor, es kulon a fo/lite elteresek (ugyanaz a szo_ids, mindket futasban
    'auto', de a C4-elonormalizalt alak kulonbozik)."""
    auto_sorok = [s for s in fo_sorok if s["dontes"] == "auto"]
    rng = random.Random(ELLENORZES_MINTA_MAG)
    if len(auto_sorok) > ELLENORZES_MINTA_DB:
        minta_auto = rng.sample(auto_sorok, ELLENORZES_MINTA_DB)
        minta_auto.sort(key=lambda s: (int(s["level"]), s["szo_id"]))
    else:
        minta_auto = list(auto_sorok)

    vitas_extra = [s for s in fo_sorok if s["dontes"] in ("vitas", "extra_auto", "extra_vitas")]

    lite_by_key = {(s["level"], s["szo_ids"]): s for s in lite_sorok}
    elteres_sorok = []
    for f in fo_sorok:
        if f["dontes"] != "auto":
            continue
        l = lite_by_key.get((f["level"], f["szo_ids"]))
        if l is None or l["dontes"] != "auto":
            continue
        f_alak = _o1_sor_alak(f, "m1")
        l_alak = _o1_sor_alak(l, "m1")
        if f_alak and l_alak and elonormalizal(f_alak) != elonormalizal(l_alak):
            elteres_sorok.append((f, l))

    return minta_auto, vitas_extra, elteres_sorok


def _atnezo_sor_szoveg(sorszam, kep_relativ_ut, hocr, m1_alak, m2_alak, dontes_nev):
    return "| %d | ![](%s) | %s | %s | %s | %s |  |" % (
        sorszam, kep_relativ_ut, hocr, m1_alak, m2_alak, dontes_nev,
    )


def _atnezo_oldalak_ir(ki_dir, sorok_kepekkel, alap_nev, cim):
    """sorok_kepekkel: lista (sorszam, kep_relativ_ut, hocr, m1_alak, m2_alak, dontes_nev)
    tuple-okbol. ELLENORZES_SOR_PER_OLDAL soronkent kulon fajl."""
    utvonalak = []
    for i in range(0, len(sorok_kepekkel), ELLENORZES_SOR_PER_OLDAL):
        resz = sorok_kepekkel[i:i + ELLENORZES_SOR_PER_OLDAL]
        oldalszam = i // ELLENORZES_SOR_PER_OLDAL + 1
        nev = "%s_%02d.md" % (alap_nev, oldalszam) if alap_nev != "ATNEZES_ELTERES" else "%s.md" % alap_nev
        utvonal = os.path.join(ki_dir, nev)
        sorok = [
            "# %s (%d/%d)" % (cim, oldalszam, -(-len(sorok_kepekkel) // ELLENORZES_SOR_PER_OLDAL)),
            "",
            "Ítélet: `ok` / `hiba: <helyes alak>` / `?`.",
            "",
            "| # | kép | hOCR | m1 | m2 | döntés | ítélet |",
            "|---|---|---|---|---|---|---|",
        ]
        for t in resz:
            sorok.append(_atnezo_sor_szoveg(*t))
        os.makedirs(ki_dir, exist_ok=True)
        with open(utvonal, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(sorok) + "\n")
        utvonalak.append(utvonal)
        if alap_nev == "ATNEZES_ELTERES":
            break
    return utvonalak


def _dir_meret_bajt(ut):
    osszeg = 0
    for gyoker, _, fajlok in os.walk(ut):
        for f in fajlok:
            osszeg += os.path.getsize(os.path.join(gyoker, f))
    return osszeg


def cmd_ellenorzes(args):
    fo_csv = os.path.join(args.kimenet_dir, "CREMER_O1_csere.tsv")
    lite_csv = os.path.join(args.lite_dir, "CREMER_O1_csere.tsv")
    ki_dir = args.ellenorzes_dir

    if not os.path.exists(fo_csv):
        print("HIBA -- nincs fo csere-tsv:", fo_csv, file=sys.stderr)
        return 2
    fo_sorok = tsv_olvas(fo_csv)
    lite_sorok = tsv_olvas(lite_csv) if os.path.exists(lite_csv) else []
    if not lite_sorok:
        print("figyelem -- nincs lite csere-tsv (%s), az elteres-szakasz ures lesz" % lite_csv, file=sys.stderr)

    minta_auto, vitas_extra, elteres = _ellenorzes_minta_epit(fo_sorok, lite_sorok)

    kepek_dir = os.path.join(ki_dir, "kepek")
    kep_cache = {}

    def kep_szerez(level):
        level = int(level)
        if level not in kep_cache:
            kep_cache[level] = level_kep_eredeti(level)
        return kep_cache[level]

    def kivag_es_relativ_ut(sor):
        level = int(sor["level"])
        try:
            bbox = json.loads(sor["bbox"])
        except (json.JSONDecodeError, TypeError):
            bbox = None
        fajlnev = "L%04d_%s.jpg" % (level, sor["szo_id"])
        cel = os.path.join(kepek_dir, fajlnev)
        if bbox:
            kep = kep_szerez(level)
            hatarok = kivagas_hatarok(bbox, kep.size)
            kivagas_ments(kep, hatarok, cel)
        return "kepek/" + fajlnev

    minta_tsv_sorok = []
    atnezo_tuple_auto_vitas = []
    sorszam = 0
    for sor in minta_auto + vitas_extra:
        sorszam += 1
        kep_relativ = kivag_es_relativ_ut(sor)
        m1_alak = _o1_sor_alak(sor, "m1")
        m2_alak = _o1_sor_alak(sor, "m2")
        atnezo_tuple_auto_vitas.append((sorszam, kep_relativ, sor["ocr"], m1_alak, m2_alak, sor["dontes"]))
        minta_tsv_sorok.append({
            "sorszam": sorszam, "oldal": (sorszam - 1) // ELLENORZES_SOR_PER_OLDAL + 1,
            "szo_ids": sor["szo_ids"], "level": sor["level"], "dontes": sor["dontes"],
            "m1_alak": m1_alak, "m2_alak": m2_alak,
        })

    elteres_tuple = []
    for i, (f, l) in enumerate(elteres, start=1):
        kep_relativ = kivag_es_relativ_ut(f)
        f_alak = _o1_sor_alak(f, "m1")
        l_alak = _o1_sor_alak(l, "m1")
        elteres_tuple.append((i, kep_relativ, f["ocr"], f_alak, l_alak, "ELTERES (fo/lite)"))

    utvonalak = _atnezo_oldalak_ir(ki_dir, atnezo_tuple_auto_vitas, "ATNEZES", "Cremer O1 ellenorzes")
    if elteres_tuple:
        utvonalak += _atnezo_oldalak_ir(ki_dir, elteres_tuple, "ATNEZES_ELTERES", "Cremer O1 fo/lite elteresek")

    minta_tsv_fejlec = ["sorszam", "oldal", "szo_ids", "level", "dontes", "m1_alak", "m2_alak"]
    minta_tsv_ut = os.path.join(ki_dir, "minta.tsv")
    tsv_ir(minta_tsv_ut, minta_tsv_fejlec, minta_tsv_sorok)

    meret = _dir_meret_bajt(ki_dir)
    print("=== ellenorzo csomag ===")
    print("auto minta:", len(minta_auto))
    print("vitas/extra_*:", len(vitas_extra))
    print("fo/lite elteres:", len(elteres))
    print("kepek:", len(atnezo_tuple_auto_vitas) + len(elteres_tuple))
    print("konyvtar merete: %.2f MB (%s)" % (meret / (1024 * 1024), ki_dir))
    for u in utvonalak:
        print("  ", u)
    print("  ", minta_tsv_ut)

    if meret > 30 * 1024 * 1024:
        print(
            "\nHIBA -- a naplok/CREMER_O1_ellenorzes/ meghaladja a 30 MB-os korlatot "
            "(%.2f MB) -- NEM commitolhato. Szakaszonkenti sorok: auto minta=%d, "
            "vitas/extra_*=%d, elteres=%d." % (meret / (1024 * 1024), len(minta_auto),
                                                len(vitas_extra), len(elteres)),
            file=sys.stderr,
        )
        return 1
    return 0


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
                  posztolo=None, cache_dir=None, hiba_naplo_dir=None,
                  csere_utvonal=None, koltseg_utvonal=None):
    """O0.5c/3 + O0.5d: ha csere_utvonal/koltseg_utvonal meg van adva, a fajlok
    a futas ELEJEN mindig ujrairodnak (csak fejlec -- torlodik az elozo futas
    eredmenye), utana laponkent hozzafuzessel bovulnek. A FOLYTATAST a
    gyorsitotar adja (level_modell_hivas cache-olvasasa a mar lekert lapokra
    halozati hivas nelkul valaszol): egy megismetelt futas ugyanazokat a
    donteseket ujra kiirja, tehat nincs duplikacio, es a tsv mindig a legutobbi
    futas teljes, konzisztens eredmenyet tukrozi. A visszaadott dict emellett
    is tartalmazza a teljes o1_sorok/koltseg_sorok listat a futas-vegi
    osszesitohoz."""
    if csere_utvonal:
        tsv_fejlec_ir_mindig(csere_utvonal, O1_CSERE_FEJLEC)
    if koltseg_utvonal:
        tsv_fejlec_ir_mindig(koltseg_utvonal, KOLTSEG_FEJLEC)

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
                hiba_naplo_dir=hiba_naplo_dir,
            )
            eredmenyek[kulcs] = cserek
            if honnan in ("halozat", "cache"):
                # O0.5d: gyorsitotar-talalatnal is uj koltseg-tsv-sor kerul (a
                # cache-elt usage-bol) -- igy egy megismetelt/folytatott futas
                # koltseg-tsv-je mindig teljes es konzisztens (a korabban mar
                # lekert lapok koltsege sem tunik el a friss ujraírasnal), es
                # a naplo.plafon_elerve_e() is a teljes, korabbi koltseget latja.
                uj_koltseg_sor = naplo.hozzaad_usage(
                    level, m_cfg["nev"], usage,
                    m_cfg.get("ar_bemenet_usd_per_1M"), m_cfg.get("ar_kimenet_usd_per_1M"))
                if koltseg_utvonal:
                    tsv_sorokat_fuzz(koltseg_utvonal, KOLTSEG_FEJLEC, [uj_koltseg_sor])

        if eredmenyek.get(k1) is None or eredmenyek.get(k2) is None:
            continue  # --csak-dontes es nincs meg gyorsitotar-talalat ehhez a laphoz

        nem_extra, extra = level_dontesek(ctx, eredmenyek[k1], eredmenyek[k2])
        lap_o1_sorai = [o1_csere_sor_epit(level, ocr_by_id, bbox_by_id, d_sor) for d_sor in nem_extra + extra]
        o1_sorok.extend(lap_o1_sorai)
        if csere_utvonal:
            tsv_sorokat_fuzz(csere_utvonal, O1_CSERE_FEJLEC, lap_o1_sorai)

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
    ap_futtat.add_argument("--m2", type=str, choices=["tartalek"], default=None,
                            help="ha 'tartalek': m2 helyett a config.tartalek_m2-t hasznalja "
                                 "(reasoning: {'effort':'low'}), D14")
    ap_futtat.add_argument("--csak-dontes", dest="csak_dontes", action="store_true",
                            help="hivas nelkul, a gyorsitotarbol szamolja ujra a donteseket")
    ap_futtat.add_argument("--onteszt", action="store_true",
                            help="halozat es kulcs nelkuli onellenorzes; a tobbi kapcsolot figyelmen kivul hagyja")
    ap_futtat.add_argument("--config", type=str, default=CONFIG_UTVONAL)
    ap_futtat.add_argument("--kimenet-dir", dest="kimenet_dir", type=str, default=NAPLOK_DIR,
                            help="hova irja a CREMER_O1_csere.tsv / CREMER_O1_koltseg.tsv fajlokat")
    ap_futtat.set_defaults(func=cmd_futtat)

    ap_ellenorzes = sub.add_parser("ellenorzes", help="O1.2: ellenorzo csomag (kivagasok, atnezooldalak, minta.tsv)")
    ap_ellenorzes.add_argument("--kimenet-dir", dest="kimenet_dir", type=str, default=NAPLOK_DIR,
                                help="a fo futas CREMER_O1_csere.tsv-jenek konyvtara")
    ap_ellenorzes.add_argument("--lite-dir", dest="lite_dir", type=str,
                                default=os.path.join(NAPLOK_DIR, "CREMER_O1_lite"),
                                help="a tartalek-m2 futas CREMER_O1_csere.tsv-jenek konyvtara")
    ap_ellenorzes.add_argument("--ellenorzes-dir", dest="ellenorzes_dir", type=str,
                                default=os.path.join(NAPLOK_DIR, "CREMER_O1_ellenorzes"),
                                help="hova irja a kivagasokat es az atnezooldalakat")
    ap_ellenorzes.set_defaults(func=cmd_ellenorzes)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
