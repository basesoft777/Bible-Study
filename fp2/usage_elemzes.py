#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/usage_elemzes.py -- a fp2/_run/cache/*/*.json nyers usage-adatai:
completion_tokens, reasoning_tokens, es (ha van) finish_reason-kozeli jelek,
modellenkent es szocikkenkent/darabonkent. A fordit.py NEM tarolja kulon a
finish_reason-t a sikeres valaszokban (a nyers valasz eldobasra kerul --
l. cache_ir/openrouter_hivas), ezert ez a script csak a token-adatokbol
kovetkeztet: ha a completion_tokens kerek/plafon-szeru ertekre all meg
(pl. 1024/2048/4096), az implicit (a fordit.py altal be nem allitott)
max_tokens-plafonra utal.

    python fp2/usage_elemzes.py
"""
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(REPO, 'fp2', '_run', 'cache')
HIBA_DIR = os.path.join(REPO, 'fp2', '_run', 'hibak') if os.path.isdir(
    os.path.join(REPO, 'fp2', '_run', 'hibak')) else None


def main():
    print('=== hiba-naplo (ha van) ===')
    hiba_dir_kimenet = os.path.join(REPO, 'fp2', '_run', 'hibak')
    if os.path.isdir(hiba_dir_kimenet):
        for gyoker, _, fajlok in os.walk(hiba_dir_kimenet):
            for fn in fajlok:
                print('  HIBA-FAJL:', os.path.join(gyoker, fn))
    else:
        print('  (nincs hibak konyvtar -- egyetlen hivas sem futott ki a JSON-ujraprobalkozasbol)')

    print('\n=== completion_tokens es reasoning_tokens darabonkent, modellenkent ===')
    for model_slug in sorted(os.listdir(CACHE_DIR)):
        modell_dir = os.path.join(CACHE_DIR, model_slug)
        if not os.path.isdir(modell_dir):
            continue
        print('\n-- %s --' % model_slug)
        for fn in sorted(os.listdir(modell_dir)):
            if not fn.endswith('.json'):
                continue
            with open(os.path.join(modell_dir, fn), encoding='utf-8') as fh:
                adat = json.load(fh)
            usage = adat.get('usage', {})
            ki = usage.get('completion_tokens')
            reas = (usage.get('completion_tokens_details') or {}).get('reasoning_tokens')
            print('  %-16s kimenet_token=%6s reasoning_token=%6s' % (fn, ki, reas))


if __name__ == '__main__':
    main()
