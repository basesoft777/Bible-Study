#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_import.py -- F16 (FELADATOK #16, N30): a BSB teljes Biblia-merese es importja.

Modszer: azonos az eszkozok/fj2/bsb.py (F06, PR #75) 1Mozes-meresevel:
  - kuszob es definicio az eszkozok/fj2/kuszob.txt-bol (kuszob=95, definicio=tahot_resze_bsb,
    nevezo=tahot_lefedett_versek); a szkript ezt nem modositja;
  - egyezes: a vers forras-Strong-halmaza (TAHOT: H, 9000-es prefixkodok nelkul) resze a
    BSB-halmaznak; nevezo: a forrassal rendelkezo versek;
  - UJ (a 27 ujszovetsegi konyvre): a forras a konkordancia/TAGNT_kivonat.tsv (G-Strongok),
    minden mas azonos. A BSB-oldali Strong-gyujtes (bsb.bsb_vers_strongok) csak H-t gyujt;
    itt a [HG] mintat a konyv nyelvehez szurjuk.
F41 (FELADATOK #41, DT6 b+e): az OSZ-konyvek BSB-vers -> MT-vers (TAHOT_kivonat-szamozas) megfeleltetese VERSSZINTU, Strong-illeszkedessel
(konyv_megfeleltetes; a szkript eltolast mar nem csak a Zsoltarokra alkalmaz); a meres es az import ezt hasznalja, a kuszob/definicio/nevezo
valtozatlan. Az import 6. oszlopa: "Angol szó állapota" (forditva / elhagyva / ures_jelzo_nelkul). N-F41c: a konyvnev-alias (JSir -> Sir)
miatti nema 0%-os konyv helyett hangos hiba (0 illesztett sor / 0 egyezo vers -> leallas).
F41 (DT-F41c (a), DT-F41b lezarva, DT-F41f; felhasznaloi dontes 2026.10.02): a cel-versszamozas az MT (WLC, a Macula-tablak). A BSB_Strongs.tsv 7. oszlopa (`Számozás`) VERSSZINTU
WLC-osszevetesbol jon (wlc_versek.vers_egyezik): mt = az Igehely-vers sorainak Strong-halmaza tartalmazza a WLC azonos szamu versenek halmazanak tobb mint felet;
kjv = nem igazolt, es a BSB(KJV)-szam marad (a Job 38-41, a mainen is KJV-szamozasu volt); ellenorizetlen = nem igazolt (a TAHOT_kivonat hibrid szamozasa; a Job MT-re
szamozasa es az ellenorizetlen versek MT-re szamozasa kulon N-tetel: N-F41g, N-F41h). A BSB(KJV)-szam marad (nincs atszamozas) a Pred 11/12, Ezs 2/3 es a 4Moz 12/13 fejezetekben
(a WLC fejezet-max egyezik a BSB-vel: KJV = MT; a TAHOT_kivonat itt Karoli-szeru; a szkript ellenorzi, elteresnel megall). A tobbi vers a TAHOT_kivonat szamozasahoz illesztett
(Strong-illeszkedes); fejezetenkenti kimutatas: naplok/F41_wlc_versszam_ellenorzes.tsv (eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py).
(A lenti F16-leiras tortenelmi: a Zsoltar-specifikus k-modell az F41-ben a verszintu megfeleltetes specialis esete; a Zsoltar-sorok valtozatlanok.)
A ZSOLTAROKON a BSB (KJV/angol) szamozasa nem egyezik a TAHOT/Karoli-kulcs (MT) szamozasaval: az MT a
feliratot sajat versszamon szamozza, a BSB nem (F16.8). A BSB-vers -> MT-vers megfeleltetes fejezetenkent
egy eltolas k = (a Karoli-kulcs igehely_mt oszlopabol az MT-fejezet utolso versszama) - (a BSB fejezet versszama,
base/text-only sorai); k csak 0..2 lehet (kulonben megall). A meres es a Zsolt-import az MT-verset hasznalja.
BELSO VERSOSZTAS (F16.11): ahol egy BSB-vers a v+k MT-versre nem illeszkedik, de a szomszedos MT-versre igen (vagy az MT-vers
a ket szomszedos BSB-vers unioja), a fejezet nem igazolhato (Zsolt 13): kimarad a merestol es az importbol.
A nem-zsoltar konyvek (1Sam 24, Pred 12, Ezs 3/9, Hos 12, Jon 2 ...) hasonlo eltolasat ez a szkript NEM
javitja (l. DT6); azokra a F06-modszer (eltolas nelkul) marad.
UJSZOVETSEG: a BSB-import az Ószovetseg miatt keszult (a gorog reteg forrasa a Macula, #87): a 27 USZ-konyv
merese tajekoztato, az importbol szandekosan kimarad (eredmeny=USZ_KIHAGYVA, nem kuszob alatti hiba).
A kuszobot elero OSZ-konyveket importalja: konkordancia/BSB_Strongs.tsv (a KJV_Strongs_*.tsv
formatumaban: Igehely STEP-alakban, Szosorszam, Strong-szam, Angol szo, Morfologiai kod (ures)).

Hasznalat:  python eszkozok/fj2/bsb_import.py --munka <mappa>   (a mappaban bsb-data-output/ klon)

Kimenet: naplok/F16_bsb_lefedettseg.tsv, konkordancia/BSB_Strongs.tsv.
"""

import argparse
import bisect
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb  # noqa: E402
import wlc_versek  # noqa: E402

URL = bsb.URL
STRONG_MINTA = {'H': re.compile(r'H0*(\d+)'), 'G': re.compile(r'G0*(\d+)')}
SZURT = {'nem_szamjegy_versszam_kulcs (meres)': 0, 'nem_szamjegy_versszam_kulcs (import)': 0, 'angol_szo_allapot=forditva': 0, 'angol_szo_allapot=elhagyva': 0, 'angol_szo_allapot=ures_jelzo_nelkul': 0, 'elided_jelzo_nem_ures_szoveggel': 0}  # kategoria -> darab: minden, ami a mereshez/importhoz nem kerul be, itt szamolodik


def szur(kat, n=1):
    SZURT[kat] = SZURT.get(kat, 0) + n


# DT-F41c (a): a BSB(KJV)-szamozas marad, sorszinten jelolve (7. oszlop `Számozás` = kjv_szamozas)
KJV_MARAD = {'Jób': {38, 39, 40, 41}}  # a mainen is KJV-szamozasu; a Job MT-re szamozasa kulon N-tetel (TVTMS/WLC gepi tablabol)
KJV_EGYEZIK_WLC = {'Préd': {11, 12}, 'Ézs': {2, 3}, '4Móz': {12, 13}}  # BSB(KJV) = WLC (fejezet-max egyezes, wlc_versek); a TAHOT_kivonat Karoli-szeru; az atszamozas visszavonva
# 7. oszlop `Számozás` (felhasznaloi dontes 2026.10.02, DT-F41f): VERSSZINTU WLC-osszevetesbol: mt = az Igehely-vers sorainak Strong-halmaza tartalmazza a WLC azonos szamu
# versenek Strong-halmazanak tobb mint felet (igazolt MT-szam); kjv = nem igazolt, es a BSB(KJV)-szam marad (csak Job 38-41); ellenorizetlen = nem igazolt (a TAHOT_kivonat
# hibrid szamozasu, vagy a WLC-ben nincs ilyen vers / ures Strong-halmaz).
SZAMOZASOK = ('mt', 'kjv', 'ellenorizetlen')
KJV_JELOLT_FEJEZETEK = {'Jób': {38, 39, 40, 41}}

MT_ELTOLASOS_KONYVEK = ('Zsolt',)  # csak itt alkalmazzuk a BSB->MT eltolast (F16.8)


_KK_CACHE = {}


def kk_mt_max(mag):
    if mag not in _KK_CACHE:
        _KK_CACHE[mag] = _kk_mt_max(mag)
    return _KK_CACHE[mag]


def _kk_mt_max(mag):
    """{fejezet: MT-fejezet utolso versszama} a konkordancia/Karoli_versmegfeleltetes.tsv `igehely_mt` oszlopabol
    (a Karoli-kulcs az iranyado az MT-szamozasra). Csak `fej:vers` alaku ertek szamit."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Karoli_versmegfeleltetes.tsv'))
    i = fej.index('igehely_mt')
    ki = {}
    for sor in sorok:
        if len(sor) <= i:
            continue
        m = re.fullmatch(r'(\d+):(\d+)', sor[i])
        if m and sor[0].rsplit(' ', 1)[0] == mag:
            f, v = int(m.group(1)), int(m.group(2))
            ki[f] = max(ki.get(f, 0), v)
    return ki


def fejezet_eltolasok(mag, fejezetek, text_only_db, tahot_max):
    """{fejezet: k}: a BSB-vers v az MT-vers v+k. k = KK-MT-max - BSB-versszam (text-only). Ellenorzes: a TAHOT
    fejezet-max egyezzen a KK-MT-max-szal; k csak 0..2. Eltereskor megall (nincs csendes kozelites)."""
    kk = kk_mt_max(mag)
    ki = {}
    for fej in fejezetek:
        if fej in kk:
            mt_max = kk[fej]
        else:
            # a Karoli-kulcsban nincs igehely_mt ertek: KJV-osztaly, a szamozas azonos (k=0); a TAHOT-max-nak egyeznie kell
            mt_max = text_only_db[fej]
        k = mt_max - text_only_db[fej]
        if not 0 <= k <= 2:
            raise SystemExit('HIBA: %s %d: varatlan BSB->MT eltolas k=%d (KK-MT-max %s, BSB versszam %s)'
                             % (mag, fej, k, kk.get(fej), text_only_db[fej]))
        if tahot_max.get(fej, 0) != mt_max:
            raise SystemExit('HIBA: %s %d: a TAHOT-max (%s) nem egyezik a Karoli-kulcs MT-max-aval / a BSB-versszammal (%s)'
                             % (mag, fej, tahot_max.get(fej), mt_max))
        ki[fej] = k
    return ki


def belso_osztas_eltereses(b, forras, mag, fej, k):
    """A fejezet a szabalyos k-modellel NEM igazolhato, ha valamelyik BSB-vers a v+k MT-versre nem illeszkedik
    (TAHOT-Strongok nem resze a BSB-versnek), de a szomszedos MT-vers (v+k+-1) igen, vagy az MT-vers a ket
    szomszedos BSB-vers unioja (belso versosztas-eltereses: az MT-vers a BSB-ben ketto vagy fele). Visszaad:
    az okok listaja (ures = a k-modell nem cafolt). A ritka egyedi nem-egyezes (cimkezesi kulonbseg) nem ok."""
    ok = []
    for v in sorted(b):
        x = forras.get('%s %d:%d' % (mag, fej, v + k))
        if x is None or x <= b[v]:
            continue
        for d in (-1, 1):
            y = forras.get('%s %d:%d' % (mag, fej, v + k + d))
            if y and y <= b[v]:
                ok.append('BSB %d illeszkedik az MT %d-hoz (nem v+k=%d-hoz)' % (v, v + k + d, v + k))
            if v + d in b and x <= (b[v] | b[v + d]):
                ok.append('MT %d a BSB %d+%d unioja' % (v + k, v, v + d))
    return ok


# --- F41: versszintu BSB -> MT (TAHOT-kivonat-szamozas) megfeleltetes -------------------------------------
# A megfeleltetes forrasa a Strong-illeszkedes: monoton (sorrendtarto) 1:1 igazitas a BSB-versek es a TAHOT-versek
# kozott, a kapcsolat erteke = a TAHOT-vers Strong-halmazanak a BSB-versben levo hanyada. Az "mt_vers" a
# konkordancia/TAHOT_kivonat.tsv szamozasa (a Karoli-kulcs MT-oszlopa ezt kovetve igazolja a fejezet-maximumot).

TAHOT_NEV = {'JSir': 'Sir'}  # F28.9 (DT24) a Konyv_normalizalo_tablaban Lam-ot JSir-re nevezte at; a TAHOT-/Karoli-fajlok 'Sir'-t hasznalnak


def forras_nev(mag):
    """A konyv neve a TAHOT_kivonat / Karoli-kulcs fajlokban (az atnevezes miatt eltérhet a normalizalo tablatol)."""
    return TAHOT_NEV.get(mag, mag)


def _ref_bont(ref):
    """'Jon 2:1' -> (2, 1); csak a fejezet:vers resz."""
    cv = ref.rsplit(' ', 1)[1]
    f, v = cv.split(':')
    return int(f), int(v)


def mt_versek(forras, fmag):
    """(rendezett [((fejezet, vers), set(Strong))], {fejezet: max vers}) a forras-halmazokbol (TAHOT)."""
    lista = []
    for r, s in forras.items():
        if r.rsplit(' ', 1)[0] == fmag:
            try:
                lista.append((_ref_bont(r), s))
            except ValueError:
                continue
    lista.sort(key=lambda x: x[0])
    tmax = {}
    for (f, v), _ in lista:
        tmax[f] = max(tmax.get(f, 0), v)
    return lista, tmax


def versillesztes(bs, mt):
    """Monoton, 1:1 igazitas. bs/mt: rendezett [((fejezet, vers), set)] listak. Visszaad: {bsb_(f,v): mt_(f,v)}.
    Egy BSB-vers csak olyan MT-versre illeszthetõ, amelynek a fejezete legfeljebb 1-gyel tér el; a kapcsolat
    erteke 2*hanyad-1 (csak 0,5 feletti hanyad szamit), azonos szamozasnal +0,02 (dontetlen eseten az azonos nyer)."""
    n, m = len(bs), len(mt)
    mtf = [f for (f, v), s in mt]
    lo = [bisect.bisect_left(mtf, bs[i][0][0] - 1) for i in range(n)]
    hi = [bisect.bisect_right(mtf, bs[i][0][0] + 1) for i in range(n)]
    f = [[0.0] * (m + 1) for _ in range(n + 1)]
    ut = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        (c, v), b = bs[i - 1]
        sor, elozo = f[i], f[i - 1]
        for j in range(1, m + 1):
            legjobb, hogy = elozo[j], 1
            if sor[j - 1] > legjobb:
                legjobb, hogy = sor[j - 1], 2
            if lo[i - 1] < j <= hi[i - 1]:
                (c2, v2), t = mt[j - 1]
                if t:
                    hanyad = len(t & b) / len(t)
                    if hanyad > 0.5:
                        s = 2 * hanyad - 1 + (0.02 if (c2, v2) == (c, v) else 0.0)
                        if elozo[j - 1] + s > legjobb:
                            legjobb, hogy = elozo[j - 1] + s, 3
            sor[j], ut[i][j] = legjobb, hogy
    i, j, ki = n, m, {}
    while i > 0 and j > 0:
        h = ut[i][j]
        if h == 3:
            ki[bs[i - 1][0]] = mt[j - 1][0]
            i -= 1
            j -= 1
        elif h == 1:
            i -= 1
        else:
            j -= 1
    return ki


def egymas_utan(a, b, tmax):
    """b az a utani kovetkezo MT-vers? (azonos fejezet +1, vagy a kovetkezo fejezet 1. verse az a fejezet utolso verse utan)."""
    if b[0] == a[0] and b[1] == a[1] + 1:
        return True
    return b[0] == a[0] + 1 and b[1] == 1 and a[1] == tmax.get(a[0], -1)


def vers_sorrend(adat):
    """{vers: [Strong-szam (int) a Strong-hordozo spanok sorrendjeben]} egy BSB display-JSON fejezetbol.
    Ugyanazokat a spanokat sorolja, mint a vers_sorok (egy elem = egy importsor), tehat az index = Szosorszam-1."""
    ki = {}
    for vs, spanok in adat['eng'].items():
        if not str(vs).isdigit():
            continue
        seq = []
        for span in spanok:
            if isinstance(span, (list, tuple)) and len(span) >= 2 and span[1]:
                m = re.search(r'[HG]0*(\d+)', json.dumps(span[1]))
                if m:
                    seq.append(int(m.group(1)))
        ki[int(vs)] = seq
    return ki


def osztas_pont(seq, t1, t2):
    """Egy BSB-vers ket MT-versre osztasa (F41.1, D3: 1Kir 22:43 = MT 22:43 + 22:44). seq: a BSB-vers Strongjai spanonkent; t1, t2: a ket
    MT-vers Strong-halmaza. A vago pont p (1 <= p < len(seq)): seq[:p] tartalmazza t1-et, seq[p:] tartalmazza t2-t, es egyik fele sem
    tartalmaz a masik MT-vers kizarolagos Strongjabol. Csak akkor van megfeleltetes, ha p EGYERTELMU (pontosan egy ervenyes p), kulonben None."""
    if not seq or not t1 or not t2:
        return None
    jo = []
    for p in range(1, len(seq)):
        elso, masodik = set(seq[:p]), set(seq[p:])
        if t1 <= elso and t2 <= masodik and not (elso & (t2 - t1)) and not (masodik & (t1 - t2)):
            jo.append(p)
    return jo[0] if len(jo) == 1 else None


def konyv_megfeleltetes(mag, bsb_fej, forras, kk_max=None, sorrend=None):
    """Egy konyv versszintu megfeleltetese. bsb_fej: {fejezet: {vers: set(Strong)}} (a display-JSON); sorrend: {(fejezet, vers): [Strong
    a spanok sorrendjeben]} (az 1 BSB-vers -> 2 MT-vers osztas igazolasahoz; nelkule az osztas nem igazolhato).
    Visszaad: (sorok, fejezet_allapot, tmax, osztas) ahol
      sorok = [(bsb_(f,v), mt_(f,v) vagy None, modell, ok)]  (modell: azonos / eltolt / illesztetlen / kjv_szamozas),
      fejezet_allapot = {bsb_fejezet: [okok]} (ures lista = igazolt vagy kjv_szamozas; nem ures = a fejezet illesztetlen),
      tmax = {mt_fejezet: max vers},
      osztas = {bsb_(f,v): (elso_mt_vers, masodik_mt_vers, p)}: a BSB-vers elso p Strong-sora az elso, a tobbi a masodik MT-versre kerul.
    A fejezet illesztetlen, ha (R1) egy verse nem illesztheto es a szomszedaibol sem tolthetõ ki, (R2) egy vers a
    megfeleltetett MT-versre nem illeszkedik, de a szomszedos MT-versre igen (belso versosztas-eltereses, F16.11), (R3) egymas utani BSB-versek nem a
    TAHOT-kivonat egymas utani MT-versekre kerulnek (kimaradt MT-vers; kivetel: a kimaradt MT-vers igazolt osztasa, l. osztas_pont), (R4) a cel
    MT-fejezet TAHOT-maximuma nem egyezik a Karoli-kulcs igehely_mt maximumaval.
    kjv_szamozas (F41.1, D3): a BSB-fejezet MINDEN verse illesztetlen es a TAHOT_kivonatban a fejezetnek nincs egyetlen verse sem (a TAHOT_kivonat nem
    teljes: pl. Job 41); a megfeleltetes nem igazolhato, az Igehely a BSB(KJV)-szamozast tartja, jelolve; nincs a merestol."""
    fmag = forras_nev(mag)
    bs = [((f, v), bsb_fej[f][v]) for f in sorted(bsb_fej) for v in sorted(bsb_fej[f])]
    mt, tmax = mt_versek(forras, fmag)
    if not mt:
        raise SystemExit('HIBA: a TAHOT_kivonatban nincs "%s" nevu konyv (konyvnev-alias? l. TAHOT_NEV / N-F41c)' % fmag)
    mtd = dict(mt)
    mtlista = [r for r, _ in mt]
    mtidx = {r: i for i, r in enumerate(mtlista)}
    tahot_fejezetek = {r[0] for r in mtlista}
    ill = versillesztes(bs, mt)
    allapot = {f: [] for f in bsb_fej}
    leker, ok_szoveg, nincs_part = {}, {}, {}
    for f in sorted(bsb_fej):
        versek = sorted(bsb_fej[f])
        for v in versek:
            if (f, v) in ill:
                leker[(f, v)] = ill[(f, v)]
                continue
            # R1: kitoltes a fejezeten beluli kozvetlen szomszedokbol, ha a ket szomszed eltolasa azonos
            elo = next((u for u in range(v - 1, 0, -1) if (f, u) in ill), None)
            utan = next((u for u in range(v + 1, max(versek) + 1) if (f, u) in ill), None)
            if elo is not None and utan is not None:
                de = (ill[(f, elo)][0] - f, ill[(f, elo)][1] - elo)
                du = (ill[(f, utan)][0] - f, ill[(f, utan)][1] - utan)
                if de == du:
                    leker[(f, v)] = (f + de[0], v + de[1])
                    ok_szoveg[(f, v)] = 'kitoltve_a_szomszedok_eltolasabol'
                    continue
            leker[(f, v)] = None
            nincs_part.setdefault(f, []).append(v)
    kjv_fejezetek = set()
    for f, vl in nincs_part.items():
        if len(vl) == len(bsb_fej[f]) and f not in tahot_fejezetek:
            kjv_fejezetek.add(f)
            continue
        allapot[f].append('nincs_mt_part: %d vers (BSB %d:%s)' % (len(vl), f, ','.join(str(x) for x in vl[:6]) + (',...' if len(vl) > 6 else '')))
    # R2: a megfeleltetett MT-vers nem illeszkedik, de a szomszedos MT-vers igen (a szomszedos BSB-vers unioja-proba nem
    # kerul ide: a Strong-halmazok kozos (funkcio)szavai miatt tulzottan sok hamis jelzest adna; a valodi kette-/osszevonast
    # az R1 (illesztetlen BSB-vers) es az R3 (kimaradt MT-vers) fogja meg)
    for (f, v), b in bs:
        x = leker.get((f, v))
        if x is None or x not in mtd or mtd[x] <= b:
            continue
        i = mtidx[x]
        for d in (-1, 1):
            if 0 <= i + d < len(mtlista):
                y = mtlista[i + d]
                if mtd[y] and mtd[y] <= b:
                    allapot[f].append('vers_osztas: BSB %d:%d illeszkedik az MT %d:%d-hoz (nem a megfeleltetett %d:%d-hoz)' % (f, v, y[0], y[1], x[0], x[1]))

    # R3: egymas utani BSB-versek a TAHOT-kivonat egymas utani MT-verseire kerulnek (a TAHOT sajat sorrendje; fejezethatar is, pl. Job 39:38 -> 40:6)
    osztas = {}
    for f in sorted(bsb_fej):
        versek = sorted(bsb_fej[f])
        for a, b2 in zip(versek, versek[1:]):
            xa, xb = leker.get((f, a)), leker.get((f, b2))
            if not (xa and xb and b2 == a + 1):
                continue
            ia, ib = mtidx.get(xa), mtidx.get(xb)
            if egymas_utan(xa, xb, tmax) or (ia is not None and ib == ia + 1):
                continue
            if ia is not None and ib == ia + 2 and sorrend and (f, a) in sorrend:
                s = mtlista[ia + 1]
                p = osztas_pont(sorrend[(f, a)], mtd[xa], mtd[s])
                if p is not None:
                    osztas[(f, a)] = (xa, s, p)
                    continue
            allapot[f].append('mt_vers_kimarad: BSB %d:%d->%d:%d, MT %d:%d->%d:%d' % (f, a, f, b2, xa[0], xa[1], xb[0], xb[1]))
    # R4: a cel MT-fejezet TAHOT-maximuma egyezzen a Karoli-kulcs igehely_mt maximumaval (ha a kulcsban van ilyen adat)
    if kk_max:
        for f in sorted(bsb_fej):
            for c2 in sorted({leker[(f, v)][0] for v in bsb_fej[f] if leker.get((f, v))}):
                if c2 in kk_max and tmax.get(c2, 0) != kk_max[c2]:
                    allapot[f].append('kk_max_eltérés: MT %d TAHOT-max %s, Karoli-kulcs igehely_mt max %s' % (c2, tmax.get(c2, 0), kk_max[c2]))
    sorok = []
    for (f, v), b in bs:
        x = leker.get((f, v))
        if allapot[f]:
            sorok.append(((f, v), None, 'illesztetlen', '; '.join(sorted(set(allapot[f])))[:300]))
            continue
        if f in kjv_fejezetek:
            sorok.append(((f, v), None, 'kjv_szamozas', 'tahot_nincs_fejezet_kjv_szamozas_marad'))
            continue
        if x == (f, v) and (f, v) not in osztas:
            modell = 'azonos'
        else:
            modell = 'eltolt'
        if (f, v) in osztas:
            ok = 'versosztas_ketto_mt_vers_strong_illeszkedik'
        elif x not in mtd:
            ok = 'tahot_nincs_vers'
        elif mtd[x] <= b:
            ok = ok_szoveg.get((f, v), 'strong_illeszkedik')
        else:
            ok = 'strong_nem_egyezo'
        sorok.append(((f, v), x, modell, ok))
    return sorok, allapot, tmax, osztas


def egyezes_tetelek(sorok, osztas, bsb_fej, sorrend, mtd):
    """A meres egysegei: [(bsb_(f,v), mt_(f,v), a BSB-oldal Strong-halmaza, az MT-oldal Strong-halmaza vagy None)]. Az illesztetlen es a
    kjv_szamozas versek nincsenek benne; a ket MT-versre osztott BSB-vers ket egyseg (az elso p Strong-sor az elso MT-verssel, a tobbi a masodikkal
    vetve ossze)."""
    ki = []
    for (f, v), x, modell, ok in sorok:
        if modell in ('illesztetlen', 'kjv_szamozas'):
            continue
        if (f, v) in osztas:
            xa, xs, p = osztas[(f, v)]
            seq = sorrend[(f, v)]
            ki.append(((f, v), xa, set(seq[:p]), mtd.get(xa)))
            ki.append(((f, v), xs, set(seq[p:]), mtd.get(xs)))
        else:
            ki.append(((f, v), x, bsb_fej[f][v], mtd.get(x)))
    return ki


def kk_betolt():
    """A Karoli-kulcs sorai: [(igehely_karoli, igehely_kjv, igehely_mt, osztaly)]."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Karoli_versmegfeleltetes.tsv'))
    nevek = ('igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly')
    idx = [fej.index(n) for n in nevek]
    return [tuple(s[i] if len(s) > i else '' for i in idx) for s in sorok]


def kk_max_tabla(kk):
    """{konyv(forras-nev): {MT-fejezet: max vers}} a Karoli-kulcs igehely_mt oszlopabol (csak a `fej:vers` alaku ertekek;
    a KJV-osztaly soraibol nem: ott az igehely_mt ures, es a Karoli-szamozas nem mindig az MT-szamozas)."""
    ki = {}
    for kar, kjv, mt, osz in kk:
        m = re.fullmatch(r'(\d+):(\d+)', mt)
        if not m:
            continue
        d = ki.setdefault(kar.rsplit(' ', 1)[0], {})
        f, v = int(m.group(1)), int(m.group(2))
        d[f] = max(d.get(f, 0), v)
    return ki


FEJLEC_SOR = 'Igehely\tSzósorszám\tStrong-szám\tAngol szó\tMorfológiai kód\tAngol szó állapota\tSzámozás\n'


def konyvek():
    """[(step_kod, magyar, nyelv)] kanonikus sorrendben: a Konyv_normalizalo_tabla 66 sora."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'))
    ki = []
    for i, s in enumerate(sorok):
        ki.append((s[0], s[1], 'H' if i < 39 else 'G'))
    assert len(ki) == 66, len(ki)
    return ki


def forras_halmazok(nyelv, na28=False):
    """{igehely: set(Strong)}. H: TAHOT (F06 fuggvenye); G: TAGNT (Igehely, Strong-szam, ..., Kritikai kiadas)."""
    if nyelv == 'H':
        return kozos.tahot_strongok()
    ki = {}
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'TAGNT_kivonat.tsv'))
    for s in sorok:
        if len(s) < 2 or not s[1].startswith('G'):
            continue
        ki.setdefault(s[0], set())
        if na28 and (len(s) < 8 or 'NA28' not in s[7]):
            continue
        n = kozos.strong_szam(s[1])
        if n is not None:
            ki[s[0]].add(n)
    return ki


def tbesg_normalizalo():
    """{Strong-szam(int): fő Strong-szam(int)} a TBESG.txt ' = a Form/Spelling/Meaning of' soraibol
    (a STEPBible kiterjesztett szamai -> a lemma szama). Csak tajekoztato mutatohoz."""
    ki = {}
    with open(os.path.join(kozos.KONKORDANCIA, 'TBESG.txt'), encoding='utf-8') as f:
        for sor in f:
            mezo = sor.split('	')
            if len(mezo) < 3 or not mezo[0].startswith('G'):
                continue
            if re.search(r' = a (Form|Spelling|Meaning) of$', mezo[1]):
                a, b = kozos.strong_szam(mezo[0]), kozos.strong_szam(mezo[2])
                if a is not None and b is not None and a != b:
                    ki[a] = b
    return ki


def vers_strongok(adat, nyelv):
    """Mint bsb.bsb_vers_strongok, de a nyelvnek megfelelo (H vagy G) Strongokat gyujti."""
    minta = STRONG_MINTA[nyelv]
    ki = {}
    for vs, spanok in adat['eng'].items():
        if not str(vs).isdigit():
            szur('nem_szamjegy_versszam_kulcs (meres)')
            continue
        h = set()
        for span in spanok:
            if isinstance(span, (list, tuple)) and len(span) >= 2 and span[1]:
                for m in minta.finditer(json.dumps(span[1])):
                    h.add(int(m.group(1)))
        ki[int(vs)] = h
    return ki


ALLAPOTOK = ('forditva', 'elhagyva', 'ures_jelzo_nelkul')


def angol_szo_allapot(span):
    """F41.4 (DT6 e): az "Angol szó" allapota egy Strong-hordozo spanra. elhagyva = a forras-span `elided` jelzot hordoz; ures_jelzo_nelkul =
    ures "Angol szó" jelzo nelkul; forditva = az "Angol szó" nem ures (ha elided jelzo es nem ures szoveg egyutt allna, az forditva-nak szamit, de
    kulon szamlalodik: 'elided_jelzo_nem_ures_szoveggel')."""
    jelzo = len(span) > 2 and isinstance(span[2], dict) and bool(span[2].get('elided'))
    ures = not str(span[0]).strip()
    if jelzo and ures:
        return 'elhagyva'
    if jelzo:
        szur('elided_jelzo_nem_ures_szoveggel')
        return 'forditva'
    return 'ures_jelzo_nelkul' if ures else 'forditva'


def vers_sorok(adat, step, fej, eltolas=0, terkep=None):
    """A BSB import sorai egy fejezetbol: (Igehely, Szosorszam, Strong, Angol szo, Morf, Angol szo allapota, Szamozas).
    Minden kihagyott span kategoriankent szamolva (SZURT). eltolas: BSB->MT (regi, k-modell), az Igehely vers-szama v+eltolas.
    terkep (F41): {(fej, vers): (mt_vers, p, mt_vers2, szamozas)}: a BSB-vers Igehelye az mt_vers = (fejezet, vers) (STEP-alakban a cel-fejezettel); ha p nem
    None, a vers elso p Strong-sora az mt_vers, a tobbi az mt_vers2 verse; a Szosorszam az MT-versen belul szamol (a masodik reszben 1-tol); szamozas
    (7. oszlop) = mt / kjv / ellenorizetlen (alapertelmezett: ellenorizetlen).
    Ahol a terkep nem ad bejegyzest, az Igehely a BSB sajat fejezet:verse (+eltolas)."""
    ki = []
    for v in adat['eng']:
        if not str(v).isdigit():
            szur('nem_szamjegy_versszam_kulcs (import)')
    for vs in sorted(int(v) for v in adat['eng'] if str(v).isdigit()):
        poz = 0
        cel1, p_oszt, cel2, szamozas = (fej, vs + eltolas), None, None, 'ellenorizetlen'
        if terkep and (fej, vs) in terkep:
            cel1, p_oszt, cel2, szamozas = terkep[(fej, vs)]
        sorszam = 0
        for span in adat['eng'][str(vs)]:
            if not (isinstance(span, (list, tuple)) and len(span) >= 2):
                szur('hibas_alaku_span')
                continue
            if not span[1]:
                szur('strong_nelkuli_span_szoveggel' if re.search(r'\w', str(span[0])) else 'strong_nelkuli_span_csak_szokoz_irasjel')
                continue
            jel = span[1]
            if not (isinstance(jel, str) and re.fullmatch(r'[HG]\d+[a-z]?', jel)):
                raise ValueError('varatlan Strong-jeloles: %r (%s %s:%s)' % (jel, step, fej, vs))
            sorszam += 1
            cel = cel1
            poz += 1
            if p_oszt is not None and sorszam > p_oszt:
                cel = cel2
                poz = sorszam - p_oszt
            allapot = angol_szo_allapot(span)
            szur('angol_szo_allapot=' + allapot)
            ki.append(('%s.%d.%d' % (step, cel[0], cel[1]), str(poz), jel, span[0], '', allapot, szamozas))
    return ki


def text_only_sorok(cel, kod, fej):
    """A base/text-only (CC0) fejezetfajl nemures sorainak szama = a BSB versszama (fuggetlen teljessegi ellenorzes)."""
    ut = os.path.join(cel, 'base', 'text-only', '%s_%03d_BSB.txt' % (kod, fej))
    if not os.path.exists(ut):
        szur('nincs_text_only_fajl')
        return 0
    with open(ut, encoding='utf-8') as f:
        return sum(1 for sor in f if sor.strip())


def konyv_fejezetek(bmappa, kod):
    return sorted(int(m.group(1)) for fn in os.listdir(bmappa)
                  for m in [re.fullmatch(kod + r'(\d+)\.json', fn)] if m)


def ot_konyv(cel, step, mag, forras, kkmax):
    """Egy ÓSZ-könyv F41-es feldolgozása: BSB-fejezetek beolvasása, versszintű megfeleltetés, mérési egységek, import-sorok.
    Visszaad egy dict-et (a fut és a bsb_verseltolas_diag --f41 közös bemenete)."""
    kod = step.upper()
    bmappa = os.path.join(cel, 'base', 'display', kod)
    if not os.path.isdir(bmappa):
        raise SystemExit('HIBA: nincs BSB-mappa: ' + kod)
    fmag = forras_nev(mag)
    fejezetek = konyv_fejezetek(bmappa, kod)
    bsb_fej, sorrend, adatok = {}, {}, {}
    for f in fejezetek:
        with open(os.path.join(bmappa, '%s%d.json' % (kod, f)), encoding='utf-8') as fh:
            adat = json.load(fh)
        adatok[f] = adat
        bsb_fej[f] = vers_strongok(adat, 'H')
        for v, seq in vers_sorrend(adat).items():
            sorrend[(f, v)] = seq
    sorok, allapot, tmax, osztas = konyv_megfeleltetes(mag, bsb_fej, forras, kkmax.get(fmag), sorrend)
    mtd = dict(mt_versek(forras, fmag)[0])
    tetelek = egyezes_tetelek(sorok, osztas, bsb_fej, sorrend, mtd)
    cel_sorok, terkep = cel_megfeleltetes(mag, step, sorok, osztas, bsb_fej)
    return {'kod': kod, 'fmag': fmag, 'fejezetek': fejezetek, 'bsb_fej': bsb_fej, 'sorrend': sorrend, 'adatok': adatok,
            'sorok': sorok, 'allapot': allapot, 'tmax': tmax, 'osztas': osztas, 'mtd': mtd, 'tetelek': tetelek,
            'cel_sorok': cel_sorok, 'terkep': terkep}


def _vers_szoveg(x):
    return '%d:%d' % x if x else ''


def cel_megfeleltetes(mag, step, sorok, osztas, bsb_fej):
    """Az IMPORT cel-versszamozasa (F41, DT-F41c (a)): a `sorok` (BSB -> TAHOT_kivonat megfeleltetes; a MERES ezt hasznalja) alapjan, a KJV_MARAD / KJV_EGYEZIK_WLC
    kivetelekkel. Visszaad: (cel_sorok, terkep). cel_sorok = [(bsb_(f,v), cel (f:v / f:v+f:v / ures), modell, ok, szamozas, tahot_vers)]; modell: azonos / eltolt /
    illesztetlen / kjv_szamozas; terkep = {bsb_(f,v): (cel_vers, p, cel_vers2, szamozas)} az import Igehelyeihez (az illesztetlen versek nincsenek benne).
    KJV_MARAD: a BSB(KJV)-szam marad, jelolve (kjv_szamozas). KJV_EGYEZIK_WLC: a BSB-szam marad (azonos), a WLC fejezet-max (Macula) egyezeset a szkript ellenorzi:
    elteresnel leall (nincs csendes kozelites); jelolve (kjv_szamozas: a szam a BSB/KJV-e, a WLC-vel azonos)."""
    if mag in KJV_EGYEZIK_WLC:
        wlc_max = wlc_versek.wlc_fejezet_max(wlc_versek.wlc_konyv(wlc_versek.macula_kod(step)))
        for f in sorted(KJV_EGYEZIK_WLC[mag]):
            if wlc_max.get(f) != max(bsb_fej[f]):
                raise SystemExit('HIBA: %s %d: a BSB(KJV) fejezet-max (%s) nem egyezik a WLC-vel (%s): a KJV_EGYEZIK_WLC kivetel nem igazolt'
                                 % (mag, f, max(bsb_fej[f]), wlc_max.get(f)))
    cel_sorok, terkep = [], {}
    wlc = wlc_versek.wlc_konyv(wlc_versek.macula_kod(step))

    def szam(f, v, *cel_versek):
        """7. oszlop: versszintu WLC-osszevetes (a BSB-vers Strong-halmaza vs a cel-vers(ek) WLC-halmaza); osztott versnel mindket cel-versnek egyeznie kell."""
        if cel_versek and all(wlc_versek.vers_egyezik(wlc.get(c, set()), bsb_fej[f][v]) for c in cel_versek):
            return 'mt'
        return 'kjv' if f in KJV_JELOLT_FEJEZETEK.get(mag, ()) else 'ellenorizetlen'

    for (f, v), x, modell, ok in sorok:
        tahot = _vers_szoveg(x)
        if (f, v) in osztas:
            xa, xs, p = osztas[(f, v)]
            tahot = '%d:%d+%d:%d' % (xa + xs)
        if modell == 'illesztetlen':
            cel_sorok.append(((f, v), '', modell, ok, '', ''))
            continue
        if f in KJV_MARAD.get(mag, ()):
            ok2 = ok if modell == 'kjv_szamozas' else 'kjv_szamozas_marad_DT-F41c_a'
            sz = szam(f, v, (f, v))
            cel_sorok.append(((f, v), '%d:%d' % (f, v), 'kjv_szamozas', ok2, sz, tahot))
            terkep[(f, v)] = ((f, v), None, None, sz)
        elif f in KJV_EGYEZIK_WLC.get(mag, ()):
            sz = szam(f, v, (f, v))
            cel_sorok.append(((f, v), '%d:%d' % (f, v), 'azonos', 'bsb_szam_egyezik_wlc_fejezet_max (a TAHOT_kivonat Karoli-szeru)', sz, tahot))
            terkep[(f, v)] = ((f, v), None, None, sz)
        elif (f, v) in osztas:
            xa, xs, p = osztas[(f, v)]
            sz = szam(f, v, xa, xs)
            cel_sorok.append(((f, v), '%d:%d+%d:%d' % (xa + xs), modell, ok, sz, tahot))
            terkep[(f, v)] = (xa, p, xs, sz)
        else:
            sz = szam(f, v, x) if x else 'ellenorizetlen'
            cel_sorok.append(((f, v), _vers_szoveg(x), modell, ok, sz, tahot))
            terkep[(f, v)] = (x, None, None, sz)
    return cel_sorok, terkep


def fut(munka, parancs):
    kuszob, definicio, nevezo = bsb.kuszob_olvas()
    assert definicio == 'tahot_resze_bsb' and nevezo == 'tahot_lefedett_versek'
    cel = os.path.join(munka, 'bsb-data-output')
    commit, hiba = kozos.klonoz(URL, cel)
    if not commit:
        raise SystemExit('HIBA: a BSB nem toltheto le: %s' % hiba)
    halm = {'H': forras_halmazok('H'), 'G': forras_halmazok('G')}
    halm_na28 = forras_halmazok('G', na28=True)
    norm = tbesg_normalizalo()
    kep = lambda halmaz: {norm.get(x, x) for x in halmaz}  # noqa: E731
    kkmax = kk_max_tabla(kk_betolt())
    mappa = os.path.join(cel, 'base', 'display')
    lefedettseg, import_sorok, import_allapot_konyvenkent = [], [], {}
    nem_importalt = []  # minden feldolgozott sor, amely nem kerul a BSB_Strongs.tsv-be (USZ, kuszob alatti konyvek, illesztetlen fejezetek)
    for step, mag, nyelv in konyvek():
        kod = step.upper()
        forras = halm[nyelv]
        if nyelv == 'H':
            k = ot_konyv(cel, step, mag, forras, kkmax)
            fmag, fejezetek, bsb_fej = k['fmag'], k['fejezetek'], k['bsb_fej']
            sorok, allapot, osztas, tetelek = k['sorok'], k['allapot'], k['osztas'], k['tetelek']
            to_db = {f: text_only_sorok(cel, kod, f) for f in fejezetek}
            text_only_versek = sum(to_db.values())
            display_versek = sum(len(bsb_fej[f]) for f in fejezetek)
            # F06-modszer (eltolas nelkul, tajekoztato): minden BSB-vers, a sajat szamaval
            forras_van_nyers = egyezo_nyers = 0
            for f in fejezetek:
                for vs in sorted(bsb_fej[f]):
                    t0 = forras.get('%s %d:%d' % (fmag, f, vs))
                    if t0 is not None:
                        forras_van_nyers += 1
                        egyezo_nyers += 1 if t0 <= bsb_fej[f][vs] else 0
            forras_van = sum(1 for t in tetelek if t[3] is not None)
            egyezo = sum(1 for t in tetelek if t[3] is not None and t[3] <= t[2])
            kjv_db = sum(1 for s in sorok if s[2] == 'kjv_szamozas')
            bsb_versek = len(tetelek) + kjv_db
            bsb_ref = {'%s %d:%d' % (fmag, t[1][0], t[1][1]) for t in tetelek}
            forras_versek = {r for r in forras if r.rsplit(' ', 1)[0] == fmag}
            forras_bsb_nelkul = len(forras_versek - bsb_ref)
            eltolt_fejezet = len({c[0][0] for c in k['cel_sorok'] if c[2] == 'eltolt'})
            illesztetlen = {f: ok[0] for f, ok in allapot.items() if ok}
            kjv_fejezetek = sorted({c[0][0] for c in k['cel_sorok'] if c[4] == 'kjv'})  # fejezetek, ahol van `kjv` szamozasu vers
            # N-F41c: konyvnev-alias vagy hibas megfeleltetes miatti nema nulla -> hangos hiba (nincs csendes kihagyas)
            illesztett_db = sum(1 for s in sorok if s[2] in ('azonos', 'eltolt'))
            if illesztett_db == 0 or forras_van == 0 or egyezo == 0:
                raise SystemExit('HIBA (N-F41c): %s: 0 illesztett sor / 0 egyezo vers (illesztett=%d, forras_van=%d, egyezo=%d) -- konyvnev-alias vagy '
                                 'hibas megfeleltetes; a szkript nem hagy ki nema konyvet' % (mag, illesztett_db, forras_van, egyezo))
            terkep = k['terkep']
            konyv_sorok = []
            for f in fejezetek:
                sorok_f = vers_sorok(k['adatok'][f], step, f, 0, terkep)  # a szurt-szamlalok minden fejezetre futnak
                if f not in illesztetlen:
                    konyv_sorok += sorok_f
                else:
                    nem_importalt += sorok_f
        else:
            bmappa = os.path.join(mappa, kod)
            if not os.path.isdir(bmappa):
                raise SystemExit('HIBA: nincs BSB-mappa: ' + kod)
            fmag = mag
            fejezetek = konyv_fejezetek(bmappa, kod)
            bsb_versek = forras_van = egyezo = egyezo_na28 = egyezo_norm = 0
            forras_van_nyers = egyezo_nyers = 0
            text_only_versek = display_versek = 0
            bsb_ref = set()
            konyv_sorok = []
            to_db = {f: text_only_sorok(cel, kod, f) for f in fejezetek}
            illesztetlen, kjv_fejezetek, eltolt_fejezet = {}, [], 0
            for f in fejezetek:
                with open(os.path.join(bmappa, '%s%d.json' % (kod, f)), encoding='utf-8') as fh:
                    adat = json.load(fh)
                b = vers_strongok(adat, nyelv)
                text_only_versek += to_db[f]
                display_versek += len(b)
                nem_importalt += vers_sorok(adat, step, f)  # az USZ nem importalt (a szurt-szamlalokhoz es az allapot-ellenorzeshez)
                for vs in sorted(b):
                    ref = '%s %d:%d' % (mag, f, vs)
                    t = forras.get(ref)
                    bsb_versek += 1
                    bsb_ref.add(ref)
                    if t is None:
                        continue
                    forras_van_nyers += 1
                    egyezo_nyers += 1 if t <= b[vs] else 0
                    forras_van += 1
                    if t <= b[vs]:
                        egyezo += 1
                    if kep(t) <= kep(b[vs]):
                        egyezo_norm += 1
                    if halm_na28.get(ref, set()) <= b[vs]:
                        egyezo_na28 += 1
            forras_versek = {r for r in forras if r.rsplit(' ', 1)[0] == mag}
            forras_bsb_nelkul = len(forras_versek - bsb_ref)
        szaz = 100.0 * egyezo / forras_van if forras_van else 0.0
        eredmeny = 'ELERI' if szaz >= kuszob else 'NEM_ERI_EL'
        if nyelv == 'G':
            eredmeny = 'USZ_KIHAGYVA'  # szandekos: az USZ gorog reteg forrasa a Macula (#87); a mert szazalek tajekoztato
        szaz_nyers = 100.0 * egyezo_nyers / forras_van_nyers if forras_van_nyers else 0.0
        lefedettseg.append((mag, kod, 'heber' if nyelv == 'H' else 'gorog',
                            str(bsb_versek), str(forras_van), str(egyezo),
                            str(bsb_versek - forras_van), str(forras_bsb_nelkul), str(text_only_versek),
                            str(text_only_versek - display_versek),
                            '%.2f' % szaz, '%.2f' % szaz_nyers, str(eltolt_fejezet),
                            ('%.2f' % (100.0 * egyezo_na28 / forras_van)) if nyelv == 'G' and forras_van else '',
                            ('%.2f' % (100.0 * egyezo_norm / forras_van)) if nyelv == 'G' and forras_van else '',
                            '%g' % kuszob, eredmeny,
                            str(len(konyv_sorok)) if eredmeny == 'ELERI' else '0',
                            ' '.join(str(x) for x in sorted(illesztetlen)) or '-',
                            ' '.join(str(x) for x in kjv_fejezetek) or '-'))
        if eredmeny != 'ELERI':
            nem_importalt += konyv_sorok
        if eredmeny == 'ELERI':
            assert nyelv == 'H'
            import_sorok += konyv_sorok
            import_allapot_konyvenkent[mag] = konyv_sorok
    ered_db = sum(1 for s in lefedettseg if s[16] == 'ELERI')
    alatta_db = sum(1 for s in lefedettseg if s[16] == 'NEM_ERI_EL')
    usz_db = sum(1 for s in lefedettseg if s[16] == 'USZ_KIHAGYVA')
    # a konyvek: a 0-sorszamu ELERI-konyv is hiba lenne (N-F41c)
    for s in lefedettseg:
        if s[16] == 'ELERI' and s[17] == '0':
            raise SystemExit('HIBA (N-F41c): %s ELERI, de 0 importalt sor' % s[0])
    fej = kozos.fejlec(URL + ' + konkordancia/TAHOT_kivonat.tsv (OSZ) + konkordancia/TAGNT_kivonat.tsv (USZ) + konkordancia/Karoli_versmegfeleltetes.tsv (igehely_mt, ellenorzes)',
                       'BSB commit ' + commit, parancs)
    allapot_szamlalo = {a: sum(1 for s in import_sorok if s[5] == a) for a in ALLAPOTOK}
    nem_imp_szamlalo = {a: sum(1 for s in nem_importalt if s[5] == a) for a in ALLAPOTOK}
    szamozas_szamlalo = {a: sum(1 for s in import_sorok if s[6] == a) for a in SZAMOZASOK}
    # a szurt-szamlalok (MIND A 66 KONYVRE) = importalt + nem importalt sorok: a ket hatokor osszevetese (F41 ellenori 5. eltereses)
    for a in ALLAPOTOK:
        if SZURT['angol_szo_allapot=' + a] != allapot_szamlalo[a] + nem_imp_szamlalo[a]:
            raise SystemExit('HIBA (F41.4): angol_szo_allapot=%s: szurt %d != importalt %d + nem importalt %d'
                             % (a, SZURT['angol_szo_allapot=' + a], allapot_szamlalo[a], nem_imp_szamlalo[a]))
    fej += ['rogzitett kuszob=%g%% definicio=%s nevezo=%s (kuszob.txt, F06-ban meres elott rogzitve); konyvenkenti alkalmazas: FELADATOK D15' % (kuszob, definicio, nevezo),
            'licenc: base/display/ CC0 1.0 (README.md, ATTRIBUTION.md); a CC-BY index-cc-by/ nem importalt',
            'nincs_forras_vers = a BSB-meresi egysegek (BSB-vers; a ket MT-versre osztott BSB-vers ket egyseg) es a kjv_szamozasu versek szama, amelyekhez a TAHOT/TAGNT-nak nincs sora (nem elteres, nem szamit a nevezobe); forras_vers_nincs_bsb = a forras verseinek szama, amelyek igehelye nem kapott BSB-verset (megfeleltetes utan; verszamozas-elteres vagy illesztetlen fejezet jele)',
            'egyezes_na28_szurve: csak USZ; a TAGNT-nak csak a NA28-cimkes soraival szamolt egyezes, ugyanazzal a nevezovel (tajekoztato, nem a kuszob alapja)',
            'egyezes_normalizalt: csak USZ; mindket oldal Strong-szamai a TBESG.txt Form/Spelling/Meaning of soraival a lemma szamara kepezve (%d szam); tajekoztato, nem a kuszob alapja' % len(norm),
            'ELTERES AZ F06-MODSZERTOL: az F06 (bsb.py) csak az 1Mozest merte, TAHOT-tal; a 27 ujszovetsegi konyvre a forras a TAGNT (G-Strongok) -- ez uj, az F06-ban nem mert alkalmazas, a kuszob es az egyezes-definicio valtozatlan',
            'text_only_versek = a base/text-only (CC0) nemures sorai; display_hianyzo_versek = text_only_versek - display-versek: az upstream display-JSON-bol hianyzo versek (masodlagos, fuggetlen ellenorzes)',
            'szurt sorok kategoriankent (MIND A 66 KONYVRE, az importalt es a nem importalt konyvekre egyarant; a nem_szamjegy_versszam_kulcs kulcsok 0 ertekkel is szerepelnek; az angol_szo_allapot=* nem szurt: az adatsorban bent van, a 6. oszlop jelzi; elhagyva = a forras-span elided jelzot hordoz, ures_jelzo_nelkul = ures Angol szo jelzo nelkul): ' + '; '.join('%s=%d' % kv for kv in sorted(SZURT.items())),
            'angol_szo_allapot az IMPORTALT sorokban (BSB_Strongs.tsv 6. oszlopa): ' + '; '.join('%s=%d' % kv for kv in sorted(allapot_szamlalo.items())),
            'HATOKOR (F41 ellenori 5.): a fenti "szurt sorok" angol_szo_allapot=* szamlaloi MIND A 66 KONYV minden feldolgozott sorara vonatkoznak; az importalt-sorok szamlaloi csak a BSB_Strongs.tsv-be kerulo sorokra; a kulonbseg a nem importalt sorok (USZ, kuszob alatti konyvek, illesztetlen fejezetek): ' + '; '.join('%s=%d' % kv for kv in sorted(nem_imp_szamlalo.items())) + ' -- a szkript ellenorzi: szurt = importalt + nem importalt, mindharom allapotra',
            'Számozás az IMPORTALT sorokban (BSB_Strongs.tsv 7. oszlopa, VERSSZINTU WLC-osszevetesbol, DT-F41f): ' + '; '.join('%s=%d' % kv for kv in sorted(szamozas_szamlalo.items())) + ' -- mt = az Igehely-vers sorainak Strong-halmaza tartalmazza a WLC (Macula) azonos szamu versenek halmazanak tobb mint felet (igazolt MT-szam); kjv = nem igazolt, a BSB(KJV)-szam marad (csak Job 38-41; a Job MT-re szamozasa: N-F41g); ellenorizetlen = nem igazolt (a TAHOT_kivonat hibrid szamozasu, vagy a WLC-ben nincs ilyen vers; MT-re szamozasa: N-F41h); fejezetenkenti kimutatas: naplok/F41_wlc_versszam_ellenorzes.tsv',
            'egyezes_szazalek_eltolas_nelkul = a F06-modszer (a BSB-vers szama valtoztatas nelkul, a TAHOT-vers ugyanazzal a szammal; a konyvnev a forras-nev, JSir -> Sir), tajekoztato; egyezes_szazalek = a kuszob alapja: a BSB-vers -> MT-vers (TAHOT_kivonat-szamozas) versszintu megfeleltetessel (F41; naplok/F41_bsb_megfeleltetes.tsv); mt_eltolt_fejezetek = a BSB-fejezetek szama, amelyekben van eltolt (mas fejezet:vers) vers; illesztetlen_fejezetek = a fejezetek, ahol a megfeleltetes nem igazolhato (kimaradnak a merestol, a versszamlalobol es az importbol); kjv_szamozasu_fejezetek = a BSB-fejezetek, amelyekben van `kjv` Számozású sor (BSB_Strongs.tsv 7. oszlop): a Job 38-41 (DT-F41c (a); a Job 41 a TAHOT_kivonatban nincs, a mereshez nem szamit); a Job 38-40 versei a MERESBEN a TAHOT_kivonathoz illesztve szerepelnek (a merés nem azonos az Igehely-szamozassal); a Pred 11/12, Ezs 2/3, 4Moz 12/13 az Igehely a BSB(KJV)-szam (= WLC), a 7. oszlop versenkent mt/ellenorizetlen',
            'konyvek: %d ELERI (mind OSZ), %d NEM_ERI_EL (OSZ), %d USZ_KIHAGYVA (az USZ szandekosan kimarad: a gorog reteg forrasa a Macula #87; a mert szazalek tajekoztato); importalt sorok: %d' % (ered_db, alatta_db, usz_db, len(import_sorok))]
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'), fej,
                 ['konyv', 'bsb_kod', 'nyelv', 'versek_bsb', 'forras_lefedett_versek', 'egyezo', 'nincs_forras_vers',
                  'forras_vers_nincs_bsb', 'text_only_versek', 'display_hianyzo_versek', 'egyezes_szazalek', 'egyezes_szazalek_eltolas_nelkul', 'mt_eltolt_fejezetek', 'egyezes_na28_szurve', 'egyezes_normalizalt', 'kuszob', 'eredmeny', 'importalt_sorok', 'illesztetlen_fejezetek', 'kjv_szamozasu_fejezetek'],
                 lefedettseg)
    # BSB_Strongs.tsv: nagy fajl (a kozos.tsv_ir 1 MB-os korlatja a naplokra vonatkozik); csv nelkul
    ut = os.path.join(kozos.KONKORDANCIA, 'BSB_Strongs.tsv')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FEJLEC_SOR)
        for s in import_sorok:
            f.write('\t'.join(kozos.tisztit(x) for x in s) + '\n')
    allapot_ellenorzes(ut, import_sorok, allapot_szamlalo, szamozas_szamlalo)
    for s in lefedettseg:
        print('\t'.join(s))
    print(fej[-1])
    print(fej[-2])


