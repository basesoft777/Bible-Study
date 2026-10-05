"""LXX-kivonat: lxx-morph (szöveg+morf+lemma) + GreekWordList (Strong), Károli-
igehely a meglévő LXX_versificacios_terkep.tsv + KEZI_ELTOLASOK segítségével.

A bulk Open Scriptorium SQLite csak ellenőrzésre szolgál (szószám/szóalak
egyezés versenként) — a repóba nem kerül. Élő API-hívás nincs.
Lásd LEXV2_1_BRIEF.md V1.3 (G4/G5, v3).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import unicodedata
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "eszkozok"))


KONKORDANCIA_DIR = os.path.join(REPO_ROOT, "konkordancia")
LXX_OS_DIR = os.path.join(KONKORDANCIA_DIR, "LXX_OS")

LXX_MORPH_COMMIT = "c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2"
LXX_MORPH_RAW = f"https://raw.githubusercontent.com/OpenScriptorium/lxx-morph/{LXX_MORPH_COMMIT}/"
GREEKWORDLIST_COMMIT = "dd5a2fd530ab3c6b748c174cec38966c356d8111"
GREEKWORDLIST_RAW = f"https://raw.githubusercontent.com/openscriptures/GreekResources/{GREEKWORDLIST_COMMIT}/"
SQLITE_URL = "https://openscriptorium.org/downloads/openscriptorium.sqlite3"

# slug -> (cím, book_key, testamentum) — az lxx-morph db/seeds/lxx_morph/<slug>.json
# fájlnevei és az Open Scriptorium /api/v1/works/rahlfs-lxx könyvlistája szerint.
BOOKS = {
    "genesis": ("Genesis", "genesis", "ot"),
    "exodus": ("Exodus", "exodus", "ot"),
    "leviticus": ("Leviticus", "leviticus", "ot"),
    "numbers": ("Numbers", "numbers", "ot"),
    "deuteronomy": ("Deuteronomy", "deuteronomy", "ot"),
    "joshua": ("Joshua (Alexandrinus A-text)", "joshua", "ot"),
    "joshua-vaticanus-b": ("Joshua (Vaticanus B-text)", "joshua", "ot"),
    "judges": ("Judges (Alexandrinus A-text)", "judges", "ot"),
    "judges-vaticanus-b": ("Judges (Vaticanus B-text)", "judges", "ot"),
    "ruth": ("Ruth", "ruth", "ot"),
    "1-samuel": ("1 Samuel", "1-samuel", "ot"),
    "2-samuel": ("2 Samuel", "2-samuel", "ot"),
    "1-kings": ("1 Kings", "1-kings", "ot"),
    "2-kings": ("2 Kings", "2-kings", "ot"),
    "1-chronicles": ("1 Chronicles", "1-chronicles", "ot"),
    "2-chronicles": ("2 Chronicles", "2-chronicles", "ot"),
    "job-lxx": ("Job (LXX)", "job", "ot"),
    "psalms-lxx": ("Psalms (LXX)", "psalms", "ot"),
    "proverbs": ("Proverbs", "proverbs", "ot"),
    "ecclesiastes": ("Ecclesiastes", "ecclesiastes", "ot"),
    "song-of-solomon": ("Song of Solomon", "song-of-solomon", "ot"),
    "isaiah": ("Isaiah", "isaiah", "ot"),
    "jeremiah-lxx": ("Jeremiah (LXX)", "jeremiah", "ot"),
    "lamentations": ("Lamentations", "lamentations", "ot"),
    "ezekiel": ("Ezekiel", "ezekiel", "ot"),
    "daniel": ("Daniel", "daniel", "ot"),
    "daniel-theodotion": ("Daniel (Theodotion)", "daniel", "deuterocanon"),
    "hosea": ("Hosea", "hosea", "ot"),
    "joel": ("Joel", "joel", "ot"),
    "amos": ("Amos", "amos", "ot"),
    "obadiah": ("Obadiah", "obadiah", "ot"),
    "jonah": ("Jonah", "jonah", "ot"),
    "micah": ("Micah", "micah", "ot"),
    "nahum": ("Nahum", "nahum", "ot"),
    "habakkuk": ("Habakkuk", "habakkuk", "ot"),
    "zephaniah": ("Zephaniah", "zephaniah", "ot"),
    "haggai": ("Haggai", "haggai", "ot"),
    "zechariah": ("Zechariah", "zechariah", "ot"),
    "malachi": ("Malachi", "malachi", "ot"),
    "tobit": ("Tobit", "tobit", "deuterocanon"),
    "tobit-sinaiticus": ("Tobit (Sinaiticus recension)", "tobit", "deuterocanon"),
    "judith": ("Judith", "judith", "deuterocanon"),
    "esther-greek": ("Esther (Greek)", "esther-greek", "deuterocanon"),
    "wisdom": ("Wisdom of Solomon", "wisdom", "deuterocanon"),
    "sirach": ("Sirach (Ecclesiasticus)", "sirach", "deuterocanon"),
    "baruch": ("Baruch", "baruch", "deuterocanon"),
    "letter-of-jeremiah": ("Letter of Jeremiah", "letter-of-jeremiah", "deuterocanon"),
    "susanna": ("Susanna", "susanna", "deuterocanon"),
    "susanna-theodotion": ("Susanna (Theodotion)", "susanna", "deuterocanon"),
    "bel-and-the-dragon": ("Bel and the Dragon", "bel-and-the-dragon", "deuterocanon"),
    "bel-and-the-dragon-theodotion": ("Bel and the Dragon (Theodotion)", "bel-and-the-dragon", "deuterocanon"),
    "1-maccabees": ("1 Maccabees", "1-maccabees", "deuterocanon"),
    "2-maccabees": ("2 Maccabees", "2-maccabees", "deuterocanon"),
    "3-maccabees": ("3 Maccabees", "3-maccabees", "deuterocanon"),
    "4-maccabees": ("4 Maccabees", "4-maccabees", "deuterocanon"),
    "1-esdras": ("1 Esdras", "1-esdras", "deuterocanon"),
    "2-esdras": ("2 Esdras", "2-esdras", "deuterocanon"),
    "psalms-of-solomon": ("Psalms of Solomon", "psalms-of-solomon", "pseudepigrapha"),
    "odes": ("Odes", "odes", "deuterocanon"),
}

# --- KEZI_ELTOLASOK (F42 / DT-F42f: ide költözött a megszűnt lxx_kivonat_fetch_v2.py-ból) ---
# Könyv-specifikus, kézi fejezethatár-eltolás-szabályok (Dán, 4Móz, Jób, Préd): a nyers
# (angol, studybible-féle) fejezet/vers -> Károli fejezet/vers; (fejezet, vers) -> (karoli_fejezet,
# karoli_vers) vagy None. Az LXX_OS Károli-kulcs-felbontása (resolve_karoli) és a naplok/KAROLI_KK*
# szkriptek használják.

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


BOOK_KEY_TO_KAROLI = {
    "genesis": "1Móz", "exodus": "2Móz", "leviticus": "3Móz", "numbers": "4Móz",
    "deuteronomy": "5Móz", "joshua": "Józs", "judges": "Bír", "ruth": "Ruth",
    "1-samuel": "1Sám", "2-samuel": "2Sám", "1-kings": "1Kir", "2-kings": "2Kir",
    "1-chronicles": "1Krón", "2-chronicles": "2Krón", "job": "Jób", "psalms": "Zsolt",
    "proverbs": "Péld", "ecclesiastes": "Préd", "song-of-solomon": "Én", "isaiah": "Ézs",
    "jeremiah": "Jer", "lamentations": "Sir", "ezekiel": "Ez", "daniel": "Dán",
    "hosea": "Hós", "joel": "Jóel", "amos": "Ámós", "obadiah": "Abd", "jonah": "Jón",
    "micah": "Mik", "nahum": "Náh", "habakkuk": "Hab", "zephaniah": "Sof",
    "haggai": "Hag", "zechariah": "Zak", "malachi": "Mal",
}
KAROLI_TO_ENGLISH_FOR_KEZI = {
    "4Móz": "Numbers", "Jób": "Job", "Préd": "Ecclesiastes", "Dán": "Daniel",
}

# --- F42 / DT-F42f (f2): elsődleges szövegváltozat Károli-könyvenként ----------------------
# Ahol az LXX_OS több fájlban ad Károli-kulcsos verset ugyanahhoz a Károli-könyvhöz
# (szövegváltozatok), az olvasók (lekerdez.py lxx-hid, lexikon_general, lxx_bridge_egyezes,
# lxx_osszevetes) ezt az elsődleges fájlt használják; a másik változat a konkordancia/LXX_OS/-ben
# megmarad. Józs: Vaticanus (B, 616 Károli-kulcsos vers; a joshua.tsv-ben 95), Bír: judges (618;
# a Vaticanus-B 617), Dán: Theodotion (327; az Old Greek 308). A 2 Esdras (Ezsd, Neh) és a görög
# Eszter a f1 besorolás (karoli_esdras_eszter) szerint.
ELSODLEGES_SLUG = {
    "Józs": "joshua-vaticanus-b",
    "Bír": "judges",
    "Dán": "daniel-theodotion",
    "Ezsd": "2-esdras",
    "Neh": "2-esdras",
    "Eszt": "esther-greek",
}


def elsodleges_slug(karoli_konyv):
    """Károli-könyv (pl. 'Zsolt') -> a LXX_OS-fájl slugja (pl. 'psalms-lxx'), vagy None."""
    if karoli_konyv in ELSODLEGES_SLUG:
        return ELSODLEGES_SLUG[karoli_konyv]
    talalt = None
    for slug, (_cim, book_key, _test) in BOOKS.items():
        if BOOK_KEY_TO_KAROLI.get(book_key) == karoli_konyv:
            if slug == book_key:
                return slug
            talalt = talalt or slug
    return talalt


VERS_REF_RE = re.compile(r'^(\d+):(\d+)$')


# --- F42 / DT-F42f (f1): 2 Esdras és a görög Eszter Károli-besorolása -----------------------
# A 2 Esdras 1-10 = Ezsd, 11-23 = Neh (fejezet - 10); a görög Eszter héber szövegű versei = Eszt.
# A Károli-kulcs a `Karoli_versmegfeleltetes.tsv` (igehely_karoli <-> igehely_kjv) és a sor
# `igehely_kjv` oszlopa szerint; az Eszter-betoldások (nincs KJV-megfelelő) és az 1 Esdras kulcs
# nélkül maradnak. A `karoli_ok` értéke itt `versmegfeleltetes_tabla`.
ESDRAS_ESZTER_SLUGOK = ("2-esdras", "esther-greek")
VERSMEGFELELTETES_TSV = os.path.join(KONKORDANCIA_DIR, "Karoli_versmegfeleltetes.tsv")
_KJV_KAROLI_CACHE = None


def load_kjv_karoli_index():
    """(Károli-könyv, 'fejezet:vers' KJV-alakban) -> [igehely_karoli, ...]; csak Ezsd/Neh/Eszt."""
    global _KJV_KAROLI_CACHE
    if _KJV_KAROLI_CACHE is not None:
        return _KJV_KAROLI_CACHE
    idx = {}
    with open(VERSMEGFELELTETES_TSV, encoding="utf-8") as f:
        for sor in f:
            sor = sor.rstrip("\r\n")
            if not sor or sor.startswith("#") or sor.startswith("igehely_karoli\t"):
                continue
            p = sor.split("\t")
            konyv = p[0].split(" ")[0]
            if konyv in ("Ezsd", "Neh", "Eszt"):
                idx.setdefault((konyv, p[1]), []).append(p[0])
    _KJV_KAROLI_CACHE = idx
    return idx


def karoli_esdras_eszter(slug, fejezet, igehely_kjv):
    """-> (igehely_karoli, karoli_ok) a 2 Esdras / görög Eszter egy versére."""
    if not igehely_kjv:
        return "", "nincs_mt_parositas"
    m = VERS_REF_RE.match(igehely_kjv)
    if not m:
        return "", "szamozas_elteres"
    kjv_fej = int(m.group(1))
    if slug == "2-esdras":
        if 1 <= fejezet <= 10:
            konyv, varhato = "Ezsd", fejezet
        elif 11 <= fejezet <= 23:
            konyv, varhato = "Neh", fejezet - 10
        else:
            return "", "szamozas_elteres"
        # A KJV-hivatkozás a mérvadó: a fejezethatár-eltolódásnál (pl. 2 Esdras 13:33-37 =
        # KJV Neh 4:1-5, 20:1 = Neh 9:38) a kjv_fej a `varhato` fejezet szomszédja (±1).
        if kjv_fej not in (varhato - 1, varhato, varhato + 1):
            return "", "szamozas_elteres"
    elif slug == "esther-greek":
        konyv = "Eszt"
    else:
        raise ValueError(slug)
    talalat = load_kjv_karoli_index().get((konyv, igehely_kjv), [])
    if len(talalat) != 1:
        return "", "szamozas_elteres"
    return talalat[0], "versmegfeleltetes_tabla"


def ujrabesorol_esdras_eszter():
    """Offline újrabesorolás (nincs letöltés): a már generált 2-esdras.tsv és esther-greek.tsv
    igehely_karoli / karoli_ok oszlopát a karoli_esdras_eszter() szerint írja újra az
    igehely_kjv oszlopból. Ugyanaz a függvény, mint a process_book()-ban."""
    jelentes = {}
    for slug in ESDRAS_ESZTER_SLUGOK:
        ut = os.path.join(LXX_OS_DIR, f"{slug}.tsv")
        komment, fejlec, sorok = [], None, []
        with open(ut, encoding="utf-8") as f:
            for sor in f:
                sor = sor.rstrip("\r\n")
                if sor.startswith("#"):
                    komment.append(sor)
                elif fejlec is None:
                    fejlec = sor
                else:
                    sorok.append(sor.split("\t"))
        assert fejlec.split("\t") == LXX_OS_HEADER, fejlec
        jegyzet = ("# F42 (DT-F42f f1): az igehely_karoli / karoli_ok oszlop a `python eszkozok/lxx_os_import.py "
                   "--ujrabesorol` szerint újrabesorolva (Karoli_versmegfeleltetes.tsv + igehely_kjv), ts="
                   + __import__("datetime").date.today().isoformat())
        komment = [k for k in komment if not k.startswith("# F42 (DT-F42f f1)")] + [jegyzet]
        kulcsolt, osszes = set(), set()
        for p in sorok:
            m = re.search(r"(\d+):(\d+)$", p[0])
            fej = int(m.group(1))
            karoli, ok = karoli_esdras_eszter(slug, fej, p[1])
            p[2], p[3] = karoli, ok
            osszes.add(p[0])
            if karoli:
                kulcsolt.add(karoli)
        with open(ut, "w", encoding="utf-8", newline="\n") as f:
            for k in komment:
                f.write(k + "\n")
            f.write(fejlec + "\n")
            for p in sorok:
                f.write("\t".join(p) + "\n")
        jelentes[slug] = (len(osszes), sorted(kulcsolt))
    return jelentes
EM_DASH = "—"

LXX_OS_HEADER = [
    "igehely_lxx", "igehely_kjv", "igehely_karoli", "karoli_ok", "pozicio",
    "szoalak", "normalizalt", "lemma", "morf", "strong", "strong_ok",
    "proveniencia",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_accents(s):
    decomposed = unicodedata.normalize("NFD", s)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn").lower()


def download(url, dest):
    urllib.request.urlretrieve(url, dest)
    return dest


def letolt_forrasok(cache_dir):
    os.makedirs(cache_dir, exist_ok=True)
    morph_dir = os.path.join(cache_dir, "lxx_morph")
    os.makedirs(morph_dir, exist_ok=True)
    for slug in BOOKS:
        dest = os.path.join(morph_dir, f"{slug}.json")
        if not os.path.isfile(dest):
            print(f"  letoltes: {slug}.json", file=sys.stderr)
            download(LXX_MORPH_RAW + f"db/seeds/lxx_morph/{slug}.json", dest)
    verse_pairs_dest = os.path.join(cache_dir, "verse_pairs.jsonl")
    if not os.path.isfile(verse_pairs_dest):
        print("  letoltes: verse_pairs.jsonl", file=sys.stderr)
        download(LXX_MORPH_RAW + "db/seeds/mt_alignment/verse_pairs.jsonl", verse_pairs_dest)
    gwl_dest = os.path.join(cache_dir, "GreekWordList.js")
    if not os.path.isfile(gwl_dest):
        print("  letoltes: GreekWordList.js", file=sys.stderr)
        download(GREEKWORDLIST_RAW + "GreekWordList.js", gwl_dest)
    return cache_dir


def letolt_sqlite(cache_dir):
    dest = os.path.join(cache_dir, "openscriptorium.sqlite3")
    if not os.path.isfile(dest):
        print("  letoltes: openscriptorium.sqlite3 (ellenorzeshez, ~339 MB)", file=sys.stderr)
        download(SQLITE_URL, dest)
    return dest


def load_greek_word_list(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    content = content.split("=", 1)[1].strip()
    if content.endswith(";"):
        content = content[:-1]
    return json.loads(content)


def load_verse_pairs(path):
    """grk_book -> {grk_ref: (mt_book, mt_refs, method)}"""
    idx = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            idx.setdefault(d["grk_book"], {})[d["grk_ref"]] = (
                d.get("mt_book"), d.get("mt_refs") or [], d.get("method")
            )
    return idx


KAROLI_MAX_CACHE = None
KJV_MAX_CACHE = None


def load_karoli_max():
    """(Karoli_konyv, fejezet) -> legmagasabb versszam, a Karoli_1908.tsv-bol."""
    global KAROLI_MAX_CACHE
    if KAROLI_MAX_CACHE is not None:
        return KAROLI_MAX_CACHE
    idx = {}
    path = os.path.join(KONKORDANCIA_DIR, "Karoli_1908.tsv")
    with open(path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            m = re.match(r'^(\S+)\s+(\d+):(\d+)$', parts[0])
            if not m:
                continue
            book, ch, v = m.groups()
            key = (book, int(ch))
            idx[key] = max(idx.get(key, 0), int(v))
    KAROLI_MAX_CACHE = idx
    return idx


def load_kjv_max(verse_pairs_path):
    """(mt_book, fejezet) -> legmagasabb KJV-versszam, a verse_pairs.jsonl-bol."""
    global KJV_MAX_CACHE
    if KJV_MAX_CACHE is not None:
        return KJV_MAX_CACHE
    idx = {}
    with open(verse_pairs_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            mt_book = d.get("mt_book")
            if not mt_book:
                continue
            for ref in d.get("mt_refs") or []:
                m = VERS_REF_RE.match(ref)
                if not m:
                    continue
                ch, v = m.groups()
                key = (mt_book, int(ch))
                idx[key] = max(idx.get(key, 0), int(v))
    KJV_MAX_CACHE = idx
    return idx


MT_MAX_CACHE = None


def load_mt_max():
    """(Karoli_konyv, fejezet) -> legmagasabb MT/heber-versszam, a
    TAHOT_kivonat.tsv-bol (KK1/KK1b H2-javitas: a Karoli sok fejezetben
    ezt koveti, nem a KJV-t)."""
    global MT_MAX_CACHE
    if MT_MAX_CACHE is not None:
        return MT_MAX_CACHE
    idx = {}
    path = os.path.join(KONKORDANCIA_DIR, "TAHOT_kivonat.tsv")
    with open(path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0]:
                continue
            m = re.match(r"^(\S+) (\d+):(\d+)$", parts[0])
            if not m:
                continue
            book, ch, v = m.group(1), int(m.group(2)), int(m.group(3))
            key = (book, ch)
            idx[key] = max(idx.get(key, 0), v)
    MT_MAX_CACHE = idx
    return idx


FEJEZET_DONTES_CACHE = None


def load_fejezet_dontes():
    """(Karoli_konyv, fejezet) -> (dontes, elfogadott_eltolas) a
    konkordancia/LXX_OS/karoli_fejezet_dontes.tsv-bol (KAROLI_KULCS_KK7_BRIEF.md
    KK7.1, athelyezve a KAROLI_KULCS_KK75_BRIEF.md G2 szerint -- az importer
    eles bemenete nem a naplok/ alatt van, l. K3). Csak azokra a fejezetekre
    vonatkozik, amelyekben a KK4-KK6 UJONNAN toltott ki kulcsokat (a regi,
    mar korabban is kitoltott sorokat sosem erinti -- l. resolve_karoli
    hasznalati helyei). Ha a tabla hianyzik, minden fejezet "nincs adat" --
    ez visszaall a KK6-os (nem korrigalt) viselkedesre."""
    global FEJEZET_DONTES_CACHE
    if FEJEZET_DONTES_CACHE is not None:
        return FEJEZET_DONTES_CACHE
    idx = {}
    path = os.path.join(LXX_OS_DIR, "karoli_fejezet_dontes.tsv")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or line.startswith("karoli_konyv"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 12:
                    continue
                karoli_konyv, fejezet = parts[0], int(parts[1])
                dontes, elfogadott_eltolas = parts[9], int(parts[11])
                idx[(karoli_konyv, fejezet)] = (dontes, elfogadott_eltolas)
    FEJEZET_DONTES_CACHE = idx
    return idx


VERS_FELULBIRALAS_CACHE = None


def load_vers_felulbiralas():
    """(book_key, nyers_fejezet, nyers_vers) -> igehely_karoli, a
    konkordancia/LXX_OS/karoli_vers_felulbiralas.tsv-bol (KAROLI_KULCS_KK75_BRIEF.md
    KK7.5.2, G1). Ez a legelso lepes a resolve_karoli-ban -- meg a
    KEZI_ELTOLASOK es a fejezetdontes-tabla elott -- mert versszintu,
    fejezethatart atlepo kivetel, amit sem a fejezet-szintu dontes, sem a
    konyv-szintu kezi_fn nem tud helyesen kezelni (l. KK7.5.1 hatarkereses:
    1Sam 20:42/21:1)."""
    global VERS_FELULBIRALAS_CACHE
    if VERS_FELULBIRALAS_CACHE is not None:
        return VERS_FELULBIRALAS_CACHE
    idx = {}
    path = os.path.join(LXX_OS_DIR, "karoli_vers_felulbiralas.tsv")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or line.startswith("book_key"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 4:
                    continue
                book_key, fejezet, vers, igehely_karoli = parts[0], int(parts[1]), int(parts[2]), parts[3]
                idx[(book_key, fejezet, vers)] = igehely_karoli
    VERS_FELULBIRALAS_CACHE = idx
    return idx


def build_dup_kjv_terkep(vp_for_book):
    """(kjv_fejezet, kjv_vers) -> (a legmagasabb (fejezet,vers) grk_ref, ami
    ráhivatkozik, hány grk_ref hivatkozik ráhivatkozik osszesen). Ha egy
    KJV-célra TÖBB LXX-forrás is mutat (Zsoltár-felirat, ami a LXX-ben több
    sorra bomlik, de a KJV nem számozza külön), csak a LEGMAGASABB (utolsó,
    a tartalmi folytatáshoz tartozó) LXX-forrás tekinthető felbonthatónak —
    a korábbi(ak) a felirat része, KJV-megfelelő nélkül (l. LEXV2_1_BRIEF.md
    V1.3a "ellenpróba"). A darabszám kell ahhoz, hogy a KK4-es általános
    MT-ág (l. resolve_karoli) meg tudja különböztetni a valódi (1:1,
    nem-ambiguus) eseteket a ténylegesen többes hivatkozásoktól — enélkül
    minden sima 1:1 eset is tévesen "nem a legmagasabb forrás"-ként bukna
    el (l. KK6 F5 regresszió, 983 hibás Zsoltár-sor)."""
    max_forras = {}
    darab = {}
    for grk_ref, (mt_book, mt_refs, method) in vp_for_book.items():
        if method == "unpaired" or len(mt_refs) != 1:
            continue
        m = VERS_REF_RE.match(mt_refs[0])
        gm = VERS_REF_RE.match(grk_ref)
        if not m or not gm:
            continue
        key = (int(m.group(1)), int(m.group(2)))
        grk_key = (int(gm.group(1)), int(gm.group(2)))
        darab[key] = darab.get(key, 0) + 1
        if key not in max_forras or grk_key > max_forras[key]:
            max_forras[key] = grk_key
    return {key: (grk_key, darab[key]) for key, grk_key in max_forras.items()}


def resolve_karoli(karoli_book, book_key, fejezet, vers, mt_refs, method, kezi_fn,
                    karoli_max_idx, kjv_max_idx, dup_kjv_terkep,
                    mt_max_idx=None, kezi_aktiv_fejezetek=None):
    """V1.3b (F01_KAROLI_KULCS_BRIEF.md KK4, G4). Két javítás a régi (V1.3a)
    algoritmushoz képest, a KK1/KK1b-menet által feltárt H1/H2 okokra:

    (1) H1 javítás — a `KEZI_ELTOLASOK`-függvény `None`-ja a ténylegesen
    érintett (legalább egy explicit eltolást tartalmazó) fejezetben
    **identitást** jelent, nem "nem az én dolgom"-ot — de csak akkor, ha
    az eredmény egy valóban létező Károli-vers (a `karoli_max_idx`
    korlátozza — l. KK6 F5 regresszió: enélkül a Jób 40:25–32 hibásan
    identitást kapott volna a 41. fejezetbe tartozó vers helyett,
    mert a `job_38_41_eltolas` csak a 40:1–24 tartományt kezeli explicit
    módon, a 25+ már a 41. fejezetbe tartozik és a régi fejezet-szintű
    őrnek kell megoldania).

    (2) H2 javítás — ha a Károli egy fejezetben a héber/MT-számozást
    követi (nem a KJV-t: `karoli_max_idx == mt_max_idx`, de
    `!= kjv_max_idx`), a Zsoltár-cím-eltolásnál már bevált `d`-eltolásos
    képlet (`Károli-vers = KJV-vers + d`) **általánosan** alkalmazandó,
    nem csak a Zsoltárokra és nem csak `d∈{1,2}`-re. **Fontos:** ez NEM
    a `konkordancia/Karoli_versmegfeleltetes.tsv` KJV-oldali
    visszakeresésén (reverse lookup) alapul — az első implementáció ezt
    próbálta, de az F5 regressziós ellenőrzés 983 hibás Zsoltár-sort
    talált (a `verse_pairs.jsonl` `mt_refs` mezője már KJV-számozású,
    nem valódi MT-számozású, ezért a tábla visszakeresése a cím-eltolásos
    fejezetekben szisztematikusan rossz célt adott — l. `naplok/KAROLI_KK6_regresszio.tsv`
    és a KK6 jelentés "F5" szakasza). A javított, közvetlen `d`-képlet
    ugyanazt az eredményt adja, mint amit a tábla helyesen KÉNE hogy
    adjon, de nem függ egy hibásan felépíthető visszakereső indextől.

    A régi fejezet-szintű versszám-egyezés (d==0) és a régi, szűkebb
    Zsoltár-cím-eltolás-ág (csak biztonsági tartalékként, gyakorlatilag
    sosem aktiválódik, mert az új, általános MT-ág korábban lefedi)
    megmarad. A `F01_KAROLI_KULCS_BRIEF.md` F3 szerint az `EGYIK_SEM`-osztályú
    fejezetek (nincs sem KJV-, sem MT-, sem KEZI-egyezés) szándékosan
    `szamozas_elteres` maradnak. A régi `LXX_versificacios_terkep.tsv`-t
    (studybible.info-számozásra épült) ez a menet NEM használja (l.
    LEXV2_1_BRIEF.md döntésnapló v4)."""
    mt_max_idx = mt_max_idx or {}
    kezi_aktiv_fejezetek = kezi_aktiv_fejezetek or set()
    fejezet_dontes = load_fejezet_dontes()

    # KAROLI_KULCS_KK75_BRIEF.md KK7.5.2, G1: versszintu felulbiralas,
    # MEG a fejezetdontes es a KEZI_ELTOLASOK elott -- fejezethatart
    # atlepo, egyedi esetekre (l. KK7.5.1 hatarkereses: 1Sam 20:42/21:1),
    # amit sem a fejezet-szintu dontes, sem a konyv-szintu kezi_fn nem
    # tud helyesen kezelni.
    felulbiralas = load_vers_felulbiralas().get((book_key, fejezet, vers))
    if felulbiralas is not None:
        return felulbiralas, "kezi_eltolas_tabla"

    if kezi_fn:
        cel = kezi_fn(fejezet, vers)
        if cel is not None:
            return f"{karoli_book} {cel[0]}:{cel[1]}", "kezi_eltolas_tabla"
        if fejezet in kezi_aktiv_fejezetek:
            # KK1 H1: a fuggveny None-ja itt "nincs eltolas ezen a versen"-t
            # jelent, nem "kivul esik a hataskoromon" -- korabban a kod
            # tevesen a lenti fejezet-szintu orre esett vissza, es emiatt a
            # teljes fejezetet szamozas_elteres-kent vesztette el. DE csak
            # akkor fogadjuk el, ha valoban letezik ilyen Karoli-vers (F5
            # regresszio, Job 40:25-32 mintajara).
            helyi_max = karoli_max_idx.get((karoli_book, fejezet))
            if helyi_max is not None and vers <= helyi_max:
                # KK7 G1/G2: ez a KK6-ban UJONNAN keletkezo sor -- a
                # fejezetdontes-tabla ELLENORZI/KORRIGALJA, mert a KK7
                # tartalmi probaja szerint az egyenletes identitas-feltetelezes
                # nem mindig helyes (l. Job 40:25-32 mintaja, F5 regresszio,
                # es altalanosabban a KK7 tartalmi probaja).
                dontes, eltolas = fejezet_dontes.get((karoli_book, fejezet), ("nincs_adat", 0))
                if dontes == "ures":
                    return "", "szamozas_elteres"
                cel_vers = vers + eltolas
                if dontes == "elfogad" and 1 <= cel_vers <= helyi_max:
                    return f"{karoli_book} {fejezet}:{cel_vers}", "kezi_eltolas_tabla"
                if dontes == "nincs_adat":
                    return f"{karoli_book} {fejezet}:{vers}", "kezi_eltolas_tabla"
                return "", "szamozas_elteres"

    if method == "unpaired" or not mt_refs:
        return "", "nincs_mt_parositas"
    if len(mt_refs) != 1:
        return "", "szamozas_elteres"

    m = VERS_REF_RE.match(mt_refs[0])
    if not m:
        return "", "szamozas_elteres"
    kjv_ch, kjv_v = int(m.group(1)), int(m.group(2))

    karoli_max = karoli_max_idx.get((karoli_book, kjv_ch))
    kjv_max = kjv_max_idx.get((book_key, kjv_ch))
    if karoli_max is None or kjv_max is None:
        return "", "szamozas_elteres"
    d = karoli_max - kjv_max

    if d == 0:
        return f"{karoli_book} {kjv_ch}:{kjv_v}", ""

    mt_max = mt_max_idx.get((karoli_book, kjv_ch))
    if mt_max is not None and karoli_max == mt_max:
        # KK1 H2: a Karoli ebben a fejezetben az MT-szamozast koveti.
        # Ugyanaz a d-eltolasos keplet, mint a regi Zsoltar-cim-ag, de
        # barmely konyvre/fejezetre es barmely d-re altalanositva.
        bejegyzes = dup_kjv_terkep.get((kjv_ch, kjv_v))
        if bejegyzes is not None:
            legmagasabb, darab = bejegyzes
            if darab > 1 and legmagasabb != (fejezet, vers):
                # tobb LXX-forras mutat ugyanarra a KJV-celra (cim-tobbesertelmuseg);
                # csak a legmagasabb (utolso, tartalmi) forras kapja meg az eltolast
                return "", "szamozas_elteres"
        uj_vers = kjv_v + d
        if uj_vers < 1 or uj_vers > karoli_max:
            return "", "szamozas_elteres"
        # KK7 G1/G2: ez UJONNAN keletkezo sor (a regi V1.3a algoritmus ezt
        # meg nem toltotte ki) -- a fejezetdontes-tabla ellenorzi/korrigalja,
        # mert az egyenletes d-eltolas csak akkor helyes, ha a tobbletvers a
        # fejezet ELEJEN van (l. brief 0.6: pl. Ezs 63, ahol a tobblet mashol
        # van, es az egyenletes eltolas minden verset elcsusztat).
        dontes, korrekcio = fejezet_dontes.get((karoli_book, kjv_ch), ("nincs_adat", 0))
        if dontes == "ures":
            return "", "szamozas_elteres"
        vegso_vers = uj_vers + korrekcio
        if dontes == "elfogad" and 1 <= vegso_vers <= karoli_max:
            return f"{karoli_book} {kjv_ch}:{vegso_vers}", "mt_szamozas_kovetes"
        if dontes == "nincs_adat":
            return f"{karoli_book} {kjv_ch}:{uj_vers}", "mt_szamozas_kovetes"
        return "", "szamozas_elteres"

    if karoli_book == "Zsolt" and d in (1, 2):
        bejegyzes = dup_kjv_terkep.get((kjv_ch, kjv_v))
        if bejegyzes is not None:
            legmagasabb, darab = bejegyzes
            if darab > 1 and legmagasabb != (fejezet, vers):
                return "", "szamozas_elteres"
        return f"{karoli_book} {kjv_ch}:{kjv_v + d}", "zsolt_felirat_eltolas"

    return "", "szamozas_elteres"


def process_book(slug, morph_dir, verse_pairs_idx, greek_word_list, proveniencia_line, verse_pairs_path):
    title, book_key, testament = BOOKS[slug]
    karoli_book = BOOK_KEY_TO_KAROLI.get(book_key)

    kezi_fn = None
    vp_for_book = verse_pairs_idx.get(slug, {})
    dup_kjv_terkep = {}
    karoli_max_idx = {}
    kjv_max_idx = {}
    mt_max_idx = {}
    kezi_aktiv_fejezetek = set()
    if karoli_book:
        eng_name = KAROLI_TO_ENGLISH_FOR_KEZI.get(karoli_book)
        kezi_fn = KEZI_ELTOLASOK.get(eng_name) if eng_name else None
        dup_kjv_terkep = build_dup_kjv_terkep(vp_for_book)
        karoli_max_idx = load_karoli_max()
        kjv_max_idx = load_kjv_max(verse_pairs_path)
        mt_max_idx = load_mt_max()
        if kezi_fn:
            karoli_max_local = load_karoli_max()
            for (b, ch) in karoli_max_local:
                if b != karoli_book:
                    continue
                for vs in range(1, karoli_max_local[(b, ch)] + 10):
                    if kezi_fn(ch, vs) is not None:
                        kezi_aktiv_fejezetek.add(ch)
                        break

    morph_path = os.path.join(morph_dir, f"{slug}.json")
    with open(morph_path, encoding="utf-8") as f:
        verses = json.load(f)

    rows = []
    stats = {
        "karoli_ok": 0, "zsolt_felirat_eltolas": 0, "szamozas_elteres": 0,
        "nincs_mt_parositas": 0, "nincs_karoli_konyv": 0, "kezi_eltolas_tabla": 0,
        "mt_szamozas_kovetes": 0,
    }
    hiany_fejezetek = set()
    chapter_mismatch_warns = []

    for v in verses:
        ref = v["ref"]
        m = re.search(r'(\d+):(\d+)$', ref)
        if not m:
            continue
        fejezet, vers = int(m.group(1)), int(m.group(2))
        igehely_lxx = f"{title} {fejezet}:{vers}"

        mt_book, mt_refs, method = vp_for_book.get(f"{fejezet}:{vers}", (None, [], None))
        igehely_kjv = ";".join(mt_refs) if mt_refs else ""

        if slug in ESDRAS_ESZTER_SLUGOK:
            igehely_karoli, karoli_ok = karoli_esdras_eszter(
                slug, fejezet, igehely_kjv if len(mt_refs) == 1 else "")
            stats.setdefault(karoli_ok, 0)
            stats[karoli_ok] += 1
        elif not karoli_book:
            igehely_karoli, karoli_ok = "", "nincs_karoli_konyv"
            stats["nincs_karoli_konyv"] += 1
        else:
            igehely_karoli, karoli_ok = resolve_karoli(
                karoli_book, book_key, fejezet, vers, mt_refs, method, kezi_fn,
                karoli_max_idx, kjv_max_idx, dup_kjv_terkep,
                mt_max_idx, kezi_aktiv_fejezetek,
            )
            if igehely_karoli == "":
                stats[karoli_ok] += 1
                if karoli_ok == "szamozas_elteres":
                    hiany_fejezetek.add(fejezet)
            else:
                stats["karoli_ok" if karoli_ok == "" else karoli_ok] += 1
                # K6: minden kitöltött sorban a Károli-fejezet = KJV-fejezet,
                # kivéve a KEZI_ELTOLASOK dokumentált eseteit.
                karoli_fej = int(igehely_karoli.rsplit(" ", 1)[1].split(":")[0])
                if mt_refs and len(mt_refs) == 1:
                    m2 = VERS_REF_RE.match(mt_refs[0])
                    if m2 and int(m2.group(1)) != karoli_fej and kezi_fn is None:
                        chapter_mismatch_warns.append(
                            f"{igehely_lxx}: Karoli-fejezet={karoli_fej} != KJV-fejezet={m2.group(1)} (nem kezi_eltolas)"
                        )

        for pozicio, w in enumerate(v.get("words") or [], start=1):
            surface = w.get("surface", "")
            lemma = w.get("lemma", "")
            pos = w.get("pos", "")
            parsing = w.get("parsing", "")
            morf = f"{pos} {parsing}".strip()

            gwl_key = strip_accents(lemma)
            gwl_entry = greek_word_list.get(gwl_key)
            if gwl_entry is None:
                strong, strong_ok = "", "lemma_nem_talalhato"
            elif gwl_entry.get("strong"):
                strong, strong_ok = gwl_entry["strong"], ""
            else:
                strong, strong_ok = "", "nincs_uszbeli_megfelelo"

            rows.append((
                igehely_lxx, igehely_kjv, igehely_karoli, karoli_ok,
                str(pozicio), surface, strip_accents(surface), lemma, morf,
                strong, strong_ok, proveniencia_line,
            ))

    return rows, stats, sorted(hiany_fejezetek), chapter_mismatch_warns


def write_tsv(path, rows, comment_lines):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for line in comment_lines:
            f.write(line + "\n")
        f.write("\t".join(LXX_OS_HEADER) + "\n")
        for row in rows:
            f.write("\t".join(row) + "\n")


def ellenoriz_sqlite(sqlite_path, slug, verses):
    """Szószám/szóalak-sorozat egyezés versenkent az SQLite ellen. Eltéréseket
    ad vissza (nem blokkol)."""
    con = sqlite3.connect(sqlite_path)
    cur = con.cursor()
    cur.execute("select id from works where slug='rahlfs-lxx'")
    row = cur.fetchone()
    if row is None:
        return ["nincs 'rahlfs-lxx' work a SQLite-ban"]
    work_id = row[0]
    _title, book_key, _test = BOOKS[slug]
    cur.execute("""
        select cr.hierarchy, wu.body
        from work_units wu
        join canonical_refs cr on wu.canonical_ref_id = cr.id
        join canonical_works cw on cr.canonical_work_id = cw.id
        where wu.work_id=? and cw.slug=?
    """, (work_id, slug))
    sqlite_verses = {}
    for hierarchy, body in cur.fetchall():
        sqlite_verses[hierarchy.replace(",", ":")] = body
    eltekek = []
    for v in verses:
        m = re.search(r'(\d+:\d+)$', v["ref"])
        if not m:
            continue
        ref = m.group(1)
        expected_n = len(v.get("words") or [])
        body = sqlite_verses.get(ref)
        if body is None:
            eltekek.append(f"{slug} {ref}: nincs a SQLite-ban")
            continue
        actual_n = len(body.split())
        if actual_n != expected_n:
            eltekek.append(f"{slug} {ref}: szoszam elter (lxx-morph={expected_n}, sqlite={actual_n})")
    con.close()
    return eltekek


def main():
    parser = argparse.ArgumentParser(description="LXX-kivonat (lxx-morph + GreekWordList)")
    parser.add_argument("--letolt", action="store_true", help="forrasok letoltese a rogzitett commitokrol")
    parser.add_argument("--forras", metavar="KONYVTAR", help="mar letoltott forrasok konyvtara")
    parser.add_argument("--sqlite-ellenoriz", action="store_true", help="bulk SQLite letoltese es ellenorzes")
    parser.add_argument("--konyvek", help="csak ezekre a slugokra fusson (vesszovel elvalasztva)")
    parser.add_argument("--ujrabesorol", action="store_true",
                        help="offline: a 2-esdras.tsv és az esther-greek.tsv Károli-besorolásának újraírása "
                             "(F42 / DT-F42f f1), letöltés nélkül")
    args = parser.parse_args()

    if args.ujrabesorol:
        for slug, (db, kulcsolt) in ujrabesorol_esdras_eszter().items():
            print(f"  {slug}: {db} vers, ebből Károli-kulcsos: {len(kulcsolt)}", file=sys.stderr)
        return

    if args.letolt and args.forras:
        print("HIBA: --letolt es --forras kizarja egymast.", file=sys.stderr)
        sys.exit(1)
    if not args.letolt and not args.forras:
        print("HIBA: --letolt vagy --forras szukseges.", file=sys.stderr)
        sys.exit(1)

    cleanup_dir = None
    try:
        if args.letolt:
            cache_dir = tempfile.mkdtemp(prefix="lxx_os_")
            cleanup_dir = cache_dir
            letolt_forrasok(cache_dir)
        else:
            cache_dir = args.forras

        morph_dir = os.path.join(cache_dir, "lxx_morph")
        verse_pairs_idx = load_verse_pairs(os.path.join(cache_dir, "verse_pairs.jsonl"))
        greek_word_list = load_greek_word_list(os.path.join(cache_dir, "GreekWordList.js"))

        morph_sha = sha256_file(os.path.join(cache_dir, "verse_pairs.jsonl"))
        gwl_sha = sha256_file(os.path.join(cache_dir, "GreekWordList.js"))
        proveniencia_line = (
            f"forras=lxx-morph@{LXX_MORPH_COMMIT} | forras=GreekWordList@{GREEKWORDLIST_COMMIT} | "
            f"ts={__import__('datetime').date.today().isoformat()}"
        )

        os.makedirs(LXX_OS_DIR, exist_ok=True)

        slugs = list(BOOKS)
        if args.konyvek:
            slugs = [s for s in args.konyvek.split(",") if s]

        sqlite_path = None
        if args.sqlite_ellenoriz:
            sqlite_path = letolt_sqlite(cache_dir if args.letolt else args.forras)

        osszes_stat = {
            "karoli_ok": 0, "zsolt_felirat_eltolas": 0, "szamozas_elteres": 0,
            "nincs_mt_parositas": 0, "nincs_karoli_konyv": 0, "kezi_eltolas_tabla": 0,
            "mt_szamozas_kovetes": 0,
        }
        osszes_hiany = {}
        osszes_chapter_warns = []
        sqlite_eltek = []

        for slug in slugs:
            morph_path = os.path.join(morph_dir, f"{slug}.json")
            if not os.path.isfile(morph_path):
                print(f"  HIANYZIK: {morph_path}", file=sys.stderr)
                continue
            with open(morph_path, encoding="utf-8") as f:
                verses = json.load(f)
            rows, stats, hiany_fejezetek, chapter_warns = process_book(
                slug, morph_dir, verse_pairs_idx, greek_word_list, proveniencia_line,
                os.path.join(cache_dir, "verse_pairs.jsonl"),
            )
            comment = [
                "# GENERÁLT: eszkozok/lxx_os_import.py — kézzel nem szerkesztendő.",
                f"# forras: lxx-morph@{LXX_MORPH_COMMIT} (CC BY 4.0) + GreekWordList@{GREEKWORDLIST_COMMIT} (CC BY 4.0)",
                f"# sha256(verse_pairs.jsonl)={morph_sha} | sha256(GreekWordList.js)={gwl_sha}",
            ]
            write_tsv(os.path.join(LXX_OS_DIR, f"{slug}.tsv"), rows, comment)
            for k, v in stats.items():
                osszes_stat[k] += v
            if hiany_fejezetek:
                osszes_hiany[slug] = hiany_fejezetek
            osszes_chapter_warns.extend(chapter_warns)
            if sqlite_path:
                sqlite_eltek.extend(ellenoriz_sqlite(sqlite_path, slug, verses))
            print(f"  {slug}: {len(rows)} sor", file=sys.stderr)

        print("\n=== Összesítés ===", file=sys.stderr)
        for k, v in osszes_stat.items():
            print(f"  {k}: {v}", file=sys.stderr)
        if osszes_hiany:
            print("\n=== Fejezetek szamozas_elteres-szel ===", file=sys.stderr)
            for slug, chs in osszes_hiany.items():
                print(f"  {slug}: {chs}", file=sys.stderr)
        if osszes_chapter_warns:
            print(f"\n=== K6-ELLENORZES: {len(osszes_chapter_warns)} Karoli-fejezet != KJV-fejezet (nem kezi_eltolas) ===", file=sys.stderr)
            for w in osszes_chapter_warns[:50]:
                print(f"  {w}", file=sys.stderr)
        if sqlite_path:
            print(f"\n=== SQLite-ellenorzes: {len(sqlite_eltek)} elteres ===", file=sys.stderr)
            for e in sqlite_eltek[:50]:
                print(f"  {e}", file=sys.stderr)
    finally:
        if cleanup_dir:
            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
