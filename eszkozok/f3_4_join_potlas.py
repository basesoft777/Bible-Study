# -*- coding: utf-8 -*-
"""F3.4 — a Karoli-Strong join visszamenoleges potlasa (ATALAKITASI_TERV 4.7 / F3.4).

Harom tablat ir:
  1. adat/elofordulasok.tsv   — karoli_szo + azonositas_modja + megbizhatosag triplet
  2. adat/jeloltek.tsv        — ugyanaz a triplet a beepitve sorokon (SEMA 2.2: innen orokloedik);
                                egyben javitja az F3.1 betolto oszlop-eltolodasat
  3. konkordancia/Karoli_Strong_kivonat.tsv — uj join-sorok

Forras: naplok/f3_4_dontesek.tsv (soronkenti, tartalom-alapu itelet) es
        naplok/f3_4_extra_join.tsv (egy igehelyhez tobb Strong / tartomany tovabbi versei).
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Az elofordulasok.tsv nehany helyen teljes konyvnevet hasznal; a Karoli_1908.tsv
# es a Konyv_normalizalo_tabla.tsv viszont a rovid alakot — normalizalas nelkul
# nema nem-talalat keletkezne (CLAUDE.md, igehely-formatum).
HOSSZU = {
    'Jelenések': 'Jel',
    'Lukács': 'Luk',
    'Máté': 'Mt',
    'Róma': 'Róm',
}

FORRAS_STUDY = {
    'KIRALY-001': 'Melkizedek_tematikus.md',
    'ISTENTISZT-001': 'Segitsegul_hivni_az_Urat_tematikus.md',
    'TEREMT-001': 'Tehom_tematikus.md',
    'ALVIL-001': 'Hadesz_Seol_tematikus.md',
    'MENNY-001': 'Isten_fiai_Nefilim_Gibborim_tematikus.md',
    'ANTROP-001': 'Pneuma_pszukhe_megkulonboztetes_tematikus.md',
    'HODIT-001': 'Rafaim_tematikus.md',
}

BEEPITVE = 'beépítve'  # "beepitve" ekezetesen


def olvas(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f]
    komment = sorok[0] if sorok[0].startswith('#') else None
    if komment:
        sorok = sorok[1:]
    fej = sorok[0].split('\t')
    adat = [s.split('\t') for s in sorok[1:] if s.strip()]
    return komment, fej, adat


def olvas_dict(ut):
    """TSV-olvasás szótár-sorokkal a csv modul nélkül — l. CLAUDE.md, „TSV-olvasás"."""
    with open(ut, encoding='utf-8') as f:
        sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
    fej = sorok[0].split('\t')
    ki = []
    for i, s in enumerate(sorok[1:], start=2):
        mezok = s.split('\t')
        if len(mezok) != len(fej):
            raise ValueError('%s %d. sor: %d mező a fejléc %d mezője helyett'
                              % (ut, i, len(mezok), len(fej)))
        ki.append(dict(zip(fej, mezok)))
    return ki


def ir(ut, komment, fej, adat):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        if komment:
            f.write(komment + '\n')
        f.write('\t'.join(fej) + '\n')
        for s in adat:
            f.write('\t'.join(s) + '\n')


def tisztit(szoveg):
    """A karoli_szo-bol a zarojeles gorog/heber magyarazatot elhagyja a join-tablahoz."""
    return re.sub(r'\s*\([^)]*\)', '', szoveg).strip()


# --- dontes-tabla ---
dontesek = {(d['id'], d['igehely']): d
            for d in olvas_dict(os.path.join(ROOT, 'naplok', 'f3_4_dontesek.tsv'))}

# --- 1. elofordulasok.tsv ---
ut = os.path.join(ROOT, 'adat', 'elofordulasok.tsv')
kom, fej, adat = olvas(ut)
I = {n: i for i, n in enumerate(fej)}
irt = strong_potolt = 0
for s in adat:
    d = dontesek.get((s[I['id']], s[I['igehely']]))
    if not d or s[I['karoli_szo']].strip():
        continue
    s[I['karoli_szo']] = d['karoli_szo']
    s[I['azonositas_modja']] = d['azonositas_modja']
    s[I['megbizhatosag']] = d['megbizhatosag']
    irt += 1
    # a gerinc_elem-ben megnevezett Strong atemelese az ures strong oszlopba
    if not s[I['strong']].strip():
        g = s[I['gerinc_elem']].strip()
        if re.match(r'^[HG]\d{4}$', g):
            s[I['strong']] = g
            strong_potolt += 1
