#!/usr/bin/env python
"""F145 ⛔(ii) mérés: a 16. kapu ragozás-tűrése (thayer_kapuk._re_cel) hamis pozitívot ad-e.

  python naplok/F145_ragozas_audit.py --gyoker <fa>

Minden besorolt sigla-sorra, amelynek cél-alakja toldalékot kap (legalább 4 betű, nem könyvrövidítés, betű/szám végű), kigyűjti a
`forditasok.tsv` minden (nem `elavult`) `forditas_hu` szövegéből (Thayer és BDB) azokat a szavakat, amelyek az új szabállyal
találatok, a régivel (szóvégi határ) nem — a hamis pozitív gyanú: a cél-alak más szó eleje.
TSV: split('\\t'), csv modul nélkül.
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ap = argparse.ArgumentParser()
ap.add_argument('--gyoker', required=True)
a = ap.parse_args()
gy = os.path.abspath(a.gyoker)
sys.path.insert(0, os.path.join(gy, 'eszkozok', 'thayer_jelolt'))
sys.path.insert(0, os.path.join(gy, 'eszkozok'))
import thayer_kapuk as TK  # noqa: E402

sigla = TK.sigla_betolt(os.path.join(gy, 'adat', 'thayer_sigla.tsv'))
with open(os.path.join(gy, 'adat', 'forditasok.tsv'), encoding='utf-8', newline='') as f:
    sorok = [s.rstrip('\r').split('\t') for s in f.read().split('\n') if s and not s.startswith('#')]
fej = sorok[0]
szovegek = [dict(zip(fej, s)) for s in sorok[1:]]
szovegek = [r['forditas_hu'] for r in szovegek if r['allapot'] != 'elavult' and r['mezo'] == 'forditas_hu']
print('szöveg: %d sor, %d karakter' % (len(szovegek), sum(map(len, szovegek))))
for r in sigla:
    if r['allapot'] != 'besorolt' or r['magyar_alak'] in ('', TK.NINCS_EGYSEGES):
        continue
    cel = r['forrasalak'] if r['magyar_alak'] == TK.VALTOZATLAN else r['magyar_alak']
    if len(cel) < TK.TOLDALEK_MIN or r['tipus'] == TK.KONYVROV or not cel[-1].isalnum():
        continue
    uj = re.compile(r'(?<![\w])' + re.escape(cel) + r'(\w*)')
    szavak = collections.Counter()
    for t in szovegek:
        for m in uj.finditer(t):
            if m.group(1):
                szavak[cel + m.group(1)] += 1
    print('%s -> %s (%s): %d különböző toldalékos alak, %d előfordulás%s' % (
        r['forrasalak'], cel, r['tipus'], len(szavak), sum(szavak.values()),
        ': ' + ', '.join('%s×%d' % kv for kv in szavak.most_common(12)) if szavak else ''))
