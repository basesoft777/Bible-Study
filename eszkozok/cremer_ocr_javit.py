#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cremer_ocr_javit.py -- CREMER_OCR_BRIEF.md O0-O2: a Cremer-lexikon hOCR-szovegenek
javitasa ket fuggetlen kepolvaso modellel OpenRouteren keresztul.

Alparancsok:
  gyanus   -- egy adott level gyanus szavainak listazasa (fejlesztes/ellenorzes;
              nem hivja a modelleket).
  futtat   -- a fo folyamat egy level-listara: lapkep kivagas a jp2-zipbol,
              hOCR gyanus szavainak kigyujtese, OpenRouter-hivas (C1-C3),
              egyezes (C4), alakellenorzes (C5), koltsegnaplo es -plafon (C6).
              --szaraz: hivas nelkul -- csak a bemenet elokeszul, es a becsult
              token- es koltsegigeny keszul jelentesnek (O0.3).

CLI:
    python eszkozok/cremer_ocr_javit.py gyanus --level 17
    python eszkozok/cremer_ocr_javit.py futtat --pilot --szaraz
    python eszkozok/cremer_ocr_javit.py futtat --pilot
    python eszkozok/cremer_ocr_javit.py futtat --levelek 17,82,124

Az OPENROUTER_API_KEY kulcsot csak kornyezeti valtozobol olvassa; sehova nem
irja ki es nem naplozza. A modellazonositokat es -arakat a
cremer_ocr_config.json adja -- ha uresek, a --szaraz mod meg mukodik, a valodi
hivas viszont hibaval leall (C1).

Kilepesi kod: 0 = rendben, 1 = szabalysertes (pl. plafon eleresekor korai
leallas, vagy hianyzo modell valodi futasnal), 2 = hiba.
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
import unicodedata
import zipfile
from datetime import datetime, timezone

REPO_GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NYERS_ALAP = os.path.join(REPO_GYOKER, "konkordancia", "_nyers", "cremer")
HOCR_UTVONAL = os.path.join(NYERS_ALAP, "cu31924098819406_hocr.html")
JP2ZIP_UTVONAL = os.path.join(NYERS_ALAP, "cu31924098819406_jp2.zip")
CONFIG_UTVONAL = os.path.join(REPO_GYOKER, "eszkozok", "cremer_ocr_config.json")
NAPLOK_DIR = os.path.join(REPO_GYOKER, "naplok")

# C7: pilot -- 7 ismert level (Abbott-Smith-szocikkek + gorog mutato) + a heber
# mutato levele + 12 veletlen level, rogzitett maggal.
PILOT_ISMERT_LEVELEK = [17, 82, 124, 350, 628, 760, 934, 950]
PILOT_VELETLEN_MAG = 20260923
PILOT_VELETLEN_DB = 12
LEVEL_MIN, LEVEL_MAX = 1, 967  # a page_numbers.json szerinti szamozott levelek (SS 0.2)


# ---------------------------------------------------------------------------
# hOCR feldolgozas
# ---------------------------------------------------------------------------

_PAGE_START_RE = re.compile(rb'<div class=[\'"]ocr_page[\'"] id="page_(\d{6})"')
_WORD_RE = re.compile(
    rb'<span class="ocrx_word" id="(?P<id>[^"]+)" '
    rb'title="bbox (?P<x0>\d+) (?P<y0>\d+) (?P<x1>\d+) (?P<y1>\d+); '
    rb'x_wconf (?P<wconf>\d+)[^"]*">(?P<text>.*?)</span>',
    re.DOTALL,
)


def _leaf_hocr_id(level):
    return "%06d" % level


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
    szoveg = nyers_bytes.decode("utf-8", errors="replace")
    return _html_entitas_dekodol(szoveg)


def _html_entitas_dekodol(szoveg):
    import html
    return html.unescape(szoveg)


_VEGYES_ESET_RE = re.compile(r"^[A-Za-z]+$")


def gyanus_e(szoveg_nyers, wconf):
    """CLAUDE_BRIEF SS1 'Gyanus szo': x_wconf < 60, VAGY latin betus torzkep
    (heurisztika: a betumag nem csupa nagybetu, nem egyszeru Title-eset, de
    van benne kis- ES nagybetu is -- pl. 'ABvocos')."""
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


