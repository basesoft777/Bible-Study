#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.42 — P4 a regressziós mérésre (P3c, PD13): a Sonnet egyedül és a Sonnet + C pár, a C
(F3V3) a v2-es két C-futással egymás mellett, a prompt_v2 → v3 hatás. Nincs API-hívás.

Futások: SONNETV3 (anthropic/claude-sonnet-5.5, prompt_v3), F3V3 (C, prompt_v3), F3V2 és
F3V2B (C, prompt_v2; a v2-es két futás). A mérés az arany LEGFRISSEBB befagyasztott
változatára megy (alapból tokenek.legfrissebb_arany: a f21p/arany_opus_v3.sha256, ha létezik,
különben v2; a --arany paraméterrel felülírható), a hash-ellenőrzést a szkript maga végzi
(eltérésnél / hiányzó hash-fájlnál SystemExit, semmi nem íródik).

Összeállítások:
  * Sonnet egyedül (SONNETV3) és C egyedül (F3V3; F3V2, F3V2B): egymodelles, PD6 szerint nincs
    minősítés, az `alacsony` arány n.é.; csak mért számok (magas pontosság n.é.).
  * Sonnet+C pár: A = Sonnet (SONNETV3), B = C (F3V3, prompt_v3-mal); döntőbíró NINCS.
    A∩B = `magas`; minden más link `alacsony` (G4: `kozepes` csak döntőbíróval létezik). Ha a
    pár egyik oldala kapuhibás maradt, annak a versnek minden (a túlélő oldal) linkje `alacsony`,
    és beleszámít az `alacsony` arányba; ha mindkettő kapuhibás, a versnek nincs kimenete (a
    lefedettség nevezőjében benne marad). Ez a meres_p3b.g4_vers „A+B” ága, változatlanul.

Az öt rögzített feltétel rétegenként (R1–R4 + Összes) és n-nel (számláló/nevező minden cellában):
  (1) `magas` pontosság ≥ 98% rétegenként; (2) összes link lefedettsége ≥ 95%; (3) régi arany
  egyezés ≥ 95% (halmaz-definíció; a MÉRT érték a kizárás nélküli; a TÁJÉKOZTATÓ az 1Móz 6:17
  kizárásával, nem minősít); (4) a vetített teljes költség 90%-os intervallumának felső széle
  ≤ 60 USD (f21p/koltseg_vetites_p3c.tsv, koltseg_vetit_p3c.py); (5) az `alacsony` arány ≤ 10%
  (link-arány a végső kimenetben; a 200 versen és az aranyon). Minősítés (megfelel / nem felel
  meg, és melyik feltétel bukott) csak a Sonnet+C párra; az egymodelles összeállítás nem kaphat.

A C-futások egymás mellett (F3V2, F3V2B, F3V3): pontosság, lefedettség, régi arany, kapuhiba
első próbára/végleg és kapupont szerint, költség. A prompt_v2 → v3 hatás: Δ (F3V3 − a v2 futás,
ill. a két v2-futás átlaga) és 90%-os bootstrap a versek felett (rétegenként rétegzetten, mag
20260930), a két v2-futás eltérésével (|F3V2B − F3V2|) mint futásközi ingadozás-becsléssel
összevetve. A jelölés leíró, nem próba: „kívül” = |Δ| nagyobb az ingadozás pontbecslésénél ÉS a
Δ 90%-os intervalluma nem tartalmazza a 0-t.

Kimenet (a régi mérők kimenetei bájtra változatlanok): f21p/meres_p3c_eredmeny.tsv,
naplok/F21P_meres_p3c.md; minden kimenet fejléce a proveniencia: scope | forras | ts.

--csak-c (F21.71): a C (F3V3) EGYEDÜLI mérése, amíg a SONNETV3 nem futott. Ugyanaz a számítás
(egymodell, kapuhiba, költség, prompt-hatás), a Sonnet és a Sonnet+C pár sorai helyett
„nincs adat (SONNETV3 nem futott)” jelölés; a C-re az öt feltétel küszöb-viszonya (PD6: nincs
minősítés, az (1) és az (5) n.é.); a v2-es C-futások (F3V2, F3V2B) és az F3V3 az arany v2-re
ÉS az arany v3-ra is (az arany v2 → v3 hatás determinisztikusan, a prompt_v2 → v3 hatás
mindkét aranyon bootstrappel); az F8V3 (C KJV-támponttal, ha a jsonl megvan) tájékoztató
oszlop (R4: KJV nélkül, nem mérhető; PD17). Kimenet: f21p/meres_p3c_c_eredmeny.tsv,
naplok/F21P_meres_p3c_c.md; a (4) feltétel a f21p/koltseg_vetites_p3c_c.tsv-ből
(koltseg_vetit_p3c.py --csak-c). A Sonnet-adat megérkezése után a teljes mérés --csak-c
nélkül, ugyanezzel a szkripttel fut (az eredeti kimeneti nevekre); --csak-c nélkül a hiányzó
SONNETV3 SystemExit (semmi nem íródik).

F21.76 (--csak-c, a meglévő sorok után, a régi sorok változatlanok): (a) az első próbás kapuhiba
kapupontonként és rétegenként a három C-futásra (F3V2, F3V2B, F3V3), a versek listájával
(kapupont, köteg, rövid hibaüzenet, végleges állapot); módszer: a köteg nyers[0] válaszának
újraellenőrzése a teljes kapun, keresztellenőrzés a rétegenkénti első-próbás számokkal, a jsonl
probalkozas=2 verseivel és a napló kapuhiba_db(probalkozas=1) összegével (EGYEZIK / ELTÉR; ELTÉR:
1-es kód). (b) a 95%-os küszöbön kívüli F3V3-lefedettség jelölése rétegenként, a hiányzó linkek
K4 (a) számával a kézi besorolásból (f21p/c_diff_p3c_besorolas.tsv; Opus-besorolás, nem mérés).
    python eszkozok/karoli_strong/meres_p3c.py [--csak-c] [--arany <jsonl> [--arany-sha <sha256-fájl>]]
                                               [--forras-dir <könyvtár>] [--onteszt]
