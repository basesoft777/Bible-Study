#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tahot_lefedettseg_ellenoriz.py — a TAHOT_kivonat.tsv lefedettségének tételes
felmérése könyvenként (ATALAKITASI_TERV.md.md F2 első lépése, 9. pont).

Nem generál semmilyen kanonikus fájlt; kimenete a MEGVALOSITAS_NAPLO.md-be
kerül dokumentálva. A könyvenkénti fejezetszám a kánoni maszoréta szöveg
közismert, közkincs adata (nem STEPBible-fájlból származik) — csak az
ellenőrzés vázához kell.
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
TAHOT = ROOT / "konkordancia" / "TAHOT_kivonat.tsv"

# Magyar rövidítés -> a könyv fejezeteinek száma (kánoni, közismert adat)
OT_FEJEZETSZAM = {
    "1Móz": 50, "2Móz": 40, "3Móz": 27, "4Móz": 36, "5Móz": 34,
    "Józs": 24, "Bír": 21, "Ruth": 4, "1Sám": 31, "2Sám": 24,
    "1Kir": 22, "2Kir": 25, "1Krón": 29, "2Krón": 36, "Ezsd": 10,
    "Neh": 13, "Eszt": 10, "Jób": 42, "Zsolt": 150, "Péld": 31,
    "Préd": 12, "Én": 8, "Ézs": 66, "Jer": 52, "Sir": 5,
    "Ez": 48, "Dán": 12, "Hós": 14, "Jóel": 3, "Ámós": 9,
    "Abd": 1, "Jón": 4, "Mik": 7, "Náh": 3, "Hab": 3,
    "Sof": 3, "Hag": 2, "Zak": 14, "Mal": 4,
}


def parse_igehely(s):
    book, rest = s.rsplit(" ", 1)
    ch, v = rest.split(":")
    return book, int(ch), int(v)


def main():
    rows = list(csv.DictReader(open(TAHOT, encoding="utf-8"), delimiter="\t"))
    present = defaultdict(set)  # book -> set(chapter)
    max_verse = defaultdict(dict)  # book -> {chapter: max verse}
    for r in rows:
        book, ch, v = parse_igehely(r["Igehely"])
        present[book].add(ch)
        max_verse[book][ch] = max(max_verse[book].get(ch, 0), v)

    print("# TAHOT_kivonat.tsv fejezet-szintű lefedettség (F2 első lépés)")
    total_missing_chapters = 0
    for book, nchap in OT_FEJEZETSZAM.items():
        expected = set(range(1, nchap + 1))
        have = present.get(book, set())
        missing = sorted(expected - have)
        if missing:
            total_missing_chapters += len(missing)
            print(f"HIÁNYZIK  {book}: fejezet(ek) {missing} (várt {nchap}, jelen {len(have)})")
    if total_missing_chapters == 0:
        print("Fejezet-szinten nincs hiány.")
    print(f"# összesen hiányzó fejezet: {total_missing_chapters}")


if __name__ == "__main__":
    main()
