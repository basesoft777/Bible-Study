import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# TAHOT Strong-szamok 1Moz 1:1-5-re
tahot = {}
with open("konkordancia/TAHOT_kivonat.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        igehely, strong = parts[0], parts[1]
        m = re.match(r"^1Móz 1:([1-5])$", igehely)
        if m:
            tahot.setdefault(int(m.group(1)), []).append(strong.lstrip("H0") or "0")

with open("/tmp/bsb_data_test/base/display/GEN/GEN1.json", encoding="utf-8") as f:
    bsb = json.load(f)

rows = []
for vs in range(1, 6):
    bsb_strongs = []
    for span in bsb["eng"][str(vs)]:
        if len(span) >= 2 and span[1]:
            s = span[1].lstrip("H0") or "0"
            bsb_strongs.append(s)
    t = tahot.get(vs, [])
    common = set(t) & set(bsb_strongs)
    total = set(t) | set(bsb_strongs)
    arany = 100 * len(common) / len(total) if total else 0
    rows.append((vs, ",".join(t), ",".join(bsb_strongs), f"{arany:.0f}%"))
    print(f"1Móz 1:{vs} — TAHOT: {t}")
    print(f"           BSB:   {bsb_strongs}")
    print(f"           halmaz-egyezes (Jaccard): {arany:.0f}%")

with open("naplok/FORRAS_FJ3_bsb_minta.tsv", "w", encoding="utf-8") as f:
    f.write("igehely\ttahot_strongok\tbsb_strongok\thalmaz_egyezes\n")
    for vs, t, b, a in rows:
        f.write(f"1Móz 1:{vs}\t{t}\t{b}\t{a}\n")
