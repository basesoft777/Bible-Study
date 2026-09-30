#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.27 — P4 a P3b-adaton (prompt_v2): minden összeállítás az arany v2-höz.

Futások: F1V2 (A), F2V2 (B), F3V2 és F3V2B (C, két futás), F4V2 (C döntőbíró az
F1V2/F2V2 eltérő vagy kapuhibás versein), F5V2/F6V2 (A/B KJV nélkül, R1).
Nincs API-hívás. Az arany v2 befagyasztott (sha256-ellenőrzés).

Összeállítások és a G4 bizonyossági szabály (F22 brief 22.6, szó szerint):
  * magas:    A és B ugyanazt a linket adta (A∩B, mindkettő kapun átment), és a
              KJV-támpont nem mond ellent. A KJV-ellentmondás („a KJV ugyanazt a
              Strong-számot más angol szóhoz köti, mint amit a Károli-szó jelent”)
              a Károli-szó jelentésének ítéletét kívánja, gépileg nem
              értelmezhető: n.é. — a magas itt a KJV-feltétel nélküli A∩B.
  * kozepes:  a döntőbíró (C, F4V2) A vagy B egyikével egyezett: a C linkje az
              A és B közül pontosan az egyikben van (mindkettő kapun átment).
  * alacsony: hármas eltérés (a C linkje sem A-ban, sem B-ben), vagy a vers
              kapuhibás maradt (A vagy B végleg kapuhibás) — ekkor a C válasza
              kerül be, minden linkje alacsony (szó szerinti olvasat; nyitott tétel).
  A+B+C végső kimenet: az A=B verseken az A (mind magas); a döntőbíróhoz ment
  (F4V2) verseken a C válasza a fenti szintekkel; ha a C is kapuhibás, a versnek
  nincs kimenete (a lefedettség nevezőjében benne marad).
  A+B (egyezéses, döntőbíró nélkül; a jelentés értelmezése, nyitott tétel): a
  kimenet az A∪B a kapun átment modell(ek)ből; A∩B = magas, minden más link
  alacsony (G4: kozepes csak döntőbíróval létezik).
  Egymodelles összeállítás (A, B, C): a szintek nem értelmezettek (PD6); csak
  mért számok, minősítés nincs.

Az öt rögzített feltétel (Döntési szabály): (1) magas pontosság ≥ 98% minden
rétegben; (2) összes link lefedettsége ≥ 95%; (3) régi arany ≥ 95% (halmaz-
definíció; a MÉRT érték a kizárás nélküli, DT21 i; a kizárásos — csak az 1Móz
6:17 — TÁJÉKOZTATÓ, nem minősít); (4) a vetített költség
90%-os felső széle ≤ 60 USD (f21p/koltseg_vetites_p3b.tsv); (5) a vetített
alacsony arány ≤ 10% (link-arány a végső kimenetben; a 200 versen és az aranyon).
Minősítés (megfelel / nem felel meg) csak az A+B-re és az A+B+C-re.

A meglévő P4-mérőfüggvények (meres.pontossag, regi_arany, ab_egyezes, kapuhiba,
kjv_hatas, hibatipusok) változatlanul futnak egy „álneves” adaton (F1 -> F1V2,
F2 -> F2V2, F3 -> F3V2, F5 -> F5V2, F6 -> F6V2; az arany a v2).

Kimenet: f21p/meres_p3b_eredmeny.tsv, naplok/F21P_meres_p3b.md (generált). A
meres_eredmeny.tsv, meres_v2_eredmeny.tsv és a hozzájuk tartozó md nem változik.
    python eszkozok/karoli_strong/meres_p3b.py [--onteszt]
