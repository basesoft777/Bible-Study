#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
szakirodalom_kinyer.py -- a vitatott pontok lektorált szakirodalma: `adat/vitatott_forrasok.tsv` (SEMA 2.58; F183, K67f).

A felhasználó döntése (2026-11-11, „mehet”): a lap 10. Értelmezés „⚠️ Vitatott pontok” részében minden vitatott ponthoz
legfeljebb egy lektorált forrás (OpenAlex, Crossref, DOAB), egymondatos, saját szavas összefoglalóval; ha a ponthoz nincs
a kérdésről szóló forrás, a sor ezt mondja ki (hiány-sor, üres szerzővel). Két kéz: a kinyerő (`modell`) nem ellenőriz.

    beolvas  KINYERT.tsv --ellenor MODELL --atnezes ATN.tsv
             a kinyert sorok a táblába; az ellenőr soronkénti ítélete (motivum, pont, atnezo, itelet = jo | elvet,
             megjegyzes) az átnézés-bemenetben; átnézés nélkül vagy elvetve az `ellenorzes` üres (nem renderel).
    ellenoriz
             szerkezet: oszlopszám, zárt értékek, kulcs-egyediség (motivum + pont), proveniencia; a forrás-sornál DOI
             vagy URL kötelező.

TSV: split('\\t') / '\\t'.join(), a csv modul nem használható (CLAUDE.md).
"""
import argparse
import collections
import datetime
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(GYOKER, 'adat', 'vitatott_forrasok.tsv')
OSZLOPOK = ['motivum', 'pont', 'szerzo', 'cim', 'megjelenes', 'ev', 'doi', 'url', 'nyilt_eleres', 'osszefoglalo',
            'lekerdezes', 'lekerdezve', 'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
FEJ_MEGJ = ('# A vitatott pontok lektorált szakirodalma (F183, K67f). Kulcs: motivum + pont. Séma: adat/SEMA.md 2.58. '
            'Ellenőrizetlen sor (üres `ellenorzes`) a lapon nem renderel. Üres szerző: hiány-sor (a ponthoz nincs a '
            'kérdésről szóló lektorált forrás). Szöveg (idézet) nincs, csak saját szavas egy mondat.')


def tsv_olvas(ut):
    if not ut or not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if not s.startswith('#') and s.strip()]
    if not sorok:
        return []
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def tabla_ir(sorok):
    for r in sorok:
        for o in OSZLOPOK:
            if '\t' in r.get(o, '') or '\n' in r.get(o, ''):
                raise SystemExit('HIBA: tab vagy sortörés: %s / %s' % (o, r.get('pont')))
    with open(TABLA, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FEJ_MEGJ + '\n' + '\t'.join(OSZLOPOK) + '\n')
        for r in sorok:
            f.write('\t'.join(r.get(o, '') for o in OSZLOPOK) + '\n')
    print('vitatott_forrasok.tsv: %d sor' % len(sorok))


def beolvas(a):
    atn = tsv_olvas(a.atnezes)
    hibak = [r['pont'] for r in atn if r.get('itelet') not in ('jo', 'elvet') or not (r.get('megjegyzes') or '').strip()
             or not (r.get('atnezo') or '').strip()]
    if hibak:
        raise SystemExit('HIBA: az átnézés-bemenet nem érdemi: %s' % hibak)
    atnezes = {(r['motivum'], r['pont']): r for r in atn}
    meglevo = {(r['motivum'], r['pont']): r for r in tsv_olvas(TABLA)}
    datum = datetime.date.today().isoformat()
    for r in tsv_olvas(a.kinyert):
        r = {o: (r.get(o) or '').strip() for o in OSZLOPOK}
        at = atnezes.get((r['motivum'], r['pont']))
        ok = None
        if r['modell'] == a.ellenor:
            ok = 'a kinyerő és az ellenőr ugyanaz'
        elif not at or at['itelet'] != 'jo':
            ok = 'nincs átnézés' if not at else 'elvetve: %s' % at['megjegyzes']
        elif at['atnezo'] != a.ellenor:
            ok = 'az átnéző nem az ellenőr'
        r['ellenorzes'] = '' if ok else '%s, %s: kézi átnézés (%s)' % (a.ellenor, datum, at['megjegyzes'])
        if ok:
            print('  ELLENŐRIZETLEN: %s (%s)' % (r['pont'], ok))
        meglevo[(r['motivum'], r['pont'])] = r
    tabla_ir(sorted(meglevo.values(), key=lambda r: (r['motivum'], r['pont'])))


def ellenoriz(_a):
    sorok = tsv_olvas(TABLA)
    hibak, kulcs = [], collections.Counter()
    for r in sorok:
        if len(r) != len(OSZLOPOK):
            hibak.append('oszlopszám: %s' % r.get('pont'))
            continue
        kulcs[(r['motivum'], r['pont'])] += 1
        if r['kinyeres'] not in ('modell', 'kezi'):
            hibak.append('zárt érték (kinyeres): %s' % r['pont'])
        if not r['proveniencia'].startswith('scope='):
            hibak.append('proveniencia: %s' % r['pont'])
        if not r['osszefoglalo']:
            hibak.append('üres összefoglaló: %s' % r['pont'])
        if r['szerzo'] and not (r['doi'] or r['url']):
            hibak.append('forrás-sor DOI vagy URL nélkül: %s' % r['pont'])
    hibak += ['a kulcs többször áll: %s' % ' | '.join(k) for k, n in kulcs.items() if n > 1]
    for h in hibak:
        print('HIBA:', h)
    print('vitatott_forrasok.tsv: %d sor, %d hiba' % (len(sorok), len(hibak)))
    return 1 if hibak else 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    al = p.add_subparsers(dest='parancs', required=True)
    b = al.add_parser('beolvas')
    b.add_argument('kinyert')
    b.add_argument('--ellenor', required=True)
    b.add_argument('--atnezes', required=True)
    al.add_parser('ellenoriz')
    a = p.parse_args()
    return {'beolvas': beolvas, 'ellenoriz': ellenoriz}[a.parancs](a) or 0


if __name__ == '__main__':
    sys.exit(main())
