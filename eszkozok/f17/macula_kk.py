#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_kk.py -- F17: Karoli-kulcs (KK) alapu MT->Karoli vers-megfeleltetes a Macula heberhez.

A Macula Hebrew a WLC (MT) szamozasat hasznalja; a Karoli-szoveg (Karoli_1908.tsv) vagy
KJV-, vagy MT-szamozasu fejezetenkent. A megfeleltetes Karoli-verstol indul, majd megfordul:

  1. konkordancia/Karoli_versmegfeleltetes.tsv `igehely_mt` oszlopa, ha ki van toltve; KEZI osztalynal,
     ha az ures, az `igehely_kjv` (tobbforrasu osszevonasnal a `raw=` lista) -- CSAK ha a KJV- es az MT-fejezet
     verskeszlete azonos (Dan 4 nem az: KJV 4:4 = MT 4:1)
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

# DT7 (c): a Károli-szöveg MT-számozású fejezetei, ahol a térkép és a KJV-alapú KEZI-kötés nem irányadó
DAN_IDENTITAS = {3, 4}


def karoli_mt_terkep(mt_versek=None):
    """{(konyv, fej, vers): {'mt': [(fej, vers)], 'forras': str, 'biz': 'rendben'|'javaslat', 'ok': str}}

    mt_versek: {magyar konyv: {(fej, vers)}} a Macula (MT) verseibol; a KEZI-sorok KJV=MT igazolasahoz
    es a hianyzo Karoli-versek interpolalasahoz kell."""
    mt_versek = mt_versek or {}
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

    # KJV-fejezetek versszama: naplok/KAROLI_KK1b_fejezetosztaly.tsv `kjv_max` (a KK1b a lxx-morph verse_pairs
    # KJV-oldalarol szamolta); a Macula-oldal a MT-fejezetek tenyleges versszama. A KJV-szamozas akkor egyezik az
    # MT-vel egy fejezetben, ha az elozo fejezet KJV- es MT-versszama azonos (nincs fejezet eleji eltolodas), es a vers
    # mindket oldalon letezik. (A kumulalt osszeg nem jo: a KK1b kjv_max-a a 4Moz 6-ra 26, a KJV-ben 27 a vers.) (Dan 4: a 3. fejezet KJV 30 / MT 33 vers -> KJV 4:4 = MT 4:1.)
    kjv_n = {}
    kf_fej, kf_sorok = K.tsv_olvas(os.path.join(K.REPO, 'naplok', 'KAROLI_KK1b_fejezetosztaly.tsv'))
    for s_ in kf_sorok:
        try:
            kjv_n[(s_[0], int(s_[2]))] = int(s_[4])
        except (ValueError, IndexError):
            continue
    mt_n = {}
    for konyv_, halmaz in mt_versek.items():
        for (f_, v_) in halmaz:
            mt_n[(konyv_, f_)] = mt_n.get((konyv_, f_), 0) + 1
    eltolodas = {}   # az elozo fejezet KJV- es MT-versszamanak kulonbsege (a fejezet eleji eltolodas jelzoje)
    for (konyv_, f_) in kjv_n:
        if f_ == 1:
            eltolodas[(konyv_, f_)] = 0
        elif (konyv_, f_ - 1) in kjv_n:
            eltolodas[(konyv_, f_)] = kjv_n[(konyv_, f_ - 1)] - mt_n.get((konyv_, f_ - 1), 0)
    kezi_fejezetek = {}   # (konyv, kjv-fejezet) -> [kjv_versek, mt_versek, eltolodas, karoli_sorok, igazolt_versek, nem_igazolt_versek]

    def kezi_igazolt(konyv_, fej_, vers_):
        kj = kjv_n.get((konyv_, fej_), 0)
        mt = mt_n.get((konyv_, fej_), 0)
        elt = eltolodas.get((konyv_, fej_), None)
        ok_ = elt == 0 and 1 <= vers_ <= min(kj, mt)
        e = kezi_fejezetek.setdefault((konyv_, fej_), [kj, mt, elt, 0, 0, 0])
        e[4 if ok_ else 5] += 1
        return ok_

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
            kezi_ertek = None
            if kk_mt is None and sor is not None and len(sor) > 3 and sor[3] == 'KEZI' and sor[1]:
                # KEZI osztaly: az igehely_mt ures; az igehely_kjv (tobbforrasu osszevonasnal a megjegyzes
                # `raw=A;raw=B` felsorolasa) a KJV-szamozas. A KJV = MT azonossag NEM altalanos (Dan 4: KJV 4:4 = MT 4:1),
                # ezert csak ott iranyado, ahol a KJV- es az MT-fejezet verskeszlete azonos (kezi_igazolt).
                celok = []
                raws = re.findall(r'raw=(\d+:\d+)', sor[5] if len(sor) > 5 else '')
                for r_ in (raws if len(raws) > 1 else [sor[1]]):
                    celok.extend(x for x in K.vers_tartomany(r_, fej) if x)
                igazolt = bool(celok) and all([kezi_igazolt(konyv, c_[0], c_[1]) for c_ in celok])
                for c_ in {c_[0] for c_ in celok}:
                    kezi_fejezetek[(konyv, c_)][3] += 1
                if igazolt:
                    kezi_ertek = {'mt': celok, 'forras': 'kk_kjv', 'biz': 'rendben', 'ok': ''}
                    statisztika['kk_kjv'] = statisztika.get('kk_kjv', 0) + 1
                else:
                    kezi_ertek = {'mt': [], 'forras': 'kk_kjv', 'biz': 'javaslat', 'ok': 'kk_kjv_mt_nem_igazolt'}
                    statisztika['kk_kjv_nem_igazolt'] = statisztika.get('kk_kjv_nem_igazolt', 0) + 1
            t = terkep.get(kulcs)
            ertek = None
            if konyv == 'Dán' and fej in DAN_IDENTITAS and (not mt_versek.get(konyv) or (fej, v) in mt_versek[konyv]):
                # DT7 (c), 2026.10.02: a Károli Dán 3-4 szövege MT-számozású (Károli x:y = MT x:y; Dán 4: 1-34, Dán 3: 31-33 is)
                ertek = {'mt': [(fej, v)], 'forras': 'identitas', 'biz': 'rendben', 'ok': 'dan_identitas_dt7'}
            hasznalhato = [ts for ts in (t or []) if not (len(ts) > 5 and ts[5] == 'EGYIK_SEM')]
            if ertek is not None:
                pass
            elif kezi_ertek is not None:
                ertek = kezi_ertek
            elif t and not kk_mt and not hasznalhato:
                # minden terkep-sor EGYIK_SEM (a Karoli-szamozas sem a hebernel, sem a latinnal, sem a
                # gorognel nem all): a terkep Heber_vers-e nem megbizhato -> identitas, ha a KK-ban van
                if sor is not None:
                    elt = eltolodas.get((konyv, fej), 0)
                    if elt not in (0, None):
                        # fejezetszam-proba: az elozo fejezet KJV- es MT-versszama eltér -> a fejezet elejen
                        # eltolodas van (pl. Pred 4: KJV 16 / MT 17 vers -> Karoli 5:1 = MT 4:17; 4Moz 29:
                        # KJV 40 / MT 39 -> Karoli 30:1 = MT 30:2). Az identitas hamis lenne: ures MT-ertek.
                        ertek = {'mt': [], 'forras': 'identitas', 'biz': 'javaslat',
                                 'ok': 'terkep_egyik_sem_eltolodas_gyanu'}
                    else:
                        ertek = {'mt': [(fej, v)], 'forras': 'identitas', 'biz': 'javaslat',
                                 'ok': 'terkep_egyik_sem_identitas'}
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
    # --- interpolacio: a KK-ban nem szereplo (vagy KEZI-sorban ures igehely_kjv/igehely_mt-s) Karoli-vers, amelynek
    # kovetkezoje (akar a kovetkezo fejezet elso verse) KEZI-horgony
    # (pl. Job 39:1-3 -> MT 38:39-41, Job 39:34-38 -> MT 40:1-5, 4Moz 13:1 -> MT 12:16): a horgony MT-versenek elozo MT-verse.
    def elozo_mt(konyv_, cel):
        lista_ = sorted(mt_versek.get(konyv_, ()))
        if cel in lista_:
            i_ = lista_.index(cel)
            return lista_[i_ - 1] if i_ > 0 else None
        return None

    for konyv, versek in kv.items():
        if konyv not in kanoni[:39]:
            continue
        sorrend = sorted(versek)
        for i_ in range(len(sorrend) - 2, -1, -1):
            kul = (konyv,) + sorrend[i_]
            kov = (konyv,) + sorrend[i_ + 1]
            sor_ = kk.get(kul)
            ures_kezi = (sor_ is not None and len(sor_) > 3 and sor_[3] == 'KEZI' and not sor_[1] and not sor_[2])
            if sor_ is not None and not ures_kezi:
                continue
            horgony = ki.get(kov)
            if not horgony or horgony['forras'] not in ('kk_kjv', 'kezi_interpolalt') or not horgony['mt']:
                continue
            if horgony['forras'] == 'kk_kjv' and horgony['biz'] != 'rendben':
                continue
            cel = elozo_mt(konyv, min(horgony['mt']))
            if cel is None:
                continue
            ki[kul] = {'mt': [cel], 'forras': 'kezi_interpolalt', 'biz': 'javaslat', 'ok': 'kezi_interpolalt'}
            statisztika['kezi_interpolalt'] = statisztika.get('kezi_interpolalt', 0) + 1

    # --- tekintely: az MT-verset, amelyet a KK (kk_mt/kk_kjv) vagy a KEZI-interpolacio igenyel, a terkep/identitas
    # nem kotheti mas Karoli-versre.
    tekintely_visszavont = 0
    hiv = {}
    for kul, e in ki.items():
        if e['forras'] in ('kk_mt', 'kk_kjv', 'kezi_interpolalt'):
            for x in e['mt']:
                hiv.setdefault((kul[0],) + x, set()).add(kul)
    for kul, e in ki.items():
        if e['forras'] in ('kk_mt', 'kk_kjv', 'kezi_interpolalt'):
            continue
        marad = [x for x in e['mt'] if not (hiv.get((kul[0],) + x) and kul not in hiv[(kul[0],) + x])]
        if len(marad) != len(e['mt']):
            e['mt'] = marad
            e['biz'] = 'javaslat'
            e['ok'] = (e['ok'] + '|' if e['ok'] else '') + 'mt_vers_kk_val_foglalt'
            tekintely_visszavont += 1
    def kat(e):
        if e['forras'] == 'identitas':
            return {'': 'identitas', 'dan_identitas_dt7': 'identitas_dan_dt7', 'terkep_egyik_sem_identitas': 'identitas_terkep_egyik_sem',
                    'terkep_egyik_sem_eltolodas_gyanu': 'terkep_egyik_sem_eltolodas_gyanu'}.get(e['ok'].split('|')[0], 'identitas_egyeb')
        if e['forras'] == 'kk_kjv' and e['biz'] != 'rendben':
            return 'kk_kjv_nem_igazolt'
        return e['forras']

    kat_db = {}
    for e in ki.values():
        k_ = kat(e)
        kat_db[k_] = kat_db.get(k_, 0) + 1
    utk_ = statisztika.get('terkep_kk_utkozes', 0)
    statisztika.clear()
    statisztika.update(kat_db)
    statisztika['terkep_kk_utkozes'] = utk_
    statisztika['particio_osszeg'] = sum(kat_db.values())
    statisztika['tekintely_visszavont'] = tekintely_visszavont
    statisztika['kezi_fejezetek'] = sorted((k[0], k[1]) + tuple(v) for k, v in kezi_fejezetek.items())
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
