import sys
import re
import glob
import os
import unicodedata
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    if sx == 0 or sy == 0:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / (sx * sy)


def normalizalt(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


NEV_TABLA = {
    "Moses": ["Mózes"], "Aaron": ["Áron"], "David": ["Dávid"], "Solomon": ["Salamon"],
    "Israel": ["Izráel", "Jákób"], "Judah": ["Júda"], "Jacob": ["Jákób"],
    "Abraham": ["Ábrahám"], "Isaac": ["Izsák"], "Joseph": ["József"],
    "Joshua": ["Józsué"], "Samuel": ["Sámuel"], "Saul": ["Saul"],
    "Egypt": ["Égyiptom", "égyiptomi"], "Jerusalem": ["Jeruzsálem", "Zion", "Sion"],
    "Zion": ["Sion"], "Babylon": ["Babilon"], "Assyria": ["Assiria"],
    "Ephraim": ["Efraim"], "Manasseh": ["Manasse"], "Levi": ["Lévi"],
    "Benjamin": ["Benjámin"], "Elijah": ["Illés"], "Elisha": ["Elizeus"],
    "Isaiah": ["Ésaiás"], "Jeremiah": ["Jeremiás"], "Daniel": ["Dániel"],
    "Job": ["Jób"], "Sinai": ["Sinai"], "Jordan": ["Jordán"],
    "Absalom": ["Absolon", "Absalom"], "Edom": ["Edom"],
}

SLUG_TO_KAROLI = {}
for line in open("eszkozok/lxx_os_import.py", encoding="utf-8"):
    pass

# Ujratoltjuk a BOOK_KEY_TO_KAROLI-t es a slug->book_key parositast az importerbol.
sys.path.insert(0, "eszkozok")
import lxx_os_import as LX  # noqa: E402

for slug, (title, book_key, testament) in LX.BOOKS.items():
    karoli_book = LX.BOOK_KEY_TO_KAROLI.get(book_key)
    if karoli_book:
        SLUG_TO_KAROLI[slug] = (karoli_book, book_key)

# Karoli szoveg es szoszam
karoli_text = {}
with open("konkordancia/Karoli_1908.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2 or not parts[0]:
            continue
        karoli_text[parts[0]] = parts[1]

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

# TAHOT: (konyv,ch,vs) -> strongok, TIPNR: strong -> nevek
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

# Ujonnan kitoltott parok betoltese, fejezetenkent csoportositva
# kulcs: (karoli_book, karoli_fejezet) -> lista (slug, raw_vers, karoli_vers)
fejezetek = defaultdict(list)
with open("naplok/KAROLI_KK7_ujonnan_kitoltott.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        slug, igehely_lxx, igehely_karoli = parts
        if slug not in SLUG_TO_KAROLI:
            continue
        karoli_book, book_key = SLUG_TO_KAROLI[slug]
        m_raw = re.search(r"(\d+):(\d+)$", igehely_lxx)
        m_kar = re.match(r"^(\S+) (\d+):(\d+)$", igehely_karoli)
        if not m_raw or not m_kar:
            continue
        raw_ch, raw_v = int(m_raw.group(1)), int(m_raw.group(2))
        kar_ch, kar_v = int(m_kar.group(2)), int(m_kar.group(3))
        fejezetek[(karoli_book, kar_ch)].append((slug, raw_ch, raw_v, kar_v))

# LXX szoszam versenkent, fajlonkent (cache)
lxx_szoszam_cache = {}


def lxx_szoszam(slug, raw_ch, raw_v):
    if slug not in lxx_szoszam_cache:
        d = {}
        path = f"konkordancia/LXX_OS/{slug}.tsv"
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or line.startswith("igehely_lxx"):
                    continue
                parts = line.split("\t")
                if len(parts) < 1:
                    continue
                d[parts[0]] = d.get(parts[0], 0) + 1
        lxx_szoszam_cache[slug] = d
    igehely = None
    for k in lxx_szoszam_cache[slug]:
        m = re.search(rf"{raw_ch}:{raw_v}$", k)
        if m:
            igehely = k
            break
    return lxx_szoszam_cache[slug].get(igehely, 0) if igehely else 0


def karoli_szoszam(karoli_book, ch, vs):
    key = f"{karoli_book} {ch}:{vs}"
    txt = karoli_text.get(key)
    if not txt:
        return None
    return len(txt.split())


eredmenyek = []

for (karoli_book, kar_ch), sorok in sorted(fejezetek.items()):
    n = len(sorok)
    korrelaciok = {}
    for shift in (-2, -1, 0, 1, 2):
        xs, ys = [], []
        hianyos = False
        for slug, raw_ch, raw_v, kar_v in sorok:
            cel_v = kar_v + shift
            if cel_v < 1:
                hianyos = True
                continue
            ks = karoli_szoszam(karoli_book, kar_ch, cel_v)
            if ks is None:
                hianyos = True
                continue
            ls = lxx_szoszam(slug, raw_ch, raw_v)
            xs.append(ls)
            ys.append(ks)
        r = pearson(xs, ys) if len(xs) >= 4 else None
        korrelaciok[shift] = (r, len(xs), hianyos)

    r0 = korrelaciok[0][0]
    rendezve = sorted(
        [(shift, r) for shift, (r, cnt, hi) in korrelaciok.items() if r is not None],
        key=lambda x: -x[1],
    )

    # Horgony: a valasztott (shift=0) Karoli-celversben van-e olyan TIPNR-nev,
    # amelynek Heber Stronga a Karoli-versben tenyleg megjelenik. CSAK akkor
    # dont, ha a korrelacios proba nem merheto (§1: "nem merheto fejezet ...
    # csak akkor fogadhato el, ha a horgony megerositi") -- egy generikus
    # nev (pl. "Israel") egy jol mereheto, egyertelmuen ELUTASITOTT fejezetben
    # NEM irhatja felul a szamszeru bizonyitekot (G1: ures jobb, mint hibas).
    horgony_info = "nincs"
    horgony_egyezik = False
    for slug, raw_ch, raw_v, kar_v in sorok:
        strongok = tahot.get((karoli_book, kar_ch, kar_v), [])
        for s in strongok:
            nevek = tipnr.get(s)
            if not nevek:
                continue
            for nev in nevek:
                alakok = NEV_TABLA.get(nev)
                if not alakok:
                    continue
                szoveg = normalizalt(karoli_text.get(f"{karoli_book} {kar_ch}:{kar_v}", ""))
                for alak in alakok:
                    if normalizalt(alak) in szoveg:
                        horgony_info = f"H{s}={nev}"
                        horgony_egyezik = True
                        break
                if horgony_egyezik:
                    break
        if horgony_egyezik:
            break

    elfogadott_eltolas = 0
    if r0 is None:
        # nem merheto korrelacioval (pl. <4 hasznalhato par, vagy hianyos eltolt-vers)
        dontes = "elfogad" if horgony_egyezik else "ures"
        indok = "horgony_nem_merheto" if horgony_egyezik else "nem_merheto_es_nincs_horgony"
    else:
        # a legjobb eltolast valasztjuk (nem csak a jelenlegi shift=0-t nezzuk) --
        # G2: "elfogadott eltolas", ami eltérhet a jelenlegi (0) erteketol, ha a
        # korrelacio azt mutatja, hogy a tobbletvers nem a fejezet elejen van
        # (l. brief 0.6: Ézs 63 pelda, ahol a helyes eltolas shift=-1 a jelenlegihez kepest).
        legjobb_shift, legjobb_r = rendezve[0]
        masodik_r = rendezve[1][1] if len(rendezve) > 1 else -2.0
        elfogadhato = legjobb_r >= 0.60 and (legjobb_r - masodik_r) >= 0.15
        if elfogadhato:
            dontes, indok = "elfogad", ("korrelacio" if legjobb_shift == 0 else "korrelacio_korrekcio")
            elfogadott_eltolas = legjobb_shift
        else:
            # mereheto, de egyik eltolas sem eleg eros/egyertelmu -- G1 szerint ures
            # marad, a horgony itt NEM irhatja felul a szamszeru bizonytalansagot
            dontes, indok = "ures", "korrelacio_nem_elegseges"

    eredmenyek.append((
        karoli_book, kar_ch, n,
        f"{korrelaciok[-2][0]:.2f}" if korrelaciok[-2][0] is not None else "",
        f"{korrelaciok[-1][0]:.2f}" if korrelaciok[-1][0] is not None else "",
        f"{korrelaciok[0][0]:.2f}" if korrelaciok[0][0] is not None else "",
        f"{korrelaciok[1][0]:.2f}" if korrelaciok[1][0] is not None else "",
        f"{korrelaciok[2][0]:.2f}" if korrelaciok[2][0] is not None else "",
        horgony_info, dontes, indok, str(elfogadott_eltolas),
    ))

with open("naplok/KAROLI_KK7_fejezet_dontes.tsv", "w", encoding="utf-8") as out:
    out.write("karoli_konyv\tfejezet\tn\tr_m2\tr_m1\tr_0\tr_p1\tr_p2\thorgony\tdontes\tindok\telfogadott_eltolas\n")
    for r in eredmenyek:
        out.write("\t".join(str(x) for x in r) + "\n")

elfogadott = sum(1 for r in eredmenyek if r[9] == "elfogad")
ures = sum(1 for r in eredmenyek if r[9] == "ures")
print(f"Osszes vizsgalt fejezet: {len(eredmenyek)}")
print(f"Elfogadva: {elfogadott}")
print(f"Uresre allitva: {ures}")
for r in eredmenyek:
    print(" ", r)
