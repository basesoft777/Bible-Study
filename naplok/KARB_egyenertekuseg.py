#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KARB_egyenertekuseg.py -- KARBANTARTAS_BRIEF.md SS1 (Egyenertekuseg,
Mellekhatas-mentesseg) merőszkriptje a KB1 10 szkriptjehez.

v2: a fuggetlen ellenorzes (naplok/ELLENOR_KARB.md) ket hibat talalt a v1-ben:
  (1) a ket ideiglenes worktree utvonala a rendszer temp konyvtaraba volt
      beegetve, ezert utolag nem reprodukalhato;
  (2) a `fajl_sha_egyezik` egyetlen globalis ertek volt, MINDEN sorba
      bemasolva -- nem szkriptenkenti/fajlonkenti eredmeny.

Ez a valtozat argumentumkent kapja a ket commit-shat (--regi-commit,
--uj-commit), a ket worktree-t a REPON BELULI, gitignore-olt
`.claude/kb_worktrees/` ala teszi (l. .gitignore: `.claude/*`), es minden
egyes szkript bare futtatasa UTAN kulon-kulon meri a fajlrendszer-
valtozast, MAJD visszaallitja mindket worktree-t (`git clean -fdx` +
`git checkout -- .`) a kovetkezo szkript merese elott -- igy a
`fajl_sha_egyezik` es az esetleges elteres-lista szkriptenkenti es
fajlonkenti, nem egy egyszeri globalis ellenorzes.

Hasznalat:
    python naplok/KARB_egyenertekuseg.py --regi-commit 68eb348 --uj-commit HEAD

A harom meres szkriptenkent:
  1. Mellekhatas-mentesseg (csak UJ-n): --help tiszta kilepessel es ures
     git status-szal fut-e, es a modul importja nem ir semmit es nem
     general stdout-ot.
  2. Argumentum nelkuli lefutas (mindket masolatban): kilepesi kod es
     stdout/stderr osszevetese -- a masolat sajat abszolut utvonala
     (ROOT-fuggo print-sorok) maszkolva.
  3. Fajl-sha egyezes: a bare futas UTAN, a ket masolat MINDEN fajljanak
     sha256-a egyezik-e -- SZKRIPTENKENT kulon merve, a ket worktree
     kozotti futtatas kozott visszaallitva.

