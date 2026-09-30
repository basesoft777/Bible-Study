#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.27 — P5 költségvetítés minden összeállításra a P3b-adatból (prompt_v2), API nélkül.

A koltseg_vetit.py módszere (P5 lépései), futásonként:
  * illesztés az első próbálkozású hívásokon: bemenet = a + b·x + c·k,
    kimenet = a + b·x (x = eredeti + Károli-szavak, k = KJV-támpont szavai; a
    döntőbírói F4V2-nél x a köteg verseinek összege, a hívás A- és B-válasza
    ezzel arányos, a tengelymetszet és a b együtthatója nyeli el);
  * ár: a modell táblaára (futtat.ARAK) × a futás mért cost/táblaár aránya (s)
    az első próbálkozásokon — az A-nál és a B-nél a cost nem egyenlő a
    táblaárral (gyorsítótár / kedvezmény), ezért a mért arány szorzóként megy
    át; az újrakérés a mért szorzóval (M = Σcost / Σcost első próba);
  * a teljes Biblia (31 158 vers) rétegenként, ceil(N/10) köteg. DT21 h)
    (F21.34): az irányadó besorolás az F22 brief 22.2 műfaji öt rétege
    (kv.F22_RETEG_KONYVEK; Préd, Sir → költészet, Dán → próféta, Ruth, Eszt →
    ÓSZ-próza a felhasználó döntése szerint); műfaji, nem kánon szerinti. A
    korábbi pilot-4-réteges besorolás tájékoztató sorokban (*_pilot4_tajekoztato)
    marad, a két változat különbségével. A pilot mérési rétegei nem változnak; a
    minta versei könyv szerint képeződnek le az F22-rétegekre (a döntőbírói
    arányhoz és a kézimunkához).
Összeállítások: A (F1V2), B (F2V2), C (F3V2), C (F3V2B), A+B = A + B,
A+B+C = A + B + (a döntőbíróhoz menő versek aránya a rétegben × C-döntőbíró),
ahol a döntőbírói arány és a döntőbírói hívás tokenigénye rétegenként a pilotból
(F4V2) jön.
Bootstrap: 1000 újramintavétel (mag 20260930); egysége a köteg (a token
versenként nem mérhető) — DT21 f): elfogadva (felhasználói döntés); a
döntőbírói arányt a versek újramintavételezése adja, a mintavétel strátumain
(R1–R4) belül; az F22-rétegenkénti arány ugyanebből a versmultihalmazból.
Ellenőrzés: a 200 versre (döntőbírónál a 193 versre) mintán belül és leave-one-out;
DT21 g): a kettő közül a konzervatívabb (nagyobb abszolút eltérésű) számít.
Kézimunka (A+B+C, G4): az `alacsony` linkek száma versenként (a 200 versen mért,
meres_p3b.osszeallitas_kimenet) és az aranyon mért eltérés/vers, rétegenként a
teljes Bibliára; a (c)-hiba/vers az A+B+C-re nincs besorolva: n.é.

Kimenet: f21p/koltseg_vetites_p3b.tsv (generált).
    python eszkozok/karoli_strong/koltseg_vetit_p3b.py [--onteszt]
