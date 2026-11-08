#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
targum_import.py -- F176.2: a Sefaria-export (Onkelos + Targum Jonathan a Profetakhoz) konverzioja
konkordancia/Targum_PD.tsv-be.

Bemenet (CLI):  --be <konyvtar>   a letoltott Sefaria-export json-jai (`<Cim_aláhuzassal>.json`), a repon kivul
                --books <books.json>  (a Sefaria-Export books.json; csak a sha256-ja kerul a fejlecbe)
Kimenet: konkordancia/Targum_PD.tsv

Szabalyok:
  * csak a `license` mezoben `Public Domain` verzio megy at (verziónként ellenőrizve); ami mas, SystemExit.
  * a versszamozas a forras sajat (MT-) szamozasa: az `igehely` a magyar konyvrovidites + a forras fejezet:verse,
    NEM Karoli-atszamozas; a `forras_vers` a Sefaria-hivatkozas valtozatlanul; a `forras_kulcs` oszlop csak
    jelzi, hogy az igehely-kulcs letezik-e a Karoli_1908.tsv-ben (igen/nem) -- a feloldas tartalmi dontes.
  * a HTML-jelolest (ha van) eltavolitja; az ures versek nem kerulnek sorba (szamuk a stderr-en).
Futtatas:  python -I eszkozok/visszhang/targum_import.py --be <letoltes/json> --books <books.json>
"""
import argparse
import glob
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402

CIM_RX = re.compile(r'^(Onkelos|Targum Jonathan on) (.+)$')
TAG_RX = re.compile(r'<[^>]+>')


def tisztit(s):
    t = html.unescape(TAG_RX.sub('', s)).replace(' ', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def fut(be, books, ki):
    magyar, sorrend = K.normalizalo()
    karoli = K.karoli_kulcsok()
    sorok, forrasok, ures, cimkes = [], [], 0, 0
    for ut in sorted(glob.glob(os.path.join(be, '*.json'))):
        d = json.load(open(ut, encoding='utf-8'))
        m = CIM_RX.match(d['title'])
        if not m:
            raise SystemExit('ismeretlen cim: %s' % d['title'])
        if d.get('license') != 'Public Domain':
            raise SystemExit('NEM Public Domain verzio: %s / %s / %s' % (d['title'], d['versionTitle'], d.get('license')))
        if d.get('language') != 'he':
            raise SystemExit('nem arameus/heber nyelvi verzio: %s' % d['title'])
        targum = 'Onkelos' if m.group(1) == 'Onkelos' else 'Jonatan'
        konyv = m.group(2)
        step = K.ANGOL_STEP[konyv]
        hu = magyar[step]
        forrasok.append((d['title'], d['versionTitle'], d['license'], d.get('versionSource', ''), K.sha256_fajl(ut)))
        for fi, fej in enumerate(d['text'], 1):
            if not isinstance(fej, list):
                raise SystemExit('nem fejezet/vers szerkezet: %s' % d['title'])
            for vi, sz in enumerate(fej, 1):
                if isinstance(sz, list):
                    sz = ' '.join(x for x in sz if isinstance(x, str))
                if not isinstance(sz, str) or not sz.strip():
                    ures += 1
                    continue
                if '<' in sz:
                    cimkes += 1
                kulcs = '%s %d:%d' % (hu, fi, vi)
                sorok.append([(sorrend.index(step), fi, vi), kulcs, '%s %d:%d' % (konyv, fi, vi), targum, d['title'], d['versionTitle'],
                              'igen' if kulcs in karoli else 'nem', tisztit(sz)])
    sorok.sort(key=lambda r: r[0])
    sorok = [r[1:] for r in sorok]
    fejlec = [
        'GENERÁLT: eszkozok/visszhang/targum_import.py (F176.2); kézzel nem szerkeszthető.',
        'forras=Sefaria-Export (storage.googleapis.com/sefaria-export/json/Tanakh/Targum/...), %d verzió-fájl; csak a license=Public Domain verziók' % len(forrasok),
        'Onkelos: "Onkelos <Könyv>" (versionTitle "Onkelos <Könyv>", versionSource http://toratemetfreeware.com/); Jonatan: "Targum Jonathan on <Könyv>" (versionTitle "Mikraot Gedolot")',
        'books.json sha256=%s | ts=%s' % (K.sha256_fajl(books), K.ts()),
        'igehely = magyar könyvrövidítés + a FORRÁS (MT-) fejezet:verse; NEM Károli-átszámozás. forras_kulcs: az igehely-kulcs létezik-e a Karoli_1908.tsv-ben (jelzés, nem feloldás; versegyezést nem állít, a Károli-feloldás nézetoldali; l. VISSZHANG_README.md 1.).',
        'ures vers (kihagyva): %d; HTML-jelolest tartalmazo vers (tisztitva): %d' % (ures, cimkes),
    ]
    oszlopok = ['igehely', 'forras_vers', 'targum', 'forras_mu', 'verzio', 'forras_kulcs', 'szoveg']
    K.ir_tsv(ki, fejlec, oszlopok, sorok)
    print('sorok: %d; forras-fajlok: %d; ures vers: %d; cimkes vers: %d' % (len(sorok), len(forrasok), ures, cimkes))
    nem = sum(1 for s in sorok if s[5] == 'nem')
    print('forras_kulcs=nem: %d sor' % nem)
    return forrasok, sorok


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--be', required=True)
    ap.add_argument('--books', required=True)
    ap.add_argument('--ki', default=os.path.join(K.GYOKER, 'konkordancia', 'Targum_PD.tsv'))
    a = ap.parse_args()
    fut(a.be, a.books, a.ki)
