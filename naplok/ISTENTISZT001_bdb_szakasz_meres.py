"""ISTENTISZT-001 arany lap, „teljes” menet (2026-10-29): a H7121 és a H8034 BDB-szakaszainak illesztése.

Csak olvas. A `bdb_szakasz_hu.tsv` (2.32) soraihoz melléteszi a `bdb_szakaszok.tsv` (2.30) angol szövegét, és
kiírja a kategóriát, a magyar szakasz hosszát és mindkét szöveg elejét/végét. Az `--teljes <strong> <sorszam>`
egy sor teljes angol és magyar szövegét adja. split('\t').
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


STRONGOK = ('H7121', 'H8034')
en = {(r['strong'], r['sorszam']): r for r in olvas('adat/bdb_szakaszok.tsv') if r['strong'] in STRONGOK}
hu = [r for r in olvas('adat/bdb_szakasz_hu.tsv') if r['strong'] in STRONGOK]

if len(sys.argv) == 4 and sys.argv[1] == '--teljes':
    k = (sys.argv[2], sys.argv[3])
    print('EN:', en[k]['jel'], en[k]['szoveg'])
    print('HU:', next(r['szoveg_hu'] for r in hu if (r['strong'], r['sorszam']) == k))
    raise SystemExit

for r in hu:
    e = en.get((r['strong'], r['sorszam']), {})
    sz = r['szoveg_hu']
    print(f"{r['strong']} {r['sorszam']:>2} {r['utvonal']:<12} {r['kategoria']:<13} jel={r['jel']!r:<8} "
          f"en={len(e.get('szoveg', '')):>5} hu={len(sz):>5}")
    print('     EN:', e.get('szoveg', '')[:110])
    if sz:
        print('     HU:', sz[:110], '…' if len(sz) > 110 else '')
