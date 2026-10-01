#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.67 — KJV-mérés: az F8V3 (C, prompt_v3, 200 vers, a TELJES KJV-táblából kapott KJV-támponttal
minden rétegben, ahol van) az F3V3-mal szemben (C, prompt_v3, KJV csak az R1-en, a régi
Genesis/Exodus/Proverbs táblából). Nincs API-hívás, nincs titok.

Futások: F3V3 (referencia), F8V3 (cél), F3V2 és F3V2B (azonos prompt_v2, azonos bemenet: a
futásközi ingadozás becslése, az arany v3-ra mérve). A mérés az arany v3-ra megy
(f21p/arany_opus_v3.jsonl, hash-ellenőrzéssel: eltérésnél / hiányzó hash-fájlnál SystemExit,
semmi nem íródik); a link = (magyar sorszám, eredeti sorszám); a f21p/meres_kizaras.tsv tokenjei
mindkét oldalról kimaradnak (PD7), mint a többi mérőben.

Mérőszámok (rétegenként R1–R4, R2+R3 és Összes; minden cellában számláló/nevező):
  (a) PONTOSSÁG: a kimenet linkjeiből hány van az aranyban; (b) LEFEDETTSÉG: az arany linkjeiből
      hány van a kimenetben — a kapun átment (allapot=ok) aranyverseken. „sajat”: a futás saját
      halmaza; „kozos”: az a halmaz, ahol az összevetett két futás MINDKETTŐ átment (ezen megy a Δ).
  (c) KAPUHIBA első próbára (a nyers[0] újraellenőrzése a teljes kapun) és végleg, a 200 versen;
      keresztellenőrzés a jsonl probalkozas=2 verseivel és a napló kapuhiba_db összegével.
  (d) régi arany egyezés (halmaz-definíció; MÉRT = kizárás nélküli; tájékoztató: 1Móz 6:17 kizárva).
  (e) Δ = F8V3 − F3V3 rétegenként és összesen; páros bootstrap a versek felett (1 000 újramintavétel,
      mag 20260930, rétegzett: az újramintavétel rétegen belül, a két futás ugyanazt a mintát kapja);
      90%-os intervallum (5. és 95. percentilis). Összevetés az ingadozás-becsléssel (F3V2B − F3V2,
      ugyanazok a mérőszámok, ugyanaz a bootstrap): két leíró jelölés külön — „az intervallum nem
      tartalmazza a 0-t” és „|Δ| > |F3V2B − F3V2|”; nem szignifikanciapróba.
  (f) ÉRINTETT linkek és szavak (az aranyversek, ahol mindkét futás átment): link-szint (hiány
      pótolva / többlet megszűnt / hiány új / többlet új) és szó-szint (egy magyar szó linkhalmaza
      pontosan az arany: javult = F3V3-ban nem, F8V3-ban igen; romlott = fordítva).
  (g) költség és tokenek a futásnaplóból (az F8V3 baleseti két kötegével együtt, jelölve),
  (h) a KJV-sor hossza a bemenetben (karakter/vers, karakter/köteg), (i) verszintű egyezés.

Kimenet (a régi mérők kimenetei bájtra változatlanok): f21p/kjv_meres_eredmeny.tsv és
naplok/F21P_kjv_meres.md; a fejléc a proveniencia: scope | forras | ts. A számok csak a szkript
kimenetéből valók; a jelentés nem von le következtetést, csak a számokat és az olvasási korlátokat adja.

    python eszkozok/karoli_strong/meres_kjv.py [--arany <jsonl> [--arany-sha <sha256-fájl>]]
                                               [--forras-dir <könyvtár>] [--onteszt]
