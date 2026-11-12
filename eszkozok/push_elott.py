#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_elott.py -- F216: helyi kapu push előtt. Pontosan azt futtatja, amit a
`.github/workflows/ellenorzes.yml` bukó lépései, így a HIBA a push előtt derül ki, nem a CI-ben
(egy piros CI-kör kb. 4 perc és egy session-kör).

A szabály (egy hely): `.claude/commands/kovetkezo.md`, „PUSH ELŐTT” szakasz. A `/kiadas` 6. lépése és a `/lap-javit`
csak hivatkozik rá.

Használat (a repó gyökeréből, az ág commitjai után, push előtt):
    python eszkozok/push_elott.py                      # az alap: a `git merge-base origin/main HEAD`
    python eszkozok/push_elott.py --alap origin/main   # más alap
    python eszkozok/push_elott.py --pr-cim "[ELLENŐRZŐ] ..."   # az E16-hoz (alapból a nyitott PR címe, ha a `gh` látja)
    python eszkozok/push_elott.py --lepes E18          # csak a nevében a szöveget tartalmazó lépések (javítás utáni gyors újrafutás;
                                                       # a push előtti kapu a teljes futás)
    python eszkozok/push_elott.py --ci-egyezes         # csak annak ellenőrzése, hogy a lépéslista egyezik a workflow-val
Kilépési kód: 0 = 0 HIBA (push mehet), 1 = van HIBA, 2 = futási hiba.

A lépéslista (LEPESEK) az egyetlen forrás a helyi futáshoz; a `--ci-egyezes` (a CI-ben is fut) megbukik, ha a
`.github/workflows/ellenorzes.yml` bukó lépései eltérnek tőle: egy Python-hívás hiányzik valamelyik oldalról, vagy egy
állandó argumentumú hívás szövege (pl. `--szigoru`) más. A CI-ben csak jelentés-lépések (tanulmány-audit, PR-komment)
maradhatnak a lépéslistán kívül (EGYEZES_KIVETEL).
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, '.github', 'workflows', 'ellenorzes.yml')
PY = sys.executable

# A CI-ben a futtat.py jelentésében a szabályonkénti minta (alap: 3) a HIBA-sorok megjelenítéséhez kevés lehet.
MINTA = '50'

# Állandó argumentumú hívások: a szövegük szó szerint szerepel a workflow-ban (a --ci-egyezes ezt ellenőrzi).
# A `None`-t tartalmazó (futási adattól függő) hívások csak szkript-szinten egyeznek.
STATIKUS_TESZTEK = [
    'eszkozok/ellenorzes/tesztek/test_szabalyok.py',
    'eszkozok/ellenorzes/tesztek/test_tanulmany.py',
    'eszkozok/teszt_ellenoriz_31.py',
    'eszkozok/teszt_ellenoriz_32.py',
    'eszkozok/teszt_ellenoriz_33.py',
    'eszkozok/teszt_ellenoriz_35.py',
    'eszkozok/teszt_gyokerok_kapuk.py',
    'eszkozok/teszt_hatastortenet.py',
    'eszkozok/teszt_proza_allitas.py',
    'eszkozok/teszt_push_elott.py',
]
STATIKUS_HIVASOK = [
    'eszkozok/ellenorzes/kovetelmeny_kapu.py HAMART-001 --szigoru',
    'eszkozok/ellenorzes/allitas_adat.py --minden --szigoru',
    'eszkozok/visszhang/tanu_kinyer.py ellenoriz',
    'eszkozok/szakirodalom_kinyer.py ellenoriz',
    'eszkozok/teszt_feladatok.py',
] + STATIKUS_TESZTEK
# Futási adattól függő hívások (a workflow-ban változókkal): a szkript-útvonal egyezik.
DINAMIKUS_SZKRIPTEK = [
    'eszkozok/ellenorzes/futtat.py',
    'eszkozok/ellenorzes/study_fajlok_szurese.py',
    'eszkozok/ellenoriz.py',
    'eszkozok/feladatok.py',
]
# Csak a CI-ben futó, nem bukó jelentés-lépések.
EGYEZES_KIVETEL = [
    'eszkozok/ellenorzes/tanulmany_audit.py',
    'eszkozok/ellenorzes/pr_komment.py',
]
# A workflow-ban kötelező, a CI-egyezést őrző lépés.
EGYEZES_PARANCS = 'eszkozok/push_elott.py --ci-egyezes'


