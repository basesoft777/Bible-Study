import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, "eszkozok")
from lxx_kivonat_fetch_v2 import KEZI_ELTOLASOK  # noqa: E402

BOOK_KEY_TO_KAROLI = {
    "genesis": "1Móz", "exodus": "2Móz", "leviticus": "3Móz", "numbers": "4Móz",
    "deuteronomy": "5Móz", "joshua": "Józs", "judges": "Bír", "ruth": "Ruth",
    "1-samuel": "1Sám", "2-samuel": "2Sám", "1-kings": "1Kir", "2-kings": "2Kir",
    "1-chronicles": "1Krón", "2-chronicles": "2Krón", "job": "Jób", "psalms": "Zsolt",
    "proverbs": "Péld", "ecclesiastes": "Préd", "song-of-solomon": "Én", "isaiah": "Ézs",
    "jeremiah": "Jer", "lamentations": "Sir", "ezekiel": "Ez", "daniel": "Dán",
    "hosea": "Hós", "joel": "Jóel", "amos": "Ámós", "obadiah": "Abd", "jonah": "Jón",
    "micah": "Mik", "nahum": "Náh", "habakkuk": "Hab", "zephaniah": "Sof",
    "haggai": "Hag", "zechariah": "Zak", "malachi": "Mal",
}
KAROLI_TO_ENGLISH_FOR_KEZI = {
    "4Móz": "Numbers", "Jób": "Job", "Préd": "Ecclesiastes", "Dán": "Daniel",
}

# fejezetosztaly
fejezetosztaly = {}
with open("naplok/KAROLI_KK1_fejezetosztaly.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        karoli_konyv, book_key, ch = parts[0], parts[1], int(parts[2])
        k = int(parts[3]) if parts[3] else None
        fejezetosztaly[(karoli_konyv, ch)] = (parts[6], book_key, k)

# Karoli 1908 versek (ellenorzott, ures-helyorzok nelkul)
ures_helyorzo = set()
with open("konkordancia/Karoli_ures_helyorzo_sorok.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts and parts[0]:
            ures_helyorzo.add(parts[0])

karoli_versek = {}  # (konyv,fejezet) -> sorted list of versek
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
        if book not in BOOK_KEY_TO_KAROLI.values():
            continue
        karoli_versek.setdefault((book, ch), set()).add(vs)

# MT->KJV forditott index (verse_pairs.jsonl alapjan): (mt_book, ch, vs) -> kjv_ref (masolat, azonos szamozas -- a "kjv" itt maga a mt_refs-bol szarmazo cel)
mt_to_kjv = {}
with open("/tmp/lxxmorph_test/db/seeds/mt_alignment/verse_pairs.jsonl", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        if len(d.get("mt_refs", [])) != 1:
            continue
        mt_ref = d["mt_refs"][0]
        m = re.match(r"^(\d+):(\d+)$", mt_ref)
        if not m:
            continue
        key = (d["mt_book"], int(m.group(1)), int(m.group(2)))
        mt_to_kjv[key] = mt_ref  # a KJV szamozas maga is ch:vs alakban, csak ez a "kanonikus" KJV-cel

out_rows = []
stat = {"KJV": 0, "MT": 0, "KEZI": 0, "EGYIK_SEM_kihagyva": 0}

for (book, ch), versek in sorted(karoli_versek.items()):
    osztaly, book_key, karoli_max = fejezetosztaly.get((book, ch), (None, None, None))
    if osztaly is None:
        continue
    eng_name = KAROLI_TO_ENGLISH_FOR_KEZI.get(book)
    kezi_fn = KEZI_ELTOLASOK.get(eng_name) if eng_name else None

    if osztaly == "EGYIK_SEM":
        stat["EGYIK_SEM_kihagyva"] += len(versek)
        continue

    if osztaly == "KEZI":
        # kezi_fn(raw_fejezet, raw_vers) -> (karoli_fejezet, karoli_vers) vagy None (=identitas, G4 javitas)
        # csak a "hazai" fejezet tartomanyat jarjuk be (0..karoli_max+5 vers), es a celt visszaindexeljuk
        for raw_vers in range(1, (karoli_max or 0) + 10):
            cel = kezi_fn(ch, raw_vers) if kezi_fn else None
            if cel is not None:
                karoli_ch, karoli_vs = cel
            else:
                karoli_ch, karoli_vs = ch, raw_vers
            if karoli_ch != ch:
                continue  # mas fejezetbe eso celokat ott a sajat fejezet-korben kezeljuk
            if karoli_vs not in versek:
                continue
            igehely_karoli = f"{book} {karoli_ch}:{karoli_vs}"
            igehely_kjv = ""
            igehely_mt = ""
            mt_key = (book_key, ch, raw_vers)
            if mt_key in mt_to_kjv:
                igehely_kjv = mt_to_kjv[mt_key]
            forras = "kezi" if kezi_fn and kezi_fn(ch, raw_vers) is not None else "kezi_identitas_javitas"
            out_rows.append((igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras,
                              f"raw={ch}:{raw_vers}"))
            stat["KEZI"] += 1
        continue

    if osztaly == "KJV":
        for vs in sorted(versek):
            igehely_karoli = f"{book} {ch}:{vs}"
            igehely_kjv = f"{ch}:{vs}"
            igehely_mt = ""
            mt_key = (book_key, ch, vs)
            forras = "szamlalas"
            out_rows.append((igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras, ""))
            stat["KJV"] += 1
        continue

    if osztaly == "MT":
        for vs in sorted(versek):
            igehely_karoli = f"{book} {ch}:{vs}"
            igehely_mt = f"{ch}:{vs}"
            mt_key = (book_key, ch, vs)
            igehely_kjv = mt_to_kjv.get(mt_key, "")
            forras = "tvtms" if igehely_kjv else "szamlalas"
            out_rows.append((igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras, ""))
            stat["MT"] += 1
        continue

with open("naplok/KAROLI_KK2_kulcstabla_tervezet.tsv", "w", encoding="utf-8") as out:
    out.write("# GENERALT-TERVEZET: naplok/KAROLI_KK2_kulcstabla_general.py - jovahagyasra var, meg NEM elesitett\n")
    out.write("igehely_karoli\tigehely_kjv\tigehely_mt\tosztaly\tforras\tmegjegyzes\n")
    for r in out_rows:
        out.write("\t".join(r) + "\n")

print(f"Osszesen {len(out_rows)} Karoli-vers-sor a tervezetben")
print(stat)

# ervenyessegi probak
seen = set()
duplikalt = 0
for r in out_rows:
    if r[0] in seen:
        duplikalt += 1
    seen.add(r[0])
print(f"Duplikalt igehely_karoli sorok: {duplikalt}")
