#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.42 — a (c) hibák újrabesorolásához a gépi diff: a Sonnet (SONNETV3) és az F3V3 (C,
prompt_v3) eltérései az arany LEGFRISSEBB befagyasztott változatához (P3c, PD13). Nincs
API-hívás. A kézi besorolás (a / b / c) a futás után az orkesztrátor / az Opus dolga; ez a
szkript csak a gépi részt, a kézi-besorolási vázat és az ellenőrzést adja.

Eltérés = a kapun átment aranyverseken az arany linkjei közül hiányzó (`hianyzo`) vagy a
futás többlet (`tobblet`) linkje, a meres_p3c.betolt linkhalmazaival (a meres_kizaras.tsv
tokenjei mind a két oldalról kimaradnak) — a c_diff_f3v2.elteresek változatlanul.

Módok:
  --lista       az eltérések kontextussal (a kézi besoroláshoz)
  --sablon      a kézi besorolás váza: f21p/c_diff_p3c_besorolas.tsv, `# MANUAL` fejléccel, a
                c_diff_f3v2b_besorolas.tsv mintájára; a gépi oszlopok kitöltve (futás, vers,
                réteg, irány, pozíciók, magyar szó, eredeti szó, és az `elozmeny_v2`: ha ugyanez
                az eltérés a v2-es arany szerinti F3V2/F3V2B besorolásban szerepelt, annak osztálya),
                az `osztaly`, `konvencio_vagy_jegyzetpont`, `indok` üres (kézi). Meglévő fájlt NEM
                ír felül (--felulir nélkül hiba).
  (alap)        ha nincs besorolás-fájl: gépi összesítés (naplok/F21P_C_diff_p3c.md, a kézi rész
                nélkül); ha van: ellenőrzi (minden eltérésnek pontosan egy besorolása, érvényes
                osztály, nem üres indok), és hibamentesen a teljes jelentést írja; hibánál 1-es
                kilépési kód, a jelentés nem íródik.
Az osztályok jelentése a c_diff.py-ban: a = a Károli-szó/konvenció szerint védhető (a modell
a konvencióhoz képest tévedett), b = a jegyzet/arany alternatívája, c = valódi modellhiba.

Kimenet: naplok/F21P_C_diff_p3c.md (generált; fejléc: scope | forras | ts).
    python eszkozok/karoli_strong/c_diff_p3c.py [--lista|--sablon [--felulir]] [--arany <jsonl> [--arany-sha <f>]]
