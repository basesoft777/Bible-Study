#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t2_1_teremt002_minosites.py — TEREMT002_KUTATAS_BRIEF.md T2.1: minősítési
JAVASLAT a TEREMT-002 66 jelöltjére (a 2026.09.25-i gate: A változat, a
negatív kritérium H8414 + H0922 egy versben).

Kimenet (csak --ir-rel): `naplok/T2_TEREMT002_minosites.tsv` (jelöltenként)
és `naplok/T2_TEREMT002_kapcsolatok_javaslat.tsv` (a kapcsolatok.tsv
oszlopaival). Az `adat/`-ot NEM írja — a döntés a felhasználóé (⛔).

Indoklás-rend (a felhasználó T2.1-utasítása szerint): egyedi a 3 pár-versnek,
az Ézs 45:18-nak, az Ézs 24:10-nek és a Jer 4:23 kereszthivatkozás-körének;
a többi pár nélküli jelölt kategória-indoklást kap; az 5 adathiba-gyanús
Károli-KH-jelölt rögzített indoklást.

A 2026.09.25-i döntés a javaslatot két ponton módosította (DONTES_SZOVEG,
KAPCSOLATOK ötödik sora): az Ézs 24:10 indoklása a döntés szövege, és az
Ézs 24:10 → Ézs 34:11 kapcsolat felvéve. A kimenet ezért már a DÖNTÖTT
állapot; a T2.2 ebből írja az `adat/`-ot.
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
ID = "TEREMT-002"
NEG = "negatív kritérium: nincs H8414+H0922 pár"

PAR = {
    "1Móz 1:2": dict(
        indoklas="A pár első előfordulása, a föld (há-árec) állítmányaként: a teremtés "
                 "előtti, rendezetlen állapot. Kollokáció-találat; a TEREMT-001-gyel "
                 "közös vers, de más mondatrészen és más funkcióval (gate 3. kérdés).",
        karoli="kietlen és puszta", megb="magas", pardes="Peshat",
        funkcio="prototípus: a föld teremtés előtti, rendezetlen állapota, amelyre a "
                "Jer 4:23 és az Ézs 34:11 ítélet-szövege visszautal",
        kapcsolodas="\"A föld pedig kietlen és puszta vala\" — a תֹהוּ וָבֹהוּ pár a föld "
                    "teremtés előtti állapotának megnevezése"),
    "Jer 4:23": dict(
        indoklas="A pár második előfordulása: Júda ítélete a föld visszatérése az 1Móz "
                 "1:2 állapotába; a 4:23–26 négy „nézek”-sora a teremtési rend elemeit "
                 "(világosság, hegyek, ember, madarak, termőföld) sorra visszavonja. "
                 "Károli szó szerint az 1Móz 1:2 fordítását ismétli. TSK 1Móz 1:2 ↔ Jer 4:23: 84 / 21 szavazat.",
        karoli="kietlen és puszta", megb="magas", pardes="Remez",
        funkcio="ítélet-alkalmazás Júdára: a föld visszarendeződése a teremtés előtti "
                "állapotba (4:23–26)",
        kapcsolodas="\"Nézek a földre, de ímé kietlen és puszta\" — az 1Móz 1:2 párja "
                    "Júda ítéletének képeként"),
    "Ézs 34:11": dict(
        indoklas="A pár harmadik előfordulása: Edom ítélete; a tohu a mérőkötél (kav), a "
                 "bohu a függőón kövei (avné) — az építő mérés rombolásra fordítva. "
                 "Károli itt másként fordít (pusztaság … semmiség), a héber pár azonos.",
        karoli="pusztaság … semmiségnek", megb="magas", pardes="Remez",
        funkcio="ítélet-alkalmazás Edomra: a tohu/bohu mint a rombolás mérőeszköze",
        kapcsolodas="\"fölvonják rá a pusztaság mérőkötelét és a semmiségnek köveit\" — "
                    "a תֹהוּ וָבֹהוּ pár Edom ítéletében, mérőkötél és függőón képében"),
}

