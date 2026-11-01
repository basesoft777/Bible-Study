"""F152 kiejtés-mérés: a kiejtes_szoveg.elemez a két kézi forráson és a két lexikonlapon (előtte–utána).

Futtatás: python naplok/F152_kiejtes_meres.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import kiejtes_szoveg  # noqa: E402

FAJLOK = ['motivumok/ISTENTISZT-001.md', 'motivumok/ALVIL-001.md',
          'lexikon/ISTENTISZT-001_TUDOMANYOS.md', 'lexikon/ALVIL-001_TUDOMANYOS.md']

for f in FAJLOK:
    with open(os.path.join(GYOKER, f), encoding='utf-8') as fh:
        hiany = kiejtes_szoveg.elemez(fh.read())
    kezi = [h for h in hiany if h[2] == 'kézi']
    print('%s: hiány %d (kézi %d, generált %d)' % (f, len(hiany), len(kezi), len(hiany) - len(kezi)))
    for h in hiany:
        print('  sor %d | %s | %s | %s | %s | javasolt: %s' % h)
