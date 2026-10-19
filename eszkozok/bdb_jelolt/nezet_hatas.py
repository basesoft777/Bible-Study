#!/usr/bin/env python
"""A nézet-döntés (DT-F107c, 6. lépés) mérései (F107). Csak olvas; döntést nem hoz.

  --utolagos   a 247 `tsv_utolagos` Strong: a BDB_teljes_unabridged.tsv utólag javított sorai a nyers JSON-hoz képest —
               az eltérő szakaszok (difflib, szóközre bontott tokenek) száma és jellege (könyvnév-csere / szám-csere / egyéb)
  --forditas   az adat/forditasok.tsv BDB-sorai: hány `forras_hash` (= a TSV `Teljes_szocikk` SHA-1-e, emeles.py) egyezik ma,
               és hány változna, ha a TSV sora a táblából generált nézet lenne:
                 V1  nyers nézet (a sorok `jel` + `szoveg`, egy szóközzel; a `<sub>` nélkül)
                 V2  V1 + a `bdb_forras_javitas.tsv` `javitva` (pe_mem) sorai
  --olvasok    a TSV olvasói: datasetek.tsv sorai, a briefek `olvas` mezője, az eszkozok/ Python-fájljai

TSV: split('\\t'), csv modul nélkül.
"""
import argparse
import collections
import datetime
import difflib
import glob
import hashlib
import json
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import bont  # noqa: E402
import forras_osszevetes  # noqa: E402
import nezet_ellenoriz  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TSV = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
FORD = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
JAV = os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')
TSV_NEV = 'BDB_teljes_unabridged'


def ws(t):
    return re.sub(r'\s+', ' ', t).strip()


def tsv_sorok():
    with open(TSV, encoding='utf-8', newline='') as f:
        return {s.split('\t')[0]: s.split('\t')[2] for s in f.read().split('\n')[1:] if s}


def json_ujra():
    with open(bont.JSON_UT, encoding='utf-8') as f:
        ki = {}
        for item in json.load(f):
            m = re.match(r'^H(\d+)', item.get('top', ''))
            if m:
                pad = 'H%04d' % int(m.group(1)) + item['top'][len(m.group(0)):]
                ki[pad] = forras_osszevetes.strip_html_142ad625(item.get('def', ''))
    return ki


def utolagos():
    tsv, ujra = tsv_sorok(), json_ujra()
    stat, strongok, minta = collections.Counter(), 0, collections.defaultdict(list)
    for k, t in tsv.items():
        if k not in ujra or ws(t) == ws(ujra[k]):
            continue
        strongok += 1
        a, b = ws(ujra[k]).split(' '), ws(t).split(' ')
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == 'equal':
                continue
            x, y = ' '.join(a[i1:i2]), ' '.join(b[j1:j2])
            if re.fullmatch(r'[1-3]?[A-Z][a-z]+', x) and re.fullmatch(r'[1-3]?[A-Z][a-z]+', y):
                oszt = 'konyvnev' + ('_psa' if y == 'Psa' else '')
            elif re.fullmatch(r'[\d:,;.\-]+', x) and re.fullmatch(r'[\d:,;.\-]+', y):
                oszt = 'szam'
            else:
                oszt = 'egyeb'
            stat[oszt] += 1
            if len(minta[oszt]) < 4:
                minta[oszt].append('%s: «%s» → «%s»' % (k, x[:40], y[:40]))
    print('UTOLAGOS: %d Strong a TSV-ben eltér a nyers JSON-tól; eltérő szakasz: %d; %s' % (
        strongok, sum(stat.values()), dict(stat.most_common())))
    for o, l in minta.items():
        for e in l:
            print('  %s\t%s' % (o, e))


def javitott_nezet(nezet):
    """V2: a nézet szövege a pe_mem `javitva` sorok cseréjével (szónként, a táblasor szövegében)."""
    with open(JAV, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    jav = collections.defaultdict(list)
    for s in sorok[3:]:
        if s:
            d = dict(zip(fej, s.split('\t')))
            if d['allapot'] == 'javitva':
                jav[d['strong']].append(d)
    return jav


def forditas():
    tsv = tsv_sorok()
    nez = nezet_ellenoriz.nezetek()
    jav = javitott_nezet(nez)
    with open(FORD, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    bdb = [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.split('\t')[0] == 'BDB']
    strongok = sorted(set(d['strong'] for d in bdb))
    ma = collections.Counter()
    v1, v2 = collections.Counter(), collections.Counter()
    utolagos_kozt = 0
    ujra = json_ujra()
    for d in bdb:
        st = d['strong']
        t = tsv.get(st)
        if t is None:
            ma['nincs_tsv_sor'] += 1
            continue
        ma['egyezik' if hashlib.sha1(t.encode('utf-8')).hexdigest() == d['forras_hash'] else 'mar_elavult'] += 1
        n = nez.get(st)
        if n is None:
            v1['nincs_a_tablaban'] += 1
            v2['nincs_a_tablaban'] += 1
            continue
        v1['valtozatlan' if n == ws(t) else 'valtozna'] += 1
        v2['valtozatlan' if (n == ws(t) and st not in jav) else 'valtozna'] += 1
        if ws(t) != ws(ujra.get(st, t)):
            utolagos_kozt += 1
    print('FORDITAS: %d BDB-sor (%d Strong); a forras_hash ma: %s' % (len(bdb), len(strongok), dict(ma)))
    print('  V1 (nyers nézet): %s' % dict(v1))
    print('  V2 (nézet + pe_mem javitva): %s' % dict(v2))
    print('  a fordítássorok közül a TSV-ben utólag javított (tsv_utolagos) Strongé: %d' % utolagos_kozt)


def olvasok():
    with open(os.path.join(GYOKER, 'adat', 'datasetek.tsv'), encoding='utf-8') as f:
        ds = [s.split('\t') for s in f.read().split('\n') if s and not s.startswith('#') and TSV_NEV in s]
    print('OLVASOK: datasetek.tsv sor: %d (%s)' % (len(ds), ', '.join('%s/%s' % (x[0], x[3]) for x in ds)))
    briefek = []
    for p in sorted(glob.glob(os.path.join(GYOKER, 'F*_BRIEF.md'))):
        with open(p, encoding='utf-8') as f:
            for s in f.read().split('\n')[:30]:
                if s.startswith('olvas:') and TSV_NEV in s:
                    briefek.append(os.path.basename(p))
    print('  briefek olvas-mezője: %d (%s)' % (len(briefek), ', '.join(briefek)))
    kod = []
    for p in sorted(glob.glob(os.path.join(GYOKER, 'eszkozok', '**', '*.py'), recursive=True)):
        with open(p, encoding='utf-8', errors='replace') as f:
            if TSV_NEV in f.read():
                kod.append(os.path.relpath(p, GYOKER).replace('\\', '/'))
    print('  eszkozok/ Python-fájl: %d (%s)' % (len(kod), ', '.join(kod)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--utolagos', action='store_true')
    ap.add_argument('--forditas', action='store_true')
    ap.add_argument('--olvasok', action='store_true')
    a = ap.parse_args()
    if a.utolagos:
        utolagos()
    if a.forditas:
        forditas()
    if a.olvasok:
        olvasok()
    print('proveniencia: scope=F107 6. lépés (DT-F107c mérései) | forras=eszkozok/bdb_jelolt/nezet_hatas.py%s%s%s | ts=%s' % (
        ' --utolagos' if a.utolagos else '', ' --forditas' if a.forditas else '', ' --olvasok' if a.olvasok else '',
        datetime.date.today().isoformat()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
