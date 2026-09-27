import sys
import json
import re
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, "eszkozok")
import lxx_os_import as LX  # noqa: E402

BOOK_KEY_TO_KAROLI = LX.BOOK_KEY_TO_KAROLI

# fejezet dontesek (csak azok a konyv/fejezet, amit a KK7 "elfogad"-ott)
fejezet_dontes = {}
with open("naplok/KAROLI_KK7_fejezet_dontes.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 12:
            continue
        fejezet_dontes[(parts[0], int(parts[1]))] = (parts[9], int(parts[11]))

# verse_pairs.jsonl: (mt_book, mt_ref) -> lista grk_ref-ekbol, csak method!=unpaired, len(mt_refs)==1
cel_forrasok = defaultdict(list)
with open("/tmp/lxx_os_forras/verse_pairs.jsonl", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        mt_refs = d.get("mt_refs") or []
        if d.get("method") == "unpaired" or len(mt_refs) != 1:
            continue
        m = re.match(r"^(\d+):(\d+)$", mt_refs[0])
        gm = re.match(r"^(\d+):(\d+)$", d["grk_ref"])
        if not m or not gm:
            continue
        key = (d["mt_book"], int(m.group(1)), int(m.group(2)))
        cel_forrasok[key].append((d["grk_book"], int(gm.group(1)), int(gm.group(2))))

talalatok = []
for (mt_book, kjv_ch, kjv_v), forrasok in cel_forrasok.items():
    if len(forrasok) < 2:
        continue
    karoli_book = BOOK_KEY_TO_KAROLI.get(mt_book)
    if not karoli_book:
        continue
    fejezetek_erintve = set(f[1] for f in forrasok)
    if len(fejezetek_erintve) < 2:
        continue  # ugyanazon fejezeten beluli duplikacio (pl. Zsoltar-cim) -- mar kezelve
    dontes, korrekcio = fejezet_dontes.get((karoli_book, kjv_ch), ("nincs_adat", 0))
    if dontes != "elfogad":
        continue  # csak az elfogadott fejezeteket erinti a KK7-korrekcio
    talalatok.append((karoli_book, kjv_ch, kjv_v, sorted(forrasok), dontes, korrekcio))

with open("naplok/KAROLI_KK75_hatarkereses2.tsv", "w", encoding="utf-8") as out:
    out.write("karoli_konyv\tkjv_fejezet\tkjv_vers\tforrasok\tfejezet_dontes\tkorrekcio\n")
    for t in talalatok:
        out.write("\t".join(str(x) for x in t) + "\n")

print(f"Fejezethatart atlepo, tobbszoros hivatkozasu KJV-cel, elfogadott fejezetben: {len(talalatok)}")
for t in talalatok:
    print(" ", t)
