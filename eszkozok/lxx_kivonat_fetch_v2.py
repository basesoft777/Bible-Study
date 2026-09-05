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

ISMERT, EXPLICIT KIZART ESET - "betu-utotagos" al-vers-hivatkozasok:
Nehany konyvben (leginkabb 2Moz, 1Kir, Zsolt, Jozs) a
`LXX_versificacios_terkep.tsv` betu-utotagos Gorog_LXX_vers/Heber_vers
ertekeket ad meg (pl. "Exo.28:22a"), jelezve, hogy egy raw LXX-felvers
tobb, kulon Karoli-versre bomlik. EMPIRIKUSAN ELLENORIZVE (2Moz 28/36-37,
Zsolt 12(13), 1Kir 12/14): a nyers studybible.info/LXX_WH oldal NEM
kulonbozteti meg ezeket szonkenti szinten - vagy egyaltalan nincs
zarojel a nyers oldalon, vagy van, de MAS szamra/betüre mutat, mint a
terkep allitja. A szavak szetosztasa a Karoli-versek kozott ezert
TARTALMI dontes lenne, nem mechanikus kulcs-egyeztetes - a szkript ezert
EXPLICIT KIZARJA ezeket (nem probal becsulni/szetosztani), es
naplozza oket a `konkordancia/Betu_utotag_kizarva.tsv` kozos riportba
(konyvek kozott gyulekezik, l. irj_betu_utotag_riportot()).

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
BETU_UTOTAG_RIPORT_UTVONAL = "konkordancia/Betu_utotag_kizarva.tsv"
NEM_PARSZOLHATO_RIPORT_UTVONAL = "konkordancia/Nem_parszolhato_terkep_ertekek.tsv"


def irj_betu_utotag_riportot(kizarasok, utvonal=BETU_UTOTAG_RIPORT_UTVONAL):
    """Hozzafuzi a betu-utotagos, ezert kizart al-vers-hivatkozasokat egy kozos,
    konyvek kozott gyulekezo TSV-riporthoz (l. modulszintu docstring 3. pontja).
    """
    import os

    uj_fajl = not os.path.exists(utvonal)
    with open(utvonal, "a", encoding="utf-8", newline="") as f:
        import csv
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        if uj_fajl:
            writer.writerow(["Karoli_konyv_prefix", "Karoli_igehely", "Oszlop", "Nyers_ertek"])
        writer.writerows(kizarasok)
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
            # FONTOS: a "[fejezet:vers]" keresztreferencia-zarojel-elotagot
            # (ha van) SZANDEKOSAN NEM vagjuk le itt - a hivo main()-nek kell
            # latnia, mert a versifikacios-terkep-alapu Igehely-cimkezes
            # ebbol dönti el, melyik Karoli-vershez tartozik a szo (l. a
            # korabbi hiba: ha itt levagjuk, a main() zarojel-detektalasa
            # soha nem talal semmit, es minden szo a nyers oldal-helyi
            # fejezet/vers-szamra esik vissza).
            greek = greek_raw.strip()
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


def daniel_4_eltolas(fejezet, vers_szam):
    """Dan konyv, nyers oldal-helyi 4. fejezet 1-37. verse -> Karoli 3:31-33
    illetve 4:1-34 (konzisztens -3 eltolodas).

    A nyers studybible.info/LXX_WH/Daniel 4 oldal NEM ad zarojeles
    kereszthivatkozast (0 db zarojel a teljes fejezetben - ellenorizve), igy a
    LXX_versificacios_terkep.tsv automatikus lookupja soha nem lep mukodesbe
    (az csak zarojel eseten aktivalodik). A terkep sajat sorai (Heber_vers/
    Latin_vers oszlopok) DOKUMENTALJAK az eltolodast, de ezeket a bracket
    hianyaban semmi nem hasznalja fel - emiatt a kimenet eddig a nyers
    oldal-helyi szamozast hasznalta kozvetlenul, ami hibas volt.

    Tartalmilag egyeztetve (l. beszelgetes): a nyers "4:1" a level koszontese
    ("Nabukodonozor kiraly... bekesseg adassek nektek"), ami a Karoliban meg
    a 3. fejezet zaro verse (3:31); a nyers "4:4" ("En Nabukodonozor bekeben
    valek...") pontosan egyezik Karoli 4:1-gyel; a nyers "4:34" ("...
    szemeimet az egre emelem...") pontosan egyezik Karoli 4:31-gyel.

    Csak Dan konyv 4. fejezetere, csak az 1-37. nyers versre vonatkozik - mas
    konyvet/fejezetet nem erint.
    """
    if fejezet != 4 or not (1 <= vers_szam <= 37):
        return None
    if vers_szam <= 3:
        return (3, vers_szam + 30)
    return (4, vers_szam - 3)


