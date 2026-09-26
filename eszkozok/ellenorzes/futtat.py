#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
futtat.py -- CI.0/CI.2: az E2-E16 ellenorzesek kozos futtatoja
(CI_ELLENORZES_BRIEF.md). Az E1-et (SEMA 1-12, Q1, Q7) NEM ez futtatja --
azt a meglevo `eszkozok/ellenoriz.py --study FILE` adja, kulon hivassal
(l. .github/workflows/ellenorzes.yml).

CLI:
    python eszkozok/ellenorzes/futtat.py --teljes
    python eszkozok/ellenorzes/futtat.py --valtozott fajl1.md fajl2.md
    python eszkozok/ellenorzes/futtat.py --valtozott fajl.md --diff-alap origin/main --diff-fej HEAD --pr-cim "..."

Kimenet: markdown jelentes stdout-ra, szabalyonkent talalatszam + minta.
Kilepesi kod: 0 = nincs HIBA-szintu talalat a valtozott fajlokon, 1 = van,
2 = futasi hiba.

--teljes modban MINDEN talalat csak JELENTES (a HIBA-besorolas a diff-
hatokorre vonatkozik, CLAUDE.md/D3 -- l. brief "Diff-hatokor" szakasz),
tehat a kilepesi kod --teljes modban mindig 0.
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kozos import md_fajlok, ROOT
import szabalyok as SZ


def fut(valtozott_fajlok, teljes, diff_alap=None, diff_fej=None, pr_cim='', commit_uzenet=''):
    """Visszaad: {szabaly: [Talalat, ...]}."""
    hatokor = ['__TELJES__'] if teljes else list(valtozott_fajlok)
    fajlok_a_szabalyoknak = md_fajlok() if teljes else valtozott_fajlok

    eredmeny = {}
    for nev, fv in SZ.SZABALYOK_FUGGVENYEI.items():
        if nev == 'E3':
            eredmeny[nev] = fv(hatokor if teljes else valtozott_fajlok)
        else:
            eredmeny[nev] = fv(fajlok_a_szabalyoknak)

    eredmeny['E5'] = SZ.e5_tartalomvesztes_or(diff_alap, diff_fej, commit_uzenet)
    eredmeny['E16'] = SZ.e16_ellenorzo_onmodositas(valtozott_fajlok if not teljes else [], pr_cim)

    return eredmeny


def jelentes_szoveg(eredmeny, teljes, minta_db=3):
    sorok = []
    sorok.append('# Ellenorzes jelentes (%s)' % ('teljes repo' if teljes else 'valtozott fajlok'))
    sorok.append('')
    hiba_van = False
    for nev in sorted(eredmeny.keys(), key=lambda n: int(n[1:])):
        talalatok = eredmeny[nev]
        szint = SZ.SZINT.get(nev, 'FIGYELMEZTETES')
        tenyleges_szint = 'JELENTES' if teljes else szint
        sorok.append('## %s (%s): %d talalat' % (nev, tenyleges_szint, len(talalatok)))
        for t in talalatok[:minta_db]:
            sorok.append('- `%s:%s` -- %s' % (t.fajl, t.sor, t.reszlet))
        if len(talalatok) > minta_db:
            sorok.append('- ... es tovabbi %d' % (len(talalatok) - minta_db))
        sorok.append('')
        if (not teljes) and szint == 'HIBA' and talalatok:
            hiba_van = True
    return '\n'.join(sorok), hiba_van


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--valtozott', nargs='*', default=[])
    ap.add_argument('--teljes', action='store_true')
    ap.add_argument('--diff-alap', default=None)
    ap.add_argument('--diff-fej', default=None)
    ap.add_argument('--pr-cim', default='')
    ap.add_argument('--commit-uzenet', default='')
    ap.add_argument('--minta', type=int, default=3)
    args = ap.parse_args()

    if not args.teljes and not args.valtozott:
        print('Hiba: --teljes vagy --valtozott FAJL... kotelezo.', file=sys.stderr)
        return 2

    valtozott_relativ = []
    for f in args.valtozott:
        rel = os.path.relpath(os.path.abspath(f), ROOT).replace(os.sep, '/')
        valtozott_relativ.append(rel)

    eredmeny = fut(
        valtozott_relativ, args.teljes,
        diff_alap=args.diff_alap, diff_fej=args.diff_fej,
        pr_cim=args.pr_cim, commit_uzenet=args.commit_uzenet,
    )
    szoveg, hiba_van = jelentes_szoveg(eredmeny, args.teljes, args.minta)
    print(szoveg)
    return 1 if hiba_van else 0


if __name__ == '__main__':
    sys.exit(main())
