"""
zaro4_adatpotlas.py — ISTENTISZT_V3_ZARO4.md Y1-Y2: hianyzo besorolasok
potlasa es egy kiejtes-helyreigazitas az adat/elofordulasok.tsv-ben.

Y1: a cel-mezo JELENLEG URES kell legyen minden sorban -- ha nem az, ⛔
(iras nem tortenik semelyik tablaban). Y2: normal, "regi" pontosan egy
elofordulasos csere.

TSV-olvasas/iras kizarolag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')
ELOFORDULASOK = os.path.join(ADAT, 'elofordulasok.tsv')

# ---------------------------------------------------------------------------
# Y1 -- hianyzo besorolasok (a cel-mezonek URESNEK kell lennie)
# ---------------------------------------------------------------------------
Y1 = [
    dict(id='ISTENTISZT-001', igehely='1Móz 21:33', mezo='pardes_szint', uj='Drash'),
    dict(id='ISTENTISZT-001', igehely='1Móz 26:25', mezo='pardes_szint', uj='Drash'),
]
for ige in ('ApCsel 9:14', 'ApCsel 9:21', 'ApCsel 22:16', 'Róm 10:14', '1Kor 1:2', '2Tim 2:22', '1Pét 1:17'):
    Y1.extend([
        dict(id='ISTENTISZT-001', igehely=ige, mezo='lexikon_szotar', uj='TBESG'),
        dict(id='ISTENTISZT-001', igehely=ige, mezo='lexikon_entry_id', uj='G1941'),
        dict(id='ISTENTISZT-001', igehely=ige, mezo='jelentes_szam', uj='2'),
        dict(id='ISTENTISZT-001', igehely=ige, mezo='jelentes_hu', uj='segítségül hívni, invokálni'),
    ])

# ---------------------------------------------------------------------------
# Y2 -- kiejtes-helyreigazitas (1 csere)
# ---------------------------------------------------------------------------
Y2 = [
    dict(id='HAMART-001', igehely='Zsid 6:7-8', mezo='kapcsolodas',
         regi='a κατάρα-szócsaláddal (katara)', uj='a κατάρα (katara)-szócsaláddal'),
]


def read_tsv_raw(path):
    with open(path, encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]
    comment_lines = []
    i = 0
    while i < len(lines) and lines[i].startswith('#'):
        comment_lines.append(lines[i])
        i += 1
    header = lines[i].split('\t')
    data_lines = lines[i + 1:]
    return comment_lines, header, data_lines


def write_tsv_raw(path, comment_lines, header, data_lines):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for c in comment_lines:
            f.write(c + '\n')
        f.write('\t'.join(header) + '\n')
        for line in data_lines:
            f.write(line + '\n')


def main():
    comment_lines, header, data_lines = read_tsv_raw(ELOFORDULASOK)
    idx = {name: i for i, name in enumerate(header)}
    rows = [line.split('\t') if line else None for line in data_lines]

    key_to_row = {}
    for i, cols in enumerate(rows):
        if cols is None:
            continue
        key = (cols[idx['id']], cols[idx['igehely']])
        key_to_row.setdefault(key, []).append(i)

    hibak = []
    terv_y1 = []
    for spec in Y1:
        key = (spec['id'], spec['igehely'])
        key_desc = 'id=%s / igehely=%s' % key
        talalt = key_to_row.get(key, [])
        if len(talalt) != 1:
            hibak.append('%s: %d sor illeszkedik a kulcsra (1 helyett)' % (key_desc, len(talalt)))
            continue
        row_i = talalt[0]
        mezo_idx = idx[spec['mezo']]
        jelenlegi = rows[row_i][mezo_idx]
        if jelenlegi != '':
            hibak.append('%s (%s): a mező NEM üres, hanem %r -- Y1 nem alkalmazható'
                          % (key_desc, spec['mezo'], jelenlegi))
            continue
        terv_y1.append((row_i, mezo_idx, spec['uj'], key_desc, spec['mezo']))

    terv_y2 = []
    for spec in Y2:
        key = (spec['id'], spec['igehely'])
        key_desc = 'id=%s / igehely=%s' % key
        talalt = key_to_row.get(key, [])
        if len(talalt) != 1:
            hibak.append('%s: %d sor illeszkedik a kulcsra (1 helyett)' % (key_desc, len(talalt)))
            continue
        row_i = talalt[0]
        mezo_idx = idx[spec['mezo']]
        cella = rows[row_i][mezo_idx]
        n = cella.count(spec['regi'])
        if n != 1:
            hibak.append("%s (%s): a régi minta %d alkalommal fordul elő (1 helyett): %r"
                          % (key_desc, spec['mezo'], n, spec['regi']))
            continue
        uj_cella = cella.replace(spec['regi'], spec['uj'], 1)
        terv_y2.append((row_i, mezo_idx, uj_cella, key_desc, spec['mezo'], spec['regi'], spec['uj']))

    if hibak:
        print('MEGALLAS -- %d hiba, iras nem tortent:' % len(hibak))
        for h in hibak:
            print('  - %s' % h)
        sys.exit(2)

    for row_i, mezo_idx, uj_ertek, _key_desc, _mezo in terv_y1:
        rows[row_i][mezo_idx] = uj_ertek
    for row_i, mezo_idx, uj_ertek, _key_desc, _mezo, _regi, _uj in terv_y2:
        rows[row_i][mezo_idx] = uj_ertek

    data_lines_uj = ['\t'.join(cols) if cols is not None else '' for cols in rows]
    write_tsv_raw(ELOFORDULASOK, comment_lines, header, data_lines_uj)

    # vegso ellenorzes: fajlbol ujraolvasva
    _c2, _h2, data_lines2 = read_tsv_raw(ELOFORDULASOK)
    rows2 = [line.split('\t') if line else None for line in data_lines2]

    ok1 = 0
    for row_i, mezo_idx, uj_ertek, key_desc, mezo in terv_y1:
        vegso = rows2[row_i][mezo_idx]
        ok = vegso == uj_ertek
        ok1 += 1 if ok else 0
        print('Y1  %s [%s]: -> %r  [%s]' % (key_desc, mezo, uj_ertek, 'OK' if ok else 'HIBA'))
    print('Y1: %d/%d mező kitöltve, igazolva a végső tartalomban' % (ok1, len(Y1)))

    ok2 = 0
    for row_i, mezo_idx, _uj_ertek, key_desc, mezo, regi, uj in terv_y2:
        vegso = rows2[row_i][mezo_idx]
        ok = uj in vegso
        ok2 += 1 if ok else 0
        print('Y2  %s [%s]: %r -> %r  [%s]' % (key_desc, mezo, regi, uj, 'OK' if ok else 'HIBA'))
    print('Y2: %d/%d csere igazolva a végső tartalomban' % (ok2, len(Y2)))


if __name__ == '__main__':
    main()
