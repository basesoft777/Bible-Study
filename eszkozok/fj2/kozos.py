#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kozos.py -- F06_FORRASFELMERES_BRIEF.md: a mero-szkriptek kozos segedfuggvenyei.

TSV-olvasas/iras: split('\t') / '\t'.join() (CLAUDE.md, "TSV-olvasas"); a csv
modul a repo sajat tablain tilos. Kulso, nyers forrasfajlokat (pl. a Nave-jelolt
CSV-i) a hivo szkript a sajat dokumentalt modon olvassa.

Minden kimenet elso sorai '#'-jeles fejlecsorok: forras-URL, commit/verzio,
letoltes datuma, futtatasi parancs (brief 3. lepes). A kimeneti TSV-k
fogyasztoi a '#'-sorokat kihagyjak.
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NAPLOK = os.path.join(REPO, 'naplok')
KONKORDANCIA = os.path.join(REPO, 'konkordancia')
FAJL_LIMIT = 1_000_000  # bajt; brief: fajlonkent legfeljebb 1 MB

SZARAZ = False  # a futtat.py allitja


def ma():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def tisztit(ertek):
    return re.sub(r'[\t\r\n]+', ' ', str(ertek)).strip()


def tsv_olvas(ut):
    """Fejlecsor + sorok (listak); a '#'-sorokat kihagyja."""
    sorok = []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n')
            if not sor or sor.startswith('#'):
                continue
            sorok.append(sor.split('\t'))
    return sorok[0], sorok[1:]


def tsv_ir(ut, fejlec_sorok, oszlopok, sorok):
    """'#' fejlecsorok + oszlopfejlec + sorok. 1 MB-nal nagyobb kimenetet nem ir."""
    szoveg = ''.join('# %s\n' % tisztit(s) for s in fejlec_sorok)
    szoveg += '\t'.join(oszlopok) + '\n'
    for s in sorok:
        if len(s) != len(oszlopok):
            raise ValueError('oszlopszam-elteres: %s' % (s,))
        szoveg += '\t'.join(tisztit(x) for x in s) + '\n'
    if len(szoveg.encode('utf-8')) > FAJL_LIMIT:
        raise ValueError('%s meghaladna az 1 MB-ot' % ut)
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)


def fejlec(forras_url, verzio, parancs):
    return ['forras-URL: %s' % forras_url, 'commit/verzio: %s' % verzio,
            'letoltes datuma: %s' % ma(), 'futtatasi parancs: %s' % parancs]


def futtat(parancs, cwd=None, idokorlat=900):
    return subprocess.run(parancs, cwd=cwd, capture_output=True, text=True,
                          encoding='utf-8', timeout=idokorlat)


def klonoz(url, cel, sparse=None, klon_idokorlat=420):
    """git clone --depth 1 (opcionalisan sparse); (commit, hiba)."""
    if SZARAZ:
        return 'SZARAZ', None
    if os.path.isdir(os.path.join(cel, '.git')):
        return commit_sha(cel), None
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    env_parancs = ['git', 'clone', '--depth', '1', '--quiet']
    if sparse:
        env_parancs += ['--filter=blob:none', '--sparse']
    try:
        r = futtat(env_parancs + [url, cel], idokorlat=klon_idokorlat)
    except subprocess.TimeoutExpired:
        shutil.rmtree(cel, ignore_errors=True)
        return None, 'idokorlat (%d mp) a klonozasnal' % klon_idokorlat
    if r.returncode != 0:
        return None, (r.stderr or r.stdout).strip()[:300]
    if sparse:
        r = futtat(['git', 'sparse-checkout', 'set'] + sparse, cwd=cel)
        if r.returncode != 0:
            return None, (r.stderr or r.stdout).strip()[:300]
    return commit_sha(cel), None


def commit_sha(cel):
    r = futtat(['git', 'rev-parse', 'HEAD'], cwd=cel)
    return r.stdout.strip() if r.returncode == 0 else 'ISMERETLEN'


# --- konyvnevek --------------------------------------------------------

