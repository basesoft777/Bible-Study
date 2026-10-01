#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.17 — a mérőpilot záró jelentése (naplok/F21P_jelentes.md), a pilot-brief P6 szerint.

Minden szám szkriptkimenetből jön (a forrásfájlt a jelentés soronként megnevezi):
  f21p/meres_eredmeny.tsv (meres.py, P4 v1), f21p/meres_v2_eredmeny.tsv
  (meres.py --v2), f21p/koltseg_vetites.tsv (koltseg_vetit.py, P5),
  f21p/ingadozas.tsv (ingadozas.py), f21p/c_diff_besorolas.tsv és
  f21p/c_diff_f3v2_osszevetes.tsv (a (c) darabszámok — az Opus besorolása, nem
  mérés), f21p/futasnaplo.tsv (a pilot tényleges költsége), valamint a
  tokenek.py / f21p/sorrend_eltero_versek.tsv (a korlátok darabszámai).
A szöveges részek (döntési szabály, nyitott tételek, következmények) a
felhasználói döntések (PD1–PD10, DT19–DT21) rögzítései; ajánlás a #22-ről nincs.

Futtatás (a fenti szkriptek után):
    python eszkozok/karoli_strong/jelentes_f21p.py
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koltseg_vetit as kv_  # noqa: E402  (DT21 h: az F22-rétegbesorolás egy helyen)
import tokenek  # noqa: E402

F21P = os.path.join(tokenek.ROOT, 'f21p')
KIMENET = os.path.join(tokenek.ROOT, 'naplok', 'F21P_jelentes.md')
RETEGEK = ['R1', 'R2', 'R3', 'R4', 'Összes']


# a P3 és a P3b futásai (a P3c-futások — F3V3, F8V3, SONNETV3 — költsége a P3c-szakaszban; F21.82)
P3_FUTASOK = ('F1', 'F2', 'F3', 'F5', 'F6', 'F3V2')
P3B_FUTASOK = ('F1V2', 'F2V2', 'F5V2', 'F6V2', 'F3V2B', 'F4V2')
P3C_FUTASOK = ('F3V3', 'F8V3', 'SONNETV3')


def _naplo_p3_p3b():
    """A futásnapló P3- és P3b-sorai (a régi szakaszok számai ezekből; a P3c-futások nélkül)."""
    return [r for r in _tsv('futasnaplo.tsv') if r['futas'] in P3_FUTASOK + P3B_FUTASOK]


