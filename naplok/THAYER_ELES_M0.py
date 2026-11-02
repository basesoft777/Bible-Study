#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F07 M0 (a) — a becslő újraillesztése a #27 M1 és a #159 mért adataiból (N68 lezárása).

    python naplok/THAYER_ELES_M0.py illeszt        # az együtthatók, a pontszám, a maradék hiba (kiírja; a naplóba másolandó)
    python naplok/THAYER_ELES_M0.py sorrend [ts]   # naplok/THAYER_ELES_sorrend.tsv + adagterv (becslés effortonként)

Bemenet (csak olvas): forditas/thayer_api/adag1 (F27 M1, egy Strongos út, effort=high), adag99 (aranyminta, high),
adag1591 (F159 B-út high) és adag1592 (medium): futasnaplo.tsv, kapu_eredmeny.jsonl, b_csoportok.json.
Modell: bemenet = A·állandó_karakter + B·forráskarakter (kérésenként; a szűkített / szűkítetlen állandó rész karakterből);
kimenet effortonként és kategóriánként külön (B-kérés: kimenet ≈ k·forráskarakter + c·Strong; egy Strongos: ≈ c0 + k·forráskarakter).
Javító kör: kategóriánként a mért javító/1. kör költségarány (bukási arány × javító kérés költsége együtt).
Minden szám `manual`-nak minősül a becslés szempontjából; a bemeneti adatok mért költségek (futasnaplo.tsv).
Proveniencia: scope=adag1,adag99,adag1591,adag1592 | forras=naplok/THAYER_ELES_M0.py illeszt | ts=2026-11-02
TSV: split('\\t'); csv modul nincs.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import thayer_api_koteg as T  # noqa: E402

MUNKA = os.path.join(ROOT, 'forditas', 'thayer_api')
AR_BE, AR_KI = T.AR_BE, T.AR_KI


def napló(adag):
    return T.AK.tsv_olvas(os.path.join(MUNKA, adag, 'futasnaplo.tsv'))


