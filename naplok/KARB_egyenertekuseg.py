import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

"""
KARB_egyenertekuseg.py -- KARBANTARTAS_BRIEF.md SS1 (Egyenertekuseg,
Mellekhatas-mentesseg) mérőszkriptje a KB1 10 szkriptjéhez.

Két elore elkeszitett ideiglenes git worktree-t hasznal (a munkapeldanyon
KIVUL, G4):
  KB_REGI -- a menet kiindulo commitja (b980c57), a valtoztatas ELOTTI kod
  KB_UJ   -- a jelen HEAD (a KB1+KB2 utan), a valtoztatas UTANI kod

Harom mérést vegez szkriptenkent:
  1. Mellekhatas-mentesseg (csak KB_UJ-n): --help tiszta kilepessel es
     ures git status-szal fut-e, es a modul importja nem ir semmit
     es nem general stdout-ot.
  2. Argumentum nelkuli lefutas (mindket masolatban): kilepesi kod es
     stdout osszevetese -- a masolat sajat abszolut utvonala
     (ROOT-fuggo print-sorok) maszkolva, mert ez pusztan a ket
     ideiglenes konyvtar nevenek kulonbsege, nem viselkedesbeli elteres.
  3. Fajl-sha egyezes: a bare futas UTAN, a ket masolat MINDEN fajljanak
     sha256-a egyezik-e, KIVEVE magukat az eszkozok/*.py szkripteket
     (ezek szandekosan kulonboznek -- ez a KB1/KB2 targya), a .git
     konyvtarat es a csak KB_UJ-ban letezo naplok/KARB_* jelentesfajlokat.

A harom meres eredmenye a naplok/KARB_KB1_egyenertekuseg.tsv-be kerul.
"""

import hashlib
import importlib.util
import os
import subprocess

KB_REGI = r"C:\Users\bases\AppData\Local\Temp\claude\C--Users-bases-Desktop-Bible-Study\39458d04-b436-4717-bca0-ee963aa712df\scratchpad\kb_regi"
KB_UJ = r"C:\Users\bases\AppData\Local\Temp\claude\C--Users-bases-Desktop-Bible-Study\39458d04-b436-4717-bca0-ee963aa712df\scratchpad\kb_uj"

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
    proc = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                           capture_output=True, text=True, encoding="utf-8")
    return proc.stdout.strip() == "", proc.stdout


def import_tiszta(root, relpath):
    """A modult importlib-bel importalja egy KULON python-folyamatban
    (hogy a mostani folyamat sys.modules-a ne szennyezodjon), es visszaadja,
    hogy volt-e stdout/stderr, valamint hogy a git status tiszta maradt-e."""
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
    return proc.returncode == 0 and stdout_ures and tiszta_git, proc.stdout, proc.stderr, proc.returncode


def sha256_fa(root, kizart_relpathok):
    """{relpath: sha256} minden fajlra a .git kivetelevel es a kizart lista nelkul."""
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
                continue
            with open(full, "rb") as f:
                ki[rel] = hashlib.sha256(f.read()).hexdigest()
    return ki


def maszkol(szoveg, root):
    return szoveg.replace(root, "<ROOT>").replace(root.replace("\\", "/"), "<ROOT>")


def main():
    sorok = []

    # -- A. fazis: mellekhatas-mentesseg MINDEN szkriptre, MIELOTT barmelyik
    #    bare-futasa (ami irna a kozos adat/*.tsv fajlokat) elszennyezne a
    #    git status-t a KOVETKEZO szkript merese elott. --
    mellekhatas = {}
    for szkript in SZKRIPTEK:
        rc_help, out_help, err_help = futtat(KB_UJ, szkript, ["--help"])
        git_tiszta_help, _ = git_status_ures(KB_UJ)
        help_tiszta = (rc_help == 0 and out_help.strip() != "" and git_tiszta_help)

        import_ok, import_out, import_err, import_rc = import_tiszta(KB_UJ, szkript)
        mellekhatas[szkript] = (help_tiszta, import_ok)

    # -- B. fazis: argumentum nelkuli lefutas mindket masolatban, sorban --
    for szkript in SZKRIPTEK:
        help_tiszta, import_ok = mellekhatas[szkript]

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

        sorok.append({
            "szkript": szkript,
            "regi_kod": regi_leiras,
            "uj_kod": uj_leiras,
            "stdout_egyezik": stdout_egyezik,
            "help_tiszta": help_tiszta,
            "import_tiszta": import_ok,
        })
        print("%s: bare stdout egyezik=%s | --help tiszta=%s | import tiszta=%s"
              % (szkript, stdout_egyezik, help_tiszta, import_ok))
        if not stdout_egyezik:
            print("  REGI stdout:\n%s" % out_regi_m)
            print("  UJ stdout:\n%s" % out_uj_m)
            print("  REGI stderr:\n%s" % err_regi_m)
            print("  UJ stderr:\n%s" % err_uj_m)

    # 3. Fajl-sha egyezes -- a MINDEN szkript lefutasa UTANI vegallapotban
    kizart = set("eszkozok/" + s for s in SZKRIPTEK)
    kizart.update({
        "eszkozok/elofordulas_szamlalo.py",
        "eszkozok/frazis_kereses_pozicio_alapon.py",
        "eszkozok/tahot_zarojeles_phaseA_kivonat.py",
        "naplok/KARB_KB0_kiindulas.md",
        "naplok/KARB_egyenertekuseg.py",
        "naplok/KARB_KB1_egyenertekuseg.tsv",
        "naplok/KARB_crlf_teszt.py",
        "naplok/KARB_KB2_crlf.tsv",
        "naplok/KARB_KB3_nullaz.py",
        "naplok/KARB_KB3_nullazas.tsv",
        "naplok/KARB_jelentes.md",
        "KARBANTARTAS_BRIEF.md",
        "FELADATOK.md",
    })
    sha_regi = sha256_fa(KB_REGI, kizart)
    sha_uj = sha256_fa(KB_UJ, kizart)
    kulcsok = set(sha_regi) | set(sha_uj)
    elteres = sorted(k for k in kulcsok if sha_regi.get(k) != sha_uj.get(k))

    print("\nFajl-sha egyezes (a script.py fajlokon es a menet sajat naplo/brief"
          " fajljain kivul): %s" % ("MIND EGYEZIK" if not elteres else "%d ELTERES" % len(elteres)))
    for k in elteres:
        print("  ELTERES: %s | regi=%s | uj=%s" % (k, sha_regi.get(k), sha_uj.get(k)))

    fajl_sha_egyezik = not elteres
    for sor in sorok:
        sor["fajl_sha_egyezik"] = fajl_sha_egyezik

    ki = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KARB_KB1_egyenertekuseg.tsv")
    fejlec = ["szkript", "regi_kod", "uj_kod", "fajl_sha_egyezik", "stdout_egyezik",
              "help_tiszta", "import_tiszta"]
    with open(ki, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(fejlec) + "\n")
        for sor in sorok:
            f.write("\t".join(str(sor[k]) for k in fejlec) + "\n")
    print("\nEredmenytabla: %s" % ki)


if __name__ == "__main__":
    main()
