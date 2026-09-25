import sys
import re
import glob
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

XML_ROOT = "/tmp/test_CenterBLC_MT-LXX/xml/2025-04-24"

# Magyar rövidítés -> STEPBible (3-betűs, angol) kód
konyv_map = {}
with open("konkordancia/Konyv_normalizalo_tabla.tsv", encoding="utf-8") as f:
    header = f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        step, magyar = parts[0], parts[1]
        konyv_map[magyar] = step.upper()

# könyvkód -> mappa (pl. GEN -> 01-GEN)
book_dirs = {}
import os
for d in os.listdir(XML_ROOT):
    if "-" in d:
        num, code = d.split("-", 1)
        book_dirs[code] = d

igehely_re = re.compile(r"^(\S+)\s+(\d+):(\d+)")
strong_re = re.compile(r"G0*(\d+)")


def parse_igehely(igehely):
    m = igehely_re.match(igehely.strip())
    if not m:
        return None
    magyar, fej, vers = m.group(1), int(m.group(2)), int(m.group(3))
    return magyar, fej, vers


def find_xml_file(book_code, fejezet):
    d = book_dirs.get(book_code)
    if not d:
        return None
    folder = os.path.join(XML_ROOT, d)
    pattern = f"-{fejezet:03d}-lowfat.xml"
    for fn in os.listdir(folder):
        if fn.endswith(pattern):
            return os.path.join(folder, fn)
    return None


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
skipped_no_ot = 0

with open("naplok/FORRAS_FJ1_arany.tsv", encoding="utf-8") as f:
    header = f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        motivum, igehely, lxx_igehely, heber, gorog, egyezes, forras = parts[:7]
        parsed = parse_igehely(igehely)
        if not parsed:
            skipped_no_ot += 1
            continue
        magyar, fej, vers = parsed
        book_code = konyv_map.get(magyar)
        if not book_code or book_code not in book_dirs:
            skipped_no_ot += 1
            continue
        xml_path = find_xml_file(book_code, fej)
        if not xml_path:
            results.append((motivum, igehely, egyezes, "NINCS_XML_FAJL", "", ""))
            continue
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

with open("naplok/FORRAS_FJ1_mtlxx_teszt.tsv", "w", encoding="utf-8") as out:
    out.write("motivum\tigehely\tarany_egyezes\tteszt_eredmeny\tvart_strong\tvers_strongjai\n")
    for r in results:
        out.write("\t".join(r) + "\n")

# Összesítés A halmazra (egyező sorok)
A = [r for r in results if r[2] == "egyező"]
A_talalat = [r for r in A if r[3] == "TALALAT"]
C = [r for r in results if r[2] == "eltérő"]

print(f"OT-en kívüli / könyv nem található sorok (kihagyva): {skipped_no_ot}")
print(f"A (egyező) halmaz mérhető sorai: {len(A)}")
print(f"A halmazból a MT-LXX-illesztés TALALAT-ot ad: {len(A_talalat)} ({100*len(A_talalat)/len(A):.1f}%)" if A else "A halmaz üres")
print(f"C (eltérő, csak jelentésre) sorok: {len(C)}, ebből TALALAT: {sum(1 for r in C if r[3]=='TALALAT')}")

from collections import Counter
print("Teszteredmény-eloszlás (A halmaz):", Counter(r[3] for r in A))
