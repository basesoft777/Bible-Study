#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cremer_o06_meres.py -- CREMER_OCR_BRIEF.md O0.6: forrasmérés a cremuoft-tetelen
(biblicotheologic00cremuoft, archive.org), annak eldontesere, hogy ez legyen-e
az uj Cremer-OCR alapja a cu31924098819406 helyett (D19).

Nem hiv modellt es nem kuld halozati forgalmat az OpenRouter fele -- csak a mar
letoltott nyers fajlokat (konkordancia/_nyers/cremuoft/) dolgozza fel, es a
konkordancia/_nyers/cremer/ alatti cu31924098819406 anyagot hasznalja
referenciakent (level-oldal konkordancia, "angol szotar").

Alparancsok:
  ellenorzes -- a naplok/CREMER_O06_ellenorzes/ alle irja az O0.6.3 minta
                atnezo csomagjat (ATNEZES_NN.md oldalak + sorok.tsv).

A level-oldal lekepezes (O0.6.1c/O0.6.2, harmadik kor -- l. ELOKESZITES.md):
az elofej sajat digit-OCR-jebol szekvencialis konzisztencia-ellenorzessel
epult, MAJD a leveleket ket tiszta szakaszra simitva (a JSON pageNumber mezoje
level 606-890 kozott rendszeresen +3-mal ter el az elofejtol -- ez a JSON
sajat hibaja, nem kiadas-elteres). A ket vegleges szakasz:
    level 14-605 <-> oldal 2-593   (eltolas = level - oldal = 12)
    level 606-958 <-> oldal 591-943 (eltolas = 15)
A cu31924098819406 oldalszamait KIZAROLAG a sajat page_numbers.json adja --
annak elofej-OCR-je (mas motor, 2008) sajat, ELLENTETES iranyu, szisztematikus
hibat mutatott (ld. ELOKESZITES.md, vizualisan cafolva), ezert ott a JSON a
megbizhato forras, nem az elofej.
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

REPO_GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CR_NYERS = os.path.join(REPO_GYOKER, "konkordancia", "_nyers", "cremuoft")
CR_HOCR = os.path.join(CR_NYERS, "biblicotheologic00cremuoft_hocr.html")
CR_JP2ZIP = os.path.join(CR_NYERS, "biblicotheologic00cremuoft_jp2.zip")
CU_NYERS = os.path.join(REPO_GYOKER, "konkordancia", "_nyers", "cremer")
CU_HOCR = os.path.join(CU_NYERS, "cu31924098819406_hocr.html")
KI_DIR = os.path.join(REPO_GYOKER, "naplok", "CREMER_O06_ellenorzes")

sys.path.insert(0, os.path.join(REPO_GYOKER, "eszkozok"))
from cremer_ocr_javit import alak_igazolt_e, elonormalizal  # noqa: E402

# ---------------------------------------------------------------------------
# Level-oldal lekepezes (O0.6.1c/O0.6.2, vegleges, simitott -- l. docstring)
# ---------------------------------------------------------------------------

CR_SZAKASZOK = [
    (14, 605, 12),
    (606, 958, 15),
]


def cr_oldal(level):
    for l0, l1, off in CR_SZAKASZOK:
        if l0 <= level <= l1:
            return level - off
    return None


# ---------------------------------------------------------------------------
# hOCR feldolgozas -- szo-szintu bbox, nyomtatott sorokba klaszterezve
# ---------------------------------------------------------------------------

_PAGE_DIV_RE = re.compile(r'<div class="ocr_page"[^>]*title="([^"]*)"')
_WORD_RE = re.compile(r'<span class="ocrx_word"[^>]*title="([^"]*)"[^>]*>(.*?)</span>')
_BBOX_RE = re.compile(r'bbox (\d+) (\d+) (\d+) (\d+)')
_WCONF_RE = re.compile(r'x_wconf (\d+)')
_TAG_RE = re.compile(r'<[^>]+>')

