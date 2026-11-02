#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F07 A1 — az első körös bukások mérése (az orkesztrátor kérése, 2026-11-02; DT-F07i/j bizonyíték).

    python naplok/THAYER_ELES_A1.py idezojel   # 8_idezojel: tiszta csere / többlet / hiány; a forrás aposztrófos idézetei
    python naplok/THAYER_ELES_A1.py hibak      # a 9_tagolas, 4_formazas, ... kapuhibák Strongonként

Bemenet (csak olvas): forditas/thayer_api/adag701/kapu_eredmeny_1_kor.jsonl (az 1. kör kapuzása, a javított kapuk előtt),
kapu_eredmeny_2_kor.jsonl (a javító kör után, a javított kapuk előtt). Proveniencia: scope=adag701 | forras=ez a szkript | ts=2026-11-02
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import thayer_api_koteg as T  # noqa: E402
import forditas_kapuk as K  # noqa: E402

D = os.path.join(ROOT, 'forditas', 'thayer_api', 'adag701')
EGY = re.compile(r"(?<![\w])'([^']{1,400}?)'(?![\w])")


def sorok(fn):
    return [json.loads(l) for l in open(os.path.join(D, fn), encoding='utf-8') if l.strip()]


def idezojel():
    ossz = tiszta = 0
    for r in sorok('kapu_eredmeny_1_kor.jsonl'):
        for h in r['hibak']:
            if not h.startswith('8_idezojel'):
                continue
            m = re.search(r'forras (\d+) par, forditas (\d+) par', h)
            a, b = int(m.group(1)), int(m.group(2))
            ne = len(EGY.findall(T.TB.nezet(T.TB.szakaszok(r['strong']))))
            t = b > a and b - a == ne
            ossz += 1
            tiszta += t
            print(r['strong'], 'forrás', a, 'fordítás', b, 'aposztrófos idézet', ne,
                  'TISZTA CSERE' if t else ('TÖBBLET' if b - a > ne else 'HIÁNY'))
    print('8_idezojel-bukás %d; ebből tiszta csere %d' % (ossz, tiszta))
    # az 1. kör végleges (beírt) fordításaiban: aposztrófos idézet marad-e (a kapu csak az ASCII-párokat számolja)
    marad = 0
    for r in sorok('kapu_eredmeny_2_kor.jsonl'):
        if r['allapot'] != 'kesz':
            continue
        src = T.TB.nezet(T.TB.szakaszok(r['strong']))
        if EGY.findall(src) and K.idezojel_parok_forditas(r['vegleges']) == K.idezojel_parok_forras(src):
            marad += 1
    print('kész Strong, amelynek forrása aposztrófos idézetet tartalmaz, és a kapun aposztróf-megtartással átment: %d' % marad)


def hibak():
    for r in sorok('kapu_eredmeny_1_kor.jsonl'):
        for h in r['hibak']:
            print(r['strong'], '|', h[:300])


if __name__ == '__main__':
    {'idezojel': idezojel, 'hibak': hibak}[sys.argv[1] if len(sys.argv) > 1 else 'hibak']()
