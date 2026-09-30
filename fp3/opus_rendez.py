#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp3/opus_rendez.py -- F27_FP3_BRIEF.md P4: az Opus-subagentek darabonkenti JSON-kimenetebol
(fp3/_run/opus/ki/<strong>_<darab>.json) osszeallitja az fp3/forditas/opus/kimenet.tsv-t,
az FP2 kimenet-TSV semajaval es a fp2/rendezo.py szabalyaival (darabok ' '-vel
osszefuzve, sortores szokozre). Hianyzo darabot jelez, nem tol be.

    python fp3/opus_rendez.py
"""

import json
import os
import sys
from datetime import date

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEMENET = os.path.join(REPO, 'fp3', '_run', 'opus', 'bemenet')
KI = os.path.join(REPO, 'fp3', '_run', 'opus', 'ki')
MINTA = os.path.join(REPO, 'fp3', 'minta.tsv')
THAYER = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
KIMENET = os.path.join(REPO, 'fp3', 'forditas', 'opus', 'kimenet.tsv')
FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash',
          'forditas_hu', 'allapot', 'modell', 'datum', 'terminologia_verzio']
MODELL = 'anthropic/claude-opus (Code-session, vegrehajto-opus)'


def sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        return [s.rstrip('\r').split('\t') for s in fh.read().split('\n') if s.strip()]


def main():
    minta = sorok(MINTA)
    mf = minta[0]
    hash_ = {dict(zip(mf, r))['strong']: dict(zip(mf, r))['forras_hash'] for r in minta[1:]}
    tf = None
    entry = {}
    for r in sorok(THAYER):
        if tf is None:
            tf = r
            continue
        d = dict(zip(tf, r))
        entry[d['Strong_padded']] = d['Strong_eredeti']
    darabszam = {r[0]: int(r[1]) for r in sorok(os.path.join(BEMENET, '_lista.tsv'))[1:]}
    ki_sorok, hianyzo = [], []
    for strong in hash_:
        reszek = []
        for i in range(darabszam[strong]):
            p = os.path.join(KI, '%s_%d.json' % (strong, i))
            if not os.path.exists(p):
                hianyzo.append('%s_%d' % (strong, i))
                continue
            with open(p, encoding='utf-8') as fh:
                reszek.append(json.load(fh)['forditas_hu'])
        if len(reszek) != darabszam[strong]:
            continue
        szoveg = ' '.join(reszek).replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ')
        ki_sorok.append(['Thayer', strong, entry[strong], 'teljes', 'forditas_hu', hash_[strong],
                         szoveg, 'pilot', MODELL, date.today().isoformat(), 'v3'])
    os.makedirs(os.path.dirname(KIMENET), exist_ok=True)
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(FEJLEC) + '\n')
        for r in ki_sorok:
            fh.write('\t'.join(r) + '\n')
    print('%d/40 szocikk irva; hianyzo darab: %s' % (len(ki_sorok), hianyzo))


if __name__ == '__main__':
    main()
