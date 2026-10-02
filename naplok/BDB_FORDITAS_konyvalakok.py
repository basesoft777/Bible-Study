#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_konyvalakok.py -- F38 DT-F38 (c): a BDB-forras (konkordancia/
BDB_teljes_unabridged.tsv) igehely elotti konyvalakjai, amelyeket a 11. kapu
leképezése (forditas_kapuk._konyv_mintak) NEM ismer. Csak olvas.

Minta: nagybetuvel kezdodo szo (opcionalis 1-3 eloszammal, szokozzel vagy
anelkul), opcionalis pont, szokoz, majd `fejezet:vers`. A mar ismert kulcsok
(Karoli-, STEPBible-, FORRAS_ALIAS-, APOKRIF_ALIAS-alak) kimaradnak; a tobbi
darabszammal (elofordulas, szocikk) es harom peldaval kerul a kimenetre.

    python naplok/BDB_FORDITAS_konyvalakok.py [--min 1] [--peldak 3]
"""

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import forditas_kapuk as K  # noqa: E402

BDB_UT = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
BETU = r'A-Za-zÀ-ɏ'
MINTA = re.compile(
    r'(?<![%s0-9])((?:[1-3] ?|I{1,3} )?[A-Z][%s]*(?: of Solomon)?)(\.?)\s+(\d{1,3}):(\d{1,3})'
    % (BETU, BETU))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min', type=int, default=1)
    ap.add_argument('--peldak', type=int, default=3)
    ap.add_argument('--alak', nargs='*', default=[], help='csak ezek az alakok, minden pelda')
    args = ap.parse_args()
    lek = K._konyv_mintak()[0]
    elo = Counter()
    szocikk = defaultdict(set)
    pelda = defaultdict(list)
    with open(BDB_UT, encoding='utf-8') as fh:
        sorok = fh.read().split('\n')
    for sor in sorok[1:]:
        if not sor:
            continue
        m_ = sor.split('\t')
        strong, szoveg = m_[0], m_[2]
        for m in MINTA.finditer(szoveg):
            alak = m.group(1)
            # ket szavas talalatnal az utolso szo is lehet ismert kulcs
            # ("Compare Isa 1:1"): azt a kapu latja, nem hianyzo alak
            utolso = alak.split(' ')[-1]
            if alak in lek or utolso in lek:
                continue
            if args.alak and alak not in args.alak:
                continue
            elo[alak] += 1
            szocikk[alak].add(strong)
            if args.alak or len(pelda[alak]) < args.peldak:
                a = max(0, m.start() - 40)
                pelda[alak].append('%s: …%s…' % (strong, szoveg[a:m.end() + 25].replace('|', '¦')))
    print('| Alak | Előfordulás | Szócikk | Példa |')
    print('|---|---|---|---|')
    for alak, n in sorted(elo.items(), key=lambda kv: (-kv[1], kv[0])):
        if n < args.min:
            continue
        print('| `%s` | %d | %d | %s |' % (alak, n, len(szocikk[alak]), '<br>'.join(pelda[alak])))
    print()
    print('Összesen: %d alak, %d előfordulás' % (sum(1 for a in elo if elo[a] >= args.min),
                                                  sum(n for n in elo.values() if n >= args.min)))


if __name__ == '__main__':
    main()
