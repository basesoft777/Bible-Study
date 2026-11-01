"""F131.3: a repón kívüli próbarender gépi mérése (a brief 3. lépése).

Bemenet: a próbarender könyvtára (`general.py --cel lexikon --id ISTENTISZT-001 --kimenet <dir>`,
a repón kívül). Csak olvas; a kimenet a stdout (a napló 3. szakasza ebből készül).

Mér:
  1. tiltott szembeállító keretezés a szótári gerincben és a „Jelentés (a szó)” oszlopban;
  2. a `(fordításra vár)` jelölések száma előtte (az éles lap) és utána (a próba), kulcsonként;
  3. a 32 előfordulás-sor címkéje vagy kimondott hiánya;
  4. a kiemelt szótári példahelyek száma (BDB 9 + 6, Thayer 7) és a meg nem találtak listája;
  5. a DT-F131h / (iv) hash-rögzítése: a bdb_szakaszok.tsv, a bdb_szakasz_hu.tsv és a
     glosszak_heber_hu.tsv H7121/H8034-sorainak SHA-1-e.

    python naplok/F131_proba_meres.py <próbakönyvtár>
"""
import collections
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402

LAP = 'ISTENTISZT-001_TUDOMANYOS.md'
JEL = '(fordításra vár)'
TILTOTT = ('eltér', 'máshová sorol', 'NEM invokáció', 'szemben a BDB', 'a BDB szerint nem')


def olvas(ut):
    with open(ut, encoding='utf-8') as f:
        return f.read()


def gerinc_reszek(szoveg):
    """A „Jelentéstartomány (szótári gerinc)” blokkok szövege (a következő `#### 1.` címig)."""
    return re.findall(r'^#### Jelentéstartomány \(szótári gerinc\)\n(.*?)(?=^#### 1\. )', szoveg, re.S | re.M)


def tabla_sorok(szoveg):
    blokk = szoveg.split('| Igehely | Kulcsszó |', 1)[1].split('\n\n', 1)[0]
    return [s for s in blokk.split('\n')[2:] if s.startswith('| [')]


def jelolesek_kulcsonkent(szoveg):
    h3 = h4 = kulcs = ''
    out = collections.Counter()
    for s in szoveg.split('\n'):
        if s.startswith('### '):
            h3, h4, kulcs = s[4:], '', ''
        elif s.startswith('#### '):
            h4, kulcs = s[5:], ''
        elif s.startswith('##### '):
            kulcs = s[6:]
        if JEL in s:
            out['%s | %s | %s' % (h3, h4, kulcs or '(blokkszint)')] += s.count(JEL)
    return out


