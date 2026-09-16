"""OSHL lexikális index import — TWOT-szám és BDB-azonosító kivonat.

Forrás: openscriptures/HebrewLexicon (CC BY 4.0). Lásd F6_BRIEF.md F6.1.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import hashlib
import os
import re
import shutil
import tarfile
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")

OSHL_COMMIT = "21c9add13bc727d3a951361778e97e3ff7afd1ce"
OSHL_URL = "https://codeload.github.com/openscriptures/HebrewLexicon/tar.gz/" + OSHL_COMMIT
LEXICAL_INDEX_RELPATH = "LexicalIndex.xml"
LEXICAL_INDEX_SHA256 = (
    "8f7a605c58899d2f44430149c143c00903976e1e91232476677972a69e5bc85f"
)

EM_DASH = "—"
WS_RE = re.compile(r"\s+")
STRONG_DIGITS_RE = re.compile(r"^\d+$")
NYELV_MAP = {"heb": "heber", "arc": "arameus"}

HEADER = [
    "strong", "strong_eredeti", "twot", "bdb_id", "nyelv", "oshl_id",
    "lemma", "atiras", "szofaj", "def_en",
]


def clean_text(s):
    if not s:
        return EM_DASH
    s = WS_RE.sub(" ", s).strip()
    return s if s else EM_DASH


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_and_locate(base_dir):
    full_path = os.path.join(base_dir, LEXICAL_INDEX_RELPATH)
    if not os.path.isfile(full_path):
        print(f"HIBA: hiányzó fájl: {full_path}", file=sys.stderr)
        sys.exit(2)
    actual = sha256_file(full_path)
    if actual != LEXICAL_INDEX_SHA256:
        print(
            f"HIBA: SHA-256 eltérés — {LEXICAL_INDEX_RELPATH}\n"
            f"  várt:   {LEXICAL_INDEX_SHA256}\n"
            f"  kapott: {actual}",
            file=sys.stderr,
        )
        sys.exit(2)
    return full_path


def download_source():
    tmp = tempfile.mkdtemp(prefix="oshl_index_")
    tarball = os.path.join(tmp, "oshl.tar.gz")
    try:
        urllib.request.urlretrieve(OSHL_URL, tarball)
        with tarfile.open(tarball) as tf:
            root_prefix = None
            for name in tf.getnames():
                root_prefix = name.split("/")[0]
                break
            member_name = f"{root_prefix}/{LEXICAL_INDEX_RELPATH}"
            tf.extract(tf.getmember(member_name), path=tmp)
        base_dir = os.path.join(tmp, root_prefix)
        located = verify_and_locate(base_dir)
        return located, tmp
    except SystemExit:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def strong_from_attr(raw):
    if raw and STRONG_DIGITS_RE.match(raw):
        return "H" + raw.zfill(4)
    return EM_DASH


def process_lexical_index(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns_match = re.match(r"^\{(.*)\}", root.tag)
    ns_uri = ns_match.group(1) if ns_match else ""

    def tag(name):
        return f"{{{ns_uri}}}{name}" if ns_uri else name

    rows = set()
    for part in root.iter(tag("part")):
        lang = part.get("{http://www.w3.org/XML/1998/namespace}lang", "")
        nyelv = NYELV_MAP.get(lang, EM_DASH)
        for entry in part.findall(tag("entry")):
            oshl_id = entry.get("id", "") or EM_DASH
            w_el = entry.find(tag("w"))
            pos_el = entry.find(tag("pos"))
            def_el = entry.find(tag("def"))

            lemma = clean_text("".join(w_el.itertext())) if w_el is not None else EM_DASH
            atiras = clean_text(w_el.get("xlit")) if w_el is not None else EM_DASH
            szofaj = clean_text("".join(pos_el.itertext())) if pos_el is not None else EM_DASH
            def_en = clean_text("".join(def_el.itertext())) if def_el is not None else EM_DASH

            for xref in entry.findall(tag("xref")):
                bdb_raw = xref.get("bdb")
                strong_raw = xref.get("strong")
                twot_raw = xref.get("twot")

                strong = strong_from_attr(strong_raw)
                strong_eredeti = strong_raw if strong_raw else EM_DASH
                twot = twot_raw if twot_raw else EM_DASH
                bdb_id = bdb_raw if bdb_raw else EM_DASH

                rows.add((
                    strong, strong_eredeti, twot, bdb_id, nyelv, oshl_id,
                    lemma, atiras, szofaj, def_en,
                ))
    return rows


def write_tsv(path, header, rows, comment_lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for line in comment_lines:
            f.write(line + "\n")
        f.write("\t".join(header) + "\n")
        for row in sorted(rows):
            f.write("\t".join(row) + "\n")


def comment_lines_for(sha):
    return [
        "# GENERÁLT: eszkozok/oshl_index_import.py — kézzel nem szerkesztendő.",
        f"# forras: openscriptures/HebrewLexicon @ {OSHL_COMMIT} | "
        f"LexicalIndex.xml sha256={sha}",
        "# licenc: CC BY 4.0 — Open Scriptures Hebrew Bible Project; "
        "l. konkordancia/OSHL_lexikalis_index_README.md",
    ]


def run_full(xml_path):
    os.makedirs(KONKORDANCIA_DIR, exist_ok=True)
    rows = process_lexical_index(xml_path)
    sha = sha256_file(xml_path)
    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "OSHL_lexikalis_index.tsv"),
        HEADER,
        rows,
        comment_lines_for(sha),
    )


def main():
    parser = argparse.ArgumentParser(
        description="OSHL lexikális index import — TWOT-szám és BDB-azonosító kivonat"
    )
    parser.add_argument("--letolt", action="store_true", help="forrás letöltése a rögzített OSHL-commitról")
    parser.add_argument("--forras", metavar="XML_FAJL", help="már letöltött LexicalIndex.xml útvonala")
    args = parser.parse_args()

    if args.letolt and args.forras:
        print("HIBA: --letolt és --forras kizárja egymást.", file=sys.stderr)
        sys.exit(1)
    if not args.letolt and not args.forras:
        print("HIBA: --letolt vagy --forras szükséges.", file=sys.stderr)
        sys.exit(1)

    cleanup_dir = None
    try:
        if args.letolt:
            xml_path, cleanup_dir = download_source()
        else:
            actual = sha256_file(args.forras)
            if actual != LEXICAL_INDEX_SHA256:
                print(
                    f"HIBA: SHA-256 eltérés — {args.forras}\n"
                    f"  várt:   {LEXICAL_INDEX_SHA256}\n"
                    f"  kapott: {actual}",
                    file=sys.stderr,
                )
                sys.exit(2)
            xml_path = args.forras

        run_full(xml_path)
    finally:
        if cleanup_dir:
            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
