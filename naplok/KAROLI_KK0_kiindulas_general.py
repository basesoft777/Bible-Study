import sys
import glob
import re
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# 0.1 karoli_ok szosor-szinten, minden LXX_OS/*.tsv-n
counts = Counter()
per_book_szamozas = Counter()  # fajl -> szamozas_elteres szosorok szama
verses_by_file_chapter = {}  # (fajl, fejezet) -> set of versek szamozas_elteres-szel

for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("igehely_lxx"):
            header_idx = i
            break
    if header_idx is None:
        continue
    for line in lines[header_idx + 1:]:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 4:
            continue
        igehely_lxx, karoli_ok = parts[0], parts[3]
        if karoli_ok == "":
            counts["(ures=kitoltott)"] += 1
        else:
            counts[karoli_ok] += 1
        if karoli_ok == "szamozas_elteres":
            per_book_szamozas[path] += 1
            m = re.search(r"(\d+):(\d+)$", igehely_lxx)
            if m:
                fejezet = int(m.group(1))
                vers = int(m.group(2))
                verses_by_file_chapter.setdefault(path, {}).setdefault(fejezet, set()).add(vers)

print("=== 0.1: karoli_ok szosor-szinten ===")
for k, v in counts.most_common():
    print(f"  {k}: {v}")

print()
print("=== 0.2: szamozas_elteres versszinten / fejezetenkent / fajlonkent ===")
total_versek = 0
total_fejezetek = 0
fajl_szam = 0
for path, chapters in verses_by_file_chapter.items():
    fajl_szam += 1
    total_fejezetek += len(chapters)
    total_versek += sum(len(v) for v in chapters.values())
print(f"  erintett fajlok: {fajl_szam}")
print(f"  erintett fejezetek (osszesen, fajlonkent osszegezve): {total_fejezetek}")
print(f"  erintett LXX-versek (osszesen): {total_versek}")
psalms = verses_by_file_chapter.get("konkordancia/LXX_OS/psalms-lxx.tsv", {})
print(f"  psalms-lxx.tsv erintett fejezetei: {len(psalms)}")

print()
print("=== 0.4: job-lxx.tsv es joshua-vaticanus-b.tsv fejezetszama ===")
for path in ("konkordancia/LXX_OS/job-lxx.tsv", "konkordancia/LXX_OS/joshua-vaticanus-b.tsv"):
    chs = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0]:
                continue
            m = re.search(r"(\d+):(\d+)$", parts[0])
            if m:
                chs.add(int(m.group(1)))
    print(f"  {path}: {len(chs)} fejezet ({min(chs)}-{max(chs)})")
