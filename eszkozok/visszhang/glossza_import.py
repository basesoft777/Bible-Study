#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
glossza_import.py -- a Glossa Ordinaria (Migne, 1880) lábjegyzetei a Vulgata-csomagból (F183, FELADATOK #183; N-F176a).

Az eBible latVUC csomag („Clementine Vulgate of 1598 with Glossa Ordinaria Migne edition 1880 in Latin”, licenc:
Public Domain) a Vulgata-szöveg mellett a Glossa Ordinaria lábjegyzeteit is hordozza (USFM `\\f + \\fr F.V \\fk … \\ft …
\\f*`). A `vulgata_import.py` (F176.2) ezeket kihagyta; ez a szkript ugyanabból a csomagból versenként kinyeri őket.

Bemenet (CLI):  --zip <latVUC_usfm.zip>   a letöltött csomag (a repón kívül; zipfile-lal olvas, nem bont ki)
Kimenet:        konkordancia/Glossa_Ordinaria.tsv (generált, kézzel nem szerkeszthető)
Oszlopok:       igehely (magyar könyvrövidítés + a FORRÁS-fejezet:vers, mint a Vulgata_Clementina.tsv-ben; nem
                Károli-átszámozás), forras_vers, forras_kulcs (a kulcs létezik-e a Károliban), sorszam (a vers
                lábjegyzeteinek sorrendje), jegyzet (a lábjegyzet szövege: a lemma-idézet « »-ben, utána a magyarázat)
Futtatás:       python -I eszkozok/visszhang/glossza_import.py --zip <latVUC_usfm.zip>

A szöveg közkincs (Migne, 1880); a lapra a tanúréteg (adat/visszhang_tanuk.tsv, SEMA 2.57) saját szavas
összefoglalója és a hivatkozás kerül. TSV-írás '\\t'.join(), a csv modul nem használható (CLAUDE.md).
"""
import argparse
import os
import re
import sys
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KIMENET = os.path.join(GYOKER, 'konkordancia', 'Glossa_Ordinaria.tsv')
BS = chr(92)
RE_FN = re.compile(re.escape(BS) + r'f \+\s*' + re.escape(BS) + r'fr\s+([0-9]+)[.:]([0-9]+)\s*(.*?)' +
                   re.escape(BS) + r'f\*', re.S)
RE_FK = re.compile(re.escape(BS) + r'fk\s+(.*?)\s*(?=' + re.escape(BS) + r'f[a-z]+\*?|$)', re.S)
RE_MARK = re.compile(re.escape(BS) + r'[a-z]+[0-9]*\*?')
FAJL_RX = re.compile(r'^[0-9]+-([0-9A-Z]{3})latVUC\.usfm$')


def tisztit(nyers):
    """A lábjegyzet szövege: a `\\fk` lemma-idézet « »-ben, a jelölők nélkül, egy sorban."""
    t = RE_FK.sub(lambda m: ' «%s» ' % m.group(1).strip(), nyers)
    t = RE_MARK.sub(' ', t)
    t = t.replace('\t', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def fut(zippath, ki):
    magyar, sorrend = K.normalizalo()
    karoli = K.karoli_kulcsok()
    z = zipfile.ZipFile(zippath)
    fajlok = {}
    for n in z.namelist():
        m = FAJL_RX.match(n)
        if m:
            fajlok[m.group(1)] = n
    sorok, osszes = [], 0
    for step in sorrend:
        usfm = step.upper()
        if usfm not in fajlok:
            raise SystemExit('hianyzo USFM-fajl: %s' % usfm)
        t = z.read(fajlok[usfm]).decode('utf-8-sig')
        szamlalo = {}
        for m in RE_FN.finditer(t):
            osszes += 1
            fej, v = int(m.group(1)), int(m.group(2))
            jegyzet = tisztit(m.group(3))
            if not jegyzet:
                continue
            kulcs = '%s %d:%d' % (magyar[step], fej, v)
            szamlalo[kulcs] = szamlalo.get(kulcs, 0) + 1
            sorok.append([kulcs, '%s %d:%d' % (usfm, fej, v), 'igen' if kulcs in karoli else 'nem',
                          str(szamlalo[kulcs]), jegyzet])
    fejlec = [
        'GENERÁLT: eszkozok/visszhang/glossza_import.py (F183); kézzel nem szerkeszthető.',
        'forras=https://ebible.org/Scriptures/latVUC_usfm.zip ("Clementine Vulgate of 1598 with Glossa Ordinaria Migne '
        'edition 1880 in Latin"; licenc: Public Domain, ebible.org/latVUC/copr.htm), sha256=%s | ts=%s'
        % (K.sha256_fajl(zippath), K.ts()),
        'a Glossa Ordinaria (Migne, 1880) lábjegyzetei versenként; a csomag lábjegyzetei: %d, átvett sor: %d (a kanonikus '
        '66 könyvből; a deuterokanonikus könyvek a Vulgata_Clementina.tsv-hez hasonlóan kimaradtak)' % (osszes, len(sorok)),
        'igehely = magyar könyvrövidítés + a FORRÁS (Vulgata-) fejezet:verse, a lábjegyzet \\fr hivatkozása szerint; NEM '
        'Károli-átszámozás (a zsoltárok és egyes könyvek számozása eltér); forras_kulcs: a kulcs létezik-e a Károliban.',
        'jegyzet: a lemma-idézet (\\fk) « »-ben, utána a magyarázat; a forrásmegjelölések (AUG., BEDA, HIERON. …) a '
        'szövegben, ahogy a kiadás adja.',
    ]
    K.ir_tsv(ki, fejlec, ['igehely', 'forras_vers', 'forras_kulcs', 'sorszam', 'jegyzet'], sorok)
    print('labjegyzet a csomagban: %d; atvett sor: %d; forras_kulcs=nem: %d' % (
        osszes, len(sorok), sum(1 for s in sorok if s[2] == 'nem')))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--zip', required=True)
    ap.add_argument('--ki', default=KIMENET)
    a = ap.parse_args()
    fut(a.zip, a.ki)


if __name__ == '__main__':
    main()
