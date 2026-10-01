#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.42 / F21.71 — a (c) hibák újrabesorolásához a gépi diff: a Sonnet (SONNETV3) és az F3V3
(C, prompt_v3) eltérései az arany LEGFRISSEBB befagyasztott változatához (P3c, PD13), és az F3V3
(c) eseteinek összevetése a v2-es C-futások (F3V2, F3V2B) (c) eseteivel. Nincs API-hívás. A kézi
besorolás (a / b / c, a konvenció és a változást magyarázó konvenció) az Opus dolga („Opus-
besorolás, nem mérés”); ez a szkript a gépi részt, a kézi-besorolási vázat és az ellenőrzést adja.

Eltérés = a kapun átment aranyverseken az arany linkjei közül hiányzó (`hianyzo`) vagy a
futás többlet (`tobblet`) linkje, a meres_p3c.betolt linkhalmazaival (a meres_kizaras.tsv
tokenjei mind a két oldalról kimaradnak) — a c_diff_f3v2.elteresek változatlanul.

A besorolás-fájl (f21p/c_diff_p3c_besorolas.tsv, `# MANUAL` fejléc) oszlopai:
  gépi:  futas, igehely, reteg, irany, k_poz, e_poz, magyar, eredeti,
         statusz      — `elteres` (a futás eltérése a legfrissebb aranytól); csak az F3V3-nál
                        még: `megszunt` (a v2-es C-futások valamelyikének (c) esete, amely az
                        F3V3-nál nem eltérés) és `nem_merheto` (ugyanez, de a vers az F3V3-nál
                        kapuhibás);
         elozmeny_v2  — ugyanez a kulcs (vers, irány, magyar szó, eredeti szó) a v2-es futások
                        arany v2-höz mért eltérései között, a kézi osztályukkal: „F3V2:c, F3V2B:a”
                        (az F3V2B közös eltérései az F3V2 osztályát öröklik, F21.31; „?”: nincs
                        besorolás); az F3V3 soraira; üres: egyik v2-futásnál sem volt eltérés;
         arany_v2_v3  — `változott`, ha a magyar szó linkjei az arany v2 és v3 között eltérnek;
  kézi:  osztaly (a/b/c az `elteres` sorokon; a `megszunt`/`nem_merheto` sorokon üres),
         konvencio_vagy_jegyzetpont (a/b-nél kötelező), valtozas_konvencio (K1–K11 vagy `nincs`;
         kötelező: a megszűnt (c) esetnél — `megszunt`/`nem_merheto` sor, vagy `elteres` sor, amely
         a v2-ben (c) volt, most a/b —, és az új (c) esetnél — `elteres` sor, (c), a v2-ben nem (c)),
         indok (mindig kötelező). F21.76: az indokban az „arany-felülvizsgálatra jelölt” jelölés
         csak (c) `elteres` soron állhat (az arany döntése is vitatható, de a 6. táblázat zárt,
         PD10); a jelölt sor minden számban továbbra is (c), a jelentés külön listában adja.

Módok:
  --lista       az eltérések kontextussal (a kézi besoroláshoz)
  --sablon      a kézi besorolás váza `# MANUAL` fejléccel (a gépi oszlopok kitöltve, a kézi
                oszlopok üresek). Meglévő fájlt NEM ír felül (--felulir nélkül hiba);
                --hozzafuz: a meglévő fájlhoz csak a hiányzó gépi sorokat fűzi (pl. a Sonnet-adat
                megérkezése után a SONNETV3 sorai), a meglévő sorok változatlanok.
  --csak-c      csak az F3V3 (a SONNETV3 nem futott); minden mód ezzel kombinálható.
  --szigoru     a kézi besorolás szigorú ellenőrzése (a fenti kötelező mezők); hibánál 1-es kód.
  (alap)        ha nincs besorolás-fájl: gépi összesítés (a kézi rész nélkül); ha van: ellenőrzi
                (minden gépi sornak pontosan egy besorolása, érvényes osztály/konvenció, nem üres
                indok; --szigoru-val a kötelező mezők is), és hibamentesen a teljes jelentést írja;
                hibánál 1-es kilépési kód, a jelentés nem íródik.
Az osztályok jelentése a c_diff.py-ban: a = a Károli-szó/konvenció szerint védhető (a modell
a konvencióhoz képest tévedett), b = a jegyzet/arany alternatívája, c = valódi modellhiba.

Kimenet: naplok/F21P_C_diff_p3c.md (generált; fejléc: scope | forras | ts).
    python eszkozok/karoli_strong/c_diff_p3c.py [--csak-c] [--lista|--sablon [--felulir|--hozzafuz]] [--szigoru]
                                               [--arany <jsonl> [--arany-sha <f>]]
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
FUTASOK_C = [meres_p3c.C3]
OSZLOPOK = ['futas', 'igehely', 'reteg', 'irany', 'k_poz', 'e_poz', 'magyar', 'eredeti', 'statusz', 'elozmeny_v2',
            'arany_v2_v3', 'osztaly', 'konvencio_vagy_jegyzetpont', 'valtozas_konvencio', 'indok']
GEPI = OSZLOPOK[:11]
STATUSZOK = ('elteres', 'megszunt', 'nem_merheto')
KONVENCIOK = tuple('K%d' % i for i in range(1, 12)) + ('nincs',)
# a DT21 a–e döntés, amely az adott konvenciót a jegyzet v2-ben módosította (8.1–8.2); a d) csak a 2Móz 26:13
DT21 = {'K7': 'a', 'K3': 'b', 'K11': 'c', 'K4': 'e'}
V2_FUTASOK = (meres_p3c.C2, meres_p3c.C2B)
RET = meres.RETEGEK + [meres.OSSZES]
JELOLT = 'arany-felülvizsgálatra jelölt'      # F21.76: az indok-oszlop jelölése; csak (c) elteres soron


def dt21(konv, ig=None):
    if konv == 'K9' and ig == '2Móz 26:13':
        return 'd'
    return DT21.get(konv, '')


# ---------------------------------------------------------------------------
# gépi rész
# ---------------------------------------------------------------------------

def betolt(forras_dir=None, arany_ut=None, arany_sha=None, csak_c=False):
    """(adat, info, adat_v2). A csak-C mód a SONNETV3-at nem tölti be."""
    futasok = [meres_p3c.C3, meres_p3c.C2, meres_p3c.C2B] if csak_c else None
    adat, info = meres_p3c.betolt(forras_dir, arany_ut, arany_sha, futasok)
    adat2, _ = meres_p3c.arany_valtozat(adat)
    return adat, info, adat2


def elteresek(adat, futasok=FUTASOK):
    """{(futas, igehely, irany, k, e): reteg} a megadott futásokra (a c_diff_f3v2.elteresek)."""
    ki = {}
    for f in futasok:
        for (ig, irany, k, e), ret in cf.elteresek(adat, f, adat.arany_linkek).items():
            ki[(f, ig, irany, k, e)] = ret
    return ki


def v2_osztalyok(adat2):
    """{futás: {(ig, irany, k, e): osztály}} az F3V2 és az F3V2B arany v2-höz mért eltéréseire, a v2-es
    kézi besorolásokból (F3V2: c_diff_f3v2_osszevetes.tsv; F3V2B: c_diff_f3v2b_besorolas.tsv, a közös
    eltérés az F3V2 osztályát örökli). Hiányzó besorolás: '?'."""
    try:
        o2 = c_diff_f3v2b.f3v2_osztaly()
    except (OSError, SystemExit):
        o2 = {}
    ob = {}
    if os.path.exists(c_diff_f3v2b.BESOROLAS_UT):
        for r in c_diff._tsv(c_diff_f3v2b.BESOROLAS_UT, c_diff_f3v2b.OSZLOPOK):
            ob[(r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))] = r['osztaly']
    ki = {}
    for f in V2_FUTASOK:
        el = cf.elteresek(adat2, f, adat2.arany_linkek)
        ki[f] = {}
        for kk in el:
            if f == meres_p3c.C2:
                ki[f][kk] = o2.get(kk, '?')
            else:
                ki[f][kk] = ob.get(kk) or o2.get(kk, '?')
    return ki


