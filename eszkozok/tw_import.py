"""unfoldingWord Translation Words (tW) import -- teljes kt+other allomany.

F05_SZOTAR_BRIEF.md S14 (D20, S0b.2 elfogadva mindket nyelven). Forras:
git.door43.org/unfoldingWord/en_tw, tag v91, commit
ff5b3852c27c3a0d01b109e482eb26047dcd20e2. CC BY-SA 4.0 -- a szarmazekos
munkabol az unfoldingWord(R) vedjegyet el kell hagyni, a modositast
jelezni kell, forrasmegjeloles szo szerint: "The original work by
unfoldingWord is available from unfoldingword.org/utw" (l. a README-t).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import argparse
import glob
import hashlib
import os
import re
import shutil
import tarfile
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')
KIMENET = os.path.join(KONKORDANCIA, 'tW_szocikkek.tsv')

TW_TAG = 'v91'
TW_COMMIT = 'ff5b3852c27c3a0d01b109e482eb26047dcd20e2'
TW_URL = 'https://git.door43.org/unfoldingWord/en_tw/archive/%s.tar.gz' % TW_TAG

STRONG_LINE_RE = re.compile(r"Strong[’']?s\s*:\s*(.+)", re.IGNORECASE)
STRONG_CODE_RE = re.compile(r'([HG])(\d{1,6})[a-z]?')
TITLE_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def download_source():
    tmp = tempfile.mkdtemp(prefix='tw_import_')
    tarball = os.path.join(tmp, 'en_tw.tar.gz')
    urllib.request.urlretrieve(TW_URL, tarball)
    tar_sha = sha256_file(tarball)
    with tarfile.open(tarball) as tf:
        tf.extractall(path=tmp)
    entries = [n for n in os.listdir(tmp) if os.path.isdir(os.path.join(tmp, n))]
    root_dir = os.path.join(tmp, entries[0])
    return root_dir, tar_sha, tmp


def normalize_strong(raw_code):
    m = STRONG_CODE_RE.match(raw_code.strip())
    if not m:
        return None
    prefix, digits = m.groups()
    if prefix == 'H':
        return 'H' + digits.zfill(4)
    # a gorog kodok a tW-ben 5 jegyuek (4 jegyu alapszam + 1 zaro
    # "jelentes-valtozat" szamjegy, tobbnyire 0) -- l. S0b.2 (b) pont;
    # a mi H/G STRONG-tipusunk 4 jegyu, ezert az utolso szamjegyet levagjuk,
    # ha 5 jegyu a bemenet.
    if len(digits) == 5:
        digits = digits[:4]
    return 'G' + digits.zfill(4)


def parse_file(path, kategoria, commit):
    with open(path, encoding='utf-8') as f:
        szoveg = f.read()
    tw_id = kategoria + '/' + os.path.splitext(os.path.basename(path))[0]

    cim_m = TITLE_RE.search(szoveg)
    cim = cim_m.group(1).strip() if cim_m else ''

    strong_m = STRONG_LINE_RE.search(szoveg)
    strongok = []
    if strong_m:
        for raw in strong_m.group(1).split(','):
            norm = normalize_strong(raw)
            if norm and norm not in strongok:
                strongok.append(norm)
    strong_mezo = '+'.join(strongok)

    return tw_id, kategoria, cim, strong_mezo, szoveg, commit


def run(bible_dir, commit):
    sorok = []
    strong_nelkul = 0
    for kategoria in ('kt', 'other'):
        d = os.path.join(bible_dir, kategoria)
        if not os.path.isdir(d):
            print('FIGYELEM -- hiányzó alkönyvtár: %s' % d, file=sys.stderr)
            continue
        for fp in sorted(glob.glob(os.path.join(d, '*.md'))):
            row = parse_file(fp, kategoria, commit)
            sorok.append(row)
            if not row[3]:
                strong_nelkul += 1

    os.makedirs(KONKORDANCIA, exist_ok=True)
    header = ['tw_id', 'kategoria', 'cim', 'strong', 'szoveg', 'forras_commit']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/tw_import.py — kézzel nem szerkesztendő.\n')
        f.write('# forras: git.door43.org/unfoldingWord/en_tw @ tag=%s commit=%s\n' % (TW_TAG, commit))
        f.write('# licenc: CC BY-SA 4.0 — © unfoldingWord; forrásmegjelölés és védjegy-szabály: '
                'konkordancia/tW_README.md\n')
        f.write('\t'.join(header) + '\n')
        for row in sorok:
            # a szoveg tabot/ujsort tartalmazhat -- CLAUDE.md szerint a mezok
            # kozott csak tab a elvalaszto, a mezon beluli ujsor/tab literalisan
            # veszelyes -- ezert a szoveg mezoben az ujsorokat \n escape-eljuk,
            # a tabot szokozre cusereljuk, hogy a sor egyetlen fizikai sor maradjon.
            sor = list(row)
            sor[4] = sor[4].replace('\t', '    ').replace('\r\n', '\n').replace('\n', '\\n')
            f.write('\t'.join(sor) + '\n')

    kt_n = sum(1 for r in sorok if r[1] == 'kt')
    other_n = sum(1 for r in sorok if r[1] == 'other')
    print('sorok osszesen: %d (kt=%d, other=%d)' % (len(sorok), kt_n, other_n))
    print('Strong-kod nelkuli szocikk: %d' % strong_nelkul)
    print('irva: %s' % KIMENET)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--letolt', action='store_true', help='forrás letöltése a v91 tag-ről')
    ap.add_argument('--forras', metavar='KÖNYVTÁR', help='már kibontott en_tw gyökérkönyvtára (a "bible/" szülője)')
    args = ap.parse_args()

    if args.letolt and args.forras:
        print('HIBA: --letolt és --forras kizárja egymást.', file=sys.stderr)
        sys.exit(1)
    if not args.letolt and not args.forras:
        print('HIBA: --letolt vagy --forras szükséges.', file=sys.stderr)
        sys.exit(1)

    cleanup_dir = None
    try:
        if args.letolt:
            root_dir, tar_sha, cleanup_dir = download_source()
            print('letoltve: %s' % TW_URL)
            print('tarball sha256: %s' % tar_sha)
            bible_dir = os.path.join(root_dir, 'bible')
        else:
            bible_dir = os.path.join(args.forras, 'bible')
        run(bible_dir, TW_COMMIT)
    finally:
        if cleanup_dir:
            shutil.rmtree(cleanup_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
