"""UBS-jelentés próba-hozzárendelés az elofordulasok.tsv ÚSZ-sorira.

Származtatott próba-jelentés — nem írja vissza az elofordulasok.tsv-t.
Lásd LEXV2_1_BRIEF.md V1.2.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT_DIR = os.path.join(REPO_ROOT, "adat")
KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")
NAPLOK_DIR = os.path.join(REPO_ROOT, "naplok")

ELOFORDULASOK_PATH = os.path.join(ADAT_DIR, "elofordulasok.tsv")
REFERENCIAK_PATH = os.path.join(KONKORDANCIA_DIR, "UBS_DNTG_referenciak.tsv")
JELENTESEK_PATH = os.path.join(KONKORDANCIA_DIR, "UBS_DNTG_jelentesek.tsv")
KIMENET_PATH = os.path.join(NAPLOK_DIR, "LEXV2_ubs_hozzarendeles_proba.tsv")

# ÚSZ-könyvek Károli-rövidítése (l. Konyv_normalizalo_tabla.tsv 41-67. sora
# / eszkozok/ubs_dntg_import.py BOOK_CODES).
NT_KONYVEK = {
    "Mt", "Mk", "Luk", "Ján", "ApCsel", "Róm", "1Kor", "2Kor", "Gal", "Ef",
    "Fil", "Kol", "1Thessz", "2Thessz", "1Tim", "2Tim", "Tit", "Filem",
    "Zsid", "Jak", "1Pét", "2Pét", "1Ján", "2Ján", "3Ján", "Júd", "Jel",
}

# "Zsid 7:1-28" -> könyv, fejezet, kezdő vers, záró vers (egyverses sornál
# a kezdő és záró vers egyezik)
IGEHELY_RE = re.compile(r'^(\S+)\s+(\d+):(\d+)(?:-(\d+))?$')

HEADER = ["id", "igehely", "strong", "lexid", "entry_kod", "glosszak", "egyertelmu", "megjegyzes"]


def read_tsv_rows(path):
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    lines = [ln for ln in lines if not ln.startswith("#")]
    header = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        if ln == "":
            continue
        rows.append(dict(zip(header, ln.split("\t"))))
    return rows


def parse_igehely(igehely):
    m = IGEHELY_RE.match(igehely)
    if not m:
        return None
    konyv, fejezet, v1, v2 = m.groups()
    if konyv not in NT_KONYVEK:
        return None
    v1 = int(v1)
    v2 = int(v2) if v2 else v1
    versek = [f"{konyv} {fejezet}:{v}" for v in range(v1, v2 + 1)]
    return konyv, versek


def load_elofordulasok_usz_sorok():
    rows = read_tsv_rows(ELOFORDULASOK_PATH)
    usz_sorok = []
    for r in rows:
        parsed = parse_igehely(r["igehely"])
        if parsed is None:
            continue
        _konyv, versek = parsed
        usz_sorok.append((r["id"], r["igehely"], r["strong"], versek))
    return usz_sorok


def build_ref_index(ref_rows):
    """igehely -> strong -> [(lexid, ref_kod), ...]"""
    idx = {}
    for r in ref_rows:
        idx.setdefault(r["igehely"], {}).setdefault(r["strong"], []).append(
            (r["lexid"], r["ref_kod"])
        )
    return idx


def build_jelentes_index(jelentes_rows):
    """(strong, lexid) -> (entry_kod, glosszak) — a domén-duplikátumok közül az elsőt tartja."""
    idx = {}
    for r in jelentes_rows:
        key = (r["strong"], r["lexid"])
        if key not in idx:
            idx[key] = (r["entry_kod"], r["glosszak"])
    return idx


def hozzarendel(usz_sorok, ref_idx, jelentes_idx):
    out_rows = []
    for (id_, igehely, strong_field, versek) in usz_sorok:
        is_range = len(versek) > 1
        strong_tokens = [s for s in strong_field.split("+") if s]

        if not strong_tokens:
            out_rows.append((
                id_, igehely, "", "", "", "", "",
                "nincs strong-token a sorban",
            ))
            continue

        for strong in strong_tokens:
            matches = []  # (lexid, ref_kod, igehely_talalt)
            for vers in versek:
                for (lexid, ref_kod) in ref_idx.get(vers, {}).get(strong, []):
                    matches.append((lexid, ref_kod, vers))

            distinct_lexids = sorted({m[0] for m in matches})

            if not distinct_lexids:
                ok = "a hivatkozott vers(ek)ben nincs UBS-referencia erre a Strong-kódra"
                if is_range:
                    ok += f" (tartomány: {len(versek)} vers)"
                out_rows.append((id_, igehely, strong, "", "", "", "", ok))
                continue

            egyertelmu = "igen" if (len(distinct_lexids) == 1 and not is_range) else "nem"
            for lexid in distinct_lexids:
                entry_kod, glosszak = jelentes_idx.get(
                    (strong, lexid), ("", "")
                )
                megjegyzes = ""
                if is_range:
                    megjegyzes = f"tartomány: {len(versek)} vers ({igehely})"
                if len(distinct_lexids) > 1:
                    extra = f"{len(distinct_lexids)} különböző jelentés a tartományban/versben"
                    megjegyzes = (megjegyzes + "; " + extra) if megjegyzes else extra
                out_rows.append((
                    id_, igehely, strong, lexid, entry_kod, glosszak,
                    egyertelmu, megjegyzes,
                ))
    return out_rows


def write_tsv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "# GENERÁLT: eszkozok/ubs_hozzarendeles.py — kézzel nem szerkesztendő.\n"
        )
        f.write(
            "# szarmaztatott proba-jelentes; nem kerul az elofordulasok.tsv-be (LEXV2_1_BRIEF.md G2)\n"
        )
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(row) + "\n")


def main():
    usz_sorok = load_elofordulasok_usz_sorok()
    ref_rows = read_tsv_rows(REFERENCIAK_PATH)
    jelentes_rows = read_tsv_rows(JELENTESEK_PATH)

    ref_idx = build_ref_index(ref_rows)
    jelentes_idx = build_jelentes_index(jelentes_rows)

    out_rows = hozzarendel(usz_sorok, ref_idx, jelentes_idx)
    write_tsv(KIMENET_PATH, HEADER, out_rows)

    n_usz = len(usz_sorok)
    n_out = len(out_rows)
    n_egyertelmu = sum(1 for r in out_rows if r[6] == "igen")
    n_nem_egyertelmu = sum(1 for r in out_rows if r[6] == "nem")
    n_nincs = sum(1 for r in out_rows if r[3] == "")
    print(f"ÚSZ-sor: {n_usz}")
    print(f"kimeneti sor: {n_out}")
    print(f"egyertelmu=igen: {n_egyertelmu}")
    print(f"egyertelmu=nem: {n_nem_egyertelmu}")
    print(f"nincs hozzárendelés (lexid üres): {n_nincs}")


if __name__ == "__main__":
    main()
