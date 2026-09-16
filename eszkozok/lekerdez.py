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

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KONK = ROOT / "konkordancia"
ADAT = ROOT / "adat"

# ---------------------------------------------------------------------------
# Segéd: időbélyeg, TSV-olvasás
# ---------------------------------------------------------------------------

def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M") + "Z"


def read_tsv(path, skip_comments=False):
    """TSV-olvasás a csv modul nélkül — l. CLAUDE.md, „TSV-olvasás".

    A mezők szabad magyar szöveget tartalmaznak idézőjelekkel; a csv modul ezt
    idézés-szintaxisnak veszi, és a kapcsolodas oszlop 79 sorában leszedi a
    határoló " jeleket. Egyetlen mező sem tartalmaz tabot, a szétvágás egyértelmű.

    skip_comments=True: néhány generált TSV (pl. grammatikai_strongok.tsv)
    '#'-tal kezdődő dokumentáló sorokkal indul a fejléc előtt.
    """
    with open(path, encoding="utf-8") as f:
        sorok = [ln.rstrip("\n").rstrip("\r") for ln in f]
    if skip_comments:
        sorok = [s for s in sorok if not s.startswith("#")]
    sorok = [s for s in sorok if s.strip()]
    fejlec = sorok[0].split("\t")
    ki = []
    for i, s in enumerate(sorok[1:], start=2):
        mezok = s.split("\t")
        if len(mezok) != len(fejlec):
            raise ValueError(
                "%s %d. sor: %d mező a fejléc %d mezője helyett"
                % (path, i, len(mezok), len(fejlec)))
        ki.append(dict(zip(fejlec, mezok)))
    return ki


def read_tsv_skip_comments(path):
    return read_tsv(path, skip_comments=True)


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


_sdbh_domenek_cache = None
_sdgnt_domenek_cache = None


def load_sdbh_domenek():
    global _sdbh_domenek_cache
    if _sdbh_domenek_cache is None:
        _sdbh_domenek_cache = read_tsv_skip_comments(KONK / "SDBH_domenek.tsv")
    return _sdbh_domenek_cache


def load_sdgnt_domenek():
    global _sdgnt_domenek_cache
    if _sdgnt_domenek_cache is None:
        _sdgnt_domenek_cache = read_tsv_skip_comments(KONK / "SDGNT_domenek.tsv")
    return _sdgnt_domenek_cache


_sdbh_sdgnt_anomaliak_cache = None


def load_sdbh_sdgnt_anomaliak():
    global _sdbh_sdgnt_anomaliak_cache
    if _sdbh_sdgnt_anomaliak_cache is None:
        _sdbh_sdgnt_anomaliak_cache = read_tsv_skip_comments(KONK / "SDBH_SDGNT_anomaliak.tsv")
    return _sdbh_sdgnt_anomaliak_cache


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


_DOMEN_PLAIN_RE = re.compile(r'^[HG]\d{4}$')


def _domen_nyelv(strong):
    if strong[:1] in ("H", "A"):
        return "H"
    if strong[:1] == "G":
        return "G"
    return None


def _domen_match(rows, strong):
    if _DOMEN_PLAIN_RE.match(strong):
        return [r for r in rows if r["strong"] == strong]
    return [r for r in rows if r["strong_kod"] == strong]


_STRONG_PART_RE = re.compile(r'^([HAG])(\d{4})([a-f]?)$')


def _anomaly_valid_parts(nyers_ertek):
    """A nyers_ertek JSON-listájából kinyeri az érvényes Strong-részeket,
    ugyanazzal a szabállyal, mint az import (§2.2/1)."""
    try:
        raw_list = json.loads(nyers_ertek)
    except (ValueError, TypeError):
        return []
    parts = []
    for sc in raw_list:
        if sc == "":
            continue
        for part in sc.split("+"):
            if _STRONG_PART_RE.match(part):
                parts.append(part)
    return parts


