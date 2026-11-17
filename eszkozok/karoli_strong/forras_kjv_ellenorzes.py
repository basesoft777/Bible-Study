#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""F175K — a Strong-réteg FORRÁSOLDALÁNAK ellenőrzése független tanúval (KJV), versenként,
szóhalmaz-szinten.

KÉRDÉS. A nyílt Károli–Strong adatkészletben a Strong-számot program rendeli a párhoz a
STEPBible TAHOT (héber ÓSZ) / TAGNT (görög ÚSZ) forrásszavaiból. Egyeznek-e e forrás
Strong-címkéi a KJV (eBible, konkordancia/KJV_Strongs_teljes.tsv) Strong-címkéivel?
A mérés a PÁROSÍTÁST NEM méri (azt az emberi validáció méri), csak a forráscímkék
(és a csomag pároknál álló Strong-halmazának) összhangját egy független tanúval.

EGYSÉG. Egy összehasonlítási egység = egy Károli-vers (a csomag 31 158 verse) és a
versmegfeleltetési tábla (konkordancia/Karoli_versmegfeleltetes.tsv, igehely_kjv) szerinti KJV-vers;
az ÚSZ-re a tábla nem terjed ki, ott a Károli- és a KJV-számozás azonosnak vett (a hiány, az
árva KJV-vers külön jelölve). Több Károli-vers egy KJV-versre képeződhet (egység = az unió);
az a KJV-vers, amelyre egyetlen Károli-vers sem képeződik („árva”), az ugyanabban a fejezetben
előtte álló, képezett KJV-vers egységéhez tartozik (a Károli összevonta a két verset; a
tiszta 1:1 halmaz `K_alap`, a kiegészített `K_ext`; az összesítés a K_ext-et használja, a
kiegészítésre szoruló egységek száma és kimenetele a diagnosztikában áll).
Nem illeszthető vers (okonként számolva): `nincs_versmegf_sor`, `nincs_kjv_megfeleles`
(a tábla igehely_kjv oszlopa üres/nem fejezet:vers), `kjv_vers_hianyzik` (a KJV-fájlban
nincs ilyen vers), `nincs_forras_token` (a Károli-versnek nincs TAHOT/TAGNT tokenje).

HALMAZOK (versenként, Strong-számonként egyszer; a Strong 4 jegyre nullázva):
  T_all   a TAHOT/TAGNT-kivonat összes Strong-címkéje a Károli-kulcson (a „+”-os
          összetett címke tagjai külön); a H9001–H9049 morféma-kódok kiszűrve.
  T_ref   ÓSZ: = T_all. ÚSZ: csak a TR-es tokenek (a repó definíciója: a „Kritikai
          kiadás” mezőben `TR`, `TR»N` vagy `TR«N` áll — tokenek.betolt_eredeti; a KJV a
          Textus Receptusból fordít, a csomag `nem_tr` oszlopa ugyanezt jelöli). Szigorúbb,
          másodlagos változat (`forras_TR_vs_kjv`): a `TR¹`-szerű, a TR eltérő olvasatát
          jelölő tokenek kimaradnak, de a KJV rájuk is címkéz, ezért a fő változat a T_all.
  P       a nyílt csomag `parok/NN_*.tsv` Strong-halmaza (a pároknál ténylegesen álló
          Strongok; morféma-kód kiszűrve) — a csomag használói ezt kapják.
  K       a KJV Strong-címkéi; a KJV igealak-kódjai (héber > 8674, görög > 5624) és a
          H9001–H9049 kiszűrve.
KONVENCIÓ. Ugyanaz a lexéma más számon (pontossag_kulso.KONVENCIO, ott dokumentálva):
a csoport minden tagja a legkisebb számra képeződik mindkét oldalon. A `_nyers` változat
ezt nem alkalmazza; a `_tartalmi` változat a grammatikai Strongokat (adat/grammatikai_strongok.tsv)
is kihagyja mindkét oldalról (a KJV a névelőt, a tárgyjelet stb. gyakran nem címkézi).

MÉRŐSZÁMOK (egységenként, majd ÓSZ/ÚSZ, könyvcsoport és könyv szerint összesítve):
  egyező halmaz (T = K) · KJV ⊆ forrás (K ⊆ T: a KJV minden Strongja megvan a forrásban) ·
  forrás ⊆ KJV (T ⊆ K) · átlagos Jaccard · mikro: közös / KJV-Strongok (a KJV-címkék
  mekkora része van meg a forrásban) és közös / forrás-Strongok.
  Értelmezés: a KJV nem fordít minden forrásszót (T ⊋ K természetes), ezért a K\T
  (csak KJV) az érdemi jel: a forrás hiányzó vagy más számú címkéje.

FŐ VÁLTOZAT: `forras_vs_kjv` = T_all (a csomag `szavak` `er` oldalával versenként azonos: a
diagnosztika ellenőrzi) a konvencióval normált K_ext ellen; a többi változat: `_nyers`
(konvenció nélkül), `_tartalmi` (grammatikai Strongok nélkül), `forras_TR_vs_kjv` (T_ref),
`csomag_parok_vs_kjv` (P).

