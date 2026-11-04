"""F123 ANTROP-001, 1. kiadás előtt (DT-F123u): a BDB H2416 bdb_szakasz_hu.tsv 13., 15–19. sorának
kézi sorjavítása (a DT-F123t, .21 mintája). A hu_illeszt.py a szakaszos fordítást összefűzi és jelölők
szerint újravágja (N-F123m), ezért a BDB2718-blokk elcsúszott; a sorok saját magyar szövege a
forditasok.tsv BDB H2416 sz<n> sora (sorszám 1:1, az angol szakasszal soronként összevetve).
Olvasás split('\t'), írás '\t'.join()."""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = Path(__file__).resolve().parent.parent
SOROK = {'13': ('-/1/-', 'animal, as living', '1 állat, mint élő'),
         '15': ('-/1/b', 'wild animals', 'b. vadállatok'),
         '16': ('-/1/c', 'living beings, of the cherubic', 'c. élőlények, a kerub'),
         '17': ('-/2/-', 'life, only in late poetry', '2 élet, csak késői'),
         '18': ('-/3/-', 'appetite, activity of hunger', '3 étvágy'),
         '19': ('-/4/-', 'revival, renewal', '4 újjáéledés')}

sz = {}
for s in (G / 'adat' / 'forditasok.tsv').read_text(encoding='utf-8').split('\n'):
    m = s.rstrip('\r').split('\t')
    if len(m) > 7 and m[0] == 'BDB' and m[1] == 'H2416' and m[7] != 'elavult':
        sz[m[3]] = m[6]
en = {}
for s in (G / 'adat' / 'bdb_szakaszok.tsv').read_text(encoding='utf-8').split('\n'):
    m = s.rstrip('\r').split('\t')
    if m[:2] == ['H2416', 'BDB2718']:
        en[m[2]] = (m[6], m[10])

p = G / 'adat' / 'bdb_szakasz_hu.tsv'
sorok = p.read_text(encoding='utf-8').split('\n')
n0 = len(sorok)
for n, (ut, en_kezd, hu_kezd) in SOROK.items():
    if en.get(n, ('', ''))[0] != ut or not en[n][1].startswith(en_kezd):
        sys.exit('HIBA: angol szakasz %s: %r' % (n, en.get(n)))
    hu = sz.get('sz' + n, '')
    if not hu.startswith(hu_kezd):
        sys.exit('HIBA: sz%s: %r' % (n, hu[:40]))
    talalt = [i for i, s in enumerate(sorok) if s.split('\t')[:2] == ['H2416', n]]
    if len(talalt) != 1:
        sys.exit('HIBA: H2416 %s. sor: %d találat' % (n, len(talalt)))
    i = talalt[0]
    m = sorok[i].rstrip('\r').split('\t')
    if m[2] != 'BDB2718' or m[5] != ut:
        sys.exit('HIBA: váratlan sor: %r' % m[:8])
    m[7] = 'illeszkedik'
    m[9] = ''
    m[10] = ''
    m[11] = hu
    m[13] = ('scope=H2416 | forras=kézi sorjavítás 2026-11-03 (F123 ANTROP-001 1. kiadás előtt, DT-F123u; '
             'a DT-F123t mintája): a szöveg az adat/forditasok.tsv BDB H2416 sz%s sora (sorszám 1:1, az angol '
             'szakasszal összevetve); a hu_illeszt.py ezt a sort elcsúsztatja (N-F123m) | ts=2026-11-03' % n)
    sorok[i] = '\t'.join(m) + ('\r' if sorok[i].endswith('\r') else '')
    print('ok', n, ut, hu[:50])

fej = [j for j, s in enumerate(sorok[:3]) if s.startswith('# GENERÁLT:')]
if len(fej) != 1:
    sys.exit('HIBA: a fejléc nem található')
j = fej[0]
cr = '\r' if sorok[j].endswith('\r') else ''
jel = (' Kézi sorjavítás: H2416 13., 15–19. sor (BDB2718), ts=2026-11-03 (DT-F123u; a hu_illeszt.py '
       'újrafuttatása felülírja, l. N-F123m).')
if jel not in sorok[j]:
    sorok[j] = sorok[j].rstrip('\r') + jel + cr

if len(sorok) != n0:
    sys.exit('HIBA: sorszám változna')
p.write_text('\n'.join(sorok), encoding='utf-8', newline='')
