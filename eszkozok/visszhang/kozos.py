#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kozos.py -- a visszhang-reteg (F176, FELADATOK #176) import-szkriptjeinek kozos segedkodja.

Nem csinal semmit onmagaban; a targum_import.py, vulgata_import.py, sblgnt_import.py,
tagnt_valtozatok.py es bdb_rokon.py hasznalja. TSV-olvasas/iras: split('\\t') / '\\t'.join(),
a csv modul NEM hasznalhato (CLAUDE.md).

Futtatas: a letoltott nyers adatot olvaso szkriptek `python -I`-vel futnak; a nyers adat konyvtara
CLI-argumentum, a szkript sajat konyvtara a repo (eszkozok/visszhang/), a letoltesi konyvtaron kivul.
"""
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NORMALIZALO = os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
KAROLI = os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv')

# angol konyvnev (Sefaria) -> STEP/USFM-rovidites a Konyv_normalizalo_tabla.tsv elso oszlopa szerint
ANGOL_STEP = {
    'Genesis': 'Gen', 'Exodus': 'Exo', 'Leviticus': 'Lev', 'Numbers': 'Num', 'Deuteronomy': 'Deu',
    'Joshua': 'Jos', 'Judges': 'Jdg', 'I Samuel': '1Sa', 'II Samuel': '2Sa', 'I Kings': '1Ki', 'II Kings': '2Ki',
    'Isaiah': 'Isa', 'Jeremiah': 'Jer', 'Ezekiel': 'Ezk', 'Hosea': 'Hos', 'Joel': 'Jol', 'Amos': 'Amo',
    'Obadiah': 'Oba', 'Jonah': 'Jon', 'Micah': 'Mic', 'Nahum': 'Nam', 'Habakkuk': 'Hab', 'Zephaniah': 'Zep',
    'Haggai': 'Hag', 'Zechariah': 'Zec', 'Malachi': 'Mal',
}


# --- számozás-átvezetés (F239 U4b): görög (LXX) és latin (Vulgata) igehely -> Károli-kulcs ---------------------------
# A Károli zsoltárszámozása a héberé (a feliratot is versnek számolja; konkordancia/LXX_versificacios_terkep.tsv:
# Karoli_egyezik_hol = Heber). A görög és a latin zsoltárszámozás egymással azonos; a versszám a kettéosztott és az
# összevont zsoltárok kivételével változatlan. A teszt a térkép minden zsoltársorával összeveti (teszt_visszhang.py).
def lxx_zsoltar(fejezet, vers):
    """(f, v) görög/latin zsoltárhely -> (f, v) Károli (héber) zsoltárhely; None, ha nincs héber párja (151.)."""
    f, v = int(fejezet), int(vers)
    if f <= 8 or 148 <= f <= 150:
        return f, v
    if f == 9:
        return (9, v) if v <= 21 else (10, v - 21)       # LXX 9:22–39 = héber 10:1–18
    if 10 <= f <= 112:
        return f + 1, v
    if f == 113:
        return (114, v) if v <= 8 else (115, v - 8)      # LXX 113:1–8 = 114; 113:9–26 = 115:1–18
    if f == 114:
        return 116, v                                    # LXX 114:1–9 = 116:1–9
    if f == 115:
        return 116, v + 9                                # LXX 115:1–10 = 116:10–19
    if 116 <= f <= 145:
        return f + 1, v
    if f == 146:
        return 147, v                                    # LXX 146:1–11 = 147:1–11
    if f == 147:
        return 147, v + 11                               # LXX 147:1–9 = 147:12–20
    return None


# A Vulgata Jób-fejezethatára a 38–41. fejezetben eltér a Károliétól (a Károli 39:1 = Vulgata 38:39; Károli 41:1 =
# Vulgata 40:20); a párok a konkordancia/Karoli_versmegfeleltetes.tsv Károli→KJV/MT soraival egyeznek.
VULGATA_JOB = [  # (Vulgata fejezet, első vers, utolsó vers) -> (Károli fejezet, eltolás)
    ((38, 39, 41), (39, -38)),
    ((39, 1, 35), (39, 3)),
    ((40, 1, 19), (40, 0)),
    ((40, 20, 28), (41, -19)),
    ((41, 1, 25), (41, 9)),
]


TERKEP = os.path.join(GYOKER, 'konkordancia', 'LXX_versificacios_terkep.tsv')
_VULG_ZS = None


def vulgata_zsoltar_kivetelek():
    """{(f, v): (F, V) vagy None}: a latin zsoltárok saját versfelosztása (a Vulgata 10:1–2 = héber 11:1; a 43:22 két
    héber vers része) a térkép (TVTMS) soraiból. Tartomány („10:1-2”) egy héber versre: mindegyik latin vers oda
    (a szöveg összefűződik); fél vers („43:22a”, „2:12a”): nincs tiszta párja, kimarad (None)."""
    global _VULG_ZS
    if _VULG_ZS is None:
        _VULG_ZS, sima, fel = {}, {}, set()
        for d in olvas_tsv(TERKEP)[1]:
            lat = re.match(r'^Psa\.(\d+):(\d+)(?:-(\d+))?([ab])?$', d.get('Latin_vers', ''))
            heb = re.match(r'^Psa\.(\d+):(\d+)([ab])?$', d.get('Heber_vers', ''))
            if not (lat and heb):
                continue
            f, v1 = int(lat.group(1)), int(lat.group(2))
            v2 = int(lat.group(3)) if lat.group(3) else v1
            cel = None if (lat.group(4) or heb.group(3)) else (int(heb.group(1)), int(heb.group(2)))
            for v in range(v1, v2 + 1):
                if cel is None:
                    fel.add((f, v))
                else:
                    sima[(f, v)] = cel
        # a tiszta pár elsőbb (a 12:6 tiszta sora és fél-vers sora is áll)
        for k in fel - set(sima):
            _VULG_ZS[k] = None
        for k, cel in sima.items():
            if lxx_zsoltar(*k) != cel:
                _VULG_ZS[k] = cel
    return _VULG_ZS


def vulgata_karoli(konyv, fejezet, vers):
    """A Vulgata (Clementina) igehelye a Károli-kulcson: (könyv, f, v) -> (könyv, f, v) vagy None (nincs párja).
    A zsoltárok és a Jób 38–41 átvezetve; a többi könyv számozása itt azonosnak vett."""
    f, v = int(fejezet), int(vers)
    if konyv == 'Zsolt':
        kiv = vulgata_zsoltar_kivetelek()
        p = kiv[(f, v)] if (f, v) in kiv else lxx_zsoltar(f, v)
        return ('Zsolt',) + p if p else None
    if konyv == 'Jób':
        for (vf, tol, ig), (kf, elt) in VULGATA_JOB:
            if f == vf and tol <= v <= ig:
                return 'Jób', kf, v + elt
    return konyv, f, v


def normalizalo():
    """-> ({STEP: magyar_rovidites}, [STEP sorrendben])"""
    with open(NORMALIZALO, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    m, sorrend = {}, []
    for s in sorok[1:]:
        if not s.strip():
            continue
        o = s.split('\t')
        m[o[0]] = o[1]
        sorrend.append(o[0])
    if len(m) != 66:
        raise SystemExit('a normalizalo tabla nem 66 konyvet ad: %d' % len(m))
    return m, sorrend


def karoli_kulcsok():
    """A Karoli_1908.tsv igehely-kulcsainak halmaza (a 'vers van-e a Karoliban' diagnosztikahoz)."""
    ki = set()
    with open(KAROLI, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    fej = sorok[0].split('\t')
    i = fej.index('Igehely') if 'Igehely' in fej else 0
    for s in sorok[1:]:
        if s.strip():
            ki.add(s.split('\t')[i])
    return ki


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for blokk in iter(lambda: f.read(1 << 20), b''):
            h.update(blokk)
    return h.hexdigest()


def ts():
    return datetime.date.today().isoformat()


def ir_tsv(ut, fejlec_sorok, oszlopok, sorok):
    """Kimenet: `# ...` fejlecsorok, oszlopfejlec, adatsorok. Cellaban tab/sortores nem lehet."""
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for s in fejlec_sorok:
            f.write('# ' + s + '\n')
        f.write('\t'.join(oszlopok) + '\n')
        for r in sorok:
            if len(r) != len(oszlopok):
                raise SystemExit('oszlopszam-hiba: %r' % (r,))
            for c in r:
                if '\t' in c or '\n' in c or '\r' in c:
                    raise SystemExit('tab/sortores a cellaban: %r' % (c[:60],))
            f.write('\t'.join(r) + '\n')


def olvas_tsv(ut):
    """-> (fejlec, [dict]); a `#` sorok kihagyva. split('\\t'), csv nelkul."""
    with open(ut, encoding='utf-8') as f:
        sorok = [s for s in f.read().split('\n') if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ki = []
    for s in sorok[1:]:
        m = s.split('\t')
        ki.append(dict(zip(fej, m + [''] * (len(fej) - len(m)))))
    return fej, ki
