#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.0/3 — token-mérés a bizonytalan (LLM-jelölt) maradék ~200 alakos mintáján.

A minta a `adat/karoli_modern/fedettseg_alakok.tsv` LLM-jelölt osztályaiból (igealak_ritka,
regies_gyanu, nem_elotag) jön, kisbetűs alakonként egyszer, rögzített maggal (20261024),
osztályonként arányosan rétegezve. Minden alakhoz az első Károli-vers, amelyben pontosan így áll
(a szövegkörnyezet). A kérések az Anthropic Messages API-n mennek (REST, `requests`; a kulcs a
`PARDES_API_KEY` környezeti változóból, csak a fejlécbe kerül, nem naplózódik). A tényleges
token-felhasználás a válasz `usage` mezőjéből jön; a becslés a teljes maradékra ebből vetít.

A modell válasza mérési melléktermék (modell_ellenorizetlen), nem a kiadott réteg, és nem
írja a szótárt: a `adat/karoli_modern/token_minta.tsv`-be kerül a proveniencia-sorral, hogy a
felhasználói mintaellenőrzés (.1/.2) és a szabályfejlesztés fel tudja használni.

Használat:
    python eszkozok/karoli_modern/token_minta.py --szaraz        # csak a minta és a prompt, API nélkül
    python eszkozok/karoli_modern/token_minta.py --futtat        # API-hívás (4 kérés × ~50 alak)
"""

import argparse
import datetime
import json
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
import tokenek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FEDETTSEG = os.path.join('adat', 'karoli_modern', 'fedettseg_alakok.tsv')
KAROLI = os.path.join('konkordancia', 'Karoli_1908.tsv')
KI = os.path.join('adat', 'karoli_modern', 'token_minta.tsv')
NAPLO = os.path.join('adat', 'karoli_modern', 'token_minta_hivasok.jsonl')
LLM_OSZTALY = ('igealak_ritka', 'regies_gyanu', 'nem_elotag')
MAG = 20261024
MINTA = 200
KOTEG = 50
MODELL = 'claude-sonnet-5-5'
MAX_TOKENS = 16000
BASE = 'https://api.anthropic.com'
KULCS_VALTOZO = 'PARDES_API_KEY'

UTASITAS = """A Károli-biblia 1908-as szövegének szóalakjait modernizáljuk. A modernizálás szintje: csak a helyesírás és az igealak változik; a szókincs, a szórend és az írásjelek NEM.

Szabályok:
- Helyesírás: a mai helyesírás szerint (cz → c, ékezetek, kettőzés: melylyel → mellyel, setétség → sötétség, néki → neki).
- Régies igealak → mai igealak, ugyanazzal az igével és igekötővel, ugyanazzal a személlyel és számmal:
  elbeszélt múlt (teremté → teremtette, felele → felelt, monda → mondta, mondának → mondták/mondtak, láték → láttam, lőn → lett, vevé → vette),
  határozói igenév (mondván → mondva), régies jövő (mondándok → mondok), régies felszólítás (cselekedjél → cselekedj).
  A tárgyas/alanyi ragozást a versbeli szerep szerint válaszd (van-e határozott tárgy).
- Ha az alak nem régies igealak (pl. főnév, névutó, mai alak), a modern alak az eredeti alak (helyesírási javítással, ha kell).
- Egy szóból egy szó lesz; szót nem toldasz be és nem hagysz el. Nagy kezdőbetű marad.

