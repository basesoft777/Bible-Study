#!/usr/bin/env python3
"""Kombinalt (LXX_WH + ABP) LXX-kivonat letoltő/parszoló szkript.

Hasznalat:
  python eszkozok/lxx_kivonat_fetch_v2.py --konyv Genesis --fejezetek 12,13 --kimenet out.tsv
  python eszkozok/lxx_kivonat_fetch_v2.py --konyv Psalms --fejezet-tol 1 --fejezet-ig 150 \
      --kimenet out.tsv --versifikacios-terkep konkordancia/LXX_versificacios_terkep.tsv \
      --karoli-konyv-prefix Zsolt

Ez a szkript az eredeti `lxx_kivonat_fetch.py`-ra epul (ujrahasznositja annak
normalizo-tabla / versifikacios-terkep / Strong-normalizalo logikajat), de
KET forrast kombinal fejezetenkent, MINDEN Strong-hianyos LXX_WH-szot
megprobalva potolni az ABP (Apostolic Bible Polyglot) interlinear oldalrol:

  1. Elsodleges forras: https://studybible.info/LXX_WH/<Konyv>%20<fejezet>
     (megtartja a morfologiai kod-oszlopot, l. eredeti szkript)
  2. Masodlagos/potlo forras: https://studybible.info/interlinear/<Konyv>%20<fejezet>
     (ABP - mas szovegcsalad, eltero Strong-lefedettseg, NINCS morfologiai kod)

A v1 szkripttel ellentetben ez a valtozat a Strong-szam NELKULI LXX_WH-
egysegeket (szavakat) IS megtartja belsőleg (nem dobja el csendben), hogy
"res"-kent (gap) kezelhesse őket:

  - Minden verset szo-egysegek RENDEZETT listajakent dolgoz fel mindket
    forrasbol (LXX_WH es ABP), Strong-szammal VAGY anelkul.
  - Minden LXX_WH "res"-hez (Strong nelkuli szo) megkeresi az ABP listaban
    azt az egysget, amelynek KOZVETLEN elozo es kovetkezo Strong-taggelt
    szomszedja PONTOSAN megegyezik a LXX_WH res elozo/kovetkezo Strong-
    szomszedjaval (ugyanaz a kontextus-illesztes, mint amit a G1941-korben
    kezzel validaltunk). Csak EGYERTELMU (pontosan egy jelolt) talalat
    eseten tortenik potlas.
  - Verset-szinten ELLENORZI, hogy a ket forras Strong-taggelt szo-
    sorozata (sorrend-tarto reszsorozat ertelemben) osszeegyeztetheto-e.
    Ha NEM (pl. eltero szoszam/szorend - szovegcsalad-elteres gyanuja),
    a teljes verset "ELTERO_SZOVEGALAP"-kent jelzi, es AZ ADOTT VERSBEN
    NEM probal ABP-potlast vegezni (a meglevo LXX_WH-adat megmarad, a
    resek uresen maradnak, kulon jelolve).
  - Azokat a reseket, ahol SEM az egyik, SEM a masik forras nem ad Strong-
    szamot (pl. valodi, egyik oldalon sem taggelt tulajdonnev), explicit
    uresen hagyja.

Kimeneti oszlopok (5, az eredeti 4 + 1 uj):
  Igehely | Strong-szam | Gorog szoalak | Morfologiai kod | Forras

A `Forras` oszlop erteke minden sornal:
  - "LXX_WH"           - a szo eredetileg is Strong-taggelt volt az LXX_WH oldalon
  - "ABP-potolt"        - a Strong-szamot az ABP oldalrol potoltuk (kontextus-egyezes alapjan)
  - "ELTERO_SZOVEGALAP" - a verset szovegcsalad-elteres miatt jelzett resz-sora (nincs potlas)
  - ""  (ures)          - egyik forras sem ad Strong-szamot erre a szora (nem tevesztes, hanem
                           valodi, mindket oldalon egyezoen Strong nelkuli szo, pl. tulajdonnev)

LICENC-MEGJEGYZES: l. a `konkordancia/LXX_kivonat_*_README.md` fajlokban
dokumentalt licenc-gap - a studybible.info (mind LXX_WH, mind ABP/interlinear
verzio) forrasanak licenc-statusza tisztazatlan. **Ez az adat kizarolag
belso munkafolyamat-celu, NEM publikus** kimenet, amig a licenc-kerdes nem
tisztazodik.
"""
import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from lxx_kivonat_fetch import (  # noqa: E402
    ANGOL_NEV_TO_STEP,
    MORF_RE,
    SZO_EGYSEG_RE,
    VERS_JELOLO_RE,
    ZAROJEL_PREFIX_RE,
    load_magyar_konyvnev,
    load_versifikacios_terkep,
    normalize_strong,
)

