import sys
import re
import glob
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# LXX_OS fajlnev (slug) -> (karoli_konyv, book_key) -- csak a testament=ot konyvek
SLUG_TO_KAROLI = {
    "genesis": ("1Móz", "genesis"), "exodus": ("2Móz", "exodus"), "leviticus": ("3Móz", "leviticus"),
    "numbers": ("4Móz", "numbers"), "deuteronomy": ("5Móz", "deuteronomy"),
    "joshua": ("Józs", "joshua"), "joshua-vaticanus-b": ("Józs", "joshua"),
    "judges": ("Bír", "judges"), "judges-vaticanus-b": ("Bír", "judges"),
    "ruth": ("Ruth", "ruth"), "1-samuel": ("1Sám", "1-samuel"), "2-samuel": ("2Sám", "2-samuel"),
    "1-kings": ("1Kir", "1-kings"), "2-kings": ("2Kir", "2-kings"),
    "1-chronicles": ("1Krón", "1-chronicles"), "2-chronicles": ("2Krón", "2-chronicles"),
    "job-lxx": ("Jób", "job"), "psalms-lxx": ("Zsolt", "psalms"),
    "proverbs": ("Péld", "proverbs"), "ecclesiastes": ("Préd", "ecclesiastes"),
    "song-of-solomon": ("Én", "song-of-solomon"), "isaiah": ("Ézs", "isaiah"),
    "jeremiah-lxx": ("Jer", "jeremiah"), "lamentations": ("Sir", "lamentations"),
    "ezekiel": ("Ez", "ezekiel"), "daniel": ("Dán", "daniel"),
    "hosea": ("Hós", "hosea"), "joel": ("Jóel", "joel"), "amos": ("Ámós", "amos"),
    "obadiah": ("Abd", "obadiah"), "jonah": ("Jón", "jonah"), "micah": ("Mik", "micah"),
    "nahum": ("Náh", "nahum"), "habakkuk": ("Hab", "habakkuk"), "zephaniah": ("Sof", "zephaniah"),
    "haggai": ("Hag", "haggai"), "zechariah": ("Zak", "zechariah"), "malachi": ("Mal", "malachi"),
}

# fejezetosztaly betoltese
fejezetosztaly = {}
with open("naplok/KAROLI_KK1_fejezetosztaly.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        karoli_konyv, book_key, ch = parts[0], parts[1], int(parts[2])
        osztaly = parts[6]
        fejezetosztaly[(karoli_konyv, int(ch))] = osztaly

ok_szamlalo = Counter()
reszletek = []
latt_versek = set()

for slug, (karoli_konyv, book_key) in SLUG_TO_KAROLI.items():
    path = f"konkordancia/LXX_OS/{slug}.tsv"
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        continue
    with f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            igehely_lxx, karoli_ok = parts[0], parts[3]
            if karoli_ok != "szamozas_elteres":
                continue
            m = re.search(r"(\d+):(\d+)$", igehely_lxx)
            if not m:
                continue
            vers_kulcs = (slug, igehely_lxx)
            if vers_kulcs in latt_versek:
                continue
            latt_versek.add(vers_kulcs)
            ch = int(m.group(1))
            osztaly = fejezetosztaly.get((karoli_konyv, ch), "NINCS_ADAT")
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
            ok_szamlalo[ok] += 1
            reszletek.append((karoli_konyv, ch, m.group(0), osztaly, ok))

print("Az 1015 (szósoronként több, de itt versenkénti számlálás LXX-oldalról) "
      "szamozas_elteres LXX-vers okonkénti bontása:")
for k, v in ok_szamlalo.most_common():
    print(f"  {k}: {v}")
print(f"Összesen: {sum(ok_szamlalo.values())}")

with open("naplok/KAROLI_KK1_ok_besorolas_reszletek.tsv", "w", encoding="utf-8") as out:
    out.write("karoli_konyv\tfejezet\tigehely_lxx_veg\tfejezetosztaly\tok\n")
    for r in reszletek:
        out.write("\t".join(str(x) for x in r) + "\n")
