#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tanulmany_audit.py -- F37 T3 "Jelentes mod": a tanulmany-szabalyok (E20 es az
E8/E9/E12/E13 tanulmanyra bovitett hatokore, plusz a minden .md-n futo E2/E15)
MINDEN tanulmanyfajlon, nem bukik. A kotelezo (piros) mod a futtat.py-ban
van: ott csak az uj vagy modositott tanulmanyfajl talalata HIBA (D8).

CLI:
    python eszkozok/ellenorzes/tanulmany_audit.py                      # stdout
    python eszkozok/ellenorzes/tanulmany_audit.py --kimenet naplok/TANULMANY_AUDIT.md

Kilepesi kod: mindig 0 (jelentes mod), kiveve a futasi hibat (2).
"""

import argparse
import collections
import datetime
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K
import szabalyok as SZ

# A tanulmanyfajlra vonatkozo szabalyok (F37 T0 3. pont): E20 uj; E21->E13,
# E22->E8, E23->E9, E24->E12 bovites; E2 es E15 minden .md-n fut.
TANULMANY_SZABALYOK = ('E20', 'E13', 'E8', 'E9', 'E12', 'E2', 'E15')
LEIRAS = {
    'E20': 'kötelező szakasz (a Tanulmány sablonból)',
    'E13': 'kiejtés a héber/görög szó mellett (volt E21)',
    'E8': 'versformátum (volt E22)',
    'E9': 'angol „sense” (volt E23)',
    'E12': 'naplójellegű szöveg 【NAPLO】 blokkon kívül (volt E24)',
    'E2': '„ellenőrizve” jelölés proveniencia nélkül',
    'E15': 'SzPA-idézet hossza',
}


def tanulmanyfajlok():
    """A verziozott (git ls-files) tanulmanyfajlok; git nelkul (pl. a teszt
    ideiglenes gyokereben) a kozos.md_fajlok(). A rejtett konyvtarak (pl. a
    helyi `.claude/worktrees/`) kimaradnak."""
    try:
        kimenet = subprocess.check_output(['git', 'ls-files', '*.md'], cwd=K.ROOT,
                                          stderr=subprocess.DEVNULL).decode('utf-8')
        fajlok = [s.strip() for s in kimenet.splitlines() if s.strip()]
    except (subprocess.CalledProcessError, OSError):
        fajlok = []
    if not fajlok:
        fajlok = K.md_fajlok()
    return sorted(f for f in fajlok if not f.startswith('.') and K.tanulmany_fajl_e(f)
                  and os.path.exists(os.path.join(K.ROOT, *f.split('/'))))


def _szint_modositasnal(t):
    """A talalat szintje, ha a fajlt egy PR modositana (a sor is valtozna)."""
    return t.szint


def _commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=K.ROOT,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except (subprocess.CalledProcessError, OSError):
        return '?'


def _cella(s):
    return s.replace('|', '\\|').replace('`', "'")


def audit(fajlok=None):
    fajlok = tanulmanyfajlok() if fajlok is None else fajlok
    eredmeny = {}
    for nev in TANULMANY_SZABALYOK:
        eredmeny[nev] = SZ.SZABALYOK_FUGGVENYEI[nev](fajlok)
    return fajlok, eredmeny


def jelentes(fajlok, eredmeny):
    s = []
    s.append('# GENERÁLT: eszkozok/ellenorzes/tanulmany_audit.py — kézzel nem szerkesztendő.')
    s.append('')
    s.append('# Tanulmány-audit (CI jelentés mód)')
    s.append('')
    s.append('*F37 T3 · jelentés mód: minden tanulmányfájl, nem bukik · commit `%s` · %s · '
             'proveniencia: `scope=%d tanulmányfájl | forras=eszkozok/ellenorzes/tanulmany_audit.py | ts=%s`*'
             % (_commit(), datetime.date.today().isoformat(), len(fajlok),
                datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))
    s.append('')
    s.append('A „szint módosításnál” oszlop azt mutatja, mi lenne a találat szintje, ha egy PR '
             'az adott sort módosítaná (a kötelező mód csak az új vagy módosított sort bünteti, D8; '
             'az E20 fájlszintű: a módosított tanulmányon mindig piros). Javítást ez a jelentés nem végez '
             '(DT-F37-5).')
    s.append('')
    s.append('## Összesítő szabályonként')
    s.append('')
    s.append('| Szabály | Mit néz | Találat | Fájl | Szint módosításnál |')
    s.append('|---|---|---|---|---|')
    for nev in TANULMANY_SZABALYOK:
        t = eredmeny[nev]
        szintek = sorted({_szint_modositasnal(x) for x in t}) or ['—']
        s.append('| %s | %s | %d | %d | %s |' % (nev, LEIRAS[nev], len(t), len({x.fajl for x in t}),
                                                ', '.join(szintek)))
    s.append('')
    s.append('## Fájlonként')
    s.append('')
    s.append('| Tanulmány | ' + ' | '.join(TANULMANY_SZABALYOK) + ' |')
    s.append('|---|' + '---|' * len(TANULMANY_SZABALYOK))
    szamlalo = collections.defaultdict(collections.Counter)
    for nev, t in eredmeny.items():
        for x in t:
            szamlalo[x.fajl][nev] += 1
    for f in fajlok:
        s.append('| `%s` | %s |' % (f, ' | '.join(str(szamlalo[f][n] or '·') for n in TANULMANY_SZABALYOK)))
    s.append('')
    s.append('## Találatok')
    for f in fajlok:
        sorok = []
        for nev in TANULMANY_SZABALYOK:
            for x in sorted(eredmeny[nev], key=lambda y: y.sor or 0):
                if x.fajl == f:
                    sorok.append('| %s | %s | %s | %s |' % (nev, x.sor or '—', _szint_modositasnal(x),
                                                            _cella(x.reszlet[:180])))
        if not sorok:
            continue
        s.append('')
        s.append('### `%s`' % f)
        s.append('')
        s.append('| Szabály | Sor | Szint módosításnál | Részlet |')
        s.append('|---|---|---|---|')
        s.extend(sorok)
    s.append('')
    return '\n'.join(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kimenet', default=None, help='a jelentes fajlja (repo-relativ); kulonben stdout')
    args = ap.parse_args()
    fajlok, eredmeny = audit()
    szoveg = jelentes(fajlok, eredmeny)
    if args.kimenet:
        ut = os.path.join(K.ROOT, *args.kimenet.replace('\\', '/').split('/'))
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s (%d tanulmany, %d talalat)' % (
            args.kimenet, len(fajlok), sum(len(t) for t in eredmeny.values())))
    else:
        print(szoveg)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # jelentes mod: a futasi hiba sem buktatja a PR-t, de jelzi
        print('tanulmany_audit.py futasi hiba: %r' % (e,), file=sys.stderr)
        sys.exit(2)
