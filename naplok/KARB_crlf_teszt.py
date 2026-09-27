#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KARB_crlf_teszt.py -- KARBANTARTAS_BRIEF.md SS1 (CRLF-tures) merőszkriptje
a KB2 4 erintett soraahoz.

v2: a fuggetlen ellenorzes (naplok/ELLENOR_KARB.md) ket problemat talalt a
v1-ben: (1) szintetikus stringeken hasonlitotta ossze a KIMASOLT rstrip-
mintakat, nem a valodi szkripteket futtatta; (2) EMPIRIKUSAN kiderult
(l. lent), hogy ez a 4 szkript egyike sem `newline=''`-lel nyitja meg a
bemenetet -- sima `open(path, encoding='utf-8')`-fal, `for line in f:`
ciklussal olvas. Python ALAPERTELMEZETT szoveges modja (`newline=None`)
UNIVERZALIS SORVEG-KEZELEST vegez: a `\\r\\n`, `\\r` es `\\n` sorvegek MIND
`\\n`-re alakulnak at MAR AZ ITERACIO SORAN, mielott a `line` valtozohoz
kerulnenek -- tehat a `line.rstrip("\\n")` es a `line.rstrip("\\r\\n")`
VALODI FAJLBOL olvasva BAJTRA AZONOS eredmenyt ad ennel a 4 hivasi pontnal.

Ez azt jelenti: a KB2 csereje (rstrip("\\n") -> rstrip("\\r\\n")) ezeknel a
konkret hivasi pontoknal VEDEKEZO HIGIENIA, NEM funkcionalis javitas -- a
felteteleztt hiba a valodi hasznalati modban (sima `open()`, sorononkenti
iteracio) sosem manifesztalodik. Ezt a mineesitest at kell vezetni a
naplok/KARB_KB0_kiindulas.md 0.4 soraba es a KARB_jelentes.md KB2
szakaszaba is (l. onnan hivatkozva).

A szkript HAROM reszben bizonyitja ezt:

  A) VALODI szkript, VALODI bemenet: a regi es az uj kod (ket kulon
     worktree-bol, `--regi-commit`/`--uj-commit`) ugyanazt a, a repoban
     tenylegesen letezo adatfajlbol vett, valodi sort kapja LF- es
     CRLF-vegzodessel, es a tenyleges fuggvenyt hivja (importalva, NEM
     ujraimplementalva). Varakozas: regi==uj MINDKET sorvegen (a csere
     nem valtoztat semmin ezen az uton).
  B) newline=''-es KONTROLLPAR: UGYANAZ a ket sor (LF/CRLF), de a fajlt
     `open(path, newline='')`-vel nyitva (megkerulve az univerzalis
     sorveg-kezelest) -- itt a REGI rstrip("\\n") mintanak HIBAZNIA kell
     CRLF-en (a `\\r` bennmarad az utolso mezoben), az UJ-nak nem. Ez
     bizonyitja, hogy maga a rstrip-csere HELYES es RONBUSZTUSABB, csak
     nem ezen a hivasi uton eri el a tenyleges kockazatot.
  C) Repo-szintu grep: mely tenyleges olvasasi utak nyitnak fajlt
     `newline=''`-vel (ahol a \\r valoban athaladhat, ha a hivo kod nem
     kezeli kulon) -- csak lelohely-lista, NEM ellenorzott, hogy ezek
     ténylegesen hibaznak-e, es NEM javitott.

