#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/kapu_keresztellenorzes.py -- a felhasznalo elozetes (kulcs-nyitas elotti)
ket kerdesehez: (1) a fp2/kapuk.tsv es a temenyleges (nem anonimizalt)
fp2/forditas/<modell>/kimenet.tsv keresztellenorzese a kritikusnak talalt
szocikkeken; (2) a fordit.py darabolasi mechanizmusanak dokumentalasa."""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORDITAS_DIR = os.path.join(REPO, 'fp2', 'forditas')
KAPUK_UT = os.path.join(REPO, 'fp2', 'kapuk.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')


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
    thayer = {r['Strong_padded']: len(r['Teljes_szocikk']) for r in tsv_dict_sorok(THAYER_UT)}
    kapuk = list(tsv_dict_sorok(KAPUK_UT))

    modellek = {}
    for model_slug in sorted(os.listdir(FORDITAS_DIR)):
        ut = os.path.join(FORDITAS_DIR, model_slug, 'kimenet.tsv')
        if os.path.exists(ut):
            modellek[model_slug] = {r['strong']: r for r in tsv_dict_sorok(ut)}

    kritikus_strongok = ['G0002', 'G0012', 'G0086', 'G0994', 'G1311', 'G1941',
                          'G1944', 'G2672', 'G3777', 'G4151', 'G5010', 'G5351',
                          'G5356', 'G5590', 'G0026', 'G0266', 'G1106', 'G1343', 'G5013']

    for strong in kritikus_strongok:
        forras_hossz = thayer.get(strong, 0)
        print('\n=== %s (forras hossz=%d) ===' % (strong, forras_hossz))
        for model_slug in sorted(modellek):
            sor_adat = modellek[model_slug].get(strong, {})
            forditas = sor_adat.get('forditas_hu', '')
            model_id = sor_adat.get('modell', model_slug)
            arany = len(forditas) / forras_hossz if forras_hossz else 0
            sorok = [k for k in kapuk if k['strong'] == strong and k['modell'] == model_id]
            eredmenyek = {k['ellenorzes']: k['eredmeny'] for k in sorok}
            print('  %-32s forditas_hossz=%6d arany=%.2f | 1=%s 2=%s 3=%s 4=%s 5=%s 6=%s 7=%s'
                  % (model_slug, len(forditas), arany,
                     eredmenyek.get('1_gorog_heber', '?'), eredmenyek.get('2_versszam', '?'),
                     eredmenyek.get('3_karoli_roviditesek', '?'), eredmenyek.get('4_formazas', '?'),
                     eredmenyek.get('5_terminologia', '?'), eredmenyek.get('6_hosszarany', '?'),
                     eredmenyek.get('7_json_sema', '?')))


if __name__ == '__main__':
    main()
