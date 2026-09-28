#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/ujra_max_tokens.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, a felhasznalo
kiegeszito 1. kerdese: a 4 legrovidebben csonkolt DeepSeek-kimenet ujrafuttatasa
explicit, megemelt max_tokens-szel (8000), annak tesztelesere, hogy a csonkolas
parameterhiba (hallgatolagos tokenplafon) volt-e. Kulon fajlba ir, a fp2/_run
eredeti gyorsitotarat NEM erinti.

    python fp2/ujra_max_tokens.py
"""
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import fordit  # noqa: E402

KIMENET_DIR = os.path.join(REPO, 'fp2', '_ujra_max_tokens')
DEEPSEEK = 'deepseek/deepseek-v4-flash'

# a 4 legrovidebben csonkolt, EGY-darabos DeepSeek kimenet (fp2/kapu_keresztellenorzes.py-bol)
CELPONTOK = ['G1311', 'G5010', 'G5356', 'G2672']


def main():
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print('HIBA -- nincs OPENROUTER_API_KEY', file=sys.stderr)
        return 1

    thayer = fordit.thayer_betolt()
    terminologia_sz = fordit.terminologia_szoveg(
        fordit.terminologia_betolt(os.path.join(REPO, 'fp2', 'terminologia_v3.tsv')))
    karoli_sz = fordit.karoli_tabla_szoveg(fordit.karoli_tabla_betolt())
    with open(os.path.join(REPO, 'fp2', 'prompt_v3.md'), encoding='utf-8') as fh:
        sablon = fh.read()

    os.makedirs(KIMENET_DIR, exist_ok=True)
    osszes_koltseg = 0.0
    eredmenyek = []

    for strong in CELPONTOK:
        forras = thayer[strong]['Teljes_szocikk']
        darabok = fordit.darabokra_bont(forras)
        assert len(darabok) == 1, '%s tobb darabos, ez a script csak 1-daraboshoz keszult' % strong
        prompt = fordit.prompt_epit(sablon, strong, darabok[0], '', terminologia_sz, karoli_sz)

        print('... %s ujrafuttatas max_tokens=8000-rel' % strong, flush=True)
        eredmeny, usage, _ = fordit.openrouter_hivas(
            DEEPSEEK, prompt, api_key, max_tokens=8000)
        koltseg = usage.get('cost') or 0.0
        osszes_koltseg += koltseg
        print('    kesz: kimenet_token=%s koltseg=%.5f USD, hossz=%d (eredeti forras=%d, arany=%.2f)'
              % (usage.get('completion_tokens'), koltseg, len(eredmeny['forditas_hu']),
                 len(forras), len(eredmeny['forditas_hu']) / len(forras)))

        with open(os.path.join(KIMENET_DIR, '%s.json' % strong), 'w', encoding='utf-8', newline='\n') as fh:
            json.dump({'strong': strong, 'model': DEEPSEEK, 'max_tokens': 8000,
                       'usage': usage, 'eredmeny': eredmeny}, fh, ensure_ascii=False, indent=1)

        eredmenyek.append((strong, len(forras), len(eredmeny['forditas_hu']), koltseg))

    print('\n=== osszesito ===')
    print('teljes koltseg: %.4f USD' % osszes_koltseg)
    for strong, forras_h, ki_h, koltseg in eredmenyek:
        print('  %-8s forras=%5d uj_kimenet=%5d arany=%.2f koltseg=%.5f' %
              (strong, forras_h, ki_h, ki_h / forras_h, koltseg))
    return 0


if __name__ == '__main__':
    sys.exit(main())