# Egyedi indoklású, elutasított jelöltek.
EGYEDI = {
    "Ézs 45:18": "Önálló tohu, bohu nélkül — a negatív kritérium kizárja. Tartalmilag a "
                 "legerősebb nem-pár vers: az Úr „nem tohu-nak teremtette” a földet, az 1Móz "
                 "1:2 állapotának kifejezett ellenpontja (Károli: „nem hiába”). Kapcsolatként "
                 "felvéve (1Móz 1:2 → Ézs 45:18, Kontraszt).",
    # A 2026.09.25-i döntés szövege, szó szerint (a javaslat indoklása hibás volt:
    # a versben van pusztulás-szó, H7665 nisberá — „rommá lőn”).
    "Ézs 24:10": None,
    "Mt 24:29": "Kozmikus elsötétülés (nap, hold, csillagok) — a Jer 4:23 „nincsen "
                "világossága” képével rokon, de lexikai pár nélkül: a fölérendelt fogalom "
                "felé húz. TSK 35.",
    "Mk 13:24": "Az Mt 24:29 szinoptikus párhuzama: elsötétülés, tohu/bohu nélkül. TSK 29.",
    "Mk 13:25": "Csillaghullás, az egek megrendülése — pár nélkül. TSK 29.",
    "Ézs 13:10": "Babilon-ítélet égi elsötétüléssel — a pusztulás-kép, pár nélkül. TSK 26.",
    "Jóel 3:15": "Nap és hold elsötétülése — pár nélkül. TSK 26.",
    "Jóel 3:16": "Az egek és a föld megrendülése — pár nélkül; a vers ráadásul oltalom-"
                 "ígérettel zárul. TSK 26.",
    "Luk 21:25": "Jelek a napban, holdban, csillagokban — pár nélkül. TSK 21.",
    "Luk 21:26": "Az egek erősségeinek megrendülése — pár nélkül. TSK 21.",
    "Ez 32:7": "A fáraó-sirató égi elsötétülése — pár nélkül. TSK 20.",
    "Ez 32:8": "„Sötétséget bocsátok földedre” — a Jer 4:23 fény-hiányához legközelebb "
               "álló kép, de pár nélkül. TSK 20.",
    "Ámós 8:9": "Délben lenyugvó nap — pár nélkül. TSK 18.",
    "Jóel 2:10": "Föld- és ég-rengés, elsötétülés — pár nélkül. TSK 18.",
    "Jóel 2:30": "Jelek az égen és a földön (vér, tűz, füst) — pár nélkül, elsötétülés "
                 "sincs benne. TSK 17.",
    "Jóel 2:31": "A nap sötétséggé, a hold vérré válik — pár nélkül. TSK 17.",
    "ApCsel 2:19": "A Jóel 2:30 idézete — pár nélkül. TSK 17.",
    "ApCsel 2:20": "A Jóel 2:31 idézete — pár nélkül; a LXX-híd sem köti a tohu-hoz "
                   "(a Jer 4:23 LXX-e οὐθέν). TSK 17.",
    "Ézs 5:30": "„A földre néz, de ímé sűrű sötétség” — a Jer 4:23 szerkezetének "
                "legközelebbi párja (néz → föld → sötétség), de pár nélkül. TSK 16.",
    "Mt 24:35": "„Az ég és a föld elmúlnak” — elmúlás, nem visszarendeződés; pár nélkül. TSK 15.",
    "Ézs 24:19": "A föld összetörése az Ézs 24 keretében (l. Ézs 24:10) — pár nélkül. TSK 12.",
    "Ézs 24:23": "A hold és a nap megszégyenülése a Sion-királyság előtt — pár nélkül. TSK 12.",
    "Jel 20:11": "A föld és az ég eltűnése a trón elől — megszűnés, nem a teremtés előtti "
                 "állapot; pár nélkül. TSK 12.",
    "Jer 9:10": "A Jer 4:25 visszhangja („az ég madaraitól fogva a barmokig minden "
                "elköltözik”), tehát a Jer 4:23–26 egység motívum-rokona — de tohu/bohu "
                "nélkül. TSK 8.",
    "Jer 9:15": "Károli-KH a Jer 4:23-hoz: üröm és mérges víz — tartalmi kapcsolat "
                "nem látszik; pár nélkül. (Az igazítást nem vizsgáltam.)",
    "Zsolt 80:6-7": "Károli-KH a Jer 4:23-hoz: könnyek kenyere, szomszédok csúfja — "
                    "tartalmi kapcsolat nem látszik; pár nélkül. (Az igazítást nem vizsgáltam.)",
}

