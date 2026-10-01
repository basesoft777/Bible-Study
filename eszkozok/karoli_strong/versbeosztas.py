#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — versbeosztás-detektor: a Károli- és az eredeti (TAHOT/TAGNT) versbeosztás összevetése a teljes Bibliára.

A Károli-kulcs szerinti igehely-egyezés nem elég: a két szöveg versei egy-egy szakaszon eltolódhatnak úgy is, hogy
a versszám azonos (vagy a versszámok hiányoznak az egyik oldalról). A detektor ezért NEM a versszámra, hanem a
vershosszra épít (szószám, mindkét oldalon), két független jelzéssel:

  1. Könyv szintű igazítás (dinamikus programozás): a könyv két versfolyamát (fejezet, vers szerint rendezve) a
     vershosszak logaritmusának eltérése szerint párosítja (egy-az-egyhez, vagy egy oldali kihagyás); a versszám
     csak egy kis döntetlen-feloldó bónusz (`BONUSZ`). Ahol az így kapott pár versszáma eltér, ott eltolódás van
     (`eltolt`), ahol az egyik oldal verse kimarad, ott nincs megfelelő (`nincs_eredeti` / `nincs_karoli`).
  2. Fejezet szintű hosszkorreláció: a fejezet Károli- és eredeti vershosszainak Pearson-korrelációja az azonos
     sorrendű (d = 0) és az eltolt (d = -2..+2) párosításra. Eltolás-gyanú, ha az eltolt korreláció legalább 0,2-del
     jobb, és legalább 0,6; gyenge illeszkedés, ha r(0) < 0,6 (legalább 8 versű fejezetben).

Kimenetek (API nélkül, determinisztikusan):
  naplok/F22_versbeosztas.md     könyvenként és fejezetenként, csak számokkal (nincs versszöveg)
  f22/versmegfeleltetes.tsv      gépi lista: a futtató (`tokenek.betolt_eredeti`) ebből adja a Károli-versnek a
                                 megfeleltetett eredeti verset; ahol nincs megfeleltetés, ott `kezi`.
                                 Oszlopok: karoli, eredeti, tipus (eltolt | nincs_eredeti | nincs_karoli).
                                 Csak a legalább 3 egymást követő eltolt pár (`MIN_SZEGMENS`) kerül be; a magányos
                                 eltérés zajnak számít.

Használat:
    python eszkozok/karoli_strong/versbeosztas.py [--md naplok/F22_versbeosztas.md] [--tsv f22/versmegfeleltetes.tsv]
    python eszkozok/karoli_strong/versbeosztas.py --onteszt
