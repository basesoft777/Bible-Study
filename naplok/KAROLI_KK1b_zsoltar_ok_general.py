import sys
import re
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

fejezetosztaly = {}
with open("naplok/KAROLI_KK1b_fejezetosztaly.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        if parts[0] != "Zsolt":
            continue
        fejezetosztaly[int(parts[2])] = parts[6]

ok_szamlalo = Counter()
karoli_ok_szamlalo = Counter()
reszletek = []

with open("konkordancia/LXX_OS/psalms-lxx.tsv", encoding="utf-8") as f:
    for line in f:
        if line.startswith("#") or line.startswith("igehely_lxx"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 4:
            continue
        igehely_lxx, karoli_ok = parts[0], parts[3]
        karoli_ok_szamlalo[karoli_ok if karoli_ok else "(kitoltott)"] += 1
        if karoli_ok != "szamozas_elteres":
            continue
        m = re.search(r"(\d+):(\d+)$", igehely_lxx)
        if not m:
            continue
        vers_kulcs = igehely_lxx
        ch = int(m.group(1))
        osztaly = fejezetosztaly.get(ch, "NINCS_ADAT")
        if osztaly == "KEZI":
            ok = "H1_importer_kezi_none_fallthrough"
        elif osztaly == "MT":
            ok = "H2_karoli_mt_szamozas"
        elif osztaly == "KJV":
            ok = "H5_valodi_verstartalmi_elteres"
        elif osztaly == "EGYIK_SEM":
            ok = "H3_egyeb_karoli_sajatossag"
        else:
            ok = "NINCS_OSZTALY_ADAT"
        ok_szamlalo[(ch, ok)] = ok_szamlalo.get((ch, ok), 0)  # noop, csak jelzi hasznalva van
        reszletek.append((ch, m.group(0), osztaly, ok))

print("=== Zsoltarok karoli_ok szosor-szinten (teljes psalms-lxx.tsv) ===")
for k, v in karoli_ok_szamlalo.most_common():
    print(f"  {k}: {v}")

vers_ok = Counter(r[3] for r in reszletek)
egyedi_versek = set((r[0], r[1]) for r in reszletek)
print(f"\n=== Zsoltarok szamozas_elteres -- egyedi LXX-versek: {len(egyedi_versek)} ===")
print(vers_ok)

with open("naplok/KAROLI_KK1b_ok_besorolas.tsv", "w", encoding="utf-8") as out:
    out.write("konyv\tfejezet\tigehely_lxx_veg\tfejezetosztaly\tok\n")
    seen = set()
    for ch, vegz, osztaly, ok in reszletek:
        key = (ch, vegz)
        if key in seen:
            continue
        seen.add(key)
        out.write(f"Zsolt\t{ch}\t{vegz}\t{osztaly}\t{ok}\n")
