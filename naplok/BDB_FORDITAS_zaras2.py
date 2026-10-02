#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_FORDITAS_zaras2.py -- F38 zaromenet 2. kor (DT-F38f, 2026.10.02).

Egy futas, a DT-F38f gepi es kezi javitasaival az adat/forditasok.tsv BDB
`teljes` soraira:

  (1) a #28 26 soran is lefutnak a gepi szabalyok (normalizal.py: `N t.`,
      tapadt konyvjelzes, Izrael, 1Pet, RV/AV-glossza) -- az `allapot` es a
      `modell` mezo nem valtozik; a javitasok a javitasi listan kulon
      jelolest kapnak (`igen (#28, DT-F38f 1)`);
  (2) a H5307, H5414, H7760 szocikkszintu `spirit` terminologia-kivetele
      megszunik (az 5. kapu a kis- es nagybetus alakot is elfogadja);
  (4) a maradek `N t.`: a tartomanyos alak (`5Móz 11:13-14t.`) a normalizalo
      uj szabalyaval (minden F38 soron);
  (5) a bizonytalan RV/AV-esetek (H4150, H2403, H3772, H4397, H5674, H8033):
      ami a forrasban RV/AV/RVm utan all, az angolul, szo szerint marad
      (`igen (kézi, DT-F38f 5)`).
A (3) Szellem-javitas (H1320) a naplok/BDB_FORDITAS_szellem.py-ban van.

Minden sor kapusorat a sor sajat terminologia-kiveteleivel futtatja elotte es
utana; ha egy F38-as sor az uj szovegen nem megy at a gatolo kapukon, megall.

    python naplok/BDB_FORDITAS_zaras2.py          # csak jelentes
    python naplok/BDB_FORDITAS_zaras2.py --ir
