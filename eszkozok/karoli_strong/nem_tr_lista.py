#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — a párosított `[nem TR]` eredeti tokenek adatszintű jelölése (D45, a felhasználó döntése: (a) változat).

A `prompt_v3` K szabálya szerint a TR-ben nem szereplő eredeti szó (`TAGNT_kivonat.tsv` `Kritikai kiadás` mezőjében nincs
`TR`, `TR»N`, `TR«N`) `forditatlan`. Ahol a TR más alakot olvas, a TR-es alaknak nincs sora a kivonatban; a modell ilyenkor
a Károli szavát a `[nem TR]` sorhoz köti. A link marad (`alacsony`, `S`), de a `strong` a kritikai szöveg alakjáé, nem
feltétlenül a TR-é. Ez a szkript a meglévő `adat/karoli_strong/szavak_<könyv>.tsv` táblákból (csak az ÚSZ-könyvek) listázza
ezeket a tokeneket a partner Károli-szavakkal, API nélkül, determinisztikusan; a `szavak`/`parok` táblákat nem írja.

Kimenet: `adat/karoli_strong/nem_tr_parositott.tsv` (séma: `adat/SEMA.md` 2.20).

Használat:
    python eszkozok/karoli_strong/nem_tr_lista.py              # a tábla írása
    python eszkozok/karoli_strong/nem_tr_lista.py --ellenoriz  # a meglévő tábla egyezik-e az újraépítéssel (írás nélkül)
"""
import argparse
import glob
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import tokenek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KIMENET = os.path.join(tokenek.ROOT, 'adat', 'karoli_strong', 'nem_tr_parositott.tsv')
FEJLEC = ['vers', 'er_sorszam', 'er_szo', 'strong', 'kritikai_kiadas', 'allapot', 'hu_sorszam', 'hu_szo']


def usz_konyvek():
    return {r[0].rsplit(' ', 1)[0] for r in tokenek._sorok(tokenek.TAGNT)}


def kiadasok():
    """igehely -> [Kritikai kiadás mező] a TAGNT-sorrendben (a tokenek sorszáma szerint)."""
    d = {}
    for r in tokenek._sorok(tokenek.TAGNT):
        d.setdefault(r[0], []).append(r[7] if len(r) > 7 else '')
    return d


def tabla_sorok(szavak, kiad):
    """szavak: a szavak_<könyv>.tsv adatsorai (mezőlisták). Visszaad: a kimenet sorai (mezőlisták)."""
    hu = {(r[0], r[2]): r[3] for r in szavak if r[1] == 'hu'}
    ki = []
    for r in szavak:
        if r[1] != 'er' or r[4] != 'parositva':   # csak a link: a forditatlan a K szabály szerinti, a fuggoben/kezi nem link
            continue
        w = bemenet.vers_adat(r[0])['eredeti'][int(r[2]) - 1]
        if not w['nem_tr']:
            continue
        partner = [p for p in r[5].replace('+', ',').split(',') if p]
        ki.append([r[0], r[2], r[3], r[6], kiad.get(r[0], [''] * int(r[2]))[int(r[2]) - 1], r[4],
                   ','.join(partner), ' '.join(hu.get((r[0], p), '') for p in partner)])
    return ki


def epit():
    usz = usz_konyvek()
    kiad = kiadasok()
    sorok, konyvek = [], []
    for ut in sorted(glob.glob(os.path.join(tokenek.ROOT, 'adat', 'karoli_strong', 'szavak_*.tsv'))):
        with open(ut, encoding='utf-8') as f:
            sz = [s.rstrip('\n').rstrip('\r').split('\t') for s in f if s.strip() and not s.startswith('#')][1:]
        if not sz or sz[0][0].rsplit(' ', 1)[0] not in usz:
            continue
        konyvek.append(os.path.basename(ut))
        sorok += tabla_sorok(sz, kiad)
    sorok.sort(key=lambda r: (tokenek.igehely_bont(r[0]) or ('', 0, 0), int(r[1])))
    return sorok, konyvek


def szoveg(sorok, konyvek, ts):
    fej = ('# GENERÁLT: eszkozok/karoli_strong/nem_tr_lista.py | scope=az ÚSZ-könyvek szavak-táblái (%s) | '
           'forras=adat/karoli_strong/szavak_<könyv>.tsv + konkordancia/TAGNT_kivonat.tsv | ts=%s | a párosított [nem TR] '
           'eredeti tokenek (a TR más alakot olvas, annak nincs sora a kivonatban); a link `alacsony`, a strong a kritikai szöveg '
           'alakjáé; D45 (a) | kézzel szerkeszteni tilos' % (', '.join(k[len('szavak_'):-4] for k in konyvek), ts))
    return '\n'.join([fej, '\t'.join(FEJLEC)] + ['\t'.join(r) for r in sorok]) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args(argv)
    sorok, konyvek = epit()
    if a.ellenoriz:
        if not os.path.exists(KIMENET):
            print('hiányzik: %s' % KIMENET, file=sys.stderr)
            return 1
        with open(KIMENET, encoding='utf-8') as f:
            meglevo = [s.rstrip('\n') for s in f if not s.startswith('#')]
        uj = szoveg(sorok, konyvek, '').split('\n')[1:-1]
        if meglevo != uj:
            print('eltér: a tábla nem egyezik az újraépítéssel', file=sys.stderr)
            return 1
        print('ellenőrzés: rendben (%d sor, %d könyv)' % (len(sorok), len(konyvek)))
        return 0
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg(sorok, konyvek, time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime())))
    print('írva: %s (%d sor, %d ÚSZ-könyv)' % (os.path.relpath(KIMENET, tokenek.ROOT), len(sorok), len(konyvek)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
