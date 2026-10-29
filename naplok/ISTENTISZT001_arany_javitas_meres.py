"""ISTENTISZT-001 arany lap, kis javító menet: mérések.

(1) N-F131a/b: a minősítős `jelentes_szam` és a nem üres `jelentes_hu` sorai
    (elofordulasok.tsv, ISTENTISZT-001).
(2) A/B/C tábla A-száma: a 33 sor szerepbesorolása a `funkcio` mező B-esete
    (❓ be nem sorolható, A/B/C B-eset) és a megszólított név (H1168 Baál) szerint,
    a TAHOT Károli-kulcsán. split('\t'), csak olvas.
"""
import re
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'


def tabla(ut):
    with open(ut, encoding='utf-8') as f:
        fej = None
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            yield dict(zip(fej, m))


sorok = [d for d in tabla('adat/elofordulasok.tsv') if d['id'] == ID]
print(f'== {ID}: {len(sorok)} sor')

print('== (1) minősítős jelentes_szam (zárójeles rész a kulcs után)')
for d in sorok:
    if re.search(r'\(.*\)', d['jelentes_szam']):
        print(f"  {d['igehely']}\t{d['jelentes_szam']}")
print('== (1) nem üres jelentes_hu')
for d in sorok:
    if d['jelentes_hu']:
        print(f"  {d['igehely']}\t{d['jelentes_szam']}\t{d['jelentes_hu']}")

print('== (2) B-eset (funkcio: A/B/C tipológia, B-eset)')
b_eset = [d['igehely'] for d in sorok if 'B-eset' in d['funkcio']]
print('  ', b_eset)

osz = {d['igehely'] for d in sorok}
baal = set()
with open('konkordancia/TAHOT_kivonat.tsv', encoding='utf-8') as f:
    next(f)
    for sor in f:
        m = sor.rstrip('\n').split('\t')
        if m[0] in osz and m[1] == 'H1168':
            baal.add(m[0])
print('== (2) a versben H1168 (Baál) áll:', sorted(baal))
a_eset = [d['igehely'] for d in sorok if d['igehely'] not in b_eset]
print(f'== (2) A (nem B-eset): {len(a_eset)}; ebből H1168-cal: {sorted(set(a_eset) & baal)}')

# ELLENOR_ISTENTISZT001_ARANY_JAVITAS G7: a „H1168 a versben” nem a megszólított név. A megszólított
# név a H9003 (בְּ) + H8034 (שֵׁם) utáni első nem-grammatikai token (a birtokos rag kihagyva), versenként.
KARMEL = ('1Kir 18:24', '1Kir 18:25', '1Kir 18:26')
tok = {v: [] for v in KARMEL}
with open('konkordancia/TAHOT_kivonat.tsv', encoding='utf-8') as f:
    next(f)
    for sor in f:
        m = sor.rstrip('\n').split('\t')
        if m[0] in tok:
            tok[m[0]].append((m[1], m[2], m[6]))
for v in KARMEL:
    t = tok[v]
    for i in range(len(t) - 2):
        if t[i][0] == 'H9003' and t[i + 1][0] == 'H8034':
            utana = [x for x in t[i + 2:i + 5] if not x[0].startswith('H90')][:1]
            print(f'== (2) megszólított név, {v}: {t[i + 1][1]} + {utana}')
print('== (2) jelentes_hu „Baál” az A-sorokon:',
      sorted(d['igehely'] for d in sorok if d['igehely'] in a_eset and 'Baál' in d['jelentes_hu']))
ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
print(f'proveniencia: scope=adat/elofordulasok.tsv (id={ID}, n={len(sorok)}) | '
      f"forras=elofordulasok.tsv (funkcio, jelentes_szam, jelentes_hu)+TAHOT_kivonat.tsv "
      f"(naplok/ISTENTISZT001_arany_javitas_meres.py, split('\\t')) | ts={ts}")
