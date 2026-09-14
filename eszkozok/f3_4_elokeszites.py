# -*- coding: utf-8 -*-
"""F3.4 előkészítés: mely elofordulasok-soroknál hiányzik a karoli_szo,
és melyikhez van már meglévő join-sor / Károli-versszöveg."""
import sys, os, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tsv_sor(mezok):
    """Egy TSV-sor a csv modul nélkül — l. CLAUDE.md, „TSV-olvasás".

    A modul írója a " jelet tartalmazó mezőt körülidézi és belül duplázza, tehát
    a körútja nem bájthű; a karoli_vers oszlop tele van idézőjellel. Sorvég
    '\\n', mint a kiváltott hívás lineterminator értéke.
    """
    ki = []
    for m in mezok:
        m = '' if m is None else str(m)
        if '\t' in m or '\n' in m or '\r' in m:
            raise ValueError('elválasztó a mezőben: %r' % (m,))
        ki.append(m)
    return '\t'.join(ki) + '\n'

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
    norm_sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
for sor_s in norm_sorok[1:]:
    sor = sor_s.split('\t')
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
    karoli_sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
for sor_s in karoli_sorok[1:]:
    sor = sor_s.split('\t')
    if len(sor) >= 2:
        karoli[sor[0]] = sor[1]

# 3. meglévő join-tábla
join = {}
with open(os.path.join(ROOT, 'konkordancia', 'Karoli_Strong_kivonat.tsv'), encoding='utf-8') as f:
    join_sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
join_fejlec = join_sorok[0].split('\t')
for sor_s in join_sorok[1:]:
    mezok = sor_s.split('\t')
    if len(mezok) != len(join_fejlec):
        raise ValueError('Karoli_Strong_kivonat.tsv: %d mező a fejléc %d mezője helyett'
                          % (len(mezok), len(join_fejlec)))
    sor = dict(zip(join_fejlec, mezok))
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
    f.write(tsv_sor(['id', 'igehely', 'strong', 'gerinc_elem', 'jelentes_hu',
                     'meglevo_join', 'karoli_vers']))
    for sor in kiir:
        f.write(tsv_sor(sor))
print('Munkalap: %s' % ki)
