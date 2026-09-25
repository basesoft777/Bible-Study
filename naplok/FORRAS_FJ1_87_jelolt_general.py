import sys
import re
import os
import glob
import unicodedata
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

XML_ROOT = "/tmp/macula_hebrew_sparse/WLC/lowfat"

konyv_map = {}
with open("konkordancia/Konyv_normalizalo_tabla.tsv", encoding="utf-8") as f:
    header = f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        step, magyar = parts[0], parts[1]
        konyv_map[magyar] = step.upper()

files_by_code = {}
for fn in os.listdir(XML_ROOT):
    m = re.match(r"^\d+-([A-Za-z]+)-(\d+)-lowfat\.xml$", fn)
    if m:
        code, chnum = m.group(1).upper(), int(m.group(2))
        files_by_code.setdefault(code, {})[chnum] = fn

igehely_re = re.compile(r"^(\S+)\s+(\d+):(\d+)")


def strip_niqud(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


_cache = {}


def load_verse_words(xml_path, ref_key):
    if xml_path not in _cache:
        tree = ET.parse(xml_path)
        words_by_ref = {}
        for w in tree.iter("w"):
            ref = w.get("ref", "")
            m = re.match(r"^(\S+ \d+:\d+)", ref)
            if not m:
                continue
            vref = m.group(1)
            words_by_ref.setdefault(vref, []).append(w)
        _cache[xml_path] = words_by_ref
    return _cache[xml_path].get(ref_key, [])


rows = []
for path in sorted(glob.glob("lexikon/*_TUDOMANYOS.md")):
    motivum = path.split("/")[-1].replace("_TUDOMANYOS.md", "")
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    in_table = False
    for line in lines:
        if "Igehely (Károli)" in line and "Egyezés" in line:
            in_table = True
            continue
        if in_table:
            if line.strip().startswith("|---") or set(line.strip()) <= set("|-: "):
                continue
            if not line.strip().startswith("|"):
                in_table = False
                continue
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) < 6:
                continue
            if cols[4] == "kutatói azonosítás függőben":
                rows.append((motivum, cols[0], cols[2]))  # motivum, igehely, heber_kulcsszo

out_rows = []
for motivum, igehely, heber in rows:
    m = igehely_re.match(igehely.strip())
    if not m:
        out_rows.append((motivum, igehely, heber, "", "", "", "nincs_igehely_parse", ""))
        continue
    magyar, fej, vers = m.group(1), int(m.group(2)), int(m.group(3))
    book_code = konyv_map.get(magyar)
    if not book_code or book_code not in files_by_code:
        out_rows.append((motivum, igehely, heber, "", "", "", "nincs_konyv", ""))
        continue
    fn = files_by_code[book_code].get(fej)
    if not fn:
        out_rows.append((motivum, igehely, heber, "", "", "", "nincs_fejezet", ""))
        continue
    xml_path = os.path.join(XML_ROOT, fn)
    ref_key = f"{book_code} {fej}:{vers}"
    words = load_verse_words(xml_path, ref_key)
    if not words:
        out_rows.append((motivum, igehely, heber, "", "", "", "nincs_vers", ""))
        continue
    # A héber_kulcsszó mezőből a puszta héber token (a szóköz/zárójel előtti rész)
    heber_token = heber.split(" ")[0].strip()
    heber_skeleton = strip_niqud(heber_token)
    match = None
    for w in words:
        lemma = w.get("lemma") or ""
        unicode_form = w.get("unicode") or ""
        for cand in (lemma, unicode_form):
            if strip_niqud(cand) == heber_skeleton:
                match = w
                break
        if match:
            break
    if match is None:
        out_rows.append((motivum, igehely, heber, "", "", "", "nincs_szoszintu_talalat", ""))
        continue
    greek = match.get("greek") or ""
    greekstrong = match.get("greekstrong") or ""
    heber_strong = match.get("strongnumberx") or ""
    if not greek and not greekstrong:
        out_rows.append((motivum, igehely, heber, heber_strong, "", "", "nincs_gorog_parositas_LXX_minusz_v_hianyos", "alacsony"))
    else:
        out_rows.append((motivum, igehely, heber, heber_strong, greek, f"G{greekstrong}" if greekstrong else "", "javasolt", "kozepes"))

with open("naplok/FORRAS_FJ1_lxx_jeloltek.tsv", "w", encoding="utf-8") as out:
    out.write("motivum\tigehely\theber_kulcsszo\theber_strong\tjavasolt_gorog_lemma\tjavasolt_gorog_strong\tallapot\tbizonyossag\n")
    for r in out_rows:
        while len(r) < 8:
            r = r + ("",)
        out.write("\t".join(r) + "\n")

from collections import Counter
c = Counter(r[6] for r in out_rows)
print(f"Összesen: {len(out_rows)} sor (a 87 függő helyből)")
print(c)
