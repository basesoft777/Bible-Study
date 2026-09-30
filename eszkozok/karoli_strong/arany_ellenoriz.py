#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P1 — az Opus-aranyminta (f21p/arany_opus.jsonl) gépi ellenőrzése.

Ellenőrzi:
  * a fájl pontosan a f21p/opus_arany_kivalasztas.tsv 60 versét tartalmazza,
    ugyanabban a sorrendben, versenként egy JSON-objektummal soronként;
  * minden vers átmegy a kapun (kapu.vers_ellenoriz, mind az öt pont);
  * a prompt_v1 5. szabálya: `[nem TR]` jelölésű eredeti szó nem áll a
    `parok` jobb oldalán (mindig `forditatlan`).

Tájékoztató (nem hiba, a kézi átnézéshez): a párosított önálló magyar névelők
(a, az) és a párosított héber névelők (H9009) listája — a prompt szerint ezek
csak névmási (vonatkozó) használatban párosulnak.

Kilépési kód 1, ha bármelyik ellenőrzés elbukik. Futtatás a repó gyökeréből:
    python eszkozok/karoli_strong/arany_ellenoriz.py
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import kapu  # noqa: E402
import tokenek  # noqa: E402

ARANY = os.path.join(tokenek.ROOT, 'f21p', 'arany_opus.jsonl')
KIVALASZTAS = os.path.join(tokenek.ROOT, 'f21p', 'opus_arany_kivalasztas.tsv')


def main():
    hibak = []
    vart = [r[1] for r in tokenek._sorok(KIVALASZTAS)]
    reteg = {r[1]: r[5] for r in tokenek._sorok(KIVALASZTAS)}
    with open(ARANY, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip()]
    objektumok = []
    for i, s in enumerate(sorok, 1):
        try:
            objektumok.append(json.loads(s))
        except ValueError as e:
            hibak.append('%d. sor: nem érvényes JSON: %s' % (i, e))
    kapott = [o.get('vers') for o in objektumok if isinstance(o, dict)]
    if kapott != vart:
        hibak.append('a versek listája/sorrendje eltér a kiválasztástól (%d vs %d)' % (len(kapott), len(vart)))
    ok = 0
    linkek = 0
    tajekoztato = []
    for o in objektumok:
        ig = o.get('vers')
        if ig not in reteg:
            continue
        adat = bemenet.vers_adat(ig)
        h = kapu.vers_ellenoriz(o, adat)
        if h:
            hibak.extend('%s: %s' % (ig, x) for x in h)
            continue
        ok += 1
        toks = adat['karoli_tokenek']
        ered = adat['eredeti']
        for m, es in o['parok']:
            linkek += len(es)
            for e in es:
                w = ered[e - 1]
                if w['nem_tr']:
                    hibak.append('%s: [nem TR] eredeti szó párosítva: %d (magyar %d)' % (ig, e, m))
                if w['strong'] == 'H9009':
                    tajekoztato.append('%s: H9009 párosítva: eredeti %d -> magyar %d %s' % (ig, e, m, toks[m - 1]))
            if toks[m - 1].lower() in ('a', 'az'):
                tajekoztato.append('%s: névelő-alak párosítva: magyar %d %s -> %s' % (ig, m, toks[m - 1], es))
    print('versek: %d, kapun átment: %d, linkek (magyar-eredeti párok): %d' % (len(objektumok), ok, linkek))
    csop = {}
    for ig in kapott:
        csop[reteg.get(ig)] = csop.get(reteg.get(ig), 0) + 1
    print('rétegcsoportok: %s' % ', '.join('%s=%d' % kv for kv in sorted(csop.items())))
    print('tájékoztató (névmási névelő-párosítások, kézi átnézésre): %d' % len(tajekoztato))
    for t in tajekoztato:
        print('  ' + t)
    if hibak:
        print('HIBA:')
        for x in hibak:
            print('  ' + x)
        sys.exit(1)
    print('rendben')


if __name__ == '__main__':
    main()
