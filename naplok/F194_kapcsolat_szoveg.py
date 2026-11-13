# -*- coding: utf-8 -*-
"""F194.30 — három ISTENTISZT-001 kapcsolat-sor szövege a lektor 6. tétele és megjegyzése szerint (adat/kapcsolatok.tsv).

(1) 1Móz 4:26 → 2Móz 33:19, (2) 2Móz 33:19 → 34:5: a `funkcio` a DT-F194b szerint (a héber szerkezet azonos, a
fordítás kiáltásként adja vissza; az Úr saját mondata csak a 33:19-ben); (3) 1Móz 13:4 → 26:25: a 13:4 oltára Béthel
és Hái között áll, nem Beérsebában. A sorok kulcsa (forras_igehely, cel_igehely, id), a többi mező változatlan.
Futtatás a repó gyökeréből: python naplok/F194_kapcsolat_szoveg.py"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
P = 'adat/kapcsolatok.tsv'
UJ = {
    ('1Móz 4:26', '2Móz 33:19'): {'funkcio': 'azonos szerkezet (kárá + besém + Jahve) — a 2Móz 33:19-ben az Úr mondatában; a magyar fordítás kiáltásként adja vissza'},
    ('2Móz 33:19', '2Móz 34:5'): {'funkcio': 'ugyanaz a jelenet: a 33:19 ígérete és a 34:5 jelenete, azonos szerkezettel; a 34:5 a kiáltót nem nevezi meg'},
    ('1Móz 13:4', '1Móz 26:25'): {'funkcio': 'öröklés — azonos szereposztás nemzedékek közt',
                                  'indoklas': 'Izsák explicit Ábrahám fia, és ugyanazt teszi, amit Ábrahám az 1Móz 13:4-ben: oltárnál segítségül hívja az Úr nevét — a nemzedéki kapcsolat a szövegből ered, nem következtetésből.'},
}
raw = open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
sorok = raw.split(nl)
fej = [s for s in sorok if s and not s.startswith('#')][0].split('\t')
ix = {k: i for i, k in enumerate(fej)}
n = 0
for i, s in enumerate(sorok):
    c = s.split('\t')
    if len(c) == len(fej) and c[ix['id']] == 'ISTENTISZT-001' and (c[0], c[1]) in UJ:
        for k, v in UJ[(c[0], c[1])].items():
            c[ix[k]] = v
        sorok[i] = '\t'.join(c); n += 1
assert n == 3, n
open(P, 'w', encoding='utf-8', newline='').write(nl.join(sorok))
print('%s: %d sor' % (P, n))