LINE_Y_KUSZOB = 30  # px -- l. ELOKESZITES.md "Sor-klaszterezes szabalya"
SOR_MIN_SZELESSEG = 150  # px -- ez alatt margo-zaj, nem valodi nyomtatott sor


def _clean(raw):
    w = _TAG_RE.sub('', raw).strip()
    return w.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"')


def hocr_lapok_betolt(hocr_utvonal):
    with open(hocr_utvonal, encoding='utf-8') as f:
        content = f.read()
    starts = [m.start() for m in re.finditer(r'<div class="ocr_page"', content)]
    starts.append(len(content))
    return [content[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]


def lap_magassag(lap_html):
    m = _PAGE_DIV_RE.search(lap_html)
    if not m:
        return None
    bm = _BBOX_RE.search(m.group(1))
    if not bm:
        return None
    return int(bm.group(4)) - int(bm.group(2))


def sorokba_klaszterez(lap_html):
    """Nyomtatott sorok a szavak y-koordinatajabol (nem az ocr_line -- az egy
    egesz bekezdes, l. ELOKESZITES.md Modszertani megjegyzes). Visszaad egy
    listat: {bbox:(x0,y0,x1,y1), szavak:[(szoveg,wconf,bbox),...]}."""
    szavak = []
    for m in _WORD_RE.finditer(lap_html):
        title, raw = m.groups()
        szoveg = _clean(raw)
        if not szoveg:
            continue
        bm = _BBOX_RE.search(title)
        bbox = tuple(int(v) for v in bm.groups()) if bm else None
        wc = _WCONF_RE.search(title)
        wconf = int(wc.group(1)) if wc else None
        szavak.append((bbox, wconf, szoveg))

    klaszterek = []
    aktualis = []
    elozo_y = None
    for bbox, wconf, szoveg in szavak:
        y = bbox[1] if bbox else None
        if y is None:
            if aktualis:
                aktualis.append((bbox, wconf, szoveg))
            continue
        if elozo_y is None or abs(y - elozo_y) <= LINE_Y_KUSZOB:
            aktualis.append((bbox, wconf, szoveg))
        else:
            klaszterek.append(aktualis)
            aktualis = [(bbox, wconf, szoveg)]
        elozo_y = y
    if aktualis:
        klaszterek.append(aktualis)

    sorok = []
    for k in klaszterek:
        dobozok = [b for b, wc, sz in k if b is not None]
        if not dobozok:
            continue
        x0 = min(b[0] for b in dobozok)
        y0 = min(b[1] for b in dobozok)
        x1 = max(b[2] for b in dobozok)
        y1 = max(b[3] for b in dobozok)
        if (x1 - x0) < SOR_MIN_SZELESSEG:
            # margo-zaj (pl. lapszeli folt, kotesarnyek): a valodi nyomtatott
            # sorok szelessege a teljes szedestukoré (>1000 px), ez alatt nem
            # sor, hanem izolalt token -- l. ELOKESZITES.md "Sor-klaszterezes
            # szabalya" (level 466-on igazolva: 5 ilyen alkotta a kulonbseget
            # a kezi es a gepi sorszamlalas kozott).
            continue
        sorok.append({'bbox': (x0, y0, x1, y1), 'szavak': [(sz, wc, b) for b, wc, sz in k]})
    return sorok


# ---------------------------------------------------------------------------
# Gyanujelek: C5 alakellenorzes, latin torzkep-gyanu, heberdetektor
# ---------------------------------------------------------------------------

GOROG_RANGE_RE = re.compile(r'[Ͱ-Ͽἀ-῿]')
LATIN_SZO_RE = re.compile(r"^[A-Za-z][A-Za-z'\-]*$")
HEBER_JELZO_RE = re.compile(r'\b(Heb\.|LXX)\b')

_angol_szotar_cache = None


def angol_szotar_epit(cu_hocr_utvonal=CU_HOCR):
    """'Angol szo': a cu31924 hOCR-jeben x_wconf >= 90 mellett legalabb 3x
    elofordulo latin token (kisbetusitve, irasjel nelkul)."""
    global _angol_szotar_cache
    if _angol_szotar_cache is not None:
        return _angol_szotar_cache
    szamlalo = {}
    with open(cu_hocr_utvonal, encoding='utf-8') as f:
        content = f.read()
    for m in _WORD_RE.finditer(content):
        title, raw = m.groups()
        szoveg = _clean(raw)
        if not LATIN_SZO_RE.match(szoveg):
            continue
        wc = _WCONF_RE.search(title)
        wconf = int(wc.group(1)) if wc else 0
        if wconf < 90:
            continue
        kulcs = re.sub(r"[^A-Za-z']", '', szoveg).lower()
        if not kulcs:
            continue
        szamlalo[kulcs] = szamlalo.get(kulcs, 0) + 1
    _angol_szotar_cache = {k for k, v in szamlalo.items() if v >= 3}
    return _angol_szotar_cache


def sor_gyanujelek(sor_szavai, angol_szotar):
    """Visszaadja a sor gepi jelzeseit: lista (szo_index, kod, reszlet)."""
    jelek = []
    szoveg_lista = [sz for sz, wc, b in sor_szavai]
    van_gorog = any(GOROG_RANGE_RE.search(sz) for sz in szoveg_lista)
    van_heber_jelzo = bool(HEBER_JELZO_RE.search(' '.join(szoveg_lista)))

    latin_gyanus_idx = set()
    for i, (sz, wc, b) in enumerate(sor_szavai):
        if GOROG_RANGE_RE.search(sz):
            continue
        if not LATIN_SZO_RE.match(sz):
            continue
        kulcs = re.sub(r"[^A-Za-z']", '', sz).lower()
        if not kulcs or kulcs in angol_szotar:
            continue
        # gyanus, HA a soron gorog karakter, heber kontextusjelzo, vagy mas
        # mar gyanusnak jelolt latin token all -- ezt ket menetben dontjuk el
        latin_gyanus_idx.add(i)

    # masodik menet: csak akkor valodi 'latin torzkep-gyanu', ha a feltetel
    # (gorog / heber jelzo / masik gyanus token ugyanazon a soron) teljesul
    valodi_latin_gyanus = set()
    if latin_gyanus_idx and (van_gorog or van_heber_jelzo or len(latin_gyanus_idx) > 1):
        valodi_latin_gyanus = latin_gyanus_idx

    for i in valodi_latin_gyanus:
        jelek.append((i, 'latin_torzkep', sor_szavai[i][0]))

    if van_heber_jelzo and valodi_latin_gyanus:
        for i in valodi_latin_gyanus:
            jelek.append((i, 'heberdetektor', sor_szavai[i][0]))

    for i, (sz, wc, b) in enumerate(sor_szavai):
        if GOROG_RANGE_RE.search(sz):
            alak = sz.strip('.,;··’\'"()[]')
            if alak and not alak_igazolt_e(alak, 'grc'):
                jelek.append((i, 'c5_nem_igazolt', sz))

    return jelek, van_gorog


# ---------------------------------------------------------------------------
# Kepkivagas a jp2-zipbol
# ---------------------------------------------------------------------------

MAX_KIVAGAS_SZELESSEG = 1000


def level_kep(level, jp2zip_utvonal=CR_JP2ZIP):
    from PIL import Image
    nev = "biblicotheologic00cremuoft_jp2/biblicotheologic00cremuoft_%04d.jp2" % level
    with zipfile.ZipFile(jp2zip_utvonal) as z:
        nyers = z.read(nev)
    kep = Image.open(io.BytesIO(nyers))
    kep.load()
    return kep


def sor_kivagas_ments(kep, bbox, cel_utvonal, parnazas=20):
    from PIL import Image
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - 40)
    x1 = min(kep.width, x1 + 40)
    y0 = max(0, y0 - parnazas)
    y1 = min(kep.height, y1 + parnazas)
    resz = kep.crop((x0, y0, x1, y1)).convert('L')
    if resz.width > MAX_KIVAGAS_SZELESSEG:
        arany = MAX_KIVAGAS_SZELESSEG / resz.width
        resz = resz.resize((MAX_KIVAGAS_SZELESSEG, max(1, round(resz.height * arany))), Image.LANCZOS)
    os.makedirs(os.path.dirname(cel_utvonal), exist_ok=True)
    resz.save(cel_utvonal, format='JPEG', quality=85)


