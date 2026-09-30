#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fp2/mintavalaszto.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 1. lepes: 30 szocikkes
minta a Gemini/DeepSeek/MiniMax osszevetesehez.

Osszetetel:
  - 20 szocikk: a kor2 (F03_FORDITAS_PILOT_BRIEF.md FP1) ugyanazon 20 szocikke, valtozatlanul
    (naplok/FORDITAS_P1_minta.tsv) -- ezen a Gemini es a DeepSeek v1/v3 kimenete kozvetlenul
    osszevetheto.
  - 10 uj szocikk: retegzett, rogzitett seed-del (20260926, ugyanaz, mint a
    FORDITAS_ELES_THAYER_BRIEF.md E6 mintajaban), a kor2 20 szocikkenek kizarasaval:
      3 rovid  (hossz <= 300 kar.)
      4 kozepes (300 < hossz <= 2000 kar.)
      3 hosszu (hossz > 2000 kar.)
    A hosszhatarok a FORDITAS_ELES_THAYER_BRIEF.md E6 mintajaval egyeznek (<=300 / 300-2000 / >2000).
    Legalabb 3 teologiailag sulyos szo (manualisan megnevezett jelolt-halmaz, alant
    dokumentalva -- ez SZERKESZTOI dontes, nem lekerdezes eredmenye, a CLAUDE.md 3.
    szabalya szerint jelolve).

Kimenet: fp2/minta.tsv (strong, csoport, hossz_kategoria, sulyos, hossz, forras_hash)
         es stdout indoklas.

    python fp2/mintavalaszto.py
