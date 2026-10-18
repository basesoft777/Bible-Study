"""F117 (VERSMEGF_JAVITAS) 4.2: versenkénti Károli 1908 ↔ KJV szöveg-összevetés, a versmegfeleltető tábla nélkül.

A `konkordancia/Karoli_versmegfeleltetes.tsv`-t SZÁNDÉKOSAN nem olvassa: a referencia a tábla hibáinak mérésére
készül (F117 brief 5. szakasz, nem körkörös mérés).

Bemenet:
  * konkordancia/Karoli_1908.tsv          (Károli-szöveg, Károli-kulcs)
  * konkordancia/KJV_Strongs_teljes.tsv   (KJV, STEPBible-kulcs; csak a Strong-címkézett angol szavak)
  * konkordancia/TAHOT_kivonat.tsv        (Károli-kulcsú héber Strong-halmaz; KIEGÉSZÍTŐ jel, l. lent)
  * konkordancia/Konyv_normalizalo_tabla.tsv, adat/grammatikai_strongok.tsv

Módszer: egy Károli-fejezet verssorát monoton igazítással (dinamikus programozás) illeszti a KJV ugyanazon könyvének
c-1, c, c+1 fejezetéből álló ablakára; az ablak elején és végén a KJV-versek kihagyása ingyenes. Lépések: 1-1 pár;
1 Károli = 2 KJV (Károli-összevonás); 2 Károli = 1 KJV; Károli-vers pár nélkül; KJV-vers kihagyva (büntetéssel).

Jelek egy (Károli-vers, KJV-vers) párra:
  nev    tulajdonnevek (és az Úr/Isten ↔ LORD/God) egyezése, durva hangalaki kulccsal; [0..1], mindkét oldal üres: 0,5
  szam   számnevek halmazának egyezése; mindkét oldal üres: 0,5
  hossz  a szószám-arány az ablak mediánjához mérve, exp(-|ln r|); [0..1]
  elso_utolso  az első és az utolsó horgony (név vagy szám) egyezése: 0, 1 vagy 2; '-' ha nincs horgony
  tahot  a TAHOT (Károli-kulcs) és a KJV Strong-halmazának Jaccard-értéke a grammatikai Strongok nélkül.
         FIGYELEM: a TAHOT F85-ös átkulcsolása a versmegfeleltető táblát egyik tanúként használta
         (eszkozok/tahot_verskulcs_finomit.py), ezért ez a jel NEM független; két igazítás fut:
         'szoveg' (nev+szam+hossz) és 'teljes' (szoveg + tahot). Elfogadott párhoz a szöveg-igazítás egyezése kell.

Kimenet (--kimenet, alapérték: naplok/F117_szoveg_osszevetes.tsv): soronként egy Károli-vers, a két igazítás
javasolt KJV-verse, a jelek, a döntési ok, és ha az --itelet fájl megvan, a kézi (modell-) ítélet és az eltérés jele.

Használat:
  python eszkozok/versmegf_szoveg_osszevet.py --minta              # Hós 14, Én 6, Dán 3, Jón 2 (a 4.2 kis mintája)
  python eszkozok/versmegf_szoveg_osszevet.py --fejezet "Hós 13" --fejezet "Hós 14" [--kimenet ...] [--itelet ...]
  python eszkozok/versmegf_szoveg_osszevet.py --minta --szoveg     # a két szöveg kiírása (olvasáshoz), nem ír fájlt

TSV-olvasás split('\\t')-tel, írás '\\t'.join()-nal (CLAUDE.md), a csv modul nélkül.
"""
import argparse
import math
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')
KAROLI = os.path.join(K, 'Karoli_1908.tsv')
KJV = os.path.join(K, 'KJV_Strongs_teljes.tsv')
TAHOT = os.path.join(K, 'TAHOT_kivonat.tsv')
KONYV = os.path.join(K, 'Konyv_normalizalo_tabla.tsv')
GRAM = os.path.join(ROOT, 'adat', 'grammatikai_strongok.tsv')
ALAP_KIMENET = os.path.join(ROOT, 'naplok', 'F117_szoveg_osszevetes.tsv')
ALAP_ITELET = os.path.join(ROOT, 'naplok', 'F117_itelet.tsv')
MINTA = ['Hós 14', 'Én 6', 'Dán 3', 'Jón 2']

