#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nave.py -- F06 3. lepes, Nave (N27): a harom jelolt merese.
  basokant/nave, theonize/bible_database, elcafe7/lex
Meres: elerhetoseg (klon + commit), temakorszam, tema<->vers relaciok szama,
versformatum lekepezhetosege a Konyv_normalizalo_tabla.tsv-re (egyezo / nem
egyezo konyvkodok), licenc- es README-fajlok szo szerinti kigyujtese.

Kimenet: naplok/F06_nave.tsv  (forras, mero, ertek, megjegyzes -- hosszu alak)
A nyers klon a munkakonyvtarba kerul (nem commitba). Szamadat csak innen.
A kulso CSV-ket (theonize) a csv modul olvassa: ezek nem a repo tablai.
"""

import csv
import json
import os
import re
import sqlite3
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

csv.field_size_limit(10 ** 9)

JELOLTEK = [
    ('basokant_nave', 'https://github.com/basokant/nave'),
    ('theonize_bible_database', 'https://github.com/theonize/bible_database'),
    ('elcafe7_lex', 'https://github.com/elcafe7/lex'),
]


def konyv_feloldo():
    """kis-betus, szokoz/pont nelkuli nev/kod -> STEPBible-kod (pl. 'exo', 'genesis' -> 'Gen')."""
    step_mag, _ = kozos.normalizalo()
    tabla = {k.lower(): k for k in step_mag}
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Angol_konyvnev_STEPBible_tabla.tsv'))
    for s in sorok:
        tabla[re.sub(r'[\s.]', '', s[0]).lower()] = s[1]
    return tabla, list(step_mag.keys())  # a sorrend a kanoni konyvsorrend


def kulcs(token):
    return re.sub(r'[\s.]', '', token).lower()


def oszlop(fej, nevek, alap):
    kis = [h.strip().lower() for h in fej]
    for n in nevek:
        if n in kis:
            return kis.index(n)
    return alap


def megnez_theonize(gyoker, sorok, feloldo, kanoni):
    azon = 'theonize_bible_database'
    mappa = None
    for m, _, fajlok in os.walk(gyoker):
        if 'Topics.csv' in fajlok:
            mappa = m
            break
    if not mappa:
        sorok.append((azon, 'topics_csv', 'nincs', 'Topics.csv nem talalhato'))
        return

    def beolvas(nev):
        ut = os.path.join(mappa, nev)
        if not os.path.exists(ut):
            return None, iter(())
        f = open(ut, encoding='utf-8', errors='replace', newline='')
        r = csv.reader(f)
        return next(r, []), r

    fej, sor_iter = beolvas('Topics.csv')
    i_t = oszlop(fej, ['topic'], 1)
    sorok.append((azon, 'topics_fejlec', '|'.join(fej), ''))
    n = 0
    egyedi = set()
    for s in sor_iter:
        if len(s) > i_t:
            n += 1
            egyedi.add(s[i_t].strip())
    sorok.append((azon, 'topics_sorok', n, 'Topics.csv adatsorai'))
    sorok.append((azon, 'temakor_egyedi_topic', len(egyedi), 'Topics.csv Topic-oszlop egyedi ertekei'))

    # vers-azonosito feloldas: MainIndex.csv-bol vagy BBCCCVVV kodolasbol
    fej_m, iter_m = beolvas('MainIndex.csv')
    vers_terkep = {}
    if fej_m:
        sorok.append((azon, 'mainindex_fejlec', '|'.join(fej_m), ''))
        i_v = oszlop(fej_m, ['verseid', 'verse_id'], None)
        i_b = oszlop(fej_m, ['book', 'bookid', 'book_id'], None)
        if i_v is not None and i_b is not None:
            for s in iter_m:
                if len(s) > max(i_v, i_b):
                    vers_terkep.setdefault(s[i_v], s[i_b])
            sorok.append((azon, 'vers_terkep_meret', len(vers_terkep), 'MainIndex.csv egyedi VerseID-i'))
    fej_i, iter_i = beolvas('TopicIndex.csv')
    if not fej_i:
        sorok.append((azon, 'topicindex_csv', 'nincs', ''))
        return
    sorok.append((azon, 'topicindex_fejlec', '|'.join(fej_i), ''))
    i_vv = oszlop(fej_i, ['verseid', 'verse_id', 'verse'], 1)
    rel = ok = 0
    nem = Counter()
    minta = []
    for s in iter_i:
        if len(s) <= i_vv:
            continue
        rel += 1
        vid = s[i_vv].strip()
        if len(minta) < 3:
            minta.append(vid)
        konyv = None
        if vid in vers_terkep:
            konyv = vers_terkep[vid]
        elif re.fullmatch(r'\d{7,8}', vid):
            konyv = str(int(vid) // 1000000)  # BBCCCVVV
        else:
            m = re.match(r'^([1-3]?\s?[A-Za-z][A-Za-z ]*?)\.?\s*\d+[:.]\d+', vid)
            konyv = m.group(1) if m else None
        step = None
        if konyv is not None:
            konyv = konyv.strip()
            if konyv.isdigit() and 1 <= int(konyv) <= len(kanoni):
                step = kanoni[int(konyv) - 1]
            else:
                step = feloldo.get(kulcs(konyv))
        if step:
            ok += 1
        else:
            nem[konyv if konyv is not None else '(nem ertelmezheto)'] += 1
    sorok.append((azon, 'tema_vers_relaciok', rel, 'TopicIndex.csv adatsorai'))
    sorok.append((azon, 'verseid_minta', '|'.join(minta), 'az elso 3 VerseID nyersen'))
    sorok.append((azon, 'konyvkod_lekepezheto_relaciok', ok, 'Konyv_normalizalo_tabla.tsv-re (kanoni sorszam vagy nev alapjan)'))
    sorok.append((azon, 'konyvkod_nem_lekepezheto_relaciok', sum(nem.values()), ''))
    sorok.append((azon, 'nem_lekepezheto_kodok_top10', '; '.join('%s=%d' % kv for kv in nem.most_common(10)), ''))


def megnez_elcafe7(gyoker, sorok, feloldo):
    azon = 'elcafe7_lex'
    db = None
    for m, _, fajlok in os.walk(gyoker):
        if 'naves.db' in fajlok:
            db = os.path.join(m, 'naves.db')
            break
    if not db:
        sorok.append((azon, 'naves_db', 'nincs', 'naves.db nem talalhato'))
        return
    con = sqlite3.connect(db)
    cur = con.cursor()
    tablak = [r[0] for r in cur.execute("select name from sqlite_master where type='table'")]
    sorok.append((azon, 'sqlite_tablak', '|'.join(tablak), ''))
    if 'topics' not in tablak:
        sorok.append((azon, 'topics_tabla', 'nincs', ''))
        return
    oszlopok = [r[1] for r in cur.execute('pragma table_info(topics)')]
    sorok.append((azon, 'topics_oszlopok', '|'.join(oszlopok), ''))
    sorok.append((azon, 'temakor_sorok', cur.execute('select count(*) from topics').fetchone()[0], 'topics tabla'))
    minta = re.compile(r'\b([1-3]?[A-Z]{2,4})\s+(\d+):(\d+)')
    rel = ok = 0
    nem = Counter()
    for (entry,) in cur.execute('select entry from topics'):
        for m in minta.finditer(entry or ''):
            rel += 1
            if feloldo.get(kulcs(m.group(1))):
                ok += 1
            else:
                nem[m.group(1)] += 1
    con.close()
    sorok.append((azon, 'tema_vers_relaciok_also_becsles', rel,
                  'csak a KOD fej:vers alaku horgonyok; a folytatolagos versek (pl. 21:4,10) nincsenek benne -- also korlat'))
    sorok.append((azon, 'konyvkod_lekepezheto_relaciok', ok, 'STEPBible-kodokra (kis-/nagybetu-fuggetlen)'))
    sorok.append((azon, 'konyvkod_nem_lekepezheto_relaciok', sum(nem.values()), ''))
    sorok.append((azon, 'nem_lekepezheto_kodok_top10', '; '.join('%s=%d' % kv for kv in nem.most_common(10)), ''))


def megnez_basokant(gyoker, sorok):
    azon = 'basokant_nave'
    kiterj = Counter()
    nagy = []
    for m, almappak, fajlok in os.walk(gyoker):
        almappak[:] = [a for a in almappak if a != '.git']
        for fn in fajlok:
            ut = os.path.join(m, fn)
            kiterj[os.path.splitext(fn)[1].lower() or '(nincs)'] += 1
            nagy.append((os.path.getsize(ut), os.path.relpath(ut, gyoker).replace(os.sep, '/')))
    sorok.append((azon, 'fajlok_kiterjesztesenkent', '; '.join('%s=%d' % kv for kv in kiterj.most_common()), ''))
    nagy.sort(reverse=True)
    sorok.append((azon, 'legnagyobb_fajlok', '; '.join('%s=%d' % (r, b) for b, r in nagy[:8]), 'relativ ut=bajt'))
    for b, r in nagy[:8]:
        if r.lower().endswith('.json') and b <= 60_000_000:
            try:
                with open(os.path.join(gyoker, r), encoding='utf-8') as f:
                    d = json.load(f)
                sorok.append((azon, 'json_szerkezet:' + r, '%s/%d' % (type(d).__name__, len(d)),
                              'legfelso szintu tipus/elemszam'))
            except Exception as e:  # noqa: BLE001
                sorok.append((azon, 'json_szerkezet:' + r, 'hiba', str(e)[:100]))


def fut(munka, parancs):
    sorok = []
    feloldo, kanoni = konyv_feloldo()
    verziok = []
    for azon, url in JELOLTEK:
        cel = os.path.join(munka, azon)
        commit, hiba = kozos.klonoz(url, cel)
        verziok.append('%s=%s' % (azon, commit or 'NEM_ELERHETO'))
        if not commit:
            sorok.append((azon, 'elerheto', 'nem', hiba))
            continue
        sorok.append((azon, 'elerheto', 'igen', 'commit ' + commit))
        try:
            if azon == 'theonize_bible_database':
                megnez_theonize(cel, sorok, feloldo, kanoni)
            elif azon == 'elcafe7_lex':
                megnez_elcafe7(cel, sorok, feloldo)
            else:
                megnez_basokant(cel, sorok)
        except Exception as e:  # noqa: BLE001 -- a hiba is meresi eredmeny
            sorok.append((azon, 'meres_hiba', type(e).__name__, str(e)[:200]))
        for rel, k in kozos.licenc_gyujt(azon, cel):
            sorok.append((azon, 'licenc_fajl', rel, '%d karakter' % k))
    if kozos.SZARAZ:
        print('nave: szaraz futas, %d jelolt, szerkezet rendben' % len(JELOLTEK))
        return
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_nave.tsv'),
                 kozos.fejlec(' ; '.join(u for _, u in JELOLTEK), ' ; '.join(verziok), parancs),
                 ['forras', 'mero', 'ertek', 'megjegyzes'], sorok)
    print('nave: %d sor' % len(sorok))
