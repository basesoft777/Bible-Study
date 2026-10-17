#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F09_J_tiszta_klon_igazolas.py -- DT-F09h: a verziózott próba reprodukálhatósága VALÓDI tiszta klónon.

`git worktree add --detach <%TEMP% alatti út> HEAD`: a worktree csak a verziózott (HEAD-beli) fájlokat tartalmazza, a
gitignore-olt `konkordancia/_nyers/` nincs meg benne. Ott a 8 motívum _TUDOMANYOS + _TORZSCIKK fájlja egy repón kívüli
ideiglenes könyvtárba generálódik, és bájtra összevetődik a HEAD-beli (verziózott) próba blobjaival
(`generalt_proba/F09_szotar_s2_proba/lexikon/`). A worktree a végén eltávolítódik (try/finally).

    python naplok/F09_J_tiszta_klon_igazolas.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDK = ['ALVIL-001', 'ANTROP-001', 'HAMART-001', 'HODIT-001', 'ISTENTISZT-001', 'KIRALY-001', 'MENNY-001', 'TEREMT-001']


def main():
    tmp = tempfile.mkdtemp(prefix='f09_tiszta_klon_')
    wt = os.path.join(tmp, 'klon')
    kimenet = os.path.join(tmp, 'kimenet')
    kesz = False
    try:
        r = subprocess.run(['git', 'worktree', 'add', '--detach', wt, 'HEAD'], cwd=ROOT, capture_output=True)
        if r.returncode != 0:
            print('HIBA: git worktree add: %s' % r.stderr.decode('utf-8', 'replace')[-300:])
            return 1
        kesz = True
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=wt, capture_output=True).stdout.decode().strip()
        van_nyers = os.path.isdir(os.path.join(wt, 'konkordancia', '_nyers'))
        print('tiszta klón: %s (HEAD %s); konkordancia/_nyers/ a klónban: %s' % (wt, head[:8], van_nyers))
        env = dict(os.environ, PARDES_DATUM='2026-10-17', PYTHONIOENCODING='utf-8')
        for mid in IDK:
            for cel in ('lexikon', 'torzscikk'):
                r = subprocess.run([sys.executable, os.path.join(wt, 'eszkozok', 'general.py'), '--cel', cel, '--id', mid,
                                    '--kimenet', kimenet], cwd=wt, env=env, capture_output=True)
                if r.returncode != 0:
                    print('HIBA: %s %s: %s' % (mid, cel, r.stderr.decode('utf-8', 'replace')[-500:]))
                    return 1
        proba = os.path.join(wt, 'generalt_proba', 'F09_szotar_s2_proba', 'lexikon')
        gen = os.path.join(kimenet, 'lexikon')
        fajlok = sorted(os.listdir(proba))
        # a verziózott próba = a HEAD-beli blob bájtjai (a worktree-ben a git autocrlf CRLF-re alakíthatja a fájlt)
        elter = []
        for f in fajlok:
            blob = subprocess.run(['git', 'show', 'HEAD:generalt_proba/F09_szotar_s2_proba/lexikon/' + f], cwd=ROOT,
                                  capture_output=True).stdout
            ut = os.path.join(gen, f)
            if not (os.path.isfile(ut) and open(ut, 'rb').read() == blob):
                elter.append(f)
        print('bájtra egyező fájl: %d / %d; eltérő: %s' % (len(fajlok) - len(elter), len(fajlok), elter or 'nincs'))
        print('proveniencia: scope=generalt_proba/F09_szotar_s2_proba/lexikon (%d fájl, HEAD %s) vs repón kívüli ideiglenes kimenet '
              '| forras=naplok/F09_J_tiszta_klon_igazolas.py (git worktree add --detach, general.py --cel lexikon|torzscikk, '
              'PARDES_DATUM=2026-10-17, _nyers/ nélkül) | ts=2026-10-17' % (len(fajlok), head[:8]))
        return 0 if (not elter and not van_nyers) else 2
    finally:
        if kesz:
            subprocess.run(['git', 'worktree', 'remove', '--force', wt], cwd=ROOT, capture_output=True)
            subprocess.run(['git', 'worktree', 'prune'], cwd=ROOT, capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)
        print('worktree eltávolítva: %s' % (not os.path.exists(wt)))


if __name__ == '__main__':
    sys.exit(main())