def elozmeny(v2o, kk):
    return ', '.join('%s:%s' % (f, v2o[f][kk]) for f in V2_FUTASOK if kk in v2o.get(f, {}))


def v2_c_kulcsok(v2o):
    return {kk for f in V2_FUTASOK for kk, o in v2o.get(f, {}).items() if o == 'c'}


def arany_valtozott(adat, adat2, ig, k):
    if ig not in adat.arany or ig not in adat2.arany:
        return ''
    a = {x for x in adat.arany_linkek(ig) if x[0] == k}
    b = {x for x in adat2.arany_linkek(ig) if x[0] == k}
    return 'változott' if a != b else ''


def sorrend(adat, futasok, kulcsok):
    return sorted(kulcsok, key=lambda x: (futasok.index(x[0]), adat.versek.index(x[1]), x[2], x[3], x[4]))


def gepi_sorok(adat, adat2, futasok=FUTASOK):
    """{(futas, ig, irany, k, e): [gépi mezők]} — az eltérések és (az F3V3-nál) a megszűnt/nem mérhető
    v2-es (c) esetek. Determinisztikus sorrendben (dict)."""
    el = elteresek(adat, futasok)
    v2o = v2_osztalyok(adat2)
    c3 = meres_p3c.C3
    kulcsok = {k: 'elteres' for k in el}
    if c3 in futasok:
        for kk in v2_c_kulcsok(v2o):
            k = (c3,) + kk
            if k in el:
                continue
            kulcsok[k] = 'nem_merheto' if not adat.ok(c3, kk[0]) else 'megszunt'
    ki = {}
    for k in sorrend(adat, futasok, kulcsok):
        f, ig, irany, kp, ep = k
        magyar = c_diff._magyar(adat, ig, kp).split(' ', 1)[1]
        eredeti = c_diff._eredeti(adat, ig, ep)
        elo = elozmeny(v2o, (ig, irany, kp, ep)) if f == c3 else ''
        ki[k] = [f, ig, adat.reteg[ig], irany, str(kp), str(ep), magyar, eredeti, kulcsok[k], elo,
                 arany_valtozott(adat, adat2, ig, kp)]
    return ki


def _fejlec_manual(verzio, n, ts, futasok):
    return ('# MANUAL: scope=f21p P3c (c)-újrabesorolás: %s eltérései az arany %s-höz, és az F3V3 összevetése a v2-es '
            'C-futások (F3V2, F3V2B) (c) eseteivel (%d sor) | forras=f21p/valaszok/{%s}.jsonl, az arany legfrissebb befagyasztott '
            'változata, f21p/arany_opus_v2.jsonl, f21p/c_diff_f3v2_osszevetes.tsv, f21p/c_diff_f3v2b_besorolas.tsv, '
            'eszkozok/karoli_strong/c_diff_p3c.py --sablon | ts=%s (a sablon gépi váza; az osztaly, konvencio_vagy_jegyzetpont, '
            'valtozas_konvencio és indok oszlop KÉZI; a besorolás idejét a besoroló frissíti) | manual (Opus-besorolás, nem mérés) | '
            'a gépi oszlopok (futas..arany_v2_v3) nem kézzel szerkesztendők\n'
            % ('+'.join(futasok), verzio, n, ','.join(futasok + list(V2_FUTASOK)), ts))


def sablon_ir(adat, adat2, ut, ts, felulir=False, arany_info=None, futasok=FUTASOK, hozzafuz=False):
    """A kézi besorolás váza. Meglévő fájlt nem ír felül (felulir/hozzafuz nélkül SystemExit); hozzafuz:
    csak a hiányzó gépi sorokat fűzi a meglévő fájl végére."""
    gs = gepi_sorok(adat, adat2, futasok)
    if os.path.exists(ut) and hozzafuz:
        meglevo = {_kulcs(r) for r in beolvas(ut)}
        uj = [v for k, v in gs.items() if k not in meglevo]
        with open(ut, 'a', encoding='utf-8', newline='\n') as f:
            for s in uj:
                assert all('\t' not in x for x in s)
                f.write('\t'.join(s + ['', '', '', '']) + '\n')
        return uj
    if os.path.exists(ut) and not felulir:
        raise SystemExit('HIBA: %s már létezik (a kézi besorolás nem íródik felül; --felulir csak szándékosan, '
                         '--hozzafuz a hiányzó sorokhoz)' % ut)
    verzio = arany_info['verzio'] if arany_info else '?'
    sorok = list(gs.values())
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(_fejlec_manual(verzio, len(sorok), ts, futasok))
        f.write('\t'.join(OSZLOPOK) + '\n')
        for s in sorok:
            assert all('\t' not in x for x in s)
            f.write('\t'.join(s + ['', '', '', '']) + '\n')
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


def _kulcs(r):
    return (r['futas'], r['igehely'], r['irany'], int(r['k_poz']), int(r['e_poz']))


def valtozas_kell(r):
    """A sor megszűnt (c) vagy új (c) eset-e (a változás-konvenció kötelező)."""
    volt_c = ':c' in r['elozmeny_v2']
    if r['statusz'] in ('megszunt', 'nem_merheto'):
        return True
    if r['futas'] != meres_p3c.C3:
        return False
    return (r['osztaly'] == 'c') != volt_c


def ellenoriz(adat, adat2, ut, futasok=FUTASOK, szigoru=False):
    """(hibák, {kulcs: sor}): minden gépi sornak pontosan egy besorolása, a gépi oszlopok egyeznek,
    érvényes osztály/konvenció, nem üres indok; szigoru: a kötelező mezők is. A más futások sorai
    (pl. a csak-C módban a SONNETV3 későbbi sorai) kimaradnak."""
    gs = gepi_sorok(adat, adat2, futasok)
    hibak = []
    kezi = {}
    for r in beolvas(ut):
        if r['futas'] not in futasok:
            continue
        k = _kulcs(r)
        if k in kezi:
            hibak.append('kétszer besorolt sor: %s' % (k,))
        kezi[k] = r
        if k in gs and [r[c] for c in GEPI] != gs[k]:
            hibak.append('a gépi oszlopok eltérnek a gépi számítástól: %s' % (k,))
        if r['statusz'] == 'elteres':
            if r['osztaly'] not in c_diff.OSZTALYOK:
                hibak.append('érvénytelen vagy üres osztály (%s kell): %s' % ('/'.join(c_diff.OSZTALYOK), k))
        elif r['osztaly']:
            hibak.append('a %s sornak nincs osztálya (üres kell): %s' % (r['statusz'], k))
        if not r['indok'].strip():
            hibak.append('üres indok: %s' % (k,))
        if JELOLT in r['indok'] and not (r['statusz'] == 'elteres' and r['osztaly'] == 'c'):
            hibak.append('a(z) „%s” jelölés csak (c) eltérés-soron állhat: %s' % (JELOLT, k))
        if r['valtozas_konvencio'] and r['valtozas_konvencio'] not in KONVENCIOK:
            hibak.append('érvénytelen változás-konvenció (K1–K11 vagy nincs): %s' % (k,))
        if szigoru:
            if r['osztaly'] in ('a', 'b') and not r['konvencio_vagy_jegyzetpont'].strip():
                hibak.append('(a)/(b) konvenció/jegyzetpont nélkül: %s' % (k,))
            if valtozas_kell(r) and not r['valtozas_konvencio']:
                hibak.append('megszűnt/új (c) eset változás-konvenció nélkül: %s' % (k,))
    for k in sorrend(adat, futasok, set(gs) - set(kezi)):
        hibak.append('besorolás nélküli gépi sor: %s' % (k,))
    for k in sorted(set(kezi) - set(gs), key=str):
        hibak.append('besorolás, amelyhez nincs gépi sor: %s' % (k,))
    return hibak, kezi


