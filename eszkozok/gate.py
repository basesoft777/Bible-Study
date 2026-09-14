#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — a 4.6 motívum-gate ütközés- és részhalmaz-jelentése
(ATALAKITASI_TERV.md.md 4.6, 2. pont; F3.3 sor).

A `motivumok.tsv` + `elofordulasok.tsv` alapján, motívumpáronként:

  1. ÜTKÖZÉS — mely igehelyek szerepelnek egynél több motívum
     `elofordulasok` táblájában (osztozó igehelyek), és mekkora az átfedés.
  2. RÉSZHALMAZ — ha B minden előfordulása benne van A-ban (B ⊆ A),
     az a 4.6 gate 4. kérdése szerint azt jelzi, hogy B talán nem önálló
     ID, hanem A egy ↳ alpontja.

Ez a szkript KIMENETET ad, NEM DÖNTÉST — a talált ütközések és
részhalmaz-gyanús párok emberi (kutató/ember) mérlegelést igényelnek a
4.6 gate négy kérdése szerint (elsősorban a 3. kérdés: különbözik-e a
funkció). A jelentés önmagában nem zár ki és nem old fel semmit.

Használat:
    python eszkozok/gate.py                    # teljes jelentés, stdout
    python eszkozok/gate.py --md kimenet.md     # jelentés Markdown fájlba is
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import csv
import datetime
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADAT = ROOT / "adat"


def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M") + "Z"


def read_tsv_skip_comments(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))


def load_data():
    motivumok = read_tsv_skip_comments(ADAT / "motivumok.tsv")
    elofordulasok = read_tsv_skip_comments(ADAT / "elofordulasok.tsv")
    igehelyek = defaultdict(set)
    for row in elofordulasok:
        igehelyek[row["id"]].add(row["igehely"])
    return motivumok, igehelyek


def cim(motivumok, id_):
    for m in motivumok:
        if m["id"] == id_:
            return m["cim"]
    return "(nincs motivumok.tsv sor)"


def collision_report(igehelyek):
    """igehely -> [id, id, ...] ahol tobb mint egy motivum osztozik rajta."""
    by_verse = defaultdict(list)
    for id_, verses in igehelyek.items():
        for v in verses:
            by_verse[v].append(id_)
    shared = {v: ids for v, ids in by_verse.items() if len(ids) > 1}
    return shared


def pair_overlap_report(igehelyek):
    ids = sorted(igehelyek)
    rows = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            common = igehelyek[a] & igehelyek[b]
            if common:
                rows.append((a, b, sorted(common), len(common)))
    return rows


def subset_report(igehelyek):
    """B ⊆ A, B != A, mindketto nem-ures."""
    ids = sorted(igehelyek)
    rows = []
    for a in ids:
        for b in ids:
            if a == b:
                continue
            va, vb = igehelyek[a], igehelyek[b]
            if not vb or not va:
                continue
            if vb.issubset(va) and vb != va:
                rows.append((b, a, sorted(vb)))
    return rows


def render(motivumok, igehelyek, shared, pair_overlap, subset):
    lines = []
    lines.append("# gate.py — ütközés- és részhalmaz-jelentés")
    lines.append("")
    lines.append("Generálva: `eszkozok/gate.py`, ts=%s" % ts())
    lines.append("")
    ids = sorted(igehelyek)
    lines.append(
        "Vizsgált motívumok (%d db, az `adat/motivumok.tsv`-ben és az "
        "`adat/elofordulasok.tsv`-ben egyaránt jelen lévők): %s"
        % (len(ids), ", ".join(ids))
    )
    lines.append("")
    lines.append("**Ez a fájl kimenet, nem döntés** — minden ütközés/részhalmaz-gyanú "
                  "a 4.6 gate négy kérdése szerint emberi mérlegelést igényel "
                  "(l. `ATALAKITASI_TERV.md.md` 4.6).")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 1. Ütközés-jelentés — motívumpáronként osztozó igehelyek")
    lines.append("")
    if not pair_overlap:
        lines.append("Nincs osztozó igehely egyetlen motívumpár között sem.")
    else:
        lines.append("| A | B | osztozó igehelyek (n) | igehelyek |")
        lines.append("|---|---|---|---|")
        for a, b, common, n in sorted(pair_overlap, key=lambda r: -r[3]):
            lines.append(
                "| %s (%s) | %s (%s) | %d | %s |"
                % (a, cim(motivumok, a), b, cim(motivumok, b), n, "; ".join(common))
            )
    lines.append("")

    lines.append("## 2. Egy igehelyen osztozó motívumok — vers-központú nézet")
    lines.append("")
    if not shared:
        lines.append("Nincs olyan igehely, amely egynél több motívum táblájában szerepelne.")
    else:
        lines.append("| Igehely | Motívumok |")
        lines.append("|---|---|")
        for v in sorted(shared):
            lines.append("| %s | %s |" % (v, ", ".join(sorted(shared[v]))))
    lines.append("")

    lines.append("## 3. Részhalmaz-ellenőrzés — B ⊆ A (B minden igehelye A-ban is megvan)")
    lines.append("")
    lines.append(
        "A 4.6 gate 4. kérdése: *ha B minden előfordulása benne van A-ban, "
        "B nem új ID, hanem A alpontja.* Az alábbi sorok jelzések, nem döntések — "
        "egy egyetlen közös igehely (n=1) önmagában nem indokolja az alpont-besorolást, "
        "csak akkor releváns, ha B teljes (nem csak egy-két elemű) halmaza esik A-ba."
    )
    lines.append("")
    if not subset:
        lines.append("Nincs B ⊆ A viszony egyetlen motívumpár között sem.")
    else:
        lines.append("| B (kisebbik) | ⊆ A (nagyobbik) | B mérete | B igehelyei |")
        lines.append("|---|---|---|---|")
        for b, a, verses in sorted(subset, key=lambda r: len(r[2])):
            lines.append(
                "| %s (%s) | %s (%s) | %d | %s |"
                % (b, cim(motivumok, b), a, cim(motivumok, a), len(verses), "; ".join(verses))
            )
    lines.append("")

    lines.append("## 4. Hatókör — mely ID-k maradtak ki")
    lines.append("")
    all_known = {m["id"] for m in motivumok}
    loaded = set(igehelyek)
    missing = sorted(all_known - loaded)
    if missing:
        lines.append(
            "A `motivumok.tsv`-ben szereplő, de `elofordulasok.tsv`-ben előfordulás "
            "nélküli ID-k (üres motívum, vagy még nincs betöltve): %s" % ", ".join(missing)
        )
    else:
        lines.append("Minden `motivumok.tsv`-beli ID-hez van legalább egy `elofordulasok` sor.")
    lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--md", help="a jelentés mentése ebbe a Markdown fájlba is")
    args = ap.parse_args()

    motivumok, igehelyek = load_data()
    shared = collision_report(igehelyek)
    pair_overlap = pair_overlap_report(igehelyek)
    subset = subset_report(igehelyek)

    report = render(motivumok, igehelyek, shared, pair_overlap, subset)
    print(report)

    if args.md:
        Path(args.md).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
