"""F54 / M1 (a): az A2 osztalyu (tabla-sor nelkuli) versek felulbiralasi sorai.

Bemenet: naplok/LXX_OS_LEFEDETTSEG_osztalyozas.tsv (alosztaly = A2_tabla_nelkul).
Kimenet: konkordancia/LXX_OS/karoli_vers_felulbiralas.tsv -- a meglevo sorok utan hozzafuzi
(book_key, fejezet, vers = az LXX-vers nyers szama; igehely_karoli; indok). Idempotens.

Feltetel (DT-F54a (a)): a fejezetek mindegyikebol legalabb egy vers tartalmi ellenorzese
(M2 mintavetel, naplok/LXX_OS_LEFEDETTSEG_M2.md) -- csak az atment fejezetek kerulnek be.
"""
import sys
import os
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).replace('\\', '/') + '/'
sys.path.insert(0, R + 'eszkozok')
import lxx_os_import as L  # noqa: E402

# fejezet -> az M2 tartalmi mintavetel verseinek listaja (a naplok/LXX_OS_LEFEDETTSEG_M2.md szerint)
ATMENT = {
    '2Móz 35': '2Móz 35:1, 35:10, 35:30',
    'Dán 3': 'Dán 3:1, 3:12, 3:25',
    'Hós 2': 'Hós 2:1, 2:8, 2:20',
    'Hós 13': 'Hós 13:1, 13:7',
    'Hós 14': 'Hós 14:1, 14:6',
    'Jób 37': 'Jób 37:1, 37:5, 37:23 (37:14 laza)',
}

utvonal = R + 'konkordancia/LXX_OS/karoli_vers_felulbiralas.tsv'
meglevo = set()
sorok = open(utvonal, encoding='utf-8').read().rstrip('\n').split('\n')
for l in sorok:
    if l.startswith('#') or l.startswith('book_key'):
        continue
    p = l.split('\t')
    meglevo.add((p[0], int(p[1]), int(p[2])))

rows = [l.rstrip('\n').split('\t') for l in open(R + 'naplok/LXX_OS_LEFEDETTSEG_osztalyozas.tsv', encoding='utf-8') if not l.startswith('#')]
hd = rows[0]
rows = [dict(zip(hd, r)) for r in rows[1:]]
uj = []
for r in rows:
    if r['alosztaly'] != 'A2_tabla_nelkul':
        continue
    fej = r['igehely'].rsplit(':', 1)[0]
    if fej not in ATMENT:
        continue
    slug = L.elsodleges_slug(r['konyv'])
    book_key = L.BOOKS[slug][1]
    m = re.match(r'^.* (\d+):(\d+)$', r['javasolt_lxx'])
    kulcs = (book_key, int(m.group(1)), int(m.group(2)))
    if kulcs in meglevo:
        continue
    indok = ('A2 (F54 M1): nincs tabla-sor; fuggetlen parositas %s, fejezet-szoszamkorrelacio r=%s; '
             'tartalmi mintavetel (M2): %s; manual, ts=2026-10-11' % (r['fej_offset'], r['fej_r'], ATMENT[fej]))
    uj.append('\t'.join([book_key, str(kulcs[1]), str(kulcs[2]), r['igehely'], indok]))
if uj:
    jegyzet = '# F54 (DT-F54a (a)): az A2 sorok a naplok/LXX_OS_LEFEDETTSEG_A2_general.py hozzafuzese (nincs tabla-sor; bizonyitek az indok oszlopban)'
    if jegyzet not in sorok:
        # a fejlec (book_key ...) elé
        i = next(k for k, l in enumerate(sorok) if l.startswith('book_key'))
        sorok.insert(i, jegyzet)
    sorok.extend(uj)
    with open(utvonal, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok) + '\n')
print('uj felulbiralasi sor:', len(uj))