ADATHIBA = {"Ézs 66:12", "Ez 34:12-16", "Ján 10:11", "1Móz 33:13", "4Móz 11:12"}
ADATHIBA_INDOK = "adathiba: az Isa.34.11 lista az Isa.40.11 másolata"

# Önálló tohu-versek Károli-szava (tartalom-alapú azonosítás).
TOHU_KAROLI = {
    "1Sám 12:21": ("hiábavalóságok", "magas"),
    "5Móz 32:10": ("zordon, sivatag vadonban", "közepes"),
    "Jób 6:18": ("sivatagba", "magas"),
    "Jób 12:24": ("pusztában", "magas"),
    "Jób 26:7": ("üresség", "magas"),
    "Zsolt 107:40": ("kietlenben", "magas"),
    "Ézs 24:10": ("álnokság", "magas"),
    "Ézs 29:21": ("csalárdul", "magas"),
    "Ézs 40:17": ("ürességnél", "magas"),
    "Ézs 40:23": ("hiábavalókká", "magas"),
    "Ézs 41:29": ("hiábavalóság", "magas"),
    "Ézs 44:9": ("hiábavalók", "magas"),
    "Ézs 45:18": ("hiába", "magas"),
    "Ézs 45:19": ("hiába", "magas"),
    "Ézs 49:4": ("semmire", "magas"),
    "Ézs 59:4": ("haszontalanban", "magas"),
}

KAPCSOLATOK = [
    ["1Móz 1:2", "Jer 4:23", ID, "Kontraszt",
     "ugyanaz az állapot, fordított irány: a teremtés kiinduló rendezetlensége Júda "
     "ítéleteként visszatér (Jer 4:23–26 a rend elemeit sorra visszavonja); TSK 84",
     "magas", "Remez"],
    ["1Móz 1:2", "Ézs 34:11", ID, "Kontraszt",
     "a pár a rombolás mérőeszközeként: a rendező mérés Edom fölött fordítva "
     "(mérőkötél és függőón); a pár kizárólagossága a kollokációval igazolt",
     "magas", "Remez"],
    ["Jer 4:23", "Ézs 34:11", ID, "Párhuzam",
     "két nép-ítélet (Júda, Edom) ugyanazzal a párral; a TSK közvetlenül nem köti össze",
     "közepes", "Remez"],
    ["1Móz 1:2", "Ézs 45:18", ID, "Kontraszt",
     "„nem tohu-nak teremtette, lakásul alkotta” — az 1Móz 1:2 állapota nem a cél; a "
     "végpont nem előfordulás (precedens: KIRALY-001 2Móz 19:6 → 1Pét 2:9)",
     "közepes", "Remez"],
    # ötödik: a 2026.09.25-i döntés felvette
    ["Ézs 24:10", "Ézs 34:11", ID, "Párhuzam",
     "ítélet-kontextusú önálló tohu (qirjat-tohu, „rommá lőn” — H7665) az Ézs 24 "
     "föld-kiüresítő keretében (24:1, 24:3: H1238 bákak), Edom tohu/bohu-ítéletével "
     "párhuzamban; a végpont nem előfordulás",
     "alacsony", "Remez"],
]

DONTES_SZOVEG = {
    "Ézs 24:10": "negatív kritérium: nincs H8414+H0922 pár; ítélet-kontextusú önálló "
                 "tohu (rommá lőn; Ézs 24:1,3 bákak) — kapcsolatként felvéve",
}


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        sorok = [ln.rstrip("\n").rstrip("\r") for ln in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith("#")]
    fej = sorok[0].split("\t")
    return [dict(zip(fej, s.split("\t"))) for s in sorok[1:]]