def sor_hash(rel, strongok):
    sorok = []
    for s in olvas(os.path.join(GYOKER, rel)).split('\n'):
        if s and not s.startswith('#') and s.split('\t')[0] in strongok:
            sorok.append(s)
    return len(sorok), hashlib.sha1('\n'.join(sorok).encode('utf-8')).hexdigest()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    proba = os.path.join(sys.argv[1], 'lexikon', LAP)
    if os.path.abspath(proba).startswith(GYOKER + os.sep):
        sys.exit('HIBA: a próbarender a repón belül van')
    uj = olvas(proba)
    regi = olvas(os.path.join(GYOKER, 'lexikon', LAP))
    print('proveniencia: scope=ISTENTISZT-001 próbarender | forras=naplok/F131_proba_meres.py; %s | ts=%s'
          % (os.path.basename(sys.argv[1]), datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))

    print('\n## 1. Tiltott keretezés (kis- és nagybetű nélkül)')
    g = '\n'.join(gerinc_reszek(uj))
    sorok = tabla_sorok(uj)
    jel_oszlop = '\n'.join(s.split(' | ')[2] for s in sorok)
    print('gerinc-blokkok:', len(gerinc_reszek(uj)), '; táblasorok:', len(sorok))
    ossz = 0
    for t in TILTOTT:
        n1 = g.lower().count(t.lower())
        n2 = jel_oszlop.lower().count(t.lower())
        ossz += n1 + n2
        print('  %r: gerinc %d, Jelentés-oszlop %d' % (t, n1, n2))
    print('összesen:', ossz)

    print('\n## 2. (fordításra vár) előtte / utána')
    a, b = jelolesek_kulcsonkent(regi), jelolesek_kulcsonkent(uj)
    print('előtte: %d, utána: %d' % (sum(a.values()), sum(b.values())))
    for k in sorted(set(a) | set(b)):
        print('  %s: %d → %d' % (k, a.get(k, 0), b.get(k, 0)))

    print('\n## 3. A 32 sor „Jelentés (a szó)” cellája')
    fej = uj.split('| Igehely | Kulcsszó |', 1)[1].split('\n', 1)[0]
    print('fejléc: | Igehely | Kulcsszó |' + fej)
    nincs = 0
    for s in sorok:
        cellak = s.split(' | ')
        ige = re.match(r'\| \[([^\]]+)\]', s).group(1)
        jel = cellak[2]
        if 'nincs hozzárendelés' in jel.split(';')[0] or 'nincs címke' in jel:
            nincs += 1
        print('  %s: %s' % (ige, jel))
    print('sorok: %d; az elsődleges tokenen címke nélkül: %d' % (len(sorok), nincs))

    print('\n## 3/b. Az „UBS-jelentés” oszlop ÓSZ-sorai (DT-F131j)')
    osz = [s for s in sorok if '`0' in s.split(' | ')[6] or 'ÓSZ' in s.split(' | ')[6]]
    dbh = [s for s in osz if '`0' in s.split(' | ')[6]]
    print('ÓSZ-sor: %d; DBH-jelentéssel: %d; hivatkozás nélkül (kimondva): %d' % (
        len(osz), len(dbh), sum(1 for s in osz if 'nincs DBH-hivatkozás' in s.split(' | ')[6])))
    print('DBH-lexid a cellákban összesen: %d; ebből (fordításra vár): %d' % (
        sum(s.split(' | ')[6].count('`0') for s in dbh), sum(s.split(' | ')[6].count(JEL) for s in dbh)))
    for s in osz:
        if 'nincs DBH-hivatkozás' in s.split(' | ')[6]:
            print('  hivatkozás nélkül: %s — %s' % (re.match(r'\| \[([^\]]+)\]', s).group(1), s.split(' | ')[6]))

    print('\n## 4. Kiemelt szótári példahelyek')
    _, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
    sorai = [s for s in elo if s['id'] == 'ISTENTISZT-001']
    adat = LG.gerinc_adat()
    for szotar, strong in (('BDB', 'H7121'), ('BDB', 'H8034'), ('Thayer', 'G1941')):
        _bek, napl = LG.gerinc_blokk(adat, szotar, strong, sorai)
        print('%s %s: kiemelt %d; meg nem talált %d; a szótár nem idézi %d'
              % (szotar, strong, len(napl['kiemelt']), len(napl['nem_talalt']), len(napl['nem_idezett'])))
        for x in napl['kiemelt']:
            print('    kiemelt: %s' % x)
        for x in napl['nem_talalt']:
            print('    NEM TALÁLT: %s' % x)
        print('    nem idézi: %s' % ', '.join(napl['nem_idezett']))
        for x in napl.get('tiltott', []):
            print('    TILTOTT FORDULAT (ismert hiány): %s' % x)

    print('\n## 5. Hash-rögzítés (DT-F131h, DT-F131a (iv))')
    for rel in ('adat/bdb_szakaszok.tsv', 'adat/bdb_szakasz_hu.tsv', 'adat/glosszak_heber_hu.tsv'):
        n, h = sor_hash(rel, {'H7121', 'H8034'})
        print('  %s H7121+H8034: %d sor, sha1 %s' % (rel, n, h))


if __name__ == '__main__':
    main()
