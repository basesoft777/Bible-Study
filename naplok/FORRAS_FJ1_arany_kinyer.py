import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

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
            igehely, lxx_igehely, heber, gorog, egyezes, forras = cols[:6]
            if egyezes in ("egyező", "eltérő") or motivum == "ISTENTISZT-001":
                rows.append((motivum, igehely, lxx_igehely, heber, gorog, egyezes, forras))

with open("naplok/FORRAS_FJ1_arany.tsv", "w", encoding="utf-8") as out:
    out.write("motivum\tigehely\tlxx_igehely\theber_kulcsszo\tgorog_megfelelo\tegyezes\tforras\n")
    for r in rows:
        out.write("\t".join(r) + "\n")

print(f"Kiírva: {len(rows)} sor -> naplok/FORRAS_FJ1_arany.tsv")
from collections import Counter
c = Counter(r[5] for r in rows)
print(c)