# ---------------------------------------------------------------------------
# O0.6.3 minta (rogzitett mag: 20260925)
# ---------------------------------------------------------------------------

MINTA_MAG = 20260925
FORESZ_ELSO = (14, 604)
SUPPLEMENT = (605, 928)


def minta_epit(lapok):
    kozep = (FORESZ_ELSO[0] + FORESZ_ELSO[1]) // 2
    elso_fele = list(range(FORESZ_ELSO[0], kozep + 1))
    masodik_fele = list(range(kozep + 1, FORESZ_ELSO[1] + 1))
    supplement = list(range(SUPPLEMENT[0], SUPPLEMENT[1] + 1))

    def gorog_szam(level):
        return len(GOROG_RANGE_RE.findall(_TAG_RE.sub(' ', lapok[level - 1])))

    pool = list(range(FORESZ_ELSO[0], SUPPLEMENT[1] + 1))
    szamok = {l: gorog_szam(l) for l in pool}
    rendezett = sorted(szamok.values())
    q75 = rendezett[int(0.75 * len(rendezett))]
    felso_negyed = [l for l in pool if szamok[l] >= q75]

    rng = random.Random(MINTA_MAG)
    p1 = rng.sample(elso_fele, 3)
    p2 = rng.sample(masodik_fele, 3)
    p3 = rng.sample(supplement, 3)
    p4 = rng.sample(felso_negyed, 3)

    ismert_oldalak = {
        'ábyssos (2)': 2, 'hádés-1 (67)': 67, 'epikatáratos (109)': 109,
        'epikaleo-1 (335)': 335, 'hádés-2/Supplement (610)': 610,
        'epikaleo-2/Supplement (742)': 742,
    }

    def level_for_oldal(oldal):
        for l0, l1, off in CR_SZAKASZOK:
            szamitott = oldal + off
            if l0 <= szamitott <= l1:
                return szamitott
        return None

    minta = []
    lattuk = set()

    def hozzaad(level, indok):
        if level not in lattuk:
            lattuk.add(level)
            minta.append((level, indok))

    for nev, oldal in ismert_oldalak.items():
        hozzaad(level_for_oldal(oldal), f"§0.5 ismert szócikk: {nev}")
    hozzaad(929, "görög szómutató első levele")
    hozzaad(949, "héber mutató első levele")
    for l in p1:
        hozzaad(l, "12-es minta: főrész 1. fele (mag 20260925)")
    for l in p2:
        hozzaad(l, "12-es minta: főrész 2. fele (mag 20260925)")
    for l in p3:
        hozzaad(l, "12-es minta: Supplement (mag 20260925)")
    for l in p4:
        hozzaad(l, "12-es minta: görögtoken-sűrű felső negyed (mag 20260925)")
    hozzaad(level_for_oldal(610), "horgonylap: ᾅδης Supplement-beli szócikkfeje")
    hozzaad(level_for_oldal(742), "horgonylap: ἐπικαλέω Supplement-beli szócikkfeje")

    return minta


