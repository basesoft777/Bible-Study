import sys
import subprocess
import glob
import os
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASELINE_COMMIT = "a6783e4"


def load_karoli_map(text):
    d = {}
    for line in text.splitlines():
        if line.startswith("#") or line.startswith("igehely_lxx"):
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        igehely_lxx, igehely_karoli, pozicio = parts[0], parts[2], parts[4]
        key = (igehely_lxx, pozicio)
        d[key] = igehely_karoli
    return d


ujonnan = []  # (fajl, igehely_lxx, igehely_karoli)

for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    rel = os.path.relpath(path)
    slug = os.path.basename(path).replace(".tsv", "")
    try:
        old_text = subprocess.run(
            ["git", "show", f"{BASELINE_COMMIT}:{rel}"],
            capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError:
        old_text = ""

    with open(path, encoding="utf-8") as f:
        new_text = f.read()

    old_map = load_karoli_map(old_text)

    seen_verses = set()
    for line in new_text.splitlines():
        if line.startswith("#") or line.startswith("igehely_lxx"):
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        igehely_lxx, igehely_karoli, pozicio = parts[0], parts[2], parts[4]
        if not igehely_karoli:
            continue
        key = (igehely_lxx, pozicio)
        if old_map.get(key):
            continue  # korabban is ki volt toltve
        vkey = (slug, igehely_lxx)
        if vkey in seen_verses:
            continue
        seen_verses.add(vkey)
        ujonnan.append((slug, igehely_lxx, igehely_karoli))

with open("naplok/KAROLI_KK7_ujonnan_kitoltott.tsv", "w", encoding="utf-8") as out:
    out.write("lxx_fajl\tigehely_lxx\tigehely_karoli\n")
    for r in ujonnan:
        out.write("\t".join(r) + "\n")

print(f"Ujonnan kitoltott EGYEDI (fajl,igehely_lxx) parok: {len(ujonnan)}")

fejezetek = set()
for slug, igehely_lxx, igehely_karoli in ujonnan:
    m = re.search(r"(\d+):(\d+)$", igehely_lxx)
    if m:
        fejezetek.add((slug, int(m.group(1))))
print(f"Erintett (fajl,fejezet) parok: {len(fejezetek)}")