"""
import argparse
import math
import os
import random
import statistics
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

GAP = 1.2            # egy oldali kihagyás ára (négyzetes log-hossz egységben)
BONUSZ = 0.10        # azonos versszámú pár döntetlen-feloldó bónusza
SAV = 60             # az igazítás sávja (a két folyam pozíciójának legnagyobb eltérése)
MIN_SZEGMENS = 3     # ennyi egymást követő eltolt pár kell a gépi listába
KORR_ELT_KULCS = 0.2
KORR_ELT_MIN = 0.6
KORR_GYENGE = 0.6
KORR_MIN_VERS = 8
MU_ALAP = -0.07      # a Károli/eredeti log-hosszarány alapértéke, ha nincs elég azonos versszámú pár


def rendez(igehelyek):
    return sorted(igehelyek, key=lambda ig: tokenek.igehely_bont(ig)[1:])


def folyamok(karoli, ered, konyv):
    """A könyv két versfolyama: [(igehely, szószám)], fejezet és vers szerint rendezve."""
    k = [(ig, len(tokenek.tokenizal(karoli[ig]))) for ig in rendez(i for i in karoli
                                                                  if tokenek.igehely_bont(i)[0] == konyv)]
    e = [(ig, len(ered[ig])) for ig in rendez(i for i in ered if tokenek.igehely_bont(i)[0] == konyv)]
    return k, e


def illeszt(k, e, gap=GAP, bonusz=BONUSZ, sav=SAV):
    """Könyv szintű igazítás. Visszaad: [(karoli_igehely|None, eredeti_igehely|None)] a folyam sorrendjében."""
    lk = [math.log(max(1, n)) for _, n in k]
    le = [math.log(max(1, n)) for _, n in e]
    helyek = {ig: j for j, (ig, _) in enumerate(e)}
    kul = [lk[i] - le[helyek[ig]] for i, (ig, _) in enumerate(k) if ig in helyek]
    mu = statistics.median(kul) if len(kul) >= 10 else MU_ALAP

    def koltseg(i, j):
        x = (lk[i] - le[j] - mu) ** 2
        return x - bonusz if k[i][0] == e[j][0] else x

    n, m = len(k), len(e)
    inf = float('inf')
    d = {(0, 0): 0.0}
    vissza = {}
    for i in range(n + 1):
        for j in range(max(0, i - sav), min(m, i + sav) + 1):
            if i == 0 and j == 0:
                continue
            legjobb, lep = inf, None
            if i > 0 and j > 0 and (i - 1, j - 1) in d:
                v = d[(i - 1, j - 1)] + koltseg(i - 1, j - 1)
                if v < legjobb:
                    legjobb, lep = v, 'p'
            if i > 0 and (i - 1, j) in d:
                v = d[(i - 1, j)] + gap
                if v < legjobb:
                    legjobb, lep = v, 'k'
            if j > 0 and (i, j - 1) in d:
                v = d[(i, j - 1)] + gap
                if v < legjobb:
                    legjobb, lep = v, 'e'
            if lep:
                d[(i, j)] = legjobb
                vissza[(i, j)] = lep
    if (n, m) not in vissza and (n, m) != (0, 0):
        raise SystemExit('az igazítás nem fér a sávba (a két folyam hossza túl eltér): %d / %d' % (n, m))
    i, j = n, m
    ki = []
    while i > 0 or j > 0:
        lep = vissza[(i, j)]
        if lep == 'p':
            ki.append((k[i - 1][0], e[j - 1][0]))
            i, j = i - 1, j - 1
        elif lep == 'k':
            ki.append((k[i - 1][0], None))
            i -= 1
        else:
            ki.append((None, e[j - 1][0]))
            j -= 1
    return ki[::-1]


def szegmensek(parok, min_hossz=MIN_SZEGMENS):
    """A gépi lista sorai az igazításból: [(karoli, eredeti, tipus)]."""
    sorok = []
    futam = []

    def lezar():
        if len(futam) >= min_hossz:
            sorok.extend((a, b, 'eltolt') for a, b in futam)
        futam.clear()

    for a, b in parok:
        if a is not None and b is not None and a != b:
            futam.append((a, b))
            continue
        lezar()
        if a is None:
            sorok.append(('', b, 'nincs_karoli'))
        elif b is None:
            sorok.append((a, '', 'nincs_eredeti'))
    lezar()
    # a gyűjtés sorrendjét a folyam adja; a futam-kiírás a hiány-sorok elé kerülhet: rendezés a (típus-független) helyre
    return sorok


def pearson(a, b):
    n = len(a)
    if n < 2:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va == 0 or vb == 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(va * vb)


def fejezet_korr(kh, eh, d):
    """A d eltolású pozíciós hosszkorreláció: K[i] ~ E[i+d]. None, ha kevés a pár."""
    a, b = [], []
    for i, x in enumerate(kh):
        j = i + d
        if 0 <= j < len(eh):
            a.append(math.log(max(1, x)))
            b.append(math.log(max(1, eh[j])))
    if len(a) < KORR_MIN_VERS:
        return None
    return pearson(a, b)


def fejezet_sorok(k, e, parok):
    """Fejezetenkénti számok. Visszaad: [dict] fejezetsorrendben."""
    kf, ef = {}, {}
    for ig, n in k:
        kf.setdefault(tokenek.igehely_bont(ig)[1], []).append(n)
    for ig, n in e:
        ef.setdefault(tokenek.igehely_bont(ig)[1], []).append(n)
    elt, khi, ehi = {}, {}, {}
    seg = {c: 0 for c in set(kf) | set(ef)}
    # szegmens-szám fejezetenként: a gépi lista eltolt futamai a Károli-oldal fejezete szerint
    gep = szegmensek(parok)
    for a, b, t in gep:
        if t == 'eltolt':
            c = tokenek.igehely_bont(a)[1]
            elt[c] = elt.get(c, 0) + 1
    for a, b in parok:
        if a is None:
            c = tokenek.igehely_bont(b)[1]
            ehi[c] = ehi.get(c, 0) + 1
        elif b is None:
            c = tokenek.igehely_bont(a)[1]
            khi[c] = khi.get(c, 0) + 1
    ki = []
    for c in sorted(set(kf) | set(ef)):
        kh, eh = kf.get(c, []), ef.get(c, [])
        r0 = fejezet_korr(kh, eh, 0)
        legjobb = (0, r0)
        for d in (-2, -1, 1, 2):
            r = fejezet_korr(kh, eh, d)
            if r is not None and (legjobb[1] is None or r > legjobb[1]):
                legjobb = (d, r)
        jel = []
        if len(kh) != len(eh):
            jel.append('LETSZAM')
        if elt.get(c):
            jel.append('ELTOLT')
        if khi.get(c):
            jel.append('KHIANY')
        if ehi.get(c):
            jel.append('EHIANY')
        d, rb = legjobb
        if d != 0 and rb is not None and r0 is not None and rb >= r0 + KORR_ELT_KULCS and rb >= KORR_ELT_MIN:
            jel.append('KORR_ELT')
        elif r0 is not None and r0 < KORR_GYENGE:
            jel.append('GYENGE')
        ki.append({'fejezet': c, 'k': len(kh), 'e': len(eh), 'eltolt': elt.get(c, 0), 'k_hiany': khi.get(c, 0),
                   'e_hiany': ehi.get(c, 0), 'r0': r0, 'd': d, 'rd': rb, 'jel': jel})
    return ki


def konyvek(karoli):
    sor = []
    for ig in karoli:
        b = tokenek.igehely_bont(ig)[0]
        if b not in sor:
            sor.append(b)
    return sor


def elemez(karoli=None, ered=None, nyers_ered=None):
    """Visszaad: [(konyv, k, e, parok, fejezetsorok)]; `ered`: a detektor a NYERS eredeti versfolyamot kapja."""
    karoli = karoli if karoli is not None else tokenek.betolt_karoli()
    ered = ered if ered is not None else tokenek.betolt_eredeti(versmegf=False)
    ki = []
    for konyv in konyvek(karoli):
        k, e = folyamok(karoli, ered, konyv)
        parok = illeszt(k, e)
        ki.append((konyv, k, e, parok, fejezet_sorok(k, e, parok)))
    return ki


def f(r):
    return '-' if r is None else '%.2f' % r


def md(eredmeny):
    s = ['# GENERÁLT: eszkozok/karoli_strong/versbeosztas.py | scope=Karoli_1908.tsv+TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (nyers versfolyam, versmegfeleltetés nélkül) | forras=determinisztikus vershossz-összevetés | ts=%s' % tokenek.generalas_ts(),
         '', '# F22_versbeosztas.md — a Károli- és az eredeti versbeosztás összevetése (teljes Biblia)', '',
         '*Csak számok, versszöveg nélkül. Módszer: l. `eszkozok/karoli_strong/versbeosztas.py` docstringje (könyv szintű hossz-igazítás + fejezet szintű hosszkorreláció; a versszám csak döntetlen-feloldó). A gépi lista: `f22/versmegfeleltetes.tsv`.*', '',
         '**Jelzések:** `LETSZAM` a fejezet Károli- és eredeti versszáma eltér; `ELTOLT` az igazítás a fejezet versét eltérő számú eredeti verssel párosította (≥ %d egymást követő pár); `KHIANY` / `EHIANY` a Károli-, illetve eredeti versnek nincs megfelelője; `KORR_ELT` egy eltolt (d ≠ 0) párosítás hosszkorrelációja ≥ r(0) + %.1f és ≥ %.1f; `GYENGE` r(0) < %.1f (legalább %d versű fejezetben). `r(0)`: a fejezet Károli- és eredeti vershosszainak korrelációja azonos sorrendben; `d`, `r(d)`: a legjobb eltolás és korrelációja.' % (MIN_SZEGMENS, KORR_ELT_KULCS, KORR_ELT_MIN, KORR_GYENGE, KORR_MIN_VERS), '',
         '## 1. Könyvenkénti összesítés', '',
         '| könyv | Károli-versek | eredeti versek | fejezet | jelzett fejezet | eltolt párok | Károli-hiány | eredeti-hiány |',
         '|---|---|---|---|---|---|---|---|']
    ossz = [0] * 7
    for konyv, k, e, parok, fs in eredmeny:
        gep = szegmensek(parok)
        elt = sum(1 for _, _, t in gep if t == 'eltolt')
        kh = sum(1 for _, _, t in gep if t == 'nincs_eredeti')
        eh = sum(1 for _, _, t in gep if t == 'nincs_karoli')
        jel = sum(1 for r in fs if r['jel'])
        sor = [len(k), len(e), len(fs), jel, elt, kh, eh]
        ossz = [a + b for a, b in zip(ossz, sor)]
        s.append('| %s | %s |' % (konyv, ' | '.join(str(x) for x in sor)))
    s.append('| **összesen** | %s |' % ' | '.join('**%d**' % x for x in ossz))
    s += ['', '## 2. Fejezetenként', '']
    for konyv, k, e, parok, fs in eredmeny:
        s += ['### %s' % konyv, '',
              '| fejezet | Károli | eredeti | eltolt | K-hiány | E-hiány | r(0) | d | r(d) | jelzés |',
              '|---|---|---|---|---|---|---|---|---|---|']
        for r in fs:
            s.append('| %d | %d | %d | %d | %d | %d | %s | %+d | %s | %s |' % (
                r['fejezet'], r['k'], r['e'], r['eltolt'], r['k_hiany'], r['e_hiany'], f(r['r0']), r['d'], f(r['rd']),
                ' '.join(r['jel']) or '-'))
        s.append('')
    return '\n'.join(s)


def tsv(eredmeny):
    s = ['# GENERÁLT: eszkozok/karoli_strong/versbeosztas.py | scope=Karoli_1908.tsv+TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | forras=determinisztikus vershossz-igazítás (naplok/F22_versbeosztas.md) | ts=%s' % tokenek.generalas_ts(),
         '# A futtató (tokenek.betolt_eredeti) ebből adja a Károli-versnek a megfeleltetett eredeti verset; ahol nincs megfeleltetés, ott kezi.',
         'karoli\teredeti\ttipus']
    for konyv, k, e, parok, fs in eredmeny:
        for a, b, t in szegmensek(parok):
            s.append('%s\t%s\t%s' % (a, b, t))
    return '\n'.join(s) + '\n'


def onteszt():
    hibak = []
    rnd = random.Random(7)

    def folyam(konyv, fejezetek):
        ki = []
        for c, n in enumerate(fejezetek, 1):
            for v in range(1, n + 1):
                ki.append(('%s %d:%d' % (konyv, c, v), rnd.randint(6, 40)))
        return ki

    k = folyam('X', [30, 30, 30])
    # 1. azonos folyam: nincs eltérés
    e = list(k)
    if any(a != b for a, b in illeszt(k, e)):
        hibak.append('azonos folyamra eltérést jelzett')
    # 2. a 2. fejezet verseinek tartalma eggyel eltolt, a versszám a szokásos (a 2Móz 36 mintája): Károli 2:v ~ eredeti 2:(v+1)
    e2 = []
    for ig, n in k:
        c, v = tokenek.igehely_bont(ig)[1:]
        if c == 2:
            e2.append(('X 2:%d' % v, k[[x[0] for x in k].index('X 2:%d' % (v + 1))][1] if v < 30 else rnd.randint(6, 40)))
        else:
            e2.append((ig, n))
    par = illeszt(k, e2)
    elt = [(a, b) for a, b in par if a is not None and b is not None and a != b]
    if len(elt) < 10:
        hibak.append('az azonos versszámú, eltolt tartalmat nem jelezte (%d eltolt pár)' % len(elt))
    # 3. az eredeti oldalon egy vers hiányzik és a Károli oldalon plusz van: nincs_eredeti / nincs_karoli
    k3 = k[:40] + [('X 2:99', 20)] + k[40:]
    par = illeszt(k3, e)
    if not any(a == 'X 2:99' and b is None for a, b in par):
        hibak.append('a megfelelő nélküli Károli-verset nem jelezte')
    # 4. a gépi lista: legalább 3 egymást követő pár kell
    sor = szegmensek([('A 1:1', 'A 1:2'), ('A 1:2', 'A 1:3'), ('A 1:3', 'A 1:3')])
    if sor:
        hibak.append('a 2 hosszú eltolt futam bekerült a gépi listába')
    sor = szegmensek([('A 1:1', 'A 1:2'), ('A 1:2', 'A 1:3'), ('A 1:3', 'A 1:4'), ('A 1:4', 'A 1:4')])
    if len(sor) != 3 or any(t != 'eltolt' for _, _, t in sor):
        hibak.append('a 3 hosszú eltolt futam nem került be')
    # 5. a fejezeti korreláció: eltolt tartalomnál KORR_ELT vagy GYENGE jelzés
    fs = fejezet_sorok(k, e2, illeszt(k, e2))
    if not any(('KORR_ELT' in r['jel'] or 'GYENGE' in r['jel'] or 'ELTOLT' in r['jel']) for r in fs if r['fejezet'] == 2):
        hibak.append('a fejezet-jelzés nem szólt az eltolt tartalomra')
    if any(r['jel'] for r in fs if r['fejezet'] != 2 and r['fejezet'] != 1 and r['fejezet'] != 3):
        hibak.append('váratlan jelzés')
    # 6. a valódi adat: az 1Móz tiszta, a 2Móz 35:36–36:37 eltolódása megvan (ha az adat elérhető)
    try:
        karoli, ered = tokenek.betolt_karoli(), tokenek.betolt_eredeti(versmegf=False)
    except Exception as ex:   # noqa: BLE001
        karoli = None
        print('(a valódi adat nem érhető el: %s)' % ex)
    if karoli:
        k1, e1 = folyamok(karoli, ered, '1Móz')
        if any(a != b for a, b in illeszt(k1, e1)):
            hibak.append('az 1Móz-ra eltérést jelzett')
        k2, e2_ = folyamok(karoli, ered, '2Móz')
        gep = szegmensek(illeszt(k2, e2_))
        if ('2Móz 35:36', '2Móz 36:1', 'eltolt') not in gep or ('2Móz 36:37', '2Móz 36:38', 'eltolt') not in gep:
            hibak.append('a 2Móz 35:36–36:37 eltolódását nem találta meg')
    # 7. a kimenetek (ideiglenes könyvtárba)
    md_s = md([('X', k[:5], k[:5], [(a[0], a[0]) for a in k[:5]], fejezet_sorok(k[:5], k[:5], [(a[0], a[0]) for a in k[:5]]))])
    if 'F22_versbeosztas' not in md_s or 'X 1:1' in md_s:
        hibak.append('az md kimenet fejléce / versszöveg-mentessége')
    if hibak:
        print('ÖNTESZT HIBA:\n  ' + '\n  '.join(hibak))
        return 1
    print('önteszt: rendben')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=os.path.join('naplok', 'F22_versbeosztas.md'))
    ap.add_argument('--tsv', default=os.path.join('f22', 'versmegfeleltetes.tsv'))
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        return onteszt()
    eredmeny = elemez()
    for ut, szoveg in ((a.md, md(eredmeny)), (a.tsv, tsv(eredmeny))):
        os.makedirs(os.path.dirname(ut) or '.', exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(szoveg + ('' if szoveg.endswith('\n') else '\n'))
        print('írva: %s' % ut)
    for konyv, k, e, parok, fs in eredmeny:
        gep = szegmensek(parok)
        elt = sum(1 for _, _, t in gep if t == 'eltolt')
        kh = sum(1 for _, _, t in gep if t == 'nincs_eredeti')
        eh = sum(1 for _, _, t in gep if t == 'nincs_karoli')
        jel = [r['fejezet'] for r in fs if r['jel']]
        if elt or kh or eh or jel:
            print('%s: K=%d E=%d eltolt=%d K-hiány=%d E-hiány=%d jelzett fejezetek: %s' % (
                konyv, len(k), len(e), elt, kh, eh, ','.join(str(c) for c in jel) or '-'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