USER_AGENT = "Mozilla/5.0 (compatible; lxx-kivonat-fetch-v2/1.0; +bible-study-repo)"
KERES_KESLELTETES_MP = 1.0

STRONG_RE = re.compile(r'([GH]\d+)')

# ABP (interlinear) oldal HTML-mintaja - MAS szerkezet, mint az LXX_WH-e:
# nincs "tvm" (morfologia) span, "english" span van helyette, es a
# vers-jelolo egyseg "<a href=...>fejezet:vers</a>" alaku (nem csak puszta
# vers-szam, mint az LXX_WH-nal).
ABP_VERS_JELOLO_RE = re.compile(
    r'<span class="strongs">&nbsp;</span>\s*'
    r'<span class="ref greek">(?:<a[^>]*>)?\s*(\d+):(\d+)\s*(?:</a>)?</span>\s*'
    r'<span class="english">&nbsp;</span>\s*</span>'
)
ABP_SZO_EGYSEG_RE = re.compile(
    r'<span class="unit">\s*<span class="strongs">(.*?)</span>\s*'
    r'<span class="greek">(.*?)</span>\s*<span class="english">(.*?)</span>\s*</span>',
    re.DOTALL,
)


class Szo:
    """Egy szo-egyseg egy versen belul (Strong-szammal vagy anelkul)."""

    __slots__ = ("strong", "greek", "morf")

    def __init__(self, strong, greek, morf):
        self.strong = strong  # normalizalt "G####"/"H####" vagy None
        self.greek = greek
        self.morf = morf  # csak LXX_WH-nal ertelmezett, ABP-nal mindig None


def fetch_html(alap_url, konyv_angol, fejezet):
    url = alap_url + urllib.parse.quote(f"{konyv_angol} {fejezet}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP hiba {url} letoltesekor: {e}") from e


def parse_lxxwh_chapter(html):
    """(fejezet:vers) -> [Szo, ...] a nyers LXX_WH oldal HTML-jebol.

    A v1-tol elteroen a Strong nelkuli egysegeket IS megtartja (Szo(strong=None, ...)).
    """
    matches = list(VERS_JELOLO_RE.finditer(html))
    versek = {}
    for i, m in enumerate(matches):
        vers_szam = int(m.group(1))
        block_start = m.end()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        block = html[block_start:block_end]
        szavak = []
        for su in SZO_EGYSEG_RE.finditer(block):
            strongs_raw, tvm_raw, greek_raw = su.groups()
            strong_m = STRONG_RE.search(strongs_raw)
            strong = normalize_strong(strong_m.group(1)) if strong_m else None
            morf_m = MORF_RE.search(tvm_raw)
            morf = morf_m.group(1).strip() if morf_m else (tvm_raw.strip() or None)
            greek = ZAROJEL_PREFIX_RE.sub("", greek_raw.strip()).strip()
            if not greek:
                continue
            szavak.append(Szo(strong, greek, morf))
        versek[vers_szam] = szavak
    return versek


