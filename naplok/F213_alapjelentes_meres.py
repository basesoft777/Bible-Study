"""F213 mérés: a szó-lap alapjelentése minden Strongon, előtte (DT-F76f: a magyar BDB-fejsor gépi tisztítása, ennek híján az
angol Strong-glossza; a görög fejben magyar alapjelentés nem volt) és utána (DT-F213a: magyar glossza → magyar BDB-fejsor a nemi
tanú javításával → angol).

Kimenet: összesítő a standard kimenetre, soronkénti TSV a megadott fájlba (strong, előtte forrás, előtte szöveg, utána forrás,
utána szöveg). Futtatás (WSL): PARDES_DB=~/pardes/pardes.db <venv>/bin/python naplok/F213_alapjelentes_meres.py <kimenet.tsv>
"""
import os
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok', 'olvaso_szerver')
sys.path.insert(0, D)
import adatbazis  # noqa: E402
import bdb_szokartya  # noqa: E402
import blokkok  # noqa: E402
import oldalak  # noqa: E402

db = os.environ.get('PARDES_DB') or os.path.expanduser('~/pardes/pardes.db')
con = adatbazis.Adatbazis(db, 'belso').kapcsolat()
kozos = oldalak.Kozos(con)
strongok = [r[0] for r in con.execute("SELECT strong FROM strong_szotar WHERE strong LIKE 'H%' OR strong LIKE 'G%' ORDER BY strong")]


def elotte(K):
    """A DT-F76f szabálya (a F213 előtti kód): a magyar BDB-fejsor `_alap_jelentes`-e a nemi tanú javítása nélkül, ennek híján az
    angol Strong-glossza; görög szónál nem volt alapjelentés-sor (a fej alcíme az angol TBESG-glossza)."""
    if K.strong[0] == 'G':
        tb = blokkok.q.tbesg(K.con, K.strong)
        return ('angol', tb[2]) if tb and tb[2] else ('nincs', '')
    b = blokkok._bdb_bontas(K)
    if b and b['hu'] and b['appar'].get('alap'):
        al = blokkok._alap_jelentes(b['appar']['alap'])
        if al and al.get('szoveg'):
            return ('bdb_csak_szofaj' if bdb_szokartya.csak_szofaj(al['szoveg']) else 'bdb'), al['szoveg']
    sz = blokkok.q.strong_szotar(K.con, K.strong)
    return ('angol', sz[3]) if sz and sz[3] else ('nincs', '')


ki = open(sys.argv[1], 'w', encoding='utf-8')
ki.write('strong\telotte_forras\telotte\tutana_forras\tutana\n')
db_e, db_u, atmenet = Counter(), Counter(), Counter()
for s in strongok:
    K = oldalak.Kontekst(con, kozos, strong=s)
    e_f, e_sz = elotte(K)
    u = blokkok.alapjelentes(K)
    u_f, u_sz = (u['forras'], u['szoveg']) if u else ('nincs', '')
    nyelv = s[0]
    db_e[(nyelv, e_f)] += 1
    db_u[(nyelv, u_f)] += 1
    atmenet[(nyelv, e_f, u_f)] += 1
    ki.write('\t'.join((s, e_f, (e_sz or '').replace('\t', ' '), u_f, (u_sz or '').replace('\t', ' '))) + '\n')
ki.close()
for nyelv, nev in (('H', 'héber'), ('G', 'görög')):
    n = sum(v for (ny, _), v in db_e.items() if ny == nyelv)
    print('== %s: %d Strong' % (nev, n))
    print('   előtte:', ', '.join('%s %d' % (f, v) for (ny, f), v in sorted(db_e.items()) if ny == nyelv))
    print('   utána: ', ', '.join('%s %d' % (f, v) for (ny, f), v in sorted(db_u.items()) if ny == nyelv))
    javul = sum(v for (ny, e, u), v in atmenet.items() if ny == nyelv and e in ('angol', 'bdb_csak_szofaj', 'nincs') and u in ('glossza', 'bdb'))
    print('   javul (angol / csak szófaj / nincs → magyar): %d' % javul)
    print('   angol marad: %d' % db_u[(nyelv, 'angol')])
    print('   átmenetek:', ', '.join('%s→%s %d' % (e, u, v) for (ny, e, u), v in sorted(atmenet.items()) if ny == nyelv))
print('proveniencia: scope=strong_szotar H+G (%d) | forras=naplok/F213_alapjelentes_meres.py, pardes.db (%s) | ts=%s' % (
    len(strongok), kozos.meta.get('epites_ts', '?'), __import__('datetime').date.today().isoformat()))
