#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cremer_o1_diagnosztika.py -- O0.5e/5: diagnosztika a 20 pilot-lap MEGLEVO
adataibol (gyorsitotar + hibanaplo), halozati hivas NELKUL -- a jelenlegi
_cserek_validal/level_dontesek szabalyokkal ujraertelmezve.

Egy lap csak akkor kap TELJES dontes-sort, ha MINDKET modellnek van
gyorsitotar-talalata (sikeres valasz). Ahol csak az egyik van meg (pl. a Qwen
meg nem lett ujrafuttatva v5-tel), a lap "adathianyos"-kent jelolve marad ki a
dontes-eloszlasbol, de az elvetett_nem_gyanus es ervenytelen szamlalas a
hibanaplobol arra a modellre/lapra is lefut.

CLI:
    python eszkozok/cremer_o1_diagnosztika.py

Kimenet: naplok/CREMER_O1_diagnosztika.md
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import glob
import json
import os
import random
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cremer_ocr_javit as m

KIMENET = os.path.join(m.REPO_GYOKER, "naplok", "CREMER_O1_diagnosztika.md")
MINTA_MAG = 20260924
MINTA_DB = 30


def _ekezet_nelkul(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _elem_nyelv(elem_resz):
    if isinstance(elem_resz, dict):
        return elem_resz.get("nyelv")
    if isinstance(elem_resz, list) and elem_resz:
        return elem_resz[0].get("nyelv")
    return None


def _hiba_naplo_elemek(model_id, level):
    """A KORABBAN (barmilyen prompt_verzio alatt) irt hibanaplo-fajlok (minden
    kiserlet) elemei -- UJRAOSZTALYOZVA a jelenlegi szabaly szerint: a v4 alatt
    meg mindent 'ervenytelen_elemek'-be iro kod a "nem-'x' elem..." kezdetu
    hibaszoveggel jelolt elemeket most Qwen-zajkent ('elvetett_nem_gyanus')
    szamolja, nem valodi semasertoskent -- ez az O0.5e/5 lenyege: a MEGLEVO
    adatot az UJ szabalyokkal ertelmezzuk ujra, halozati hivas nelkul."""
    minta = os.path.join(m.HIBA_DIR, m._modell_slug(model_id), "%04d_*.json" % level)
    ervenytelen = []
    elvetett = []
    for p in sorted(glob.glob(minta)):
        with open(p, encoding="utf-8") as fh:
            adat = json.load(fh)
        for e in adat.get("ervenytelen_elemek", []):
            if e.get("hiba", "").startswith("nem-'x' elem"):
                elvetett.append(e)
            else:
                ervenytelen.append(e)
        elvetett.extend(adat.get("elvetett_nem_gyanus_elemek", []))
    return ervenytelen, elvetett


def fo():
    lapindex = m.hocr_lapindex_epit()
    levelek = m.pilot_levelek()
    config = m.config_betolt()
    modellek = config["modellek"]
    k1, k2 = "m1", "m2"
    m1_id = modellek[k1]["nev"]
    m2_id = modellek[k2]["nev"]

    dontes_szamlalo = {}  # (dontes, nyelv) -> db
    vitas_bontas = {"csak_diakritika": 0, "betukulonbseg": 0, "eltero_szo_ids": 0, "eltero_nyelv": 0}
    elvetett_szamlalo = {m1_id: 0, m2_id: 0}
    ervenytelen_szamlalo = {m1_id: 0, m2_id: 0}
    vitas_minta_forras = []
    adathianyos_lapok = []
    feldolgozott_lapok = 0

    for level in levelek:
        sorok = m.level_sorok(level, lapindex)
        _, eredeti_meret, uj_meret = m.level_kep_jpeg(level, config.get("kepmeret_max_el_px", 2000))
        payload, ctx, gyanus_db = m.level_payload_es_ctx(level, sorok, eredeti_meret, uj_meret)
        ocr_by_id = {w["szo_id"]: w["ocr"] for sor in sorok for w in sor["szavak"]}

        eredmenyek = {}
        for kulcs, model_id in ((k1, m1_id), (k2, m2_id)):
            ervenytelen_h, elvetett_h = _hiba_naplo_elemek(model_id, level)
            ervenytelen_szamlalo[model_id] += len(ervenytelen_h)
            elvetett_szamlalo[model_id] += len(elvetett_h)

            talalat = m.cache_olvas(model_id, level)
            if talalat is None:
                eredmenyek[kulcs] = None
                continue
            tartalom = talalat["nyers_valasz"]["choices"][0]["message"]["content"]
            try:
                ervenyes, _ervenytelen, _elvetett = m._cserek_validal(json.loads(tartalom), ctx)
            except (json.JSONDecodeError, ValueError, KeyError):
                ervenyes = None
            eredmenyek[kulcs] = ervenyes

        if eredmenyek[k1] is None or eredmenyek[k2] is None:
            adathianyos_lapok.append(level)
            continue

        feldolgozott_lapok += 1
        sorok_d, _ = m.level_dontesek(ctx, eredmenyek[k1], eredmenyek[k2])
        for d_sor in sorok_d:
            nyelv = _elem_nyelv(d_sor["m1"]) or _elem_nyelv(d_sor["m2"]) or "nincs"
            dontes_szamlalo[(d_sor["dontes"], nyelv)] = dontes_szamlalo.get((d_sor["dontes"], nyelv), 0) + 1

            if d_sor["dontes"] == "vitas":
                c1, c2 = d_sor["m1"], d_sor["m2"]
                if isinstance(c1, dict) and isinstance(c2, dict) and c1["szo_ids"] == c2["szo_ids"]:
                    if c1["nyelv"] != c2["nyelv"]:
                        vitas_bontas["eltero_nyelv"] += 1
                    elif _ekezet_nelkul(m.elonormalizal(c1["alak"])) == _ekezet_nelkul(m.elonormalizal(c2["alak"])):
                        vitas_bontas["csak_diakritika"] += 1
                    else:
                        vitas_bontas["betukulonbseg"] += 1
                else:
                    vitas_bontas["eltero_szo_ids"] += 1
                ocr_szoveg = " ".join(ocr_by_id.get(sid, "") for sid in d_sor["szo_ids"])
                vitas_minta_forras.append({
                    "level": level, "hocr": ocr_szoveg,
                    "m1": json.dumps(c1, ensure_ascii=False) if c1 else "",
                    "m2": json.dumps(c2, ensure_ascii=False) if c2 else "",
                })

    rng = random.Random(MINTA_MAG)
    vitas_minta = (rng.sample(vitas_minta_forras, MINTA_DB)
                   if len(vitas_minta_forras) > MINTA_DB else list(vitas_minta_forras))
    vitas_minta.sort(key=lambda r: r["level"])

    sorok_md = []
    sorok_md.append("# CREMER O1 diagnosztika (O0.5e/5)")
    sorok_md.append("")
    sorok_md.append(
        "A 20 pilot-lap MEGLEVO gyorsitotar- es hibanaplo-adatabol, halozati hivas NELKUL, "
        "a jelenlegi validalasi/dontesi szabalyokkal (elemszintu validalas + Qwen-zaj kulon "
        "kezelese, D15/D17) ujraertelmezve. `m1` = `%s`, `m2` = `%s`." % (m1_id, m2_id)
    )
    sorok_md.append("")
    sorok_md.append("Teljes dontessel feldolgozott lap: **%d / %d**." % (feldolgozott_lapok, len(levelek)))
    if adathianyos_lapok:
        sorok_md.append(
            "Adathianyos lap (legalabb az egyik modellnek nincs gyorsitotar-talalata, "
            "a teljes dontes-eloszlasbol kimaradt): **%s**." % ", ".join(str(x) for x in sorted(adathianyos_lapok))
        )
    sorok_md.append("")

    sorok_md.append("## a) dontes-eloszlas, nyelvenkent")
    sorok_md.append("")
    sorok_md.append("| dontes | nyelv | darab |")
    sorok_md.append("|---|---|---|")
    for (d, nyelv), n in sorted(dontes_szamlalo.items(), key=lambda x: (-x[1], x[0])):
        sorok_md.append("| %s | %s | %d |" % (d, nyelv, n))
    osszesen = sum(dontes_szamlalo.values())
    sorok_md.append("| **osszesen** | | **%d** |" % osszesen)
    sorok_md.append("")

    sorok_md.append("## b) a `vitas` sorok bontasa")
    sorok_md.append("")
    sorok_md.append("| tipus | darab |")
    sorok_md.append("|---|---|")
    sorok_md.append("| csak ekezet/hehezet kulonbseg | %d |" % vitas_bontas["csak_diakritika"])
    sorok_md.append("| betukulonbseg | %d |" % vitas_bontas["betukulonbseg"])
    sorok_md.append("| eltero szo_ids | %d |" % vitas_bontas["eltero_szo_ids"])
    sorok_md.append("| eltero nyelv | %d |" % vitas_bontas["eltero_nyelv"])
    sorok_md.append("")

    sorok_md.append("## c) `elvetett_nem_gyanus` es valodi `ervenytelen` elemek modellenkent")
    sorok_md.append("")
    sorok_md.append("(a hibanaplo OSSZES eddig irt kiserletebol, a 20 pilot-lapra -- adathianyos "
                     "lapoknal is, mert ott is lehetett mar hibanaplo-bejegyzes egy korabbi kiserletbol)")
    sorok_md.append("")
    sorok_md.append("| modell | elvetett_nem_gyanus | valodi ervenytelen |")
    sorok_md.append("|---|---|---|")
    for model_id in (m1_id, m2_id):
        sorok_md.append("| %s | %d | %d |" % (model_id, elvetett_szamlalo[model_id], ervenytelen_szamlalo[model_id]))
    sorok_md.append("")

    sorok_md.append("## d) %d veletlen `vitas` sor (mag: %d)" % (len(vitas_minta), MINTA_MAG))
    sorok_md.append("")
    sorok_md.append("| level | hOCR | m1 | m2 |")
    sorok_md.append("|---|---|---|---|")
    for r in vitas_minta:
        sorok_md.append("| %s | %s | %s | %s |" % (
            r["level"], r["hocr"].replace("|", "\\|"), r["m1"].replace("|", "\\|"), r["m2"].replace("|", "\\|"),
        ))
    sorok_md.append("")

    os.makedirs(os.path.dirname(KIMENET), exist_ok=True)
    with open(KIMENET, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sorok_md) + "\n")
    print("irva:", KIMENET)
    print("feldolgozott lap:", feldolgozott_lapok, "/", len(levelek))
    print("adathianyos lapok:", adathianyos_lapok)


if __name__ == "__main__":
    fo()
