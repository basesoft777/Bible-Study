"""F120 (DT-F120a átmeneti út, (c) őrrel): a bizonytalan BSB-sorok kritériumának mérése (csak olvas).

A mai BSB_Strongs.tsv minden BSB-versére a sqlite_epit._bsb_szamozas() mai leképezése (mt_kk, különben azonosság),
majd az őr feltétele: a cél Károli-vers TAHOT-Strong-halmazának (T) mekkora hányada van meg a BSB-vers
Strong-halmazában (B): arany = |T ∩ B| / |T| (a bsb_import F41-es illeszkedési mércéje, > 0,5 = illeszkedik).
Mindkét halmaz a sqlite_epit szűrésével: strong_normalizal, a grammatikai_strongok.tsv és a H9001–H9049 nélkül.

Kimenet (stdout): az arány-eloszlás, a kihagyandó versek fejezetenként, a nem ellenőrizhető versek, és az őr utáni
ütközések. Használat: python naplok/F120_or_meres.py
"""
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))

from strong_util import strong_normalizal  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

K = os.path.join(ROOT, 'konkordancia')
STEP = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)[a-z]?$')
ALIAS = {'JSir': 'Sir'}
KUSZOB = 0.5


def sorok(path):
    with open(path, encoding='utf-8') as f:
        fej = None
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if not s or s.startswith('#'):
                continue
            m = s.split('\t')
            if fej is None:
                fej = m
                continue
            yield dict(zip(fej, m + [''] * (len(fej) - len(m))))


def halmaz_elem(nyers, gram):
    try:
        lanc = strong_normalizal(nyers)
    except ValueError:
        return []
    return [s for s in (lanc.split('+') if lanc else []) if s not in gram and not ('H9001' <= s <= 'H9049')]


def main():
    gram = {r['strong'] for r in sorok(os.path.join(ROOT, 'adat', 'grammatikai_strongok.tsv'))}
    tahot = defaultdict(set)
    for r in sorok(os.path.join(K, 'TAHOT_kivonat.tsv')):
        tahot[r['Igehely']].update(halmaz_elem(r['Strong-szám'], gram))
    karoli = {r['igehely_karoli'] for r in sorok(os.path.join(K, 'Karoli_versmegfeleltetes.tsv'))}
    mt_kk = {}
    for r in sorok(os.path.join(K, 'Karoli_versmegfeleltetes.tsv')):
        if r['igehely_mt']:
            mt_kk[(r['igehely_karoli'].rsplit(' ', 1)[0], r['igehely_mt'])] = r['igehely_karoli']
    sh = {}
    for r in sorok(os.path.join(K, 'Konyv_normalizalo_tabla.tsv')):
        hu = ALIAS.get(r['Magyar rövidítés'], r['Magyar rövidítés'])
        sh[r['STEPBible-rövidítés']] = hu
        for a in r['Forrás-alakok'].split(','):
            if a.strip():
                sh.setdefault(a.strip(), hu)
    bsb = defaultdict(set)
    szam = {}
    for r in sorok(os.path.join(K, 'BSB_Strongs.tsv')):
        m = STEP.match(r['Igehely'])
        if not m or m.group(1) not in sh:
            continue
        kulcs = (sh[m.group(1)], '%d:%d' % (int(m.group(2)), int(m.group(3))))
        bsb[kulcs].update(halmaz_elem(r['Strong-szám'], gram))
        szam[kulcs] = r['Számozás']
    eloszlas = Counter()
    kihagy = defaultdict(list)
    nem_ell = []
    cel = defaultdict(set)
    for (konyv, mk), b in sorted(bsb.items()):
        kk = mt_kk.get((konyv, mk), '%s %s' % (konyv, mk))
        if kk not in karoli:
            eloszlas['nincs Károli-vers'] += 1
            continue
        t = tahot.get(kk, set())
        if not t or not b:
            nem_ell.append('%s %s -> %s (T %d, B %d, Számozás %s)' % (konyv, mk, kk, len(t), len(b), szam[(konyv, mk)]))
            eloszlas['nem ellenőrizhető'] += 1
            cel[kk].add(mk)
            continue
        a = len(t & b) / len(t)
        if a > KUSZOB:
            eloszlas['illeszkedik (> 0,5)'] += 1
            cel[kk].add(mk)
        else:
            eloszlas['bizonytalan (<= 0,5)'] += 1
            kihagy[kk.rsplit(':', 1)[0]].append('%s->%s %.2f %s' % (mk, kk.rsplit(' ', 1)[1], a, szam[(konyv, mk)]))
    print('eloszlás: %s' % dict(eloszlas))
    print('kihagyandó versek fejezetenként (Károli-cél fejezete):')
    for f, l in sorted(kihagy.items()):
        print('  %s: %d  %s' % (f, len(l), '; '.join(l[:6]) + (' …' if len(l) > 6 else '')))
    print('nem ellenőrizhető: %d' % len(nem_ell))
    for x in nem_ell:
        print('  ' + x)
    utk = {k: sorted(v) for k, v in cel.items() if len(v) > 1}
    print('ütközés az őr után: %d %s' % (len(utk), utk))
    print('proveniencia: scope=BSB_Strongs.tsv (F71.2) x TAHOT_kivonat.tsv a Karoli_versmegfeleltetes.tsv-n át | '
          'eszkoz=naplok/F120_or_meres.py | kuszob=0,5 (|T∩B|/|T|) | ts=2026-11-01')


if __name__ == '__main__':
    main()
