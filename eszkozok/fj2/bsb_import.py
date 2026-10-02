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

URL = bsb.URL
STRONG_MINTA = {'H': re.compile(r'H0*(\d+)'), 'G': re.compile(r'G0*(\d+)')}
SZURT = {'nem_szamjegy_versszam_kulcs (meres)': 0, 'nem_szamjegy_versszam_kulcs (import)': 0}  # kategoria -> darab: minden, ami a mereshez/importhoz nem kerul be, itt szamolodik


def szur(kat, n=1):
    SZURT[kat] = SZURT.get(kat, 0) + n


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


def konyv_megfeleltetes(mag, bsb_fej, forras, kk_max=None):
    """Egy konyv versszintu megfeleltetese. bsb_fej: {fejezet: {vers: set(Strong)}} (a display-JSON).
    Visszaad: (sorok, fejezet_allapot, tmax) ahol
      sorok = [(bsb_(f,v), mt_(f,v) vagy None, modell, ok)]  (modell: azonos / eltolt / illesztetlen),
      fejezet_allapot = {bsb_fejezet: [okok]} (ures lista = igazolt; nem ures = a fejezet illesztetlen),
      tmax = {mt_fejezet: max vers}.
    A fejezet illesztetlen, ha (R1) egy verse nem illesztheto es a szomszedaibol sem tolthetõ ki, (R2) egy vers a
    megfeleltetett MT-versre nem illeszkedik, de a szomszedos MT-versre igen (belso versosztas-eltereses, F16.11), (R3) egymas utani BSB-versek nem egymas utani MT-versekre
    kerulnek (kimaradt MT-vers), (R4) a cel MT-fejezet TAHOT-maximuma nem egyezik a Karoli-kulcs igehely_mt maximumaval."""
    fmag = forras_nev(mag)
    bs = [((f, v), bsb_fej[f][v]) for f in sorted(bsb_fej) for v in sorted(bsb_fej[f])]
    mt, tmax = mt_versek(forras, fmag)
    mtd = dict(mt)
    mtlista = [r for r, _ in mt]
    mtidx = {r: i for i, r in enumerate(mtlista)}
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
    for f, vl in nincs_part.items():
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

    # R3: egymas utani BSB-versek egymas utani MT-versek
    for f in sorted(bsb_fej):
        versek = sorted(bsb_fej[f])
        for a, b2 in zip(versek, versek[1:]):
            xa, xb = leker.get((f, a)), leker.get((f, b2))
            if xa and xb and b2 == a + 1 and not egymas_utan(xa, xb, tmax):
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
        if x == (f, v):
            modell = 'azonos'
        else:
            modell = 'eltolt'
        if x not in mtd:
            ok = 'tahot_nincs_vers'
        elif mtd[x] <= b:
            ok = ok_szoveg.get((f, v), 'strong_illeszkedik')
        else:
            ok = 'strong_nem_egyezo'
        sorok.append(((f, v), x, modell, ok))
    return sorok, allapot, tmax


FEJLEC_SOR = 'Igehely\tSzósorszám\tStrong-szám\tAngol szó\tMorfológiai kód\n'


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


def vers_sorok(adat, step, fej, eltolas=0):
    """A BSB import sorai egy fejezetbol: (Igehely, Szosorszam, Strong, Angol szo, Morf).
    Minden kihagyott span kategoriankent szamolva (SZURT). eltolas: BSB->MT (Zsolt), az Igehely vers-szama v+eltolas."""
    ki = []
    for v in adat['eng']:
        if not str(v).isdigit():
            szur('nem_szamjegy_versszam_kulcs (import)')
    for vs in sorted(int(v) for v in adat['eng'] if str(v).isdigit()):
        poz = 0
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
            poz += 1
            if len(span) > 2 and isinstance(span[2], dict) and span[2].get('elided'):
                szur('elided_span_bent_ures_Angol_szo_jeloles_nelkul')
            ki.append(('%s.%d.%d' % (step, fej, vs + eltolas), str(poz), jel, span[0], ''))
    return ki


