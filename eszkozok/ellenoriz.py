#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ellenoriz.py -- F8.5: az `adat/SEMA.md` 3. szakaszának (Integritási
szabályok) gepi kikenyszeritese, plusz a Minosegi kapu gepi resze
(Q1, Q7) egy megadott study-fajlra (F8_BRIEF.md G4).

Hatokor (G4):
  - SEMA §3 1-6. es 8. szabalya KIKENYSZERITVE (a jelentes kilepesi kodot ad).
  - a 7. szabaly a `gate.py` collision_report/pair_overlap_report/
    subset_report fuggvenyeit hivja meg -- JELENTES, a kilepesi kodot
    nem befolyasolja.
  - `--study FILE` (ismetelheto): Q1 (szerkezeti teljesseg) es Q7
    (dataset-lefedettseg arra a motivumra, amelynek forras_study-ja a
    fajlt tartalmazza) gepi; Q2-Q6 mindig KEZI, soha nem "megfelelt".

N12: a 8. szabaly motivumszintu -- a nyomot az `adat/auditok.tsv` (l.
SEMA.md 2.9) es az `elofordulasok.tsv` proveniencia-mezoi egyutt adjak,
a `forras` kulcs `+` menten bontott fajlnevei, PONTOS egyezessel (a regi
reszsztring-illesztes hibaja megszunt). Ket jelentessorra bomlik: "8.
Dataset-lefedettseg (gepi)" es "8/c. Kezi dataset-lefedettseg" -- l.
LEKERDEZO_NELKULI es RETROAKTIV_IDK lent.

CLI:
    python eszkozok/ellenoriz.py [--adat DIR] [--study FILE ...] [--md FILE]

Kilepesi kod: 0 = rendben, 1 = szabalysertes, 2 = hiba.
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G
import gate as GATE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')

PROVENIENCIA_KOTELEZO_KULCSOK = {'scope', 'forras', 'ts'}
PROVENIENCIA_MEGENGEDETT_TOVABBI_KULCSOK = {'strong', 'n'}
PROVENIENCIA_TILTOTT_KULCSOK = {'talalat', 'strong_vart'}

# N12/G4: azok a `mindig` tematikus datasetek, amelyekhez nincs `lekerdez.py`
# parancs -- a lefedettsegük mindig KEZI ("nincs lekérdező"), minden ID-nel.
# Ha egyszer lesz `lekerdez.py bdb`, a fajlnev kikerul a halmazbol.
LEKERDEZO_NELKULI = {'BDB_teljes_unabridged.tsv'}

# N12/G3: a `6e3fd43`-ban F3-betoltessel retroaktivan bekerult 7 motivum
# ID-jenek ZART listaja, N14/G1-gyel a HAMART-001-gyel 8-ra bovitve (a
# study 2026.09.11-i megirasakor a lekerdez.py meg nem letezett -- F2:
# 2026.09.14 --, tehat a HAMART-001 ugyanabba az osztalyba tartozik, mint
# a masik het retroaktiv ID). A retroaktiv motivumok hianyzo datasetjei
# KEZI jelentest kapnak ("retroaktiv, F3"), nem SÉRTÉST -- de a lista NEM
# bovul automatikusan ("nincs auditok-sora -> retroaktiv" eppen az uj,
# elfelejtett rogzitesu motivumot rejtene el, l. N12_BRIEF.md G3).
RETROAKTIV_IDK = {
    'ALVIL-001', 'ANTROP-001', 'HAMART-001', 'HODIT-001', 'ISTENTISZT-001',
    'KIRALY-001', 'MENNY-001', 'TEREMT-001',
}


class Sor(object):
    """Egy jelentes-sor: verdict = RENDBEN | SÉRTÉS | KÉZI | JELENTÉS."""

    def __init__(self, cim, verdict, n=None, peldak=None, megjegyzes=None):
        self.cim = cim
        self.verdict = verdict
        self.n = n
        self.peldak = peldak or []
        self.megjegyzes = megjegyzes

    def sor_szoveg(self):
        fej = '**%s**: %s' % (self.cim, self.verdict)
        if self.n is not None:
            fej += ' (%d)' % self.n
        if self.megjegyzes:
            fej += ' -- %s' % self.megjegyzes
        sorok = [fej]
        for p in self.peldak[:10]:
            sorok.append('  - %s' % p)
        if self.n is not None and self.n > 10:
            sorok.append('  - ... és további %d' % (self.n - 10))
        return '\n'.join(sorok)


