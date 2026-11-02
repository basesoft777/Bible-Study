"""F152.23: a DT-F152d sor (az ISTENTISZT-001 arany lap lezárása, 1. kiadás) a DONTESEK.md-be, a DT479 sora után.

CRLF-fájl: newline='' olvasás és írás; csak egy sor kerül be.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'DONTESEK.md'
SOR = ('| DT-F152d | #152 ISTENTISZT_TERV_HATRALEK (lezárás: az arany lap 1. kiadása) | Lezárható-e az ISTENTISZT-001 '
       'arany lapja most, vagy előbb a `/kiadas` lektori kérdéseire (`naplok/KIADAS_ISTENTISZT-001_lektor.md`, a '
       'lektor-felületen) kell választ adni? | (a) most lezárható, a lektori kérdések a következő kiadás bemenetei · '
       '(b) a lezárás a lektori kérdések lezárása után | (a) | ✅ | **(a) — a felhasználó döntött** (2026-11-02, az '
       'orkesztrátoron át), szó szerint: „ettől független lezárható / a lektori átnézés eredménye egy új kiadás”. '
       'Következmény: a lap 1. kiadásként lezárható; a lektori kérdések a 2. kiadás bemenetei, nem a mostani lezárás '
       'feltételei. A kolofon kiadás-sora ma nem renderelődik (N-F125a), ezért adatba nem került. | '
       '`naplok/ISTENTISZT_TERV_HATRALEK_zaras.md`; `naplok/KIADAS_ISTENTISZT-001_lektor.md` |')

with open(UT, encoding='utf-8', newline='') as f:
    sorok = f.read().split('\r\n')
idx = [i for i, s in enumerate(sorok) if s.startswith('| DT479 |')]
assert len(idx) == 1, idx
assert not any(s.startswith('| DT-F152d |') for s in sorok)
uj = sorok[:idx[0] + 1] + [SOR] + sorok[idx[0] + 1:]
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(uj))
print('beírva: DT-F152d a(z) %d. sor után' % (idx[0] + 1))