# Az F117 A–D′ célhalmaza (brief 1. táblázat): fejezet -> {vers: osztály}; None = a fejezet minden verse
A_FEJEZETEK = ['2Móz 35', '2Móz 36', 'Dán 3', 'Hós 2', 'Hós 13', 'Hós 14', 'Jób 17', 'Jób 37', 'Péld 12', 'Én 5',
               'Én 6', 'Ézs 4', 'Ézs 64']
CEL = {fj: None for fj in A_FEJEZETEK}
CEL['Préd 9'] = {v: 'B' for v in (21, 22, 23)}
CEL['Jób 39'] = {v: 'B' for v in range(34, 39)}
CEL['1Kir 22'] = dict([(v, 'D') for v in (46, 47, 48, 49, 54)] + [(v, "D′") for v in (43, 44, 45, 50, 51, 52, 53)])
CEL['Ézs 3'] = 'D'
CEL['Jón 2'] = 'D'
CEL['1Sám 24'] = 'D'
CEL['1Sám 20'] = {43: 'D'}


def cel_osztaly(fj, v):
    """-> az A–D′ osztály, vagy '' (a fejezet nem célvers-e, csak kontextus)."""
    c = CEL.get(fj, '')
    if c is None:
        return 'C' if (fj == 'Dán 3' and v >= 31) else 'A'
    if isinstance(c, str):
        return c
    return c.get(v, '')

# igazítási súlyok és büntetések (a 4.2 mintán rögzítve; a küszöb a DT-F117b tárgya)
W_NEV, W_SZAM, W_HOSSZ = 0.45, 0.15, 0.40
W_TAHOT = 0.40          # a 'teljes' igazításban: (1 - W_TAHOT) * szoveg + W_TAHOT * tahot
P_KAROLI_URES = 0.35    # Károli-vers pár nélkül
P_KJV_KIHAGY = 0.35     # KJV-vers kihagyva az igazítás belsejében
P_OSSZEVON = 0.10       # 1-2 vagy 2-1 lépés

VERS_K = re.compile(r'^(.+) (\d+):(\d+)$')
VERS_S = re.compile(r'^([^.]+)\.(\d+)\.(\d+)$')
SZO = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)


