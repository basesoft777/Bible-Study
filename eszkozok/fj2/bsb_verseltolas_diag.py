#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_verseltolas_diag.py -- F16: tajekoztato diagnozis a kuszob alatti OSZ-konyvekre;
F41 (--f41, alapertelmezett): versszintu BSB -> MT megfeleltetes mind a 39 OSZ-konyvre.

A TAHOT heber (MT) verszamozast hasznal, a BSB angolt; a bsb_import.py igehely-szintu
egyezese ezert a szamozasi eltolas miatt is elbukhat. Ez a szkript fejezetenkent a
{-1, 0, +1, +2} eltolasok kozul a legjobbat valasztja (BSB v <-> TAHOT v+k), es igy
megmutatja, mennyi a kuszob alatti eredmenybol szamozas-artefaktum. NEM a kuszob alapja,
NEM modositja az import-dontest; a dontes a DONTESEK.md-tetelben a felhasznaloe.

Kimenet: naplok/F16_bsb_verseltolas_diagnozis.tsv (csak a NEM_ERI_EL OSZ-konyvek) a --f16 kapcsoloval;
naplok/F41_bsb_megfeleltetes.tsv (konyv, bsb_vers, mt_vers, modell, ok) es naplok/F41_nem_egyezo_versek.tsv (okkategoriaval) a --f41 futasnal.
A F41 megfeleltetes: bsb_import.konyv_megfeleltetes (Strong-illeszkedes, monoton igazitas, fejezetenkenti igazolas);
az "mt_vers" a TAHOT_kivonat szamozasa. Egy fejezet illesztetlen, ha a megfeleltetese nem igazolhato (l. a fuggveny docstringje).
Hasznalat: python eszkozok/fj2/bsb_verseltolas_diag.py --munka <mappa> [--f16 | --f41]
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb_import as bi  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ELTOLASOK = (-1, 0, 1, 2)


def fut_f16(munka, parancs):
    mappa = os.path.join(munka, 'bsb-data-output', 'base', 'display')
    commit = kozos.commit_sha(os.path.join(munka, 'bsb-data-output'))
    tahot = bi.forras_halmazok('H')
    fej, lef = kozos.tsv_olvas(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'))
    ered_i = fej.index('eredmeny')
    alatta = {s[0] for s in lef if s[2] == 'heber' and s[ered_i] == 'NEM_ERI_EL'}
    sorok = []
    for step, mag, nyelv in bi.konyvek()[:39]:
        if mag not in alatta:
            continue
        kod = step.upper()
        bmappa = os.path.join(mappa, kod)
        fejezetek = sorted(int(m.group(1)) for fn in os.listdir(bmappa)
                           for m in [re.fullmatch(kod + r'(\d+)\.json', fn)] if m)
        nevezo = egyezo_alap = egyezo_eltolt = 0
        eltolt_fejezetek = []
        for fej_szam in fejezetek:
            with open(os.path.join(bmappa, '%s%d.json' % (kod, fej_szam)), encoding='utf-8') as f:
                b = bi.vers_strongok(json.load(f), 'H')
            legjobb = None
            for k in ELTOLASOK:
                db = n = 0
                for vs in b:
                    t = tahot.get('%s %d:%d' % (mag, fej_szam, vs + k))
                    if t is None:
                        continue
                    n += 1
                    if t <= b[vs]:
                        db += 1
                if legjobb is None or db > legjobb[1]:
                    legjobb = (k, db, n)
            db0 = n0 = 0
            for vs in b:
                t = tahot.get('%s %d:%d' % (mag, fej_szam, vs))
                if t is None:
                    continue
                n0 += 1
                if t <= b[vs]:
                    db0 += 1
            nevezo += n0
            egyezo_alap += db0
            # az eltolt valtozat nevezoje a nulla-eltolasu nevezo (a tobbi vers tovabbra sem egyezik)
            egyezo_eltolt += max(legjobb[1], db0)
            if legjobb[0] != 0 and legjobb[1] > db0:
                eltolt_fejezetek.append('%d(%+d)' % (fej_szam, legjobb[0]))
        sorok.append((mag, str(nevezo), str(egyezo_alap), '%.2f' % (100.0 * egyezo_alap / nevezo),
                      str(egyezo_eltolt), '%.2f' % (100.0 * egyezo_eltolt / nevezo),
                      ' '.join(eltolt_fejezetek) if eltolt_fejezetek else '-'))
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_bsb_verseltolas_diagnozis.tsv'),
                 kozos.fejlec(bi.URL + ' + konkordancia/TAHOT_kivonat.tsv', 'BSB commit ' + commit, parancs)
                 + ['tajekoztato diagnozis, NEM a kuszob alapja; fejezetenkent a legjobb BSB v <-> TAHOT v+k eltolas (k in -1,0,1,2); nevezo = a nulla-eltolasu nevezo',
                    'eltolt_fejezetek: fejezet(eltolas) csak ott, ahol az eltolas javit'],
                 ['konyv', 'nevezo', 'egyezo_eltolas_nelkul', 'szazalek_eltolas_nelkul', 'egyezo_legjobb_eltolassal',
                  'szazalek_legjobb_eltolassal', 'eltolt_fejezetek'], sorok)
    for s in sorok:
        print('\t'.join(s))


