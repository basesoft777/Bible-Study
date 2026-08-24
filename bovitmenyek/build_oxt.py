#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Csomagoló szkript: bovitmenyek/pardes_strong_annotator/ forrásból elkészíti
a pardes_strong_annotator.oxt fájlt.

Két lépést végez:
1. Bemásolja a konkordancia/ mappából a bővítmény működéséhez szükséges
   3 TSV-t a bővítmény data/ almappájába (felülírva a korábbi másolatot) —
   így az .oxt önmagában hordozza az adatokat, nincs szüksége a repóra
   telepítés után (lásd README.md az indoklásért).
2. Zip-eli a bővítmény mappáját .oxt kiterjesztéssel (az .oxt egyszerűen
   egy ZIP, azonos módon strukturálva, mint egy .docx vagy .jar).

Használat:
    python bovitmenyek/build_oxt.py
"""

import os
import shutil
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
KONKORDANCIA = os.path.join(REPO_ROOT, 'konkordancia')
EXT_SRC = os.path.join(SCRIPT_DIR, 'pardes_strong_annotator')
EXT_DATA = os.path.join(EXT_SRC, 'data')
OXT_OUT = os.path.join(SCRIPT_DIR, 'pardes_strong_annotator.oxt')

REQUIRED_TSVS = [
    'Karoli_1908.tsv',
    'Karoli_Strong_kivonat.tsv',
    'Konyv_normalizalo_tabla.tsv',
]


def copy_data():
    os.makedirs(EXT_DATA, exist_ok=True)
    for name in REQUIRED_TSVS:
        src = os.path.join(KONKORDANCIA, name)
        if not os.path.isfile(src):
            raise SystemExit(f"HIBA: hiányzó forrásfájl: {src}")
        dst = os.path.join(EXT_DATA, name)
        shutil.copyfile(src, dst)
        print(f"  másolva: {name}")


def build_zip():
    if os.path.exists(OXT_OUT):
        os.remove(OXT_OUT)
    with zipfile.ZipFile(OXT_OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _dirs, files in os.walk(EXT_SRC):
            for fname in files:
                full = os.path.join(root, fname)
                arcname = os.path.relpath(full, EXT_SRC)
                z.write(full, arcname)
    print(f"kész: {OXT_OUT}")


def main():
    print("Konkordancia-TSV-k másolása a bővítménybe...")
    copy_data()
    print("Csomagolás .oxt fájlba...")
    build_zip()


if __name__ == '__main__':
    main()
