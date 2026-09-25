#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t2_2_teremt002_atvezetes.py — TEREMT002_KUTATAS_BRIEF.md T2.2: a 2026.09.25-i
minősítési döntés átvezetése.

  1. `adat/jeloltek.tsv` — a 66 TEREMT-002 sor `dontes`, `indoklas`,
     `karoli_szo`, `azonositas_modja`, `megbizhatosag` mezője a
     `naplok/T2_TEREMT002_minosites.tsv` szerint; minden más sor és a
     sorrend változatlan (ellenőrizve, eltérésnél megáll).
  2. `naplok/T2_TEREMT002_elofordulasok_munkalap.tsv` — a `betolt.py beepit`
     bemenete a 3 beépített sorra (az `elofordulasok.tsv`-t a beepit írja).
  3. `adat/kapcsolatok.tsv` — az 5 jóváhagyott kapcsolat hozzáfűzése (G10).

Használat:
    python eszkozok/t2_2_teremt002_atvezetes.py          # száraz futás
    python eszkozok/t2_2_teremt002_atvezetes.py --ir
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eszkozok"))
import t2_1_teremt002_minosites as M  # noqa: E402  (a PAR kapcsolodas-szövegei)

ADAT = ROOT / "adat"
NAPLOK = ROOT / "naplok"
ID = "TEREMT-002"
JEL_MEZOK = ["dontes", "indoklas", "karoli_szo", "azonositas_modja", "megbizhatosag"]


def nyers_sorok(path):
    szoveg = path.read_bytes().decode("utf-8")
    if "\r" in szoveg:
        sys.exit("HIBA: CRLF: %s" % path)
    if not szoveg.endswith("\n"):
        sys.exit("HIBA: nincs záró sorvég: %s" % path)
    return szoveg[:-1].split("\n")


def tabla(path):
    """(összes nyers sor, fejléc-index, fejléc) — split('\\t')."""
    sorok = nyers_sorok(path)
    fi = next(i for i, s in enumerate(sorok) if not s.startswith("#"))
    return sorok, fi, sorok[fi].split("\t")


def munkalap(path):
    sorok, fi, fej = tabla(path)
    return [dict(zip(fej, s.split("\t"))) for s in sorok[fi + 1:] if s]


def kollokacio_prov():
    sorok, fi, fej = tabla(ADAT / "auditok.tsv")
    talalat = [dict(zip(fej, s.split("\t"))) for s in sorok[fi + 1:]]
    talalat = [r["proveniencia"] for r in talalat if r["id"] == ID
               and "strong=H8414+H0922 |" in r["proveniencia"]
               and r["proveniencia"].startswith("scope=TAHOT-teljes+TAGNT-teljes")]
    if len(talalat) != 1:
        sys.exit("HIBA: a kollokáció audit-sora nem egyértelmű: %d" % len(talalat))
    return talalat[0]


