#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FP2_meres.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 0. lepes (csak olvas).

Lekerdezi:
  - a Thayer_teljes.tsv szocikkszamat, teljes karakterszamat es hosszeloszlasat
    (median, p90, max);
  - az OpenRouter /api/v1/models vegpontrol a harom versenyzo modell
    (Gemini 3.1 Flash Lite, DeepSeek V4 Flash, MiniMax*) aktualis arat es
    parametereit.

Kimenet: stdout (a naplok/FP2_felmeres.md ebbol keszul).

    python naplok/FP2_meres.py
"""

import json
import os
import re
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def thayer_stat():
    fejlec = None
    hosszak = []
    ossz = 0
    for m in tsv_sorok(THAYER_UT):
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        h = len(r['Teljes_szocikk'])
        hosszak.append(h)
        ossz += h
    hosszak.sort()
    n = len(hosszak)
    p90_idx = int(round(0.90 * (n - 1)))
    print('## Thayer_teljes.tsv statisztika')
    print('szocikkek szama:', n)
    print('teljes karakterszam (Teljes_szocikk osszesen):', ossz)
    print('median hossz:', statistics.median(hosszak))
    print('p90 hossz:', hosszak[p90_idx])
    print('max hossz:', hosszak[-1])
    print('min hossz:', hosszak[0])
    return {'n': n, 'ossz': ossz, 'median': statistics.median(hosszak),
            'p90': hosszak[p90_idx], 'max': hosszak[-1], 'min': hosszak[0]}


def openrouter_modellek():
    import requests
    print('\n## OpenRouter /api/v1/models')
    v = requests.get('https://openrouter.ai/api/v1/models', timeout=60)
    print('HTTP', v.status_code)
    adat = v.json().get('data', [])
    print('modellek szama:', len(adat))

    minta = re.compile(r'gemini-3\.1-flash-lite$|deepseek-v4-flash$|minimax', re.I)
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
    with open(os.path.join(REPO, 'naplok', 'FP2_openrouter_jeloltek.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(sorted(jeloltek, key=lambda j: j['id']), fh, ensure_ascii=False, indent=1)
        fh.write('\n')

    print('\n## OpenRouter -- kulon "minimax" keresés (bővebb minta, created szerint rendezve)')
    minimax_sorok = [m for m in adat if 'minimax' in m['id'].lower()]
    minimax_sorok.sort(key=lambda m: m.get('created', 0))
    for m in minimax_sorok:
        p = m.get('pricing', {})
        print('  %-22s created=%-12s be %8s  ki %8s  ctx %8s  | %s' % (
            m['id'], m.get('created'),
            round(float(p.get('prompt', 0)) * 1e6, 4),
            round(float(p.get('completion', 0)) * 1e6, 4),
            m.get('context_length'), (m.get('description') or '')[:70]))
    if minimax_sorok:
        legujabb = minimax_sorok[-1]
        print('\n  legujabb (created szerint):', legujabb['id'], '| created=', legujabb.get('created'))


def main():
    thayer_stat()
    kulcs = os.environ.get('OPENROUTER_API_KEY')
    print('\nOPENROUTER_API_KEY:', 'beallitva' if kulcs else 'NINCS')
    if kulcs:
        openrouter_modellek()


if __name__ == '__main__':
    main()