def git(*args):
    r = subprocess.run(['git'] + list(args), cwd=ROOT, capture_output=True, encoding='utf-8')
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def python_hivasok(szoveg):
    """A workflow szövegéből a `python <eszkozok/...py> <argok>` hívások (megjegyzéssorok nélkül), soronként
    összevonva (a sorvégi `\\` folytatást egy sorrá)."""
    sorok = [s for s in szoveg.splitlines() if not s.lstrip().startswith('#')]
    egy = re.sub(r'\\\s*\n\s*', ' ', '\n'.join(sorok))
    return re.findall(r'python\s+(eszkozok/[\w./-]+\.py)([^\n]*)', egy)


def ci_egyezes(szoveg=None):
    """A lépéslista és a workflow egyezése (szoveg: a workflow szövege; alap: a fájl). Visszaadja a hibák listáját."""
    if szoveg is None:
        try:
            with open(WORKFLOW, encoding='utf-8') as f:
                szoveg = f.read()
        except OSError as exc:
            return ['a workflow nem olvasható: %s' % exc]
    hivasok = python_hivasok(szoveg)
    ci_szkriptek = {h[0] for h in hivasok}
    egy_szoveg = re.sub(r'\s+', ' ', szoveg)
    hibak = []
    var = set(DINAMIKUS_SZKRIPTEK) | {s.split()[0] for s in STATIKUS_HIVASOK} | set(EGYEZES_KIVETEL)
    var.add('eszkozok/push_elott.py')
    for sz in sorted(ci_szkriptek - var):
        hibak.append('a workflow-ban van, a push_elott.py lépéslistáján nincs: %s' % sz)
    for sz in sorted((set(DINAMIKUS_SZKRIPTEK) | {s.split()[0] for s in STATIKUS_HIVASOK}) - ci_szkriptek):
        hibak.append('a push_elott.py lépéslistáján van, a workflow-ban nincs: %s' % sz)
    for h in STATIKUS_HIVASOK:
        if 'python ' + h not in egy_szoveg:
            hibak.append('a workflow-ban a hívás szövege eltér: python %s' % h)
    if EGYEZES_PARANCS not in egy_szoveg:
        hibak.append('a workflow-ban nincs egyezés-lépés: python %s' % EGYEZES_PARANCS)
    return hibak


TMP_KONYVTAR = None   # a lépések ideiglenes könyvtára (a main() állítja be)


def ideiglenes_konyvtar():
    """Ideiglenes könyvtár a repóval azonos meghajtón. Windowson a szabály-tesztek (test_szabalyok.py) a repó gyökeréhez
    képest relatív útvonalat képeznek az ideiglenes fájlokból, és ez más meghajtón ValueError-ral bukik (pl. a worktree
    E:-n, a %TEMP% C:-n). Ilyenkor a meghajtó gyökerében készül a könyvtár."""
    alap = None
    if os.name == 'nt':
        if os.path.splitdrive(tempfile.gettempdir())[0].lower() != os.path.splitdrive(ROOT)[0].lower():
            alap = os.path.splitdrive(ROOT)[0] + os.sep + 'push_elott_tmp'
            os.makedirs(alap, exist_ok=True)
    return tempfile.mkdtemp(prefix='push_elott_', dir=alap)


