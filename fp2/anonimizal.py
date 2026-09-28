#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp2/anonimizal.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 5. lepes:
szocikkenkent veletlenszeruen (rogzitett seeddel) A/B/C cimkere rendeli a
harom modell kimenetet.

Kimenet:
  fp2/anonim_kulcs.tsv   -- strong, cimke, modell (ezt a biralat vegeig nem
                            szabad megnyitni/beolvasni)
  fp2/biralando.md       -- forras + A/B/C forditas szocikkenkent, modellnev
                            NELKUL, a vak biralathoz

    python fp2/anonimizal.py
"""

import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORDITAS_DIR = os.path.join(REPO, 'fp2', 'forditas')
MINTA_UT = os.path.join(REPO, 'fp2', 'minta.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
KULCS_UT = os.path.join(REPO, 'fp2', 'anonim_kulcs.tsv')
BIRALANDO_UT = os.path.join(REPO, 'fp2', 'biralando.md')

SEED = 20260928  # FP2 sajat, rogzitett seed (kulonbozik a mintavalasztoetol)


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


def main():
    minta = list(tsv_dict_sorok(MINTA_UT))
    thayer = {r['Strong_padded']: r['Teljes_szocikk'] for r in tsv_dict_sorok(THAYER_UT)}

    modellek_kimenete = {}  # model_slug -> {strong: forditas_hu}
    for model_slug in sorted(os.listdir(FORDITAS_DIR)):
        ut = os.path.join(FORDITAS_DIR, model_slug, 'kimenet.tsv')
        if not os.path.exists(ut):
            continue
        modellek_kimenete[model_slug] = {r['strong']: r for r in tsv_dict_sorok(ut)}

    model_slugok = sorted(modellek_kimenete)
    assert len(model_slugok) == 3, 'harom modell kimenetet varunk, talalt: %r' % model_slugok

    rnd = random.Random(SEED)
    kulcs_sorok = []
    biralando_reszek = []

    for sor in minta:
        strong = sor['strong']
        cimkek = ['A', 'B', 'C']
        sorrend = list(model_slugok)
        rnd.shuffle(sorrend)
        cimke_modell = dict(zip(cimkek, sorrend))
        for cimke, model_slug in cimke_modell.items():
            kulcs_sorok.append({'strong': strong, 'cimke': cimke, 'modell': model_slug})

        forras = thayer.get(strong, '(HIANYZIK A THAYERBOL)')
        resz = ['## %s\n' % strong, '**Forrás (Thayer, angol):**\n', forras, '']
        for cimke in cimkek:
            model_slug = cimke_modell[cimke]
            forditas = modellek_kimenete[model_slug][strong]['forditas_hu']
            resz.append('**%s:**\n' % cimke)
            resz.append(forditas)
            resz.append('')
        biralando_reszek.append('\n'.join(resz))

    with open(KULCS_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('strong\tcimke\tmodell\n')
        for r in kulcs_sorok:
            fh.write('%s\t%s\t%s\n' % (r['strong'], r['cimke'], r['modell']))
    print('irva: %s (%d sor) -- A BIRALAT VEGEIG NE OLVASD BE' % (KULCS_UT, len(kulcs_sorok)))

    with open(BIRALANDO_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# FP2 -- vak biralando csomag\n\n')
        fh.write('*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 5. lepes. Modellnev nelkul, '
                  'cimke: A/B/C, szocikkenkent veletlenszeruen ujrarendezve '
                  '(seed=%d).*\n\n' % SEED)
        fh.write('\n\n---\n\n'.join(biralando_reszek))
    print('irva: %s (%d szocikk)' % (BIRALANDO_UT, len(minta)))


if __name__ == '__main__':
    main()