Az eredmeny a naplok/KARB_KB1_egyenertekuseg.tsv-be kerul.
"""

import argparse
import hashlib
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WT_ROOT = os.path.join(ROOT, '.claude', 'kb_worktrees')
KB_REGI = os.path.join(WT_ROOT, 'kb_regi')
KB_UJ = os.path.join(WT_ROOT, 'kb_uj')

SZKRIPTEK = [
    "f3_1_betoltes.py",
    "f3_2_betoltes.py",
    "f3_4_ellenoriz.py",
    "f3_4_elokeszites.py",
    "f3_4_gorog_ellenoriz.py",
    "f3_4_join_potlas.py",
    "f3_4_munkalap_general.py",
    "f3_4_nema_nemtalalat.py",
    "f3_4_zaro_ellenoriz.py",
    "merge_karoli_szofaj.py",
]

# A KB2 (CRLF-tures) is erinti 3 masik szkript forraskodjat (a negyedik,
# f3_4_zaro_ellenoriz.py, mar a SZKRIPTEK listaban van) -- ha az uj_commit
# a KB2-t is tartalmazza, ezek forraskodja is kulonbozik regi/uj kozott,
# fuggetlenul ettol a (KB1-es) merestol.
KB2_EGYEB_SZKRIPTEK = [
    "elofordulas_szamlalo.py",
    "frazis_kereses_pozicio_alapon.py",
    "tahot_zarojeles_phaseA_kivonat.py",
]

# A meres celjatol fuggetlen, a menet sajat naplo-/brief-fajljai -- ezek
# a ket allapot kozott mindig kulonboznek (regi allapotban meg nem
# leteznek), a fajl-sha egyezesbol kizarva.
SAJAT_FAJLOK = {
    "naplok/KARB_KB0_kiindulas.md",
    "naplok/KARB_egyenertekuseg.py",
    "naplok/KARB_KB1_egyenertekuseg.tsv",
    "naplok/KARB_crlf_teszt.py",
    "naplok/KARB_KB2_crlf.tsv",
    "naplok/KARB_KB3_nullaz.py",
    "naplok/KARB_KB3_nullazas.tsv",
    "naplok/KARB_jelentes.md",
    "naplok/ELLENOR_KARB.md",
    "KARBANTARTAS_BRIEF.md",
    "FELADATOK.md",
}


def sh(args, cwd=None, check=True, env=None):
    r = subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=env,
    )
    if check and r.returncode != 0:
        raise RuntimeError("parancs hiba: %r\nstdout:\n%s\nstderr:\n%s" % (
            args, r.stdout, r.stderr))
    return r


def worktree_keszit(path, commit):
    if os.path.isdir(path):
        sh(["git", "worktree", "remove", "--force", path], cwd=ROOT, check=False)
    os.makedirs(WT_ROOT, exist_ok=True)
    sh(["git", "worktree", "add", "--detach", path, commit], cwd=ROOT)


def worktree_visszaallit(path):
    """A worktree-t a sajat HEAD-jere allitja vissza, es eltavolit minden
    nyomkovetett modositast + nem verziozott (bare futtatas altal irt)
    fajlt -- igy a kovetkezo szkript merese tiszta allapotbol indul."""
    sh(["git", "checkout", "--force", "HEAD", "--", "."], cwd=path)
    sh(["git", "clean", "-fdx"], cwd=path)


def worktree_torol(path):
    sh(["git", "worktree", "remove", "--force", path], cwd=ROOT, check=False)


def kornyezet():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def futtat(root, relpath, args):
    proc = subprocess.run(
        [sys.executable, os.path.join("eszkozok", relpath)] + args,
        cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=kornyezet(),
    )
    return proc.returncode, proc.stdout, proc.stderr


def git_status_ures(root):
    proc = sh(["git", "status", "--porcelain"], cwd=root)
    return proc.stdout.strip() == "", proc.stdout


def import_tiszta(root, relpath):
    """A modult importlib-bel importalja egy KULON python-folyamatban, es
    visszaadja, hogy volt-e stdout, valamint hogy a git status tiszta
    maradt-e."""
    modnev = relpath[:-3]
    kod = (
        "import importlib.util, sys\n"
        "spec = importlib.util.spec_from_file_location(%r, r'eszkozok/%s')\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
    ) % (modnev, relpath)
    proc = subprocess.run([sys.executable, "-c", kod], cwd=root,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=kornyezet())
    tiszta_git, _ = git_status_ures(root)
    stdout_ures = proc.stdout.strip() == ""
    return proc.returncode == 0 and stdout_ures and tiszta_git


def sha256_fa(root, kizart_relpathok):
    """{relpath: sha256} minden fajlra a .git kivetelevel es a kizart
    lista nelkul."""
    ki = {}
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        if "__pycache__" in dirnames:
            dirnames.remove("__pycache__")
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if rel == ".git" or rel in kizart_relpathok:
                # ".git" worktree-ben FAJL (gitdir-mutato), nem konyvtar --
                # az os.walk dirnames-alapu kizarasa ezt nem kapja el.
                continue
            with open(full, "rb") as f:
                ki[rel] = hashlib.sha256(f.read()).hexdigest()
    return ki


def maszkol(szoveg, root):
    return szoveg.replace(root, "<ROOT>").replace(root.replace("\\", "/"), "<ROOT>")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--regi-commit", required=True,
                     help="A menet kiindulo commitja (a valtoztatas ELOTTI kod)")
    ap.add_argument("--uj-commit", default="HEAD",
                     help="A vizsgalt commit (a valtoztatas UTANI kod, alapertelmezetten HEAD)")
    args = ap.parse_args()

    regi_sha = sh(["git", "rev-parse", args.regi_commit], cwd=ROOT).stdout.strip()
    uj_sha = sh(["git", "rev-parse", args.uj_commit], cwd=ROOT).stdout.strip()

    print("Parancs: python naplok/KARB_egyenertekuseg.py --regi-commit %s --uj-commit %s"
          % (args.regi_commit, args.uj_commit))
    print("regi_commit feloldva: %s" % regi_sha)
    print("uj_commit feloldva:   %s" % uj_sha)
    print("worktree-k: %s / %s\n" % (KB_REGI, KB_UJ))

    worktree_keszit(KB_REGI, regi_sha)
    worktree_keszit(KB_UJ, uj_sha)

    sorok = []
    try:
        for szkript in SZKRIPTEK:
            worktree_visszaallit(KB_REGI)
            worktree_visszaallit(KB_UJ)

            # -- 1. Mellekhatas-mentesseg (csak UJ-n) --
            rc_help, out_help, _ = futtat(KB_UJ, szkript, ["--help"])
            git_tiszta_help, _ = git_status_ures(KB_UJ)
            help_tiszta = (rc_help == 0 and out_help.strip() != "" and git_tiszta_help)
            worktree_visszaallit(KB_UJ)
            import_ok = import_tiszta(KB_UJ, szkript)
            worktree_visszaallit(KB_UJ)

            # -- 2. Argumentum nelkuli (bare) lefutas mindket masolatban --
            rc_regi, out_regi, err_regi = futtat(KB_REGI, szkript, [])
            rc_uj, out_uj, err_uj = futtat(KB_UJ, szkript, [])

            out_regi_m = maszkol(out_regi, KB_REGI)
            out_uj_m = maszkol(out_uj, KB_UJ)
            err_regi_m = maszkol(err_regi, KB_REGI)
            err_uj_m = maszkol(err_uj, KB_UJ)
            stdout_egyezik = (rc_regi == rc_uj) and (out_regi_m == out_uj_m) and (err_regi_m == err_uj_m)

            regi_leiras = "exit=%d, stdout %d sor, stderr %d sor" % (
                rc_regi, out_regi.count("\n"), err_regi.count("\n"))
            uj_leiras = "exit=%d, stdout %d sor, stderr %d sor" % (
                rc_uj, out_uj.count("\n"), err_uj.count("\n"))

            # -- 3. Fajl-sha egyezes, EBBEN a bare futasban, ESZKRIPTENKENT.
            #    A tobbi 9 SZKRIPT forraskodja is kulonbozik regi/uj kozott
            #    (ok is a KB1 resze) -- ez onmagaban NEM mellekhatas, ezert
            #    MIND a 10 szkriptet kizarjuk a forras-osszehasonlitasbol;
            #    csak azt merjuk, hogy EBBEN a lefutasban (az ADAT- es egyeb
            #    fajlokon) a regi es az uj kod ugyanazt a mellekhatast
            #    produkalja-e. --
            kizart = SAJAT_FAJLOK | {
                "eszkozok/" + s for s in SZKRIPTEK + KB2_EGYEB_SZKRIPTEK
            }
            sha_regi = sha256_fa(KB_REGI, kizart)
            sha_uj = sha256_fa(KB_UJ, kizart)
            kulcsok = set(sha_regi) | set(sha_uj)
            elteres = sorted(k for k in kulcsok if sha_regi.get(k) != sha_uj.get(k))
            fajl_sha_egyezik = not elteres

            sorok.append({
                "szkript": szkript,
                "regi_kod": regi_leiras,
                "uj_kod": uj_leiras,
                "fajl_sha_egyezik": fajl_sha_egyezik,
                "elteres_fajlok": ";".join(elteres) if elteres else "",
                "stdout_egyezik": stdout_egyezik,
                "help_tiszta": help_tiszta,
                "import_tiszta": import_ok,
            })
            print("%s: fajl-sha egyezik=%s%s | bare stdout egyezik=%s | --help tiszta=%s | import tiszta=%s"
                  % (szkript, fajl_sha_egyezik,
                     (" (elteres: %s)" % ", ".join(elteres)) if elteres else "",
                     stdout_egyezik, help_tiszta, import_ok))
            if not stdout_egyezik:
                print("  REGI stdout:\n%s" % out_regi_m)
                print("  UJ stdout:\n%s" % out_uj_m)
                print("  REGI stderr:\n%s" % err_regi_m)
                print("  UJ stderr:\n%s" % err_uj_m)
    finally:
        worktree_torol(KB_REGI)
        worktree_torol(KB_UJ)

    ki = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KARB_KB1_egyenertekuseg.tsv")
    fejlec = ["szkript", "regi_kod", "uj_kod", "fajl_sha_egyezik", "elteres_fajlok",
              "stdout_egyezik", "help_tiszta", "import_tiszta"]
    with open(ki, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Parancs: python naplok/KARB_egyenertekuseg.py --regi-commit %s --uj-commit %s\n"
                % (regi_sha, uj_sha))
        f.write("\t".join(fejlec) + "\n")
        for sor in sorok:
            f.write("\t".join(str(sor[k]) for k in fejlec) + "\n")
    print("\nEredmenytabla: %s" % ki)

    return 0 if all(s["fajl_sha_egyezik"] and s["stdout_egyezik"] and s["help_tiszta"] and s["import_tiszta"]
                     for s in sorok) else 1


if __name__ == "__main__":
    sys.exit(main())
