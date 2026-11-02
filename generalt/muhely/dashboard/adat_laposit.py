#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F156: a nyilvános/belső Feed-JSON laposítása a Dashboard adatfájljaihoz (motivumok, kapuk, stash, tortenes,
belso_kapuk). Használat: python generalt/muhely/dashboard/adat_laposit.py <kimeneti könyvtár>"""
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ny = json.load(open(os.path.join(G, 'feed_nyilvanos.json'), encoding='utf-8'))
be = json.load(open(os.path.join(G, 'feed_belso.json'), encoding='utf-8'))

mot, kapuk, stash, tort, belso = [], [], [], [], []
for m in ny['motivumok']:
    mot.append({'id': m['id'], 'cim': m['cim'], 'allas': m['allasfokozat'], 'mondat': m['olvasoi_mondat'],
                'zold_db': m['zold_db'], 'ossz_db': m['ossz_db'],
                'nyitott_jelolt': m['nyitott_jelolt_db'], 'elvetett_jelolt': m['elvetett_jelolt_db']})
    for k in m['kriteriumok']:
        kapuk.append({'kulcs': '%s|%d' % (m['id'], k['sorszam']), 'motivum': m['id'], 'sorszam': k['sorszam'],
                      'szin': k['szin'], 'nev': k['olvasoi_nev'], 'allapot': k['olvasoi_allapot'],
                      'szoveg': k['olvasoi_szoveg']})
    s = m.get('stash')
    if s:
        stash.append({'id': m['id'], 'cim': s['cim'], 'osz': s['elofordulas_osz'], 'usz': s['elofordulas_usz'],
                      'kapcs': s['kapcsolatok_db'], 'szo': s['terjedelem_szo'], 'kotet': s['kotet_olvasoi']})
for e in ny['heti_tortenes']:
    tort.append({'kulcs': '%s|%s|%s' % (e['datum'], e['motivum'], e['olvasoi_esemeny']), 'datum': e['datum'],
                 'motivum': e['motivum'], 'esemeny': e['olvasoi_esemeny']})
for m in be['motivumok']:
    for k in m['kriteriumok']:
        belso.append({'kulcs': '%s|%d' % (m['id'], k['sorszam']), 'motivum': m['id'], 'kapu': k['nev'],
                      'allapot': k['allapot'], 'ertek': k['ertek'], 'reszlet': '; '.join(k['reszlet'])[:300],
                      'prov': k['proveniencia']})
for nev, rows in (('motivumok', mot), ('kapuk', kapuk), ('stash', stash), ('tortenes', tort), ('belso_kapuk', belso)):
    json.dump(rows, open(os.path.join(out, nev + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(nev, len(rows))