def proveniencia_parse(ertek):
    """{kulcs: ertek} -- a ' | ' tagolt 'kulcs=ertek' parok. Ures/rossz
    alaknal ures dict (a hivo dontse a hibat)."""
    if not ertek or not ertek.strip():
        return {}
    ki = {}
    for resz in ertek.split('|'):
        resz = resz.strip()
        if '=' not in resz:
            return {}
        k, v = resz.split('=', 1)
        ki[k.strip()] = v.strip()
    return ki


def proveniencia_ervenyes(ertek):
    """True, ha a proveniencia-sor megfelel G9-nek (kotelezo scope/forras/ts,
    megengedett tovabbi strong/n, tiltott talalat/strong_vart)."""
    kulcsok = proveniencia_parse(ertek)
    if not kulcsok or not PROVENIENCIA_KOTELEZO_KULCSOK.issubset(kulcsok):
        return False
    if set(kulcsok) & PROVENIENCIA_TILTOTT_KULCSOK:
        return False
    if not set(kulcsok).issubset(
            PROVENIENCIA_KOTELEZO_KULCSOK | PROVENIENCIA_MEGENGEDETT_TOVABBI_KULCSOK):
        return False
    return True


def forras_fajlok(proveniencia):
    """set -- a proveniencia `forras` kulcsa `+` menten bontva, strip-pel.
    Ervenytelen sornal (proveniencia_parse ures dict-et ad) ures halmaz."""
    kulcsok = proveniencia_parse(proveniencia)
    forras = kulcsok.get('forras', '')
    if not forras:
        return set()
    return {r.strip() for r in forras.split('+') if r.strip()}


# ---------------------------------------------------------------------------
# SEMA §3 tabla-szabalyok
# ---------------------------------------------------------------------------

def szabaly1_hivatkozasi_epseg(motivum_id_halmaz, elofordulasok, kapcsolatok, jeloltek, auditok):
    hibas = []
    for sor in elofordulasok:
        if sor['id'] not in motivum_id_halmaz:
            hibas.append('elofordulasok: %s / %s' % (sor['id'], sor['igehely']))
    for sor in kapcsolatok:
        if sor['id'] not in motivum_id_halmaz:
            hibas.append('kapcsolatok: %s / %s -> %s' % (
                sor['id'], sor['forras_igehely'], sor['cel_igehely']))
    for sor in jeloltek:
        if sor['id'] not in motivum_id_halmaz:
            hibas.append('jeloltek: %s / %s' % (sor['id'], sor['igehely']))
    for sor in auditok:
        if sor['id'] not in motivum_id_halmaz:
            hibas.append('auditok: %s / %s' % (sor['id'], sor.get('lepes', '')))
    if hibas:
        return Sor('1. Hivatkozási épség', 'SÉRTÉS', len(hibas), hibas)
    return Sor('1. Hivatkozási épség', 'RENDBEN')


def szabaly2_nincs_kozvetlen_ut(elofordulasok, jeloltek):
    beepitett = {(j['id'], j['igehely']) for j in jeloltek if j.get('dontes') == 'beépítve'}
    hibas = []
    for sor in elofordulasok:
        kulcs = (sor['id'], sor['igehely'])
        if kulcs not in beepitett:
            hibas.append('%s / %s' % kulcs)
    if hibas:
        return Sor('2. Nincs közvetlen út', 'SÉRTÉS', len(hibas), hibas)
    return Sor('2. Nincs közvetlen út', 'RENDBEN')


