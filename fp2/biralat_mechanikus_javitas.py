#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/biralat_mechanikus_javitas.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, a
felhasznalo kiegeszito 3. kerdese: a G0266-korrekcio szabalyat (hosszarany < 0.8
VAGY gorog/heber-paritas SERTES = kritikus kihagyas) GEPIESEN alkalmazza mind a
90 kimenetre. Az eredeti (szubjektiv, olvasason alapulo) pontszamot es
hibabesorolast KULON oszlopban megtartja -- ez a lepes NEM irja felul azokat,
csak egy MASODIK, mechanikus ellenorzest ad melle.

    python fp2/biralat_mechanikus_javitas.py
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'fp2'))
from biralat_adatok import sorok_dict  # noqa: E402

KULCS_UT = os.path.join(REPO, 'fp2', 'anonim_kulcs.tsv')
KAPUK_UT = os.path.join(REPO, 'fp2', 'kapuk.tsv')
KIMENET_UT = os.path.join(REPO, 'fp2', 'biralat_vegleges.tsv')

FEJLEC = ['strong', 'cimke', 'modell', 'eredeti_osszesen', 'eredeti_hibak',
          'hosszarany', 'gorogheber_kapu', 'mechanikus_kritikus', 'valtozott_e']


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


def _slug_to_model_id():
    """a fp2/forditas/<slug>/kimenet.tsv sajat 'modell' oszlopabol nyeri ki a
    valodi (kapuk.tsv-ben is hasznalt) model-azonositot, mert az anonim_kulcs.tsv
    a mappa-szeletet (pl. 'deepseek_deepseek-v4-flash'), a kapuk.tsv viszont a
    valodi azonositot (pl. 'deepseek/deepseek-v4-flash') hasznalja."""
    terkep = {}
    forditas_dir = os.path.join(REPO, 'fp2', 'forditas')
    for slug in os.listdir(forditas_dir):
        ut = os.path.join(forditas_dir, slug, 'kimenet.tsv')
        if not os.path.exists(ut):
            continue
        for r in tsv_dict_sorok(ut):
            terkep[slug] = r['modell']
            break
    return terkep


def main():
    slug_terkep = _slug_to_model_id()
    kulcs = {(r['strong'], r['cimke']): slug_terkep[r['modell']] for r in tsv_dict_sorok(KULCS_UT)}
    kapuk = list(tsv_dict_sorok(KAPUK_UT))

    hosszarany = {}
    gorogheber = {}
    for k in kapuk:
        key = (k['strong'], k['modell'])
        if k['ellenorzes'] == '6_hosszarany':
            m = re.match(r'^([\d.]+)', k['reszlet'])
            if m:
                hosszarany[key] = float(m.group(1))
        elif k['ellenorzes'] == '1_gorog_heber':
            gorogheber[key] = k['eredmeny']

    sorok = list(sorok_dict())
    eltero = 0
    for r in sorok:
        modell = kulcs[(r['strong'], r['cimke'])]
        key = (r['strong'], modell)
        arany = hosszarany.get(key)
        gh = gorogheber.get(key, '?')
        mech_kritikus = (arany is not None and arany < 0.8) or gh == 'SERTES'
        eredeti_kritikus = 'kritikus' in r['hibak']
        valtozott = mech_kritikus != eredeti_kritikus
        if valtozott:
            eltero += 1
        r['modell'] = modell
        r['hosszarany'] = arany if arany is not None else ''
        r['gorogheber_kapu'] = gh
        r['mechanikus_kritikus'] = 'igen' if mech_kritikus else 'nem'
        r['valtozott_e'] = 'igen' if valtozott else 'nem'
        r['eredeti_osszesen'] = r['osszesen']
        r['eredeti_hibak'] = r['hibak'] or '(nincs)'

    with open(KIMENET_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(FEJLEC) + '\n')
        for r in sorok:
            fh.write('\t'.join(str(r[m]) for m in FEJLEC) + '\n')

    print('irva: %s (%d sor)' % (KIMENET_UT, len(sorok)))
    print('eltero minositesu sor (a mechanikus szabaly mast mond, mint az eredeti olvasas): %d/%d'
          % (eltero, len(sorok)))
    print('\n=== eltero sorok ===')
    for r in sorok:
        if r['valtozott_e'] == 'igen':
            print('  %-8s %s (%-32s) eredeti=%-20s hosszarany=%-6s gorogheber=%-8s mechanikus_kritikus=%s'
                  % (r['strong'], r['cimke'], r['modell'], r['eredeti_hibak'],
                     r['hosszarany'], r['gorogheber_kapu'], r['mechanikus_kritikus']))


if __name__ == '__main__':
    main()
