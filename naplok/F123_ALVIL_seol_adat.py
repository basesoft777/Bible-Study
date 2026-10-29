"""F123.ALVIL.J32 (ELLENOR_F123_ALVIL-001_3 A, DT-F123m): a Seol-csere (DT26, DT-F123k) kiterjesztése az ALVIL-001 lapján
megjelenő adatmezőkre.

Célmezők (a lap 63 „Seól”-jának forrásai):
- `adat/elofordulasok.tsv` `kapcsolodas`, csak az ALVIL-001 sorok;
- `adat/jeloltek.tsv` a #123 saját 3 jelöltsora (ALVIL-001, `forras_kereses` „F123 X.A …”): `forras_kereses`, `indoklas`;
- `adat/motivum_kapcsolatok.tsv` 2 sora (ALVIL-001 ApCsel 2:27/2:31 ↔ ISTENTISZT-001 ApCsel 2:21, `funkcio`): **kihagyva**, mert a
  sor az ISTENTISZT-001 lapján is megjelenik (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`), amelyen párhuzamos session dolgozik
  (DT-F123m: ilyenkor megállás és jelzés).
Kivétel a szó szerinti idézet („…” a felhasználó szavaiból vagy egy forrás saját írásmódjából): a célmezőkben ilyen nincs; a
`kapcsolodas` "…" idézőjeles alakjai a régi tanulmány saját (nem Károli-) fordításai, a forrás J7-es cseréjével azonosan kezelve.

Csere: „Seól” → „Seol” (ragozva is, a szótő cseréjével). TSV: `split('\\t')` / `'\\t'.join()`; írás előtt soronkénti összevetés:
csak a célmezők változhatnak, és bennük csak a „Seól” → „Seol”. A csere- és kihagyáslista: `naplok/F123_ALVIL_seol_adat.tsv`.

    python naplok/F123_ALVIL_seol_adat.py [--ir]
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLO = os.path.join(GY, 'naplok', 'F123_ALVIL_seol_adat.tsv')
TS = '2026-10-29'

CELOK = [
    ('adat/elofordulasok.tsv', ['kapcsolodas'], lambda d: d['id'] == 'ALVIL-001'),
    ('adat/jeloltek.tsv', ['forras_kereses', 'indoklas'],
     lambda d: d['id'] == 'ALVIL-001' and d['forras_kereses'].startswith('F123 X.A')),
]
KIHAGY = [
    ('adat/motivum_kapcsolatok.tsv', ['funkcio'], lambda d: 'ALVIL-001' in (d['id_a'], d['id_b']),
     'kihagyva: a sor az ISTENTISZT-001 lapján is megjelenik (párhuzamos session; DT-F123m: megállás és jelzés)'),
]


def tabla(ut):
    s = io.open(os.path.join(GY, ut), encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    L = s.split(nl)
    fi = next(i for i, x in enumerate(L) if x and not x.startswith('#'))
    return s, nl, L, fi, L[fi].split('\t')


def main():
    ir = '--ir' in sys.argv
    naplo = []
    uj_fajlok = {}
    for ut, mezok, cond in CELOK:
        s, nl, L, fi, fej = tabla(ut)
        idx = [fej.index(m) for m in mezok]
        L2 = list(L)
        for i in range(fi + 1, len(L)):
            x = L[i]
            if not x or x.startswith('#'):
                continue
            m = x.split('\t')
            d = dict(zip(fej, m))
            if not cond(d):
                continue
            m2 = list(m)
            for j in idx:
                if 'Seól' in m[j]:
                    m2[j] = m[j].replace('Seól', 'Seol')
                    naplo.append([ut, str(i + 1), d.get('id', ''), d.get('igehely', ''), fej[j], str(m[j].count('Seól')),
                                  'csere', m[j], m2[j]])
            elter = [j for j in range(len(m)) if m[j] != m2[j]]
            assert set(elter) <= set(idx), (ut, i, elter)
            for j in elter:
                assert m2[j] == m[j].replace('Seól', 'Seol')
            L2[i] = '\t'.join(m2)
        assert len(L2) == len(L)
        assert all(L[i] == L2[i] or 'Seól' in L[i] for i in range(len(L)))
        uj_fajlok[ut] = nl.join(L2)
    for ut, mezok, cond, ok in KIHAGY:
        s, nl, L, fi, fej = tabla(ut)
        for i in range(fi + 1, len(L)):
            x = L[i]
            if not x or x.startswith('#'):
                continue
            m = x.split('\t')
            d = dict(zip(fej, m))
            if cond(d):
                for f in mezok:
                    if 'Seól' in d[f]:
                        naplo.append([ut, str(i + 1), '%s↔%s' % (d['id_a'], d['id_b']), d['igehely_a'], f,
                                      str(d[f].count('Seól')), ok, d[f], d[f]])
    with open(NAPLO, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F123.ALVIL.J32 (ELLENOR_F123_ALVIL-001_3 A, DT-F123m): a „Seól” → „Seol” csere adatmezőkben | készítő: '
                'naplok/F123_ALVIL_seol_adat.py | proveniencia: scope=ALVIL-001 lapjának adatmezői (elofordulasok kapcsolodas, '
                'jeloltek #123 3 sora, motivum_kapcsolatok) | forras=split(\'\\t\'), soronkénti összevetés | ts=%s\n' % TS)
        f.write('\t'.join(['tabla', 'sor', 'id', 'igehely', 'mezo', 'db', 'muvelet', 'regi', 'uj']) + '\n')
        for r in naplo:
            f.write('\t'.join(r) + '\n')
    cs = [r for r in naplo if r[6] == 'csere']
    kh = [r for r in naplo if r[6] != 'csere']
    print('CSERE\t%d mező, %d előfordulás' % (len(cs), sum(int(r[5]) for r in cs)))
    print('KIHAGYVA\t%d mező, %d előfordulás' % (len(kh), sum(int(r[5]) for r in kh)))
    if ir:
        for ut, t in uj_fajlok.items():
            io.open(os.path.join(GY, ut), 'w', encoding='utf-8', newline='').write(t)
        print('ÍRVA: ' + ', '.join(uj_fajlok))


if __name__ == '__main__':
    main()
