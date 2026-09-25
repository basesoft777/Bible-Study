#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t2_3_teremt002_forrasreteg.py — TEREMT002_KUTATAS_BRIEF.md T2.3 (G6): a napló
(`motivumlog/PaRDeS_motivumok.md`) három kézi TEREMT-002-szövegének átemelése
a forrásrétegbe (`motivumok/TEREMT-002.md`), karakterre azonosan — az N14.3
(HAMART-001) mintája.

A három szöveg: a Tematikus áttekintés kézi tétele (archív), a ⭐ küszöb-
bekezdés (beolvasztható, BEOLVASZTHATO_SZAKASZOK) és a kézi kulcsszó-index
sora (archív). A naplóból kikerülnek; a helyüket a `general.py --cel naplo`
generált blokkjai veszik át. Más napló-sor nem változik (a HAMART-001 „Lásd
még” bejegyzése, amely a TEREMT-002-re hivatkozik, marad).

Használat:
    python eszkozok/t2_3_teremt002_forrasreteg.py          # száraz futás
    python eszkozok/t2_3_teremt002_forrasreteg.py --ir
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
NAPLO = ROOT / "motivumlog" / "PaRDeS_motivumok.md"
CEL = ROOT / "motivumok" / "TEREMT-002.md"
ID = "TEREMT-002"

# (kezdőszöveg, a sort követő üres sor is kikerül-e)
KERES = {
    "attekintes": ("- תהו/בהו — teremtés-visszavonás mint ítélet-nyelvezet (3 előfordulás", False),
    "kuszob": ("**\"תהו/בהו — teremtés-visszavonás mint ítélet-nyelvezet\"** `[ID: TEREMT-002]`", True),
    "kulcsszo": ("| **תהו/בהו — teremtés-visszavonás mint ítélet-nyelvezet** ⭐ `[ID: TEREMT-002]`", False),
}

FEJ = [
    "# Tohu va-vohu (תֹהוּ וָבֹהוּ) — a föld kietlen és puszta állapota a teremtéskor és az ítéletkor — forrásréteg `[ID: TEREMT-002]`",
    "",
    "<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. NEM generált fájl. -->",
    "",
    "*Proveniencia: az alábbi szövegblokkok a `motivumlog/PaRDeS_motivumok.md`-ből lettek "
    "átemelve, **karakterre azonosan**, 2026-09-25-én (TEREMT002_KUTATAS_BRIEF.md T2.3 / G6; "
    "az N14.3 mintája). A naplóban a helyükön a `general.py` generált marker-blokkjai állnak. "
    "A TEREMT-002 natív egyforrású motívum (G1): tematikus tanulmány nem tartozik hozzá, a "
    "próza a T3-ban ide kerül. Ami a tábláról levezethető (`adat/motivumok.tsv`, "
    "`adat/elofordulasok.tsv`), az nem ide tartozik.*",
    "",
]
SZAKASZ = {
    "attekintes": "## Tematikus áttekintés — a napló mai tétele *(archív — a 2026-09-25-i "
                  "kivonás előtti szöveg; a mérvadó érték a generált blokkban áll)*",
    "kuszob": "## ⭐ Emlékeztető küszöb — a napló mai bekezdése",
    "kulcsszo": "## Kulcsszó-index — a napló mai sora *(archív — a 2026-09-25-i kivonás "
                "előtti szöveg; a mérvadó érték a generált blokkban áll)*",
}


def main():
    ap = argparse.ArgumentParser(description="T2.3 — TEREMT-002 forrásréteg")
    ap.add_argument("--ir", action="store_true")
    a = ap.parse_args()

    if CEL.exists():
        sys.exit("HIBA: %s már létezik" % CEL)
    regi = NAPLO.read_bytes().decode("utf-8")
    if "\r" in regi:
        sys.exit("HIBA: CRLF a naplóban")
    sorok = regi.split("\n")

    talalt, torol = {}, set()
    for kulcs, (eleje, uressel) in KERES.items():
        idx = [i for i, s in enumerate(sorok) if s.startswith(eleje)]
        if len(idx) != 1:
            sys.exit("HIBA: %s: %d találat" % (kulcs, len(idx)))
        i = idx[0]
        talalt[kulcs] = sorok[i]
        torol.add(i)
        if uressel:
            if sorok[i + 1] != "":
                sys.exit("HIBA: %s után nem üres sor" % kulcs)
            torol.add(i + 1)

    uj_naplo = [s for i, s in enumerate(sorok) if i not in torol]
    # a naplóban más TEREMT-002-említés csak a HAMART-001 „Lásd még”-je lehet
    maradt = [s for s in uj_naplo if ID in s or "teremtés-visszavonás" in s]
    if len(maradt) != 1 or not maradt[0].startswith("- **Lásd még:**"):
        sys.exit("HIBA: váratlan maradék TEREMT-002-említés: %d" % len(maradt))

    ki = list(FEJ)
    for kulcs in ("attekintes", "kuszob", "kulcsszo"):
        ki += [SZAKASZ[kulcs], "", talalt[kulcs], ""]
    forras = "\n".join(ki)

    # karakterre azonosság: minden átemelt sor szó szerint a forrásrétegben
    for kulcs, s in talalt.items():
        assert ("\n" + s + "\n") in forras, kulcs
    assert len(uj_naplo) == len(sorok) - len(torol)

    print("átemelve: %d szöveg, a naplóból %d sor kikerül (%s)" % (
        len(talalt), len(torol), ", ".join(str(i + 1) for i in sorted(torol))))
    for k, s in talalt.items():
        print("  %-10s %d karakter" % (k, len(s)))
    if a.ir:
        CEL.write_bytes(forras.encode("utf-8"))
        NAPLO.write_bytes("\n".join(uj_naplo).encode("utf-8"))
        print("ÍRVA: %s, %s" % (CEL.relative_to(ROOT), NAPLO.relative_to(ROOT)))
    else:
        print("száraz futás — nincs írás")


if __name__ == "__main__":
    main()
