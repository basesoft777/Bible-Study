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
import tokenek  # noqa: E402

F21P = os.path.join(tokenek.ROOT, 'f21p')
KIMENET = os.path.join(tokenek.ROOT, 'naplok', 'F21P_jelentes.md')
RETEGEK = ['R1', 'R2', 'R3', 'R4', 'Összes']


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

    def kc(o, r):
        x = kp.get('vetites', o, r, 'koltseg_usd')
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
        b = minos[(o, 'minosites (PD9 szerinti kizárással)')]
        ki.append('- **%s: %s** (%s); a PD9 szerinti kizárással is: %s (%s).' % (o, a['szamlalo'], a['megjegyzes'], b['szamlalo'], b['megjegyzes']))
    ki.append('- Az A, a B és a C egymodelles összeállítás: a PD6 szerint nem minősíthető.')
    ki.append('- A Döntési szabály „Javaslat” pontjához (tények): rétegenként sem az A+B, sem az A+B+C nem teljesíti a '
              'rétegfeltételeket (l. lent), tehát a szabály szerinti eset: „egyik sem” — a bukott feltételek a táblákban.')
    ki += ['', '### Az öt feltétel összeállításonként és rétegenként', '',
           'Feltételek: (1) `magas` pontosság ≥ 98% rétegenként; (2) lefedettség ≥ 95%; (3) régi arany ≥ 95% (halmaz-'
           'definíció; kizárás nélkül / PD9 szerinti kizárással); (4) vetített költség 90%-os felső széle ≤ 60 USD '
           '(teljes Biblia, rétegenként a réteg része); (5) vetített `alacsony` arány ≤ 10% (link-arány a végső '
           'kimenetben; a 200 versen / az aranyon). Egymodelles összeállításnál az (1) és az (5) n.é. (PD6); az (1) '
           'helyén az összpontosság tájékoztatásul áll.', '',
           '| összeállítás | réteg | (1) magas pontosság | (2) lefedettség | (3) régi arany: kizárás nélkül / PD9 | (4) költség USD [90%] | (5) alacsony: 200 vers / arany |',
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
                g('feltetelek', o, r, 'regi_arany_pd9_kizarassal'), kc(o, r), al))
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
    ki += ['### P5 minden összeállításra (teljes Biblia, 90%-os intervallum)', '',
           '**Eltérés a brieftől:** a bootstrap egysége a köteg, nem a vers (DT21 f, nyitott, nincs jóváhagyva). Az ár a '
           'modell táblaára × a futás mért cost/táblaár aránya (az A-nál és a B-nél a cost nem egyenlő a táblaárral).', '',
           '| összeállítás | R1 | R2 | R3 | R4 | Összes |', '|---|---|---|---|---|---|']
    for o in oss_mind + ['C döntőbíró rész']:
        ki.append('| %s | %s |' % (o, ' | '.join(kc(o, r) for r in RETEGEK)))
    ki += ['', '| futás | cost/táblaár (s) | újrakérés-szorzó M | ellenőrzés mintán belül | leave-one-out |', '|---|---|---|---|---|']
    for f in ('F1V2', 'F2V2', 'F3V2', 'F3V2B', 'F4V2'):
        ki.append('| %s | %s | %s | %s%% | %s%% |' % (f, kp.get('ar', f, '-', 'cost1_per_tablaar_s')['ertek'], kp.get('ar', f, '-', 'ujrakeres_szorzo_M')['ertek'],
                                                  kp.get('ellenorzes', f, '-', 'elteres_szazalek')['ertek'], kp.get('ellenorzes', f, '-', 'loo_elteres_szazalek')['ertek']))
    naplo = _tsv('futasnaplo.tsv')
    ki.append('')
    ki.append('A pilot tényleges költsége (futásnapló, minden futás, P3 és P3b): %.6f USD. A C (F3V2) vetítés intervalluma '
              'itt kissé eltér a P3-as koltseg_vetites.tsv-étől, mert a két szkript bootstrapja más véletlenszám-sorrendet '
              'használ (azonos mag mellett).' % sum(float(r['koltseg_usd']) for r in naplo))
    ki.append('')
    ki.append('Döntőbírói versarány rétegenként (F4V2): %s. Kézimunka-vetítés (A+B+C, G4): vetített `alacsony` link a '
              'Bibliára %s (alt olvasat: %s); vetített eltérés az aranyhoz mérten %s; a (c)-hiba/vers az A+B+C-re n.é. '
              '(nincs besorolva).' % (
                  ', '.join('%s %s' % (r, kp.get('dontobiro', 'F4V2', r, 'dontobirohoz_meno_versek_aranya')['megjegyzes']) for r in RETEGEK[:4]),
                  kp.get('kezimunka', 'A+B+C', 'Összes', 'vetitett_alacsony_link_biblia')['ertek'],
                  kp.get('kezimunka', 'A+B+C (alt)', 'Összes', 'vetitett_alacsony_link_biblia')['ertek'],
                  kp.get('kezimunka', 'A+B+C', 'Összes', 'vetitett_elteres_biblia')['ertek']))
    ki.append('')
    ki.append('*A lenti szakaszok a P3 (a P3b előtti) adatát őrzik változatlanul (v1-A/B, F3/F3V2); a P3b-eredmény a fenti.*')
    ki.append('')
    return ki


