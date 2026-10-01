#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.60 — szkriptes előpárosítás (kísérlet, API nélkül): szótár + determinisztikus párosító,
mérés az arany v3-on. Nem minősítés: a kimenet mért szám, döntési szabályhoz nem viszonyít.

1. SZÓTÁR (--szotar). Forrás: a C két prompt_v2-es futása (f21p/valaszok/F3V2.jsonl,
   F3V2B.jsonl), csak a MINDKÉT futásban kapun átment (allapot=ok) versek, az arany v3
   (f21p/arany_opus_v3.jsonl) igehelyei KIZÁRVA. Egyező link = az a (magyar sorszám, eredeti
   sorszám) pár, amely ugyanabban a versben mindkét futás linkjei között szerepel (metszet).
   Minden egyező linkből egy (szóalak, Strong) pár lesz:
     * szóalak = a tokenek.tokenizal() tokenje, csak kisbetűsítve (str.lower), az ékezetek és a
       Károli-helyesírás (pl. „melylyel”) változatlanok; más normalizálás (tő, toldalék) nincs:
       a szótár szóalak-szintű, „nyers”.
     * Strong = a tokenek.betolt_eredeti() 'strong' mezője változatlanul (összetett Strong, pl.
       'G2532+G1473', egy egész karakterlánc).
   Kizárva a szótárból (a K1/K8/K9 szabályok hatásköre, hogy ne ütközzenek):
     * minden Strong, amelynek valamelyik ('+' menti) összetevője H9xxx (héber grammatikai
       elő-/utórag: névelő, ve-, elöljárók, ragok, H9012/H9013), G3588 (görög névelő) vagy
       G2532 (καί, a krázisos összetett alakokkal együtt, pl. κἀγώ = G2532+G1473);
     * a magyar 'a', 'az' (K1) és 'és', 's' (K9) szóalak.
   Felvétel: (i) a (szóalak, Strong) pár az egyező linkek között összesen >= 3-szor szerepel,
   ÉS (ii) a szóalakhoz az egyező linkek között (a kizárások után) más Strong nem tartozik.
   Ha van versengő Strong, a szóalak kimarad („versengés”), akkor is, ha az egyik pár >= 3;
   különben, ha a db < 3, „kevés előfordulás”. Kimenet: f21p/szotar_elopar.tsv.

2. PÁROSÍTÓ (parosit). Bemenet egy vers: Károli-tokenek, eredeti szavak (sorsz, strong,
   alak, tukor, nem_tr) és a szótár. Nem használ KJV-t és modellválaszt. A [nem TR] eredeti
   szót egyik szabály sem dönti el (oka: nem_tr; a TR-szabály, K, nincs a feladatban).
   (1) Szótár: a magyar token szóalakja a szótárban → Strong S. Egy versben S-re: magyar
       igénylők = a vers azon tokenjei, amelyek szótári Strongja S; jelöltek = a vers azon
       (TR-es) eredeti szavai, amelyek Strongja S. Döntés csak 1 igénylő : 1 jelölt esetén
       (link k → e); különben minden igénylő „modellre vár”: tobb_magyar (>= 2 igénylő:
       ismételt szóalak vagy két szóalak ugyanarra a Strongra), nincs_jelolt, tobb_jelolt.
   (2) K1 (A szabály). Magyar 'a'/'az' → betoldas, ha névelőként áll: van utána token, az
       nem vonatkozó névmás / kötőszó (a ki, a mely, a mint, a hogy, a mi ... lista: VONATKOZO),
       nem névutó (az előtt, a mellett ...: NEVUTO), nem 'a', 'az', 'is', és a névelőalak illik
       a következő szóhoz (a + mássalhangzó, az + magánhangzó). Különben „modellre vár”
       (K1_kivetel: névmási használat lehet). Eredeti H9009 / G3588 → forditatlan, ha az angol
       tükörfordítás puszta névelő (a < > és a [is]/[was]/... betoldás lehántása után csak
       'the', esetleg elöljáróval: of/to/in/with/on/for/by/at/from/than the), ÉS a magyar
       versben nincs e/ez/ezen/eme/emez/ama token (J szabály: a mutató névmás a névelő sorára
       mehet). Különben „modellre vár” (K1_kivetel_nevmasi, ill. K1_kivetel_J).
   (3) K8 (H szabály). H9012, H9013 → forditatlan.
   (4) K9 (I szabály). ve- = H9001, H9002; καί = G2532 (pontosan; az összetett krázis nem).
       Kötőszó-szavak (a szabály listája): és, s, pedig, is, de, hogy. Konzervatív bővítés a
       „nincs kötőszó” vizsgálathoz: mind, se, sem, sőt (a καί/ve- szokásos magyar alakjai a
       mind…mind, sem, sőt szerkezetben).
       (a) a magyar versben nincs sem kötőszó-szó, sem bővítő szó → minden ve-/καί forditatlan
           (K9_nincs_kotoszo);
       (b) a versben pontosan egy (TR-es) ve-/καί van, a magyar kötőszó-szavak közül pontosan
           egy áll, az 'és' vagy 's', bővítő szó nincs, és az eredetiben nincs τε (G5037) →
           link: az 'és'/'s' → a ve-/καί (K9_egy_es);
       (c) minden más esetben a ve-/καί és a magyar kötőszó „modellre vár” (K9_nem_gepies).
       A pozíciós megfeleltetést (melyik és melyik ve-hez) a szkript nem kísérli meg.
   Minden más magyar token és eredeti szó „modellre vár”.

3. MÉRÉS (--meres) az arany v3-on (60 vers; LF-normalizált sha256 a f21p/arany_opus_v3.sha256
   ellen, tokenek.hash_hiba), rétegenként (f21p/minta.tsv: R1–R4 + Összes), a
   f21p/meres_kizaras.tsv eredeti tokenjeit érintő linkek / forditatlan-tételek mindkét
   oldalról kimaradnak (mint a meres.py). Gépi ellenőrzés: szótár-forrásversek ∩ arany = ∅,
   különben SystemExit. Egység: link (k, e), betoldas k, forditatlan e. A C-összevetés
   egységenkénti igen/nem kérdés: a szkript minden döntése „igen” erre az egységre; a C
   ugyanarra az egységre igent mond, ha az egység benne van a C kimenetében (csak a C-ben
   kapun átment versek). Wilson 90%: meres.wilson (linkszintű, optimista).
   Kimenet: f21p/elopar_eredmeny.tsv, naplok/F21P_elopar.md.

Használat:
    python eszkozok/karoli_strong/elopar.py            (szótár + mérés)
    python eszkozok/karoli_strong/elopar.py --szotar   (csak szótár)
    python eszkozok/karoli_strong/elopar.py --meres    (mérés a meglévő szótárral)
    python eszkozok/karoli_strong/elopar.py --onteszt  (mock-önteszt, nem ír a repóba)
