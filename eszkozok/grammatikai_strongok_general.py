#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adat/grammatikai_strongok.tsv előállítása.

Az ATALAKITASI_TERV.md.md 4.1 pontja szerint a gerinc-metszet (lekerdez.py gerinc)
e fájl nélkül használhatatlan, mert a metszet túlnyomó része affixum és funkciószó.

SZERKEZET (felhasználói döntés, 2026.09.13):

  1. HÉBER, GÉPI ALAP — a TAHOT H9xxx tartománya. Ezt a szkript automatikusan
     olvassa ki, provenienciával; kézi karbantartást nem igényel.
  2. HÉBER, KÉZI KIEGÉSZÍTÉS — hét funkciószó, amely nincs a H9xxx-ben, de
     ugyanolyan zajt ad. Tételes indoklással, l. a HEBER_KEZI feletti kritériumot.
  3. GÖRÖG — a TAGNT-ből. FIGYELEM: a héber H9xxx-nek NINCS görög megfelelője.
     A TAGNT G9xxx tartománya nem grammatikai, hanem 7 ritka lexikai szó
     (συναλλάσσω, ὑπόλειμμα, ταπεινοφροσύνη stb.), egyenként 1 előfordulással —
     kiegészítő Strong-számok, nem nyelvtani jelölők. A görög oldal ezért
     tételes, indokolt lista, amely a H9xxx tartalmát tükrözi (névelő, kötőszó,
     elöljárók, névmások, tagadószók).

TILTÓLISTA — tartalmi szavak, amelyek SOHA nem kerülhetnek a táblába, akkor sem,
ha egy későbbi bővítés gyakoriság alapján beemelné őket. A tiltás gépi, nem
udvariassági kérés: a szkript hibával áll le, ha egy lista megsérti.

Kimeneti oszlopok: strong | rovid_jelentes | kategoria | kizaras_oka

Futtatás a repó gyökeréből:
    python eszkozok/grammatikai_strongok_general.py
