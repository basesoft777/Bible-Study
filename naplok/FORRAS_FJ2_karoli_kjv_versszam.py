import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

step_to_magyar = {}
with open("konkordancia/Konyv_normalizalo_tabla.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        step_to_magyar[parts[0]] = parts[1]

karoli_verses = {}
with open("konkordancia/Karoli_1908.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if not parts or not parts[0]:
            continue
        igehely = parts[0]
        magyar, chvs = igehely.split(" ", 1)
        karoli_verses.setdefault(magyar, set()).add(chvs)

books = {
    "Gen": "1Móz",
    "Exo": "2Móz",
    "Pro": "Péld",
}

files = {
    "Gen": "konkordancia/KJV_Strongs_Genesis.tsv",
    "Exo": "konkordancia/KJV_Strongs_Exodus.tsv",
    "Pro": "konkordancia/KJV_Strongs_Proverbs.tsv",
}

for step, path in files.items():
    magyar = books[step]
    kjv_verses = set()
    with open(path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0]:
                continue
            ref = parts[0]  # Gen.1.1
            bits = ref.split(".")
            if len(bits) != 3:
                continue
            chvs = f"{bits[1]}:{bits[2]}"
            kjv_verses.add(chvs)
    kar = karoli_verses.get(magyar, set())
    only_kar = kar - kjv_verses
    only_kjv = kjv_verses - kar
    print(f"{magyar} ({step}): Károli={len(kar)} vers, KJV={len(kjv_verses)} vers, "
          f"csak Károliban={len(only_kar)}, csak KJV-ben={len(only_kjv)}")
    if only_kar:
        print("   csak Károliban:", sorted(only_kar)[:10])
    if only_kjv:
        print("   csak KJV-ben:", sorted(only_kjv)[:10])
