#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V27 — konvenció-egységesítés: a Károli 1908 – Strong párosítás 1.1-es állapotának törlőlistája.

A döntés: DT-F175vr (dontesek/uj/johd-validacio-70cc1f.md). A párosítási prompt (`f21p/prompt_v3.md`) A szabálya
szerint a héber határozott névelő (H9009) és a görög névelő (G3588) `forditatlan`, kivéve a névmási szerepet; a C
szabály szerint a tárgyjelölő ʾet (H0853) `forditatlan`. A 2. szabályt (a H9xxx előtag a ragos magyar szóhoz
tartozik) a párosító modell a névelőre is alkalmazta. Az 1.1 a validáció előtt ezeket a kapcsolatokat törli.

A szabály (determinisztikus, a pár rögzített jegyeiből: a pár Strong-száma, a magyar szó, és az utána álló magyar
szó ugyanabban a versben):
  * törlődik minden `parok_*.tsv`-sor, amelynek `strong`-ja H9009, G3588 vagy H0853, és a magyar szava
    (kisbetűsítve) nincs a megtartó listán;
  * a megtartó lista négy csoportja (`megtartas_oka`):
      - `nevmas`: névmás, mutató és vonatkozó szó (NEVMAS), a „ma”, „mai” időmutatóval;
      - `a_vonatkozo`: az „a” szó, ha utána vonatkozó névmás áll (a ki, a mely, a mi …; az „a” a kettéírt
        vonatkozó névmás része, prompt_v3 B);
      - `onallo_az`: az önálló „az” (a prompt_v3 A szabálya szerint az „önálló az” jelentés névmási szerep;
        a névelői „az”-tól a pár jegyeiből nem választható el, ezért marad, és az ismert-hiba listára kerül);
      - `megszolito`: a megszólító névelő „óh” fordítása (pl. Bír 16:28).
Csak törlő javítás: új pár nem keletkezik, a megmaradó `parok`-sorok bájtra változatlanok. A `szavak_*.tsv`-ben a
két érintett token partnerlistája szűkül; ha üres lesz, a magyar token `betoldas`, az eredeti `forditatlan` lesz; a
magyar token `strong` mezője a megmaradó partnerekből vezetődik le (mint az `egyesit.py`-ban); a token
`bizonyossag` és `forras` mezője változatlan (a két modell döntését írja le, nem a takarítást).

