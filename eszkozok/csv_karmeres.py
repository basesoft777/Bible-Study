#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
csv_karmeres.py — a konkordancia/*.tsv táblák csv.reader-kára a split('\t')-hez
képest (F4_BRIEF.md, Tétel C — a B tétel előfeltétele).

Minden konkordancia/*.tsv-re megméri, hány mezőn és hány soron tér el a
csv.reader kimenete a split('\t') kimenetétől, és mely oszlopokban. Ez a mérés
NEM ír vissza semmit a konkordancia/ alá — csak olvas, és a
naplok/F4_0_csv_karmeres.tsv-be ír riportot.

Futtatás a repó gyökeréből:
    python eszkozok/csv_karmeres.py
"""

import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KONK = ROOT / "konkordancia"
KIMENET = ROOT / "naplok" / "F4_0_csv_karmeres.tsv"


def split_rows(path):
    with open(path, encoding="utf-8") as f:
        return [ln.rstrip("\n").rstrip("\r").split("\t") for ln in f]


def csv_rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def merj(path):
    sraw = split_rows(path)
    craw = csv_rows(path)

    sorok = len(sraw)
    oszlopok = len(sraw[0]) if sraw else 0

    eltero_mezo = 0
    eltero_sorok = set()
    erintett_oszlopok = set()
    header = sraw[0] if sraw else []

    n = min(len(sraw), len(craw))
    for i in range(n):
        s_row, c_row = sraw[i], craw[i]
        m = min(len(s_row), len(c_row))
        for j in range(m):
            if s_row[j] != c_row[j]:
                eltero_mezo += 1
                eltero_sorok.add(i + 1)
                oszlopnev = header[j] if j < len(header) else f"oszlop_{j}"
                erintett_oszlopok.add(oszlopnev)
        if len(s_row) != len(c_row):
            eltero_sorok.add(i + 1)
            erintett_oszlopok.add("(sor-hossz-eltérés)")

    return {
        "fajl": path.name,
        "sorok": sorok,
        "oszlopok": oszlopok,
        "eltero_mezo": eltero_mezo,
        "eltero_sor": len(eltero_sorok),
        "erintett_oszlopok": ";".join(sorted(erintett_oszlopok)) if erintett_oszlopok else "(nincs eltérés)",
    }


def main():
    fajlok = sorted(KONK.glob("*.tsv"))
    print(f"{len(fajlok)} konkordancia/*.tsv fájl mérése...", file=sys.stderr)

    eredmenyek = []
    for path in fajlok:
        try:
            eredmenyek.append(merj(path))
        except Exception as e:
            print(f"HIBA {path.name}: {e}", file=sys.stderr)
            eredmenyek.append({
                "fajl": path.name, "sorok": "?", "oszlopok": "?",
                "eltero_mezo": "?", "eltero_sor": "?",
                "erintett_oszlopok": f"MÉRÉSI HIBA: {e}",
            })

    fejlec = ["fajl", "sorok", "oszlopok", "eltero_mezo", "eltero_sor", "erintett_oszlopok"]
    sorok_ki = ["\t".join(fejlec)]
    for r in eredmenyek:
        sorok_ki.append("\t".join(str(r[k]) for k in fejlec))

    KIMENET.parent.mkdir(parents=True, exist_ok=True)
    with open(KIMENET, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sorok_ki) + "\n")

    osszes_eltero_mezo = sum(r["eltero_mezo"] for r in eredmenyek if isinstance(r["eltero_mezo"], int))
    erintett_fajlok = sum(1 for r in eredmenyek if isinstance(r["eltero_mezo"], int) and r["eltero_mezo"] > 0)
    print(f"Kész: {len(eredmenyek)} fájl mérve, {erintett_fajlok} fájlon van eltérés, "
          f"összesen {osszes_eltero_mezo} eltérő mező.", file=sys.stderr)
    print(f"Riport: {KIMENET}", file=sys.stderr)


if __name__ == "__main__":
    main()
