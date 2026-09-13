#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adat/grammatikai_strongok.tsv előállítása.

Az ATALAKITASI_TERV.md.md 4.1 pontja szerint a gerinc-metszet (lekerdez.py gerinc)
e fájl nélkül használhatatlan, mert a metszet túlnyomó része affixum és funkciószó.

A fájl NEM kézzel karbantartott: ez a szkript állítja elő két meglévő datasetből
(konkordancia/TAHOT_kivonat.tsv, konkordancia/Strong_szotar.tsv) plusz két
kézzel gondozott listából (KERETSZO, KIVETEL), amelyek itt, a forrásban élnek.

Futtatás a repó gyökeréből:
    python eszkozok/grammatikai_strongok_general.py
"""

import csv
import os
import sys
from collections import Counter
from datetime import datetime, timezone

TAHOT = os.path.join("konkordancia", "TAHOT_kivonat.tsv")
SZOTAR = os.path.join("konkordancia", "Strong_szotar.tsv")
KIMENET = os.path.join("adat", "grammatikai_strongok.tsv")

# A Strong_szotar.tsv "Szófaj" mezőjének azon értékei, amelyek funkciószót jelölnek.
# Ezek kizárása mechanikusan biztonságos: a szó nem hordoz motívum-tartalmat.
FUNKCIO_SZOFAJ = {
    "elöljárószó",
    "partikula",
    "mutató partikula",
    "kötőszó",
    "mutató névmás",
    "személyes névmás",
    "kérdő névmás",
    "vonatkozó névmás",
    "tagadószó",
}

# Elbeszélői keretszavak: nagy gyakoriságú, tartalmi szófajú tételek, amelyek
# szakaszhatártól függetlenül szinte minden metszetben megjelennek.
# FIGYELEM: ezek kizárása NEM automatikus (kizaras=jelzes) — a gerinc-parancs
# kiírja őket, megjelölve, és explicit döntést kér. Indok: a lista több eleme
# bizonyíthatóan lehet valódi gerinc-elem is. Két dokumentált ellenpélda:
#   - H8085 (sámá) a "sámá + chámász" kollokáció egyik tagja (terv 4.1 / F2 teszt);
#   - H1121 (bén) a "bené ha-elohim" szerkezet hordozója (Isten fiai/Nefilim motívum).
KERETSZO = {
    "H3605": "kol — 'minden', kvantor-szerű főnév",
    "H0559": "amar — 'mondani', az elbeszélés alapigéje",
    "H1961": "hajá — 'lenni', létige",
    "H6213": "aszá — 'tenni, csinálni'",
    "H0935": "bó — 'jönni, bemenni'",
    "H1980": "halak — 'menni'",
    "H5414": "natan — 'adni'",
    "H7200": "ráá — 'látni'",
    "H8085": "sámá — 'hallani' (ellenpélda: sámá + chámász kollokáció)",
    "H1696": "dabar — 'szólni' (az ige; a H1697 davar főnév kivétel, nem keretszó)",
    "H3947": "lakach — 'venni, elvenni'",
    "H3045": "jada — 'ismerni, tudni'",
    "H7725": "sub — 'visszatérni'",
    "H3318": "jaca — 'kimenni'",
    "H5927": "alá — 'felmenni'",
    "H7971": "salach — 'küldeni'",
    "H3427": "jasab — 'lakni, ülni'",
    "H0398": "akal — 'enni'",
    "H1121": "bén — 'fiú' (ellenpélda: bené ha-elohim)",
    "H0376": "is — 'férfi, ember'",
    "H0802": "issá — 'asszony, feleség'",
    "H0001": "ab — 'atya'",
    "H3117": "jóm — 'nap'",
    "H6440": "pané — 'arc, szín előtt' (gyakran elöljárós szerkezet része)",
    "H3027": "jad — 'kéz'",
    "H1004": "bajit — 'ház'",
    "H5892": "ir — 'város'",
    "H8141": "sáná — 'év'",
    "H5869": "ajin — 'szem'",
    "H0259": "echad — 'egy'",
    "H3651": "kén — 'így, úgy'",
    "H8033": "sám — 'ott'",
    "H4428": "melek — 'király'",
    "H5650": "ebed — 'szolga'",
}

# Kivételek: nagy gyakoriságú, de motívum-hordozó szavak. Azért kapnak saját sort,
# hogy egy későbbi, gyakoriság-alapú bővítés se söpörhesse be őket némán.
# Ezeket a gerinc-metszet SOHA nem szűri ki.
KIVETEL = {
    "H3068": "JHVH — az istennév maga motívum-hordozó",
    "H0430": "Elohim — a HAMART-001 metszetében is szerepelt; kizárása teológiai tartalmat törölne",
    "H8034": "sém — 'név'; nyitott motívum-jelölt tárgya ('shem — név szerzése')",
    "H1697": "davar — 'ige, beszéd, dolog' (főnév)",
    "H0776": "erec — 'föld, ország'; a teremtéstani motívumok hordozója",
    "H0127": "adamá — 'termőföld'; a HAMART-001 gerincének egyetlen tartalmi szava",
    "H7307": "rúach — 'szél, lélek'; a pneuma/pszükhé motívum héber oldala",
    "H5315": "nefes — 'lélek, élet'; ugyanott",
    "H3820": "léb — 'szív'",
    "H5971": "am — 'nép'",
    "H4191": "mút — 'meghalni'",
    "H2416": "chaj — 'élő, élet'",
}


def betolt_szotar(path):
    """Strong-szám -> (szótő, szófaj, jelentés)."""
    d = {}
    with open(path, encoding="utf-8") as f:
        r = csv.reader(f, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) >= 6 and row[0]:
                d[row[0]] = (row[1], row[3], row[5])
    return d


def tahot_gyakorisag(path):
    """Strong-szám -> ÓSZ-előfordulásszám a TAHOT-kivonatban, és a szótő/gloss."""
    freq = Counter()
    alak = {}
    with open(path, encoding="utf-8") as f:
        r = csv.reader(f, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) >= 6 and row[1].startswith("H"):
                freq[row[1]] += 1
                alak.setdefault(row[1], (row[4], row[5]))
    return freq, alak


def main():
    for p in (TAHOT, SZOTAR):
        if not os.path.exists(p):
            sys.exit("HIÁNYZÓ FORRÁS: %s (a repó gyökeréből futtasd)" % p)

    szotar = betolt_szotar(SZOTAR)
    freq, alak = tahot_gyakorisag(TAHOT)

    sorok = []
    seen = set()

    def felvesz(strong, kategoria, kizaras, indok):
        if strong in seen:
            return
        seen.add(strong)
        sz_szoto, sz_szofaj, sz_jelentes = szotar.get(strong, ("", "", ""))
        t_szoto, t_gloss = alak.get(strong, ("", ""))
        sorok.append({
            "strong": strong,
            "szoto": sz_szoto or t_szoto,
            "szofaj": sz_szofaj,
            "jelentes": sz_jelentes or t_gloss,
            "kategoria": kategoria,
            "kizaras": kizaras,
            "osz_elofordulas": str(freq.get(strong, 0)),
            "indok": indok,
        })

    # 4. Kivételek elsőként, hogy a későbbi szabályok ne írhassák felül őket.
    for strong, indok in sorted(KIVETEL.items()):
        felvesz(strong, "kivetel", "soha", indok)

    # 1. Affixumok — a STEPBible H9xxx tartománya: prefixumok, szuffixumok,
    #    névmási jelölők. Nincs köztük tartalmi szó, ezért mind 'mindig'.
    for strong in sorted(s for s in freq if s.startswith("H9")):
        felvesz(strong, "affixum", "mindig",
                "STEPBible H9xxx grammatikai jelölő (prefixum/szuffixum/névmási elem)")

    # 2. Funkciószavak — a Strong_szotar.tsv szófaji mezője alapján, de csak
    #    azok, amelyek ténylegesen elő is fordulnak a TAHOT-kivonatban.
    for strong in sorted(freq):
        if strong.startswith("H9"):
            continue
        szofaj = szotar.get(strong, ("", "", ""))[1]
        if szofaj in FUNKCIO_SZOFAJ:
            felvesz(strong, "funkcioszo", "mindig",
                    "Strong_szotar.tsv szófaj: %s" % szofaj)

    # 3. Keretszavak — kézzel gondozott lista, gyakoriság alapján válogatva,
    #    tételesen ellenőrizve. NEM automatikus kizárás.
    for strong, indok in sorted(KERETSZO.items()):
        felvesz(strong, "keretszo", "jelzes", indok)

    sorok.sort(key=lambda s: s["strong"])

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    mezok = ["strong", "szoto", "szofaj", "jelentes",
             "kategoria", "kizaras", "osz_elofordulas", "indok"]

    with open(KIMENET, "w", encoding="utf-8", newline="") as f:
        f.write("# GENERÁLT: eszkozok/grammatikai_strongok_general.py | "
                "forras=TAHOT_kivonat.tsv+Strong_szotar.tsv | ts=%s\n" % ts)
        f.write("# Kézzel nem szerkesztendő. A KERETSZO/KIVETEL listák a szkript forrásában élnek.\n")
        w = csv.DictWriter(f, fieldnames=mezok, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for s in sorok:
            w.writerow(s)

    osszes = Counter(s["kategoria"] for s in sorok)
    print("Kiirva: %s (%d sor)" % (KIMENET, len(sorok)))
    for k in ("affixum", "funkcioszo", "keretszo", "kivetel"):
        print("  %-11s %4d" % (k, osszes[k]))


if __name__ == "__main__":
    main()