def parse_abp_chapter(html):
    """(fejezet:vers) -> [Szo, ...] a nyers ABP/interlinear oldal HTML-jebol.

    Osszetett Strong-egysegeknel (pl. "4633-1473" ket <a> tag egy strongs
    spanban, tobbszavas gorog alak, pl. "σκηνην αυτου") - ha a szoszam
    (whitespace-szeparalt gorog szavak) megegyezik a Strong-szamokeval,
    szetbontjuk kulon Szo-kra; kulonben (ritka, pl. osszevont alak) egyetlen
    Szo-t kepzunk az ELSO Strong-szammal (konzervativ leegyszerusites - ez
    csak a kontextus-illesztes pontossagat csokkentheti minimalisan az
    erintett ritka esetekben, uj adatot nem talal ki).
    """
    marker_positions = [(m.start(), m.end(), (int(m.group(1)), int(m.group(2))))
                         for m in ABP_VERS_JELOLO_RE.finditer(html)]
    versek = {}
    for i, (start, end, kulcs) in enumerate(marker_positions):
        block_end = marker_positions[i + 1][0] if i + 1 < len(marker_positions) else len(html)
        block = html[end:block_end]
        szavak = []
        for su in ABP_SZO_EGYSEG_RE.finditer(block):
            strongs_raw, greek_raw, _english_raw = su.groups()
            strong_matches = [normalize_strong(s) for s in STRONG_RE.findall(strongs_raw)]
            greek = greek_raw.strip()
            if strongs_raw.strip() == "*" or not strong_matches:
                if greek:
                    szavak.append(Szo(None, greek, None))
                continue
            gorog_reszek = greek.split()
            if len(gorog_reszek) == len(strong_matches):
                for strong, resz in zip(strong_matches, gorog_reszek):
                    szavak.append(Szo(strong, resz, None))
            else:
                szavak.append(Szo(strong_matches[0], greek, None))
        # csak a konyv-fejezet szinten kert fejezetre szukitunk kesobb - itt
        # meg a (fejezet, vers) kulcsot kell megtartani, mert az ABP oldal
        # kereszthivatkozasokat is tartalmazhat MAS fejezetre (pl. parhuzamos
        # utalasok) - ezeket a hivo fuggveny sziiri a keresett fejezetre.
        versek[kulcs] = szavak
    return versek


def elozo_strong(szavak, idx):
    for j in range(idx - 1, -1, -1):
        if szavak[j].strong:
            return szavak[j].strong
    return None


def kovetkezo_strong(szavak, idx):
    for j in range(idx + 1, len(szavak)):
        if szavak[j].strong:
            return szavak[j].strong
    return None


def strong_sorozat(szavak):
    return [sz.strong for sz in szavak if sz.strong]


def sorrendtarto_reszsorozat(a, b):
    """Igaz, ha `a` (lista) sorrend-tarto reszsorozata `b`-nek (b-ben tobb elem is lehet)."""
    it = iter(b)
    return all(x in it for x in a)


