import sys
import hashlib
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

LXX_MORPH_COMMIT = "c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2"
VERSE_PAIRS_SHA256 = "3a91c571f1f32545f78397a256fdfa5124bcbcbc42902411a8a93209dcb2e985"

rows_by_karoli = {}
with open("naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv", encoding="utf-8") as f:
    f.readline()
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras, megjegyzes = parts[:6]
        rows_by_karoli.setdefault(igehely_karoli, []).append(
            (igehely_kjv, igehely_mt, osztaly, forras, megjegyzes))

final_rows = []
osszevont = []
for igehely_karoli, sorok in sorted(rows_by_karoli.items()):
    if len(sorok) == 1:
        final_rows.append((igehely_karoli,) + sorok[0])
        continue
    # tobb sor - preferaljuk az explicit "kezi"-t a "kezi_identitas_javitas" felett
    kezi_sorok = [s for s in sorok if s[3] == "kezi"]
    if len(kezi_sorok) == 1:
        final_rows.append((igehely_karoli,) + kezi_sorok[0])
        osszevont.append((igehely_karoli, "kezi_elsobbseget_elvez_identitas_felett", len(sorok)))
    elif len(kezi_sorok) > 1:
        # tobb explicit kezi forras is ugyanoda mutat (pl. Pred 2:25+2:26 -> 2:26 osszevonas)
        raw_forrasok = ";".join(s[4] for s in kezi_sorok)
        igehely_kjv, igehely_mt, osztaly, forras, _ = kezi_sorok[0]
        final_rows.append((igehely_karoli, igehely_kjv, igehely_mt, osztaly,
                            "kezi_tobbforrasu_osszevonas", raw_forrasok))
        osszevont.append((igehely_karoli, "tobb_kezi_forras_osszevonva", len(sorok)))
    else:
        # nem vart eset - az elsot tartjuk meg, jelezve
        final_rows.append((igehely_karoli,) + sorok[0])
        osszevont.append((igehely_karoli, "VARATLAN_TOBBSOR_NEM_KEZI", len(sorok)))

out_path = "konkordancia/Karoli_versmegfeleltetes.tsv"
with open(out_path, "w", encoding="utf-8") as out:
    out.write("# GENERÁLT: naplok/KAROLI_KK4_tabla_veglegesit.py — kézzel nem szerkesztendő.\n")
    out.write(f"# forras: lxx-morph@{LXX_MORPH_COMMIT} (verse_pairs.jsonl, TVTMS-alapu MT-KJV kulcs, CC BY 4.0) "
              f"+ Karoli_1908.tsv + TAHOT_kivonat.tsv + eszkozok/lxx_kivonat_fetch_v2.py KEZI_ELTOLASOK\n")
    out.write(f"# sha256(verse_pairs.jsonl)={VERSE_PAIRS_SHA256}\n")
    out.write("# proveniencia: forras=KAROLI_KULCS_BRIEF.md KK4 (2. menet) | ts=2026-09-25\n")
    out.write("igehely_karoli\tigehely_kjv\tigehely_mt\tosztaly\tforras\tmegjegyzes\n")
    for r in final_rows:
        out.write("\t".join(r) + "\n")

print(f"Vegleges tabla: {len(final_rows)} sor -> {out_path}")
print(f"Osszevont/duplikalt-feloldott sorok: {len(osszevont)}")
for o in osszevont:
    print(" ", o)

with open(out_path, "rb") as f:
    print("sha256:", hashlib.sha256(f.read()).hexdigest())
