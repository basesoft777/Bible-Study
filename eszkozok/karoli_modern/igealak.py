#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.2 — a modernizált Károli-réteg igealak-lépcsője és a *vala* (DT128, DT-F96d, DT-F96e c, DT-F96f).

A .1 (helyesírás, `helyesiras.py`) kimenetére épül: a .1-et a saját függvényeivel újraszámolja, és
összeveti a kiadott `adat/karoli_modern/helyesiras_tokenek.tsv`-vel; eltérésnél megáll, és nem ír.
Determinisztikus, API és Hunspell nélkül. Az LLM-es ellenőrzés (DT-F96d: az előfizetésből, Claude
Code-ból, API nélkül) külön lépés: a `--llm-kerdes` kiírja a kérdéseket (repón kívülre), a modell
válaszait a `--llm-valasz` olvassa be az `adat/karoli_modern/igealak_llm.tsv`-be; a generátor ezt
csak olvassa, a tő-őrön át.

Csak olvas: `konkordancia/Karoli_1908.tsv`, `adat/szoto/karoli_szotari_alak.tsv` (#94),
`adat/karoli_modern/helyesiras_tokenek.tsv` (.1), `adat/karoli_modern/igealak_llm.tsv` (ha van).
A tokenizálás a `tokenizal` (a #22 `hu_sorszam`-a): a réteg Strongot nem tárol (DT-F96f).

Alakszintű döntés (az osztály a `fedettseg.py osztalyoz` szerint):

  igealak_gyakori   régies jegy a 200 leggyakoribb jegyes alakon (DT140): a jegy szerinti mai alak,
                    automatikus csere (a hibás jegyű és rosszul képzett alak a KEZI táblában)
  regies_lista      lőn → lett, lőnek → lettek, vagyon → van (névelő után főnév, marad), a vala-család
                    tokenszinten (l. lent)
  regies_gyanu_kezi a jegy nélküli régies alakok kézzel átnézett, gyakori része (GYANU_KEZI: jő → jön,
                    mondák → mondták …; N-F96b): automatikus csere
  igealak_ritka,    NEM automatikus csere (N-F94h: a ritka alak jegye ~6%-ban hibás): a szabály jelöltje
  regies_gyanu      és az LLM jelöltje a `jelolt` oszlopba kerül, a modern szöveg nem változik
  felszolito.E2     -jál/-jél → -j: nem automatikus (DT-F96k, a felhasználó dönt), jelölt

Tokenszintű döntés:

  vala-család       létigei → volt / voltak / voltam …; segédigei (közvetlenül előtte, egy szóközzel,
                    véges igealak) → kiesik (`kieso=segedige`): ha az ige jelen idejű, múlt időbe kerül
                    (lebeg vala → lebegett, mondja vala → mondta); ha múlt idejű, csak a vala esik ki;
                    ha a jelen idő nem elemezhető, mindkettő marad (`bizonytalan=vala_segedige`).
                    Igenév után (írva vala) létigei: volt.
  tárgyas/alanyi    a T/3, E/2, T/1, T/2 régies alakja a ragozást nem jelöli: határozott tárgy a
                    tagmondatban (azt, ezt, őt, őket, a/az + -t, birtokos -t, utána „, hogy”) → tárgyas;
                    különben alanyi; a mond mindig tárgyas (DT128: monda → mondta)
  -ék E/1 vagy T/3  magas hangrendű igén (kérék): E/1, ha a versben egyes szám első személy áll (én,
                    engem, nekem …), különben T/3 tárgyas (`bizonytalan=ek_E1_T3`)

Önellenőrzés (K2): a modern versszöveg újratokenizálva pontosan a nem kieső tokenek modern alakjait
adja, sorrendben; a nem-betű váz a kieső tokenek egy-egy szóközén kívül változatlan.

Ír (generált, kézzel nem szerkeszthető):
  adat/karoli_modern/igealak_alakok.tsv    alakonként: osztály, jegy, szabály-jelölt, LLM-jelölt, döntés
  adat/karoli_modern/igealak_tokenek.tsv   a .1 + .2 után változó, kieső, bizonytalan vagy jelölt tokenek
  adat/karoli_modern/igealak_minta.tsv     rögzített magú minta (--minta; --minta-frissit)

Használat:
    python eszkozok/karoli_modern/igealak.py
    python eszkozok/karoli_modern/igealak.py --minta | --minta-frissit
    python eszkozok/karoli_modern/igealak.py --kimenet <könyvtár>          (próba a repón kívülre)
    python eszkozok/karoli_modern/igealak.py --llm-kerdes <könyvtár> [--koteg N]
    python eszkozok/karoli_modern/igealak.py --llm-valasz <könyvtár> --modell <név>
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_modern'))
import tokenek  # noqa: E402
import fedettseg  # noqa: E402
import helyesiras  # noqa: E402
import igeragozas as ir  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KAROLI = fedettseg.KAROLI
SZOTARI = fedettseg.SZOTARI
KI_DIR = os.path.join('adat', 'karoli_modern')
H_TOKENEK = os.path.join(KI_DIR, 'helyesiras_tokenek.tsv')
LLM_TABLA = os.path.join(KI_DIR, 'igealak_llm.tsv')
LLM_NAPLO = os.path.join(KI_DIR, 'igealak_llm_hivasok.jsonl')
SZKRIPT = 'eszkozok/karoli_modern/igealak.py'
MODUL = 'eszkozok/karoli_modern/igeragozas.py'
MAG = 20261024
BETU = helyesiras.BETU

JEGY_SZEM = {
    'mult.alanyi.E3': ('E3', False), 'mult.targyas.E3': ('E3', True), 'mult.E3': ('E3', False),
    'mult.E1': ('E1', None), 'mult.E2': ('E2', None), 'mult.T1': ('T1', None), 'mult.T2': ('T2', None),
    'mult.T3': ('T3', None),
}
VALA = {'vala': ('E3', 'volt'), 'valának': ('T3', 'voltak'), 'valék': ('E1', 'voltam'),
        'valál': ('E2', 'voltál'), 'valánk': ('T1', 'voltunk'), 'valátok': ('T2', 'voltatok')}
LON = {'lőn': 'lett', 'lőnek': 'lettek'}
TARGYAS_MINDIG = {'mond'}  # DT128: monda → mondta (az idézett beszéd tárgy)
HATAROZOTT_TARGY = {'azt', 'ezt', 'őt', 'őket', 'magát', 'magokat', 'magukat', 'azokat', 'ezeket', 'mindazt',
                    'amazt', 'önmagát', 'mindezt', 'mindazokat', 'mindezeket', 'magamat', 'magadat'}
BIRTOKOS_TARGY = re.compile(r'(ját|jét|át|ét|mat|met|dat|det|nkat|nket|tokat|teket|ukat|üket|jukat|jüket|'
                            r'imat|imet|idat|idet|ait|eit|jait|jeit)$')
E1_JEL = {'én', 'engem', 'nekem', 'nékem', 'velem', 'tőlem', 'hozzám', 'bennem', 'belőlem', 'rám', 'reám',
          'rólam', 'előttem', 'magam', 'magamat', 'enyém', 'nálam', 'értem', 'utánam', 'ellenem', 'mellettem'}
# A fedettseg.igei_tovek próbáján igeinek látszó, de vala előtt névszói szavak (köz → között, hely → helyett).
NEM_IGE = {'köz', 'hely', 'nyíl', 'erős', 'fel', 'meg', 'el', 'körül', 'szerint', 'mellett', 'között', 'mell', 'ala',
           'felett', 'alatt', 'előtt', 'helyett', 'ott', 'itt', 'fia', 'fiai', 'neve', 'feje'}

# A gyakori jegyes alakok kézi felülbírálása (modell-átnézés, F96.2): alak (kisbetűs) → mai alak, vagy
# None = a jegy hibás (nem régies igealak, nem változik). A szabály jelöltje itt nem jó.
KEZI = {
    'megkérdé': 'megkérdezte',  # a #94 lemmája: megkérd; a mai ige megkérdez
    'áldozék': 'áldozott',  # áldozik, E/3 (1Móz 8:20: és áldozék égőáldozattal)
    'eltemeték': 'eltemették',  # eltemet, T/3 tárgyas (1Móz 25:9: eltemeték őt ... az ő fiai)
    'eltemetteték': 'eltemettetett',  # szenvedő E/3 (1Móz 35:19: és eltemetteték)
    'megjelenék': 'megjelent',  # megjelenik, E/3 (1Móz 12:7: megjelenék az Úr)
    'érte': None,  # névutós névmás (érte = őérte), a jegy hibás
    'hivatá': 'hívatta',  # hivat → hívat (helyesírás) + tárgyas E/3
}
# A jegy nélküli régies gyanú (regies_gyanu) kézzel átnézett, gyakori alakjai (N-F96b): kisbetűs → mai.
GYANU_KEZI = {
    # jő-család (jön régies alakja) és a lészen (lesz)
    'jő': 'jön', 'eljő': 'eljön', 'kijő': 'kijön', 'feljő': 'feljön', 'bejő': 'bejön', 'jőnek': 'jönnek',
    'eljőnek': 'eljönnek', 'jőjjön': 'jöjjön', 'jőjj': 'jöjj', 'jőjjenek': 'jöjjenek',
    'lészen': 'lesz', 'meglészen': 'meglesz', 'lésznek': 'lesznek',
    # vőn, tőn (vesz, tesz régi múltja)
    'vőn': 'vett', 'tőn': 'tett', 'vőnek': 'vettek', 'tőnek': 'tettek',
    # -ák: tárgyas T/3 elbeszélő múlt (a #94 értékkészletéből hiányzik, N-F96b)
    'mondák': 'mondták', 'megmondák': 'megmondták', 'elmondák': 'elmondták', 'adák': 'adták',
    'találák': 'találták', 'láták': 'látták', 'megláták': 'meglátták', 'hallák': 'hallották',
    'meghallák': 'meghallották', 'elhozák': 'elhozták', 'kihozák': 'kihozták', 'előhozák': 'előhozták',
    'akarák': 'akarták', 'elbocsáták': 'elbocsátották', 'hagyák': 'hagyták', 'állíták': 'állították',
    'meghajták': 'meghajtották', 'elfoglalák': 'elfoglalták', 'megfogák': 'megfogták', 'imádák': 'imádták',
    'hányák': 'hányták', 'csinálák': 'csinálták',
    # alanyi E/3 és T/3 elbeszélő múlt jegy nélkül
    'álla': 'állt', 'állának': 'álltak', 'síra': 'sírt', 'sírának': 'sírtak', 'tére': 'tért',
    # v-tövű és szenvedő elbeszélő múlt
    'megharaguvék': 'megharagudott', 'megesküvék': 'megesküdött', 'elaluvék': 'elaludt', 'feküvék': 'feküdt',
    'lefeküvék': 'lefeküdt', 'találtaték': 'találtatott', 'vetteték': 'vettetett',
    'várván': 'várva',
}
# A határozói igenév kivételei: a mai irodalmi alak is -vén (lévén), nem változik.
IGENEV_KIVETEL = {'lévén', 'jövén', 'eljövén', 'feljövén', 'kijövén', 'bejövén', 'visszajövén', 'előjövén'}


def sha(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def nagy(minta, uj):
    return uj[:1].upper() + uj[1:] if minta[:1].isupper() else uj


def magas(szo):
    return ir.hang(szo) != 'o'


class Alakok:
    """Alakszintű igealak-jelöltek (szövegkörnyezet nélkül) és osztályok."""

    def __init__(self, tabla, gy, kis_szavak):
        self.tabla = tabla
        self.kis_szavak = kis_szavak
        self.igei = fedettseg.igei_tovek(tabla, kis_szavak)
        kis_gy = collections.Counter()
        for t, n in gy.items():
            kis_gy[t.lower()] += n
        jegyes_kis = {}
        for alak, s in tabla.items():
            if s['regies_jegy']:
                jegyes_kis[alak.lower()] = kis_gy.get(alak.lower(), 0)
        self.gyakori = set(k for k, _ in sorted(jegyes_kis.items(), key=lambda x: (-x[1], x[0]))[:fedettseg.GYAKORI_JEGYES])
        self.oszt = {}
        for alak in gy:
            sor = fedettseg.tablasor(tabla, alak)
            o, reszlet, _ = fedettseg.osztalyoz(alak, sor, self.gyakori, self.igei)
            self.oszt[alak] = (o, reszlet, sor)

    def bontas(self, alak, sor):
        """(igekötő, alapige) a lemma mai alakjából."""
        lemma = (sor['szotari_alak_mai'] or sor['szotari_alak']).lower()
        return ir.szetbont(lemma, self.kis_szavak)

    def jegy_jeloltek(self, alak, sor):
        """A jegy szerinti mai alak(ok): {'': x} egyértelműen, {'alanyi': x, 'targyas': y} vagy
        {'E1': x, 'T3': y} szövegkörnyezetfüggően; None, ha a szabály nem képez alakot."""
        jegy = sor['regies_jegy']
        kis = alak.lower()
        if jegy == 'hatarozoi_igenev':
            if kis in IGENEV_KIVETEL or not kis.endswith(('ván', 'vén')):
                return {}
            return {'': nagy(alak, kis[:-3] + ('va' if kis.endswith('ván') else 've'))}
        if jegy == 'felszolito.E2':
            return None  # DT-F96k (🟡): külön jelölt, nem csere
        if jegy not in JEGY_SZEM:
            return None
        kot, alap = self.bontas(alak, sor)
        if not kis.startswith(kot):
            return None
        szem, targy = JEGY_SZEM[jegy]
        if alap in TARGYAS_MINDIG:
            targy = True
        if jegy == 'mult.E1' and magas(alap) and kis.endswith('ék') and self.targyas_kepes(kot, alap):
            e1, t3 = ir.mult(alap, 'E1', False), ir.mult(alap, 'T3', True)
            if e1 and t3:
                return {'E1': nagy(alak, kot + e1), 'T3': nagy(alak, kot + t3)}
            return None
        if targy is None:
            a, t = ir.mult(alap, szem, False), ir.mult(alap, szem, True)
            if not a:
                return None
            if a == t or not self.targyas_kepes(kot, alap):
                return {'': nagy(alak, kot + a)}
            return {'alanyi': nagy(alak, kot + a), 'targyas': nagy(alak, kot + t)}
        m = ir.mult(alap, szem, targy)
        return {'': nagy(alak, kot + m)} if m else None

    def targyas_kepes(self, kot, alap):
        """Tárgyas-e az ige: tárgyas jelen (mondja, kéri, hozza) vagy tárgyas múlt (mondta) a korpuszban."""
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        jel = [v + 'ja', v + 'ják', v + 'i', ir.mult(alap, 'E3', True) or '']
        if v[-1:] in ('s', 'z'):
            jel += [v + v[-1] + 'a', v + v[-1] + 'ák']
        return any(j and ((kot + j) in self.kis_szavak or j in self.kis_szavak) for j in jel)

    def felszolito_jelolt(self, alak, sor):
        kis = alak.lower()
        if sor and sor['regies_jegy'] == 'felszolito.E2' and kis.endswith(('ál', 'él')):
            return alak[:-2]
        return None

    def gyanu_jelolt(self, alak, sor, reszlet):
        """A jegy nélküli régies gyanú szabály-jelöltje (az -ák/-ék T/3 tárgyas, a -taték, a jő-család)."""
        kis = alak.lower()
        if kis in GYANU_KEZI:
            return {'': nagy(alak, GYANU_KEZI[kis])}
        if reszlet in ('elemezetlen:-ák', 'elemezetlen:-ék'):
            kot, alap = ir.szetbont(kis[:-2], self.kis_szavak)
            m = ir.mult(alap, 'T3', True)
            return {'': nagy(alak, kot + m)} if m else None
        if reszlet.startswith('vegzodes:-'):
            veg = reszlet.split('-', 1)[1]
            kot, alap = self.bontas(alak, sor)
            szem = {'á': ('E3', True), 'é': ('E3', True), 'a': ('E3', False), 'e': ('E3', False),
                    'ának': ('T3', None), 'ének': ('T3', None), 'ák': ('T3', True), 'ék': ('T3', True),
                    'ál': ('E2', None), 'él': ('E2', None), 'ánk': ('T1', None), 'énk': ('T1', None),
                    'átok': ('T2', None), 'étek': ('T2', None)}.get(veg)
            if not szem or not kis.startswith(kot):
                return None
            s, t = szem
            m = ir.mult(alap, s, bool(t))
            return {'': nagy(alak, kot + m)} if m else None
        return None


def to_or(llm, alak_h, sor, alakok, reszlet=''):
    """DT-F96d tő-őr: az LLM-alak egy token, a kezdőbetű-állás egyezik, és hordozza az igekötőt és az
    igetövet (a rendhagyó igén a múlt tövét is); a változatlan válasz átmegy."""
    if not llm:
        return False
    if tokenek.tokenizal(llm) != [llm] or llm[:1].isupper() != alak_h[:1].isupper():
        return False
    o, a = llm.lower(), alak_h.lower()
    if o == a:
        return True
    tovek = []
    if sor and sor['szotari_alak'].lower() != a:
        kot, alap = alakok.bontas(alak_h, sor)
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        tovek.append(kot + v[:max(2, len(v) - 1)])
        if alap in ir.RENDHAGYO:
            e3, t = ir.RENDHAGYO[alap]
            tovek += [kot + e3[:max(2, len(e3) - 2)], kot + t[:max(2, len(t) - 1)]]
    else:
        veg = reszlet.split('-', 1)[1] if '-' in reszlet else ''
        to = a[:-len(veg)] if veg and a.endswith(veg) else a[:max(2, len(a) - 3)]
        tovek.append(to[:max(2, len(to) - 1)])
    return any(o.startswith(t) for t in tovek) and abs(len(o) - len(a)) <= 5


def llm_beolvas():
    ut = os.path.join(ROOT, LLM_TABLA)
    ki = {}
    if not os.path.exists(ut):
        return ki
    fej = None
    with open(ut, encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            ki[d['alak']] = d
    return ki


def tagmondat(spans, szoveg, i, irany):
    """Az i. token tagmondatbeli szomszédai (írásjelig, legfeljebb 7) az adott irányban."""
    ki = []
    j = i
    while len(ki) < 7:
        k = j + irany
        if k < 0 or k >= len(spans):
            break
        koz = szoveg[spans[j][1]:spans[k][0]] if irany > 0 else szoveg[spans[k][1]:spans[j][0]]
        if re.search(r'[.;:!?]', koz):
            break
        ki.append(k)
        j = k
    return ki


def targyas_e(spans, szoveg, i):
    """Határozott tárgy a tagmondatban (heurisztika, manual)."""
    koz_utan = szoveg[spans[i][1]:spans[i + 1][0]] if i + 1 < len(spans) else ''
    if i + 1 < len(spans) and ',' in koz_utan and spans[i + 1][2].lower() == 'hogy':
        return True
    if ':' in koz_utan:
        return True  # idézett beszéd
    for j in tagmondat(spans, szoveg, i, 1) + tagmondat(spans, szoveg, i, -1):
        w = spans[j][2].lower()
        if w in HATAROZOTT_TARGY:
            return True
        elo = spans[j - 1][2].lower() if j > 0 else ''
        if elo in ('a', 'az') and w.endswith('t') and len(w) > 2:
            return True
        if BIRTOKOS_TARGY.search(w) and len(w) > 4:
            return True
    return False


def e1_e(spans):
    return any(s[2].lower() in E1_JEL for s in spans)


class Feldolgozo:
    def __init__(self, alakok, alakszotar, dont, llm):
        self.a = alakok
        self.alakszotar = alakszotar
        self.dont = dont
        self.llm = llm
        self.alak_dontes = {}  # alak → (alkalmazas, jeloltek, szabaly)
        self.szamlalo = collections.Counter()

    def alak_info(self, alak):
        """(alkalmazás, jelöltek dict vagy None, szabály-címke) alakonként, gyorsítótárral.
        alkalmazás: 'szabaly' (automatikus), 'jelolt' (nem automatikus), 'vala', 'lon', 'vagyon', ''."""
        if alak in self.alak_dontes:
            return self.alak_dontes[alak]
        o, reszlet, sor = self.a.oszt[alak]
        kis = alak.lower()
        ki = ('', None, '')
        if kis in VALA:
            ki = ('vala', None, 'vala')
        elif kis in LON:
            ki = ('lon', {'': nagy(alak, LON[kis])}, 'lon')
        elif kis == 'vagyon':
            ki = ('vagyon', {'': nagy(alak, 'van')}, 'vagyon')
        elif kis in GYANU_KEZI:
            ki = ('szabaly', {'': nagy(alak, GYANU_KEZI[kis])}, 'gyanu_kezi')
        elif o == 'igealak_gyakori':
            if kis in KEZI:
                ki = ('szabaly', {'': nagy(alak, KEZI[kis])}, 'igealak_kezi') if KEZI[kis] else ('', None, 'jegyhiba_kezi')
            else:
                j = self.a.jegy_jeloltek(alak, sor)
                if j == {}:
                    ki = ('', None, 'igenev_kivetel')
                elif j:
                    ki = ('szabaly', j, 'igealak:' + sor['regies_jegy'])
                elif sor['regies_jegy'] == 'felszolito.E2':
                    f = self.a.felszolito_jelolt(alak, sor)
                    ki = ('jelolt', {'': f} if f else None, 'felszolito_E2')
                else:
                    ki = ('jelolt', None, 'igealak_nincs_szabaly')
        elif o == 'igealak_ritka':
            if sor['regies_jegy'] == 'felszolito.E2':
                f = self.a.felszolito_jelolt(alak, sor)
                ki = ('jelolt', {'': f} if f else None, 'felszolito_E2')
            else:
                j = self.a.jegy_jeloltek(alak, sor)
                ki = ('', None, 'igenev_kivetel') if j == {} else ('jelolt', j, 'igealak_ritka:' + sor['regies_jegy'])
        elif o == 'regies_gyanu':
            ki = ('jelolt', self.a.gyanu_jelolt(alak, sor, reszlet), 'gyanu:' + reszlet)
        if not ki[0] and sor and o in ('valtozatlan', 'regies_gyanu', 'helyesiras_tabla', 'helyesiras_szabaly'):
            # DT-F96k (🟡): a régies, kötőhangzós múlt (mondotta → mondta, szólott → szólt) jelölt, nem csere
            m = ir.kotohang_mult(self.alakszotar[alak][0], sor['szotari_alak_mai'] or sor['szotari_alak'],
                                 self.a.kis_szavak)
            if m and m in self.a.kis_szavak:
                ki = ('jelolt', {'': nagy(alak, m)}, 'kotohang_mult')
        self.alak_dontes[alak] = ki
        return ki

    def llm_jelolt(self, alak, alak_h):
        """(llm-alak, tő-őr) az LLM-táblából (kisbetűs kulcs); ('', '') ha nincs."""
        d = self.llm.get(alak.lower())
        if not d:
            return '', ''
        llm = nagy(alak_h, d['llm_alak'])
        o, reszlet, sor = self.a.oszt[alak]
        return llm, 'ok' if to_or(llm, alak_h, sor, self.a, reszlet) else 'bukott'

    def vers(self, igehely, szoveg):
        sorok_h, modern_h = helyesiras.vers_feldolgoz(igehely, szoveg, self.alakszotar, self.dont)
        spans = [(m.start(), m.end(), m.group(0)) for m in BETU.finditer(szoveg)]
        # [sorszam, 1908, .1-alak, modern, kieso, szabaly(.1), szabaly(.2), bizonytalan(.1), bizonytalan(.2), jelolt]
        t = [[s[0], s[1], s[2], s[2], s[3], s[4], '', s[5], '', ''] for s in sorok_h]
        for i, r in enumerate(t):
            if r[4]:
                continue
            alk, jel, cim = self.alak_info(r[1])
            if alk in ('szabaly', 'lon', 'vagyon') and jel:
                if alk == 'vagyon' and i > 0 and spans[i - 1][2].lower() in ('a', 'az'):
                    r[6] = 'vagyon_fonev_marad'
                    continue
                if alk == 'lon' and r[1].lower() == 'lőnek' and re.search(r'nyil|nyíl|íj', szoveg.lower()):
                    r[8] = 'lonek_lo'
                    continue
                r[3], r[6] = self.valaszt(jel, spans, szoveg, i, r), cim
            elif alk == 'jelolt':
                jl = []
                if jel:
                    jl.append('szabaly:' + '|'.join('%s%s' % (k + '=' if k else '', v) for k, v in jel.items()))
                llm, tor = self.llm_jelolt(r[1], r[2])
                if llm:
                    jl.append('llm:%s(%s)' % (llm, 'tő-őr ok' if tor == 'ok' else 'tő-őr bukott'))
                r[9] = '; '.join(jl)
                r[6] = cim
            elif alk == 'vala':
                self.vala(t, spans, szoveg, i)
        modern = self.szoveg(szoveg, spans, t)
        self.k2(igehely, szoveg, modern, t)
        return t, modern

    def valaszt(self, jel, spans, szoveg, i, r):
        if '' in jel:
            return jel['']
        if 'E1' in jel:
            r[8] = 'ek_E1_T3'
            return jel['E1'] if e1_e(spans) else jel['T3']
        r[8] = 'targyas_heur'
        return jel['targyas'] if targyas_e(spans, szoveg, i) else jel['alanyi']

    def vala(self, t, spans, szoveg, i):
        r = t[i]
        kis = r[1].lower()
        szem, volt = VALA[kis]
        elo_ok = i > 0 and szoveg[spans[i - 1][1]:spans[i][0]] == ' ' and not t[i - 1][4]
        if not elo_ok:
            r[3], r[6] = nagy(r[1], volt), 'vala_letige'
            return
        e = t[i - 1]
        ealak = e[1]
        o, reszlet, sor = self.a.oszt[ealak]
        ek = e[2].lower()  # a .1 utáni alak (szűlt → szült)
        if sor is None:
            r[3], r[6] = nagy(r[1], volt), 'vala_letige'
            return
        lemma = (sor['szotari_alak_mai'] or sor['szotari_alak']).lower()
        jegy = sor['regies_jegy']
        sajat_mult = False
        if not jegy and not (self.a.igei(lemma) or ir.ige_e(ir.szetbont(lemma, self.a.kis_szavak)[1], self.a.kis_szavak)):
            # a #94 elemezetlen vagy hibás sora (ülnek, jöttek, hallotta, szeret → szer): saját tőkeresés
            sajat_mult = ir.mult_lemma_nelkul(ek, self.a.kis_szavak)
            if not sajat_mult:
                for l in ir.lemma_jeloltek(ek, self.a.kis_szavak):
                    if ir.jelen_elemez(ek, l, self.a.kis_szavak):
                        lemma = l
                        break
        if jegy == 'hatarozoi_igenev' or (ek.endswith(('va', 've')) and ek != lemma and self.a.igei(sor['szotari_alak'])):
            r[3], r[6] = nagy(r[1], volt), 'vala_letige_igenev'
            return
        if jegy.startswith('mult.') or ek in VALA:
            self.kiesik(r, 'vala_segedige_mult')
            return
        if sajat_mult and ek not in ir.IGEKOTOK and lemma not in NEM_IGE:
            self.kiesik(r, 'vala_segedige_mult')
            return
        kot, alap = ir.szetbont(lemma, self.a.kis_szavak)
        if (ek in ir.IGEKOTOK or lemma in NEM_IGE or lemma in ('van', 'lesz') or ek.endswith('ni')
                or not (self.a.igei(lemma) or ir.ige_e(alap, self.a.kis_szavak))):
            r[3], r[6] = nagy(r[1], volt), 'vala_letige'
            return
        if self.mult_e(ek, kot, alap) or ir.mult_alak_e(ek, lemma, self.a.kis_szavak):
            self.kiesik(r, 'vala_segedige_mult')
            return
        je = ir.jelen_elemez(e[2], lemma, self.a.kis_szavak)
        if not je and o == 'regies_gyanu':
            self.kiesik(r, 'vala_segedige_mult')  # régies, nem jelen idejű igealak (írának vala)
            return
        if je:
            k2, alap2, sz, tg = je
            m = ir.mult(alap2, sz, tg)
            if m:
                uj = nagy(e[2], k2 + m)
                e[3] = uj
                e[6] = cimke(e[6], 'jelen_mult_vala')
                if uj.lower() not in self.a.kis_szavak:
                    e[8] = 'mult_korpuszban_nincs'
                self.kiesik(r, 'vala_segedige_jelen')
                return
        r[8] = 'vala_segedige'
        r[6] = 'vala_nem_elemezheto'

    def mult_e(self, ek, kot, alap):
        if not ek.startswith(kot):
            return False
        tv = ir.mult_tovek(alap)
        if tv is None:
            return False
        e3, to = tv
        resz = ek[len(kot):]
        if resz == e3 or resz.startswith(to):
            return True
        v = alap[:-2] if alap.endswith('ik') and len(alap) > 3 else alap
        return resz.startswith(v + ir.kotohang(v))  # mondotta, megmondotta, állottak

    def kiesik(self, r, cim):
        r[3] = ''
        r[4] = 'segedige'
        r[6] = cim

    def szoveg(self, szoveg, spans, t):
        ki = []
        poz = 0
        for i, (a, b, w) in enumerate(spans):
            if t[i][4] == 'osszevonva':
                ki.append(szoveg[poz:a])
                poz = spans[i + 1][0]
                continue
            if t[i][4] == 'segedige':
                poz = b  # az előtte álló egy szóköz és a vala kiesik
                continue
            ki.append(szoveg[poz:a])
            ki.append(t[i][3])
            poz = b
        ki.append(szoveg[poz:])
        return ''.join(ki)

    def k2(self, igehely, szoveg, modern, t):
        vart = [r[3] for r in t if not r[4]]
        if tokenek.tokenizal(modern) != vart:
            raise SystemExit('K2 hiba (tokenek): %s' % igehely)
        ves = sum(1 for r in t if r[4])
        vaz_e, vaz_m = BETU.sub('', szoveg), BETU.sub('', modern)
        if len(vaz_e) - len(vaz_m) != ves or vaz_m.replace(' ', '') != vaz_e.replace(' ', ''):
            raise SystemExit('K2 hiba (írásjel-váz): %s' % igehely)


def cimke(a, b):
    return a + '+' + b if a else b


def h_tokenek_beolvas():
    ki = []
    with open(os.path.join(ROOT, H_TOKENEK), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#') or l.startswith('igehely\t'):
                continue
            ki.append(tuple(l.rstrip('\n').split('\t')))
    return ki


def elokeszit():
    tabla = fedettseg.tabla_beolvas()
    versek = []
    with open(os.path.join(ROOT, KAROLI), encoding='utf-8') as f:
        next(f)
        for l in f:
            m = l.rstrip('\n').split('\t')
            if len(m) >= 2:
                versek.append((m[0], m[1]))
    gy = collections.Counter(t for _, sz in versek for t in tokenek.tokenizal(sz))
    kis_szavak = set(t.lower() for t in gy)
    alakszotar = {a: helyesiras.alak_modern(a, fedettseg.tablasor(tabla, a), kis_szavak) for a in gy}
    dont = helyesiras.ami_proba_keszit(tabla, fedettseg.igei_tovek(tabla, kis_szavak))
    alakok = Alakok(tabla, gy, kis_szavak)
    return tabla, versek, gy, kis_szavak, alakszotar, dont, alakok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', action='store_true')
    ap.add_argument('--minta-frissit', action='store_true')
    ap.add_argument('--kimenet', default=None)
    ap.add_argument('--llm-kerdes', default=None, help='az LLM-kérdések könyvtára (a repón kívül)')
    ap.add_argument('--koteg', type=int, default=560)
    ap.add_argument('--llm-valasz', default=None, help='az LLM-válaszok könyvtára (a repón kívül)')
    ap.add_argument('--modell', default=None)
    a = ap.parse_args()
    tabla, versek, gy, kis_szavak, alakszotar, dont, alakok = elokeszit()
    if a.llm_kerdes:
        llm_kerdes(a.llm_kerdes, a.koteg, versek, gy, alakok, alakszotar)
        return
    if a.llm_valasz:
        llm_valasz(a.llm_valasz, a.modell, alakok, alakszotar)
        return
    fd = Feldolgozo(alakok, alakszotar, dont, llm_beolvas())
    h_vart = set(h_tokenek_beolvas())
    h_kapott = set()
    vers_ki = {}
    for igehely, sz in versek:
        t, modern = fd.vers(igehely, sz)
        vers_ki[igehely] = (sz, modern, t)
        for r in t:
            if r[1] != r[2] or r[4] == 'osszevonva' or r[7]:
                h_kapott.add((igehely, str(r[0]), r[1], r[2] if r[4] != 'osszevonva' else '',
                              'osszevonva' if r[4] == 'osszevonva' else '', r[5], r[7]))
    if h_kapott != h_vart:
        raise SystemExit('a .1 újraszámolása eltér a %s-től: %d / %d sor eltér'
                         % (H_TOKENEK, len(h_kapott - h_vart), len(h_vart - h_kapott)))
    print('a .1 újraszámolva, egyezik a %s-vel (%d sor)' % (H_TOKENEK, len(h_vart)))
    kiir(vers_ki, gy, alakok, fd, a)


def bemenet_hash():
    return ('%s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s)%s'
            % (KAROLI, sha(KAROLI)[:12], SZOTARI, sha(SZOTARI)[:12], H_TOKENEK, sha(H_TOKENEK)[:12],
               SZKRIPT, sha(SZKRIPT)[:12], MODUL, sha(MODUL)[:12],
               (' + %s (sha256:%s)' % (LLM_TABLA, sha(LLM_TABLA)[:12])) if os.path.exists(os.path.join(ROOT, LLM_TABLA)) else ''))


def kiir(vers_ki, gy, alakok, fd, a):
    ki_dir = a.kimenet or os.path.join(ROOT, KI_DIR)
    os.makedirs(ki_dir, exist_ok=True)
    hk = bemenet_hash()
    fejlec = ('# GENERÁLT: %s (F96.2) — kézzel nem szerkeszthető; a javítás a szabályban vagy a KEZI / GYANU_KEZI '
              'táblában | forras=%s | a .1 (helyesiras.py) kimenetére épül, újraszámolva és összevetve | '
              'tokenizálás: tokenizal (a #22 hu_sorszam-a; Strong token-kulcson illeszthető, DT-F96f) | a ritka '
              'jegyes és a régies gyanús alak NEM automatikus csere (N-F94h): a jelolt oszlopban | LLM: az '
              'igealak_llm.tsv (DT-F96d, előfizetés, API nélkül), tő-őrrel\n' % (SZKRIPT, hk))
    tok_ki = []
    for igehely, (sz, modern, t) in vers_ki.items():
        for r in t:
            if r[1] != r[3] or r[4] or r[7] or r[8] or r[9]:
                tok_ki.append([igehely, str(r[0]), r[1], r[2], r[3], r[4], cimke(r[5], r[6]) if r[5] and r[6] else (r[5] or r[6]),
                               cimke(r[7], r[8]) if r[7] and r[8] else (r[7] or r[8]), r[9]])
    with open(os.path.join(ki_dir, 'igealak_tokenek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=a .1 + .2 után változó, kieső, bizonytalan vagy jelölt tokenek (%d) a %d '
                               'tokenből\n' % (len(tok_ki), sum(gy.values()))))
        f.write('\t'.join(['igehely', 'sorszam', 'alak_1908', 'alak_helyesiras', 'alak_modern', 'kieso', 'szabaly',
                           'bizonytalan', 'jelolt']) + '\n')
        for r in tok_ki:
            f.write('\t'.join(r) + '\n')
    # alakonként
    alak_ki = []
    for alak in sorted(gy):
        alk, jel, cim = fd.alak_info(alak)
        o, reszlet, sor = alakok.oszt[alak]
        if not (alk or o in ('igealak_gyakori', 'igealak_ritka', 'regies_gyanu', 'regies_lista')):
            continue
        llm, tor = fd.llm_jelolt(alak, fd.alakszotar[alak][0])
        sz = '|'.join('%s%s' % (k + '=' if k else '', v) for k, v in jel.items()) if jel else ''
        egy = ''
        if llm and jel:
            egy = 'egyezik' if llm in jel.values() else 'elter'
        alak_ki.append([alak, str(gy[alak]), o, reszlet, sor['regies_jegy'] if sor else '',
                        sor['szotari_alak'] if sor else '', alk or 'valtozatlan', cim, sz, llm, tor, egy])
    with open(os.path.join(ki_dir, 'igealak_alakok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=az igealak-osztályú és a vala/lőn/vagyon alakok (%d); alkalmazas: '
                               'szabaly = automatikus csere, jelolt = nem automatikus (a modern szöveg nem változik)\n'
                               % len(alak_ki)))
        f.write('\t'.join(['alak', 'gyakorisag', 'osztaly', 'reszlet', 'regies_jegy', 'szotari_alak', 'alkalmazas',
                           'szabaly', 'szabaly_jelolt', 'llm_alak', 'to_or', 'egyezes']) + '\n')
        for r in alak_ki:
            f.write('\t'.join(r) + '\n')
    osszesit(vers_ki, gy, alakok, fd, alak_ki)
    if a.minta:
        minta(vers_ki, ki_dir, fejlec, fd)
    elif a.minta_frissit:
        minta_frissit(vers_ki, ki_dir, fejlec, fd)
    print('bemenet: %s' % hk)


def osszesit(vers_ki, gy, alakok, fd, alak_ki):
    tokszam = sum(gy.values())
    valt_vers = sum(1 for v in vers_ki.values() if v[0] != v[1])
    c = collections.Counter()
    kieso = collections.Counter()
    biz = collections.Counter()
    marad = collections.Counter()
    marad_jelolt = collections.Counter()
    for sz, modern, t in vers_ki.values():
        for r in t:
            if r[4]:
                kieso[r[4]] += 1
            if r[6]:
                c[r[6].split(':')[0] if not r[6].startswith('igealak:') else r[6]] += 1
            if r[8]:
                biz[r[8]] += 1
            if not r[4] and r[3].lower() == r[2].lower():
                o = alakok.oszt[r[1]][0]
                kis = r[1].lower()
                if o in ('igealak_gyakori', 'igealak_ritka', 'regies_gyanu') or kis in VALA or kis in LON or kis == 'vagyon':
                    alk = fd.alak_info(r[1])[0]
                    if alk == 'szabaly' and r[3] == r[2] and not r[8]:
                        continue
                    marad[o if o != 'regies_lista' else 'regies_lista:' + kis] += 1
                    if r[9]:
                        marad_jelolt[o] += 1
    print('versek: %d, tokenek: %d; változó vers (.1 + .2): %d' % (len(vers_ki), tokszam, valt_vers))
    print('.2-szabályonként (token): %s' % dict(sorted(c.items(), key=lambda x: -x[1])))
    print('kieső token: %s' % dict(kieso))
    print('.2 bizonytalan (token): %s' % dict(biz))
    print('LEFEDETTSÉG — régies igealak a modern szövegben (token): %s; ebből jelölttel: %s'
          % (dict(sorted(marad.items(), key=lambda x: -x[1])), dict(marad_jelolt)))
    print('alakonként: %s' % dict(collections.Counter((r[2], r[6]) for r in alak_ki)))
    eg = collections.Counter((r[2], r[10], r[11]) for r in alak_ki if r[9])
    if eg:
        print('LLM: osztály × tő-őr × egyezés (alak): %s' % dict(sorted(eg.items())))


# ---- LLM (DT-F96d) -------------------------------------------------------------------------------

UTASITAS = """A Károli-biblia 1908-as szövegének szóalakjait modernizáljuk: csak a helyesírás és az igealak változik; a szókincs, a szórend és az írásjel NEM.
Minden sorban egy (már helyesírásilag javított) szóalak, a #94 szótári alakja, a régies jegy (ha van) és a versrészlet, amelyben az alak először áll (a szó ott [szögletes zárójelben]).
Feladat: add meg a szó mai alakját.
- Régies igealak → mai igealak, ugyanazzal az igével és igekötővel, személlyel és számmal: elbeszélt múlt (teremté → teremtette, felele → felelt, monda → mondta, mondának → mondták/mondtak, láték → láttam, lőn → lett, vevé → vette, adaték → adatott), határozói igenév (mondván → mondva), jő → jön. A tárgyas/alanyi ragozást a versrészlet szerint válaszd.
- Ha a szó nem régies igealak (főnév, névutó, mai alak, a -jék felszólító), a mai alak maga a szó, változatlanul.
- Egy szóból egy szó lesz: nem toldasz be és nem hagysz el szót, a szóválasztás marad (nem cseréled más igére). A kezdőbetű marad.
Kimenet: soronként `id<TAB>mai alak`, minden bemeneti sorra pontosan egy, más szöveg nélkül."""


def llm_kerdes(ki, koteg, versek, gy, alakok, alakszotar):
    """A nem automatikus (jelölt) alakok kérdései kisbetűs alakonként, az első előfordulás versrészletével."""
    if os.path.abspath(ki).startswith(ROOT):
        raise SystemExit('a kérdések a repón kívülre mennek')
    fd = Feldolgozo(alakok, alakszotar, None, {})
    kell = {}
    for alak in sorted(gy, key=lambda x: (x.lower(), x)):
        alk, jel, cim = fd.alak_info(alak)
        if alk == 'jelolt' and cim.startswith(('igealak_ritka', 'gyanu:')):  # a felszólító és a kötőhangzós múlt: DT-F96k
            kell.setdefault(alak.lower(), alak)
    elso = {}
    for igehely, sz in versek:
        sp = [m.group(0) for m in BETU.finditer(sz)]
        for i, w in enumerate(sp):
            k = w.lower()
            if k in kell and k not in elso:
                elso[k] = (igehely, ' '.join(sp[max(0, i - 8):i]) + ' [' + w + '] ' + ' '.join(sp[i + 1:i + 9]))
    sorok = []
    for n, k in enumerate(sorted(kell), 1):
        alak = kell[k]
        o, reszlet, sor = alakok.oszt[alak]
        sorok.append(['L%04d' % n, alakszotar[alak][0].lower(), sor['szotari_alak'] if sor else '',
                      sor['regies_jegy'] if sor else '', elso[k][1]])
    os.makedirs(ki, exist_ok=True)
    nk = 0
    for s in range(0, len(sorok), koteg):
        nk += 1
        with open(os.path.join(ki, 'kerdes_%02d.tsv' % nk), 'w', encoding='utf-8', newline='\n') as f:
            f.write('id\talak\tszotari_alak\tjegy\tversreszlet\n')
            for r in sorok[s:s + koteg]:
                f.write('\t'.join(r) + '\n')
    with open(os.path.join(ki, 'utasitas.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(UTASITAS + '\n')
    with open(os.path.join(ki, 'kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        for r in sorok:
            f.write('%s\t%s\n' % (r[0], r[1]))
    print('LLM-kérdés: %d alak, %d köteg → %s' % (len(sorok), nk, ki))


def llm_valasz(ki, modell, alakok, alakszotar):
    """A válaszfájlok (valasz_NN.tsv) és a hívásnapló (hivasok.jsonl) beolvasása az igealak_llm.tsv-be."""
    if not modell:
        raise SystemExit('--modell kötelező (a ténylegesen futott modell neve)')
    kulcs = {}
    with open(os.path.join(ki, 'kulcs.tsv'), encoding='utf-8') as f:
        for l in f:
            i, al = l.rstrip('\n').split('\t')
            kulcs[i] = al
    valasz = {}
    hibas = []
    for fn in sorted(os.listdir(ki)):
        if not re.match(r'valasz_\d+\.tsv$', fn):
            continue
        with open(os.path.join(ki, fn), encoding='utf-8') as f:
            for l in f:
                m = l.rstrip('\n').split('\t')
                if len(m) < 2 or m[0] not in kulcs:
                    if l.strip() and not l.startswith('id\t'):
                        hibas.append(l.rstrip('\n'))
                    continue
                valasz[m[0]] = m[1].strip()
    hiany = sorted(set(kulcs) - set(valasz))
    hivasok = []
    if os.path.exists(os.path.join(ki, 'hivasok.jsonl')):
        with open(os.path.join(ki, 'hivasok.jsonl'), encoding='utf-8') as f:
            hivasok = [json.loads(l) for l in f if l.strip()]
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    ut = os.path.join(ROOT, LLM_TABLA)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s --llm-valasz (F96.2, DT-F96d) — modell-kimenet (modell_ellenorizetlen), kézzel nem '
                'szerkeszthető | modell=%s (Claude Code, előfizetés, API nélkül) | scope=a nem automatikus (jelölt) '
                'igealakok kisbetűsen (%d kérdés, %d válasz, %d hiányzó) | token: %s | ts=%s\n'
                % (SZKRIPT, modell, len(kulcs), len(valasz), len(hiany),
                   sum(h.get('total_tokens', 0) for h in hivasok), ts))
        f.write('alak\tllm_alak\tkerdes_id\n')
        for i in sorted(kulcs):
            if i in valasz:
                f.write('%s\t%s\t%s\n' % (kulcs[i], valasz[i], i))
    with open(os.path.join(ROOT, LLM_NAPLO), 'w', encoding='utf-8', newline='\n') as f:
        for h in hivasok:
            f.write(json.dumps(h, ensure_ascii=False) + '\n')
    print('LLM-válasz: %d / %d; hiányzik: %d %s; értelmezhetetlen sor: %d %s'
          % (len(valasz), len(kulcs), len(hiany), hiany[:10], len(hibas), hibas[:5]))
    print('token (a hívásnaplóból): %d' % sum(h.get('total_tokens', 0) for h in hivasok))


# ---- minta -------------------------------------------------------------------------------------

RETEGEK = [  # (réteg, darab)
    ('igealak:mult.targyas.E3', 8), ('igealak:mult.alanyi.E3', 8), ('igealak:mult.E3', 4),
    ('igealak:mult.T3', 6), ('igealak:mult.E1', 4), ('igealak:hatarozoi_igenev', 6), ('igealak_egyeb', 4),
    ('targyas_heur', 8), ('ek_E1_T3', 4), ('lon', 6), ('vagyon', 2), ('gyanu_kezi', 6),
    ('vala_letige', 10), ('vala_segedige_mult', 8), ('vala_segedige_jelen', 10), ('vala_bizonytalan', 4),
    ('jelolt_ritka', 8), ('jelolt_gyanu', 6), ('felszolito_E2', 4), ('kotohang_mult', 4), ('valtozatlan', 4),
]


def minta_retegek(t):
    rek = set()
    for r in t:
        c = r[6]
        if c.startswith('igealak:'):
            j = c.split('+')[0]
            rek.add(j if j in ('igealak:mult.targyas.E3', 'igealak:mult.alanyi.E3', 'igealak:mult.E3',
                               'igealak:mult.T3', 'igealak:mult.E1', 'igealak:hatarozoi_igenev') else 'igealak_egyeb')
        for k in ('lon', 'vagyon', 'gyanu_kezi', 'vala_letige', 'vala_segedige_mult', 'vala_segedige_jelen',
                  'felszolito_E2', 'kotohang_mult'):
            if c.split('+')[0].startswith(k):
                rek.add(k if k != 'vala_letige' or c.startswith('vala_letige') else k)
        if r[8] in ('targyas_heur', 'ek_E1_T3'):
            rek.add(r[8])
        if r[8] == 'vala_segedige':
            rek.add('vala_bizonytalan')
        if r[9] and c.startswith('igealak_ritka'):
            rek.add('jelolt_ritka')
        if r[9] and c.startswith('gyanu:'):
            rek.add('jelolt_gyanu')
    return rek


def minta(vers_ki, ki_dir, fejlec, fd):
    rnd = random.Random(MAG)
    jelolt = collections.defaultdict(list)
    for ih, (sz, modern, t) in vers_ki.items():
        rek = minta_retegek(t)
        if not rek and sz == modern:
            rek.add('valtozatlan')
        for r in rek:
            jelolt[r].append(ih)
    valasztott, hasznalt = [], set()
    for reteg, db in RETEGEK:
        l = sorted(jelolt[reteg])
        rnd.shuffle(l)
        n = 0
        for ih in l:
            if n >= db:
                break
            if ih in hasznalt:
                continue
            hasznalt.add(ih)
            valasztott.append((reteg, ih))
            n += 1
    sorok = [minta_sor('G%03d' % i, reteg, ih, vers_ki) + ['', ''] for i, (reteg, ih) in enumerate(valasztott, 1)]
    minta_ir(sorok, ki_dir, fejlec, '')


def minta_frissit(vers_ki, ki_dir, fejlec, fd):
    ut = os.path.join(ki_dir, 'igealak_minta.tsv')
    regi = helyesiras.felhasznaloi_oszlopok(ut, ('minta_id',), ('reteg', 'igehely', 'ellenorzes', 'megjegyzes'))
    sorok = [minta_sor(k[0], v[0], v[1], vers_ki) + [v[2], v[3]] for k, v in sorted(regi.items())]
    minta_ir(sorok, ki_dir, fejlec, ' | a kiválasztás változatlan, a szabály szerint újraszámolva (--minta-frissit)')


def minta_sor(mid, reteg, ih, vers_ki):
    sz, modern, t = vers_ki[ih]
    valt, alt = [], []
    for r in t:
        if r[4] == 'osszevonva':
            valt.append('%d:%s→(összevonva)' % (r[0], r[1]))
        elif r[4] == 'segedige':
            valt.append('%d:%s→(kiesik, segédige)' % (r[0], r[1]))
        elif r[1] != r[3]:
            valt.append('%d:%s→%s%s' % (r[0], r[1], r[3], ' [.2]' if r[6] else ''))
        if r[8]:
            valt.append('%d:%s?(%s)' % (r[0], r[1], r[8]))
        if r[9]:
            alt.append('%d:%s→ %s' % (r[0], r[1], r[9]))
    return [mid, reteg, ih, sz, modern, '; '.join(valt), ' | '.join(alt)]


def minta_ir(sorok, ki_dir, fejlec, megj):
    with open(os.path.join(ki_dir, 'igealak_minta.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=rögzített magú (%d) rétegzett minta, %d vers; az ellenorzes és a '
                               'megjegyzes oszlopot a felhasználó tölti (jó / hibás; a jelölt soron A = a jelölt jó, '
                               'B = maradjon), a modell nem%s\n' % (MAG, len(sorok), megj)))
        f.write('\t'.join(['minta_id', 'reteg', 'igehely', 'szoveg_1908', 'szoveg_modern', 'valtozasok', 'jelolt',
                           'ellenorzes', 'megjegyzes']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    print('minta: %d vers; rétegenként: %s' % (len(sorok), dict(collections.Counter(s[1] for s in sorok))))


if __name__ == '__main__':
    main()
