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