def _tsv(nev):
    with open(os.path.join(F21P, nev), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


class T:
    """Egy TSV kulcs szerinti kereséssel."""

    def __init__(self, nev, kulcsok):
        self.sorok = _tsv(nev)
        self.kulcsok = kulcsok

    def get(self, *ertek):
        for r in self.sorok:
            if all(r[k] == v for k, v in zip(self.kulcsok, ertek)):
                return r
        raise KeyError('%s: %s' % (self.kulcsok, ertek))


def pct(sz, nev):
    sz, nev = float(sz), float(nev)
    return '%.1f%% (%d/%d)' % (100 * sz / nev, sz, nev) if nev else '— (0/0)'


def _hanyad(r):
    return float(r['szamlalo']) / float(r['nevezo'])


def p3b_szakasz():
    """A P3b (prompt_v2, minden összeállítás) eredményszakasza a meres_p3b_eredmeny.tsv és a
    koltseg_vetites_p3b.tsv alapján (F21.27)."""
    mp = T('meres_p3b_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kp = T('koltseg_vetites_p3b.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])

    def g(sz, o, r, m):
        x = mp.get(sz, o, r, m)
        return pct(x['szamlalo'], x['nevezo']) if x['nevezo'] not in ('',) else x['szamlalo']

    def kc(o, r, sz=None):
        # az „Összes” az irányadó F22-vetítés; az R1–R4 a korábbi pilot-4-réteges tájékoztató sor (DT21 h)
        sz = sz or ('vetites' if r in ('Összes',) + tuple(kv_.F22_RETEGEK) else 'vetites_pilot4_tajekoztato')
        x = kp.get(sz, o, r, 'koltseg_usd')
        return '%s [%s–%s]' % (x['ertek'], x['also90'], x['felso90'])

    oss_mind = ['A (F1V2)', 'B (F2V2)', 'C (F3V2)', 'C (F3V2B)', 'A+B', 'A+B+C']
    minos = {(r['osszeallitas'], r['mero']): r for r in mp.sorok if r['szakasz'] == 'minosites'}
    ki = ['## P3b-eredmény (prompt_v2): minden összeállítás az arany v2-höz (forrás: meres_p3b_eredmeny.tsv, '
          'koltseg_vetites_p3b.tsv)', '',
          'Futások: A = F1V2, B = F2V2, C = F3V2 és F3V2B (két futás), A+B+C döntőbíró = F4V2, KJV nélkül F5V2/F6V2 — '
          'mind prompt_v2. A G4 bizonyossági szabály szó szerint (F22 brief 22.6): magas = A∩B (a KJV-ellentmondás '
          'feltétele gépileg nem értelmezhető, n.é.); kozepes = a döntőbíró linkje A vagy B egyikében; alacsony = hármas '
          'eltérés, vagy a vers kapuhibás maradt (A vagy B végleg kapuhibás: a C válasza, minden link alacsony). Az A+B '
          'döntőbíró nélkül: A∩B magas, minden más link alacsony (a jelentés értelmezése). Egymodelles összeállítás '
          '(A, B, C) a PD6 szerint nem minősíthető, csak mért számokat kap.', '',
          '### Összefoglaló (P3b)', '']
    for o in ('A+B', 'A+B+C'):
        a = minos[(o, 'minosites (kizárás nélküli régi arannyal)')]
        b = minos[(o, 'minosites (tájékoztató: 1Móz 6:17 kizárva)')]
        ki.append('- **%s: %s** (%s; mért, a kizárás nélküli régi arannyal — DT21 i). Tájékoztató (az 1Móz 6:17 '
                  'kizárásával, nem minősít): %s (%s).' % (o, a['szamlalo'], a['megjegyzes'], b['szamlalo'], b['megjegyzes']))
    ki.append('- Az A, a B és a C egymodelles összeállítás: a PD6 szerint nem minősíthető.')
    ki.append('- A Döntési szabály „Javaslat” pontjához (tények): rétegenként sem az A+B, sem az A+B+C nem teljesíti a '
              'rétegfeltételeket (l. lent), tehát a szabály szerinti eset: „egyik sem” — a bukott feltételek a táblákban.')
    ki += ['', '### Az öt feltétel összeállításonként és rétegenként', '',
           'Feltételek: (1) `magas` pontosság ≥ 98% rétegenként; (2) lefedettség ≥ 95%; (3) régi arany ≥ 95% (halmaz-'
           'definíció; a MÉRT érték a kizárás nélküli, a küszöb ehhez viszonyít — DT21 i; mellette TÁJÉKOZTATÓKÉNT az '
           '1Móz 6:17 nélküli érték); (4) vetített költség 90%-os felső széle ≤ 60 USD (teljes Biblia; az „Összes” sor '
           'az F22 műfaji öt réteg szerinti vetítés, DT21 h; az R1–R4 sorokban a réteg része a korábbi pilot-4-réteges '
           'besorolás szerint, tájékoztató); (5) vetített `alacsony` arány ≤ 10% (link-arány a végső '
           'kimenetben; a 200 versen / az aranyon). Egymodelles összeállításnál az (1) és az (5) n.é. (PD6); az (1) '
           'helyén az összpontosság tájékoztatásul áll.', '',
           '| összeállítás | réteg | (1) magas pontosság | (2) lefedettség | (3) régi arany: mért (kizárás nélkül) / tájékoztató (1Móz 6:17 nélkül) | (4) költség USD [90%] (Összes: F22; R1–R4: pilot-4, tájékoztató) | (5) alacsony: 200 vers / arany |',
           '|---|---|---|---|---|---|---|']
    for o in oss_mind:
        egym = o not in ('A+B', 'A+B+C')
        for r in RETEGEK:
            if egym:
                p1_ = 'n.é. (PD6); összpontosság: %s' % g('feltetelek', o, r, 'pontossag_osszes (tajekoztato, PD6)')
                al = 'n.é. (PD6)'
            else:
                p1_ = g('feltetelek', o, r, 'magas_pontossag')
                al = '%s / %s' % (g('feltetelek', o, r, 'alacsony_arany [200 vers]'), g('feltetelek', o, r, 'alacsony_arany [arany]'))
            ki.append('| %s | %s | %s | %s | %s / %s | %s | %s |' % (
                o, r, p1_, g('feltetelek', o, r, 'lefedettseg'), g('feltetelek', o, r, 'regi_arany_kizaras_nelkul'),
                g('feltetelek', o, r, 'regi_arany_kizarassal_tajekoztato'), kc(o, r), al))
    ki += ['', 'Egymodelles összeállításnál a lefedettség és a régi arany a kapun átment versekre vonatkozik (n a cellában); '
           'az A+B és az A+B+C mind a 60 aranyversre és mind a 200 versre.', '',
           '### Minősítés (csak A+B és A+B+C)', '', '| összeállítás | feltétel | eredmény | megjegyzés |', '|---|---|---|---|']
    for r in mp.sorok:
        if r['szakasz'] == 'minosites':
            ki.append('| %s | %s | %s | %s |' % (r['osszeallitas'], r['mero'], r['szamlalo'], r['megjegyzes']))
    ki += ['', '| összeállítás | réteg | rétegfeltételek (1, 2, 3, 5; a (4) összesen) | bukott |', '|---|---|---|---|']
    for r in mp.sorok:
        if r['szakasz'] == 'minosites_reteg':
            ki.append('| %s | %s | %s | %s |' % (r['osszeallitas'], r['reteg'], r['szamlalo'], r['megjegyzes']))
    ki += ['', '### Bizonyossági szintek (A+B+C, G4)', '',
           '| réteg | magas pontosság | kozepes pontosság | alacsony pontosság | eloszlás magas / kozepes / alacsony (200 vers) |',
           '|---|---|---|---|---|']
    for r in RETEGEK:
        ki.append('| %s | %s | %s | %s | %s / %s / %s |' % (
            r, g('feltetelek', 'A+B+C', r, 'magas_pontossag'), g('szintek', 'A+B+C', r, 'kozepes_pontossag'),
            g('szintek', 'A+B+C', r, 'alacsony_pontossag'), g('szintek', 'A+B+C', r, 'eloszlas_magas [200 vers]'),
            g('szintek', 'A+B+C', r, 'eloszlas_kozepes [200 vers]'), g('szintek', 'A+B+C', r, 'eloszlas_alacsony [200 vers]')))
    ki += ['', 'Érzékenység (a G4 „kapuhibás maradt” ágának másik olvasata: a kapuhibás versben a C túlélő modellel egyező '
           'linkje kozepes): alacsony arány a 200 versen %s, az aranyon %s (A+B+C (alt)); a minősítés ezen nem változna, '
           '%s' % (g('feltetelek', 'A+B+C (alt)', 'Összes', 'alacsony_arany [200 vers]'),
                   g('feltetelek', 'A+B+C (alt)', 'Összes', 'alacsony_arany [arany]'),
                   'mert az (5) ezzel az olvasattal sem teljesül.' if _hanyad(mp.get('feltetelek', 'A+B+C (alt)', 'Összes', 'alacsony_arany [200 vers]')) > 0.10
                   else 'az (5) ezzel az olvasattal teljesülne.'), '']
    # KJV v2
    d1 = mp.get('p4_kjv_hatas', 'KJV-val − KJV nélkül', 'R1', 'delta_magas_pontossag_szazalekpont [közös halmaz]')
    d2 = mp.get('p4_kjv_hatas', 'KJV-val vs KJV nélkül', 'R1', 'A–B_eltérés_relativ_csokkenes [közös halmaz (mind a négy átment)]')
    d3 = mp.get('p4_kjv_hatas', 'KJV-val vs KJV nélkül', 'R1', 'A–B_eltérés_relativ_csokkenes [saját halmaz (A és B átment)]')
    nk = mp.get('p4_kjv_hatas', 'KJV-val (F1V2/F2V2)', 'R1', 'magas (A∩B) arany_versek [közös halmaz]')
    mk1 = mp.get('p4_kjv_hatas', 'KJV-val (F1V2/F2V2)', 'R1', 'magas (A∩B) pontossag [közös halmaz]')
    mk0 = mp.get('p4_kjv_hatas', 'KJV nélkül (F5V2/F6V2)', 'R1', 'magas (A∩B) pontossag [közös halmaz]')
    ki += ['### KJV-támpont a v2-adaton (F1V2/F2V2 vs F5V2/F6V2, R1)', '',
           '- `magas` (A∩B) pontosság a közös halmazon (mind a négy futás átment: %s/%s R1-aranyvers): KJV-val %s, KJV '
           'nélkül %s; különbség %s százalékpont (küszöb: ≥ +1).' % (nk['szamlalo'], nk['nevezo'], pct(mk1['szamlalo'], mk1['nevezo']),
                                                                  pct(mk0['szamlalo'], mk0['nevezo']), d1['szamlalo']),
           '- Az A–B eltérés relatív csökkenése: közös halmazon %s%%, saját halmazokon %s%% (küszöb: ≥ 20%%; %s; %s).' % (
               d2['szamlalo'], d3['szamlalo'], d2['megjegyzes'], d3['megjegyzes']),
           '- A közös halmaz %s aranyvers: a kiválasztás torzít (csak azok a versek, ahol mind a négy futás kapun átment; '
           'a KJV-val futó A és B más verseken bukik, mint a KJV nélküli). Az 1. küszöb-mérőszám formálisan teljesül, a '
           '2. nem; a kis n miatt nem végleges.' % nk['szamlalo'], '']
    # ingadozás
    ki += ['### A C két futása (F3V2 vs F3V2B, azonos prompt): futásközi ingadozás', '',
           '| réteg | mérőszám | F3V2 | F3V2B | Δ | Δ 90% | |Δ| 95. percentilis |', '|---|---|---|---|---|---|---|']
    for r in mp.sorok:
        if r['szakasz'] == 'c_ingadozas' and '|' in r['szamlalo']:
            x, y, d = (float(v) for v in r['szamlalo'].split('|'))
            lo, hi, ab = (float(v) for v in r['nevezo'].split('|'))
            ki.append('| %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp |' % (
                r['reteg'], r['mero'], 100 * x, 100 * y, 100 * d, 100 * lo, 100 * hi, 100 * ab))
    import c_diff_f3v2b as cb
    import meres_p3b
    ad = meres_p3b.betolt()
    _, e2, eb, kezi = cb.ellenoriz(ad)
    o2 = cb.f3v2_osztaly()
    kozos = set(e2) & set(eb)
    c2 = {k for k in e2 if o2.get(k) == 'c'}
    cbb = {k for k in eb if (o2.get(k) if k in kozos else kezi[k]['osztaly']) == 'c'}
    ki += ['', 'A (c)-esetek (az Opus besorolása, nem mérés; naplok/F21P_C_diff_F3V2B.md): F3V2 %d, F3V2B %d; azonos %d, '
           'új az F3V2B-nél %d, az F3V2-nél volt, az F3V2B-nél nincs %d. Eltérés az aranyhoz: F3V2 %d, F3V2B %d, ebből '
           'közös %d.' % (len(c2), len(cbb), len(c2 & cbb), len(cbb - c2), len(c2 - cbb), len(e2), len(eb), len(kozos))]
    ki += ['', 'Azonos linkhalmazú vers: %s az aranyon, %s a mintán; linkegyezés Σ|∩|/Σ|∪| %s (arany), %s (minta). '
           'Azonos prompt és konfiguráció mellett ez a futásközi ingadozás becslése (egy futáspárból); a (c)-hibák egy '
           'része futásról futásra cserélődik.' % (
               g('c_ingadozas', 'F3V2 vs F3V2B', 'Összes', 'azonos_linkhalmazu_versek [arany]'),
               g('c_ingadozas', 'F3V2 vs F3V2B', 'Összes', 'azonos_linkhalmazu_versek [minta]'),
               g('c_ingadozas', 'F3V2 vs F3V2B', 'Összes', 'link_egyezes [arany]'),
               g('c_ingadozas', 'F3V2 vs F3V2B', 'Összes', 'link_egyezes [minta]')), '']
    # kapuhiba
    ki += ['### Kapuhiba v1 és v2 (első próbára / végleg; érvénytelen JSON első próbára)', '',
           '| futás | első próbára | végleg | JSON-hiba (1. kapupont) első próbára | végleg |', '|---|---|---|---|---|']
    for o in ('A v1 (F1)', 'A v2 (F1V2)', 'B v1 (F2)', 'B v2 (F2V2)', 'C v1 (F3)', 'C v2 (F3V2)', 'C (2. futás) v2 (F3V2B)',
              'A KJV nélkül v1 (F5)', 'A KJV nélkül v2 (F5V2)', 'B KJV nélkül v1 (F6)', 'B KJV nélkül v2 (F6V2)', 'C döntőbíró v2 (F4V2)'):
        try:
            je = g('kapuhiba_tipus', o, 'Összes', 'kapupont_1-json_elso')
            jv = g('kapuhiba_tipus', o, 'Összes', 'kapupont_1-json_vegleg')
        except KeyError:
            je = jv = 'nincs ilyen hiba'
        ki.append('| %s | %s | %s | %s | %s |' % (o, g('kapuhiba', o, 'Összes', 'elso_probara'), g('kapuhiba', o, 'Összes', 'vegleg'), je, jv))
    f4 = 'C döntőbíró v2 (F4V2)'
    ki += ['', 'A döntőbíró (F4V2) versei: az F1V2/F2V2 eltérő vagy kapuhibás versei, %s. Az első próbás kapuhibát a teljes '
           'kapun számoljuk (ötpontos kapu + 6. pont: az A–B rögzítés, futtat.biro_kenyszer, ahogy a futtató a futáskor '
           'ellenőrizte): első próbára %s, végleg %s. Kapupontonként első próbára: 1. pont %s, 1-json %s, 3. pont %s, '
           '4. pont %s, 6. pont (rögzítés-sértés) %s.' % (
               mp.get('kapuhiba', f4, 'Összes', 'vegleg')['nevezo'], g('kapuhiba', f4, 'Összes', 'elso_probara'),
               g('kapuhiba', f4, 'Összes', 'vegleg'), g('kapuhiba_tipus', f4, 'Összes', 'kapupont_1_elso'),
               g('kapuhiba_tipus', f4, 'Összes', 'kapupont_1-json_elso'), g('kapuhiba_tipus', f4, 'Összes', 'kapupont_3_elso'),
               g('kapuhiba_tipus', f4, 'Összes', 'kapupont_4_elso'), g('kapuhiba_tipus', f4, 'Összes', 'kapupont_6_elso')),
           '**Megfigyelés (nem feltétel):** legalább %s versben a C első válasza megsértette az A–B rögzítést; a 6. pontos '
           'kényszer és az egy újrakérés mindet javította (végleg %s).' % (
               mp.get('kapuhiba_tipus', f4, 'Összes', 'kapupont_6_elso')['szamlalo'],
               '%s/%s' % (mp.get('kapuhiba', f4, 'Összes', 'vegleg')['szamlalo'], mp.get('kapuhiba', f4, 'Összes', 'vegleg')['nevezo'])),
           'Keresztellenőrzés (az újraszámolt első próbás hibás versek = a jsonl probalkozas=2 versei = a futásnapló '
           'kapuhiba_db összege az első próbálkozásokon): %s.' % '; '.join(
               '%s %s = %s: %s' % (r['osszeallitas'], r['szamlalo'], r['nevezo'], r['megjegyzes'].split(': ')[-1]) for r in mp.sorok if r['szakasz'] == 'kapuhiba_kereszt'),
           'A mentett (kapun átment) válaszok újraellenőrzése a teljes kapun (futtat.mentett_valaszok_ellenoriz): %s.' % '; '.join(
               '%s: %s hiba' % (r['osszeallitas'], r['szamlalo']) for r in mp.sorok if r['szakasz'] == 'mentett_ellenorzes'), '']
    # P5
    F22 = list(kv_.F22_RETEGEK)
    ki += ['### P5 minden összeállításra (teljes Biblia, 90%-os intervallum)', '',
           '**Eltérés a brieftől:** a bootstrap egysége a köteg, nem a vers — DT21 f): **elfogadva (felhasználói döntés)**. '
           'Az ár a modell táblaára × a futás mért cost/táblaár aránya (az A-nál és a B-nél a cost nem egyenlő a táblaárral).', '',
           '**Rétegbesorolás (DT21 h, felhasználói döntés):** a teljes Biblia vetítése az F22 brief 22.2 **műfaji** (nem '
           'kánon szerinti) öt rétege szerint készül: %s. A 22.2 szövegén túli könyveket a felhasználó sorolta be: %s. A '
           'pilot mérési rétegei (R1–R4, minta.tsv, arany v2) nem változnak; a minta versei a döntőbírói arányhoz és a '
           'kézimunkához könyv szerint képeződnek le az F22-rétegekre (Péld az R1-ből a költészethez; az R4 evangéliumai '
           'az evangélium+ApCsel, levelei a levél+Jel réteghez). A korábbi pilot-4-réteges besorolás alább tájékoztatóként áll.' % (
               '; '.join('%s (%s)' % (r, ', '.join(kv_.F22_RETEG_KONYVEK[r])) for r in F22),
               ', '.join('%s → %s' % (k, v) for k, v in kv_.F22_FELHASZNALOI_BESOROLAS.items())), '',
           '**A leképezés még nyitott része (nem egyértelmű):** az ApCsel és a Jel nincs a pilotmintában, ezért a '
           'mintában nincs az F22 szerinti evangélium+ApCsel és levél+Jel réteg-pontos mérése: e két réteg döntőbírói '
           'aránya és kézimunka-rátája csak az evangéliumok, illetve a levelek mintaverseiből jön, és a vetítés az '
           'ApCsel/Jel verseire is ezt alkalmazza (a token-illesztés rétegfüggetlen, azt nem érinti). Az öt F22-réteg a '
           'pilot négy mérési rétegével szemben: a mérési táblák R1–R4-ek maradnak, az öt réteg csak a vetítésben él.', '',
           '| összeállítás | %s | Összes (F22) |' % ' | '.join(F22), '|---|' + '---|' * (len(F22) + 1)]
    for o in oss_mind + ['C döntőbíró rész']:
        ki.append('| %s | %s |' % (o, ' | '.join(kc(o, r, 'vetites') for r in F22 + ['Összes'])))
    ki += ['', 'Tájékoztató: a korábbi pilot-4-réteges besorolás szerint (ugyanazzal a bootstrap-mintával):', '',
           '| összeállítás | R1 | R2 | R3 | R4 | Összes (pilot-4) |', '|---|---|---|---|---|---|']
    for o in oss_mind + ['C döntőbíró rész']:
        ki.append('| %s | %s |' % (o, ' | '.join(kc(o, r, 'vetites_pilot4_tajekoztato') for r in RETEGEK)))
    ki += ['', 'A két besorolás költségkülönbsége (tájékoztató; F22 műfaji 5 réteg − korábbi pilot-4 réteg, pont-becslés):', '',
           '| összeállítás | F22 USD | pilot-4 USD | különbség USD | különbség % |', '|---|---|---|---|---|']
    for o in oss_mind + ['C döntőbíró rész']:
        ki.append('| %s | %s | %s | %s | %s%% |' % (
            o, kp.get('vetites', o, 'Összes', 'koltseg_usd')['ertek'], kp.get('vetites_pilot4_tajekoztato', o, 'Összes', 'koltseg_usd')['ertek'],
            kp.get('besorolas_kulonbseg_tajekoztato', o, 'Összes', 'f22_minus_pilot4_usd')['ertek'],
            kp.get('besorolas_kulonbseg_tajekoztato', o, 'Összes', 'f22_minus_pilot4_szazalek')['ertek']))
    ki += ['', 'Az egymodelles összeállításoknál a különbség csak a rétegenkénti ceil(N/10) kötegszám kerekítéséből jön (az '
           'illesztés rétegfüggetlen); az A+B+C-nél a döntőbírói versarány rétegenkénti súlyozása is változik.', '',
           '| futás | cost/táblaár (s) | újrakérés-szorzó M | ellenőrzés mintán belül | leave-one-out | **számító (DT21 g: a konzervatívabb)** |',
           '|---|---|---|---|---|---|']
    for f in ('F1V2', 'F2V2', 'F3V2', 'F3V2B', 'F4V2'):
        sz = kp.get('ellenorzes', f, '-', 'szamito_elteres_szazalek')
        ki.append('| %s | %s | %s | %s%% | %s%% | %s%% (%s) |' % (
            f, kp.get('ar', f, '-', 'cost1_per_tablaar_s')['ertek'], kp.get('ar', f, '-', 'ujrakeres_szorzo_M')['ertek'],
            kp.get('ellenorzes', f, '-', 'elteres_szazalek')['ertek'], kp.get('ellenorzes', f, '-', 'loo_elteres_szazalek')['ertek'],
            sz['ertek'], sz['megjegyzes'].split('számít: ')[-1]))
    ki += ['', 'DT21 g) (felhasználói döntés): a mintán belüli és a leave-one-out ellenőrzés közül a konzervatívabb — a '
           'nagyobb abszolút eltérésű — számít a ≤ 10%%-os küszöbhöz; ez minden futásnál a leave-one-out (a mintán belüli '
           'illesztés a saját hívásait közel 0 eltéréssel adja vissza). Az A+B+C összesített ellenőrzése (%s%%) csak '
           'mintán belüli; a futásonkénti leave-one-out a fenti táblában.' % kp.get('ellenorzes', 'A+B+C', '-', 'elteres_szazalek')['ertek']]
    naplo = _naplo_p3_p3b()
    ki.append('')
    ki.append('A pilot tényleges költsége (futásnapló, minden futás, P3 és P3b): %.6f USD. A C (F3V2) vetítés intervalluma '
              'itt kissé eltér a P3-as koltseg_vetites.tsv-étől, mert a két szkript bootstrapja más véletlenszám-sorrendet '
              'használ (azonos mag mellett).' % sum(float(r['koltseg_usd']) for r in naplo))
    ki.append('')
    ki.append('Döntőbírói versarány F22-rétegenként (F4V2; a minta versei könyv szerint leképezve): %s. Tájékoztató, '
              'pilot-rétegenként: %s. Kézimunka-vetítés (A+B+C, G4; F22-rétegenként): vetített `alacsony` link a '
              'Bibliára %s (alt olvasat: %s); vetített eltérés az aranyhoz mérten %s; a (c)-hiba/vers az A+B+C-re n.é. '
              '(nincs besorolva). Tájékoztató, a pilot-4-réteges besorolással: `alacsony` %s (alt: %s), eltérés %s.' % (
                  ', '.join('%s %s' % (r, kp.get('dontobiro', 'F4V2', r, 'dontobirohoz_meno_versek_aranya')['megjegyzes'].split(' (')[0]) for r in F22),
                  ', '.join('%s %s' % (r, kp.get('dontobiro_pilot4_tajekoztato', 'F4V2', r, 'dontobirohoz_meno_versek_aranya')['megjegyzes'].split(': ')[-1].split(' (')[0]) for r in RETEGEK[:4]),
                  kp.get('kezimunka', 'A+B+C', 'Összes', 'vetitett_alacsony_link_biblia')['ertek'],
                  kp.get('kezimunka', 'A+B+C (alt)', 'Összes', 'vetitett_alacsony_link_biblia')['ertek'],
                  kp.get('kezimunka', 'A+B+C', 'Összes', 'vetitett_elteres_biblia')['ertek'],
                  kp.get('kezimunka_pilot4_tajekoztato', 'A+B+C', 'Összes', 'vetitett_alacsony_link_biblia')['ertek'],
                  kp.get('kezimunka_pilot4_tajekoztato', 'A+B+C (alt)', 'Összes', 'vetitett_alacsony_link_biblia')['ertek'],
                  kp.get('kezimunka_pilot4_tajekoztato', 'A+B+C', 'Összes', 'vetitett_elteres_biblia')['ertek']))
    ki.append('')
    ki.append('*A lenti szakaszok a P3 (a P3b előtti) adatát őrzik változatlanul (v1-A/B, F3/F3V2); a P3b-eredmény a fenti.*')
    ki.append('')
    return ki


