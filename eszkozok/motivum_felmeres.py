#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motivum_felmeres.py — motívumfüggetlen felmérő lekérdezés (F123, 2d. szakasz 1. pont).

A `naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md` „Javasolt sorrend” 5. pontjában
javasolt három lekérdezés egy tetszőleges motívumra:

  (a) kísérő szavak — a motívum előfordulási verseiben álló többi Strong
      (`adat/grammatikai_strongok.tsv` szűréssel), versszám szerint;
  (b) szomszédos motívumok — más motívumok előfordulásai ugyanabban a fejezetben;
  (c) válasz-szavak — a megadott „válasz” Strongok (alapból felel/meghall) a motívum
      előfordulásaitól ±N versen belül, ugyanabban a fejezetben.

A kimenet mért tény, nem állítás: a szomszédos motívum vagy a közös szókészlet csak
jelöltként mehet tovább (`adat/jeloltek.tsv`, CLAUDE.md 2. szabály), és a közös
szókészlet nem bizonyít idézést. Az eszköz csak olvas; adattáblát nem ír.

Adatforrás: a repó kanonikus táblái (`adat/elofordulasok.tsv`, `adat/motivumok.tsv`,
`konkordancia/TAHOT_kivonat.tsv`, `konkordancia/TAGNT_kivonat.tsv`,
`adat/grammatikai_strongok.tsv`), nem a `pardes.db` — így a mérés az ág aktuális
adatán fut, építés nélkül. A TSV-olvasás `split('\\t')` (a `lekerdez.read_tsv`).

Futtatás:
    python eszkozok/motivum_felmeres.py ALVIL-001 --ki naplok/F123_felmeres_ALVIL-001
    (opciók: --tavolsag 3, --valasz H6030,H8085,G0191,G1522,G0611, --min-vers 2)

Kimenet (a --ki előtaggal): `<elotag>_kiserok.tsv`, `<elotag>_szomszedok.tsv`,
`<elotag>_valasz.tsv` és `<elotag>.md` (összegzés, paraméterek, proveniencia).
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lekerdez as L  # noqa: E402

ROOT = L.ROOT
ALAP_VALASZ = ['H6030', 'H8085', 'G0191', 'G1522', 'G0611']


def igehely_lista(igehely, karoli_kulcsok):
    """Egy igehely vagy tartomány versei (magyar alak) a Károli-kulcsok szerint."""
    if '-' not in igehely:
        return [igehely]
    try:
        rng = L.parse_range(igehely)
    except ValueError:
        return [igehely]
    if rng[0] == 'verse':
        return [igehely]
    ki = []
    for kulcs, p in karoli_kulcsok:
        if L.in_range(rng, *p):
            ki.append((p[1], p[2], kulcs))
    ki.sort()
    return [k[2] for k in ki] or [igehely]


def strongok(nyers):
    return [s.strip() for s in nyers.split('+') if s.strip()]


def betolt():
    karoli = []
    for k in L.load_karoli_1908():
        try:
            karoli.append((k, L.parse_igehely(k)))
        except ValueError:
            continue
    elof = L.read_tsv_skip_comments(ROOT / 'adat' / 'elofordulasok.tsv')
    motiv = {r['id']: r for r in L.read_tsv_skip_comments(ROOT / 'adat' / 'motivumok.tsv')}
    # vers -> [(strong, szoto, rovid)]
    versek = defaultdict(list)
    for r in L.load_tahot() + L.load_tagnt():
        for s in strongok(r['Strong-szám']):
            versek[r['_parsed']].append((s, r['Szótő'], r['Rövid jelentés']))
    gramm = L.load_grammatikai_strongok()
    return karoli, elof, motiv, versek, gramm


