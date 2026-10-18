"""F117 4.1 előtti mérés (naplok/F117_tabla_allapot_meres.py): az A–D′ osztály sorai a táblában és a KK1b-tervezetben. Csak olvas."""
import sys
import re
import os
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
TERV = os.path.join(ROOT, 'naplok', 'KAROLI_KK1b_kulcstabla_tervezet.tsv')
KAROLI = os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv')
KJV = os.path.join(ROOT, 'konkordancia', 'KJV_Strongs_teljes.tsv')


def olvas(path):
    with open(path, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    adat = [s for s in sorok if s and not s.startswith('#')]
    fej = adat[0].split('\t')
    out = defaultdict(list)
    for s in adat[1:]:
        p = s.split('\t')
        out[p[0]].append(p)
    return fej, out


_, tabla = olvas(TABLA)
_, terv = olvas(TERV)

VERS = re.compile(r'^(.+) (\d+):(\d+)$')
karoli_fej = defaultdict(list)
with open(KAROLI, encoding='utf-8') as f:
    f.readline()
    for s in f:
        p = s.rstrip('\n').split('\t')
        m = VERS.match(p[0])
        if m:
            karoli_fej[(m.group(1), int(m.group(2)))].append(int(m.group(3)))

# KJV fejezetméret (az első oszlop formátumát nézzük)
with open(KJV, encoding='utf-8') as f:
    kjv_fej_sor = f.readline().rstrip('\n')
    kjv_minta = [f.readline().rstrip('\n')[:120] for _ in range(2)]
print('KJV fejléc:', kjv_fej_sor[:200])
print('KJV minta:', kjv_minta)

A = [('2Móz', 35), ('2Móz', 36), ('Dán', 3), ('Hós', 2), ('Hós', 13), ('Hós', 14), ('Jób', 17),
     ('Jób', 37), ('Péld', 12), ('Én', 5), ('Én', 6), ('Ézs', 4), ('Ézs', 64)]

print('\n== A — hiányzó fejezet ==')
osszA = Counter()
for k, c in A:
    vv = sorted(karoli_fej[(k, c)])
    ig = ['%s %d:%d' % (k, c, v) for v in vv]
    n_t = sum(1 for i in ig if i in tabla)
    n_tv = sum(1 for i in ig if i in terv)
    # van-e a fejezetre bármilyen sor (pl. más Károli-fejezetből ide mutató KJV)
    pref = '%s %d:' % (k, c)
    tv_any = [i for i in terv if i.startswith(pref)]
    osszA['karoli_vers'] += len(vv)
    osszA['tablaban'] += n_t
    osszA['tervezetben'] += n_tv
    print('%s %d: Károli %d vers | táblában %d | tervezetben %d %s' % (
        k, c, len(vv), n_t, n_tv, '' if not tv_any else '(tervezet-kulcsok: %d)' % len(tv_any)))
print('A összesen:', dict(osszA))


def mutat(cimke, igek):
    print('\n== %s ==' % cimke)
    forr = Counter()
    for i in igek:
        t = tabla.get(i)
        tv = terv.get(i)
        ts = ' | '.join('kjv=%s mt=%s %s/%s %s' % (p[1], p[2], p[3], p[4], p[5][:40]) for p in t) if t else 'NINCS SOR'
        tvs = ('%d sor: ' % len(tv)) + ' ; '.join('%s/%s kjv=%s' % (p[3], p[4], p[1]) for p in tv) if tv else 'NINCS SOR'
        print('  %-12s tábla: %s || tervezet: %s' % (i, ts, tvs))
        forr[(t[0][3] + '|' + t[0][4]) if t else 'nincs_sor'] += 1
    print('  osztály|forrás a táblában:', dict(forr))
    return forr


B = ['Préd 9:%d' % v for v in (21, 22, 23)] + ['Jób 39:%d' % v for v in range(34, 39)]
mutat('B — KEZI üres KJV', B)
C = ['Dán 3:%d' % v for v in range(30, 34)] + ['Dán 4:1', 'Dán 4:37']
mutat('C — Dán 3:31–33 (+ szomszédok)', C)
print('  Károli Dán 3 versszám:', len(karoli_fej[('Dán', 3)]), '| Dán 4:', len(karoli_fej[('Dán', 4)]))

D = {}
D['1Kir 22'] = ['1Kir 22:%d' % v for v in list(range(46, 50)) + [54]]
D['Ézs 3'] = ['Ézs 3:%d' % v for v in sorted(karoli_fej[('Ézs', 3)])]
D['Jón 2'] = ['Jón 2:%d' % v for v in sorted(karoli_fej[('Jón', 2)])]
D['1Sám 24'] = ['1Sám 24:%d' % v for v in sorted(karoli_fej[('1Sám', 24)])]
D['1Sám 20'] = ['1Sám 20:43']
osszD = Counter()
for nev, igek in D.items():
    f = mutat('D — %s (Károli %d vers)' % (nev, len(igek)), igek if len(igek) < 12 else igek[:3] + igek[-3:])
    for i in igek:
        t = tabla.get(i)
        osszD[(t[0][3] + '|' + t[0][4]) if t else 'nincs_sor'] += 1
print('\nD összes (teljes fejezetek):', dict(osszD))

Dv = ['1Kir 22:%d' % v for v in list(range(43, 46)) + list(range(50, 54))]
mutat('D′ — tvtms szomszédok', Dv)

# Többsoros tervezet-kulcsok az érintett halmazon: hány esik a KK4 választási szabálya alá
print('\nTervezet: többsoros Károli-kulcsok összesen:', sum(1 for k, v in terv.items() if len(v) > 1))
