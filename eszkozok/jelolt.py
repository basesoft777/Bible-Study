#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jelolt.py -- F8.6: A3b jelolt-generalas meglevo motivumokhoz
(F8_BRIEF.md G6).

Bemenet: egy igeszakasz (`--szakasz`). A TAHOT/TAGNT ebbol a szakasz minden
Strongjat adja, a grammatikai Strongok kiszurve (`lekerdez.load_grammatikai_
strongok`); ezt metszi az `elofordulasok.strong` mezovel (osszetett ertekek,
pl. `H7121+H8034`, elemeire bontva). Egy Strong tobb ID-hez is tartozhat --
ID-nkent kulon sor.

Soronkenti allapot: `mar elofordulas` (id+igehely mar az `elofordulasok`-ban),
`mar jelolt` (mar a `jeloltek`-ben), `uj jelolt` (egyik sem). A `formulaikus`
azonossagu motivumok soraihoz a `pozicionalis ellenorzes kell` jelzes jarul --
egy formula gyakori Strongja sok hamis jeloltet ad (l. F8_BRIEF.md L6), a
tenyleges pozicio (pl. igen egymas melletti szo-e) itt nem ellenorizheto.

`--ir`: csak az `uj jelolt` sorok kerulnek a `jeloltek.tsv` vegere,
`dontes=nyitva`-val. A `beepitve`/`elutasitva` erteket ez a szkript SOHA
nem irja.

CLI:
    python eszkozok/jelolt.py --szakasz "1Móz 7:1-24" [--ir] [--adat DIR] [--md FILE]

