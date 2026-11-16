# -*- coding: utf-8 -*-
"""F224.13, C-futás (Opus): a többlet-jelzések vak mintája, a 2. körrel azonos módszerrel.

A sokaság: az Opus nem „igazolt” ítéletei, amelyeket a lektori listák
(naplok/KIADAS_HAMART-001_lektor.md 1–46; naplok/KIADAS_ISTENTISZT-001_lektor_2kiadas.md 1–22;
naplok/ALLITAS_ISTENTISZT-001_atnezes.md 9 HIBA) nem fednek. A fedés kijelölése kézi
(naplok/F224_proba.md 7. szakasz); itt csak a rögzített sokaság és a húzás áll.
"""
import sys, random
sys.stdout.reconfigure(encoding='utf-8')

SOKASAG = ['HAM-K2', 'HAM-K3', 'HAM-K9', 'HAM-K21', 'HAM-K30', 'HAM-K46', 'HAM-K48',
           'HAM-K57', 'HAM-K60', 'HAM-K64', 'HAM-K87', 'HAM-K88', 'HAM-K89', 'HAM-K90',
           'HAM-K94', 'HAM-K95', 'HAM-K97', 'HAM-K99', 'HAM-K100', 'HAM-K101', 'HAM-K107',
           'HAM-K108', 'HAM-K110', 'IST-K12', 'IST-K37']
print(len(SOKASAG), 'tétel a sokaságban')
print('minta:', sorted(random.Random(224).sample(SOKASAG, 12), key=lambda x: (x[:3], int(x[5:]))))
