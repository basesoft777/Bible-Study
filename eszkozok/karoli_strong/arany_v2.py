#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.12 — az Opus-arany v2 előállítása a v1-ből (f21p/arany_opus.jsonl ->
f21p/arany_opus_v2.jsonl). A v1 nem változik.

Csak a jegyzet (f21p/arany_opus_jegyzetek.md 2. szakasz) konvencióival ütköző
esetek javulnak; minden javításnál a sértett konvenció száma. A többi sor bájtra
azonos a v1-gyel (a szkript ellenőrzi). A v2 jóváhagyásig nem fagy be.

Javítások (JAVITASOK): vers -> (felülírt/új párok {magyar: [eredeti...]},
betoldas-ból törlendő, betoldas-hoz adandó, forditatlan-hoz adandó,
forditatlan-ból törlendő, konvenció, indok).

Futtatás a repó gyökeréből:
    python eszkozok/karoli_strong/arany_v2.py
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

V1 = os.path.join(tokenek.ROOT, 'f21p', 'arany_opus.jsonl')
V2 = os.path.join(tokenek.ROOT, 'f21p', 'arany_opus_v2.jsonl')

JAVITASOK = {
    '2Móz 25:8': {
        'parok': {7: [10]},
        'betoldas_torol': [7], 'betoldas_ad': [], 'forditatlan_ad': [], 'forditatlan_torol': [],
        'konvencio': 'K4 (2. szakasz 4.: birtokos és névmási ragok — ha a magyar külön névmást is kitesz, a névmáshoz is)',
        'indok': 'az ő közöttök archaikus birtokos szerkezet (vö. az ő ura): az ő a -ām („őket, köztük”) rag külön kitett '
                 'névmása, nem az 1. személyű ige alanya; a v1 tévesen K6-ként (betoldas) kezelte',
    },
    '2Móz 26:13': {
        'parok': {24: [27, 28]},
        'betoldas_torol': [], 'betoldas_ad': [], 'forditatlan_ad': [26], 'forditatlan_torol': [],
        'konvencio': 'K9 (2. szakasz 9.: le nem fordított ve-/kai forditatlan)',
        'indok': 'a וּ (26) a magyarban nem a másfelől része; a v1 a másfelől-höz kötötte, ami a K9-cel ütközik. '
                 'Nyitott: a K9 szerint az is-hez is köthető volna (egyfelől is másfelől is), de az is betoldas-a a '
                 '6. táblázat dokumentált döntése, ezért a v2 a minimális javítást (forditatlan) alkalmazza',
    },
}


def javit(o, j):
    parok = {m: e for m, e in o['parok']}
    parok.update(j['parok'])
    return {
        'vers': o['vers'],
        'parok': [[m, parok[m]] for m in sorted(parok)],
        'betoldas': sorted((set(o['betoldas']) - set(j['betoldas_torol'])) | set(j['betoldas_ad'])),
        'forditatlan': sorted((set(o['forditatlan']) - set(j['forditatlan_torol'])) | set(j['forditatlan_ad'])),
    }


def main():
    with open(V1, encoding='utf-8') as f:
        v1 = f.read()
    sorok = v1.split('\n')
    ki = []
    for s in sorok:
        if s.strip():
            o = json.loads(s)
            if o['vers'] in JAVITASOK:
                o2 = javit(o, JAVITASOK[o['vers']])
                print('%s (%s)' % (o['vers'], JAVITASOK[o['vers']]['konvencio'].split(' ')[0]))
                print('  v1: %s' % s)
                s = json.dumps(o2, ensure_ascii=False, separators=(',', ':'))
                print('  v2: %s' % s)
        ki.append(s)
    elteres = {json.loads(a)['vers'] for a, b in zip(sorok, ki) if a != b}
    if elteres != set(JAVITASOK) or len(ki) != len(sorok):
        raise SystemExit('váratlan eltérés a v1-től: %s' % sorted(elteres))
    if os.path.exists(tokenek.ARANY_V2_SHA):
        # F21.14: a v2 befagyasztva; a szkript csak ellenőriz, nem ír felül
        import hashlib
        uj = hashlib.sha256('\n'.join(ki).encode('utf-8')).hexdigest()
        meglevo = tokenek.arany_v2_befagyasztas_ellenoriz(V2)
        if uj != meglevo:
            raise SystemExit('HIBA: a v2 befagyasztva (%s), a most előállított tartalom eltér; nem írom felül' % meglevo)
        print('v2 befagyasztva; az előállított tartalom egyezik (sha256 %s), nem írtam felül' % meglevo)
        return
    with open(V2, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki))
    print('v2: %d vers változott -> %s' % (len(elteres), V2))


if __name__ == '__main__':
    main()
