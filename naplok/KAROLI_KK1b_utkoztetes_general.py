import sys
import re
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# a terkep betoltese: Karoli_igehely -> lista (Heber_vers, Elteres_tipusa, Karoli_egyezik_hol)
terkep = defaultdict(list)
SIMPLE_REF_RE = re.compile(r"^[A-Za-z0-9]+\.(\d+):(\d+)$")
with open("konkordancia/LXX_versificacios_terkep.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        karoli_igehely, heber_vers, latin_vers, gorog_vers, elteres, egyezik_hol = parts[:6]
        terkep[karoli_igehely].append((heber_vers, elteres, egyezik_hol))

ELLENORZOTT_JELZOK = {"Heber", "Heber,Latin", "Heber,Gorog", "Heber,Latin,Gorog"}


def egyszeru_chvs(ref):
    m = SIMPLE_REF_RE.match(ref)
    if not m:
        return None
    return f"{int(m.group(1))}:{int(m.group(2))}"


egyezik_c = Counter()
utkozes_reszletek = []

out_rows = []
with open("naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv", encoding="utf-8") as f:
    header_line = f.readline()
    col_header = f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras, megjegyzes = parts[:6]

        terkep_sorok = terkep.get(igehely_karoli)
        if not terkep_sorok:
            terkep_utkozes = "NINCS_TERKEP_SOR"
            out_rows.append((igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras, megjegyzes, terkep_utkozes))
            egyezik_c[terkep_utkozes] += 1
            continue

        # a "varhato" MT-cel: ha van igehely_mt, azt hasznaljuk, kulonben a Karoli sajat ch:vs-et
        karoli_chvs = igehely_karoli.rsplit(" ", 1)[1]
        varhato = igehely_mt if igehely_mt else karoli_chvs

        allapotok = []
        for heber_vers, elteres, egyezik_hol in terkep_sorok:
            terkep_chvs = egyszeru_chvs(heber_vers)
            ellenorzott = egyezik_hol in ELLENORZOTT_JELZOK
            if terkep_chvs is None:
                allapotok.append(("OSSZETETT_TERKEP_SOR", ellenorzott, heber_vers))
                continue
            if terkep_chvs == varhato:
                allapotok.append(("EGYEZIK", ellenorzott, heber_vers))
            else:
                if ellenorzott:
                    allapotok.append(("UTKOZIK_ELLENORZOTT", ellenorzott, heber_vers))
                else:
                    allapotok.append(("UTKOZIK_ELLENORIZETLEN", ellenorzott, heber_vers))

        # prioritas: ha barmelyik sor UTKOZIK_ELLENORZOTT, az a dontő (K4: ez nem maradhat javitas/bizonyitas nelkul)
        statuszok = [a[0] for a in allapotok]
        if "UTKOZIK_ELLENORZOTT" in statuszok:
            terkep_utkozes = "UTKOZIK_ELLENORZOTT"
        elif "UTKOZIK_ELLENORIZETLEN" in statuszok:
            terkep_utkozes = "UTKOZIK_ELLENORIZETLEN"
        elif "EGYEZIK" in statuszok:
            terkep_utkozes = "EGYEZIK"
        else:
            terkep_utkozes = "OSSZETETT_TERKEP_SOR"

        egyezik_c[terkep_utkozes] += 1
        out_rows.append((igehely_karoli, igehely_kjv, igehely_mt, osztaly, forras, megjegyzes, terkep_utkozes))
        if terkep_utkozes in ("UTKOZIK_ELLENORZOTT", "UTKOZIK_ELLENORIZETLEN"):
            for heber_vers, elteres, egyezik_hol in terkep_sorok:
                utkozes_reszletek.append((igehely_karoli, osztaly, varhato, heber_vers, elteres, egyezik_hol, terkep_utkozes))

with open("naplok/KAROLI_KK1b_kulcstabla_tervezet_utkoztetve.tsv", "w", encoding="utf-8") as out:
    out.write("# GENERALT-TERVEZET: naplok/KAROLI_KK1b_utkoztetes_general.py - jovahagyasra var\n")
    out.write("igehely_karoli\tigehely_kjv\tigehely_mt\tosztaly\tforras\tmegjegyzes\tterkep_utkozes\n")
    for r in out_rows:
        out.write("\t".join(r) + "\n")

with open("naplok/KAROLI_KK1b_utkozes.tsv", "w", encoding="utf-8") as out:
    out.write("igehely_karoli\tosztaly\tvarhato_mt\tterkep_heber_vers\tterkep_elteres_tipusa\tterkep_egyezik_hol\tvegso_besorolas\n")
    for r in utkozes_reszletek:
        out.write("\t".join(r) + "\n")

print("A KK1b kulcstabla-tervezet terkep-utkoztetese, osztalyonkent:")
osztaly_x_utkozes = defaultdict(Counter)
for r in out_rows:
    osztaly_x_utkozes[r[3]][r[6]] += 1
for osztaly, c in osztaly_x_utkozes.items():
    print(f"  {osztaly}: {dict(c)}")

print(f"\nOsszesitve: {dict(egyezik_c)}")
print(f"Osszes tervezet-sor: {len(out_rows)}")