def lista(adat, adat2, futasok=FUTASOK):
    gs = gepi_sorok(adat, adat2, futasok)
    aktualis = None
    for k, s in gs.items():
        f, ig, irany, kp, ep = k
        if (f, ig) != aktualis:
            aktualis = (f, ig)
            print('\n%s [%s] %s' % (ig, adat.reteg[ig], f))
            if adat.ok(f, ig):
                print('    %s: %s' % (f, json.dumps(adat.futas[f][ig]['obj']['parok'])))
            print('    ARANY: %s' % json.dumps(adat.arany[ig]['parok']))
        print('  %s %s %s -> %s%s%s' % (s[8], irany, c_diff._magyar(adat, ig, kp), c_diff._eredeti(adat, ig, ep),
                                        ('   [előzmény: %s]' % s[9]) if s[9] else '', ('   [arany v2→v3: %s]' % s[10]) if s[10] else ''))


# ---------------------------------------------------------------------------
# jelentés
# ---------------------------------------------------------------------------

def fejlec(info, ts, van_kezi, futasok):
    return ('GENERÁLT: eszkozok/karoli_strong/c_diff_p3c.py%s | scope=%s (prompt_v3) a kapun átment aranyversekre, arany %s '
            '(%d vers, sha256 %s); az F3V3 (c) esetei a v2-es C-futások (F3V2, F3V2B; arany v2) (c) eseteivel összevetve | '
            'forras=f21p/valaszok/{%s}.jsonl, %s (sha256 ellenőrizve), f21p/arany_opus_v2.jsonl, f21p/meres_kizaras.tsv, '
            'f21p/c_diff_f3v2_osszevetes.tsv, f21p/c_diff_f3v2b_besorolas.tsv%s | ts=%s (a generálás ideje; ismételt futáskor '
            'csak ez a sor tér el) | kézzel szerkeszteni tilos'
            % (' --csak-c' if futasok == FUTASOK_C else '', ' és '.join(futasok), info['verzio'], info['aranyversek'],
               info['sha256'][:16], ','.join(futasok + list(V2_FUTASOK)), os.path.basename(info['jsonl']),
               ', f21p/c_diff_p3c_besorolas.tsv (MANUAL)' if van_kezi else '', ts))


# jellemző példák (futás, vers, irány, k, e) — kézi válogatás a besorolás után; a (c) esetek mind listázódnak
PELDAK = [
    ('F3V3', 'Péld 23:19', 'tobblet', 4, 4),       # megszűnt, K3 (DT21 b)
    ('F3V3', 'Péld 23:19', 'hianyzo', 3, 4),       # megszűnt, K4 (DT21 e)
    ('F3V3', '2Móz 21:26', 'tobblet', 9, 13),      # megszűnt, K4 (DT21 e)
    ('F3V3', '2Móz 21:26', 'hianyzo', 8, 13),      # átsorolt c -> a, K4
    ('F3V3', 'Mt 5:34', 'tobblet', 3, 3),          # megszűnt, K3
    ('F3V3', 'Mt 27:18', 'tobblet', 2, 1),         # megszűnt, K7 (DT21 a)
    ('F3V3', 'Mk 2:23', 'tobblet', 3, 2),          # megszűnt, K7
    ('F3V3', 'Jak 3:1', 'tobblet', 7, 8),          # megszűnt, K11 (DT21 c)
    ('F3V3', 'Mt 21:4', 'hianyzo', 3, 5),          # megszűnt az arany v3 változásával, K11
    ('F3V3', 'Jób 33:13', 'tobblet', 4, 5),        # az arany v3 hozta létre, (a) K11
    ('F3V3', '2Móz 25:40', 'hianyzo', 12, 9),      # új (c)
    ('F3V3', 'Jer 51:3', 'tobblet', 8, 9),         # új (c)
    ('F3V3', 'Ez 22:25', 'hianyzo', 7, 7),         # új (c), határeset
    ('F3V3', '1Pét 4:11', 'tobblet', 7, 3),        # maradt (c)
    ('F3V3', 'Jer 51:3', 'hianyzo', 2, 1),         # (b) 3. szakasz
]


def _sor_md(x):
    return '| %s | %s | %s | %s %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        meres_p3c.NEVEK[x['futas']], x['igehely'], x['irany'], x['k_poz'], x['magyar'], x['eredeti'], x['statusz'],
        x['elozmeny_v2'] or '—', x['arany_v2_v3'] or '—', x['osztaly'] or '—', x['konvencio_vagy_jegyzetpont'] or '—',
        ('%s%s' % (x['valtozas_konvencio'], (' (DT21 %s)' % dt21(x['valtozas_konvencio'], x['igehely']))
                   if dt21(x['valtozas_konvencio'], x['igehely']) else '')) if x['valtozas_konvencio'] else '—', x['indok'])


SOR_FEJ = ['| futás | vers | irány | magyar szó | eredeti szó | állapot | előzmény (v2) | arany v2→v3 | osztály | konvenció / jegyzetpont | '
           'változás-konvenció | indok (kézi) |', '|---|---|---|---|---|---|---|---|---|---|---|---|']


def _v2_tabla(adat2):
    """A v2-es C-futások (c) esetei rétegenként (az arany v2-höz, a v2-es kézi besorolásból)."""
    v2o = v2_osztalyok(adat2)
    ki = {}
    for f in V2_FUTASOK:
        for r in RET:
            ks = [kk for kk in v2o[f] if r == meres.OSSZES or adat2.reteg[kk[0]] == r]
            ki[(f, r)] = {o: sum(1 for kk in ks if v2o[f][kk] == o) for o in ('a', 'b', 'c', '?')}
            ki[(f, r)]['n'] = len(ks)
    return ki, v2o