def sorok(path):
    with open(path, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if s and not s.startswith('#'):
                yield s.split('\t')


def konyv_tabla():
    hu2st = {}
    for p in sorok(KONYV):
        if p[0] == 'STEPBible-rövidítés' or len(p) < 2:
            continue
        hu2st[p[1]] = p[0]
    return hu2st


def gram_strongok():
    out = set()
    for p in sorok(GRAM):
        if p[0] != 'strong':
            out.add(norm_strong(p[0]))
    return out


def norm_strong(s):
    m = re.match(r'^([HG])0*(\d+)', s.strip())
    return (m.group(1) + m.group(2)) if m else ''


def kar_fejezet(konyv, c):
    out = []
    for p in sorok(KAROLI):
        m = VERS_K.match(p[0])
        if m and m.group(1) == konyv and int(m.group(2)) == c:
            out.append((int(m.group(3)), p[1] if len(p) > 1 else ''))
    return sorted(out)


def kjv_ablak(st, fejezetek):
    """-> [(c, v, [angol szavak], {strongok})] a megadott fejezetekre, sorrendben."""
    d = {}
    for p in sorok(KJV):
        m = VERS_S.match(p[0])
        if not m or m.group(1) != st or int(m.group(2)) not in fejezetek:
            continue
        kulcs = (int(m.group(2)), int(m.group(3)))
        e = d.setdefault(kulcs, ([], set()))
        if len(p) > 3:
            e[0].append(p[3])
        if len(p) > 2:
            for x in p[2].split('+'):
                n = norm_strong(x)
                if n:
                    e[1].add(n)
    return [(c, v, d[(c, v)][0], d[(c, v)][1]) for (c, v) in sorted(d)]


def tahot_strongok(konyv, fejezetek):
    d = {}
    for p in sorok(TAHOT):
        m = VERS_K.match(p[0])
        if not m or m.group(1) != konyv or int(m.group(2)) not in fejezetek:
            continue
        n = norm_strong(p[1]) if len(p) > 1 else ''
        if n:
            d.setdefault((int(m.group(2)), int(m.group(3))), set()).add(n)
    return d


# ---- jelek -------------------------------------------------------------------------------------------------------

def _ekezet_le(s):
    return ''.join(ch for ch in unicodedata.normalize('NFD', s) if unicodedata.category(ch) != 'Mn')


def hang_kulcs(szo):
    s = _ekezet_le(szo.lower()).replace('’', '').replace("'", '')
    for a, b in (('ph', 'f'), ('th', 't'), ('sh', 's'), ('ch', 'k'), ('sz', 's'), ('zs', 's'), ('cs', 'c'),
                 ('gy', 'g'), ('ny', 'n'), ('ly', 'i'), ('ck', 'k'), ('c', 'k'), ('q', 'k'), ('x', 'ks'),
                 ('y', 'i'), ('j', 'i'), ('w', 'v'), ('z', 's'), ('h', '')):
        s = s.replace(a, b)
    # mássalhangzó-váz (a magánhangzók a két nyelv névalakjaiban a legkevésbé stabilak: Nabukodonozor/Nebuchadnezzar,
    # Sidrák/Shadrach); az első három mássalhangzó a kulcs, így a magyar toldalék (Sidrákot) nem zavar
    s = re.sub(r'[aeiou]', '', s)
    s = re.sub(r'(.)\1+', r'\1', s)
    return s[:3]


def kar_nevek(szoveg):
    """Nagybetűs szavak; mondatkezdő csak akkor, ha isteni név. Úr* -> lord, Isten* -> god."""
    out = []
    mondat_eleje = True
    for m in re.finditer(r"[^\W\d_]+|[.!?:;]", szoveg):
        t = m.group(0)
        if t in '.!?:;':
            mondat_eleje = True
            continue
        if t[0].isupper():
            low = _ekezet_le(t.lower())
            if low.startswith('ur') and len(t) <= 7:
                out.append('lord')
            elif low.startswith('isten'):
                out.append('god')
            elif not mondat_eleje:
                out.append(hang_kulcs(t))
        mondat_eleje = False
    return out


def kjv_nevek(szavak):
    out = []
    for w in szavak:
        for t in re.findall(r"[^\W\d_]+", w):
            if not t[0].isupper() or t in ('I', 'O'):
                continue
            low = t.lower()
            if low in ('lord', 'god', 'gods'):
                out.append('lord' if low == 'lord' else 'god')
            else:
                out.append(hang_kulcs(t))
    return out


HU_SZAM = {'kettő': 2, 'két': 2, 'kettőt': 2, 'három': 3, 'négy': 4, 'öt': 5, 'hét': 7, 'nyolc': 8, 'kilenc': 9,
           'tíz': 10, 'tizen': 10, 'húsz': 20, 'huszon': 20, 'harminc': 30, 'negyven': 40, 'ötven': 50, 'hatvan': 60,
           'hetven': 70, 'nyolcvan': 80, 'kilencven': 90, 'száz': 100, 'ezer': 1000, 'második': 2, 'harmad': 3,
           'negyed': 4, 'ötöd': 5, 'hatod': 6, 'heted': 7, 'nyolcad': 8, 'kilenced': 9, 'tized': 10}
EN_SZAM = {'two': 2, 'twain': 2, 'second': 2, 'three': 3, 'third': 3, 'four': 4, 'fourth': 4, 'five': 5, 'fifth': 5,
           'six': 6, 'sixth': 6, 'seven': 7, 'seventh': 7, 'eight': 8, 'eighth': 8, 'nine': 9, 'ninth': 9,
           'ten': 10, 'tenth': 10, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60,
           'threescore': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000,
           'twelve': 12, 'eleven': 11}
_HU_TOVEK = sorted(HU_SZAM, key=len, reverse=True)


def kar_szamok(szoveg):
    out = []
    for t in SZO.findall(szoveg.lower()):
        if t in ('öt', 'hét', 'két', 'kettő', 'kettőt'):
            out.append(HU_SZAM[t])
            continue
        for tv in _HU_TOVEK:
            if len(tv) >= 4 and t.startswith(tv):
                out.append(HU_SZAM[tv])
                break
    return out


def kjv_szamok(szavak):
    out = []
    for w in szavak:
        for t in re.findall(r"[^\W\d_]+", w.lower()):
            if t in EN_SZAM:
                out.append(EN_SZAM[t])
    return out


def _halmaz_egyezes(a, b):
    if not a and not b:
        return 0.5
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    return len(sa & sb) / max(len(sa), len(sb))


def nev_egyezes(a, b):
    if not a and not b:
        return 0.5
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    hit = sum(1 for x in sa if any(x == y or (min(len(x), len(y)) >= 2 and (x.startswith(y) or y.startswith(x)))
                                    for y in sb))
    return hit / max(len(sa), len(sb))


def horgonyok(nevek_szamok):
    return [x for x in nevek_szamok]


class Vers:
    __slots__ = ('kulcs', 'szoveg', 'nevek', 'szamok', 'hossz', 'strong', 'horgony')


def kar_vers(konyv, c, v, szoveg, tahot):
    x = Vers()
    x.kulcs = '%s %d:%d' % (konyv, c, v)
    x.szoveg = szoveg
    x.nevek = kar_nevek(szoveg)
    x.szamok = kar_szamok(szoveg)
    x.hossz = max(1, len(SZO.findall(szoveg)))
    x.strong = tahot.get((c, v), set())
    x.horgony = _horgony_sor(szoveg, kar=True)
    return x


def kjv_vers(c, v, szavak, strongok):
    x = Vers()
    x.kulcs = '%d:%d' % (c, v)
    x.szoveg = ' '.join(szavak)
    x.nevek = kjv_nevek(szavak)
    x.szamok = kjv_szamok(szavak)
    x.hossz = max(1, len(szavak))
    x.strong = strongok
    x.horgony = _horgony_sor(x.szoveg, kar=False)
    return x


def _horgony_sor(szoveg, kar):
    """A szöveg-sorrendű horgonyok (név-kulcs vagy szám) listája."""
    nev = kar_nevek(szoveg) if kar else kjv_nevek(szoveg.split())
    szam = kar_szamok(szoveg) if kar else kjv_szamok(szoveg.split())
    # sorrend: a két lista összefésülése a szövegbeli első előfordulás szerint (közelítés: nevek, majd számok)
    return nev + ['#%d' % n for n in szam]


def egyesit(a, b, kar):
    x = Vers()
    x.kulcs = a.kulcs + '+' + b.kulcs.split(':')[-1]
    x.szoveg = a.szoveg + ' ' + b.szoveg
    x.nevek = a.nevek + b.nevek
    x.szamok = a.szamok + b.szamok
    x.hossz = a.hossz + b.hossz
    x.strong = a.strong | b.strong
    x.horgony = a.horgony + b.horgony
    return x


def jelek(k, j, arany_med, gram):
    nev = nev_egyezes(k.nevek, j.nevek)
    szam = _halmaz_egyezes(k.szamok, j.szamok)
    r = (k.hossz / j.hossz) / arany_med
    hossz = math.exp(-abs(math.log(r)))
    if k.horgony and j.horgony:
        eu = int(nev_egyezes([k.horgony[0]], [j.horgony[0]]) == 1) + int(nev_egyezes([k.horgony[-1]], [j.horgony[-1]]) == 1)
    else:
        eu = '-'
    ks, js = k.strong - gram, j.strong - gram
    tahot = (len(ks & js) / len(ks | js)) if (ks or js) else 0.0
    szov = W_NEV * nev + W_SZAM * szam + W_HOSSZ * hossz
    return {'nev': nev, 'szam': szam, 'hossz': hossz, 'r': r, 'eu': eu, 'tahot': tahot, 'szoveg': szov,
            'teljes': (1 - W_TAHOT) * szov + W_TAHOT * tahot}


# ---- igazítás ----------------------------------------------------------------------------------------------------

def igazit(kv, jv, arany_med, gram, mod):
    """Monoton igazítás. -> lista: Károli-indexenként (kjv_indexek tuple, lépés)."""
    n, m = len(kv), len(jv)
    NEG = -1e9
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    bt = [[None] * (m + 1) for _ in range(n + 1)]
    for jj in range(m + 1):
        dp[0][jj] = 0.0          # ingyenes KJV-kihagyás az elején
        bt[0][jj] = ('start',)
    cache = {}

    def s(ki, ji, ki2=None, ji2=None):
        kk = (ki, ji, ki2, ji2)
        if kk not in cache:
            k = kv[ki] if ki2 is None else egyesit(kv[ki], kv[ki2], True)
            j = jv[ji] if ji2 is None else egyesit(jv[ji], jv[ji2], False)
            cache[kk] = jelek(k, j, arany_med, gram)[mod]
        return cache[kk]

    for i in range(n + 1):
        for jj in range(m + 1):
            if i == 0:
                continue
            best, arg = NEG, None
            # 1-1
            if jj >= 1 and dp[i - 1][jj - 1] > NEG:
                v = dp[i - 1][jj - 1] + s(i - 1, jj - 1)
                if v > best:
                    best, arg = v, ('11',)
            # 1-2
            if jj >= 2 and dp[i - 1][jj - 2] > NEG:
                v = dp[i - 1][jj - 2] + s(i - 1, jj - 2, None, jj - 1) - P_OSSZEVON
                if v > best:
                    best, arg = v, ('12',)
            # 2-1
            if i >= 2 and jj >= 1 and dp[i - 2][jj - 1] > NEG:
                v = dp[i - 2][jj - 1] + s(i - 2, jj - 1, i - 1, None) - P_OSSZEVON
                if v > best:
                    best, arg = v, ('21',)
            # Károli-vers pár nélkül
            if dp[i - 1][jj] > NEG:
                v = dp[i - 1][jj] - P_KAROLI_URES
                if v > best:
                    best, arg = v, ('10',)
            # KJV-vers kihagyva (belül)
            if jj >= 1 and dp[i][jj - 1] > NEG and i >= 1:
                v = dp[i][jj - 1] - P_KJV_KIHAGY
                if v > best:
                    best, arg = v, ('01',)
            dp[i][jj], bt[i][jj] = best, arg
    # ingyenes KJV-kihagyás a végén
    jj = max(range(m + 1), key=lambda x: dp[n][x])
    i = n
    par = [None] * n
    kihagy = []          # az igazítás belsejében kihagyott (árva) KJV-versek indexei
    while i > 0:
        op = bt[i][jj][0]
        if op == '11':
            par[i - 1] = ((jj - 1,), '1-1')
            i, jj = i - 1, jj - 1
        elif op == '12':
            par[i - 1] = ((jj - 2, jj - 1), '1-2')
            i, jj = i - 1, jj - 2
        elif op == '21':
            par[i - 1] = ((jj - 1,), '2-1')
            par[i - 2] = ((jj - 1,), '2-1')
            i, jj = i - 2, jj - 1
        elif op == '10':
            par[i - 1] = ((), 'nincs_par')
            i -= 1
        elif op == '01':
            kihagy.append(jj - 1)
            jj -= 1
        else:
            break
    return par, sorted(kihagy)


def fejezet_osszevet(konyv, c, hu2st, gram, blokk=False):
    """Egy Károli-fejezet igazítása. blokk=True: a Károli c-1..c+1 fejezetei együtt, a KJV c-2..c+2 ablakára
    (a szomszéd fejezetekkel közös, hézag- és átfedésmentes lefedés ellenőrzéséhez); az eredmény a c fejezet sorai.
    -> (eredmény, arány, árva KJV-versek [(kulcs, előtte álló Károli-vers, utána álló Károli-vers)])"""
    st = hu2st[konyv]
    kar_fej = [cc for cc in ((c - 1, c, c + 1) if blokk else (c,)) if cc >= 1]
    kar = []
    for cc in kar_fej:
        kar += [(cc, v, t) for v, t in kar_fejezet(konyv, cc)]
    if not any(cc == c for cc, _, _ in kar):
        raise SystemExit('nincs Károli-szöveg: %s %d' % (konyv, c))
    kar_fej = sorted({cc for cc, _, _ in kar})
    fej = set(range(min(kar_fej) - 1, max(kar_fej) + 2))
    kjv = kjv_ablak(st, fej)
    tahot = tahot_strongok(konyv, set(kar_fej))
    kv_all = [kar_vers(konyv, cc, v, t, tahot) for cc, v, t in kar]
    jv = [kjv_vers(cc, vv, sz, sg) for cc, vv, sz, sg in kjv]
    # hosszarány-medián: a Károli-fejezet(ek) szószáma / a KJV ugyanazon számú fejezete(i)nek szószáma
    kar_ossz = sum(x.hossz for x in kv_all)
    kjv_c = [x for x in jv if int(x.kulcs.split(':')[0]) in kar_fej]
    arany_med = kar_ossz / max(1, sum(x.hossz for x in kjv_c))
    p_sz, _ = igazit(kv_all, jv, arany_med, gram, 'szoveg')
    p_te, kihagy = igazit(kv_all, jv, arany_med, gram, 'teljes')
    # árva KJV-versek: az igazítás belsejében kihagyott KJV-versek, a két szomszéd Károli-verssel
    arva = []
    for x in kihagy:
        elotte = [kv_all[i].kulcs for i in range(len(kv_all)) if p_te[i][0] and max(p_te[i][0]) < x]
        utana = [kv_all[i].kulcs for i in range(len(kv_all)) if p_te[i][0] and min(p_te[i][0]) > x]
        arva.append((jv[x].kulcs, elotte[-1] if elotte else '-', utana[0] if utana else '-'))
    sel = [i for i, (cc, _, _) in enumerate(kar) if cc == c]
    kv = [kv_all[i] for i in sel]
    p_sz = [p_sz[i] for i in sel]
    p_te = [p_te[i] for i in sel]
    eredmeny = []
    for i, k in enumerate(kv):
        idx_sz, lep_sz = p_sz[i]
        idx_te, lep_te = p_te[i]
        jav_sz = ';'.join(jv[x].kulcs for x in idx_sz)
        jav_te = ';'.join(jv[x].kulcs for x in idx_te)
        if idx_te:
            j = jv[idx_te[0]] if len(idx_te) == 1 else egyesit(jv[idx_te[0]], jv[idx_te[1]], False)
            jl = jelek(k, j, arany_med, gram)
        else:
            jl = None
        # a második legjobb KJV-vers a szöveg-jel szerint (a választotton kívül), a margó méréséhez
        cand = sorted(((jelek(k, j2, arany_med, gram)['szoveg'], j2.kulcs) for j2 in jv
                       if j2.kulcs not in jav_te.split(';')), reverse=True)
        masodik = '%s:%.2f' % (cand[0][1], cand[0][0]) if cand else ''
        # szomszéd-margó: a választott pár szöveg-jele mínusz a ±1 eltolt KJV-vers szöveg-jele (a tipikus táblahiba
        # az egyverses eltolás); csak 1-1 lépésnél
        if len(idx_te) == 1:
            szomsz = [jelek(k, jv[x], arany_med, gram)['szoveg'] for x in (idx_te[0] - 1, idx_te[0] + 1)
                      if 0 <= x < len(jv)]
            masodik += ' | margo=%+.2f' % (jl['szoveg'] - max(szomsz)) if szomsz else ''
        if jav_sz == jav_te and jav_te:
            ok = 'szoveg=teljes (%s)' % lep_te
        elif not jav_te and not jav_sz:
            ok = 'nincs_par mindkét igazításban'
        else:
            ok = 'ELTÉR: szoveg=%s, teljes=%s' % (jav_sz or '-', jav_te or '-')
        eredmeny.append((k, jav_te, jav_sz, jl, masodik, ok, [jv[x] for x in idx_te]))
    return eredmeny, arany_med, arva


def itelet_betolt(path):
    out = {}
    if not os.path.exists(path):
        return out
    for p in sorok(path):
        if p[0] == 'igehely_karoli':
            continue
        out[p[0]] = (p[1] if len(p) > 1 else '', p[2] if len(p) > 2 else '')
    return out


def eltolas_tipus(karoli_kulcs, kjv):
    """azonos_szam / eltolt (fejezeten belül) / fejezetvalto / nincs_par."""
    if not kjv:
        return 'nincs_par'
    c, v = karoli_kulcs.rsplit(' ', 1)[1].split(':')
    kc, kv_ = kjv.split(';')[0].split(':')
    if kc != c:
        return 'fejezetvalto'
    return 'azonos_szam' if kv_ == v else 'eltolt'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fejezet', action='append', default=[])
    ap.add_argument('--minta', action='store_true')
    ap.add_argument('--teljes', action='store_true',
                    help='az A–D′ célhalmaz minden fejezete, blokk-igazítással (a szomszéd fejezetekkel együtt)')
    ap.add_argument('--kimenet', default=ALAP_KIMENET)
    ap.add_argument('--itelet', default=ALAP_ITELET)
    ap.add_argument('--szoveg', action='store_true', help='a két szöveg kiírása olvasáshoz; fájlt nem ír')
    ap.add_argument('--csak-cel', action='store_true', help='--szoveg mellett csak a célversek')
    ap.add_argument('--blokk', action='store_true', help='blokk-igazítás --fejezet mellett is')
    a = ap.parse_args()
    fejezetek = (MINTA if a.minta else []) + (list(CEL) if a.teljes else []) + a.fejezet
    if not fejezetek:
        ap.error('--minta, --teljes vagy --fejezet kell')
    hu2st = konyv_tabla()
    gram = gram_strongok()
    itelet = itelet_betolt(a.itelet)
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    ki = []
    arva_ossz = []
    for fj in fejezetek:
        m = re.match(r'^(.+) (\d+)$', fj)
        konyv, c = m.group(1), int(m.group(2))
        eredm, arany, arva = fejezet_osszevet(konyv, c, hu2st, gram, blokk=(a.teljes or a.blokk))
        for x in arva:
            arva_ossz.append((fj,) + x)
        if a.szoveg:
            print('=== %s (szószám-arány medián %.2f; árva KJV a blokkban: %s) ===' % (
                fj, arany, ', '.join('%s [%s | %s]' % x for x in arva) or '-'))
            for k, jt, js, jl, mas, ok, jvs in eredm:
                v = int(k.kulcs.rsplit(':', 1)[1])
                osz = cel_osztaly(fj, v)
                if a.csak_cel and not osz:
                    continue
                print('%s [%s] → %s | %s | %s' % (k.kulcs, osz or 'kontextus', jt or '-', ok, mas))
                print('   K: %s' % k.szoveg)
                for j in jvs:
                    print('   J %s: %s' % (j.kulcs, j.szoveg))
            continue
        for k, jt, js, jl, mas, ok, jvs in eredm:
            v = int(k.kulcs.rsplit(':', 1)[1])
            osz = cel_osztaly(fj, v)
            it, it_megj = itelet.get(k.kulcs, ('', ''))
            if it == '':
                elt = ''
            else:
                elt = 'egyezik' if it == jt else 'ELTÉR'
            sor = [k.kulcs, osz or 'kontextus', jt, js, eltolas_tipus(k.kulcs, jt),
                   '%.2f' % jl['nev'] if jl else '', '%.2f' % jl['szam'] if jl else '',
                   '%.2f' % jl['r'] if jl else '', str(jl['eu']) if jl else '',
                   '%.2f' % jl['tahot'] if jl else '', '%.2f' % jl['szoveg'] if jl else '',
                   mas, ok, it, elt, it_megj,
                   'scope=gepi:%s%s | forras=eszkozok/versmegf_szoveg_osszevet.py | ts=%s%s' % (
                       fj, ' (blokk)' if a.teljes else '', ts,
                       (' ; itelet: scope=manual | forras=%s' % os.path.relpath(a.itelet, ROOT).replace('\\', '/')) if it else '')]
            assert not any('\t' in x or '\n' in x for x in sor)
            ki.append('\t'.join(sor))
    if a.szoveg:
        return
    n_cel = sum(1 for s in ki if s.split('\t')[1] != 'kontextus')
    fejlec = [
        '# F117 4.2–4.3: Károli 1908 ↔ KJV versenkénti szöveg-összevetés (a Karoli_versmegfeleltetes.tsv olvasása nélkül)',
        '# proveniencia: scope=%s | forras=Karoli_1908.tsv+KJV_Strongs_teljes.tsv+TAHOT_kivonat.tsv '
        '(eszkozok/versmegf_szoveg_osszevet.py%s) | n=%d (célvers: %d) | ts=%s' % (
            '+'.join(fejezetek), ' --teljes' if a.teljes else '', len(ki), n_cel, ts),
        '# jelek: nev/szam [0..1] (mindkét oldal üres: 0,5); hossz_r = szószám-arány / medián (1 = átlagos); '
        'elso_utolso 0–2; tahot = Strong-Jaccard (NEM független jel); s_szoveg = %.2f*nev + %.2f*szam + %.2f*hossz' % (
            W_NEV, W_SZAM, W_HOSSZ),
        '# kjv_teljes = igazítás szöveg+TAHOT-jellel; kjv_szoveg = igazítás csak szöveg-jellel; osztaly = A–D′ célvers '
        'vagy kontextus (a célfejezet nem célverse); itelet = kézi ítélet a két szöveg elolvasása után; '
        'eltérés = az itelet és a kjv_teljes viszonya',
        '# árva KJV-vers (az igazítás belsejében kihagyva; blokk: [előtte | utána álló Károli-vers]): %s' % (
            '; '.join('%s: %s [%s | %s]' % x for x in arva_ossz) or 'nincs'),
        '\t'.join(['igehely_karoli', 'osztaly', 'kjv_teljes', 'kjv_szoveg', 'eltolas', 'nev', 'szam', 'hossz_r',
                   'elso_utolso', 'tahot', 's_szoveg', 'masodik_legjobb', 'dontesi_ok', 'itelet', 'elteres',
                   'itelet_megjegyzes', 'proveniencia']),
    ]
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(fejlec + ki) + '\n')
    print('írva: %s (%d sor, célvers %d; árva KJV: %d)' % (a.kimenet, len(ki), n_cel, len(arva_ossz)))


if __name__ == '__main__':
    main()
