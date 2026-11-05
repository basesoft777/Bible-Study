"""F123 HAMART-001 U2: a Strong-háló 4 nyitott blokkjának (582 vers) gépi biztonsági mérése.

A régi napló a négy lexéma általános használatát elutasította (H0127 köznyelvi, H2403 bűnáldozat,
H7843 fizikai pusztítás, H2555 kollokáció nélkül). Itt azt mérem, van-e a blokkokban olyan vers,
amely a genezisi lánc egy-egy E-sorának szó szerinti szerkezetét hordozza:
  F1 = adamá + pānîm + pusztító ige (1Móz 6:7, 4:14 „a föld színéről” mintája)
  F2 = sáchat + erec/adamá (1Móz 6:11-13 „megromlott a föld” mintája)
  F3 = chámász + erec (1Móz 6:11,13 „megtelt a föld erőszakkal”, málé nélkül)
  F4 = chattát + adamá/erec egy versben (bűn és föld együtt)
Kimenet: naplok/F123_HAMART3_formula.tsv (minden mintatalálat Károli-szöveggel), összesítés a stdout-ra.
"""
import sys
import collections

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PUSZTITO = {'H4229', 'H8045', 'H3772', 'H7843', 'H5428', 'H6', 'H0006', 'H7993', 'H1644', 'H5080', 'H3423'}


def tsv(fajl):
    sorok = [l.rstrip('\n').split('\t') for l in open(fajl, encoding='utf-8') if not l.startswith('#')]
    return sorok[0], sorok[1:]


_, blokk = tsv('naplok/F123_teljesseg_HAMART-001_blokkok.tsv')
versek = collections.defaultdict(set)
for r in blokk:
    if r[0] == 'strong':
        versek[r[2]].add(r[1])

h, tahot = tsv('konkordancia/TAHOT_kivonat.tsv')
strongok = collections.defaultdict(set)
for r in tahot:
    if r[0] in versek:
        s = r[1].strip()
        for darab in s.replace('/', ' ').replace('+', ' ').split():
            if darab.startswith('H'):
                strongok[r[0]].add(darab[:5])

h2, karoli = tsv('konkordancia/Karoli_1908.tsv')
karoli_szoveg = {}
for r in karoli:
    if len(r) >= 2:
        karoli_szoveg[r[0]] = r[-1]

eredmeny = []
for v in sorted(versek):
    s = strongok[v]
    jel = []
    if 'H0127' in s and 'H6440' in s and s & PUSZTITO:
        jel.append('F1')
    if 'H7843' in s and ({'H0776', 'H0127'} & s):
        jel.append('F2')
    if 'H2555' in s and 'H0776' in s:
        jel.append('F3')
    if 'H2403' in s and ({'H0776', 'H0127'} & s):
        jel.append('F4')
    if jel:
        eredmeny.append((v, ','.join(sorted(versek[v])), '+'.join(jel), karoli_szoveg.get(v, '?')))

with open('naplok/F123_HAMART3_formula.tsv', 'w', encoding='utf-8') as ki:
    ki.write('# GENERÁLT: naplok/F123_HAMART3_formula.py | scope=naplok/F123_teljesseg_HAMART-001_blokkok.tsv halo=strong (582 vers) × TAHOT_kivonat.tsv × Karoli_1908.tsv | forras=split(\'\\t\') | ts=2026-11-05\n')
    ki.write('igehely\tblokk\tminta\tkaroli\n')
    for e in eredmeny:
        ki.write('\t'.join(e) + '\n')

print('blokk-vers:', len(versek), '| TAHOT-ban talált vers:', len(strongok), '| Károli-fejléc:', h2[:3])
c = collections.Counter()
for e in eredmeny:
    for m in e[2].split('+'):
        c[m] += 1
print('mintatalálat (vers):', len(eredmeny), dict(c))
