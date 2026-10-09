#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F85.1 — a TAHOT_kivonat.tsv kulcsai és a sorok tartalma Károli-verse közti eltérések esetlistája (az egész ÓSZ).

Csak olvas; a TAHOT_kivonat.tsv-t, az f22/ és a parok_* táblákat nem módosítja. Kimenet: egyetlen TSV
(--ki, alapértelmezés naplok/F85_esetlista.tsv) + a stdout összegzése.

Módszer (determinisztikus, API nélkül):
  1. Könyvenként a TAHOT versfolyamot (kulcs szerint rendezve; a vers tartalma = a sorok H<1..8999> Strong-halmaza,
     a H9xxx elöljáró/funkciókódok nélkül) monoton igazítja a Macula (MT/WLC) versfolyamához (Needleman-Wunsch,
     pontszám = Jaccard - 0,30; sáv +-80 vers; döntetlenben a azonos számozás +0,01). A versszám tehát NEM
     bemenet, csak döntetlen-feloldó.
  2. A Macula-vers Károli-versét a Macula saját `karoli` oszlopa adja (KK-alapú, tvtms/kézi). Ez a tartalom Károli-verse.
  3. Független tanú: a KJV (KJV_Strongs_teljes.tsv) Strong-halmaza a Károli-vers `igehely_kjv` megfelelőjén
     (Karoli_versmegfeleltetes.tsv; ahol nincs sor, azonos kulcs) - Jaccard a TAHOT-vers halmazával.
  4. Besorolás: eltolas / osszevonas_1_2 / osszevonas_2_1 / valodi_hiany_tahot / valodi_hiany_karoli / bizonytalan.
     Az azonos kulcsú, igazolt (identitás) versek nem kerülnek a listába, csak az összegzésbe.

Használat:
    python eszkozok/tahot_verskulcs_esetlista.py [--ki naplok/F85_esetlista.tsv]
