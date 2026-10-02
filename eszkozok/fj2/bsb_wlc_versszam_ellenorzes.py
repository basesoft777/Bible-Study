#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_wlc_versszam_ellenorzes.py -- F41 (FELADATOK #41, 9. lepes; DT-F41f: VERSSZINTU atiras): a konkordancia/BSB_Strongs.tsv Igehely-versszamozasanak gepi ellenorzese a WLC-vel
(konkordancia/Macula_heber_*.tsv, `ref` = a Macula/WLC szamozas; wlc_versek.py). A referencia a WLC; a TAHOT_kivonat szama nem MT-forras.

Versszintu igazolas (wlc_versek.vers_egyezik): egy Igehely-vers `mt`, ha a WLC azonos szamu versenek (nem ures) Strong-halmazanak TOBB MINT FELE az Igehely-vers sorainak
Strong-halmazaban van (azonos modszer, mint a bsb_import.versillesztes). A szkript a BSB_Strongs.tsv-bol FUGGETLENUL ujraszamolja, es osszeveti a fajl 7. oszlopaval (`Számozás`:
mt / kjv / ellenorizetlen); elteresnel hibaval all le. Elvart ertek: mt, ha a vers egyezik; kulonben kjv (csak Job 38-41: a BSB(KJV)-szam marad), kulonben ellenorizetlen.
(A korabbi, fejezetszintu valtozat -- az Igehely-versek halmaza vs a WLC-fejezet versei -- a reszfejezetes teves egyezest adta: BSB ⊆ WLC, pl. 4Moz 12, 25/26; ez megszunt.)

Ket kimenet (mindketto GENERALT, kezzel nem szerkesztendo; csv nelkul, split('\\t')):
  1. naplok/F41_wlc_versszam_ellenorzes.tsv -- fejezetenkent (a BSB_Strongs.tsv minden fejezete + a WLC azon fejezetei, amelyeknek nincs BSB-sora):
       konyv, fejezet, bsb_versek, bsb_max, wlc_versek, wlc_max, mt_versek, kjv_versek, ellenorizetlen_versek (az Igehely-versek darabszama 7. oszlop szerint), sorok_mt,
       sorok_kjv, sorok_ellenorizetlen (a BSB_Strongs.tsv sorainak darabszama), ellenorizetlen_versek_lista, bsb_nincs_wlcben (az Igehely-versek, amelyek nincsenek a WLC fejezetben),
       wlc_nincs_bsbben (darab), kategoria: mt (minden vers mt) / reszben_mt (van mt es nem igazolt vers is) / nem_igazolt (nincs mt vers: kjv vagy ellenorizetlen) /
       nincs_bsb_sor (a WLC fejezetnek nincs BSB_Strongs-sora: nem importalt konyv vagy fejezet).
  2. naplok/F41_wlc_hatar_ellenorzes.tsv -- a fejezethatar-vizsgalat (F41, DT-F41c (a) 1. pont): azokra az OSZ-fejezetekre, ahol a BSB(KJV) fejezet-max, a WLC fejezet-max es a
       TAHOT_kivonat fejezet-max nem mind azonos: konyv, fejezet, bsb_max (naplok/F41_bsb_megfeleltetes.tsv), wlc_max, tahot_max, tahot_modell, kovetkeztetes
     (bsb=wlc: a KJV-szam MT-szam, a TAHOT_kivonat attol eltero (Karoli-szeru) / tahot=wlc: a TAHOT_kivonat MT-szamozasu, a KJV elter / bsb=tahot!=wlc: a TAHOT_kivonat KJV-szamozasu
     (hibrid) / egyik sem).
Hasznalat: python eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb_import as bi  # noqa: E402
import wlc_versek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FEJ1 = ['konyv', 'fejezet', 'bsb_versek', 'bsb_max', 'wlc_versek', 'wlc_max', 'mt_versek', 'kjv_versek', 'ellenorizetlen_versek', 'sorok_mt', 'sorok_kjv',
        'sorok_ellenorizetlen', 'ellenorizetlen_versek_lista', 'bsb_nincs_wlcben', 'wlc_nincs_bsbben', 'kategoria']
FEJ2 = ['konyv', 'fejezet', 'bsb_max', 'wlc_max', 'tahot_max', 'tahot_modell', 'kovetkeztetes']
SZAMOZASOK = bi.SZAMOZASOK


def tsv_ir_nagy(ut, fejlec_sorok, oszlopok, sorok):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for h in fejlec_sorok:
            f.write('# %s\n' % kozos.tisztit(h))
        f.write('\t'.join(oszlopok) + '\n')
        for s in sorok:
            if len(s) != len(oszlopok):
                raise ValueError('oszlopszam-elteres: %s' % (s,))
            f.write('\t'.join(kozos.tisztit(x) for x in s) + '\n')