def egyeztet_es_potol(lxx_szavak, abp_szavak, log_prefix, figyelmeztetesek):
    """Egy vers LXX_WH szo-listajat egesziti ki ABP-adattal.

    Visszaad: [(strong, forras), ...] - ugyanolyan hosszu, mint lxx_szavak.

    FONTOS (v2-korrekcio a pilot-tapasztalat alapjan): a ket forras Strong-
    szamozasa a nevmasoknal (G1473/G0846/G4771 stb.) GYAKRAN elter akkor is,
    ha a szoveg maga megegyezik (kulonbozo tagg2elesi konvencio, nem valodi
    szovegvariancia) - ezert a vers-szintu szekvencia-egyezes hianya ONMAGABAN
    NEM tiltja le az egyes resek helyi (kozvetlen elozo/kovetkezo Strong-
    kontextus alapjan torteno) potlasat - az minden esetben, verset-szintu
    egyezestol fuggetlenul megtortenik. A vers-szintu elteres csak arra
    hasznalt jelzes, hogy egy FEL NEM OLDOTT resnel (0 vagy tobbertelmu ABP-
    jelolt) melyik magyarazat valoszinubb: valodi szovegcsalad-elteres
    (ELTERO_SZOVEGALAP) vagy tenyleg egyik forras altal sem taggelt szo (ures).
    """
    eredmeny = [(sz.strong, "LXX_WH" if sz.strong else "") for sz in lxx_szavak]

    if abp_szavak is None:
        # nincs ABP-adat ehhez a vershez (pl. az oldal nem adta vissza) -
        # nem probalunk potolni, de nem is jelezzuk hibasan szovegalap-
        # elteresnek - egyszeruen nincs mivel osszevetni.
        return eredmeny

    lxx_core = strong_sorozat(lxx_szavak)
    abp_core = strong_sorozat(abp_szavak)
    vers_szintu_elteres = bool(lxx_core) and not sorrendtarto_reszsorozat(lxx_core, abp_core)
    if vers_szintu_elteres:
        figyelmeztetesek.append(
            f"{log_prefix}: ELTERO_SZOVEGALAP gyanu (LXX_WH Strong-sorozat nem "
            f"sorrend-tarto reszsorozata az ABP-enek) - LXX_WH: {lxx_core} / ABP: {abp_core}"
        )

    for i, sz in enumerate(lxx_szavak):
        if sz.strong:
            continue
        elozo = elozo_strong(lxx_szavak, i)
        kov = kovetkezo_strong(lxx_szavak, i)
        jeloltek = []
        for j, asz in enumerate(abp_szavak):
            if not asz.strong:
                continue
            if elozo_strong(abp_szavak, j) == elozo and kovetkezo_strong(abp_szavak, j) == kov:
                jeloltek.append(asz.strong)
        egyedi_jeloltek = set(jeloltek)
        if len(egyedi_jeloltek) == 1:
            eredmeny[i] = (jeloltek[0], "ABP-potolt")
        elif len(egyedi_jeloltek) > 1:
            figyelmeztetesek.append(
                f"{log_prefix}: TOBBERTELMU ABP-jelolt a(z) '{sz.greek}' szohoz "
                f"(elozo={elozo}, kov={kov}) -> {sorted(egyedi_jeloltek)} - nincs potlas"
            )
        elif vers_szintu_elteres:
            eredmeny[i] = (None, "ELTERO_SZOVEGALAP")
        # 0 jelolt, verset-szinten nincs elteres -> csendben ures marad
        # (mindket forras egyezoen nem taggeli - tipikusan valodi tulajdonnev)

    return eredmeny


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
    ap.add_argument("--versifikacios-terkep", dest="versifikacios_terkep")
    ap.add_argument("--karoli-konyv-prefix", dest="karoli_konyv_prefix")
    ap.add_argument(
        "--keslekedes", type=float, default=KERES_KESLELTETES_MP,
        help="Kereses kozotti szunet masodpercben (forras-oldal kimelese, alapertelmezett: 1.0)",
    )
    args = ap.parse_args()

    step_kod = ANGOL_NEV_TO_STEP.get(args.konyv)
    if not step_kod:
        raise SystemExit(f"Ismeretlen konyvnev: {args.konyv!r} (nincs a ANGOL_NEV_TO_STEP tablaban)")
    magyar_konyv = load_magyar_konyvnev(step_kod)
    if not magyar_konyv:
        raise SystemExit(f"'{step_kod}' STEP-kod nem talalhato a normalizo-tablaban")

    vers_lookup = None
    if args.versifikacios_terkep:
        if not args.karoli_konyv_prefix:
            raise SystemExit("--versifikacios-terkep hasznalatahoz --karoli-konyv-prefix is kotelezo")
        vers_lookup, figyelmeztetesek = load_versifikacios_terkep(
            args.versifikacios_terkep, args.karoli_konyv_prefix
        )
        for fig in figyelmeztetesek:
            print(f"  FIGYELMEZTETES: {fig}", file=sys.stderr)

    fejezetek = parse_fejezet_lista(args)

    all_rows = []
    figyelmeztetesek = []
    hianyzo_kulcsok = set()
    stat = {"lxx_wh": 0, "abp_potolt": 0, "hianyzik": 0, "elutero_szovegalap": 0}

    for idx, fejezet in enumerate(fejezetek):
        if idx > 0:
            time.sleep(args.keslekedes)
        print(f"Letoltes: {args.konyv} {fejezet} (LXX_WH) ...", file=sys.stderr)
        lxx_html = fetch_html("https://studybible.info/LXX_WH/", args.konyv, fejezet)
        time.sleep(args.keslekedes)
        print(f"Letoltes: {args.konyv} {fejezet} (ABP/interlinear) ...", file=sys.stderr)
        abp_html = fetch_html("https://studybible.info/interlinear/", args.konyv, fejezet)

        lxx_versek = parse_lxxwh_chapter(lxx_html)
        abp_versek_raw = parse_abp_chapter(abp_html)
        # az ABP kulcsok (fejezet_helyi, vers) alakuak - a kert fejezetre szukitjuk
        abp_versek = {vers: szavak for (fej, vers), szavak in abp_versek_raw.items() if fej == fejezet}

        fejezet_sor_szam = 0
        for vers_szam in sorted(lxx_versek):
            lxx_szavak = lxx_versek[vers_szam]
            abp_szavak = abp_versek.get(vers_szam)
            log_prefix = f"{args.konyv} {fejezet}:{vers_szam}"
            eredmeny = egyeztet_es_potol(lxx_szavak, abp_szavak, log_prefix, figyelmeztetesek)

            aktualis_kulcs = (fejezet, vers_szam)
            for sz, (strong, forras) in zip(lxx_szavak, eredmeny):
                greek_stripped = sz.greek
                zarojel_m = ZAROJEL_PREFIX_RE.match(greek_stripped)
                if zarojel_m:
                    aktualis_kulcs = (int(zarojel_m.group(1)), int(zarojel_m.group(2)))
                szo = ZAROJEL_PREFIX_RE.sub("", greek_stripped).strip()
                if not szo:
                    continue
                if vers_lookup is not None and zarojel_m:
                    gorog_lookup, heber_lookup = vers_lookup
                    lookup_kulcs = (fejezet, aktualis_kulcs[0], aktualis_kulcs[1])
                    igehely = gorog_lookup.get(lookup_kulcs) or heber_lookup.get(lookup_kulcs)
                    if igehely is None:
                        hianyzo_kulcsok.add(lookup_kulcs)
                        continue
                else:
                    igehely = f"{magyar_konyv} {fejezet}:{vers_szam}"
                all_rows.append((igehely, strong or "", szo, sz.morf or "", forras))
                fejezet_sor_szam += 1
                if forras == "LXX_WH":
                    stat["lxx_wh"] += 1
                elif forras == "ABP-potolt":
                    stat["abp_potolt"] += 1
                elif forras == "ELTERO_SZOVEGALAP":
                    stat["elutero_szovegalap"] += 1
                else:
                    stat["hianyzik"] += 1
        print(f"  -> {fejezet_sor_szam} sor ({magyar_konyv} {fejezet})", file=sys.stderr)

    with open(args.kimenet, "w", encoding="utf-8", newline="") as f:
        import csv
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Igehely", "Strong-szám", "Görög szóalak", "Morfológiai kód", "Forrás"])
        writer.writerows(all_rows)

    if hianyzo_kulcsok:
        print(f"FIGYELEM: {len(hianyzo_kulcsok)} zarojeles LXX-kulcshoz nem volt terkep-talalat:", file=sys.stderr)
        for kulcs in sorted(hianyzo_kulcsok):
            print(f"  {kulcs}", file=sys.stderr)

    if figyelmeztetesek:
        print(f"\nFIGYELMEZTETESEK ({len(figyelmeztetesek)}):", file=sys.stderr)
        for fig in figyelmeztetesek:
            print(f"  {fig}", file=sys.stderr)

    print(
        f"\nKesz: {len(all_rows)} adatsor -> {args.kimenet}\n"
        f"  LXX_WH (eredeti): {stat['lxx_wh']}\n"
        f"  ABP-potolt: {stat['abp_potolt']}\n"
        f"  ELTERO_SZOVEGALAP (nincs potlas): {stat['elutero_szovegalap']}\n"
        f"  Meg mindig hianyzik (egyik forras sem taggeli): {stat['hianyzik']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