def szabaly3_proveniencia(elofordulasok, auditok):
    """G9: a scope/forras/ts kotelezo; a lekerdez.py tovabbi kulcsai (strong,
    n) megengedettek; az igazolas-jellegu kulcsok (talalat, strong_vart)
    tiltottak (F8_BRIEF.md G9). Az `auditok.proveniencia` ugyanezen szabaly
    ala esik (SEMA.md §3/3, N12) -- a proveniencia_ervenyes hivasa import,
    nem masolat (F8 D21)."""
    hibas = []
    for sor in elofordulasok:
        if not proveniencia_ervenyes(sor.get('proveniencia', '')):
            hibas.append('%s / %s (%r)' % (sor['id'], sor['igehely'], sor.get('proveniencia', '')))
    for sor in auditok:
        if not proveniencia_ervenyes(sor.get('proveniencia', '')):
            hibas.append('auditok: %s / %s (%r)' % (
                sor['id'], sor.get('lepes', ''), sor.get('proveniencia', '')))
    if hibas:
        return Sor('3. Proveniencia-kényszer', 'SÉRTÉS', len(hibas), hibas)
    return Sor('3. Proveniencia-kényszer', 'RENDBEN')


def szabaly4_gerinc_elem(elofordulasok):
    hibas = []
    for sor in elofordulasok:
        if not (sor.get('gerinc_elem') or '').strip():
            hibas.append('%s / %s' % (sor['id'], sor['igehely']))
    if hibas:
        return Sor('4. Horgony-kényszer', 'SÉRTÉS', len(hibas), hibas)
    return Sor('4. Horgony-kényszer', 'RENDBEN')


def szabaly5_karoli_triplet(elofordulasok):
    hibas = []
    for sor in elofordulasok:
        if (sor.get('karoli_szo') or '').strip():
            if not (sor.get('azonositas_modja') or '').strip() or \
               not (sor.get('megbizhatosag') or '').strip():
                hibas.append('%s / %s' % (sor['id'], sor['igehely']))
    if hibas:
        return Sor('5. Károli-triplet', 'SÉRTÉS', len(hibas), hibas)
    return Sor('5. Károli-triplet', 'RENDBEN')


def szabaly6_gate_kenyszer(motivumok):
    hibas = []
    for m in motivumok:
        if m.get('statusz') in ('publikálható', 'véglegesített'):
            for mezo in ('azonossag_tipusa', 'negativ_kriterium', 'folerendelt_fogalom'):
                if not (m.get(mezo) or '').strip():
                    hibas.append('%s (%s üres)' % (m['id'], mezo))
    if hibas:
        return Sor('6. Gate-kényszer (4.6)', 'SÉRTÉS', len(hibas), hibas)
    return Sor('6. Gate-kényszer (4.6)', 'RENDBEN')


def szabaly7_gate_jelentes(motivumok, elofordulasok):
    igehelyek = {}
    for sor in elofordulasok:
        igehelyek.setdefault(sor['id'], set()).add(sor['igehely'])
    shared = GATE.collision_report(igehelyek)
    pair_overlap = GATE.pair_overlap_report(igehelyek)
    subset = GATE.subset_report(igehelyek)
    megjegyzes = ('%d osztozó igehely, %d átfedő motívumpár, %d részhalmaz-gyanús pár '
                  '(l. `python eszkozok/gate.py` a részletekért)'
                  % (len(shared), len(pair_overlap), len(subset)))
    return Sor('7. Ütközés-/részhalmaz-jelentés (gate.py)', 'JELENTÉS', megjegyzes=megjegyzes)


def _mindig_datasetek(datasetek):
    """[(nev, fajlnev)] -- a study_tipus=tematikus, kotelezoseg=mindig,
    allapot!=hianyzik sorok, a `fajl` mezo alapneve szerint."""
    ki = []
    for sor in datasetek:
        if sor.get('study_tipus') != 'tematikus':
            continue
        if sor.get('kotelezoseg') != 'mindig':
            continue
        if sor.get('allapot') == 'hianyzik':
            continue
        ki.append((sor['dataset'], os.path.basename(sor['fajl'])))
    return ki


