#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp2/kapuk.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 4. lepes: a #3 gepi
kapuinak (naplok/FORDITAS_P4_ellenoriz.py SS1, 1-7. ellenorzes) lefuttatasa
az FP2 harom modelljenek kimenetein (fp2/forditas/<modell>/kimenet.tsv).

A naplok/FORDITAS_P4_ellenoriz.py fuggvenyeit importalja (nem masolja/modositja),
csak a beolvasast es a terminologiat cimzi at az FP2 sajat fajljaira (minta,
terminologia v3, a harom modell kimenete egyszerre).

Kimenet: fp2/kapuk.tsv (strong, csoport, modell, ellenorzes, eredmeny, reszlet)
         + osszesito stdoutra.

    python fp2/kapuk.py
"""

import importlib.util
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_spec = importlib.util.spec_from_file_location(
    'forditas_p4_ellenoriz', os.path.join(REPO, 'naplok', 'FORDITAS_P4_ellenoriz.py'))
_p4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_p4)

MINTA_UT = os.path.join(REPO, 'fp2', 'minta.tsv')
TERMINOLOGIA_UT = os.path.join(REPO, 'fp2', 'terminologia_v3.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
FORDITAS_DIR = os.path.join(REPO, 'fp2', 'forditas')
KAPUK_UT = os.path.join(REPO, 'fp2', 'kapuk.tsv')

KAPUK_FEJLEC = ['strong', 'csoport', 'modell', 'ellenorzes', 'eredmeny', 'reszlet']


def betolt():
    thayer = {r['Strong_padded']: r['Teljes_szocikk'] for r in _p4.tsv_dict_sorok(THAYER_UT)}
    karoli_halmaz = {r['Magyar rövidítés'] for r in _p4.tsv_dict_sorok(KAROLI_UT)}
    terminologia = list(_p4.tsv_dict_sorok(TERMINOLOGIA_UT))
    csoport = {r['strong']: r['csoport'] for r in _p4.tsv_dict_sorok(MINTA_UT)}
    return thayer, karoli_halmaz, terminologia, csoport


def main():
    thayer, karoli_halmaz, terminologia, csoport = betolt()

    sorok = []
    for model_slug in sorted(os.listdir(FORDITAS_DIR)):
        kimenet_ut = os.path.join(FORDITAS_DIR, model_slug, 'kimenet.tsv')
        if not os.path.exists(kimenet_ut):
            continue
        kimenet = list(_p4.tsv_dict_sorok(kimenet_ut))
        for r in kimenet:
            strong = r['strong']
            modell = r['modell']
            forras = thayer.get(strong, '')
            forditas = r['forditas_hu']
            cs = csoport.get(strong, '?')

            if forditas.startswith('HIBA:'):
                for nev in ('1_gorog_heber', '2_versszam', '3_karoli_roviditesek',
                            '4_formazas', '5_terminologia', '6_hosszarany', '7_json_sema'):
                    sorok.append({'strong': strong, 'csoport': cs, 'modell': modell,
                                  'ellenorzes': nev, 'eredmeny': 'HIBA', 'reszlet': forditas})
                continue

            sorok.append({'strong': strong, 'csoport': cs, 'modell': modell,
                          'ellenorzes': '7_json_sema', 'eredmeny': 'RENDBEN', 'reszlet': ''})

            bizonytalan_lista = []  # FP2-ben a bizonytalan_feloldasok kulon fajlban van,
                                      # de a kapu csak jelzesre hasznalja -- itt ures listaval
                                      # a legszigorubb (0 kivetel) ellenorzes fut

            for nev, fv in (
                ('1_gorog_heber', lambda: _p4.ellenoriz_1_gorog_heber(forras, forditas)),
                ('2_versszam', lambda: _p4.ellenoriz_2_versszam(forras, forditas)),
                ('3_karoli_roviditesek', lambda: _p4.ellenoriz_3_karoli_roviditesek(forditas, karoli_halmaz)),
                ('4_formazas', lambda: _p4.ellenoriz_4_formazas(forras, forditas)),
                ('5_terminologia', lambda: _p4.ellenoriz_5_terminologia(forras, forditas, terminologia, bizonytalan_lista)),
                ('6_hosszarany', lambda: _p4.ellenoriz_6_hosszarany(forras, forditas)),
            ):
                eredmeny, reszlet = fv()
                sorok.append({'strong': strong, 'csoport': cs, 'modell': modell,
                              'ellenorzes': nev, 'eredmeny': eredmeny, 'reszlet': reszlet})

    _p4.tsv_ir(KAPUK_UT, KAPUK_FEJLEC, sorok)
    print('irva: %s (%d sor)' % (KAPUK_UT, len(sorok)))

    pass_fail_nevek = {'1_gorog_heber', '2_versszam', '3_karoli_roviditesek',
                        '4_formazas', '5_terminologia', '7_json_sema'}
    modellenkent = {}
    for s in sorok:
        if s['ellenorzes'] not in pass_fail_nevek:
            continue
        m = s['modell']
        d = modellenkent.setdefault(m, {'RENDBEN': 0, 'SERTES': 0, 'HIBA': 0})
        d[s['eredmeny']] = d.get(s['eredmeny'], 0) + 1

    print('\n=== atmenesi arany modellenkent (1,2,3,4,5,7 ellenorzes egyutt) ===')
    for m in sorted(modellenkent):
        d = modellenkent[m]
        print('  %-32s RENDBEN %3d | SERTES %3d | HIBA %3d | atmeneti arany %.1f%%'
              % (m, d['RENDBEN'], d['SERTES'], d['HIBA'],
                 100.0 * d['RENDBEN'] / (d['RENDBEN'] + d['SERTES']) if (d['RENDBEN'] + d['SERTES']) else 0.0))


if __name__ == '__main__':
    main()
