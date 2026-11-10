"""F105 (FELADATOK #105; ELLENOR_F105 3.): vak minta a rafe-maqqéf szabály (`eszkozok/bdb_rovidites.maqqef_javit`) kézi
ellenőrzéséhez, két független kitöltőnek.

Pool: a BDB-szócikkek (`konkordancia/BDB_teljes_unabridged.tsv`, a szeletelő `lapit` alakjában, a megjelenítés szórend-
cseréje után) héber futamainak azon szavai, amelyekben pontosan egy rafe (U+05BF) áll, a szabály a szón belül maqqéfet tesz,
és a futamot közvetlenül hivatkozás követi (Károli-vers a `bdb_vers_jelentes.tsv`-ből, nem kiszűrve; a futam és a hivatkozás
között csak írásjel, zárójel, szóköz, „&c.”). A két jelölt:
  - a szabály kimenete;
  - az alternatíva: a szóhatár a rafét hordozó betű másik oldalán; ha ott nem értelmezhető (a szó elejére vagy végére esne),
    maqqéf nélkül, összevonva.
A hivatkozott vers dönt, ha (TAHOT, a Károli-kulcson; mássalhangzó-váz, végbetű alapbetűre, pe = mem) a jelölt részei a vers
egymást követő TAHOT-sorainak (morfémáinak) összefűzései: bontásnál pontosan az egyik jelölt áll; összevonásnál a szabály
bontása nem áll, az egész szó igen. A mintába csak az eldönthető szavak kerülnek (seed 1051, 50 tétel, vagy a teljes pool, ha
kisebb).

Kimenet a `--ki` könyvtárba (a repón KÍVÜL; nem commitoljuk):
  - `vak_minta.md`: tételenként sorszám, Károli-kulcs, a vers héber szövege (TAHOT, morfémák szóközzel), A és B. A futam többi
    szava a két jelöltben azonos; a geres mindkettőből kikerül. Nincs benne Strong, állapot, gépi döntés, szabályra utalás.
  - `kulcs.tsv`: sorszám, és melyik betű (A/B) a szabályé.
Az A/B tételenként rögzített seeddel (`random.Random(105100 + sorszám)`) véletlen. Gépi ellenőrzés a kiírás előtt: egyik
jelöltben sincs rafe vagy geres, és a két jelölt betűsora (váz) azonos; eltérésnél a szkript megáll.
Futtatás: python naplok/F105_vak_maqqef.py --ki <könyvtár a repón kívül>
"""
import argparse
import os
import random
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'olvaso_szerver'))
import bdb_rovidites as BR  # noqa: E402
import bdb_szelet  # noqa: E402

BDB = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
VJ = os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')
H = '֑-ׇא-״יִ-ﭏ'
FUTAM_RE = re.compile(r'[%s]+(?: [%s]+)*' % (H, H))
KOZ_RE = re.compile(r'^(?:[\s,;:.()\[\]‎]|&c\.?)*$')
GERES = '׳'
VEGBETU = dict(zip('כמנפצ', 'ךםןףץ'))


def tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r').split('\t') for s in f if not s.startswith('#')]
    return [dict(zip(sorok[0], s)) for s in sorok[1:]]


def pad(st):
    m = re.match(r'^H(\d+)(.*)$', st or '')
    return 'H%04d%s' % (int(m.group(1)), m.group(2)) if m else st


def vaz(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if 'א' <= c <= 'ת')
    return s.translate(str.maketrans('ךםןףץפ', 'כמנפצמ')).replace('פ', 'מ')


def betu(c):
    return 'א' <= c <= 'ת'


def alt_bontas(szo, k):
    """A szó (NFD, rafe nélkül) maqqéffel a k-adik betű előtt; az előtte álló betű végbetű-alakra."""
    ki, n, kesz = [], 0, False
    for c in szo:
        if betu(c):
            if n == k and not kesz:
                j = len(ki) - 1
                while j >= 0 and not betu(ki[j]):
                    j -= 1
                if j >= 0 and ki[j] in VEGBETU:
                    ki[j] = VEGBETU[ki[j]]
                ki.append('־')
                kesz = True
            n += 1
        ki.append(c)
    return ''.join(ki)