Módok:
  --felmeres [--letet DIR]  gyakorisági tábla a törlendő kapcsolatok magyar szavairól (típusonként, Strong-számonként),
                            a megtartott kapcsolatok táblája, a 95%-ot lefedő típusokon kívüli maradékból 50 véletlen
                            tétel versszöveggel (rögzített mag), és egy összefoglaló; MIND a repón kívüli letétbe
                            (alapértelmezés: ~/Bible-Study-letet/konvencio_11/), mert a validátorok nem láthatják
  --general DIR             az 1.1 `parok_*.tsv` és `szavak_*.tsv` táblái DIR-be, a törlőlistával
                            (`torolt_kapcsolatok.tsv`) és az ismert-hiba listával (`ismert_hiba_onallo_az.tsv`);
                            utána lefut az --ellenoriz
  --ellenoriz DIR           egy előállított 1.1 ellenőrzése az 1.0-hoz képest: a párok részhalmaz, minden megmaradó
                            sor bájtra azonos, a törölt sorok pontosan a törlőlista, a szótábla konzisztens
  --hash                    a törlőlista SHA-256-ja (a kanonikus `torolt_kapcsolatok.tsv` bájtjain)

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (a `csv` modul tilos, CLAUDE.md).
"""
import argparse
import collections
import glob
import hashlib
import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FORRAS = os.path.join(GYOKER, 'adat', 'karoli_strong')
KAROLI = os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv')
LETET = os.path.join(os.path.expanduser('~'), 'Bible-Study-letet', 'konvencio_11')

CEL_STRONG = ('H0853', 'G3588', 'H9009')
MAG = 'F175.V27 konvencio-egysegesites'
LEFEDES = 0.95
MARADEK_DB = 50

# --- a megtartó lista (rögzített; a változtatás a törlőlista hash-ét is változtatja) ---------------------------
_KI = ('ki kik kit kiket kinek kiknek kiben kikben kinél kiknél kitől kiktől kihez kikhez kivel kikkel kié kiké '
       'kiért kikért kiből kikből kire kikre kiről kikről kin kiken')
_MELY = ('mely melyek melyet melyeket melynek melyeknek melyben melyekben melynél melyeknél melytől melyektől '
         'melyhez melyekhez mellyel melylyel melyekkel melyért melyekért melyből melyekből melyre melyekre melyről '
         'melyekről melyen melyeken')
_MI = 'mi mik mit miket minek miknek miben miből mire miről mitől mihez mié'
_A_ELOTAGU = 'aki akik akit akiket akinek akiknek amely amelyek amelyet amelyeket amelynek ami amit amik'
_VALA = 'valaki valakik valakit valakinek valami valamit'
_EZ = ('e ez ezt ezek ezeket ennek ezeknek ebben ezekben ezen ezeken ezzel ezekkel erre ezekre ebből ezekből ettől '
       'ezektől ehhez ezekhez erről ezekről ezé ezeké')
_AZ = ('azt azok azokat annak azoknak abban azokban azon azokon azzal azokkal arra azokra abból azokból attól '
       'azoktól ahhoz azokhoz azokért arról azokról azé azoké')
_AMA = 'ama amaz amazok amazokat amazt amannak amazoknak'
_UGYAN = 'ugyanaz ugyanazt ugyanazon ugyanazok ugyanannak ugyanez ugyanezt ugyanezen ugyanebben ugyanabban'
_ILYEN = 'ilyen ilyenek ilyent olyan olyanok olyant'
_SZEMELYES = ('én engem nékem te téged néked ő őt néki őnéki ők őket nékik őnékik minket nékünk ti titeket néktek '
              'övé övéi vele velök velem veled velünk veletek tőle tőlök tőlem hozzá hozzájok érette érettök róla '
              'rajta benne bennök belőle')
_HATAROZATLAN = 'némelyek némelyeket mások'
_IDO = 'ma mai'

VONATKOZO = frozenset((_KI + ' ' + _MELY + ' ' + _MI).split())
NEVMAS = frozenset(' '.join((_KI, _MELY, _MI, _A_ELOTAGU, _VALA, _EZ, _AZ, _AMA, _UGYAN, _ILYEN, _SZEMELYES,
                             _HATAROZATLAN, _IDO)).split())
MEGSZOLITO = frozenset(('óh', 'oh', 'ó'))
ONALLO_AZ = 'az'

TORLO_FEJ = ['vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong']


def megtartas_oka(hu_szo, kovetkezo):
    """A pár megtartásának oka, vagy None (= törlendő). Csak a CEL_STRONG párjaira hívandó."""
    s = hu_szo.lower()
    k = (kovetkezo or '').lower()
    if s in MEGSZOLITO:
        return 'megszolito'
    if s == ONALLO_AZ:
        return 'onallo_az'
    if s == 'a' and k in VONATKOZO:
        return 'a_vonatkozo'
    if s in NEVMAS:
        return 'nevmas'
    return None


def tabla_olvas(ut):
    """(proveniencia-sor, fejléc, sorok[list], nyers sorok[str]) — az első sor `#`-kezdetű proveniencia."""
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read().split('\n')
    if nyers and nyers[-1] == '':
        nyers = nyers[:-1]
    if not nyers or not nyers[0].startswith('#'):
        raise SystemExit('nincs proveniencia-sor: %s' % ut)
    fej = nyers[1].split('\t')
    adat = nyers[2:]
    return nyers[0], fej, [s.split('\t') for s in adat], adat


def konyvek():
    """A könyvek nevei (a fájlnév `parok_` utáni része), rendezve."""
    nevek = sorted(os.path.basename(p)[len('parok_'):-len('.tsv')] for p in glob.glob(os.path.join(FORRAS, 'parok_*.tsv')))
    if not nevek:
        raise SystemExit('nincs parok_*.tsv: %s' % FORRAS)
    for n in nevek:
        if not os.path.exists(os.path.join(FORRAS, 'szavak_%s.tsv' % n)):
            raise SystemExit('hiányzó szavak_%s.tsv' % n)
    return nevek


def konyv_dontes(konyv):
    """Egy könyv párjai a döntéssel: [(sor, nyers, ok|None|'nem_cel')], a szótábla és a hu-tokenek."""
    _, pfej, psorok, pnyers = tabla_olvas(os.path.join(FORRAS, 'parok_%s.tsv' % konyv))
    _, sfej, ssorok, _ = tabla_olvas(os.path.join(FORRAS, 'szavak_%s.tsv' % konyv))
    pi = {k: i for i, k in enumerate(pfej)}
    si = {k: i for i, k in enumerate(sfej)}
    hu = {}
    for r in ssorok:
        if r[si['oldal']] == 'hu':
            hu[(r[si['vers']], int(r[si['sorszam']]))] = r[si['szo']]
    ki = []
    for r, ny in zip(psorok, pnyers):
        if r[pi['strong']] not in CEL_STRONG:
            ki.append((r, ny, 'nem_cel'))
            continue
        kov = hu.get((r[pi['vers']], int(r[pi['hu_sorszam']]) + 1))
        ki.append((r, ny, megtartas_oka(r[pi['hu_szo']], kov)))
    return pi, ki, hu


def torlolista():
    """A törlőlista sorai (TORLO_FEJ szerint) könyv- és fájlsorrendben, a megtartott sorok az okkal."""
    torol, megtart = [], []
    for kv in konyvek():
        pi, dontesek, hu = konyv_dontes(kv)
        for r, _, ok in dontesek:
            if ok == 'nem_cel':
                continue
            sor = [r[pi['vers']], r[pi['hu_sorszam']], r[pi['hu_szo']], r[pi['er_sorszam']], r[pi['er_szo']],
                   r[pi['strong']]]
            if ok is None:
                torol.append(sor)
            else:
                kov = hu.get((r[pi['vers']], int(r[pi['hu_sorszam']]) + 1), '')
                megtart.append(sor + [ok, kov, kv])
    return torol, megtart


def torlolista_bajtok(torol):
    return ('\t'.join(TORLO_FEJ) + '\n' + ''.join('\t'.join(s) + '\n' for s in torol)).encode('utf-8')


def torlolista_hash(torol=None):
    if torol is None:
        torol, _ = torlolista()
    return hashlib.sha256(torlolista_bajtok(torol)).hexdigest()


# --- az 1.1 előállítása -------------------------------------------------------------------------------------------

def hu_strong(strongok):
    """A magyar token `strong` mezője: a partnerek Strong-számai ismétlés nélkül, sorrendben, `+`-szal (egyesit.py)."""
    ut = []
    for x in strongok:
        if x not in ut:
            ut.append(x)
    return '+'.join(ut)


def szavak_szukit(sfej, ssorok, torolt):
    """A szótábla az 1.1 szerint. torolt: {(vers, hu_sorszam, er_sorszam)}. Visszaad: új sorok (list)."""
    si = {k: i for i, k in enumerate(sfej)}
    er_strong = {}
    for r in ssorok:
        if r[si['oldal']] == 'er':
            er_strong[(r[si['vers']], int(r[si['sorszam']]))] = r[si['strong']]
    hu_vesz = collections.defaultdict(set)
    er_vesz = collections.defaultdict(set)
    for v, h, e in torolt:
        hu_vesz[(v, h)].add(e)
        er_vesz[(v, e)].add(h)
    uj = []
    for r in ssorok:
        v, old, n = r[si['vers']], r[si['oldal']], int(r[si['sorszam']])
        vesz = (hu_vesz if old == 'hu' else er_vesz).get((v, n))
        if not vesz:
            uj.append(r)
            continue
        regi = [int(x) for x in r[si['partner_sorszam']].split(',') if x]
        if not vesz <= set(regi):
            raise SystemExit('a törlendő partner nincs a szótáblában: %s %s %d %s' % (v, old, n, sorted(vesz)))
        marad = [x for x in regi if x not in vesz]
        r2 = list(r)
        r2[si['partner_sorszam']] = ','.join(str(x) for x in marad)
        if old == 'hu':
            r2[si['strong']] = hu_strong(er_strong[(v, x)] for x in marad)
            if not marad:
                r2[si['allapot']] = 'betoldas'
        elif not marad:
            r2[si['allapot']] = 'forditatlan'
        uj.append(r2)
    return uj


def general(cel):
    os.makedirs(cel, exist_ok=True)
    torol_mind, megtart = torlolista()
    h = hashlib.sha256(torlolista_bajtok(torol_mind)).hexdigest()
    for kv in konyvek():
        pprov, pfej, psorok, pnyers = tabla_olvas(os.path.join(FORRAS, 'parok_%s.tsv' % kv))
        sprov, sfej, ssorok, _ = tabla_olvas(os.path.join(FORRAS, 'szavak_%s.tsv' % kv))
        pi, dontesek, _ = konyv_dontes(kv)
        torolt = set()
        marad = []
        for r, ny, ok in dontesek:
            if ok is None:
                torolt.add((r[pi['vers']], int(r[pi['hu_sorszam']]), int(r[pi['er_sorszam']])))
            else:
                marad.append(ny)
        jel = ('# GENERÁLT: eszkozok/karoli_strong/konvencio_egysegesites.py — 1.1 (konvenció-egységesítés: a névelő- '
               'és ʾet-kapcsolatok törlése a megtartó lista kivételével) | torlolista_sha256=%s | az 1.0 proveniencia-'
               'sora: ' % h)
        with open(os.path.join(cel, 'parok_%s.tsv' % kv), 'w', encoding='utf-8', newline='') as f:
            f.write(jel + pprov.lstrip('# ') + '\n' + '\t'.join(pfej) + '\n' + ''.join(s + '\n' for s in marad))
        uj = szavak_szukit(sfej, ssorok, torolt)
        with open(os.path.join(cel, 'szavak_%s.tsv' % kv), 'w', encoding='utf-8', newline='') as f:
            f.write(jel + sprov.lstrip('# ') + '\n' + '\t'.join(sfej) + '\n' + ''.join('\t'.join(s) + '\n' for s in uj))
    with open(os.path.join(cel, 'torolt_kapcsolatok.tsv'), 'wb') as f:
        f.write(torlolista_bajtok(torol_mind))
    with open(os.path.join(cel, 'ismert_hiba_onallo_az.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(TORLO_FEJ + ['kovetkezo_szo']) + '\n')
        for s in megtart:
            if s[6] == 'onallo_az':
                f.write('\t'.join(s[:6] + [s[7]]) + '\n')
    print('1.1 előállítva: %s · törölt kapcsolat: %d · torlolista_sha256=%s' % (cel, len(torol_mind), h))
    return ellenoriz(cel)


def ellenoriz(cel):
    """Az 1.1 (cel) és az 1.0 (FORRAS) összevetése. Visszaad: hibák száma."""
    hibak = []
    torol, _ = torlolista()
    vart_torolt = set((s[0], int(s[1]), int(s[3])) for s in torol)
    talalt_torolt = set()
    osszes_10 = osszes_11 = 0
    for kv in konyvek():
        _, pfej, _, n10 = tabla_olvas(os.path.join(FORRAS, 'parok_%s.tsv' % kv))
        _, pfej11, _, n11 = tabla_olvas(os.path.join(cel, 'parok_%s.tsv' % kv))
        if pfej11 != pfej:
            hibak.append('parok_%s: a fejléc eltér' % kv)
        pi = {k: i for i, k in enumerate(pfej)}
        osszes_10 += len(n10)
        osszes_11 += len(n11)
        # részhalmaz, sorrendtartó, bájtra azonos sorok
        j = 0
        for ny in n10:
            if j < len(n11) and n11[j] == ny:
                j += 1
                continue
            r = ny.split('\t')
            talalt_torolt.add((r[pi['vers']], int(r[pi['hu_sorszam']]), int(r[pi['er_sorszam']])))
            if r[pi['strong']] not in CEL_STRONG:
                hibak.append('parok_%s: nem névelő/ʾet sor tűnt el: %s' % (kv, ny[:80]))
        if j != len(n11):
            hibak.append('parok_%s: az 1.1-ben az 1.0-ban nem szereplő vagy átrendezett sor áll (%d/%d)' % (kv, j, len(n11)))
        # szótábla: minden token egyszer, szimmetrikus partnerség a pártáblával, a hu strong levezethető
        _, sfej, s10, _ = tabla_olvas(os.path.join(FORRAS, 'szavak_%s.tsv' % kv))
        _, sfej11, s11, _ = tabla_olvas(os.path.join(cel, 'szavak_%s.tsv' % kv))
        si = {k: i for i, k in enumerate(sfej)}
        if sfej11 != sfej or len(s10) != len(s11):
            hibak.append('szavak_%s: fejléc vagy sorszám eltér' % kv)
            continue
        par11 = collections.defaultdict(set)
        er11 = collections.defaultdict(set)
        for ny in n11:
            r = ny.split('\t')
            v, h, e = r[pi['vers']], int(r[pi['hu_sorszam']]), int(r[pi['er_sorszam']])
            par11[(v, h)].add(e)
            er11[(v, e)].add(h)
        er_strong = {(r[si['vers']], int(r[si['sorszam']])): r[si['strong']] for r in s11 if r[si['oldal']] == 'er'}
        for a, b in zip(s10, s11):
            kulcs_a = (a[si['vers']], a[si['oldal']], a[si['sorszam']], a[si['szo']])
            kulcs_b = (b[si['vers']], b[si['oldal']], b[si['sorszam']], b[si['szo']])
            if kulcs_a != kulcs_b:
                hibak.append('szavak_%s: a tokensor eltér: %s' % (kv, kulcs_a))
                continue
            for mezo in ('bizonyossag', 'forras'):
                if a[si[mezo]] != b[si[mezo]]:
                    hibak.append('szavak_%s: %s változott: %s' % (kv, mezo, kulcs_a))
            v, old, n = b[si['vers']], b[si['oldal']], int(b[si['sorszam']])
            p = sorted(int(x) for x in b[si['partner_sorszam']].split(',') if x)
            vart = sorted((par11 if old == 'hu' else er11).get((v, n), ()))
            if a[si['allapot']] in ('fuggoben',):
                if b != a:
                    hibak.append('szavak_%s: függőben lévő token változott: %s' % (kv, kulcs_a))
                continue
            if p != vart:
                hibak.append('szavak_%s: partnerlista ≠ pártábla: %s %s %s' % (kv, kulcs_a, p, vart))
            p10 = set(int(x) for x in a[si['partner_sorszam']].split(',') if x)
            if not set(p) <= p10:
                hibak.append('szavak_%s: új partner: %s' % (kv, kulcs_a))
            if old == 'hu':
                if b[si['strong']] != hu_strong(er_strong[(v, x)] for x in p):
                    hibak.append('szavak_%s: a hu strong nem a partnerekből vezethető le: %s' % (kv, kulcs_a))
                vart_all = 'parositva' if p else ('betoldas' if a[si['allapot']] in ('parositva', 'betoldas') else a[si['allapot']])
            else:
                if b[si['strong']] != a[si['strong']]:
                    hibak.append('szavak_%s: az er strong változott: %s' % (kv, kulcs_a))
                vart_all = 'parositva' if p else 'forditatlan'
            if b[si['allapot']] != vart_all:
                hibak.append('szavak_%s: állapot %s, várt %s: %s' % (kv, b[si['allapot']], vart_all, kulcs_a))
            if not p10 - set(p) and b != a:
                hibak.append('szavak_%s: érintetlen token változott: %s' % (kv, kulcs_a))
    if talalt_torolt != vart_torolt:
        hibak.append('a törölt sorok halmaza ≠ törlőlista (%d vs %d)' % (len(talalt_torolt), len(vart_torolt)))
    if osszes_10 - osszes_11 != len(vart_torolt):
        hibak.append('párszám: %d − %d ≠ %d' % (osszes_10, osszes_11, len(vart_torolt)))
    tl = os.path.join(cel, 'torolt_kapcsolatok.tsv')
    if not os.path.exists(tl) or open(tl, 'rb').read() != torlolista_bajtok(torol):
        hibak.append('a torolt_kapcsolatok.tsv nem a kanonikus törlőlista')
    for hb in hibak[:40]:
        print('HIBA:', hb)
    print('ellenőrzés: 1.0 pár %d → 1.1 pár %d (törölt %d) · %d hiba' % (osszes_10, osszes_11, osszes_10 - osszes_11,
                                                                          len(hibak)))
    return len(hibak)


# --- felmérés a letétbe -------------------------------------------------------------------------------------------

def karoli_versek():
    ki = {}
    with open(KAROLI, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) >= 2:
                ki[m[0]] = m[1]
    return ki


def felmeres(letet):
    os.makedirs(letet, exist_ok=True)
    torol, megtart = torlolista()
    # er-tokenek száma és a hu-oldali partnerek (a törlés utáni maradék a mintához)
    er_ossz = collections.Counter()
    hu_partner = {}
    er_info = {}
    for kv in konyvek():
        _, sfej, ssorok, _ = tabla_olvas(os.path.join(FORRAS, 'szavak_%s.tsv' % kv))
        si = {k: i for i, k in enumerate(sfej)}
        for r in ssorok:
            if r[si['oldal']] == 'er':
                er_info[(r[si['vers']], r[si['sorszam']])] = (r[si['szo']], r[si['strong']])
                if r[si['strong']] in CEL_STRONG:
                    er_ossz[r[si['strong']]] += 1
            else:
                hu_partner[(r[si['vers']], r[si['sorszam']])] = r[si['partner_sorszam']]
    torolt_kulcs = set((s[0], s[1], s[3]) for s in torol)

    tip = collections.defaultdict(collections.Counter)
    for s in torol:
        tip[s[2].lower()][s[5]] += 1
    sorrend = sorted(tip, key=lambda w: (-sum(tip[w].values()), w))
    ossz = len(torol)
    kum = 0
    lefedo = set()
    with open(os.path.join(letet, 'torlendo_tipusok.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['rang', 'hu_szo', 'db', 'H9009', 'G3588', 'H0853', 'kum_arany', 'a_95_szazalekban']) + '\n')
        for i, w in enumerate(sorrend, 1):
            n = sum(tip[w].values())
            benne = kum < LEFEDES * ossz
            kum += n
            if benne:
                lefedo.add(w)
            f.write('\t'.join([str(i), w, str(n), str(tip[w]['H9009']), str(tip[w]['G3588']), str(tip[w]['H0853']),
                               '%.4f' % (kum / ossz), 'igen' if benne else 'nem']) + '\n')

    mt = collections.defaultdict(collections.Counter)
    for s in megtart:
        mt[(s[6], s[2].lower())][s[5]] += 1
    with open(os.path.join(letet, 'megtartott_tipusok.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['megtartas_oka', 'hu_szo', 'db', 'H9009', 'G3588', 'H0853']) + '\n')
        for (ok, w) in sorted(mt, key=lambda k: (k[0], -sum(mt[k].values()), k[1])):
            c = mt[(ok, w)]
            f.write('\t'.join([ok, w, str(sum(c.values())), str(c['H9009']), str(c['G3588']), str(c['H0853'])]) + '\n')

    versek = karoli_versek()
    maradek = [s for s in torol if s[2].lower() not in lefedo]
    rnd = random.Random(MAG)
    valasztott = sorted(rnd.sample(range(len(maradek)), min(MARADEK_DB, len(maradek))))

    def masik(s):
        p = [x for x in hu_partner.get((s[0], s[1]), '').split(',') if x and (s[0], s[1], x) not in torolt_kulcs]
        return ', '.join('%s %s' % er_info.get((s[0], x), ('?', '?')) for x in p) or '(nincs: betoldás lesz)'

    with open(os.path.join(letet, 'maradek_50.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['n', 'vers', 'hu_sorszam', 'hu_szo', 'er_szo', 'strong', 'a_magyar_szo_tobbi_partnere_1_1',
                           'karoli_vers', 'jogos_par (igen/nem)']) + '\n')
        for n, i in enumerate(valasztott, 1):
            s = maradek[i]
            f.write('\t'.join([str(n), s[0], s[1], s[2], s[4], s[5], masik(s), versek.get(s[0], '?'), '']) + '\n')

    # összefoglaló
    st_torol = collections.Counter(s[5] for s in torol)
    st_megt = collections.Counter(s[5] for s in megtart)
    ok_megt = collections.Counter(s[6] for s in megtart)
    az_mag = collections.Counter()
    for s in megtart:
        if s[6] == 'onallo_az':
            az_mag['magánhangzó előtt' if s[7][:1].lower() in 'aáeéiíoóöőuúüű' else 'mássalhangzó előtt / versvég'] += 1
    h = torlolista_hash(torol)
    with open(os.path.join(letet, 'OSSZEFOGLALO.md'), 'w', encoding='utf-8', newline='') as f:
        f.write('# Konvenció-egységesítés (1.1) — felmérés a felhasználói átnézéshez\n\n')
        f.write('Letétanyag, a repóba nem kerül. Előállítva: `eszkozok/karoli_strong/konvencio_egysegesites.py '
                '--felmeres`. A törlőlista SHA-256-ja (még nem fagyasztott): `%s`.\n\n' % h)
        f.write('| Strong | eredeti token az 1.0-ban | pár az 1.0-ban | törlendő | megmarad |\n|---|---:|---:|---:|---:|\n')
        for st in CEL_STRONG:
            f.write('| %s | %d | %d | %d | %d |\n' % (st, er_ossz[st], st_torol[st] + st_megt[st], st_torol[st], st_megt[st]))
        f.write('| összesen | %d | %d | %d | %d |\n\n' % (sum(er_ossz.values()), len(torol) + len(megtart), len(torol),
                                                         len(megtart)))
        f.write('Megtartás oka: %s.\n\n' % ', '.join('%s %d' % kv for kv in sorted(ok_megt.items())))
        f.write('Az önálló „az” (megmarad, ismert-hiba lista): %s.\n\n' % ', '.join('%s %d' % kv for kv in sorted(az_mag.items())))
        f.write('Szótípus a törlendők között: %d; a 95%%-ot lefedő típus: %d; a maradék %d pár (%d típus), ebből '
                '%d véletlen tétel a `maradek_50.tsv`-ben (mag: `%s`).\n\n' % (len(tip), len(lefedo), len(maradek),
                                                                           len(tip) - len(lefedo), len(valasztott), MAG))
        f.write('Fájlok: `torlendo_tipusok.tsv` (minden törlendő típus, gyakoriság szerint; `a_95_szazalekban`), '
                '`megtartott_tipusok.tsv` (a megtartott kapcsolatok okonként), `maradek_50.tsv` (az utolsó oszlopba '
                'írható az ítélet).\n')
    print('felmérés: %s · törlendő %d, megtartott %d · típus %d, 95%%-ot lefedő %d · torlolista_sha256=%s'
          % (letet, len(torol), len(megtart), len(tip), len(lefedo), h))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--felmeres', action='store_true')
    g.add_argument('--general', metavar='DIR')
    g.add_argument('--ellenoriz', metavar='DIR')
    g.add_argument('--hash', action='store_true')
    ap.add_argument('--letet', default=LETET)
    a = ap.parse_args()
    if a.felmeres:
        felmeres(a.letet)
    elif a.general:
        sys.exit(1 if general(a.general) else 0)
    elif a.ellenoriz:
        sys.exit(1 if ellenoriz(a.ellenoriz) else 0)
    else:
        print(torlolista_hash())


if __name__ == '__main__':
    main()
