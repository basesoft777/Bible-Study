#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.42 — P5 költségvetítés a regressziós mérésre (P3c, PD13): a Sonnet egyedül és a
Sonnet + C pár költsége a teljes Bibliára, API nélkül.

A koltseg_vetit.py / koltseg_vetit_p3b.py módszere (P5 lépései), futásonként (SONNETV3, F3V3):
  * illesztés az első próbálkozású hívásokon: bemenet = a + b·x + c·k, kimenet = a + b·x
    (x = eredeti + Károli-szavak, k = KJV-támpont szavai a köteg verseire);
  * ár: a modell táblaára (futtat.ARAK) × a futás mért cost/táblaár aránya (s) az első
    próbálkozásokon; az újrakérés-szorzó a futás SAJÁT mért adatából: M = Σcost / Σcost(első
    próba) (a Sonnetnél a Sonnet-futásból, a C-nél az F3V3-ból);
  * a teljes Biblia (31 158 vers) rétegenként, ceil(N/10) köteg; a rétegbesorolás az F22 brief
    22.2 műfaji öt rétege (kv.F22_RETEG_KONYVEK: Préd, Sir → költészet, Dán → próféta,
    Ruth, Eszt → ÓSZ-próza; PD12); a pilot mérési rétegei nem változnak;
  * összeállítások: Sonnet (SONNETV3), C (F3V3), Sonnet+C = a két futás vetített költségének
    összege (mindkettő a saját mért költségéből; döntőbíró NINCS, tehát nincs döntőbírói arány);
  * bizonytalanság: bootstrap 1 000 újramintavétel (mag 20260930), egysége a KÖTEG (a token
    versenként nem mérhető; PD12: elfogadva); minden újramintavételnél új illesztés és új M,
    a két futás kötegei egymástól függetlenül; 90%-os percentilis-intervallum;
  * ellenőrzés a 200 versre: mintán belül és leave-one-out, futásonként és a párra (a két
    futás kötegeinek összege); a konzervatívabb (nagyobb abszolút eltérésű) számít (PD12, DT21 g);
    küszöb ≤ 10%.
Kézimunka (a Sonnet+C pár, G4): az `alacsony` linkek száma versenként (a 200 versen mért
meres_p3c.par_kimenet) és az aranyon mért eltérés/vers, rétegenként a teljes Bibliára; a
mérés az arany legfrissebb befagyasztott változatára megy (meres_p3c.betolt).

Kimenet: f21p/koltseg_vetites_p3c.tsv (generált; proveniencia-fejléc: scope | forras | ts).
A régi koltseg_vetites*.tsv fájlok nem változnak.
    python eszkozok/karoli_strong/koltseg_vetit_p3c.py [--arany <jsonl> [--arany-sha <fájl>]]
                                                       [--forras-dir <könyvtár>] [--onteszt]
