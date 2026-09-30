#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kozos.py -- CI.0: kozos segedfuggvenyek az eszkozok/ellenorzes/* szabalyokhoz
(l. naplok/../F02_CI_ELLENORZES_BRIEF.md tetellista). Egy fuggveny = egy Talalat
tipus, egy fajl-felderito, es a tsv-olvasas (split('\\t'), a `csv` modul
tilos -- CLAUDE.md "TSV-olvasas" szakasz).

Ezt a modult sem ez a fajl, sem a tobbi ellenorzes/*.py nem futtatja
onallo szkriptkent -- csak a futtat.py hasznalja.
"""

import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ADAT = os.path.join(ROOT, 'adat')

# CLAUDE.md "Ezt olvasd, ezt ne" -- ezeket a nagy archiv/changelog fajlokat a
# szabalyok sem olvassak be egyben (kiveve, ha a szabaly kifejezetten arrol
# szol -- egyik sem szol).
KIZART_FAJLOK = {
    'PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md',
    'PaRDeS_dontesek_CHANGELOG.md',
}
KIZART_UTVONAL_RESZLETEK = (
    os.path.join('motivumlog', 'PaRDeS_motivumok_CHANGELOG.md'),
)

# D14: az ellenorzes sajat naploi/jelentesei -- ezek tartalma (mintasorok,
# datumok, fajlnevek) sose generaljon onhivatkozo talalatot egyik szabalynal
# sem.
KIZART_NAPLO_MINTAK = (
    re.compile(r'^naplok/CI_.*\.md$'),
    re.compile(r'^naplok/ELLENOR_.*\.md$'),
)

# A generalt (kimenet-reteg) konyvtarak/fajlmintak -- CLAUDE.md "Retegek"
# szakasz: "lexikon/[ID]_TUDOMANYOS.md", "lexikon/[ID]_TORZSCIKK.md" kezzel
# szerkeszteni tilos, tehat a legtobb tartalmi szabaly (E5, E7, E8 stb.) nem
# fut le rajuk -- de E11 (Cremer/NIDNTTE/NIDOTTE tiltas) kifejezetten "a
# renderben" is ellenorzendo, tehat arra a szabalyra nem zart ki.
GENERALT_KONYVTARAK = ('generalt_proba',)


def repo_ut(*resz):
    return os.path.join(ROOT, *resz)


def md_olvasas(ut):
    """Egy .md fajl tartalma sorokra bontva (\\n nelkul), UTF-8-kent."""
    with open(ut, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


def tsv_sorok(ut, koment_elojel='#'):
    """A tsv adatsorai listakent (split('\\t')) -- a `#`-fejlecsorokat es az
    ures sorokat kihagyja. A CLAUDE.md "TSV-olvasas" szabalya szerint a
    `csv` modul NEM hasznalhato ezeken a tablakon."""
    sorok = []
    with open(ut, 'r', encoding='utf-8') as f:
        for eredeti in f:
            sor = eredeti.rstrip('\n')
            if not sor.strip():
                continue
            if sor.startswith(koment_elojel):
                continue
            sorok.append(sor.split('\t'))
    return sorok


def tsv_fejlec_es_sorok(ut, koment_elojel='#'):
    """(fejlec_oszlopnevek, adatsorok) -- az elso nem '#'-sor a fejlec."""
    fejlec = None
    adat = []
    with open(ut, 'r', encoding='utf-8') as f:
        for eredeti in f:
            sor = eredeti.rstrip('\n')
            if not sor.strip():
                continue
            if sor.startswith(koment_elojel):
                continue
            if fejlec is None:
                fejlec = sor.split('\t')
                continue
            adat.append(sor.split('\t'))
    return fejlec, adat


def dict_sorok(ut, koment_elojel='#'):
    """A tsv adatsorai {oszlopnev: ertek} dict-kent."""
    fejlec, adat = tsv_fejlec_es_sorok(ut, koment_elojel)
    ki = []
    for sor in adat:
        d = {}
        for i, nev in enumerate(fejlec):
            d[nev] = sor[i] if i < len(sor) else ''
        ki.append(d)
    return ki


def dict_sorok_sorszammal(ut, koment_elojel='#'):
    """[(fajl_sorszam, {oszlopnev: ertek}), ...] -- a fajl_sorszam a
    tenyleges 1-alapu sor a fajlban (nem az adatsor-sorszam), hogy a D8
    diff-hatokorrel osszevethető legyen."""
    fejlec = None
    ki = []
    with open(ut, 'r', encoding='utf-8') as f:
        for i, eredeti in enumerate(f, start=1):
            sor = eredeti.rstrip('\n')
            if not sor.strip():
                continue
            if sor.startswith(koment_elojel):
                continue
            mezok = sor.split('\t')
            if fejlec is None:
                fejlec = mezok
                continue
            d = {}
            for j, nev in enumerate(fejlec):
                d[nev] = mezok[j] if j < len(mezok) else ''
            ki.append((i, d))
    return ki


_HUNK_FEJLEC = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@')


def git_diff_hozzaadott_sorok(base_ref, head_ref, relut):
    """A `relut` fajlban a `base_ref..head_ref` diff altal HOZZAADOTT/
    MODOSITOTT sorok szama (a HEAD-beli, azaz uj fajltartalom sorszamai) --
    D8: a HIBA-szint csak ezekre a sorokra vonatkozik, a fajl regi sorai
    csak JELENTES-t kapnak.

    Ures halmaz, ha nincs base/head (pl. --teljes mod), vagy a git diff
    hibaval ter vissza (pl. uj fajl -- akkor minden sora "hozzaadott",
    ezt kulon kezeljuk lent)."""
    if not base_ref or not head_ref:
        return None
    try:
        kimenet = subprocess.check_output(
            ['git', 'diff', '--unified=0', '%s..%s' % (base_ref, head_ref),
             '--', relut],
            cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return None
    if not kimenet.strip():
        return set()
    sorok = set()
    for sor in kimenet.splitlines():
        m = _HUNK_FEJLEC.match(sor)
        if not m:
            continue
        kezdo = int(m.group(1))
        hossz = int(m.group(2)) if m.group(2) is not None else 1
        for i in range(kezdo, kezdo + hossz):
            sorok.add(i)
    return sorok


def kizart_e(relut):
    relut = relut.replace('\\', '/')
    alap = os.path.basename(relut)
    if alap in KIZART_FAJLOK:
        return True
    for resz in KIZART_UTVONAL_RESZLETEK:
        if relut.endswith(resz.replace('\\', '/')):
            return True
    for konyvtar in GENERALT_KONYVTARAK:
        if relut.startswith(konyvtar + '/') or relut == konyvtar:
            return True
    for minta in KIZART_NAPLO_MINTAK:
        if minta.match(relut):
            return True
    return False


def md_fajlok(alkonyvtarak=None, kizarva_generalt=True):
    """A repo .md fajljai (repo-relativ, '/'-vel), a kizart_e() szurovel.
    `alkonyvtarak`: ha nem None, csak ezek ala eso fajlok (pl. ['tematikus_lezart'])."""
    ki = []
    for gyoker, konyvtarak, fajlok in os.walk(ROOT):
        konyvtarak[:] = [d for d in konyvtarak if d not in ('.git', 'konkordancia', 'node_modules')]
        for fajl in fajlok:
            if not fajl.endswith('.md'):
                continue
            teljes = os.path.join(gyoker, fajl)
            relut = os.path.relpath(teljes, ROOT).replace(os.sep, '/')
            if kizarva_generalt and kizart_e(relut):
                continue
            if alkonyvtarak is not None:
                if not any(relut == a or relut.startswith(a.rstrip('/') + '/') for a in alkonyvtarak):
                    continue
            ki.append(relut)
    return sorted(ki)


class Talalat(object):
    """Egy szabalysertes/figyelmeztetes egy sora: (szabaly, szint, fajl, sor, reszlet)."""

    __slots__ = ('szabaly', 'szint', 'fajl', 'sor', 'reszlet')

    def __init__(self, szabaly, szint, fajl, sor, reszlet):
        self.szabaly = szabaly
        self.szint = szint  # 'HIBA' | 'FIGYELMEZTETES'
        self.fajl = fajl
        self.sor = sor
        self.reszlet = reszlet

    def __repr__(self):
        return '%s:%s %s:%s %r' % (self.szabaly, self.szint, self.fajl, self.sor, self.reszlet)


def szakaszokra_bont(sorok):
    """A markdown sorokat '#'-cimsorok menten szakaszokra bontja.
    Visszaad: lista (cim_sorindex, cim_szoveg, kezdo_sorindex, zaro_sorindex) --
    a zaro_sorindex kizarolagos (a kovetkezo cimsorig, vagy a fajl vegeig)."""
    cimsor_idx = [i for i, s in enumerate(sorok) if s.startswith('#')]
    szakaszok = []
    if not cimsor_idx or cimsor_idx[0] != 0:
        eleje = 0
        vege = cimsor_idx[0] if cimsor_idx else len(sorok)
        szakaszok.append((None, None, eleje, vege))
    for j, idx in enumerate(cimsor_idx):
        vege = cimsor_idx[j + 1] if j + 1 < len(cimsor_idx) else len(sorok)
        szakaszok.append((idx, sorok[idx], idx, vege))
    return szakaszok
