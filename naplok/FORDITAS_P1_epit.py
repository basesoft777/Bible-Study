#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORDITAS_P1_epit.py -- FORDITAS_PILOT_BRIEF.md v1, FP1: a 20 szocikkes minta
kivalasztasa a brief SS1. szerint (E 13, A 1, N 3, V 3) es a G5 ideiglenes
terminologia elokeszitese.

Kimenet:
  naplok/FORDITAS_P1_minta.tsv          -- strong, csoport, hossz, forras_hash
  naplok/FORDITAS_P1_arany.tsv          -- a G1941 arany forditas (kulon fajlban,
                                            a prompt ezt nem kapja meg)
  naplok/FORDITAS_P_terminologia.tsv    -- G5 indulo sorok

    python naplok/FORDITAS_P1_epit.py
"""

import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEBER_MINTA = re.compile(r'[֐-׿]')
JELZET_MINTA = re.compile(r'\b(?:L|T|Tr|WH|Rec\.)\b')


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_ir(ut, fejlec, sorok):
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(fejlec) + '\n')
        for s in sorok:
            fh.write('\t'.join(s) + '\n')


def lexikon_thayer():
    fejlec = None
    ki = []
    for m in tsv_sorok(os.path.join(REPO, 'adat', 'lexikon_hivatkozasok.tsv')):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        if r['szotar'] == 'Thayer':
            ki.append(r)
    return ki


def thayer_teljes():
    fejlec = None
    ki = {}
    for m in tsv_sorok(os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')):
        if fejlec is None:
            fejlec = m
            continue
        r = dict(zip(fejlec, m))
        ki[r['Strong_padded']] = r
    return ki


def elofordulas_gorog_strongok_hianyzo(van):
    fejlec = None
    strongok = set()
    for m in tsv_sorok(os.path.join(REPO, 'adat', 'elofordulasok.tsv')):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        szoveg = '\t'.join(m)
        for s in re.findall(r'\bG\d{4}\b', szoveg):
            strongok.add(s)
    return sorted(strongok - van)


def sha1(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


def main():
    thayer_sorok = lexikon_thayer()
    tt = thayer_teljes()

    e_csoport = sorted(r['strong'] for r in thayer_sorok if not r['forditas_hu'].strip())
    a_csoport = sorted(r['strong'] for r in thayer_sorok if r['forditas_hu'].strip())
    assert a_csoport == ['G1941'], a_csoport
    assert len(e_csoport) == 13, len(e_csoport)

    van_thayer_sor = {r['strong'] for r in thayer_sorok}
    n_csoport = elofordulas_gorog_strongok_hianyzo(van_thayer_sor)
    assert n_csoport == ['G0035', 'G0540', 'G2672'], n_csoport

    foglalt = set(e_csoport) | set(a_csoport) | set(n_csoport)

    # V1 -- <= 300 karakteres, a Strong_padded szerinti legkisebb, meg nem foglalt
    v1 = None
    for strong in sorted(tt):
        if strong in foglalt:
            continue
        if len(tt[strong]['Teljes_szocikk']) <= 300:
            v1 = strong
            break
    assert v1 is not None

    # V2 -- heber idezetet tartalmaz, a legkisebb meg nem foglalt/kivalasztott
    foglalt.add(v1)
    v2 = None
    for strong in sorted(tt):
        if strong in foglalt:
            continue
        if HEBER_MINTA.search(tt[strong]['Teljes_szocikk']):
            v2 = strong
            break
    assert v2 is not None

    # V3 -- szovegkiadas-jelzetekkel (L T Tr WH Rec.) legsurubb: a jelzetek
    # nyers elofordulasszama maximalis a meg nem foglalt szocikkek kozott,
    # a G6 sajat "hosszu szocikk" hatarara (4000 karakter) korlatozva --
    # e nelkul a legtobb jelzetet tartalmazo szocikk tobbnyire eleve a
    # leghosszabbak koze esik (pl. epi, G1909, 33067 karakter), ami a V
    # csoport "valtozatossag" celjaval szemben allna, es a G7 koltsegplafont
    # is feleslegesen terhelne. Dontetlennel a legkisebb Strong_padded.
    foglalt.add(v2)
    legjobb_szam = -1
    v3 = None
    for strong in sorted(tt):
        if strong in foglalt:
            continue
        if len(tt[strong]['Teljes_szocikk']) > 4000:
            continue
        szam = len(JELZET_MINTA.findall(tt[strong]['Teljes_szocikk']))
        if szam > legjobb_szam:
            legjobb_szam = szam
            v3 = strong
    assert v3 is not None

    v_csoport = [v1, v2, v3]

    print('E (%d): %s' % (len(e_csoport), ', '.join(e_csoport)))
    print('A (%d): %s' % (len(a_csoport), ', '.join(a_csoport)))
    print('N (%d): %s' % (len(n_csoport), ', '.join(n_csoport)))
    print('V (%d): %s' % (len(v_csoport), ', '.join(v_csoport)))
    print('  V1 (<=300 kar.): %s, hossz=%d' % (v1, len(tt[v1]['Teljes_szocikk'])))
    print('  V2 (heber idezet): %s, hossz=%d' % (v2, len(tt[v2]['Teljes_szocikk'])))
    print('  V3 (jelzet-suru, %d db): %s, hossz=%d' % (legjobb_szam, v3, len(tt[v3]['Teljes_szocikk'])))

    sorok = []
    for csoport, strongok in (('E', e_csoport), ('A', a_csoport), ('N', n_csoport), ('V', v_csoport)):
        for strong in strongok:
            szoveg = tt[strong]['Teljes_szocikk']
            sorok.append((strong, csoport, str(len(szoveg)), sha1(szoveg)))
    sorok.sort(key=lambda s: s[0])

    assert len(sorok) == 20, len(sorok)
    assert len({s[0] for s in sorok}) == 20, 'ismetlodo strong a mintaban'

    minta_ut = os.path.join(REPO, 'naplok', 'FORDITAS_P1_minta.tsv')
    tsv_ir(minta_ut, ['strong', 'csoport', 'hossz', 'forras_hash'], sorok)
    print('\nirva:', minta_ut, '(%d sor)' % len(sorok))

    # arany -- kulon fajlba, a prompt nem kapja meg
    arany_sor = next(r for r in thayer_sorok if r['strong'] == 'G1941')
    arany_ut = os.path.join(REPO, 'naplok', 'FORDITAS_P1_arany.tsv')
    tsv_ir(arany_ut, ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'forditas_hu'],
           [(arany_sor['strong'], arany_sor['szotar'], arany_sor['entry_id'],
             arany_sor['jelentes_szam'], arany_sor['forditas_hu'])])
    print('irva:', arany_ut, '(a modell ezt nem kapja meg)')

    # G5 -- ideiglenes terminologia
    terminologia = [
        ('spirit', 'szellem', 'SZOTAR S2 indulo sor', 'v1'),
        ('spiritual', 'szellemi', 'SZOTAR S2 indulo sor', 'v1'),
        ('soul', 'lélek', 'SZOTAR S2 indulo sor', 'v1'),
        ('cf.', 'vö.', 'G1941 aranybol: rovidites-feloldas (confer)', 'v1'),
        ('cl.', 'klasszikus', 'G1941 aranybol: rovidites-feloldas (classical)', 'v1'),
        ('pass.', 'szenvedő alakban', 'G1941 aranybol: rovidites-feloldas (passive)', 'v1'),
        ('sc.', 'ti.', 'G1941 aranybol: rovidites-feloldas (scilicet -> tudniillik)', 'v1'),
        ('see', 'l.', 'G1941 aranybol: rovidites-feloldas (see -> lasd)', 'v1'),
        ('Sept.', 'Septuaginta', 'G1941 aranybol: rovidites-feloldas', 'v1'),
        ('i. e.', 'azaz', 'G1941 aranybol: rovidites-feloldas (id est)', 'v1'),
        ('etc.', 'stb.', 'G1941 aranybol: rovidites-feloldas', 'v1'),
        ('p.', 'o.', 'G1941 aranybol: rovidites-feloldas (page -> oldal)', 'v1'),
        ('Heb.', 'héb.', 'G1941 aranybol: rovidites-feloldas (Hebrew -> heber)', 'v1'),
    ]
    term_ut = os.path.join(REPO, 'naplok', 'FORDITAS_P_terminologia.tsv')
    tsv_ir(term_ut, ['angol', 'magyar', 'megjegyzes', 'verzio'], terminologia)
    print('irva:', term_ut, '(%d sor)' % len(terminologia))


if __name__ == '__main__':
    main()