def bsb_strongs_olvas():
    """({STEP-kod: {(fej, vers): set(Strong int)}}, {(STEP-kod, fej, vers): {Szamozas: sorok}}) a konkordancia/BSB_Strongs.tsv-bol (split('\\t'))."""
    versek, szam = {}, {}
    with open(os.path.join(kozos.KONKORDANCIA, 'BSB_Strongs.tsv'), encoding='utf-8', newline='') as f:
        fej = f.readline().rstrip('\n').split('\t')
        if fej[:7] != ['Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó', 'Morfológiai kód', 'Angol szó állapota', 'Számozás']:
            raise SystemExit('HIBA: a BSB_Strongs.tsv fejlece nem a vart 7 oszlopos: %s' % fej)
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if len(m) != 7:
                raise SystemExit('HIBA: nem 7 oszlopos sor: %r' % sor)
            if m[6] not in SZAMOZASOK:
                raise SystemExit('HIBA: ervenytelen Szamozas: %r' % sor)
            b, c, v = m[0].split('.')
            n = kozos.strong_szam(m[2])
            h = versek.setdefault(b, {}).setdefault((int(c), int(v)), set())
            if n is not None and n < 9000:
                h.add(n)
            d = szam.setdefault((b, int(c), int(v)), {})
            d[m[6]] = d.get(m[6], 0) + 1
    return versek, szam


def elvart(mag, c, egyezik):
    if egyezik:
        return 'mt'
    return 'kjv' if c in bi.KJV_JELOLT_FEJEZETEK.get(mag, ()) else 'ellenorizetlen'


