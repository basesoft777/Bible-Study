#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_ellenorzes.py — a régi (tartalom-alapú) Károli-szó + Strong párok ellenőrzése
a #22 gépi párosítása (adat/karoli_strong/parok_<könyv>.tsv) ellen. F65.

Ítélet soronként (elofordulasok.tsv sor: karoli_szo + strong + igehely):
  egyezik   — a sor minden Strongja előfordul a karoli_szo szavainak gépi párjai között
              ugyanazon a versen (igehely-tartományon); a szó-egyezés laza (DT-F65a (1)):
              bármelyik szó elég. Részleges egyezés: több szavas karoli_szo, ahol nem
              minden szó illeszkedett — a nem illesztett szavak fel vannak sorolva;
  elter     — a karoli_szo szavai megvannak a versben, de a sor valamelyik Strongja nincs
              köztük (a gépi Strongok az eltéréslistába kerülnek; a sor NEM változik);
  nincs_par — a karoli_szo egyetlen szava sincs a vers gépi párosításában
              (könyv hiányzik / szóalak eltér / vers hiányzik).
Átállítási feltétel (DT-F65a (2)-(3), SEMA 1.7): `egyezik` ÉS a Strongot igazoló gépi
párok mind `magas` bizonyosságúak. Csak az `azonositas_modja` mező változik
(`tartalom-alapú` -> `szó-szintű-gépi`); `karoli_szo`, `megbizhatosag`, `proveniencia`
marad. A --frissit alapból szárazon fut (--ir nélkül nem ír), és idempotens: csak
`tartalom-alapú` sort állít át, a már átállított sort nem bántja.

I/O: split('\\t') / '\\t'.join(), a csv modul tilos (CLAUDE.md).

Futtatás a repó gyökeréből:
    python eszkozok/karoli_ellenorzes.py --meres
    python eszkozok/karoli_ellenorzes.py --ellenorzes naplok/KAROLI_ELLENORZES_elteresek.tsv
    python eszkozok/karoli_ellenorzes.py --variancia adat/karoli_variancia.tsv [--ts 2026-10-11]
    python eszkozok/karoli_ellenorzes.py --frissit [--ir] [--motivum ID]