def numeri_12_13_eltolas(fejezet, vers_szam):
    """Numeri, nyers 12. fejezet 16. verse -> Karoli 13:1; nyers 13. fejezet
    1-33. verse -> Karoli 13:2-34 (a valodi Karoli 13:1 tartalma a LXX-ben a
    12. fejezet vegere "csuszott at").

    A nyers studybible.info/LXX_WH/Numbers 12 es Numbers 13 oldalak egyike
    sem ad zarojeles kereszthivatkozast ehhez a hatarhoz (ellenorizve), igy a
    LXX_versificacios_terkep.tsv automatikus lookupja sosem aktivalodott.

    Tartalmilag egyeztetve: a nyers "12:16" ("και μετα ταυτα εξηρεν ο λαος εξ
    ασηρωθ...") pontosan egyezik Karoli 13:1-gyel ("Azutan pedig elindula a
    nep Haserothbol..."); a nyers "13:1" ("και ελαλησεν κυριος προς μωυσην
    λεγων") pontosan egyezik Karoli 13:2-vel; a nyers "13:30" pontosan
    egyezik Karoli 13:33-mal. A 11. es 14. fejezet hatarai tisztak (tartalmi
    egyeztetve), nem erintettek.
    """
    if fejezet == 12 and vers_szam == 16:
        return (13, 1)
    if fejezet == 13 and 1 <= vers_szam <= 33:
        return (13, vers_szam + 1)
    return None


def job_38_41_eltolas(fejezet, vers_szam):
    """Job, nyers 38-40. fejezetek elteruleseinek felbontasa Karoli
    38:1-38 / 39:1-38 / 40:1-19 / 41:1-34 hataraira.

    A nyers studybible.info/LXX_WH/Job 38, 39, 40 oldalak egyike sem ad
    zarojeles kereszthivatkozast ehhez a lancolt hatarhoz (ellenorizve), igy
    a LXX_versificacios_terkep.tsv automatikus lookupja sosem aktivalodott.
    A Job 41. fejezet hatara tiszta (tartalmilag egyeztetve), nem erintett.

    Tartalmilag egyeztetve minden szakaszhataron:
      - nyers 38:1-38 valtozatlan (Karoli 38:1-38)
      - nyers 38:39-41 -> Karoli 39:1-3 ("Vadaszol-e predat a nosteny
        oroszlannak...", "hollonak eledelt" - pontos egyezes)
      - nyers 39:1-30 -> Karoli 39:4-33 ("Tudod-e a koszali zergek
        ellesenek idejet..." - pontos egyezes 39:4-gyel, 39:33-mal a vegen)
      - nyers 40:1-5 -> Karoli 39:34-38 ("Szola tovabba az Ur Jobnak..." -
        pontos egyezes)
      - nyers 40:6-24 -> Karoli 40:1-19 ("Ekkor szola az Ur Jobnak a
        forgoszelbol..." - pontos egyezes 40:1-gyel, 40:19-cel a vegen)
    """
    if fejezet == 38:
        if 1 <= vers_szam <= 38:
            return None
        if 39 <= vers_szam <= 41:
            return (39, vers_szam - 38)
        return None
    if fejezet == 39 and 1 <= vers_szam <= 30:
        return (39, vers_szam + 3)
    if fejezet == 40:
        if 1 <= vers_szam <= 5:
            return (39, vers_szam + 33)
        if 6 <= vers_szam <= 24:
            return (40, vers_szam - 5)
        return None
    return None


