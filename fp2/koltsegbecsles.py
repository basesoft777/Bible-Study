#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fp2/koltsegbecsles.py -- FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 7. lepes
(es a felhasznalo kiegeszito kerdesei): a teljes Thayer forditasanak
koltsegbecslese modellenkent, tobb forgatokonyvben.

    python fp2/koltsegbecsles.py
"""
import os
import re
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'fp2'))
import fordit  # noqa: E402

THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
FUTASNAPLO_UT = os.path.join(REPO, 'fp2', 'futasnaplo.tsv')
MINTA_UT = os.path.join(REPO, 'fp2', 'minta.tsv')


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


# ---------------------------------------------------------------------------
# 0. alapadatok
# ---------------------------------------------------------------------------

def thayer_adatok():
    thayer = {r['Strong_padded']: r['Teljes_szocikk'] for r in tsv_dict_sorok(THAYER_UT)}
    return thayer


ARAK = {
    # id: (prompt_usd_per_1M, completion_usd_per_1M, cache_read_usd_per_1M)
    'google/gemini-3.1-flash-lite': (0.25, 1.50, 0.025),
    'deepseek/deepseek-v4-flash': (0.14, 0.28, 0.028),
    'minimax/minimax-m3': (0.30, 1.20, 0.06),
}


def overhead_token_regresszio(futasnaplo, minta_hossz, model_id):
    """Linearis regresszio (legkisebb negyzetek, 1 valtozo): bemenet_token =
    A (fix overhead-token) + B (token/forras-karakter) * forras_karakter,
    csak az EGY-darabos szocikkeken (ahol a darab forrasa == a teljes szocikk)."""
    xs, ys = [], []
    for r in futasnaplo:
        if r['modell'] != model_id or r['darab'] != '0' or r['forras'] not in ('halozat', 'cache'):
            continue
        strong = r['strong']
        if strong not in minta_hossz:
            continue
        # csak egy-darabos szocikkek (nincs "_1" tovabbi darabja ugyanahhoz a strong+modellhez)
        tobb_darabos = any(r2['strong'] == strong and r2['modell'] == model_id and r2['darab'] != '0'
                            for r2 in futasnaplo)
        if tobb_darabos:
            continue
        xs.append(minta_hossz[strong])
        ys.append(int(r['bemenet_token']))
    n = len(xs)
    if n < 2:
        return None, None
    atlag_x = sum(xs) / n
    atlag_y = sum(ys) / n
    szamlalo = sum((x - atlag_x) * (y - atlag_y) for x, y in zip(xs, ys))
    nevezo = sum((x - atlag_x) ** 2 for x in xs)
    b = szamlalo / nevezo if nevezo else 0
    a = atlag_y - b * atlag_x
    return a, b


def kimenet_arany(futasnaplo, thayer_kar, cache_dir, model_id, csak_egeszseges):
    """kimenet_token / forras_karakter arany, csak a darab sajat forras-
    karakterehez viszonyitva (a cache JSON forditas_hu hosszaval nem itt,
    hanem kulon fuggvennyel -- ez csak a token/forras-karakter aranyt adja,
    a kimeneti karakter/token aranyat a masik fuggveny szamolja)."""
    aranyok = []
    for r in futasnaplo:
        if r['modell'] != model_id or r['forras'] not in ('halozat', 'cache'):
            continue
        aranyok.append(int(r['kimenet_token']))
    return aranyok


def main():
    thayer = thayer_adatok()
    futasnaplo = list(tsv_dict_sorok(FUTASNAPLO_UT))
    minta = list(tsv_dict_sorok(MINTA_UT))
    minta_hossz = {r['strong']: int(r['hossz']) for r in minta if r['hossz_kategoria'] != 'arany'}

    print('=== 0. Thayer teljes korpusz ===')
    teljes_karakter = sum(len(t) for t in thayer.values())
    print('szocikkek:', len(thayer), '| osszes karakter:', teljes_karakter)

    print('\n=== 0b. teljes korpusz darabolasa (fordit.darabokra_bont) ===')
    darab_szamok = {s: len(fordit.darabokra_bont(t)) for s, t in thayer.items()}
    osszes_darab = sum(darab_szamok.values())
    darabolt_szocikkek = [s for s, n in darab_szamok.items() if n > 1]
    nem_darabolt_karakter = sum(len(thayer[s]) for s, n in darab_szamok.items() if n == 1)
    darabolt_karakter = sum(len(thayer[s]) for s, n in darab_szamok.items() if n > 1)
    print('osszes darab (API-hivas egy modellre): %d' % osszes_darab)
    print('darabolt szocikkek: %d (%d karakter) | nem darabolt: %d (%d karakter)'
          % (len(darabolt_szocikkek), darabolt_karakter,
             len(thayer) - len(darabolt_szocikkek), nem_darabolt_karakter))

    print('\n=== 1. overhead-token regresszio modellenkent (egy-darabos szocikkeken) ===')
    overhead = {}
    for model_id in ARAK:
        a, b = overhead_token_regresszio(futasnaplo, minta_hossz, model_id)
        overhead[model_id] = (a, b)
        print('  %-32s overhead=%.1f token | %.4f token/forras-karakter (bemenet)'
              % (model_id, a, b))

    print('\n=== 1b. a bemenet_token hany %%-a a fix overhead (prompt+terminologia+karoli), atlagosan ===')
    for model_id in ARAK:
        aranyok = []
        for r in futasnaplo:
            if r['modell'] != model_id or r['darab'] != '0' or r['forras'] not in ('halozat', 'cache'):
                continue
            strong = r['strong']
            if strong not in minta_hossz:
                continue
            a, b = overhead[model_id]
            becsult_overhead = a
            teljes = int(r['bemenet_token'])
            if teljes:
                aranyok.append(becsult_overhead / teljes)
        if aranyok:
            print('  %-32s atlag overhead-arany: %.1f%%' % (model_id, 100 * statistics.mean(aranyok)))

    # -----------------------------------------------------------------
    # 2. kimenet: kimenet_token / forras-karakter arany, csak "egeszseges"
    # (nem kritikus) szocikkeken -- ez a realis "ha mukodik" varhato arany
    # -----------------------------------------------------------------
    print('\n=== 2. kimenet_token / forras-karakter arany ("egeszseges" szocikkeken) ===')
    kritikus_par = set()
    for sor in tsv_dict_sorok(os.path.join(REPO, 'fp2', 'biralat_vegleges.tsv')):
        if 'kritikus' in sor['eredeti_hibak']:
            kritikus_par.add((sor['strong'], sor['modell']))

    kimenet_arany_modaton = {}
    for model_id in ARAK:
        # HIBA-JAVITAS (fuggetlen ellenorzes, 2026.09.28): korabban a 0. darab
        # kimenet_token-jet osztotta a TELJES szocikk hosszaval -- ez tobb-
        # darabos szocikkeknel (pl. G4151, 12 darab) sulyosan alabecsulte az
        # aranyt, mert a tobbi 11 darab kimenetet figyelmen kivul hagyta,
        # mikozben a nevezoben a teljes (nem csak az elso darab) hosszat
        # hasznalta. Javitva: modellenkent es szocikkenkent osszegezzuk az
        # OSSZES darab kimenet_token-jet, es azt osztjuk a szocikk teljes
        # forraskarakter-szamaval -- ez helyesen kezeli mind az egy-, mind a
        # tobb-darabos szocikkeket.
        szocikk_kimenet_ossz = {}
        for r in futasnaplo:
            if r['modell'] != model_id or r['forras'] not in ('halozat', 'cache'):
                continue
            strong = r['strong']
            if (strong, model_id) in kritikus_par:
                continue
            if strong not in minta_hossz:
                continue
            szocikk_kimenet_ossz[strong] = szocikk_kimenet_ossz.get(strong, 0) + int(r['kimenet_token'])

        aranyok = []
        for strong, kimenet_ossz in szocikk_kimenet_ossz.items():
            if kimenet_ossz:
                aranyok.append(kimenet_ossz / minta_hossz[strong])
        if aranyok:
            p10 = statistics.quantiles(aranyok, n=10)[0] if len(aranyok) >= 10 else min(aranyok)
            p90 = statistics.quantiles(aranyok, n=10)[8] if len(aranyok) >= 10 else max(aranyok)
            kimenet_arany_modaton[model_id] = statistics.mean(aranyok)
            print('  %-32s n=%2d atlag=%.4f token/forras-kar | p10=%.4f p90=%.4f'
                  % (model_id, len(aranyok), statistics.mean(aranyok), p10, p90))

    # -----------------------------------------------------------------
    # 3. koltseg-forgatokonyvek (a felhasznalo 2026.09.28-i jovahagyott
    # javitasaival) -- l. naplok/FP2_koltsegbecsles.md
    # -----------------------------------------------------------------
    N = osszes_darab
    C = teljes_karakter
    N_darabolt = sum(n for s, n in darab_szamok.items() if n > 1)
    C_darabolt = sum(len(thayer[s]) for s, n in darab_szamok.items() if n > 1)
    N_nemdarabolt = N - N_darabolt
    C_nemdarabolt = C - C_darabolt

    def koltseg(model_id, n, c, ar_be=None, ar_ki=None):
        a, b = overhead[model_id]
        ar_be = ar_be if ar_be is not None else ARAK[model_id][0]
        ar_ki = ar_ki if ar_ki is not None else ARAK[model_id][1]
        be = n * a + b * c
        ki = kimenet_arany_modaton[model_id] * c
        return be / 1e6 * ar_be + ki / 1e6 * ar_ki

    GEMINI = 'google/gemini-3.1-flash-lite'
    DEEPSEEK = 'deepseek/deepseek-v4-flash'
    MINIMAX = 'minimax/minimax-m3'

    print('\n=== 3. koltseg-forgatokonyvek (teljes Thayer) ===')
    for nev, mid in (('1 Gemini', GEMINI), ('2 DeepSeek', DEEPSEEK), ('3 MiniMax', MINIMAX)):
        c = koltseg(mid, N, C)
        c2 = koltseg(mid, N, C, ARAK[mid][0] * 2, ARAK[mid][1] * 2)
        print('  %-14s alap=%.3f USD | ar x2=%.3f USD' % (nev, c, c2))

    g_full = koltseg(GEMINI, N, C)
    g_retry = g_full * 1.03
    print('  4a Gemini+3%% onujra:        alap=%.3f | ar x2=%.3f' % (g_retry, g_retry * 2))

    mm_per_darab_nemdarabolt = koltseg(MINIMAX, N_nemdarabolt, C_nemdarabolt) / N_nemdarabolt
    extra_4b = (1 / 25) * N_nemdarabolt * mm_per_darab_nemdarabolt  # Gemini 4%-os hibaaranya a nem-darabolton
    b4b = g_full + extra_4b
    print('  4b Gemini+MiniMax tartalek: alap=%.3f (kb. egyenerteku a 4a-val)' % b4b)

    def cache_koltseg(ar_be, ar_ki, ar_cache):
        a, b = overhead[GEMINI]
        overhead_cache = 1 * a * ar_be / 1e6 + (N - 1) * a * ar_cache / 1e6
        forras_resz = b * C * ar_be / 1e6
        kimenet_resz = kimenet_arany_modaton[GEMINI] * C * ar_ki / 1e6
        return overhead_cache + forras_resz + kimenet_resz

    c5 = cache_koltseg(*ARAK[GEMINI])
    c5_x2 = cache_koltseg(ARAK[GEMINI][0] * 2, ARAK[GEMINI][1] * 2, ARAK[GEMINI][2] * 2)
    c7 = c5 * 1.03
    c7_x2 = c5_x2 * 1.03
    print('  5 Gemini+cache:             alap=%.3f | ar x2=%.3f' % (c5, c5_x2))
    print('  7 Gemini+cache+3%% onujra:   alap=%.3f | ar x2=%.3f' % (c7, c7_x2))

    print('\n=== 4. p10-p90 sav (kimenet-token szorasbol, bemenet fixnek tekintve) ===')
    for nev, mid in (('1 Gemini', GEMINI), ('2 DeepSeek', DEEPSEEK), ('3 MiniMax', MINIMAX)):
        a, b = overhead[mid]
        be = N * a + b * C
        aranyok = []
        szocikk_kimenet_ossz = {}
        for r in futasnaplo:
            if r['modell'] != mid or r['forras'] not in ('halozat', 'cache'):
                continue
            if r['strong'] not in minta_hossz or (r['strong'], mid) in kritikus_par:
                continue
            szocikk_kimenet_ossz[r['strong']] = szocikk_kimenet_ossz.get(r['strong'], 0) + int(r['kimenet_token'])
        for strong, ossz in szocikk_kimenet_ossz.items():
            aranyok.append(ossz / minta_hossz[strong])
        aranyok.sort()
        p10 = statistics.quantiles(aranyok, n=10)[0] if len(aranyok) >= 10 else min(aranyok)
        p90 = statistics.quantiles(aranyok, n=10)[8] if len(aranyok) >= 10 else max(aranyok)
        c_lo = be / 1e6 * ARAK[mid][0] + p10 * C / 1e6 * ARAK[mid][1]
        c_hi = be / 1e6 * ARAK[mid][0] + p90 * C / 1e6 * ARAK[mid][1]
        print('  %-14s p10=%.3f p90=%.3f USD' % (nev, c_lo, c_hi))

    a, b = overhead[GEMINI]
    be = N * a + b * C
    aranyok = []
    szocikk_kimenet_ossz = {}
    for r in futasnaplo:
        if r['modell'] != GEMINI or r['forras'] not in ('halozat', 'cache'):
            continue
        if r['strong'] not in minta_hossz or (r['strong'], GEMINI) in kritikus_par:
            continue
        szocikk_kimenet_ossz[r['strong']] = szocikk_kimenet_ossz.get(r['strong'], 0) + int(r['kimenet_token'])
    for strong, ossz in szocikk_kimenet_ossz.items():
        aranyok.append(ossz / minta_hossz[strong])
    aranyok.sort()
    p10 = statistics.quantiles(aranyok, n=10)[0] if len(aranyok) >= 10 else min(aranyok)
    p90 = statistics.quantiles(aranyok, n=10)[8] if len(aranyok) >= 10 else max(aranyok)
    a, b = overhead[GEMINI]
    overhead_cache = 1 * a * ARAK[GEMINI][0] / 1e6 + (N - 1) * a * ARAK[GEMINI][2] / 1e6
    forras_resz = b * C * ARAK[GEMINI][0] / 1e6
    c7_lo = (overhead_cache + forras_resz + p10 * C / 1e6 * ARAK[GEMINI][1]) * 1.03
    c7_hi = (overhead_cache + forras_resz + p90 * C / 1e6 * ARAK[GEMINI][1]) * 1.03
    print('  7 Gemini+cache+retry p10=%.3f p90=%.3f USD' % (c7_lo, c7_hi))

    return thayer, futasnaplo, minta, overhead, darab_szamok, osszes_darab, teljes_karakter, kimenet_arany_modaton


if __name__ == '__main__':
    main()
