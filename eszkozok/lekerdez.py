#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lekerdez.py — a hétlépéses kutatási protokoll determinisztikus parancsai
(ATALAKITASI_TERV.md.md F2, 4.1, 4.3).

Minden parancs a saját provenienciáját írja ki utolsó sorként, szó szerint
másolható alakban az `adat/jeloltek.tsv` / `elofordulasok.tsv` proveniencia
mezőjébe (l. adat/SEMA.md 1.5). Nyers adat innen nem kerül a fő szál
kontextusába — csak ez a kimenet.

FONTOS: a proveniencia scope-jában soha nem `OT-full`, hanem `TAHOT-teljes`
(illetve `NT-teljes`) szerepel, amíg a TAHOT_kivonat.tsv lefedettségi rése
nincs véglegesen tisztázva (l. adat/SEMA.md 4., ATALAKITASI_TERV.md.md 9. pont
kockázat-táblája). A `TAHOT-teljes` azt jelenti: a kivonat egészére, nem az
Ószövetség kánonjának egészére vonatkozó állítás.
"""

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import csv
import datetime
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
KONK = ROOT / "konkordancia"
ADAT = ROOT / "adat"

# ---------------------------------------------------------------------------
# Segéd: időbélyeg, TSV-olvasás
# ---------------------------------------------------------------------------

def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M") + "Z"


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def read_tsv_skip_comments(path):
    """Néhány generált TSV (pl. grammatikai_strongok.tsv) '#'-tal kezdődő
    dokumentáló sorokkal indul a fejléc előtt."""
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))


# ---------------------------------------------------------------------------
# Könyvnév-normalizálás — adat/SEMA.md 1.1
# ---------------------------------------------------------------------------

_book_cache = None


def book_tables():
    global _book_cache
    if _book_cache is None:
        rows = read_tsv(KONK / "Konyv_normalizalo_tabla.tsv")
        step2hu, hu2step = {}, {}
        for r in rows:
            step = r["STEPBible-rövidítés"].strip()
            hu = r["Magyar rövidítés"].strip()
            step2hu[step] = hu
            hu2step[hu] = step
        _book_cache = (step2hu, hu2step)
    return _book_cache


IGEHELY_STEP_RE = re.compile(r"^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)$")


def parse_igehely(s):
    """'1Móz 3:16' vagy 'Gen.1.1' -> (magyar_konyv, fejezet, vers).

    A magyar alak (könyv-rövidítés + szóköz + fejezet:vers) könyvnevei
    számjeggyel is kezdődhetnek (1Móz, 2Krón stb.), ezért nem regex-szel,
    hanem az utolsó szóköz mentén választjuk szét — a fejezet:vers rész
    mindig a végén, számjegyekből áll.
    """
    s = s.strip()
    m = IGEHELY_STEP_RE.match(s)
    if m:
        step, ch, v = m.groups()
        step2hu, _ = book_tables()
        hu = step2hu.get(step)
        if hu is None:
            raise ValueError(f"ismeretlen STEPBible könyv-rövidítés: {step}")
        return (hu, int(ch), int(v))
    if " " in s and ":" in s:
        book, rest = s.rsplit(" ", 1)
        book = book.strip()
        if book and ":" in rest:
            ch_str, v_str = rest.split(":", 1)
            if ch_str.isdigit() and v_str.isdigit():
                return (book, int(ch_str), int(v_str))
    raise ValueError(f"nem elemezhető igehely: {s!r}")


def to_step(igehely_hu):
    """'1Móz 3:16' -> 'Gen.3.16' (a STEPBible-alakú datasetekhez)."""
    book, ch, v = parse_igehely(igehely_hu)
    _, hu2step = book_tables()
    step = hu2step.get(book)
    if step is None:
        raise ValueError(f"ismeretlen magyar könyv-rövidítés: {book}")
    return f"{step}.{ch}.{v}"


# ---------------------------------------------------------------------------
# Igehely-tartomány elemzés — a `gerinc` parancshoz
# ---------------------------------------------------------------------------

RANGE_CROSS_RE = re.compile(r"^(.+?)\s+(\d+):(\d+)-(\d+):(\d+)$")
RANGE_SPAN_RE = re.compile(r"^(.+?)\s+(\d+):(\d+)-(\d+)$")
RANGE_VERSE_RE = re.compile(r"^(.+?)\s+(\d+):(\d+)$")
RANGE_CHAPTER_RE = re.compile(r"^(.+?)\s+(\d+)$")


def parse_range(spec):
    spec = spec.strip()
    m = RANGE_CROSS_RE.match(spec)
    if m:
        book, c1, v1, c2, v2 = m.groups()
        return ("cross", book.strip(), int(c1), int(v1), int(c2), int(v2))
    m = RANGE_SPAN_RE.match(spec)
    if m:
        book, c, v1, v2 = m.groups()
        return ("span", book.strip(), int(c), int(v1), int(v2))
    m = RANGE_VERSE_RE.match(spec)
    if m:
        book, c, v = m.groups()
        return ("verse", book.strip(), int(c), int(v))
    m = RANGE_CHAPTER_RE.match(spec)
    if m:
        book, c = m.groups()
        return ("chapter", book.strip(), int(c))
    raise ValueError(f"nem elemezhető tartomány: {spec!r}")


def in_range(rng, book, ch, v):
    kind = rng[0]
    if kind == "chapter":
        return book == rng[1] and ch == rng[2]
    if kind == "verse":
        return book == rng[1] and ch == rng[2] and v == rng[3]
    if kind == "span":
        return book == rng[1] and ch == rng[2] and rng[3] <= v <= rng[4]
    if kind == "cross":
        _, b, c1, v1, c2, v2 = rng
        if book != b or ch < c1 or ch > c2:
            return False
        if ch == c1 and v < v1:
            return False
        if ch == c2 and v > v2:
            return False
        return True
    return False


# ---------------------------------------------------------------------------
# Dataset-betöltők (cache-elve, egy futáson belül egyszer olvasva)
# ---------------------------------------------------------------------------

_tahot_cache = None
_tagnt_cache = None
_gramm_cache = None
_tsk_cache = None
_karoli_kh_cache = None
_karoli_1908_cache = None


def load_tahot():
    global _tahot_cache
    if _tahot_cache is None:
        rows = read_tsv(KONK / "TAHOT_kivonat.tsv")
        for r in rows:
            r["_parsed"] = parse_igehely(r["Igehely"])
        _tahot_cache = rows
    return _tahot_cache


def load_tagnt():
    global _tagnt_cache
    if _tagnt_cache is None:
        rows = read_tsv(KONK / "TAGNT_kivonat.tsv")
        for r in rows:
            r["_parsed"] = parse_igehely(r["Igehely"])
        _tagnt_cache = rows
    return _tagnt_cache


def load_grammatikai_strongok():
    global _gramm_cache
    if _gramm_cache is None:
        rows = read_tsv_skip_comments(ADAT / "grammatikai_strongok.tsv")
        _gramm_cache = {r["strong"] for r in rows}
    return _gramm_cache


def load_tsk():
    global _tsk_cache
    if _tsk_cache is None:
        _tsk_cache = read_tsv(KONK / "TSK_kereszthivatkozasok.tsv")
    return _tsk_cache


def load_karoli_kh():
    global _karoli_kh_cache
    if _karoli_kh_cache is None:
        _karoli_kh_cache = read_tsv(KONK / "Karoli_kereszthivatkozasok.tsv")
    return _karoli_kh_cache


def load_karoli_1908():
    global _karoli_1908_cache
    if _karoli_1908_cache is None:
        rows = read_tsv(KONK / "Karoli_1908.tsv")
        _karoli_1908_cache = {r["Igehely"]: r["Károli-szöveg (teljes vers)"] for r in rows}
    return _karoli_1908_cache


def combined_rows():
    """(parsed_igehely, strong, forrasfajl) hármasok TAHOT + TAGNT-ből."""
    out = []
    for r in load_tahot():
        out.append((r["_parsed"], r["Strong-szám"], "TAHOT_kivonat.tsv"))
    for r in load_tagnt():
        out.append((r["_parsed"], r["Strong-szám"], "TAGNT_kivonat.tsv"))
    return out


# ---------------------------------------------------------------------------
# Parancsok
# ---------------------------------------------------------------------------

def cmd_gerinc(args):
    """1. lépés — gerinc-metszet: közös Strong-halmaz N szakasz között, grammatikai szűréssel."""
    if len(args.szakasz) < 2:
        print("Legalább két szakasz kell a metszethez.", file=sys.stderr)
        sys.exit(1)
    ranges = [parse_range(s) for s in args.szakasz]
    rows = combined_rows()
    per_range = []
    sources = set()
    for rng in ranges:
        s = set()
        for parsed, strong, src in rows:
            book, ch, v = parsed
            if in_range(rng, book, ch, v):
                s.add(strong)
                sources.add(src)
        per_range.append(s)

    intersection = set.intersection(*per_range) if per_range else set()
    gramm = load_grammatikai_strongok()
    kiszurve = sorted(s for s in intersection if s in gramm)
    marad = sorted(s for s in intersection if s not in gramm)

    print(f"# gerinc-metszet — {len(ranges)} szakasz")
    for spec, s in zip(args.szakasz, per_range):
        print(f"#   {spec}: {len(s)} egyedi Strong")
    print(f"# metszet (szűretlen): {len(intersection)}")
    print(f"# grammatikai szűrővel kiszűrve ({len(kiszurve)}): {','.join(kiszurve) if kiszurve else '(nincs)'}")
    print(f"# gerinc-jelölt (marad): {len(marad)}")
    for s in marad:
        print(s)

    prov = (f"scope=range:{'+'.join(args.szakasz)} | forras={'+'.join(sorted(sources))} "
            f"| n={len(marad)} | ts={ts()}")
    print(f"proveniencia: {prov}")


def cmd_scan(args):
    """3. lépés — teljes ÓSZ/ÚSZ scan egy Strong-számra."""
    strong = args.strong.strip().upper()
    if strong.startswith("H"):
        rows, src, scope = load_tahot(), "TAHOT_kivonat.tsv", "TAHOT-teljes"
    elif strong.startswith("G"):
        rows, src, scope = load_tagnt(), "TAGNT_kivonat.tsv", "TAGNT-teljes"
    else:
        print("A Strong-szám H vagy G előtaggal kezdődjön.", file=sys.stderr)
        sys.exit(1)

    if args.szakasz:
        rng = parse_range(args.szakasz)
        rows = [r for r in rows if in_range(rng, *r["_parsed"])]
        scope = f"range:{args.szakasz}"

    hits = [r for r in rows if r["Strong-szám"] == strong]
    igehelyek = sorted({r["Igehely"] for r in hits}, key=lambda s: parse_igehely(s))

    print(f"# scan {strong} — {len(igehelyek)} igehely, {len(hits)} szó-előfordulás")
    for ig in igehelyek:
        print(ig)

    prov = f"scope={scope} | forras={src} | strong={strong} | n={len(igehelyek)} | ts={ts()}"
    print(f"proveniencia: {prov}")


def cmd_kollokacio(args):
    """4. lépés — kollokáció: két Strong-szám együttes előfordulása egy versben."""
    a, b = args.strong_a.strip().upper(), args.strong_b.strip().upper()
    rows = combined_rows()
    byverse = defaultdict(set)
    sources = set()
    for parsed, strong, src in rows:
        byverse[parsed].add(strong)
        sources.add(src)

    talalatok = sorted(
        (parsed for parsed, strongs in byverse.items() if a in strongs and b in strongs)
    )
    print(f"# kollokáció {a} + {b} — {len(talalatok)} vers")
    for book, ch, v in talalatok:
        print(f"{book} {ch}:{v}")

    prov = (f"scope=TAHOT-teljes+TAGNT-teljes | forras={'+'.join(sorted(sources))} "
            f"| strong={a}+{b} | n={len(talalatok)} | ts={ts()}")
    print(f"proveniencia: {prov}")


def cmd_igealak(args):
    """5. lépés — igealak-szintű ellenőrzés: egy Strong minden ragozott alakja, emberi döntéshez."""
    strong = args.strong.strip().upper()
    if strong.startswith("H"):
        rows, src, scope = load_tahot(), "TAHOT_kivonat.tsv", "TAHOT-teljes"
    elif strong.startswith("G"):
        rows, src, scope = load_tagnt(), "TAGNT_kivonat.tsv", "TAGNT-teljes"
    else:
        print("A Strong-szám H vagy G előtaggal kezdődjön.", file=sys.stderr)
        sys.exit(1)

    hits = [r for r in rows if r["Strong-szám"] == strong]
    hits.sort(key=lambda r: r["_parsed"])

    print(f"# igealak-ellenőrzés {strong} — {len(hits)} szó-előfordulás")
    print("# igehely\tragozott_alak\tkiejtes\trovid_jelentes\tangol_tukorforditas")
    for r in hits:
        print(f"{r['Igehely']}\t{r['Ragozott alak']}\t{r['Kiejtés']}\t{r['Rövid jelentés']}\t{r['Angol tükörfordítás']}")
    print("# EMBERI DÖNTÉS: a fenti alakok binyan/igealak szerinti csoportosítása nem automatikus.")

    prov = f"scope={scope} | forras={src} | strong={strong} | n={len(hits)} | ts={ts()}"
    print(f"proveniencia: {prov}")


def _lxx_filename(magyar_konyv):
    mapping = {
        "1Móz": "Genezis", "2Móz": "Exodus", "3Móz": "Leviticus", "4Móz": "Numeri",
        "5Móz": "Deuteronomium", "Józs": "Jozsue", "Bír": "Birak", "Ruth": "Ruth",
        "1Sám": "Samuel_1", "2Sám": "Samuel_2", "1Kir": "Kiralyok_1", "2Kir": "Kiralyok_2",
        "1Krón": "Kronikak_1", "2Krón": "Kronikak_2", "Ezsd": "Ezsdras", "Neh": "Nehemias",
        "Eszt": "Eszter", "Jób": "Job", "Zsolt": "Zsoltarok", "Péld": "Peldabeszedek",
        "Préd": "Predikator", "Én": "Enekek_Eneke", "Ézs": "Ezsaias", "Jer": "Jeremias",
        "Sir": "Siralmak", "Ez": "Ezekiel", "Dán": "Daniel", "Hós": "Hoseas",
        "Jóel": "Joel", "Ámós": "Amos", "Abd": "Abdias", "Jón": "Jonas", "Mik": "Mikeas",
        "Náh": "Nahum", "Hab": "Habakuk", "Sof": "Sofonias", "Hag": "Aggeus",
        "Zak": "Zakarias", "Mal": "Malakias",
    }
    return mapping.get(magyar_konyv)


def cmd_lxx_hid(args):
    """6. lépés — LXX-híd: egy ÓSZ-igehely görög (LXX) megfelelője, és annak ÚSZ-előfordulásai."""
    igehely = args.igehely.strip()
    book, ch, v = parse_igehely(igehely)
    fname = _lxx_filename(book)
    if fname is None:
        print(f"Nincs LXX-kivonat ehhez a könyvhöz: {book}", file=sys.stderr)
        sys.exit(1)
    path = KONK / f"LXX_kivonat_{fname}.tsv"
    if not path.exists():
        print(f"Hiányzó LXX-fájl: {path}", file=sys.stderr)
        sys.exit(1)

    rows = read_tsv(path)
    hits = [r for r in rows if r["Igehely"] == igehely]
    print(f"# LXX-híd {igehely} — {len(hits)} görög szó-előfordulás")
    for r in hits:
        print(f"{r['Strong-szám']}\t{r['Görög szóalak']}\t{r.get('Morfológiai kód', '')}")

    tagnt = load_tagnt()
    strongok = sorted({r["Strong-szám"] for r in hits})
    print(f"# az LXX-Strongok ÚSZ-előfordulásai (híd-jelölt), max 10 versenként:")
    for s in strongok:
        nt_hits = sorted({r["Igehely"] for r in tagnt if r["Strong-szám"] == s},
                          key=lambda x: parse_igehely(x))
        print(f"  {s}: {len(nt_hits)} ÚSZ-vers — {', '.join(nt_hits[:10])}"
              + (" ..." if len(nt_hits) > 10 else ""))

    prov = (f"scope=range:{igehely} | forras={path.name}+TAGNT_kivonat.tsv "
            f"| n={len(hits)} | ts={ts()}")
    print(f"proveniencia: {prov}")


def cmd_tsk(args):
    """A5 — TSK-kereszthivatkozások lekérdezése egy igehelyre."""
    igehely = args.igehely.strip()
    rows = load_tsk()
    hits = [r for r in rows if r["Igehely"] == igehely]
    hits.sort(key=lambda r: -int(r["Votes"]))

    print(f"# TSK {igehely} — {len(hits)} kapcsolódó igehely")
    for r in hits:
        print(f"{r['Kapcsolódó igehely magyar megjelenítése']}\tVotes={r['Votes']}")

    prov = f"scope=range:{igehely} | forras=TSK_kereszthivatkozasok.tsv | n={len(hits)} | ts={ts()}"
    print(f"proveniencia: {prov}")


def cmd_karoli(args):
    """A5 — Károli-szöveg + Károli-KH lekérdezés egy igehelyre (4.7 — karoli_szo hozzárendeléshez)."""
    igehely = args.igehely.strip()
    karoli = load_karoli_1908()
    szoveg = karoli.get(igehely)
    if szoveg is None:
        print(f"Nincs Károli-szöveg ehhez: {igehely}", file=sys.stderr)
        sys.exit(1)
    print(f"# Károli 1908 — {igehely}")
    print(szoveg)

    try:
        step_key = to_step(igehely)
    except ValueError as e:
        step_key = None

    kh_rows = load_karoli_kh()
    kh_hits = [r for r in kh_rows if r["Igehely"] == step_key] if step_key else []
    print(f"# Károli-KH ({igehely}) — {len(kh_hits)} kapcsolódó igehely")
    for r in kh_hits:
        print(r["Kapcsolódó igehely magyar megjelenítése"])

    prov = (f"scope=range:{igehely} | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv "
            f"| n={len(kh_hits)} | ts={ts()}")
    print(f"proveniencia: {prov}")


def cmd_domen(args):
    """3. használat (4.3) — szemantikai domén lekérdezés (SDBH/SDGNT). Előfeltétel: import."""
    dataset_rows = read_tsv_skip_comments(ADAT / "datasetek.tsv")
    sdbh = [r for r in dataset_rows if r["dataset"] == "SDBH"]
    allapot = sdbh[0]["allapot"] if sdbh else "ismeretlen"
    if allapot != "elerheto":
        print(
            "A `domen` parancs előfeltétele (SDBH/SDGNT import) nem teljesült.\n"
            f"adat/datasetek.tsv szerint az SDBH állapota: {allapot!r}.\n"
            "Ez a NYITOTT_FELADATOK.md-ben rögzített nyitott tétel — l. "
            "\"SDBH / SDGNT import\". A parancs nem ad ki eredményt, mert az "
            "üres/hiányzó eredmény a helyes viselkedés (nincs helyettesítő adat "
            "kitalálva).",
            file=sys.stderr,
        )
        sys.exit(2)
    # Az importálás után ide kerül a tényleges lekérdezés (StrongCodes join).
    print("SDBH elérhető, de a domén-lekérdezés logikája még nincs implementálva.",
          file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog="lekerdez.py",
        description="Determinisztikus lekérdező CLI — ATALAKITASI_TERV.md.md F2.",
    )
    sub = p.add_subparsers(dest="parancs", required=True)

    sp = sub.add_parser("gerinc", help="1. lépés — gerinc-metszet N szakasz között")
    sp.add_argument("szakasz", nargs="+", help="pl. '1Móz 3' '1Móz 6:1-8'")
    sp.set_defaults(func=cmd_gerinc)

    sp = sub.add_parser("scan", help="3. lépés — teljes scan egy Strong-számra")
    sp.add_argument("strong")
    sp.add_argument("--szakasz", help="opcionális szűkítés egy tartományra")
    sp.set_defaults(func=cmd_scan)

    sp = sub.add_parser("kollokacio", help="4. lépés — két Strong együttes előfordulása egy versben")
    sp.add_argument("strong_a")
    sp.add_argument("strong_b")
    sp.set_defaults(func=cmd_kollokacio)

    sp = sub.add_parser("igealak", help="5. lépés — egy Strong minden ragozott alakja")
    sp.add_argument("strong")
    sp.set_defaults(func=cmd_igealak)

    sp = sub.add_parser("lxx-hid", help="6. lépés — egy ÓSZ-igehely LXX-megfelelője + ÚSZ-hidak")
    sp.add_argument("igehely")
    sp.set_defaults(func=cmd_lxx_hid)

    sp = sub.add_parser("tsk", help="TSK-kereszthivatkozások egy igehelyre")
    sp.add_argument("igehely")
    sp.set_defaults(func=cmd_tsk)

    sp = sub.add_parser("karoli", help="Károli-szöveg + Károli-KH egy igehelyre")
    sp.add_argument("igehely")
    sp.set_defaults(func=cmd_karoli)

    sp = sub.add_parser("domen", help="szemantikai domén (SDBH/SDGNT) — előfeltétel hiányzik")
    sp.add_argument("strong", nargs="?")
    sp.set_defaults(func=cmd_domen)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
