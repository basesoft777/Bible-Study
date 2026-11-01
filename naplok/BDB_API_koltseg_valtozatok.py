#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F38 / 13. adag: hálózat nélküli költségvetítés két változatra, az 1. csomag mért értékeiből.

(A) cache nélkül, kérésenként 1 Strong; (B) cache nélkül, kérésenként több Strong (legfeljebb ~8000 forráskarakter), a kimenet
Strong-határon bontva. A prompt tartalma nem változik: a B-ben a közös szabály-rész egyszer, a Strongonkénti rész (kötelező-alak
lista, adatblokk, forrás) Strongonként áll. Mért: forditas/bdb_api/adag13/futasnaplo.tsv. Proveniencia: manual (becslés).
"""
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'eszkozok'))
import bdb_api_koteg as B  # noqa: E402

AR_BE, AR_KI = 1.00, 5.00
HATAR = 8000


def reszek(k):
    p = k['prompt']
    a = p.index('Adatblokk:')
    f = p.index('Forrás (Thayer, angol):')
    kot_i = p.index(B.KOT_JEL) + len(B.KOT_JEL)
    kot_v = p.rfind(B.BEMENET_JEL)
    egyedi = len(p[kot_i:kot_v]) * 0 + len(k['kot']) + (len(p[a:f]) + len(p[f:p.index('## Kimenet')]))
    return len(p), egyedi


ker = B.terv(13)
mert = [r for r in B.AK.tsv_olvas(B.ut('futasnaplo.tsv'))] if False else None
B.MUNKA = os.path.join(B.MUNKA_GYOKER, 'adag13')
naplo = B.AK.tsv_olvas(B.ut('futasnaplo.tsv'))
naplo = [r for r in naplo if r['custom_id'].endswith('-p1')]
cid = {r['custom_id']: r for r in naplo}
mert_ker = [k for k in ker if B.custom_id(k['strong'], k['csoport'], 1) in cid]
be_tok = sum(int(r['bemenet_token']) + int(r['cache_olvasas']) + int(r['cache_iras']) for r in naplo)
ki_tok = sum(int(r['kimenet_token']) for r in naplo)
kar_prompt = sum(len(k['prompt']) for k in mert_ker)
kar_forras = sum(k['forras_kar'] for k in mert_ker)
tok_kar = be_tok / kar_prompt
print('mért (%d kérés): bemenet %d token (%.3f token/prompt-karakter), kimenet %d token (%.0f/kérés, %.3f token/forráskarakter)' % (
    len(naplo), be_tok, tok_kar, ki_tok, ki_tok / len(naplo), ki_tok / kar_forras))
n = len(ker)
tot_prompt = sum(len(k['prompt']) for k in ker)
tot_forras = sum(k['forras_kar'] for k in ker)
a_be = tot_prompt * tok_kar
a_ki_kerelem = n * ki_tok / len(naplo)
a_ki_kar = tot_forras * ki_tok / kar_forras
a_lo = (a_be * AR_BE + a_ki_kar * AR_KI) / 1e6
a_hi = (a_be * AR_BE + a_ki_kerelem * AR_KI) / 1e6
print('(A) %d kérés; bemenet %.1f M token; kimenet %.2f–%.2f M token; USD/adag %.1f–%.1f' % (
    n, a_be / 1e6, a_ki_kar / 1e6, a_ki_kerelem / 1e6, a_lo, a_hi))
# B: a Strongok az adag sorrendjében, ~8000 forráskarakterig
sorrend = {s: i for i, s in enumerate(B.adag_strongok(13))}
rend = sorted(ker, key=lambda k: (sorrend.get(k['strong'], 0), k['csoport']))
csop, cur, cur_kar = [], [], 0
for k in rend:
    if cur and cur_kar + k['forras_kar'] > HATAR:
        csop.append(cur)
        cur, cur_kar = [], 0
    cur.append(k)
    cur_kar += k['forras_kar']
if cur:
    csop.append(cur)
kozos = sum(len(k['prompt']) - reszek(k)[1] for k in ker) / n     # a közös szabály-rész átlaga (karakter)
egyedi = sum(reszek(k)[1] for k in ker)
b_prompt = len(csop) * kozos + egyedi
b_be = b_prompt * tok_kar
b_lo = (b_be * AR_BE + a_ki_kar * AR_KI) / 1e6
b_hi = (b_be * AR_BE + (a_ki_kar + len(csop) * (a_ki_kerelem / n)) * AR_KI) / 1e6
print('(B) %d kérés (átlag %.1f Strong, %.0f forráskarakter); közös rész %.0f karakter, Strongonkénti rész átlag %.0f karakter; '
      'bemenet %.1f M token; USD/adag %.1f–%.1f' % (len(csop), n / len(csop), tot_forras / len(csop), kozos, egyedi / n,
                                                  b_be / 1e6, b_lo, b_hi))
sor = [l.rstrip('\n').split('\t') for l in open(B.SORREND, encoding='utf-8') if not l.startswith('#')][1:]
a14 = [r for r in sor if r[4] == '14']
a13 = [r for r in sor if r[4] == '13']
arany_db = len(a14) / len(a13)
arany_kar = sum(int(r[3]) for r in a14) / sum(int(r[3]) for r in a13)
print('hátralék a 13. adag után: a 14. adag, %d szócikk, %d forráskarakter (a 13.-nak %.1f%%-a szócikkben, %.1f%%-a karakterben)' % (
    len(a14), sum(int(r[3]) for r in a14), 100 * arany_db, 100 * arany_kar))
print('  A: %.1f–%.1f USD, B: %.1f–%.1f USD (a kérésszámmal arányosítva; a B közös-rész többlete a kis adagnál arányosan nagyobb)' % (
    arany_db * min(a_lo, a_hi), arany_db * max(a_lo, a_hi), arany_db * min(b_lo, b_hi), arany_db * max(b_lo, b_hi)))
print('13. + 14. adag összesen: A %.0f–%.0f USD, B %.0f–%.0f USD' % (
    (1 + arany_db) * min(a_lo, a_hi), (1 + arany_db) * max(a_lo, a_hi), (1 + arany_db) * min(b_lo, b_hi), (1 + arany_db) * max(b_lo, b_hi)))
