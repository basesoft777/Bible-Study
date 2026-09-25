import sys
import json
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SRC = "/tmp/lxxmorph_test/db/seeds/lxx_morph"

checks = [
    ("job-lxx", "Job", [("17", "13"), ("17", "16"), ("38", "7"), ("38", "16"), ("38", "30")]),
    ("hosea", "Hos", [("13", "14")]),
    ("jonah", "Jonah", [("2", "3"), ("2", "6")]),
    ("jeremiah-lxx", "Jer", [("51", "46")]),
    ("isaiah", "Isa", [("63", "13")]),
    ("joshua-vaticanus-b", "Josh", [("12", "4"), ("13", "12"), ("15", "8"), ("18", "16"), ("17", "15")]),
]

for slug, prefix, refs in checks:
    path = os.path.join(SRC, f"{slug}.json")
    if not os.path.exists(path):
        print(slug, "NINCS FÁJL A FORRÁSBAN")
        continue
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    all_refs = set(v["ref"] for v in data)
    for ch, vs in refs:
        found = False
        for p in (prefix, prefix.capitalize(), prefix.upper()):
            if f"{p} {ch}:{vs}" in all_refs:
                found = True
                break
        print(slug, f"{prefix} {ch}:{vs}", "MEGVAN a forrásban" if found else "TÉNYLEG HIÁNYZIK a forrásból is")
