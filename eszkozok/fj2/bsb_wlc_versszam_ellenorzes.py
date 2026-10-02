#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_wlc_versszam_ellenorzes.py -- F41 (FELADATOK #41, 9. lepes): a konkordancia/BSB_Strongs.tsv Igehely-versszamozasanak gepi ellenorzese a WLC-vel
(konkordancia/Macula_heber_*.tsv, `ref` = a Macula/WLC szamozas; wlc_versek.py). Ez szuri a HIBRID szamozast: azokat a fejezeteket, amelyek Igehelye nem a WLC-szamozas.

Ket kimenet (mindketto GENERALT, kezzel nem szerkesztendo; csv nelkul, split('\\t')):
  1. naplok/F41_wlc_versszam_ellenorzes.tsv -- fejezetenkent (a BSB_Strongs.tsv minden fejezete + a WLC azon fejezetei, amelyeknek nincs BSB-sora):
       konyv, fejezet, szamozas_jelzo (a fejezet sorainak 7. oszlopa: tahot_szamozas / kjv_szamozas), bsb_versek, bsb_max, wlc_versek, wlc_max,
       bsb_nincs_wlcben (az Igehely-versek, amelyek nincsenek a WLC fejezetben), wlc_nincs_bsbben (darab), egyezes_szazalek, wlc_egyezik (igen/nem), kategoria.
     egyezes_szazalek = azon kozos versek hanyada (a WLC-ben nem ures Strong-halmazu versek kozul), ahol a WLC-vers Strong-halmazanak tobb mint a fele a BSB-versben van
     (azonos modszer, mint a bsb_import.versillesztes: hanyad > 0,5). wlc_egyezik = igen, ha bsb_nincs_wlcben ures ES az egyezes_szazalek >= 90 (a mert eloszlas ketcsucsu:
     a fejezetek 29-nal kevesebb vagy 90 feletti ertekeket adnak; l. a fejlec hisztogramja).
     kategoria: wlc_egyezik / wlc_elter (az Igehely-szamozas nem WLC, a fejezet nincs KJV-jelolve: hibrid) / kjv_jelolt (a sorok 7. oszlopa kjv_szamozas: kulon kategoria; a wlc_egyezik
     oszlop ettol fuggetlenul megmondja, hogy a megtartott KJV-szamozas egyezik-e a WLC-vel) / nincs_bsb_sor (a WLC fejezetnek nincs BSB_Strongs-sora: nem importalt konyv vagy fejezet).
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

