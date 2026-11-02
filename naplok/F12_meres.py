"""F12 0. lépés: a brief 3. szakaszának (Kiindulás) újramérése a TEREMT-002-re.

Csak olvas; split('\t'), csv modul nélkül. Kimenet: stdout (a napló ebből készül).
Futtatás: python naplok/F12_meres.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = 'TEREMT-002'
STRONGOK = {'H8414', 'H0922'}


def tabla(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if not s.startswith('#')]
    sorok = [s for s in sorok if s]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def erint(r, *mezok):
    for m in mezok:
        v = r.get(m, '')
        if v == ID or any(s in v for s in STRONGOK):
            return True
    return False


def main():
    _, elo = tabla('adat/elofordulasok.tsv')
    sajat = [r for r in elo if r['id'] == ID]
    print('3.1 előfordulás-sorok:', len(sajat))
    for r in sajat:
        print('   ', r['igehely'], '|', r['pardes_szint'], '|', r['gerinc_elem'], '|', r['strong'])
    print('3.2 szótári mezők (kitöltött / összes):')
    for m in ('lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam', 'jelentes_en', 'jelentes_hu'):
        print('   ', m, sum(1 for r in sajat if r[m].strip()), '/', len(sajat))
    print('3.3 karoli_szo:')
    for r in sajat:
        print('   ', r['igehely'], '|', r['karoli_szo'])

    _, szak = tabla('adat/bdb_szakaszok.tsv')
    print('3.4 BDB-tagolás:')
    for r in szak:
        if r['strong'] in STRONGOK:
            print('   ', r['strong'], r['szakasz'], r['utvonal'], '|', r['szoveg'][:70])

    _, vj = tabla('adat/bdb_vers_jelentes.tsv')
    print('3.5 BDB példahelyek (a motívum három versén):')
    versek = {r['igehely'] for r in sajat}
    for r in vj:
        if r['strong'] in STRONGOK and r['karoli_vers'] in versek:
            print('   ', r['strong'], r['karoli_vers'], r['utvonal'], r['szakasz'], r['okkod'])

    print('3.6 tokenek a versben (TAHOT):')
    tfej, tah = tabla('konkordancia/TAHOT_kivonat.tsv')
    strong_mezo = [m for m in tfej if 'strong' in m.lower()]
    for v in sorted(versek):
        for s in sorted(STRONGOK):
            n = sum(1 for r in tah if r.get('Igehely') == v and any(s in r.get(m, '') for m in strong_mezo))
            print('   ', v, s, n)

    _, hu = tabla('adat/bdb_szakasz_hu.tsv')
    print('3.7 magyar BDB-szakasz:')
    for r in hu:
        if r['strong'] in STRONGOK:
            print('   ', r['strong'], r['szakasz'], r['utvonal'], r['kategoria'])

    _, ford = tabla('adat/forditasok.tsv')
    print('3.8 forditasok.tsv:')
    for r in ford:
        if r['strong'] in STRONGOK:
            print('   ', r['szotar'], r['strong'], r['jelentes_szam'], r['mezo'], r['allapot'], r['modell'])

    print('3.9 sorok a táblákban:')
    for rel, mezok in (('adat/szotar_szakasz_cimke.tsv', ('strong',)),
                       ('adat/lexikon_hivatkozasok.tsv', ('strong',)),
                       ('adat/res_forras.tsv', ('id',)),
                       ('adat/lxx_dontesek.tsv', ('id', 'heber_strong')),
                       ('adat/bdb_forras_javitas.tsv', ('strong',)),
                       ('adat/kiadasok.tsv', ('id',)),
                       ('adat/funkcio_kapcsolok.tsv', ('id',))):
        _, t = tabla(rel)
        print('   ', rel, sum(1 for r in t if erint(r, *mezok)))

    _, jel = tabla('adat/jeloltek.tsv')
    print('3.10 jeloltek.tsv (id/cel_id = TEREMT-002):',
          sum(1 for r in jel if r['id'] == ID or r.get('cel_id') == ID))
    _, aud = tabla('adat/auditok.tsv')
    print('     auditok.tsv TEREMT-002:', sum(1 for r in aud if r['id'] == ID),
          '| ebből lxx-hid:', sum(1 for r in aud if r['id'] == ID and 'lxx' in r['lepes']))

    _, mot = tabla('adat/motivumok.tsv')
    print('3.11 motivumok.tsv:')
    for r in mot:
        if r['id'] == ID:
            for m in ('statusz', 'statusz_verzio', 'azonossag_tipusa', 'negativ_kriterium',
                      'folerendelt_fogalom', 'sablon_verzio', 'forras_study'):
                print('   ', m, '=', r[m][:100])

    with open(os.path.join(GYOKER, 'motivumok', ID + '.md'), encoding='utf-8') as f:
        md = f.read().split('\n')
    print('3.12 motivumok/TEREMT-002.md:', len(md), 'sor; RÉS-jelölő:',
          sum(1 for s in md if 'RÉS-KEZDET' in s))
    for s in md:
        if s.startswith('#'):
            print('   ', s[:90])
    print('     lexikon/TEREMT-002_TUDOMANYOS.md létezik:',
          os.path.exists(os.path.join(GYOKER, 'lexikon', ID + '_TUDOMANYOS.md')))


if __name__ == '__main__':
    main()