"""

import os
import sys
from collections import Counter
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def tsv_sor(mezok):
    """Egy TSV-sor a csv modul nelkul — l. CLAUDE.md, „TSV-olvasas".

    A modul iroja a " jelet tartalmazo mezot korulidezi es belul duplazza,
    tehat a korutja nem bajthu. Sorveg LF, mint a kivaltott hivas
    lineterminator erteke.
    """
    ki = []
    for m in mezok:
        m = "" if m is None else str(m)
        if "\t" in m or "\n" in m or "\r" in m:
            raise ValueError("elvalaszto a mezoben: %r" % (m,))
        ki.append(m)
    return "\t".join(ki) + "\n"


TAHOT = os.path.join("konkordancia", "TAHOT_kivonat.tsv")
TAGNT = os.path.join("konkordancia", "TAGNT_kivonat.tsv")
KIMENET = os.path.join("adat", "grammatikai_strongok.tsv")

# ---------------------------------------------------------------------------
# TILTÓLISTA — tartalmi szavak, amelyek nem lehetnek kizárva a gerinc-metszetből.
# ---------------------------------------------------------------------------
TILTOLISTA = {
    "H3068": "JHVH — az istennév maga motívum-hordozó",
    "H0559": "amar, 'mondani' — elbeszélői keretszó, DE tartalmi ige; kizárása leletet törölne",
    "G2316": "theosz, 'Isten' — a H3068/H0430 görög párja, ugyanazon okból",
    "G3004": "legó, 'szólni' — a H0559 görög párja, ugyanazon okból",
    "H1961": "hájá, 'lenni' — gyakori (3 562), DE tartalmi ige; a teremtés-motívumoknál gerinc-elem lehet",
    "H6213": "aszá, 'tenni, csinálni' — gyakori (2 628), DE tartalmi ige; ugyanazon okból",
}

# ---------------------------------------------------------------------------
# HATARESET — dokumentált, de NEM aktív. Sem a táblába, sem a tiltólistára nem
# kerül: a kérdés nyitva marad, hogy egy későbbi kör eldönthesse.
# ---------------------------------------------------------------------------
HATARESET = {
    "H3605": ("kol, 'minden' — gyakori (5 412) és kvantor-szerű, DE tartalmi jegyet is "
              "hordozhat: a teljesség / kivétel nélküliség motívumszinten releváns lehet. "
              "Ha valaha felvesszük, külön kategóriával és külön indoklással."),
}

# ---------------------------------------------------------------------------
# 2. HÉBER KÉZI KIEGÉSZÍTÉS — nincs a H9xxx-ben, de ugyanaz a zaj.
#
# A FELVÉTEL KRITÉRIUMA (nem a H9xxx tagság!):
#   Egy Strong-szám akkor grammatikai, ha a szó önmagában nem hordoz tartalmi
#   jegyet — függetlenül attól, hogy prefixként vagy szabadon áll.
#   A H9xxx tartomány kényelmes kiindulás, de nem definíció: ortográfiai határ,
#   nem szemantikai. Egy elöljáró nem attól lesz tartalmas, hogy külön szóként
#   írják. Ezért tartozik ide az alábbi hét tétel is.
#
# Ellenőrizhető jel: mind a hét szófaja a Strong_szotar.tsv-ben elöljárószó,
# kötőszó vagy névmás — szemben a szándékosan kihagyottakkal (H3605 főnév,
# H1961 és H6213 ige), amelyek a TILTOLISTA-ra, illetve a HATARESET-be kerültek.
# ---------------------------------------------------------------------------
HEBER_KEZI = [
    ("H0853", "[tárgy jelölője]", "targyrag",
     "Tárgyrag (אֵת). Nem hordoz jelentést, csak a határozott tárgyat jelöli; "
     "gyakorlatilag minden tranzitív mondatban jelen van, ezért minden metszetbe bekerül."),
    ("H0834", "amely, aki", "vonatkozo_nevmas",
     "Vonatkozó névmás (אֲשֶׁר). Tisztán szerkezeti elem: alárendelt tagmondatot vezet be, "
     "a tagmondat tartalmáról semmit nem mond."),
    ("H3808", "nem", "tagadoszo",
     "Tagadószó (לֹא). A tagadás formális jelölője; a tagadott fogalom hordozza a tartalmat, "
     "nem maga a partikula."),
    ("H0413", "-hoz, felé", "eloljaro",
     "Szabadon álló elöljáró (אֶל). Görög párja a G1519 (εἰς), amely már a listán van. "
     "A H9xxx csak a prefixált elöljárókat fedi — ez ortográfiai határ, nem szemantikai."),
    ("H5921", "-on, fölött, ellen", "eloljaro",
     "Szabadon álló elöljáró (עַל). Görög párja a G1909 (ἐπί), amely már a listán van."),
    ("H3588", "mert, hogy, amikor", "kotoszo",
     "Alárendelő kötőszó (כִּי). Görög párja a G3754 (ὅτι), amely már a listán van."),
    ("H5704", "-ig", "eloljaro",
     "Szabadon álló elöljáró (עַד). Időbeli vagy térbeli határt jelöl, tartalmi jegy nélkül."),
    ("H4480", "-ból, -ből, -tól", "eloljaro",
     "Szabadon álló elöljáró (מִן־). A LEGÁRULKODÓBB eset: a PREFIXÁLT változata (H9006, "
     "6 383 előfordulás) már a gépi H9xxx alapban van, a szabadon álló (1 189) nem volt — "
     "ugyanaz a szó, ugyanaz a jelentés, pusztán az írásmód választotta ketté."),
    ("H1931", "ő, az", "nevmas",
     "Személyes/mutató névmás (הוּא). Görög párja a G0846 (αὐτός), amely már a listán van."),
    ("H2088", "ez", "nevmas",
     "Mutató névmás (זֶה). Görög párja a G3778 (οὗτος), amely már a listán van."),
]

# ---------------------------------------------------------------------------
# 3. GÖRÖG — tételes lista. A 'tukor' mező azt mondja, a H9xxx melyik elemét pótolja.
#    (strong, rövid jelentés, kategória, tükör/indok)
# ---------------------------------------------------------------------------
GOROG_KEZI = [
    ("G3588", "a, az",          "nevelo",     "Határozott névelő (ὁ). A héber oldalon ezt a H9009 (ה) fedi le, ami a gépi H9xxx alapban van."),
    ("G2532", "és",             "kotoszo",    "Mellérendelő kötőszó (καί). Héber párja a H9002 (ו), a gépi alapban."),
    ("G1161", "pedig, de",      "partikula",  "Mondatkapcsoló partikula (δέ). Tisztán diskurzus-jelölő, nincs fogalmi tartalma."),
    ("G0235", "hanem",          "kotoszo",    "Ellentétes kötőszó (ἀλλά)."),
    ("G1063", "mert, ugyanis",  "partikula",  "Magyarázó partikula (γάρ). Az érvelés szerkezetét jelöli, nem a tartalmát."),
    ("G3767", "tehát",          "partikula",  "Következtető partikula (οὖν)."),
    ("G3754", "hogy, mert",     "kotoszo",    "Alárendelő kötőszó (ὅτι). Héber párja a H3588 (כִּי)."),
    ("G1437", "ha",             "kotoszo",    "Feltételes kötőszó (ἐάν)."),
    ("G1487", "ha",             "kotoszo",    "Feltételes kötőszó (εἰ)."),
    ("G2228", "vagy",           "kotoszo",    "Választó kötőszó (ἤ)."),
    ("G1722", "-ban, -ben",     "eloljaro",   "Elöljáró (ἐν). Héber párja a H9003 (בְּ), a gépi alapban."),
    ("G1519", "-ba, felé",      "eloljaro",   "Elöljáró (εἰς). Héber párja részben a H9005 (לְ)."),
    ("G1537", "-ból, -ből",     "eloljaro",   "Elöljáró (ἐκ). Héber párja a H9006 (מִן)."),
    ("G0575", "-tól, -től",     "eloljaro",   "Elöljáró (ἀπό). Héber párja szintén a H9006."),
    ("G1909", "-on, -en, -ra",  "eloljaro",   "Elöljáró (ἐπί)."),
    ("G4314", "-hoz, felé",     "eloljaro",   "Elöljáró (πρός)."),
    ("G1223", "által, keresztül","eloljaro",  "Elöljáró (διά)."),
    ("G2596", "szerint, ellen", "eloljaro",   "Elöljáró (κατά)."),
    ("G3326", "-val, után",     "eloljaro",   "Elöljáró (μετά)."),
    ("G4012", "-ról, felől",    "eloljaro",   "Elöljáró (περί)."),
    ("G5259", "által",          "eloljaro",   "Elöljáró (ὑπό)."),
    ("G4862", "-val együtt",    "eloljaro",   "Elöljáró (σύν)."),
    ("G0846", "ő, az, maga",    "nevmas",     "Személyes/visszaható névmás (αὐτός). Héber párja a H9023 stb. névmási szuffixum-sor, a gépi alapban."),
    ("G1473", "én",             "nevmas",     "Személyes névmás (ἐγώ, alanyeset)."),
    ("G3165", "engem, én, mi",  "nevmas",     "Személyes névmás (ἐγώ, függő esetek). A TAGNT a TÖBBES SZÁMÚ alakokat is ide sorolja (ἡμῶν), ezért a G2249 (ἡμεῖς) nem kap sort — a kivonatban 0 előfordulású."),
    ("G4771", "te, ti",         "nevmas",     "Személyes névmás (σύ). A TAGNT a többes számú alakokat is ide sorolja, ezért a G5210 (ὑμεῖς) nem kap sort — a kivonatban 0 előfordulású."),
    ("G3778", "ez",             "nevmas",     "Mutató névmás (οὗτος)."),
    ("G1565", "az",             "nevmas",     "Mutató névmás (ἐκεῖνος)."),
    ("G3739", "aki, amely",     "vonatkozo_nevmas", "Vonatkozó névmás (ὅς). Héber párja a H0834 (אֲשֶׁר), kézi kiegészítésként."),
    ("G3756", "nem",            "tagadoszo",  "Tagadószó (οὐ). Héber párja a H3808 (לֹא), kézi kiegészítésként."),
    ("G3361", "ne, nem",        "tagadoszo",  "Tagadószó (μή)."),
]


def olvas_kivonat(path, prefix):
    """Strong-szám -> (előfordulásszám, rövid jelentés) a kivonat-TSV-ből."""
    freq = Counter()
    gloss = {}
    with open(path, encoding="utf-8") as f:
        sorok = [ln.rstrip("\n").rstrip("\r") for ln in f if ln.strip()]
    for s in sorok[1:]:
        row = s.split("\t")
        if len(row) >= 6 and row[1].startswith(prefix):
            freq[row[1]] += 1
            gloss.setdefault(row[1], row[5])
    return freq, gloss


def main():
    for p in (TAHOT, TAGNT):
        if not os.path.exists(p):
            sys.exit("HIÁNYZÓ FORRÁS: %s (a repó gyökeréből futtasd)" % p)

    h_freq, h_gloss = olvas_kivonat(TAHOT, "H")
    g_freq, g_gloss = olvas_kivonat(TAGNT, "G")

    sorok = []
    seen = set()

    def felvesz(strong, jelentes, kategoria, ok):
        if strong in TILTOLISTA:
            sys.exit("TILTÓLISTA MEGSÉRTVE: %s — %s\n"
                     "Ez a szó tartalmi, nem szűrhető ki a gerinc-metszetből."
                     % (strong, TILTOLISTA[strong]))
        if strong in seen:
            return
        seen.add(strong)
        sorok.append({
            "strong": strong,
            "rovid_jelentes": jelentes,
            "kategoria": kategoria,
            "kizaras_oka": ok,
        })

    # --- 1. Héber gépi alap: a TAHOT H9xxx tartománya -----------------------
    h9 = sorted(s for s in h_freq if s.startswith("H9"))
    h9_db = sum(h_freq[s] for s in h9)
    for strong in h9:
        felvesz(strong, h_gloss.get(strong, ""), "affixum",
                "STEPBible H9xxx grammatikai jelölő (prefixum, szuffixum vagy névmási elem); "
                "gépi alap, nem kézzel karbantartott")

    # --- 2. Héber kézi kiegészítés -----------------------------------------
    for strong, jelentes, kat, ok in HEBER_KEZI:
        felvesz(strong, jelentes, kat, ok)

    # --- 3. Görög tételes lista --------------------------------------------
    hianyzo_gorog = []
    for strong, jelentes, kat, ok in GOROG_KEZI:
        if strong not in g_freq:
            hianyzo_gorog.append(strong)
        felvesz(strong, jelentes, kat, ok)

    sorok.sort(key=lambda s: s["strong"])

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    prov_h = ("scope=OT-full | forras=TAHOT_kivonat.tsv | tartomany=H9xxx | "
              "n=%d | elofordulas=%d | ts=%s" % (len(h9), h9_db, ts))
    g_db = sum(g_freq.get(s, 0) for s, _, _, _ in GOROG_KEZI)
    prov_g = ("scope=NT-full | forras=TAGNT_kivonat.tsv | modszer=teteles-lista | "
              "n=%d | elofordulas=%d | ts=%s" % (len(GOROG_KEZI), g_db, ts))

    mezok = ["strong", "rovid_jelentes", "kategoria", "kizaras_oka"]
    with open(KIMENET, "w", encoding="utf-8", newline="") as f:
        f.write("# GENERÁLT: eszkozok/grammatikai_strongok_general.py — kézzel nem szerkesztendő.\n")
        f.write("# A kézi listák (HEBER_KEZI, GOROG_KEZI) és a TILTOLISTA a szkript forrásában élnek.\n")
        f.write("# proveniencia-heber: %s\n" % prov_h)
        f.write("# proveniencia-gorog: %s\n" % prov_g)
        f.write("# A TAGNT G9xxx tartomanya NEM grammatikai (7 ritka lexikai szo), ezert a gorog\n")
        f.write("# oldalnak nincs gepi alapja — teteles lista, soronkent indokolva.\n")
        f.write("# KRITERIUM: egy Strong-szam akkor grammatikai, ha a szo onmagaban nem hordoz\n")
        f.write("# tartalmi jegyet — fuggetlenul attol, hogy prefixkent vagy szabadon all.\n")
        f.write("# A H9xxx tartomany kenyelmes kiindulas, de nem definicio.\n")
        f.write("# SCOPE: ez a 'gerinc' parancs stopword-listaja, NEM globalis kizaras. Ha egy\n")
        f.write("# eloljaro motivumszinten szamit (pl. al-pene), azt a 'kollokacio' parancs\n")
        f.write("# talalja meg, nem a metszet. A ketto nem utkozik.\n")
        f.write(tsv_sor(mezok))
        for s in sorok:
            f.write(tsv_sor([s[k] for k in mezok]))

    kat = Counter(s["kategoria"] for s in sorok)
    print("Kiirva: %s (%d sor)" % (KIMENET, len(sorok)))
    print("  heber H9xxx (gepi):  %3d kod, %6d elofordulas" % (len(h9), h9_db))
    print("  heber kezi:          %3d kod" % len(HEBER_KEZI))
    print("  gorog teteles:       %3d kod, %6d elofordulas" % (len(GOROG_KEZI), g_db))
    print("  kategoriak: %s" % ", ".join("%s=%d" % (k, v) for k, v in sorted(kat.items())))
    print("  tiltolista ervenyben: %s" % ", ".join(sorted(TILTOLISTA)))
    print("  hatareset (dokumentalt, nem aktiv): %s" % ", ".join(sorted(HATARESET)))
    if hianyzo_gorog:
        print("  FIGYELEM — nem fordul elo a TAGNT-ben: %s" % ", ".join(hianyzo_gorog))


if __name__ == "__main__":
    main()
