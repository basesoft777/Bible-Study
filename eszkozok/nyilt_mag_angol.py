#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nyilt_mag_angol.py -- a nyílt mag szabad szövegének angol párja: kötegelés, betöltés, állapot (F170.3–4, FELADATOK #170).

A fordítást gép (Sonnet-subagent) végzi; ez a szkript nem hív modellt. A forrás a *generált* magyar cellaszöveg
(`nyilt_mag_export.SZABAD` oszlopai), a tár a `adat/nyilt_angol.tsv` (forrásréteg; az export csak olvassa). Kulcs:
tábla + oszlop + sorkulcs; a sorhoz a magyar szöveg hash-e (`forras_hash`) tartozik. Ha a magyar cella változik, a
hash eltér: a fordítás elavult, az export nem veszi be, a kapu bukik — újrafordítandó.

Alparancsok:
    allapot                         a cellák száma: fordított / hiányzó / elavult
    kigyujt --ki DIR [--koteg 40]   a fordítandó (hiányzó vagy elavult) szövegek kötegekbe, egyedi szövegenként
                                    (DIR/koteg_NN.json: [{"id": hash, "mezo": "tábla/oszlop", "hu": szöveg}])
    betolt --be FÁJL --modell NÉV   a fordított köteg ([{"id": hash, "en": szöveg}]) betöltése minden olyan cellára,
                                    amelynek a magyar szövege ez; a `modell` a fordító saját, kiírt modellneve

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (CLAUDE.md); írás előtt ellenőrzi, hogy a meglévő kulcsok egyike sem
vész el (a tartalmat a `betolt` csak az új vagy elavult kulcson, ill. `--felulir`-ral cseréli).
"""
import argparse
import datetime
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nyilt_mag_export as E  # noqa: E402

FEJLEC = ('# A nyílt mag szabad szövegének gépi angol fordítása (F170, FELADATOK #170). Forrásréteg: a fordítás itt '
          'él, a nyilt_mag/ export csak kiolvassa. Kulcs: tabla + oszlop + sorkulcs; forras_hash = a magyar cellaszöveg '
          'SHA-256-jának első 16 jegye. Írja: eszkozok/nyilt_mag_angol.py betolt. Séma: adat/SEMA.md 2.50')
UT = os.path.join(E.GYOKER, E.ANGOL_TABLA)


def tar_olvas():
    if not os.path.exists(UT):
        return []
    with open(UT, encoding='utf-8') as f:
        sorok = [s.rstrip('\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    if fej != E.ANGOL_FEJ:
        raise SystemExit('a tár fejléce nem a várt: %s' % fej)
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def tar_ir(sorok, regi):
    """A meglévő (nem cserélt) sorok változatlanok maradnak; rendezve írunk."""
    uj_kulcs = {(s['tabla'], s['oszlop'], s['sorkulcs']) for s in sorok}
    for r in regi:
        k = (r['tabla'], r['oszlop'], r['sorkulcs'])
        if k not in uj_kulcs:
            raise SystemExit('a tár egy sora elveszne: %s' % (k,))
    sorok = sorted(sorok, key=lambda s: (s['tabla'], s['oszlop'], s['sorkulcs']))
    ki = [FEJLEC, '\t'.join(E.ANGOL_FEJ)]
    for s in sorok:
        for k in E.ANGOL_FEJ:
            if '\t' in s[k] or '\n' in s[k]:
                raise SystemExit('tab/újsor a mezőben: %s' % s[k][:60])
        ki.append('\t'.join(s[k] for k in E.ANGOL_FEJ))
    with open(UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')


def cellak():
    fajlok, _ = E.export('nyilt_mag')
    return E.szabad_cellak(fajlok)


def osztalyoz(cs, tar):
    t = {(s['tabla'], s['oszlop'], s['sorkulcs']): s for s in tar}
    ok, hiany, elavult = [], [], []
    for c in cs:
        s = t.get(c[:3])
        if s is None:
            hiany.append(c)
        elif s['forras_hash'] != E.szoveg_hash(c[3]):
            elavult.append(c)
        else:
            ok.append(c)
    return ok, hiany, elavult


def allapot(_a):
    cs = cellak()
    ok, hiany, elavult = osztalyoz(cs, tar_olvas())
    print('szabad szöveges cella: %d; fordított: %d; hiányzó: %d; elavult: %d' % (len(cs), len(ok), len(hiany),
                                                                                  len(elavult)))
    print('egyedi fordítandó szöveg: %d' % len({E.szoveg_hash(c[3]) for c in hiany + elavult}))
    return 0


def kigyujt(a):
    cs = cellak()
    _, hiany, elavult = osztalyoz(cs, tar_olvas())
    egyedi = {}
    for c in hiany + elavult:
        egyedi.setdefault(E.szoveg_hash(c[3]), {'id': E.szoveg_hash(c[3]), 'mezo': '%s/%s' % (c[0], c[1]), 'hu': c[3]})
    tetel = sorted(egyedi.values(), key=lambda x: (x['mezo'], x['id']))
    os.makedirs(a.ki, exist_ok=True)
    n = 0
    for i in range(0, len(tetel), a.koteg):
        n += 1
        with open(os.path.join(a.ki, 'koteg_%02d.json' % n), 'w', encoding='utf-8') as f:
            json.dump(tetel[i:i + a.koteg], f, ensure_ascii=False, indent=1)
    print('%d egyedi szöveg, %d köteg: %s' % (len(tetel), n, a.ki))
    return 0


def betolt(a):
    with open(a.be, encoding='utf-8') as f:
        forditas = json.load(f)
    en = {}
    for x in forditas:
        t = ' '.join((x.get('en') or '').split())
        if not t:
            raise SystemExit('üres fordítás: %s' % x.get('id'))
        en[x['id']] = t
    tar = tar_olvas()
    regi = [dict(s) for s in tar]
    t = {(s['tabla'], s['oszlop'], s['sorkulcs']): s for s in tar}
    datum = a.datum or datetime.date.today().isoformat()
    talalt, db = set(), 0
    for c in cellak():
        h = E.szoveg_hash(c[3])
        if h not in en:
            continue
        talalt.add(h)
        s = t.get(c[:3])
        if s and s['forras_hash'] == h and not a.felulir:
            continue
        uj = {'tabla': c[0], 'oszlop': c[1], 'sorkulcs': c[2], 'forras_hash': h, 'forras_hu': c[3], 'angol': en[h],
              'modell': a.modell, 'datum': datum}
        t[c[:3]] = uj
        db += 1
    nincs = sorted(set(en) - talalt)
    if nincs:
        raise SystemExit('a kötegben olyan azonosító, amely egyetlen mai cellához sem tartozik: %s' % nincs[:5])
    tar_ir(list(t.values()), regi)
    print('betöltve: %d cella (%d egyedi szöveg), modell: %s' % (db, len(en), a.modell))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    al = ap.add_subparsers(dest='cmd', required=True)
    al.add_parser('allapot')
    k = al.add_parser('kigyujt')
    k.add_argument('--ki', required=True)
    k.add_argument('--koteg', type=int, default=40)
    b = al.add_parser('betolt')
    b.add_argument('--be', required=True)
    b.add_argument('--modell', required=True)
    b.add_argument('--datum')
    b.add_argument('--felulir', action='store_true', help='az egyező hash-ű meglévő fordítás felülírása (javítás)')
    a = ap.parse_args()
    return {'allapot': allapot, 'kigyujt': kigyujt, 'betolt': betolt}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