# ---------------------------------------------------------------------------
# ATNEZES-oldalak es tsv iras
# ---------------------------------------------------------------------------

ITELETKOD_LISTA = """**Ítéletkódok** (CREMER_OCR_BRIEF.md O0.6.4): `ok`; `n<k>` nem-szó görög
(pl. Odvatos); `l<k>` latinosított görög (pl. Adtapoy, x.7.r.); `v<k>` valós szóra
cserélt görög (pl. ὅτε/ὅτι); `h<k>` csak ékezet-, hehezet-, iota subscriptum- vagy
koronishiba; `m<k>` a képen görög, a rétegből hiányzik; `e<k>` hibás vagy
latinosított héber hely. Egy sorban több kód is állhat, vesszővel elválasztva."""


def sorok_tsv_ir(utvonal, sorok):
    fejlec = ["sorszam", "level", "oldal", "bbox", "hocr_sor", "gepi_jelzesek", "itelet"]
    with open(utvonal, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(fejlec) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')


def atnezo_oldalak_ir(ki_dir, sorok_kepekkel, oldalankent=50):
    n = len(sorok_kepekkel)
    oldalszam = (n + oldalankent - 1) // oldalankent if n else 0
    for i in range(oldalszam):
        resz = sorok_kepekkel[i * oldalankent:(i + 1) * oldalankent]
        cel = os.path.join(ki_dir, "ATNEZES_%02d.md" % (i + 1))
        sorok = []
        if i == 0:
            sorok.append(ITELETKOD_LISTA)
            sorok.append("")
        sorok.append("| sorszám | kivágás | cremuoft-sor | gépi jelölés | ítélet |")
        sorok.append("|---|---|---|---|---|")
        for r in resz:
            sorok.append(r)
        with open(cel, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok) + '\n')
    return oldalszam


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_ellenorzes(args):
    os.makedirs(KI_DIR, exist_ok=True)
    lapok = hocr_lapok_betolt(CR_HOCR)
    minta = minta_epit(lapok)
    angol_szotar = angol_szotar_epit()

    tsv_sorok = []
    md_sorok = []
    sorszam = 0
    for level, indok in minta:
        lap_html = lapok[level - 1]
        oldal = cr_oldal(level)
        sorok = sorokba_klaszterez(lap_html)
        kep = None
        for sor in sorok:
            szoveg_lista = [sz for sz, wc, b in sor['szavak']]
            teljes_szoveg = ' '.join(szoveg_lista)
            van_gorog = any(GOROG_RANGE_RE.search(sz) for sz in szoveg_lista)
            jelek, _ = sor_gyanujelek(sor['szavak'], angol_szotar)
            heber_talalat = any(k == 'heberdetektor' for _, k, _ in jelek)
            latin_talalat = any(k == 'latin_torzkep' for _, k, _ in jelek)
            if not (van_gorog or latin_talalat or heber_talalat):
                continue
            sorszam += 1
            if kep is None:
                kep = level_kep(level)
            kep_nev = "level%04d_sor%03d.jpg" % (level, sorszam)
            kep_utvonal = os.path.join(KI_DIR, "kepek", kep_nev)
            sor_kivagas_ments(kep, sor['bbox'], kep_utvonal)
            jel_szoveg = ', '.join(sorted({k for _, k, _ in jelek})) if jelek else '(csak görög, jelzés nélkül)'
            hocr_sor_tsv = teljes_szoveg.replace('\t', ' ')
            tsv_sorok.append([
                str(sorszam), str(level), str(oldal) if oldal is not None else '',
                '%d,%d,%d,%d' % sor['bbox'], hocr_sor_tsv, jel_szoveg, '',
            ])
            kep_rel = "kepek/%s" % kep_nev
            hocr_sor_md = teljes_szoveg.replace('|', '\\|')
            md_sorok.append(
                "| %d | ![](%s) | %s | %s |  |" % (sorszam, kep_rel, hocr_sor_md, jel_szoveg)
            )

    sorok_tsv_ir(os.path.join(KI_DIR, "sorok.tsv"), tsv_sorok)
    oldalszam = atnezo_oldalak_ir(KI_DIR, md_sorok)

    print("Minta levelek: %d" % len(minta))
    for level, indok in minta:
        print("  level %d (oldal %s): %s" % (level, cr_oldal(level), indok))
    print("Osszes megjelolt sor: %d" % sorszam)
    print("ATNEZES-oldalak: %d" % oldalszam)
    print("tsv: %s" % os.path.join(KI_DIR, "sorok.tsv"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='parancs', required=True)
    p_ell = sub.add_parser('ellenorzes', help='O0.6.3-4 ellenorzo csomag')
    p_ell.set_defaults(func=cmd_ellenorzes)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
