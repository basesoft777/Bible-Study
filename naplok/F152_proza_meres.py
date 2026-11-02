"""F152.17 mérés: a próza számai a 22 soros ISTENTISZT-001-en (a K1–K5 és a DT-F152b átvezetése után).

- LXX: hány ószövetségi helyen áll ἐπικαλέω (G1941) a görög versben;
- az „oltár” (H4196) és a כֹּל (H3605) a héber helyeken, a πᾶς (G3956) az újszövetségieken.
Csak olvas; split('\t').
"""
import glob
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'


def sorok(ut):
    with open(ut, encoding='utf-8') as f:
        for s in f:
            if s.startswith('#') or not s.strip():
                continue
            yield s.rstrip('\r\n').split('\t')


helyek = [m[1] for m in sorok('adat/elofordulasok.tsv') if m[0] == ID]
tahot, tagnt = {}, {}
for m in sorok('konkordancia/TAHOT_kivonat.tsv'):
    tahot.setdefault(m[0], set()).add(m[1])
for m in sorok('konkordancia/TAGNT_kivonat.tsv'):
    tagnt.setdefault(m[0], set()).add(m[1])
osz = [h for h in helyek if h in tahot]
usz = [h for h in helyek if h in tagnt]
print('helyek: %d (ÓSZ %d, ÚSZ %d)' % (len(helyek), len(osz), len(usz)))

lxx = {}
for ut in glob.glob('konkordancia/LXX_OS/*.tsv'):
    fej = None
    for m in sorok(ut):
        if fej is None:
            fej = m
            continue
        d = dict(zip(fej, m))
        if d.get('igehely_karoli') in osz:
            lxx.setdefault(d['igehely_karoli'], set()).add(d['strong'])
eg = [h for h in osz if '1941' in lxx.get(h, set())]
print('LXX G1941: %d / %d; nem: %s' % (len(eg), len(osz), [h for h in osz if h not in eg]))
print('H4196 (oltár):', [h for h in osz if 'H4196' in tahot[h]])
print('H3605 (kol):', [h for h in osz if 'H3605' in tahot[h]])
print('G3956 (pász):', [h for h in usz if 'G3956' in tagnt[h]])