def level_szavai(level, lapindex, hocr_utvonal=HOCR_UTVONAL):
    nyers = level_hocr_szoveg(level, lapindex, hocr_utvonal)
    szavak = []
    for m in _WORD_RE.finditer(nyers):
        text = _html_dekodol(m.group("text"))
        szavak.append({
            "szo_id": m.group("id").decode("ascii"),
            "bbox": [int(m.group("x0")), int(m.group("y0")), int(m.group("x1")), int(m.group("y1"))],
            "wconf": int(m.group("wconf")),
            "ocr": text,
        })
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


# ---------------------------------------------------------------------------
# C3: kimeneti payload (a modellnek kuldott JSON-leiras a gyanus szavakrol)
# ---------------------------------------------------------------------------

def level_payload(level, gyanus_szavak):
    return {
        "level": level,
        "utasitas": (
            "Add vissza SZIGORU JSON tombkent a gyanus szavak javitott alakjat "
            "(gorog vagy heber vagy javitott latin), csak a felsorolt szo_id-kra. "
            "Ne irj szabad szoveget. Formatum minden elemre: "
            "{\"szo_id\": str, \"alak\": str, \"nyelv\": \"grc\"|\"heb\"|\"lat\"}."
        ),
        "gyanus_szavak": [
            {"szo_id": sz["szo_id"], "ocr": sz["ocr"], "bbox": sz["bbox"], "wconf": sz["wconf"]}
            for sz in gyanus_szavak
        ],
    }


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
    gyanus = level_gyanus_szavai(level, lapindex, hocr_utvonal)
    _, eredeti_meret, uj_meret = level_kep_jpeg(level, max_el_px, jp2zip_utvonal)
    payload = level_payload(level, gyanus)
    payload_szoveg = json.dumps(payload, ensure_ascii=False)
    kep_token = kep_token_becsles(uj_meret)
    szoveg_token = szoveg_token_becsles(payload_szoveg)
    kimenet_token = kimenet_token_becsles(len(gyanus))
    return {
        "level": level,
        "gyanus_db": len(gyanus),
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


def _nfc(s):
    return unicodedata.normalize("NFC", s)


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
                        alakok.add(_nfc(mezok[i_ragozott]))
                        alakok.add(_nfc(mezok[i_szoto]))
    lxx_dir = os.path.join(REPO_GYOKER, "konkordancia", "LXX_OS")
    if os.path.isdir(lxx_dir):
        for nev in os.listdir(lxx_dir):
            if not nev.endswith(".tsv"):
                continue
            with open(os.path.join(lxx_dir, nev), encoding="utf-8") as fh:
                fejlec = None
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
                        alakok.add(_nfc(mezok[i_szoalak]))
                        alakok.add(_nfc(mezok[i_lemma]))
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
    _gorog_szoveg_cache = _nfc("\n".join(reszek))
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
    _heber_szoveg_cache = _nfc("\n".join(reszek))
    return _heber_szoveg_cache


def alak_igazolt_e(alak, nyelv):
    """C5: 'alak_igazolt' -- talalat eseten True, kulonben False (nem hiba,
    l. C5 -- a Cremer klasszikus idezetei tobbnyire nincsenek a listakban)."""
    alak_nfc = _nfc(alak)
    if nyelv == "grc":
        if alak_nfc in _gorog_alakok_epit():
            return True
        return alak_nfc in _gorog_szoveg_epit()
    if nyelv == "heb":
        return alak_nfc in _heber_szoveg_epit()
    return False


# ---------------------------------------------------------------------------
# C4: egyezes / vitas / hianyzo
# ---------------------------------------------------------------------------

def dontes(csere_m1, csere_m2):
    """csere_m1, csere_m2: dict {"alak":..,"nyelv":..} vagy None (nincs csere).
    Visszaad: 'auto' | 'vitas' | 'hianyzo'."""
    if csere_m1 is None or csere_m2 is None:
        return "hianyzo"
    if _nfc(csere_m1["alak"]) == _nfc(csere_m2["alak"]) and csere_m1["nyelv"] == csere_m2["nyelv"]:
        return "auto"
    return "vitas"


# ---------------------------------------------------------------------------
# OpenRouter-hivas (C1-C3) -- csak valodi futasnal (nem --szaraz)
# ---------------------------------------------------------------------------

class OpenRouterHiba(Exception):
    pass


def openrouter_hivas(model_id, kep_jpeg_bytes, payload, api_key, ujraprobalkozas=1):
    """Egy hivas egy modellhez, egy laphoz (C2). Visszaad: list[{"szo_id","alak","nyelv"}]
    vagy dobja az OpenRouterHiba-t 'hiba'-kent (C3: egy ujraprobalkozas ervenytelen
    JSON-ra, utana feladja)."""
    import base64
    import requests

    kep_b64 = base64.b64encode(kep_jpeg_bytes).decode("ascii")
    uzenet = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": json.dumps(payload, ensure_ascii=False)},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + kep_b64}},
            ],
        }
    ]
    utolso_hiba = None
    for kiserlet in range(ujraprobalkozas + 1):
        valasz = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
            json={"model": model_id, "messages": uzenet, "response_format": {"type": "json_object"}},
            timeout=120,
        )
        valasz.raise_for_status()
        tartalom = valasz.json()["choices"][0]["message"]["content"]
        try:
            adat = json.loads(tartalom)
            if isinstance(adat, dict) and "cserek" in adat:
                adat = adat["cserek"]
            if not isinstance(adat, list):
                raise ValueError("nem lista")
            return adat
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            utolso_hiba = e
            continue
    raise OpenRouterHiba("ervenytelen JSON %d kiserlet utan: %s" % (ujraprobalkozas + 1, utolso_hiba))


