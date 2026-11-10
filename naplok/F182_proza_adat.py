# -*- coding: utf-8 -*-
"""F182 HAMART-001, 1. fázis, F2 — az 1Móz 7:23 1/a prózája (adat/elofordulasok.tsv `kapcsolodas`, `funkcio`).

A vers vége csonkítva állt („csak Noé marada meg”), a funkció pedig „egyedül Noé marad meg”-et mondott, holott a
Károli-vers: „és csak Noé marada meg, és azok a kik vele valának a bárkában”. A javítás a teljes tagmondatot idézi
(konkordancia/Karoli_1908.tsv), és a funkció is a veléjük lévőket nevezi meg. A próza keze: claude-opus-5-5.

Írás előtt csak a megnevezett sor két mezője változhat (összevetés); a `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F182_proza_adat.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'adat/elofordulasok.tsv'
KULCS = ('HAMART-001', '1Móz 7:23')
REGI = {
    'kapcsolodas': 'Az elbeszélés rögzíti a végrehajtást: „eltörle az Isten minden állatot, a mely a föld színén vala, '
                   'az embertől a baromig”. A 6:7 felsorolása tér itt vissza, és a vers végén megnevezi, aki megmarad: '
                   '„csak Noé marada meg”.',
    'funkcio': '🌊 özönvíz — a 6:7 ítéletének végrehajtása; egyedül Noé marad meg',
}
UJ = {
    'kapcsolodas': 'Az elbeszélés rögzíti a végrehajtást: „eltörle az Isten minden állatot, a mely a föld színén vala, '
                   'az embertől a baromig”. A 6:7 felsorolása tér itt vissza, és a vers végén megnevezi, akik '
                   'megmaradnak: „csak Noé marada meg, és azok a kik vele valának a bárkában”.',
    'funkcio': '🌊 özönvíz — a 6:7 ítéletének végrehajtása; csak Noé és a vele lévők maradnak meg a bárkában',
}
PROV = 'scope=manual | forras=F182 HAMART-001, 1. fázis, F2 (claude-opus-5-5; a Károli-vers teljes tagmondata: konkordancia/Karoli_1908.tsv) | ts=2026-11-10'


def main(ir):
    sorok = open(UT, encoding='utf-8', newline='').read().split('\n')
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    fej = sorok[fej_i].split('\t')
    ix = {k: i for i, k in enumerate(fej)}
    karoli = {l.split('\t', 1)[0]: l.split('\t', 1)[1] for l in
              open('konkordancia/Karoli_1908.tsv', encoding='utf-8').read().split('\n')[1:] if '\t' in l}
    assert 'csak Noé marada meg, és azok a kik vele valának a bárkában' in karoli['1Móz 7:23']
    eredeti = list(sorok)
    talalt = 0
    for n in range(fej_i + 1, len(sorok)):
        r = sorok[n].split('\t')
        if tuple(r[:2]) != KULCS:
            continue
        for k in REGI:
            assert r[ix[k]] == REGI[k], (k, r[ix[k]])
            r[ix[k]] = UJ[k]
        r[ix['proveniencia']] = PROV
        sorok[n] = '\t'.join(r)
        talalt += 1
    assert talalt == 1
    elter = [i for i in range(len(sorok)) if sorok[i] != eredeti[i]]
    assert len(elter) == 1
    print('%s: 1 sor (%s), mezők: kapcsolodas, funkcio, proveniencia' % (UT, KULCS[1]))
    if ir:
        open(UT, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
    else:
        print('(próba; írás: --ir)')


if __name__ == '__main__':
    main('--ir' in sys.argv)