KUSZOB_SZAZALEK = 90.0
FEJ1 = ['konyv', 'fejezet', 'szamozas_jelzo', 'bsb_versek', 'bsb_max', 'wlc_versek', 'wlc_max', 'bsb_nincs_wlcben', 'wlc_nincs_bsbben', 'egyezes_szazalek', 'wlc_egyezik', 'kategoria']
FEJ2 = ['konyv', 'fejezet', 'bsb_max', 'wlc_max', 'tahot_max', 'tahot_modell', 'kovetkeztetes']


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
    """({STEP-kod: {(fej, vers): set(Strong int)}}, {(STEP-kod, fej): {Szamozas: darab}}) a konkordancia/BSB_Strongs.tsv-bol (split('\\t'))."""
    versek, szam = {}, {}
    with open(os.path.join(kozos.KONKORDANCIA, 'BSB_Strongs.tsv'), encoding='utf-8', newline='') as f:
        fej = f.readline().rstrip('\n').split('\t')
        if fej[:7] != ['Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó', 'Morfológiai kód', 'Angol szó állapota', 'Számozás']:
            raise SystemExit('HIBA: a BSB_Strongs.tsv fejlece nem a vart 7 oszlopos: %s' % fej)
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if len(m) != 7:
                raise SystemExit('HIBA: nem 7 oszlopos sor: %r' % sor)
            b, c, v = m[0].split('.')
            n = kozos.strong_szam(m[2])
            h = versek.setdefault(b, {}).setdefault((int(c), int(v)), set())
            if n is not None and n < 9000:
                h.add(n)
            d = szam.setdefault((b, int(c)), {})
            d[m[6]] = d.get(m[6], 0) + 1
    return versek, szam


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
    hiszto = {}
    for step, mag, ny in konyvek:
        kod = wlc_versek.macula_kod(step)
        wlc = wlc_versek.wlc_konyv(kod)
        wmax = wlc_versek.wlc_fejezet_max(wlc)
        fmag = bi.forras_nev(mag)
        bsb_konyv = versek.get(step, {})
        # 1. fejezetenkenti ellenorzes
        for c in sorted(set(wmax) | {c for c, v in bsb_konyv}):
            wv = {v for (cc, v) in wlc if cc == c}
            bv = {v for (cc, v) in bsb_konyv if cc == c}
            if not bv:
                sorok1.append((mag, str(c), '', '0', '0', str(len(wv)), str(max(wv)) if wv else '0', '', str(len(wv)), '', 'nem',
                               'nincs_bsb_sor'))
                continue
            kozos_versek = [v for v in sorted(bv) if v in wv and wlc[(c, v)]]
            ok = sum(1 for v in kozos_versek if len(wlc[(c, v)] & bsb_konyv[(c, v)]) / len(wlc[(c, v)]) > 0.5)
            pc = 100.0 * ok / len(kozos_versek) if kozos_versek else 0.0
            nincs = sorted(bv - wv)
            jelzo = szam[(step, c)]
            jelzo_ertek = 'kjv_szamozas' if jelzo.get('kjv_szamozas') else 'tahot_szamozas'
            if len(jelzo) > 1:
                jelzo_ertek = '+'.join(sorted(jelzo))  # vegyes jelolesu fejezet (nem varhato: hibakent latszik)
            egyezik = (not nincs) and pc >= KUSZOB_SZAZALEK
            if jelzo_ertek == 'kjv_szamozas':
                kat = 'kjv_jelolt'
            else:
                kat = 'wlc_egyezik' if egyezik else 'wlc_elter'
            sav = min(int(pc // 10) * 10, 90)
            hiszto[sav] = hiszto.get(sav, 0) + 1
            sorok1.append((mag, str(c), jelzo_ertek, str(len(bv)), str(max(bv)), str(len(wv)), str(max(wv)) if wv else '0',
                           ' '.join(str(x) for x in nincs), str(len(wv - bv)), '%.1f' % pc, 'igen' if egyezik else 'nem', kat))
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
        kat_db[s[11]] = kat_db.get(s[11], 0) + 1
    fej = kozos.fejlec('konkordancia/BSB_Strongs.tsv + konkordancia/Macula_heber_*.tsv (WLC, `ref` oszlop)', 'WLC: Macula Hebrew (l. naplok/F17_import_naplo.md)',
                       'python eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py')
    fej1 = fej + ['F41 9. lepes: a BSB_Strongs.tsv Igehely-versszamozasa vs WLC, fejezetenkent; l. a szkript docstringjet (kategoriak, egyezes_szazalek)',
                  'kategoria-darabszamok (fejezet): ' + '; '.join('%s=%d' % kv for kv in sorted(kat_db.items())),
                  'egyezes_szazalek-hisztogram (a BSB-sorral rendelkezo fejezetek, 10%-os savok): ' + '; '.join('%d-%d=%d' % (k, k + 10, v) for k, v in sorted(hiszto.items())) + (' (a 30 es 90 kozotti savok uresek: a kuszob (90%) nem vag el valos fejezetet)' if not any(hiszto.get(b, 0) for b in (30, 40, 50, 60, 70, 80)) else ' (FIGYELEM: van fejezet a 30-90% savban: a 90%-os kuszob felulvizsgalando)'),
                  'konyvenkent a wlc_elter / kjv_jelolt+nem fejezetek: ' + '; '.join('%s: %s' % (m, ' '.join(s[1] for s in sorok1 if s[0] == m and (s[11] == 'wlc_elter' or (s[11] == 'kjv_jelolt' and s[10] == 'nem')))) for m in dict.fromkeys(s[0] for s in sorok1 if s[11] == 'wlc_elter' or (s[11] == 'kjv_jelolt' and s[10] == 'nem'))),
                  'FIGYELEM: a wlc_elter (hibrid) fejezetek Igehelye a TAHOT_kivonat versszamozasa, amely 25 ószövetsegi konyvben nem azonos a WLC-vel (N-F41d); a `tahot_szamozas` jelzo ezt NEM mondja ki WLC-egyezesnek: az egyezest ez a naplo adja. Az atszamozas (BSB/TAHOT -> WLC) kulon N-tetel, nem az F41 feladata.']
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_wlc_versszam_ellenorzes.tsv'), fej1, FEJ1, sorok1)
    fej2 = fej + ['F41 1. lepes (DT-F41c (a)): fejezethatar-vizsgalat; csak azok az OSZ-fejezetek, ahol a BSB(KJV), a WLC es a TAHOT_kivonat fejezet-maximuma nem mind azonos, vagy a TAHOT-megfeleltetes nem csupa azonos',
                  'bsb_max = a BSB (KJV) fejezet utolso verse (naplok/F41_bsb_megfeleltetes.tsv bsb_vers); wlc_max = a Macula (WLC) fejezet utolso verse; tahot_max = a konkordancia/TAHOT_kivonat.tsv fejezet-max; tahot_modell = a F41.1 BSB->TAHOT megfeleltetes modelljei a fejezet BSB-versein']
    tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_wlc_hatar_ellenorzes.tsv'), fej2, FEJ2, sorok2)
    print('kategoriak:', sorted(kat_db.items()))
    print('hisztogram:', sorted(hiszto.items()))
    print('fejezetek: %d; hatar-sorok: %d' % (len(sorok1), len(sorok2)))
    for s in sorok2:
        if (s[0], s[1]) in {('Préd', '11'), ('Préd', '12'), ('Ézs', '2'), ('Ézs', '3')}:
            print('\t'.join(s))


if __name__ == '__main__':
    fut()
