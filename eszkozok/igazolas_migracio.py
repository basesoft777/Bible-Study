#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
igazolas_migracio.py — a D25 séma-döntés végrehajtása.

Az F3 betöltői a proveniencia-stringbe írták az igazolás tényét is:

    scope=manual | forras=Tehom_tematikus.md | ts=2026-09-10 | talalat=IGAZOLVA | strong_vart=H8415

Ez egy mezőben két tényt hordoz: honnan származik az ÁLLÍTÁS (a study -> manual),
és hogy IGAZOLTA-e valami (a TAHOT-visszakeresés -> lekérdezés volt). A SEMA 1.5
szerint a proveniencia kötelező kulcsai kizárólag scope, forras, ts.

Ez a szkript szétválasztja a kettőt:
  - a proveniencia visszaáll a kanonikus "scope | forras | ts" alakra,
  - a talalat= érték az új `igazolas` oszlopba kerül (zárt értékkészlet, SEMA 1.8),
  - a strong_vart= eldobásra kerül, mert igazoltan redundáns a `strong` oszloppal
    (a migráció ezt minden soron ellenőrzi, és eltérésnél MEGÁLL).

I/O — FONTOS: sima split('\\t') / '\\t'.join(), NEM a csv modul.
A csv.reader/csv.writer körútja nem bájthű: a " jellel kezdődő mezőkről a reader
leszedi az idézőjeleket, a " jelet tartalmazó mezőket pedig a writer körülidézi és
belül duplázza. Ezen a táblán ez 127 sort érintene a migráción felül. A repó többi
eszköze (f3_4_*.py) szintén split('\\t')-vel olvas, tehát ez az egyetlen konzisztens
forma. Egyik mező sem tartalmaz tabot, így a szétvágás egyértelmű — ezt a szkript
ellenőrzi is.

Futtatás a repó gyökeréből:
    python eszkozok/igazolas_migracio.py            # szárazon, csak jelent
    python eszkozok/igazolas_migracio.py --ir       # ténylegesen ír
"""

import collections
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'adat', 'elofordulasok.tsv')

TALALAT_MAP = {
    'IGAZOLVA': 'TAHOT-igazolt',
    'NT-nincs_TAHOT_hatalykor': 'TAHOT-hatokoron-kivul',
    None: 'nincs',
}
ERVENYES = sorted(set(TALALAT_MAP.values()))


def kulcsok(prov):
    """A proveniencia-string kulcs->érték szótára, sorrendtartóan."""
    d = collections.OrderedDict()
    for darab in prov.split('|'):
        darab = darab.strip()
        if not darab or '=' not in darab:
            continue
        k, _, v = darab.partition('=')
        d[k.strip()] = v.strip()
    return d


def main():
    ir = '--ir' in sys.argv

    with io.open(TABLA, encoding='utf-8', newline='') as f:
        nyers = f.read()

    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    vege_ujsor = nyers.endswith(sorveg)
    sorok = nyers.split(sorveg)
    if vege_ujsor:
        sorok = sorok[:-1]

    # a tábla '#' előtétsorokkal kezdődhet — a fejléc az első nem-kommentsor
    fejlec_idx = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fejlec = sorok[fejlec_idx].split('\t')

    if 'igazolas' in fejlec:
        print('A migráció már lefutott (az igazolas oszlop létezik). Nincs teendő.')
        return 0

    i_prov = fejlec.index('proveniencia')
    i_strong = fejlec.index('strong')

    hibak = []
    kimenet = list(sorok[:fejlec_idx])
    kimenet.append('\t'.join(fejlec + ['igazolas']))
    szamlalo = collections.Counter()

    for sorszam, nyers_sor in enumerate(sorok[fejlec_idx + 1:], start=fejlec_idx + 2):
        if not nyers_sor.strip():
            kimenet.append(nyers_sor)
            continue
        if nyers_sor.startswith('#'):
            kimenet.append(nyers_sor)
            continue

        mezok = nyers_sor.split('\t')
        if len(mezok) != len(fejlec):
            hibak.append('%d. sor: %d oszlop %d helyett' % (sorszam, len(mezok), len(fejlec)))
            continue

        d = kulcsok(mezok[i_prov])

        sv = d.get('strong_vart')
        if sv is not None and sv != mezok[i_strong].strip():
            hibak.append('%d. sor: strong_vart=%s != strong=%s' % (sorszam, sv, mezok[i_strong]))
            continue

        talalat = d.get('talalat')
        if talalat not in TALALAT_MAP:
            hibak.append('%d. sor: ismeretlen talalat=%s' % (sorszam, talalat))
            continue

        hianyzo = [k for k in ('scope', 'forras', 'ts') if k not in d]
        if hianyzo:
            hibak.append('%d. sor: hiányzó kötelező kulcs: %s' % (sorszam, ', '.join(hianyzo)))
            continue

        igazolas = TALALAT_MAP[talalat]
        szamlalo[igazolas] += 1
        mezok[i_prov] = ' | '.join('%s=%s' % (k, d[k]) for k in ('scope', 'forras', 'ts'))
        kimenet.append('\t'.join(mezok + [igazolas]))

    print('Sorok: %d' % (len(sorok) - fejlec_idx - 1))
    for k in ERVENYES:
        print('  igazolas=%-24s %d' % (k, szamlalo[k]))

    if hibak:
        print('\nHIBA (%d) — nem írtam semmit:' % len(hibak))
        for h in hibak[:20]:
            print('  ' + h)
        return 1

    # bájthűség-próba: az utolsó oszlop levágása után minden sornak azonosnak kell
    # lennie az eredetivel, a proveniencia-mező kivételével
    ellenorzott = 0
    for eredeti, uj in zip(sorok[fejlec_idx + 1:], kimenet[fejlec_idx + 1:]):
        if not eredeti.strip() or eredeti.startswith('#'):
            continue
        a = eredeti.split('\t')
        b = uj.split('\t')[:-1]
        for oszlop, (x, y) in enumerate(zip(a, b)):
            if oszlop == i_prov:
                continue
            if x != y:
                hibak.append('bájthűség sérült a(z) %s oszlopban' % fejlec[oszlop])
        ellenorzott += 1

    if hibak:
        print('\nHIBA — nem írtam semmit:')
        for h in hibak[:20]:
            print('  ' + h)
        return 1

    print('\nHiba nincs. Bájthűség ellenőrizve %d soron (a proveniencián kívül minden mező változatlan).' % ellenorzott)
    if not ir:
        print('Szárazon futott. Tényleges íráshoz: --ir')
        return 0

    with io.open(TABLA, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(kimenet) + (sorveg if vege_ujsor else ''))
    print('Megírva: adat/elofordulasok.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