def tsv_ir_nagy(ut, fejlec_sorok, oszlopok, sorok):
    """Mint kozos.tsv_ir, de az 1 MB-os naplo-korlat nelkul (a megfeleltetes ~23 000 versszintu sor; csv nelkul)."""
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for h in fejlec_sorok:
            f.write('# %s\n' % kozos.tisztit(h))
        f.write('\t'.join(oszlopok) + '\n')
        for s in sorok:
            if len(s) != len(oszlopok):
                raise ValueError('oszlopszam-elteres: %s' % (s,))
            f.write('\t'.join(kozos.tisztit(x) for x in s) + '\n')


# Aramai szakaszok (F41.3, a brief szerint; a TAHOT_kivonatban nincs nyelvjeloles): [(elso_vers, utolso_vers)] (fejezet, vers) tuple-ok, zart intervallum.
# A Dan 2:4 es az Ezsd 4:8 a hatarvers (Dan 2:4a heber, 2:4b arami): a tartomany a brief szerinti kezdopont.
ARAMI = {
    'Dán': [((2, 4), (7, 28))],
    'Ezsd': [((4, 8), (6, 18)), ((7, 12), (7, 26))],
    'Jer': [((10, 11), (10, 11))],
}


def arami_e(mag, mt):
    return any(a <= mt <= b for a, b in ARAMI.get(mag, ()))


def kozos_vaz(s):
    """Heber lemma massalhangzos vaza (niqqud, taamim, maqaf nelkul)."""
    return re.sub(r'[֑-ׇ־]', '', s)