"""

import argparse
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kapu  # noqa: E402
import meres  # noqa: E402
import meres_p3b  # noqa: E402
import meres_p3c  # noqa: E402
import tokenek  # noqa: E402

F21P = meres.F21P
ARANY_UT = os.path.join(F21P, 'arany_opus_v3.jsonl')
ARANY_SHA = os.path.join(F21P, 'arany_opus_v3.sha256')
EREDMENY_UT = os.path.join(F21P, 'kjv_meres_eredmeny.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_kjv_meres.md')
REF, CEL, Z1, Z2 = 'F3V3', 'F8V3', 'F3V2', 'F3V2B'
FUTASOK = [REF, CEL, Z1, Z2]
KJV_FORRAS = {REF: 'regi', CEL: 'teljes'}
BALESET_KOTEGEK = ('1', '2')          # naplok/F21_baleset_F8V3.md: az F8V3 első két kötege helyi balesetből
MAG = 20260930
N_BOOT = 1000
CSOPORTOK = [('R1', ['R1']), ('R2', ['R2']), ('R3', ['R3']), ('R2+R3', ['R2', 'R3']), ('R4', ['R4']),
             (meres.OSSZES, ['R1', 'R2', 'R3', 'R4'])]
CSOP = dict(CSOPORTOK)
CSOP_NEVEK = [n for n, _ in CSOPORTOK]
RETEGEK = meres.RETEGEK
MEROK_DELTA = ('pontossag', 'lefedettseg', 'kapuhiba_elso_probara', 'kapuhiba_vegleg')
Sorok = meres_p3b.Sorok


# ---------------------------------------------------------------------------
# betöltés (arany v3, hash-ellenőrzéssel)
# ---------------------------------------------------------------------------

def betolt(forras_dir=None, arany_ut=None, arany_sha=None):
    """(adat, info). Az arany hash-ellenőrzése itt történik; hiba: SystemExit."""
    jsonl = arany_ut or ARANY_UT
    sha = arany_sha or (os.path.splitext(jsonl)[0] + '.sha256' if arany_ut else ARANY_SHA)
    h = tokenek.hash_hiba(jsonl, sha, 'arany %s' % os.path.basename(jsonl))
    if h:
        raise SystemExit('HIBA: %s' % h)
    adat = meres.Adat(futasok=FUTASOK, forras_dir=forras_dir or F21P)
    adat.arany = {o['vers']: o for o in meres._jsonl(jsonl)}
    info = {'jsonl': jsonl, 'sha_fajl': sha, 'verzio': os.path.basename(jsonl), 'sha256': tokenek.sha256_lf(jsonl),
            'aranyversek': len(adat.arany)}
    return adat, info


def csop_versek(adat, nev, lista=None):
    st = CSOP[nev]
    return [ig for ig in (adat.versek if lista is None else lista) if adat.reteg[ig] in st]


# ---------------------------------------------------------------------------
# (a), (b) pontosság, lefedettség
# ---------------------------------------------------------------------------

def pont_lef(adat, sorok, futasok=FUTASOK):
    """'sajat': a futás saját (kapun átment) aranyverseken."""
    for f in futasok:
        for cs in CSOP_NEVEK:
            av = [ig for ig in csop_versek(adat, cs) if ig in adat.arany]
            vs = [ig for ig in av if adat.ok(f, ig)]
            t = sum(len(adat.linkek(f, ig) & adat.arany_linkek(ig)) for ig in vs)
            c = sum(len(adat.linkek(f, ig)) for ig in vs)
            g = sum(len(adat.arany_linkek(ig)) for ig in vs)
            sorok.add('sajat', f, cs, 'arany_versek_kapun_atment', len(vs), len(av))
            sorok.add('sajat', f, cs, 'pontossag', t, c, 'a kimenet linkjeiből az aranyban')
            sorok.add('sajat', f, cs, 'lefedettseg', t, g, 'az arany linkjeiből a kimenetben')


def kozos_pont_lef(adat, sorok, parok):
    """'kozos': az a halmaz, ahol a pár mindkét futása átment (ezen a halmazon megy a Δ)."""
    for fa, fb in parok:
        for f in (fa, fb):
            for cs in CSOP_NEVEK:
                av = [ig for ig in csop_versek(adat, cs) if ig in adat.arany]
                vs = [ig for ig in av if adat.ok(fa, ig) and adat.ok(fb, ig)]
                t = sum(len(adat.linkek(f, ig) & adat.arany_linkek(ig)) for ig in vs)
                c = sum(len(adat.linkek(f, ig)) for ig in vs)
                g = sum(len(adat.arany_linkek(ig)) for ig in vs)
                oss = '%s [pár: %s–%s]' % (f, fa, fb)
                sorok.add('kozos', oss, cs, 'arany_versek_mindketto_atment', len(vs), len(av))
                sorok.add('kozos', oss, cs, 'pontossag', t, c)
                sorok.add('kozos', oss, cs, 'lefedettseg', t, g)


# ---------------------------------------------------------------------------
# (c) kapuhiba
# ---------------------------------------------------------------------------

def kapu_elso(adat, f):
    """{igehely: {kapupont-típus}} az ELSŐ nyers válasz teljes-kapus újraellenőrzéséből (csak a hibás versek)."""
    ki = {}
    for sor in adat.kotegsorok[f]:
        r1 = kapu.valasz_ellenoriz(sor['nyers'][0], sor['igehelyek'])
        for ig in sor['igehelyek']:
            if not r1[ig]['ok']:
                ki[ig] = meres._tipusok(r1[ig]['hibak'])
    return ki


def kapu_vegleg(adat, f):
    ki = {}
    for sor in adat.kotegsorok[f]:
        for ig in sor['igehelyek']:
            v = sor['versek'][ig]
            if v['allapot'] != 'ok':
                ki[ig] = meres._tipusok(v['hibak'])
    return ki


def kapuhiba(adat, sorok, futasok=FUTASOK):
    for f in futasok:
        elso, vegleg = kapu_elso(adat, f), kapu_vegleg(adat, f)
        _, _, elso_h = meres.hibatipusok(adat, f)
        p2 = {ig for ig, r in adat.futas[f].items() if r['probalkozas'] == 2}
        naplo_p1 = sum(int(r['kapuhiba_db']) for r in adat.naplo if r['futas'] == f and r['probalkozas'] == '1')
        egyezik = set(elso) == elso_h == p2 and len(elso_h) == naplo_p1
        sorok.add('kapuhiba_kereszt', f, meres.OSSZES, 'keresztellenorzes_elso_probalkozas', len(elso_h), naplo_p1,
                  'újraszámolt első-próbás hibás versek (%d) = jsonl probalkozas=2 versek (%d) = napló kapuhiba_db(probalkozas=1) '
                  'összeg (%d): %s' % (len(elso_h), len(p2), naplo_p1, 'EGYEZIK' if egyezik else 'ELTÉR'))
        for cs in CSOP_NEVEK:
            vs = [ig for ig in csop_versek(adat, cs) if ig in adat.futas[f]]
            sorok.add('kapuhiba', f, cs, 'elso_probara', sum(1 for ig in vs if ig in elso), len(vs))
            sorok.add('kapuhiba', f, cs, 'vegleg', sum(1 for ig in vs if ig in vegleg), len(vs))
            for p in sorted({p for t in list(elso.values()) + list(vegleg.values()) for p in t}):
                sorok.add('kapuhiba_tipus', f, cs, 'kapupont_%s_elso' % p, sum(1 for ig in vs if p in elso.get(ig, ())), len(vs),
                          'hibás versek ezzel a kapuponttal (egy vers több ponton is hibázhat)')
                sorok.add('kapuhiba_tipus', f, cs, 'kapupont_%s_vegleg' % p, sum(1 for ig in vs if p in vegleg.get(ig, ())), len(vs))
        for ig in sorted(vegleg, key=adat.versek.index):
            sorok.add('kapuhiba_vegleges_versek', f, adat.reteg[ig], ig, ','.join(sorted(vegleg[ig])), '', 'végleges kapuhiba (kapupont)')


# ---------------------------------------------------------------------------
# (d) régi arany
# ---------------------------------------------------------------------------

def regi_arany(adat, sorok, futasok=(REF, CEL)):
    for f in futasok:
        ok_v = {ig for ig in adat.versek if adat.ok(f, ig)}
        for cs in RETEGEK + [meres.OSSZES]:
            hb, e, hbk, ek = meres_p3b.regi_osszeallitas(adat, lambda ig: adat.linkek(f, ig), cs, ok_v)
            sorok.add('regi_arany', f, cs, 'regi_arany_kizaras_nelkul', e, hb, 'MÉRT (DT21 i); kapun átment versek, halmaz-definíció')
            sorok.add('regi_arany', f, cs, 'regi_arany_kizarassal_tajekoztato', ek, hbk,
                      'TÁJÉKOZTATÓ (DT21 i): 1Móz 6:17 kizárva; kapun átment versek')


# ---------------------------------------------------------------------------
# (e) Δ, páros bootstrap
# ---------------------------------------------------------------------------

def _kvant(b):
    b = sorted(b)
    return b[int(0.05 * len(b))], b[int(0.95 * len(b)) - 1]


def _osztas(a, b):
    return a / b if b else 0.0


def _merok(g, k):
    """g = (t_r, c_r, t_c, c_c, gold), k = (e_r, v_r, e_c, v_c, n) összegek -> {mero: (ref, cel)}."""
    return {'pontossag': (_osztas(g[0], g[1]), _osztas(g[2], g[3])),
            'lefedettseg': (_osztas(g[0], g[4]), _osztas(g[2], g[4])),
            'kapuhiba_elso_probara': (_osztas(k[0], k[4]), _osztas(k[2], k[4])),
            'kapuhiba_vegleg': (_osztas(k[1], k[4]), _osztas(k[3], k[4]))}


def _osszeg(vektorok, hossz):
    return tuple(sum(v[i] for v in vektorok) for i in range(hossz))


def boot_delta(gold, kap, csoportok, n_boot=N_BOOT, mag=MAG):
    """Páros, rétegzett bootstrap a versek felett.

    gold: {igehely: (réteg, (t_ref, c_ref, t_cel, c_cel, arany_link))}  (az aranyversek, ahol mindkét futás átment)
    kap:  {igehely: (réteg, (elso_ref, vegleg_ref, elso_cel, vegleg_cel))}  (a 200 vers)
    csoportok: {név: [rétegek]}
    Visszaad: {név: {mérő: (ref, cel, delta, alsó90, felső90, n_gold, n_200)}}.
    A két futás ugyanazt az újramintát kapja (páros); az újramintavétel rétegen belül történik; a mérőszámok a
    csoport rétegeinek összegéből jönnek (linkek összege verseken át, nem versátlag)."""
    rnd = random.Random(mag)
    retegek = sorted({r for r, _ in gold.values()} | {r for r, _ in kap.values()})
    gl = {r: [v for ig, (rr, v) in gold.items() if rr == r] for r in retegek}
    kl = {r: [v + (1,) for ig, (rr, v) in kap.items() if rr == r] for r in retegek}
    kl = {r: [tuple(x) for x in s] for r, s in kl.items()}
    boot = {n: {m: [] for m in MEROK_DELTA} for n in csoportok}
    for _ in range(n_boot):
        ag, ak = {}, {}
        for r in retegek:          # a rétegek rögzített sorrendben: determinisztikus
            sg, sk = gl[r], kl[r]
            ag[r] = _osszeg([sg[rnd.randrange(len(sg))] for _ in sg], 5) if sg else (0,) * 5
            ak[r] = _osszeg([sk[rnd.randrange(len(sk))] for _ in sk], 5) if sk else (0,) * 5
        for n, st in csoportok.items():
            m = _merok(_osszeg([ag[r] for r in st if r in ag], 5), _osszeg([ak[r] for r in st if r in ak], 5))
            for k_, (a, b) in m.items():
                boot[n][k_].append(b - a)
    ki = {}
    for n, st in csoportok.items():
        g = _osszeg([v for r in st for v in gl.get(r, [])], 5)
        k = _osszeg([v for r in st for v in kl.get(r, [])], 5)
        n_g = sum(len(gl.get(r, [])) for r in st)
        n_k = sum(len(kl.get(r, [])) for r in st)
        ki[n] = {}
        for m, (a, b) in _merok(g, k).items():
            lo, hi = _kvant(boot[n][m]) if boot[n][m] else (0.0, 0.0)
            ki[n][m] = (a, b, b - a, lo, hi, n_g, n_k)
    return ki


def delta_bemenet(adat, fa, fb):
    """A boot_delta bemenete a (fa → fb) párra: (gold, kap)."""
    _, _, ea = meres.hibatipusok(adat, fa)
    _, _, eb = meres.hibatipusok(adat, fb)
    gold = {}
    for ig in adat.versek:
        if ig in adat.arany and adat.ok(fa, ig) and adat.ok(fb, ig):
            g, la, lb = adat.arany_linkek(ig), adat.linkek(fa, ig), adat.linkek(fb, ig)
            gold[ig] = (adat.reteg[ig], (len(la & g), len(la), len(lb & g), len(lb), len(g)))
    kap = {ig: (adat.reteg[ig], (int(ig in ea), int(not adat.ok(fa, ig)), int(ig in eb), int(not adat.ok(fb, ig))))
           for ig in adat.versek if ig in adat.futas[fa] and ig in adat.futas[fb]}
    return gold, kap


def hatas(adat, sorok, n_boot=N_BOOT):
    """Sorok: 'hatas' (a két összevetés Δ-ja és intervalluma), 'hatas_osszevetes' (Δ az ingadozáshoz képest)."""
    csop = {n: st for n, st in CSOPORTOK}
    adatok = {}
    for nev, fa, fb in (('F8V3 − F3V3', REF, CEL), ('F3V2B − F3V2 (ingadozás)', Z1, Z2)):
        gold, kap = delta_bemenet(adat, fa, fb)
        adatok[nev] = boot_delta(gold, kap, csop, n_boot)
        for cs in CSOP_NEVEK:
            for m, (a, b, d, lo, hi, ng, nk) in adatok[nev][cs].items():
                sorok.add('hatas', nev, cs, m, '%.4f|%.4f|%.4f' % (a, b, d), '%.4f|%.4f' % (lo, hi),
                          'ref|cél|Δ ; 90%%-os intervallum alsó|felső; n_arany=%d, n_200=%d' % (ng, nk))
    hat, ing = adatok['F8V3 − F3V3'], adatok['F3V2B − F3V2 (ingadozás)']
    for cs in CSOP_NEVEK:
        for m, (a, b, d, lo, hi, ng, nk) in hat[cs].items():
            zd, zlo, zhi = ing[cs][m][2], ing[cs][m][3], ing[cs][m][4]
            sorok.add('hatas_osszevetes', 'F8V3 − F3V3 vs ingadozás', cs, m, '%.4f|%.4f|%.4f|%.4f' % (a, b, d, zd),
                      '%.4f|%.4f|%.4f|%.4f' % (lo, hi, zlo, zhi),
                      'intervallum_nem_tartalmazza_0=%s; abs_delta_nagyobb_az_ingadozasnal=%s; n_arany=%d, n_200=%d; '
                      'ref|cél|Δ|ingadozás-Δ ; alsó|felső (F8V3−F3V3)|alsó|felső (ingadozás)' % (
                          'igen' if (lo > 0 or hi < 0) else 'nem', 'igen' if abs(d) > abs(zd) else 'nem', ng, nk))


# ---------------------------------------------------------------------------
# (f) érintett linkek és szavak
# ---------------------------------------------------------------------------

def link_besorol(G, S, T):
    """Link-szint: G = arany, S = F3V3, T = F8V3 linkhalmaz (egy versre). Visszaad: {kategória: [linkek]}."""
    return {'hiany_potolva': sorted((G & T) - S),             # arany-link, F3V3-ban hiányzott, F8V3-ban megvan
            'tobblet_megszunt': sorted((S - G) - T),          # F3V3-ban többlet volt, F8V3-ban nincs
            'hiany_uj': sorted((G & S) - T),                  # arany-link, F3V3-ban megvolt, F8V3-ban hiányzik
            'tobblet_uj': sorted((T - G) - S)}                # F8V3-ban új többlet


def szo_besorol(G, S, T):
    """Szó-szint: egy magyar szó arany / F3V3 / F8V3 linkhalmaza (az eredeti sorszámok halmaza).
    'javult': F3V3-ban nem, F8V3-ban pontosan az arany; 'romlott': fordítva; 'valtozott_rossz_marad': mindkettő
    eltér az aranytól és egymástól is; 'nem_valtozott_jo'/'nem_valtozott_rossz': S == T."""
    if S == T:
        return 'nem_valtozott_jo' if S == G else 'nem_valtozott_rossz'
    if T == G:
        return 'javult'
    if S == G:
        return 'romlott'
    return 'valtozott_rossz_marad'


def _strongok(s):
    return {'%s%04d' % (m.group(1), int(m.group(2))) for m in re.finditer(r'([HG])(\d+)', s)}


def _kjv_strongok(ig, forras):
    t = tokenek.kjv_tamapont_forras(ig, forras)
    return None if not t else set(re.findall(r'\{([HG]\d+)\}', t))


def _szavak(linkek):
    d = {}
    for k, e in linkek:
        d.setdefault(k, set()).add(e)
    return d


def erintett(adat, sorok):
    """Az érintett linkek és szavak; a szó-szintű rekordokat is visszaadja (a jelentés példáihoz)."""
    versek = [ig for ig in adat.versek if ig in adat.arany and adat.ok(REF, ig) and adat.ok(CEL, ig)]
    kimaradt = [ig for ig in adat.versek if ig in adat.arany and not (adat.ok(REF, ig) and adat.ok(CEL, ig))]
    for ig in kimaradt:
        sorok.add('erintett_kimaradt', '%s/%s' % (REF, CEL), adat.reteg[ig], ig,
                  ','.join(f for f in (REF, CEL) if not adat.ok(f, ig)), '', 'az aranyvers kimarad: ezen a futáson végleges kapuhiba')
    mind = [ig for ig in adat.versek if ig in adat.arany]
    kjv_cel = {ig: _kjv_strongok(ig, KJV_FORRAS[CEL]) for ig in mind}
    kjv_ref = {ig: _kjv_strongok(ig, KJV_FORRAS[REF]) for ig in mind}
    szavak = []       # szó-szintű rekordok
    linkdb = {}
    szodb = {}
    csoportok = [(cs, lambda ig, st=st: adat.reteg[ig] in st) for cs, st in CSOPORTOK]
    csoportok.append(('R2+R3, KJV-sorral az F8V3-ban', lambda ig: adat.reteg[ig] in ('R2', 'R3') and kjv_cel[ig] is not None))
    csoportok.append(('R2+R3, KJV-sor nélkül az F8V3-ban', lambda ig: adat.reteg[ig] in ('R2', 'R3') and kjv_cel[ig] is None))
    for ig in versek:
        G, S, T = adat.arany_linkek(ig), adat.linkek(REF, ig), adat.linkek(CEL, ig)
        lb = link_besorol(G, S, T)
        for kat, ls in lb.items():
            for k, e in ls:
                w = adat.ered[ig][e - 1]
                sorok.add('erintett_link', kat, adat.reteg[ig], ig, str(k), str(e),
                          'magyar: %s | eredeti: %s %s (%s) | KJV-sor az F8V3-ban: %s' % (
                              tokenek.tokenizal(adat.karoli[ig])[k - 1], w['alak'], w['strong'], w['tukor'],
                              'nincs' if kjv_cel[ig] is None else ('az eredeti Strongja benne van' if _strongok(w['strong']) & kjv_cel[ig] else 'az eredeti Strongja nincs benne')))
        gs, ss, ts = _szavak(G), _szavak(S), _szavak(T)
        for k in sorted(set(gs) | set(ss) | set(ts)):
            g_, s_, t_ = gs.get(k, set()), ss.get(k, set()), ts.get(k, set())
            kat = szo_besorol(g_, s_, t_)
            szavak.append({'vers': ig, 'k': k, 'reteg': adat.reteg[ig], 'kat': kat, 'G': g_, 'S': s_, 'T': t_,
                           'szo': tokenek.tokenizal(adat.karoli[ig])[k - 1],
                           'kjv_van': kjv_cel[ig] is not None, 'kjv_ref_van': kjv_ref[ig] is not None})
    for cs, pred in csoportok:
        vs = [ig for ig in versek if pred(ig)]
        sorok.add('erintett_szamok', '%s/%s' % (REF, CEL), cs, 'aranyversek_mindketto_atment', len(vs),
                  sum(1 for ig in adat.versek if ig in adat.arany and pred(ig)), 'nevező: az aranyversek a csoportban')
        lc = {k: 0 for k in ('hiany_potolva', 'tobblet_megszunt', 'hiany_uj', 'tobblet_uj')}
        for ig in vs:
            for kat, ls in link_besorol(adat.arany_linkek(ig), adat.linkek(REF, ig), adat.linkek(CEL, ig)).items():
                lc[kat] += len(ls)
        for kat, x in lc.items():
            sorok.add('erintett_szamok', '%s/%s' % (REF, CEL), cs, 'link_%s' % kat, x, '')
        sorok.add('erintett_szamok', '%s/%s' % (REF, CEL), cs, 'link_javitott_osszes (hiany_potolva + tobblet_megszunt)',
                  lc['hiany_potolva'] + lc['tobblet_megszunt'], '')
        sorok.add('erintett_szamok', '%s/%s' % (REF, CEL), cs, 'link_romlott_osszes (hiany_uj + tobblet_uj)',
                  lc['hiany_uj'] + lc['tobblet_uj'], '')
        vset = set(vs)
        sz = [x for x in szavak if x['vers'] in vset]
        for kat in ('javult', 'romlott', 'valtozott_rossz_marad', 'nem_valtozott_jo', 'nem_valtozott_rossz'):
            sorok.add('erintett_szamok', '%s/%s' % (REF, CEL), cs, 'szo_%s' % kat, sum(1 for x in sz if x['kat'] == kat), len(sz),
                      'nevező: a csoport aranyversein szereplő magyar szavak (az arany, F3V3 vagy F8V3 linkhalmazában van link)')
        szodb[cs] = len(sz)
        linkdb[cs] = lc
    # a szó-szintű rekordok a TSV-be (a jelentés példáit a jelentés a rekordokból választja)
    peldak = peldak_valaszt(adat, szavak)
    for x in szavak:
        if x['kat'] in ('javult', 'romlott', 'valtozott_rossz_marad'):
            sorok.add('erintett_szo', x['kat'], x['reteg'], x['vers'], str(x['k']), '',
                      szo_leiras(adat, x) + (' | PÉLDA' if id(x) in {id(p) for p in peldak} else ''))
    return versek, kimaradt, szavak, peldak


def szo_leiras(adat, x):
    ig = x['vers']

    def ered(es):
        return ', '.join('%d %s (%s)' % (e, adat.ered[ig][e - 1]['alak'], adat.ered[ig][e - 1]['tukor']) for e in sorted(es)) or '—'
    return 'magyar: %s | eredeti – arany: %s | F3V3: %s | F8V3: %s | KJV-sor az F8V3-ban: %s, az F3V3-ban: %s' % (
        x['szo'], ered(x['G']), ered(x['S']), ered(x['T']), 'van' if x['kjv_van'] else 'nincs', 'van' if x['kjv_ref_van'] else 'nincs')


def peldak_valaszt(adat, szavak, javult_max=8, romlott_max=5):
    """Jellemző példák az R2–R3 versekből: determinisztikus, versenként körbejárva (egy vers egy kört kap, amíg van
    másik vers), a minta sorrendjében."""
    ki = []
    for kat, maximum in (('javult', javult_max), ('romlott', romlott_max)):
        jel = [x for x in szavak if x['kat'] == kat and x['reteg'] in ('R2', 'R3')]
        versenkent = {}
        for x in jel:
            versenkent.setdefault(x['vers'], []).append(x)
        sorrend = [ig for ig in adat.versek if ig in versenkent]
        valasztott = []
        kor = 0
        while len(valasztott) < maximum and any(len(versenkent[ig]) > kor for ig in sorrend):
            for ig in sorrend:
                if len(versenkent[ig]) > kor and len(valasztott) < maximum:
                    valasztott.append(versenkent[ig][kor])
            kor += 1
        ki += valasztott
    return ki


# ---------------------------------------------------------------------------
# (g) költség, (h) KJV-sor hossza
# ---------------------------------------------------------------------------

def koteg_cimke(adat, sor):
    return '+'.join(sorted({adat.reteg[ig] for ig in sor['igehelyek']}))


def koltseg(adat, sorok):
    for f in (REF, CEL):
        s = [r for r in adat.naplo if r['futas'] == f]
        for cim, resz in (('teljes', s), ('ebből baleseti kötegek (%s)' % '+'.join(BALESET_KOTEGEK),
                                           [r for r in s if str(r['koteg']) in BALESET_KOTEGEK and f == CEL])):
            if not resz:
                continue
            oss = '%s %s' % (f, cim)
            sorok.add('koltseg', oss, meres.OSSZES, 'hivasok', len(resz), '', 'próbálkozás=1: %d, próbálkozás=2: %d' % (
                sum(1 for r in resz if r['probalkozas'] == '1'), sum(1 for r in resz if r['probalkozas'] == '2')))
            sorok.add('koltseg', oss, meres.OSSZES, 'bemeneti_token', sum(int(r['bemenet_token']) for r in resz), '')
            sorok.add('koltseg', oss, meres.OSSZES, 'kimeneti_token', sum(int(r['kimenet_token']) for r in resz), '')
            sorok.add('koltseg', oss, meres.OSSZES, 'koltseg_usd', '%.6f' % sum(float(r['koltseg_usd']) for r in resz), '',
                      'koltseg_forras: %s' % ','.join(sorted({r['koltseg_forras'] for r in resz})))
        sorok.add('koltseg', '%s teljes' % f, meres.OSSZES, 'beallitas', '; '.join(sorted({
            '%s | %s | prompt %s' % (r['modell'], r['gondolkodas_mod'], r['prompt_sha256_12']) for r in s})), '')
    ref_s = [r for r in adat.naplo if r['futas'] == REF]
    cel_s = [r for r in adat.naplo if r['futas'] == CEL]
    for mero, fn in (('hivasok', lambda s_: len(s_)), ('bemeneti_token', lambda s_: sum(int(r['bemenet_token']) for r in s_)),
                     ('kimeneti_token', lambda s_: sum(int(r['kimenet_token']) for r in s_))):
        sorok.add('koltseg', 'F8V3 − F3V3 (teljes)', meres.OSSZES, mero, fn(cel_s) - fn(ref_s), fn(ref_s), 'különbség; nevező: az F3V3 értéke')
    sorok.add('koltseg', 'F8V3 − F3V3 (teljes)', meres.OSSZES, 'koltseg_usd', '%.6f' % (sum(float(r['koltseg_usd']) for r in cel_s) - sum(float(r['koltseg_usd']) for r in ref_s)), '',
              'különbség (az újrakérések és a kimenet is benne van)')
    # köteg-szintű összevetés (csak a próbálkozás=1: ugyanaz a bemenet-szerkezet; az újrakérések mérete eltér)
    cimke = {}
    for f in (REF, CEL):
        for sor in adat.kotegsorok[f]:
            cimke[(f, str(sor['koteg']))] = koteg_cimke(adat, sor)
    p1 = {(r['futas'], r['koteg']): int(r['bemenet_token']) for r in adat.naplo if r['futas'] in (REF, CEL) and r['probalkozas'] == '1'}
    csoportok = {}
    for sor in adat.kotegsorok[REF]:
        k = str(sor['koteg'])
        if (CEL, k) in cimke and (REF, k) in p1 and (CEL, k) in p1:
            csoportok.setdefault(cimke[(REF, k)], []).append(k)
    for c, ks in sorted(csoportok.items()):
        a = sum(p1[(REF, k)] for k in ks)
        b = sum(p1[(CEL, k)] for k in ks)
        ka = sum(kjv_koteg_karakter(adat, REF, k) for k in ks)
        kb = sum(kjv_koteg_karakter(adat, CEL, k) for k in ks)
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'koteg_db', len(ks), '', 'a köteg rétegei (egy köteg több rétegű is lehet)')
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'bemenet_token_p1_F3V3', a, '')
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'bemenet_token_p1_F8V3', b, '')
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'bemenet_token_p1_delta', b - a, a, 'F8V3 − F3V3; nevező: az F3V3 bemeneti tokenje')
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'kjv_sor_karakter_F3V3', ka, '')
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'kjv_sor_karakter_F8V3', kb, '')
        sorok.add('koltseg_koteg', 'F8V3 − F3V3', c, 'kjv_sor_karakter_delta', kb - ka, '', 'F8V3 − F3V3')


def kjv_sor_hossz(ig, forras):
    """A KJV-TÁMPONT sor hossza a bemenetben (a 'KJV-TÁMPONT: ' előtaggal és az elválasztó sortöréssel); 0, ha nincs sor."""
    t = tokenek.kjv_tamapont_forras(ig, forras)
    return len('KJV-TÁMPONT: %s' % t) + 1 if t else 0


_KOTEG_KJV = {}


def kjv_koteg_karakter(adat, f, koteg):
    kulcs = (id(adat), f, koteg)
    if kulcs not in _KOTEG_KJV:
        sor = next(s for s in adat.kotegsorok[f] if str(s['koteg']) == str(koteg))
        _KOTEG_KJV[kulcs] = sum(kjv_sor_hossz(ig, KJV_FORRAS[f]) for ig in sor['igehelyek'])
    return _KOTEG_KJV[kulcs]


def kjv_hossz(adat, sorok):
    for f in (REF, CEL):
        for cs in CSOP_NEVEK:
            vs = csop_versek(adat, cs)
            h = [kjv_sor_hossz(ig, KJV_FORRAS[f]) for ig in vs]
            van = [x for x in h if x]
            sorok.add('kjv_hossz', f, cs, 'versek_kjv_sorral', len(van), len(vs), 'KJV-forrás: %s' % KJV_FORRAS[f])
            sorok.add('kjv_hossz', f, cs, 'kjv_sor_karakter_osszes', sum(van), '')
            sorok.add('kjv_hossz', f, cs, 'kjv_sor_karakter_atlag_vers', sum(van), len(van), 'számláló: összes karakter; nevező: a KJV-sorral bíró versek')
        kot = {}
        for sor in adat.kotegsorok[f]:
            kot.setdefault(koteg_cimke(adat, sor), []).append(kjv_koteg_karakter(adat, f, str(sor['koteg'])))
        for c, h in sorted(kot.items()):
            sorok.add('kjv_hossz_koteg', f, c, 'koteg_db', len(h), '')
            sorok.add('kjv_hossz_koteg', f, c, 'kjv_karakter_koteg_atlag', sum(h), len(h), 'számláló: karakter-összeg; nevező: a kötegek száma')
            sorok.add('kjv_hossz_koteg', f, c, 'kjv_karakter_koteg_min', min(h), '')
            sorok.add('kjv_hossz_koteg', f, c, 'kjv_karakter_koteg_max', max(h), '')
    # keresztellenőrzés: a KJV-sorral bíró versek halmaza a jsonl kjv_forras mezőjével / a minta.tsv-vel
    jel = {ig for s in adat.kotegsorok[CEL] for ig in s.get('kjv_forras', {}).get('kjv_sorral_versek', [])}
    sajat = {ig for ig in adat.versek if kjv_sor_hossz(ig, KJV_FORRAS[CEL])}
    sorok.add('kjv_kereszt', CEL, meres.OSSZES, 'kjv_sorral_versek_jsonl_vs_ujraszamolt', len(sajat), len(jel),
              'jsonl kjv_forras.kjv_sorral_versek (%d) = újraszámolt (%d): %s' % (len(jel), len(sajat), 'EGYEZIK' if jel == sajat else 'ELTÉR'))
    minta = {m['igehely'] for m in adat.minta if m['kjv_tamapont'] == 'van'}
    regi = {ig for ig in adat.versek if kjv_sor_hossz(ig, KJV_FORRAS[REF])}
    sorok.add('kjv_kereszt', REF, meres.OSSZES, 'kjv_sorral_versek_minta_vs_ujraszamolt', len(regi), len(minta),
              'minta.tsv kjv_tamapont=van (%d) = újraszámolt régi-tábla (%d): %s' % (len(minta), len(regi), 'EGYEZIK' if minta == regi else 'ELTÉR'))
    sha = {s.get('kjv_forras', {}).get('sha256') for s in adat.kotegsorok[CEL]}
    sorok.add('kjv_kereszt', CEL, meres.OSSZES, 'kjv_tabla_sha256_a_jsonlban', len(sha), '', '; '.join(sorted(str(x) for x in sha)))


# ---------------------------------------------------------------------------
# (i) verszintű egyezés
# ---------------------------------------------------------------------------

def versegyezes(adat, sorok):
    for fa, fb, nev in ((REF, CEL, 'F3V3–F8V3'), (Z1, Z2, 'F3V2–F3V2B (ingadozás)')):
        for halmaz in ('200 vers', 'arany'):
            for cs in CSOP_NEVEK:
                vs = [ig for ig in csop_versek(adat, cs) if adat.ok(fa, ig) and adat.ok(fb, ig)
                      and (halmaz == '200 vers' or ig in adat.arany)]
                osz = [ig for ig in csop_versek(adat, cs) if halmaz == '200 vers' or ig in adat.arany]
                azonos = sum(1 for ig in vs if adat.linkek(fa, ig) == adat.linkek(fb, ig))
                m = sum(len(adat.linkek(fa, ig) & adat.linkek(fb, ig)) for ig in vs)
                u = sum(len(adat.linkek(fa, ig) | adat.linkek(fb, ig)) for ig in vs)
                sorok.add('versegyezes', nev, cs, 'versek_mindketto_atment [%s]' % halmaz, len(vs), len(osz))
                sorok.add('versegyezes', nev, cs, 'azonos_linkhalmazu_versek [%s]' % halmaz, azonos, len(vs))
                sorok.add('versegyezes', nev, cs, 'link_egyezes (uniós arány) [%s]' % halmaz, m, u, 'Σ|A∩B| / Σ|A∪B|, ahol mindkettő átment')


def mentett_ellenorzes(sorok, forras_dir, futasok=FUTASOK):
    import futtat
    for f in futasok:
        h = futtat.mentett_valaszok_ellenoriz(f, forras_dir)
        sorok.add('mentett_ellenorzes', f, meres.OSSZES, 'hibak', len(h), '',
                  'futtat.mentett_valaszok_ellenoriz: %s' % ('0 hiba' if not h else '; '.join(h[:5])))


# ---------------------------------------------------------------------------
# a teljes számítás
# ---------------------------------------------------------------------------

def szamol(forras_dir=None, arany_ut=None, arany_sha=None, n_boot=N_BOOT, mentett=True):
    """Visszaad: (adat, info, sorok, erintett_adat)."""
    adat, info = betolt(forras_dir, arany_ut, arany_sha)
    sorok = Sorok()
    pont_lef(adat, sorok)
    kozos_pont_lef(adat, sorok, ((REF, CEL), (Z1, Z2)))
    kapuhiba(adat, sorok)
    regi_arany(adat, sorok)
    hatas(adat, sorok, n_boot)
    er = erintett(adat, sorok)
    koltseg(adat, sorok)
    kjv_hossz(adat, sorok)
    versegyezes(adat, sorok)
    if mentett:
        mentett_ellenorzes(sorok, forras_dir or F21P)
    return adat, info, sorok, er


# ---------------------------------------------------------------------------
# kiírás
# ---------------------------------------------------------------------------

def fejlec(info, ts):
    return ('GENERÁLT: eszkozok/karoli_strong/meres_kjv.py | scope=KJV-mérés (F21.67): F8V3 (C, prompt_v3, 200 vers, KJV-támpont a '
            'teljes KJV-táblából) az F3V3-mal szemben (C, prompt_v3, KJV csak az R1-en, régi tábla); ingadozás: F3V2, F3V2B; arany %s '
            '(%d vers, sha256 %s) | forras=f21p/valaszok/{F3V3,F8V3,F3V2,F3V2B}.jsonl, %s (sha256 ellenőrizve), f21p/meres_kizaras.tsv, '
            'f21p/regi_arany_hibas.tsv, f21p/minta.tsv, konkordancia/Karoli_Strong_kivonat.tsv, konkordancia/KJV_Strongs_teljes.tsv, '
            'f21p/futasnaplo.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
            'kézzel szerkeszteni tilos' % (info['verzio'], info['aranyversek'], info['sha256'][:16], os.path.basename(info['jsonl']), ts))


def _pct(sz, nev):
    return meres_p3c._pct(sz, nev)


def _f(x):
    return '%.1f%%' % (100 * x)


def _pp(x):
    return '%+.1f pp' % (100 * x)


def _cella(mero, sz, nev):
    if nev == '':
        return sz
    if mero.endswith('atlag_vers'):
        return '%.0f (%s/%s)' % (int(sz) / int(nev), sz, nev) if int(nev) else '— (0/0)'
    return _pct(sz, nev)


def tabla(sorok, szakasz, merok, osszeallitasok, csoportok=None):
    csoportok = csoportok or CSOP_NEVEK
    out = ['| összeállítás | mérőszám | %s |' % ' | '.join(csoportok), '|---|---|%s' % ('---|' * len(csoportok))]
    for o in osszeallitasok:
        for m in merok:
            cellak, talalt = [], False
            for r in csoportok:
                x = [s for s in sorok.lista if s[0] == szakasz and s[1] == o and s[2] == r and s[3] == m]
                if x:
                    talalt = True
                    cellak.append(_cella(m, x[0][4], x[0][5]))
                else:
                    cellak.append('—')
            if talalt:
                out.append('| %s | %s | %s |' % (o, m, ' | '.join(cellak)))
    return out + ['']


def jelentes_szoveg(sorok, info, ts, er, adat):
    versek, kimaradt, szavak, peldak = er
    fej = fejlec(info, ts)
    S = sorok.lista

    def ertek(szakasz, oss, ret, mero):
        x = [s for s in S if s[0] == szakasz and s[1] == oss and s[2] == ret and s[3] == mero]
        return x[0] if x else None

    ki = ['# F21P_kjv_meres.md — KJV-mérés: F8V3 (teljes KJV-tábla, minden rétegben) az F3V3-mal szemben', '', '<!-- %s -->' % fej, '',
          'Kizárólag szkriptkimenet; a jelentés nem von le következtetést, csak a számokat és az olvasási korlátokat adja. '
          'Cellaforma: érték (számláló/nevező). A mérés az arany **%s** változatára megy (%d vers, hash ellenőrizve). '
          'Rétegek: R1–R4; „R2+R3” = a két réteg együtt (ahol a KJV-sor az F3V3-hoz képest tényleg új); „Összes” = R1–R4.'
          % (info['verzio'], info['aranyversek']), '']
    # --- 0. mi a különbség a két futás bemenetében
    ki += ['## 0. A két futás beállítása és a KJV-sor jelenléte', '']
    for f in (REF, CEL):
        b = ertek('koltseg', '%s teljes' % f, meres.OSSZES, 'beallitas')
        ki.append('- %s: %s; KJV-forrás: %s' % (f, b[4] if b else '—', KJV_FORRAS[f]))
    ki += ['', '| futás | mérőszám | ' + ' | '.join(CSOP_NEVEK) + ' |', '|---|---|' + '---|' * len(CSOP_NEVEK)]
    for f in (REF, CEL):
        cellak = []
        for cs in CSOP_NEVEK:
            x = ertek('kjv_hossz', f, cs, 'versek_kjv_sorral')
            cellak.append('%s/%s' % (x[4], x[5]))
        ki.append('| %s | versek KJV-sorral (a 200-ból) | %s |' % (f, ' | '.join(cellak)))
    ki += ['']
    ki += ['Keresztellenőrzések a KJV-sorra:']
    for s in S:
        if s[0] == 'kjv_kereszt':
            ki.append('- %s: %s %s' % (s[1], s[3], s[6]))
    ki += ['']
    # --- a)
    ki += ['## a) Pontosság és lefedettség (a kapun átment aranyverseken; „sajat” = a futás saját halmaza)', '']
    ki += tabla(sorok, 'sajat', ['arany_versek_kapun_atment', 'pontossag', 'lefedettseg'], FUTASOK)
    ki += ['A páros halmaz („kozos”: mindkét összevetett futás átment; ezen megy a Δ):', '']
    ki += tabla(sorok, 'kozos', ['arany_versek_mindketto_atment', 'pontossag', 'lefedettseg'],
                ['%s [pár: %s–%s]' % (f, a, b) for a, b in ((REF, CEL), (Z1, Z2)) for f in (a, b)])
    # --- e) Δ
    ki += ['## b) A különbség: F8V3 − F3V3, páros bootstrap (versek felett, rétegzett, 1 000 újramintavétel, mag %d), az ingadozással összevetve' % MAG, '',
           'Δ = F8V3 − F3V3 a közös (mindkét futás által átment) aranyversek linkjein (pontosság, lefedettség) és a 200 versen (kapuhiba); a „Δ 90%” a '
           'bootstrap 5.–95. percentilise. Ingadozás-becslés: F3V2B − F3V2 (azonos prompt, azonos bemenet), ugyanazokkal a mérőszámokkal és ugyanazzal a '
           'bootstrappel, az arany v3-ra mérve. Két leíró jelölés külön: **[0∉]** = a Δ 90%-os intervalluma nem tartalmazza a 0-t; **[>zaj]** = '
           '|Δ| > |F3V2B − F3V2|. Nem szignifikanciapróba.', '',
           '| réteg | mérőszám | F3V3 | F8V3 | Δ | Δ 90% | ingadozás (F3V2B − F3V2) | ingadozás 90% | jelölés | n (arany / 200) |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for s in S:
        if s[0] == 'hatas_osszevetes':
            a, b, d, zd = (float(v) for v in s[4].split('|'))
            lo, hi, zlo, zhi = (float(v) for v in s[5].split('|'))
            jel = []
            if 'intervallum_nem_tartalmazza_0=igen' in s[6]:
                jel.append('[0∉]')
            if 'abs_delta_nagyobb_az_ingadozasnal=igen' in s[6]:
                jel.append('[>zaj]')
            n = re.search(r'n_arany=(\d+), n_200=(\d+)', s[6])
            ki.append('| %s | %s | %s | %s | %s | [%s; %s] | %s | [%s; %s] | %s | %s / %s |' % (
                s[2], s[3], _f(a), _f(b), _pp(d), _pp(lo).replace(' pp', ''), _pp(hi), _pp(zd), _pp(zlo).replace(' pp', ''), _pp(zhi),
                ' '.join(jel) or '—', n.group(1), n.group(2)))
    ki += ['']
    # --- c) kapuhiba
    ki += ['## c) Kapuhiba első próbára és végleg (a 200 versen, rétegenként)', '']
    ki += tabla(sorok, 'kapuhiba', ['elso_probara', 'vegleg'], FUTASOK)
    ki += ['Keresztellenőrzés (újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg):', '']
    for s in S:
        if s[0] == 'kapuhiba_kereszt':
            ki.append('- %s: %s' % (s[1], s[6]))
    ki += ['', '### Hibatípusok kapupont szerint (hibás versek száma a rétegben a 200-ból; egy vers több ponton is hibázhat)', '']
    merok_t = []
    for s in S:
        if s[0] == 'kapuhiba_tipus' and s[3] not in merok_t:
            merok_t.append(s[3])
    ki += tabla(sorok, 'kapuhiba_tipus', merok_t, [REF, CEL], [meres.OSSZES, 'R1', 'R2', 'R3', 'R4'])
    vegl = [s for s in S if s[0] == 'kapuhiba_vegleges_versek']
    ki += ['Végleges kapuhibás versek: ' + ('; '.join('%s: %s (%s, kapupont %s)' % (s[1], s[3], s[2], s[4]) for s in vegl) if vegl else 'nincs'), '']
    ki += ['Mentett (allapot=ok) válaszok újraellenőrzése a teljes kapun:', '']
    for s in S:
        if s[0] == 'mentett_ellenorzes':
            ki.append('- %s: %s hiba (%s)' % (s[1], s[4], s[6]))
    ki += ['']
    # --- d) régi arany
    ki += ['## d) Régi arany egyezés (halmaz-definíció; MÉRT = kizárás nélküli; tájékoztató: 1Móz 6:17 kizárva; a kapun átment versekre)', '']
    ki += tabla(sorok, 'regi_arany', ['regi_arany_kizaras_nelkul', 'regi_arany_kizarassal_tajekoztato'], [REF, CEL], RETEGEK + [meres.OSSZES])
    # --- f) érintett
    ki += ['## f) Érintett linkek és szavak (az aranyversek, ahol az F3V3 és az F8V3 is átment)', '']
    if kimaradt:
        ki.append('Kimaradt aranyversek (valamelyik futás végleges kapuhibája): ' + '; '.join(
            '%s (%s: %s)' % (ig, adat_reteg(S, ig), [s[4] for s in S if s[0] == 'erintett_kimaradt' and s[3] == ig][0]) for ig in kimaradt) + '.')
        ki.append('')
    csn = CSOP_NEVEK + ['R2+R3, KJV-sorral az F8V3-ban', 'R2+R3, KJV-sor nélkül az F8V3-ban']
    ki += tabla(sorok, 'erintett_szamok', ['aranyversek_mindketto_atment',
                                           'link_hiany_potolva', 'link_tobblet_megszunt', 'link_hiany_uj', 'link_tobblet_uj',
                                           'link_javitott_osszes (hiany_potolva + tobblet_megszunt)',
                                           'link_romlott_osszes (hiany_uj + tobblet_uj)',
                                           'szo_javult', 'szo_romlott', 'szo_valtozott_rossz_marad', 'szo_nem_valtozott_jo', 'szo_nem_valtozott_rossz'],
                ['%s/%s' % (REF, CEL)], csn)
    ki += ['Link-szint: **hiány pótolva** = arany-link, az F3V3-ban hiányzott, az F8V3-ban megvan; **többlet megszűnt** = az F3V3-ban (aranyban nem szereplő) '
           'többlet-link, az F8V3-ban nincs; **hiány új** = arany-link, az F3V3-ban megvolt, az F8V3-ban hiányzik; **többlet új** = az F8V3-ban új, aranyban nem '
           'szereplő link. Szó-szint: egy magyar szó linkhalmaza pontosan az arany (javult: F3V3-ban nem, F8V3-ban igen; romlott: fordítva; '
           'változott_rossz_marad: mindkettő eltér az aranytól és egymástól is). Az érintett linkek és szavak teljes listája az '
           '`erintett_link` és `erintett_szo` szakaszban áll (f21p/kjv_meres_eredmeny.tsv).', '']
    ki += ['### Jellemző példák az R2–R3 versekből (szó-szint; versenként körbejárva, a minta sorrendjében; a kiválasztás szabálya determinisztikus, nem szubjektív)', '']
    for kat, cim in (('javult', 'Javult (F3V3-ban nem, F8V3-ban pontosan az arany)'), ('romlott', 'Romlott (F3V3-ban pontosan az arany, F8V3-ban nem)')):
        ki += ['**%s**' % cim, '']
        x = [p for p in peldak if p['kat'] == kat]
        if not x:
            ki += ['(nincs ilyen szó az R2–R3 versekben)', '']
            continue
        ki += ['| vers | réteg | leírás |', '|---|---|---|']
        for p in x:
            ki.append('| %s | %s | %s |' % (p['vers'], p['reteg'], szo_leiras(adat, p).replace(' | ', '; ')))
        ki += ['']
    # --- g) költség
    ki += ['## g) Költség és tokenek (a futásnaplóból)', '', '| futás | mérőszám | érték | megjegyzés |', '|---|---|---|---|']
    for s in S:
        if s[0] == 'koltseg':
            ki.append('| %s | %s | %s | %s |' % (s[1], s[3], s[4], s[6]))
    ki += ['', 'Az F8V3 első két kötege (1., 2.) helyi baleset eredménye (naplok/F21_baleset_F8V3.md; azonos futtató és konfiguráció); a fenti „teljes” sorok '
               'ezeket tartalmazzák, a „baleseti kötegek” sor külön mutatja őket. Köteg-szintű bemenet-összevetés (csak a próbálkozás=1 hívások, mert az '
               'újrakérések mérete eltér), a köteg rétegei szerint csoportosítva:', '',
           '| köteg rétegei | kötegek | bemenet token F3V3 | bemenet token F8V3 | Δ (F8V3 − F3V3) | KJV-sor karakter F3V3 | KJV-sor karakter F8V3 | Δ karakter |',
           '|---|---|---|---|---|---|---|---|']
    cs_ = []
    for s in S:
        if s[0] == 'koltseg_koteg' and s[2] not in cs_:
            cs_.append(s[2])
    for c in cs_:
        def v(m, c=c):
            x = ertek('koltseg_koteg', 'F8V3 − F3V3', c, m)
            return x
        d = v('bemenet_token_p1_delta')
        ki.append('| %s | %s | %s | %s | %s (%s) | %s | %s | %s |' % (
            c, v('koteg_db')[4], v('bemenet_token_p1_F3V3')[4], v('bemenet_token_p1_F8V3')[4], d[4], _pct(d[4], d[5]),
            v('kjv_sor_karakter_F3V3')[4], v('kjv_sor_karakter_F8V3')[4], v('kjv_sor_karakter_delta')[4]))
    ki += ['']
    # --- h) KJV-sor hossza
    ki += ['## h) A KJV-sor hossza a bemenetben (a „KJV-TÁMPONT: ” előtaggal és a sortöréssel)', '']
    ki += tabla(sorok, 'kjv_hossz', ['versek_kjv_sorral', 'kjv_sor_karakter_osszes', 'kjv_sor_karakter_atlag_vers'], [REF, CEL])
    ki += ['Köteg-szinten (karakter/köteg, a köteg rétegei szerint):', '', '| futás | köteg rétegei | kötegek | átlag | min | max |', '|---|---|---|---|---|---|']
    for f in (REF, CEL):
        for c in sorted({s[2] for s in S if s[0] == 'kjv_hossz_koteg' and s[1] == f}):
            ki.append('| %s | %s | %s | %s | %s | %s |' % (
                f, c, ertek('kjv_hossz_koteg', f, c, 'koteg_db')[4], _atlag(ertek('kjv_hossz_koteg', f, c, 'kjv_karakter_koteg_atlag')),
                ertek('kjv_hossz_koteg', f, c, 'kjv_karakter_koteg_min')[4], ertek('kjv_hossz_koteg', f, c, 'kjv_karakter_koteg_max')[4]))
    ki += ['']
    # --- i) verszintű egyezés
    ki += ['## i) Verszintű egyezés (hány vers kap azonos linkhalmazt; az F3V2–F3V2B pár az ingadozási alapvonal; az R4-en az F3V3/F8V3 bemenete azonos)', '']
    ki += tabla(sorok, 'versegyezes', ['versek_mindketto_atment [200 vers]', 'azonos_linkhalmazu_versek [200 vers]', 'link_egyezes (uniós arány) [200 vers]',
                                       'azonos_linkhalmazu_versek [arany]', 'link_egyezes (uniós arány) [arany]'],
                ['F3V3–F8V3', 'F3V2–F3V2B (ingadozás)'])
    # --- olvasási korlátok
    r23 = ertek('kjv_hossz', CEL, 'R2+R3', 'versek_kjv_sorral')
    r2, r3, r4 = (ertek('kjv_hossz', CEL, r, 'versek_kjv_sorral') for r in ('R2', 'R3', 'R4'))
    n23 = ertek('erintett_szamok', '%s/%s' % (REF, CEL), 'R2+R3', 'aranyversek_mindketto_atment')
    ki += ['## j) Olvasási korlátok', '',
           '1. **A kontroll tisztátalan (R1).** Az R1-en mindkét futásban volt KJV-sor, de a forrás és a forma is más: az F3V3 a régi '
           'Genesis/Exodus/Proverbs táblából kapta (frázisok, üres szavú {H0853}-elemek), az F8V3 a konkordancia/KJV_Strongs_teljes.tsv-ből (csak tartalmi szavak '
           '+ Strong, névelő/kötőszó/írásjel nélkül). Az R1-en tehát a különbség forrás- és formaváltás + futásközi ingadozás, nem tiszta „KJV nélkül/KJV-vel”.',
           '2. **Az R4 hiánya.** Az ÚSZ-ön (R4; 50 vers a mintában, %s az aranyban) az F8V3 sem kapott KJV-sort (a Károli ↔ KJV megfeleltetési tábla csak az ÓSZ-t fedi: '
           'KJV-sorral bíró R4 versek: %s/%s). Az R4-en a két futás bemenete azonos, a különbség tiszta futásközi ingadozás.' % (
               ertek('sajat', REF, 'R4', 'arany_versek_kapun_atment')[5], r4[4], r4[5]),
           '3. **A KJV-hatás tiszta mérése az R2–R3-on van** (F3V3: nincs KJV-sor, F8V3: van; KJV-sorral az F8V3-ban: R2 %s/%s, R3 %s/%s vers a 200-ból), '
           'de ott az aranyba eső versek száma kicsi (R2+R3: %s aranyvers, ebből mindkét futás átment: %s).' % (
               r2[4], r2[5], r3[4], r3[5], n23[5], n23[4]),
           '4. **Az ingadozás-becslés egyetlen futáspár** (F3V2 és F3V2B, prompt_v2, arany v3-ra mérve; ugyanazon az aranyversek-halmazon a kapun átment verseken), '
           'tehát maga is zajos; a jelölések („0∉”, „>zaj”) leíró jelölések, nem szignifikanciapróbák, és a rétegenkénti cellák kis n-ű mintán (rétegenként 10–20 aranyvers) alapulnak.',
           '5. A pontosság/lefedettség linkszintű, a bootstrap a versek felett, rétegzetten történik; a közös (mindkét futás által átment) halmaz a kapuhibás versek '
           'kiesése miatt kisebb lehet a saját halmazoknál (l. a) és f) szakasz).',
           '6. A KJV-sor hossza a bemenetben és a bemeneti többlet token a köteg-szintű táblában áll; a futásnapló költségsorai az újrakéréseket is tartalmazzák, '
           'ezért a teljes költség-különbség nem csak a KJV-sor hatása.', '']
    return '\n'.join(ki) + '\n'


def _atlag(sor):
    return '%.0f (%s/%s)' % (int(sor[4]) / int(sor[5]), sor[4], sor[5]) if int(sor[5]) else '—'


def adat_reteg(S, ig):
    return [s[2] for s in S if s[0] == 'erintett_kimaradt' and s[3] == ig][0]


def kiir(sorok, info, ts, er, adat, eredmeny_ut, jelentes_ut):
    fej = fejlec(info, ts)
    with open(eredmeny_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# ' + fej + '\n')
        f.write('\t'.join(['szakasz', 'osszeallitas', 'reteg', 'mero', 'szamlalo', 'nevezo', 'megjegyzes']) + '\n')
        for s in sorok.lista:
            assert all('\t' not in x for x in s), s
            f.write('\t'.join(s) + '\n')
    txt = jelentes_szoveg(sorok, info, ts, er, adat)
    # a példa-leírásokhoz az eredeti szavak is: a szó-szintű sorok megjegyzésében állnak (erintett_szo)
    with open(jelentes_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)


def fut(forras_dir=None, arany_ut=None, arany_sha=None, eredmeny_ut=None, jelentes_ut=None, ts=None, n_boot=N_BOOT, mentett=True):
    adat, info, sorok, er = szamol(forras_dir, arany_ut, arany_sha, n_boot, mentett)
    kiir(sorok, info, ts or tokenek.generalas_ts(), er, adat, eredmeny_ut or EREDMENY_UT, jelentes_ut or JELENTES_UT)
    print('kész: %d sor -> %s, %s' % (len(sorok.lista), eredmeny_ut or EREDMENY_UT, jelentes_ut or JELENTES_UT))
    rossz = [s for s in sorok.lista if s[0] in ('kapuhiba_kereszt', 'kjv_kereszt') and 'ELTÉR' in s[6]]
    if rossz:
        print('FIGYELEM: keresztellenőrzés eltér: %s' % [(s[0], s[1], s[3]) for s in rossz], file=sys.stderr)
        return 1
    return 0


# ---------------------------------------------------------------------------
# önteszt (mock-adat, determinisztikus)
# ---------------------------------------------------------------------------

def mock_general(mappa):
    """Mock-futások (F3V3, F8V3, F3V2, F3V2B) a mappában: az arany v3 szerinti válaszok futásonként módosítva
    (a P3cMock szabálya: az igehely hash-e szerint), futásszintű kapuhibákkal. Nincs hálózat."""
    import contextlib
    import io
    import json
    import shutil
    import bemenet
    import futtat
    import p3c_mock
    arany = {}
    with open(ARANY_UT, encoding='utf-8') as f:
        for s in f:
            if s.strip():
                o = json.loads(s)
                arany[o['vers']] = o
    minta = futtat.minta_betolt()
    ig_all = [s['igehely'] for s in minta]
    gold = [ig for ig in ig_all if ig in arany]
    hibas_mindig = {REF: {gold[7]}, CEL: {gold[11]}, Z1: {gold[13]}}
    hibas_elso = {REF: {gold[5]}, CEL: {gold[9]}, Z2: {gold[15]}}
    mock = p3c_mock.P3cMock(arany, hibas_mindig, hibas_elso)
    os.makedirs(mappa, exist_ok=True)
    tmp_v3 = os.path.join(mappa, 'prompt_v3_teszt.md')
    with open(bemenet.PROMPT_V2_UT, encoding='utf-8') as f:
        v2 = f.read()
    with open(tmp_v3, 'w', encoding='utf-8', newline='\n') as f:
        f.write(v2.replace(bemenet.VEGE, '\nKJV-mérés mock: a prompt_v3 ideiglenes helyettesítője.\n' + bemenet.VEGE))
    eredeti_prompt = {f: futtat.FUTASOK[f]['prompt'] for f in futtat.V3_FUTASOK}
    eredeti_elt = dict(p3c_mock.ELTERES)
    try:
        for f in futtat.V3_FUTASOK:
            futtat.FUTASOK[f]['prompt'] = tmp_v3
        p3c_mock.ELTERES.update({REF: (3, 0), CEL: (4, 0), Z1: (5, 0), Z2: (5, 2)})
        ctx = futtat.Kontextus(mock, 'mock-kulcs-nem-titok', mappa, plafon=futtat.PLAFON_USD)
        for f in FUTASOK:
            mock.futas = f
            with contextlib.redirect_stdout(io.StringIO()):
                kod = futtat.futasok_vegrehajt(ctx, [f], minta)
            assert kod == 0, (f, kod)
    finally:
        for f, p in eredeti_prompt.items():
            futtat.FUTASOK[f]['prompt'] = p
        p3c_mock.ELTERES.clear()
        p3c_mock.ELTERES.update(eredeti_elt)
    arany_ut = os.path.join(mappa, 'arany_teszt.jsonl')
    shutil.copyfile(ARANY_UT, arany_ut)
    with open(os.path.join(mappa, 'arany_teszt.sha256'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('%s  arany_teszt.jsonl\n' % tokenek.sha256_lf(arany_ut))
    return {'mappa': mappa, 'arany_ut': arany_ut, 'arany_sha': os.path.join(mappa, 'arany_teszt.sha256'), 'gold': gold,
            'hibas_mindig': hibas_mindig, 'hibas_elso': hibas_elso}


def onteszt():
    import contextlib
    import io
    import json
    import shutil
    import bemenet
    import p3c_mock
    hibak = []

    def ellen(f, leiras):
        if not f:
            hibak.append(leiras)

    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'a régi kimenetek megváltoztak: %s' % p3c_mock.regi_kimenetek_hibak())

    # --- a link- és szó-besorolás kézzel
    G, S, T = {(1, 1), (2, 2), (3, 3)}, {(1, 1), (2, 9), (4, 4)}, {(1, 1), (2, 2), (3, 8), (5, 5)}
    lb = link_besorol(G, S, T)
    ellen(lb == {'hiany_potolva': [(2, 2)], 'tobblet_megszunt': [(2, 9), (4, 4)], 'hiany_uj': [], 'tobblet_uj': [(3, 8), (5, 5)]},
          'link_besorol hibás: %s' % lb)
    lb2 = link_besorol(G, T, S)           # a fordított összevetés: a javult/romlott felcserélődik
    ellen(lb2['hiany_uj'] == [(2, 2)] and lb2['hiany_potolva'] == [] and lb2['tobblet_uj'] == [(2, 9), (4, 4)],
          'link_besorol a fordított irányban hibás: %s' % lb2)
    ellen(szo_besorol({1}, {2}, {1}) == 'javult' and szo_besorol({1}, {1}, {2}) == 'romlott'
          and szo_besorol({1}, {2}, {3}) == 'valtozott_rossz_marad' and szo_besorol({1}, {1}, {1}) == 'nem_valtozott_jo'
          and szo_besorol({1}, {2}, {2}) == 'nem_valtozott_rossz' and szo_besorol({1, 2}, {1}, {1, 2}) == 'javult',
          'szo_besorol hibás')

    # --- a páros bootstrap kézzel: azonos futások: Δ = 0 és az intervallum [0; 0]; következetes javulás: az intervallum > 0
    gold0 = {'v%d' % i: ('R1' if i < 6 else 'R2', (3, 4, 3, 4, 5)) for i in range(12)}
    kap0 = {'v%d' % i: ('R1' if i < 6 else 'R2', (0, 0, 0, 0)) for i in range(12)}
    r0 = boot_delta(gold0, kap0, {'R1': ['R1'], 'Összes': ['R1', 'R2']}, 200)
    ellen(all(v[2] == 0 and v[3] == 0 and v[4] == 0 for g in r0.values() for v in g.values()), 'boot_delta: azonos futásoknál a Δ nem nulla: %s' % r0)
    gold1 = {k: (r, (3, 4, 4, 4, 5)) for k, (r, _) in gold0.items()}
    kap1 = {k: (r, (1, 1, 0, 0)) for k, (r, _) in kap0.items()}
    r1 = boot_delta(gold1, kap1, {'Összes': ['R1', 'R2']}, 200)
    ellen(abs(r1['Összes']['pontossag'][2] - 0.25) < 1e-12 and abs(r1['Összes']['pontossag'][3] - 0.25) < 1e-12
          and abs(r1['Összes']['lefedettseg'][2] - 0.2) < 1e-12 and r1['Összes']['kapuhiba_elso_probara'][2] == -1.0 and r1['Összes']['kapuhiba_vegleg'][3] == -1.0,
          'boot_delta: a következetes javulás Δ-ja/intervalluma hibás: %s' % r1)
    # vegyes: a Δ pontbecslése az összegek hányadosa, az intervallum tartalmazza; a páros-minta determinisztikus
    gold2 = {'a': ('R1', (1, 2, 2, 2, 2)), 'b': ('R1', (2, 2, 1, 2, 2)), 'c': ('R1', (2, 2, 2, 2, 2)), 'd': ('R1', (0, 1, 1, 1, 2))}
    ra = boot_delta(gold2, {'a': ('R1', (0, 0, 0, 0))}, {'R1': ['R1']}, 300)
    rb = boot_delta(gold2, {'a': ('R1', (0, 0, 0, 0))}, {'R1': ['R1']}, 300)
    ellen(ra == rb, 'boot_delta nem determinisztikus')
    ref, cel, dl, lo, hi, ng, nk = ra['R1']['pontossag']
    ellen(abs(ref - 5 / 7) < 1e-12 and abs(cel - 6 / 7) < 1e-12 and abs(dl - 1 / 7) < 1e-12 and lo <= dl <= hi and ng == 4 and nk == 1,
          'boot_delta: a pontbecslés hibás: %s' % (ra,))

    # --- a KJV-sor hossza = a versblokk-különbség
    for ig, forras in (('1Móz 4:9', 'regi'), ('1Móz 4:9', 'teljes'), ('Zsolt 23:1', 'teljes'), ('Mt 24:38', 'teljes')):
        d = len(bemenet.versblokk(ig, True, forras)) - len(bemenet.versblokk(ig, False))
        ellen(kjv_sor_hossz(ig, forras) == d, 'kjv_sor_hossz(%s, %s) = %d, a versblokk-különbség %d' % (ig, forras, kjv_sor_hossz(ig, forras), d))
    ellen(kjv_sor_hossz('Mt 24:38', 'regi') == 0, 'a régi táblában nincs ÚSZ KJV-sor, a hossz 0 kell legyen')

    # --- mock-adatos teljes menet
    mappa = p3c_mock.ideiglenes('f21p_onteszt_meres_kjv_')
    try:
        info = mock_general(mappa)
        ut_e, ut_j = os.path.join(mappa, 'eredmeny.tsv'), os.path.join(mappa, 'jelentes.md')
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_e, ut_j, ts='T1', n_boot=100)
        ellen(kod == 0, 'a mock-futás kilépési kódja %d' % kod)
        with open(ut_e, encoding='utf-8') as f:
            tsv1 = f.read()
        with open(ut_j, encoding='utf-8') as f:
            md1 = f.read()
        sor0 = tsv1.split('\n')[0]
        ellen(sor0.startswith('# GENERÁLT: eszkozok/karoli_strong/meres_kjv.py | scope=') and ' | forras=' in sor0 and ' | ts=T1 ' in sor0,
              'a TSV fejléce nem a scope|forras|ts proveniencia: %s' % sor0[:120])
        ellen('scope=' in md1 and 'forras=' in md1 and 'ts=T1' in md1, 'az md nem viseli a proveniencia-fejlécet')
        with contextlib.redirect_stdout(io.StringIO()):
            fut(mappa, info['arany_ut'], info['arany_sha'], ut_e, ut_j, ts='T2', n_boot=100)
        with open(ut_e, encoding='utf-8') as f:
            tsv2 = f.read()
        with open(ut_j, encoding='utf-8') as f:
            md2 = f.read()
        ellen(tsv1.replace('ts=T1 ', 'ts=T2 ') == tsv2 and md1.replace('ts=T1', 'ts=T2') == md2, 'a futás nem determinisztikus (a ts-en kívül eltérés)')
        ellen(all(len(x.split('\t')) == 7 for x in tsv2.split('\n')[2:] if x), 'a TSV-sorok nem mind 7 mezősek')
        adat, ainfo, sk, er = szamol(mappa, info['arany_ut'], info['arany_sha'], n_boot=60)
        S = sk.lista

        def ert(szakasz, oss, ret, mero):
            x = [s for s in S if s[0] == szakasz and s[1] == oss and s[2] == ret and s[3] == mero]
            if not x:
                return None
            return (int(x[0][4]), int(x[0][5]) if x[0][5] != '' else None)

        # független újraszámolás a nyers jsonl-ből
        def futas_linkek(f):
            ki = {}
            with open(os.path.join(mappa, 'valaszok', '%s.jsonl' % f), encoding='utf-8') as fh:
                for s in fh:
                    if s.strip():
                        for ig, v in json.loads(s)['versek'].items():
                            ki[ig] = None if v['allapot'] != 'ok' else {(p[0], e) for p in v['obj']['parok'] for e in p[1]}
            return ki
        kiz = tokenek.meres_kizaras()
        gold = {}
        with open(info['arany_ut'], encoding='utf-8') as fh:
            for s in fh:
                if s.strip():
                    o = json.loads(s)
                    gold[o['vers']] = {(p[0], e) for p in o['parok'] for e in p[1] if (o['vers'], e) not in kiz}

        def szur(ig, x):
            return None if x is None else {(k, e) for k, e in x if (ig, e) not in kiz}
        lr = {ig: szur(ig, x) for ig, x in futas_linkek(REF).items()}
        lc = {ig: szur(ig, x) for ig, x in futas_linkek(CEL).items()}
        t_r = c_r = t_c = c_c = g_ = 0
        cnt = {k: 0 for k in ('hiany_potolva', 'tobblet_megszunt', 'hiany_uj', 'tobblet_uj')}
        szo = {k: 0 for k in ('javult', 'romlott', 'valtozott_rossz_marad', 'nem_valtozott_jo', 'nem_valtozott_rossz')}
        nv = 0
        for ig, G in gold.items():
            a, b = lr[ig], lc[ig]
            if a is None or b is None:
                continue
            nv += 1
            t_r += len(a & G)
            c_r += len(a)
            t_c += len(b & G)
            c_c += len(b)
            g_ += len(G)
            cnt['hiany_potolva'] += len((G & b) - a)
            cnt['tobblet_megszunt'] += len((a - G) - b)
            cnt['hiany_uj'] += len((G & a) - b)
            cnt['tobblet_uj'] += len((b - G) - a)
            for k in {x for x, _ in G | a | b}:
                g1 = {e for x, e in G if x == k}
                s1 = {e for x, e in a if x == k}
                t1 = {e for x, e in b if x == k}
                if s1 == t1:
                    szo['nem_valtozott_jo' if s1 == g1 else 'nem_valtozott_rossz'] += 1
                elif t1 == g1:
                    szo['javult'] += 1
                elif s1 == g1:
                    szo['romlott'] += 1
                else:
                    szo['valtozott_rossz_marad'] += 1
        ellen(ert('kozos', '%s [pár: %s–%s]' % (REF, REF, CEL), meres.OSSZES, 'pontossag') == (t_r, c_r), 'kozos F3V3 pontosság eltér a független számítástól')
        ellen(ert('kozos', '%s [pár: %s–%s]' % (CEL, REF, CEL), meres.OSSZES, 'pontossag') == (t_c, c_c), 'kozos F8V3 pontosság eltér')
        ellen(ert('kozos', '%s [pár: %s–%s]' % (CEL, REF, CEL), meres.OSSZES, 'lefedettseg') == (t_c, g_), 'kozos F8V3 lefedettség eltér')
        ellen(ert('erintett_szamok', '%s/%s' % (REF, CEL), meres.OSSZES, 'aranyversek_mindketto_atment')[0] == nv, 'az érintett aranyversek száma eltér')
        for k, x in cnt.items():
            ellen(ert('erintett_szamok', '%s/%s' % (REF, CEL), meres.OSSZES, 'link_%s' % k)[0] == x, 'érintett link-szám eltér (%s)' % k)
        for k, x in szo.items():
            ellen(ert('erintett_szamok', '%s/%s' % (REF, CEL), meres.OSSZES, 'szo_%s' % k)[0] == x, 'érintett szó-szám eltér (%s)' % k)
        ellen(cnt['hiany_potolva'] + cnt['tobblet_megszunt'] > 0 and cnt['hiany_uj'] + cnt['tobblet_uj'] > 0 and szo['javult'] > 0 and szo['romlott'] > 0,
              'a mock nem ad javult és romlott szót is (%s %s): a teszt nem fedi az eseteket' % (cnt, szo))
        ellen(len([s for s in S if s[0] == 'erintett_szo' and s[1] == 'javult']) == szo['javult'], 'az erintett_szo sorok száma (javult) eltér')
        # a kapuhibás aranyvers kimarad az érintettek közül, és a kimaradt-sor megvan
        kim = {s[3] for s in S if s[0] == 'erintett_kimaradt'}
        ellen(info['gold'][7] in kim or info['gold'][11] in kim, 'a végleges kapuhibás aranyvers nem szerepel az erintett_kimaradt sorok között')
        # kapuhiba-keresztellenőrzés, mentett ellenőrzés, kjv-keresztellenőrzés
        kk = [s for s in S if s[0] == 'kapuhiba_kereszt']
        ellen(len(kk) == 4 and all('EGYEZIK' in s[6] for s in kk), 'kapuhiba-keresztellenőrzés: %s' % [s[6] for s in kk])
        ellen(all(s[4] == '0' for s in S if s[0] == 'mentett_ellenorzes') and len([s for s in S if s[0] == 'mentett_ellenorzes']) == 4,
              'mentett ellenőrzés hibát ad / nem fedi a 4 futást')
        kj = [s for s in S if s[0] == 'kjv_kereszt' and 'ELTÉR' in s[6]]
        ellen(not kj, 'a kjv-keresztellenőrzés eltér a mockban: %s' % [s[6] for s in kj])
        # a kapuhiba végleges soraiban a beültetett hibás versek ott vannak
        vv = {(s[1], s[3]) for s in S if s[0] == 'kapuhiba_vegleges_versek'}
        ellen((REF, info['gold'][7]) in vv and (CEL, info['gold'][11]) in vv, 'a beültetett végleges kapuhibák nem látszanak: %s' % sorted(vv))
        # a hatas sorok alakja, a hatas_osszevetes jelölés
        ho = [s for s in S if s[0] == 'hatas_osszevetes']
        ellen(len({s[2] for s in ho}) == len(CSOP_NEVEK) and len({s[3] for s in ho}) == 4, 'a hatas_osszevetes sorok nem fedik a csoportokat/mérőszámokat')
        ellen(all(len(s[4].split('|')) == 4 and len(s[5].split('|')) == 4 and 'abs_delta_nagyobb_az_ingadozasnal=' in s[6] for s in ho),
              'a hatas_osszevetes sorok alakja hibás')
        # a KJV-sor hossza a mockban: az F8V3 R4-en nincs, R1-en van; a köteg-összeg = a versek összege
        ellen(ert('kjv_hossz', CEL, 'R4', 'versek_kjv_sorral')[0] == 0 and ert('kjv_hossz', CEL, 'R1', 'versek_kjv_sorral')[0] == 100, 'a KJV-sor jelenléte az F8V3-ban hibás')
        ellen(ert('kjv_hossz', REF, 'R2', 'versek_kjv_sorral')[0] == 0 and ert('kjv_hossz', REF, 'R1', 'versek_kjv_sorral')[0] == 100, 'a KJV-sor jelenléte az F3V3-ban hibás')
        tot = sum(int(s[4]) for s in S if s[0] == 'kjv_hossz' and s[1] == CEL and s[2] == meres.OSSZES and s[3] == 'kjv_sor_karakter_osszes')
        tk = sum(int(s[4]) for s in S if s[0] == 'kjv_hossz_koteg' and s[1] == CEL and s[3] == 'kjv_karakter_koteg_atlag')
        ellen(tot == tk, 'a KJV-sor karakter-összege (%d) nem egyezik a köteg-összegekkel (%d)' % (tot, tk))
        # példák: legfeljebb 8 + 5, csak R2–R3, determinisztikus kiválasztás
        _, _, szavak, peldak = er
        ellen(len(peldak) <= 13 and all(p['reteg'] in ('R2', 'R3') for p in peldak), 'a példák száma/rétege hibás')
        ellen([id(p) for p in peldak_valaszt(adat, szavak)] == [id(p) for p in peldak], 'a példa-kiválasztás nem determinisztikus')
        # költség: az F8V3 baleseti sorok külön
        ellen(ert('koltseg', 'F8V3 ebből baleseti kötegek (1+2)', meres.OSSZES, 'hivasok') is not None, 'a baleseti köteg-sor hiányzik a költségből')
        # hash-ellenőrzés: a módosított arany SystemExit, semmi nem íródik
        rossz = os.path.join(mappa, 'arany_rossz.jsonl')
        shutil.copyfile(info['arany_ut'], rossz)
        with open(rossz, 'a', encoding='utf-8', newline='\n') as f:
            f.write('{"vers":"x","parok":[],"betoldas":[],"forditatlan":[]}\n')
        shutil.copyfile(info['arany_sha'], os.path.join(mappa, 'arany_rossz.sha256'))
        ut_x = os.path.join(mappa, 'nem_irodik.tsv')
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fut(mappa, rossz, None, ut_x, os.path.join(mappa, 'nem_irodik.md'), n_boot=10)
            ellen(False, 'az eltérő hash-ű arany nem állította meg a mérést')
        except SystemExit as e:
            ellen('sha256' in str(e) and not os.path.exists(ut_x), 'az eltérő hash hibaüzenete/mellékhatása hibás: %s' % e)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fut(mappa, rossz, os.path.join(mappa, 'nincs.sha256'), ut_x, os.path.join(mappa, 'nem_irodik.md'), n_boot=10)
            ellen(False, 'a hiányzó hash-fájl nem állította meg a mérést')
        except SystemExit as e:
            ellen('hiányzik' in str(e), 'a hiányzó hash-fájl hibaüzenete hibás: %s' % e)
        # a repó arany v3-ja létező, hash-ellenőrzött fájl
        ellen(tokenek.hash_hiba(ARANY_UT, ARANY_SHA) is None, 'a repó arany v3-ja hash-hibás')
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('meres_kjv önteszt rendben (link- és szó-besorolás, páros bootstrap kézzel és determinizmus, KJV-sor hossza a versblokkhoz mérve, '
          'független újraszámolás a mock-adaton, kapuhiba-keresztellenőrzés, hash-ellenőrzés, régi kimenetek bájtazonossága)')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--arany', default=None, help='az arany jsonl-je (alap: f21p/arany_opus_v3.jsonl)')
    ap.add_argument('--arany-sha', default=None, help='a hash-fájl (alap: az --arany neve .sha256 kiterjesztéssel; nélküle f21p/arany_opus_v3.sha256)')
    ap.add_argument('--forras-dir', default=None, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    return fut(args.forras_dir, args.arany, args.arany_sha)


if __name__ == '__main__':
    sys.exit(main())
