import sys
import re
import random
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# kicsi, kezzel epitett Heber-Magyar tulajdonnev-forditasi tabla (TIPNR normalizalt nev -> Karoli-alak(ok))
NEV_TABLA = {
    "Moses": ["Mózes", "Mózesnek", "Mózesnél", "Mózessel", "Mózest"],
    "Aaron": ["Áron", "Áronnak", "Áronnal", "Áront"],
    "David": ["Dávid", "Dávidnak", "Dávidot", "Dávidnál"],
    "Solomon": ["Salamon", "Salamonnak", "Salamont"],
    "Israel": ["Izráel", "Izráelnek", "Izráelt", "izráeliták", "Izráelben"],
    "Judah": ["Júda", "Júdának", "Júdát"],
    "Jacob": ["Jákób", "Jákóbnak", "Jákóbot"],
    "Zion": ["Sion", "Sionnak", "Sionba", "Sionban", "Sionról"],
    "Abraham": ["Ábrahám", "Ábrahámnak", "Ábrahámot"],
    "Isaac": ["Izsák", "Izsáknak", "Izsákot"],
    "Joseph": ["József", "Józsefnek", "Józsefet"],
    "Joshua": ["Józsué", "Józsuénak", "Józsuét"],
    "Samuel": ["Sámuel", "Sámuelnek", "Sámuelt"],
    "Saul": ["Saul", "Saulnak", "Sault"],
    "Egypt": ["Égyiptom", "égyiptomi", "Égyiptomba", "Égyiptomból"],
    "Jerusalem": ["Jeruzsálem", "Jeruzsálembe", "Jeruzsálemben"],
    "Zion": ["Sion", "Sionnak", "Sionban"],
    "Babylon": ["Babilon", "babiloni"],
    "Assyria": ["Assiria", "assiriai"],
    "Ephraim": ["Efraim", "Efraimnak"],
    "Manasseh": ["Manasse", "Manassénak"],
    "Levi": ["Lévi", "Lévinek"],
    "Benjamin": ["Benjámin", "Benjáminnak"],
    "Elijah": ["Illés", "Illésnek"],
    "Elisha": ["Elizeus", "Elizeusnak"],
    "Isaiah": ["Ésaiás", "Ésaiásnak"],
    "Jeremiah": ["Jeremiás", "Jeremiásnak"],
    "Daniel": ["Dániel", "Dánielnek"],
    "Job": ["Jób", "Jóbnak"],
    "Sinai": ["Sinai"],
    "Jordan": ["Jordán", "Jordánon"],
}


def normalizalt(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


# TIPNR: Strong -> normalizalt nev(ek) ES nevvaltozat(ok) egyutt (mindket oszlop, mert a
# "normalizalt nev" a szemely VEGSO/kanonikus neve lehet, a tenyleges versben meg a korabbi
# nev (pl. H3290 normalizalt neve "Israel", de sok korai igehelyen meg "Jacob" a szoveg -
# l. KAROLI_KK1b_mintaproba modszertani megjegyzes)
tipnr = {}
with open("konkordancia/TIPNR_kivonat.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        nev, valtozat, strong = parts[0], parts[1], parts[2]
        key = strong.lstrip("H0") or "0"
        tipnr.setdefault(key, set()).add(nev)
        tipnr.setdefault(key, set()).add(valtozat)

# TAHOT: (konyv,ch,vs) -> lista strongokrol
tahot = {}
with open("konkordancia/TAHOT_kivonat.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2 or not parts[0]:
            continue
        m = re.match(r"^(\S+) (\d+):(\d+)$", parts[0])
        if not m:
            continue
        book, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
        strong = parts[1].lstrip("H0") or "0"
        tahot.setdefault((book, ch, vs), []).append(strong)

# Karoli szoveg
karoli_text = {}
with open("konkordancia/Karoli_1908.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2 or not parts[0]:
            continue
        karoli_text[parts[0]] = parts[1]

# fejezetosztaly betoltese, csak KJV/MT
kjv_fejezetek = []
mt_fejezetek = []
with open("naplok/KAROLI_KK1b_fejezetosztaly.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        karoli_konyv, book_key, ch, k, j, t, osztaly = parts
        if not k:
            continue
        if osztaly == "KJV":
            kjv_fejezetek.append((karoli_konyv, int(ch), int(k)))
        elif osztaly == "MT":
            mt_fejezetek.append((karoli_konyv, int(ch), int(k)))

random.seed(42)
minta_kjv = random.sample(kjv_fejezetek, max(1, round(len(kjv_fejezetek) * 0.10)))
minta_mt = random.sample(mt_fejezetek, max(1, round(len(mt_fejezetek) * 0.10)))

sorok = []
for osztaly_nev, minta in (("KJV", minta_kjv), ("MT", minta_mt)):
    for karoli_konyv, ch, karoli_max in minta:
        for vs in (1, karoli_max):
            igehely_karoli = f"{karoli_konyv} {ch}:{vs}"
            szoveg = karoli_text.get(igehely_karoli, "")
            szoveg_norm = normalizalt(szoveg)
            strongok = tahot.get((karoli_konyv, ch, vs), [])
            talalt_horgony = None
            talalt_egyezik = None
            for strong in strongok:
                nevek = tipnr.get(strong)
                if not nevek:
                    continue
                for nev in nevek:
                    alakok = NEV_TABLA.get(nev)
                    if not alakok:
                        continue
                    for alak in alakok:
                        if normalizalt(alak) in szoveg_norm:
                            talalt_horgony = f"H{strong}={nev}"
                            talalt_egyezik = True
                            break
                    if talalt_egyezik:
                        break
                if talalt_egyezik:
                    break
                # van tulajdonnev de nem egyezik szoveggel -- meg jelezzuk, ha van forditasi alakunk
                if strong in tipnr and any(NEV_TABLA.get(n) for n in tipnr[strong]):
                    talalt_horgony = f"H{strong}={list(tipnr[strong])[0]} (nincs egyezes)"
                    talalt_egyezik = False
            if talalt_horgony is None:
                allapot = "NINCS_ELLENORIZHETO_HORGONY"
            elif talalt_egyezik:
                allapot = "EGYEZIK"
            else:
                allapot = "NEM_EGYEZIK"
            sorok.append((osztaly_nev, igehely_karoli, talalt_horgony or "", allapot))

with open("naplok/KAROLI_KK1b_mintaproba.tsv", "w", encoding="utf-8") as f:
    f.write("osztaly\tigehely_karoli\thorgony\tallapot\n")
    for r in sorok:
        f.write("\t".join(r) + "\n")

from collections import Counter
c = Counter(r[3] for r in sorok)
print(f"Mintasorok osszesen: {len(sorok)} (KJV fejezetek: {len(minta_kjv)}, MT fejezetek: {len(minta_mt)}, seed=42)")
print(c)
ellenorizheto = c.get("EGYEZIK", 0) + c.get("NEM_EGYEZIK", 0)
if ellenorizheto:
    print(f"Az ellenorizheto (nevanchoros) mintan az egyezes: {c.get('EGYEZIK',0)}/{ellenorizheto} = {100*c.get('EGYEZIK',0)/ellenorizheto:.1f}%")
else:
    print("Nincs ellenorizheto (nevanchoros) mintasor a kis tablaval.")
