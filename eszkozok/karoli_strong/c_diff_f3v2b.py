#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.27 — a C második futásának (F3V2B) C-diffje, az F3V2-vel összevetve, és az
A+B+C (F4V2) gépi diffje az arany v2-höz. Nincs API-hívás.

F3V2B (azonos prompt és konfiguráció, mint az F3V2):
  * gépi eltérések az arany v2-höz (hiányzó / többlet), a meres.py linkhalmazaival;
  * összevetés az F3V2 eltéréseivel: közös (mindkét futásban ugyanaz az eltérés —
    az F3V2 kézi besorolását örökli, f21p/c_diff_f3v2_osszevetes.tsv), csak_f3v2b
    (új az F3V2-höz képest — kézi besorolás: f21p/c_diff_f3v2b_besorolas.tsv),
    csak_f3v2 (az F3V2 eltérése, amely az F3V2B-nél nincs);
  * a (c) esetek száma: azonos / új / megszűnt — ez a futásközi ingadozás
    alapja (azonos prompt mellett).
A+B+C: a végső kimenet (meres_p3b.osszeallitas_kimenet, G4) eltérései az arany
v2-höz, rétegenként és bizonyossági szintenként, gépi összesítés (kézi besorolás
nélkül).

Módok:
  --lista   a csak_f3v2b eltérések kontextussal (a kézi besoroláshoz)
  (alap)    ellenőrzi, hogy minden csak_f3v2b eltérésnek van besorolása és
            fordítva, majd megírja a naplok/F21P_C_diff_F3V2B.md-t.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_diff  # noqa: E402
import c_diff_f3v2 as cf  # noqa: E402
import meres  # noqa: E402
import meres_p3b  # noqa: E402
import tokenek  # noqa: E402

BESOROLAS_UT = os.path.join(tokenek.ROOT, 'f21p', 'c_diff_f3v2b_besorolas.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_C_diff_F3V2B.md')
OSZLOPOK = ['igehely', 'reteg', 'irany', 'k_poz', 'e_poz', 'osztaly', 'konvencio_vagy_jegyzetpont', 'indok']


def elteresek(adat, f):
    return cf.elteresek(adat, f, adat.arany_linkek)   # az adat.arany itt a v2


def f3v2_osztaly():
    """{kulcs: osztály} az F3V2 eltéréseire (a F21.16-os kézi besorolásból)."""
    ki = {}
    for r in c_diff._tsv(cf.OSSZEVETES_UT, cf.OSZLOPOK):
        if r['statusz'] in ('maradt', 'uj', 'oroklott'):
            ki[(r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))] = r['f3v2_osztaly']
    return ki


def osszevet(adat):
    e2 = elteresek(adat, 'F3V2')
    eb = elteresek(adat, 'F3V2B')
    return e2, eb


def lista(adat):
    e2, eb = osszevet(adat)
    import json
    for kk in sorted(set(eb) - set(e2), key=lambda x: (adat.versek.index(x[0]), x[1], x[2], x[3])):
        ig = kk[0]
        print('%s [%s] %s %s -> %s' % (ig, eb[kk], kk[1], c_diff._magyar(adat, ig, kk[2]), c_diff._eredeti(adat, ig, kk[3])))
        print('    F3V2B: %s' % json.dumps(adat.futas['F3V2B'][ig]['obj']['parok']))
        print('    F3V2 : %s' % json.dumps(adat.futas['F3V2'][ig]['obj']['parok']))
        print('    ARANY: %s' % json.dumps(adat.arany[ig]['parok']))


def ellenoriz(adat):
    e2, eb = osszevet(adat)
    uj = set(eb) - set(e2)
    hibak = []
    kezi = {}
    if os.path.exists(BESOROLAS_UT):
        for r in c_diff._tsv(BESOROLAS_UT, OSZLOPOK):
            k = (r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))
            kezi[k] = r
            if r['osztaly'] not in c_diff.OSZTALYOK:
                hibak.append('érvénytelen osztály: %s' % (k,))
            if not r['indok'].strip():
                hibak.append('üres indok: %s' % (k,))
    for k in sorted(uj - set(kezi)):
        hibak.append('besorolás nélküli új F3V2B-eltérés: %s' % (k,))
    for k in sorted(set(kezi) - uj):
        hibak.append('besorolás, amelyhez nincs új F3V2B-eltérés: %s' % (k,))
    return hibak, e2, eb, kezi


