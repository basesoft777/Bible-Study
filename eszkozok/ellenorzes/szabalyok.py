#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
szabalyok.py -- CI.0: az E2-E20 es E25 ellenorzesek (F02_CI_ELLENORZES_BRIEF.md
"Ellenorzolista" tablazata; az E20 es az E8/E9/E12/E13 tanulmanyfajlra
szolo bovitese: F37_TANULMANY_ELLENORZES_BRIEF.md T3, naplok/T0_felmeres.md 3.
pont -- a tervezett E21-E24 atfedes miatt nem uj szabaly, hanem az E13, E8,
E9, E12 hatokorenek bovitese, DT-F37-8). Egy szabaly = egy fuggveny, mind
`(fajllista) -> [Talalat, ...]` alaku (E16 kivetel: PR-metaadatot is kap;
E5 kivetel: git diff-et is kap -- l. az egyes fuggvenyek docstringjet).

A HIBA/FIGYELMEZTETES szint a fuggvenyben van rogzitve a brief tablazata
szerint (D4: a heurisztikus E12-E15 FIGYELMEZTETES-sel indul) -- a futtat.py
ezt olvassa ki, nem duplikalja.

Egyik fuggveny sem ir fajlt; a `kozos.py` fajl- es tsv-olvaso segedei
felett dolgoznak.
"""

import os
import datetime
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kozos import (
    ROOT, ADAT, Talalat, md_olvasas, dict_sorok, dict_sorok_sorszammal,
    szakaszokra_bont, repo_ut, tanulmany_fajl_e, TANULMANY_SABLON,
)

# D8: ezeknek a szabalyoknak a talalata motivum-/fajl-szintu (nem egy
# konkret uj/modositott sorhoz kotheto), ezert a diff-alapu HIBA/JELENTES
# leminositest a futtat.py nem alkalmazza rajuk -- mindig a sajat
# (SZINT-ben rogzitett) szintjukon jelentkeznek. E6/E7 a brief expliciten
# ezt mondja ki; E4/E5/E16 szerkezetileg ugyanide tartozik (E5 maga is
# diff-alapu, E16 fajl-letezes, E4 motivum-szintu audit-allapot).
# E20 (F37): a hianyzo kotelezo szakasz a tanulmany egeszere vonatkozik, nem
# egy sorra -- a modositott tanulmanyfajlon mindig piros (F37 T3 "Futasi mod").
FAJLSZINTU_SZABALYOK = {'E4', 'E5', 'E6', 'E7', 'E16', 'E19', 'E20', 'E25', 'E26', 'E27',
                        'E28', 'E29', 'E31'}

# Adattablan futo szabalyok: --teljes modban a futtat.py a ['__TELJES__']
# jelzot adja nekik (az md-fajlok listaja helyett), kulonben nem futnanak.
HATOKOR_SZABALYOK = {'E3', 'E19', 'E25', 'E28', 'E29', 'E31'}

SZINT = {
    'E2': 'HIBA', 'E3': 'HIBA', 'E4': 'HIBA', 'E5': 'HIBA', 'E6': 'HIBA',
    'E7': 'HIBA', 'E8': 'HIBA', 'E9': 'HIBA', 'E10': 'HIBA', 'E11': 'HIBA',
    'E12': 'FIGYELMEZTETES', 'E13': 'FIGYELMEZTETES', 'E14': 'FIGYELMEZTETES',
    'E15': 'FIGYELMEZTETES', 'E16': 'HIBA', 'E19': 'HIBA', 'E20': 'HIBA',
    'E25': 'FIGYELMEZTETES', 'E26': 'HIBA', 'E27': 'HIBA', 'E28': 'HIBA', 'E29': 'HIBA',
    'E31': 'HIBA',
}
# F37 (E21 -> E13): tanulmanyfajlon az E13 HIBA (a fuggveny talalatonkent
# allitja be; a futtat.py a talalat sajat szintjet veszi alapul).
E13_TANULMANY_SZINT = 'HIBA'


# --------------------------------------------------------------------------
# E2 -- "ellenorizve" jeloles csak proveniencia-sorral egy szakaszban
# --------------------------------------------------------------------------

# D10: a sima "ellenőrizve" szó nem szamit -- csak a harom eros jeloles.
JELOLES_MINTA = re.compile(
    r'STEPBible-ellenőrizve|🔍|🔬\s*valódi kutatás'
)
PROVENIENCIA_MINTA = re.compile(
    r'scope\s*=.*\|.*forras\s*=.*\|.*ts\s*='
)
# D10: checklist-sor ([x]/[ ]) sose szamit jelolesnek.
CHECKLIST_SOR_MINTA = re.compile(r'^\s*[-*]\s*\[[ xX]\]')


def e2_ellenorizve_proveniencia(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        szakaszok = szakaszokra_bont(sorok)
        for _cim_idx, _cim, eleje, vege in szakaszok:
            szakasz_szoveg = '\n'.join(sorok[eleje:vege])
            van_proveniencia = bool(PROVENIENCIA_MINTA.search(szakasz_szoveg))
            naplo_blokkban = False
            for i in range(eleje, vege):
                sor = sorok[i]
                # D10: a 【NAPLO: ...】 blokk tartalma nem szamit.
                if '【NAPLO' in sor or '【NAPLÓ' in sor:
                    naplo_blokkban = True
                if naplo_blokkban:
                    if '】' in sor:
                        naplo_blokkban = False
                    continue
                if CHECKLIST_SOR_MINTA.match(sor):
                    continue
                if not JELOLES_MINTA.search(sor):
                    continue
                sor_maga_proveniens = PROVENIENCIA_MINTA.search(sor)
                if sor_maga_proveniens or van_proveniencia:
                    continue
                talalatok.append(Talalat(
                    'E2', SZINT['E2'], relut, i + 1, sor.strip()[:200]
                ))
    return talalatok


# --------------------------------------------------------------------------
# E3 -- proveniencia-mezo nem ures; lekerdezes nelkul 'manual', nem 'ellenorizve'
# --------------------------------------------------------------------------

def e3_proveniencia_mezo_ures_vagy_ellenorizve(fajlok):
    talalatok = []
    elofordulasok_ut = os.path.join(ADAT, 'elofordulasok.tsv')
    if 'adat/elofordulasok.tsv' not in fajlok and elofordulasok_ut not in [
        repo_ut(f) for f in fajlok
    ]:
        # E3 csak akkor fut az elofordulasok.tsv-n, ha az a valtozott
        # fajlok kozott van (a --teljes mod mindig fut).
        pass
    if not os.path.exists(elofordulasok_ut):
        return talalatok
    if 'adat/elofordulasok.tsv' not in fajlok and fajlok != ['__TELJES__']:
        return talalatok
    # D8: valodi fajl-sorszam kell (nem az adatsor-index), hogy a
    # diff-alapu HIBA/JELENTES leminosites a tenyleges tsv-sorral
    # osszevethető legyen.
    for sorszam, d in dict_sorok_sorszammal(elofordulasok_ut):
        prov = d.get('proveniencia', '')
        if not prov.strip():
            talalatok.append(Talalat(
                'E3', SZINT['E3'], 'adat/elofordulasok.tsv', sorszam,
                '%s | %s -- proveniencia ures' % (d.get('id', ''), d.get('igehely', ''))
            ))
        elif 'ellenőrizve' in prov or 'ellenorizve' in prov:
            talalatok.append(Talalat(
                'E3', SZINT['E3'], 'adat/elofordulasok.tsv', sorszam,
                '%s | %s -- proveniencia="%s"' % (d.get('id', ''), d.get('igehely', ''), prov[:80])
            ))
    return talalatok


# --------------------------------------------------------------------------
# E4 -- friss teljes kereses (auditok.tsv) -> naplo fajl + minden jelolt dontese
# --------------------------------------------------------------------------

TELJES_SCAN_LEPESEK = {'B3'}  # "3. teljes OSZ/UJSZ scan" -- CLAUDE.md het lepes


def e4_teljes_scan_naplo_es_dontes(fajlok):
    """`fajlok`: `['__TELJES__']` -- minden motivum-ID (teljes-repo/JELENTES
    mod); egyebkent a valtozott fajlok listaja -- D8 szerint E4 motivum-
    szintu (FAJLSZINTU_SZABALYOK), de a diff-hatokor (D3) miatt PR-modban
    csak azokra a motivum-ID-kra fut, amelyeknek az auditok.tsv/jeloltek.tsv
    sora vagy a naplofajluk maga a valtozott fajlok kozott van -- kulonben
    minden regi, PR-en kivuli hianyt HIBA-nak jelentene minden PR-en."""
    talalatok = []
    auditok_ut = os.path.join(ADAT, 'auditok.tsv')
    jeloltek_ut = os.path.join(ADAT, 'jeloltek.tsv')
    if not (os.path.exists(auditok_ut) and os.path.exists(jeloltek_ut)):
        return talalatok
    teljes_mod = fajlok == ['__TELJES__']
    valtozott_halmaz = set(fajlok)
    erintett_auditok_jeloltek = teljes_mod or (
        'adat/auditok.tsv' in valtozott_halmaz or 'adat/jeloltek.tsv' in valtozott_halmaz
    )
    auditok = dict_sorok(auditok_ut)
    jeloltek = dict_sorok(jeloltek_ut)

    id_lepesek = {}
    for d in auditok:
        id_lepesek.setdefault(d.get('id', ''), set()).add(d.get('lepes', ''))

    id_jeloltek = {}
    for d in jeloltek:
        # DT-F127b: a teljes scan jelöltjei előfordulás-jelöltek; a motívumközi
        # jelölt döntését az ellenoriz.py 2/b. szabálya őrzi.
        if d.get('jelolt_tipus', 'elofordulas') != 'elofordulas':
            continue
        id_jeloltek.setdefault(d.get('id', ''), []).append(d)

    naplo_szovegek = {}
    for gyoker, konyvtarak, fnevek in os.walk(ROOT):
        if os.path.basename(gyoker) != 'naplok':
            continue
        for fnev in fnevek:
            if fnev.endswith('kereszthivatkozas_naplo.md'):
                ut = os.path.join(gyoker, fnev)
                relut = os.path.relpath(ut, ROOT).replace(os.sep, '/')
                try:
                    naplo_szovegek[relut] = '\n'.join(md_olvasas(ut))
                except (IOError, OSError):
                    pass

    for motivum_id, lepesek in sorted(id_lepesek.items()):
        if not (lepesek & TELJES_SCAN_LEPESEK):
            continue
        talalt_naplo = None
        for relut, szoveg in naplo_szovegek.items():
            if motivum_id in szoveg:
                talalt_naplo = relut
                break
        naplo_erintett = teljes_mod or (talalt_naplo is not None and talalt_naplo in valtozott_halmaz)
        if not (erintett_auditok_jeloltek or naplo_erintett):
            continue
        if talalt_naplo is None:
            talalatok.append(Talalat(
                'E4', SZINT['E4'], 'adat/auditok.tsv', 0,
                '%s: teljes scan (B3) fut, de nincs *_kereszthivatkozas_naplo.md, '
                'amely megemliti az ID-t' % motivum_id
            ))
            continue
        for jd in id_jeloltek.get(motivum_id, []):
            if not jd.get('dontes', '').strip():
                talalatok.append(Talalat(
                    'E4', SZINT['E4'], talalt_naplo, 0,
                    '%s: jelolt igehely "%s" dontes nelkul a jeloltek.tsv-ben' %
                    (motivum_id, jd.get('igehely', ''))
                ))
    return talalatok


# --------------------------------------------------------------------------
# E5 -- tartalomveszres-or (git diff alapu)
# --------------------------------------------------------------------------

CIMSOR_MINTA = re.compile(r'^#{2,3}\s')

# Sor elejen (opcionalis whitespace utan) allo jeloles -- nem eleg, ha a
# szoveg barhol csak *emliti* a jelolest (l. naplok/ELLENOR_CI_E5.md,
# "Sulyos" talalat: sajat commit-uzenet leiro mondata veletlenul kikapcsolta
# az E5-ot, mert a regi ellenorzes sima reszszoveg-keresest hasznalt).
SZANDEKOS_JELOLES_MINTA = re.compile(
    r'^\s*(TÖRLÉS-SZÁNDÉKOS|TORLES-SZANDEKOS):', re.MULTILINE
)


def _cimsor_szoveg_kulcs(cimsor):
    """A cimsor osszehasonlitasi kulcsa: a szint (##/###) es a szoveg, a
    szamok (pl. `16.0`, `#16`) nelkul. Igy a pontcimek atszamozasa nem
    szamit torlesnek, csak a szoveg valtozasa."""
    m = re.match(r'^(#{2,3})\s+(.*)$', cimsor.strip())
    if not m:
        return None
    szoveg = re.sub(r'#?\d+(?:\.\d+)*', '', m.group(2))
    return (m.group(1), ' '.join(szoveg.split()))


def _tenylegesen_torolt_cimsorok(torolt, hozzaadott):
    """A torolt cimsorok, amelyeknek nincs (szam nelkuli) megfeleloje a
    ugyanabban a fajlban hozzaadott cimsorok kozott; a megfeleltetes
    darabszamra pontos (egy hozzaadott cimsor egy torlest fedez)."""
    szabad = {}
    for c in hozzaadott:
        k = _cimsor_szoveg_kulcs(c)
        szabad[k] = szabad.get(k, 0) + 1
    maradt = []
    for c in torolt:
        k = _cimsor_szoveg_kulcs(c)
        if szabad.get(k, 0) > 0:
            szabad[k] -= 1
        else:
            maradt.append(c)
    return maradt


def _study_fajlok_halmaza_ref(ref):
    """A study-fajlok halmaza egy adott git ref allapotabol (`git show
    ref:adat/motivumok.tsv`), NEM a munkakonyvtarbol -- ha a
    study_fajlok_halmaza()-t hasznalnank, az mindig a jelenleg kicheckoutolt
    (tipikusan a head_ref) allapotot olvasna, es egy olyan PR, amely egy
    study-fajlt es a hozza tartozo forras_study-bejegyzest egyszerre torli,
    nem szamitana study-fajlnak -- pedig eppen ez a tartalomvesztes, amit az
    E5 hivatott elkapni. `ref` hianyaban vagy hiba eseten ures halmaz."""
    if not ref:
        return set()
    try:
        nyers = subprocess.check_output(
            ['git', 'show', '%s:adat/motivumok.tsv' % ref],
            cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return set()
    sorok = [s.rstrip('\r') for s in nyers.split('\n') if s.strip() and not s.startswith('#')]
    if not sorok:
        return set()
    fejlec = sorok[0].split('\t')
    try:
        idx = fejlec.index('forras_study')
    except ValueError:
        return set()
    halmaz = set()
    for sor in sorok[1:]:
        mezok = sor.split('\t')
        if idx >= len(mezok):
            continue
        for f in mezok[idx].split(';'):
            f = f.strip()
            if f:
                halmaz.add(f)
    return halmaz


def _study_vagy_sablon_fajl(fajl, study_halmaz):
    """F02_CI_ELLENORZES_BRIEF.md E5: a >30-sor-torles ag csak study- es
    sablonfajlokra vonatkozik. A study-fajlok kanonikus halmaza az
    `adat/motivumok.tsv` `forras_study` oszlopa; a sablonfajlok a
    `sablonok/` konyvtar alatt vannak."""
    if fajl is None:
        return False
    if fajl in study_halmaz:
        return True
    return fajl.startswith('sablonok/')


def e5_tartalomvesztes_or(base_ref, head_ref, commit_uzenet=''):
    """Git diff `base_ref..head_ref` -- ha torol ##/### cimsort (barmely
    fajlban), vagy egy study-/sablonfajlbol 30-nal tobb sort, a
    commit-uzenetben kell 'TORLES-SZANDEKOS:' jelolesnek lennie. Mas
    fajlokbol (pl. `eszkozok/*.py`) torolt >30 sor nem szamit -- a brief
    E5-sora expliciten study-/sablonfajlra korlatozza ezt az agat.
    `base_ref`/`head_ref` hianyaban (pl. --teljes mod) [] -- ez a szabaly
    csak diff-mod ban ertelmezheto."""
    talalatok = []
    if not base_ref or not head_ref:
        return talalatok
    study_halmaz = _study_fajlok_halmaza_ref(base_ref) | _study_fajlok_halmaza_ref(head_ref)
    try:
        kimenet = subprocess.check_output(
            ['git', 'diff', '--unified=0', '%s..%s' % (base_ref, head_ref)],
            cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return talalatok

    van_szandekos = bool(SZANDEKOS_JELOLES_MINTA.search(commit_uzenet))
    aktualis_fajl = None
    torolt_szam = 0
    torolt_cimsor = []
    hozzaadott_cimsor = []

    def lezar():
        if aktualis_fajl is None:
            return
        if van_szandekos:
            return
        torolt = _tenylegesen_torolt_cimsorok(torolt_cimsor, hozzaadott_cimsor)
        if torolt:
            for c in torolt:
                talalatok.append(Talalat(
                    'E5', SZINT['E5'], aktualis_fajl, 0,
                    'torolt cimsor "TÖRLÉS-SZÁNDÉKOS:" jeloles nelkul: %s' % c
                ))
        elif torolt_szam > 30 and _study_vagy_sablon_fajl(aktualis_fajl, study_halmaz):
            talalatok.append(Talalat(
                'E5', SZINT['E5'], aktualis_fajl, 0,
                '%d torolt sor "TÖRLÉS-SZÁNDÉKOS:" jeloles nelkul' % torolt_szam
            ))

    for sor in kimenet.splitlines():
        if sor.startswith('+++ ') or sor.startswith('--- '):
            continue
        if sor.startswith('diff --git'):
            lezar()
            m = re.search(r' b/(\S+)$', sor)
            aktualis_fajl = m.group(1) if m else None
            if aktualis_fajl and aktualis_fajl.startswith('beerkezo/'):
                aktualis_fajl = None  # F20 B6: a beerkezo/ kimarad
            torolt_szam = 0
            torolt_cimsor = []
            hozzaadott_cimsor = []
            continue
        if sor.startswith('+') and not sor.startswith('++'):
            if CIMSOR_MINTA.match(sor[1:]):
                hozzaadott_cimsor.append(sor[1:].strip())
            continue
        if sor.startswith('-') and not sor.startswith('--'):
            torolt_szam += 1
            if CIMSOR_MINTA.match(sor[1:]):
                torolt_cimsor.append(sor[1:].strip())
    lezar()
    return talalatok


# --------------------------------------------------------------------------
# E6 -- tematikus study: "0. Forras-osszegyujtes" szakasz + elo sablon oszlopszam
# --------------------------------------------------------------------------

def _tablazat_oszlopszamok(sorok):
    """A '|---|---|...' elvalaszto sorok oszlopszamai (lista)."""
    ki = []
    for sor in sorok:
        s = sor.strip()
        if re.match(r'^\|(\s*:?-+:?\s*\|)+$', s):
            oszlopok = [o for o in s.strip('|').split('|')]
            ki.append(len(oszlopok))
    return ki


def _elo_sablon_talalati_tabla_oszlopszam():
    ut = repo_ut('sablonok', '4_PaRDeS_tematikus_sablon.md')
    if not os.path.exists(ut):
        return None
    sorok = md_olvasas(ut)
    szakaszok = szakaszokra_bont(sorok)
    for _idx, cim, eleje, vege in szakaszok:
        if cim and cim.strip().lstrip('#').strip().startswith('1. Előfordulások összegyűjtése'):
            oszlopszamok = _tablazat_oszlopszamok(sorok[eleje:vege])
            if oszlopszamok:
                return max(oszlopszamok)
    return None


def e6_tematikus_forras_es_tabla(fajlok):
    talalatok = []
    elvart = _elo_sablon_talalati_tabla_oszlopszam()
    for relut in fajlok:
        if not relut.endswith('_tematikus.md'):
            continue
        if not relut.startswith('tematikus_lezart/') or '/naplok/' in relut:
            continue
        ut = repo_ut(relut)
        try:
            sorok = md_olvasas(ut)
        except (IOError, OSError):
            continue
        egesz = '\n'.join(sorok)
        if '0. Forrás-összegyűjtés' not in egesz:
            talalatok.append(Talalat(
                'E6', SZINT['E6'], relut, 0,
                'hianyzik a "0. Forrás-összegyűjtés" szakasz'
            ))
        if elvart is not None:
            szakaszok = szakaszokra_bont(sorok)
            for _idx, cim, eleje, vege in szakaszok:
                if cim and cim.strip().lstrip('#').strip().startswith('1. Előfordulások összegyűjtése'):
                    oszlopszamok = _tablazat_oszlopszamok(sorok[eleje:vege])
                    if oszlopszamok and max(oszlopszamok) != elvart:
                        talalatok.append(Talalat(
                            'E6', SZINT['E6'], relut, eleje + 1,
                            'talalati tabla oszlopszama %d, az elo sablone %d' %
                            (max(oszlopszamok), elvart)
                        ))
    return talalatok


# --------------------------------------------------------------------------
# E7 -- 'bekerult' donteshez tartozo igehely a study tablajaban, ne csak prozaban
# --------------------------------------------------------------------------

def e7_bekerult_de_nincs_tablaban(fajlok):
    talalatok = []
    jeloltek_ut = os.path.join(ADAT, 'jeloltek.tsv')
    if not os.path.exists(jeloltek_ut):
        return talalatok
    jeloltek = dict_sorok(jeloltek_ut)
    bekerultek = [d for d in jeloltek if d.get('dontes', '').strip().lower() == 'bekerult']
    if not bekerultek:
        return talalatok

    study_fajlok = [f for f in fajlok if f.endswith('_tematikus.md') and f.startswith('tematikus_lezart/') and '/naplok/' not in f]
    for relut in study_fajlok:
        ut = repo_ut(relut)
        try:
            sorok = md_olvasas(ut)
        except (IOError, OSError):
            continue
        egesz = '\n'.join(sorok)
        tabla_sorok = '\n'.join(s for s in sorok if s.strip().startswith('|'))
        for d in bekerultek:
            igehely = d.get('igehely', '').strip()
            if not igehely or igehely not in egesz:
                continue
            if igehely in tabla_sorok:
                continue
            talalatok.append(Talalat(
                'E7', SZINT['E7'], relut, 0,
                '%s (%s) bekerult dontessel szerepel a szovegben, de nincs a tablazatban' %
                (igehely, d.get('id', ''))
            ))
    return talalatok


# --------------------------------------------------------------------------
# E8 -- igehely-format
# --------------------------------------------------------------------------

TILTOTT_IGEHELY_MINTAK = [
    re.compile(r'\b\d\s+Móz\b'),
    re.compile(r'\b\d\.\s*Móz\b'),
    re.compile(r'\bApCsel\.\s'),
    re.compile(r'\b\d\.\s*(Sám|Kir|Krón|Kor|Thessz|Tim|Pét|Jn)\b'),
]
HELYES_IGEHELY_MINTA = re.compile(r'\b\d(Móz|Sám|Kir|Krón|Kor|Thessz|Tim|Pét|Jn)\b')

# F37 (E22 -> E8): a tanulmanyfajlban a versformatum egyseges (`1Móz 17:1`).
# A ket tovabbi tiltott alak csak itt tiltott: mas fajlban (CLAUDE.md, briefek,
# adat-leirasok) a STEPBible-alak (`Gen.1.1`) adatformatumkent legitim.
TANULMANY_TILTOTT_IGEHELY_MINTAK = [
    # hosszu konyvnev fejezet:vers elott: "1Mózes 12:1", "1 Mózes 3:1"
    re.compile(r'\b[1-5]\.?\s?Mózes\s+\d+[:,.]\d'),
    # STEPBible-alak a prozaban: "Gen.12.7", "1Ki.7.13"
    re.compile(r'\b[1-3]?[A-Z][a-z]{1,4}\.\d+\.\d+\b'),
]


def e8_igehely_format(fajlok):
    """D16: a backtickes inline kod (`...`) es a kodblokk (```...```) ki van
    zarva -- egy szabalyleiro sor, amely peldakent idezi a tiltott formatumot
    (pl. "`1 Móz`"), nem tenyleges study-szoveg.

    F37 (E22): tanulmanyfajlon (kozos.tanulmany_fajl_e) a
    TANULMANY_TILTOTT_IGEHELY_MINTAK is tiltott."""
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        mintak = TILTOTT_IGEHELY_MINTAK
        if tanulmany_fajl_e(relut):
            mintak = TILTOTT_IGEHELY_MINTAK + TANULMANY_TILTOTT_IGEHELY_MINTAK
        kodblokkban = False
        for i, sor in enumerate(sorok):
            if sor.strip().startswith('```'):
                kodblokkban = not kodblokkban
                continue
            if kodblokkban:
                continue
            tisztitott = re.sub(r'`[^`]*`', '', sor)
            for minta in mintak:
                m = minta.search(tisztitott)
                if m:
                    talalatok.append(Talalat(
                        'E8', SZINT['E8'], relut, i + 1,
                        'tiltott igehely-format: "%s" -- %s' % (m.group(0), sor.strip()[:150])
                    ))
    return talalatok


# --------------------------------------------------------------------------
# E9 -- angol "sense" szo a study-/lexikonszovegben
# --------------------------------------------------------------------------

SENSE_MINTA = re.compile(r'\bsense\b', re.IGNORECASE)

# F11 M3 (DT-F11a, DT-F11f (2)): az archivum/ alatti fajl a regi fajl
# ARCHÍV fejlecu, bajtra valtozatlan peldanya -- nem forras, nem
# szerkesztendo, tehat a szovegere szolo E9 nem fut ra.
ARCHIV_KONYVTAR = 'archivum/'


def e9_angol_sense(fajlok):
    """F37 (E23): tanulmanyfajlon a D11 blockquote-kizaras nem ervenyes -- ott
    a blockquote a 🔗 kereszthivatkozas-blokk (Karoli-idezet + magyar
    magyarazo sor), nem angol forrasszoveg. Az idezojeles szoveg ott is kizart.
    Az archivum/ alatti fajl kimarad (ARCHIV_KONYVTAR)."""
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        if relut.replace('\\', '/').startswith(ARCHIV_KONYVTAR):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        tanulmany = tanulmany_fajl_e(relut)
        kodblokkban = False
        for i, sor in enumerate(sorok):
            if sor.strip().startswith('```'):
                kodblokkban = not kodblokkban
                continue
            if kodblokkban:
                continue
            # D11: blockquote (idezett angol forrasszoveg) kizarva.
            if sor.lstrip().startswith('>') and not tanulmany:
                continue
            tisztitott = re.sub(r'`[^`]*`', '', sor)
            tisztitott = re.sub(r'"[^"]*"', '', tisztitott)
            tisztitott = re.sub(r'“[^”]*”', '', tisztitott)
            tisztitott = re.sub(r'„[^”]*”', '', tisztitott)
            if SENSE_MINTA.search(tisztitott):
                talalatok.append(Talalat(
                    'E9', SZINT['E9'], relut, i + 1, sor.strip()[:150]
                ))
    return talalatok


# --------------------------------------------------------------------------
# E10 -- spirit -> lelek / spiritual -> lelki tiltott forditas
# --------------------------------------------------------------------------

SPIRIT_LELEK_MINTA = re.compile(
    r'\bspirit(ual)?\b[^.\n]{0,25}\b(lélek\w*|lelki\w*)\b'
    r'|\b(lélek\w*|lelki\w*)\b[^.\n]{0,25}\bspirit(ual)?\b',
    re.IGNORECASE
)


def _e10_hatokorben_e(relut):
    """D17: E10 hatokore a szotari forditas tenyleges helye -- adat/ (pl.
    `forditas_ubs.tsv`, `lexikon_hivatkozasok.tsv`, a jovobeli SZOTAR S1
    `terminologia.tsv`/`forditasok.tsv`) es lexikon/ (a render). A gyoker
    brief-/tervfajlok (pl. `F05_SZOTAR_BRIEF.md`, `F02_CI_ELLENORZES_BRIEF.md`), ahol
    a szabaly sajat magat dokumentalja peldakent, nem tartoznak ide."""
    return relut.startswith('adat/') or relut.startswith('lexikon/')


def e10_spirit_lelek(fajlok):
    talalatok = []
    for relut in fajlok:
        if not _e10_hatokorben_e(relut):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
            # D17a: csak az inline kod kizart -- az idezojel- es a
            # blockquote-kizarast a D17a visszavonta, mert a lexikon a
            # magyar glosszat idezojelben adja ("lélek"), a Thayer-forditas
            # (#7) pedig blockquote-ban renderel, tehat pont a celpontot
            # rejtettek volna el.
            tisztitott = re.sub(r'`[^`]*`', '', sor)
            if SPIRIT_LELEK_MINTA.search(tisztitott):
                talalatok.append(Talalat(
                    'E10', SZINT['E10'], relut, i + 1, sor.strip()[:150]
                ))
    return talalatok


# --------------------------------------------------------------------------
# E11 -- Cremer/NIDNTTE/NIDOTTE tiltas (TWOT-szam kivetel)
# --------------------------------------------------------------------------

CREMER_MINTA = re.compile(r'\bCremer\b', re.IGNORECASE)
NIDNTTE_MINTA = re.compile(r'\bNIDNTTE\b')
NIDOTTE_MINTA = re.compile(r'\bNIDOTTE\b')


def _e11_hatokorben_e(relut):
    """D12: E11 hatokore -- lexikon/, adat/szotar_szerepek.tsv,
    eszkozok/*general*.py. A CI.0 61 talalatanak nagy resze a
    CREMER_OCR_BRIEF.md sajat targyalasa volt, nem tenyleges
    szerepmatrix-/render-sertes."""
    if relut.startswith('lexikon/'):
        return True
    if relut == 'adat/szotar_szerepek.tsv':
        return True
    if relut.startswith('eszkozok/') and 'general' in os.path.basename(relut) and relut.endswith('.py'):
        return True
    return False


def e11_cremer_nidntte_nidotte(fajlok):
    talalatok = []
    for relut in fajlok:
        if not _e11_hatokorben_e(relut):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
            # D12: forrasidezeten (blockquote) belul nem szamit.
            if sor.lstrip().startswith('>'):
                continue
            for minta, nev in ((CREMER_MINTA, 'Cremer'), (NIDNTTE_MINTA, 'NIDNTTE'), (NIDOTTE_MINTA, 'NIDOTTE')):
                if minta.search(sor):
                    talalatok.append(Talalat(
                        'E11', SZINT['E11'], relut, i + 1,
                        '%s emlitve: %s' % (nev, sor.strip()[:150])
                    ))
    return talalatok


# --------------------------------------------------------------------------
# E12 -- proveniencia prozaban (FIGYELMEZTETES)
# --------------------------------------------------------------------------

PROZAI_PROVENIENCIA_MINTA = re.compile(
    r'\b202\d\.\d{2}\.|\.tsv\b|\.md\b|audit során|visszaírva|felismerve|l\.\s*\d+\.?\s*pont'
)

# D13: E12/E13 hatokore a study-/naplo-/lexikon-reteg, nem a teljes repo --
# a CI.0 4087/3837 talalata jorreszt hatokoron kivuli brief-/tervdokumentumokbol jott.
E12_E13_HATOKOR = (
    'tematikus_lezart/', 'genezis/', 'ujszovetseg/', 'melyelemzesek/',
    'motivumlog/', 'lexikon/',
)


def _e12_e13_hatokorben_e(relut):
    # F37 (ELLENOR_TANULMANY_ELLENORZES 1.): a tanulmanyfajl a hatokor-
    # konyvtarakon kivul is a study-reteg resze, kulonben egy uj konyvtarba
    # irt tanulmanyon az E13 HIBA es az E12 csendben nem futna.
    return (any(relut.startswith(p) for p in E12_E13_HATOKOR)
            or tanulmany_fajl_e(relut))


# F37 (E24 -> E12): tanulmanyfajlon a naplojellegu szoveg tovabbi ket tipusa
# (naplok/T0_felmeres.md 3. pont): a sablonon kivuli napló-szakasz cimsora
# es a folyamatleiro mondat. A felismeres bizonytalan, ezert FIGYELMEZTETES
# marad (F37 T3: "ha bizonytalan, ez a szabaly csak figyelmeztessen").
TANULMANY_NAPLO_CIMSOR_MINTA = re.compile(
    r'^#{2,4}\s.*(önellenőrzés|napló[- ]frissítés|Kiegészítés\s*\(|Következő lépés|Javasolt következő)',
    re.IGNORECASE
)
TANULMANY_NAPLO_PROZA_MINTA = re.compile(
    r'retroaktív|visszamenőleges|Code-prompt|\bcommit\b', re.IGNORECASE
)


def e12_proveniencia_prozaban(fajlok):
    """F37 (E24): tanulmanyfajlon a naplojellegu cimsor es folyamat-mondat is
    talalat, ha nem `【NAPLO: …】` blokkban all."""
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        if not _e12_e13_hatokorben_e(relut):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        tanulmany = tanulmany_fajl_e(relut)
        naplo_blokkban = False
        for i, sor in enumerate(sorok):
            if '【NAPLO' in sor or '【NAPLÓ' in sor:
                naplo_blokkban = True
            if naplo_blokkban:
                if '】' in sor:
                    naplo_blokkban = False
                continue
            if tanulmany and (TANULMANY_NAPLO_CIMSOR_MINTA.search(sor)
                              or TANULMANY_NAPLO_PROZA_MINTA.search(sor)):
                talalatok.append(Talalat(
                    'E12', SZINT['E12'], relut, i + 1,
                    'naplojellegu szoveg 【NAPLO】 blokkon kivul: ' + sor.strip()[:140]
                ))
                continue
            if PROZAI_PROVENIENCIA_MINTA.search(sor):
                talalatok.append(Talalat(
                    'E12', SZINT['E12'], relut, i + 1, sor.strip()[:150]
                ))
    return talalatok


# --------------------------------------------------------------------------
# E13 -- heber/gorog szo kiejtes nelkul (FIGYELMEZTETES)
# --------------------------------------------------------------------------

HEBER_GOROG_FUTAM = re.compile(
    r'[֐-׿]{2,}|[Ͱ-Ͽ]{2,}'
)
# D13: elfogadott kiejtes-jelolesek --
#   (a) "– atiras" kotojel utan
#   (b) "(atiras)" zarojelben, akar veszo utan is (pl. "(H8414, tohu)")
#   (c) STEP-pontozott atiras barhol a 40 karakteres ablakban (pl. "te.hom")
KIEJTES_ELFOGADVA = re.compile(
    r'–\s*\*?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]'
    r'|\([^()]*[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2,}[^()]*\)'
    r'|\b[a-zá-űA-ZÁ-Ű]+(?:\.[a-zá-űA-ZÁ-Ű]+)+\b'
)


# F37 (E21 -> E13): a sor MINDEN heber/gorog futamat (kifejezest) nezi, nem
# csak az elsot. Egy kifejezes: egymas utani heber/gorog szavak (szokoz,
# maqaf, perjel, vesszo kozott), a politonikus gorog (U+1F00-1FFF) is.
_HG = r'[֐-׿]|[Ͱ-Ͽ]|[ἀ-῿]'
HEBER_GOROG_KIFEJEZES = re.compile(
    r'(?:%s){2,}(?:[\s/־,]+(?:%s)+)*' % (_HG, _HG)
)
_LATIN = r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüűāēīōūšḥṭṣʼʾʿ\']'
# A kifejezes UTAN allo, tovabbi elfogadott kiejtes-alakok (a D13 harom alakja mellett):
#   (d) dolt atiras kozvetlenul utana, opcionalis elvalasztoval: ", *mispachot*",
#       "| *lech-lechá* |" (a tablazat kovetkezo cellaja), "/ *pneuma*"
#   (e) perjel vagy tablazat-cella utan latin betus atiras: "/ toledot", "| re.Shit"
KIEJTES_UTANA_TANULMANY = re.compile(
    r'^\s*[|,/:;(–-]?\s*\*{1,2}_?%s' % _LATIN
    + r'|^\s*[/|]\s*\(?%s' % _LATIN
)
# A kifejezes ELOTT allo atiras: "*gadal* (גדל)", "*lech-lechá* / לֶךְ",
# "karat/כרת" (perjellel kozvetlenul elotte)
KIEJTES_ELOTTE = re.compile(
    r'\*[^*\n]{1,40}\*\s*[(/,–-]?\s*$' + r'|%s{2,}\s*/\s*$' % _LATIN
)
_HG_BETU = re.compile(_HG)
_LATIN_BETU = re.compile(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]')


