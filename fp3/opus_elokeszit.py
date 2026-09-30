#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp3/opus_elokeszit.py -- F27_FP3_BRIEF.md P4 elokeszites: az fp3/minta.tsv 40 szocikkehez
darabonkent (az eszkozok/fordit.py darabokra_bont hatarával, 4000 kar.) elkesziti a
teljes promptot (fp3/prompt_v4.md + fp2/terminologia_v3.tsv + Karoli-tabla) --
ugyanazt, amit a fordit.py a Gemininek kuld. A prompt a Gemini/mas kimenetet nem tartalmazza.

Kimenet: fp3/_run/opus/bemenet/<strong>_<darab>.md   (a subagent ezt olvassa)
         fp3/_run/opus/bemenet/_lista.tsv            (strong, darabszam)

    python fp3/opus_elokeszit.py
"""

import importlib.util
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = importlib.util.spec_from_file_location('fordit', os.path.join(REPO, 'eszkozok', 'fordit.py'))
F = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(F)

BEMENET = os.path.join(REPO, 'fp3', '_run', 'opus', 'bemenet')


def main():
    os.makedirs(BEMENET, exist_ok=True)
    minta = F.minta_betolt(os.path.join(REPO, 'fp3', 'minta.tsv'))
    thayer = F.thayer_betolt()
    term = F.terminologia_szoveg(F.terminologia_betolt(os.path.join(REPO, 'fp2', 'terminologia_v3.tsv')))
    karoli = F.karoli_tabla_szoveg(F.karoli_tabla_betolt())
    with open(os.path.join(REPO, 'fp3', 'prompt_v4.md'), encoding='utf-8') as fh:
        sablon = fh.read()
    lista = []
    for sor in minta:
        strong = sor['strong']
        darabok = F.darabokra_bont(thayer[strong]['Teljes_szocikk'])
        for i, d in enumerate(darabok):
            p = F.prompt_epit(sablon, strong, d, F.darab_info_szoveg(i, len(darabok)), term, karoli)
            with open(os.path.join(BEMENET, '%s_%d.md' % (strong, i)), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(p)
        lista.append((strong, len(darabok)))
    with open(os.path.join(BEMENET, '_lista.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('strong\tdarab\n')
        for s, n in lista:
            fh.write('%s\t%d\n' % (s, n))
    print('%d szocikk, %d darab; darabolt: %s' % (len(lista), sum(n for _, n in lista),
          [(s, n) for s, n in lista if n > 1]))


if __name__ == '__main__':
    main()
