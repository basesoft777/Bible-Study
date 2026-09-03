#!/usr/bin/env python3
"""
Kockazat-szuro szkript a 18 auditalatlan bovitett tanulmanyra (1Moz 2:4-7 -- 16).
Kiszamitja a 4 kockazati jelzot minden kulcsszora, es Markdown riportot general.

Futtatas: python eszkozok/kockazat_szures_18_tanulmany.py
Kimenet:  sablonok/Kockazat_szures_riport_2026-09-03.md
"""

import re
import csv
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
GEN_DIR = ROOT / "genezis"
KONK_DIR = ROOT / "konkordancia"
OUT_PATH = ROOT / "sablonok" / "Kockazat_szures_riport_2026-09-03.md"

STUDY_FILES = [
    "1Moz_2v4-7_bovitett.md",
    "1Moz_2v8-25_bovitett.md",
    "1Moz_3v1-6_bovitett.md",
    "1Moz_3v7-24_bovitett.md",
    "1Moz_4v1-24_bovitett.md",
    "1Moz_4v25-5v32_bovitett.md",
    "1Moz_6v1-8_bovitett.md",
    "1Moz_6v9-22_bovitett.md",
    "1Moz_7v1-24_bovitett.md",
    "1Moz_8v1-22_bovitett.md",
    "1Moz_9v1-17_bovitett.md",
    "1Moz_9v18-29_bovitett.md",
    "1Moz_10v1-11v32_bovitett.md",
    "1Moz_12v1-20_bovitett.md",
    "1Moz_13v1-18_bovitett.md",
    "1Moz_14_bovitett.md",
    "1Moz_15_bovitett.md",
    "1Moz_16_bovitett.md",
]

NT_BOOKS = {
    "1Ján", "1Kor", "1Pét", "1Thessz", "1Tim", "2Ján", "2Kor", "2Pét",
    "2Thessz", "2Tim", "3Ján", "ApCsel", "Ef", "Fil", "Filem", "Gal",
    "Jak", "Jel", "Ján", "Júd", "Kol", "Luk", "Mk", "Mt", "Róm", "Tit", "Zsid",
}

STRONG_RE = re.compile(r"H\d+")
GREEK_STRONG_RE = re.compile(r"G\d+")


# ---------------------------------------------------------------------------
# Konkordancia-adatok betoltese
# ---------------------------------------------------------------------------

