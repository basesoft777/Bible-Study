import sys
import glob
import re
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SLUG_TO_KAROLI = {
    "genesis": "1Móz", "exodus": "2Móz", "leviticus": "3Móz", "numbers": "4Móz",
    "deuteronomy": "5Móz", "joshua": "Józs", "joshua-vaticanus-b": "Józs",
    "judges": "Bír", "judges-vaticanus-b": "Bír", "ruth": "Ruth",
    "1-samuel": "1Sám", "2-samuel": "2Sám", "1-kings": "1Kir", "2-kings": "2Kir",
    "1-chronicles": "1Krón", "2-chronicles": "2Krón",
    "job-lxx": "Jób", "psalms-lxx": "Zsolt",
    "proverbs": "Péld", "ecclesiastes": "Préd", "song-of-solomon": "Én", "isaiah": "Ézs",
    "jeremiah-lxx": "Jer", "lamentations": "Sir", "ezekiel": "Ez",
    "daniel": "Dán", "daniel-theodotion": "Dán",
    "hosea": "Hós", "joel": "Jóel", "amos": "Ámós", "obadiah": "Abd", "jonah": "Jón",
    "micah": "Mik", "nahum": "Náh", "habakkuk": "Hab", "zephaniah": "Sof",
    "haggai": "Hag", "zechariah": "Zak", "malachi": "Mal",
    "2-esdras": None, "esther-greek": None,
}

fejezetosztaly = {}
with open("naplok/KAROLI_KK1b_fejezetosztaly.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        fejezetosztaly[(parts[0], int(parts[2]))] = parts[6]

parok = set()
ok_c = Counter()
reszletek = []

for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    slug = path.split("/")[-1].replace(".tsv", "")
    karoli_book = SLUG_TO_KAROLI.get(slug)
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            igehely_lxx, karoli_ok = p[0], p[3]
            if karoli_ok != "szamozas_elteres":
                continue
            key = (slug, igehely_lxx)
            if key in parok:
                continue
            parok.add(key)

            ok = "NINCS_KAROLI_KONYV_VAGY_NEM_MERT"
            if karoli_book:
                m = re.search(r"(\d+):(\d+)$", igehely_lxx)
                if m:
                    ch = int(m.group(1))
                    osztaly = fejezetosztaly.get((karoli_book, ch), "NINCS_ADAT")
                    if osztaly == "EGYIK_SEM":
                        ok = "H3_EGYIK_SEM"
                    elif osztaly in ("KJV", "MT", "KEZI"):
                        ok = "H5_VALODI_ELTERES_VAGY_CIMSOR_AMBIGUITAS"
                    else:
                        ok = "NINCS_OSZTALY_ADAT"
            ok_c[ok] += 1
            reszletek.append((slug, igehely_lxx, ok))

print(f"F1 utana-ertek: {len(parok)} deduplikalt par")
print("Ok-bontas:", dict(ok_c))

with open("naplok/KAROLI_KK6_utana_ok.tsv", "w", encoding="utf-8") as out:
    out.write("lxx_fajl\tigehely_lxx\tok\n")
    for r in reszletek:
        out.write("\t".join(r) + "\n")

h5_count = ok_c.get("H5_VALODI_ELTERES_VAGY_CIMSOR_AMBIGUITAS", 0)
print(f"\nF2: K7 nevezo = 1015 - {h5_count} (H5-kent igazolt) = {1015 - h5_count}")
kitoltott_most = 1015 - len(parok)
print(f"F2: K7 aranya = {kitoltott_most} / {1015 - h5_count} = {100*kitoltott_most/(1015-h5_count):.1f}%")
