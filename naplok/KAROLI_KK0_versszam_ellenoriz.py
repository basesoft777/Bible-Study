import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

karoli_max = {}
with open("konkordancia/Karoli_1908.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if not parts or not parts[0]:
            continue
        igehely = parts[0]
        m = re.match(r"^(\S+) (\d+):(\d+)$", igehely)
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

samples = [
    ("Jób", "job", 17),
    ("Jób", "job", 37),
    ("Jób", "job", 38),
    ("Jón", "jonah", 2),
    ("Hós", "hosea", 13),
    ("Ézs", "isaiah", 64),
]
for karoli_book, slug, ch in samples:
    k = karoli_max.get((karoli_book, ch))
    j = kjv_max.get((slug, ch))
    print(f"{karoli_book} {ch}: Karoli={k} / KJV={j}")