def normalizalo():
    """(step_kis -> magyar, magyar -> step_kis) a Konyv_normalizalo_tabla.tsv-bol."""
    fej, sorok = tsv_olvas(os.path.join(KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'))
    step_mag = {s[0]: s[1] for s in sorok if len(s) >= 2}
    return step_mag, {v: k for k, v in step_mag.items()}


def strong_szam(jel):
    """'H1254', 'H1254a', 'G0086', '1254' -> egesz szam (int) vagy None."""
    m = re.search(r'(\d+)', str(jel))
    return int(m.group(1)) if m else None


_TAHOT = None


def tahot_strongok(prefix_nelkul=True):
    """{igehely (magyar rovidites, pl. '1Móz 1:1'): halmaz(int Strong)};
    a 9000-es (es afeletti) STEPBible-prefixkodok nelkul, ha prefix_nelkul."""
    global _TAHOT
    if _TAHOT is None:
        _TAHOT = {}
        fej, sorok = tsv_olvas(os.path.join(KONKORDANCIA, 'TAHOT_kivonat.tsv'))
        for s in sorok:
            if len(s) < 2 or not s[1].startswith('H'):
                continue
            n = strong_szam(s[1])
            if n is None:
                continue
            _TAHOT.setdefault(s[0], set())
            if prefix_nelkul and n >= 9000:
                continue
            _TAHOT[s[0]].add(n)
    return _TAHOT


# --- licenc- es README-szovegek gyujtese ----------------------------------

LICENC_MAPPA = os.path.join(NAPLOK, 'F06_licenc_szovegek')
LICENC_SOROK = []  # (forras, mentett_fajl, eredeti_ut, karakter)
_LICENC_MINTA = re.compile(r'(?i)^(licen[cs]e|licensing|copying|copyright|notice|readme|credits|terms)')


def licenc_gyujt(forras_id, gyoker, max_melyseg=2):
    """Szo szerint kimasolja a licenc-/README-fajlokat a naplok/F06_licenc_szovegek/ ala
    (fajlonkent legfeljebb 1 MB). Visszaadja a mentett fajlok listajat:
    [(eredeti_relativ_ut, karakterszam)]."""
    talalt = []
    if SZARAZ or not os.path.isdir(gyoker):
        return talalt
    os.makedirs(LICENC_MAPPA, exist_ok=True)
    for mappa, almappak, fajlok in os.walk(gyoker):
        almappak[:] = [a for a in almappak if a != '.git']
        rel_mappa = os.path.relpath(mappa, gyoker)
        melyseg = 0 if rel_mappa == '.' else rel_mappa.count(os.sep) + 1
        if melyseg > max_melyseg:
            almappak[:] = []
            continue
        for fn in sorted(fajlok):
            if not _LICENC_MINTA.match(fn):
                continue
            ut = os.path.join(mappa, fn)
            if os.path.getsize(ut) > FAJL_LIMIT:
                LICENC_SOROK.append((forras_id, '', os.path.relpath(ut, gyoker).replace(os.sep, '/'), -1))
                continue
            with open(ut, encoding='utf-8', errors='replace', newline='') as f:
                szoveg = f.read()
            rel = os.path.relpath(ut, gyoker).replace(os.sep, '/')
            mentett = '%s__%s.txt' % (forras_id, rel.replace('/', '__'))
            with open(os.path.join(LICENC_MAPPA, mentett), 'w', encoding='utf-8', newline='') as f:
                f.write(szoveg)
            LICENC_SOROK.append((forras_id, mentett, rel, len(szoveg)))
            talalt.append((rel, len(szoveg)))
    return talalt


def licenc_index_ir(parancs):
    """INDEX.tsv a gyujtott szovegekrol (a licenc.py ezt olvassa)."""
    if SZARAZ:
        return
    sorok = [(f, m, r, str(k)) for f, m, r, k in LICENC_SOROK]
    ut = os.path.join(LICENC_MAPPA, 'INDEX.tsv')
    if os.path.exists(ut):  # reszleges futtatasnal a korabbi, mas forrasok sorai megmaradnak
        mostani = {s[0] for s in sorok}
        sorok = [tuple(x) for x in tsv_olvas(ut)[1] if x[0] not in mostani] + sorok
    tsv_ir(ut,
           ['F06 licenc-/README-szovegek indexe (a mentett fajl a forras szo szerinti masolata)',
            'letoltes datuma: %s' % ma(), 'futtatasi parancs: %s' % parancs],
           ['forras', 'mentett_fajl', 'eredeti_ut', 'karakter'], sorok)