def _eredeti_nyelvu_versor(sor):
    """A Tanulmany sablon 2. pontja a teljes verset eredeti nyelven kéri: az
    ilyen sor (tobbsegeben heber/gorog betu, legalabb harom heber/gorog szo)
    folyo szoveg, nem szotari szo -- a kiejtes-szabaly nem vonatkozik ra."""
    hg = len(_HG_BETU.findall(sor))
    lat = len(_LATIN_BETU.findall(sor))
    szavak = len(re.findall(r'(?:%s)+' % _HG, sor))
    return szavak >= 3 and hg >= 0.6 * (hg + lat)


def _kifejezes_kiejtessel(sor, m):
    utana = sor[m.end():m.end() + 60]
    if KIEJTES_ELFOGADVA.search(utana[:40]) or KIEJTES_UTANA_TANULMANY.search(utana):
        return True
    elotte = sor[max(0, m.start() - 50):m.start()]
    # a kifejezes egy zarojelben all, a zarojelen belul atirassal: "(מִשְׁפְּחֹת, *mispachot*)"
    nyito = elotte.rfind('(')
    if nyito != -1 and ')' not in elotte[nyito:]:
        zaro = sor.find(')', m.end())
        if zaro != -1 and re.search(_LATIN + r'{2,}', sor[m.end():zaro]):
            return True
    return bool(KIEJTES_ELOTTE.search(elotte))


