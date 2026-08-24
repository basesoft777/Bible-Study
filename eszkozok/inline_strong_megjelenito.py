#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inline Strong-szám megjelenítő — a PaRDeS-projekt Károli-Strong join-táblájának
(konkordancia/Karoli_Strong_kivonat.tsv) egyszerű, olvasható megjelenítője.

CÉL
---
Egy megadott igehelyhez kiírja a konkordancia/Karoli_1908.tsv teljes Károli-versét,
és a konkordancia/Karoli_Strong_kivonat.tsv-ben már feldolgozott szavak UTÁN
beszúrja a Strong-számot szögletes zárójelben, pl.:

    Kezdetben[H7225] teremté[H1254] Isten[H430] az eget[H8064] és a föld.[H776]et.

Ahol egy szóhoz nincs feldolgozott Strong-adat a join-táblában, az a szó
JELÖLETLENÜL marad — ez nem hiba, csak azt jelzi, hogy azt a szót még nem
dolgozta fel egyetlen tanulmány sem (lásd a döntési fájl 4.12-es lefedettségi
táblázatát).

HASZNÁLAT
---------
    python eszkozok/inline_strong_megjelenito.py "Gen.1.1"
    python eszkozok/inline_strong_megjelenito.py "1Móz 1:1"

Az igehely megadható STEPBible-natív formátumban (pl. "Gen.1.1", ahogy a
konkordancia/TAHOT_kivonat.tsv és a Karoli_Strong_kivonat.tsv is tárolja) VAGY
a projekt magyar formátumában (pl. "1Móz 1:1", ahogy a Karoli_1908.tsv tárolja)
— a script automatikusan felismeri és konvertálja a Konyv_normalizalo_tabla.tsv
alapján.

Több igehely is megadható egyszerre (szóközzel elválasztva), vagy a --konyv és
--fejezet kapcsolókkal egy teljes fejezet is kiírható egyszerre.

FÜGGŐSÉGEK
----------
Csak a Python standard könyvtárát használja (nincs szükség pip install-ra).
A script relatív úton keresi a konkordancia/ mappát a repó gyökeréhez képest
— bárhonnan futtatható, amíg a repó szerkezete nem változik.

