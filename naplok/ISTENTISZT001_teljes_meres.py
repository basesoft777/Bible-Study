"""ISTENTISZT-001 arany lap, „teljes” menet (2026-10-29): az N-F131a/b mérése.

Csak olvas. Az `elofordulasok.tsv` ISTENTISZT-001 soraiból kiírja azokat, amelyeknek a `jelentes_hu`-ja
vagy a `jelentes_szam`-a nem tiszta szójelentés / nem SEMA 2.2.2-alak, a `funkcio` és a `kapcsolodas`
mezővel együtt, hogy a szétválasztás soronként látsszon. split('\t').
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('adat/elofordulasok.tsv', encoding='utf-8', newline='') as f:
    sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
fej = sorok[0].split('\t')
ix = {n: i for i, n in enumerate(fej)}
rek = [s.split('\t') for s in sorok[1:]]
ist = [r for r in rek if r[ix['id']] == 'ISTENTISZT-001']
print('ISTENTISZT-001 sorok:', len(ist))

print('\n== jelentes_hu eloszlás ==')
szaml = {}
for r in ist:
    szaml.setdefault(r[ix['jelentes_hu']], []).append(r[ix['igehely']])
for k, v in sorted(szaml.items(), key=lambda x: -len(x[1])):
    print(f'{len(v):3}  {k!r}  ← {", ".join(v)}')

print('\n== jelentes_szam eloszlás ==')
szaml = {}
for r in ist:
    szaml.setdefault(r[ix['jelentes_szam']], []).append(r[ix['igehely']])
for k, v in sorted(szaml.items(), key=lambda x: -len(x[1])):
    print(f'{len(v):3}  {k!r}  ← {", ".join(v)}')

TISZTA = re.compile(r'^[a-záéíóöőúüű ,;]+$')
print('\n== soronként: nem a többségi jelentes_hu, vagy minősítős jelentes_szam ==')
tobbseg = max(set(r[ix['jelentes_hu']] for r in ist), key=lambda k: sum(r[ix['jelentes_hu']] == k for r in ist))
for r in ist:
    hu, sz = r[ix['jelentes_hu']], r[ix['jelentes_szam']]
    if hu != tobbseg or '(' in sz:
        print('---', r[ix['igehely']], '| strong', r[ix['strong']], '| szótár', r[ix['lexikon_szotar']])
        for m in ('jelentes_szam', 'jelentes_en', 'jelentes_hu', 'funkcio', 'kapcsolodas', 'karoli_szo'):
            print(f'   {m}: {r[ix[m]]}')