def jelentes(adat, adat2, info, kezi, ut, ts, futasok=FUTASOK):
    gs = gepi_sorok(adat, adat2, futasok)
    v2t, v2o = _v2_tabla(adat2)
    c3 = meres_p3c.C3
    ki = ['# F21P_C_diff_p3c.md — a (c) hibák újrabesorolása: %s eltérései az arany %s-höz, a v2-es C-futásokkal összevetve'
          % (' és '.join(meres_p3c.NEVEK[f] for f in futasok), info['verzio']), '',
          '<!-- %s -->' % fejlec(info, ts, kezi is not None, futasok), '',
          'Gépi diff: a kapun átment aranyverseken az arany linkjeiből hiányzó és a futás többlet linkjei; az állapot (eltérés / '
          'megszűnt / nem mérhető), az előzmény (a v2-es C-futások arany v2-höz mért eltérései és azok v2-es kézi osztálya) és az '
          'arany v2 → v3 változása gépi. **Az osztályok (a / b / c), a konvenció és a változást magyarázó konvenció kézi '
          'besorolás: Opus-besorolás, nem mérés.** A mért értékek (pontosság, lefedettség, küszöb-viszony) a '
          'naplok/F21P_meres_p3c_c.md-ben; a küszöb szempontjából csak azok számítanak.' + ('' if kezi is not None else
          ' A kézi besorolás-fájl (f21p/c_diff_p3c_besorolas.tsv) még nincs meg: ez a jelentés csak a gépi részt tartalmazza.'), '']
    if futasok == FUTASOK_C:
        ki += ['A SONNETV3 még nem futott; a Sonnet eltéréseinek besorolása a Sonnet-adat megérkezése után (--sablon --hozzafuz, '
               '--csak-c nélkül).', '']
    ki += ['## 1. Eltérések futásonként és rétegenként (gépi)', '',
           '| futás | réteg | aranyversek (kapun átment) | hiányzó | többlet | eltérő versek |', '|---|---|---|---|---|---|']
    el = {k: v for k, v in gs.items() if v[8] == 'elteres'}
    for f in futasok:
        for r in RET:
            vs = [ig for ig in adat.versek if ig in adat.arany and adat.ok(f, ig) and (r == meres.OSSZES or adat.reteg[ig] == r)]
            ks = [k for k in el if k[0] == f and (r == meres.OSSZES or adat.reteg[k[1]] == r)]
            ki.append('| %s | %s | %d | %d | %d | %d |' % (meres_p3c.NEVEK[f], r, len(vs), sum(1 for k in ks if k[2] == 'hianyzo'),
                                                        sum(1 for k in ks if k[2] == 'tobblet'), len({k[1] for k in ks})))
    for f in V2_FUTASOK:
        for r in RET:
            ks = [kk for kk in v2o[f] if r == meres.OSSZES or adat2.reteg[kk[0]] == r]
            ki.append('| %s × arany v2 | %s | — | %d | %d | %d |' % (meres_p3c.NEVEK[f], r, sum(1 for k in ks if k[1] == 'hianyzo'),
                                                                   sum(1 for k in ks if k[1] == 'tobblet'), len({k[0] for k in ks})))
    if meres_p3c.SONNET in futasok:
        ki += ['', '### A Sonnet és az F3V3 közös és eltérő eltérései (gépi)', '',
               '| réteg | csak a Sonnet | csak az F3V3 | közös (mindkettő ugyanazt) |', '|---|---|---|---|']
        s_k = {k[1:] for k in el if k[0] == meres_p3c.SONNET}
        c_k = {k[1:] for k in el if k[0] == c3}
        for r in RET:
            def n(hz):
                return sum(1 for k in hz if r == meres.OSSZES or adat.reteg[k[0]] == r)
            ki.append('| %s | %d | %d | %d |' % (r, n(s_k - c_k), n(c_k - s_k), n(s_k & c_k)))
    ki += ['', '### Az F3V3 sorainak állapota rétegenként (gépi)', '',
           '| réteg | eltérés | ebből: a v2-ben is eltérés | ebből: a v2-ben (c) | megszűnt v2 (c) | nem mérhető v2 (c) | az arany v2→v3-ban változott szó |',
           '|---|---|---|---|---|---|---|']
    for r in RET:
        rs = [v for k, v in gs.items() if k[0] == c3 and (r == meres.OSSZES or v[2] == r)]
        ki.append('| %s | %d | %d | %d | %d | %d | %d |' % (
            r, sum(1 for v in rs if v[8] == 'elteres'), sum(1 for v in rs if v[8] == 'elteres' and v[9]),
            sum(1 for v in rs if v[8] == 'elteres' and ':c' in v[9]), sum(1 for v in rs if v[8] == 'megszunt'),
            sum(1 for v in rs if v[8] == 'nem_merheto'), sum(1 for v in rs if v[10])))
    if kezi is None:
        ki.append('')
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(ki) + '\n')
        return
    ki += zaro_szakasz(adat, adat2, kezi, futasok, v2t, v2o)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def _van(r, ret):
    return ret == meres.OSSZES or r == ret


def lefedettseg_jeloles(adat, sorok_c3):
    """F21.76 (1): a 95%-os küszöbön kívüli mért F3V3-lefedettség jelölése rétegenként (nincs további teendő),
    a hiányzó linkek K4 (a) számával (Opus-besorolás, nem mérés)."""
    ki = []
    for r in meres.RETEGEK:
        t, _, g, _ = meres_p3c._pl(adat, meres_p3c.C3, r)
        if not g or t / g >= meres_p3c.KUSZOB_LEF:
            continue
        hi = [x for x in sorok_c3.values() if x['statusz'] == 'elteres' and x['irany'] == 'hianyzo' and x['reteg'] == r]
        k4a = [x for x in hi if x['osztaly'] == 'a' and x['konvencio_vagy_jegyzetpont'].startswith('K4')]
        ki.append('- az %s lefedettsége a 95%%-os küszöbön kívül (%s%%); a hiányzó %d link közül %d K4-eltérés (a). (A mért érték: '
                  'naplok/F21P_meres_p3c_c.md; a K4-szám Opus-besorolás, nem mérés; a besorolás hiányzó eltérés-sorai: %d, %s.)'
                  % (r, ('%.1f' % (100.0 * t / g)).replace('.', ','), g - t, len(k4a), len(hi), 'EGYEZIK' if len(hi) == g - t else 'ELTÉR'))
    return (['', 'Jelölés (F21.76; nincs további teendő):', ''] + ki) if ki else []


def felulvizsgalat_szakasz(adat, sorok_c3, allapot):
    """F21.76 (3): az „arany-felülvizsgálatra jelölt” (c) esetek külön listája; a számokban továbbra is (c)."""
    c_sorok = [x for x in sorok_c3.values() if x['statusz'] == 'elteres' and x['osztaly'] == 'c']
    jc = [x for k, x in sorted(sorok_c3.items(), key=lambda kv_: (adat.versek.index(kv_[0][1]),) + kv_[0][2:]) if JELOLT in x['indok']]
    ki = ['', '### Arany-felülvizsgálatra jelölt (c) esetek (Opus-besorolás, nem mérés)', '',
          'Az F3V3 %d (c) esetéből %d „%s” (az arany döntése is vitatható, de a 6. táblázat zárt, PD10). A korrigált számban (fent) '
          'és minden táblában továbbra is (c)-nek számít.' % (len(c_sorok), len(jc), JELOLT), '',
          '| réteg | F3V3 (c) | ebből arany-felülvizsgálatra jelölt | ebből: maradt | ebből: új (c) |', '|---|---|---|---|---|']
    for r in RET:
        cs = [x for x in c_sorok if _van(x['reteg'], r)]
        js = [x for x in jc if _van(x['reteg'], r)]
        ki.append('| %s | %d | %d | %d | %d |' % (r, len(cs), len(js), sum(1 for x in js if allapot(x) == 'maradt'),
                                                sum(1 for x in js if allapot(x) == 'uj')))
    ki += [''] + SOR_FEJ + [_sor_md(x) for x in jc]
    return ki