MÓDSZERTAN
----------
A Strong-szám mindig KÖZVETLENÜL a hozzá tartozó szó/kifejezés UTÁN kerül be,
a szó eredeti írásjeleit (vessző, pont) is beleértve, ha azok a szóhoz tapadva
szerepeltek a join-táblában. Ha egy versben több sor is van a join-táblában,
a beillesztés a versben elfoglalt POZÍCIÓ szerinti sorrendben, hátulról előre
történik, hogy egy korábbi beillesztés ne tolja el a későbbi keresések pozícióját.
"""

import sys
import os
import csv
import argparse
import io

# Windows konzol alapértelmezetten nem UTF-8-at használ — explicit átállítjuk,
# hogy az ékezetes magyar/héber szöveg helyesen jelenjen meg.
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
KONKORDANCIA = os.path.join(REPO_ROOT, 'konkordancia')


def load_tsv(filename):
    path = os.path.join(KONKORDANCIA, filename)
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        rows = [row for row in reader if row and len(row) == len(header)]
    return header, rows


def load_konyv_normalizalo():
    """STEPBible-rövidítés <-> Magyar rövidítés kétirányú megfeleltetés."""
    _, rows = load_tsv('Konyv_normalizalo_tabla.tsv')
    step_to_hu = {}
    hu_to_step = {}
    for step, hu, _full in rows:
        step_to_hu[step] = hu
        hu_to_step[hu] = step
    return step_to_hu, hu_to_step


def load_karoli_verses():
    """Magyar igehely (pl. '1Móz 1:1') -> teljes Károli-vers szövege."""
    _, rows = load_tsv('Karoli_1908.tsv')
    return {ref: text for ref, text in rows}


def load_join_table():
    """STEPBible-natív igehely -> [(Strong-szám, Károli-szó), ...] lista, sorrendben."""
    _, rows = load_tsv('Karoli_Strong_kivonat.tsv')
    by_verse = {}
    for row in rows:
        igehely, strong, karoli_szo = row[0], row[1], row[2]
        by_verse.setdefault(igehely, []).append((strong, karoli_szo))
    return by_verse


def to_step_ref(ref, hu_to_step):
    """'1Móz 1:1' -> 'Gen.1.1'; ha már STEPBible-natív ('Gen.1.1'), változatlanul hagyja."""
    if ' ' not in ref or ':' not in ref:
        return ref  # feltehetően már STEPBible-natív, pl. "Gen.1.1"
    hu_abbrev, cv = ref.rsplit(' ', 1)
    if hu_abbrev not in hu_to_step:
        return ref  # nem ismert magyar rövidítés — hagyjuk változatlanul, hibát a hívó jelzi
    ch, v = cv.split(':')
    return f"{hu_to_step[hu_abbrev]}.{ch}.{v}"


def to_hu_ref(step_ref, step_to_hu):
    """'Gen.1.1' -> '1Móz 1:1'."""
    parts = step_ref.split('.')
    if len(parts) != 3:
        return step_ref
    step_abbrev, ch, v = parts
    hu_abbrev = step_to_hu.get(step_abbrev)
    if not hu_abbrev:
        return step_ref
    return f"{hu_abbrev} {ch}:{v}"


def annotate_verse(verse_text, join_rows):
    """Beszúrja a Strong-számokat a Károli-vers szövegébe, pozíció szerint hátulról előre."""
    # Minden (strong, karoli_szo) párhoz megkeressük a szó pozícióját a versben.
    positioned = []
    for strong, karoli_szo in join_rows:
        idx = verse_text.find(karoli_szo)
        if idx == -1:
            # Nem található szó szerint a versben (elméletileg nem fordulhat elő,
            # mivel a join-tábla generálásakor ellenőriztük — de defenzíven kezeljük).
            print(f"  [figyelmeztetés: \"{karoli_szo}\" ({strong}) nem található szó szerint a vers szövegében, kihagyva]", file=sys.stderr)
            continue
        positioned.append((idx, karoli_szo, strong))

    # Hátulról előre szúrjuk be, hogy a korábbi pozíciók ne csússzanak el.
    positioned.sort(key=lambda x: x[0], reverse=True)
    result = verse_text
    for idx, karoli_szo, strong in positioned:
        insert_at = idx + len(karoli_szo)
        result = f"{result[:insert_at]}[{strong}]{result[insert_at:]}"
    return result


def show_verse(step_ref, karoli_verses, join_table, step_to_hu):
    hu_ref = to_hu_ref(step_ref, step_to_hu)
    verse_text = karoli_verses.get(hu_ref)
    if verse_text is None:
        print(f"HIBA: nincs Károli-szöveg ehhez az igehelyhez: {hu_ref} ({step_ref})", file=sys.stderr)
        return
    join_rows = join_table.get(step_ref, [])
    annotated = annotate_verse(verse_text, join_rows)
    print(f"{hu_ref} ({step_ref}):")
    print(f"  {annotated}")
    if not join_rows:
        print("  (ehhez a igeversz még nincs feldolgozott Strong-adat a join-táblában)")


def main():
    parser = argparse.ArgumentParser(
        description="Károli-vers megjelenítése inline Strong-számokkal a Karoli_Strong_kivonat.tsv alapján."
    )
    parser.add_argument('igehely', nargs='*', help='Igehely(ek), pl. "Gen.1.1" vagy "1Móz 1:1"')
    parser.add_argument('--konyv', help='Teljes fejezet kiírásához: STEPBible-rövidítés, pl. "Gen"')
    parser.add_argument('--fejezet', type=int, help='Teljes fejezet kiírásához: fejezetszám')
    args = parser.parse_args()

    step_to_hu, hu_to_step = load_konyv_normalizalo()
    karoli_verses = load_karoli_verses()
    join_table = load_join_table()

    if args.konyv and args.fejezet:
        prefix = f"{args.konyv}.{args.fejezet}."
        verses = sorted(
            (int(k.split('.')[2]) for k in join_table if k.startswith(prefix)),
        )
        # Ha a fejezetnek nincs join-tábla-sora, próbáljuk a Karoli_1908.tsv alapján kilistázni.
        if not verses:
            hu_abbrev = step_to_hu.get(args.konyv, args.konyv)
            verses = sorted(
                int(ref.rsplit(':', 1)[1])
                for ref in karoli_verses
                if ref.startswith(f"{hu_abbrev} {args.fejezet}:")
            )
        for v in verses:
            show_verse(f"{prefix}{v}", karoli_verses, join_table, step_to_hu)
        return

    if not args.igehely:
        parser.print_help()
        sys.exit(1)

    for ref in args.igehely:
        step_ref = to_step_ref(ref, hu_to_step)
        show_verse(step_ref, karoli_verses, join_table, step_to_hu)


if __name__ == '__main__':
    main()
