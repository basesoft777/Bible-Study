"""SDBH/SDGNT import — UBS szemantikai domén-szótárak kivonatolása.

Forrás: ubsicap/ubs-open-license (CC BY-SA 4.0). Lásd SDBH_IMPORT_BRIEF.md.
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
import tarfile
import tempfile
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")

UBS_COMMIT = "3a6edd8212df2e1189037ad39687726990c80d56"
UBS_URL = "https://codeload.github.com/ubsicap/ubs-open-license/tar.gz/" + UBS_COMMIT

# key -> (relatív útvonal a dictionaries/ szülőkönyvtárból, elvárt SHA-256)
FILES = {
    "hebrew_dic": (
        "dictionaries/hebrew/JSON/UBSHebrewDic-v0.9.2-en.JSON",
        "1686a25dd31dc9afb7b932927e160070667c73caedad11aa7e4482c21f800e8e",
    ),
    "hebrew_dom": (
        "dictionaries/hebrew/JSON/UBSHebrewDicLexicalDomains-v0.9.2-en.JSON",
        "fbc862b2c46966cf7f3bf19c2f3e79a7391c34f8c737e1979fa5178ac603d0df",
    ),
    "greek_dic": (
        "dictionaries/greek/JSON/UBSGreekNTDic-v1.1-en.JSON",
        "d84bb9077a43fa4a4f7e571fe2ffa460fa655d7b78439b366281ce527fd56893",
    ),
    "greek_dom": (
        "dictionaries/greek/JSON/UBSGreekNTDicLexicalDomains-v1.1-en.JSON",
        "a816a6bb2bdbdd7df6f46f771b5ddb1b9c019d73c3f0147e5a5cead5cfef8b4b",
    ),
}

STRONG_RE = re.compile(r'^([HAG])(\d{4})([a-f]?)$')
WS_RE = re.compile(r'[\t\r\n]+')
EM_DASH = "—"

NYELV_MAP = {"H": "heber", "A": "arameus", "G": "gorog"}

DOMENEK_HEADER = [
    "strong", "strong_kod", "osszetett", "nyelv", "szotar", "entry_id",
    "lemma", "lexid", "entry_kod", "domen_kod", "domen", "glossza",
    "hivatkozas_n",
]
DOMENFA_HEADER = ["szotar", "kod", "szint", "szulo_kod", "cimke", "leiras"]
ANOMALIAK_HEADER = ["szotar", "entry_id", "lemma", "tipus", "nyers_ertek", "allapot"]


def clean_text(s):
    if not s:
        return ""
    return WS_RE.sub(" ", s).strip()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_and_locate(base_dir):
    """base_dir a dictionaries/ szülőkönyvtára. Visszaad key -> teljes útvonal
    mapet, vagy 2-es kóddal kilép SHA-eltérésnél."""
    result = {}
    for key, (relpath, expected_sha) in FILES.items():
        full_path = os.path.join(base_dir, relpath.replace("/", os.sep))
        if not os.path.isfile(full_path):
            print(f"HIBA: hiányzó fájl: {full_path}", file=sys.stderr)
            sys.exit(2)
        actual = sha256_file(full_path)
        if actual != expected_sha:
            print(
                f"HIBA: SHA-256 eltérés — {relpath}\n"
                f"  várt:   {expected_sha}\n"
                f"  kapott: {actual}",
                file=sys.stderr,
            )
            sys.exit(2)
        result[key] = full_path
    return result


def download_sources():
    tmp = tempfile.mkdtemp(prefix="sdbh_sdgnt_")
    tarball = os.path.join(tmp, "ubs.tar.gz")
    try:
        urllib.request.urlretrieve(UBS_URL, tarball)
        with tarfile.open(tarball) as tf:
            root_prefix = None
            for name in tf.getnames():
                root_prefix = name.split("/")[0]
                break
            members = []
            for key, (relpath, _sha) in FILES.items():
                member_name = f"{root_prefix}/{relpath}"
                members.append(tf.getmember(member_name))
            tf.extractall(path=tmp, members=members)
        base_dir = os.path.join(tmp, root_prefix)
        located = verify_and_locate(base_dir)
        # a fájlokat egy stabil ideiglenes könyvtárba másoljuk, hogy a
        # tar tmp könyvtár törlése után is elérhetők legyenek a hívó számára
        return located, tmp
    except SystemExit:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


def parse_strong_codes(raw_list, szotar, entry_id, lemma, anomalies):
    """Visszaadja az érvényes (strong, strong_kod, osszetett, nyelv) négyeseket.
    Az érvénytelen és üres eseteket az anomalies listába írja."""
    valid_parts = []
    for sc in (raw_list or []):
        if sc == "":
            continue
        elem_parts = sc.split("+")
        is_composite = len(elem_parts) > 1
        for part in elem_parts:
            m = STRONG_RE.match(part)
            if not m:
                anomalies.append((szotar, entry_id, lemma, "ervenytelen_kod", sc))
                continue
            prefix, digits, _suffix = m.groups()
            strong = ("H" if prefix in ("H", "A") else "G") + digits
            nyelv = NYELV_MAP[prefix]
            osszetett = sc if is_composite else EM_DASH
            valid_parts.append((strong, part, osszetett, nyelv))
    if not valid_parts:
        anomalies.append(
            (szotar, entry_id, lemma, "strong_nelkul",
             json.dumps(raw_list or [], ensure_ascii=False))
        )
    return valid_parts


def extract_glossza(lex_senses):
    glosses = []
    seen = set()
    for sense in (lex_senses or []):
        if sense.get("LanguageCode") != "en":
            continue
        for g in (sense.get("Glosses") or []):
            g_clean = clean_text(g)
            if g_clean and g_clean not in seen:
                seen.add(g_clean)
                glosses.append(g_clean)
    return "; ".join(glosses) if glosses else EM_DASH


def extract_domains(lex_meaning, szotar):
    def nonempty(lst):
        return [d for d in (lst or []) if d.get("DomainCode")]

    if szotar == "SDGNT":
        subdomains = nonempty(lex_meaning.get("LEXSubDomains"))
        chosen = subdomains if subdomains else nonempty(lex_meaning.get("LEXDomains"))
    else:
        chosen = nonempty(lex_meaning.get("LEXDomains"))

    if not chosen:
        return [(EM_DASH, EM_DASH)]
    return [(d["DomainCode"], clean_text(d["Domain"])) for d in chosen]


def process_dictionary(json_path, szotar):
    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)

    rows = set()
    anomalies = []
    for e in entries:
        entry_id = e["MainId"]
        lemma = clean_text(e.get("Lemma"))
        strong_parts = parse_strong_codes(
            e.get("StrongCodes"), szotar, entry_id, lemma, anomalies
        )
        if not strong_parts:
            continue
        for bf in (e.get("BaseForms") or []):
            for lm in (bf.get("LEXMeanings") or []):
                lexid = lm.get("LEXID", "")
                raw_entry_kod = lm.get("LEXEntryCode")
                entry_kod = clean_text(raw_entry_kod) if raw_entry_kod else EM_DASH
                glossza = extract_glossza(lm.get("LEXSenses"))
                hivatkozas_n = str(len(lm.get("LEXReferences") or []))
                domains = extract_domains(lm, szotar)
                for (strong, strong_kod, osszetett, nyelv) in strong_parts:
                    for (domen_kod, domen) in domains:
                        rows.add((
                            strong, strong_kod, osszetett, nyelv, szotar,
                            entry_id, lemma, lexid, entry_kod, domen_kod,
                            domen, glossza, hivatkozas_n,
                        ))
    return rows, anomalies, len(entries)


def process_domain_tree(json_path, szotar):
    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)

    rows = set()
    for d in entries:
        code = d["Code"]
        level = str(d["Level"])
        szulo_kod = code[:-3] if len(code) > 3 else EM_DASH
        label = EM_DASH
        desc = EM_DASH
        for loc in (d.get("SemanticDomainLocalizations") or []):
            if loc.get("LanguageCode") == "en":
                label = clean_text(loc.get("Label")) or EM_DASH
                desc = clean_text(loc.get("Description")) or EM_DASH
                break
        rows.add((szotar, code, level, szulo_kod, label, desc))
    return rows


def write_tsv(path, header, rows, comment_lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for line in comment_lines:
            f.write(line + "\n")
        f.write("\t".join(header) + "\n")
        for row in sorted(rows):
            f.write("\t".join(row) + "\n")


def comment_lines_for(source_desc):
    return [
        "# GENERÁLT: eszkozok/sdbh_sdgnt_import.py — kézzel nem szerkesztendő.",
        f"# forras: ubsicap/ubs-open-license @ {UBS_COMMIT} | {source_desc}",
        "# licenc: CC BY-SA 4.0 — © United Bible Societies; forrásmegjelölés: konkordancia/SDBH_SDGNT_README.md",
    ]


def src_desc(name, path):
    return f"{name} sha256={sha256_file(path)}"


def run_minta(paths):
    hebrew_rows, hebrew_anoms, _n = process_dictionary(paths["hebrew_dic"], "SDBH")
    greek_rows, greek_anoms, _n2 = process_dictionary(paths["greek_dic"], "SDGNT")

    def rows_for(rows, pred):
        return sorted(r for r in rows if pred(r))

    print("=== H0779 ===")
    for r in rows_for(hebrew_rows, lambda r: r[0] == "H0779"):
        print("\t".join(r))

    print("=== H6093 ===")
    for r in rows_for(hebrew_rows, lambda r: r[0] == "H6093"):
        print("\t".join(r))

    print("=== A0002 ===")
    for r in rows_for(hebrew_rows, lambda r: r[1] == "A0002"):
        print("\t".join(r))

    print("=== G2671 ===")
    for r in rows_for(greek_rows, lambda r: r[0] == "G2671"):
        print("\t".join(r))

    print("=== H1237+H0205a összetett ===")
    for r in rows_for(hebrew_rows, lambda r: r[2] == "H1237+H0205a"):
        print("\t".join(r))

    h7043_domains = {r[9] for r in hebrew_rows if r[0] == "H7043"}
    print(f"=== H7043 doménszám: {len(h7043_domains)} ===")

    print("=== ervenytelen_kod anomáliák (SDBH) ===")
    for a in sorted(x for x in hebrew_anoms if x[3] == "ervenytelen_kod"):
        print("\t".join(a))


def run_full(paths):
    os.makedirs(KONKORDANCIA_DIR, exist_ok=True)

    hebrew_rows, hebrew_anoms, _n = process_dictionary(paths["hebrew_dic"], "SDBH")
    greek_rows, greek_anoms, _n2 = process_dictionary(paths["greek_dic"], "SDGNT")

    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "SDBH_domenek.tsv"),
        DOMENEK_HEADER,
        hebrew_rows,
        comment_lines_for(src_desc("UBSHebrewDic-v0.9.2-en.JSON", paths["hebrew_dic"])),
    )
    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "SDGNT_domenek.tsv"),
        DOMENEK_HEADER,
        greek_rows,
        comment_lines_for(src_desc("UBSGreekNTDic-v1.1-en.JSON", paths["greek_dic"])),
    )

    hebrew_tree = process_domain_tree(paths["hebrew_dom"], "SDBH")
    greek_tree = process_domain_tree(paths["greek_dom"], "SDGNT")
    tree_desc = (
        src_desc("UBSHebrewDicLexicalDomains-v0.9.2-en.JSON", paths["hebrew_dom"])
        + "; "
        + src_desc("UBSGreekNTDicLexicalDomains-v1.1-en.JSON", paths["greek_dom"])
    )
    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "SDBH_SDGNT_domenfa.tsv"),
        DOMENFA_HEADER,
        hebrew_tree | greek_tree,
        comment_lines_for(tree_desc),
    )

    anom_desc = (
        src_desc("UBSHebrewDic-v0.9.2-en.JSON", paths["hebrew_dic"])
        + "; "
        + src_desc("UBSGreekNTDic-v1.1-en.JSON", paths["greek_dic"])
    )
    all_anoms = {tuple(list(a) + ["AZONOSITVA, NEM JAVITVA"]) for a in hebrew_anoms + greek_anoms}
    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "SDBH_SDGNT_anomaliak.tsv"),
        ANOMALIAK_HEADER,
        all_anoms,
        comment_lines_for(anom_desc),
    )


def main():
    parser = argparse.ArgumentParser(description="SDBH/SDGNT import — szemantikai domén-kivonat")
    parser.add_argument("--letolt", action="store_true", help="forrás letöltése a rögzített UBS-commitról")
    parser.add_argument("--forras", metavar="KÖNYVTÁR", help="már kibontott dictionaries/ szülőkönyvtára")
    parser.add_argument("--minta", action="store_true", help="csak mintakimenet, nem ír fájlt")
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
            paths, cleanup_dir = download_sources()
        else:
            paths = verify_and_locate(args.forras)

        if args.minta:
            run_minta(paths)
        else:
            run_full(paths)
    finally:
        if cleanup_dir:
            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
