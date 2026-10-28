#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/glossza_minta.py -- F140 DT-F140c (b): rétegzett, véletlen minta a nem átnézett glosszákból.

Jogosult sor: allapot=sonnet (nem `kezi`), az entry_id nincs az átnézési listán
(naplok/GLOSSZA_FORDITAS_atnezes.tsv), nem H9xxx (az egységesített előtag/utótag-csoport).
Rétegek (egymást kizáróan, ebben a sorrendben): ige (glossza_en `to `-val kezdődik; 70),
ritka (nem ige, TAHOT-előfordulás <= 5; 70), egyéb (60). Seed rögzített (140).
Kimenet: naplok/GLOSSZA_FORDITAS_minta_DTF140c.tsv (az `itelet` és `javaslat_hu` oszlopot az átnéző tölti).
Őr: létező kimeneti fájlt csak `--felulir` mellett ír felül (az átnézett minta oszlopai: itelet, javaslat_hu,
megjegyzes elvesznének). A minta a DT-F140c javításai után NEM reprodukálható: a jogosult halmaz az aktuális
`allapot`-tól függ (a kijavított `kezi` sorok kiesnek); a rögzített seed csak a javítás előtti állapotra ad
ugyanazt; a minta tartalma a két mintafájlban él (naplok/GLOSSZA_FORDITAS_minta*_DTF140c.tsv).
  python eszkozok/glossza_minta.py --ige-kozos   DT-F140c (b): az összes át nem nézett `sonnet` ige-sor, amelynek
    angol glosszáján legalább 2 Strong osztozik (a testvér-, minta- és átnézési-listás sorok kizárva); kimenet:
    naplok/GLOSSZA_FORDITAS_ige_kozos_DTF140c.tsv (glossza szerint rendezve)
A minta (a fő, az --ige2 és az --ige-kozos is) a javítások után NEM reprodukálható: a jogosult halmaz az
aktuális `allapot`-tól függ, a kijavított (`kezi`) sorok kiesnek; a tényleges minta a naplok/ alatti fájlokban él.
Használat: python eszkozok/glossza_minta.py [--felulir | --ige2 | --ige-kozos]
  python eszkozok/glossza_minta.py --ige2   második ige-minta (DT-F140c (A) 3. lépés): 150 sor, seed 141,
    kizárja az első minta soraiból és a DT-F140c javításaiból érintett sorokat; kimenet:
    naplok/GLOSSZA_FORDITAS_minta2_ige_DTF140c.tsv