"""

import collections
import datetime
import glob
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAROK_MINTA = os.path.join('adat', 'karoli_strong', 'parok_*.tsv')
ELOFORDULASOK = os.path.join('adat', 'elofordulasok.tsv')
JELOLTEK = os.path.join('adat', 'jeloltek.tsv')
SZURT = {'a', 'az', 'és'}  # névelő és kötőszó: nem kerül a nem illesztett listába (DT-F65b (2))
UJ_MOD = 'szó-szintű-gépi'
REGI_MOD = 'tartalom-alapú'


def ma_ts():
    """A futás UTC időbélyege (nincs beégetett alapérték)."""
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def olvas(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    if sorok and sorok[-1] == '':
        sorok.pop()
    return sorok


def tabla(rel):
    """(sorok, a fejléc sorindexe, fejléc-mezők). A '#'-sorok megmaradnak."""
    sorok = olvas(rel)
    i = 0
    while sorok[i].startswith('#'):
        i += 1
    return sorok, i, sorok[i].split('\t')


def token(s):
    return re.findall(r"[^\W\d_]+", s.casefold())


def strong_norm(s):
    m = re.match(r'^([HG])0*(\d+)', s.strip())
    return (m.group(1) + m.group(2).zfill(4)) if m else s.strip()


def parok_sorok(f):
    with open(f, encoding='utf-8', newline='') as fh:
        for l in fh:
            l = l.rstrip('\n')
            if l.startswith('#') or l.startswith('vers\t') or not l:
                continue
            yield l.split('\t')


def betolt_parok():
    """vers -> [(hu_szo, strong, bizonyossag)]; könyv -> bizonyossag-számláló."""
    vers = collections.defaultdict(list)
    konyv_biz = {}
    for f in sorted(glob.glob(os.path.join(ROOT, PAROK_MINTA))):
        nev = os.path.basename(f)[len('parok_'):-4]
        c = collections.Counter()
        for p in parok_sorok(f):
            vers[p[0]].append((p[2], p[5], p[6]))
            c[p[6]] += 1
        konyv_biz[nev] = c
    return vers, konyv_biz


def versek(igehely):
    """'1Móz 14:18-20' -> versek listája; fejezethatárt átlépő tartomány: None."""
    m = re.match(r'^(\S+) (\d+):(\d+)(?:-(?:(\d+):)?(\d+))?$', igehely.strip())
    if not m:
        return None
    k, f1, v1, f2, v2 = m.groups()
    if v2 is None:
        return ['%s %s:%s' % (k, f1, v1)]
    if f2 is None or f2 == f1:
        return ['%s %s:%d' % (k, f1, v) for v in range(int(v1), int(v2) + 1)]
    return None


def ellenoriz_sor(igehely, karoli_szo, strongok, vers):
    """-> dict: itelet, gepi, biz, illesztett, nem_illesztett, megjegyzes"""
    r = {'itelet': 'nincs_par', 'gepi': [], 'biz': [], 'illesztett': [],
         'nem_illesztett': [], 'nincs_gepi_par': [], 'mas_strong': [], 'megjegyzes': ''}
    vl = versek(igehely)
    if vl is None:
        r['megjegyzes'] = 'igehely-tartomány nem bontható (%s)' % igehely
        return r
    par = [p for v in vl for p in vers.get(v, [])]
    if not par:
        r['megjegyzes'] = 'a vers/könyv nincs a gépi párosításban'
        return r
    toks = []
    for t in token(karoli_szo):
        if t not in toks:
            toks.append(t)
    talalt = [p for p in par if p[0].casefold() in toks]
    if not talalt:
        r['megjegyzes'] = 'a karoli_szo egyetlen szava sincs a versben'
        return r
    r['gepi'] = sorted({strong_norm(p[1]) for p in talalt})
    keresett = [strong_norm(s) for s in strongok]
    hianyzo = [s for s in keresett if s not in r['gepi']]
    if hianyzo:
        r['itelet'] = 'elter'
        r['biz'] = sorted({p[2] for p in talalt})
        r['megjegyzes'] = 'hiányzó a gépi párokból: ' + ','.join(hianyzo)
        return r
    egyezo = [p for p in talalt if strong_norm(p[1]) in keresett]
    ill = {p[0].casefold() for p in egyezo}
    r['itelet'] = 'egyezik'
    r['biz'] = sorted({p[2] for p in egyezo})
    r['illesztett'] = [t for t in toks if t in ill]
    # Névelő és "és" kiszűrve a listából (DT-F65b (2)); csak lista-szűrés, az ítélet nem változik.
    for t in toks:
        if t in ill or t in SZURT:
            continue
        masok = sorted({strong_norm(p[1]) for p in par if p[0].casefold() == t})
        if masok:
            r['mas_strong'].append('%s:%s' % (t, '+'.join(masok)))
        else:
            r['nincs_gepi_par'].append(t)
        r['nem_illesztett'].append(t)
    return r


def reszleges(r):
    """Több szavas karoli_szo, ahol (a névelő és az "és" nélkül) nem minden szó illeszkedett a sor Strongjaihoz."""
    return bool(r['nem_illesztett'])


def frissitheto(r):
    return r['itelet'] == 'egyezik' and r['biz'] == ['magas']


def ellenorzes_futtat(vers=None, modok=(REGI_MOD, UJ_MOD)):
    if vers is None:
        vers, _ = betolt_parok()
    sorok, i, fej = tabla(ELOFORDULASOK)
    ix = {n: k for k, n in enumerate(fej)}
    eredm = []
    for n in range(i + 1, len(sorok)):
        p = sorok[n].split('\t')
        if len(p) <= ix['azonositas_modja'] or p[ix['azonositas_modja']] not in modok:
            continue
        st = [s for s in p[ix['strong']].split('+') if s]
        r = ellenoriz_sor(p[ix['igehely']], p[ix['karoli_szo']], st, vers)
        eredm.append({'n': n + 1, 'id': p[0], 'igehely': p[ix['igehely']], 'karoli_szo': p[ix['karoli_szo']],
                      'strong': p[ix['strong']], 'mod': p[ix['azonositas_modja']], 'r': r})
    return eredm


def meres():
    vers, kb = betolt_parok()
    print('## bizonyossag-megoszlás könyvenként')
    for k, c in sorted(kb.items()):
        print('%s\t%s' % (k, dict(c)))
    er = ellenorzes_futtat(vers)
    print('## elofordulasok.tsv tartalom-alapú / szó-szintű-gépi sorok: %d' % len(er))
    print(collections.Counter(e['r']['itelet'] for e in er))
    print('frissíthető (egyezik+magas):', sum(1 for e in er if frissitheto(e['r'])))
    kon = collections.Counter((e['igehely'].split(' ')[0], e['r']['itelet']) for e in er)
    for k in sorted(kon):
        print(k, kon[k])


ELT_FEJ = ['sor', 'id', 'igehely', 'karoli_szo', 'regi_strong', 'jelenlegi_mod', 'itelet',
           'gepi_strongok', 'bizonyossag', 'reszleges', 'illesztett_szavak',
           'nincs_gepi_par', 'mas_strong', 'megjegyzes']


def nincs_strong_sorok():
    """A jeloltek.tsv azon tartalom-alapú sorai, amelyeknek nincs elofordulasok-párjuk (id + igehely):
    Strong híján az ellenőrzés nem futtatható (`nincs_strong`)."""
    ekulcs = set()
    sorok, i, fej = tabla(ELOFORDULASOK)
    ix = {n: k for k, n in enumerate(fej)}
    for n in range(i + 1, len(sorok)):
        p = sorok[n].split('\t')
        if len(p) > ix['igehely']:
            ekulcs.add((p[ix['id']], p[ix['igehely']]))
    sorok, i, fej = tabla(JELOLTEK)
    ix = {n: k for k, n in enumerate(fej)}
    ki = []
    for n in range(i + 1, len(sorok)):
        p = sorok[n].split('\t')
        if len(p) > ix['azonositas_modja'] and p[ix['azonositas_modja']] == REGI_MOD                 and (p[ix['id']], p[ix['igehely']]) not in ekulcs:
            ki.append((n + 1, p[ix['id']], p[ix['igehely']], p[ix['karoli_szo']], p[ix['azonositas_modja']]))
    return ki


# A régi igehely nem Károli-kulcs (KJV/MT-számozás); a Károli-kulcs a jobb oldalon.
# Az ítélet nem változik, csak jelölés a megjegyzésben.
KULCS_ELTOLAS = {
    'Préd 9:10': 'Préd 9:12',
    'Jób 17:13': 'Jób 17:12',
    'Jób 17:16': 'Jób 17:15',
}


def megjegyzes(e):
    r = e['r']
    m = r['megjegyzes']
    k = KULCS_ELTOLAS.get(e['igehely'])
    if k and r['itelet'] != 'egyezik':
        m += ('; a régi igehely nem Károli-kulcs (verseltolás), a Károli-kulcs: %s; '
              'az ítélet nem valódi szóeltérésből ered, kézi ítéletre vár' % k)
    return m


def ir_eltereslista(ut, vers=None):
    er = ellenorzes_futtat(vers)
    ns = nincs_strong_sorok()
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('# F65 M2: a tartalom-alapú (és már átállított) sorok ellenőrzése a #22 gépi párosítása ellen | '
                'scope=manual | forras=adat/elofordulasok.tsv, adat/karoli_strong/parok_*.tsv | ts=manual (nem lekérdezés) | '
                'előállítás: eszkozok/karoli_ellenorzes.py; az elter/nincs_par sor NEM változott, kézi ítéletre vár\n')
        f.write('\t'.join(ELT_FEJ) + '\n')
        for e in er:
            r = e['r']
            f.write('\t'.join([str(e['n']), e['id'], e['igehely'], e['karoli_szo'], e['strong'], e['mod'],
                               r['itelet'], ','.join(r['gepi']), ','.join(r['biz']),
                               'igen' if reszleges(r) else 'nem', ','.join(r['illesztett']),
                               ','.join(r['nincs_gepi_par']), ','.join(r['mas_strong']), megjegyzes(e)]) + '\n')
        for n, i_d, ig, szo, mod in ns:
            f.write('\t'.join([str(n), i_d, ig, szo, '', mod, 'nincs_strong', '', '', 'nem', '', '', '',
                               'jeloltek.tsv-sor: nincs elofordulasok-párja (id + igehely), Strong híján nem ellenőrizhető']) + '\n')
    print('írva:', ut, len(er), '+', len(ns), 'nincs_strong sor')
    return er


VAR_FEJ = ['tipus', 'konyv', 'kulcs', 'ertek', 'darab', 'bizonyossag', 'id', 'igehely',
           'karoli_szo', 'reszleges', 'nincs_gepi_par', 'mas_strong', 'proveniencia']


def variancia(ut, ts=None, konyvek=None):
    """Variancia-térkép + soronkénti megerősítések. konyvek: parok-fájlnevek (None = amelyikben van magas pár)."""
    ts = ts or ma_ts()
    sor_ki = []
    vers = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(ROOT, PAROK_MINTA))):
        k = os.path.basename(f)[len('parok_'):-4]
        rows = list(parok_sorok(f))
        kh = rows[0][0].split(' ')[0] if rows else k  # a konyv oszlop alakja: az igehely rövidítése (SEMA 2.24)
        for p in rows:
            vers[p[0]].append((p[2], p[5], p[6]))
        if konyvek is None:
            if not any(p[6] == 'magas' for p in rows):
                continue
        elif k not in konyvek:
            continue
        a = collections.defaultdict(collections.Counter)
        b = collections.defaultdict(collections.Counter)
        for p in rows:
            st, sz, bz = strong_norm(p[5]), p[2].casefold(), p[6]
            a[(bz, st)][sz] += 1
            b[(bz, sz)][st] += 1
        prov = 'scope=manual | forras=adat/karoli_strong/parok_%s.tsv | ts=%s' % (k, ts)
        for tip, d in (('strong_szoalak', a), ('szoalak_strong', b)):
            for (bz, kulcs) in sorted(d):
                for ertek, n in sorted(d[(bz, kulcs)].items(), key=lambda x: (-x[1], x[0])):
                    sor_ki.append([tip, kh, kulcs, ertek, str(n), bz, '', '', '', '', '', '', prov])
    for e in ellenorzes_futtat(vers):
        r = e['r']
        if not frissitheto(r):
            continue
        sor_ki.append(['megerosites', e['igehely'].split(' ')[0], e['strong'], ','.join(r['gepi']), '', 'magas',
                       e['id'], e['igehely'], e['karoli_szo'], 'igen' if reszleges(r) else 'nem',
                       ','.join(r['nincs_gepi_par']), ','.join(r['mas_strong']),
                       'scope=manual | forras=adat/karoli_strong/parok_*.tsv (vers: %s) | ts=%s' % (e['igehely'], ts)])
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('# F65 M1: Károli-variancia (Strong -> szóalakok, szóalak -> Strongok) a magas párt tartalmazó könyvekre, '
                'és soronkénti megerősítések | scope=manual | forras=adat/karoli_strong/parok_*.tsv | ts=%s | '
                'modell-kimenet származéka, javaslat: nem lekérdezés-eredmény | '
                'előállítás: eszkozok/karoli_ellenorzes.py --variancia\n' % ts)
        f.write('\t'.join(VAR_FEJ) + '\n')
        for s in sor_ki:
            f.write('\t'.join(s) + '\n')
    print('írva:', ut, len(sor_ki), 'sor')
    return sor_ki


def frissit(ir=False, motivum=None, vers=None):
    """Az egyezik+magas sorok azonositas_modja-ját átállítja. -> (elofordulasok, jeloltek) darabszám."""
    er = ellenorzes_futtat(vers, modok=(REGI_MOD,))
    cel = {(e['id'], e['igehely']) for e in er
           if frissitheto(e['r']) and (motivum is None or e['id'] == motivum)}
    szamok = []
    for rel in (ELOFORDULASOK, JELOLTEK):
        sorok, i, fej = tabla(rel)
        ix = {n: k for k, n in enumerate(fej)}
        uj = list(sorok)
        db = 0
        for n in range(i + 1, len(sorok)):
            p = sorok[n].split('\t')
            if len(p) <= ix['azonositas_modja'] or p[ix['azonositas_modja']] != REGI_MOD:
                continue
            if (p[ix['id']], p[ix['igehely']]) in cel:
                p[ix['azonositas_modja']] = UJ_MOD
                uj[n] = '\t'.join(p)
                db += 1
        for n, (a, b) in enumerate(zip(sorok, uj)):
            if a != b:
                pa, pb = a.split('\t'), b.split('\t')
                kul = [k for k in range(len(pa)) if pa[k] != pb[k]]
                if len(pa) != len(pb) or kul != [ix['azonositas_modja']]:
                    raise SystemExit('ELTÉRÉS a %s %d. során: nem csak az azonositas_modja változott' % (rel, n + 1))
        if ir and db:
            with open(os.path.join(ROOT, rel), 'w', encoding='utf-8', newline='') as f:
                f.write('\n'.join(uj) + '\n')
        szamok.append(db)
    print('%s: elofordulasok %d, jeloltek %d sor%s' % ('ÍRVA' if ir else 'szárazon', szamok[0], szamok[1],
                                                       '' if ir else ' (--ir nélkül nem ír)'))
    return tuple(szamok)


def _arg(a, nev, alap=None):
    return a[a.index(nev) + 1] if nev in a else alap


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--meres':
        meres()
    elif a and a[0] == '--ellenorzes':
        ir_eltereslista(a[1])
    elif a and a[0] == '--variancia':
        variancia(a[1], _arg(a, '--ts'))
    elif a and a[0] == '--frissit':
        frissit('--ir' in a, _arg(a, '--motivum'))
    else:
        print(__doc__)
