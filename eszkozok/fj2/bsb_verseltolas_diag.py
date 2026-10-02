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
naplok/F41_bsb_megfeleltetes.tsv (konyv, bsb_vers, mt_vers, modell, ok) a --f41 futasnal.
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


def kk_betolt():
    """A Karoli-kulcs sorai: [(igehely_karoli, igehely_kjv, igehely_mt, osztaly)]."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Karoli_versmegfeleltetes.tsv'))
    nevek = ('igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly')
    idx = [fej.index(n) for n in nevek]
    return [tuple(s[i] if len(s) > i else '' for i in idx) for s in sorok]


def kk_max_tabla(kk):
    """{konyv(forras-nev): {MT-fejezet: max vers}} a Karoli-kulcs igehely_mt oszlopabol (csak a `fej:vers` alaku ertekek;
    a KJV-osztaly soraibol nem: ott az igehely_mt ures, es a Karoli-szamozas nem mindig az MT-szamozas)."""
    ki = {}
    for kar, kjv, mt, osz in kk:
        ref = mt
        m = re.fullmatch(r'(\d+):(\d+)', ref)
        if not m:
            continue
        k = kar.rsplit(' ', 1)[0]
        d = ki.setdefault(k, {})
        f, v = int(m.group(1)), int(m.group(2))
        d[f] = max(d.get(f, 0), v)
    return ki


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


def f41_futtat(munka, parancs):
    cel = os.path.join(munka, 'bsb-data-output')
    mappa = os.path.join(cel, 'base', 'display')
    commit = kozos.commit_sha(cel)
    tahot = bi.forras_halmazok('H')
    kk = kk_betolt()
    kkmax = kk_max_tabla(kk)
    fej, lef = kozos.tsv_olvas(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'))
    li = {n: fej.index(n) for n in ('egyezes_szazalek', 'eredmeny', 'importalt_sorok')}
    regi = {bi.forras_nev(s[0]): s for s in lef if s[2] == 'heber'}
    tsv_sorok, osszegzes, kk_elt, reg_zsolt = [], [], [], []
    for step, mag, nyelv in bi.konyvek()[:39]:
        fmag = bi.forras_nev(mag)
        kod = step.upper()
        bmappa = os.path.join(mappa, kod)
        fejezetek = sorted(int(m.group(1)) for fn in os.listdir(bmappa)
                           for m in [re.fullmatch(kod + r'(\d+)\.json', fn)] if m)
        bsb_fej, sorszam = {}, {}
        for f in fejezetek:
            with open(os.path.join(bmappa, '%s%d.json' % (kod, f)), encoding='utf-8') as fh:
                adat = json.load(fh)
            bsb_fej[f] = bi.vers_strongok(adat, 'H')
            for sor in bi.vers_sorok(adat, step, f):
                v = int(sor[0].rsplit('.', 1)[1])
                sorszam[(f, v)] = sorszam.get((f, v), 0) + 1
        forras = tahot
        sorok, allapot, tmax = bi.konyv_megfeleltetes(mag, bsb_fej, forras, kkmax.get(fmag))
        mtd = dict(bi.mt_versek(forras, fmag)[0])
        nev = eg = 0
        eltolt_fej, ill_fej, atszam_sor, kieso_sor, n_eltolt = {}, {}, 0, 0, 0
        for (f, v), x, modell, ok in sorok:
            tsv_sorok.append((mag, '%d:%d' % (f, v), ('%d:%d' % x) if x else '', modell, ok))
            if modell == 'illesztetlen':
                ill_fej.setdefault(f, ok)
                kieso_sor += sorszam.get((f, v), 0)
                continue
            if x in mtd:
                nev += 1
                if mtd[x] <= bsb_fej[f][v]:
                    eg += 1
            if modell == 'eltolt':
                n_eltolt += 1
                eltolt_fej.setdefault(f, set()).add((x[0] - f, x[1] - v))
                atszam_sor += sorszam.get((f, v), 0)
        r = regi[fmag]
        osszegzes.append((mag, r[li['egyezes_szazalek']], '%.2f' % (100.0 * eg / nev) if nev else '0', str(eg), str(nev),
                          r[li['eredmeny']], len(eltolt_fej), n_eltolt, atszam_sor, len(ill_fej), kieso_sor, eltolt_fej, ill_fej))
        # Karoli-kulcs igehely_kjv ellenorzes: a BSB (KJV-szamozas) verse -> a mi MT-versunk vs. a kulcs MT-verse
        meg = {(f, v): x for (f, v), x, modell, ok in sorok if x}
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
                if modell != 'illesztetlen' and x != (f, v + k_regi[f]):
                    kul += 1
            reg_zsolt.append(kul)
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_bsb_megfeleltetes.tsv'),
                 kozos.fejlec(bi.URL + ' + konkordancia/TAHOT_kivonat.tsv + konkordancia/Karoli_versmegfeleltetes.tsv (igehely_mt, ellenorzes)',
                              'BSB commit ' + commit, parancs)
                 + ['versszintu BSB-vers -> MT-vers megfeleltetes mind a 39 OSZ-konyvre (F41.1); bsb_vers = a BSB (display-JSON) fejezet:verse; mt_vers = a konkordancia/TAHOT_kivonat.tsv szamozasa (a Karoli-kulcs MT-oszlopa a fejezet-maximumot igazolja)',
                    'modell: azonos = mt_vers = bsb_vers; eltolt = mas fejezet:vers (fejezethataron atnyulo eset is); illesztetlen = a fejezet megfeleltetese nem igazolhato, a fejezet nem szamit a meresbe es az importba (mt_vers ures)',
                    'a megfeleltetes forrasa a Strong-illeszkedes (monoton 1:1 igazitas, a TAHOT-vers Strong-halmazanak BSB-ben levo hanyada > 0,5); fejezetenkenti igazolas: nincs_mt_part / vers_osztas / mt_vers_kimarad / kk_max_eltérés (l. bsb_import.konyv_megfeleltetes)',
                    'ok (azonos/eltolt): strong_illeszkedik = a TAHOT-vers Strongjai a BSB-vers reszei; strong_nem_egyezo = megfeleltetett, de nem egyezo vers; tahot_nincs_vers = a megfeleltetett MT-vers nincs a TAHOT_kivonatban; kitoltve_a_szomszedok_eltolasabol = a vers nem illesztheto, a fejezeten belüli szomszedai azonos eltolasuak'],
                 ['konyv', 'bsb_vers', 'mt_vers', 'modell', 'ok'], tsv_sorok)
    print('KONYV\tregi%\tuj%\tegyezo\tnevezo\tregi_eredmeny\teltolt_fej\teltolt_vers\tatszamozott_sor\tillesztetlen_fej\tkieso_sor')
    for o in osszegzes:
        print('\t'.join(str(x) for x in o[:11]))
    print('--- eltolt fejezetek (BSB fejezet: (dfej,dvers) halmaz)')
    for o in osszegzes:
        if o[11]:
            print(o[0], {f: sorted(d) for f, d in sorted(o[11].items())})
    print('--- illesztetlen fejezetek')
    for o in osszegzes:
        for f, ok in sorted(o[12].items()):
            print(o[0], f, ok)
    print('--- KK igehely_kjv ellenorzes: konyv, osszehasonlitott, elteres')
    for k in kk_elt:
        if k[2]:
            print(k[0], k[1], k[2])
            for p in k[3]:
                print('   ', p)
    print('Zsolt regresszio (a F16.8-modelltol eltero, nem illesztetlen vers): %s' % reg_zsolt)


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