def megfeleltetes_bsb_max():
    """{(konyv_magyar, fejezet): (BSB max vers, set(modell))} a naplok/F41_bsb_megfeleltetes.tsv-bol (bsb_vers = a BSB (KJV) fejezet:vers)."""
    ki = {}
    with open(os.path.join(kozos.NAPLOK, 'F41_bsb_megfeleltetes.tsv'), encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#') or sor.startswith('konyv\t'):
                continue
            p = sor.rstrip('\n').split('\t')
            c, v = p[1].split(':')
            k = (p[0], int(c))
            mx, mod = ki.get(k, (0, set()))
            ki[k] = (max(mx, int(v)), mod | {p[3]})
    return ki


def fut():
    versek, szam = bsb_strongs_olvas()
    konyvek = bi.konyvek()[:39]
    tahot = kozos.tahot_strongok()
    sorok1, sorok2 = [], []
    ossz_vers = {a: 0 for a in SZAMOZASOK}
    ossz_sor = {a: 0 for a in SZAMOZASOK}
    elteres = []
    for step, mag, ny in konyvek:
        kod = wlc_versek.macula_kod(step)
        wlc = wlc_versek.wlc_konyv(kod)
        wmax = wlc_versek.wlc_fejezet_max(wlc)
        bsb_konyv = versek.get(step, {})
        for c in sorted(set(wmax) | {c for c, v in bsb_konyv}):
            wv = {v for (cc, v) in wlc if cc == c}
            bv = {v for (cc, v) in bsb_konyv if cc == c}
            if not bv:
                sorok1.append((mag, str(c), '0', '0', str(len(wv)), str(max(wv)) if wv else '0', '0', '0', '0', '0', '0', '0', '', '', str(len(wv)), 'nincs_bsb_sor'))
                continue
            vdb = {a: 0 for a in SZAMOZASOK}
            sdb = {a: 0 for a in SZAMOZASOK}
            ell = []
            for v in sorted(bv):
                egyezik = wlc_versek.vers_egyezik(wlc.get((c, v), set()), bsb_konyv[(c, v)])
                var = elvart(mag, c, egyezik)
                jel = szam[(step, c, v)]
                if set(jel) != {var}:
                    elteres.append('%s %d:%d: a 7. oszlop %s, a WLC-osszevetes szerint elvart %s' % (mag, c, v, dict(jel), var))
                vdb[var] += 1
                for a, n in jel.items():
                    sdb[a] += n
                if var != 'mt':
                    ell.append('%d%s' % (v, '' if var == 'ellenorizetlen' else '(kjv)'))
            for a in SZAMOZASOK:
                ossz_vers[a] += vdb[a]
                ossz_sor[a] += sdb[a]
            nincs = sorted(bv - wv)
            if vdb['mt'] == len(bv):
                kat = 'mt'
            elif vdb['mt']:
                kat = 'reszben_mt'
            else:
                kat = 'nem_igazolt'
            sorok1.append((mag, str(c), str(len(bv)), str(max(bv)), str(len(wv)), str(max(wv)) if wv else '0', str(vdb['mt']), str(vdb['kjv']), str(vdb['ellenorizetlen']),
                           str(sdb['mt']), str(sdb['kjv']), str(sdb['ellenorizetlen']), ' '.join(ell), ' '.join(str(x) for x in nincs), str(len(wv - bv)), kat))
    if elteres:
        raise SystemExit('HIBA: a BSB_Strongs.tsv 7. oszlopa eltér a versszintű WLC-összevetéstől (%d vers); első 10:\n%s' % (len(elteres), '\n'.join(elteres[:10])))
    # 2. fejezethatar-vizsgalat
    mf = megfeleltetes_bsb_max()
    for step, mag, ny in konyvek:
        wmax = wlc_versek.wlc_fejezet_max(wlc_versek.wlc_konyv(wlc_versek.macula_kod(step)))
        fmag = bi.forras_nev(mag)
        tmax = {}
        for r in tahot:
            if r.rsplit(' ', 1)[0] == fmag:
                c, v = bi._ref_bont(r)
                tmax[c] = max(tmax.get(c, 0), v)
        for c in sorted({cc for (m, cc) in mf if m == mag}):
            b, mod = mf[(mag, c)]
            w, t = wmax.get(c, 0), tmax.get(c, 0)
            if b == w == t and mod <= {'azonos'}:
                continue
            if b == w and t != w:
                kov = 'bsb=wlc: a KJV-szam MT-szam; a TAHOT_kivonat eltero (Karoli-szeru)'
            elif t == w and b != w:
                kov = 'tahot=wlc: a TAHOT_kivonat MT-szamozasu; a KJV elter'
            elif b == t and t != w:
                kov = 'bsb=tahot!=wlc: a TAHOT_kivonat KJV-szamozasu (hibrid)'
            elif b == w == t:
                kov = 'bsb=wlc=tahot (fejezet-max)'
            else:
                kov = 'egyik_sem'
            sorok2.append((mag, str(c), str(b), str(w), str(t), '+'.join(sorted(mod)), kov))
    kat_db = {}
    for s in sorok1:
        kat_db[s[15]] = kat_db.get(s[15], 0) + 1
    nem_mt = [s for s in sorok1 if s[15] in ('reszben_mt', 'nem_igazolt')]
    fej = kozos.fejlec('konkordancia/BSB_Strongs.tsv + konkordancia/Macula_heber_*.tsv (WLC, `ref` oszlop)', 'WLC: Macula Hebrew (l. naplok/F17_import_naplo.md)',
                       'python eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py')
    fej1 = fej + ['F41 9. lepes (DT-F41f): a BSB_Strongs.tsv Igehely-versszamozasa vs WLC, VERSSZINTEN; l. a szkript docstringjet (kategoriak, igazolas). A 7. oszlop (`Számozás`) minden verse ujraszamolva es egyezik a fajllal (0 elteres)',
                  'kategoria-darabszamok (fejezet): ' + '; '.join('%s=%d' % kv for kv in sorted(kat_db.items())),
                  'Igehely-versek a 7. oszlop szerint: ' + '; '.join('%s=%d' % kv for kv in ossz_vers.items()) + ' | sorok: ' + '; '.join('%s=%d' % kv for kv in ossz_sor.items()),
                  'a nem teljesen mt fejezetek (reszben_mt / nem_igazolt): ' + '; '.join('%s %s (%s)' % (s[0], s[1], s[15]) for s in nem_mt),
                  'FIGYELEM: az `ellenorizetlen` vers Igehelye a TAHOT_kivonat hibrid szamozasa (25 ószövetsegi konyvben nem azonos a WLC-vel, N-F41d) vagy a WLC-ben nincs ilyen szamu vers / ures a WLC-vers Strong-halmaza; a `kjv` a Job 38-41 nem igazolt versei (BSB(KJV)-szam marad). Az atszamozas (-> WLC) kulon N-tetel (N-F41g, N-F41h), nem az F41 feladata.']
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_wlc_versszam_ellenorzes.tsv'), fej1, FEJ1, sorok1)
    fej2 = fej + ['F41 1. lepes (DT-F41c (a)): fejezethatar-vizsgalat; csak azok az OSZ-fejezetek, ahol a BSB(KJV), a WLC es a TAHOT_kivonat fejezet-maximuma nem mind azonos, vagy a TAHOT-megfeleltetes nem csupa azonos',
                  'bsb_max = a BSB (KJV) fejezet utolso verse (naplok/F41_bsb_megfeleltetes.tsv bsb_vers); wlc_max = a Macula (WLC) fejezet utolso verse; tahot_max = a konkordancia/TAHOT_kivonat.tsv fejezet-max; tahot_modell = a F41.1 BSB->TAHOT megfeleltetes modelljei a fejezet BSB-versein']
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_wlc_hatar_ellenorzes.tsv'), fej2, FEJ2, sorok2)
    print('kategoriak:', sorted(kat_db.items()))
    print('versek:', ossz_vers, 'sorok:', ossz_sor)
    print('fejezetek: %d; hatar-sorok: %d' % (len(sorok1), len(sorok2)))
    print('nem teljesen mt fejezetek: %d' % len(nem_mt))
    for s in sorok2:
        if (s[0], s[1]) in {('Préd', '11'), ('Préd', '12'), ('Ézs', '2'), ('Ézs', '3'), ('4Móz', '12'), ('4Móz', '13'), ('4Móz', '29'), ('4Móz', '30')}:
            print('\t'.join(s))


if __name__ == '__main__':
    fut()
