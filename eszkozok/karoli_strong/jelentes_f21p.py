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
          'konkordancia/Karoli_Strong_kivonat.tsv | ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | '
          'kézzel szerkeszteni tilos -->' % tokenek.generalas_ts(), '',
          'A számok kizárólag szkriptkimenetből jönnek (a forrás soronként jelölve). A **korrigált** értékek '
          'kizárólag „**Opus-besorolás, nem mérés**” jelöléssel szerepelnek; a küszöb szempontjából csak a mért '
          'érték számít (PD10). A jelentés nem ajánl döntést a #22-ről.', '']
    c_regi0 = m2.get('regi_arany', 'F3V2', 'Összes', 'egyezes')
    c_regik = m2.get('regi_arany', 'F3V2', 'Összes', 'egyezes_hibas_kizarva')
    c3_regi0 = m1.get('regi_arany', 'C', 'Összes', 'egyezes')
    REGI_JEL = ('a kizárás a küszöb átlépését fordítja meg; a kizárás a futás után, a C két nem-egyezése alapján '
                'történt (PD9); az 1Móz 13:4 a besorolásban vitatható, a f21p/regi_arany_hibas.tsv-ben hibás')
    ki += ['## Összefoglaló', '',
           '- **Egyik mért összeállítás sem felel meg; az A+B+C nem mért (PD8, az F4 nem futott).**',
           '- Az A+B két mért feltételen bukott: az A∩B (`magas`) pontosság R1-ben, R3-ban és R4-ben a 98%% alatt van, '
           'a régi arany egyezése %s (a 95%% alatt).' % p1('regi_arany', 'A+B magas (A∩B)', 'Összes', 'egyezes'),
           '- A C egymodelles összeállítás, a PD6 szerint nem minősíthető. A C régi arany egyezése: kizárás nélkül '
           '%s — a 95%% alatt; a PD9 szerinti kizárással %s — %s.' % (
               pct(c_regi0['szamlalo'], c_regi0['nevezo']), pct(c_regik['szamlalo'], c_regik['nevezo']), REGI_JEL), '']

    # (a) EREDMÉNY
    ki += ['## (a) Eredmény', '',
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
    ki += ['## (b) Mi bukott el (csak a rögzített öt feltétel)', '',
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
    ki += ['## (b2) Mérőszámok összeállításonként és rétegenként (P-K4; forrás: meres_eredmeny.tsv, arany v1)', '',
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
    ki += ['## (c) A mért számok', '', '### Pontosság és lefedettség (C; forrás: meres_v2_eredmeny.tsv)', '',
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
    ki.append('| **a pilot összesen** | **%.6f** (plafon: 3 USD) |' % pilot_cost)
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
    ki += ['## (d) Költségvetítés (P5, csak a C; forrás: koltseg_vetites.tsv)', '',
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
           '- **Marad (a jelenlegi céllal):** a Döntési szabály szerint egyik mért összeállítás sem felel meg; az A+B+C '
           'nem mért (PD8), az A és a B kiesett, a C egyedül a PD6 szerint nem minősíthető. A teljes futás a jelenlegi '
           'szabállyal nem indítható.',
           '- **Módosított céllal indul:** a mért adat (C pontossága, lefedettsége, kapuhibája, a vetített költség) '
           'rendelkezésre áll; a Döntési szabály vagy a PD6 módosítása felhasználói döntés; az öt nyitott tétel és a '
           'prompt túlkötése nyitott.',
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
