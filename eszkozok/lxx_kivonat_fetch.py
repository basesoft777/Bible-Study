#!/usr/bin/env python3
"""Ujrafelhasznalhato LXX-kivonat letoltő/parszoló szkript a studybible.info/LXX_WH forrasrol.

Hasznalat:
  python eszkozok/lxx_kivonat_fetch.py --konyv Psalms --fejezetek 16,110 --kimenet out.tsv
  python eszkozok/lxx_kivonat_fetch.py --konyv Genesis --fejezet-tol 1 --fejezet-ig 50 --kimenet out.tsv

Az URL-minta valtozatlan a `konkordancia/LXX_kivonat_Genezis_README.md`-ben
dokumentalthoz kepest: https://studybible.info/LXX_WH/<Konyv>%20<fejezetszam>
(fejezetenkent kulon oldal). A kimenet ugyanaz a 4 oszlopos sema, mint a
`konkordancia/LXX_kivonat_Genezis.tsv`:
  Igehely | Strong-szam | Gorog szoalak | Morfologiai kod

Csak Strong-szammal ellatott szavak kerulnek a kimenetbe (a forrasoldal
nehany szonal - pl. tulajdonnevek - nem ad Strong-szamot; ezek kimaradnak,
mivel a kimenet celja kifejezetten a Strong-taggelt konkordancia-kivonat).

Opcionalis --versifikacios-terkep + --karoli-konyv-prefix parameterekkel a
szkript a `konkordancia/LXX_versificacios_terkep.tsv` `Gorog_LXX_vers`
oszlopat hasznalja az Igehely-cimke meghatarozasahoz a nyers oldal-helyi
vers-sorszam helyett. Ez azoknal a konyveknel szukseges (pl. Zsoltarok),
ahol a LXX belso vers-/fejezetszamozasa el van tolva a maszoretai/Karoli
szamozastol (pl. zsoltar-feliratok kulon LXX-versszamot kapnak, amit a
Karoli nem szamoz kulon). A forrasoldal minden ilyen esetben `[fejezet:vers]`
alaku zarojeles jelolessel latja el az erintett szo elejet a nyers HTML-ben
(pl. `[109:4]`) - ez pontosan megegyezik a `Gorog_LXX_vers` oszloppal, es a
szkript ezt hasznalja a terkepben valo kereseshez, majd a talalt sor
`Karoli_igehely` erteket irja a kimenetbe. Zarojel hianyaban (nincs
elteres az adott fejezetben) a nyers oldal-helyi fejezet/vers-szam kerul
kozvetlenul hasznalatra (ugyanugy, mint --versifikacios-terkep nelkul).
"""
import argparse
import csv
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

NORMALIZO_TABLA = "konkordancia/Konyv_normalizalo_tabla.tsv"
USER_AGENT = "Mozilla/5.0 (compatible; lxx-kivonat-fetch/1.0; +bible-study-repo)"
KERES_KESLELTETES_MP = 1.0

# studybible.info a teljes angol (KJV-hagyomanyu) konyvnevet varja az URL-ben.
# A STEP-rovidites hidalja at ezt a Konyv_normalizalo_tabla.tsv magyar
# oszlopaihoz (l. a tablazat elso oszlopa).
ANGOL_NEV_TO_STEP = {
    "Genesis": "Gen", "Exodus": "Exo", "Leviticus": "Lev", "Numbers": "Num",
    "Deuteronomy": "Deu", "Joshua": "Jos", "Judges": "Jdg", "Ruth": "Rut",
    "1 Samuel": "1Sa", "2 Samuel": "2Sa", "1 Kings": "1Ki", "2 Kings": "2Ki",
    "1 Chronicles": "1Ch", "2 Chronicles": "2Ch", "Ezra": "Ezr",
    "Nehemiah": "Neh", "Esther": "Est", "Job": "Job", "Psalms": "Psa",
    "Proverbs": "Pro", "Ecclesiastes": "Ecc", "Song of Solomon": "Sng",
    "Isaiah": "Isa", "Jeremiah": "Jer", "Lamentations": "Lam",
    "Ezekiel": "Ezk", "Daniel": "Dan", "Hosea": "Hos", "Joel": "Jol",
    "Amos": "Amo", "Obadiah": "Oba", "Jonah": "Jon", "Micah": "Mic",
    "Nahum": "Nam", "Habakkuk": "Hab", "Zephaniah": "Zep", "Haggai": "Hag",
    "Zechariah": "Zec", "Malachi": "Mal",
}

