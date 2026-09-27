#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORDITAS_P0_meres.py -- FORDITAS_PILOT_BRIEF.md v1, FP0: a §0 kiindulás újramérése,
az openrouter.ai elérhetősége, a kulcs megléte (értéke soha nem kerül ki), és a
G3 modelljelöltek azonosítója és ára a /api/v1/models végpontról.

Kimenet: stdout (a naplok/FORDITAS_P0_kiindulas.md ebből készül) és
naplok/FORDITAS_P0_modellek.json (a jelölt modellek nyers árlistasora, kulcs nélkül).

    python naplok/FORDITAS_P0_meres.py
"""

import hashlib
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def lexikon_thayer():
    fejlec = None
    ki = []
    for m in tsv_sorok(os.path.join(REPO, 'adat', 'lexikon_hivatkozasok.tsv')):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        if r['szotar'] == 'Thayer':
            ki.append(r)
    return ki


def thayer_teljes():
    fejlec = None
    ki = {}
    for m in tsv_sorok(os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')):
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        ki[r['Strong_padded']] = r
    return fejlec, ki


def elofordulas_gorog_strongok(teljes_sor=False):
    """teljes_sor=False: csak a `strong` oszlop; True: a sor bármely mezője
    (a `kapcsolodas` szövegében említett Strong-számok is)."""
    fejlec = None
    strongok = set()
    for m in tsv_sorok(os.path.join(REPO, 'adat', 'elofordulasok.tsv')):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        szoveg = '\t'.join(m) if teljes_sor else r.get('strong', '')
        for s in re.findall(r'\bG\d{4}\b', szoveg):
            strongok.add(s)
    return strongok


def main():
    print('## 0.2 lexikon_hivatkozasok.tsv, szotar = Thayer')
    thayer = lexikon_thayer()
    print('sorok:', len(thayer))
    kesz = [r['strong'] for r in thayer if r['forditas_hu'].strip()]
    ures = sorted(r['strong'] for r in thayer if not r['forditas_hu'].strip())
    print('lefordítva:', kesz)
    print('üres forditas_hu (%d):' % len(ures), ', '.join(ures))

    print('\n## 0.3 az üres szócikkek szoveg_en hossza')
    ossz = 0
    for r in sorted(thayer, key=lambda r: r['strong']):
        if r['forditas_hu'].strip():
            continue
        h = len(r['szoveg_en'])
        ossz += h
        print('  %s %6d' % (r['strong'], h))
    print('összesen:', ossz)

    fejlec, tt = thayer_teljes()
    print('\n## 0.5 Thayer_teljes.tsv')
    print('szócikkek:', len(tt), '| fejléc:', fejlec)

    print('\n## 0.3b szoveg_en == Thayer_teljes Teljes_szocikk?')
    for r in sorted(thayer, key=lambda r: r['strong']):
        t = tt.get(r['strong'])
        azonos = t is not None and t['Teljes_szocikk'] == r['szoveg_en']
        print('  %s azonos=%s' % (r['strong'], azonos))

    print('\n## 0.4 elofordulasok.tsv görög tokenjei Thayer-sor nélkül')
    van = {r['strong'] for r in thayer}
    gor = elofordulas_gorog_strongok()
    print('(a) csak a `strong` oszlop: görög tokenek %d | Thayer-sor nélkül: %s'
          % (len(gor), ', '.join(sorted(gor - van)) or '0'))
    gor = elofordulas_gorog_strongok(teljes_sor=True)
    hiany = sorted(gor - van)
    print('(b) a teljes sor (szövegben említett is): görög tokenek', len(gor),
          '| Thayer-sor nélkül (%d):' % len(hiany), ', '.join(hiany))
    for s in hiany:
        t = tt.get(s)
        print('  %s Thayer_teljes-ben: %s, hossz %s' % (s, t is not None, len(t['Teljes_szocikk']) if t else '-'))

    print('\n## 0.7 kulcs és elérhetőség')
    kulcs = os.environ.get('OPENROUTER_API_KEY')
    print('OPENROUTER_API_KEY:', 'beállítva' if kulcs else 'NINCS')
    import requests
    v = requests.get('https://openrouter.ai/api/v1/models', timeout=60)
    print('GET /api/v1/models: HTTP', v.status_code)
    adat = v.json().get('data', [])
    print('modellek száma:', len(adat))
    minta = re.compile(r'deepseek.*(v4|flash)|gemini-3\.8|gemini-3.*flash|claude-haiku|claude-4\.5-haiku|haiku-4|gpt-5-mini', re.I)
    jeloltek = []
    for m in adat:
        if minta.search(m['id']):
            p = m.get('pricing', {})
            jeloltek.append({
                'id': m['id'], 'name': m.get('name'),
                'prompt_usd_per_1M': round(float(p.get('prompt', 0)) * 1e6, 4),
                'completion_usd_per_1M': round(float(p.get('completion', 0)) * 1e6, 4),
                'context_length': m.get('context_length'),
                'supported_parameters': m.get('supported_parameters'),
            })
    for j in sorted(jeloltek, key=lambda j: j['id']):
        print('  %-45s be %8s  ki %8s  ctx %s' % (j['id'], j['prompt_usd_per_1M'], j['completion_usd_per_1M'], j['context_length']))
    with open(os.path.join(REPO, 'naplok', 'FORDITAS_P0_modellek.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(sorted(jeloltek, key=lambda j: j['id']), fh, ensure_ascii=False, indent=1)
        fh.write('\n')


if __name__ == '__main__':
    main()
