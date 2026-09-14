# -*- coding: utf-8 -*-
"""F3.4 előkészítés: mely elofordulasok-soroknál hiányzik a karoli_szo,
és melyikhez van már meglévő join-sor / Károli-versszöveg."""
import csv, sys, os, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def olvas(ut, komment=True):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f]
    if komment and sorok and sorok[0].startswith('#'):
        sorok = sorok[1:]
    fejlec = sorok[0].split('\t')
    return fejlec, [dict(zip(fejlec, s.split('\t'))) for s in sorok[1:] if s.strip()]

# 1. normalizáló tábla: STEPBible -> magyar
norm = {}
with open(os.path.join(ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8') as f:
    r = csv.reader(f, delimiter='\t')
    next(r)
    for sor in r:
        if len(sor) >= 2:
            norm[sor[0]] = sor[1]

def step_to_hu(ig):
    m = re.match(r'^([A-Za-z0-9]+)\.(\d+)\.(\d+)', ig)
    if not m:
        return ig
    k = norm.get(m.group(1))
    if not k:
        return ig
    return '%s %s:%s' % (k, m.group(2), m.group(3))

# 2. Károli teljes szöveg
karoli = {}
with open(os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
    r = csv.reader(f, delimiter='\t')
    next(r)
    for sor in r:
        if len(sor) >= 2:
            karoli[sor[0]] = sor[1]

# 3. meglévő join-tábla
join = {}
with open(os.path.join(ROOT, 'konkordancia', 'Karoli_Strong_kivonat.tsv'), encoding='utf-8') as f:
    r = csv.DictReader(f, delimiter='\t')
    for sor in r:
        hu = step_to_hu(sor['Igehely'])
        join.setdefault((hu, sor['Strong-szám']), []).append(sor)

fej, elo = olvas(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))

hianyzo = [s for s in elo if not s['karoli_szo'].strip()]
print('Összes sor: %d | karoli_szo hiányzik: %d' % (len(elo), len(hianyzo)))

van_join = 0
nincs_vers = []
kiir = []
for s in hianyzo:
    ig = s['igehely']
    st = s['strong'].strip()
    kulcs = (ig, st)
    jsor = join.get(kulcs)
    if jsor:
        van_join += 1
    vers = karoli.get(ig)
    if vers is None:
        nincs_vers.append(ig)
    kiir.append((s['id'], ig, st, s['gerinc_elem'], s['jelentes_hu'],
                 'JOIN:' + jsor[0]['Károli-szó'] if jsor else '',
                 vers or ''))

print('Ebből meglévő join-sorból örökölhető: %d' % van_join)
print('Károli-versszöveg nincs (%d): %s' % (len(nincs_vers), ', '.join(sorted(set(nincs_vers)))))

ki = os.path.join(ROOT, 'eszkozok', 'f3_4_munkalap.tsv')
with open(ki, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['id', 'igehely', 'strong', 'gerinc_elem', 'jelentes_hu', 'meglevo_join', 'karoli_vers'])
    w.writerows(kiir)
print('Munkalap: %s' % ki)