def _felteteles_datasetek(datasetek):
    """[(nev, fajlnev)] -- a study_tipus=tematikus, kotelezoseg=felteteles
    sorok, a `fajl` mezo alapneve szerint (F8.5a)."""
    ki = []
    for sor in datasetek:
        if sor.get('study_tipus') != 'tematikus':
            continue
        if sor.get('kotelezoseg') != 'felteteles':
            continue
        ki.append((sor['dataset'], os.path.basename(sor['fajl'])))
    return ki


def szabaly8b_feltetel_datasetek(datasetek, cim='8/b. Feltételes datasetek'):
    """KEZI sor a felteteles tematikus datasetekrol (F8.5a) -- a feltetel
    teljesulese iteletet igenyel, nem geppel donthet."""
    felteteles = _felteteles_datasetek(datasetek)
    peldak = ['%s (%s)' % (nev, fajl) for nev, fajl in felteteles]
    return Sor(cim, 'KÉZI', len(peldak), peldak,
               megjegyzes='a feltétel teljesülése ítélet, l. F8_BRIEF.md F8.5a')


def _id_szerint_provok(elofordulasok, auditok):
    """{motivum_id: [proveniencia, ...]} -- az elofordulasok es az auditok
    provenienciai egyutt (N12: a nyom motivumszintu, ket tablabol jon)."""
    ki = {}
    for sor in elofordulasok:
        ki.setdefault(sor['id'], []).append(sor.get('proveniencia', ''))
    for sor in auditok:
        ki.setdefault(sor['id'], []).append(sor.get('proveniencia', ''))
    return ki


def _fedett_datasetek(provok):
    """set -- a provok listajanak forras_fajlok()-uniója."""
    fedett = set()
    for p in provok:
        fedett |= forras_fajlok(p)
    return fedett


def szabaly8_dataset_lefedettseg_gepi(motivumok, elofordulasok, auditok, datasetek, csak_id=None):
    """(Sor, erintett_id_lista). N12: PONTOS fajlnev-egyezes (a regi
    reszsztring-illesztes megszunt); a LEKERDEZO_NELKULI datasetek es a
    RETROAKTIV_IDK meg fedetlen datasetjei nem szamitanak gepi parnak --
    ezeket a 8/c (szabaly8c_kezi_lefedettseg) jelenti. 0 gepi par eseten a
    sor KEZI, sose RENDBEN (F8 D13/D16 elve: ures halmazon a "rendben" hamis
    zold). csak_id: ha adott, csak erre az egy ID-re (Q7 hasznalja);
    egyebkent minden, elofordulasok/auditok-ban jelen levo ID-re."""
    mindig = _mindig_datasetek(datasetek)
    id_szerint_proveniencia = _id_szerint_provok(elofordulasok, auditok)

    id_lista = [csak_id] if csak_id else sorted(id_szerint_proveniencia)
    hibas = []
    gepi_par_szam = 0
    for motivum_id in id_lista:
        fedett = _fedett_datasetek(id_szerint_proveniencia.get(motivum_id, []))
        for dataset_nev, dataset_fajl in mindig:
            if dataset_fajl in LEKERDEZO_NELKULI:
                continue
            talalt = dataset_fajl in fedett
            if not talalt and motivum_id in RETROAKTIV_IDK:
                continue
            gepi_par_szam += 1
            if not talalt:
                hibas.append('%s -- hiányzik: %s (%s)' % (motivum_id, dataset_nev, dataset_fajl))
    if gepi_par_szam == 0:
        return Sor('8. Dataset-lefedettség (gépi)', 'KÉZI', megjegyzes='nincs gépileg ellenőrizhető motívum'), id_lista
    if hibas:
        return Sor('8. Dataset-lefedettség (gépi)', 'SÉRTÉS', len(hibas), hibas), id_lista
    return Sor('8. Dataset-lefedettség (gépi)', 'RENDBEN'), id_lista


def _tematikus_forras_study(forras_study_ertek):
    """Az elso `tematikus_lezart/`-tagu resz a `;`-vel tagolt forras_study
    mezobol, vagy None."""
    for resz in (forras_study_ertek or '').split(';'):
        resz = resz.strip()
        if resz.startswith('tematikus_lezart/'):
            return resz
    return None


