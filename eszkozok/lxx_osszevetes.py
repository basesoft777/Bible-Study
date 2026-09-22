"""V1.4 — a régi (studybible.info alapú) és az új (lxx-morph alapú) LXX-kivonat
összevetése a 8 motívum ÓSZ-igehelyein, a generátor ma is használt
lxx-hid lépése szerint (a verset a vers-cím, nem a héber Strong azonosítja).

Lásd LEXV2_1_BRIEF.md V1.4.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT_DIR = os.path.join(REPO_ROOT, "adat")
KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")
LXX_OS_DIR = os.path.join(KONKORDANCIA_DIR, "LXX_OS")
NAPLOK_DIR = os.path.join(REPO_ROOT, "naplok")

ELOFORDULASOK_PATH = os.path.join(ADAT_DIR, "elofordulasok.tsv")
KIMENET_PATH = os.path.join(NAPLOK_DIR, "LEXV2_lxx_osszevetes.tsv")

HEADER = ["id", "igehely", "strong", "regi_talalat", "uj_talalat", "uj_szoalak", "uj_lemma", "megjegyzes"]

# Károli-rövidítés -> régi LXX_kivonat_<fajlnev>.tsv szuffixum (l. eszkozok/lekerdez.py _lxx_filename)
REGI_LXX_FAJLNEV = {
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

IGEHELY_RE = re.compile(r'^(\S+)\s+(\d+):(\d+)(?:-(\d+))?$')


def normalize_strong(s):
    """A régi (LXX_kivonat, 'G1722') és az új (LXX_OS/GreekWordList, '1722')
    Strong-alak közös 'G####' formára hozása az összevetéshez."""
    if not s:
        return ""
    digits = re.sub(r'\D', '', s)
    if not digits:
        return ""
    return "G" + digits.zfill(4)


def read_tsv_rows(path, skip_comment_prefix="#"):
    with open(path, encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]
    lines = [ln for ln in lines if not ln.startswith(skip_comment_prefix)]
    header = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        if ln == "":
            continue
        rows.append(dict(zip(header, ln.split("\t"))))
    return rows


def load_motivum_ot_versek():
    rows = read_tsv_rows(ELOFORDULASOK_PATH)
    versek = []
    for r in rows:
        m = IGEHELY_RE.match(r["igehely"])
        if not m:
            continue
        book = m.group(1)
        if book not in REGI_LXX_FAJLNEV:
            continue  # ÚSZ-sor
        ch = int(m.group(2))
        v1 = int(m.group(3))
        v2 = int(m.group(4)) if m.group(4) else v1
        for v in range(v1, v2 + 1):
            versek.append((r["id"], f"{book} {ch}:{v}", book))
    return versek


def load_regi_index(book):
    fname = REGI_LXX_FAJLNEV.get(book)
    if fname is None:
        return {}
    path = os.path.join(KONKORDANCIA_DIR, f"LXX_kivonat_{fname}.tsv")
    if not os.path.isfile(path):
        return {}
    rows = read_tsv_rows(path, skip_comment_prefix="\0")  # nincs komment-sor ebben a fajlban
    idx = {}
    for r in rows:
        idx.setdefault(r["Igehely"], []).append((r["Strong-szám"], r["Görög szóalak"]))
    return idx


_UJ_CACHE = {}


def load_uj_index_all():
    """igehely_karoli -> [(strong, szoalak, lemma), ...] az összes LXX_OS fájlból."""
    if _UJ_CACHE:
        return _UJ_CACHE
    idx = {}
    for path in glob.glob(os.path.join(LXX_OS_DIR, "*.tsv")):
        rows = read_tsv_rows(path)
        for r in rows:
            ig = r.get("igehely_karoli", "")
            if not ig:
                continue
            idx.setdefault(ig, []).append((r["strong"], r["szoalak"], r["lemma"]))
    _UJ_CACHE.update(idx)
    return idx


def main():
    versek = load_motivum_ot_versek()
    uj_index = load_uj_index_all()

    regi_cache = {}
    out_rows = []
    stat = {"egyezik": 0, "csak_regi": 0, "csak_uj": 0, "nem_parosithato": 0}

    for (id_, igehely, book) in versek:
        if book not in regi_cache:
            regi_cache[book] = load_regi_index(book)
        regi_hits = regi_cache[book].get(igehely, [])
        uj_hits = uj_index.get(igehely, [])

        regi_strongs = {normalize_strong(s) for (s, _sz) in regi_hits if s}
        regi_strongs.discard("")
        uj_strongs = {normalize_strong(s) for (s, _sz, _l) in uj_hits if s}
        uj_strongs.discard("")

        if not regi_hits and not uj_hits:
            out_rows.append((id_, igehely, "", "nem", "nem", "", "", "nincs adat egyik kivonatban sem ehhez a igehelyhez"))
            stat["nem_parosithato"] += 1
            continue

        uj_by_strong = {}
        for (s, sz, l) in uj_hits:
            ns = normalize_strong(s)
            if ns and ns not in uj_by_strong:
                uj_by_strong[ns] = (sz, l)

        for strong in sorted(regi_strongs | uj_strongs):
            regi_ott = strong in regi_strongs
            uj_ott = strong in uj_strongs
            uj_szoalak, uj_lemma = uj_by_strong.get(strong, ("", ""))
            if regi_ott and uj_ott:
                megjegyzes = "egyezik"
                stat["egyezik"] += 1
            elif regi_ott and not uj_ott:
                if not uj_hits:
                    megjegyzes = "szamozas miatt nem parosithato (uj kivonatban nincs ez az igehely)"
                    stat["nem_parosithato"] += 1
                else:
                    megjegyzes = "csak regi"
                    stat["csak_regi"] += 1
            else:
                megjegyzes = "csak uj"
                stat["csak_uj"] += 1
            out_rows.append((
                id_, igehely, strong,
                "igen" if regi_ott else "nem",
                "igen" if uj_ott else "nem",
                uj_szoalak, uj_lemma, megjegyzes,
            ))

    os.makedirs(NAPLOK_DIR, exist_ok=True)
    with open(KIMENET_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write("# GENERÁLT: eszkozok/lxx_osszevetes.py — kézzel nem szerkesztendő.\n")
        f.write("\t".join(HEADER) + "\n")
        for row in out_rows:
            f.write("\t".join(row) + "\n")

    print(f"vizsgalt ÓSZ-vers: {len(versek)}")
    print(f"kimeneti sor: {len(out_rows)}")
    for k, v in stat.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