"""
import sys
import os
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glossza_forditas as g

SEED = 140
MERET = {'ige': 70, 'ritka': 70, 'egyeb': 60}
KIMENET = os.path.join(g.GYOKER, 'naplok', 'GLOSSZA_FORDITAS_minta_DTF140c.tsv')
ATNEZES = os.path.join(g.GYOKER, 'naplok', 'GLOSSZA_FORDITAS_atnezes.tsv')


def atnezett():
    ids = set()
    with open(ATNEZES, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            m = sor.rstrip('\n').split('\t')
            if i and len(m) > 2:
                ids.add(m[2])
    return ids


def kizart_minta():
    ids = set()
    with open(KIMENET, encoding='utf-8') as f:
        for i, sor in enumerate(f):
            m = sor.split('\t')
            if i and len(m) > 2:
                ids.add(m[2])
    return ids


def vedett(ut):
    if os.path.exists(ut) and '--felulir' not in sys.argv:
        raise SystemExit('MEGALL: a(z) %s mar letezik (atnezett minta); felulirasa csak --felulir mellett' % ut)


def main_ige2():
    tabla = g.tabla_olvas()
    tb = {s['entry_id']: s for s in g.tbesh_sorok()}
    gyak = g.tahot_gyakorisag()
    kiz = atnezett() | kizart_minta()
    jel = [k for k in sorted(tabla) if tabla[k]['allapot'] == 'sonnet' and k not in kiz
           and not tabla[k]['strong'].startswith('H9') and tabla[k]['glossza_en'].startswith('to ')]
    rnd = random.Random(141)
    ki = sorted(rnd.sample(jel, 150))
    ut = os.path.join(g.GYOKER, 'naplok', 'GLOSSZA_FORDITAS_minta2_ige_DTF140c.tsv')
    vedett(ut)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['reteg', 'strong', 'entry_id', 'tahot_elofordulas', 'lemma', 'glossza_en',
                           'definicio_eleje', 'glossza_hu', 'itelet', 'javaslat_hu', 'megjegyzes']) + '\n')
        for k in ki:
            r, s = tabla[k], tb[k]
            f.write('\t'.join(['ige2', r['strong'], k, str(gyak.get(r['strong'], 0)), s['lemma'], r['glossza_en'],
                               s['definicio'][:160], r['glossza_hu'], '', '', '']) + '\n')
    print('ige2: jogosult %d, minta %d -> %s' % (len(jel), len(ki), ut))


def main_ige_kozos():
    import collections
    tabla = g.tabla_olvas()
    tb = {s['entry_id']: s for s in g.tbesh_sorok()}
    gyak = g.tahot_gyakorisag()
    kiz = atnezett()
    for f in ('GLOSSZA_FORDITAS_minta_DTF140c.tsv', 'GLOSSZA_FORDITAS_minta2_ige_DTF140c.tsv',
              'GLOSSZA_FORDITAS_testver_DTF140d.tsv'):
        with open(os.path.join(g.GYOKER, 'naplok', f), encoding='utf-8') as fh:
            for i, sor in enumerate(fh):
                m = sor.split('\t')
                if i and len(m) > 2:
                    kiz.add(m[2])
    ige = [k for k, r in tabla.items() if r['glossza_en'].startswith('to ') and not r['strong'].startswith('H9')]
    csop = collections.defaultdict(list)
    for k in ige:
        csop[tabla[k]['glossza_en']].append(k)
    ki = []
    for gl in sorted(csop):
        if len({tabla[k]['strong'] for k in csop[gl]}) < 2:
            continue
        ki += [k for k in sorted(csop[gl]) if tabla[k]['allapot'] == 'sonnet' and k not in kiz]
    ut = os.path.join(g.GYOKER, 'naplok', 'GLOSSZA_FORDITAS_ige_kozos_DTF140c.tsv')
    vedett(ut)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['reteg', 'strong', 'entry_id', 'tahot_elofordulas', 'lemma', 'glossza_en',
                           'definicio_eleje', 'glossza_hu', 'itelet', 'javaslat_hu', 'megjegyzes']) + '\n')
        for k in ki:
            r, s = tabla[k], tb[k]
            f.write('\t'.join(['ige_kozos', r['strong'], k, str(gyak.get(r['strong'], 0)), s['lemma'], r['glossza_en'],
                               s['definicio'][:160], r['glossza_hu'], '', '', '']) + '\n')
    print('ige_kozos: %d sor -> %s' % (len(ki), ut))


def main():
    if '--ige-kozos' in sys.argv:
        return main_ige_kozos()
    if '--ige2' in sys.argv:
        return main_ige2()
    vedett(KIMENET)
    tabla = g.tabla_olvas()
    tb = {s['entry_id']: s for s in g.tbesh_sorok()}
    gyak = g.tahot_gyakorisag()
    atn = atnezett()
    reteg = {k: [] for k in MERET}
    for k in sorted(tabla):
        r = tabla[k]
        if r['allapot'] != 'sonnet' or k in atn or r['strong'].startswith('H9'):
            continue
        if r['glossza_en'].startswith('to '):
            reteg['ige'].append(k)
        elif gyak.get(r['strong'], 0) <= 5:
            reteg['ritka'].append(k)
        else:
            reteg['egyeb'].append(k)
    rnd = random.Random(SEED)
    sorok = []
    for nev in ('ige', 'ritka', 'egyeb'):
        print('%s: jogosult %d, minta %d' % (nev, len(reteg[nev]), MERET[nev]))
        for k in sorted(rnd.sample(reteg[nev], MERET[nev])):
            r, s = tabla[k], tb[k]
            sorok.append([nev, r['strong'], k, str(gyak.get(r['strong'], 0)), s['lemma'], r['glossza_en'],
                          s['definicio'][:160], r['glossza_hu'], '', '', ''])
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['reteg', 'strong', 'entry_id', 'tahot_elofordulas', 'lemma', 'glossza_en',
                           'definicio_eleje', 'glossza_hu', 'itelet', 'javaslat_hu', 'megjegyzes']) + '\n')
        for m in sorok:
            f.write('\t'.join(m) + '\n')
    print('minta: %d sor -> %s' % (len(sorok), KIMENET))


if __name__ == '__main__':
    main()
