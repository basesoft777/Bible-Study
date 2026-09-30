#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.17 — P5 költségvetítés a C modellre (F3: prompt v1, F3V2: prompt v2), API nélkül.

A pilot-brief P5 lépései:
  1. Hívásonként a mért token (futasnaplo.tsv) és a köteg vers-tulajdonságai:
     x = Σ (eredeti szavak + Károli-szavak), k = Σ KJV-támpont-szavak (a
     pilotban az R1-en van KJV-támpont, ez a bemenetet növeli, ezért külön
     regresszor).
  2. Lineáris illesztés tokenfajtánként, az első próbálkozású hívásokon (a köteg
     utasításrésze hívásonként egyszer, ez a tengelymetszet):
        bemenet = a + b·x + c·k ;  kimenet = a + b·x.
     Gondolkodási token: a futásnaplóban 0 mindkét futásnál, az F3V2 nyers
     usage-ában (completion_tokens_details.reasoning_tokens) is 0 — a kimeneti
     token tartalmazná, külön tag nincs.
  3. Alkalmazás a teljes Biblia valódi vershosszaira (31 158 Károli-vers;
     Karoli_1908.tsv + TAHOT_kivonat.tsv + TAGNT_kivonat.tsv), rétegenként
     (RETEG_KONYVEK), rétegenként ceil(N/10) köteggel.
  4. Ár: a cost mező. Az első próbálkozású hívásoknál a cost a táblaárral
     lineáris (az F3V2 nyers usage cost_details-e szerint pontosan bemenet·0,75 +
     kimenet·3,75 USD/1M); a szkript ezt ellenőrzi (cost / táblaár-arány). Az
     újrakérések cost-ja NEM lineáris a tokenben (a megismételt előtag
     gyorsítótárazott), ezért az újrakérést nem tokenből, hanem a pilot mért
     arányából vetítjük: M = Σ cost (minden hívás) / Σ cost (első próbálkozás),
     futásonként (a hívás/köteg arány mellett közölve).
  5. (Csak C, egymodelles; A+B+C nem futott, PD8.)
  6. Bizonytalanság: bootstrap (1000 újramintavétel, mag 20260930) a pilot
     kötegei felett (a vers-szintű tokenszám nem mérhető: a token hívásonként,
     10 versre ismert; a köteg a legkisebb mért egység) — minden
     újramintavételnél új illesztés és új M; 90%-os percentilis-intervallum.
  7. Ellenőrzés: a módszerrel a 200 pilot-versre vetített költség vs. a pilot
     tényleges költsége (≤ 10%).
Kézimunka-vetítés: a pilot aranyán (60 vers) mért eltérés/vers (hiányzó +
többlet link, az arany v2-höz), és a (c)-hiba/vers arány — ez utóbbi az Opus
besorolása, nem mérés — rétegenként a teljes Bibliára. `alacsony` arány:
egymodelles összeállításra n.é. (PD6). Minősítés nincs.

Kimenet: f21p/koltseg_vetites.tsv (generált). Futtatás:
    python eszkozok/karoli_strong/koltseg_vetit.py