def main():
    m1 = T('meres_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    m2 = T('meres_v2_eredmeny.tsv', ['szakasz', 'osszeallitas', 'reteg', 'mero'])
    kv = T('koltseg_vetites.tsv', ['szakasz', 'futas', 'reteg', 'mero'])
    ing = T('ingadozas.tsv', ['szakasz', 'reteg', 'mero'])

    def p1(sz, oss, ret, mero):
        r = m1.get(sz, oss, ret, mero)
        return pct(r['szamlalo'], r['nevezo'])

    def p2(sz, oss, ret, mero):
        r = m2.get(sz, oss, ret, mero)
        return pct(r['szamlalo'], r['nevezo'])

    naplo = _tsv('futasnaplo.tsv')
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
          'f21p/c_diff_f3v2b_besorolas.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
          'kézzel szerkeszteni tilos -->' % tokenek.generalas_ts(), '',
          'A számok kizárólag szkriptkimenetből jönnek (a forrás soronként jelölve). A **korrigált** értékek '
          'kizárólag „**Opus-besorolás, nem mérés**” jelöléssel szerepelnek; a küszöb szempontjából csak a mért '
          'érték számít (PD10). A jelentés nem ajánl döntést a #22-ről.', '']
    ki += p3b_szakasz()
    c_regi0 = m2.get('regi_arany', 'F3V2', 'Összes', 'egyezes')
    c_regik = m2.get('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva')
    c3_regi0 = m1.get('regi_arany', 'C', 'Összes', 'egyezes')
    REGI_JEL = ('a kizárás a küszöb átlépését fordítja meg; a kizárás a futás után, a C két nem-egyezése alapján '
                'történt (PD9); az 1Móz 13:4 a besorolásban vitatható, a f21p/regi_arany_hibas.tsv-ben hibás')
    ki += ['## Összefoglaló — P3 (korábbi, a P3b előtt: v1-A/B, F3/F3V2)', '',
           '- **Egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8, az F4 nem futott).**',
           '- Az A+B két mért feltételen bukott: az A∩B (`magas`) pontosság R1-ben, R3-ban és R4-ben a 98%% alatt van, '
           'a régi arany egyezése %s (a 95%% alatt).' % p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes'),
           '- A C egymodelles összeállítás, a PD6 szerint nem minősíthető. A C régi arany egyezése: kizárás nélkül '
           '%s — a 95%% alatt; a PD9 szerinti kizárással %s — %s.' % (
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
    c_regi = p2('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva')
    c_ko = kv.get('vetites', 'F3V2', 'Összes', 'koltseg_usd')
    ki.append('| A | n.é. (egymodelles, PD6) | mért: %s — nem minősíthető | mért: %s | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |'
              % (p1('pontossag_lefedettseg', 'A', 'Összes', 'lefedettseg'), p1('regi_arany', 'A', 'Összes', 'egyezes')))
    ki.append('| B | n.é. (egymodelles, PD6) | mért: %s — nem minősíthető | mért: %s | nem vetítve (PD8: kiesett) | n.é. (PD6) | nem minősíthető (PD6) |'
              % (p1('pontossag_lefedettseg', 'B', 'Összes', 'lefedettseg'), p1('regi_arany', 'B', 'Összes', 'egyezes')))
    ki.append('| C | n.é. (egymodelles, PD6) | mért: F3 %s (arany v1), F3V2 %s (arany v2) — nem minősíthető | mért: kizárás nélkül F3 %s, F3V2 %s — a 95%% alatt; a PD9 szerinti kizárással F3V2 %s (%s) | vetítve: F3 %s USD [%s–%s], F3V2 %s USD [%s–%s] (90%%) | n.é. (PD6) | nem minősíthető (PD6) |'
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
        for mero in ('egyezes', 'egyezes_hibas_kizarva'):
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
           '### Régi arany egyezés (halmaz-definíció, PD9; a 2 hibás hármas nélkül is)', '',
           '| összeállítás | kizárás nélkül | hibás hármasok nélkül |', '|---|---|---|']
    for o in ('A', 'B', 'C', 'A+B magas (A∩B)'):
        ki.append('| %s (arany-független, 200 verses minta) | %s | %s |' % (
            o, p1('regi_arany', o, 'Összes', 'egyezes'), p1('regi_arany', o, 'Összes', 'egyezes_hibas_kizarva')))
    ki.append('| C — F3V2 | %s | %s |' % (p2('regi_arany', 'F3V2', 'Összes', 'egyezes'), p2('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva')))
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
           'hívásonként, 10 versre ismert, versenként nem mérhető). Ez a DT21 f) nyitott tétele, **nincs jóváhagyva**.', '',
           'Módszer: illesztés tokenfajtánként az első próbálkozású hívásokon (bemenet = a + b·x + c·k; kimenet = a + b·x; '
           'x = eredeti + Károli-szavak, k = KJV-támpont szavai); a teljes Biblia valódi vershosszai (Karoli_1908, '
           'TAHOT/TAGNT); ár a cost mezőből; az újrakérés a pilot mért szorzójával; bootstrap a kötegek felett (1000); '
           'ellenőrzés a 200 versen.', '',
           '| réteg | könyvek | versek |', '|---|---|---|']
    for r in ('R1', 'R2', 'R3', 'R4'):
        ki.append('| %s | %s | %s |' % (r, kv.get('reteg_besorolas', '-', r, 'konyvek')['ertek'], kv.get('biblia', '-', r, 'versek')['ertek']))
    ki += ['', 'A besorolás szabálya: műfaj és kánonrész, a minta rétegeivel összhangban (R1: Törvény, történeti könyvek, '
           'Péld, Préd; R2: Jób, Zsolt, Én; R3: Ézs–Mal a Siralmakkal és Dániellel; R4: az ÚSZ).', '',
           '| futás | illesztés (bemenet a/b/c; kimenet a/b) | cost/táblaár (1. próba) | újrakérés-szorzó M | 200 vers: vetített / tényleges (eltérés) | leave-one-out eltérés |',
           '|---|---|---|---|---|---|']
    for f in ('F3', 'F3V2'):
        ki.append('| %s | %s ; %s | %s | %s | %s / %s USD (%s%%) | %s%% |' % (
            f, kv.get('illesztes', f, '-', 'bemenet_a_b_c')['ertek'], kv.get('illesztes', f, '-', 'kimenet_a_b')['ertek'],
            kv.get('ar', f, '-', 'cost1_per_tablaar')['ertek'], kv.get('ar', f, '-', 'ujrakeres_szorzo_M')['ertek'],
            kv.get('ellenorzes', f, '-', 'pilot_200_vetitett_usd')['ertek'], kv.get('ellenorzes', f, '-', 'pilot_200_tenyleges_usd')['ertek'],
            kv.get('ellenorzes', f, '-', 'elteres_szazalek')['ertek'], kv.get('ellenorzes', f, '-', 'loo_elteres_szazalek')['ertek']))
    ki += ['', 'Az újrakérések cost-ja nem lineáris a tokenben (a megismételt előtag gyorsítótárazott), ezért az '
           'újrakérést nem tokenből, hanem a mért M szorzóval vetítjük.', '',
           '| réteg | F3 (prompt v1) USD [90%] | F3V2 (prompt v2) USD [90%] |', '|---|---|---|']
    for r in RETEGEK:
        a, b = kv.get('vetites', 'F3', r, 'koltseg_usd'), kv.get('vetites', 'F3V2', r, 'koltseg_usd')
        ki.append('| %s | %s [%s–%s] | %s [%s–%s] |' % (r, a['ertek'], a['also90'], a['felso90'], b['ertek'], b['also90'], b['felso90']))
    ki += ['', '**Kézimunka-vetítés (C):** az aranyon mért eltérés/vers és a (c)-hiba/vers (ez utóbbi Opus-besorolás, nem mérés), '
           'rétegenként a teljes Bibliára; a rétegenkénti arany kis mintájú (10–20 vers). `alacsony` arány: n.é. (PD6).', '',
           '| futás | eltérés/vers (mért, 60 aranyvers) | vetített eltérés a Bibliára | (c)/vers (Opus-besorolás, nem mérés) | vetített (c) a Bibliára (Opus-besorolás, nem mérés) |',
           '|---|---|---|---|---|']
    for f in ('F3', 'F3V2'):
        ki.append('| %s | %s | %s | %s | %s |' % (
            f, kv.get('kezimunka', f, 'Összes', 'elteres_per_vers_arany_v2')['ertek'], kv.get('kezimunka', f, 'Összes', 'vetitett_elteres_biblia')['ertek'],
            kv.get('kezimunka', f, 'Összes', 'c_hiba_per_vers')['ertek'], kv.get('kezimunka', f, 'Összes', 'vetitett_c_hiba_biblia')['ertek']))
    ki.append('')

    # (e) nyitott tételek, eszközök, korlátok
    ki += ['## (e) Nyitott tételek a #22 esetleges újraindításához (DT21), átvihető eszközök, megtanult korlátok', '',
           '### Öt nyitott tétel (nincs v3, nincs újabb futás; DT21)', '',
           '1. **G / K7:** a prompt_v2 G-szabályának kivétele („többtagú igei szerkezet minden tagja”) tágabb, mint a jegyzet '
           'K7-e (*tudja vala*, *megy vala*): melyik az irányadó.',
           '2. **C:** a prompt „azt, őt …” felsorolása a C-nél az *\'et* nélküli, betoldott tárgyi névmásokra is általánosult.',
           '3. **„azt … hogy” / „azért … hogy”:** az arany az előbbit betoldásnak veszi, az utóbbit (Mt 21:4) köti.',
           '4. **2Móz 26:13 *is*:** a K9 szerint a *ve-* az *is*-hez köthető volna; az arany v2 forditatlan-nak veszi (az F3V2-nél (b)).',
           '5. **D:** a birtokláncban (*szolgálójának szemét*) nem egyértelmű, melyik szó viseli a ragot.', '',
           'További nyitott tétel a P3b-ből (DT21 k): **k)** a G4 szerinti `alacsony` arány két olvasata az A+B+C-nél '
           '(szó szerinti: a kapuhibás maradt versben a C minden linkje alacsony; „alt”: a túlélő modellel egyező C-link '
           '`közepes`) és az A+B döntőbíró nélküli meghatározása (A∩B = `magas`, a többi link `alacsony`); a jelentés '
           'értelmezése, nem a briefé; az (5) feltétel egyik olvasattal sem teljesül.', '',
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
           '- Gondolkodási mód (eltérés a brief Keretek pontjától, amely mindhárom modellnél azonos beállítást kért): az A '
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
           'felhasználói döntés; az öt nyitott tétel és a prompt túlkötése nyitott.',
           '- **Elhalasztva:** az eszközök, az arany v2 és a mért adat megmarad; a nyitott tételek dokumentálva.', '']

    # (f) korrigált
    ki += ['## (f) A korrigált értékek (Opus-besorolás, nem mérés)', '',
           'A küszöb szempontjából csak a mért érték számít. A (c)-hibák (az arany szerinti valódi C-hibák) darabszáma az '
           'Opus besorolása: F3 × arany v1: %d; F3 × arany v2: %d; F3V2 × arany v2: %d (f21p/c_diff_besorolas.tsv, '
           'f21p/c_diff_f3v2_osszevetes.tsv). A korrigált pontosság és lefedettség: naplok/F21P_C_diff.md és '
           'naplok/F21P_C_diff_F3V2.md, ugyanezzel a jelöléssel.' % (v1_c, f3_c, f3v2_c), '']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(ki) + '\n')
    print('-> %s' % KIMENET)


if __name__ == '__main__':
    main()
