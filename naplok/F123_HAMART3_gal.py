# -*- coding: utf-8 -*-
"""F123 HAMART-001, N-F123hc döntése (a felhasználó, 2026-11-08, az orkesztrátoron át, szó szerint: „a”; a hangnemről:
„így már látszik, hogy ezt nagyon ki akartuk domborítani”). Helyőrző: DT-F123hd.
- Gal 3:10 elutasítva és kikerül az elofordulasok.tsv-ből (a K7 következménye: az 5Móz 27:26 szövetségi átok-mondata);
- Gal 3:13 → Gal 3:13-14, tartományként, határesetként; az 1/a próza és a funkció a felhasználó jóváhagyott szövege;
- az elutasitasi_okok.tsv 126-os mintája a Gal 3:10 indoklásának fordulatát is felismeri.
Írás előtt soronként összevet: csak a megnevezett sorok változnak. Futtatás a repó gyökeréből:
python naplok/F123_HAMART3_gal.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ID, DT, DATUM = 'HAMART-001', 'DT-F123hd', '2026.11.08'
PROV = ('scope=manual | forras=F123 HAMART-001, N-F123hc döntése (claude-opus-5-5; a felhasználó szövege, DT-F123hd) '
        '| ts=2026-11-08')
GAL310 = ('Pál az 5Móz 27:26 átok-mondatát idézi; az átok a tóra megszegőjére szól, a szövetség rendjében, a föld szava '
          'nélkül, mint az 5Móz 27:15-26 — a motívum határán kívül.')
GAL313_IND = ('Beépítve, határesetként: Pál az 5Móz 21:23 átok-mondatát idézi, amelyben az átok és a föld együtt áll, a '
              'lánc görög átok-szavával (ἐπικατάρατος, epikataratosz); a kapcsolatot a 3:14 áldás-mondata adja, amely az '
              '1Móz 12:3 ígéretét veszi fel.')
GAL313_KAPCS = ('A Gal 3:13 az 5Móz 21:23 átok-mondatát idézi („Átkozott minden, a ki fán függ”). Az idézett versben az átok '
                'és a föld együtt áll, és Pál a lánc görög átok-szavát használja. A Genezisre közvetlenül nem utal vissza; a '
                'kapcsolatot a 3:14 áldás-mondata adja, amely az 1Móz 12:3 ígéretét veszi fel.')
GAL313_FUNK = 'átok és áldás — határeset: a kapcsolat az áldás-mondaton át'
OK_REGI, OK_UJ = 'szövetségi átok-formula', 'szövetségi átok-formula|a szövetség rendjében, a föld szava nélkül'


def beolvas(ut):
    s = open(ut, encoding='utf-8', newline='').read().split('\n')
    fi = next(i for i, l in enumerate(s) if l and not l.startswith('#'))
    return s, fi, {k: i for i, k in enumerate(s[fi].split('\t'))}


def ir(ut, sorok, ok):
    if ok:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))


def main(irj):
    # elutasítási ok
    ut = 'adat/elutasitasi_okok.tsv'
    s, fi, ix = beolvas(ut)
    n = [i for i, l in enumerate(s) if l.split('\t')[:2] == ['126', ID]]
    assert len(n) == 1
    r = s[n[0]].split('\t')
    assert r[ix['minta']] == OK_REGI, r[ix['minta']]
    r[ix['minta']] = OK_UJ
    s[n[0]] = '\t'.join(r)
    ir(ut, s, irj)
    print(ut, ': 1 minta')
    # jelöltek
    ut = 'adat/jeloltek.tsv'
    s, fi, ix = beolvas(ut)
    eredeti, kesz = list(s), []
    for i in range(fi + 1, len(s)):
        r = s[i].split('\t')
        if len(r) < len(ix) or r[0] != ID or r[ix['jelolt_tipus']] != 'elofordulas':
            continue
        if r[1] == 'Gal 3:10':
            assert r[ix['dontes']] == 'beépítve'
            r[ix['dontes']], r[ix['indoklas']] = 'elutasítva', GAL310
        elif r[1] == 'Gal 3:13':
            assert r[ix['dontes']] == 'beépítve'
            r[1], r[ix['indoklas']] = 'Gal 3:13-14', GAL313_IND
        else:
            continue
        r[ix['datum']], r[ix['dontes_ref']] = DATUM, DT
        s[i] = '\t'.join(r)
        kesz.append(i)
    assert len(kesz) == 2 and sum(1 for a, b in zip(s, eredeti) if a != b) == 2
    ir(ut, s, irj)
    print(ut, ': 2 sor')
    # előfordulások
    ut = 'adat/elofordulasok.tsv'
    s, fi, ix = beolvas(ut)
    ki, lat = [], []
    for i, l in enumerate(s):
        r = l.split('\t')
        if i > fi and len(r) >= len(ix) and r[0] == ID and r[1] == 'Gal 3:10':
            lat.append('ki')
            continue
        if i > fi and len(r) >= len(ix) and r[0] == ID and r[1] == 'Gal 3:13':
            r[1], r[ix['kapcsolodas']], r[ix['funkcio']], r[ix['proveniencia']] = 'Gal 3:13-14', GAL313_KAPCS, GAL313_FUNK, PROV
            lat.append('mod')
            l = '\t'.join(r)
        ki.append(l)
    assert sorted(lat) == ['ki', 'mod'], lat
    ir(ut, ki, irj)
    print(ut, ': 1 törölve, 1 módosítva')


if __name__ == '__main__':
    main('--ir' in sys.argv)
    if '--ir' not in sys.argv:
        print('(próba; írás: --ir)')
