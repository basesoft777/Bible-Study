"""F117.5 (4.6): két fogyasztó viselkedése a régi és az új Karoli_versmegfeleltetes.tsv-n (csak olvas, semmit nem futtat újra).

1. fj2/bsb_import.fejezet_eltolasok(): a `_kk_mt_max` (az igehely_mt oszlop MT-fejezet-maximuma) és a TAHOT Károli-fejezet-
   maximuma egyezését követeli (eltérésnél SystemExit). Itt: azok a (könyv, fejezet) párok, ahol a két érték eltér,
   régi és új táblán (a BSB `text_only` versszám nélkül: csak a TAHOT-ellenőrzés feltétele).
2. sqlite_epit._bsb_szamozas(): MT-kulcs -> Károli-vers (`mt_kk` a kitöltött igehely_mt-ből, különben azonosság).
   Itt: a BSB MT-versei közül hány Károli-versre esik egynél több MT-vers (ütközés), régi és új táblán.
Használat: python naplok/F117_fogyaszto_proba.py <regi_tabla.tsv>
"""
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')
VERS = re.compile(r'^(.+) (\d+):(\d+)$')


def sorok(path):
    with open(path, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if s and not s.startswith('#'):
                yield s.split('\t')


def tabla(path):
    return [p for p in sorok(path) if p[0] != 'igehely_karoli']


def mt_max(t):
    d = defaultdict(dict)
    for p in t:
        m = re.fullmatch(r'(\d+):(\d+)', p[2])
        if m:
            b = p[0].rsplit(' ', 1)[0]
            f, v = int(m.group(1)), int(m.group(2))
            d[b][f] = max(d[b].get(f, 0), v)
    return d


def tahot_max():
    d = defaultdict(dict)
    for p in sorok(os.path.join(K, 'TAHOT_kivonat.tsv')):
        m = VERS.match(p[0])
        if m:
            b, f, v = m.group(1), int(m.group(2)), int(m.group(3))
            d[b][f] = max(d[b].get(f, 0), v)
    return d


def bsb_mt_versek():
    hu = {p[0]: p[1] for p in sorok(os.path.join(K, 'Konyv_normalizalo_tabla.tsv')) if len(p) > 1}
    out = set()
    for p in sorok(os.path.join(K, 'BSB_Strongs.tsv')):
        m = re.match(r'^([^.]+)\.(\d+)\.(\d+)$', p[0])
        if m and m.group(1) in hu:
            out.add((hu[m.group(1)], '%d:%d' % (int(m.group(2)), int(m.group(3)))))
    return out


def utkozes(t, bsb):
    mt_kk = {}
    for p in t:
        if p[2]:
            mt_kk[(p[0].rsplit(' ', 1)[0], p[2])] = p[0]
    cel = defaultdict(list)
    for (b, mk) in bsb:
        k = mt_kk.get((b, mk), '%s %s' % (b, mk))
        cel[k].append(mk)
    return {k: sorted(v) for k, v in cel.items() if len(v) > 1}


def main():
    regi = tabla(sys.argv[1])
    uj = tabla(os.path.join(K, 'Karoli_versmegfeleltetes.tsv'))
    th = tahot_max()
    for nev, t in (('régi', regi), ('új', uj)):
        mm = mt_max(t)
        elt = []
        for b, d in sorted(mm.items()):
            for f, v in sorted(d.items()):
                if th.get(b, {}).get(f) != v:
                    elt.append('%s %d (MT-max %d, TAHOT-Károli-max %s)' % (b, f, v, th.get(b, {}).get(f)))
        print('bsb_import TAHOT-ellenőrzés, %s tábla: %d fejezetben eltér: %s' % (nev, len(elt), '; '.join(elt[:40])))
    bsb = bsb_mt_versek()
    for nev, t in (('régi', regi), ('új', uj)):
        u = utkozes(t, bsb)
        print('sqlite_epit MT->Károli ütközés (BSB MT-versek), %s tábla: %d Károli-vers: %s' % (
            nev, len(u), '; '.join('%s <- %s' % (k, ','.join(v)) for k, v in sorted(u.items())[:40])))
    print('proveniencia: scope=BSB_Strongs.tsv MT-versei + TAHOT fejezet-maximum | forras=Karoli_versmegfeleltetes.tsv régi/új | '
          'eszkoz=naplok/F117_fogyaszto_proba.py | n_bsb=%d | ts=2026-10-18' % len(bsb))


if __name__ == '__main__':
    main()
