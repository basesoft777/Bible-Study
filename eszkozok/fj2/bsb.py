#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb.py -- F06 3. lepes, BSB (N30): a teljes 1Mozes versenkenti Strong-osszevetese a TAHOT-tal.

A kuszob es az egyezes-definicio MERES ELOTT rogzitett, az eszkozok/fj2/kuszob.txt-ben
(a felhasznalo valasza a brief 2. lepesenel); a szkript a fajl nelkul nem fut, es a
kuszobot nem modositja. Formatum (kulcs=ertek soronkent):
    kuszob=95
    definicio=tahot_resze_bsb        (a TAHOT-halmaz reszhalmaza a BSB-halmaznak)
    nevezo=tahot_lefedett_versek     (a TAHOT-tal nem rendelkezo versek kulon listan, nem elteres)
A 9000-es (es afeletti) STEPBible-prefixkodok kimaradnak (kozos.tahot_strongok).

Kimenet: naplok/F06_bsb_genezis.tsv (versenkent), naplok/F06_bsb_elteresek.tsv (a nem egyezok).
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

URL = 'https://github.com/BSB-publishing/bsb-data-output'
KUSZOB_UT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kuszob.txt')


def kuszob_olvas():
    if not os.path.exists(KUSZOB_UT):
        raise SystemExit('HIBA: nincs eszkozok/fj2/kuszob.txt -- a brief 2. lepese (a BSB-kuszob rogzitese) meg nem tortent')
    ertek = {}
    with open(KUSZOB_UT, encoding='utf-8') as f:
        for sor in f:
            sor = sor.strip()
            if sor and not sor.startswith('#') and '=' in sor:
                k, v = sor.split('=', 1)
                ertek[k.strip()] = v.strip()
    for k in ('kuszob', 'definicio', 'nevezo'):
        if k not in ertek:
            raise SystemExit('HIBA: kuszob.txt hianyzo kulcs: ' + k)
    if ertek['definicio'] not in ('tahot_resze_bsb', 'azonos_halmaz'):
        raise SystemExit('HIBA: ismeretlen definicio: ' + ertek['definicio'])
    return float(ertek['kuszob']), ertek['definicio'], ertek['nevezo']


def bsb_vers_strongok(adat):
    """{vers_szam(int): halmaz(int Strong)} egy fejezet-JSON-bol."""
    szotar = adat.get('eng') if isinstance(adat, dict) and isinstance(adat.get('eng'), dict) else adat
    ki = {}
    for vs, spanok in szotar.items():
        if not str(vs).isdigit():
            continue
        h = set()
        for span in spanok:
            if isinstance(span, (list, tuple)) and len(span) >= 2 and span[1]:
                for m in re.finditer(r'H0*(\d+)', json.dumps(span[1])):
                    h.add(int(m.group(1)))
        ki[int(vs)] = h
    return ki


def fut(munka, parancs):
    kuszob, definicio, nevezo = (95.0, 'tahot_resze_bsb', 'tahot_lefedett_versek') if kozos.SZARAZ else kuszob_olvas()
    cel = os.path.join(munka, 'bsb-data-output')
    commit, hiba = kozos.klonoz(URL, cel)
    if not commit:
        raise SystemExit('HIBA: a BSB nem toltheto le: %s' % hiba)
    if kozos.SZARAZ:
        print('bsb: szaraz futas, kuszob=%s definicio=%s nevezo=%s' % (kuszob, definicio, nevezo))
        return
    tahot = kozos.tahot_strongok()
    mappa = os.path.join(cel, 'base', 'display', 'GEN')
    fejezetek = sorted(int(m.group(1)) for fn in os.listdir(mappa) for m in [re.fullmatch(r'GEN(\d+)\.json', fn)] if m)
    sorok, elteresek = [], []
    osszes = tahot_van = egyezo = 0
    jaccard_osszeg = 0.0
    for fej in fejezetek:
        with open(os.path.join(mappa, 'GEN%d.json' % fej), encoding='utf-8') as f:
            bsb = bsb_vers_strongok(json.load(f))
        for vs in sorted(bsb):
            osszes += 1
            ref = '1Móz %d:%d' % (fej, vs)
            b = bsb[vs]
            t = tahot.get(ref)
            if t is None:
                sorok.append((ref, '', str(len(b)), '', 'nincs_tahot', ''))
                elteresek.append((ref, 'nincs_tahot', '', ''))
                continue
            tahot_van += 1
            kozos_h = t & b
            if definicio == 'tahot_resze_bsb':
                egyezik = t <= b
            else:
                egyezik = t == b
            jacc = 100.0 * len(kozos_h) / len(t | b) if (t | b) else 100.0
            jaccard_osszeg += jacc
            if egyezik:
                egyezo += 1
            else:
                elteresek.append((ref, 'tahot_nincs_a_bsb-ben' if definicio == 'tahot_resze_bsb' else 'halmaz_elter',
                                  ','.join(map(str, sorted(t - b))), ','.join(map(str, sorted(b - t)))))
            sorok.append((ref, str(len(t)), str(len(b)), '%.1f' % jacc, 'egyezik' if egyezik else 'elter',
                          ','.join(map(str, sorted(t - b)))))
    szazalek_tahot = 100.0 * egyezo / tahot_van if tahot_van else 0.0
    szazalek_osszes = 100.0 * egyezo / osszes if osszes else 0.0
    alap = szazalek_tahot if nevezo == 'tahot_lefedett_versek' else szazalek_osszes
    ered = 'ELERI' if alap >= kuszob else 'NEM_ERI_EL'
    fej_sorok = kozos.fejlec(URL + ' + konkordancia/TAHOT_kivonat.tsv', 'BSB commit ' + commit, parancs)
    fej_sorok += ['rogzitett kuszob=%s%% definicio=%s nevezo=%s (kuszob.txt, meres elott rogzitve)' % (kuszob, definicio, nevezo),
                  'versek_bsb=%d tahot_lefedett=%d egyezo=%d nincs_tahot=%d' % (osszes, tahot_van, egyezo, osszes - tahot_van),
                  'egyezes_tahot_lefedett_versekre=%.2f%% egyezes_osszes_versre=%.2f%% eredmeny=%s' % (szazalek_tahot, szazalek_osszes, ered),
                  'atlag_jaccard_tahot_lefedett_versekre=%.2f%%' % (jaccard_osszeg / tahot_van if tahot_van else 0.0)]
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_bsb_genezis.tsv'), fej_sorok,
                 ['igehely', 'tahot_strongok_db', 'bsb_strongok_db', 'jaccard_szazalek', 'allapot', 'tahot_hianyzik_a_bsb-bol'], sorok)
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_bsb_elteresek.tsv'), fej_sorok[:4] + fej_sorok[4:5],
                 ['igehely', 'ok', 'tahot_nincs_a_bsb-ben', 'bsb_tobblet'], elteresek)
    for s in fej_sorok[-3:]:
        print(s)