def main():
    ap = argparse.ArgumentParser(description='Motívumfüggetlen felmérő lekérdezés (F123 2d. 1.)')
    ap.add_argument('motivum')
    ap.add_argument('--ki', required=True, help='kimeneti előtag (pl. naplok/F123_felmeres_ALVIL-001)')
    ap.add_argument('--tavolsag', type=int, default=3)
    ap.add_argument('--valasz', default=','.join(ALAP_VALASZ))
    ap.add_argument('--min-vers', type=int, default=1,
                    help='a kísérő szó legalább ennyi motívumversben álljon (alap: 1, azaz mind)')
    args = ap.parse_args()

    karoli, elof, motiv, versek, gramm = betolt()
    if args.motivum not in motiv:
        sys.exit('ismeretlen motívum-ID: %s' % args.motivum)
    ts = L.ts()
    valasz = [s.strip() for s in args.valasz.split(',') if s.strip()]

    # a motívum versei, sorok szerint
    sajat_sorok = [r for r in elof if r['id'] == args.motivum]
    sajat_strong = set()
    for r in sajat_sorok:
        sajat_strong.update(strongok(r['strong']) if r['strong'] else [])
    m_versek = []  # (sor_igehely, vers_igehely, parsed)
    nem_elemzett = []
    for r in sajat_sorok:
        for v in igehely_lista(r['igehely'], karoli):
            try:
                m_versek.append((r['igehely'], v, L.parse_igehely(v)))
            except ValueError:
                nem_elemzett.append(v)
    if nem_elemzett:
        print('figyelem: nem elemezhető igehely: %s' % ', '.join(nem_elemzett), file=sys.stderr)
    m_parsed = sorted({p for _, _, p in m_versek})

    # (a) kísérő szavak
    gyak = defaultdict(set)
    info = {}
    kizart_gramm = set()
    for p in m_parsed:
        for s, szoto, rovid in versek.get(p, []):
            if s in gramm:
                kizart_gramm.add(s)
                continue
            gyak[s].add(p)
            info.setdefault(s, (szoto, rovid))
    glob = defaultdict(int)
    for p, toks in versek.items():
        for s in {t[0] for t in toks}:
            if s in gyak:
                glob[s] += 1
    prov_a = ('scope=%s előfordulási versei (%d sor, %d vers) | forras=adat/elofordulasok.tsv + '
              'konkordancia/TAHOT_kivonat.tsv + TAGNT_kivonat.tsv, szűrés: adat/grammatikai_strongok.tsv '
              '(%d grammatikai Strong kizárva) | ts=%s' % (args.motivum, len(sajat_sorok), len(m_parsed),
                                                         len(kizart_gramm), ts))
    a_sorok = []
    for s in sorted(gyak, key=lambda x: (-len(gyak[x]), x)):
        if len(gyak[s]) < args.min_vers:
            continue
        vl = ['%s %d:%d' % p for p in sorted(gyak[s])]
        a_sorok.append([s, info[s][0], info[s][1], 'igen' if s in sajat_strong else 'nem',
                        str(len(gyak[s])), str(glob[s]), '; '.join(vl), prov_a])

    # (b) szomszédos motívumok ugyanabban a fejezetben
    fej_m = defaultdict(set)
    for _, v, p in m_versek:
        fej_m[(p[0], p[1])].add(p[2])
    mas = defaultdict(lambda: defaultdict(set))  # (fej) -> id -> versek
    for r in elof:
        if r['id'] == args.motivum:
            continue
        for v in igehely_lista(r['igehely'], karoli):
            try:
                p = L.parse_igehely(v)
            except ValueError:
                continue
            if (p[0], p[1]) in fej_m:
                mas[(p[0], p[1])][r['id']].add(p[2])
    prov_b = ('scope=%s fejezetei (%d fejezet) × adat/elofordulasok.tsv többi motívuma | '
              'forras=adat/elofordulasok.tsv (tartományok versre bontva a Karoli_1908.tsv kulcsaival) | ts=%s'
              % (args.motivum, len(fej_m), ts))
    b_sorok = []
    for fej in sorted(mas):
        for mid in sorted(mas[fej]):
            sv = sorted(fej_m[fej])
            mv = sorted(mas[fej][mid])
            tav = min(abs(a - b) for a in sv for b in mv)
            b_sorok.append(['%s %d' % fej, mid, ', '.join(map(str, sv)), ', '.join(map(str, mv)),
                            str(tav), 'igen' if set(sv) & set(mv) else 'nem', prov_b])

    # (c) válasz-szavak ±N versen belül
    prov_c = ('scope=%s előfordulásai ±%d vers, azonos fejezet | forras=konkordancia/TAHOT_kivonat.tsv + '
              'TAGNT_kivonat.tsv | valasz=%s | ts=%s' % (args.motivum, args.tavolsag, '+'.join(valasz), ts))
    c_sorok = []
    vizsgalt = set()
    for sor_ig, v, p in m_versek:
        for d in range(-args.tavolsag, args.tavolsag + 1):
            q = (p[0], p[1], p[2] + d)
            for s, szoto, rovid in versek.get(q, []):
                if s in valasz:
                    kulcs = (v, q, s)
                    if kulcs in vizsgalt:
                        continue
                    vizsgalt.add(kulcs)
                    c_sorok.append([sor_ig, v, '%s %d:%d' % q, str(d), s, szoto, rovid, prov_c])
    c_hely = {r[1] for r in c_sorok}

    elotag = Path(args.ki)
    if not elotag.is_absolute():
        elotag = ROOT / elotag

    def ir(utvonal, fejlec, sorok):
        with open(utvonal, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT: eszkozok/motivum_felmeres.py %s | %s\n' % (args.motivum, ts))
            f.write('\t'.join(fejlec) + '\n')
            for s in sorok:
                assert all('\t' not in m and '\n' not in m for m in s)
                f.write('\t'.join(s) + '\n')

    ir(str(elotag) + '_kiserok.tsv',
       ['strong', 'szoto', 'rovid_jelentes', 'sajat_gerinc', 'motivum_vers_db', 'korpusz_vers_db', 'versek',
        'proveniencia'], a_sorok)
    ir(str(elotag) + '_szomszedok.tsv',
       ['fejezet', 'mas_motivum', 'sajat_versek', 'mas_versek', 'min_tavolsag', 'kozos_vers', 'proveniencia'],
       b_sorok)
    ir(str(elotag) + '_valasz.tsv',
       ['sor_igehely', 'motivum_vers', 'talalat_vers', 'eltolas', 'strong', 'szoto', 'rovid_jelentes',
        'proveniencia'], c_sorok)

    mas_db = defaultdict(int)
    for r in b_sorok:
        mas_db[r[1]] += 1
    md = []
    md.append('# GENERÁLT: eszkozok/motivum_felmeres.py %s | %s' % (args.motivum, ts))
    md.append('')
    md.append('# Felmérő lekérdezés — %s' % args.motivum)
    md.append('')
    md.append('*Mért tény, nem állítás. A szomszédos motívum és a közös szókészlet csak jelöltként mehet '
              'tovább (`adat/jeloltek.tsv`, 2. szabály); a közös szókészlet nem bizonyít idézést. '
              'A teljes sorok a három TSV-ben állnak; ez az összegzés.*')
    md.append('')
    md.append('Paraméterek: távolság ±%d vers (azonos fejezet); válasz-Strongok: %s; kísérő szó min. '
              '%d motívumversben.' % (args.tavolsag, ', '.join(valasz), args.min_vers))
    md.append('')
    md.append('| Blokk | Sorok | Fájl |')
    md.append('|---|---|---|')
    md.append('| (a) kísérő szavak | %d Strong (%d motívumvers; %d grammatikai Strong kizárva) | `%s_kiserok.tsv` |'
              % (len(a_sorok), len(m_parsed), len(kizart_gramm), elotag.name))
    md.append('| (b) szomszédos motívumok | %d fejezet×motívum pár, %d másik motívum | `%s_szomszedok.tsv` |'
              % (len(b_sorok), len(mas_db), elotag.name))
    md.append('| (c) válasz-szavak | %d találat, %d motívumversnél | `%s_valasz.tsv` |'
              % (len(c_sorok), len(c_hely), elotag.name))
    md.append('')
    md.append('**(b) másik motívumok, fejezetszám szerint:** ' +
              (', '.join('%s %d' % (k, v) for k, v in sorted(mas_db.items(), key=lambda x: (-x[1], x[0])))
               or '— (üres eredmény)'))
    md.append('')
    top = ['%s %s (%s/%s)' % (r[0], r[1], r[4], r[5]) for r in a_sorok if r[3] == 'nem'][:15]
    md.append('**(a) a 15 leggyakoribb nem saját kísérő Strong (motívumvers / korpuszvers):** ' +
              ('; '.join(top) or '— (üres eredmény)'))
    md.append('')
    md.append('Proveniencia:')
    md.append('')
    for p in (prov_a, prov_b, prov_c):
        md.append('- `%s`' % p)
    md.append('')
    with open(str(elotag) + '.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md))
    print('(a) %d kísérő Strong · (b) %d pár · (c) %d válasz-találat -> %s.*'
          % (len(a_sorok), len(b_sorok), len(c_sorok), elotag))


if __name__ == '__main__':
    main()