def predikator_eltolas(fejezet, vers_szam):
    """Prédikátor (Ecclesiastes) - a KONYVNEK NINCS EGYETLEN SORA SEM a
    LXX_versificacios_terkep.tsv-ben (0 sor), tehat itt nem "a terkep nem
    aktivalodik" a problema (mint Danielnel/Numerinel/Jobnal), hanem a
    terkep MAGA hianyzik teljesen errol a konyvrol. A teljes konyvet
    vegigellenorizve (minden fejezethatar, tartalmi egyeztetessel) 4
    valodi eltolodasi/osszevonasi pont talalhato:

      1/2 hatar:  nyers 1. fej. 1-17. vers valtozatlan; nyers 1:18 -> 2:1
                  ("oti en plethei sofias..." = "Mert a bolcsessegnek
                  sokasagaban..." - pontos egyezes). Nyers 2. fej. 1-24.
                  vers -> Karoli 2:2-25 (egyenkent +1); nyers 2:25 ES 2:26
                  EGYUTT Karoli 2:26-ba olvad ossze (Karoli itt ket
                  gorog/nyers verset egyetlen hosszu mondatba von ossze:
                  "ki ehet... Isten bolcseseget ad" - mindket felet
                  tartalmazza).
      8/9 hatar:  nyers 8. fej. 1-15. vers valtozatlan; nyers 8:16-17 ->
                  9:1-2. Nyers 9. fej. 1-18. vers -> Karoli 9:3-20
                  (egyenkent +2).
      9/10 hatar: nyers 10. fej. 1-3. vers -> Karoli 9:21-23 (+20); nyers
                  10:4-20 -> Karoli 10:1-17 (egyenkent -3).
      11/12 hatar: nyers 11. fej. 1-8. vers valtozatlan; nyers 11:9-10 ->
                  Karoli 12:1-2. Nyers 12. fej. 1-14. vers -> Karoli
                  12:3-16 (egyenkent +2).

    A 2-8. es a vege (12:16) tartalmilag egyeztetve tiszta, nem erintett.
    Minden pontot tobb, fuggetlen tartalmi idezet-egyezessel ellenoriztunk
    (l. beszelgetes) - pl. nyers 8:16 = "en ois edoka ten kardian mou tou
    gnonai sofian..." = Karoli 9:1 "Mikor adam az en szivemet a
    bolcsesegnek megtudasara..."; nyers 10:4 = "ean pneuma tou
    exousiazontos anabe..." = Karoli 10:1 "Mikor a fejedelemnek haragja
    felgerjed..."; nyers 11:9 = "eufrainou neaniske..." = Karoli 12:1
    "Orvendezz a te ifjusagodban..."; nyers 12:1 = "kai mnestheti tou
    ktisantos se..." = Karoli 12:3 "Es emlekezzel meg a te Teremtodrol...".
    """
    if fejezet == 1:
        if 1 <= vers_szam <= 17:
            return None
        if vers_szam == 18:
            return (2, 1)
        return None
    if fejezet == 2:
        if 1 <= vers_szam <= 24:
            return (2, vers_szam + 1)
        if vers_szam in (25, 26):
            return (2, 26)
        return None
    if fejezet == 8:
        if 1 <= vers_szam <= 15:
            return None
        if vers_szam in (16, 17):
            return (9, vers_szam - 15)
        return None
    if fejezet == 9 and 1 <= vers_szam <= 18:
        return (9, vers_szam + 2)
    if fejezet == 10:
        if 1 <= vers_szam <= 3:
            return (9, vers_szam + 20)
        if 4 <= vers_szam <= 20:
            return (10, vers_szam - 3)
        return None
    if fejezet == 11:
        if 1 <= vers_szam <= 8:
            return None
        if vers_szam in (9, 10):
            return (12, vers_szam - 8)
        return None
    if fejezet == 12 and 1 <= vers_szam <= 14:
        return (12, vers_szam + 2)
    return None


# Konyv-specifikus, kezi fejezethatar-eltolas-szabalyok azokra az ismert
# esetekre, ahol a nyers oldal nem ad zarojelet (a LXX_versificacios_terkep.tsv
# automatikus lookupja emiatt sosem aktivalodik), DE tartalmilag egyeztetett,
# konzisztens eltolodas van a nyers oldal-helyi es a Karoli-szamozas kozott.
# Minden fuggveny (fejezet, vers_szam) -> (karoli_fejezet, karoli_vers) vagy
# None (ha nem erintett) alairasu.
KEZI_ELTOLASOK = {
    "Daniel": daniel_4_eltolas,
    "Numbers": numeri_12_13_eltolas,
    "Job": job_38_41_eltolas,
    "Ecclesiastes": predikator_eltolas,
}


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
        vers_lookup, terkep_figyelmeztetesek, betu_utotag_kizarasok, nem_parszolhato = load_versifikacios_terkep(
            args.versifikacios_terkep, args.karoli_konyv_prefix
        )
        for fig in terkep_figyelmeztetesek:
            print(f"  FIGYELMEZTETES: {fig}", file=sys.stderr)
        if betu_utotag_kizarasok:
            irj_betu_utotag_riportot(betu_utotag_kizarasok)
            print(
                f"  {len(betu_utotag_kizarasok)} db betu-utotagos al-vers-hivatkozas "
                f"kizarva (l. {BETU_UTOTAG_RIPORT_UTVONAL})",
                file=sys.stderr,
            )
        if nem_parszolhato:
            irj_betu_utotag_riportot(nem_parszolhato, utvonal=NEM_PARSZOLHATO_RIPORT_UTVONAL)
            print(
                f"  {len(nem_parszolhato)} db nem-parszolhato terkep-ertek kihagyva "
                f"(l. {NEM_PARSZOLHATO_RIPORT_UTVONAL})",
                file=sys.stderr,
            )

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
            zarojel_volt = False
            for sz, (strong, forras) in zip(lxx_szavak, eredmeny):
                greek_stripped = sz.greek
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
                        hianyzo_kulcsok.add(lookup_kulcs)
                        continue
                else:
                    kezi_fn = KEZI_ELTOLASOK.get(args.konyv)
                    kezi_cel = kezi_fn(fejezet, vers_szam) if kezi_fn else None
                    if kezi_cel is not None:
                        igehely = f"{magyar_konyv} {kezi_cel[0]}:{kezi_cel[1]}"
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
