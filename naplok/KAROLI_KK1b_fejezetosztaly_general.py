import sys
import json
import re
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, "eszkozok")
from lxx_kivonat_fetch_v2 import KEZI_ELTOLASOK  # noqa: E402

# a KK1-ben mar hasznalt 36 konyv + az uj harom
BOOK_KEY_TO_KAROLI = {
    "genesis": "1Móz", "exodus": "2Móz", "leviticus": "3Móz", "numbers": "4Móz",
    "deuteronomy": "5Móz", "joshua": "Józs", "judges": "Bír", "ruth": "Ruth",
    "1-samuel": "1Sám", "2-samuel": "2Sám", "1-kings": "1Kir", "2-kings": "2Kir",
    "1-chronicles": "1Krón", "2-chronicles": "2Krón",
    "ezra": "Ezsd", "nehemiah": "Neh", "esther": "Eszt",
    "job": "Jób", "psalms": "Zsolt",
    "proverbs": "Péld", "ecclesiastes": "Préd", "song-of-solomon": "Én", "isaiah": "Ézs",
    "jeremiah": "Jer", "lamentations": "Sir", "ezekiel": "Ez", "daniel": "Dán",
    "hosea": "Hós", "joel": "Jóel", "amos": "Ámós", "obadiah": "Abd", "jonah": "Jón",
    "micah": "Mik", "nahum": "Náh", "habakkuk": "Hab", "zephaniah": "Sof",
    "haggai": "Hag", "zechariah": "Zak", "malachi": "Mal",
}
KAROLI_TO_ENGLISH_FOR_KEZI = {
    "4Móz": "Numbers", "Jób": "Job", "Préd": "Ecclesiastes", "Dán": "Daniel",
}

ures_helyorzo = set()
with open("konkordancia/Karoli_ures_helyorzo_sorok.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts and parts[0]:
            ures_helyorzo.add(parts[0])

karoli_max = {}
with open("konkordancia/Karoli_1908.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if not parts or not parts[0] or parts[0] in ures_helyorzo:
            continue
        m = re.match(r"^(\S+) (\d+):(\d+)$", parts[0])
        if not m:
            continue
        book, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
        key = (book, ch)
        if key not in karoli_max or vs > karoli_max[key]:
            karoli_max[key] = vs

kjv_max = {}
with open("/tmp/lxxmorph_test/db/seeds/mt_alignment/verse_pairs.jsonl", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        for mt_ref in d.get("mt_refs", []):
            m = re.match(r"^(\d+):(\d+)$", mt_ref)
            if not m:
                continue
            ch, vs = int(m.group(1)), int(m.group(2))
            key = (d["mt_book"], ch)
            if key not in kjv_max or vs > kjv_max[key]:
                kjv_max[key] = vs

mt_max = {}
with open("konkordancia/TAHOT_kivonat.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if not parts or not parts[0]:
            continue
        m = re.match(r"^(\S+) (\d+):(\d+)$", parts[0])
        if not m:
            continue
        book, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
        key = (book, ch)
        if key not in mt_max or vs > mt_max[key]:
            mt_max[key] = vs

results = []
for book_key, karoli_book in BOOK_KEY_TO_KAROLI.items():
    eng_name = KAROLI_TO_ENGLISH_FOR_KEZI.get(karoli_book)
    kezi_fn = KEZI_ELTOLASOK.get(eng_name) if eng_name else None

    chapters = sorted(set(ch for (b, ch) in karoli_max if b == karoli_book))
    for ch in chapters:
        k = karoli_max.get((karoli_book, ch))
        j = kjv_max.get((book_key, ch))
        t = mt_max.get((karoli_book, ch))

        is_kezi = False
        if kezi_fn:
            for vs in range(1, (max(k or 0, j or 0, t or 0) + 5)):
                if kezi_fn(ch, vs) is not None:
                    is_kezi = True
                    break

        # zsolt cim-eltolas: kulon osztaly, ha Karoli = KJV+d (d in 1,2) es MEG NEM KJV/MT-egyezo
        zsolt_cim = False
        if karoli_book == "Zsolt" and k is not None and j is not None:
            d = k - j
            if d in (1, 2) and (t is None or k != t):
                zsolt_cim = True

        if is_kezi:
            osztaly = "KEZI"
        elif k is not None and j is not None and k == j:
            osztaly = "KJV"
        elif k is not None and t is not None and k == t:
            osztaly = "MT"
        elif zsolt_cim:
            osztaly = "ZSOLT_CIM_ELTOLAS"
        else:
            osztaly = "EGYIK_SEM"

        results.append((karoli_book, book_key, ch, k, j, t, osztaly))

with open("naplok/KAROLI_KK1b_fejezetosztaly.tsv", "w", encoding="utf-8") as out:
    out.write("karoli_konyv\tbook_key\tfejezet\tkaroli_max\tkjv_max\tmt_max\tosztaly\n")
    for r in results:
        out.write("\t".join(str(x) if x is not None else "" for x in r) + "\n")

from collections import Counter
c = Counter(r[6] for r in results)
print(f"Osszesen {len(results)} fejezet, {len(BOOK_KEY_TO_KAROLI)} konyv")
print(c)

# uj konyvek kulon
uj = [r for r in results if r[1] in ("ezra", "nehemiah", "esther")]
print(f"\nEzsdras/Nehemias/Eszter: {len(uj)} fejezet")
print(Counter(r[6] for r in uj))

zsolt = [r for r in results if r[0] == "Zsolt"]
print(f"\nZsoltarok: {len(zsolt)} fejezet")
print(Counter(r[6] for r in zsolt))
