"""F09 S2.5b (DT187 (1)): a H8034 TBESH-sora a lexikon_hivatkozasok.tsv-be, az F6.3-minta szerint.

Jelolt-sor nelkul (a jeloltek.tsv kulcsa id + igehely, a szotari szocikknek nincs igehelye),
a konkordancia/TBESH.txt H8034 sorabol szo szerinti kivonattal; a szkript ellenorzi, hogy a
szoveg_en reszsztringje a forras (HTML-jelolesektol megtisztitott, szokozoket osszevont) sorszovegenek,
es -- ha a helyben el konszolidalt tabla megvan -- hogy azonos a konszolidalt `teljes_szoveg`-gel.
A magyar fordites a forditasok.tsv-ben (itt nincs: "fordításra vár"). Iras: '\\t'.join.

    python naplok/F09_S2_5b_h8034_bekotes.py         # szarazon
    python naplok/F09_S2_5b_h8034_bekotes.py --ir    # ir
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import hashlib
import io
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HIV = os.path.join(ROOT, 'adat', 'lexikon_hivatkozasok.tsv')
TBESH_TXT = os.path.join(ROOT, 'konkordancia', 'TBESH.txt')
KONSZ = os.path.join(ROOT, 'konkordancia', '_nyers', 'tbesh', 'TBESH_konszolidalt.tsv')
HEADER = ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forrasfajl']

# 1. a forrassor
raw = None
with io.open(TBESH_TXT, encoding='utf-8') as f:
    for sor in f:
        if sor.startswith('H8034\t'):
            if raw is not None:
                raise SystemExit('tobb H8034 sor a TBESH.txt-ben')
            raw = sor.rstrip('\r\n').split('\t')[-1]
if raw is None:
    raise SystemExit('nincs H8034 sor a TBESH.txt-ben')
tiszta = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw)).strip()
szoveg_en = tiszta
print('forras (TBESH.txt, HTML-tol megtisztitva):', szoveg_en)

# 1b. VALODI osszevetes (J5, ellenori 5.): a TBESH.txt 10842. sora (sorszam szerint, fuggetlenul
# a fenti keresestol) szoveg-mezeje, megtisztitva, egyezzen a kivonattal; es -- ha a sor mar
# benne van a lexikon_hivatkozasok.tsv-ben -- az ott tarolt szoveg_en is egyezzen vele.
SORSZAM = 10842
sor_10842 = None
with io.open(TBESH_TXT, encoding='utf-8') as f:
    for n, sor_ in enumerate(f, 1):
        if n == SORSZAM:
            sor_10842 = sor_.rstrip('\r\n')
            break
if sor_10842 is None:
    raise SystemExit('a TBESH.txt-nek nincs %d. sora' % SORSZAM)
m_ = sor_10842.split('\t')
assert m_[0] == 'H8034', 'a %d. sor nem a H8034: %r' % (SORSZAM, m_[0])
tiszta_10842 = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m_[-1])).strip()
assert tiszta_10842 == szoveg_en, 'a kivonat nem egyezik a TBESH.txt %d. sorával' % SORSZAM
print('TBESH.txt %d. sora == kivonat: igaz' % SORSZAM)
with io.open(HIV, encoding='utf-8', newline='') as f:
    for l_ in f.read().split('\n'):
        c_ = l_.split('\t')
        if c_[:4] == ['H8034', 'TBESH', 'H8034', 'teljes']:
            assert c_[4] == tiszta_10842, 'a tabla szoveg_en nem egyezik a TBESH.txt %d. sorával' % SORSZAM
            print('lexikon_hivatkozasok.tsv H8034/TBESH sor szoveg_en == TBESH.txt %d. sora: igaz' % SORSZAM)

# 2. keresztellenorzes a konszolidalt tablaval (ha megvan)
if os.path.isfile(KONSZ):
    konsz = None
    with io.open(KONSZ, encoding='utf-8') as f:
        for sor in f:
            m = sor.rstrip('\n').split('\t')
            if m[0] == 'H8034':
                konsz = m
    assert konsz is not None
    print('konszolidalt teljes_szoveg egyezik:', konsz[6] == szoveg_en, '(forras=%s)' % konsz[7])
    assert konsz[6] == szoveg_en, 'a kivonat nem egyezik a konszolidalt tablaval'

sor = dict(zip(HEADER, ['H8034', 'TBESH', 'H8034', 'teljes', szoveg_en, 'konkordancia/TBESH.txt']))
for k, v in sor.items():
    assert '\t' not in v and '\n' not in v, k

# 3. a meglevo tabla: nincs mar ilyen sor; a meglevo sorok valtozatlanok (elotag)
with io.open(HIV, encoding='utf-8', newline='') as f:
    regi = f.read()
assert '\r' not in regi
for l in regi.split('\n'):
    m = l.split('\t')
    if len(m) >= 4 and m[:4] == ['H8034', 'TBESH', 'H8034', 'teljes']:
        if '--ir' in sys.argv:
            raise SystemExit('mar van ilyen sor -- nem irok ujra')
        print('a sor mar a tablaban van; az ellenorzes fent lefutott, nincs ujrairas')
        sys.exit(0)
uj = regi if regi.endswith('\n') else regi + '\n'
uj += '\t'.join(sor[k] for k in HEADER) + '\n'
assert uj.startswith(regi)
print('sha1(szoveg_en)  =', hashlib.sha1(szoveg_en.encode('utf-8')).hexdigest())
print('sha256(TBESH.txt)=', hashlib.sha256(open(TBESH_TXT, 'rb').read()).hexdigest())
print('sha256(forras-mezo)=', hashlib.sha256(raw.encode('utf-8')).hexdigest())
if '--ir' in sys.argv:
    with io.open(HIV, 'w', encoding='utf-8', newline='') as f:
        f.write(uj)
    print('irva:', HIV)
