"""F123 ANTROP-001, 1. kiadás előkészítése (DT-F123t): a BDB H2416 bdb_szakasz_hu.tsv 14. sorának
kézi sorjavítása (az ALVIL.1 mintája). A hu_illeszt.py a BDB2718 -/1/a sorát `elakad`-ra illeszti,
a magyar szöveg viszont megvan (adat/forditasok.tsv BDB H2416 sz14). Olvasás split('\t'), írás '\t'.join()."""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = Path(__file__).resolve().parent.parent
p = G / 'adat' / 'bdb_szakasz_hu.tsv'
sorok = p.read_text(encoding='utf-8').split('\n')
n0 = len(sorok)

sz14 = None
for s in (G / 'adat' / 'forditasok.tsv').read_text(encoding='utf-8').split('\n'):
    m = s.rstrip('\r').split('\t')
    if len(m) > 7 and m[0] == 'BDB' and m[1] == 'H2416' and m[3] == 'sz14' and m[7] != 'elavult':
        sz14 = m[6]
if not sz14 or not sz14.startswith('a. általában'):
    sys.exit('HIBA: a sz14 fordítás nem található')

talalt = [i for i, s in enumerate(sorok) if s.split('\t')[:2] == ['H2416', '14']]
if len(talalt) != 1:
    sys.exit('HIBA: H2416 14. sor: %d találat' % len(talalt))
i = talalt[0]
m = sorok[i].rstrip('\r').split('\t')
if m[2] != 'BDB2718' or m[5] != '-/1/a' or m[7] != 'elakad' or m[11] != '':
    sys.exit('HIBA: váratlan sor: %r' % m[:12])
m[7] = 'illeszkedik'
m[9] = ''
m[10] = ''
m[11] = sz14
m[13] = ('scope=H2416 | forras=kézi sorjavítás 2026-11-03 (F123 ANTROP-001 1. kiadás előkészítése, DT-F123t; '
         'az ALVIL.1 mintája): a szöveg az adat/forditasok.tsv BDB H2416 sz14 sora; a hu_illeszt.py ezt a sort '
         'elakad-ra illeszti (N-F123m) | ts=2026-11-03')
sorok[i] = '\t'.join(m) + ('\r' if sorok[i].endswith('\r') else '')

fej = [j for j, s in enumerate(sorok[:3]) if s.startswith('# GENERÁLT:')]
if len(fej) != 1:
    sys.exit('HIBA: a fejléc nem található')
j = fej[0]
cr = '\r' if sorok[j].endswith('\r') else ''
jel = (' Kézi sorjavítás: H2416 14. sor (BDB2718 -/1/a), ts=2026-11-03 (DT-F123t; a hu_illeszt.py '
       'újrafuttatása felülírja, l. N-F123m).')
if jel not in sorok[j]:
    sorok[j] = sorok[j].rstrip('\r') + jel + cr

if len(sorok) != n0:
    sys.exit('HIBA: sorszám változna')
p.write_text('\n'.join(sorok), encoding='utf-8', newline='')
print('ok:', sz14[:60])
