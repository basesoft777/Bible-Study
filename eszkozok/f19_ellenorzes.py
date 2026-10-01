#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f19_ellenorzes.py -- F19.3: onallo lekerdezes a konkordancia/KJV_Strongs_teljes.tsv-en (az ASV_Strongs_teljes.tsv F19.7 ota
nincs a repoban, forrashibas: DT19 (b); ha a fajl megvan, pl. a regi commitbol, ugyanazt merik rajta) (nem az importer
parszolojat hasznalja): kulcs-Strong darabszamok, kulcsversek, egyezes a meglevo studybible-tablakkal
(Genesis, Exodus, Proverbs) konyvenkent es vershalmazonkent, token-szintu egyezes a luvlylavnder-rel.

Hasznalat: python eszkozok/f19_ellenorzes.py [--luv <mappa a luvlylavnder klonnal>]
TSV-olvasas split('\t'), csv modul nelkul.
"""

import argparse
import collections
import datetime
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KON = os.path.join(REPO, 'konkordancia')


def olvas(fajl):
    """-> {igehely: [(strong, szo)]}; a '#' sorokat es a fejlecet kihagyja"""
    d = collections.defaultdict(list)
    fej = False
    for s in open(fajl, encoding='utf-8').read().split('\n'):
        if not s.strip() or s.startswith('#'):
            continue
        if not fej:
            fej = True
            continue
        c = s.split('\t')
        d[c[0]].append((c[2], c[3]))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luv', default=None)
    a = ap.parse_args()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    print('proveniencia: scope=konkordancia/KJV_Strongs_teljes.tsv onallo lekerdezes | forras=eszkozok/f19_ellenorzes.py | ts=%s' % ts)
    tabla = {}
    for ver in ('KJV', 'ASV'):
        fp = os.path.join(KON, ver + '_Strongs_teljes.tsv')
        if not os.path.exists(fp):
            print('== %s: a tabla nincs a repoban (l. DT19 (b))' % ver)
            continue
        d = olvas(fp)
        tabla[ver] = d
        c = collections.Counter(s for v in d.values() for s, _ in v)
        tot = sum(c.values())
        print('\n== %s: %d token, %d kulonbozo Strong' % (ver, tot, len(c)))
        print('  H430=%d H776=%d H1=%d H3068=%d H8064=%d H6440=%d G746=%d G2316=%d' % tuple(c[k] for k in ('H430', 'H776', 'H1', 'H3068', 'H8064', 'H6440', 'G746', 'G2316')))
        print('  H3068 aranya: %.2f%%; legnepszerubb 5: %s' % (100.0 * c['H3068'] / tot, c.most_common(5)))
        ph = [n for n in ('Gen.1.1', 'Jhn.1.1', 'Mrk.9.43') if n in d]
        for ig in ('Gen.1.1', 'Jhn.1.1'):
            print('  %s: %s' % (ig, ' '.join('%s=%s' % (w, s) for s, w in d.get(ig, []))))
        frazis = sum(1 for v in d.values() for _, w in v if ' ' in w.strip())
        print('  tobbszavas (frazis) "Angol szo" mezo: %d' % frazis)
        print('  pelda frazis: %s' % [(ig, w) for ig, v in d.items() for _, w in v if ' ' in w.strip()][:3])
    for ver in tabla:
        print('\n== %s vs meglevo studybible-tabla, vershalmazonkent' % ver)
        for nev, step in (('Genesis', 'Gen'), ('Exodus', 'Exo'), ('Proverbs', 'Pro')):
            regi = olvas(os.path.join(KON, '%s_Strongs_%s.tsv' % (ver, nev)))
            egy = ossz = 0
            for ig, sz in regi.items():
                if ig not in tabla[ver]:
                    continue
                ossz += 1
                egy += 1 if set(s for s, _ in sz) == set(s for s, _ in tabla[ver][ig]) else 0
            print('  %s: %d/%d vers azonos Strong-halmazzal (%.1f%%)' % (nev, egy, ossz, 100.0 * egy / max(ossz, 1)))
    if a.luv:
        print('\n== token-szintu egyezes a luvlylavnder-rel (a token Strongja benne van-e a luv ugyanazon versenek Strong-halmazaban)')
        konyvek = [s.split('\t')[0] for s in open(os.path.join(KON, 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8').read().split('\n')[1:] if s.strip()]
        for ver, alm, fj in (('KJV', 'KJV-Strongs', 'kjv_strongs.json'), ('ASV', 'ASV-Strongs', 'asvs.json')):
            if ver not in tabla:
                continue
            luv = json.load(open(os.path.join(a.luv, 'Bible-Versions', alm, fj), encoding='utf-8'))
            lsz = {}
            for r in luv['verses']:
                lsz['%s.%d.%d' % (konyvek[r['book'] - 1], r['chapter'], r['verse'])] = set(x + y for x, y in re.findall(r'[{]([HG])0*([0-9]+)[}]', r['text']))
            ben = ossz = 0
            for ig, v in tabla[ver].items():
                if ig not in lsz or not lsz[ig]:
                    continue
                for s, _ in v:
                    ossz += 1
                    ben += 1 if s in lsz[ig] else 0
            print('  %s: %d/%d token (%.1f%%)' % (ver, ben, ossz, 100.0 * ben / max(ossz, 1)))


if __name__ == '__main__':
    main()
