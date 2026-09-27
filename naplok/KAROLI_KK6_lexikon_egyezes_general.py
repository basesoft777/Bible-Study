import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

counts = {}
total_rows = 0

for path in sorted(glob.glob("lexikon/*_TUDOMANYOS.md")):
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
            if len(cols) < 5:
                continue
            egyezes = cols[4]
            counts[egyezes] = counts.get(egyezes, 0) + 1
            total_rows += 1

print("Összesített 'Egyezés' oszlop, mind a 8 TUDOMANYOS fájlból:")
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {k!r}: {v}")
print(f"Összesen sor: {total_rows}")