def load_strong_dict():
    """Strong_szotar.tsv -> {H szam: {szoto, gyok, jelentes}}"""
    d = {}
    with open(KONK_DIR / "Strong_szotar.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 6:
                continue
            code, szoto, kiejtes, szofaj, gyok, jelentes = row[:6]
            d[code] = {"szoto": szoto, "gyok": gyok, "jelentes": jelentes}
    return d


def load_tbesh_dict():
    """TBESH.txt -> {H szam: elso Meaning mezo (a G-vegzodesu alapbejegyzes)}"""
    d = {}
    with open(KONK_DIR / "TBESH.txt", encoding="utf-8-sig") as f:
        lines = f.readlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("eStrong#\tdStrong"):
            start = i + 1
            break
    if start is None:
        return d
    for line in lines[start:]:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 8:
            continue
        estrong = parts[0].strip()
        meaning = parts[7]
        if estrong and estrong not in d and re.fullmatch(r"H\d+", estrong):
            d[estrong] = meaning
    return d


def count_senses_tbesh(meaning):
    """Szamolja a top-szintu jelentes-agakat (pl. '1) ...', nem '1a) ...')."""
    segments = meaning.split("<br>")
    toplevel = [s for s in segments if re.match(r"^\s*\d+\)", s)]
    return len(toplevel)


def load_bdb_dict():
    """BDB_teljes_unabridged.tsv -> {H szam: Teljes_szocikk} (tartalek)."""
    d = {}
    path = KONK_DIR / "BDB_teljes_unabridged.tsv"
    if not path.exists():
        return d
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 3:
                continue
            padded, eredeti, szocikk = row[0], row[1], row[2]
            code = padded.strip()
            if code and re.fullmatch(r"H\d+", code) and code not in d:
                d[code] = szocikk
    return d


def count_senses_bdb(text):
    """Kozelito heurisztika: '; N ' vagy '. N ' vagy sor elejen 'N ' mintak, N=1-9(9)."""
    matches = re.findall(r"(?:^|[;.—]\s)([1-9][0-9]?)\s(?=[a-zà-ž])", text)
    nums = sorted(set(int(m) for m in matches if int(m) <= 12))
    return len(nums)


def load_lxx_genesis():
    """LXX_kivonat_Genezis.tsv -> {Igehely (pl. '1Móz 2:7'): set(G szamok)}"""
    d = defaultdict(set)
    with open(KONK_DIR / "LXX_kivonat_Genezis.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            verse, strong = row[0], row[1]
            if GREEK_STRONG_RE.fullmatch(strong.strip()):
                d[verse.strip()].add(strong.strip())
    return d


def load_tagnt():
    """TAGNT_kivonat.tsv -> ({Igehely: set(G szamok)}, {G szam: globalis elofordulas-szam})"""
    by_verse = defaultdict(set)
    global_freq = defaultdict(int)
    with open(KONK_DIR / "TAGNT_kivonat.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            verse, strong = row[0].strip(), row[1].strip()
            if GREEK_STRONG_RE.fullmatch(strong):
                by_verse[verse].add(strong)
                global_freq[strong] += 1
    return by_verse, global_freq


def load_tahot_occurrences():
    """TAHOT_kivonat.tsv -> {H szam: [Igehely, ...]} (osszes ELOFORDULAS)"""
    d = defaultdict(list)
    with open(KONK_DIR / "TAHOT_kivonat.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            verse, strong = row[0].strip(), row[1].strip()
            if STRONG_RE.fullmatch(strong):
                d[strong].append(verse)
    return d


def load_tagnt_occurrences():
    """TAGNT_kivonat.tsv -> {G szam: [Igehely, ...]} (osszes ELOFORDULAS, gorog kulcsszavakhoz)"""
    d = defaultdict(list)
    with open(KONK_DIR / "TAGNT_kivonat.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            verse, strong = row[0].strip(), row[1].strip()
            if GREEK_STRONG_RE.fullmatch(strong):
                d[strong].append(verse)
    return d


# ---------------------------------------------------------------------------
# Tanulmany-parszolas
# ---------------------------------------------------------------------------

def extract_section(text, heading_prefix, next_prefix="## "):
    """Kivagja a szakaszt a heading_prefix-tol a kovetkezo '## '-ig."""
    idx = text.find(heading_prefix)
    if idx == -1:
        return None
    rest = text[idx + len(heading_prefix):]
    m = re.search(r"\n## ", rest)
    if m:
        return rest[:m.start()]
    return rest


def parse_keyword_table(section2_text):
    """
    Visszaadja: (kulcsszavak listaja: [{vers, szo, strongs:[...]}, ...], parse_ok: bool)
    A tablazat oszlopai fejlecbol azonositva (Vers / Strong / Szo).
    """
    if section2_text is None:
        return [], False

    lines = section2_text.splitlines()
    table_lines = [ln for ln in lines if ln.strip().startswith("|")]
    if not table_lines:
        return [], False

    header_cells = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
    header_lower = [c.lower() for c in header_cells]

    vers_idx = next((i for i, c in enumerate(header_lower) if "vers" in c), None)
    strong_idx = next((i for i, c in enumerate(header_lower) if "strong" in c), None)
    word_idx = next(
        (i for i, c in enumerate(header_lower) if ("héber" in c or "szó" in c) and "strong" not in c),
        None,
    )

    if vers_idx is None or strong_idx is None:
        return [], False

    keywords = []
    parse_ok = True
    for ln in table_lines[1:]:
        stripped = ln.strip().strip("|")
        if re.fullmatch(r"[\s\-:|]*", stripped):
            continue
        cells = [c.strip() for c in stripped.split("|")]
        if len(cells) <= max(vers_idx, strong_idx):
            parse_ok = False
            continue
        vers_cell = cells[vers_idx]
        strong_cell = cells[strong_idx]
        word_cell = cells[word_idx] if word_idx is not None and word_idx < len(cells) else ""
        strongs = STRONG_RE.findall(strong_cell)
        if not strongs:
            continue
        keywords.append({"vers_raw": vers_cell, "szo": word_cell, "strongs": strongs})
    return keywords, parse_ok


def normalize_verse(vers_raw, filename):
    """
    Igyekszik '1Móz X:Y' formatumu Igehely-kulcsot eloallitani.
    Ha a vers_raw mar tartalmaz ':'-t, ugy hasznaljuk (elso resz, ha tartomany).
    Ha csak csupasz szam, a fajlnevbol probaljuk kitalalni a fejezetet.
    """
    vers_raw = vers_raw.strip()
    m = re.match(r"^(\d+):(\d+)", vers_raw)
    if m:
        return f"1Móz {m.group(1)}:{m.group(2)}"
    m2 = re.match(r"^(\d+)$", vers_raw)
    if m2:
        chap_m = re.search(r"_(\d+)v", filename)
        if chap_m:
            return f"1Móz {chap_m.group(1)}:{m2.group(1)}"
    return None


REF_PATTERN = r"[1-3]?[A-ZÁÉÍÓÖŐÚÜŰ][a-zA-ZÀ-ɏ]*\s\d+:\d+(?:-\d+)?"


def extract_ref_blocks(full_text):
    """
    Az osszes '> 🔗 ...' sorbol kinyeri a hivatkozas-szoveget. Ket formatumot ismer fel:
      A) '> 🔗 ↔ **Ref** *(...)*'                (bold hivatkozas a sor elejen)
      B) '> 🔗 "idezet..." (Ref, Karoli)'         (zarojeles hivatkozas a sor vegen)
      C) '> 🔗 *Ref* (kulcsszó: ...)'             (dolt hivatkozas a sor elejen)
      D) '> 🔗 Ref — "idezet..."'                 (sima szoveges hivatkozas a sor elejen)
    Altalanos strategia: a 🔗-t tartalmazo soron az elso 'Konyv fej:vers' mintat vesszuk —
    ez minden ismert formatumnal a tenyleges hivatkozas, mert az idezett szoveg maga
    nem tartalmaz ilyen mintat.
    """
    refs = []
    for line in full_text.splitlines():
        if "🔗" not in line:
            continue
        m = re.search(REF_PATTERN, line)
        if m:
            refs.append(m.group(0).strip())
    return refs


def extract_all_bold_refs(full_text):
    """Az egesz dokumentumban minden '**Konyv fejezet:vers[-vers]**' mintat kinyer."""
    pattern = re.compile(r"\*\*(" + REF_PATTERN + r")\*\*")
    return pattern.findall(full_text)


def parse_verse_ref(ref):
    """
    'Jób 10:8-9' -> ('Jób', [8,9], 10)  egyszerusitve csak azonos fejezeten beluli tartomanyt kezel.
    Visszaad: (konyv, fejezet, [versek]) vagy None, ha nem parszolhato egyszeruen.
    """
    m = re.match(r"^([1-3]?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű.]+)\s(\d+):(\d+)(?:-(\d+))?$", ref.strip())
    if not m:
        return None
    book, chap, v1, v2 = m.groups()
    chap = int(chap)
    v1 = int(v1)
    v2 = int(v2) if v2 else v1
    return book, chap, list(range(v1, v2 + 1))


def verse_keys(book, chap, verses):
    return [f"{book} {chap}:{v}" for v in verses]


# ---------------------------------------------------------------------------
# Jelzo-szamitas
# ---------------------------------------------------------------------------

def jelzo1_origin(keywords, full_text, strong_dict):
    """Origin-lanc-kockazat: hivatkozott H-szam, amit a study sehol nem emlit."""
    flagged = []
    seen_codes = set(re.findall(r"H\d+", full_text))
    for kw in keywords:
        for code in kw["strongs"]:
            info = strong_dict.get(code)
            if not info:
                continue
            gyok = info["gyok"]
            refs = [c for c in STRONG_RE.findall(gyok) if c != code]
            for ref_code in refs:
                ref_word = strong_dict.get(ref_code, {}).get("szoto", "")
                mentioned = (ref_code in seen_codes) or (ref_word and ref_word in full_text)
                if not mentioned:
                    flagged.append((code, kw["szo"], ref_code))
    return flagged


def jelzo2_polisemia(keywords, tbesh_dict, bdb_dict):
    """Poliszemia-kockazat: jelentes-agak szama kulcsszavankent."""
    results = []
    for kw in keywords:
        for code in kw["strongs"]:
            if code in tbesh_dict:
                n = count_senses_tbesh(tbesh_dict[code])
                src = "TBESH"
            elif code in bdb_dict:
                n = count_senses_bdb(bdb_dict[code])
                src = "BDB (közelítő)"
            else:
                n = None
                src = "nincs adat"
            results.append((code, kw["szo"], n, src))
    return results


STOPWORD_FREQ_THRESHOLD = 800  # e felett a globalis NT-elofordulas nagy eselllyel nyelvtani "ragaszto"
# szo (kai/and, ho/the, de/but, autou/his, hoti/that, gar/for, stb.) -- ezeket a piros zaszlo
# eldontesenel kizarjuk, kulonben a metszet szinte SOHA nem lenne ures, es a jelzo hasznalhatatlan
# lenne (lasd Modszertan/Korlatok).


def jelzo3_lxx(keywords, refs, filename, lxx_genesis, tagnt_by_verse, tagnt_global_freq):
    """Kereszthivatkozas/LXX-kockazat: piros zaszlo + kiaknazatlan ritka szo."""
    gen_verse_keys = set()
    for kw in keywords:
        vk = normalize_verse(kw["vers_raw"], filename)
        if vk:
            gen_verse_keys.add(vk)

    gen_greek = set()
    for vk in gen_verse_keys:
        gen_greek |= lxx_genesis.get(vk, set())

    red_flags = []
    opportunities = []
    study_strongs = set()
    for kw in keywords:
        study_strongs.update(kw["strongs"])

    for ref in refs:
        parsed = parse_verse_ref(ref)
        if not parsed:
            continue
        book, chap, verses = parsed
        if book not in NT_BOOKS:
            continue
        nt_keys = verse_keys(book, chap, verses)
        nt_greek = set()
        for k in nt_keys:
            nt_greek |= tagnt_by_verse.get(k, set())
        if not nt_greek:
            continue  # nincs adat erre a versre, nem ertekelheto
        intersection = gen_greek & nt_greek
        content_intersection = {
            g for g in intersection
            if tagnt_global_freq.get(g, 0) <= STOPWORD_FREQ_THRESHOLD
        }
        if not content_intersection:
            red_flags.append(ref)
        else:
            for g in content_intersection:
                freq = tagnt_global_freq.get(g, 0)
                if freq and freq < 200 and g not in study_strongs:
                    opportunities.append((ref, g, freq))
    return red_flags, opportunities, bool(gen_verse_keys)


def jelzo4_teljes_elofordulas(keywords, full_text, tahot_occ, tagnt_occ, refs):
    """Teljes-elofordulas-res: sosem idezett elofordulasok szama kulcsszavankent."""
    covered_refs = set(extract_all_bold_refs(full_text)) | set(refs)
    covered_norm = set()
    for r in covered_refs:
        parsed = parse_verse_ref(r)
        if parsed:
            book, chap, verses = parsed
            covered_norm.update(verse_keys(book, chap, verses))

    results = []
    for kw in keywords:
        vk = normalize_verse(kw["vers_raw"], "")
        for code in kw["strongs"]:
            occ = tahot_occ.get(code) if code.startswith("H") else tagnt_occ.get(code)
            occ = occ or []
            occ_set = set(occ)
            if vk:
                covered_norm_local = covered_norm | {vk}
            else:
                covered_norm_local = covered_norm
            remaining = occ_set - covered_norm_local
            results.append((code, kw["szo"], len(occ_set), len(remaining)))
    return results


# ---------------------------------------------------------------------------
# Fo feldolgozas
# ---------------------------------------------------------------------------

def process_study(filename, strong_dict, tbesh_dict, bdb_dict,
                   lxx_genesis, tagnt_by_verse, tagnt_global_freq,
                   tahot_occ, tagnt_occ):
    path = GEN_DIR / filename
    full_text = path.read_text(encoding="utf-8")

    section2 = extract_section(full_text, "## 2. Eredeti nyelvi szöveg")
    keywords, parse_ok = parse_keyword_table(section2)

    refs = extract_ref_blocks(full_text)

    j1 = jelzo1_origin(keywords, full_text, strong_dict)
    j2 = jelzo2_polisemia(keywords, tbesh_dict, bdb_dict)
    j3_red, j3_opp, j3_has_verse = jelzo3_lxx(
        keywords, refs, filename, lxx_genesis, tagnt_by_verse, tagnt_global_freq
    )
    j4 = jelzo4_teljes_elofordulas(keywords, full_text, tahot_occ, tagnt_occ, refs)

    return {
        "filename": filename,
        "keywords": keywords,
        "parse_ok": parse_ok,
        "refs": refs,
        "j1": j1,
        "j2": j2,
        "j3_red": j3_red,
        "j3_opp": j3_opp,
        "j3_has_verse": j3_has_verse,
        "j4": j4,
    }


def summarize_impression(res):
    """Szoveges 1-2 mondatos indoklas + Magas/Kozepes/Alacsony besorolas."""
    reasons = []
    level = "Alacsony"

    if res["j1"]:
        codes = sorted(set(f"{c}→{rc}" for c, _, rc in res["j1"]))
        reasons.append(f"{len(res['j1'])} kiaknázatlan Origin-lánc-hivatkozás ({', '.join(codes[:3])}{'...' if len(codes) > 3 else ''})")
        level = "Közepes"

    if res["j3_red"]:
        reasons.append(f"{len(res['j3_red'])} NT-idézet LXX-metszete üres (lehetséges hamis pozitív kereszthivatkozás: {', '.join(res['j3_red'][:2])})")
        level = "Magas"

    high_poly = [c for c, szo, n, src in res["j2"] if n and n >= 4]
    if high_poly:
        reasons.append(f"{len(high_poly)} kulcsszó erősen poliszémikus (4+ jelentés-ág)")
        if level != "Magas":
            level = "Közepes"

    big_gaps = [c for c, szo, total, rem in res["j4"] if rem >= 15]
    if big_gaps:
        reasons.append(f"{len(big_gaps)} kulcsszónál 15+ soha nem idézett előfordulás maradt")

    if res["j3_opp"]:
        reasons.append(f"{len(res['j3_opp'])} kiaknázatlan ritka LXX/NT-szó a metszetben")

    if not res["parse_ok"] or not res["keywords"]:
        reasons.append("a kulcsszó-táblázat kinyerése részben vagy teljesen sikertelen volt — az alábbi jelzők hiányosak")
        level = "Közepes" if level == "Alacsony" else level

    if not reasons:
        reasons.append("egyik jelző sem mutatott érdemi kiaknázatlan hivatkozást vagy rést")

    return level, "; ".join(reasons) + "."


def top_risky_keywords(res, n=3):
    scores = defaultdict(int)
    labels = {}
    for c, szo, rc in res["j1"]:
        scores[c] += 3
        labels[c] = szo
    for c, szo, num, src in res["j2"]:
        if num:
            scores[c] += max(0, num - 1)
        labels.setdefault(c, szo)
    for c, szo, total, rem in res["j4"]:
        scores[c] += rem // 5
        labels.setdefault(c, szo)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:n]
    return [f"{labels.get(c, '?')} ({c})" for c, _ in ranked] if ranked else ["—"]


def main():
    print("Konkordancia-adatok betoltese...", file=sys.stderr)
    strong_dict = load_strong_dict()
    tbesh_dict = load_tbesh_dict()
    bdb_dict = load_bdb_dict()
    lxx_genesis = load_lxx_genesis()
    tagnt_by_verse, tagnt_global_freq = load_tagnt()
    tahot_occ = load_tahot_occurrences()
    tagnt_occ = load_tagnt_occurrences()

    all_results = []
    failed_parse = []

    for fn in STUDY_FILES:
        path = GEN_DIR / fn
        if not path.exists():
            print(f"HIANYZIK: {fn}", file=sys.stderr)
            failed_parse.append((fn, "fájl nem található"))
            continue
        res = process_study(
            fn, strong_dict, tbesh_dict, bdb_dict,
            lxx_genesis, tagnt_by_verse, tagnt_global_freq,
            tahot_occ, tagnt_occ,
        )
        all_results.append(res)
        if not res["parse_ok"] or not res["keywords"]:
            failed_parse.append((fn, "kulcsszó-táblázat kinyerése hiányos vagy sikertelen"))
        print(f"  feldolgozva: {fn} ({len(res['keywords'])} kulcsszó, {len(res['refs'])} igehely-hivatkozás)", file=sys.stderr)

    write_report(all_results, failed_parse)
    print(f"\nRiport elmentve: {OUT_PATH}", file=sys.stderr)


def write_report(all_results, failed_parse):
    lines = []
    lines.append("# Kockázat-szűrő riport — 18 auditálatlan bővített tanulmány")
    lines.append("")
    lines.append("*Készült: 2026.09.03, gépi szűréssel (`eszkozok/kockazat_szures_18_tanulmany.py`), "
                  "a 🥈 2. prioritású átadási dokumentum alapján. Célja rangsor a 🥉 3. prioritáshoz "
                  "(melyik 3-5 tanulmányt írjuk újra teljesen). Ez a riport NEM módosítja a study-fájlokat, "
                  "csak elemzi őket.*")
    lines.append("")
    lines.append("## Módszertan és korlátok")
    lines.append("")
    lines.append("A szkript minden tanulmány \"## 2. Eredeti nyelvi szöveg\" táblázatából kinyeri a "
                  "(vers, héber szó, Strong-szám) hármasokat, a \"## 4. Kapcsolódó igehelyek\" 🔗-blokkjaiból "
                  "pedig az idézett igehelyeket. Négy jelzőt számít minden kulcsszóra:")
    lines.append("")
    lines.append("1. **Origin-lánc-kockázat** — a `Strong_szotar.tsv` \"Gyök/Származtatás\" oszlopában "
                  "hivatkozott másik Strong-szám, amit a study sehol nem említ.")
    lines.append("2. **Poliszémia-kockázat** — a `TBESH.txt` (elsődleges) vagy `BDB_teljes_unabridged.tsv` "
                  "(tartalék) alapján számolt jelentés-ágak nyers száma.")
    lines.append("3. **Kereszthivatkozás/LXX-kockázat** — a study genezisi verseinek LXX görög Strong-jai és "
                  "az idézett újszövetségi versek görög Strong-jai közötti metszet (a >800 globális NT-előfordulású, "
                  "tisztán nyelvtani \"ragasztószavak\" — και, ὁ, δέ, αὐτοῦ stb. — kizárásával, mert enélkül a "
                  "metszet szinte soha nem lenne üres); üres tartalmi metszet = piros zászló (lehetséges hamis "
                  "pozitív), ritka (globálisan <200 előfordulású), nem-kulcsszóként szereplő közös szó = "
                  "kiaknázatlan lehetőség.")
    lines.append("4. **Teljes-előfordulás-rés** — a kulcsszó összes bibliai előfordulása (`TAHOT_kivonat.tsv` / "
                  "`TAGNT_kivonat.tsv`) mínusz a study bárhol már idézett igehelyei.")
    lines.append("")
    lines.append("**Korlátok:**")
    lines.append("- A Markdown-táblázat-parszolás nem tökéletes minden fájlban — lásd alább, mely tanulmányoknál "
                  "volt hiányos a kulcsszó-kinyerés.")
    lines.append("- Az Origin-lánc jelző csak azt jelzi, hogy VAN kiaknázatlan hivatkozás — nem dönti el, hogy az "
                  "tartalmilag érdemi-e (ahogy a celem esetében 9 a 11-ből nem hozott újat). Ez emberi értékelést igényel.")
    lines.append("- A 3. jelző (LXX-híd) csak a Genezis-only LXX-pilot hatókörén belül működik — más ószövetségi "
                  "könyvekre hivatkozó study-részek nem ellenőrizhetők ezzel.")
    lines.append("- A 3. jelző stopword-szűrése (>800 előfordulás) heurisztikus — nem valódi morfológiai "
                  "szűrés, ezért elméletileg kiszűrhet egy ritka esetben tényleg releváns, de nagyon gyakori "
                  "szót (pl. θεός), és átengedhet egy határeset körüli szót. A piros zászlók emberi átnézést "
                  "igényelnek, nem automatikus törlést.")
    lines.append("- **Fontos:** a 3. jelző piros zászlója NEM jelenti automatikusan, hogy a study hibás "
                  "kereszthivatkozást tartalmaz — csak azt, hogy nincs közös tartalmi LXX/NT görög szó a "
                  "genezisi vers és az idézett újszövetségi vers között. Ha a study maga is csak **tematikus** "
                  "(nem lexikai) kapcsolatként jelöli meg az adott igehelyet, a piros zászló hamis riasztás — "
                  "lásd pl. `1Moz_7v1-24_bovitett.md` Róm 9:27 találatát, ahol a study explicit módon "
                  "tematikus párhuzamnak nevezi, nem lexikai/LXX-kapcsolatnak. Minden piros zászlót a study "
                  "saját szövegkörnyezetében kell ellenőrizni, mielőtt hibának minősítenénk.")
    lines.append("- A poliszémia-szám (2. jelző) nyers jelentés-ág-szám, nem azt méri, hogy a study melyik ágat "
                  "választotta helyesen vagy helytelenül.")
    lines.append("- A teljes-előfordulás-rés (4. jelző) csak azt méri, hogy egy igehely szó szerint idézve "
                  "szerepel-e valahol a dokumentumban (bold `**Könyv fej:vers**` minta) — parafrázisokat nem ismeri fel.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Összefoglaló táblázat")
    lines.append("")
    lines.append("| Tanulmány | Legkockázatosabb kulcsszó(k) | Jelző 1 (Origin) | Jelző 2 (poliszémia) | "
                  "Jelző 3 (LXX-kereszthiv.) | Jelző 4 (feltáratlan előford.) | Összbenyomás |")
    lines.append("|---|---|---|---|---|---|---|")

    for res in all_results:
        fn = res["filename"]
        risky = ", ".join(top_risky_keywords(res))
        j1_cell = f"{len(res['j1'])} kiaknázatlan hiv." if res["j1"] else "nincs"
        max_poly = max((n for c, s, n, src in res["j2"] if n), default=None)
        j2_cell = f"max {max_poly} jelentés-ág" if max_poly is not None else "n/a"
        j3_bits = []
        if res["j3_red"]:
            j3_bits.append(f"{len(res['j3_red'])} piros zászló")
        if res["j3_opp"]:
            j3_bits.append(f"{len(res['j3_opp'])} kiaknázatlan")
        j3_cell = ", ".join(j3_bits) if j3_bits else ("nincs adat" if not res["j3_has_verse"] else "nincs kockázat")
        max_gap = max((rem for c, s, total, rem in res["j4"]), default=None)
        j4_cell = f"max {max_gap} sosem idézett" if max_gap is not None else "n/a"
        level, reason = summarize_impression(res)
        lines.append(f"| `{fn}` | {risky} | {j1_cell} | {j2_cell} | {j3_cell} | {j4_cell} | "
                      f"**{level}**: {reason} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Nyers, nem-szubjektív összesítő táblázat")
    lines.append("")
    lines.append("*Csak számok — saját súlyozáshoz.*")
    lines.append("")
    lines.append("| Tanulmány | Kulcsszavak száma | Igehely-hivatkozások száma | J1 db | J2 max | J2 átlag | "
                  "J3 piros zászló | J3 kiaknázatlan | J4 max rés | J4 összes rés |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")

    for res in all_results:
        n_kw = len(res["keywords"])
        n_refs = len(res["refs"])
        j1_n = len(res["j1"])
        poly_vals = [n for c, s, n, src in res["j2"] if n]
        j2_max = max(poly_vals) if poly_vals else 0
        j2_avg = round(sum(poly_vals) / len(poly_vals), 1) if poly_vals else 0
        j3_red_n = len(res["j3_red"])
        j3_opp_n = len(res["j3_opp"])
        gap_vals = [rem for c, s, total, rem in res["j4"]]
        j4_max = max(gap_vals) if gap_vals else 0
        j4_sum = sum(gap_vals) if gap_vals else 0
        lines.append(f"| `{res['filename']}` | {n_kw} | {n_refs} | {j1_n} | {j2_max} | {j2_avg} | "
                      f"{j3_red_n} | {j3_opp_n} | {j4_max} | {j4_sum} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Részletes jelző-1 (Origin-lánc) találatok")
    lines.append("")
    any_j1 = False
    for res in all_results:
        if not res["j1"]:
            continue
        any_j1 = True
        lines.append(f"**`{res['filename']}`**")
        for code, szo, ref_code in res["j1"]:
            lines.append(f"- `{code}` ({szo}) → hivatkozott, de nem tárgyalt `{ref_code}`")
        lines.append("")
    if not any_j1:
        lines.append("*(nincs találat)*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Részletes jelző-3 (LXX-kereszthivatkozás) találatok")
    lines.append("")
    any_j3 = False
    for res in all_results:
        if not res["j3_red"] and not res["j3_opp"]:
            continue
        any_j3 = True
        lines.append(f"**`{res['filename']}`**")
        for ref in res["j3_red"]:
            lines.append(f"- 🔴 piros zászló: **{ref}** — üres a metszet a genezisi vers(ek) LXX görög "
                          f"Strong-jaival (lehetséges hamis pozitív kereszthivatkozás)")
        for ref, g, freq in res["j3_opp"]:
            lines.append(f"- 🟡 kiaknázatlan: **{ref}** ↔ `{g}` (globális NT-előfordulás: {freq}) — "
                          f"a study nem nevezi meg kulcsszóként")
        lines.append("")
    if not any_j3:
        lines.append("*(nincs találat)*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Sikertelen vagy hiányos kulcsszó-kinyerés")
    lines.append("")
    if failed_parse:
        for fn, reason in failed_parse:
            lines.append(f"- `{fn}` — {reason}")
    else:
        lines.append("*(minden tanulmánynál sikeres volt a kulcsszó-kinyerés)*")
    lines.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
