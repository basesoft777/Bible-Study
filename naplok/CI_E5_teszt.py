#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI_E5_teszt.py -- az E5-javitas (szabalyok.py: a >30-sor-torles ag csak
study-/sablonfajlra vonatkozik, es a "TÖRLÉS-SZÁNDÉKOS:" jelolesnek sor
elejen kell allnia, nem eleg, ha a commit-uzenet csak *emliti*) negyesetes
ellenorzese, ideiglenes git worktree-ben, a valodi e5_tartalomvesztes_or()-t
hasznalva.

Minden eset szintetikus (fejlec-mentes, sima szoveges) tartalommal dolgozik
egy-egy valodi study-/sablon-/eszkozok-fajl helyen, hogy a torolt-sor-szam
ag a cimsor-agtol fuggetlenul, elkulonitve legyen tesztelheto:

  A) study-fajlbol 35 sima sor torlese, jeloles nelkul -- piros varva
     (a `%d torolt sor` uzenet, NEM a cimsor-uzenet)
  B) ugyanaz, de a commit-uzenetben sor elejen "TÖRLÉS-SZÁNDÉKOS:" -- zold
  B2) a jelenlegi PR sajat hibajanak regressziós tesztje: ha a jelzes csak
      *emlitve* van a szoveg kozepen (nem sor elejen), NEM szamit
      szandekosnak -- piros varva
  C) eszkozok/*.py fajlbol 35 sor torlese, jeloles nelkul -- zold varva
     (a szabaly nem vonatkozik ra, mert nem study-/sablonfajl)
  D) sablonok/ alatti fajlbol 35 sor torlese, jeloles nelkul -- piros varva

Eredmeny: naplok/CI_E5_teszt.tsv. Kilepesi kod: 0, ha minden eset a vart
eredmenyt adta, kulonben 1.
"""

import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SZINTETIKUS_SOR_SZAM = 60
TOROLT_SOR_SZAM = 35  # > 30, es nem tartalmaz "##"/"###" cimsort


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


def szintetikus_tartalom_ir(path, sorszam=SZINTETIKUS_SOR_SZAM):
    """Fejlec-mentes (nincs '#' a sor elejen), sima szoveges tartalom --
    igy a >30-sor-torles ag a cimsor-agtol fuggetlenul tesztelheto."""
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for i in range(sorszam):
            f.write('teszt-sor %d -- sima szoveg, nem cimsor\n' % i)


def sor_torles_commit(wt, base, rel_path, uzenet):
    """A `base` commitrol elagazva (detached HEAD) egyetlen fajlbol torol
    sorokat, es commitol -- igy az esetek fuggetlenek egymastol, a
    base..head diff nem tartalmazza a tobbi eset valtoztatasat."""
    sh(['git', 'checkout', '--detach', base], cwd=wt)
    path = os.path.join(wt, rel_path)
    with open(path, encoding='utf-8') as f:
        sorok = f.readlines()
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(sorok[TOROLT_SOR_SZAM:])
    sh(['git', 'add', rel_path], cwd=wt)
    return git_commit(wt, uzenet)


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
        py_rel = 'eszkozok/lekerdez.py'
        sablon_rel = 'sablonok/1_PaRDeS_alap_sablon.md'
        if not os.path.isfile(os.path.join(wt, sablon_rel)):
            raise RuntimeError('%s nem letezik a worktree-ben' % sablon_rel)

        # --- alap-commit: szintetikus, fejlec-mentes tartalom mindharom
        #     erintett fajlban, hogy a torolt-sor-szam ag a cimsor-agtol
        #     fuggetlenul tesztelheto legyen ---
        for rel in (study_fajl, py_rel, sablon_rel):
            szintetikus_tartalom_ir(os.path.join(wt, rel))
            sh(['git', 'add', rel], cwd=wt)
        base = git_commit(wt, 'teszt alap: szintetikus, fejlec-mentes tartalom')

        # --- A/B/B2 eset: study-fajlbol 35 sor torles ---
        head_study = sor_torles_commit(
            wt, base, study_fajl, 'A/B/B2 eset: study-fajl torles jeloles nelkul'
        )

        talalatok_a = SZ.e5_tartalomvesztes_or(base, head_study, commit_uzenet='')
        ok_a = len(talalatok_a) > 0 and all(
            'torolt sor' in t.reszlet and 'cimsor' not in t.reszlet
            for t in talalatok_a
        )
        sorok.append(('A', study_fajl, 'piros, "torolt sor" uzenet', str(ok_a)))
        sikerult = sikerult and ok_a

        talalatok_b = SZ.e5_tartalomvesztes_or(
            base, head_study,
            commit_uzenet='TÖRLÉS-SZÁNDÉKOS: teszt A/B eset\n'
        )
        ok_b = len(talalatok_b) == 0
        sorok.append(('B', study_fajl, 'zold (sor elejen jeloles)', str(ok_b)))
        sikerult = sikerult and ok_b

        talalatok_b2 = SZ.e5_tartalomvesztes_or(
            base, head_study,
            commit_uzenet=(
                'A commit leirja, hogy a "TÖRLÉS-SZÁNDÉKOS:" jeloles '
                'mit csinal, de nem sor elejen all.'
            ),
        )
        ok_b2 = len(talalatok_b2) > 0
        sorok.append((
            'B2', study_fajl,
            'piros (csak emlitve, nem sor elejen -- regresszio a PR sajat hibajara)',
            str(ok_b2),
        ))
        sikerult = sikerult and ok_b2

        # --- C eset: eszkozok/*.py fajlbol 35 sor torles ---
        head_py = sor_torles_commit(
            wt, base, py_rel, 'C eset: eszkozok/*.py torles jeloles nelkul'
        )
        talalatok_c = SZ.e5_tartalomvesztes_or(base, head_py, commit_uzenet='')
        ok_c = len(talalatok_c) == 0
        sorok.append(('C', py_rel, 'zold (E5 nem vonatkozik)', str(ok_c)))
        sikerult = sikerult and ok_c

        # --- D eset: sablonok/ alatti fajlbol 35 sor torles ---
        head_sablon = sor_torles_commit(
            wt, base, sablon_rel, 'D eset: sablonfajl torles jeloles nelkul'
        )
        talalatok_d = SZ.e5_tartalomvesztes_or(base, head_sablon, commit_uzenet='')
        ok_d = len(talalatok_d) > 0
        sorok.append(('D', sablon_rel, 'piros (sablonfajl)', str(ok_d)))
        sikerult = sikerult and ok_d

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