def zaro_szakasz(adat, adat2, kezi, futasok, v2t, v2o):
    c3 = meres_p3c.C3
    ki = ['', '## 2. A kézi besorolás (a / b / c) rétegenként, a v2-es C-futásokkal egymás mellett (Opus-besorolás, nem mérés)', '',
          'Az F3V3 az arany v3-hoz, az F3V2 és az F3V2B a saját aranyához (v2) mérve, a v2-es kézi besorolással (F21.16, F21.31).', '',
          '| réteg | F3V2 a | F3V2 b | F3V2 c | F3V2B a | F3V2B b | F3V2B c | %s |' % ' | '.join(
              '%s %s' % (meres_p3c.NEVEK[f], o) for f in futasok for o in ('a', 'b', 'c')),
          '|---|' + '---|' * (6 + 3 * len(futasok))]
    for r in RET:
        cel = [str(v2t[(f, r)][o]) for f in V2_FUTASOK for o in ('a', 'b', 'c')]
        for f in futasok:
            rs = [x for k, x in kezi.items() if k[0] == f and x['statusz'] == 'elteres' and _van(x['reteg'], r)]
            cel += [str(sum(1 for x in rs if x['osztaly'] == o)) for o in ('a', 'b', 'c')]
        ki.append('| %s | %s |' % (r, ' | '.join(cel)))
    nkerdo = sum(v2t[(f, meres.OSSZES)]['?'] for f in V2_FUTASOK)
    if nkerdo:
        ki += ['', 'Figyelem: %d v2-es eltérésnek nincs v2-es kézi osztálya („?”).' % nkerdo]
    # a (c) esetek: megszűnt / maradt / új, rétegenként
    sorok_c3 = {k: x for k, x in kezi.items() if k[0] == c3}

    def allapot(x):
        volt = ':c' in x['elozmeny_v2']
        if x['statusz'] in ('megszunt', 'nem_merheto'):
            return 'megszunt' if x['statusz'] == 'megszunt' else 'nem_merheto'
        if volt and x['osztaly'] == 'c':
            return 'maradt'
        if volt:
            return 'atsorolt'            # a v2-ben (c) volt, most is eltérés, de (a)/(b)
        if x['osztaly'] == 'c':
            return 'uj'
        return ''
    if c3 in futasok:
        ki += ['', '## 3. Az F3V3 (c) esetei a v2-es C-futások (c) eseteihez képest (Opus-besorolás, nem mérés)', '',
               'v2 (c) = az F3V2 vagy az F3V2B (c) esete (kulcs: vers, irány, magyar szó, eredeti szó). **maradt** = az F3V3-nál is '
               'eltérés és (c); **megszűnt** = az F3V3-nál nem eltérés; **átsorolt** = az F3V3-nál is eltérés, de a jegyzet v2 / arany '
               'v3 szerint (a) vagy (b); **új** = az F3V3 (c) esete, amely a v2-ben nem volt (c). Az „arany v2→v3: változott” jelölésű '
               'sorokban a változást (részben) az arany változása okozza, nem a modell.', '',
               '| réteg | v2 (c) összesen | F3V2 (c) | F3V2B (c) | F3V3 (c) | maradt | megszűnt | ebből mindkét v2-ben (c) | átsorolt (a/b) | '
               'nem mérhető | új (c) |',
               '|---|---|---|---|---|---|---|---|---|---|---|']
        v2c = v2_c_kulcsok(v2o)
        for r in RET:
            rs = [x for x in sorok_c3.values() if _van(x['reteg'], r)]
            al = [allapot(x) for x in rs]
            ki.append('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |' % (
                r, sum(1 for kk in v2c if _van(adat2.reteg[kk[0]], r)), v2t[(V2_FUTASOK[0], r)]['c'], v2t[(V2_FUTASOK[1], r)]['c'],
                sum(1 for x in rs if x['statusz'] == 'elteres' and x['osztaly'] == 'c'), al.count('maradt'), al.count('megszunt'),
                sum(1 for x in rs if allapot(x) == 'megszunt' and x['elozmeny_v2'].count(':c') == 2),
                al.count('atsorolt'), al.count('nem_merheto'), al.count('uj')))
        ki += ['', 'A „megszűnt” eset, amely csak az egyik v2-futásban volt (c), a futásközi ingadozással is összefér (a két v2-futás '
               'azonos prompttal sem adta ugyanazt); a mindkét v2-futásban (c) eset megszűnése erősebb jel.']
        # korrigált értékek, a v2-es futásokkal egymás mellett
        ki += ['', '### Korrigált pontosság és lefedettség — Opus-besorolás, nem mérés', '',
               'Az (a) és (b) eltérést nem-hibának véve. Az F3V3 az arany v3-hoz, az F3V2 és az F3V2B az arany v2-höz (a saját v2-es kézi '
               'besorolásukkal). A küszöb szempontjából csak a mért érték számít (PD10).', '',
               '| réteg | mérőszám | F3V2 × v2 mért | F3V2 × v2 korrigált (Opus, nem mérés) | F3V2B × v2 mért | F3V2B × v2 korrigált (Opus, nem mérés) '
               '| F3V3 × v3 mért | F3V3 × v3 korrigált (Opus-besorolás, nem mérés) |', '|---|---|---|---|---|---|---|---|']
        for r in RET:
            cel = {'pontosság': [], 'lefedettség': []}
            for f in V2_FUTASOK:
                t, c, g, _ = meres_p3c._pl(adat2, f, r)
                ab = [kk for kk, o in v2o[f].items() if o in ('a', 'b') and _van(adat2.reteg[kk[0]], r)]
                tb = sum(1 for kk in ab if kk[1] == 'tobblet')
                hb = sum(1 for kk in ab if kk[1] == 'hianyzo')
                cel['pontosság'] += [meres_p3c._pct(t, c), meres_p3c._pct(t + tb, c)]
                cel['lefedettség'] += [meres_p3c._pct(t, g), meres_p3c._pct(t + hb, g)]
            t, c, g, _ = meres_p3c._pl(adat, c3, r)
            ab = [x for x in sorok_c3.values() if x['statusz'] == 'elteres' and x['osztaly'] in ('a', 'b') and _van(x['reteg'], r)]
            tb = sum(1 for x in ab if x['irany'] == 'tobblet')
            hb = sum(1 for x in ab if x['irany'] == 'hianyzo')
            cel['pontosság'] += [meres_p3c._pct(t, c), meres_p3c._pct(t + tb, c)]
            cel['lefedettség'] += [meres_p3c._pct(t, g), meres_p3c._pct(t + hb, g)]
            for m in ('pontosság', 'lefedettség'):
                ki.append('| %s | %s | %s |' % (r, m, ' | '.join(cel[m])))
        ki += lefedettseg_jeloles(adat, sorok_c3)
        ki += felulvizsgalat_szakasz(adat, sorok_c3, allapot)
        # a változás konvenciónként
        hatas = [('segített (v2 (c) megszűnt)', 'megszunt'), ('segített (v2 (c) átsorolva a/b-be)', 'atsorolt'),
                 ('nem mérhető', 'nem_merheto'), ('nem segített (v2 (c) maradt)', 'maradt'), ('ártott / új (c)', 'uj')]
        ki += ['', '## 4. A változás konvenciónként (kézi: a valtozas_konvencio oszlop)', '',
               'segített = a v2 (c) eset megszűnt (vagy a jegyzet v2 szerint már nem hiba), és a megnevezett konvenció (prompt-szabály '
               'vagy az arany v3 változása) magyarázza; nem segített = a v2 (c) eset maradt (a változás-konvenció itt a rá vonatkozó '
               'szabály, ha van); ártott / új = új (c) eset. „nincs” = nem konvenció, modell-ingadozás. A DT21-oszlop: a jegyzet v2-ben '
               'a DT21 melyik a–e döntése módosította a konvenciót (a = K7 szűkítés, b = K3, c = K11, d = 2Móz 26:13 *is*, e = K4 '
               'pontosítás). Zárójelben: ebből az arany v2 → v3 változásához kötött sor.', '',
               '| változás-konvenció | DT21 | ' + ' | '.join(h for h, _ in hatas) + ' |', '|---|---|' + '---|' * len(hatas)]
        konvok = sorted({x['valtozas_konvencio'] for x in sorok_c3.values() if x['valtozas_konvencio']},
                        key=lambda v: (v == 'nincs', int(v[1:]) if v != 'nincs' else 0))
        for kv in konvok:
            cel = []
            for _, st in hatas:
                rs = [x for x in sorok_c3.values() if allapot(x) == st and x['valtozas_konvencio'] == kv]
                ar = sum(1 for x in rs if x['arany_v2_v3'])
                cel.append('%d%s' % (len(rs), (' (%d)' % ar) if ar else ''))
            dts = sorted({dt21(kv, x['igehely']) for x in sorok_c3.values() if x['valtozas_konvencio'] == kv} - {''})
            ki.append('| %s | %s | %s |' % (kv, ', '.join(dts) or '—', ' | '.join(cel)))
        ki += ['', '### Az a–e szabályok (DT21) hatása összesítve', '',
               '| DT21 | konvenció | segített (megszűnt + átsorolt) | nem segített (maradt) | ártott (új c) |', '|---|---|---|---|---|']
        for betu, kv in (('a', 'K7'), ('b', 'K3'), ('c', 'K11'), ('d', 'K9 (2Móz 26:13)'), ('e', 'K4')):
            def n(sts):
                return sum(1 for x in sorok_c3.values() if allapot(x) in sts and dt21(x['valtozas_konvencio'], x['igehely']) == betu)
            ki.append('| %s | %s | %d | %d | %d |' % (betu, kv, n(('megszunt', 'atsorolt')), n(('maradt',)), n(('uj',))))
        ki += ['', '## 5. Jellemző példák (kézi válogatás)', ''] + SOR_FEJ
        for k in PELDAK:
            if k in kezi:
                ki.append(_sor_md(kezi[k]))
        for cim, st in (('Minden új (c) eset', ('uj',)), ('Minden megszűnt v2 (c) eset (az F3V3-nál nem eltérés)', ('megszunt', 'nem_merheto')),
                        ('Minden átsorolt v2 (c) eset (az F3V3-nál is eltérés, de a/b)', ('atsorolt',)), ('Minden maradt (c) eset', ('maradt',))):
            ki += ['', '## %s' % cim, ''] + SOR_FEJ
            ki += [_sor_md(x) for k, x in sorted(sorok_c3.items(), key=lambda kv_: (adat.versek.index(kv_[0][1]),) + kv_[0][2:])
                   if allapot(x) in st]
    ki += ['', '## 6. Minden sor (gépi állapot, kézi besorolás)', ''] + SOR_FEJ
    for k in sorrend(adat, futasok, kezi):
        ki.append(_sor_md(kezi[k]))
    ki.append('')
    return ki


