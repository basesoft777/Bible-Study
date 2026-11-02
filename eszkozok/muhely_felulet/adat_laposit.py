#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F156: a Feed-JSON laposítása a Dashboard adatfájljaihoz.

Nyilvános adat (a `feed_nyilvanos.json`-ból, csak előrehaladás): motivumok, tortenes, stash.
Belső adat (a `feed_belso.json`-ból): belso_matrix, belso_hatra, belso_kapuk.
Használat: python eszkozok/muhely_felulet/adat_laposit.py <kimeneti könyvtár>"""
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'generalt', 'muhely')
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ny = json.load(open(os.path.join(G, 'feed_nyilvanos.json'), encoding='utf-8'))
be = json.load(open(os.path.join(G, 'feed_belso.json'), encoding='utf-8'))

mot, stash, tort = [], [], []
for m in ny['motivumok']:
    st = m.get('stash') or {}
    mot.append({'id': m['id'], 'cim': m['cim'], 'allas': m['allasfokozat'], 'mondat': m['olvasoi_mondat'],
                'zold_db': m['zold_db'], 'ossz_db': m['ossz_db'], 'elvetett': m['elvetett_jelolt_db'],
                'beepitett': m['beepitett_jelolt_db'],
                'lepesek': ' · '.join(k['olvasoi_nev'] for k in m['teljesult_lepesek'])})
    if st:
        stash.append({'id': m['id'], 'cim': st['cim'], 'osz': st['elofordulas_osz'], 'usz': st['elofordulas_usz'],
                      'kapcs': st['kapcsolatok_db'], 'szo': st['terjedelem_szo'], 'kotet': st['kotet_olvasoi'],
                      'fole': st['folerendelt_fogalom'], 'neg': st['negativ_kriterium'],
                      'kiadas': st.get('kiadas_allapot') or ''})
for e in ny['heti_tortenes']:
    tort.append({'kulcs': '%s|%s|%s' % (e['datum'], e['motivum'], e['olvasoi_esemeny']), 'datum': e['datum'],
                 'motivum': e['motivum'], 'esemeny': e['olvasoi_esemeny']})

matrix, hatra, belso = [], [], []
for m in be['motivumok']:
    sor = {'id': m['id'], 'mondat': m['olvasoi_mondat'], 'allas': m['allasfokozat_olvasoi']}
    for k in m['kriteriumok']:
        sor['k%d' % k['sorszam']] = k['olvasoi_allapot']
        sor['s%d' % k['sorszam']] = k['szin']
        kulcs = '%s|%d' % (m['id'], k['sorszam'])
        belso.append({'kulcs': kulcs, 'motivum': m['id'], 'kapu': k['nev'], 'allapot': k['allapot'],
                      'ertek': k['ertek'], 'reszlet': '; '.join(k['reszlet'])[:300], 'prov': k['proveniencia']})
        if k['allapot'] != 'zold':
            hatra.append({'kulcs': kulcs, 'motivum': m['id'], 'sorszam': k['sorszam'], 'szin': k['szin'],
                          'nev': k['olvasoi_nev'], 'allapot': k['olvasoi_allapot'], 'szoveg': k['olvasoi_szoveg']})
    matrix.append(sor)

for nev, rows in (('motivumok', mot), ('stash', stash), ('tortenes', tort), ('belso_matrix', matrix),
                  ('belso_hatra', hatra), ('belso_kapuk', belso)):
    json.dump(rows, open(os.path.join(out, nev + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(nev, len(rows))
