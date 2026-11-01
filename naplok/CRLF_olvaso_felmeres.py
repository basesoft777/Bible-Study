"""CRLF-sérülékeny táblaolvasók felmérése (ISTENTISZT-001 arany, BDB-frissítés menete, 2026-10-29; az E19 KeyError 'illesztes' után).

Csak olvas. Egy olvasás akkor sérülékeny, ha a fájlt `newline=''`-vel nyitja (a CRLF változatlanul marad), a szöveget
`split('\\n')`-nel vágja, és a környéken (az olvasás sora és a következő 3 sor) nincs `\\r`-kezelés (`rstrip('\\r')`,
`.rstrip()`, `strip()`, `splitlines()`, `replace('\\r`). Heurisztika: a jelölt sorokat kézzel kell átnézni; a `newline=''`
nélküli nyitás (univerzális sorvég) nem sérülékeny. A kimenet fájl:sor listája.
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NYIT = re.compile(r"open\([^)]*newline=''")
VAG = re.compile(r"split\('\\n'\)")
KEZEL = re.compile(r"rstrip\('\\r'\)|rstrip\('\\r\\n'\)|\.rstrip\(\)|\.strip\(\)|splitlines\(|replace\('\\r")

talalat = []
for gy, _d, fajlok in os.walk(os.path.join(GYOKER, 'eszkozok')):
    for fn in fajlok:
        if not fn.endswith('.py'):
            continue
        ut = os.path.join(gy, fn)
        with open(ut, encoding='utf-8', errors='replace') as f:
            sorok = f.read().split('\n')
        for i, s in enumerate(sorok):
            if not VAG.search(s):
                continue
            ablak_elotte = '\n'.join(sorok[max(0, i - 2):i + 1])
            if not NYIT.search(ablak_elotte):
                continue
            ablak = '\n'.join(sorok[i:i + 4])
            if KEZEL.search(ablak):
                continue
            talalat.append((os.path.relpath(ut, GYOKER).replace(os.sep, '/'), i + 1, s.strip()[:110]))
teszt = [t for t in talalat if '/teszt_' in t[0] or '/tesztek/' in t[0]]
print('sérülékeny jelölt: %d (ebből teszt: %d)' % (len(talalat), len(teszt)))
for ut, n, s in sorted(talalat):
    print('%s:%d  %s' % (ut, n, s))