VERS_JELOLO_RE = re.compile(
    r'<span class="ref greek">(?:<a[^>]*>)?\s*(\d+)\s*(?:</a>)?</span>\s*</span>'
)
SZO_EGYSEG_RE = re.compile(
    r'<span class="unit">\s*<span class="strongs">(.*?)</span>\s*'
    r'<span class="tvm">(.*?)</span>\s*<span class="greek">(.*?)</span>\s*</span>',
    re.DOTALL,
)
STRONG_RE = re.compile(r'([GH]\d+)')
MORF_RE = re.compile(r'>([^<>]+)</a>')
ZAROJEL_PREFIX_RE = re.compile(r'^\[(\d+):(\d+)[^\]]*\]\s*')
GOROG_LXX_VERS_RE = re.compile(r'^[A-Za-z]+\.(\d+):(\d+)(?:-(\d+))?([a-z]?)$')


def normalize_strong(strong):
    """G86 -> G0086, H430 -> H0430 (4 szamjegyre padolva, l. eszkozok/merge_karoli_szofaj.py)."""
    m = re.match(r"^([HG])(\d+)([A-Za-z]*)$", strong)
    if not m:
        return strong
    letter, digits, suffix = m.groups()
    return f"{letter}{int(digits):04d}{suffix}"


def load_magyar_konyvnev(step_kod):
    with open(NORMALIZO_TABLA, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            if row and row[0] == step_kod:
                return row[1]
    return None


def fetch_html(konyv_angol, fejezet):
    url = "https://studybible.info/LXX_WH/" + urllib.parse.quote(f"{konyv_angol} {fejezet}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP hiba {konyv_angol} {fejezet} letoltesekor: {e}") from e


KAROLI_1908_UTVONAL = "konkordancia/Karoli_1908.tsv"


def load_karoli_max_vers(path, karoli_konyv_prefix):
    """Konyvenkent (fejezet -> legnagyobb Karoli-vers-szam) a Karoli_1908.tsv-bol."""
    igehely_re = re.compile(rf'^{re.escape(karoli_konyv_prefix)} (\d+):(\d+)$')
    max_vers = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if not row:
                continue
            m = igehely_re.match(row[0])
            if not m:
                continue
            fejezet, vers = int(m.group(1)), int(m.group(2))
            if vers > max_vers.get(fejezet, 0):
                max_vers[fejezet] = vers
    return max_vers


def load_karoli_letezo_igehelyek(path, karoli_konyv_prefix):
    """A Karoli_1908.tsv-ben ENYLEGESEN letezo Igehely-ertekek halmaza egy konyvre.

    Pl. Eszter csak 10 fejezetet tartalmaz a protestans (nem-deuterokanoni)
    Karoliban - a versifikacios-terkep nehany sora (a gorog apokrif
    toldalekokhoz, pl. "Eszt 12:1"-"Eszt 16:x") olyan Karoli_igehely erteket
    ad meg celkent, ami a valosagban SOHA nem letezett a Karoliban. Ezt a
    halmazt hasznalva a load_versifikacios_terkep() ki tudja szurni az ilyen,
    fabrikalt cel-hivatkozasu sorokat, mielott azok a keresoszotarba
    kerulnenek (l. ott a hasznalatot).
    """
    igehely_re = re.compile(rf'^{re.escape(karoli_konyv_prefix)} \d+:\d+$')
    letezo = set()
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if row and igehely_re.match(row[0]):
                letezo.add(row[0])
    return letezo


def load_versifikacios_terkep(path, karoli_konyv_prefix, karoli_1908_path=KAROLI_1908_UTVONAL):
    """Betolti a LXX_versificacios_terkep.tsv-t egy adott Karoli-konyvre (pl. 'Zsolt', 'Jóel').

    Visszaad: ((kert_fejezet:int, zarojel_fejezet:int, zarojel_vers:int) -> Karoli_igehely)
    dict, egy figyelmeztetes-lista (utkozesek/kihagyasok a README-hez), es egy
    kulon "betu_utotag_kizarasok" lista - (konyv, Karoli_igehely, oszlop,
    nyers_ertek) sorok azokrol a betu-utotagos al-vers-hivatkozasokrol
    (pl. "Exo.28:22a"), amiket a nyers LXX_WH oldal szonkenti szinten nem
    kulonboztet meg, ezert explicit kizarodtak (l. gyujt() belsejeben).

    A kulcs elso eleme a LEKERDEZETT (Karoli-fejezetszammal megegyezo) oldal
    fejezetszama, mert ugyanaz a zarojeles [fejezet:vers] ertek (pl. "53:4")
    ket KULONBOZO oldalon is elofordulhat teljesen mas jelentessel: sajat
    oldalan (pl. a "Psalms 53" oldalon egy belso cim-eltolodas miatt) ES egy
    masik zsoltar oldalan kereszthivatkozaskent (pl. a "Psalms 54" oldalon a
    LXX-fejezet-eltolodas miatt) - a lekerdezett fejezet nelkul ezek
    utkoznenek egy lapos globalis szotarban.
    """
    # A studybible.info nyers HTML-jeben a szo elejere irt [fejezet:vers]
    # zarojel konyvenkent KOVETKEZETESEN vagy a Gorog_LXX_vers, vagy a
    # Heber_vers oszloppal egyezik (empirikusan ellenorizve: Zsoltaroknal a
    # Gorog-gal, pl. Zsolt 110:4 -> [109:4]; Joelnel a Heber-rel, pl.
    # Jóel 3:1 -> [4:1]) - SOHA nem mindkettovel egyszerre egy adott konyvben.
    # Ezert KET KULON szotar epul (elsodleges: Gorog_LXX_vers, tartalek:
    # Heber_vers), nem egy kozos - igy a ket oszlop verszam-terei nem
    # utkozhetnek hamisan (pl. Zsolt 147-nel a Heber_vers ertekei az elso
    # felben ugyanazt a fejezetszamot hasznaljak, mint a Gorog_LXX_vers a
    # masodik felben, l. Validacios_naplo/README).
    karoli_fejezet_re = re.compile(rf'^{re.escape(karoli_konyv_prefix)} (\d+):(\d+)$')
    letezo_igehelyek = load_karoli_letezo_igehelyek(karoli_1908_path, karoli_konyv_prefix)

    def gyujt(oszlopnev, cimke):
        renumber_sorok = []
        egyeb_sorok = []
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                igehely = row["Karoli_igehely"]
                karoli_m = karoli_fejezet_re.match(igehely)
                if not karoli_m:
                    continue
                if igehely not in letezo_igehelyek:
                    # A terkep celkent olyan "Karoli-verset" ad meg, ami a
                    # valosagban SOHA nem letezett a Karoli_1908.tsv-ben (pl.
                    # a gorog apokrif Eszter-toldalekok "Eszt 12:1".."Eszt
                    # 16:x" cimkei - a protestans Karoli csak 10 fejezetet
                    # tartalmaz Eszterbol). Ezt a sort SOHA nem szabad
                    # indexelni, kulonben fabrikalt, nem-letezo Igehely-
                    # cimke kerulne a vegso kimenetbe (l. Zsolt 151 mintajara:
                    # ha nincs valodi Karoli-cel, a szonak uresen kell
                    # maradnia, nem egy kitalalt cimke alatt megjelennie).
                    figyelmeztetesek.append(
                        f"KIHAGYVA (nem letezik a Karoliban, {cimke}): '{igehely}' "
                        f"nem valodi Karoli-vers - a rea mutato zarojel-hivatkozas "
                        f"uresen marad"
                    )
                    continue
                # FONTOS: ha EZ az oszlop (Gorog/Heber) ugyis megegyezik mar
                # a Karolival ehhez a sorhoz (a Karoli_egyezik_hol felsorolja),
                # akkor ez a bejegyzes CSAK trivialis onhivatkozas lenne (a
                # nyers oldal sosem bocsatana ki ra zarojelet, hiszen mar
                # egyezik) - SZANDEKOSAN NEM indexeljuk be, mert a nyers
                # zarojel-szam (fejezet,vers) UGYANAZ lehet, mint egy MASIK
                # Karoli-vers VALODI (tenylegesen elterő) kereszthivatkozasa
                # ugyanebben az oszlopban - a trivialis bejegyzes indexelese
                # alhamis utkozest okozna, ami a keresesnel (or-lancolat)
                # csendben a rossz erteket adna vissza (l. 1Moz 31:55/32:1
                # eset: a Gorog oszlop mindket szomszedos versnel trivialisan
                # egyezik a Karolival, mikozben a Heber oszlop valodi +1
                # eltolast hordoz - enelkul a szures nelkul a trivialis
                # Gorog-bejegyzesek felulirnak egy masik vers valodi
                # Heber-alapu zarojel-celjat, mert a lookup Gorog-ot probalja
                # elsokent).
                if cimke in row["Karoli_egyezik_hol"].split(","):
                    continue
                kert_fejezet = int(karoli_m.group(1))
                nyers_ertek = row[oszlopnev].strip()
                m = GOROG_LXX_VERS_RE.match(nyers_ertek)
                if not m:
                    continue  # pl. korrupt "Psa.Psa.151:x" sor (l. README) - szandekosan kimarad
                if m.group(4):
                    # Betu-utotagos al-vers-hivatkozas (pl. "Exo.28:22a") - ez
                    # egy Karoli-versre bontott LXX-felvers-hatart jelolne, DE
                    # a nyers studybible.info/LXX_WH oldal (ellenorizve tobb
                    # konyvon: 2Moz 28/36-37, Zsolt 12(13), 1Kir 12/14) NEM
                    # bontja szonkenti szinten kulon zarojellel az egyes
                    # al-verseket - vagy egyaltalan nincs zarojel a nyers
                    # oldalon erre a szora, vagy van, de MAS (nem a terkeppel
                    # egyezo) szamra/betüre mutat. A szavak Karoli-versek
                    # kozotti szetosztasa emiatt TARTALMI dontes lenne, nem
                    # mechanikus kulcs-egyeztetes - ezert EXPLICIT kizarjuk
                    # (nem probaljuk megbecsulni/szetosztani), ugyanugy, mint
                    # a nem letezo Karoli-celu sorokat.
                    figyelmeztetesek.append(
                        f"TOMB_HATAR_NEM_SZETVALASZTHATO ({cimke}): '{igehely}' <- "
                        f"'{nyers_ertek}' - a LXX_WH-oldal nem bontja szonkenti "
                        f"szinten a Karoli-alverseket, a zarojel-hivatkozas kizarva"
                    )
                    betu_utotag_kizarasok.append((karoli_konyv_prefix, igehely, cimke, nyers_ertek))
                    continue
                fejezet = int(m.group(1))
                v1 = int(m.group(2))
                v2 = int(m.group(3)) if m.group(3) else v1
                entry = (kert_fejezet, fejezet, v1, v2, igehely)
                if row["Elteres_tipusa"] == "Renumber":
                    renumber_sorok.append(entry)
                else:
                    egyeb_sorok.append(entry)
        return renumber_sorok, egyeb_sorok

    figyelmeztetesek = []
    betu_utotag_kizarasok = []

    def epit(oszlopnev, cimke):
        renumber_sorok, egyeb_sorok = gyujt(oszlopnev, cimke)
        lookup = {}
        for kert_fejezet, fejezet, v1, v2, igehely in renumber_sorok:
            for v in range(v1, v2 + 1):
                kulcs = (kert_fejezet, fejezet, v)
                if kulcs in lookup and lookup[kulcs] != igehely:
                    figyelmeztetesek.append(
                        f"UTKOZES (Renumber, {cimke}): {kulcs} mar '{lookup[kulcs]}'-hez rendelve, "
                        f"ujabb jelolt '{igehely}' figyelmen kivul hagyva"
                    )
                    continue
                lookup[kulcs] = igehely
        for kert_fejezet, fejezet, v1, v2, igehely in egyeb_sorok:
            for v in range(v1, v2 + 1):
                kulcs = (kert_fejezet, fejezet, v)
                if kulcs in lookup:
                    if lookup[kulcs] != igehely:
                        figyelmeztetesek.append(
                            f"KIHAGYVA (nem-Renumber, {cimke}, mar lefoglalva): {kulcs} -> "
                            f"'{lookup[kulcs]}' marad ervenyben, NEM '{igehely}'"
                        )
                    continue
                lookup[kulcs] = igehely

        # Cim-felirat-potlas: nehany zsoltarnal (pl. Zsolt 12, 18-21, 30...) a
        # Karoli maga is ONALLO 1. versnek szamozza a puszta zsoltar-feliratot
        # (pl. "Zsolt 20:1: Az éneklőmesternek; Dávid zsoltára."), szemben a
        # tobbsegi esettel, ahol a felirat beleolvad a Karoli 1. versebe vagy
        # egyaltalan nincs is felirat - emiatt a terkep ILYENKOR NEM
        # dokumental kulon sort a felirat-vershez (a terkep-generalas csak az
        # elteres-eseteket rogziti, es ezt a mintat nem ismerte fel). Mivel a
        # nyers HTML-ben a felirat MINDIG a fejezet elso [fejezet:1] zarojelu
        # szava, es a Karoli-fejezet TOBBI verse mar dokumentalt egy adott
        # zarojel-fejezettel (fo), ez biztonsagosan levezethetô: ha egy adott
        # kert_fejezethez a terkepben dokumentalt LEGKISEBB vers pontosan 2
        # (azaz nincs sajat 1-es bejegyzes), a hianyzo (fo, 1) kulcsot a
        # Karoli fejezet 1. versehez rendeljuk.
        legkisebb_vers = {}
        for (kf, fo, v), ig in lookup.items():
            if kf not in legkisebb_vers or v < legkisebb_vers[kf][0]:
                legkisebb_vers[kf] = (v, fo)
        for kf, (min_v, fo) in legkisebb_vers.items():
            if min_v == 2:
                kulcs1 = (kf, fo, 1)
                if kulcs1 not in lookup:
                    lookup[kulcs1] = f"{karoli_konyv_prefix} {kf}:1"

        # Zaro-vers-potlas: sok zsoltarnal (pl. konyv-elvalaszto doxologia,
        # "Áldott az Úr..." tipusu zaro sor) a terkep a fejezet UTOLSO
        # Karoli-versehez sem dokumental sort, ugyanazon okbol, mint a
        # cim-felirat-hianynal (a terkep-generalas nem fedte le a fejezet-
        # hatarokat teljesen). Ha egy adott kert_fejezetnel a terkepben
        # dokumentalt LEGNAGYOBB Karoli-vers pontosan eggyel kisebb, mint a
        # Karoli_1908.tsv-ben tenylegesen letezo utolso vers, a hianyzo
        # zarojel-kulcsot (ugyanaz a fo, bracket_v+1) a kovetkezo Karoli
        # vershez rendeljuk.
        karoli_v_re = re.compile(rf'^{re.escape(karoli_konyv_prefix)} (\d+):(\d+)$')
        legnagyobb_vers = {}
        for (kf, fo, bracket_v), ig in lookup.items():
            m = karoli_v_re.match(ig)
            if not m:
                continue
            karoli_v = int(m.group(2))
            if kf not in legnagyobb_vers or karoli_v > legnagyobb_vers[kf][0]:
                legnagyobb_vers[kf] = (karoli_v, fo, bracket_v)
        karoli_max = load_karoli_max_vers(karoli_1908_path, karoli_konyv_prefix)
        for kf, (max_karoli_v, fo, bracket_v) in legnagyobb_vers.items():
            if karoli_max.get(kf) == max_karoli_v + 1:
                kulcs_uj = (kf, fo, bracket_v + 1)
                if kulcs_uj not in lookup:
                    lookup[kulcs_uj] = f"{karoli_konyv_prefix} {kf}:{max_karoli_v + 1}"
        return lookup

    gorog_lookup = epit("Gorog_LXX_vers", "Gorog")
    heber_lookup = epit("Heber_vers", "Heber")
    return (gorog_lookup, heber_lookup), figyelmeztetesek, betu_utotag_kizarasok


def parse_chapter(html, magyar_konyv, fejezet, vers_lookup=None, hianyzo_kulcsok=None):
    """Egy fejezet HTML-jebol kinyeri a (Igehely, Strong-szam, Gorog szoalak, Morf kod) sorokat.

    Ha vers_lookup meg van adva, a szo elejere irt `[fejezet:vers]` zarojeles
    LXX-hivatkozas (ha van) vezerli az Igehely-cimkezest a terkepen keresztul;
    kulonben (nincs zarojel az adott fejezetben) a nyers oldal-helyi
    fejezet/vers-szam kerul hasznalatra, ugyanugy mint vers_lookup nelkul.
    """
    matches = list(VERS_JELOLO_RE.finditer(html))
    rows = []
    for i, m in enumerate(matches):
        vers_szam = int(m.group(1))
        block_start = m.end()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        block = html[block_start:block_end]
        aktualis_kulcs = (fejezet, vers_szam)
        zarojel_volt = False
        for su in SZO_EGYSEG_RE.finditer(block):
            strongs_raw, tvm_raw, greek_raw = su.groups()
            strong_m = STRONG_RE.search(strongs_raw)
            if not strong_m:
                continue  # nincs Strong-szam -> kimarad a kivonatbol
            strong = normalize_strong(strong_m.group(1))
            morf_m = MORF_RE.search(tvm_raw)
            morf = morf_m.group(1).strip() if morf_m else tvm_raw.strip()
            greek_stripped = greek_raw.strip()
            zarojel_m = ZAROJEL_PREFIX_RE.match(greek_stripped)
            if zarojel_m:
                aktualis_kulcs = (int(zarojel_m.group(1)), int(zarojel_m.group(2)))
                zarojel_volt = True
            szo = ZAROJEL_PREFIX_RE.sub("", greek_stripped).strip()
            if not szo:
                continue
            if vers_lookup is not None and zarojel_volt:
                gorog_lookup, heber_lookup = vers_lookup
                lookup_kulcs = (fejezet, aktualis_kulcs[0], aktualis_kulcs[1])
                igehely = gorog_lookup.get(lookup_kulcs) or heber_lookup.get(lookup_kulcs)
                if igehely is None:
                    # Nincs Karoli-vers-megfeleltetes ehhez az LXX-hivatkozashoz
                    # (pl. cim-felirat-only LXX-vers vagy a 150. zsoltar utani
                    # apokrif 151. zsoltar-toldalek) - a szo szandekosan
                    # kimarad a kimenetbol, l. README.
                    if hianyzo_kulcsok is not None:
                        hianyzo_kulcsok.add(lookup_kulcs)
                    continue
            else:
                igehely = f"{magyar_konyv} {fejezet}:{vers_szam}"
            rows.append((igehely, strong, szo, morf))
    return rows


def parse_fejezet_lista(args):
    if args.fejezetek:
        return [int(x) for x in args.fejezetek.split(",") if x.strip()]
    if args.fejezet_tol and args.fejezet_ig:
        return list(range(args.fejezet_tol, args.fejezet_ig + 1))
    raise SystemExit("Meg kell adni --fejezetek VAGY --fejezet-tol/--fejezet-ig parametert.")


def main():
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--konyv", required=True, help="Angol konyvnev, pl. Psalms, Joel, Genesis")
    ap.add_argument("--fejezetek", help="Vesszovel elvalasztott fejezetlista, pl. 16,110")
    ap.add_argument("--fejezet-tol", type=int, dest="fejezet_tol")
    ap.add_argument("--fejezet-ig", type=int, dest="fejezet_ig")
    ap.add_argument("--kimenet", required=True, help="Kimeneti TSV fajl utvonala")
    ap.add_argument(
        "--versifikacios-terkep",
        dest="versifikacios_terkep",
        help="konkordancia/LXX_versificacios_terkep.tsv utvonala (opcionalis, l. modulszintu docstring)",
    )
    ap.add_argument(
        "--karoli-konyv-prefix",
        dest="karoli_konyv_prefix",
        help="Karoli-konyvnev-prefix a terkep Karoli_igehely oszlopahoz, pl. 'Zsolt', 'Jóel' "
        "(kotelezo, ha --versifikacios-terkep meg van adva)",
    )
    args = ap.parse_args()

    step_kod = ANGOL_NEV_TO_STEP.get(args.konyv)
    if not step_kod:
        raise SystemExit(f"Ismeretlen konyvnev: {args.konyv!r} (nincs a ANGOL_NEV_TO_STEP tablaban)")
    magyar_konyv = load_magyar_konyvnev(step_kod)
    if not magyar_konyv:
        raise SystemExit(f"'{step_kod}' STEP-kod nem talalhato a {NORMALIZO_TABLA} fajlban")

    vers_lookup = None
    if args.versifikacios_terkep:
        if not args.karoli_konyv_prefix:
            raise SystemExit("--versifikacios-terkep hasznalatahoz --karoli-konyv-prefix is kotelezo")
        vers_lookup, figyelmeztetesek, _betu_utotag_kizarasok = load_versifikacios_terkep(
            args.versifikacios_terkep, args.karoli_konyv_prefix
        )
        gorog_n, heber_n = len(vers_lookup[0]), len(vers_lookup[1])
        print(
            f"Versifikacios terkep betoltve: {gorog_n} Gorog-kulcs + {heber_n} Heber-kulcs",
            file=sys.stderr,
        )
        for fig in figyelmeztetesek:
            print(f"  FIGYELMEZTETES: {fig}", file=sys.stderr)

    fejezetek = parse_fejezet_lista(args)

    all_rows = []
    hianyzo_kulcsok = set()
    for idx, fejezet in enumerate(fejezetek):
        if idx > 0:
            time.sleep(KERES_KESLELTETES_MP)
        print(f"Letoltes: {args.konyv} {fejezet} ...", file=sys.stderr)
        html = fetch_html(args.konyv, fejezet)
        rows = parse_chapter(html, magyar_konyv, fejezet, vers_lookup, hianyzo_kulcsok)
        print(f"  -> {len(rows)} sor ({magyar_konyv} {fejezet})", file=sys.stderr)
        all_rows.extend(rows)

    with open(args.kimenet, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Igehely", "Strong-szám", "Görög szóalak", "Morfológiai kód"])
        writer.writerows(all_rows)

    if hianyzo_kulcsok:
        print(f"FIGYELEM: {len(hianyzo_kulcsok)} zarojeles LXX-kulcshoz nem volt terkep-talalat:", file=sys.stderr)
        for kulcs in sorted(hianyzo_kulcsok):
            print(f"  {kulcs}", file=sys.stderr)

    print(f"Kesz: {len(all_rows)} adatsor -> {args.kimenet}", file=sys.stderr)


if __name__ == "__main__":
    main()
