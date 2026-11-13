# -*- coding: utf-8 -*-
"""F194.36 — az ISTENTISZT-001 20 előfordulás-sorának `igazolas` mezője (adat/SEMA.md 1.8) a szövegből.

A 20 sor `igazolas: nincs` értékkel állt: a TAHOT-visszakeresés (n14_hamart_betoltes.tahot_ellenoriz mintája) nem futott
rájuk. Ószövetségi sor: a `strong` mező minden tagja (H7121+H8034) a Károli-kulcsú TAHOT-versben áll → `TAHOT-igazolt`,
különben `nincs`. Újszövetségi sor: a SEMA 1.8 zárt értékkészletében nincs TAGNT-érték, ezért `TAHOT-hatokoron-kivul`
(a HAMART-001 és a többi motívum gyakorlata); a görög szót (G1941) a TAGNT-ben ellenőrizzük, és eltérésnél megállunk.
A proveniencia-sor a kimenet végén áll, a naplóba kerül. Írás előtt a nem érintett sorok összevetése (CLAUDE.md).
Futtatás a repó gyökeréből: python naplok/F194_igazolas.py [--ir]"""
import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'eszkozok'))
import lekerdez as L  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
P = 'adat/elofordulasok.tsv'
USZ = ('Mt ', 'Mk ', 'Luk ', 'Ján ', 'ApCsel ', 'Róm ', '1Kor ', '2Kor ', 'Gal ', 'Ef ', 'Fil ', 'Kol ', 'Zsid ',
       'Jak ', '1Pét ', '2Pét ', 'Jel ', '1Tim ', '2Tim ')


def van(sorok, igehely, strong):
    rng = L.parse_range(igehely)
    return any(r['Strong-szám'] == strong and r['_parsed'] and L.in_range(rng, *r['_parsed']) for r in sorok)


raw = open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
sorok = raw.split(nl)
fi = next(k for k, s in enumerate(sorok) if s.startswith('id\t'))
fej = sorok[fi].split('\t')
ix = {n: i for i, n in enumerate(fej)}
tahot, tagnt = L.load_tahot(), L.load_tagnt()
uj = list(sorok)
valtozott = 0
for k in range(fi + 1, len(sorok)):
    m = sorok[k].split('\t')
    if m[0] != ID:
        continue
    ige, strong = m[ix['igehely']], m[ix['strong']]
    tagok = [s for s in strong.split('+') if s]
    if ige.startswith(USZ):
        hiany = [s for s in tagok if not van(tagnt, ige, s)]
        if hiany:
            sys.exit('ELTÉRÉS: %s — a TAGNT-ben nincs: %s' % (ige, hiany))
        ert = 'TAHOT-hatokoron-kivul'
    else:
        ert = 'TAHOT-igazolt' if tagok and all(van(tahot, ige, s) for s in tagok) else 'nincs'
    print('%-14s %-12s %s → %s' % (ige, strong, m[ix['igazolas']], ert))
    if m[ix['igazolas']] != ert:
        m[ix['igazolas']] = ert
        uj[k] = '\t'.join(m)
        valtozott += 1

# a nem érintett sorok összevetése
for a, b in zip(sorok, uj):
    if a != b and a.split('\t')[0] != ID:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')
print('változott: %d sor' % valtozott)
print('proveniencia: scope=motivum:%s (20 sor, strong-tagonként) | forras=konkordancia/TAHOT_kivonat.tsv+'
      'konkordancia/TAGNT_kivonat.tsv (lekerdez.load_tahot/load_tagnt, parse_range/in_range) | ts=%s'
      % (ID, datetime.date.today().isoformat()))
if '--ir' in sys.argv:
    open(P, 'w', encoding='utf-8', newline='').write(nl.join(uj))
    print('írva:', P)
