#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t1_teremt002_munkalap.py — TEREMT002_KUTATAS_BRIEF.md T1.1: a TEREMT-002
(תֹהוּ וָבֹהוּ) lekérdezései munkalapba.

Nem ír az `adat/`-ba (G3): a jelöltek és az auditok sorai a `naplok/`
munkalapjaira kerülnek, a `jeloltek.tsv` / `auditok.tsv` oszlopaival; a
betöltés a gate ⛔ utáni T1.3 tárgya.

Két fázis:
  A — a hét lépésből az 1–6.: gerinc, domén (a B3 támasza), scan, kollokáció
      (a gerinc-pár és a mező-szavak a gerinccel), igealak (a mező igei
      tagjára), valamint a 19 tohu-versre lxx-hid, tsk, karoli.
  B — a három magvers TSK/Károli-KH célpontjai jelöltek lesznek; ezekre is
      lefut a tsk, a karoli és (ÓSZ-helyre) az lxx-hid. Ezek célpontjai már
      NEM lesznek jelöltek (nincs rekurzió): a másodrendű listába kerülnek,
      ahogy a nem-mag tohu-versek TSK/KH-célpontjai és az igealak versei is.
      A másodrendű lista jelöltté léptetése gate-kérdés.

A nyers lekérdezés-kimenet a `--nyers` könyvtárba megy (a repón kívül);
a fő szálba csak a munkalapok és az összesítő kerül.

Használat:
    python eszkozok/t1_teremt002_munkalap.py --nyers <repón kívüli könyvtár>
    python eszkozok/t1_teremt002_munkalap.py --nyers <…> --ir   # naplok/ írása
