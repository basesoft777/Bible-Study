#!/usr/bin/env python3
"""Ujrafelhasznalhato LXX-kivonat letoltő/parszoló szkript a studybible.info/LXX_WH forrasrol.

Hasznalat:
  python eszkozok/lxx_kivonat_fetch.py --konyv Psalms --fejezetek 16,110 --kimenet out.tsv
  python eszkozok/lxx_kivonat_fetch.py --konyv Genesis --fejezet-tol 1 --fejezet-ig 50 --kimenet out.tsv

Az URL-minta valtozatlan a `konkordancia/LXX_kivonat_Genezis_README.md`-ben
dokumentalthoz kepest: https://studybible.info/LXX_WH/<Konyv>%20<fejezetszam>
(fejezetenkent kulon oldal). A kimenet ugyanaz a 4 oszlopos sema, mint a
`konkordancia/LXX_kivonat_Genezis.tsv`:
  Igehely | Strong-szam | Gorog szoalak | Morfologiai kod

Csak Strong-szammal ellatott szavak kerulnek a kimenetbe (a forrasoldal
nehany szonal - pl. tulajdonnevek - nem ad Strong-szamot; ezek kimaradnak,
mivel a kimenet celja kifejezetten a Strong-taggelt konkordancia-kivonat).
"""
import argparse
import csv
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

NORMALIZO_TABLA = "konkordancia/Konyv_normalizalo_tabla.tsv"
USER_AGENT = "Mozilla/5.0 (compatible; lxx-kivonat-fetch/1.0; +bible-study-repo)"
KERES_KESLELTETES_MP = 1.0

# studybible.info a teljes angol (KJV-hagyomanyu) konyvnevet varja az URL-ben.
# A STEP-rovidites hidalja at ezt a Konyv_normalizalo_tabla.tsv magyar
# oszlopaihoz (l. a tablazat elso oszlopa).
ANGOL_NEV_TO_STEP = {
    "Genesis": "Gen", "Exodus": "Exo", "Leviticus": "Lev", "Numbers": "Num",
    "Deuteronomy": "Deu", "Joshua": "Jos", "Judges": "Jdg", "Ruth": "Rut",
    "1 Samuel": "1Sa", "2 Samuel": "2Sa", "1 Kings": "1Ki", "2 Kings": "2Ki",
    "1 Chronicles": "1Ch", "2 Chronicles": "2Ch", "Ezra": "Ezr",
    "Nehemiah": "Neh", "Esther": "Est", "Job": "Job", "Psalms": "Psa",
    "Proverbs": "Pro", "Ecclesiastes": "Ecc", "Song of Solomon": "Sng",
    "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam",
    "Ezekiel": "Ezk", "Daniel": "Dan", "Hosea": "Hos", "Joel": "Jol",
    "Amos": "Amo", "Obadiah": "Oba", "Jonah": "Jon", "Micah": "Mic",
    "Nahum": "Nam", "Habakkuk": "Hab", "Zephaniah": "Zep", "Haggai": "Hag",
    "Zechariah": "Zec", "Malachi": "Mal",
}

VERS_JELOLO_RE = re.compile(
    r'<span class="ref greek">(?:<a[^>]*>)?\s*(\d+)\s*(?:</a>)?</span>\s*</span>'
)
SZO_EGYSEG_RE = re.compile(
    r'<span class="unit">\s*<span class="strongs">(.*?)</span>\s*'
    r'<span class="tvm">(.*?)</span>\s*<span class="greek">(.*?)</span>\s*</span>',
    re.DOTALL,
)
STRONG_RE = re.compile(r'([GH]\d+)')
MORF_RE = re.compile(r'>([^<>]+)</a>')
ZAROJEL_PREFIX_RE = re.compile(r'^\[\d+:\d+\]\s*')


def normalize_strong(strong):
    """G86 -> G0086, H430 -> H0430 (4 szamjegyre padolva, l. eszkozok/merge_karoli_szofaj.py)."""
    m = re.match(r"^([HG])(\d+)([A-Za-z]*)$", strong)
    if not m:
        return strong
    letter, digits, suffix = m.groups()
    return f"{letter}{int(digits):04d}{suffix}"


