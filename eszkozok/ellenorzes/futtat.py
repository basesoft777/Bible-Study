#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
futtat.py -- CI.0/CI.2: az E2-E19 ellenorzesek kozos futtatoja
(F02_CI_ELLENORZES_BRIEF.md). Az E1-et (SEMA 1-12, Q1, Q7) NEM ez futtatja --
azt a meglevo `eszkozok/ellenoriz.py --study FILE` adja, kulon hivassal
(l. .github/workflows/ellenorzes.yml).

CLI:
    python eszkozok/ellenorzes/futtat.py --teljes
    python eszkozok/ellenorzes/futtat.py --valtozott fajl1.md fajl2.md
    python eszkozok/ellenorzes/futtat.py --valtozott fajl.md --diff-alap origin/main --diff-fej HEAD --pr-cim "..."

Kimenet: markdown jelentes stdout-ra, szabalyonkent talalatszam + minta.
Kilepesi kod: 0 = nincs HIBA-szintu talalat, 1 = van, 2 = futasi hiba.

--teljes modban MINDEN talalat csak JELENTES (a HIBA-besorolas a diff-
hatokorre vonatkozik, D3 -- l. brief "Diff-hatokor" szakasz), tehat a
kilepesi kod --teljes modban mindig 0.

D8 (--valtozott + --diff-alap/--diff-fej modban): a HIBA csak a diff altal
HOZZAADOTT/MODOSITOTT sorokra vonatkozik -- egy szabaly regi (a PR altal
nem erintett) talalata csak JELENTES. Kivetel a SZ.FAJLSZINTU_SZABALYOK
(E4, E5, E6, E7, E16, E19, E25, E26): ezeknel a talalat nem egy konkret uj sorhoz kotheto,
tehat mindig a sajat szintjukon jelentkeznek. Ha --diff-alap/--diff-fej
hianyzik --valtozott modban is, a regi (D8 elotti) viselkedes ervenyesul:
a talalat fajlszinten a sajat szintjen jelentkezik -- ezt CI.2 mindig
diff-refekkel hivja, csak a helyi, kezi futtatashoz marad tartalek.
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kozos import md_fajlok, kizart_e, git_diff_hozzaadott_sorok, ROOT
import szabalyok as SZ


def _szint_diff_szerint(talalat, alap_szint, hozzaadott_cache, diff_alap, diff_fej):
    """D8: a talalat vegleges szintje -- HIBA csak akkor marad, ha a
    talalat sora a diff altal hozzaadott/modositott sorok kozott van."""
    if talalat.sor is None or talalat.sor == 0:
        return alap_szint
    if not diff_alap or not diff_fej:
        return alap_szint
    if talalat.fajl not in hozzaadott_cache:
        hozzaadott_cache[talalat.fajl] = git_diff_hozzaadott_sorok(diff_alap, diff_fej, talalat.fajl)
    hozzaadott = hozzaadott_cache[talalat.fajl]
    if hozzaadott is None:
        # Nem allapithato meg a diff (pl. a fajl nincs a base-ben es a
        # head-ben sem elerheto) -- konzervativan a sajat szinten marad.
        return alap_szint
    if talalat.sor in hozzaadott:
        return alap_szint
    return 'JELENTES'


def fut(valtozott_fajlok, teljes, diff_alap=None, diff_fej=None, pr_cim='', commit_uzenet='', esemeny=''):
    """Visszaad: {szabaly: [Talalat, ...]} -- a Talalat.szint mar a vegleges
    (D8-cal leminositett) szint."""
    valtozott_fajlok = [f for f in valtozott_fajlok if not kizart_e(f)]  # D14
    hatokor = ['__TELJES__'] if teljes else list(valtozott_fajlok)
    fajlok_a_szabalyoknak = md_fajlok() if teljes else valtozott_fajlok

    nyers = {}
    for nev, fv in SZ.SZABALYOK_FUGGVENYEI.items():
        if nev in SZ.HATOKOR_SZABALYOK:
            # E3, E19: adattablan futnak; --teljes modban a '__TELJES__'
            # jelzo kell nekik, nem az md-fajlok listaja (ELLENOR_F28 2. tetel).
            nyers[nev] = fv(hatokor if teljes else valtozott_fajlok)
        else:
            nyers[nev] = fv(fajlok_a_szabalyoknak)

    nyers['E5'] = SZ.e5_tartalomvesztes_or(diff_alap, diff_fej, commit_uzenet)
    # E26 (F30): veglegesszam az agon; push-esemenynel (main) nem ertelmezett
    nyers['E26'] = SZ.e26_vegleges_szam_agon(diff_alap, diff_fej, commit_uzenet, esemeny)
    # E16: push-esemenynel nincs PR-cim, ezert nem ertelmezett (a PR-en fut)
    if esemeny == 'push':
        nyers['E16'] = []
    else:
        nyers['E16'] = SZ.e16_ellenorzo_onmodositas(valtozott_fajlok if not teljes else [], pr_cim)

    hozzaadott_cache = {}
    eredmeny = {}
    for nev, talalatok in nyers.items():
        if teljes:
            for t in talalatok:
                t.szint = 'JELENTES'
        elif nev not in SZ.FAJLSZINTU_SZABALYOK:
            alap_szint = SZ.SZINT[nev]
            for t in talalatok:
                t.szint = _szint_diff_szerint(t, alap_szint, hozzaadott_cache, diff_alap, diff_fej)
        eredmeny[nev] = talalatok

    return eredmeny


