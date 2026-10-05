"""F42 / DT-F42f (f3): a régi LXX_kivonat és az LXX_OS teljes, versenkénti összevetése.

A régi `konkordancia/LXX_kivonat_*.tsv` (studybible.info, LXX_WH + ABP) kivezetése előtt
készült eltéréslista: minden régi Károli-versre összeveti a régi Strong-multihalmazt az LXX_OS
(elsődleges szövegváltozat, `lxx_os_import.ELSODLEGES_SLUG`) `igehely_karoli` szerinti soraival.

    python eszkozok/lxx_osszevetes.py [--kimenet UT]

Kimenet (alapértelmezés): `naplok/FORRASKIVEZETES_M5_eltereslista.tsv`, csak az NEM azonos versek.
Kategóriák:
  strong_eltero      a Strong-multihalmazok Jaccard-hasonlósága >= 0,8 (jellemzően konvenció-eltérés)
  nagy_eltero        < 0,8 (szövegalap- vagy vers-hozzárendelés-eltérés)
  zsoltar_eltolas    a régi vers az LXX_OS KÖVETKEZŐ versével egyezik (a régi zsoltár-kivonat
                     egy verssel eltolt, N17); az átállás ezt JAVÍTJA
  csak_regi_vers     az LXX_OS-ben nincs Károli-kulcsos sor erre a versre
  csak_uj_vers       az LXX_OS-ben van, a régiben nincs
A régi fájlok kivezetése (F42.M5) után a szkript a régi adatot nem találja: a git-történetből
(`git show <F42 előtti commit>:konkordancia/LXX_kivonat_<Könyv>.tsv`) állítható vissza.
A proveniencia: manual (összevetés), nem lekérdezés.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import collections
import datetime
import os
import re
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lxx_os_import as OS  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")
LXX_OS_DIR = os.path.join(KONKORDANCIA_DIR, "LXX_OS")
KIMENET_PATH = os.path.join(REPO_ROOT, "naplok", "FORRASKIVEZETES_M5_eltereslista.tsv")

# Károli-rövidítés -> régi LXX_kivonat_<fajlnev>.tsv szuffixum
REGI_LXX_FAJLNEV = {
    "1Móz": "Genezis", "2Móz": "Exodus", "3Móz": "Leviticus", "4Móz": "Numeri",
    "5Móz": "Deuteronomium", "Józs": "Jozsue", "Bír": "Birak", "Ruth": "Ruth",
    "1Sám": "Samuel_1", "2Sám": "Samuel_2", "1Kir": "Kiralyok_1", "2Kir": "Kiralyok_2",
    "1Krón": "Kronikak_1", "2Krón": "Kronikak_2", "Ezsd": "Ezsdras", "Neh": "Nehemias",
    "Eszt": "Eszter", "Jób": "Job", "Zsolt": "Zsoltarok", "Péld": "Peldabeszedek",
    "Préd": "Predikator", "Én": "Enekek_Eneke", "Ézs": "Ezsaias", "Jer": "Jeremias",
    "Sir": "Siralmak", "Ez": "Ezekiel", "Dán": "Daniel", "Hós": "Hoseas",
    "Jóel": "Joel", "Ámós": "Amos", "Abd": "Abdias", "Jón": "Jonas", "Mik": "Mikeas",
    "Náh": "Nahum", "Hab": "Habakuk", "Sof": "Sofonias", "Hag": "Aggeus",
    "Zak": "Zakarias", "Mal": "Malakias",
}

HEADER = ["igehely", "kategoria", "regi_n", "uj_n", "jaccard", "uj_lxx_vers", "csak_regi_strong",
          "csak_uj_strong"]


def norm_strong(s):
    d = re.sub(r"\D", "", s or "")
    return "G" + d.zfill(4) if d.strip("0") else ""


def alak(s):
    s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()
    return s.replace("ς", "σ").replace("᾿", "").replace("'", "")


def olvas(path):
    sorok = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\r\n")
            if ln and not ln.startswith("#"):
                sorok.append(ln.split("\t"))
    return sorok[0], sorok[1:]


def uj_index():
    """igehely_karoli -> [sor-dict]; a könyvenkénti elsődleges fájlból."""
    elsodleges = {}
    for kb in set(OS.BOOK_KEY_TO_KAROLI.values()) | set(OS.ELSODLEGES_SLUG):
        elsodleges[OS.elsodleges_slug(kb)] = kb
    idx = collections.defaultdict(list)
    for slug in sorted(elsodleges):
        fejlec, sorok = olvas(os.path.join(LXX_OS_DIR, slug + ".tsv"))
        for p in sorok:
            r = dict(zip(fejlec, p))
            if r["igehely_karoli"]:
                idx[r["igehely_karoli"]].append(r)
    return idx


def regi_index(konyv):
    ut = os.path.join(KONKORDANCIA_DIR, "LXX_kivonat_%s.tsv" % REGI_LXX_FAJLNEV[konyv])
    if not os.path.isfile(ut):
        raise SystemExit("A régi LXX_kivonat kivezetve (F42); a git-történetből állítható vissza: %s" % ut)
    fejlec, sorok = olvas(ut)
    idx = collections.defaultdict(list)
    for p in sorok:
        r = dict(zip(fejlec, p))
        idx[r["Igehely"]].append(r)
    return idx


def jaccard(a, b):
    a2 = collections.Counter(k for k in a.elements() if k)
    b2 = collections.Counter(k for k in b.elements() if k)
    un = sum((a2 | b2).values())
    return (sum((a2 & b2).values()) / un) if un else 1.0


def kovetkezo_vers(igehely):
    m = re.match(r"^(.*?)(\d+):(\d+)$", igehely)
    return "%s%s:%d" % (m.group(1), m.group(2), int(m.group(3)) + 1)


def main():
    ut_ki = KIMENET_PATH
    if "--kimenet" in sys.argv:
        ut_ki = sys.argv[sys.argv.index("--kimenet") + 1]
    uj = uj_index()
    kat_db = collections.Counter()
    konyv_db = collections.defaultdict(collections.Counter)
    parok = collections.Counter()      # (régi Strong, új Strong) -> db, azonos szóalak mellett
    sorok_ki = []
    regi_osszes = set()
    for konyv in REGI_LXX_FAJLNEV:
        regi = regi_index(konyv)
        for vers, rr in regi.items():
            regi_osszes.add(vers)
            ur = uj.get(vers, [])
            rs = collections.Counter(norm_strong(r["Strong-szám"]) for r in rr)
            if not ur:
                kat = "csak_regi_vers"
                sorok_ki.append([vers, kat, str(len(rr)), "0", "", "", "", ""])
                kat_db[kat] += 1; konyv_db[konyv][kat] += 1
                continue
            us = collections.Counter(norm_strong(r["strong"]) for r in ur)
            rsn = {k: v for k, v in rs.items() if k}
            usn = {k: v for k, v in us.items() if k}
            if rsn == usn:
                kat_db["azonos"] += 1; konyv_db[konyv]["azonos"] += 1
                continue
            j = jaccard(collections.Counter(rsn), collections.Counter(usn))
            kat = "strong_eltero" if j >= 0.8 else "nagy_eltero"
            if kat == "nagy_eltero" and konyv == "Zsolt":
                kovetkezo = uj.get(kovetkezo_vers(vers), [])
                if kovetkezo:
                    ks = collections.Counter(norm_strong(r["strong"]) for r in kovetkezo)
                    ksn = {k: v for k, v in ks.items() if k}
                    if jaccard(collections.Counter(rsn), collections.Counter(ksn)) >= 0.8:
                        kat = "zsoltar_eltolas"
            # szóalak szerinti Strong-párok (a konvenció-eltérések gyűjtéséhez)
            ualak = collections.defaultdict(list)
            for r in ur:
                ualak[alak(r["szoalak"])].append(norm_strong(r["strong"]))
            for r in rr:
                lista = ualak.get(alak(r["Görög szóalak"]))
                if lista:
                    parok[(norm_strong(r["Strong-szám"]), lista.pop(0))] += 1
            csak_r = " ".join("%s:%d" % (k, v) for k, v in sorted((collections.Counter(rsn) - collections.Counter(usn)).items()))
            csak_u = " ".join("%s:%d" % (k, v) for k, v in sorted((collections.Counter(usn) - collections.Counter(rsn)).items()))
            sorok_ki.append([vers, kat, str(len(rr)), str(len(ur)), "%.2f" % j,
                             ur[0]["igehely_lxx"], csak_r, csak_u])
            kat_db[kat] += 1; konyv_db[konyv][kat] += 1
    for vers, ur in uj.items():
        if vers not in regi_osszes:
            sorok_ki.append([vers, "csak_uj_vers", "0", str(len(ur)), "", ur[0]["igehely_lxx"], "", ""])
            kat_db["csak_uj_vers"] += 1
            konyv_db[vers.split()[0]]["csak_uj_vers"] += 1

    os.makedirs(os.path.dirname(ut_ki), exist_ok=True)
    with open(ut_ki, "w", encoding="utf-8", newline="\n") as f:
        f.write("# GENERÁLT: eszkozok/lxx_osszevetes.py — kézzel nem szerkesztendő.\n")
        f.write("# proveniencia: scope=konkordancia/LXX_kivonat_*.tsv (regi) vs konkordancia/LXX_OS/*.tsv (elsodleges "
                "valtozat, lxx_os_import.ELSODLEGES_SLUG) | forras=manual (osszevetes, nem lekerdezes) | ts=%s\n"
                % datetime.date.today().isoformat())
        f.write("# csak a NEM azonos versek; kategoriak: l. a szkript docstringje (F42.M5)\n")
        f.write("\t".join(HEADER) + "\n")
        for s in sorok_ki:
            f.write("\t".join(s) + "\n")
    print("kategoriak:", dict(kat_db))
    for k in sorted(konyv_db):
        print("  %s: %s" % (k, dict(konyv_db[k])))
    print("leggyakoribb (regi, uj) Strong-parok azonos szoalaknal, ha elternek:")
    for (a, b), n in parok.most_common(40):
        if a != b:
            print("  %s -> %s: %d" % (a, b, n))
    print("kimenet: %s (%d sor)" % (ut_ki, len(sorok_ki)))


if __name__ == "__main__":
    main()