# ---------------------------------------------------------------------------
# F21.82: a regressziós mérés (P3c) vezető szakasza, a #22-javaslat szakasza, a régi számok összevetése
# ---------------------------------------------------------------------------

P3C_FORRAS = ('f21p/meres_p3c_eredmeny.tsv, f21p/koltseg_vetites_p3c.tsv, f21p/c_diff_p3c_besorolas.tsv, '
              'f21p/kjv_meres_eredmeny.tsv, f21p/elopar_kjv_eredmeny.tsv, f21p/meres_p3c_c_eredmeny.tsv')


def _ar(t, sz, o, r, m):
    x = t.get(sz, o, r, m)
    return pct(x['szamlalo'], x['nevezo']) if x['nevezo'] not in ('',) else x['szamlalo']


def _usd(t, o, r):
    x = t.get('vetites', o, r, 'koltseg_usd')
    return '%s [%s–%s]' % (x['ertek'], x['also90'], x['felso90'])


def _genezis_versek():
    """(az 1Móz versszáma, az 1Móz 1–5 versszáma) a Károli-kivonatból (tokenek.betolt_karoli)."""
    kar = tokenek.betolt_karoli()
    gen = [ig for ig in kar if ig.startswith('1Móz ')]
    g15 = [ig for ig in gen if int(ig.split(' ')[1].split(':')[0]) <= 5]
    return len(gen), len(g15)


def _dt21_hatas(bes):
    """{DT21-betű: (segített, nem segített, ártott)} az F3V3-sorokból (c_diff_p3c logikája: megszűnt/átsorolt = segített,
    maradt = nem segített, új (c) = ártott), a változás-konvenció DT21-hozzárendelésével."""
    import c_diff_p3c as cdp
    ki = {b: [0, 0, 0] for b in 'abcde'}
    for r in bes:
        if r['futas'] != 'F3V3':
            continue
        volt = ':c' in r['elozmeny_v2']
        if r['statusz'] in ('megszunt', 'nem_merheto'):
            al = 0
        elif r['statusz'] == 'elteres' and volt and r['osztaly'] in ('a', 'b'):
            al = 0
        elif r['statusz'] == 'elteres' and volt and r['osztaly'] == 'c':
            al = 1
        elif r['statusz'] == 'elteres' and r['osztaly'] == 'c':
            al = 2
        else:
            continue
        b = cdp.dt21(r['valtozas_konvencio'], r['igehely'])
        if b:
            ki[b][al] += 1
    return ki


