#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
szabalyok.py -- CI.0: az E2-E16 ellenorzesek (CI_ELLENORZES_BRIEF.md
"Ellenorzolista" tablazata). Egy szabaly = egy fuggveny, mind
`(fajllista) -> [Talalat, ...]` alaku (E16 kivetel: PR-metaadatot is kap;
E5 kivetel: git diff-et is kap -- l. az egyes fuggvenyek docstringjet).

A HIBA/FIGYELMEZTETES szint a fuggvenyben van rogzitve a brief tablazata
szerint (D4: a heurisztikus E12-E15 FIGYELMEZTETES-sel indul) -- a futtat.py
ezt olvassa ki, nem duplikalja.

Egyik fuggveny sem ir fajlt; a `kozos.py` fajl- es tsv-olvaso segedei
felett dolgoznak.
"""

import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kozos import (
    ROOT, ADAT, Talalat, md_olvasas, dict_sorok, szakaszokra_bont,
    repo_ut,
)

SZINT = {
    'E2': 'HIBA', 'E3': 'HIBA', 'E4': 'HIBA', 'E5': 'HIBA', 'E6': 'HIBA',
    'E7': 'HIBA', 'E8': 'HIBA', 'E9': 'HIBA', 'E10': 'HIBA', 'E11': 'HIBA',
    'E12': 'FIGYELMEZTETES', 'E13': 'FIGYELMEZTETES', 'E14': 'FIGYELMEZTETES',
    'E15': 'FIGYELMEZTETES', 'E16': 'HIBA',
}


# --------------------------------------------------------------------------
# E2 -- "ellenorizve" jeloles csak proveniencia-sorral egy szakaszban
# --------------------------------------------------------------------------

JELOLES_MINTA = re.compile(
    r'ellenőrizve|STEPBible-ellenőrizve|🔍|🔬\s*valódi kutatás'
)
PROVENIENCIA_MINTA = re.compile(
    r'scope\s*=.*\|.*forras\s*=.*\|.*ts\s*='
)


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
            for i in range(eleje, vege):
                sor = sorok[i]
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
    sorok = dict_sorok(elofordulasok_ut)
    for n, d in enumerate(sorok, start=1):
        prov = d.get('proveniencia', '')
        if not prov.strip():
            talalatok.append(Talalat(
                'E3', SZINT['E3'], 'adat/elofordulasok.tsv', n,
                '%s | %s -- proveniencia ures' % (d.get('id', ''), d.get('igehely', ''))
            ))
        elif 'ellenőrizve' in prov or 'ellenorizve' in prov:
            talalatok.append(Talalat(
                'E3', SZINT['E3'], 'adat/elofordulasok.tsv', n,
                '%s | %s -- proveniencia="%s"' % (d.get('id', ''), d.get('igehely', ''), prov[:80])
            ))
    return talalatok


# --------------------------------------------------------------------------
# E4 -- friss teljes kereses (auditok.tsv) -> naplo fajl + minden jelolt dontese
# --------------------------------------------------------------------------

TELJES_SCAN_LEPESEK = {'B3'}  # "3. teljes OSZ/UJSZ scan" -- CLAUDE.md het lepes


def e4_teljes_scan_naplo_es_dontes(fajlok):
    talalatok = []
    auditok_ut = os.path.join(ADAT, 'auditok.tsv')
    jeloltek_ut = os.path.join(ADAT, 'jeloltek.tsv')
    if not (os.path.exists(auditok_ut) and os.path.exists(jeloltek_ut)):
        return talalatok
    auditok = dict_sorok(auditok_ut)
    jeloltek = dict_sorok(jeloltek_ut)

    id_lepesek = {}
    for d in auditok:
        id_lepesek.setdefault(d.get('id', ''), set()).add(d.get('lepes', ''))

    id_jeloltek = {}
    for d in jeloltek:
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


def e5_tartalomvesztes_or(base_ref, head_ref, commit_uzenet=''):
    """Git diff `base_ref..head_ref` -- ha torol ##/### cimsort, vagy egy
    study-/sablonfajlbol 30-nal tobb sort, a commit-uzenetben kell
    'TORLES-SZANDEKOS:' jelolesnek lennie. `base_ref`/`head_ref` hianyaban
    (pl. --teljes mod) [] -- ez a szabaly csak diff-mod ban ertelmezheto."""
    talalatok = []
    if not base_ref or not head_ref:
        return talalatok
    try:
        kimenet = subprocess.check_output(
            ['git', 'diff', '--unified=0', '%s..%s' % (base_ref, head_ref)],
            cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return talalatok

    van_szandekos = 'TÖRLÉS-SZÁNDÉKOS:' in commit_uzenet or 'TORLES-SZANDEKOS:' in commit_uzenet
    aktualis_fajl = None
    torolt_szam = 0
    torolt_cimsor = []

    def lezar():
        if aktualis_fajl is None:
            return
        if van_szandekos:
            return
        if torolt_cimsor:
            for c in torolt_cimsor:
                talalatok.append(Talalat(
                    'E5', SZINT['E5'], aktualis_fajl, 0,
                    'torolt cimsor "TÖRLÉS-SZÁNDÉKOS:" jeloles nelkul: %s' % c
                ))
        elif torolt_szam > 30:
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
            torolt_szam = 0
            torolt_cimsor = []
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


def e8_igehely_format(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
            if '```' in sor:
                continue
            for minta in TILTOTT_IGEHELY_MINTAK:
                m = minta.search(sor)
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


def e9_angol_sense(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        kodblokkban = False
        for i, sor in enumerate(sorok):
            if sor.strip().startswith('```'):
                kodblokkban = not kodblokkban
                continue
            if kodblokkban:
                continue
            tisztitott = re.sub(r'`[^`]*`', '', sor)
            tisztitott = re.sub(r'"[^"]*"', '', tisztitott)
            tisztitott = re.sub(r'“[^”]*”', '', tisztitott)
            if SENSE_MINTA.search(tisztitott):
                talalatok.append(Talalat(
                    'E9', SZINT['E9'], relut, i + 1, sor.strip()[:150]
                ))
    return talalatok


# --------------------------------------------------------------------------
# E10 -- spirit -> lelek / spiritual -> lelki tiltott forditas
# --------------------------------------------------------------------------

SPIRIT_LELEK_MINTA = re.compile(
    r'\bspirit(ual)?\b[^.\n]{0,25}\blel(ek|ki)\b|\blel(ek|ki)\b[^.\n]{0,25}\bspirit(ual)?\b',
    re.IGNORECASE
)


def e10_spirit_lelek(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
            if SPIRIT_LELEK_MINTA.search(sor):
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


def e11_cremer_nidntte_nidotte(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
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


def e12_proveniencia_prozaban(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        naplo_blokkban = False
        for i, sor in enumerate(sorok):
            if '【NAPLO' in sor or '【NAPLÓ' in sor:
                naplo_blokkban = True
            if naplo_blokkban:
                if '】' in sor:
                    naplo_blokkban = False
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
KIEJTES_UTANA = re.compile(r'^[^\n]{0,40}(–\s*\*?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]|\(\*?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]+\*?\))')


def e13_kiejtes_hianya(fajlok):
    talalatok = []
    for relut in fajlok:
        if not relut.endswith('.md'):
            continue
        try:
            sorok = md_olvasas(repo_ut(relut))
        except (IOError, OSError):
            continue
        for i, sor in enumerate(sorok):
            m = HEBER_GOROG_FUTAM.search(sor)
            if not m:
                continue
            utana = sor[m.end():m.end() + 40]
            if KIEJTES_UTANA.match(utana):
                continue
            talalatok.append(Talalat(
                'E13', SZINT['E13'], relut, i + 1, sor.strip()[:150]
            ))
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
}
