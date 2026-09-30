#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_kk.py -- F17: Karoli-kulcs (KK) alapu MT->Karoli vers-megfeleltetes a Macula heberhez.

A Macula Hebrew a WLC (MT) szamozasat hasznalja; a Karoli-szoveg (Karoli_1908.tsv) vagy
KJV-, vagy MT-szamozasu fejezetenkent. A megfeleltetes Karoli-verstol indul, majd megfordul:

  1. konkordancia/Karoli_versmegfeleltetes.tsv `igehely_mt` oszlopa, ha ki van toltve; KEZI osztalynal,
     ha az ures, az `igehely_kjv` (a KJV- es az MT-szamozas ezekben a konyvekben azonos)
     (a KK tartalmilag ellenorzott; ha a terkep mast mond, a KK az iranyado, l. `utkozesek`)
  2. konkordancia/LXX_versificacios_terkep.tsv: a Karoli-vers `Heber_vers` oszlopa (STEP-alak;
     '--' = nincs heber megfelelo). Az `EGYIK_SEM` sorokat nem hasznaljuk (a Karoli-szamozas
     egyik hagyomannyal sem egyezik, a Heber_vers nem megbizhato: pl. 1Moz 37:1 -> Gen.36:44,
     ami nem letezik); az `ELLENORZESRE_VAR` sor javaslat.
  3. egyebkent identitas, ha a Karoli-vers a KK-tablaban szerepel.

A `forras` a Karoli-vers hordozott ertekbol szarmazik: terkep | kk_mt | kk_kjv (KEZI osztaly, ures igehely_mt) | identitas.
A terkep utolso oszlopa (`Karoli_egyezik_hol`) `EGYIK_SEM` / `ELLENORZESRE_VAR` -> bizonytalan.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import macula_kozos as K  # noqa: E402


def karoli_mt_terkep():
    """{(konyv, fej, vers): {'mt': [(fej, vers)], 'forras': str, 'biz': 'rendben'|'javaslat', 'ok': str}}"""
    usfm_mag, usfm_step, mag_usfm, kanoni = K.konyvtablak()
    step_mag = {v: usfm_mag[k] for k, v in usfm_step.items()}
    kv = K.karoli_versek()
    kk_fej, kk_sorok = K.tsv_olvas(os.path.join(K.KONK, 'Karoli_versmegfeleltetes.tsv'))
    kk = {}
    for s in kk_sorok:
        m = re.match(r'^(\S+) (\d+):(\d+)$', s[0])
        if m:
            kk[(m.group(1), int(m.group(2)), int(m.group(3)))] = s
    t_fej, t_sorok = K.tsv_olvas(os.path.join(K.KONK, 'LXX_versificacios_terkep.tsv'))
    terkep = {}
    for s in t_sorok:
        m = re.match(r'^(\S+) (\d+):(\d+)$', s[0])
        if not m:
            continue
        terkep.setdefault((m.group(1), int(m.group(2)), int(m.group(3))), []).append(s)

    ki = {}
    statisztika = {'terkep': 0, 'kk_mt': 0, 'identitas': 0, 'terkep_kk_utkozes': 0}
    utkozesek = []
    for konyv, versek in kv.items():
        if konyv not in kanoni[:39]:
            continue
        for (fej, v) in sorted(versek):
            kulcs = (konyv, fej, v)
            sor = kk.get(kulcs)
            kk_mt = None
            kk_forras = 'kk_mt'
            if sor is not None and len(sor) > 2 and sor[2]:
                kk_mt = K.vers_tartomany(sor[2], fej)
            elif sor is not None and len(sor) > 3 and sor[3] == 'KEZI' and sor[1]:
                # KEZI osztaly: az igehely_mt ures, az igehely_kjv az iranyado Karoli-KJV/MT szamozas
                # (ezekben a konyvekben a KJV- es az MT-szamozas azonos; 4Moz 13:34 -> 13:33, Pred 9:10 -> 9:8)
                kk_mt = K.vers_tartomany(sor[1], fej)
                kk_forras = 'kk_kjv'
            t = terkep.get(kulcs)
            ertek = None
            hasznalhato = [ts for ts in (t or []) if not (len(ts) > 5 and ts[5] == 'EGYIK_SEM')]
            if t and not kk_mt and not hasznalhato:
                # minden terkep-sor EGYIK_SEM (a Karoli-szamozas sem a hebernel, sem a latinnal, sem a
                # gorognel nem all): a terkep Heber_vers-e nem megbizhato -> identitas, ha a KK-ban van
                if sor is not None:
                    ertek = {'mt': [(fej, v)], 'forras': 'identitas', 'biz': 'javaslat',
                             'ok': 'terkep_egyik_sem_identitas'}
                    statisztika['identitas_terkep_egyik_sem'] = statisztika.get('identitas_terkep_egyik_sem', 0) + 1
            elif t and not kk_mt:
                mtlista, biz, ok = [], 'rendben', ''
                for ts in hasznalhato:
                    heber = ts[1]
                    if heber.strip() in ('--', ''):
                        continue
                    pre, _, rest = heber.partition('.')
                    if pre not in step_mag or step_mag[pre] != konyv:
                        biz, ok = 'javaslat', 'terkep_masik_konyv:' + heber
                        continue
                    for x in K.vers_tartomany(rest, fej):
                        if x is None:
                            biz, ok = 'javaslat', 'terkep_tartomany_hianyos:' + heber
                        elif x not in mtlista:
                            mtlista.append(x)
                    hol = ts[5] if len(ts) > 5 else ''
                    if hol == 'ELLENORZESRE_VAR':
                        biz, ok = 'javaslat', 'terkep_ellenorzesre_var'
                if not mtlista:
                    biz, ok = 'javaslat', ok or 'terkep_nincs_heber_vers'
                ertek = {'mt': mtlista, 'forras': 'terkep', 'biz': biz, 'ok': ok}
                statisztika['terkep'] += 1
            elif kk_mt:
                ertek = {'mt': [x for x in kk_mt if x], 'forras': kk_forras, 'biz': 'rendben', 'ok': ''}
                if None in kk_mt:
                    ertek['biz'], ertek['ok'] = 'javaslat', 'kk_mt_tartomany_hianyos'
                statisztika[kk_forras] = statisztika.get(kk_forras, 0) + 1
                if t:
                    # a terkep is szol: az eltereseket megorizzuk (nem dontjuk el)
                    tl = []
                    for ts in t:
                        pre, _, rest = ts[1].partition('.')
                        tl.extend(x for x in K.vers_tartomany(rest, fej) if x)
                    if tl != ertek['mt']:
                        statisztika['terkep_kk_utkozes'] += 1
                        utkozesek.append((konyv, fej, v, tl, ertek['mt']))
            elif sor is not None:
                ertek = {'mt': [(fej, v)], 'forras': 'identitas', 'biz': 'rendben', 'ok': ''}
                statisztika['identitas'] += 1
            if ertek is not None:
                ki[kulcs] = ertek
    return ki, statisztika, utkozesek


def mt_karoli_index(ki):
    """{(konyv, fej, vers): [(karoli_kulcs, ertek), ...]} az MT-oldalrol."""
    inv = {}
    for kulcs, e in ki.items():
        for (mf, mv) in e['mt']:
            inv.setdefault((kulcs[0], mf, mv), []).append((kulcs, e))
    return inv


if __name__ == '__main__':
    ki, st, ut = karoli_mt_terkep()
    print(st, len(ki), len(ut))
    for x in ut[:10]:
        print(x)