"""

import hashlib
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
KOR2_MINTA_UT = os.path.join(REPO, 'naplok', 'FORDITAS_P1_minta.tsv')
KIMENET_UT = os.path.join(REPO, 'fp2', 'minta.tsv')

SEED = 20260926  # ugyanaz, mint a FORDITAS_ELES_THAYER_BRIEF.md E6 mintaja

# Teologiailag sulyos jelolt-halmaz -- SZERKESZTOI valasztas (nem lekerdezes), a
# szokveny szerint gyakran targyalt uj-szovetsegi alapfogalmak. A vegleges 10-be csak
# az kerul, ami (a) megvan a Thayer_teljes.tsv-ben, (b) nincs a kor2 20 szocikke kozott.
SULYOS_JELOLTEK = {
    'G0026': 'agape (szeretet)',
    'G2316': 'theos (Isten)',
    'G4102': 'pistis (hit)',
    'G1343': 'dikaiosyne (igazsag/megigazulas)',
    'G5485': 'charis (kegyelem)',
    'G0266': 'hamartia (bun)',
    'G3341': 'metanoia (megterés)',
    'G4991': 'soteria (udvosseg)',
    'G2222': 'zoe (elet)',
    'G1391': 'doxa (dicsoseg)',
}


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def thayer_betolt():
    fejlec = None
    ki = {}
    for m in tsv_sorok(THAYER_UT):
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        ki[r['Strong_padded']] = r
    return ki


def kor2_strongok():
    fejlec = None
    ki = []
    for m in tsv_sorok(KOR2_MINTA_UT):
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        ki.append(r['strong'])
    return ki


def hossz_kategoria(h):
    if h <= 300:
        return 'rovid'
    if h <= 2000:
        return 'kozepes'
    return 'hosszu'


def forras_hash(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


def main():
    thayer = thayer_betolt()
    kor2 = kor2_strongok()
    kor2_halmaz = set(kor2)

    print('=== kor2 20 szocikke (valtozatlanul atveve) ===')
    for s in kor2:
        print(' ', s)

    jelolt_halmaz = {s: t for s, t in thayer.items() if s not in kor2_halmaz}

    # sulyos jeloltek szurese: megvan-e a Thayerben
    sulyos_elerheto = {s: c for s, c in SULYOS_JELOLTEK.items() if s in jelolt_halmaz}
    sulyos_hianyzo = [s for s in SULYOS_JELOLTEK if s not in jelolt_halmaz]
    print('\n=== teologiailag sulyos jeloltek ===')
    for s, cim in SULYOS_JELOLTEK.items():
        elerheto = s in jelolt_halmaz
        print('  %s %-35s elerheto=%s%s' % (s, cim, elerheto,
              ' (a kor2-ben mar szerepel)' if s in kor2_halmaz else ''))
    if sulyos_hianyzo:
        print('  HIANYZIK a Thayer_teljes.tsv-bol:', ', '.join(sulyos_hianyzo))

    # bucketek: minden Thayer-strong (a kor2-n kivul) kategoriaba sorolasa
    bucketek = {'rovid': [], 'kozepes': [], 'hosszu': []}
    for s, r in jelolt_halmaz.items():
        h = len(r['Teljes_szocikk'])
        bucketek[hossz_kategoria(h)].append(s)

    rnd = random.Random(SEED)
    for k in bucketek:
        bucketek[k].sort()  # determinisztikus alap-sorrend a shuffle elott
        rnd.shuffle(bucketek[k])

    # celszamok bucketenkent
    cel = {'rovid': 3, 'kozepes': 4, 'hosszu': 3}
    kivalasztott = []

    # elobb a legalabb 3 sulyos szot biztositjuk, a sajat bucketjukbe helyezve,
    # a bucket elejere (a shuffle utani legelso, determinisztikus pozicion)
    sulyos_kivalasztott = []
    for s in sorted(sulyos_elerheto):  # determinisztikus bejaras
        kat = hossz_kategoria(len(thayer[s]['Teljes_szocikk']))
        if len(sulyos_kivalasztott) >= 3:
            break
        if bucketek[kat].count(s) and len([x for x in sulyos_kivalasztott if x[1] == kat]) < cel[kat]:
            sulyos_kivalasztott.append((s, kat))

    for s, kat in sulyos_kivalasztott:
        kivalasztott.append((s, kat, True))
        bucketek[kat].remove(s)

    for kat, darab in cel.items():
        mar_van = len([x for x in kivalasztott if x[1] == kat])
        hianyzik = darab - mar_van
        for s in bucketek[kat][:hianyzik]:
            kivalasztott.append((s, kat, s in SULYOS_JELOLTEK))

    kivalasztott.sort(key=lambda x: x[0])

    print('\n=== kivalasztott 10 uj szocikk ===')
    for s, kat, sulyos_e in kivalasztott:
        h = len(thayer[s]['Teljes_szocikk'])
        print('  %-8s %-8s hossz=%6d sulyos=%s' % (s, kat, h, sulyos_e))

    assert len(kivalasztott) == 10, 'nem sikerult 10 uj szocikket valasztani: %d' % len(kivalasztott)
    assert len(set(s for s, _, _ in kivalasztott)) == 10, 'duplikatum a kivalasztasban'
    assert sum(1 for _, _, sulyos_e in kivalasztott if sulyos_e) >= 3, 'kevesebb mint 3 sulyos szo'
    assert sum(1 for _, kat, _ in kivalasztott if kat == 'rovid') == 3
    assert sum(1 for _, kat, _ in kivalasztott if kat == 'kozepes') == 4
    assert sum(1 for _, kat, _ in kivalasztott if kat == 'hosszu') == 3

    sorok = []
    for s in kor2:
        h = len(thayer[s]['Teljes_szocikk'])
        sorok.append({
            'strong': s, 'csoport': 'kor2',
            'hossz_kategoria': hossz_kategoria(h) if s != 'G1941' else 'arany',
            'sulyos': 'nem', 'hossz': h, 'forras_hash': forras_hash(thayer[s]['Teljes_szocikk']),
        })
    for s, kat, sulyos_e in kivalasztott:
        h = len(thayer[s]['Teljes_szocikk'])
        sorok.append({
            'strong': s, 'csoport': 'uj',
            'hossz_kategoria': kat, 'sulyos': 'igen' if sulyos_e else 'nem',
            'hossz': h, 'forras_hash': forras_hash(thayer[s]['Teljes_szocikk']),
        })

    fejlec = ['strong', 'csoport', 'hossz_kategoria', 'sulyos', 'hossz', 'forras_hash']
    os.makedirs(os.path.dirname(KIMENET_UT), exist_ok=True)
    with open(KIMENET_UT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(fejlec) + '\n')
        for sor in sorok:
            fh.write('\t'.join(str(sor[m]) for m in fejlec) + '\n')

    print('\nirva: %s (%d sor)' % (KIMENET_UT, len(sorok)))


if __name__ == '__main__':
    main()