def main():
    ap = argparse.ArgumentParser(description="T2.1 — TEREMT-002 minősítési javaslat")
    ap.add_argument("--ir", action="store_true")
    a = ap.parse_args()

    jel = [r for r in read_tsv(ROOT / "adat" / "jeloltek.tsv") if r["id"] == ID]
    assert len(jel) == 66, len(jel)
    ki = []
    kat = {}
    for r in jel:
        ih = r["igehely"]
        tohu = r["forras_kereses"].startswith("scan H8414")
        sor = dict(id=ID, igehely=ih, javaslat="elutasítva", kategoria="", indoklas="",
                   karoli_szo="", azonositas_modja="", megbizhatosag="",
                   gerinc_elem="", strong="", fo_elofordulas="", pardes_szint="",
                   funkcio="")
        if ih in PAR:
            p = PAR[ih]
            sor.update(javaslat="beépítve", kategoria="pár", indoklas=p["indoklas"],
                       karoli_szo=p["karoli"], azonositas_modja="tartalom-alapú",
                       megbizhatosag=p["megb"], gerinc_elem="tohu+bohu",
                       strong="H8414+H0922", fo_elofordulas=ih,
                       pardes_szint=p["pardes"], funkcio=p["funkcio"])
        elif ih in ADATHIBA:
            sor.update(kategoria="adathiba", indoklas=ADATHIBA_INDOK)
        elif ih in EGYEDI:
            sor.update(kategoria="egyedi", indoklas=DONTES_SZOVEG.get(ih)
                       or NEG + ". " + EGYEDI[ih])
        elif tohu:
            sor.update(kategoria="önálló tohu",
                       indoklas=NEG + " — önálló tohu (a „puszta vidék” vagy a "
                                      "„semmiség/hiábavalóság” jelentésben).")
        else:
            sor.update(kategoria="kereszthivatkozás",
                       indoklas=NEG + " — kereszthivatkozás-célpont, a versben sem "
                                      "tohu, sem bohu.")
        if tohu and ih not in PAR:
            szo, m = TOHU_KAROLI[ih]
            sor.update(karoli_szo=szo, azonositas_modja="tartalom-alapú", megbizhatosag=m)
        kat[sor["kategoria"]] = kat.get(sor["kategoria"], 0) + 1
        ki.append(sor)

    assert set(EGYEDI) | ADATHIBA | set(PAR) <= {r["igehely"] for r in jel}
    print("javaslat:", {j: sum(1 for s in ki if s["javaslat"] == j)
                         for j in ("beépítve", "elutasítva")})
    print("kategória:", kat)

    if a.ir:
        mezok = list(ki[0].keys())
        szov = ["# T2.1 minősítés, a 2026.09.25-i döntés szerint (TEREMT002_KUTATAS_BRIEF.md). "
                "A T2.2 ebből ír. gerinc_elem/strong/fo_elofordulas/pardes_szint/funkcio csak "
                "a beépítendő sorokon.", "\t".join(mezok)]
        for s in ki:
            for v in s.values():
                assert "\t" not in v and "\n" not in v
            szov.append("\t".join(s[m] for m in mezok))
        (ROOT / "naplok" / "T2_TEREMT002_minosites.tsv").write_bytes(
            ("\n".join(szov) + "\n").encode("utf-8"))
        kfej = ["forras_igehely", "cel_igehely", "id", "tipus", "funkcio",
                "bizonyossag", "pardes_szint"]
        kszov = ["# T2.1 kapcsolatok, a 2026.09.25-i döntés szerint (5), a kapcsolatok.tsv alakjában.",
                 "\t".join(kfej)] + ["\t".join(k) for k in KAPCSOLATOK]
        (ROOT / "naplok" / "T2_TEREMT002_kapcsolatok_javaslat.tsv").write_bytes(
            ("\n".join(kszov) + "\n").encode("utf-8"))
        print("írva: naplok/T2_TEREMT002_minosites.tsv, "
              "naplok/T2_TEREMT002_kapcsolatok_javaslat.tsv")


if __name__ == "__main__":
    main()
