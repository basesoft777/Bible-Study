# -*- coding: utf-8 -*-
"""F3.4 munkalap: minden karoli_szo nélküli elofordulasok-sorhoz a Károli-versszöveg.
Könyvnév-normalizálás és versintervallum-kibontás kötelező (CLAUDE.md: néma nem-találat)."""
import sys, os, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# az elofordulasok.tsv-ben előforduló hosszú könyvnevek -> Karoli_1908.tsv rövidítés
HOSSZU = {'Jelenések': 'Jel', 'Lukács': 'Luk', 'Máté': 'Mt', 'Róma': 'Róm',
          'Márk': 'Mk', 'János': 'Ján', 'Cselekedetek': 'ApCsel'}

def olvas_tsv(ut, komment=True):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f]
    if komment and sorok and sorok[0].startswith('#'):
        sorok = sorok[1:]
    fejlec = sorok[0].split('\t')
    return fejlec, [dict(zip(fejlec, s.split('\t'))) for s in sorok[1:] if s.strip()]

karoli = {}
with open(os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
    karoli_sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
for sor_s in karoli_sorok[1:]:
    sor = sor_s.split('\t')
    if len(sor) >= 2:
        karoli[sor[0]] = sor[1]

def bont(igehely):
    """'Jelenések 20:1-3' -> [('Jel 20:1', szoveg), ...]; hiányzót None-nal jelöl."""
    m = re.match(r'^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$', igehely.strip())
    if not m:
        return None, [(igehely, None)]
    konyv, fej, v1, v2 = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    konyv = HOSSZU.get(konyv, konyv)
    vegso = int(v2) if v2 else v1
    ki = []
    for v in range(v1, vegso + 1):
        kulcs = '%s %s:%d' % (konyv, fej, v)
        ki.append((kulcs, karoli.get(kulcs)))
    return konyv, ki

fej, elo = olvas_tsv(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))
hianyzo = [s for s in elo if not s['karoli_szo'].strip()]

nemtalalt = []
ki = os.path.join(ROOT, 'eszkozok', 'f3_4_munkalap.txt')
with open(ki, 'w', encoding='utf-8', newline='\n') as f:
    for s in hianyzo:
        konyv, reszek = bont(s['igehely'])
        f.write('### %s | %s | strong=%s | gerinc=%s\n' % (s['id'], s['igehely'], s['strong'], s['gerinc_elem']))
        if s['jelentes_hu'].strip():
            f.write('    jelentés: %s\n' % s['jelentes_hu'][:160])
        for kulcs, szoveg in reszek:
            if szoveg is None:
                nemtalalt.append((s['id'], s['igehely'], kulcs))
                f.write('    [%s] *** NINCS KÁROLI-SOR ***\n' % kulcs)
            else:
                f.write('    [%s] %s\n' % (kulcs, szoveg))
        f.write('\n')

print('Munkalap: %s (%d sor)' % (ki, len(hianyzo)))
print('Néma nem-találat (%d):' % len(nemtalalt))
for a in nemtalalt:
    print('   %s | %s -> %s' % a)
