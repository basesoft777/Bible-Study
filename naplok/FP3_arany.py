#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F27 M1 — az aranyminta összevetése (naplok/FP3_arany.md): forrás, kézi (`kezi`, teljes szócikk) és API-Sonnet egymás alatt.
Ítélet nélkül; csak mérhető jellemzők. A kapuhibás válasz is megjelenik (utolsó próba nyers/végleges szövege)."""
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GY = os.path.dirname(ITT)
for u in (os.path.join(GY, 'eszkozok'), os.path.join(GY, 'eszkozok', 'thayer_jelolt')):
    sys.path.insert(0, u)
import thayer_bemenet as TB  # noqa: E402

STRONGOK = ['G0282', 'G1941', 'G1944', 'G4151', 'G5590']
TOK = re.compile(r'⟪\d+⟫')
SZAM = re.compile(r'\d+[:,]\d+')


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n')]
    s = [x for x in s if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


kezi = {r['strong']: r for r in tsv(os.path.join(GY, 'adat', 'forditasok.tsv'))
        if r['szotar'] == 'Thayer' and r['allapot'] == 'kezi' and r['mezo'] == 'forditas_hu'}
api = {}
for l in open(os.path.join(GY, 'forditas', 'thayer_api', 'adag99', 'kapu_eredmeny.jsonl'), encoding='utf-8'):
    r = json.loads(l)
    api[r['strong']] = r
ki = ['# FP3 aranyminta — az 5 `kezi` Thayer-Strong szakaszos API-fordítása (F27 M1)\n',
      '*Ítélet nélküli összevetés. Forrás: javított forrásnézet (`thayer_bemenet`); `kezi`: a régi teljes szócikk-sor (`allapot=kezi`, nem szakaszos); '
      'Sonnet: a #158 kötegelő kimenete (claude-sonnet-5-5, Batch; 1. kör + legfeljebb 1 javító kör), tokenekkel. Csak a naplóba, a `forditasok.tsv`-be nem kerül. '
      'proveniencia: scope=%s | forras=forditas/thayer_api/adag99/, adat/forditasok.tsv | ts=2026-11-02*\n' % ', '.join(STRONGOK)]
for sp in STRONGOK:
    szak = TB.szakaszok(sp)
    forras = TB.nezet(szak)
    k = kezi.get(sp, {}).get('forditas_hu', '')
    r = api.get(sp, {})
    s = r.get('vegleges') or ''
    ki.append('\n## %s\n' % sp)
    ki.append('- szakasz: %d; forrás %d kar.; `kezi` %d kar.; Sonnet (token nélkül) %d kar.' % (
        len(szak), len(forras), len(k), len(TOK.sub('', s))))
    ki.append('- kapu: %s (próba: %s); hiba: %s' % (r.get('allapot', '—'), r.get('proba', '—'), '; '.join(r.get('hibak', [])) or 'nincs'))
    ki.append('- igehely-alakok (c:v) száma: forrás %d, `kezi` %d, Sonnet %d' % (
        len(SZAM.findall(forras)), len(SZAM.findall(k)), len(SZAM.findall(s))))
    ki.append('\n**Forrás** (kódblokkban: angol forrásszöveg)\n\n```\n%s\n```\n' % forras)
    ki.append('**`kezi`**\n\n%s\n' % k)
    ki.append('**Sonnet (API)**\n\n%s\n' % (s if r.get('vegleges') else '*nincs használható válasz — ' + str(r.get('hibak')) + '*'))
with open(os.path.join(ITT, 'FP3_arany.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(ki))
print('kész', os.path.getsize(os.path.join(ITT, 'FP3_arany.md')))
