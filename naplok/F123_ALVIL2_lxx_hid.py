# -*- coding: utf-8 -*-
"""F123 ALVIL-001 új cikk, U1 — LXX-híd a teljes ÓSZ-re (6. lépés, a `lekerdez.py lxx-hid`
logikája versenként, egyszerre): a H7585-versek LXX-megfelelőjében áll-e ᾅδης (G0086), és
melyik kanonikus LXX-versben áll ᾅδης H7585 nélkül (LXX-többlet). Kanonikus könyvek, a
`lxx_os_import.elsodleges_slug` szövegváltozata. Döntés nélkül.
Kimenet: naplok/F123_ALVIL2_lxx_hid.tsv; összegzés a konzolra."""
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L  # noqa: E402
import lxx_os_import as OS  # noqa: E402

TS = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
tahot = L.load_tahot()
seol = defaultdict(int)
konyvek = []
for r in tahot:
    b = r['_parsed'][0]
    if b not in konyvek:
        konyvek.append(b)
    if r['Strong-szám'] == 'H7585':
        seol[r['Igehely']] += 1

lxx_szo = defaultdict(list)     # karoli-vers -> [(lemma, szoalak, strong)]
fajlok = set()
for b in konyvek:
    slug = OS.elsodleges_slug(b)
    if not slug:
        continue
    ut = os.path.join(GY, 'konkordancia', 'LXX_OS', slug + '.tsv')
    if not os.path.exists(ut) or slug in fajlok:
        continue
    fajlok.add(slug)
    sorok = [s.rstrip('\r\n').split('\t') for s in open(ut, encoding='utf-8') if not s.startswith('#')]
    fej = sorok[0]
    for s in sorok[1:]:
        d = dict(zip(fej, s))
        if d.get('igehely_karoli'):
            lxx_szo[d['igehely_karoli']].append((d['lemma'], d['szoalak'], d['strong']))

ki = []
for v in sorted(seol, key=L.parse_igehely):
    szavak = lxx_szo.get(v, [])
    hades = [x[1] for x in szavak if x[0].lower() == 'ᾅδης']
    if not szavak:
        oszt = 'nincs LXX-vers'
    elif hades:
        oszt = 'seól → ᾍδης'
    else:
        oszt = 'seól → más'
    ki.append((v, oszt, ', '.join(hades) or '—'))
plusz = sorted([v for v, sz in lxx_szo.items() if any(x[0].lower() == 'ᾅδης' for x in sz) and v not in seol],
               key=L.parse_igehely)
for v in plusz:
    ki.append((v, 'ᾍδης seól nélkül (LXX-többlet)', ', '.join(x[1] for x in lxx_szo[v] if x[0].lower() == 'ᾅδης')))

prov = ('scope=TAHOT-teljes H7585 × LXX_OS kanonikus könyvek (%d fájl, elsodleges_slug) | '
        'forras=TAHOT_kivonat.tsv+LXX_OS/*.tsv (igehely_karoli, lemma) | ts=%s' % (len(fajlok), TS))
with open(os.path.join(GY, 'naplok', 'F123_ALVIL2_lxx_hid.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('# ' + prov + '\n')
    f.write('igehely\tosztaly\tlxx_szoalak\n')
    for s in ki:
        f.write('\t'.join(s) + '\n')
from collections import Counter
c = Counter(o for _, o, _ in ki)
for k, v in c.most_common():
    print('%3d  %s' % (v, k))
print('seól → más:', ', '.join(v for v, o, _ in ki if o == 'seól → más'))
print('nincs LXX-vers:', ', '.join(v for v, o, _ in ki if o == 'nincs LXX-vers'))
print('LXX-többlet:', ', '.join(plusz))
print('proveniencia:', prov)
