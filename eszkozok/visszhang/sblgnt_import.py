#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sblgnt_import.py -- F176.2: az SBLGNT kritikai apparatusa (LogosBible/SBLGNT, data/sblgntapp/text/*.txt)
-> konkordancia/SBLGNT_apparatus.tsv.

Bemenet (CLI):  --be <konyvtar>   a 27 apparatus-szovegfajl (Matt.txt, Mark.txt, ...), a repon kivul
                --commit <sha>    a LogosBible/SBLGNT commit, amibol a fajlok valok (a fejlecbe)
                --license <fajl>  a commit LICENSE-fajlja (sha256 a fejlecbe)
Kimenet: konkordancia/SBLGNT_apparatus.tsv

Egy sor = egy apparatus-jegyzet (a vers alatti `•`-os vagy szamozott sor), szo szerint a forrasbol, a vezeto `•` nelkul.
Az SBLGNT alapszovege NEM kerul at (arra a TAGNT_kivonat.tsv `SBL` jelzese es a Macula_gorog.tsv hivatkozik);
csak a kritikai apparatus. A versszamozas a forras sajat szamozasa (nem Karoli-atszamozas): az `igehely` a magyar
konyvrovidites + a forras fejezet:verse, a `forras_vers` a forras fejlecsora; a `karoli_kulcs` csak letezest jelez.
Futtatas:  python -I eszkozok/visszhang/sblgnt_import.py --be <letoltes/app> --commit <sha> --license <LICENSE>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402

KONYV = {
    'Matthew': 'Mat', 'Mark': 'Mrk', 'Luke': 'Luk', 'John': 'Jhn', 'Acts': 'Act', 'Romans': 'Rom',
    '1 Corinthians': '1Co', '2 Corinthians': '2Co', 'Galatians': 'Gal', 'Ephesians': 'Eph', 'Philippians': 'Php',
    'Colossians': 'Col', '1 Thessalonians': '1Th', '2 Thessalonians': '2Th', '1 Timothy': '1Ti', '2 Timothy': '2Ti',
    'Titus': 'Tit', 'Philemon': 'Phm', 'Hebrews': 'Heb', 'James': 'Jas', '1 Peter': '1Pe', '2 Peter': '2Pe',
    '1 John': '1Jn', '2 John': '2Jn', '3 John': '3Jn', 'Jude': 'Jud', 'Revelation': 'Rev',
}
FEJ_RX = re.compile(r'^((?:[1-3] )?[A-Z][a-z]+) ([0-9]+):([0-9]+)(?:\s*[–-]\s*([0-9]+)(?::([0-9]+))?)?\s*$')


def fut(be, commit, lic, ki):
    magyar, sorrend = K.normalizalo()
    karoli = K.karoli_kulcsok()
    sorok, fajlok, nemfej = [], 0, []
    for fn in sorted(os.listdir(be)):
        if not fn.endswith('.txt'):
            continue
        fajlok += 1
        szoveg = open(os.path.join(be, fn), encoding='utf-8-sig').read().replace('\r\n', '\n')
        blokkok = re.split(r'\n\s*\n', szoveg.strip())
        for b in blokkok:
            sorai = [s.rstrip() for s in b.split('\n') if s.strip()]
            m = FEJ_RX.match(sorai[0]) if sorai else None
            if not m:
                nemfej.append((fn, sorai[0][:60] if sorai else ''))
                continue
            step = KONYV[m.group(1)]
            kulcs = '%s %s:%s' % (magyar[step], m.group(2), m.group(3))
            for i, j in enumerate(sorai[1:], 1):
                j = re.sub(r'^•\s*', '', j.strip())
                sorok.append([(sorrend.index(step), int(m.group(2)), int(m.group(3)), i), kulcs, sorai[0].strip(), str(i),
                              'igen' if kulcs in karoli else 'nem', j])
    sorok.sort(key=lambda r: r[0])
    sorok = [r[1:] for r in sorok]
    fejlec = [
        'GENERÁLT: eszkozok/visszhang/sblgnt_import.py (F176.2); kézzel nem szerkeszthető.',
        'forras=github.com/LogosBible/SBLGNT @ %s, data/sblgntapp/text/*.txt (%d fájl) | licenc: CC BY 4.0 (a repó LICENSE-fájlja és README-je; LICENSE sha256=%s) | ts=%s' % (commit, fajlok, K.sha256_fajl(lic), K.ts()),
        'kötelező megjelölés: SBL Greek New Testament, Copyright 2010 Society of Biblical Literature and Logos Bible Software, CC BY 4.0 (https://sblgnt.com)',
        'egy sor = egy apparátus-jegyzet, szó szerint; az SBLGNT alapszövege nincs a táblában. igehely = magyar könyvrövidítés + a FORRÁS fejezet:verse (NEM Károli-átszámozás); karoli_kulcs: az igehely-kulcs létezik-e a Karoli_1908.tsv-ben.',
        'nem verssor-fejléccel kezdődő blokk (kihagyva): %d' % len(nemfej),
    ]
    K.ir_tsv(ki, fejlec, ['igehely', 'forras_vers', 'sorszam', 'karoli_kulcs', 'jegyzet'], sorok)
    print('sorok: %d; fajlok: %d; nem-fejleces blokk: %d %s; karoli_kulcs=nem: %d' % (
        len(sorok), fajlok, len(nemfej), nemfej[:5], sum(1 for s in sorok if s[3] == 'nem')))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--be', required=True)
    ap.add_argument('--commit', required=True)
    ap.add_argument('--license', required=True)
    ap.add_argument('--ki', default=os.path.join(K.GYOKER, 'konkordancia', 'SBLGNT_apparatus.tsv'))
    a = ap.parse_args()
    fut(a.be, a.commit, a.license, a.ki)
