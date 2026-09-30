#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P4 — mérés a v1-adaton (F1, F2, F3, F5, F6; az F4 nélkül).

Bemenet:  f21p/valaszok/F{1,2,3,5,6}.jsonl, f21p/arany_opus.jsonl (60 vers),
          f21p/meres_kizaras.tsv, f21p/minta.tsv, a régi arany (tokenek.regi_arany),
          f21p/regi_arany_hibas.tsv (a régi arany hibásnak jelölt hármasai),
          f21p/futasnaplo.tsv (költség, próbálkozás).
Kimenet:  f21p/meres_eredmeny.tsv (gépi, hosszú alak) és
          naplok/F21P_meres_v1.md (olvasható), kizárólag a szkript számaiból.

Nincs API-hívás, nincs titok. A számok rétegenként (R1–R4) és összesen; minden
mérőszám mellett a nevező (n) áll, mert az arany kis mintájú (rétegenként
10–20 vers). A Wilson-intervallum (90%) linkszintű, a versen belüli
összefüggést nem kezeli, tehát optimista; csak tájékoztató.

Definíciók (F21 brief P4, a v1.1 döntésekkel):
  * link = (magyar sorszám, eredeti sorszám) a `parok`-ból; a
    f21p/meres_kizaras.tsv tokenjeit érintő linkek mind a modell, mind az arany
    oldaláról kimaradnak (PD7).
  * pontosság = a modell linkjeiből hány van az aranyban; lefedettség = az arany
    linkjeiből hány van a modellben — csak a kapun átment (allapot=ok) versekre,
    azon belül csak az aranyba eső 60 versre. A+B `magas` = az A és B egyező
    linkjei (A∩B), csak azokon a verseken, ahol A ÉS B is átment.
  * régi arany egyezés (F21.12, halmaz-definíció): a (vers, Károli-szó, Strong)
    hármas Strong mezőjét '+' mentén összetevőkre bontjuk (a régi arany
    összetett Strongja, pl. 'H5128+H5110'); a hármas egyezik, ha a Károli-szó
    (vagy többszavas kifejezés, folytonos tokensorozat) valamelyik
    előfordulásának tokenjeihez linkelt eredeti szavak Strong-halmaza MINDEN
    összetevőt tartalmaz. Egytagú Strongra ez azonos a korábbi definícióval.
    A kapun átment versekre, a teljes 200 verses mintában (nem csak az
    aranyban). Ha a szó nem található a vers tokenjei között, külön soron
    (nem_talalhato) szerepel, a nevezőben is.
    Kontrollként megmarad a korábbi érték (egyezes_korabbi_osszetett_strong_nelkul:
    a Strong mezőt egész karakterláncként hasonlítja, így összetett Strong soha
    nem egyezhet), és külön sor a f21p/regi_arany_hibas.tsv-ben hibásnak jelölt
    hármasok kizárásával (egyezes_hibas_kizarva_tajekoztato; a nevezőből is kimaradnak).
    DT21 i): a MÉRT (elsődleges) érték a kizárás nélküli `egyezes`; a küszöb
    (95%) ehhez viszonyít. A kizárásos érték csak tájékoztató. A hibás-lista
    DT21 i) óta csak az 1Móz 6:17-et tartalmazza (a 13:4 visszavonva).
  * A–B egyezés = Σ|A∩B| / Σ|A∪B| a linkeken, csak ahol A és B is átment.
  * kapuhiba: első próbálkozásra = az első nyers válasz kapuja (újraszámolva a
    `nyers[0]`-ból; keresztellenőrzés: egyezik a jsonl `probalkozas=2` verseivel és a
    futásnapló `kapuhiba_db` összegével); végleg = allapot=kapuhiba.
  * `alacsony` arány: egymodelles futásokra NEM értelmezett (PD6, G4): n.é.
    Az A+B-re F4 nélkül csak a döntőbíróhoz menő versek száma és a nem egyező
    linkek aránya adható.
  * KJV-hatás: az F1/F2 R1-es részhalmaza (100 vers) az F5/F6-tal szemben.

Használat:  python eszkozok/karoli_strong/meres.py
            python eszkozok/karoli_strong/meres.py --v2 [--onteszt]   (F21.14: F3/F3V2 × arany v1/v2, meres_v2.py)