# ---------------------------------------------------------------------------
# Config es koltsegplafon (C6)
# ---------------------------------------------------------------------------

def config_betolt(utvonal=CONFIG_UTVONAL):
    with open(utvonal, encoding="utf-8") as fh:
        return json.load(fh)


class KoltsegNaplo:
    def __init__(self, plafon_usd):
        self.plafon_usd = plafon_usd
        self.osszeg_usd = 0.0
        self.sorok = []

    def hozzaad(self, level, model_id, bemenet_token, kimenet_token, ar_bemenet_1m, ar_kimenet_1m):
        koltseg = 0.0
        if ar_bemenet_1m is not None:
            koltseg += bemenet_token / 1_000_000 * ar_bemenet_1m
        if ar_kimenet_1m is not None:
            koltseg += kimenet_token / 1_000_000 * ar_kimenet_1m
        self.osszeg_usd += koltseg
        self.sorok.append({
            "level": level, "model": model_id,
            "bemenet_token": bemenet_token, "kimenet_token": kimenet_token,
            "koltseg_usd": round(koltseg, 6), "futo_osszeg_usd": round(self.osszeg_usd, 6),
        })
        return self.osszeg_usd

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

def tsv_ir(utvonal, fejlec, sorok):
    os.makedirs(os.path.dirname(utvonal), exist_ok=True)
    with open(utvonal, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(fejlec) + "\n")
        for sor in sorok:
            fh.write("\t".join(str(sor.get(mezo, "")) for mezo in fejlec) + "\n")


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
    levelek = _levelek_argumentumbol(args)
    if levelek is None:
        return 2

    config = config_betolt()
    max_el_px = config.get("kepmeret_max_el_px", 2000)
    lapindex = hocr_lapindex_epit()

    hianyzo_levelek = [lv for lv in levelek if lv not in lapindex]
    if hianyzo_levelek:
        print("HIBA -- nincs a hOCR-ben:", hianyzo_levelek, file=sys.stderr)
        return 2

    if args.szaraz:
        return _futtat_szaraz(levelek, lapindex, max_el_px, config)

    modellek = config.get("modellek", {})
    hianyzo_modell = [k for k, v in modellek.items() if not v.get("nev")]
    if hianyzo_modell:
        print(
            "HIBA -- a config.modellek alatt nincs kitoltve a nev: %s "
            "(a modellneveket a felhasznalo tolti ki, l. CREMER_OCR_BRIEF.md C1)"
            % hianyzo_modell,
            file=sys.stderr,
        )
        return 1

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("HIBA -- az OPENROUTER_API_KEY kornyezeti valtozo nincs beallitva", file=sys.stderr)
        return 1

    return _futtat_eles(levelek, lapindex, max_el_px, config, modellek, api_key, args)


