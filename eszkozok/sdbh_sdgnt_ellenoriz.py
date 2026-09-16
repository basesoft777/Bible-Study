"""SDBH/SDGNT import — ellenőrző szkript.

Csak a repó fájljait olvassa (split('\\t')), és kritériumonként OK/HIBA
sort ír. Lásd SDBH_IMPORT_BRIEF.md §3.1.b, §1.4.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import hashlib
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONK = os.path.join(REPO_ROOT, "konkordancia")
EM_DASH = "—"

FAILURES = 0


def ok(label, condition, detail=""):
    global FAILURES
    status = "OK" if condition else "HIBA"
    if not condition:
        FAILURES += 1
    suffix = f" — {detail}" if detail else ""
    print(f"{status}: {label}{suffix}")
    return condition


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        content = f.read()
    lines = content.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    data_lines = [l for l in lines if not l.startswith("#")]
    header = data_lines[0].split("\t")
    rows = [l.split("\t") for l in data_lines[1:]]
    return header, rows


def sha256_no_comments(path):
    with open(path, "rb") as f:
        content = f.read()
    lines = content.split(b"\n")
    lines = [l for l in lines if not l.startswith(b"#")]
    joined = b"\n".join(lines)
    return hashlib.sha256(joined).hexdigest()


def main():
    sdbh_path = os.path.join(KONK, "SDBH_domenek.tsv")
    sdgnt_path = os.path.join(KONK, "SDGNT_domenek.tsv")
    domenfa_path = os.path.join(KONK, "SDBH_SDGNT_domenfa.tsv")
    anom_path = os.path.join(KONK, "SDBH_SDGNT_anomaliak.tsv")

    sdbh_h, sdbh_rows = read_tsv(sdbh_path)
    sdgnt_h, sdgnt_rows = read_tsv(sdgnt_path)
    domenfa_h, domenfa_rows = read_tsv(domenfa_path)
    anom_h, anom_rows = read_tsv(anom_path)

    # --- mezőszám ellenőrzés ---
    for name, header, rows in (
        ("SDBH_domenek.tsv", sdbh_h, sdbh_rows),
        ("SDGNT_domenek.tsv", sdgnt_h, sdgnt_rows),
        ("SDBH_SDGNT_domenfa.tsv", domenfa_h, domenfa_rows),
        ("SDBH_SDGNT_anomaliak.tsv", anom_h, anom_rows),
    ):
        bad = [i for i, r in enumerate(rows) if len(r) != len(header)]
        ok(f"{name}: minden sor mezőszáma a fejléccel egyezik", not bad,
           f"{len(bad)} eltérő sor" if bad else "")

    # --- §1.4 SDBH táblázat ---
    ok("SDBH adatsor = 22280", len(sdbh_rows) == 22280, str(len(sdbh_rows)))
    ok("SDBH kul strong = 8557", len({r[0] for r in sdbh_rows}) == 8557)
    ok("SDBH kul strong_kod = 8935", len({r[1] for r in sdbh_rows}) == 8935)
    ok("SDBH kul entry_id = 7862", len({r[5] for r in sdbh_rows}) == 7862)
    ok("SDBH kul lexid = 16219", len({r[7] for r in sdbh_rows}) == 16219)
    ok("SDBH kul domen_kod (— nélkül) = 380",
       len({r[9] for r in sdbh_rows if r[9] != EM_DASH}) == 380)
    ok("SDBH domen_kod = — sor = 344",
       sum(1 for r in sdbh_rows if r[9] == EM_DASH) == 344)
    ok("SDBH osszetett != — sor = 12",
       sum(1 for r in sdbh_rows if r[2] != EM_DASH) == 12)
    aram_rows = [r for r in sdbh_rows if r[3] == "arameus"]
    ok("SDBH nyelv=arameus sor = 2086", len(aram_rows) == 2086)
    ok("SDBH nyelv=arameus kul strong_kod = 647",
       len({r[1] for r in aram_rows}) == 647)

    # --- §1.4 SDGNT táblázat ---
    ok("SDGNT adatsor = 9075", len(sdgnt_rows) == 9075, str(len(sdgnt_rows)))
    ok("SDGNT kul strong = 5312", len({r[0] for r in sdgnt_rows}) == 5312)
    ok("SDGNT kul strong_kod = 5397", len({r[1] for r in sdgnt_rows}) == 5397)
    ok("SDGNT kul entry_id = 5397", len({r[5] for r in sdgnt_rows}) == 5397)
    ok("SDGNT kul lexid = 9067", len({r[7] for r in sdgnt_rows}) == 9067)
    ok("SDGNT kul domen_kod (— nélkül) = 668",
       len({r[9] for r in sdgnt_rows if r[9] != EM_DASH}) == 668)
    ok("SDGNT domen_kod = — sor = 21",
       sum(1 for r in sdgnt_rows if r[9] == EM_DASH) == 21)
    ok("SDGNT osszetett != — sor = 0",
       sum(1 for r in sdgnt_rows if r[2] != EM_DASH) == 0)

    # --- doménfa-sor / anomália-sor összesítve ---
    ok("doménfa-sor = 1149", len(domenfa_rows) == 1149, str(len(domenfa_rows)))
    ok("anomália-sor = 150", len(anom_rows) == 150, str(len(anom_rows)))
    sdbh_anom = [r for r in anom_rows if r[0] == "SDBH"]
    sdgnt_anom = [r for r in anom_rows if r[0] == "SDGNT"]
    ok("SDBH anomália = 40 (35 strong_nelkul + 5 ervenytelen_kod)",
       len(sdbh_anom) == 40
       and sum(1 for r in sdbh_anom if r[3] == "strong_nelkul") == 35
       and sum(1 for r in sdbh_anom if r[3] == "ervenytelen_kod") == 5)
    ok("SDGNT anomália = 110 strong_nelkul",
       len(sdgnt_anom) == 110
       and all(r[3] == "strong_nelkul" for r in sdgnt_anom))

    # --- négy SHA-256 ---
    expected_sha = {
        "SDBH_domenek.tsv": "678160daa869dc81ef8d5b7743d4e4be533d8933409805bc45158bef5debd709",
        "SDGNT_domenek.tsv": "800ae82baebdcc4ca9951fcfff8b861d98f4d6da5b9aec3917c2316395c0c097",
        "SDBH_SDGNT_domenfa.tsv": "88319a86cb313242b08abecc282f891353668f1862d918b54a8e9ec77efef991",
        "SDBH_SDGNT_anomaliak.tsv": "ab69a6162ff741282a5739326a848ef8d963a8862e0f01d26d2c3ef76dcb5ba1",
    }
    for name, expected in expected_sha.items():
        actual = sha256_no_comments(os.path.join(KONK, name))
        ok(f"{name} SHA-256 = {expected[:12]}…", actual == expected,
           "" if actual == expected else f"kapott {actual}")

    # --- doménfa-integritás ---
    tree_by_dict = {"SDBH": {}, "SDGNT": {}}
    for r in domenfa_rows:
        szotar, kod, _szint, szulo, _cimke, _leiras = r
        tree_by_dict[szotar][kod] = szulo

    missing_parent = []
    for szotar, codes in tree_by_dict.items():
        for kod, szulo in codes.items():
            if szulo != EM_DASH and szulo not in codes:
                missing_parent.append((szotar, kod, szulo))
    ok("minden szulo_kod létezik a saját szótára kódjai között", not missing_parent,
       str(missing_parent[:5]) if missing_parent else "")

    missing_domain_codes = []
    for r in sdbh_rows:
        if r[9] != EM_DASH and r[9] not in tree_by_dict["SDBH"]:
            missing_domain_codes.append(("SDBH", r[9]))
    for r in sdgnt_rows:
        if r[9] != EM_DASH and r[9] not in tree_by_dict["SDGNT"]:
            missing_domain_codes.append(("SDGNT", r[9]))
    missing_domain_codes = list({x for x in missing_domain_codes})
    ok("a kivonatok minden domen_kod-ja (— nélkül) szerepel a fában",
       not missing_domain_codes,
       str(missing_domain_codes[:5]) if missing_domain_codes else "")

    # --- arámi ellenőrzés (a "bejegyzés" az egység: brief §1.3) ---
    aram_by_entry = {}
    for r in sdbh_rows:
        aram_by_entry.setdefault(r[5], set()).add(r[3])
    only_aram_entries = {eid for eid, nyelvek in aram_by_entry.items() if nyelvek == {"arameus"}}
    ok("csak arámi kódot viselő bejegyzések száma = 367",
       len(only_aram_entries) == 367, str(len(only_aram_entries)))

    codes_by_entry = {}
    for r in sdbh_rows:
        if r[5] in only_aram_entries:
            codes_by_entry.setdefault(r[5], set()).add(r[0])

    tahot_path = os.path.join(KONK, "TAHOT_kivonat.tsv")
    tahot_header, tahot_rows = read_tsv(tahot_path)
    strong_idx = tahot_header.index("Strong-szám")
    igehely_idx = tahot_header.index("Igehely")

    def book_chapter(igehely):
        # "1Móz 3:16" -> ("1Móz", "3")
        book, rest = igehely.split(" ", 1)
        chapter = rest.split(":", 1)[0]
        return book, chapter

    tahot_locations = {}
    for r in tahot_rows:
        strong = r[strong_idx]
        book, chapter = book_chapter(r[igehely_idx])
        tahot_locations.setdefault(strong, set()).add((book, chapter))

    def is_exclusive_loc(book, chapter):
        if book in ("Dán", "Ezsd"):
            return True
        return (book, chapter) in {("Jer", "10"), ("1Móz", "31")}

    found = 0
    not_found = []
    exclusive = 0
    homograph_codes = set()
    for eid, codes in codes_by_entry.items():
        if not all(c in tahot_locations for c in codes):
            not_found.append(eid)
            continue
        found += 1
        entry_exclusive = True
        for code in codes:
            if not all(is_exclusive_loc(b, c) for (b, c) in tahot_locations[code]):
                entry_exclusive = False
                homograph_codes.add(code)
        if entry_exclusive:
            exclusive += 1

    ok("arámi: 367/367 bejegyzés A-kódja megtalálható H-alakban a TAHOT-ban",
       found == 367, f"{found}/367, hiányzó: {not_found[:5]}")
    ok("arámi: 362 kizárólag Dán/Ezsd/Jer10/1Móz31-ben",
       exclusive == 362, f"{exclusive}/362")
    expected_homographs = {"H1529", "H2269", "H5613", "H6211", "H8412"}
    ok("arámi: az öt homográf pontosan a felsorolt",
       homograph_codes == expected_homographs, str(sorted(homograph_codes)))

    # --- lefedettség ---
    tagnt_path = os.path.join(KONK, "TAGNT_kivonat.tsv")
    tagnt_header, tagnt_rows = read_tsv(tagnt_path)
    tagnt_strong_idx = tagnt_header.index("Strong-szám")

    def coverage(rows, strong_idx, sdbh_or_sdgnt_strongs, single_code_re, exclude_9xxx):
        distinct_strongs = set()
        total_tokens = 0
        covered_tokens = 0
        covered_strongs = set()
        for r in rows:
            s = r[strong_idx]
            if not single_code_re.match(s):
                continue
            if exclude_9xxx and s.startswith("H9"):
                continue
            total_tokens += 1
            distinct_strongs.add(s)
            if s in sdbh_or_sdgnt_strongs:
                covered_tokens += 1
                covered_strongs.add(s)
        return len(covered_strongs), len(distinct_strongs), covered_tokens, total_tokens

    sdbh_strongs = {r[0] for r in sdbh_rows}
    sdgnt_strongs = {r[0] for r in sdgnt_rows}
    single_h_re = re.compile(r'^H\d{4}[a-zA-Z]?$')
    single_g_re = re.compile(r'^G\d{4}[a-zA-Z]?$')

    cs, ds, ct, tt = coverage(tahot_rows, strong_idx, sdbh_strongs, single_h_re, exclude_9xxx=True)
    ok("TAHOT_kivonat lefedettség Strong-kód = 8421/8502",
       (cs, ds) == (8421, 8502), f"{cs}/{ds}")
    ok("TAHOT_kivonat lefedettség token = 259162/299370",
       (ct, tt) == (259162, 299370), f"{ct}/{tt}")

    cs2, ds2, ct2, tt2 = coverage(tagnt_rows, tagnt_strong_idx, sdgnt_strongs, single_g_re, exclude_9xxx=False)
    ok("TAGNT_kivonat lefedettség Strong-kód = 5252/5410",
       (cs2, ds2) == (5252, 5410), f"{cs2}/{ds2}")
    ok("TAGNT_kivonat lefedettség token = 130159/141489",
       (ct2, tt2) == (130159, 141489), f"{ct2}/{tt2}")

    print()
    if FAILURES == 0:
        print("ÖSSZESEN: minden kritérium OK.")
        sys.exit(0)
    else:
        print(f"ÖSSZESEN: {FAILURES} HIBA.")
        sys.exit(1)


if __name__ == "__main__":
    main()
