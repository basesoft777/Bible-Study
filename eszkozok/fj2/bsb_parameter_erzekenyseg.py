#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_parameter_erzekenyseg.py -- F41 (DT-F41g): a `Számozás` kriterium (wlc_versek.vers_igazolt) PARAMETER-ERZEKENYSEGI vizsgalata, reprodukalhato naplo.

A konkordancia/BSB_Strongs.tsv Igehely-versszamozasan (a fajl 7. oszlopa nem kell, csak az Igehely + Strong-halmaz) ujraszamolja a mt / kjv / ellenorizetlen cimkeket tobb
parameter-beallitassal, es kimutatja:
  - az mt / kjv / ellenorizetlen darabszamot (vers es sor), az ellenorizetlen fejezetek szamat;
  - a 23 korabban teves vers (20 teves `mt` + 3 hibrid reszvers) cimkejet (a helyes: egyik sem `mt`);
  - a kontroll-versek (Hos 12:1, Jon 2:1, Ezs 8:23, 1Sam 24:1, 1Kir 22:43/44, 4Moz 30:1) es kontroll-fejezetek (Hos 12, Jon 2, 1Sam 24, 1Kir 22, 4Moz 12/13/30) mt-aranyat
    (a helyes: mt);
  - a Job 40:1/3/6 cimkejet.
Parameterek: ABLAK (a szomszed fejezetek szelso versei a kornyezetben), a (d) reszvers-szuro arany/darab kuszobe, es a MARGO (a (b)/(c) pontban a WLC-vers atfedese legalabb
MARGO-val legyen jobb a tobbinel; a 0,2-es valtozat a DT-F41g korabbi ("3 000 ellenorizetlen vers") allitasanak reprodukcioja). Kulon sor: a korabbi (F41.10) egyvers-kuszob
(csak atfedes > 0,5) -- ez mutatja, hogy a szigoritas nelkul a teves versek `mt` cimket kapnak.
A baseline (alap) sor a fajl 7. oszlopaval osszevetve: 0 elteres, kulonben leallas.

Kimenet (GENERALT, kezzel nem szerkesztendo; csv nelkul, split('\\t')): naplok/F41_parameter_erzekenyseg.tsv, naplok/F41_parameter_erzekenyseg.md
Hasznalat: python eszkozok/fj2/bsb_parameter_erzekenyseg.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb_import as bi  # noqa: E402
import bsb_wlc_versszam_ellenorzes as ell  # noqa: E402
import wlc_versek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# (nev, ablak, d_arany, d_db, margo, regi_egyvers)
KONFIGOK = [
    ('alap (DT-F41g)', 20, 0.5, 2, 0.0, False),
    ('ablak=5', 5, 0.5, 2, 0.0, False),
    ('ablak=10', 10, 0.5, 2, 0.0, False),
    ('ablak=30', 30, 0.5, 2, 0.0, False),
    ('d: nincs reszvers-szuro', 20, 0.5, 10 ** 6, 0.0, False),
    ('d: arany=0.3', 20, 0.3, 2, 0.0, False),
    ('d: arany=0.7', 20, 0.7, 2, 0.0, False),
    ('d: db=1', 20, 0.5, 1, 0.0, False),
    ('d: db=3', 20, 0.5, 3, 0.0, False),
    ('margo=0.1', 20, 0.5, 2, 0.1, False),
    ('margo=0.2', 20, 0.5, 2, 0.2, False),
    ('regi egyvers-kuszob (F41.10: csak atfedes>0,5)', 20, 0.5, 2, 0.0, True),
]

# a 23 korabban teves vers (ELLENOR_F41_3 1. eltereses): 20 teves `mt` (formulas szomszed) + 3 hibrid reszvers
TEVES = [('1Móz', 32, 28), ('2Móz', 8, 15), ('3Móz', 6, 1), ('4Móz', 17, 1), ('4Móz', 17, 8), ('4Móz', 17, 9), ('5Móz', 23, 3), ('5Móz', 23, 20), ('1Sám', 21, 5),
         ('2Kir', 12, 1), ('2Kir', 12, 7), ('2Kir', 12, 15), ('1Krón', 6, 1), ('1Krón', 6, 22), ('Neh', 7, 70), ('Neh', 7, 71), ('Neh', 10, 31), ('Ez', 21, 1),
         ('Ez', 21, 2), ('Zak', 2, 1), ('4Móz', 26, 1), ('1Sám', 20, 42), ('1Krón', 12, 4)]