def jelentes(adat, e2, eb, kezi):
    o2 = f3v2_osztaly()
    ts = tokenek.generalas_ts()
    kozos = set(e2) & set(eb)
    csak_b = set(eb) - set(e2)
    csak_2 = set(e2) - set(eb)

    def osz_b(k):
        return o2[k] if k in kozos else kezi[k]['osztaly']

    ki = ['# F21P_C_diff_F3V2B.md — a C második futása (F3V2B) az F3V2-vel összevetve; az A+B+C gépi diffje', '',
          '<!-- GENERÁLT: eszkozok/karoli_strong/c_diff_f3v2b.py | scope=F3V2 és F3V2B a 60 aranyversen (arany v2); '
          'A+B+C (F1V2, F2V2, F4V2, G4) | forras=f21p/valaszok/{F3V2,F3V2B,F1V2,F2V2,F4V2}.jsonl, f21p/arany_opus_v2.jsonl '
          '(sha256 ellenőrizve), f21p/meres_kizaras.tsv, f21p/c_diff_f3v2_osszevetes.tsv, f21p/c_diff_f3v2b_besorolas.tsv '
          '| ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->' % ts, '',
          'A közös eltérések (mindkét futásban ugyanaz a link hiányzik vagy többlet) az F3V2 kézi besorolását '
          'öröklik; az F3V2B új eltéréseit (csak_f3v2b) az Opus sorolta be. **Az osztályok az Opus besorolása, nem '
          'mérés.** Azonos prompt mellett a két futás eltérése a futásközi ingadozás becslése.', '',
          '## 1. Eltérések rétegenként', '',
          '| réteg | F3V2 eltérés | F3V2B eltérés | közös | csak F3V2B | csak F3V2 |', '|---|---|---|---|---|---|']
    for r in meres.RETEGEK + [meres.OSSZES]:
        def n(hz):
            return sum(1 for k in hz if r == meres.OSSZES or adat.reteg[k[0]] == r)
        ki.append('| %s | %d | %d | %d | %d | %d |' % (r, n(e2), n(eb), n(kozos), n(csak_b), n(csak_2)))
    ki += ['', '## 2. A (c) esetek (az Opus besorolása, nem mérés)', '',
           '| réteg | F3V2 (c) | F3V2B (c) | azonos (c) | új (c) az F3V2B-nél | megszűnt (c) (az F3V2-nél volt) |',
           '|---|---|---|---|---|---|']
    for r in meres.RETEGEK + [meres.OSSZES]:
        def v(k):
            return r == meres.OSSZES or adat.reteg[k[0]] == r
        c2 = [k for k in e2 if v(k) and o2.get(k) == 'c']
        cb = [k for k in eb if v(k) and osz_b(k) == 'c']
        az = [k for k in cb if k in kozos]
        ujc = [k for k in cb if k in csak_b]
        megsz = [k for k in c2 if k in csak_2]
        ki.append('| %s | %d | %d | %d | %d | %d |' % (r, len(c2), len(cb), len(az), len(ujc), len(megsz)))
    ki += ['', '## 3. Az F3V2B új eltérései (kézi besorolás)', '',
           '| vers | irány | magyar szó | eredeti szó | osztály | konvenció / jegyzetpont | indok |', '|---|---|---|---|---|---|---|']
    for k in sorted(csak_b, key=lambda x: (adat.versek.index(x[0]), x[1], x[2], x[3])):
        r = kezi[k]
        ki.append('| %s | %s | %s | %s | %s | %s | %s |' % (k[0], k[1], c_diff._magyar(adat, k[0], k[2]),
                                                           c_diff._eredeti(adat, k[0], k[3]), r['osztaly'],
                                                           r['konvencio_vagy_jegyzetpont'] or '—', r['indok']))
    ki += ['', '## 4. Az F3V2 eltérései, amelyek az F3V2B-nél nincsenek (osztály az F3V2 besorolásából)', '',
           '| vers | irány | magyar szó | eredeti szó | F3V2-osztály |', '|---|---|---|---|---|']
    for k in sorted(csak_2, key=lambda x: (adat.versek.index(x[0]), x[1], x[2], x[3])):
        ki.append('| %s | %s | %s | %s | %s |' % (k[0], k[1], c_diff._magyar(adat, k[0], k[2]), c_diff._eredeti(adat, k[0], k[3]), o2.get(k, '?')))
    # A+B+C gépi diff
    kim = meres_p3b.osszeallitas_kimenet(adat)
    ki += ['', '## 5. Az A+B+C (G4) gépi diffje az arany v2-höz (kézi besorolás nélkül)', '',
           '| réteg | hiányzó | többlet (magas) | többlet (kozepes) | többlet (alacsony) | aranyvers |', '|---|---|---|---|---|---|']
    for r in meres.RETEGEK + [meres.OSSZES]:
        vs = [ig for ig in adat.versek if ig in adat.arany and (r == meres.OSSZES or adat.reteg[ig] == r)]
        hi = sum(len(adat.arany_linkek(ig) - set(kim[ig]['A+B+C'])) for ig in vs)
        tb = {s: sum(1 for ig in vs for l, x in kim[ig]['A+B+C'].items() if x == s and l not in adat.arany_linkek(ig))
              for s in meres_p3b.SZINTEK}
        ki.append('| %s | %d | %d | %d | %d | %d |' % (r, hi, tb['magas'], tb['kozepes'], tb['alacsony'], len(vs)))
    ki.append('')
    with open(JELENTES_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def main():
    adat = meres_p3b.betolt()
    if '--lista' in sys.argv:
        lista(adat)
        return 0
    hibak, e2, eb, kezi = ellenoriz(adat)
    if hibak:
        print('HIBA (a jelentés nem íródott):')
        for h in hibak:
            print('  ' + h)
        return 1
    jelentes(adat, e2, eb, kezi)
    print('F3V2: %d, F3V2B: %d eltérés; közös %d, csak F3V2B %d, csak F3V2 %d -> %s' % (
        len(e2), len(eb), len(set(e2) & set(eb)), len(set(eb) - set(e2)), len(set(e2) - set(eb)), JELENTES_UT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
