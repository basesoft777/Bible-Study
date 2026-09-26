import sys
import re
import glob
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# csak az UJONNAN kitoltott sorok erdekelnek (a KK7 altal bevezetett ket
# mechanizmus: kezi_eltolas_tabla H1-fallback resze, es mt_szamozas_kovetes)
UJ_MECHANIZMUS = {"kezi_eltolas_tabla", "mt_szamozas_kovetes"}

karoli_max = {}
with open("konkordancia/Karoli_1908.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if not parts or not parts[0]:
            continue
        m = re.match(r"^(\S+) (\d+):(\d+)$", parts[0])
        if not m:
            continue
        book, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
        key = (book, ch)
        if key not in karoli_max or vs > karoli_max[key]:
            karoli_max[key] = vs

# minden LXX_OS sor -- egyedi (fajl, igehely_lxx) -> (igehely_karoli, karoli_ok)
sorok = []
for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    slug = path.split("/")[-1].replace(".tsv", "")
    seen = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            igehely_lxx, igehely_karoli, karoli_ok = parts[0], parts[2], parts[3]
            if (slug, igehely_lxx) in seen:
                continue
            seen.add((slug, igehely_lxx))
            if karoli_ok not in UJ_MECHANIZMUS or not igehely_karoli:
                continue
            m = re.match(r"^(\S+) (\d+):(\d+)$", igehely_karoli)
            if not m:
                continue
            kar_book, kar_ch, kar_v = m.group(1), int(m.group(2)), int(m.group(3))
            m2 = re.search(r"(\d+):(\d+)$", igehely_lxx)
            raw_ch, raw_v = (int(m2.group(1)), int(m2.group(2))) if m2 else (None, None)
            sorok.append((slug, igehely_lxx, raw_ch, raw_v, igehely_karoli, kar_book, kar_ch, kar_v, karoli_ok))

talalatok = []

# ismert, dokumentalt sok-az-egyhez osszevonasok (KK2/KK4-bol) -- ezek
# szandekos KEZI_ELTOLASOK-forrasu merge-ek, nem hibak
ISMERT_OSSZEVONAS = {
    "Préd 9:20", "Préd 12:15", "Jób 39:31", "4Móz 13:34", "Préd 9:19",
    "Jób 39:32", "Préd 2:26", "Préd 12:16", "Jób 39:33",
}

# (a) ket kulonbozo LXX-vers ugyanarra a Karoli-versre mutat -- CSAK ugyanazon
# LXX-fajlon (slug) belul: a kulonbozo szoveg-tanuk (pl. daniel vs
# daniel-theodotion, joshua vs joshua-vaticanus-b) legitim, fuggetlen
# forrasok, ugyanarra a Karoli-celra mutatva -- ez nem hiba.
karoli_to_lxx = defaultdict(list)
for r in sorok:
    karoli_to_lxx[(r[0], r[4])].append(r)  # kulcs: (slug, igehely_karoli)
for (slug, kar), lista in karoli_to_lxx.items():
    if kar in ISMERT_OSSZEVONAS:
        continue
    egyedi_forras = set(r[1] for r in lista)
    if len(egyedi_forras) > 1:
        for r in lista:
            talalatok.append((r[1], r[4], "(a) tobbes_hivatkozas",
                               f"ugyanabban a fajlban ({slug}) tovabbi forras ugyanarra: "
                               f"{sorted(x for x in egyedi_forras if x != r[1])}"))

# (b) fejezethatart atlepo hozzarendeles (raw fejezet != karoli fejezet, ES a konyv
# ugyanaz -- tehat nem konyv-szintu deuterokanonikus elteres, hanem valodi fejezet-atlepes
# EGY konyvon belul)
for r in sorok:
    slug, igehely_lxx, raw_ch, raw_v, igehely_karoli, kar_book, kar_ch, kar_v, ok = r
    if raw_ch is not None and raw_ch != kar_ch:
        talalatok.append((igehely_lxx, igehely_karoli, "(b) fejezethatar_atlepes",
                           f"nyers fejezet={raw_ch}, karoli fejezet={kar_ch}"))

# (c) egy elfogadott fejezetben Karoli-vers marad ki a sorozatbol -- azok a
# fejezetek, amelyekben van ujonnan kitoltott sor: nezzuk meg, a kitoltott
# karoli-versek + a MAR korabban is kitoltott karoli-versek egyutt lefedik-e
# a fejezet 1..max tartomanyat folytonosan, VAGY legalabb nincs-e olyan
# ujonnan kitoltott sor, amely at nem fedett szomszedos hezagot hagy maga utan
fejezet_uj_versek = defaultdict(set)
for r in sorok:
    slug, igehely_lxx, raw_ch, raw_v, igehely_karoli, kar_book, kar_ch, kar_v, ok = r
    fejezet_uj_versek[(kar_book, kar_ch)].add(kar_v)

# korabban mar kitoltott karoli-versek fejezetenkent (barmely karoli_ok=="" vagy
# mas "regi" mechanizmus -- mindent, ami NEM a ket uj mechanizmusban van)
fejezet_regi_versek = defaultdict(set)
for path in sorted(glob.glob("konkordancia/LXX_OS/*.tsv")):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("igehely_lxx"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            igehely_karoli, karoli_ok = parts[2], parts[3]
            if not igehely_karoli or karoli_ok in UJ_MECHANIZMUS:
                continue
            m = re.match(r"^(\S+) (\d+):(\d+)$", igehely_karoli)
            if not m:
                continue
            fejezet_regi_versek[(m.group(1), int(m.group(2)))].add(int(m.group(3)))

for (kar_book, kar_ch), uj_versek in fejezet_uj_versek.items():
    teljes = uj_versek | fejezet_regi_versek.get((kar_book, kar_ch), set())
    max_v = karoli_max.get((kar_book, kar_ch))
    if max_v is None:
        continue
    hianyzo = set(range(1, max_v + 1)) - teljes
    if hianyzo:
        talalatok.append((f"{kar_book} {kar_ch} (fejezet)", "", "(c) hianyzo_karoli_vers",
                           f"hianyzo versek a fejezetbol: {sorted(hianyzo)}"))

with open("naplok/KAROLI_KK75_hatarkereses.tsv", "w", encoding="utf-8") as out:
    out.write("lxx_igehely\tmost\ttipus\tbizonyitek\n")
    for t in talalatok:
        out.write("\t".join(str(x) for x in t) + "\n")

print(f"Osszes talalat: {len(talalatok)}")
for t in talalatok:
    print(" ", t)