KONTROLL_VERS = [('Hós', 12, 1), ('Jón', 2, 1), ('Ézs', 8, 23), ('1Sám', 24, 1), ('1Kir', 22, 43), ('1Kir', 22, 44), ('4Móz', 30, 1)]
KONTROLL_FEJEZET = [('Hós', 12), ('Jón', 2), ('1Sám', 24), ('1Kir', 22), ('4Móz', 12), ('4Móz', 13), ('4Móz', 30)]
JOB40 = [('Jób', 40, 1), ('Jób', 40, 3), ('Jób', 40, 6)]

FEJ = ['konfig', 'ablak', 'd_arany', 'd_db', 'margo', 'mt_vers', 'kjv_vers', 'ellenorizetlen_vers', 'mt_sor', 'kjv_sor', 'ellenorizetlen_sor', 'ellenorizetlen_fejezet',
       'valtozas_az_alaphoz_vers', 'tevesek23_mt_db', 'tevesek23_mt_lista', 'kontroll_versek_mt', 'kontroll_versek_nem_mt', 'kontroll_fejezetek_mt_arany', 'job40_1_3_6']


def cimke(mag, c, v, wlc, widx, bfej, bsb_konyv, regi):
    h = bsb_konyv[(c, v)]
    if regi:
        egyezik = wlc_versek.vers_egyezik(wlc.get((c, v), set()), h)
    else:
        parok = [(wlc[(c, v + d)], bsb_konyv[(c, v + d)]) for d in (-1, 1) if (c, v + d) in bsb_konyv and (c, v + d) in wlc]
        egyezik = wlc_versek.vers_igazolt(wlc, widx, [(c, v)], h, wlc_versek.bsb_kornyezet(bfej, c, v), parok)
    return ell.elvart(mag, c, egyezik)


