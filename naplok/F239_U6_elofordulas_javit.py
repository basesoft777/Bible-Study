# -*- coding: utf-8 -*-
"""F239 U6 — a TEREMT-001 négy 1/a-sorának javítása az adat/elofordulasok.tsv-ben (K99; D21; D5; D4).
Pontcsere: minden `regi` pontosan egyszer áll a megnevezett sor megnevezett mezőjében; minden más sor bájtra azonos.
Futtatás: python naplok/F239_U6_elofordulas_javit.py [--ir]"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(GY, 'adat', 'elofordulasok.tsv')
CSERE = [
    ('1Móz 7:11', 'kapcsolodas',
     'A mélység forrásai a héberben csak itt és a 8:2-ben állnak együtt;',
     'A mélység és a források szava a héberben a 8:2-n kívül csak a Péld 8:24-ben áll még együtt;'),
    ('Zsolt 36:7', 'kapcsolodas',
     ' A hasonlat a magasság és a mélység két végpontjával méri Isten igazságát és ítéleteit.', ''),
    ('Jel 9:11', 'funkcio',
     'a mélységnek királya van, a Vesztő', 'a sáskák királya a mélység angyala, a Vesztő'),
    ('Jel 9:11', 'kapcsolodas',
     'A mélységnek itt uralkodója van, akinek a neve a pusztítást mondja.',
     'A sáskák királya itt a mélység angyala, akinek a neve a pusztítást mondja.'),
    ('Jel 20:3', 'funkcio',
     'bezárják és lepecsételik, ezer esztendőre', 'a sárkányt a mélységbe vetik és bezárják, ezer esztendőre'),
    ('Jel 20:3', 'kapcsolodas',
     'A Jelenések könyvében a mélységet a 9:2-ben megnyitják, itt bezárják és lepecsételik; a lezárás időre szól.',
     'A Jelenések könyvében a mélység kútját a 9:2-ben megnyitják, itt a sárkányt zárják a mélységbe, és pecsétet tesznek fölé; a fogság időre szól.'),
]
nyers = open(UT, encoding='utf-8', newline='').read()
sorok = nyers.split('\n')
fej = sorok[1].split('\t')
uj = list(sorok)
for ig, mezo, regi, ujs in CSERE:
    idx = [i for i, s in enumerate(uj) if s.split('\t')[:2] == ['TEREMT-001', ig]]
    if len(idx) != 1:
        sys.exit('HIBA: %s sor %d-szer' % (ig, len(idx)))
    f = uj[idx[0]].split('\t')
    j = fej.index(mezo)
    if f[j].count(regi) != 1:
        sys.exit('HIBA: %s/%s: a régi szöveg %d-szer áll' % (ig, mezo, f[j].count(regi)))
    f[j] = f[j].replace(regi, ujs)
    uj[idx[0]] = '\t'.join(f)
valt = [i for i in range(len(sorok)) if sorok[i] != uj[i]]
print('változott sor:', len(valt), [uj[i].split('\t')[1] for i in valt])
assert len(uj) == len(sorok) and all(len(uj[i].split('\t')) == len(sorok[i].split('\t')) for i in valt)
if '--ir' in sys.argv:
    open(UT, 'w', encoding='utf-8', newline='').write('\n'.join(uj))
    ujra = open(UT, encoding='utf-8', newline='').read().split('\n')
    assert ujra == uj
    print('írva:', UT)