"""

import argparse
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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import koltseg_vetit as kv  # noqa: E402
import koltseg_vetit_p3b as kp  # noqa: E402
import meres_p3c as mp  # noqa: E402
import tokenek  # noqa: E402

KIMENET = os.path.join(kv.F21P, 'koltseg_vetites_p3c.tsv')
MAG = 20260930
N_BOOT = 1000
SONNET, C3 = mp.SONNET, mp.C3
FUTAS_MODELL = {SONNET: 'anthropic/claude-sonnet-5.5', C3: 'google/gemini-3.8-flash'}
OSS_S, OSS_C, OSS_PAR = mp.NEVEK[SONNET], mp.NEVEK[C3], mp.PAR


def kotegek_p3c(f, vd, forras_dir):
    """[{'x','k','in','out','cost1','cost_ossz','hivas','gond'}] a futás kötegeire (a kv.kotegek,
    a forrás-könyvtár paraméterével)."""
    naplo = [r for r in kv._tsv(os.path.join(forras_dir, 'futasnaplo.tsv')) if r['futas'] == f]
    ki = []
    with open(os.path.join(forras_dir, 'valaszok', '%s.jsonl' % f), encoding='utf-8') as fh:
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
                       'cost_ossz': sum(float(r['koltseg_usd']) for r in n), 'hivas': len(n)})
    return ki


def osszeallitasok(par, ar, bib):
    """{összeállítás: {réteg: cost}} a futásonkénti paraméterekből (par: {futás: illesztés})."""
    v = {f: kp.vetit_futas(par[f], ar[f], bib) for f in (SONNET, C3)}
    o = {OSS_S: v[SONNET], OSS_C: v[C3]}
    o[OSS_PAR] = {r: v[SONNET][r] + v[C3][r] for r in list(bib) + ['Összes']}
    return o


def _ellenorzes(kk_lista, ar_lista):
    """(mintán belüli, leave-one-out) vetített költség a kötegeken; a lista elemei egy-egy futás
    kötegei (+ ára): a pár esetén a két futás összege."""
    pred = loo = tenyl = 0.0
    for kk, ar in zip(kk_lista, ar_lista):
        p = kp.illeszt(kk, ar)
        pred += sum(kp.koltseg(p, ar, q['x'], q['k'], 1) for q in kk)
        tenyl += sum(q['cost_ossz'] for q in kk)
        for i in range(len(kk)):
            pi = kp.illeszt(kk[:i] + kk[i + 1:], ar)
            loo += kp.koltseg(pi, ar, kk[i]['x'], kk[i]['k'], 1)
    return pred, loo, tenyl


def szamol(forras_dir=None, arany_ut=None, arany_sha=None, n_boot=N_BOOT, vd=None, bib=None):
    """A teljes P5-számítás. Visszaad: (sorok lista-listája, arany_info)."""
    import futtat
    forras_dir = forras_dir or kv.F21P
    ar = {f: futtat.ARAK[FUTAS_MODELL[f]] for f in FUTAS_MODELL}
    assert FUTAS_MODELL[SONNET] == futtat.MODELLEK['S'] and FUTAS_MODELL[C3] == futtat.MODELLEK['C']
    vd = vd or kv.Versadat()
    bib = bib or kv.biblia(vd, kv.F22_RETEG_KONYVEK)      # irányadó: F22 műfaji öt réteg (PD12)
    F22 = kv.F22_RETEGEK
    kk = {f: kotegek_p3c(f, vd, forras_dir) for f in FUTAS_MODELL}
    param = {f: kp.illeszt(kk[f], ar[f]) for f in kk}
    sorok = [['szakasz', 'osszeallitas', 'reteg', 'mero', 'ertek', 'also90', 'felso90', 'megjegyzes']]

    def add(*m):
        sorok.append([str(x) for x in m])

    nev = {SONNET: OSS_S, C3: OSS_C}
    for f in kk:
        cin, cout, M, s = param[f]
        add('illesztes', nev[f], '-', 'bemenet_a_b_c', '%.2f / %.4f / %.4f' % tuple(cin), '', '', '%d első próbálkozású hívás (%s)' % (len(kk[f]), f))
        add('illesztes', nev[f], '-', 'kimenet_a_b', '%.2f / %.4f' % tuple(cout), '', '', '')
        add('ar', nev[f], '-', 'cost1_per_tablaar_s', round(s, 6), '', '',
            'táblaár %s: %.2f/%.2f USD/1M' % ((FUTAS_MODELL[f],) + ar[f]))
        add('ar', nev[f], '-', 'ujrakeres_szorzo_M', round(M, 6), '', '',
            'a futás saját mért adatából: Σcost / Σcost(első próba); hívás/köteg = %.2f' % (sum(q['hivas'] for q in kk[f]) / len(kk[f])))
    # ellenőrzés a 200 versre: futásonként és a párra
    for cimke, fs in ((OSS_S, [SONNET]), (OSS_C, [C3]), (OSS_PAR, [SONNET, C3])):
        pred, loo, tenyl = _ellenorzes([kk[f] for f in fs], [ar[f] for f in fs])
        bent, loo_sz = 100 * (pred - tenyl) / tenyl, 100 * (loo - tenyl) / tenyl
        sz, melyik = kv.szamito_ellenorzes(bent, loo_sz)
        add('ellenorzes', cimke, '-', 'pilot_vetitett_usd', round(pred, 6), '', '', 'mintán belül')
        add('ellenorzes', cimke, '-', 'pilot_tenyleges_usd', round(tenyl, 6), '', '', 'futasnaplo.tsv')
        add('ellenorzes', cimke, '-', 'elteres_szazalek', round(bent, 3), '', '', 'mintán belül, küszöb ≤ 10%')
        add('ellenorzes', cimke, '-', 'loo_elteres_szazalek', round(loo_sz, 3), '', '', 'leave-one-out, küszöb ≤ 10%')
        add('ellenorzes', cimke, '-', 'szamito_elteres_szazalek', round(sz, 3), '', '',
            'PD12/DT21 g): a konzervatívabb (nagyobb abszolút eltérésű) számít: %s; küszöb ≤ 10%%: %s'
            % (melyik, 'teljesül' if abs(sz) <= 10 else 'nem teljesül'))
    alap = osszeallitasok(param, ar, bib)
    rnd = random.Random(MAG)
    boot = {o: {r: [] for r in F22 + ['Összes']} for o in alap}
    for _ in range(n_boot):
        par = {}
        for f in kk:
            minta_k = [kk[f][rnd.randrange(len(kk[f]))] for _ in kk[f]]
            par[f] = kp.illeszt(minta_k, ar[f])
        b = osszeallitasok(par, ar, bib)
        for o in b:
            for r in b[o]:
                boot[o][r].append(b[o][r])
    for o in alap:
        for r in F22 + ['Összes']:
            bs = sorted(boot[o][r])
            add('vetites', o, r, 'koltseg_usd', round(alap[o][r], 4), round(bs[int(0.05 * len(bs))], 4),
                round(bs[int(0.95 * len(bs)) - 1], 4),
                'F22 műfaji réteg; bootstrap %d (köteg-egység: PD12); Sonnet+C = a két futás vetítésének összege, döntőbíró nélkül' % len(bs))
    for r in F22:
        add('biblia_rs', '-', r, 'versek_szama', bib[r]['n'], '', '', 'szavak (eredeti+Károli) %d, KJV-szavak %d' % (bib[r]['x'], bib[r]['k']))
    # kézimunka: a pár `alacsony` linkjei és az aranytól való eltérés, F22-rétegenként (a minta versei könyv szerint leképezve)
    adat, info = mp.betolt(forras_dir, arany_ut, arany_sha)
    kim = mp.par_kimenet(adat)
    tot_a = tot_e = tot_l = 0.0
    for r in F22:
        vs = [ig for ig in adat.versek if kv.f22_reteg(ig) == r]
        if not vs:
            add('kezimunka', OSS_PAR, r, 'alacsony_link_per_vers', 'n.é.', '', '', 'nincs minta-vers a rétegben')
            continue
        ala = sum(1 for ig in vs for s_ in kim[ig].values() if s_ == 'alacsony')
        av = [ig for ig in vs if ig in adat.arany]
        elt = sum(len(set(kim[ig]) ^ adat.arany_linkek(ig)) for ig in av)
        add('kezimunka', OSS_PAR, r, 'alacsony_link_per_vers', round(ala / len(vs), 4), '', '',
            'mért, %d vers (könyv szerint F22-rétegre képezve)' % len(vs))
        add('kezimunka', OSS_PAR, r, 'vetitett_alacsony_link_biblia', round(ala / len(vs) * bib[r]['n']), '', '', '× %d vers' % bib[r]['n'])
        tot_a += ala / len(vs) * bib[r]['n']
        osz = sum(len(kim[ig]) for ig in vs)          # F21.80: minden link a pár végső kimenetében (a vetített alacsony arányhoz)
        add('kezimunka', OSS_PAR, r, 'link_per_vers', round(osz / len(vs), 4), '', '', 'mért, %d vers (a pár végső kimenete, minden szint)' % len(vs))
        add('kezimunka', OSS_PAR, r, 'vetitett_link_biblia', round(osz / len(vs) * bib[r]['n']), '', '', '× %d vers' % bib[r]['n'])
        tot_l += osz / len(vs) * bib[r]['n']
        if av:
            add('kezimunka', OSS_PAR, r, 'elteres_per_vers_arany', round(elt / len(av), 4), '', '', 'mért, %d aranyvers (%s)' % (len(av), info['verzio']))
            add('kezimunka', OSS_PAR, r, 'vetitett_elteres_biblia', round(elt / len(av) * bib[r]['n']), '', '', '× %d vers (kis n)' % bib[r]['n'])
            tot_e += elt / len(av) * bib[r]['n']
        else:
            add('kezimunka', OSS_PAR, r, 'elteres_per_vers_arany', 'n.é.', '', '', 'nincs aranyvers a rétegben')
    add('kezimunka', OSS_PAR, 'Összes', 'vetitett_alacsony_link_biblia', round(tot_a), '', '', 'F22-rétegenként vetítve')
    add('kezimunka', OSS_PAR, 'Összes', 'vetitett_link_biblia', round(tot_l), '', '', 'F22-rétegenként vetítve (minden szint)')
    add('kezimunka', OSS_PAR, 'Összes', 'vetitett_alacsony_arany', round(tot_a / tot_l, 4) if tot_l else 'n.é.', '', '',
        'F21.80: vetitett_alacsony_link_biblia / vetitett_link_biblia (az (5) feltétel vetített alakja)')
    add('kezimunka', OSS_PAR, 'Összes', 'vetitett_elteres_biblia', round(tot_e), '', '', 'F22-rétegenként vetítve (a nem n.é. rétegek összege)')
    add('kezimunka', OSS_PAR, 'Összes', 'c_hiba_per_vers', 'n.é.', '', '', 'az eltérések (a)/(b)/(c) besorolása a futás után kézi (c_diff_p3c.py)')
    return sorok, info


# ---------------------------------------------------------------------------
# --csak-c (F21.71): a C (F3V3) egyedül; a v2-es C-futások (F3V2, F3V2B) tájékoztatásul
# ---------------------------------------------------------------------------

KIMENET_C = os.path.join(kv.F21P, 'koltseg_vetites_p3c_c.tsv')
C2, C2B = mp.C2, mp.C2B
FUTASOK_C = (C3, C2, C2B)


def szamol_c(forras_dir=None, arany_ut=None, arany_sha=None, n_boot=N_BOOT, vd=None, bib=None):
    """A csak-C P5: futásonként (F3V3 irányadó; F3V2, F3V2B tájékoztató) illesztés, ár, M a saját
    adatból, ellenőrzés a 200 versre (mintán belül + leave-one-out, a konzervatívabb számít), vetítés
    F22-rétegenként, köteg-bootstrap. Visszaad: (sorok, arany_info)."""
    import futtat
    forras_dir = forras_dir or kv.F21P
    modell = futtat.MODELLEK['C']
    ar = futtat.ARAK[modell]
    vd = vd or kv.Versadat()
    bib = bib or kv.biblia(vd, kv.F22_RETEG_KONYVEK)
    F22 = kv.F22_RETEGEK
    kk = {f: kotegek_p3c(f, vd, forras_dir) for f in FUTASOK_C}
    param = {f: kp.illeszt(kk[f], ar) for f in kk}
    sorok = [['szakasz', 'osszeallitas', 'reteg', 'mero', 'ertek', 'also90', 'felso90', 'megjegyzes']]

    def add(*m):
        sorok.append([str(x) for x in m])
    szerep = {C3: 'IRÁNYADÓ (prompt_v3)', C2: 'tájékoztató (prompt_v2)', C2B: 'tájékoztató (prompt_v2, a C második futása)'}
    for f in FUTASOK_C:
        cin, cout, M, s = param[f]
        n = mp.NEVEK[f]
        add('illesztes', n, '-', 'bemenet_a_b_c', '%.2f / %.4f / %.4f' % tuple(cin), '', '', '%d első próbálkozású hívás (%s; %s)' % (len(kk[f]), f, szerep[f]))
        add('illesztes', n, '-', 'kimenet_a_b', '%.2f / %.4f' % tuple(cout), '', '', 'a kimeneti token a gondolkodási tokent is tartalmazza, ha a modell jelenti')
        add('illesztes', n, '-', 'gondolkodasi_token_osszesen', sum(q['gond'] for q in kk[f]), '', '', 'futasnaplo.tsv gondolkodas_token (minden hívás)')
        add('ar', n, '-', 'cost1_per_tablaar_s', round(s, 6), '', '', 'táblaár %s: %.2f/%.2f USD/1M' % ((modell,) + ar))
        add('ar', n, '-', 'ujrakeres_szorzo_M', round(M, 6), '', '',
            'a futás saját mért adatából: Σcost / Σcost(első próba); hívás/köteg = %.2f' % (sum(q['hivas'] for q in kk[f]) / len(kk[f])))
        pred, loo, tenyl = _ellenorzes([kk[f]], [ar])
        bent, loo_sz = 100 * (pred - tenyl) / tenyl, 100 * (loo - tenyl) / tenyl
        sz, melyik = kv.szamito_ellenorzes(bent, loo_sz)
        add('ellenorzes', n, '-', 'pilot_vetitett_usd', round(pred, 6), '', '', 'mintán belül (200 vers, %d köteg)' % len(kk[f]))
        add('ellenorzes', n, '-', 'pilot_loo_vetitett_usd', round(loo, 6), '', '', 'leave-one-out (kötegenként kihagyva)')
        add('ellenorzes', n, '-', 'pilot_tenyleges_usd', round(tenyl, 6), '', '', 'futasnaplo.tsv (minden hívás)')
        add('ellenorzes', n, '-', 'elteres_szazalek', round(bent, 3), '', '', 'mintán belül, küszöb ≤ 10%')
        add('ellenorzes', n, '-', 'loo_elteres_szazalek', round(loo_sz, 3), '', '', 'leave-one-out, küszöb ≤ 10%')
        add('ellenorzes', n, '-', 'szamito_elteres_szazalek', round(sz, 3), '', '',
            'PD12/DT21 g): a konzervatívabb (nagyobb abszolút eltérésű) számít: %s; küszöb ≤ 10%%: %s'
            % (melyik, 'teljesül' if abs(sz) <= 10 else 'nem teljesül'))
    alap = {mp.NEVEK[f]: kp.vetit_futas(param[f], ar, bib) for f in FUTASOK_C}
    rnd = random.Random(MAG)
    boot = {o: {r: [] for r in F22 + ['Összes']} for o in alap}
    for _ in range(n_boot):
        for f in FUTASOK_C:
            minta_k = [kk[f][rnd.randrange(len(kk[f]))] for _ in kk[f]]
            v = kp.vetit_futas(kp.illeszt(minta_k, ar), ar, bib)
            for r in v:
                boot[mp.NEVEK[f]][r].append(v[r])
    for f in FUTASOK_C:
        o = mp.NEVEK[f]
        for r in F22 + ['Összes']:
            bs = sorted(boot[o][r])
            add('vetites', o, r, 'koltseg_usd', round(alap[o][r], 4), round(bs[int(0.05 * len(bs))], 4),
                round(bs[int(0.95 * len(bs)) - 1], 4),
                'F22 műfaji réteg; bootstrap %d (köteg-egység: PD12); %s; KJV-támpont a vetítésben a régi táblák szerint '
                '(1Móz, 2Móz, Péld), mint az F3V3-ban' % (len(bs), szerep[f]))
    for r in F22:
        add('biblia_rs', '-', r, 'versek_szama', bib[r]['n'], '', '', 'szavak (eredeti+Károli) %d, KJV-szavak %d' % (bib[r]['x'], bib[r]['k']))
    # kézimunka: egymodelles összeállításnál az alacsony szint n.é. (PD6); az aranytól való eltérés/vers tájékoztató
    adat, info = mp.betolt(forras_dir, arany_ut, arany_sha, list(FUTASOK_C))
    oss = mp.NEVEK[C3]
    add('kezimunka', oss, 'Összes', 'alacsony_link_biblia', 'n.é.', '', '', 'egymodelles összeállítás (PD6): az alacsony szint nem értelmezhető')
    tot = 0.0
    for r in F22:
        av = [ig for ig in adat.versek if kv.f22_reteg(ig) == r and ig in adat.arany and adat.ok(C3, ig)]
        if not av:
            add('kezimunka', oss, r, 'elteres_per_vers_arany', 'n.é.', '', '', 'nincs (kapun átment) aranyvers a rétegben')
            continue
        elt = sum(len(adat.linkek(C3, ig) ^ adat.arany_linkek(ig)) for ig in av)
        add('kezimunka', oss, r, 'elteres_per_vers_arany', round(elt / len(av), 4), '', '',
            'TÁJÉKOZTATÓ: mért, %d aranyvers (%s); hiányzó + többlet link/vers' % (len(av), info['verzio']))
        add('kezimunka', oss, r, 'vetitett_elteres_biblia', round(elt / len(av) * bib[r]['n']), '', '', '× %d vers (kis n)' % bib[r]['n'])
        tot += elt / len(av) * bib[r]['n']
    add('kezimunka', oss, 'Összes', 'vetitett_elteres_biblia', round(tot), '', '', 'TÁJÉKOZTATÓ: F22-rétegenként vetítve (a nem n.é. rétegek összege)')
    return sorok, info


def fejlec_c(info, ts):
    return ('GENERÁLT: eszkozok/karoli_strong/koltseg_vetit_p3c.py --csak-c | scope=P5 a regressziós mérésre: a C (F3V3, prompt_v3) '
            'egyedül, irányadó; a v2-es C-futások (F3V2, F3V2B, prompt_v2) tájékoztatásul; a SONNETV3 nem futott (a Sonnet és a '
            'Sonnet+C vetítése nincs adat); teljes Biblia 31 158 vers, F22 műfaji öt réteg (PD12), kézimunka-tájékoztató az arany '
            '%s-höz | forras=f21p/futasnaplo.tsv, f21p/valaszok/{F3V3,F3V2,F3V2B}.jsonl, f21p/minta.tsv, konkordancia/Karoli_1908.tsv, '
            'konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/KJV_Strongs_*.tsv, %s (sha256 %s, ellenőrizve) | '
            'ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | mag=%d | kézzel szerkeszteni tilos'
            % (info['verzio'], os.path.basename(info['jsonl']), info['sha256'][:16], ts, MAG))


def fut_c(forras_dir=None, arany_ut=None, arany_sha=None, ut=None, ts=None, n_boot=N_BOOT):
    sorok, info = szamol_c(forras_dir, arany_ut, arany_sha, n_boot)
    ut = ut or KIMENET_C
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# ' + fejlec_c(info, ts or tokenek.generalas_ts()) + '\n')
        for s in sorok:
            assert all('\t' not in x for x in s)
            fh.write('\t'.join(s) + '\n')
    for s in sorok:
        if s[0] == 'vetites' and s[2] == 'Összes':
            print('vetites %s: %s USD [%s–%s]' % (s[1], s[4], s[5], s[6]))
        if s[0] == 'ellenorzes' and s[3] == 'szamito_elteres_szazalek':
            print('  ellenőrzés %s: %s%% (%s)' % (s[1], s[4], s[7]))
    print('-> %s' % ut)
    return 0


def onteszt_csak_c(mappa, info, ellen):
    """A --csak-c önteszt a mock-adaton (a SONNETV3 nélkül is fut)."""
    import contextlib
    import io
    os.remove(os.path.join(mappa, 'valaszok', 'SONNETV3.jsonl'))
    ut1, ut2 = os.path.join(mappa, 'c1.tsv'), os.path.join(mappa, 'c2.tsv')
    with contextlib.redirect_stdout(io.StringIO()):
        fut_c(mappa, info['arany_ut'], info['arany_sha'], ut1, 'T1', n_boot=60)
        fut_c(mappa, info['arany_ut'], info['arany_sha'], ut2, 'T2', n_boot=60)
    with open(ut1, encoding='utf-8') as f:
        t1 = f.read()
    with open(ut2, encoding='utf-8') as f:
        t2 = f.read()
    ellen(t1.replace('ts=T1 ', 'ts=T2 ') == t2, 'csak-c: a vetítés nem determinisztikus')
    s0 = t1.split('\n')[0]
    ellen(s0.startswith('# GENERÁLT: eszkozok/karoli_strong/koltseg_vetit_p3c.py --csak-c | scope=') and ' | forras=' in s0 and ' | ts=T1 ' in s0,
          'csak-c: a TSV fejléce nem a scope|forras|ts proveniencia')
    sorok = [x.split('\t') for x in t1.split('\n')[2:] if x]
    ellen(all(len(x) == 8 for x in sorok), 'csak-c: a TSV-sorok nem mind 8 mezősek')
    F22 = kv.F22_RETEGEK
    vet = {(x[1], x[2]): (float(x[4]), float(x[5]), float(x[6])) for x in sorok if x[0] == 'vetites'}
    nevek = [mp.NEVEK[f] for f in FUTASOK_C]
    ellen(set(vet) == {(o, r) for o in nevek for r in F22 + ['Összes']}, 'csak-c: a vetítés nem pontosan a három C-futás × F22-rétegek')
    ellen(all(v[1] <= v[2] and v[0] > 0 for v in vet.values()), 'csak-c: a vetítés intervalluma/értéke hibás')
    ellen(all(abs(sum(vet[(o, r)][0] for r in F22) - vet[(o, 'Összes')][0]) < 6e-4 for o in nevek), 'csak-c: a rétegek összege nem az Összes')
    ellen(not any(x[1] in (OSS_S, OSS_PAR) for x in sorok), 'csak-c: Sonnet- vagy pár-sor a kimenetben')
    naplo = kv._tsv(os.path.join(mappa, 'futasnaplo.tsv'))
    for f in FUTASOK_C:
        rs = [r for r in naplo if r['futas'] == f]
        m_ert = sum(float(r['koltseg_usd']) for r in rs) / sum(float(r['koltseg_usd']) for r in rs if r['probalkozas'] == '1')
        x = [s for s in sorok if s[0] == 'ar' and s[1] == mp.NEVEK[f] and s[3] == 'ujrakeres_szorzo_M']
        ellen(x and abs(float(x[0][4]) - m_ert) < 2e-6, 'csak-c: M (%s) nem a saját adatból' % f)
        t = [s for s in sorok if s[0] == 'ellenorzes' and s[1] == mp.NEVEK[f] and s[3] == 'pilot_tenyleges_usd']
        ellen(t and abs(float(t[0][4]) - sum(float(r['koltseg_usd']) for r in rs)) < 2e-6, 'csak-c: a tényleges költség nem a napló összege (%s)' % f)
        e = {s[3]: float(s[4]) for s in sorok if s[0] == 'ellenorzes' and s[1] == mp.NEVEK[f] and s[3].endswith('szazalek')}
        ellen(abs(e['szamito_elteres_szazalek']) == max(abs(e['elteres_szazalek']), abs(e['loo_elteres_szazalek'])),
              'csak-c: a számító eltérés nem a konzervatívabb (%s)' % f)
    ellen(any(s[0] == 'kezimunka' and s[3] == 'alacsony_link_biblia' and s[4] == 'n.é.' for s in sorok), 'csak-c: az alacsony kézimunka nem n.é.')


def fejlec(info, ts):
    return ('GENERÁLT: eszkozok/karoli_strong/koltseg_vetit_p3c.py | scope=P5 a regressziós mérésre: Sonnet egyedül (SONNETV3), '
            'C (F3V3), Sonnet+C (a két futás költségének összege, döntőbíró nélkül), prompt_v3, teljes Biblia 31 158 vers, F22 '
            'műfaji öt réteg (PD12), kézimunka az arany %s-höz | forras=f21p/futasnaplo.tsv, f21p/valaszok/{SONNETV3,F3V3}.jsonl, '
            'f21p/minta.tsv, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, '
            'konkordancia/KJV_Strongs_*.tsv, %s (sha256 %s, ellenőrizve) | ts=%s (a generálás ideje; ismételt futáskor csak ez a '
            'sor tér el) | mag=%d | kézzel szerkeszteni tilos' % (info['verzio'], os.path.basename(info['jsonl']), info['sha256'][:16], ts, MAG))


def ir(sorok, info, ut, ts):
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# ' + fejlec(info, ts) + '\n')
        for s in sorok:
            assert all('\t' not in x for x in s)
            fh.write('\t'.join(s) + '\n')


def fut(forras_dir=None, arany_ut=None, arany_sha=None, ut=None, ts=None, n_boot=N_BOOT):
    sorok, info = szamol(forras_dir, arany_ut, arany_sha, n_boot)
    ir(sorok, info, ut or KIMENET, ts or tokenek.generalas_ts())
    for s in sorok:
        if s[0] == 'vetites' and s[2] == 'Összes':
            print('vetites %s: %s USD [%s–%s]' % (s[1], s[4], s[5], s[6]))
        if s[0] == 'ellenorzes' and s[3] == 'szamito_elteres_szazalek':
            print('  ellenőrzés %s: %s%% (%s)' % (s[1], s[4], s[7]))
    print('-> %s' % (ut or KIMENET))
    return 0


def onteszt():
    import contextlib
    import io
    import shutil
    import p3c_mock
    hibak = []

    def ellen(f, leiras):
        if not f:
            hibak.append(leiras)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'a régi kimenetek megváltoztak: %s' % p3c_mock.regi_kimenetek_hibak())
    with contextlib.redirect_stdout(io.StringIO()):
        ellen(kp.onteszt() == 0, 'a koltseg_vetit_p3b önteszt (a közös illesztés/vetítés) hibás')
    # a szorzók kézzel: két ismert költségű köteg; a pár összege az egyes futások összege
    kk = {SONNET: [{'x': 100, 'k': 0, 'in': 1000 + 10 * 100, 'out': 50 + 2 * 100, 'cost1': 0.0, 'cost_ossz': 0.0},
                   {'x': 200, 'k': 10, 'in': 1000 + 10 * 200 + 3 * 10, 'out': 50 + 2 * 200, 'cost1': 0.0, 'cost_ossz': 0.0},
                   {'x': 300, 'k': 0, 'in': 1000 + 10 * 300, 'out': 50 + 2 * 300, 'cost1': 0.0, 'cost_ossz': 0.0}]}
    ar = (2.0, 10.0)
    for q in kk[SONNET]:
        q['cost1'] = (q['in'] * ar[0] + q['out'] * ar[1]) / 1e6 * 0.5      # s = 0.5
        q['cost_ossz'] = q['cost1'] * 1.25                                  # M = 1.25
    p = kp.illeszt(kk[SONNET], ar)
    ellen(abs(p[3] - 0.5) < 1e-9 and abs(p[2] - 1.25) < 1e-9, 'illesztés: s/M hibás: %s' % (p[2:],))
    c = kp.koltseg(p, ar, 400, 0, 1)
    ellen(abs(c - (1000 + 4000) / 1e6 * 2.0 * 0.5 * 1.25 - (50 + 800) / 1e6 * 10.0 * 0.5 * 1.25) < 1e-12, 'Sonnet-árú költség hibás: %s' % c)
    bib_mock = {'r1': {'n': 25, 'x': 5000, 'k': 100}, 'r2': {'n': 12, 'x': 2400, 'k': 0}}
    kk_c = [dict(q, cost1=(q['in'] * 0.75 + q['out'] * 3.75) / 1e6 * 0.5) for q in kk[SONNET]]   # ugyanazok a tokenek, C-ár
    for q in kk_c:
        q['cost_ossz'] = q['cost1'] * 1.25
    par = {SONNET: p, C3: kp.illeszt(kk_c, (0.75, 3.75))}
    ar2 = {SONNET: (2.0, 10.0), C3: (0.75, 3.75)}
    o = osszeallitasok(par, ar2, bib_mock)
    ellen(all(abs(o[OSS_PAR][r] - o[OSS_S][r] - o[OSS_C][r]) < 1e-12 for r in ('r1', 'r2', 'Összes'))
          and abs(o[OSS_PAR]['Összes'] - o[OSS_PAR]['r1'] - o[OSS_PAR]['r2']) < 1e-12 and o[OSS_S]['Összes'] > o[OSS_C]['Összes'],
          'a Sonnet+C nem a két futás összege / a réteg-összeg nem az Összes')
    # mock-adatos menet a teljes Bibliára (F22 rétegek), determinisztikusan
    mappa = p3c_mock.ideiglenes('f21p_onteszt_koltseg_p3c_')
    try:
        info = p3c_mock.general(mappa)
        ut1, ut2 = os.path.join(mappa, 'k1.tsv'), os.path.join(mappa, 'k2.tsv')
        with contextlib.redirect_stdout(io.StringIO()):
            fut(mappa, info['arany_ut'], info['arany_sha'], ut1, 'T1', n_boot=100)
            fut(mappa, info['arany_ut'], info['arany_sha'], ut2, 'T2', n_boot=100)
        with open(ut1, encoding='utf-8') as f:
            t1 = f.read()
        with open(ut2, encoding='utf-8') as f:
            t2 = f.read()
        ellen(t1.replace('ts=T1 ', 'ts=T2 ') == t2, 'a vetítés nem determinisztikus (a ts-en kívül eltérés)')
        ellen(t1.startswith('# GENERÁLT: eszkozok/karoli_strong/koltseg_vetit_p3c.py | scope=') and ' | forras=' in t1.split('\n')[0]
              and ' | ts=T1 ' in t1.split('\n')[0], 'a TSV fejléce nem a scope|forras|ts proveniencia')
        sorok = [x.split('\t') for x in t1.split('\n')[2:] if x]
        ellen(all(len(x) == 8 for x in sorok), 'a TSV-sorok nem mind 8 mezősek')
        F22 = kv.F22_RETEGEK
        vet = {(x[1], x[2]): (float(x[4]), float(x[5]), float(x[6])) for x in sorok if x[0] == 'vetites'}
        ellen(all((o_, r) in vet for o_ in (OSS_S, OSS_C, OSS_PAR) for r in F22 + ['Összes']), 'a vetítés nem fedi az összeállításokat × F22-rétegeket')
        ellen(all(v[1] <= v[2] and v[0] > 0 for v in vet.values()), 'a vetítés intervalluma/értéke hibás')
        ellen(abs(vet[(OSS_PAR, 'Összes')][0] - vet[(OSS_S, 'Összes')][0] - vet[(OSS_C, 'Összes')][0]) < 2e-4,
              'Sonnet+C ≠ Sonnet + C (Összes)')
        ellen(abs(sum(vet[(OSS_PAR, r)][0] for r in F22) - vet[(OSS_PAR, 'Összes')][0]) < 6e-4, 'a rétegek összege nem az Összes')
        ellen(vet[(OSS_S, 'Összes')][0] > vet[(OSS_C, 'Összes')][0], 'a Sonnet nem drágább a C-nél a mockban (ár 2/10 vs 0.75/3.75 egyező tokenekkel)')
        # M és s független újraszámolása a naplóból
        naplo = kv._tsv(os.path.join(mappa, 'futasnaplo.tsv'))
        for f, oss in ((SONNET, OSS_S), (C3, OSS_C)):
            rs = [r for r in naplo if r['futas'] == f]
            m_ert = sum(float(r['koltseg_usd']) for r in rs) / sum(float(r['koltseg_usd']) for r in rs if r['probalkozas'] == '1')
            x = [s for s in sorok if s[0] == 'ar' and s[1] == oss and s[3] == 'ujrakeres_szorzo_M']
            ellen(x and abs(float(x[0][4]) - m_ert) < 2e-6, 'M (%s): %s vs független %.6f' % (oss, x[0][4] if x else None, m_ert))
            xs = [s for s in sorok if s[0] == 'ar' and s[1] == oss and s[3] == 'cost1_per_tablaar_s']
            ellen(xs and abs(float(xs[0][4]) - 1.0) < 1e-5, 's (%s) a mockban (táblaár = cost) nem 1: %s' % (oss, xs[0][4] if xs else None))
        ellen(any(s[0] == 'ar' and s[1] == OSS_S and 'anthropic/claude-sonnet-5.5: 2.00/10.00' in s[7] for s in sorok), 'a Sonnet táblaára nincs a sorokban')
        # ellenőrzés: futásonként és a párra, a konzervatívabb számít
        for oss in (OSS_S, OSS_C, OSS_PAR):
            x = {s[3]: s for s in sorok if s[0] == 'ellenorzes' and s[1] == oss}
            ellen({'pilot_vetitett_usd', 'pilot_tenyleges_usd', 'elteres_szazalek', 'loo_elteres_szazalek', 'szamito_elteres_szazalek'} <= set(x),
                  'az ellenőrzés sorai hiányosak: %s (%s)' % (oss, sorted(x)))
            if x:
                b_, l_, sz = (float(x[k][4]) for k in ('elteres_szazalek', 'loo_elteres_szazalek', 'szamito_elteres_szazalek'))
                ellen(abs(sz) == max(abs(b_), abs(l_)), 'a számító eltérés nem a konzervatívabb: %s' % oss)
        t_par = float([s for s in sorok if s[0] == 'ellenorzes' and s[1] == OSS_PAR and s[3] == 'pilot_tenyleges_usd'][0][4])
        t_s = float([s for s in sorok if s[0] == 'ellenorzes' and s[1] == OSS_S and s[3] == 'pilot_tenyleges_usd'][0][4])
        t_c = float([s for s in sorok if s[0] == 'ellenorzes' and s[1] == OSS_C and s[3] == 'pilot_tenyleges_usd'][0][4])
        ellen(abs(t_par - t_s - t_c) < 2e-6, 'a pár tényleges költsége nem a két futás összege')
        ellen(abs(t_s - sum(float(r['koltseg_usd']) for r in naplo if r['futas'] == SONNET)) < 2e-6, 'a Sonnet tényleges költsége nem a napló összege')
        # kézimunka: az Összes a rétegek összege
        ala = [float(s[4]) for s in sorok if s[0] == 'kezimunka' and s[3] == 'vetitett_alacsony_link_biblia' and s[2] != 'Összes']
        tot = [float(s[4]) for s in sorok if s[0] == 'kezimunka' and s[3] == 'vetitett_alacsony_link_biblia' and s[2] == 'Összes']
        ellen(tot and abs(sum(ala) - tot[0]) <= len(ala), 'a kézimunka Összes nem a rétegek összege (%s vs %s)' % (sum(ala), tot))
        onteszt_csak_c(mappa, info, ellen)
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('koltseg_vetit_p3c önteszt rendben (Sonnet-árú illesztés, s és M a saját adatból, pár = összeg, F22-rétegek, '
          'ellenőrzés futásonként és párra, determinizmus, régi kimenetek bájtazonossága; --csak-c: három C-futás, M és tényleges '
          'költség a saját adatból, konzervatívabb ellenőrzés, SONNETV3 nélkül)')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--arany', default=None, help='az arany jsonl-je (alap: a legfrissebb befagyasztott)')
    ap.add_argument('--arany-sha', default=None)
    ap.add_argument('--forras-dir', default=None, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    ap.add_argument('--csak-c', action='store_true',
                    help='a C (F3V3) egyedül, a v2-es C-futások tájékoztatásul, a Sonnet nélkül (kimenet: koltseg_vetites_p3c_c.tsv)')
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    if args.csak_c:
        return fut_c(args.forras_dir, args.arany, args.arany_sha)
    return fut(args.forras_dir, args.arany, args.arany_sha)


if __name__ == '__main__':
    sys.exit(main())
