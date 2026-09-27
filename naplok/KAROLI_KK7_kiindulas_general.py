import sys
import subprocess
import glob
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASELINE_COMMIT = "a6783e4"


def load_karoli_map(text):
    """igehely_lxx -> lista of (igehely_karoli) az osszes szosorra (pozicio szerint)"""
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


valtozatlan = 0
megvaltozott = 0
ujonnan_kitoltott = 0
ures_maradt = 0
eltunt = 0
megvaltozott_reszletek = []

for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    rel = os.path.relpath(path)
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
    new_map = load_karoli_map(new_text)

    kulcsok = set(old_map) | set(new_map)
    for k in kulcsok:
        o = old_map.get(k, "")
        n = new_map.get(k, "")
        if o and n:
            if o == n:
                valtozatlan += 1
            else:
                megvaltozott += 1
                megvaltozott_reszletek.append((rel, k[0], k[1], o, n))
        elif o and not n:
            eltunt += 1
        elif not o and n:
            ujonnan_kitoltott += 1
        else:
            ures_maradt += 1

print(f"korabban kitoltott es valtozatlan: {valtozatlan}")
print(f"megvaltozott: {megvaltozott}")
print(f"ujonnan kitoltott: {ujonnan_kitoltott}")
print(f"ures maradt: {ures_maradt}")
print(f"eltunt: {eltunt}")

if megvaltozott_reszletek:
    with open("naplok/KAROLI_KK7_megvaltozott_sorok.tsv", "w", encoding="utf-8") as out:
        out.write("fajl\tigehely_lxx\tpozicio\tregi\tuj\n")
        for r in megvaltozott_reszletek:
            out.write("\t".join(r) + "\n")
    print(f"reszletek: naplok/KAROLI_KK7_megvaltozott_sorok.tsv ({len(megvaltozott_reszletek)} sor)")