def allapot_ellenorzes(ut, import_sorok, allapot_szamlalo, szamozas_szamlalo):
    """F41.4 gepi ellenorzes: a kiirt BSB_Strongs.tsv-t visszaolvasva (split('\\t'), csv nelkul) ures "Angol szó" csak elhagyva / ures_jelzo_nelkul allapottal
    fordulhat elo; minden sor 7 oszlopos, az allapot es a Szamozas ervenyes; a darabszamok egyeznek a memoriabeli (naplobeli) szamlalokkal; az ures_jelzo_nelkul db
    ki van irva (varhato 0)."""
    db = {a: 0 for a in ALLAPOTOK}
    szdb = {a: 0 for a in SZAMOZASOK}
    sorok = 0
    with open(ut, encoding='utf-8') as f:
        fejsor = f.readline().rstrip('\n').split('\t')
        assert fejsor == FEJLEC_SOR.rstrip('\n').split('\t'), fejsor
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if len(m) != 7:
                raise SystemExit('HIBA (F41.4): nem 7 oszlopos sor: %r' % sor)
            sorok += 1
            if m[6] not in SZAMOZASOK:
                raise SystemExit('HIBA (F41.4): ervenytelen Szamozas: %r' % sor)
            szdb[m[6]] += 1
            if m[5] not in ALLAPOTOK:
                raise SystemExit('HIBA (F41.4): ervenytelen allapot: %r' % sor)
            if m[3] == '' and m[5] == 'forditva':
                raise SystemExit('HIBA (F41.4): ures Angol szo "forditva" allapottal: %r' % sor)
            if m[3] != '' and m[5] != 'forditva':
                raise SystemExit('HIBA (F41.4): nem ures Angol szo nem "forditva" allapottal: %r' % sor)
            db[m[5]] += 1
    if sorok != len(import_sorok) or db != allapot_szamlalo or szdb != szamozas_szamlalo:
        raise SystemExit('HIBA (F41.4): a visszaolvasott darabszamok nem egyeznek: %s / %s (sorok %d / %d)' % (db, allapot_szamlalo, sorok, len(import_sorok)))
    print('F41.4 allapot-ellenorzes OK: %d sor; %s; %s' % (sorok, ', '.join('%s=%d' % kv for kv in sorted(db.items())), ', '.join('%s=%d' % kv for kv in sorted(szdb.items()))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--munka', required=True, help='mappa, amelyben a bsb-data-output/ klon van (vagy ide klonozodik)')
    a = ap.parse_args()
    fut(a.munka, 'python eszkozok/fj2/bsb_import.py --munka <mappa>')


if __name__ == '__main__':
    main()