class Futas:
    def __init__(self, szuro=None):
        self.szuro = szuro
        self.hibas = []   # (lépés, kilépési kód)
        self.hiba_sorok = []

    def lepes(self, nev, argv, stdin_szoveg=None, fajlba=None):
        """Egy lépés: stdout+stderr összegyűjtve. Kiírja az állapotot; HIBA esetén a HIBA-sorokat, vagy a kimenet végét."""
        if self.szuro and self.szuro not in nev:
            return 0, ''
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        if TMP_KONYVTAR:
            env.update(TEMP=TMP_KONYVTAR, TMP=TMP_KONYVTAR, TMPDIR=TMP_KONYVTAR)
        t0 = time.time()
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, encoding='utf-8', errors='replace',
                           input=stdin_szoveg, env=env)
        felirat = '%s [%d mp]' % (nev, time.time() - t0)
        kimenet = (r.stdout or '') + (('\n' + r.stderr) if r.stderr else '')
        if fajlba:
            with open(fajlba, 'w', encoding='utf-8') as f:
                f.write(r.stdout or '')
        if r.returncode == 0:
            print('RENDBEN  %s' % felirat)
        else:
            print('HIBA     %s (kilépési kód: %d)' % (felirat, r.returncode))
            self.hibas.append((nev, r.returncode))
            sorok = kimenet.splitlines()
            hiba = [s for s in sorok if 'HIBA' in s or 'SÉRTÉS' in s or 'FAIL' in s or 'Error' in s or 'Traceback' in s]
            minta = hiba if hiba else sorok[-25:]
            for s in minta[:80]:
                print('   ' + s)
            if len(minta) > 80:
                print('   ... és további %d sor' % (len(minta) - 80))
            self.hiba_sorok.extend(hiba)
        return r.returncode, kimenet