"""

import argparse
import copy
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import meres  # noqa: E402
import meres_p3b  # noqa: E402
import tokenek  # noqa: E402

F21P = meres.F21P
EREDMENY_UT = os.path.join(F21P, 'meres_p3c_eredmeny.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_meres_p3c.md')
KOLTSEG_UT = os.path.join(F21P, 'koltseg_vetites_p3c.tsv')
FUTASOK = ['SONNETV3', 'F3V3', 'F3V2', 'F3V2B']
SONNET, C3, C2, C2B = FUTASOK
PAR = 'Sonnet+C'
NEVEK = {SONNET: 'Sonnet (SONNETV3)', C3: 'C (F3V3)', C2: 'C (F3V2)', C2B: 'C (F3V2B)'}
RETEGEK = meres_p3b.RETEGEK
SZINTEK = meres_p3b.SZINTEK
MAG = 20260930
N_BOOT = 1000
Sorok = meres_p3b.Sorok
_ret = meres_p3b._ret

# --csak-c (F21.71)
F8 = 'F8V3'
NEVEK[F8] = 'C KJV-vel (F8V3, tájékoztató)'
FUTASOK_C = [C3, C2, C2B]              # a csak-C mód kötelező futásai
FUTASOK_C_OPC = [F8]                   # tájékoztató; csak ha a jsonl megvan
EREDMENY_C_UT = os.path.join(F21P, 'meres_p3c_c_eredmeny.tsv')
JELENTES_C_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_meres_p3c_c.md')
KOLTSEG_C_UT = os.path.join(F21P, 'koltseg_vetites_p3c_c.tsv')
NINCS_SONNET = 'nincs adat (SONNETV3 nem futott)'
V2_CIMKE = ' × arany v2'


def _jsonl_ut(forras_dir, f):
    return os.path.join(forras_dir or F21P, 'valaszok', '%s.jsonl' % f)


def futasok_c(forras_dir=None):
    """A csak-C mód futásai: a kötelezők és a meglévő tájékoztatók."""
    return FUTASOK_C + [f for f in FUTASOK_C_OPC if os.path.exists(_jsonl_ut(forras_dir, f))]


# ---------------------------------------------------------------------------
# betöltés (legfrissebb befagyasztott arany, hash-ellenőrzéssel)
# ---------------------------------------------------------------------------

def arany_forras(arany_ut=None, arany_sha=None):
    """(jsonl, sha256-fájl, verzió-jelölés). Alap: tokenek.legfrissebb_arany(); a --arany
    megadásakor a hash-fájl alapból ugyanaz a név .sha256 kiterjesztéssel."""
    if arany_ut is None:
        return tokenek.legfrissebb_arany()
    sha = arany_sha or os.path.splitext(arany_ut)[0] + '.sha256'
    return arany_ut, sha, os.path.basename(arany_ut)


def betolt(forras_dir=None, arany_ut=None, arany_sha=None, futasok=None):
    """(adat, arany_info). Az arany hash-ellenőrzése itt történik; hiba: SystemExit.
    futasok: a betöltendő futások (alap: FUTASOK, a teljes P3c-mérés); hiányzó jsonl: SystemExit
    (a SONNETV3 hiányánál a --csak-c módra utaló üzenettel)."""
    futasok = futasok or FUTASOK
    for f in futasok:
        if not os.path.exists(_jsonl_ut(forras_dir, f)):
            raise SystemExit('HIBA: hiányzik a futás válaszfájlja: %s%s' % (
                _jsonl_ut(forras_dir, f), ' (SONNETV3 nem futott; a C egyedüli mérése: --csak-c)' if f == SONNET else ''))
    jsonl, sha, verzio = arany_forras(arany_ut, arany_sha)
    h = tokenek.hash_hiba(jsonl, sha, 'arany %s' % verzio)
    if h:
        raise SystemExit('HIBA: %s' % h)
    arany = {o['vers']: o for o in meres._jsonl(jsonl)}
    adat = meres.Adat(futasok=futasok, forras_dir=forras_dir or F21P)
    adat.arany = arany                       # minden arany_linkek hívás a legfrissebb aranyhoz mér
    info = {'jsonl': jsonl, 'sha_fajl': sha, 'verzio': verzio, 'sha256': tokenek.sha256_lf(jsonl),
            'aranyversek': len(arany)}
    return adat, info


# ---------------------------------------------------------------------------
# a pár végső kimenete
# ---------------------------------------------------------------------------

def par_kimenet(adat, fa=SONNET, fb=C3):
    """{igehely: {link: szint}} a Sonnet+C párra (döntőbíró nélkül): A∩B magas, minden más
    link alacsony; az egyik oldal kapuhibája: a túlélő oldal linkjei alacsonyak."""
    ki = {}
    for ig in adat.versek:
        a_ok, b_ok = adat.ok(fa, ig), adat.ok(fb, ig)
        _, ab = meres_p3b.g4_vers(a_ok, b_ok, adat.linkek(fa, ig), adat.linkek(fb, ig), False, None, False)
        ki[ig] = ab
    return ki


# ---------------------------------------------------------------------------
# mérőszámok
# ---------------------------------------------------------------------------

def par_merok(adat, sorok, kim, oss=PAR):
    """A pár mérőszámai (a meres_p3b.tobbmodell egyetlen összeállításra, lapos kimenettel)."""
    for ret in RETEGEK:
        arany_v = [ig for ig in adat.versek if ig in adat.arany and _ret(adat, ig, ret)]
        szint_t = {s: 0 for s in SZINTEK}
        szint_c = {s: 0 for s in SZINTEK}
        t = c = g = 0
        for ig in arany_v:
            k, gl = kim[ig], adat.arany_linkek(ig)
            g += len(gl)
            for l, s in k.items():
                c += 1
                szint_c[s] += 1
                if l in gl:
                    t += 1
                    szint_t[s] += 1
        sorok.add('feltetelek', oss, ret, 'arany_versek', len(arany_v), len(arany_v), 'minden aranyvers (a végső kimenet üres is lehet)')
        sorok.add('feltetelek', oss, ret, 'magas_pontossag', szint_t['magas'], szint_c['magas'],
                  'G4: A∩B (Sonnet ∩ C); a KJV-ellentmondás feltétele gépileg n.é.')
        for s in ('kozepes', 'alacsony'):
            sorok.add('szintek', oss, ret, '%s_pontossag' % s, szint_t[s], szint_c[s])
        sorok.add('feltetelek', oss, ret, 'pontossag_osszes (tajekoztato)', t, c)
        sorok.add('feltetelek', oss, ret, 'lefedettseg', t, g, 'minden aranyvers')
        hb, e, hbk, ek = meres_p3b.regi_osszeallitas(adat, lambda ig: set(kim[ig]), ret)
        sorok.add('feltetelek', oss, ret, 'regi_arany_kizaras_nelkul', e, hb, 'MÉRT (DT21 i); a végső kimeneten, 200 vers')
        sorok.add('feltetelek', oss, ret, 'regi_arany_kizarassal_tajekoztato', ek, hbk,
                  'TÁJÉKOZTATÓ (DT21 i): 1Móz 6:17 nélkül; a végső kimeneten, 200 vers')
        for halmaz, vs in (('200 vers', [ig for ig in adat.versek if _ret(adat, ig, ret)]), ('arany', arany_v)):
            osz = sum(len(kim[ig]) for ig in vs)
            ala = sum(1 for ig in vs for s in kim[ig].values() if s == 'alacsony')
            sorok.add('feltetelek', oss, ret, 'alacsony_arany [%s]' % halmaz, ala, osz, 'link-arány a végső kimenetben')
            for s in SZINTEK:
                sorok.add('szintek', oss, ret, 'eloszlas_%s [%s]' % (s, halmaz),
                          sum(1 for ig in vs for x in kim[ig].values() if x == s), osz)
            ures = sum(1 for ig in vs if not kim[ig])
            sorok.add('szintek', oss, ret, 'kimenet_nelkuli_versek [%s]' % halmaz, ures, len(vs))
        # a pár versosztályai (döntőbíró nélkül)
        vs = [ig for ig in adat.versek if _ret(adat, ig, ret)]
        n = len(vs)
        oszt = {'mindketto_atment_azonos_linkekkel': 0, 'mindketto_atment_eltero_linkekkel': 0,
                'csak_Sonnet_atment': 0, 'csak_C_atment': 0, 'egyik_sem_atment': 0}
        for ig in vs:
            a, b = adat.ok(SONNET, ig), adat.ok(C3, ig)
            if a and b:
                oszt['mindketto_atment_azonos_linkekkel' if adat.linkek(SONNET, ig) == adat.linkek(C3, ig)
                     else 'mindketto_atment_eltero_linkekkel'] += 1
            elif a:
                oszt['csak_Sonnet_atment'] += 1
            elif b:
                oszt['csak_C_atment'] += 1
            else:
                oszt['egyik_sem_atment'] += 1
        for mero, x in oszt.items():
            sorok.add('par_versosztalyok', oss, ret, mero, x, n, 'a 200 verses minta')


def ab_egyezes_par(adat, sorok):
    """A Sonnet és a C (F3V3) link-egyezése (Σ|A∩B| / Σ|A∪B|, ahol mindkettő átment) — a
    meres.ab_egyezes változatlanul."""
    m = meres.Sorok()
    meres.ab_egyezes(adat, m, 'ab_egyezes', SONNET, C3, PAR)
    for r in m.lista:
        sorok.add('ab_egyezes', r['osszeallitas'], r['reteg'], r['mero'], r['szamlalo'], r['nevezo'], r['megjegyzes'])


# ---------------------------------------------------------------------------
# kapuhiba, költség
# ---------------------------------------------------------------------------

def kapuhiba_futasok(adat, sorok, futasok=FUTASOK):
    """Kapuhiba első próbára és végleg (rétegenként), kapupont szerint, keresztellenőrzéssel."""
    for f in futasok:
        elso, vegleg, elso_h = meres.hibatipusok(adat, f)
        p2 = {ig for ig, r in adat.futas[f].items() if r['probalkozas'] == 2}
        naplo_p1 = sum(int(r['kapuhiba_db']) for r in adat.naplo if r['futas'] == f and r['probalkozas'] == '1')
        egyezik = elso_h == p2 and len(elso_h) == naplo_p1
        nev = '%s' % NEVEK[f]
        sorok.add('kapuhiba_kereszt', nev, meres.OSSZES, 'keresztellenorzes_elso_probalkozas', len(elso_h), naplo_p1,
                  'újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (%d) = napló kapuhiba_db(probalkozas=1) '
                  'összeg (%d): %s' % (len(p2), naplo_p1, 'EGYEZIK' if egyezik else 'ELTÉR'))
        for ret in RETEGEK:
            vs = [ig for ig in adat.versek if ig in adat.futas[f] and _ret(adat, ig, ret)]
            if not vs:
                continue
            sorok.add('kapuhiba', nev, ret, 'elso_probara', sum(1 for ig in vs if ig in elso_h), len(vs))
            sorok.add('kapuhiba', nev, ret, 'vegleg', sum(1 for ig in vs if not adat.ok(f, ig)), len(vs))
        n = len(adat.futas[f])
        for p in sorted(set(elso) | set(vegleg)):
            sorok.add('kapuhiba_tipus', nev, meres.OSSZES, 'kapupont_%s_elso' % p, elso.get(p, 0), n)
            sorok.add('kapuhiba_tipus', nev, meres.OSSZES, 'kapupont_%s_vegleg' % p, vegleg.get(p, 0), n)


def koltseg_futasok(adat, sorok, futasok=FUTASOK):
    """A futásnapló összesítése futásonként (hívás, token, cost, gondolkodási mód, prompt-azonosító)."""
    for f in futasok:
        sor = [r for r in adat.naplo if r['futas'] == f]
        if not sor:
            continue
        nev = NEVEK[f]
        sorok.add('koltseg', nev, meres.OSSZES, 'hivasok', len(sor), '',
                  'próbálkozás=1: %d, próbálkozás=2: %d' % (sum(1 for r in sor if r['probalkozas'] == '1'),
                                                          sum(1 for r in sor if r['probalkozas'] == '2')))
        sorok.add('koltseg', nev, meres.OSSZES, 'bemeneti_token', sum(int(r['bemenet_token']) for r in sor), '', '')
        sorok.add('koltseg', nev, meres.OSSZES, 'kimeneti_token', sum(int(r['kimenet_token']) for r in sor), '',
                  'a completion_tokens (a gondolkodási token benne van, ha a modell jelenti)')
        sorok.add('koltseg', nev, meres.OSSZES, 'koltseg_usd', '%.6f' % sum(float(r['koltseg_usd']) for r in sor), '',
                  'koltseg_forras: %s' % ','.join(sorted({r['koltseg_forras'] for r in sor})))
        sorok.add('koltseg', nev, meres.OSSZES, 'gondolkodas_mod', '; '.join(sorted({r['gondolkodas_mod'] for r in sor})), '',
                  'a beállítás eltér (PD15): a C minimal (kötelező), a Sonnet minimális gondolkodási kerettel; az A és a B kikapcsolva')
        sorok.add('koltseg', nev, meres.OSSZES, 'prompt_sha256_12', '; '.join(sorted({r['prompt_sha256_12'] for r in sor})), '', '')


def mentett_ellenorzes(sorok, forras_dir, futasok=FUTASOK):
    """A mentett (allapot=ok) válaszok újraellenőrzése a teljes kapun (futtat.mentett_valaszok_ellenoriz)."""
    import futtat
    for f in futasok:
        h = futtat.mentett_valaszok_ellenoriz(f, forras_dir)
        sorok.add('mentett_ellenorzes', NEVEK[f], meres.OSSZES, 'hibak', len(h), '',
                  'futtat.mentett_valaszok_ellenoriz: %s' % ('0 hiba' if not h else '; '.join(h[:5])))


# ---------------------------------------------------------------------------
# a prompt_v2 → v3 hatás (Δ és 90% bootstrap), az ingadozással összevetve
# ---------------------------------------------------------------------------

def _kvant(b):
    b = sorted(b)
    return b[int(0.05 * len(b))], b[int(0.95 * len(b)) - 1]


def delta_adatok(adat, refs, cel, n_boot=N_BOOT):
    """{reteg: {mero: (ref, cel, delta, also90, felso90, abs95, n)}} — a cel futás és a refs futások
    átlaga közti különbség. Pontosság/lefedettség: az aranyversek, ahol MINDEN szereplő futás átment
    (a linkek összege verseken át); kapuhiba: a 200 vers. Bootstrap: versek, rétegenként rétegzetten."""
    rnd = random.Random(MAG)
    fs = list(refs) + [cel]
    arany_v = [ig for ig in adat.versek if ig in adat.arany and all(adat.ok(f, ig) for f in fs)]
    per = {ig: {f: (len(adat.linkek(f, ig) & adat.arany_linkek(ig)), len(adat.linkek(f, ig)), len(adat.arany_linkek(ig)))
                for f in fs} for ig in arany_v}
    kapu = {}
    for f in fs:
        _, _, elso = meres.hibatipusok(adat, f)
        kapu[f] = {ig: (ig in elso, not adat.ok(f, ig)) for ig in adat.versek}

    def pl(vs, f):
        t, c, g = (sum(per[ig][f][i] for ig in vs) for i in range(3))
        return (t / c if c else 0.0), (t / g if g else 0.0)

    def merok(vs, v2_):
        out = {}
        out['pontossag'] = ([pl(vs, f)[0] for f in refs], pl(vs, cel)[0])
        out['lefedettseg'] = ([pl(vs, f)[1] for f in refs], pl(vs, cel)[1])
        out['kapuhiba_elso_probara'] = ([sum(kapu[f][ig][0] for ig in v2_) / len(v2_) for f in refs],
                                        sum(kapu[cel][ig][0] for ig in v2_) / len(v2_))
        out['kapuhiba_vegleg'] = ([sum(kapu[f][ig][1] for ig in v2_) / len(v2_) for f in refs],
                                  sum(kapu[cel][ig][1] for ig in v2_) / len(v2_))
        return out

    def atlag(x):
        return sum(x) / len(x)

    sa = {r: [ig for ig in arany_v if adat.reteg[ig] == r] for r in meres.RETEGEK}
    s2 = {r: [ig for ig in adat.versek if adat.reteg[ig] == r] for r in meres.RETEGEK}
    boot = {r: [] for r in RETEGEK}
    mero_nevek = ('pontossag', 'lefedettseg', 'kapuhiba_elso_probara', 'kapuhiba_vegleg')
    for _ in range(n_boot):
        ma = {r: [s[rnd.randrange(len(s))] for _ in s] for r, s in sa.items() if s}
        m2 = {r: [s[rnd.randrange(len(s))] for _ in s] for r, s in s2.items()}
        for r in RETEGEK:
            va = sum(ma.values(), []) if r == meres.OSSZES else ma.get(r, [])
            v2_ = sum(m2.values(), []) if r == meres.OSSZES else m2[r]
            if not va or not v2_:
                continue
            m = merok(va, v2_)
            boot[r].append({k: m[k][1] - atlag(m[k][0]) for k in mero_nevek})
    ki = {}
    for r in RETEGEK:
        va = [ig for ig in arany_v if _ret(adat, ig, r)]
        v2_ = [ig for ig in adat.versek if _ret(adat, ig, r)]
        if not va or not v2_ or not boot[r]:
            continue
        m = merok(va, v2_)
        ki[r] = {}
        for k in mero_nevek:
            ref, cl = atlag(m[k][0]), m[k][1]
            b = [q[k] for q in boot[r]]
            lo, hi = _kvant(b)
            ab = sorted(abs(x) for x in b)
            ki[r][k] = (ref, cl, cl - ref, lo, hi, ab[int(0.95 * len(ab)) - 1], len(va) if k in mero_nevek[:2] else len(v2_))
    return ki


def prompt_hatas(adat, sorok, n_boot=N_BOOT, utotag='', extra=()):
    """Sorok: 'hatas' (minden összevetés) és 'hatas_osszevetes' (a prompt-hatás az ingadozáshoz képest).
    utotag: az összevetés-nevek utótagja (a csak-C mód az arany v2-re is méri: ' [arany v2]');
    extra: további (név, refs, cél) összevetések csak a 'hatas' sorokba (pl. F8V3 − F3V3)."""
    osszevetesek = (('F3V3 − F3V2', [C2], C3), ('F3V3 − F3V2B', [C2B], C3),
                    ('F3V3 − átlag(F3V2, F3V2B)', [C2, C2B], C3), ('F3V2B − F3V2 (ingadozás)', [C2], C2B)) + tuple(extra)
    adatok = {}
    for nev, refs, cel in osszevetesek:
        adatok[nev] = delta_adatok(adat, refs, cel, n_boot)
        for r, d in adatok[nev].items():
            for mero, (ref, cl, dl, lo, hi, ab, n) in d.items():
                sorok.add('hatas', nev + utotag, r, mero, '%.4f|%.4f|%.4f' % (ref, cl, dl), '%.4f|%.4f|%.4f' % (lo, hi, ab),
                          'ref|cél|Δ ; 90%%-os intervallum alsó|felső|a |Δ| 95. percentilise; n=%d' % n)
    hat = adatok['F3V3 − átlag(F3V2, F3V2B)']
    ing = adatok['F3V2B − F3V2 (ingadozás)']
    for r in hat:
        for mero, (ref, cl, dl, lo, hi, ab, n) in hat[r].items():
            fl = abs(ing[r][mero][2]) if r in ing else float('nan')
            kivul = abs(dl) > fl and (lo > 0 or hi < 0)
            sorok.add('hatas_osszevetes', 'F3V3 vs v2 átlag' + utotag, r, mero, '%.4f|%.4f|%.4f|%.4f' % (ref, cl, dl, fl),
                      '%.4f|%.4f' % (lo, hi), '%s; n=%d; ref = a két v2-futás átlaga, cél = F3V3, Δ, |F3V2B − F3V2| (ingadozás); '
                      '90%% intervallum alsó|felső' % ('kívül az ingadozáson' if kivul else 'az ingadozáson belül / a 0-t tartalmazza', n))


# ---------------------------------------------------------------------------
# minősítés (csak a Sonnet+C pár)
# ---------------------------------------------------------------------------

def koltseg_felso(ut=None):
    """{osszeallitas: (ertek, also90, felso90)} a koltseg_vetites_p3c.tsv 'vetites'/Összes soraiból, ha van."""
    ut = ut or KOLTSEG_UT
    if not os.path.exists(ut):
        return {}
    ki = {}
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').split('\t') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0]
    for s in sorok[1:]:
        r = dict(zip(fej, s))
        if r['szakasz'] == 'vetites' and r['reteg'] == 'Összes':
            ki[r['osszeallitas']] = (float(r['ertek']), float(r['also90']), float(r['felso90']))
    return ki


def _arany(sorok, oss, ret, mero):
    for s in sorok.lista:
        if s[0] == 'feltetelek' and s[1] == oss and s[2] == ret and s[3] == mero:
            return (int(s[4]), int(s[5])) if s[5] not in ('', '0') else None
    return None


def minosit(sorok, kf, oss=PAR):
    """A Sonnet+C pár minősítése az öt rögzített feltétellel (a meres_p3b.minosit logikája)."""
    feltetel = {}
    mp = [_arany(sorok, oss, r, 'magas_pontossag') for r in meres.RETEGEK]
    # F21.82 (PD19 (1)): a 0/0 magas-linkű réteg az (1)-ben „nem mérhető” (nem „nem teljesül”); ha egy mérhető réteg
    # 98% alatt van, az (1) nem teljesül; ha minden mérhető réteg teljesül, de van 0/0 réteg: nem mérhető
    nm_retegek = [r for r, x in zip(meres.RETEGEK, mp) if not x]
    if any(x and x[0] / x[1] < 0.98 for x in mp):
        feltetel['1'] = False
    elif nm_retegek:
        feltetel['1'] = 'nm'
    else:
        feltetel['1'] = True
    lf = _arany(sorok, oss, meres.OSSZES, 'lefedettseg')
    feltetel['2'] = bool(lf) and lf[0] / lf[1] >= 0.95
    r0 = _arany(sorok, oss, meres.OSSZES, 'regi_arany_kizaras_nelkul')
    rk = _arany(sorok, oss, meres.OSSZES, 'regi_arany_kizarassal_tajekoztato')
    feltetel['3'] = bool(r0) and r0[0] / r0[1] >= 0.95
    feltetel['3_tajekoztato'] = bool(rk) and rk[0] / rk[1] >= 0.95
    feltetel['4'] = (kf[oss][2] <= 60.0) if oss in kf else None
    al = _arany(sorok, oss, meres.OSSZES, 'alacsony_arany [200 vers]')
    feltetel['5'] = bool(al) and al[0] / al[1] <= 0.10
    for k, v in feltetel.items():
        sorok.add('minosites', oss, meres.OSSZES, 'feltetel_%s' % k, {True: 'teljesül', False: 'nem teljesül', None: 'nem mért',
                                                                     'nm': 'nem mérhető'}[v],
                  '', ('0/0 magas link: %s (PD19 (1))' % ', '.join(nm_retegek)) if v == 'nm' else '')
    for cimke, kulcsok in (('minosites (kizárás nélküli régi arannyal)', ('1', '2', '3', '4', '5')),
                           ('minosites (tájékoztató: 1Móz 6:17 kizárva)', ('1', '2', '3_tajekoztato', '4', '5'))):
        bukott = [k for k in kulcsok if feltetel[k] is False]
        nem_mert = [k for k in kulcsok if feltetel[k] is None]
        nem_merheto = [k for k in kulcsok if feltetel[k] == 'nm']
        if bukott:
            e = 'nem felel meg'
        elif nem_mert or nem_merheto:
            e = 'nem minősíthető (nem mért feltétel)' if nem_mert else 'nem minősíthető (nem mérhető feltétel)'
        else:
            e = 'megfelel'
        sorok.add('minosites', oss, meres.OSSZES, cimke, e, '',
                  'bukott feltétel: %s; nem mért: %s' % (', '.join(bukott) or '—', ', '.join(nem_mert) or '—')
                  + ('; nem mérhető: %s' % ', '.join(nem_merheto) if nem_merheto else ''))
    for r in meres.RETEGEK:
        m = _arany(sorok, oss, r, 'magas_pontossag')
        l = _arany(sorok, oss, r, 'lefedettseg')
        a = _arany(sorok, oss, r, 'alacsony_arany [200 vers]')
        g = _arany(sorok, oss, r, 'regi_arany_kizaras_nelkul')
        reszek = {'1': (m[0] / m[1] >= 0.98) if m else None, '2': bool(l) and l[0] / l[1] >= 0.95,
                  '3': (g[0] / g[1] >= 0.95) if g else None, '5': bool(a) and a[0] / a[1] <= 0.10}
        bukott = [k for k, v in reszek.items() if v is False]
        sorok.add('minosites_reteg', oss, r, 'reteg_feltetelek (1,2,3,5; a 4. összesen)',
                  'teljesül' if not bukott else 'nem teljesül', '',
                  'bukott: %s; (3) %s%s' % (', '.join(bukott) or '—', 'n.é. (nincs régi arany a rétegben)' if reszek['3'] is None else 'mért',
                                           '; (1) nem mérhető (0/0 magas link, PD19 (1))' if reszek['1'] is None else ''))


# ---------------------------------------------------------------------------
# --csak-c: a C (F3V3) egyedül, a v2-es C-futások két aranyon, F8V3 tájékoztatásul
# ---------------------------------------------------------------------------

def arany_valtozat(adat, jsonl=None, sha=None, verzio='v2'):
    """(adat-másolat egy másik befagyasztott arannyal, info). Alap: az arany v2 (tokenek.ARANY_V2);
    hash-ellenőrzés, eltérésnél SystemExit. A futásadatok közösek (sekély másolat, csak olvasás)."""
    jsonl = jsonl or tokenek.ARANY_V2
    sha = sha or tokenek.ARANY_V2_SHA
    h = tokenek.hash_hiba(jsonl, sha, 'arany %s' % verzio)
    if h:
        raise SystemExit('HIBA: %s' % h)
    a2 = copy.copy(adat)
    a2.arany = {o['vers']: o for o in meres._jsonl(jsonl)}
    return a2, {'jsonl': jsonl, 'sha_fajl': sha, 'verzio': verzio, 'sha256': tokenek.sha256_lf(jsonl),
                'aranyversek': len(a2.arany)}


def nincs_sonnet(sorok):
    """A Sonnet és a Sonnet+C pár sorai a Sonnet-adat nélkül."""
    for oss in (NEVEK[SONNET], PAR):
        for ret in RETEGEK:
            sorok.add('nincs_adat', oss, ret, 'minden_mero', NINCS_SONNET, '',
                      'a Sonnet-adat megérkezése után a teljes mérés ugyanezzel a szkripttel fut (--csak-c nélkül): '
                      'f21p/meres_p3c_eredmeny.tsv, naplok/F21P_meres_p3c.md')


def kuszob_c(sorok, kf, oss=None):
    """Az öt rögzített feltétel küszöb-viszonya a C-re (egymodelles: PD6, nincs minősítés)."""
    oss = oss or NEVEK[C3]

    def viszony(x, kuszob, nagyobb):
        jo = (x >= kuszob) if nagyobb else (x <= kuszob)
        return 'a küszöbön belül' if jo else 'a küszöbön kívül'
    for ret in RETEGEK:
        p = _arany(sorok, oss, ret, 'pontossag_osszes (tajekoztato, PD6)')
        sorok.add('kuszob', oss, ret, 'f1_magas_pontossag_98', 'n.é.', '',
                  'egymodelles (PD6): a magas szint nem értelmezhető; az összpontosság mért (nem a feltétel mérőszáma): %s'
                  % (_pct(*p) if p else '—'))
        lf = _arany(sorok, oss, ret, 'lefedettseg')
        if lf:
            sorok.add('kuszob', oss, ret, 'f2_lefedettseg_95', lf[0], lf[1],
                      'küszöb ≥ 95%%: %s (küszöb-viszony, nem minősítés; PD6)' % viszony(lf[0] / lf[1], 0.95, True))
        for mero, cimke in (('regi_arany_kizaras_nelkul', 'f3_regi_arany_95 (MÉRT, kizárás nélkül)'),
                            ('regi_arany_kizarassal_tajekoztato', 'f3_regi_arany_95 (TÁJÉKOZTATÓ, 1Móz 6:17 nélkül)')):
            g = _arany(sorok, oss, ret, mero)
            if g:
                sorok.add('kuszob', oss, ret, cimke, g[0], g[1],
                          'küszöb ≥ 95%%: %s (küszöb-viszony, nem minősítés; PD6)%s' % (
                              viszony(g[0] / g[1], 0.95, True), '' if 'MÉRT' in cimke else '; a küszöb szempontjából nem számít (PD12)'))
            else:
                sorok.add('kuszob', oss, ret, cimke, 'n.é.', '', 'nincs régi arany hármas a rétegben')
        sorok.add('kuszob', oss, ret, 'f5_alacsony_arany_10', 'n.é.', '', 'egymodelles (PD6): az alacsony szint nem értelmezhető')
    if oss in kf:
        e, lo, hi = kf[oss]
        sorok.add('kuszob', oss, meres.OSSZES, 'f4_koltseg_felso90_60', '%.2f' % hi, '',
                  'vetített teljes költség %.2f USD [90%%: %.2f–%.2f]; küszöb: a felső szél ≤ 60 USD: %s (küszöb-viszony, nem minősítés; PD6)'
                  % (e, lo, hi, viszony(hi, 60.0, False)))
    else:
        sorok.add('kuszob', oss, meres.OSSZES, 'f4_koltseg_felso90_60', 'nem mért', '', 'a költségvetítés (koltseg_vetit_p3c.py --csak-c) kimenete hiányzik')
    sorok.add('kuszob', oss, meres.OSSZES, 'minosites', 'nincs (egymodelles összeállítás, PD6)', '',
              'a teljes futásra rétegenként sem mehet; csak mért számok és a küszöbhöz viszonyítás')


def _pl(adat, f, ret):
    """(találat, modell-link, arany-link, vers) a kapun átment aranyverseken."""
    vs = [ig for ig in adat.versek if ig in adat.arany and _ret(adat, ig, ret) and adat.ok(f, ig)]
    t = sum(len(adat.linkek(f, ig) & adat.arany_linkek(ig)) for ig in vs)
    c = sum(len(adat.linkek(f, ig)) for ig in vs)
    g = sum(len(adat.arany_linkek(ig)) for ig in vs)
    return t, c, g, len(vs)


def arany_hatas(adat3, adat2, sorok, futasok):
    """Az arany v2 → v3 hatás azonos futás-kimeneten (determinisztikus): pontosság és lefedettség."""
    for f in futasok:
        for ret in RETEGEK:
            t2, c2, g2, n2 = _pl(adat2, f, ret)
            t3, c3, g3, n3 = _pl(adat3, f, ret)
            for mero, (a2, b2, a3, b3) in (('pontossag', (t2, c2, t3, c3)), ('lefedettseg', (t2, g2, t3, g3))):
                v2 = a2 / b2 if b2 else 0.0
                v3 = a3 / b3 if b3 else 0.0
                sorok.add('arany_hatas', NEVEK[f], ret, mero, '%.4f|%.4f|%.4f' % (v2, v3, v3 - v2), '%d/%d|%d/%d' % (a2, b2, a3, b3),
                          'arany v2|arany v3|Δ (v3 − v2), azonos futás-kimeneten; n=%d aranyvers (kapun átment)' % n3)
    # a két arany eltérő linkjei (a 60 aranyversen)
    elt = [(ig, l) for ig in adat3.versek if ig in adat3.arany and ig in adat2.arany
           for l in sorted(adat3.arany_linkek(ig) ^ adat2.arany_linkek(ig))]
    sorok.add('arany_hatas', 'arany v2 → v3', meres.OSSZES, 'eltero_linkek', len(elt), '',
              '; '.join('%s %s %s' % (ig, l, 'csak v3' if l in adat3.arany_linkek(ig) else 'csak v2') for ig, l in elt))


def kjv_tajekoztato(adat, sorok):
    """Az F8V3 és az F3V3 KJV-sorral bíró versei rétegenként (a 200 verses mintán), és a PD17-jelölés."""
    for ret in RETEGEK:
        vs = [ig for ig in adat.versek if _ret(adat, ig, ret)]
        n8 = sum(1 for ig in vs if tokenek.kjv_tamapont_teljes(ig))
        n3 = sum(1 for ig in vs if tokenek.kjv_tamapont(ig))
        sorok.add('kjv', NEVEK[F8], ret, 'versek_kjv_sorral (teljes tábla)', n8, len(vs), 'tokenek.kjv_tamapont_teljes')
        sorok.add('kjv', NEVEK[C3], ret, 'versek_kjv_sorral (régi tábla)', n3, len(vs), 'tokenek.kjv_tamapont')
    sorok.add('kjv', NEVEK[F8], 'R4', 'jeloles', 'KJV nélkül, nem mérhető', '',
              'PD17 (2): a Károli ↔ KJV megfeleltetés az ÚSZ-t nem fedi; az R4-en az F8V3 és az F3V3 bemenete azonos')
    sorok.add('kjv', NEVEK[F8], 'R2', 'jeloles', 'gyenge (zsoltár-eltolódás)', '',
              'PD17 (1): a zsoltárfeliratok miatti versmegfeleltetési eltolódás (N-F21); a KJV-sor valószínűleg rossz versről jön; naplok/F21P_kjv_meres.md')
    sorok.add('kjv', NEVEK[F8], meres.OSSZES, 'jeloles', 'nem igazolt, a javított táblával újramérhető', '',
              'PD17 (3): a KJV a promptban — a pilot döntése')


# ---------------------------------------------------------------------------
# F21.76: az első próbás kapuhiba kapupontonként és rétegenként; az R1-lefedettség jelölése
# ---------------------------------------------------------------------------

KAPUPONTOK_ALAP = ['1', '1-json', '2', '3', '4']     # mindig kiírt kapupontok (a többi csak, ha előfordul)
BESOROLAS_C_UT = os.path.join(F21P, 'c_diff_p3c_besorolas.tsv')
KUSZOB_LEF = 0.95


def _rovid(h, n=100):
    h = ' '.join(h.split())
    return h if len(h) <= n else h[:n - 1] + '…'


def kapupont_versek(adat, f):
    """Az első próbán kapuhibás versek a minta sorrendjében: [(igehely, réteg, köteg, [kapupontok],
    [első-próbás hibaüzenetek], végleg átment-e, [végleges kapupontok])]. Módszer: a köteg nyers[0]
    válaszának újraellenőrzése a teljes kapun (a meres.hibatipusok módszere, kapupont: meres._tipusok)."""
    ki = {}
    for sor in adat.kotegsorok[f]:
        ig_lista = sor['igehelyek']
        r1 = meres.kapu.valasz_ellenoriz(sor['nyers'][0], ig_lista)
        for ig in ig_lista:
            if r1[ig]['ok']:
                continue
            v = sor['versek'][ig]
            vok = v['allapot'] == 'ok'
            ki[ig] = (ig, adat.reteg[ig], sor.get('koteg', '?'), sorted(meres._tipusok(r1[ig]['hibak'])), list(r1[ig]['hibak']),
                      vok, [] if vok else sorted(meres._tipusok(v['hibak'])))
    return [ki[ig] for ig in adat.versek if ig in ki]


def kapupont_reteg(adat, sorok, futasok=FUTASOK_C):
    """Az első próbás kapuhibás versek kapupontonként és rétegenként, a versek listájával; keresztellenőrzés
    a kapuhiba-szakasz rétegenkénti első-próbás számaival, a jsonl probalkozas=2 verseivel és a napló
    kapuhiba_db(probalkozas=1) összegével (a kapuhiba_futasok után hívandó)."""
    vers = {f: kapupont_versek(adat, f) for f in futasok}
    pontok = list(KAPUPONTOK_ALAP) + sorted({p for f in futasok for x in vers[f] for p in x[3]} - set(KAPUPONTOK_ALAP))
    for f in futasok:
        nev = NEVEK[f]
        for ret in RETEGEK:
            vs = [ig for ig in adat.versek if ig in adat.futas[f] and _ret(adat, ig, ret)]
            if not vs:
                continue
            xs = [x for x in vers[f] if _ret(adat, x[0], ret)]
            sorok.add('kapupont_reteg', nev, ret, 'hibas_versek_elso', len(xs), len(vs),
                      'az első próbán kapuhibás versek (bármely kapupont); kötegek: %d' % len({x[2] for x in xs}))
            for p in pontok:
                xp = [x for x in xs if p in x[3]]
                sorok.add('kapupont_reteg', nev, ret, 'kapupont_%s_elso' % p, len(xp), len(vs), 'kötegek: %d' % len({x[2] for x in xp}))
            sorok.add('kapupont_reteg', nev, ret, 'tobb_kapupontos_versek_elso', sum(1 for x in xs if len(x[3]) > 1), len(vs),
                      'egy vers több kapupontnál is hibás: a kapupont-sorok összege ennyivel több a hibás versekénél')
        reteg_sz = {s[2]: int(s[4]) for s in sorok.lista if s[0] == 'kapuhiba' and s[1] == nev and s[3] == 'elso_probara'}
        reteg_egy = all(n == sum(1 for x in vers[f] if _ret(adat, x[0], r)) for r, n in reteg_sz.items()) and bool(reteg_sz)
        _, _, elso_h = meres.hibatipusok(adat, f)
        p2 = {ig for ig, r in adat.futas[f].items() if r['probalkozas'] == 2}
        naplo_p1 = sum(int(r['kapuhiba_db']) for r in adat.naplo if r['futas'] == f and r['probalkozas'] == '1')
        hv = {x[0] for x in vers[f]}
        egy = reteg_egy and hv == elso_h == p2 and len(hv) == naplo_p1
        sorok.add('kapupont_kereszt', nev, meres.OSSZES, 'kapupont_versek_elso', len(hv), naplo_p1,
                  'a kapupont-bontás hibás versei (%d) = a kapuhiba-szakasz rétegenkénti első-próbás számai (%s) = jsonl '
                  'probalkozas=2 versek (%d) = napló kapuhiba_db(probalkozas=1) összeg (%d): %s' % (
                      len(hv), ', '.join('%s: %d' % (r, reteg_sz[r]) for r in RETEGEK if r in reteg_sz), len(p2), naplo_p1,
                      'EGYEZIK' if egy else 'ELTÉR'))
        for x in vers[f]:
            uzen = ' / '.join(_rovid(h) for h in x[4][:2]) + (' (+%d további)' % (len(x[4]) - 2) if len(x[4]) > 2 else '')
            sorok.add('kapupont_vers', nev, x[1], x[0], '+'.join(x[3]), 'köteg %s' % x[2],
                      'első próba: %s | végleg: %s%s' % (uzen, 'átment (2. próba)' if x[5] else 'kapuhibás (kapupont %s)' % '+'.join(x[6]),
                                                       ' | aranyvers' if x[0] in adat.arany else ''))


def besorolas_beolvas(ut):
    """A kézi besorolás-fájl (c_diff_p3c_besorolas.tsv) sorai dict-ként (split('\\t'); a '#' sorok kimaradnak)."""
    with open(ut, encoding='utf-8') as f:
        s = [x.rstrip('\n').rstrip('\r') for x in f if x.strip() and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def lefedettseg_jeloles(adat, sorok, besorolas_ut, kuszob=KUSZOB_LEF):
    """F21.76 (1): a küszöbön kívüli F3V3-lefedettség jelölése rétegenként (nincs további teendő): a hiányzó
    linkek közül a K4-eltérés (a) száma a kézi besorolásból (Opus-besorolás, nem mérés)."""
    if not besorolas_ut or not os.path.exists(besorolas_ut):
        return
    bs = besorolas_beolvas(besorolas_ut)
    for ret in meres.RETEGEK:
        t, _, g, _ = _pl(adat, C3, ret)
        if not g or t / g >= kuszob:
            continue
        hi = [r for r in bs if r['futas'] == C3 and r['reteg'] == ret and r['statusz'] == 'elteres' and r['irany'] == 'hianyzo']
        k4a = [r for r in hi if r['osztaly'] == 'a' and r['konvencio_vagy_jegyzetpont'].startswith('K4')]
        sorok.add('jeloles', NEVEK[C3], ret, 'lefedettseg_kuszobon_kivul', t, g,
                  'az %s lefedettsége a %s%%-os küszöbön kívül (%s%%); a hiányzó %d link közül %d K4-eltérés (a)'
                  ' — a K4-szám Opus-besorolás, nem mérés (f21p/c_diff_p3c_besorolas.tsv); a besorolás hiányzó eltérés-sorai: %d (%s)'
                  % (ret, ('%g' % (100.0 * kuszob)).replace('.', ','), ('%.1f' % (100.0 * t / g)).replace('.', ','), g - t, len(k4a), len(hi), 'EGYEZIK' if len(hi) == g - t else 'ELTÉR'))


def szamol_c(forras_dir=None, arany_ut=None, arany_sha=None, koltseg_ut=None, n_boot=N_BOOT, arany_v2_ut=None, arany_v2_sha=None,
             besorolas_ut=None):
    """A csak-C P4-számítás (kiírás nélkül). Visszaad: (adat, info, sorok, kf, info_v2, futasok).
    besorolas_ut: a kézi besorolás (az R1-jelöléshez; alap: a repó fájlja, ha a forras_dir az alap)."""
    futasok = futasok_c(forras_dir)
    adat, info = betolt(forras_dir, arany_ut, arany_sha, futasok)
    adat2, info2 = arany_valtozat(adat, arany_v2_ut, arany_v2_sha)
    sorok = Sorok()
    for f in futasok:
        meres_p3b.egymodell(adat, sorok, NEVEK[f], f)
    for f in FUTASOK_C:
        meres_p3b.egymodell(adat2, sorok, NEVEK[f] + V2_CIMKE, f)
    nincs_sonnet(sorok)
    kf = koltseg_felso(koltseg_ut or KOLTSEG_C_UT)
    kuszob_c(sorok, kf)
    arany_hatas(adat, adat2, sorok, FUTASOK_C)
    extra = (('F8V3 − F3V3 (KJV, tájékoztató)', [C3], F8),) if F8 in futasok else ()
    prompt_hatas(adat, sorok, n_boot, extra=extra)
    prompt_hatas(adat2, sorok, n_boot, utotag=' [arany v2]')
    kapuhiba_futasok(adat, sorok, futasok)
    for f in futasok:
        _, _, elso_h = meres.hibatipusok(adat, f)
        el = [ig for ig in adat.versek if ig in elso_h]
        vg = [ig for ig in adat.versek if ig in adat.futas[f] and not adat.ok(f, ig)]
        sorok.add('kapuhiba_versek', NEVEK[f], meres.OSSZES, 'elso_probara', len(el), '', ', '.join(el) or '—')
        sorok.add('kapuhiba_versek', NEVEK[f], meres.OSSZES, 'vegleg', len(vg), '',
                  ', '.join('%s (%s%s)' % (ig, adat.reteg[ig], ', aranyvers' if ig in adat.arany else '') for ig in vg) or '—')
    koltseg_futasok(adat, sorok, futasok)
    mentett_ellenorzes(sorok, forras_dir or F21P, futasok)
    if F8 in futasok:
        kjv_tajekoztato(adat, sorok)
    # F21.76: a régi sorok után (a meglévő sorok sorrendje változatlan)
    kapupont_reteg(adat, sorok, FUTASOK_C)
    lefedettseg_jeloles(adat, sorok, besorolas_ut if besorolas_ut is not None else (BESOROLAS_C_UT if forras_dir is None else None))
    return adat, info, sorok, kf, info2, futasok


def _tabla(sorok, szakasz, merok, osszeallitasok, retegek=None):
    out = ['| összeállítás | mérőszám | %s |' % ' | '.join(retegek or RETEGEK), '|---|---|' + '---|' * len(retegek or RETEGEK)]
    for o in osszeallitasok:
        for m in merok:
            cellak = []
            talalt = False
            for r in (retegek or RETEGEK):
                x = [s for s in sorok.lista if s[0] == szakasz and s[1] == o and s[2] == r and s[3] == m]
                if x:
                    talalt = True
                    cellak.append(_pct(x[0][4], x[0][5]) if x[0][5] != '' else x[0][4])
                else:
                    cellak.append('—')
            if talalt:
                out.append('| %s | %s | %s |' % (o, m, ' | '.join(cellak)))
    return out + ['']


def fejlec_c(info, info2, futasok, ts, bes=False):
    return ('GENERÁLT: eszkozok/karoli_strong/meres_p3c.py --csak-c | scope=P4 a regressziós mérésre, a C (F3V3, prompt_v3) EGYEDÜL '
            '(a SONNETV3 nem futott: a Sonnet és a Sonnet+C pár nincs adat); a v2-es C-futások (F3V2, F3V2B) és az F3V3 az arany v3-ra '
            'és az arany v2-re is; %s200 verses minta; arany %s (%d vers, sha256 %s) és arany %s (%d vers, sha256 %s); az első próbás '
            'kapuhiba kapupontonként és rétegenként (F3V2, F3V2B, F3V3; F21.76) | '
            'forras=f21p/valaszok/{%s}.jsonl, %s és %s (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, '
            'konkordancia/Karoli_Strong_kivonat.tsv, f21p/futasnaplo.tsv, f21p/koltseg_vetites_p3c_c.tsv%s%s | ts=%s (a generálás '
            'ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos' % (
                'F8V3 (C KJV-támponttal) tájékoztatásul; ' if F8 in futasok else '', info['verzio'], info['aranyversek'],
                info['sha256'][:16], info2['verzio'], info2['aranyversek'], info2['sha256'][:16], ','.join(futasok),
                os.path.basename(info['jsonl']), os.path.basename(info2['jsonl']),
                ', konkordancia/KJV_Strongs_teljes.tsv, konkordancia/KJV_Strongs_*.tsv' if F8 in futasok else '',
                ', f21p/c_diff_p3c_besorolas.tsv (MANUAL; csak a lefedettség-jelölés K4-száma)' if bes else '', ts))


def _kapupont_md(sorok):
    """A j) szakasz: az első próbás kapuhiba kapupontonként és rétegenként (F21.76); csak számok és versek."""
    fs = [NEVEK[f] for f in (C2, C2B, C3)]
    kr = {(s[1], s[2], s[3]): s for s in sorok.lista if s[0] == 'kapupont_reteg'}
    if not kr:
        return []
    merok = []
    for s in sorok.lista:
        if s[0] == 'kapupont_reteg' and s[3] not in merok:
            merok.append(s[3])

    def cella(o, r, m):
        x = kr.get((o, r, m))
        if not x:
            return '—'
        k = x[6].split('kötegek: ')[-1] if 'kötegek: ' in x[6] else ''
        return '%s/%s%s' % (x[4], x[5], (' (%s köteg)' % k) if k and x[4] != '0' else '')

    def d(a, b, r, m):
        xa, xb = kr.get((a, r, m)), kr.get((b, r, m))
        return '%+d' % (int(xa[4]) - int(xb[4])) if xa and xb else '—'
    ki = ['', '## j) Az első próbás kapuhiba kapupontonként és rétegenként (F3V2, F3V2B: prompt_v2; F3V3: prompt_v3)', '',
          'Módszer: minden köteg első nyers válaszának (nyers[0]) újraellenőrzése a teljes kapun, a kapupont a hibaüzenet sorszámából '
          '(meres._tipusok: 1, 1-json = nem érvényes JSON, 1-hianyzo_vers, 2, 3, 4, 5); keresztellenőrzés a kapuhiba-szakasz '
          'rétegenkénti első-próbás számaival, a jsonl probalkozas=2 verseivel és a napló kapuhiba_db(probalkozas=1) összegével. '
          'Cella: hibás versek / a réteg versei a 200-ból (az érintett kötegek száma); egy vers több kapupontnál is hibás lehet. '
          'Δ = verszám-különbség.', '',
          '| réteg | kapupont | %s | %s | %s | F3V3 − F3V2 | F3V3 − F3V2B |' % tuple(fs), '|---|---|---|---|---|---|---|']
    for r in RETEGEK:
        for m in merok:
            ki.append('| %s | %s | %s | %s | %s | %s | %s |' % (r, m, cella(fs[0], r, m), cella(fs[1], r, m), cella(fs[2], r, m),
                                                           d(fs[2], fs[0], r, m), d(fs[2], fs[1], r, m)))
    ki += ['', '| futás | keresztellenőrzés (kapupont-bontás) |', '|---|---|']
    for s in sorok.lista:
        if s[0] == 'kapupont_kereszt':
            ki.append('| %s | %s |' % (s[1], s[6]))
    vers = [s for s in sorok.lista if s[0] == 'kapupont_vers']
    ki += ['', '### Az R3: F3V3, F3V2, F3V2B kapupontonként, a versekkel', '',
           '| kapupont | %s | %s | %s |' % tuple(fs), '|---|---|---|---|']
    pontok = []
    for m in merok:
        if m.startswith('kapupont_') and m.endswith('_elso'):
            pontok.append(m[len('kapupont_'):-len('_elso')])
    for p in pontok:
        cel = []
        for o in fs:
            vs = [s for s in vers if s[1] == o and s[2] == 'R3' and p in s[4].split('+')]
            cel.append('%d: %s' % (len(vs), ', '.join(s[3] for s in vs) or '—'))
        ki.append('| %s | %s |' % (p, ' | '.join(cel)))
    ki += ['', '### Minden első próbán kapuhibás vers (futásonként, a minta sorrendjében)', '',
           '| futás | réteg | vers | kapupont | köteg | első próba: hibaüzenet (röviden) \\| végleg |', '|---|---|---|---|---|---|']
    for o in fs:
        for s in vers:
            if s[1] == o:
                ki.append('| %s | %s | %s | %s | %s | %s |' % (s[1], s[2], s[3], s[4], s[5], s[6].replace('|', '\\|')))
    return ki


def _hatas_md(sorok, utotag):
    ki = ['| réteg | mérőszám | v2 átlag | F3V3 | Δ | Δ 90% | \\|F3V2B − F3V2\\| | jelölés | n |', '|---|---|---|---|---|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'hatas_osszevetes' and s[1] == 'F3V3 vs v2 átlag' + utotag:
            ref, cl, dl, fl = (float(v) for v in s[4].split('|'))
            lo, hi = (float(v) for v in s[5].split('|'))
            jel, _, rest = s[6].partition(';')
            ki.append('| %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp | %s | %s |' % (
                s[2], s[3], 100 * ref, 100 * cl, 100 * dl, 100 * lo, 100 * hi, 100 * fl, jel, rest.split('n=')[1].split(';')[0]))
    return ki + ['']


def kiir_c(sorok, info, info2, futasok, ts, eredmeny_ut, jelentes_ut, kf):
    fej = fejlec_c(info, info2, futasok, ts, any(s[0] == 'jeloles' for s in sorok.lista))
    with open(eredmeny_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# ' + fej + '\n')
        f.write('\t'.join(['szakasz', 'osszeallitas', 'reteg', 'mero', 'szamlalo', 'nevezo', 'megjegyzes']) + '\n')
        for s in sorok.lista:
            assert all('\t' not in x for x in s)
            f.write('\t'.join(s) + '\n')
    c3, c2, c2b = NEVEK[C3], NEVEK[C2], NEVEK[C2B]
    ki = ['# F21P_meres_p3c_c.md — P4 a regressziós mérésre: a C (F3V3) egyedül, a v2-es C-futásokkal (a Sonnet nélkül)', '',
          '<!-- %s -->' % fej, '',
          'Kizárólag szkriptkimenet (meres_p3c.py --csak-c). A SONNETV3 még nem futott: a Sonnet egyedül és a Sonnet + C pár sorai '
          '**%s**; a teljes P4 a Sonnet-adat megérkezése után ugyanezzel a szkripttel fut (--csak-c nélkül, az eredeti '
          'f21p/meres_p3c_eredmeny.tsv és naplok/F21P_meres_p3c.md néven). A C egymodelles összeállítás: PD6 szerint **nincs '
          'minősítése** (nem „megfelelt / nem felel meg”), csak mért számok és a küszöbhöz viszonyítás; az (1) és az (5) feltétel '
          'n.é. A futások beállítása: a C `kotelezo_effort=minimal` (gondolkodással), temperature 0; az F3V2/F3V2B a prompt_v2-vel, '
          'az F3V3 és az F8V3 a prompt_v3-mal. Cellaforma: érték (számláló/nevező). A mérés az arany **%s** változatára megy '
          '(%d vers, sha256 ellenőrizve); a v2-es összevetéshez az arany **%s** is (%d vers, sha256 ellenőrizve).'
          % (NINCS_SONNET, info['verzio'], info['aranyversek'], info2['verzio'], info2['aranyversek']), '']
    ki += ['## a) A C (F3V3) egyedül: az öt rögzített feltétel rétegenként (arany %s)' % info['verzio'], '']
    ki += _tabla(sorok, 'feltetelek', ['arany_versek_kapun_atment', 'pontossag_osszes (tajekoztato, PD6)', 'lefedettseg',
                                       'regi_arany_kizaras_nelkul', 'regi_arany_kizarassal_tajekoztato', 'magas_pontossag',
                                       'alacsony_arany'], [c3])
    ki += ['### Küszöb-viszony (PD6: nem minősítés)', '', '| feltétel | réteg | érték | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'kuszob':
            ki.append('| %s | %s | %s | %s |' % (s[3], s[2], _pct(s[4], s[5]) if s[5] != '' else s[4], s[6]))
    jel = [s for s in sorok.lista if s[0] == 'jeloles']
    if jel:
        ki += ['', 'Jelölés (F21.76; nincs további teendő):', '']
        ki += ['- %s.' % s[6].split(' — ')[0] + ' (%s)' % s[6].split(' — ', 1)[1] for s in jel]
    ki += ['', '## b) A Sonnet egyedül és a Sonnet + C pár', '', '| összeállítás | állapot |', '|---|---|',
           '| %s | %s |' % (NEVEK[SONNET], NINCS_SONNET), '| %s | %s |' % (PAR, NINCS_SONNET), '']
    oszlop = [c2, c2b, c3] + ([NEVEK[F8]] if F8 in futasok else [])
    ki += ['## c) A C-futások egymás mellett, arany %s (F3V2, F3V2B: prompt_v2; F3V3: prompt_v3%s)' % (
        info['verzio'], '; F8V3: prompt_v3 + KJV-támpont, tájékoztató' if F8 in futasok else ''), '']
    ki += _tabla(sorok, 'feltetelek', ['arany_versek_kapun_atment', 'pontossag_osszes (tajekoztato, PD6)', 'lefedettseg',
                                       'regi_arany_kizaras_nelkul', 'regi_arany_kizarassal_tajekoztato'], oszlop)
    if F8 in futasok:
        ki += ['Az F8V3 oszlop tájékoztató (PD17): az **R4 „KJV nélkül, nem mérhető”** (a Károli ↔ KJV megfeleltetés az ÚSZ-t nem fedi, '
               'az R4-en a bemenet azonos az F3V3-éval); az R2 a zsoltár-eltolódás miatt gyenge (N-F21); a KJV a promptban: „nem '
               'igazolt, a javított táblával újramérhető”. Részletek: naplok/F21P_kjv_meres.md.', '']
        ki += _tabla(sorok, 'kjv', ['versek_kjv_sorral (teljes tábla)', 'versek_kjv_sorral (régi tábla)', 'jeloles'], [NEVEK[F8], c3])
    ki += ['## d) Ugyanez az arany %s-re (a v2-es futások saját aranya; az arany v2 → v3 hatás elválasztásához)' % info2['verzio'], '']
    ki += _tabla(sorok, 'feltetelek', ['arany_versek_kapun_atment', 'pontossag_osszes (tajekoztato, PD6)', 'lefedettseg'],
                 [c2 + V2_CIMKE, c2b + V2_CIMKE, c3 + V2_CIMKE])
    ki += ['### Az arany v2 → v3 hatás azonos futás-kimeneten (determinisztikus)', '',
           '| futás | réteg | mérőszám | arany v2 | arany v3 | Δ (v3 − v2) | számláló/nevező (v2 \\| v3) |', '|---|---|---|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'arany_hatas' and s[3] in ('pontossag', 'lefedettseg'):
            v2, v3, d = (float(v) for v in s[4].split('|'))
            ki.append('| %s | %s | %s | %.2f%% | %.2f%% | %+.2f pp | %s |' % (s[1], s[2], s[3], 100 * v2, 100 * v3, 100 * d, s[5].replace('|', ' \\| ')))
    for s in sorok.lista:
        if s[0] == 'arany_hatas' and s[3] == 'eltero_linkek':
            ki += ['', 'A két arany eltérő linkjei: %s — %s' % (s[4], s[6])]
    ki += ['', '## e) Kapuhiba első próbára és végleg; hibatípusok kapupont szerint (hibás versek a 200-ból)', '']
    ki += _tabla(sorok, 'kapuhiba', ['elso_probara', 'vegleg'], oszlop)
    merok_t = []
    for s in sorok.lista:
        if s[0] == 'kapuhiba_tipus' and s[3] not in merok_t:
            merok_t.append(s[3])
    ki += ['| futás | kapupont | hibás versek (n a 200) |', '|---|---|---|']
    for o in oszlop:
        for m in merok_t:
            x = [s for s in sorok.lista if s[0] == 'kapuhiba_tipus' and s[1] == o and s[3] == m]
            if x:
                ki.append('| %s | %s | %s/%s |' % (o, m, x[0][4], x[0][5]))
    ki += ['', '| futás | keresztellenőrzés (első próbás hibás versek) |', '|---|---|']
    for s in sorok.lista:
        if s[0] == 'kapuhiba_kereszt':
            ki.append('| %s | %s |' % (s[1], s[6]))
    ki += ['', '| futás | mentett válaszok újraellenőrzése (hibák) |', '|---|---|']
    for s in sorok.lista:
        if s[0] == 'mentett_ellenorzes':
            ki.append('| %s | %s — %s |' % (s[1], s[4], s[6]))
    ki += ['', '| futás | első próbára kapuhibás versek | véglegesen kapuhibás versek |', '|---|---|---|']
    for o in oszlop:
        x = {s[3]: s for s in sorok.lista if s[0] == 'kapuhiba_versek' and s[1] == o}
        if x:
            ki.append('| %s | %s: %s | %s: %s |' % (o, x['elso_probara'][4], x['elso_probara'][6], x['vegleg'][4], x['vegleg'][6]))
    ki += ['', '## f) Költség és beállítás futásonként (a futásnaplóból)', '', '| futás | mérőszám | érték | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'koltseg':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[3], s[4], s[6]))
    ki.append('')
    ki.append('(4) vetített költség, teljes Biblia (f21p/koltseg_vetites_p3c_c.tsv; 90%; a bootstrap egysége a köteg):')
    ki.append('')
    for o in oszlop:
        if o in kf:
            ki.append('- %s: %.2f USD [%.2f–%.2f]' % (o, *kf[o]))
    if not kf:
        ki.append('- (a f21p/koltseg_vetites_p3c_c.tsv még nincs meg: a (4) feltétel nem mért)')
    for betu, utotag, cim in (('g', '', 'arany %s' % info['verzio']), ('h', ' [arany v2]', 'arany %s' % info2['verzio'])):
        ki += ['', '## %s) A prompt_v2 → v3 hatás (F3V3 a két v2-futás átlagához képest), %s, és a futásközi ingadozás' % (betu, cim), '',
               'Δ = F3V3 − a v2-futások átlaga, azonos aranyon (tehát az arany változása nincs benne); a 90%%-os intervallum a versek '
               'bootstrapje (rétegenként rétegzett, %d újramintavétel, mag %d). Az ingadozás-becslés egyetlen futáspár '
               '(|F3V2B − F3V2|, azonos prompt). „kívül”: |Δ| > az ingadozás ÉS az intervallum nem tartalmazza a 0-t (leíró jelölés, '
               'nem próba).' % (N_BOOT, MAG), '']
        ki += _hatas_md(sorok, utotag)
    ki += ['## i) Páronkénti összevetések (a „[arany v2]” utótag nélkül az arany v3-ra; az F8V3 − F3V3 tájékoztató)', '',
           '| összevetés | réteg | mérőszám | ref | cél | Δ | Δ 90% | \\|Δ\\| 95. percentilis | n |', '|---|---|---|---|---|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'hatas':
            x, y, d = (float(v) for v in s[4].split('|'))
            lo, hi, ab = (float(v) for v in s[5].split('|'))
            ki.append('| %s | %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp | %s |' % (
                s[1], s[2], s[3], 100 * x, 100 * y, 100 * d, 100 * lo, 100 * hi, 100 * ab, s[6].split('n=')[-1]))
    if F8 in futasok:
        ki += ['', 'Az „F8V3 − F3V3 (KJV, tájékoztató)” sorok R4-e: KJV nélkül, nem mérhető (azonos bemenet, a különbség futásközi ingadozás).']
    ki += _kapupont_md(sorok)
    ki.append('')
    with open(jelentes_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def fut_c(forras_dir=None, arany_ut=None, arany_sha=None, eredmeny_ut=None, jelentes_ut=None, koltseg_ut=None, ts=None,
          n_boot=N_BOOT, arany_v2_ut=None, arany_v2_sha=None):
    adat, info, sorok, kf, info2, futasok = szamol_c(forras_dir, arany_ut, arany_sha, koltseg_ut, n_boot, arany_v2_ut, arany_v2_sha)
    kiir_c(sorok, info, info2, futasok, ts or tokenek.generalas_ts(), eredmeny_ut or EREDMENY_C_UT, jelentes_ut or JELENTES_C_UT, kf)
    print('kész (--csak-c): %d sor -> %s, %s (arany: %s; futások: %s)' % (
        len(sorok.lista), eredmeny_ut or EREDMENY_C_UT, jelentes_ut or JELENTES_C_UT, info['verzio'], ', '.join(futasok)))
    for s in sorok.lista:
        if s[0] == 'kuszob' and s[2] == meres.OSSZES:
            print('  %s | %s | %s' % (s[3], _pct(s[4], s[5]) if s[5] != '' else s[4], s[6][:110]))
    rossz = [s for s in sorok.lista if s[3] in ('keresztellenorzes_elso_probalkozas', 'kapupont_versek_elso', 'lefedettseg_kuszobon_kivul')
             and 'ELTÉR' in s[6]]
    if rossz:
        print('FIGYELEM: a kapuhiba keresztellenőrzése / a jelölés eltér: %s' % [(s[0], s[1]) for s in rossz], file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# kiírás
# ---------------------------------------------------------------------------

def _pct(sz, nev):
    try:
        sz, nev = float(sz), float(nev)
    except ValueError:
        return sz
    return '%.1f%% (%d/%d)' % (100 * sz / nev, sz, nev) if nev else '— (0/0)'


def fejlec(info, ts):
    return ('GENERÁLT: eszkozok/karoli_strong/meres_p3c.py | scope=P3c (prompt_v3): Sonnet egyedül (SONNETV3), C (F3V3) a v2-es '
            'két C-futással (F3V2, F3V2B), Sonnet+C pár (A=SONNETV3, B=F3V3, döntőbíró nélkül), a Sonnet gondolkodási kerete, '
            'length-lezárásai, végleges kapuhibái és a kapupont-bontás (F21.80), 200 verses minta, arany %s '
            '(%d vers, sha256 %s) | forras=f21p/valaszok/{SONNETV3,F3V3,F3V2,F3V2B}.jsonl, %s (sha256 ellenőrizve), '
            'f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/futasnaplo.tsv, '
            'f21p/koltseg_vetites_p3c.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
            'kézzel szerkeszteni tilos' % (info['verzio'], info['aranyversek'], info['sha256'][:16],
                                          os.path.basename(info['jsonl']), ts))


def kiir(sorok, info, ts, eredmeny_ut, jelentes_ut, kf):
    fej = fejlec(info, ts)
    with open(eredmeny_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# ' + fej + '\n')
        f.write('\t'.join(['szakasz', 'osszeallitas', 'reteg', 'mero', 'szamlalo', 'nevezo', 'megjegyzes']) + '\n')
        for s in sorok.lista:
            assert all('\t' not in x for x in s)
            f.write('\t'.join(s) + '\n')
    ki = ['# F21P_meres_p3c.md — P4 a regressziós mérésre (P3c): Sonnet, Sonnet+C, C (F3V3) a v2-es C-futásokkal', '',
          '<!-- %s -->' % fej, '',
          'Kizárólag szkriptkimenet. Az összeállítások: Sonnet egyedül (SONNETV3), C egyedül (F3V3), Sonnet+C pár (A = Sonnet, '
          'B = C F3V3-futása, mindkettő prompt_v3; A∩B = magas, döntőbíró nélkül; az egyik oldal kapuhibája: a vers minden '
          'linkje alacsony és beleszámít az alacsony arányba). Egymodelles összeállítás (Sonnet, C) nem minősíthető (PD6): az '
          'alacsony arány n.é. Az A/B/C/Sonnet beállítása eltérő (PD15: a C minimal, kötelező; a Sonnet minimális gondolkodási kerettel, '
          'temperature nélkül, nem determinisztikus; az A és a B kikapcsolva). '
          'Cellaforma: érték (számláló/nevező). A mérés az arany **%s** változatára megy (%d vers).' % (info['verzio'], info['aranyversek']), '']

    def tabla(szakasz, merok, osszeallitasok):
        out = ['| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |', '|---|---|---|---|---|---|---|']
        for o in osszeallitasok:
            for m in merok:
                cellak = []
                talalt = False
                for r in RETEGEK:
                    x = [s for s in sorok.lista if s[0] == szakasz and s[1] == o and s[2] == r and s[3] == m]
                    if x:
                        talalt = True
                        cellak.append(_pct(x[0][4], x[0][5]) if x[0][5] != '' else x[0][4])
                    else:
                        cellak.append('—')
                if talalt:
                    out.append('| %s | %s | %s |' % (o, m, ' | '.join(cellak)))
        return out + ['']

    oss_all = [NEVEK[SONNET], NEVEK[C3], PAR]
    ki += ['## a) Az öt feltétel összeállításonként és rétegenként', '']
    ki += tabla('feltetelek', ['arany_versek_kapun_atment', 'arany_versek', 'magas_pontossag',
                               'pontossag_osszes (tajekoztato, PD6)', 'pontossag_osszes (tajekoztato)', 'lefedettseg',
                               'regi_arany_kizaras_nelkul', 'regi_arany_kizarassal_tajekoztato', 'alacsony_arany',
                               'alacsony_arany [200 vers]', 'alacsony_arany [arany]'], oss_all)
    ki.append('(4) vetített költség, teljes Biblia (f21p/koltseg_vetites_p3c.tsv, 90%; a bootstrap egysége a köteg):')
    ki.append('')
    for o in oss_all:
        if o in kf:
            ki.append('- %s: %.2f USD [%.2f–%.2f]' % (o, *kf[o]))
    if not kf:
        ki.append('- (a f21p/koltseg_vetites_p3c.tsv még nincs meg: a (4) feltétel nem mért)')
    ki += ['', '## b) Minősítés (csak a Sonnet+C pár; az egymodelles összeállítás PD6 szerint nem minősíthető)', '',
           '| összeállítás | feltétel | eredmény | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'minosites':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[3], s[4], s[6]))
    ki += ['', '| összeállítás | réteg | rétegfeltételek (1, 2, 3, 5) | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'minosites_reteg':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[2], s[4], s[6]))
    ki += ['', '## c) A Sonnet+C pár bizonyossági szintjei és versosztályai', '']
    ki += tabla('szintek', ['kozepes_pontossag', 'alacsony_pontossag'] + ['eloszlas_%s [%s]' % (x, h) for h in ('200 vers', 'arany')
                                                                        for x in SZINTEK]
                + ['kimenet_nelkuli_versek [200 vers]', 'kimenet_nelkuli_versek [arany]'], [PAR])
    ki += tabla('par_versosztalyok', ['mindketto_atment_azonos_linkekkel', 'mindketto_atment_eltero_linkekkel', 'csak_Sonnet_atment',
                                      'csak_C_atment', 'egyik_sem_atment'], [PAR])
    ki += tabla('ab_egyezes', ['versek_mindketto_atment', 'link_egyezes (uniós arány)', 'azonos_linkhalmazu_versek'], [PAR])
    ki += ['## d) A C három futása egymás mellett (F3V2, F3V2B: prompt_v2; F3V3: prompt_v3) és a Sonnet', '']
    c_nevek = [NEVEK[f] for f in (C2, C2B, C3, SONNET)]
    ki += tabla('feltetelek', ['arany_versek_kapun_atment', 'pontossag_osszes (tajekoztato, PD6)', 'lefedettseg',
                               'regi_arany_kizaras_nelkul', 'regi_arany_kizarassal_tajekoztato'], c_nevek)
    ki += ['### Kapuhiba első próbára és végleg; hibatípusok kapupont szerint (hibás versek száma a 200-ból)', '']
    ki += tabla('kapuhiba', ['elso_probara', 'vegleg'], c_nevek)
    merok_t = []
    for s in sorok.lista:
        if s[0] == 'kapuhiba_tipus' and s[3] not in merok_t:
            merok_t.append(s[3])
    ki += ['| futás | kapupont | hibás versek (n a 200) |', '|---|---|---|']
    for o in c_nevek:
        for m in merok_t:
            x = [s for s in sorok.lista if s[0] == 'kapuhiba_tipus' and s[1] == o and s[3] == m]
            if x:
                ki.append('| %s | %s | %s/%s |' % (o, m, x[0][4], x[0][5]))
    ki += ['', '| futás | keresztellenőrzés (első próbás hibás versek) |', '|---|---|']
    for s in sorok.lista:
        if s[0] == 'kapuhiba_kereszt':
            ki.append('| %s | %s |' % (s[1], s[6]))
    ki += ['', '| futás | mentett válaszok újraellenőrzése (hibák) |', '|---|---|']
    for s in sorok.lista:
        if s[0] == 'mentett_ellenorzes':
            ki.append('| %s | %s — %s |' % (s[1], s[4], s[6]))
    ki += ['', '### Költség és beállítás futásonként (a futásnaplóból)', '', '| futás | mérőszám | érték | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'koltseg':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[3], s[4], s[6]))
    ki += ['', '## e) A prompt_v2 → v3 hatás (F3V3 a két v2-futáshoz képest) és a futásközi ingadozás', '',
           'Δ = F3V3 − a v2-futás(ok) átlaga; a 90%%-os intervallum a versek bootstrapje (rétegenként rétegzett, %d újramintavétel). '
           'Az ingadozás-becslés egyetlen futáspár (|F3V2B − F3V2|). „kívül”: |Δ| > az ingadozás ÉS az intervallum nem '
           'tartalmazza a 0-t (leíró jelölés, nem próba).' % N_BOOT, '',
           '| réteg | mérőszám | v2 átlag | F3V3 | Δ | Δ 90% | \\|F3V2B − F3V2\\| | jelölés | n |', '|---|---|---|---|---|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'hatas_osszevetes':
            ref, cl, dl, fl = (float(v) for v in s[4].split('|'))
            lo, hi = (float(v) for v in s[5].split('|'))
            jel, _, rest = s[6].partition(';')
            ki.append('| %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp | %s | %s |' % (
                s[2], s[3], 100 * ref, 100 * cl, 100 * dl, 100 * lo, 100 * hi, 100 * fl, jel, rest.split('n=')[1].split(';')[0]))
    ki += ['', '### Páronkénti összevetések', '',
           '| összevetés | réteg | mérőszám | ref | cél | Δ | Δ 90% | \\|Δ\\| 95. percentilis | n |', '|---|---|---|---|---|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'hatas':
            x, y, d = (float(v) for v in s[4].split('|'))
            lo, hi, ab = (float(v) for v in s[5].split('|'))
            ki.append('| %s | %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp | %s |' % (
                s[1], s[2], s[3], 100 * x, 100 * y, 100 * d, 100 * lo, 100 * hi, 100 * ab, s[6].split('n=')[-1]))
    ki += kiegeszites_md(sorok)
    ki.append('')
    with open(jelentes_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


# ---------------------------------------------------------------------------
# F21.80: a teljes mérés kiegészítései (a Sonnet futása, kapupont-bontás, a minősítés részletezése)
# ---------------------------------------------------------------------------

def _keret(gmod):
    """A konfigurált gondolkodási keret a gondolkodas_mod mezőből ('reasoning_max_tokens=1024' -> 1024), egyébként None."""
    if gmod.startswith('reasoning_max_tokens='):
        try:
            return int(gmod.split('=', 1)[1])
        except ValueError:
            return None
    return None


def gondolkodas_futasok(adat, sorok, futasok=FUTASOK):
    """A mért gondolkodási token futásonként (a futásnapló gondolkodas_token oszlopából), a finish_reason-ök és a
    konfigurált kerethez viszonyítás (csak ahol a gondolkodas_mod keretet ad)."""
    import futtat
    for f in futasok:
        sor = [r for r in adat.naplo if r['futas'] == f]
        if not sor:
            continue
        nev = NEVEK[f]
        g = [int(r.get('gondolkodas_token') or 0) for r in sor]
        ki = sum(int(r['kimenet_token']) for r in sor)
        sorok.add('gondolkodas', nev, meres.OSSZES, 'gondolkodasi_token', sum(g), ki,
                  'a kimeneti tokenből (completion_tokens) a modell által jelentett gondolkodási token (futásnapló)')
        sorok.add('gondolkodas', nev, meres.OSSZES, 'gondolkodasi_token_hivasonkent_max', max(g), '', 'min %d, medián %d, %d hívás' % (
            min(g), sorted(g)[len(g) // 2], len(g)))
        fr = {}
        for r in sor:
            fr[r.get('finish_reason') or '?'] = fr.get(r.get('finish_reason') or '?', 0) + 1
        sorok.add('gondolkodas', nev, meres.OSSZES, 'finish_reason', ', '.join('%s: %d' % kv_ for kv_ in sorted(fr.items())), '', '')
        modell = sorted({r['modell'] for r in sor})
        ar = futtat.ARAK.get(modell[0]) if len(modell) == 1 else None
        if ar:
            gk = sum(g) * ar[1] / 1e6
            ko = sum(float(r['koltseg_usd']) for r in sor)
            sorok.add('gondolkodas', nev, meres.OSSZES, 'gondolkodasi_token_koltsege_usd', '%.6f' % gk, '%.6f' % ko,
                      'a gondolkodási token × a kimeneti táblaár (%.2f USD/1M; %s) a mért összköltséghez (%.1f%%)' % (ar[1], modell[0], 100 * gk / ko if ko else 0))
        kerets = {_keret(r['gondolkodas_mod']) for r in sor} - {None}
        if len(kerets) == 1:
            k = kerets.pop()
            sorok.add('gondolkodas', nev, meres.OSSZES, 'keret_feletti_hivasok', sum(1 for x in g if x > k), len(g),
                      'a konfigurált keret (reasoning.max_tokens=%d) fölötti mért gondolkodási token hívásonként; a legnagyobb a keret %.1f-szerese'
                      % (k, max(g) / k))
        ln = [r for r in sor if (r.get('finish_reason') or '') == 'length']
        if ln:
            sorok.add('gondolkodas', nev, meres.OSSZES, 'length_hivasok', len(ln), len(sor),
                      'finish_reason=length: %s; költségük %.6f USD; kimenet %s token, ebből gondolkodás %s' % (
                          ', '.join('köteg %s / próba %s' % (r['koteg'], r['probalkozas']) for r in ln),
                          sum(float(r['koltseg_usd']) for r in ln), '+'.join(r['kimenet_token'] for r in ln),
                          '+'.join(r.get('gondolkodas_token') or '0' for r in ln)))


def sonnet_hivasok(adat, sorok, f=SONNET):
    """A Sonnet hívásonként: mért gondolkodási token a konfigurált kerethez képest, kimenet, finish_reason, költség."""
    for r in sorted((r for r in adat.naplo if r['futas'] == f), key=lambda r: (int(r['koteg']), int(r['probalkozas']))):
        k = _keret(r['gondolkodas_mod'])
        g = int(r.get('gondolkodas_token') or 0)
        sorok.add('sonnet_hivas', NEVEK[f], meres.OSSZES, 'köteg %02d / próba %s' % (int(r['koteg']), r['probalkozas']), g, r['kimenet_token'],
                  'gondolkodási token / kimeneti token; keret %s%s; finish_reason=%s; költség %s USD; versek %s, kapuhiba_db %s' % (
                      k, (' (×%.1f)' % (g / k)) if k else '', r.get('finish_reason') or '?', r['koltseg_usd'], r['igehely_db'], r['kapuhiba_db']))


def vegleges_kapuhibak(adat, sorok, f=SONNET):
    """A véglegesen kapuhibás versek: réteg, köteg, a végső kapupont és hibaüzenet, a köteg hívásainak finish_reason-je."""
    for sor in adat.kotegsorok[f]:
        n = [r for r in adat.naplo if r['futas'] == f and int(r['koteg']) == sor['koteg']]
        for ig in sor['igehelyek']:
            v = sor['versek'][ig]
            if v['allapot'] == 'ok':
                continue
            sorok.add('vegleges_kapuhiba', NEVEK[f], adat.reteg[ig], ig, '+'.join(sorted(meres._tipusok(v['hibak']))), 'köteg %s' % sor['koteg'],
                      'hívások: %s | végső hiba: %s%s' % (
                          '; '.join('próba %s: finish_reason=%s, kimenet %s (gondolkodás %s)' % (
                              r['probalkozas'], r.get('finish_reason') or '?', r['kimenet_token'], r.get('gondolkodas_token') or '0')
                              for r in sorted(n, key=lambda r: int(r['probalkozas']))),
                          ' / '.join(_rovid(h) for h in v['hibak'][:1]), ' | aranyvers' if ig in adat.arany else ''))


def alacsony_vetitett(ut=None):
    """(arány, alacsony, összes link) a koltseg_vetites_p3c.tsv kézimunka-soraiból (F22-rétegenként vetítve), ha van."""
    ut = ut or KOLTSEG_UT
    if not os.path.exists(ut):
        return None
    with open(ut, encoding='utf-8') as f:
        s = [x.rstrip('\n').split('\t') for x in f if x.strip() and not x.startswith('#')]
    fej = s[0]
    v = {}
    for x in s[1:]:
        r = dict(zip(fej, x))
        if r['szakasz'] == 'kezimunka' and r['reteg'] == 'Összes' and r['mero'] in ('vetitett_alacsony_link_biblia', 'vetitett_link_biblia'):
            v[r['mero']] = float(r['ertek'])
    if len(v) == 2 and v['vetitett_link_biblia']:
        return v['vetitett_alacsony_link_biblia'] / v['vetitett_link_biblia'], v['vetitett_alacsony_link_biblia'], v['vetitett_link_biblia']
    return None


def minosites_reszlet(sorok, kf, av, oss=PAR):
    """A minősítés részletezése: az (1) rétegenként (a 0/0 réteg „nem mérhető”, PD19 (1)) és az (5)
    mért (200 vers) és vetített (F22-rétegenként, a teljes Bibliára) értéke."""
    for r in meres.RETEGEK:
        m = _arany(sorok, oss, r, 'magas_pontossag')
        sorok.add('minosites_reszlet', oss, r, 'feltetel_1_magas_pontossag', m[0] if m else 0, m[1] if m else 0,
                  ('≥ 98%%: %s' % ('teljesül' if m[0] / m[1] >= 0.98 else 'nem teljesül')) if m else
                  'nincs magas link a rétegben (0/0): nem mérhető (PD19 (1); a Sonnet R3-aranyversei a 15. köteg length-lezárása '
                  'miatt végleg kapuhibásak; a próféták előtt pótolandó, pótló futás most nincs)')
    al = _arany(sorok, oss, meres.OSSZES, 'alacsony_arany [200 vers]')
    sorok.add('minosites_reszlet', oss, meres.OSSZES, 'feltetel_5_alacsony_arany_mert_200_vers', al[0], al[1],
              '≤ 10%%: %s; a minősítés ezt használja (meres_p3b.minosit)' % ('teljesül' if al[0] / al[1] <= 0.10 else 'nem teljesül'))
    if av:
        sorok.add('minosites_reszlet', oss, meres.OSSZES, 'feltetel_5_alacsony_arany_vetitett', '%.4f' % av[0], '',
                  'F22-rétegenként vetítve a teljes Bibliára (koltseg_vetites_p3c.tsv: %.0f / %.0f link); ≤ 10%%: %s' % (
                      av[1], av[2], 'teljesül' if av[0] <= 0.10 else 'nem teljesül'))
    if oss in kf:
        sorok.add('minosites_reszlet', oss, meres.OSSZES, 'feltetel_4_koltseg_felso90', '%.2f' % kf[oss][2], '',
                  'vetített %.2f USD [90%%: %.2f–%.2f]; ≤ 60 USD: %s' % (kf[oss][0], kf[oss][1], kf[oss][2],
                                                                     'teljesül' if kf[oss][2] <= 60 else 'nem teljesül'))


def beallitas_jeloles(sorok):
    sorok.add('jeloles', NEVEK[SONNET], meres.OSSZES, 'nem_determinisztikus', 'igen', '',
              'a Sonnet-kérés temperature nélkül ment, gondolkodással: a futás nem determinisztikus (egyetlen futás, ingadozás-becslés nincs)')
    sorok.add('jeloles', 'F21 pilot', meres.OSSZES, 'beallitas_elteres', 'igen', '',
              'az A és a B gondolkodás nélkül; a C kötelező minimális gondolkodással (kotelezo_effort=minimal); a Sonnet minimális '
              'gondolkodási kerettel (reasoning.max_tokens=1024), amelyet a modell nem tartott be (l. gondolkodas)')


def _kapupont_md_sonnet(sorok):
    fs = [NEVEK[SONNET], NEVEK[C3]]
    kr = {(s[1], s[2], s[3]): s for s in sorok.lista if s[0] == 'kapupont_reteg'}
    if not kr:
        return []
    merok = []
    for s in sorok.lista:
        if s[0] == 'kapupont_reteg' and s[3] not in merok:
            merok.append(s[3])

    def cella(o, r, m):
        x = kr.get((o, r, m))
        return '%s/%s' % (x[4], x[5]) if x else '—'
    ki = ['', '## h) Az első próbás kapuhiba kapupontonként és rétegenként: Sonnet és C (F3V3)', '',
          'Módszer: a köteg nyers[0] válaszának újraellenőrzése a teljes kapun (meres._tipusok); keresztellenőrzés a rétegenkénti '
          'első-próbás számokkal, a jsonl probalkozas=2 verseivel és a napló kapuhiba_db(probalkozas=1) összegével.', '',
          '| réteg | kapupont | %s | %s |' % tuple(fs), '|---|---|---|---|']
    for r in RETEGEK:
        for m in merok:
            ki.append('| %s | %s | %s | %s |' % (r, m, cella(fs[0], r, m), cella(fs[1], r, m)))
    ki += ['', '| futás | keresztellenőrzés (kapupont-bontás) |', '|---|---|']
    ki += ['| %s | %s |' % (s[1], s[6]) for s in sorok.lista if s[0] == 'kapupont_kereszt']
    ki += ['', '| futás | réteg | vers | kapupont | köteg | első próba: hibaüzenet (röviden) \\| végleg |', '|---|---|---|---|---|---|']
    ki += ['| %s | %s | %s | %s | %s | %s |' % (s[1], s[2], s[3], s[4], s[5], s[6].replace('|', '\\|'))
           for s in sorok.lista if s[0] == 'kapupont_vers' and s[1] == fs[0]]
    return ki


def kiegeszites_md(sorok):
    """A teljes jelentés F21.80-as szakaszai (f–h)."""
    gs = {s[3]: s for s in sorok.lista if s[0] == 'gondolkodas' and s[1] == NEVEK[SONNET]}
    ki = ['', '## f) A Sonnet futása: a gondolkodási keret, a length-lezárások, a végleges kapuhibák (F21.80)', '']
    if gs:
        g, kt = gs['gondolkodasi_token'], gs.get('gondolkodasi_token_koltsege_usd')
        mx, kf_ = gs['gondolkodasi_token_hivasonkent_max'], gs.get('keret_feletti_hivasok')
        ln = gs.get('length_hivasok')
        ki += ['### (i) A gondolkodási keret: a modell nem tartotta be', '',
               '- A konfigurált keret: reasoning.max_tokens = 1024 (gondolkodas_mod: %s).' % ', '.join(
                   sorted({s[4] for s in sorok.lista if s[0] == 'koltseg' and s[1] == NEVEK[SONNET] and s[3] == 'gondolkodas_mod'})),
               '- Mért gondolkodási token összesen: %s a %s kimeneti tokenből (%.1f%%); hívásonként a legnagyobb %s (%s).' % (
                   g[4], g[5], 100.0 * int(g[4]) / int(g[5]), mx[4], mx[6])]
        if kf_:
            ki.append('- A keret fölötti hívások: %s a %s-ből; %s.' % (kf_[4], kf_[5], kf_[6].split('; ', 1)[1]))
        if kt:
            ki.append('- A költségre: %s.' % kt[6].replace('a gondolkodási token × a kimeneti táblaár', 'a gondolkodási token a kimeneti táblaáron %s USD' % kt[4]))
        if ln:
            ki.append('- A length-lezárások: %s a %s hívásból (%s): a kimenet elérte a max_tokens-t, és nagyobb részét a gondolkodási '
                      'token adta; a köteg versei véglegesen kapuhibásak maradtak (alább).' % (ln[4], ln[5], ln[6]))
        ki += ['', '| köteg / próba | gondolkodási token / kimeneti token | megjegyzés |', '|---|---|---|']
        ki += ['| %s | %s / %s | %s |' % (s[3], s[4], s[5], s[6].split('; ', 1)[1]) for s in sorok.lista if s[0] == 'sonnet_hivas']
    ki += ['', '| futás | mérőszám | érték | nevező | megjegyzés |', '|---|---|---|---|---|']
    ki += ['| %s | %s | %s | %s | %s |' % (s[1], s[3], s[4], s[5], s[6]) for s in sorok.lista if s[0] == 'gondolkodas']
    ki += ['', '### (ii) Beállítás-eltérés és determinizmus', '']
    ki += ['- %s: %s.' % (s[1], s[6]) for s in sorok.lista if s[0] == 'jeloles']
    vk = [s for s in sorok.lista if s[0] == 'vegleges_kapuhiba']
    ki += ['', '### A Sonnet véglegesen kapuhibás versei (%d)' % len(vk), '',
           '| réteg | vers | végső kapupont | köteg | hívások \\| végső hiba |', '|---|---|---|---|---|']
    ki += ['| %s | %s | %s | %s | %s |' % (s[2], s[3], s[4], s[5], s[6].replace('|', '\\|')) for s in vk]
    ki += ['', '## g) A minősítés részletezése (az (1) 0/0 rétege „nem mérhető”, PD19 (1); a küszöb szempontjából csak a mért érték számít)', '',
           '| feltétel | réteg | érték | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'minosites_reszlet':
            ert = _pct(s[4], s[5]) if s[5] not in ('', '0') else ('%.1f%%' % (100 * float(s[4])) if 'vetitett' in s[3] else
                                                                ('— (0/0)' if s[5] == '0' else s[4]))
            ki.append('| %s | %s | %s | %s |' % (s[3], s[2], ert, s[6]))
    ki += _kapupont_md_sonnet(sorok)
    return ki


def szamol(forras_dir=None, arany_ut=None, arany_sha=None, koltseg_ut=None, n_boot=N_BOOT):
    """A teljes P4-számítás (kiírás nélkül). Visszaad: (adat, info, sorok, kimenet, kf)."""
    adat, info = betolt(forras_dir, arany_ut, arany_sha)
    sorok = Sorok()
    for f in (SONNET, C3, C2, C2B):
        meres_p3b.egymodell(adat, sorok, NEVEK[f], f)
    kim = par_kimenet(adat)
    par_merok(adat, sorok, kim)
    ab_egyezes_par(adat, sorok)
    kf = koltseg_felso(koltseg_ut)
    minosit(sorok, kf)
    prompt_hatas(adat, sorok, n_boot)
    kapuhiba_futasok(adat, sorok)
    koltseg_futasok(adat, sorok)
    mentett_ellenorzes(sorok, forras_dir or F21P)
    # F21.80 (a meglévő sorok után)
    gondolkodas_futasok(adat, sorok)
    sonnet_hivasok(adat, sorok)
    vegleges_kapuhibak(adat, sorok)
    minosites_reszlet(sorok, kf, alacsony_vetitett(koltseg_ut))
    beallitas_jeloles(sorok)
    kapupont_reteg(adat, sorok, [SONNET, C3])
    return adat, info, sorok, kim, kf


def fut(forras_dir=None, arany_ut=None, arany_sha=None, eredmeny_ut=None, jelentes_ut=None, koltseg_ut=None, ts=None):
    adat, info, sorok, kim, kf = szamol(forras_dir, arany_ut, arany_sha, koltseg_ut)
    kiir(sorok, info, ts or tokenek.generalas_ts(), eredmeny_ut or EREDMENY_UT, jelentes_ut or JELENTES_UT, kf)
    print('kész: %d sor -> %s, %s (arany: %s)' % (len(sorok.lista), eredmeny_ut or EREDMENY_UT, jelentes_ut or JELENTES_UT, info['verzio']))
    for s in sorok.lista:
        if s[0] == 'minosites':
            print('  %s | %s | %s | %s' % (s[1], s[3], s[4], s[6]))
    rossz = [s for s in sorok.lista if s[3] == 'keresztellenorzes_elso_probalkozas' and 'ELTÉR' in s[6]]
    if rossz:
        print('FIGYELEM: a kapuhiba keresztellenőrzése eltér: %s' % [s[1] for s in rossz], file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# önteszt (mock-adat, determinisztikus)
# ---------------------------------------------------------------------------

def onteszt_csak_c(mappa, info, ellen):
    """A --csak-c mód öntesztje a mock-adaton (a hívó onteszt() mappájában; a repó kimeneteit nem írja)."""
    import contextlib
    import io
    import json
    arany3, sha3 = os.path.join(F21P, 'arany_opus_v3.jsonl'), os.path.join(F21P, 'arany_opus_v3.sha256')
    nincs_k = os.path.join(mappa, 'nincs_koltseg_c.tsv')
    ut_e, ut_j = os.path.join(mappa, 'c_eredmeny.tsv'), os.path.join(mappa, 'c_jelentes.md')

    def futtat_c(ts, koltseg=nincs_k, e=ut_e, j=ut_j):
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut_c(mappa, arany3, sha3, e, j, koltseg, ts=ts, n_boot=40)
        with open(e, encoding='utf-8') as f:
            t = f.read()
        with open(j, encoding='utf-8') as f:
            m = f.read()
        return kod, t, m
    kod, t1, m1 = futtat_c('T1')
    ellen(kod == 0, 'csak-c: a mock-futás kilépési kódja %d' % kod)
    s0 = t1.split('\n')[0]
    ellen(s0.startswith('# GENERÁLT: eszkozok/karoli_strong/meres_p3c.py --csak-c | scope=') and ' | forras=' in s0 and ' | ts=T1 ' in s0,
          'csak-c: a TSV fejléce nem a scope|forras|ts proveniencia: %s' % s0[:120])
    ellen('scope=' in m1 and 'forras=' in m1 and 'ts=T1' in m1, 'csak-c: az md nem viseli a proveniencia-fejlécet')
    kod, t2, m2 = futtat_c('T2')
    ellen(t1.replace('ts=T1 ', 'ts=T2 ') == t2 and m1.replace('ts=T1', 'ts=T2') == m2, 'csak-c: a futás nem determinisztikus')
    sorok = [x.split('\t') for x in t1.split('\n')[2:] if x]
    ellen(all(len(x) == 7 for x in sorok), 'csak-c: a TSV-sorok nem mind 7 mezősek')
    # a Sonnet és a pár: csak „nincs adat” sorok, minden rétegben; nincs minősítés, nincs Sonnet-mérés
    na = {(x[1], x[2]) for x in sorok if x[0] == 'nincs_adat' and x[4] == NINCS_SONNET}
    ellen(na == {(o, r) for o in (NEVEK[SONNET], PAR) for r in RETEGEK}, 'csak-c: a nincs-adat sorok hiányosak: %s' % sorted(na))
    ellen(not any(x[0] in ('minosites', 'minosites_reteg', 'par_versosztalyok', 'ab_egyezes') for x in sorok)
          and not any(x[1] in (NEVEK[SONNET], PAR) and x[0] != 'nincs_adat' for x in sorok),
          'csak-c: a Sonnet / a pár mért sort vagy minősítést kapott')
    ellen(NINCS_SONNET in m1, 'csak-c: az md-ben nincs a nincs-adat jelölés')
    # küszöb: (1) és (5) n.é. minden rétegben, a (4) költségfájl nélkül nem mért, egy „nincs” minősítés
    ku = {(x[3], x[2]): x for x in sorok if x[0] == 'kuszob'}
    ellen(all(ku[('f1_magas_pontossag_98', r)][4] == 'n.é.' and ku[('f5_alacsony_arany_10', r)][4] == 'n.é.' for r in RETEGEK),
          'csak-c: az (1)/(5) nem n.é.')
    ellen(ku[('f4_koltseg_felso90_60', meres.OSSZES)][4] == 'nem mért', 'csak-c: a hiányzó költség nem „nem mért”')
    ellen(ku[('minosites', meres.OSSZES)][4].startswith('nincs'), 'csak-c: a C minősítést kapott')
    ellen(not any(x[4] in ('megfelel', 'nem felel meg') for x in sorok), 'csak-c: megfelel/nem felel meg szerepel')
    # a (4) a költségfájlból
    ut_k = os.path.join(mappa, 'koltseg_c_teszt.tsv')
    with open(ut_k, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: mock\nszakasz\tosszeallitas\treteg\tmero\tertek\talso90\tfelso90\tmegjegyzes\n')
        f.write('vetites\t%s\tÖsszes\tkoltseg_usd\t30\t25\t61\tmock\n' % NEVEK[C3])
    kod, tk, _ = futtat_c('T1', ut_k, os.path.join(mappa, 'ck.tsv'), os.path.join(mappa, 'ck.md'))
    x = [s.split('\t') for s in tk.split('\n') if s.startswith('kuszob\t%s\tÖsszes\tf4_' % NEVEK[C3])]
    ellen(x and x[0][4] == '61.00' and 'a küszöbön kívül' in x[0][6], 'csak-c: a (4) nem a költségfájl felső széle / viszonya: %s' % x)
    # független újraszámolás: az F3V3 lefedettsége az arany v3-ra (Összes), a saját jsonl-olvasással
    kiz = tokenek.meres_kizaras()
    gold = {}
    with open(arany3, encoding='utf-8') as fh:
        for s in fh:
            if s.strip():
                o = json.loads(s)
                gold[o['vers']] = {(p[0], e) for p in o['parok'] for e in p[1] if (o['vers'], e) not in kiz}
    t = g = 0
    with open(os.path.join(mappa, 'valaszok', 'F3V3.jsonl'), encoding='utf-8') as fh:
        for s in fh:
            if not s.strip():
                continue
            for ig, v in json.loads(s)['versek'].items():
                if v['allapot'] == 'ok' and ig in gold:
                    lk = {(p[0], e) for p in v['obj']['parok'] for e in p[1] if (ig, e) not in kiz}
                    t += len(lk & gold[ig])
                    g += len(gold[ig])
    x = [s for s in sorok if s[0] == 'feltetelek' and s[1] == NEVEK[C3] and s[2] == meres.OSSZES and s[3] == 'lefedettseg']
    ellen(x and (int(x[0][4]), int(x[0][5])) == (t, g), 'csak-c: az F3V3 lefedettsége (%s) nem a független (%d/%d)' % (x[0][4:6] if x else None, t, g))
    # az arany v2 → v3 hatás: a v2-oldal = az egymodell × arany v2 sora; vannak eltérő linkek
    for f in FUTASOK_C:
        ah = [s for s in sorok if s[0] == 'arany_hatas' and s[1] == NEVEK[f] and s[2] == meres.OSSZES and s[3] == 'lefedettseg']
        ev = [s for s in sorok if s[0] == 'feltetelek' and s[1] == NEVEK[f] + V2_CIMKE and s[2] == meres.OSSZES and s[3] == 'lefedettseg']
        ellen(ah and ev and ah[0][5].split('|')[0] == '%s/%s' % (ev[0][4], ev[0][5]), 'csak-c: az arany-hatás v2-oldala nem az egymodell × v2 (%s)' % f)
    # F21.76: a kapupont-bontás (a mock első-próbás és tartós hibái mind az 5. kapupontnál), keresztellenőrzés, j) szakasz
    for f in FUTASOK_C:
        varhato = set(info['hibas_mindig'].get(f, ())) | set(info['hibas_elso'].get(f, ()))
        kv = [s for s in sorok if s[0] == 'kapupont_vers' and s[1] == NEVEK[f]]
        ellen({s[3] for s in kv} == varhato and all(s[4] == '5' for s in kv),
              'csak-c: a kapupont-versek (%s) nem a mock hibás versei: %s' % (f, sorted(s[3] for s in kv)))
        ellen(all(('végleg: kapuhibás' in s[6]) == (s[3] in info['hibas_mindig'].get(f, ())) for s in kv),
              'csak-c: a kapupont-versek végleges állapota hibás (%s)' % f)
        kk = [s for s in sorok if s[0] == 'kapupont_kereszt' and s[1] == NEVEK[f]]
        ellen(kk and 'EGYEZIK' in kk[0][6] and int(kk[0][4]) == len(varhato), 'csak-c: a kapupont-keresztellenőrzés (%s): %s' % (f, kk))
        for r in RETEGEK:
            h = [s for s in sorok if s[0] == 'kapupont_reteg' and s[1] == NEVEK[f] and s[2] == r and s[3] == 'hibas_versek_elso']
            p5 = [s for s in sorok if s[0] == 'kapupont_reteg' and s[1] == NEVEK[f] and s[2] == r and s[3] == 'kapupont_5_elso']
            p1 = [s for s in sorok if s[0] == 'kapupont_reteg' and s[1] == NEVEK[f] and s[2] == r and s[3] == 'kapupont_1-json_elso']
            ellen(h and p5 and p1 and h[0][4] == p5[0][4] and p1[0][4] == '0', 'csak-c: a kapupont-réteg sorai hibásak (%s, %s)' % (f, r))
    ellen(not any(s[0] == 'kapupont_vers' and s[1] == NEVEK[SONNET] for s in sorok), 'csak-c: Sonnet-kapupont sor')
    ellen('## j) Az első próbás kapuhiba kapupontonként és rétegenként' in m1 and '### Az R3: F3V3, F3V2, F3V2B' in m1,
          'csak-c: az md-ben nincs a j) szakasz')
    ellen(not any(s[0] == 'jeloles' for s in sorok), 'csak-c: a mock-futás (forras_dir) besorolás-jelölést kapott')
    # az R1-jelölés: mock besorolás-fájl a mock-adat F3V3-ának valódi hiányzó linkjeivel (két K4 (a), a többi c)
    adat_m, _ = betolt(mappa, arany3, sha3, FUTASOK_C)
    kus = 0.999           # a mock lefedettsége a 95%-ot minden rétegben meghaladja: szigorúbb küszöbbel teszteljük
    jel_ret = [r for r in meres.RETEGEK if _pl(adat_m, C3, r)[2] and _pl(adat_m, C3, r)[0] / _pl(adat_m, C3, r)[2] < kus]
    ut_b = os.path.join(mappa, 'besorolas_mock.tsv')
    with open(ut_b, 'w', encoding='utf-8', newline='\n') as fb:
        fb.write('# MANUAL: mock\nfutas\treteg\tirany\tstatusz\tosztaly\tkonvencio_vagy_jegyzetpont\n')
        for r in jel_ret:
            t_, _, g_, _ = _pl(adat_m, C3, r)
            for i in range(g_ - t_):
                fb.write('%s\t%s\thianyzo\telteres\t%s\t%s\n' % (C3, r, 'a' if i < 2 else 'c', 'K4 mock' if i < 2 else ''))
    sj = Sorok()
    lefedettseg_jeloles(adat_m, sj, ut_b, kus)
    sj95 = Sorok()
    lefedettseg_jeloles(adat_m, sj95, ut_b)
    ellen(jel_ret and [s[2] for s in sj.lista] == jel_ret and all(
        'a 99,9%-os küszöbön kívül' in s[6] and 'K4-eltérés (a)' in s[6] and 'EGYEZIK' in s[6] and
        (' közül %d K4' % min(2, int(s[5]) - int(s[4]))) in s[6] for s in sj.lista),
          'csak-c: az R1-jelölés hibás: %s' % sj.lista)
    ellen(sj95.lista == [], 'csak-c: 95%%-os küszöbbel a mock jelölést kapott: %s' % sj95.lista)
    with open(ut_b, 'a', encoding='utf-8', newline='\n') as fb:      # egy többlet hiányzó sor -> ELTÉR
        fb.write('%s\t%s\thianyzo\telteres\tc\t\n' % (C3, jel_ret[0] if jel_ret else 'R1'))
    sje = Sorok()
    lefedettseg_jeloles(adat_m, sje, ut_b, kus)
    ellen(sje.lista and 'ELTÉR' in sje.lista[0][6], 'csak-c: a jelölés keresztellenőrzése nem fogja az eltérést')
    el = [s for s in sorok if s[0] == 'arany_hatas' and s[3] == 'eltero_linkek']
    ellen(el and int(el[0][4]) > 0, 'csak-c: a két arany között nincs eltérő link')
    ellen(len({s[1] for s in sorok if s[0] == 'hatas_osszevetes'}) == 2, 'csak-c: a prompt-hatás nem mindkét aranyon')
    ellen(not any(s[0] == 'kjv' for s in sorok), 'csak-c: F8V3 nélkül kjv-sorok vannak')
    # F8V3 (tájékoztató): az F3V3 másolata a mockban (a napló-sorokkal) -> kjv-sorok, Δ = 0
    import shutil
    shutil.copyfile(os.path.join(mappa, 'valaszok', 'F3V3.jsonl'), os.path.join(mappa, 'valaszok', 'F8V3.jsonl'))
    naplo = os.path.join(mappa, 'futasnaplo.tsv')
    with open(naplo, encoding='utf-8') as f:
        ns = f.read().split('\n')
    uj = [s.split('\t') for s in ns[1:] if s and s.split('\t')[1] == C3]
    with open(naplo, 'a', encoding='utf-8', newline='\n') as f:
        for m in uj:
            m[1] = F8
            f.write('\t'.join(m) + '\n')
    kod, t8, m8 = futtat_c('T1', nincs_k, os.path.join(mappa, 'c8.tsv'), os.path.join(mappa, 'c8.md'))
    s8 = [x.split('\t') for x in t8.split('\n')[2:] if x]
    ellen(kod == 0 and any(s[0] == 'kjv' and s[2] == 'R4' and s[4] == 'KJV nélkül, nem mérhető' for s in s8)
          and 'KJV nélkül, nem mérhető' in m8, 'csak-c: az F8V3 R4-jelölése hiányzik (kód %d)' % kod)
    d8 = [s for s in s8 if s[0] == 'hatas' and s[1].startswith('F8V3 − F3V3')]
    ellen(d8 and all(abs(float(s[4].split('|')[2])) < 1e-12 for s in d8), 'csak-c: az F8V3 = F3V3 másolat Δ-ja nem nulla')
    os.remove(os.path.join(mappa, 'valaszok', 'F8V3.jsonl'))
    # a SONNETV3 hiánya: a teljes mód SystemExit (--csak-c-re utal, semmi nem íródik), a csak-c ugyanazt adja
    os.remove(os.path.join(mappa, 'valaszok', 'SONNETV3.jsonl'))
    ut_x = os.path.join(mappa, 'teljes_nem_irodik.tsv')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            fut(mappa, arany3, sha3, ut_x, os.path.join(mappa, 'teljes_nem_irodik.md'), nincs_k, ts='T1')
        ellen(False, 'a SONNETV3 hiánya nem állította meg a teljes mérést')
    except SystemExit as e:
        ellen('--csak-c' in str(e) and not os.path.exists(ut_x), 'a SONNETV3 hiányának hibaüzenete/mellékhatása hibás: %s' % e)
    kod, t3, _ = futtat_c('T1')
    ellen(kod == 0 and t3 == t1, 'csak-c: a SONNETV3 jsonl hiánya megváltoztatta a csak-c kimenetet')


def onteszt():
    import contextlib
    import io
    import json
    import shutil
    import p3c_mock
    hibak = []

    def ellen(f, leiras):
        if not f:
            hibak.append(leiras)

    # a régi kimenetek bájtazonossága
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'a régi kimenetek megváltoztak: %s' % p3c_mock.regi_kimenetek_hibak())
    # a minősítés-logika mock sorlistán (feltételenként bukó esetek)
    kf0 = {PAR: (10.0, 8.0, 12.0)}

    def mock_sorok(mag=99, lef=96, regi=(30, 30), al=5):
        s = Sorok()
        for r in meres.RETEGEK + [meres.OSSZES]:
            s.add('feltetelek', PAR, r, 'magas_pontossag', mag, 100)
            s.add('feltetelek', PAR, r, 'lefedettseg', lef, 100)
            s.add('feltetelek', PAR, r, 'regi_arany_kizaras_nelkul', regi[0], regi[1])
            s.add('feltetelek', PAR, r, 'regi_arany_kizarassal_tajekoztato', regi[0], regi[1])
            s.add('feltetelek', PAR, r, 'alacsony_arany [200 vers]', al, 100)
        return s

    def ered(s, kf):
        minosit(s, kf)
        return {x[3]: x[4] for x in s.lista if x[0] == 'minosites'}
    m = ered(mock_sorok(), kf0)
    ellen(m['minosites (kizárás nélküli régi arannyal)'] == 'megfelel', 'minősítés: a mind az öt feltételt teljesítő nem felel meg: %s' % m)
    for nev, s, kf, bukik in (('1', mock_sorok(mag=97), kf0, '1'), ('2', mock_sorok(lef=94), kf0, '2'),
                              ('3', mock_sorok(regi=(30, 32)), kf0, '3'), ('4', mock_sorok(), {PAR: (50.0, 40.0, 61.0)}, '4'),
                              ('5', mock_sorok(al=11), kf0, '5')):
        m = ered(s, kf)
        ellen(m['minosites (kizárás nélküli régi arannyal)'] == 'nem felel meg' and m['feltetel_%s' % bukik] == 'nem teljesül',
              'minősítés: a %s. feltétel bukása nem buktat: %s' % (nev, m))
    m = ered(mock_sorok(), {})
    ellen(m['feltetel_4'] == 'nem mért' and m['minosites (kizárás nélküli régi arannyal)'] == 'nem minősíthető (nem mért feltétel)',
          'minősítés: a hiányzó költség nem „nem mért”: %s' % m)
    # F21.82: a 0/0 magas-linkű réteg az (1)-ben „nem mérhető”; más bukott feltétellel „nem felel meg”, egyébként nem minősíthető
    def nulla_r3(s):
        s.lista = [x if not (x[3] == 'magas_pontossag' and x[2] == 'R3') else x[:4] + ['0', '0', ''] for x in s.lista]
        return s
    m = ered(nulla_r3(mock_sorok()), kf0)
    ellen(m['feltetel_1'] == 'nem mérhető' and m['minosites (kizárás nélküli régi arannyal)'] == 'nem minősíthető (nem mérhető feltétel)',
          'minősítés: a 0/0 réteg nem „nem mérhető”: %s' % m)
    m = ered(nulla_r3(mock_sorok(al=11)), kf0)
    ellen(m['feltetel_1'] == 'nem mérhető' and m['minosites (kizárás nélküli régi arannyal)'] == 'nem felel meg',
          'minősítés: a 0/0 réteg + bukott (5) nem „nem felel meg”: %s' % m)
    m = ered(nulla_r3(mock_sorok(mag=97)), kf0)
    ellen(m['feltetel_1'] == 'nem teljesül', 'minősítés: a mérhető rétegek bukása a 0/0 réteg mellett nem buktat: %s' % m)
    # a pár-logika kézzel (kapuhibás oldal: a túlélő oldal linkjei alacsonyak)
    A, B = {(1, 1), (2, 2)}, {(1, 1), (2, 3)}
    _, ab = meres_p3b.g4_vers(True, True, A, B, False, None, False)
    ellen(ab == {(1, 1): 'magas', (2, 2): 'alacsony', (2, 3): 'alacsony'}, 'pár: A∩B / A△B szintek hibásak: %s' % ab)
    _, ab = meres_p3b.g4_vers(True, False, A, None, False, None, False)
    ellen(ab == {(1, 1): 'alacsony', (2, 2): 'alacsony'}, 'pár: a B kapuhibája nem teszi alacsonnyá az A linkjeit: %s' % ab)
    _, ab = meres_p3b.g4_vers(False, False, None, None, False, None, False)
    ellen(ab == {}, 'pár: a két kapuhiba nem üres kimenet')

    # mock-adatos teljes menet
    mappa = p3c_mock.ideiglenes('f21p_onteszt_meres_p3c_')
    try:
        info = p3c_mock.general(mappa)
        ut_e, ut_j = os.path.join(mappa, 'eredmeny.tsv'), os.path.join(mappa, 'jelentes.md')
        # költségfájl nélkül: a (4) feltétel nem mért
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_e, ut_j, os.path.join(mappa, 'nincs_koltseg.tsv'), ts='T1')
        ellen(kod == 0, 'a mock-futás kilépési kódja %d' % kod)
        with open(ut_e, encoding='utf-8') as f:
            tsv1 = f.read()
        with open(ut_j, encoding='utf-8') as f:
            md1 = f.read()
        sor0 = tsv1.split('\n')[0]
        ellen(sor0.startswith('# GENERÁLT: eszkozok/karoli_strong/meres_p3c.py | scope=') and ' | forras=' in sor0 and ' | ts=T1 ' in sor0,
              'a TSV fejléce nem a scope|forras|ts proveniencia: %s' % sor0[:120])
        ellen('scope=' in md1 and 'forras=' in md1 and 'ts=T1' in md1 and 'arany_teszt.jsonl' in md1,
              'az md nem viseli a proveniencia-fejlécet')
        ellen('nem minősíthető (nem mért feltétel)' in md1 or 'nem felel meg' in md1, 'az md-ben nincs minősítés')
        # determinisztikus: az ismételt futás csak a ts-ben tér el
        with contextlib.redirect_stdout(io.StringIO()):
            fut(mappa, info['arany_ut'], info['arany_sha'], ut_e, ut_j, os.path.join(mappa, 'nincs_koltseg.tsv'), ts='T2')
        with open(ut_e, encoding='utf-8') as f:
            tsv2 = f.read()
        with open(ut_j, encoding='utf-8') as f:
            md2 = f.read()
        ellen(tsv1.replace('ts=T1 ', 'ts=T2 ') == tsv2 and md1.replace('ts=T1', 'ts=T2') == md2,
              'a futás nem determinisztikus (a ts-en kívül eltérés)')
        sorok = [x.split('\t') for x in tsv2.split('\n')[2:] if x]
        ellen(all(len(x) == 7 for x in sorok), 'a TSV-sorok nem mind 7 mezősek')
        adat, ainfo, sk, kim, kf = szamol(mappa, info['arany_ut'], info['arany_sha'], os.path.join(mappa, 'nincs_koltseg.tsv'), n_boot=50)

        # független újraszámolás (a saját jsonl-olvasással): a pár `magas` pontossága és lefedettsége, összesen
        def futas_linkek(f):
            ki = {}
            with open(os.path.join(mappa, 'valaszok', '%s.jsonl' % f), encoding='utf-8') as fh:
                for s in fh:
                    if not s.strip():
                        continue
                    for ig, v in json.loads(s)['versek'].items():
                        ki[ig] = None if v['allapot'] != 'ok' else {(p[0], e) for p in v['obj']['parok'] for e in p[1]}
            return ki
        ls, lc = futas_linkek(SONNET), futas_linkek(C3)
        kiz = tokenek.meres_kizaras()
        gold = {}
        with open(info['arany_ut'], encoding='utf-8') as fh:
            for s in fh:
                if s.strip():
                    o = json.loads(s)
                    gold[o['vers']] = {(p[0], e) for p in o['parok'] for e in p[1] if (o['vers'], e) not in kiz}

        def szur(ig, x):
            return {(k, e) for k, e in x if (ig, e) not in kiz}
        mt = mc = gt = 0
        t_minden = 0          # a végső kimenet minden (magas és alacsony) linkje az aranyban: a lefedettség számlálója
        alacsony_osszes = osszes_link = 0
        for ig in adat.versek:
            a = None if ls[ig] is None else szur(ig, ls[ig])
            b = None if lc[ig] is None else szur(ig, lc[ig])
            if a is not None and b is not None:
                magas = a & b
                ala = len(a ^ b)
            elif a is not None or b is not None:
                magas = set()
                ala = len(a if a is not None else b)
            else:
                magas, ala = set(), 0
            osszes_link += len(magas) + ala
            alacsony_osszes += ala
            if ig in gold:
                gt += len(gold[ig])
                mc += len(magas)
                mt += len(magas & gold[ig])
                if a is not None and b is not None:
                    kimenet_l = a | b
                else:
                    kimenet_l = a if a is not None else (b if b is not None else set())
                t_minden += len(kimenet_l & gold[ig])
        x = _arany(sk, PAR, meres.OSSZES, 'magas_pontossag')
        # az Összes sor az R1–R4 összeadása: a magas_pontossag az Összes-ben
        ellen(x == (mt, mc), 'pár: a magas pontosság (%s) nem egyezik a független számítással (%s)' % (x, (mt, mc)))
        x = _arany(sk, PAR, meres.OSSZES, 'lefedettseg')
        ellen(x == (t_minden, gt), 'pár: a lefedettség (%s) nem egyezik a független számítással (%s)' % (x, (t_minden, gt)))
        x = _arany(sk, PAR, meres.OSSZES, 'alacsony_arany [200 vers]')
        ellen(x == (alacsony_osszes, osszes_link), 'pár: az alacsony arány (%s) nem egyezik (%s)' % (x, (alacsony_osszes, osszes_link)))
        # kapuhibás oldal: a vers minden linkje alacsony
        ig_c = info['c_hiba']         # az F3V3 tartósan kapuhibás, a Sonnet ok
        ig_s = info['sonnet_hiba']    # a Sonnet kapuhibás, a C ok
        ig_m = info['mind_hiba']      # mindkettő
        ellen(lc[ig_c] is None and ls[ig_c] is not None and kim[ig_c] and set(kim[ig_c].values()) == {'alacsony'}
              and set(kim[ig_c]) == szur(ig_c, ls[ig_c]), 'pár: a C kapuhibás versén nem a Sonnet minden linkje alacsony')
        ellen(ls[ig_s] is None and lc[ig_s] is not None and kim[ig_s] and set(kim[ig_s].values()) == {'alacsony'}
              and set(kim[ig_s]) == szur(ig_s, lc[ig_s]), 'pár: a Sonnet kapuhibás versén nem a C minden linkje alacsony')
        ellen(ls[ig_m] is None and lc[ig_m] is None and kim[ig_m] == {}, 'pár: a két kapuhibás versnek van kimenete')
        x = _arany(sk, PAR, meres.OSSZES, 'kimenet_nelkuli_versek [200 vers]')
        # a kimenet_nelkuli sor a szintek szakaszban van: külön keresés
        kn = [s for s in sk.lista if s[0] == 'szintek' and s[1] == PAR and s[2] == meres.OSSZES and s[3] == 'kimenet_nelkuli_versek [200 vers]']
        ellen(kn and int(kn[0][4]) >= 1, 'pár: nincs kimenet nélküli vers a két kapuhibás vers mellett')
        # kapuhiba-keresztellenőrzés és mentett ellenőrzés
        kk = [s for s in sk.lista if s[0] == 'kapuhiba_kereszt']
        ellen(len(kk) == 4 and all('EGYEZIK' in s[6] for s in kk), 'kapuhiba-keresztellenőrzés: %s' % [s[6] for s in kk])
        ellen(all(s[4] == '0' for s in sk.lista if s[0] == 'mentett_ellenorzes'), 'mentett ellenőrzés hibát ad')
        # F21.80: a végleges kapuhibák (a mock tartós hibái), a kapupont-bontás (Sonnet, F3V3), a minősítés részletezése, jelölések
        vk = {s[3] for s in sk.lista if s[0] == 'vegleges_kapuhiba'}
        ellen(vk == set(info['hibas_mindig']['SONNETV3']), 'F21.80: a Sonnet végleges kapuhibái nem a mock tartós hibái: %s' % sorted(vk))
        kpk = [s for s in sk.lista if s[0] == 'kapupont_kereszt']
        ellen({s[1] for s in kpk} == {NEVEK[SONNET], NEVEK[C3]} and all('EGYEZIK' in s[6] for s in kpk), 'F21.80: kapupont-kereszt: %s' % kpk)
        ellen(len([s for s in sk.lista if s[0] == 'minosites_reszlet' and s[3] == 'feltetel_1_magas_pontossag']) == 4
              and any(s[0] == 'jeloles' and s[3] == 'nem_determinisztikus' for s in sk.lista)
              and len([s for s in sk.lista if s[0] == 'sonnet_hivas']) == len([r for r in adat.naplo if r['futas'] == SONNET])
              and any(s[0] == 'gondolkodas' and s[1] == NEVEK[SONNET] and s[3] == 'gondolkodasi_token' for s in sk.lista),
              'F21.80: a minősítés-részletezés / jelölés / hívás- / gondolkodás-sorok hiányosak')
        ellen('## f) A Sonnet futása' in md1 and '## g) A minősítés részletezése' in md1 and '## h) Az első próbás kapuhiba' in md1,
              'F21.80: az md f–h szakasza hiányzik')
        ellen(_keret('reasoning_max_tokens=1024') == 1024 and _keret('kotelezo_effort=minimal') is None, 'F21.80: _keret hibás')
        # a prompt-hatás: a v2-átlaghoz képest; az ingadozás-sor megvan minden rétegre
        ho = [s for s in sk.lista if s[0] == 'hatas_osszevetes']
        ellen(len({s[2] for s in ho}) == 5 and len({s[3] for s in ho}) == 4, 'a prompt-hatás sorai nem fedik a rétegeket/mérőszámokat (%d)' % len(ho))
        ellen(all(len(s[4].split('|')) == 4 and len(s[5].split('|')) == 2 for s in ho), 'a hatas_osszevetes sorok alakja hibás')
        # a mock-beli F3V3 és F3V2 módosítási szabálya eltér: a Δ nem azonosan nulla
        ellen(any(abs(float(s[4].split('|')[2])) > 0 for s in ho), 'a prompt-hatás Δ-ja mindenütt nulla a mockban')
        # egymodelles összeállítás: nincs magas/alacsony, n.é.
        for f in (SONNET, C3, C2, C2B):
            ellen(any(s[1] == NEVEK[f] and s[3] == 'magas_pontossag' and s[4] == 'n.é.' for s in sk.lista)
                  and any(s[1] == NEVEK[f] and s[3] == 'alacsony_arany' and s[4] == 'n.é.' for s in sk.lista)
                  and not any(s[0] == 'minosites' and s[1] == NEVEK[f] for s in sk.lista),
                  'egymodelles %s: magas/alacsony nem n.é., vagy kapott minősítést' % NEVEK[f])
        # költségfájllal a (4) feltétel mért
        ut_k = os.path.join(mappa, 'koltseg_teszt.tsv')
        with open(ut_k, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# MANUAL: mock\n')
            f.write('szakasz\tosszeallitas\treteg\tmero\tertek\talso90\tfelso90\tmegjegyzes\n')
            f.write('vetites\t%s\tÖsszes\tkoltseg_usd\t30\t25\t45\tmock\n' % PAR)
        kfx = koltseg_felso(ut_k)
        ellen(kfx == {PAR: (30.0, 25.0, 45.0)}, 'a koltseg_felso nem olvassa a mock-fájlt: %s' % kfx)
        # hash-ellenőrzés: a módosított arany SystemExit, semmi nem íródik
        rossz = os.path.join(mappa, 'arany_rossz.jsonl')
        shutil.copyfile(info['arany_ut'], rossz)
        with open(rossz, 'a', encoding='utf-8', newline='\n') as f:
            f.write('{"vers":"x","parok":[],"betoldas":[],"forditatlan":[]}\n')
        shutil.copyfile(info['arany_sha'], os.path.join(mappa, 'arany_rossz.sha256'))
        ut_x = os.path.join(mappa, 'nem_irodik.tsv')
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fut(mappa, rossz, None, ut_x, os.path.join(mappa, 'nem_irodik.md'))
            ellen(False, 'az eltérő hash-ű arany nem állította meg a mérést')
        except SystemExit as e:
            ellen('sha256' in str(e) and not os.path.exists(ut_x), 'az eltérő hash hibaüzenete/mellékhatása hibás: %s' % e)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fut(mappa, rossz, os.path.join(mappa, 'nincs.sha256'), ut_x, os.path.join(mappa, 'nem_irodik.md'))
            ellen(False, 'a hiányzó hash-fájl nem állította meg a mérést')
        except SystemExit as e:
            ellen('hiányzik' in str(e), 'a hiányzó hash-fájl hibaüzenete hibás: %s' % e)
        # az arany útvonala paraméter: egy másik (rendben lévő) arany-másolat ugyanazt adja
        masik = os.path.join(mappa, 'masik_arany.jsonl')
        shutil.copyfile(info['arany_ut'], masik)
        shutil.copyfile(info['arany_sha'], os.path.join(mappa, 'masik_arany.sha256'))
        _, ainfo2, sk2, _, _ = szamol(mappa, masik, None, os.path.join(mappa, 'nincs_koltseg.tsv'), n_boot=50)
        ellen([s for s in sk2.lista if s[0] == 'feltetelek'] == [s for s in sk.lista if s[0] == 'feltetelek']
              and ainfo2['verzio'] == 'masik_arany.jsonl', 'az --arany paraméter nem érvényesül')
        # a repó alapértelmezett aranya (legfrissebb) létező, hash-ellenőrzött fájl
        jsonl, sha, verzio = tokenek.legfrissebb_arany()
        ellen(tokenek.hash_hiba(jsonl, sha) is None, 'a repó legfrissebb aranya (%s) hash-hibás' % verzio)
        onteszt_csak_c(mappa, info, ellen)
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('meres_p3c önteszt rendben (minősítés-logika mind az öt feltételre, pár-szintek és kapuhibás oldal, független '
          'újraszámolás a mock-adaton, determinizmus, hash-ellenőrzés, arany-paraméter, régi kimenetek bájtazonossága; '
          '--csak-c: nincs-adat jelölés, PD6-küszöbviszony, arany v2 → v3 hatás, F8V3 tájékoztató, SONNETV3-hiány)')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--arany', default=None, help='az arany jsonl-je (alap: a legfrissebb befagyasztott: v3, ha van, különben v2)')
    ap.add_argument('--arany-sha', default=None, help='a hash-fájl (alap: az --arany neve .sha256 kiterjesztéssel)')
    ap.add_argument('--forras-dir', default=None, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    ap.add_argument('--csak-c', action='store_true',
                    help='a C (F3V3) egyedüli mérése a Sonnet-adat nélkül (kimenet: meres_p3c_c_eredmeny.tsv, F21P_meres_p3c_c.md)')
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    if args.csak_c:
        return fut_c(args.forras_dir, args.arany, args.arany_sha)
    return fut(args.forras_dir, args.arany, args.arany_sha)


if __name__ == '__main__':
    sys.exit(main())