"""

import argparse
import collections
import difflib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'naplok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402
import normalizal as N  # noqa: E402
from BDB_FORDITAS_ujranormalizal import kivetelek  # noqa: E402

JEL = 'F38 BDB_FORDITAS'
KIMENET = os.path.join(REPO, 'naplok', 'BDB_FORDITAS_zaras_javitasok.tsv')
IRAS_28_REGI = 'nem (#28 sor)'
IRAS_28 = 'igen (#28, DT-F38f 1)'
IRAS_KEZI = 'igen (kézi, DT-F38f 5)'
JELOLES_F38 = 'F38.274: DT-F38f — tartományos „N t.”, kézi RV/AV-glossza'
JELOLES_28 = 'F38.274: DT-F38f (1) — gépi szabályok a #28 soron (N t., tapadt könyvjelzés, RV/AV, Izráel)'
JELOLES_SPIRIT = ('F38.274: a „spirit” szócikkszintű kivétele megszűnt (DT-F38f 2: az 5. kapu a '
                  'kis- és a nagybetűs alakot is elfogadja)')

# a szocikkszintu `spirit` kivetel (BDB_FORDITAS_szellem.py F38.268-as szovege)
SPIRIT_STRONG = {'H5307', 'H5414', 'H7760'}
SPIRIT_RESZ_KEZDET = 'a „spirit” kulcs szócikkszintű kivétele:'
SPIRIT_RESZ_VEGE = 'terminológia-kivétel (bizonytalan_feloldasok): spirit'

# (strong, regi_reszlet, uj_reszlet): DT-F38f (5) -- ami a forrasban RV/AV/RVm utan all,
# a forditasban is angolul, szo szerint marad
RV_KEZI = [
    ('H4150', 'RV rendszerint set feast vagy appointed season', 'RV usually set feast or appointed season'),
    ('H2403', 'RV fordítása sin-offering;', 'RV renders sin-offering;'),
    ('H3772', 'RV szerint fordítják: made for thee a covenant with them,',
     'RV made for thee a covenant with them,'),
    ('H4397', '(az RV angel szava túl szűk)', '(az angyal RV too specific)'),
    ('H5674', 'RVm, akik felemésztik, felfalják őket', 'RVm, those that shall consume, devour them'),
    ('H8033', 'RVm onnan [a mennyből], (onnan) a Pásztor (׳י), Izráel Köve (Sziklája),',
     'RVm from there [from heaven], (from) the Shepherd (׳י), the Stone (Rock) of Israel,'),
]


def valtozasok(regi, uj):
    a, b = regi.split(' '), uj.split(' ')
    ki = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != 'equal':
            ki.append((' '.join(a[i1:i2]), ' '.join(b[j1:j2])))
    return ki


def spirit_kivetel_torles(megj):
    """A F38.268-as `spirit`-kivetel szovegreszenek eltavolitasa a megjegyzesbol."""
    a = megj.find(SPIRIT_RESZ_KEZDET)
    if a < 0:
        return megj
    b = megj.index(SPIRIT_RESZ_VEGE, a) + len(SPIRIT_RESZ_VEGE)
    elo = megj[:a].rstrip('; ')
    utan = megj[b:].lstrip('; ')
    return '; '.join(x for x in (elo, utan, JELOLES_SPIRIT) if x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    args = ap.parse_args()
    with open(E.FORDITASOK_UT, encoding='utf-8', newline='') as fh:
        sorok = fh.read().split('\n')
    assert sorok[-1] == ''
    sorok = sorok[:-1]
    ix = {n: i for i, n in enumerate(E.FORDITASOK_FEJLEC)}
    uj_sorok = list(sorok)
    javitasok = []          # (strong, szabaly, regi, uj, iras)
    kapu_elotte, kapu_utana = {}, {}
    szamlalo = collections.Counter()
    kezi = collections.defaultdict(list)
    for s in RV_KEZI:
        kezi[s[0]].append(s)
    kezi_kesz = set()
    for i, s in enumerate(sorok):
        m = s.split('\t')
        if len(m) != 12 or m[0] != 'BDB' or m[3] != 'teljes':
            continue
        sp, forras = E.forras_szoveg(m[1])
        f38 = JEL in m[ix['megjegyzes']]
        szamlalo['F38' if f38 else '#28'] += 1
        kiv_regi = kivetelek(m[ix['megjegyzes']])
        hu = m[ix['forditas_hu']]
        kapu_elotte[sp] = K.kapuk_futtat('BDB', forras, hu, bizonytalan=kiv_regi)
        megj = m[ix['megjegyzes']]
        spirit_volt = sp in SPIRIT_STRONG and SPIRIT_RESZ_KEZDET in megj
        if spirit_volt:
            megj = spirit_kivetel_torles(megj)
            szamlalo['spirit-kivetel torolve'] += 1
        kiv = kivetelek(megj)
        szoveg = hu
        iras_gepi = 'igen' if f38 else IRAS_28
        for nev in N.SZABALY_SORREND:
            if 'BDB' not in N.SZABALYOK[nev]:
                continue
            uj, db = N.FUGGVENYEK[nev](szoveg)
            if db:
                for r, u in valtozasok(szoveg, uj):
                    javitasok.append((sp, nev, r, u, iras_gepi))
                szoveg = uj
        uj, glossza = N.glossza_visszaallit(forras, szoveg)
        for r, u in glossza:
            javitasok.append((sp, 'glossza_visszaallit', r, u, iras_gepi))
        szoveg = uj
        for strong, regi, ujr in kezi.get(sp, ()):
            db = szoveg.count(regi)
            if db != 1:
                raise SystemExit('%s: a kezi cserehez a regi reszlet %d-szer all (1 kell): %s' % (sp, db, regi))
            szoveg = szoveg.replace(regi, ujr)
            javitasok.append((sp, 'rv_av_kezi', regi, ujr, IRAS_KEZI))
            kezi_kesz.add(sp + regi)
        kapu_utana[sp] = K.kapuk_futtat('BDB', forras, szoveg, bizonytalan=kiv)
        if f38 and not K.atment(kapu_utana[sp]):
            raise SystemExit('%s: az uj szoveg nem megy at a gatolo kapukon -- megallok: %s' % (
                sp, [(n, e, r[:200]) for n, e, r in kapu_utana[sp] if e == 'SERTES']))
        if szoveg != hu or spirit_volt:
            if szoveg != hu:
                jel = JELOLES_F38 if f38 else JELOLES_28
                if jel not in megj:
                    megj = '; '.join(x for x in (megj, jel) if x)
                szamlalo['valtozott ' + ('F38' if f38 else '#28')] += 1
            m[ix['forditas_hu']] = szoveg
            m[ix['megjegyzes']] = megj
            uj_sorok[i] = '\t'.join(m)
    if len(kezi_kesz) != len(RV_KEZI):
        raise SystemExit('nem minden kezi csere futott le: %s' % (len(kezi_kesz),))
    # biztonsag: az allapot/modell/mas oszlopok nem valtoztak
    for a, b in zip(sorok, uj_sorok):
        if a == b:
            continue
        ma, mb = a.split('\t'), b.split('\t')
        for c in range(12):
            if c not in (ix['forditas_hu'], ix['megjegyzes']) and ma[c] != mb[c]:
                raise SystemExit('varatlan oszlopvaltozas: %s %s' % (ma[1], E.FORDITASOK_FEJLEC[c]))
    # jelentes
    print('szamlalo:', dict(szamlalo))
    print('javitasok (db) szabalyonkent es irassal:')
    for k, v in sorted(collections.Counter((j[1], j[4]) for j in javitasok).items()):
        print('  %-22s %-26s %d' % (k[0], k[1], v))
    print('erintett szocikk irassal:', {k: len({j[0] for j in javitasok if j[4] == k})
                                       for k in sorted({j[4] for j in javitasok})})
    for sp in sorted(kapu_elotte):
        for (n, e0, _), (_, e1, r1) in zip(kapu_elotte[sp], kapu_utana[sp]):
            if e0 != e1:
                print('kapu valtozas %s %s: %s -> %s %s' % (sp, n, e0, e1, r1[:100] if e1 == 'SERTES' else ''))
    marad = [(sp, n, r[:160]) for sp in sorted(kapu_utana) for n, e, r in kapu_utana[sp] if e == 'SERTES']
    print('gatolo SERTES az iras utan:', marad if marad else 'nincs')
    # TSV
    regi_tsv = []
    with open(KIMENET, encoding='utf-8', newline='') as fh:
        tsv_sorok = fh.read().split('\n')
    fej = tsv_sorok[0]
    assert fej == 'szocikk\tszabaly\tregi\tuj\tdb\tiras', fej
    for l in tsv_sorok[1:]:
        if l:
            regi_tsv.append(l.split('\t'))
    regi_28 = {(f[0], f[1], f[2], f[3]) for f in regi_tsv if f[5] == IRAS_28_REGI}
    uj_28 = {(sp, nev, r, u) for sp, nev, r, u, iras in javitasok if iras == IRAS_28}
    if regi_28 - uj_28:
        raise SystemExit('a regi #28 javitando sorok kozul nem futott le: %s' % sorted(regi_28 - uj_28)[:10])
    atirt = 0
    for f in regi_tsv:
        if f[5] == IRAS_28_REGI:
            f[5] = IRAS_28
            atirt += 1
    print('a regi `nem (#28 sor)` jeloles atirva: %d egyedi sor' % atirt)
    uj_csop = collections.Counter(j for j in javitasok if (j[0], j[1], j[2], j[3]) not in regi_28)
    uj_tsv = list(regi_tsv)
    for (sp, nev, r, u, iras), db in sorted(uj_csop.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        uj_tsv.append([sp, nev, r, u, str(db), iras])
    print('uj javitas-sor (egyedi): %d; a lista osszesen: %d' % (len(uj_csop), len(uj_tsv)))
    if args.ir:
        with open(E.FORDITASOK_UT, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(uj_sorok) + '\n')
        with open(KIMENET, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join([fej] + ['\t'.join(x) for x in uj_tsv]) + '\n')
        print('adat/forditasok.tsv es a javitasi lista irva')


if __name__ == '__main__':
    main()