GYANÚS CÍMKÉK (f175k/gyanus_forrascimkek.tsv): a konvenció-normált T_all és K_ext
különbségeiből — `csak_forras` (T\K), `csak_kjv` (K\T) és `csere` (az egységben pontosan
egy T\K és egy K\T elem: valószínűleg ugyanaz a szó két számon). Gyanús jelölt: legalább
`--min-vers` vers és legalább `--min-arany` arány (a Strong megjelenéseinek mekkora hányadában
hiányzik a másik oldalról), nem grammatikai Strong; a `csak_forras` jelölt csak akkor gyanús, ha van
csere-partnere is (a KJV a szavak nagy részét — kötőszó, „minden”, „lenni” — egyáltalán nem címkézi,
ez nem forráshiba); `csere`: legalább `--min-vers` vers és nem ismert konvenció; a csere a TARTALMI
halmazokból képződik (a nagyon gyakori szavaknál két független eltérés egybeesése elkerülhetetlen).
Ez JELÖLT-lista (kézi ellenőrzésre), nem hibalista: a jelöltek javarésze a KJV-Strong külön
számot adó alakváltozata (fokozás, igető, névmási alak), nem a TAHOT/TAGNT hibája.

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong/forras_kjv_ellenorzes.py
    python eszkozok/karoli_strong/forras_kjv_ellenorzes.py --kimenet f175k --verstabla <út.tsv>

A TSV-ket split/join kezeli (a `csv` modul tilos, CLAUDE.md). A kimenet nem tartalmaz
Károli-szöveget és nem tartalmaz zárt forrásból való adatot.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

AZ = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.normpath(os.path.join(AZ, '..', '..'))
sys.path.insert(0, AZ)
sys.path.insert(0, os.path.join(AZ, '..'))
import pontossag_kulso as pk  # noqa: E402  (KONVENCIO, _KONV_CSOPORT — a dokumentált megfeleltetés)
from nyilt_mag_export import STEP_OSIS  # noqa: E402  (STEPBible-rövidítés -> OSIS-könyvkód)

# a F22 műfaji besorolása (pontossag_minta.CSOPORT), OSIS-könyvkódokkal
CSOPORT = {}
for _k in ['Gen', 'Exod', 'Lev', 'Num', 'Deut']:
    CSOPORT[_k] = 'OSZ_mozes'
for _k in ['Josh', 'Judg', 'Ruth', '1Sam', '2Sam', '1Kgs', '2Kgs', '1Chr', '2Chr', 'Ezra', 'Neh', 'Esth']:
    CSOPORT[_k] = 'OSZ_tortenet'
for _k in ['Job', 'Ps', 'Prov', 'Eccl', 'Song', 'Lam']:
    CSOPORT[_k] = 'OSZ_koltoi'
for _k in ['Isa', 'Jer', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph',
           'Hag', 'Zech', 'Mal']:
    CSOPORT[_k] = 'OSZ_profeta'
for _k in ['Matt', 'Mark', 'Luke', 'John', 'Acts']:
    CSOPORT[_k] = 'USZ_evangelium'
