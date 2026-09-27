#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI_E5_teszt.py -- az E5-javitas (szabalyok.py: a >30-sor-torles ag csak
study-/sablonfajlra vonatkozik) harom esetes ellenorzese, ideiglenes git
worktree-ben, a valodi e5_tartalomvesztes_or()-t hasznalva:

  A) study-fajlbol >30 sor torlese, jeloles nelkul -- E5 piros varva
  B) ugyanaz, de a commit-uzenetben "TÖRLÉS-SZÁNDÉKOS:" -- E5 zold varva
  C) eszkozok/*.py fajlbol >30 sor torlese, jeloles nelkul -- E5 zold varva
     (a szabaly nem vonatkozik ra, mert nem study-/sablonfajl)

Eredmeny: naplok/CI_E5_teszt.tsv. Kilepesi kod: 0, ha mindharom eset a
vart eredmenyt adta, kulonben 1.
"""

import importlib
import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(args, cwd=None, check=True):
    r = subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, encoding='utf-8'
    )
    if check and r.returncode != 0:
        raise RuntimeError('parancs hiba: %r\nstdout:\n%s\nstderr:\n%s' % (
            args, r.stdout, r.stderr
        ))
    return r


def git_commit(wt, uzenet):
    sh(['git', '-c', 'user.email=teszt@example.com', '-c', 'user.name=CI E5 teszt',
        'commit', '-m', uzenet], cwd=wt)
    return sh(['git', 'rev-parse', 'HEAD'], cwd=wt).stdout.strip()


def main():
    wt = tempfile.mkdtemp(prefix='ci_e5_teszt_')
    branch = 'ci-e5-teszt-tmp'
    sorok = []
    sikerult = True
    modul_dir = None
    try:
        sh(['git', 'worktree', 'add', '-b', branch, wt, 'HEAD'], cwd=ROOT)

        modul_dir = os.path.join(wt, 'eszkozok', 'ellenorzes')
        sys.path.insert(0, modul_dir)
        import study_fajlok_szurese as SFS
        import szabalyok as SZ

        study_halmaz = SFS.study_fajlok_halmaza(adat_dir=os.path.join(wt, 'adat'))
        study_fajl = sorted(study_halmaz)[0]
        study_path = os.path.join(wt, study_fajl)

        # --- A + B eset: study-fajlbol >30 sor torles ---
        with open(study_path, encoding='utf-8') as f:
            eredeti_sorok = f.readlines()
        if len(eredeti_sorok) < 40:
            raise RuntimeError(
                '%s csak %d sor -- nem alkalmas a >30-soros torles tesztre'
                % (study_fajl, len(eredeti_sorok))
            )
        with open(study_path, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(eredeti_sorok[40:])
        sh(['git', 'add', study_fajl], cwd=wt)
        base_ab = sh(['git', 'rev-parse', 'HEAD'], cwd=wt).stdout.strip()
        head_ab = git_commit(wt, 'A/B eset: study-fajl torles jeloles nelkul')

        talalatok_a = SZ.e5_tartalomvesztes_or(base_ab, head_ab, commit_uzenet='')
        ok_a = len(talalatok_a) > 0
        sorok.append(('A', study_fajl, 'piros (talalat van)', str(ok_a)))
        sikerult = sikerult and ok_a

        talalatok_b = SZ.e5_tartalomvesztes_or(
            base_ab, head_ab, commit_uzenet='TÖRLÉS-SZÁNDÉKOS: teszt A/B eset'
        )
        ok_b = len(talalatok_b) == 0
        sorok.append(('B', study_fajl, 'zold (nincs talalat)', str(ok_b)))
        sikerult = sikerult and ok_b

        # --- C eset: eszkozok/*.py fajlbol >30 sor torles ---
        py_rel = 'eszkozok/lekerdez.py'
        py_path = os.path.join(wt, py_rel)
        with open(py_path, encoding='utf-8') as f:
            py_sorok = f.readlines()
        if len(py_sorok) < 40:
            raise RuntimeError(
                '%s csak %d sor -- nem alkalmas a >30-soros torles tesztre'
                % (py_rel, len(py_sorok))
            )
        with open(py_path, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(py_sorok[35:])
        sh(['git', 'add', py_rel], cwd=wt)
        base_c = head_ab
        head_c = git_commit(wt, 'C eset: eszkozok/*.py torles jeloles nelkul')

        talalatok_c = SZ.e5_tartalomvesztes_or(base_c, head_c, commit_uzenet='')
        ok_c = len(talalatok_c) == 0
        sorok.append(('C', py_rel, 'zold (E5 nem vonatkozik)', str(ok_c)))
        sikerult = sikerult and ok_c

        fejlec = ['eset', 'fajl', 'varakozas', 'teljesult']
        sorszovegek = ['\t'.join(fejlec)]
        for eset, fajl, varakozas, teljesult in sorok:
            sorszovegek.append('\t'.join([eset, fajl, varakozas, teljesult]))

        cel = os.path.join(ROOT, 'naplok', 'CI_E5_teszt.tsv')
        with open(cel, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorszovegek) + '\n')

        print('\n'.join(sorszovegek))
        print()
        print('OSSZESEN: %s' % ('RENDBEN' if sikerult else 'HIBA'))
        return 0 if sikerult else 1
    finally:
        for m in ('szabalyok', 'study_fajlok_szurese', 'kozos', 'general'):
            sys.modules.pop(m, None)
        if modul_dir is not None and modul_dir in sys.path:
            sys.path.remove(modul_dir)
        sh(['git', 'worktree', 'remove', '--force', wt], cwd=ROOT, check=False)
        sh(['git', 'branch', '-D', branch], cwd=ROOT, check=False)


if __name__ == '__main__':
    sys.exit(main())
