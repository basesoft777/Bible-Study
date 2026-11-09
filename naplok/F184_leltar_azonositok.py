"""F184.D0 leltár-szkenner (scratch, a repón kívül).

Folyamat-dokumentumokban azonosító-jeleket keres (V<n>, E<nn>, HIBA-*, C-vh, DT<n>,
DT-F<nn><x>, ellenoriz.py sorszám, SEMA <n.nn>, kapunevek), és azonosítónként
kiírja, hány dokumentumban és mely sorokban áll. A DONTESEK.md-ből csak azokat a
sorokat veszi, amelyek a többi dokumentum által hivatkozott DT-azonosítót definiálják.

Használat: python naplok/F184_leltar_azonositok.py <repo> <kimenet.tsv>
"""
import re
import sys
import glob
import os
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

repo, kimenet = sys.argv[1], sys.argv[2]
os.chdir(repo)

fajlok = ['CLAUDE.md', 'MUNKAMENET.md', 'BRIEF_SABLON.md', 'adat/SEMA.md',
          'Rendszerfejlesztesi_playbook.md']
fajlok += sorted(glob.glob('sablonok/*.md'))
fajlok += sorted(glob.glob('.claude/commands/*.md'))

MINTAK = {
    'V': re.compile(r'(?<![\w-])V[1-9]\b'),
    'E': re.compile(r'(?<![\w-])E[1-9][0-9]\b'),
    'HIBA': re.compile(r'HIBA-[A-ZÁÉÍÓÖŐÚÜŰ0-9_-]+'),
    'Cvh': re.compile(r'\bC-vh\b'),
    'DT': re.compile(r'\bDT[0-9]{1,4}\b'),
    'DTF': re.compile(r'\bDT-F[0-9]{2,3}[a-z]{0,2}\b'),
    'SEMA': re.compile(r'SEMA(?:\.md)?\s*(?:§\s*)?([0-9]+\.[0-9]+(?:\.[0-9]+)?)'),
    'kapu': re.compile(r'\b(olvasoi_kapu|ellenoriz\.py|szabalyok\.py|lap_kapu|forras_kapu|vh_kapu)\b'),
    'ell_sorszam': re.compile(r'ellenoriz\.py[^\n]{0,40}?\b(\d{1,2})\.'),
}


def kulcsok(sor):
    for nev, m in MINTAK.items():
        for t in m.finditer(sor):
            if nev in ('SEMA',):
                yield 'SEMA ' + t.group(1)
            elif nev == 'ell_sorszam':
                yield 'ellenoriz.py ' + t.group(1) + '.'
            else:
                yield t.group(0)


elofordulas = defaultdict(lambda: defaultdict(list))  # kulcs -> fajl -> [sorszam]
szakasz_cache = {}
for f in fajlok:
    if not os.path.exists(f):
        continue
    sorok = open(f, encoding='utf-8').read().split('\n')
    szakasz = ''
    for i, s in enumerate(sorok, 1):
        if s.startswith('#'):
            szakasz = s.strip('# ').strip()[:50]
        for k in set(kulcsok(s)):
            elofordulas[k][f].append((i, szakasz))

# DONTESEK.md: csak a hivatkozott DT-sorok definíciója
dt_kulcsok = {k for k in elofordulas if k.startswith('DT')}
dont_def = {}
with open('DONTESEK.md', encoding='utf-8') as fh:
    for i, s in enumerate(fh, 1):
        m = re.match(r'\|\s*\*{0,2}(DT[-F0-9a-z]+)\*{0,2}\s*\|', s)
        if m and m.group(1) in dt_kulcsok:
            dont_def[m.group(1)] = i

ki = []
for k, fm in elofordulas.items():
    ndok = len(fm) + (1 if k in dont_def else 0)
    if len(fm) < 2:
        continue
    helyek = []
    for f, lst in sorted(fm.items()):
        helyek.append(f + ':' + ','.join(str(i) for i, _ in lst[:12]) + ('…' if len(lst) > 12 else ''))
    if k in dont_def:
        helyek.append('DONTESEK.md:' + str(dont_def[k]))
    ki.append((ndok, k, ' ; '.join(helyek)))

ki.sort(key=lambda r: (-r[0], r[1]))
with open(kimenet, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('dok_szam\tkulcs\telofordulasok\n')
    for r in ki:
        fh.write('%d\t%s\t%s\n' % r)
print('fajlok:', len(fajlok), '| kulcs >=2 dokban:', len(ki))
