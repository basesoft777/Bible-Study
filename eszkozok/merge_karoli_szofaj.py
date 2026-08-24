#!/usr/bin/env python3
"""Egyszeri script: Karoli_Strong_kivonat.tsv bovitese Szofaj + Gyok/Szarmaztatas oszlopokkal, Strong_szotar.tsv alapjan."""
import csv
import re

SZOTAR_PATH = "konkordancia/Strong_szotar.tsv"
KIVONAT_PATH = "konkordancia/Karoli_Strong_kivonat.tsv"


def normalize(strong):
    """H430 -> H0430, H7225 -> H7225, G26 -> G0026 (4 szamjegyre padolva)."""
    m = re.match(r"^([HG])(\d+)([A-Za-z]*)$", strong)
    if not m:
        return strong
    letter, digits, suffix = m.groups()
    return f"{letter}{int(digits):04d}{suffix}"

lookup = {}
with open(SZOTAR_PATH, encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    header = next(reader)
    for row in reader:
        if not row:
            continue
        strong = row[0]
        szofaj = row[3] if len(row) > 3 else ""
        gyok = row[4] if len(row) > 4 else ""
        lookup[strong] = (szofaj, gyok)

with open(KIVONAT_PATH, encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    rows = list(reader)

out_rows = [rows[0] + ["Szófaj", "Gyök/Származtatás"]]
for row in rows[1:]:
    if not row:
        continue
    strong = row[1]
    szofaj, gyok = lookup.get(normalize(strong), ("", ""))
    out_rows.append(row + [szofaj, gyok])

with open(KIVONAT_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t", lineterminator="\n")
    writer.writerows(out_rows)

print(f"Sorok: {len(out_rows)-1}, ebbol Strong_szotar-adattal ellatva: {sum(1 for r in out_rows[1:] if r[6])}")
