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
    python eszkozok/karoli_strong/meres_p3c.py [--arany <jsonl> [--arany-sha <sha256-fájl>]]
                                               [--forras-dir <könyvtár>] [--onteszt]
"""

import argparse
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


def betolt(forras_dir=None, arany_ut=None, arany_sha=None):
    """(adat, arany_info). Az arany hash-ellenőrzése itt történik; hiba: SystemExit."""
    jsonl, sha, verzio = arany_forras(arany_ut, arany_sha)
    h = tokenek.hash_hiba(jsonl, sha, 'arany %s' % verzio)
    if h:
        raise SystemExit('HIBA: %s' % h)
    arany = {o['vers']: o for o in meres._jsonl(jsonl)}
    adat = meres.Adat(futasok=FUTASOK, forras_dir=forras_dir or F21P)
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
                  'a beállítás eltér: a Sonnet kikapcsolva, a C minimal/low (kötelező)')
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


def prompt_hatas(adat, sorok, n_boot=N_BOOT):
    """Sorok: 'hatas' (minden összevetés) és 'hatas_osszevetes' (a prompt-hatás az ingadozáshoz képest)."""
    osszevetesek = (('F3V3 − F3V2', [C2], C3), ('F3V3 − F3V2B', [C2B], C3),
                    ('F3V3 − átlag(F3V2, F3V2B)', [C2, C2B], C3), ('F3V2B − F3V2 (ingadozás)', [C2], C2B))
    adatok = {}
    for nev, refs, cel in osszevetesek:
        adatok[nev] = delta_adatok(adat, refs, cel, n_boot)
        for r, d in adatok[nev].items():
            for mero, (ref, cl, dl, lo, hi, ab, n) in d.items():
                sorok.add('hatas', nev, r, mero, '%.4f|%.4f|%.4f' % (ref, cl, dl), '%.4f|%.4f|%.4f' % (lo, hi, ab),
                          'ref|cél|Δ ; 90%%-os intervallum alsó|felső|a |Δ| 95. percentilise; n=%d' % n)
    hat = adatok['F3V3 − átlag(F3V2, F3V2B)']
    ing = adatok['F3V2B − F3V2 (ingadozás)']
    for r in hat:
        for mero, (ref, cl, dl, lo, hi, ab, n) in hat[r].items():
            fl = abs(ing[r][mero][2]) if r in ing else float('nan')
            kivul = abs(dl) > fl and (lo > 0 or hi < 0)
            sorok.add('hatas_osszevetes', 'F3V3 vs v2 átlag', r, mero, '%.4f|%.4f|%.4f|%.4f' % (ref, cl, dl, fl),
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
    feltetel['1'] = all(x and x[0] / x[1] >= 0.98 for x in mp)
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
        sorok.add('minosites', oss, meres.OSSZES, 'feltetel_%s' % k, {True: 'teljesül', False: 'nem teljesül', None: 'nem mért'}[v])
    for cimke, kulcsok in (('minosites (kizárás nélküli régi arannyal)', ('1', '2', '3', '4', '5')),
                           ('minosites (tájékoztató: 1Móz 6:17 kizárva)', ('1', '2', '3_tajekoztato', '4', '5'))):
        bukott = [k for k in kulcsok if feltetel[k] is False]
        nem_mert = [k for k in kulcsok if feltetel[k] is None]
        if bukott:
            e = 'nem felel meg'
        elif nem_mert:
            e = 'nem minősíthető (nem mért feltétel)'
        else:
            e = 'megfelel'
        sorok.add('minosites', oss, meres.OSSZES, cimke, e, '',
                  'bukott feltétel: %s; nem mért: %s' % (', '.join(bukott) or '—', ', '.join(nem_mert) or '—'))
    for r in meres.RETEGEK:
        m = _arany(sorok, oss, r, 'magas_pontossag')
        l = _arany(sorok, oss, r, 'lefedettseg')
        a = _arany(sorok, oss, r, 'alacsony_arany [200 vers]')
        g = _arany(sorok, oss, r, 'regi_arany_kizaras_nelkul')
        reszek = {'1': bool(m) and m[0] / m[1] >= 0.98, '2': bool(l) and l[0] / l[1] >= 0.95,
                  '3': (g[0] / g[1] >= 0.95) if g else None, '5': bool(a) and a[0] / a[1] <= 0.10}
        bukott = [k for k, v in reszek.items() if v is False]
        sorok.add('minosites_reteg', oss, r, 'reteg_feltetelek (1,2,3,5; a 4. összesen)',
                  'teljesül' if not bukott else 'nem teljesül', '',
                  'bukott: %s; (3) %s' % (', '.join(bukott) or '—', 'n.é. (nincs régi arany a rétegben)' if reszek['3'] is None else 'mért'))


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
            'két C-futással (F3V2, F3V2B), Sonnet+C pár (A=SONNETV3, B=F3V3, döntőbíró nélkül), 200 verses minta, arany %s '
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
          'alacsony arány n.é. Az A/B/C/Sonnet beállítása eltérő (a Sonnet gondolkodása kikapcsolva, a C-é minimal/low, kötelező). '
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
    ki.append('')
    with open(jelentes_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


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
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('meres_p3c önteszt rendben (minősítés-logika mind az öt feltételre, pár-szintek és kapuhibás oldal, független '
          'újraszámolás a mock-adaton, determinizmus, hash-ellenőrzés, arany-paraméter, régi kimenetek bájtazonossága)')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--arany', default=None, help='az arany jsonl-je (alap: a legfrissebb befagyasztott: v3, ha van, különben v2)')
    ap.add_argument('--arany-sha', default=None, help='a hash-fájl (alap: az --arany neve .sha256 kiterjesztéssel)')
    ap.add_argument('--forras-dir', default=None, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    return fut(args.forras_dir, args.arany, args.arany_sha)


if __name__ == '__main__':
    sys.exit(main())
