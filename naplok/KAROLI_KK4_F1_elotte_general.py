import sys
import glob
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# F1: deduplikalt (LXX-fajl, igehely_lxx) parok karoli_ok=szamozas_elteres-szel
parok = set()
fajlonkent = Counter()

for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    slug = path.split("/")[-1].replace(".tsv", "")
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            igehely_lxx, karoli_ok = parts[0], parts[3]
            if karoli_ok != "szamozas_elteres":
                continue
            key = (slug, igehely_lxx)
            if key in parok:
                continue
            parok.add(key)
            fajlonkent[slug] += 1

print(f"F1 elotte-ertek: {len(parok)} deduplikalt (LXX-fajl, igehely_lxx) par, karoli_ok=szamozas_elteres")
print(f"psalms-lxx.tsv: {fajlonkent.get('psalms-lxx', 0)}")
print(f"Erintett fajlok szama: {len(fajlonkent)}")
print("Fajlonkenti bontas:")
for k, v in fajlonkent.most_common():
    print(f"  {k}: {v}")

with open("naplok/KAROLI_KK4_F1_elotte.tsv", "w", encoding="utf-8") as out:
    out.write("lxx_fajl\tigehely_lxx\n")
    for slug, igehely in sorted(parok):
        out.write(f"{slug}\t{igehely}\n")