def lemma_terkep():
    """{Strong (int, < 9000): set(massalhangzos lemma-vaz)} a TAHOT_kivonat `Szótő` oszlopabol (a 9000-es prefixkodok nelkul)."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'TAHOT_kivonat.tsv'))
    i = fej.index('Szótő')
    ki = {}
    for s in sorok:
        if len(s) > i and s[1].startswith('H'):
            n = kozos.strong_szam(s[1])
            if n is not None and n < 9000:
                ki.setdefault(n, set()).add(kozos_vaz(s[i]))
    return ki


def okkategoria(mag, x, bset, tset, mtd, mtlista, mtidx, lem):
    """Egy nem egyezo meresi egyseg (a TAHOT-vers Strong-halmaza nem resze a BSB-oldalnak) okkategoriaja; sorrend = a brief felsorolasa:
    szamozas = a szomszedos MT-vers (+-1, a TAHOT sorrendjeben) Strong-halmaza teljesen a BSB-oldal resze (a vers a szomszedos MT-versre illik);
    arami = az MT-vers a brief szerinti arami tartomanyba esik;
    cimkezes = a TAHOT minden hianyzo Strongjahoz van a BSB-tobbletben olyan Strong, amellyel kozos massalhangzos lemma-vazon osztozik a
      TAHOT_kivonatban (eltero Strong-szam ugyanarra a lemma-vazra; formai kriterium, nem szemantikai allitas);
    egyeb = minden mas."""
    i = mtidx.get(x)
    if i is not None:
        for d in (-1, 1):
            if 0 <= i + d < len(mtlista):
                y = mtlista[i + d]
                if mtd[y] and mtd[y] <= bset:
                    return 'szamozas'
    if arami_e(mag, x):
        return 'arami'
    hianyzo, tobblet = tset - bset, bset - tset
    if hianyzo and all(any(lem.get(m, set()) & lem.get(e, set()) for e in tobblet) for m in hianyzo):
        return 'cimkezes'
    return 'egyeb'


def cimke_par_e(hianyzo, tobblet, lem):
    return bool(hianyzo) and all(any(lem.get(m, set()) & lem.get(e, set()) for e in tobblet) for m in hianyzo)


def f41_futtat(munka, parancs):
    cel = os.path.join(munka, 'bsb-data-output')
    commit = kozos.commit_sha(cel)
    tahot = bi.forras_halmazok('H')
    kk = bi.kk_betolt()
    kkmax = bi.kk_max_tabla(kk)
    lem = lemma_terkep()
    fej, lef = kozos.tsv_olvas(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'))
    li = {n: fej.index(n) for n in ('egyezes_szazalek', 'egyezes_szazalek_eltolas_nelkul', 'eredmeny')}
    lefd = {bi.forras_nev(s[0]): s for s in lef if s[2] == 'heber'}
    tsv_sorok, osszegzes, kk_elt, reg_zsolt, nem_egyezo = [], [], [], [], []
    kat_szamlalo, kat_aramikeresztbe, peldak_9, sorok_konyv = {}, {}, {}, {}
    for step, mag, nyelv in bi.konyvek()[:39]:
        k = bi.ot_konyv(cel, step, mag, tahot, kkmax)
        fmag, kod, fejezetek, bsb_fej = k['fmag'], k['kod'], k['fejezetek'], k['bsb_fej']
        sorok, osztas, mtd, tmax = k['sorok'], k['osztas'], k['mtd'], k['tmax']
        sorok_konyv[mag] = (k['sorok'], tmax)
        mtlista = sorted(mtd)
        mtidx = {r: i for i, r in enumerate(mtlista)}
        sorszam = {}
        for f in fejezetek:
            for sor in bi.vers_sorok(k['adatok'][f], step, f):
                v = int(sor[0].rsplit('.', 1)[1])
                sorszam[(f, v)] = sorszam.get((f, v), 0) + 1
        eltolt_fej, ill_fej, atszam_sor, kieso_sor, n_eltolt, n_kjv, osztott = {}, {}, 0, 0, 0, 0, []
        for (f, v), x, modell, ok in sorok:
            if modell == 'kjv_szamozas':
                n_kjv += 1
                continue
            if (f, v) in osztas:
                xa, xs, p = osztas[(f, v)]
                osztott.append('%d:%d->%d:%d+%d:%d' % ((f, v) + xa + xs))
            if modell == 'illesztetlen':
                ill_fej.setdefault(f, ok)
                kieso_sor += sorszam.get((f, v), 0)
                continue
            if modell == 'eltolt':
                n_eltolt += 1
                eltolt_fej.setdefault(f, set()).add((x[0] - f, x[1] - v))
                atszam_sor += sorszam.get((f, v), 0)
        for (f, v), cel_v, modell, ok, szam, tahot_v in k['cel_sorok']:
            tsv_sorok.append((mag, '%d:%d' % (f, v), cel_v, modell, ok, tahot_v, szam))
        nev = sum(1 for t in k['tetelek'] if t[3] is not None)
        eg = sum(1 for t in k['tetelek'] if t[3] is not None and t[3] <= t[2])
        szamlalo = {'szamozas': 0, 'arami': 0, 'cimkezes': 0, 'egyeb': 0}
        arami_cimke = 0
        for (f, v), x, bset, tset in k['tetelek']:
            if tset is None or tset <= bset:
                continue
            kat = okkategoria(fmag, x, bset, tset, mtd, mtlista, mtidx, lem)
            szamlalo[kat] += 1
            if kat == 'arami' and cimke_par_e(tset - bset, bset - tset, lem):
                arami_cimke += 1
            nem_egyezo.append((mag, '%d:%d' % (f, v), '%d:%d' % x, ' '.join('H%d' % n for n in sorted(tset - bset)),
                               ' '.join('H%d' % n for n in sorted(bset - tset)), kat))
        kat_szamlalo[mag] = (nev, szamlalo)
        kat_aramikeresztbe[mag] = arami_cimke
        lr = lefd[fmag]
        osszegzes.append((mag, lr[li['egyezes_szazalek_eltolas_nelkul']], '%.2f' % (100.0 * eg / nev) if nev else '0', str(eg), str(nev),
                          lr[li['eredmeny']], len(eltolt_fej), n_eltolt, atszam_sor, len(ill_fej), kieso_sor, n_kjv, eltolt_fej, ill_fej, osztott))
        # Karoli-kulcs igehely_kjv ellenorzes (N-F41a): a BSB (KJV-szamozas) verse -> a mi MT-versunk vs. a kulcs sora
        meg = {(f, v): x for (f, v), x, modell, ok in sorok if x and (f, v) not in osztas}
        ossz = elt = 0
        peldak = []
        for kar, kjv, mt, osz in kk:
            if kar.rsplit(' ', 1)[0] != fmag or not kjv or osz not in ('MT', 'KJV'):
                continue
            m = re.fullmatch(r'(\d+):(\d+)', kjv)
            if not m:
                continue
            kulcs = (int(m.group(1)), int(m.group(2)))
            if kulcs not in meg:
                continue
            ossz += 1
            kk_mt = mt if mt else kjv
            sajat = '%d:%d' % meg[kulcs]
            if sajat != kk_mt:
                elt += 1
                if len(peldak) < 3:
                    peldak.append('%s: kulcs kjv=%s mt=%s, Strong-illeszkedes szerint BSB %s -> MT %s' % (kar, kjv, kk_mt, kjv, sajat))
        kk_elt.append((mag, ossz, elt, peldak))
        # regresszio a Zsoltar F16.8-modelljevel (fejezetenkenti k)
        if mag in bi.MT_ELTOLASOS_KONYVEK:
            to_db = {f: bi.text_only_sorok(cel, kod, f) for f in fejezetek}
            k_regi = bi.fejezet_eltolasok(fmag, fejezetek, to_db, tmax)
            kul = 0
            for (f, v), x, modell, ok in sorok:
                if modell in ('azonos', 'eltolt') and x != (f, v + k_regi[f]):
                    kul += 1
            reg_zsolt.append(kul)
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_bsb_megfeleltetes.tsv'),
                 kozos.fejlec(bi.URL + ' + konkordancia/TAHOT_kivonat.tsv + konkordancia/Karoli_versmegfeleltetes.tsv (igehely_mt, ellenorzes)',
                              'BSB commit ' + commit, parancs)
                 + ['versszintu BSB-vers -> MT-vers megfeleltetes mind a 39 OSZ-konyvre (F41.1); bsb_vers = a BSB (display-JSON) fejezet:verse; mt_vers = az IMPORT cel-Igehelye (a BSB_Strongs.tsv Igehely-oszlopa): a TAHOT_kivonat versszamozasahoz Strong-illeszkedessel megfeleltetett vers (cel: MT/WLC; a TAHOT_kivonat versszamozasa 25 konyvben nem azonos a WLC-vel, l. NYITOTT N-F41d), kiveve a BSB(KJV)-szamozas-megtartott fejezeteket (Job 38-41, Pred 11/12, Ezs 2/3, 4Moz 12/13: mt_vers = bsb_vers); a tahot_vers a TAHOT_kivonat verse, amelyhez a BSB-verset a MERES illesztette (a Pred 11/12, Ezs 2/3, 4Moz 12/13 sorain ez a Karoli-szeru TAHOT-szam, az Igehely nem ez); a WLC-vel versszintu egyezes: naplok/F41_wlc_versszam_ellenorzes.tsv',
                    'szamozas (DT-F41f; = a BSB_Strongs.tsv 7. oszlopa, VERSSZINTU WLC-osszevetesbol): mt = a WLC azonos szamu versevel igazolt MT-szam (wlc_versek.vers_igazolt, DT-F41g); kjv = a BSB(KJV)-szam marad, es tenylegesen KJV != MT (csak Job 41; a Job MT-re szamozasa kulon N-tetel, N-F41g); ellenorizetlen = a WLC-vel egyertelmuen nem igazolt (nem allitja, hogy a szam hibas; MT-re szamozasa: N-F41h); ures = illesztetlen fejezet. Felhasznaloi dontes 2026.10.02: 4Moz 12/13 atszamozasa visszavonva (WLC: KJV = MT), Job 38-41 a main KJV-szamozasan; Pred 11/12, Ezs 2/3: az atszamozas visszavonva (KJV = MT: naplok/F41_wlc_hatar_ellenorzes.tsv)',
                    'modell (az Igehely cel-szamozasa szerint): azonos = mt_vers = bsb_vers; eltolt = mas fejezet:vers (fejezethataron atnyulo eset is; az 1 BSB-vers -> 2 MT-vers osztas is: mt_vers = a ket MT-vers "fej:vers+fej:vers" alakban); illesztetlen = a fejezet megfeleltetese nem igazolhato, a fejezet nem szamit a meresbe es az importba (mt_vers ures); kjv_szamozas = az Igehely a BSB(KJV)-szam marad (Job 38-41; mt_vers = bsb_vers); a Job 41 a TAHOT_kivonatban nincs (tahot_vers ures), a meresbol kimarad; a Job 38-40 a MERESBEN a TAHOT_kivonathoz illesztve szerepel (a tahot_vers oszlop); a Pred 11/12, Ezs 2/3 es 4Moz 12/13 modellje azonos (a BSB-szam egyezik a WLC-vel)',
                    'a megfeleltetes forrasa a Strong-illeszkedes (monoton 1:1 igazitas, a TAHOT-vers Strong-halmazanak BSB-ben levo hanyada > 0,5); fejezetenkenti igazolas: nincs_mt_part / vers_osztas / mt_vers_kimarad (a TAHOT_kivonat sajat versfolyamaban kimaradt MT-vers; az egyertelmuen igazolt 1 -> 2 osztas kivetel, l. bsb_import.osztas_pont) / kk_max_eltérés (l. bsb_import.konyv_megfeleltetes)',
                    'ok (azonos/eltolt): strong_illeszkedik = a TAHOT-vers Strongjai a BSB-vers reszei; strong_nem_egyezo = megfeleltetett, de nem egyezo vers; tahot_nincs_vers = a megfeleltetett MT-vers nincs a TAHOT_kivonatban; kitoltve_a_szomszedok_eltolasabol = a vers nem illesztheto, a fejezeten belüli szomszedai azonos eltolasuak; versosztas_ketto_mt_vers_strong_illeszkedik = a BSB-vers a ket MT-vers uniojat adja, a vago pont egyertelmu']
                 + ['osztott BSB-versek (1 -> 2 MT-vers): ' + '; '.join('%s %s' % (o[0], ' '.join(o[14])) for o in osszegzes if o[14])],
                 ['konyv', 'bsb_vers', 'mt_vers', 'modell', 'ok', 'tahot_vers', 'szamozas'], tsv_sorok)
    print('KONYV\tF06_nyers%\tuj%\tegyezo\tnevezo\tregi_eredmeny\teltolt_fej\teltolt_vers\tatszamozott_sor\tillesztetlen_fej\tkieso_sor\tkjv_vers')
    for o in osszegzes:
        print('\t'.join(str(x) for x in o[:12]))
    print('--- eltolt fejezetek (BSB fejezet: (dfej,dvers) halmaz)')
    for o in osszegzes:
        if o[12]:
            print(o[0], {f: sorted(d) for f, d in sorted(o[12].items())})
    print('--- illesztetlen fejezetek')
    for o in osszegzes:
        for f, ok in sorted(o[13].items()):
            print(o[0], f, ok)
    print('--- osztott versek', [(o[0], o[14]) for o in osszegzes if o[14]])
    print('--- KK igehely_kjv ellenorzes: konyv, osszehasonlitott, elteres')
    for kk_s in kk_elt:
        if kk_s[2]:
            print(kk_s[0], kk_s[1], kk_s[2])
            for p in kk_s[3]:
                print('   ', p)
    print('Zsolt regresszio (a F16.8-modelltol eltero, nem illesztetlen vers): %s' % reg_zsolt)
    # F41.2 / 3.2: nem egyezo versek
    sorok_ossz = {}
    for kn, (nev, sz) in kat_szamlalo.items():
        sorok_ossz[kn] = sum(sz.values())
    cim = ['a meres nevezojebe eso (a TAHOT_kivonat versenkent mert), de NEM egyezo egysegek: a TAHOT-vers Strong-halmaza nem resze a BSB-oldalnak, a F41.1 megfeleltetes utan (naplok/F41_bsb_megfeleltetes.tsv); a ket MT-versre osztott BSB-vers ket egyseg; az illesztetlen es a kjv_szamozasu fejezetek nincsenek benne',
           'tahot_nincs_bsbben = a TAHOT-nak azok a Strongjai, amelyek a BSB-oldalon nincsenek (ez okozza a nem-egyezest); bsb_tobblet = a BSB-oldal Strongjai, amelyek a TAHOT-versben nincsenek (tajekoztato)',
           'okkategoria (a brief sorrendjeben): szamozas = a szomszedos MT-vers (+-1, a TAHOT sorrendjeben) Strong-halmaza teljesen a BSB-oldal resze (a vers a szomszedos MT-versre illik; a modell nem kezelte); arami = az MT-vers a brief szerinti arami szakaszba esik (Dan 2:4-7:28, Ezsd 4:8-6:18 es 7:12-26, Jer 10:11; a TAHOT_kivonatban nincs nyelvjeloles, ezert tartomany); cimkezes = a TAHOT minden hianyzo Strongjahoz van a BSB-tobbletben olyan Strong, amellyel kozos massalhangzos lemma-vazon osztozik a TAHOT_kivonat Szoto oszlopaban (formai kriterium, nem szemantikai allitas); egyeb = minden mas',
           'a bsb_tobblet es a tahot_nincs_bsbben Strong-szamai a 9000-es prefixkodok nelkuliek (a merés is igy szamol)']
    def megf(mag, f, v):
        for (ff, vv), x, modell, ok in sorok_konyv[mag][0]:
            if (ff, vv) == (f, v):
                return '%s %s (%s)' % ('%d:%d' % (f, v), ('-> %d:%d' % x) if x else '-> ?', modell)
        return '%d:%d nincs' % (f, v)

    cim.append('feltevesek (brief 3.2) a megfeleltetesbol: 2Sam 18:33 / 19:1 (a feltevesben szereplo szamozasi hatar): BSB ' + megf('2Sám', 18, 33) + '; BSB ' + megf('2Sám', 19, 1)
               + '; a TAHOT_kivonat 2Sam-szamozasa a KJV-e (18. fej. max %d, 19. fej. max %d) -> a szamozasi eltolas feltevese NEM igazolodott (nincs eltolt vers a 2Sam-ban)' % (sorok_konyv['2Sám'][1].get(18, 0), sorok_konyv['2Sám'][1].get(19, 0)))
    cim.append('Dan 3/4 es 5:31/6:1: a TAHOT_kivonat Dan-szamozasa a KJV-e (fejezet-max: 3=%d, 4=%d, 5=%d, 6=%d); BSB 5:31 ' % tuple(sorok_konyv['Dán'][1].get(c, 0) for c in (3, 4, 5, 6)) + megf('Dán', 5, 31)
               + ' -> a szamozasi eltolas feltevese NEM igazolodott (nincs eltolt vers a Dan-ban). Figyelem: ez a TAHOT_kivonat szamozasa, nem feltetlenul a masoreta (WLC) szamozas (N-F41d)')
    egd = {o[0]: int(o[3]) for o in osszegzes}
    for kn in ('2Sám', 'Ezsd', 'Dán'):
        nev, sz = kat_szamlalo[kn]
        db = sum(sz.values())
        sor = '%s (%d egyezo / %d nevezo = %.2f%%): %d nem egyezo egyseg; okkategoria: szamozas=%d, arami=%d, cimkezes=%d, egyeb=%d' % (
            kn, egd[kn], nev, 100.0 * egd[kn] / nev, db, sz['szamozas'], sz['arami'], sz['cimkezes'], sz['egyeb'])
        if kn in ARAMI:
            sor += '; csak az arami tartomanyon belul levo eltereseket egyezonek veve %.2f%%, az arami + cimkezes sorokat egyezonek veve %.2f%% (tajekoztato szamitas, NEM a kuszob alapja)' % (
                100.0 * (egd[kn] + sz['arami']) / nev, 100.0 * (egd[kn] + sz['arami'] + sz['cimkezes']) / nev)
        else:
            sor += '; a cimkezes sorokat egyezonek veve %.2f%% (tajekoztato, NEM a kuszob alapja)' % (100.0 * (egd[kn] + sz['cimkezes']) / nev)
        cim.append(sor)
    # a harom konyv oka, egy-egy mondatban (a szamokat a fenti szamlalok adjak)
    def par_db(mag, h, e):
        return sum(1 for r in nem_egyezo if r[0] == mag and h in r[3].split() and e in r[4].split())

    sz2, sze, szd = kat_szamlalo['2Sám'][1], kat_szamlalo['Ezsd'][1], kat_szamlalo['Dán'][1]
    cim.append('OK 2Sam: nem szamozasi eltereses, hanem %d szetszort, egyedi Strong-eltereses (%d cimkezes, %d egyeb; arami nincs): a TAHOT es a BSB egy-ket szavat mas Strong-szammal cimkezi, egy-egy versben; egyetlen vers sem illik a szomszedos MT-versre.' % (
        sum(sz2.values()), sz2['cimkezes'], sz2['egyeb']))
    cim.append('OK Ezsd: a %d nem egyezobol %d esik az arami tartomanyba (ebbol %d a H1247 (TAHOT) / H1123 (BSB) par, a H1123 a TAHOT_kivonatban nem szerepel), %d cimkezes, %d egyeb a heber szakaszokban: az arami cimkezes az ok egy resze, de nem az egesz.' % (
        sum(sze.values()), sze['arami'], par_db('Ezsd', 'H1247', 'H1123'), sze['cimkezes'], sze['egyeb']))
    cim.append('OK Dan: a felteves (arami cimkezes) a fo okra CAFOLVA: a %d nem egyezobol csak %d esik az arami tartomanyba (ebbol %d a H1247/H1123 par), %d cimkezes, ezek mind az arami tartomanyon kivul, a heber fejezetekben vannak, tobbsegukben a Daniel-nev (H1840 TAHOT / H1841 BSB, %d vers), %d egyeb.' % (
        sum(szd.values()), szd['arami'], par_db('Dán', 'H1247', 'H1123'), szd['cimkezes'], par_db('Dán', 'H1840', 'H1841'), szd['egyeb']))
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_nem_egyezo_versek.tsv'),
                 kozos.fejlec(bi.URL + ' + konkordancia/TAHOT_kivonat.tsv', 'BSB commit ' + commit, parancs) + cim,
                 ['konyv', 'bsb_vers', 'mt_vers', 'tahot_nincs_bsbben', 'bsb_tobblet', 'okkategoria'], nem_egyezo)
    print('--- nem egyezo egysegek konyvenkent: szamozas / arami / cimkezes / egyeb (nevezo)')
    for kn, (nev, sz) in kat_szamlalo.items():
        print(kn, sz['szamozas'], sz['arami'], sz['cimkezes'], sz['egyeb'], '(%d)' % nev, 'arami-cimke=%d' % kat_aramikeresztbe[kn])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--munka', required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--f16', action='store_true', help='a F16 tajekoztato eltolas-diagnozis (naplok/F16_bsb_verseltolas_diagnozis.tsv)')
    g.add_argument('--f41', action='store_true', help='a F41 versszintu megfeleltetes (alapertelmezett)')
    a = ap.parse_args()
    if a.f16:
        fut_f16(a.munka, 'python eszkozok/fj2/bsb_verseltolas_diag.py --munka <mappa> --f16')
    else:
        f41_futtat(a.munka, 'python eszkozok/fj2/bsb_verseltolas_diag.py --munka <mappa> --f41')


if __name__ == '__main__':
    main()
