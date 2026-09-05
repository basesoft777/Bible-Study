#!/usr/bin/env python3
"""
Pozicio-alapu frazis-keresesi szkript tobb-szavas heber/gorog formulakhoz.

PROBLEMA, AMIT MEGOLD: ha egy motivum tobb szobol allo, rogzult formula
(pl. "kara be-sem JHVH" -- "segitseget hivni az Ur neveben"), a puszta
Strong-szam grep hasznavehetetlen, mert az egyes szavak (pl. "hivni",
"nev") onmagukban tul gyakoriak -- szazasaval hoznak zajt, ami tobbnyire
mas jelentesu hasznalat (pl. "es nevezé nevét X-nek" nevadas-formula).

MODSZERTAN (3 lepes, mindegyik EMBERI ellenorzest igenyel a vegen):
1. Kalibracio: mekkora a tenyleges szo-tavolsag a MAR ISMERT, biztos
   talalatokban? (ne talalomra valasszunk ablakmeretet)
2. Szuk ablak: keresés a kalibralt tavolsagon belul, EXPLICIT
   isteni nev/cim kozvetlenul a kulcsszo utan.
3. Bovitett ablak + anafora-ellenorzes: a szuk ablak alatt/folott is
   nezzunk kortul (hamis-negativ teszt), es fogadjuk el a nevmasos
   (pl. "az o neve") formakat IS talalatnak, HA az isteni nev korabban
   mar szerepel ugyanabban a versben.

KRITIKUS FIGYELMEZTETES: a 3. lepes (anafora-bovites) hamis pozitivokat
IS hoz -- pl. "Isten neven szolitott" (mas szemelyt hiv neven, nem
onmagat) homonim szerkezetkent illeszkedik a mintara, de MAS jelentesu.
A "Segitsegul hivni az Urat" study 2026.09.05-i auditjanal 7 anaforikus
jelolt kozul csak 3 (Ezs 12:4, Zsolt 105:1, 1Kron 16:8) bizonyult
valodinak, 4 (Ezs 43:1, 44:5, 45:3, Ruth 4:11, 4:14) hamis pozitiv volt
("valakit neven szolitani/hirnevet szerezni" ertelemben, nem "Isten
nevet segitsegul hivni"). MINDEN JELOLTET TARTALMILAG ELLENORIZNI KELL,
a szkript kimenete SOHA nem hasznalhato automatikus beepitesre.

Futtatas: python eszkozok/frazis_kereses_pozicio_alapon.py
"""

import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
TAHOT_PATH = ROOT / "konkordancia" / "TAHOT_kivonat.tsv"


def load_verse_strongs(tsv_path):
    """Beolvassa a TAHOT/TAGNT kivonatot, versenkent sorrendben tarolt
    Strong-szam listakent (a fajl mar szo-sorrend szerint rendezett)."""
    verse_strongs = {}
    verse_order = []
    with open(tsv_path, encoding="utf-8", errors="replace") as f:
        next(f)  # fejlec sor kihagyasa
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            ref, strong = parts[0], parts[1]
            if ref not in verse_strongs:
                verse_strongs[ref] = []
                verse_order.append(ref)
            verse_strongs[ref].append(strong)
    return verse_strongs, verse_order


def calibrate_window(verse_strongs, known_true_refs, verb_strong, noun_strong):
    """1. lepes: megmeri a tavolsagot a mar ismert talalatokban."""
    distances = []
    for ref in known_true_refs:
        seq = verse_strongs.get(ref, [])
        if verb_strong in seq and noun_strong in seq:
            i = seq.index(verb_strong)
            j = seq.index(noun_strong)
            distances.append(j - i)
    return distances


def search_phrase(
    verse_strongs,
    verse_order,
    verb_strong,
    prep_strong,
    noun_strong,
    divine_strongs,
    window=4,
    check_anaphora=True,
):
    """2.+3. lepes: szuk ablakos + opcionalis anafora-bovitett kereses.

    Visszaad egy listat (igehely, cimke) parokkal, ahol a cimke
    'explicit-utana' vagy 'anaforikus-korabbi' -- ez utobbi MINDIG
    tartalmi ellenorzest igenyel felhasznalas elott.
    """
    results = []
    for ref in verse_order:
        seq = verse_strongs[ref]
        for i, s in enumerate(seq):
            if s != verb_strong:
                continue
            local_window = seq[i + 1 : i + 1 + window]
            if prep_strong not in local_window or noun_strong not in local_window:
                continue
            j = i + 1 + local_window.index(noun_strong)
            after = seq[j + 1 : j + 3]
            explicit_after = any(d in after for d in divine_strongs)
            explicit_before = any(d in seq[:i] for d in divine_strongs)
            if explicit_after:
                results.append((ref, "explicit-utana"))
            elif check_anaphora and explicit_before:
                results.append((ref, "anaforikus-korabbi"))
    return results


if __name__ == "__main__":
    verse_strongs, verse_order = load_verse_strongs(TAHOT_PATH)

    # Pelda: "kara be-shem JHVH" ("segitseget hivni az Ur neveben")
    known_true = [
        "1Móz 4:26", "1Móz 12:8", "1Móz 13:4", "1Móz 21:33", "1Móz 26:25",
        "1Kir 18:24", "1Kir 18:25", "1Kir 18:26", "2Kir 5:11",
        "Sof 3:9", "Jóel 2:32",
    ]
    distances = calibrate_window(verse_strongs, known_true, "H7121", "H8034")
    print("Kalibralt tavolsagok az ismert talalatokban:", distances)

    results = search_phrase(
        verse_strongs, verse_order,
        verb_strong="H7121", prep_strong="H9003", noun_strong="H8034",
        divine_strongs={"H3068", "H0430", "H0410", "H0136"},
        window=max(distances) if distances else 4,
    )
    for ref, tag in results:
        marker = " <- ISMERT" if ref in known_true else " *** UJ, ELLENORIZENDO ***"
        print(ref, tag, marker)
