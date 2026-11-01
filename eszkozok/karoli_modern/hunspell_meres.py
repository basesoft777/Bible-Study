#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.1/2 — Hunspell hu_HU fejlesztési mérés a helyesírási lépcső szabályaira (DT301).

A Hunspell CSAK fejlesztési mérce (DT301): a szabályok ellenőrzésére fut, a kiadott rétegbe és a
szóalak-szótárba nem kerül belőle alak. Ez a szkript csak ítéletet ad (elfogad / elutasít) a
helyesírási lépcső meglévő alakpárjaira; a `helyesiras_alakok.tsv` és a `helyesiras_tokenek.tsv`
alakjai nem változnak, a `tamasz` oszlop sem. A szótárfájlok a repóba nem kerülnek: a hívó adja
meg az útvonalukat (a repón kívül), a kimenet csak a sha256-jukat és a forrás-URL-t rögzíti.

Futtató: a `hunspell_driver.cxx` (a Hunspell 1.7.2 könyvtár `Hunspell::spell` hívása soronként;
fordítás: `naplok/KAROLI_MODERN_meres.md` 4.1). A futtató szavanként olvas a standard bemenetről,
és `szó<TAB>1|0` sort ír.

Olvas (csak olvas):
  adat/karoli_modern/helyesiras_alakok.tsv   a szövegkörnyezet nélkül változó alakok (1908 → modern)
  adat/karoli_modern/helyesiras_tokenek.tsv  a szövegkörnyezetfüggő párok (nevmas: a kik → akik …)

Ír (generált, kézzel nem szerkeszthető):
  adat/karoli_modern/helyesiras_hunspell.tsv  alakpáronként a két Hunspell-ítélet és az összevetés

Ítélet (`hunspell_itelet`), a pár két alakjának ítéletéből:
  megerosit   a modern alakot elfogadja, az 1908-asat elutasítja (a szabályt alátámasztja)
  semleges    mindkettőt elfogadja (a Hunspell a régi alakot is ismeri: nem dönt)
  cafol       a modern alakot elutasítja, az 1908-asat elfogadja (a szabály gyanús: jelzendő)
  ismeretlen  mindkettőt elutasítja (tulajdonnév, ritka szó: nem dönt a szabályról, de a modern
              alak sem támasztott)

Használat:
    python eszkozok/karoli_modern/hunspell_meres.py --futtato <hs_check> --aff <hu_HU.aff> --dic <hu_HU.dic>
    ... --kimenet <könyvtár>   (próba a repón kívülre)
