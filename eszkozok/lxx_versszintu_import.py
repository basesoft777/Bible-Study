"""LXX_versszintu_parok.tsv -- a S0b.3 (naplok/SZOTAR_S0b_lxx_versszint_szkript.py,
csak H7121-re) altalanositasa mind a 26 heber gerinc-tokenre (D28 hatokor).

F05_SZOTAR_BRIEF.md S13: a motivum sajat heber Strong-tokenjenek Karoli-
igehelyeit a konkordancia/LXX_OS/*.tsv-ben megtalalva, versenkent
egyedi, grammatikailag szurt (adat/grammatikai_strongok.tsv 31 G-sora)
gorog Strong-kodokkal parositva -- "versszintu egyutt-eloforduls, nem
szoillesztes" (D14/D25).

TSV-iras kizarolag '\\t'.join() (CLAUDE.md).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import glob
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')

KIMENET = os.path.join(KONKORDANCIA, 'LXX_versszintu_parok.tsv')

# A 26 heber gerinc-token (D28 hatokor), az adat/elofordulasok.tsv strong
# mezojebol kinyerve (S1.4 futtataskor lekerdezve, l. a jelentes).
HEBER_TOKENEK = [
    'H0127', 'H0430', 'H0779', 'H0922', 'H1121', 'H2403', 'H2416', 'H2555',
    'H3548', 'H3678', 'H4467', 'H5303', 'H5315', 'H6093', 'H6975', 'H7043',
    'H7121', 'H7451', 'H7496', 'H7497', 'H7585', 'H7843', 'H8004', 'H8034',
    'H8414', 'H8415',
]


def read_tsv_skip_comments(path):
    with open(path, encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f if not l.startswith('#')]
    header = lines[0].split('\t')
    rows = []
    for l in lines[1:]:
        if not l:
            continue
        parts = l.split('\t')
        parts += [''] * (len(header) - len(parts))
        rows.append(dict(zip(header, parts)))
    return rows


def main():
    gram_rows = read_tsv_skip_comments(os.path.join(ADAT, 'grammatikai_strongok.tsv'))
    gram_g = {r['strong'] for r in gram_rows if r['strong'].startswith('G')}
    print('grammatikai G-strong szam:', len(gram_g))

    tahot_rows = read_tsv_skip_comments(os.path.join(KONKORDANCIA, 'TAHOT_kivonat.tsv'))
    token_versek = {}
    for token in HEBER_TOKENEK:
        versek = sorted({r['Igehely'] for r in tahot_rows if r['Strong-szám'] == token})
        token_versek[token] = versek
        print('%s: %d TAHOT-igehely' % (token, len(versek)))

    lxx_files = sorted(glob.glob(os.path.join(KONKORDANCIA, 'LXX_OS', '*.tsv')))
    vers_index = {}  # igehely_karoli -> [(strong_g, lxx_igehely), ...]
    for fp in lxx_files:
        for r in read_tsv_skip_comments(fp):
            kv = r.get('igehely_karoli', '')
            if not kv:
                continue
            strong_raw = r.get('strong', '')
            if not strong_raw:
                continue
            strong_g = 'G' + strong_raw.zfill(4)
            vers_index.setdefault(kv, []).append((strong_g, r.get('igehely_lxx', '')))

    ma = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    sorok = []
    hianyzo_osszesen = 0
    for token in HEBER_TOKENEK:
        for kv in token_versek[token]:
            talalatok = vers_index.get(kv)
            if not talalatok:
                hianyzo_osszesen += 1
                continue
            lxx_igehely = talalatok[0][1]
            egyedi_g = sorted({s for s, _ in talalatok})
            szurt_g = sorted(s for s in egyedi_g if s not in gram_g)
            proveniencia = ('scope=LXX_OS-versszint | forras=LXX_OS/*.tsv+grammatikai_strongok.tsv '
                             '| heber_strong=%s | ts=%s' % (token, ma))
            for g in szurt_g:
                sorok.append((token, kv, lxx_igehely, g, proveniencia))
            if not szurt_g:
                sorok.append((token, kv, lxx_igehely, '', proveniencia))

    header = ['heber_strong', 'igehely', 'lxx_igehely', 'gorog_strong', 'proveniencia']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/lxx_versszintu_import.py — kézzel nem szerkesztendő.\n')
        f.write('# Versszintu egyutt-elofordulas (S13, D14/D25) -- NEM szoillesztes. '
                'Kulcs: heber_strong+igehely+gorog_strong. Dok.: konkordancia/README.md\n')
        f.write('\t'.join(header) + '\n')
        for row in sorted(sorok):
            f.write('\t'.join(row) + '\n')

    print()
    print('sorok osszesen: %d' % len(sorok))
    print('TAHOT-igehely LXX_OS-ben nem talalhato (kihagyva): %d' % hianyzo_osszesen)
    print('irva: %s' % KIMENET)


if __name__ == '__main__':
    main()
