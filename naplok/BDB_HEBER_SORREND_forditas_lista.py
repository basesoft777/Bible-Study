#!/usr/bin/env python
"""A héber sorrend-javítás (DT-F131z) kézi listája a fordításhoz: azok a `heber_sorrend` / `javitva` kifejezések, amelyek a
Strong magyar BDB-fordításában (`adat/forditasok.tsv`, BDB, `forditas_hu`) NEM állnak betű szerint, ezért a megjelenítés
cseréje ott nem hat (a fordító átírta vagy szétszedte). Csak olvas; kimenet: naplok/BDB_HEBER_SORREND_forditas_kezi.tsv.

Futtatás: python naplok/BDB_HEBER_SORREND_forditas_lista.py [--ts 2026-11-01]
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import hashlib
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

JAV = 'adat/bdb_forras_javitas.tsv'
FORD = 'adat/forditasok.tsv'
KI = 'naplok/BDB_HEBER_SORREND_forditas_kezi.tsv'


def tsv(ut):
    sorok, fej = [], None
    with open(ut, encoding='utf-8') as f:
        for ln in f:
            if ln.startswith('#'):
                continue
            m = ln.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m)))
    return sorok


def sha12(ut):
    with open(ut, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    hu = collections.defaultdict(str)
    for r in tsv(FORD):
        if r['szotar'] == 'BDB' and r.get('mezo', 'forditas_hu') == 'forditas_hu':
            hu[r['strong']] += '\n' + r['forditas_hu']
    ossz = ben = 0
    ki = []
    latott = set()
    for r in tsv(JAV):
        if r['hiba'] != 'heber_sorrend' or r['allapot'] != 'javitva' or r['strong'] not in hu:
            continue
        kulcs = (r['strong'], r['forras_alak'])
        if kulcs in latott:
            continue
        latott.add(kulcs)
        ossz += 1
        if r['forras_alak'] in hu[r['strong']]:
            ben += 1
            continue
        ki.append([r['strong'], r['sorszam'], r['forras_alak'], r['javitott_alak'], '',
                   'scope=%s | forras=naplok/BDB_HEBER_SORREND_forditas_lista.py; %s@%s, %s@%s | ts=%s'
                   % (r['strong'], JAV, sha12(JAV), FORD, sha12(FORD), a.ts)])
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/BDB_HEBER_SORREND_forditas_lista.py --ts %s — a javitva kifejezések, amelyek a magyar '
                'fordításban nem állnak betű szerint (DT-F131z; kézi átnézésre).\n' % a.ts)
        f.write('\t'.join(['strong', 'sorszam', 'forras_alak', 'javitott_alak', 'kezi_megjegyzes', 'proveniencia']) + '\n')
        for s in ki:
            f.write('\t'.join(s) + '\n')
    print('lefordított Strong javitva kifejezése (egyedi): %d; betű szerint a magyarban: %d (%.1f%%); kézi listán: %d'
          % (ossz, ben, 100.0 * ben / max(ossz, 1), len(ki)))


if __name__ == '__main__':
    main()