Minden sorban: sorszám, az alak, a szótári alak (a #94 táblából, lehet hibás), és egy vers, amelyben az alak áll.
Válaszként csak sorokat adj, tabulátorral elválasztva: sorszám<TAB>modern alak<TAB>biztos|bizonytalan<TAB>rövid indoklás (legfeljebb 8 szó).
"""


def sorok(ut):
    with open(os.path.join(ROOT, ut), encoding='utf-8') as f:
        for l in f:
            l = l.rstrip('\n')
            if l.startswith('#'):
                continue
            yield l.split('\t')


def minta_kesz():
    fej = None
    jeloltek = {}
    for m in sorok(FEDETTSEG):
        if fej is None:
            fej = m
            continue
        r = dict(zip(fej, m))
        if r['osztaly'] in LLM_OSZTALY:
            k = r['alak'].lower()
            if k not in jeloltek or int(r['gyakorisag']) > int(jeloltek[k]['gyakorisag']):
                jeloltek[k] = r
    osztalyok = {}
    for k in sorted(jeloltek):
        osztalyok.setdefault(jeloltek[k]['osztaly'], []).append(jeloltek[k])
    ossz = sum(len(v) for v in osztalyok.values())
    rnd = random.Random(MAG)
    minta = []
    for o in sorted(osztalyok):
        n = max(1, round(MINTA * len(osztalyok[o]) / ossz))
        minta.extend(rnd.sample(osztalyok[o], min(n, len(osztalyok[o]))))
    rnd.shuffle(minta)
    minta = minta[:MINTA]
    kell = set(r['alak'] for r in minta)
    pelda = {}
    with open(os.path.join(ROOT, KAROLI), encoding='utf-8') as f:
        next(f)
        for l in f:
            ig, szoveg = l.rstrip('\n').split('\t')[:2]
            for t in tokenek.tokenizal(szoveg):
                if t in kell and t not in pelda:
                    pelda[t] = (ig, szoveg)
    for r in minta:
        r['pelda_igehely'], r['pelda_vers'] = pelda[r['alak']]
    return minta, {o: len(v) for o, v in osztalyok.items()}, len(jeloltek)


def prompt(koteg, eltolas):
    t = [UTASITAS, '']
    for i, r in enumerate(koteg, eltolas + 1):
        t.append('%d\t%s\t%s\t%s: %s' % (i, r['alak'], r['szotari_alak'], r['pelda_igehely'], r['pelda_vers']))
    return '\n'.join(t)


def hivas(szoveg):
    import requests
    kulcs = os.environ.get(KULCS_VALTOZO)
    if not kulcs:
        raise SystemExit('nincs %s' % KULCS_VALTOZO)
    fej = {'x-api-key': kulcs, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}
    torzs = {'model': MODELL, 'max_tokens': MAX_TOKENS, 'thinking': {'type': 'adaptive'},
             'output_config': {'effort': 'low'}, 'messages': [{'role': 'user', 'content': szoveg}]}
    for kiserlet in range(3):
        try:
            r = requests.post(BASE + '/v1/messages', headers=fej,
                              data=json.dumps(torzs, ensure_ascii=False).encode('utf-8'), timeout=600)
        except requests.RequestException as e:
            if kiserlet == 2:
                raise SystemExit('HÁLÓZATI HIBA: %s' % type(e).__name__)
            time.sleep(5)
            continue
        if r.status_code in (429, 500, 502, 503, 529) and kiserlet < 2:
            time.sleep(10)
            continue
        if r.status_code >= 400:
            raise SystemExit('API-HIBA %d: %s' % (r.status_code, r.text[:500]))
        return r.json()


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--szaraz', action='store_true')
    g.add_argument('--futtat', action='store_true')
    a = ap.parse_args()
    minta, osztaly_db, jelolt_db = minta_kesz()
    print('LLM-jelölt kisbetűs alak: %d %s; minta: %d' % (jelolt_db, osztaly_db, len(minta)))
    kotegek = [minta[i:i + KOTEG] for i in range(0, len(minta), KOTEG)]
    if a.szaraz:
        print(prompt(kotegek[0], 0)[:3000])
        return
    valasz = {}
    hivasok = []
    for ki, k in enumerate(kotegek):
        p = prompt(k, ki * KOTEG)
        ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        j = hivas(p)
        u = j.get('usage', {})
        szoveg = ''.join(b.get('text', '') for b in j.get('content', []) if b.get('type') == 'text')
        hivasok.append({'ts': ts, 'koteg': ki + 1, 'alak_db': len(k), 'modell': j.get('model'), 'usage': u,
                        'stop_reason': j.get('stop_reason')})
        print('köteg %d: %s' % (ki + 1, json.dumps(u)))
        for l in szoveg.splitlines():
            m = l.split('\t')
            if len(m) >= 3 and m[0].strip().isdigit():
                valasz[int(m[0].strip())] = (m[1].strip(), m[2].strip(), m[3].strip() if len(m) > 3 else '')
    with open(os.path.join(ROOT, NAPLO), 'w', encoding='utf-8', newline='\n') as f:
        for h in hivasok:
            f.write(json.dumps(h, ensure_ascii=False) + '\n')
    modellek = sorted(set(h['modell'] for h in hivasok))
    ts0, ts1 = hivasok[0]['ts'], hivasok[-1]['ts']
    with open(os.path.join(ROOT, KI), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/karoli_modern/token_minta.py (F96.0/3) — kézzel nem szerkeszthető | '
                'scope=%d alakos rétegzett minta az LLM-jelölt maradékból (mag %d) | forras=%s + %s; modell: %s '
                '(API, adaptive, effort=low) | ts=%s–%s | modell-kimenet, modell_ellenorizetlen: mérési melléktermék, '
                'nem a kiadott réteg\n' % (len(minta), MAG, FEDETTSEG, KAROLI, ', '.join(modellek), ts0, ts1))
        f.write('\t'.join(['sorszam', 'alak', 'osztaly', 'reszlet', 'szotari_alak', 'regies_jegy', 'pelda_igehely',
                           'llm_modern', 'llm_biztos', 'llm_indoklas', 'ellenorzes']) + '\n')
        for i, r in enumerate(minta, 1):
            v = valasz.get(i, ('', 'nincs_valasz', ''))
            f.write('\t'.join([str(i), r['alak'], r['osztaly'], r['reszlet'], r['szotari_alak'], r['regies_jegy'],
                               r['pelda_igehely'], v[0], v[1], v[2], 'modell_ellenorizetlen']) + '\n')
    be = sum(h['usage'].get('input_tokens', 0) for h in hivasok)
    ki_ = sum(h['usage'].get('output_tokens', 0) for h in hivasok)
    print('összesen: bemenet %d, kimenet %d, összes %d token; %d alak; alakonként %.1f; válasz nélkül: %d'
          % (be, ki_, be + ki_, len(minta), (be + ki_) / len(minta), sum(1 for i in range(1, len(minta) + 1) if i not in valasz)))
    print('vetítés a teljes maradékra (%d alak): %.0f token' % (jelolt_db, (be + ki_) / len(minta) * jelolt_db))


if __name__ == '__main__':
    main()