A negyedik szkriptnel (tahot_zarojeles_phaseA_kivonat.py) a nyers TAHOT
input-fajlok (eszkozok/tahot/*.txt) NINCSENEK a repoban (kulso, nem
verziozott adat) -- az A/B resz ezert egy REPREZENTATIV, a modul sajat
docstringje szerinti 12-mezos sorral dolgozik, NEM valodi repo-adattal;
ez explicit jelolve van az eredmenyben (proveniencia: manual/fixture).

Hasznalat:
    python naplok/KARB_crlf_teszt.py --regi-commit 68eb348 --uj-commit HEAD
"""

import argparse
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WT_ROOT = os.path.join(ROOT, '.claude', 'kb_worktrees')
KB2_REGI = os.path.join(WT_ROOT, 'kb2_regi')
KB2_UJ = os.path.join(WT_ROOT, 'kb2_uj')


def sh(args, cwd=None, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError("parancs hiba: %r\nstdout:\n%s\nstderr:\n%s" % (
            args, r.stdout, r.stderr))
    return r


def worktree_keszit(path, commit):
    if os.path.isdir(path):
        sh(["git", "worktree", "remove", "--force", path], cwd=ROOT, check=False)
    os.makedirs(WT_ROOT, exist_ok=True)
    sh(["git", "worktree", "add", "--detach", path, commit], cwd=ROOT)


def worktree_torol(path):
    sh(["git", "worktree", "remove", "--force", path], cwd=ROOT, check=False)


def python_futtat(worktree, kod, cwd_fajlok_ide=None):
    """Egy python -c parancsot futtat a MEGADOTT worktree eszkozok/ konyvtaraval
    a sys.path elejen, hogy a valodi (regi vagy uj) modult importalja."""
    teljes_kod = (
        "import sys\n"
        "sys.path.insert(0, %r)\n" % os.path.join(worktree, "eszkozok")
        + kod
    )
    r = subprocess.run([sys.executable, "-c", teljes_kod],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("python hiba (%s):\n%s" % (worktree, r.stderr))
    return r.stdout.strip()


def ir_ideiglenes(tartalom, sorveg, konyvtar):
    """Egy ideiglenes fajlt ir bytes-szinten a kert sorveggel (LF vagy CRLF),
    hogy a fajl VALODI CRLF-et tartalmazzon a lemezen (nem csak a python-
    string-irodalomban)."""
    path = os.path.join(konyvtar, "fixture.tsv")
    adat = tartalom.replace("\n", sorveg).encode("utf-8")
    with open(path, "wb") as f:
        f.write(adat)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--regi-commit", required=True)
    ap.add_argument("--uj-commit", default="HEAD")
    args = ap.parse_args()

    regi_sha = sh(["git", "rev-parse", args.regi_commit], cwd=ROOT).stdout.strip()
    uj_sha = sh(["git", "rev-parse", args.uj_commit], cwd=ROOT).stdout.strip()
    print("Parancs: python naplok/KARB_crlf_teszt.py --regi-commit %s --uj-commit %s"
          % (args.regi_commit, args.uj_commit))
    print("regi=%s uj=%s\n" % (regi_sha, uj_sha))

    worktree_keszit(KB2_REGI, regi_sha)
    worktree_keszit(KB2_UJ, uj_sha)

    sorok = []
    sikerult = True
    try:
        munka_regi = os.path.join(WT_ROOT, "fixture_regi")
        munka_uj = os.path.join(WT_ROOT, "fixture_uj")
        os.makedirs(munka_regi, exist_ok=True)
        os.makedirs(munka_uj, exist_ok=True)

        # --------------------------------------------------------------
        # A) elofordulas_szamlalo.py -- VALODI sor a konkordancia/TAGNT_
        #    kivonat.tsv-bol (a repo tenyleges adata).
        # --------------------------------------------------------------
        with open(os.path.join(ROOT, "konkordancia", "TAGNT_kivonat.tsv"), encoding="utf-8") as f:
            fejlec_a = f.readline().rstrip("\n")
            sor_a = f.readline().rstrip("\n")
        strong_a = sor_a.split("\t")[1]
        tartalom_a = fejlec_a + "\n" + sor_a + "\n"

        for sorveg_nev, sorveg in (("LF", "\n"), ("CRLF", "\r\n")):
            p_regi = ir_ideiglenes(tartalom_a, sorveg, munka_regi)
            p_uj = ir_ideiglenes(tartalom_a, sorveg, munka_uj)
            kod = (
                "import elofordulas_szamlalo as M\n"
                "print(M.count_occurrences(%r, %r))\n"
            )
            ki_regi = python_futtat(KB2_REGI, kod % (p_regi, strong_a))
            ki_uj = python_futtat(KB2_UJ, kod % (p_uj, strong_a))
            egyezik = (ki_regi == ki_uj)
            sikerult = sikerult and egyezik
            sorok.append((
                "elofordulas_szamlalo.py", "A: valodi TAGNT-sor, %s" % sorveg_nev,
                "regi=%s | uj=%s | %s" % (ki_regi, ki_uj, "EGYEZIK" if egyezik else "ELTER"),
                "valodi (konkordancia/TAGNT_kivonat.tsv 1. adatsora)",
            ))

        # --------------------------------------------------------------
        # B) elofordulas_szamlalo.py -- newline=''-es kontrollpar: a
        #    REGI mintanak (rstrip("\n")) hibaznia kell CRLF-en, ha a
        #    fajlt newline=''-vel nyitjuk (megkerulve az univerzalis
        #    sorveg-kezelest).
        # --------------------------------------------------------------
        p_regi_crlf = ir_ideiglenes(tartalom_a, "\r\n", munka_regi)
        kod_kontroll = (
            "with open(%r, encoding='utf-8', newline='') as f:\n"
            "    f.readline()\n"
            "    sor = f.readline()\n"
            "regi = sor.rstrip('\\n').split('\\t')\n"
            "uj = sor.rstrip('\\r\\n').split('\\t')\n"
            "print('regi utolso mezo=%%r' %% regi[-1])\n"
            "print('uj utolso mezo=%%r' %% uj[-1])\n"
        ) % p_regi_crlf
        ki_kontroll = python_futtat(KB2_UJ, kod_kontroll)
        regi_hibas = "\\r" in ki_kontroll.splitlines()[0]
        uj_hibas = "\\r" in ki_kontroll.splitlines()[1]
        kontroll_ok = regi_hibas and not uj_hibas
        sikerult = sikerult and kontroll_ok
        sorok.append((
            "elofordulas_szamlalo.py", "B: newline='' kontroll, CRLF",
            "%s | varva: regi HIBAS, uj OK | %s" % (
                ki_kontroll.replace("\n", " ; "), "RENDBEN" if kontroll_ok else "HIBA"),
            "szintetikus kontroll (ugyanaz a valodi sor, csak a fajlnyitas mod maskepp)",
        ))

        # --------------------------------------------------------------
        # A/B ismetelve a masik ket, VALODI adaton dolgozo szkriptre:
        # frazis_kereses_pozicio_alapon.py (TAHOT_kivonat.tsv) es
        # f3_4_zaro_ellenoriz.py (adat/elofordulasok.tsv).
        # --------------------------------------------------------------
        with open(os.path.join(ROOT, "konkordancia", "TAHOT_kivonat.tsv"), encoding="utf-8") as f:
            fejlec_b = f.readline().rstrip("\n")
            sorai_b = [f.readline().rstrip("\n") for _ in range(2)]
        tartalom_b = fejlec_b + "\n" + "\n".join(sorai_b) + "\n"
        ref_b = sorai_b[0].split("\t")[0]

        for sorveg_nev, sorveg in (("LF", "\n"), ("CRLF", "\r\n")):
            p_regi = ir_ideiglenes(tartalom_b, sorveg, munka_regi)
            p_uj = ir_ideiglenes(tartalom_b, sorveg, munka_uj)
            kod = (
                "import frazis_kereses_pozicio_alapon as M\n"
                "vs, vo = M.load_verse_strongs(%r)\n"
                "print(vs.get(%r))\n"
            )
            ki_regi = python_futtat(KB2_REGI, kod % (p_regi, ref_b))
            ki_uj = python_futtat(KB2_UJ, kod % (p_uj, ref_b))
            egyezik = (ki_regi == ki_uj)
            sikerult = sikerult and egyezik
            sorok.append((
                "frazis_kereses_pozicio_alapon.py", "A: valodi TAHOT-sorok, %s" % sorveg_nev,
                "regi=%s | uj=%s | %s" % (ki_regi, ki_uj, "EGYEZIK" if egyezik else "ELTER"),
                "valodi (konkordancia/TAHOT_kivonat.tsv elso 2 adatsora)",
            ))

        p_regi_crlf_b = ir_ideiglenes(tartalom_b, "\r\n", munka_regi)
        kod_kontroll_b = (
            "with open(%r, encoding='utf-8', newline='') as f:\n"
            "    f.readline()\n"
            "    sor = f.readline()\n"
            "regi = sor.rstrip('\\n').split('\\t')\n"
            "uj = sor.rstrip('\\r\\n').split('\\t')\n"
            "print('regi utolso mezo=%%r' %% regi[-1])\n"
            "print('uj utolso mezo=%%r' %% uj[-1])\n"
        ) % p_regi_crlf_b
        ki_kontroll_b = python_futtat(KB2_UJ, kod_kontroll_b)
        regi_hibas_b = "\\r" in ki_kontroll_b.splitlines()[0]
        uj_hibas_b = "\\r" in ki_kontroll_b.splitlines()[1]
        kontroll_ok_b = regi_hibas_b and not uj_hibas_b
        sikerult = sikerult and kontroll_ok_b
        sorok.append((
            "frazis_kereses_pozicio_alapon.py", "B: newline='' kontroll, CRLF",
            "%s | varva: regi HIBAS, uj OK | %s" % (
                ki_kontroll_b.replace("\n", " ; "), "RENDBEN" if kontroll_ok_b else "HIBA"),
            "szintetikus kontroll",
        ))

        # f3_4_zaro_ellenoriz.py -- valodi adat/elofordulasok.tsv sorok
        # (a # komment-fejlecet es a valodi oszlop-fejlecet is meghagyva,
        # ahogy az olvas() fuggveny elvarja).
        with open(os.path.join(ROOT, "adat", "elofordulasok.tsv"), encoding="utf-8") as f:
            komment_c = f.readline().rstrip("\n")
            fejlec_c = f.readline().rstrip("\n")
            sor_c = f.readline().rstrip("\n")
        tartalom_c = komment_c + "\n" + fejlec_c + "\n" + sor_c + "\n"

        for sorveg_nev, sorveg in (("LF", "\n"), ("CRLF", "\r\n")):
            p_regi = ir_ideiglenes(tartalom_c, sorveg, munka_regi)
            p_uj = ir_ideiglenes(tartalom_c, sorveg, munka_uj)
            kod = (
                "import f3_4_zaro_ellenoriz as M\n"
                "fej, sorok = M.olvas(%r)\n"
                "print('##EREDMENY##' + repr(sorok))\n"
            )
            # A REGI valtozat (b980c57-ben meg nincs __main__-or, KB1
            # targya) modulszinten ir stdout-ra IMPORTKOR -- ezert csak az
            # utolso, sajat jelolt sorunkat hasonlitjuk ossze, nem a teljes
            # kimenetet.
            def utolso_eredmeny(szoveg):
                for sor in reversed(szoveg.splitlines()):
                    if sor.startswith("##EREDMENY##"):
                        return sor[len("##EREDMENY##"):]
                return szoveg
            ki_regi_teljes = python_futtat(KB2_REGI, kod % p_regi)
            ki_uj_teljes = python_futtat(KB2_UJ, kod % p_uj)
            ki_regi = utolso_eredmeny(ki_regi_teljes)
            ki_uj = utolso_eredmeny(ki_uj_teljes)
            egyezik = (ki_regi == ki_uj)
            sikerult = sikerult and egyezik
            sorok.append((
                "f3_4_zaro_ellenoriz.py", "A: valodi elofordulasok.tsv-sor, %s" % sorveg_nev,
                "regi==uj: %s" % ("EGYEZIK" if egyezik else "ELTER (l. reszletek stdout-on)"),
                "valodi (adat/elofordulasok.tsv 1. adatsora)",
            ))
            if not egyezik:
                print("  f3_4_zaro_ellenoriz.py %s ELTERES:\n  regi=%s\n  uj=%s"
                      % (sorveg_nev, ki_regi, ki_uj))

        p_regi_crlf_c = ir_ideiglenes(tartalom_c, "\r\n", munka_regi)
        kod_kontroll_c = (
            "with open(%r, encoding='utf-8', newline='') as f:\n"
            "    sorok = [s.rstrip('\\n') for s in f]\n"
            "if sorok[0].startswith('#'): sorok = sorok[1:]\n"
            "fej = sorok[0].split('\\t')\n"
            "d = dict(zip(fej, sorok[1].split('\\t')))\n"
            "print('regi utolso mezo=%%r' %% list(d.values())[-1])\n"
            "sorok2 = [s.rstrip('\\r\\n') for s in open(%r, encoding='utf-8', newline='')]\n"
            "if sorok2[0].startswith('#'): sorok2 = sorok2[1:]\n"
            "fej2 = sorok2[0].split('\\t')\n"
            "d2 = dict(zip(fej2, sorok2[1].split('\\t')))\n"
            "print('uj utolso mezo=%%r' %% list(d2.values())[-1])\n"
        ) % (p_regi_crlf_c, p_regi_crlf_c)
        ki_kontroll_c = python_futtat(KB2_UJ, kod_kontroll_c)
        regi_hibas_c = "\\r" in ki_kontroll_c.splitlines()[0]
        uj_hibas_c = "\\r" in ki_kontroll_c.splitlines()[1]
        kontroll_ok_c = regi_hibas_c and not uj_hibas_c
        sikerult = sikerult and kontroll_ok_c
        sorok.append((
            "f3_4_zaro_ellenoriz.py", "B: newline='' kontroll, CRLF",
            "%s | varva: regi HIBAS, uj OK | %s" % (
                ki_kontroll_c.replace("\n", " ; "), "RENDBEN" if kontroll_ok_c else "HIBA"),
            "szintetikus kontroll",
        ))

        # --------------------------------------------------------------
        # tahot_zarojeles_phaseA_kivonat.py -- a nyers TAHOT-fajlok NINCSENEK
        # a repoban; reprezentativ (nem valodi) 12-mezos sor, a modul sajat
        # docstringje szerinti szerkezettel.
        # --------------------------------------------------------------
        raw_12mezo = "\t".join([
            "Gen.1.1#1=x", "heber", "translit", "translation", "dStrongs",
            "f5", "f6", "f7", "f8", "f9", "f10", "H0430=El=Isten",
        ])
        for sorveg_nev, sorveg in (("LF", "\n"), ("CRLF", "\r\n")):
            p_regi = ir_ideiglenes(raw_12mezo + "\n", sorveg, munka_regi)
            p_uj = ir_ideiglenes(raw_12mezo + "\n", sorveg, munka_uj)
            kod = (
                "import re\n"
                "REF_RE = re.compile(r'^([A-Za-z0-9]+)\\.(\\d+)\\.(\\d+)(\\((\\d+)\\.(\\d+)\\))?#(\\d+)=(.*)$')\n"
                "with open(%r, encoding='utf-8') as f:\n"
                "    for line in f:\n"
                "        line = line.rstrip('\\r\\n')\n"
                "        fields = line.split('\\t')\n"
                "        print(repr(fields[11]))\n"
            )
            ki_regi = python_futtat(KB2_REGI, kod % p_regi)
            ki_uj = python_futtat(KB2_UJ, kod % p_uj)
            egyezik = (ki_regi == ki_uj)
            sikerult = sikerult and egyezik
            sorok.append((
                "tahot_zarojeles_phaseA_kivonat.py", "A: reprezentativ 12-mezos sor, %s" % sorveg_nev,
                "regi=%s | uj=%s | %s" % (ki_regi, ki_uj, "EGYEZIK" if egyezik else "ELTER"),
                "MANUAL/FIXTURE -- a nyers TAHOT-fajlok (eszkozok/tahot/*.txt) nincsenek a repoban",
            ))

        p_regi_crlf_d = ir_ideiglenes(raw_12mezo + "\n", "\r\n", munka_regi)
        kod_kontroll_d = (
            "with open(%r, encoding='utf-8', newline='') as f:\n"
            "    sor = f.readline()\n"
            "regi = sor.rstrip('\\n').split('\\t')\n"
            "uj = sor.rstrip('\\r\\n').split('\\t')\n"
            "print('regi fields[11]=%%r' %% regi[11])\n"
            "print('uj fields[11]=%%r' %% uj[11])\n"
        ) % p_regi_crlf_d
        ki_kontroll_d = python_futtat(KB2_UJ, kod_kontroll_d)
        regi_hibas_d = "\\r" in ki_kontroll_d.splitlines()[0]
        uj_hibas_d = "\\r" in ki_kontroll_d.splitlines()[1]
        kontroll_ok_d = regi_hibas_d and not uj_hibas_d
        sikerult = sikerult and kontroll_ok_d
        sorok.append((
            "tahot_zarojeles_phaseA_kivonat.py", "B: newline='' kontroll, CRLF",
            "%s | varva: regi HIBAS, uj OK | %s" % (
                ki_kontroll_d.replace("\n", " ; "), "RENDBEN" if kontroll_ok_d else "HIBA"),
            "szintetikus kontroll (MANUAL/FIXTURE alapon)",
        ))

    finally:
        worktree_torol(KB2_REGI)
        worktree_torol(KB2_UJ)

    # --------------------------------------------------------------
    # C) repo-szintu grep: hol nyilik meg fajl newline=''-vel OLVASASRA
    #    (irasra nyitott newline='' NEM kockazat -- azt kizarjuk).
    # --------------------------------------------------------------
    grep = subprocess.run(
        ["git", "grep", "-n", "newline=''", "--", "eszkozok/"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    kockazatos = []
    for sor in grep.stdout.splitlines():
        if "sys.stdout" in sor or "sys.stderr" in sor:
            continue
        if "'w'" in sor or ", 'a'" in sor or "'wb'" in sor:
            continue
        kockazatos.append(sor)

    print("\n" + "\n".join("%s\t%s\t%s\t%s" % s for s in sorok))
    print("\nC) newline='' OLVASASRA nyitott lelohelyek (grep, NEM ellenorzott, NEM javitott): %d"
          % len(kockazatos))
    for sor in kockazatos:
        print("  %s" % sor)

    ki = os.path.join(ROOT, "naplok", "KARB_KB2_crlf.tsv")
    with open(ki, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Parancs: python naplok/KARB_crlf_teszt.py --regi-commit %s --uj-commit %s\n"
                % (regi_sha, uj_sha))
        f.write("# MINOSITES: a KB2 rstrip(\"\\n\")->rstrip(\"\\r\\n\") csereje ennel a 4 hivasi\n")
        f.write("# pontnal VEDEKEZO HIGIENIA, nem funkcionalis javitas -- l. a szkript fejleceben.\n")
        f.write("szkript\teset\teredmeny\tproveniencia\n")
        for szkript, eset, eredmeny, prov in sorok:
            f.write("%s\t%s\t%s\t%s\n" % (szkript, eset, eredmeny, prov))
        f.write("\n# C) newline='' OLVASASRA nyitott lelohelyek (grep, nem ellenorzott, nem javitott):\n")
        for sor in kockazatos:
            f.write("# %s\n" % sor)
    print("\nEredmenytabla: %s" % ki)

    return 0 if sikerult else 1


if __name__ == "__main__":
    sys.exit(main())
