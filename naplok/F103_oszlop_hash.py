"""F103_oszlop_hash.py — F103 (DT-F103a (A), feltétel (1)): a 2.29 tábla (adat/bdb_vers_jelentes.tsv) régi oszlopainak hash-e.

Az oszlopok NÉV szerint olvasva (split('\\t')), a két `#` fejlécsor nélkül; a hash a régi 15 oszlop soronkénti tab-join-jának SHA-256-ja.
Használat (a repó gyökeréből):
  python naplok/F103_oszlop_hash.py                    # a mai tábla
  python naplok/F103_oszlop_hash.py --git <commit>     # a tábla a megadott commitban (git show)
"""
import hashlib
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGI = ['strong', 'bdb_id', 'sorszam', 'poz', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'szakasz', 'resz',
        'utvonal', 'okkod', 'szurt', 'proveniencia']


def hash_regi(szoveg):
    sorok = [s for s in szoveg.split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    idx = [fej.index(k) for k in REGI]
    h = hashlib.sha256()
    for s in sorok[1:]:
        m = s.split('\t')
        h.update(('\t'.join(m[i] for i in idx) + '\n').encode('utf-8'))
    return h.hexdigest(), len(sorok) - 1, fej


def main():
    if '--git' in sys.argv:
        c = sys.argv[sys.argv.index('--git') + 1]
        szoveg = subprocess.check_output(['git', '-C', REPO, 'show', '%s:adat/bdb_vers_jelentes.tsv' % c]).decode('utf-8')
    else:
        with open(os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv'), encoding='utf-8', newline='') as f:
            szoveg = f.read()
    h, n, fej = hash_regi(szoveg)
    print('regi_oszlopok_sha256\t%s' % h)
    print('sor\t%d' % n)
    print('fejlec\t%s' % ','.join(fej))


if __name__ == '__main__':
    main()