def p3c_szakasz():
    """A regressziós mérés (P3c) összefoglalója és a végleges eredmény (vezető szakasz)."""
    import c_diff_p3c as cdp
    mc = T('meres_p3c_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kc = T('koltseg_vetites_p3c.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    mb = T('meres_p3b_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kb = T('koltseg_vetites_p3b.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kj = T('kjv_meres_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    ej = T('elopar_kjv_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    mcc = T('meres_p3c_c_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    bes = _tsv('c_diff_p3c_besorolas.tsv')
    S, C3_, PAR = 'Sonnet (SONNETV3)', 'C (F3V3)', 'Sonnet+C'
    R4_ = ['R1', 'R2', 'R3', 'R4']

    def bukott(t, o):
        return t.get('minosites', o, 'Összes', 'minosites (kizárás nélküli régi arannyal)')

    def bukott_t(t, o):
        return t.get('minosites', o, 'Összes', 'minosites (tájékoztató: 1Móz 6:17 kizárva)')
    ki = ['## A regressziós mérés (P3c, prompt_v3) — összefoglaló és végleges eredmény (F21.82)', '',
          'Források: %s; a régi P3/P3b-adat: f21p/meres_p3b_eredmeny.tsv, f21p/koltseg_vetites_p3b.tsv; a költség: '
          'f21p/futasnaplo.tsv. A P3c az arany **v3**-ra mér, a P3b az arany **v2**-re (a két arany 3 linkben tér el; l. '
          'naplok/F21P_meres_p3c_c.md). A korrigált értékek kizárólag „Opus-besorolás, nem mérés” jelöléssel; a küszöb '
          'szempontjából csak a mért érték számít.' % P3C_FORRAS, '',
          '### Végleges eredmény a Döntési szabály szerint: egyik összeállítás sem felel meg', '']
    for t, o, cim in ((mb, 'A+B', 'A+B (P3b, prompt_v2, arany v2)'), (mb, 'A+B+C', 'A+B+C (P3b, prompt_v2, arany v2)'),
                      (mc, PAR, 'Sonnet + C pár (P3c: A = SONNETV3, B = F3V3, prompt_v3, arany v3; döntőbíró nélkül)')):
        a, b = bukott(t, o), bukott_t(t, o)
        ki.append('- **%s: %s** — %s (tájékoztató, 1Móz 6:17 nélkül: %s — %s).' % (cim, a['szamlalo'], a['megjegyzes'], b['szamlalo'], b['megjegyzes']))
    f1 = mc.get('minosites', PAR, 'Összes', 'feltetel_1')
    ki += ['- A Sonnet + C pár (1) feltétele: **%s** (%s): a Sonnet R3-aranyversei a 15. köteg length-lezárása miatt végleg '
           'kapuhibásak; a próféták előtt pótolandó, pótló futás most nincs (PD19 (1)).' % (f1['szamlalo'], f1['megjegyzes']),
           '- Az egymodelles összeállítások (A, B, C — F3V2, F3V2B, F3V3 —, Sonnet) a PD6 szerint nem minősíthetők; csak mért számaik vannak.', '',
           '### (a) Az öt feltétel összeállításonként (Összes; az (1) rétegenként)', '',
           'Feltételek: (1) `magas` pontosság ≥ 98% rétegenként; (2) lefedettség ≥ 95%; (3) régi arany ≥ 95% (mért = kizárás '
           'nélkül; tájékoztató = 1Móz 6:17 nélkül); (4) a vetített teljes költség 90%-os felső széle ≤ 60 USD; (5) `alacsony` '
           'arány ≤ 10% (a 200 versen mért link-arány; a Sonnet + C-nél a teljes Bibliára vetített is). Egymodelles '
           'összeállításnál az (1) helyén az összpontosság (tájékoztató, PD6), az (5) n.é.', '',
           '| összeállítás | (1) magas pontosság R1 / R2 / R3 / R4 | (2) lefedettség | (3) régi arany: mért / tájékoztató | (4) költség USD [90%] | (5) alacsony | minősítés |',
           '|---|---|---|---|---|---|---|']
    for t, k, o, nev in ((mb, kb, 'A+B', 'A+B (P3b)'), (mb, kb, 'A+B+C', 'A+B+C (P3b)'), (mc, kc, PAR, 'Sonnet + C (P3c)')):
        p1_ = ' / '.join(_ar(t, 'feltetelek', o, r, 'magas_pontossag') for r in R4_)
        al = _ar(t, 'feltetelek', o, 'Összes', 'alacsony_arany [200 vers]')
        if o == PAR:
            v = mc.get('minosites_reszlet', PAR, 'Összes', 'feltetel_5_alacsony_arany_vetitett')
            al += '; vetítve %.1f%%' % (100 * float(v['szamlalo']))
        ki.append('| %s | %s | %s | %s / %s | %s | %s | %s (%s) |' % (
            nev, p1_, _ar(t, 'feltetelek', o, 'Összes', 'lefedettseg'), _ar(t, 'feltetelek', o, 'Összes', 'regi_arany_kizaras_nelkul'),
            _ar(t, 'feltetelek', o, 'Összes', 'regi_arany_kizarassal_tajekoztato'), _usd(k, o, 'Összes'), al,
            bukott(t, o)['szamlalo'], bukott(t, o)['megjegyzes']))
    for t, k, o, nev in ((mb, kb, 'A (F1V2)', 'A (F1V2, P3b)'), (mb, kb, 'B (F2V2)', 'B (F2V2, P3b)'), (mb, kb, 'C (F3V2)', 'C (F3V2, P3b)'),
                         (mb, kb, 'C (F3V2B)', 'C (F3V2B, P3b)'), (mc, kc, C3_, 'C (F3V3, P3c)'), (mc, kc, S, 'Sonnet (SONNETV3, P3c)')):
        ki.append('| %s | n.é. (PD6); összpontosság %s | %s | %s / %s | %s | n.é. (PD6) | nem minősíthető (PD6) |' % (
            nev, _ar(t, 'feltetelek', o, 'Összes', 'pontossag_osszes (tajekoztato, PD6)'), _ar(t, 'feltetelek', o, 'Összes', 'lefedettseg'),
            _ar(t, 'feltetelek', o, 'Összes', 'regi_arany_kizaras_nelkul'), _ar(t, 'feltetelek', o, 'Összes', 'regi_arany_kizarassal_tajekoztato'),
            _usd(k, o, 'Összes')))
    ki += ['', 'Egymodelles összeállításnál a lefedettség és a régi arany a kapun átment versekre vonatkozik (n a cellában); a '
           'Sonnet kapun átment aranyversei: %s.' % _ar(mc, 'feltetelek', S, 'Összes', 'arany_versek_kapun_atment'), '']
    # (b) a C három futása
    ki += ['### (b) A C (F3V3) a v2-es C-futásokkal egymás mellett, arany v3 (meres_p3c_eredmeny.tsv)', '',
           '| futás | mérőszám | R1 | R2 | R3 | R4 | Összes |', '|---|---|---|---|---|---|---|']
    for o in ('C (F3V2)', 'C (F3V2B)', C3_):
        for m in ('pontossag_osszes (tajekoztato, PD6)', 'lefedettseg'):
            ki.append('| %s | %s | %s |' % (o, m.split(' ')[0], ' | '.join(_ar(mc, 'feltetelek', o, r, m) for r in RETEGEK)))
        for m in ('elso_probara', 'vegleg'):
            ki.append('| %s | kapuhiba %s | %s |' % (o, m, ' | '.join(_ar(mc, 'kapuhiba', o, r, m) for r in RETEGEK)))
    ki += ['', 'A prompt_v2 → v3 hatás: Δ = F3V3 − a két v2-futás átlaga (azonos aranyon), 90%-os bootstrap a versek felett; '
           'az ingadozás-becslés egyetlen futáspár (|F3V2B − F3V2|, azonos prompt); „kívül”: |Δ| > ingadozás ÉS az '
           'intervallum nem tartalmazza a 0-t (leíró jelölés, nem próba).', '',
           '| réteg | mérőszám | v2 átlag | F3V3 | Δ | Δ 90% | ingadozás | jelölés |', '|---|---|---|---|---|---|---|---|']
    for r in mc.sorok:
        if r['szakasz'] == 'hatas_osszevetes' and r['reteg'] == 'Összes' or (r['szakasz'] == 'hatas_osszevetes' and r['mero'] in ('pontossag', 'lefedettseg')):
            ref, cl, dl, fl = (float(v) for v in r['szamlalo'].split('|'))
            lo, hi = (float(v) for v in r['nevezo'].split('|'))
            ki.append('| %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] | %.2f pp | %s |' % (
                r['reteg'], r['mero'], 100 * ref, 100 * cl, 100 * dl, 100 * lo, 100 * hi, 100 * fl, r['megjegyzes'].split(';')[0]))
    # (c) a Sonnet-futás
    g = {r['mero']: r for r in mc.sorok if r['szakasz'] == 'gondolkodas' and r['osszeallitas'] == S}
    ko = {r['mero']: r for r in mc.sorok if r['szakasz'] == 'koltseg' and r['osszeallitas'] == S}
    vk = [r for r in mc.sorok if r['szakasz'] == 'vegleges_kapuhiba' and r['osszeallitas'] == S]
    ki += ['', '### (c) A Sonnet-futás (meres_p3c_eredmeny.tsv: koltseg, gondolkodas, vegleges_kapuhiba, jeloles)', '',
           '- Költség: %s USD (%s hívás; %s); bemenet %s, kimenet %s token.' % (
               ko['koltseg_usd']['szamlalo'], ko['hivasok']['szamlalo'], ko['hivasok']['megjegyzes'],
               ko['bemeneti_token']['szamlalo'], ko['kimeneti_token']['szamlalo']),
           '- A gondolkodási keret be nem tartása: %s gondolkodási token a %s kimeneti tokenből; hívásonként a legnagyobb %s '
           '(%s); a keret (reasoning.max_tokens = 1024) fölötti hívás %s a %s-ből (%s). A gondolkodási token a kimeneti '
           'táblaáron %s USD a mért %s USD-ből.' % (
               g['gondolkodasi_token']['szamlalo'], g['gondolkodasi_token']['nevezo'], g['gondolkodasi_token_hivasonkent_max']['szamlalo'],
               g['gondolkodasi_token_hivasonkent_max']['megjegyzes'], g['keret_feletti_hivasok']['szamlalo'], g['keret_feletti_hivasok']['nevezo'],
               g['keret_feletti_hivasok']['megjegyzes'].split('; ')[-1], g['gondolkodasi_token_koltsege_usd']['szamlalo'],
               g['gondolkodasi_token_koltsege_usd']['nevezo']),
           '- Length-lezárás: %s a %s hívásból — %s.' % (g['length_hivasok']['szamlalo'], g['length_hivasok']['nevezo'], g['length_hivasok']['megjegyzes']),
           '- A %d végleges kapuhibás vers (%s): %s.' % (
               len(vk), ', '.join(sorted({'%s, végső kapupont %s' % (r['nevezo'], r['szamlalo']) for r in vk})),
               ', '.join('%s (%s%s)' % (r['mero'], r['reteg'], ', aranyvers' if 'aranyvers' in r['megjegyzes'] else '') for r in vk))]
    ki += ['- %s' % r['megjegyzes'] for r in mc.sorok if r['szakasz'] == 'jeloles' and r['mero'] == 'nem_determinisztikus']
    # (d) beállítás-eltérés
    ki += ['', '### (d) A beállítás-eltérések jelölése', '']
    ki += ['- %s: %s.' % (r['osszeallitas'], r['megjegyzes']) for r in mc.sorok if r['szakasz'] == 'jeloles' and r['mero'] == 'beallitas_elteres']
    ki += ['- A gondolkodási mód futásonként (futásnapló): %s.' % '; '.join(
        '%s: %s' % (r['osszeallitas'], r['szamlalo']) for r in mc.sorok if r['szakasz'] == 'koltseg' and r['mero'] == 'gondolkodas_mod'), '']
    # (e) P5
    F22 = list(kv_.F22_RETEGEK)
    ki += ['### (e) P5: a teljes Biblia költsége összeállításonként (F22 műfaji öt réteg, köteg-bootstrap, 90%)', '',
           'Az A, B, C (F3V2), A+B, A+B+C a P3b-vetítés (koltseg_vetites_p3b.tsv, prompt_v2); a C (F3V3), a Sonnet és a Sonnet + C '
           'a P3c-vetítés (koltseg_vetites_p3c.tsv, prompt_v3; a pár = a két futás vetítésének összege, döntőbíró nélkül). Az '
           'újrakérési szorzó (M) minden futásnál a saját mért adatból.', '',
           '| összeállítás | %s | Összes |' % ' | '.join(F22), '|---|' + '---|' * (len(F22) + 1)]
    for t, o in ((kb, 'A (F1V2)'), (kb, 'B (F2V2)'), (kb, 'C (F3V2)'), (kb, 'A+B'), (kb, 'A+B+C'), (kc, C3_), (kc, S), (kc, PAR)):
        ki.append('| %s | %s |' % (o, ' | '.join(_usd(t, o, r) for r in F22 + ['Összes'])))
    ki += ['', 'Ellenőrzés a 200 versre (a konzervatívabb számít, DT21 g): %s.' % '; '.join(
        '%s %s%%' % (o, kc.get('ellenorzes', o, '-', 'szamito_elteres_szazalek')['ertek']) for o in (S, C3_, PAR)), '']
    # (f) KJV
    h = kj.get('hatas', 'F8V3 − F3V3', 'Összes', 'pontossag')
    hi_ = kj.get('hatas', 'F3V2B − F3V2 (ingadozás)', 'Összes', 'pontossag')
    d = float(h['szamlalo'].split('|')[2])
    lo, up = (float(v) for v in h['nevezo'].split('|'))
    di = float(hi_['szamlalo'].split('|')[2])
    kr4 = mcc.get('kjv', 'C KJV-vel (F8V3, tájékoztató)', 'R4', 'jeloles')
    ek = ej.get('dontes', 'KJV-szabály A) önállóan', 'Összes', 'pontossag (döntés ∩ arany forditatlan / döntés)')
    ki += ['### (f) A KJV-támpont', '',
           '- A mérés (kjv_meres_eredmeny.tsv, F8V3 − F3V3, Összes): a pontosság Δ = %+.2f pp [90%%: %+.2f; %+.2f], az ingadozás-becslés '
           '(F3V2B − F3V2) %+.2f pp: a mérés szerint nincs kimutatható hatás (az ingadozáson belül); a pilot döntése: „nem igazolt, a '
           'javított táblával újramérhető” (PD17 (3)).' % (100 * d, 100 * lo, 100 * up, 100 * di),
           '- Az R4: „%s” (meres_p3c_c_eredmeny.tsv); a Károli ↔ KJV versmegfeleltetés zsoltár-eltolódása: N-F21 (NYITOTT_FELADATOK.md).' % kr4['szamlalo'],
           '- Az előpárosítás KJV-szabálya („nincs KJV-tag → forditatlan-jelölt”; elopar_kjv_eredmeny.tsv, A) önállóan, Összes): pontosság %s.' % pct(ek['szamlalo'], ek['nevezo']), '']
    # (g) a (c) hibák újrabesorolása
    def oszt(f, o):
        return sum(1 for r in bes if r['futas'] == f and r['statusz'] == 'elteres' and r['osztaly'] == o)
    sk = {(r['igehely'], r['irany'], r['k_poz'], r['e_poz']) for r in bes if r['futas'] == 'SONNETV3' and r['osztaly'] == 'c'}
    ck = {(r['igehely'], r['irany'], r['k_poz'], r['e_poz']) for r in bes if r['futas'] == 'F3V3' and r['statusz'] == 'elteres' and r['osztaly'] == 'c'}
    ki += ['### (g) A (c) hibák újrabesorolása (Opus-besorolás, nem mérés; c_diff_p3c_besorolas.tsv, naplok/F21P_C_diff_p3c.md)', '',
           '- C (F3V3), arany v3: a / b / c = %d / %d / %d; Sonnet (50 kapun átment aranyvers): %d / %d / %d; közös (c) eset: %d.' % (
               oszt('F3V3', 'a'), oszt('F3V3', 'b'), oszt('F3V3', 'c'), oszt('SONNETV3', 'a'), oszt('SONNETV3', 'b'), oszt('SONNETV3', 'c'), len(sk & ck)),
           '- A konvenciók hatása (a v2-es C-futások (c) eseteihez képest, DT21 a–e): l. (h).',
           '- Olvasási korlátok: a besorolás az Opus kézi döntése, nem mérés; a Sonnet R3-a nincs benne (kapuhiba); az egyetlen '
           'v2-futásban (c) eset megszűnése a futásközi ingadozással is összefér; a korrigált értékek a küszöb szempontjából nem számítanak.', '']
    # (h) nyitott tételek
    dh = _dt21_hatas(bes)
    jel = [r for r in bes if cdp.JELOLT in r['indok']]
    ki += ['### (h) Nyitott és lezárt tételek', '',
           '- A DT21 a–e a regressziós mérésben lezárva (segített = a v2 (c) eset megszűnt vagy átsorolódott; nem segített = maradt; '
           'ártott = új (c)): %s.' % '; '.join('%s) %d / %d / %d' % (b, *dh[b]) for b in 'abcde'),
           '- „Arany-felülvizsgálatra jelölt” sor: %d (C: %d, Sonnet: %d): %s; a számokban (c), a 6. táblázat zárt (PD10).' % (
               len(jel), sum(1 for r in jel if r['futas'] == 'F3V3'), sum(1 for r in jel if r['futas'] == 'SONNETV3'),
               ', '.join(sorted({r['igehely'] for r in jel}, key=lambda x: x))),
           '- Az (1) feltétel R3-ja nem mérhető (a Sonnet R3-pótlása a próféták előtt; pótló futás most nincs).',
           '- N-F21: a Károli ↔ KJV versmegfeleltetés zsoltár-eltolódása (most nem javítjuk; PD17 (1)).', '']
    # (i) a teljes pilot költsége
    naplo = _tsv('futasnaplo.tsv')
    ki += ['### (i) A teljes pilot költsége (futásnapló, futásonként)', '',
           '| szakasz | futás | hívás | költség USD | megjegyzés |', '|---|---|---|---|---|']
    for szak, fs in (('P3', P3_FUTASOK), ('P3b', P3B_FUTASOK), ('P3c', P3C_FUTASOK)):
        for f in fs:
            rs = [r for r in naplo if r['futas'] == f]
            megj = ''
            if f == 'F8V3':
                bal = [r for r in rs if int(r['koteg']) in (1, 2)]
                megj = 'ebből a véletlen helyi futás két kötege (1., 2.; naplok/F21_baleset_F8V3.md): %d hívás, %.6f USD' % (
                    len(bal), sum(float(r['koltseg_usd']) for r in bal))
            ki.append('| %s | %s | %d | %.6f | %s |' % (szak, f, len(rs), sum(float(r['koltseg_usd']) for r in rs), megj))
        ki.append('| **%s összesen** | | | **%.6f** | |' % (szak, sum(float(r['koltseg_usd']) for r in naplo if r['futas'] in fs)))
    ossz = sum(float(r['koltseg_usd']) for r in naplo)
    ismeretlen = sorted({r['futas'] for r in naplo} - set(P3_FUTASOK + P3B_FUTASOK + P3C_FUTASOK))
    fo = max(float(r['futo_osszeg_usd']) for r in naplo if r.get('futo_osszeg_usd'))
    ki += ['| **a pilot összesen** | | %d | **%.6f** | a napló utolsó futó összege %.6f: %s%s |' % (
        len(naplo), ossz, float(naplo[-1]['futo_osszeg_usd']), 'EGYEZIK' if abs(ossz - float(naplo[-1]['futo_osszeg_usd'])) < 1e-6 else 'ELTÉR',
        ('; ismeretlen futás: %s' % ', '.join(ismeretlen)) if ismeretlen else ''), '',
           'A plafonok és a megállási küszöbök (felhasználói döntések): 3 USD (P3/P3b; 2 USD-s küszöb) → 4,00 USD, küszöb 3,90 '
           '(PD14 (2)) → 5,00 USD, küszöb 4,90 (PD18 (1)). A futó összeg legnagyobb értéke a naplóban %.6f USD: a 4,90-es küszöb '
           'és az 5,00-es plafon alatt%s.' % (fo, '' if fo <= 4.90 else ' — NEM'), '']
    return ki


def javaslat_szakasz():
    """A #22 választott iránya (PD19 (3), DT32): javaslatként rögzítve, ajánlás nélkül, a mért adatokkal."""
    mc = T('meres_p3c_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kc = T('koltseg_vetites_p3c.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    S, C3_, PAR = 'Sonnet (SONNETV3)', 'C (F3V3)', 'Sonnet+C'
    ng, n15 = _genezis_versek()
    pr = int(kc.get('biblia_rs', '-', 'próféta', 'versek_szama')['ertek'])
    v = mc.get('minosites_reszlet', PAR, 'Összes', 'feltetel_5_alacsony_arany_vetitett')
    g = {r['mero']: r for r in mc.sorok if r['szakasz'] == 'gondolkodas' and r['osszeallitas'] == S}
    import math
    ki = ['', '## Javaslat — a #22 választott iránya (a felhasználó döntése, javaslatként rögzítve; a #22 briefje ezzel nem '
          'változik, brief-diff nem készül, teljes futás nem indul)', '',
          'A felhasználó szó szerinti iránya (PD19 (3), DT32):', '',
          '> „Sonnet a Code-ban + C az Actionsben, könyvenként, a Genezissel kezdve; `magas` = egyezés, eltérésnél a Sonnet '
          'változata `alacsony` jelöléssel; a próféták kötegmérete 5 vers; az 1Móz 1–5 után `/usage`-jelentés, és megállás, '
          'ha a teljes Genezisre vetítve a heti keret 50%-a fölött van.”', '',
          'Az irány elemei és a mért adatok, amelyekre a döntés épül (rögzítés, ajánlás nélkül; a számok forrása '
          'f21p/koltseg_vetites_p3c.tsv és f21p/meres_p3c_eredmeny.tsv):', '',
          '- **Futtatási környezet.** A Sonnet a Claude Code-ban fut, az előfizetési (heti) kereten belül; a C (F3V3 beállítás, '
          'prompt_v3) a GitHub Actionsben, OpenRouter-költségen. A mért adatok szerint a Sonnet teljes Bibliára vetített '
          'OpenRouter-költsége %s USD, a C-é %s USD, a páré %s USD (90%%-os intervallum; a (4) küszöb 60 USD): ezért fut a '
          'Sonnet a Code-ban. A Code-ban futó Sonnet a heti keretet terheli; erre a pilotnak nincs mért adata.' % (
              _usd(kc, S, 'Összes'), _usd(kc, C3_, 'Összes'), _usd(kc, PAR, 'Összes')),
          '- **Könyvenként, a Genezissel kezdve.** Az 1Móz %d vers, ebből az 1Móz 1–5 %d vers (Károli-kivonat).' % (ng, n15),
          '- **`magas` = egyezés.** Ez a pár mérésének logikája (A∩B, döntőbíró nélkül): a két modell egyező linkje `magas`. A '
          'mért `magas`-pontosság rétegenként: %s; az R3 nem mérhető (0/0).' % ', '.join(
              '%s %s' % (r, _ar(mc, 'feltetelek', PAR, r, 'magas_pontossag')) for r in ('R1', 'R2', 'R3', 'R4')),
          '- **Eltérésnél a Sonnet változata `alacsony` jelöléssel** kerül be (nem a C-é). A pár mérésében az `alacsony` arány '
          '%s (200 vers, mért), %.1f%% (a teljes Bibliára vetítve), az R3-ban %s; ez a mérés a két modell nem egyező linkjeit '
          'együtt (és a kapuhibás oldal mellett a túlélő oldal linkjeit) számolja, ezért a csak Sonnet-változatot tartalmazó '
          'kimenet `alacsony` aránya ettől eltérhet (nem mért).' % (
              _ar(mc, 'feltetelek', PAR, 'Összes', 'alacsony_arany [200 vers]'), 100 * float(v['szamlalo']),
              _ar(mc, 'feltetelek', PAR, 'R3', 'alacsony_arany [200 vers]')),
          '- **A próféták kötegmérete 5 vers.** Ok: a Sonnet R3-kötege (15.) mindkét próbán length-lezárással végződött (%s), és '
          'a köteg tíz R3-aranyverse végleg kapuhibás; a pótlás a próféták előtt (kis köteg a hosszú gondolkodás miatt). A próféta '
          'réteg (F22) %d vers: 10 verses kötegben %d, 5 versesben %d köteg.' % (
              g['length_hivasok']['megjegyzes'], pr, math.ceil(pr / 10), math.ceil(pr / 5)),
          '- **A `/usage`-jelentés és az 50%%-os megállási feltétel.** A heti keret felhasználását a Claude Code `/usage` '
          'parancsa mutatja; a leolvasást a felhasználó végzi (vagy a `/usage` kimenetét adja át), az 1Móz 1–5 előtt és után. '
          'A mérték: a teljes Genezisre vetített felhasználás = (az 1Móz 1–5 alatt felhasznált heti keret) × (az 1Móz versszáma / '
          'az 1Móz 1–5 versszáma) = × %d/%d (≈ × %.2f); megállás, ha ez a heti keret 50%%-a fölött van. A Sonnet tokenigényéről '
          'a pilot mért adata (OpenRouter, 200 vers): %s gondolkodási token a %s kimeneti tokenből; hívásonként legfeljebb %s.' % (
              ng, n15, ng / n15, g['gondolkodasi_token']['szamlalo'], g['gondolkodasi_token']['nevezo'],
              g['gondolkodasi_token_hivasonkent_max']['szamlalo']),
          '- **Kapcsolódó állapotok.** A #22 fejléce `dontesre_var` (a briefje nem változik). Az F31-brief (F31_F21R_BRIEF.md, '
          '`nem_indult`) a regressziós mérést írja le, amely ezen az ágon, a pilot PD13–PD19 döntései szerint lefutott: az '
          'átfedés kezelése a felhasználó döntése.', '']
    return ki


def regi_szamok_osszevet(regi_ut, uj_ut):
    """A régi jelentés minden számának (a ts-sor kivételével) megvan-e legalább annyi előfordulása az újban.
    Visszaad: (régi számok darabja, hiányzó számok {szám: hiány})."""
    import re
    from collections import Counter

    def szamok(ut):
        with open(ut, encoding='utf-8') as f:
            sorok = [s for s in f if 'ts=' not in s]
        return Counter(re.findall(r'\d+(?:[.,]\d+)*', ''.join(sorok)))
    a, b = szamok(regi_ut), szamok(uj_ut)
    return sum(a.values()), {k: v - b[k] for k, v in a.items() if b[k] < v}


def main():
    m1 = T('meres_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    m2 = T('meres_v2_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kv = T('koltseg_vetites.tsv', ['szakasz', 'futas', 'reteg', 'mero'])
    ing = T('ingadozas.tsv', ['szakasz', 'reteg', 'mero'])
    mp_ = T('meres_p3b_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])

    def p1(sz, oss, ret, mero):
        r = m1.get(sz, oss, ret, mero)
        return pct(r['szamlalo'], r['nevezo'])

    def p2(sz, oss, ret, mero):
        r = m2.get(sz, oss, ret, mero)
        return pct(r['szamlalo'], r['nevezo'])

    naplo = _naplo_p3_p3b()
    pilot_cost = sum(float(r['koltseg_usd']) for r in naplo)
    futasonkent = {}
    for r in naplo:
        futasonkent[r['futas']] = futasonkent.get(r['futas'], 0.0) + float(r['koltseg_usd'])
    besor = _tsv('c_diff_besorolas.tsv')
    osz = _tsv('c_diff_f3v2_osszevetes.tsv')
    f3_c = sum(1 for r in osz if r['statusz'] in ('maradt', 'megszunt', 'nem_merheto'))
    f3v2_c = sum(1 for r in osz if r['statusz'] in ('maradt', 'uj', 'oroklott') and r['f3v2_osztaly'] == 'c')
    v1_c = sum(1 for r in besor if r['osztaly'] == 'c')
    eltero = len(_tsv('sorrend_eltero_versek.tsv')) if os.path.exists(os.path.join(F21P, 'sorrend_eltero_versek.tsv')) else None
    osszetett = sum(1 for _, _, s in tokenek.regi_arany() if '+' in s)
    minta = _tsv('minta.tsv')
    ered = tokenek.betolt_eredeti()
    nem_tr = sum(1 for m in minta for w in ered[m['igehely']] if w['nem_tr'])

    ki = ['# F21P_jelentes.md — Károli–Strong mérőpilot: záró jelentés (P6)', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/jelentes_f21p.py | scope=F21 mérőpilot, P6 záró jelentés (A, B, C, '
          'A+B, A+B+C; R1–R4) | forras=f21p/meres_eredmeny.tsv, '
          'f21p/meres_v2_eredmeny.tsv, f21p/koltseg_vetites.tsv, f21p/ingadozas.tsv, f21p/c_diff_besorolas.tsv, '
          'f21p/c_diff_f3v2_osszevetes.tsv, f21p/futasnaplo.tsv, f21p/minta.tsv, f21p/sorrend_eltero_versek.tsv, '
          'konkordancia/Karoli_Strong_kivonat.tsv, f21p/meres_p3b_eredmeny.tsv, f21p/koltseg_vetites_p3b.tsv, '
          'f21p/c_diff_f3v2b_besorolas.tsv, %s | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
          'kézzel szerkeszteni tilos -->' % (P3C_FORRAS, tokenek.generalas_ts()), '',
          'A számok kizárólag szkriptkimenetből jönnek (a forrás soronként jelölve). A **korrigált** értékek '
          'kizárólag „**Opus-besorolás, nem mérés**” jelöléssel szerepelnek; a küszöb szempontjából csak a mért '
          'érték számít (PD10). A jelentés nem ajánl döntést a #22-ről.', '']
    ki += p3c_szakasz()
    ki.append('*A lenti szakaszok a P3b- és a P3-adatot őrzik változatlanul (prompt_v2 / v1, arany v2 / v1).*')
    ki.append('')
    ki += p3b_szakasz()
    c_regi0 = m2.get('regi_arany', 'F3V2', 'Összes', 'egyezes')
    c_regik = m2.get('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva_tajekoztato')
    c3_regi0 = m1.get('regi_arany', 'C', 'Összes', 'egyezes')
    REGI_JEL = ('tájékoztató, nem minősít — a küszöb szempontjából a mért, kizárás nélküli érték számít (DT21 i); '
                'a hibásnak jelölt hármas csak az 1Móz 6:17, az 1Móz 13:4 korábbi hibás-jelölése a felhasználó döntése '
                'szerint visszavonva')
    ki += ['## Összefoglaló — P3 (korábbi, a P3b előtt: v1-A/B, F3/F3V2)', '',
           '- **Egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8, az F4 nem futott).**',
           '- Az A+B két mért feltételen bukott: az A∩B (`magas`) pontosság R1-ben, R3-ban és R4-ben a 98%% alatt van, '
           'a régi arany egyezése %s (a 95%% alatt).' % p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes'),
           '- A C egymodelles összeállítás, a PD6 szerint nem minősíthető. A C régi arany egyezése: **mért (kizárás '
           'nélkül) %s — a 95%% alatt**; az 1Móz 6:17 kizárásával %s (%s).' % (
               pct(c_regi0['szamlalo'], c_regi0['nevezo']), pct(c_regik['szamlalo'], c_regik['nevezo']), REGI_JEL), '']

    # (a) EREDMÉNY
    ki += ['## (a) Eredmény — P3 (korábbi, a P3b előtt)', '',
           '**Egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8, az F4 nem futott).** A rögzített öt feltétel '
           '(`magas` pontosság ≥ 98% minden rétegben; lefedettség ≥ 95%; régi arany ≥ 95%; vetített költség 90%-os '
           'felső széle ≤ 60 USD; vetített `alacsony` arány ≤ 10%) összeállításonként:', '',
           '| összeállítás | magas pontosság ≥ 98% | lefedettség ≥ 95% | régi arany ≥ 95% | költség ≤ 60 USD | alacsony ≤ 10% | minősítés |',
           '|---|---|---|---|---|---|---|']
    c_lef = p2('pontossag_lefedettseg', 'F3V2 × arany v2', 'Összes', 'lefedettseg')
    c_lef_v1 = p1('pontossag_lefedettseg', 'C', 'Összes', 'lefedettseg')
    c_regi = p2('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva_tajekoztato')
    c_ko = kv.get('vetites', 'F3V2', 'Összes', 'koltseg_usd')
    ki.append('| A | n.é. (egymodelles, PD6) | mért: %s — nem minősíthető | mért: %s | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |'
              % (p1('pontossag_lefedettseg', 'A', 'Összes', 'lefedettseg'), p1('regi_arany', 'A', 'Összes', 'egyezes')))
    ki.append('| B | n.é. (egymodelles, PD6) | mért: %s — nem minősíthető | mért: %s | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |'
              % (p1('pontossag_lefedettseg', 'B', 'Összes', 'lefedettseg'), p1('regi_arany', 'B', 'Összes', 'egyezes')))
    ki.append('| C | n.é. (egymodelles, PD6) | mért: F3 %s (arany v1), F3V2 %s (arany v2) — nem minősíthető | mért (kizárás nélkül): F3 %s, F3V2 %s — a 95%% alatt; az 1Móz 6:17 kizárásával F3V2 %s (%s) | vetítve (F22 műfaji 5 réteg): F3 %s USD [%s–%s], F3V2 %s USD [%s–%s] (90%%) | n.é. (PD6) | nem minősíthető (PD6) |'
              % (c_lef_v1, c_lef, pct(c3_regi0['szamlalo'], c3_regi0['nevezo']), pct(c_regi0['szamlalo'], c_regi0['nevezo']),
                 c_regi, REGI_JEL, kv.get('vetites', 'F3', 'Összes', 'koltseg_usd')['ertek'],
                 kv.get('vetites', 'F3', 'Összes', 'koltseg_usd')['also90'], kv.get('vetites', 'F3', 'Összes', 'koltseg_usd')['felso90'],
                 c_ko['ertek'], c_ko['also90'], c_ko['felso90']))
    ki.append('| A+B | **bukott**: A∩B pontosság R1 %s, R2 %s, R3 %s, R4 %s | nem mért (F4 nélkül nincs végső linkhalmaz; A∩B lefedettség tájékoztatásul: %s) | **bukott** (A∩B): %s; a korábbi, összetett Strong nélküli definícióval is %s | nem vetítve (PD8) | nem mért (F4 nélkül; PD8) | nem felel meg |'
              % tuple([p1('pontossag_lefedettseg', 'A+B magas (A∩B)', r, 'pontossag') for r in ('R1', 'R2', 'R3', 'R4')]
                      + [p1('pontossag_lefedettseg', 'A+B magas (A∩B)', 'Összes', 'lefedettseg'),
                         p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes'),
                         p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes_korabbi_osszetett_strong_nelkul')]))
    ki.append('| A+B+C | nem mért (az F4 nem futott, PD8) | nem mért | nem mért | nem vetítve | nem mért | nem mért (PD8) |')
    ki.append('')

    # (b) MI BUKOTT EL — csak a rögzített öt feltétel
    ki += ['## (b) Mi bukott el — P3 (korábbi; csak a rögzített öt feltétel)', '',
           '- **A+B, `magas` pontosság ≥ 98%% minden rétegben — bukott:** az A∩B linkek pontossága R1 %s, R2 %s, R3 %s, R4 %s '
           '(forrás: meres_eredmeny.tsv, pontossag_lefedettseg).' % tuple(
               p1('pontossag_lefedettseg', 'A+B magas (A∩B)', r, 'pontossag') for r in ('R1', 'R2', 'R3', 'R4')),
           '- **A+B, régi arany ≥ 95%% — bukott:** az A∩B egyezése a halmaz-definícióval %s, a korábbi (összetett Strong '
           'nélküli) definícióval %s (meres_eredmeny.tsv, regi_arany).' % (
               p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes'),
               p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes_korabbi_osszetett_strong_nelkul')),
           '- **A+B, lefedettség, költség, `alacsony` arány:** nem mért (F4 nélkül nincs végső linkhalmaz és bizonyossági '
           'szint; PD8).',
           '- **A, B, C (egymodelles):** a PD6 szerint nem minősíthető; a `magas`/`alacsony` szint egy modellnél nem '
           'értelmezhető. A C mért összpontossága a rétegenkénti 98%%-hoz mérten az arany v2-n F3: %s; F3V2: %s. '
           'A korrigált (Opus-besorolás, nem mérés) érték nem számít.' % (
               ', '.join('%s %s' % (r, p2('pontossag_lefedettseg', 'F3 × arany v2', r, 'pontossag')) for r in ('R1', 'R2', 'R3', 'R4')),
               ', '.join('%s %s' % (r, p2('pontossag_lefedettseg', 'F3V2 × arany v2', r, 'pontossag')) for r in ('R1', 'R2', 'R3', 'R4'))),
           '- **A+B+C:** nem mért (PD8, az F4 nem futott).', '',
           '**Megfigyelés (nem feltétel):** a kapuhiba nem tartozik a rögzített öt feltétel közé. Végleges kapuhiba '
           'A %s, B %s; első próbára A %s, B %s. A döntőbíróhoz menne (eltérő, csak egyik átment, egyik sem): %s '
           '(meres_eredmeny.tsv, kapuhiba és ab_osszeallitas). Emiatt az A+B összeállításban a döntőbíró (F4) nélkül '
           'az `alacsony`-arány feltétel nem mért.' % (
               p1('kapuhiba', 'F1 (A)', 'Összes', 'kapuhiba_vegleg'), p1('kapuhiba', 'F2 (B)', 'Összes', 'kapuhiba_vegleg'),
               p1('kapuhiba', 'F1 (A)', 'Összes', 'kapuhiba_elso_probara'), p1('kapuhiba', 'F2 (B)', 'Összes', 'kapuhiba_elso_probara'),
               p1('ab_osszeallitas', 'A+B', 'Összes', 'dontobirohoz_menne (eltero + csak egyik + egyik sem)')), '']

    # (b2) P-K4: minden mérőszám összeállításonként és rétegenként (meres_eredmeny.tsv)
    ki += ['## (b2) Mérőszámok összeállításonként és rétegenként — P3 (P-K4; forrás: meres_eredmeny.tsv, arany v1)', '',
           'Bizonyossági szintek (G4): a `magas` az A∩B (az A+B egyező linkjei); a `kozepes` és az `alacsony` a döntőbíró '
           '(F4) döntésén alapul, F4 nélkül nem mért (PD8); egymodelles összeállításra egyik szint sem értelmezett (PD6).', '',
           '| összeállítás | mérőszám | R1 | R2 | R3 | R4 | Összes |', '|---|---|---|---|---|---|---|']
    for oss_ in ('A', 'B', 'C', 'A+B magas (A∩B)', 'A∪B (döntőbíró előtti felső korlát)'):
        for mero in ('arany_versek_kapun_atment', 'pontossag', 'lefedettseg'):
            ki.append('| %s | %s | %s |' % (oss_, mero, ' | '.join(p1('pontossag_lefedettseg', oss_, r, mero) for r in RETEGEK)))
    for mero in ('versek_mindketto_atment', 'link_egyezes (uniós arány)', 'azonos_linkhalmazu_versek'):
        ki.append('| A–B | %s | %s |' % (mero, ' | '.join(p1('ab_egyezes', 'A–B', r, mero) for r in RETEGEK)))
    for oss_ in ('A', 'B', 'C', 'A+B magas (A∩B)'):
        for mero in ('egyezes', 'egyezes_hibas_kizarva_tajekoztato'):
            ki.append('| %s | régi arany: %s | %s |' % (oss_, mero, ' | '.join(p1('regi_arany', oss_, r, mero) for r in RETEGEK)))
    for oss_ in ('F1 (A)', 'F2 (B)', 'F3 (C)', 'F5 (A (KJV nélkül))', 'F6 (B (KJV nélkül))'):
        for mero in ('kapuhiba_elso_probara', 'kapuhiba_vegleg'):
            cellak = []
            for r in RETEGEK:
                try:
                    cellak.append(p1('kapuhiba', oss_, r, mero))
                except KeyError:
                    cellak.append('—')
            ki.append('| %s | %s | %s |' % (oss_, mero, ' | '.join(cellak)))
    for mero in ('mindketto_atment_azonos_linkekkel', 'mindketto_atment_eltero_linkekkel', 'csak_A_atment', 'csak_B_atment',
                 'egyik_sem_atment', 'dontobirohoz_menne (eltero + csak egyik + egyik sem)', 'nem_egyezo_link_arany (1 − A∩B/A∪B)'):
        ki.append('| A+B | %s | %s |' % (mero, ' | '.join(p1('ab_osszeallitas', 'A+B', r, mero) for r in RETEGEK)))
    ki.append('| A+B | alacsony_arany | n.é. | n.é. | n.é. | n.é. | n.é. |')
    ki.append('')

    # (c) mért számok
    oss = ['F3 × arany v1', 'F3 × arany v2', 'F3V2 × arany v2']
    ki += ['## (c) A mért számok — P3 (C: F3/F3V2; v1-A/B)', '', '### Pontosság és lefedettség (C; forrás: meres_v2_eredmeny.tsv)', '',
           '| réteg | mérőszám | ' + ' | '.join(oss) + ' |', '|---|---|---|---|---|']
    for r in RETEGEK:
        for mero in ('pontossag', 'lefedettseg'):
            ki.append('| %s | %s | %s |' % (r, mero, ' | '.join(p2('pontossag_lefedettseg', o, r, mero) for o in oss)))
    ki += ['', 'Az A és a B (arany v1, kapun átment versek; meres_eredmeny.tsv): A pontosság %s, lefedettség %s; '
           'B pontosság %s, lefedettség %s.' % (
               p1('pontossag_lefedettseg', 'A', 'Összes', 'pontossag'), p1('pontossag_lefedettseg', 'A', 'Összes', 'lefedettseg'),
               p1('pontossag_lefedettseg', 'B', 'Összes', 'pontossag'), p1('pontossag_lefedettseg', 'B', 'Összes', 'lefedettseg')), '',
           '### Régi arany egyezés (halmaz-definíció; mért = kizárás nélkül, DT21 i)', '',
           '| összeállítás | kizárás nélkül (MÉRT) | az 1Móz 6:17 nélkül (TÁJÉKOZTATÓ) |', '|---|---|---|']
    for o in ('A', 'B', 'C', 'A+B magas (A∩B)'):
        ki.append('| %s (arany-független, 200 verses minta) | %s | %s |' % (
            o, p1('regi_arany', o, 'Összes', 'egyezes'), p1('regi_arany', o, 'Összes', 'egyezes_hibas_kizarva_tajekoztato')))
    ki.append('| C — F3V2 | %s | %s |' % (p2('regi_arany', 'F3V2', 'Összes', 'egyezes'), p2('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva_tajekoztato')))
    ki += ['', '### Kapuhiba-arány (első próbára / végleg)', '', '| futás | első próbára | végleg |', '|---|---|---|']
    for oss_, nev in (('F1 (A)', 'A'), ('F2 (B)', 'B'), ('F3 (C)', 'C (F3)')):
        ki.append('| %s | %s | %s |' % (nev, p1('kapuhiba', oss_, 'Összes', 'kapuhiba_elso_probara'), p1('kapuhiba', oss_, 'Összes', 'kapuhiba_vegleg')))
    ki.append('| C (F3V2) | %s | %s |' % (p2('kapuhiba', 'F3V2', 'Összes', 'elso_probara'), p2('kapuhiba', 'F3V2', 'Összes', 'vegleg')))
    ki += ['', '### Költség (futásnapló)', '', '| futás | cost USD |', '|---|---|']
    for f in sorted(futasonkent):
        ki.append('| %s | %.6f |' % (f, futasonkent[f]))
    p3b_futasok = ('F1V2', 'F2V2', 'F5V2', 'F6V2', 'F3V2B', 'F4V2')
    ki.append('| P3 összesen (a P3b előtt: F1–F3, F5, F6, F3V2) | %.6f |' % sum(v for f, v in futasonkent.items() if f not in p3b_futasok))
    ki.append('| **a pilot összesen (P3 + P3b)** | **%.6f** (plafon: 3 USD) |' % pilot_cost)
    ki.append('')
    ki.append('A C gondolkodási tokenje a futásnaplóban 0 (F3 és F3V2), és az F3V2 nyers usage-ában is 0 '
              '(koltseg_vetites.tsv, illesztes/gondolkodasi_token).')
    d1 = m1.get('kjv_hatas', 'KJV-val − KJV nélkül', 'R1', 'delta_magas_pontossag_szazalekpont [közös halmaz]')
    d2 = m1.get('kjv_hatas', 'KJV-val vs KJV nélkül', 'R1', 'A–B_eltérés_relativ_csokkenes [közös halmaz (mind a négy átment)]')
    nk = m1.get('kjv_hatas', 'KJV-val (F1/F2)', 'R1', 'magas (A∩B) arany_versek [közös halmaz]')
    ki += ['', '### KJV-támpont (N29)', '',
           'A v1-adaton nem teljesül, n=%s, nem végleges. A közös halmazon (mind a négy futás átment, %s/%s R1-aranyvers): '
           'a `magas` pontosság különbsége (KJV-val − KJV nélkül) %s százalékpont (küszöb: ≥ +1); az A–B eltérés '
           'relatív csökkenése %s%% (küszöb: ≥ 20%%) — meres_eredmeny.tsv, kjv_hatas. Az A és a B kiesett (PD8), '
           'a KJV-hatás a C-re nem mért.' % (nk['szamlalo'], nk['szamlalo'], nk['nevezo'], d1['ertek'], d2['ertek']), '']
    # ingadozás
    ki += ['### Futásközi eltérés (F3 vs F3V2, arany v2; forrás: ingadozas.tsv)', '',
           'A két C-futás promptja is különbözik: az eltérés = prompthatás + futásközi ingadozás, a kettő egy-egy '
           'futásból **nem választható szét**. A bootstrap (a versek felett, rétegzett, 1000) a versminta '
           'bizonytalanságát fedi, a futás megismétlésének szórását nem. A |Δ| a két futás közti eltérés (prompt és '
           'ingadozás együtt) felső becslése, nem az ingadozásé.', '',
           '| réteg | mérőszám | F3 | F3V2 | Δ | Δ 90%-os intervallum | |Δ| felső becslés (95. percentilis) | n |',
           '|---|---|---|---|---|---|---|---|']
    for r in RETEGEK:
        for sz, mero in (('arany_v2', 'pontossag'), ('arany_v2', 'lefedettseg'), ('kapu', 'kapuhiba_elso_probara'), ('kapu', 'kapuhiba_vegleg')):
            x = ing.get(sz, r, mero)
            ki.append('| %s | %s | %.2f%% | %.2f%% | %+.2f pp | [%+.2f; %+.2f] pp | %.2f pp | %s |' % (
                r, mero, 100 * float(x['F3']), 100 * float(x['F3V2']), 100 * float(x['delta']),
                100 * float(x['delta_also90']), 100 * float(x['delta_felso90']), 100 * float(x['abs_delta_felso95']), x['n']))
    a60 = ing.get('linkhalmaz', 'Összes', 'azonos_linkhalmazu_versek [arany (60)]')
    a200 = ing.get('linkhalmaz', 'Összes', 'azonos_linkhalmazu_versek [minta (200)]')
    j200 = ing.get('linkhalmaz', 'Összes', 'link_egyezes Σ|∩|/Σ|∪| [minta (200)]')
    lef = ing.get('arany_v2', 'Összes', 'lefedettseg')
    ki += ['', 'Verszintű linkhalmaz-egyezés: azonos linkhalmazú vers %s/%s az aranyon, %s/%s a mintán (mindkét futás '
           'átment); a linkek egyezése Σ|∩|/Σ|∪| = %.1f%% (%s) a mintán.' % (
               a60['delta'], a60['n'], a200['delta'], a200['n'], 100 * float(j200['delta']), j200['megjegyzes']),
           'A lefedettség %.2f%% → %.2f%% különbsége (+%.2f pp) 90%%-os intervalluma [%+.2f; %+.2f] pp: a versminta '
           'bizonytalansága ezt a különbséget nem magyarázza (az intervallum nem tartalmazza a 0-t); hogy mekkora része '
           'prompthatás és mekkora futásközi ingadozás, egy-egy futásból nem mondható meg.' % (
               100 * float(lef['F3']), 100 * float(lef['F3V2']), 100 * float(lef['delta']),
               100 * float(lef['delta_also90']), 100 * float(lef['delta_felso90'])), '']

    # (d) P5
    ki += ['## (d) Költségvetítés — P3 (P5, csak a C; forrás: koltseg_vetites.tsv; a P3b-vetítés a fenti P3b-szakaszban)', '',
           '**Eltérés a brieftől:** a bootstrap egysége a 10 verses köteg, nem a vers (a brief P5.6 a verseken kéri; a token '
           'hívásonként, 10 versre ismert, versenként nem mérhető). DT21 f): **elfogadva (felhasználói döntés)**.', '',
           'Módszer: illesztés tokenfajtánként az első próbálkozású hívásokon (bemenet = a + b·x + c·k; kimenet = a + b·x; '
           'x = eredeti + Károli-szavak, k = KJV-támpont szavai); a teljes Biblia valódi vershosszai (Karoli_1908, '
           'TAHOT/TAGNT); ár a cost mezőből; az újrakérés a pilot mért szorzójával; bootstrap a kötegek felett (1000); '
           'ellenőrzés a 200 versen.', '',
           'Rétegbesorolás (DT21 h): az F22 brief 22.2 műfaji (nem kánon szerinti) öt rétege; a korábbi pilot-4-réteges '
           'besorolás tájékoztatóként alább.', '',
           '| réteg (F22) | könyvek | versek |', '|---|---|---|']
    for r in kv_.F22_RETEGEK:
        ki.append('| %s | %s | %s |' % (r, kv.get('reteg_besorolas', '-', r, 'konyvek')['ertek'], kv.get('biblia', '-', r, 'versek')['ertek']))
    ki += ['', '| réteg (pilot-4, tájékoztató) | könyvek | versek |', '|---|---|---|']
    for r in ('R1', 'R2', 'R3', 'R4'):
        ki.append('| %s | %s | %s |' % (r, kv.get('reteg_besorolas_pilot4_tajekoztato', '-', r, 'konyvek')['ertek'],
                                        kv.get('biblia_pilot4_tajekoztato', '-', r, 'versek')['ertek']))
    ki += ['', '| futás | illesztés (bemenet a/b/c; kimenet a/b) | cost/táblaár (1. próba) | újrakérés-szorzó M | 200 vers: vetített / tényleges (eltérés) | leave-one-out eltérés | **számító (DT21 g)** |',
           '|---|---|---|---|---|---|---|']
    for f in ('F3', 'F3V2'):
        sz = kv.get('ellenorzes', f, '-', 'szamito_elteres_szazalek')
        ki.append('| %s | %s ; %s | %s | %s | %s / %s USD (%s%%) | %s%% | %s%% (%s) |' % (
            f, kv.get('illesztes', f, '-', 'bemenet_a_b_c')['ertek'], kv.get('illesztes', f, '-', 'kimenet_a_b')['ertek'],
            kv.get('ar', f, '-', 'cost1_per_tablaar')['ertek'], kv.get('ar', f, '-', 'ujrakeres_szorzo_M')['ertek'],
            kv.get('ellenorzes', f, '-', 'pilot_200_vetitett_usd')['ertek'], kv.get('ellenorzes', f, '-', 'pilot_200_tenyleges_usd')['ertek'],
            kv.get('ellenorzes', f, '-', 'elteres_szazalek')['ertek'], kv.get('ellenorzes', f, '-', 'loo_elteres_szazalek')['ertek'],
            sz['ertek'], sz['megjegyzes'].split('számít: ')[-1]))
    ki += ['', 'Az újrakérések cost-ja nem lineáris a tokenben (a megismételt előtag gyorsítótárazott), ezért az '
           'újrakérést nem tokenből, hanem a mért M szorzóval vetítjük.', '',
           '| réteg (F22) | F3 (prompt v1) USD [90%] | F3V2 (prompt v2) USD [90%] |', '|---|---|---|']
    for r in list(kv_.F22_RETEGEK) + ['Összes']:
        a, b = kv.get('vetites', 'F3', r, 'koltseg_usd'), kv.get('vetites', 'F3V2', r, 'koltseg_usd')
        ki.append('| %s | %s [%s–%s] | %s [%s–%s] |' % (r, a['ertek'], a['also90'], a['felso90'], b['ertek'], b['also90'], b['felso90']))
    ki += ['', '| réteg (pilot-4, tájékoztató) | F3 USD [90%] | F3V2 USD [90%] |', '|---|---|---|']
    for r in RETEGEK:
        a, b = kv.get('vetites_pilot4_tajekoztato', 'F3', r, 'koltseg_usd'), kv.get('vetites_pilot4_tajekoztato', 'F3V2', r, 'koltseg_usd')
        ki.append('| %s | %s [%s–%s] | %s [%s–%s] |' % (r, a['ertek'], a['also90'], a['felso90'], b['ertek'], b['also90'], b['felso90']))
    ki += ['', 'A két besorolás különbsége (tájékoztató, F22 − pilot-4): F3 %s USD (%s%%), F3V2 %s USD (%s%%).' % (
        kv.get('besorolas_kulonbseg_tajekoztato', 'F3', 'Összes', 'f22_minus_pilot4_usd')['ertek'],
        kv.get('besorolas_kulonbseg_tajekoztato', 'F3', 'Összes', 'f22_minus_pilot4_szazalek')['ertek'],
        kv.get('besorolas_kulonbseg_tajekoztato', 'F3V2', 'Összes', 'f22_minus_pilot4_usd')['ertek'],
        kv.get('besorolas_kulonbseg_tajekoztato', 'F3V2', 'Összes', 'f22_minus_pilot4_szazalek')['ertek'])]
    ki += ['', '**Kézimunka-vetítés (C):** az aranyon mért eltérés/vers és a (c)-hiba/vers (ez utóbbi Opus-besorolás, nem mérés), '
           'F22-rétegenként a teljes Bibliára (a minta aranyversei könyv szerint leképezve); a rétegenkénti arany kis '
           'mintájú (10–20 vers). `alacsony` arány: n.é. (PD6).', '',
           '| futás | eltérés/vers (mért, 60 aranyvers) | vetített eltérés a Bibliára (F22) | (c)/vers (Opus-besorolás, nem mérés) | vetített (c) a Bibliára (F22; Opus-besorolás, nem mérés) | tájékoztató, pilot-4: eltérés / (c) |',
           '|---|---|---|---|---|---|']
    for f in ('F3', 'F3V2'):
        ki.append('| %s | %s | %s | %s | %s | %s / %s |' % (
            f, kv.get('kezimunka', f, 'Összes', 'elteres_per_vers_arany_v2')['ertek'], kv.get('kezimunka', f, 'Összes', 'vetitett_elteres_biblia')['ertek'],
            kv.get('kezimunka', f, 'Összes', 'c_hiba_per_vers')['ertek'], kv.get('kezimunka', f, 'Összes', 'vetitett_c_hiba_biblia')['ertek'],
            kv.get('kezimunka_pilot4_tajekoztato', f, 'Összes', 'vetitett_elteres_biblia')['ertek'],
            kv.get('kezimunka_pilot4_tajekoztato', f, 'Összes', 'vetitett_c_hiba_biblia')['ertek']))
    ki.append('')

    # (e) nyitott tételek, eszközök, korlátok
    ki += ['## (e) A DT21 tételei, átvihető eszközök, megtanult korlátok', '',
           '**A #22:** a döntés elhalasztva a regressziós futás utánra; brief-diff nem készül, teljes futás nem indul; '
           'marad `dontesre_var`.', '',
           '### Az a–e tétel: regressziós mérésre átvéve (DT21 döntés: a–e a jegyzet v2-be, prompt_v3, F3V3)', '',
           '1. **G / K7:** a prompt_v2 G-szabályának kivétele („többtagú igei szerkezet minden tagja”) tágabb, mint a jegyzet '
           'K7-e (*tudja vala*, *megy vala*): melyik az irányadó.',
           '2. **C:** a prompt „azt, őt …” felsorolása a C-nél az *\'et* nélküli, betoldott tárgyi névmásokra is általánosult.',
           '3. **„azt … hogy” / „azért … hogy”:** az arany az előbbit betoldásnak veszi, az utóbbit (Mt 21:4) köti.',
           '4. **2Móz 26:13 *is*:** a K9 szerint a *ve-* az *is*-hez köthető volna; az arany v2 forditatlan-nak veszi (az F3V2-nél (b)).',
           '5. **D:** a birtokláncban (*szolgálójának szemét*) nem egyértelmű, melyik szó viseli a ragot.', '',
           '### Lezárt tételek (f–k; felhasználói döntés, DT21)', '',
           '- **f)** a P5 bootstrap-egysége a köteg: elfogadva (felhasználói döntés).',
           '- **g)** költség-ellenőrzés: a mintán belüli és a leave-one-out közül a konzervatívabb (nagyobb abszolút '
           'eltérésű) számít; ez minden futásnál a leave-one-out (P5-táblák, „számító” oszlop).',
           '- **h)** a teljes Biblia rétegbesorolása: az F22 brief 22.2 műfaji öt rétege (Préd, Sir → költészet, Dán → '
           'próféta, Ruth, Eszt → ÓSZ-próza a felhasználó döntése szerint); a korábbi pilot-4-réteges besorolás '
           'tájékoztató; a pilot mérési rétegei (R1–R4) változatlanok. Nyitott marad: az ApCsel és a Jel nincs a mintában.',
           '- **i)** régi arany: a mért érték a kizárás nélküli (C, F3V2: %s — a 95%% alatt); a kizárásos érték csak '
           'tájékoztató (az 1Móz 6:17 nélkül: %s); az 1Móz 13:4 hibás-jelölése visszavonva.' % (
               pct(c_regi0['szamlalo'], c_regi0['nevezo']), pct(c_regik['szamlalo'], c_regik['nevezo'])),
           '- **j)** a gondolkodási mód eltérése a pilot idején elfogadva.',
           '- **k)** az A+B+C-nél a szó szerinti olvasat számít (%s), az A+B definíciója elfogadva.' % (
               pct(*[mp_.get('feltetelek', 'A+B+C', 'Összes', 'alacsony_arany [200 vers]')[k] for k in ('szamlalo', 'nevezo')])), '',
           '### Az F22-re átvihető eszközök', '',
           '- prompt: f21p/prompt_v1.md, f21p/prompt_v2.md (a tíz konvenció szabályként);',
           '- kapu: eszkozok/karoli_strong/kapu.py (ötpontos, újrakéréssel);',
           '- arany v2: f21p/arany_opus_v2.jsonl (befagyasztva, sha256: f21p/arany_opus_v2.sha256), a jegyzettel;',
           '- eszkozok/karoli_strong/tokenek.py (tokenizálás, TR-jelölés, kizárás), futtat.py (futtató, plafon, --szaraz, '
           '--onteszt), meres.py és meres_v2.py (mérés), c_diff.py és c_diff_f3v2.py (diff és besorolás-váz), '
           'koltseg_vetit.py, ingadozas.py.', '',
           '### Megtanult korlátok', '',
           '- TAHOT-sorrend: %s vers kivonatbeli sorrendje nem a szórend (f21p/sorrend_eltero_versek.tsv), ezek a mintából kimaradtak.' % (eltero if eltero is not None else 'n.é.'),
           '- X / Q(K) változatsorok: a Ketiv / Qere és az üres helyőrzők a kivonatban nem mind látszanak (l. f21p/arany_opus_jegyzetek.md 3. szakasz).',
           '- `[nem TR]`: a „TR»N / TR«N” jelölés javítva (PD7); a 200 verses mintában most %d `[nem TR]` token, az „eltérő alak” tokenek kizárva.' % nem_tr,
           '- Összetett Strong a régi aranyban: %d hármas „+”-os Stronggal; halmaz-definícióval mérve (PD9).' % osszetett,
           '- Az A és a B JSON-hibái: első próbára érvénytelen JSON A %s, B %s (meres_eredmeny.tsv, kapuhiba_tipus).' % (
               p1('kapuhiba_tipus', 'F1 (A)', 'Összes', 'kapupont_1-json_elso_probara'),
               p1('kapuhiba_tipus', 'F2 (B)', 'Összes', 'kapupont_1-json_elso_probara')),
           '- A C gondolkodási tokenje a naplóban és a nyers usage-ban 0 (minimal effort); a nyers usage tárolása az F3V2-től.',
           '- Gondolkodási mód (eltérés a brief Keretek pontjától, amely mindhárom modellnél azonos beállítást kért; DT21 j: '
           'a pilot idején elfogadva): az A '
           'és a B kikapcsolva, a C-nél a gondolkodás kötelező, `minimal` szinten. Az F1–F6 napló `gondolkodas_token` = 0 '
           'értéke nem mérés (a token olvasása csak az F21.10-től él); a nyers usage az F3V2-től tárolt, abban is 0. '
           'A költség ettől helyes, mert a `cost` mezőből jön.',
           '- A prompt-szabályok túlkötést okozhatnak: az F3V2 több linket ad (%s link az F3 %s-ével szemben, arany v2).' % (
               m2.get('pontossag_lefedettseg', 'F3V2 × arany v2', 'Összes', 'pontossag')['nevezo'],
               m2.get('pontossag_lefedettseg', 'F3 × arany v2', 'Összes', 'pontossag')['nevezo']), '',
           '### A #22 opcióinak következményei (tények, ajánlás nélkül)', '',
           '- **Marad (a jelenlegi céllal):** a P3b-adaton az A+B és az A+B+C mért, és a Döntési szabály szerint egyik '
           'sem felel meg (a bukott feltételek a P3b-szakaszban); az A, a B és a C egymodelles, a PD6 szerint nem '
           'minősíthető. A teljes futás a jelenlegi szabállyal nem indítható.',
           '- **Módosított céllal indul:** minden összeállítás mért adata (pontosság, lefedettség, régi arany, kapuhiba, '
           'bizonyossági szintek, vetített költség) rendelkezésre áll; a Döntési szabály, a PD6 vagy a G4 módosítása '
           'felhasználói döntés; az a–e tétel és a prompt túlkötése regressziós mérésre átvéve (jegyzet v2, prompt_v3, F3V3).',
           '- **Elhalasztva:** az eszközök, az arany v2 és a mért adat megmarad; az a–e tétel regressziós mérésre átvéve, a lezárt f–k tétel dokumentálva.', '']

    # (f) korrigált
    ki += ['## (f) A korrigált értékek (Opus-besorolás, nem mérés)', '',
           'A küszöb szempontjából csak a mért érték számít. A (c)-hibák (az arany szerinti valódi C-hibák) darabszáma az '
           'Opus besorolása: F3 × arany v1: %d; F3 × arany v2: %d; F3V2 × arany v2: %d (f21p/c_diff_besorolas.tsv, '
           'f21p/c_diff_f3v2_osszevetes.tsv). A korrigált pontosság és lefedettség: naplok/F21P_C_diff.md és '
           'naplok/F21P_C_diff_F3V2.md, ugyanezzel a jelöléssel.' % (v1_c, f3_c, f3v2_c), '']
    ki += javaslat_szakasz()
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(ki) + '\n')
    print('-> %s' % KIMENET)


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--regi':
        # a régi számok összevetése: python jelentes_f21p.py --regi <a korábbi F21P_jelentes.md>
        n, hiany = regi_szamok_osszevet(sys.argv[2], KIMENET)
        print('régi számok: %d előfordulás; hiányzó: %s' % (n, hiany or 'nincs (minden régi szám megvan)'))
        sys.exit(1 if hiany else 0)
    main()
