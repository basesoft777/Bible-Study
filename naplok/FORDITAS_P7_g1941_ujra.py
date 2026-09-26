#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORDITAS_P7_g1941_ujra.py -- FORDITAS_KOR2_JAVITO_BRIEF.md K2: a DeepSeek
(m1) G1941-fordítása a kor2 futásban csonkolt (pontosság = 0, l.
FORDITAS_P5_pontok_kor2.tsv). Ez a szkript 3 FUGGETLEN, gyorsítótár nélküli
hívást futtat ugyanarra a bemenetre, hogy eldöntse: a csonkolás egyszeri
volt-e, vagy a DeepSeek megbízhatatlan hosszú, összetett szócikkeken.

Az eszkozok/fordit.py fuggvenyeit hasznalja VALTOZATLANUL (prompt_epit,
openrouter_hivas, terminologia_szoveg, karoli_tabla_szoveg, darabokra_bont,
thayer_betolt, minta_betolt) -- a fordit.py-t nem modositja, a gyorsitotarat
(naplok/FORDITAS_P_cache/) sem olvassa, sem irja, es a mar kesz
naplok/FORDITAS_P3_kimenet.tsv / naplok/FORDITAS_P_koltseg.tsv erintetlen
marad.

Kimenet:
  naplok/FORDITAS_P7_g1941_deepseek.tsv -- futas, bemenet_token, kimenet_token,
    finish_reason, koltseg_usd, hosszarany, gorog_heber_egyezes, json_ervenyes,
    forditas_hu
  naplok/FORDITAS_P7_g1941_deepseek.md -- a harom forditas olvashato formaban

    python naplok/FORDITAS_P7_g1941_ujra.py
"""

import os
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLOK = os.path.join(REPO, 'naplok')
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import fordit  # noqa: E402
from FORDITAS_P4_ellenoriz import GOROG_HEBER_MINTA, _ekezet_nelkul  # noqa: E402

MODELL_ID = 'deepseek/deepseek-v4-flash'
FUTASOK = 3

KIMENET_UT = os.path.join(NAPLOK, 'FORDITAS_P7_g1941_deepseek.tsv')
MD_UT = os.path.join(NAPLOK, 'FORDITAS_P7_g1941_deepseek.md')
KIMENET_FEJLEC = ['futas', 'bemenet_token', 'kimenet_token', 'finish_reason',
                   'koltseg_usd', 'hosszarany', 'gorog_heber_egyezes',
                   'json_ervenyes', 'forditas_hu']


def gorog_heber_egyezik_e(forras, forditas):
    f_forras = Counter(_ekezet_nelkul(t) for t in GOROG_HEBER_MINTA.findall(forras))
    f_forditas = Counter(_ekezet_nelkul(t) for t in GOROG_HEBER_MINTA.findall(forditas))
    return 'RENDBEN' if f_forras == f_forditas else 'SERTES'


def main():
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print('HIBA -- az OPENROUTER_API_KEY kornyezeti valtozo nincs beallitva', file=sys.stderr)
        return 1

    minta = {s['strong']: s for s in fordit.minta_betolt()}
    sor = minta['G1941']
    thayer = fordit.thayer_betolt()
    forras = thayer['G1941']['Teljes_szocikk']
    assert fordit.hashlib.sha1(forras.encode('utf-8')).hexdigest() == sor['forras_hash'], \
        'a forras_hash nem egyezik a mintaval'

    arak = fordit.modell_arak_betolt()
    ar = arak.get(MODELL_ID, {})
    ar_be, ar_ki = ar.get('prompt_usd_per_1M'), ar.get('completion_usd_per_1M')

    terminologia_sz = fordit.terminologia_szoveg(fordit.terminologia_betolt())
    karoli_sz = fordit.karoli_tabla_szoveg(fordit.karoli_tabla_betolt())
    with open(fordit.PROMPT_UT, encoding='utf-8') as fh:
        sablon = fh.read()

    darabok = fordit.darabokra_bont(forras)
    assert len(darabok) == 1, 'a G1941 egyetlen darabban kell legyen (< 4000 kar.)'
    prompt = fordit.prompt_epit(sablon, 'G1941', darabok[0],
                                 fordit.darab_info_szoveg(0, 1), terminologia_sz, karoli_sz)

    sorok = []
    md_reszek = ['# FORDITAS_P7_g1941_deepseek -- 3 fuggetlen ujrafuttatas (DeepSeek V4 Flash)\n']
    md_reszek.append('*A csonkolas (kor2, pontossag=0) ismetlodesenek vizsgalata -- '
                      'gyorsitotar nelkul, ugyanazzal a bemenettel.*\n')

    for i in range(1, FUTASOK + 1):
        print('=== futas %d/%d ===' % (i, FUTASOK))
        try:
            eredmeny, usage, nyers_valasz = fordit.openrouter_hivas(
                MODELL_ID, prompt, api_key, ar_bemenet_1m=ar_be, ar_kimenet_1m=ar_ki)
        except fordit.OpenRouterHiba as e:
            print('HIBA -- %s' % e)
            sorok.append({'futas': i, 'bemenet_token': '', 'kimenet_token': '',
                          'finish_reason': 'HIBA', 'koltseg_usd': '', 'hosszarany': '',
                          'gorog_heber_egyezes': '', 'json_ervenyes': 'HAMIS',
                          'forditas_hu': 'HIBA: %s' % e})
            md_reszek.append('\n---\n\n## %d. futás\n\nHIBA: %s\n' % (i, e))
            continue

        finish_reason = (nyers_valasz.get('choices') or [{}])[0].get('finish_reason')
        forditas = eredmeny['forditas_hu']
        hosszarany = len(forditas) / len(forras)
        egyezes = gorog_heber_egyezik_e(forras, forditas)
        koltseg = usage.get('cost') or 0.0

        print('  bemenet=%d kimenet=%d finish_reason=%s koltseg=%.6f hosszarany=%.2f gorog/heber=%s'
              % (usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0),
                 finish_reason, koltseg, hosszarany, egyezes))

        sorok.append({
            'futas': i,
            'bemenet_token': usage.get('prompt_tokens', 0),
            'kimenet_token': usage.get('completion_tokens', 0),
            'finish_reason': finish_reason,
            'koltseg_usd': round(koltseg, 6),
            'hosszarany': round(hosszarany, 3),
            'gorog_heber_egyezes': egyezes,
            'json_ervenyes': 'IGAZ',
            'forditas_hu': forditas,
        })
        md_reszek.append('\n---\n\n## %d. futás (finish_reason=%s, hosszarány=%.2f, 1. ellenőrzés=%s)\n\n%s\n'
                          % (i, finish_reason, hosszarany, egyezes, forditas))

    fordit.tsv_ir(KIMENET_UT, KIMENET_FEJLEC, sorok)
    print('\nirva:', KIMENET_UT)
    with open(MD_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(''.join(md_reszek))
    print('irva:', MD_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
