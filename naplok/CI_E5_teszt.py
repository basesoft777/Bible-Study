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
  E) egy study-fajl TELJES torlese, UGYANABBAN a commitban a
     adat/motivumok.tsv-bol a forras_study-hivatkozas is eltavolitva,
     jeloles nelkul -- piros varva. Ez azt a hibat teszteli, amit a
     naplok/ELLENOR_CI_E5.md 2. kore jelzett: ha a study-halmazt csak a
     head-allapotbol epitenenk, egy ilyen PR utan a fajl mar nem szamitana
     study-fajlnak, es a >30-soros ag nem jelezne ra. A javitas: a
     study-halmaz a base_ref ES a head_ref motivumok.tsv-jenek uniojabol
     epul (l. _study_fajlok_halmaza_ref() a szabalyok.py-ban). Az E eset
     emellett a teljes futtat.py-t (minden E2-E16 szabalyt) is lefuttatja
     ugyanerre a base..head parra, hogy dokumentalja, mas szabaly is
     jelez-e ra (l. a script vegi kiiratast es naplok/CI_E5_teszt.md-t).

Eredmeny: naplok/CI_E5_teszt.tsv (+ naplok/CI_E5_teszt_E_futtat.md, az E
eset teljes futtat.py-jelentese). Kilepesi kod: 0, ha minden eset a vart
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


def forras_study_hivatkozas_torol(motivumok_path, torlendo_fajl):
    """A `forras_study` oszlopbol eltavolitja a `torlendo_fajl` bejegyzest
    (';'-vel tagolt lista) -- split('\\t')/'\\t'.join(), a CLAUDE.md
    "TSV-olvasas" szabalya szerint, a `csv` modul nelkul."""
    with open(motivumok_path, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(sorveg)
    zaro_ures = sorok and sorok[-1] == ''
    if zaro_ures:
        sorok = sorok[:-1]
    fejlec_idx = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fejlec = sorok[fejlec_idx].split('\t')
    idx = fejlec.index('forras_study')
    talalt = False
    for i in range(fejlec_idx + 1, len(sorok)):
        if not sorok[i].strip() or sorok[i].startswith('#'):
            continue
        mezok = sorok[i].split('\t')
        resz = [r.strip() for r in mezok[idx].split(';') if r.strip()]
        if torlendo_fajl in resz:
            resz.remove(torlendo_fajl)
            mezok[idx] = ';'.join(resz)
            sorok[i] = '\t'.join(mezok)
            talalt = True
    if not talalt:
        raise RuntimeError(
            '%s nem szerepel a forras_study oszlopban' % torlendo_fajl
        )
    uj_nyers = sorveg.join(sorok) + (sorveg if zaro_ures else '')
    with open(motivumok_path, 'w', encoding='utf-8', newline='') as f:
        f.write(uj_nyers)


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

        # --- E eset: study-fajl teljes torlese + a forras_study-hivatkozas
        #     eltavolitasa a motivumok.tsv-bol, egyazon commitban ---
        sh(['git', 'checkout', '--detach', base], cwd=wt)
        motivumok_path = os.path.join(wt, 'adat', 'motivumok.tsv')
        forras_study_hivatkozas_torol(motivumok_path, study_fajl)
        sh(['git', 'rm', study_fajl], cwd=wt)
        sh(['git', 'add', 'adat/motivumok.tsv'], cwd=wt)
        head_e = git_commit(
            wt,
            'E eset: study-fajl teljes torlese + motivumok.tsv-referencia '
            'eltavolitasa, jeloles nelkul'
        )
        talalatok_e = SZ.e5_tartalomvesztes_or(base, head_e, commit_uzenet='')
        ok_e = len(talalatok_e) > 0
        sorok.append((
            'E', study_fajl,
            'piros (teljes torles + referencia-eltavolitas, union-fix)',
            str(ok_e),
        ))
        sikerult = sikerult and ok_e

        # --- E eset kiegeszito dokumentacio: a TELJES futtat.py (minden
        #     E2-E16 szabaly) lefuttatva ugyanerre a base..head parra, hogy
        #     lathato legyen, mas szabaly is jelez-e ra ezen kivul. Ez NEM
        #     resze a sikerult/HIBA dontesnek -- tisztan dokumentacio. ---
        import futtat as FT
        teljes_eredmeny = FT.fut(
            [study_fajl, 'adat/motivumok.tsv'], False,
            diff_alap=base, diff_fej=head_e, commit_uzenet='',
        )
        e_dokumentacio_sorok = [
            '# E eset -- teljes futtat.py jelentes (dokumentacio, nem resze a sikerult/HIBA dontesnek)',
            '',
            '`base=%s`, `head=%s` (a study-fajl teljes torlese + motivumok.tsv-referencia eltavolitasa, jeloles nelkul)' % (base, head_e),
            '',
        ]
        egyeb_szabaly_is_jelez = False
        for nev in sorted(teljes_eredmeny.keys(), key=lambda n: int(n[1:])):
            talalatok_nev = teljes_eredmeny[nev]
            if not talalatok_nev:
                continue
            if nev != 'E5':
                egyeb_szabaly_is_jelez = True
            e_dokumentacio_sorok.append('## %s (%d talalat)' % (nev, len(talalatok_nev)))
            for t in talalatok_nev[:5]:
                e_dokumentacio_sorok.append('- `%s` `%s:%s` -- %s' % (t.szint, t.fajl, t.sor, t.reszlet))
            e_dokumentacio_sorok.append('')
        e_dokumentacio_sorok.append(
            'Osszegzes: %s' % (
                'az E5-on kivul MAS szabaly is jelez erre a valtoztatasra (l. fent).'
                if egyeb_szabaly_is_jelez else
                'az E5-on kivul EGYETLEN mas E2-E16 szabaly sem jelzett talalatot '
                'erre a valtoztatasra -- az E5 union-fix nelkul ez a tartalomvesztes '
                'szurten athaladna a CI-n.'
            )
        )
        doku_path = os.path.join(ROOT, 'naplok', 'CI_E5_teszt_E_futtat.md')
        with open(doku_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(e_dokumentacio_sorok) + '\n')
        print('\n'.join(e_dokumentacio_sorok))
        print()

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
        for m in ('szabalyok', 'study_fajlok_szurese', 'kozos', 'general', 'futtat'):
            sys.modules.pop(m, None)
        if modul_dir is not None and modul_dir in sys.path:
            sys.path.remove(modul_dir)
        sh(['git', 'worktree', 'remove', '--force', wt], cwd=ROOT, check=False)
        sh(['git', 'branch', '-D', branch], cwd=ROOT, check=False)


if __name__ == '__main__':
    sys.exit(main())