"""

import json
import os
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meres  # noqa: E402
import tokenek  # noqa: E402

F21P = meres.F21P
SZOTAR_UT = os.path.join(F21P, 'szotar_elopar.tsv')
EREDMENY_UT = os.path.join(F21P, 'elopar_eredmeny.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_elopar.md')
SZOTAR_FUTASOK = ('F3V2', 'F3V2B')
C_FUTASOK = ('F3V2', 'F3V2B', 'F3V3')
RETEGEK = meres.RETEGEK + [meres.OSSZES]
MIN_DB = 3

NEVELO = {'a', 'az'}
KOTOSZO = {'és', 's', 'pedig', 'is', 'de', 'hogy'}
K9_BOVITO = {'mind', 'se', 'sem', 'sőt'}
ES = {'és', 's'}
MUTATO_J = {'e', 'ez', 'ezen', 'eme', 'emez', 'ama'}
SZOTAR_KIZART_SZOALAK = NEVELO | ES
MAGANHANGZO = set('aáeéiíoóöőuúüű')
VONATKOZO = {
    'ki', 'kik', 'kit', 'kiket', 'kinek', 'kiknek', 'kitől', 'kiktől', 'kiért', 'kivel', 'kikkel',
    'kiben', 'kikben', 'kiből', 'kihez', 'kikhez', 'kire', 'kikre', 'kié', 'kiké', 'kiről',
    'mely', 'melyek', 'melyet', 'melyeket', 'melynek', 'melyeknek', 'melyben', 'melyekben',
    'melyből', 'melyekből', 'melyre', 'melyekre', 'melyen', 'melyeken', 'melylyel', 'mellyel',
    'melyekkel', 'melytől', 'melyektől', 'melyért', 'melyhez', 'melyekhez', 'melyről', 'melyig',
    'mi', 'mik', 'mit', 'miket', 'minek', 'miben', 'miből', 'mire', 'min', 'mivel', 'miért',
    'mihez', 'mitől', 'miről', 'mint', 'miképen', 'miként', 'hogy', 'mikor', 'midőn', 'mig',
    'míg', 'meddig', 'hol', 'honnan', 'hová', 'hova', 'mennyi', 'mennyire',
}
NEVUTO = {
    'előtt', 'után', 'alatt', 'által', 'felett', 'fölött', 'mellett', 'miatt', 'közé', 'között',
    'közül', 'ellen', 'iránt', 'szerint', 'nélkül', 'óta', 'helyett', 'végett', 'felé', 'mögött',
    'mellé', 'mögé', 'elé', 'alá', 'fölé', 'felől', 'körül', 'kívül', 'belől', 'végre', 'utána',
}
TUKOR_ELOLJARO = {'of', 'to', 'in', 'with', 'on', 'for', 'by', 'at', 'from', 'than'}
TUKOR_LETIGE = ('[is]', '[was]', '[are]', '[were]', '[will be]', '[am]', '[be]')
VE_KAI = {'H9001', 'H9002', 'G2532'}
K8_STRONG = {'H9012', 'H9013'}
NEVELO_STRONG = {'H9009', 'G3588'}
SZABALY_CSOPORT = {'szotar': 'szótár', 'K1': 'K1', 'K8': 'K8', 'K9_nincs_kotoszo': 'K9', 'K9_egy_es': 'K9'}


# ---------------------------------------------------------------------------
# 1. szótár
# ---------------------------------------------------------------------------

def szotar_kizart_strong(strong):
    """Igaz, ha a Strong valamelyik ('+' menti) összetevője H9xxx, G3588 vagy G2532."""
    for s in strong.split('+'):
        if s.startswith('H9') or s in ('G3588', 'G2532'):
            return True
    return False


def futas_linkek(obj):
    """Egy kapun átment vers objektumából a linkhalmaz {(magyar, eredeti)}."""
    return {(p[0], e) for p in obj['parok'] for e in p[1]}


def szotar_epit(futas_a, futas_b, karoli, ered, kizart_versek, min_db=MIN_DB):
    """(szotar, statisztika, forrasversek).

    futas_a, futas_b: {igehely: rekord} (rekord: {'allapot', 'obj'}); csak a mindkettőben 'ok'
    versek, a kizart_versek (az arany igehelyei) nélkül. szotar: {szóalak: (strong, db, vers_db)}.
    """
    forras = sorted(ig for ig in futas_a
                    if ig in futas_b and futas_a[ig]['allapot'] == 'ok' and futas_b[ig]['allapot'] == 'ok'
                    and ig not in kizart_versek)
    par_db = Counter()
    par_versek = defaultdict(set)
    par_tokenek = defaultdict(set)   # (vers, magyar sorszám): tájékoztató, a db link-szintű
    egyezo = kizart_strong = kizart_szoalak = 0
    for ig in forras:
        tl = tokenek.tokenizal(karoli[ig])
        ew = ered[ig]
        kozos = futas_linkek(futas_a[ig]['obj']) & futas_linkek(futas_b[ig]['obj'])
        for k, e in sorted(kozos):
            egyezo += 1
            szo = tl[k - 1].lower()
            strong = ew[e - 1]['strong']
            if szotar_kizart_strong(strong):
                kizart_strong += 1
                continue
            if szo in SZOTAR_KIZART_SZOALAK:
                kizart_szoalak += 1
                continue
            par_db[(szo, strong)] += 1
            par_versek[(szo, strong)].add(ig)
            par_tokenek[(szo, strong)].add((ig, k))
    strongok = defaultdict(set)
    for (szo, strong) in par_db:
        strongok[szo].add(strong)
    szotar = {}
    verseng = keves = 0
    verseng_dominans = 0
    for szo in sorted(strongok):
        if len(strongok[szo]) > 1:
            verseng += 1
            if any(par_db[(szo, s)] >= min_db for s in strongok[szo]):
                verseng_dominans += 1
            continue
        strong = next(iter(strongok[szo]))
        if par_db[(szo, strong)] < min_db:
            keves += 1
            continue
        szotar[szo] = (strong, par_db[(szo, strong)], len(par_versek[(szo, strong)]))
    stat = {
        'forrasversek': len(forras),
        'egyezo_linkek': egyezo,
        'kizart_link_strong_miatt': kizart_strong,
        'kizart_link_szoalak_miatt': kizart_szoalak,
        'szotarjelolt_parok': len(par_db),
        'szotarjelolt_szoalakok': len(strongok),
        'kiesett_versenges': verseng,
        'kiesett_versenges_de_volt_3_feletti_par': verseng_dominans,
        'kiesett_keves': keves,
        'szotar_meret': len(szotar),
        'szotar_lefedett_linkek': sum(v[1] for v in szotar.values()),
        'szotar_bejegyzes_3_alatti_token_elofordulassal': sum(
            1 for szo, v in szotar.items() if len(par_tokenek[(szo, v[0])]) < min_db),
    }
    return szotar, stat, forras


def szotar_ir(szotar, stat, ut=SZOTAR_UT, ts=None):
    ts = ts or tokenek.generalas_ts()
    fej = ('# GENERÁLT: eszkozok/karoli_strong/elopar.py --szotar | scope=f21p, F3V2 ∩ F3V2B egyező '
           'linkjei, mindkét futásban kapun átment versek, az arany v3 60 verse kizárva (%d forrásvers) | '
           'forras=f21p/valaszok/F3V2.jsonl, f21p/valaszok/F3V2B.jsonl, konkordancia/Karoli_1908.tsv, '
           'konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, f21p/arany_opus_v3.jsonl '
           '(csak az igehelyek kizárásához) | ts=%s | feltétel: db >= %d és egyértelmű szóalak; kizárva: '
           'H9xxx, G3588, G2532 összetevőjű Strong, a/az/és/s szóalak | kézzel szerkeszteni tilos'
           % (stat['forrasversek'], ts, MIN_DB))
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + '\n')
        f.write('# statisztika: ' + '; '.join('%s=%s' % (k, v) for k, v in stat.items()) + '\n')
        f.write('\t'.join(['szoalak', 'strong', 'db', 'vers_db']) + '\n')
        for szo in sorted(szotar):
            s, db, vdb = szotar[szo]
            f.write('\t'.join([szo, s, str(db), str(vdb)]) + '\n')


def szotar_olvas(ut=SZOTAR_UT):
    """{szóalak: (strong, db, vers_db)} és a statisztika-sor szótára (split('\\t'), nincs csv)."""
    szotar, stat = {}, {}
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip()]
    adat = []
    for s in sorok:
        if s.startswith('# statisztika: '):
            for t in s[len('# statisztika: '):].split('; '):
                k, v = t.split('=', 1)
                stat[k] = int(v)
        elif not s.startswith('#'):
            adat.append(s.split('\t'))
    for r in adat[1:]:
        szotar[r[0]] = (r[1], int(r[2]), int(r[3]))
    return szotar, stat


# ---------------------------------------------------------------------------
# 2. párosító
# ---------------------------------------------------------------------------

def nevelo_e(szo, kovetkezo):
    """A magyar 'a'/'az' névelőként áll-e (gépies vizsgálat; kétes esetben False)."""
    if kovetkezo is None:
        return False
    if kovetkezo in VONATKOZO or kovetkezo in NEVUTO or kovetkezo in ('a', 'az', 'is'):
        return False
    elso = kovetkezo[0]
    if szo == 'a':
        return elso.isalpha() and elso not in MAGANHANGZO
    return elso in MAGANHANGZO


def tukor_nevelo(tukor):
    """Az angol tükörfordítás puszta névelő-e ('the', '<the>', 'of the', '[is] the' ...)."""
    s = tukor.lower().replace('<', ' ').replace('>', ' ')
    for b in TUKOR_LETIGE:
        s = s.replace(b, ' ')
    if '[' in s or ']' in s:
        return False
    szavak = [w.strip(',.;:!?·') for w in s.split()]
    szavak = [w for w in szavak if w]
    if not szavak or szavak[-1] != 'the' or szavak.count('the') != 1:
        return False
    return all(w in TUKOR_ELOLJARO for w in szavak[:-1])


def parosit(tok, ew, szotar):
    """Egy vers előpárosítása.

    tok: Károli-tokenek (eredeti írásmód); ew: eredeti szó dictek (sorsz, strong, alak, tukor,
    nem_tr); szotar: {szóalak: (strong, ...)}. Visszaad: dict
      linkek: {(k, e): szabály}, betoldas: {k: szabály}, forditatlan: {e: szabály},
      var_magyar: {k: ok}, var_eredeti: {e: ok}.
    """
    t = [x.lower() for x in tok]
    n = len(t)
    linkek, betoldas, forditatlan = {}, {}, {}
    var_m, var_e = {}, {}
    van_mutato = any(x in MUTATO_J for x in t)

    # nem_tr: egyik szabály sem dönt
    for w in ew:
        if w['nem_tr']:
            var_e[w['sorsz']] = 'nem_tr'

    # K1 magyar
    for k in range(1, n + 1):
        if t[k - 1] in NEVELO:
            kov = t[k] if k < n else None
            if nevelo_e(t[k - 1], kov):
                betoldas[k] = 'K1'
            else:
                var_m[k] = 'K1_kivetel'
    # K1 eredeti, K8
    for w in ew:
        e = w['sorsz']
        if e in var_e:
            continue
        if w['strong'] in NEVELO_STRONG:
            if van_mutato:
                var_e[e] = 'K1_kivetel_J'
            elif tukor_nevelo(w['tukor']):
                forditatlan[e] = 'K1'
            else:
                var_e[e] = 'K1_kivetel_nevmasi'
        elif w['strong'] in K8_STRONG:
            forditatlan[e] = 'K8'
    # K9
    ve = [w['sorsz'] for w in ew if w['strong'] in VE_KAI and w['sorsz'] not in var_e]
    h_kot = [k for k in range(1, n + 1) if t[k - 1] in KOTOSZO]
    h_bov = [k for k in range(1, n + 1) if t[k - 1] in K9_BOVITO]
    van_te = any(w['strong'] == 'G5037' for w in ew)
    if ve:
        if not h_kot and not h_bov:
            for e in ve:
                forditatlan[e] = 'K9_nincs_kotoszo'
        elif (len(ve) == 1 and len(h_kot) == 1 and t[h_kot[0] - 1] in ES and not h_bov and not van_te):
            linkek[(h_kot[0], ve[0])] = 'K9_egy_es'
        else:
            for e in ve:
                var_e[e] = 'K9_nem_gepies'
            for k in h_kot + h_bov:
                if t[k - 1] in ES:
                    var_m.setdefault(k, 'K9_nem_gepies')
    # szótár
    igeny = defaultdict(list)
    for k in range(1, n + 1):
        if k in betoldas or k in var_m or any(kk == k for kk, _ in linkek):
            continue
        if t[k - 1] in szotar:
            igeny[szotar[t[k - 1]][0]].append(k)
    for s in sorted(igeny):
        ks = igeny[s]
        jel = [w['sorsz'] for w in ew if w['strong'] == s and not w['nem_tr']]
        if len(ks) > 1:
            ok = 'tobb_magyar'
        elif not jel:
            ok = 'nincs_jelolt'
        elif len(jel) > 1:
            ok = 'tobb_jelolt'
        else:
            linkek[(ks[0], jel[0])] = 'szotar'
            continue
        for k in ks:
            var_m[k] = ok
    # a többi magyar token és eredeti szó: modellre vár
    dontott_m = set(betoldas) | {k for k, _ in linkek}
    for k in range(1, n + 1):
        if k not in dontott_m and k not in var_m:
            var_m[k] = 'nincs_szotarban' if t[k - 1] not in szotar else 'egyeb'
    dontott_e = set(forditatlan) | {e for _, e in linkek}
    for w in ew:
        e = w['sorsz']
        if e not in dontott_e and e not in var_e:
            var_e[e] = 'nincs_szabaly'
    assert not (set(var_m) & dontott_m), 'belső hiba: magyar token döntve és várakozó'
    assert len({k for k, _ in linkek}) == len(linkek), 'belső hiba: egy magyar token két szkript-linkben'
    return {'linkek': linkek, 'betoldas': betoldas, 'forditatlan': forditatlan,
            'var_magyar': var_m, 'var_eredeti': var_e}


# ---------------------------------------------------------------------------
# 3. mérés
# ---------------------------------------------------------------------------

def metszet_ellenoriz(forrasversek, arany_versek):
    m = set(forrasversek) & set(arany_versek)
    if m:
        raise SystemExit('HIBA: a szótár forrásversei és az arany versei metszik egymást: %s' % sorted(m))
    return 0


def betolt():
    jsonl, sha, verzio = tokenek.legfrissebb_arany()
    if verzio != 'v3':
        raise SystemExit('HIBA: az arany v3 nincs befagyasztva (%s)' % sha)
    h = tokenek.hash_hiba(jsonl, sha, 'arany v3')
    if h:
        raise SystemExit('HIBA: %s' % h)
    adat = meres.Adat(futasok=list(C_FUTASOK))
    adat.arany = {o['vers']: o for o in meres._jsonl(jsonl)}
    info = {'jsonl': jsonl, 'sha256': tokenek.sha256_lf(jsonl), 'versek': len(adat.arany)}
    return adat, info


def szotar_adatbol(adat):
    a, b = SZOTAR_FUTASOK
    return szotar_epit(adat.futas[a], adat.futas[b], adat.karoli, adat.ered, set(adat.arany))


def egysegek_arany(adat, ig):
    o = adat.arany[ig]
    lk = adat.arany_linkek(ig)
    b = set(o['betoldas'])
    f = {e for e in o['forditatlan'] if (ig, e) not in adat.kizaras}
    return lk, b, f


def egysegek_c(adat, f, ig):
    if not adat.ok(f, ig):
        return None
    o = adat.futas[f][ig]['obj']
    return (adat.linkek(f, ig), set(o['betoldas']),
            {e for e in o['forditatlan'] if (ig, e) not in adat.kizaras})


def szkript_egysegek(adat, ig, p):
    """[(egység, csoport, szabály)] a kizárásokkal; egység: ('L', k, e) / ('B', k) / ('F', e)."""
    ki = []
    for (k, e), sz in sorted(p['linkek'].items()):
        if (ig, e) in adat.kizaras:
            continue
        ki.append((('L', k, e), SZABALY_CSOPORT[sz], sz))
    for k, sz in sorted(p['betoldas'].items()):
        ki.append((('B', k), SZABALY_CSOPORT[sz], sz))
    for e, sz in sorted(p['forditatlan'].items()):
        if (ig, e) in adat.kizaras:
            continue
        ki.append((('F', e), SZABALY_CSOPORT[sz], sz))
    return ki


def egyseg_halmaz(lk, b, f):
    return {('L', k, e) for k, e in lk} | {('B', k) for k in b} | {('F', e) for e in f}


def szamol(adat, szotar, forrasversek):
    """(sorok, reszletek) — a teljes mérés; determinisztikus (rendezett bejárás)."""
    metszet_ellenoriz(forrasversek, adat.arany)
    versek = [ig for ig in adat.versek if ig in adat.arany]
    par = {}
    for ig in versek:
        par[ig] = parosit(tokenek.tokenizal(adat.karoli[ig]), adat.ered[ig], szotar)
    sorok = meres.Sorok()
    hibak = []
    csoportok = ['szótár', 'K1', 'K8', 'K9']
    for ret in RETEGEK:
        vs = [ig for ig in versek if ret == meres.OSSZES or adat.reteg[ig] == ret]
        sz = Counter()
        for ig in vs:
            p = par[ig]
            g_lk, g_b, g_f = egysegek_arany(adat, ig)
            g_u = egyseg_halmaz(g_lk, g_b, g_f)
            sz['arany_link'] += len(g_lk)
            sz['arany_betoldas'] += len(g_b)
            sz['arany_forditatlan'] += len(g_f)
            sz['arany_egyseg'] += len(g_u)
            for u, cs, szab in szkript_egysegek(adat, ig, p):
                jo = u in g_u
                tip = u[0]
                sz['s_%s_%s' % (tip, cs)] += 1
                sz['s_%s_%s_jo' % (tip, cs)] += jo
                sz['s_%s' % tip] += 1
                sz['s_%s_jo' % tip] += jo
                sz['s_%s' % cs] += 1
                sz['s_%s_jo' % cs] += jo
                sz['s_egyseg'] += 1
                sz['s_egyseg_jo'] += jo
                if ret == meres.OSSZES and not jo:
                    hibak.append((ig, u, cs, szab))
            tl = tokenek.tokenizal(adat.karoli[ig])
            sz['magyar_token'] += len(tl)
            for k, ok in p['var_magyar'].items():
                sz['var_m'] += 1
                sz['var_m_%s' % ok] += 1
            ered_ossz = [w['sorsz'] for w in adat.ered[ig] if (ig, w['sorsz']) not in adat.kizaras]
            sz['eredeti_szo'] += len(ered_ossz)
            for e in ered_ossz:
                if e in p['var_eredeti']:
                    sz['var_e'] += 1
                    sz['var_e_%s' % p['var_eredeti'][e]] += 1
            # C-összevetés
            for f in C_FUTASOK:
                c = egysegek_c(adat, f, ig)
                if c is None:
                    continue
                c_u = egyseg_halmaz(*c)
                sz['c_%s_versek' % f] += 1
                for u, cs, szab in szkript_egysegek(adat, ig, p):
                    g_igen = u in g_u
                    c_igen = u in c_u
                    for csop in (cs, 'összes'):
                        kk = 'c_%s_%s' % (f, csop)
                        sz[kk + '_n'] += 1
                        sz[kk + '_szkript_jo'] += g_igen
                        sz[kk + '_c_jo'] += (c_igen == g_igen)
                        sz[kk + '_elter'] += (not c_igen)
                        sz[kk + '_elter_szkript_jo'] += (not c_igen) and g_igen
                        sz[kk + '_elter_c_jo'] += (not c_igen) and not g_igen
                        sz[kk + '_arany_igen'] += g_igen
                        sz[kk + '_arany_igen_c_igen'] += g_igen and c_igen
        S = 'szkript'
        sorok.add('alap', S, ret, 'arany_versek', len(vs), None, 'a mérésben részt vevő aranyversek (rétegben)')
        # lefedettség
        sorok.add('lefedettseg', S, ret, 'link_lefedettseg (összes szkript-link ∩ arany / arany link)',
                  sz['s_L_jo'], sz['arany_link'], 'az arany linkjeiből a szkript által helyesen eldöntött', intervallum=True)
        for cs in ('szótár', 'K9'):
            sorok.add('lefedettseg', S, ret, 'link_lefedettseg [%s]' % cs, sz['s_L_%s_jo' % cs], sz['arany_link'],
                      'csak a(z) %s szabály linkjei' % cs, intervallum=True)
        sorok.add('lefedettseg', S, ret, 'betoldas_lefedettseg [K1]', sz['s_B_jo'], sz['arany_betoldas'],
                  'az arany betoldas-szavaiból a szkript K1-betoldasa', intervallum=True)
        sorok.add('lefedettseg', S, ret, 'forditatlan_lefedettseg [K1+K8+K9]', sz['s_F_jo'], sz['arany_forditatlan'],
                  'az arany forditatlan-szavaiból a szkript forditatlan-döntése', intervallum=True)
        sorok.add('lefedettseg', S, ret, 'egyseg_lefedettseg (link + betoldas + forditatlan)', sz['s_egyseg_jo'],
                  sz['arany_egyseg'], 'az arany döntési egységeiből a szkript helyes döntése', intervallum=True)
        sorok.add('lefedettseg', S, ret, 'egyseg_dontott_arany (szkript-döntés / arany egység)', sz['s_egyseg'],
                  sz['arany_egyseg'], 'a szkript döntéseinek száma az arany egységszámához mérve (helyes és hibás együtt)')
        # pontosság
        sorok.add('pontossag', S, ret, 'link_pontossag [összes link]', sz['s_L_jo'], sz['s_L'],
                  'a szkript linkjeiből az aranyban', intervallum=True)
        for cs in ('szótár', 'K9'):
            sorok.add('pontossag', S, ret, 'link_pontossag [%s]' % cs, sz['s_L_%s_jo' % cs], sz['s_L_%s' % cs], '',
                      intervallum=True)
        sorok.add('pontossag', S, ret, 'betoldas_pontossag [K1]', sz['s_B_K1_jo'], sz['s_B_K1'],
                  'a szkript betoldas-döntéseiből az arany betoldas-listájában', intervallum=True)
        for cs in ('K1', 'K8', 'K9'):
            sorok.add('pontossag', S, ret, 'forditatlan_pontossag [%s]' % cs, sz['s_F_%s_jo' % cs], sz['s_F_%s' % cs],
                      'a szkript forditatlan-döntéseiből az arany forditatlan-listájában', intervallum=True)
        for cs in csoportok:
            sorok.add('pontossag', S, ret, 'egyseg_pontossag [%s]' % cs, sz['s_%s_jo' % cs], sz['s_%s' % cs],
                      'a csoport minden döntése (link, betoldas, forditatlan)', intervallum=True)
        sorok.add('pontossag', S, ret, 'egyseg_pontossag [K1+K8+K9]',
                  sz['s_K1_jo'] + sz['s_K8_jo'] + sz['s_K9_jo'], sz['s_K1'] + sz['s_K8'] + sz['s_K9'],
                  'a három K-szabály döntései együtt', intervallum=True)
        sorok.add('pontossag', S, ret, 'egyseg_pontossag [összes]', sz['s_egyseg_jo'], sz['s_egyseg'],
                  'a szkript minden döntése', intervallum=True)
        # modellre vár
        sorok.add('modellre_var', S, ret, 'magyar_token_modellre_var', sz['var_m'], sz['magyar_token'],
                  'a magyar tokenekből szkript-döntés nélkül')
        for ok in ('nincs_szotarban', 'tobb_magyar', 'nincs_jelolt', 'tobb_jelolt', 'K1_kivetel', 'K9_nem_gepies', 'egyeb'):
            sorok.add('modellre_var', S, ret, 'magyar_ok: %s' % ok, sz['var_m_%s' % ok], sz['magyar_token'], '')
        sorok.add('modellre_var', S, ret, 'eredeti_szo_modellre_var', sz['var_e'], sz['eredeti_szo'],
                  'az eredeti szavakból sem szkript-link, sem forditatlan (a kizárt tokenek nélkül)')
        for ok in ('nincs_szabaly', 'K1_kivetel_nevmasi', 'K1_kivetel_J', 'K9_nem_gepies', 'nem_tr'):
            sorok.add('modellre_var', S, ret, 'eredeti_ok: %s' % ok, sz['var_e_%s' % ok], sz['eredeti_szo'], '')
        # C-összevetés
        for f in C_FUTASOK:
            for csop in csoportok + ['összes']:
                kk = 'c_%s_%s' % (f, csop)
                if not sz[kk + '_n'] and csop != 'összes':
                    continue
                oss = '%s [%s]' % (f, csop)
                sorok.add('c_osszevetes', oss, ret, 'versek_C_ok', sz['c_%s_versek' % f], len(vs),
                          'aranyversek, ahol a C kapun átment (csak ezeken számol)')
                sorok.add('c_osszevetes', oss, ret, 'szkript_pontossag (ugyanezeken)', sz[kk + '_szkript_jo'], sz[kk + '_n'],
                          'szkript-egység az aranyban', intervallum=True)
                sorok.add('c_osszevetes', oss, ret, 'C_pontossag (ugyanazokon az egységeken)', sz[kk + '_c_jo'], sz[kk + '_n'],
                          'a C igen/nem válasza az egységre egyezik az arannyal', intervallum=True)
                sorok.add('c_osszevetes', oss, ret, 'C_fedi_a_helyes_szkript_dontest', sz[kk + '_arany_igen_c_igen'],
                          sz[kk + '_arany_igen'], 'az aranyban is meglévő szkript-egységekből a C-ben is megvan', intervallum=True)
                sorok.add('c_osszevetes', oss, ret, 'elteres (C nem mondja ugyanezt)', sz[kk + '_elter'], sz[kk + '_n'], '')
                sorok.add('c_osszevetes', oss, ret, 'elteresbol_szkript_egyezik_arannyal', sz[kk + '_elter_szkript_jo'],
                          sz[kk + '_elter'], 'eltérésnél pontosan az egyik egyezik az arannyal')
                sorok.add('c_osszevetes', oss, ret, 'elteresbol_C_egyezik_arannyal', sz[kk + '_elter_c_jo'], sz[kk + '_elter'], '')
    return sorok, {'par': par, 'hibak': hibak, 'versek': versek}


# ---------------------------------------------------------------------------
# hibák leírása
# ---------------------------------------------------------------------------

def _eredeti_leir(w):
    return '#%d %s %s [%s]' % (w['sorsz'], w['alak'], w['strong'], w['tukor'])


def hiba_leiras(adat, ig, u):
    """(magyar, szkript-döntés, arany szerint, hibatípus) szöveggel."""
    tl = tokenek.tokenizal(adat.karoli[ig])
    ew = adat.ered[ig]
    g_lk, g_b, g_f = egysegek_arany(adat, ig)
    if u[0] in ('L', 'B'):
        k = u[1]
        magyar = '%d %s' % (k, tl[k - 1])
        ar = [e for kk, e in sorted(g_lk) if kk == k]
        if k in g_b:
            arany = 'betoldas'
        else:
            arany = ', '.join(_eredeti_leir(ew[e - 1]) for e in ar) or '—'
        if u[0] == 'L':
            e = u[2]
            dontes = '→ ' + _eredeti_leir(ew[e - 1])
            if k in g_b:
                tip = 'a magyar szó az aranyban betoldas'
            elif ar:
                tip = 'az aranyban más eredeti szóhoz kötve'
            else:
                tip = 'egyéb'
            if e in g_f:
                tip += '; az eredeti szó az aranyban forditatlan'
            else:
                masik = sorted(kk for kk, ee in g_lk if ee == e)
                if masik:
                    tip += '; az eredeti szó az aranyban: ' + ', '.join('%d %s' % (kk, tl[kk - 1]) for kk in masik)
        else:
            dontes = 'betoldas'
            tip = 'a névelő az aranyban párosítva (névmási vagy más használat)'
        return magyar, dontes, arany, tip
    e = u[1]
    magyar = '—'
    dontes = 'forditatlan: ' + _eredeti_leir(ew[e - 1])
    ar = sorted(k for k, ee in g_lk if ee == e)
    arany = ', '.join('%d %s' % (k, tl[k - 1]) for k in ar) or '—'
    return magyar, dontes, arany, 'az eredeti szó az aranyban párosítva'


# ---------------------------------------------------------------------------
# kiírás
# ---------------------------------------------------------------------------

def fejlec(info, ts, szotar_stat):
    return ('# GENERÁLT: eszkozok/karoli_strong/elopar.py | scope=f21p, előpárosítás (kísérlet) az arany v3 '
            '60 versén (rétegek: f21p/minta.tsv), szótár %d forrásversből (F3V2 ∩ F3V2B), C-összevetés: %s | '
            'forras=f21p/szotar_elopar.tsv, f21p/arany_opus_v3.jsonl (sha256 %s), f21p/meres_kizaras.tsv, '
            'f21p/minta.tsv, f21p/valaszok/F3V2.jsonl, F3V2B.jsonl, F3V3.jsonl, konkordancia/Karoli_1908.tsv, '
            'TAHOT_kivonat.tsv, TAGNT_kivonat.tsv | ts=%s | nem minősítés; kézzel szerkeszteni tilos'
            % (szotar_stat['forrasversek'], ', '.join(C_FUTASOK), info['sha256'], ts))


def tsv_ir(sorok, info, ts, szotar_stat, ut=EREDMENY_UT):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec(info, ts, szotar_stat) + '\n')
        f.write('\t'.join(meres.OSZLOPOK) + '\n')
        for r in sorok.lista:
            f.write('\t'.join(meres._fmt(r[k]).replace('\t', ' ') for k in meres.OSZLOPOK) + '\n')


def _tabla(sorok, szakasz, oss_szuro=None):
    rs = [r for r in sorok.lista if r['szakasz'] == szakasz and (oss_szuro is None or oss_szuro(r['osszeallitas']))]
    kulcsok = []
    for r in rs:
        k = (r['osszeallitas'], r['mero'])
        if k not in kulcsok:
            kulcsok.append(k)
    ki = ['| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |', '|---|---|---|---|---|---|---|']
    for k in kulcsok:
        cellak = []
        for ret in RETEGEK:
            x = [r for r in rs if (r['osszeallitas'], r['mero']) == k and r['reteg'] == ret]
            cellak.append(meres._cella(x[0]) if x else '—')
        ki.append('| %s | %s | %s |' % (k[0], k[1], ' | '.join(cellak)))
    return ki + ['']


def md_ir(sorok, info, ts, szotar, szotar_stat, adat, reszlet, ut=JELENTES_UT):
    ki = ['# F21P_elopar.md — szkriptes előpárosítás (kísérlet), mérés az arany v3-on', '',
          '<!-- %s -->' % fejlec(info, ts, szotar_stat).lstrip('# '), '',
          '**Ez kísérlet, nem minősítés:** a számok a szkript kimenetei (f21p/elopar_eredmeny.tsv), '
          'döntési szabályhoz (küszöbhöz) nem viszonyítanak. Cellaforma: érték% (számláló/nevező) '
          '[90%-os Wilson-intervallum, linkszintű, a versen belüli összefüggést nem kezeli, tehát '
          'optimista]. Az arany 60 vers (R1 20, R2 10, R3 10, R4 20): a rétegenkénti nevező kicsi, '
          'a K8-nál és a K9-linknél nagyon kicsi (n < 30 esetén az intervallum széles; nézd a nevezőt).', '',
          '## Algoritmus (összefoglalás; a teljes leírás az elopar.py docstringjében)', '',
          '- **Szótár:** F3V2 ∩ F3V2B egyező linkjei (ugyanaz a (magyar, eredeti) sorszámpár mindkét '
          'futásban, ugyanabban a versben), csak a mindkét futásban kapun átment versekből, az arany 60 '
          'verse nélkül. Kulcs: a Károli-token kisbetűsítve (ékezettel, egyéb normalizálás nélkül); érték: '
          'a TAHOT/TAGNT Strong-mező. Kizárva: a H9xxx / G3588 / G2532 összetevőjű Strong és az a/az/és/s '
          'szóalak (K-szabályok hatásköre). Felvétel: db >= 3 és a szóalaknak nincs versengő Strongja.',
          '- **Szótári döntés:** versenként Strongonként csak 1 magyar igénylő : 1 (TR-es) eredeti jelölt '
          'esetén; az ismételt szóalak vagy az azonos Strongra mutató két szóalak „modellre vár” (tobb_magyar).',
          '- **K1:** a/az → betoldas, ha a következő szó nem vonatkozó névmás/kötőszó, nem névutó, nem a/az/is, '
          'és az alak illik (a + mássalhangzó, az + magánhangzó); H9009/G3588 → forditatlan, ha a tükörfordítás '
          'puszta névelő (the, of the, <the>, [is] the ...) és a versben nincs e/ez/ezen/eme/emez/ama (J szabály). '
          'Minden más névelő-eset: modellre vár.',
          '- **K8:** H9012, H9013 → forditatlan.',
          '- **K9:** ve- (H9001, H9002) / καί (G2532): ha a magyar versben nincs és/s/pedig/is/de/hogy és nincs '
          'mind/se/sem/sőt → forditatlan; ha pontosan egy ve-/καί és pontosan egy kötőszó-szó van, és az az és/s '
          '(bővítő szó és τε nélkül) → link; minden más eset modellre vár.',
          '- A [nem TR] eredeti szót egyik szabály sem dönti el. Nem használ KJV-t és modellválaszt.', '',
          '## Szótár', '',
          '| mérőszám | érték |', '|---|---|']
    for k, v in szotar_stat.items():
        ki.append('| %s | %s |' % (k, v))
    m = len(set(reszlet['forrasversek']) & set(adat.arany))
    ki += ['', 'Gépi ellenőrzés: a szótár forrásversei (%d) és az arany versei (%d) metszete: **%d**.'
           % (len(reszlet['forrasversek']), len(adat.arany), m), '']
    leggy = sorted(szotar.items(), key=lambda x: (-x[1][1], x[0]))[:15]
    ki += ['A 15 leggyakoribb szótárbejegyzés: ' + ', '.join('*%s* → %s (%d)' % (s, v[0], v[1]) for s, v in leggy), '']
    cimek = [('lefedettseg', 'Lefedettség (az arany egységeiből a szkript által helyesen eldöntött)'),
             ('pontossag', 'Pontosság a szkript saját döntésein'),
             ('modellre_var', '„Modellre vár” aránya és okai'),
             ('alap', 'Alapadat')]
    for sz, cim in cimek:
        ki += ['## ' + cim, ''] + _tabla(sorok, sz)
    ki += ['## C-összevetés ugyanazokon az egységeken (tájékoztató)', '',
           'Egységenkénti igen/nem kérdés: a szkript minden döntése „igen” az adott egységre (link, betoldas, '
           'forditatlan). A C ugyanerre igent mond, ha az egység benne van a C kimenetében. A C-pontosság: a C '
           'igen/nem válasza egyezik az arannyal. Eltérésnél pontosan az egyik egyezik. Csak a C-ben kapun '
           'átment aranyversek.', '']
    for f in C_FUTASOK:
        ki += ['### %s' % f, ''] + _tabla(sorok, 'c_osszevetes', lambda o, f=f: o.startswith(f + ' '))
    # hibák
    hibak = reszlet['hibak']
    ki += ['## Hibás szkript-döntések', '',
           'Összesen %d hibás szkript-egység (a kizárások után): ' % len(hibak) +
           ', '.join('%s: %d' % (k, v) for k, v in sorted(Counter(h[2] for h in hibak).items())) + '.', '']
    tipusok = Counter()
    for ig, u, cs, szab in hibak:
        tipusok[(cs, hiba_leiras(adat, ig, u)[3].split(';')[0])] += 1
    ki += ['| csoport | hibatípus (az arany szerint) | db |', '|---|---|---|']
    for (cs, t), db in sorted(tipusok.items(), key=lambda x: (-x[1], x[0])):
        ki.append('| %s | %s | %d |' % (cs, t, db))
    ki += ['', '### Hibás szótári döntések szótárbejegyzésenként', '',
           '| szóalak | Strong | db (szótár) | vers_db | hibás döntés | helyes döntés |', '|---|---|---|---|---|---|']
    jo_kulcs, rossz_kulcs = Counter(), Counter()
    for ig in reszlet['versek']:
        tl = tokenek.tokenizal(adat.karoli[ig])
        g_lk = adat.arany_linkek(ig)
        for (k, e), szab in reszlet['par'][ig]['linkek'].items():
            if szab != 'szotar' or (ig, e) in adat.kizaras:
                continue
            (jo_kulcs if (k, e) in g_lk else rossz_kulcs)[tl[k - 1].lower()] += 1
    for s, db in sorted(rossz_kulcs.items(), key=lambda x: (-x[1], x[0])):
        v = szotar[s]
        ki.append('| %s | %s | %d | %d | %d | %d |' % (s, v[0], v[1], v[2], db, jo_kulcs[s]))
    if not rossz_kulcs:
        ki.append('| (nincs hibás szótári döntés) | | | | 0 | %d |' % sum(jo_kulcs.values()))
    ki += ['', 'A helyes szótári döntések bejegyzésenként: ' +
           (', '.join('*%s* (%d)' % (s, d) for s, d in sorted(jo_kulcs.items())) or '—') + '.']
    ki += ['', '### Példák (az első 15 hibás döntés versrendben; legfeljebb 10 szótári, a többi K-szabály)', '',
           '| vers | csoport | magyar szó | szkript-döntés | az arany szerint | típus |', '|---|---|---|---|---|---|']
    szot = [h for h in hibak if h[2] == 'szótár'][:10]
    kh = [h for h in hibak if h[2] != 'szótár'][:15 - len(szot)]
    for ig, u, cs, szab in sorted(szot + kh, key=lambda h: (reszlet['versek'].index(h[0]), str(h[1]))):
        mg, d, a, t = hiba_leiras(adat, ig, u)
        ki.append('| %s | %s | %s | %s | %s | %s |' % (ig, cs, mg, d.replace('|', '/'), a.replace('|', '/'), t))
    ki += ['', '## Nyitott kérdések (a kísérlet korlátai, nem döntés)', '',
           '- A szótár szóalak-szintű és nyers (csak kisbetű): a toldalékos alakok külön kulcsok, ezért a '
           'lefedettség a gyakori, kötött alakokra korlátozódik; tövesítés nem készült.',
           '- A szótár forrása két modellfutás egyezése, nem arany: a C következetes tévedései bekerülhetnek.',
           '- A K1 névelő-vizsgálata (a/az + következő szó) és a tükörfordítás-alapú névmási szűrés gépies '
           'közelítés; a K9 csak az „egy ve-/καί : egy és/s” és a „nincs kötőszó” esetet dönti el.',
           '- A mérés 60 versen fut; a C-összevetés csak a szkript által eldöntött egységeken értelmezett, nem a '
           'C teljes pontossága.',
           '- A szótár `db` mezője link-szintű (egy magyar token több azonos Strongú eredetihez kötve többször '
           'számít); a `szotar_bejegyzes_3_alatti_token_elofordulassal` sor mutatja, hány bejegyzés esne ki, ha '
           'a feltétel token-előfordulásra szólna.',
           '- A fenti hibapéldák a szabályok lehetséges finomítására utalnak (pl. a K9 kötőszó-listája, a '
           'névelő + δέ, a magyar „a ki” és a görög névelő összekapcsolása). Ezek az arany ismeretében '
           'fogalmazódnának meg, tehát az ugyanezen a 60 versen mért javulás nem volna független mérés; a '
           'szkript ezért nem tartalmazza őket.', '']
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def fut(szotar_mod=True, meres_mod=True, szotar_ut=SZOTAR_UT, eredmeny_ut=EREDMENY_UT, jelentes_ut=JELENTES_UT, ts=None):
    adat, info = betolt()
    ts = ts or tokenek.generalas_ts()
    szotar, stat, forras = szotar_adatbol(adat)
    if szotar_mod:
        szotar_ir(szotar, stat, szotar_ut, ts)
        print('szótár: %d szóalak, %d forrásvers -> %s' % (len(szotar), stat['forrasversek'], szotar_ut))
    if meres_mod:
        f_szotar, f_stat = szotar_olvas(szotar_ut)
        if f_szotar != szotar:
            raise SystemExit('HIBA: a %s nem egyezik az újraépített szótárral (futtasd: --szotar)' % szotar_ut)
        sorok, reszlet = szamol(adat, f_szotar, forras)
        reszlet['forrasversek'] = forras
        tsv_ir(sorok, info, ts, f_stat, eredmeny_ut)
        md_ir(sorok, info, ts, f_szotar, f_stat, adat, reszlet, jelentes_ut)
        print('mérés: %d sor -> %s, %s' % (len(sorok.lista), eredmeny_ut, jelentes_ut))
    return 0


# ---------------------------------------------------------------------------
# önteszt (mock-adat, nem ír a repóba)
# ---------------------------------------------------------------------------

def _w(sorsz, strong, tukor='x', nem_tr=False):
    return {'sorsz': sorsz, 'strong': strong, 'alak': 'α%d' % sorsz, 'tukor': tukor, 'nem_tr': nem_tr}


def onteszt():
    hibak = []

    def ell(felt, uzenet):
        if not felt:
            hibak.append(uzenet)

    # --- szótárépítés ---
    karoli = {'V1': 'Isten szól ház ház', 'V2': 'Isten szól ház', 'V3': 'isten szól ház', 'V4': 'Isten szól',
              'ARANY': 'Isten Isten Isten szól', 'HIBAS': 'Isten szól'}
    ered = {'V1': [_w(1, 'H0430'), _w(2, 'H0559'), _w(3, 'H1004'), _w(4, 'H9009')],
            'V2': [_w(1, 'H0430'), _w(2, 'H0559'), _w(3, 'H1005')],
            'V3': [_w(1, 'H0430'), _w(2, 'H1696'), _w(3, 'H1004')],
            'V4': [_w(1, 'H0430'), _w(2, 'H0559')],
            'ARANY': [_w(1, 'H0430'), _w(2, 'H0430'), _w(3, 'H0430'), _w(4, 'H7777')],
            'HIBAS': [_w(1, 'H0430'), _w(2, 'H0559')]}

    def rek(parok, ok=True):
        return {'allapot': 'ok' if ok else 'kapuhiba', 'obj': {'parok': parok, 'betoldas': [], 'forditatlan': []}}
    fa = {'V1': rek([[1, [1]], [2, [2]], [3, [3]], [4, [4]]]), 'V2': rek([[1, [1]], [2, [2]], [3, [3]]]),
          'V3': rek([[1, [1]], [2, [2]], [3, [3]]]), 'V4': rek([[1, [1]], [2, [2]]]),
          'ARANY': rek([[1, [1]], [2, [2]], [3, [3]], [4, [4]]]), 'HIBAS': rek([[1, [1]], [2, [2]]], ok=False)}
    fb = {'V1': rek([[1, [1]], [2, [2]], [3, [3]], [4, [4]]]), 'V2': rek([[1, [1]], [2, [2]], [3, [3]]]),
          'V3': rek([[1, [1]], [2, [1]], [3, [3]]]), 'V4': rek([[1, [1]], [2, [2]]]),
          'ARANY': rek([[1, [1]], [2, [2]], [3, [3]], [4, [4]]]), 'HIBAS': rek([[1, [1]], [2, [2]]])}
    sz, st, forras = szotar_epit(fa, fb, karoli, ered, {'ARANY'})
    ell(forras == ['V1', 'V2', 'V3', 'V4'], 'forrásversek: az arany és a kapuhibás vers kizárva (%s)' % forras)
    ell(sz.get('isten') == ('H0430', 4, 4), 'isten → H0430, db 4 (kisbetűsítés; az arany 3 előfordulása nem számít): %s' % (sz.get('isten'),))
    ell('ház' not in sz and st['kiesett_versenges'] == 1, 'ház: versengő Strong (H1004/H1005) → kimarad')
    # szól: V1, V2, V4 egyező (3) → H0559 db 3; a V3-ban a két futás eltér (nem egyező link)
    ell(sz.get('szól') == ('H0559', 3, 3), 'szól → H0559 db 3 (a V3 eltérő linkje nem számít): %s' % (sz.get('szól'),))
    ell(st['kizart_link_strong_miatt'] == 1, 'a H9009-es egyező link kizárva: %s' % st)
    sz2, st2, _ = szotar_epit(fa, fb, karoli, ered, {'ARANY'}, min_db=4)
    ell('szól' not in sz2 and st2['kiesett_keves'] >= 1, 'min_db=4: a szól kevés előfordulás miatt kiesik')
    ell(all(not v[0].startswith('H9') for v in sz.values()), 'H9xxx nincs a szótárban')
    ell(szotar_kizart_strong('G2532+G1473') and szotar_kizart_strong('G3588') and not szotar_kizart_strong('G2316'),
        'összetett Strong kizárása')
    sz3, _, _ = szotar_epit(fa, fb, karoli, ered, set())
    ell(sz3.get('isten', (None, 0))[1] == 7, 'ha az arany nincs kizárva, beszámítana (a kizárás hatásos)')

    # --- metszet-ellenőrzés ---
    try:
        metszet_ellenoriz(['V1', 'ARANY'], {'ARANY': 1})
        ell(False, 'metszet-ellenőrzés: átfedésnél SystemExit kell')
    except SystemExit:
        pass
    ell(metszet_ellenoriz(['V1'], {'ARANY': 1}) == 0, 'metszet-ellenőrzés: diszjunkt halmaz rendben')

    # --- párosító ---
    szt = {'isten': ('H0430', 9, 9), 'mondá': ('H0559', 9, 9), 'házat': ('H1004', 9, 9), 'házba': ('H1004', 9, 9),
           'fiú': ('H1121', 9, 9)}
    p = parosit(['Isten', 'mondá'], [_w(1, 'H0559'), _w(2, 'H0430')], szt)
    ell(p['linkek'] == {(1, 2): 'szotar', (2, 1): 'szotar'}, 'egy jelölt → link: %s' % p['linkek'])
    p = parosit(['Isten', 'Isten'], [_w(1, 'H0430')], szt)
    ell(not p['linkek'] and p['var_magyar'] == {1: 'tobb_magyar', 2: 'tobb_magyar'}, 'ismételt szóalak → tobb_magyar')
    p = parosit(['házat', 'házba'], [_w(1, 'H1004')], szt)
    ell(not p['linkek'] and p['var_magyar'][1] == 'tobb_magyar', 'két szóalak ugyanarra a Strongra → tobb_magyar')
    p = parosit(['Isten'], [_w(1, 'H0430'), _w(2, 'H0430')], szt)
    ell(p['var_magyar'] == {1: 'tobb_jelolt'}, 'két jelölt → tobb_jelolt')
    p = parosit(['fiú'], [_w(1, 'H0430')], szt)
    ell(p['var_magyar'] == {1: 'nincs_jelolt'}, 'nincs jelölt')
    p = parosit(['fiú'], [_w(1, 'H1121', nem_tr=True)], szt)
    ell(p['var_magyar'] == {1: 'nincs_jelolt'} and p['var_eredeti'] == {1: 'nem_tr'}, 'nem_tr eredeti nem jelölt')
    p = parosit(['kenyér'], [_w(1, 'H3899')], szt)
    ell(p['var_magyar'] == {1: 'nincs_szotarban'} and p['var_eredeti'] == {1: 'nincs_szabaly'}, 'szótáron kívül → modellre vár')
    # K1
    p = parosit(['a', 'király', 'az', 'Úr', 'a', 'ki', 'az', 'előtt', 'az'], [_w(1, 'H9009', 'the')], {})
    ell(p['betoldas'] == {1: 'K1', 3: 'K1'}, 'K1 betoldas: a + mássalhangzó, az + magánhangzó: %s' % p['betoldas'])
    ell(p['var_magyar'][5] == 'K1_kivetel' and p['var_magyar'][7] == 'K1_kivetel' and p['var_magyar'][9] == 'K1_kivetel',
        'K1 kivétel: a ki, az előtt, verszáró az')
    ell(p['forditatlan'] == {1: 'K1'}, 'H9009 [the] → forditatlan')
    p = parosit(['az', 'király'], [_w(1, 'G3588', 'the')], {})
    ell(p['var_magyar'] == {1: 'K1_kivetel', 2: 'nincs_szotarban'}, 'az + mássalhangzó → modellre vár')
    p = parosit(['a', 'ki'], [_w(1, 'G3588', 'who'), _w(2, 'G3588', 'the [one]'), _w(3, 'G3588', 'of the'),
                              _w(4, 'H9009', '[is] <the>')], {})
    ell(p['var_eredeti'].get(1) == 'K1_kivetel_nevmasi' and p['var_eredeti'].get(2) == 'K1_kivetel_nevmasi'
        and p['forditatlan'] == {3: 'K1', 4: 'K1'}, 'névelő tükör: who / the [one] vár, of the / [is] <the> forditatlan: %s' % p)
    p = parosit(['e', 'földön'], [_w(1, 'G3588', 'the')], {})
    ell(p['var_eredeti'] == {1: 'K1_kivetel_J'}, 'J szabály: e/ez a versben → a névelő vár')
    # K8
    p = parosit(['menj'], [_w(1, 'H1980'), _w(2, 'H9012', '!'), _w(3, 'H9013', '!')], {})
    ell(p['forditatlan'] == {2: 'K8', 3: 'K8'}, 'K8')
    # K9
    p = parosit(['mondá', 'Isten'], [_w(1, 'H9002', 'and'), _w(2, 'H0559'), _w(3, 'H0430')], szt)
    ell(p['forditatlan'] == {1: 'K9_nincs_kotoszo'}, 'K9: nincs kötőszó → forditatlan')
    p = parosit(['Isten', 'és', 'ember'], [_w(1, 'H0430'), _w(2, 'H9001', 'and'), _w(3, 'H0120')], szt)
    ell(p['linkek'].get((2, 2)) == 'K9_egy_es', 'K9: egy ve- : egy és → link')
    p = parosit(['Isten', 'és', 'ember', 'is'], [_w(1, 'H0430'), _w(2, 'H9001'), _w(3, 'H0120')], szt)
    ell(p['var_eredeti'].get(2) == 'K9_nem_gepies' and p['var_magyar'].get(2) == 'K9_nem_gepies',
        'K9: és + is → nem gépies')
    p = parosit(['Isten', 'és', 'ember'], [_w(1, 'H9002'), _w(2, 'H0430'), _w(3, 'H9002'), _w(4, 'H0120')], szt)
    ell(p['var_eredeti'].get(1) == 'K9_nem_gepies' and p['var_eredeti'].get(3) == 'K9_nem_gepies', 'K9: két ve- egy és → vár')
    p = parosit(['sem', 'Isten'], [_w(1, 'G2532'), _w(2, 'G2316')], {})
    ell(p['var_eredeti'].get(1) == 'K9_nem_gepies', 'K9: bővítő szó (sem) → nem forditatlan')
    p = parosit(['és', 'Isten'], [_w(1, 'G2532'), _w(2, 'G5037')], {})
    ell(p['var_eredeti'].get(1) == 'K9_nem_gepies', 'K9: τε a versben → vár')
    # determinizmus
    ell(parosit(['a', 'Isten', 'és', 'ember'], [_w(1, 'H0430'), _w(2, 'H9002')], szt) ==
        parosit(['a', 'Isten', 'és', 'ember'], [_w(1, 'H0430'), _w(2, 'H9002')], szt), 'determinizmus (párosító)')

    # --- teljes futás kétszer, ideiglenes könyvtárba (determinizmus, a repó nem változik) ---
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        uts = [[os.path.join(d, '%s%d' % (n, i)) for n in ('sz', 'er', 'je')] for i in (1, 2)]
        for u in uts:
            fut(True, True, u[0], u[1], u[2], ts='T')
        for a, b in zip(*uts):
            with open(a, 'rb') as x, open(b, 'rb') as y:
                ell(x.read() == y.read(), 'determinizmus: %s' % os.path.basename(a))
        szv, stv = szotar_olvas(uts[0][0])
        ell(szv and stv['forrasversek'] > 0, 'a szótár visszaolvasható')

    if hibak:
        print('ÖNTESZT: HIBA (%d)' % len(hibak))
        for h in hibak:
            print('  - ' + h)
        return 1
    print('ÖNTESZT: rendben')
    return 0


def main():
    if '--onteszt' in sys.argv:
        return onteszt()
    if '--szotar' in sys.argv:
        return fut(True, False)
    if '--meres' in sys.argv:
        return fut(False, True)
    return fut(True, True)


if __name__ == '__main__':
    sys.exit(main())