ir(ut, kom, fej, adat)
print('elofordulasok.tsv: %d sor kapott karoli_szo tripletet, %d sor strong-potlast'
      % (irt, strong_potolt))

# --- 2. jeloltek.tsv ---
ut = os.path.join(ROOT, 'adat', 'jeloltek.tsv')
kom, fej, adat = olvas(ut)
J = {n: i for i, n in enumerate(fej)}
_, fe, ea = olvas(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))
E = {n: i for i, n in enumerate(fe)}
eidx = {(s[E['id']], s[E['igehely']]): s for s in ea}

javitott = feltoltott = 0
for s in adat:
    e = eidx.get((s[J['id']], s[J['igehely']]))
    if not e:
        continue
    # (a) F3.1 oszlop-eltolodas javitasa: a karoli_szo oszlopban jelentes_hu all
    if s[J['karoli_szo']] and s[J['karoli_szo']] == e[E['jelentes_hu']]:
        s[J['karoli_szo']] = ''
        s[J['azonositas_modja']] = ''
        s[J['megbizhatosag']] = ''
        javitott += 1
    # (b) triplet oroklese az elofordulasok-bol
    if s[J['dontes']] == BEEPITVE and e[E['karoli_szo']].strip():
        s[J['karoli_szo']] = e[E['karoli_szo']]
        s[J['azonositas_modja']] = e[E['azonositas_modja']]
        s[J['megbizhatosag']] = e[E['megbizhatosag']]
        feltoltott += 1
ir(ut, kom, fej, adat)
print('jeloltek.tsv: %d eltolt sor javitva, %d sor kapott tripletet' % (javitott, feltoltott))

# --- 3. Karoli_Strong_kivonat.tsv ---
norm = {}
with open(os.path.join(ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8') as f:
    norm_sorok = [ln.rstrip('\n').rstrip('\r') for ln in f if ln.strip()]
for sor_s in norm_sorok[1:]:
    sor = sor_s.split('\t')
    if len(sor) >= 2:
        norm[sor[1]] = sor[0]


def hu_to_step(ig):
    m = re.match(r'^(.+?)\s+(\d+):(\d+)$', ig.strip())
    if not m:
        return None
    konyv = HOSSZU.get(m.group(1), m.group(1))
    k = norm.get(konyv)
    return '%s.%s.%s' % (k, m.group(2), m.group(3)) if k else None


szotar = {}
for sor in olvas_dict(os.path.join(ROOT, 'konkordancia', 'Strong_szotar.tsv')):
    szotar[sor['Strong-szám']] = (
        sor['Szófaj'],
        sor['Gyök/Származtatás'])

ut = os.path.join(ROOT, 'konkordancia', 'Karoli_Strong_kivonat.tsv')
with open(ut, encoding='utf-8') as f:
    jsorok = [s.rstrip('\n') for s in f]
jfej = jsorok[0].split('\t')
jadat = [s.split('\t') for s in jsorok[1:] if s.strip()]
letezo = set((s[0], s[1]) for s in jadat)

ujak = []
hibak = []


def felvesz(igehely_hu, strong, karoli_szo, azon, megbiz, motivum_id):
    step = hu_to_step(igehely_hu)
    if not step:
        hibak.append('NORMALIZALAS_SIKERTELEN: ' + igehely_hu)
        return
    if (step, strong) in letezo:
        return
    szofaj, gyok = szotar.get(strong, ('', ''))
    ujak.append([step, strong, karoli_szo, azon, FORRAS_STUDY[motivum_id], megbiz, szofaj, gyok])
    letezo.add((step, strong))


for d in dontesek.values():
    if not d['join_igehely'].strip():
        continue
    felvesz(d['join_igehely'], d['join_strong'], tisztit(d['karoli_szo']),
            d['azonositas_modja'], d['megbizhatosag'], d['id'])

extra = os.path.join(ROOT, 'naplok', 'f3_4_extra_join.tsv')
if os.path.exists(extra):
    for d in olvas_dict(extra):
        felvesz(d['igehely'], d['strong'], d['karoli_szo'],
                d['azonositas_modja'], d['megbizhatosag'], d['id'])

jadat.extend(ujak)
with open(ut, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\t'.join(jfej) + '\n')
    for s in jadat:
        f.write('\t'.join(s) + '\n')
print('Karoli_Strong_kivonat.tsv: %d uj sor (osszesen %d)' % (len(ujak), len(jadat)))
if hibak:
    print('HIBAK:')
    for h in hibak:
        print('   ' + h)
