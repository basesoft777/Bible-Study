"""Frissességi teszt a célgépen (#76 K4, M0 3.8): a telepített pardes.db épségét és a manifesttel való egyezését igazolja.

Három lépés:
  1. a `meta` tábla `hash:<tábla>` sorai (építéskori sorszám|sha256) egyeznek a tábla mai, újraszámolt tartalmával
     (ugyanaz a hash, mint az eszkozok/sqlite_epit.py `tablak_hash`-e: rendezett tartalom, `\\t`-bal és `\\n`-nel);
  2. ha van manifest (`--manifest`), a `meta` hash-sorai egyeznek a manifest soraival (a manifestet az építés gépén
     készíti a `--manifest-keszit`; a TSV-k frissességét ott a `eszkozok/olvaso_pilot/db_meres.py` D5 ellenőrzi);
  3. kiírja az építés időpontját (`meta.epites_ts`) és a kiadás szempontjából fontos tábláinak hiányát.

Kilépési kód: 0 = friss és ép, 1 = eltérés (a telepítés megáll).
Használat:
  python frissesseg.py --db pardes.db [--manifest manifest.tsv] [--csak-meta]
  python frissesseg.py --db pardes.db --manifest-keszit manifest.tsv
A TSV-k olvasása/írása `split('\\t')` / `'\\t'.join()` (a `csv` modul nem használható ezeken a táblákon).
"""
import argparse
import hashlib
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def nyit(db):
    return sqlite3.connect('file:%s?mode=ro' % db, uri=True)


def meta_hashek(con):
    ki = {}
    for k, v in con.execute("SELECT kulcs, ertek FROM meta WHERE kulcs LIKE 'hash:%'"):
        db, h = v.split('|')
        ki[k[5:]] = (int(db), h)
    return ki


def tablak_hash(con):
    """{tabla: (sorszam, sha256)} -- azonos az sqlite_epit.tablak_hash-sel."""
    nevek = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
        "AND name NOT LIKE 'fts_motivum_%' AND name != 'meta' ORDER BY name")]
    ki = {}
    for n in nevek:
        oszlopszam = len(con.execute('PRAGMA table_info("%s")' % n).fetchall())
        order = ','.join(str(i + 1) for i in range(oszlopszam))
        h = hashlib.sha256()
        db = 0
        for row in con.execute('SELECT * FROM "%s" ORDER BY %s' % (n, order)):
            h.update(('\t'.join('' if v is None else str(v) for v in row) + '\n').encode('utf-8'))
            db += 1
        ki[n] = (db, h.hexdigest())
    return ki


def manifest_olvas(ut):
    ki = {}
    for l in open(ut, encoding='utf-8').read().split('\n'):
        if not l or l.startswith('#') or l.startswith('tabla\t'):
            continue
        t, db, h = l.split('\t')
        ki[t] = (int(db), h)
    return ki


def main():
    ap = argparse.ArgumentParser(description='pardes.db frissességi teszt (#76 K4)')
    ap.add_argument('--db', required=True)
    ap.add_argument('--manifest')
    ap.add_argument('--manifest-keszit', dest='keszit')
    ap.add_argument('--csak-meta', action='store_true', help='nem számolja újra a táblák hash-ét (gyors; csak a manifest-egyezés)')
    a = ap.parse_args()
    con = nyit(a.db)
    meta = meta_hashek(con)
    ts = con.execute("SELECT ertek FROM meta WHERE kulcs='epites_ts'").fetchone()
    print('epites_ts:', ts[0] if ts else '(nincs)', '| meta hash-sorok:', len(meta))
    if a.keszit:
        with open(a.keszit, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# manifest a pardes.db meta hash-soraiból (epites_ts=%s)\ntabla\tsor\tsha256\n' % (ts[0] if ts else ''))
            for t in sorted(meta):
                f.write('%s\t%d\t%s\n' % (t, meta[t][0], meta[t][1]))
        print('manifest kiírva:', a.keszit, '(%d tábla)' % len(meta))
        return 0
    hiba = []
    if not a.csak_meta:
        mai = tablak_hash(con)
        for t in sorted(set(meta) | set(mai)):
            if meta.get(t) != mai.get(t):
                hiba.append('tábla-hash eltér: %s (meta %s, mai %s)' % (t, meta.get(t), mai.get(t)))
        print('újraszámolt táblák:', len(mai), '| eltérés a meta-tól:', len([h for h in hiba if h.startswith('tábla-hash')]))
    if a.manifest:
        man = manifest_olvas(a.manifest)
        for t in sorted(set(man) | set(meta)):
            if man.get(t) != meta.get(t):
                hiba.append('manifest eltér: %s (manifest %s, meta %s)' % (t, man.get(t), meta.get(t)))
        print('manifest sorai:', len(man), '| eltérés a meta-tól:', len([h for h in hiba if h.startswith('manifest')]))
    for h in hiba[:30]:
        print('HIBA:', h)
    print('EREDMÉNY:', 'FRISS ÉS ÉP' if not hiba else 'ELTÉRÉS (%d)' % len(hiba))
    return 0 if not hiba else 1


if __name__ == '__main__':
    sys.exit(main())
