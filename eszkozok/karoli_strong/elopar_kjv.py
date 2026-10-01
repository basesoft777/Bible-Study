#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.66 — a KJV-szabály („nincs KJV-tag → forditatlan-jelölt”) külön mérése a szkriptes
előpárosításban (kísérlet, API nélkül), az arany v3 60 versén, rétegenként (R1–R4 + Összes).
Nem minősítés: a kimenet mért szám, döntési szabályhoz nem viszonyít.

Az elopar.py-t importálja (szótár, párosító, betöltés, kizárások); az elopar.py meglévő
kimeneteit (f21p/elopar_eredmeny.tsv, f21p/szotar_elopar.tsv, naplok/F21P_elopar.md) nem
írja. Nem használ modellválaszt, szótárt vagy aranyat a KJV-szabályhoz: az arany csak a mérés
mércéje; a szótár és a K-szabályok csak a B) változat (együttes előpárosítás) részei; a C
futásai csak a tájékoztató összevetésben szerepelnek.

KJV-SZABÁLY (egy vers, egy eredeti szó):
  0. KJV-sor: tokenek.kjv_tamapont_forras(igehely, forras) — 'teljes' (alap; F19,
     konkordancia/KJV_Strongs_teljes.tsv a Karoli_versmegfeleltetes.tsv KJV-oszlopával) vagy
     'regi' (Genesis/Exodus/Proverbs, csak kontroll az R1-en). A KJV-Strong-halmaz a sor
     {...} címkéiből áll (minden címke, az üres szavú {H0853} is).
     Ha nincs KJV-sor (None): a vers minden szava 'nincs_kjv_sor' — NEM 'nincs KJV-tag';
     a szabály ott nem alkalmazható. Okai: (a) ÚSZ: a megfeleltetési tábla csak az ÓSZ-t fedi
     (a teljes táblában van ÚSZ-sor, de Károli → KJV kulcs nincs); (b) ÓSZ-vers, amelynek a
     megfeleltetésben nincs 'fejezet:vers' alakú KJV-megfelelője (pl. Zsolt 22:32);
     (c) KJV-oldali adathiány (naplok/F19_hianyok.tsv: Mk 9:43, Lk 6:41, Lk 17:36).
  1. Normalizálás: minden Strong (a TAHOT/TAGNT- és a KJV-oldalon is) ^([HG])0*(\\d+)[a-zA-Z]?$
     → betű + négyjegyű szám (H430 = H0430 = H0430a → H0430). Más alak változatlan.
  2. Összetett Strong: a '+' mentén összetevőkre bontva (pl. G2532+G1473 = κἀγώ). A
     LEXIKÁLIS összetevők = az összetevők a KIZÁRÁSI LISTA nélkül.
  3. KIZÁRÁSI LISTA (nyelvtani Strongok, a K1/K8/K9 hatásköre; a KJV-ben eleve nincs rájuk
     Strong): minden H9xxx (STEPBible héber elő-/utórag: H9001/H9002 ve-, H9003–H9008
     elöljárók, H9009 névelő, H9010–H9013 ragok és -ah/nún), G3588 (görög névelő), G2532 (καί).
     Ha egy szónak nincs lexikális összetevője: 'kizart_nyelvtani' (a KJV-szabály nem dönt).
     A listán túl más funkciószó (pl. H0853, H0834, G1161) NINCS kizárva: a lista a K-szabályok
     duplázását zárja ki, nem a KJV-címkézés hiányait (ezt a hibaok-elemzés méri, l. lent).
  4. [nem TR] eredeti szó: 'nem_tr', nem dönt (mint az elopar.py párosítója).
  5. Különben: 'van_kjv_tag', ha legalább egy lexikális összetevő normalizált Strongja a vers
     KJV-Strong-halmazában van; 'nincs_kjv_tag' (= forditatlan-JELÖLT), ha egyik sincs.

DÖNTÉS:
  A) a KJV-szabály önállóan: minden 'nincs_kjv_tag' szó → forditatlan.
  B) a KJV-szabály az előpárosítással együtt: a 'nincs_kjv_tag' szó csak akkor forditatlan,
     ha az elopar.parosit() rá nem döntött (sem forditatlan [K1/K8/K9], sem link [szótár/K9]).
     A K-szabályok csak kizárási listás Strongokra döntenek, ezért a B) az A)-tól csak a
     szótári / K9-linkkel ütköző szavakban tér el (az ütközés külön sor).
  A kombinált előpárosítás = az elopar.py döntései + a B) forditatlan-döntései.

MÉRÉS (az arany v3: LF-normalizált sha256, elopar.betolt; f21p/meres_kizaras.tsv kizárásai
mindkét oldalon): pontosság = a forditatlan-döntések hányada forditatlan az aranyban (Wilson
90%, meres.wilson, szószintű, optimista); fedés = az arany forditatlan-szavainak hány %-át
dönti el a szabály (három nevezővel: a réteg összes arany forditatlan-szava; a KJV-sorral
rendelkező versekben; ugyanott a nem kizárt, lexikális szavak). Versszámozás-gyanú (arany
nélkül): a vers JÓL CÍMKÉZETT Strongjai (korpusz-szintű KJV-címkézési arány >= 50%, n >= 5;
legalább 2 ilyen) közül kevesebb mint fele van a KJV-sorban; érzékenységi sor: az A) a gyanús
versek nélkül. Hibaok (gépi besorolás, első illő): versszámozás-gyanú;
ritkán címkézett Strong (a korpuszban a Strong KJV-címkézési aránya < 50%, n >= 5 vers; az
arány a teljes ÓSZ-en számolva: a KJV-sorral rendelkező versek közül, amelyekben a Strong a
TAHOT-ban szerepel, hányban van a KJV-címkék között; arany nélkül); más Strong a KJV-sorban
(a KJV-sornak van olyan Strongja, amely a vers eredetijében nincs); egyéb (kihagyott címke,
többszavas kifejezés). C-összevetés (tájékoztató, F3V2/F3V2B/F3V3): a C igent mond egy
forditatlan-döntésre, ha a szó a C forditatlan-listájában van (csak a C-ben kapun átment
versek); a C pontossága = a C igen/nem válasza egyezik az arannyal.

Használat:
    python eszkozok/karoli_strong/elopar_kjv.py            (mérés -> f21p/elopar_kjv_eredmeny.tsv,
                                                            naplok/F21P_elopar_kjv.md)
    python eszkozok/karoli_strong/elopar_kjv.py --onteszt  (mock-önteszt, nem ír a repóba)
