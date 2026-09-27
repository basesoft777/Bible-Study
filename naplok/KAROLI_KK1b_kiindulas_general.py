import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

print("=== 0b.1: KAROLI_KK1_fejezetosztaly.tsv ===")
konyvek = set()
osztaly_c = Counter()
with open("naplok/KAROLI_KK1_fejezetosztaly.tsv", encoding="utf-8") as f:
    f.readline()
    n = 0
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        konyvek.add(parts[0])
        osztaly_c[parts[6]] += 1
        n += 1
print(f"  fejezetek: {n}, konyvek: {len(konyvek)}")
print(f"  osztaly-bontas: {dict(osztaly_c)}")

print("\n=== 0b.2: hianyzo konyvek ===")
BOOK_KEY_TO_KAROLI_TELJES = {
    "genesis": "1Móz", "exodus": "2Móz", "leviticus": "3Móz", "numbers": "4Móz",
    "deuteronomy": "5Móz", "joshua": "Józs", "judges": "Bír", "ruth": "Ruth",
    "1-samuel": "1Sám", "2-samuel": "2Sám", "1-kings": "1Kir", "2-kings": "2Kir",
    "1-chronicles": "1Krón", "2-chronicles": "2Krón", "ezra": "Ezsd", "nehemiah": "Neh",
    "esther": "Eszt", "job": "Jób", "psalms": "Zsolt",
    "proverbs": "Péld", "ecclesiastes": "Préd", "song-of-solomon": "Én", "isaiah": "Ézs",
    "jeremiah": "Jer", "lamentations": "Sir", "ezekiel": "Ez", "daniel": "Dán",
    "hosea": "Hós", "joel": "Jóel", "amos": "Ámós", "obadiah": "Abd", "jonah": "Jón",
    "micah": "Mik", "nahum": "Náh", "habakkuk": "Hab", "zephaniah": "Sof",
    "haggai": "Hag", "zechariah": "Zak", "malachi": "Mal",
}
print(f"  39 konyv modell osszesen: {len(BOOK_KEY_TO_KAROLI_TELJES)}")
hianyzo = [v for v in BOOK_KEY_TO_KAROLI_TELJES.values() if v not in konyvek]
print(f"  a KK1 fejezetosztaly-tablabol hianyzo konyvek: {hianyzo}")

print("\n=== 0b.5-0b.6: LXX_versificacios_terkep.tsv ===")
elteres_c = Counter()
egyezik_c = Counter()
n = 0
with open("konkordancia/LXX_versificacios_terkep.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        elteres_c[parts[4]] += 1
        egyezik_c[parts[5]] += 1
        n += 1
print(f"  sorok: {n}")
print(f"  Elteres_tipusa: {dict(elteres_c)}")
print(f"  Karoli_egyezik_hol: {egyezik_c.most_common()}")

print("\n=== 0b.7: hasznalta-e a KK-menet a terkepet ===")
import glob
hasznalta = False
for path in glob.glob("naplok/KAROLI_KK*.py") + glob.glob("naplok/KAROLI_KK*.md"):
    with open(path, encoding="utf-8") as f:
        if "LXX_versificacios_terkep" in f.read():
            print(f"  hivatkozas: {path}")
            hasznalta = True
print(f"  hasznalta: {hasznalta}")

print("\n=== 0b.8: ellentmondas-minta (Jon 2:3) ===")
with open("konkordancia/LXX_versificacios_terkep.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts and parts[0] == "Jón 2:3":
            print(f"  terkep sora: {parts}")
print("  tartalmi kontroll (KK0 0.8): Karoli Jon 2:3 = MT 2:3 = LXX 2:3 (nem eltolva)")
