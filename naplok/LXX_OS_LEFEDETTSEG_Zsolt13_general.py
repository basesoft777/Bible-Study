"""F54 / M1 (d), DT-F54b: a Zsolt 13 kulcsainak javitasa felulbiralasi sorokkal.

A Karoli a zsoltarcimet szamozott versnek veszi (Zsolt 13:1), igy a helyes parositas
LXX Ps 12:n -> Zsolt 13:n (n = 1..6). A meglevo kulcsok egy verssel eltoltak voltak
(12:2->13:1, 12:3->13:2, 12:4->13:3, 12:5->13:4), a 12:6 kulcsa az M1-ben (tabla, 13:6) jott letre.
Tartalmi ellenorzes (Karoli <-> LXX): 13:2 "meddig felejtkezel" = 12:2; 13:3 "meddig tanakodjam" = 12:3;
13:4 "nezz ide, felelj nekem" = 12:4; 13:5 "hogy ne mondja ellensegem" = 12:5; 13:6 "kegyelmedben biztam" = 12:6.
Idempotens; hozzafuz a konkordancia/LXX_OS/karoli_vers_felulbiralas.tsv-hez.
"""
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).replace('\\', '/') + '/'
utvonal = R + 'konkordancia/LXX_OS/karoli_vers_felulbiralas.tsv'
sorok = open(utvonal, encoding='utf-8').read().rstrip('\n').split('\n')
van = {tuple(l.split('\t')[:3]) for l in sorok if not l.startswith('#') and not l.startswith('book_key')}
TART = {
    1: 'cim: "Az eneklőmesternek; Dávid zsoltára" = "eis to telos psalmos to Dauid"',
    2: '"Uram, meddig felejtkezel" = "heos pote kyrie epilethe mou"',
    3: '"Meddig tanakodjam lelkemben" = "heos tinos thesomai boulas en psyche mou"',
    4: '"Nézz ide, felelj nékem" = "epiblepson eisakouson mou kyrie"',
    5: '"Hogy ne mondja ellenségem" = "mepote eipe ho echthros mou"',
    6: '"kegyelmedben bíztam" = "ego de epi to eleei sou elpisa"',
}
uj = []
for n in range(1, 7):
    k = ('psalms', '12', str(n))
    if k in van:
        continue
    indok = ('F54 DT-F54b: a Karoli a cimet szamozott versnek veszi, igy LXX Ps 12:%d -> Zsolt 13:%d; tartalmi egyezes (manual, ts=2026-10-11): %s' % (n, n, TART[n]))
    uj.append('\t'.join(['psalms', '12', str(n), 'Zsolt 13:%d' % n, indok]))
if uj:
    sorok.extend(uj)
    with open(utvonal, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok) + '\n')
print('uj sor:', len(uj))