"""

import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meres  # noqa: E402
import tokenek  # noqa: E402

F21P = meres.F21P
EREDMENY_UT = os.path.join(F21P, 'meres_p3b_eredmeny.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_meres_p3b.md')
KOLTSEG_UT = os.path.join(F21P, 'koltseg_vetites_p3b.tsv')
P3B = ['F1V2', 'F2V2', 'F3V2', 'F3V2B', 'F4V2', 'F5V2', 'F6V2']
ALIAS = {'F1': 'F1V2', 'F2': 'F2V2', 'F3': 'F3V2', 'F5': 'F5V2', 'F6': 'F6V2'}
RETEGEK = meres.RETEGEK + [meres.OSSZES]
MAG = 20260930
N_BOOT = 1000
SZINTEK = ('magas', 'kozepes', 'alacsony')
OSSZEALLITASOK = ['A (F1V2)', 'B (F2V2)', 'C (F3V2)', 'C (F3V2B)', 'A+B', 'A+B+C']
MINOSITHETO = ('A+B', 'A+B+C')


# ---------------------------------------------------------------------------
# betöltés
# ---------------------------------------------------------------------------

def betolt():
    tokenek.arany_v2_befagyasztas_ellenoriz()
    v2 = {o['vers']: o for o in meres._jsonl(tokenek.ARANY_V2)}
    adat = meres.Adat(futasok=P3B)
    adat.arany = v2                      # minden arany_linkek hívás az arany v2-höz mér
    return adat


def alias_adat(adat):
    """Az adat másolata F1/F2/F3/F5/F6 kulcsokkal a meres.py függvényeihez."""
    import copy
    a = copy.copy(adat)
    a.futas = {k: adat.futas[v] for k, v in ALIAS.items()}
    a.kotegsorok = {k: adat.kotegsorok[v] for k, v in ALIAS.items()}
    visszafele = {v: k for k, v in ALIAS.items()}
    a.naplo = [dict(r, futas=visszafele[r['futas']]) for r in adat.naplo if r['futas'] in visszafele]
    return a


# ---------------------------------------------------------------------------
# G4: a végső kimenet és a szintek
# ---------------------------------------------------------------------------

def g4_vers(a_ok, b_ok, la, lb, c_ok, lc, dontobiro, alt=False):
    """Egy vers végső kimenete szintekkel: (abc, ab), mindkettő {link: szint}.

    a_ok/b_ok/c_ok: kapun átment-e; la/lb/lc: linkhalmazok (None, ha nem ok);
    dontobiro: a vers a döntőbíróhoz (F4V2) ment-e."""
    ab = {}
    if a_ok and b_ok:
        for l in la & lb:
            ab[l] = 'magas'
        for l in la ^ lb:
            ab[l] = 'alacsony'
    elif a_ok:
        ab = {l: 'alacsony' for l in la}
    elif b_ok:
        ab = {l: 'alacsony' for l in lb}
    abc = {}
    if a_ok and b_ok and la == lb:
        abc = {l: 'magas' for l in la}
    elif dontobiro and c_ok:
        for l in lc:
            if a_ok and b_ok:
                if l in la and l in lb:
                    abc[l] = 'magas'
                elif l in la or l in lb:
                    abc[l] = 'kozepes'
                else:
                    abc[l] = 'alacsony'
            elif alt and ((a_ok and l in la) or (b_ok and l in lb)):
                abc[l] = 'kozepes'       # alternatív olvasat: a C a túlélő modellel egyezik
            else:
                abc[l] = 'alacsony'      # a vers kapuhibás maradt: a C válasza, alacsony
    elif a_ok and b_ok:
        abc = {l: 'magas' for l in la & lb}   # a döntőbíró kapuhibás: csak a rögzített rész
    return abc, ab


def osszeallitas_kimenet(adat):
    """{ig: {'A+B': {link: szint}, 'A+B+C': {...}}} mind a 200 versre."""
    ki = {}
    for ig in adat.versek:
        a_ok, b_ok = adat.ok('F1V2', ig), adat.ok('F2V2', ig)
        c_ok = adat.ok('F4V2', ig)
        abc, ab = g4_vers(a_ok, b_ok, adat.linkek('F1V2', ig), adat.linkek('F2V2', ig),
                          c_ok, adat.linkek('F4V2', ig), ig in adat.futas['F4V2'])
        alt, _ = g4_vers(a_ok, b_ok, adat.linkek('F1V2', ig), adat.linkek('F2V2', ig),
                         c_ok, adat.linkek('F4V2', ig), ig in adat.futas['F4V2'], alt=True)
        ki[ig] = {'A+B': ab, 'A+B+C': abc, 'A+B+C (alt)': alt}
    return ki


# ---------------------------------------------------------------------------
# mérőszámok
# ---------------------------------------------------------------------------

class Sorok:
    def __init__(self):
        self.lista = []

    def add(self, szakasz, oss, reteg, mero, sz, nev='', megj=''):
        self.lista.append([szakasz, oss, reteg, mero, str(sz), str(nev), megj])


def _ret(adat, ig, ret):
    return ret == meres.OSSZES or adat.reteg[ig] == ret


def regi_osszeallitas(adat, kimenet_fn, ret, versek=None):
    """(hb, egyezik, hb_k, egyezik_k) a végső kimeneten; versek: a figyelembe vett versek."""
    hibas = meres.regi_hibas()
    hb = e = hbk = ek = 0
    for ig, szo, strong in adat.regi:
        if not _ret(adat, ig, ret) or (versek is not None and ig not in versek):
            continue
        _, egy = meres.regi_egyezik(adat, ig, szo, strong, kimenet_fn(ig))
        hb += 1
        e += egy
        if (ig, szo, strong) not in hibas:
            hbk += 1
            ek += egy
    return hb, e, hbk, ek


def egymodell(adat, sorok, nev, f):
    for ret in RETEGEK:
        arany_v = [ig for ig in adat.versek if ig in adat.arany and _ret(adat, ig, ret)]
        vs = [ig for ig in arany_v if adat.ok(f, ig)]
        t = sum(len(adat.linkek(f, ig) & adat.arany_linkek(ig)) for ig in vs)
        c = sum(len(adat.linkek(f, ig)) for ig in vs)
        g = sum(len(adat.arany_linkek(ig)) for ig in vs)
        sorok.add('feltetelek', nev, ret, 'arany_versek_kapun_atment', len(vs), len(arany_v))
        sorok.add('feltetelek', nev, ret, 'pontossag_osszes (tajekoztato, PD6)', t, c)
        sorok.add('feltetelek', nev, ret, 'lefedettseg', t, g, 'a kapun átment aranyverseken')
        ok_v = {ig for ig in adat.versek if adat.ok(f, ig)}
        hb, e, hbk, ek = regi_osszeallitas(adat, lambda ig: adat.linkek(f, ig), ret, ok_v)
        sorok.add('feltetelek', nev, ret, 'regi_arany_kizaras_nelkul', e, hb, 'MÉRT (DT21 i); kapun átment versek')
        sorok.add('feltetelek', nev, ret, 'regi_arany_kizarassal_tajekoztato', ek, hbk,
                  'TÁJÉKOZTATÓ (DT21 i): 1Móz 6:17 nélkül; kapun átment versek')
        sorok.add('feltetelek', nev, ret, 'magas_pontossag', 'n.é.', '', 'egymodelles (PD6)')
        sorok.add('feltetelek', nev, ret, 'alacsony_arany', 'n.é.', '', 'egymodelles (PD6)')


def tobbmodell(adat, sorok, kimenet):
    for oss in MINOSITHETO + ('A+B+C (alt)',):
        for ret in RETEGEK:
            arany_v = [ig for ig in adat.versek if ig in adat.arany and _ret(adat, ig, ret)]
            szint_t = {s: 0 for s in SZINTEK}
            szint_c = {s: 0 for s in SZINTEK}
            t = c = g = 0
            for ig in arany_v:
                k, gl = kimenet[ig][oss], adat.arany_linkek(ig)
                g += len(gl)
                for l, s in k.items():
                    c += 1
                    szint_c[s] += 1
                    if l in gl:
                        t += 1
                        szint_t[s] += 1
            sorok.add('feltetelek', oss, ret, 'arany_versek', len(arany_v), len(arany_v), 'minden aranyvers (a végső kimenet üres is lehet)')
            sorok.add('feltetelek', oss, ret, 'magas_pontossag', szint_t['magas'], szint_c['magas'],
                      'G4: A∩B; a KJV-ellentmondás feltétele gépileg n.é.')
            for s in ('kozepes', 'alacsony'):
                sorok.add('szintek', oss, ret, '%s_pontossag' % s, szint_t[s], szint_c[s])
            sorok.add('feltetelek', oss, ret, 'pontossag_osszes (tajekoztato)', t, c)
            sorok.add('feltetelek', oss, ret, 'lefedettseg', t, g, 'minden aranyvers')
            hb, e, hbk, ek = regi_osszeallitas(adat, lambda ig: set(kimenet[ig][oss]), ret)
            sorok.add('feltetelek', oss, ret, 'regi_arany_kizaras_nelkul', e, hb, 'MÉRT (DT21 i); a végső kimeneten, 200 vers')
            sorok.add('feltetelek', oss, ret, 'regi_arany_kizarassal_tajekoztato', ek, hbk,
                      'TÁJÉKOZTATÓ (DT21 i): 1Móz 6:17 nélkül; a végső kimeneten, 200 vers')
            for halmaz, vs in (('200 vers', [ig for ig in adat.versek if _ret(adat, ig, ret)]), ('arany', arany_v)):
                osz = sum(len(kimenet[ig][oss]) for ig in vs)
                ala = sum(1 for ig in vs for s in kimenet[ig][oss].values() if s == 'alacsony')
                sorok.add('feltetelek', oss, ret, 'alacsony_arany [%s]' % halmaz, ala, osz, 'link-arány a végső kimenetben')
                for s in SZINTEK:
                    sorok.add('szintek', oss, ret, 'eloszlas_%s [%s]' % (s, halmaz),
                              sum(1 for ig in vs for x in kimenet[ig][oss].values() if x == s), osz)
                ures = sum(1 for ig in vs if not kimenet[ig][oss])
                sorok.add('szintek', oss, ret, 'kimenet_nelkuli_versek [%s]' % halmaz, ures, len(vs))


def c_ingadozas(adat, sorok):
    """F3V2 vs F3V2B: azonos prompt, a különbség a futásközi ingadozás becslése."""
    rnd = random.Random(MAG)
    fa, fb = 'F3V2', 'F3V2B'
    arany_v = [ig for ig in adat.versek if ig in adat.arany and adat.ok(fa, ig) and adat.ok(fb, ig)]
    per = {ig: {f: (len(adat.linkek(f, ig) & adat.arany_linkek(ig)), len(adat.linkek(f, ig)), len(adat.arany_linkek(ig)))
                for f in (fa, fb)} for ig in arany_v}
    kapu = {}
    for f in (fa, fb):
        _, _, elso = meres.hibatipusok(adat, f)
        kapu[f] = {ig: (ig in elso, not adat.ok(f, ig)) for ig in adat.versek}

    def merok(vs):
        o = {}
        for f in (fa, fb):
            t, c, g = (sum(per[ig][f][i] for ig in vs) for i in range(3))
            o[f] = (t / c if c else 0.0, t / g if g else 0.0)
        return o

    def kmerok(vs):
        return {f: (sum(kapu[f][ig][0] for ig in vs) / len(vs), sum(kapu[f][ig][1] for ig in vs) / len(vs)) for f in kapu}

    sa = {r: [ig for ig in arany_v if adat.reteg[ig] == r] for r in meres.RETEGEK}
    s2 = {r: [ig for ig in adat.versek if adat.reteg[ig] == r] for r in meres.RETEGEK}
    boot = {r: [] for r in RETEGEK}
    for _ in range(N_BOOT):
        ma = {r: [s[rnd.randrange(len(s))] for _ in s] for r, s in sa.items()}
        m2 = {r: [s[rnd.randrange(len(s))] for _ in s] for r, s in s2.items()}
        for r in RETEGEK:
            va = sum(ma.values(), []) if r == meres.OSSZES else ma[r]
            v2_ = sum(m2.values(), []) if r == meres.OSSZES else m2[r]
            m, k = merok(va), kmerok(v2_)
            boot[r].append((m[fb][0] - m[fa][0], m[fb][1] - m[fa][1], k[fb][0] - k[fa][0], k[fb][1] - k[fa][1]))
    for r in RETEGEK:
        va = [ig for ig in arany_v if _ret(adat, ig, r)]
        v2_ = [ig for ig in adat.versek if _ret(adat, ig, r)]
        m, k = merok(va), kmerok(v2_)
        ertek = [(m[fa][0], m[fb][0], 'pontossag'), (m[fa][1], m[fb][1], 'lefedettseg'),
                 (k[fa][0], k[fb][0], 'kapuhiba_elso_probara'), (k[fa][1], k[fb][1], 'kapuhiba_vegleg')]
        for i, (x, y, nev) in enumerate(ertek):
            b = sorted(q[i] for q in boot[r])
            ab = sorted(abs(q[i]) for q in boot[r])
            sorok.add('c_ingadozas', 'F3V2 vs F3V2B', r, nev, '%.4f|%.4f|%.4f' % (x, y, y - x),
                      '%.4f|%.4f|%.4f' % (b[int(0.05 * len(b))], b[int(0.95 * len(b)) - 1], ab[int(0.95 * len(ab)) - 1]),
                      'F3V2|F3V2B|Δ ; 90%%-os intervallum alsó|felső|a |Δ| 95. percentilise; n=%d' % (len(va) if i < 2 else len(v2_)))
        for halmaz, vs0 in (('arany', arany_v), ('minta', [ig for ig in adat.versek if adat.ok(fa, ig) and adat.ok(fb, ig)])):
            vs = [ig for ig in vs0 if _ret(adat, ig, r)]
            az = sum(1 for ig in vs if adat.linkek(fa, ig) == adat.linkek(fb, ig))
            mm = sum(len(adat.linkek(fa, ig) & adat.linkek(fb, ig)) for ig in vs)
            uu = sum(len(adat.linkek(fa, ig) | adat.linkek(fb, ig)) for ig in vs)
            sorok.add('c_ingadozas', 'F3V2 vs F3V2B', r, 'azonos_linkhalmazu_versek [%s]' % halmaz, az, len(vs))
            sorok.add('c_ingadozas', 'F3V2 vs F3V2B', r, 'link_egyezes [%s]' % halmaz, mm, uu, 'Σ|∩|/Σ|∪|')


def hibatipusok_teljes(ad, f):
    """Mint a meres.hibatipusok, de a döntőbírói futásnál (F4V2) az első próbálkozás nyers
    válaszát a TELJES kapun ellenőrzi: az ötpontos kapu + a 6. pont (az A–B rögzítés,
    futtat.biro_kenyszer, az A és B végleges válaszaiból számolt rögzítéssel), ahogy a
    futtató a futáskor tette (futtat.valasz_ellenoriz_futashoz). F21.31."""
    import futtat
    if futtat.FUTASOK.get(f, {}).get('tipus') != 'biro':
        return meres.hibatipusok(ad, f)
    elso, vegleg = {}, {}
    elso_h = set()
    for sor in ad.kotegsorok[f]:
        r1 = futtat.valasz_ellenoriz_futashoz(f, sor['nyers'][0], sor['igehelyek'], F21P)
        for ig in sor['igehelyek']:
            if not r1[ig]['ok']:
                elso_h.add(ig)
                for t in meres._tipusok(r1[ig]['hibak']):
                    elso[t] = elso.get(t, 0) + 1
            v = sor['versek'][ig]
            if v['allapot'] != 'ok':
                for t in meres._tipusok(v['hibak']):
                    vegleg[t] = vegleg.get(t, 0) + 1
    return elso, vegleg, elso_h


def kapuhiba_v1_v2(sorok):
    """v1 (F1, F2, F3, F5, F6) és v2 (F1V2, F2V2, F3V2, F3V2B, F5V2, F6V2) kapuhibája és hibatípusai."""
    adat1 = meres.Adat()
    adat2 = meres.Adat(futasok=P3B)
    parok = [('A', 'F1', 'F1V2'), ('B', 'F2', 'F2V2'), ('C', 'F3', 'F3V2'), ('C (2. futás)', None, 'F3V2B'),
             ('A KJV nélkül', 'F5', 'F5V2'), ('B KJV nélkül', 'F6', 'F6V2'), ('C döntőbíró', None, 'F4V2')]
    for nev, f1, f2 in parok:
        for verzio, ad, f in (('v1', adat1, f1), ('v2', adat2, f2)):
            if f is None:
                continue
            elso, vegleg, elso_h = hibatipusok_teljes(ad, f)
            p2 = {ig for ig, r in ad.futas[f].items() if r['probalkozas'] == 2}
            naplo_p1 = sum(int(r['kapuhiba_db']) for r in ad.naplo if r['futas'] == f and r['probalkozas'] == '1')
            egyezik = elso_h == p2 and len(elso_h) == naplo_p1
            sorok.add('kapuhiba_kereszt', '%s %s (%s)' % (nev, verzio, f), meres.OSSZES, 'keresztellenorzes_elso_probalkozas',
                      len(elso_h), naplo_p1, 'újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek (%d) = napló '
                      'kapuhiba_db(probalkozas=1) összeg (%d): %s' % (len(p2), naplo_p1, 'EGYEZIK' if egyezik else 'ELTÉR'))
            for ret in RETEGEK:
                vs = [ig for ig in ad.versek if ig in ad.futas[f] and _ret(ad, ig, ret)]
                if not vs:
                    continue
                sorok.add('kapuhiba', '%s %s (%s)' % (nev, verzio, f), ret, 'elso_probara', sum(1 for ig in vs if ig in elso_h), len(vs))
                sorok.add('kapuhiba', '%s %s (%s)' % (nev, verzio, f), ret, 'vegleg', sum(1 for ig in vs if not ad.ok(f, ig)), len(vs))
            n = len(ad.futas[f])
            for p in sorted(set(elso) | set(vegleg)):
                sorok.add('kapuhiba_tipus', '%s %s (%s)' % (nev, verzio, f), meres.OSSZES, 'kapupont_%s_elso' % p, elso.get(p, 0), n)
                sorok.add('kapuhiba_tipus', '%s %s (%s)' % (nev, verzio, f), meres.OSSZES, 'kapupont_%s_vegleg' % p, vegleg.get(p, 0), n)


def mentett_ellenorzes(sorok):
    """A mentett (allapot=ok) válaszok újraellenőrzése a teljes kapun (futtat.mentett_valaszok_ellenoriz):
    ötpontos kapu, az F4V2-nél a 6. pont (rögzítés) is."""
    import futtat
    for f in P3B:
        h = futtat.mentett_valaszok_ellenoriz(f, F21P)
        sorok.add('mentett_ellenorzes', f, meres.OSSZES, 'hibak', len(h), '',
                  'futtat.mentett_valaszok_ellenoriz: %s' % ('0 hiba' if not h else '; '.join(h[:5])))


def meglevo_merok(adat, sorok):
    """A meres.py P4-függvényei az álneves v2-adaton (A=F1V2, B=F2V2, C=F3V2; arany v2)."""
    a = alias_adat(adat)
    s = meres.Sorok()
    meres.pontossag(a, s)
    meres.ab_egyezes(a, s)
    meres.ab_osszeallitas(a, s)
    meres.kjv_hatas(a, s)
    for r in s.lista:
        if r['szakasz'] in ('pontossag_lefedettseg', 'ab_egyezes', 'ab_osszeallitas', 'kjv_hatas'):
            oss = r['osszeallitas']
            for k, v in (('F1/F2', 'F1V2/F2V2'), ('F5/F6', 'F5V2/F6V2')):
                oss = oss.replace(k, v)
            sorok.add('p4_' + r['szakasz'], oss, r['reteg'], r['mero'], r['szamlalo'], r['nevezo'], r['megjegyzes'])


# ---------------------------------------------------------------------------
# minősítés (csak A+B, A+B+C)
# ---------------------------------------------------------------------------

def koltseg_felso():
    """{osszeallitas: (ertek, also90, felso90)} a koltseg_vetites_p3b.tsv-ből (Összes), ha van."""
    if not os.path.exists(KOLTSEG_UT):
        return {}
    ki = {}
    with open(KOLTSEG_UT, encoding='utf-8') as f:
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


def minosit(sorok):
    kf = koltseg_felso()
    for oss in MINOSITHETO:
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
        # rétegenként (a vegyes összeállításhoz): (1), (2), (5) rétegben; (3) csak ahol van régi arany; (4) összesen
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


def kiir(sorok, ts):
    fej = ('GENERÁLT: eszkozok/karoli_strong/meres_p3b.py | scope=P3b (prompt_v2): A=F1V2, B=F2V2, C=F3V2 és F3V2B, '
           'A+B, A+B+C (F4V2), KJV nélkül F5V2/F6V2; arany v2 (60 vers), 200 verses minta | forras=f21p/valaszok/'
           '{F1V2,F2V2,F3V2,F3V2B,F4V2,F5V2,F6V2}.jsonl, f21p/valaszok/{F1,F2,F3,F5,F6}.jsonl (v1-kapuhiba), '
           'f21p/arany_opus_v2.jsonl (sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, '
           'konkordancia/Karoli_Strong_kivonat.tsv, f21p/futasnaplo.tsv, f21p/koltseg_vetites_p3b.tsv | ts=%s '
           '(a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos' % ts)
    with open(EREDMENY_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# ' + fej + '\n')
        f.write('\t'.join(['szakasz', 'osszeallitas', 'reteg', 'mero', 'szamlalo', 'nevezo', 'megjegyzes']) + '\n')
        for s in sorok.lista:
            assert all('\t' not in x for x in s)
            f.write('\t'.join(s) + '\n')
    ki = ['# F21P_meres_p3b.md — P4 a P3b-adaton (prompt_v2), minden összeállítás, arany v2', '',
          '<!-- %s -->' % fej, '',
          'Kizárólag szkriptkimenet. A G4 szabály szó szerint (F22 brief 22.6): magas = A∩B (a KJV-ellentmondás '
          'feltétele gépileg n.é.); kozepes = a C döntőbíró linkje A vagy B egyikében; alacsony = hármas eltérés, '
          'vagy a vers kapuhibás maradt (A vagy B végleg kapuhibás: a C válasza, minden link alacsony). Az A+B '
          '(döntőbíró nélkül): A∩B magas, minden más link alacsony — a jelentés értelmezése. Egymodelles '
          'összeállítás (A, B, C) nem minősíthető (PD6). Cellaforma: érték (számláló/nevező).', '']

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

    ki += ['## a) Az öt feltétel összeállításonként és rétegenként', '']
    ki += tabla('feltetelek', ['arany_versek_kapun_atment', 'arany_versek', 'magas_pontossag', 'pontossag_osszes (tajekoztato, PD6)',
                               'pontossag_osszes (tajekoztato)', 'lefedettseg', 'regi_arany_kizaras_nelkul',
                               'regi_arany_kizarassal_tajekoztato', 'alacsony_arany', 'alacsony_arany [200 vers]', 'alacsony_arany [arany]'],
                OSSZEALLITASOK)
    kf = koltseg_felso()
    ki += ['(4) vetített költség, teljes Biblia (f21p/koltseg_vetites_p3b.tsv, 90%; a bootstrap egysége a köteg — DT21 f: elfogadva, felhasználói döntés):', '']
    for o in OSSZEALLITASOK:
        if o in kf:
            ki.append('- %s: %.2f USD [%.2f–%.2f]' % (o, *kf[o]))
    ki += ['', '## b) Minősítés (csak A+B és A+B+C; a többi PD6 szerint nem minősíthető)', '',
           '| összeállítás | feltétel | eredmény | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'minosites':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[3], s[4], s[6]))
    ki += ['', '| összeállítás | réteg | rétegfeltételek (1, 2, 3, 5) | megjegyzés |', '|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'minosites_reteg':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[2], s[4], s[6]))
    ki += ['', '## c) Bizonyossági szintek (A+B, A+B+C)', '']
    ki += tabla('szintek', ['kozepes_pontossag', 'alacsony_pontossag'] + ['eloszlas_%s [%s]' % (x, h) for h in ('200 vers', 'arany') for x in SZINTEK]
                + ['kimenet_nelkuli_versek [200 vers]', 'kimenet_nelkuli_versek [arany]'], MINOSITHETO)
    ki += ['## d) A meres.py P4-mérőszámai a v2-adaton (A=F1V2, B=F2V2, C=F3V2, arany v2)', '']
    for sz, cim in (('p4_pontossag_lefedettseg', 'pontosság és lefedettség'), ('p4_ab_egyezes', 'A–B egyezés'),
                    ('p4_ab_osszeallitas', 'A+B összeállítás, döntőbíróhoz menő versek'), ('p4_kjv_hatas', 'KJV-hatás (F1V2/F2V2 vs F5V2/F6V2, R1)')):
        osszk = []
        merok = []
        for s in sorok.lista:
            if s[0] == sz:
                if s[1] not in osszk:
                    osszk.append(s[1])
                if s[3] not in merok:
                    merok.append(s[3])
        ki += ['### %s' % cim, ''] + tabla(sz, merok, osszk)
    ki += ['## e) A C két futása (F3V2 vs F3V2B, azonos prompt): futásközi ingadozás', '',
           'A két futás konfigurációja azonos (prompt_v2, C, 200 vers), ezért a különbség a futásközi ingadozás '
           'becslése (egyetlen futáspárból; a bootstrap a versminta bizonytalanságát adja hozzá, a futás többszöri '
           'megismétlésének eloszlását nem helyettesíti).', '',
           '| réteg | mérőszám | F3V2 | F3V2B | Δ | Δ 90% | |Δ| 95. percentilis | n |', '|---|---|---|---|---|---|---|---|']
    for s in sorok.lista:
        if s[0] == 'c_ingadozas' and '|' in s[4]:
            x, y, d = (float(v) for v in s[4].split('|'))
            lo, hi, ab = (float(v) for v in s[5].split('|'))
            ki.append('| %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp | %s |' % (
                s[2], s[3], 100 * x, 100 * y, 100 * d, 100 * lo, 100 * hi, 100 * ab, s[6].split('n=')[-1]))
    ki += [''] + tabla('c_ingadozas', ['azonos_linkhalmazu_versek [arany]', 'link_egyezes [arany]',
                                       'azonos_linkhalmazu_versek [minta]', 'link_egyezes [minta]'], ['F3V2 vs F3V2B'])
    ki += ['## f) Kapuhiba: v1 és v2 egymás mellett, hibatípusok kapupont szerint', '']
    oss_k = []
    for s in sorok.lista:
        if s[0] == 'kapuhiba' and s[1] not in oss_k:
            oss_k.append(s[1])
    ki += tabla('kapuhiba', ['elso_probara', 'vegleg'], oss_k)
    merok_t = []
    for s in sorok.lista:
        if s[0] == 'kapuhiba_tipus' and s[3] not in merok_t:
            merok_t.append(s[3])
    ki += tabla('kapuhiba_tipus', merok_t, oss_k)
    ki += ['A döntőbírói futás (F4V2) első próbás kapuhibája a teljes kapun számolva: ötpontos kapu + 6. pont (az A–B '
           'rögzítés, futtat.biro_kenyszer), ahogy a futtató a futáskor ellenőrizte.', '',
           '| futás | keresztellenőrzés (első próbás hibás versek) |', '|---|---|']
    for s_ in sorok.lista:
        if s_[0] == 'kapuhiba_kereszt':
            ki.append('| %s | %s |' % (s_[1], s_[6]))
    ki += ['', '| futás | mentett válaszok újraellenőrzése (hibák) |', '|---|---|']
    for s_ in sorok.lista:
        if s_[0] == 'mentett_ellenorzes':
            ki.append('| %s | %s — %s |' % (s_[1], s_[4], s_[6]))
    ki.append('')
    with open(JELENTES_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def fut():
    adat = betolt()
    sorok = Sorok()
    kimenet = osszeallitas_kimenet(adat)
    for nev, f in (('A (F1V2)', 'F1V2'), ('B (F2V2)', 'F2V2'), ('C (F3V2)', 'F3V2'), ('C (F3V2B)', 'F3V2B')):
        egymodell(adat, sorok, nev, f)
    tobbmodell(adat, sorok, kimenet)
    minosit(sorok)
    c_ingadozas(adat, sorok)
    kapuhiba_v1_v2(sorok)
    mentett_ellenorzes(sorok)
    meglevo_merok(adat, sorok)
    kiir(sorok, tokenek.generalas_ts())
    print('kész: %d sor -> %s, %s' % (len(sorok.lista), EREDMENY_UT, JELENTES_UT))
    for s in sorok.lista:
        if s[0] == 'minosites':
            print('  %s | %s | %s | %s' % (s[1], s[3], s[4], s[6]))
    return 0


# ---------------------------------------------------------------------------
# önteszt (mock, determinisztikus)
# ---------------------------------------------------------------------------

def onteszt():
    hibak = []
    A = {(1, 1), (2, 2), (3, 3)}
    B = {(1, 1), (2, 2), (3, 4)}
    C = {(1, 1), (2, 2), (3, 3), (4, 5)}
    abc, ab = g4_vers(True, True, A, B, True, C, True)
    if abc != {(1, 1): 'magas', (2, 2): 'magas', (3, 3): 'kozepes', (4, 5): 'alacsony'}:
        hibak.append('G4 A+B+C: %s' % abc)
    if ab != {(1, 1): 'magas', (2, 2): 'magas', (3, 3): 'alacsony', (3, 4): 'alacsony'}:
        hibak.append('G4 A+B: %s' % ab)
    abc, ab = g4_vers(False, True, None, B, True, C, True)
    if set(abc.values()) != {'alacsony'} or set(ab.values()) != {'alacsony'} or set(ab) != B:
        hibak.append('G4 kapuhibás A: %s / %s' % (abc, ab))
    abc, ab = g4_vers(True, True, A, A, False, None, False)
    if abc != {l: 'magas' for l in A} or ab != {l: 'magas' for l in A}:
        hibak.append('G4 A=B: %s / %s' % (abc, ab))
    abc, _ = g4_vers(True, True, A, B, False, None, True)
    if abc != {(1, 1): 'magas', (2, 2): 'magas'}:
        hibak.append('G4 döntőbíró kapuhibás: %s' % abc)
    abc, ab = g4_vers(False, False, None, None, True, C, True)
    if set(abc.values()) != {'alacsony'} or ab:
        hibak.append('G4 mindkettő kapuhibás: %s / %s' % (abc, ab))
    # minősítés-logika egy mock sorlistán
    s = Sorok()
    for oss in MINOSITHETO:
        for r in meres.RETEGEK + [meres.OSSZES]:
            s.add('feltetelek', oss, r, 'magas_pontossag', 99, 100)
            s.add('feltetelek', oss, r, 'lefedettseg', 96, 100)
            s.add('feltetelek', oss, r, 'regi_arany_kizaras_nelkul', 30, 32)
            s.add('feltetelek', oss, r, 'regi_arany_kizarassal_tajekoztato', 30, 30)
            s.add('feltetelek', oss, r, 'alacsony_arany [200 vers]', 5, 100)
    minosit(s)
    m = {(x[1], x[3]): x[4] for x in s.lista if x[0] == 'minosites'}
    if m[('A+B', 'minosites (kizárás nélküli régi arannyal)')] != 'nem felel meg' or m[('A+B', 'feltetel_3')] != 'nem teljesül':
        hibak.append('minősítés: a 30/32 régi arany nem buktat: %s' % m)
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('meres_p3b önteszt rendben (G4: 6 mock eset, minősítés-logika)')
    return 0


if __name__ == '__main__':
    sys.exit(onteszt() if '--onteszt' in sys.argv else fut())
