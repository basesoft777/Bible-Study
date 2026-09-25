#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t1_3_teremt002_betoltes.py — TEREMT002_KUTATAS_BRIEF.md T1.3: a TEREMT-002
motívum-sora a `motivumok.tsv`-be (G2, a 2026.09.25-i gate-döntés mezőivel),
a T1.1 munkalapjainak sorai az `auditok.tsv`-be és a `jeloltek.tsv`-be
(mind `nyitva`, G4).

Csak hozzáfűz. Írás előtt ellenőrzi, hogy az eredeti fájl változatlanul
előtagja az újnak, hogy a TEREMT-002 még nincs a táblákban, és hogy a
munkalap fejléce egyezik a tábláéval; eltérésnél megáll.

Használat:
    python eszkozok/t1_3_teremt002_betoltes.py          # száraz futás
    python eszkozok/t1_3_teremt002_betoltes.py --ir
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
ADAT = ROOT / "adat"
NAPLOK = ROOT / "naplok"
ID = "TEREMT-002"

MOTIVUM = {
    "id": ID,
    "cim": "Tohu va-vohu (תֹהוּ וָבֹהוּ) — a föld kietlen és puszta állapota "
           "a teremtéskor és az ítéletkor",
    "ui_cimke": "Tohu va-vohu",
    "tema": "Teremtéstan + Hamartológia",
    "pardes_szint": "Remez",
    "statusz": "feldolgozás alatt",
    "statusz_verzio": "v1",
    "statusz_datum": "2026.09.25",
    "azonossag_tipusa": "formulaikus",
    "negativ_kriterium":
        "az igehelynek a תֹהוּ וָבֹהוּ (tohu va-vohu) szópárt kell tartalmaznia "
        "(H8414 + H0922 egy versben) — a תֹּהוּ (tohu) önmagában nem elég, sem a "
        "„semmiség/hiábavalóság” jelentésben (Ézs 40:17, 44:9), sem a „puszta, "
        "úttalan vidék” jelentésben (5Móz 32:10, Zsolt 107:40); és a lexikai pár "
        "nélküli kozmikus elsötétülés- vagy pusztulás-kép sem (Jóel 2:10, Mt 24:29)",
    "folerendelt_fogalom":
        "az isteni ítélet mint pusztulás / kozmikus felbomlás általában "
        "(prófétai pusztulás-, elsötétülés- és romhalmaz-képek), a תֹהוּ וָבֹהוּ "
        "(tohu va-vohu) páron kívül",
    "sablon_verzio": "",
    "forras_study": "",
}


def beolvas(path):
    """(nyers bájtok, megjegyzés-sorok, fejléc, adatsorok) — split('\\t')."""
    nyers = path.read_bytes()
    szoveg = nyers.decode("utf-8")
    if "\r" in szoveg:
        sys.exit("HIBA: CRLF a fájlban: %s" % path)
    sorok = [s for s in szoveg.split("\n") if s != ""]
    megj = [s for s in sorok if s.startswith("#")]
    tobbi = [s for s in sorok if not s.startswith("#")]
    return nyers, megj, tobbi[0].split("\t"), [s.split("\t") for s in tobbi[1:]]


def hozzafuz(path, uj_sorok, ir):
    nyers, _, fej, adat = beolvas(path)
    for s in adat:
        if s[0] == ID:
            sys.exit("HIBA: %s már szerepel: %s" % (ID, path.name))
    for s in uj_sorok:
        if len(s) != len(fej):
            sys.exit("HIBA: %s — %d mező a %d helyett: %r"
                     % (path.name, len(s), len(fej), s[:2]))
        for m in s:
            if "\t" in m or "\n" in m or "\r" in m:
                sys.exit("HIBA: tab/sortörés mezőben: %r" % m)
    if not nyers.endswith(b"\n"):
        sys.exit("HIBA: a fájl nem sorvéggel zárul: %s" % path)
    uj = nyers + ("\n".join("\t".join(s) for s in uj_sorok) + "\n").encode("utf-8")
    assert uj[:len(nyers)] == nyers
    # visszaolvasás: a régi sorok változatlanok, az újak a végén
    ellen = [s for s in uj.decode("utf-8").split("\n") if s and not s.startswith("#")]
    assert [x.split("\t") for x in ellen[1:len(adat) + 1]] == adat
    assert [x.split("\t") for x in ellen[len(adat) + 1:]] == uj_sorok
    print("%s: %d sor + %d új = %d" % (path.name, len(adat), len(uj_sorok),
                                       len(adat) + len(uj_sorok)))
    if ir:
        path.write_bytes(uj)
    return fej


def munkalap(nev, tabla):
    _, _, fej_m, sorok = beolvas(NAPLOK / nev)
    _, _, fej_t, _ = beolvas(ADAT / tabla)
    if fej_m != fej_t:
        sys.exit("HIBA: a munkalap fejléce eltér: %s" % nev)
    for s in sorok:
        if s[0] != ID:
            sys.exit("HIBA: idegen id a munkalapon: %r" % s[:2])
    return sorok


def main():
    ap = argparse.ArgumentParser(description="T1.3 — TEREMT-002 betöltés")
    ap.add_argument("--ir", action="store_true")
    a = ap.parse_args()

    _, _, fej, _ = beolvas(ADAT / "motivumok.tsv")
    if set(fej) != set(MOTIVUM):
        sys.exit("HIBA: motivumok.tsv fejléc eltér: %r" % fej)
    if len(MOTIVUM["ui_cimke"]) > 24:
        sys.exit("HIBA: ui_cimke > 24 karakter")

    aud = munkalap("T1_TEREMT002_auditok_munkalap.tsv", "auditok.tsv")
    jel = munkalap("T1_TEREMT002_jeloltek_munkalap.tsv", "jeloltek.tsv")
    if any(s[3] != "nyitva" for s in jel):
        sys.exit("HIBA: nem nyitva jelölt a munkalapon (G4)")
    kulcsok = [(s[0], s[1]) for s in jel]
    if len(set(kulcsok)) != len(kulcsok):
        sys.exit("HIBA: ismétlődő jelölt-kulcs")

    hozzafuz(ADAT / "motivumok.tsv", [[MOTIVUM[k] for k in fej]], a.ir)
    hozzafuz(ADAT / "auditok.tsv", aud, a.ir)
    hozzafuz(ADAT / "jeloltek.tsv", jel, a.ir)
    lep = {}
    for s in aud:
        lep[s[1]] = lep.get(s[1], 0) + 1
    print("auditok lepes szerint:", dict(sorted(lep.items())))
    print("ÍRVA" if a.ir else "száraz futás — nincs írás")


if __name__ == "__main__":
    main()
