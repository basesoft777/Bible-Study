#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2. lepes: a vegleges TAHOT_kivonat.tsv (Karoli-nativ Igehely mezovel) es a
TAHOT_kivonat_nyitott_esetek.tsv legenerálása.

Bemenetek:
  - a MEGLEVO konkordancia/TAHOT_kivonat.tsv (435 723 sor, STEPBible-kulcsos) -
    ezek tartalma valtozatlan marad, csak az Igehely mezo alakul at
    STEPBible-formatumbol ("Gen.1.1") Karoli-formatumba ("1Móz 1:1").
  - phaseA_all.tsv - az OSSZES nyers sorbol (parennel egyutt) generalt kivonat,
    ebbol csak a secondary!='' (azaz korabban eldobott) sorokat hasznaljuk fel.
  - step1_decisions.tsv - a fejezet-szintu dontesek (ELSODLEGES/MASODLAGOS/...),
    3 kezi felulbiralassal (lasd DONTES_FELULBIRALAS lent).
"""
import re, csv, os, sys
from collections import defaultdict

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\Users\bases\Desktop\Bible-Study"
OLD_TAHOT = REPO + r"\konkordancia\TAHOT_kivonat.tsv"
NORM_PATH = REPO + r"\konkordancia\Konyv_normalizalo_tabla.tsv"
KAROLI_PATH = REPO + r"\konkordancia\Karoli_1908.tsv"
PHASEA_PATH = SCRATCH + "/phaseA_all.tsv"
DECISIONS_PATH = SCRATCH + "/step1_decisions.tsv"

OUT_MAIN = REPO + r"\konkordancia\TAHOT_kivonat.tsv"
OUT_OPEN = REPO + r"\konkordancia\TAHOT_kivonat_nyitott_esetek.tsv"

# ---- kezi felulbiralasok a step1 automatikus dontesein ----
# (konyv, tuple(erintett primary fejezetek)) -> ('DONTES', megjegyzes)
DONTES_FELULBIRALAS = {
    ("Ezk", (20, 21)): ("ADATMINOSEGI_GYANU",
        "Ez 20:44 a Karoli 1908-ban osszeolvadt/tulhosszu vers: a heber "
        "21:1-5 (\"erdotuz\" oraculum) szovege belefolyt a 20:44 vegebe, "
        "majd a 21:1 csak az oraculum elso mondatat ismetli, mielott athalna "
        "a valodi (Jeruzsalem elleni) 21:2 oraculumra. A tiszta numerikus "
        "fejezethossz-egyezes (masodlagos/heber: 20=44, 21=37) felszinesen "
        "stimmelne, de tartalmilag nem megbizhato -> ADATMINOSEGI_GYANU, "
        "korabbi audit (Karoli_adatminosegi_anomaliak.tsv, Ez 20:44) altal "
        "mar dokumentalt jelenseg."),
    ("Job", (40, 41)): ("ADATMINOSEGI_GYANU",
        "Sem az elsodleges (angol/NRSV), sem a masodlagos (heber) fejezethossz "
        "nem egyezik a Karoli tenyleges 40. (28v) es 41. (25v) fejezet-hosszaval "
        "(elsodleges: 24/34; masodlagos: 32/26) - korabbi audit szerint Jób 41:25 "
        "is osszeolvadt/gyanus vers -> ADATMINOSEGI_GYANU."),
    ("1Sa", (20, 21)): ("ELSODLEGES",
        "Tartalmilag ellenorizve: Károli 1Sám 20:43 (\"Felkele ezután és "
        "elméne. Jonathán pedig bement a városba.\") pontosan a heber 21:1 "
        "szovegenek felel meg, de Karoli ONALLO 43. versként adja hozza az "
        "elsodleges (angol) 20. fejezethez, nem tolja at a 21. fejezetbe. "
        "Ezert a fejezetszamozas elsodleges (nincs hatareltolodas: 20 es 21 "
        "sajat maga marad), DE az erintett szo-sorok (1Sa.20.42(21.1)) kulon "
        "kezelendok: Igehely = '1Sám 20:43' (lasd KULON_SOR_KIVETEL)."),
}

# egyedi sor-szintu kivetel: (primary_ref, secondary_ref) -> kesz Karoli kulcs
KULON_SOR_KIVETEL = {
    ("1Sa.20.42", "1Sa.21.1"): "1Sám 20:43",
}


def load_norm():
    m = {}
    with open(NORM_PATH, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            step, hu, full = row
            m[step] = hu
    return m


def load_karoli_valid_refs():
    s = set()
    with open(KAROLI_PATH, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            if row:
                s.add(row[0])
    return s


def load_decisions():
    """(konyv, fejezet) -> dontes string, tovabba csoport-info a felulbiralashoz."""
    chap_decision = {}
    with open(DECISIONS_PATH, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            book, hu, chapters_s, decision = row[0], row[1], row[2], row[3]
            chapters = tuple(int(x) for x in chapters_s.split(','))
            key = (book, chapters)
            if key in DONTES_FELULBIRALAS:
                decision = DONTES_FELULBIRALAS[key][0]
            elif decision == "TARTALMI_ELLENORZES_SZUKSEGES(mindketto_egyezik)":
                # a fejezethossz mindket hipotezis alatt egyezik (tipikusan zsoltarcim,
                # ami egybeolvad az 1. verssel) - a per-sor alapertelmezett szabaly
                # (masodlagos, ha van zarojel, kulonben elsodleges) helyesen mukodik,
                # lasd a dontesi naplo/README erveleset.
                decision = "MASODLAGOS"
            for c in chapters:
                chap_decision[(book, c)] = decision
    return chap_decision


REF_RE = re.compile(r'^([A-Za-z0-9]+)\.(\d+)\.(\d+)$')


def to_karoli_ref(norm, book, chap, verse):
    hu = norm.get(book)
    if hu is None:
        return None
    return f"{hu} {chap}:{verse}"


def main():
    norm = load_norm()
    valid_karoli = load_karoli_valid_refs()
    chap_decision = load_decisions()

    main_rows = []  # (karoli_ref, strong, hebrew, translit, root, gloss, english)
    open_rows = []  # (raw_primary, raw_secondary, statusz, indoklas, strong, hebrew, translit, root, gloss, english)

    # --- 1) meglevo TAHOT_kivonat.tsv sorok: csak az Igehely mezo konvertalasa ---
    n_old = 0
    n_old_bad = 0
    with open(OLD_TAHOT, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        header = next(r)
        for row in r:
            if len(row) != 7:
                continue
            ref, strong, heb, translit, root, gloss, english = row
            m = REF_RE.match(ref)
            if not m:
                n_old_bad += 1
                continue
            book, chap, verse = m.group(1), int(m.group(2)), int(m.group(3))
            karoli_ref = to_karoli_ref(norm, book, chap, verse)
            if karoli_ref is None:
                n_old_bad += 1
                continue
            main_rows.append((karoli_ref, strong, heb, translit, root, gloss, english))
            n_old += 1
    print(f"Regi sorok atvéve: {n_old} (hiba: {n_old_bad})", file=sys.stderr)

    # --- 2) korabban eldobott (zarojeles) sorok phaseA_all.tsv-bol ---
    n_new_main = 0
    n_new_open = 0
    with open(PHASEA_PATH, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            primary, secondary, strong, heb, translit, root, gloss, english = row
            if not secondary:
                continue  # ezeket mar az 1) lepes lefedte

            # egyedi sor-szintu kivetel eloszor
            if (primary, secondary) in KULON_SOR_KIVETEL:
                karoli_ref = KULON_SOR_KIVETEL[(primary, secondary)]
                main_rows.append((karoli_ref, strong, heb, translit, root, gloss, english))
                n_new_main += 1
                continue

            pm = REF_RE.match(primary)
            sm = REF_RE.match(secondary)
            if not pm or not sm:
                open_rows.append((primary, secondary, "NYITOTT", "hivatkozas-format hiba",
                                   strong, heb, translit, root, gloss, english))
                n_new_open += 1
                continue
            pbook, pchap, pverse = pm.group(1), int(pm.group(2)), int(pm.group(3))
            sbook, schap, sverse = sm.group(1), int(sm.group(2)), int(sm.group(3))

            decision = chap_decision.get((pbook, pchap))
            if decision is None:
                # nincs dontes-csoportban - ne forduljon elo, de biztonsag kedveert NYITOTT
                open_rows.append((primary, secondary, "NYITOTT", "nincs dontesi csoport",
                                   strong, heb, translit, root, gloss, english))
                n_new_open += 1
                continue

            if decision == "ADATMINOSEGI_GYANU":
                open_rows.append((primary, secondary, "ADATMINOSEGI_GYANU",
                                   f"lasd DONTES_FELULBIRALAS a generalo szkriptben ({pbook} fejezet {pchap})",
                                   strong, heb, translit, root, gloss, english))
                n_new_open += 1
                continue
            elif decision == "ELSODLEGES":
                karoli_ref = to_karoli_ref(norm, pbook, pchap, pverse)
            elif decision == "MASODLAGOS":
                karoli_ref = to_karoli_ref(norm, sbook, schap, sverse)
            else:
                open_rows.append((primary, secondary, "NYITOTT", f"ismeretlen dontes: {decision}",
                                   strong, heb, translit, root, gloss, english))
                n_new_open += 1
                continue

            if karoli_ref is None or karoli_ref not in valid_karoli:
                open_rows.append((primary, secondary, "NYITOTT",
                                   f"a generalt Karoli-kulcs ('{karoli_ref}') nem letezik a Karoli_1908.tsv-ben",
                                   strong, heb, translit, root, gloss, english))
                n_new_open += 1
                continue

            main_rows.append((karoli_ref, strong, heb, translit, root, gloss, english))
            n_new_main += 1

    print(f"Uj sorok a fokivonatba: {n_new_main}  nyitott/gyanus sorok: {n_new_open}", file=sys.stderr)

    # --- vegso kereszt-ellenorzes: minden fokivonat-kulcs letezik-e a Karoliban ---
    n_mismatch = 0
    for row in main_rows:
        if row[0] not in valid_karoli:
            n_mismatch += 1
    print(f"Kereszt-ellenorzes: {n_mismatch} olyan sor, aminek Karoli-kulcsa NEM letezik "
          f"a Karoli_1908.tsv-ben (elvart: 0)", file=sys.stderr)

    # --- kiiras ---
    with open(OUT_MAIN, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['Igehely', 'Strong-szám', 'Ragozott alak', 'Kiejtés', 'Szótő',
                    'Rövid jelentés', 'Angol tükörfordítás'])
        for row in main_rows:
            w.writerow(row)

    with open(OUT_OPEN, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['STEPBible_elsodleges', 'STEPBible_masodlagos', 'Státusz', 'Indoklás',
                    'Strong-szám', 'Ragozott alak', 'Kiejtés', 'Szótő',
                    'Rövid jelentés', 'Angol tükörfordítás'])
        for row in open_rows:
            w.writerow(row)

    print(f"Vegso fokivonat sorszam: {len(main_rows)}", file=sys.stderr)
    print(f"Nyitott esetek sorszam: {len(open_rows)}", file=sys.stderr)


if __name__ == '__main__':
    main()