def _anomaly_part_matches(part, strong):
    """Utótag nélküli H####/G#### bemenetnél normalizált illesztés, utótagos
    vagy A#### bemenetnél a részen, ahogy áll."""
    if _DOMEN_PLAIN_RE.match(strong):
        m = _STRONG_PART_RE.match(part)
        prefix, digits, _suffix = m.groups()
        normalized = ("H" if prefix in ("H", "A") else "G") + digits
        return normalized == strong
    return part == strong


def _matching_jelentes_nelkul(anom_rows, dataset_name, strong):
    matches = []
    for r in anom_rows:
        if r["szotar"] != dataset_name or r["tipus"] != "jelentes_nelkul":
            continue
        parts = _anomaly_valid_parts(r["nyers_ertek"])
        if any(_anomaly_part_matches(p, strong) for p in parts):
            matches.append(r)
    return matches


def _print_anomaly_warnings(dataset_name, matches):
    for r in matches:
        print(f"# figyelem: elemzetlen {dataset_name}-bejegyzés illeszkedik — "
              f"{r['entry_id']} {r['lemma']} {r['nyers_ertek']}")
    if matches:
        print("# (a forrásban szerepel, de jelentés-elemzés és domén nélkül: "
              "SDBH_SDGNT_anomaliak.tsv, jelentes_nelkul — nem negatív lelet)")


