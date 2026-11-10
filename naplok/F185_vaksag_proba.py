"""F185 seed-103 vakság-próba: a kiírt szócikkszöveg minden bekezdése (a ⟦azon⟧ jelölők nélkül) egy-egy nyers forrásbekezdés
(`F185_minta103.nyers_bekezdesek`), sorrendben; és megszámolja, hány szócikkben vágna vagy döntene a gépi szerkezet (a 2.30
sorai több mint a nyers bekezdések, vagy van `belso_fejek` — ott a gépi tagolásra épülő munkalap szivárgott volna), továbbá hogy
a munkalap (vak.tsv) nem hordoz-e gépi útvonalat, szakaszt vagy bizonyosságot.
Használat (a repó gyökeréből): python naplok/F185_vaksag_proba.py"""
import collections
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import F185_minta103 as M  # noqa: E402

szov = open(M.KI + 'szocikkek.txt', encoding='utf-8').read()
dbdb = {}
for it in json.load(open(M.bont.JSON_UT, encoding='utf-8')):
    m = re.match(r'^H(\d+)', it.get('top', ''))
    if m:
        dbdb['H%04d' % int(m.group(1)) + it['top'][len(m.group(0)):]] = it['def']
tabla = collections.defaultdict(list)
for r in M.olvas(os.path.join(M.R, 'adat', 'bdb_szakaszok.tsv')):
    tabla[r['strong']].append(r)
jo = rossz = vagott = 0
for blokk in szov.split('=== ')[1:]:
    st, tor = blokk.split(' ===\n', 1)
    bek = [re.sub(r'⟦[A-Z]\d{3}⟧ ', '', b) for b in tor.strip().split('\n\n') if not b.startswith('[… a szócikk')]
    nyers = M.nyers_bekezdesek(dbdb.get(st, ''))
    if bek == nyers[:len(bek)]:
        jo += 1
    else:
        rossz += 1
        print('ELTÉR:', st)
    if len(tabla[st]) - 1 > len(nyers) or any(r.get('belso_fejek') for r in tabla[st]):
        vagott += 1
fej = open(M.KI + 'vak.tsv', encoding='utf-8').read().split('\n')[1].split('\t')
tilos = [m for m in fej if m in ('utvonal', 'szakasz', 'bizonyossag', 'okkod', 'mt_vers', 'karoli_vers')]
print('szócikk: %d egyezik a nyers bekezdésekkel, %d eltér; gépileg vágott vagy sorbelső fejes szócikk (ott szivárgott volna): %d; '
      'a vak lap gépi oszlopa: %s' % (jo, rossz, vagott, tilos or 'nincs'))