def _naplo_mutato(motivum_id, motivum_sor):
    """A 8/c ember-ellenorzesi mutato-szovege egy ID-hez (N12.2). A naplo
    utja: '<study-mappa>/naplok/<torzs>_kereszthivatkozas_naplo.md', ahol
    <torzs> a study-fajl neve '.md' nelkul, vagy ugyanez a '_tematikus'
    vegzodes nelkul -- az elso letezo. Ha egyik sem, de letezik a generalt
    proba, arra mutat kifejezett megszoritassal; ha az sem, "napló nincs"."""
    forras_study = _tematikus_forras_study((motivum_sor or {}).get('forras_study'))
    if not forras_study:
        return 'ember ellenőrizze: (nincs tematikus_lezart forrás_study) | napló nincs'

    study_mappa = forras_study.split('/', 1)[0]
    fajlnev = forras_study.rsplit('/', 1)[-1]
    torzs1 = fajlnev[:-3] if fajlnev.endswith('.md') else fajlnev
    torzsek = [torzs1]
    if torzs1.endswith('_tematikus'):
        torzsek.append(torzs1[:-len('_tematikus')])

    for torzs in torzsek:
        jelolt = '%s/naplok/%s_kereszthivatkozas_naplo.md' % (study_mappa, torzs)
        if os.path.exists(os.path.join(ROOT, jelolt)):
            return 'ember ellenőrizze: `%s` + `%s`' % (forras_study, jelolt)

    generalt = 'generalt_proba/%s/naplok/%s_kereszthivatkozas_naplo_GENERALT.md' % (
        study_mappa, motivum_id)
    if os.path.exists(os.path.join(ROOT, generalt)):
        return ('napló nincs (csak generált próba: `%s`, nem a study eredeti keresése)'
                % generalt)
    return 'napló nincs'


def szabaly8c_kezi_lefedettseg(motivumok, elofordulasok, auditok, datasetek, csak_id=None,
                                cim='8/c. Kézi dataset-lefedettség'):
    """N12: soronkent egy ID -- a fedetlen datasetek listaja, BDB-nel
    '(nincs lekérdező)', retroaktivnal '(retroaktív, F3)', plusz a
    naplo-mutato. Az a dataset, amely SEM LEKERDEZO_NELKULI, SEM nem
    retroaktiv-fedetlen, itt nem jelenik meg -- azt a gepi szabaly mar
    SÉRTÉSkent jelentette."""
    mindig = _mindig_datasetek(datasetek)
    id_szerint_proveniencia = _id_szerint_provok(elofordulasok, auditok)
    motivum_szerint = {m['id']: m for m in motivumok}

    id_lista = [csak_id] if csak_id else sorted(id_szerint_proveniencia)
    sorok = []
    for motivum_id in id_lista:
        fedett = _fedett_datasetek(id_szerint_proveniencia.get(motivum_id, []))
        hianyok = []
        for dataset_nev, dataset_fajl in mindig:
            if dataset_fajl in fedett:
                continue
            if dataset_fajl in LEKERDEZO_NELKULI:
                hianyok.append('%s (nincs lekérdező)' % dataset_nev)
            elif motivum_id in RETROAKTIV_IDK:
                hianyok.append('%s (retroaktív, F3)' % dataset_nev)
        if not hianyok:
            continue
        mutato = _naplo_mutato(motivum_id, motivum_szerint.get(motivum_id))
        sorok.append('%s -- fedetlen: %s | %s' % (motivum_id, ', '.join(hianyok), mutato))
    return Sor(cim, 'KÉZI', len(sorok), sorok)


# ---------------------------------------------------------------------------
# Q1 / Q7 -- --study
# ---------------------------------------------------------------------------

import re

FOCIM_RE = re.compile(r'^## (\d+)\.', re.M)