def fut(forras_dir=None, arany_ut=None, arany_sha=None, besorolas_ut=None, jelentes_ut=None, ts=None, csak_c=False, szigoru=False):
    futasok = FUTASOK_C if csak_c else FUTASOK
    adat, info, adat2 = betolt(forras_dir, arany_ut, arany_sha, csak_c)
    besorolas_ut = besorolas_ut or BESOROLAS_UT
    kezi = None
    if os.path.exists(besorolas_ut):
        hibak, kezi = ellenoriz(adat, adat2, besorolas_ut, futasok, szigoru)
        if hibak:
            print('HIBA (a jelentés nem íródott): %d hiba a kézi besorolásban%s:' % (len(hibak), ' (szigorú)' if szigoru else ''))
            for h in hibak[:50]:
                print('  ' + h)
            return 1
    elif szigoru:
        print('HIBA: nincs kézi besorolás-fájl (%s); a szigorú ellenőrzés nem futhat' % besorolas_ut)
        return 1
    jelentes(adat, adat2, info, kezi, jelentes_ut or JELENTES_UT, ts or tokenek.generalas_ts(), futasok)
    gs = gepi_sorok(adat, adat2, futasok)
    print('%s; kézi besorolás: %s%s -> %s' % (
        ', '.join('%s: %d eltérés' % (f, sum(1 for k, v in gs.items() if k[0] == f and v[8] == 'elteres')) for f in futasok)
        + ', megszűnt/nem mérhető v2 (c): %d' % sum(1 for v in gs.values() if v[8] != 'elteres'),
        'teljes' if kezi is not None else 'még nincs', ' (szigorú ellenőrzés: rendben)' if szigoru and kezi is not None else '',
        jelentes_ut or JELENTES_UT))
    return 0