def kapu(adag):
    with open(os.path.join(MUNKA, adag, 'kapu_eredmeny.jsonl'), encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def lsq(sorok, y):
    """Legkisebb négyzetek, szabad tag nélkül: y = sum(b_j * x_j) -> (b, R², átlagos |relatív hiba|)."""
    n = len(sorok[0])
    A = [[sum(r[i] * r[j] for r in sorok) for j in range(n)] for i in range(n)]
    v = [sum(r[i] * yy for r, yy in zip(sorok, y)) for i in range(n)]
    for i in range(n):      # Gauss-elimináció
        p = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[p], v[i], v[p] = A[p], A[i], v[p], v[i]
        for k in range(i + 1, n):
            f = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= f * A[i][j]
            v[k] -= f * v[i]
    b = [0.0] * n
    for i in range(n - 1, -1, -1):
        b[i] = (v[i] - sum(A[i][j] * b[j] for j in range(i + 1, n))) / A[i][i]
    pred = [sum(bj * xj for bj, xj in zip(b, r)) for r in sorok]
    ym = sum(y) / len(y)
    ss_res = sum((a - p) ** 2 for a, p in zip(y, pred))
    ss_tot = sum((a - ym) ** 2 for a in y)
    return b, 1 - ss_res / ss_tot if ss_tot else 1.0, sum(abs(a - p) / a for a, p in zip(y, pred) if a) / len(y)


def egy_strongos_pontok(adag):
    """Az egy Strongos (A-stílusú) 1. körös kérések: (állandó_kar, forrás_kar, be_token, ki_token, kategória, költség, effort)."""
    pontok = []
    ker = {}
    for r in napló(adag):
        cid = r['custom_id']
        m = T.custom_id_bont(cid)
        if not m or m[2] != 1:
            continue
        sp, cs, _ = m
        if sp not in ker:
            ker[sp] = T.kerelmek_strongra(sp)
        k = ker[sp][cs - 1]
        kat = T.kategoria(T.konnyu_strongra(sp))
        pontok.append((T.allando_kar(k['prompt']), k['forras_kar'], int(r['bemenet_token']), int(r['kimenet_token']), kat,
                       float(r['koltseg_usd']), r['effort']))
    return pontok


def b_pontok(adag):
    """A B-kérések: (állandó_kar, forrás_kar, be_token, ki_token, Strong-szám, költség, effort)."""
    with open(os.path.join(MUNKA, adag, 'b_csoportok.json'), encoding='utf-8') as f:
        cs = json.load(f)
    pontok = []
    T.MUNKA = os.path.join(MUNKA, adag)
    for r in napló(adag):
        if not T.CID_B.match(r['custom_id']):
            continue
        nev = r['custom_id'][:4]
        ks = [T.kerelmek_strongra(s)[0] for s in cs[nev]]
        prompt = T.b_prompt(ks)
        pontok.append((T.allando_kar(prompt), sum(k['forras_kar'] for k in ks), int(r['bemenet_token']), int(r['kimenet_token']),
                       len(ks), float(r['koltseg_usd']), r['effort']))
    return pontok


def javito_koltseg(adag):
    """(javító kérések darabja, összköltség, B-stílusú vagy egy Strongos) az adag p2 soraiból, a Strong kategóriája szerint."""
    ki = {}
    for r in napló(adag):
        m = T.custom_id_bont(r['custom_id'])
        if not m or m[2] != 2:
            continue
        kat = T.kategoria(T.konnyu_strongra(m[0]))
        d, u = ki.get(kat, (0, 0.0))
        ki[kat] = (d + 1, u + float(r['koltseg_usd']))
    return ki


def koltseg_1_kor(adag):
    ki = {}
    for r in napló(adag):
        cid = r['custom_id']
        m = T.custom_id_bont(cid)
        if m and m[2] == 2:
            continue
        if T.CID_B.match(cid):
            kat = 'B'
        elif m:
            kat = T.kategoria(T.konnyu_strongra(m[0]))
        else:
            continue
        d, u = ki.get(kat, (0, 0.0))
        ki[kat] = (d + 1, u + float(r['koltseg_usd']))
    return ki


def koltseg(be, ki):
    return (be * AR_BE + ki * AR_KI) / 1e6


def illeszt():
    A = egy_strongos_pontok('adag1') + egy_strongos_pontok('adag99')
    B_h, B_m = b_pontok('adag1591'), b_pontok('adag1592')
    eredm = {}
    print('# Egy Strongos (A) kérések, effort=high, szűkítetlen állandó rész (n=%d)' % len(A))
    be, r2, hiba = lsq([(1.0, p[1]) for p in A], [p[2] for p in A])
    ki, r2k, hibak = lsq([(1.0, p[1]) for p in A], [p[3] for p in A])
    print('  bemenet: %.0f + %.4f·kar; R²=%.4f; átl. |hiba|=%.1f%%' % (be[0], be[1], r2, hiba * 100))
    print('  kimenet: %.0f + %.4f·kar; R²=%.4f; átl. |hiba|=%.1f%%' % (ki[0], ki[1], r2k, hibak * 100))
    eredm['A'] = (be, ki)
    print('# B-kérések (szűkített állandó rész; n=4 effortonként, a bemenet azonos)')
    bb, r2, hiba = lsq([(p[0], p[1]) for p in B_h], [p[2] for p in B_h])
    print('  bemenet: %.4f·állandó_kar + %.4f·kar; R²=%.4f; átl. |hiba|=%.1f%% (4 pont, 2 paraméter: tájékoztató)' % (bb[0], bb[1], r2, hiba * 100))
    eredm['B_be'] = bb
    for effort, ps in (('high', B_h), ('medium', B_m)):
        k, r2, hiba = lsq([(p[1],) for p in ps], [p[3] for p in ps])
        k2, r22, hiba2 = lsq([(p[1], p[4]) for p in ps], [p[3] for p in ps])
        print('  kimenet %s: %.4f·kar (R²=%.4f, átl. |hiba|=%.1f%%); kar+Strong: %.4f·kar + %.0f·Strong (átl. |hiba|=%.1f%%)' % (
            effort, k[0], r2, hiba * 100, k2[0], k2[1], hiba2 * 100))
        eredm['B_ki_' + effort] = k[0]
    print('# Pontszám: becsült / mért költség a mérő adagokra (a fenti együtthatókkal)')
    for nev, ps, f in (('A (adag1+adag99, high)', A, lambda p: koltseg(be[0] + be[1] * p[1], ki[0] + ki[1] * p[1])),
                       ('B high', B_h, lambda p: koltseg(bb[0] * p[0] + bb[1] * p[1], eredm['B_ki_high'] * p[1])),
                       ('B medium', B_m, lambda p: koltseg(bb[0] * p[0] + bb[1] * p[1], eredm['B_ki_medium'] * p[1]))):
        becs, mert = sum(f(p) for p in ps), sum(p[5] for p in ps)
        print('  %s: becsült %.4f USD, mért %.4f USD, eltérés %+.1f%%' % (nev, becs, mert, 100 * (becs - mert) / mert))
    print('# Javító kör / 1. kör költségarány kategóriánként (mért)')
    for adag in ('adag1', 'adag99', 'adag1591', 'adag1592'):
        p1, p2 = koltseg_1_kor(adag), javito_koltseg(adag)
        print('  %s: 1. kör %s; javító %s' % (adag, {k: (d, round(u, 4)) for k, (d, u) in p1.items()},
                                          {k: (d, round(u, 4)) for k, (d, u) in p2.items()}))
    return 0


ALLANDO_A_SZUKITETT = 27500      # az egy Strongos kérés szűkített állandó része karakterben (G25: 26 463, G1941: 29 398; manual)
ALLANDO_B = 21084                # a B-kérés szűkített állandó része karakterben (a 4 mérő kérés átlaga)
ADAG_KAR = 500000
ELSO_ADAG_ELEJEN = ['G0282']     # DT-F07a 3.: a kezi sor mellett újrafordul (beir --regi-elavult --kezi-marad)


def sorrend_epit(ts, kizar=()):
    """A `naplok/FP3_sorrend.tsv` sorrendje a még nem szakaszos Strongokkal (a `thayer_api_koteg.py lista` szerint), a G0282 elöl.
    -> [{sorszam, strong, gyakorisag, karakter, szakasz, kategoria, adag, kar_kerelmek}]"""
    lista = {r['strong']: r for r in T.teljes_lista(ts)}
    fp3 = []
    with open(os.path.join(ROOT, 'naplok', 'FP3_sorrend.tsv'), encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#') or sor.startswith('sorszam'):
                continue
            m = sor.rstrip('\n').split('\t')
            fp3.append(m)
    sorok = []
    for s in ELSO_ADAG_ELEJEN:
        sorok.append([s, '', str(lista[s]['karakter']), lista[s]['szakasz']])
    for m in fp3:
        if lista[m[1]]['statusz'] == 'forditando' and m[1] not in kizar:
            sorok.append([m[1], m[2], m[3], m[4]])
    ki, adag, kar = [], 1, 0
    for i, (sp, gy, k, sz) in enumerate(sorok):
        kk = T.konnyu_strongra(sp)
        if kar and kar + int(k) > ADAG_KAR:
            adag, kar = adag + 1, 0
        kar += int(k)
        ki.append({'sorszam': str(i + 1), 'strong': sp, 'gyakorisag': gy, 'karakter': k, 'szakasz': sz,
                   'kategoria': T.kategoria(kk), 'adag': str(adag), 'kerelmek': [x['forras_kar'] for x in kk]})
    return ki


def adag_becsles(sorok, effort):
    """Adagonként {adag: (Strong, karakter, B-kérés, nagy kérés, első kör, javító kör)} — kalibrált becslés (manual)."""
    ki = {}
    for a in sorted({int(r['adag']) for r in sorok}):
        rs = [r for r in sorok if int(r['adag']) == a]
        kicsik = [r for r in rs if r['kategoria'] != 'nagy']
        nagyok = [r for r in rs if r['kategoria'] == 'nagy']
        ix = {r['strong']: [{'forras_kar': r['kerelmek'][0]}] for r in kicsik}
        cs, _ = T.b_csoportok_epit([r['strong'] for r in kicsik], ix)
        b_usd = sum(T.becsles_adat(ALLANDO_B, sum(ix[s][0]['forras_kar'] for s in g), len(g), 'B', effort)[2] for g in cs.values())
        a_usd = sum(T.becsles_adat(ALLANDO_A_SZUKITETT, k, 1, 'A', effort)[2] for r in nagyok for k in r['kerelmek'])
        ki[a] = (len(rs), sum(int(r['karakter']) for r in rs), len(cs), sum(len(r['kerelmek']) for r in nagyok), b_usd + a_usd,
                 T.javito_kor_becsles(b_usd, 'B') + T.javito_kor_becsles(a_usd, 'A'))
    return ki


def sorrend(ts, kizar=()):
    sorok = sorrend_epit(ts, kizar)
    fej = ['sorszam', 'strong', 'gyakorisag', 'karakter', 'szakasz', 'kategoria', 'adag']
    ut = os.path.join(ROOT, 'naplok', 'THAYER_ELES_sorrend.tsv')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/THAYER_ELES_M0.py sorrend (F07 M0) — a naplok/FP3_sorrend.tsv sorrendje a még nem szakaszos Strongokkal '
                '(thayer_api_koteg.py lista), a G0282 elöl; adagok kb. %d forráskarakterrel | scope=teljes Thayer | '
                'forras=naplok/FP3_sorrend.tsv + thayer_api_koteg.py lista | ts=%s\n' % (ADAG_KAR, ts))
        f.write('\t'.join(fej) + '\n')
        for r in sorok:
            f.write('\t'.join(r[m] for m in fej) + '\n')
    print('irva: %s (%d Strong)' % (ut, len(sorok)))
    for effort in ('high', 'medium'):
        print('# adagterv, effort=%s (manual becslés; első kör + javító kör, plafon = 1,3 × becslés)' % effort)
        oss = 0.0
        for a, (n, kar, b, na, elso, jav) in adag_becsles(sorok, effort).items():
            oss += elso + jav
            print('  A%d: %d Strong, %d karakter, %d B-kérés, %d egyenkénti kérés; első kör %.2f + javító %.2f = %.2f USD; adagplafon %.2f' % (
                a, n, kar, b, na, elso, jav, elso + jav, 1.3 * (elso + jav)))
        print('  összesen %.2f USD (összplafon 120)' % oss)
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'illeszt':
        sys.exit(illeszt())
    if len(sys.argv) > 1 and sys.argv[1] == 'sorrend':
        sys.exit(sorrend(sys.argv[2] if len(sys.argv) > 2 else '2026-11-02'))
    print(__doc__)
