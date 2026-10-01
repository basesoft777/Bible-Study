"""f08_nulladiff.py -- F8.8 (DT23 (d)): az ag- es a main-allapotu generalt lexikon/torzscikk kimenet osszevetese.
Hasznalat: python eszkozok/f08/f08_nulladiff.py <ag_kimenet> <main_kimenet>
(mindketto: general.py --cel lexikon/torzscikk --kimenet <konyvtar>, a repon kivul)
"""
import difflib
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

AG = os.path.join(sys.argv[1], 'lexikon')
MA = os.path.join(sys.argv[2], 'lexikon')
LD_HELYEK = ['2Móz 33:19', '2Móz 34:5', 'Ézs 12:4', 'Zsolt 116:17']


def olvas(p):
    with io.open(p, encoding='utf-8', newline='') as f:
        return f.read().splitlines()


osszes = 0
for nev in sorted(set(os.listdir(AG)) | set(os.listdir(MA))):
    a, m = os.path.join(AG, nev), os.path.join(MA, nev)
    if not (os.path.exists(a) and os.path.exists(m)):
        print('%s: csak az egyik oldalon' % nev)
        continue
    la, lm = olvas(a), olvas(m)
    diff = [d for d in difflib.unified_diff(lm, la, lineterm='', n=0)
            if d[:1] in '+-' and not d.startswith(('+++', '---'))]
    minus = [d for d in diff if d.startswith('-')]
    plus = [d for d in diff if d.startswith('+')]
    # LD001-LD004 sorai (az LXX-blokk tablasorai az adott igehelyre)
    ld_a = [s for s in la if any(s.startswith('| %s |' % h) for h in LD_HELYEK)]
    ld_m = [s for s in lm if any(s.startswith('| %s |' % h) for h in LD_HELYEK)]
    ld_ok = 'soronként azonos' if ld_a == ld_m else 'ELTER'
    print('%s: -%d/+%d sor; LD001-004 igehely-sorai: %d vs %d, %s' % (nev, len(minus), len(plus), len(ld_m), len(ld_a), ld_ok))
    osszes += len(diff)
    for d in diff:
        if 'eltérő' in d and d.startswith('+'):
            continue
        if 'kutatói azonosítás függőben' in d and d.startswith('-'):
            continue
        print('    ' + d[:220])
print('osszes diff-sor: %d' % osszes)