def e13_kiejtes_hianya(fajlok):
    """F37 (E21): tanulmanyfajlon (kozos.tanulmany_fajl_e) HIBA, mashol
    FIGYELMEZTETES marad. Soronkent egy talalat (az elso kiejtes nelkuli
    kifejezes), hogy a jelentes ne sokszorozodjon."""
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        if not _e12_e13_hatokorben_e(relut):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        szint = E13_TANULMANY_SZINT if tanulmany_fajl_e(relut) else SZINT['E13']
        for i, sor in enumerate(sorok):
            if _eredeti_nyelvu_versor(sor):
                continue
            elfogadott = set()
            for m in HEBER_GOROG_KIFEJEZES.finditer(sor):
                kif = m.group(0).strip()
                # ugyanaz a kifejezes a sorban mar kiejtessel allt
                if kif in elfogadott:
                    continue
                if _kifejezes_kiejtessel(sor, m):
                    elfogadott.add(kif)
                    continue
                talalatok.append(Talalat(
                    'E13', szint, relut, i + 1,
                    'kiejtes nelkul: %s -- %s' % (m.group(0).strip()[:40], sor.strip()[:120])
                ))
                break
    return talalatok


# --------------------------------------------------------------------------
# E14 -- tematikus sablon 1. pont "Jelentes-szoveg" oszlopa angol (FIGYELMEZTETES)
# --------------------------------------------------------------------------

ANGOL_STOPSZAVAK = set(
    'the a an of to in on for and or is are be with as by at from that this '
    'it not no be left over into out up down'.split()
)


def _angol_arany(szoveg):
    szavak = re.findall(r"[A-Za-z']+", szoveg)
    if not szavak:
        return 0.0
    angol = sum(1 for sz in szavak if sz.lower() in ANGOL_STOPSZAVAK)
    return angol / float(len(szavak))


def e14_jelentes_szoveg_angol(fajlok):
    talalatok = []
    for relut in fajlok:
        if not (relut.endswith('_tematikus.md') and relut.startswith('tematikus_lezart/') and '/naplok/' not in relut):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        szakaszok = szakaszokra_bont(sorok)
        for _idx, cim, eleje, vege in szakaszok:
            if not (cim and cim.strip().lstrip('#').strip().startswith('1. Előfordulások összegyűjtése')):
                continue
            fejlec_sor = None
            for i in range(eleje, vege):
                if sorok[i].strip().startswith('|') and 'Jelentés-szöveg' in sorok[i]:
                    fejlec_sor = sorok[i]
                    oszlopok = [o.strip() for o in fejlec_sor.strip('|').split('|')]
                    try:
                        idx = oszlopok.index(next(o for o in oszlopok if 'Jelentés-szöveg' in o))
                    except StopIteration:
                        idx = None
                    if idx is None:
                        continue
                    for j in range(i + 2, vege):
                        sor = sorok[j]
                        if not sor.strip().startswith('|'):
                            break
                        cellak = [c.strip() for c in sor.strip('|').split('|')]
                        if idx < len(cellak):
                            cella = cellak[idx]
                            if _angol_arany(cella) > 0.4:
                                talalatok.append(Talalat(
                                    'E14', SZINT['E14'], relut, j + 1, cella[:150]
                                ))
    return talalatok


# --------------------------------------------------------------------------
# E15 -- SzPA-idezet hossza >25 szo (FIGYELMEZTETES)
# --------------------------------------------------------------------------

SZPA_IDEZET_MINTA = re.compile(r'SzPA[^:]{0,20}[:„"«]\s*(.+)')