def illeszt(sorok, reszek):
    """Van-e i, és utána egymást követő sor-tartományok, amelyek összefűzése sorban a részeket adja."""
    n = len(sorok)
    for i in range(n):
        p, ok = i, True
        for r in reszek:
            acc, q = '', p
            while q < n and len(acc) < len(r):
                acc += sorok[q]
                q += 1
            if acc != r:
                ok = False
                break
            p = q
        if ok:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki', required=True)
    a = ap.parse_args()
    ki = os.path.abspath(a.ki)
    if os.path.commonpath([ki, REPO]) == REPO:
        sys.exit('A kimenet a repón kívülre menjen: %s' % ki)
    versek, versszoveg = {}, {}
    for d in tsv(TAHOT):
        versek.setdefault(d['Igehely'], []).append(vaz(d.get('Ragozott alak', '')))
        versszoveg.setdefault(d['Igehely'], []).append(d.get('Ragozott alak', '').strip())
    hiv = {}
    for d in tsv(VJ):
        hiv.setdefault(pad(d['strong']), []).append((int(d['poz']), d.get('karoli_vers', ''), d.get('szurt', '')))
    for v in hiv.values():
        v.sort()
    pool = []
    for d in tsv(BDB):
        st = d['Strong_padded']
        flat = BR._sorrend_csere(bdb_szelet.lapit(d['Teljes_szocikk']), st)   # a csere hosszt tart: a poz érvényes
        for m in FUTAM_RE.finditer(flat):
            futam = m.group(0)
            if BR.RAFE not in futam:
                continue
            vers = None
            for hp, kar, szurt in hiv.get(st, []):
                if hp >= m.end():
                    if KOZ_RE.match(flat[m.end():hp]) and kar and szurt != '1':
                        vers = kar
                    break
            if not vers or vers not in versek:
                continue
            tok = futam.split(' ')
            for ti, w in enumerate(tok):
                if w.count(BR.RAFE) != 1:
                    continue
                szabaly = BR.maqqef_javit(w)
                if BR.MAQQEF not in szabaly or BR.RAFE in szabaly:
                    continue
                nfd = unicodedata.normalize('NFD', w)
                bi, n = None, -1
                for c in nfd:
                    if betu(c):
                        n += 1
                    elif c == BR.RAFE:
                        bi = n
                hossz = len(vaz(w))
                k = len(vaz(szabaly.split(BR.MAQQEF)[0]))
                alt_k = bi + 1 if k == bi else bi
                tiszta = nfd.replace(BR.RAFE, '')
                if 0 < alt_k < hossz:
                    alt = alt_bontas(tiszta, alt_k)
                    s_ok = illeszt(versek[vers], [vaz(x) for x in szabaly.split(BR.MAQQEF)])
                    a_ok = illeszt(versek[vers], [vaz(x) for x in alt.split(BR.MAQQEF)])
                    dont = s_ok != a_ok
                else:
                    alt = tiszta
                    dont = (not illeszt(versek[vers], [vaz(x) for x in szabaly.split(BR.MAQQEF)])
                            and illeszt(versek[vers], [vaz(tiszta)]))
                if not dont:
                    continue
                kozos = [BR.maqqef_javit(t) for t in tok]
                pool.append((vers, kozos, ti, szabaly, alt))
    rnd = random.Random(1051)
    minta = rnd.sample(pool, 50) if len(pool) > 50 else list(pool)
    md = ['# Vak minta: a maqqéf (szóhatár) helye a BDB héber idézeteiben (%d tétel)' % len(minta), '',
          '**Jelölés: a geres mindkét jelöltből eltávolítva (rövidítésjel); a kérdés csak a szóhatár (maqqéf) helye.**', '',
          'Tételenként: a hivatkozott vers (Károli-kulcs), a vers héber szövege (TAHOT; morfémánként tagolva, ezért egyes '
          'előtagok és végződések külön állnak), és ugyanannak az idézetnek két alakja, A és B; a kettő csak egy szóhatárban '
          'különbözik. Kérdés: melyik alak szóhatára egyezik a vers szövegével? Válasz: A / B / nem tudom.', '']
    kulcs, hiba = ['sorszam\tszabaly'], 0
    for i, (vers, kozos, ti, szabaly, alt) in enumerate(minta, 1):
        sz = [t.replace(GERES, '') for t in kozos]
        jel_s = ' '.join(sz[:ti] + [szabaly.replace(GERES, '')] + sz[ti + 1:])
        jel_a = ' '.join(sz[:ti] + [unicodedata.normalize('NFC', alt).replace(GERES, '')] + sz[ti + 1:])
        for x in (jel_s, jel_a):
            if BR.RAFE in x or GERES in x:
                hiba += 1
        if vaz(jel_s) != vaz(jel_a) or jel_s == jel_a:
            hiba += 1
        a_szab = random.Random(105100 + i).random() < 0.5
        A, B = (jel_s, jel_a) if a_szab else (jel_a, jel_s)
        md += ['## %d.' % i, '', '- vers: %s' % vers,
               '- a vers héber szövege: %s' % ' '.join(x for x in versszoveg[vers] if x),
               '- A: %s' % A, '- B: %s' % B, '- válasz: ', '']
        kulcs.append('%d\t%s' % (i, 'A' if a_szab else 'B'))
    if hiba:
        sys.exit('MEGÁLL: %d ellenőrzési hiba (rafe / geres / eltérő betűsor / azonos jelölt); nem ír' % hiba)
    os.makedirs(ki, exist_ok=True)
    with open(os.path.join(ki, 'vak_minta.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md))
    with open(os.path.join(ki, 'kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(kulcs) + '\n')
    print('pool (eldönthető): %d | minta: %d | A = szabály: %d | ellenőrzés: rafe 0, geres 0, eltérő betűsor 0' % (
        len(pool), len(minta), sum(1 for s in kulcs[1:] if s.endswith('A'))))


if __name__ == '__main__':
    main()
