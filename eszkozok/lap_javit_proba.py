#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lap_javit_proba.py -- F123.LAPJAVIT (DT-F123f): a `/lap-javit <ID>` próza-javításának előnézete, éles írás nélkül.

A javasolt cseréket (forrásfájl, régi szöveg, új szöveg) **memóriában** alkalmazza a lap kézi forrására (a
`res_forras.tsv` szerinti tanulmány vagy `motivumok/[ID].md`), a lapot kétszer generálja egy repón kívüli
ideiglenes könyvtárba (`alap/`: csere nélkül, `uj/`: cserével), és a kettőt veti össze: lapdiff és az olvasói kapu
(`olvasoi_kapu.py`) BUKÁS/FIGYELMEZTETÉS-száma mindkét változaton. A repóban semmit nem ír: a forrás tényleges
javítása a parancsban, a felhasználó jóváhagyása után történik (Edit), és utána a lap `general.py --ir`-rel
generálódik.

A csere-fájl TSV (`split('\\t')`), fejléc: `forras	regi	uj`; a `forras` repó-relatív út (pl.
`motivumok/HODIT-001.md`, `tematikus_lezart/Rafaim_tematikus.md`). A `regi` pontosan egyszer forduljon elő a
forrásfájlban és a lapra kerülő nézetében is; különben a szkript megáll (kilépési kód 2), mert a javítás helye
nem egyértelmű. A héber/görög/magyar szöveg ezért fájlból jön, nem parancssorból (CLAUDE.md, Shell).

    python eszkozok/lap_javit_proba.py --id HODIT-001 --csere <tmp>/csere.tsv --kimenet <tmp>/proba

Kilépési kód: 0 = az új változaton az olvasói kapu nem ad több BUKÁS-t, mint az alapon; 1 = több BUKÁS;
2 = hiba (nem egyértelmű csere, repón belüli kimenet).
"""

import argparse
import difflib
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402
import olvasoi_kapu as OK  # noqa: E402


def csere_beolvas(ut):
    """[(forras, regi, uj)] a csere-fájlból; a `#`-sor és az üres sor kimarad."""
    with io.open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    fejlec = sorok[0].split('\t')
    if fejlec != ['forras', 'regi', 'uj']:
        raise ValueError('a csere-fájl fejléce: forras, regi, uj (kapott: %r)' % fejlec)
    ki = []
    for s in sorok[1:]:
        mezok = s.split('\t')
        if len(mezok) != 3 or not mezok[0].strip() or not mezok[1]:
            raise ValueError('hibás csere-sor: %r' % s)
        ki.append((mezok[0].strip(), mezok[1], mezok[2]))
    return ki


def generalt_lap(kimenet, motivum_id):
    """A lap generálása a `kimenet/lexikon/` alá (a `general.py --cel lexikon --id ... --kimenet ...` útja,
    ugyanabban a folyamatban, hogy a memóriában cserélt forrás érvényesüljön)."""
    regi_argv = sys.argv
    try:
        sys.argv = ['general.py', '--cel', 'lexikon', '--id', motivum_id, '--kimenet', kimenet]
        G.main()
    finally:
        sys.argv = regi_argv
    with io.open(os.path.join(kimenet, 'lexikon', '%s_TUDOMANYOS.md' % motivum_id), encoding='utf-8') as f:
        return f.read()


def kapu(kimenet, motivum_id):
    """(BUKÁS, FIGYELMEZTETÉS) az olvasói kapuból a `kimenet/lexikon/` lapján."""
    OK.LEXIKON_KONYVTAR = os.path.abspath(os.path.join(kimenet, 'lexikon'))
    tal, megj = OK.motivum_meres(motivum_id)
    if tal is None:
        return None, megj
    _, b, fi = OK.osszesit(tal)
    return (b, fi), tal


def csere_alkalmaz(cserek):
    """A cserék a `lexikon_general` forrás-gyorsítótárában. Hibalista: ahol a `regi` nem pontosan egyszer áll a
    forrásfájlban vagy a lapra kerülő nézetében."""
    hibak = []
    for forras, regi, uj in cserek:
        with io.open(os.path.join(G.ROOT, forras), encoding='utf-8', newline='') as f:
            nyers = f.read().replace('\r\n', '\n')
        if nyers.count(regi) != 1:
            hibak.append('%s: a régi szöveg %d-szer áll a forrásfájlban (pontosan 1 kell)' % (forras, nyers.count(regi)))
            continue
        nezet = LG._tanulmany_szoveg(forras)
        if nezet.count(regi) != 1:
            hibak.append('%s: a régi szöveg %d-szer áll a lapra kerülő nézetben (belső szinten van, vagy '
                         'ismétlődik)' % (forras, nezet.count(regi)))
            continue
        LG._tanulmany_szoveg_cache[forras] = nezet.replace(regi, uj)
    return hibak


def main():
    ap = argparse.ArgumentParser(description='A /lap-javit próza-javításának előnézete, éles írás nélkül')
    ap.add_argument('--id', required=True)
    ap.add_argument('--csere', required=True, help='TSV: forras, regi, uj')
    ap.add_argument('--kimenet', required=True, help='repón KÍVÜLI ideiglenes könyvtár')
    ap.add_argument('--jelentes', help='a jelentés Markdown-fájlba (alapból <kimenet>/jelentes.md)')
    a = ap.parse_args()
    if not G.helyi_kimenet_engedett(a.kimenet):
        print('HIBA: a --kimenet csak a repón kívül lehet (CLAUDE.md: a --kimenet próbák ideiglenes könyvtárba)',
              file=sys.stderr)
        return 2
    cserek = csere_beolvas(a.csere)

    alap_dir, uj_dir = os.path.join(a.kimenet, 'alap'), os.path.join(a.kimenet, 'uj')
    alap = generalt_lap(alap_dir, a.id)
    hibak = csere_alkalmaz(cserek)
    if hibak:
        for h in hibak:
            print('HIBA: ' + h, file=sys.stderr)
        return 2
    uj = generalt_lap(uj_dir, a.id)

    k_alap, _ = kapu(alap_dir, a.id)
    k_uj, tal_uj = kapu(uj_dir, a.id)
    diff = [s for s in difflib.unified_diff(alap.split('\n'), uj.split('\n'), 'alap', 'uj', lineterm='', n=0)]

    ki = ['# /lap-javit próba — %s' % a.id, '',
          '*scope=%s | forras=eszkozok/lap_javit_proba.py (memóriában cserélt forrás, éles írás nélkül) | '
          'ts=futáskor*' % a.id, '',
          '## Cserék', '']
    for forras, regi, uj_sz in cserek:
        ki += ['- `%s`' % forras, '  - régi: %s' % regi, '  - új: %s' % uj_sz]
    ki += ['', '## Olvasói kapu', '', '| Változat | BUKÁS | FIGYELMEZTETÉS |', '|---|---|---|',
           '| alap | %s | %s |' % (k_alap or ('—', '—')), '| új | %s | %s |' % (k_uj or ('—', '—')), '',
           '## Lapdiff (alap → új)', '', '```diff'] + diff + ['```', '']
    jelentes = a.jelentes or os.path.join(a.kimenet, 'jelentes.md')
    with io.open(jelentes, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki))
    valtozott = sum(1 for s in diff if s[:1] in '+-' and not s.startswith(('+++', '---')))
    print('lap_javit_proba: %s — %d csere, %d megváltozott lapsor; olvasói kapu alap %s → új %s; jelentés: %s'
          % (a.id, len(cserek), valtozott, k_alap, k_uj, jelentes))
    if k_alap and k_uj and k_uj[0] > k_alap[0]:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