def main():
    ap = argparse.ArgumentParser(description="T2.2 — TEREMT-002 átvezetés")
    ap.add_argument("--ir", action="store_true")
    a = ap.parse_args()

    dont = {r["igehely"]: r for r in munkalap(NAPLOK / "T2_TEREMT002_minosites.tsv")}
    if len(dont) != 66:
        sys.exit("HIBA: %d döntés-sor a 66 helyett" % len(dont))

    # --- 1. jeloltek.tsv --------------------------------------------------
    sorok, fi, fej = tabla(ADAT / "jeloltek.tsv")
    ix = {m: fej.index(m) for m in fej}
    uj, valt, latott = [], 0, set()
    for i, s in enumerate(sorok):
        if i <= fi or not s:
            uj.append(s)
            continue
        m = s.split("\t")
        if m[0] != ID:
            uj.append(s)
            continue
        d = dont.get(m[ix["igehely"]])
        if d is None:
            sys.exit("HIBA: döntés nélküli jelölt: %s" % m[ix["igehely"]])
        if m[ix["dontes"]] != "nyitva":
            sys.exit("HIBA: már minősített jelölt: %s" % m[ix["igehely"]])
        m[ix["dontes"]] = d["javaslat"]
        for f in JEL_MEZOK[1:]:
            m[ix[f]] = d[f]
        latott.add(m[ix["igehely"]])
        uj.append("\t".join(m))
        valt += 1
    if valt != 66 or latott != set(dont):
        sys.exit("HIBA: %d sor frissült, a halmaz eltér" % valt)
    elter = [(x, y) for x, y in zip(sorok, uj) if x != y]
    assert len(sorok) == len(uj) and len(elter) == 66
    assert all(x.split("\t")[0] == ID for x, _ in elter)
    print("jeloltek.tsv: %d TEREMT-002 sor frissül (beépítve %d, elutasítva %d)" % (
        valt, sum(1 for d in dont.values() if d["javaslat"] == "beépítve"),
        sum(1 for d in dont.values() if d["javaslat"] == "elutasítva")))

    # --- 2. beépítési munkalap ------------------------------------------
    _, _, efej = tabla(ADAT / "elofordulasok.tsv")
    prov = kollokacio_prov()
    beep = []
    for ih, d in dont.items():
        if d["javaslat"] != "beépítve":
            continue
        r = {f: "" for f in efej}
        r.update(id=ID, igehely=ih, kapcsolodas=M.PAR[ih]["kapcsolodas"],
                 pardes_szint=d["pardes_szint"], funkcio=d["funkcio"],
                 gerinc_elem=d["gerinc_elem"], strong=d["strong"],
                 karoli_szo=d["karoli_szo"], azonositas_modja=d["azonositas_modja"],
                 megbizhatosag=d["megbizhatosag"], proveniencia=prov,
                 igazolas="TAHOT-igazolt", fo_elofordulas=d["fo_elofordulas"])
        beep.append(r)
    for r in beep:
        for v in r.values():
            assert "\t" not in v and "\n" not in v
    ml = ["# T2.2 munkalap -- betolt.py beepit formátumában. Sema: adat/SEMA.md 2.2",
          "\t".join(efej)] + ["\t".join(r[f] for f in efej) for r in beep]
    print("beépítési munkalap: %d sor" % len(beep))

    # --- 3. kapcsolatok.tsv ----------------------------------------------
    ksorok, kfi, kfej = tabla(ADAT / "kapcsolatok.tsv")
    kulcs = {tuple(s.split("\t")[:3]) for s in ksorok[kfi + 1:]}
    kuj = [k for k in munkalap(NAPLOK / "T2_TEREMT002_kapcsolatok_javaslat.tsv")]
    if len(kuj) != 5:
        sys.exit("HIBA: %d kapcsolat az 5 helyett" % len(kuj))
    for k in kuj:
        if (k["forras_igehely"], k["cel_igehely"], k["id"]) in kulcs:
            sys.exit("HIBA: már létező kapcsolat: %r" % k)
        if k["tipus"] not in ("Előkép", "Párhuzam", "Beteljesedés", "Kontraszt", "Variáns"):
            sys.exit("HIBA: tipus: %r" % k["tipus"])
        if k["bizonyossag"] not in ("magas", "közepes", "alacsony"):
            sys.exit("HIBA: bizonyossag: %r" % k["bizonyossag"])
    kuj_sorok = ["\t".join(k[f] for f in kfej) for k in kuj]
    print("kapcsolatok.tsv: %d sor + %d új" % (len(ksorok) - kfi - 1, len(kuj_sorok)))

    if a.ir:
        (ADAT / "jeloltek.tsv").write_bytes(("\n".join(uj) + "\n").encode("utf-8"))
        (NAPLOK / "T2_TEREMT002_elofordulasok_munkalap.tsv").write_bytes(
            ("\n".join(ml) + "\n").encode("utf-8"))
        (ADAT / "kapcsolatok.tsv").write_bytes(
            ("\n".join(ksorok + kuj_sorok) + "\n").encode("utf-8"))
        print("ÍRVA")
    else:
        print("száraz futás — nincs írás")


if __name__ == "__main__":
    main()