def text_only_sorok(cel, kod, fej):
    """A base/text-only (CC0) fejezetfajl nemures sorainak szama = a BSB versszama (fuggetlen teljessegi ellenorzes)."""
    ut = os.path.join(cel, 'base', 'text-only', '%s_%03d_BSB.txt' % (kod, fej))
    if not os.path.exists(ut):
        szur('nincs_text_only_fajl')
        return 0
    with open(ut, encoding='utf-8') as f:
        return sum(1 for sor in f if sor.strip())


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
    mappa = os.path.join(cel, 'base', 'display')
    lefedettseg, import_sorok, zsolt_sorok, nem_egyezo = [], [], [], []
    for step, mag, nyelv in konyvek():
        kod = step.upper()
        bmappa = os.path.join(mappa, kod)
        if not os.path.isdir(bmappa):
            raise SystemExit('HIBA: nincs BSB-mappa: ' + kod)
        fejezetek = sorted(int(m.group(1)) for fn in os.listdir(bmappa)
                           for m in [re.fullmatch(kod + r'(\d+)\.json', fn)] if m)
        forras = halm[nyelv]
        bsb_versek = forras_van = egyezo = egyezo_na28 = egyezo_norm = 0
        forras_van_nyers = egyezo_nyers = 0  # F06-modszer: eltolas nelkul (tajekoztato)
        text_only_versek = display_versek = 0
        bsb_ref = set()
        konyv_sorok = []
        to_db = {fej: text_only_sorok(cel, kod, fej) for fej in fejezetek}
        elt = {}
        if mag in MT_ELTOLASOS_KONYVEK:
            tmax = {}
            for r in forras:
                m = re.fullmatch(re.escape(mag) + r' (\d+):(\d+)', r)
                if m:
                    tmax[int(m.group(1))] = max(tmax.get(int(m.group(1)), 0), int(m.group(2)))
            elt = fejezet_eltolasok(mag, fejezetek, to_db, tmax)
        eltolt_fejezet = sum(1 for k in elt.values() if k)
        illesztetlen = {}  # fejezet -> okok: a k-modell nem igazolhato, a fejezet kimarad a merestol es az importbol
        for fej in fejezetek:
            with open(os.path.join(bmappa, '%s%d.json' % (kod, fej)), encoding='utf-8') as f:
                adat = json.load(f)
            b = vers_strongok(adat, nyelv)
            k = elt.get(fej, 0)
            text_only_versek += to_db[fej]
            display_versek += len(b)
            fej_sorok = vers_sorok(adat, step, fej, k)
            okok = belso_osztas_eltereses(b, forras, mag, fej, k) if mag in MT_ELTOLASOS_KONYVEK else []
            if okok:
                illesztetlen[fej] = okok
            else:
                konyv_sorok += fej_sorok
            if mag in MT_ELTOLASOS_KONYVEK:
                d_cim = any(h.get('level') == 'd' and not re.fullmatch(r'Psalms \d+.\d+', h.get('text', ''))
                            for sv in adat.get('structure', {}).values() for h in sv.get('headings', []))  # a 'Psalms 1-41' stb. konyv-cim nem felirat
                zsolt_sorok.append((str(fej), str(to_db[fej]), str(len(b)), 'igen' if 1 in b else 'nem',
                                    'igen' if d_cim else 'nem', str(kk_mt_max(mag).get(fej, '')),
                                    str(tmax.get(fej, 0)), str(k),
                                    'illesztetlen' if okok else 'illesztett', '; '.join(sorted(set(okok)))))
            for vs in sorted(b):
                t0 = forras.get('%s %d:%d' % (mag, fej, vs))
                if t0 is not None:
                    forras_van_nyers += 1
                    if t0 <= b[vs]:
                        egyezo_nyers += 1
                if fej in illesztetlen:
                    continue  # nem igazolhato kotes: nincs a merestol, nincs a bsb_ref-ben, nincs importalva
                bsb_versek += 1
                ref = '%s %d:%d' % (mag, fej, vs + k)
                bsb_ref.add(ref)
                t = forras.get(ref)
                if t is None:
                    continue
                forras_van += 1
                if t <= b[vs]:
                    egyezo += 1
                elif mag in MT_ELTOLASOS_KONYVEK:
                    nem_egyezo.append((str(fej), str(vs), str(vs + k), str(len(t)), str(len(b[vs])),
                                       ' '.join('H%d' % x for x in sorted(t - b[vs])),
                                       ' '.join('H%d' % x for x in sorted(b[vs] - t))))
                if nyelv == 'G' and kep(t) <= kep(b[vs]):
                    egyezo_norm += 1
                if nyelv == 'G' and halm_na28.get(ref, set()) <= b[vs]:
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
                            ' '.join(str(f) for f in sorted(illesztetlen)) or '-'))
        if eredmeny == 'ELERI':
            assert nyelv == 'H'
            import_sorok += konyv_sorok
    ered_db = sum(1 for s in lefedettseg if s[16] == 'ELERI')
    alatta_db = sum(1 for s in lefedettseg if s[16] == 'NEM_ERI_EL')
    usz_db = sum(1 for s in lefedettseg if s[16] == 'USZ_KIHAGYVA')
    fej = kozos.fejlec(URL + ' + konkordancia/TAHOT_kivonat.tsv (OSZ) + konkordancia/TAGNT_kivonat.tsv (USZ)',
                       'BSB commit ' + commit, parancs)
    fej += ['rogzitett kuszob=%g%% definicio=%s nevezo=%s (kuszob.txt, F06-ban meres elott rogzitve); konyvenkenti alkalmazas: FELADATOK D15' % (kuszob, definicio, nevezo),
            'licenc: base/display/ CC0 1.0 (README.md, ATTRIBUTION.md); a CC-BY index-cc-by/ nem importalt',
            'nincs_forras_vers = a BSB-versek szama, amelyekhez a TAHOT/TAGNT-nak nincs sora (nem elteres, nem szamit a nevezobe); forras_vers_nincs_bsb = a forras verseinek szama, amelyek igehelye a BSB-ben nincs meg (verszamozas-elteres jele)',
            'egyezes_na28_szurve: csak USZ; a TAGNT-nak csak a NA28-cimkes soraival szamolt egyezes, ugyanazzal a nevezovel (tajekoztato, nem a kuszob alapja)',
            'egyezes_normalizalt: csak USZ; mindket oldal Strong-szamai a TBESG.txt Form/Spelling/Meaning of soraival a lemma szamara kepezve (%d szam); tajekoztato, nem a kuszob alapja' % len(norm),
            'ELTERES AZ F06-MODSZERTOL: az F06 (bsb.py) csak az 1Mozest merte, TAHOT-tal; a 27 ujszovetsegi konyvre a forras a TAGNT (G-Strongok) -- ez uj, az F06-ban nem mert alkalmazas, a kuszob es az egyezes-definicio valtozatlan',
            'text_only_versek = a base/text-only (CC0) nemures sorai; display_hianyzo_versek = text_only_versek - display-versek: az upstream display-JSON-bol hianyzo versek (masodlagos, fuggetlen ellenorzes)',
            'szurt sorok kategoriankent (MIND A 66 KONYVRE, az importalt es a nem importalt konyvekre egyarant; a nem_szamjegy_versszam_kulcs kulcsok 0 ertekkel is szerepelnek; az elided_span_* nem szurt: az adatsorban bent van, ures Angol szo-val, jeloles nelkul): ' + '; '.join('%s=%d' % kv for kv in sorted(SZURT.items())),
            'egyezes_szazalek_eltolas_nelkul = a F06-modszer (a BSB-vers szama valtoztatas nelkul, a TAHOT-vers ugyanazzal a szammal); egyezes_szazalek = a kuszob alapja: a Zsoltaroknal a BSB-vers -> MT-vers megfeleltetessel (F16.8; k = Karoli-kulcs igehely_mt fejezet-max - BSB versszam), minden mas konyvre azonos az eltolas nelkulivel; mt_eltolt_fejezetek = a k>0 fejezetek szama; illesztetlen_fejezetek = a Zsoltar-fejezetek, ahol a fejezetenkent allando k-modell belso versosztas-eltereses miatt nem igazolhato (javaslat: a fejezet kimarad a merestol, a versszamlalobol es az importbol; l. naplok/F16_bsb_zsolt_megfeleltetes.tsv)',
            'konyvek: %d ELERI (mind OSZ), %d NEM_ERI_EL (OSZ), %d USZ_KIHAGYVA (az USZ szandekosan kimarad: a gorog reteg forrasa a Macula #87; a mert szazalek tajekoztato); importalt sorok: %d' % (ered_db, alatta_db, usz_db, len(import_sorok))]
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'), fej,
                 ['konyv', 'bsb_kod', 'nyelv', 'versek_bsb', 'forras_lefedett_versek', 'egyezo', 'nincs_forras_vers',
                  'forras_vers_nincs_bsb', 'text_only_versek', 'display_hianyzo_versek', 'egyezes_szazalek', 'egyezes_szazalek_eltolas_nelkul', 'mt_eltolt_fejezetek', 'egyezes_na28_szurve', 'egyezes_normalizalt', 'kuszob', 'eredmeny', 'importalt_sorok', 'illesztetlen_fejezetek'],
                 lefedettseg)
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_bsb_zsolt_megfeleltetes.tsv'),
                 kozos.fejlec(URL + ' + konkordancia/Karoli_versmegfeleltetes.tsv (igehely_mt) + konkordancia/TAHOT_kivonat.tsv',
                              'BSB commit ' + commit, parancs)
                 + ['zsoltaronkenti BSB-vers -> MT-vers megfeleltetes (F16.8): bsb_versszam = base/text-only sorai (a BSB/KJV-szamozas); display_versek = a display-JSON versszama; '
                    'display_elso_vers = van-e az 1. vers a display-JSON-ban; bsb_d_cim = van-e "d" szintu (leiro cim, felirat) heading a fejezet structure-jeben (a "Psalms 1-41" tipusu konyvcimek nelkul); '
                    'kk_mt_max = a Karoli-kulcs igehely_mt oszlopabol az MT-fejezet utolso versszama (ures: a kulcsban nincs igehely_mt, KJV-osztaly, azonos szamozas, k=0); tahot_max = a TAHOT_kivonat fejezet-maxa (ellenorzes: egyezik); '
                    'k = kk_mt_max - bsb_versszam: a BSB-vers v az MT-vers v+k (k>0: az MT a feliratot sajat versszamon szamozza); allapot = illesztetlen, ha a fejezetenkent allando k belso versosztas-eltereses miatt nem igazolhato (l. belso_osztas_eltereses a szkriptben): a fejezet nincs a meresben es az importban'],
                 ['zsoltar', 'bsb_versszam', 'display_versek', 'display_elso_vers', 'bsb_d_cim', 'kk_mt_max', 'tahot_max', 'k', 'allapot', 'illesztetlen_ok'],
                 zsolt_sorok)
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_zsolt_nem_egyezo_versek.tsv'),
                 kozos.fejlec(URL + ' + konkordancia/TAHOT_kivonat.tsv', 'BSB commit ' + commit, parancs)
                 + ['a Zsoltar-meres (egyezes_szazalek) nevezojebe eso, de NEM egyezo versek (a TAHOT-Strong-halmaz nem resze a BSB-versnek); az illesztetlen fejezetek (Zsolt 13) nincsenek benne',
                    'tahot_strong_szam/bsb_strong_szam = a halmazok merete; tahot_nincs_bsbben = a TAHOT-nak azok a Strongjai, amelyek a BSB-versben nincsenek (ez okozza a nem-egyezest); bsb_tobblet = a BSB-vers Strongjai, amelyek a TAHOT-versben nincsenek (tajekoztato)'],
                 ['zsoltar', 'bsb_vers', 'mt_vers', 'tahot_strong_szam', 'bsb_strong_szam', 'tahot_nincs_bsbben', 'bsb_tobblet'],
                 nem_egyezo)
    # BSB_Strongs.tsv: nagy fajl (a kozos.tsv_ir 1 MB-os korlatja a naplokra vonatkozik); csv nelkul
    ut = os.path.join(kozos.KONKORDANCIA, 'BSB_Strongs.tsv')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FEJLEC_SOR)
        for s in import_sorok:
            f.write('\t'.join(kozos.tisztit(x) for x in s) + '\n')
    for s in lefedettseg:
        print('\t'.join(s))
    print(fej[-1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--munka', required=True, help='mappa, amelyben a bsb-data-output/ klon van (vagy ide klonozodik)')
    a = ap.parse_args()
    fut(a.munka, 'python eszkozok/fj2/bsb_import.py --munka <mappa>')


if __name__ == '__main__':
    main()