def main():
    ap = argparse.ArgumentParser(description='F216: a CI bukó lépései helyben, push előtt.')
    ap.add_argument('--alap', default=None, help='a diff alapja (alap: git merge-base origin/main HEAD)')
    ap.add_argument('--pr-cim', default=None, help='a PR címe (E16); alap: a nyitott PR címe, ha a gh elérhető')
    ap.add_argument('--lepes', default=None, help='csak a nevében ezt a szöveget tartalmazó lépések futnak (a teljes futás a kapu)')
    ap.add_argument('--ci-egyezes', action='store_true', help='csak a lépéslista és a workflow egyezését ellenőrzi')
    args = ap.parse_args()

    if args.ci_egyezes:
        hibak = ci_egyezes()
        for h in hibak:
            print('HIBA: ' + h)
        if hibak:
            return 1
        print('RENDBEN: a push_elott.py lépéslistája és a workflow egyezik.')
        return 0

    rc, fej, _ = git('rev-parse', 'HEAD')
    if rc != 0:
        print('HIBA: nem git-munkakönyvtár.', file=sys.stderr)
        return 2
    git('fetch', '-q', 'origin', 'main')
    alap_ref = args.alap or 'origin/main'
    rc, alap, hiba = git('merge-base', alap_ref, 'HEAD')
    if rc != 0:
        print('HIBA: a merge-base nem állapítható meg (%s): %s' % (alap_ref, hiba), file=sys.stderr)
        return 2
    rc, nem_commitolt, _ = git('status', '--porcelain')
    if nem_commitolt:
        print('FIGYELEM: nem commitolt változás van; a CI csak a commitokat látja (alap..HEAD), a kapu is azokat.')
    rc, valtozott, _ = git('diff', '--name-only', alap, fej)
    fajlok = [s for s in valtozott.splitlines() if s]
    rc, uzenetek, _ = git('log', '--format=%B', '%s..%s' % (alap, fej))
    pr_cim = args.pr_cim
    if pr_cim is None:
        pr_cim = ''
        try:
            r = subprocess.run(['gh', 'pr', 'view', '--json', 'title', '-q', '.title'], cwd=ROOT,
                               capture_output=True, encoding='utf-8', timeout=30)
            if r.returncode == 0:
                pr_cim = r.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    print('push_elott: alap %s, fej %s, %d változott fájl, PR-cím: %s' % (alap[:8], fej[:8], len(fajlok), pr_cim or '(nincs)'))

    fut = Futas(args.lepes)
    global TMP_KONYVTAR
    tmp = TMP_KONYVTAR = ideiglenes_konyvtar()

    # 0. a lépéslista egyezik a workflow-val
    for h in ci_egyezes():
        print('HIBA     CI-egyezés: %s' % h)
        fut.hibas.append(('CI-egyezés', 1))
        fut.hiba_sorok.append(h)

    # 1. E2-E39
    uzenet_fajl = os.path.join(tmp, 'commit_uzenetek.txt')
    with open(uzenet_fajl, 'w', encoding='utf-8') as f:
        f.write(uzenetek + '\n')
    if fajlok:
        fut.lepes('E2-E39 (futtat.py)', [
            PY, 'eszkozok/ellenorzes/futtat.py', '--valtozott'] + fajlok + [
            '--diff-alap', alap, '--diff-fej', fej, '--pr-cim', pr_cim, '--esemeny', 'pull_request',
            '--commit-uzenet-fajl', uzenet_fajl, '--minta', MINTA])
    else:
        print('RENDBEN  E2-E39 (nincs változott fájl)')
    if args.lepes:
        print('FIGYELEM: részleges futás (--lepes %s); a push előtti kapu a teljes futás.' % args.lepes)

    # 2. E1
    rc, study = fut.lepes('E1 szűrés (study_fajlok_szurese.py)',
                          [PY, 'eszkozok/ellenorzes/study_fajlok_szurese.py'], stdin_szoveg='\n'.join(fajlok) + '\n')
    study_args = []
    if rc == 0:
        for s in study.splitlines():
            if s.strip():
                study_args += ['--study', s.strip()]
    fut.lepes('E1 (ellenoriz.py)', [PY, 'eszkozok/ellenoriz.py'] + study_args + ['--md', os.path.join(tmp, 'e1_jelentes.md')])

    # 3. E38-E39 gyökérok-kapuk
    fut.lepes('E39 követelménylista-kapu', [PY, 'eszkozok/ellenorzes/kovetelmeny_kapu.py', 'HAMART-001', '--szigoru'])
    fut.lepes('E38 állítás-adat kapu', [PY, 'eszkozok/ellenorzes/allitas_adat.py', '--minden', '--szigoru'])

    # 4. szabály-tesztek
    for t in STATIKUS_TESZTEK[:2]:
        fut.lepes('teszt: ' + t, [PY, t])
    fut.lepes('teszt: eszkozok/visszhang/tanu_kinyer.py ellenoriz', [PY, 'eszkozok/visszhang/tanu_kinyer.py', 'ellenoriz'])
    fut.lepes('teszt: eszkozok/szakirodalom_kinyer.py ellenoriz', [PY, 'eszkozok/szakirodalom_kinyer.py', 'ellenoriz'])
    for t in STATIKUS_TESZTEK[2:]:
        fut.lepes('teszt: ' + t, [PY, t])

    # 5. feladatkövetés (E18) és tesztjei
    fut.lepes('E18 feladatok.py ellenoriz', [PY, 'eszkozok/feladatok.py', 'ellenoriz', '--pr-alap', alap])
    fut.lepes('feladatok.py tesztek', [PY, 'eszkozok/teszt_feladatok.py'])

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    if fut.hibas:
        print('HIBA: %d bukott lépés: %s' % (len(fut.hibas), '; '.join(n for n, _ in fut.hibas)))
        print('A push ne menjen, amíg nincs 0 HIBA.')
        return 1
    if args.lepes:
        print('0 HIBA a futtatott lépésekben (részleges futás: ez nem a push előtti kapu).')
        return 0
    print('0 HIBA: a push mehet.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