"""
import argparse
import datetime
import glob
import math
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')

SAV = 80
ILL_KUSZOB = 0.30      # a DP-pár pontszám-eltolása
KORR_MIN = 8
BIZONYTALAN_J = 0.50   # ennél kisebb WLC-Jaccard: bizonytalan
KJV_IGAZOL_J = 0.50    # a KJV-tanú igazol (alacsony WLC-illeszkedésű azonos kulcsnál: KJV_IGAZOL_J + 0,1)


def bont(ig):
    """'1Móz 3:16' -> ('1Móz', 3, 16)"""
    k, r = ig.rsplit(' ', 1)
    c, v = r.split(':')
    return k, int(c), int(v)


def strong_szam(s):
    m = re.fullmatch(r'H0*(\d+)[a-z]?', s)
    if not m:
        return None
    n = int(m.group(1))
    return n if 0 < n < 9000 else None


def betolt_tahot():
    ver = {}
    sorrend = []
    with open(os.path.join(K, 'TAHOT_kivonat.tsv'), encoding='utf-8') as fh:
        next(fh)
        for sor in fh:
            p = sor.rstrip('\n').split('\t')
            ig = p[0]
            if ig not in ver:
                ver[ig] = [set(), 0]
                sorrend.append(ig)
            n = strong_szam(p[1])
            if n:
                ver[ig][0].add(n)
                ver[ig][1] += 1
    return ver


def betolt_karoli():
    ki = []
    with open(os.path.join(K, 'Karoli_1908.tsv'), encoding='utf-8') as fh:
        next(fh)
        for sor in fh:
            ki.append(sor.split('\t', 1)[0])
    return ki


def betolt_macula():
    """{konyv: {(mt_fej, mt_vers): [strongszett, {karoli-versek}, allapotok]}}"""
    ki = {}
    for f in sorted(glob.glob(os.path.join(K, 'Macula_heber_*.tsv'))):
        konyv = None
        adat = {}
        sorok = []
        with open(f, encoding='utf-8') as fh:
            for sor in fh:
                if sor.startswith('#') or sor.startswith('xml_id'):
                    continue
                p = sor.rstrip('\n').split('\t')
                if len(p) < 9:
                    continue
                sorok.append(p)
                if konyv is None and p[2]:
                    konyv = p[2].split(';')[0].rsplit(' ', 1)[0]
        for p in sorok:
            m = re.match(r'[A-Z0-9]+ (\d+):(\d+)!', p[1])
            kulcs = (int(m.group(1)), int(m.group(2)))
            e = adat.setdefault(kulcs, [set(), set(), set()])
            n = strong_szam(p[7])
            if n:
                e[0].add(n)
            for kk in p[2].split(';'):
                if kk:
                    e[1].add(kk)
            e[2].add(p[3])
        ki[konyv] = adat
    return ki


def betolt_kjv():
    norm = {}
    with open(os.path.join(K, 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8') as fh:
        next(fh)
        for sor in fh:
            p = sor.rstrip('\n').split('\t')
            norm[p[0]] = p[1]
    ver = {}
    with open(os.path.join(K, 'KJV_Strongs_teljes.tsv'), encoding='utf-8') as fh:
        for sor in fh:
            if sor.startswith('#') or sor.startswith('Igehely'):
                continue
            p = sor.rstrip('\n').split('\t')
            if len(p) < 3:
                continue
            b, c, v = p[0].split('.')
            hu = norm.get(b)
            if not hu:
                continue
            n = strong_szam(p[2])
            if n:
                ver.setdefault('%s %s:%s' % (hu, c, v), set()).add(n)
    return ver


def betolt_kjvmap():
    m = {}
    with open(os.path.join(K, 'Karoli_versmegfeleltetes.tsv'), encoding='utf-8') as fh:
        for sor in fh:
            if sor.startswith('#') or sor.startswith('igehely_karoli'):
                continue
            p = sor.rstrip('\n').split('\t')
            if len(p) >= 3 and p[1]:
                k = p[0]
                konyv = k.rsplit(' ', 1)[0]
                m[k] = '%s %s' % (konyv, p[1])
    return m


def betolt_karoli_szoveg():
    ki = {}
    with open(os.path.join(K, 'Karoli_1908.tsv'), encoding='utf-8') as fh:
        next(fh)
        for sor in fh:
            p = sor.rstrip('\n').split('\t', 1)
            ki[p[0]] = p[1] if len(p) > 1 else ''
    return ki


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


def jaccard(a, b):
    if not a and not b:
        return 0.0
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def igazit(tk, mk, tver, mver, konyv):
    """tk: [(fej,vers)] TAHOT; mk: [(fej,vers)] Macula. Visszaad: [(t_index|None, m_index|None, J)]."""
    n, m = len(tk), len(mk)
    ts = [tver['%s %d:%d' % (konyv, c, v)][0] for c, v in tk]
    ms = [mver[x][0] for x in mk]
    cache = {}

    def pont(i, j):
        k = (i, j)
        if k not in cache:
            jj = jaccard(ts[i], ms[j])
            cache[k] = (jj, jj - ILL_KUSZOB + (0.01 if tk[i] == mk[j] else 0.0))
        return cache[k][1]

    neg = float('-inf')
    d = {(0, 0): 0.0}
    vissza = {}
    for i in range(n + 1):
        for j in range(max(0, i - SAV), min(m, i + SAV) + 1):
            if i == 0 and j == 0:
                continue
            leg, lep = neg, None
            if i > 0 and j > 0 and (i - 1, j - 1) in d:
                v = d[(i - 1, j - 1)] + pont(i - 1, j - 1)
                if v > leg:
                    leg, lep = v, 'p'
            if i > 0 and (i - 1, j) in d:
                v = d[(i - 1, j)]
                if v > leg:
                    leg, lep = v, 't'
            if j > 0 and (i, j - 1) in d:
                v = d[(i, j - 1)]
                if v > leg:
                    leg, lep = v, 'm'
            if lep:
                d[(i, j)] = leg
                vissza[(i, j)] = lep
    if (n, m) not in vissza:
        raise SystemExit('az igazítás nem fér a sávba: %s %d/%d' % (konyv, n, m))
    i, j = n, m
    ki = []
    while i > 0 or j > 0:
        lep = vissza[(i, j)]
        if lep == 'p':
            ki.append((i - 1, j - 1, cache[(i - 1, j - 1)][0]))
            i, j = i - 1, j - 1
        elif lep == 't':
            ki.append((i - 1, None, 0.0))
            i -= 1
        else:
            ki.append((None, j - 1, 0.0))
            j -= 1
    return ki[::-1]


def olvas_tsv(ut):
    """A '#' sorok és a fejléc nélkül: [[mezők]] (split a tabulátoron, a csv modul tilos)."""
    with open(ut, encoding='utf-8') as fh:
        sorok = [s.rstrip('\n').rstrip('\r') for s in fh if s.strip() and not s.startswith('#')]
    return [s.split('\t') for s in sorok[1:]]


def hatekony_tabla():
    """A #22 tényleges K->T táblája (detektor + kézi javítás, mint tokenek._kezi_javitas): [(karoli, eredeti, tipus)]."""
    sor = [tuple((r + ['', '', ''])[:3]) for r in olvas_tsv(os.path.join(ROOT, 'f22', 'versmegfeleltetes.tsv'))]
    kezi = [tuple((r + ['', '', ''])[:3]) for r in olvas_tsv(os.path.join(ROOT, 'f22', 'versmegfeleltetes_kezi.tsv'))]
    for k, e, t in kezi:
        if k:
            sor = [r for r in sor if r[0] != k]
        if e:
            sor = [r for r in sor if not (r[0] == '' and r[1] == e)]
    return sor + [(k, e, t) for k, e, t in kezi if t != 'torol']


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ki', default=os.path.join(ROOT, 'naplok', 'F85_esetlista.tsv'))
    a = ap.parse_args(argv)

    tver = betolt_tahot()
    karoli_mind = betolt_karoli()
    macula = betolt_macula()
    kjv = betolt_kjv()
    tabla = hatekony_tabla()
    osszev = olvas_tsv(os.path.join(ROOT, 'f22', 'versosszevonas.tsv'))

    konyvek = []
    for ig in tver:
        b = bont(ig)[0]
        if b not in konyvek:
            konyvek.append(b)
    karoli = [k for k in karoli_mind if bont(k)[0] in konyvek]
    kset = set(karoli)
    tset = set(tver)

    # --- 1. a T-vers tartalmának MT-párja (Strong-illeszkedés) ---
    t_m = {}
    for konyv in konyvek:
        if konyv not in macula:
            print('FIGYELEM: nincs Macula-könyv: %s' % konyv)
            continue
        tk = sorted((bont(ig)[1], bont(ig)[2]) for ig in tset if bont(ig)[0] == konyv)
        mver = macula[konyv]
        mk = sorted(mver)
        for ti, mj, jj in igazit(tk, mk, tver, mver, konyv):
            if ti is None:
                continue
            t = '%s %d:%d' % (konyv, *tk[ti])
            if mj is None:
                t_m[t] = (None, 0.0, set(), set())
            else:
                t_m[t] = ('%s %d:%d' % (konyv, *mk[mj]), jj, set(mver[mk[mj]][1]), mver[mk[mj]][2])

    # --- 2. a #22 tényleges K<->T hozzárendelése ---
    t_k = {}
    k_t = {}
    k_nincs_er = []
    t_nincs_k = []
    for k, e, tip in tabla:
        if tip == 'eltolt':
            t_k.setdefault(e, []).append(k)
            k_t.setdefault(k, []).append(e)
        elif tip == 'nincs_eredeti':
            k_nincs_er.append(k)
        elif tip == 'nincs_karoli':
            t_nincs_k.append(e)
    for r in osszev:
        k, e = r[0], r[3]
        if k not in t_k.setdefault(e, []):
            t_k[e].append(k)
        if e not in k_t.setdefault(k, []):
            k_t[k].append(e)

    # --- 3. a végleges K<->T leképezés (a #22 tábla; az összevonás-fájl felülírja a nincs_karoli jelzést) ---
    osszev_t = {r[3] for r in osszev}
    t_nincs_k = [t for t in t_nincs_k if t not in osszev_t]
    kezi_par = {(r[0], r[1]) for r in olvas_tsv(os.path.join(ROOT, 'f22', 'versmegfeleltetes_kezi.tsv')) if r[0] and r[1]}
    kezi_par |= {(r[0], r[3]) for r in osszev}
    t_kv = {}
    for t in tset:
        if t in t_k:
            t_kv[t] = list(t_k[t])
        elif t in kset and t not in t_nincs_k:
            t_kv[t] = [t]
        else:
            t_kv[t] = []
    k_tv = {}
    for t, ks in t_kv.items():
        for k in ks:
            k_tv.setdefault(k, []).append(t)

    # hosszak a fejezeti korrelációhoz (Károli: szószám; TAHOT: a nem-előtag sorok száma)
    klen = {k: len(sz.split()) for k, sz in betolt_karoli_szoveg().items()}
    tlen = {t: n for t, (st, n) in tver.items()}

    fej_t = {}
    for ig in tset:
        fej_t.setdefault(bont(ig)[:2], []).append(ig)

    def rmap(b, c, fn):
        """A (b, c) fejezet T-versei hosszának és a fn(T) által adott Károli-vers hosszának korrelációja (log-hossz)."""
        a, bb = [], []
        for ig in fej_t.get((b, c), []):
            k = fn(ig)
            if k and k in klen:
                a.append(math.log(max(1, tlen[ig])))
                bb.append(math.log(max(1, klen[k])))
        if len(a) < KORR_MIN:
            return None
        return pearson(a, bb)

    def f_azon(t):
        return t

    def f_22(t):
        ks = t_kv.get(t, [])
        return ks[0] if len(ks) == 1 else None

    def f_mac(t):
        mk_ = t_m.get(t, (None, 0.0, set(), set()))[2]
        return sorted(mk_)[0] if len(mk_) == 1 else None

    def f2(x):
        return '-' if x is None else '%.2f' % x

    sorok = []
    elvetett_macula = {}
    osszes = {'tahot_vers': len(tset), 'identitas_igazolt': 0, 'identitas_alacsony_J': 0, 'identitas_igazolt_KJV': 0, 'macula_elvetve_hossz': 0}
    for t in sorted(tset, key=lambda x: (konyvek.index(bont(x)[0]), bont(x)[1:])):
        b, c, v = bont(t)
        m, jj, mac_k, allap = t_m.get(t, (None, 0.0, set(), set()))
        ts = tver[t][0]
        ks = t_kv[t]
        sima = (ks == [t] and len(k_tv.get(t, [])) == 1)
        mac_ellen = bool(mac_k) and not (set(ks) & mac_k)
        legjobb = (0.0, '')
        if not sima or mac_ellen or jj < BIZONYTALAN_J:
            for cc in (c - 1, c, c + 1):
                for vv in range(1, 177):
                    kk = '%s %d:%d' % (b, cc, vv)
                    if kk in kjv:
                        jk = jaccard(ts, kjv[kk])
                        if jk > legjobb[0]:
                            legjobb = (jk, kk)
        macs = ';'.join(sorted(mac_k, key=lambda x: bont(x)[1:])) or '-'
        ig = 'WLC=%s J=%.2f | Macula-Károli=%s | KJV-legjobb=%s J=%.2f' % (m or '-', jj, macs, legjobb[1] or '-', legjobb[0])
        if sima:
            if jj < BIZONYTALAN_J and legjobb[1] == t and legjobb[0] >= KJV_IGAZOL_J + 0.1:
                osszes['identitas_igazolt_KJV'] += 1
                continue
            if jj < BIZONYTALAN_J:
                osszes['identitas_alacsony_J'] += 1
                sorok.append((b, c, t, t, 'bizonytalan', 'azonos kulcs, de a WLC-illeszkedés alacsony | ' + ig))
                continue
            if mac_ellen:
                # a #22 szerint azonos kulcs, a Macula más Károli-verset ad: a Károli-oldali hossz dönt
                r0 = rmap(b, c, f_azon)
                rd = rmap(b, c, f_mac)
                d = (bont(sorted(mac_k)[0])[2] - v) if len(mac_k) == 1 else 0
                if r0 is not None and rd is not None and r0 >= rd + 0.05:
                    osszes['macula_elvetve_hossz'] += 1
                    elvetett_macula.setdefault((b, c), []).append((v, d, r0, rd))
                    continue
                sorok.append((b, c, t, t, 'bizonytalan',
                              'a #22 szerint azonos kulcs, a Macula más Károli-verset ad; hosszkorreláció (fejezet): r(azonos)=%s, r(Macula)=%s | %s' % (f2(r0), f2(rd), ig)))
                continue
            osszes['identitas_igazolt'] += 1
            continue
        # innentől a T-nél eltérés / összevonás / hiány van
        if not ks:
            sorok.append((b, c, t, '', 'valodi_hiany_tahot',
                          'nincs Károli-megfelelő (#22: nincs_karoli) | ' + ig))
            continue
        ks_s = ';'.join(sorted(ks, key=lambda x: bont(x)[1:]))
        if len(ks) > 1:
            tip = 'osszevonas_1_2'
        elif len(k_tv.get(ks[0], [])) > 1:
            tip = 'osszevonas_2_1'
        else:
            tip = 'eltolas'
        kezi = any((k, t) in kezi_par for k in ks)
        r0 = rmap(b, c, f_azon)
        r22 = rmap(b, c, f_22)
        hossz = 'hosszkorreláció (fejezet): r(azonos)=%s, r(#22)=%s' % (f2(r0), f2(r22))
        if mac_ellen:
            rm = rmap(b, c, f_mac)
            if r22 is not None and rm is not None and r22 >= rm + 0.05:
                szint, tip2 = 'H', tip      # a hossz a #22 mellett, a Macula ellenében
            else:
                szint, tip2 = 'ellentmond', 'bizonytalan'
            hossz += ', r(Macula)=%s' % f2(rm)
        elif mac_k:
            szint, tip2 = 'A', tip
        else:
            szint, tip2 = 'B', tip
        if kezi and szint in ('B', 'H'):
            szint = szint + '+kezi'
        if r0 is not None and r22 is not None and r0 > r22 + 0.1:
            tip2 = 'bizonytalan'
            hossz += ' (a hossz az azonos kulcsot támogatja)'
        if jj < BIZONYTALAN_J or any(k not in kset for k in ks):
            tip2 = 'bizonytalan'
        sorok.append((b, c, t, ks_s, tip2, 'szint=%s | #22-tipus=%s | %s | %s' % (szint, tip, hossz, ig)))

    for k in karoli:
        if k in k_tv:
            continue
        b, c, v = bont(k)
        kulcs = ' (a %s TAHOT-kulcs létezik, de a #22 szerint más Károli-verset hordoz)' % k if k in tset else ''
        sorok.append((b, c, '', k, 'valodi_hiany_karoli',
                      'a Károli-versnek nincs TAHOT-tartalma' + (' (#22: nincs_eredeti)' if k in k_nincs_er else ' (a #22-ben sincs)') + kulcs))

    kulcs_t_nelkul_k = sorted(tset - kset, key=lambda x: (konyvek.index(bont(x)[0]), bont(x)[1:]))
    kulcs_k_nelkul_t = [k for k in karoli if k not in tset]
    magyarazott_t = {s[2] for s in sorok if s[2]}
    magyarazott_k = set()
    for s in sorok:
        for kk in s[3].split(';'):
            if kk:
                magyarazott_k.add(kk)
    nem_listazott_t = [x for x in kulcs_t_nelkul_k if x not in magyarazott_t]
    nem_listazott_k = [x for x in kulcs_k_nelkul_t if x not in magyarazott_k]

    def rend(s):
        ig = s[2] or s[3].split(';')[0]
        return (konyvek.index(s[0]), s[1], bont(ig)[2], s[2])

    sorok.sort(key=rend)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    tipusok = {}
    for s in sorok:
        tipusok[s[4]] = tipusok.get(s[4], 0) + 1
    with open(a.ki, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_esetlista.py | scope=TAHOT_kivonat.tsv teljes ÓSZ (%d vers, %d könyv) | forras=konkordancia/TAHOT_kivonat.tsv, Macula_heber_*.tsv (WLC és karoli oszlop), KJV_Strongs_teljes.tsv, Karoli_1908.tsv, f22/versmegfeleltetes.tsv, f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv | ts=%s\n' % (len(tset), len(konyvek), ts))
        fh.write('# tipus: eltolas (1:1, a tartalom Károli-verse más, mint a kulcs) | osszevonas_1_2 (egy TAHOT-vers több Károli-verset hordoz) | osszevonas_2_1 (több TAHOT-vers egy Károli-versben) | valodi_hiany_tahot (a TAHOT-versnek nincs Károli-párja) | valodi_hiany_karoli (a Károli-versnek nincs TAHOT-tartalma) | bizonytalan. A karoli_vers oszlop a javasolt kulcs. szint=A: a #22 és a Macula egyezik; B: a Macula nem ad Károli-verset, csak a #22 hossz-detektor/kézi tábla; ellentmond: eltér. Az azonos kulcsú, WLC-vel igazolt (J>=%.2f) versek nincsenek a listában.\n' % BIZONYTALAN_J)
        fh.write('konyv\tfejezet\ttahot_kulcs\tkaroli_vers\ttipus\tigazolas\n')
        for s in sorok:
            fh.write('\t'.join([s[0], str(s[1]), s[2], s[3], s[4], s[5]]) + '\n')
    elv_ut = os.path.join(os.path.dirname(a.ki), 'F85_macula_elvetve.tsv')
    with open(elv_ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_esetlista.py | ts=%s | azok a fejezetek, ahol a #22 tábla szerint azonos kulcs van, a Macula `karoli` oszlopa más Károli-verset ad, és a Károli-oldali hosszkorreláció az azonos kulcsot támogatja (r0 >= r(d)+0,05): a Macula-jelzés elvetve\n' % ts)
        fh.write('konyv\tfejezet\telvetett_versek\tmacula_eltolas_d\tr0\tr_d\n')
        for (bb, cc), l in sorted(elvetett_macula.items(), key=lambda x: (konyvek.index(x[0][0]), x[0][1])):
            fh.write('\t'.join([bb, str(cc), str(len(l)), str(l[0][1]), f2(l[0][2]), f2(l[0][3])]) + '\n')
    print('írva: %s (%d sor)' % (a.ki, len(sorok)))
    print('elvetett Macula-jelzés fejezetei: %d (%s)' % (len(elvetett_macula), elv_ut))
    print('típusok:', tipusok)
    print('azonos kulcs:', osszes)
    print('TAHOT-kulcs Károli-vers nélkül: %d; ebből nincs a listában: %s' % (len(kulcs_t_nelkul_k), nem_listazott_t))
    print('Károli-vers TAHOT-kulcs nélkül: %d; ebből nincs a listában: %s' % (len(kulcs_k_nelkul_t), nem_listazott_k))
    return 0


if __name__ == '__main__':
    sys.exit(main())