"""

import json
import math
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

F21P = os.path.join(tokenek.ROOT, 'f21p')
KIMENET = os.path.join(F21P, 'koltseg_vetites.tsv')
MAG = 20260930
N_BOOT = 1000
KOTEG = 10
FUTASOK = ['F3', 'F3V2']
AR = (0.75, 3.75)  # USD / 1M token, google/gemini-3.8-flash (futtat.ARAK); a cost-ellenőrzés ezt igazolja

# Rétegbesorolás a minta szerkezete szerint (a szabály: műfaj és kánonrész):
#   R1 próza + bölcsesség: a Törvény és a történeti könyvek (1Móz–Eszt), Péld, Préd
#      (a mintában 1Móz, 2Móz, Péld);
#   R2 költészet: Jób, Zsolt, Én (a mintában Jób, Zsolt);
#   R3 próféták: Ézs–Mal a Siralmakkal és Dániellel (a mintában Ézs, Jer, Ez);
#   R4 ÚSZ: mind a 27 könyv (a mintában evangéliumok és levelek; ApCsel és Jel is ide).
RETEG_KONYVEK = {
    'R1': ['1Móz', '2Móz', '3Móz', '4Móz', '5Móz', 'Józs', 'Bír', 'Ruth', '1Sám', '2Sám', '1Kir', '2Kir',
           '1Krón', '2Krón', 'Ezsd', 'Neh', 'Eszt', 'Péld', 'Préd'],
    'R2': ['Jób', 'Zsolt', 'Én'],
    'R3': ['Ézs', 'Jer', 'Sir', 'Ez', 'Dán', 'Hós', 'Jóel', 'Ámós', 'Abd', 'Jón', 'Mik', 'Náh', 'Hab', 'Sof',
           'Hag', 'Zak', 'Mal'],
    'R4': ['Mt', 'Mk', 'Luk', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef', 'Fil', 'Kol', '1Thessz',
           '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak', '1Pét', '2Pét', '1Ján', '2Ján', '3Ján',
           'Júd', 'Jel'],
}
RETEGEK = ['R1', 'R2', 'R3', 'R4']


def _tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def konyv_reteg():
    d = {}
    for r, ks in RETEG_KONYVEK.items():
        for k in ks:
            d[k] = r
    return d


class Versadat:
    def __init__(self):
        self.karoli = tokenek.betolt_karoli()
        self.ered = tokenek.betolt_eredeti()
        self._kjv = {}

    def x(self, ig):
        return len(tokenek.tokenizal(self.karoli.get(ig, ''))) + len(self.ered.get(ig, []))

    def k(self, ig):
        if ig not in self._kjv:
            t = tokenek.kjv_tamapont(ig)
            self._kjv[ig] = len(t.split()) if t else 0
        return self._kjv[ig]


def kotegek(f, vd):
    """[{'x','k','in','out','cost1','cost_ossz','hivas'}] a futás kötegeire."""
    naplo = [r for r in _tsv(os.path.join(F21P, 'futasnaplo.tsv')) if r['futas'] == f]
    ki = []
    with open(os.path.join(F21P, 'valaszok', '%s.jsonl' % f), encoding='utf-8') as fh:
        for s in fh:
            if not s.strip():
                continue
            sor = json.loads(s)
            n = [r for r in naplo if int(r['koteg']) == sor['koteg']]
            p1 = [r for r in n if r['probalkozas'] == '1']
            assert len(p1) == 1, (f, sor['koteg'])
            ki.append({'x': sum(vd.x(ig) for ig in sor['igehelyek']),
                       'k': sum(vd.k(ig) for ig in sor['igehelyek']),
                       'in': int(p1[0]['bemenet_token']), 'out': int(p1[0]['kimenet_token']),
                       'gond': sum(int(r['gondolkodas_token']) for r in n),
                       'cost1': float(p1[0]['koltseg_usd']),
                       'cost_ossz': sum(float(r['koltseg_usd']) for r in n), 'hivas': len(n),
                       'usage_gond': (sum((h.get('usage') or {}).get('completion_tokens_details', {}).get('reasoning_tokens', 0) or 0
                                          for h in sor['hivasok']) if 'hivasok' in sor else None)})
    return ki


def ols(X, y):
    """Legkisebb négyzetek normálegyenlettel (kis méret, Gauss-elimináció)."""
    n = len(X[0])
    A = [[sum(r[i] * r[j] for r in X) for j in range(n)] for i in range(n)]
    b = [sum(r[i] * yy for r, yy in zip(X, y)) for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        b[c], b[p] = b[p], b[c]
        for r in range(n):
            if r != c and A[c][c]:
                m = A[r][c] / A[c][c]
                A[r] = [a - m * cc for a, cc in zip(A[r], A[c])]
                b[r] -= m * b[c]
    return [b[i] / A[i][i] for i in range(n)]


def illeszt(kk):
    """(in_coef [a,b,c], out_coef [a,b], M)"""
    cin = ols([[1.0, q['x'], q['k']] for q in kk], [q['in'] for q in kk])
    cout = ols([[1.0, q['x']] for q in kk], [q['out'] for q in kk])
    M = sum(q['cost_ossz'] for q in kk) / sum(q['cost1'] for q in kk)
    return cin, cout, M


def koltseg_koteg(cin, cout, x, k, nkoteg=1):
    be = nkoteg * cin[0] + cin[1] * x + cin[2] * k
    ki = nkoteg * cout[0] + cout[1] * x
    return be, ki, (be * AR[0] + ki * AR[1]) / 1e6


def biblia(vd):
    kr = konyv_reteg()
    d = {r: {'n': 0, 'x': 0, 'k': 0, 'eredeti_nelkul': 0} for r in RETEGEK}
    for ig in vd.karoli:
        r = kr[tokenek.konyv_rovid(ig)]
        d[r]['n'] += 1
        d[r]['x'] += vd.x(ig)
        d[r]['k'] += vd.k(ig)
        d[r]['eredeti_nelkul'] += ig not in vd.ered
    return d


def vetit(cin, cout, M, bib):
    ki = {}
    for r in RETEGEK:
        nk = math.ceil(bib[r]['n'] / KOTEG)
        be, kim, c = koltseg_koteg(cin, cout, bib[r]['x'], bib[r]['k'], nk)
        ki[r] = {'kotegek': nk, 'bemenet': be, 'kimenet': kim, 'cost1': c, 'cost': c * M}
    ki['Összes'] = {kk: sum(ki[r][kk] for r in RETEGEK) for kk in ('kotegek', 'bemenet', 'kimenet', 'cost1', 'cost')}
    return ki


def kezimunka():
    """{(futas, reteg): (eltérés, (c), versek)} az aranyon (60 vers, arany v2)."""
    import c_diff
    import c_diff_f3v2 as cf
    import meres_v2
    adat, g = meres_v2.betolt()
    f3b = cf.f3_besorolas()
    kezi = {}
    for r in c_diff._tsv(cf.OSSZEVETES_UT, cf.OSZLOPOK):
        kezi[((r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz'])), r['statusz'])] = r
    ki = {}
    for f in FUTASOK:
        el = cf.elteresek(adat, f, g['v2'])
        for ret in RETEGEK + ['Összes']:
            vs = [ig for ig in adat.versek if ig in adat.arany and adat.ok(f, ig) and (ret == 'Összes' or adat.reteg[ig] == ret)]
            e = [kk for kk, r in el.items() if ret == 'Összes' or r == ret]
            if f == 'F3':
                c = sum(1 for kk in e if f3b[kk]['osztaly'] == 'c')
            else:
                c = sum(1 for kk in e for st in ('maradt', 'uj', 'oroklott')
                        if (kk, st) in kezi and kezi[(kk, st)]['f3v2_osztaly'] == 'c')
            ki[(f, ret)] = (len(e), c, len(vs))
    return ki


def main():
    vd = Versadat()
    bib = biblia(vd)
    rnd = random.Random(MAG)
    sorok = [['szakasz', 'futas', 'reteg', 'mero', 'ertek', 'also90', 'felso90', 'megjegyzes']]

    def add(*m):
        sorok.append([str(x) for x in m])

    for r in RETEGEK:
        add('reteg_besorolas', '-', r, 'konyvek', ' '.join(RETEG_KONYVEK[r]), '', '',
            'műfaj és kánonrész szerint, a minta rétegeivel összhangban')
        add('biblia', '-', r, 'versek', bib[r]['n'], '', '', 'Károli-versek')
        add('biblia', '-', r, 'x_osszeg', bib[r]['x'], '', '', 'Σ(eredeti szavak + Károli-szavak)')
        add('biblia', '-', r, 'kjv_szavak', bib[r]['k'], '', '', 'KJV-támpont szavai (csak 1Móz/2Móz/Péld, 1:1 versmegfeleltetéssel)')
        add('biblia', '-', r, 'eredeti_nelkuli_versek', bib[r]['eredeti_nelkul'], '', '', 'x csak a Károli-szavakból (a 61 maradék)')
    add('biblia', '-', 'Összes', 'versek', sum(bib[r]['n'] for r in RETEGEK), '', '', '')
    print('Biblia: %d vers' % sum(bib[r]['n'] for r in RETEGEK))
    for f in FUTASOK:
        kk = kotegek(f, vd)
        cin, cout, M = illeszt(kk)
        tabla = sum((q['in'] * AR[0] + q['out'] * AR[1]) / 1e6 for q in kk)
        c1 = sum(q['cost1'] for q in kk)
        add('illesztes', f, '-', 'bemenet_a_b_c', '%.2f / %.4f / %.4f' % tuple(cin), '', '',
            'bemenet = a + b·x + c·k, %d első próbálkozású hívás' % len(kk))
        add('illesztes', f, '-', 'kimenet_a_b', '%.2f / %.4f' % tuple(cout), '', '', 'kimenet = a + b·x')
        add('illesztes', f, '-', 'gondolkodasi_token', sum(q['gond'] for q in kk),
            '', '', 'napló; nyers usage: %s' % ('n.é. (nem tárolt)' if kk[0]['usage_gond'] is None
                                                  else sum(q['usage_gond'] for q in kk)))
        add('ar', f, '-', 'cost1_per_tablaar', round(c1 / tabla, 6), '', '',
            'első próbálkozás: Σcost / Σ(bemenet·0,75 + kimenet·3,75)/1e6')
        add('ar', f, '-', 'ujrakeres_szorzo_M', round(M, 6), '', '',
            'Σcost(minden hívás)/Σcost(első próbálkozás); hívás/köteg = %.2f' % (sum(q['hivas'] for q in kk) / len(kk)))
        # ellenőrzés: a módszer a 200 pilot-versre
        pred = sum(koltseg_koteg(cin, cout, q['x'], q['k'])[2] for q in kk) * M
        tenyl = sum(q['cost_ossz'] for q in kk)
        add('ellenorzes', f, '-', 'pilot_200_vetitett_usd', round(pred, 6), '', '', 'a módszerrel, a pilot kötegeire')
        add('ellenorzes', f, '-', 'pilot_200_tenyleges_usd', round(tenyl, 6), '', '', 'futasnaplo.tsv')
        add('ellenorzes', f, '-', 'elteres_szazalek', round(100 * (pred - tenyl) / tenyl, 3), '', '',
            'küszöb a brief szerint: ≤ 10%; mintán belüli (az illesztés ugyanezeken a hívásokon), ezért közel 0')
        # mintán kívüli ellenőrzés: leave-one-out a kötegek felett
        loo = 0.0
        for i in range(len(kk)):
            tobbi = kk[:i] + kk[i + 1:]
            ci, co, Mi = illeszt(tobbi)
            loo += koltseg_koteg(ci, co, kk[i]['x'], kk[i]['k'])[2] * Mi
        add('ellenorzes', f, '-', 'pilot_200_loo_vetitett_usd', round(loo, 6), '', '',
            'leave-one-out: minden köteg a többi 19-ből illesztve és vetítve')
        add('ellenorzes', f, '-', 'loo_elteres_szazalek', round(100 * (loo - tenyl) / tenyl, 3), '', '',
            'mintán kívüli eltérés a pilot tényleges költségétől (küszöb: ≤ 10%)')
        v = vetit(cin, cout, M, bib)
        # bootstrap a kötegek felett
        boot = {r: [] for r in RETEGEK + ['Összes']}
        for _ in range(N_BOOT):
            minta = [kk[rnd.randrange(len(kk))] for _ in kk]
            try:
                b = vetit(*illeszt(minta), bib)
            except ZeroDivisionError:
                continue
            for r in boot:
                boot[r].append(b[r]['cost'])
        for r in RETEGEK + ['Összes']:
            bs = sorted(boot[r])
            lo, hi = bs[int(0.05 * len(bs))], bs[int(0.95 * len(bs)) - 1]
            add('vetites', f, r, 'koltseg_usd', round(v[r]['cost'], 4), round(lo, 4), round(hi, 4),
                'kötegek: %d; bemenet %.0f, kimenet %.0f token (első próba); ×M; bootstrap %d' % (
                    v[r]['kotegek'], v[r]['bemenet'], v[r]['kimenet'], len(bs)))
        print('%s: teljes Biblia %.4f USD [%.4f–%.4f]; ellenőrzés 200 versen: %.6f vs %.6f (%.3f%%)' % (
            f, v['Összes']['cost'], sorted(boot['Összes'])[int(0.05 * len(boot['Összes']))],
            sorted(boot['Összes'])[int(0.95 * len(boot['Összes'])) - 1], pred, tenyl, 100 * (pred - tenyl) / tenyl))
    km = kezimunka()
    for f in FUTASOK:
        for r in RETEGEK + ['Összes']:
            e, c, n = km[(f, r)]
            nb = sum(bib[x]['n'] for x in RETEGEK) if r == 'Összes' else bib[r]['n']
            add('kezimunka', f, r, 'elteres_per_vers_arany_v2', round(e / n, 4) if n else '', '', '',
                'mért: hiányzó+többlet link az arany v2-höz, %d/%d aranyvers' % (e, n))
            add('kezimunka', f, r, 'c_hiba_per_vers', round(c / n, 4) if n else '', '', '',
                'az Opus besorolása, nem mérés: %d (c) / %d aranyvers' % (c, n))
            if r != 'Összes' and n:
                add('kezimunka', f, r, 'vetitett_elteres_biblia', round(e / n * nb), '', '', 'eltérés/vers × %d vers (kis n: %d aranyvers)' % (nb, n))
                add('kezimunka', f, r, 'vetitett_c_hiba_biblia', round(c / n * nb), '', '', 'Opus-besorolás, nem mérés; × %d vers' % nb)
        tot_e = sum(km[(f, r)][0] / km[(f, r)][2] * bib[r]['n'] for r in RETEGEK)
        tot_c = sum(km[(f, r)][1] / km[(f, r)][2] * bib[r]['n'] for r in RETEGEK)
        add('kezimunka', f, 'Összes', 'vetitett_elteres_biblia', round(tot_e), '', '', 'rétegenként vetítve, összegezve')
        add('kezimunka', f, 'Összes', 'vetitett_c_hiba_biblia', round(tot_c), '', '', 'Opus-besorolás, nem mérés; rétegenként vetítve')
        add('kezimunka', f, 'Összes', 'alacsony_arany', 'n.é.', '', '', 'egymodelles összeállításra nem értelmezett (PD6, G4)')
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/karoli_strong/koltseg_vetit.py | scope=C (F3, F3V2), P5 teljes Biblia '
                 '(31 158 vers) | forras=f21p/futasnaplo.tsv, f21p/valaszok/F3.jsonl, f21p/valaszok/F3V2.jsonl, '
                 'konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, '
                 'konkordancia/KJV_Strongs_*.tsv, f21p/c_diff_besorolas.tsv, f21p/c_diff_f3v2_osszevetes.tsv | '
                 'ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | mag=%d | kézzel szerkeszteni tilos\n' % (tokenek.generalas_ts(), MAG))
        for s in sorok:
            assert all('\t' not in x for x in s)
            fh.write('\t'.join(s) + '\n')
    print('-> %s' % KIMENET)


if __name__ == '__main__':
    main()