E16_PUSH_MEGJEGYZES = 'E16: push-esemény, nem értelmezett (a PR-en fut)'


def jelentes_szoveg(eredmeny, teljes, minta_db=3, esemeny=''):
    sorok = []
    sorok.append('# Ellenorzes jelentes (%s)' % ('teljes repo' if teljes else 'valtozott fajlok'))
    sorok.append('')
    hiba_van = False
    for nev in sorted(eredmeny.keys(), key=lambda n: int(n[1:])):
        talalatok = eredmeny[nev]
        hiba_szamu = sum(1 for t in talalatok if t.szint == 'HIBA')
        jelentes_szamu = len(talalatok) - hiba_szamu
        cim_reszek = []
        if hiba_szamu:
            cim_reszek.append('HIBA: %d' % hiba_szamu)
        if jelentes_szamu:
            cim_reszek.append('JELENTES: %d' % jelentes_szamu)
        if not cim_reszek:
            cim_reszek.append('0 talalat')
        sorok.append('## %s (%s)' % (nev, ', '.join(cim_reszek)))
        if nev == 'E16' and esemeny == 'push':
            sorok.append('- %s' % E16_PUSH_MEGJEGYZES)
        for t in talalatok[:minta_db]:
            sorok.append('- `%s` `%s:%s` -- %s' % (t.szint, t.fajl, t.sor, t.reszlet))
        if len(talalatok) > minta_db:
            sorok.append('- ... es tovabbi %d' % (len(talalatok) - minta_db))
        sorok.append('')
        if hiba_szamu:
            hiba_van = True
    return '\n'.join(sorok), hiba_van


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--valtozott', nargs='*', default=[])
    ap.add_argument('--teljes', action='store_true')
    ap.add_argument('--diff-alap', default=None)
    ap.add_argument('--diff-fej', default=None)
    ap.add_argument('--pr-cim', default='')
    ap.add_argument('--esemeny', default='',
                    help='a GitHub-esemeny neve (pl. push, pull_request); push-esemenynel az E16 nem ertelmezett')
    ap.add_argument('--commit-uzenet', default='')
    ap.add_argument(
        '--commit-uzenet-fajl', default=None,
        help=(
            'Fajl, amelynek tartalma a PR osszes commit-uzenete '
            '(base..head, osszefuzve). Ekezetes/idezojeles szoveg miatt '
            'biztonsagosabb, mint a --commit-uzenet shell-argumentum '
            '(l. CLAUDE.md "Shell" szakasz). Ha meg van adva, felulirja '
            'a --commit-uzenetet.'
        ),
    )
    ap.add_argument('--minta', type=int, default=3)
    args = ap.parse_args()

    if not args.teljes and not args.valtozott:
        print('Hiba: --teljes vagy --valtozott FAJL... kotelezo.', file=sys.stderr)
        return 2

    valtozott_relativ = []
    for f in args.valtozott:
        rel = os.path.relpath(os.path.abspath(f), ROOT).replace(os.sep, '/')
        valtozott_relativ.append(rel)

    commit_uzenet = args.commit_uzenet
    if args.commit_uzenet_fajl:
        with open(args.commit_uzenet_fajl, encoding='utf-8') as f:
            commit_uzenet = f.read()

    eredmeny = fut(
        valtozott_relativ, args.teljes,
        diff_alap=args.diff_alap, diff_fej=args.diff_fej,
        pr_cim=args.pr_cim, commit_uzenet=commit_uzenet, esemeny=args.esemeny,
    )
    szoveg, hiba_van = jelentes_szoveg(eredmeny, args.teljes, args.minta, args.esemeny)
    print(szoveg)
    return 1 if hiba_van else 0


if __name__ == '__main__':
    sys.exit(main())
