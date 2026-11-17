#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.B — a három vak bíráló (Opus, Gemini, GPT) összevetése a #172 mintáján.

Bemenet: f172/itelet_par.tsv (Opus, `opus` oszlop) és f172/kulso_biralo/<rov>/itelet_par.tsv
(`biralo` oszlop; előállítás: pontossag_meres.py --biralo <rov> --valasz ... --kimenet ...),
f172/keret.tsv (rétegsúlyok), a bírálók meres_eredmeny.tsv-je.

A pár ítélete bírálónként `helyes` (a gépi pár eredeti tokenje a bíráló halmazában van).
Kimenet:
  f172/kulso_biralo/egyezes.tsv   — bírálónként a rétegsúlyozott pontosság (a 95,06%-kal
      azonos módon); a 2-ből-3 többségi ítélet rétegsúlyozott pontossága; páronkénti és
      háromutas egyezés a pár-ítéleten (Cohen-kappa) és a jelölt halmazon (pontos egyezés);
      a mintán, súlyozatlanul.
  f172/kulso_biralo/elteresek.tsv — a nem egyhangú párok, bírálónként a halmazzal (sorszám,
      alak, Strong) és gépi indoklással (melyik bíráló miért nem fogadja el a párt).

Használat: python eszkozok/karoli_strong/kulso_biralo_ertekel.py
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pontossag_meres as pmr  # noqa: E402
import pontossag_minta as pm  # noqa: E402

F172 = pmr.F172
KB = os.path.join(F172, 'kulso_biralo')
BIRALOK = [('opus', 'Opus', os.path.join(F172, 'itelet_par.tsv'), 'opus'),
           ('gemini', 'Gemini', os.path.join(KB, 'gemini', 'itelet_par.tsv'), 'biralo'),
           ('gpt', 'GPT', os.path.join(KB, 'gpt', 'itelet_par.tsv'), 'biralo')]
MERES = {'opus': os.path.join(F172, 'meres_eredmeny.tsv'),
         'gemini': os.path.join(KB, 'gemini', 'meres_eredmeny.tsv'),
         'gpt': os.path.join(KB, 'gpt', 'meres_eredmeny.tsv')}
OK = {'fölös pár': 'a Károli-szót betoldásnak tartja (üres halmaz)',
      'azonos lexéma, más előfordulás': 'ugyanennek a Strong-számnak egy másik előfordulását jelöli',
      'szomszédos token': 'a szomszédos eredeti szót jelöli',
      'rossz szó a versben': 'más eredeti szót jelöl a versben'}


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')


def betolt():
    tab = {}
    for rov, _, ut, osz in BIRALOK:
        _, sorok = pm._tabla(ut)
        tab[rov] = {r['minta_id']: dict(r, halmaz=r[osz]) for r in sorok}
    kozos = set.intersection(*(set(t) for t in tab.values()))
    for rov, t in tab.items():
        if len(t) != len(kozos):
            raise SystemExit('%s: %d pár, a közös: %d' % (rov, len(t), len(kozos)))
    return tab, sorted(kozos)