"""

import json
import math
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kapu  # noqa: E402
import tokenek  # noqa: E402

F21P = os.path.join(tokenek.ROOT, 'f21p')
EREDMENY_UT = os.path.join(F21P, 'meres_eredmeny.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_meres_v1.md')
ARANY_UT = os.path.join(F21P, 'arany_opus.jsonl')
NAPLO_UT = os.path.join(F21P, 'futasnaplo.tsv')
MINTA_UT = os.path.join(F21P, 'minta.tsv')

FUTASOK = ['F1', 'F2', 'F3', 'F5', 'F6']
MODELL_NEV = {'F1': 'A', 'F2': 'B', 'F3': 'C', 'F5': 'A (KJV nélkül)', 'F6': 'B (KJV nélkül)'}
RETEGEK = ['R1', 'R2', 'R3', 'R4']
OSSZES = 'Összes'
OSZLOPOK = ['szakasz', 'osszeallitas', 'reteg', 'mero', 'szamlalo', 'nevezo', 'ertek',
            'wilson90_alsó', 'wilson90_felső', 'megjegyzes']
Z90 = 1.645


# ---------------------------------------------------------------------------
# betöltés
# ---------------------------------------------------------------------------

def _tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip()]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def _jsonl(ut):
    with open(ut, encoding='utf-8') as f:
        return [json.loads(s) for s in f if s.strip()]


class Adat:
    def __init__(self, futasok=None, forras_dir=None):
        """futasok: a betöltendő futások (alap: FUTASOK); forras_dir: a valaszok/ és
        a futasnaplo.tsv könyvtára (alap: f21p/; a v2-váz önteszt ideiglenes mappát ad)."""
        forras_dir = forras_dir or F21P
        self.minta = _tsv(MINTA_UT)
        self.reteg = {m['igehely']: m['reteg'] for m in self.minta}
        self.versek = [m['igehely'] for m in self.minta]
        self.arany = {o['vers']: o for o in _jsonl(ARANY_UT)}
        self.kizaras = tokenek.meres_kizaras()
        self.karoli = tokenek.betolt_karoli()
        self.ered = tokenek.betolt_eredeti()
        self.regi = tokenek.regi_arany(set(self.versek))
        self.futas = {}        # F -> {igehely: rekord + 'koteg': sor}
        self.kotegsorok = {}   # F -> [köteg-sorok]
        self.naplo_ut = os.path.join(forras_dir, 'futasnaplo.tsv')
        for f in (futasok or FUTASOK):
            sorok = _jsonl(os.path.join(forras_dir, 'valaszok', '%s.jsonl' % f))
            self.kotegsorok[f] = sorok
            d = {}
            for sor in sorok:
                for ig, r in sor['versek'].items():
                    d[ig] = dict(r, koteg=sor)
            self.futas[f] = d
        # csak a betöltött futások naplósorai (F21.16: a későbbi F3V2-sorok ne kerüljenek a v1-es P4-összesítőbe)
        self.naplo = [r for r in _tsv(self.naplo_ut) if r['futas'] in (futasok or FUTASOK)]

    def ok(self, f, ig):
        r = self.futas[f].get(ig)
        return r is not None and r['allapot'] == 'ok'

    def linkek(self, f, ig):
        """A futás linkhalmaza egy versre (kizárásokkal); None, ha nem ok."""
        if not self.ok(f, ig):
            return None
        return self._szur(ig, {(p[0], e) for p in self.futas[f][ig]['obj']['parok'] for e in p[1]})

    def arany_linkek(self, ig):
        o = self.arany[ig]
        return self._szur(ig, {(p[0], e) for p in o['parok'] for e in p[1]})

    def _szur(self, ig, linkek):
        return {(k, e) for k, e in linkek if (ig, e) not in self.kizaras}

    def reteg_versek(self, reteg, ig_lista=None):
        forras = self.versek if ig_lista is None else ig_lista
        return [ig for ig in forras if reteg == OSSZES or self.reteg[ig] == reteg]


# ---------------------------------------------------------------------------
# segédek
# ---------------------------------------------------------------------------

def wilson(x, n, z=Z90):
    if n == 0:
        return None
    p = x / n
    d = 1 + z * z / n
    kozep = (p + z * z / (2 * n)) / d
    fel = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, kozep - fel), min(1.0, kozep + fel)


class Sorok:
    def __init__(self):
        self.lista = []

    def add(self, szakasz, oss, reteg, mero, szaml, nev=None, megj='', intervallum=False):
        if nev is None:
            ertek = szaml
            wa = wf = ''
        else:
            ertek = (szaml / nev) if nev else ''
            wa = wf = ''
            if intervallum and nev:
                w = wilson(szaml, nev)
                wa, wf = '%.4f' % w[0], '%.4f' % w[1]
        self.lista.append({'szakasz': szakasz, 'osszeallitas': oss, 'reteg': reteg, 'mero': mero,
                           'szamlalo': szaml, 'nevezo': '' if nev is None else nev,
                           'ertek': ertek, 'wilson90_alsó': wa, 'wilson90_felső': wf, 'megjegyzes': megj})


# ---------------------------------------------------------------------------
# a mérések
# ---------------------------------------------------------------------------

def osszeallitasok(adat):
    """{név: (ok_fn(ig) -> bool, link_fn(ig) -> linkhalmaz)} a pontossághoz és a régi aranyhoz."""
    def egy(f):
        return (lambda ig: adat.ok(f, ig), lambda ig: adat.linkek(f, ig))

    def ketto(m):
        def ok(ig):
            return adat.ok('F1', ig) and adat.ok('F2', ig)

        def lk(ig):
            a, b = adat.linkek('F1', ig), adat.linkek('F2', ig)
            return m(a, b)
        return ok, lk
    return {
        'A': egy('F1'), 'B': egy('F2'), 'C': egy('F3'),
        'A+B magas (A∩B)': ketto(lambda a, b: a & b),
        'A∪B (döntőbíró előtti felső korlát)': ketto(lambda a, b: a | b),
    }


def pontossag(adat, sorok):
    for nev, (ok, lk) in osszeallitasok(adat).items():
        for ret in RETEGEK + [OSSZES]:
            arany_versek = adat.reteg_versek(ret, [ig for ig in adat.versek if ig in adat.arany])
            vs = [ig for ig in arany_versek if ok(ig)]
            modell = talalat = arany = 0
            for ig in vs:
                l, g = lk(ig), adat.arany_linkek(ig)
                modell += len(l)
                talalat += len(l & g)
                arany += len(g)
            sorok.add('pontossag_lefedettseg', nev, ret, 'arany_versek_kapun_atment', len(vs), len(arany_versek),
                      'nevező: az aranyba eső versek a rétegben; számláló: ebből kapun átment')
            sorok.add('pontossag_lefedettseg', nev, ret, 'pontossag', talalat, modell,
                      'a modell linkjeiből az aranyban', intervallum=True)
            sorok.add('pontossag_lefedettseg', nev, ret, 'lefedettseg', talalat, arany,
                      'az arany linkjeiből a modellben', intervallum=True)


def _hivatkozas_szavak(adat, ig, links):
    """{magyar sorszám: {eredeti Strong, ...}} egy vers linkjeiből."""
    ered = adat.ered[ig]
    d = {}
    for k, e in links:
        d.setdefault(k, set()).add(ered[e - 1]['strong'])
    return d


def _kifejezes_helyek(tokenek_lista, kif):
    n = len(kif)
    if n == 0:
        return []
    kif = [t.casefold() for t in kif]
    tl = [t.casefold() for t in tokenek_lista]
    return [i for i in range(len(tl) - n + 1) if tl[i:i + n] == kif]


REGI_HIBAS_UT = os.path.join(F21P, 'regi_arany_hibas.tsv')


def regi_hibas():
    """A régi arany hibásnak jelölt hármasai: {(igehely, karoli_szo, strong): ok}."""
    if not os.path.exists(REGI_HIBAS_UT):
        return {}
    # a '#'-kezdetű sor MANUAL-proveniencia (DT21 i: az 1Móz 13:4 visszavonása), átugorjuk
    with open(REGI_HIBAS_UT, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return {(r['igehely'], r['karoli_szo'], r['strong']): r['ok']
            for r in (dict(zip(fej, s.split('\t'))) for s in sorok[1:])}


def regi_egyezik(adat, ig, szo, strong, links, halmaz=True):
    """(talalhato, egyezik) egy régi-arany-hármasra a megadott linkhalmazzal.

    halmaz=True: a Strong '+' mentén összetevőkre bontva; egyezik, ha egy
    előfordulás tokenjeihez linkelt eredeti Strongok halmaza minden összetevőt
    tartalmaz. halmaz=False: a korábbi (F21.10) definíció, a Strong mező egész
    karakterláncként, tokenenként.
    """
    tl = tokenek.tokenizal(adat.karoli[ig])
    kif = tokenek.tokenizal(szo)
    helyek = _kifejezes_helyek(tl, kif)
    if not helyek:
        return False, False
    kszavak = _hivatkozas_szavak(adat, ig, links)
    if not halmaz:
        return True, any(strong in kszavak.get(i + j + 1, set()) for i in helyek for j in range(len(kif)))
    osszetevok = set(strong.split('+'))
    for i in helyek:
        linkelt = set()
        for j in range(len(kif)):
            linkelt |= kszavak.get(i + j + 1, set())
        if osszetevok <= linkelt:
            return True, True
    return True, False


def regi_arany(adat, sorok):
    hibas = regi_hibas()
    for nev, (ok, lk) in osszeallitasok(adat).items():
        if nev.startswith('A∪B'):
            continue
        for ret in RETEGEK + [OSSZES]:
            hb = egyezik = nincs = korabbi = 0
            hb_k = egyezik_k = kizart = 0
            for ig, szo, strong in adat.regi:
                if ret != OSSZES and adat.reteg[ig] != ret:
                    continue
                if not ok(ig):
                    continue
                hb += 1
                links = lk(ig)
                talalhato, e = regi_egyezik(adat, ig, szo, strong, links)
                _, e_regi = regi_egyezik(adat, ig, szo, strong, links, halmaz=False)
                if not talalhato:
                    nincs += 1
                egyezik += e
                korabbi += e_regi
                if (ig, szo, strong) in hibas:
                    kizart += 1
                else:
                    hb_k += 1
                    egyezik_k += e
            sorok.add('regi_arany', nev, ret, 'hármasok_kapun_atment_versekben', hb, None,
                      'nevező: régi arany hármasok a rétegben, ahol a vers kapun átment')
            sorok.add('regi_arany', nev, ret, 'nem_talalhato_karoli_szo', nincs, hb,
                      'a Károli-szó/kifejezés nincs a vers tokenjei között (a nevezőben benne van)')
            sorok.add('regi_arany', nev, ret, 'egyezes_korabbi_osszetett_strong_nelkul', korabbi, hb,
                      'KONTROLL, korábbi (F21.10) definíció: a Strong mező egész karakterláncként; összetett Strong sosem egyezik',
                      intervallum=True)
            sorok.add('regi_arany', nev, ret, 'egyezes', egyezik, hb,
                      'MÉRT (elsődleges, DT21 i): halmaz-definíció (F21.12): az összetett Strong minden összetevője a Károli-szóhoz linkelt eredeti Strongok között; kizárás nélkül; a küszöb ehhez viszonyít',
                      intervallum=True)
            sorok.add('regi_arany', nev, ret, 'hibas_regi_hármas_kizarva', kizart, hb,
                      'TÁJÉKOZTATÓ: f21p/regi_arany_hibas.tsv: a régi arany hibásnak jelölt hármasai (DT21 i óta csak az 1Móz 6:17; a 13:4 visszavonva)')
            sorok.add('regi_arany', nev, ret, 'egyezes_hibas_kizarva_tajekoztato', egyezik_k, hb_k,
                      'TÁJÉKOZTATÓ (DT21 i): halmaz-definíció, a hibásnak jelölt régi hármas(ok) nélkül (a nevezőből is kimarad); küszöb-viszonyításra nem használható',
                      intervallum=True)


def ab_egyezes(adat, sorok, szakasz='ab_egyezes', fa='F1', fb='F2', cimke='A–B', retegek=None):
    for ret in (retegek or RETEGEK + [OSSZES]):
        vs = [ig for ig in adat.reteg_versek(ret) if adat.ok(fa, ig) and adat.ok(fb, ig)]
        osszes_vers = adat.reteg_versek(ret, [ig for ig in adat.versek if ig in adat.futas[fa] and ig in adat.futas[fb]])
        metszet = unio = azonos = 0
        for ig in vs:
            a, b = adat.linkek(fa, ig), adat.linkek(fb, ig)
            metszet += len(a & b)
            unio += len(a | b)
            azonos += 1 if a == b else 0
        sorok.add(szakasz, cimke, ret, 'versek_mindketto_atment', len(vs), len(osszes_vers),
                  'nevező: a rétegben futott versek')
        sorok.add(szakasz, cimke, ret, 'link_egyezes (uniós arány)', metszet, unio,
                  'Σ|A∩B| / Σ|A∪B|, csak ahol mindkettő átment', intervallum=True)
        sorok.add(szakasz, cimke, ret, 'azonos_linkhalmazu_versek', azonos, len(vs), 'vers-szintű egyezés')


def hibatipusok(adat, f):
    """{'elso': {pont: versdb}, 'vegleg': {pont: versdb}} és a teljes-válasz-hibák száma."""
    elso, vegleg = {}, {}
    elso_hibas_versek = set()
    for sor in adat.kotegsorok[f]:
        ig_lista = sor['igehelyek']
        r1 = kapu.valasz_ellenoriz(sor['nyers'][0], ig_lista)
        for ig in ig_lista:
            if not r1[ig]['ok']:
                elso_hibas_versek.add(ig)
                for t in _tipusok(r1[ig]['hibak']):
                    elso[t] = elso.get(t, 0) + 1
        for ig in ig_lista:
            v = sor['versek'][ig]
            if v['allapot'] != 'ok':
                for t in _tipusok(v['hibak']):
                    vegleg[t] = vegleg.get(t, 0) + 1
    return elso, vegleg, elso_hibas_versek


def _tipusok(hibak):
    """Kapupont szerinti hibatípusok (versenként egyszer): '1-json', '1-hianyzo_vers', '1', '2'..'5'."""
    ki = set()
    for h in hibak:
        m = re.match(r'(\d)\.', h)
        pont = m.group(1) if m else '?'
        if pont == '1':
            if 'nem érvényes JSON' in h or 'nem JSON' in h:
                pont = '1-json'
            elif 'hiányzik ez a vers' in h:
                pont = '1-hianyzo_vers'
        ki.add(pont)
    return ki


def kapuhiba(adat, sorok):
    for f in FUTASOK:
        elso, vegleg, elso_hibas = hibatipusok(adat, f)
        jsonl_p2 = {ig for ig, r in adat.futas[f].items() if r['probalkozas'] == 2}
        naplo_p1 = sum(int(r['kapuhiba_db']) for r in adat.naplo if r['futas'] == f and r['probalkozas'] == '1')
        egyezik = (elso_hibas == jsonl_p2 and len(elso_hibas) == naplo_p1)
        for ret in RETEGEK + [OSSZES]:
            vs = adat.reteg_versek(ret, [ig for ig in adat.versek if ig in adat.futas[f]])
            if not vs:
                continue
            e = sum(1 for ig in vs if ig in elso_hibas)
            v = sum(1 for ig in vs if adat.futas[f][ig]['allapot'] != 'ok')
            sorok.add('kapuhiba', '%s (%s)' % (f, MODELL_NEV[f]), ret, 'kapuhiba_elso_probara', e, len(vs),
                      'első nyers válasz kapuja, újraszámolva', intervallum=True)
            sorok.add('kapuhiba', '%s (%s)' % (f, MODELL_NEV[f]), ret, 'kapuhiba_vegleg', v, len(vs),
                      'egy újrakérés után is hibás', intervallum=True)
        sorok.add('kapuhiba', '%s (%s)' % (f, MODELL_NEV[f]), '-', 'keresztellenorzes_elso_probalkozas',
                  len(elso_hibas), naplo_p1,
                  'újraszámolt első-próbás hibás versek = jsonl probalkozas=2 versek = napló kapuhiba_db(probalkozas=1) összeg: %s'
                  % ('EGYEZIK' if egyezik else 'ELTÉR'))
        for t in sorted(set(elso) | set(vegleg)):
            sorok.add('kapuhiba_tipus', '%s (%s)' % (f, MODELL_NEV[f]), OSSZES,
                      'kapupont_%s_elso_probara' % t, elso.get(t, 0), len(adat.futas[f]),
                      'hibás versek száma ezzel a kapuponttal (egy vers több ponton is hibázhat)')
            sorok.add('kapuhiba_tipus', '%s (%s)' % (f, MODELL_NEV[f]), OSSZES,
                      'kapupont_%s_vegleg' % t, vegleg.get(t, 0), len(adat.futas[f]),
                      'a végleg hibás versek kapuponttal')


def ab_osszeallitas(adat, sorok):
    """Az A+B összeállítás F4 nélkül: osztályok, döntőbíróhoz menő versek."""
    for ret in RETEGEK + [OSSZES]:
        vs = adat.reteg_versek(ret)
        n = len(vs)
        egyezo = eltero = csak_a = csak_b = egyik_sem = 0
        for ig in vs:
            a, b = adat.ok('F1', ig), adat.ok('F2', ig)
            if a and b:
                if adat.linkek('F1', ig) == adat.linkek('F2', ig):
                    egyezo += 1
                else:
                    eltero += 1
            elif a:
                csak_a += 1
            elif b:
                csak_b += 1
            else:
                egyik_sem += 1
        for mero, x in (('mindketto_atment_azonos_linkekkel', egyezo), ('mindketto_atment_eltero_linkekkel', eltero),
                        ('csak_A_atment', csak_a), ('csak_B_atment', csak_b), ('egyik_sem_atment', egyik_sem)):
            sorok.add('ab_osszeallitas', 'A+B', ret, mero, x, n, '')
        sorok.add('ab_osszeallitas', 'A+B', ret, 'dontobirohoz_menne (eltero + csak egyik + egyik sem)',
                  eltero + csak_a + csak_b + egyik_sem, n,
                  'F4 nélküli pontos darabszám: nem azonos linkhalmazú vagy kapuhibás vers', intervallum=True)
        sorok.add('ab_osszeallitas', 'A+B', ret, 'alacsony_arany', 'n.é.', None,
                  'egymodelles futásra nem értelmezett (PD6, G4); az A+B alacsony aránya a C döntésétől függ (F4 nélkül nem számolható)')
    # link-szintű nem-egyező arány (mindkettő átment)
    for ret in RETEGEK + [OSSZES]:
        vs = [ig for ig in adat.reteg_versek(ret) if adat.ok('F1', ig) and adat.ok('F2', ig)]
        unio = sum(len(adat.linkek('F1', ig) | adat.linkek('F2', ig)) for ig in vs)
        metsz = sum(len(adat.linkek('F1', ig) & adat.linkek('F2', ig)) for ig in vs)
        sorok.add('ab_osszeallitas', 'A+B', ret, 'nem_egyezo_link_arany (1 − A∩B/A∪B)', unio - metsz, unio,
                  'csak ahol mindkettő átment; ez a link-szintű „nem magas” felső becslés, F4 nélkül')


def kjv_hatas(adat, sorok):
    """Az F1/F2 R1-es részhalmaza az F5/F6-tal szemben (kapun átment versek, közös halmazon is)."""
    r1 = adat.reteg_versek('R1')
    r1_arany = [ig for ig in r1 if ig in adat.arany]
    szakasz = 'kjv_hatas'

    def pont_lef(f, vs):
        modell = talalat = arany = 0
        for ig in vs:
            l, g = adat.linkek(f, ig), adat.arany_linkek(ig)
            modell += len(l)
            talalat += len(l & g)
            arany += len(g)
        return talalat, modell, arany

    feltetelek = (('KJV-val (F1/F2)', 'F1', 'F2'), ('KJV nélkül (F5/F6)', 'F5', 'F6'))
    # kapuhiba mindkét feltételben (R1, mindkét modell)
    for cimke, fa, fb in feltetelek:
        for f in (fa, fb):
            vs = [ig for ig in r1 if ig in adat.futas[f]]
            v = sum(1 for ig in vs if adat.futas[f][ig]['allapot'] != 'ok')
            _, _, eh = hibatipusok(adat, f)
            e = sum(1 for ig in vs if ig in eh)
            sorok.add(szakasz, '%s %s' % (cimke, MODELL_NEV[f]), 'R1', 'kapuhiba_vegleg', v, len(vs), 'R1 összes verse', intervallum=True)
            sorok.add(szakasz, '%s %s' % (cimke, MODELL_NEV[f]), 'R1', 'kapuhiba_elso_probara', e, len(vs), 'R1 összes verse', intervallum=True)
    # egymodelles: saját halmaz és a KJV-val/nélkül közös halmaz
    for modell, fk, fn in (('A', 'F1', 'F5'), ('B', 'F2', 'F6')):
        kozos = [ig for ig in r1_arany if adat.ok(fk, ig) and adat.ok(fn, ig)]
        for cimke, f in (('KJV-val', fk), ('KJV nélkül', fn)):
            sajat = [ig for ig in r1_arany if adat.ok(f, ig)]
            for halmaz_nev, vs in (('saját halmaz (kapun átment)', sajat), ('közös halmaz (mindkét feltételben átment)', kozos)):
                t, m, a = pont_lef(f, vs)
                sorok.add(szakasz, '%s %s' % (modell, cimke), 'R1', 'arany_versek [%s]' % halmaz_nev, len(vs), len(r1_arany), '')
                sorok.add(szakasz, '%s %s' % (modell, cimke), 'R1', 'pontossag [%s]' % halmaz_nev, t, m, '', intervallum=True)
                sorok.add(szakasz, '%s %s' % (modell, cimke), 'R1', 'lefedettseg [%s]' % halmaz_nev, t, a, '', intervallum=True)
    # A–B egyezés
    kozos4 = [ig for ig in r1 if all(adat.ok(f, ig) for f in ('F1', 'F2', 'F5', 'F6'))]
    eltérés = {}
    for cimke, fa, fb in feltetelek:
        sajat = [ig for ig in r1 if adat.ok(fa, ig) and adat.ok(fb, ig)]
        for halmaz_nev, vs in (('saját halmaz (A és B átment)', sajat), ('közös halmaz (mind a négy átment)', kozos4)):
            m = u = 0
            for ig in vs:
                a, b = adat.linkek(fa, ig), adat.linkek(fb, ig)
                m += len(a & b)
                u += len(a | b)
            sorok.add(szakasz, cimke, 'R1', 'A–B_versek [%s]' % halmaz_nev, len(vs), len(r1), 'nevező: R1 versei')
            sorok.add(szakasz, cimke, 'R1', 'A–B_egyezes [%s]' % halmaz_nev, m, u, 'Σ|A∩B| / Σ|A∪B|', intervallum=True)
            eltérés[(cimke, halmaz_nev)] = (u - m, u)
    # `magas` (A∩B) pontosság az aranyon, közös halmazon
    kozos4_arany = [ig for ig in kozos4 if ig in adat.arany]
    magas = {}
    for cimke, fa, fb in feltetelek:
        t = m = a = 0
        for ig in kozos4_arany:
            l = adat.linkek(fa, ig) & adat.linkek(fb, ig)
            g = adat.arany_linkek(ig)
            m += len(l)
            t += len(l & g)
            a += len(g)
        magas[cimke] = (t, m)
        sorok.add(szakasz, cimke, 'R1', 'magas (A∩B) arany_versek [közös halmaz]', len(kozos4_arany), len(r1_arany), '')
        sorok.add(szakasz, cimke, 'R1', 'magas (A∩B) pontossag [közös halmaz]', t, m, '', intervallum=True)
        sorok.add(szakasz, cimke, 'R1', 'magas (A∩B) lefedettseg [közös halmaz]', t, a, '', intervallum=True)
    # a brief KJV-küszöb mérőszámai (nincs minősítés)
    (t1, m1), (t0, m0) = magas['KJV-val (F1/F2)'], magas['KJV nélkül (F5/F6)']
    if m1 and m0:
        sorok.add(szakasz, 'KJV-val − KJV nélkül', 'R1', 'delta_magas_pontossag_szazalekpont [közös halmaz]',
                  round(100 * (t1 / m1 - t0 / m0), 2), None, 'küszöb-mérőszám 1 (a brief szerint ≥ +1 pp); n: %d ill. %d link' % (m1, m0))
    for halmaz_nev in ('közös halmaz (mind a négy átment)', 'saját halmaz (A és B átment)'):
        x1, u1 = eltérés[('KJV-val (F1/F2)', halmaz_nev)]
        x0, u0 = eltérés[('KJV nélkül (F5/F6)', halmaz_nev)]
        if u1 and u0 and x0:
            sorok.add(szakasz, 'KJV-val vs KJV nélkül', 'R1', 'A–B_eltérés_relativ_csokkenes [%s]' % halmaz_nev,
                      round(100 * ((x0 / u0) - (x1 / u1)) / (x0 / u0), 2), None,
                      'küszöb-mérőszám 2 (a brief szerint ≥ 20%%); eltérés KJV nélkül %d/%d, KJV-val %d/%d' % (x0, u0, x1, u1))


def koltseg(adat, sorok):
    import futtat  # csak az ártábla és a modellnevek miatt
    for f in FUTASOK + ['-- összesen']:
        sor = [r for r in adat.naplo if f == '-- összesen' or r['futas'] == f]
        if not sor:
            continue
        nev = f if f == '-- összesen' else '%s (%s)' % (f, MODELL_NEV[f])
        hivas_p1 = sum(1 for r in sor if r['probalkozas'] == '1')
        hivas_p2 = sum(1 for r in sor if r['probalkozas'] == '2')
        sorok.add('koltseg', nev, '-', 'hivasok_osszes', len(sor), None, 'próbálkozás=1: %d, próbálkozás=2: %d' % (hivas_p1, hivas_p2))
        sorok.add('koltseg', nev, '-', 'bemeneti_token', sum(int(r['bemenet_token']) for r in sor), None, '')
        sorok.add('koltseg', nev, '-', 'kimeneti_token (a completion_tokens, a gondolkodást is tartalmazhatja)',
                  sum(int(r['kimenet_token']) for r in sor), None, '')
        sorok.add('koltseg', nev, '-', 'gondolkodasi_token (napló gondolkodas_token oszlopa)',
                  sum(int(r['gondolkodas_token']) for r in sor), None,
                  'FIGYELEM: a C-nél a napló 0-t ír; a nyers usage nem maradt meg, a múltbeli érték nem rekonstruálható' if f in ('F3', '-- összesen') else '')
        sorok.add('koltseg', nev, '-', 'koltseg_usd (OpenRouter cost mező)', round(sum(float(r['koltseg_usd']) for r in sor), 6), None,
                  'koltseg_forras: %s' % ','.join(sorted({r['koltseg_forras'] for r in sor})))
        sorok.add('koltseg', nev, '-', 'gondolkodasi_mod', '; '.join(sorted({r['gondolkodas_mod'] for r in sor})), None, '')
    # a cost és a táblaár viszonya modellenként (a rejtett gondolkodási token lehetséges jele; A/B nyitva: cache, ártábla)
    for modell in futtat.MODELLEK.values():
        sor = [r for r in adat.naplo if r['modell'] == modell]
        ar_be, ar_ki = futtat.ARAK[modell]
        tabla = sum(int(r['bemenet_token']) * ar_be / 1e6 + int(r['kimenet_token']) * ar_ki / 1e6 for r in sor)
        cost = sum(float(r['koltseg_usd']) for r in sor)
        sorok.add('koltseg_tablaar', modell, '-', 'cost / (bemenet·ár + kimenet·ár)', round(cost, 6), round(tabla, 6),
                  'táblaár %.3f/%.3f USD/1M (futtat.ARAK); az érték a tényleges/táblaár arány; nem a gondolkodási token mérése' % (ar_be, ar_ki))


# ---------------------------------------------------------------------------
# kiírás
# ---------------------------------------------------------------------------

def _fmt(v):
    if isinstance(v, float):
        return '%.6g' % v
    return str(v)


def tsv_ir(sorok, adat_ts):
    fej = ('# GENERÁLT: eszkozok/karoli_strong/meres.py | scope=f21p (F1,F2,F3,F5,F6; F4 nélkül) | '
           'forras=f21p/valaszok/*.jsonl, f21p/arany_opus.jsonl, f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, f21p/futasnaplo.tsv | '
           'ts=%s (a futásnapló utolsó sora) | kézzel szerkeszteni tilos' % adat_ts)
    with open(EREDMENY_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + '\n')
        f.write('\t'.join(OSZLOPOK) + '\n')
        for r in sorok.lista:
            f.write('\t'.join(_fmt(r[k]) for k in OSZLOPOK) + '\n')


def _cella(r):
    if r['nevezo'] == '':
        return _fmt(r['ertek'])
    if r['ertek'] == '':
        return '— (%s/%s)' % (r['szamlalo'], r['nevezo'])
    s = '%.1f%% (%s/%s)' % (100 * r['ertek'], r['szamlalo'], r['nevezo'])
    if r['wilson90_alsó'] != '':
        s += ' [%.0f–%.0f]' % (100 * float(r['wilson90_alsó']), 100 * float(r['wilson90_felső']))
    return s


def md_ir(sorok, adat_ts):
    cimek = {
        'pontossag_lefedettseg': 'a) Pontosság és lefedettség az Opus-aranyhoz (csak kapun átment, aranyba eső versek)',
        'regi_arany': 'b) Régi arany egyezés (kapun átment versek, a 200 verses mintában)',
        'ab_egyezes': 'c) A–B egyezés (csak ahol A és B is átment a kapun)',
        'kapuhiba': 'd) Kapuhiba-arány (első próbára és végleg)',
        'kapuhiba_tipus': 'd2) Kapuhiba-típusok kapupont szerint (hibás versek száma)',
        'ab_osszeallitas': 'e) Az A+B összeállítás F4 nélkül (döntőbíróhoz menő versek)',
        'kjv_hatas': 'f) KJV-hatás az R1-en (F1/F2 R1-részhalmaz az F5/F6-tal szemben)',
        'koltseg': 'g) Költség futásonként (a futásnaplóból)',
        'koltseg_tablaar': 'g2) A cost és a táblaár viszonya',
    }
    ki = ['# F21P_meres_v1.md — P4 mérés a v1-adaton (F1, F2, F3, F5, F6; F4 nélkül)', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/meres.py | scope=f21p | forras=f21p/valaszok/*.jsonl, '
          'f21p/arany_opus.jsonl, f21p/meres_kizaras.tsv, f21p/regi_arany_hibas.tsv, f21p/futasnaplo.tsv | ts=%s | '
          'kézzel szerkeszteni tilos; a számok forrása f21p/meres_eredmeny.tsv -->' % adat_ts, '',
          'Kizárólag szkriptkimenet; értelmezés és küszöb-minősítés nincs benne. Cellaforma: érték% (számláló/nevező)'
          ' [90%-os Wilson-intervallum, linkszintű, optimista]. Az arany 60 vers (R1 20, R2 10, R3 10, R4 20), ezért '
          'a rétegenkénti értékek megbízhatósága korlátozott: a nevezőt mindig nézd. `alacsony` arány: egymodelles '
          'futásokra n.é. (PD6, G4).', '',
          'Régi arany (b) pont, F21.12: az `egyezes` a halmaz-definíció — a régi Strong mező \'+\' mentén '
          'összetevőkre bontva, a hármas akkor egyezik, ha a Károli-szó (kifejezés) valamelyik előfordulásához '
          'linkelt eredeti szavak Strongjai között MINDEN összetevő ott van. Az '
          '`egyezes_korabbi_osszetett_strong_nelkul` a korábbi (F21.10) érték kontrollként (a Strong mező egész '
          'karakterláncként; összetett Strong sosem egyezhetett). A `hibas_regi_hármas_kizarva` a '
          'f21p/regi_arany_hibas.tsv-ben hibásnak jelölt hármasok száma („N hármas kizárva: a régi arany '
          'hibás”); az `egyezes_hibas_kizarva_tajekoztato` ezek nélkül számol, a nevezőből is kihagyva. '
          'DT21 i): a MÉRT (elsődleges) érték a kizárás nélküli `egyezes`, a küszöb ehhez viszonyít; a '
          'kizárásos érték csak TÁJÉKOZTATÓ. A hibás-lista csak az 1Móz 6:17-et tartalmazza (az 1Móz 13:4 '
          'jelölése a felhasználó döntése szerint visszavonva).', '']
    szakaszok = []
    for r in sorok.lista:
        if r['szakasz'] not in szakaszok:
            szakaszok.append(r['szakasz'])
    for sz in szakaszok:
        ki += ['## ' + cimek.get(sz, sz), '']
        rs = [r for r in sorok.lista if r['szakasz'] == sz]
        if sz in ('koltseg', 'koltseg_tablaar', 'kapuhiba_tipus'):
            ki += ['| összeállítás | mérőszám | érték | megjegyzés |', '|---|---|---|---|']
            for r in rs:
                ki.append('| %s | %s | %s | %s |' % (r['osszeallitas'], r['mero'], _cella(r), r['megjegyzes']))
            ki.append('')
            continue
        # pivot: (összeállítás, mérőszám) sorok; oszlopok: rétegek
        kulcsok = []
        for r in (x for x in rs if x['reteg'] != '-'):
            k = (r['osszeallitas'], r['mero'])
            if k not in kulcsok:
                kulcsok.append(k)
        ki += ['| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |', '|---|---|---|---|---|---|---|']
        for k in kulcsok:
            cellak = []
            for ret in RETEGEK + [OSSZES]:
                x = [r for r in rs if (r['osszeallitas'], r['mero']) == k and r['reteg'] == ret]
                cellak.append(_cella(x[0]) if x else '—')
            ki.append('| %s | %s | %s |' % (k[0], k[1], ' | '.join(cellak)))
        ki.append('')
        extra = [r for r in rs if r['reteg'] == '-' or r['megjegyzes'].startswith(('küszöb', 'FIGYELEM'))]
        for r in extra:
            ki.append('- %s — %s: %s; %s' % (r['mero'], r['osszeallitas'], _cella(r), r['megjegyzes']))
        if extra:
            ki.append('')
    with open(JELENTES_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def main():
    if '--v2' in sys.argv:
        # F21.14: az F3 és az F3V2 az arany v1/v2-höz (meres_v2.py; a v2 befagyasztott, sha256-ellenőrzéssel)
        import meres_v2
        return meres_v2.onteszt() if '--onteszt' in sys.argv else meres_v2.fut()[0]
    adat = Adat()
    sorok = Sorok()
    pontossag(adat, sorok)
    regi_arany(adat, sorok)
    ab_egyezes(adat, sorok)
    kapuhiba(adat, sorok)
    ab_osszeallitas(adat, sorok)
    kjv_hatas(adat, sorok)
    koltseg(adat, sorok)
    adat_ts = max(r['ts'] for r in adat.naplo)
    tsv_ir(sorok, adat_ts)
    md_ir(sorok, adat_ts)
    print('kész: %d sor -> %s, %s' % (len(sorok.lista), EREDMENY_UT, JELENTES_UT))
    bad = [r for r in sorok.lista if r['mero'] == 'keresztellenorzes_elso_probalkozas' and 'ELTÉR' in r['megjegyzes']]
    if bad:
        print('FIGYELEM: a kapuhiba keresztellenőrzése eltér: %s' % [r['osszeallitas'] for r in bad], file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
