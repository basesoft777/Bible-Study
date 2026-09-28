#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp2/rendezo.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 4. lepes: a fp2/_run/
gyorsitotarabol (JSON, biztonsagos, nem sertett) allitja ossze a modellenkenti
kimenetet -- NEM a naplok/FORDITAS_P3-mintajara irt fp2/_run/kimenet.tsv-bol,
mert abban SERULT sorok vannak (l. "Talalt hibak a #3 eszkozeiben",
naplok/FP2_felmeres.md): a fordit.py tsv_ir/tsv_sorok parja split('\n')/
'\n'.join()-nal olvas/ir, es nem kezeli, ha egy mezo (forditas_hu) maga is
tartalmaz sortores karaktert (a JSON-valaszban escapelt "\n", amit a
json.loads mar valodi sortoresse alakitott at) -- ez nem uj hiba, csak most
eloszor volt eleg hosszu/tobbsoros forditas ahhoz, hogy manifesztalodjon.

Kimenet:
  fp2/forditas/<modell_slug>/kimenet.tsv  -- a KIMENET_FEJLEC semaja szerint,
      csoportonkent/darabonkent helyesen osszeillesztve
  fp2/futasnaplo.tsv                       -- fp2/_run/koltseg.tsv atmasolva
      (az a fajl NEM serult -- csak szamokat es rovid cimkeket tartalmaz)

    python fp2/rendezo.py
"""

import json
import os
import re
import sys
from datetime import date

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(REPO, 'fp2', '_run', 'cache')
KOLTSEG_UT = os.path.join(REPO, 'fp2', '_run', 'koltseg.tsv')
MINTA_UT = os.path.join(REPO, 'fp2', 'minta.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
FUTASNAPLO_UT = os.path.join(REPO, 'fp2', 'futasnaplo.tsv')
FORDITAS_DIR = os.path.join(REPO, 'fp2', 'forditas')

KIMENET_FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo',
                   'forras_hash', 'forditas_hu', 'allapot', 'modell', 'datum',
                   'terminologia_verzio']


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


def tsv_ir(ut, fejlec, sorok):
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(fejlec) + '\n')
        for sor in sorok:
            # a forditas_hu mezoben talalhato sortoreseket szokozre cserejuk,
            # hogy a kimeneti TSV maga ne legyen ismet sertett (l. a modul
            # docstringjeben leirt hiba) -- ez CSAK a kimeneti fajlt vedi,
            # a fp2/forditas/*.md olvashato mintaban a sortores megmarad
            ertekek = []
            for mezo in fejlec:
                ertek = str(sor.get(mezo, ''))
                ertek = ertek.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ')
                ertekek.append(ertek)
            fh.write('\t'.join(ertekek) + '\n')


def minta_csoport():
    return {r['strong']: r for r in tsv_dict_sorok(MINTA_UT)}


def thayer_betolt():
    return {r['Strong_padded']: r for r in tsv_dict_sorok(THAYER_UT)}


def cache_beolvas():
    """visszaad: {(model_slug, strong): {darab_index: cache_adat}}"""
    eredmeny = {}
    for model_slug in sorted(os.listdir(CACHE_DIR)):
        modell_dir = os.path.join(CACHE_DIR, model_slug)
        if not os.path.isdir(modell_dir):
            continue
        for fn in sorted(os.listdir(modell_dir)):
            if not fn.endswith('.json'):
                continue
            m = re.match(r'^(.+)_(\d+)\.json$', fn)
            if not m:
                print('FIGYELEM -- nem illeszkedo fajlnev: %s' % fn, file=sys.stderr)
                continue
            strong, darab_index = m.group(1), int(m.group(2))
            with open(os.path.join(modell_dir, fn), encoding='utf-8') as fh:
                adat = json.load(fh)
            eredmeny.setdefault((model_slug, strong), {})[darab_index] = adat
    return eredmeny


def main():
    minta = minta_csoport()
    thayer = thayer_betolt()
    cache = cache_beolvas()
    ma = date.today().isoformat()

    modellenkent = {}
    hianyzo = []
    for (model_slug, strong), darabok in sorted(cache.items()):
        if strong not in minta:
            continue  # ez a modell-cache mas futasbol is szarmazhat
        db_szam = max(darabok) + 1
        hianyzo_e = [i for i in range(db_szam) if i not in darabok]
        if hianyzo_e:
            hianyzo.append((model_slug, strong, hianyzo_e))
            continue
        model_id = darabok[0]['model']
        forditas_reszek = [darabok[i]['eredmeny']['forditas_hu'] for i in range(db_szam)]
        forditas_hu = ' '.join(forditas_reszek)
        t = thayer.get(strong, {})
        sor = {
            'szotar': 'Thayer', 'strong': strong, 'entry_id': t.get('Strong_eredeti', strong),
            'jelentes_szam': 'teljes', 'mezo': 'forditas_hu',
            'forras_hash': darabok[0]['forras_hash'], 'forditas_hu': forditas_hu,
            'allapot': 'pilot', 'modell': model_id, 'datum': ma,
            'terminologia_verzio': darabok[0]['terminologia_verzio'],
        }
        modellenkent.setdefault(model_slug, []).append(sor)

    if hianyzo:
        print('FIGYELEM -- hianyos darabsorozat (kihagyva):')
        for model_slug, strong, hi in hianyzo:
            print('  %s %s hianyzo darabok: %s' % (model_slug, strong, hi))

    for model_slug, sorok in sorted(modellenkent.items()):
        sorok.sort(key=lambda s: s['strong'])
        ut = os.path.join(FORDITAS_DIR, model_slug, 'kimenet.tsv')
        tsv_ir(ut, KIMENET_FEJLEC, sorok)
        print('irva: %s (%d sor)' % (ut, len(sorok)))
        hianyzo_strongok = sorted(set(minta) - {s['strong'] for s in sorok})
        if hianyzo_strongok:
            print('  HIANYZIK a mintabol: %s' % ', '.join(hianyzo_strongok))

    # futasnaplo: a koltseg.tsv egyszeru atmasolasa (nem serult fajl)
    koltseg_sorok = list(tsv_dict_sorok(KOLTSEG_UT))
    with open(KOLTSEG_UT, encoding='utf-8') as fh:
        fejlec = fh.readline().rstrip('\n').split('\t')
    tsv_ir(FUTASNAPLO_UT, fejlec, koltseg_sorok)
    print('irva: %s (%d sor)' % (FUTASNAPLO_UT, len(koltseg_sorok)))


if __name__ == '__main__':
    main()
