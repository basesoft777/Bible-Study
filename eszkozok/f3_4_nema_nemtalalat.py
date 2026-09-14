# -*- coding: utf-8 -*-
"""F3.4 néma nem-találat szűrő: mely Károli-versben NEM szerepel a Strong-hoz
tartozó egyetlen ismert magyar visszaadás sem. Ezek kézi felülvizsgálatra
kerülnek — nem tölthetők ki gépileg (CLAUDE.md 3. alapszabály)."""
import sys, os, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KULCSSZAVAK = {
    'H7585': ['seol', 'sír', 'koporsó', 'pokol', 'alvilág', 'holtak orsz', 'sírverem', 'mélység'],
    'H8415': ['mélység', 'mély ', 'mélyek', 'örvény', 'hullám', 'víz-ár', 'vízár', 'fenék', 'fenékig',
              'vízáradat', 'tárház', 'mély viz', 'mélységes', 'mély ár'],
    'G0086': ['pokol', 'sír'],
    'G0012': ['mélység'],
    'H7497': ['refeus', 'refaim', 'réfaim', 'refáim', 'óriás'],
    'H7496': ['halott', 'árny', 'élet nélkül', 'meghalt', 'holtak'],
    'H5303': ['óriás'],
    'H1121+H0430': ['isten', 'fiai'],
    'H7121+H8034': ['hív', 'kiált', 'magasztal', 'nev'],
    'H3548': ['pap'],
    'H8004': ['sálem'],
    'G5010': ['rend'],
    'G5010+G0813+G0282': ['rend'],
    'G4151+G5590': ['lélek', 'lelk', 'szellem', 'valót'],
    'H5315+H2416': ['lélek', 'élő'],
}
HOSSZU = {'Jelenések': 'Jel', 'Lukács': 'Luk', 'Máté': 'Mt', 'Róma': 'Róm'}

karoli = {}
with open(os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
    karoli_sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
for sor_s in karoli_sorok[1:]:
    sor = sor_s.split('\t')
    if len(sor) >= 2:
        karoli[sor[0]] = sor[1]

with open(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'), encoding='utf-8') as f:
    sorok = [s.rstrip('\n') for s in f][1:]
fejlec = sorok[0].split('\t')
elo = [dict(zip(fejlec, s.split('\t'))) for s in sorok[1:] if s.strip()]

def verseк(igehely):
    m = re.match(r'^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$', igehely.strip())
    if not m:
        return []
    konyv = HOSSZU.get(m.group(1), m.group(1))
    fej, v1 = m.group(2), int(m.group(3))
    v2 = int(m.group(4)) if m.group(4) else v1
    return ['%s %s:%d' % (konyv, fej, v) for v in range(v1, v2 + 1)]

gyanus = []
for s in elo:
    if s['karoli_szo'].strip():
        continue
    kulcs = s['strong'].strip() or s['gerinc_elem'].strip()
    szavak = KULCSSZAVAK.get(kulcs)
    if not szavak:
        continue
    szoveg = ' '.join(karoli.get(v, '') for v in verseк(s['igehely'])).lower()
    if not szoveg.strip():
        gyanus.append((s['id'], s['igehely'], kulcs, 'NINCS KÁROLI-SOR'))
    elif not any(w in szoveg for w in szavak):
        gyanus.append((s['id'], s['igehely'], kulcs, 'nincs ismert visszaadás'))

print('Gyanús sorok (%d):' % len(gyanus))
for g in gyanus:
    print('  %-14s %-18s %-14s %s' % g)