"""

import math
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koltseg_vetit as kv  # noqa: E402
import tokenek  # noqa: E402

KIMENET = os.path.join(kv.F21P, 'koltseg_vetites_p3b.tsv')
MAG = 20260930
N_BOOT = 1000
RETEGEK = kv.RETEGEK
FUTAS_MODELL = {'F1V2': 'google/gemini-3.1-flash-lite', 'F2V2': 'deepseek/deepseek-v4-flash',
                'F3V2': 'google/gemini-3.8-flash', 'F3V2B': 'google/gemini-3.8-flash', 'F4V2': 'google/gemini-3.8-flash'}
ARAK = {'google/gemini-3.1-flash-lite': (0.25, 1.50), 'deepseek/deepseek-v4-flash': (0.14, 0.28),
        'google/gemini-3.8-flash': (0.75, 3.75)}   # = futtat.ARAK (a szkript ellenőrzi)


def illeszt(kk, ar):
    cin, cout, M = kv.illeszt(kk)
    tabla = sum((q['in'] * ar[0] + q['out'] * ar[1]) / 1e6 for q in kk)
    s = sum(q['cost1'] for q in kk) / tabla
    return cin, cout, M, s


def koltseg(param, ar, x, k, nkoteg):
    cin, cout, M, s = param
    be = nkoteg * cin[0] + cin[1] * x + cin[2] * k
    ki = nkoteg * cout[0] + cout[1] * x
    return (be * ar[0] + ki * ar[1]) / 1e6 * s * M


def vetit_futas(param, ar, bib, arany=None):
    """{reteg: cost}; arany: {reteg: p} a döntőbíró versaránya (None = minden vers). A rétegek a bib kulcsai."""
    ki = {}
    for r in bib:
        p = 1.0 if arany is None else arany[r]
        n = bib[r]['n'] * p
        ki[r] = koltseg(param, ar, bib[r]['x'] * p, bib[r]['k'] * p, math.ceil(n / kv.KOTEG) if n else 0)
    ki['Összes'] = sum(ki[r] for r in bib)
    return ki


def minta_versek(minta, rnd=None):
    """A minta versei; rnd-vel újramintavétel a mintavétel strátumain (a pilot R1–R4 rétegein) belül.

    A pilotminta R1–R4 szerint rétegzetten készült, ezért a bootstrap e strátumokon belül mintavételez;
    az F22-rétegenkénti arány ebből a versmultihalmazból, könyv szerinti leképezéssel származik.
    """
    ki = []
    for r in RETEGEK:
        vs = [m['igehely'] for m in minta if m['reteg'] == r]
        if rnd is not None:
            vs = [vs[rnd.randrange(len(vs))] for _ in vs]
        ki += vs
    return ki


def dontobiro_arany(versek, f4_versek, reteg_fn, retegek):
    """{reteg: a döntőbíróhoz menő versek aránya} a megadott rétegbesorolással."""
    ki = {}
    for r in retegek:
        vs = [ig for ig in versek if reteg_fn(ig) == r]
        ki[r] = sum(1 for ig in vs if ig in f4_versek) / len(vs)
    return ki


def main():
    import futtat
    for f, m in FUTAS_MODELL.items():
        assert futtat.ARAK[m] == ARAK[m], m
    vd = kv.Versadat()
    bib = kv.biblia(vd, kv.F22_RETEG_KONYVEK)   # irányadó: F22 műfaji öt réteg (DT21 h)
    bib4 = kv.biblia(vd)                        # tájékoztató: a korábbi pilot-4-réteges besorolás
    F22 = kv.F22_RETEGEK
    minta = kv._tsv(os.path.join(kv.F21P, 'minta.tsv'))
    pilot_reteg = {m['igehely']: m['reteg'] for m in minta}

    def p4_fn(ig):
        return pilot_reteg[ig]

    kk = {f: kv.kotegek(f, vd) for f in FUTAS_MODELL}
    import json
    f4_versek = set()
    with open(os.path.join(kv.F21P, 'valaszok', 'F4V2.jsonl'), encoding='utf-8') as fh:
        for s in fh:
            if s.strip():
                f4_versek.update(json.loads(s)['igehelyek'])
    param = {f: illeszt(kk[f], ARAK[FUTAS_MODELL[f]]) for f in kk}
    mv = minta_versek(minta)
    p_arany = dontobiro_arany(mv, f4_versek, kv.f22_reteg, F22)
    p_arany4 = dontobiro_arany(mv, f4_versek, p4_fn, RETEGEK)
    sorok = [['szakasz', 'osszeallitas', 'reteg', 'mero', 'ertek', 'also90', 'felso90', 'megjegyzes']]

    def add(*m):
        sorok.append([str(x) for x in m])

    for f in kk:
        cin, cout, M, s = param[f]
        add('illesztes', f, '-', 'bemenet_a_b_c', '%.2f / %.4f / %.4f' % tuple(cin), '', '', '%d első próbálkozású hívás' % len(kk[f]))
        add('illesztes', f, '-', 'kimenet_a_b', '%.2f / %.4f' % tuple(cout), '', '', '')
        add('ar', f, '-', 'cost1_per_tablaar_s', round(s, 6), '', '', 'táblaár %s: %.2f/%.2f USD/1M' % ((FUTAS_MODELL[f],) + ARAK[FUTAS_MODELL[f]]))
        add('ar', f, '-', 'ujrakeres_szorzo_M', round(M, 6), '', '', 'hívás/köteg = %.2f' % (sum(q['hivas'] for q in kk[f]) / len(kk[f])))
        pred = sum(koltseg(param[f], ARAK[FUTAS_MODELL[f]], q['x'], q['k'], 1) for q in kk[f])
        tenyl = sum(q['cost_ossz'] for q in kk[f])
        loo = 0.0
        for i in range(len(kk[f])):
            pi = illeszt(kk[f][:i] + kk[f][i + 1:], ARAK[FUTAS_MODELL[f]])
            loo += koltseg(pi, ARAK[FUTAS_MODELL[f]], kk[f][i]['x'], kk[f][i]['k'], 1)
        bent, loo_sz = 100 * (pred - tenyl) / tenyl, 100 * (loo - tenyl) / tenyl
        add('ellenorzes', f, '-', 'pilot_vetitett_usd', round(pred, 6), '', '', 'mintán belül')
        add('ellenorzes', f, '-', 'pilot_tenyleges_usd', round(tenyl, 6), '', '', 'futasnaplo.tsv')
        add('ellenorzes', f, '-', 'elteres_szazalek', round(bent, 3), '', '', 'mintán belül, küszöb ≤ 10%')
        add('ellenorzes', f, '-', 'loo_elteres_szazalek', round(loo_sz, 3), '', '', 'leave-one-out, küszöb ≤ 10%')
        sz, melyik = kv.szamito_ellenorzes(bent, loo_sz)
        add('ellenorzes', f, '-', 'szamito_elteres_szazalek', round(sz, 3), '', '',
            'DT21 g): a konzervatívabb (nagyobb abszolút eltérésű) számít: %s; küszöb ≤ 10%%: %s' % (
                melyik, 'teljesül' if abs(sz) <= 10 else 'nem teljesül'))
    for r in F22:
        n = [ig for ig in mv if kv.f22_reteg(ig) == r]
        add('dontobiro', 'F4V2', r, 'dontobirohoz_meno_versek_aranya', round(p_arany[r], 4), '', '',
            '%d/%d vers (a minta versei könyv szerint az F22-rétegre képezve)' % (sum(1 for ig in n if ig in f4_versek), len(n)))
    for r in RETEGEK:
        add('dontobiro_pilot4_tajekoztato', 'F4V2', r, 'dontobirohoz_meno_versek_aranya', round(p_arany4[r], 4), '', '',
            'TÁJÉKOZTATÓ: %d/%d vers (pilot-réteg)' % (sum(1 for m in minta if m['reteg'] == r and m['igehely'] in f4_versek),
                                                      sum(1 for m in minta if m['reteg'] == r)))

    def osszeallitasok(par, pa, b_):
        v = {f: vetit_futas(par[f], ARAK[FUTAS_MODELL[f]], b_) for f in ('F1V2', 'F2V2', 'F3V2', 'F3V2B')}
        d = vetit_futas(par['F4V2'], ARAK[FUTAS_MODELL['F4V2']], b_, pa)
        o = {'A (F1V2)': v['F1V2'], 'B (F2V2)': v['F2V2'], 'C (F3V2)': v['F3V2'], 'C (F3V2B)': v['F3V2B']}
        o['A+B'] = {r: v['F1V2'][r] + v['F2V2'][r] for r in list(b_) + ['Összes']}
        o['A+B+C'] = {r: o['A+B'][r] + d[r] for r in list(b_) + ['Összes']}
        o['C döntőbíró rész'] = d
        return o

    alap = osszeallitasok(param, p_arany, bib)
    alap4 = osszeallitasok(param, p_arany4, bib4)
    # ellenőrzés az A+B+C-re a pilot kötegein (mintán belül)
    pred = sum(koltseg(param[f], ARAK[FUTAS_MODELL[f]], q['x'], q['k'], 1) for f in ('F1V2', 'F2V2', 'F4V2') for q in kk[f])
    tenyl = sum(q['cost_ossz'] for f in ('F1V2', 'F2V2', 'F4V2') for q in kk[f])
    add('ellenorzes', 'A+B+C', '-', 'elteres_szazalek', round(100 * (pred - tenyl) / tenyl, 3), '', '',
        'F1V2+F2V2+F4V2 a pilot kötegein: %.6f vs %.6f USD (mintán belül; futásonként a leave-one-out is fent)' % (pred, tenyl))
    rnd = random.Random(MAG)
    boot = {o: {r: [] for r in F22 + ['Összes']} for o in alap}
    boot4 = {o: {r: [] for r in RETEGEK + ['Összes']} for o in alap4}
    for _ in range(N_BOOT):
        par = {}
        for f in kk:
            minta_k = [kk[f][rnd.randrange(len(kk[f]))] for _ in kk[f]]
            par[f] = illeszt(minta_k, ARAK[FUTAS_MODELL[f]])
        mvb = minta_versek(minta, rnd)
        b = osszeallitasok(par, dontobiro_arany(mvb, f4_versek, kv.f22_reteg, F22), bib)
        b4 = osszeallitasok(par, dontobiro_arany(mvb, f4_versek, p4_fn, RETEGEK), bib4)
        for o in b:
            for r in b[o]:
                boot[o][r].append(b[o][r])
            for r in b4[o]:
                boot4[o][r].append(b4[o][r])
    for o in alap:
        for r in F22 + ['Összes']:
            bs = sorted(boot[o][r])
            add('vetites', o, r, 'koltseg_usd', round(alap[o][r], 4), round(bs[int(0.05 * len(bs))], 4),
                round(bs[int(0.95 * len(bs)) - 1], 4), 'F22 műfaji réteg; bootstrap %d (köteg-egység: DT21 f, elfogadva — felhasználói döntés)' % len(bs))
    for o in alap4:
        for r in RETEGEK + ['Összes']:
            bs = sorted(boot4[o][r])
            add('vetites_pilot4_tajekoztato', o, r, 'koltseg_usd', round(alap4[o][r], 4), round(bs[int(0.05 * len(bs))], 4),
                round(bs[int(0.95 * len(bs)) - 1], 4), 'TÁJÉKOZTATÓ, korábbi pilot-4-réteges besorolás; bootstrap %d' % len(bs))
    for o in alap:
        d = alap[o]['Összes'] - alap4[o]['Összes']
        add('besorolas_kulonbseg_tajekoztato', o, 'Összes', 'f22_minus_pilot4_usd', round(d, 6), '', '',
            'TÁJÉKOZTATÓ: F22 műfaji 5 réteg − korábbi pilot-4 réteg (pont-becslés)')
        add('besorolas_kulonbseg_tajekoztato', o, 'Összes', 'f22_minus_pilot4_szazalek', round(100 * d / alap4[o]['Összes'], 4), '', '',
            'TÁJÉKOZTATÓ: a pilot-4-réteges érték százalékában')
    # kézimunka: A+B+C alacsony és eltérés — F22-rétegenként (a minta versei könyv szerint leképezve)
    import meres
    import meres_p3b
    adat = meres_p3b.betolt()
    kim = meres_p3b.osszeallitas_kimenet(adat)

    def kezi(oss, reteg_fn, retegek, b_):
        tot_a = tot_e = 0.0
        sor = []
        for r in retegek:
            vs = [ig for ig in adat.versek if reteg_fn(ig) == r]
            ala = sum(1 for ig in vs for s in kim[ig][oss].values() if s == 'alacsony')
            av = [ig for ig in vs if ig in adat.arany]
            elt = sum(len(set(kim[ig][oss]) ^ adat.arany_linkek(ig)) for ig in av)
            sor.append((r, ala, len(vs), elt, len(av)))
            tot_a += ala / len(vs) * b_[r]['n']
            tot_e += elt / len(av) * b_[r]['n']
        return sor, tot_a, tot_e

    for oss in ('A+B+C', 'A+B+C (alt)', 'A+B'):
        sor, tot_a, tot_e = kezi(oss, kv.f22_reteg, F22, bib)
        for r, ala, nv, elt, na in sor:
            add('kezimunka', oss, r, 'alacsony_link_per_vers', round(ala / nv, 4), '', '', 'mért, %d vers (könyv szerint F22-rétegre képezve)' % nv)
            add('kezimunka', oss, r, 'vetitett_alacsony_link_biblia', round(ala / nv * bib[r]['n']), '', '', '× %d vers' % bib[r]['n'])
            add('kezimunka', oss, r, 'elteres_per_vers_arany_v2', round(elt / na, 4), '', '', 'mért, %d aranyvers' % na)
            add('kezimunka', oss, r, 'vetitett_elteres_biblia', round(elt / na * bib[r]['n']), '', '', '× %d vers (kis n)' % bib[r]['n'])
        add('kezimunka', oss, 'Összes', 'vetitett_alacsony_link_biblia', round(tot_a), '', '', 'F22-rétegenként vetítve')
        add('kezimunka', oss, 'Összes', 'vetitett_elteres_biblia', round(tot_e), '', '', 'F22-rétegenként vetítve')
        add('kezimunka', oss, 'Összes', 'c_hiba_per_vers', 'n.é.', '', '', 'az A+B(+C) eltérései nincsenek (a)/(b)/(c)-re besorolva')
        _, t4a, t4e = kezi(oss, lambda ig: adat.reteg[ig], RETEGEK, bib4)
        add('kezimunka_pilot4_tajekoztato', oss, 'Összes', 'vetitett_alacsony_link_biblia', round(t4a), '', '',
            'TÁJÉKOZTATÓ: a korábbi pilot-4-réteges besorolással vetítve')
        add('kezimunka_pilot4_tajekoztato', oss, 'Összes', 'vetitett_elteres_biblia', round(t4e), '', '',
            'TÁJÉKOZTATÓ: a korábbi pilot-4-réteges besorolással vetítve')
    _ = meres
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/karoli_strong/koltseg_vetit_p3b.py | scope=P5 minden összeállításra (A, B, C, A+B, '
                 'A+B+C), P3b-adat (prompt_v2), teljes Biblia 31 158 vers, F22 műfaji öt réteg (DT21 h), mellette a korábbi '
                 'pilot-4-réteges besorolás tájékoztató sorai | forras=f21p/futasnaplo.tsv, '
                 'f21p/valaszok/{F1V2,F2V2,F3V2,F3V2B,F4V2}.jsonl, f21p/minta.tsv, konkordancia/Karoli_1908.tsv, '
                 'konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/KJV_Strongs_*.tsv, '
                 'f21p/arany_opus_v2.jsonl | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
                 'mag=%d | kézzel szerkeszteni tilos\n' % (tokenek.generalas_ts(), MAG))
        for s in sorok:
            assert all('\t' not in x for x in s)
            fh.write('\t'.join(s) + '\n')
    for s in sorok:
        if s[0] in ('vetites', 'vetites_pilot4_tajekoztato') and s[2] == 'Összes':
            print('%s %s: %s USD [%s–%s]' % (s[0], s[1], s[4], s[5], s[6]))
        if s[0] == 'ellenorzes' and 'elteres' in s[3]:
            print('  ellenőrzés %s %s: %s%%' % (s[1], s[3], s[4]))
    print('-> %s' % KIMENET)
    return 0


def onteszt():
    """Mock: két ismert költségű köteg; az illesztés és a vetítés visszaadja a várt értéket."""
    hibak = []
    kk = [{'x': 100, 'k': 0, 'in': 1000 + 10 * 100, 'out': 50 + 2 * 100, 'cost1': 0.001, 'cost_ossz': 0.0012},
          {'x': 200, 'k': 10, 'in': 1000 + 10 * 200 + 3 * 10, 'out': 50 + 2 * 200, 'cost1': 0.002, 'cost_ossz': 0.002},
          {'x': 300, 'k': 0, 'in': 1000 + 10 * 300, 'out': 50 + 2 * 300, 'cost1': 0.003, 'cost_ossz': 0.003}]
    ar = (1.0, 1.0)
    for q in kk:
        q['cost1'] = (q['in'] + q['out']) / 1e6 * 0.5   # s = 0.5
        q['cost_ossz'] = q['cost1'] * 1.1                # M = 1.1
    p = illeszt(kk, ar)
    if abs(p[0][0] - 1000) > 1e-6 or abs(p[0][1] - 10) > 1e-6 or abs(p[3] - 0.5) > 1e-9 or abs(p[2] - 1.1) > 1e-9:
        hibak.append('illesztés: %s' % (p,))
    c = koltseg(p, ar, 400, 0, 1)
    varhato = (1000 + 4000 + 50 + 800) / 1e6 * 0.5 * 1.1
    if abs(c - varhato) > 1e-12:
        hibak.append('költség: %s vs %s' % (c, varhato))
    if hibak:
        print('ÖNTESZT HIBA: %s' % hibak)
        return 1
    print('koltseg_vetit_p3b önteszt rendben (mock illesztés, s és M szorzó, vetítés)')
    return 0


if __name__ == '__main__':
    sys.exit(onteszt() if '--onteszt' in sys.argv else main())
