import sys
import re
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# TAHOT verslistak konyvenkent (a "letezik-e ilyen MT-vers" horgony)
tahot_versek = {}  # karoli_konyv -> set of (ch,vs)
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
        tahot_versek.setdefault(book, set()).add((ch, vs))

rows = []
with open("naplok/KAROLI_KK1b_utkozes.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        igehely_karoli, osztaly, varhato_mt, terkep_heber, elteres, egyezik_hol, besorolas = parts
        if besorolas != "UTKOZIK_ELLENORIZETLEN":
            continue
        rows.append((igehely_karoli, osztaly, varhato_mt, terkep_heber, elteres, egyezik_hol))

SIMPLE_REF_RE = re.compile(r"^[A-Za-z0-9]+\.(\d+):(\d+)$")

dontesek = Counter()
out = []
for igehely_karoli, osztaly, varhato_mt, terkep_heber, elteres, egyezik_hol in rows:
    book = igehely_karoli.rsplit(" ", 1)[0]
    m1 = re.match(r"^(\d+):(\d+)$", varhato_mt)
    sajat_van = False
    if m1:
        sajat_van = (int(m1.group(1)), int(m1.group(2))) in tahot_versek.get(book, set())

    m2 = SIMPLE_REF_RE.match(terkep_heber)
    terkep_van = False
    if m2:
        terkep_van = (int(m2.group(1)), int(m2.group(2))) in tahot_versek.get(book, set())

    if sajat_van and not terkep_van:
        dontes = "TERVEZET_MARAD (a terkep celja nincs a TAHOT-ban, a mienk igen)"
    elif terkep_van and not sajat_van:
        dontes = "TERKEP_JAVASOLT_JAVITAS (a terkep celja van a TAHOT-ban, a mienk nincs)"
    elif sajat_van and terkep_van:
        dontes = "BIZONYTALAN_MINDKETTO_LETEZIK (kezi tartalmi egyeztetes kell)"
    else:
        dontes = "BIZONYTALAN_EGYIK_SEM_LETEZIK (osszetett/tartomanyos terkep-sor, kezi kell)"

    dontesek[dontes] += 1
    out.append((igehely_karoli, osztaly, varhato_mt, terkep_heber, egyezik_hol, dontes))

with open("naplok/KAROLI_KK1b_terkep_javaslat.tsv", "w", encoding="utf-8") as f:
    f.write("igehely_karoli\tosztaly\tvarhato_mt\tterkep_heber_vers\tterkep_egyezik_hol\tautomatikus_horgony_dontes\n")
    for r in out:
        f.write("\t".join(r) + "\n")

print(f"UTKOZIK_ELLENORIZETLEN sorok: {len(rows)}")
print("Automatikus TAHOT-letezesi horgony dontesek:")
for k, v in dontesek.most_common():
    print(f"  {k}: {v}")

javitando = [r for r in out if r[5].startswith("TERKEP_JAVASOLT_JAVITAS")]
print(f"\nA terkep sajat javitando sorai (a 15 lexikon-sorhoz kapcsolodo minta, max 10):")
for r in javitando[:10]:
    print(" ", r)