for _k in ['Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus',
           'Phlm', 'Heb', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude']:
    CSOPORT[_k] = 'USZ_level'
CSOPORT['Rev'] = 'USZ_jelenesek'
USZ = frozenset(k for k, v in CSOPORT.items() if v.startswith('USZ'))

TR_KIADAS = re.compile(r'^TR(?:[»«]\d+)?$')   # tokenek._TR_KIADAS
IGEHELY = re.compile(r'^(.+) (\d+):(\d+)$')
KONYV_ALIAS = {'Sir': 'JSir'}                  # nyilt_mag_export.KONYV_ALIAS
STRONG = re.compile(r'^([HG])(\d+)$')
KJV_CV = re.compile(r'^\d+:\d+$')

VALTOZATOK = [
    # név, forrás-oldali halmaz, konvenció-normált-e, tartalmi-e
    ('forras_vs_kjv', 'T_all', True, False),            # a fő változat
    ('forras_vs_kjv_nyers', 'T_all', False, False),
    ('forras_vs_kjv_tartalmi', 'T_all', True, True),
    ('forras_TR_vs_kjv', 'T_ref', True, False),
    ('csomag_parok_vs_kjv', 'P', True, False),
]


# ---------------------------------------------------------------------------------------- olvasás

def tsv_sorok(ut):
    """A „#” sorokat és az üres sorokat átugorja; az első sor a fejléc. split('\\t'), csv nélkül."""
    with open(ut, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if not s.strip() or s.startswith('#'):
                continue
            yield s.split('\t')


def strong_norm(s):
    m = STRONG.match(s.strip())
    return '%s%04d' % (m.group(1), int(m.group(2))) if m else None


def szam(s):
    return int(s[1:])


def morfema(s):
    return s[0] == 'H' and 9001 <= szam(s) <= 9049


def igealak_kod(s):
    return szam(s) > (8674 if s[0] == 'H' else 5624)


def kanon_terkep():
    """{Strong: a konvenció-csoport képviselője (a legkisebb szám)}, a pontossag_kulso.KONVENCIO csoportjaiból."""
    ki = {}
    for elo, csoportok in pk._KONV_CSOPORT.items():
        for csop in csoportok:
            kep = '%s%04d' % (elo, min(csop))
            for n in csop:
                ki['%s%04d' % (elo, n)] = kep
    return ki


def konyv_terkep(normtabla):
    """(magyar rövidítés -> OSIS, STEPBible-rövidítés -> OSIS, OSIS -> magyar rövidítés)."""
    it = tsv_sorok(normtabla)
    next(it)
    hu2osis, osis2hu = {}, {}
    for r in it:
        osis = STEP_OSIS[r[0]]
        hu2osis[r[1]] = osis
        osis2hu[osis] = r[1]
    for a, b in KONYV_ALIAS.items():
        if b in hu2osis:
            hu2osis[a] = hu2osis[b]
    return hu2osis, osis2hu


def hu_kulcs(igehely, hu2osis):
    m = IGEHELY.match(igehely)
    if not m or m.group(1) not in hu2osis:
        return None
    return (hu2osis[m.group(1)], int(m.group(2)), int(m.group(3)))


def osis_kulcs(osis):
    """'Gen.1.1' -> ('Gen', 1, 1)."""
    k, c, v = osis.split('.')
    return (k, int(c), int(v))


def step_kulcs(step):
    k, c, v = step.split('.')
    return (STEP_OSIS[k], int(c), int(v))


def kulcs_hu(k, osis2hu):
    return '%s %d:%d' % (osis2hu.get(k[0], k[0]), k[1], k[2])


def betolt_kjv(ut):
    """({vers: {Strong}}, a KJV-ben létező versek halmaza, {Strong: első angol szó})."""
    kjv, jelen, angol = defaultdict(set), set(), {}
    it = tsv_sorok(ut)
    next(it)
    for r in it:
        k = step_kulcs(r[0])
        jelen.add(k)
        s = strong_norm(r[2])
        if s is None or morfema(s) or igealak_kod(s):
            continue
        kjv[k].add(s)
        angol.setdefault(s, r[3].strip())
    return kjv, jelen, angol


def betolt_forras(ut, nt, hu2osis):
    """(T_all, T_ref, jelen, gloss): TAHOT (nt=False) vagy TAGNT (nt=True), Károli-kulcson.
    T_ref: ÚSZ-ben csak a TR-es tokenek (a repó definíciója); ÓSZ-ben = T_all."""
    t_all, t_ref, jelen, gloss = defaultdict(set), defaultdict(set), set(), {}
    nem_kulcs = 0
    it = tsv_sorok(ut)
    next(it)
    for r in it:
        k = hu_kulcs(r[0], hu2osis)
        if k is None:
            nem_kulcs += 1
            continue
        jelen.add(k)
        tr = True
        if nt:
            tr = any(TR_KIADAS.match(x) for x in (r[7].split('+') if len(r) > 7 else []))
        for s in r[1].split('+'):
            s = strong_norm(s)
            if s is None or morfema(s):
                continue
            t_all[k].add(s)
            if tr:
                t_ref[k].add(s)
            gloss.setdefault(s, '%s | %s' % (r[4].strip(), r[5].strip()))
    return t_all, t_ref, jelen, gloss, nem_kulcs


def betolt_versmegf(ut, hu2osis):
    """{Károli-vers kulcs: KJV-vers kulcs vagy None (az igehely_kjv nem fejezet:vers)}."""
    megf = {}
    it = tsv_sorok(ut)
    next(it)
    for r in it:
        k = hu_kulcs(r[0], hu2osis)
        if k is None:
            continue
        kjv = r[1].strip()
        megf[k] = (k[0], int(kjv.split(':')[0]), int(kjv.split(':')[1])) if KJV_CV.match(kjv) else None
    return megf


def betolt_csomag(mappa):
    """(univerzum: [(könyv,c,v)] sorrendben, P {vers: {Strong}}, E {vers: {Strong}} a csomag szavak
    `er` oldaláról). A csomag a sajátos OSIS-kulccsal (Gen.1.1) azonosít."""
    univerzum = []
    it = tsv_sorok(os.path.join(mappa, 'versek.tsv'))
    next(it)
    for r in it:
        univerzum.append(osis_kulcs(r[0]))
    par, er = defaultdict(set), defaultdict(set)
    pdir = os.path.join(mappa, 'parok')
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith('.tsv'):
            continue
        it = tsv_sorok(os.path.join(pdir, fn))
        next(it)
        for r in it:
            s = strong_norm(r[4])
            if s is not None and not morfema(s):
                par[osis_kulcs(r[0])].add(s)
    sdir = os.path.join(mappa, 'szavak')
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith('.tsv'):
            continue
        it = tsv_sorok(os.path.join(sdir, fn))
        next(it)
        for r in it:
            if r[1] != 'er' or len(r) < 7 or not r[6]:
                continue
            for x in r[6].split('+'):
                s = strong_norm(x)
                if s is not None and not morfema(s):
                    er[osis_kulcs(r[0])].add(s)
    return univerzum, par, er


def betolt_grammatikai(ut):
    if not ut or not os.path.exists(ut):
        return set()
    it = tsv_sorok(ut)
    next(it)
    ki = set()
    for r in it:
        s = strong_norm(r[0])
        if s:
            ki.add(s)
    return ki


def forras_arva_kapcsol(univerzum, t_all, t_ref, jelen):
    """Azok a TAHOT/TAGNT-versek, amelyeknek nincs Károli-versük (a Károli egy versbe vonta őket az előzővel),
    az ugyanabban a fejezetben előttük álló Károli-vers T-halmazához tartoznak (a csomag `er` oldala is így
    kezeli őket). Visszaad: (t_all, t_ref másolata az unióval, a kapcsolt versek száma, a kapcsolatlanoké)."""
    uv = set(univerzum)
    fej = defaultdict(list)
    for v in univerzum:
        fej[(v[0], v[1])].append(v[2])
    ta, tr = {k: set(v) for k, v in t_all.items()}, {k: set(v) for k, v in t_ref.items()}
    kapcs = nelkul = 0
    for o in sorted(jelen):
        if o in uv:
            continue
        elozo = [n for n in fej.get((o[0], o[1]), []) if n < o[2]]
        if not elozo:
            nelkul += 1
            continue
        p = (o[0], o[1], max(elozo))
        ta.setdefault(p, set()).update(t_all.get(o, ()))
        tr.setdefault(p, set()).update(t_ref.get(o, ()))
        kapcs += 1
    return ta, tr, kapcs, nelkul


# ------------------------------------------------------------------------------- egységek építése

def egysegek_epit(univerzum, t_all, t_ref, jelen_forras, par, kjv, kjv_jelen, megf, osis2hu):
    """Összehasonlítási egységek + a ki nem hagyott versek okonkénti listája.
    Egység: {'id', 'konyv', 'csoport', 'hu': [Károli-vers kulcsok], 'T_all', 'T_ref', 'P',
             'K_alap', 'K_ext', 'arva': az egységhez kapcsolt árva KJV-versek száma}."""
    kizart = []            # (kulcs, oldal, ok)
    cel = {}               # Károli-vers -> KJV-vers kulcs
    for v in univerzum:
        if v[0] in USZ:
            t = v
            if t not in kjv_jelen:
                kizart.append((v, 'karoli', 'kjv_vers_hianyzik'))
                continue
        else:
            if v not in megf:
                kizart.append((v, 'karoli', 'nincs_versmegf_sor'))
                continue
            t = megf[v]
            if t is None:
                kizart.append((v, 'karoli', 'nincs_kjv_megfeleles'))
                continue
            if t not in kjv_jelen:
                kizart.append((v, 'karoli', 'kjv_vers_hianyzik'))
                continue
        cel[v] = t
    hivatkozott = set(cel.values())
    # árva KJV-versek: létező, de Károli-vers nem képeződik rájuk (csak a csomag könyveiben)
    konyvek = {v[0] for v in univerzum}
    fejezetek = defaultdict(list)           # (könyv, c) -> a hivatkozott KJV-versek számai
    for t in hivatkozott:
        fejezetek[(t[0], t[1])].append(t[2])
    for lista in fejezetek.values():
        lista.sort()
    arva_kapcsolt = defaultdict(list)       # hivatkozott KJV-vers -> kapcsolt árva versek
    arva_nelkul = []
    for o in sorted(kjv_jelen):
        if o in hivatkozott or o[0] not in konyvek:
            continue
        elozo = [n for n in fejezetek.get((o[0], o[1]), []) if n < o[2]]
        if elozo:
            arva_kapcsolt[(o[0], o[1], elozo[-1])].append(o)
        else:
            arva_nelkul.append(o)
            kizart.append((o, 'kjv', 'kjv_vers_karoli_parja_nelkul'))
    csoportok = defaultdict(list)           # KJV-vers -> a rá képeződő Károli-versek
    for v in univerzum:
        if v in cel:
            csoportok[cel[v]].append(v)
    egysegek = []
    for v in univerzum:
        if v not in cel or csoportok.get(cel[v], [None])[0] != v:
            continue
        tag = csoportok[cel[v]]
        van = [x for x in tag if x in jelen_forras]
        if not van:
            for x in tag:
                kizart.append((x, 'karoli', 'nincs_forras_token'))
            continue
        for x in tag:
            if x not in jelen_forras:
                kizart.append((x, 'karoli', 'nincs_forras_token'))
        t = cel[v]
        k_alap = set(kjv.get(t, ()))
        k_ext = set(k_alap)
        for o in arva_kapcsolt.get(t, []):
            k_ext |= kjv.get(o, set())
        egysegek.append({
            'id': kulcs_hu(v, osis2hu), 'konyv': v[0], 'fejezet': (v[0], v[1]),
            'csoport': CSOPORT.get(v[0], 'ismeretlen'), 'hu': van,
            'T_all': set().union(*(t_all.get(x, set()) for x in van)),
            'T_ref': set().union(*(t_ref.get(x, set()) for x in van)),
            'P': set().union(*(par.get(x, set()) for x in van)),
            'K_alap': k_alap, 'K_ext': k_ext, 'arva': len(arva_kapcsolt.get(t, [])),
            'kjv_vers': kulcs_hu(t, osis2hu), 'tobb_karoli': len(tag) > 1})
    return egysegek, kizart, len(arva_nelkul), sum(len(x) for x in arva_kapcsolt.values())


# ----------------------------------------------------------------------------------- mérés

def halmazok(e, forras_mezo, kanon_van, tartalmi, kanon, gramm):
    """(T, K) az egységből a változat szerint."""
    t, k = e[forras_mezo], e['K_ext']
    if kanon_van:
        t = {kanon.get(s, s) for s in t}
        k = {kanon.get(s, s) for s in k}
    if tartalmi:
        t = {s for s in t if s not in gramm}
        k = {s for s in k if s not in gramm}
    return t, k


def mutato(par_lista):
    """par_lista: [(T, K)] -> mérőszámok szótára."""
    n = len(par_lista)
    egyezo = rk = rt = 0
    jacc = 0.0
    inter = st = sk = 0
    for t, k in par_lista:
        i = len(t & k)
        u = len(t | k)
        egyezo += t == k
        rk += k <= t
        rt += t <= k
        jacc += (i / u) if u else 1.0
        inter += i
        st += len(t)
        sk += len(k)
    return {'egyseg_db': n, 'egyezo_db': egyezo, 'kjv_reszhalmaza_db': rk, 'forras_reszhalmaza_db': rt,
            'jaccard_atlag': (jacc / n) if n else 0.0, 'forras_strong_db': st, 'kjv_strong_db': sk,
            'kozos_strong_db': inter}


def arany(a, b):
    return '%.4f' % (a / b) if b else ''


def meres_sorok(egysegek, kanon, gramm):
    """[(valtozat, tipus, csoport, mutato)] — ÖSSZES, testamentum, könyvcsoport, könyv szerint."""
    ki = []
    for nev, mezo, kanon_van, tartalmi in VALTOZATOK:
        csoportok = defaultdict(list)
        for e in egysegek:
            par_ = halmazok(e, mezo, kanon_van, tartalmi, kanon, gramm)
            nt = 'USZ' if e['konyv'] in USZ else 'OSZ'
            csoportok[('osszes', 'OSSZES')].append(par_)
            csoportok[('testamentum', nt)].append(par_)
            csoportok[('konyvcsoport', e['csoport'])].append(par_)
            csoportok[('konyv', e['konyv'])].append(par_)
        for (tip, cs), lista in sorted(csoportok.items(), key=lambda x: (x[0][0] != 'osszes', x[0][0] != 'testamentum',
                                                                       x[0][0] != 'konyvcsoport', x[0][1])):
            ki.append((nev, tip, cs, mutato(lista)))
    return ki


MERES_FEJ = ['valtozat', 'csoport_tipus', 'csoport', 'egyseg_db', 'egyezo_halmaz_db', 'egyezo_halmaz_arany',
             'kjv_reszhalmaza_db', 'kjv_reszhalmaza_arany', 'forras_reszhalmaza_db', 'forras_reszhalmaza_arany',
             'jaccard_atlag', 'forras_strong_db', 'kjv_strong_db', 'kozos_strong_db',
             'kjv_strongok_megvannak_aranya', 'forras_strongok_kjvben_aranya']


def meres_tsv_sor(nev, tip, cs, m):
    return [nev, tip, cs, str(m['egyseg_db']), str(m['egyezo_db']), arany(m['egyezo_db'], m['egyseg_db']),
            str(m['kjv_reszhalmaza_db']), arany(m['kjv_reszhalmaza_db'], m['egyseg_db']),
            str(m['forras_reszhalmaza_db']), arany(m['forras_reszhalmaza_db'], m['egyseg_db']),
            '%.4f' % m['jaccard_atlag'], str(m['forras_strong_db']), str(m['kjv_strong_db']),
            str(m['kozos_strong_db']), arany(m['kozos_strong_db'], m['kjv_strong_db']),
            arany(m['kozos_strong_db'], m['forras_strong_db'])]


# ------------------------------------------------------------------------- gyanús címkék

def gyanus_lista(egysegek, kanon, gramm, gloss, angol, min_vers, min_arany, top):
    r"""Jelölt-lista a konvenció-normált T_all és K_ext különbségeiből.
    csak_forras / csak_kjv: a teljes halmazokból (T\K, K\T); csere: a TARTALMI halmazokból (grammatikai Strongok
    nélkül) az egységek, ahol pontosan egy T\K és egy K\T elem van (a két független különbség egybeesése a
    nagyon gyakori szavaknál elkerülhetetlen, ezért kimaradnak). Gyanús: l. a modul docstringje."""
    csak_f, csak_k, csere = Counter(), Counter(), Counter()
    pelda = defaultdict(list)
    f_vers, k_vers, mindket = Counter(), Counter(), Counter()
    for e in egysegek:
        t, k = halmazok(e, 'T_all', True, False, kanon, gramm)
        for s in t:
            f_vers[s] += 1
        for s in k:
            k_vers[s] += 1
        for s in t & k:
            mindket[s] += 1
        for s in t - k:
            csak_f[s] += 1
            if len(pelda[('f', s)]) < 3:
                pelda[('f', s)].append(e['id'])
        for s in k - t:
            csak_k[s] += 1
            if len(pelda[('k', s)]) < 3:
                pelda[('k', s)].append(e['id'])
        tc, kc = halmazok(e, 'T_all', True, True, kanon, gramm)
        df, dk = tc - kc, kc - tc
        if len(df) == 1 and len(dk) == 1:
            c = (next(iter(df)), next(iter(dk)))
            csere[c] += 1
            if len(pelda[('c', c)]) < 3:
                pelda[('c', c)].append(e['id'])
    legjobb_t, legjobb_k = {}, {}       # forrás-Strong -> (legtöbb csere partnere, db); KJV-Strong -> (…)
    for (t, k), n in sorted(csere.items(), key=lambda x: (-x[1], x[0])):
        legjobb_t.setdefault(t, (k, n))
        legjobb_k.setdefault(k, (t, n))

    def gl(s):
        return gloss.get(s, '')

    def an(s):
        return angol.get(s, '')

    def megj(s):
        if s[0] == 'G' and szam(s) > 5624:
            return 'STEPBible-kiterjesztett görög kód (> 5624), a KJV Strong-rendszerében nincs'
        return ''

    sorok = []
    for tip, szamlalo, nevezo, partnerek in (('csak_forras', csak_f, f_vers, legjobb_t),
                                             ('csak_kjv', csak_k, k_vers, legjobb_k)):
        rendezett = sorted(szamlalo.items(), key=lambda x: (-x[1], x[0]))
        for i, (s, n) in enumerate(rendezett):
            ar = n / nevezo[s] if nevezo[s] else 0.0
            gram = s in gramm
            partner, pn = partnerek.get(s, ('', 0))
            if tip == 'csak_kjv':
                gyanus = n >= min_vers and ar >= min_arany and not gram
            else:
                # a KJV a szavak nagy részét (kötőszó, minden, lenni …) nem címkézi: a csak_forras gyanús, ha
                # van csere-partner (a KJV ugyanazt a szót más számon címkézi)
                gyanus = n >= min_vers and ar >= min_arany and not gram and pn >= 0.3 * n
            if i >= top and not gyanus:
                continue
            kulcs = 'f' if tip == 'csak_forras' else 'k'
            sorok.append([tip, s if tip == 'csak_forras' else '', s if tip == 'csak_kjv' else '', str(n),
                          str(nevezo[s]), str(mindket[s]), '%.4f' % ar, 'nem', 'igen' if gram else 'nem',
                          gl(s) if tip == 'csak_forras' else '', an(s) if tip == 'csak_kjv' else '',
                          partner, str(pn) if partner else '', '; '.join(pelda[(kulcs, s)]),
                          'igen' if gyanus else 'nem', megj(s) if tip == 'csak_forras' else ''])
    rendezett = sorted(csere.items(), key=lambda x: (-x[1], x[0]))
    for i, ((t, k), n) in enumerate(rendezett):
        ismert = t[0] == k[0] and frozenset({szam(t), szam(k)}) in pk.KONVENCIO
        gyanus = n >= min_vers and not ismert
        if i >= top and not gyanus:
            continue
        sorok.append(['csere', t, k, str(n), '', '', '', 'igen' if ismert else 'nem', 'nem', gl(t), an(k), '', '',
                      '; '.join(pelda[('c', (t, k))]), 'igen' if gyanus else 'nem', megj(t)])
    return sorok


GYANUS_FEJ = ['tipus', 'strong_forras', 'strong_kjv', 'vers_db', 'oldal_osszes_vers_db', 'mindket_oldalon_vers_db',
              'arany', 'ismert_konvencio', 'grammatikai', 'forras_szoto_jelentes', 'kjv_angol_szo',
              'csere_partner', 'csere_partner_vers_db', 'peldak', 'gyanus', 'megjegyzes']


def alacsony_atfedes(egysegek, kanon, gramm, min_kjv, kuszob):
    """Egységek, ahol a KJV Strongjainak kevesebb mint `kuszob` hányada van meg a forrásban (és a KJV-nak legalább
    `min_kjv` Strongja van): a versszámozási eltolás / versösszevonás jelölt-helyei. Visszaad: (sorok, a
    fejezetek száma, ahol ≥ 40% az ilyen egységek aránya (legalább 5 egység))."""
    ki, fej = [], defaultdict(lambda: [0, 0])
    for e in egysegek:
        t, k = halmazok(e, 'T_all', True, False, kanon, gramm)
        x = fej[e['fejezet']]
        x[0] += 1
        if len(k) >= min_kjv and len(t & k) / len(k) < kuszob:
            x[1] += 1
            ki.append([e['id'], e['kjv_vers'], str(len(t)), str(len(k)), str(len(t & k)),
                       '%.4f' % (len(t & k) / len(k)), str(e['arva']), '1' if e['tobb_karoli'] else '0'])
    rossz = sum(1 for n, b in fej.values() if n >= 5 and b / n >= 0.4)
    return ki, rossz


# ------------------------------------------------------------------------------ diagnosztika

def diagnosztika(univerzum, egysegek, kizart, arva_nelkul, arva_kapcsolt_db, t_all, er, nem_kulcs,
                 kanon, gramm, osis2hu):
    d = []
    d.append(('karoli_versek_a_csomagban', len(univerzum)))
    d.append(('osszehasonlitott_egysegek', len(egysegek)))
    d.append(('osszehasonlitott_karoli_versek', sum(len(e['hu']) for e in egysegek)))
    d.append(('egyseg_tobb_karoli_versbol', sum(1 for e in egysegek if e['tobb_karoli'])))
    for ok, n in sorted(Counter(x[2] for x in kizart).items()):
        d.append(('nem_illesztheto:' + ok, n))
    d.append(('kjv_arva_versek_karoli_pár_nélkül', arva_nelkul))
    d.append(('kjv_arva_versek_egyseghez_kapcsolva', arva_kapcsolt_db))
    kiegesz = [e for e in egysegek if e['arva']]
    d.append(('egyseg_arva_kjv_verssel_kiegeszitve', len(kiegesz)))

    def lefed(e, mezo):
        t = {kanon.get(x, x) for x in e['T_all']}
        k = {kanon.get(x, x) for x in e[mezo]}
        return len(t & k) / len(t) if t else 1.0
    if kiegesz:
        d.append(('kiegeszitett_egyseg_forras_strongok_kjvben_aranya_K_alappal',
                  '%.4f' % (sum(lefed(e, 'K_alap') for e in kiegesz) / len(kiegesz))))
        d.append(('kiegeszitett_egyseg_forras_strongok_kjvben_aranya_K_ext-tel',
                  '%.4f' % (sum(lefed(e, 'K_ext') for e in kiegesz) / len(kiegesz))))
    d.append(('forras_sor_nem_leképezhető_kulcs', nem_kulcs))
    # a csomag eredeti oldala és a kivonat T_all összevetése Károli-versenként
    egyez = elter = 0
    elterok = []
    for v in univerzum:
        a, b = er.get(v, set()), t_all.get(v, set())
        if a == b:
            egyez += 1
        else:
            elter += 1
            elterok.append(kulcs_hu(v, osis2hu))
    d.append(('csomag_er_oldal_egyezik_a_kivonattal_vers', egyez))
    d.append(('csomag_er_oldal_elter_a_kivonattol_vers', elter))
    d.append(('csomag_er_oldal_elter_versek', '; '.join(elterok[:20])))
    d.append(('ures_kjv_halmaz_egyseg', sum(1 for e in egysegek if not e['K_ext'])))
    d.append(('ures_forras_halmaz_egyseg', sum(1 for e in egysegek if not e['T_all'])))
    return d


# --------------------------------------------------------------------------------- kimenet

def git_head():
    try:
        return subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=GYOKER, capture_output=True,
                              text=True, check=True).stdout.strip() or 'ismeretlen'
    except Exception:
        return 'ismeretlen'


def fejlec(forras, head, megj):
    return ('# MANUAL: scope=F175K a Strong-réteg forrásoldali ellenőrzése a KJV-val (TAHOT/TAGNT vs KJV Strong-címkék, '
            'versenként, szóhalmaz-szinten; a párosítást nem méri) | forras=%s @ git:%s | ts=git:%s | manual '
            '(determinisztikus szkript: eszkozok/karoli_strong/forras_kjv_ellenorzes.py; %s; nincs szöveges '
            'Károli-tartalom)\n' % (forras, head, head, megj))


def ir(ut, fej_sor, fejlec_sor, sorok):
    os.makedirs(os.path.dirname(os.path.abspath(ut)), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej_sor)
        f.write('\t'.join(fejlec_sor) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')


def futtat(a, head=None):
    head = head or git_head()
    kon = a.konkordancia
    hu2osis, osis2hu = konyv_terkep(os.path.join(kon, 'Konyv_normalizalo_tabla.tsv'))
    kanon = kanon_terkep()
    gramm = betolt_grammatikai(a.grammatikai)
    kjv, kjv_jelen, angol = betolt_kjv(os.path.join(kon, 'KJV_Strongs_teljes.tsv'))
    ho_all, ho_ref, ho_jelen, gl_h, nk1 = betolt_forras(os.path.join(kon, 'TAHOT_kivonat.tsv'), False, hu2osis)
    nt_all, nt_ref, nt_jelen, gl_g, nk2 = betolt_forras(os.path.join(kon, 'TAGNT_kivonat.tsv'), True, hu2osis)
    t_all, t_ref, jelen = {}, {}, ho_jelen | nt_jelen
    t_all.update(ho_all)
    t_all.update(nt_all)
    t_ref.update(ho_ref)
    t_ref.update(nt_ref)
    gloss = dict(gl_h)
    gloss.update(gl_g)
    megf = betolt_versmegf(os.path.join(kon, 'Karoli_versmegfeleltetes.tsv'), hu2osis)
    univerzum, par, er = betolt_csomag(a.csomag)
    t_all, t_ref, forras_arva, forras_arva_nelkul = forras_arva_kapcsol(univerzum, t_all, t_ref, jelen)
    egysegek, kizart, arva_nelkul, arva_kapcsolt = egysegek_epit(univerzum, t_all, t_ref, jelen, par, kjv, kjv_jelen,
                                                                  megf, osis2hu)
    forras = ('konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/KJV_Strongs_teljes.tsv, '
              'konkordancia/Karoli_versmegfeleltetes.tsv, nyilt_karoli_strong/data (Zenodo 1.0)')
    kim = a.kimenet
    ms = meres_sorok(egysegek, kanon, gramm)
    ir(os.path.join(kim, 'meres_osszesites.tsv'),
       fejlec(forras, head, 'változatok: forras_vs_kjv (fő: T_all, konvenció-normált), _nyers, _tartalmi, forras_TR_vs_kjv '
                            '(ÚSZ-ben csak a TR-es tokenek), csomag_parok_vs_kjv; egység = Károli-vers (több-egy leképezésnél unió)'),
       MERES_FEJ, [meres_tsv_sor(*x) for x in ms])
    gy = gyanus_lista(egysegek, kanon, gramm, gloss, angol, a.min_vers, a.min_arany, a.top)
    ir(os.path.join(kim, 'gyanus_forrascimkek.tsv'),
       fejlec(forras, head, 'a konvenció-normált T_all és K_ext különbségei; top %d / tipus + minden gyanús jelölt '
                            '(min_vers=%d, min_arany=%.2f); JELÖLT-lista, nem hibalista' % (a.top, a.min_vers, a.min_arany)),
       GYANUS_FEJ, gy)
    kiz = [[kulcs_hu(k, osis2hu), oldal, ok] for k, oldal, ok in kizart]
    kiz.sort(key=lambda x: (x[2], x[1], x[0]))
    ir(os.path.join(kim, 'nem_illesztheto_versek.tsv'),
       fejlec(forras, head, 'oldal: karoli = a csomag Károli-verse, kjv = KJV-vers (a KJV-igehely a KJV-számozás szerint)'),
       ['igehely', 'oldal', 'ok'], kiz)
    al, rossz_fejezet = alacsony_atfedes(egysegek, kanon, gramm, a.min_kjv, a.atfedes_kuszob)
    ir(os.path.join(kim, 'alacsony_atfedesu_egysegek.tsv'),
       fejlec(forras, head, 'egységek, ahol a KJV Strongjainak < %.0f%%-a van meg a forrásban (KJV-Strongok >= %d; '
                            'konvenció-normált): a versszámozási eltolás / versösszevonás jelölt-helyei'
                            % (a.atfedes_kuszob * 100, a.min_kjv)),
       ['igehely_karoli', 'igehely_kjv', 'forras_db', 'kjv_db', 'kozos_db', 'kozos_per_kjv', 'kapcsolt_arva_kjv_vers',
        'tobb_karoli_vers'], al)
    dg = diagnosztika(univerzum, egysegek, kizart, arva_nelkul, arva_kapcsolt, t_all, er, nk1 + nk2, kanon, gramm,
                      osis2hu)
    fo = {(t, c): m for n, t, c, m in ms if n == 'forras_vs_kjv'}
    for cs in ('OSSZES', 'OSZ', 'USZ'):
        m = fo[('osszes' if cs == 'OSSZES' else 'testamentum', cs)]
        dg.append(('kjv_csak_strong_elofordulas_%s' % cs, m['kjv_strong_db'] - m['kozos_strong_db']))
    dg.append(('ebbol_a_gyanus_csak_kjv_jeloltek_strongjain', sum(int(x[3]) for x in gy if x[0] == 'csak_kjv' and x[14] == 'igen')))
    dg.append(('forras_vers_karoli_pár_nélkül_elozo_hez_kapcsolva', forras_arva))
    dg.append(('forras_vers_karoli_pár_nélkül_kapcsolat_nélkül', forras_arva_nelkul))
    dg.append(('egyseg_alacsony_atfedessel', len(al)))
    dg.append(('fejezet_ahol_az_alacsony_atfedesu_egysegek_aranya_>=40%', rossz_fejezet))
    ir(os.path.join(kim, 'diagnosztika.tsv'), fejlec(forras, head, 'számlálók'), ['mutato', 'ertek'],
       [[k, str(v)] for k, v in dg])
    if a.verstabla:
        sor = []
        for e in egysegek:
            t, k = halmazok(e, 'T_all', True, False, kanon, gramm)
            sor.append([e['id'], e['kjv_vers'], str(len(t)), str(len(k)), str(len(t & k)),
                        ' '.join(sorted(t - k)), ' '.join(sorted(k - t))])
        ir(a.verstabla, fejlec(forras, head, 'versenkénti (forras_vs_kjv); csak a mérés munkaanyaga, nem része a letétnek'),
           ['igehely_karoli', 'igehely_kjv', 'forras_db', 'kjv_db', 'kozos_db', 'csak_forras', 'csak_kjv'], sor)
    return ms, dg, gy, al


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--konkordancia', default=os.path.join(GYOKER, 'konkordancia'))
    ap.add_argument('--csomag', default=os.path.join(GYOKER, 'nyilt_karoli_strong', 'data'))
    ap.add_argument('--grammatikai', default=os.path.join(GYOKER, 'adat', 'grammatikai_strongok.tsv'))
    ap.add_argument('--kimenet', default=os.path.join(GYOKER, 'f175k'))
    ap.add_argument('--verstabla', default=None, help='opcionális versenkénti TSV (a repón kívülre ajánlott)')
    ap.add_argument('--min-vers', dest='min_vers', type=int, default=5)
    ap.add_argument('--min-arany', dest='min_arany', type=float, default=0.5)
    ap.add_argument('--top', type=int, default=50)
    ap.add_argument('--min-kjv', dest='min_kjv', type=int, default=4)
    ap.add_argument('--atfedes-kuszob', dest='atfedes_kuszob', type=float, default=0.5)
    a = ap.parse_args(argv)
    ms, dg, gy, al = futtat(a)
    for nev, tip, cs, m in ms:
        if tip in ('osszes', 'testamentum') or (tip == 'konyvcsoport' and nev == 'forras_vs_kjv'):
            print('%-24s %-12s %-16s egység %5d  egyező %s  KJV⊆forrás %s  Jaccard %.4f  KJV-Strongok megvannak %s'
                  % (nev, tip, cs, m['egyseg_db'], arany(m['egyezo_db'], m['egyseg_db']),
                     arany(m['kjv_reszhalmaza_db'], m['egyseg_db']), m['jaccard_atlag'],
                     arany(m['kozos_strong_db'], m['kjv_strong_db'])))
    for k, v in dg:
        print('%-55s %s' % (k, v))
    print('gyanús jelölt: %d, alacsony átfedésű egység: %d' % (sum(1 for x in gy if x[14] == 'igen'), len(al)))


if __name__ == '__main__':
    main()