"""

import argparse
import collections
import hashlib
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALAKOK = 'adat/karoli_modern/helyesiras_alakok.tsv'
TOKENEK = 'adat/karoli_modern/helyesiras_tokenek.tsv'
KI = 'adat/karoli_modern/helyesiras_hunspell.tsv'
FORRAS_URL = ('https://raw.githubusercontent.com/LibreOffice/dictionaries/'
              '67032ee957631908098a72edf48dc81cac27e369/hu_HU/')


def sha_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def olvas_tsv(rel):
    """(fejléc-mezők, sorok dict-ként); az első `#` sor a GENERÁLT-fejléc."""
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        sorok = f.read().split('\n')
    sorok = [s for s in sorok if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ki = []
    for s in sorok[1:]:
        m = s.split('\t')
        if len(m) != len(fej):
            sys.exit('HIBA: mezőszám-eltérés: %s: %r' % (rel, s[:80]))
        ki.append(dict(zip(fej, m)))
    return fej, ki


def hunspell(futtato, aff, dic, szavak):
    bemenet = '\n'.join(szavak) + '\n'
    p = subprocess.run([futtato, aff, dic], input=bemenet.encode('utf-8'),
                       stdout=subprocess.PIPE, check=True)
    ered = {}
    for s in p.stdout.decode('utf-8').split('\n'):
        if not s:
            continue
        m = s.split('\t')
        ered[m[0]] = m[1] == '1'
    hiany = [w for w in szavak if w not in ered]
    if hiany:
        sys.exit('HIBA: a futtató %d szóra nem adott ítéletet (pl. %r)' % (len(hiany), hiany[:3]))
    return ered


def itelet(regi_ok, uj_ok):
    if uj_ok and not regi_ok:
        return 'megerosit'
    if uj_ok and regi_ok:
        return 'semleges'
    if regi_ok:
        return 'cafol'
    return 'ismeretlen'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--futtato', required=True)
    ap.add_argument('--aff', required=True)
    ap.add_argument('--dic', required=True)
    ap.add_argument('--kimenet', default=None, help='próba-kimenet könyvtára (a repón kívül)')
    a = ap.parse_args()

    _, alakok = olvas_tsv(ALAKOK)
    _, tokenek = olvas_tsv(TOKENEK)

    # 1) a szövegkörnyezet nélküli alakpárok (minden sor)
    parok = collections.OrderedDict()
    for r in alakok:
        parok[(r['alak'], r['alak_modern'])] = {
            'forras': 'alakok', 'szabaly': r['szabaly'], 'tamasz': r['tamasz'],
            'gyakorisag': int(r['gyakorisag'])}
    # 2) a szövegkörnyezetfüggő párok a tokentáblából (nem kieső, változó, nem az 1. pontban)
    tok_gyak = collections.Counter()
    tok_szab = {}
    for r in tokenek:
        if r['kieso'] or r['alak_1908'] == r['alak_modern']:
            continue
        k = (r['alak_1908'], r['alak_modern'])
        if k in parok:
            continue
        tok_gyak[k] += 1
        tok_szab.setdefault(k, r['szabaly'])
    for k, n in sorted(tok_gyak.items(), key=lambda x: (-x[1], x[0])):
        parok[k] = {'forras': 'tokenek', 'szabaly': tok_szab[k], 'tamasz': '', 'gyakorisag': n}

    szavak = sorted({w for k in parok for w in k})
    ered = hunspell(a.futtato, a.aff, a.dic, szavak)

    sha_aff, sha_dic = sha_fajl(a.aff), sha_fajl(a.dic)
    sha_szkript = sha_fajl(os.path.abspath(__file__))
    sha_driver = sha_fajl(os.path.join(ROOT, 'eszkozok', 'karoli_modern', 'hunspell_driver.cxx'))
    sha_be = (sha_fajl(os.path.join(ROOT, ALAKOK)), sha_fajl(os.path.join(ROOT, TOKENEK)))

    fejlec = ('# GENERÁLT: eszkozok/karoli_modern/hunspell_meres.py (F96.1/2) — kézzel nem szerkeszthető | '
              'Hunspell hu_HU CSAK fejlesztési mérce (DT301): ítélet a meglévő alakpárokra, a kimeneti rétegbe '
              'nem kerül belőle alak, a tamasz oszlop nem változik | '
              'forras=%s + %s (sha256:%s / %s) | hunspell=%s{hu_HU.aff,hu_HU.dic} '
              '(sha256:%s / %s; MPLv2 vagy LGPLv3+, Németh László és Godó Ferenc, v1.9) + Hunspell 1.7.2 '
              '(hunspell_driver.cxx sha256:%s) + hunspell_meres.py (sha256:%s) | scope=%d alakpár (%d szó)\n'
              % (ALAKOK, TOKENEK, sha_be[0][:12], sha_be[1][:12], FORRAS_URL, sha_aff[:12], sha_dic[:12],
                 sha_driver[:12], sha_szkript[:12], len(parok), len(szavak)))
    oszl = ['alak_1908', 'alak_modern', 'forras', 'szabaly', 'tamasz', 'gyakorisag',
            'hunspell_1908', 'hunspell_modern', 'hunspell_itelet']
    kimenet_sorok = []
    stat = collections.Counter()
    for (regi, uj), d in parok.items():
        ro, uo = ered[regi], ered[uj]
        it = itelet(ro, uo)
        kimenet_sorok.append([regi, uj, d['forras'], d['szabaly'], d['tamasz'], str(d['gyakorisag']),
                              'elfogad' if ro else 'elutasit', 'elfogad' if uo else 'elutasit', it])
        stat[(d['forras'], d['tamasz'] or '-', it)] += 1

    ki_ut = os.path.join(a.kimenet, os.path.basename(KI)) if a.kimenet else os.path.join(ROOT, KI)
    with open(ki_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec)
        f.write('\t'.join(oszl) + '\n')
        for s in kimenet_sorok:
            f.write('\t'.join(s) + '\n')
    print('írva: %s (%d pár, %d szó)' % (os.path.relpath(ki_ut, ROOT) if not a.kimenet else ki_ut,
                                          len(parok), len(szavak)))
    print('sha256 aff=%s dic=%s' % (sha_aff, sha_dic))
    for k in sorted(stat):
        print('%s\t%s\t%s\t%d' % (k[0], k[1], k[2], stat[k]))


if __name__ == '__main__':
    main()