def _futtat_szaraz(levelek, lapindex, max_el_px, config):
    print("=== --szaraz: bemenet elokeszitese, %d level ===" % len(levelek))
    osszes_bemenet = 0
    osszes_kimenet = 0
    osszes_gyanus = 0
    modellek = config.get("modellek", {})
    aktiv_modellek = [k for k, v in modellek.items() if v.get("nev")] or list(modellek.keys()) or ["m1", "m2"]
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
    print("becsult bemenet token / level:", osszes_bemenet)
    print("becsult kimenet token / level:", osszes_kimenet)
    print("becsult bemenet token (mind a %d modellel):" % len(aktiv_modellek), osszes_bemenet * len(aktiv_modellek))
    print("becsult kimenet token (mind a %d modellel):" % len(aktiv_modellek), osszes_kimenet * len(aktiv_modellek))

    koltseg_ismert = False
    koltseg_osszesen = 0.0
    for k, v in modellek.items():
        ar_be = v.get("ar_bemenet_usd_per_1M")
        ar_ki = v.get("ar_kimenet_usd_per_1M")
        if ar_be is not None and ar_ki is not None:
            koltseg_ismert = True
            koltseg_osszesen += osszes_bemenet / 1_000_000 * ar_be + osszes_kimenet / 1_000_000 * ar_ki

    if koltseg_ismert:
        print("becsult koltseg (a configban megadott arakkal):", round(koltseg_osszesen, 4), "USD")
    else:
        print(
            "becsult koltseg: ISMERETLEN -- a config.modellek arai meg uresek "
            "(l. CREMER_OCR_BRIEF.md C1). Tajekoztato keresztellenorzeshez a D7 "
            "dontesnaplo durva becslese: kb. 5000 bemeneti + 1500 kimeneti "
            "token/lap/modell, ami a teljes 967 lapos kotetre ~10 USD lenne "
            "ket modellel egyutt (a 20 USD-s plafon alatt)."
        )

    print("\nmegjegyzes: a fenti tokenszamok tervezesi kozelitesek "
          "(kep ~pixel/750, szoveg ~karakter/4) -- a valodi tokenizalast a "
          "szolgaltato adja, csak a pilot-futas (O1) koltsegnaploja mondja meg pontosan.")
    return 0


def _futtat_eles(levelek, lapindex, max_el_px, config, modellek, api_key, args):
    koltsegplafon = config.get("koltsegplafon_pilot_usd" if args.pilot else "koltsegplafon_usd")
    naplo = KoltsegNaplo(koltsegplafon)
    eredmeny_sorok = []
    koltseg_sorok = []
    ujraprobalkozas = config.get("ujraprobalkozas_ervenytelen_json", 1)

    for level in levelek:
        if naplo.plafon_elerve_e():
            print("koltsegplafon elerve, leallas level=%d elott" % level, file=sys.stderr)
            break

        gyanus = level_gyanus_szavai(level, lapindex)
        if not gyanus:
            continue
        payload = level_payload(level, gyanus)
        kep_bytes, _, uj_meret = level_kep_jpeg(level, max_el_px)

        cserek_modellenkent = {}
        for kulcs, m in modellek.items():
            try:
                cserek = openrouter_hivas(m["nev"], kep_bytes, payload, api_key, ujraprobalkozas)
            except OpenRouterHiba:
                cserek = None
            cserek_by_id = {c["szo_id"]: c for c in cserek} if cserek else {}
            cserek_modellenkent[kulcs] = cserek_by_id

            bemenet_becsult = kep_token_becsles(uj_meret) + szoveg_token_becsles(json.dumps(payload, ensure_ascii=False))
            kimenet_becsult = kimenet_token_becsles(len(gyanus))
            osszeg = naplo.hozzaad(
                level, m["nev"], bemenet_becsult, kimenet_becsult,
                m.get("ar_bemenet_usd_per_1M"), m.get("ar_kimenet_usd_per_1M"),
            )
            koltseg_sorok.append(naplo.sorok[-1])

        modell_kulcsok = list(modellek.keys())
        if len(modell_kulcsok) >= 2:
            c1, c2 = modell_kulcsok[0], modell_kulcsok[1]
        else:
            c1 = c2 = modell_kulcsok[0] if modell_kulcsok else None

        for sz in gyanus:
            csere1 = cserek_modellenkent.get(c1, {}).get(sz["szo_id"])
            csere2 = cserek_modellenkent.get(c2, {}).get(sz["szo_id"])
            d = dontes(csere1, csere2)
            alak = csere1["alak"] if d == "auto" and csere1 else ""
            nyelv = csere1["nyelv"] if d == "auto" and csere1 else ""
            alak_igazolt = alak_igazolt_e(alak, nyelv) if alak else False
            eredmeny_sorok.append({
                "szo_id": sz["szo_id"], "level": level, "bbox": sz["bbox"],
                "ocr": sz["ocr"], "m1": json.dumps(csere1, ensure_ascii=False) if csere1 else "",
                "m2": json.dumps(csere2, ensure_ascii=False) if csere2 else "",
                "dontes": d, "alak_igazolt": "igen" if alak_igazolt else "nem",
            })

    return {"eredmeny_sorok": eredmeny_sorok, "koltseg_sorok": koltseg_sorok, "naplo": naplo}


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
    ap_futtat.add_argument("--config", type=str, default=CONFIG_UTVONAL)
    ap_futtat.set_defaults(func=cmd_futtat)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
