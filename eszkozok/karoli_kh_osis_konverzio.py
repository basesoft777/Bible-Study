#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_osis_konverzio.py -- a HunKar OSIS XML Károli-kereszthivatkozásainak kinyerése a `konkordancia/Karoli_kereszthivatkozasok.tsv`
formátumába (N-F156a). A tábla eredeti generálása (v24, 2026-08-24, 1a4d46a8) chat-menet volt, a szkript nem került a repóba;
ez a szkript a README módszerleírása szerint újraírja, és `--osszevet` módban sor-sorról összeveti a meglévő táblával.

A nyers forrás NINCS a repóban (adatként kezelendő, nem futtatható): github.com/krisek/HunKar, `hunkaroli_rev.osis.xml`,
commit 0e244494dd190e4a6b132c1afddfa307e73792f8, Public Domain (hunkar.conf). Az útvonal argumentum.

Használat:
    python -I eszkozok/karoli_kh_osis_konverzio.py <hunkaroli_rev.osis.xml> --osszevet
    python -I eszkozok/karoli_kh_osis_konverzio.py <hunkaroli_rev.osis.xml> --ki <kimenet.tsv>
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KH = 'konkordancia/Karoli_kereszthivatkozasok.tsv'
NORM = 'konkordancia/Konyv_normalizalo_tabla.tsv'
FEJLEC = 'Igehely\tKapcsolódó igehely\tKapcsolódó igehely magyar megjelenítése'


def beolvas(xml):
    """[(osis_vers, [(osis_cel, megjelenites)])] a forrás sorrendjében; csak a hivatkozásos versek."""
    with open(xml, encoding='utf-8') as f:
        t = f.read()
    versek = re.findall(r'<verse osisID="([^"]+)"[^>]*>(.*?)</verse>', t, re.S)
    ki = []
    for vid, test in versek:
        refs = re.findall(r'<reference osisRef="([^"]+)">(.*?)</reference>', test, re.S)
        ki.append((vid, refs))
    return ki


def konyvtabla(versek):
    """OSIS-könyvkód -> STEP-kód: pozíció alapján (66 könyv, kanonikus sorrend), a README szerint."""
    osis = []
    for vid, _ in versek:
        k = vid.split('.')[0]
        if k not in osis:
            osis.append(k)
    with open(os.path.join(GYOKER, NORM), encoding='utf-8') as f:
        step = [s.split('\t')[0] for s in f.read().split('\n')[1:] if s][:66]
    if len(osis) != 66 or len(step) != 66:
        raise SystemExit('nem 66 könyv: osis=%d step=%d' % (len(osis), len(step)))
    return dict(zip(osis, step))


def konv(ref, tabla):
    return '-'.join('.'.join([tabla[r.split('.')[0]]] + r.split('.')[1:]) for r in ref.split('-'))


def sorok(xml):
    versek = beolvas(xml)
    tabla = konyvtabla(versek)
    ki = []
    for vid, refs in versek:
        for cel, mutat in refs:
            ki.append('\t'.join([konv(vid, tabla), konv(cel, tabla), mutat]))
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xml')
    ap.add_argument('--osszevet', action='store_true', help='sor-sorról összeveti a meglévő táblával')
    ap.add_argument('--ki', help='kimeneti TSV (a repó gyökeréhez képest vagy abszolút)')
    a = ap.parse_args()
    uj = sorok(a.xml)
    print('forrásból kinyert sor: %d' % len(uj))
    if a.osszevet:
        with open(os.path.join(GYOKER, KH), encoding='utf-8') as f:
            reg = f.read().split('\n')
        fej, reg = reg[0], [s.rstrip('\r') for s in reg[1:] if s]
        kul = [(i + 2, x, y) for i, (x, y) in enumerate(zip(reg, uj)) if x != y]
        print('meglévő tábla: %d sor; fejléc egyezik: %s; eltérő sor: %d; hossz egyezik: %s'
              % (len(reg), fej == FEJLEC, len(kul), len(reg) == len(uj)))
        for i, x, y in kul[:10]:
            print('  %d: %r != %r' % (i, x, y))
        sys.exit(0 if not kul and len(reg) == len(uj) and fej == FEJLEC else 1)
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(FEJLEC + '\n' + '\n'.join(uj) + '\n')


if __name__ == '__main__':
    main()