def main():
    import bemenet
    _, ered = bemenet._adatok()
    tab, ids = betolt()
    _, keret = pm._tabla(os.path.join(F172, 'keret.tsv'))
    sulyok = {r['reteg']: int(r['parsor']) for r in keret if r['reteg'] in pm.RETEGEK}
    rovok = [b[0] for b in BIRALOK]
    nevek = {b[0]: b[1] for b in BIRALOK}
    H = {r: [tab[r][i]['helyes'] == '1' for i in ids] for r in rovok}
    S = {r: [tab[r][i]['halmaz'] for i in ids] for r in rovok}
    sorok = []

    def sor(*x):
        sorok.append([str(v) for v in x])

    # --- pontosság bírálónként (a bíráló saját meres_eredmeny.tsv-jéből, ugyanazzal a módszerrel)
    for r in rovok:
        _, m = pm._tabla(MERES[r])
        for x in m:
            if x['szakasz'] == 'sulyozott' or (x['szakasz'] == 'bontas' and x['cimke'].startswith('OSSZES')):
                sor('pontossag', '%s · %s' % (nevek[r], x['cimke']), x['n'], x['x'], x['p'], x['also95'],
                    x['felso95'], x['megjegyzes'])
    # --- többségi (2 a 3-ból) ítélet, rétegsúlyozva
    reteg = [tab['opus'][i]['reteg'] for i in ids]
    tobb = [sum(H[r][k] for r in rovok) >= 2 for k in range(len(ids))]
    egyh = [all(H[r][k] for r in rovok) for k in range(len(ids))]
    for cimke, v, megj in [('többségi ítélet (2/3)', tobb, 'a pár helyes, ha legalább két bíráló szerint az'),
                           ('egyhangú ítélet (3/3)', egyh, 'alsó korlát: a pár helyes, ha mindhárom szerint az')]:
        adat = {rt: (sum(x for x, g in zip(v, reteg) if g == rt), sum(g == rt for g in reteg)) for rt in pm.RETEGEK}
        for nev, ret in [('OSZ', pmr.OSZ), ('USZ', pmr.USZ), ('OSSZES', pm.RETEGEK)]:
            p, lo, hi, n = pmr.retegzett({rt: adat[rt] for rt in ret}, sulyok)
            sor('pontossag', '%s · %s' % (cimke, nev), n, sum(adat[rt][0] for rt in ret), '%.4f' % p, '%.4f' % lo,
                '%.4f' % hi, 'rétegzett becslés, normál 95%; ' + megj)
    # --- egyezés
    n = len(ids)
    for a, b in [('opus', 'gemini'), ('opus', 'gpt'), ('gemini', 'gpt')]:
        e = sum(x == y for x, y in zip(H[a], H[b]))
        lo, hi = pmr.wilson(e, n)
        sor('egyezes_itelet', '%s–%s' % (nevek[a], nevek[b]), n, e, '%.4f' % (e / n), '%.4f' % lo, '%.4f' % hi,
            'pár-ítélet (helyes/nem); Cohen-kappa=%.3f; súlyozatlan, Wilson 95%%' % kappa(H[a], H[b]))
    e3 = sum(H['opus'][k] == H['gemini'][k] == H['gpt'][k] for k in range(n))
    lo, hi = pmr.wilson(e3, n)
    sor('egyezes_itelet', 'háromutas', n, e3, '%.4f' % (e3 / n), '%.4f' % lo, '%.4f' % hi,
        'mindhárom bíráló ítélete azonos; súlyozatlan, Wilson 95%')
    for a, b in [('opus', 'gemini'), ('opus', 'gpt'), ('gemini', 'gpt')]:
        e = sum(x == y for x, y in zip(S[a], S[b]))
        lo, hi = pmr.wilson(e, n)
        sor('egyezes_halmaz', '%s–%s' % (nevek[a], nevek[b]), n, e, '%.4f' % (e / n), '%.4f' % lo, '%.4f' % hi,
            'a cél Károli-szóhoz jelölt eredeti halmaz pontosan azonos; súlyozatlan')
    e3 = sum(S['opus'][k] == S['gemini'][k] == S['gpt'][k] for k in range(n))
    lo, hi = pmr.wilson(e3, n)
    sor('egyezes_halmaz', 'háromutas', n, e3, '%.4f' % (e3 / n), '%.4f' % lo, '%.4f' % hi,
        'mindhárom halmaz azonos; súlyozatlan')
    # --- eltérések
    elt = []
    for k, i in enumerate(ids):
        if H['opus'][k] == H['gemini'][k] == H['gpt'][k]:
            continue
        r0 = tab['opus'][i]
        v = r0['vers']

        def tok(h):
            if h in ('', '-'):
                return '∅'
            return '; '.join('%s %s %s' % (e, ered[v][int(e) - 1]['alak'], ered[v][int(e) - 1]['strong'])
                             for e in h.split(','))
        igen = [nevek[r] for r in rovok if H[r][k]]
        nem = [r for r in rovok if not H[r][k]]
        ind = 'a gépi pár (%s %s %s) %s szerint helyes; ' % (r0['er_sorszam'], r0['er_szo'], r0['strong'],
                                                              ' és '.join(igen) or 'egyik bíráló')
        ind += '; '.join('%s szerint nem: %s (%s)' % (nevek[r], OK.get(tab[r][i]['hibatipus'], tab[r][i]['hibatipus']),
                                                      tok(tab[r][i]['halmaz'])) for r in nem)
        # nem egyhangú: pontosan egy bíráló áll szemben a másik kettővel
        tipus = 'Opus kisebbségben' if H['gemini'][k] == H['gpt'][k] else 'egy külső kisebbségben'
        elt.append([i, r0['reteg'], v, r0['hu_sorszam'], r0['hu_szo'], r0['er_sorszam'], r0['er_szo'], r0['strong'],
                    r0['morfema'], tok(S['opus'][k]), r0['helyes'], tok(S['gemini'][k]), tab['gemini'][i]['helyes'],
                    tok(S['gpt'][k]), tab['gpt'][i]['helyes'], '1' if tobb[k] else '0', tipus, ind])
    sor('elteres', 'nem egyhangú pár-ítélet', n, len(elt), '', '', '', 'f172/kulso_biralo/elteresek.tsv')
    for t in ('Opus kisebbségben', 'egy külső kisebbségben'):
        sor('elteres', t, len(elt), sum(x[16] == t for x in elt), '', '', '', '')

    head = pm.git_head()
    fej = '# MANUAL: scope=F175.B három vak bíráló összevetése (Opus, Gemini, GPT) | forras=%s | ts=git:%s | ' \
          'manual (determinisztikus; a bírálók modell-kimenetek, nem arany)\n' % (
              ', '.join(os.path.relpath(b[2], pm.GYOKER).replace(os.sep, '/') for b in BIRALOK), head)
    with open(os.path.join(KB, 'egyezes.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej)
        f.write('\t'.join(['szakasz', 'cimke', 'n', 'x', 'p', 'also95', 'felso95', 'megjegyzes']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    with open(os.path.join(KB, 'elteresek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej)
        f.write('\t'.join(['minta_id', 'reteg', 'vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong',
                           'morfema', 'opus', 'opus_helyes', 'gemini', 'gemini_helyes', 'gpt', 'gpt_helyes',
                           'tobbseg_helyes', 'tipus', 'indoklas']) + '\n')
        for x in elt:
            f.write('\t'.join(x) + '\n')
    for s in sorok:
        print('%-15s %-48s n=%-5s x=%-5s p=%s [%s, %s] %s' % tuple(s))


if __name__ == '__main__':
    main()
