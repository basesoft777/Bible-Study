"""UBS Dictionary of Biblical Hebrew import -- jelentesek es igehely-hivatkozasok.

Az eszkozok/ubs_dntg_import.py mintajara (SZOTAR_BRIEF.md S5). Forras:
ubsicap/ubs-open-license (CC BY-SA 4.0), ugyanaz a commit, mint a
konkordancia/SDBH_SDGNT_README.md-ben rogzitett SDBH/SDGNT-importe.
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

HEBREW_DIC_RELPATH = "dictionaries/hebrew/JSON/UBSHebrewDic-v0.9.2-en.JSON"
HEBREW_DIC_SHA = "1686a25dd31dc9afb7b932927e160070667c73caedad11aa7e4482c21f800e8e"

STRONG_RE = re.compile(r'^H(\d{4})([a-f]?)$')
WS_RE = re.compile(r'[\t\r\n]+')
REF_RE = re.compile(r'^(\d{3})(\d{3})(\d{3})(\d{5})')
EM_DASH = "—"

# UBS/Paratext-USFM konyvkod (001-039) -> magyar Karoli-rovidites, a
# konkordancia/Konyv_normalizalo_tabla.tsv elso 39 soraval (kanonikus OSZ
# sorrend) egyezo indexeles. Ugyanaz a szamozasi konvencio, mint amit a
# ubs_dntg_import.py BOOK_CODES-ja (040=Mt...066=Jel) mar hasznal a NT-re.
BOOK_CODES = {
    "001": "1Móz", "002": "2Móz", "003": "3Móz", "004": "4Móz", "005": "5Móz",
    "006": "Józs", "007": "Bír", "008": "Ruth", "009": "1Sám", "010": "2Sám",
    "011": "1Kir", "012": "2Kir", "013": "1Krón", "014": "2Krón", "015": "Ezsd",
    "016": "Neh", "017": "Eszt", "018": "Jób", "019": "Zsolt", "020": "Péld",
    "021": "Préd", "022": "Én", "023": "Ézs", "024": "Jer", "025": "Sir",
    "026": "Ez", "027": "Dán", "028": "Hós", "029": "Jóel", "030": "Ámós",
    "031": "Abd", "032": "Jón", "033": "Mik", "034": "Náh", "035": "Hab",
    "036": "Sof", "037": "Hag", "038": "Zak", "039": "Mal",
}

JELENTESEK_HEADER = [
    "strong", "strong_kod", "lemma", "main_id", "lexid", "entry_kod",
    "domen_kod", "domen", "definicio_rovid", "definicio_hosszu", "glosszak",
    "megjegyzes",
]
REFERENCIAK_HEADER = ["lexid", "strong", "igehely", "szopozicio", "ref_kod"]
ANOMALIAK_HEADER = ["entry_id", "lemma", "tipus", "nyers_ertek", "allapot"]


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
    full_path = os.path.join(base_dir, HEBREW_DIC_RELPATH.replace("/", os.sep))
    if not os.path.isfile(full_path):
        print(f"HIBA: hiányzó fájl: {full_path}", file=sys.stderr)
        sys.exit(2)
    actual = sha256_file(full_path)
    if actual != HEBREW_DIC_SHA:
        print(
            f"HIBA: SHA-256 eltérés — {HEBREW_DIC_RELPATH}\n"
            f"  várt:   {HEBREW_DIC_SHA}\n"
            f"  kapott: {actual}",
            file=sys.stderr,
        )
        sys.exit(2)
    return full_path


def download_source():
    tmp = tempfile.mkdtemp(prefix="ubs_dbh_")
    tarball = os.path.join(tmp, "ubs.tar.gz")
    try:
        urllib.request.urlretrieve(UBS_URL, tarball)
        with tarfile.open(tarball) as tf:
            root_prefix = None
            for name in tf.getnames():
                root_prefix = name.split("/")[0]
                break
            member_name = f"{root_prefix}/{HEBREW_DIC_RELPATH}"
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


def parse_strong_codes(raw_list, entry_id, lemma, anomalies):
    valid = []
    for sc in (raw_list or []):
        if sc == "":
            continue
        m = STRONG_RE.match(sc)
        if not m:
            anomalies.append((entry_id, lemma, "ervenytelen_kod", sc))
            continue
        digits, _suffix = m.groups()
        strong = "H" + digits
        valid.append((strong, sc))
    if not valid:
        anomalies.append(
            (entry_id, lemma, "strong_nelkul",
             json.dumps(raw_list or [], ensure_ascii=False))
        )
    return valid


def extract_domains(lex_meaning):
    def nonempty(lst):
        return [d for d in (lst or []) if d.get("DomainCode")]

    subdomains = nonempty(lex_meaning.get("LEXSubDomains"))
    chosen = subdomains if subdomains else nonempty(lex_meaning.get("LEXDomains"))
    if not chosen:
        return [(EM_DASH, EM_DASH)]
    return [(d["DomainCode"], clean_text(d["Domain"])) for d in chosen]


def extract_en_sense(lex_senses):
    for sense in (lex_senses or []):
        if sense.get("LanguageCode") == "en":
            return sense
    return None


def extract_glossza(sense):
    if not sense:
        return EM_DASH
    glosses = []
    seen = set()
    for g in (sense.get("Glosses") or []):
        g_clean = clean_text(g)
        if g_clean and g_clean not in seen:
            seen.add(g_clean)
            glosses.append(g_clean)
    return "; ".join(glosses) if glosses else EM_DASH


def decode_ref(ref_kod):
    """14 jegyu LEXReferences-kod -> (igehely, szopozicio) vagy None. A
    konyvkod-tartomany (001-039) az OSZ-re szukitve -- ha a kod ezen kivul
    esik (pl. deuterokanonikus vagy NT-hivatkozas egy heber szocikkben),
    None-t ad vissza, a hivo dekodolasi anomaliakent naploz."""
    m = REF_RE.match(ref_kod)
    if not m:
        return None
    book_kod, fejezet, vers, pozicio = m.groups()
    konyv = BOOK_CODES.get(book_kod)
    if konyv is None:
        return None
    igehely = f"{konyv} {int(fejezet)}:{int(vers)}"
    return igehely, str(int(pozicio))


def process_dictionary(json_path):
    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)

    jelentes_rows = set()
    ref_rows = set()
    anomalies = []
    ref_decode_anomalies = []

    for e in entries:
        entry_id = e["MainId"]
        lemma = clean_text(e.get("Lemma"))
        raw_strong_codes = e.get("StrongCodes")
        strong_parts = parse_strong_codes(raw_strong_codes, entry_id, lemma, anomalies)
        if not strong_parts:
            continue

        meanings_count = 0
        for bf in (e.get("BaseForms") or []):
            for lm in (bf.get("LEXMeanings") or []):
                meanings_count += 1
                lexid = lm.get("LEXID", "")
                raw_entry_kod = lm.get("LEXEntryCode")
                entry_kod = clean_text(raw_entry_kod) if raw_entry_kod else EM_DASH
                sense = extract_en_sense(lm.get("LEXSenses"))
                definicio_rovid = clean_text(sense.get("DefinitionShort")) if sense else ""
                definicio_hosszu = clean_text(sense.get("DefinitionLong")) if sense else ""
                glosszak = extract_glossza(sense)
                megjegyzes = clean_text(sense.get("Comments")) if sense else ""
                domains = extract_domains(lm)

                for (strong, strong_kod) in strong_parts:
                    for (domen_kod, domen) in domains:
                        jelentes_rows.add((
                            strong, strong_kod, lemma, entry_id, lexid,
                            entry_kod, domen_kod, domen,
                            definicio_rovid or EM_DASH,
                            definicio_hosszu or EM_DASH,
                            glosszak,
                            megjegyzes or EM_DASH,
                        ))

                    for ref_kod in (lm.get("LEXReferences") or []):
                        decoded = decode_ref(ref_kod)
                        if decoded is None:
                            ref_decode_anomalies.append(
                                (entry_id, lemma, "ref_dekodolas_sikertelen_vagy_osz_kivuli", ref_kod)
                            )
                            continue
                        igehely, szopozicio = decoded
                        ref_rows.add((lexid, strong, igehely, szopozicio, ref_kod))

        if meanings_count == 0:
            anomalies.append((
                entry_id, lemma, "jelentes_nelkul",
                json.dumps(raw_strong_codes or [], ensure_ascii=False),
            ))

    return jelentes_rows, ref_rows, anomalies + ref_decode_anomalies, len(entries)


def write_tsv(path, header, rows, comment_lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for line in comment_lines:
            f.write(line + "\n")
        f.write("\t".join(header) + "\n")
        for row in sorted(rows):
            f.write("\t".join(row) + "\n")


def comment_lines_for(source_desc):
    return [
        "# GENERÁLT: eszkozok/ubs_dbh_import.py — kézzel nem szerkesztendő.",
        f"# forras: ubsicap/ubs-open-license @ {UBS_COMMIT} | {source_desc}",
        "# licenc: CC BY-SA 4.0 — © United Bible Societies; forrásmegjelölés: konkordancia/SDBH_SDGNT_README.md",
    ]


def src_desc(name, path):
    return f"{name} sha256={sha256_file(path)}"


ALLAPOT_MAP = {
    "strong_nelkul": "AZONOSITVA, NEM JAVITVA",
    "ervenytelen_kod": "AZONOSITVA, NEM JAVITVA",
    "jelentes_nelkul": "FORRASBAN_BEFEJEZETLEN",
    "ref_dekodolas_sikertelen_vagy_osz_kivuli": "AZONOSITVA, NEM JAVITVA",
}


def run_full(path):
    os.makedirs(KONKORDANCIA_DIR, exist_ok=True)
    jelentes_rows, ref_rows, anomalies, _n = process_dictionary(path)

    desc = src_desc("UBSHebrewDic-v0.9.2-en.JSON", path)

    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "UBS_DBH_jelentesek.tsv"),
        JELENTESEK_HEADER,
        jelentes_rows,
        comment_lines_for(desc),
    )
    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "UBS_DBH_referenciak.tsv"),
        REFERENCIAK_HEADER,
        ref_rows,
        comment_lines_for(desc),
    )

    all_anoms = [tuple(list(a) + [ALLAPOT_MAP[a[2]]]) for a in anomalies]
    write_tsv(
        os.path.join(KONKORDANCIA_DIR, "UBS_DBH_anomaliak.tsv"),
        ANOMALIAK_HEADER,
        all_anoms,
        comment_lines_for(desc),
    )

    print(f"jelentesek: {len(jelentes_rows)} sor")
    print(f"referenciak: {len(ref_rows)} sor")
    print(f"anomaliak: {len(all_anoms)} sor")


def main():
    parser = argparse.ArgumentParser(
        description="UBS heber szotar import -- jelentes- es hivatkozas-kivonat"
    )
    parser.add_argument("--letolt", action="store_true", help="forrás letöltése a rögzített UBS-commitról")
    parser.add_argument("--forras", metavar="KÖNYVTÁR", help="már kibontott dictionaries/ szülőkönyvtára")
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
            path, cleanup_dir = download_source()
        else:
            path = verify_and_locate(args.forras)
        run_full(path)
    finally:
        if cleanup_dir:
            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
