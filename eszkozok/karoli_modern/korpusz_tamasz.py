#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.0 — korpusz-támasz becslés: a jegyes alakokra a szabályos mai alak-jelöltek (a régies jegy
szerint, a szótári alak tövéből) közül hány szerepel magában a Károli 1908 korpuszban.

Ha pontosan egy jelölt szerepel, a mai alak a korpuszból egyértelmű (`egy`); ha több, a választás
a -t/-tt vagy a tárgyas/alanyi ragozáson múlik (`tobb`); ha egy sem, a szabály korpusz nélkül
dönt, vagy LLM-jelölt (`nincs`). Ez a .0 döntési opcióihoz becslés (mekkora LLM-maradék szűnne meg
korpusz-támaszú szabállyal), nem a kiadott szabálykészlet; a jelöltlisták kézi (manual), a mai
magyar igeragozás általános ismeretéből.

Olvas: `adat/karoli_modern/fedettseg_alakok.tsv`, `konkordancia/Karoli_1908.tsv`.
Használat: python eszkozok/karoli_modern/korpusz_tamasz.py
"""

import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
import tokenek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FEDETTSEG = os.path.join('adat', 'karoli_modern', 'fedettseg_alakok.tsv')
KAROLI = os.path.join('konkordancia', 'Karoli_1908.tsv')

VEG = {
    'mult.targyas.E3': ['ta', 'te', 'tta', 'tte', 'otta', 'ette', 'ötte'],
    'mult.alanyi.E3': ['t', 'tt', 'ott', 'ett', 'ött'],
    'mult.E3': ['t', 'tt', 'ott', 'ett', 'ött'],
    'mult.T3': ['tak', 'tek', 'ttak', 'ttek', 'ottak', 'ettek', 'öttek', 'ták', 'ték', 'tták', 'tték'],
    'mult.E1': ['tam', 'tem', 'ttam', 'ttem', 'ottam', 'ettem', 'öttem', 'tak', 'tek', 'ták', 'ték', 'tták', 'tték'],
    'mult.E2': ['tál', 'tél', 'ttál', 'ttél', 'ottál', 'ettél', 'öttél'],
    'mult.T1': ['tunk', 'tünk', 'ttunk', 'ttünk', 'ottunk', 'ettünk', 'öttünk', 'tuk', 'tük', 'ttuk', 'ttük'],
    'mult.T2': ['tatok', 'tetek', 'ttatok', 'ttetek', 'ottatok', 'ettetek', 'öttetek', 'tátok', 'tétek', 'ttátok', 'ttétek'],
}


def main():
    szavak = set()
    with open(os.path.join(ROOT, KAROLI), encoding='utf-8') as f:
        next(f)
        for l in f:
            m = l.rstrip('\n').split('\t')
            if len(m) >= 2:
                szavak.update(t.lower() for t in tokenek.tokenizal(m[1]))
    fej = None
    eredm = collections.Counter()
    jegyenkent = collections.defaultdict(collections.Counter)
    latott = set()
    with open(os.path.join(ROOT, FEDETTSEG), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            r = dict(zip(fej, m))
            if r['osztaly'] not in ('igealak_ritka', 'igealak_gyakori'):
                continue
            kis = r['alak'].lower()
            if kis in latott:
                continue
            latott.add(kis)
            jegy, lemma = r['regies_jegy'], r['szotari_alak']
            to = lemma[:-2] if lemma.endswith('ik') else lemma
            if jegy == 'hatarozoi_igenev':
                jel = [kis[:-3] + 'va', kis[:-3] + 've'] if kis.endswith(('ván', 'vén')) else []
            elif jegy == 'felszolito.E2':
                jel = [kis[:-2]] if kis.endswith(('ál', 'él')) else []
            else:
                jel = [to + v for v in VEG.get(jegy, [])]
            van = [j for j in jel if j in szavak]
            k = 'egy' if len(van) == 1 else ('tobb' if van else 'nincs')
            eredm[(r['osztaly'], k)] += 1
            jegyenkent[jegy][k] += 1
    print('osztaly\tegy\ttobb\tnincs')
    for o in ('igealak_gyakori', 'igealak_ritka'):
        print('%s\t%d\t%d\t%d' % (o, eredm[(o, 'egy')], eredm[(o, 'tobb')], eredm[(o, 'nincs')]))
    print('jegy\tegy\ttobb\tnincs')
    for j in sorted(jegyenkent):
        c = jegyenkent[j]
        print('%s\t%d\t%d\t%d' % (j, c['egy'], c['tobb'], c['nincs']))


if __name__ == '__main__':
    main()