"""

import argparse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import c_diff  # noqa: E402
import c_diff_f3v2 as cf  # noqa: E402
import c_diff_f3v2b  # noqa: E402
import meres  # noqa: E402
import meres_p3c  # noqa: E402
import tokenek  # noqa: E402

BESOROLAS_UT = os.path.join(tokenek.ROOT, 'f21p', 'c_diff_p3c_besorolas.tsv')
JELENTES_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_C_diff_p3c.md')
FUTASOK = [meres_p3c.SONNET, meres_p3c.C3]
OSZLOPOK = ['futas', 'igehely', 'reteg', 'irany', 'k_poz', 'e_poz', 'magyar', 'eredeti', 'elozmeny_v2', 'osztaly',
            'konvencio_vagy_jegyzetpont', 'indok']
GEPI = OSZLOPOK[:9]


def elteresek(adat, futasok=FUTASOK):
    """{(futas, igehely, irany, k, e): reteg} a megadott futásokra (a c_diff_f3v2.elteresek)."""
    ki = {}
    for f in futasok:
        for (ig, irany, k, e), ret in cf.elteresek(adat, f, adat.arany_linkek).items():
            ki[(f, ig, irany, k, e)] = ret
    return ki


def sorrend(adat, futasok, kulcsok):
    return sorted(kulcsok, key=lambda x: (futasok.index(x[0]), adat.versek.index(x[1]), x[2], x[3], x[4]))


def elozmenyek():
    """{(igehely, irany, k, e): 'F3V2:c' | 'F3V2B:a' ...} a v2-es arany szerinti korábbi kézi besorolásból
    (tájékoztató: ha a legfrissebb arany más, a kulcsok eltérhetnek)."""
    ki = {}
    try:
        for kulcs, o in c_diff_f3v2b.f3v2_osztaly().items():
            ki[kulcs] = 'F3V2:%s' % o
    except (OSError, SystemExit):
        pass
    if os.path.exists(c_diff_f3v2b.BESOROLAS_UT):
        for r in c_diff._tsv(c_diff_f3v2b.BESOROLAS_UT, c_diff_f3v2b.OSZLOPOK):
            kulcs = (r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))
            ki.setdefault(kulcs, 'F3V2B:%s' % r['osztaly'])
    return ki


def gepi_sorok(adat, el, elozm, futasok=FUTASOK):
    """A gépi oszlopok soronként (a kézi besorolás váza)."""
    sorok = []
    for k in sorrend(adat, futasok, el):
        f, ig, irany, kp, ep = k
        magyar = c_diff._magyar(adat, ig, kp).split(' ', 1)[1]
        eredeti = c_diff._eredeti(adat, ig, ep)
        sorok.append([f, ig, el[k], irany, str(kp), str(ep), magyar, eredeti, elozm.get((ig, irany, kp, ep), '')])
    return sorok


def sablon_ir(adat, ut, ts, felulir=False, arany_info=None):
    """A kézi besorolás váza. Meglévő fájlt nem ír felül (felulir nélkül SystemExit)."""
    if os.path.exists(ut) and not felulir:
        raise SystemExit('HIBA: %s már létezik (a kézi besorolás nem íródik felül; --felulir csak szándékosan)' % ut)
    el = elteresek(adat)
    sorok = gepi_sorok(adat, el, elozmenyek())
    verzio = arany_info['verzio'] if arany_info else '?'
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# MANUAL: scope=f21p P3c (c)-újrabesorolás: SONNETV3 és F3V3 eltérései az arany %s-höz (%d eltérés) | '
                'forras=f21p/valaszok/{SONNETV3,F3V3}.jsonl, az arany legfrissebb befagyasztott változata, '
                'eszkozok/karoli_strong/c_diff_p3c.py --sablon | ts=%s (a sablon gépi váza; az osztaly, '
                'konvencio_vagy_jegyzetpont és indok oszlop KÉZI, még üres; a besorolás idejét a besoroló frissíti) | '
                'a gépi oszlopok (futas..elozmeny_v2) nem kézzel szerkesztendők\n' % (verzio, len(sorok), ts))
        f.write('\t'.join(OSZLOPOK) + '\n')
        for s in sorok:
            assert all('\t' not in x for x in s)
            f.write('\t'.join(s + ['', '', '']) + '\n')
    return sorok


def beolvas(ut):
    """A kézi besorolás-fájl sorai; a '#' fejlécet átugorja, a fejlécet ellenőrzi."""
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    if fej != OSZLOPOK:
        raise SystemExit('%s: hibás fejléc: %s' % (ut, fej))
    ki = []
    for i, s in enumerate(sorok[1:], 2):
        m = s.split('\t')
        if len(m) != len(OSZLOPOK):
            raise SystemExit('%s %d. sor: %d mező (%d kell)' % (ut, i, len(m), len(OSZLOPOK)))
        ki.append(dict(zip(OSZLOPOK, m)))
    return ki


def ellenoriz(adat, ut, futasok=FUTASOK):
    """(hibák, {kulcs: sor}): minden gépi eltérésnek pontosan egy besorolása, érvényes osztály, nem üres indok."""
    el = elteresek(adat, futasok)
    hibak = []
    kezi = {}
    for r in beolvas(ut):
        k = (r['futas'], r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))
        if k in kezi:
            hibak.append('kétszer besorolt eltérés: %s' % (k,))
        kezi[k] = r
        if r['osztaly'] not in c_diff.OSZTALYOK:
            hibak.append('érvénytelen vagy üres osztály (%s kell): %s' % ('/'.join(c_diff.OSZTALYOK), k))
        if not r['indok'].strip():
            hibak.append('üres indok: %s' % (k,))
        if k in el and r['reteg'] != el[k]:
            hibak.append('a réteg nem egyezik a gépi réteggel: %s' % (k,))
    for k in sorrend(adat, futasok, set(el) - set(kezi)):
        hibak.append('besorolás nélküli eltérés: %s' % (k,))
    for k in sorted(set(kezi) - set(el), key=str):
        hibak.append('besorolás, amelyhez nincs gépi eltérés: %s' % (k,))
    return hibak, kezi


def lista(adat, futasok=FUTASOK):
    el = elteresek(adat, futasok)
    elozm = elozmenyek()
    aktualis = None
    for k in sorrend(adat, futasok, el):
        f, ig, irany, kp, ep = k
        if (f, ig) != aktualis:
            aktualis = (f, ig)
            print('\n%s [%s] %s' % (ig, adat.reteg[ig], f))
            print('    %s: %s' % (f, json.dumps(adat.futas[f][ig]['obj']['parok'])))
            print('    ARANY: %s' % json.dumps(adat.arany[ig]['parok']))
        print('  %s %s -> %s%s' % (irany, c_diff._magyar(adat, ig, kp), c_diff._eredeti(adat, ig, ep),
                                  ('   [előzmény: %s]' % elozm[(ig, irany, kp, ep)]) if (ig, irany, kp, ep) in elozm else ''))


def fejlec(info, ts, van_kezi):
    return ('GENERÁLT: eszkozok/karoli_strong/c_diff_p3c.py | scope=SONNETV3 és F3V3 (prompt_v3) a kapun átment aranyversekre, arany %s '
            '(%d vers, sha256 %s) | forras=f21p/valaszok/{SONNETV3,F3V3}.jsonl, %s (sha256 ellenőrizve), f21p/meres_kizaras.tsv%s | '
            'ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos'
            % (info['verzio'], info['aranyversek'], info['sha256'][:16], os.path.basename(info['jsonl']),
               ', f21p/c_diff_p3c_besorolas.tsv (MANUAL)' if van_kezi else '', ts))


def jelentes(adat, info, el, kezi, ut, ts):
    ki = ['# F21P_C_diff_p3c.md — a Sonnet és az F3V3 eltérései az aranytól (a (c) hibák újrabesorolásához)', '',
          '<!-- %s -->' % fejlec(info, ts, kezi is not None), '',
          'Gépi diff: a kapun átment aranyverseken az arany linkjeiből hiányzó és a futás többlet linkjei. **Az osztályok (a / b / c) '
          'kézi besorolás (az Opus / az orkesztrátor), nem mérés.**' + ('' if kezi is not None else
          ' A kézi besorolás-fájl (f21p/c_diff_p3c_besorolas.tsv) még nincs meg: ez a jelentés csak a gépi részt tartalmazza.'), '',
          '## 1. Eltérések futásonként és rétegenként (gépi)', '',
          '| futás | réteg | aranyversek (kapun átment) | hiányzó | többlet | eltérő versek |', '|---|---|---|---|---|---|']
    for f in FUTASOK:
        for r in meres.RETEGEK + [meres.OSSZES]:
            vs = [ig for ig in adat.versek if ig in adat.arany and adat.ok(f, ig) and (r == meres.OSSZES or adat.reteg[ig] == r)]
            ks = [k for k in el if k[0] == f and (r == meres.OSSZES or adat.reteg[k[1]] == r)]
            ki.append('| %s | %s | %d | %d | %d | %d |' % (meres_p3c.NEVEK[f], r, len(vs), sum(1 for k in ks if k[2] == 'hianyzo'),
                                                        sum(1 for k in ks if k[2] == 'tobblet'), len({k[1] for k in ks})))
    ki += ['', '## 2. A két futás közös és eltérő hibái (gépi)', '',
           '| réteg | csak a Sonnet | csak az F3V3 | közös (mindkettő ugyanazt) |', '|---|---|---|---|']
    s_k = {k[1:] for k in el if k[0] == meres_p3c.SONNET}
    c_k = {k[1:] for k in el if k[0] == meres_p3c.C3}
    for r in meres.RETEGEK + [meres.OSSZES]:
        def n(hz):
            return sum(1 for k in hz if r == meres.OSSZES or adat.reteg[k[0]] == r)
        ki.append('| %s | %d | %d | %d |' % (r, n(s_k - c_k), n(c_k - s_k), n(s_k & c_k)))
    if kezi is not None:
        ki += ['', '## 3. A kézi besorolás (a / b / c) futásonként és rétegenként', '',
               '| futás | réteg | a | b | c | összes |', '|---|---|---|---|---|---|']
        for f in FUTASOK:
            for r in meres.RETEGEK + [meres.OSSZES]:
                rs = [x for k, x in kezi.items() if k[0] == f and (r == meres.OSSZES or x['reteg'] == r)]
                ki.append('| %s | %s | %d | %d | %d | %d |' % (meres_p3c.NEVEK[f], r, *(sum(1 for x in rs if x['osztaly'] == o) for o in c_diff.OSZTALYOK), len(rs)))
        ki += ['', '## 4. Az újrabesorolás: az előzmény (v2-es arany, F3V2/F3V2B) és az új osztály', '',
               '| előzmény | a | b | c | összes |', '|---|---|---|---|---|']
        elozm_osztalyok = sorted({x['elozmeny_v2'] or '(nincs előzmény)' for x in kezi.values()})
        for eo in elozm_osztalyok:
            rs = [x for x in kezi.values() if (x['elozmeny_v2'] or '(nincs előzmény)') == eo]
            ki.append('| %s | %d | %d | %d | %d |' % (eo, *(sum(1 for x in rs if x['osztaly'] == o) for o in c_diff.OSZTALYOK), len(rs)))
        ki += ['', '## 5. A (c) esetek (valódi modellhiba, az Opus besorolása)', '',
               '| futás | vers | irány | magyar szó | eredeti szó | előzmény | indok |', '|---|---|---|---|---|---|---|']
        for k in sorrend(adat, FUTASOK, kezi):
            x = kezi[k]
            if x['osztaly'] == 'c':
                ki.append('| %s | %s | %s | %s | %s | %s | %s |' % (meres_p3c.NEVEK[k[0]], k[1], k[2], x['magyar'], x['eredeti'],
                                                                 x['elozmeny_v2'] or '—', x['indok']))
    ki.append('')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def fut(forras_dir=None, arany_ut=None, arany_sha=None, besorolas_ut=None, jelentes_ut=None, ts=None):
    adat, info = meres_p3c.betolt(forras_dir, arany_ut, arany_sha)
    el = elteresek(adat)
    besorolas_ut = besorolas_ut or BESOROLAS_UT
    kezi = None
    if os.path.exists(besorolas_ut):
        hibak, kezi = ellenoriz(adat, besorolas_ut)
        if hibak:
            print('HIBA (a jelentés nem íródott): %d hiba a kézi besorolásban:' % len(hibak))
            for h in hibak[:50]:
                print('  ' + h)
            return 1
    jelentes(adat, info, el, kezi, jelentes_ut or JELENTES_UT, ts or tokenek.generalas_ts())
    print('SONNETV3: %d, F3V3: %d eltérés; kézi besorolás: %s -> %s' % (
        sum(1 for k in el if k[0] == meres_p3c.SONNET), sum(1 for k in el if k[0] == meres_p3c.C3),
        'teljes' if kezi is not None else 'még nincs', jelentes_ut or JELENTES_UT))
    return 0


def onteszt():
    import contextlib
    import io
    import shutil
    import p3c_mock
    hibak = []

    def ellen(f, leiras):
        if not f:
            hibak.append(leiras)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'a régi kimenetek megváltoztak: %s' % p3c_mock.regi_kimenetek_hibak())
    mappa = p3c_mock.ideiglenes('f21p_onteszt_c_diff_p3c_')
    try:
        info = p3c_mock.general(mappa)
        adat, ainfo = meres_p3c.betolt(mappa, info['arany_ut'], info['arany_sha'])
        el = elteresek(adat)
        ellen(len(el) > 0 and {k[0] for k in el} == set(FUTASOK), 'a mock-adaton nincs eltérés mindkét futásra')
        # független újraszámolás az eltérésekre (a saját jsonl-olvasással)
        gold = {}
        with open(info['arany_ut'], encoding='utf-8') as fh:
            for s in fh:
                if s.strip():
                    o = json.loads(s)
                    gold[o['vers']] = {(p[0], e) for p in o['parok'] for e in p[1]}
        kiz = tokenek.meres_kizaras()
        varhato = set()
        for f in FUTASOK:
            with open(os.path.join(mappa, 'valaszok', '%s.jsonl' % f), encoding='utf-8') as fh:
                for s in fh:
                    if not s.strip():
                        continue
                    for ig, v in json.loads(s)['versek'].items():
                        if v['allapot'] != 'ok' or ig not in gold:
                            continue
                        lk = {(p[0], e) for p in v['obj']['parok'] for e in p[1] if (ig, e) not in kiz}
                        g = {(k, e) for k, e in gold[ig] if (ig, e) not in kiz}
                        varhato |= {(f, ig, 'hianyzo', k, e) for k, e in g - lk}
                        varhato |= {(f, ig, 'tobblet', k, e) for k, e in lk - g}
        ellen(set(el) == varhato, 'az eltérések nem egyeznek a független számítással (%d vs %d)' % (len(el), len(varhato)))
        # a kapuhibás versek nem szerepelnek az eltérések között
        ellen(not any(k[1] == info['c_hiba'] for k in el if k[0] == meres_p3c.C3)
              and not any(k[1] == info['sonnet_hiba'] for k in el if k[0] == meres_p3c.SONNET),
              'kapuhibás vers eltérései is szerepelnek')
        # sablon
        ut_b = os.path.join(mappa, 'besorolas.tsv')
        ut_j = os.path.join(mappa, 'jelentes.md')
        sorok = sablon_ir(adat, ut_b, 'T1', arany_info=ainfo)
        ellen(len(sorok) == len(el), 'a sablon sorainak száma nem az eltéréseké')
        with open(ut_b, encoding='utf-8') as f:
            elso = f.readline()
            fej = f.readline().rstrip('\n').split('\t')
        ellen(elso.startswith('# MANUAL: scope=') and ' | forras=' in elso and ' | ts=T1 ' in elso and fej == OSZLOPOK,
              'a sablon fejléce nem a # MANUAL proveniencia / az oszlopok hibásak')
        r0 = beolvas(ut_b)
        ellen(all(x['osztaly'] == '' and x['indok'] == '' and x['konvencio_vagy_jegyzetpont'] == '' for x in r0),
              'a sablon kézi oszlopai nem üresek')
        try:
            sablon_ir(adat, ut_b, 'T2', arany_info=ainfo)
            ellen(False, 'a meglévő besorolás-fájl felülíródott (--felulir nélkül)')
        except SystemExit as e:
            ellen('nem íródik felül' in str(e), 'a felülírás-védelem hibaüzenete hibás: %s' % e)
        with open(ut_b, encoding='utf-8') as f:
            ellen('T1' in f.readline(), 'a védett sablon megváltozott')
        # a kitöltetlen sablon: az ellenőrzés minden sort hibának jelez; jelentés nem íródik
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_j, ts='T1')
        ellen(kod == 1 and not os.path.exists(ut_j), 'a kitöltetlen besorolásra a fut() nem 1-es kód / jelentés íródott')
        h, _ = ellenoriz(adat, ut_b)
        ellen(len(h) == 2 * len(el), 'a kitöltetlen sablon hibáinak száma nem 2 × eltérés (osztály és indok): %d vs %d' % (len(h), 2 * len(el)))
        # besorolás-fájl nélkül: gépi összesítés
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], os.path.join(mappa, 'nincs.tsv'), ut_j, ts='T1')
        ellen(kod == 0 and os.path.exists(ut_j), 'besorolás nélkül a gépi jelentés nem íródott')
        with open(ut_j, encoding='utf-8') as f:
            md0 = f.read()
        ellen('kézi besorolás-fájl' in md0 and 'scope=' in md0 and 'forras=' in md0 and 'ts=T1' in md0 and '## 3.' not in md0,
              'a gépi jelentés fejléce/tartalma hibás')
        # kitöltött besorolás: osztályok felváltva, az indok nem üres -> teljes jelentés, determinisztikus
        sorok_k = []
        with open(ut_b, encoding='utf-8') as f:
            sorok_f = f.read().split('\n')
        for i, s in enumerate(sorok_f):
            if not s or s.startswith('#') or s.startswith('futas\t'):
                sorok_k.append(s)
                continue
            m = s.split('\t')
            m[9], m[11] = 'abc'[i % 3], 'teszt-indok %d' % i
            sorok_k.append('\t'.join(m))
        with open(ut_b, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_k))
        h, kezi = ellenoriz(adat, ut_b)
        ellen(h == [] and len(kezi) == len(el), 'a kitöltött besorolás hibát ad: %s' % h[:3])
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_j, ts='T1')
        with open(ut_j, encoding='utf-8') as f:
            md1 = f.read()
        with contextlib.redirect_stdout(io.StringIO()):
            fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_j, ts='T2')
        with open(ut_j, encoding='utf-8') as f:
            md2 = f.read()
        ellen(kod == 0 and '## 5.' in md1 and '## 4.' in md1 and md1.replace('ts=T1', 'ts=T2') == md2,
              'a teljes jelentés hibás / nem determinisztikus')
        # hibák: ismeretlen osztály, üres indok, hiányzó és többlet sor
        sorok_h = list(sorok_k)
        idx = [i for i, s in enumerate(sorok_h) if s and not s.startswith('#') and not s.startswith('futas\t')]
        m = sorok_h[idx[0]].split('\t')
        m[9] = 'x'
        sorok_h[idx[0]] = '\t'.join(m)
        m = sorok_h[idx[1]].split('\t')
        m[11] = ' '
        sorok_h[idx[1]] = '\t'.join(m)
        del sorok_h[idx[2]]
        m = sorok_h[idx[3]].split('\t')
        m[5] = str(int(m[5]) + 1000)
        sorok_h[idx[3]] = '\t'.join(m)
        ut_h = os.path.join(mappa, 'besorolas_hibas.tsv')
        with open(ut_h, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_h))
        h, _ = ellenoriz(adat, ut_h)
        ellen(any('érvénytelen vagy üres osztály' in x for x in h) and any('üres indok' in x for x in h)
              and any('besorolás nélküli' in x for x in h) and any('nincs gépi eltérés' in x for x in h),
              'az ellenőrzés nem fogta meg mind a négy hibatípust: %s' % h[:6])
        # az előzmény-oszlop: a valódi F3V2/F3V2B besorolások kulcsai (ha egyeznek) jelennek meg
        ez = elozmenyek()
        ellen(len(ez) > 0 and all(v.startswith(('F3V2:', 'F3V2B:')) for v in ez.values()), 'az előzmények nem a v2-es besorolásból valók')
        # hash-ellenőrzés: módosított arany -> SystemExit
        rossz = os.path.join(mappa, 'rossz.jsonl')
        shutil.copyfile(info['arany_ut'], rossz)
        with open(rossz, 'a', encoding='utf-8', newline='\n') as f:
            f.write('{}\n')
        shutil.copyfile(info['arany_sha'], os.path.join(mappa, 'rossz.sha256'))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fut(mappa, rossz, None, os.path.join(mappa, 'nincs.tsv'), os.path.join(mappa, 'x.md'))
            ellen(False, 'az eltérő hash-ű arany nem állította meg a diffet')
        except SystemExit as e:
            ellen('sha256' in str(e), 'az eltérő hash hibaüzenete hibás: %s' % e)
        # --lista nem dob
        with contextlib.redirect_stdout(io.StringIO()) as puf:
            lista(adat)
        ellen('ARANY:' in puf.getvalue() and 'hianyzo' in puf.getvalue() or 'tobblet' in puf.getvalue(), 'a --lista kimenete üres')
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    ellen(not os.path.exists(BESOROLAS_UT), 'az önteszt besorolás-fájlt hozott létre a repóban: %s' % BESOROLAS_UT)
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('c_diff_p3c önteszt rendben (független eltérés-számítás, # MANUAL sablon és felülírás-védelem, négy hibatípus, '
          'gépi és teljes jelentés, determinizmus, hash-ellenőrzés, régi kimenetek bájtazonossága)')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lista', action='store_true', help='az eltérések kontextussal')
    ap.add_argument('--sablon', action='store_true', help='a kézi besorolás váza (# MANUAL fejléccel; meglévőt nem ír felül)')
    ap.add_argument('--felulir', action='store_true', help='--sablon: a meglévő besorolás-fájl felülírása (szándékosan)')
    ap.add_argument('--arany', default=None, help='az arany jsonl-je (alap: a legfrissebb befagyasztott)')
    ap.add_argument('--arany-sha', default=None)
    ap.add_argument('--forras-dir', default=None)
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    if args.lista or args.sablon:
        adat, info = meres_p3c.betolt(args.forras_dir, args.arany, args.arany_sha)
        if args.lista:
            lista(adat)
            return 0
        sorok = sablon_ir(adat, BESOROLAS_UT, tokenek.generalas_ts(), args.felulir, info)
        print('a sablon megírva: %s (%d eltérés)' % (BESOROLAS_UT, len(sorok)))
        return 0
    return fut(args.forras_dir, args.arany, args.arany_sha)


if __name__ == '__main__':
    sys.exit(main())