def q1_szerkezeti_teljesseg(study_szoveg):
    """RENDBEN / (SÉRTÉS, hianyzo_vagy_ures lista) -- a '## 1.'-'## 6.'
    szamozott focimek megvannak-e, es egyik torzse sem ures. A cim szoveget
    nem vizsgalja."""
    talalatok = {}
    pozicio = [(m.start(), int(m.group(1))) for m in FOCIM_RE.finditer(study_szoveg)]
    hatarok = pozicio + [(len(study_szoveg), None)]
    for i, (start, szam) in enumerate(pozicio):
        vege = hatarok[i + 1][0]
        # a torzs a cimsor sorvegetol a kovetkezo '## ' cimig
        sor_vege = study_szoveg.index('\n', start) if '\n' in study_szoveg[start:] else vege
        torzs = study_szoveg[sor_vege:vege].strip()
        talalatok[szam] = torzs

    hianyzo = [n for n in range(1, 7) if n not in talalatok]
    ures = [n for n in range(1, 7) if n in talalatok and not talalatok[n]]
    if hianyzo or ures:
        problemak = []
        if hianyzo:
            problemak.append('hiányzó főcím(ek): %s' % ', '.join('## %d.' % n for n in hianyzo))
        if ures:
            problemak.append('üres törzsű főcím(ek): %s' % ', '.join('## %d.' % n for n in ures))
        return False, problemak
    return True, []


def forras_study_illeszkedik(forras_study_ertek, study_fajl_relativ):
    reszek = [r.strip() for r in (forras_study_ertek or '').split(';') if r.strip()]
    return study_fajl_relativ in reszek


def study_ellenorzes(study_path, motivumok, elofordulasok, auditok, datasetek):
    """[Sor] -- Q1, Q2-Q6 (KÉZI), Q7 + 8/b + 8/c egy study-fajlra."""
    rel = os.path.relpath(study_path, ROOT).replace(os.sep, '/')
    with open(study_path, encoding='utf-8') as f:
        szoveg = f.read()

    rendben, problemak = q1_szerkezeti_teljesseg(szoveg)
    if rendben:
        sorok = [Sor('Q1 (%s)' % rel, 'RENDBEN')]
    else:
        sorok = [Sor('Q1 (%s)' % rel, 'SÉRTÉS', len(problemak), problemak)]

    for q in ('Q2', 'Q3', 'Q4', 'Q5', 'Q6'):
        sorok.append(Sor('%s (%s)' % (q, rel), 'KÉZI',
                          megjegyzes='ítéletet igényel, l. F8_BRIEF.md G4'))

    erintett_id = [m['id'] for m in motivumok if forras_study_illeszkedik(m.get('forras_study'), rel)]
    if not erintett_id:
        sorok.append(Sor('Q7 (%s)' % rel, 'SÉRTÉS', 1,
                          ['egyetlen motivumok.tsv sor forras_study-ja sem tartalmazza ezt a fájlt']))
    else:
        felteteles = _felteteles_datasetek(datasetek)
        for motivum_id in erintett_id:
            q7_sor, _ = szabaly8_dataset_lefedettseg_gepi(motivumok, elofordulasok, auditok,
                                                           datasetek, csak_id=motivum_id)
            q7_sor.cim = 'Q7 (%s, %s)' % (rel, motivum_id)
            if q7_sor.verdict == 'RENDBEN' and felteteles:
                q7_sor.verdict = 'RENDBEN (mindig)'
            sorok.append(q7_sor)
            sorok.append(szabaly8b_feltetel_datasetek(
                datasetek, cim='8/b (%s, %s). Feltételes datasetek' % (rel, motivum_id)))
            sorok.append(szabaly8c_kezi_lefedettseg(
                motivumok, elofordulasok, auditok, datasetek, csak_id=motivum_id,
                cim='8/c (%s, %s). Kézi dataset-lefedettség' % (rel, motivum_id)))
    return sorok


# ---------------------------------------------------------------------------
# Fő futás
# ---------------------------------------------------------------------------

def osszesito(sorok):
    """A 'RENDBEN (mindig)' is a RENDBEN kosarba szamit (F8.5a)."""
    darab = {'RENDBEN': 0, 'SÉRTÉS': 0, 'KÉZI': 0, 'JELENTÉS': 0}
    for s in sorok:
        alap = s.verdict.split(' ', 1)[0]
        darab[alap] = darab.get(alap, 0) + 1
    return darab


