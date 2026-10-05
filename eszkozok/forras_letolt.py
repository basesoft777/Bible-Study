"""Forrásfájlok sha256-os helyreállítása (F42, M1).

Ma egyetlen fájlt tud: a `konkordancia/TBESH.txt`-t, a STEPBible-Data
`b99716b0cddb648ddb95cc786a197180f2f97d48` commitjáról. A fájl a repóban
marad (DT-F42e); a szkript friss klónban, cloud sessionben vagy sérülés után
állítja vissza, és csak akkor tölt le, ha a fájl hiányzik vagy az ellenőrzőösszeg
nem egyezik (idempotens).

NEM tölt le: a `TBESH.lexicon`-t (a forrása, egy Google Drive-fájl, nem
rögzíthető commitra; DT-F42b) és a `TBESH_konszolidalt.tsv`-t (generált:
`python eszkozok/tbesh_konszolidalt_import.py`).

Használat:
    python eszkozok/forras_letolt.py              # hiányzót/hibásat letölti
    python eszkozok/forras_letolt.py --ellenoriz  # csak ellenőriz, hálózat nélkül
A CI nem futtatja (DT-F42c).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import hashlib
import os
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import utvonalak as U  # noqa: E402

COMMIT = 'b99716b0cddb648ddb95cc786a197180f2f97d48'
REPO = 'STEPBible/STEPBible-Data'

# cel -> (út a forrásrepóban, sha256, méret bájtban)
MANIFEST = {
    U.TBESH_TXT: (
        'Lexicons/TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt',
        '464dccadd95fd8620dd05fa0d7a4caba58ec3c4d5db3ebf38e43d046ca25b591',
        3288045,
    ),
}


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def url(forras_ut):
    return 'https://raw.githubusercontent.com/%s/%s/%s' % (
        REPO, COMMIT, urllib.parse.quote(forras_ut))


def allapot(cel):
    _, sha, _ = MANIFEST[cel]
    if not os.path.isfile(cel):
        return 'hianyzik'
    return 'ok' if sha256_fajl(cel) == sha else 'eltero'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ellenoriz', action='store_true', help='csak ellenőriz, nem tölt le')
    args = ap.parse_args()
    rossz = 0
    for cel, (forras_ut, sha, meret) in MANIFEST.items():
        rel = os.path.relpath(cel, U.ROOT).replace(os.sep, '/')
        st = allapot(cel)
        if st == 'ok':
            print('%s: rendben (sha256 egyezik, nincs letöltés)' % rel)
            continue
        if args.ellenoriz:
            print('HIBA %s: %s' % (rel, st))
            rossz += 1
            continue
        print('%s: %s — letöltés: %s' % (rel, st, url(forras_ut)))
        with urllib.request.urlopen(url(forras_ut), timeout=120) as r:
            adat = r.read()
        if hashlib.sha256(adat).hexdigest() != sha:
            print('HIBA %s: a letöltött fájl sha256-ja nem egyezik (%d bájt, várt %d); nem írtam felül'
                  % (rel, len(adat), meret))
            rossz += 1
            continue
        os.makedirs(os.path.dirname(cel), exist_ok=True)
        with open(cel, 'wb') as f:
            f.write(adat)
        print('%s: visszaállítva, sha256 egyezik' % rel)
    print('Nem letölthető (helyben élő) fájlok: %s, %s'
          % (os.path.relpath(U.TBESH_LEXICON, U.ROOT).replace(os.sep, '/'),
             os.path.relpath(U.TBESH_KONSZOLIDALT, U.ROOT).replace(os.sep, '/')))
    sys.exit(1 if rossz else 0)


if __name__ == '__main__':
    main()