# ---------------------------------------------------------------------------
# önteszt
# ---------------------------------------------------------------------------

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
    I_OSZT, I_KONV, I_VALT, I_IND = (OSZLOPOK.index(c) for c in ('osztaly', 'konvencio_vagy_jegyzetpont', 'valtozas_konvencio', 'indok'))
    mappa = p3c_mock.ideiglenes('f21p_onteszt_c_diff_p3c_')
    try:
        info = p3c_mock.general(mappa)
        adat, ainfo, adat2 = betolt(mappa, info['arany_ut'], info['arany_sha'])
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
        ellen(not any(k[1] == info['c_hiba'] for k in el if k[0] == meres_p3c.C3)
              and not any(k[1] == info['sonnet_hiba'] for k in el if k[0] == meres_p3c.SONNET),
              'kapuhibás vers eltérései is szerepelnek')
        # a gépi sorok: minden eltérés `elteres`; a többi sor F3V3-as, v2-ben (c) kulcs, nem eltérés
        gs = gepi_sorok(adat, adat2)
        ellen({k for k, v in gs.items() if v[8] == 'elteres'} == set(el), 'az elteres sorok nem az eltérések')
        v2c = v2_c_kulcsok(v2_osztalyok(adat2))
        ellen(all(k[0] == meres_p3c.C3 and k[1:] in v2c and k not in el for k, v in gs.items() if v[8] != 'elteres'),
              'a megszűnt/nem mérhető sorok nem a v2 (c) kulcsai közül valók')
        ellen(all(len(v) == len(GEPI) for v in gs.values()), 'a gépi sorok mezőszáma hibás')
        # sablon
        ut_b = os.path.join(mappa, 'besorolas.tsv')
        ut_j = os.path.join(mappa, 'jelentes.md')
        sorok = sablon_ir(adat, adat2, ut_b, 'T1', arany_info=ainfo)
        ellen(len(sorok) == len(gs), 'a sablon sorainak száma nem a gépi soroké')
        with open(ut_b, encoding='utf-8') as f:
            elso = f.readline()
            fej = f.readline().rstrip('\n').split('\t')
        ellen(elso.startswith('# MANUAL: scope=') and ' | forras=' in elso and ' | ts=T1 ' in elso and fej == OSZLOPOK,
              'a sablon fejléce nem a # MANUAL proveniencia / az oszlopok hibásak')
        r0 = beolvas(ut_b)
        ellen(all(x['osztaly'] == '' and x['indok'] == '' and x['konvencio_vagy_jegyzetpont'] == '' and x['valtozas_konvencio'] == ''
                  for x in r0), 'a sablon kézi oszlopai nem üresek')
        try:
            sablon_ir(adat, adat2, ut_b, 'T2', arany_info=ainfo)
            ellen(False, 'a meglévő besorolás-fájl felülíródott (--felulir nélkül)')
        except SystemExit as e:
            ellen('nem íródik felül' in str(e), 'a felülírás-védelem hibaüzenete hibás: %s' % e)
        with open(ut_b, encoding='utf-8') as f:
            ellen('T1' in f.readline(), 'a védett sablon megváltozott')
        # a kitöltetlen sablon: az ellenőrzés hibát jelez; jelentés nem íródik
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_j, ts='T1')
        ellen(kod == 1 and not os.path.exists(ut_j), 'a kitöltetlen besorolásra a fut() nem 1-es kód / jelentés íródott')
        h, _ = ellenoriz(adat, adat2, ut_b)
        n_el = sum(1 for v in gs.values() if v[8] == 'elteres')
        ellen(len(h) == 2 * n_el + (len(gs) - n_el), 'a kitöltetlen sablon hibáinak száma nem 2 × eltérés + egyéb sor: %d' % len(h))
        # besorolás-fájl nélkül: gépi összesítés
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], os.path.join(mappa, 'nincs.tsv'), ut_j, ts='T1')
        ellen(kod == 0 and os.path.exists(ut_j), 'besorolás nélkül a gépi jelentés nem íródott')
        with open(ut_j, encoding='utf-8') as f:
            md0 = f.read()
        ellen('kézi besorolás-fájl' in md0 and 'scope=' in md0 and 'forras=' in md0 and 'ts=T1' in md0 and '## 2.' not in md0,
              'a gépi jelentés fejléce/tartalma hibás')
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], os.path.join(mappa, 'nincs.tsv'), ut_j, ts='T1', szigoru=True)
        ellen(kod == 1, 'a szigorú ellenőrzés besorolás-fájl nélkül nem 1-es kód')
        # kitöltött besorolás: osztályok felváltva (a nem-eltérés soron üres), az indok nem üres; a szigorú kötelezők
        sorok_k = []
        with open(ut_b, encoding='utf-8') as f:
            sorok_f = f.read().split('\n')
        for i, s in enumerate(sorok_f):
            if not s or s.startswith('#') or s.startswith('futas\t'):
                sorok_k.append(s)
                continue
            m = s.split('\t')
            m[I_OSZT] = 'abc'[i % 3] if m[8] == 'elteres' else ''
            m[I_IND] = 'teszt-indok %d' % i
            if m[I_OSZT] in ('a', 'b'):
                m[I_KONV] = 'K%d' % (1 + i % 11)
            r = dict(zip(OSZLOPOK, m))
            if valtozas_kell(r):
                m[I_VALT] = KONVENCIOK[i % len(KONVENCIOK)]
            sorok_k.append('\t'.join(m))
        with open(ut_b, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_k))
        h, kezi = ellenoriz(adat, adat2, ut_b, szigoru=True)
        ellen(h == [] and len(kezi) == len(gs), 'a kitöltött besorolás hibát ad: %s' % h[:3])
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_j, ts='T1', szigoru=True)
        with open(ut_j, encoding='utf-8') as f:
            md1 = f.read()
        with contextlib.redirect_stdout(io.StringIO()):
            fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_j, ts='T2', szigoru=True)
        with open(ut_j, encoding='utf-8') as f:
            md2 = f.read()
        ellen(kod == 0 and '## 2.' in md1 and '## 3.' in md1 and '## 4.' in md1 and 'Opus-besorolás, nem mérés' in md1
              and md1.replace('ts=T1', 'ts=T2') == md2, 'a teljes jelentés hibás / nem determinisztikus')
        # a szigorú ellenőrzés: a hiányzó változás-konvenció és a/b konvenció hiba
        sorok_s = list(sorok_k)
        idx_v = [i for i, s in enumerate(sorok_s) if s and not s.startswith(('#', 'futas\t')) and s.split('\t')[I_VALT]]
        idx_ab = [i for i, s in enumerate(sorok_s) if s and not s.startswith(('#', 'futas\t')) and s.split('\t')[I_OSZT] in ('a', 'b')]
        if idx_v:
            m = sorok_s[idx_v[0]].split('\t')
            m[I_VALT] = ''
            sorok_s[idx_v[0]] = '\t'.join(m)
        m = sorok_s[idx_ab[0]].split('\t')
        m[I_KONV] = ''
        sorok_s[idx_ab[0]] = '\t'.join(m)
        ut_s = os.path.join(mappa, 'besorolas_szigoru.tsv')
        with open(ut_s, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_s))
        h_laza, _ = ellenoriz(adat, adat2, ut_s)
        h_sz, _ = ellenoriz(adat, adat2, ut_s, szigoru=True)
        ellen(h_laza == [] and any('konvenció/jegyzetpont nélkül' in x for x in h_sz)
              and (not idx_v or any('változás-konvenció nélkül' in x for x in h_sz)), 'a szigorú ellenőrzés nem fog: %s' % h_sz[:3])
        # F21.76: az „arany-felülvizsgálatra jelölt” jelölés: (c) soron a külön listába kerül (és (c) marad), (a)/(b) soron hiba
        sorok_j = list(sorok_k)
        idx_c = [i for i, s in enumerate(sorok_j) if s and not s.startswith(('#', 'futas\t')) and s.split('\t')[I_OSZT] == 'c'
                 and s.split('\t')[0] == meres_p3c.C3]
        for i in idx_c[:2]:
            m = sorok_j[i].split('\t')
            m[I_IND] += ' [%s]' % JELOLT
            sorok_j[i] = '\t'.join(m)
        ut_jb = os.path.join(mappa, 'besorolas_jelolt.tsv')
        with open(ut_jb, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_j))
        ut_jj = os.path.join(mappa, 'jelentes_jelolt.md')
        with contextlib.redirect_stdout(io.StringIO()):
            kod_j = fut(mappa, info['arany_ut'], info['arany_sha'], ut_jb, ut_jj, ts='T1', szigoru=True)
        with open(ut_jj, encoding='utf-8') as f:
            mdj = f.read()
        szak = mdj.split('### Arany-felülvizsgálatra jelölt (c) esetek')[-1].split('\n## ')[0]
        n_c3 = sum(1 for s in sorok_k if s and not s.startswith(('#', 'futas\t')) and s.split('\t')[0] == meres_p3c.C3
                   and s.split('\t')[I_OSZT] == 'c')
        ellen(kod_j == 0 and idx_c and ('Az F3V3 %d (c) esetéből %d' % (n_c3, min(2, len(idx_c)))) in szak
              and szak.count('[%s]' % JELOLT) == min(2, len(idx_c))
              and mdj.split('## 3.')[1].split('\n')[6] == md1.split('## 3.')[1].split('\n')[6],
              'a jelölt (c) esetek listája / számai hibásak (kód %d)' % kod_j)
        idx_a = [i for i, s in enumerate(sorok_j) if s and not s.startswith(('#', 'futas\t')) and s.split('\t')[I_OSZT] == 'a']
        m = sorok_j[idx_a[0]].split('\t')
        m[I_IND] += ' [%s]' % JELOLT
        sorok_j[idx_a[0]] = '\t'.join(m)
        with open(ut_jb, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_j))
        h_j, _ = ellenoriz(adat, adat2, ut_jb)
        ellen(any('csak (c) eltérés-soron' in x for x in h_j), 'a jelölés (a) soron nem hiba: %s' % h_j[:3])
        # hibák: ismeretlen osztály, üres indok, hiányzó és többlet sor, érvénytelen változás-konvenció, osztály a megszűnt soron
        sorok_h = list(sorok_k)
        idx = [i for i, s in enumerate(sorok_h) if s and not s.startswith('#') and not s.startswith('futas\t') and s.split('\t')[8] == 'elteres']
        m = sorok_h[idx[0]].split('\t')
        m[I_OSZT] = 'x'
        sorok_h[idx[0]] = '\t'.join(m)
        m = sorok_h[idx[1]].split('\t')
        m[I_IND] = ' '
        sorok_h[idx[1]] = '\t'.join(m)
        m = sorok_h[idx[4]].split('\t')
        m[I_VALT] = 'K12'
        sorok_h[idx[4]] = '\t'.join(m)
        m = sorok_h[idx[3]].split('\t')
        m[5] = str(int(m[5]) + 1000)
        sorok_h[idx[3]] = '\t'.join(m)
        del sorok_h[idx[2]]
        ut_h = os.path.join(mappa, 'besorolas_hibas.tsv')
        with open(ut_h, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok_h))
        h, _ = ellenoriz(adat, adat2, ut_h)
        ellen(any('érvénytelen vagy üres osztály' in x for x in h) and any('üres indok' in x for x in h)
              and any('besorolás nélküli' in x for x in h) and any('nincs gépi sor' in x for x in h)
              and any('érvénytelen változás-konvenció' in x for x in h),
              'az ellenőrzés nem fogta meg mind az öt hibatípust: %s' % h[:6])
        # az előzmény-oszlop: a valódi F3V2/F3V2B besorolások kulcsai; a v2-osztályok a/b/c/?
        v2o = v2_osztalyok(adat2)
        ellen(set(v2o) == set(V2_FUTASOK) and all(o in ('a', 'b', 'c', '?') for d in v2o.values() for o in d.values()),
              'a v2-osztályok hibásak')
        # --csak-c: a Sonnet nélkül (a SONNETV3 jsonl törölve), csak az F3V3 sorai; a meglévő besorolás Sonnet-sorai kimaradnak
        os.remove(os.path.join(mappa, 'valaszok', 'SONNETV3.jsonl'))
        adat_c, ainfo_c, adat2_c = betolt(mappa, info['arany_ut'], info['arany_sha'], csak_c=True)
        gs_c = gepi_sorok(adat_c, adat2_c, FUTASOK_C)
        ellen(gs_c == {k: v for k, v in gs.items() if k[0] == meres_p3c.C3}, 'csak-c: az F3V3 gépi sorai eltérnek a teljes módétól')
        h, kezi_c = ellenoriz(adat_c, adat2_c, ut_b, FUTASOK_C, szigoru=True)
        ellen(h == [] and set(kezi_c) == set(gs_c), 'csak-c: a meglévő (Sonnet-sorokat is tartalmazó) besorolás hibát ad: %s' % h[:3])
        ut_jc = os.path.join(mappa, 'jelentes_c.md')
        with contextlib.redirect_stdout(io.StringIO()):
            kod = fut(mappa, info['arany_ut'], info['arany_sha'], ut_b, ut_jc, ts='T1', csak_c=True, szigoru=True)
        with open(ut_jc, encoding='utf-8') as f:
            mdc = f.read()
        ellen(kod == 0 and '--csak-c' in mdc.split('\n')[2] and 'Sonnet (SONNETV3) |' not in mdc and '## 3.' in mdc,
              'csak-c: a jelentés hibás (kód %d)' % kod)
        # --csak-c sablon, majd --hozzafuz: a hiányzó sorok hozzáfűzve, a meglévők változatlanok
        ut_bc = os.path.join(mappa, 'besorolas_c.tsv')
        sablon_ir(adat_c, adat2_c, ut_bc, 'T1', arany_info=ainfo_c, futasok=FUTASOK_C)
        with open(ut_bc, encoding='utf-8') as f:
            elotte = f.read()
        uj = sablon_ir(adat_c, adat2_c, ut_bc, 'T2', arany_info=ainfo_c, futasok=FUTASOK_C, hozzafuz=True)
        with open(ut_bc, encoding='utf-8') as f:
            utana = f.read()
        ellen(uj == [] and elotte == utana, 'csak-c: a --hozzafuz hiány nélkül is írt')
        with open(ut_bc, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(elotte.split('\n')[:3]) + '\n')
        uj = sablon_ir(adat_c, adat2_c, ut_bc, 'T2', arany_info=ainfo_c, futasok=FUTASOK_C, hozzafuz=True)
        ellen(len(uj) == len(gs_c) - 1 and len(beolvas(ut_bc)) == len(gs_c), 'csak-c: a --hozzafuz nem a hiányzó sorokat fűzte hozzá')
        # hash-ellenőrzés: módosított arany -> SystemExit
        rossz = os.path.join(mappa, 'rossz.jsonl')
        shutil.copyfile(info['arany_ut'], rossz)
        with open(rossz, 'a', encoding='utf-8', newline='\n') as f:
            f.write('{}\n')
        shutil.copyfile(info['arany_sha'], os.path.join(mappa, 'rossz.sha256'))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fut(mappa, rossz, None, os.path.join(mappa, 'nincs.tsv'), os.path.join(mappa, 'x.md'), csak_c=True)
            ellen(False, 'az eltérő hash-ű arany nem állította meg a diffet')
        except SystemExit as e:
            ellen('sha256' in str(e), 'az eltérő hash hibaüzenete hibás: %s' % e)
        # --lista nem dob
        with contextlib.redirect_stdout(io.StringIO()) as puf:
            lista(adat_c, adat2_c, FUTASOK_C)
        ellen('ARANY:' in puf.getvalue() and ('hianyzo' in puf.getvalue() or 'tobblet' in puf.getvalue()), 'a --lista kimenete üres')
    finally:
        shutil.rmtree(mappa, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('c_diff_p3c önteszt rendben (független eltérés-számítás, megszűnt v2 (c) sorok, # MANUAL sablon, felülírás-védelem és '
          '--hozzafuz, öt hibatípus és a szigorú ellenőrzés, gépi és teljes jelentés, determinizmus, --csak-c, hash-ellenőrzés, '
          'régi kimenetek bájtazonossága)')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lista', action='store_true', help='az eltérések kontextussal')
    ap.add_argument('--sablon', action='store_true', help='a kézi besorolás váza (# MANUAL fejléccel; meglévőt nem ír felül)')
    ap.add_argument('--felulir', action='store_true', help='--sablon: a meglévő besorolás-fájl felülírása (szándékosan)')
    ap.add_argument('--hozzafuz', action='store_true', help='--sablon: a meglévő fájlhoz csak a hiányzó gépi sorok')
    ap.add_argument('--csak-c', action='store_true', help='csak az F3V3 (a SONNETV3 nem futott)')
    ap.add_argument('--szigoru', action='store_true', help='a kézi besorolás szigorú ellenőrzése (kötelező mezők)')
    ap.add_argument('--arany', default=None, help='az arany jsonl-je (alap: a legfrissebb befagyasztott)')
    ap.add_argument('--arany-sha', default=None)
    ap.add_argument('--forras-dir', default=None)
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    futasok = FUTASOK_C if args.csak_c else FUTASOK
    if args.lista or args.sablon:
        adat, info, adat2 = betolt(args.forras_dir, args.arany, args.arany_sha, args.csak_c)
        if args.lista:
            lista(adat, adat2, futasok)
            return 0
        sorok = sablon_ir(adat, adat2, BESOROLAS_UT, tokenek.generalas_ts(), args.felulir, info, futasok, args.hozzafuz)
        print('a sablon %s: %s (%d sor)' % ('kiegészítve' if args.hozzafuz else 'megírva', BESOROLAS_UT, len(sorok)))
        return 0
    return fut(args.forras_dir, args.arany, args.arany_sha, csak_c=args.csak_c, szigoru=args.szigoru)


if __name__ == '__main__':
    sys.exit(main())
