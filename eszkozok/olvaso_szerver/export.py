"""Statikus export — váz (#76 M2): a lapelőállítás Flasktól függetlensége miatt egy paranccsal előállítható.

Az első kiadásban a lapok kérésre készülnek; ez a szkript azt mutatja meg, hogy az `oldalak.py` szerver nélkül is
előállítja a lapokat. Egy könyv fejezet-lapjait írja a megadott könyvtárba (`<könyv>/<fejezet>.html`).
A kimenet hivatkozásai szerver-abszolút útvonalak (`/szo/H0216`), tehát a teljes statikus változat (átírt
hivatkozások, az összes szó-lap) külön feladat; itt csak a váz van.

Használat:  python export.py --kimenet <könyvtár> [--konyv 1Moz] [--kiadas belso] [--db pardes.db]
A kimenet könyvtárát a repón kívülre kell tenni.
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import adatbazis
import hozzaferes
import oldalak


def kiir_arculat(gyar, kimenet):
    """A token-blokk (#98, DT-F98e) ugyanabból a függvényből (`arculat.css_blokk`), amelyből a szerver a `/arculat.css`-t adja;
    a lapok `/arculat.css?v=<hash>` címen linkelik (a váz szerver-abszolút hivatkozásaival)."""
    ut = os.path.join(kimenet, 'arculat.css')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(gyar.arculat.css)
    return ut


def kiir(gyar, kimenet, slug, szint):
    kk = gyar.kozos.slug_kk[slug]
    os.makedirs(os.path.join(kimenet, slug), exist_ok=True)
    kiir_arculat(gyar, kimenet)
    n = 0
    for fej, _ in gyar.kozos.fejezet_szam[kk]:
        # az új elrendezés, rétegek nélkül, ugyanabból a sablonból (#134, DT-F134h (a))
        html = gyar.fejezet_lap(slug, fej, None, oldalak.ALAP_RETEG, szint, '', '', '/%s/%d' % (slug, fej))
        with open(os.path.join(kimenet, slug, '%d.html' % fej), 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description='Statikus export váz (egy könyv fejezet-lapjai)')
    ap.add_argument('--kimenet', required=True)
    ap.add_argument('--konyv', default='1Moz')
    ap.add_argument('--kiadas', default='belso', choices=adatbazis.KIADASOK)
    ap.add_argument('--db', default=os.environ.get('PARDES_DB') or (adatbazis.GY + 'pardes.db'))
    a = ap.parse_args()
    hozz = hozzaferes.Hozzaferes.betolt()
    gyar = oldalak.OldalGyar(adatbazis.Adatbazis(a.db, a.kiadas), hozz)
    n = kiir(gyar, a.kimenet, a.konyv, hozz.szint())
    print('%d fejezet-lap kiírva: %s' % (n, os.path.join(a.kimenet, a.konyv)))


if __name__ == '__main__':
    main()
