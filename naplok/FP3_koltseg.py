#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F27 M1 — költségmérés és kivetítés a teljes Thayerre (mért tokenek, nem a kötegelő becslése).
Modell: token = a·kérés + b·forráskarakter (bemenet és kimenet külön, legkisebb négyzetek az 1. körös kérésekre,
M1 + aranyminta). Ár: a kötegelő Batch-ára (AR_BE/AR_KI, USD / millió token). A javító kör a mért arányból."""
import collections
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(ITT)
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import thayer_api_koteg as TK  # noqa: E402

AR_BE, AR_KI = TK.AR_BE, TK.AR_KI


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n')]
    s = [x for x in s if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def sorok(adag):
    return tsv(os.path.join(GY, 'forditas', 'thayer_api', adag, 'futasnaplo.tsv'))


def lsq(xs, ys):
    """y = a·x1 + b·x2 (konstans nélkül) -> (a, b)."""
    s11 = sum(x[0] * x[0] for x in xs); s12 = sum(x[0] * x[1] for x in xs); s22 = sum(x[1] * x[1] for x in xs)
    t1 = sum(x[0] * y for x, y in zip(xs, ys)); t2 = sum(x[1] * y for x, y in zip(xs, ys))
    d = s11 * s22 - s12 * s12
    return (t1 * s22 - t2 * s12) / d, (t2 * s11 - t1 * s12) / d


def kat(k):
    return 'kicsi' if k < 500 else ('kozepes' if k < 3000 else 'nagy')


def main():
    kat_strong = {}
    for r in tsv(os.path.join(ITT, 'FP3_m1_strongok.tsv')):
        kat_strong[r['strong']] = r['kategoria']
    meres = []          # (adag, kor, strong, csoport, forras_kar, be, ki, usd)
    for adag, lista in (('adag1', 'FP3_m1_strongok.txt'), ('adag99', 'FP3_arany_strongok.txt')):
        strongok = [l.strip() for l in open(os.path.join(ITT, lista), encoding='utf-8') if l.strip()]
        kar = {(k['strong'], k['csoport']): k['forras_kar'] for s in strongok for k in TK.kerelmek_strongra(s)}
        for r in sorok(adag):
            m = TK.CID.match(r['custom_id'])
            if not m:
                continue
            sp, cs, pr = m.group('strong'), int(m.group('csoport')), int(m.group('proba'))
            meres.append((adag, pr, sp, cs, kar[(sp, cs)], int(r['bemenet_token']), int(r['kimenet_token']), float(r['koltseg_usd'])))
    k1 = [m for m in meres if m[1] == 1]
    k2 = [m for m in meres if m[1] == 2]
    def osszeg(ms, i): return sum(m[i] for m in ms)
    print('mért kérés: 1. kör %d, javító kör %d' % (len(k1), len(k2)))
    for nev, adagok in (('M1', ('adag1',)), ('aranyminta', ('adag99',)), ('együtt', ('adag1', 'adag99'))):
        a = [m for m in k1 if m[0] in adagok]; b = [m for m in k2 if m[0] in adagok]
        print('%s: 1. kör %d kérés, %d kar., be %d, ki %d token, %.4f USD; javító kör %d kérés, be %d, ki %d, %.4f USD; össz %.4f USD; javító/1. kör: kérés %.2f, USD %.2f' % (
            nev, len(a), osszeg(a, 4), osszeg(a, 5), osszeg(a, 6), osszeg(a, 7), len(b), osszeg(b, 5), osszeg(b, 6), osszeg(b, 7),
            osszeg(a, 7) + osszeg(b, 7), len(b) / len(a), osszeg(b, 7) / osszeg(a, 7)))
    xs = [(1.0, m[4]) for m in k1]
    a_be, b_be = lsq(xs, [m[5] for m in k1])
    a_ki, b_ki = lsq(xs, [m[6] for m in k1])
    print('illesztés (1. kör, %d kérés): bemenet = %.0f·kérés + %.3f·kar.; kimenet = %.0f·kérés + %.3f·kar.' % (len(k1), a_be, b_be, a_ki, b_ki))
    # kategóriánként (1. kör): token/karakter és USD/karakter
    kc = collections.defaultdict(lambda: [0, 0, 0, 0, 0.0])
    for m in k1:
        c = 'funkciószó' if kat_strong.get(m[2]) == 'funkciószó' else (kat_strong.get(m[2]) or ('arany:' + kat(m[4])))
        v = kc[c]; v[0] += 1; v[1] += m[4]; v[2] += m[5]; v[3] += m[6]; v[4] += m[7]
    print('kategória\tkérés\tkarakter\tbemenet\tkimenet\tUSD\tUSD/1000 kar.')
    for c, v in sorted(kc.items()):
        print('%s\t%d\t%d\t%d\t%d\t%.4f\t%.4f' % (c, v[0], v[1], v[2], v[3], v[4], 1000 * v[4] / v[1]))
    # kivetítés: a teljes lista valódi kérés- és karakterszámával, az illesztett modellel, kategóriánként
    teljes = [r for r in tsv(os.path.join(ITT, 'FP3_sorrend.tsv'))]
    ossz_ker = collections.Counter(); ossz_kar = collections.Counter()
    for r in teljes:
        k = int(r['karakter'])
        c = kat(k)
        ker = TK.kerelmek_strongra(r['strong']) if k >= 20000 else None
        ossz_ker[c] += len(ker) if ker else 1
        ossz_kar[c] += k
    print('teljes lista kategóriánként (kérés a csoportokból: ≥20 000 kar. Strongnál a valódi csoportszám, egyébként 1):')
    teljes_usd = 0.0
    for c in ('kicsi', 'kozepes', 'nagy'):
        be = a_be * ossz_ker[c] + b_be * ossz_kar[c]; ki = a_ki * ossz_ker[c] + b_ki * ossz_kar[c]
        usd = (be * AR_BE + ki * AR_KI) / 1e6
        teljes_usd += usd
        print('%s\tkérés %d\tkar. %d\tbe %.0f\tki %.0f\t%.2f USD' % (c, ossz_ker[c], ossz_kar[c], be, ki, usd))
    k2usd = osszeg(k2, 7) / osszeg(k1, 7)
    print('1. kör összesen: %.2f USD; javító kör (mért arány %.2f az 1. körhöz): +%.2f USD; mindkettő: %.2f USD' % (
        teljes_usd, k2usd, teljes_usd * k2usd, teljes_usd * (1 + k2usd)))


main()


def javit_kategoriankent():
    kat_strong = {r['strong']: r['kategoria'] for r in tsv(os.path.join(ITT, 'FP3_m1_strongok.tsv'))}
    cid = {}
    for adag in ('adag1',):
        for r in sorok(adag):
            m = TK.CID.match(r['custom_id'])
            if m:
                cid[(m.group('strong'), int(m.group('csoport')), int(m.group('proba')))] = float(r['koltseg_usd'])
    c = collections.defaultdict(lambda: [0, 0, 0.0, 0.0])
    for (sp, cs, pr), usd in cid.items():
        k = kat_strong[sp]
        if pr == 1:
            c[k][0] += 1; c[k][2] += usd
        else:
            c[k][1] += 1; c[k][3] += usd
    print('javító kör kategóriánként (M1): kategória, 1. kör kérés/USD, javító kérés/USD, USD-arány')
    for k, v in sorted(c.items()):
        print('%s\t%d\t%.4f\t%d\t%.4f\t%.2f' % (k, v[0], v[2], v[1], v[3], v[3] / v[2]))


javit_kategoriankent()
