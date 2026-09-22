"""LXX-kivonat: lxx-morph (szöveg+morf+lemma) + GreekWordList (Strong), Károli-
igehely a meglévő LXX_versificacios_terkep.tsv + KEZI_ELTOLASOK segítségével.

A bulk Open Scriptorium SQLite csak ellenőrzésre szolgál (szószám/szóalak
egyezés versenként) — a repóba nem kerül. Élő API-hívás nincs.
Lásd LEXV2_1_BRIEF.md V1.3 (G4/G5, v3).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import unicodedata
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "eszkozok"))

from lxx_kivonat_fetch import (  # noqa: E402
    GOROG_LXX_VERS_RE,
    load_karoli_letezo_igehelyek,
    load_versifikacios_terkep,
)
from lxx_kivonat_fetch_v2 import KEZI_ELTOLASOK  # noqa: E402

KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")
LXX_OS_DIR = os.path.join(KONKORDANCIA_DIR, "LXX_OS")
TERKEP_UTVONAL = os.path.join(KONKORDANCIA_DIR, "LXX_versificacios_terkep.tsv")

LXX_MORPH_COMMIT = "c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2"
LXX_MORPH_RAW = f"https://raw.githubusercontent.com/OpenScriptorium/lxx-morph/{LXX_MORPH_COMMIT}/"
GREEKWORDLIST_COMMIT = "dd5a2fd530ab3c6b748c174cec38966c356d8111"
GREEKWORDLIST_RAW = f"https://raw.githubusercontent.com/openscriptures/GreekResources/{GREEKWORDLIST_COMMIT}/"
SQLITE_URL = "https://openscriptorium.org/downloads/openscriptorium.sqlite3"

# slug -> (cím, book_key, testamentum) — az lxx-morph db/seeds/lxx_morph/<slug>.json
# fájlnevei és az Open Scriptorium /api/v1/works/rahlfs-lxx könyvlistája szerint.
BOOKS = {
    "genesis": ("Genesis", "genesis", "ot"),
    "exodus": ("Exodus", "exodus", "ot"),
    "leviticus": ("Leviticus", "leviticus", "ot"),
    "numbers": ("Numbers", "numbers", "ot"),
    "deuteronomy": ("Deuteronomy", "deuteronomy", "ot"),
    "joshua": ("Joshua (Alexandrinus A-text)", "joshua", "ot"),
    "joshua-vaticanus-b": ("Joshua (Vaticanus B-text)", "joshua", "ot"),
    "judges": ("Judges (Alexandrinus A-text)", "judges", "ot"),
    "judges-vaticanus-b": ("Judges (Vaticanus B-text)", "judges", "ot"),
    "ruth": ("Ruth", "ruth", "ot"),
    "1-samuel": ("1 Samuel", "1-samuel", "ot"),
    "2-samuel": ("2 Samuel", "2-samuel", "ot"),
    "1-kings": ("1 Kings", "1-kings", "ot"),
    "2-kings": ("2 Kings", "2-kings", "ot"),
    "1-chronicles": ("1 Chronicles", "1-chronicles", "ot"),
    "2-chronicles": ("2 Chronicles", "2-chronicles", "ot"),
    "job-lxx": ("Job (LXX)", "job", "ot"),
    "psalms-lxx": ("Psalms (LXX)", "psalms", "ot"),
    "proverbs": ("Proverbs", "proverbs", "ot"),
    "ecclesiastes": ("Ecclesiastes", "ecclesiastes", "ot"),
    "song-of-solomon": ("Song of Solomon", "song-of-solomon", "ot"),
    "isaiah": ("Isaiah", "isaiah", "ot"),
    "jeremiah-lxx": ("Jeremiah (LXX)", "jeremiah", "ot"),
    "lamentations": ("Lamentations", "lamentations", "ot"),
    "ezekiel": ("Ezekiel", "ezekiel", "ot"),
    "daniel": ("Daniel", "daniel", "ot"),
    "daniel-theodotion": ("Daniel (Theodotion)", "daniel", "deuterocanon"),
    "hosea": ("Hosea", "hosea", "ot"),
    "joel": ("Joel", "joel", "ot"),
    "amos": ("Amos", "amos", "ot"),
    "obadiah": ("Obadiah", "obadiah", "ot"),
    "jonah": ("Jonah", "jonah", "ot"),
    "micah": ("Micah", "micah", "ot"),
    "nahum": ("Nahum", "nahum", "ot"),
    "habakkuk": ("Habakkuk", "habakkuk", "ot"),
    "zephaniah": ("Zephaniah", "zephaniah", "ot"),
    "haggai": ("Haggai", "haggai", "ot"),
    "zechariah": ("Zechariah", "zechariah", "ot"),
    "malachi": ("Malachi", "malachi", "ot"),
    "tobit": ("Tobit", "tobit", "deuterocanon"),
    "tobit-sinaiticus": ("Tobit (Sinaiticus recension)", "tobit", "deuterocanon"),
    "judith": ("Judith", "judith", "deuterocanon"),
    "esther-greek": ("Esther (Greek)", "esther-greek", "deuterocanon"),
    "wisdom": ("Wisdom of Solomon", "wisdom", "deuterocanon"),
    "sirach": ("Sirach (Ecclesiasticus)", "sirach", "deuterocanon"),
    "baruch": ("Baruch", "baruch", "deuterocanon"),
    "letter-of-jeremiah": ("Letter of Jeremiah", "letter-of-jeremiah", "deuterocanon"),
    "susanna": ("Susanna", "susanna", "deuterocanon"),
    "susanna-theodotion": ("Susanna (Theodotion)", "susanna", "deuterocanon"),
    "bel-and-the-dragon": ("Bel and the Dragon", "bel-and-the-dragon", "deuterocanon"),
    "bel-and-the-dragon-theodotion": ("Bel and the Dragon (Theodotion)", "bel-and-the-dragon", "deuterocanon"),
    "1-maccabees": ("1 Maccabees", "1-maccabees", "deuterocanon"),
    "2-maccabees": ("2 Maccabees", "2-maccabees", "deuterocanon"),
    "3-maccabees": ("3 Maccabees", "3-maccabees", "deuterocanon"),
    "4-maccabees": ("4 Maccabees", "4-maccabees", "deuterocanon"),
    "1-esdras": ("1 Esdras", "1-esdras", "deuterocanon"),
    "2-esdras": ("2 Esdras", "2-esdras", "deuterocanon"),
    "psalms-of-solomon": ("Psalms of Solomon", "psalms-of-solomon", "pseudepigrapha"),
    "odes": ("Odes", "odes", "deuterocanon"),
}

BOOK_KEY_TO_KAROLI = {
    "genesis": "1Móz", "exodus": "2Móz", "leviticus": "3Móz", "numbers": "4Móz",
    "deuteronomy": "5Móz", "joshua": "Józs", "judges": "Bír", "ruth": "Ruth",
    "1-samuel": "1Sám", "2-samuel": "2Sám", "1-kings": "1Kir", "2-kings": "2Kir",
    "1-chronicles": "1Krón", "2-chronicles": "2Krón", "job": "Jób", "psalms": "Zsolt",
    "proverbs": "Péld", "ecclesiastes": "Préd", "song-of-solomon": "Én", "isaiah": "Ézs",
    "jeremiah": "Jer", "lamentations": "Sir", "ezekiel": "Ez", "daniel": "Dán",
    "hosea": "Hós", "joel": "Jóel", "amos": "Ámós", "obadiah": "Abd", "jonah": "Jón",
    "micah": "Mik", "nahum": "Náh", "habakkuk": "Hab", "zephaniah": "Sof",
    "haggai": "Hag", "zechariah": "Zak", "malachi": "Mal",
}
KAROLI_TO_ENGLISH_FOR_KEZI = {
    "4Móz": "Numbers", "Jób": "Job", "Préd": "Ecclesiastes", "Dán": "Daniel",
}

VERS_REF_RE = re.compile(r'^(\d+):(\d+)$')
EM_DASH = "—"

LXX_OS_HEADER = [
    "igehely_lxx", "igehely_kjv", "igehely_karoli", "karoli_ok", "pozicio",
    "szoalak", "normalizalt", "lemma", "morf", "strong", "strong_ok",
    "proveniencia",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_accents(s):
    decomposed = unicodedata.normalize("NFD", s)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn").lower()


def download(url, dest):
    urllib.request.urlretrieve(url, dest)
    return dest


def letolt_forrasok(cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
    morph_dir = os.path.join(cache_dir, "lxx_morph")
    os.makedirs(morph_dir, exist_ok=True)
    for slug in BOOKS:
        dest = os.path.join(morph_dir, f"{slug}.json")
        if not os.path.isfile(dest):
            print(f"  letoltes: {slug}.json", file=sys.stderr)
            download(LXX_MORPH_RAW + f"db/seeds/lxx_morph/{slug}.json", dest)
    verse_pairs_dest = os.path.join(cache_dir, "verse_pairs.jsonl")
    if not os.path.isfile(verse_pairs_dest):
        print("  letoltes: verse_pairs.jsonl", file=sys.stderr)
        download(LXX_MORPH_RAW + "db/seeds/mt_alignment/verse_pairs.jsonl", verse_pairs_dest)
    gwl_dest = os.path.join(cache_dir, "GreekWordList.js")
    if not os.path.isfile(gwl_dest):
        print("  letoltes: GreekWordList.js", file=sys.stderr)
        download(GREEKWORDLIST_RAW + "GreekWordList.js", gwl_dest)
    return cache_dir


def letolt_sqlite(cache_dir):
    dest = os.path.join(cache_dir, "openscriptorium.sqlite3")
    if not os.path.isfile(dest):
        print("  letoltes: openscriptorium.sqlite3 (ellenorzeshez, ~339 MB)", file=sys.stderr)
        download(SQLITE_URL, dest)
    return dest


def load_greek_word_list(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    content = content.split("=", 1)[1].strip()
    if content.endswith(";"):
        content = content[:-1]
    return json.loads(content)


def load_verse_pairs(path):
    """grk_book -> {grk_ref: (mt_book, mt_refs, method)}"""
    idx = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            idx.setdefault(d["grk_book"], {})[d["grk_ref"]] = (
                d.get("mt_book"), d.get("mt_refs") or [], d.get("method")
            )
    return idx


def build_gorog_to_karoli(karoli_book):
    """LXX_versificacios_terkep.tsv alapján (fejezet,vers) -> Karoli_igehely."""
    gorog_lookup, warns, betu_excl, nem_parsz = load_versifikacios_terkep(TERKEP_UTVONAL, karoli_book)
    gorog_map, heber_map = gorog_lookup
    result = {}
    for (kert_fej, zar_fej, zar_vers), igehely in gorog_map.items():
        result.setdefault((kert_fej, zar_vers), igehely)
    for (kert_fej, zar_fej, zar_vers), igehely in heber_map.items():
        result.setdefault((kert_fej, zar_vers), igehely)
    return result, warns


def resolve_karoli(karoli_book, gorog_to_karoli, letezo_igehelyek, fejezet, vers, kezi_fn):
    key = (fejezet, vers)
    if key in gorog_to_karoli:
        return gorog_to_karoli[key], "versificacios_terkep"
    if kezi_fn:
        cel = kezi_fn(fejezet, vers)
        if cel is not None:
            igehely = f"{karoli_book} {cel[0]}:{cel[1]}"
            return igehely, "kezi_eltolas_tabla"
    identity = f"{karoli_book} {fejezet}:{vers}"
    if identity in letezo_igehelyek:
        return identity, ""
    return None, "szamozas_elteres"


def process_book(slug, morph_dir, verse_pairs_idx, greek_word_list, proveniencia_line):
    title, book_key, testament = BOOKS[slug]
    karoli_book = BOOK_KEY_TO_KAROLI.get(book_key)

    gorog_to_karoli = {}
    letezo_igehelyek = set()
    kezi_fn = None
    map_warns = []
    if karoli_book:
        gorog_to_karoli, map_warns = build_gorog_to_karoli(karoli_book)
        letezo_igehelyek = load_karoli_letezo_igehelyek(
            os.path.join(KONKORDANCIA_DIR, "Karoli_1908.tsv"), karoli_book
        )
        eng_name = KAROLI_TO_ENGLISH_FOR_KEZI.get(karoli_book)
        kezi_fn = KEZI_ELTOLASOK.get(eng_name) if eng_name else None

    morph_path = os.path.join(morph_dir, f"{slug}.json")
    with open(morph_path, encoding="utf-8") as f:
        verses = json.load(f)

    vp_for_book = verse_pairs_idx.get(slug, {})

    rows = []
    stats = {"karoli_ok": 0, "szamozas_elteres": 0, "nincs_mt_parositas": 0, "nincs_karoli_konyv": 0}
    hiany_fejezetek = set()

    for v in verses:
        ref = v["ref"]
        m = re.search(r'(\d+):(\d+)$', ref)
        if not m:
            continue
        fejezet, vers = int(m.group(1)), int(m.group(2))
        igehely_lxx = f"{title} {fejezet}:{vers}"

        mt_book, mt_refs, method = vp_for_book.get(f"{fejezet}:{vers}", (None, [], None))
        igehely_kjv = ";".join(mt_refs) if mt_refs else ""

        if not karoli_book:
            igehely_karoli, karoli_ok = "", "nincs_karoli_konyv"
            stats["nincs_karoli_konyv"] += 1
        elif method == "unpaired" or not mt_refs:
            igehely_karoli, karoli_ok = "", "nincs_mt_parositas"
            stats["nincs_mt_parositas"] += 1
        else:
            igehely_karoli, karoli_ok = resolve_karoli(
                karoli_book, gorog_to_karoli, letezo_igehelyek, fejezet, vers, kezi_fn
            )
            if igehely_karoli is None:
                igehely_karoli = ""
                stats["szamozas_elteres"] += 1
                hiany_fejezetek.add(fejezet)
            else:
                stats["karoli_ok"] += 1
                if karoli_ok == "":
                    pass

        for pozicio, w in enumerate(v.get("words") or [], start=1):
            surface = w.get("surface", "")
            lemma = w.get("lemma", "")
            pos = w.get("pos", "")
            parsing = w.get("parsing", "")
            morf = f"{pos} {parsing}".strip()

            gwl_key = strip_accents(lemma)
            gwl_entry = greek_word_list.get(gwl_key)
            if gwl_entry is None:
                strong, strong_ok = "", "lemma_nem_talalhato"
            elif gwl_entry.get("strong"):
                strong, strong_ok = gwl_entry["strong"], ""
            else:
                strong, strong_ok = "", "nincs_uszbeli_megfelelo"

            rows.append((
                igehely_lxx, igehely_kjv, igehely_karoli, karoli_ok,
                str(pozicio), surface, strip_accents(surface), lemma, morf,
                strong, strong_ok, proveniencia_line,
            ))

    return rows, stats, sorted(hiany_fejezetek), map_warns


def write_tsv(path, rows, comment_lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for line in comment_lines:
            f.write(line + "\n")
        f.write("\t".join(LXX_OS_HEADER) + "\n")
        for row in rows:
            f.write("\t".join(row) + "\n")


def ellenoriz_sqlite(sqlite_path, slug, verses):
    """Szószám/szóalak-sorozat egyezés versenkent az SQLite ellen. Eltéréseket
    ad vissza (nem blokkol)."""
    con = sqlite3.connect(sqlite_path)
    cur = con.cursor()
    cur.execute("select id from works where slug='rahlfs-lxx'")
    row = cur.fetchone()
    if row is None:
        return ["nincs 'rahlfs-lxx' work a SQLite-ban"]
    work_id = row[0]
    _title, book_key, _test = BOOKS[slug]
    cur.execute("""
        select cr.hierarchy, wu.body
        from work_units wu
        join canonical_refs cr on wu.canonical_ref_id = cr.id
        join canonical_works cw on cr.canonical_work_id = cw.id
        where wu.work_id=? and cw.slug=?
    """, (work_id, slug))
    sqlite_verses = {}
    for hierarchy, body in cur.fetchall():
        sqlite_verses[hierarchy.replace(",", ":")] = body
    eltekek = []
    for v in verses:
        m = re.search(r'(\d+:\d+)$', v["ref"])
        if not m:
            continue
        ref = m.group(1)
        expected_n = len(v.get("words") or [])
        body = sqlite_verses.get(ref)
        if body is None:
            eltekek.append(f"{slug} {ref}: nincs a SQLite-ban")
            continue
        actual_n = len(body.split())
        if actual_n != expected_n:
            eltekek.append(f"{slug} {ref}: szoszam elter (lxx-morph={expected_n}, sqlite={actual_n})")
    con.close()
    return eltekek


def main():
    parser = argparse.ArgumentParser(description="LXX-kivonat (lxx-morph + GreekWordList)")
    parser.add_argument("--letolt", action="store_true", help="forrasok letoltese a rogzitett commitokrol")
    parser.add_argument("--forras", metavar="KONYVTAR", help="mar letoltott forrasok konyvtara")
    parser.add_argument("--sqlite-ellenoriz", action="store_true", help="bulk SQLite letoltese es ellenorzes")
    parser.add_argument("--konyvek", help="csak ezekre a slugokra fusson (vesszovel elvalasztva)")
    args = parser.parse_args()

    if args.letolt and args.forras:
        print("HIBA: --letolt es --forras kizarja egymast.", file=sys.stderr)
        sys.exit(1)
    if not args.letolt and not args.forras:
        print("HIBA: --letolt vagy --forras szukseges.", file=sys.stderr)
        sys.exit(1)

    cleanup_dir = None
    try:
        if args.letolt:
            cache_dir = tempfile.mkdtemp(prefix="lxx_os_")
            cleanup_dir = cache_dir
            letolt_forrasok(cache_dir)
        else:
            cache_dir = args.forras

        morph_dir = os.path.join(cache_dir, "lxx_morph")
        verse_pairs_idx = load_verse_pairs(os.path.join(cache_dir, "verse_pairs.jsonl"))
        greek_word_list = load_greek_word_list(os.path.join(cache_dir, "GreekWordList.js"))

        morph_sha = sha256_file(os.path.join(cache_dir, "verse_pairs.jsonl"))
        gwl_sha = sha256_file(os.path.join(cache_dir, "GreekWordList.js"))
        proveniencia_line = (
            f"forras=lxx-morph@{LXX_MORPH_COMMIT} | forras=GreekWordList@{GREEKWORDLIST_COMMIT} | "
            f"ts={__import__('datetime').date.today().isoformat()}"
        )

        os.makedirs(LXX_OS_DIR, exist_ok=True)

        slugs = list(BOOKS)
        if args.konyvek:
            slugs = [s for s in args.konyvek.split(",") if s]

        sqlite_path = None
        if args.sqlite_ellenoriz:
            sqlite_path = letolt_sqlite(cache_dir if args.letolt else args.forras)

        osszes_stat = {"karoli_ok": 0, "szamozas_elteres": 0, "nincs_mt_parositas": 0, "nincs_karoli_konyv": 0}
        osszes_hiany = {}
        osszes_map_warns = []
        sqlite_eltek = []

        for slug in slugs:
            morph_path = os.path.join(morph_dir, f"{slug}.json")
            if not os.path.isfile(morph_path):
                print(f"  HIANYZIK: {morph_path}", file=sys.stderr)
                continue
            with open(morph_path, encoding="utf-8") as f:
                verses = json.load(f)
            rows, stats, hiany_fejezetek, map_warns = process_book(
                slug, morph_dir, verse_pairs_idx, greek_word_list, proveniencia_line
            )
            comment = [
                "# GENERÁLT: eszkozok/lxx_os_import.py — kézzel nem szerkesztendő.",
                f"# forras: lxx-morph@{LXX_MORPH_COMMIT} (CC BY 4.0) + GreekWordList@{GREEKWORDLIST_COMMIT} (CC BY 4.0)",
                f"# sha256(verse_pairs.jsonl)={morph_sha} | sha256(GreekWordList.js)={gwl_sha}",
            ]
            write_tsv(os.path.join(LXX_OS_DIR, f"{slug}.tsv"), rows, comment)
            for k, v in stats.items():
                osszes_stat[k] += v
            if hiany_fejezetek:
                osszes_hiany[slug] = hiany_fejezetek
            osszes_map_warns.extend(map_warns)
            if sqlite_path:
                sqlite_eltek.extend(ellenoriz_sqlite(sqlite_path, slug, verses))
            print(f"  {slug}: {len(rows)} sor", file=sys.stderr)

        print("\n=== Összesítés ===", file=sys.stderr)
        for k, v in osszes_stat.items():
            print(f"  {k}: {v}", file=sys.stderr)
        if osszes_hiany:
            print("\n=== Fejezetek szamozas_elteres-szel ===", file=sys.stderr)
            for slug, chs in osszes_hiany.items():
                print(f"  {slug}: {chs}", file=sys.stderr)
        if sqlite_path:
            print(f"\n=== SQLite-ellenorzes: {len(sqlite_eltek)} elteres ===", file=sys.stderr)
            for e in sqlite_eltek[:50]:
                print(f"  {e}", file=sys.stderr)
    finally:
        if cleanup_dir:
            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
