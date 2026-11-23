# -*- coding: utf-8 -*-
"""F239 U6 — a javítókör lekérdezései (D8, D15, D22, K9, K69, K70, K99, D4, D16, D7). Csak olvas; a kimenet a stdout-ra.
TSV: split('\\t'), csv nélkül."""
import sys, os, glob, re
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L
import teljesseg_meres as T

tahot = L.load_tahot(); tagnt = L.load_tagnt()
def tok(rows, ig): return [r for r in rows if r['Igehely'] == ig]

# motívum versei
mot = set()
for s in open(os.path.join(GY, 'adat', 'elofordulasok.tsv'), encoding='utf-8'):
    f = s.rstrip('\r\n').split('\t')
    if f[0] == 'TEREMT-001':
        ig = f[1]
        if ig == 'Jel 9:1-2': mot |= {'Jel 9:1', 'Jel 9:2'}
        else: mot.add(ig)
print('motívum versei:', len(mot))

# K69/K70/K9: a Károli-háló
k1908 = {}
for s in open(os.path.join(GY, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8'):
    f = s.rstrip('\r\n').split('\t')
    if len(f) >= 2 and f[0] != 'Igehely': k1908[f[0]] = f[1]
tabla = T.szotari_tabla(os.path.join(GY, 'adat', 'szoto', 'karoli_szotari_alak.tsv'))
lem = {'mélység', 'mély', 'mélységes', 'örvény', 'fenékig'}
halo = T.halo_karoli(lem, k1908, tabla)
print('\n[K69/K70] Károli-háló (5 lemma + előtag-tartalék):', len(halo), '| motívumvers:', len(set(halo) & mot), '| nem motívum:', len(set(halo) - mot))
csak_lemma = {v for v, szk in halo.items() if any(T.szotari_alak(sz, tabla) in lem for sz in szk)}
print('  csak a szótövező 5 lemmájával:', len(csak_lemma))
elotag = Counter(sz.lower() for v, szk in halo.items() for sz in szk if T.szotari_alak(sz, tabla) not in lem)
print('  előtag-tartalékkal illesztett alakok:', dict(elotag))
melyseg = {v for v, szk in halo.items() if any(T.szotari_alak(sz, tabla) == 'mélység' for sz in szk)}
print('[K9] a „mélység” szótári alak versei:', len(melyseg), '| a motívumon kívül:', len(melyseg - mot))
nem_mot = sorted(set(halo) - mot, key=L.parse_igehely)

# a jeloltek TEREMT-001 elutasított sorai
print('\n[K70] jeloltek.tsv TEREMT-001 elutasított sorai:')
fej = None
for s in open(os.path.join(GY, 'adat', 'jeloltek.tsv'), encoding='utf-8'):
    f = s.rstrip('\r\n').split('\t')
    if s.startswith('#'): continue
    if fej is None: fej = f; continue
    r = dict(zip(fej, f))
    if r.get('id') == 'TEREMT-001' and r.get('dontes') == 'elutasítva':
        m = re.search(r'Összesítő sor (\d+) versre', r.get('indoklas', ''))
        halo_nev = 'karoli' if 'Károli-szó háló' in r.get('forras_kereses', '') else ('lxx' if 'LXX-többlet' in r.get('forras_kereses', '') else ('szotar' if 'szótár' in r.get('forras_kereses', '').lower() else 'egyedi'))
        print('  %-12s %-7s n=%-3s %s' % (r['igehely'], halo_nev, m.group(1) if m else '1', r.get('indoklas', '')[:90]))

# D22: a Septuaginta többlete
print('\n[D22] LXX ἄβυσσος-vers, a héberben H8415 nélkül:')
h8415 = {r['Igehely'] for r in tahot if r['Strong-szám'] == 'H8415'}
lxx = defaultdict(list)
for ut in sorted(glob.glob(os.path.join(GY, 'konkordancia', 'LXX_OS', '*.tsv'))):
    fejl = None
    for s in open(ut, encoding='utf-8'):
        if s.startswith('#'): continue
        m = s.rstrip('\r\n').split('\t')
        if fejl is None: fejl = {n: i for i, n in enumerate(m)}; continue
        if 'lemma' not in fejl: break
        lxx[m[fejl['igehely_karoli']]].append((m[fejl['lemma']], m[fejl['szoalak']]))
tobblet = sorted([v for v, sz in lxx.items() if any(l == 'ἄβυσσος' for l, _ in sz) and v and v not in h8415], key=L.parse_igehely)
for v in tobblet:
    heb = ' '.join('%s(%s)' % (r['Strong-szám'], r['Kiejtés']) for r in tok(tahot, v) if r['Strong-szám'] in ('H4688', 'H6683', 'H7338', 'H7341'))
    print('  %s | héber mélység-szó: %s | a Károli-hálóban: %s' % (v, heb or '-', 'igen' if v in halo else 'nem'))
print('  n=%d' % len(tobblet))

# D15: a hét vers görög szövege (ἄβυσσος + καταβαίνω/ἀνάγω)
print('\n[D15] a hét vers: a lemma-sor')
for v in ['Ez 26:19', 'Ez 31:15', 'Jób 36:16', 'Jób 38:30', 'Zsolt 71:20', 'Zsolt 71:21', 'Zsolt 107:26']:
    print('  %s: %s' % (v, ' '.join(a for _, a in lxx.get(v, []))))

# K99: kollokáció
print('\n[K99] H8415 + H4599 (forrás) egy versben:', sorted({r['Igehely'] for r in tahot if r['Strong-szám'] == 'H4599'} & h8415, key=L.parse_igehely))
print('      H8415 + H5869 (forrás/szem) egy versben:', sorted({r['Igehely'] for r in tahot if r['Strong-szám'] == 'H5869'} & h8415, key=L.parse_igehely))

# D8: nagy mélység
print('\n[D8] H8415 + H7227 egy versben:', sorted({r['Igehely'] for r in tahot if r['Strong-szám'] == 'H7227'} & h8415, key=L.parse_igehely))
for v in ['Zsolt 78:15']:
    print('  %s: %s' % (v, ' | '.join('%s %s %s' % (r['Strong-szám'], r['Kiejtés'], r['Angol tükörfordítás']) for r in tok(tahot, v))))

# D4: Jel 20:3
print('\n[D4] Jel 20:3 (TAGNT):')
for r in tok(tagnt, 'Jel 20:3'):
    print('  %s %s %s | %s | krit: %s' % (r['Strong-szám'], r['Ragozott alak'], r['Kiejtés'], r['Angol tükörfordítás'], r['Kritikai kiadás']))

# D7: Jón 2:6, 2:7
for v in ['Jón 2:6', 'Jón 2:7']:
    print('\n[D7] %s: %s' % (v, ' | '.join('%s %s' % (r['Strong-szám'], r['Angol tükörfordítás']) for r in tok(tahot, v))))

# D16: 2Móz 15 — a tenger szava a mélység mellett
for v in ['2Móz 15:4', '2Móz 15:5', '2Móz 15:8', '2Móz 15:10']:
    print('\n[D16] %s: %s' % (v, ' | '.join('%s %s' % (r['Strong-szám'], r['Angol tükörfordítás']) for r in tok(tahot, v))))

# D20: a kulcs és a nyit–zár a Jelenések könyvében
for s, nev in [('G2807', 'kulcs'), ('G0455', 'megnyit'), ('G2808', 'bezár')]:
    v = sorted({r['Igehely'] for r in tagnt if r['Strong-szám'] == s and r['Igehely'].startswith('Jel ')}, key=L.parse_igehely)
    print('\n[D20] %s %s a Jelenésekben: %d vers: %s' % (s, nev, len(v), ', '.join(v)))