def fut():
    versek, szam = ell.bsb_strongs_olvas()
    konyvek = bi.konyvek()[:39]
    adat = {}
    for step, mag, ny in konyvek:
        if step not in versek:
            continue
        wlc = wlc_versek.wlc_konyv(wlc_versek.macula_kod(step))
        bfej = {}
        for (cc, vv), h in versek[step].items():
            bfej.setdefault(cc, {})[vv] = h
        adat[mag] = (step, wlc, wlc_versek.wlc_index(wlc), bfej, versek[step])
    alap = None
    fajl_elteres = None
    sorok, md_sorok = [], []
    for nev, ablak, d_arany, d_db, margo, regi in KONFIGOK:
        wlc_versek.ABLAK, wlc_versek.D_ARANY, wlc_versek.D_DB, wlc_versek.MARGO = ablak, d_arany, d_db, margo
        cim = {}
        for mag, (step, wlc, widx, bfej, bk) in adat.items():
            for (c, v) in bk:
                cim[(mag, c, v)] = cimke(mag, c, v, wlc, widx, bfej, bk, regi)
        sorsz = {k: sum(szam[(adat[k[0]][0], k[1], k[2])].values()) for k in cim}
        vdb = {a: sum(1 for x in cim.values() if x == a) for a in bi.SZAMOZASOK}
        sdb = {a: sum(sorsz[k] for k, x in cim.items() if x == a) for a in bi.SZAMOZASOK}
        ell_fej = len({(k[0], k[1]) for k, x in cim.items() if x == 'ellenorizetlen'})
        if alap is None:  # a baseline a fajl 7. oszlopaval: 0 elteres
            alap = dict(cim)
            fajl_elteres = [k for k in cim if set(szam[(adat[k[0]][0], k[1], k[2])]) != {cim[k]}]
            if fajl_elteres:
                raise SystemExit('HIBA: az alap-konfiguracio elter a BSB_Strongs.tsv 7. oszlopatol (%d vers); elso: %s' % (len(fajl_elteres), fajl_elteres[:5]))
        valt = sum(1 for k in cim if cim[k] != alap[k])
        tev_mt = ['%s %d:%d' % t for t in TEVES if cim.get(t) == 'mt']
        kv_nem = ['%s %d:%d=%s' % (t + (cim.get(t, 'nincs'),)) for t in KONTROLL_VERS if cim.get(t) != 'mt']
        kv_mt = sum(1 for t in KONTROLL_VERS if cim.get(t) == 'mt')
        kf = []
        for mag, c in KONTROLL_FEJEZET:
            vs = [k for k in cim if k[0] == mag and k[1] == c]
            kf.append('%s %d: %d/%d' % (mag, c, sum(1 for k in vs if cim[k] == 'mt'), len(vs)))
        j40 = ', '.join('%s %d:%d=%s' % (t + (cim.get(t, 'nincs'),)) for t in JOB40)
        sorok.append((nev, str(ablak), str(d_arany), str(d_db) if d_db < 10 ** 6 else 'ki', str(margo), str(vdb['mt']), str(vdb['kjv']), str(vdb['ellenorizetlen']),
                      str(sdb['mt']), str(sdb['kjv']), str(sdb['ellenorizetlen']), str(ell_fej), str(valt), '%d/%d' % (len(tev_mt), len(TEVES)), '; '.join(tev_mt) or '-',
                      '%d/%d' % (kv_mt, len(KONTROLL_VERS)), '; '.join(kv_nem) or '-', '; '.join(kf), j40))
    fej = kozos.fejlec('konkordancia/BSB_Strongs.tsv + konkordancia/Macula_heber_*.tsv (WLC)', 'F41, DT-F41g paraméter-érzékenység',
                       'python eszkozok/fj2/bsb_parameter_erzekenyseg.py')
    fej += ['GENERÁLT, kézzel nem szerkesztendő. Az alap sor (DT-F41g: ABLAK=20, (d) arány 0,5 / darab ≥ 2, margó 0) a BSB_Strongs.tsv 7. oszlopával összevetve: 0 eltérés. '
            'Egység: vers = az Igehely-vers (%d vers); sor = a BSB_Strongs.tsv sora.' % len(alap),
            'margo = a (b)/(c) pontban a WLC-vers átfedése legalább ennyivel legyen jobb a többinél (0 = szigorúan jobb); a "d_db = ki" a részvers-szűrő kikapcsolása; '
            'a "régi egyvers-küszöb" az F41.10 kritérium (csak átfedés > 0,5).',
            'tevesek23 = a 23 korábban téves vers (20 téves mt + 3 hibrid részvers), a helyes eredmény 0/23 mt; kontroll = a helyesen mt versek / fejezetek, a helyes: minden mt.']
    ell.tsv_ir_nagy(os.path.join(kozos.NAPLOK, 'F41_parameter_erzekenyseg.tsv'), fej, FEJ, sorok)
    md = ['# GENERÁLT: python eszkozok/fj2/bsb_parameter_erzekenyseg.py — F41 paraméter-érzékenység (DT-F41g); kézzel nem szerkesztendő', '',
          'A `Számozás` kritérium (`wlc_versek.vers_igazolt`) paraméterei és hatásuk; részletek: `naplok/F41_parameter_erzekenyseg.tsv`. Egység: Igehely-vers (összesen %d).' % len(alap), '',
          '| konfig | mt | kjv | ellenorizetlen | ell. fejezet | változás az alaphoz | téves 23-ból mt | kontroll vers mt |', '|---|---|---|---|---|---|---|---|']
    for s in sorok:
        md.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (s[0], s[5], s[6], s[7], s[11], s[12], s[13], s[15]))
    md += ['', '**Kontroll-fejezetek (mt/összes vers) konfigurációnként:**', '']
    for s in sorok:
        md.append('- %s: %s' % (s[0], s[17]))
    md += ['', '**Job 40:1/3/6:** ' + sorok[0][18] + ' (alap).', '']
    with open(os.path.join(kozos.NAPLOK, 'F41_parameter_erzekenyseg.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md))
    for s in sorok:
        print('\t'.join(s[:15] + s[15:17]))


if __name__ == '__main__':
    fut()
