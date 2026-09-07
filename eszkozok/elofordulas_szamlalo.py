#!/usr/bin/env python3
"""
Elofordulas-szamlalo szkript Strong-szamokhoz.

Egy Strong-szamot kapva parancssori argumentumkent megszamolja az
elofordulasait a konkordancia/TAGNT_kivonat.tsv-ben (G-szamu) vagy a
konkordancia/TAHOT_kivonat.tsv-ben (H-szamu).

A Mounce (MCGED) lexikon copyright vedett, ezert nem kerult feldolgozasra;
ez a szkript a funkciojat potolja: a mar meglevo TAGNT/TAHOT-kivonatokbol
szamolja ki, hany helyen fordul elo egy adott Strong-szam.

Hasznalat: python3 eszkozok/elofordulas_szamlalo.py G1941
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAGNT_PATH = ROOT / "konkordancia" / "TAGNT_kivonat.tsv"
TAHOT_PATH = ROOT / "konkordancia" / "TAHOT_kivonat.tsv"


def count_occurrences(tsv_path, strong):
    count = 0
    with open(tsv_path, encoding="utf-8", errors="replace") as f:
        next(f)  # fejlec sor kihagyasa
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            if parts[1] == strong:
                count += 1
    return count


def main():
    if len(sys.argv) != 2:
        print("Hasznalat: python3 eszkozok/elofordulas_szamlalo.py <Strong-szam>")
        sys.exit(1)

    strong = sys.argv[1].strip().upper()
    if strong.startswith("G"):
        tsv_path, tsv_name = TAGNT_PATH, "TAGNT_kivonat.tsv"
    elif strong.startswith("H"):
        tsv_path, tsv_name = TAHOT_PATH, "TAHOT_kivonat.tsv"
    else:
        print(f"Ismeretlen Strong-szam elotag: {strong} (G vagy H kezdetu lehet)")
        sys.exit(1)

    count = count_occurrences(tsv_path, strong)
    print(f"{strong}: {count} elofordulas a {tsv_name}-ben")


if __name__ == "__main__":
    main()