def cmd_domen(args):
    """3. használat (4.3) — szemantikai domén lekérdezés (SDBH/SDGNT): mező-tágítás 1 Stronggal, elhatárolás 2-vel."""
    strongok = [s.strip() for s in args.strong]
    if len(strongok) > 2:
        print("A `domen` legfeljebb két Strong-kódot fogad el.", file=sys.stderr)
        sys.exit(1)

    nyelvek = {_domen_nyelv(s) for s in strongok}
    if None in nyelvek or len(nyelvek) > 1:
        print("Vegyes nyelvű vagy ismeretlen előtagú Strong-kód(ok) — a `domen` "
              "csak azonos nyelvű (H/A vagy G) argumentumot fogad el.", file=sys.stderr)
        sys.exit(1)
    nyelv = nyelvek.pop()

    dataset_name = "SDBH" if nyelv == "H" else "SDGNT"
    dataset_rows = read_tsv_skip_comments(ADAT / "datasetek.tsv")
    ds = [r for r in dataset_rows if r["dataset"] == dataset_name]
    allapot = ds[0]["allapot"] if ds else "ismeretlen"
    if allapot != "elerheto":
        print(
            f"A `domen` parancs előfeltétele ({dataset_name} import) nem teljesült.\n"
            f"adat/datasetek.tsv szerint a {dataset_name} állapota: {allapot!r}.\n"
            "A parancs nem ad ki eredményt, mert az üres/hiányzó eredmény a helyes "
            "viselkedés (nincs helyettesítő adat kitalálva).",
            file=sys.stderr,
        )
        sys.exit(2)

    if dataset_name == "SDBH":
        rows = load_sdbh_domenek()
        scope, forras = "SDBH-v0.9.2", "SDBH_domenek.tsv+SDBH_SDGNT_anomaliak.tsv"
    else:
        rows = load_sdgnt_domenek()
        scope, forras = "SDGNT-v1.1", "SDGNT_domenek.tsv+SDBH_SDGNT_anomaliak.tsv"

    anom_rows = load_sdbh_sdgnt_anomaliak()

    if len(strongok) == 1:
        strong = strongok[0]
        hits = _domen_match(rows, strong)
        matches = _matching_jelentes_nelkul(anom_rows, dataset_name, strong)
        domenkodok = sorted({r["domen_kod"] for r in hits if r["domen_kod"] != "—"})
        n = len(domenkodok)

        if not hits:
            if matches:
                print(f"# domen {strong} — nincs elemzett {dataset_name}-bejegyzés")
                _print_anomaly_warnings(dataset_name, matches)
            else:
                print(f"# domen {strong} — nincs {dataset_name}-bejegyzés "
                      "(a szótár nem teljes: hiányzó bejegyzés nem negatív lelet)")
            prov = f"scope={scope} | forras={forras} | strong={strong} | n=0 | ts={ts()}"
            print(f"proveniencia: {prov}")
            sys.exit(0)

        print(f"# domen {strong} — {len(hits)} jelentés-egység, {n} domén")
        _print_anomaly_warnings(dataset_name, matches)
        for r in sorted(hits, key=lambda r: (r["lexid"], r["domen_kod"])):
            domen_label = r["domen"] if r["domen_kod"] != "—" else "domén nélkül"
            print(f"{r['strong_kod']}\t{r['nyelv']}\t{r['lemma']}\t{r['lexid']}\t"
                  f"{r['glossza']}\t{r['domen_kod']}\t{domen_label}")

        queried_strongs = {r["strong"] for r in hits}
        for domen_kod in domenkodok:
            domain_rows = [r for r in rows if r["domen_kod"] == domen_kod]
            domen_label = domain_rows[0]["domen"] if domain_rows else ""
            all_strongs = sorted({r["strong"] for r in domain_rows})
            print(f"## {domen_kod} {domen_label} ({len(all_strongs)} Strong)")
            tarsak = sorted(s for s in all_strongs if s not in queried_strongs)
            for tars in tarsak:
                glosszak = sorted({r["glossza"] for r in domain_rows if r["strong"] == tars})
                print(f"{tars}\t{'; '.join(glosszak)}")

        prov = f"scope={scope} | forras={forras} | strong={strong} | n={n} | ts={ts()}"
        print(f"proveniencia: {prov}")
        sys.exit(0)

    # elhatárolás — két Strong
    strong_a, strong_b = strongok
    hits_a = _domen_match(rows, strong_a)
    hits_b = _domen_match(rows, strong_b)
    matches_a = _matching_jelentes_nelkul(anom_rows, dataset_name, strong_a)
    matches_b = _matching_jelentes_nelkul(anom_rows, dataset_name, strong_b)
    _print_anomaly_warnings(dataset_name, matches_a)
    _print_anomaly_warnings(dataset_name, matches_b)

    kodok_a = {r["domen_kod"] for r in hits_a if r["domen_kod"] != "—"}
    kodok_b = {r["domen_kod"] for r in hits_b if r["domen_kod"] != "—"}
    kozos = sorted(kodok_a & kodok_b)
    n = len(kozos)

    if not kozos:
        print("# nincs közös domén")
        prov = (f"scope={scope} | forras={forras} | strong={strong_a}+{strong_b} "
                f"| n=0 | ts={ts()}")
        print(f"proveniencia: {prov}")
        sys.exit(0)

    print(f"# domen {strong_a} {strong_b} — {n} közös domén")
    for domen_kod in kozos:
        domain_rows = [r for r in rows if r["domen_kod"] == domen_kod]
        domen_label = domain_rows[0]["domen"] if domain_rows else ""
        print(f"## {domen_kod} {domen_label}")
        for label, hits in ((strong_a, hits_a), (strong_b, hits_b)):
            for r in sorted(hits, key=lambda r: r["lexid"]):
                if r["domen_kod"] == domen_kod:
                    print(f"{label}\t{r['lexid']}\t{r['glossza']}")

    prov = (f"scope={scope} | forras={forras} | strong={strong_a}+{strong_b} "
            f"| n={n} | ts={ts()}")
    print(f"proveniencia: {prov}")


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

    sp = sub.add_parser("domen", help="szemantikai domén (SDBH/SDGNT) — mező-tágítás 1 Stronggal, elhatárolás 2-vel")
    sp.add_argument("strong", nargs="+")
    sp.set_defaults(func=cmd_domen)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