def main():
    parser = argparse.ArgumentParser(description='F8.5 -- SEMA §3 + Q-kapu gépi része')
    parser.add_argument('--adat', default=ALAPERTELMEZETT_ADAT,
                         help='az adat/ könyvtár (alapértelmezés: a repó adat/-ja)')
    parser.add_argument('--study', action='append', default=[],
                         help='study-fájl Q1/Q7 ellenőrzéséhez (ismételhető)')
    parser.add_argument('--md', default=None, help='a jelentés Markdown fájlba is')
    args = parser.parse_args()

    try:
        _, motivumok = G.tsv_beolvas(os.path.join(args.adat, 'motivumok.tsv'))
        _, elofordulasok = G.tsv_beolvas(os.path.join(args.adat, 'elofordulasok.tsv'))
        _, jeloltek = G.tsv_beolvas(os.path.join(args.adat, 'jeloltek.tsv'))
        _, kapcsolatok = G.tsv_beolvas(os.path.join(args.adat, 'kapcsolatok.tsv'))
        _, datasetek = G.tsv_beolvas(os.path.join(args.adat, 'datasetek.tsv'))
        _, auditok = G.tsv_beolvas(os.path.join(args.adat, 'auditok.tsv'))
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    motivum_id_halmaz = {m['id'] for m in motivumok}

    tabla_sorok = []
    try:
        tabla_sorok.append(szabaly1_hivatkozasi_epseg(motivum_id_halmaz, elofordulasok,
                                                        kapcsolatok, jeloltek, auditok))
        tabla_sorok.append(szabaly2_nincs_kozvetlen_ut(elofordulasok, jeloltek))
        tabla_sorok.append(szabaly3_proveniencia(elofordulasok, auditok))
        tabla_sorok.append(szabaly4_gerinc_elem(elofordulasok))
        tabla_sorok.append(szabaly5_karoli_triplet(elofordulasok))
        tabla_sorok.append(szabaly6_gate_kenyszer(motivumok))
        tabla_sorok.append(szabaly7_gate_jelentes(motivumok, elofordulasok))
        sor8, _ = szabaly8_dataset_lefedettseg_gepi(motivumok, elofordulasok, auditok, datasetek)
        felteteles = _felteteles_datasetek(datasetek)
        if sor8.verdict == 'RENDBEN' and felteteles:
            sor8.verdict = 'RENDBEN (mindig)'
        tabla_sorok.append(sor8)
        tabla_sorok.append(szabaly8b_feltetel_datasetek(datasetek))
        tabla_sorok.append(szabaly8c_kezi_lefedettseg(motivumok, elofordulasok, auditok, datasetek))
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    study_sorok = []
    try:
        for study_path in args.study:
            study_sorok.extend(study_ellenorzes(study_path, motivumok, elofordulasok,
                                                 auditok, datasetek))
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    minden_sor = tabla_sorok + study_sorok
    osszes = osszesito(minden_sor)

    kimenet = ['# ellenoriz.py -- SEMA §3 + Q-kapu gépi része (F8.5)', '',
               '## Tábla-szabályok (`adat/SEMA.md` §3)', '']
    for s in tabla_sorok:
        kimenet.append(s.sor_szoveg())
        kimenet.append('')
    if study_sorok:
        kimenet.append('## `--study` ellenőrzés')
        kimenet.append('')
        for s in study_sorok:
            kimenet.append(s.sor_szoveg())
            kimenet.append('')
    kimenet.append('## Összesítő')
    kimenet.append('')
    kimenet.append('RENDBEN: %d | SÉRTÉS: %d | KÉZI: %d | JELENTÉS: %d'
                    % (osszes['RENDBEN'], osszes['SÉRTÉS'], osszes['KÉZI'], osszes['JELENTÉS']))

    szoveg = '\n'.join(kimenet) + '\n'
    print(szoveg)

    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('  megírva: %s' % args.md, file=sys.stderr)

    sys.exit(1 if osszes['SÉRTÉS'] > 0 else 0)


if __name__ == '__main__':
    main()