def load_magyar_konyvnev(step_kod):
    with open(NORMALIZO_TABLA, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            if row and row[0] == step_kod:
                return row[1]
    return None


def fetch_html(konyv_angol, fejezet):
    url = "https://studybible.info/LXX_WH/" + urllib.parse.quote(f"{konyv_angol} {fejezet}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP hiba {konyv_angol} {fejezet} letoltesekor: {e}") from e


def parse_chapter(html, magyar_konyv, fejezet):
    """Egy fejezet HTML-jebol kinyeri a (Igehely, Strong-szam, Gorog szoalak, Morf kod) sorokat."""
    matches = list(VERS_JELOLO_RE.finditer(html))
    rows = []
    for i, m in enumerate(matches):
        vers_szam = m.group(1)
        block_start = m.end()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        block = html[block_start:block_end]
        igehely = f"{magyar_konyv} {fejezet}:{vers_szam}"
        for su in SZO_EGYSEG_RE.finditer(block):
            strongs_raw, tvm_raw, greek_raw = su.groups()
            strong_m = STRONG_RE.search(strongs_raw)
            if not strong_m:
                continue  # nincs Strong-szam -> kimarad a kivonatbol
            strong = normalize_strong(strong_m.group(1))
            morf_m = MORF_RE.search(tvm_raw)
            morf = morf_m.group(1).strip() if morf_m else tvm_raw.strip()
            szo = ZAROJEL_PREFIX_RE.sub("", greek_raw).strip()
            if not szo:
                continue
            rows.append((igehely, strong, szo, morf))
    return rows


def parse_fejezet_lista(args):
    if args.fejezetek:
        return [int(x) for x in args.fejezetek.split(",") if x.strip()]
    if args.fejezet_tol and args.fejezet_ig:
        return list(range(args.fejezet_tol, args.fejezet_ig + 1))
    raise SystemExit("Meg kell adni --fejezetek VAGY --fejezet-tol/--fejezet-ig parametert.")


def main():
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konyv", required=True, help="Angol konyvnev, pl. Psalms, Joel, Genesis")
    ap.add_argument("--fejezetek", help="Vesszovel elvalasztott fejezetlista, pl. 16,110")
    ap.add_argument("--fejezet-tol", type=int, dest="fejezet_tol")
    ap.add_argument("--fejezet-ig", type=int, dest="fejezet_ig")
    ap.add_argument("--kimenet", required=True, help="Kimeneti TSV fajl utvonala")
    args = ap.parse_args()

    step_kod = ANGOL_NEV_TO_STEP.get(args.konyv)
    if not step_kod:
        raise SystemExit(f"Ismeretlen konyvnev: {args.konyv!r} (nincs a ANGOL_NEV_TO_STEP tablaban)")
    magyar_konyv = load_magyar_konyvnev(step_kod)
    if not magyar_konyv:
        raise SystemExit(f"'{step_kod}' STEP-kod nem talalhato a {NORMALIZO_TABLA} fajlban")

    fejezetek = parse_fejezet_lista(args)

    all_rows = []
    for idx, fejezet in enumerate(fejezetek):
        if idx > 0:
            time.sleep(KERES_KESLELTETES_MP)
        print(f"Letoltes: {args.konyv} {fejezet} ...", file=sys.stderr)
        html = fetch_html(args.konyv, fejezet)
        rows = parse_chapter(html, magyar_konyv, fejezet)
        print(f"  -> {len(rows)} sor ({magyar_konyv} {fejezet})", file=sys.stderr)
        all_rows.extend(rows)

    with open(args.kimenet, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Igehely", "Strong-szám", "Görög szóalak", "Morfológiai kód"])
        writer.writerows(all_rows)

    print(f"Kesz: {len(all_rows)} adatsor -> {args.kimenet}", file=sys.stderr)


if __name__ == "__main__":
    main()
