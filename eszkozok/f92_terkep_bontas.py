#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/f92_terkep_bontas.py -- F92 (ellenor ÚJ-2, ÚJ-4): a pardes.db-ből igazolható állítások lekérdezése.

Csak olvas (mode=ro). Két igazolás:
  1. a LXX_versificacios_terkep.tsv kulcsainak bontása (a 39 NEM_MEGHATAROZHATO sor és a 179-es különbség);
  2. a görög ÚSZ-előfordulás: pardes.db `token_strong` = a TAGNT_kivonat.tsv egész Strong-mezői + a `+` láncok
     elemei, minden G-Strongra (az eltérések száma).
Futtatás: python eszkozok/f92_terkep_bontas.py [--db pardes.db]
A kimenet első sora a proveniencia-sor (CLAUDE.md 1. szabály).
"""
import argparse
import datetime
import os
import re
import sqlite3
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sorok(rel):
    fej = None
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        for s in f:
            if s.startswith('#') or not s.strip():
                continue
            m = s.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            yield m


def hnorm(s):
    m = re.match(r'^([HG])0*(\d+)([A-Z]?)$', (s or '').strip().upper())
    return '%s%04d' % (m.group(1), int(m.group(2))) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', default=os.path.join(ROOT, 'pardes.db'))
    a = ap.parse_args()
    con = sqlite3.connect('file:%s?mode=ro' % a.db.replace('\\', '/'), uri=True)
    meta = dict(con.execute('SELECT kulcs, ertek FROM meta'))
    print('scope=F92 igazolás (térkép-bontás, ÚSZ-előfordulás) | forras=pardes.db meta.epites_ts=%s meta.mod=%s + '
          'konkordancia/LXX_versificacios_terkep.tsv + konkordancia/TAGNT_kivonat.tsv | ts=%s'
          % (meta.get('epites_ts'), meta.get('mod'), datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))
    # 1. térkép
    kulcsok, nm = Counter(), 0
    for r in sorok('konkordancia/LXX_versificacios_terkep.tsv'):
        if r[0] == 'NEM_MEGHATAROZHATO':
            nm += 1
        else:
            kulcsok[r[0]] += 1
    van_os = {x for (x,) in con.execute("SELECT DISTINCT karoli_igehely FROM lxx_versszam WHERE forras='LXX_OS'")}
    van_terkep = {x for (x,) in con.execute("SELECT DISTINCT karoli_igehely FROM lxx_versszam WHERE forras='versificacios_terkep'")}
    nincs = {x for (x,) in con.execute("SELECT DISTINCT karoli_igehely FROM lxx_versszam WHERE forras='nincs'")}
    ot = van_os | van_terkep | nincs
    vers = {x for (x,) in con.execute('SELECT igehely FROM vers')}
    print('terkep: NEM_MEGHATAROZHATO sor %d (nem Károli-kulcs; a normalizalas_jelentes-ben számolva)' % nm)
    print('terkep: valódi Károli-kulcs %d' % len(kulcsok))
    print('  ebből ÓSZ-vers az lxx_versszam-ban: %d (LXX_OS-sal is: %d; csak térkép: %d)' % (
        len(set(kulcsok) & ot), len(set(kulcsok) & van_os), len(set(kulcsok) & van_terkep)))
    print('  ebből nem ÓSZ-vers az lxx_versszam-ban, de Károli-vers: %d' % len((set(kulcsok) - ot) & vers))
    print('  ebből nem Károli-vers: %d' % len(set(kulcsok) - vers))
    # 2. ÚSZ
    egesz, lanc = Counter(), Counter()
    for r in sorok('konkordancia/TAGNT_kivonat.tsv'):
        if len(r) < 2:
            continue
        n = hnorm(r[1])
        if n:
            egesz[n] += 1
        elif '+' in r[1]:
            for x in r[1].split('+'):
                h = hnorm(x)
                if h:
                    lanc[h] += 1
    ossz = rossz = 0
    for g, db in con.execute("SELECT strong, COUNT(*) FROM token_strong WHERE strong LIKE 'G%' GROUP BY strong"):
        ossz += 1
        if db != egesz[g] + lanc[g]:
            rossz += 1
    print('uszt: G-Strong a token_strong-ban %d; DB != TAGNT egész mező + láncelem: %d' % (ossz, rossz))
    print('uszt: a lekerdez.py scan és a pilot TSV-útja csak az egész mezőt számolja (G4218 példa: DB-szám = egész + láncelem)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