"""

import argparse
import datetime
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
LEKERDEZ = ROOT / "eszkozok" / "lekerdez.py"
NAPLOK = ROOT / "naplok"
ID = "TEREMT-002"
DATUM = datetime.date.today().strftime("%Y.%m.%d")

MAG = ["1Móz 1:2", "Jer 4:23", "Ézs 34:11"]
PAR = set(MAG)  # a kollokáció méri; lent ellenőrizve

# B3 mező-hipotézis (T1_TEREMT002_scan.md 2. pont): a mező-szavak a gerinccel
# kollokálva; a H0950+H4003 és a H0922+H1238 külön szonda.
MEZO = ["H0657", "H0205", "H7385", "H1892", "H6957", "H0068", "H0216",
        "H4057", "H8077", "H0950", "H1238"]
MEZO_IGEI = ["H1238"]

# A Károli-KH és a TSK saját rövidítései -> SEMA 1.1 kanonikus alak.
KONYV_ALIAS = {"Ésa": "Ézs", "Ezék": "Ez"}


# ---------------------------------------------------------------------------

def read_tsv(path):
    """split('\\t') — a csv modul ezeken a táblákon adatot ront (CLAUDE.md)."""
    with open(path, encoding="utf-8") as f:
        sorok = [ln.rstrip("\n").rstrip("\r") for ln in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith("#")]
    fej = sorok[0].split("\t")
    return [dict(zip(fej, s.split("\t"))) for s in sorok[1:]]


def osz_konyvek():
    sorok = read_tsv(ROOT / "konkordancia" / "Konyv_normalizalo_tabla.tsv")
    magyar = [s["Magyar rövidítés"] for s in sorok]
    assert magyar[38] == "Mal", "a könyvtábla sorrendje nem kanonikus"
    return set(magyar[:39])


OSZ = None


def norm(ih):
    ih = ih.strip().replace(",", ":")
    k, rest = ih.split(" ", 1)
    return KONYV_ALIAS.get(k, k) + " " + rest


def konyv(ih):
    return ih.rsplit(" ", 1)[0]


class Futtato:
    def __init__(self, nyers):
        self.nyers = nyers
        self.hivasok = []  # (lepes, args, proveniencia, fajl)
        self.kimenet = {}

    def fut(self, lepes, args):
        kulcs = tuple(args)
        if kulcs in self.kimenet:
            return self.kimenet[kulcs]
        r = subprocess.run([sys.executable, str(LEKERDEZ)] + args,
                           capture_output=True, text=True, encoding="utf-8",
                           cwd=ROOT)
        ki = r.stdout + r.stderr
        nev = "%03d_%s.txt" % (len(self.hivasok),
                               "_".join(a.replace(" ", "").replace(":", "-")
                                        for a in args))
        (self.nyers / nev).write_text(ki, encoding="utf-8")
        p = [ln for ln in ki.splitlines() if ln.startswith("proveniencia: ")]
        if not p:
            sys.exit("HIBA: nincs proveniencia-sor: %s (kód %d)\n%s"
                     % (" ".join(args), r.returncode, ki[-500:]))
        self.hivasok.append((lepes, args, p[-1][len("proveniencia: "):], nev))
        self.kimenet[kulcs] = ki
        return ki


def talalat_versek(ki):
    """scan / kollokacio kimenetéből az igehely-sorok."""
    return [ln.split("\t")[0] for ln in ki.splitlines()
            if ln and not ln.startswith("#") and not ln.startswith("proveniencia")]


def igealak_versek(ki):
    v = []
    for ln in ki.splitlines():
        if ln and not ln.startswith("#") and not ln.startswith("proveniencia"):
            ih = ln.split("\t")[0]
            if ih not in v:
                v.append(ih)
    return v


def tsk_celok(ki):
    ki_l = []
    for ln in ki.splitlines()[1:]:
        if ln.startswith("#") or ln.startswith("proveniencia") or not ln.strip():
            continue
        ih, votes = ln.split("\t")
        ki_l.append((norm(ih), votes.replace("Votes=", "")))
    return ki_l


def kh_celok(ki):
    ki_l, bent = [], False
    for ln in ki.splitlines():
        if ln.startswith("# Károli-KH ("):
            bent = True
            continue
        if bent and ln.strip() and not ln.startswith("proveniencia"):
            ki_l.append(norm(ln))
    return ki_l


def karoli_szoveg(ki):
    s = ki.splitlines()
    return s[1] if len(s) > 1 else ""


def versek_kibontasa(ih):
    """`Ez 34:12-16` -> [Ez 34:12 … Ez 34:16]; fejezeten átnyúlót nem bont."""
    if "-" not in ih:
        return [ih]
    k, hely = ih.rsplit(" ", 1)
    fej, versek = hely.split(":", 1)
    a, b = versek.split("-", 1)
    if ":" in b:
        return [ih]
    return ["%s %s:%d" % (k, fej, v) for v in range(int(a), int(b) + 1)]


# ---------------------------------------------------------------------------

def main():
    global OSZ
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--nyers", required=True,
                    help="könyvtár a nyers kimenetnek (a repón kívül)")
    ap.add_argument("--ir", action="store_true",
                    help="a naplok/ munkalapjainak írása")
    a = ap.parse_args()
    nyers = Path(a.nyers).resolve()
    if ROOT in nyers.parents or nyers == ROOT:
        sys.exit("HIBA: a --nyers könyvtár a repón belül van")
    nyers.mkdir(parents=True, exist_ok=True)
    OSZ = osz_konyvek()
    F = Futtato(nyers)

    # --- A fázis ----------------------------------------------------------
    F.fut("B2", ["gerinc"] + MAG)
    tohu = talalat_versek(F.fut("B4", ["scan", "H8414"]))
    bohu = talalat_versek(F.fut("B4", ["scan", "H0922"]))
    par = talalat_versek(F.fut("B4", ["kollokacio", "H8414", "H0922"]))
    mezo_koll = {}
    for s in MEZO:
        mezo_koll[s] = talalat_versek(F.fut("B4", ["kollokacio", "H8414", s]))
    mezo_koll["H0922+H1238"] = talalat_versek(
        F.fut("B4", ["kollokacio", "H0922", "H1238"]))
    mezo_koll["H0950+H4003"] = talalat_versek(
        F.fut("B4", ["kollokacio", "H0950", "H4003"]))
    igealak = {}
    for s in MEZO_IGEI:
        igealak[s] = igealak_versek(F.fut("B4", ["igealak", s]))
    F.fut("B3", ["domen", "H8414", "H0922"])
    F.fut("B3", ["domen", "H8414"])
    F.fut("B3", ["domen", "H0922"])

    lexikai = list(tohu)
    for ih in bohu:
        if ih not in lexikai:
            lexikai.append(ih)
    tsk_ki, kh_ki, karoli_ki = {}, {}, {}
    for ih in lexikai:
        F.fut("B4", ["lxx-hid", ih])
    for ih in lexikai:
        tsk_ki[ih] = tsk_celok(F.fut("A5", ["tsk", ih]))
    for ih in lexikai:
        k = F.fut("A5", ["karoli", ih])
        kh_ki[ih] = kh_celok(k)
        karoli_ki[ih] = karoli_szoveg(k)

    # --- jelöltek ----------------------------------------------------------
    jelolt = {}  # igehely -> {"forras": [...], "tipus": ...}

    def felvesz(ih, forras, tipus):
        j = jelolt.setdefault(ih, {"forras": [], "tipus": tipus})
        if forras not in j["forras"]:
            j["forras"].append(forras)

    for ih in lexikai:
        tip = "par" if ih in par else ("tohu" if ih in tohu else "bohu")
        if ih in tohu:
            felvesz(ih, "scan H8414", tip)
        if ih in bohu:
            felvesz(ih, "scan H0922", tip)
        if ih in par:
            felvesz(ih, "kollokacio H8414+H0922", tip)
    for ih in MAG:
        for cel, v in tsk_ki[ih]:
            felvesz(cel, "TSK %s (Votes=%s)" % (ih, v), "tsk")
        for cel in kh_ki[ih]:
            felvesz(cel, "Károli-KH (forrás-vers: %s)" % ih, "kh")

    # --- B fázis: a nem-lexikai jelöltekre is tsk, karoli, lxx-hid ------------
    # A lekerdez.py tartományt nem fogad: a tartomány-jelölt versenként fut.
    for ih in [i for i in jelolt if i not in lexikai]:
        tsk_ki[ih], kh_ki[ih], szov = [], [], []
        for v in versek_kibontasa(ih):
            if konyv(v) in OSZ:
                F.fut("B4", ["lxx-hid", v])
            tsk_ki[ih] += tsk_celok(F.fut("A5", ["tsk", v]))
            k = F.fut("A5", ["karoli", v])
            kh_ki[ih] += kh_celok(k)
            szov.append(karoli_szoveg(k))
        karoli_ki[ih] = " ".join(szov)

    # --- másodrendű találatok (nem jelöltek) -------------------------------
    masod = defaultdict(list)
    for ih, celok in tsk_ki.items():
        if ih in MAG:
            continue
        for cel, v in celok:
            if cel not in jelolt:
                masod[cel].append("TSK %s (Votes=%s)" % (ih, v))
    for ih, celok in kh_ki.items():
        if ih in MAG:
            continue
        for cel in celok:
            if cel not in jelolt:
                masod[cel].append("Károli-KH (forrás-vers: %s)" % ih)
    for s, versek in igealak.items():
        for ih in versek:
            if ih not in jelolt:
                masod[ih].append("igealak %s" % s)
    for s, versek in mezo_koll.items():
        for ih in versek:
            if ih not in jelolt:
                masod[ih].append("kollokacio %s" % (s if "+" in s else "H8414+" + s))

    # --- indoklás (nyitva: G4) -------------------------------------------
    KH_HIBA = "Ézs 34:11"

    def indoklas(ih, j):
        t = j["tipus"]
        if t == "par":
            return ("T1: minősítetlen (G4). A tohu+bohu pár kollokációs "
                    "találata; gerinc_elem-javaslat (G5): tohu+bohu.")
        if t == "tohu":
            return ("T1: minősítetlen (G4). Önálló H8414-előfordulás, bohu "
                    "nélkül; gerinc_elem-javaslat (G5): tohu.")
        if t == "bohu":
            return ("T1: minősítetlen (G4). Önálló H0922-előfordulás; "
                    "gerinc_elem-javaslat (G5): bohu.")
        megj = ("T1: minősítetlen (G4). Kereszthivatkozás-célpont, a versben "
                "nincs H8414/H0922 — lexikai gerinc_elem nem nevezhető meg; "
                "ha a T2.1-ben sem, a jeloltek.tsv-ben marad.")
        if any(f == "Károli-KH (forrás-vers: %s)" % KH_HIBA for f in j["forras"]):
            megj += (" ADATHIBA-GYANÚ: a Karoli_kereszthivatkozasok.tsv "
                     "Isa.34.11 KH-listája betűre azonos az Isa.40.11-ével "
                     "(pásztor-kép); a célpont valószínűleg nem az Ézs 34:11-é.")
        return megj

    jel_sorok = []
    for ih, j in jelolt.items():
        jel_sorok.append([ID, ih, "; ".join(j["forras"]), "nyitva",
                          indoklas(ih, j), "", "", "", DATUM])

    aud_sorok = [[ID, lep, prov, DATUM] for lep, _, prov, _ in F.hivasok]
    aud_sorok.append([ID, "B4",
                      "scope=manual | forras=nem alkalmazható: igealak a "
                      "gerinc-elemekre (H8414, H0922 — mindkettő főnév) | ts="
                      + datetime.datetime.now(datetime.timezone.utc)
                      .strftime("%Y-%m-%dT%H:%M") + "Z", DATUM])

    masod_sorok = [[ih, "; ".join(f)] for ih, f in sorted(masod.items())]

    # --- átfedés más motívumokkal (T1.2) ---------------------------------
    elo = read_tsv(ROOT / "adat" / "elofordulasok.tsv")
    jel = read_tsv(ROOT / "adat" / "jeloltek.tsv")
    jelolt_versek = {}
    for ih in jelolt:
        for v in versek_kibontasa(ih):
            jelolt_versek.setdefault(v, ih)
    atfedes = defaultdict(list)
    for tabla, sorok in (("elofordulasok", elo), ("jeloltek", jel)):
        for s in sorok:
            for v in versek_kibontasa(s["igehely"]):
                if v in jelolt_versek:
                    atfedes[(s["id"], tabla)].append(
                        (s["igehely"], jelolt_versek[v],
                         s.get("dontes", ""), s.get("funkcio", "")))

    # --- kiírás ----------------------------------------------------------
    print("hívások: %d (+1 nem alkalmazható sor)" % len(F.hivasok))
    print("scan H8414: %d vers | scan H0922: %d | kollokáció: %d %s"
          % (len(tohu), len(bohu), len(par), par))
    print("kollokáció == napló 0.4:", set(par) == PAR)
    for s, v in mezo_koll.items():
        print("  mező %s: %d %s" % (s, len(v), v))
    for s, v in igealak.items():
        print("  igealak %s: %d vers %s" % (s, len(v), v))
    tip_n = defaultdict(int)
    for j in jelolt.values():
        tip_n[j["tipus"]] += 1
    print("jelöltek: %d %s" % (len(jelolt), dict(tip_n)))
    print("másodrendű (nem jelölt): %d" % len(masod_sorok))
    print("átfedés:")
    for (mid, tabla), l in sorted(atfedes.items()):
        print("  %s / %s: %d" % (mid, tabla, len(l)))
        for x in l:
            print("     %s  (jelölt: %s)  %s  %s" % x)
    print("karoli (lexikai):")
    for ih in lexikai:
        print("  %s | %s" % (ih, karoli_ki[ih]))

    if a.ir:
        def ir(nev, megj, fej, sorok):
            szoveg = "\n".join([megj, "\t".join(fej)]
                               + ["\t".join(s) for s in sorok]) + "\n"
            for s in sorok:
                for m in s:
                    assert "\t" not in m and "\n" not in m, m
            (NAPLOK / nev).write_bytes(szoveg.encode("utf-8"))
        ir("T1_TEREMT002_jeloltek_munkalap.tsv",
           "# T1.1 munkalap (TEREMT002_KUTATAS_BRIEF.md) -- adat/jeloltek.tsv "
           "alakjában, betöltés a T1.3-ban. Sema: adat/SEMA.md 2.4",
           ["id", "igehely", "forras_kereses", "dontes", "indoklas",
            "karoli_szo", "azonositas_modja", "megbizhatosag", "datum"],
           jel_sorok)
        ir("T1_TEREMT002_auditok_munkalap.tsv",
           "# T1.1 munkalap (TEREMT002_KUTATAS_BRIEF.md) -- adat/auditok.tsv "
           "alakjában, betöltés a T1.3-ban. Sema: adat/SEMA.md 2.9",
           ["id", "lepes", "proveniencia", "datum"], aud_sorok)
        ir("T1_TEREMT002_masodrendu_talalatok.tsv",
           "# T1.1: lekérdezés-találatok, amelyek NEM jelöltek (a nem-mag "
           "versek TSK/Károli-KH célpontjai, igealak, mező-kollokáció). "
           "Jelöltté léptetésük gate-kérdés (T1_TEREMT002_gate.md).",
           ["igehely", "forras_kereses"], masod_sorok)
        print("írva: naplok/T1_TEREMT002_{jeloltek,auditok}_munkalap.tsv, "
              "naplok/T1_TEREMT002_masodrendu_talalatok.tsv")


if __name__ == "__main__":
    main()
