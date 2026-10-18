"""F117.6: a fogyasztói TSK-index (lexikon_general.tsk_index, a tsk_kulcs-on át) a három E5-helyen, küszöb nélkül. Csak olvas."""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import lexikon_general as LG  # noqa: E402

idx = LG.tsk_index()
for v in ('Jón 2:3', 'Jón 2:6', 'Zsolt 42:8'):
    s = idx.get(v, [])
    print('%s: %d sor (KJV-forrás: %s) -> %s' % (
        v, len(s), sorted({o['KJV Igehely'] for o in s}),
        '; '.join('%s (%s)' % (o['Kapcsolódó igehely'], o['Votes']) for o in sorted(s, key=lambda o: -int(o['Votes'])))))
print('proveniencia: scope=Jón 2:3, Jón 2:6, Zsolt 42:8 | forras=lexikon_general.tsk_index (tsk_kulcs) | ts=2026-10-18')
