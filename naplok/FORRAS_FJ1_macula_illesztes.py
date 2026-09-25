import sys
import re
import os
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
strong_re = re.compile(r"G0*(\d+)")

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


results = []
skipped = 0

with open("naplok/FORRAS_FJ1_arany.tsv", encoding="utf-8") as f:
    header = f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        motivum, igehely, lxx_igehely, heber, gorog, egyezes, forras = parts[:7]
        m = igehely_re.match(igehely.strip())
        if not m:
            skipped += 1
            continue
        magyar, fej, vers = m.group(1), int(m.group(2)), int(m.group(3))
        book_code = konyv_map.get(magyar)
        if not book_code or book_code not in files_by_code:
            skipped += 1
            continue
        fn = files_by_code[book_code].get(fej)
        if not fn:
            results.append((motivum, igehely, egyezes, "NINCS_XML_FAJL", "", ""))
            continue
        xml_path = os.path.join(XML_ROOT, fn)
        ref_key = f"{book_code} {fej}:{vers}"
        words = load_verse_words(xml_path, ref_key)
        if not words:
            results.append((motivum, igehely, egyezes, "NINCS_VERS", "", ""))
            continue
        expected_strong_m = strong_re.search(gorog)
        expected_strong = expected_strong_m.group(1) if expected_strong_m else None
        verse_strongs = [w.get("greekstrong", "") for w in words]
        verse_strongs_norm = [s.lstrip("0") or "0" for s in verse_strongs if s]
        verse_match = expected_strong in verse_strongs_norm if expected_strong else False
        results.append((motivum, igehely, egyezes, "TALALAT" if verse_match else "NINCS_EGYEZES",
                         expected_strong or "", ",".join(verse_strongs_norm)))

with open("naplok/FORRAS_FJ1_macula_teszt.tsv", "w", encoding="utf-8") as out:
    out.write("motivum\tigehely\tarany_egyezes\tteszt_eredmeny\tvart_strong\tvers_strongjai\n")
    for r in results:
        out.write("\t".join(r) + "\n")

A = [r for r in results if r[2] == "egyező"]
A_talalat = [r for r in A if r[3] == "TALALAT"]
C = [r for r in results if r[2] == "eltérő"]

print(f"Kihagyott sorok: {skipped}")
print(f"A (egyező) halmaz mérhető sorai: {len(A)}")
if A:
    print(f"A halmazból TALALAT: {len(A_talalat)} ({100*len(A_talalat)/len(A):.1f}%)")
print(f"C sorok: {len(C)}, TALALAT: {sum(1 for r in C if r[3]=='TALALAT')}")
from collections import Counter
print(Counter(r[3] for r in A))