Kilepesi kod: 0 = lefutott (jeloltekkel vagy azok nelkul), 2 = hiba.
"""

import argparse
import datetime
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G
import lekerdez as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')

JELOLTEK_FEJLEC = ['id', 'igehely', 'forras_kereses', 'dontes', 'indoklas',
                    'karoli_szo', 'azonositas_modja', 'megbizhatosag', 'datum']


def szakasz_strongok(rng):
    """[(igehely, strong)] a szakaszban, TAHOT+TAGNT, grammatikai Strongok
    nelkul, duplikatum nelkul."""
    gramm = L.load_grammatikai_strongok()
    talalt = set()
    for r in L.load_tahot():
        book, ch, v = r['_parsed']
        if L.in_range(rng, book, ch, v) and r['Strong-szám'] not in gramm:
            talalt.add((r['Igehely'], r['Strong-szám']))
    for r in L.load_tagnt():
        book, ch, v = r['_parsed']
        if L.in_range(rng, book, ch, v) and r['Strong-szám'] not in gramm:
            talalt.add((r['Igehely'], r['Strong-szám']))
    return talalt


def elofordulas_strong_index(elofordulasok):
    """(elemi_strong -> {id, ...}, {(id, igehely), ...}) -- az osszetett
    Strong-ertekek ('+' -tagolt) elemeire bontva."""
    idx = {}
    letezo_parok = set()
    for sor in elofordulasok:
        letezo_parok.add((sor['id'], sor['igehely']))
        for elemi in (sor.get('strong') or '').split('+'):
            elemi = elemi.strip()
            if elemi:
                idx.setdefault(elemi, set()).add(sor['id'])
    return idx, letezo_parok


def jelolt_sorok_szamit(szakasz_spec, adat_dir):
    """[{id, igehely, strong, allapot, pozicionalis}] -- id, majd igehely
    szerint rendezve."""
    rng = L.parse_range(szakasz_spec)
    _, motivumok = G.tsv_beolvas(os.path.join(adat_dir, 'motivumok.tsv'))
    _, elofordulasok = G.tsv_beolvas(os.path.join(adat_dir, 'elofordulasok.tsv'))
    _, jeloltek = G.tsv_beolvas(os.path.join(adat_dir, 'jeloltek.tsv'))

    strong_idx, letezo_parok = elofordulas_strong_index(elofordulasok)
    jelolt_parok = {(j['id'], j['igehely']) for j in jeloltek}
    formulaikus = {m['id'] for m in motivumok if m.get('azonossag_tipusa') == 'formulaikus'}

    talalt = set()
    for igehely, strong in szakasz_strongok(rng):
        ids = strong_idx.get(strong)
        if not ids:
            continue
        for motivum_id in ids:
            talalt.add((motivum_id, igehely, strong))

    sorok = []
    for motivum_id, igehely, strong in sorted(talalt):
        kulcs = (motivum_id, igehely)
        if kulcs in letezo_parok:
            allapot = 'már előfordulás'
        elif kulcs in jelolt_parok:
            allapot = 'már jelölt'
        else:
            allapot = 'új jelölt'
        sorok.append({
            'id': motivum_id,
            'igehely': igehely,
            'strong': strong,
            'allapot': allapot,
            'pozicionalis': motivum_id in formulaikus,
        })
    return sorok


def jelentes_szoveg(szakasz_spec, sorok):
    ki = ['# jelolt.py -- A3b jelölt-generálás (F8.6)', '',
          'Szakasz: `%s`' % szakasz_spec, '',
          '| Motívum-ID | Igehely | Strong | Állapot | Megjegyzés |',
          '|---|---|---|---|---|']
    for s in sorok:
        megj = 'pozicionális ellenőrzés kell' if s['pozicionalis'] else ''
        ki.append('| %s | %s | %s | %s | %s |' % (
            s['id'], s['igehely'], s['strong'], s['allapot'], megj))
    n_uj = sum(1 for s in sorok if s['allapot'] == 'új jelölt')
    ki.append('')
    ki.append('Összesen %d sor; ebből %d "új jelölt".' % (len(sorok), n_uj))
    return '\n'.join(ki) + '\n'


def jeloltek_ir(adat_dir, szakasz_spec, sorok):
    """Csak az 'uj jelolt' sorokat irja, id+igehely kulcs-duplikacio nelkul.
    Visszaadja a ténylegesen beirt (id, igehely) parok listajat."""
    path = os.path.join(adat_dir, 'jeloltek.tsv')
    _, jeloltek_meglevo = G.tsv_beolvas(path)
    meglevo_parok = {(j['id'], j['igehely']) for j in jeloltek_meglevo}

    ma = datetime.date.today().isoformat()
    uj_sorok = []
    irt_parok = set()
    for s in sorok:
        if s['allapot'] != 'új jelölt':
            continue
        kulcs = (s['id'], s['igehely'])
        if kulcs in meglevo_parok or kulcs in irt_parok:
            continue
        irt_parok.add(kulcs)
        mezok = {
            'id': s['id'],
            'igehely': s['igehely'],
            'forras_kereses': 'jelolt.py %s' % szakasz_spec,
            'dontes': 'nyitva',
            'indoklas': 'automatikus jelölt (A3b), minősítendő',
            'karoli_szo': '',
            'azonositas_modja': '',
            'megbizhatosag': '',
            'datum': ma,
        }
        uj_sorok.append('\t'.join(mezok[m] for m in JELOLTEK_FEJLEC))

    if not uj_sorok:
        return []

    domináns, _, _ = G.sorveg_elemez(path)
    with open(path, 'rb') as f:
        nyers = f.read()
    vegzodik_sorveggel = nyers.endswith(b'\n')
    domináns_b = domináns.encode('utf-8')
    with open(path, 'ab') as f:
        if not vegzodik_sorveggel:
            f.write(domináns_b)
        f.write(domináns_b.join(s.encode('utf-8') for s in uj_sorok))
        f.write(domináns_b)
    return sorted(irt_parok)


def main():
    parser = argparse.ArgumentParser(description='F8.6 -- A3b jelölt-generálás')
    parser.add_argument('--szakasz', required=True, help='igeszakasz, pl. "1Móz 7:1-24"')
    parser.add_argument('--adat', default=ALAPERTELMEZETT_ADAT,
                         help='az adat/ könyvtár (alapértelmezés: a repó adat/-ja)')
    parser.add_argument('--ir', action='store_true',
                         help='az "új jelölt" sorok írása a jeloltek.tsv végére')
    parser.add_argument('--md', default=None, help='a jelentés Markdown fájlba is')
    args = parser.parse_args()

    try:
        sorok = jelolt_sorok_szamit(args.szakasz, args.adat)
    except Exception as exc:
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)

    szoveg = jelentes_szoveg(args.szakasz, sorok)
    print(szoveg)

    if args.md:
        with open(args.md, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('  megírva: %s' % args.md, file=sys.stderr)

    if args.ir:
        try:
            irt = jeloltek_ir(args.adat, args.szakasz, sorok)
        except Exception as exc:
            print('HIBA: %s' % exc, file=sys.stderr)
            sys.exit(2)
        print('  --ir: %d új jeloltek.tsv sor íródott.' % len(irt), file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    main()