"""

import os
import re
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import elopar  # noqa: E402
import meres  # noqa: E402
import tokenek  # noqa: E402

EREDMENY_UT = os.path.join(meres.F21P, 'elopar_kjv_eredmeny.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_elopar_kjv.md')
RETEGEK = elopar.RETEGEK
C_FUTASOK = elopar.C_FUTASOK
KIZART_G = {'G3588', 'G2532'}
RITKA_ARANY = 0.5
RITKA_MIN_N = 5
VERSSZAM_ARANY = 0.5
F19_HIANY_VERSEK = ('Mk 9:43', 'Lk 6:41', 'Lk 17:36')

_NORM = re.compile(r'^([HG])0*(\d+)[a-zA-Z]?$')
_CIMKE = re.compile(r'\{([^{}]+)\}')

ALLAPOTOK = ('nincs_kjv_sor', 'nem_tr', 'kizart_nyelvtani', 'van_kjv_tag', 'nincs_kjv_tag')


# ---------------------------------------------------------------------------
# a szabály
# ---------------------------------------------------------------------------

def normal(s):
    """'H430' / 'H0430' / 'H0430a' -> 'H0430'; más alak változatlan (strip után)."""
    s = s.strip()
    m = _NORM.match(s)
    return '%s%04d' % (m.group(1), int(m.group(2))) if m else s


def kizart_osszetevo(s):
    s = normal(s)
    return s.startswith('H9') or s in KIZART_G


def lexikalis(strong):
    """A '+' menti összetevők a kizárási lista nélkül, normalizálva."""
    return [normal(c) for c in strong.split('+') if c.strip() and not kizart_osszetevo(c)]


def kjv_halmaz(sor):
    """A KJV-támpont szövegéből ('word{H0430} {H0853} ...') a normalizált Strong-halmaz;
    None-ra None (nincs KJV-sor)."""
    if sor is None:
        return None
    ki = set()
    for c in _CIMKE.findall(sor):
        for s in c.split('+'):
            if s.strip():
                ki.add(normal(s))
    return ki


def kjv_szabaly(ew, kh):
    """{sorsz: állapot}; kh: a vers KJV-Strong-halmaza vagy None (nincs KJV-sor)."""
    ki = {}
    for w in ew:
        e = w['sorsz']
        if kh is None:
            ki[e] = 'nincs_kjv_sor'
        elif w['nem_tr']:
            ki[e] = 'nem_tr'
        else:
            lex = lexikalis(w['strong'])
            if not lex:
                ki[e] = 'kizart_nyelvtani'
            elif any(s in kh for s in lex):
                ki[e] = 'van_kjv_tag'
            else:
                ki[e] = 'nincs_kjv_tag'
    return ki


def dontes_a(allapot):
    return {e for e, a in allapot.items() if a == 'nincs_kjv_tag'}


def dontes_b(allapot, p):
    """A B) változat: csak az elopar.parosit() által el nem döntött szavakra."""
    dontott = set(p['forditatlan']) | {e for _, e in p['linkek']}
    return {e for e in dontes_a(allapot) if e not in dontott}


def nincs_sor_ok(ig, adat_reteg):
    """A 'nincs KJV-sor' oka (tájékoztató)."""
    if adat_reteg == 'R4':
        return 'ÚSZ (a megfeleltetési tábla csak az ÓSZ-t fedi)'
    if ig in F19_HIANY_VERSEK:
        return 'KJV-oldali adathiány (F19_hianyok)'
    megf, _ = tokenek._kjv_megfeleltetes()
    m = megf.get(ig)
    if m is None or not re.match(r'^\d+:\d+$', m or ''):
        return 'nincs KJV-megfeleltetés (versszámozás)'
    return 'a KJV-vers nincs a táblában'


def tartalmi(ew, arany_tab):
    """A vers lexikális Strongjai közül a korpuszban jól címkézettek (arány >= 50%, n >= 5)."""
    ki = set()
    for w in ew:
        for s in lexikalis(w['strong']):
            a = arany_tab.get(s)
            if a and a[1] >= RITKA_MIN_N and a[0] / a[1] >= RITKA_ARANY:
                ki.add(s)
    return ki


def illeszkedes(ew, kh, arany_tab):
    """(a jól címkézett Strongokból a KJV-halmazban, összes jól címkézett)."""
    t = tartalmi(ew, arany_tab)
    return sum(1 for s in t if s in kh), len(t)


def versszam_gyanu(ew, kh, arany_tab):
    """Arany nélküli vizsgálat: a vers jól címkézett Strongjainak (>= 2) kevesebb mint fele van
    a KJV-sorban -> a megfeleltetett KJV-vers valószínűleg nem ugyanaz a vers."""
    if kh is None:
        return False
    t, n = illeszkedes(ew, kh, arany_tab)
    return n >= 2 and t / n < VERSSZAM_ARANY


def szomszed_illeszkedes(ig, ew, arany_tab):
    """[(eltolás, KJV-vers, talált, összes)] a megfeleltetett KJV-vers -1/0/+1 szomszédaira
    (ugyanabban a fejezetben; tájékoztató, a versszámozás-gyanú igazolására)."""
    megf, h2s = tokenek._kjv_megfeleltetes()
    m = megf.get(ig)
    b = tokenek.igehely_bont(ig)
    if not m or not re.match(r'^\d+:\d+$', m) or not b or b[0] not in h2s:
        return []
    c, v = (int(x) for x in m.split(':'))
    tab = tokenek._kjv_teljes_tabla()
    ki = []
    for d in (-1, 0, 1):
        sorok = tab.get('%s.%d.%d' % (h2s[b[0]], c, v + d))
        if not sorok:
            continue
        kh = {normal(s) for _, s in sorok}
        t, n = illeszkedes(ew, kh, arany_tab)
        ki.append((d, '%d:%d' % (c, v + d), t, n))
    return ki


# ---------------------------------------------------------------------------
# korpusz-szintű KJV-címkézési arány (arany nélkül, hibaok-besoroláshoz)
# ---------------------------------------------------------------------------

def cimkezesi_arany(karoli, ered):
    """{Strong: (hány versben van a KJV-címkék között, hány KJV-soros ÓSZ-versben szerepel)}."""
    van, ossz = Counter(), Counter()
    for ig in karoli:
        ew = ered.get(ig)
        if not ew or ew[0]['strong'].startswith('G'):
            continue
        kh = kjv_halmaz(tokenek.kjv_tamapont_forras(ig, 'teljes'))
        if kh is None:
            continue
        for s in {x for w in ew for x in lexikalis(w['strong'])}:
            ossz[s] += 1
            van[s] += s in kh
    return {s: (van[s], ossz[s]) for s in ossz}


def korpusz_gyanu(karoli, ered, arany_tab):
    """A versszámozás-gyanú a teljes ÓSZ-en (KJV-soros versek), a szomszéd-illeszkedéssel."""
    osztaly = {r[0]: r[3] for r in tokenek._sorok_versmegf() if len(r) > 3}
    ki = {'ossz': 0, 'gyanu': 0, 'szomszed': 0, 'konyv': Counter(), 'osztaly': Counter()}
    for ig in karoli:
        ew = ered.get(ig)
        if not ew or ew[0]['strong'].startswith('G'):
            continue
        kh = kjv_halmaz(tokenek.kjv_tamapont_forras(ig, 'teljes'))
        if kh is None:
            continue
        ki['ossz'] += 1
        if not versszam_gyanu(ew, kh, arany_tab):
            continue
        ki['gyanu'] += 1
        if any(d != 0 and n >= 2 and t / n >= VERSSZAM_ARANY for d, _, t, n in szomszed_illeszkedes(ig, ew, arany_tab)):
            ki['szomszed'] += 1
            ki['konyv'][tokenek.konyv_rovid(ig)] += 1
            ki['osztaly'][osztaly.get(ig)] += 1
    return ki


def hiba_ok(w, ew, kh, arany_tab):
    lex_vers = {x for v in ew for x in lexikalis(v['strong'])}
    if versszam_gyanu(ew, kh, arany_tab):
        return 'versszámozás-gyanú (a vers jól címkézett Strongjainak < 50%-a a KJV-sorban)'
    ar = [arany_tab.get(s) for s in lexikalis(w['strong'])]
    if ar and all(a is not None and a[1] >= RITKA_MIN_N and a[0] / a[1] < RITKA_ARANY for a in ar):
        return 'ritkán címkézett Strong (a KJV a korpuszban < 50%-ban címkézi)'
    if kh - lex_vers:
        return 'más Strong a KJV-sorban (a vers eredetijében nem szereplő KJV-címke)'
    return 'egyéb (kihagyott címke / többszavas kifejezés)'


# ---------------------------------------------------------------------------
# mérés
# ---------------------------------------------------------------------------

def szamol(adat, szotar, forras_versek, arany_tab):
    elopar.metszet_ellenoriz(forras_versek, adat.arany)
    versek = [ig for ig in adat.versek if ig in adat.arany]
    sorok = meres.Sorok()
    reszlet = {'versek': versek, 'per': {}, 'hibak': [], 'nincs_sor': [], 'regi': {}}
    for ig in versek:
        ew = adat.ered[ig]
        kt = tokenek.kjv_tamapont_forras(ig, 'teljes')
        kh = kjv_halmaz(kt)
        al = kjv_szabaly(ew, kh)
        p = elopar.parosit(tokenek.tokenizal(adat.karoli[ig]), ew, szotar)
        rk = None
        if adat.reteg[ig] == 'R1':
            rk = kjv_halmaz(tokenek.kjv_tamapont_forras(ig, 'regi'))
        gy = versszam_gyanu(ew, kh, arany_tab)
        reszlet['per'][ig] = {'kh': kh, 'al': al, 'p': p, 'A': dontes_a(al), 'B': dontes_b(al, p),
                              'A_ng': set() if gy else dontes_a(al), 'gyanu': gy,
                              'regi_kh': rk, 'regi_al': kjv_szabaly(ew, rk) if rk is not None else None}
        if kh is None:
            reszlet['nincs_sor'].append((ig, adat.reteg[ig], nincs_sor_ok(ig, adat.reteg[ig])))
    for ret in RETEGEK:
        vs = [ig for ig in versek if ret == meres.OSSZES or adat.reteg[ig] == ret]
        sz = Counter()
        for ig in vs:
            d = reszlet['per'][ig]
            g_lk, g_b, g_f = elopar.egysegek_arany(adat, ig)
            kotott = {e for _, e in g_lk}
            ered_ig = [w for w in adat.ered[ig] if (ig, w['sorsz']) not in adat.kizaras]
            van_sor = d['kh'] is not None
            sz['versek'] += 1
            sz['versek_kjv'] += van_sor
            sz['eredeti_szo'] += len(ered_ig)
            sz['arany_f'] += len(g_f)
            if van_sor:
                sz['eredeti_szo_kjv'] += len(ered_ig)
                sz['arany_f_kjv'] += len(g_f)
                if not d['gyanu']:
                    sz['versek_kjv_ng'] += 1
                    sz['arany_f_kjv_ng'] += len(g_f)
            for w in ered_ig:
                e = w['sorsz']
                a = d['al'][e]
                sz['all_' + a] += 1
                if van_sor and a in ('van_kjv_tag', 'nincs_kjv_tag'):
                    sz['arany_f_kjv_lex'] += e in g_f
                if a == 'nincs_kjv_tag':
                    sz['jelolt_arany_f'] += e in g_f
            for valt in ('A', 'B', 'A_ng'):
                for e in sorted(d[valt]):
                    if (ig, e) in adat.kizaras:
                        continue
                    jo = e in g_f
                    sz['%s_n' % valt] += 1
                    sz['%s_jo' % valt] += jo
                    sz['%s_kotott' % valt] += (not jo) and e in kotott
                    if valt == 'A' and not jo and ret == meres.OSSZES:
                        reszlet['hibak'].append((ig, e))
            # ütközés az előpárosítással (A, de az elopar döntött)
            p = d['p']
            lk_e = {e for _, e in p['linkek'] if (ig, e) not in adat.kizaras}
            for e in d['A']:
                if (ig, e) in adat.kizaras:
                    continue
                if e in lk_e:
                    sz['utk_link'] += 1
                    sz['utk_link_link_jo'] += any((k, e) in g_lk for k, ee in p['linkek'] if ee == e)
                    sz['utk_link_kjv_jo'] += e in g_f
                if e in p['forditatlan']:
                    sz['utk_f'] += 1
            # kombinált előpárosítás
            g_u = elopar.egyseg_halmaz(g_lk, g_b, g_f)
            sz['arany_egyseg'] += len(g_u)
            regi_u = elopar.szkript_egysegek(adat, ig, p)
            sz['elopar_n'] += len(regi_u)
            sz['elopar_jo'] += sum(1 for u, _, _ in regi_u if u in g_u)
            sz['elopar_F_jo'] += sum(1 for u, _, _ in regi_u if u[0] == 'F' and u in g_u)
            sz['elopar_F_n'] += sum(1 for u, _, _ in regi_u if u[0] == 'F')
            bu = [('F', e) for e in sorted(d['B']) if (ig, e) not in adat.kizaras]
            sz['komb_n'] += len(regi_u) + len(bu)
            sz['komb_jo'] += sum(1 for u, _, _ in regi_u if u in g_u) + sum(1 for u in bu if u in g_u)
            sz['komb_F_n'] += sum(1 for u, _, _ in regi_u if u[0] == 'F') + len(bu)
            sz['komb_F_jo'] += sum(1 for u, _, _ in regi_u if u[0] == 'F' and u in g_u) + sum(1 for u in bu if u in g_u)
            # C-összevetés az A-döntéseken
            for f in C_FUTASOK:
                c = elopar.egysegek_c(adat, f, ig)
                if c is None:
                    continue
                sz['c_%s_versek' % f] += 1
                c_f = c[2]
                for e in sorted(d['A']):
                    if (ig, e) in adat.kizaras:
                        continue
                    g = e in g_f
                    ci = e in c_f
                    kk = 'c_%s' % f
                    sz[kk + '_n'] += 1
                    sz[kk + '_kjv_jo'] += g
                    sz[kk + '_c_jo'] += (ci == g)
                    sz[kk + '_c_igen'] += ci
                    sz[kk + '_c_igen_jo'] += ci and g
            # régi tábla (R1 kontroll)
            if d['regi_al'] is not None:
                ja = dontes_a(d['al'])
                jr = dontes_a(d['regi_al'])
                for nev, h in (('regi', jr), ('teljes', ja), ('csak_regi', jr - ja), ('csak_teljes', ja - jr),
                               ('mindketto', ja & jr)):
                    h = {e for e in h if (ig, e) not in adat.kizaras}
                    sz['r_%s_n' % nev] += len(h)
                    sz['r_%s_jo' % nev] += sum(1 for e in h if e in g_f)
                sz['r_versek'] += 1
                sz['r_arany_f'] += len(g_f)
        S = 'KJV-szabály'
        add = sorok.add
        add('alap', S, ret, 'arany_versek', sz['versek'], None, 'a mérésben részt vevő aranyversek (rétegben)')
        add('alap', S, ret, 'versek_kjv_sorral (teljes tábla)', sz['versek_kjv'], sz['versek'],
            'a Károli → KJV megfeleltetéssel KJV-sort kapó versek')
        add('alap', S, ret, 'versek_nincs_kjv_sor', sz['versek'] - sz['versek_kjv'], sz['versek'],
            'itt a szabály nem alkalmazható (nincs KJV-sor, nem „nincs KJV-tag”)')
        add('alap', S, ret, 'eredeti_szo (kizárások nélkül)', sz['eredeti_szo'], None, '')
        add('alap', S, ret, 'eredeti_szo a KJV-soros versekben', sz['eredeti_szo_kjv'], sz['eredeti_szo'], '')
        for a in ALLAPOTOK:
            add('allapot', S, ret, 'állapot: %s' % a, sz['all_' + a], sz['eredeti_szo'],
                'eredeti szavak a KJV-szabály szerint')
        add('allapot', S, ret, 'jelolt_arany_szerint_forditatlan', sz['jelolt_arany_f'], sz['all_nincs_kjv_tag'],
            'a „nincs KJV-tag” jelöltekből forditatlan az aranyban (= A pontossága)', intervallum=True)
        for valt, cim in (('A', 'A) önállóan'), ('B', 'B) az előpárosítással együtt')):
            oss = 'KJV-szabály %s' % cim
            add('dontes', oss, ret, 'forditatlan_dontes', sz['%s_n' % valt], None, 'a KJV-szabály forditatlan-döntései')
            add('dontes', oss, ret, 'pontossag (döntés ∩ arany forditatlan / döntés)', sz['%s_jo' % valt],
                sz['%s_n' % valt], 'Wilson 90%, szószintű', intervallum=True)
            add('dontes', oss, ret, 'hibás döntés, az aranyban kötött (link)', sz['%s_kotott' % valt],
                sz['%s_n' % valt] - sz['%s_jo' % valt], 'a hibás döntésekből az aranyban magyar szóhoz kötött')
            add('dontes', oss, ret, 'fedes (az arany összes forditatlan-szavából)', sz['%s_jo' % valt], sz['arany_f'],
                'a réteg minden aranyverse; a KJV-sor nélküli versek arany forditatlan-szavai is a nevezőben',
                intervallum=True)
            add('dontes', oss, ret, 'fedes a KJV-soros versekben', sz['%s_jo' % valt], sz['arany_f_kjv'],
                'csak a KJV-sorral rendelkező versek arany forditatlan-szavai', intervallum=True)
            add('dontes', oss, ret, 'fedes a KJV-soros versek lexikális szavain', sz['%s_jo' % valt],
                sz['arany_f_kjv_lex'], 'a kizárási lista, a [nem TR] nélkül: amit a szabály elvben eldönthet',
                intervallum=True)
        oss = 'érzékenység: A) a versszámozás-gyanús versek nélkül'
        add('dontes', oss, ret, 'versek_kjv_sorral_gyanu_nelkul', sz['versek_kjv_ng'], sz['versek_kjv'],
            'arany nélküli vizsgálat: a vers jól címkézett Strongjainak >= 50%-a a KJV-sorban')
        add('dontes', oss, ret, 'forditatlan_dontes', sz['A_ng_n'], None, '')
        add('dontes', oss, ret, 'pontossag (döntés ∩ arany forditatlan / döntés)', sz['A_ng_jo'], sz['A_ng_n'],
            'Wilson 90%, szószintű', intervallum=True)
        add('dontes', oss, ret, 'fedes (az arany összes forditatlan-szavából)', sz['A_ng_jo'], sz['arany_f'], '',
            intervallum=True)
        add('dontes', oss, ret, 'fedes a nem gyanús KJV-soros versekben', sz['A_ng_jo'], sz['arany_f_kjv_ng'], '',
            intervallum=True)
        add('utkozes', S, ret, 'A-döntés, amelyet az előpárosítás linkként döntött el', sz['utk_link'], sz['A_n'],
            'szótár / K9-link ugyanarra az eredeti szóra (a B ezeket kihagyja)')
        add('utkozes', S, ret, 'ebből a link az aranyban', sz['utk_link_link_jo'], sz['utk_link'], '')
        add('utkozes', S, ret, 'ebből forditatlan az aranyban', sz['utk_link_kjv_jo'], sz['utk_link'], '')
        add('utkozes', S, ret, 'A-döntés, amelyet a K1/K8/K9 forditatlannak döntött', sz['utk_f'], sz['A_n'],
            'a kizárási lista miatt várhatóan 0')
        oss = 'előpárosítás (F21.60)'
        add('kombinalt', oss, ret, 'egyseg_lefedettseg', sz['elopar_jo'], sz['arany_egyseg'], 'az elopar.py döntései',
            intervallum=True)
        add('kombinalt', oss, ret, 'egyseg_pontossag', sz['elopar_jo'], sz['elopar_n'], '', intervallum=True)
        add('kombinalt', oss, ret, 'forditatlan_lefedettseg', sz['elopar_F_jo'], sz['arany_f'], '', intervallum=True)
        add('kombinalt', oss, ret, 'forditatlan_pontossag', sz['elopar_F_jo'], sz['elopar_F_n'], '', intervallum=True)
        oss = 'előpárosítás + KJV-szabály B)'
        add('kombinalt', oss, ret, 'egyseg_lefedettseg', sz['komb_jo'], sz['arany_egyseg'],
            'az elopar.py döntései + a B) forditatlan-döntései', intervallum=True)
        add('kombinalt', oss, ret, 'egyseg_pontossag', sz['komb_jo'], sz['komb_n'], '', intervallum=True)
        add('kombinalt', oss, ret, 'egyseg_dontott_arany', sz['komb_n'], sz['arany_egyseg'],
            'döntések száma (helyes és hibás) az arany egységszámához mérve')
        add('kombinalt', oss, ret, 'forditatlan_lefedettseg', sz['komb_F_jo'], sz['arany_f'], '', intervallum=True)
        add('kombinalt', oss, ret, 'forditatlan_pontossag', sz['komb_F_jo'], sz['komb_F_n'], '', intervallum=True)
        for f in C_FUTASOK:
            kk = 'c_%s' % f
            oss = '%s (az A-döntéseken)' % f
            add('c_osszevetes', oss, ret, 'versek_C_ok', sz[kk + '_versek'], sz['versek'], 'aranyversek, ahol a C kapun átment')
            add('c_osszevetes', oss, ret, 'KJV-szabály pontossága (ugyanezeken)', sz[kk + '_kjv_jo'], sz[kk + '_n'],
                '', intervallum=True)
            add('c_osszevetes', oss, ret, 'C pontossága (igen/nem egyezik az arannyal)', sz[kk + '_c_jo'], sz[kk + '_n'],
                'a C forditatlan-listája ezeken a szavakon', intervallum=True)
            add('c_osszevetes', oss, ret, 'C forditatlan-igen pontossága', sz[kk + '_c_igen_jo'], sz[kk + '_c_igen'],
                'ahol a C is forditatlannak jelöli', intervallum=True)
        if ret in ('R1', meres.OSSZES) and sz['r_versek']:
            for nev, cim in (('regi', 'régi tábla (Gen/Exo/Pro)'), ('teljes', 'teljes tábla (F19)'),
                             ('mindketto', 'mindkét tábla szerint jelölt'), ('csak_regi', 'csak a régi szerint'),
                             ('csak_teljes', 'csak a teljes szerint')):
                add('regi_teljes', 'R1-kontroll: %s' % cim, ret, '"nincs KJV-tag" jelölt (A-döntés)', sz['r_%s_n' % nev],
                    None, 'R1-versek: %d' % sz['r_versek'])
                add('regi_teljes', 'R1-kontroll: %s' % cim, ret, 'pontossag', sz['r_%s_jo' % nev], sz['r_%s_n' % nev], '',
                    intervallum=True)
                add('regi_teljes', 'R1-kontroll: %s' % cim, ret, 'fedes', sz['r_%s_jo' % nev], sz['r_arany_f'], '',
                    intervallum=True)
    return sorok, reszlet


# ---------------------------------------------------------------------------
# kiírás
# ---------------------------------------------------------------------------

def fejlec(info, ts, kjv_id):
    return ('# GENERÁLT: eszkozok/karoli_strong/elopar_kjv.py | scope=f21p, a KJV-szabály ("nincs KJV-tag → '
            'forditatlan-jelölt") mérése (kísérlet) az arany v3 60 versén, rétegenként (f21p/minta.tsv); A) '
            'önállóan, B) az előpárosítással együtt; R1-kontroll a régi táblával; C-összevetés: %s | '
            'forras=%s (sha256 %s), konkordancia/KJV_Strongs_{Genesis,Exodus,Proverbs}.tsv, '
            'konkordancia/Karoli_versmegfeleltetes.tsv, f21p/arany_opus_v3.jsonl (sha256 %s; csak mérce), '
            'f21p/meres_kizaras.tsv, f21p/minta.tsv, f21p/szotar_elopar.tsv (csak B), f21p/valaszok/F3V2.jsonl, '
            'F3V2B.jsonl, F3V3.jsonl (csak C-összevetés), konkordancia/Karoli_1908.tsv, TAHOT_kivonat.tsv, '
            'TAGNT_kivonat.tsv | ts=%s | kísérlet, nem minősítés a döntési szabály szerint; kézzel szerkeszteni tilos'
            % (', '.join(C_FUTASOK), kjv_id[0], kjv_id[1], info['sha256'], ts))


def tsv_ir(sorok, fej, ut=EREDMENY_UT):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + '\n')
        f.write('\t'.join(meres.OSZLOPOK) + '\n')
        for r in sorok.lista:
            f.write('\t'.join(meres._fmt(r[k]).replace('\t', ' ') for k in meres.OSZLOPOK) + '\n')


def _w_leir(w):
    return '#%d %s %s [%s]' % (w['sorsz'], w['alak'], w['strong'], w['tukor'])


def md_ir(sorok, fej, adat, reszlet, arany_tab, ut=JELENTES_UT):
    tab = elopar._tabla
    ki = ['# F21P_elopar_kjv.md — a KJV-szabály mérése a szkriptes előpárosításban (kísérlet)', '',
          '<!-- %s -->' % fej.lstrip('# '), '',
          '**Kísérlet, nem minősítés a döntési szabály szerint.** A számok a szkript kimenetei '
          '(f21p/elopar_kjv_eredmeny.tsv); küszöbhöz nem viszonyítanak, ajánlást nem tartalmaznak. '
          'Cellaforma: érték% (számláló/nevező) [90%-os Wilson-intervallum, szószintű, a versen belüli '
          'összefüggést nem kezeli, tehát optimista]. A 60 vers rétegenként kicsi (R1 20, R2 10, R3 10, R4 20): '
          'nézd a nevezőt.', '',
          '## A KJV-szabály algoritmusa', '',
          '1. **KJV-sor:** `tokenek.kjv_tamapont_forras(igehely, "teljes")` — a `konkordancia/KJV_Strongs_teljes.tsv` '
          '(F19) sora a `Karoli_versmegfeleltetes.tsv` KJV-oszlopa szerinti versre. A vers KJV-Strong-halmaza a sor '
          'összes `{...}` címkéje. Ha nincs KJV-sor, a vers minden szava **„nincs KJV-sor”** (nem „nincs KJV-tag”): a '
          'szabály ott nem alkalmazható.',
          '2. **Normalizálás:** minden Strong `^([HG])0*(\\d+)[a-zA-Z]?$` → betű + négyjegyű szám (H430 = H0430 = H0430a).',
          '3. **Összetett Strong:** a `+` mentén összetevőkre bontva; a **lexikális összetevők** = az összetevők a '
          'kizárási lista nélkül (pl. G2532+G1473 κἀγώ → G1473).',
          '4. **Kizárási lista** (a K1/K8/K9 hatásköre; a KJV-ben eleve nincs rájuk Strong): **minden H9xxx** '
          '(STEPBible héber elő-/utórag: H9001/H9002 ve-, H9003–H9008 elöljárók, H9009 névelő, H9010–H9013), '
          '**G3588** (görög névelő), **G2532** (καί). Lexikális összetevő nélküli szó: „kizárt (nyelvtani)”, a szabály '
          'nem dönt. Más funkciószó (H0853, H0834, G1161 …) nincs kizárva: a lista a K-szabályok duplázását zárja ki, '
          'nem a KJV-címkézés hiányait — ezek hatását a hibaok-elemzés méri.',
          '5. **[nem TR]** eredeti szó: nem dönt (mint az elopar.py).',
          '6. Különben **„van KJV-tag”**, ha legalább egy lexikális összetevő a KJV-halmazban van; **„nincs KJV-tag”** '
          '(forditatlan-jelölt), ha egyik sincs.', '',
          '**Döntés.** *A) önállóan:* minden „nincs KJV-tag” szó → `forditatlan`. *B) az előpárosítással együtt:* csak '
          'ha az `elopar.parosit()` arra a szóra nem döntött (sem K1/K8/K9-forditatlan, sem szótári / K9-link). A '
          'K-szabályok csak kizárási listás Strongokra döntenek, ezért a B) az A)-tól csak a szótári/K9-linkkel '
          'ütköző szavakban tér el. A KJV-szabály szótárt, modellválaszt és aranyat nem használ; az arany csak a mérce.', '']
    ki += ['## Alapadat és a szavak állapota', ''] + tab(sorok, 'alap') + tab(sorok, 'allapot')
    ki += ['### A KJV-sor nélküli aranyversek', '', '| vers | réteg | ok |', '|---|---|---|']
    for ig, r, ok in reszlet['nincs_sor']:
        ki.append('| %s | %s | %s |' % (ig, r, ok))
    hv = [v for v in F19_HIANY_VERSEK if v in adat.arany]
    ki += ['', 'A F19 KJV-oldali adathiány-versei (%s) közül az aranyban: %s.'
           % (', '.join(F19_HIANY_VERSEK), ', '.join(hv) if hv else 'egy sincs'), '']
    ki += ['### Versszámozás-gyanús versek (KJV-sor van, de valószínűleg nem a megfelelő vers)', '',
           'Arany nélküli vizsgálat: a vers *jól címkézett* Strongjai (a korpuszban a KJV legalább 50%-ban címkézi, '
           'n >= 5) közül kevesebb mint fele van a megfeleltetett KJV-vers címkéi között. Az oszlopok a megfeleltetett '
           'KJV-vers (0) és a fejezeten belüli szomszédai (-1, +1) illeszkedését mutatják (talált/összes jól címkézett '
           'Strong). A KJV-szám a `Karoli_versmegfeleltetes.tsv` igehely_kjv oszlopa.', '',
           '| vers | réteg | megfeleltetett KJV-vers | -1 | 0 | +1 | „nincs KJV-tag” jelölt |', '|---|---|---|---|---|---|---|']
    n_gy = 0
    for ig in reszlet['versek']:
        d = reszlet['per'][ig]
        if not d['gyanu']:
            continue
        n_gy += 1
        sz_ = {x[0]: '%s: %d/%d' % (x[1], x[2], x[3]) for x in szomszed_illeszkedes(ig, adat.ered[ig], arany_tab)}
        megf = tokenek._kjv_megfeleltetes()[0].get(ig)
        ki.append('| %s | %s | %s | %s | %s | %s | %d |' % (ig, adat.reteg[ig], megf, sz_.get(-1, '—'), sz_.get(0, '—'),
                                                         sz_.get(1, '—'), len(d['A'])))
    if not n_gy:
        ki.append('| (nincs) | | | | | | |')
    kg = reszlet.get('korpusz_gyanu')
    if kg:
        ki += ['', 'Ugyanez a vizsgálat a teljes ÓSZ-en (tájékoztató, arany nélkül): %d KJV-soros ÓSZ-versből %d '
               'versszámozás-gyanús; ebből %d-nál egy fejezeten belüli szomszédos KJV-vers (-1/+1) illeszkedik '
               '(>= 50%%). Könyvenként: %s. A megfeleltetési tábla osztálya (osztaly) ezeknél: %s.'
               % (kg['ossz'], kg['gyanu'], kg['szomszed'],
                  ', '.join('%s %d' % x for x in sorted(kg['konyv'].items(), key=lambda x: (-x[1], x[0]))),
                  ', '.join('%s %d' % x for x in sorted(kg['osztaly'].items(), key=lambda x: (-x[1], str(x[0])))))]
    ki += ['']
    ki += ['## Döntések, pontosság, fedés (A és B)', ''] + tab(sorok, 'dontes')
    ki += ['## Ütközés az előpárosítással', ''] + tab(sorok, 'utkozes')
    ki += ['## Kombinált előpárosítás (az F21.60 előpárosítás + a B) döntései)', '',
           'Az előpárosítás sorai az F21P_elopar.md számait ismétlik (166/1335 egység; 1,1% link-fedés); '
           'a KJV-szabály csak forditatlan-döntést ad, a link-fedést nem változtatja.', ''] + tab(sorok, 'kombinalt')
    ki += ['## R1-kontroll: régi (Genesis/Exodus/Proverbs) és teljes tábla', '',
           'A régi tábla frázisokat és üres szavú {H0853}-elemeket is tartalmaz, a teljes (eBible) szó-szintű és a '
           'H0853-at szinte sosem címkézi; a két forrás „nincs KJV-tag” jelöltjeinek különbsége a forma hatása.', '']
    ki += tab(sorok, 'regi_teljes')
    kul_r, kul_t = Counter(), Counter()
    for ig in reszlet['versek']:
        d = reszlet['per'][ig]
        if d['regi_al'] is None:
            continue
        ew = adat.ered[ig]
        ja, jr = dontes_a(d['al']), dontes_a(d['regi_al'])
        for e in jr - ja:
            if (ig, e) not in adat.kizaras:
                kul_r[ew[e - 1]['strong']] += 1
        for e in ja - jr:
            if (ig, e) not in adat.kizaras:
                kul_t[ew[e - 1]['strong']] += 1
    ki += ['A különbség Strongonként: csak a régi szerint jelölt: ' +
           (', '.join('%s (%d)' % x for x in sorted(kul_r.items(), key=lambda x: (-x[1], x[0]))) or '—') +
           '; csak a teljes szerint jelölt: ' +
           (', '.join('%s (%d)' % x for x in sorted(kul_t.items(), key=lambda x: (-x[1], x[0]))) or '—') + '.', '']
    ki += ['## C-összevetés ugyanezeken a döntéseken (tájékoztató)', '',
           'Az A) döntéseken: a C igent mond, ha a szó a C `forditatlan`-listájában van (csak a C-ben kapun átment '
           'aranyversek). A C pontossága: a C igen/nem válasza egyezik az arannyal.', ''] + tab(sorok, 'c_osszevetes')
    # hibák
    hibak = reszlet['hibak']
    okok = Counter()
    strongok = Counter()
    sorlista = []
    for ig, e in hibak:
        d = reszlet['per'][ig]
        ew = adat.ered[ig]
        w = ew[e - 1]
        ok = hiba_ok(w, ew, d['kh'], arany_tab)
        okok[ok] += 1
        strongok[w['strong']] += 1
        sorlista.append((ig, w, ok))
    ki += ['## Hibás KJV-döntések (A, összes réteg): forditatlan a szabály szerint, de az aranyban nem', '',
           'Összesen %d. Gépi okbesorolás (első illő; a definíció a szkript docstringjében):' % len(hibak), '',
           '| ok | R1 | R2 | R3 | R4 | összes |', '|---|---|---|---|---|---|']
    ok_ret = Counter((ok, adat.reteg[ig]) for ig, w, ok in sorlista)
    for ok, db in sorted(okok.items(), key=lambda x: (-x[1], x[0])):
        ki.append('| %s | %s | %d |' % (ok, ' | '.join(str(ok_ret[(ok, r)]) for r in meres.RETEGEK), db))
    helyes = Counter()
    for ig in reszlet['versek']:
        _, _, g_f = elopar.egysegek_arany(adat, ig)
        for e in reszlet['per'][ig]['A']:
            if e in g_f and (ig, e) not in adat.kizaras:
                helyes[(adat.ered[ig][e - 1]['strong'], adat.reteg[ig])] += 1
    hs = Counter()
    for (s, r), db in helyes.items():
        hs[s] += db
    ki += ['', 'A helyes A-döntések Strongonként: ' +
           (', '.join('%s %d (%s)' % (s, db, ', '.join('%s %d' % (r, helyes[(s, r)]) for r in meres.RETEGEK
                                                      if helyes[(s, r)]))
                      for s, db in sorted(hs.items(), key=lambda x: (-x[1], x[0]))) or '—') + '.']
    ki += ['', 'Leggyakoribb Strongok a hibákban: ' +
           ', '.join('%s (%d)' % x for x in sorted(strongok.items(), key=lambda x: (-x[1], x[0]))[:15]) + '.', '',
           '### Példák (versrendben, okonként legfeljebb 5, összesen legfeljebb 15)', '',
           '| vers | eredeti szó | az aranyban (magyar) | KJV-címkézési arány (korpusz) | a KJV-sor a versben nem illeszkedő címkéi | ok |',
           '|---|---|---|---|---|---|']
    per_ok = Counter()
    pelda = []
    for ig, w, ok in sorlista:
        if per_ok[ok] >= 5 or len(pelda) >= 15:
            continue
        per_ok[ok] += 1
        pelda.append((ig, w, ok))
    for ig, w, ok in sorted(pelda, key=lambda x: (reszlet['versek'].index(x[0]), x[1]['sorsz'])):
        d = reszlet['per'][ig]
        tl = tokenek.tokenizal(adat.karoli[ig])
        g_lk = adat.arany_linkek(ig)
        mg = ', '.join('%d %s' % (k, tl[k - 1]) for k, ee in sorted(g_lk) if ee == w['sorsz']) or '—'
        ar = ['%s %d/%d' % (s, arany_tab[s][0], arany_tab[s][1]) if s in arany_tab else '%s —' % s
              for s in lexikalis(w['strong'])]
        lex_vers = {x for v in adat.ered[ig] for x in lexikalis(v['strong'])}
        nem_ill = ' '.join(sorted(d['kh'] - lex_vers)) or '—'
        ki.append('| %s | %s | %s | %s | %s | %s |' % (ig, _w_leir(w).replace('|', '/'), mg, ', '.join(ar), nem_ill, ok))
    ki += ['', '## Nyitott kérdések (a kísérlet korlátai, nem döntés)', '',
           '- A versszámozás-gyanús versek (fent) a KJV-sor forrását érintik, nem a szabályt: ahol a megfeleltetett '
           'KJV-vers helyett a szomszédos illeszkedik, ott a `Karoli_versmegfeleltetes.tsv` igehely_kjv oszlopa (és így a '
           '`tokenek.kjv_tamapont_teljes`) más verset ad. Ugyanez a KJV-sor megy a C-nek a KJV-támponttal futó '
           'változatokban; a javítás nem e mérés hatásköre (a tábla és a tokenek.py nem része a feladatnak).',
           '- Az R4-ben (és a Zsolt 22:32-ben) nincs KJV-sor: a teljes táblában van ÚSZ-adat, de a Károli → KJV '
           'versmegfeleltetés csak az ÓSZ-t fedi; ott a szabály nem alkalmazható, és a hiányt a szkript nem tölti ki.',
           '- A kizárási lista csak a K-szabályok Strongjait zárja ki. Hogy a KJV által jellemzően nem címkézett '
           'funkciószavak (a „ritkán címkézett Strong” hibaok) kizárása mit adna, az a fenti hibaok-táblából látszik, '
           'de egy erre szabott lista ugyanezen a 60 versen mérve nem volna független mérés; a szkript nem tartalmazza.',
           '- A korpusz-szintű címkézési arány verstalálaton alapul (a Strong szerepel-e a vers KJV-címkéi között), nem '
           'szószintű illesztésen; a versen belül ismétlődő Strongot nem különbözteti meg.',
           '- A szabály versszintű halmazokkal dolgozik: ha egy Strong a versben kétszer áll, és a KJV csak egyszer '
           'címkézi, mindkét előfordulás „van KJV-tag” (a fordítatlan második nem jelölt).',
           '- A mérés 60 versen fut; a C-összevetés csak a KJV-szabály döntésein értelmezett, nem a C teljes pontossága.', '']
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def fut(eredmeny_ut=EREDMENY_UT, jelentes_ut=JELENTES_UT, ts=None):
    adat, info = elopar.betolt()
    ts = ts or tokenek.generalas_ts()
    szotar, stat, forras = elopar.szotar_adatbol(adat)
    f_szotar, _ = elopar.szotar_olvas(elopar.SZOTAR_UT)
    if f_szotar != szotar:
        raise SystemExit('HIBA: a %s nem egyezik az újraépített szótárral' % elopar.SZOTAR_UT)
    arany_tab = cimkezesi_arany(adat.karoli, adat.ered)
    sorok, reszlet = szamol(adat, f_szotar, forras, arany_tab)
    reszlet['korpusz_gyanu'] = korpusz_gyanu(adat.karoli, adat.ered, arany_tab)
    fej = fejlec(info, ts, tokenek.kjv_forras_azonosito())
    tsv_ir(sorok, fej, eredmeny_ut)
    md_ir(sorok, fej, adat, reszlet, arany_tab, jelentes_ut)
    print('mérés: %d sor -> %s, %s' % (len(sorok.lista), eredmeny_ut, jelentes_ut))
    return 0


# ---------------------------------------------------------------------------
# önteszt (mock-adat, nem ír a repóba)
# ---------------------------------------------------------------------------

def _w(sorsz, strong, nem_tr=False):
    return {'sorsz': sorsz, 'strong': strong, 'alak': 'α%d' % sorsz, 'tukor': 'x', 'nem_tr': nem_tr}


def onteszt():
    hibak = []

    def ell(felt, uzenet):
        if not felt:
            hibak.append(uzenet)

    # normalizálás
    ell(normal('H430') == 'H0430' and normal('H0430') == 'H0430' and normal('H0430a') == 'H0430'
        and normal('G25') == 'G0025' and normal('G5485') == 'G5485' and normal(' H853 ') == 'H0853',
        'normalizálás')
    ell(normal('xyz') == 'xyz', 'ismeretlen alak változatlan')
    # KJV-halmaz a támpont-szövegből
    kh = kjv_halmaz('In the beginning{H7225} God{H430} {H853} and{H853} x{G2532+G1473}')
    ell(kh == {'H7225', 'H0430', 'H0853', 'G2532', 'G1473'}, 'KJV-halmaz: %s' % kh)
    ell(kjv_halmaz(None) is None, 'nincs KJV-sor -> None')
    # kizárási lista
    ell(kizart_osszetevo('H9001') and kizart_osszetevo('H9009') and kizart_osszetevo('G3588')
        and kizart_osszetevo('G2532') and not kizart_osszetevo('H0853') and not kizart_osszetevo('G1161'),
        'kizárási lista')
    ell(lexikalis('G2532+G1473') == ['G1473'] and lexikalis('G3588') == [] and lexikalis('H430') == ['H0430'],
        'lexikális összetevők')
    # a szabály ágai
    ew = [_w(1, 'H9003'), _w(2, 'H7225'), _w(3, 'H1254'), _w(4, 'H430'), _w(5, 'H0853'),
          _w(6, 'G2532+G1473'), _w(7, 'G1063+G2532'), _w(8, 'G4151', nem_tr=True), _w(9, 'G3588')]
    al = kjv_szabaly(ew, {'H7225', 'H0430', 'G1473'})
    ell(al[1] == 'kizart_nyelvtani', 'H9xxx: kizárt')
    ell(al[2] == 'van_kjv_tag', 'van KJV-tag')
    ell(al[3] == 'nincs_kjv_tag', 'nincs KJV-tag')
    ell(al[4] == 'van_kjv_tag', 'normalizálás a szónál (H430 ~ H0430)')
    ell(al[5] == 'nincs_kjv_tag', 'H0853 nincs a listán: jelölt, ha a KJV nem címkézi')
    ell(al[6] == 'van_kjv_tag', 'összetett: a lexikális összetevő (G1473) a KJV-ben')
    ell(al[7] == 'nincs_kjv_tag', 'összetett: egyik lexikális összetevő sincs (G1063)')
    ell(al[8] == 'nem_tr', 'nem_tr: nem dönt')
    ell(al[9] == 'kizart_nyelvtani', 'G3588: kizárt')
    al2 = kjv_szabaly(ew, None)
    ell(set(al2.values()) == {'nincs_kjv_sor'}, 'nincs KJV-sor: minden szó nincs_kjv_sor (nem nincs_kjv_tag)')
    ell(dontes_a(al2) == set(), 'nincs KJV-sor: nincs döntés')
    ell(dontes_a(al) == {3, 5, 7}, 'A-döntések: %s' % dontes_a(al))
    p = {'forditatlan': {1: 'K8'}, 'linkek': {(1, 3): 'szotar'}}
    ell(dontes_b(al, p) == {5, 7}, 'B: a szótári linkkel ütköző szó kimarad')
    # R4: ÚSZ-vers a valós adatban: nincs KJV-sor
    ell(tokenek.kjv_tamapont_forras('Mt 4:4', 'teljes') is None, 'R4 (Mt 4:4): nincs KJV-sor')
    ell(nincs_sor_ok('Mt 4:4', 'R4').startswith('ÚSZ'), 'R4 ok-szöveg')
    ell(tokenek.kjv_tamapont_forras('1Móz 1:1', 'teljes') is not None, 'ÓSZ-vers: van KJV-sor')
    # hibaok
    tab = {'H1254': (1, 10), 'H7225': (9, 10)}
    ew3 = [_w(1, 'H7225'), _w(2, 'H1254')]
    ell(hiba_ok(ew3[1], ew3, {'H7225'}, tab).startswith('ritkán'), 'hibaok: ritkán címkézett')
    tab2 = {'H1254': (8, 10), 'H7225': (9, 10)}
    ell(hiba_ok(ew3[1], ew3, {'H9999'}, tab2).startswith('versszámozás'), 'hibaok: versszámozás-gyanú')
    ell(versszam_gyanu(ew3, {'H9999'}, tab2) and not versszam_gyanu(ew3, {'H7225'}, tab2)
        and not versszam_gyanu(ew3, None, tab2), 'versszámozás-gyanú: 0/2 igen, 1/2 nem (< 50% kell), nincs sor: nem')
    ell(not versszam_gyanu(ew3, {'H9999'}, tab), 'versszámozás-gyanú: 1 jól címkézett Strong kevés (n >= 2 kell)')
    ell(hiba_ok(ew3[1], ew3, {'H7225', 'H1255'}, tab2).startswith('más Strong'), 'hibaok: más Strong')
    ell(hiba_ok(ew3[1], ew3, {'H7225'}, tab2).startswith('egyéb'), 'hibaok: egyéb')
    # teljes futás kétszer ideiglenes könyvtárba (determinizmus; a repó nem változik)
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        uts = [(os.path.join(d, 'e%d.tsv' % i), os.path.join(d, 'j%d.md' % i)) for i in (1, 2)]
        for u in uts:
            fut(u[0], u[1], ts='T')
        for a, b in zip(*uts):
            with open(a, 'rb') as x, open(b, 'rb') as y:
                ell(x.read() == y.read(), 'determinizmus: %s' % os.path.basename(a))
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
    return fut()


if __name__ == '__main__':
    sys.exit(main())
