import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

VP_PATH = "/tmp/lxxmorph_test/db/seeds/mt_alignment/verse_pairs.jsonl"

magyar_to_slug = {
    "Jób": "job",
    "Hós": "hosea",
    "Jón": "jonah",
    "Jer": "jeremiah",
    "Józs": "joshua",
    "Ézs": "isaiah",
}

rows = [
    ("ALVIL-001", "Jób 17:13"),
    ("ALVIL-001", "Jób 17:16"),
    ("ALVIL-001", "Hós 13:14"),
    ("ALVIL-001", "Jón 2:3"),
    ("HAMART-001", "Jer 51:46"),
    ("HODIT-001", "Józs 12:4"),
    ("HODIT-001", "Józs 13:12"),
    ("HODIT-001", "Józs 15:8"),
    ("HODIT-001", "Józs 18:16"),
    ("HODIT-001", "Józs 17:15"),
    ("MENNY-001", "Jób 38:7"),
    ("TEREMT-001", "Jób 38:16"),
    ("TEREMT-001", "Jób 38:30"),
    ("TEREMT-001", "Ézs 63:13"),
    ("TEREMT-001", "Jón 2:6"),
]

# reverse index: (mt_book, mt_ref) -> list of (grk_ref, method)
rev = {}
with open(VP_PATH, encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        for mt_ref in d.get("mt_refs", []):
            rev.setdefault((d["mt_book"], mt_ref), []).append((d["grk_ref"], d["method"]))

out = []
for motivum, igehely in rows:
    magyar, chvs = igehely.split(" ", 1)
    ch, vs = chvs.split(":")
    slug = magyar_to_slug[magyar]
    key = (slug, f"{ch}:{vs}")
    matches = rev.get(key)
    if matches:
        grk_refs = "; ".join(f"{g} ({m})" for g, m in matches)
        besorolas = "megoldva" if len(matches) == 1 and matches[0][1] == "identity" else "megoldva_athelyezessel"
        out.append((motivum, igehely, grk_refs, besorolas))
    else:
        out.append((motivum, igehely, "NINCS_PARBAN", "valodi_eltres_kutatoi_kerdes"))

with open("naplok/FORRAS_FJ2_szamozas.tsv", "w", encoding="utf-8") as f:
    f.write("motivum\tigehely_mt\tlxx_igehely_javasolt\tbesorolas\n")
    for r in out:
        f.write("\t".join(r) + "\n")

for r in out:
    print(r)