def e15_szpa_idezet_hossz(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
            m = SZPA_IDEZET_MINTA.search(sor)
            if not m:
                continue
            idezet = m.group(1)
            idezojelben = re.search(r'[„"“]([^”"“]{0,600})[”"”]', idezet)
            szoveg = idezojelben.group(1) if idezojelben else idezet
            szoszam = len(szoveg.split())
            if szoszam > 25:
                talalatok.append(Talalat(
                    'E15', SZINT['E15'], relut, i + 1,
                    '%d szo -- %s' % (szoszam, szoveg[:150])
                ))
    return talalatok


# --------------------------------------------------------------------------
# E16 -- ellenorzo-onmodositas
# --------------------------------------------------------------------------

ONMODOSITAS_MINTAK = (
    'eszkozok/ellenorzes/',
    'eszkozok/ellenoriz.py',
    '.github/',
    '.claude/agents/fuggetlen-ellenor.md',
)


def e16_ellenorzo_onmodositas(fajlok, pr_cim=''):
    talalatok = []
    erintett = [f for f in fajlok if any(f.startswith(m) or f == m.rstrip('/') for m in ONMODOSITAS_MINTAK)]
    if not erintett:
        return talalatok
    if pr_cim.strip().startswith('[ELLENŐRZŐ]'):
        return talalatok
    talalatok.append(Talalat(
        'E16', SZINT['E16'], erintett[0], 0,
        'a PR erinti az ellenorzot (%s), de a cim nem "[ELLENŐRZŐ]" elotagu: %r' %
        (', '.join(erintett), pr_cim)
    ))
    return talalatok


# --------------------------------------------------------------------------
# E19 -- szotari hivatkozas forditas nelkul (F28_EMELES_BRIEF.md E6, D44)
# --------------------------------------------------------------------------
# Az E17 nevet a DT3 (sorszam-valtozas kuszob), az E18-at a feladatkovetes
# foglalja; ez a kovetkezo szabad szam.
#
# HIBA, ha az adat/lexikon_hivatkozasok.tsv egy Thayer- vagy BDB-sorahoz az
# adat/forditasok.tsv-ben nincs `opus`, `sonnet` vagy `kezi` allapotu `forditas_hu`
# sor, sem ugyanarra a `jelentes_szam`-ra, sem `teljes` szintre. A kulcs:
# szotar + strong + entry_id (a strong a Strong_padded alakra normalizalva).
# Csak akkor fut, ha a ket tabla valamelyike a valtozott fajlok kozott van;
# fajlszintu (D8): egy forditas-sor torlese is HIBA, akkor is, ha a
# hivatkozas sora nem valtozott.

E19_SZOTARAK = ('Thayer', 'BDB')
E19_ALLAPOTOK = ('opus', 'sonnet', 'kezi')
E19_FAJLOK = ('adat/lexikon_hivatkozasok.tsv', 'adat/forditasok.tsv')


def _e19_strong(s):
    m = re.match(r'^([GH])0*(\d{1,4})([a-z]?)$', (s or '').strip())
    return '%s%04d%s' % (m.group(1), int(m.group(2)), m.group(3)) if m else (s or '').strip()


def e19_szotari_forditas_hiany(fajlok):
    talalatok = []
    if fajlok != ['__TELJES__'] and not any(f in E19_FAJLOK for f in fajlok):
        return talalatok
    lex_ut = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
    ford_ut = os.path.join(ADAT, 'forditasok.tsv')
    if not os.path.exists(lex_ut):
        return talalatok
    van = set()
    if os.path.exists(ford_ut):
        for d in dict_sorok(ford_ut):
            if d.get('allapot') in E19_ALLAPOTOK and d.get('mezo') == 'forditas_hu':
                van.add((d.get('szotar'), _e19_strong(d.get('strong')), (d.get('entry_id') or '').strip(),
                         d.get('jelentes_szam')))
    for sorszam, d in dict_sorok_sorszammal(lex_ut):
        szotar = d.get('szotar')
        if szotar not in E19_SZOTARAK:
            continue
        alap = (szotar, _e19_strong(d.get('strong')), (d.get('entry_id') or '').strip())
        if alap + (d.get('jelentes_szam'),) in van or alap + ('teljes',) in van:
            continue
        talalatok.append(Talalat(
            'E19', SZINT['E19'], 'adat/lexikon_hivatkozasok.tsv', sorszam,
            '%s %s %s/%s -- nincs opus, sonnet vagy kezi forditas (sem erre a jelentesre, sem teljes szintre)'
            % (szotar, d.get('strong'), d.get('entry_id'), d.get('jelentes_szam'))
        ))
    return talalatok

# --------------------------------------------------------------------------
# E20 -- tanulmany: minden kotelezo szakasz megvan (F37 T3, DT-F37-6)
# --------------------------------------------------------------------------
# A szakaszlistat a Tanulmany sablon (kozos.TANULMANY_SABLON) szamozott `##`
# cimsoraibol olvassa, nem kodba egetve: kotelezo minden szamozott szakasz,
# amelynek cimsoraban nincs "(feltételes pont)". A tanulmany cimsora a szam
# (pl. `1/b.`) es a cim magja szerint illeszkedik: a mag a cim a `*(…)*`
# megjegyzes es a ` — ` utani alcim nelkul, kis-nagybetu nelkul.
# HIBA, ha (a) a kotelezo szakasz szama hianyzik, (b) a szam megvan, de a cim
# magja mas, (c) a szakasz torzse ures. Fajlszintu (FAJLSZINTU_SZABALYOK).

_E20_CIMSOR = re.compile(r'^##\s+(\d+(?:/[a-z])?)\.\s+(.*?)\s*$')


def _e20_mag(cim):
    cim = re.sub(r'\*\([^)]*\)\*', '', cim)
    cim = re.sub(r'\([^)]*\)', '', cim)
    cim = cim.split(' — ')[0]
    return ' '.join(cim.replace('*', '').split()).lower()


def tanulmany_sablon_szakaszai(sablon_relut=None):
    """[(szam, cim_mag, kotelezo, teljes_cim)] a Tanulmany sablonbol; None,
    ha a sablon nem olvashato."""
    ut = repo_ut(*(sablon_relut or TANULMANY_SABLON).split('/'))
    try:
        sorok = md_olvasas(ut)
    except (IOError, OSError):
        return None
    ki = []
    for sor in sorok:
        m = _E20_CIMSOR.match(sor)
        if not m:
            continue
        ki.append((m.group(1), _e20_mag(m.group(2)),
                   'feltételes pont' not in m.group(2), m.group(2).strip()))
    return ki


def e20_kotelezo_szakaszok(fajlok):
    talalatok = []
    tanulmanyok = [f for f in fajlok if tanulmany_fajl_e(f)]
    if not tanulmanyok:
        return talalatok
    sablon = tanulmany_sablon_szakaszai()
    if not sablon:
        for relut in tanulmanyok:
            talalatok.append(Talalat('E20', SZINT['E20'], relut, 0,
                                     'a Tanulmany sablon (%s) nem olvashato, vagy nincs '
                                     'szamozott ## szakasza' % TANULMANY_SABLON))
        return talalatok
    kotelezok = [s for s in sablon if s[2]]
    for relut in tanulmanyok:
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        cimek = {}
        for i, sor in enumerate(sorok):
            m = _E20_CIMSOR.match(sor)
            if m and m.group(1) not in cimek:
                vege = len(sorok)
                for j in range(i + 1, len(sorok)):
                    if sorok[j].startswith('## ') or sorok[j].startswith('# '):
                        vege = j
                        break
                torzs = '\n'.join(sorok[i + 1:vege]).replace('---', '').strip()
                cimek[m.group(1)] = (i + 1, _e20_mag(m.group(2)), torzs)
        for szam, mag, _k, teljes in kotelezok:
            if szam not in cimek:
                talalatok.append(Talalat('E20', SZINT['E20'], relut, 0,
                                         'hianyzik a kotelezo szakasz: ## %s. %s' % (szam, teljes)))
                continue
            sorszam, t_mag, torzs = cimek[szam]
            if not (t_mag.startswith(mag) or mag.startswith(t_mag)) or not t_mag:
                talalatok.append(Talalat('E20', SZINT['E20'], relut, sorszam,
                                         'a ## %s. szakasz cime ("%s") nem a sablon szerinti ("%s")'
                                         % (szam, t_mag, mag)))
            elif not torzs:
                talalatok.append(Talalat('E20', SZINT['E20'], relut, sorszam,
                                         'a ## %s. %s szakasz torzse ures' % (szam, teljes)))
    return talalatok


# --------------------------------------------------------------------------
# E25 -- dontes atvezetese (F51_KONZISZTENCIA_BRIEF.md K3, adat/SEMA.md 2.21)
# --------------------------------------------------------------------------
# Az adat/dontes_hatas.tsv minden sorara:
#   (a) a `tilos_minta` talalat az `erintett_fajl`-ban -> FIGYELMEZTETES, ha
#       nincs a fajlban `atmeneti_jeloles`, kulonben JELENTES;
#   (b) a `tovabbvivo_feladat` allapota nem_indult / brief_kell, es a `datum`
#       ota tobb mint 14 nap telt el -> FIGYELMEZTETES;
#   (c) hianyzo/hibas hivatkozas (dontes_forras fajl vagy azonosito,
#       erintett_fajl, regex) -> HIBA (DT-F51-4).
# Kivetel: a `tipus: archiv` fejlecu erintett fajlt az (a) ag kihagyja
# (archivumot nem szerkesztunk, a torteneti allapot nem hiba).
# Adattablan fut (HATOKOR_SZABALYOK): minden futasnal, a bemeneti listatol fuggetlenul.

E25_TABLA = 'adat/dontes_hatas.tsv'
E25_HATARNAP = 14
E25_NYITOTT_ALLAPOTOK = ('nem_indult', 'brief_kell')
MA = None  # tesztekben felulirhato datum (datetime.date); egyebkent a mai nap


def _e25_fejlec(sorok):
    """A fajl elejen allo `---` kozotti fejlec {mezo: ertek} dictje (egyszeru kulcs: ertek)."""
    if not sorok or sorok[0].strip() != '---':
        return {}
    fej = {}
    for sor in sorok[1:]:
        if sor.strip() == '---':
            break
        if ':' in sor:
            k, _, v = sor.partition(':')
            fej[k.strip()] = v.strip().strip('"')
    return fej


def _e25_feladat_allapotok():
    """{feladat_szam(str): allapot} az F*_BRIEF.md es egyeb *_BRIEF.md fejlecekbol."""
    allapotok = {}
    try:
        nevek = sorted(os.listdir(SZ_ROOT()))
    except OSError:
        return allapotok
    for nev in nevek:
        if not nev.endswith('_BRIEF.md'):
            continue
        try:
            fej = _e25_fejlec(md_olvasas(os.path.join(SZ_ROOT(), nev)))
        except (OSError, UnicodeDecodeError):
            continue
        if fej.get('feladat') and fej.get('allapot'):
            allapotok[fej['feladat']] = fej['allapot']
    return allapotok


def SZ_ROOT():
    return ROOT


def e25_dontes_atvezetes(fajlok):
    talalatok = []
    tabla = os.path.join(ROOT, *E25_TABLA.split('/'))
    if not os.path.exists(tabla):
        return talalatok
    ma = MA or datetime.date.today()
    allapotok = None
    for sorszam, d in dict_sorok_sorszammal(tabla):
        def hiba(reszlet):
            talalatok.append(Talalat('E25', 'HIBA', E25_TABLA, sorszam, reszlet))

        forras = d.get('dontes_forras', '')
        fajl_resz, _, azonosito = forras.partition('#')
        erintett = d.get('erintett_fajl', '')
        ok = True
        # (c) hivatkozasok
        if not fajl_resz or not azonosito:
            hiba('dontes_forras nem `fajl#azonosito` alaku: %r' % forras)
            ok = False
        else:
            forras_ut = os.path.join(ROOT, *fajl_resz.split('/'))
            if not os.path.exists(forras_ut):
                hiba('a dontes_forras fajlja nem letezik: %s' % fajl_resz)
                ok = False
            else:
                szoveg = chr(10).join(md_olvasas(forras_ut))
                if not re.search(r'\b%s\b' % re.escape(azonosito), szoveg):
                    hiba('a(z) %s azonosito nem szerepel a(z) %s fajlban' % (azonosito, fajl_resz))
                    ok = False
        erintett_ut = os.path.join(ROOT, *erintett.split('/')) if erintett else ''
        if not erintett or not os.path.exists(erintett_ut):
            hiba('az erintett_fajl nem letezik: %r' % erintett)
            ok = False
        try:
            tilos = re.compile(d.get('tilos_minta', ''))
            if not d.get('tilos_minta'):
                raise re.error('ures minta')
        except re.error as e:
            hiba('hibas tilos_minta (%s): %r' % (e, d.get('tilos_minta')))
            ok = False
        atm = None
        if d.get('atmeneti_jeloles'):
            try:
                atm = re.compile(d['atmeneti_jeloles'])
            except re.error as e:
                hiba('hibas atmeneti_jeloles (%s): %r' % (e, d.get('atmeneti_jeloles')))
                ok = False
        try:
            datum = datetime.date.fromisoformat(d.get('datum', ''))
        except ValueError:
            hiba('a datum nem EEEE-HH-NN: %r' % d.get('datum'))
            ok = False
            datum = None
        if not ok:
            continue
        # (a) regi allapot az erintett fajlban
        sorok = md_olvasas(erintett_ut)
        if _e25_fejlec(sorok).get('tipus') != 'archiv':
            talalat_sorok = [i for i, s in enumerate(sorok, 1) if tilos.search(s)]
            if talalat_sorok:
                van_atm = atm is not None and any(atm.search(s) for s in sorok)
                szint = 'JELENTES' if van_atm else 'FIGYELMEZTETES'
                talalatok.append(Talalat(
                    'E25', szint, erintett, talalat_sorok[0],
                    '%s: a dontes elotti allapot (%s) %d helyen%s'
                    % (forras, d['tilos_minta'], len(talalat_sorok),
                       ' -- atmeneti jelolessel' if van_atm else '')
                ))
        # (b) regota allo tovabbvivo feladat
        tv = d.get('tovabbvivo_feladat', '').strip()
        if tv:
            if allapotok is None:
                allapotok = _e25_feladat_allapotok()
            allapot = allapotok.get(tv)
            if allapot in E25_NYITOTT_ALLAPOTOK and (ma - datum).days > E25_HATARNAP:
                talalatok.append(Talalat(
                    'E25', 'FIGYELMEZTETES', E25_TABLA, sorszam,
                    '%s: a #%s tovabbvivo feladat allapota %s, a dontes (%s) ota %d nap telt el'
                    % (forras, tv, allapot, d['datum'], (ma - datum).days)
                ))
    return talalatok


# --------------------------------------------------------------------------
# E26 -- veglegesszam az agon (F30_SZAMOZAS_BRIEF.md SZ.3)
# --------------------------------------------------------------------------
# Az E17 nevet a DT3, az E18-at a feladatkovetes, az E19-et a szotari
# forditas, az E20-E24-et mas feladatok foglaljak, az E25 a dontes-
# atvezetes. Ez a kovetkezo szabad szam. (F37: az E20 a tanulmany kotelezo
# szakaszai; a tervezett E21-E24 az E13/E8/E9/E12 bovitesekent valosult meg,
# DT-F37-8 -- a szamuk szabad maradt, de ujrahasznositasuk elott l.
# naplok/T0_felmeres.md 3. pont.)
#
# PR-en (nem push-esemenynel: a main-en a `szamkiosztas` Action ad szamot)
# a diff nem hozhat letre uj veglegesszamot:
#   (a) a DONTESEK.md `| DT<n> |` soraban, a NYITOTT_FELADATOK.md
#       `- **N<n>` felsorolasaban, a FELADATOK.md Dontesnaplo `| D<n> |`
#       soraban nem jelenhet meg a base-ben nem letezo vegleges azonosito;
#   (b) hozzaadott sor nem hivatkozhat a base-beli legnagyobbnal nagyobb
#       DT<n>-re (minden .md/.tsv) vagy N<n>-re (.md, 1-3 jegyu);
#   (c) a helyorzok (DT-F<nn>, N-F<nn>, D-F<nn>) definicioja a fejben egyedi.
# Kivetel: a commit-uzenetben `SZÁMKIOSZTÁS-SZÁNDÉKOS:` kezdetu sor
# (pl. egy regi, hibas szam atszamozasa) -- mint az E5 torles-jelolese.
# Fajlszintu (D8): HIBA, ha a PR ilyet hoz.

E26_UZENET = 'Az ágon helyőrző kell (DT-F<nn>), a végleges számot a merge adja.'
E26_SZANDEKOS = re.compile(r'^\s*(SZÁMKIOSZTÁS-SZÁNDÉKOS|SZAMKIOSZTAS-SZANDEKOS):', re.MULTILINE)
_E26_FAJL = {'DT': 'DONTESEK.md', 'N': 'NYITOTT_FELADATOK.md', 'D': 'FELADATOK.md'}
_E26_VEGLEGES_DEF = {
    'DT': re.compile(r'^\|\s*(DT\d+)\s*\|'),
    'N': re.compile(r'^\s*(?:[-*]|\d+\.)\s*\**\s*(N\d{1,3})(?![A-Za-z0-9])'),
    'D': re.compile(r'^\|\s*(D\d+)\s*\|'),
}
_E26_HELYORZO_DEF = {
    'DT': re.compile(r'^\|\s*(DT-F\d+[a-z]?)\s*\|'),
    'N': re.compile(r'^\s*(?:[-*]|\d+\.)\s*\**\s*(N-F\d+[a-z]?)(?![A-Za-z0-9])'),
    'D': re.compile(r'^\|\s*(D-F\d+[a-z]?)\s*\|'),
}
_E26_DT_HIVATKOZAS = re.compile(r'(?<![A-Za-z0-9-])DT(\d+)(?![A-Za-z0-9])')
_E26_N_HIVATKOZAS = re.compile(r'(?<![A-Za-z0-9-])N(\d{1,3})(?![A-Za-z0-9])')
_E26_HUNK_FEJLEC = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@')
_E26_KIZART_FAJL = {
    'F30_SZAMOZAS_BRIEF.md',
    'eszkozok/szamkiosztas.py',
    'eszkozok/ellenorzes/szabalyok.py',
    'eszkozok/ellenorzes/tesztek/test_szabalyok.py',
    'eszkozok/ellenorzes/tesztek/test_szamkiosztas.py',
}


def _e26_git_fajl(ref, relut):
    try:
        return subprocess.check_output(
            ['git', 'show', '%s:%s' % (ref, relut)],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return ''


def _e26_definiciok(szoveg, minta):
    ki = []
    for sor in szoveg.splitlines():
        m = minta.match(sor)
        if m:
            ki.append(m.group(1))
    return ki


def e26_vegleges_szam_agon(base_ref, head_ref, commit_uzenet='', esemeny=''):
    talalatok = []
    if not base_ref or not head_ref or esemeny == 'push':
        return talalatok
    if E26_SZANDEKOS.search(commit_uzenet or ''):
        return talalatok

    def hiba(fajl, sor, reszlet):
        talalatok.append(Talalat('E26', SZINT['E26'], fajl, sor, '%s %s' % (reszlet, E26_UZENET)))

    legnagyobb = {}
    for kulcs, relut in _E26_FAJL.items():
        base_sz = _e26_git_fajl(base_ref, relut)
        head_sz = _e26_git_fajl(head_ref, relut)
        base_def = set(_e26_definiciok(base_sz, _E26_VEGLEGES_DEF[kulcs]))
        for az in _e26_definiciok(head_sz, _E26_VEGLEGES_DEF[kulcs]):
            if az not in base_def:
                hiba(relut, 0, 'új végleges azonosító: %s.' % az)
                base_def.add(az)
        helyorzok = _e26_definiciok(head_sz, _E26_HELYORZO_DEF[kulcs])
        for az in sorted({h for h in helyorzok if helyorzok.count(h) > 1}):
            hiba(relut, 0, 'a helyőrző kétszer definiált: %s.' % az)
        if kulcs == 'DT':
            szamok = [int(x) for x in re.findall(r'\bDT(\d+)\b', base_sz)]
        elif kulcs == 'N':
            szamok = [int(x) for x in re.findall(r'\bN(\d{1,3})\b', base_sz)]
        else:
            szamok = []
        legnagyobb[kulcs] = max(szamok) if szamok else 0

    try:
        kimenet = subprocess.check_output(
            ['git', 'diff', '--unified=0', '%s..%s' % (base_ref, head_ref), '--', '*.md', '*.tsv'],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return talalatok
    fajl = None
    sorszam = 0
    jelentett = set()
    for sor in kimenet.splitlines():
        if sor.startswith('diff --git'):
            m = re.search(r' b/(\S+)$', sor)
            fajl = m.group(1) if m else None
            if fajl and (fajl in _E26_KIZART_FAJL
                         or fajl.startswith(('konkordancia/', 'generalt_proba/', 'beerkezo/'))):
                fajl = None
            continue
        m = _E26_HUNK_FEJLEC.match(sor)
        if m:
            sorszam = int(m.group(1))
            continue
        if fajl is None or not sor.startswith('+') or sor.startswith('+++'):
            continue
        szoveg = sor[1:]
        for m in _E26_DT_HIVATKOZAS.finditer(szoveg):
            if int(m.group(1)) > legnagyobb['DT'] and ('DT', m.group(0)) not in jelentett:
                jelentett.add(('DT', m.group(0)))
                hiba(fajl, sorszam, 'a %s szám a main-en még nem létezik.' % m.group(0))
        if fajl.endswith('.md'):
            for m in _E26_N_HIVATKOZAS.finditer(szoveg):
                if int(m.group(1)) > legnagyobb['N'] and ('N', m.group(0)) not in jelentett:
                    jelentett.add(('N', m.group(0)))
                    hiba(fajl, sorszam, 'a %s szám a main-en még nem létezik.' % m.group(0))
        sorszam += 1
    return talalatok


SZABALYOK_FUGGVENYEI = {
    'E2': e2_ellenorizve_proveniencia,
    'E3': e3_proveniencia_mezo_ures_vagy_ellenorizve,
    'E4': e4_teljes_scan_naplo_es_dontes,
    'E6': e6_tematikus_forras_es_tabla,
    'E7': e7_bekerult_de_nincs_tablaban,
    'E8': e8_igehely_format,
    'E9': e9_angol_sense,
    'E10': e10_spirit_lelek,
    'E11': e11_cremer_nidntte_nidotte,
    'E12': e12_proveniencia_prozaban,
    'E13': e13_kiejtes_hianya,
    'E14': e14_jelentes_szoveg_angol,
    'E15': e15_szpa_idezet_hossz,
    'E19': e19_szotari_forditas_hiany,
    'E20': e20_kotelezo_szakaszok,
    'E25': e25_dontes_atvezetes,
}


# ---------------------------------------------------------------------------
# E27 -- hivatkozas-ellenorzes (F40_HIVATKOZAS_ELLENORZES_BRIEF.md)
# ---------------------------------------------------------------------------
# A brief munkaneve E25 volt (H5), de az E25 (dontes-atvezetes) es az E26
# (veglegesszam az agon) mar foglalt, az E17/E18/E19-et is mas szabaly viszi;
# a kovetkezo szabad szam az E27 (eltérés a briefhez képest, jelezve).
#
# A: a FELADATOK.md / NYITOTT_FELADATOK.md backtickes utvonalai leteznek-e;
# B: a `claude/...` agnevek leteznek-e a tavoli repoban (egy ls-remote);
# C: a 7-40 jegyu hexa commit-azonositok leteznek-e;
# D: a *_BRIEF.md fejlec `olvas` mezojenek utvonalai leteznek-e (csak az
#    utvonalak; a fejlec ervenyessege az E18-e, DT-F40b);
# E: a PR altal torolt/atnevezett fajl megmaradt-e hivatkozaskent.
# Hatokor (DT-F40a): a FELADATOK.md generalt blokkjanak nyitott soran a
# hianyzo fajl/commit mindig HIBA, az ag csak FIGYELMEZTETES; az `olvas`
# hianyzo fajlja HIBA, kiveve ha lezart a brief, vagy barmely nem lezart
# feladat `ir`-je fedi (DT-F40c: FIGYELMEZTETES); a Kesz szakasz fajlhianya FIGYELMEZTETES; minden egyeb a
# diff altal hozzaadott/modositott sorokra vonatkozik (D8: a regi, a PR altal
# nem erintett talalat csak JELENTES); az E-ellenorzes a PR sajat hibaja,
# ezert mindig HIBA. A szabaly FAJLSZINTU (a futtat.py nem
# leminositi), mert a diff-hatokort maga kezeli.

E27_KOVETO_FAJLOK = ('FELADATOK.md', 'NYITOTT_FELADATOK.md')
# a "Kesz"/"Lezarva" szakaszok: ott az ag/fajl hianya normalis (H2)
E27_KESZ_CIMSOROK = ('kész', 'lezárva', 'korábbi, szám nélküli lezárt')
E27_UTVONAL_VEG = ('.md', '.tsv', '.py', '.json', '.yml')
E27_UTVONAL_KARAKTER = re.compile(r'^[A-Za-z0-9_./-]+$')
E27_BACKTICK = re.compile(r'`([^`\n]+)`')
E27_AG = re.compile(r'(?<![A-Za-z0-9_./-])claude/[A-Za-z0-9._/-]*[A-Za-z0-9_]')
E27_HEXA = re.compile(r'(?<![A-Za-z0-9_./-])[0-9a-f]{7,40}(?![A-Za-z0-9_])')
E27_CSAK_CHATBEN = 'csak chatben'
# DT-F09h: szűk kivétel -- a gitignore-olt `konkordancia/_nyers/` alatti hivatkozás csak akkor engedett, ha
# ugyanabban a sorban ott a jelölő (a hivatkozott fájl opcionális, a kód hiányában is működik). Általános
# `_nyers/` kivétel nincs: a jelöletlen hivatkozás továbbra is HIBA.
E27_OPCIONALIS_NYERS_ELOTAG = 'konkordancia/_nyers/'
E27_OPCIONALIS_JELOLO = '(opcionális, DT-F09h)'
E27_KIZART_KONYVTAR = ('.git', 'beerkezo', 'node_modules', 'konkordancia', '__pycache__')


def _e27_sorok(szoveg):
    """CRLF-tűrő sorbontás (a git is csak a sorvégeknél bont)."""
    sorok = re.split(r'\r\n|\n|\r', szoveg)
    if sorok and sorok[-1] == '':
        sorok.pop()
    return sorok


def _e27_olvas(relut):
    try:
        with open(os.path.join(ROOT, *relut.split('/')), 'rb') as f:
            return f.read().decode('utf-8', errors='replace')
    except OSError:
        return None


def _e27_tavoli_agak():
    """A tavoli `origin` againak halmaza, vagy None, ha nem eleheto
    (token/halozat hiany): ilyenkor a B-ellenorzes nem dont, csak jelez."""
    try:
        kimenet = subprocess.check_output(
            ['git', 'ls-remote', '--heads', 'origin'],
            cwd=ROOT, stderr=subprocess.DEVNULL, timeout=60).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError, subprocess.TimeoutExpired):
        return None
    agak = set()
    for sor in kimenet.splitlines():
        resz = sor.split('\t')
        if len(resz) == 2 and resz[1].startswith('refs/heads/'):
            agak.add(resz[1][len('refs/heads/'):])
    return agak


def _e27_commit_van(az):
    try:
        subprocess.check_output(
            ['git', 'cat-file', '-e', '%s^{commit}' % az],
            cwd=ROOT, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def _e27_diff_statusz(base_ref, head_ref):
    """{regi_ut: 'D' | 'R'} a torolt es atnevezett fajlokra."""
    try:
        kimenet = subprocess.check_output(
            ['git', 'diff', '--name-status', '-M', '%s..%s' % (base_ref, head_ref)],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return {}
    ki = {}
    for sor in kimenet.splitlines():
        resz = sor.split('\t')
        if len(resz) >= 2 and resz[0][:1] in ('D', 'R'):
            ki[resz[1]] = resz[0][:1]
    return ki


def _e27_hozzaadott_sorok(base_ref, head_ref, relut):
    from kozos import git_diff_hozzaadott_sorok
    return git_diff_hozzaadott_sorok(base_ref, head_ref, relut)


def _e27_utvonal_jelolt(szoveg):
    """A backtickes szovegbol a fajlutvonal (horgony nelkul), vagy None."""
    s = szoveg.strip().split('#')[0]
    if not s or s.startswith('/') or not E27_UTVONAL_KARAKTER.match(s):
        return None
    if '/' not in s and not s.endswith(E27_UTVONAL_VEG):
        return None
    if s.startswith('claude/'):
        return None  # agnev: a B-ellenorzes dolga
    if '/' in s and not s.endswith('/') and not s.endswith(E27_UTVONAL_VEG):
        # kiterjesztes nelkuli `a/b` (pl. szervezet/repo, tort): csak akkor
        # fajlutvonal, ha az elso szakasza letezo repo-beli bejegyzes
        if not os.path.exists(os.path.join(ROOT, s.split('/')[0])):
            return None
    if s.startswith(('./', '../', 'http')) or '//' in s:
        return None
    return s


_E27_ALAPNEVEK = {}


def _e27_alapnevek():
    """A repo fajljainak alapnev-halmaza (git ls-files, tartalekkent os.walk):
    a konyvtar nelkuli `ellenoriz.py` alakú rovid hivatkozas akkor jo, ha
    van ilyen nevu fajl a repoban (a kovetkezo/feladatok szovegei igy irnak)."""
    kulcs = ROOT
    if kulcs in _E27_ALAPNEVEK:
        return _E27_ALAPNEVEK[kulcs]
    nevek = set()
    try:
        kimenet = subprocess.check_output(
            ['git', 'ls-files'], cwd=ROOT, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace')
        for sor in kimenet.splitlines():
            nevek.add(sor.rsplit('/', 1)[-1])
    except (subprocess.CalledProcessError, OSError):
        pass
    if not nevek:
        for _gy, mappak, fajlok in os.walk(ROOT):
            mappak[:] = [m for m in mappak if not m.startswith('.')]
            nevek.update(fajlok)
    _E27_ALAPNEVEK[kulcs] = nevek
    return nevek


def _e27_opcionalis_nyers(relut, sor):
    """True, ha a hivatkozás a gitignore-olt `_nyers/` alá mutat, és a sor jelöli az opcionalitást (DT-F09h)."""
    return relut.startswith(E27_OPCIONALIS_NYERS_ELOTAG) and E27_OPCIONALIS_JELOLO in sor


def _e27_van_ut(relut):
    teljes = os.path.join(ROOT, *relut.rstrip('/').split('/'))
    if relut.endswith('/'):
        return os.path.isdir(teljes)
    if os.path.exists(teljes):
        return True
    if '/' not in relut:
        return relut in _e27_alapnevek()
    return False


def _e27_szakasz_kesz(cimsor):
    c = cimsor.lstrip('#').strip().lower()
    return any(c.startswith(k) for k in E27_KESZ_CIMSOROK)


def _e27_fejlec_mezo(szoveg, kulcs):
    """A brief YAML-fejlecenek `kulcs` mezoje: lista (a skalar egyelemu lista),
    vagy [] ha nincs fejlec / nincs mezo / a mezo hibas. DT-F40b: a fejlec
    ervenyessegenek ellenorzese (lezaras, lista-ertek) az E18-e, ez a
    fuggveny nem jelez, csak olvas."""
    sorok = _e27_sorok(szoveg)
    if not sorok or sorok[0].strip() != '---':
        return []
    veg = None
    for i in range(1, len(sorok)):
        if sorok[i].strip() == '---':
            veg = i
            break
    if veg is None:
        return []
    minta = re.compile(r'^%s:\s*(.*)$' % re.escape(kulcs))
    for i in range(1, veg):
        m = minta.match(sorok[i])
        if not m:
            continue
        ertek = m.group(1).strip()
        if ertek.startswith('['):
            if not ertek.endswith(']'):
                return []
            elemek = [e.strip().strip("'\"") for e in ertek[1:-1].split(',')]
            return [e for e in elemek if e]
        if ertek == '':
            elemek = []
            j = i + 1
            while j < veg and re.match(r'^\s+-\s+', sorok[j]):
                elemek.append(re.sub(r'^\s+-\s+', '', sorok[j]).strip().strip("'\""))
                j += 1
            return elemek
        return [ertek.strip("'\"")]
    return []


def _e27_mezo_sorszam(szoveg, kulcs):
    """A `kulcs:` mezo 1-alapu sorszama a fejlecben (0, ha nincs)."""
    sorok = _e27_sorok(szoveg)
    for i, sor in enumerate(sorok[1:], start=2):
        if sor.strip() == '---':
            break
        if sor.startswith(kulcs + ':'):
            return i
    return 0


def _e27_briefek():
    ki = []
    for gyoker, mappak, fajlok in os.walk(ROOT):
        mappak[:] = [m for m in mappak if m not in E27_KIZART_KONYVTAR and not m.startswith('.')]
        for f in fajlok:
            if f.endswith('_BRIEF.md'):
                ki.append(os.path.relpath(os.path.join(gyoker, f), ROOT).replace(os.sep, '/'))
    return sorted(ki)


def _e27_brief_terkep():
    """{feladatszam: {'brief': relut, 'ir': [...], 'fugg': [...]}} a briefek
    fejleceibol (a generalt blokk sorainak forras-brief nevezesehez es a
    nem lezart feladatok `ir` mezo szerinti lefedettsegehez (DT-F40c))."""
    terkep = {}
    for relut in _e27_briefek():
        szoveg = _e27_olvas(relut)
        if szoveg is None:
            continue
        szam = _e27_fejlec_mezo(szoveg, 'feladat')
        if not szam or not szam[0].isdigit():
            continue
        terkep[int(szam[0])] = {
            'brief': relut,
            'ir': _e27_fejlec_mezo(szoveg, 'ir'),
            'allapot': (_e27_fejlec_mezo(szoveg, 'allapot') or [''])[0],
            'fugg': [int(x) for x in _e27_fejlec_mezo(szoveg, 'fugg') if x.strip().isdigit()],
        }
    return terkep


def _e27_ir_fedi(ir_lista, ut):
    """Az `ir` mezo valamelyik eleme fedi-e az utat: azonos, konyvtar-elotag
    (`naplok/`), vagy joker-minta (`naplok/F40_*`)."""
    import fnmatch
    for e in ir_lista:
        e = e.split('#')[0].strip()
        if not e:
            continue
        if e == ut or (e.endswith('/') and ut.startswith(e)) or fnmatch.fnmatch(ut, e):
            return True
    return False


E27_GENERALT_KEZDET = re.compile(r'<!--\s*GENERÁLT-KEZDET:.*?--cel\s+(\w+)')
E27_GENERALT_VEGE = re.compile(r'<!--\s*GENERÁLT-VÉGE:')
E27_SORSZAM = re.compile(r'^\|\s*(\d+)\s*\|')


def e27_hivatkozas(base_ref=None, head_ref=None, esemeny=''):
    talalatok = []
    hozzaadott_cache = {}

    def jelez(alap, relut, sor, reszlet, kozvetlen=False):
        sz = alap
        if not kozvetlen and not (base_ref and head_ref):
            # diff nelkul (kezi futas, --teljes) nem allapithato meg, mi a PR
            # sajat hibaja: csak JELENTES (mint a D8 elotti teljes mod)
            sz = 'JELENTES'
        elif not kozvetlen and sor:
            if relut not in hozzaadott_cache:
                hozzaadott_cache[relut] = _e27_hozzaadott_sorok(base_ref, head_ref, relut)
            h = hozzaadott_cache[relut]
            if h is not None and sor not in h:
                sz = 'JELENTES'
        talalatok.append(Talalat('E27', sz, relut, sor, reszlet))

    torolt = _e27_diff_statusz(base_ref, head_ref) if (base_ref and head_ref) else {}
    agak = None
    agak_lekerve = False
    terkep = None

    for relut in E27_KOVETO_FAJLOK:
        szoveg = _e27_olvas(relut)
        if szoveg is None:
            continue
        kesz = False
        generalt_nyitott = False   # DT-F40a (a): a FELADATOK.md generalt blokkjanak nyitott sorai
        for sorszam, sor in enumerate(_e27_sorok(szoveg), start=1):
            if sor.startswith('#'):
                kesz = _e27_szakasz_kesz(sor)
            mk = E27_GENERALT_KEZDET.search(sor)
            if mk:
                generalt_nyitott = (relut == 'FELADATOK.md' and mk.group(1) != 'kesz')
            elif E27_GENERALT_VEGE.search(sor):
                generalt_nyitott = False
            nyitott_sor = generalt_nyitott and not kesz
            forras = ''
            if nyitott_sor:
                ms = E27_SORSZAM.match(sor)
                if terkep is None:
                    terkep = _e27_brief_terkep()
                if ms and int(ms.group(1)) in terkep:
                    forras = (' A sor a generált blokkban áll; a javítás a forrás-briefben történik: `%s`.'
                              % terkep[int(ms.group(1))]['brief'])
                else:
                    forras = (' A sor a generált blokkban áll; a javítás a forrás-briefben történik '
                              '(a sor száma nem azonosít briefet).')
            csak_chatben = E27_CSAK_CHATBEN in sor
            latott = set()
            for m in E27_BACKTICK.finditer(sor):
                ut = _e27_utvonal_jelolt(m.group(1))
                if ut is None or ut in latott:
                    continue
                latott.add(ut)
                if ut in torolt:
                    st = 'törölve' if torolt[ut] == 'D' else 'átnevezve'
                    jelez('HIBA', relut, sorszam,
                          'a hivatkozott `%s` a PR-ban %s; frissítsd a mutatót ugyanabban a commitban.' % (ut, st),
                          kozvetlen=True)
                elif not csak_chatben and not _e27_opcionalis_nyers(ut, sor) and not _e27_van_ut(ut):
                    uzenet = 'a hivatkozott fájl/könyvtár nem létezik: `%s`.' % ut
                    if nyitott_sor:      # DT-F40a (a): mindig HIBA, diff-hatokor nelkul
                        jelez('HIBA', relut, sorszam, uzenet + forras, kozvetlen=True)
                    elif kesz:           # DT-F40a (c) / H2: figyelmeztetes
                        jelez('FIGYELMEZTETES', relut, sorszam,
                              uzenet + ' (lezárt szakasz)', kozvetlen=(relut == 'FELADATOK.md'))
                    else:                # DT-F40a (d): diff-hatokoru
                        jelez('HIBA', relut, sorszam, uzenet)
            for m in E27_AG.finditer(sor):
                if not agak_lekerve:
                    agak = _e27_tavoli_agak()
                    agak_lekerve = True
                    if agak is None:
                        jelez('FIGYELMEZTETES', relut, 0,
                              'a távoli ágak nem kérdezhetők le (git ls-remote), a B-ellenőrzés kimarad.',
                              kozvetlen=True)
                if agak is None:
                    break
                ag = m.group(0)
                if ag not in agak:
                    uzenet = 'a hivatkozott ág nem létezik a távoli repóban: `%s`' % ag
                    if nyitott_sor:      # DT-F40a (a): a tervezett (meg nem letezo) ag ervenyes
                        jelez('FIGYELMEZTETES', relut, sorszam,
                              uzenet + ' (nyitott sor: a tervezett ág érvényes).' + forras, kozvetlen=True)
                    elif kesz:
                        jelez('FIGYELMEZTETES', relut, sorszam,
                              uzenet + ' (lezárt szakasz: merge után törölt ág normális).')
                    else:
                        jelez('HIBA', relut, sorszam, uzenet + '.')
            for m in E27_HEXA.finditer(sor):
                az = m.group(0)
                if not (re.search(r'\d', az) and re.search(r'[a-f]', az)):
                    continue
                if not _e27_commit_van(az):
                    uzenet = 'a hivatkozott commit nem létezik: `%s`.' % az
                    if nyitott_sor:      # DT-F40a (a): mindig HIBA
                        jelez('HIBA', relut, sorszam, uzenet + forras, kozvetlen=True)
                    else:
                        jelez('FIGYELMEZTETES', relut, sorszam, uzenet)

    # D: csak az `olvas` mezo utvonalai (DT-F40b: a fejlec-ervenyesseg az E18-e)
    if terkep is None:
        terkep = _e27_brief_terkep()
    brief_szam = {adat['brief']: szam for szam, adat in terkep.items()}
    for relut in _e27_briefek():
        szoveg = _e27_olvas(relut)
        if szoveg is None:
            continue
        sor = _e27_mezo_sorszam(szoveg, 'olvas')
        szam = brief_szam.get(relut)
        lezart = ((_e27_fejlec_mezo(szoveg, 'allapot') or [''])[0] == 'lezarva')
        # DT-F40c (b): barmely nem lezart feladat `ir`-je fedhet (nem csak a `fugg`-beliek)
        elo_feladatok = [a for a in terkep.values() if a['allapot'] != 'lezarva']
        for elem in _e27_fejlec_mezo(szoveg, 'olvas'):
            ut = elem.split('#')[0].strip()
            if not ut or any(c in ut for c in '*<>{} ') or ut.startswith(('http', '/')):
                continue
            if ut in torolt:
                st = 'törölve' if torolt[ut] == 'D' else 'átnevezve'
                jelez('HIBA', relut, sor,
                      'az `olvas` mezőben hivatkozott `%s` a PR-ban %s; frissítsd a mutatót ugyanabban a commitban.' % (ut, st),
                      kozvetlen=True)
            elif not _e27_van_ut(ut):
                if lezart:   # DT-F40c (a): lezart brief bemenete szandekosan eltunhet
                    jelez('FIGYELMEZTETES', relut, sor,
                          'az `olvas` mezőben hivatkozott fájl nem létezik: `%s` (lezárt feladat: a bemenet szándékosan eltűnhetett).' % ut,
                          kozvetlen=True)
                    continue
                elo = [f for f in elo_feladatok if _e27_ir_fedi(f['ir'], ut)]
                if elo:
                    jelez('FIGYELMEZTETES', relut, sor,
                          'az `olvas` mezőben hivatkozott fájl még nem létezik: `%s` (egy nem lezárt feladat állítja elő: `%s`).'
                          % (ut, elo[0]['brief']), kozvetlen=True)
                else:   # DT-F40a (b) / DT-F40c (b): HIBA
                    jelez('HIBA', relut, sor,
                          'az `olvas` mezőben hivatkozott fájl nem létezik: `%s`, és egyetlen nem lezárt feladat `ir` mezője sem fedi.' % ut,
                          kozvetlen=True)
    return talalatok


# ---------------------------------------------------------------------------
# A migrált nézetek engedélyezőlistája (E28, E29) -- F116 (FELADATOK #116),
# naplok/MOTIVUM_FORRAS_ci_terv.md 1. és 2. szakasz
# ---------------------------------------------------------------------------
# A lista kezdetben üres (D2): a #11 veszi fel a sort ugyanabban a commitban,
# amelyben a migrált lap először a forrásból generálódik. Oszlopok: id, fajl
# (a generált nézet repó-relatív útja), cel (a general.py célja), melyseg
# (apparatus | olvasoi), feladat, datum. Olvasás: kozos.dict_sorok_sorszammal
# (split('\t')), a `csv` modul tilos (CLAUDE.md "TSV-olvasás").

E28_LISTA = 'eszkozok/ellenorzes/e28_migralt_nezetek.tsv'
E28_MELYSEGEK = ('apparatus', 'olvasoi')


def _migralt_lista():
    """[(fajl_sorszam, {oszlop: ertek}), ...] -- a lista sorai (a fejlécen
    kívül); hiányzó lista-fájl esetén üres."""
    ut = os.path.join(ROOT, *E28_LISTA.split('/'))
    if not os.path.exists(ut):
        return []
    return [(n, d) for n, d in dict_sorok_sorszammal(ut) if d.get('fajl', '').strip()]


def _lf(szoveg):
    return szoveg.replace('\r\n', '\n')


# --------------------------------------------------------------------------
# E28 -- a generált nézet bájtra egyezik az adat- és forrásrétegből újragenerálttal
# --------------------------------------------------------------------------

# A meglévő három marker-blokkos cél (general.py ELESITHETO: naplo, index, nyitott).
E28_MARKER_CELOK = (
    ('naplo', 'motivumlog/PaRDeS_motivumok.md'),
    ('index', 'Lezart_tematikus_tanulmanyok_index.md'),
    ('nyitott', 'NYITOTT_FELADATOK.md'),
)
# A szabály akkor fut PR-en, ha a változott fájlok között van ezek valamelyike
# (fnmatch; a `*` a `/`-t is fedi), vagy a hatókör valamely generált fájlja.
E28_INDITO_MINTAK = (
    'adat/*.tsv', 'motivumok/*.md', 'eszkozok/*general*.py',
    'sablonok/9_*.md', E28_LISTA,
)
# A futtat.py jelentése ezeket az egy-soros megjegyzéseket írja az E28 alá
# (pl. "E28: 0 migrált nézet"); minden futás elején újra épül.
E28_JEGYZETEK = []

_E28_TS = re.compile(r'GENERÁLT[^\n]*?\bts=(\d{4}-\d{2}-\d{2})')


def _e28_indul(fajlok):
    if '__TELJES__' in fajlok:
        return True
    import fnmatch
    hatokor = {f for _, f in E28_MARKER_CELOK}
    hatokor.update(d['fajl'].strip() for _, d in _migralt_lista())
    for f in fajlok:
        f = f.replace('\\', '/')
        if f in hatokor or any(fnmatch.fnmatch(f, m) for m in E28_INDITO_MINTAK):
            return True
    return False


def _e28_commitolt(relut):
    """A fájl commitolt (HEAD-beli) blobja, a `git show` nyers bájtjaiból UTF-8-cal
    dekódolva, sorvég-konverzió NÉLKÜL: az összevetés bájtra megy, a sorvégnek is
    egyeznie kell (CI-terv 1. szakasz 3. pont). Ha a git nem érhető el vagy a fájl
    nincs a HEAD-ben (helyi, nem commitolt futás), a munkafa-fájl a tartalék: ott a
    sorvég LF-re normalizált (a core.autocrlf miatt), ezért az nem blob-összevetés,
    és a jelentés megjegyzése jelzi; None, ha a fájl az sincs."""
    try:
        nyers = subprocess.run(['git', 'show', 'HEAD:' + relut], cwd=ROOT,
                               capture_output=True, check=True).stdout
        return nyers.decode('utf-8')
    except (subprocess.CalledProcessError, OSError):
        try:
            with open(os.path.join(ROOT, *relut.split('/')), 'rb') as f:
                nyers = f.read()
        except OSError:
            return None
    jegyzet = ('E28: tartalék, nem blob-összevetés (a HEAD-ben nincs meg a fájl vagy a git nem '
               'érhető el): munkafa-fájl, LF-re normalizálva: %s' % relut)
    if jegyzet not in E28_JEGYZETEK:
        E28_JEGYZETEK.append(jegyzet)
    return _lf(nyers.decode('utf-8'))


def _general_modul():
    """A general.py modul (a kód mellől, nem a -- tesztben átállított -- ROOT-ból)."""
    eszkozok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if eszkozok not in sys.path:
        sys.path.insert(0, eszkozok)
    import general
    return general


def _e28_general_futtat(cel, azonosito, datum, kimenet):
    """A general.py alfolyamatként, a repón kívüli `kimenet` könyvtárba;
    (kilépési kód, stderr). A generátor logikája nem duplikálódik."""
    env = dict(os.environ, PARDES_DATUM=datum, PYTHONIOENCODING='utf-8')
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, 'eszkozok', 'general.py'),
         '--cel', cel, '--id', azonosito, '--kimenet', kimenet],
        cwd=ROOT, env=env, capture_output=True)
    return p.returncode, p.stderr.decode('utf-8', errors='replace')


def _e28_generalt_blokkok(cel):
    """[(cel_kulcs, blokk_szoveg)] a general.py saját függvényeivel (a
    `--ellenoriz` útja: blokk_lista_eles); a marker-pár keresése és a törzs
    levágása is a general.py-é (marker_par_keres, blokk_torzs)."""
    G = _general_modul()
    _, motivumok = G.tsv_beolvas(G.MOTIVUMOK_TSV)
    _, elofordulasok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
    blokkok, _hianyzo = G.blokk_lista_eles(
        cel, motivumok, elofordulasok, G.konyv_sorrend_betolt(), set())
    return blokkok


def _e28_marker_torzs(szoveg, cel_kulcs):
    """(torzs, torzs_kezdo_sor_szama) vagy None, ha a marker-pár nincs meg."""
    G = _general_modul()
    talalat = G.marker_par_keres(szoveg, cel_kulcs)
    if not talalat:
        return None
    _, tk, tv, _ = talalat
    return szoveg[tk:tv], szoveg[:tk].count('\n') + 1


def _e28_elso_elteres(a_szoveg, b_szoveg):
    """(index, a_sor, b_sor) az első eltérő sorra (0-alapú index), None ha egyezik."""
    a, b = a_szoveg.split('\n'), b_szoveg.split('\n')
    for i in range(max(len(a), len(b))):
        sa = a[i] if i < len(a) else None
        sb = b[i] if i < len(b) else None
        if sa != sb:
            return i, sa, sb
    return None


def _e28_sor_szoveg(sor):
    return '(nincs sor)' if sor is None else repr(sor[:160])


def e28_generalt_nezet_egyezes(fajlok):
    """E28: a generált nézet bájtra egyezik azzal, amit a generátor a commit
    adat- és forrásrétegéből előállít (CI-terv 1. szakasz). Két ág: (1) a három
    marker-blokkos cél törzs-összevetése (general.py függvényein át);
    (2) a migrált nézetek (engedélyezőlista) újragenerálása a repón kívüli
    ideiglenes könyvtárba, PARDES_DATUM = a commitolt fájl első GENERÁLT
    jelölőjének ts= dátuma, majd bájt-összevetés a commitolt blob nyers bájtjaival (a sorvég is
    számít; csak a git nélküli munkafa-tartalék normalizál, és azt jelzi).
    Elfogadott eltérés nincs; fájlszintű HIBA."""
    import shutil
    import tempfile
    del E28_JEGYZETEK[:]
    talalatok = []
    if not _e28_indul(fajlok):
        E28_JEGYZETEK.append('E28: nem futott (nincs érintett fájl a változások között)')
        return talalatok

    def hiba(relut, sor, reszlet):
        talalatok.append(Talalat('E28', SZINT['E28'], relut, sor, reszlet))

    # (1) marker-blokkok
    for cel, relut in E28_MARKER_CELOK:
        szoveg = _e28_commitolt(relut)
        if szoveg is None:
            hiba(relut, 0, 'a marker-blokkos cél fájlja nem található')
            continue
        try:
            blokkok = _e28_generalt_blokkok(cel)
        except Exception as e:   # a generátor hibája a CI-ban nem lehet csendes
            hiba(relut, 0, 'a general.py --cel %s nem futott le: %s: %s'
                 % (cel, type(e).__name__, e))
            continue
        javit = 'python eszkozok/general.py --cel %s --ir' % cel
        for cel_kulcs, blk in blokkok:
            try:
                talalat = _e28_marker_torzs(szoveg, cel_kulcs)
            except ValueError as e:   # nyitó marker záró pár nélkül (general.marker_par_keres)
                hiba(relut, 0, '%s: %s. Javítás: %s (a hiányzó záró markert a kézi szakaszon kívül '
                     'pótolni kell, majd újragenerálni)' % (cel_kulcs, e, javit))
                continue
            if talalat is None:
                hiba(relut, 0, '%s: a marker-pár hiányzik. Javítás: %s' % (cel_kulcs, javit))
                continue
            torzs, kezdo = talalat
            G = _general_modul()
            generalt = G.blokk_torzs(blk, cel_kulcs)
            el = _e28_elso_elteres(torzs, generalt)
            if el:
                i, sa, sb = el
                hiba(relut, kezdo + i,
                     '%s: a commitolt blokk eltér az újragenerálttól (törzs %d. sora). '
                     'commitolt: %s | generált: %s. Javítás: %s'
                     % (cel_kulcs, i + 1, _e28_sor_szoveg(sa), _e28_sor_szoveg(sb), javit))

    # (2) migrált nézetek
    lista = _migralt_lista()
    if not lista:
        E28_JEGYZETEK.append('E28: 0 migrált nézet')
    else:
        E28_JEGYZETEK.append('E28: %d migrált nézet' % len(lista))
    for sorszam, d in lista:
        relut = d['fajl'].strip()
        cel, azonosito = d.get('cel', '').strip(), d.get('id', '').strip()
        commitolt = _e28_commitolt(relut)
        if commitolt is None:
            hiba(relut, 0, 'a lista %d. sora: a migrált nézet fájlja nem található' % sorszam)
            continue
        m = _E28_TS.search(commitolt)
        if not m:
            hiba(relut, 0, 'nincs GENERÁLT jelölő ts= dátummal: a PARDES_DATUM nem állapítható meg '
                 '(a nézetet a generátor állítja elő, kézi fájl nem kerülhet a listára)')
            continue
        datum = m.group(1)
        javit = 'python eszkozok/general.py --cel %s --id %s --ir' % (cel, azonosito)
        tmp = tempfile.mkdtemp(prefix='e28_')
        try:
            kod, hibakimenet = _e28_general_futtat(cel, azonosito, datum, tmp)
            ut = os.path.join(tmp, *relut.split('/'))
            if kod != 0 or not os.path.exists(ut):
                hiba(relut, 0, 'a generátor nem állította elő a nézetet (kilépési kód %s): %s'
                     % (kod, hibakimenet.strip()[-200:]))
                continue
            with open(ut, 'rb') as f:
                generalt = f.read().decode('utf-8')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        el = _e28_elso_elteres(commitolt, generalt)
        if el:
            i, sa, sb = el
            hiba(relut, i + 1,
                 'a commitolt nézet eltér az újragenerálttól (PARDES_DATUM=%s). '
                 'commitolt: %s | generált: %s. Javítás: %s'
                 % (datum, _e28_sor_szoveg(sa), _e28_sor_szoveg(sb), javit))
    return talalatok


SZABALYOK_FUGGVENYEI['E28'] = e28_generalt_nezet_egyezes


# --------------------------------------------------------------------------
# E29 -- a kiadható kimenetben nulla `belso` jelölés és nulla `【NAPLO`
# --------------------------------------------------------------------------
# Csak a kimenetet ellenőrzi (N-F23b, D5): nem szűr, és nem hívja a generátort.
# A minta-lista forrása a SEMA 3.10.4 jelölő-listája (build-kihagyás: `belso`,
# `SZINT-*`, `INAKTÍV`, `JELÖLT`, `ADAT-HIV`, `ADAT-ÉRTÉK`, `FORRÁSRÉTEG`) és a
# 3.10.3 (`【NAPLO】` mindig belső); ha a SEMA bővül, ez a konstans is bővül.
E29_MINTAK = (
    '【NAPLO', '【NAPLÓ',                  # mindig belso (SEMA 3.10.3)
    'SZINT-KEZDET', 'SZINT-VÉGE',        # a belso jelölői is, bármely értékkel
    'SZINT: belso',                       # a #64 ideiglenes egyjelölős alakja (ADAT-NÉZET)
    'INAKTÍV:', 'JELÖLT:', 'ADAT-HIV:', 'ADAT-ÉRTÉK:', 'FORRÁSRÉTEG',
)
# Az `olvasoi` nézet ezen felül a jelölőket és a proveniencia-sorokat sem viszi.
E29_OLVASOI_TOVABBI = (
    'GENERÁLT-KEZDET', 'GENERÁLT-VÉGE', 'RÉS-KEZDET', 'RÉS-VÉGE', 'proveniencia:',
)


def e29_kiadhato_kimenet_tisztasaga(fajlok):
    """E29: a lista minden `fajl`-ján szöveges keresés (kódkerítésen belül is) a
    mélység szerinti mintákra; bármely találat HIBA (fájlszintű, D6). A `fajlok`
    paramétert nem használja: minden PR-en és --teljes módban fut."""
    talalatok = []
    for sorszam, d in _migralt_lista():
        relut = d['fajl'].strip()
        melyseg = d.get('melyseg', '').strip()
        if melyseg not in E28_MELYSEGEK:
            talalatok.append(Talalat('E29', SZINT['E29'], E28_LISTA, sorszam,
                                     'ismeretlen melyseg: %r (apparatus | olvasoi)' % melyseg))
            continue
        mintak = E29_MINTAK + (E29_OLVASOI_TOVABBI if melyseg == 'olvasoi' else ())
        try:
            with open(os.path.join(ROOT, *relut.split('/')), 'r', encoding='utf-8') as f:
                sorok = _lf(f.read()).split('\n')
        except (IOError, OSError):
            talalatok.append(Talalat('E29', SZINT['E29'], relut, 0,
                                     'a lista %d. sorában megnevezett fájl nem olvasható' % sorszam))
            continue
        for i, sor in enumerate(sorok, start=1):
            for minta in mintak:
                if minta in sor:
                    talalatok.append(Talalat('E29', SZINT['E29'], relut, i, 'minta: %s' % minta))
    return talalatok


SZABALYOK_FUGGVENYEI['E29'] = e29_kiadhato_kimenet_tisztasaga


# --------------------------------------------------------------------------
# E30 -- ékezet nélkül írt magyar szó a PR commit-üzeneteiben (F112, DT-F112a)
# --------------------------------------------------------------------------
# Szókészlet: a base-ág kézi commitjaiban legalább E30_MIN_GYAKORISAG-szor
# előforduló ékezetes szó ékezetlen alakja. A kizárási lista az
# e30_ascii_alakok.tsv (alak, ok, forras). A pontosság az M0 mérésben van:
# naplok/COMMIT_EKEZET_meres.md.
E30_MIN_GYAKORISAG = 3
E30_ALAKOK_TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'e30_ascii_alakok.tsv')
_E30_ACCENT = str.maketrans('áéíóöőúüűÁÉÍÓÖŐÚÜŰ', 'aeiooouuuAEIOOOUUU')
_E30_KOD = re.compile(r'`[^`\n]*`')
_E30_FAJLUT = re.compile(r'\S*[/\\]\S*|\S+\.(?:md|py|tsv|yml|yaml|txt|json|sh|db)\b')
_E30_AZONOSITO = re.compile(r'\b[A-Za-zÁ-ű]*[A-Z0-9][A-Za-z0-9_\-]*\d[A-Za-z0-9_\-]*\b|\b(?:DT|N|E|F|G|D|A|B|M|S)-?[A-Za-z]*\d+[a-z]?\b')
_E30_SZO = re.compile(r'(?<![\w/\\.\-])([a-z]{3,})(?![\w/\\\-=]|\.\w)')
_E30_ACC_SZO = re.compile(r'[a-záéíóöőúüű]*[áéíóöőúüű][a-záéíóöőúüű]*')
E30_GEPI_ELEJE = ('szamkiosztas:',)
E30_GEPI_RESZ = ('FELADATOK.md frissítés (gép)',)


def e30_gepi_e(uzenet):
    elso = (uzenet or '').lstrip().split('\n', 1)[0]
    return elso.startswith(E30_GEPI_ELEJE) or any(r in elso for r in E30_GEPI_RESZ)


def e30_tisztit(uzenet):
    """A magyar szövegrészt hagyja meg: kód, fájlút, azonosító, Co-Authored-By nélkül."""
    sorok = [s for s in (uzenet or '').split('\n') if not s.lower().startswith('co-authored-by:')]
    szoveg = '\n'.join(sorok)
    for minta in (_E30_KOD, _E30_FAJLUT, _E30_AZONOSITO):
        szoveg = minta.sub(' ', szoveg)
    return szoveg


def e30_kizaras(utvonal=E30_ALAKOK_TSV):
    ki = {}
    if not os.path.exists(utvonal):
        return ki
    with open(utvonal, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    for s in sorok[1:]:
        if not s.strip() or s.startswith('#'):
            continue
        mezok = s.split('\t')
        ki[mezok[0]] = mezok[1] if len(mezok) > 1 else ''
    return ki


def e30_szokeszlet(uzenetek, min_gyak=E30_MIN_GYAKORISAG):
    """{ékezetlen alak: ékezetes alak} az ékezetes szavak gyakorisága alapján."""
    from collections import Counter
    szamlalo = Counter()
    for u in uzenetek:
        if e30_gepi_e(u):
            continue
        szamlalo.update(w for w in _E30_ACC_SZO.findall(e30_tisztit(u).lower()) if len(w) >= 3)
    szotar = {}
    for szo, db in szamlalo.most_common():
        if db < min_gyak:
            continue
        szotar.setdefault(szo.translate(_E30_ACCENT), szo)
    return szotar


def e30_jeloltek(uzenet, szotar, kizaras):
    """[(ékezetlen alak, javasolt ékezetes alak)] egy üzenetben, ismétlés nélkül."""
    if e30_gepi_e(uzenet):
        return []
    ki, latott = [], set()
    for m in _E30_SZO.finditer(e30_tisztit(uzenet)):
        szo = m.group(1)
        if szo in latott or szo in kizaras or szo not in szotar or szotar[szo] == szo:
            continue
        latott.add(szo)
        ki.append((szo, szotar[szo]))
    return ki


def e30_commitok(alap, fej):
    """[(rövid hash, üzenet)] az alap..fej kézi, nem-merge commitjaira."""
    kimenet = subprocess.run(
        ['git', 'log', '--no-merges', '--format=%h%x1f%B%x1e', '%s..%s' % (alap, fej) if alap else fej],
        cwd=ROOT, capture_output=True, encoding='utf-8', errors='replace').stdout
    ki = []
    for blokk in kimenet.split('\x1e'):
        if '\x1f' in blokk:
            h, u = blokk.strip('\n').split('\x1f', 1)
            ki.append((h, u))
    return ki


def e30_meres(alap='', fej='origin/main', mag=112, minta=50):
    """M0 mérés (naplok/COMMIT_EKEZET_meres.md). Futtatás a repó gyökeréből:
    python -c "import sys; sys.path.insert(0,'eszkozok/ellenorzes'); import szabalyok as S; S.e30_meres()"
    Kiírja: üzenetszám, jelölt üzenetek, 30 leggyakoribb jelölt alak, és a
    rögzített seedű véletlen minta (hash, alak -> javaslat, környezet)."""
    import random
    from collections import Counter
    commitok = e30_commitok(alap, fej)
    kezi = [(h, u) for h, u in commitok if not e30_gepi_e(u)]
    szotar = e30_szokeszlet([u for _, u in kezi])
    kiz = e30_kizaras()
    talalatok, uzenetek, db = [], 0, Counter()
    for h, u in kezi:
        j = e30_jeloltek(u, szotar, kiz)
        if j:
            uzenetek += 1
        for a, b in j:
            talalatok.append((h, a, b, u))
            db[a] += 1
    print('commit (merge nelkul): %d, gepi kihagyva: %d, kezi: %d' % (len(commitok), len(commitok) - len(kezi), len(kezi)))
    print('szokeszlet: %d, kizaras: %d' % (len(szotar), len(kiz)))
    print('jelolt uzenet: %d, jelolt talalat: %d' % (uzenetek, len(talalatok)))
    print('30 leggyakoribb: ' + ', '.join('%s=%d' % x for x in db.most_common(30)))
    random.Random(mag).shuffle(talalatok)
    for i, (h, a, b, u) in enumerate(talalatok[:minta], 1):
        sor = next((s for s in u.split('\n') if re.search(r'(?<![\w])%s(?![\w])' % a, s)), '')
        print('%2d\t%s\t%s -> %s\t%s' % (i, h, a, b, sor.strip()[:150]))


def e30_ascii_commit(base_ref, head_ref, commit_uzenet='', esemeny=''):
    """E30 (DT-F112a: FIGYELMEZTETES): ekezet nelkul irt magyar szo a PR base..head
    kezi commitjaiban. Push-esemenynel (main) nem fut (G4). Ha nincs base/head
    (kezi futtatas --commit-uzenet-fajl-lal), az atadott szoveget nezi, '-' hash-sel."""
    if esemeny == 'push':
        return []
    if base_ref and head_ref:
        commitok = e30_commitok(base_ref, head_ref)
    elif commit_uzenet:
        commitok = [('-', commit_uzenet)]
    else:
        return []
    commitok = [(h, u) for h, u in commitok if not e30_gepi_e(u)]
    if not commitok:
        return []
    szotar = e30_szokeszlet([u for _, u in e30_commitok('', base_ref or 'HEAD')])
    kiz = e30_kizaras()
    talalatok = []
    for h, u in commitok:
        for a, b in e30_jeloltek(u, szotar, kiz):
            talalatok.append(Talalat('E30', SZINT['E30'], h, 'uzenet',
                                     '`%s` -> `%s` (ekezet nelkul irt magyar szo a commit-uzenetben)' % (a, b)))
    return talalatok


SZINT['E30'] = 'FIGYELMEZTETES'
FAJLSZINTU_SZABALYOK.add('E30')


# ---------------------------------------------------------------------------
# E31 -- a `forras_tanulmany` letezo, reponbeli fajlra mutat (#11 S2, DT250)
# ---------------------------------------------------------------------------
# SEMA 2.2: az adat/elofordulasok.tsv `forras_tanulmany` mezoje repo-relativ
# fajlut (a generalt visszamutato link forrasa, DT66 (a) 5.). Ures ertek
# megengedett (nincs rogzitett forrastanulmany, nem negativ lelet), nem jelez.
# A nem ures ertek HIBA, ha: szokoz a ket vegen; `\` elvalaszto; abszolut ut
# vagy meghajto-elotag; ures, `.` vagy `..` utelem (igy a `./` elotag, a `//`
# es a repobol kilepo ut is); vagy az ut nem letezo fajl. A letezes
# kis-nagybetu-pontos (utelemenkent os.listdir), hogy a Windows-os futas
# ugyanazt mondja, mint a CI Linuxa.
# Az E30 szamot a #112 (F112_COMMIT_EKEZET_BRIEF.md, PR #427) foglalja, ezert
# ez a kovetkezo szabad szam.
# Fajlszintu (D8 nelkul) es mindig fut, a `fajlok` parametertol fuggetlenul:
# egy tanulmanyfajl atnevezese vagy torlese akkor is pirosra forditja, ha a
# tabla nem valtozott (CLAUDE.md: a hivatkozas ugyanabban a commitban frissul).

E31_TABLA = 'adat/elofordulasok.tsv'
E31_MEZO = 'forras_tanulmany'


def _e31_ut_hiba(ertek):
    """None, ha az `ertek` letezo, reponbeli fajl pontos repo-relativ utja;
    kulonben a hiba rovid oka."""
    if ertek != ertek.strip():
        return 'szóköz az érték végén'
    if '\\' in ertek:
        return '`\\` elválasztó (a repó-relatív út `/`-rel tagolt)'
    if ertek.startswith('/') or re.match(r'^[A-Za-z]:', ertek):
        return 'abszolút út'
    reszek = ertek.split('/')
    if any(r in ('', '.', '..') for r in reszek):
        return 'üres, `.` vagy `..` útelem (a repó-relatív út előtag és visszalépés nélküli)'
    hely = ROOT
    for r in reszek:
        try:
            tartalom = os.listdir(hely)
        except (IOError, OSError):
            return 'nem létező fájl'
        if r not in tartalom:
            return 'nem létező fájl'
        hely = os.path.join(hely, r)
    if not os.path.isfile(hely):
        return 'nem fájl (könyvtár)'
    return None


def e31_forras_tanulmany_letezik(fajlok):
    """E31: az adat/elofordulasok.tsv minden nem ures `forras_tanulmany`
    erteke letezo, reponbeli fajlra mutat; az ures ertek nem jelez. HIBA,
    fajlszintu; a `fajlok` parametert nem hasznalja."""
    talalatok = []
    ut = os.path.join(ROOT, *E31_TABLA.split('/'))
    if not os.path.exists(ut):
        return talalatok
    for sorszam, d in dict_sorok_sorszammal(ut):
        ertek = d.get(E31_MEZO, '')
        if ertek == '':
            continue
        ok = _e31_ut_hiba(ertek)
        if ok:
            talalatok.append(Talalat(
                'E31', SZINT['E31'], E31_TABLA, sorszam,
                '%s | %s -- forras_tanulmany=%r: %s' % (d.get('id', ''), d.get('igehely', ''), ertek, ok)))
    return talalatok


SZABALYOK_FUGGVENYEI['E31'] = e31_forras_tanulmany_letezik


# ---------------------------------------------------------------------------
# E32 -- kiosztott helyorzo egy kimeneti string-literalban (#141, DT-F141a)
# ---------------------------------------------------------------------------
# A `szamkiosztas` Action a helyorzoket (DT-F.., N-F.., D-F..) csak az .md/.tsv
# fajlokban szamozza at; az eszkozok/**/*.py string-literaljait nem. Ami egy
# generator kimenetebe (fejlec, proveniencia-sor, uzenet) kerul literalkent,
# az a kiosztas utan is a regi helyorzot irja vissza a kiosztott szam helyere
# (dokumentalt eset: a lexikon `kapcsolodo` blokkja, DT-F127b -> DT277).
# A szabaly AST-alapon jelez: csak a string-literalt nezi (a megjegyzes nincs az
# AST-ben, a docstring es az onallo szoveg-kifejezes kimarad), es csak olyan
# helyorzot, amelyhez a `szamkiosztas:` commitok mar veglegesszamot rendeltek
# (a git logbol; az a helyorzo, amelynek a definicios sora ma is megvan, nem
# kiosztott). Kodot nem modosit, csak jelez.
# Szint: HIBA, de a futtat.py D8-cal JELENTES-re minositi a diff altal nem
# erintett sorokat, --teljes modban pedig minden talalat JELENTES. Hatokor:
# adat nelkuli, fajlokon futo szabaly (HATOKOR_SZABALYOK: --teljes modban a
# '__TELJES__' jelzot kapja; egyebkent a valtozott .py fajlokat nezi).
# Kizaras: (1) a szabalyt es a kiosztast magukat (szamkiosztas.py, szabalyok.py)
# es a tesztfajlokat (eszkozok/ellenorzes/tesztek/, teszt_*.py, test_*.py),
# mert a tesztfixture szandekosan hordoz mintahelyorzot; (2) minden sort, amely
# az `e32-kihagy` (vagy a szamkiosztas `szamkiosztas-kihagy`) jelolest
# tartalmazza -- szandekosan torteneti literal jelolese.

E32_KIZART_FAJLOK = {
    'eszkozok/szamkiosztas.py',
    'eszkozok/ellenorzes/szabalyok.py',
}
E32_KIZART_ELOTAG = ('eszkozok/ellenorzes/tesztek/',)
E32_KIHAGY_JELOLESEK = ('e32-kihagy', 'szamkiosztas-kihagy')
_E32_KIOSZTAS_MINTA = re.compile(r'((?:DT|N|D)-F\d+[a-z]?)\s*→\s*((?:DT|N|D)\d+)')


def _szamkiosztas_modul():
    """Az eszkozok/szamkiosztas.py modul, a kod melletti fajlutrol (importlib),
    a sys.path-tol fuggetlenul."""
    import importlib.util
    ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'szamkiosztas.py')
    spec = importlib.util.spec_from_file_location('szamkiosztas', ut)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _e32_kiosztasok():
    """{helyorzo: veglegesszam} a `szamkiosztas:` commitok uzeneteibol (HEAD
    tortenete), kiveve azokat a helyorzokat, amelyeknek a definicios sora
    ma is megvan (ezek nem kiosztottak). Git nelkul ures dict."""
    try:
        kimenet = subprocess.check_output(
            ['git', 'log', '--format=%B', '--grep=^szamkiosztas:', 'HEAD'],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return {}
    kiosztott = {}
    for h, v in _E32_KIOSZTAS_MINTA.findall(kimenet):
        kiosztott.setdefault(h, v)
    # A szamkiosztas.py-t explicit fajlutrol toltjuk (az eszkozok/ nincs a
    # sys.path-on, ha az E28 nem hivta elobb a _general_modul()-t). Hiba nem
    # nyelodik le: ha a modul nem toltheto be, a szures kimaradasa hamis HIBAt
    # adna, ezert a kivetel felszallhat.
    SK = _szamkiosztas_modul()
    for kulcs in ('DT', 'N', 'D'):
        for h in SK._definiciok(ROOT, kulcs)[0]:
            kiosztott.pop(h, None)
    return kiosztott


def _e32_py_fajlok(fajlok):
    if fajlok and fajlok[0] == '__TELJES__':
        lista = []
        for mappa, almappak, nevek in os.walk(os.path.join(ROOT, 'eszkozok')):
            almappak[:] = [a for a in almappak if a != '__pycache__']
            for nev in nevek:
                if nev.endswith('.py'):
                    lista.append(os.path.relpath(os.path.join(mappa, nev), ROOT).replace(os.sep, '/'))
        return sorted(lista)
    return sorted(f.replace('\\', '/') for f in fajlok
                  if f.replace('\\', '/').startswith('eszkozok/') and f.endswith('.py'))


def _e32_kizart(relut):
    nev = relut.rsplit('/', 1)[-1]
    return (relut in E32_KIZART_FAJLOK or relut.startswith(E32_KIZART_ELOTAG)
            or nev.startswith(('teszt_', 'test_')))


def _e32_dokumentacios_csomopontok(fa):
    """A docstringek es az onallo szoveg-kifejezesek Constant csomopontjainak
    id()-ja (ezeket a szabaly nem nezi)."""
    import ast
    kizart = set()
    for csp in ast.walk(fa):
        if (isinstance(csp, ast.Expr) and isinstance(csp.value, ast.Constant)
                and isinstance(csp.value.value, str)):
            kizart.add(id(csp.value))
    return kizart


def _e32_string_tokenek(szoveg):
    """[(sor, oszlop, nyers_szoveg)] a fajl string-tokenjeibol (STRING es, ha a
    Python tokenizalja, FSTRING_MIDDLE). Tokenizalasi hibanal a lista ures
    (a hivo ilyenkor az AST-sorra esik vissza)."""
    import io
    import tokenize
    tipusok = {tokenize.STRING}
    if hasattr(tokenize, 'FSTRING_MIDDLE'):
        tipusok.add(tokenize.FSTRING_MIDDLE)
    lista = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(szoveg).readline):
            if tok.type in tipusok:
                lista.append((tok.start[0], tok.start[1], tok.string))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return []
    return lista


def _e32_bajt_karakter(sorok, sor, bajt_off):
    """Az `ast` UTF-8 BAJT-offszetet a `tokenize` KARAKTER-offszetere valtja
    a sor szovegen (nem-ASCII karakter a sorban elcsuszatna az osszevetest)."""
    if not sorok or not (0 < sor <= len(sorok)):
        return bajt_off
    return len(sorok[sor - 1].encode('utf-8')[:bajt_off].decode('utf-8', 'ignore'))


def _e32_literal_talalatok(csp, tokenek, minta, sorok=None):
    """[(tenyleges_sor, helyorzo, hely)] egy string-Constantban. Implicit
    osszefuzesnel ('a' 'b' tobb soron) a Constant egyetlen csomopont, amelynek
    lineno-ja az elso sor; ezert a csomopont lineno..end_lineno tartomanyaba eso
    string-tokeneket kulon nezi, es a tokenen beluli sor adja a talalat sorat.
    Token nelkul (tokenizalasi hiba) az AST-sorra esik vissza."""
    kezd = (csp.lineno, _e32_bajt_karakter(sorok, csp.lineno, csp.col_offset))
    veg_sor = getattr(csp, 'end_lineno', None) or csp.lineno
    veg_off = getattr(csp, 'end_col_offset', None)
    veg = (veg_sor, _e32_bajt_karakter(sorok, veg_sor, veg_off) if veg_off is not None else 10 ** 9)
    belul = [t for t in tokenek if kezd <= (t[0], t[1]) < veg]
    if not belul:
        return [(csp.lineno + csp.value.count('\n', 0, m.start()), m.group(0),
                 (id(csp), m.start())) for m in minta.finditer(csp.value)]
    eredmeny = []
    for sor0, _oszlop, nyers in belul:
        for m in minta.finditer(nyers):
            eredmeny.append((sor0 + nyers.count('\n', 0, m.start()), m.group(0),
                             (sor0, _oszlop, m.start())))
    return eredmeny


def e32_kiosztott_helyorzo_literalban(fajlok):
    """E32: `eszkozok/**/*.py` string-literaljaban (nem megjegyzesben, nem
    docstringben) olyan helyorzo all, amelyhez a szamkiosztas mar veglegesszamot
    rendelt. A Talalat sora a helyorzo tenyleges sora (tobbsoros literalnal is)."""
    import ast
    talalatok = []
    py_fajlok = [f for f in _e32_py_fajlok(fajlok) if not _e32_kizart(f)]
    if not py_fajlok:
        return talalatok
    kiosztott = _e32_kiosztasok()
    if not kiosztott:
        return talalatok
    minta = re.compile(r'(?<![A-Za-z0-9-])(?:DT|N|D)-F\d+[a-z]?(?![A-Za-z0-9-])')
    for relut in py_fajlok:
        ut = os.path.join(ROOT, *relut.split('/'))
        try:
            with open(ut, 'rb') as f:
                szoveg = f.read().decode('utf-8')
            fa = ast.parse(szoveg, filename=relut)
        except (IOError, OSError, SyntaxError, UnicodeDecodeError, ValueError):
            continue
        sorok = szoveg.splitlines()
        doku = _e32_dokumentacios_csomopontok(fa)
        tokenek = _e32_string_tokenek(szoveg)
        latott = set()
        for csp in ast.walk(fa):
            if not (isinstance(csp, ast.Constant) and isinstance(csp.value, str)):
                continue
            if id(csp) in doku:
                continue
            for sor, helyorzo, hely in _e32_literal_talalatok(csp, tokenek, minta, sorok):
                if hely in latott:
                    continue
                latott.add(hely)
                uj = kiosztott.get(helyorzo)
                if not uj:
                    continue
                sor_szoveg = sorok[sor - 1] if 0 < sor <= len(sorok) else ''
                if any(j in sor_szoveg for j in E32_KIHAGY_JELOLESEK):
                    continue
                talalatok.append(Talalat(
                    'E32', SZINT['E32'], relut, sor,
                    '`%s` kiosztott helyőrző (a szamkiosztas: %s) áll a string-literálban; '
                    'írd a kiosztott számra, vagy tedd számfüggetlenné a szöveget '
                    '(szándékos történeti literálnál: `e32-kihagy` jelölés a sorban)'
                    % (helyorzo, uj)))
    return talalatok


SZINT['E32'] = 'HIBA'
HATOKOR_SZABALYOK.add('E32')
SZABALYOK_FUGGVENYEI['E32'] = e32_kiosztott_helyorzo_literalban
