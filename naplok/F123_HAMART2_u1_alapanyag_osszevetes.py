# -*- coding: utf-8 -*-
"""F123 HAMART-001 U1 — az alapanyag-kivonat igehelyeinek gépi összevetése az adatréteggel.

Bemenet: a régi tanulmány és kereszthivatkozás-napló igehely-említései (sorszámmal), az adat/elofordulasok.tsv és
az adat/jeloltek.tsv HAMART-001-sorai (versre bontva). Kimenet: naplok/F123_alapanyag_HAMART-001_elteres.tsv,
összegzés a konzolra. Csak olvas; adattáblát nem ír. TSV: split('\\t'), '\\t'.join(); csv modul nincs."""
import importlib.util
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
spec = importlib.util.spec_from_file_location('keszito', os.path.join(GY, 'naplok', 'F123_adat_keszito.py'))
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)
L = K.L

MID = 'HAMART-001'
S = 'tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md'
N = 'tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md'
TS = '2026-11-03'


def sorok(path):
    return open(os.path.join(GY, path), encoding='utf-8').read().split('\n')


_ver_cache = {}


def versre(ig):
    if ig not in _ver_cache:
        _ver_cache[ig] = K.versre(ig)
    return _ver_cache[ig]


CF = re.compile(r'\s*[,;]\s*(\d+):(\d+)((?:\s*[-–]\s*\d+)?)')


def emlites_lista(sor, rx):
    """K.emlitesek + a folytatólagos ', f:v' alak (azonos könyv); a ', N szavazat' alakú számadat kiszűrve."""
    sor = re.sub(r'[,;]?\s*\d+(?:[-–]\d+)?\s*szavazat', '', sor)
    ki = list(K.emlitesek(sor, rx))
    for m in rx.finditer(sor):
        konyv = K.KONYV_ALIAS.get(m.group(1), m.group(1))
        pos = m.end()
        while True:
            c = CF.match(sor, pos)
            if not c:
                break
            ki.append('%s %s:%s%s' % (konyv, c.group(1), c.group(2), c.group(3).replace(' ', '')))
            pos = c.end()
    return ki


def kontextus(forras, n, sor):
    """A sor szerepe a forrásban (a sorszám-tartomány és a döntésjelölés szerint)."""
    if forras == S:
        if 62 <= n <= 121:
            return 'tanulmány-tábla (beépített)'
        return 'tanulmány-próza'
    if 146 <= n <= 168:
        return 'napló 4/a (BEÉPÍTVE)'
    if 176 <= n <= 202:
        if 'NYITVA' in sor:
            return 'napló 4/b (NYITVA HAGYVA)'
        if 'részben' in sor:
            return 'napló 4/b (vegyes)'
        if 'ELUTASÍTVA' in sor:
            return 'napló 4/b (ELUTASÍTVA)'
        if 'BEÉPÍTVE' in sor:
            return 'napló 4/b (BEÉPÍTVE)'
        return 'napló 4/b (vegyes)'
    if 208 <= n <= 220:
        return 'napló 4/c (elutasított gerinc-scan)'
    if 242 <= n <= 252:
        return 'napló 6 (összegzés)'
    return 'napló (egyéb említés)'


def main():
    rx = K.igehely_re()
    E, J = defaultdict(set), defaultdict(set)
    for fn, cel in (('adat/elofordulasok.tsv', E), ('adat/jeloltek.tsv', J)):
        fej = None
        for s in open(os.path.join(GY, fn), encoding='utf-8'):
            if s.startswith('#'):
                continue
            c = s.rstrip('\n').split('\t')
            if fej is None:
                fej = c
                continue
            d = dict(zip(fej, c))
            if d.get('id') != MID:
                continue
            for v in versre(d['igehely']):
                cel[v].add(d.get('dontes', 'E') if fn.endswith('jeloltek.tsv') else 'E')

    talalat = defaultdict(list)  # vers -> [(forras, sor, kontextus)]
    for forras in (S, N):
        for i, sor in enumerate(sorok(forras), 1):
            for ig in emlites_lista(sor, rx):
                for v in versre(ig):
                    talalat[v].append((forras, i, kontextus(forras, i, sor)))

    sorrend = {'tanulmány-tábla (beépített)': 0, 'napló 4/a (BEÉPÍTVE)': 1, 'napló 4/b (BEÉPÍTVE)': 2}
    ki = []
    osszeg = defaultdict(int)
    for v, hely in sorted(talalat.items()):
        if v in E:
            allapot = 'E'
        elif v in J:
            allapot = 'J:' + '/'.join(sorted(J[v]))
        else:
            allapot = 'NINCS'
        kontx = sorted({h[2] for h in hely}, key=lambda x: (sorrend.get(x, 9), x))
        beepitett = any(k in sorrend for k in kontx)
        osztaly = ('beépítettnek mondott' if beepitett else
                   'napló-elutasítás/nyitva' if any('ELUTAS' in k or 'NYITVA' in k or '4/c' in k for k in kontx) else
                   'egyéb említés')
        osszeg[(osztaly, allapot.split(':')[0] if allapot != 'NINCS' else 'NINCS')] += 1
        ki.append([v, allapot, osztaly, '; '.join(kontx),
                   '; '.join('%s:%d' % ('S' if h[0] == S else 'N', h[1]) for h in hely[:8]) + (' …' if len(hely) > 8 else '')])

    p = os.path.join(GY, 'naplok', 'F123_alapanyag_%s_elteres.tsv' % MID)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_HAMART2_u1_alapanyag_osszevetes.py | scope=%s (%d vers-említés) × adat/elofordulasok.tsv + adat/jeloltek.tsv (%s) | forras=split(\'\\t\'), %s, %s | ts=%s\n'
                % (MID, len(talalat), MID, S, N, TS))
        f.write('igehely\tallapot_az_adatban\tosztaly\tkontextus\tforras_sor\n')
        for r in ki:
            f.write('\t'.join(r) + '\n')

    print('említett vers:', len(talalat))
    for k, n in sorted(osszeg.items()):
        print('%-28s %-8s %d' % (k[0], k[1], n))
    e_nem_emlitett = sorted(v for v in E if v not in talalat)
    print('E-vers, amelyet a két forrás nem említ (igehely-formában):', len(e_nem_emlitett), ' '.join(e_nem_emlitett))


if __name__ == '__main__':
    main()
