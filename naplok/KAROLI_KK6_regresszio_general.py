import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

regressziok = []
osszes_regi_kitoltott = 0
osszes_uj_kitoltott = 0
valtozott_de_meg_kitoltott = 0

for old_path in sorted(glob.glob("konkordancia/_nyers/KK4_regresszio_elotte/*.tsv")):
    slug = old_path.split("/")[-1].replace(".tsv", "")
    new_path = f"konkordancia/LXX_OS/{slug}.tsv"

    regi = {}
    with open(old_path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            igehely_lxx, igehely_karoli, karoli_ok = parts[0], parts[1], parts[2]
            if igehely_lxx in regi:
                continue
            regi[igehely_lxx] = igehely_karoli

    uj = {}
    with open(new_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            igehely_lxx, igehely_karoli = parts[0], parts[2]
            if igehely_lxx in uj:
                continue
            uj[igehely_lxx] = igehely_karoli

    for igehely_lxx, regi_ertek in regi.items():
        if not regi_ertek:
            continue
        osszes_regi_kitoltott += 1
        uj_ertek = uj.get(igehely_lxx, "")
        if uj_ertek:
            osszes_uj_kitoltott += 1
        if uj_ertek != regi_ertek:
            ok = "uresre_valtozott" if not uj_ertek else "mas_celra_valtozott"
            regressziok.append((slug, igehely_lxx, regi_ertek, uj_ertek, ok))
            valtozott_de_meg_kitoltott += 1 if uj_ertek else 0

with open("naplok/KAROLI_KK6_regresszio.tsv", "w", encoding="utf-8") as out:
    out.write("fajl\tigehely_lxx\tregi\tuj\tok\n")
    for r in regressziok:
        out.write("\t".join(r) + "\n")

print(f"Korabban kitoltott sorok (osszes): {osszes_regi_kitoltott}")
print(f"Ezekbol most is kitoltott: {osszes_uj_kitoltott}")
print(f"Regresszios sorok (a regi kitoltott ertek MEGVALTOZOTT): {len(regressziok)}")
for r in regressziok:
    print(" ", r)
